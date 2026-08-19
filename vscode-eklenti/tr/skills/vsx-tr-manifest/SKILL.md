---
name: vsx-tr-manifest
description: VS Code eklenti manifest'i (package.json) kanonu — activationEvents ve otomatik uretimi, katki noktalari (contributes), engines/@types eslemesi, guvenilmeyen ve sanal workspace'ler icin capabilities beyanlari, main ve browser giris noktalari ve pazar yeri metadata alanlari. Bu skill'i package.json yazilirken, genisletilirken, incelenirken ya da hata ayiklanirken ac — bir komut, view, ayar, menu ya da kisayol eklenirken, aktivasyon stratejisi secilirken ya da duzeltilirken, bir katki sessizce gorunmedigi zaman, workspace guveni ya da web destegi beyan edilirken ve paketleme ya da yayin oncesinde. Uc agent de (mimar, gelistirici, qa-yayinci) bu dosyayi paylasir.
---

# Eklenti Manifest'i

`package.json` bir eklentideki en sonuc dogurucu dosyadir. Yazdigin kod ile editorun beklentilerinin bulustugu tek yerdir ve **sessizce basarisiz olur**: bozuk bir katki noktasi hata firlatmaz, sadece hic gorunmez. Bu skill'in var olma sebebi ve asagidaki disiplinin cabaya degmesinin nedeni tam olarak bu ozelliktir.

Uc agent de bu dosyaya dokunur — mimar olusturur, gelistirici ozelliklerin yanina girdi ekler, qa-yayinci gondermeden once dogrular — bu yuzden kanon uc yerde degil burada bir kez yasar.

**Yazmadan once semayi guncel dokumana karsi dogrula.** Manifest referansi `code.visualstudio.com/api/references/extension-manifest`, katki noktalari ise `.../contribution-points` adresinde. Burada bir alanin seklini tahmin etmek, bir ogle sonrasini kaybetme yontemidir.

## Aktivasyon olaylari

Bir eklenti hareketsiz baslar. `activationEvents` — arti asagida anlatilan otomatik uretilenler — VS Code'un onu ne zaman uyandiracagina karar verir. Aktivasyonunun her milisaniyesi, kullanicinin editor acilisindan bir milisaniyedir ve bu sure kurulu diger tum eklentilerle paylasilir. Kontrol ettigin en buyuk performans kaldiraci budur.

### Otomatik uretim: zaten ima edileni listeleme

**VS Code 1.74'ten beri** aktivasyon olaylari **`contributes`'tan otomatik uretilir**. `contributes.commands` icinde bir komut beyan ediyorsan, ayrica onun icin `onCommand:` yazmazsin. Otomatik uretilen set: `onCommand`, `onLanguage`, `onView`, `onCustomEditor`, `onAuthenticationRequest` ve — 1.76'dan beri — `onTaskType`.

Icsellestirilmeye deger bir sonuc: **modern bir manifest'in `activationEvents` dizisi cogu zaman mesru olarak bostur ya da hic yoktur.** `contributes.commands`'i aynalayan `onCommand:` girdileriyle dolu bir dizi, manifest'in 1.74 oncesi bir sablondan kopyalandiginin guvenilir isaretidir. Hata degildir, ama *bilincli olan* olaylari gizleyen gurultudur.

Hala acik girdi gerektiren olaylar: `workspaceContains:`, `onStartupFinished`, `onFileSystem:`, `onDebug` ve digerleri. Bkz. `references/aktivasyon.md`.

### Ise yarayan en dar olayi secmek

En iyiden en kotuye:

- **Bir katkidan otomatik uretilen** — eklenti, kullanici o seyi fiilen cagirdiginda uyanir. Ideal.
- **`workspaceContains:<glob>`** — yalnizca ilgili dosyayi gercekten iceren workspace'lerde uyanir. Cogu projede alakasiz olan araclar icin mukemmel.
- **`onLanguage:<id>`** — o dilden bir dosya acildiginda uyanir.
- **`onStartupFinished`** — editor acilisini tamamladiktan sonra uyanir. Dogal bir tetigi olmayan arka plan isleri icin. Acilisi geciktirmez; `*`'in kabul edilemez oldugu yerde bunu kabul edilebilir yapan da budur.
- **`*`** — her seferinde, her pencerede, acilis sirasinda uyanir. Gorundugu cogu durumda kastedilen davranis aslinda `onStartupFinished`'dir.

`*` sadece onerilmemekle kalmaz — **`vsce package` `--allow-star-activation` verilmedikce onunla derlemeyi reddeder.** O bayraga uzanmayi bir cozum degil, yeniden dusunme sinyali say. Gercekten gerekiyorsa, raporunda daha darinin neden ise yaramadigini soyle; ifade edemiyorsan yanlis secimdir.

## Katki noktalari (contributes)

`contributes`, eklentinin editore ne kattigini beyan eder: komutlar, menuler, view'lar, viewsContainers, configuration, keybindings, languages, grammars, snippets, walkthroughs ve digerleri.

En yaygin sessiz basarisizligi onleyen kural:

> **Kod ve manifest girdisi tek bir is birimidir, asla iki ayri is degil.**

`vscode.commands.registerCommand` ile kaydedilmis ama `contributes.commands` icinde olmayan bir komut, komut paletinde gorunmez. `getConfiguration()` ile okunan ama `contributes.configuration` semasi olmayan bir ayar, Settings arayuzunde gorunmez, dogrulama almaz ve kesfedilebilir bir varsayilani olmaz. Ikisi de hata vermez. Sadece calismazlar ve gelistirici dogru gorunen koda bakip kalir.

Tersi de onemli: kayitli bir handler'i olmayan bir `contributes.commands` girdisi, tiklandiginda hata firlatan bir palet ogesi uretir.

Bunun otesinde icsellestirmeye deger iki sey:

- **`contributes.menus`, `contributes.commands`'tan ayridir.** Bir komutu beyan etmek onu var eder; menu yerlesimi ise komut paletinde mi, editor baslik cubugunda mi, dosya gezgini baglam menusunde mi yoksa hicbir yerde mi gorunecegine karar verir. Gorunurlugu `when` ifadeleri kontrol eder — bkz. `references/katki-noktalari.md`.
- **Bir katkiyi beyan etmek ucuzdur; aktive olmak degil.** Cogu katki bildirimseldir ve cagrilana kadar hicbir sey harcamaz. Birkaci erken aktivasyona zorlar. Hangisini ekledigini bil.

Katki basina semalar, `when` ifadesi baglam anahtarlari ve menu grup siralamasi `references/katki-noktalari.md` icinde.

## engines.vscode ve @types/vscode

Bu ikisi uyusmak zorunda ve kuralin yonu onemli:

- **`engines.vscode`**, eklentinin destekledigi *en dusuk* VS Code surumudur. Daha eski surumdeki bir kullaniciya eklenti onerilmez.
- **`@types/vscode`**, `engines.vscode` ile **ayni surum ya da daha eski** olmalidir.

Bunun onledigi hata: beyan ettigin engine'den daha yeni tipler, destekledigini iddia ettigin en eski surumde var olmayan bir API'ye karsi derleme yapmana izin verir. Temiz derlenir ve gercek bir kullanicinin makinesinde calisma aninda patlar. `vsce` bu eslemeyi paketleme aninda kontrol eder.

Pratikte ikisini de ayni minor surumle beyan et:

```json
"engines": { "vscode": "^1.104.0" },
"devDependencies": { "@types/vscode": "^1.104.0" }
```

Onemli iki ayrinti:

- **`^1.8.0` "1.8.0 ve sonrasi" demektir; ciplak `1.8.0` yalnizca o surum demektir.** Gercekten sabitlemek istemiyorsan caret kullan.
- **`@types/vscode`, yayinlanan VS Code surumunun gerisinde kalir.** "En son tipler" ve "en son VS Code" farkli sayilardir, bu yuzden engine tabanini urun surumunden cikarma.

`engines.vscode`'u, fiilen kullandigin her API'yi iceren en eski surume ayarla — "en son"a degil, ve simdi cagirdigin bir API'yi engelleyen bayat bir sablon degerine de degil.

## capabilities: guven ve sanal workspace'ler

`capabilities`, eklentinin iki kisitli baglamda nasil davrandigini beyan eder. **Bunlari atlarsan varsayilanlar kabul edilir ve kabul edilen varsayilan her zaman guvenli olan degildir** — bilincli olarak beyan et.

- **`untrustedWorkspaces`** — kullanicinin henuz guvenmedigi klasorler icin VS Code'un girdigi Restricted Mode'daki davranis. Bu onemlidir cunku guvenilmeyen bir depoyu acmak, o deponun kod calistirmasina izin vermemelidir. Eklenti workspace'ten bir sey calistiriyorsa (bir linter binary'si, config'te belirtilmis bir komut), guvenilmeyen ortamda guvenli degildir.
- **`virtualWorkspaces`** — workspace gercek bir diskte olmadiginda (uzaktan acilan GitHub depolari, diger sanal dosya sistemleri) davranis. Node `fs` yollari kullanan ya da workspace dosyalarina karsi surec baslatan hicbir sey burada calismaz.

Ikisi de destegi `true`, `false` ya da `"limited"` olarak ifade eder:

```json
"capabilities": {
  "untrustedWorkspaces": {
    "supported": "limited",
    "description": "Workspace'e guvenilene kadar yalnizca sozdizimi ozellikleri kullanilabilir.",
    "restrictedConfigurations": ["myExt.formatterPath"]
  },
  "virtualWorkspaces": {
    "supported": false,
    "description": "Linter'in calismasi icin dosyalarin diskte olmasi gerekiyor."
  }
}
```

Sekillerin acikca gostermedigi uc sey:

- **`supported` degeri `false` ya da `"limited"` oldugunda `description` zorunludur** — kullaniciya gosterilir, o yuzden onun icin yaz.
- **`restrictedConfigurations`**, guven verilene kadar *workspace tarafindan saglanan* degerleri yok sayilacak ayar ID'lerini listeler. Calistirilan bir yurutulebiliri ya da bir yolu adlandiran her ayar buraya aittir.
- **`virtualWorkspaces` ayrica ciplak bir boolean da kabul eder** (`"virtualWorkspaces": true`) ve `restrictedConfigurations` alani yoktur. Belirtilmediginde `true` varsayilir — gercek dosyalara ihtiyaci olan bir eklentinin bilincli olarak `false` beyan etmesi gerekmesinin sebebi budur.

Daha fazlasi `references/yetenekler.md` icinde.

Bunlari **kodun fiilen ne yaptigina gore durustce** beyan et. Yanlis bir `untrustedWorkspaces: true` bir guvenlik yanlis beyanidir ve tam olarak pazar yeri incelemesinin yakaladigi — ya da daha kotusu, yakalamadigi — turden bir seydir.

## main, browser ve web extension host

- **`main`** — masaustu VS Code icin Node.js giris noktasi. Tum Node API'si mevcut.
- **`browser`** — vscode.dev ve github.dev icin Web Worker giris noktasi.

Web eklentileri **tum VS Code API'sini** korur ama Node'u tamamen kaybeder. Bir browser bundle'inda kullanilamayanlar: `fs`, `child_process` ve Node global'leri `process`, `os`, `path`, `util`, `url`, `setImmediate`. Yurutulebilir baslatmak yok, dogrudan dosya sistemi erisimi yok (`workspace.fs` kullan) ve ag cagrilari CORS'a izin veren uc noktalara karsi `fetch` ile yapilmali. Bundle ayrica **tek bir dosya** olmalidir — `importScripts` ve dinamik import'lar calismaz, `require()` shim'i yalnizca `require('vscode')`'u cozer.

Bu, ozellik kodunda yamayla gecistirilecek bir sey degil yapisal bir kisittir. Bir binary'yi calistiran bir ozellik, web host'la basitce uyumsuzdur; etrafindan dolasmak yerine catismayi isaretle.

Bir eklenti her iki giris noktasini da beyan edip kaynagi platform dallariyla paylasabilir. VS Code'un bir eklentiyi web yetenekli saydigi durum: `browser` girdisi varsa **ya da** `main` yoksa ve `localizations`, `debuggers`, `terminal` veya typescript server plugin'lerinden hicbirini katmiyorsa — yani bir eklenti kimse oyle olmasina karar vermeden web yetenekli olarak yuzeye cikabilir. Bkz. `references/web-eklentileri.md`.

## Pazar yeri metadata'si

Halka acik yayinlarken zorunlu ya da fiilen zorunlu; yalnizca ic kullanim icin istege bagli (bkz. `vsx-tr-davranis` icindeki titizlik kadrani):

- `publisher` — pazar yeri publisher ID'nizle tam olarak eslesmeli.
- `name`, `displayName`, `description`, `version` — surum duz `major.minor.patch` olmali; **`1.2.0-beta` gibi semver on-surum etiketleri desteklenmez** (bunun yerine `vsce publish --pre-release` kullan).
- `icon` — **PNG, en az 128×128. SVG ikonlar reddedilir.**
- `categories`, `keywords` — kesfedilebilirlik.
- `repository` — yoklugu paketleme aninda `--allow-missing-repository` gerektirir.
- `license` / `LICENSE` dosyasi — yoklugu `--skip-license` gerektirir.
- `README.md` — bu dosya pazar yeri listeleme sayfasinin *kendisidir*. Gorseller HTTPS uzerinden sunulmali ve guvenilir rozet saglayicilari disinda SVG yasaktir.

Yayinlama mekanigi ve yayin oncesi kontrol listesi `vsx-tr-yayin`'a aittir; bu bolum yalnizca manifest icinde yasayani kapsar.

## Bir manifest'i incelemek

Dogrularken (ozellikle qa-yayinci) sunlari bu sirayla kontrol et — tekrar eden gercek hatalari yakalayanlar bunlar:

1. Her `contributes.commands` girdisinin kayitli bir handler'i var ve her kayitli komutun bir girdisi var.
2. Kodda `getConfiguration()` ile okunan her anahtar `contributes.configuration` icinde mevcut.
3. `@types/vscode`, `engines.vscode`'dan yeni degil.
4. `capabilities` kodun fiilen yaptigini yansitiyor.
5. Gerekce belirtilmemis `*` aktivasyonu yok.
6. `browser` beyan edilmisse, o bundle'dan Node'a ozgu hicbir API'ye erisilemiyor.
7. Yayinlama: `publisher`, `icon`, `repository`, `license`, README mevcut.

## Referanslar

- `references/aktivasyon.md` — otomatik uretim kurallari, tam olay listesi, acilis performansi.
- `references/katki-noktalari.md` — katki basina semalar, `when` ifadeleri, menu gruplari.
- `references/yetenekler.md` — guven ve sanal workspace beyanlari.
- `references/web-eklentileri.md` — cift hedefli derlemeler ve Node API kisitlari.
