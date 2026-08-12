---
name: ciktinin-kalici-evi
description: Üretilen bir rapor/karar oturumluk taşıyıcıda kalırsa kaybolur — kanal taşıyıcıdır, kayıt değildir
metadata:
  type: feedback
---

**Bir denetim raporu, karar ya da gereksinim cevabı üretildiğinde kalıcı kayda
geçer. Kanal TAŞIYICIDIR, kayıt değildir.**

**Why:** kanal oturumluk — oturum kapanınca arşive gömülür ve sonraki oturum
onu bulamaz. Ölçüldü (2026-08-12), **iki bağımsız vaka aynı gün:**

- QA'nın PRC-41 RED raporu yalnız kanala yazıldı → ertesi gün PA aradı,
  bulamadı, sordu. Clara arşivi kazıp çıkardı.
- Bir karar cevabı (S0 sınır kararı) hiçbir yere yazılmadı → geriye yalnız
  *"S0 cevaplandı"* **beyanı** kaldı, içeriği yok.

PA'nın çıkarımı: ***"Aynı hata iki kez olduysa taşıyıcı değil DÜZEN sorunu
demektir."***

**Kanonda karşılığı YOK ve üç agent bağımsız buldu** (BE · QA · CA). Üç kural
birlikte bir kapan üretiyor: `HANDOFF-SCREEN-ONLY` (dosyaya yazma yasak) +
`MEMORY-POINTER-ONLY` (memory'ye yasak) + `HANDOFF-CLOSE-NOTE-ROUTING` (dört ev
sayıyor, hiçbiri denetim raporuna uymuyor).

CA'nın ince düzeltmesi: *"'Kural yok' DEMİYORUM — `impact-analysis:65`'te VAR
ama **'## Referans' başlığı altında**, akış adımı değil. **Adım olsaydı
atlanamazdı.**"*

**How to apply:** kendi işimde de geçerli. Bir ölçüm, karar ya da bulgu
ürettiğimde *"bu nerede yaşayacak"* sorusunu **üretirken** sorarım, sonra değil.
Sahada bir agent rapor üretiyorsa ClickUp yorumuna geçirmesini isterim —
adres vermek yetmez, **içerik kalıcı katmanda durmalı.**

Ve kayıt taşınırken: **sınıfı kaynak belirler, taşıyan değiştiremez.**
QA'nın cümlesi — *"gözlemi düşürmek taşıma değil SÜZME'dir."*

İlgili: [[feedback_dogru_katmana_yaz]] · [[feedback_kayit_kapanis_notu]]
