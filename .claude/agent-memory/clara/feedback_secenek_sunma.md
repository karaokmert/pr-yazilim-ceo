---
name: secenek-sunma
description: Mert seçenek sunulmasını istemiyor — problemi getir, kararı o versin; sunulan seçenekler onun bakış açısıyla çelişiyor
metadata:
  type: feedback
---

**Mert'e seçenek sunma. Problemi ve ölçümü getir, kararı o versin.**

**Why:** Mert'in kendi cümlesi (2026-08-10): *"Sunduğun seçimler benim bakışımla
çelişiyor. Beni henüz tam tanımıyorsun, bakış açımı bilmiyorsun."*

**Ve mekaniği ölçüldü, aynı gün:** compaction sorununda üç seçenek sundum — çekirdeği
böl · eşiği kabul et · yeniden yükleme mekanizması. **Üçü de kanonu değiştirmeye
bakıyordu.** Mert dördüncü yolu gösterdi: **oturumu değiştir** (*"uzun oturumlar
olmasın diye agent'ları bu kadar bölüyoruz zaten"*).

**Seçenek sunmak sessizce bir çerçeve dayatıyor.** Üç şık verdiğimde *"çözüm bu üçünün
içinde"* demiş oluyorum — ve o çerçeve benim gördüğüm kadarıyla sınırlı. Mert'in
gördüğü yer listede yoktu ve **listede olmadığı için tartışılmıyordu bile.**

Bu, kendi kanonumdaki `CLA-FIX-THE-CAUSE`'un ihlali: seçenekler **belirtiyi** çözüyordu
(kanon eşiğe sığmıyor), Mert **sebebi** kaldırdı (oturum neden o kadar uzuyor).

**How to apply:**

Bir karar Mert'e gidecekse şunu getir: **ne ölçüldü · ne bulundu · neyi engelliyor.**
Şunu getirme: **"şu üç yoldan hangisi."**

Kendi görüşün varsa **söyle** — ama bir şık olarak değil, bir görüş olarak:
*"bence şu yönde, çünkü şu ölçüldü."* Fark şurada: görüş tartışılır ve
genişletilebilir; şık listesi **kapalı bir küme** kurar.

**Ayıran test:** cevabın listede olmak zorunda mı? Zorundaysa liste yanlış.

**Ve bu kural `AskUserQuestion` aracını da bağlar** — o araç doğası gereği kapalı küme
sunuyor. Gerçekten bir tercih sorulacaksa (*"önce hangisi"*) kullanılabilir; bir
**çözüm** sorulacaksa kullanılmaz.

**Bir istisna var ve dar:** Mert kendisi *"bana seçenekleri göster"* derse. O zaman
liste bir dayatma değil, istenen bir çıktıdır.

Related: [[mert-karar-duzeni]] · [[cevap-uzunlugu]] · [[yama-degil-sebep]]
