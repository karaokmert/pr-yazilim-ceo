---
name: katman-degeri-icerikten-olculur
description: Bir aracı katmanın (koordinatör, relay, monitör) değerini ölçerken trafik SAYISINA değil taşıdığı İÇERİĞE bak — sayı "gereksiz" der, içerik "işini yapmadı" diyebilir
metadata:
  type: feedback
---

Bir aracı katmanın işe yarayıp yaramadığı **taşıdığı içerikten** ölçülür, geçen
trafiğin sayısından değil.

**Why:** 2026-08-10, Goat'ta PA+Clara denemesi. Clara ilk ölçümde mesaj sayısına ve
süreye baktı (2s23dk, 1 tur kapandı) ve *"tek agent varken aracı katman israftır,
kaldır"* dedi. Mert düzeltti: katman gerekliydi — o **işini yapmadı**. İçerik
okununca görüldü: aracı Clara'nın 10 mesajındaki her teknik detay PA'nın raporundan
geri okunmuştu (kendi okumasından tek dosya adı yok), 4 sorusunun hepsi **süreç**
sorusuydu (*"mesajı aldın mı", "izleyicin çalışıyor mu"*), **içerik sorusu sıfır**,
ve PA'nın 6222 karakterlik brief'i Mert'e özetlenerek aktarıldı. Mert'in cümlesi:
*"bana haberci güvenlik görevlisi yaptı."*

İki teşhis **zıt sonuç üretiyor**: sayıya bakan katmanı kaldırır, içeriğe bakan
katmanı düzeltir. Yanlış olanı seçmek çalışan bir yapıyı sökmek demek.

**How to apply:** Bir katmanın (koordinatör, relay, monitör, aracı agent) değeri
sorgulandığında — önce şunu sor: **bu katman gelen bilgiye BİR ŞEY EKLİYOR mu?**
Eklemiyorsa iki ihtimal var ve karıştırılmaz:
- Çözmesi beklenen bir problem **YOK** → katman gereksiz, kaldır (yalın üretim)
- Problem **VAR** ama dolduramadı → katman gerekli, düzelt

Ayırt eden şey problemin varlığı, trafiğin miktarı değil.

**Ve aracı katman için hakimiyet ön şarttır:** işi bilmeyen bir katman gelen bilginin
yeterli olup olmadığını yargılayamaz, muğlak yeri görüp geri soramaz, karar için
brief üretemez. Üçü de hakimiyete bağlı — hakimiyet yoksa üçü de olmaz ve geriye
haberci kalır.

İlgili: [[feedback_olcum_yerine_yorum]] · [[feedback_kapsamini_yaz]] ·
[[user_mert_yalin_uretim]]
