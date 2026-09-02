---
name: feedback-ekran-tasarimi-once-sor
description: Mert bir UI/ekran taslağı istediğinde ekranların NEYE göre bölüneceği önce sorulur — Clara soru sormadan tasarladı ve kurgu tutmadı
metadata:
  type: feedback
---

Mert bir ekran taslağı ya da UI denemesi istediğinde, **ekranların neye göre
bölüneceğini önce sor.** Kendi çerçevenle bölme.

**Why:** 2026-09-02, proje ekonomisi aracı. Mert "demo ui taslak, bu projeyi yapsak
nasıl sayfaları olacak" dedi. Clara altı ekranı **sorulardan** kurdu (müsaitlik,
kârlılık, doluluk) — çünkü gereksinim konuşmasında sorular birikmişti. Mert
**varlıklardan** bekliyordu: Müşteriler · Projeler · Taskler · Plan · Maliyet.
Sonuç: *"Hayal ettiğimden farklı ve eksik olmuş."* Bir artifact boşa gitti.

Mert'in kurgusu doğruydu: bir yönetim programı varlık üzerinden gezilir, rapor
üzerinden değil. Clara'nın ekranları o varlıkların içindeki görünümlerdi — yanlış
değil, yanlış YERDE.

**How to apply:** Ekran/UI taslağı istendiğinde tasarıma geçmeden bir soru sor:
menüler neye göre bölünsün — varlıklar mı (müşteri, proje, task), akışlar mı
(planlama, yürütme), yoksa sorular mı (kim boş, kâr ne)? Bu tek soru bir artifact
turunu kurtarıyor.

⚠️ Aynı derse ilgili: Clara gereksinim konuşmasında da "maliyeti değil işi
planlasak" uyarısını aldı — çözüm sorusunu gereksinim sorusu sanma eğilimi var.
Bkz. [[feedback-gereksinim-once-cozum-sonra]]
