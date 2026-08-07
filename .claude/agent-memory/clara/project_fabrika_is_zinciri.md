---
name: fabrika-is-zinciri
description: Fabrikada bir iş nasıl yürür — Clara'dan PAM'e, PAM'den PAD'e, PQA onayına ve Mert'in push onayına kadar zincirin sırası
metadata:
  type: project
---

Mert'in 2026-08-07'de tarif ettiği iş zinciri. Clara bu zincirin **taşıyıcısı ve
yöneticisi**; her adımda kendi kararını değil trafiği yönetir.

```
Clara → PAM (iş)
PAM ↔ Clara   PAM işi sorgular, soru sorar, belirsizlik danışır
              Clara cevaplayabiliyorsa cevaplar
              ONAY gerekiyorsa Mert'e sorar, döner
PAM → gereksinim → Clara
              Clara sapma/kararsızlık görmezse ONAYLAR
PAM → handoff → Clara → PAD
              araya PCA girecekse: PAM handoff yazar, Clara iletir
PQA onaylayana kadar sürer → commit → Clara'ya bilgi
Clara → Mert: brief (ne yapıldı · ne değişti · ne karar alındı)
Mert → PUSH ONAYI
```

**Why:** Mert'in cümlesi: *"ben senden brief alırım ne yapıldı neler değişti ne
kararlar alındı, push onayını ben veririm."* Zincirin görünürlüğü Clara'nın
taşımasıyla sağlanıyor — agent'lar birbirini çağırmıyor
([[task-kaldirildi-karari]]).

**How to apply:**

- **Üç iş varsa üçü de aynı şekilde yönetilir** ve push onayı **her iş için ayrı**
  alınır. Bir onay diğerine geçmez.
- **Clara kuralı dayatmaz.** Mert'in cümlesi: *"sen işi anlat, PAM yeterince
  iyiyse zaten işi senin istediğin gibi yapar. Beklediğin işi yapmaması PAM'in
  gelişmesi gerektiğini gösterir ve o gelişimi planlarız. Her işin kuralını
  dayatmasını sen yaparsan patron değil amele olursun."*
  Yani ölçüm verilir, madde eşlemesi yapılmaz — agent kendi bulur. Bulamazsa
  bu bir **gelişim bulgusu**dur, düzeltilecek bir hata değil.
- **Handoff yazarken kim kime yazıyor karıştırılmaz.** Clara PAM'e yazarken
  PAM'in PAD'e ne diyeceğini yazmaz; kararı bildirir ve handoff'unu ister.
