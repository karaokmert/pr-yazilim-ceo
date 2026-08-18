# Karar — plugin sürümü ertelendi (v8 OY)

**Tarih:** 2026-08-16 17:59 · **Karar mercii:** Mert

## Durum

`v8/ozel-yazilim` plugin'i **v0.7.0**'da duruyor. Ölçüldü: v0.7.0'dan (`3c3ea81`)
beri o dizinde **sekiz commit** birikmiş.

| Commit | Ne |
|---|---|
| `4aa1735` | prod akışı tek zincir, `deploy-release` → `dev-deploy` |
| `22a235a` | PA/QA/DO body'lerine dev+prod yükleme emri |
| `c09a78a` | 18 dosyada cascade — atıf yönlendirme + kimlik senkronu |
| `fc2d2d8` · `cce5b46` · `2570de9` | üç denetim turunun düzeltmeleri |
| `c7dd3d3` · `5c5810d` | açılış paragrafı + iki PQA bulgusunun düzeltmesi |

## Karar

**Sürüm bugün artırılmıyor.** Açık kalemlerden bazıları da body'lere dokunacak;
hepsi bitince **tek sürüm** çıkılacak.

## ⚠️ Bilinen bedel — kayda geçiyor

Ekip `/plugin update` dediğinde bu sekiz değişikliğin **hiçbirini almıyor.** Sahada
**12 Ağustos'taki hâl** çalışıyor.

Symlink dönemindeki *"anında aktif"* davranış bitti (CLAUDE.md §3) — kaynağa yazmak
sahaya indirmiyor, plugin sürümü gerekiyor.

**Bugünkü iyileştirme repoda var, sahada yok.** Bu bilinçli bir erteleme, unutulmuş
bir adım değil.

## Ne zaman yeniden gündeme gelir

Açık kalemlerin kapanışında. Bekleyen altı kalem:

- **Tip 2 gövdesi** — ölçüm negatif çıktı, karar Mert'te
- **BE 64↔94** — SQL-MIGRATION *"atomik commit"* mi *"LOCAL, commit'lenmez"* mi
- **BE 107↔108** — *"PA'ya BİLGİ YAZMAZSIN"* vs *"sistemik bug → PA'ya BİLGİ"*
- **"Alan → skil" haritası** — dört body'de var, beşinde yok
- **`/sendmessage` push satırı** — karar verildi (PQA atar), komut metni düzeltilmedi
- **İletimi kim yapar** — `ISD-RELAY-DONT-CALL` vs komutun 8/11. adımı

İlk dördü body'lere dokunuyor — sürüm onlardan sonra.

## Sürüm basamağı — henüz seçilmedi

Sekiz commit içinde kırıcı değişiklik var mı ölçülmedi. Basamak (minor/major) sürüm
turu açıldığında seçilecek.

Not: 14 Ağustos sabahı bir `/remember` kaydında *"0.8.0 bump önerildi"* satırı var —
o gün konuşulmuş, yapılmamış.
