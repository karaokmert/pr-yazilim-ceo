# Restructuring an Existing Extension

Diagnosing structural problems in a project that already exists, and scoping fixes so they stay reviewable.

## Contents

- [The scoping principle](#the-scoping-principle)
- [Diagnosing](#diagnosing)
- [Activation on everything](#activation-on-everything)
- [No bundling](#no-bundling)
- [No disposal pattern](#no-disposal-pattern)
- [Stale engines and types](#stale-engines-and-types)
- [Manifest drift](#manifest-drift)
- [Everything in extension.ts](#everything-in-extensionts)
- [Sequencing multiple fixes](#sequencing-multiple-fixes)

## The scoping principle

A big-bang restructuring is unreviewable and dangerous, for one specific reason: it mixes structural change with behavior change. When something breaks afterward — and something will — nobody can tell which change caused it, so the fix is to revert everything, including the parts that were right.

So: **name one problem, propose one fix, change only that.** A project with four structural problems gets four changes, each independently verifiable and revertible.

There's a second reason, less obvious. Existing structure often encodes a constraint nobody wrote down — a weird build step exists because of a CI quirk, an odd activation event because of a customer's setup. Changing things one at a time surfaces those constraints as failures you can attribute. Changing everything at once surfaces them as a mystery.

**Ask before assuming a choice was a mistake.** "This uses webpack; is that deliberate?" costs one question and occasionally saves you from removing something load-bearing.

## Diagnosing

A quick pass that finds most structural problems:

```bash
# Activation strategy
jq '.activationEvents, .engines, .main, .browser' package.json

# Is there a build step at all?
jq '.scripts' package.json

# Does the manifest point at source rather than build output?
jq -r '.main' package.json     # "./src/extension.js" or "./out/..." unbundled is a smell

# Package boundary
cat .vscodeignore 2>/dev/null || echo "NO .vscodeignore"

# What would actually ship
npx @vscode/vsce ls | head -50

# Disposal discipline: compare registrations to subscriptions
grep -rn "vscode\.\(commands\|languages\|window\|workspace\)\.register\|createStatusBarItem\|createFileSystemWatcher\|onDid" src/ | wc -l
grep -rn "context\.subscriptions\.push" src/ | wc -l

# Secrets in the wrong place
grep -rn "globalState\.update\|workspaceState\.update" src/

# Size of the entry point
wc -l src/extension.ts
```

The two `grep | wc -l` counts are a heuristic, not proof — one `push` can take several disposables. A large gap is worth investigating; a small one isn't necessarily a problem.

## Activation on everything

**Symptom:** `"activationEvents": ["*"]`, or a long list of `onCommand:` entries duplicating `contributes.commands` on a modern engine.

**Cost:** the extension activates during startup in every window. `vsce package` also refuses to build with `*` unless given `--allow-star-activation`.

**Fix:** determine what actually needs to be ready.

- Everything reachable through commands, views, or languages → **delete the events entirely.** On VS Code 1.74+ they're auto-generated (see the manifest skill).
- Background work with no natural trigger → `onStartupFinished`.
- Only relevant to certain projects → `workspaceContains:<glob>`.

**Verify:** `Developer: Show Running Extensions` before and after — the extension should no longer appear in the startup activation list, and should appear once you invoke it.

This is usually the highest-value structural fix available, and often the smallest diff.

## No bundling

**Symptom:** no `esbuild`/`webpack` in scripts, `main` pointing at `out/extension.js`, hundreds of files in `vsce ls`.

**Cost:** a large `.vsix`, slow installs, and slower activation — every `require` is a file read.

**Fix:** add a bundler (config in `build-setup.md`), point `main` at the bundled output, update `.vscodeignore`, and add the watch task the debugger needs.

**Verify:** `vsce ls` should now show a handful of files. Then package, install the `.vsix`, and confirm the extension still activates — bundling breaks dynamic `require`s and any runtime asset path that assumed the old layout, and neither shows up at build time.

Watch for: assets loaded by relative path (webview HTML, grammars) that must be explicitly kept in `.vscodeignore` and referenced via `context.extensionUri` rather than `__dirname`.

## No disposal pattern

**Symptom:** `registerCommand` and event listener results assigned to variables or ignored, few `context.subscriptions.push` calls.

**Cost:** leaked listeners and duplicate registrations across activation cycles. It rarely breaks visibly in development — it degrades the editor over a long session, which is exactly why it survives so long.

**Fix:** push every disposable into `context.subscriptions`. For resources with a shorter life (webview panels, per-session watchers), use a scoped disposable array disposed at the right moment.

This one is safe to do incrementally — each registration is independent, so it can land alongside other work rather than as a big sweep. Establishing it in the entry point matters most, since new code is written by imitation.

## Stale engines and types

**Symptom:** `engines.vscode` several years old, or `@types/vscode` newer than `engines.vscode`.

**Cost:** a too-low floor blocks APIs you could use and forces manual activation events; types ahead of the engine compile against APIs that don't exist on the version you claim to support, which fails at runtime on a user's machine. `vsce` checks this pairing.

**Fix:** decide the genuine minimum supported version, set both to that with matching caret ranges. Raising the floor **is a breaking change** for users on older VS Code — it belongs in a major version bump and the changelog.

Note that `@types/vscode` lags the shipping VS Code release, so don't derive the floor from the product version.

## Manifest drift

**Symptom:** commands in `contributes` with no handler, registered commands missing from the manifest, settings read via `getConfiguration()` with no schema.

**Cost:** palette entries that throw when clicked, commands that don't appear, settings invisible in the UI with no validation.

**Fix:** reconcile in both directions.

```bash
# Declared commands
jq -r '.contributes.commands[]?.command' package.json | sort > /tmp/declared.txt
# Registered commands
grep -rhoE "registerCommand\(\s*['\"]([^'\"]+)" src/ | sed -E "s/.*['\"]//" | sort > /tmp/registered.txt
comm -3 /tmp/declared.txt /tmp/registered.txt

# Settings read in code vs declared
grep -rhoE "get(<[^>]+>)?\(\s*['\"]([^'\"]+)" src/ | sed -E "s/.*['\"]//" | sort -u
jq -r '.contributes.configuration.properties | keys[]' package.json 2>/dev/null | sort
```

Each orphan is a decision: delete the dead declaration, or add the missing half. Both are small.

## Everything in extension.ts

**Symptom:** an `extension.ts` of many hundreds of lines holding activation, command handlers, providers, and business logic.

**Cost:** nothing is testable without the extension host, and everything conflicts in review.

**Fix, incrementally rather than as one sweep:** extract feature modules that export a `register(context)` function, and pull pure logic into modules with **no `vscode` import** — those become unit-testable without the harness, which is the real prize.

Do this as features are touched, not as a standalone refactor. A pure-motion commit that moves a thousand lines is very hard to review and is exactly where a subtle behavior change hides.

## Sequencing multiple fixes

When several problems coexist, order matters — later fixes are verified by earlier ones:

1. **Manifest and activation** — smallest diff, biggest immediate win, no code change.
2. **Bundling** — changes what ships; verify by installing the built `.vsix`.
3. **`.vscodeignore` and package inspection** — confirms step 2 actually did what you think.
4. **Disposal discipline** — incremental, safe to spread across later work.
5. **Module extraction** — largest and riskiest; do it last, feature by feature.

Land them separately. If step 2 breaks something, you want to know it was step 2.
