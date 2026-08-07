---
name: mert-karar-duzeni
description: Mert nasıl karar verir — sunulan seçenekleri reddedip sorunun kendisini yeniden kurar; "Mert olsa ne yapardı" sorusunun cevabı
metadata:
  type: user
---

Mert'in karar alma düzeni. Bu kayıt **"Mert olsa ne yapardı"** sorusuna cevap
vermek için tutuluyor — kontrolü zaman zaman Clara'ya bıraktığı için (kendi
ifadesi, 2026-08-07).

## Ana örüntü: sorulan soruyu reddeder, sorunun kendisini düzeltir

Üç karar, aynı gün, aynı şekil. Clara her seferinde **iki seçenek** sundu; Mert
üçünü de seçmedi ve **üçüncü bir yol** gösterdi. Ortak sebep: **sorulan sorunun
kendisi yanlış kurulmuştu.**

**Push kapısı.** Soru: *"push PAM'e mi geçsin, PQA'da mı kalsın?"*
Cevabı: ikisi de değil — **kuralı değiştirme, bir adım ekle.** PQA onaylar →
PAM'e bilgi → PAM dökümanını düzeltir → PQA son commit'i de denetler → push.
Yayın kapısı denetleyende kaldı, PAM dönüşü kazandı, PAM'in kendi commit'i de
denetimsiz geçmedi.

**Araç yasağı.** Soru: *"`Task` PAD'in tanımından tamamen silinsin mi?"*
Cevabı: ekseni değiştir — *"Araçları yasaklamıyoruz, `tools`'a araç eklemiyoruz
hiçbir araç için. Yasak **kime çağrı yapıldığında**."* Ekosistem agent'ı
çağrılamaz, ara araçlar serbest. Bir yan sorun (davranış testinin kapanması)
kendiliğinden çözüldü.

**Görev listesi kapsamı.** Soru: *"kural koşullu mu koşulsuz mu olsun?"*
Cevabı: seçeneği reddetti — *"Tek tasklık bir liste olmaz. İş tek kalem görünse
de içinde adımlar var."* Yani soru *"iş büyük mü küçük mü"* değil, **"bu işin
adımları neler."** Üretici tarafın *"formalite riski"* endişesi, o durumun **var
olmadığı** gösterilerek çözüldü.

## Türetilen refleks — Clara için

**Bir ikilem sunmadan önce sor: soru doğru kurulmuş mu?** İki seçenek arasında
sıkışmışsan, çoğu zaman ikisi de yanlış bir varsayımı paylaşıyordur. Mert o
varsayımı görüyor.

**Kural değiştirmek yerine adım eklemeyi tercih ediyor.** Mevcut kuralın gerekçesi
hâlâ geçerliyse kural durur; eksik olan şey araya giren bir adımdır. Bu, cascade
maliyetini de düşürüyor.

**Ekseni sorguluyor: yasak neyin üzerinde?** Araç mı, hedef mi? Boyut mu, yapı mı?
Yanlış eksende yazılan kural doğru davranışı da engelliyor.

**Var olmayan bir durumu çözmeye kalkışma.** *"Tek görevlik iş"* diye bir şey
yoktu ve o durum için tasarım yapmak boşunaydı. Aynı refleks yalın üretimde de
var ([[mert-yalin-uretim]]): olmayan probleme çözüm önerilmez.

## Ne zaman karar Mert'te kalır

Kendi cümlesi (2026-08-07): *"Bana sorman gereken kritik karar olursa not al."*
Ve: *"push onayını ben veririm."*

Ölçülmüş sınır: **kapı açan kararlar** onun — yayın onayı, bir kuralın
kaldırılması, kapsamın genişletilmesi. **Yöntem kararları** üretenin — katman
seçimi, terim ayrımı, cascade ekseni.

Ayıran soru: *bu karar bir şeyi geri alınamaz hâle getiriyor mu?*
