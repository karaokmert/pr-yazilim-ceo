# Activation Events

Detailed reference. The decision rules are in the parent SKILL.md; this file has the full event list, the auto-generation boundary, and the debugging procedure.

## Contents

- [Auto-generated events](#auto-generated-events)
- [Events you must still declare](#events-you-must-still-declare)
- [Startup performance](#startup-performance)
- [Debugging activation](#debugging-activation)

## Auto-generated events

Since **VS Code 1.74**, declaring a contribution generates its activation event. Do not also list these:

| Contribution | Auto-generated event | Since |
|---|---|---|
| `contributes.commands` | `onCommand:<id>` | 1.74 |
| `contributes.languages` | `onLanguage:<id>` | 1.74 |
| `contributes.views` | `onView:<id>` | 1.74 |
| `contributes.customEditors` | `onCustomEditor:<viewType>` | 1.74 |
| `contributes.authentication` | `onAuthenticationRequest:<id>` | 1.74 |
| `contributes.taskDefinitions` | `onTaskType:<type>` | 1.76 |

A manifest targeting 1.74+ frequently has no `activationEvents` array at all. That is correct and modern, not an omission.

If `engines.vscode` is below 1.74, you must list them manually — another reason not to leave a stale engine floor in place.

## Events you must still declare

**`onStartupFinished`** — after startup completes. The correct choice for background work with no natural trigger, and the correct replacement for `*` in nearly every case where `*` appears.

**`workspaceContains:<glob>`** — when the workspace contains a matching file. Excellent for project-type-specific tooling: an extension for a particular framework stays inert in every unrelated project.

```json
"activationEvents": ["workspaceContains:**/.myproject-config.json"]
```

Note the cost: VS Code searches the workspace to evaluate this. A very broad glob on a huge repository is itself a startup cost.

**`onFileSystem:<scheme>`** — a file with the given URI scheme is opened (`ftp`, `ssh`, custom schemes).

**`onDebug`**, `onDebugResolve:<type>`, `onDebugInitialConfigurations` — debugging-related activation.

**`onUri`** — the extension's URI handler is invoked from outside VS Code (OAuth callbacks, deep links).

**`onWebviewPanel:<viewType>`** — VS Code restores a webview from a previous session. Required if webviews should survive a window reload.

**`onTerminalProfile:<id>`**, `onWalkthrough:<id>`, `onNotebook:<type>`, `onRenderer:<id>`, `onEditSession:<scheme>`, `onSearch:<scheme>` — narrower cases; look up the current shape when you need one.

**`*`** — during startup, always. `vsce package` **rejects this** unless given `--allow-star-activation`. Before using it, verify that `onStartupFinished` truly doesn't work; it almost always does.

## Startup performance

Activation cost is shared. Every extension's activation runs while the user waits for a usable editor, and users routinely have dozens installed.

- Keep `activate()` to registration. Defer indexing, network calls, and process spawning until first use.
- `activate()` may be `async`; VS Code awaits it. Awaiting slow work there directly delays startup.
- **Measure rather than guess**: the `Developer: Show Running Extensions` command reports each extension's activation time and what triggered it. Use it before optimizing.
- `Developer: Startup Performance` gives a fuller breakdown.

## Debugging activation

When an extension appears completely dead, this order finds the cause fastest:

1. **`Developer: Show Running Extensions`** — is it activated at all? If it's absent, the activation event never fired.
2. **Check the trigger matches reality.** `onLanguage:javascript` won't fire for a `.ts` file; a `workspaceContains` glob won't match if the file is nested differently than assumed.
3. **Output panel → "Extension Host" channel** — activation errors surface here, not as a dialog. An exception thrown in `activate()` leaves the extension half-initialized and silently broken.
4. **Confirm the command ID matches exactly** between `contributes.commands` and `registerCommand`. A typo produces exactly this symptom.
5. **Check `engines.vscode`** against the running VS Code version. Too high, and the extension won't load at all.

**Extension Bisect** (`Help: Start Extension Bisect`) is the tool for the other direction — when something is broken and you don't know which of many installed extensions is responsible. It binary-searches by enabling and disabling halves.
