---
name: rapor-kime-gider
description: Bir raporu iletirken başlığa değil İÇERİĞE bak — içinde başkasının sorusuna cevap varsa ona da iletilir
metadata:
  type: feedback
---

Bir agent raporu iletirken bloğun başlığı **kime yazarsa yazsın**, içeriğinde başka
bir agent'ın sorusuna cevap varsa **ona da iletilir.**

**Why:** 2026-08-07'de PQA'nın denetim raporu *"PQA → PAM"* başlığıyla geldi ve
Clara yalnız PAM'e iletti. Oysa PAD son turda **üç soru sormuştu** ve üçünün de
cevabı o raporun içindeydi (bulgu 5'in ikinci cümlesi yerinde mi · altıncı izin
düzeltmesi doğru mu · sınır vakaları gerçekten sınır vakası mı).

PAD cevap almadan bekledi. Mert yakaladı: *"PAD deneyim bekliyorda kalmış, PQA
denetimi onayladığından haberi yok, bu iletişimi sağlaman lazımdı."*

Arıza **sessiz**: PAD beklediğini biliyordu ama cevabın gelmediğini bilmiyordu —
kanalda mesaj yoktu, yani "henüz yazılmadı" ile "yazıldı ama bana gelmedi" aynı
görünüyordu.

**How to apply:** Bir rapor geldiğinde iki soru sor: *"bu kime hitap ediyor"* ve
**"bunun içinde kimin sorusunun cevabı var?"** İkincisi çoğu zaman birden fazla
kişi. Devir bloğu bir hedefe gider (`ISD-ONE-TARGET`) ama **bilgi** birden fazla
tarafı ilgilendirebilir — o zaman ayrı bir `BİLGİ` mesajı yazılır.

Ayıran test: **biri bir soru sorduysa, cevabı gelene kadar hattı açık say.** Zincir
başka yöne dallanmış olsa bile o soru kapanmamıştır.
