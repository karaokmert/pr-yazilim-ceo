---
name: akisi-bloklamayin
description: Her görevi onaya bağlamak yasak — iş devam eder, yalnız geri dönülemez/tercihe bağlı olanda durulur (Mert, 2026-08-10)
metadata:
  type: feedback
---

Bir agent'a iş yürütürken **her adımı onaya bağlamak yasak.** Mert'in cümlesi,
2026-08-10: *"Her görevi bloklama, iş devam etsin."*

**Why:** Her bulguda durup onay istemek işi durduruyor ve bekleyen taraf Clara
oluyor — agent hazır, iş hazır, tek eksik bir "devam" cümlesi. Aynı oturumda beş
kez oldu: BE her ölçüm sonucunda `QUESTION` yazıp bekledi, cevapların hepsi
ölçümden çıkıyordu. Sonuç: gerçek karar (SQL şeması) ile rutin bulgu (discovery
sayımı eksik) aynı kapıya bindirildi ve kapı tıkandı.

**How to apply:** Agent'a iş verirken **iki listeyi açıkça yaz** — neyi sormadan
geçeceği, neyi sormak zorunda olduğu.

Sormadan devam + kararını yazar: sayım/kapsam eksiğini tamamlama · isimlendirme,
metot seçimi, yerleşim · emsal/desen seçimi · işi engellemeyen bulgu (not düşer,
devam eder).

Durur ve sorar: **geri dönülemez** iş (SQL/şema, veri silme, prod) · **kapsam
genişlemesi** (yeni alan/ekran/akış) · **yayındaki davranış değişimi** · iki yol
var ve seçim **maliyete/önceliğe** bağlı (ölçümle çözülmüyor).

Ayıran ölçüt kanondaki ile aynı: **ölçümle çözülen → agent çözer ve yazar;
tercihe bağlı → yukarı taşır.** Bkz. [[mert-etki-analizi-olcutu]] ve
[[secenek-sunma]].

**Kararını yazması zorunlu.** *"Devam ettim"* yetmez — NE karar verdi, NEDEN.
Görünmeyen karar verilmemiş karara benziyor, ve iki ay sonra kimse neden öyle
yapıldığını bilmiyor.

Clara için aynı kural: BE'nin *"(a) mı (b) mi"* sorusunu Mert'e taşımak yanlıştı
— cevap agent'ın kendi ölçümünden çıkıyordu ((b) ürünü bekletiyordu). O soru
Clara'nın cevaplayacağı sorudur.
