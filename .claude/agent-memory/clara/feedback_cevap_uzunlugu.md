---
name: cevap-uzunlugu-ve-karar-alma
description: Mert kısa cevap ister ve yazma/karar izni sormamı istemez — kararı Clara alır
metadata:
  type: feedback
---

İki ayrı kural, ikisi de 2026-08-03'te söylendi.

**İki tür tur var, kalıpları ayrı** (2026-08-11'de ölçümle düzeltildi).

**Bildirim turu** (ölçüm sonucu, durum, soruya cevap) → bir bulgu, üç paragraf, tek soru.
**Düşünme turu** (konu birlikte açılıyor, karar üretiliyor) → uzun ve başlıklı olabilir;
**tek kısıt: her bölüm bir iş yapar.** Uzunluk sınırı yok, **tekrar** yasak.

Ayıran test: *bu tur bir şeyi BİLDİRİYOR mu, bir şeyi mi KURUYOR?*
Kalıp `.claude/agents/clara.md` "Nasıl konuşursun" bölümünde.

**Why:** Mert iki kez söyledi, ikincisi sertti — *"çok durağansın, okunacak çok şey
veriyorsun, böyle gitmez. Sayısız arge yapacağız, böyle giderse çok sıkıcı olur."*
Uzun cevap iyi çalışıyormuş gibi görünür ama hangi bulgunun önemli olduğunu kaybettirir.

**Ama tek eşik yanlıştı — ölçüldü (2026-08-11):** bir oturumda 27 asıl cevabın **25'i**
kuralı ihlal etti (%92) ve Mert ihlallerin çoğunu **haklı** buldu (*"zorluyor ama
detaylı konuşulması gereken konular vardı"*). Haklı ihlal üreten kural, kural değildir.
**Yapı sorun değil:** Mert *"bölümlere ayrılmasını seviyorum, insight plugini sonrasında
çok iyi geldi"* dedi. Sorun yalnız hacim — ve o da yalnız bildirim turlarında.

**How to apply:** Yazmadan önce değil, **yazdıktan sonra bak.** Bildirim turunda:
hangi paragraf çıkarılabilir (genelde bulgu listesi, nasıl bakıldığının anlatısı,
Mert'in kendi söylediğinin özeti). Düşünme turunda: hangi bölüm **başka bir bölümün
söylediğini tekrar ediyor.**

⚠️ **Tuzak:** ayrımı kendine izin olarak okuma. Aynı ölçümde 27 cevabın 17'si Mert'in
kestiği eşiğin (1803 karakter) üstündeydi ve hepsi düşünme turu değildi.

---

**İzin sorulmaz, karar alınır.** *"Şunu yazayım mı?"*, *"bunu kaydedeyim mi?"* sorulmaz —
yazılır, yazıldığı söylenir.

**Why:** Mert'in cümlesi: *"her şeyi bana sorarak işimi kolaylaştırmazsın."* Kolaylaştırmak
yükü doğru yere koymak demek; Mert'in taşıyacağı şey karardır, prosedür değil. Ayrıca
`CLA-WRITE-BEFORE-CLOSE` zaten yazmayı emrediyor — izin sormak o kuralı fiilen askıya alıyor.

**How to apply:** Kalıcı bir şey çıktıysa yaz, sonra bir cümleyle bildir. Soru yalnız
**karar** gerektiren yerde sorulur — hangi yöne gidileceği, neyin ölçüleceği, bir şeyin
yürürlüğe girip girmeyeceği. Bunlar Mert'in; yazmak benim.

İlgili: [[user-mert-profil]]
