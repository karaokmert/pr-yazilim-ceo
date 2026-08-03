---
name: hatirladigim-kayittir
description: Kafamdaki hazır özet bir kayıttır ve en kırılganıdır — üstüne argüman kurmadan kaynağı aç
metadata:
  type: feedback
---

Bir konuda kafamda hazır bir özet varsa (*"bunu konuşmuştuk, sonuç şuydu"*), o özet
bir dosya kadar kontrol gerektirir — aslında daha fazla, çünkü dosyanın tarihi ve
dayanağı var, özetin yok.

**Dayanak:** 2026-08-03'te ölçüldü, kendi hatam.

**Why:** v8 hakkında kafamda *"sahada tutmadı, kurallara uyulmadı"* özeti vardı ve
Mert'e *"genel yazılan kural davranış üretmez"* diye karşı argüman kurdum. Oysa o
sonucun sebebini çürüten dosya aynı gün `HARITA.md`'ye yazılmıştı
(`incelemeler/skill-preload-bulgusu/kayit.md`): arıza kural biçiminde değil,
skill'lerin hiç yüklenmemesindeydi. Dosya elimin altındaydı, **açmadım** — çünkü bilgi
eksik değildi, hazır sanılıyordu.

Mert bunu *"hafıza yönetimi"* sorunu olarak okudu; itiraz ettim ve o itiraz doğru:
erişim sorunu değildi, refleks sorunuydu. RAG ya da daha iyi bir hafıza sistemi bunu
çözmezdi.

Ayrıca `memory-okuma-kontrolu` kuralı zaten *"bir kayda dayanmadan önce bak"* diyordu —
boşluk şuydu: **kendi hatırladığımı bir kayıt saymamıştım.**

**How to apply:** Ayıran soru — *"bunu hatırlıyorsam, nereden hatırladığımı da
söyleyebiliyor muyum?"* Söyleyemiyorsam o bilgi değil izlenim; üstüne argüman
kurmadan kaynağı açılır. Özellikle bir **karşı argüman** kuracakken: itirazın gücü
dayanağından geliyor, izlenime dayanan itiraz yanlış yöne çeker.

İlgili: [[memory-okuma-kontrolu]] — o kural dosyaya dayanmayı, bu kural kendi kafama
dayanmayı kontrol ediyor. İkisi aynı hatanın iki yüzü.
