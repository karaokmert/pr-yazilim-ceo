---
name: vsx-tr-yayin
description: VS Code eklentilerini test etme, paketleme ve gonderme kanonu — @vscode/test-cli entegrasyon test duzeni, @vscode/vsce ile .vsix uretimi ve incelenmesi, anlamsal surumleme ve degisiklik gunlugu, yayin oncesi guvenlik ve izin incelemesi, pazar yeri yayinlama (ve Open VSX) ve ic kullanim .vsix dagitimi. Bu skill'i bir eklenti test edilirken, paketlenirken, surumlenirken, guvenlik incelemesinden gecirilirken ya da yayinlanirken ac — test duzeni kurulurken, bir .vsix uretilirken, bir pazar yeri listelemesi hazirlanirken, gonderimden once gizli bilgilerin ya da telemetrinin nasil ele alindigi incelenirken ya da ekibe bir ic derleme dagitilirken.
---

# Test, Paketleme ve Yayin

Bu qa-yayincinin kanonu: "Extension Development Host'ta calisiyor" ile "insanlarin calisan, surumlenmis, guvenilir bir urunu var" arasindaki her sey.

Hepsini sekillendiren iki cerceve noktasi:

**Yayinlamak pratikte geri alinamaz.** Bir pazar yeri eklentisini yayindan kaldirabilirsin, ama onu zaten kurmus makinelerden kaldiramazsin. Yayin zincirinin problemleri not edip devam etmek yerine hatada durmasinin sebebi budur.

**Buldugunu duzeltmezsin.** Kusurlar kesin tekrar bilgisiyle gelistiriciye doner. Buldugunu duzelten bir agent, baska ne bozuk diye bakmayi birakir — ve kontrolun bagimsizligi rolun tum degeridir. Devir formati `vsx-tr-akis` icinde.

## Yayin zinciri

Zincirin kendisi — sabit bes adim ve her adimin basarisizliginin not edilip devam edilmek yerine zinciri durdurdugu kural — `vsx-tr-akis` icinde kanondur. Bu skill her adimin uygulama detayini saglar; okumadiysan once oradaki zincir tanimini oku.

Asagidaki bolumler (1-5 numarali) sirasiyla dogrudan o zincire eslesir.

## 1. Test

Eklenti testleri **gercek, indirilmis bir VS Code ornegi icinde** calisir, taklit bir API'ye karsi degil. Duzenin tanimlayici ozelligi budur ve kurulumun degmesinin sebebidir: taklit bir `vscode` namespace'i, API'yi degil API hakkindaki varsayimlarini test eder ve tam olarak yakalaman gereken bozulmayi gizler — kaydolmayan bir katki noktasi, hic tetiklenmeyen bir aktivasyon olayi.

Guncel kurulum tek degil, **birlikte iki paket**tir:

```bash
npm install --save-dev @vscode/test-cli @vscode/test-electron
```

`@vscode/test-cli` kosucu ve yapilandirma katmanidir (`.vscode-test.js` / `.mjs` / `.json`); `@vscode/test-electron` ise gercek VS Code'u indirip baslatan katmandir. Daha eski projeler `@vscode/test-electron`i elle yazilmis bir kosucuyla dogrudan surebilir — o hala calisir ve yayinin ortasinda yeniden yazmaya degmez.

Namespace'siz **`vscode-test` paketi kullanimdan kalkmistir** (`@vscode/test-electron` olarak yeniden adlandirildi). Onu bulursan bu gelistirici icin bir modernlestirme notudur, yayin turu sirasinda duzeltilecek bir sey degil.

Web eklentileri ucuncu bir paket olan `@vscode/test-web` uzerinden test edilir; o, eklentiyi bir tarayicida calistirir — gercekten farkli bir ortam, yani masaustu test gecisleri web davranisi hakkinda hicbir sey soylemez.

Kurulum ve yapilandirma ozellikleri `references/test.md` icinde.

**Neyin test edilmeye deger oldugu**, oncelik sirasina gore — eklenti testleri yavastir, bu yuzden onlari gercek bozulmayi yakaladiklari yerde harca:

- **Aktivasyon** — eklenti beyan ettigi tetikte aktive oluyor. Hicbir seyin calismadigi en zararli ariza sinifini yakalar.
- **Komutlar calisiyor** — `vscode.commands.executeCommand` ile cagir ve etkiyi dogrula. Bu ayrica manifest girdisiyle kaydin anlastigini kanitlar.
- **Provider'lar dogru sonuc donduruyor** — gercek bir fixture dokumani ac, provider'i cagir ve donen seyi dogrula.
- **Configuration'a saygi gosteriliyor** — bir ayari degistir, davranisin degistigini dogrula.

`sinon` ya da benzerini yalnizca gercek dis unsurlar icin kullan — ag cagrilari, alt surecler, saatler. `vscode` namespace'inin kendisini taklit etmek duzenin amacini bosa cikarir.

Asenkron zamanlama, kararsiz eklenti testlerinin alisilmis kaynagidir: aktivasyon, provider kaydi ve dil sunucusu hazirligi anlik degildir. Sabit bir sure uyumak yerine gercek bir kosulu bekle.

## 2. Guvenlik ve izin incelemesi

**Ayri ve bilincli bir tur — testin yan etkisi degil.** Ic ve yayinlanan eklentiler icin aynen gecerlidir (bkz. `vsx-tr-davranis` icindeki titizlik kadrani); bir ic arac cogu zaman halka acik olandan daha hassas altyapinin kimlik bilgilerini tutar.

Asagidaki ilk kontrolun arkasindaki sahiplik kurali — gizli bilgiler yalnizca `context.secrets`'a aittir, asla `globalState`/`workspaceState`/ayarlar/sabit kodlanmis — `vsx-tr-davranis` icinde kanondur. Bu bolum, o kurala karsi yayin anindaki dogrulama turudur, neden dogru oldugunun yeniden ifadesi degil.

Dort kontrol:

**Gizli bilgiler.** Kaynakta `globalState`, `workspaceState`, `contributes.configuration` icinde ya da sabit kodlanmis her seyi ara. **Gizli bir bilgiyi yanlis yerde bulmak yayini durdurur** — gelistiriciye doner, sonraya not edilmez.

**Makineden ne cikiyor.** Her ag cagrisini ve varsa telemetriyi belirle. Yayinlanan bir eklenti icin ifsa edilmemis veri toplama pazar yeri politikasini ihlal eder; onu README'de ifsa et ve kullanicinin genel telemetri ayarina saygi goster. Ic kullanim icinse ekip yine de bilmeyi hak eder.

**Yetenek beyanlari.** `capabilities.untrustedWorkspaces` ve `capabilities.virtualWorkspaces` kodun fiilen yaptigiyla eslesmelidir — varsayilanlarda birakilmis degil, koda karsi dogrulanmis. Workspace tarafindan belirtilen bir binary calistiran bir eklenti, manifest ne iddia ederse etsin guvenilmeyen bir workspace'te guvenli degildir. Sekiller `vsx-tr-manifest` icinde.

**Bagimliliklar.** Yayin derlemesinden once `npm audit` (ya da esdegeri) calistir. Paketlenmis bagimliliklar `.vsix` icinde gonderilir; savunmasiz bir gecisli bagimlilik artik senin eklentinin acigidir.

## 3. Surumleme ve degisiklik gunlugu

Paketlemeyle ayni is birimi. Surumu ilerlememis bir `.vsix` gondermek, onu zaten kurmus olan herkes icin guncelleme mekanigini bozar — VS Code'un bir guncelleme sunmak icin hicbir sebebi olmaz.

Semver, kullanicilarin deneyimledigi seye kapsamlandirilmis:

- **Patch** — hata duzeltmeleri, arayuz degisikligi yok.
- **Minor** — geriye uyumlu yeni ozellikler, yeni komutlar ya da ayarlar.
- **Major** — kirici degisiklikler: kaldirilmis ya da yeniden adlandirilmis komutlar, kaldirilmis ayarlar, degismis varsayilan davranis, yukseltilmis `engines.vscode` minimumu.

Bir komutu yeniden adlandirmak, icsel hissettirse de *kiricidir* — kullanici kisayollari ve task'lari komut ID'lerine string olarak referans verir.

Pazar yeri konvansiyonu tek sayili minor surumleri on-surum olarak kabul eder; ekip `--pre-release` kullaniyorsa numaralandirma semasini onunla tutarli tut.

`CHANGELOG.md`, kullanicinin gordugu degisikligi anlatan gercek girdiler alir. "Hata duzeltmeleri ve iyilestirmeler", guncelleyip guncellememeye karar veren bir kullaniciya tam olarak hicbir sey soylemez.

## 4. Paketleme ve inceleme

`@vscode/vsce` `.vsix`i uretir. Bir `.vsix` bir zip'tir — inceleme adimini hem mumkun hem zorunlu kilan sey budur.

**Temiz bir `vsce package` cikis kodu, dogru icerigin kaniti degildir.** `.vscodeignore` hatalari hata uretmez; eksik bir varlik iceren ya da binadan hic cikmamasi gereken bir seyi iceren bir paket uretir. Paketi ac ve dosya listesini oku. Yalnizca ilk seferde degil, her yayinda.

Ne aradigin:

- **Orada olmamasi gerekenler**: `src/`, testler ve fixture'lar, `.env` ya da kimlik bilgisi dosyalari, `.git`, dev `node_modules`, ic notlar.
- **Orada olmasi gerekenler**: `main`/`browser`in isaret ettigi paketlenmis giris noktasi, `package.json`, README, CHANGELOG, LICENSE, ikon ve her calisma zamani varligi (webview HTML/CSS, gorseller, gramerler).
- **Boyut mantigi**: paketlenmis bir eklenti tipik olarak bir megabyte'in oldukca altindadir. Onlarca megabyte neredeyse her zaman `node_modules`in dahil edildigi anlamina gelir.

Paketleme, cikarma ve icerik listeleme komutlari `references/paketleme.md` icinde.

**Yalnizca kaynagi degil, paketlenmis urunu test et.** Uretilen `.vsix`i temiz bir VS Code ornegine kur ve eklentinin aktive oldugunu ve ana komutunun calistigini dogrula. Bu, kaynak seviyesindeki tum testlerin yapisal olarak yakalayamayacagi arizayi yakalar: paketi bir dosya eksik olan dogru bir eklenti. Bu skill'deki en yuksek degerli tek kontroldur.

## 5. Dagitim

### Yayinlanan — pazar yeri

Yayinlamadan once dogrula, cunku aksi halde pazar yeri incelemesi ya da kullanicilarin bunlari senin icin bulur:

- `publisher` gercek publisher ID ile esletiyor ve kimlik dogrulama calisiyor (asagi bak).
- `README.md` bir **listeleme sayfasi** olarak yazilmis — ne yaptigi, birinin onu neden istedigi ve bir ekran goruntusu ya da GIF. Bir yabancinin kurmaya karar vermesinin tum dayanagi budur.
- `LICENSE` mevcut, `icon` ayarli (**PNG ≥128×128 — SVG reddedilir**), `categories` ve `keywords` dolu, `repository` gercek kaynaga isaret ediyor.
- Surum duz `major.minor.patch` — `-beta` soneki yok; on-surumler icin `--pre-release` kullan.
- Surum ve degisiklik gunlugu guncellenmis.

**Kimlik dogrulama degisiyor ve eski yol sonlaniyor.** Yayinlama tarihsel olarak bir Azure DevOps Personal Access Token kullandi (`vsce login` ya da ortamda `VSCE_PAT`). **Azure DevOps'taki global PAT'lar emekliye ayriliyor — duyurulan tarih 2026-12-01.** Yerine gelen Microsoft Entra ID: `vsce publish --azure-credential` ya da GitHub Actions'tan hicbir saklanan token olmadan yayinlamak icin `vsce publish --oidc`.

Simdi kurulan her sey icin Entra ID yolunu tercih et. PAT tabanli mevcut bir hat bulursan, onu sessizce bozulmaya birakmak yerine son tarihi olan bir is olarak isaretle.

**Imzalama senin isin degil — Marketplace her eklentiyi yayin aninda imzalar** ve VS Code o imzayi kurulumda dogrular. Imzalama anahtarlari uretmez ya da yonetmezsin. Bunun anlami su: bozulmus ya da kurcalanmis bir paket, kullanicinin makinesinde `SignatureIsInvalid` ya da `NotSigned` gibi hatalarla dogrulamada basarisiz olur; yani kullanicilar kurulum hatalari bildirirse her seyden once paket butunlugunu kontrol etmeye deger. Yerel olarak dogrulaman gerekirse `vsce generate-manifest` ve `vsce verify-signature` mevcuttur.

**Yayinlamak bir insan kararidir.** Hazirlik durumunu sun ve tetigi insana birak — geri alinamazlik noktasi burasidir.

Eklenti ayrica VSCodium ve diger uyumlu editorleri hedefliyorsa, **Open VSX ayri bir yayin adimi olan ayri bir kayit defteridir** ve `ovsx` CLI'sini kullanir. Birine yayinlamak digerine yayinlamaz. Ikisini de acikca ele al ya da yalnizca birinin yapildigini belirt.

Open VSX Eclipse Foundation tarafindan isletilir, bu yuzden `code.visualstudio.com` hicbirini belgelemez — `ovsx` cevaplari icin oraya bakma ve pazar yeri kurallarinin gecerli oldugunu varsayma. Publisher yerine namespace kullanir (`ovsx create-namespace`).

Yayin sonrasi, listelemenin dogru render edildigini dogrula — bozuk bir README gorseli, bakan herkes tarafindan gorulur.

### Ic kullanim

Daha hafif ve dogru sekilde oyle: `.vsix`i uret, ekibin ulasabilecegi bir yere koy (paylasim, CI urunu, ic galeri) ve kurulum talimatlari ver:

```
code --install-extension /path/to/extension-0.1.0.vsix
```

Kullanicilar ayrica Komut Paletinde **Extensions: Install from VSIX** ile de kurabilir.

**VSIX'ten kurulmus bir eklentide otomatik guncelleme varsayilan olarak kapalidir.** Ic dagitimi en cok isiran gercek budur: meslektaslar ilk kurduklari derlemede suresiz kalir ve aylar once duzelttigin hatalari bildirirler. Buna gore planla — guncellemeleri acikca duyur ve surumu eklentinin urettigi her ciktida gorunur yap ki bir hata raporu kendi derlemesini tanimlasin.

Pazar yeri listeleme cilasini atla — halka acik olmayan bir urun icin bosa emektir. **Guvenlik incelemesini, surumlemeyi ya da paket incelemesini atlama.** Onlar sunum degil, muhendislik butunlugudur.

## Bir yayin turunu raporlamak

Su besini bu sirayla kapsa:

1. **Testler** — ne calisti, gecti/kaldi, bulunan hatalar (tekrar bilgisiyle, duzeltilmemis olarak geri verilmis).
2. **Paket incelemesi** — gercek icerik ozeti, beklenmeyen her sey isaretlenmis.
3. **Guvenlik incelemesi** — dort kontrol, her biri sonucuyla.
4. **Surum ve degisiklik gunlugu** — yeni surum ve semver gerekcesi.
5. **Dagitim** — pazar yeri URL'si ya da urun konumu ve kurulum komutu.

Bilinen bosluklari acikca belirt. "Agac view'i icin test kapsami yok; komut yolu kapsanmis" faydalidir. Sessizlik, var olmayan bir kapsam olarak okunur.

## Yayin ne zaman durdurulur

Su durumlarda dur, raporla ve paketleme ya da yayinlama:

- Bir test basarisiz olur ya da gonderilen bir kod yolunu etkileyen bir hata bulunur.
- `context.secrets` disinda herhangi bir yerde bir gizli bilgi bulunur.
- Paket incelemesi gonderilmemesi gereken bir sey gosterir.
- Yetenek beyanlari gercek davranisla esletmez.
- Dagitim niyeti belirsizdir ve urun ikisinin daha zorlu olani icin hazir degildir.

**Durmak normal bir sonuctur.** Gecikmis bir yayin bir gune mal olur; bilinen bozuk yayinlanmis bir surum ise kotu bir yoruma, bir destek yukune ve acil bir yamaya — zaten kurmus kullanicilar icin.

## Referanslar

- `references/test.md` — duzen kurulumu, yapilandirma, test desenleri, asenkron zamanlama.
- `references/paketleme.md` — vsce komutlari, .vsix incelemesi, yayinlama mekanigi.
- `references/guvenlik-incelemesi.md` — inceleme kontrol listesi ayrintili.
