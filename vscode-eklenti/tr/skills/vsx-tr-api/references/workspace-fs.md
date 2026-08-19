# Workspace, Dosyalar ve Editorler

`vscode.Uri`, `vscode.workspace` ve dokuman/editor API'leri icin ayrintili referans. Ust skill kurallari kapsar; bu dosya sekilleri kapsar.

Yonlendirici fikir: **workspace mutlaka yerel diskte degildir.** Uzaktan SSH, dev container'lar, WSL, GitHub Codespaces, `vscode.dev` tarayici derlemesi ve diger eklentilerin katkida bulundugu sanal dosya sistemleri — hepsi siradan workspace'ler olarak gorunur. `vscode.Uri` ve `workspace.fs`'e karsi yazilmis kod bunlarin hepsinde calisir. Node `path` ve `fs`'e karsi yazilmis kod tam olarak birinde calisir ve asla goremeyecegin bir kullanicinin makinesinde basarisiz olur.

## Icindekiler

- [Uri temelleri](#uri-temelleri)
- [workspace.fs](#workspacefs)
- [Node fs ne zaman kabul edilebilir](#node-fs-ne-zaman-kabul-edilebilir)
- [Workspace klasorleri](#workspace-klasorleri)
- [Dosya bulmak](#dosya-bulmak)
- [TextDocument ve editorler](#textdocument-ve-editorler)
- [Duzenleme: WorkspaceEdit mi editor.edit mi](#duzenleme-workspaceedit-mi-editoredit-mi)
- [Position ve Range](#position-ve-range)
- [FileSystemWatcher](#filesystemwatcher)
- [Dokuman olaylari](#dokuman-olaylari)
- [Depolama konumlari](#depolama-konumlari)

---

## Uri temelleri

Bir `Uri`, `scheme:` + `authority` + `path` + `query` + `fragment` demektir. VS Code'da adreslenebilir her sey birer tanedir — dosyalar, kaydedilmemis buffer'lar, Git blob'lari, ayarlar, uzak dosya sistemlerinin icindeki kaynaklar.

### Olusturmak

```typescript
import * as vscode from 'vscode';

// Bir isletim sistemi yolundan. Windows surucu harflerini ve ayiricilari dogru ele alir.
const a = vscode.Uri.file('/home/me/project/src/index.ts');
const w = vscode.Uri.file('C:\\Users\\me\\project\\src\\index.ts');

// Tam bir URI string'inden. Bir sema gerektirir — bu, isletim sistemi yollari ICIN DEGILDIR.
const b = vscode.Uri.parse('https://example.com/api?x=1');
const c = vscode.Uri.parse('untitled:Untitled-1');

// Birlestirme. path.join ya da string birlestirme yerine bunu kullan:
// semayi ve authority'yi korur, boylece uzak ve sanal uri'lerde calisir.
const d = vscode.Uri.joinPath(folder.uri, 'src', 'index.ts');

// Diger her seyi koruyarak bir varyant turetmek.
const e = d.with({ path: d.path + '.map' });
```

`Uri.parse(birIsletimSistemiYolu)` tekrarlayan bir hatadir. `parse('/home/me/file.ts')` bos semali bir Uri uretir; `parse('C:\\x\\y.ts')` ise `c:`'yi sema olarak yorumlar. Isletim sistemi yollari icin `Uri.file`, zaten URI'ye benzeyen seyler icin `Uri.parse` kullan.

### scheme

Sema, elinde ne tur bir sey oldugunu soyler ve capraz ortam hatalarinin cogunu onleyen kontrol odur.

| Sema | Nedir |
| --- | --- |
| `file` | Extension host'un gorebildigi dosya sistemindeki gercek bir dosya. |
| `untitled` | Arkasinda dosya olmayan kaydedilmemis bir buffer. |
| `git` | Salt okunur bir Git blob'u (bir diff goruntusunun sol paneli). |
| `vscode-remote` | Yerel bir UI eklentisinden gorulen, uzak bir makinedeki dosya. |
| `vscode-userdata` | Ayarlar, kisayollar, snippet'ler. |
| `output`, `vscode-notebook-cell`, … | Cesitli ozelliklerden sanal dokumanlar. |
| baska her sey | Baska bir eklentinin katkida bulundugu sanal bir dosya sistemi. |

Dil provider'lari bunlarin hepsinde cagrilir. `scheme` filtresi olmadan `'typescript'` uzerine kaydedilmis bir provider Git diff panellerinde ve cikti kanallarinda da tetiklenir. Ozelligin yalnizca gercek dosyalar icin anlamliysa ya selector'i filtrele (`{ language: 'typescript', scheme: 'file' }`) ya da en ustte koru:

```typescript
if (document.uri.scheme !== 'file') { return undefined; }
```

Bir `git:` uri'sine yazmak basarisiz olur. Bir `vscode-remote:` yoluna karsi bir formatlayici binary calistirmak basarisiz olur, cunku yol senin kodunu calistiran makinede degildir.

### fsPath ve path

```typescript
uri.path     // Her zaman URI yol bileseni: egik cizgiler, yuzde-cozulmus.
uri.fsPath   // Platforma ozgu isletim sistemi yolu. Windows'ta ters egik cizgi, surucu harfi, bastaki egik cizgi yok.
```

**`fsPath` yalnizca `file` semasi icin anlamlidir.** Baska herhangi bir semada, diskte hicbir seyi adlandirmayan makul gorunumlu bir string uretir. Ariza modu budur: hata firlatmaz, sana bir yol verir ve iki satir sonraki `fs.readFile`, yeniden ureteyemeyecegin bir makinede ENOENT ile basarisiz olur.

Bundan cikan kural:

- `fsPath`'i yalnizca bir yolu VS Code disindaki bir seye — bir alt surece, bir Node API'sine — verirken ve yalnizca `scheme === 'file'` oldugunu teyit ettikten sonra kullan.
- Karsilastirmalar, glob eslestirmesi ve URI tarafi kimligin gosterimi icin `path` kullan.
- **Uri'leri asla string olarak karsilastirma.** `uri.toString()` yuzde kodlamasina gore farklilasir; `uri.fsPath` Windows surucu harfi buyuk-kucuk harfine gore farklilasir. `a.toString() === b.toString()`i yalnizca ayni kaynaktan gelen tam degerler icin karsilastir; baska her sey icin `a.scheme === b.scheme && a.path === b.path` karsilastir ya da workspace'in kendi yardimcilarini kullan.
- `uri.toString()` yuzde kodlar. `uri.toString(true)` kodlamayi atlar ki bu yalnizca gosterim icindir — kodlama-atlanmis bir string'i asla `parse`'a geri dondurme.

## workspace.fs

`vscode.workspace.fs`, Uri'nin adlandirdigi dosya sistemi neyse onun uzerinde `FileSystemProvider` islemlerini uygular. Her yerde asenkron ve bayt yonelimlidir.

```typescript
const fs = vscode.workspace.fs;

// Okuma ve yazma Uint8Array'dir. Kodlama parametresi yoktur.
const bytes: Uint8Array = await fs.readFile(uri);
await fs.writeFile(uri, new Uint8Array([1, 2, 3]));

// Metadata.
const st: vscode.FileStat = await fs.stat(uri);
// st.type: FileType.File | Directory | SymbolicLink (bir bit maskesi — symlink'ler birlesir)
// st.size, st.ctime, st.mtime

// Dizinler.
const entries: [string, vscode.FileType][] = await fs.readDirectory(dirUri);
await fs.createDirectory(dirUri);   // ara dizinleri olusturur, mkdir -p gibi

// Degistirme.
await fs.delete(uri, { recursive: true, useTrash: true });
await fs.rename(src, dest, { overwrite: false });
await fs.copy(src, dest, { overwrite: false });
```

### Metin yardimcilari

`readFile`/`writeFile` bayt konustugu icin, her cagri noktasinda cozmek yerine bir kez sarmala:

```typescript
const decoder = new TextDecoder();          // varsayilan utf-8
const encoder = new TextEncoder();          // her zaman utf-8

export async function readText(uri: vscode.Uri): Promise<string> {
  return decoder.decode(await vscode.workspace.fs.readFile(uri));
}

export async function writeText(uri: vscode.Uri, content: string): Promise<void> {
  await vscode.workspace.fs.writeFile(uri, encoder.encode(content));
}
```

`writeFile` dosya yoksa olusturur ve varsa keser, ama her saglayicida eksik ust dizinleri **olusturmaz**. Var oldugundan emin degilsen once ust dizinde `createDirectory` cagir.

### Yokluk normaldir

Eksik bir dosyada `stat`, bir `FileSystemError` ile reddedilir. "Orada degil" siradan bir cevap oldugu icin varsaymak yerine sor:

```typescript
export async function exists(uri: vscode.Uri): Promise<boolean> {
  try {
    await vscode.workspace.fs.stat(uri);
    return true;
  } catch (err) {
    if (err instanceof vscode.FileSystemError && err.code === 'FileNotFound') {
      return false;
    }
    throw err;   // izinler, ulasilamayan saglayici — bunlari yutma
  }
}
```

Her seyi yakalayip `false` dondurmek, izin hatalarini ve kopmus uzak baglantilari "dosya eksik" olarak gizler ki bu hata ayiklamayi yanlis yone gonderir.

### useTrash

`delete(uri, { useTrash: true })`, saglayicinin destekledigi yerde isletim sistemi cop kutusuna tasir; boylece bir hata geri alinabilir. Kullanicinin makul olarak geri isteyebilecegi her sey icin tercih et. Her dosya sisteminde desteklenmez; bunu yapamayan bir saglayici basarisiz olmak yerine kalici olarak siler.

### Bir editorde acik olan bir dosyayi okumak

`workspace.fs.readFile` *diski* okur. Kullanicinin kaydedilmemis degisiklikleri varsa bayat icerigi alirsin. Bir dokuman acik olabilecekse bunun yerine dokuman API'si uzerinden oku:

```typescript
const doc = await vscode.workspace.openTextDocument(uri);
const text = doc.getText();   // kaydedilmemis duzenlemeleri yansitir
```

## Node fs ne zaman kabul edilebilir

Node `fs`, uc kosulun uc de gecerliyse savunulabilir:

1. Yol **eklentiye ait**, workspace icerigi degil — `context.globalStorageUri`, bir onbellek dizini, ev dizinindeki bir aracin kendi config'i.
2. Eklentinin **yalnizca masaustu oldugu teyit edilmis** (zaten surec baslatiyor ya da `package.json` bir `browser` giris noktasi beyan etmiyor).
3. Uri'yi semasinin `file` olacagi sekilde **kontrol etmis ya da kurmus**sun.

O zaman bile, uzak bir workspace'te `context.globalStorageUri` *uzak* makinede yasar ki bu genelde istedigin seydir ama bilincli olmaya deger.

```typescript
import * as fsNode from 'node:fs/promises';

// Yalnizca masaustu eklenti, eklentiye ait onbellek dizini, globalStorageUri'den
// insa oldugu icin file semasi garantili. Node fs burada streaming destegi icin
// kullaniliyor.
const cacheDir = context.globalStorageUri;
if (cacheDir.scheme !== 'file') {
  throw new Error('Cache requires a local filesystem.');
}
await fsNode.mkdir(cacheDir.fsPath, { recursive: true });
```

**Bu karari verdiginde sebebini bir yorumda belirt.** Gelecekteki bir okuyucu, bilincli bir yalnizca-masaustu kararini birinin tanidik API'ye uzanmasindan ayirt edemez ve fark, eklentinin tarayicida calisip calismadigidir.

Workspace icerigi asla bu kategoride degildir. Kullanicinin kaynak dosyalarini Node `fs` ile okumak, bu bolumun onlemek icin var oldugu belirli hatadir.

## Workspace klasorleri

`workspace.workspaceFolders`, `readonly WorkspaceFolder[] | undefined` tipindedir. Uc durum, hepsi siradan:

```typescript
const folders = vscode.workspace.workspaceFolders;

if (!folders || folders.length === 0) {
  // Acik klasor yok — kullanici tek bir dosya acti ya da bos bir pencere.
  // Hata degil. Nazikce geri cekil: aktif editor uzerinde calis ya da acikla ve don.
  return;
}

if (folders.length === 1) {
  const root = folders[0];
  // root.uri, root.name, root.index
}

// Cok koklu. Sessizce folders[0]'i secme.
```

`workspaceFolders[0]`, eklenti kodundaki en yaygin tek cokmedir ve ikinci en yaygin hatadir (cok koklu bir workspace'te 2..n klasorlerini sessizce yok saymak).

### Bir kaynagin hangi klasore ait oldugunu cozmek

```typescript
const folder = vscode.workspace.getWorkspaceFolder(someUri);
// Kaynak her workspace klasorunun disindaysa undefined —
// orn. diskte baska bir yerden acilmis bir dosya ya da kendisi workspace
// klasoru olmayan bir klasorun altindaki bir node_modules dosyasi.
```

Klasor basina yapilandirmayi, klasor basina arac cagirmayi ve klasor basina ciktiyi kapsamlandirmanin dogru yolu budur.

### Aktif editorun klasorune kapsamlandirmak

Bir islem dogasi geregi tek klasorluyse (bir linter calistir, bir config ac), durust cozumleme sirasi sudur: aktif editorun klasoru, sonra tam olarak bir tane varsa o tek klasor, sonra sor.

```typescript
async function pickTargetFolder(): Promise<vscode.WorkspaceFolder | undefined> {
  const active = vscode.window.activeTextEditor?.document.uri;
  if (active) {
    const owner = vscode.workspace.getWorkspaceFolder(active);
    if (owner) { return owner; }
  }

  const folders = vscode.workspace.workspaceFolders ?? [];
  if (folders.length === 1) { return folders[0]; }
  if (folders.length === 0) { return undefined; }

  return vscode.window.showWorkspaceFolderPick({
    placeHolder: 'Select a folder to run in',
  });
}
```

`showWorkspaceFolderPick`, diger tum seciciler gibi kapatildiginda `undefined` dondurur.

### Gosterim yollari ve degisiklik olaylari

```typescript
// Gosterim icin workspace'e goreli. Ikinci argüman olarak false gecmedikce
// cok koklu ortamlarda klasor adini icerir.
const label = vscode.workspace.asRelativePath(uri);
const bare = vscode.workspace.asRelativePath(uri, false);

context.subscriptions.push(
  vscode.workspace.onDidChangeWorkspaceFolders(e => {
    // e.added, e.removed — klasor basina state'i yeniden kur (watcher'lar, onbellekler, indeksler)
    for (const removed of e.removed) { this.disposeFolderState(removed); }
    for (const added of e.added) { void this.initFolderState(added); }
  }),
);
```

Eklentin klasor basina kaynak tutuyorsa (her birine bir watcher, her birine bir onbelleklenmis indeks) bu dinleyici istege bagli degildir — onsuz, canli bir workspace'e klasor eklemek, eklentinin hic gormedigi bir klasor uretir.

## Dosya bulmak

```typescript
const uris = await vscode.workspace.findFiles(
  '**/*.config.json',      // dahil: GlobPattern
  '**/node_modules/**',    // haric: GlobPattern | null | undefined
  200,                     // maxResults
  token,                   // CancellationToken
);
```

### RelativePattern aramayi kapsamlandirir

Ciplak bir string glob'u **her** workspace klasorunu arar. Tek bir klasoru — ya da hic workspace klasoru olmayan bir dizini — aramak icin `RelativePattern` kullan:

```typescript
const pattern = new vscode.RelativePattern(folder, 'src/**/*.ts');
const found = await vscode.workspace.findFiles(pattern, null, 100, token);

// Ayrica bir Uri tabani kabul eder; bir alt dizinin altini boyle ararsin.
const subPattern = new vscode.RelativePattern(
  vscode.Uri.joinPath(folder.uri, 'packages'),
  '*/package.json',
);
```

### Dislamalar

`findFiles`, gectigin haric argümanina ek olarak kullanicinin `files.exclude` ve `search.exclude` ayarlarina saygi gosterir. Sonuclari:

- Haric argümani olarak `undefined` gecmek yine de kullanicinin ayarlarini uygular.
- Acikca `null` gecmek *varsayilan* dislamalari devre disi birakir — yani `node_modules` ve `.git` icinde yururusun. Nadiren istedigin sey.
- Kullanicinin aramadan dislarigi bir dosya, eklentinin ona ihtiyaci olsa bile dondurulmez. Dislanmis dosyalari gormek zorundaysan `readDirectory` gezinmesi yedegindir.

### Maliyet

Buyuk bir depoda genis bir glob gercekten yavastir — bir monorepo'da `**/*` saniyeler surebilir ve on binlerce sonuc uretebilir.

- Yalnizca sinirli bir kumeye ihtiyacin oldugunda her zaman `maxResults` gecir. Akis formu yoktur; promise bir kez, her seyle birlikte cozulur.
- Arama bir provider'i ya da kullanicinin uzaklasabilecegi bir arayuzu besliyorsa her zaman bir `CancellationToken` isle.
- Glob'u olabildigince siki capalamis ol: `src/**/*.ts`, `**/*.ts`'i yener ve bir `RelativePattern` ikisini de yener.
- Sonuclari onbellekle ve her istekte aramayi yeniden calistirmak yerine bir `FileSystemWatcher`'dan gecersiz kil.

## TextDocument ve editorler

### Acmak

```typescript
// Uri ile — genel form. Zaten acik bir dokuman varsa onu dondurur.
const doc = await vscode.workspace.openTextDocument(uri);

// Isletim sistemi yoluyla — kolaylik, yalnizca file semasi.
const doc2 = await vscode.workspace.openTextDocument('/abs/path/file.ts');

// Icerikli yeni bir kaydedilmemis buffer. Diske hicbir sey yazilmaz.
const scratch = await vscode.workspace.openTextDocument({
  language: 'json',
  content: JSON.stringify(report, null, 2),
});
```

`openTextDocument` dokumani bellege yukler ve `onDidOpenTextDocument`'i tetikler; hicbir sey **gostermez**. Gostermek ayri bir adimdir:

```typescript
const editor = await vscode.window.showTextDocument(doc, {
  viewColumn: vscode.ViewColumn.Beside,
  preview: false,        // false = gercek bir sekme, italik onizleme sekmesi degil
  preserveFocus: true,   // imleci kullanicinin biraktigi yerde birak
  selection: new vscode.Range(0, 0, 0, 0),
});
```

`preview: false` ayrimi onemlidir: birkac dokumani varsayilan `preview: true` ile acmak tek bir sekmeyi yeniden kullanir, boylece her acilis oncekini degistirir ve kullanicinin elinde yalnizca sonuncusu kalir.

### Mevcut durumu okumak

```typescript
const editor = vscode.window.activeTextEditor;
if (!editor) { return; }   // aktif editor olmamasi normaldir — kullanici bir webview'de,
                           // ayarlarda, terminalde ya da karsilama sayfasinda olabilir

const doc = editor.document;
const all = doc.getText();
const selected = doc.getText(editor.selection);   // secim bosken bos string
const line = doc.lineAt(editor.selection.active.line);
// line.text, line.range, line.rangeIncludingLineBreak,
// line.firstNonWhitespaceCharacterIndex, line.isEmptyOrWhitespace

vscode.window.visibleTextEditors;   // ekrandaki her editor, bolunmus paneller dahil
vscode.workspace.textDocuments;     // acik her dokuman, gorunur editoru olmayanlar dahil
```

`activeTextEditor`, hissettirdiginden cok daha sik `undefined`'dir. Bir komut yalnizca editor icinse `registerTextEditorCommand` tam olarak seni bu kontrolden kurtarmak icin vardir.

### Offset'ler ve pozisyonlar

```typescript
const offset: number = doc.offsetAt(position);
const position: vscode.Position = doc.positionAt(offset);
```

Bunlar, bayt ya da karakter offset'i konusan her araca — bir ayristirici, `getText()` uzerinde bir regex, bir AST — koprudür. Sinirda cevir ve VS Code kodunun icinde `Position` ile kal.

Uyariyi not et: `offsetAt`/`positionAt`, JavaScript string indekslerine uyan UTF-16 kod birimlerini sayar. UTF-8 bayt offset'i raporlayan bir arac, dogrudan devir degil gercek bir donusum ister ve fark yalnizca ASCII olmayan karakter iceren dosyalarda ortaya cikar — ki bu tam olarak gonderilen turden bir hatadir.

### Dokuman kimligi ve durumu

```typescript
doc.uri;          // kimlik
doc.fileName;     // fsPath tadinda string; ayni uyarilar gecerli
doc.languageId;   // 'typescript', 'json', ... — VS Code ayarlar, kullanici degistirebilir
doc.version;      // her degisiklikte artar; dogru bayatlik kontrolu
doc.isDirty;      // kaydedilmemis degisiklikleri var
doc.isUntitled;   // hic diske kaydedilmemis — anlamli bir fsPath'i yok
doc.isClosed;     // dokuman gitti; onu duzenleme
doc.eol;          // EndOfLine.LF | CRLF
doc.lineCount;
```

`doc.version`, asenkron isin gecersizlestigini boyle tespit edersin:

```typescript
const versionAtStart = doc.version;
const result = await expensiveAnalysis(doc.getText());
if (doc.version !== versionAtStart) { return; }   // kullanici yazdi; sonuc bayat
applyResult(result);
```

Metni karsilastirmak ya da zaman damgalarini karsilastirmak calismaz — `version` amaclanan mekanizmadir.

## Duzenleme: WorkspaceEdit mi editor.edit mi

### WorkspaceEdit

Genel amacli duzenleme API'si. Birden fazla dosyayi kapsar, **tek bir geri alma adimi** olarak uygulanir, hicbir editorde acik olmayan dokumanlarda calisir ve ayni islemde dosya olusturabilir/yeniden adlandirabilir/silebilir.

```typescript
const edit = new vscode.WorkspaceEdit();

edit.replace(docA.uri, rangeInA, 'newText');
edit.insert(docB.uri, new vscode.Position(0, 0), '// generated\n');
edit.delete(docB.uri, someRange);

// Dosya islemleri ayni geri alma adimina katilir.
edit.createFile(newUri, { overwrite: false, ignoreIfExists: true });
edit.renameFile(oldUri, newUri, { overwrite: false });
edit.deleteFile(deadUri, { recursive: false, ignoreIfNotExists: true });

const ok = await vscode.workspace.applyEdit(edit);
if (!ok) {
  vscode.window.showErrorMessage('Could not apply changes.');
  return;
}
```

**`applyEdit` bir boolean dondurur ve `false` olabilir.** Hedef bir dokuman duzenlemenin altinda degistiginde, bir dosya salt okunur oldugunda, dosya sistemi saglayicisi reddettiginde ya da araliklar catistiginda basarisiz olur. Donus degerini yok saymak en kotu hata sinifini uretir: eklenti basari raporlar ve hicbir sey olmamistir.

Tek bir `WorkspaceEdit` icindeki araliklarin hepsi, duzenlemeden *once*ki dokuman durumuna gore cozulur; yani onceki eklemeler icin sonraki offset'leri ayarlaman gerekmez. Istisna, ortusen araliklardir — onlar tanimsiz davranistir ve duzenlemeyi kurmadan once birlestirilmelidir.

`applyEdit` kaydetmez. Degisikligin diske ulasmasi gerekiyorsa ardindan `doc.save()` cagir ve kullanici adina kaydetmenin onlarin kaydederken-bicimlendir ve diger katilimcilarini tetikleyecegini dusun.

### editor.edit

Tek bir gorunur editore kapsamlandirilmistir ve ayni islemin parcasi olarak secimi degistirmenin tek yoludur.

```typescript
const applied = await editor.edit(builder => {
  builder.replace(editor.selection, transformed);
  builder.insert(new vscode.Position(0, 0), header);
});
if (!applied) { return; }

editor.selection = new vscode.Selection(newStart, newEnd);
editor.revealRange(new vscode.Range(newStart, newEnd),
  vscode.TextEditorRevealType.InCenterIfOutsideViewport);
```

Callback senkron olmalidir. Icinde `await` kullanmak, await'ten sonra kuyruklanan duzenlemeleri sessizce dusurur, cunku edit builder yalnizca cagri suresince gecerlidir. Once her seyi hesapla, sonra `edit`i cagir.

Iki `editor.edit` cagrisi iki geri alma adimidir; bir refactor'un `edit` cagrilari dongusu olarak uygulanmasinin kullaniciya on iki kez Ctrl+Z'ye bastirmasinin sebebi budur.

**Yalnizca aktif editoru duzenlemiyorsan ve imlec kontrolune ihtiyacin yoksa `WorkspaceEdit`'i sec.** Code action'lar, refactor'lar, hizli duzeltmeler ve birden fazla dosyaya dokunan her sey icin dogru cevap `WorkspaceEdit`'tir — ve ozellikle code action'lar icin zorunlu olandir, cunku eylem duzenlemeyi uygulamak yerine tasir.

## Position ve Range

```typescript
const pos = new vscode.Position(line, character);   // ikisi de SIFIR TABANLI
const range = new vscode.Range(startLine, startChar, endLine, endChar);
const range2 = new vscode.Range(startPos, endPos);
const sel = new vscode.Selection(anchorPos, activePos);
```

`Position` ve `Range` degismezdir. Metotlar yeni ornekler dondurur:

```typescript
pos.translate(1, 0);              // bir satir asagi
pos.with({ character: 0 });       // ayni satirin basi
range.with({ end: newEnd });
range.contains(pos);
range.intersection(other);        // Range | undefined
range.union(other);
range.isEmpty;                    // start ve end esit — bir imlec, secim degil
range.isSingleLine;
```

`Selection extends Range` ve yon ekler:

- `anchor` — secimin basladigi yer (kullanicinin bastigi yer).
- `active` — imlecin simdi oldugu yer (kullanicinin surukledigi yer).
- `isReversed` — kullanici geriye dogru sectiginde true, yani `active` `anchor`dan once gelir.

`Range`'den devralinan `start`/`end` her zaman siralidir; `anchor`/`active` degildir. Metin islemleri icin `start`/`end`, "imlec nerede" icin `active` kullan.

`editor.selections` (cogul) cok imlecli durumdur ve her zaman en az bir girdisi vardir. Yalnizca `editor.selection`'i ele alan bir komut calisir ama diger imlecleri sessizce yok sayar ki bu, cok imlecli modda yasayan kullanicilar icin gercek bir hata raporudur.

### Bir eksik kaymasi

**VS Code satirlari ve karakterleri sifir tabanlidir. Neredeyse her dis arac bir tabanli satir raporlar ve bircogu bir tabanli sutun da raporlar.** Derleyiciler, linter'lar, `grep -n`, stack trace'ler, `tsc` ciktisi, ESLint, kendi protokolunu konusan cogu dil sunucusu.

Donusum tek bir cikarmadir ve surekli unutulur. Belirti, tutarli sekilde bir satir yukarida olan tanilar ve vurgulamalardir — fark edilecek kadar gorunur, gonderilecek kadar ince.

Donusumu sinirda acik ve isimlendirilmis yap:

```typescript
interface ToolLocation {
  line: number;    // dis aractan, 1 tabanli
  column: number;  // dis aractan, 1 tabanli
}

/** Bir aracin 1 tabanli konumunu VS Code'un 0 tabanli Position'ina cevirir. */
function toPosition(loc: ToolLocation): vscode.Position {
  return new vscode.Position(Math.max(0, loc.line - 1), Math.max(0, loc.column - 1));
}
```

Arac basina kontrol etmeye deger iki takip:

- Bazi araclar 1 tabanli satir ama **0 tabanli** sutun raporlar. Bir konvansiyon yoktur; simetriyi varsaymak yerine aracin dokumanini oku ya da bilinen bir dosyaya karsi test et.
- VS Code'da bir `Range` sonu dislayicidir. Kapsayici bir bitis araligi raporlayan bir arac, tabana gore `-1`den *sonra* bitis karakterinde `+1` ister ki bu net olarak degisiklik yapmaz — ve bunu yanlis yapmak bir karakter kisa bir vurgu uretir; fark edilmesi en zor varyant.

Bir arac sutunsuz yalnizca satir raporladiginda `doc.lineAt(line).range` sana tum satiri verir ki bu bir sutun tahmin etmekten daha iyidir.

## FileSystemWatcher

```typescript
const watcher = vscode.workspace.createFileSystemWatcher(
  new vscode.RelativePattern(folder, '**/*.config.json'),
  false,   // ignoreCreateEvents
  false,   // ignoreChangeEvents
  false,   // ignoreDeleteEvents
);

context.subscriptions.push(
  watcher,
  watcher.onDidCreate(uri => this.onConfigAdded(uri)),
  watcher.onDidChange(uri => this.scheduleReload(uri)),
  watcher.onDidDelete(uri => this.onConfigRemoved(uri)),
);
```

**Watcher ve her dinleyici ayri dispose edilebilirlerdir.** Hepsini it. Canli dinleyicileri olan dispose edilmis bir watcher yine closure'lari sizdirir.

### Ne gorur, ne gormez

- Varsayilan olarak bir watcher yalnizca **workspace klasorlerinin icindeki** yollari kapsar. Disarisini izlemek bir Uri tabanli `RelativePattern` gerektirir ve bunun destegi dosya sistemi saglayicisina gore degisir — buna guvenmeden once guncel dokumanlara karsi dogrula.
- Kullanicinin `files.watcherExclude` ayarina saygi gosterir. Kullanicinin disladigi dosyalar (yaygin olarak `node_modules`, `.git`, derleme ciktisi), glob'un ne derse desin olay uretmez.
- Uc yok sayma bayragi maliyet icin vardir. Yalnizca silmeleri onemseyen bir watcher, handler'da filtrelemek yerine `ignoreCreateEvents` ve `ignoreChangeEvents`i `true` yapmalidir — bayraklar olaylarin hic iletilmemesini saglar.

### Geciktirme

Tek bir mantiksal degisiklik siklikla birden fazla olay uretir. Bir kaydetme `change`i iki kez tetikleyebilir; atomik yazan bir editor (gecici yaz, uzerine yeniden adlandir) `create`, sonra `delete`, sonra `change` tetikler; bir `git checkout` bir patlama halinde yuzlerce olay tetikler.

Gercek is yapmadan once bunlari birlestir:

```typescript
const pending = new Set<string>();
let timer: NodeJS.Timeout | undefined;

function scheduleReload(uri: vscode.Uri) {
  pending.add(uri.toString());
  if (timer) { clearTimeout(timer); }
  timer = setTimeout(() => {
    timer = undefined;
    const batch = [...pending].map(s => vscode.Uri.parse(s));
    pending.clear();
    void reloadAll(batch);
  }, 300);
}
```

Ayrica: watcher olaylari sana bir yolun degistigini soyler, simdi ne icerdigini degil. `workspace.fs` ya da `openTextDocument` uzerinden yeniden oku ve baktiginda dosyanin bazen gitmis olmasini bekle — bir degisikligi bir silme izlemis olabilir.

## Dokuman olaylari

```typescript
context.subscriptions.push(
  // Dokuman basina HER tus vurusunda tetiklenir. Burada asla senkron gercek is yapma.
  vscode.workspace.onDidChangeTextDocument(e => {
    // e.document, e.contentChanges (araliklar + metin), e.reason (Undo | Redo | undefined)
    if (e.contentChanges.length === 0) { return; }   // yalnizca metadata degisikligi, orn. dirty bayragi
    if (e.document.uri.scheme !== 'file') { return; }
    debouncedAnalyze(e.document);
  }),

  vscode.workspace.onDidSaveTextDocument(doc => { void runLinter(doc); }),
  vscode.workspace.onDidOpenTextDocument(doc => { void analyze(doc); }),
  vscode.workspace.onDidCloseTextDocument(doc => { diagnostics.delete(doc.uri); }),
);
```

`onDidChangeTextDocument`, tum eklenti API'sinin sicak yoludur. Onu geciktir (200-500ms), once semaya ve dile gore filtrele ve handler govdesinde asla tum bir dosyayi ayristirma. `e.contentChanges` sana degisen tam araliklari verir ki bu bircok durumda artimli is icin yeterlidir.

`onDidCloseTextDocument`, tanilarin temizlendigi yerdir. Onu atlamak, kullanicinin kapattigi dosyalar icin Problems panelinde bayat hatalar birakir — klasik "hayalet hatalar" sikayeti.

Bu olaylarin *dokumanlari* kapsadigini, dosyalari degil, unutma. Bir dokuman gorunur editoru olmadan acik olabilir ve bir dosya hic dokuman olayi olmadan diskte degisebilir (o, watcher'in isi).

### Kaydetme katilimcilari

`onWillSaveTextDocument`, bir kaydetme tamamlanmadan once duzenlemelere katkida bulunmani saglar:

```typescript
context.subscriptions.push(
  vscode.workspace.onWillSaveTextDocument(e => {
    if (e.document.languageId !== 'myLang') { return; }
    if (e.reason !== vscode.TextDocumentSaveReason.Manual) { return; }

    // waitUntil, Thenable<TextEdit[]> ya da Thenable<void> kabul eder.
    // Handler govdesi icinde senkron cagrilmali.
    e.waitUntil(computeEdits(e.document));
  }),
);
```

Kisitlar, hepsi zorlanir:

- `waitUntil`, olay sirasinda **senkron** cagrilmalidir. Bir `await`ten sonra cagirmak hata firlatir, cunku kaydetme zaten ilerlemistir.
- Bir **zaman asimi** vardir — cok uzun surersen kaydetme senin duzenlemelerin olmadan devam eder. Bunu saniyeler degil, birkac yuz milisaniyelik bir butce olarak ele al. Yavas is, kaydetmeyi bloke etmedigi `onDidSaveTextDocument` icine aittir.
- Birden fazla eklenti katilir. Sira garanti edilmez ve baska bir katilimcinin duzenlemeleri seninkinden once ya da sonra inebilir.
- Burada dondurulen duzenlemeler yalnizca kaydedilen dokumana uygulanir. Dosyalar arasi olan her sey, baska bir yerden tetiklenen bir `WorkspaceEdit`e aittir.

`onWillSaveTextDocument`in asiri kullanilmasi kolaydir. Kullanici kaydederken bir donusum istemediyse ekleme; kaydederken-bicimlendir onlarin bilerek actigi bir ayardir ve dosyalarinda surpriz bir degisiklik, hic ozellik olmamasindan kotudur.

## Depolama konumlari

```typescript
context.extensionUri;      // kurulu eklenti dizini — SALT OKUNUR
context.globalStorageUri;  // eklenti basina, workspace'ler arasi, yazilabilir
context.storageUri;        // eklenti basina, workspace basina, yazilabilir — klasor yoksa undefined
context.logUri;            // oturum basina log dizini, yazilabilir
```

| Konum | Kapsam | Omur | Ne icin |
| --- | --- | --- | --- |
| `extensionUri` | Kurulu eklenti | Her guncellemede degistirilir | Gomulu varliklar: ikonlar, sablonlar, semalar. Asla yazma. |
| `globalStorageUri` | Kullanici, tum workspace'ler | Kaldirilana kadar | Onbellekler, indirilen araclar, projeler arasi veri. |
| `storageUri` | Kullanici, bu workspace | Kaldirilana kadar | Proje basina indeksler, proje basina onbellekler. |
| `logUri` | Bu oturum | Periyodik temizlenir | Bir oturum boyunca saklamaya deger log dosyalari. |

Tablodan cikan kurallar:

- **`extensionUri` icine asla yazma.** Dizin guncellemede tumden degistirilir, bu yuzden oraya yazilan her sey sessizce kaybolur — ve bazi kurulumlarda salt okunurdur, yani yazma dogrudan basarisiz olur. Onu yalnizca gomulu kaynaklari okumak ve webview kaynak koklerini kurmak icin `Uri.joinPath` ile kullan.
- **Acik bir workspace klasoru yokken `storageUri` `undefined`dir.** Bu, farkli bir sekilde `workspaceFolders` ile ayni uc durumlu problemdir. `globalStorageUri`'ye geri don ya da ozelligi atla:

```typescript
const storage = context.storageUri ?? context.globalStorageUri;
await vscode.workspace.fs.createDirectory(storage);
const dataFile = vscode.Uri.joinPath(storage, 'index.json');
```

- **Bu dizinlerin hicbirinin var oldugu garanti degildir.** Ilk yazmadan once `createDirectory` cagir; idempotenttir.
- Bunlar *dosyalar* icindir. Kucuk degerler — bayraklar, son kullanilan secimler, imlec konumlari — `context.globalState` / `context.workspaceState` icine aittir ve kimlik bilgileri `context.secrets` icine ve baska hicbir yere.
- Uzak bir workspace'te bu Uri'ler uzak makineye isaret eder, extension host'un calistigi yerle uyumlu olarak. Bu normalde dogrudur ama yerelde kurulmus bir onbellegin uzak bir pencereye gectikten sonra orada olmayacagi anlamina gelir.

---

**Imza kontrolu.** `workspace.fs.copy`, `LogOutputChannel` donemi eklemeleri ve `RelativePattern` Uri-tabani asiri yuklemesi orijinal API'den sonra geldi ve watcher'in workspace klasorleri disindaki davranisi surumler boyunca degisti. Yakin zamanda kullanmadigin her seyi `@types/vscode` icindeki guncel `vscode.d.ts`'e ve `package.json` icindeki `engines.vscode` tabanina karsi dogrula — o tabandan yeni bir API sorunsuz derlenir ve kullanicinin daha eski editorunde calisma aninda patlar.
