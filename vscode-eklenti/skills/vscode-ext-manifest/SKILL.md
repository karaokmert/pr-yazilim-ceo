---
name: vscode-ext-manifest
description: Canon for the VS Code extension manifest (package.json) — activation events and auto-generation, contribution points, engines/@types pinning, capabilities declarations for untrusted and virtual workspaces, main vs browser entry points, and the marketplace metadata fields. Load this whenever package.json is being written, extended, reviewed, or debugged — when adding a command, view, setting, menu, or keybinding, when choosing or fixing an activation strategy, when a contribution silently fails to appear, when declaring workspace trust or web support, and before packaging or publishing. All three agents (architect, developer, qa-publisher) share this file.
---

# The Extension Manifest

`package.json` is the most consequential file in an extension. It is the only place where the code you wrote and the editor's expectations meet, and **it fails quietly**: a malformed contribution point does not throw, it just never appears. That single property is why this skill exists and why the discipline below is worth the effort.

All three agents touch this file — the architect creates it, the developer adds entries alongside features, qa-publisher validates it before shipping — so the canon lives here once rather than in three places.

**Verify schema against current docs before writing.** The manifest reference is at `code.visualstudio.com/api/references/extension-manifest` and the contribution points at `.../contribution-points`. Guessing a field shape here is how you lose an afternoon.

## Activation events

An extension starts inert. `activationEvents` — plus the auto-generated ones described below — decide when VS Code wakes it up. Every millisecond of your activation is a millisecond of the user's editor startup, shared with every other extension they have installed. This is the single biggest performance lever you control.

### Auto-generation: don't list what's already implied

Since **VS Code 1.74**, activation events are **generated automatically from `contributes`**. If you declare a command in `contributes.commands`, you do not also write `onCommand:` for it. The auto-generated set is `onCommand`, `onLanguage`, `onView`, `onCustomEditor`, `onAuthenticationRequest`, and — since 1.76 — `onTaskType`.

A consequence worth internalizing: **a modern manifest's `activationEvents` array is often legitimately empty or absent entirely.** An array full of `onCommand:` entries mirroring `contributes.commands` is a reliable tell that the manifest was copied from a pre-1.74 template. It isn't an error, but it's noise that hides the events that *are* deliberate.

Events that still need an explicit entry: `workspaceContains:`, `onStartupFinished`, `onFileSystem:`, `onDebug`, and the rest. See `references/activation.md`.

### Choosing the narrowest event that works

Ordered from best to worst:

- **Auto-generated from a contribution** — the extension wakes when the user actually invokes the thing. Ideal.
- **`workspaceContains:<glob>`** — wakes only in workspaces that actually contain the relevant file. Excellent for tooling that is irrelevant in most projects.
- **`onLanguage:<id>`** — wakes when a file of that language opens.
- **`onStartupFinished`** — wakes after the editor has finished starting. For background work with no natural trigger. It does not delay startup, which is what makes it acceptable where `*` is not.
- **`*`** — wakes during startup, every time, in every window. In most cases where it appears, `onStartupFinished` was the intended behavior.

`*` is not merely discouraged — **`vsce package` refuses to build with it** unless you pass `--allow-star-activation`. Treat reaching for that flag as a signal to reconsider rather than as the fix. If you genuinely need it, say in your report why nothing narrower works; if you can't articulate it, it's the wrong choice.

## Contribution points

`contributes` declares what the extension adds to the editor: commands, menus, views, viewsContainers, configuration, keybindings, languages, grammars, snippets, walkthroughs, and more.

The rule that prevents the most common silent failure:

> **Code and manifest entry are one unit of work, never two.**

A command registered with `vscode.commands.registerCommand` but absent from `contributes.commands` will not appear in the command palette. A setting read via `getConfiguration()` with no `contributes.configuration` schema won't show in the Settings UI, gets no validation, and has no discoverable default. Neither of these errors. They just don't work, and the developer stares at correct-looking code.

The inverse also matters: a `contributes.commands` entry with no registered handler produces a palette item that throws when clicked.

Two things worth internalizing beyond that:

- **`contributes.menus` is separate from `contributes.commands`.** Declaring a command makes it exist; menu placement decides whether it appears in the command palette, the editor title bar, the explorer context menu, or nowhere. `when` clauses control visibility — see `references/contribution-points.md`.
- **Declaring a contribution is cheap; activating is not.** Most contributions are declarative and cost nothing until invoked. A few force early activation. Know which you're adding.

Per-contribution schemas, `when`-clause context keys, and menu group ordering are in `references/contribution-points.md`.

## engines.vscode and @types/vscode

These two must agree, and the direction of the rule matters:

- **`engines.vscode`** is the *minimum* VS Code version the extension supports. A user on an older version won't be offered the extension.
- **`@types/vscode`** must be **the same version or older** than `engines.vscode`.

The failure this prevents: types newer than your declared engine let you compile against an API that doesn't exist on the oldest version you claim to support. It builds clean and throws at runtime on a real user's machine. `vsce` checks this pairing at package time.

In practice, declare both with the same minor version:

```json
"engines": { "vscode": "^1.104.0" },
"devDependencies": { "@types/vscode": "^1.104.0" }
```

Two details that matter:

- **`^1.8.0` means "1.8.0 and onwards"; a bare `1.8.0` means that version only.** Use the caret unless you genuinely mean to pin.
- **`@types/vscode` lags the shipping VS Code release.** "Latest types" and "latest VS Code" are different numbers, so don't infer your engine floor from the product version.

Set `engines.vscode` to the oldest version that has every API you actually use — not "latest", and not a stale template value that now blocks an API you're calling.

## capabilities: trust and virtual workspaces

`capabilities` declares how the extension behaves in two restricted contexts. **Defaults are assumed if you omit these, and the assumed default is not always the safe one** — declare them deliberately.

- **`untrustedWorkspaces`** — behavior in Restricted Mode, which VS Code enters for folders the user hasn't trusted. This matters because opening an untrusted repo must not let it execute code. If the extension runs anything from the workspace (a linter binary, a config-specified command), it is not safe untrusted.
- **`virtualWorkspaces`** — behavior when the workspace isn't on a real disk (GitHub repos opened remotely, other virtual file systems). Anything using Node `fs` paths or spawning processes against workspace files does not work here.

Both express support as `true`, `false`, or `"limited"`:

```json
"capabilities": {
  "untrustedWorkspaces": {
    "supported": "limited",
    "description": "Only syntax features are available until the workspace is trusted.",
    "restrictedConfigurations": ["myExt.formatterPath"]
  },
  "virtualWorkspaces": {
    "supported": false,
    "description": "Running the linter requires files on disk."
  }
}
```

Three things the shapes don't make obvious:

- **`description` is required** when `supported` is `false` or `"limited"` — it's shown to the user, so write it for them.
- **`restrictedConfigurations`** lists setting IDs whose *workspace-provided* values should be ignored until trust is granted. Any setting naming an executable or a path that gets run belongs here.
- **`virtualWorkspaces` also accepts a bare boolean** (`"virtualWorkspaces": true`) and has no `restrictedConfigurations`. It defaults to `true` when unspecified — which is why an extension that needs real files on disk must declare `false` deliberately.

More in `references/capabilities.md`.

Declare these **honestly relative to what the code actually does**. A false `untrustedWorkspaces: true` is a security misrepresentation, and it's exactly the kind of thing marketplace review catches — or worse, doesn't.

## main, browser, and the web extension host

- **`main`** — the Node.js entry point, for desktop VS Code. Full Node API available.
- **`browser`** — the Web Worker entry point, for vscode.dev and github.dev.

Web extensions keep the **full VS Code API** but lose Node entirely. Unavailable in a browser bundle: `fs`, `child_process`, and the Node globals `process`, `os`, `path`, `util`, `url`, `setImmediate`. No spawning executables, no direct filesystem access (use `workspace.fs`), and network calls must use `fetch` against CORS-permitting endpoints. The bundle must also be **a single file** — `importScripts` and dynamic imports don't work, and the `require()` shim resolves only `require('vscode')`.

This is a structural constraint, not something to patch around in feature code. A feature that shells out to a binary is simply incompatible with the web host; flag the conflict rather than working around it.

An extension may declare both entry points and share source behind platform branches. Note that VS Code treats an extension as web-capable if it has a `browser` entry **or** has no `main` and contributes none of `localizations`, `debuggers`, `terminal`, or typescript server plugins — so an extension can be surfaced as web-capable without anyone deciding it should be. See `references/web-extensions.md`.

## Marketplace metadata

Required or effectively required when publishing publicly; optional for internal-only (see the rigor dial in `vscode-ext-behavior`):

- `publisher` — must match your marketplace publisher ID exactly.
- `name`, `displayName`, `description`, `version` — version must be plain `major.minor.patch`; **semver pre-release tags like `1.2.0-beta` are not supported** (use `vsce publish --pre-release` instead).
- `icon` — **PNG, at least 128×128. SVG icons are rejected.**
- `categories`, `keywords` — discoverability.
- `repository` — its absence forces `--allow-missing-repository` at package time.
- `license` / `LICENSE` file — its absence forces `--skip-license`.
- `README.md` — this *is* the marketplace listing page. Images must be served over HTTPS, and SVGs are prohibited except from trusted badge providers.

Publishing mechanics and the pre-publish checklist belong to `vscode-ext-release`; this section covers only what lives in the manifest.

## Reviewing a manifest

When validating (qa-publisher especially), check these in order — they catch the recurring real failures:

1. Every `contributes.commands` entry has a registered handler, and every registered command has an entry.
2. Every `getConfiguration()` key read in code exists in `contributes.configuration`.
3. `@types/vscode` is not newer than `engines.vscode`.
4. `capabilities` reflect what the code actually does.
5. No `*` activation without a stated reason.
6. If `browser` is declared, no Node-only API is reachable from that bundle.
7. Publishing: `publisher`, `icon`, `repository`, `license`, README present.

## References

- `references/activation.md` — auto-generation rules, full event list, startup performance.
- `references/contribution-points.md` — per-contribution schemas, `when` clauses, menu groups.
- `references/capabilities.md` — trust and virtual workspace declarations.
- `references/web-extensions.md` — dual-target builds and Node API constraints.
