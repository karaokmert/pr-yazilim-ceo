---
name: vsx-tr-api
description: VS Code Extension API ozellik isi icin uygulama kanonu — komutlar, dil ozelligi provider'lari (hover, completion, code action, CodeLens, definition, formatting, diagnostics), agac view'lari, webview'ler ve CSP/mesaj koprusu, workspace ve dosya sistemi erisimi, configuration ve state, gizli bilgiler, iptal ve ilerleme, dis surec entegrasyonu. Bu skill'i vscode API'sine karsi TypeScript ile eklenti ozellik kodu yazarken ya da hata ayiklarken ac — bir komut eklerken, bir provider ya da kenar cubugu view'i insa ederken, bir webview paneli olustururken, ayarlari okurken ya da state'i kalici hale getirirken, dokuman ve editorleri ele alirken ya da bir provider'in neden bayat veri dondurdugunu veya bir webview'in neden bos render edildigini arastirirken.
---

# Extension API Uygulama Desenleri

Bu gelistiricinin calisma kanonu. `vscode` namespace'ine karsi ozelliklerin nasil dogru insa edilecegini kapsar; agirlik API'nin keskin kenarlarinda — makul gorunen kodun yalnizca baskasinin makinesinde ortaya cikan sekillerde yanlis oldugu yerlerde.

Bu kodla eslesen manifest girdileri `vsx-tr-manifest` icinde. **Buradaki her ozelligin bir manifest yarisi vardir; birlikte gonderilirler ya da ozellik calismaz.**

Tum ekip icin gecerli sahiplik kurallari — dispose, gizli bilgiler ve yokluk yonetimi — `vsx-tr-davranis` icinde kanondur. Once onu oku; bu skill onu varsayar ve yeniden ifade etmek yerine asagida belirli API yuzeylerine uygular.

**Hafizaya guvenmeden once imzalari kontrol et.** Provider arayuzleri ve webview API'leri surumler arasinda kaydi. Yakin zamanda kullanmadigin her seye bak.

## Her seyin altindaki ozellik

**Paylasilan bir surecte misafirsin.** Extension host, senin kodunu kullanicinin kurdugu diger tum eklentilerle yan yana calistirir. Onun olay dongusunu tikarsan *onlarin* editorunu dondurursun. Bir dinleyici sizdirirsan bedelini *onlar* oder. `vsx-tr-davranis` icindeki dispose disiplininin ve asagidaki asenkron desenlerin birer stil tercihi olmamasinin sebebi budur — paylasilan bir sureci kullanilabilir tutan seylerdir.

`vsx-tr-davranis` sahiplik kurallarinin bu API yuzeyi icin acikca adlandirmaya deger iki uygulamasi:

- **Burada neyin `Disposable` sayildigi**: komut kayitlari, provider'lar, dinleyiciler, watcher'lar, durum cubugu ogeleri ve tani koleksiyonlari birer tane dondurur. Her biri olusturuldugu anda sahiplenilir — kuralin kendisi icin `vsx-tr-davranis`a bak.
- **Bu API'de "yokluk"un neye benzedigi**: aktif editor yok, workspace klasoru yok, cok koklu workspace, kaydedilmemis dokuman, bos secim. `workspace.workspaceFolders` `undefined` olabilir ya da bircok girdisi olabilir — `workspaceFolders[0]`, tek bir dosya acan kullaniciyi bekleyen bir cokmedir.

## Komutlar

`vscode.commands.registerCommand` ile kaydet, dispose edilebiliri it ve `contributes.commands` girdisini ayni degisiklikte ekle.

Handler'lar *neden* cagrildiklari konusunda hicbir sey varsaymamali. Bir komut palette, bir kisayoldan, bir menuden ya da `executeCommand` cagiran baska bir eklentiden tetiklenebilir — yani bekledigin aktif editor var olmayabilir. Hata firlatmak yerine kontrol et ve net bir mesajla nazikce geri cekil.

Bir komut yalnizca aktif bir editorle anlamliysa `registerTextEditorCommand` daha iyi secimdir: VS Code editoru ve edit builder'i saglar ve editor-yok durumunu senin icin ele alir.

## Dil ozelligi provider'lari

Provider'lar bir arayuzu uygular, bir `DocumentSelector`'a karsi kaydedilir ve *VS Code tarafindan*, kendi takviminde cagrilir — seninkinde degil. Her seyi belirleyen iki sonuc:

**Bekledigin den cok daha sik cagrilirlar.** Hover fare hareketiyle tetiklenir; completion neredeyse her tus vurusunda. Cagri basina pahali is yapan bir provider, yazmayi bozuk hissettirir. Onbellekle, geciktir ve sicak yolu ucuz tut.

**Iptal gercektir ve saygi gosterilmelidir.** Her provider bir `CancellationToken` alir. Kullanici devam ettiginde VS Code iptal eder — ve token'i yok sayarsan terk edilmis isin hala olay dongusu icin yarisir.

Iptale saygi gostermek, sonucu sonda atmak degil, *alttaki isi durdurmak* demektir:

```ts
async provideCompletionItems(doc, pos, token) {
  const results = await this.expensiveLookup(doc, pos, token); // token asagi gecirildi
  if (token.isCancellationRequested) { return undefined; }
  return results;
}
```

Her `await`'ten sonra token'i kontrol et ve gercekten iptal olsunlar diye alt sureclere ve ag cagrilarina isle. `undefined` dondurmek, bir provider'in "sunacak bir seyim yok" deme seklidir — normaldir, hata degil.

Tanilar gerisinden farkli calisir: bir `DiagnosticCollection`'in sahibi sensin ve sana sorulmak yerine kendi takviminde (tipik olarak dokuman degisiminde, geciktirilmis) icine yazarsin. Kapanan ya da silinen dokumanlar icin girdileri temizlemeyi unutma, yoksa bayat hatalar Problems panelinde hortlar.

Provider basina sozlesmeler, donus tipi ayrintilari ve ortusen provider'lar arasindaki secim `references/providerlar.md` icinde.

## Agac view'lari

`TreeDataProvider`, ozel kenar cubugu ve panel view'larini besler. Insanlari takan iki sey:

- **Yenileme, senin tetikledigin bir olaydir**, `onDidChangeTreeData` uzerinden. Alttaki verini degistirmek, sen onu tetikleyene kadar gorunur hicbir sey yapmaz — tum agaci yenilemek icin `undefined` ile, o alt agaci yenilemek icin belirli bir eleman ile.
- **`getChildren()` tembel cagrilir**, yalnizca genisletilmis dugumler icin. Tum agaci istekli sekilde kurma; cocuklari talep uzerine dondur ve `getTreeItem`'in ucuz oldugundan emin ol.

View nesnesinin kendisine ihtiyacin oldugunda — secim, reveal, rozetler, mesaj — `registerTreeDataProvider` yerine `window.createTreeView` kullan. Bkz. `references/view-lar.md`.

## Webview'ler

Webview'ler API'deki en yuksek riskli yuzeydir, cunku guvenligini saglamaktan senin sorumlu oldugun gercek bir tarayici baglamidir.

**Nonce'lu Content-Security-Policy zorunludur, istege bagli degil.** CSP olmadan, guvenilmeyen herhangi bir icerigi — dosya iceriklerini, API yanitlarini, workspace'ten gelen her seyi — render eden bir webview, extension host kodunla mesajlasabilen bir baglama acilan bir enjeksiyon vektorudur.

Desen:

1. Kati bir CSP meta etiketi ayarla, betiklere yalnizca render basina bir `nonce` ile izin ver.
2. `localResourceRoots`'u ihtiyac duyulan en dar dizin setine ayarla.
3. Her yerel dosya yolunu `webview.asWebviewUri()` ile cevir — ham `file://` yollari yuklenmez.
4. Kullanici ya da workspace icerigini asla kacislanmamis halde HTML string'ine enjekte etme.

**Bos webview hata ayiklama kurali:** hicbir sey render etmeyen bir webview neredeyse her zaman CSP'nin kendi betigini engellemesidir (eksik ya da uyusmayan nonce) ya da `asWebviewUri` ile cevrilmemis bir kaynak yolu. Baska bir yere bakmadan once webview gelistirici araclarini ac.

Eklenti ve webview yalnizca mesajlasarak iletisim kurar — `postMessage` / `onDidReceiveMessage`. Gelen mesajlari guvenilmeyen girdi olarak ele al ve dogrula; webview, eklenti kodundan farkli bir guven baglamidir.

Webview'ler `retainContextWhenHidden` ayarlanmadikca gizlendiklerinde yok edilir — ki bu bellege mal olur, o yuzden state'i serilestirip geri yuklemeyi tercih et. Tam HTML sablonu, nonce uretimi ve state kaliciligi `references/webviewler.md` icinde.

## Workspace ve dosya sistemi

**Node `fs` yerine `vscode.workspace.fs`'i tercih et.** Workspace yerel diskte olmayabilir — uzaktan SSH, container'lar, GitHub sanal dosya sistemleri. `workspace.fs` bunlarin hepsinde calisir; Node `fs` sessizce yalnizca yerel dosyalarda ve yalnizca masaustunde calisir.

String yollar yerine `vscode.Uri` kullan, string birlestirme ya da Node `path` yerine `Uri.joinPath` kullan.

Node `fs`, hedef gercekten yerel ve workspace disindaysa — `context.globalStorageUri` icinde bir onbellek, ev dizinindeki bir aracin kendi config'i — ve eklentinin yalnizca masaustu oldugu teyit edildiyse savunulabilir. Bu karari verdiginde bunu soyle.

Duzenlemeler `WorkspaceEdit` (cok dosyali, tek islem olarak geri alinabilir, acilmamis dokumanlarda calisir) ya da `editor.edit()` (tek aktif editor) uzerinden gider. Aktif dosyadan fazlasina dokunan her sey icin `WorkspaceEdit`'i tercih et.

`createFileSystemWatcher` dis degisikliklere tepki verir — onu dispose etmeyi unutma ve istedigin den daha sik tetiklenmesini bekle.

## Configuration ve state

**Configuration** — eslesen bir `contributes.configuration` semasi ile `workspace.getConfiguration('yourExt')` uzerinden oku. Degeri aktivasyonda onbelleklemek yerine kullanim noktasinda oku, ya da `onDidChangeConfiguration`'i dinleyip yeniden oku; aksi halde kullanicilar bir ayari degistirir ve yeniden yukleyene kadar hicbir sey olmaz.

**State** — workspace basina veri icin `context.workspaceState`, workspace'ler arasi icin `context.globalState`. Ikisi de kucuk degerler icindir (tercihler, imlec konumlari, kapatilmis ipuclari), veri deposu degil. `globalState.setKeysForSync` anahtarlari Settings Sync'e dahil eder.

**Gizli bilgiler** — `context.secrets`, token'lar, anahtarlar ve kimlik bilgileri icin kabul edilebilir tek yerdir; asenkrondur ve isletim sistemi anahtarligiyla desteklenir. Kural ve gerekcesi (`globalState` diskte duz metindir, ayarlar senkronlanir ve hata raporlarina yapistirilir, bu ic eklentiler icin de gecerlidir) `vsx-tr-davranis` icinde kanondur — burasi yalnizca bunun API'sinin yasadigi yer.

**Depolama yollari** — sahip oldugun dosyalar icin `context.globalStorageUri` ve `context.storageUri`. Eklentinin kurulum dizinine asla yazma; guncellemede degistirilir.

## Ilerleme, asenkron ve uzun surecek isler

Bir andan fazlasini alan her sey `window.withProgress` icine aittir ki kullanici editorun takilmadigini bilsin. Kullanici tarafindan baslatilan isler icin `ProgressLocation.Notification` (`cancellable: true` ekle ve token'a saygi goster), arka plan durumu icin `ProgressLocation.Window`.

Asla senkron agir is yapma — paylasilan host'u tikiyorsun. Bir alt surece ya da worker'a devret.

`window.showInformationMessage` ve benzerleri, secilen dugmeye ya da kapatildiginda `undefined`'a cozulen promise'ler dondurur. Kapatma yaygin durumdur; onu ele al.

## Dis surecler

Bir binary'ye (formatlayici, linter, ic CLI) devrederken:

- Bu **yalnizca masaustudur**. Web extension host'ta calisamaz — etrafindan dolasmak yerine catismayi isaretle.
- Ciddi ciktisi olan her sey icin `exec` yerine `spawn`'i tercih et; `exec` tamponlar ve buyuk sonuclarda limitini asabilir.
- **Her zaman bir zaman asimi ayarla ve iptali gercekten sureci oldurecek sekilde bagla.** Hicbir seyin oldurmedigi takilmis bir alt surec, kullanicinin goremedigi ve yeniden baslatmadan temizleyemedigi bir sizintidir.
- Kullanici ya da workspace girdisini birlestirerek asla bir kabuk komutu kurma — argumanlari bir dizi olarak gecir. Workspace'ten turetilen yollar guvenilmeyen girdidir.
- stderr'i yakala ve yuzeye cikar. Sessizce basarisiz olan bir arac, gurultuyle hata veren birinden daha kotudur.

## Hata ayiklama kontrol listesi

Bir sey calismadiginda, su bes durum vakalarin cogunu aciklar:

1. **Hic bir sey olmuyor** → eklenti hic aktive olmadi. Aktivasyon olaylarini ve Extension Host cikti kanalini kontrol et.
2. **Komut palette yok** → `contributes.commands` girdisi yok ya da onu gizleyen bir `when` ifadesi var.
3. **Webview bos** → CSP kendi betigini engelliyor ya da kaynaklar `asWebviewUri`'den gecirilmemis.
4. **Provider bayat veri donduruyor** → gecersiz kilma olmadan onbellekleme ya da `onDidChangeTextDocument`'i yok sayma.
5. **Ayar degisikliginin etkisi yok** → deger aktivasyonda onbelleklenmis, `onDidChangeConfiguration` dinleyicisi yok.

## Referanslar

- `references/providerlar.md` — provider basina sozlesmeler, iptal, tanilar.
- `references/webviewler.md` — CSP sablonu, nonce, mesaj koprusu, state geri yukleme.
- `references/view-lar.md` — agac view'lari, dekorasyonlar, durum cubugu, quick pick.
- `references/workspace-fs.md` — Uri yonetimi, duzenlemeler, watcher'lar, cok koklu.
