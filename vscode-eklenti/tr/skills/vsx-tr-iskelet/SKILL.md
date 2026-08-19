---
name: vsx-tr-iskelet
description: VS Code eklenti projelerini kurma ve yeniden yapilandirma kanonu — proje yerlesimi, bundler secimi ve esbuild/webpack yapilandirmasi, extension host icin tsconfig, .vscodeignore paket siniri, launch.json hata ayiklama kurulumu, activate/deactivate yasam dongusu iskeleti ve birden fazla eklenti gonderen ekipler icin monorepo yerlesimi. Bu skill'i sifirdan yeni bir eklenti olustururken, mevcut bir projenin yapisini ya da derlemesini elden gecirirken, acilis performansi veya aktivasyon stratejisi yeniden tasarlanmasi gerektiginde, birkac eklenti arasinda paylasilan kod kurulurken ya da paketlenmis bir .vsix yanlis dosyalar icerdiginde ac.
---

# Eklenti Proje Iskeleti

Bu mimarin kanonu: ozellik kodunun icinde yasayacagi sekli belirleyen kararlar. Simdi ucuz, sonra pahalidirlar — aktivasyon stratejisi, dispose deseni ve paket siniri, sonradan telafi edilmesi kurulmasindan cok daha zor olan seylerdir.

Manifest ozellikleri `vsx-tr-manifest` icinde yasar. Bu skill onun etrafindaki her seyi kapsar.

## Bir sey uretmeden once bunlari netlestir

Dort cevap kurulumun cogunu belirler. Sor, ya da cikar ve varsayimi acikca soyle:

1. **Bu eklentiyi ne tetikliyor?** Belirli diller mi? Yalnizca acik komut mu? Workspace'te bir dosyanin varligi mi? Bir view'in acilmasi mi? Bu, aktivasyon stratejisini ve manifest'in cogunu belirler.
2. **Ic kullanim mi, yayin mi?** `vsx-tr-davranis` icindeki titizlik kadrani. LICENSE, ikon ve pazar yeri kalitesinde README'nin simdi kapsamda mi yoksa ertelenmis mi oldugunu belirler.
3. **Yalnizca masaustu mu, web extension host da mi?** Bu yapisaldir. Web destegi, browser bundle'indan erisilebilen her yerde `fs` ve `child_process`'i yasaklar — bunu ozellikler yazildiktan sonra kesfetmek onlari yeniden yazmak demektir.
4. **Tek eklenti mi, kod paylasan birkac eklenti mi?** Monorepo kararlarini iki eklenti ayristiktan sonra geriye donuk vermek acilidir.

**Minimum kur, sonra her eklemeyi gerekcelendir.** Uretilen sablonlar geriye ornek komutlar, yer tutucu katki noktalari ve kullanilmayan config birakir. Her `contributes` girdisi ve her bagimlilik gercekten istenen bir seye karsilik gelmeli. Artik kalan sablon kodu notr degildir — aktive olur, gonderilir ve sonraki kisi onun tasiyici oldugunu varsayar.

## Proje yerlesimi

Konvansiyonel sekil; izlenmeye deger cunku araclar ve diger tum VS Code gelistiricileri bunu varsayar:

```
extension-root/
├── .vscode/
│   ├── launch.json        # Extension Development Host hata ayiklama config'i
│   └── tasks.json         # hata ayiklayicinin bagimli oldugu derleme gorevi
├── src/
│   ├── extension.ts       # activate() / deactivate()
│   └── test/
├── dist/                  # paketlenmis cikti (gitignore'lu, gonderilir)
├── package.json           # manifest
├── tsconfig.json
├── esbuild.js
├── .vscodeignore          # .vsix'in DISINDA kalacaklar
└── README.md / CHANGELOG.md / LICENSE
```

`src/extension.ts`'i ince tut — yalnizca aktivasyon baglantisi, ozellikler kendi modullerinde ve oradan kaydediliyor. Yuzlerce satira buyuyen bir `extension.ts`, test edilmesi zor olacak bir projenin guvenilir erken belirtisidir.

## Bundle etmek

**Bundle et.** Bundle edilmemis bir eklenti yuzlerce gevsek dosya ve `node_modules`'unu gonderir; bu `.vsix`'i sisirir, kurulumu yavaslatir ve aktivasyonu olculebilir sekilde yavaslatir — her `require` bir dosya okumasidir.

**Yeni projeler icin varsayilan esbuild'dir**: hizli, kucuk config ve eklentiler icin guncel oneri. **webpack**'i yalnizca somut bir sebeple kullan — mevcut bir ekip konvansiyonu ya da esbuild'in karsilayamadigi loader'lar. Her iki durumda da secimi ve sebebini soyle.

Derleme config'inin en azindan sunlara ihtiyaci var:

- Masaustu bundle'i icin **`platform: 'node'`** ve **`format: 'cjs'`**. Extension host CommonJS yukler.
- **`external: ['vscode']`** — bu istege bagli degil. `vscode` modulu calisma aninda host tarafindan enjekte edilir ve diskte yoktur. Onu bundle etmek yuklemede kafa karistirici bir hatayla basarisiz olur.
- **Ayri dev ve production betikleri** — dev'de `--sourcemap --watch` ki hata ayiklayici TypeScript'e eslesin; production'da sourcemap'siz `--minify`.

Calisan esbuild ve webpack config'leri, arti hata ayiklayicinin ihtiyac duydugu watch gorevi baglantisi `references/derleme-kurulumu.md` icinde.

## TypeScript yapilandirmasi

- Varsayilan olarak **`"strict": true`**. API mesru olarak istege bagli degerlerle dolu — `activeTextEditor`, `workspaceFolders`, provider donusleri — ve strict mode, aksi halde calisma anindaki bir cokmeye donusecek yokluk yonetimini zorunlu kilan seydir.
- **`module`/`target`**, extension host'un fiilen calistirdigi Node runtime'iyla eslesmelidir. Varsaymak yerine guncel degeri kontrol et; VS Code'un paketli Node'u surumlerle birlikte hareket eder.
- **`@types/vscode`, `engines.vscode`'dan yeni olmamali** — bkz. `vsx-tr-manifest`. Engine'in onundeki tipler, destekledigini iddia ettigin en eski surumde var olmayan API'lere karsi derleme yapar.

## .vscodeignore: paket siniri

`.vscodeignore`, `.vsix` icinde neyin yer alacagina karar verir. Amac olarak `.gitignore`'un tersidir — kaynak kontrolunden degil, *gonderilen bir urunden* disliyorsun — ve tekrarlayan bir gonderim hatasi kaynagidir.

Gonderilmemesi **gerekenler**: `src/`, testler ve fixture'lar, `node_modules` dev bagimliliklari, `.git`, `.env` ya da herhangi bir kimlik bilgisi dosyasi, derleme config'leri, production'da sourcemap'ler.

Gonderilmesi **gerekenler**: paketlenmis cikti, `package.json`, README, CHANGELOG, LICENSE, ikon ve tum calisma zamani varliklari (webview HTML/CSS, gorseller, gramerler).

Bundle ederken tipik sekil her seyi disliyip `dist/`'i yeniden dahil etmektir — ama **fiilen derlenmis paketi inceleyerek dogrula**, asla ignore dosyasini okuyup akil yurutedek degil. Sondaki bir slash farki neyin eslestigini sessizce degistirir. Inceleme proseduru `vsx-tr-yayin` icinde; buradaki nokta su: bunu iskelet kurar ve paketleme dogrular — tek basina hicbir adim yeterli degildir.

## Hata ayiklama yapilandirmasi

`.vscode/launch.json`, Extension Development Host'u baslatir — eklentinin yuklu oldugu ikinci bir VS Code penceresi. O olmadan gelistiricinin isini calistirmasinin hicbir yolu yoktur.

`--extensionDevelopmentPath` proje kokune isaret etmeli, once derleyen bir `preLaunchTask` olmali (aksi halde bayat bir bundle'i hata ayiklarsin — gercekten kafa karistirici bir arizadir) ve `outFiles` paketlenmis ciktiya isaret etmeli ki breakpoint'ler dogru eslesin.

Config `references/derleme-kurulumu.md` icinde.

## Yasam dongusu iskeleti

`activate()` ilk tetikleyici olayda cagrilir; `deactivate()` kapanista.

**Dispose desenini ilk iskelette kur.** Iskelet kurmanin en yuksek kaldirac etkisine sahip isi budur, cunku gelecekteki her katkici bunu taklit yoluyla devralir. Ilk uc kayit `context.subscriptions`'a itiyorsa dorduncusu de itecektir. Iskelet ozensizse, sonradan eklenen her ozellik varsayilan olarak sizdirir ve telafi etmek her seyi denetlemek demektir.

`activate()`'i hizli ve tembel tut. Kullanici beklerken calisir. Ucuza kaydet; pahali isi — indeks kurma, ag cagrilari, surec baslatma — gercekten bir sey ihtiyac duyana kadar ertele. Aktivasyonda gercek bir is olmak zorundaysa, acilisi tikamak yerine `onStartupFinished` arkasina koy.

`activate()` `async` olabilir ve bir promise dondurebilir; VS Code onu bekler. Bu, gercek kurulum icindir, agir kaldirma icin degil.

`deactivate()` yalnizca `context.subscriptions`'in ifade edemedigi temizlik icin gereklidir — state bosaltma, alt surecleri sonlandirma. Dispose edilebilir her sey zaten halledilmis olmali.

## Birden fazla eklenti icin monorepo yerlesimi

Bir ekip birkac eklenti gonderdiginde ilgilidir (bu ekip gonderiyor — bazilari ic kullanim, bazilari yayinlanan).

Secim uc secenek arasinda ve durust cevap genelde ilkidir:

- **Ayri depolar, bilincli tekrar.** Kucuk bir yardimci kod paylasan iki eklenti icin en iyisi. Kucuk olcekte tekrar, derleme karmasikligindan ucuzdur.
- **Paylasilan paketli workspace monorepo'su** (npm/pnpm workspaces). Birkac eklenti onemli mantik paylastiginda dogru. Maliyeti gercek: her eklentinin bundler'i paylasilan paketi cozmek zorunda ve `.vscodeignore` her eklenti icin dogru olmali.
- **Yayinlanmis ozel npm paketi.** Paylasim depo ya da ekip sinirlarini astiginda dogru; maliyeti degisiklik ile kullanim arasina giren bir yayin adimi.

Hangisini secersen sec, **her eklenti kendi `package.json` manifest'ini, kendi surumunu ve kendi `.vsix`'ini korur** — eklentiler her zaman bagimsiz surumlenir ve gonderilir.

Yerlesim ve paket basina derleme baglantisi `references/monorepo.md` icinde.

## Mevcut bir projeyi yeniden yapilandirmak

Buyuk patlama seklinde yeniden yazma. Buyuk ve aciklanmamis bir yeniden yapilandirma incelenemez ve yapisal degisiklikle davranis degisikligini karistirir; boylece bir sey bozuldugunda hangisinin sebep oldugunu kimse soyleyemez.

Bunun yerine: belirli problemin adini koy, kapsamli duzeltmeyi oner ve yalnizca onu degistir. Bir proje `*` uzerinde aktive oluyorsa, derleme adimi yoksa ve dispose deseni yoksa, bunlar uc ayri gerekceyle uc ayri degisikliktir — ve bu sirayla, her biri dogrulanabilir sekilde inebilirler.

Yaygin yapisal problemler ve kapsamli duzeltmeleri `references/yeniden-yapilandirma.md` icinde.

## Devretmek

Gelistiricinin acikca ihtiyaci olanlar: aktivasyon stratejisi ve nedeni, dispose edilebilirlerin nereye gittigi, ic kullanim-yayin durusu, web extension host'un hedef olup olmadigi ve dev derlemesinin nasil calistirilacagi. Tam devir formati `vsx-tr-akis` icinde.

## Referanslar

- `references/derleme-kurulumu.md` — esbuild/webpack config'leri, tsconfig, launch.json, tasks.json.
- `references/monorepo.md` — cok eklentili yerlesim ve paylasilan paketler.
- `references/yeniden-yapilandirma.md` — mevcut projelerde tani koyma ve duzeltmeleri kapsamlandirma.
