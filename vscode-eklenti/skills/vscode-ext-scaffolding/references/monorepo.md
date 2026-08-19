# Multiple Extensions and Shared Code

For a team shipping several extensions — some internal, some published. The decision is not "monorepo or not" in the abstract; it's about how much genuinely shared logic exists and what the coordination cost is.

## Contents

- [Choosing a structure](#choosing-a-structure)
- [Separate repos](#separate-repos)
- [Workspace monorepo](#workspace-monorepo)
- [Private npm package](#private-npm-package)
- [Rules that hold regardless](#rules-that-hold-regardless)
- [Migrating later](#migrating-later)

## Choosing a structure

Be honest about how much is actually shared. Teams routinely reach for a monorepo to share a few hundred lines of utilities and then pay build complexity forever.

| Situation | Structure |
|---|---|
| Two extensions, a few shared helpers | Separate repos, deliberate duplication |
| Several extensions, substantial shared domain logic | Workspace monorepo |
| Sharing crosses teams or repos you don't control | Private npm package |
| Extensions are released on independent schedules by different people | Separate repos or npm package |

The question that usually settles it: **when the shared code changes, must all consumers update together?** If yes, a monorepo makes that atomic and is worth its cost. If consumers can adopt at their own pace, a versioned package models reality better and a monorepo will fight you.

## Separate repos

The default, and correct more often than teams expect.

Duplicating a `formatBytes` helper across two extensions costs a few lines. Sharing it costs a workspace tool, a build graph, resolution config in two bundlers, and a `.vscodeignore` that has to understand the layout. At small scale duplication is genuinely cheaper — and it lets the two copies diverge when the extensions' needs diverge, which they usually do.

Reconsider when the same non-trivial logic has been copied a third time, or when a bug gets fixed in one copy and not the other. That second symptom is the real signal.

## Workspace monorepo

```
extensions-monorepo/
├── package.json              # workspaces config, shared devDependencies
├── tsconfig.base.json        # shared compiler options
├── packages/
│   └── shared/
│       ├── package.json      # name: "@company/ext-shared"
│       ├── src/index.ts
│       └── tsconfig.json
└── extensions/
    ├── linter/
    │   ├── package.json      # the extension manifest
    │   ├── .vscodeignore
    │   ├── esbuild.js
    │   └── src/extension.ts
    └── snippets/
        └── ...
```

```jsonc
// root package.json
{
  "private": true,
  "workspaces": ["packages/*", "extensions/*"],
  "devDependencies": { "typescript": "^5.x", "esbuild": "^0.x" }
}
```

```jsonc
// extensions/linter/package.json — the extension manifest
{
  "name": "company-linter",
  "publisher": "company",
  "version": "0.3.1",
  "main": "./dist/extension.js",
  "dependencies": { "@company/ext-shared": "workspace:*" }
}
```

### The parts that bite

**Bundling absorbs the shared package.** Because esbuild follows the import and inlines the source, `dist/extension.js` contains the shared code and the `.vsix` never needs the workspace layout. This is what makes monorepos workable for extensions at all — but it means **each extension must bundle**, since an unbundled one would ship a `node_modules` symlink pointing outside the package.

**`.vscodeignore` is per-extension**, relative to that extension's directory. Verify each one by inspecting its built `.vsix`; a layout that works for one extension can silently include the whole workspace for another.

**Hoisting changes paths.** Workspace tools hoist dependencies to the root `node_modules`, so anything resolving paths relative to `__dirname` may not find what it expects. Prefer `context.extensionUri` for runtime asset paths — it's correct regardless of layout.

**TypeScript needs to resolve the shared package.** Either project references with `composite: true`, or path mapping in `tsconfig.base.json`. Path mapping is simpler; project references give better incremental builds. Either way, make sure the bundler and `tsc` agree on resolution, or you get code that type-checks and fails to bundle.

**Version and release each extension independently.** Each has its own `version` and its own `.vsix`. A shared version number across unrelated extensions forces meaningless releases and confuses users about what changed.

## Private npm package

Publish the shared code to a private registry and depend on it by version.

Right when sharing crosses repository or team boundaries, or when consumers need to adopt changes on their own schedule. The cost is a publish step between changing shared code and using it, which is friction during active development — and the reason teams often start here and regret it while the shared code is still churning.

A reasonable middle path: keep shared code in a monorepo while it's unstable, extract it to a package once it settles.

## Rules that hold regardless

- **Each extension keeps its own manifest, version, changelog, and `.vsix`.** Extensions are independently installed and updated by users; they cannot share a release.
- **Shared code must not import `vscode`** unless every consumer is an extension and you accept the coupling. Pure logic with no `vscode` import is testable without the extension host — much faster, and it's the code most worth sharing anyway.
- **`engines.vscode` is per-extension.** Shared code must work against the *lowest* floor among consumers, which is easy to forget when adding an API call.
- **Each extension gets its own `.vsix` inspection.** Never assume that because one packaged correctly, its sibling did.

## Migrating later

Moving from separate repos to a monorepo is mechanical: move directories, add the workspace config, extract the shared package, fix imports. Preserving git history takes effort (subtree merges) but the code motion is straightforward.

Going the other direction — splitting a monorepo — is harder, because implicit coupling accumulates: shared config, shared build assumptions, cross-imports nobody noticed.

**So when the choice is genuinely close, start separate.** The cheaper migration is the one you're more likely to need.
