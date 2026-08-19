# Workspace Trust and Virtual Workspaces

Detailed reference for `capabilities`. The parent SKILL.md gives the shapes and the honesty rule; this file has the decision guide, the runtime implementation of `"limited"`, and the reasoning behind each field.

Official docs: `code.visualstudio.com/api/extension-guides/workspace-trust` and `code.visualstudio.com/api/extension-guides/virtual-workspaces`.

## Contents

- [What Restricted Mode actually is](#what-restricted-mode-actually-is)
- [Deciding your untrustedWorkspaces value](#deciding-your-untrustedworkspaces-value)
- [Implementing "limited" in code](#implementing-limited-in-code)
- [restrictedConfigurations and machine scope](#restrictedconfigurations-and-machine-scope)
- [Virtual workspaces](#virtual-workspaces)
- [Writing the description text](#writing-the-description-text)
- [Reviewing this honestly](#reviewing-this-honestly)

## What Restricted Mode actually is

When a user opens a folder VS Code has not seen before, it asks: **"Do you trust the authors of the files in this folder?"** Until they answer yes, the window runs in **Restricted Mode**.

The threat this defends against is specific and real. Cloning a repository to read it, reviewing a pull request from a stranger, opening an attachment someone emailed — none of those are consent to run that person's code. But an editor is a code-execution engine. Before workspace trust existed, opening a folder was enough: a `.vscode/settings.json` in the repo could point an extension's "path to the linter binary" setting at a script in the repo, and the extension would dutifully spawn it. The user did nothing but open a folder.

Restricted Mode closes that. In an untrusted window VS Code:

- **Disables extensions that declare `untrustedWorkspaces.supported: false`** entirely. They do not activate at all until trust is granted. The user sees them greyed out with your `description` as the explanation.
- **Runs extensions declaring `"limited"`**, but ignores the workspace-provided values of any setting listed in `restrictedConfigurations`.
- **Runs extensions declaring `true`** normally, on the extension's word that this is safe.
- Blocks its own dangerous behaviors: tasks, debugging, and workspace-defined terminal profiles do not run.

Trust is per-folder and remembered. It can also arrive **mid-session** — the user clicks "Trust" in the banner without reloading the window. That is why the runtime API below exists and why "check trust once at activation" is a bug.

The declaration is not advisory. `false` means your extension does not run, so choosing it has a real cost to users working in untrusted folders. Choosing `true` when it is not warranted has a cost to their machine.

## Deciding your untrustedWorkspaces value

The test is not "does my extension feel dangerous". It is: **can content in the workspace influence what code gets executed?** Workspace content includes files, but critically also `.vscode/settings.json`, `.vscode/tasks.json`, and any config file your extension reads.

### Unsafe untrusted — declare `false` or `"limited"`

- **Spawns a binary whose path comes from a workspace setting.** `myExt.formatterPath`, `myExt.pythonPath`, `myExt.eslintPath`. The repository sets it to `./tools/pwn.sh` and you run it.
- **Runs scripts defined in the workspace.** Executing npm scripts, Makefile targets, or a `tasks.json` entry — the script body is attacker-controlled.
- **Evaluates workspace configuration as code.** Loading `myext.config.js` with `require()` or `import()`. A JS config file *is* a program; requiring it runs it. This one is frequently overlooked because it feels like "reading config".
- **Passes workspace content to an interpreter.** Handing a workspace file to `node`, `python`, `bash`, or an `eval()`. Also any templating engine that permits expressions.
- **Starts a language server or tool from `node_modules`.** The repo controls `node_modules`; a postinstall-planted binary there is workspace-controlled code.
- **Reads credentials and sends them somewhere the workspace names.** A workspace setting supplying an endpoint URL plus an extension holding a token is exfiltration.
- **Auto-applies workspace-supplied edits or commands** without a user gesture.

### Safe untrusted — `true` is defensible

- **Syntax highlighting via a TextMate grammar or semantic tokens** computed in-process from buffer text. No execution.
- **Formatting with a formatter bundled inside the extension**, where the workspace cannot redirect which binary runs and cannot inject arguments.
- **Read-only analysis in-process**: parsing files with a bundled parser and publishing diagnostics. Reading a file is not running it.
- **Pure UI**: a color theme, an icon theme, a keymap, a snippet set.
- **Features driven entirely by user settings**, where you have marked the risky settings `machine` scope so a workspace cannot supply them at all.

The middle ground is common and is exactly what `"limited"` is for: highlight and parse immediately, but do not spawn the configured linter until the user trusts the folder.

## Implementing "limited" in code

Declaring `"limited"` without gating anything in code is worse than declaring `true` — it claims a safety property you did not build. The manifest is a promise; this is the implementation.

Two pieces of API:

- **`vscode.workspace.isTrusted`** — a boolean, correct at the moment you read it.
- **`vscode.workspace.onDidGrantWorkspaceTrust`** — fires when the user grants trust mid-session. Trust is never revoked in a live window, so there is no corresponding "revoked" event; you only ever transition untrusted to trusted.

The pattern: **register safe features unconditionally, defer dangerous ones behind a single enable function, and call that function either immediately or from the event.**

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  // Always safe: in-process, no workspace-controlled execution.
  registerSafeFeatures(context);

  if (vscode.workspace.isTrusted) {
    enableTrustedFeatures(context);
  } else {
    // Trust can arrive later without a window reload. Without this listener the
    // user grants trust and the extension stays half-functional until restart.
    const sub = vscode.workspace.onDidGrantWorkspaceTrust(() => {
      enableTrustedFeatures(context);
      sub.dispose(); // one-shot: trust is not revoked in a live window
    });
    context.subscriptions.push(sub);

    // Tell the user why things are missing, without nagging on every activation.
    void vscode.window.setStatusBarMessage(
      '$(shield) MyExt: linting disabled until this workspace is trusted',
      10_000
    );
  }
}

function registerSafeFeatures(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.languages.registerDocumentSymbolProvider(
      { language: 'mylang' },
      new InProcessSymbolProvider() // parses buffer text, spawns nothing
    )
  );
}

// Guard against double-registration: this can run at activation OR from the
// trust event, and must be idempotent either way.
let trustedFeaturesEnabled = false;

function enableTrustedFeatures(context: vscode.ExtensionContext) {
  if (trustedFeaturesEnabled) return;
  trustedFeaturesEnabled = true;

  // Only now do we read a setting that names an executable and run it.
  const linterPath = vscode.workspace
    .getConfiguration('myExt')
    .get<string>('linterPath', 'mylint');

  context.subscriptions.push(startLinterProcess(linterPath));
}
```

Commands are a common leak in this pattern. A command registered in `contributes.commands` appears in the palette regardless of trust, so a dangerous command must check trust **when invoked**, not only at registration:

```typescript
vscode.commands.registerCommand('myExt.runBuildTask', async () => {
  if (!vscode.workspace.isTrusted) {
    // Prompts the user; resolves once they answer.
    const granted = await vscode.workspace.requestWorkspaceTrust({
      message: 'Running the build task executes scripts from this workspace.'
    });
    if (!granted) {
      vscode.window.showWarningMessage('Build requires a trusted workspace.');
      return;
    }
  }
  await runBuild();
});
```

Two further notes:

- **Multi-root workspaces are trusted as a unit.** `isTrusted` is a single window-level boolean, not per-folder. You cannot trust one root and not another.
- **`requestWorkspaceTrust` is a user-facing prompt.** Call it in response to a user gesture, never during `activate()` — a prompt on startup trains users to click "Trust" reflexively, which defeats the whole mechanism.

## restrictedConfigurations and machine scope

`restrictedConfigurations` is an optional `string[]` of setting IDs. In an untrusted workspace VS Code **ignores the workspace-provided value** of each listed setting and falls back to the user or default value. Your `getConfiguration().get()` call returns the safe value; you do not write any filtering code.

**The rule of thumb: if a setting names an executable, a script, a path that gets run, or arguments passed to a process, it belongs here.** Also include settings that select a module to load, a plugin directory to scan, or an endpoint that receives data.

```json
"capabilities": {
  "untrustedWorkspaces": {
    "supported": "limited",
    "description": "%capabilities.untrusted.description%",
    "restrictedConfigurations": [
      "myExt.linterPath",
      "myExt.linterArgs",
      "myExt.pluginDirectory",
      "myExt.telemetryEndpoint"
    ]
  }
}
```

### Pair it with `scope: "machine"`

`restrictedConfigurations` protects untrusted workspaces. **`scope: "machine"` in `contributes.configuration` goes further: the setting cannot be set from workspace settings at all, trusted or not** — only from user settings or the machine-level settings file.

```json
"contributes": {
  "configuration": {
    "title": "MyExt",
    "properties": {
      "myExt.linterPath": {
        "type": "string",
        "default": "mylint",
        "scope": "machine",
        "description": "Absolute path to the mylint executable."
      }
    }
  }
}
```

`scope: "machine-overridable"` is the middle option: machine-level by default, but a workspace may override it — which reopens the hole in trusted workspaces only. Use it when project-specific values are genuinely needed.

Belt and braces: a path-to-executable setting should be **`machine` scope and listed in `restrictedConfigurations`**. The scope stops workspace override; the restricted list is the second layer if the scope is ever relaxed. They cost nothing together and they fail independently.

## Virtual workspaces

A **virtual workspace** is one where the files are not on local disk. VS Code serves them through a `FileSystemProvider` under a non-`file:` URI scheme. Real cases:

- **github.dev** — pressing `.` on a GitHub repo. Files come from the GitHub API; nothing is cloned.
- **vscode.dev** with a remote repository open.
- **Any extension contributing a custom `FileSystemProvider`** — an FTP browser, an S3 bucket viewer, an in-memory or database-backed filesystem.

Note this is orthogonal to web extensions: **desktop VS Code can open a virtual workspace too.** You can be running in Node with full `fs` available, and still have no real path for the workspace files. That is the trap.

### The test

Ask three questions about your extension's workspace handling:

1. **Does it use Node `fs` on workspace paths?** `fs.readFileSync(uri.fsPath)` fails — there is no such file. Use `vscode.workspace.fs`, which routes through the provider.
2. **Does it spawn a process against workspace files?** `spawn('eslint', [filePath])` cannot work; the child process has no way to see a `vscode-vfs://` URI. This is usually fatal for virtual support, not patchable.
3. **Does it assume `uri.fsPath` is a real path?** In a virtual workspace `fsPath` still returns a string, which is what makes this so easy to get wrong. It is a display-shaped path, not something the OS can open. Also avoid `path.join` on it and joining URI strings by hand — use `vscode.Uri.joinPath`.

If all three are no and everything goes through `workspace.fs` and `Uri`, you likely support virtual workspaces already.

### It defaults to true — this is the important gotcha

**Omitting `virtualWorkspaces` means `true`.** An extension that requires real files on disk and simply never thought about this gets offered to users on github.dev, installs cleanly, activates, and then silently fails — or throws `ENOENT` errors that make no sense to a user who can plainly see the file in the explorer.

An extension that needs real files must declare `false` **deliberately**. Nothing warns you.

```json
"capabilities": {
  "virtualWorkspaces": {
    "supported": false,
    "description": "The linter runs as a local process and needs files on disk."
  }
}
```

The bare-boolean shorthand is valid and fine when there is nothing to explain:

```json
"capabilities": { "virtualWorkspaces": true }
```

But note the asymmetry: `"virtualWorkspaces": false` as a bare boolean is legal JSON but gives the user no explanation for why the extension is unavailable. Prefer the object form whenever the value is `false` or `"limited"`.

There is **no `restrictedConfigurations` for `virtualWorkspaces`**. That field exists only under `untrustedWorkspaces`. Virtual workspaces are a capability problem, not a security-boundary problem — there is no attacker-controlled-settings vector to neutralize, so the field would have no meaning.

For `"limited"`, gate at runtime on the scheme rather than on a trust flag:

```typescript
const isVirtual = vscode.workspace.workspaceFolders?.every(
  f => f.uri.scheme !== 'file'
) ?? false;

if (isVirtual) {
  // Register only the providers that work over workspace.fs.
  registerReadOnlyFeatures(context);
} else {
  registerFullFeatures(context);
}
```

## Writing the description text

**`description` is required whenever `supported` is `false` or `"limited"`** — for both `untrustedWorkspaces` and `virtualWorkspaces`. It is optional only when `supported` is `true`, where there is nothing to explain. Omitting it on a restricted declaration leaves the user looking at a disabled feature with no stated reason, which is why the field is mandatory rather than encouraged.

The `description` is **shown to the user in the UI** — in the extensions list next to a disabled extension, and in the trust dialog. It is not a code comment. Write it for someone who does not know what your extension does internally and is trying to understand why something is missing.

A workable formula: **what is unavailable + why + what to do about it, in one sentence.**

Good:

> `"Linting and formatting are disabled until you trust this workspace, because they run tools configured by the project."`

> `"Running the test suite requires files on disk, so this extension is unavailable in remote repositories."`

Bad, and why:

- `"Not supported."` — tells the user nothing; they still have to guess.
- `"This extension does not support untrustedWorkspaces."` — restates the manifest field name back at the user.
- `"Requires trust due to child_process.spawn on user-configured binary paths."` — implementation detail. The user does not know what `spawn` is and cannot act on it.

Localize it. The `description` supports `%key%` substitution from `package.nls.json` like any other user-facing manifest string:

```json
"capabilities": {
  "untrustedWorkspaces": {
    "supported": "limited",
    "description": "%capabilities.untrustedWorkspaces.description%"
  }
}
```

```json
{
  "capabilities.untrustedWorkspaces.description":
    "Linting is disabled until you trust this workspace, because linters are configured by the project."
}
```

Skipping localization here is a common miss — teams localize command titles and forget these strings, which are precisely the ones a confused user reads.

## Reviewing this honestly

The declaration must match what the code does. This is the whole point of the mechanism, and it is checkable.

When reviewing (qa-publisher especially), run these checks:

1. **If `untrustedWorkspaces.supported` is `true`, grep the source for execution surfaces** — `child_process`, `spawn`, `exec`, `execFile`, `fork`, dynamic `require(`/`import(`, `eval`, `new Function`. Any hit demands a justification: does the workspace influence what runs?
2. **Every setting that names a path-to-run appears in `restrictedConfigurations`** and preferably carries `scope: "machine"`. Cross-check `contributes.configuration` against the restricted list; an unlisted `*Path` or `*Command` setting is the finding.
3. **`"limited"` is backed by real gating.** Search for `isTrusted` and `onDidGrantWorkspaceTrust`. If neither appears, the `"limited"` claim is decorative and the extension is behaving as `true`.
4. **`description` is present whenever `supported` is `false` or `"limited"`**, and is written for users.
5. **If `virtualWorkspaces` is absent or `true`, grep for `fsPath`, `require('fs')`, and `path.join` applied to workspace URIs.** Hits mean the default is wrong and `false` should be declared.
6. **Trust checks are not activation-only.** A dangerous command must re-check on invocation.

A `supported: true` that the code does not honor is **a security misrepresentation, not a documentation bug**. VS Code disables extensions on the strength of that field; a user who chose Restricted Mode specifically decided not to run untrusted code, and a wrong declaration silently overrides their decision. Marketplace review may catch it. It may also not. Treat this as a correctness gate, not a polish item — and when in doubt between `true` and `"limited"`, choose `"limited"` and gate the risky half.
