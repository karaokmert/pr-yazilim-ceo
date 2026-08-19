# Karar — esbuild 0.24 açığı kabul edildi (VSX Agent Panel)

**Tarih:** 2026-08-18 · **Karar veren:** Mert · **Getiren:** VSX Architect → Clara

## Ne

`vsx-agent-panel` projesinde `esbuild 0.24` bir orta seviye açık taşıyor:
**GHSA-67mh-4wv8-2f99** — geliştirme sunucusu her siteden istek kabul ediyor.
Düzeltmesi `esbuild 0.28`'e **kırıcı (breaking) geçiş** gerektiriyor.

## Karar

**Kayda geçilip devam edildi.** Şimdi güncellenmeyecek.

## Gerekçe

Açık esbuild'in **dev server**'ını etkiliyor; bu projede dev server kullanılmıyor,
esbuild yalnız bundle üretiyor. Ayrıca `devDependency` olduğu için üretilen
`.vsix` paketine **girmiyor** — sahaya çıkan ürüne etkisi yok. Risk geliştirici
makinesiyle sınırlı ve dar.

## Ne zaman yeniden bakılır

- Projede bir dev server kullanılmaya başlanırsa
- esbuild başka bir sebeple güncellenecekse (0.28 geçişi o turda yapılır)
- Eklenti public marketplace'e çıkarılacaksa (dağıtım niyeti değişirse)

## Kaynak

Architect'in devir bloğu, 2026-08-18 21:42 — `npm audit` çıktısına dayanıyor.
Architect kararı kendi vermedi, merkeze taşıdı; bu doğru davranıştı.
