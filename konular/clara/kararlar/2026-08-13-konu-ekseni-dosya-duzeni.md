# Dosya düzeni konu eksenine geçti — yazma ve okuma birleşti

**Karar veren:** Mert · **Tarih:** 2026-08-13 · **Durum:** uygulandı

## Sorun — ölçüldü

Mert'in tespiti: *"dosya yapın çok dağınık Clara, nerede ne var bilmiyorsun ve iş
geldiğinde de oraya gidip okumuyorsun."*

Üç ölçüm yapıldı ve teşhisi doğruladı:

1. **%88'i yazılıp unutulmuş** — 64 dosya bir kez yazılmış, bir daha hiç dokunulmamış
   (git geçmişi: tek commit). Arşiv değil mezarlık.
2. **Bir konu 79-127 dosyaya dağılmış** — `clickup` 79, `fabrika` 127, `kanal` 118
   dosyada geçiyor. Hiçbirinin evi yok.
3. **Yazma ve okuma farklı eksende.** Yazarken sorulan: *"bugün ne oldu"* (günlük) ·
   *"ne karar verdik"* (kararlar) · *"ne ölçtük"* (incelemeler) — hepsi **olay ekseni.**
   Okurken sorulan: *"ClickUp düzeni için ne yapmıştık?"* — **konu ekseni.**

Mert'in soruları bunu açığa çıkardı: *"günlüğe sonradan ne için bakıyorsun? Yaptığın
işler gruplanıyor mu? Üç ay sonra bir iş geldiğinde orada üç ay öncesinin dosyasını
bulup ne yapmışız kaç kere değiştirmişiz ne kararlar almışıza bakman gerektiğini
biliyor musun?"* — Cevap: hayır.

## Karar

**Dosyalar konu ekseninde durur.** `konular/{konu}/` altında sekiz konu:
`clara` · `agent-kanonu` · `fabrika` · `clickup-is-takibi` · `kanal-iletisim` ·
`memory-duzeni` · `olcum-arama` · `saha-yonetimi`

Her konunun **tek yaşayan dosyası** var: `KONU.md`. Altında `kararlar/` ·
`incelemeler/` · `fikirler/`.

**Yazma refleksi:** iş bitince *"bu hangi konunun dosyası"* diye sorulur,
*"bugünün günlüğü nerede"* diye değil.
**Okuma refleksi:** işe başlarken o konunun `KONU.md`'si **açılır.**

Aynı soru iki yerde de sorulur — eksen birleşir.

## Neden CLAUDE.md'ye değil body'ye yazıldı

Mert'in kararı: *"bunu CLAUDE.md'ye değil de kendi body'ne yazsana daha iyi olur."*

Gerekçe: **body her oturumda yüklenir.** CLAUDE.md'ye yazılan bir kural okunmayabilir —
ki bu düzenin çözmeye çalıştığı arızanın ta kendisi olurdu.

## Arşiv disiplini

Mert: *"arşiv içinde artık önemsiz olan şeyleri tutma. Karar aldık uygulandı bittiyse
uzun uzun raporu kalmasın."*

**Uygulanmış bir kararın uzun raporu tutulmaz** — karar ve gerekçesi yeter. Ayrıntılı
rapor ancak hâlâ **açık** bir işin dayanağıysa saklanır.

## Ne yapıldı

- 53 karar + 19 inceleme + 6 fikir klasörü konulara dağıtıldı
- Sekiz `KONU.md` üretildi (kararlar tarih sıralı, özetleriyle)
- Araçlar ayrıldı: `tools/`, `panel/`, `arge/*.py`, `sprint/*.py` → `araclar/`
- Çıktılar ayrıldı: `takvim-doktor.png`, QR dosyaları → `varliklar/`
- Kök dizin **11 klasörden 8'e** indi
- `HARITA.md` ikincil oldu: yalnız açık/yarım işler (kapalılar `HARITA-ARSIV.md`'de)

**İçerik kaybı yok** — hiçbir şey silinmedi, taşındı.
