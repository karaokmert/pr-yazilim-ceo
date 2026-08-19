# Workspace Guveni ve Sanal Workspace'ler

`capabilities` icin ayrintili referans. Ust SKILL.md sekilleri ve durustluk kuralini verir; bu dosyada karar rehberi, `"limited"`'in calisma anindaki uygulamasi ve her alanin arkasindaki gerekce var.

Resmi dokumanlar: `code.visualstudio.com/api/extension-guides/workspace-trust` ve `code.visualstudio.com/api/extension-guides/virtual-workspaces`.

## Icindekiler

- [Restricted Mode aslinda nedir](#restricted-mode-aslinda-nedir)
- [untrustedWorkspaces degerine karar vermek](#untrustedworkspaces-degerine-karar-vermek)
- [Kodda "limited" uygulamak](#kodda-limited-uygulamak)
- [restrictedConfigurations ve machine kapsami](#restrictedconfigurations-ve-machine-kapsami)
- [Sanal workspace'ler](#sanal-workspaceler)
- [description metnini yazmak](#description-metnini-yazmak)
- [Bunu durustce incelemek](#bunu-durustce-incelemek)

## Restricted Mode aslinda nedir

Kullanici VS Code'un daha once gormedigi bir klasoru actiginda soru sorulur: **"Bu klasordeki dosyalarin yazarlarina guveniyor musunuz?"** Evet diyene kadar pencere **Restricted Mode**'da calisir.

Bunun savundugu tehdit belirli ve gercek. Okumak icin bir depo klonlamak, bir yabancidan gelen pull request'i incelemek, birinin e-postayla gonderdigi bir eki acmak — bunlarin hicbiri o kisinin kodunu calistirmaya riza degildir. Ama bir editor, kod yurutme motorudur. Workspace guveni var olmadan once bir klasoru acmak yeterliydi: depodaki bir `.vscode/settings.json`, bir eklentinin "linter binary yolu" ayarini depodaki bir betige isaret ettirebilir ve eklenti onu itaatkarca calistirirdi. Kullanici bir klasor acmaktan baska bir sey yapmamisti.

Restricted Mode bunu kapatir. Guvenilmeyen bir pencerede VS Code:

- **`untrustedWorkspaces.supported: false` beyan eden eklentileri tamamen devre disi birakir.** Guven verilene kadar hic aktive olmazlar. Kullanici onlari soluklastirilmis olarak ve aciklama olarak senin `description` metninle gorur.
- **`"limited"` beyan eden eklentileri calistirir**, ama `restrictedConfigurations` icinde listelenen her ayarin workspace tarafindan saglanan degerini yok sayar.
- **`true` beyan eden eklentileri** normal calistirir, eklentinin bunun guvenli oldugu sozune guvenerek.
- Kendi tehlikeli davranislarini engeller: task'lar, hata ayiklama ve workspace tanimli terminal profilleri calismaz.

Guven klasor bazlidir ve hatirlanir. Ayrica **oturum ortasinda** da gelebilir — kullanici pencereyi yeniden yuklemeden banner'daki "Trust"a tiklar. Asagidaki calisma zamani API'sinin var olma sebebi ve "guveni aktivasyonda bir kez kontrol et" yaklasiminin neden bir hata oldugu budur.

Beyan tavsiye niteliginde degildir. `false`, eklentinin calismayacagi anlamina gelir; yani onu secmenin guvenilmeyen klasorlerde calisan kullanicilara gercek bir maliyeti vardir. `true`'yu hak edilmediginde secmenin ise makinelerine bir maliyeti vardir.

## untrustedWorkspaces degerine karar vermek

Test "eklentim tehlikeli hissettiriyor mu" degildir. Su: **workspace icerigi hangi kodun calistigini etkileyebilir mi?** Workspace icerigi dosyalari kapsar, ama kritik olarak `.vscode/settings.json`, `.vscode/tasks.json` ve eklentinin okudugu her config dosyasini da kapsar.

### Guvenilmeyende guvensiz — `false` ya da `"limited"` beyan et

- **Yolu bir workspace ayarindan gelen bir binary calistiriyor.** `myExt.formatterPath`, `myExt.pythonPath`, `myExt.eslintPath`. Depo bunu `./tools/pwn.sh` yapar ve sen calistirirsin.
- **Workspace'te tanimli betikleri calistiriyor.** npm script'leri, Makefile hedefleri ya da bir `tasks.json` girdisini calistirmak — betik govdesi saldirgan kontrolundedir.
- **Workspace yapilandirmasini kod olarak degerlendiriyor.** `myext.config.js`'i `require()` ya da `import()` ile yuklemek. Bir JS config dosyasi *bir programdir*; onu require etmek calistirir. Bu, "config okumak" gibi hissettirdigi icin siklikla gozden kacar.
- **Workspace icerigini bir yorumlayiciya veriyor.** Bir workspace dosyasini `node`, `python`, `bash`'e ya da bir `eval()`'e vermek. Ifadelere izin veren her sablon motoru de dahil.
- **`node_modules`'tan bir dil sunucusu ya da arac baslatiyor.** `node_modules`'u depo kontrol eder; oraya postinstall ile yerlestirilmis bir binary, workspace kontrolundeki koddur.
- **Kimlik bilgilerini okuyup workspace'in adlandirdigi bir yere gonderiyor.** Bir uc nokta URL'si saglayan workspace ayari arti token tutan bir eklenti, veri sizdirmadir.
- **Kullanici hareketi olmadan workspace tarafindan saglanan duzenlemeleri ya da komutlari otomatik uyguluyor.**

### Guvenilmeyende guvenli — `true` savunulabilir

- **TextMate grameri ya da semantik token'lar ile sozdizimi vurgulama**, buffer metninden surec icinde hesaplanan. Yurutme yok.
- **Eklentinin icine gomulu bir formatlayici ile bicimlendirme**, workspace'in hangi binary'nin calistigini yonlendiremedigi ve argüman enjekte edemedigi durumda.
- **Surec icinde salt okunur analiz**: gomulu bir ayristirici ile dosyalari ayristirmak ve tani yayinlamak. Bir dosyayi okumak onu calistirmak degildir.
- **Saf arayuz**: bir renk temasi, bir ikon temasi, bir tus haritasi, bir snippet seti.
- **Tamamen kullanici ayarlarindan surulen ozellikler**, riskli ayarlari `machine` kapsami ile isaretledigin ve bir workspace'in onlari hic saglayamayacagi durumda.

Orta yol yaygindir ve `"limited"` tam olarak bunun icindir: hemen vurgula ve ayristir, ama kullanici klasore guvenene kadar yapilandirilmis linter'i baslatma.

## Kodda "limited" uygulamak

`"limited"` beyan edip kodda hicbir seyi kapiya baglamamak, `true` beyan etmekten daha kotudur — insa etmedigin bir guvenlik ozelligini iddia etmis olursun. Manifest bir sozdur; bu ise uygulamasidir.

Iki parca API:

- **`vscode.workspace.isTrusted`** — okudugun anda dogru olan bir boolean.
- **`vscode.workspace.onDidGrantWorkspaceTrust`** — kullanici oturum ortasinda guven verdiginde tetiklenir. Canli bir pencerede guven asla geri alinmaz, bu yuzden karsilik gelen bir "geri alindi" olayi yoktur; yalnizca guvenilmeyenden guvenilene gecersin.

Desen: **guvenli ozellikleri kosulsuz kaydet, tehlikeli olanlari tek bir etkinlestirme fonksiyonunun arkasina ertele ve o fonksiyonu ya hemen ya da olaydan cagir.**

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  // Her zaman guvenli: surec ici, workspace kontrollu yurutme yok.
  registerSafeFeatures(context);

  if (vscode.workspace.isTrusted) {
    enableTrustedFeatures(context);
  } else {
    // Guven pencere yeniden yuklenmeden sonradan gelebilir. Bu dinleyici olmadan
    // kullanici guven verir ve eklenti yeniden baslatilana kadar yari islevsel kalir.
    const sub = vscode.workspace.onDidGrantWorkspaceTrust(() => {
      enableTrustedFeatures(context);
      sub.dispose(); // tek seferlik: canli pencerede guven geri alinmaz
    });
    context.subscriptions.push(sub);

    // Kullaniciya neden eksik olduklarini soyle, her aktivasyonda dirdir etmeden.
    void vscode.window.setStatusBarMessage(
      '$(shield) MyExt: bu workspace guvenilir olana kadar linting devre disi',
      10_000
    );
  }
}

function registerSafeFeatures(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.languages.registerDocumentSymbolProvider(
      { language: 'mylang' },
      new InProcessSymbolProvider() // buffer metnini ayristirir, hicbir sey baslatmaz
    )
  );
}

// Cift kayda karsi koruma: bu hem aktivasyonda HEM DE guven olayindan calisabilir
// ve her iki durumda da idempotent olmali.
let trustedFeaturesEnabled = false;

function enableTrustedFeatures(context: vscode.ExtensionContext) {
  if (trustedFeaturesEnabled) return;
  trustedFeaturesEnabled = true;

  // Ancak simdi bir yurutulebiliri adlandiran bir ayari okuyup calistiriyoruz.
  const linterPath = vscode.workspace
    .getConfiguration('myExt')
    .get<string>('linterPath', 'mylint');

  context.subscriptions.push(startLinterProcess(linterPath));
}
```

Komutlar bu desende yaygin bir sizinti noktasidir. `contributes.commands` icinde kayitli bir komut guvenden bagimsiz olarak palette gorunur, bu yuzden tehlikeli bir komut guveni yalnizca kayit sirasinda degil **cagrildiginda** kontrol etmelidir:

```typescript
vscode.commands.registerCommand('myExt.runBuildTask', async () => {
  if (!vscode.workspace.isTrusted) {
    // Kullaniciya sorar; onlar cevaplayinca cozulur.
    const granted = await vscode.workspace.requestWorkspaceTrust({
      message: 'Build task calistirmak bu workspace\'teki betikleri yurutur.'
    });
    if (!granted) {
      vscode.window.showWarningMessage('Build icin guvenilir bir workspace gerekiyor.');
      return;
    }
  }
  await runBuild();
});
```

Iki ek not:

- **Cok koklu workspace'ler bir butun olarak guvenilir.** `isTrusted` klasor basina degil, pencere seviyesinde tek bir boolean'dir. Bir koke guvenip digerine guvenmemek mumkun degildir.
- **`requestWorkspaceTrust` kullaniciya donuk bir istemdir.** Onu bir kullanici hareketine yanit olarak cagir, asla `activate()` sirasinda — aciliste cikan bir istem, kullanicilari refleks olarak "Trust"a tiklamaya alistirir ki bu tum mekanizmayi bosa cikarir.

## restrictedConfigurations ve machine kapsami

`restrictedConfigurations`, istege bagli bir `string[]` ayar ID'si listesidir. Guvenilmeyen bir workspace'te VS Code, listelenen her ayarin **workspace tarafindan saglanan degerini yok sayar** ve kullanici ya da varsayilan degere geri doner. `getConfiguration().get()` cagrin guvenli degeri dondurur; hicbir filtreleme kodu yazmazsin.

**Basit kural: bir ayar bir yurutulebiliri, bir betigi, calistirilan bir yolu ya da bir surece gecirilen argumanlari adlandiriyorsa buraya aittir.** Ayrica yuklenecek bir modulu, taranacak bir eklenti dizinini ya da veri alan bir uc noktayi secen ayarlari da dahil et.

```json
"capabilities": {
  "untrustedWorkspaces": {
    "supported": "limited",
    "description": "%capabilities.untrusted.description%",
    "restrictedConfigurations": [
      "myExt.linterPath",
      "myExt.linterArgs",
      "myExt.pluginDirectory",
      "myExt.telemetryEndpoint"
    ]
  }
}
```

### `scope: "machine"` ile birlikte kullan

`restrictedConfigurations` guvenilmeyen workspace'leri korur. **`contributes.configuration` icindeki `scope: "machine"` daha da ileri gider: ayar, guvenilir olsun olmasin workspace ayarlarindan hic ayarlanamaz** — yalnizca kullanici ayarlarindan ya da makine seviyesindeki ayar dosyasindan.

```json
"contributes": {
  "configuration": {
    "title": "MyExt",
    "properties": {
      "myExt.linterPath": {
        "type": "string",
        "default": "mylint",
        "scope": "machine",
        "description": "mylint yurutulebilirinin mutlak yolu."
      }
    }
  }
}
```

`scope: "machine-overridable"` orta secenektir: varsayilan olarak makine seviyesi, ama bir workspace bunu gecersiz kilabilir — bu da acigi yalnizca guvenilir workspace'lerde yeniden acar. Projeye ozgu degerler gercekten gerektiginde kullan.

Cift kemer: yurutulebilir-yolu iceren bir ayar hem **`machine` kapsaminda olmali hem de `restrictedConfigurations` icinde listelenmelidir**. Kapsam workspace gecersiz kilmasini durdurur; kisitli liste ise kapsam bir gun gevsetilirse ikinci katmandir. Birlikte hicbir sey maliyetleri yoktur ve bagimsiz olarak basarisiz olurlar.

## Sanal workspace'ler

**Sanal workspace**, dosyalarin yerel diskte olmadigi bir workspace'tir. VS Code bunlari `file:` olmayan bir URI semasi altinda bir `FileSystemProvider` uzerinden sunar. Gercek durumlar:

- **github.dev** — bir GitHub deposunda `.` tusuna basmak. Dosyalar GitHub API'sinden gelir; hicbir sey klonlanmaz.
- **vscode.dev**, uzak bir depo acikken.
- **Ozel bir `FileSystemProvider` katan herhangi bir eklenti** — bir FTP tarayicisi, bir S3 bucket goruntuleyici, bellek ici ya da veritabani destekli bir dosya sistemi.

Bunun web eklentilerinden bagimsiz oldugunu unutma: **masaustu VS Code de bir sanal workspace acabilir.** Tam `fs` erisimiyle Node'da calisiyor olabilirsin ve yine de workspace dosyalari icin gercek bir yolun olmayabilir. Tuzak budur.

### Test

Eklentinin workspace yonetimi hakkinda uc soru sor:

1. **Workspace yollarinda Node `fs` kullaniyor mu?** `fs.readFileSync(uri.fsPath)` basarisiz olur — oyle bir dosya yok. Saglayici uzerinden yonlendiren `vscode.workspace.fs` kullan.
2. **Workspace dosyalarina karsi bir surec baslatiyor mu?** `spawn('eslint', [filePath])` calisamaz; alt surecin bir `vscode-vfs://` URI'sini gormesinin hicbir yolu yoktur. Bu genelde sanal destek icin olumcul, yamayla gecistirilebilir degil.
3. **`uri.fsPath`'in gercek bir yol oldugunu varsayiyor mu?** Sanal bir workspace'te `fsPath` yine bir string dondurur — bunu yanlis yapmayi bu kadar kolaylastiran sey de budur. O bir gorunum-sekilli yoldur, isletim sisteminin acabilecegi bir sey degil. Ayrica onun uzerinde `path.join` kullanmaktan ve URI string'lerini elle birlestirmekten kacin — `vscode.Uri.joinPath` kullan.

Ucu de hayirsa ve her sey `workspace.fs` ve `Uri` uzerinden gidiyorsa, muhtemelen sanal workspace'leri zaten destekliyorsun.

### Varsayilani `true` — onemli tuzak bu

**`virtualWorkspaces`'i atlamak `true` demektir.** Gercek dosyalara ihtiyaci olan ve bunu hic dusunmemis bir eklenti github.dev kullanicilarina sunulur, temiz kurulur, aktive olur ve sonra sessizce basarisiz olur — ya da dosyayi gezginde apacik goren bir kullaniciya hicbir anlam ifade etmeyen `ENOENT` hatalari firlatir.

Gercek dosyalara ihtiyaci olan bir eklenti **bilincli olarak** `false` beyan etmelidir. Hicbir sey seni uyarmaz.

```json
"capabilities": {
  "virtualWorkspaces": {
    "supported": false,
    "description": "Linter yerel bir surec olarak calisiyor ve dosyalarin diskte olmasi gerekiyor."
  }
}
```

Ciplak boolean kisayolu gecerlidir ve aciklanacak bir sey olmadiginda uygundur:

```json
"capabilities": { "virtualWorkspaces": true }
```

Ama asimetriye dikkat: ciplak boolean olarak `"virtualWorkspaces": false` gecerli JSON'dur ama kullaniciya eklentinin neden kullanilamadigina dair hicbir aciklama vermez. Deger `false` ya da `"limited"` oldugunda nesne formunu tercih et.

**`virtualWorkspaces` icin `restrictedConfigurations` yoktur.** O alan yalnizca `untrustedWorkspaces` altinda vardir. Sanal workspace'ler bir yetenek sorunudur, guvenlik siniri sorunu degil — etkisiz hale getirilecek saldirgan kontrollu ayar vektoru olmadigi icin alanin bir anlami olmazdi.

`"limited"` icin bir guven bayragi yerine sema uzerinden calisma aninda kapiya bagla:

```typescript
const isVirtual = vscode.workspace.workspaceFolders?.every(
  f => f.uri.scheme !== 'file'
) ?? false;

if (isVirtual) {
  // Yalnizca workspace.fs uzerinden calisan provider'lari kaydet.
  registerReadOnlyFeatures(context);
} else {
  registerFullFeatures(context);
}
```

## description metnini yazmak

**`supported` degeri `false` ya da `"limited"` oldugunda `description` zorunludur** — hem `untrustedWorkspaces` hem `virtualWorkspaces` icin. Yalnizca `supported` `true` oldugunda istege baglidir, cunku orada aciklanacak bir sey yoktur. Kisitli bir beyanda atlamak, kullaniciyi devre disi bir ozellige belirtilmis bir sebep olmadan bakar durumda birakir; alanin tesvik edilen degil zorunlu olmasinin sebebi de budur.

`description` **kullaniciya arayuzde gosterilir** — devre disi bir eklentinin yanindaki eklenti listesinde ve guven diyalogunda. Bir kod yorumu degildir. Eklentinin icsel olarak ne yaptigini bilmeyen ve bir seyin neden eksik oldugunu anlamaya calisan biri icin yaz.

Isleyen bir formul: **ne kullanilamiyor + neden + bu konuda ne yapilabilir, tek cumlede.**

Iyi:

> `"Bu workspace'e guvenene kadar linting ve bicimlendirme devre disi, cunku bunlar proje tarafindan yapilandirilan araclari calistiriyor."`

> `"Test paketini calistirmak dosyalarin diskte olmasini gerektiriyor, bu yuzden bu eklenti uzak depolarda kullanilamaz."`

Kotu ve nedeni:

- `"Desteklenmiyor."` — kullaniciya hicbir sey soylemez; hala tahmin etmek zorunda.
- `"Bu eklenti untrustedWorkspaces desteklemiyor."` — manifest alan adini kullaniciya geri okur.
- `"Kullanici yapilandirmali binary yollarinda child_process.spawn nedeniyle guven gerekiyor."` — uygulama detayi. Kullanici `spawn`'in ne oldugunu bilmez ve buna gore hareket edemez.

Yerellestir. `description`, diger tum kullaniciya donuk manifest string'leri gibi `package.nls.json`'dan `%key%` ikamesini destekler:

```json
"capabilities": {
  "untrustedWorkspaces": {
    "supported": "limited",
    "description": "%capabilities.untrustedWorkspaces.description%"
  }
}
```

```json
{
  "capabilities.untrustedWorkspaces.description":
    "Bu workspace'e guvenene kadar linting devre disi, cunku linter'lar proje tarafindan yapilandiriliyor."
}
```

Burada yerellestirmeyi atlamak yaygin bir kacirmadir — ekipler komut basliklarini yerellestirir ve tam da kafasi karismis bir kullanicinin okudugu bu string'leri unutur.

## Bunu durustce incelemek

Beyan, kodun yaptigiyla eslesmek zorundadir. Mekanizmanin tum amaci budur ve kontrol edilebilirdir.

Incelerken (ozellikle qa-yayinci) su kontrolleri calistir:

1. **`untrustedWorkspaces.supported` `true` ise kaynakta yurutme yuzeylerini ara** — `child_process`, `spawn`, `exec`, `execFile`, `fork`, dinamik `require(`/`import(`, `eval`, `new Function`. Herhangi bir eslesme gerekce ister: workspace neyin calistigini etkiliyor mu?
2. **Calistirilacak-yol adlandiran her ayar `restrictedConfigurations` icinde gorunuyor** ve tercihen `scope: "machine"` tasiyor. `contributes.configuration`'i kisitli listeye karsi capraz kontrol et; listelenmemis bir `*Path` ya da `*Command` ayari bulgudur.
3. **`"limited"` gercek bir kapiyla destekleniyor.** `isTrusted` ve `onDidGrantWorkspaceTrust` ara. Ikisi de yoksa `"limited"` iddiasi dekoratiftir ve eklenti `true` gibi davraniyordur.
4. **`supported` `false` ya da `"limited"` oldugunda `description` mevcut** ve kullanicilar icin yazilmis.
5. **`virtualWorkspaces` yoksa ya da `true` ise, workspace URI'lerine uygulanan `fsPath`, `require('fs')` ve `path.join` ara.** Eslesmeler varsayilanin yanlis oldugunu ve `false` beyan edilmesi gerektigini gosterir.
6. **Guven kontrolleri yalnizca aktivasyonda degil.** Tehlikeli bir komut cagrildiginda yeniden kontrol etmelidir.

Kodun uymadigi bir `supported: true`, **bir dokumantasyon hatasi degil bir guvenlik yanlis beyanidir**. VS Code eklentileri o alanin gucune dayanarak devre disi birakir; Restricted Mode'u ozellikle secmis bir kullanici guvenilmeyen kod calistirmamaya karar vermistir ve yanlis bir beyan bu karari sessizce gecersiz kilar. Pazar yeri incelemesi bunu yakalayabilir. Yakalamayabilir de. Bunu bir cila kalemi degil, bir dogruluk kapisi olarak ele al — ve `true` ile `"limited"` arasinda tereddut ettiginde `"limited"`'i sec ve riskli yariyi kapiya bagla.
