# VS Code Extension Team — Skill Set

Six skills for the three agents in `../agents/`. Two are shared by everyone, four are domain canon split by ownership.

## The map

| Skill | Kind | architect | developer | qa-publisher |
|---|---|:--:|:--:|:--:|
| `vscode-ext-behavior` | shared standard | yes | yes | yes |
| `vscode-ext-workflow` | shared workflow | yes | yes | yes |
| `vscode-ext-manifest` | domain (cross-cutting) | yes | yes | yes |
| `vscode-ext-scaffolding` | domain | **owner** | — | — |
| `vscode-ext-api-patterns` | domain | — | **owner** | — |
| `vscode-ext-release` | domain | — | — | **owner** |

Each agent loads three: the two shared ones, plus its own domain skill. All three additionally reach for `vscode-ext-manifest`, because `package.json` is the one file every role writes to.

## Why this split

**`behavior` and `workflow` are separate** rather than one "how we work" skill. They answer different questions and get consulted at different moments: `behavior` is *how do I judge this?* and applies continuously; `workflow` is *whose is this and where does it go next?* and applies at boundaries. Merging them would mean loading routing rules during focused implementation work, and calibration rules during a handoff.

**`manifest` is its own skill rather than living in `scaffolding`.** The manifest is genuinely shared territory — the architect designs it, the developer adds `contributes` entries beside each feature, qa-publisher validates it before packaging. Filing it under the architect would leave the other two guessing at a file they both edit, and duplicating it into three places would guarantee drift.

**The domain skills split by role, not by topic**, because that matches how work arrives. An agent asked to build a tree view needs the whole API surface, not a slice of "views" that stops where packaging begins.

**Detail lives in `references/`.** Each SKILL.md carries the decision rules and stays readable; the schemas, configs, and worked code sit in reference files loaded only when needed.

## Skills at a glance

**`vscode-ext-behavior`** — the rigor dial (internal vs. published) that calibrates every decision, why this API punishes confident memory, ownership rules that cross role boundaries (disposal, secrets, absence handling), and how to report work.

**`vscode-ext-workflow`** — routing (does this change the shape, fill the shape, or ship the shape?), what each handoff must carry, the fixed release chain, and the two decisions that always go to the human.

**`vscode-ext-manifest`** — activation events and their auto-generation, contribution points, `engines`/`@types` pinning, `capabilities` for trust and virtual workspaces, `main` vs `browser`, marketplace metadata. Plus a review checklist.

**`vscode-ext-scaffolding`** — project layout, bundling, tsconfig, `.vscodeignore`, debug setup, the lifecycle skeleton, monorepo decisions, and how to scope fixes to an existing project without a big-bang rewrite.

**`vscode-ext-api-patterns`** — commands, providers, tree views, webviews, workspace and file system, configuration and state, progress and cancellation, external processes. Includes a debugging checklist for the five most common silent failures.

**`vscode-ext-release`** — the test harness, the security review, versioning, packaging and `.vsix` inspection, marketplace and Open VSX publishing, internal distribution, and when to stop a release.

## Currency

Technical content was verified against official sources and live CLI output rather than written from memory. Facts with a shelf life:

- **Azure DevOps PAT retirement (announced 2026-12-01)** — `vsce login` / `VSCE_PAT` is a sunsetting path; `--azure-credential` and `--oidc` replace it. This is the most time-sensitive item in the set.
- **Activation event auto-generation** (VS Code 1.74+, `onTaskType` 1.76+) — modern manifests often need no `activationEvents` at all.
- **`@vscode/test-cli` + `@vscode/test-electron`** are the current test harness; unscoped `vscode-test` is deprecated.
- **The Marketplace signs extensions**; publishers don't manage keys.
- **Chat participants, language model tools, and MCP server providers are stable API** (finalized 1.90).

Version-specific claims are marked as needing verification where they were not confirmable. When something here disagrees with `vsce --help` or `code --help`, trust the binary.
