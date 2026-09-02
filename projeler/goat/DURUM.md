# Goat — durum

**ClickUp:** folder `90154701631` · Task List `901507627697` · Bugfix `901507627696` · Planning `901524538892`
**Prefix:** GOAT / GAP (admin panel) / GWS (web sitesi) / GSP (sponsor panel) / GYP (yayıncı panel)
**Ne:** Sponsor–yayıncı–üye ekosistemi. Promosyon, boost/ek hizmet, affiliate komisyon, çark/turnuva etkinlikleri, canlı yayın.
**Kim:** Mert · Buse (UI) · Umutcan (test/video) · Burcu

⚠️ Ölçüm 2026-09-02, ClickUp taraması. Space'in **en ağır açık iş yükü** burada.

---

## Ne bitti

**Yayıncı paneli (GYP) uçtan uca kapanmış:** login/logout/profil (PRY-15785),
proje işlemleri (PRY-15784), CRUD (PRY-15783), yayın planı (PRY-15786), yayın
işlemleri (PRY-15788), GWS yeni yayın & yayıncı (PRY-15817). Üstüne replay &
yayıncı detay fix paketi (PRY-15851) ve video işleme (PRY-15853).

Bir önceki dalga: Oran Etkinliği (PRY-15733), Yayıncı Panel (PRY-15597), Turnuva
Etkinliği (PRY-15580) ve altı fix paketi.

**Örüntü:** Yayıncı modülü bitmiş, **ekip sponsor ekonomisine geçmiş.** Bugün açık
olan yükün tamamı başka yerde: sponsor/affiliate, promosyon, boost, güvenlik.

---

## Şu an açık — konu damarları

**Affiliate (sponsor komisyon zinciri):** PRY-17527 (Affiliate Panel, full stack,
Mert) · PRY-17530 (Affiliate Panel UI, Buse) · PRY-15932 (oran alanı / sponsor
komisyon %) · PRY-15943 (sponsor kayıtta oran + periyod) · PRY-15947 (sponsor
panel erişim bilgisi)

**Güvenlik ve veri kaybı — en riskli grup:**
- **PRY-17542** — Anasayfa bölüm kaydetme çözülemeyen içerikleri **KALICI SİLİYOR**
  **(urgent, ATANMAMIŞ)**
- PRY-17373 — XSS: dangerouslySetInnerHTML sanitize eksikliği, 4 panel (urgent, Mert)
- PRY-17505 — Phone Number input hatası (urgent, Mert)
- PRY-15998 — SMS OTP "999999" hardcoded kaldır (ACİL, Mert)
- PRY-15999 — Self-referral saldırısı, invite-friend (Mert)
- PRY-17374 — CronJob concurrencyPolicy eksik, 3/4 job, çift çalışma riski (high, Mert)

**Anasayfa / içerik listeleri:** PRY-17535 · PRY-17543 (Redis cache boşken tüm
bölümler boş) · PRY-17483 (pasif sponsorlar görünüyor + sayım tutarsızlığı) ·
PRY-17684 · PRY-17716 · PRY-17666 · PRY-17685 · PRY-17694

**Promosyon:** PRY-17683 (detay çalışmıyor) · PRY-17691/17692 (BE+FE detay
kopukluğu, 5 alan) · PRY-17455/17454 (yeni alanlar) · PRY-15941 · PRY-15952 ·
PRY-15956 · PRY-15957 · PRY-15317 · PRY-15318

**Boost / ek hizmet:** PRY-15343 · PRY-17471 · **PRY-17478** (boş listede Index out
of range, ilk boost başlatma patlıyor — **high, ATANMAMIŞ**) · PRY-17477 · PRY-17479
· PRY-17480 · PRY-17481 · PRY-17472 (sponsor tıklama istatistiği veri kaynağı yok —
kritik) · PRY-17473 · PRY-17474 · PRY-17475 · PRY-17578

**Görsel oran / kırpma arızaları (bir bütün):** PRY-17671 (sağlayıcı logoları
kesiliyor) · PRY-17672 · PRY-17673 · PRY-17674 · PRY-17676 (banner) · PRY-17677 ·
PRY-17679 (high, Mert) · PRY-17678 · PRY-17712

**Arama / indeks:** PRY-17838 (arama katmanı hataları sessizce yutuyor, 37 nokta) ·
PRY-17839 · PRY-17726 · PRY-15939 · PRY-15995

**Tarih / UTC:** PRY-17714 (UTC ortaklaştırma) · PRY-17718 (tarih kayması envanteri)
· PRY-17713 (3 saat kayma)

**Cache / orphan bütünlüğü:** PRY-15993 · PRY-15994 (sonsuz TTL) · PRY-15996 ·
PRY-15989 · PRY-15990 · PRY-15991 · PRY-15992 (LIVE sonsuz broadcast)

**Super admin / hesap:** PRY-17719 · PRY-17446 · PRY-17686 · PRY-17448

**UI / teknik borç:** PRY-18080 (Tasarım UI Düzenlemeleri, atanmamış) ·
**PRY-18082 (GWS - UI Düzenlemeleri, Buse)** ← Sprint 7 işi · PRY-17690 · PRY-17467
· PRY-17563 · PRY-17468

**Diğer dikkat çekenler:** PRY-17560 (yayın detayında **sahte/hardcoded veri
gösteriliyor, yayında** — high, ATANMAMIŞ) · PRY-17722 (oyun giriş problemi, high,
Mert) · PRY-17728 (hakkımızda edit, high, Mert) · PRY-17835 (coin işlem hatası)

---

## Bloke

- **PRY-17668** — GAP dinamik listede 15 seçili ama listede 10 görünüyor, 2. sayfa
  yok (sıcak fırsatlar). Mert'te.

**Pause:** PRY-17837 (geçersiz adres 404 + ödeme listesi boş-veri koruması)

---

## Sahipsiz kritikler

- **PRY-17542** (urgent) — veri kaybı, anasayfa içerik siliyor
- **PRY-17560** (high) — yayında sahte veri gösteriliyor
- **PRY-17478** (high) — boost başlatma patlıyor

---

## Planning'de bekleyen

**Yapısal altyapı kuyruğu** (hepsi "team", hepsi atanmamış): PRY-16000 (yapısal
iyileştirmeler) · PRY-16001 (EF Fluent API + migration disiplini) · PRY-16002
(UnitOfWork / transaction wrapper) · PRY-16003 (merkezi logging + APM + DLQ) ·
PRY-16004 (distributed lock + cache invalidation + heartbeat) · PRY-16005 (DevOps)
· PRY-16006 (K8s cron concurrencyPolicy) · PRY-16009 (chat modülü) · PRY-17694

⚠️ PRY-16006 ile PRY-17374 **aynı iş, iki yerde, iki farklı statüde.**

**Müşteri talepleri** ("customer", atanmamış): PRY-17508 (chat istekleri) ·
PRY-17510 · PRY-17512 · PRY-17513 · PRY-17514 (hata mesajları Türkçe olsun)

---

## Sprint 7'de yapılacaklarla eşleşme (Mert + Umutcan — 4 iş)

- **Affilate** (Mert, Per) → VAR, güçlü. Beş kalem, ana ikisi atanmış.
- **Bugfix** (Mert, Cum) → VAR, çok geniş. Yukarıdaki damarların hepsi Bugfix
  listesinde.
- **Test İşlemleri** (Umutcan, Çar+Per) → **YOK.** Test/E2E/senaryo geçen açık
  Goat task'ı yok.
- **Video İşlemleri** (Umutcan, Cum) → **YOK.** Tek video kaydı PRY-15853 ve o
  kapanmış.

⚠️ **Umutcan'ın Goat'ta hiçbir açık task'ı yok.** Atanmış işler Mert, Buse ve
Burcu'da. Bu hafta ona verilecek iki başlık tam olarak karşılığı olmayan iki başlık.
