# Language Feature Providers

Reference detail for `vscode.languages` provider interfaces. Every registration returns a `Disposable` — push it into `context.subscriptions` at the moment you create it.

## Contents

- [Registration and DocumentSelector](#registration-and-documentselector)
- [HoverProvider](#hoverprovider)
- [CompletionItemProvider](#completionitemprovider)
- [CodeActionProvider](#codeactionprovider)
- [CodeLensProvider](#codelensprovider)
- [Definition, References, Document Symbols](#definition-references-document-symbols)
- [Formatting providers](#formatting-providers)
- [Diagnostics](#diagnostics)
- [Cancellation done properly](#cancellation-done-properly)
- [Debounce and cache pattern](#debounce-and-cache-pattern)

---

## Registration and DocumentSelector

All providers register as `vscode.languages.register<X>Provider(selector, provider, ...extras)`; the extras differ per type.

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  const selector: vscode.DocumentSelector = { language: 'yaml', scheme: 'file' };

  context.subscriptions.push(
    vscode.languages.registerHoverProvider(selector, new MyHoverProvider()),
    vscode.languages.registerCompletionItemProvider(
      selector, new MyCompletionProvider(), '.', ':'   // trigger characters
    ),
    vscode.languages.registerCodeActionsProvider(selector, new MyCodeActionProvider(), {
      providedCodeActionKinds: [vscode.CodeActionKind.QuickFix],
    }),
  );
}
```

A `DocumentFilter` has three optional fields; a `DocumentSelector` is one filter, a language-id string, or an array of either.

```typescript
const loose: vscode.DocumentSelector = 'typescript';                        // any TS document
const tight: vscode.DocumentSelector = { language: 'typescript', scheme: 'file' };
const byPath: vscode.DocumentSelector = { scheme: 'file', pattern: '**/config/*.json' };
const many: vscode.DocumentSelector = [
  { language: 'javascript', scheme: 'file' },
  { language: 'javascript', scheme: 'untitled' },
];
```

**`scheme` is the field people forget, and it is the one that produces bug reports.** Matching on `{ language: 'x' }` alone also matches `untitled:` (never saved, so `uri.fsPath` points at nothing), `git:` (the read-only left side of a diff view), `output:`, `vscode-notebook-cell:`, and extension-provided virtual schemes.

So: if the provider shells out to a tool, reads the file from disk, or resolves paths relative to the file's real location, add `scheme: 'file'`. Otherwise it runs against a git-diff pane, throws or returns nonsense, and the user reports "hover is broken in diffs." If the provider works purely from `document.getText()`, leaving the scheme open is a feature — completion in an untitled scratch buffer is useful.

**Multiple extensions can register for the same selector.** VS Code calls all of them and merges: hovers stack, completion lists concatenate, code actions all appear in the lightbulb. There is no return value meaning "ignore the others," so never assume you are alone, and never duplicate what a built-in provider already supplies — two identical completion items is a visible defect. Returning `undefined` is not failure; it lets the others' results stand.

---

## HoverProvider

```typescript
class MyHoverProvider implements vscode.HoverProvider {
  provideHover(
    document: vscode.TextDocument,
    position: vscode.Position,
    token: vscode.CancellationToken
  ): vscode.ProviderResult<vscode.Hover> {
    const range = document.getWordRangeAtPosition(position, /[A-Za-z_][\w.-]*/);
    if (!range) { return undefined; }          // nothing under the cursor — normal

    const info = this.lookup(document.getText(range));
    if (!info) { return undefined; }

    const md = new vscode.MarkdownString();
    md.appendMarkdown(`**${info.title}**\n\n${info.summary}\n\n`);
    md.appendCodeblock(info.signature, 'typescript');

    // Command links are inert unless the string is trusted. Only set isTrusted
    // when every command URI in it was built by you — a trusted string built
    // from workspace content is a command-execution vector.
    md.isTrusted = true;
    const args = encodeURIComponent(JSON.stringify([info.id]));
    md.appendMarkdown(`\n\n[Open definition](command:myExt.openDef?${args})`);

    return new vscode.Hover(md, range);        // passing range stops popup flicker
  }
}
```

`ProviderResult<T>` allows `T`, `undefined`, `null`, or a `Thenable` of those — async is fine.

**Hover fires on mouse movement.** Anything beyond a few milliseconds is felt as editor-wide sluggishness, because you are on the shared host. No synchronous file reads, no uncached process spawns. Supplying the `range` also matters for UX: without it VS Code guesses the hover region and the popup flickers as the mouse moves inside one word.

---

## CompletionItemProvider

```typescript
class MyCompletionProvider implements vscode.CompletionItemProvider {
  provideCompletionItems(
    document: vscode.TextDocument,
    position: vscode.Position,
    token: vscode.CancellationToken,
    context: vscode.CompletionContext
  ): vscode.ProviderResult<vscode.CompletionItem[] | vscode.CompletionList> {
    const linePrefix = document.lineAt(position).text.slice(0, position.character);
    if (!linePrefix.endsWith('.')) { return undefined; }

    return this.members().map((m, i) => {
      const item = new vscode.CompletionItem(m.name, vscode.CompletionItemKind.Method);

      item.sortText = String(i).padStart(4, '0');  // list order; label is the fallback
      item.filterText = m.name;                    // what typing is matched against
      item.preselect = m.isCommon;                 // highlighted when the list opens

      // SnippetString gives tab stops; a plain string inserts literally.
      item.insertText = new vscode.SnippetString(`${m.name}(\${1:${m.firstParam}})$0`);

      // Explicit range = explicit replacement. Without it VS Code infers the
      // replaced range from the current word — usually, but not always, right.
      item.range = document.getWordRangeAtPosition(position)
        ?? new vscode.Range(position, position);

      (item as any).data = { id: m.id };           // carried into resolve
      return item;
    });
  }

  async resolveCompletionItem(
    item: vscode.CompletionItem,
    token: vscode.CancellationToken
  ): Promise<vscode.CompletionItem> {
    const id = (item as any).data?.id;
    if (!id) { return item; }

    const docs = await this.fetchDocs(id, token);  // only for the highlighted item
    if (token.isCancellationRequested) { return item; }

    item.documentation = new vscode.MarkdownString(docs.markdown);
    item.detail = docs.signature;
    return item;
  }
}
```

**`resolveCompletionItem` is the performance mechanism, not a nicety.** `provideCompletionItems` may return hundreds of items and fires on nearly every keystroke; `resolveCompletionItem` runs for at most one item — the one currently highlighted. So put label, kind, sortText, filterText, insertText and range in `provide`, and `documentation`, `detail`, and expensive `additionalTextEdits` (auto-import lines) in `resolve`.

Resolve must not change `label`, `filterText`, `sortText`, or `insertText`: the list is already rendered and filtered by then, so those changes are ignored or produce inconsistent behavior.

- **Trigger characters** are the trailing varargs at registration. They invoke the provider when that character is typed; `context.triggerKind` and `context.triggerCharacter` tell you which path you are on. Without them you are only called on explicit invoke and normal word typing.
- `new vscode.CompletionList(items, /* isIncomplete */ true)` makes VS Code re-query on every further keystroke instead of filtering client-side. Correct for server-side prefix search; otherwise it multiplies your call count.
- `CompletionItemKind` drives the icon and some sorting. Pick the honest one.
- `item.commitCharacters` makes a character both accept the item and get inserted. Use sparingly — surprise commits infuriate users.

---

## CodeActionProvider

```typescript
class MyCodeActionProvider implements vscode.CodeActionProvider {
  provideCodeActions(
    document: vscode.TextDocument,
    range: vscode.Range | vscode.Selection,
    context: vscode.CodeActionContext,
    token: vscode.CancellationToken
  ): vscode.ProviderResult<(vscode.CodeAction | vscode.Command)[]> {
    const actions: vscode.CodeAction[] = [];

    // context.diagnostics holds only diagnostics intersecting `range`, from
    // every source. Filter to your own.
    for (const diag of context.diagnostics) {
      if (diag.source !== 'myExt' || diag.code !== 'unknown-key') { continue; }

      const suggestion = this.suggest(diag);
      const fix = new vscode.CodeAction(
        `Replace with "${suggestion}"`, vscode.CodeActionKind.QuickFix);
      fix.edit = new vscode.WorkspaceEdit();
      fix.edit.replace(document.uri, diag.range, suggestion);
      fix.diagnostics = [diag];   // links the fix to the squiggle in the UI
      fix.isPreferred = true;     // eligible for the auto-fix / "Fix All" path
      actions.push(fix);
    }

    if (!range.isEmpty) {
      // Command instead of edit: VS Code runs the command, which can be async,
      // prompt the user, or apply its own WorkspaceEdit.
      const extract = new vscode.CodeAction(
        'Extract to variable', vscode.CodeActionKind.RefactorExtract);
      extract.command = {
        command: 'myExt.extractVariable',
        title: 'Extract to variable',
        arguments: [document.uri, range],
      };
      actions.push(extract);
    }

    return actions;
  }
}
```

**Edit vs Command.** Use `action.edit` when the change is a pure text transformation known now — VS Code applies it as one undoable operation and can preview it. Use `action.command` when the action must ask the user something, do async work, or touch things outside the text. Both together is legal: edit applies first, then the command runs.

**`providedCodeActionKinds` metadata matters.** VS Code filters by kind *before* calling you, so "Organize Imports" only wakes providers that declared `SourceOrganizeImports`. Declare what you return: undeclared kinds never surface in the filtered menus that request them, and undeclared-but-unreturned kinds get you called for nothing.

Kinds are hierarchical strings: `QuickFix` (`quickfix`); `Refactor` (`refactor`) with `RefactorExtract`/`RefactorInline`/`RefactorRewrite`; `Source` (`source`) with `SourceOrganizeImports` and `SourceFixAll`. Only `Source` actions are eligible for `editor.codeActionsOnSave` — which is why `SourceFixAll` is the kind for a "clean this file on save" action.

`context.only` means the client is asking for one specific kind; returning anything outside it is wasted work.

---

## CodeLensProvider

```typescript
class MyCodeLensProvider implements vscode.CodeLensProvider {
  private readonly onDidChange = new vscode.EventEmitter<void>();
  public readonly onDidChangeCodeLenses = this.onDidChange.event;

  constructor(context: vscode.ExtensionContext) {
    context.subscriptions.push(
      this.onDidChange,
      vscode.workspace.onDidChangeConfiguration(e => {
        if (e.affectsConfiguration('myExt.showLenses')) { this.onDidChange.fire(); }
      })
    );
  }

  provideCodeLenses(
    document: vscode.TextDocument,
    token: vscode.CancellationToken
  ): vscode.ProviderResult<vscode.CodeLens[]> {
    const lenses: vscode.CodeLens[] = [];
    for (let line = 0; line < document.lineCount; line++) {
      if (token.isCancellationRequested) { return []; }
      if (/^\s*(export\s+)?function\s/.test(document.lineAt(line).text)) {
        lenses.push(new vscode.CodeLens(new vscode.Range(line, 0, line, 0)));
      }
    }
    return lenses;   // no command yet — resolve fills it in
  }

  async resolveCodeLens(
    lens: vscode.CodeLens,
    token: vscode.CancellationToken
  ): Promise<vscode.CodeLens> {
    const count = await this.countReferences(lens.range, token);   // expensive
    if (token.isCancellationRequested) { return lens; }
    lens.command = {
      title: `${count} reference${count === 1 ? '' : 's'}`,
      command: 'myExt.showReferences',
      arguments: [lens.range],
    };
    return lens;
  }
}
```

Same lazy split as completion: `provideCodeLenses` finds positions cheaply and returns lenses **without** a command; `resolveCodeLens` fills the command in, and only for lenses currently in the viewport. A lens with no command and no resolve renders as nothing.

`onDidChangeCodeLenses` is the refresh mechanism — firing it discards current lenses and re-runs `provideCodeLenses`. Wire it to whatever the lens content depends on (saves, config, a background analysis finishing) and debounce it, since each fire re-runs the whole pass. Dispose the `EventEmitter`.

---

## Definition, References, Document Symbols

```typescript
class MyDefinitionProvider implements vscode.DefinitionProvider {
  provideDefinition(
    document: vscode.TextDocument,
    position: vscode.Position,
    token: vscode.CancellationToken
  ): vscode.ProviderResult<vscode.Definition | vscode.LocationLink[]> {
    const target = this.resolveSymbol(document, position);
    if (!target) { return undefined; }

    return new vscode.Location(target.uri, target.range);

    // LocationLink is richer and gives better peek UX:
    //   originSelectionRange — what to underline in the source document
    //   targetRange          — the full symbol body, used for the peek preview
    //   targetSelectionRange — where the cursor lands (usually just the name)
    // return [{
    //   originSelectionRange: document.getWordRangeAtPosition(position),
    //   targetUri: target.uri,
    //   targetRange: target.fullRange,
    //   targetSelectionRange: target.nameRange,
    // }];
  }
}

class MyReferenceProvider implements vscode.ReferenceProvider {
  provideReferences(
    document: vscode.TextDocument,
    position: vscode.Position,
    context: vscode.ReferenceContext,     // honor context.includeDeclaration
    token: vscode.CancellationToken
  ): vscode.ProviderResult<vscode.Location[]> {
    return this.findAll(document, position, context.includeDeclaration, token);
  }
}
```

The same `Definition | LocationLink[]` shape is used by `registerTypeDefinitionProvider`, `registerImplementationProvider`, and `registerDeclarationProvider`.

`provideDocumentSymbols` may return `SymbolInformation[]` or `DocumentSymbol[]`. **Prefer `DocumentSymbol`** — it nests via `children`, so Outline and breadcrumbs show real structure, where `SymbolInformation` is flat with a `containerName` string that VS Code has to interpret. `SymbolInformation` remains correct for `WorkspaceSymbolProvider`, where results span files and there is no single tree.

```typescript
class MySymbolProvider implements vscode.DocumentSymbolProvider {
  provideDocumentSymbols(
    document: vscode.TextDocument,
    token: vscode.CancellationToken
  ): vscode.ProviderResult<vscode.DocumentSymbol[]> {
    const cls = new vscode.DocumentSymbol(
      'Widget',
      'class',                          // detail, shown greyed beside the name
      vscode.SymbolKind.Class,
      new vscode.Range(0, 0, 40, 0),    // full range — drives outline folding
      new vscode.Range(0, 6, 0, 12)     // selection range — MUST be inside full range
    );
    cls.children.push(new vscode.DocumentSymbol(
      'render', '(): void', vscode.SymbolKind.Method,
      new vscode.Range(5, 2, 12, 3), new vscode.Range(5, 2, 5, 8)));
    return [cls];
  }
}
```

A `selectionRange` not contained in `range` gets the symbol rejected — the most common cause of "my outline is empty."

---

## Formatting providers

Three registrations, three triggers, all returning `TextEdit[]`.

```typescript
// Whole document — "Format Document" and format-on-save.
vscode.languages.registerDocumentFormattingEditProvider(selector, {
  async provideDocumentFormattingEdits(document, options, token) {
    // options: { tabSize, insertSpaces, ... } — the editor's effective settings
    // for this document. Respect them; do not read your own indent config.
    const formatted = await runFormatter(document.getText(), options, token);
    if (token.isCancellationRequested) { return undefined; }

    const whole = new vscode.Range(
      document.positionAt(0), document.positionAt(document.getText().length));
    return [vscode.TextEdit.replace(whole, formatted)];
  },
});

// Selection — "Format Selection"; registering it also enables format-on-paste.
vscode.languages.registerDocumentRangeFormattingEditProvider(selector, {
  provideDocumentRangeFormattingEdits(document, range, options, token) {
    return formatRange(document, range, options, token);
  },
});

// As the user types. Only fires when editor.formatOnType is enabled.
vscode.languages.registerOnTypeFormattingEditProvider(selector, {
  provideOnTypeFormattingEdits(document, position, ch, options, token) {
    if (ch !== '}') { return undefined; }
    return [dedentClosingBrace(document, position)];
  },
}, '}', ';', '\n');   // first trigger char plus varargs
```

Prefer real range formatting over formatting the whole file and slicing — slicing mangles context-sensitive languages. Return `undefined` rather than an empty array when nothing changes. Never return overlapping ranges; the result is undefined behavior. Replacing the whole document is acceptable but produces a coarse undo entry and can move the viewport, so emit a minimal diff when you can compute one.

---

## Diagnostics

Diagnostics invert the model: nobody asks you. You own a `DiagnosticCollection` and write into it on your own schedule.

```typescript
export function activate(context: vscode.ExtensionContext) {
  // The name becomes the default `source` shown in the Problems panel.
  const diagnostics = vscode.languages.createDiagnosticCollection('myExt');
  context.subscriptions.push(diagnostics);

  const timers = new Map<string, NodeJS.Timeout>();

  const schedule = (document: vscode.TextDocument) => {
    if (document.languageId !== 'yaml' || document.uri.scheme !== 'file') { return; }
    const key = document.uri.toString();
    clearTimeout(timers.get(key));
    timers.set(key, setTimeout(() => {
      timers.delete(key);
      diagnostics.set(document.uri, analyze(document));
    }, 300));
  };

  context.subscriptions.push(
    vscode.workspace.onDidChangeTextDocument(e => schedule(e.document)),
    vscode.workspace.onDidOpenTextDocument(schedule),

    // CRITICAL. Without this the Problems panel keeps listing errors for a
    // document that is no longer open; clicking one reopens the file to show
    // a squiggle that is not there.
    vscode.workspace.onDidCloseTextDocument(document => {
      const key = document.uri.toString();
      clearTimeout(timers.get(key));
      timers.delete(key);
      diagnostics.delete(document.uri);
    }),
  );

  // Deleted or renamed on disk — close events do not always cover this.
  const watcher = vscode.workspace.createFileSystemWatcher('**/*.yaml');
  context.subscriptions.push(watcher, watcher.onDidDelete(uri => diagnostics.delete(uri)));

  vscode.workspace.textDocuments.forEach(schedule);  // already-open documents
}
```

Clearing rules, in order of how often they are missed:

1. `collection.delete(uri)` on document close and on file delete.
2. `collection.set(uri, [])` when a re-analysis finds nothing — the empty array is what removes old squiggles. Skipping the call because "there is nothing to report" leaves the previous errors up forever.
3. `collection.clear()` when the feature is disabled in settings, or its workspace folder is removed.
4. `collection.dispose()` via `context.subscriptions`.

```typescript
function analyze(document: vscode.TextDocument): vscode.Diagnostic[] {
  const diag = new vscode.Diagnostic(
    new vscode.Range(3, 2, 3, 10),
    'Key "retrys" is not recognized. Did you mean "retries"?',
    vscode.DiagnosticSeverity.Warning        // Error | Warning | Information | Hint
  );

  diag.source = 'myExt';                     // shown in Problems; code actions filter on it

  // A plain code, or a code with a docs link the user can click.
  diag.code = {
    value: 'unknown-key',
    target: vscode.Uri.parse('https://example.com/rules/unknown-key'),
  };

  // Point at the other place that matters — the schema, the conflicting
  // declaration, the original definition. Rendered as a nested entry.
  diag.relatedInformation = [
    new vscode.DiagnosticRelatedInformation(
      new vscode.Location(schemaUri, new vscode.Range(10, 0, 10, 20)),
      'Valid keys are declared here'),
  ];

  // Tags change rendering: Unnecessary greys out, Deprecated strikes through.
  diag.tags = [vscode.DiagnosticTag.Unnecessary];

  return [diag];
}
```

`DiagnosticSeverity.Hint` renders no squiggle at all — only a lightbulb. Right for "a refactor is available here," wrong for anything the user must notice.

---

## Cancellation done properly

Checking the token once at the end is close to useless. What matters is that the *underlying work* stops.

### Wrong

```typescript
async provideHover(document, position, token) {
  // Nothing here can be interrupted. The process runs to completion and the
  // request completes, both burning CPU on the shared extension host, for a
  // hover the user stopped caring about ten keystrokes ago.
  const analysis = await runAnalyzer(document.fileName);
  const docs = await fetch(`https://api.example.com/docs/${analysis.symbol}`);

  if (token.isCancellationRequested) { return undefined; }  // too late to matter
  return new vscode.Hover(await docs.text());
}
```

Under fast typing this queues one abandoned process and one abandoned request per keystroke. They all still resolve, still allocate, and still compete for the single event loop shared by the editor UI and every other extension. The user does not report "hover is slow" — they report "the editor stutters."

### Right

```typescript
import { spawn } from 'node:child_process';

function runAnalyzer(file: string, token: vscode.CancellationToken): Promise<string> {
  return new Promise((resolve, reject) => {
    const child = spawn('my-analyzer', ['--json', file]);

    const sub = token.onCancellationRequested(() => child.kill());  // actually kill it
    const timer = setTimeout(() => child.kill(), 5000);             // never hang forever

    let out = '';
    child.stdout.on('data', d => { out += d; });
    child.on('error', reject);
    child.on('close', code => {
      clearTimeout(timer);
      sub.dispose();                       // the listener is a Disposable too
      code === 0 ? resolve(out) : reject(new Error(`analyzer exited ${code}`));
    });
  });
}

function fetchDocs(symbol: string, token: vscode.CancellationToken): Promise<string> {
  const controller = new AbortController();
  const sub = token.onCancellationRequested(() => controller.abort());
  return fetch(`https://api.example.com/docs/${symbol}`, { signal: controller.signal })
    .then(r => r.text())
    .finally(() => sub.dispose());
}

async provideHover(
  document: vscode.TextDocument,
  position: vscode.Position,
  token: vscode.CancellationToken
): Promise<vscode.Hover | undefined> {
  const analysis = await runAnalyzer(document.fileName, token);
  if (token.isCancellationRequested) { return undefined; }   // check after EVERY await

  const docs = await fetchDocs(JSON.parse(analysis).symbol, token);
  if (token.isCancellationRequested) { return undefined; }

  return new vscode.Hover(new vscode.MarkdownString(docs));
}
```

Three habits, all required:

1. **Thread the token down** into every async helper. A helper that does not accept a token cannot be cancelled, and that is a bug on a provider path.
2. **Check after each `await`.** Each await is a point where the world may have moved on; work past it is work you will discard.
3. **`token.onCancellationRequested` returns a `Disposable`.** Dispose it when the operation settles, or you leak a listener per provider call — and providers are called constantly.

Cancellation is not an error path. Returning `undefined` on a cancelled token is the correct, quiet outcome: do not log it, do not surface it.

---

## Debounce and cache pattern

For expensive document-keyed providers. The cache key is `uri + version`.

```typescript
interface CacheEntry<T> { version: number; value: Promise<T>; }

/**
 * document.version is the correct cache key: VS Code increments it on every
 * single edit to that document. Same uri + same version means the text is
 * byte-identical and the cached result is still exactly correct; a changed
 * version means the entry is worthless. Hashing the text also works but costs
 * a full read per call, while the version number is already maintained for
 * you. Never key on uri alone — the file changes underneath and you serve
 * stale results indefinitely.
 */
export class DocumentCache<T> implements vscode.Disposable {
  private readonly entries = new Map<string, CacheEntry<T>>();
  private readonly disposables: vscode.Disposable[] = [];

  constructor(
    private readonly compute:
      (doc: vscode.TextDocument, token: vscode.CancellationToken) => Promise<T>
  ) {
    this.disposables.push(vscode.workspace.onDidCloseTextDocument(
      doc => this.entries.delete(doc.uri.toString())));
  }

  get(document: vscode.TextDocument, token: vscode.CancellationToken): Promise<T> {
    const key = document.uri.toString();
    const hit = this.entries.get(key);
    if (hit && hit.version === document.version) { return hit.value; }

    const value = this.compute(document, token);
    this.entries.set(key, { version: document.version, value });

    // A rejected promise must not stay cached, or the failure is permanent
    // until the next edit.
    value.catch(() => {
      if (this.entries.get(key)?.version === document.version) {
        this.entries.delete(key);
      }
    });

    return value;
  }

  dispose(): void {
    this.entries.clear();
    this.disposables.forEach(d => d.dispose());
  }
}

export function debounce<A extends unknown[]>(fn: (...args: A) => void, ms: number) {
  let timer: NodeJS.Timeout | undefined;
  const wrapped = (...args: A) => {
    if (timer) { clearTimeout(timer); }
    timer = setTimeout(() => { timer = undefined; fn(...args); }, ms);
  };
  wrapped.cancel = () => { if (timer) { clearTimeout(timer); timer = undefined; } };
  return wrapped;
}
```

Debounce belongs on the **push** side (diagnostics on change), not the pull side. Do not debounce inside `provideCompletionItems` — VS Code already asked, and delaying the answer just makes completion feel laggy; cache there instead. Keep typing-triggered windows at 200-500ms: longer feels broken, shorter defeats the purpose.

---

**Signature check.** Provider interfaces have gained members across releases (`CompletionItemProvider` generics, `CodeActionProvider.resolveCodeAction`, newer providers such as `DocumentPasteEditProvider`). Verify anything you have not used recently against the `vscode.d.ts` in the project's `@types/vscode`, and against the `engines.vscode` floor in `package.json` — an API newer than that floor compiles fine and throws at runtime on the user's older editor.
