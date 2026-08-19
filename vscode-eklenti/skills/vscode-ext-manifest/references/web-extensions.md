# Web Extensions

Detailed reference for `browser` and the web extension host. The parent SKILL.md gives the constraint summary; this file has the manifest shapes, the porting map, the dual-target source layout, verification, and the decision of whether to attempt web support at all.

Official docs: `code.visualstudio.com/api/extension-guides/web-extensions`.

## Contents

- [What the web extension host is](#what-the-web-extension-host-is)
- [Manifest shapes](#manifest-shapes)
- [The constraints, and why each exists](#the-constraints-and-why-each-exists)
- [Porting map: Node pattern to web replacement](#porting-map-node-pattern-to-web-replacement)
- [Shared source, platform branches](#shared-source-platform-branches)
- [Verifying the browser bundle is actually clean](#verifying-the-browser-bundle-is-actually-clean)
- [Testing with @vscode/test-web](#testing-with-vscodetest-web)
- [When not to support web](#when-not-to-support-web)

## What the web extension host is

Desktop VS Code runs extensions in a Node.js process. **In the browser there is no Node process** — VS Code itself is JavaScript in a tab, and extensions run inside a **Web Worker**. That worker is the web extension host.

Where this actually runs:

- **vscode.dev** — VS Code in a browser tab, no backend.
- **github.dev** — pressing `.` on any GitHub repository.
- **GitHub Codespaces accessed through a browser** (the browser-side extension host; a Codespace also has a remote Node host).
- **Embedded/managed VS Code deployments** where users are given a browser URL rather than an install.

Why a company might care:

- **Zero-install review and editing.** A reviewer opens a PR in github.dev and your extension's syntax support, validation, and navigation are simply there.
- **Locked-down machines.** Environments where users cannot install desktop software still get the tooling.
- **Onboarding and demos.** A link is a lower barrier than an install, especially for a customer evaluating a DSL or config format you support.
- **Reach for the marketplace listing.** Web-capable extensions surface in browser contexts where non-web ones do not appear at all.

The single most important fact: **web extensions have the full VS Code API.** Commands, languages, diagnostics, tree views, webviews, decorations, workspace edits, the file system API — all present. What you lose is **Node.js**, and with it the ability to touch the machine directly. Most of the API you actually call in a well-written extension is `vscode.*`, which is exactly why porting is often more feasible than it first appears.

## Manifest shapes

`main` is the Node entry point; `browser` is the Web Worker entry point. Both may coexist.

**Desktop only** — the traditional shape:

```json
{
  "main": "./dist/node/extension.js",
  "engines": { "vscode": "^1.104.0" }
}
```

**Web only** — no Node code at all. Common for pure language support, themes with logic, or formatters implemented in TypeScript:

```json
{
  "browser": "./dist/web/extension.js",
  "engines": { "vscode": "^1.104.0" }
}
```

**Both** — VS Code picks the entry point matching the host it is running:

```json
{
  "main": "./dist/node/extension.js",
  "browser": "./dist/web/extension.js",
  "engines": { "vscode": "^1.104.0" },
  "capabilities": {
    "virtualWorkspaces": true
  }
}
```

Two behaviors worth knowing:

**VS Code treats an extension as web-capable if** the manifest has a `browser` entry point, **or** it lacks `main` **and** contributes none of: `localizations`, `debuggers`, `terminal`, or typescript server plugins. The second branch matters — a declarative-only extension (a theme, a grammar, a snippet pack) is web-capable without anyone deciding it should be, which is correct, since it has no code to break.

But the same rule means an extension that *does* have logic and simply omits `main` can be classified web-capable by accident. If you have no code entry point, that is fine. If you have code, declare an entry point deliberately.

**`vsce` tags web extensions automatically** based on manifest shape when packaging, so the marketplace listing reflects it without extra flags. `web` is a valid `--target` value for platform-specific packaging; whether `--target web` is *required* for a web extension versus merely available is not something to assume — check current `vsce` docs before adding it to a publish script.

Pair this with `capabilities.virtualWorkspaces`. Browser contexts are almost always virtual workspaces (github.dev files come from an API, not a disk). An extension that declares `browser` but `virtualWorkspaces: false` is contradicting itself in most of the places it would run — worth flagging in review.

## The constraints, and why each exists

Every constraint below traces to one fact: **the code runs in a Web Worker, not in Node.** A worker has no OS handle, no process table, no module loader, and a browser-enforced network policy.

**No `require()` of anything except `vscode`.** The host provides a `require` shim that resolves `require('vscode')` and nothing else. There is no module resolution algorithm, no `node_modules` lookup, no filesystem to resolve from. Your dependencies must be bundled into your code before it ships.

**No `importScripts`, no dynamic `import()`.** Consequently the bundle must be **a single file**. Code splitting, lazy chunks, and worker-loading tricks all break. This is the constraint that most often surprises a team porting a larger extension: a build that emits several chunks is not merely suboptimal, it does not run.

**No Node globals.** `process`, `os`, `path`, `util`, `url`, `setImmediate` are absent. `process.env` does not exist because there is no process. `path` is absent because there is no OS path semantics to implement — and note that path *string* manipulation is not the problem; the problem is that a bundler polyfill for `path` will silently give you POSIX semantics for URIs that are not POSIX paths.

**No child processes.** No `child_process`, no `spawn`, `exec`, or `fork`. A worker cannot create OS processes. This is absolute, and it is the constraint that decides whether a port is possible at all.

**No direct filesystem access.** No `fs`. Use `vscode.workspace.fs`, which routes through whatever `FileSystemProvider` is serving the workspace — the GitHub API on github.dev, an in-memory provider elsewhere. This is a genuine improvement even on desktop: `workspace.fs` works in virtual workspaces where `fs` does not.

**Network via the Fetch API, against CORS-compliant resources.** `http`/`https` Node modules are gone; `fetch` is available. The CORS part is the real constraint and it is enforced by the browser, not by VS Code: an API that works fine from your desktop extension will be blocked in the browser unless the server sends permissive CORS headers. You cannot fix this from extension code. Verify the endpoints you depend on before committing to a port.

**Webviews behave largely the same.** Webview content is an iframe in both hosts, so webview-heavy UI is often the most portable part of an extension — provided the extension side of the message channel is not doing Node work on the webview's behalf.

## Porting map: Node pattern to web replacement

| Node pattern | Web replacement | Notes |
|---|---|---|
| `fs.readFile` / `readFileSync` | `await vscode.workspace.fs.readFile(uri)` | Returns `Uint8Array`. Decode with `new TextDecoder().decode(bytes)`. |
| `fs.writeFile` | `await vscode.workspace.fs.writeFile(uri, bytes)` | Encode with `new TextEncoder().encode(text)`. |
| `fs.readdir` | `await vscode.workspace.fs.readDirectory(uri)` | Returns `[name, FileType][]`. |
| `fs.stat` / `existsSync` | `await vscode.workspace.fs.stat(uri)` | Throws `FileSystemError.FileNotFound` when absent — that rejection *is* the existence check. |
| `fs.mkdir` | `await vscode.workspace.fs.createDirectory(uri)` | Creates intermediate directories. |
| `path.join` | `vscode.Uri.joinPath(baseUri, ...segments)` | Correct across schemes; never concatenate URI strings. |
| `path.dirname` / `basename` | `Uri.joinPath(uri, '..')`; `uri.path.split('/').pop()` | Operate on `uri.path`, never `uri.fsPath`. |
| `uri.fsPath` | `uri.toString()` or `uri.path` | `fsPath` returns a string in a virtual workspace but it is not openable. |
| `child_process.spawn` / `exec` | **Not possible.** | Needs a hosted service, a WASM build of the tool, or a reimplementation in TypeScript. See [When not to support web](#when-not-to-support-web). |
| `process.env.FOO` | `vscode.workspace.getConfiguration()`, or a secret in `context.secrets` | No environment. Make it a setting. |
| `process.platform` | Not applicable | Branch on host at build time, not at runtime. |
| `os.homedir` / `tmpdir` | `context.globalStorageUri` / `context.storageUri` | Extension-scoped storage, works in both hosts. Prefer these on desktop too. |
| `crypto` (Node) | Web Crypto: `crypto.subtle`, `crypto.getRandomValues` | `subtle` is async. `crypto.randomUUID()` is available in both. |
| `Buffer` | `Uint8Array`, `TextEncoder`, `TextDecoder` | Also cleaner on desktop; `Buffer` is Node-only surface you did not need. |
| `http` / `https` / `axios` (Node adapter) | `fetch` | Endpoints must send CORS headers. |
| `setImmediate` | `queueMicrotask` or `setTimeout(fn, 0)` | Not identical scheduling, rarely load-bearing. |
| `require('./thing')` at runtime | Static `import` resolved at bundle time | No runtime module loading of any kind. |

A useful side effect: **most of these replacements are better on desktop too.** `workspace.fs` handles virtual workspaces, `Uri.joinPath` handles non-file schemes, `globalStorageUri` respects the user's portable install. Porting to web frequently fixes latent desktop bugs.

## Shared source, platform branches

The goal is one codebase producing two bundles, with platform differences isolated behind an interface rather than scattered through feature code.

The standard layout is three directories:

```
src/
  common/
    extension.ts        # shared activate() logic, feature registration
    fileSystem.ts       # the interface, not an implementation
    linter.ts           # feature code — imports the interface only
  node/
    extension.ts        # entry for `main`: builds Node impls, calls common
    nodeProcessRunner.ts
  browser/
    extension.ts        # entry for `browser`: builds web impls, calls common
    webProcessRunner.ts
```

**The rule that makes this work: `src/common/` must never import from `src/node/` or `src/browser/`.** Dependencies point inward. If common needs a capability that differs by platform, it declares an interface and receives an implementation.

Define the capability that differs:

```typescript
// src/common/toolRunner.ts
export interface ToolRunner {
  /** Runs the analysis tool over `content` and returns raw output. */
  run(content: string, fileName: string): Promise<string>;
}
```

Shared activation takes the platform pieces as arguments:

```typescript
// src/common/extension.ts
import * as vscode from 'vscode';
import type { ToolRunner } from './toolRunner';

export interface PlatformServices {
  toolRunner: ToolRunner;
}

export function activateShared(
  context: vscode.ExtensionContext,
  services: PlatformServices
) {
  const diagnostics = vscode.languages.createDiagnosticCollection('mylang');
  context.subscriptions.push(diagnostics);

  context.subscriptions.push(
    vscode.workspace.onDidSaveTextDocument(async doc => {
      if (doc.languageId !== 'mylang') return;
      const output = await services.toolRunner.run(doc.getText(), doc.fileName);
      diagnostics.set(doc.uri, parseDiagnostics(output));
    })
  );
}
```

Node entry point — spawns the real binary:

```typescript
// src/node/extension.ts
import * as vscode from 'vscode';
import { execFile } from 'child_process';
import { promisify } from 'util';
import { activateShared } from '../common/extension';
import type { ToolRunner } from '../common/toolRunner';

const execFileAsync = promisify(execFile);

const nodeToolRunner: ToolRunner = {
  async run(content, fileName) {
    const { stdout } = await execFileAsync('mylint', ['--stdin', fileName], {
      // pass content on stdin in real code
    });
    return stdout;
  }
};

export function activate(context: vscode.ExtensionContext) {
  activateShared(context, { toolRunner: nodeToolRunner });
}
```

Browser entry point — the same capability, obtained differently:

```typescript
// src/browser/extension.ts
import * as vscode from 'vscode';
import { activateShared } from '../common/extension';
import type { ToolRunner } from '../common/toolRunner';
import { analyzeInProcess } from '../common/pureAnalyzer';

const webToolRunner: ToolRunner = {
  async run(content, fileName) {
    // Option A: a TypeScript reimplementation that runs anywhere.
    return analyzeInProcess(content, fileName);

    // Option B: a CORS-enabled hosted service.
    // const res = await fetch('https://lint.example.com/analyze', {
    //   method: 'POST',
    //   headers: { 'content-type': 'application/json' },
    //   body: JSON.stringify({ content, fileName })
    // });
    // if (!res.ok) throw new Error(`Lint service failed: ${res.status}`);
    // return await res.text();
  }
};

export function activate(context: vscode.ExtensionContext) {
  activateShared(context, { toolRunner: webToolRunner });
}
```

Build both with esbuild, `platform: 'browser'` for the web bundle, and **`format: 'cjs'` with a single output file** — code splitting must stay off:

```javascript
// esbuild.js
const esbuild = require('esbuild');

const shared = {
  bundle: true,
  external: ['vscode'],   // provided by the host in BOTH targets
  minify: true,
  sourcemap: true,
  format: 'cjs'
};

Promise.all([
  esbuild.build({
    ...shared,
    entryPoints: ['src/node/extension.ts'],
    outfile: 'dist/node/extension.js',
    platform: 'node'
  }),
  esbuild.build({
    ...shared,
    entryPoints: ['src/browser/extension.ts'],
    outfile: 'dist/web/extension.js',
    platform: 'browser',
    // No `inject` of Node polyfills. If the build fails for a missing Node
    // module, that is a real finding — fix the import, do not polyfill it.
  })
]).catch(() => process.exit(1));
```

## Verifying the browser bundle is actually clean

**A successful build is not proof.** This is the single most important operational point in this file.

Bundlers are permissive by design. Depending on configuration and plugins, a Node import in your dependency tree may be silently replaced with a shim that throws only when called, resolved to a browser polyfill with different semantics, or stubbed to an empty module so `fs.readFile` becomes `undefined` and you get `TypeError: fs.readFile is not a function` at runtime — inside a user's browser tab, in a code path your tests did not exercise.

Worse, the offending import is usually in a **transitive dependency**, not your source. Auditing `src/` finds nothing.

Grep the built artifact:

```bash
# Node built-ins that should never appear in the web bundle.
grep -nE "require\(['\"](fs|path|os|child_process|crypto|http|https|net|tls|stream|zlib|util|url)['\"]\)" \
  dist/web/extension.js

# Node globals that survived bundling.
grep -nE "\b(process\.(env|platform|cwd)|__dirname|__filename|setImmediate|Buffer\.)" \
  dist/web/extension.js

# Forbidden dynamic loading — the single-file rule.
grep -nE "\b(importScripts|import\()" dist/web/extension.js
```

Reading the results needs care, because minified bundles produce noise:

- **`require('vscode')` is expected and correct.** The host shim provides it.
- **`process.env.NODE_ENV` inside a bundled library** is a common false-ish positive. It is only safe if your build **defines** it away (`define: { 'process.env.NODE_ENV': '"production"' }`); otherwise it throws at runtime. Confirm which case you are in rather than waving it through.
- **String literals in error messages** can match these patterns harmlessly. Look at the surrounding code, not just the line count.
- **A polyfilled `path` module inlined by the bundler** will not match `require('path')` — it will be inlined function bodies. This is why grep is a screen, not a proof.

Add a size check as a second signal. A web bundle that is dramatically larger than the Node one usually means polyfills got pulled in:

```bash
ls -la dist/web/extension.js dist/node/extension.js
```

**The only real proof is running it.** Grep catches the obvious cases cheaply; `@vscode/test-web` catches the rest.

## Testing with @vscode/test-web

`@vscode/test-web` downloads a VS Code web build, serves it on **localhost:3000**, and loads your extension into the browser host — the actual environment, not a simulation.

Run against a folder of test data:

```bash
npx @vscode/test-web --extensionDevelopmentPath=$(pwd) ./test-data
```

Choose the browser engine:

```bash
npx @vscode/test-web \
  --browserType=chromium \
  --extensionDevelopmentPath=$(pwd) \
  ./test-data
```

`--browserType` accepts `chromium`, `firefox`, and `webkit`. Test in more than one when you rely on newer web platform features — worker and Fetch behavior differ at the edges.

Wire it into `package.json` alongside the build:

```json
{
  "scripts": {
    "compile-web": "node esbuild.js",
    "open-in-browser": "npm run compile-web && vscode-test-web --extensionDevelopmentPath=. ./test-data"
  },
  "devDependencies": {
    "@vscode/test-web": "^0.0.60"
  }
}
```

What to actually exercise once it is open:

1. **That the extension activated at all.** A Node import that survived bundling typically throws during activation; the extension simply never starts. Check the browser devtools console — the worker's errors land there, not in a VS Code output channel.
2. **Every code path that touches files.** The test-data folder is served through a `FileSystemProvider`, so this is where a lingering `fs` call or an `fsPath` assumption surfaces.
3. **Every network call.** CORS failures appear only in a real browser.
4. **Commands from the palette**, including ones you assume are trivial.

Automated tests can run in this harness as well, though the setup is heavier than desktop `@vscode/test-electron`. Even manual verification here is worth far more than a clean build, because it exercises the worker boundary that the build never checks.

## When not to support web

**If the extension's core value requires executing local binaries, web support is not achievable by patching.** Say so at the start of the work, not after two days of bundler debugging.

Cases where the answer is simply no:

- The extension **is** a wrapper around a CLI tool — a compiler, a formatter binary, a package manager, a version control client beyond what VS Code provides natively.
- It needs **a language server distributed as a native executable**. (A language server written in TypeScript or compiled to WASM is a different story and can work.)
- It reads or writes **outside the workspace** — dotfiles in the home directory, system config, a local database.
- It integrates with **locally running services** by port or unix socket.
- It depends on **native Node modules** (`.node` addons). These cannot be bundled for a worker at all.

The honest framing for a stakeholder: **this is a structural decision, not a build configuration.** The web host has no process table. There is no flag, polyfill, or bundler setting that creates one. The paths forward are all substantial projects in their own right:

- **Reimplement the tool's logic in TypeScript.** Viable for a parser or a formatter, not for a compiler.
- **Compile the tool to WebAssembly.** Real, increasingly common, and a significant piece of work with its own filesystem-shim problems.
- **Move the work to a hosted service** the extension calls over `fetch`. Now you own a service, its availability, its CORS configuration, and the privacy question of sending user code to it.
- **Ship a reduced web build** — the shape most teams land on. Syntax, navigation, formatting, and validation that can run in-process go to web; anything requiring the binary stays desktop-only, declared honestly.

That last option is what the dual-entry-point manifest and the `PlatformServices` pattern above are for. It is a legitimate and common outcome, and it is much better than a web bundle that installs and then fails.

Decide this **before** writing the abstraction layer. Retrofitting a `ToolRunner` interface through a mature codebase is expensive; discovering afterward that the web implementation can never exist makes that expense pure waste. The question to answer first is not "how do we build for web" but "what, if anything, can our extension do without a process".
