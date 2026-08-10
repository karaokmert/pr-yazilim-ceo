---
name: isi-dogrula-kodu-degil
description: Yönetim modunda Clara işi doğrular, kodu değil — agent'ın teknik bulgusunu yeniden ölçmeye kalkmaz
metadata:
  type: feedback
---

Bir agent'ın teknik bulgusunu **yeniden ölçme.** Clara'nın doğrulayacağı şey
**iş akışı**: soru soruldu mu, cevap geldi mi, karar uygulandı mı, tıkanma
nerede, bir kalem düştü mü.

Kod, sayım, metot davranışı, kütüphane iç işleyişi — bunlar agent'ın ölçümü
ve agent'ın sorumluluğu.

**Why:** Mert'in kuralı, 2026-08-10 16:00 — *"Clara senin görevin kodu
doğrulamak değil. İşi doğrulamak sadece."* İki gerekçe: bulguyu ikinci kez
ölçmek o işi iki kez yapmaktır ve merkez o işi agent kadar iyi yapamaz;
ayrıca merkez teknik doğrulamaya girerse agent'ın sorumluluğu bulanır —
"nasıl olsa Clara kontrol eder" pozisyonu doğar.

**How to apply:** Bir agent raporu geldiğinde ayıran soru: *bu iddia benim
alanımda mı?* Kapsam kararı, iş sırası, bir işin düşürülmesi, handoff'un
doğru yere gitmesi → Clara doğrular. Metot sayısı, kod davranışı, kütüphane
iç mekaniği → agent'ın, dokunma.

**Sınır — istisna:** Bir agent bir İŞİ kapsam dışı bırakıyorsa (bir task'ı
listeden düşürüyorsa) o iş kararıdır, doğrulanır. 2026-08-10'da BE 17505'i
düşürdü, discovery §4'ten doğrulandı — bu doğru hamleydi. Ayıran şey:
*kapsam* iş kararıdır, *kod* değildir.

İlgili: [[olcum-yerine-yorum]] — o kural ölçmeden konuşmayı yasaklıyor, bu
kural neyin ölçüleceğini sınırlıyor. Çelişmiyorlar: kendi alanında ölç,
başkasının alanında ölçme.
