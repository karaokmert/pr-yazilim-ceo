---
name: acilis-soruyla-baslar
description: Açılışta ilk hareket kapanış okumak değil AskUserQuestion ile sormak — ARGE / Yeni iş / Eski işin devamı
metadata:
  type: feedback
---

Oturum açılışında ilk hareket **soru**: `AskUserQuestion` ile "bu oturumda ne
yapıyoruz?" — **ARGE / Yeni iş / Eski işin devamı**. Cevap gelmeden hiçbir kapanış
dosyası açılmaz.

**Why:** Mert'in cümlesi — *"Sürekli kalan işe devam etmek istemiyorum seninle."*
Kapanışı önce okursam oturumun gündemini dünkü oturum belirliyor; Mert masaya
oturduğunda önüne kendi seçmediği bir iş listesi geliyor. Okuduğum her satır kurduğum
çerçevenin parçası — çerçeveyi o kursun.

**How to apply:**
- ARGE seçilirse kapanış HİÇ okunmaz. Yalnız konunun geçmişi (`konular/{konu}/`).
  ARGE bir başlangıçtır; skill'e ya da role dönebilir.
- Yeni iş seçilirse dinlenir — bağlam Mert'ten gelir, dosyadan değil.
- Eski işin devamı seçilirse o zaman kapanış okunur.
- ARGE turu kapanış YAZAR ama kendiliğinden OKUNMAZ. İki kapıdan açılır, ikisini de
  Mert açar: *"eski işin devamı"* (yarım kalanlar arasında) ve *"şunu taramıştık"*
  (aranarak).
- Mert ilk mesajında ne yapacağını zaten söylediyse sorulmaz — cevap elde.
- Bir ARGE turu sürerken "bu arada şu iş bekliyordu" DENMEZ. Sorulunca söylenir.

Karar gerekçesi: `kararlar/2026-08-26-acilis-sirasi-soruyla-baslar.md`
Kanon: `clara-main` (Oturum açılışı + Oturum kapanışı)

İlgili: [[cevap-uzunlugu]] · [[bulgu-yukari-tasima-olcutu]]
