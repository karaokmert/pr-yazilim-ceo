# Web Eklentileri

`browser` ve web extension host icin ayrintili referans. Ust SKILL.md kisit ozetini verir; bu dosyada manifest sekilleri, tasima haritasi, cift hedefli kaynak yerlesimi, dogrulama ve web destegini hic denemeye deger olup olmadigi karari var.

Resmi dokumanlar: `code.visualstudio.com/api/extension-guides/web-extensions`.

## Icindekiler

- [Web extension host nedir](#web-extension-host-nedir)
- [Manifest sekilleri](#manifest-sekilleri)
- [Kisitlar ve her birinin nedeni](#kisitlar-ve-her-birinin-nedeni)
- [Tasima haritasi: Node deseninden web karsiligina](#tasima-haritasi-node-deseninden-web-karsiligina)
- [Paylasilan kaynak, platform dallari](#paylasilan-kaynak-platform-dallari)
- [Browser bundle'inin gercekten temiz oldugunu dogrulamak](#browser-bundleinin-gercekten-temiz-oldugunu-dogrulamak)
- [@vscode/test-web ile test etmek](#vscodetest-web-ile-test-etmek)
- [Web'i ne zaman desteklememeli](#webi-ne-zaman-desteklememeli)

## Web extension host nedir

Masaustu VS Code eklentileri bir Node.js sureci icinde calistirir. **Tarayicida Node sureci yoktur** — VS Code'un kendisi bir sekmedeki JavaScript'tir ve eklentiler bir **Web Worker** icinde calisir. O worker, web extension host'tur.

Bunun fiilen calistigi yerler:

- **vscode.dev** — bir tarayici sekmesinde VS Code, arka uc yok.
- **github.dev** — herhangi bir GitHub deposunda `.` tusuna basmak.
- **Tarayici uzerinden erisilen GitHub Codespaces** (tarayici tarafindaki extension host; bir Codespace'in ayrica uzak bir Node host'u da vardir).
- Kullanicilara kurulum yerine bir tarayici URL'si verilen **gomulu/yonetilen VS Code kurulumlari**.

Bir sirketin bunu neden onemseyebilecegi:

- **Kurulumsuz inceleme ve duzenleme.** Bir inceleyici github.dev'de bir PR acar ve eklentinin sozdizimi destegi, dogrulamasi ve gezinmesi orada oylece vardir.
- **Kisitli makineler.** Kullanicilarin masaustu yazilim kuramadigi ortamlar yine de araci alir.
- **Ise alistirma ve demolar.** Bir baglanti, bir kurulumdan daha dusuk bir esiktir — ozellikle destekledigin bir DSL ya da config formatini degerlendiren bir musteri icin.
- **Pazar yeri listelemesinde erisim.** Web yetenekli eklentiler, web yetenekli olmayanlarin hic gorunmedigi tarayici baglamlarinda yuzeye cikar.

En onemli tek gercek: **web eklentileri tum VS Code API'sine sahiptir.** Komutlar, diller, tanilar, agac view'lari, webview'ler, dekorasyonlar, workspace duzenlemeleri, dosya sistemi API'si — hepsi mevcut. Kaybettigin sey **Node.js** ve onunla birlikte makineye dogrudan dokunma yetenegi. Iyi yazilmis bir eklentide fiilen cagirdigin API'nin cogu `vscode.*`'dir; tasimanin ilk gorundugunden daha sik mumkun olmasinin sebebi tam olarak budur.

## Manifest sekilleri

`main` Node giris noktasi, `browser` ise Web Worker giris noktasidir. Ikisi bir arada bulunabilir.

**Yalnizca masaustu** — geleneksel sekil:

```json
{
  "main": "./dist/node/extension.js",
  "engines": { "vscode": "^1.104.0" }
}
```

**Yalnizca web** — hic Node kodu yok. Saf dil destegi, mantik iceren temalar ya da TypeScript'te yazilmis formatlayicilar icin yaygin:

```json
{
  "browser": "./dist/web/extension.js",
  "engines": { "vscode": "^1.104.0" }
}
```

**Ikisi birden** — VS Code calistigi host'a uygun giris noktasini secer:

```json
{
  "main": "./dist/node/extension.js",
  "browser": "./dist/web/extension.js",
  "engines": { "vscode": "^1.104.0" },
  "capabilities": {
    "virtualWorkspaces": true
  }
}
```

Bilinmesi gereken iki davranis:

**VS Code bir eklentiyi web yetenekli sayar eger** manifest'te bir `browser` giris noktasi varsa **ya da** `main` yoksa **ve** su katkilardan hicbirini yapmiyorsa: `localizations`, `debuggers`, `terminal` veya typescript server plugin'leri. Ikinci dal onemlidir — bildirimsel-yalniz bir eklenti (bir tema, bir gramer, bir snippet paketi) kimse oyle olmasina karar vermeden web yetenekli olur ki bu dogrudur, cunku bozulacak bir kodu yoktur.

Ama ayni kural, mantigi *olan* ve sadece `main`'i atlayan bir eklentinin kazara web yetenekli siniflandirilabilecegi anlamina da gelir. Kod giris noktan yoksa bu sorun degil. Kodun varsa bir giris noktasini bilincli olarak beyan et.

**`vsce` web eklentilerini paketleme sirasinda manifest seklini temel alarak otomatik etiketler**, boylece pazar yeri listelemesi ekstra bayrak olmadan bunu yansitir. `web`, platforma ozgu paketleme icin gecerli bir `--target` degeridir; ancak bir web eklentisi icin `--target web`'in *zorunlu* mu yoksa sadece kullanilabilir mi oldugu varsayilacak bir sey degil — bir yayin betigine eklemeden once guncel `vsce` dokumanlarini kontrol et.

Bunu `capabilities.virtualWorkspaces` ile birlikte kullan. Tarayici baglamlari neredeyse her zaman sanal workspace'lerdir (github.dev dosyalari bir API'den gelir, diskten degil). `browser` beyan eden ama `virtualWorkspaces: false` diyen bir eklenti, calisacagi yerlerin cogunda kendi kendisiyle celisiyordur — incelemede isaretlemeye deger.

## Kisitlar ve her birinin nedeni

Asagidaki her kisit tek bir gercege dayanir: **kod Node'da degil bir Web Worker'da calisir.** Bir worker'in isletim sistemi tutamaci, surec tablosu, modul yukleyicisi yoktur ve tarayici tarafindan dayatilan bir ag politikasi vardir.

**`vscode` disinda hicbir seyin `require()`'u yok.** Host, `require('vscode')`'u cozen ve baska hicbir seyi cozmeyen bir `require` shim'i saglar. Modul cozumleme algoritmasi yok, `node_modules` aramasi yok, cozulecek bir dosya sistemi yok. Bagimliliklarin gonderilmeden once koduna paketlenmis olmali.

**`importScripts` yok, dinamik `import()` yok.** Sonuc olarak bundle **tek bir dosya** olmali. Kod bolme, tembel parcalar ve worker yukleme numaralari hepsi bozulur. Daha buyuk bir eklentiyi tasiyan bir ekibi en cok sasirtan kisit budur: birkac parca ureten bir derleme yalnizca suboptimal degildir, hic calismaz.

**Node global'leri yok.** `process`, `os`, `path`, `util`, `url`, `setImmediate` yoktur. `process.env` yoktur cunku surec yoktur. `path` yoktur cunku uygulanacak bir isletim sistemi yol semantigi yoktur — ve dikkat, yol *string* manipulasyonu sorun degildir; sorun, `path` icin bir bundler polyfill'inin POSIX yolu olmayan URI'ler icin sana sessizce POSIX semantigi vermesidir.

**Alt surec yok.** `child_process` yok, `spawn`, `exec` ya da `fork` yok. Bir worker isletim sistemi sureci olusturamaz. Bu mutlaktir ve bir tasimanin hic mumkun olup olmadigina karar veren kisittir.

**Dogrudan dosya sistemi erisimi yok.** `fs` yok. `vscode.workspace.fs` kullan; o, workspace'e hizmet eden `FileSystemProvider` ne ise onun uzerinden yonlendirir — github.dev'de GitHub API'si, baska yerde bellek ici bir saglayici. Bu masaustunde bile gercek bir iyilesmedir: `workspace.fs`, `fs`'in calismadigi sanal workspace'lerde calisir.

**Ag, Fetch API uzerinden ve CORS uyumlu kaynaklara karsi.** Node `http`/`https` modulleri gitti; `fetch` mevcut. CORS kismi gercek kisittir ve VS Code tarafindan degil tarayici tarafindan dayatilir: masaustu eklentinden gayet iyi calisan bir API, sunucu izin verici CORS basliklari gondermedikce tarayicida engellenir. Bunu eklenti kodundan duzeltemezsin. Bir tasimaya baglanmadan once bagimli oldugun uc noktalari dogrula.

**Webview'ler buyuk olcude ayni davranir.** Webview icerigi her iki host'ta da bir iframe'dir, bu yuzden webview agirlikli arayuz cogu zaman bir eklentinin en tasinabilir kismidir — yeter ki mesaj kanalinin eklenti tarafi webview adina Node isi yapmiyor olsun.

## Tasima haritasi: Node deseninden web karsiligina

| Node deseni | Web karsiligi | Notlar |
|---|---|---|
| `fs.readFile` / `readFileSync` | `await vscode.workspace.fs.readFile(uri)` | `Uint8Array` dondurur. `new TextDecoder().decode(bytes)` ile coz. |
| `fs.writeFile` | `await vscode.workspace.fs.writeFile(uri, bytes)` | `new TextEncoder().encode(text)` ile kodla. |
| `fs.readdir` | `await vscode.workspace.fs.readDirectory(uri)` | `[name, FileType][]` dondurur. |
| `fs.stat` / `existsSync` | `await vscode.workspace.fs.stat(uri)` | Yoksa `FileSystemError.FileNotFound` firlatir — o reddetme *varlik kontrolunun kendisidir*. |
| `fs.mkdir` | `await vscode.workspace.fs.createDirectory(uri)` | Ara dizinleri olusturur. |
| `path.join` | `vscode.Uri.joinPath(baseUri, ...segments)` | Semalar arasi dogru; URI string'lerini asla birlestirme. |
| `path.dirname` / `basename` | `Uri.joinPath(uri, '..')`; `uri.path.split('/').pop()` | `uri.path` uzerinde calis, asla `uri.fsPath` uzerinde. |
| `uri.fsPath` | `uri.toString()` ya da `uri.path` | `fsPath` sanal bir workspace'te string dondurur ama acilabilir degildir. |
| `child_process.spawn` / `exec` | **Mumkun degil.** | Barindirilan bir servis, aracin WASM derlemesi ya da TypeScript'te yeniden yazim gerekir. Bkz. [Web'i ne zaman desteklememeli](#webi-ne-zaman-desteklememeli). |
| `process.env.FOO` | `vscode.workspace.getConfiguration()` ya da `context.secrets` icinde bir gizli bilgi | Ortam yok. Onu bir ayara donustur. |
| `process.platform` | Uygulanamaz | Calisma aninda degil derleme aninda host'a gore dallan. |
| `os.homedir` / `tmpdir` | `context.globalStorageUri` / `context.storageUri` | Eklenti kapsamli depolama, her iki host'ta calisir. Masaustunde de bunlari tercih et. |
| `crypto` (Node) | Web Crypto: `crypto.subtle`, `crypto.getRandomValues` | `subtle` asenkrondur. `crypto.randomUUID()` ikisinde de mevcut. |
| `Buffer` | `Uint8Array`, `TextEncoder`, `TextDecoder` | Masaustunde de daha temiz; `Buffer` ihtiyacin olmayan Node'a ozgu bir yuzeydir. |
| `http` / `https` / `axios` (Node adaptoru) | `fetch` | Uc noktalar CORS basliklari gondermeli. |
| `setImmediate` | `queueMicrotask` ya da `setTimeout(fn, 0)` | Ayni zamanlama degil, nadiren belirleyici. |
| Calisma aninda `require('./thing')` | Bundle aninda cozulen statik `import` | Hicbir turde calisma zamani modul yuklemesi yok. |

Kullanisli bir yan etki: **bu degisimlerin cogu masaustu icin de daha iyidir.** `workspace.fs` sanal workspace'leri kaldirir, `Uri.joinPath` `file` disi semalari kaldirir, `globalStorageUri` kullanicinin tasinabilir kurulumuna saygi gosterir. Web'e tasima siklikla gizli masaustu hatalarini duzeltir.

## Paylasilan kaynak, platform dallari

Hedef, tek bir kod tabaninin iki bundle uretmesi ve platform farklarinin ozellik koduna dagilmak yerine bir arayuzun arkasinda izole edilmesidir.

Standart yerlesim uc dizindir:

```
src/
  common/
    extension.ts        # paylasilan activate() mantigi, ozellik kaydi
    fileSystem.ts       # arayuz, uygulama degil
    linter.ts           # ozellik kodu — yalnizca arayuzu import eder
  node/
    extension.ts        # `main` icin giris: Node uygulamalarini kurar, common'i cagirir
    nodeProcessRunner.ts
  browser/
    extension.ts        # `browser` icin giris: web uygulamalarini kurar, common'i cagirir
    webProcessRunner.ts
```

**Bunu isleten kural: `src/common/` asla `src/node/` ya da `src/browser/`'dan import etmemeli.** Bagimliliklar iceri dogru gosterir. Common'in platforma gore degisen bir yetenege ihtiyaci varsa bir arayuz beyan eder ve bir uygulama alir.

Degisen yetenegi tanimla:

```typescript
// src/common/toolRunner.ts
export interface ToolRunner {
  /** Analiz aracini `content` uzerinde calistirir ve ham ciktiyi dondurur. */
  run(content: string, fileName: string): Promise<string>;
}
```

Paylasilan aktivasyon platform parcalarini argüman olarak alir:

```typescript
// src/common/extension.ts
import * as vscode from 'vscode';
import type { ToolRunner } from './toolRunner';

export interface PlatformServices {
  toolRunner: ToolRunner;
}

export function activateShared(
  context: vscode.ExtensionContext,
  services: PlatformServices
) {
  const diagnostics = vscode.languages.createDiagnosticCollection('mylang');
  context.subscriptions.push(diagnostics);

  context.subscriptions.push(
    vscode.workspace.onDidSaveTextDocument(async doc => {
      if (doc.languageId !== 'mylang') return;
      const output = await services.toolRunner.run(doc.getText(), doc.fileName);
      diagnostics.set(doc.uri, parseDiagnostics(output));
    })
  );
}
```

Node giris noktasi — gercek binary'yi baslatir:

```typescript
// src/node/extension.ts
import * as vscode from 'vscode';
import { execFile } from 'child_process';
import { promisify } from 'util';
import { activateShared } from '../common/extension';
import type { ToolRunner } from '../common/toolRunner';

const execFileAsync = promisify(execFile);

const nodeToolRunner: ToolRunner = {
  async run(content, fileName) {
    const { stdout } = await execFileAsync('mylint', ['--stdin', fileName], {
      // gercek kodda icerigi stdin uzerinden gecir
    });
    return stdout;
  }
};

export function activate(context: vscode.ExtensionContext) {
  activateShared(context, { toolRunner: nodeToolRunner });
}
```

Browser giris noktasi — ayni yetenek, farkli sekilde elde edilmis:

```typescript
// src/browser/extension.ts
import * as vscode from 'vscode';
import { activateShared } from '../common/extension';
import type { ToolRunner } from '../common/toolRunner';
import { analyzeInProcess } from '../common/pureAnalyzer';

const webToolRunner: ToolRunner = {
  async run(content, fileName) {
    // Secenek A: her yerde calisan bir TypeScript yeniden yazimi.
    return analyzeInProcess(content, fileName);

    // Secenek B: CORS destekli, barindirilan bir servis.
    // const res = await fetch('https://lint.example.com/analyze', {
    //   method: 'POST',
    //   headers: { 'content-type': 'application/json' },
    //   body: JSON.stringify({ content, fileName })
    // });
    // if (!res.ok) throw new Error(`Lint service failed: ${res.status}`);
    // return await res.text();
  }
};

export function activate(context: vscode.ExtensionContext) {
  activateShared(context, { toolRunner: webToolRunner });
}
```

Ikisini de esbuild ile derle, web bundle'i icin `platform: 'browser'` ve **`format: 'cjs'` ile tek cikti dosyasi** — kod bolme kapali kalmali:

```javascript
// esbuild.js
const esbuild = require('esbuild');

const shared = {
  bundle: true,
  external: ['vscode'],   // HER IKI hedefte de host tarafindan saglanir
  minify: true,
  sourcemap: true,
  format: 'cjs'
};

Promise.all([
  esbuild.build({
    ...shared,
    entryPoints: ['src/node/extension.ts'],
    outfile: 'dist/node/extension.js',
    platform: 'node'
  }),
  esbuild.build({
    ...shared,
    entryPoints: ['src/browser/extension.ts'],
    outfile: 'dist/web/extension.js',
    platform: 'browser',
    // Node polyfill'lerini `inject` etme. Derleme eksik bir Node modulu
    // yuzunden basarisiz oluyorsa bu gercek bir bulgudur — import'u duzelt,
    // polyfill ekleme.
  })
]).catch(() => process.exit(1));
```

## Browser bundle'inin gercekten temiz oldugunu dogrulamak

**Basarili bir derleme kanit degildir.** Bu dosyadaki en onemli operasyonel nokta budur.

Bundler'lar tasarim geregi musamahakardir. Yapilandirma ve eklentilere bagli olarak, bagimlilik agacindaki bir Node import'u sessizce yalnizca cagrildiginda hata firlatan bir shim ile degistirilebilir, farkli semantige sahip bir tarayici polyfill'ine cozulebilir ya da bos bir module stub'lanabilir — boylece `fs.readFile` `undefined` olur ve `TypeError: fs.readFile is not a function` alirsin: kullanicinin tarayici sekmesinde, testlerinin denemedigi bir kod yolunda.

Daha kotusu, sorunlu import genelde senin kaynaginda degil **gecisli bir bagimlilikta** olur. `src/` denetimi hicbir sey bulmaz.

Uretilen ciktida ara:

```bash
# Web bundle'inda asla gorunmemesi gereken Node built-in'leri.
grep -nE "require\(['\"](fs|path|os|child_process|crypto|http|https|net|tls|stream|zlib|util|url)['\"]\)" \
  dist/web/extension.js

# Bundle'dan sag cikan Node global'leri.
grep -nE "\b(process\.(env|platform|cwd)|__dirname|__filename|setImmediate|Buffer\.)" \
  dist/web/extension.js

# Yasak dinamik yukleme — tek dosya kurali.
grep -nE "\b(importScripts|import\()" dist/web/extension.js
```

Sonuclari okumak dikkat ister, cunku minify edilmis bundle'lar gurultu uretir:

- **`require('vscode')` beklenir ve dogrudur.** Host shim'i onu saglar.
- **Paketlenmis bir kutuphanenin icindeki `process.env.NODE_ENV`** yaygin bir yari-yanlis-pozitiftir. Yalnizca derlemen onu tanimlayarak yok ediyorsa (`define: { 'process.env.NODE_ENV': '"production"' }`) guvenlidir; aksi halde calisma aninda hata firlatir. Hangi durumda oldugunu el sallayarak gecmek yerine dogrula.
- **Hata mesajlarindaki string sabitleri** bu desenlerle zararsizca eslesebilir. Yalnizca satir sayisina degil, cevresindeki koda bak.
- **Bundler tarafindan satir ici hale getirilmis polyfill'lenmis bir `path` modulu** `require('path')` ile eslesmez — satir ici fonksiyon govdeleri olarak gorunur. `grep`'in bir kanit degil bir tarama olmasinin sebebi budur.

Ikinci bir sinyal olarak bir boyut kontrolu ekle. Node'unkinden dramatik olarak daha buyuk bir web bundle'i genelde polyfill'lerin iceri girdigi anlamina gelir:

```bash
ls -la dist/web/extension.js dist/node/extension.js
```

**Tek gercek kanit onu calistirmaktir.** `grep` bariz durumlari ucuza yakalar; `@vscode/test-web` gerisini yakalar.

## @vscode/test-web ile test etmek

`@vscode/test-web` bir VS Code web derlemesini indirir, **localhost:3000** uzerinde sunar ve eklentini tarayici host'una yukler — bir simulasyon degil, gercek ortam.

Bir test verisi klasorune karsi calistir:

```bash
npx @vscode/test-web --extensionDevelopmentPath=$(pwd) ./test-data
```

Tarayici motorunu sec:

```bash
npx @vscode/test-web \
  --browserType=chromium \
  --extensionDevelopmentPath=$(pwd) \
  ./test-data
```

`--browserType`, `chromium`, `firefox` ve `webkit` kabul eder. Yeni web platformu ozelliklerine dayaniyorsan birden fazlasinda test et — worker ve Fetch davranisi kenarlarda farklilasir.

Derlemenin yanina `package.json`'a bagla:

```json
{
  "scripts": {
    "compile-web": "node esbuild.js",
    "open-in-browser": "npm run compile-web && vscode-test-web --extensionDevelopmentPath=. ./test-data"
  },
  "devDependencies": {
    "@vscode/test-web": "^0.0.60"
  }
}
```

Acildiginda fiilen ne denenmeli:

1. **Eklentinin hic aktive olup olmadigi.** Bundle'dan sag cikan bir Node import'u genelde aktivasyon sirasinda hata firlatir; eklenti oylece hic baslamaz. Tarayici devtools konsolunu kontrol et — worker'in hatalari bir VS Code cikti kanalina degil oraya duser.
2. **Dosyalara dokunan her kod yolu.** test-data klasoru bir `FileSystemProvider` uzerinden sunulur, bu yuzden geride kalmis bir `fs` cagrisi ya da bir `fsPath` varsayimi burada yuzeye cikar.
3. **Her ag cagrisi.** CORS hatalari yalnizca gercek bir tarayicida gorunur.
4. **Paletteki komutlar**, onemsiz oldugunu varsaydiklarin dahil.

Otomatik testler de bu ortamda calistirilabilir, ancak kurulum masaustu `@vscode/test-electron`'dan daha agirdir. Burada elle dogrulama bile temiz bir derlemeden cok daha degerlidir, cunku derlemenin hic kontrol etmedigi worker sinirini dener.

## Web'i ne zaman desteklememeli

**Eklentinin cekirdek degeri yerel binary'ler calistirmayi gerektiriyorsa, web destegi yamayla elde edilemez.** Bunu isin basinda soyle, iki gunluk bundler hata ayiklamasindan sonra degil.

Cevabin basitce hayir oldugu durumlar:

- Eklenti bir CLI aracinin sarmalayicisinin **kendisidir** — bir derleyici, bir formatlayici binary'si, bir paket yoneticisi, VS Code'un yerlesik olarak sundugunun otesinde bir surum kontrol istemcisi.
- **Yerel bir yurutulebilir olarak dagitilan bir dil sunucusuna** ihtiyaci var. (TypeScript'te yazilmis ya da WASM'a derlenmis bir dil sunucusu bambaska bir hikaye ve calisabilir.)
- **Workspace disina** okuyor ya da yaziyor — ev dizinindeki dotfile'lar, sistem yapilandirmasi, yerel bir veritabani.
- Port ya da unix soketi uzerinden **yerel calisan servislerle** entegre oluyor.
- **Yerel Node modullerine** (`.node` eklentileri) bagimli. Bunlar bir worker icin hic paketlenemez.

Bir paydas icin durust cerceve: **bu bir derleme yapilandirmasi degil, yapisal bir karardir.** Web host'un surec tablosu yoktur. Bir tane yaratan bir bayrak, polyfill ya da bundler ayari yoktur. Ileriye donuk yollarin hepsi kendi baslarina ciddi projelerdir:

- **Aracin mantigini TypeScript'te yeniden yaz.** Bir ayristirici ya da formatlayici icin uygulanabilir, bir derleyici icin degil.
- **Araci WebAssembly'e derle.** Gercek, giderek yayginlasan ve kendi dosya-sistemi-shim sorunlariyla birlikte gelen ciddi bir is parcasi.
- **Isi, eklentinin `fetch` ile cagirdigi barindirilan bir servise tasi.** Artik bir servisin, kullanilabilirliginin, CORS yapilandirmasinin ve kullanici kodunu ona gondermenin gizlilik sorusunun sahibisin.
- **Kucultulmus bir web derlemesi gonder** — cogu ekibin ulastigi sekil budur. Surec ici calisabilen sozdizimi, gezinme, bicimlendirme ve dogrulama web'e gider; binary gerektiren her sey durustce beyan edilerek masaustune ozel kalir.

Bu son secenek, yukaridaki cift-giris-noktali manifest'in ve `PlatformServices` deseninin var olma sebebidir. Mesru ve yaygin bir sonuctur ve kurulup sonra basarisiz olan bir web bundle'indan cok daha iyidir.

Buna soyutlama katmanini yazmadan **once** karar ver. Olgunlasmis bir kod tabanina sonradan bir `ToolRunner` arayuzu gecirmek pahalidir; sonrasinda web uygulamasinin asla var olamayacagini kesfetmek o masrafi tamamen israfa cevirir. Once cevaplanacak soru "web icin nasil derleriz" degil, "eklentimiz surec olmadan ne yapabilir, yapabiliyorsa" sorusudur.
