# Contribution Points

Schemas for the contribution points this team uses most. Full reference: `code.visualstudio.com/api/references/contribution-points`.

## Contents

- [commands](#commands)
- [menus and when clauses](#menus-and-when-clauses)
- [configuration](#configuration)
- [keybindings](#keybindings)
- [views and viewsContainers](#views-and-viewscontainers)
- [languages and grammars](#languages-and-grammars)
- [AI-related contributions](#ai-related-contributions)

## commands

```json
"contributes": {
  "commands": [{
    "command": "myExt.doThing",
    "title": "Do The Thing",
    "category": "My Extension",
    "icon": "$(zap)",
    "enablement": "editorLangId == typescript"
  }]
}
```

- **`title`** is what the user reads in the palette. Write it as an action.
- **`category`** prefixes it ("My Extension: Do The Thing") — groups your commands and makes them findable by extension name.
- **`icon`** takes a `$(codicon-name)` reference (see the codicon list) or a light/dark image pair. Only shown where icons render, such as editor title bars.
- **`enablement`** greys the command out when false. Distinct from menu `when`, which hides it entirely.

## menus and when clauses

Declaring a command does **not** place it anywhere except the command palette. Placement is `contributes.menus`:

```json
"menus": {
  "commandPalette": [
    { "command": "myExt.doThing", "when": "editorLangId == typescript" }
  ],
  "editor/context": [
    { "command": "myExt.doThing", "when": "editorHasSelection", "group": "1_modification" }
  ],
  "explorer/context": [
    { "command": "myExt.doThing", "when": "resourceExtname == .json" }
  ],
  "editor/title": [
    { "command": "myExt.doThing", "when": "resourceLangId == markdown", "group": "navigation" }
  ],
  "view/title": [
    { "command": "myExt.refresh", "when": "view == myExt.myView", "group": "navigation" }
  ]
}
```

Common menu locations: `commandPalette`, `editor/context`, `editor/title`, `editor/title/context`, `explorer/context`, `view/title`, `view/item/context`, `scm/title`, `terminal/context`, `comments/comment/title`.

**Groups control ordering.** `navigation` sorts first and renders as icons in title bars. Others (`1_modification`, `9_cutcopypaste`) sort by their numeric prefix. Append `@n` for order within a group: `"group": "navigation@2"`.

**Useful `when` context keys:**

| Key | Meaning |
|---|---|
| `editorFocus`, `editorTextFocus` | Editor has focus |
| `editorHasSelection` | Non-empty selection |
| `editorLangId == x` | Active editor's language |
| `resourceLangId == x` | Language of the resource (works in explorer) |
| `resourceExtname == .x` | File extension |
| `resourceFilename == x` | Exact filename |
| `resourceScheme == file` | URI scheme — use to hide features in virtual workspaces |
| `explorerResourceIsFolder` | Explorer selection is a folder |
| `view == viewId` | Which view |
| `viewItem == contextValue` | Tree item's `contextValue` — how per-item menus work |
| `workspaceFolderCount > 1` | Multi-root |
| `isWindows`, `isMac`, `isLinux` | Platform |
| `config.myExt.enabled` | Any setting's value |

Operators: `==`, `!=`, `&&`, `||`, `!`, `=~` (regex), `in`. Set your own with `vscode.commands.executeCommand('setContext', 'myExt.isReady', true)` — the standard way to gate UI on extension state.

To place a menu item per tree item, set `contextValue` on the `TreeItem` and match `viewItem == thatValue`.

## configuration

```json
"configuration": {
  "title": "My Extension",
  "properties": {
    "myExt.enable": {
      "type": "boolean",
      "default": true,
      "description": "Enable the thing.",
      "scope": "resource"
    },
    "myExt.mode": {
      "type": "string",
      "enum": ["fast", "thorough"],
      "enumDescriptions": ["Quicker, less precise.", "Slower, more precise."],
      "default": "fast",
      "description": "How hard to work."
    },
    "myExt.toolPath": {
      "type": "string",
      "default": "",
      "markdownDescription": "Absolute path to the tool. Leave empty to use `PATH`.",
      "scope": "machine"
    }
  }
}
```

**Always namespace keys** with the extension name. **`scope` matters more than it looks:**

| Scope | Meaning |
|---|---|
| `application` | Global only; cannot be set per workspace |
| `machine` | Per machine; **cannot be overridden by workspace settings** |
| `machine-overridable` | Machine default, workspace may override |
| `window` | Default; per window/workspace |
| `resource` | Per file/folder — right for anything language- or folder-specific |
| `language-overridable` | Per language via `[typescript]` blocks |

**Use `machine` for anything naming an executable or a path that gets run.** Otherwise a cloned repository can point your extension at an arbitrary binary via committed workspace settings. Pair it with `restrictedConfigurations` in `capabilities.untrustedWorkspaces`.

`markdownDescription` renders links and code formatting; `deprecationMessage` marks a setting obsolete without removing it.

## keybindings

```json
"keybindings": [{
  "command": "myExt.doThing",
  "key": "ctrl+alt+t",
  "mac": "cmd+alt+t",
  "when": "editorTextFocus"
}]
```

Keybindings are a scarce shared resource — every extension competes for the same combinations. Prefer chords (`ctrl+k ctrl+t`) and always scope with `when`. Check for conflicts before claiming a common binding.

## views and viewsContainers

```json
"viewsContainers": {
  "activitybar": [{
    "id": "myExtContainer",
    "title": "My Extension",
    "icon": "resources/icon.svg"
  }]
},
"views": {
  "myExtContainer": [{
    "id": "myExt.myView",
    "name": "Things",
    "when": "myExt.hasThings",
    "icon": "resources/view-icon.svg",
    "contextualTitle": "My Extension Things"
  }]
},
"viewsWelcome": [{
  "view": "myExt.myView",
  "contents": "No things found.\n[Scan Workspace](command:myExt.scan)",
  "when": "!myExt.hasThings"
}]
```

Views can go in existing containers (`explorer`, `scm`, `debug`, `test`) instead of a new activity bar entry — often the better choice, since a new activity bar icon is a significant claim on the user's screen.

**`viewsWelcome` is underused.** It turns an empty view into a call to action with clickable command links, and it's the difference between a view that looks broken and one that guides. Activity bar icons should be monochrome SVG.

## languages and grammars

```json
"languages": [{
  "id": "mylang",
  "aliases": ["My Language"],
  "extensions": [".mylang"],
  "configuration": "./language-configuration.json"
}],
"grammars": [{
  "language": "mylang",
  "scopeName": "source.mylang",
  "path": "./syntaxes/mylang.tmLanguage.json"
}]
```

`language-configuration.json` supplies comment tokens, bracket pairs, auto-closing pairs, and folding — cheap to provide and immediately noticeable to users.

## AI-related contributions

Chat participants, language model tools, and MCP server providers are **stable API** (finalized in 1.90 for chat and language models). Relevant when building AI-assisted tooling:

```json
"chatParticipants": [{
  "id": "myExt.participant",
  "name": "myhelper",
  "fullName": "My Helper",
  "description": "Ask about our internal APIs",
  "isSticky": true
}],
"languageModelTools": [{
  "name": "myExt_lookupThing",
  "displayName": "Look Up Thing",
  "modelDescription": "Looks up a thing by name in the internal registry.",
  "toolReferenceName": "lookupThing",
  "canBeReferencedInPrompt": true,
  "icon": "$(search)",
  "inputSchema": {
    "type": "object",
    "properties": { "name": { "type": "string", "description": "Thing name" } }
  }
}],
"mcpServerDefinitionProviders": [{
  "id": "myExt.mcpProvider",
  "label": "My MCP Servers"
}]
```

Registered from `activate()` via `vscode.lm.registerTool` and `vscode.lm.registerMcpServerDefinitionProvider`; chat participants via `vscode.chat.createChatParticipant`.

Two constraints worth knowing before designing around these: **language model access requires user consent**, and `lm.selectChatModels()` should be called from a user-initiated action rather than at activation. The minimum `engines.vscode` for each of these is not clearly documented — determine it from the release notes for the specific feature rather than assuming.
