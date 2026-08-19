# Aktivasyon Olaylari

Ayrintili referans. Karar kurallari ust SKILL.md icinde; bu dosyada tam olay listesi, otomatik uretim siniri ve hata ayiklama proseduru var.

## Icindekiler

- [Otomatik uretilen olaylar](#otomatik-uretilen-olaylar)
- [Hala beyan etmen gerekenler](#hala-beyan-etmen-gerekenler)
- [Acilis performansi](#acilis-performansi)
- [Aktivasyon hatasi ayiklama](#aktivasyon-hatasi-ayiklama)

## Otomatik uretilen olaylar

**VS Code 1.74'ten beri** bir katki beyan etmek onun aktivasyon olayini uretir. Bunlari ayrica listeleme:

| Katki | Otomatik uretilen olay | Baslangic |
|---|---|---|
| `contributes.commands` | `onCommand:<id>` | 1.74 |
| `contributes.languages` | `onLanguage:<id>` | 1.74 |
| `contributes.views` | `onView:<id>` | 1.74 |
| `contributes.customEditors` | `onCustomEditor:<viewType>` | 1.74 |
| `contributes.authentication` | `onAuthenticationRequest:<id>` | 1.74 |
| `contributes.taskDefinitions` | `onTaskType:<type>` | 1.76 |

1.74+ hedefleyen bir manifest'te sik sik hic `activationEvents` dizisi olmaz. Bu bir eksiklik degil, dogru ve moderndir.

`engines.vscode` 1.74'un altindaysa bunlari elle listelemen gerekir — bayat bir engine tabanini yerinde birakmamak icin bir sebep daha.

## Hala beyan etmen gerekenler

**`onStartupFinished`** — acilis tamamlandiktan sonra. Dogal bir tetigi olmayan arka plan isleri icin dogru secim ve `*`'in gorundugu neredeyse her durumda onun dogru yerine gececek olan.

**`workspaceContains:<glob>`** — workspace eslesen bir dosya icerdiginde. Proje-tipine ozgu araclar icin mukemmel: belirli bir framework icin yazilmis bir eklenti, ilgisiz her projede hareketsiz kalir.

```json
"activationEvents": ["workspaceContains:**/.myproject-config.json"]
```

Maliyetine dikkat: VS Code bunu degerlendirmek icin workspace'i tarar. Devasa bir depoda cok genis bir glob'un kendisi bir acilis maliyetidir.

**`onFileSystem:<scheme>`** — verilen URI semasina sahip bir dosya acildiginda (`ftp`, `ssh`, ozel semalar).

**`onDebug`**, `onDebugResolve:<type>`, `onDebugInitialConfigurations` — hata ayiklamayla ilgili aktivasyon.

**`onUri`** — eklentinin URI handler'i VS Code disindan cagrildiginda (OAuth geri cagrilari, derin baglantilar).

**`onWebviewPanel:<viewType>`** — VS Code onceki bir oturumdan bir webview'i geri yukledigi zaman. Webview'lerin pencere yeniden yuklemesinden sag cikmasi gerekiyorsa zorunludur.

**`onTerminalProfile:<id>`**, `onWalkthrough:<id>`, `onNotebook:<type>`, `onRenderer:<id>`, `onEditSession:<scheme>`, `onSearch:<scheme>` — daha dar durumlar; ihtiyacin oldugunda guncel seklini arastir.

**`*`** — acilis sirasinda, her zaman. `vsce package` `--allow-star-activation` verilmedikce **bunu reddeder**. Kullanmadan once `onStartupFinished`'in gercekten ise yaramadigini dogrula; neredeyse her zaman yariyor.

## Acilis performansi

Aktivasyon maliyeti paylasilir. Her eklentinin aktivasyonu, kullanici kullanilabilir bir editor beklerken calisir ve kullanicilarda rutin olarak onlarca eklenti kurulu olur.

- `activate()`'i kayit islemleriyle sinirli tut. Indeksleme, ag cagrilari ve surec baslatmayi ilk kullanima ertele.
- `activate()` `async` olabilir; VS Code onu bekler. Orada yavas isi beklemek acilisi dogrudan geciktirir.
- **Tahmin etmek yerine olc**: `Developer: Show Running Extensions` komutu her eklentinin aktivasyon suresini ve onu neyin tetikledigini raporlar. Optimize etmeden once bunu kullan.
- `Developer: Startup Performance` daha dolu bir dokum verir.

## Aktivasyon hatasi ayiklama

Bir eklenti tamamen olu gorundugunde, sebebi en hizli bulan sira budur:

1. **`Developer: Show Running Extensions`** — hic aktive oldu mu? Listede yoksa aktivasyon olayi hic tetiklenmemistir.
2. **Tetigin gercekle esletigini kontrol et.** `onLanguage:javascript` bir `.ts` dosyasi icin tetiklenmez; bir `workspaceContains` glob'u, dosya varsayilandan farkli bir derinlikte duruyorsa eslesmez.
3. **Output paneli → "Extension Host" kanali** — aktivasyon hatalari bir diyalog olarak degil burada yuzeye cikar. `activate()` icinde firlatilan bir istisna eklentiyi yari kurulmus ve sessizce bozuk birakir.
4. **Komut ID'sinin `contributes.commands` ile `registerCommand` arasinda tam olarak eslestigini dogrula.** Bir yazim hatasi tam olarak bu belirtiyi uretir.
5. **`engines.vscode`'u** calisan VS Code surumune karsi kontrol et. Cok yuksekse eklenti hic yuklenmez.

**Extension Bisect** (`Help: Start Extension Bisect`), diger yon icin arac — bir sey bozuk oldugunda ve kurulu bircok eklentiden hangisinin sorumlu oldugunu bilmediginde. Yarilari acip kapatarak ikili arama yapar.
