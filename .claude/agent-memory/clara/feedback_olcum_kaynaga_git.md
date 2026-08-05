---
name: olcum-kaynaga-git
description: Ölçüm yaparken erken bakma ve kullanıcının özetini kaynak sanma — iki kez düştüğüm tuzak
metadata:
  type: feedback
---

Bir ölçüm yaparken iki şey yasak: **işi biten sanmadan bakmak** ve **kullanıcının
özetini kaynak saymak.**

**Why:** 2026-08-04 kanal deneyinde ikisine de düştüm, ikisi de aynı turda.

*Birinci:* `web-ui-designer` kanalını kurduktan saniyeler sonra kayıt listesine
baktım, boş gördüm, Mert'e *"agent kaydını bırakmadı, sessiz başarısızlık"* dedim.
Agent hâlâ çalışıyordu — birkaç saniye sonra kaydı düştü. Sessiz başarısızlık olan
şey benim ölçümümdü.

*İkinci:* Mert *"UID'e de yolladım, o da kendine uyarladı"* dedi. Onaylayıp geçtim.
UID uyarlamamıştı — **reddetmişti**, üç gerekçeyle (kanal kuralı, kendi kanonu, ve
komutun teknik olarak zaten çözmeyeceği). Kanalı okuduğumda gördüm. Kullanıcının
özeti bir gözlem değil, bir izlenim olabilir.

**How to apply:** Bir agent'ın çıktısını ölçerken **tamamlanma bildirimini bekle** —
`task-notification` gelmeden dosyaya bakıp "eksik" demek yanlış ölçüm üretir. Ve
kullanıcı bir agent'ın ne yaptığını özetlediğinde, o özet üzerine bulgu kurmadan
önce **kanalı/dosyayı kendim aç.** İkisi de `CLA-LABEL-YOUR-EVIDENCE` ihlali:
tahmini ölçüm gibi sundum.

İlgili: [[kanal-testleri]], [[user-mert-profil]]
