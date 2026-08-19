# Eklenti Test Duzeni

Gercek bir VS Code ornegi icinde calisan testler icin kurulum ve desenler.

## Icindekiler

- [Gercek ornek neden onemli](#gercek-ornek-neden-onemli)
- [Kurulum](#kurulum)
- [Yapilandirma](#yapilandirma)
- [Test desenleri](#test-desenleri)
- [Asenkron zamanlama ve kararsizlik](#asenkron-zamanlama-ve-kararsizlik)
- [Fixture'lar](#fixturelar)
- [CI](#ci)
- [Web eklentisi testleri](#web-eklentisi-testleri)

## Gercek ornek neden onemli

Duzen gercek bir VS Code indirir ve baslatir, eklentiyi yukler ve testleri extension host icinde calistirir. Testlerindeki `vscode` modulu gercek olandir.

Bu, yavasligina degmektedir cunku en cok can yakan arizalar tam olarak bir taklidin yeniden ureteyemeyecegi olanlardir: kaydolmayan bir katki noktasi, hic tetiklenmeyen bir aktivasyon olayi, manifest ile kod arasinda bir komut ID'si uyusmazligi, hicbir zaman eslesmeyen bir selector'a karsi kaydedilmis bir provider. Taklit bir `vscode` namespace'i API hakkindaki inanclarini test eder. Yalnizca gercek host API'yi test eder.

Odunlesme de gercektir — bu testler her biri milisaniyeler degil saniyeler surer. Onlari entegrasyon davranisi icin harca. Saf mantik (ayristiricilar, formatlayicilar, donusumler) `vscode` import'u olmayan modullere cikarilmali ve normal, hizli sekilde birim testi yapilmalidir.

## Kurulum

```bash
npm install --save-dev @vscode/test-cli @vscode/test-electron mocha @types/mocha
```

Her iki pakete de ihtiyac var: `@vscode/test-cli` kosucu ve yapilandirma katmani, `@vscode/test-electron` ise altta VS Code'u indirip baslatan.

```jsonc
// package.json
"scripts": {
  "compile-tests": "tsc -p . --outDir out",
  "pretest": "npm run compile-tests && npm run lint",
  "test": "vscode-test"
}
```

Derleme adimina dikkat. Testler `out/`'tan JavaScript olarak calisir, eklentinin kendisinin gonderdigi paketlenmis `dist/`'ten ayri — bundler tek bir dosya uretir ki bu bir test kosucusunun istedigi sey degildir.

**Kullanimdan kalkmis atasi, namespace'siz `vscode-test` paketidir** (`@vscode/test-electron` olarak yeniden adlandirildi). Bir proje hala onu kullaniyorsa, bunu bir yayin sirasinda duzeltmek yerine modernlestirme isi olarak not et.

## Yapilandirma

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

`files` tek zorunlu secenektir. Bilinmeye deger digerleri:

| Secenek | Kullanim |
|---|---|
| `version` | `'stable'`, `'insiders'` ya da belirli bir surum — `engines.vscode` icindeki tabani test et |
| `workspaceFolder` | Acilacak klasor; onsuz testler workspace olmadan calisir |
| `launchArgs` | Ek CLI argumanlari, orn. `['--disable-extensions']` |
| `installExtensions` | Once kurulacak bagimliliklar |
| `env` | Ortam degiskenleri |
| `mocha` | Mocha secenekleri (`ui`, `timeout`, `grep`) |
| `label` | Birkac yapilandirma kullanirken birini adlandirir |

**Mocha zaman asimini varsayilanin oldukca uzerine ayarla.** Aktivasyon arti gercek bir editor islemi duzenli olarak 2000ms'yi asar ve olusan basarisizliklar zaman asimi degil hata gibi gorunur.

**`launchArgs` icinde `--disable-extensions` varsayilan yapmaya deger.** Aksi halde gelistiricinin kendi kurulu eklentileri test kosumuna katilir ve sonuclar makineler ile CI arasinda farklilasir.

Birden fazla yapilandirma (farkli VS Code surumleri, farkli fixture workspace'leri) bir dizi olarak export edilebilir.

## Test desenleri

### Aktivasyon

Yazilacak ilk test. Bu basarisiz olursa geri kalan hicbir sey onemli degildir.

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

O ucuncu test, sessizce paketteki en degerli testlerden biridir: manifest girdisiyle `registerCommand` cagrisinin anlastigini kanitlar. O uyusmazlik "komut gorunmuyor" durumunun basli kaynaklarindandir ve tip kontrolune gorunmezdir.

### Komutlar

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

Handler'i dogrudan cagirmak yerine `executeCommand` uzerinden cagirmak, kayit yolunu da dener.

### Provider'lar

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

`vscode.execute*Provider` komutlari VS Code'un gercek dagitimindan gecer, boylece kaydin ve `DocumentSelector`in fiilen eslestigini dogrularlar — provider sinifini dogrudan cagirmak bunu yapmaz. Hover, completion, definition, references, dokuman sembolleri, code action'lar, bicimlendirme ve daha fazlasi icin mevcuttur.

### Configuration

```typescript
test('honors the enable setting', async () => {
  const config = vscode.workspace.getConfiguration('myExt');
  await config.update('enable', false, vscode.ConfigurationTarget.Global);
  try {
    // devre disi davranisi dogrula
  } finally {
    await config.update('enable', undefined, vscode.ConfigurationTarget.Global);
  }
});
```

**Ayarlari her zaman bir `finally` icinde geri yukle.** Yapilandirma degisiklikleri ayni ornekteki testler arasinda kalicidir ve sizdirilmis bir ayar, tani koymasi iskence olan ilgisiz testlerde basarisizliklar uretir.

## Asenkron zamanlama ve kararsizlik

Kararsiz eklenti testlerinin baskin kaynagi. VS Code'da neredeyse hicbir sey senkron degildir: aktivasyon, provider kaydi, tani hesaplamasi ve dil sunucusu hazirligi kendi takvimlerinde oturur.

**Bir sureyi degil, kosulu bekle.** `await new Promise(r => setTimeout(r, 500))` lokalde gecen ve CI'da basarisiz olan bir tahmindir:

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

// Tanilar dokuman acildiktan sonra asenkron hesaplanir
const diagnostics = await waitFor(() => {
  const d = vscode.languages.getDiagnostics(doc.uri);
  return d.length > 0 ? d : undefined;
});
```

Bir olayin mevcut oldugu yerde onu yoklamaya tercih et — `onDidChangeDiagnostics`, `onDidOpenTextDocument`, `onDidChangeConfiguration`.

**Testler arasinda temizle.** Durumun tasinmamasi icin editorleri kapat:

```typescript
teardown(async () => {
  await vscode.commands.executeCommand('workbench.action.closeAllEditors');
});
```

## Fixture'lar

Depo altinda bir fixture workspace'i tut (orn. `test-fixtures/sample-workspace/`) ve `workspaceFolder`'i ona yonlendir. Ongorulebilir icerikli dosyalar, testlere uzerinde calisacak gercek bir sey verir.

**Fixture'larin `.vscodeignore` icinde dislandigina emin ol** — gonderilen `.vsix` icindeki test verisi, tam olarak paket inceleme adiminin yakalamak icin var oldugu hata sinifidir.

Dosyalari degistiren testler icin ya bir gecici dizindeki kopyalar uzerinde calis ya da teardown'da geri yukle. Commit'lenmis bir fixture'i degistiren bir test, sonraki kosumun yanlis sebeple gecmesine ya da kalmasina yol acar.

## CI

Linux CI'nin ekrani yoktur, bu yuzden VS Code'un sanal bir ekrana ihtiyaci vardir:

```yaml
- run: npm ci
- run: xvfb-run -a npm test
  if: runner.os == 'Linux'
- run: npm test
  if: runner.os != 'Linux'
```

`engines.vscode`in tabanina ve `stable`a karsi bir matriste test etmek, kimsenin beyan etmedigi yukseltilmis bir API gereksinimini yakalamanin en ucuz yoludur.

## Web eklentisi testleri

Eklenti bir `browser` giris noktasi beyan ediyorsa masaustu testleri onun hakkinda hicbir sey soylemez — Web Worker host'u, farkli kullanilabilir API'leri olan farkli bir ortamdir.

```bash
npx @vscode/test-web --extensionDevelopmentPath=. --extensionTestsPath=out/test/suite ./test-fixtures
```

`--browserType`, chromium, firefox ya da webkit secer. Masaustunde gecen ve tarayici host'unda hic calistirilmamis bir test paketi, yayin raporunda acikca belirtmeye deger bilinen bir bosluktur.
