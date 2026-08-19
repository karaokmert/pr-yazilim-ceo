# Webviews

A webview is a real browser context running inside the editor, which you are responsible for securing. Everything below follows from that: it is a separate trust boundary, with its own lifecycle, its own resource loading rules, and a message channel that is the only thing connecting it to your extension code.

## Contents

- [WebviewPanel vs WebviewView](#webviewpanel-vs-webviewview)
- [The secure HTML template](#the-secure-html-template)
- [Debugging a blank webview](#debugging-a-blank-webview)
- [Message passing](#message-passing)
- [State persistence](#state-persistence)
- [Lifecycle and disposal](#lifecycle-and-disposal)
- [Theming](#theming)

---

## WebviewPanel vs WebviewView

Two containers, one webview API inside them.

**`WebviewPanel`** occupies an editor tab. Created imperatively — usually from a command — and lives until closed. Use it for content that competes with a document for attention: a preview, a report, a form the user works through, a graph.

```typescript
const panel = vscode.window.createWebviewPanel(
  'myExt.report',                 // viewType — must match the serializer registration
  'Analysis Report',              // tab title
  vscode.ViewColumn.Beside,       // where to open
  {
    enableScripts: true,          // off by default; without it nothing runs
    localResourceRoots: [
      vscode.Uri.joinPath(context.extensionUri, 'media'),
    ],
  }
);
panel.webview.html = getHtml(panel.webview, context.extensionUri);
panel.iconPath = vscode.Uri.joinPath(context.extensionUri, 'media', 'icon.svg');
```

**`WebviewView`** lives in a sidebar or panel container. You do not create it — you register a provider, and VS Code constructs the view when the user reveals it. Use it for persistent, ambient UI that sits alongside the editor.

```typescript
class MySidebarProvider implements vscode.WebviewViewProvider {
  public static readonly viewType = 'myExt.sidebar';   // must match package.json

  constructor(private readonly extensionUri: vscode.Uri) {}

  resolveWebviewView(
    view: vscode.WebviewView,
    context: vscode.WebviewViewResolveContext,
    token: vscode.CancellationToken
  ): void {
    view.webview.options = {
      enableScripts: true,
      localResourceRoots: [vscode.Uri.joinPath(this.extensionUri, 'media')],
    };
    view.webview.html = getHtml(view.webview, this.extensionUri);

    view.webview.onDidReceiveMessage(msg => this.handle(msg));
  }
}

context.subscriptions.push(
  vscode.window.registerWebviewViewProvider(
    MySidebarProvider.viewType,
    new MySidebarProvider(context.extensionUri),
    { webviewOptions: { retainContextWhenHidden: false } }
  )
);
```

The manifest half is required, or the view never appears:

```json
{
  "contributes": {
    "views": {
      "explorer": [
        { "type": "webview", "id": "myExt.sidebar", "name": "My Extension" }
      ]
    }
  }
}
```

`"type": "webview"` is what distinguishes this from a tree view; omitting it makes VS Code expect a `TreeDataProvider` and the registration silently fails to bind.

**Choosing.** Sidebar view for something the user glances at while working (status, a filter panel, a chat surface). Editor panel for something they focus on. A webview view is also destroyed and recreated far more aggressively — every time the user collapses the container — so state persistence matters more there.

---

## The secure HTML template

```typescript
function getNonce(): string {
  // A fresh random token per render. Not a constant, not derived from content.
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let text = '';
  for (let i = 0; i < 32; i++) {
    text += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return text;
}

function getHtml(webview: vscode.Webview, extensionUri: vscode.Uri): string {
  const nonce = getNonce();

  // asWebviewUri rewrites a local file Uri into the vscode-webview-resource://
  // scheme the webview can actually load. A raw file:// path is blocked.
  const scriptUri = webview.asWebviewUri(
    vscode.Uri.joinPath(extensionUri, 'media', 'main.js'));
  const styleUri = webview.asWebviewUri(
    vscode.Uri.joinPath(extensionUri, 'media', 'main.css'));

  return /* html */ `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy" content="
    default-src 'none';
    style-src ${webview.cspSource} 'unsafe-inline';
    img-src ${webview.cspSource} https: data:;
    font-src ${webview.cspSource};
    script-src 'nonce-${nonce}';
    connect-src 'none';
  ">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="${styleUri}" rel="stylesheet">
  <title>Analysis Report</title>
</head>
<body>
  <h1 id="title">Analysis</h1>
  <div id="root"></div>
  <script nonce="${nonce}" src="${scriptUri}"></script>
</body>
</html>`;
}
```

What each directive is doing:

- **`default-src 'none'`** — deny everything not explicitly re-allowed. Start from zero; every other directive is a deliberate exception. Any resource type you forget is blocked rather than silently permitted.
- **`style-src ${webview.cspSource}`** — `webview.cspSource` is the per-webview origin string VS Code generates; it is the only value that matches the URIs `asWebviewUri` produces. Hardcoding an origin here does not work. `'unsafe-inline'` is added only if you actually set inline `style="..."` attributes; drop it when you can.
- **`img-src ... https: data:`** — widen only as far as you need. `data:` for inline SVG/base64, `https:` only if you genuinely load remote images (which leaks the user's IP to that host — consider bundling instead).
- **`script-src 'nonce-${nonce}'`** — the important one. Only `<script>` tags carrying this exact nonce execute. No `'unsafe-inline'`, no `'unsafe-eval'`. Injected script from a filename, a commit message, or an API response has no nonce and does not run.
- **`connect-src 'none'`** — no `fetch`/XHR/WebSocket from the webview. Network work belongs in the extension host, which has the user's proxy settings and credentials; the webview should ask for data over `postMessage`. Widen only with a specific host if there is a real reason.

**Never string-concatenate untrusted content into the HTML.** File contents, symbol names, error messages, API responses, commit text, workspace paths — all untrusted. A CSP with a nonce blocks the most direct script injection, but concatenation still lets an attacker break your DOM structure and forge UI.

Two correct approaches:

```typescript
// 1. Pass data over the message channel and let the webview render it into
//    the DOM as *text*. This is the default choice.
panel.webview.postMessage({ type: 'setTitle', value: userSuppliedName });
```

```javascript
// media/main.js — textContent, never innerHTML, for untrusted values.
window.addEventListener('message', (event) => {
  const msg = event.data;
  if (msg.type === 'setTitle') {
    document.getElementById('title').textContent = msg.value;
  }
});
```

```typescript
// 2. If a value truly must be baked into the initial HTML, escape it.
function escapeHtml(s: string): string {
  return s.replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[c]!));
}
```

For JSON baked into the page, `JSON.stringify` is not sufficient on its own — a `</script>` sequence inside a string still terminates the block. Escape the `<`:

```typescript
const payload = JSON.stringify(data).replace(/</g, '\\u003c');
```

**`localResourceRoots` is the second half of the boundary.** It scopes which directories the webview may load files from at all, regardless of CSP. Set it to the narrowest set that works — `media/` and `dist/`, not `extensionUri`. Omitting it defaults to the extension root, which is wider than you want. If you must load workspace files (images in a preview), add that specific folder Uri, and understand you are granting read access to it.

---

## Debugging a blank webview

The single most common failure: the panel opens, the tab has the right title, the content area is empty or shows only static HTML with no behavior.

**Open the developer tools first.** Command Palette → **"Developer: Open Webview Developer Tools"**. This is a real Chromium devtools window for the webview. The Console tab will name the exact CSP directive that blocked the exact URL. Every cause below is one line in that console; guessing without opening it wastes far more time than opening it.

Causes, in the order they actually occur:

1. **Missing or mismatched nonce.** The `<script>` tag has no `nonce` attribute, or the HTML was built with a different nonce than the one interpolated into the CSP — most often because `getNonce()` was called twice in the same render. Generate it once per `getHtml` call and use that one variable in both places. Console shows `Refused to execute inline script because it violates the following Content Security Policy directive`.

2. **`enableScripts` not set.** It defaults to `false`. No error, no console message, just an inert page. Check the options object on `createWebviewPanel` or `webview.options` in `resolveWebviewView`.

3. **Forgot `asWebviewUri`.** A raw `file://` path or a relative `./media/main.js` does not resolve in the webview's origin. Symptom is a 404-shaped failure in the Network tab and a missing script; the page renders its static HTML and nothing else. Every local resource — scripts, stylesheets, images, fonts — goes through `webview.asWebviewUri()`.

4. **`localResourceRoots` too narrow.** The Uri is correctly rewritten but points outside the allowed roots, so the load is refused. Common after moving files from `media/` to `dist/` without updating the roots array. The console message mentions the resource being outside allowed local resource roots.

5. **CSP typo.** A missing semicolon between directives silently merges two directives into one, and the second one stops applying. A missing `${webview.cspSource}` in `style-src` means the stylesheet loads but is blocked from applying — page renders unstyled rather than blank, which is the tell.

6. **Script error after load.** The script executes but throws on line one (a bad import, `acquireVsCodeApi` called twice). The Console shows a normal JS exception, not a CSP violation. Read the error before assuming CSP.

A useful bisect: temporarily replace the whole body with `<h1>hello</h1>` and no script. If that renders, the HTML pipeline works and the problem is in resource loading or CSP. If it does not, the problem is upstream — the html was never assigned, or the panel was disposed immediately.

---

## Message passing

The only channel between the two contexts. Both directions are async and structured-clone serialized — you can send plain objects, arrays, numbers, strings; you cannot send functions, class instances with methods, or `vscode.Uri` objects (call `.toString()`).

Define the protocol once and share the types:

```typescript
// src/protocol.ts — imported by both the extension and the webview bundle.
export type ToWebview =
  | { type: 'init'; items: ReadonlyArray<{ id: string; label: string }> }
  | { type: 'setBusy'; busy: boolean }
  | { type: 'error'; message: string };

export type FromWebview =
  | { type: 'ready' }
  | { type: 'select'; id: string }
  | { type: 'save'; text: string };
```

Extension side:

```typescript
import type { ToWebview, FromWebview } from './protocol';

function post(webview: vscode.Webview, msg: ToWebview): Thenable<boolean> {
  return webview.postMessage(msg);
}

panel.webview.onDidReceiveMessage(
  (raw: unknown) => {
    // Inbound messages are UNTRUSTED. The webview is a different trust context
    // and may be running content influenced by the workspace. Validate the
    // shape and the values before acting — never pass a field straight into
    // a filesystem path, a shell command, or executeCommand.
    if (typeof raw !== 'object' || raw === null || !('type' in raw)) { return; }
    const msg = raw as FromWebview;

    switch (msg.type) {
      case 'ready':
        void post(panel.webview, { type: 'init', items: loadItems() });
        return;
      case 'select':
        if (typeof msg.id !== 'string' || !isKnownId(msg.id)) { return; }
        void revealItem(msg.id);
        return;
      case 'save':
        if (typeof msg.text !== 'string' || msg.text.length > 100_000) { return; }
        void saveText(msg.text);
        return;
      default:
        return;   // unknown message types are ignored, not thrown on
    }
  },
  undefined,
  context.subscriptions
);
```

Webview side:

```javascript
// media/main.js
// acquireVsCodeApi() can be called ONCE per webview, ever. A second call
// throws, and because it usually happens on a module re-import or a second
// bundle include, the error surfaces far from its cause. Call it once at the
// top level of the entry module and pass the handle around.
const vscode = acquireVsCodeApi();

window.addEventListener('message', (event) => {
  const msg = event.data;              // ToWebview
  switch (msg.type) {
    case 'init':   render(msg.items);   break;
    case 'setBusy': setBusy(msg.busy);  break;
    case 'error':  showError(msg.message); break;
  }
});

document.getElementById('root').addEventListener('click', (e) => {
  const id = e.target.dataset.id;
  if (id) { vscode.postMessage({ type: 'select', id }); }
});

// Tell the extension the DOM is ready. Do not rely on the extension posting
// immediately after setting .html — messages sent before the script has
// attached its listener are dropped.
vscode.postMessage({ type: 'ready' });
```

The `ready` handshake matters. `webview.html = ...` returns before the webview has parsed and executed the script, so a `postMessage` fired right after assignment lands with nobody listening and is lost silently. Have the webview announce readiness and send the initial payload in response.

`postMessage` from the extension side returns a `Thenable<boolean>` that resolves `false` when the message could not be delivered — for example the webview is hidden and not retaining context. Treat that as normal, not as an error to report.

---

## State persistence

Three mechanisms, for three different disappearances.

**1. `setState` / `getState` — the webview is hidden and later shown again.** When a webview is hidden, VS Code destroys its DOM and JS context. On reveal, the HTML is re-evaluated from scratch: your script runs again, from zero. `setState` persists a JSON-serializable object across exactly that.

```javascript
const vscode = acquireVsCodeApi();

// Restore whatever survived; undefined on the very first render.
let state = vscode.getState() ?? { scrollTop: 0, filter: '', selectedId: null };
applyState(state);

function update(patch) {
  state = { ...state, ...patch };
  vscode.setState(state);            // cheap; safe to call often
}
```

Keep it small — UI state (scroll position, active tab, filter text, selection), not data. Data should be re-requested from the extension on `ready`, since the extension holds the authoritative copy anyway.

**2. `retainContextWhenHidden` — the same disappearance, brute-forced.**

```typescript
vscode.window.createWebviewPanel('myExt.report', 'Report', vscode.ViewColumn.One, {
  enableScripts: true,
  retainContextWhenHidden: true,   // costs memory for as long as the panel exists
});
```

This keeps the entire hidden context alive: DOM, JS heap, timers, everything, for every panel, for the whole session. **Prefer `setState`.** `retainContextWhenHidden` is defensible only when the state genuinely cannot be reconstructed — a live editing session with unsaved user input, a long-running in-page computation, a video or canvas mid-render. Reaching for it because rebuilding is inconvenient is how extensions get a reputation for making VS Code heavy.

**3. `WebviewPanelSerializer` — the window was reloaded or reopened.** `setState` does not survive a window reload on its own; something has to recreate the panel. A serializer, plus the matching activation event, does that.

```typescript
class ReportSerializer implements vscode.WebviewPanelSerializer {
  constructor(private readonly extensionUri: vscode.Uri) {}

  async deserializeWebviewPanel(panel: vscode.WebviewPanel, state: unknown): Promise<void> {
    // The panel already exists — VS Code restored the tab. Options do NOT
    // survive, so re-apply them before setting html.
    panel.webview.options = {
      enableScripts: true,
      localResourceRoots: [vscode.Uri.joinPath(this.extensionUri, 'media')],
    };
    panel.webview.html = getHtml(panel.webview, this.extensionUri);
    wirePanel(panel);

    // `state` is whatever the webview last passed to setState. Untrusted:
    // it round-tripped through storage. Validate before using.
    if (state && typeof state === 'object') {
      void panel.webview.postMessage({ type: 'restore', state });
    }
  }
}

context.subscriptions.push(
  vscode.window.registerWebviewPanelSerializer('myExt.report', new ReportSerializer(context.extensionUri))
);
```

```json
{
  "activationEvents": ["onWebviewPanel:myExt.report"]
}
```

The `viewType` string must match in all three places — `createWebviewPanel`, `registerWebviewPanelSerializer`, and the `onWebviewPanel:` activation event — or the restored tab shows an empty shell that never resolves. Without the activation event your extension is not running when VS Code tries to restore the panel, so the serializer is never reached.

---

## Lifecycle and disposal

A panel can close at any moment: the user hits the X, closes the tab group, or reloads the window. That is almost always long before `deactivate()`. So **anything scoped to a panel must be disposed when the panel closes, not when the extension does.**

Pushing per-panel listeners into `context.subscriptions` is the standard leak: open and close a panel fifty times and you accumulate fifty dead listeners, each holding its panel's closure alive, all still firing on every workspace event until the window reloads.

```typescript
export class ReportPanel {
  private static current: ReportPanel | undefined;
  private readonly disposables: vscode.Disposable[] = [];   // per-panel bag

  public static show(extensionUri: vscode.Uri): void {
    const column = vscode.window.activeTextEditor?.viewColumn ?? vscode.ViewColumn.One;

    // Singleton: reveal the existing panel rather than stacking duplicates.
    if (ReportPanel.current) {
      ReportPanel.current.panel.reveal(column);
      return;
    }

    const panel = vscode.window.createWebviewPanel(
      'myExt.report', 'Analysis Report', column,
      {
        enableScripts: true,
        localResourceRoots: [vscode.Uri.joinPath(extensionUri, 'media')],
      }
    );
    ReportPanel.current = new ReportPanel(panel, extensionUri);
  }

  private constructor(
    private readonly panel: vscode.WebviewPanel,
    extensionUri: vscode.Uri
  ) {
    this.panel.webview.html = getHtml(this.panel.webview, extensionUri);

    // Everything tied to this panel goes in the panel's own bag.
    this.disposables.push(
      this.panel.webview.onDidReceiveMessage(msg => this.handle(msg)),
      vscode.workspace.onDidSaveTextDocument(doc => this.refresh(doc)),
      this.panel.onDidChangeViewState(e => {
        if (e.webviewPanel.visible) { this.refresh(); }
      }),
    );

    // Fires when the user closes it AND when we call panel.dispose().
    this.panel.onDidDispose(() => this.dispose(), null, this.disposables);
  }

  public dispose(): void {
    ReportPanel.current = undefined;
    this.panel.dispose();                    // no-op if already disposed
    while (this.disposables.length) {
      this.disposables.pop()?.dispose();
    }
  }
}
```

Notes on the pattern:

- `onDidDispose` is the one hook you must always wire. It fires for both user-initiated close and programmatic `panel.dispose()`, so a single teardown path covers both.
- The singleton reveal-don't-recreate pattern is what users expect for report/preview panels. Track the instance, and clear the static reference in `dispose()` — forgetting that leaves a stale reference and `reveal()` throws on a disposed panel.
- If the extension also owns long-lived resources (a shared cache, a watcher used by every panel), those belong in `context.subscriptions`, not the per-panel bag. The split is by lifetime, not by convenience.

---

## Theming

The webview inherits nothing from the editor's styling. Hardcode `#ffffff` and half your users — everyone on a dark theme, plus every high-contrast user — get an unreadable page. VS Code injects CSS custom properties into every webview; use them.

```css
/* media/main.css */
body {
  background-color: var(--vscode-editor-background);
  color: var(--vscode-editor-foreground);
  font-family: var(--vscode-font-family);
  font-size: var(--vscode-font-size);
  font-weight: var(--vscode-font-weight);
  padding: 0 20px;
}

button {
  background-color: var(--vscode-button-background);
  color: var(--vscode-button-foreground);
  border: none;
  padding: 6px 14px;
  cursor: pointer;
}
button:hover { background-color: var(--vscode-button-hoverBackground); }
button:focus { outline: 1px solid var(--vscode-focusBorder); }

input, textarea {
  background-color: var(--vscode-input-background);
  color: var(--vscode-input-foreground);
  border: 1px solid var(--vscode-input-border, transparent);
}

a { color: var(--vscode-textLink-foreground); }
a:hover { color: var(--vscode-textLink-activeForeground); }

code, pre {
  font-family: var(--vscode-editor-font-family);
  font-size: var(--vscode-editor-font-size);
}

.error { color: var(--vscode-errorForeground); }
.muted { color: var(--vscode-descriptionForeground); }
.panel { border: 1px solid var(--vscode-panel-border); }
```

The variable names mirror the theme color keys in the VS Code color reference, with dots replaced by dashes: `button.hoverBackground` becomes `--vscode-button-hoverBackground`. Provide a fallback for anything you are not certain exists in every theme: `var(--vscode-input-border, transparent)`.

VS Code also puts a class on `<body>` — `vscode-light`, `vscode-dark`, or `vscode-high-contrast` (plus `vscode-high-contrast-light`) — for the cases where a variable is not enough:

```css
/* Shadows and overlays often need different treatment per theme kind. */
.card { box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12); }
body.vscode-dark .card { box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5); }

/* High contrast themes want visible borders instead of subtle fills. */
body.vscode-high-contrast .card {
  box-shadow: none;
  border: 1px solid var(--vscode-contrastBorder);
}
```

Both mechanisms update live: switching theme re-injects the variables and swaps the body class without recreating the webview, so a page built on them follows the user's theme with no JavaScript. A page built on hardcoded colors does not, and looks broken to a large fraction of users the moment it ships.

If you need a lot of standard controls, the `@vscode/webview-ui-toolkit` components implement this theming for you — but check its current maintenance status before adopting it, since its support state has changed over time.

---

**Signature check.** Webview options, the `WebviewView` API, and custom editors (`registerCustomEditorProvider`, which builds on the same webview primitives) have all evolved. Verify against the `vscode.d.ts` in the project's `@types/vscode` and against the `engines.vscode` floor in `package.json` before relying on anything you have not used recently.
