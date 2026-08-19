# Tree Views, Status Bar, and UI Surfaces

Reference detail for the UI surfaces in the `vscode.window` namespace. The parent skill covers the rules; this file covers the shapes.

Every one of these creates something you own. `createTreeView`, `createStatusBarItem`, `createOutputChannel`, `createQuickPick`, `registerFileDecorationProvider` all return disposables — push them into `context.subscriptions` at the moment you create them, not at the end of `activate` after the interesting code.

## Contents

- [TreeDataProvider](#treedataprovider)
- [The refresh event](#the-refresh-event)
- [TreeItem in detail](#treeitem-in-detail)
- [contextValue and per-item menus](#contextvalue-and-per-item-menus)
- [createTreeView vs registerTreeDataProvider](#createtreeview-vs-registertreedataprovider)
- [Lazy loading and performance](#lazy-loading-and-performance)
- [Empty state: viewsWelcome](#empty-state-viewswelcome)
- [StatusBarItem](#statusbaritem)
- [QuickPick](#quickpick)
- [InputBox](#inputbox)
- [Notifications](#notifications)
- [OutputChannel and LogOutputChannel](#outputchannel-and-logoutputchannel)
- [FileDecorationProvider](#filedecorationprovider)

---

## TreeDataProvider

A tree view is a pull interface. You do not build a tree and hand it over; you answer questions about one node at a time, and VS Code decides which questions to ask.

The interface is generic over *your* node type. Use a real domain type rather than `TreeItem` itself — you will need the underlying data when a command fires on a node, and `TreeItem` does not carry it.

```typescript
import * as vscode from 'vscode';

interface Task {
  id: string;
  label: string;
  status: 'pending' | 'running' | 'failed' | 'done';
  parentId?: string;
}

export class TaskTreeProvider implements vscode.TreeDataProvider<Task> {
  private readonly _onDidChangeTreeData =
    new vscode.EventEmitter<Task | undefined | void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  private tasks: Task[] = [];

  constructor(private readonly context: vscode.ExtensionContext) {}

  // Called for every node VS Code is about to render. Keep it cheap and synchronous.
  getTreeItem(element: Task): vscode.TreeItem {
    const hasChildren = this.tasks.some(t => t.parentId === element.id);
    const item = new vscode.TreeItem(
      element.label,
      hasChildren
        ? vscode.TreeItemCollapsibleState.Collapsed
        : vscode.TreeItemCollapsibleState.None,
    );

    item.id = element.id;                 // stable id keeps expansion state across refreshes
    item.description = element.status;    // dimmed text after the label
    item.iconPath = iconForStatus(element.status);
    item.contextValue = `task.${element.status}`;  // what menu `when` clauses match
    item.command = {
      command: 'myExt.openTask',
      title: 'Open Task',
      arguments: [element],
    };
    return item;
  }

  // Called only for the root and for nodes the user expands.
  getChildren(element?: Task): Task[] {
    return element
      ? this.tasks.filter(t => t.parentId === element.id)
      : this.tasks.filter(t => t.parentId === undefined);
  }

  // Optional in the interface — REQUIRED if you ever call TreeView.reveal().
  getParent(element: Task): Task | undefined {
    return element.parentId
      ? this.tasks.find(t => t.id === element.parentId)
      : undefined;
  }

  setTasks(tasks: Task[]): void {
    this.tasks = tasks;
    this._onDidChangeTreeData.fire();   // without this, the view still shows the old data
  }

  dispose(): void {
    this._onDidChangeTreeData.dispose();
  }
}
```

`getChildren` may return a promise. Async is fine and expected — a node whose children come from a network call or a child process should return `Promise<Task[]>`, and VS Code shows a spinner on that node while it resolves. What is not fine is doing that work in `getTreeItem`, which is called for every visible row on every repaint.

Register it, and note which registration you want (the next-but-one section explains the choice):

```typescript
const provider = new TaskTreeProvider(context);
context.subscriptions.push(
  provider,
  vscode.window.registerTreeDataProvider('myExt.tasks', provider),
);
```

The view id (`myExt.tasks`) must match a `contributes.views` entry in `package.json`. Without it the registration silently does nothing — there is no view to attach to.

## The refresh event

This is the single most common tree view bug, so it is worth stating plainly: **mutating your backing array does nothing.** VS Code does not watch your data. It re-queries the provider only when `onDidChangeTreeData` fires.

The `EventEmitter` you expose is the mechanism. What you fire determines the scope of the refresh:

```typescript
// Whole tree — VS Code re-queries getChildren(undefined) and walks down again.
this._onDidChangeTreeData.fire();
this._onDidChangeTreeData.fire(undefined);  // identical

// One subtree — VS Code re-queries getChildren(element) and rebuilds under that node only.
this._onDidChangeTreeData.fire(someTask);
```

Fire the narrowest scope that is correct. A full-tree fire collapses nothing if your `TreeItem.id` values are stable, but it does re-run `getChildren` for every expanded node — on a tree whose children come from a process, that is a burst of work for a change to one leaf.

The type parameter of the emitter must include `undefined` (or `void`) or the whole-tree form will not typecheck:

```typescript
new vscode.EventEmitter<Task | undefined | void>();
```

Two related traps:

- **Set `TreeItem.id`** if your data can be re-created rather than mutated in place. Without it VS Code identifies nodes by label path, and a refresh after a rename collapses the tree and loses selection.
- **Do not fire from inside `getChildren`.** It re-enters, and you get either an infinite refresh loop or a view that flickers permanently.

## TreeItem in detail

```typescript
const item = new vscode.TreeItem(label, collapsibleState);
```

The first argument can also be a `TreeItemLabel` (`{ label, highlights }`) when you want to highlight substrings — useful for search results.

| Property | What it does |
| --- | --- |
| `label` | Primary text. `string` or `TreeItemLabel` with highlight ranges. |
| `description` | Dimmed text after the label. `true` derives it from `resourceUri`. |
| `tooltip` | `string` or `MarkdownString` for rich hover content. |
| `iconPath` | `ThemeIcon`, a `Uri`, or `{ light, dark }` file paths. |
| `collapsibleState` | `None`, `Collapsed`, or `Expanded`. |
| `command` | Runs on single click of the row. |
| `resourceUri` | Ties the row to a file — icon, decorations, and Git colors follow. |
| `contextValue` | The string per-item menu `when` clauses match against. |
| `id` | Stable identity across refreshes. |
| `accessibilityInformation` | Screen reader label and role. |

### collapsibleState

`None` means leaf — no twistie, and `getChildren` is never called for it. `Collapsed` and `Expanded` both mean "this node has children"; the difference is only the initial render.

Compute this from whether children actually exist. A node set to `Collapsed` whose `getChildren` returns an empty array renders a twistie that expands to nothing, which reads as a bug to the user. When you genuinely cannot know without doing the work, `Collapsed` plus an async `getChildren` that returns `[]` is the honest tradeoff — but prefer knowing.

### iconPath

Three forms, in descending order of preference:

```typescript
// 1. ThemeIcon — a built-in codicon by name, without the $() wrapper.
item.iconPath = new vscode.ThemeIcon('check');
item.iconPath = new vscode.ThemeIcon('error', new vscode.ThemeColor('charts.red'));

// 2. Theme-aware file pair — your own SVGs, one per theme.
item.iconPath = {
  light: vscode.Uri.joinPath(context.extensionUri, 'media', 'light', 'task.svg'),
  dark: vscode.Uri.joinPath(context.extensionUri, 'media', 'dark', 'task.svg'),
};

// 3. Single Uri — same icon in both themes. Usually wrong; it will be
//    illegible in one of them unless the artwork is deliberately neutral.
item.iconPath = vscode.Uri.joinPath(context.extensionUri, 'media', 'logo.png');
```

`ThemeIcon` is preferred because it inherits the user's icon theme and color tokens automatically, and costs no bundle size. The second argument is a `ThemeColor`, which takes a *theme color id* — not a hex value. There is no API to set a literal color; that is deliberate, so extensions cannot break high-contrast and colorblind-friendly themes.

Codicon names come from the codicon reference in the VS Code docs. In `iconPath` you pass the bare name (`'check'`); in text properties that support inline icons you use the `$(check)` form. Mixing the two up is a frequent mistake — `new ThemeIcon('$(check)')` renders nothing.

### tooltip with MarkdownString

```typescript
const md = new vscode.MarkdownString();
md.appendMarkdown(`**${task.label}**\n\n`);
md.appendMarkdown(`Status: \`${task.status}\`\n\n`);
md.appendCodeblock(task.lastError ?? '(no errors)', 'text');
item.tooltip = md;
```

If the tooltip needs a clickable command link, set `md.isTrusted = true` and use `command:` URIs — but only when every part of the string is content you produced. `isTrusted` on a string built from workspace content is a command-injection vector. Prefer `appendText` (which escapes) over `appendMarkdown` for any interpolated value.

### resourceUri

Setting `resourceUri` is how you get file-shaped rows for free:

```typescript
item.resourceUri = vscode.Uri.file(task.filePath);
item.iconPath = undefined;          // let the file icon theme decide
item.description = true;            // show the containing folder as the description
```

VS Code then applies the user's file icon theme, Git decorations (modified, untracked), problem decorations, and anything registered via `FileDecorationProvider`. A tree of files that does not set `resourceUri` looks foreign inside the explorer, and loses all of that for nothing.

## contextValue and per-item menus

`contextValue` is a plain string you attach to an item; menu contributions match it in a `when` clause via the `viewItem` context key. This is the entire mechanism for per-row context menus and inline action buttons.

```typescript
item.contextValue = task.status === 'running' ? 'task.running' : 'task.idle';
```

```jsonc
// package.json
"contributes": {
  "menus": {
    "view/item/context": [
      {
        "command": "myExt.cancelTask",
        "when": "view == myExt.tasks && viewItem == task.running",
        "group": "inline"
      },
      {
        "command": "myExt.rerunTask",
        "when": "view == myExt.tasks && viewItem =~ /^task\\./",
        "group": "1_actions"
      }
    ]
  }
}
```

Points that matter:

- Always scope with `view == <yourViewId>`, or your menu items appear on other extensions' trees that happen to use the same `contextValue`.
- `==` is exact match. For families of values use the regex operator `=~`, as above.
- `group: "inline"` puts the action on the row as a hover icon instead of in the right-click menu. Reserve it for the one or two most common actions.
- The command receives the *node* as its first argument (the `Task`, not the `TreeItem`), because that is what `getChildren` returned. Multi-select views pass the full selection as a second argument.
- Changing `contextValue` requires firing the change event — it is part of the `TreeItem`, so the row must be re-queried before the menu changes.

## createTreeView vs registerTreeDataProvider

`registerTreeDataProvider` wires up the provider and returns only a `Disposable`. `createTreeView` does the same and hands back a `TreeView<T>` object — the view itself.

Use `createTreeView` when you need any of:

```typescript
const view = vscode.window.createTreeView('myExt.tasks', {
  treeDataProvider: provider,
  showCollapseAll: true,
  canSelectMany: false,
  // dragAndDropController: ...  // opt in only if you implement drag/drop
});
context.subscriptions.push(view);

// Programmatic reveal — REQUIRES TreeDataProvider.getParent() to be implemented.
await view.reveal(someTask, { select: true, focus: true, expand: 2 });

// Header text and a numeric badge on the view container icon.
view.title = 'Tasks';
view.message = 'No workspace folder open.';   // replaces the tree body with this text
view.badge = { value: failedCount, tooltip: `${failedCount} failed` };

// Observation.
view.onDidChangeSelection(e => { /* e.selection: readonly Task[] */ });
view.onDidChangeVisibility(e => {
  if (e.visible) { provider.startPolling(); } else { provider.stopPolling(); }
});
view.onDidExpandElement(e => { /* e.element */ });
view.onDidCollapseElement(e => { /* e.element */ });

// State you can read.
view.visible;    // boolean
view.selection;  // readonly Task[]
```

`reveal` without `getParent` throws at runtime. It is the one place the "optional" member of `TreeDataProvider` is not optional, and it is easy to miss because the interface compiles fine without it.

`onDidChangeVisibility` is the hook that stops a tree view from being a background CPU cost. A view in a collapsed sidebar section is invisible and still holds your poller alive unless you stop it.

`view.message` is the right tool for a *transient* explanatory state ("Scanning...", "Connect an account to see tasks"). For a persistent empty state that needs buttons, use `viewsWelcome` instead — see below.

## Lazy loading and performance

The tree is pull-based, which is a gift: you only pay for what the user actually looks at. Squandering it is easy.

- `getChildren` is called for the root, then for each node as it is expanded — never for collapsed subtrees. Do not pre-walk the whole hierarchy in your constructor or in `setTasks`.
- `getTreeItem` is called for every visible row, and again after every refresh. It must be cheap: no I/O, no `fs.statSync`, no string parsing of a large file. If a row's icon depends on a stat call, do the stat when you load that level in `getChildren` and cache it on your node type.
- Async `getChildren` is the correct place for slow work. VS Code renders a spinner on the node while the promise is pending.
- Do not return thousands of children from one call. Beyond a few hundred rows the view stops being usable anyway; return the first page plus a synthetic "Load more..." node whose `command` fetches the next page and fires a targeted refresh.
- Cancellation is not part of the `TreeDataProvider` interface — there is no token. If a pending `getChildren` becomes irrelevant (the user collapsed the node, the workspace changed), you have to guard it yourself with a generation counter and drop the stale result.

## Empty state: viewsWelcome

A tree that legitimately has nothing to show renders as a blank rectangle, which is indistinguishable from broken. `contributes.viewsWelcome` fills it with text and command links instead.

```jsonc
"contributes": {
  "viewsWelcome": [
    {
      "view": "myExt.tasks",
      "contents": "No tasks found in this workspace.\n[Create a task](command:myExt.createTask)\nOr read the [setup guide](https://example.com/docs).",
      "when": "myExt:hasWorkspace && !myExt:hasTasks"
    },
    {
      "view": "myExt.tasks",
      "contents": "Open a folder to see tasks.\n[Open Folder](command:vscode.openFolder)",
      "when": "workbenchState == empty"
    }
  ]
}
```

Mechanics worth knowing:

- Markdown links written as `[Label](command:someCommand)` render as full-width buttons. Ordinary URL links render as inline links. That difference is how you signal primary action versus documentation.
- Welcome content appears only when the provider returns zero root children. You cannot force it while the tree has rows.
- The `when` clause is what makes this useful. Drive your own keys from the extension:

```typescript
await vscode.commands.executeCommand('setContext', 'myExt:hasTasks', tasks.length > 0);
```

Set these keys at every point the answer changes — after load, after refresh, after an error. A `setContext` call that only runs on activation leaves the welcome view stuck in its initial state forever.

Distinguishing states is the point. "No tasks yet" and "could not connect to the task server" are different problems for the user; two `viewsWelcome` entries with different `when` clauses cost nothing and save a support round-trip.

## StatusBarItem

```typescript
const status = vscode.window.createStatusBarItem(
  'myExt.buildStatus',                    // stable id — lets users hide it via UI
  vscode.StatusBarAlignment.Left,
  100,                                    // higher priority sits further left
);
context.subscriptions.push(status);

status.name = 'Build Status';             // shown in the status bar's own context menu
status.text = '$(sync~spin) Building';    // $(codicon) renders inline; ~spin animates
status.tooltip = new vscode.MarkdownString('Click to open the build log');
status.command = 'myExt.showBuildLog';
status.show();
```

Then transition it as state changes:

```typescript
function setResult(ok: boolean, detail: string) {
  status.text = ok ? '$(check) Build' : '$(error) Build';
  status.tooltip = detail;
  status.backgroundColor = ok
    ? undefined
    : new vscode.ThemeColor('statusBarItem.errorBackground');
}
```

Notes:

- `backgroundColor` accepts only two theme colors in practice: `statusBarItem.warningBackground` and `statusBarItem.errorBackground`. Others are ignored. This is intentional — the status bar is not a canvas.
- Left alignment is for things about the current workspace or task; right is for things about the current editor (line ending, language mode). Priority orders items within a side.
- `hide()` when the item is not relevant. A status bar item that is always present, always saying the same thing, is noise the user cannot remove — which is why `name` matters: it gives them a way to hide it themselves.
- Keep the text short. This is a shared strip; a long string pushes other extensions' items off-screen.
- Dispose it. A leaked status bar item survives extension deactivation and stays on screen until reload.

## QuickPick

Two levels of API. Reach for the simple one first.

### window.showQuickPick

```typescript
interface TaskPick extends vscode.QuickPickItem {
  task: Task;
}

const picks: TaskPick[] = tasks.map(t => ({
  label: t.label,
  description: t.status,
  detail: t.id,          // second line, dimmed
  task: t,
}));

const chosen = await vscode.window.showQuickPick(picks, {
  title: 'Run Task',
  placeHolder: 'Select a task to run',
  matchOnDescription: true,
  matchOnDetail: false,
  ignoreFocusOut: false,
});

if (!chosen) { return; }   // dismissed — the common case, not an error
await runTask(chosen.task);
```

**`showQuickPick` resolves to `undefined` when the user presses Escape or clicks away.** Every call site needs that early return. Treating dismissal as an error — logging it, showing a message — is a bad habit that produces noisy extensions.

Extending `QuickPickItem` with your own field (`task` above) is the clean way to get from selection back to data. The alternative, matching on `label`, breaks the moment two items share a label.

### window.createQuickPick

Use the object form when you need behavior the one-shot function cannot express: a busy indicator, results that change as the user types, buttons, or staying open after a selection.

```typescript
const qp = vscode.window.createQuickPick<TaskPick>();
qp.title = 'Search Tasks';
qp.placeholder = 'Type to search the server';
qp.matchOnDescription = true;
qp.busy = true;
qp.buttons = [
  { iconPath: new vscode.ThemeIcon('refresh'), tooltip: 'Reload' },
];

const disposables: vscode.Disposable[] = [];
let generation = 0;

disposables.push(
  // Dynamic filtering: fetch results per keystroke rather than filtering a static list.
  qp.onDidChangeValue(async value => {
    const mine = ++generation;
    qp.busy = true;
    const results = await searchTasks(value);
    if (mine !== generation) { return; }   // a newer query already superseded this one
    qp.items = results.map(t => ({ label: t.label, description: t.status, task: t }));
    qp.busy = false;
  }),
  qp.onDidAccept(() => {
    const [picked] = qp.selectedItems;
    if (picked) { void runTask(picked.task); }
    qp.hide();
  }),
  qp.onDidTriggerButton(() => void reload()),
  qp.onDidHide(() => {
    disposables.forEach(d => d.dispose());
    qp.dispose();
  }),
);

qp.show();
```

`onDidHide` firing `dispose` is the standard lifecycle: the picker is modal-ish and single-use, so it cleans itself up rather than living in `context.subscriptions`.

The generation counter matters. `onDidChangeValue` fires per keystroke, requests finish out of order, and without the guard a slow response for `"bui"` can overwrite the correct results for `"build"`.

When you drive `items` yourself from `onDidChangeValue`, VS Code still applies its own fuzzy filter on top unless you clear it. If the server already filtered, that double filtering hides valid results — the usual fix is to keep the labels containing the typed text, or to accept the built-in filter and only use `onDidChangeValue` to widen the candidate set.

### Separators

```typescript
qp.items = [
  { label: 'Recent', kind: vscode.QuickPickItemKind.Separator } as TaskPick,
  ...recent,
  { label: 'All Tasks', kind: vscode.QuickPickItemKind.Separator } as TaskPick,
  ...all,
];
```

A separator item is not selectable and ignores everything but `label`. It is the right way to group; a fake item with dashes in the label is selectable and will eventually be selected.

## InputBox

```typescript
const name = await vscode.window.showInputBox({
  title: 'New Task',
  prompt: 'Task name',
  value: suggestedName,
  valueSelection: [0, suggestedName.length],  // pre-select for easy overwrite
  placeHolder: 'e.g. build-frontend',
  ignoreFocusOut: true,
  password: false,
  validateInput: text => {
    if (!text.trim()) { return 'Name is required.'; }
    if (!/^[a-z0-9-]+$/.test(text)) { return 'Use lowercase letters, digits, and dashes.'; }
    if (existingNames.has(text)) { return `"${text}" already exists.`; }
    return undefined;   // undefined (or null) means valid
  },
});

if (name === undefined) { return; }   // dismissed
```

- `validateInput` runs on every keystroke and may return a promise. Keep it fast; if it must hit the network, debounce inside it or validate optimistically and re-check on accept. While it returns a non-undefined message, the input cannot be accepted.
- Returning a `InputBoxValidationMessage` (`{ message, severity }`) instead of a bare string lets you show a non-blocking warning rather than a hard error. Verify the exact shape against the current `vscode.d.ts` before relying on it.
- `ignoreFocusOut: true` keeps the box open when focus moves elsewhere. Use it for multi-step flows where the user may need to look at the editor; leave it off for quick single prompts, where auto-dismiss is what the user expects.
- `password: true` masks the input, but does not make it secret. Whatever you collect this way still needs `context.secrets` for storage — never `globalState`.
- An empty string is a *valid* return value distinct from dismissal. Check `=== undefined`, not falsiness, or the user typing nothing and pressing Enter is silently treated as a cancel.

For genuinely multi-step input, `createInputBox` gives you the same object-level control as `createQuickPick` (`step`, `totalSteps`, back buttons, `onDidChangeValue`).

## Notifications

```typescript
const OPEN = 'Open Log';
const DISMISS = 'Not Now';

const choice = await vscode.window.showWarningMessage(
  'Build finished with 3 warnings.',
  OPEN,
  DISMISS,
);

if (choice === OPEN) {
  await vscode.commands.executeCommand('myExt.showBuildLog');
}
```

The return value is the exact string of the chosen button, or `undefined` if the notification was dismissed or timed out. Compare against constants rather than inline literals so a typo becomes a compile error rather than a dead branch.

The options-object overload adds `modal` and per-item control:

```typescript
const confirm = await vscode.window.showWarningMessage(
  'Delete 12 tasks? This cannot be undone.',
  { modal: true, detail: 'Tasks will be removed from the server.' },
  'Delete',
);
if (confirm !== 'Delete') { return; }
```

`modal: true` blocks the editor until answered, and VS Code adds its own Cancel button. Reserve it for destructive, irreversible actions. A modal for anything else is the fastest way to make users uninstall an extension.

**On not overusing notifications.** A notification interrupts, steals focus from the reading position, and stacks up. The decision rule:

| Situation | Surface |
| --- | --- |
| User must decide something now | Notification with buttons, or modal if destructive |
| An action the user just triggered failed | `showErrorMessage` with an "Open Log" button |
| Ongoing work the user started | `window.withProgress` |
| Ambient state (build status, connection) | Status bar item |
| Diagnostic detail, tool output, traces | Output channel |
| Routine success ("saved", "formatted") | Nothing at all |

"Operation completed successfully" as a notification is almost always wrong: the user watched it happen, and the interruption costs more than the confirmation is worth.

## OutputChannel and LogOutputChannel

```typescript
const output = vscode.window.createOutputChannel('My Extension');
context.subscriptions.push(output);

output.appendLine(`Starting build for ${folder.name}`);
output.append('.');            // no newline — progress dots
output.show(true);             // true = preserveFocus, do NOT steal the cursor
```

`show()` with no argument moves focus into the panel, yanking the user out of the editor mid-keystroke. Pass `true` unless the user explicitly asked to see the log.

### LogOutputChannel

For diagnostics, create the channel with `{ log: true }` and get a leveled logger instead:

```typescript
const log = vscode.window.createOutputChannel('My Extension', { log: true });
context.subscriptions.push(log);

log.trace('resolved config', config);       // hidden unless user sets Trace level
log.debug('spawning', binPath, args);
log.info('build started');
log.warn('deprecated setting "myExt.oldKey" in use');
log.error(err instanceof Error ? err : String(err));

log.onDidChangeLogLevel(level => { /* adjust verbosity of your own work */ });
```

What this buys over a plain channel:

- Each line gets a timestamp and level prefix automatically, in VS Code's own log format.
- The user controls verbosity per channel through the output panel's gear menu, and through the **Developer: Set Log Level** command. Levels below the setting are not written at all, so `log.trace` in a hot path costs nearly nothing when disabled.
- `log.logLevel` and `onDidChangeLogLevel` let you skip building expensive messages when nobody will see them.
- The channel participates in the log-collection commands users are asked to run when filing bugs.

**This is where diagnostic logging belongs, not `console.log`.** `console.log` goes to the extension host's developer tools — a place ordinary users never open and cannot easily export. Anything you would want to see in a bug report has to be in an output channel.

One channel per extension is the norm. Multiple channels are justified when they have genuinely different audiences (a user-facing "Build Output" that shows tool stdout, plus a "My Extension" log channel for diagnostics), not as a substitute for log levels.

## FileDecorationProvider

File decorations add a badge (one or two characters), a color, and a tooltip to any row that carries a `resourceUri` — in the explorer, in open editor tabs, and in your own tree views. This is the mechanism behind Git's `M`/`U` markers.

```typescript
class TaskDecorationProvider implements vscode.FileDecorationProvider {
  private readonly _onDidChange = new vscode.EventEmitter<vscode.Uri | vscode.Uri[]>();
  readonly onDidChangeFileDecorations = this._onDidChange.event;

  provideFileDecoration(uri: vscode.Uri): vscode.FileDecoration | undefined {
    const status = statusFor(uri);
    if (!status) { return undefined; }   // no decoration is the normal answer
    return {
      badge: status === 'failed' ? '!' : undefined,
      color: new vscode.ThemeColor(
        status === 'failed' ? 'errorForeground' : 'gitDecoration.modifiedResourceForeground',
      ),
      tooltip: `Task ${status}`,
      propagate: true,   // bubble the color up to parent folders
    };
  }

  refresh(uris: vscode.Uri[]): void { this._onDidChange.fire(uris); }
  dispose(): void { this._onDidChange.dispose(); }
}

const deco = new TaskDecorationProvider();
context.subscriptions.push(deco, vscode.window.registerFileDecorationProvider(deco));
```

Constraints that catch people out:

- `badge` is at most two characters. Longer strings are truncated, not wrapped.
- `color` must be a `ThemeColor` id, like everywhere else in this API.
- The provider is called for every visible resource, frequently. Answer from a map you maintain; do not stat the filesystem inside it.
- Decorations only attach where a `resourceUri` exists. A tree item without one cannot be decorated — which is another reason to set it.
- Multiple extensions decorate the same resource; VS Code merges and may drop yours. Do not rely on a decoration being the only signal for something important.

---

**Signature check.** `TreeView.badge`, `LogOutputChannel`, `InputBoxValidationMessage`, `TreeItemLabel` highlights, and the drag-and-drop controller were all added after the original tree view API, and some shifted shape before stabilizing. Verify anything you have not used recently against the current `vscode.d.ts` in `@types/vscode`, and against the `engines.vscode` floor in `package.json` — an API newer than that floor compiles cleanly and throws at runtime on the user's older editor.
