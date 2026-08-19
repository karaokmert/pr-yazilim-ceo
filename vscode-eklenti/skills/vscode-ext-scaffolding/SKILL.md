---
name: vscode-ext-scaffolding
description: Canon for setting up and restructuring VS Code extension projects — project layout, bundler choice and esbuild/webpack configuration, tsconfig for the extension host, the .vscodeignore package boundary, launch.json debug setup, the activate/deactivate lifecycle skeleton, and monorepo layout for teams shipping multiple extensions. Load this when creating a new extension from scratch, when reworking an existing project's structure or build, when startup performance or activation strategy needs redesign, when setting up shared code across several extensions, or when a packaged .vsix turns out to contain the wrong files.
---

# Extension Project Scaffolding

This is the architect's canon: the decisions that set the shape feature code lives inside. They are cheap now and expensive later — activation strategy, disposal pattern, and the package boundary are all far harder to retrofit than to establish.

Manifest specifics live in `vscode-ext-manifest`. This skill covers everything around it.

## Establish these before generating anything

Four answers drive most of the setup. Ask, or infer and state the assumption explicitly:

1. **What triggers this extension?** Specific languages? Explicit command only? Presence of a file in the workspace? A view being opened? This drives the activation strategy and much of the manifest.
2. **Internal or published?** The rigor dial from `vscode-ext-behavior`. It decides whether LICENSE, icon, and marketplace-grade README are in scope now or deferred.
3. **Desktop only, or also the web extension host?** This is structural. Web support forbids `fs` and `child_process` everywhere reachable from the browser bundle — discovering it after features are written means rewriting them.
4. **One extension or several sharing code?** Monorepo decisions are painful to make retroactively once two extensions have diverged.

**Scaffold minimally, then justify every addition.** Generated templates leave behind sample commands, placeholder contribution points, and unused config. Every `contributes` entry and every dependency should map to something actually asked for. Leftover boilerplate is not neutral — it activates, it ships, and the next person assumes it's load-bearing.

## Project layout

The conventional shape, which is worth following because tooling and every other VS Code developer assume it:

```
extension-root/
├── .vscode/
│   ├── launch.json        # Extension Development Host debug config
│   └── tasks.json         # build task the debugger depends on
├── src/
│   ├── extension.ts       # activate() / deactivate()
│   └── test/
├── dist/                  # bundled output (gitignored, shipped)
├── package.json           # the manifest
├── tsconfig.json
├── esbuild.js
├── .vscodeignore          # what stays OUT of the .vsix
└── README.md / CHANGELOG.md / LICENSE
```

Keep `src/extension.ts` thin — activation wiring only, with features in their own modules registered from it. An `extension.ts` that grows to hundreds of lines is the reliable early symptom of a project that will be hard to test.

## Bundling

**Bundle.** An unbundled extension ships hundreds of loose files and its `node_modules`, which inflates the `.vsix`, slows install, and measurably slows activation — every `require` is a file read.

**esbuild is the default for new projects**: fast, small config, and the current recommendation for extensions. Use **webpack** only for a concrete reason — an existing team convention or loaders esbuild can't cover. State the choice and the reason either way.

The build config needs, at minimum:

- **`platform: 'node'`** and **`format: 'cjs'`** for the desktop bundle. The extension host loads CommonJS.
- **`external: ['vscode']`** — this one is not optional. The `vscode` module is injected by the host at runtime and is not on disk. Bundling it fails at load with a confusing error.
- **Separate dev and production scripts** — dev with `--sourcemap --watch` so the debugger maps to TypeScript; production `--minify` without sourcemaps.

Working esbuild and webpack configs, plus the watch-task wiring the debugger needs, are in `references/build-setup.md`.

## TypeScript configuration

- **`"strict": true`** by default. The API is full of legitimately optional values — `activeTextEditor`, `workspaceFolders`, provider returns — and strict mode is what forces the absence-handling that would otherwise become a runtime crash for a user in a state you didn't imagine.
- **`module`/`target`** must match the Node runtime the extension host actually runs. Check the current value rather than assuming; VS Code's bundled Node moves with releases.
- **`@types/vscode` no newer than `engines.vscode`** — see `vscode-ext-manifest`. Types ahead of the engine compile against APIs that don't exist on the oldest version you claim to support.

## .vscodeignore: the package boundary

`.vscodeignore` decides what ends up in the `.vsix`. It's inverted from `.gitignore` in purpose — you're excluding from a *shipped artifact*, not from source control — and it is a recurring source of shipped mistakes.

What must **not** ship: `src/`, tests and fixtures, `node_modules` dev dependencies, `.git`, `.env` or any credential file, build configs, sourcemaps in production.

What must ship: the bundled output, `package.json`, README, CHANGELOG, LICENSE, icon, and any runtime assets (webview HTML/CSS, images, grammars).

When bundling, the typical shape excludes everything and re-includes `dist/` — but **verify by inspecting the actual built package**, never by reading the ignore file and reasoning about it. A trailing-slash difference silently changes what matches. Inspection procedure is in `vscode-ext-release`; the point here is that scaffolding sets this up and packaging verifies it — neither step alone is sufficient.

## Debug configuration

`.vscode/launch.json` launches the Extension Development Host — a second VS Code window with the extension loaded. Without it the developer has no way to run their work.

It needs `--extensionDevelopmentPath` pointed at the project root, a `preLaunchTask` that builds first (otherwise you debug a stale bundle — a genuinely confusing failure), and `outFiles` pointed at the bundled output so breakpoints map correctly.

Config in `references/build-setup.md`.

## The lifecycle skeleton

`activate()` is called on the first triggering event; `deactivate()` on shutdown.

**Establish the disposal pattern in the initial skeleton.** This is the highest-leverage thing scaffolding does, because it's a convention every future contributor inherits by imitation. If the first three registrations push into `context.subscriptions`, the fourth will too. If the skeleton is sloppy, every feature added later leaks by default and retrofitting means auditing everything.

Keep `activate()` fast and lazy. It runs while the user waits. Register cheaply; defer expensive work — index building, network calls, process spawning — until something actually needs it. If real work must happen at activation, put it behind `onStartupFinished` rather than blocking startup.

`activate()` can be `async` and return a promise; VS Code awaits it. That's for genuine setup, not for the heavy lifting.

`deactivate()` is only needed for cleanup that `context.subscriptions` can't express — flushing state, terminating child processes. Anything disposable should already be handled.

## Monorepo layout for multiple extensions

Relevant when a team ships several extensions (this team does — some internal, some published).

The choice is between three options, and the honest answer is usually the first:

- **Separate repos, deliberate duplication.** Best for two extensions sharing a little utility code. Duplication is cheaper than build complexity at small scale.
- **Workspace monorepo with a shared package** (npm/pnpm workspaces). Right when several extensions share substantial logic. The cost is real: every extension's bundler must resolve the shared package, and `.vscodeignore` has to be right per-extension.
- **Published private npm package.** Right when sharing crosses repo or team boundaries, at the cost of a publish step between change and use.

Whichever you pick, **each extension keeps its own `package.json` manifest, its own version, and its own `.vsix`** — extensions version and ship independently, always.

Layout and per-package build wiring are in `references/monorepo.md`.

## Restructuring an existing project

Don't big-bang rewrite. A large unexplained restructuring is unreviewable, and it mixes structural change with behavior change so that when something breaks nobody can tell which caused it.

Instead: name the specific problem, propose the scoped fix, and change only that. If a project activates on `*`, has no build step, and has no disposal pattern, those are three separate changes with three separate justifications — and they can land in that order, each verifiable.

The common structural problems and their scoped fixes are in `references/restructuring.md`.

## Handing off

The developer needs, explicitly: the activation strategy and why, where disposables go, the internal-vs-published posture, whether the web extension host is a target, and how to run the dev build. Full handoff format is in `vscode-ext-workflow`.

## References

- `references/build-setup.md` — esbuild/webpack configs, tsconfig, launch.json, tasks.json.
- `references/monorepo.md` — multi-extension layout and shared packages.
- `references/restructuring.md` — diagnosing and scoping fixes to existing projects.
