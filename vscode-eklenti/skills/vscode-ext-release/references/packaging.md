# Packaging and Publishing

Mechanics of `@vscode/vsce` and `ovsx`. Decision rules and the release chain are in the parent SKILL.md.

**Prefer the binary over the docs for CLI facts.** `vsce --help` and `vsce package --help` report more flags than the documentation page, and they describe the version you actually have installed. When something here disagrees with what the binary says, the binary wins — re-run it.

## Contents

- [Installing](#installing)
- [Packaging](#packaging)
- [Inspecting the .vsix](#inspecting-the-vsix)
- [Authentication (changing — read this)](#authentication-changing--read-this)
- [Publishing to the Marketplace](#publishing-to-the-marketplace)
- [Pre-release versions](#pre-release-versions)
- [Platform-specific packages](#platform-specific-packages)
- [Signing and verification](#signing-and-verification)
- [Open VSX](#open-vsx)
- [Internal distribution](#internal-distribution)

## Installing

```bash
npm install --save-dev @vscode/vsce
# or invoke without installing:
npx @vscode/vsce package
```

`vsce` requires a modern Node — its README and package metadata have disagreed on the exact floor (22.x vs >=20), so if you hit an engine error, trust the error over either document. Supported package managers are npm and yarn 1.x.

## Packaging

```bash
vsce package
vsce package --out dist/my-extension.vsix
vsce package --pre-release
```

Flags worth knowing:

| Flag | Use |
|---|---|
| `--out <path>` | Output location |
| `--pre-release` | Mark as a pre-release version |
| `--no-dependencies` | Skip bundling `node_modules` — for already-bundled extensions |
| `--target <target>` | Platform-specific build |
| `--allow-star-activation` | Required if `activationEvents` contains `*` |
| `--allow-missing-repository` | Required if `repository` is absent |
| `--skip-license` | Required if no LICENSE file |
| `--ignoreFile <path>` | Use an alternative to `.vscodeignore` |
| `--readme-path`, `--changelog-path` | Non-default doc locations |

**On `--no-dependencies`:** when the extension is bundled (esbuild/webpack) the entire runtime lives in `dist/`, and `node_modules` should be excluded via `.vscodeignore` anyway. Passing `--no-dependencies` makes that explicit and speeds packaging. This pairing is common practice rather than a documented rule — the authoritative check is inspecting the resulting package, not the flag.

**Treat the `--allow-*` flags as questions, not fixes.** Each one suppresses a guard that exists for a reason. Reaching for `--allow-star-activation` means the activation strategy deserves another look; `--allow-missing-repository` and `--skip-license` are defensible for internal extensions and are gaps for published ones.

## Inspecting the .vsix

**Mandatory every release.** A clean exit code says nothing about contents.

```bash
# What would be included, without building
vsce ls

# Inspect a built package (a .vsix is a zip)
unzip -l my-extension-0.1.0.vsix

# Extract and look around
mkdir -p /tmp/vsix-check && unzip -q my-extension-0.1.0.vsix -d /tmp/vsix-check
find /tmp/vsix-check -type f | sort

# Size check
du -h my-extension-0.1.0.vsix
```

Checklist against the listing:

- **Absent:** `src/`, `**/*.ts` (except declarations you intend to ship), tests, fixtures, `.env`, `.git`, dev `node_modules`, build configs, internal notes.
- **Present:** the file `main`/`browser` points at, `package.json`, `README.md`, `CHANGELOG.md`, `LICENSE`, the icon, and every runtime asset — webview HTML/CSS/JS, images, grammars, language configuration.
- **Size:** a bundled extension is usually well under 1 MB. Tens of megabytes means `node_modules` got in.

The highest-value check is the runtime assets. Missing code usually fails immediately and obviously; a missing webview stylesheet or grammar file produces an extension that loads fine and is subtly broken for every user.

**Then install the package and run it:**

```bash
code --install-extension my-extension-0.1.0.vsix --force
```

Confirm it activates and its main command works. This is the only check that catches a correct codebase with a broken package.

## Authentication (changing — read this)

Historically publishing used an Azure DevOps Personal Access Token:

```bash
vsce login <publisher>
# or
VSCE_PAT=<token> vsce publish
```

**Global PATs in Azure DevOps are being retired, with an announced date of 2026-12-01.** Anything built on `vsce login` / `VSCE_PAT` has a deadline.

The replacement is Microsoft Entra ID:

```bash
# Interactive / service-principal
vsce publish --azure-credential

# GitHub Actions, no stored secret at all
vsce publish --oidc
```

`--oidc` with workload identity federation is the best option for CI: nothing long-lived is stored anywhere. Prefer these for any new setup, and treat an existing PAT pipeline as scheduled work rather than something that will keep running.

## Publishing to the Marketplace

```bash
vsce publish                  # uses package.json version
vsce publish minor            # bump, commit tag, publish
vsce publish 1.2.3            # explicit version
vsce publish --packagePath my-extension-1.2.3.vsix   # publish an inspected artifact
```

**Prefer `--packagePath`** so you publish the exact artifact you inspected and installed, rather than a fresh build that could differ.

`--skip-duplicate` avoids an error when the version already exists — useful in CI reruns.

Other commands: `vsce ls-publishers`, `vsce verify-pat`, `vsce show <ext-id>`, `vsce unpublish <ext-id>`.

**Unpublishing does not remove the extension from machines that already installed it.** There is no recall. This is the whole reason the release chain stops on failure.

## Pre-release versions

```bash
vsce publish --pre-release
```

**Semver pre-release tags are not supported** — a version must be plain `major.minor.patch`. `1.2.0-beta.1` is rejected. The marketplace convention is to use odd minor versions for pre-release (`1.3.x` pre-release, `1.4.x` stable); if the team adopts that, keep it consistent, because users opting into pre-releases get whatever is newest.

## Platform-specific packages

Only needed when the extension ships native binaries or platform-specific dependencies.

Targets: `win32-x64`, `win32-arm64`, `linux-x64`, `linux-arm64`, `linux-armhf`, `alpine-x64`, `alpine-arm64`, `darwin-x64`, `darwin-arm64`, `web`.

```bash
vsce package --target darwin-arm64
vsce publish --target win32-x64 win32-arm64
```

VS Code serves the matching build automatically. A pure-TypeScript extension needs none of this — one universal package covers everything.

For web extensions, VS Code tags web capability from the manifest shape (a `browser` entry point), so an explicit `--target web` is generally not required.

## Signing and verification

**The Marketplace signs every extension at publish time — you don't manage keys.** VS Code verifies the signature on install and update, required on all platforms since 1.100.

What this means operationally: if users report install failures with `PackageIntegrityCheckFailed`, `SignatureIsInvalid`, or `NotSigned`, the problem is package integrity or the delivery path, not their VS Code. (`extensions.verifySignature` can disable the check, but recommending that to a user is bad advice — it disables the protection globally.)

`vsce generate-manifest` and `vsce verify-signature` exist for local verification if needed.

Since 1.97, the first install of a third-party extension shows a trust-the-publisher prompt.

## Open VSX

A separate registry (Eclipse Foundation) serving VSCodium and other compatible editors. **VS Code's documentation does not cover it** — don't look there, and don't assume marketplace rules carry over.

```bash
npm install -g ovsx
ovsx create-namespace <namespace>       # one-time
ovsx publish my-extension-0.1.0.vsix -p <token>
ovsx verify-pat <namespace>
```

It uses namespaces rather than publishers. Publishing to the Marketplace does not publish here — they are entirely independent. If both are targets, do both explicitly and say so in the report.

## Internal distribution

```bash
code --install-extension /path/to/my-extension-0.1.0.vsix
code --install-extension /path/to/ext.vsix --force   # overwrite existing
```

Or **Extensions: Install from VSIX** in the Command Palette.

**Auto-update is disabled for VSIX-installed extensions.** Colleagues stay on their first install indefinitely unless told otherwise. Mitigations: announce updates on a channel people read, surface the version in the extension's own output so bug reports identify the build, and keep old `.vsix` files around so a bad release can be rolled back by reinstalling the previous one.

Useful CLI flags for testing a package in isolation:

```bash
code --list-extensions --show-versions
code --disable-extensions                    # launch with all others off
code --extensions-dir /tmp/x --user-data-dir /tmp/u   # throwaway environment
code --profile <name>                        # a named, disposable profile
```

The `--extensions-dir` + `--user-data-dir` pair is the reliable way to test an install against a genuinely clean environment without disturbing your own setup.
