# Paketleme ve Yayinlama

`@vscode/vsce` ve `ovsx` mekanigi. Karar kurallari ve yayin zinciri ust SKILL.md icinde.

**CLI gercekleri icin dokumana degil ikili dosyaya guven.** `vsce --help` ve `vsce package --help`, dokumantasyon sayfasindan daha fazla bayrak raporlar ve fiilen kurulu olan surumu tarif ederler. Burada yazan bir sey ikilinin soyledigiyle celisiyorsa ikili kazanir — yeniden calistir.

## Icindekiler

- [Kurulum](#kurulum)
- [Paketleme](#paketleme)
- [.vsix'i incelemek](#vsixi-incelemek)
- [Kimlik dogrulama (degisiyor — bunu oku)](#kimlik-dogrulama-degisiyor--bunu-oku)
- [Marketplace'e yayinlamak](#marketplacee-yayinlamak)
- [On-surumler](#on-surumler)
- [Platforma ozgu paketler](#platforma-ozgu-paketler)
- [Imzalama ve dogrulama](#imzalama-ve-dogrulama)
- [Open VSX](#open-vsx)
- [Ic dagitim](#ic-dagitim)

## Kurulum

```bash
npm install --save-dev @vscode/vsce
# ya da kurmadan cagir:
npx @vscode/vsce package
```

`vsce` modern bir Node gerektirir — README'si ve paket metadata'si tam alt sinir konusunda celisti (22.x'e karsi >=20), bu yuzden bir engine hatasi alirsan iki dokumana degil hataya guven. Desteklenen paket yoneticileri npm ve yarn 1.x'tir.

## Paketleme

```bash
vsce package
vsce package --out dist/my-extension.vsix
vsce package --pre-release
```

Bilinmeye deger bayraklar:

| Bayrak | Kullanim |
|---|---|
| `--out <yol>` | Cikti konumu |
| `--pre-release` | On-surum olarak isaretle |
| `--no-dependencies` | `node_modules`i paketlemeyi atla — zaten bundle edilmis eklentiler icin |
| `--target <hedef>` | Platforma ozgu derleme |
| `--allow-star-activation` | `activationEvents` `*` iceriyorsa zorunlu |
| `--allow-missing-repository` | `repository` yoksa zorunlu |
| `--skip-license` | LICENSE dosyasi yoksa zorunlu |
| `--ignoreFile <yol>` | `.vscodeignore` yerine bir alternatif kullan |
| `--readme-path`, `--changelog-path` | Varsayilan olmayan dokuman konumlari |

**`--no-dependencies` uzerine:** eklenti bundle edildiginde (esbuild/webpack) tum calisma zamani `dist/` icinde yasar ve `node_modules` zaten `.vscodeignore` ile dislanmis olmalidir. `--no-dependencies` gecmek bunu acik yapar ve paketlemeyi hizlandirir. Bu eslestirme belgelenmis bir kuraldan cok yaygin bir uygulamadir — yetkili kontrol, bayrak degil ortaya cikan paketi incelemektir.

**`--allow-*` bayraklarini duzeltme degil soru olarak ele al.** Her biri bir sebeple var olan bir korumayi bastirir. `--allow-star-activation`a uzanmak aktivasyon stratejisinin bir daha bakilmayi hak ettigi anlamina gelir; `--allow-missing-repository` ve `--skip-license` ic eklentiler icin savunulabilir ve yayinlananlar icin birer bosluktur.

## .vsix'i incelemek

**Her yayinda zorunlu.** Temiz bir cikis kodu icerik hakkinda hicbir sey soylemez.

```bash
# Derlemeden neyin dahil edilecegi
vsce ls

# Uretilmis bir paketi incele (bir .vsix bir zip'tir)
unzip -l my-extension-0.1.0.vsix

# Cikar ve etrafina bak
mkdir -p /tmp/vsix-check && unzip -q my-extension-0.1.0.vsix -d /tmp/vsix-check
find /tmp/vsix-check -type f | sort

# Boyut kontrolu
du -h my-extension-0.1.0.vsix
```

Listeye karsi kontrol listesi:

- **Yok**: `src/`, `**/*.ts` (gondermek istedigin bildirimler haric), testler, fixture'lar, `.env`, `.git`, dev `node_modules`, derleme config'leri, ic notlar.
- **Var**: `main`/`browser`in isaret ettigi dosya, `package.json`, `README.md`, `CHANGELOG.md`, `LICENSE`, ikon ve her calisma zamani varligi — webview HTML/CSS/JS, gorseller, gramerler, dil yapilandirmasi.
- **Boyut**: paketlenmis bir eklenti genelde 1 MB'in oldukca altindadir. Onlarca megabyte, `node_modules`in girdigi anlamina gelir.

En yuksek degerli kontrol calisma zamani varliklaridir. Eksik kod genelde hemen ve bariz sekilde basarisiz olur; eksik bir webview stil sayfasi ya da gramer dosyasi ise sorunsuz yuklenen ve her kullanici icin ince sekilde bozuk olan bir eklenti uretir.

**Sonra paketi kur ve calistir:**

```bash
code --install-extension my-extension-0.1.0.vsix --force
```

Aktive oldugunu ve ana komutunun calistigini dogrula. Bozuk bir paketle dogru bir kod tabanini yakalayan tek kontrol budur.

## Kimlik dogrulama (degisiyor — bunu oku)

Tarihsel olarak yayinlama bir Azure DevOps Personal Access Token kullandi:

```bash
vsce login <publisher>
# ya da
VSCE_PAT=<token> vsce publish
```

**Azure DevOps'taki global PAT'lar emekliye ayriliyor; duyurulan tarih 2026-12-01.** `vsce login` / `VSCE_PAT` uzerine kurulu her seyin bir son tarihi var.

Yerine gelen Microsoft Entra ID:

```bash
# Etkilesimli / servis sorumlusu
vsce publish --azure-credential

# GitHub Actions, hicbir saklanan sir olmadan
vsce publish --oidc
```

Workload identity federation ile `--oidc`, CI icin en iyi secenektir: hicbir yerde uzun omurlu hicbir sey saklanmaz. Yeni her kurulum icin bunlari tercih et ve mevcut bir PAT hattini calismaya devam edecek bir sey degil planlanmis is olarak ele al.

## Marketplace'e yayinlamak

```bash
vsce publish                  # package.json surumunu kullanir
vsce publish minor            # artir, etiket commit'le, yayinla
vsce publish 1.2.3            # acik surum
vsce publish --packagePath my-extension-1.2.3.vsix   # incelenmis bir urunu yayinla
```

**`--packagePath`'i tercih et** ki farkli olabilecek taze bir derlemeyi degil, inceledigin ve kurdugun tam urunu yayinlayasin.

`--skip-duplicate`, surum zaten varsa hatayi onler — CI yeniden kosumlarinda kullanislidir.

Diger komutlar: `vsce ls-publishers`, `vsce verify-pat`, `vsce show <ext-id>`, `vsce unpublish <ext-id>`.

**Yayindan kaldirmak, eklentiyi zaten kurmus makinelerden kaldirmaz.** Geri cagirma yoktur. Yayin zincirinin hatada durmasinin tum sebebi budur.

## On-surumler

```bash
vsce publish --pre-release
```

**Semver on-surum etiketleri desteklenmez** — bir surum duz `major.minor.patch` olmalidir. `1.2.0-beta.1` reddedilir. Pazar yeri konvansiyonu on-surum icin tek sayili minor surumleri kullanmaktir (`1.3.x` on-surum, `1.4.x` kararli); ekip bunu benimserse tutarli tut, cunku on-surumlere dahil olan kullanicilar en yenisi neyse onu alir.

## Platforma ozgu paketler

Yalnizca eklenti yerel binary'ler ya da platforma ozgu bagimliliklar gonderdiginde gereklidir.

Hedefler: `win32-x64`, `win32-arm64`, `linux-x64`, `linux-arm64`, `linux-armhf`, `alpine-x64`, `alpine-arm64`, `darwin-x64`, `darwin-arm64`, `web`.

```bash
vsce package --target darwin-arm64
vsce publish --target win32-x64 win32-arm64
```

VS Code eslesen derlemeyi otomatik sunar. Saf TypeScript bir eklentinin bunlarin hicbirine ihtiyaci yoktur — tek bir evrensel paket her seyi kapsar.

Web eklentileri icin VS Code, web yetenegini manifest seklinden (bir `browser` giris noktasi) etiketler, bu yuzden acik bir `--target web` genelde gerekmez.

## Imzalama ve dogrulama

**Marketplace her eklentiyi yayin aninda imzalar — anahtar yonetmezsin.** VS Code imzayi kurulumda ve guncellemede dogrular; 1.100'den beri tum platformlarda zorunludur.

Operasyonel anlami: kullanicilar `PackageIntegrityCheckFailed`, `SignatureIsInvalid` ya da `NotSigned` ile kurulum hatalari bildirirse, problem onlarin VS Code'u degil paket butunlugu ya da teslim yoludur. (`extensions.verifySignature` kontrolu kapatabilir ama bunu bir kullaniciya onermek kotu tavsiyedir — korumayi global olarak devre disi birakir.)

`vsce generate-manifest` ve `vsce verify-signature` gerekirse yerel dogrulama icin mevcuttur.

1.97'den beri, ucuncu taraf bir eklentinin ilk kurulumu bir yayinciya-guven istemi gosterir.

## Open VSX

VSCodium ve diger uyumlu editorlere hizmet eden ayri bir kayit defteri (Eclipse Foundation). **VS Code'un dokumantasyonu bunu kapsamaz** — oraya bakma ve pazar yeri kurallarinin tasindigini varsayma.

```bash
npm install -g ovsx
ovsx create-namespace <namespace>       # tek seferlik
ovsx publish my-extension-0.1.0.vsix -p <token>
ovsx verify-pat <namespace>
```

Publisher yerine namespace kullanir. Marketplace'e yayinlamak buraya yayinlamaz — tamamen bagimsizdirlar. Ikisi de hedefse ikisini de acikca yap ve raporda soyle.

## Ic dagitim

```bash
code --install-extension /path/to/my-extension-0.1.0.vsix
code --install-extension /path/to/ext.vsix --force   # mevcut olanin uzerine yaz
```

Ya da Komut Paletinde **Extensions: Install from VSIX**.

**VSIX ile kurulmus eklentiler icin otomatik guncelleme kapalidir.** Meslektaslar aksi soylenmedikce ilk kurulumlarinda suresiz kalir. Onlemler: guncellemeleri insanlarin okudugu bir kanalda duyur, surumu eklentinin kendi ciktisinda gorunur yap ki hata raporlari derlemeyi tanimlasin ve eski `.vsix` dosyalarini sakla ki kotu bir yayin oncekini yeniden kurarak geri alinabilsin.

Bir paketi izole olarak test etmek icin kullanisli CLI bayraklari:

```bash
code --list-extensions --show-versions
code --disable-extensions                    # digerlerinin hepsi kapali baslat
code --extensions-dir /tmp/x --user-data-dir /tmp/u   # tek kullanimlik ortam
code --profile <ad>                          # adlandirilmis, atilabilir bir profil
```

`--extensions-dir` + `--user-data-dir` cifti, kendi kurulumunu bozmadan gercekten temiz bir ortama karsi bir kurulumu test etmenin guvenilir yoludur.
