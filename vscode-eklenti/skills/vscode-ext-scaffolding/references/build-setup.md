# Build and Tooling Setup

Working configurations for a VS Code extension build. These are starting points to adapt, not
templates to paste — the reasoning next to each block tells you which parts are load-bearing and
which are project preference.

## Contents

- [1. esbuild setup](#1-esbuild-setup)
- [2. webpack alternative](#2-webpack-alternative)
- [3. Dual desktop + web builds](#3-dual-desktop--web-builds)
- [4. tsconfig.json](#4-tsconfigjson)
- [5. .vscode/launch.json](#5-vscodelaunchjson)
- [6. .vscode/tasks.json](#6-vscodetasksjson)
- [7. .vscodeignore](#7-vscodeignore)

---

## 1. esbuild setup

esbuild is the bundler the extension documentation recommends. The build is a plain Node script
rather than a config file, which is what makes the watch/production split and the problem-matcher
plugin below possible without extra tooling.

`esbuild.js` at the project root:

```javascript
const esbuild = require('esbuild');

const production = process.argv.includes('--production');
const watch = process.argv.includes('--watch');

/**
 * Emits the exact markers the VS Code problem matcher in tasks.json looks for.
 * Without these, a watch build never reports "finished" and the debugger waits forever
 * on its preLaunchTask. See section 6.
 * @type {import('esbuild').Plugin}
 */
const esbuildProblemMatcherPlugin = {
  name: 'esbuild-problem-matcher',
  setup(build) {
    build.onStart(() => {
      console.log('[watch] build started');
    });
    build.onEnd((result) => {
      result.errors.forEach(({ text, location }) => {
        console.error(`✘ [ERROR] ${text}`);
        if (location) {
          console.error(`    ${location.file}:${location.line}:${location.column}:`);
        }
      });
      console.log('[watch] build finished');
    });
  },
};

async function main() {
  const ctx = await esbuild.context({
    entryPoints: ['src/extension.ts'],
    bundle: true,
    format: 'cjs',
    minify: production,
    sourcemap: !production,
    sourcesContent: false,
    platform: 'node',
    outfile: 'dist/extension.js',
    external: ['vscode'],
    logLevel: 'silent',
    plugins: [esbuildProblemMatcherPlugin],
  });

  if (watch) {
    await ctx.watch();
  } else {
    await ctx.rebuild();
    await ctx.dispose();
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
```

Why each option is what it is:

- **`external: ['vscode']` is mandatory.** The `vscode` module is injected by the extension host at
  runtime; it does not exist on disk and cannot be resolved. Bundling it produces a load-time failure
  with an error message that does not point at the cause. Any other module the host provides — or
  that must stay unbundled, like a native `.node` addon — goes in this array too.
- **`format: 'cjs'` + `platform: 'node'`** — the desktop extension host loads CommonJS. ESM output
  will not load.
- **`sourcemap` in dev only, `minify` in production.** Sourcemaps are what make breakpoints land on
  TypeScript instead of the bundle; they also roughly double the shipped size and expose source, so
  they are off for the published build. `sourcesContent: false` keeps the dev sourcemap small by
  referencing files on disk rather than embedding them — fine locally, since the sources are there.
- **`logLevel: 'silent'` + the plugin.** esbuild's own output is suppressed so the plugin owns the
  console format. If you drop the plugin, drop this too or you will lose error reporting entirely.
- **`esbuild.context()` rather than `esbuild.build()`** — a context supports both `.watch()` and a
  one-shot `.rebuild()`, so a single script covers every mode.

Matching `package.json` scripts:

```json
{
  "main": "./dist/extension.js",
  "scripts": {
    "compile": "npm run check-types && node esbuild.js",
    "watch": "npm-run-all -p watch:*",
    "watch:esbuild": "node esbuild.js --watch",
    "watch:tsc": "tsc --noEmit --watch --project tsconfig.json",
    "check-types": "tsc --noEmit",
    "package": "npm run check-types && node esbuild.js --production",
    "vscode:prepublish": "npm run package"
  }
}
```

**esbuild does not type-check.** It strips types and emits; a type error will bundle happily and fail
at runtime. That is why `check-types` (`tsc --noEmit`) runs separately — once before a build, and
continuously in watch mode as `watch:tsc`. Dropping it is the single most common way an esbuild
extension setup ends up worse than the tsc setup it replaced.

`vscode:prepublish` is run automatically by `vsce package` / `vsce publish`, which is what guarantees
the shipped `.vsix` contains the production bundle rather than whatever was last built locally.

---

## 2. webpack alternative

Use webpack when there is a concrete reason: an existing team convention, or loaders esbuild cannot
cover. It is slower and the config is larger; there is no advantage by default.

`webpack.config.js`:

```javascript
'use strict';

const path = require('path');

/** @type {import('webpack').Configuration} */
const extensionConfig = {
  target: 'node',
  mode: 'none', // set by the --mode CLI flag; 'none' avoids surprise defaults
  entry: './src/extension.ts',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'extension.js',
    libraryTarget: 'commonjs2',
  },
  externals: {
    vscode: 'commonjs vscode', // same mandatory rule as esbuild: provided by the host
  },
  resolve: {
    extensions: ['.ts', '.js'],
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        exclude: /node_modules/,
        use: [{ loader: 'ts-loader' }],
      },
    ],
  },
  devtool: 'nosources-source-map',
  infrastructureLogging: {
    level: 'log', // required for the webpack problem matcher in tasks.json
  },
};

module.exports = [extensionConfig];
```

Notes:

- `externals: { vscode: 'commonjs vscode' }` is webpack's spelling of `external: ['vscode']`.
- `ts-loader` type-checks as it compiles, so there is no separate `check-types` step the way esbuild
  needs one.
- `devtool: 'nosources-source-map'` maps stack traces without embedding source. Use
  `source-map` during development if you want full breakpoint fidelity, and keep sourcemaps out of
  the shipped `.vsix` via `.vscodeignore` either way.
- `infrastructureLogging.level: 'log'` is not cosmetic — the built-in `$ts-webpack-watch` matcher
  parses that output to detect build start/end.

Scripts: `"compile": "webpack"`, `"watch": "webpack --watch"`,
`"package": "webpack --mode production --devtool hidden-source-map"`.

---

## 3. Dual desktop + web builds

A web extension runs in a **Web Worker**, not Node. Supporting both means producing two bundles from
one source tree and declaring both in the manifest.

```javascript
const shared = {
  bundle: true,
  format: 'cjs',           // both hosts load CommonJS
  minify: production,
  sourcemap: !production,
  external: ['vscode'],
  logLevel: 'silent',
  plugins: [esbuildProblemMatcherPlugin],
};

const nodeCtx = await esbuild.context({
  ...shared,
  entryPoints: ['src/extension.ts'],
  platform: 'node',
  outfile: 'dist/extension.js',
});

const webCtx = await esbuild.context({
  ...shared,
  entryPoints: ['src/web/extension.ts'],
  platform: 'browser',
  outfile: 'dist/web/extension.js',
});
```

Manifest side:

```json
{
  "main": "./dist/extension.js",
  "browser": "./dist/web/extension.js"
}
```

`main` is used by the desktop host, `browser` by the web host. An extension may declare only one, or
both; declaring `browser` is what makes it installable in a browser-based VS Code.

### The constraints that shape the web bundle

- **No Node APIs.** `fs` and `child_process` do not exist in a Web Worker. Neither do the Node
  globals: `process`, `os`, `path`, `util`, `url`, `setImmediate`. Anything reachable from the web
  entry point must avoid them. Use workspace filesystem APIs instead of `fs`, and there is no
  substitute for spawning a process — that feature simply cannot be offered on web.
- **Single file, always.** `importScripts` and dynamic `import()` are unavailable, so code splitting
  is off the table. The web bundle must be exactly one output file.
- **`require()` is a shim** that resolves only `require('vscode')`. Any other runtime `require` that
  survives bundling throws.

The usual structure is a separate `src/web/extension.ts` entry that imports only web-safe modules,
with node-only code confined behind the desktop entry.

### How to check

Do not reason about it from the source. Check the built artifact:

```bash
# 1. Exactly one file must exist under the web output directory.
ls -R dist/web

# 2. Node built-ins must not be reachable in the bundle.
grep -nE "require\((['\"])(fs|path|os|child_process|util|url)\1\)" dist/web/extension.js

# 3. The only surviving require should be 'vscode'.
grep -oE "require\([^)]*\)" dist/web/extension.js | sort -u
```

Any hit in step 2 means a node-only module is reachable from the web entry — trace it back and gate
it. A cleaner check when available: run the extension under the web extension host test runner, which
fails on the actual missing global rather than on a text match.

---

## 4. tsconfig.json

```jsonc
{
  "compilerOptions": {
    "module": "Node16",
    "target": "ES2022",
    "lib": ["ES2022"],
    "moduleResolution": "Node16",
    "outDir": "out",
    "rootDir": "src",
    "sourceMap": true,
    "strict": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true
  },
  "exclude": ["node_modules", ".vscode-test"]
}
```

**Verify `module`/`target` against current documentation rather than assuming.** The extension host
runs VS Code's bundled Node, and that version moves with VS Code releases — the recommended pair
today is not necessarily the pair from an older tutorial or from a generated template. Targeting
higher than the host supports produces syntax the host cannot parse; targeting far lower just
produces worse output.

Field by field:

- **`lib`** should match `target` and must *not* include `"DOM"` for a node-targeted extension. DOM
  types let you write `document.querySelector` and compile cleanly for code that will crash in the
  extension host. Webview scripts are a separate compilation unit and can have DOM libs of their own.
- **`outDir` / `rootDir`** — with a bundler, `outDir` is mostly for the type-check and test builds;
  the shipped artifact comes from `dist/` via esbuild. Keeping `rootDir: "src"` preserves the
  directory shape in `out/`, which matters for the test runner locating compiled test files.
- **`sourceMap: true`** — needed so breakpoints map back to TypeScript. The bundler also emits its
  own sourcemap; both paths matter depending on whether you debug the bundle or the tsc output.
- **`strict: true`** — the VS Code API returns optional values constantly (`activeTextEditor`,
  `workspaceFolders`, provider results). Strict mode converts "user was in a state I didn't imagine"
  runtime crashes into compile errors.
- **`skipLibCheck: true`** is commonly set because it skips type-checking of `.d.ts` files in
  dependencies. Without it, one transitive dependency shipping types that conflict with another
  breaks your build for a reason you cannot fix. It does not weaken checking of your own code.

Type package pinning belongs here too: **`@types/vscode` must be at or below the `engines.vscode`
floor**, using caret ranges that match on both — e.g. `"engines": { "vscode": "^1.X.0" }` with
`"@types/vscode": "^1.X.0"`. Types ahead of the engine compile against APIs missing on the oldest
version you claim to support. Note also that `@types/vscode` lags the shipping VS Code version, so
"whatever VS Code I have installed" is the wrong number to write down — look up the current published
types version and set the floor to a version you actually intend to support.

---

## 5. .vscode/launch.json

```jsonc
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run Extension",
      "type": "extensionHost",
      "request": "launch",
      "args": ["--extensionDevelopmentPath=${workspaceFolder}"],
      "outFiles": ["${workspaceFolder}/dist/**/*.js"],
      "preLaunchTask": "${defaultBuildTask}"
    },
    {
      "name": "Extension Tests",
      "type": "extensionHost",
      "request": "launch",
      "args": [
        "--extensionDevelopmentPath=${workspaceFolder}",
        "--extensionTestsPath=${workspaceFolder}/out/test/suite/index"
      ],
      "outFiles": [
        "${workspaceFolder}/dist/**/*.js",
        "${workspaceFolder}/out/test/**/*.js"
      ],
      "preLaunchTask": "${defaultBuildTask}"
    }
  ]
}
```

- **`--extensionDevelopmentPath`** points the second VS Code window at this project so it loads the
  extension from source instead of from the marketplace.
- **`--extensionTestsPath`** points at the compiled test suite entry — note it is the `out/`
  (tsc) path, not the bundled `dist/` path. Tests are typically compiled with `tsc`, not bundled,
  because the test runner loads individual suite files.
- **`outFiles`** must point at whatever is actually loaded. If it points at `out/**/*.js` while the
  manifest's `main` loads `dist/extension.js`, the debugger will not find the sourcemap for the
  running code and breakpoints show as unverified (hollow circles) and never hit. When both bundled
  code and tsc-compiled tests are in play, list both paths.

### The stale-bundle failure

`preLaunchTask` is what builds before launching. Get it wrong and the failure is quiet and
genuinely confusing: **the debugger launches successfully and runs the previous build.** Your edit
is not there, breakpoints in new code never hit, and the obvious conclusion — "my code isn't being
reached" — is wrong.

Two ways to get it wrong:

1. **Missing entirely.** Nothing builds; you always debug whatever is on disk.
2. **Name mismatch.** The string must match a task `label` in `tasks.json` exactly. `${defaultBuildTask}`
   sidesteps this by resolving to the task marked `"group": { "kind": "build", "isDefault": true }`,
   which is why it is preferred over hardcoding a name that can drift.

If you suspect a stale bundle, check the modification time of `dist/extension.js` against your last
edit. That is a one-second answer to a question that otherwise costs an hour.

---

## 6. .vscode/tasks.json

```jsonc
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "watch",
      "dependsOn": ["npm: watch:tsc", "npm: watch:esbuild"],
      "presentation": { "reveal": "never" },
      "group": { "kind": "build", "isDefault": true }
    },
    {
      "type": "npm",
      "script": "watch:esbuild",
      "group": "build",
      "problemMatcher": "$esbuild-watch",
      "isBackground": true,
      "label": "npm: watch:esbuild",
      "presentation": { "group": "watch", "reveal": "never" }
    },
    {
      "type": "npm",
      "script": "watch:tsc",
      "group": "build",
      "problemMatcher": "$tsc-watch",
      "isBackground": true,
      "label": "npm: watch:tsc",
      "presentation": { "group": "watch", "reveal": "never" }
    }
  ]
}
```

The compound `watch` task is the default build task, so `${defaultBuildTask}` in launch.json resolves
to it, and it runs both the bundler watch and the type-check watch.

### Why the background problem matcher decides whether debugging works

A watch task never exits. VS Code therefore cannot use "process exited" as the signal that the build
is done — it has to read the task's **output**. The problem matcher's `background.beginsPattern` and
`endsPattern` are that contract: when output matches `beginsPattern`, VS Code considers a build
in progress; when it matches `endsPattern`, the build is considered finished and the debug session
is allowed to launch.

**If `endsPattern` never matches, F5 hangs indefinitely** with no error — VS Code is still waiting for
a build it believes is running. This is one of the most common "it just hangs before launching"
setups, and it is silent because nothing is technically wrong.

This is precisely what the `esbuildProblemMatcherPlugin` in section 1 exists for. esbuild produces no
such markers on its own; the plugin prints `[watch] build started` and `[watch] build finished`, and
`$esbuild-watch` matches those exact strings. **Removing the plugin while keeping
`problemMatcher: "$esbuild-watch"` breaks F5.** They are one mechanism in two files.

If you use a custom build script whose output does not match a built-in matcher, define the patterns
inline instead:

```jsonc
{
  "problemMatcher": {
    "owner": "custom",
    "fileLocation": ["relative", "${workspaceFolder}"],
    "pattern": {
      "regexp": "^(.*):(\\d+):(\\d+):\\s+(warning|error):\\s+(.*)$",
      "file": 1, "line": 2, "column": 3, "severity": 4, "message": 5
    },
    "background": {
      "activeOnStart": true,
      "beginsPattern": "^\\[watch\\] build started$",
      "endsPattern": "^\\[watch\\] build finished$"
    }
  }
}
```

Diagnosing a hang: open the task terminal (Terminal → Run Task, or the task output panel) and read
what the build actually printed. Compare it character by character against `endsPattern`. The mismatch
is usually a changed log string or an anchored regex that no longer matches.

---

## 7. .vscodeignore

`.vscodeignore` excludes from the shipped `.vsix`. It uses `.gitignore` syntax but inverted in
purpose — this is the package boundary, not source control.

### Exclusion-list style (simpler, matches the docs example)

```
.vscode/**
.vscode-test/**
node_modules/**
out/**
src/**
.gitignore
.yarnrc
esbuild.js
vsc-extension-quickstart.md
**/tsconfig.json
**/eslint.config.mjs
**/*.map
**/*.ts
```

The documented example for a bundled extension excludes `.vscode`, `node_modules`, `out/`, `src/`,
`tsconfig.json`, `webpack.config.js`, and `esbuild.js` — this is that list plus sourcemaps and stray
TypeScript.

### Exclude-everything-then-reinclude style (safer default)

```
# Exclude everything...
**

# ...then re-include only what ships.
!dist/**
!package.json
!README.md
!CHANGELOG.md
!LICENSE
!icon.png
!media/**
!syntaxes/**

# Re-includes can pull unwanted things back in; re-exclude them.
!dist/**/*.map
dist/**/*.map
```

This style fails closed: a new directory added later is excluded by default rather than silently
shipped. The exclusion-list style fails open, which is how credentials and internal notes end up in
published packages. Prefer this style unless the project already uses the other.

Be aware that negation is order-dependent and a re-included directory brings its whole subtree — the
trailing `dist/**/*.map` above exists because `!dist/**` would otherwise pull production sourcemaps
back in.

### What must ship

Bundled output (`dist/`), `package.json`, README, CHANGELOG, LICENSE, the icon, and every runtime
asset: webview HTML/CSS/JS, images, language grammars, snippets, themes. **Runtime assets are the
usual casualty** of the exclude-everything style — the extension installs fine and then a webview
opens blank, because the HTML it loads was never packaged.

### Verify by inspecting the built package, never by reading this file

A `.vscodeignore` cannot be validated by reading it. A trailing slash, an ordering issue between a
negation and a later pattern, or a re-included directory dragging in a subtree all change what
matches in ways that are not visible in the text. Build the package and list its contents:

```bash
npx @vscode/vsce ls          # what would be packaged, without building
npx @vscode/vsce package     # build the .vsix
unzip -l my-extension-0.0.1.vsix
```

Read the actual file list. Confirm every runtime asset is present and that `src/`, tests, `.env`,
and production sourcemaps are not. Do this every time the ignore file or the project layout changes —
this is the only check that answers the real question. The full packaging verification procedure
lives in `vscode-ext-release`.
