# Dil Ozelligi Provider'lari

`vscode.languages` provider arayuzleri icin ayrintili referans. Her kayit bir `Disposable` dondurur — olusturdugun anda `context.subscriptions` icine it.

## Icindekiler

- [Kayit ve DocumentSelector](#kayit-ve-documentselector)
- [HoverProvider](#hoverprovider)
- [CompletionItemProvider](#completionitemprovider)
- [CodeActionProvider](#codeactionprovider)
- [CodeLensProvider](#codelensprovider)
- [Definition, References, Document Symbols](#definition-references-document-symbols)
- [Bicimlendirme provider'lari](#bicimlendirme-providerlari)
- [Tanilar (Diagnostics)](#tanilar-diagnostics)
- [Iptali dogru yapmak](#iptali-dogru-yapmak)
- [Geciktirme ve onbellek deseni](#geciktirme-ve-onbellek-deseni)

---

## Kayit ve DocumentSelector

Tum provider'lar `vscode.languages.register<X>Provider(selector, provider, ...ekstralar)` seklinde kaydedilir; ekstralar tipe gore degisir.

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  const selector: vscode.DocumentSelector = { language: 'yaml', scheme: 'file' };

  context.subscriptions.push(
    vscode.languages.registerHoverProvider(selector, new MyHoverProvider()),
    vscode.languages.registerCompletionItemProvider(
      selector, new MyCompletionProvider(), '.', ':'   // tetikleyici karakterler
    ),
    vscode.languages.registerCodeActionsProvider(selector, new MyCodeActionProvider(), {
      providedCodeActionKinds: [vscode.CodeActionKind.QuickFix],
    }),
  );
}
```

Bir `DocumentFilter`'in uc istege bagli alani vardir; bir `DocumentSelector` ise tek bir filtre, bir dil-id string'i ya da ikisinden bir dizidir.

```typescript
const loose: vscode.DocumentSelector = 'typescript';                        // herhangi bir TS dokumani
const tight: vscode.DocumentSelector = { language: 'typescript', scheme: 'file' };
const byPath: vscode.DocumentSelector = { scheme: 'file', pattern: '**/config/*.json' };
const many: vscode.DocumentSelector = [
  { language: 'javascript', scheme: 'file' },
  { language: 'javascript', scheme: 'untitled' },
];
```

**`scheme`, insanlarin unuttugu alandir ve hata raporu ureten de odur.** Yalnizca `{ language: 'x' }` ile eslestirmek ayrica `untitled:` (hic kaydedilmemis, yani `uri.fsPath` hicbir seye isaret etmez), `git:` (bir diff goruntusunun salt okunur sol tarafi), `output:`, `vscode-notebook-cell:` ve eklentilerin sagladigi sanal semalarla da eslesir.

Yani: provider bir araca devrediyorsa, dosyayi diskten okuyorsa ya da yollari dosyanin gercek konumuna gore cozuyorsa `scheme: 'file'` ekle. Aksi halde bir git-diff panelinde calisir, hata firlatir ya da sacma sey dondurur ve kullanici "diff'lerde hover bozuk" diye rapor eder. Provider tamamen `document.getText()` uzerinden calisiyorsa semayi acik birakmak bir ozelliktir — kaydedilmemis bir not defterinde completion faydalidir.

**Birden fazla eklenti ayni selector icin kayit olabilir.** VS Code hepsini cagirir ve birlestirir: hover'lar ust uste binerv completion listeleri birlestirilir, code action'lar hepsi ampulde gorunur. "Digerlerini yok say" anlamina gelen bir donus degeri yoktur, bu yuzden asla yalniz oldugunu varsayma ve yerlesik bir provider'in zaten sagladigini asla tekrarlama — iki ayni completion ogesi gorunur bir kusurdur. `undefined` dondurmek basarisizlik degildir; digerlerinin sonuclarinin gecerli kalmasini saglar.

---

## HoverProvider

```typescript
class MyHoverProvider implements vscode.HoverProvider {
  provideHover(
    document: vscode.TextDocument,
    position: vscode.Position,
    token: vscode.CancellationToken
  ): vscode.ProviderResult<vscode.Hover> {
    const range = document.getWordRangeAtPosition(position, /[A-Za-z_][\w.-]*/);
    if (!range) { return undefined; }          // imlecin altinda bir sey yok — normal

    const info = this.lookup(document.getText(range));
    if (!info) { return undefined; }

    const md = new vscode.MarkdownString();
    md.appendMarkdown(`**${info.title}**\n\n${info.summary}\n\n`);
    md.appendCodeblock(info.signature, 'typescript');

    // Komut baglantilari, string guvenilir olarak isaretlenmedikce etkisizdir.
    // isTrusted'i yalnizca icindeki her komut URI'sini sen kurduysan ayarla —
    // workspace icerigiyle kurulmus guvenilir bir string, komut yurutme vektorudur.
    md.isTrusted = true;
    const args = encodeURIComponent(JSON.stringify([info.id]));
    md.appendMarkdown(`\n\n[Open definition](command:myExt.openDef?${args})`);

    return new vscode.Hover(md, range);        // range vermek popup titremesini durdurur
  }
}
```

`ProviderResult<T>`; `T`, `undefined`, `null` ya da bunlarin bir `Thenable`'ina izin verir — asenkron sorun degil.

**Hover fare hareketiyle tetiklenir.** Birkac milisaniyeyi asan her sey editor geneli agirlik olarak hissedilir, cunku paylasilan host uzerindesin. Senkron dosya okumasi yok, onbelleklenmemis surec baslatma yok. `range` saglamak ayrica kullanici deneyimi acisindan onemlidir: onsuz VS Code hover bolgesini tahmin eder ve fare tek bir kelimenin icinde hareket ederken popup titrer.

---

## CompletionItemProvider

```typescript
class MyCompletionProvider implements vscode.CompletionItemProvider {
  provideCompletionItems(
    document: vscode.TextDocument,
    position: vscode.Position,
    token: vscode.CancellationToken,
    context: vscode.CompletionContext
  ): vscode.ProviderResult<vscode.CompletionItem[] | vscode.CompletionList> {
    const linePrefix = document.lineAt(position).text.slice(0, position.character);
    if (!linePrefix.endsWith('.')) { return undefined; }

    return this.members().map((m, i) => {
      const item = new vscode.CompletionItem(m.name, vscode.CompletionItemKind.Method);

      item.sortText = String(i).padStart(4, '0');  // liste sirasi; label yedektir
      item.filterText = m.name;                    // yazilanla neyin eslestirilecegi
      item.preselect = m.isCommon;                 // liste acildiginda vurgulanan

      // SnippetString tab duraklari verir; duz bir string harfiyen eklenir.
      item.insertText = new vscode.SnippetString(`${m.name}(\${1:${m.firstParam}})$0`);

      // Acik range = acik degistirme. Onsuz VS Code degistirilecek araligi
      // mevcut kelimeden cikarir — genelde, ama her zaman degil, dogru.
      item.range = document.getWordRangeAtPosition(position)
        ?? new vscode.Range(position, position);

      (item as any).data = { id: m.id };           // resolve'a tasinir
      return item;
    });
  }

  async resolveCompletionItem(
    item: vscode.CompletionItem,
    token: vscode.CancellationToken
  ): Promise<vscode.CompletionItem> {
    const id = (item as any).data?.id;
    if (!id) { return item; }

    const docs = await this.fetchDocs(id, token);  // yalnizca vurgulanan oge icin
    if (token.isCancellationRequested) { return item; }

    item.documentation = new vscode.MarkdownString(docs.markdown);
    item.detail = docs.signature;
    return item;
  }
}
```

**`resolveCompletionItem` bir incelik degil, performans mekanizmasidir.** `provideCompletionItems` yuzlerce oge dondurebilir ve neredeyse her tus vurusunda tetiklenir; `resolveCompletionItem` en fazla bir oge icin calisir — su anda vurgulanan. Yani label, kind, sortText, filterText, insertText ve range'i `provide` icine; `documentation`, `detail` ve pahali `additionalTextEdits`'i (otomatik import satirlari) `resolve` icine koy.

Resolve, `label`, `filterText`, `sortText` ya da `insertText`'i degistirmemelidir: liste o noktada zaten render edilmis ve filtrelenmistir, bu yuzden o degisiklikler yok sayilir ya da tutarsiz davranis uretir.

- **Tetikleyici karakterler**, kayit sirasindaki sondaki varargs'dir. O karakter yazildiginda provider'i cagirirlar; `context.triggerKind` ve `context.triggerCharacter` hangi yolda oldugunu soyler. Onlarsiz yalnizca acik cagirma ve normal kelime yaziminda cagrilirsin.
- `new vscode.CompletionList(items, /* isIncomplete */ true)`, VS Code'un istemci tarafinda filtrelemek yerine sonraki her tus vurusunda yeniden sorgulamasini saglar. Sunucu tarafi onek aramasi icin dogru; aksi halde cagri sayini katlar.
- `CompletionItemKind` ikonu ve bir kisim siralamayi belirler. Durust olani sec.
- `item.commitCharacters`, bir karakteri hem ogeyi kabul eden hem de eklenen sey yapar. Az kullan — surpriz kabuller kullanicilari cileden cikarir.

---

## CodeActionProvider

```typescript
class MyCodeActionProvider implements vscode.CodeActionProvider {
  provideCodeActions(
    document: vscode.TextDocument,
    range: vscode.Range | vscode.Selection,
    context: vscode.CodeActionContext,
    token: vscode.CancellationToken
  ): vscode.ProviderResult<(vscode.CodeAction | vscode.Command)[]> {
    const actions: vscode.CodeAction[] = [];

    // context.diagnostics yalnizca `range` ile kesisen tanilari tutar, her
    // kaynaktan. Kendi tanilarina filtrele.
    for (const diag of context.diagnostics) {
      if (diag.source !== 'myExt' || diag.code !== 'unknown-key') { continue; }

      const suggestion = this.suggest(diag);
      const fix = new vscode.CodeAction(
        `Replace with "${suggestion}"`, vscode.CodeActionKind.QuickFix);
      fix.edit = new vscode.WorkspaceEdit();
      fix.edit.replace(document.uri, diag.range, suggestion);
      fix.diagnostics = [diag];   // duzeltmeyi arayuzdeki dalgali cizgiye baglar
      fix.isPreferred = true;     // otomatik duzeltme / "Fix All" yoluna uygun
      actions.push(fix);
    }

    if (!range.isEmpty) {
      // Duzenleme yerine komut: VS Code komutu calistirir; komut asenkron
      // olabilir, kullaniciya sorabilir ya da kendi WorkspaceEdit'ini uygulayabilir.
      const extract = new vscode.CodeAction(
        'Extract to variable', vscode.CodeActionKind.RefactorExtract);
      extract.command = {
        command: 'myExt.extractVariable',
        title: 'Extract to variable',
        arguments: [document.uri, range],
      };
      actions.push(extract);
    }

    return actions;
  }
}
```

**Duzenleme mi komut mu.** Degisiklik simdi bilinen saf bir metin donusumuyse `action.edit` kullan — VS Code bunu tek bir geri alinabilir islem olarak uygular ve onizleyebilir. Eylem kullaniciya bir sey sormali, asenkron is yapmali ya da metnin disindaki seylere dokunmaliysa `action.command` kullan. Ikisi birlikte de gecerlidir: once duzenleme uygulanir, sonra komut calisir.

**`providedCodeActionKinds` metadata'si onemlidir.** VS Code seni cagirmadan *once* tipe gore filtreler, yani "Organize Imports" yalnizca `SourceOrganizeImports` beyan eden provider'lari uyandirir. Ne donduruyorsan onu beyan et: beyan edilmemis tipler onlari isteyen filtrelenmis menulerde hic gorunmez ve beyan edilip dondurulmeyen tipler seni bosuna cagirtir.

Tipler hiyerarsik string'lerdir: `QuickFix` (`quickfix`); `RefactorExtract`/`RefactorInline`/`RefactorRewrite` ile birlikte `Refactor` (`refactor`); `SourceOrganizeImports` ve `SourceFixAll` ile birlikte `Source` (`source`). `editor.codeActionsOnSave` icin yalnizca `Source` eylemleri uygundur — "kaydederken bu dosyayi temizle" eyleminin tipinin `SourceFixAll` olmasinin sebebi budur.

`context.only`, istemcinin belirli tek bir tip istedigi anlamina gelir; onun disinda bir sey dondurmek bosa istir.

---

## CodeLensProvider

```typescript
class MyCodeLensProvider implements vscode.CodeLensProvider {
  private readonly onDidChange = new vscode.EventEmitter<void>();
  public readonly onDidChangeCodeLenses = this.onDidChange.event;

  constructor(context: vscode.ExtensionContext) {
    context.subscriptions.push(
      this.onDidChange,
      vscode.workspace.onDidChangeConfiguration(e => {
        if (e.affectsConfiguration('myExt.showLenses')) { this.onDidChange.fire(); }
      })
    );
  }

  provideCodeLenses(
    document: vscode.TextDocument,
    token: vscode.CancellationToken
  ): vscode.ProviderResult<vscode.CodeLens[]> {
    const lenses: vscode.CodeLens[] = [];
    for (let line = 0; line < document.lineCount; line++) {
      if (token.isCancellationRequested) { return []; }
      if (/^\s*(export\s+)?function\s/.test(document.lineAt(line).text)) {
        lenses.push(new vscode.CodeLens(new vscode.Range(line, 0, line, 0)));
      }
    }
    return lenses;   // henuz komut yok — resolve dolduruyor
  }

  async resolveCodeLens(
    lens: vscode.CodeLens,
    token: vscode.CancellationToken
  ): Promise<vscode.CodeLens> {
    const count = await this.countReferences(lens.range, token);   // pahali
    if (token.isCancellationRequested) { return lens; }
    lens.command = {
      title: `${count} reference${count === 1 ? '' : 's'}`,
      command: 'myExt.showReferences',
      arguments: [lens.range],
    };
    return lens;
  }
}
```

Completion ile ayni tembel ayrim: `provideCodeLenses` konumlari ucuza bulur ve lens'leri **komutsuz** dondurur; `resolveCodeLens` komutu doldurur ve yalnizca su anda goruntu alaninda olan lens'ler icin. Komutu ve resolve'u olmayan bir lens hicbir sey olarak render edilir.

`onDidChangeCodeLenses` yenileme mekanizmasidir — onu tetiklemek mevcut lens'leri atar ve `provideCodeLenses`'i yeniden calistirir. Lens icerigi neye bagliysa (kaydetmeler, config, biten bir arka plan analizi) ona bagla ve gecikmeli calistir, cunku her tetikleme tum turu yeniden calistirir. `EventEmitter`'i dispose et.

---

## Definition, References, Document Symbols

```typescript
class MyDefinitionProvider implements vscode.DefinitionProvider {
  provideDefinition(
    document: vscode.TextDocument,
    position: vscode.Position,
    token: vscode.CancellationToken
  ): vscode.ProviderResult<vscode.Definition | vscode.LocationLink[]> {
    const target = this.resolveSymbol(document, position);
    if (!target) { return undefined; }

    return new vscode.Location(target.uri, target.range);

    // LocationLink daha zengindir ve daha iyi peek deneyimi verir:
    //   originSelectionRange — kaynak dokumanda neyin altinin cizilecegi
    //   targetRange          — tam sembol govdesi, peek onizlemesinde kullanilir
    //   targetSelectionRange — imlecin nereye inecegi (genelde yalnizca isim)
    // return [{
    //   originSelectionRange: document.getWordRangeAtPosition(position),
    //   targetUri: target.uri,
    //   targetRange: target.fullRange,
    //   targetSelectionRange: target.nameRange,
    // }];
  }
}

class MyReferenceProvider implements vscode.ReferenceProvider {
  provideReferences(
    document: vscode.TextDocument,
    position: vscode.Position,
    context: vscode.ReferenceContext,     // context.includeDeclaration'a saygi goster
    token: vscode.CancellationToken
  ): vscode.ProviderResult<vscode.Location[]> {
    return this.findAll(document, position, context.includeDeclaration, token);
  }
}
```

Ayni `Definition | LocationLink[]` sekli `registerTypeDefinitionProvider`, `registerImplementationProvider` ve `registerDeclarationProvider` tarafindan da kullanilir.

`provideDocumentSymbols`, `SymbolInformation[]` ya da `DocumentSymbol[]` dondurebilir. **`DocumentSymbol`'u tercih et** — `children` ile ic ice gecer, boylece Outline ve breadcrumb'lar gercek yapiyi gosterir; `SymbolInformation` ise VS Code'un yorumlamak zorunda oldugu bir `containerName` string'iyle duzdur. `SymbolInformation`, sonuclarin dosyalari astigi ve tek bir agacin olmadigi `WorkspaceSymbolProvider` icin dogru olmayi surdurur.

```typescript
class MySymbolProvider implements vscode.DocumentSymbolProvider {
  provideDocumentSymbols(
    document: vscode.TextDocument,
    token: vscode.CancellationToken
  ): vscode.ProviderResult<vscode.DocumentSymbol[]> {
    const cls = new vscode.DocumentSymbol(
      'Widget',
      'class',                          // detail, ismin yaninda soluk gosterilir
      vscode.SymbolKind.Class,
      new vscode.Range(0, 0, 40, 0),    // tam aralik — outline katlamasini belirler
      new vscode.Range(0, 6, 0, 12)     // secim araligi — tam araligin ICINDE OLMALI
    );
    cls.children.push(new vscode.DocumentSymbol(
      'render', '(): void', vscode.SymbolKind.Method,
      new vscode.Range(5, 2, 12, 3), new vscode.Range(5, 2, 5, 8)));
    return [cls];
  }
}
```

`range` icinde yer almayan bir `selectionRange` sembolun reddedilmesine yol acar — "outline'im bos" durumunun en yaygin sebebi budur.

---

## Bicimlendirme provider'lari

Uc kayit, uc tetik, hepsi `TextEdit[]` donduruyor.

```typescript
// Tum dokuman — "Format Document" ve kaydederken bicimlendir.
vscode.languages.registerDocumentFormattingEditProvider(selector, {
  async provideDocumentFormattingEdits(document, options, token) {
    // options: { tabSize, insertSpaces, ... } — bu dokuman icin editorun
    // etkin ayarlari. Onlara saygi goster; kendi girinti config'ini okuma.
    const formatted = await runFormatter(document.getText(), options, token);
    if (token.isCancellationRequested) { return undefined; }

    const whole = new vscode.Range(
      document.positionAt(0), document.positionAt(document.getText().length));
    return [vscode.TextEdit.replace(whole, formatted)];
  },
});

// Secim — "Format Selection"; bunu kaydetmek ayrica yapistirirken bicimlendirmeyi acar.
vscode.languages.registerDocumentRangeFormattingEditProvider(selector, {
  provideDocumentRangeFormattingEdits(document, range, options, token) {
    return formatRange(document, range, options, token);
  },
});

// Kullanici yazarken. Yalnizca editor.formatOnType acikken tetiklenir.
vscode.languages.registerOnTypeFormattingEditProvider(selector, {
  provideOnTypeFormattingEdits(document, position, ch, options, token) {
    if (ch !== '}') { return undefined; }
    return [dedentClosingBrace(document, position)];
  },
}, '}', ';', '\n');   // ilk tetik karakteri arti varargs
```

Tum dosyayi bicimlendirip dilimlemek yerine gercek aralik bicimlendirmesini tercih et — dilimleme baglama duyarli dilleri bozar. Hicbir sey degismediginde bos dizi yerine `undefined` dondur. Asla ortusen araliklar dondurme; sonuc tanimsiz davranistir. Tum dokumani degistirmek kabul edilebilir ama kaba bir geri alma girdisi uretir ve goruntu alanini kaydirabilir, bu yuzden hesaplayabildigin durumda minimal bir diff uret.

---

## Tanilar (Diagnostics)

Tanilar modeli tersine cevirir: kimse sana sormaz. Bir `DiagnosticCollection`'in sahibisin ve kendi takviminde icine yazarsin.

```typescript
export function activate(context: vscode.ExtensionContext) {
  // Isim, Problems panelinde gosterilen varsayilan `source` olur.
  const diagnostics = vscode.languages.createDiagnosticCollection('myExt');
  context.subscriptions.push(diagnostics);

  const timers = new Map<string, NodeJS.Timeout>();

  const schedule = (document: vscode.TextDocument) => {
    if (document.languageId !== 'yaml' || document.uri.scheme !== 'file') { return; }
    const key = document.uri.toString();
    clearTimeout(timers.get(key));
    timers.set(key, setTimeout(() => {
      timers.delete(key);
      diagnostics.set(document.uri, analyze(document));
    }, 300));
  };

  context.subscriptions.push(
    vscode.workspace.onDidChangeTextDocument(e => schedule(e.document)),
    vscode.workspace.onDidOpenTextDocument(schedule),

    // KRITIK. Bu olmadan Problems paneli artik acik olmayan bir dokuman icin
    // hatalari listelemeye devam eder; birine tiklamak dosyayi orada olmayan
    // bir dalgali cizgiyi gostermek icin yeniden acar.
    vscode.workspace.onDidCloseTextDocument(document => {
      const key = document.uri.toString();
      clearTimeout(timers.get(key));
      timers.delete(key);
      diagnostics.delete(document.uri);
    }),
  );

  // Diskte silinmis ya da yeniden adlandirilmis — kapanma olaylari bunu her zaman kapsamaz.
  const watcher = vscode.workspace.createFileSystemWatcher('**/*.yaml');
  context.subscriptions.push(watcher, watcher.onDidDelete(uri => diagnostics.delete(uri)));

  vscode.workspace.textDocuments.forEach(schedule);  // zaten acik dokumanlar
}
```

Temizleme kurallari, ne siklikta atlandiklarina gore siralanmis:

1. Dokuman kapandiginda ve dosya silindiginde `collection.delete(uri)`.
2. Yeniden analiz hicbir sey bulmadiginda `collection.set(uri, [])` — eski dalgali cizgileri kaldiran sey bos dizidir. "Raporlanacak bir sey yok" diye cagriyi atlamak onceki hatalari sonsuza kadar ekranda birakir.
3. Ozellik ayarlarda kapatildiginda ya da workspace klasoru kaldirildiginda `collection.clear()`.
4. `context.subscriptions` uzerinden `collection.dispose()`.

```typescript
function analyze(document: vscode.TextDocument): vscode.Diagnostic[] {
  const diag = new vscode.Diagnostic(
    new vscode.Range(3, 2, 3, 10),
    'Key "retrys" is not recognized. Did you mean "retries"?',
    vscode.DiagnosticSeverity.Warning        // Error | Warning | Information | Hint
  );

  diag.source = 'myExt';                     // Problems'ta gosterilir; code action'lar buna gore filtreler

  // Duz bir kod ya da kullanicinin tiklayabilecegi bir dokuman baglantisiyla bir kod.
  diag.code = {
    value: 'unknown-key',
    target: vscode.Uri.parse('https://example.com/rules/unknown-key'),
  };

  // Onem tasiyan diger yeri goster — semayi, catisan beyani, orijinal tanimi.
  // Ic ice bir girdi olarak render edilir.
  diag.relatedInformation = [
    new vscode.DiagnosticRelatedInformation(
      new vscode.Location(schemaUri, new vscode.Range(10, 0, 10, 20)),
      'Valid keys are declared here'),
  ];

  // Etiketler render'i degistirir: Unnecessary soluklastirir, Deprecated ustunu cizer.
  diag.tags = [vscode.DiagnosticTag.Unnecessary];

  return [diag];
}
```

`DiagnosticSeverity.Hint` hic dalgali cizgi render etmez — yalnizca bir ampul. "Burada bir refactor mevcut" icin dogru, kullanicinin fark etmesi gereken hicbir sey icin yanlis.

---

## Iptali dogru yapmak

Token'i sonda bir kez kontrol etmek neredeyse ise yaramaz. Onemli olan *alttaki isin* durmasidir.

### Yanlis

```typescript
async provideHover(document, position, token) {
  // Buradaki hicbir sey kesilemez. Surec sonuna kadar calisir ve istek
  // tamamlanir; ikisi de paylasilan extension host'ta CPU yakar — kullanicinin
  // on tus vurusu once umursamayi biraktigi bir hover icin.
  const analysis = await runAnalyzer(document.fileName);
  const docs = await fetch(`https://api.example.com/docs/${analysis.symbol}`);

  if (token.isCancellationRequested) { return undefined; }  // onemsemek icin cok gec
  return new vscode.Hover(await docs.text());
}
```

Hizli yazma altinda bu, tus vurusu basina bir terk edilmis surec ve bir terk edilmis istek kuyruklar. Hepsi yine cozulur, yine bellek ayirir ve editor arayuzu ile diger tum eklentilerin paylastigi tek olay dongusu icin yarisir. Kullanici "hover yavas" diye rapor etmez — "editor takiliyor" der.

### Dogru

```typescript
import { spawn } from 'node:child_process';

function runAnalyzer(file: string, token: vscode.CancellationToken): Promise<string> {
  return new Promise((resolve, reject) => {
    const child = spawn('my-analyzer', ['--json', file]);

    const sub = token.onCancellationRequested(() => child.kill());  // gercekten oldur
    const timer = setTimeout(() => child.kill(), 5000);             // asla sonsuza kadar takilma

    let out = '';
    child.stdout.on('data', d => { out += d; });
    child.on('error', reject);
    child.on('close', code => {
      clearTimeout(timer);
      sub.dispose();                       // dinleyici de bir Disposable
      code === 0 ? resolve(out) : reject(new Error(`analyzer exited ${code}`));
    });
  });
}

function fetchDocs(symbol: string, token: vscode.CancellationToken): Promise<string> {
  const controller = new AbortController();
  const sub = token.onCancellationRequested(() => controller.abort());
  return fetch(`https://api.example.com/docs/${symbol}`, { signal: controller.signal })
    .then(r => r.text())
    .finally(() => sub.dispose());
}

async provideHover(
  document: vscode.TextDocument,
  position: vscode.Position,
  token: vscode.CancellationToken
): Promise<vscode.Hover | undefined> {
  const analysis = await runAnalyzer(document.fileName, token);
  if (token.isCancellationRequested) { return undefined; }   // HER await'ten sonra kontrol et

  const docs = await fetchDocs(JSON.parse(analysis).symbol, token);
  if (token.isCancellationRequested) { return undefined; }

  return new vscode.Hover(new vscode.MarkdownString(docs));
}
```

Uc aliskanlik, hepsi zorunlu:

1. **Token'i asagi isle**, her asenkron yardimciya. Token kabul etmeyen bir yardimci iptal edilemez ve bu bir provider yolunda bir hatadir.
2. **Her `await`'ten sonra kontrol et.** Her await, dunyanin ilerlemis olabilecegi bir noktadir; onun otesindeki is, atacagin istir.
3. **`token.onCancellationRequested` bir `Disposable` dondurur.** Islem tamamlandiginda onu dispose et, yoksa provider cagrisi basina bir dinleyici sizdirirsin — ve provider'lar surekli cagrilir.

Iptal bir hata yolu degildir. Iptal edilmis bir token'da `undefined` dondurmek dogru ve sessiz sonuctur: onu loglama, yuzeye cikarma.

---

## Geciktirme ve onbellek deseni

Pahali, dokuman anahtarli provider'lar icin. Onbellek anahtari `uri + version`.

```typescript
interface CacheEntry<T> { version: number; value: Promise<T>; }

/**
 * document.version dogru onbellek anahtaridir: VS Code onu o dokumandaki her
 * tek duzenlemede artirir. Ayni uri + ayni version, metnin bayt olarak ayni
 * oldugu ve onbelleklenmis sonucun hala tam olarak dogru oldugu anlamina
 * gelir; degismis bir version ise girdinin degersiz oldugu. Metni hash'lemek
 * de calisir ama cagri basina tam bir okumaya mal olur; version numarasi ise
 * zaten senin icin tutuluyor. Asla yalnizca uri ile anahtarlama — dosya
 * altindan degisir ve sonsuza kadar bayat sonuc sunarsin.
 */
export class DocumentCache<T> implements vscode.Disposable {
  private readonly entries = new Map<string, CacheEntry<T>>();
  private readonly disposables: vscode.Disposable[] = [];

  constructor(
    private readonly compute:
      (doc: vscode.TextDocument, token: vscode.CancellationToken) => Promise<T>
  ) {
    this.disposables.push(vscode.workspace.onDidCloseTextDocument(
      doc => this.entries.delete(doc.uri.toString())));
  }

  get(document: vscode.TextDocument, token: vscode.CancellationToken): Promise<T> {
    const key = document.uri.toString();
    const hit = this.entries.get(key);
    if (hit && hit.version === document.version) { return hit.value; }

    const value = this.compute(document, token);
    this.entries.set(key, { version: document.version, value });

    // Reddedilmis bir promise onbellekte kalmamali, yoksa basarisizlik bir
    // sonraki duzenlemeye kadar kalici olur.
    value.catch(() => {
      if (this.entries.get(key)?.version === document.version) {
        this.entries.delete(key);
      }
    });

    return value;
  }

  dispose(): void {
    this.entries.clear();
    this.disposables.forEach(d => d.dispose());
  }
}

export function debounce<A extends unknown[]>(fn: (...args: A) => void, ms: number) {
  let timer: NodeJS.Timeout | undefined;
  const wrapped = (...args: A) => {
    if (timer) { clearTimeout(timer); }
    timer = setTimeout(() => { timer = undefined; fn(...args); }, ms);
  };
  wrapped.cancel = () => { if (timer) { clearTimeout(timer); timer = undefined; } };
  return wrapped;
}
```

Geciktirme **itme** tarafina aittir (degisimde tanilar), cekme tarafina degil. `provideCompletionItems` icinde geciktirme yapma — VS Code zaten sordu ve cevabi geciktirmek yalnizca completion'i agir hissettirir; orada bunun yerine onbellekle. Yazma tetikli pencereleri 200-500ms araliginda tut: daha uzunu bozuk hissettirir, daha kisasi amaci bosa cikarir.

---

**Imza kontrolu.** Provider arayuzleri surumler boyunca uye kazandi (`CompletionItemProvider` generic'leri, `CodeActionProvider.resolveCodeAction`, `DocumentPasteEditProvider` gibi yeni provider'lar). Yakin zamanda kullanmadigin her seyi projenin `@types/vscode` icindeki `vscode.d.ts`'ine ve `package.json` icindeki `engines.vscode` tabanina karsi dogrula — o tabandan yeni bir API sorunsuz derlenir ve kullanicinin daha eski editorunde calisma aninda patlar.
