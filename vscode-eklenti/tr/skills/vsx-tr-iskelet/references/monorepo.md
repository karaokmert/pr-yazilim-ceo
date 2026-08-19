# Birden Fazla Eklenti ve Paylasilan Kod

Birkac eklenti gonderen bir ekip icin — bazilari ic kullanim, bazilari yayinlanan. Karar soyut olarak "monorepo mu degil mi" degildir; gercekten ne kadar paylasilan mantik oldugu ve koordinasyon maliyetinin ne oldugudur.

## Icindekiler

- [Bir yapi secmek](#bir-yapi-secmek)
- [Ayri depolar](#ayri-depolar)
- [Workspace monorepo](#workspace-monorepo)
- [Ozel npm paketi](#ozel-npm-paketi)
- [Her durumda gecerli kurallar](#her-durumda-gecerli-kurallar)
- [Sonradan gecis](#sonradan-gecis)

## Bir yapi secmek

Gercekte ne kadar paylasildigi konusunda durust ol. Ekipler rutin olarak birkac yuz satirlik yardimci kodu paylasmak icin monorepo'ya uzanir ve sonra sonsuza kadar derleme karmasikligi oder.

| Durum | Yapi |
|---|---|
| Iki eklenti, birkac paylasilan yardimci | Ayri depolar, bilincli tekrar |
| Birkac eklenti, ciddi paylasilan alan mantigi | Workspace monorepo |
| Paylasim ekipleri ya da kontrol etmedigin depolari asiyor | Ozel npm paketi |
| Eklentiler farkli kisilerce bagimsiz takvimlerde yayinlaniyor | Ayri depolar ya da npm paketi |

Meseleyi genelde cozen soru: **paylasilan kod degistiginde tum tuketicilerin birlikte guncellenmesi zorunlu mu?** Evetse, bir monorepo bunu atomik yapar ve maliyetine deger. Tuketiciler kendi hizlarinda uyum saglayabiliyorsa, surumlenmis bir paket gercegi daha iyi modeller ve monorepo sana direnir.

## Ayri depolar

Varsayilan ve ekiplerin bekledigin den daha sik dogru olan.

Bir `formatBytes` yardimcisini iki eklenti arasinda tekrarlamak birkac satira mal olur. Onu paylasmak bir workspace araci, bir derleme grafi, iki bundler'da cozumleme yapilandirmasi ve yerlesimi anlamasi gereken bir `.vscodeignore`'a mal olur. Kucuk olcekte tekrar gercekten daha ucuzdur — ve eklentilerin ihtiyaclari ayristiginda (ki genelde ayrisir) iki kopyanin da ayrismasina izin verir.

Ayni onemsiz olmayan mantik ucuncu kez kopyalandiginda ya da bir hata bir kopyada duzeltilip digerinde duzeltilmediginde yeniden dusun. Ikinci belirti gercek sinyaldir.

## Workspace monorepo

```
extensions-monorepo/
├── package.json              # workspaces yapilandirmasi, paylasilan devDependencies
├── tsconfig.base.json        # paylasilan derleyici secenekleri
├── packages/
│   └── shared/
│       ├── package.json      # name: "@company/ext-shared"
│       ├── src/index.ts
│       └── tsconfig.json
└── extensions/
    ├── linter/
    │   ├── package.json      # eklenti manifest'i
    │   ├── .vscodeignore
    │   ├── esbuild.js
    │   └── src/extension.ts
    └── snippets/
        └── ...
```

```jsonc
// kok package.json
{
  "private": true,
  "workspaces": ["packages/*", "extensions/*"],
  "devDependencies": { "typescript": "^5.x", "esbuild": "^0.x" }
}
```

```jsonc
// extensions/linter/package.json — eklenti manifest'i
{
  "name": "company-linter",
  "publisher": "company",
  "version": "0.3.1",
  "main": "./dist/extension.js",
  "dependencies": { "@company/ext-shared": "workspace:*" }
}
```

### Isirdigi yerler

**Bundle etmek paylasilan paketi soğurur.** esbuild import'u takip edip kaynagi satir ici hale getirdigi icin `dist/extension.js` paylasilan kodu icerir ve `.vsix`'in workspace yerlesimine hic ihtiyaci olmaz. Monorepo'lari eklentiler icin calisir kilan sey budur — ama bu, **her eklentinin bundle etmesi gerektigi** anlamina gelir, cunku bundle edilmemis olan, paket disina isaret eden bir `node_modules` symlink'i gonderirdi.

**`.vscodeignore` eklenti basinadir** ve o eklentinin dizinine goredir. Her birini derlenmis `.vsix`'ini inceleyerek dogrula; bir eklentide isleyen bir yerlesim, digeri icin sessizce tum workspace'i dahil edebilir.

**Hoisting yollari degistirir.** Workspace araclari bagimliliklari kok `node_modules`'a yukseltir, bu yuzden `__dirname`'e gore yol cozen her sey bekledigini bulamayabilir. Calisma zamani varlik yollari icin `context.extensionUri`'yi tercih et — yerlesimden bagimsiz olarak dogrudur.

**TypeScript'in paylasilan paketi cozmesi gerekir.** Ya `composite: true` ile proje referanslari ya da `tsconfig.base.json` icinde yol eslemesi. Yol eslemesi daha basit; proje referanslari daha iyi artimli derleme verir. Her durumda bundler ile `tsc`'nin cozumleme konusunda anlastigindan emin ol, yoksa tip kontrolunden gecen ama bundle edilemeyen kod elde edersin.

**Her eklentiyi bagimsiz surumle ve yayinla.** Her birinin kendi `version`'u ve kendi `.vsix`'i vardir. Ilgisiz eklentiler arasinda paylasilan bir surum numarasi anlamsiz yayinlar zorlar ve kullanicilarin neyin degistigi konusunda kafasini karistirir.

## Ozel npm paketi

Paylasilan kodu ozel bir registry'e yayinla ve ona surumle bagimli ol.

Paylasim depo ya da ekip sinirlarini astiginda, ya da tuketicilerin degisiklikleri kendi takvimlerinde benimsemesi gerektiginde dogru. Maliyeti, paylasilan kodu degistirmekle kullanmak arasina giren bir yayin adimidir; bu da aktif gelistirme sirasinda surtunmedir — ekiplerin siklikla buradan baslayip paylasilan kod hala calkalanirken pisman olmalarinin sebebi budur.

Makul bir orta yol: paylasilan kod kararsizken monorepo'da tut, oturduktan sonra bir pakete cikar.

## Her durumda gecerli kurallar

- **Her eklenti kendi manifest'ini, surumunu, degisiklik gunlugunu ve `.vsix`'ini korur.** Eklentiler kullanicilar tarafindan bagimsiz kurulur ve guncellenir; bir yayini paylasamazlar.
- **Paylasilan kod `vscode`'u import etmemeli** — her tuketici bir eklenti degilse ve bu bagi kabul etmiyorsan. `vscode` import'u olmayan saf mantik, extension host olmadan test edilebilir — cok daha hizli, ve zaten paylasilmaya en deger kod odur.
- **`engines.vscode` eklenti basinadir.** Paylasilan kod tuketiciler arasindaki *en dusuk* tabana karsi calismak zorundadir; bir API cagrisi eklerken unutulmasi kolay olan sey budur.
- **Her eklenti kendi `.vsix` incelemesini alir.** Biri dogru paketlendi diye kardesinin de paketlendigini asla varsayma.

## Sonradan gecis

Ayri depolardan monorepo'ya gecmek mekaniktir: dizinleri tasi, workspace yapilandirmasini ekle, paylasilan paketi cikar, import'lari duzelt. Git gecmisini korumak caba ister (subtree merge'ler) ama kod hareketi dosdogrudur.

Ters yon — bir monorepo'yu bolmek — daha zordur, cunku ortuk baglilik birikir: paylasilan config, paylasilan derleme varsayimlari, kimsenin fark etmedigi capraz import'lar.

**Bu yuzden secim gercekten yakinsa ayri baslayin.** Daha ucuz olan gecis, ihtiyac duymaniz daha muhtemel olandir.
