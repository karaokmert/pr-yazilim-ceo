---
name: sessizlik-yoklamasi
description: Bir agent 5 dakikadan fazla sessizse yoklanır — aktif kaldığı doğrulanır (Mert, 2026-08-10)
metadata:
  type: feedback
---

Bir agent'tan **5 dakikadan fazla** yanıt gelmezse yoklanır: *"devam ediyor
musun?"* Mert'in talimatı, 2026-08-10 gece: *"5 dk'dan fazla yanıt gelmezse
agent'a devam ediyor musun diye soru sor, aktif kaldıklarına emin ol."*

**Why:** Agent oturumu sessizce ölebiliyor ya da bir şey bekliyor olabiliyor, ve
**sessizlik iki farklı şeyi aynı gösteriyor** — "çalışıyor" ile "durdu". Gözetimsiz
bir gecede fark edilmeyen bir durma, bütün geceyi boşa çıkarır.

**How to apply:** Bekleme süresi 5 dakikayı aşarsa kanaldan yokla (kendi kutusuna
kısa bir `QUESTION`). Yoklama **iş vermez**, yalnız canlılık sorar. Cevap gelirse
devam; gelmezse süreç ölçülür (`ps`) ve durum Mert'e bildirilir.

**Ölçmeden önce yoklama yapılmaz sanılmasın** — tersi de doğru: sessizliğin
sebebi tahmin edilmez. Kanonda zaten var: *"sessizliğin sebebi tahmin edilmez,
sorulur."* Bu kural ona bir **eşik** veriyor (5 dk) ve gözetimsiz çalışmada
zorunlu kılıyor.

⚠️ Yoklama gürültü de üretebilir: agent kod yazarken kutusuna bakmıyor, yoklama
cevabı gecikir. O yüzden yoklama **iş akışını kesmez** — bir sonraki turda cevap
gelirse yeterli. Üst üste iki yoklamaya cevap yoksa süreç ölçülür.

Bkz. [[akisi-bloklamayin]] — bekleyen taraf Clara olmamalı; yoklama beklemeyi
görünür kılar, uzatmaz.
