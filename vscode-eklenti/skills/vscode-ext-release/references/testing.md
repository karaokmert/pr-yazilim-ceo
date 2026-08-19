# Extension Test Harness

Setup and patterns for tests that run inside a real VS Code instance.

## Contents

- [Why the real instance matters](#why-the-real-instance-matters)
- [Setup](#setup)
- [Configuration](#configuration)
- [Test patterns](#test-patterns)
- [Async timing and flakiness](#async-timing-and-flakiness)
- [Fixtures](#fixtures)
- [CI](#ci)
- [Web extension tests](#web-extension-tests)

## Why the real instance matters

The harness downloads and launches an actual VS Code, loads the extension, and runs tests inside the extension host. The `vscode` module in your tests is the real one.

This is worth the slowness because the failures that hurt most are precisely the ones a mock cannot reproduce: a contribution point that doesn't register, an activation event that never fires, a command ID mismatch between manifest and code, a provider registered against a selector that never matches. A mocked `vscode` namespace tests your beliefs about the API. Only the real host tests the API.

The tradeoff is real too — these tests take seconds each, not milliseconds. Spend them on integration behavior. Pure logic (parsers, formatters, transformations) should be extracted into modules with no `vscode` import and unit-tested normally, fast.

## Setup

```bash
npm install --save-dev @vscode/test-cli @vscode/test-electron mocha @types/mocha
```

Both packages are needed: `@vscode/test-cli` is the runner and config layer, `@vscode/test-electron` downloads and launches VS Code underneath it.

```jsonc
// package.json
"scripts": {
  "compile-tests": "tsc -p . --outDir out",
  "pretest": "npm run compile-tests && npm run lint",
  "test": "vscode-test"
}
```

Note the compile step. Tests run as JavaScript from `out/`, separate from the bundled `dist/` the extension itself ships — the bundler produces a single file, which is not what a test runner wants.

**The deprecated ancestor is the unscoped `vscode-test` package** (renamed to `@vscode/test-electron`). If a project still uses it, note it as modernization work rather than fixing it during a release.

## Configuration

```javascript
// .vscode-test.js
const { defineConfig } = require('@vscode/test-cli');

module.exports = defineConfig({
  files: 'out/test/**/*.test.js',
  version: 'stable',
  workspaceFolder: './test-fixtures/sample-workspace',
  mocha: {
    ui: 'tdd',
    timeout: 20000
  }
});
```

`files` is the only required option. Others worth knowing:

| Option | Use |
|---|---|
| `version` | `'stable'`, `'insiders'`, or a specific version — test the floor in `engines.vscode` |
| `workspaceFolder` | Folder to open; without it, tests run with no workspace |
| `launchArgs` | Extra CLI args, e.g. `['--disable-extensions']` |
| `installExtensions` | Dependencies to install first |
| `env` | Environment variables |
| `mocha` | Mocha options (`ui`, `timeout`, `grep`) |
| `label` | Names a config when using several |

**Set the Mocha timeout well above the default.** Activation plus a real editor operation regularly exceeds 2000ms, and the resulting failures look like bugs rather than timeouts.

**`--disable-extensions` in `launchArgs` is worth defaulting to.** Otherwise the developer's own installed extensions participate in the test run, and results differ between machines and CI.

Multiple configurations (different VS Code versions, different fixture workspaces) can be exported as an array.

## Test patterns

### Activation

The first test to write. If this fails, nothing else matters.

```typescript
import * as assert from 'assert';
import * as vscode from 'vscode';

suite('Activation', () => {
  test('extension is present', () => {
    assert.ok(vscode.extensions.getExtension('publisher.my-extension'));
  });

  test('activates', async () => {
    const ext = vscode.extensions.getExtension('publisher.my-extension')!;
    await ext.activate();
    assert.strictEqual(ext.isActive, true);
  });

  test('registers its commands', async () => {
    await vscode.extensions.getExtension('publisher.my-extension')!.activate();
    const commands = await vscode.commands.getCommands(true);
    assert.ok(commands.includes('myExt.doThing'));
  });
});
```

That third test is quietly one of the most valuable in the suite: it proves the manifest entry and the `registerCommand` call agree. That mismatch is a top source of "the command doesn't appear" and it is invisible to type checking.

### Commands

```typescript
test('formats the document', async () => {
  const doc = await vscode.workspace.openTextDocument({
    language: 'typescript',
    content: 'const   x=1'
  });
  const editor = await vscode.window.showTextDocument(doc);

  await vscode.commands.executeCommand('myExt.format');

  assert.strictEqual(doc.getText(), 'const x = 1;\n');
});
```

Invoking through `executeCommand` rather than calling the handler directly exercises the registration path too.

### Providers

```typescript
test('provides hover for known symbols', async () => {
  const doc = await vscode.workspace.openTextDocument(
    vscode.Uri.file(path.join(fixtures, 'sample.ts'))
  );
  await vscode.window.showTextDocument(doc);

  const hovers = await vscode.commands.executeCommand<vscode.Hover[]>(
    'vscode.executeHoverProvider',
    doc.uri,
    new vscode.Position(3, 10)
  );

  assert.ok(hovers.length > 0);
  assert.match((hovers[0].contents[0] as vscode.MarkdownString).value, /expected text/);
});
```

The `vscode.execute*Provider` commands go through VS Code's real dispatch, so they verify that the registration and `DocumentSelector` actually match — which calling the provider class directly does not. Available for hover, completion, definition, references, document symbols, code actions, formatting, and more.

### Configuration

```typescript
test('honors the enable setting', async () => {
  const config = vscode.workspace.getConfiguration('myExt');
  await config.update('enable', false, vscode.ConfigurationTarget.Global);
  try {
    // assert disabled behavior
  } finally {
    await config.update('enable', undefined, vscode.ConfigurationTarget.Global);
  }
});
```

**Always restore settings in a `finally`.** Configuration changes persist across tests in the same instance, and a leaked setting produces failures in unrelated tests that are miserable to diagnose.

## Async timing and flakiness

The dominant source of flaky extension tests. Almost nothing in VS Code is synchronous: activation, provider registration, diagnostic computation, and language server readiness all settle on their own schedule.

**Wait for the condition, not for a duration.** `await new Promise(r => setTimeout(r, 500))` is a guess that passes locally and fails in CI:

```typescript
async function waitFor<T>(
  probe: () => T | undefined,
  timeoutMs = 5000,
  intervalMs = 50
): Promise<T> {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const value = probe();
    if (value !== undefined) { return value; }
    await new Promise(r => setTimeout(r, intervalMs));
  }
  throw new Error('Timed out waiting for condition');
}

// Diagnostics are computed asynchronously after the document opens
const diagnostics = await waitFor(() => {
  const d = vscode.languages.getDiagnostics(doc.uri);
  return d.length > 0 ? d : undefined;
});
```

Where an event exists, prefer it to polling — `onDidChangeDiagnostics`, `onDidOpenTextDocument`, `onDidChangeConfiguration`.

**Clean up between tests.** Close editors so state doesn't carry over:

```typescript
teardown(async () => {
  await vscode.commands.executeCommand('workbench.action.closeAllEditors');
});
```

## Fixtures

Keep a fixture workspace under the repo (e.g. `test-fixtures/sample-workspace/`) and point `workspaceFolder` at it. Files with predictable content give tests something real to operate on.

**Make sure fixtures are excluded in `.vscodeignore`** — test data in the shipped `.vsix` is the exact class of mistake the package inspection step exists to catch.

For tests that modify files, either work on copies in a temp directory or restore in teardown. A test that mutates a committed fixture makes the next run pass or fail for the wrong reason.

## CI

Linux CI has no display, so VS Code needs a virtual one:

```yaml
- run: npm ci
- run: xvfb-run -a npm test
  if: runner.os == 'Linux'
- run: npm test
  if: runner.os != 'Linux'
```

Testing against `engines.vscode`'s floor and against `stable` in a matrix is the cheapest way to catch a raised API requirement that nobody declared.

## Web extension tests

If the extension declares a `browser` entry point, desktop tests say nothing about it — the Web Worker host is a different environment with different available APIs.

```bash
npx @vscode/test-web --extensionDevelopmentPath=. --extensionTestsPath=out/test/suite ./test-fixtures
```

`--browserType` selects chromium, firefox, or webkit. A test suite that passes on desktop and was never run in the browser host is a known gap worth stating explicitly in the release report.
