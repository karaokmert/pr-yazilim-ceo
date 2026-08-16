---
name: dosya-degil-sorgu
description: Bir bilgi erişim problemi geldiğinde çözüm YENİ DOSYA değildir — var olanı okumaktır; Mert 485 dosyalık düzenden sıkıldığını söyledi
metadata:
  type: feedback
---

Bir "bilgi kayboluyor / haberim olmuyor / nerede yazmıştık" problemi geldiğinde
**yeni bir dosya, defter ya da kayıt düzeni önerme.** Çözüm var olanı okumaktır.

**Why:** 2026-08-16'da Mert *"birçok session açıyorum, bunların diğer sessionlarda
haberi olmuyor"* dedi. Clara canlı bir defter dosyası önerdi. Mert kesti:
*"Sürekli yazılan, okuması çok zahmetli olan dosyalama sisteminden çok sıkıldım."*

Ölçüldü: repoda **485 markdown dosyası** var (konular 155 · agent-memory 68 ·
günlük 62). Clara 486'ncısını öneriyordu.

Doğru teşhis: bu bir **dosyalama** problemi değil, **sorgu** problemi. Bilgi zaten
yazılıyor ve fazlasıyla yazılıyor; eksik olan onu Mert'in yerine okuyan şey.
Mert'in tarifi: *"ekip yöneten Clara'ların işlerini okuyabiliyor ve raporlayabiliyor
olman gerekiyor."*

**How to apply:** Bir erişim problemi geldiğinde önce sor — **bu bilgi zaten bir
yerde yazılı mı?** Yazılıysa çözüm okuma tarafında: hangi engel var, hangi kural
beni okumaktan alıkoyuyor, hangi araç yanlış çağrılıyor. Yeni dosya ancak bilgi
**hiç üretilmiyorsa** gündeme gelir.

Aynı gün ikinci kanıt: Obsidian araştırıldı ve kazancının agent tarafında değil
**Mert'in bakma penceresi** tarafında olduğu çıktı — yine okuma tarafı.

İlgili: [[grep-satir-goster]]
