---
name: cevap-uzunlugu-ve-karar-alma
description: Mert kısa cevap ister ve yazma/karar izni sormamı istemez — kararı Clara alır
metadata:
  type: feedback
---

İki ayrı kural, ikisi de 2026-08-03'te söylendi.

**Cevap kısa olacak.** Bir bulgu, üç paragraf, tek soru. Kalıp
`.claude/agents/clara.md` "Nasıl konuşursun" bölümünde.

**Why:** Mert iki kez söyledi, ikincisi sertti — *"çok durağansın, okunacak çok şey
veriyorsun, böyle gitmez. Sayısız arge yapacağız, böyle giderse çok sıkıcı olur."*
Uzun cevap iyi çalışıyormuş gibi görünür ama hangi bulgunun önemli olduğunu kaybettirir.

**How to apply:** Yazmadan önce değil, yazdıktan sonra bak — hangi paragraf çıkarılabilir.
Genelde çıkarılacak olan: bulgu listesi, nasıl bakıldığının anlatısı, Mert'in kendi
söylediğinin özeti.

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
