---
name: vscode-ext-release
description: Canon for testing, packaging, and shipping VS Code extensions — the @vscode/test-cli integration test harness, building and inspecting the .vsix with @vscode/vsce, semantic versioning and changelogs, the pre-release security and permissions review, marketplace publishing (and Open VSX), and internal .vsix distribution. Load this whenever an extension is being tested, packaged, versioned, security-reviewed, or released — when setting up the test harness, building a .vsix, preparing a marketplace listing, reviewing how secrets or telemetry are handled before shipping, or distributing an internal build to the team.
---

# Testing, Packaging, and Release

This is the qa-publisher's canon: everything between "it works in the Extension Development Host" and "people have a working, versioned, trustworthy artifact."

Two framing points that shape all of it:

**Releasing is irreversible in practice.** You can unpublish a marketplace extension, but you cannot remove it from machines that already installed it. This is why the release chain stops on failure rather than noting problems and proceeding.

**You do not fix what you find.** Defects go back to the developer with precise repro information. An agent that fixes what it finds stops looking for what else is broken — and the independence of the check is the whole value of the role. Handoff format is in `vscode-ext-workflow`.

## The release chain

The chain itself — the fixed five steps, and the rule that each step's failure stops the chain rather than being noted and passed along — is canon in `vscode-ext-workflow`. This skill supplies the execution detail for each step; read the chain definition there first if you haven't.

The sections below (numbered 1–5) map directly onto that chain, in order.

## 1. Testing

Extension tests run **inside a real, downloaded VS Code instance**, not against a mocked API. This is the defining property of the harness and the reason it's worth the setup: a mocked `vscode` namespace tests your assumptions about the API rather than the API, and it hides exactly the breakage you most need to catch — a contribution point that doesn't register, an activation event that never fires.

The current setup is **two packages together**, not one:

```bash
npm install --save-dev @vscode/test-cli @vscode/test-electron
```

`@vscode/test-cli` is the runner and config layer (`.vscode-test.js` / `.mjs` / `.json`); `@vscode/test-electron` is the layer that downloads and launches real VS Code. Older projects may drive `@vscode/test-electron` directly with a hand-written runner — that still works and isn't worth rewriting mid-release.

The unscoped **`vscode-test` package is deprecated** (renamed to `@vscode/test-electron`). If you find it, that's a modernization note for the developer, not something to fix during a release pass.

Web extensions test through a third package, `@vscode/test-web`, which runs the extension in a browser — a genuinely different environment, so desktop test passes say nothing about web behavior.

Setup and config specifics are in `references/testing.md`.

**What's worth testing**, in priority order — extension tests are slow, so spend them where they catch real breakage:

- **Activation** — the extension activates on its declared trigger. Catches the most damaging class of failure, where nothing works at all.
- **Commands execute** — invoke via `vscode.commands.executeCommand` and assert the effect. This also proves the manifest entry and the registration agree.
- **Providers return correct results** — open a real fixture document, call the provider, assert on what comes back.
- **Configuration is honored** — change a setting, assert behavior changes.

Use `sinon` or similar only for genuine externals — network calls, child processes, clocks. Mocking the `vscode` namespace itself defeats the point of the harness.

Async timing is the usual source of flaky extension tests: activation, provider registration, and language-server readiness are not instantaneous. Wait for a real condition rather than sleeping a fixed duration.

## 2. Security and permissions review

**A distinct, deliberate pass — not a side effect of testing.** It applies identically to internal and published extensions (see the rigor dial in `vscode-ext-behavior`); an internal tool often holds credentials to more sensitive infrastructure than a public one.

The ownership rule behind the first check below — secrets belong only in `context.secrets`, never `globalState`/`workspaceState`/settings/hardcoded — is canon in `vscode-ext-behavior`. This section is the release-time verification pass against that rule, not a restatement of why it's true.

Four checks:

**Secrets.** Grep the source for anything in `globalState`, `workspaceState`, `contributes.configuration`, or hardcoded. **Finding a secret in the wrong place blocks the release** — it goes back to the developer, it does not get noted for later.

**What leaves the machine.** Identify every network call and any telemetry. For a published extension, undisclosed data collection violates marketplace policy; disclose it in the README and respect the user's global telemetry setting. For internal, the team still deserves to know.

**Capability declarations.** `capabilities.untrustedWorkspaces` and `capabilities.virtualWorkspaces` must match what the code actually does — verified against the code, not left at defaults. An extension that executes a workspace-specified binary is not safe in an untrusted workspace regardless of what the manifest claims. Shapes are in `vscode-ext-manifest`.

**Dependencies.** Run `npm audit` (or equivalent) before the release build. Bundled dependencies ship inside the `.vsix`; a vulnerable transitive dependency is now your extension's vulnerability.

## 3. Versioning and changelog

Same unit of work as packaging. Shipping a `.vsix` whose version didn't move breaks update mechanics for everyone who already has it installed — VS Code has no reason to offer an update.

Semver, scoped to what users experience:

- **Patch** — bug fixes, no interface change.
- **Minor** — new backward-compatible features, new commands or settings.
- **Major** — breaking changes: removed or renamed commands, removed settings, changed default behavior, raised `engines.vscode` minimum.

Renaming a command *is* breaking, even though it feels internal — user keybindings and tasks reference command IDs by string.

Marketplace convention treats odd minor versions as pre-release; if the team uses `--pre-release`, keep the numbering scheme consistent with it.

`CHANGELOG.md` gets real entries describing user-visible change. "Bug fixes and improvements" tells a user deciding whether to update precisely nothing.

## 4. Packaging and inspection

`@vscode/vsce` builds the `.vsix`. A `.vsix` is a zip — which is what makes the inspection step possible and mandatory.

**A clean `vsce package` exit code is not evidence of correct contents.** `.vscodeignore` mistakes do not produce errors; they produce a package that is missing an asset or containing something that should never have left the building. Extract the package and read the file list. Every release, not just the first.

What you are looking for:

- **Must not be there**: `src/`, tests and fixtures, `.env` or credential files, `.git`, dev `node_modules`, internal notes.
- **Must be there**: the bundled entry point that `main`/`browser` points at, `package.json`, README, CHANGELOG, LICENSE, icon, and every runtime asset (webview HTML/CSS, images, grammars).
- **Size sanity**: a bundled extension is typically well under a megabyte. Tens of megabytes almost always means `node_modules` got included.

The commands for packaging, extracting, and listing contents are in `references/packaging.md`.

**Test the packaged artifact, not just the source.** Install the built `.vsix` into a clean VS Code instance and confirm the extension activates and its main command runs. This catches the failure that all source-level testing structurally cannot: a correct extension whose package is missing a file. It's the single highest-value check in this skill.

## 5. Distribution

### Published — marketplace

Confirm before publishing, because the marketplace review or your users will otherwise find these for you:

- `publisher` matches the real publisher ID, and authentication works (see below).
- `README.md` is written as a **listing page** — what it does, why someone wants it, and a screenshot or GIF. This is the entire basis on which a stranger decides to install.
- `LICENSE` present, `icon` set (**PNG ≥128×128 — SVG is rejected**), `categories` and `keywords` populated, `repository` pointing at real source.
- Version is plain `major.minor.patch` — no `-beta` suffix; use `--pre-release` for pre-releases.
- Version and changelog updated.

**Authentication is changing, and the old path is sunsetting.** Publishing has historically used an Azure DevOps Personal Access Token (`vsce login`, or `VSCE_PAT` in the environment). **Global PATs in Azure DevOps are being retired — the announced date is 2026-12-01.** The replacement is Microsoft Entra ID: `vsce publish --azure-credential`, or `vsce publish --oidc` for publishing from GitHub Actions with no stored token at all.

Prefer the Entra ID path for anything set up now. If you find an existing PAT-based pipeline, flag it as work that has a deadline rather than leaving it to break silently.

**Signing is not your job — the Marketplace signs every extension at publish time**, and VS Code verifies that signature on install. You don't generate or manage signing keys. What this does mean: a tampered or corrupted package fails verification on the user's machine with errors like `SignatureIsInvalid` or `NotSigned`, so if users report install failures, the package integrity is worth checking before anything else. `vsce generate-manifest` and `vsce verify-signature` exist if you need to verify locally.

**Publishing is a human decision.** Present the readiness state and let the human trigger it — this is the irreversibility point.

If the extension also targets VSCodium and other compatible editors, **Open VSX is a separate registry with a separate publish step** using the `ovsx` CLI. Publishing to one does not publish to the other. Handle both explicitly or state that only one was done.

Open VSX is run by the Eclipse Foundation, so `code.visualstudio.com` documents none of it — don't look there for `ovsx` answers, and don't assume marketplace rules transfer. It uses namespaces (`ovsx create-namespace`) rather than publishers.

Post-publish, confirm the listing renders correctly — a broken README image is visible to everyone who looks at it.

### Internal

Lighter and correctly so: build the `.vsix`, put it where the team can reach it (share, CI artifact, internal gallery), and give install instructions:

```
code --install-extension /path/to/extension-0.1.0.vsix
```

Users can also install via **Extensions: Install from VSIX** in the Command Palette.

**An extension installed from a VSIX has auto-update disabled by default.** This is the fact that most often bites internal distribution: colleagues stay on whatever build they first installed, indefinitely, and will report bugs you fixed months ago. Plan for it — announce updates explicitly, and make the version visible in any output the extension produces so a bug report identifies its build.

Skip the marketplace listing polish — it's wasted effort for a non-public artifact. **Do not skip the security review, versioning, or package inspection.** Those are engineering integrity, not presentation.

## Reporting a release pass

Cover these five, in this order:

1. **Tests** — what ran, pass/fail, bugs found (with repro, handed back unfixed).
2. **Package inspection** — actual contents summary, anything unexpected flagged.
3. **Security review** — the four checks, each with its result.
4. **Version and changelog** — new version and the semver reasoning.
5. **Distribution** — marketplace URL, or artifact location and install command.

State known gaps plainly. "No test coverage for the tree view; the command path is covered" is useful. Silence reads as coverage that doesn't exist.

## When to stop the release

Stop, report, and do not package or publish when:

- A test fails, or a bug is found that affects a shipping code path.
- A secret is found anywhere other than `context.secrets`.
- Package inspection shows something that must not ship.
- Capability declarations don't match actual behavior.
- Distribution intent is ambiguous and the artifact isn't ready for the more demanding of the two.

**Stopping is a normal outcome.** A delayed release costs a day; a known-broken published release costs a bad review, a support load, and an emergency patch — for users who already installed it.

## References

- `references/testing.md` — harness setup, config, test patterns, async timing.
- `references/packaging.md` — vsce commands, .vsix inspection, publishing mechanics.
- `references/security-review.md` — the review checklist in detail.
