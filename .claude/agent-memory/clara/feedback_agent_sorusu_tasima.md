---
name: agent-sorusu-tasima
description: Agent'tan gelen soru/brief/çıktı Mert'e ham veya adres olarak taşınmaz — içeriği Clara getirir, anlaşılır anlatıya çevirir, eksikse agent'la netleştirir
metadata:
  type: feedback
---

**GENEL KURAL — ADRES DEĞİL İÇERİK TAŞINIR.** Mert agent'ların ekranını
görmüyor; merkez olmanın anlamı trafiğin Clara'dan geçmesi DEĞİL, Clara'nın
geçerken **içeriği taşıması.** *"PA sana sundu"*, *"terminal çıktısında var"*,
*"yukarıda duruyor"* — üçü de aynı hata: içerik yerine adres verilmiş.

Ayıran soru: **bu ekranı hiç görmemiş biri, benim mesajımdan karar verebilir
mi?** Veremiyorsa taşınan şey içerik değil işarettir.

Elde içerik yoksa uydurulmaz — **agent'tan tam metin istenir** (kanala
gönder, özetleme, kısaltma), sonra Mert'in formatına çevrilir.

**Bir agent'ın sorusu Mert'e taşınmadan önce iki kapıdan geçer:**

1. **Anlatı kapısı** — soru Mert'in ekranında KENDİ BAŞINA anlaşılır olmalı:
   hangi proje, hangi task, ne olmuş, agent neden soruyor, kararın sonucu ne.
   Terminal çıktısına / "yukarıda duruyor"ya atıf YETMEZ — Mert o ekranı
   görmüyor, AskUserQuestion ekranı tek başına yeterli olmalı.
2. **Netlik kapısı** — soru Clara'ya bile tam anlaşılır değilse Mert'e
   gitmeden ÖNCE agent'la netleştirilir. Yarım soruyu taşımak yükü Mert'e
   atmaktır.

**Why:** 2026-08-09 Goat saha testi: PA'nın ilk sorusu (bonus 0/null,
PRY-17455) read.py çıktısında bırakılıp bağlamsız a/b olarak soruldu. Mert:
"Soru bana böyle getirilmez ki. Bağlamı ne? Nereden geldi? O ekranı ben
görmüyorum. Yeterince açık değilse senin PA ile açık hale getirmen
gerekirdi." Bu proje-yonetimi'nin "rapor değil karar getir" kuralının öbür
yüzü: karar getirmek yetmez, karar VERİLEBİLİR hâlde getirmek gerekir.

**How to apply:** Kanaldan QUESTION geldiğinde: (1) mesajı oku, (2) kendime
sor — "bu anlatıyı hiç bilmeyen biri bu ekrandan karar verebilir mi?",
(3) hayırsa önce anlatıyı kur ya da agent'a netleştirme yaz, (4) soruyu
ancak ondan sonra, bağlam özeti SORUNUN İÇİNDE olacak şekilde sor.

**Aynı kuralın kendi soruma uygulanması (2026-08-09, ikinci vaka):** Onay
istenecek İÇERİK de sorunun içinde taşınır. Hook çıktısı örneğini mesaja
bastım, AskUserQuestion kutusu mesajı ezdi — Mert iki kez "görmedim" dedi.
Çözüm: AskUserQuestion'ın **preview alanı** — onaylanacak metin/mockup
seçeneğin preview'ına konur, kutuda görünür. Mesaja basıp "yukarıda" demek
agent sorusundaki "terminal çıktısında duruyor"un birebir Clara hâli.

**Üçüncü vaka — brief devri (2026-08-09, aynı gün).** PA task brief'ini
kendi ekranına bastı ve kanala haber vermedi; Clara bunu öğrenince Mert'e
*"PA sana sundu, onaylıyor musun"* dedi — yani onay istenen içeriği
taşımadan onay istedi. Mert kesti: **"Briefi senin bana iletmen gerekmiyor
mu? Benim istediğim format ve yapıda."**

Buradaki ek ders: **agent'ın kendi ekranına basması taşıma sayılmaz.** Bir
çıktı ekranda üretildiyse Clara'nın elinde YOKTUR — özetiyle brief kurulamaz,
tam metin istenir. Ve agent'a şu hatırlatılır: ekrana basmak yetmez, kanala
da bildirilir.

**Üç vakanın ortak mekaniği:** üçünde de içerik bir ekranda kaldı, Mert'e
onun adresi gitti. Sırasıyla — agent sorusu (a/b), onaylanacak örnek çıktı,
task brief'i. Aynı hata üç farklı kılıkta; ortak refleks yukarıdaki genel
kural.
