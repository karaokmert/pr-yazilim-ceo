---
name: vscode-ext-api-patterns
description: Implementation canon for VS Code Extension API feature work — commands, language feature providers (hover, completion, code actions, CodeLens, definition, formatting, diagnostics), tree views, webviews and their CSP/message bridge, workspace and file system access, configuration and state, secrets, cancellation and progress, and external process integration. Load this whenever writing or debugging extension feature code in TypeScript against the vscode API — adding a command, building a provider or sidebar view, creating a webview panel, reading settings or persisting state, handling documents and editors, or tracking down why a provider returns stale data or a webview renders blank.
---

# Extension API Implementation Patterns

This is the developer's working canon. It covers how to build features correctly against the `vscode` namespace, with emphasis on the API's sharp edges — the places where reasonable-looking code is wrong in ways that only show up on someone else's machine.

Manifest entries that pair with this code are in `vscode-ext-manifest`. **Every feature here has a manifest half; they ship together or the feature doesn't work.**

The ownership rules that apply across the whole team — disposal, secrets, and absence-handling — are canon in `vscode-ext-behavior`. Read that first; this skill assumes it and applies it to specific API surfaces below rather than restating it.

**Check signatures before relying on memory.** Provider interfaces and webview APIs have shifted across releases. Look up anything you haven't used recently.

## The property underneath everything

**You are a guest in a shared process.** The extension host runs your code alongside every other extension the user installed. Block its event loop and you freeze *their* editor. Leak a listener and *they* pay. This is why the disposal discipline in `vscode-ext-behavior` and the async patterns below aren't style preferences — they're what keeps a shared process usable.

Two applications of the `vscode-ext-behavior` ownership rules worth naming explicitly for this API surface:

- **What counts as a `Disposable` here**: command registrations, providers, listeners, watchers, status bar items, and diagnostic collections all return one. Each is owned the moment it's created — see `vscode-ext-behavior` for the rule itself.
- **What "absence" looks like in this API**: no active editor, no workspace folder, multi-root workspace, untitled document, empty selection. `workspace.workspaceFolders` can be `undefined` or have many entries — `workspaceFolders[0]` is a crash waiting for the user who opened a single file.

## Commands

Register with `vscode.commands.registerCommand`, push the disposable, and add the `contributes.commands` entry in the same change.

Handlers should assume nothing about *why* they were invoked. A command can fire from the palette, a keybinding, a menu, or another extension calling `executeCommand` — so the active editor you expect may not exist. Check and degrade with a clear message rather than throwing.

`registerTextEditorCommand` is the better choice when a command only makes sense with an active editor: VS Code supplies the editor and edit builder, and handles the no-editor case for you.

## Language feature providers

Providers implement an interface, get registered against a `DocumentSelector`, and are called *by VS Code*, on its schedule — not yours. Two consequences drive everything:

**They are called far more often than you'd expect.** Hover fires on mouse movement; completion on nearly every keystroke. A provider that does expensive work per call makes typing feel broken. Cache, debounce, and keep the hot path cheap.

**Cancellation is real and must be honored.** Every provider receives a `CancellationToken`. When the user moves on, VS Code cancels — and if you ignore the token, your abandoned work still competes for the event loop.

Honoring cancellation means *stopping the underlying work*, not discarding the result at the end:

```ts
async provideCompletionItems(doc, pos, token) {
  const results = await this.expensiveLookup(doc, pos, token); // token passed down
  if (token.isCancellationRequested) { return undefined; }
  return results;
}
```

Check the token after each await, and thread it into child processes and network calls so they actually abort. Returning `undefined` is how a provider says "nothing to offer" — normal, not an error.

Diagnostics work differently from the rest: you own a `DiagnosticCollection` and push into it on your own schedule (typically on document change, debounced) rather than being asked. Remember to clear entries for closed or deleted documents, or stale errors haunt the Problems panel.

Per-provider contracts, return-type details, and the choice between overlapping providers are in `references/providers.md`.

## Tree views

`TreeDataProvider` backs custom sidebar and panel views. The two things that trip people up:

- **Refresh is an event you fire**, via `onDidChangeTreeData`. Mutating your backing data does nothing visible until you fire it — with `undefined` to refresh the whole tree, or a specific element to refresh that subtree.
- **`getChildren()` is called lazily**, only for expanded nodes. Don't eagerly build the entire tree; return children on demand, and make sure `getTreeItem` is cheap.

Use `window.createTreeView` rather than `registerTreeDataProvider` when you need the view object itself — selection, reveal, badges, message. See `references/views.md`.

## Webviews

Webviews are the highest-risk surface in the API, because they are a real browser context that you are responsible for securing.

**Content-Security-Policy with a nonce is mandatory, not optional.** Without a CSP, a webview rendering any untrusted content — file contents, API responses, anything from the workspace — is an injection vector into a context that can message your extension host code.

The pattern:

1. Set a strict CSP meta tag, scripts allowed only via a per-render `nonce`.
2. Set `localResourceRoots` to the narrowest set of directories needed.
3. Convert every local file path with `webview.asWebviewUri()` — raw `file://` paths do not load.
4. Never inject unescaped user or workspace content into the HTML string.

**The blank-webview debugging rule:** a webview that renders nothing is almost always CSP blocking its own script (missing or mismatched nonce) or a resource path that wasn't converted through `asWebviewUri`. Open the webview developer tools before looking anywhere else.

Extension and webview communicate only by message passing — `postMessage` / `onDidReceiveMessage`. Treat inbound messages as untrusted input and validate them; the webview is a different trust context from your extension code.

Webviews are destroyed when hidden unless `retainContextWhenHidden` is set — which costs memory, so prefer serializing state and restoring it. Full HTML template, nonce generation, and state persistence are in `references/webviews.md`.

## Workspace and file system

**Prefer `vscode.workspace.fs` over Node `fs`.** The workspace may not be on local disk — remote SSH, containers, GitHub virtual filesystems. `workspace.fs` works across all of them; Node `fs` silently only works on local files, and only on desktop.

Use `vscode.Uri` rather than string paths, and `Uri.joinPath` rather than string concatenation or Node `path`.

Node `fs` is defensible when the target is genuinely local and outside the workspace — a cache in `context.globalStorageUri`, a tool's own config in the home directory — and when the extension is confirmed desktop-only. Say so when you make that call.

Edits go through `WorkspaceEdit` (multi-file, undoable as one operation, works on unopened documents) or `editor.edit()` (single active editor). Prefer `WorkspaceEdit` for anything touching more than the active file.

`createFileSystemWatcher` reacts to external changes — remember to dispose it, and expect it to fire more often than you'd like.

## Configuration and state

**Configuration** — read via `workspace.getConfiguration('yourExt')`, with a matching `contributes.configuration` schema. Read the value at the point of use rather than caching it at activation, or listen to `onDidChangeConfiguration` and re-read; otherwise users change a setting and nothing happens until they reload.

**State** — `context.workspaceState` for per-workspace data, `context.globalState` for cross-workspace. Both are for small values (preferences, cursor positions, dismissed hints), not data stores. `globalState.setKeysForSync` opts keys into Settings Sync.

**Secrets** — `context.secrets` is the only acceptable place for tokens, keys, and credentials; it's async, backed by the OS keychain. The rule and its reasoning (`globalState` is plaintext on disk, settings sync and get pasted into bug reports, this holds for internal extensions too) is canon in `vscode-ext-behavior` — this is just where the API for it lives.

**Storage paths** — `context.globalStorageUri` and `context.storageUri` for files you own. Never write into the extension's install directory; it's replaced on update.

## Progress, async, and long work

Anything taking more than a moment belongs in `window.withProgress`, so the user knows the editor isn't stuck. `ProgressLocation.Notification` for user-initiated work (add `cancellable: true` and honor the token), `ProgressLocation.Window` for background status.

Never do synchronous heavy work — you're blocking the shared host. Offload to a child process or worker.

`window.showInformationMessage` and friends return promises that resolve to the chosen button, or `undefined` if dismissed. Dismissal is the common case; handle it.

## External processes

When shelling out to a binary (formatter, linter, internal CLI):

- This is **desktop-only**. It cannot work in the web extension host — flag the conflict rather than working around it.
- Prefer `spawn` over `exec` for anything with substantial output; `exec` buffers and can blow its limit on large results.
- **Always set a timeout and always wire cancellation to actually kill the process.** A hung child process that nothing kills is a leak the user cannot see and cannot clear without restarting.
- Never build a shell command by concatenating user or workspace input — pass arguments as an array. Workspace-derived paths are untrusted input.
- Capture stderr and surface it. A tool that fails silently is worse than one that errors loudly.

## Debugging checklist

When something doesn't work, these five explain most cases:

1. **Nothing happens at all** → the extension never activated. Check activation events and the Extension Host output channel.
2. **Command missing from palette** → no `contributes.commands` entry, or a `when` clause hiding it.
3. **Webview blank** → CSP blocking its own script, or resources not passed through `asWebviewUri`.
4. **Provider returns stale data** → caching without invalidation, or ignoring `onDidChangeTextDocument`.
5. **Setting change has no effect** → value cached at activation, no `onDidChangeConfiguration` listener.

## References

- `references/providers.md` — per-provider contracts, cancellation, diagnostics.
- `references/webviews.md` — CSP template, nonce, message bridge, state restore.
- `references/views.md` — tree views, decorations, status bar, quick pick.
- `references/workspace-fs.md` — Uri handling, edits, watchers, multi-root.
