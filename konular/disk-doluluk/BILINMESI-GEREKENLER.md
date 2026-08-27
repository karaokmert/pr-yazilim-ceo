# Disk doluluğu — web-sitesi klasörü ve build cache'leri

**Ölçüm ve temizlik tarihi: 2026-08-27.**

## Sorunun teşhisi — sanılandan farklı

Mert'in sorusu "her projede bir sürü node sürümü oluşuyor" şeklindeydi.
**Node sürümü sorun değil:** makinede iki node var (nvm v20.20.2, homebrew
v22.23.1), ikisi birkaç yüz MB.

Gerçek sebep: her proje kendi `node_modules`'ını ve kendi **build cache**'ini
yerelde tutuyor, ve build cache'i hiç temizlenmiyor.

## Ölçülen dağılım (temizlik öncesi, 72 GB)

| Ne | Boyut | Adet |
|---|---|---|
| `.turbo` build cache | **43 GB** | 58 |
| `node_modules` | 20 GB | 140 |
| `.next` | 11.5 GB | 26 |
| `~/.npm` global cache | **19 GB** | (klasör dışı) |

`dist` / `build` / `.astro` toplamı 130 MB — ihmal edilebilir.

**Tek kaynak baskın:** `web-template-next/.turbo` tek başına **27 GB**.
Diğer tüm projelerin `.turbo` toplamı 16 GB.

## Yapılan (Mert onayıyla: "önce sil, sonra konuşalım")

Silinen: tüm `.turbo` + tüm `.next` + `npm cache clean --force`.
Dokunulmayan: kaynak kod, commit'ler, `node_modules`.

**Sonuç: web-sitesi 72 GB → 17 GB · `~/.npm` 19 GB → 2.3 GB · disk %14 kullanımda.**

Tek bedeli: her projenin bir sonraki build'i cache'siz koşar.

## ⚠️ SEBEP DURUYOR — bu temizlik kalıcı değil

Turbo cache'inde üst sınır tanımlı değil; her build yeni katman bırakıyor ve
hiçbiri silinmiyor. `web-template-next` 27 GB'a böyle çıktı. Birkaç hafta
içinde aynı yere geri döner.

**Bu bir yama, sebebin kaldırılması değil.** Eksinin yanına artı konuldu.

## Turbo cache limiti — YAPILDI (2026-08-27)

Turbo 2.10 kurulu. İki alan var, ikisi de **kök seviyesinde** (`tasks`'ın içine
değil, yanına). Kaynak: turborepo.dev/docs/reference/configuration — dokümandan
doğrulandı, hatırlamayla değil.

```jsonc
{
  "$schema": "https://turbo.build/schema.json",
  "cacheMaxSize": "2GB",
  "cacheMaxAge": "7d",
  "ui": "tui",
  "tasks": { ... }
}
```

Eviction her `turbo run` başında **arka planda** koşar, işi bloklamaz. İkisi
birlikte tanımlıysa önce yaş, sonra boyut eviction'ı işler.

**Nereye yazıldı:** `web-template-next/turbo.json` (Mert'in kararı: "ondan
türetilenlerde çözülmüş olur").

⚠️ **Geriye dönük değil.** `turbo.json` miras alınmaz, KOPYALANIR. Template'ten
bundan sonra türetilen projeler limiti taşır; **zaten türetilmiş 18 proje
taşımaz.** Onlar bugün sıfırdan başlıyor (hepsi silindi) ama limitsizler —
`trendyol-siparis` 3 GB'a, `mucizeler-merkezi-next` 2.9 GB'a çıkmıştı, birkaç ay
sonra yine oraya gelirler.

19 projede `turbo.json` var: balkanbee · mucizeler-merkezi-next ·
web-template-next · trendyol-siparis · yalinnetwork · karaokymm ·
durudiagnostik-new · prproject-managment · demosite · web-template ·
trendyol-siparis-2 · adalya-IT · btproduct · cevizioex · gazi-template ·
PR-redesign · rundevu · karaokai · pryazilim-crm

## Kalıcı çözüm için açık kalan iki iş

1. **Mevcut 18 projeye limit yayılımı** — yukarıdaki listede web-template-next
   dışındakiler. Elle yazmak sürdürülebilir değil; toplu bir hamle gerekiyor.
2. **npm → pnpm geçişi** — 20 projede `pnpm-lock.yaml`, 12'sinde
   `package-lock.json` var. pnpm bağımlılıkları tek global store'da tutup
   hardlink verir (20 proje aynı React'i bir kez saklar). Ama `~/.npm` 19 GB'a
   çıkarken `~/Library/pnpm` 3.4 GB'de kalmıştı — o 12 npm projesi pnpm'in
   kazancını yiyor. ⚠️ Geçişin riski var, ayrı bir iş.
3. **Periyodik temizlik düzeni** — dokunulmayan projelerin `node_modules`'ını
   ve build cache'ini otomatik silen bir mekanizma

Mert bu turda üçünü de ertelemeyi seçti — "önce sil, sonra konuşalım".

## Tekrar ölçmek gerekirse

```
cd /Users/karaok/p/web-sitesi
find . -name .turbo -type d -not -path "*/node_modules/*" -prune -exec du -sk {} + | sort -rn | head
```

---

# ozel-yazilim klasörü — aynı gün, farklı şişme (2026-08-27)

Mert sordu: "~/p/ozel-yazilim'da da var mı böyle bir şişme?" **Vardı: 66 GB.**

## Şişmenin şekli FARKLI

`web-sitesi`'nde suçlu turbo build cache'iydi. Burada **.NET derleme çıktısı**:

| Ne | Boyut | Adet |
|---|---|---|
| `bin/` + `obj/` (.NET) | **29.5 GB** | 238 |
| `node_modules` | 21 GB | 59 |
| `.next` + `.turbo` | 9.6 GB | 30 |
| `Pods` (iOS) | 2.8 GB | 3 |

⚠️ **Ölçüm tuzağı:** ham `find` `dist`'i 7.4 GB / `build`'i 4 GB gösterdi ama
%99'u `node_modules` içindeydi — ayrı bir yük değil. Aynı şekilde 900 `bin/`
klasörünün 662'si `node_modules/.bin`, toplam 40 MB. **`-not -path
"*/node_modules/*"` olmadan bu ölçüm yanıltıyor.**

En büyükler: wupdoc 13 GB · deliverigo 9.8 · goat 9.2 · liston 8.7 · osinif 6.6

## Silmeden önce doğrulanan

`bin/` içeriği `Debug`/`Release` — saf derleme çıktısı. Altı projede
(wupdoc, deliverigo, goat, liston, osinif, egelisaglik) `git ls-files` ile
bakıldı: **sıfır takipli** `bin`/`obj` dosyası, hepsinin `.gitignore`'unda
tanımlı. Silinmesi commit'leri etkilemiyor.

## Yapılan (Mert onayıyla: "Hepsi — 39 GB")

Silinen: `bin` + `obj` + `.next` + `.turbo` (node_modules dışı).
Dokunulmayan: kaynak kod, `node_modules`, `Pods`.

**Sonuç: 66 GB → 27 GB.**

⚠️ **web-sitesi'nden farkı:** orada silinen şey cache'ti, maliyetsizdi. Burada
`bin/` silmek o projelerin bir sonraki `dotnet build`'ini sıfırdan koşturur —
`make dev` / telepresence akışı yeniden derleme bekler.

## Günün toplamı

**web-sitesi 72→17 GB · ozel-yazilim 66→27 GB · ~/.npm 19→2.3 GB**
Disk kullanımı %14 → **%12**, boş alan 86 GB.

## ⚠️ Burada da sebep duruyor

.NET `bin`/`obj` her build'de yeniden dolar ve hiçbir üst sınırı yok — turbo'nun
`cacheMaxSize`'ı gibi bir karşılığı da yok. Tek çözüm periyodik `dotnet clean`
ya da dokunulmayan projeleri süpüren bir düzen. Bu da açık iş listesinde.

---

# ~/p geneli — üçüncü tur (2026-08-27)

Mert sordu: "~/p'de başka silinebilir gereksiz şeyler var mı?"

## Ölçülen (iki büyük klasör zaten temizlenmişken, ~/p = 47 GB)

| Aday | Boyut | Karar |
|---|---|---|
| `node_modules` toplamı | 37 GB (141 adet) | 60+ gün dokunulmamış 66 tanesi silindi |
| `.vscode-test` | 1.8 GB | **Silindi** (ayrı turda, aşağıda) |
| Boş klasörler (`trash`,`temp`,`friends`) | ~0 | **Silinmedi** |

`.vscode-test`: `vsx-clickup-panel` ve `vsx-agent-panel`'in her birinde 900 MB.
VS Code test binary cache'i, test koşulunca yeniden iner — bedelsiz silinebilir.
`pr-yazilim-ceo`'nun 1.96 GB'ının neredeyse tamamı buydu.
**Sonradan silindi: `pr-yazilim-ceo` 1.96 GB → 174 MB.**

## Yapılan (Mert onayıyla)

`find ~/p -name node_modules -type d -prune -mtime +60 -exec rm -rf {} +`

**Sonuç: ~/p 48 → 35 GB.** Kalan 86 `node_modules` = 24.7 GB (son 60 günde
dokunulan aktif projeler).

⚠️ Bedeli: o projelere dönüldüğünde `pnpm install` gerekiyor. Listede
`adalya-IT` ve `yalinnetwork` de vardı — bu ikisinde symlink dönüşümü hâlâ
commit'siz bekliyor (bkz. `konular/web-sitesi-repo-durumu/`).

⚠️ `-mtime +60` filtresi doğru çalıştı: `liston/src/mobile-app` (2.36 GB) ve
`osinif/src/web-admin` (1.23 GB) listede ÇIKMADI — aktif projeler.

## GÜNÜN TOPLAMI

| | Önce | Sonra |
|---|---|---|
| `web-sitesi` | 72 GB | 17 GB |
| `ozel-yazilim` | 66 GB | 27 GB |
| `~/.npm` | 19 GB | 2.3 GB |
| **Disk boş** | ~19 GB | **95 GB** |

(`.vscode-test` de silindikten sonraki son hâl.)

## Yan bulgu — silme konusu DEĞİL

`~/p/docs/` altında `AuthKey_544L52H86W.p8` var — Apple imzalama anahtarı.
Kaybolursa yenisi üretilemez — Apple `.p8` anahtarını bir kez indirtir, sonra
yalnız yenisini oluşturmaya izin verir ve eskisi iptal olur. Yedeği olup
olmadığı **bilinmiyor, ölçülmedi.** Nerede kullanıldığı da taranmadı.

Mert "silelim onu da" dediğinde hedef belirsizdi (`.vscode-test` mi `.p8` mi)
ve soruldu — `.vscode-test` çıktı. **`.p8` yerinde duruyor, dokunulmadı.**

⚠️ Açık kalan: bu anahtarın yedeği var mı, hangi projede kullanılıyor.
