# Pre-Release Security and Permissions Review

The deliberate checklist pass before any release, internal or public. Run it as its own step — folding it into testing is how it gets skipped, because a passing test suite feels like completion.

**This applies at full strength to internal extensions.** Internal developer tooling frequently holds credentials to production infrastructure, source control, and internal APIs. The audience is smaller; the blast radius often is not.

## Contents

- [1. Secrets and credentials](#1-secrets-and-credentials)
- [2. Data leaving the machine](#2-data-leaving-the-machine)
- [3. Capability declarations](#3-capability-declarations)
- [4. Dependencies](#4-dependencies)
- [5. Untrusted input](#5-untrusted-input)
- [Reporting](#reporting)

## 1. Secrets and credentials

**Rule: credentials live in `context.secrets`, nowhere else.**

`context.secrets` is async and backed by the OS keychain. The alternatives all fail:

- `globalState` / `workspaceState` — plaintext JSON on disk.
- `contributes.configuration` (settings) — plaintext, synced across machines by Settings Sync, and routinely pasted into bug reports and screen shares.
- Source constants — shipped inside the `.vsix`, which anyone can unzip.
- `.env` shipped in the package — same problem, plus it looks deliberate.

Search for the pattern, not just the obvious names:

```bash
# Storage APIs that should never hold credentials
grep -rn "globalState\.update\|workspaceState\.update" src/

# Likely credential names near assignment
grep -rniE "(token|secret|apikey|api_key|password|credential|bearer)\s*[:=]" src/

# Settings reads that sound credential-shaped
grep -rn "getConfiguration" src/ | grep -iE "token|key|secret|password"

# Credential-ish files that might ship
find . -name ".env*" -not -path "./node_modules/*"
```

Then confirm none of it made it into the package:

```bash
mkdir -p /tmp/sec && unzip -q *.vsix -d /tmp/sec
grep -rniE "(api[_-]?key|secret|password|bearer )" /tmp/sec/extension/ | grep -v node_modules
```

**A secret in the wrong place blocks the release.** It goes back to the developer. It does not get noted as a follow-up, because "we'll move it next sprint" ships the credential.

One nuance worth checking: a token correctly stored in `context.secrets` but then *logged* — to an OutputChannel, to `console.log`, or into an error message — is just as exposed. Grep the logging paths too.

## 2. Data leaving the machine

Enumerate every outbound call: `fetch`, `https.request`, `axios`, any SDK, and any spawned process that reaches the network.

For each, answer three questions:

1. **What is sent?** Specifically — file contents, file paths, workspace names, and identifiers are all more sensitive than teams assume. Source code leaving the machine is a serious disclosure for many organizations.
2. **Where does it go?** A first-party endpoint is a different conversation from a third-party analytics service.
3. **Does the user know?**

**Telemetry** has hard rules for published extensions: disclose it in the README, and respect the user's global setting. VS Code exposes `vscode.env.isTelemetryEnabled` and `onDidChangeTelemetryEnabled`; use `@vscode/extension-telemetry` rather than rolling your own, since it honors the global setting for you. Sending telemetry when the user has disabled it violates marketplace policy and, more importantly, breaks a promise the editor made on your behalf.

For internal extensions, disclosure is still owed to colleagues — they just get it in a README rather than a listing page.

## 3. Capability declarations

Both flags in `capabilities` must reflect what the code actually does. Verify against the code; don't accept the manifest's word.

**`untrustedWorkspaces`** — the question is: *if someone opens a malicious repository with this extension installed but the workspace untrusted, can that repository cause code to run?*

It is **not** safe (`supported: false` or `"limited"`) if the extension:

- Executes a binary whose path comes from workspace settings or a workspace file.
- Runs scripts from the workspace (`package.json` scripts, task definitions, hooks).
- Loads and evaluates workspace-provided config as code.
- Passes workspace content to something that interprets it.

If it's `"limited"`, list the dangerous settings in `restrictedConfigurations` so their workspace values are ignored until trust is granted. Any setting naming an executable belongs there, and should also be `scope: "machine"`.

**`virtualWorkspaces`** — *does this work when files aren't on disk?* It does not if the extension uses Node `fs` on workspace paths, spawns processes against workspace files, or assumes `uri.fsPath` is real. **This defaults to `true` when unspecified**, so an extension that needs real files must declare `false` deliberately or it will be offered in a context where it silently fails.

## 4. Dependencies

```bash
npm audit
npm audit --production        # what actually ships
npm ls --all --depth=0
```

Bundled dependencies ship inside the `.vsix` — a vulnerable transitive dependency becomes your extension's vulnerability, distributed by you.

Judgment applies: a prototype-pollution advisory in a dev-only build tool is not a release blocker; anything reachable at runtime in a published extension is. What matters is that the audit was **run and read**, and that anything not fixed was a decision rather than an oversight.

Also worth a look: dependencies added since the last release. A new transitive dependency tree is a good moment to ask whether the functionality justified it.

## 5. Untrusted input

The workspace is attacker-controlled in the threat model — anyone can send a colleague a repository.

- **Never build shell commands by concatenation.** Pass arguments as an array; a filename containing `;` or `$()` is a valid filename and a command injection.
- **Validate webview messages.** The webview is a separate trust context; a message handler that trusts its payload and does file or process work is an escalation path. Check the message shape before acting on it.
- **Never inject workspace or user content into webview HTML unescaped.** Send it via `postMessage` and set it as text, or escape it.
- **Path traversal**: a workspace-relative path containing `../` can reach outside the workspace. Resolve and verify containment before reading or writing.
- **Resource limits**: a hostile or merely enormous file shouldn't hang the extension host. Bound file sizes and set process timeouts.

## Reporting

Report each of the five as an explicit line with its result, not as a summary sentence. "Security review passed" hides which checks actually ran.

```
Secrets:       PASS — token in context.secrets; no credential in state/settings; not logged
Data egress:   PASS — one call to internal-api.example.com (file path + line only); disclosed in README
Capabilities:  FAIL — untrustedWorkspaces not declared; extension runs myExt.linterPath from
                      workspace settings. Needs supported:"limited" + restrictedConfigurations,
                      and the setting should be scope:"machine". BLOCKS RELEASE.
Dependencies:  PASS — npm audit: 2 moderate, both dev-only (build tooling), not shipped
Untrusted in.: PASS — spawn() with argument array; webview messages validated by discriminant
```

A `FAIL` on secrets or capabilities stops the release and goes back to the developer. Everything else is a judgment call to be surfaced, with your recommendation, for the human to decide.
