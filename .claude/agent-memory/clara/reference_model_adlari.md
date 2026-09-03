---
name: model-adlari
description: Claude Code'da gecerli model adlari - olculdu, tahmin edilmesin; frontmatter'da sondaki bosluk sessizce dusuruyor
metadata:
  type: reference
---

Bir agent gövdesinin frontmatter'ında `model:` alanına yazılacak değer **ölçülerek**
belirlenir, hatırlanarak değil. Ölçüm yolu: `claude --model <ad> -p "ok"` — geçersiz ad
açık cevap veriyor (*"It may not exist or you may not have access to it"*).

**2026-09-03'te ölçülenler:**
- `fable` — çalışıyor (alias, en güncel sürüme bağlanır)
- `claude-fable-5` — çalışıyor (tam ad, sürümü sabitler)
- `claude-fable-5.1` — **YOK**, reddediliyor

`claude --help` çıktısı da aynı biçimi söylüyor: alias (`fable`, `opus`, `sonnet`) ya da
tam ad (`claude-fable-5`).

**Why:** Mert "fable 5.1" istedi; böyle bir ad yok. Kabul edip yazsaydım model sessizce
düşecekti — hata vermez, öyle durur. Ölçmek beş saniye sürdü.

**How to apply:** Bir frontmatter'a model adı yazmadan önce o adı çalıştırıp gör.
Ve ⚠️ **sondaki boşluğa dikkat** — `model: fable ` YAML'da `"fable "` olur, eşleşmez,
sessizce düşer. Aynı tuzak bu dosyada bir kez yaşandı.

İlgili: [[feedback_olcum_yerine_yorum]] · [[feedback_aracin_ne_olctugu]]
