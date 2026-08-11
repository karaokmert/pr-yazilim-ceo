---
name: bulgu-yukari-tasima-olcutu
description: Bir bulgu ölçülüp kaydedildiğinde iş bitmiştir — yukarı taşımanın tek ölçütü "bu şu anki işi bloke ediyor mu?" (Mert, 2026-08-11)
metadata:
  type: feedback
---

Bir bulgu **ölçülüp kaydedildiğinde iş bitmiştir.** Onu Mert'e karar olarak taşımak
ancak şu sorunun cevabı **EVET** ise doğrudur:

> **Bu bulgu ŞU ANKİ işi bloke ediyor mu?**

Hayırsa: kayda geçer, akış **durmaz**, Mert'e getirilmez.

**Why:** 2026-08-11'de Mert kesti: *"Clara hızlanmamız lazım. Çok oyalanıyoruz.
Backend'i dev'e giden hiçbir işe başlamadık daha, neden oyalanıyorsun."*

Ölçüldü: o gün 20 commit gitti, **7'si doküman** (üçte bir). Ve Clara Mert'e **yedi yan
karar** getirmişti — `motion-dom` pin drift'i · 322 derleme uyarısı · `web_site` CI ·
dört sahipsiz task · ClickUp statüsü · doküman yeri · üç eşleme belirsizliği.

**Hiçbiri** o anki işi (backend'i dev'e götürmek) ilerletmiyordu. Üçü kapatıldı ve
günlüğe yazıldı; akış hemen hızlandı.

**How to apply — bir bulgu çıktığında sıra:**
1. **Ölç** (tahmin taşıma)
2. **Kaydet** (günlük / `HARITA.md` / ilgili belge)
3. **Sor:** bu şu anki işi bloke ediyor mu?
   - EVET → Mert'e getir, karar gerekiyor
   - HAYIR → **devam et**, bir daha getirme

⚠️ **Tuzak — "önemli" ile "bloke edici" aynı şey değil.** 322 güvenlik uyarısı önemli;
ama o gün hiçbir işi durdurmuyordu. Önemli olanı hemen getirmek, akışı önemsiz kadar
etkili durduruyor.

⚠️ **Ve tersi:** bir bulgu bloke ediyorsa **hemen** getirilir, biriktirilmez. O gün SQL
migration ve telepresence tam bu sınıftaydı — ikisi de tek cümlede iletildi ve iş aktı.

**Aynı ölçüt agent'lara da verildi:** *"Bir bulgu ölçülüp kaydedildiğinde iş bitmiştir.
Yukarı taşımanın ölçütü 'bu şu anki işi bloke ediyor mu'. Hayırsa akış durmaz."*

Bkz. [[akisi-bloklamayin]] — aynı ailenin onay tarafı.
Bkz. [[secenek-sunma]] — şık listesi de akışı durduran bir biçim.
Bkz. [[zemin-degisti-mi]] — cevabı elimde olan şey soru değil, bağlam.
