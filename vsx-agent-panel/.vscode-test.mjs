import { defineConfig } from '@vscode/test-cli';

export default defineConfig({
  files: 'out/test/**/*.test.js',
  // Testler kullanicinin GERCEK ~/.claude/sessions dizinine karsi degil,
  // her testin kendi kurdugu sahte HOME'a karsi kosar (bkz. suite icindeki
  // env kurulumu). Bos bir gecici klasor acilir: acik bir klasor olmadan
  // bazi API'ler (workspace.fs, createFileSystemWatcher) farkli davranir.
  workspaceFolder: './src/test/fixtures/workspace',
  mocha: {
    ui: 'tdd',
    timeout: 20000,
  },
});
