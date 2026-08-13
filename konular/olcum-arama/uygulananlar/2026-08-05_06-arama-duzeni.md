# Arama düzeni — UYGULANDI (2 karar)

**Süre:** 2026-08-05 → 08-06

## 1. Ne yapıldı
**Qdrant ayrı vektör alanı kullanır** (5 Ağt) — bu odanın kayıtları başka projelerin
koleksiyonuyla karışmaz.
**Arama disiplini kurala bağlandı** (6 Ağt): bildiğin kelime → `grep` · niyet sorusu →
vektör · liste sorusu → `ls`.

## 2. Neden öyle
Yanlış araç **sessizce** yanlış cevap veriyor. Vektörün üç körlüğü ölçüldü:
çıktısı cevap değil **adres** · **skor alakayı ölçmez** · eskimiş kayıt soruya daha
benzer görünür (sorunu ayrıntılı anlatır, taze kayıt *"çözüldü"* diye kısa geçer).

## 3. Nerede yaşıyor
`.claude/skills/arama-disiplini/` · `.claude/settings.local.json` (Qdrant koleksiyonu)

---
> 2 karar dosyası özetlendikten sonra `.trash`'e alındı.
