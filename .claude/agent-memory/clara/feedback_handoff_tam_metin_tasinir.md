---
name: handoff-tam-metin-tasinir
description: Handoff ekrana basılır dosyaya yazılmaz — merkez adresi değil TAM METNİ taşır (2026-08-11)
metadata:
  type: feedback
---

Bir agent'ın hazırladığı handoff **ekrana basılır, dosyaya yazılmaz** (kanon böyle).
Dolayısıyla merkez onu hedefe taşırken **adres veremez — tam metni taşımak zorundadır.**

**Why:** 2026-08-11'de Goat'ta PA, BE için bir handoff hazırladı ve ekrana bastı (doğru
davranış). Clara onu okudu ama BE'ye taşımadı; yalnızca *"detay PA'nın handoff'unda,
oku"* dedi.

BE aradı ve bulamadı — çünkü **bulacağı bir dosya yoktu.** Sonra kendisi yazdı:
*"PA'nın handoff'unu dosyada ARADIM, BULAMADIM (handoff ekrana basılır dosyaya
yazılmaz — kanon böyle, doğru davranış). İçeriği bana ULAŞMADI."*

Bir tur kayboldu. Ve o turda BE *"ölçmeden yazarsam mevcut bir şeyi ikinci kez yazma
riski var"* diye durmuştu — yani doğru davranıyordu, eksik olan **merkezin işiydi.**

**How to apply:**

- Bir handoff geldiğinde **tam metnini** hedefe yaz. Özetleme.
- *"Şu dosyada / şu handoff'ta yazılı"* demek geçersiz — o dosya yok.
- Handoff isterken agent'a söyle: **ekrana bas AMA kanala da yaz.** Kanal kopyası olursa
  merkez özet değil tam metin taşır.

Ayıran soru: **hedefe gönderdiğim şey tek başına yeterli mi, yoksa başka bir yere
bakması gerekiyor mu?** İkincisiyse taşıma tamamlanmamıştır.

⚠️ Ve bu kuralın gerekçesi kanonda zaten var: *"rapor özetlenmez"* ve *"uzun içerik
kanala gömülmez — dosya yolu verilir."* İkisi çelişiyor gibi görünür ama ayrım şu:
**dosyası VARSA yol verilir, YOKSA metin taşınır.** Handoff'un dosyası yok.

Bkz. [[dogru-bilgi-yanlis-tasima]] — aynı ailenin özetleme tarafı.
Bkz. [[agent-sorusu-tasima]] — ham taşımanın ters yönü: soru anlatıya çevrilir.
