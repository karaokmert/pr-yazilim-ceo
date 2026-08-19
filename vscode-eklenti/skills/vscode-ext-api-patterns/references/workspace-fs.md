# Workspace, Files, and Editors

Reference detail for `vscode.Uri`, `vscode.workspace`, and the document/editor APIs. The parent skill covers the rules; this file covers the shapes.

The governing idea: **the workspace is not necessarily on local disk.** Remote SSH, dev containers, WSL, GitHub Codespaces, the `vscode.dev` browser build, and virtual filesystems contributed by other extensions all present as ordinary workspaces. Code written against `vscode.Uri` and `workspace.fs` works in all of them. Code written against Node `path` and `fs` works in exactly one, and fails on a user's machine you will never see.

## Contents

- [Uri fundamentals](#uri-fundamentals)
- [workspace.fs](#workspacefs)
- [When node fs is acceptable](#when-node-fs-is-acceptable)
- [Workspace folders](#workspace-folders)
- [Finding files](#finding-files)
- [TextDocument and editors](#textdocument-and-editors)
- [Editing: WorkspaceEdit vs editor.edit](#editing-workspaceedit-vs-editoredit)
- [Position and Range](#position-and-range)
- [FileSystemWatcher](#filesystemwatcher)
- [Document events](#document-events)
- [Storage locations](#storage-locations)

---

## Uri fundamentals

A `Uri` is `scheme:` + `authority` + `path` + `query` + `fragment`. Everything addressable in VS Code is one — files, untitled buffers, Git blobs, settings, resources inside remote filesystems.

### Constructing

```typescript
import * as vscode from 'vscode';

// From an OS path. Handles Windows drive letters and separators correctly.
const a = vscode.Uri.file('/home/me/project/src/index.ts');
const w = vscode.Uri.file('C:\\Users\\me\\project\\src\\index.ts');

// From a full URI string. Requires a scheme — this is NOT for OS paths.
const b = vscode.Uri.parse('https://example.com/api?x=1');
const c = vscode.Uri.parse('untitled:Untitled-1');

// Joining. Use this instead of path.join or string concatenation:
// it preserves scheme and authority, so it works on remote and virtual uris.
const d = vscode.Uri.joinPath(folder.uri, 'src', 'index.ts');

// Deriving a variant while keeping everything else.
const e = d.with({ path: d.path + '.map' });
```

`Uri.parse(someOsPath)` is a recurring bug. `parse('/home/me/file.ts')` produces a Uri with an empty scheme; `parse('C:\\x\\y.ts')` interprets `c:` as the scheme. Use `Uri.file` for OS paths, `Uri.parse` for things that already look like URIs.

### scheme

The scheme tells you what kind of thing you are holding, and it is the check that prevents most cross-environment bugs.

| Scheme | What it is |
| --- | --- |
| `file` | A real file on the filesystem the extension host can see. |
| `untitled` | An unsaved buffer with no backing file. |
| `git` | A read-only Git blob (the left pane of a diff view). |
| `vscode-remote` | A file on a remote host, seen from a local UI extension. |
| `vscode-userdata` | Settings, keybindings, snippets. |
| `output`, `vscode-notebook-cell`, … | Virtual documents from various features. |
| anything else | A virtual filesystem contributed by another extension. |

Language providers get called on all of these. A provider registered on `'typescript'` without a `scheme` filter fires on Git diff panes and output channels too. If your feature only makes sense for real files, either filter the selector (`{ language: 'typescript', scheme: 'file' }`) or guard at the top:

```typescript
if (document.uri.scheme !== 'file') { return undefined; }
```

Writing to a `git:` uri fails. Running a formatter binary against a `vscode-remote:` path fails, because the path is not on the machine running your code.

### fsPath vs path

```typescript
uri.path     // Always the URI path component: forward slashes, percent-decoded.
uri.fsPath   // Platform-native OS path. Backslashes on Windows, drive letter, no leading slash.
```

**`fsPath` is only meaningful for the `file` scheme.** On any other scheme it produces a plausible-looking string that does not name anything on disk. That is the failure mode: it does not throw, it hands you a path, and the `fs.readFile` two lines later fails with ENOENT on a machine you cannot reproduce on.

The rule that follows:

- Use `fsPath` only when handing a path to something outside VS Code — a child process, a Node API — and only after confirming `scheme === 'file'`.
- Use `path` for comparisons, glob matching, and display of the URI-side identity.
- **Never compare Uris by string.** `uri.toString()` differs by percent-encoding and casing; `uri.fsPath` differs by Windows drive-letter casing. Compare `a.toString() === b.toString()` only for exact same-source values; for anything else compare `a.scheme === b.scheme && a.path === b.path`, or use the workspace's own helpers where they exist.
- `uri.toString()` percent-encodes. `uri.toString(true)` skips encoding, which is for display only — never round-trip a skip-encoding string back through `parse`.

## workspace.fs

`vscode.workspace.fs` implements `FileSystemProvider` operations over whatever filesystem the Uri names. It is async everywhere and byte-oriented.

```typescript
const fs = vscode.workspace.fs;

// Read and write are Uint8Array. There is no encoding parameter.
const bytes: Uint8Array = await fs.readFile(uri);
await fs.writeFile(uri, new Uint8Array([1, 2, 3]));

// Metadata.
const st: vscode.FileStat = await fs.stat(uri);
// st.type: FileType.File | Directory | SymbolicLink (a bitmask — symlinks combine)
// st.size, st.ctime, st.mtime

// Directories.
const entries: [string, vscode.FileType][] = await fs.readDirectory(dirUri);
await fs.createDirectory(dirUri);   // creates intermediate directories, like mkdir -p

// Mutation.
await fs.delete(uri, { recursive: true, useTrash: true });
await fs.rename(src, dest, { overwrite: false });
await fs.copy(src, dest, { overwrite: false });
```

### Text helpers

Since `readFile`/`writeFile` speak bytes, wrap them once rather than decoding at every call site:

```typescript
const decoder = new TextDecoder();          // defaults to utf-8
const encoder = new TextEncoder();          // always utf-8

export async function readText(uri: vscode.Uri): Promise<string> {
  return decoder.decode(await vscode.workspace.fs.readFile(uri));
}

export async function writeText(uri: vscode.Uri, content: string): Promise<void> {
  await vscode.workspace.fs.writeFile(uri, encoder.encode(content));
}
```

`writeFile` creates the file if missing and truncates if present, but it does **not** create missing parent directories on every provider. Call `createDirectory` on the parent first when you are not certain it exists.

### Absence is normal

`stat` on a missing file rejects with a `FileSystemError`. Since "not there" is an ordinary answer, ask rather than assume:

```typescript
export async function exists(uri: vscode.Uri): Promise<boolean> {
  try {
    await vscode.workspace.fs.stat(uri);
    return true;
  } catch (err) {
    if (err instanceof vscode.FileSystemError && err.code === 'FileNotFound') {
      return false;
    }
    throw err;   // permissions, unavailable provider — do not swallow these
  }
}
```

Catching everything and returning `false` hides permission errors and disconnected remotes as "file missing", which sends debugging in the wrong direction.

### useTrash

`delete(uri, { useTrash: true })` moves to the OS trash where the provider supports it, so a mistake is recoverable. Prefer it for anything the user could plausibly want back. It is not supported on every filesystem; a provider that cannot do it deletes permanently rather than failing.

### Reading a file that is open in an editor

`workspace.fs.readFile` reads *disk*. If the user has unsaved changes, you get the stale content. When a document may be open, read through the document API instead:

```typescript
const doc = await vscode.workspace.openTextDocument(uri);
const text = doc.getText();   // reflects unsaved edits
```

## When node fs is acceptable

Node `fs` is defensible when all three hold:

1. The path is **extension-owned**, not workspace content — `context.globalStorageUri`, a cache directory, a tool's own config in the home directory.
2. The extension is **confirmed desktop-only** (it already spawns processes, or `package.json` declares no `browser` entry point).
3. You have **checked or constructed** the Uri such that the scheme is `file`.

Even then, `context.globalStorageUri` on a remote workspace lives on the *remote* host, which is usually what you want but is worth being deliberate about.

```typescript
import * as fsNode from 'node:fs/promises';

// Desktop-only extension, extension-owned cache directory, file scheme guaranteed
// by construction from globalStorageUri. Node fs is used here for streaming support.
const cacheDir = context.globalStorageUri;
if (cacheDir.scheme !== 'file') {
  throw new Error('Cache requires a local filesystem.');
}
await fsNode.mkdir(cacheDir.fsPath, { recursive: true });
```

**State the reason in a comment when you make this call.** A future reader cannot distinguish a deliberate desktop-only decision from someone reaching for the familiar API, and the difference is whether the extension works in the browser.

Workspace content is never in this category. Reading the user's source files with Node `fs` is the specific mistake this whole section exists to prevent.

## Workspace folders

`workspace.workspaceFolders` is `readonly WorkspaceFolder[] | undefined`. Three states, all ordinary:

```typescript
const folders = vscode.workspace.workspaceFolders;

if (!folders || folders.length === 0) {
  // No folder open — the user opened a single file, or an empty window.
  // Not an error. Degrade: operate on the active editor, or explain and return.
  return;
}

if (folders.length === 1) {
  const root = folders[0];
  // root.uri, root.name, root.index
}

// Multi-root. Do not silently pick folders[0].
```

`workspaceFolders[0]` is the single most common crash in extension code, and the second most common bug (silently ignoring folders 2..n in a multi-root workspace).

### Resolving which folder a resource belongs to

```typescript
const folder = vscode.workspace.getWorkspaceFolder(someUri);
// undefined when the resource is outside every workspace folder —
// e.g. a file opened from elsewhere on disk, or a node_modules file
// under a folder that is not itself a workspace folder.
```

This is the correct way to scope per-folder configuration, per-folder tool invocation, and per-folder output.

### Scoping to the active editor's folder

When an operation is inherently single-folder (run a linter, open a config), the honest resolution order is: active editor's folder, then the only folder if there is exactly one, then ask.

```typescript
async function pickTargetFolder(): Promise<vscode.WorkspaceFolder | undefined> {
  const active = vscode.window.activeTextEditor?.document.uri;
  if (active) {
    const owner = vscode.workspace.getWorkspaceFolder(active);
    if (owner) { return owner; }
  }

  const folders = vscode.workspace.workspaceFolders ?? [];
  if (folders.length === 1) { return folders[0]; }
  if (folders.length === 0) { return undefined; }

  return vscode.window.showWorkspaceFolderPick({
    placeHolder: 'Select a folder to run in',
  });
}
```

`showWorkspaceFolderPick` returns `undefined` on dismissal, like every other picker.

### Display paths and change events

```typescript
// Workspace-relative for display. Includes the folder name in multi-root
// unless you pass false as the second argument.
const label = vscode.workspace.asRelativePath(uri);
const bare = vscode.workspace.asRelativePath(uri, false);

context.subscriptions.push(
  vscode.workspace.onDidChangeWorkspaceFolders(e => {
    // e.added, e.removed — rebuild per-folder state (watchers, caches, indexes)
    for (const removed of e.removed) { this.disposeFolderState(removed); }
    for (const added of e.added) { void this.initFolderState(added); }
  }),
);
```

If your extension keeps per-folder resources (a watcher each, a cached index each), this listener is not optional — without it, adding a folder to a live workspace produces a folder your extension never sees.

## Finding files

```typescript
const uris = await vscode.workspace.findFiles(
  '**/*.config.json',      // include: GlobPattern
  '**/node_modules/**',    // exclude: GlobPattern | null | undefined
  200,                     // maxResults
  token,                   // CancellationToken
);
```

### RelativePattern scopes the search

A bare string glob searches **every** workspace folder. To search one folder — or a directory that is not a workspace folder at all — use `RelativePattern`:

```typescript
const pattern = new vscode.RelativePattern(folder, 'src/**/*.ts');
const found = await vscode.workspace.findFiles(pattern, null, 100, token);

// Also accepts a Uri base, which is how you search below a subdirectory.
const subPattern = new vscode.RelativePattern(
  vscode.Uri.joinPath(folder.uri, 'packages'),
  '*/package.json',
);
```

### Exclusions

`findFiles` respects the user's `files.exclude` and `search.exclude` settings in addition to the exclude argument you pass. Consequences:

- Passing `undefined` as the exclude argument still applies the user's settings.
- Passing `null` explicitly disables the *default* exclusions — which means you will walk `node_modules` and `.git`. Rarely what you want.
- A file the user has excluded from search will not be returned, even if your extension needs it. If you must see excluded files, `readDirectory` traversal is the fallback.

### Cost

A broad glob on a large repository is genuinely slow — `**/*` on a monorepo can take seconds and produce tens of thousands of results.

- Always pass `maxResults` when you only need a bounded set. There is no streaming form; the promise resolves once, with everything.
- Always thread a `CancellationToken` through when the search backs a provider or a UI that the user can navigate away from.
- Anchor the glob as tightly as possible: `src/**/*.ts` beats `**/*.ts`, and a `RelativePattern` beats both.
- Cache results and invalidate from a `FileSystemWatcher` rather than re-running the search on every request.

## TextDocument and editors

### Opening

```typescript
// By Uri — the general form. Returns the already-open document if there is one.
const doc = await vscode.workspace.openTextDocument(uri);

// By OS path — convenience, file scheme only.
const doc2 = await vscode.workspace.openTextDocument('/abs/path/file.ts');

// A new untitled buffer with content. Nothing is written to disk.
const scratch = await vscode.workspace.openTextDocument({
  language: 'json',
  content: JSON.stringify(report, null, 2),
});
```

`openTextDocument` loads the document into memory and fires `onDidOpenTextDocument`; it does **not** show anything. Showing is a separate step:

```typescript
const editor = await vscode.window.showTextDocument(doc, {
  viewColumn: vscode.ViewColumn.Beside,
  preview: false,        // false = a real tab, not the italic preview tab
  preserveFocus: true,   // leave the cursor where the user had it
  selection: new vscode.Range(0, 0, 0, 0),
});
```

The `preview: false` distinction matters: opening several documents with the default `preview: true` reuses one tab, so each open replaces the previous one and the user ends up with only the last.

### Reading the current state

```typescript
const editor = vscode.window.activeTextEditor;
if (!editor) { return; }   // no active editor is normal — the user may be in a webview,
                           // in settings, in the terminal, or on the welcome page

const doc = editor.document;
const all = doc.getText();
const selected = doc.getText(editor.selection);   // empty string when the selection is empty
const line = doc.lineAt(editor.selection.active.line);
// line.text, line.range, line.rangeIncludingLineBreak,
// line.firstNonWhitespaceCharacterIndex, line.isEmptyOrWhitespace

vscode.window.visibleTextEditors;   // every editor currently on screen, including split panes
vscode.workspace.textDocuments;     // every open document, including ones with no visible editor
```

`activeTextEditor` is `undefined` far more often than it feels. `registerTextEditorCommand` exists precisely to spare you this check when a command is editor-only.

### Offsets and positions

```typescript
const offset: number = doc.offsetAt(position);
const position: vscode.Position = doc.positionAt(offset);
```

These are the bridge to any tool that speaks byte or character offsets — a parser, a regex over `getText()`, an AST. Convert at the boundary and stay in `Position` inside VS Code code.

Note the caveat: `offsetAt`/`positionAt` count UTF-16 code units, matching JavaScript string indices. A tool that reports UTF-8 byte offsets needs a real conversion, not a direct handoff, and the difference only shows up on files containing non-ASCII characters — which is exactly the kind of bug that ships.

### Document identity and state

```typescript
doc.uri;          // identity
doc.fileName;     // fsPath-flavored string; same caveats as fsPath
doc.languageId;   // 'typescript', 'json', ... — set by VS Code, changeable by the user
doc.version;      // increments on every change; the correct staleness check
doc.isDirty;      // has unsaved changes
doc.isUntitled;   // never saved to disk — has no meaningful fsPath
doc.isClosed;     // the document is gone; do not edit it
doc.eol;          // EndOfLine.LF | CRLF
doc.lineCount;
```

`doc.version` is how you detect that async work has been invalidated:

```typescript
const versionAtStart = doc.version;
const result = await expensiveAnalysis(doc.getText());
if (doc.version !== versionAtStart) { return; }   // the user typed; result is stale
applyResult(result);
```

Comparing text, or comparing timestamps, does not work — `version` is the intended mechanism.

## Editing: WorkspaceEdit vs editor.edit

### WorkspaceEdit

The general-purpose editing API. It spans multiple files, applies as **one undo step**, works on documents that are not open in any editor, and can create/rename/delete files in the same operation.

```typescript
const edit = new vscode.WorkspaceEdit();

edit.replace(docA.uri, rangeInA, 'newText');
edit.insert(docB.uri, new vscode.Position(0, 0), '// generated\n');
edit.delete(docB.uri, someRange);

// File operations participate in the same undo step.
edit.createFile(newUri, { overwrite: false, ignoreIfExists: true });
edit.renameFile(oldUri, newUri, { overwrite: false });
edit.deleteFile(deadUri, { recursive: false, ignoreIfNotExists: true });

const ok = await vscode.workspace.applyEdit(edit);
if (!ok) {
  vscode.window.showErrorMessage('Could not apply changes.');
  return;
}
```

**`applyEdit` returns a boolean and it can be `false`.** It fails when a target document changed underneath the edit, when a file is read-only, when the filesystem provider refuses, or when ranges conflict. Ignoring the return value produces the worst class of bug: the extension reports success and nothing happened.

Ranges inside a single `WorkspaceEdit` are all resolved against the document state *before* the edit, so you do not need to adjust later offsets for earlier insertions. Overlapping ranges are the exception — those are undefined behavior and should be merged before you build the edit.

`applyEdit` does not save. Follow with `doc.save()` if the change must reach disk, and consider that saving on the user's behalf triggers their format-on-save and other participants.

### editor.edit

Scoped to one visible editor, and the only way to change the selection as part of the same operation.

```typescript
const applied = await editor.edit(builder => {
  builder.replace(editor.selection, transformed);
  builder.insert(new vscode.Position(0, 0), header);
});
if (!applied) { return; }

editor.selection = new vscode.Selection(newStart, newEnd);
editor.revealRange(new vscode.Range(newStart, newEnd),
  vscode.TextEditorRevealType.InCenterIfOutsideViewport);
```

The callback must be synchronous. Awaiting inside it silently drops the edits queued after the await, because the edit builder is only valid for the duration of the call. Compute everything first, then call `edit`.

Two `editor.edit` calls are two undo steps, which is why a refactor implemented as a loop of `edit` calls makes the user press Ctrl+Z twelve times.

**Choose `WorkspaceEdit` unless you are editing only the active editor and need cursor control.** For code actions, refactors, quick fixes, and anything touching more than one file, `WorkspaceEdit` is the right answer — and for code actions specifically it is the required one, since the action carries the edit rather than applying it.

## Position and Range

```typescript
const pos = new vscode.Position(line, character);   // both ZERO-BASED
const range = new vscode.Range(startLine, startChar, endLine, endChar);
const range2 = new vscode.Range(startPos, endPos);
const sel = new vscode.Selection(anchorPos, activePos);
```

`Position` and `Range` are immutable. Methods return new instances:

```typescript
pos.translate(1, 0);              // one line down
pos.with({ character: 0 });       // start of the same line
range.with({ end: newEnd });
range.contains(pos);
range.intersection(other);        // Range | undefined
range.union(other);
range.isEmpty;                    // start equals end — a cursor, not a selection
range.isSingleLine;
```

`Selection extends Range` and adds direction:

- `anchor` — where the selection started (where the user pressed down).
- `active` — where the cursor is now (where the user dragged to).
- `isReversed` — true when the user selected backwards, i.e. `active` precedes `anchor`.

`start`/`end` inherited from `Range` are always ordered; `anchor`/`active` are not. Use `start`/`end` for text operations and `active` for "where is the cursor".

`editor.selections` (plural) is the multi-cursor case, and it always has at least one entry. A command that only handles `editor.selection` works but quietly ignores the other cursors, which is a real bug report for users who live in multi-cursor mode.

### The off-by-one

**VS Code lines and characters are zero-based. Almost every external tool reports one-based lines, and many report one-based columns too.** Compilers, linters, `grep -n`, stack traces, `tsc` output, ESLint, most language servers speaking their own protocol.

The conversion is one subtraction and it is forgotten constantly. The symptom is diagnostics and highlights that are consistently one line high — visible enough to notice, subtle enough to ship.

Make the conversion explicit and named, at the boundary:

```typescript
interface ToolLocation {
  line: number;    // 1-based, from the external tool
  column: number;  // 1-based, from the external tool
}

/** Converts a tool's 1-based location to a VS Code 0-based Position. */
function toPosition(loc: ToolLocation): vscode.Position {
  return new vscode.Position(Math.max(0, loc.line - 1), Math.max(0, loc.column - 1));
}
```

Two follow-ups worth checking per tool:

- Some tools report a 1-based line but a **0-based** column. There is no convention; read the tool's docs or test against a known file rather than assuming symmetry.
- A `Range` end is exclusive in VS Code. A tool reporting an inclusive end range needs `+1` on the end character *after* the `-1` for the base, which nets out to no change — and getting that wrong produces a highlight one character short, the hardest variant to spot.

When a tool reports only a line with no column, `doc.lineAt(line).range` gives you the whole line, which is better than guessing a column.

## FileSystemWatcher

```typescript
const watcher = vscode.workspace.createFileSystemWatcher(
  new vscode.RelativePattern(folder, '**/*.config.json'),
  false,   // ignoreCreateEvents
  false,   // ignoreChangeEvents
  false,   // ignoreDeleteEvents
);

context.subscriptions.push(
  watcher,
  watcher.onDidCreate(uri => this.onConfigAdded(uri)),
  watcher.onDidChange(uri => this.scheduleReload(uri)),
  watcher.onDidDelete(uri => this.onConfigRemoved(uri)),
);
```

**The watcher and each listener are separate disposables.** Push all of them. A disposed watcher with live listeners still leaks the closures.

### What it does and does not see

- By default a watcher only covers paths **inside workspace folders**. Watching outside requires a `RelativePattern` with a Uri base, and support for that varies by filesystem provider — verify against the current docs before depending on it.
- It respects the user's `files.watcherExclude` setting. Files the user excluded (commonly `node_modules`, `.git`, build output) produce no events, no matter what your glob says.
- The three ignore flags exist for cost. A watcher that only cares about deletions should set `ignoreCreateEvents` and `ignoreChangeEvents` to `true` rather than filtering in the handler — the flags prevent the events from being delivered at all.

### Debounce

One logical change frequently produces multiple events. A save can fire `change` twice; an editor writing atomically (write temp, rename over) fires `create` then `delete` then `change`; a `git checkout` fires hundreds of events in a burst.

Collapse them before doing real work:

```typescript
const pending = new Set<string>();
let timer: NodeJS.Timeout | undefined;

function scheduleReload(uri: vscode.Uri) {
  pending.add(uri.toString());
  if (timer) { clearTimeout(timer); }
  timer = setTimeout(() => {
    timer = undefined;
    const batch = [...pending].map(s => vscode.Uri.parse(s));
    pending.clear();
    void reloadAll(batch);
  }, 300);
}
```

Also: watcher events tell you a path changed, not what it now contains. Re-read through `workspace.fs` or `openTextDocument`, and expect the file to sometimes be gone by the time you look — a delete may have followed the change.

## Document events

```typescript
context.subscriptions.push(
  // Fires on EVERY keystroke, per document. Never do real work synchronously here.
  vscode.workspace.onDidChangeTextDocument(e => {
    // e.document, e.contentChanges (ranges + text), e.reason (Undo | Redo | undefined)
    if (e.contentChanges.length === 0) { return; }   // metadata-only change, e.g. dirty flag
    if (e.document.uri.scheme !== 'file') { return; }
    debouncedAnalyze(e.document);
  }),

  vscode.workspace.onDidSaveTextDocument(doc => { void runLinter(doc); }),
  vscode.workspace.onDidOpenTextDocument(doc => { void analyze(doc); }),
  vscode.workspace.onDidCloseTextDocument(doc => { diagnostics.delete(doc.uri); }),
);
```

`onDidChangeTextDocument` is the hot path of the entire extension API. Debounce it (200-500ms), filter by scheme and language first, and never parse a whole file in the handler body. `e.contentChanges` gives you the exact ranges that changed, which is enough for incremental work in many cases.

`onDidCloseTextDocument` is where diagnostics get cleaned up. Skipping it leaves stale errors in the Problems panel for files the user closed — the classic "ghost errors" complaint.

Note that these events cover *documents*, not files. A document can be open with no visible editor, and a file can change on disk with no document event at all (that is the watcher's job).

### Save participants

`onWillSaveTextDocument` lets you contribute edits before a save completes:

```typescript
context.subscriptions.push(
  vscode.workspace.onWillSaveTextDocument(e => {
    if (e.document.languageId !== 'myLang') { return; }
    if (e.reason !== vscode.TextDocumentSaveReason.Manual) { return; }

    // waitUntil accepts Thenable<TextEdit[]> or Thenable<void>.
    // It must be called synchronously, inside the handler body.
    e.waitUntil(computeEdits(e.document));
  }),
);
```

Constraints, all of them enforced:

- `waitUntil` must be called **synchronously** during the event. Calling it after an `await` throws, because the save has already moved on.
- There is a **timeout** — the save proceeds without your edits if you take too long. Treat this as a budget of a few hundred milliseconds, not seconds. Slow work belongs in `onDidSaveTextDocument` instead, where it does not block the save.
- Multiple extensions participate. The order is not guaranteed, and another participant's edits may land before or after yours.
- Edits returned here apply to the document being saved only. Anything cross-file belongs in a `WorkspaceEdit` triggered elsewhere.

`onWillSaveTextDocument` is easy to overuse. If the user did not ask for a transformation on save, do not add one; format-on-save is a setting they opted into, and a surprise mutation of their file is worse than no feature.

## Storage locations

```typescript
context.extensionUri;      // the installed extension directory — READ ONLY
context.globalStorageUri;  // per-extension, cross-workspace, writable
context.storageUri;        // per-extension, per-workspace, writable — undefined with no folder
context.logUri;            // per-session log directory, writable
```

| Location | Scope | Lifetime | Use for |
| --- | --- | --- | --- |
| `extensionUri` | The installed extension | Replaced on every update | Bundled assets: icons, templates, schemas. Never write. |
| `globalStorageUri` | User, all workspaces | Until uninstall | Caches, downloaded tools, cross-project data. |
| `storageUri` | User, this workspace | Until uninstall | Per-project indexes, per-project caches. |
| `logUri` | This session | Cleared periodically | Log files worth keeping across a session. |

Rules that follow from the table:

- **Never write into `extensionUri`.** The directory is replaced wholesale on update, so anything written there is silently lost — and on some installations it is read-only, so the write fails outright. Use it only with `Uri.joinPath` to read bundled resources and to build webview resource roots.
- **`storageUri` is `undefined` when no workspace folder is open.** It is the same three-state problem as `workspaceFolders`, in a different shape. Fall back to `globalStorageUri` or skip the feature:

```typescript
const storage = context.storageUri ?? context.globalStorageUri;
await vscode.workspace.fs.createDirectory(storage);
const dataFile = vscode.Uri.joinPath(storage, 'index.json');
```

- **None of these directories are guaranteed to exist.** Call `createDirectory` before the first write; it is idempotent.
- These are for *files*. Small values — flags, last-used choices, cursor positions — belong in `context.globalState` / `context.workspaceState`, and credentials belong in `context.secrets` and nowhere else.
- On a remote workspace these Uris point at the remote host, matching where the extension host runs. That is normally correct, but it means a cache built locally will not be there after switching to a remote window.

---

**Signature check.** `workspace.fs.copy`, `LogOutputChannel`-era additions, and the `RelativePattern` Uri-base overload arrived after the original API, and watcher behavior outside workspace folders has changed across releases. Verify anything you have not used recently against the current `vscode.d.ts` in `@types/vscode`, and against the `engines.vscode` floor in `package.json` — an API newer than that floor compiles cleanly and throws at runtime on the user's older editor.
