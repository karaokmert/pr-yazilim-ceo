---
name: agent-sorusu-tasima
description: Agent'tan gelen soru Mert'e ham/bağlamsız taşınmaz — önce Clara anlaşılır anlatıya çevirir, eksikse agent'la netleştirir
metadata:
  type: feedback
---

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
