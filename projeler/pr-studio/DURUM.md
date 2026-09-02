# PR Studio — durum

**ClickUp:** folder `901516926211` · PR Studio Task List `901524614099` · KaraokYMM Task List `901525363563` · Efranca Task List `901525395193` · Bugfix `901524614101` · Planning `901524614095`

⚠️ **Bu folder'da ÜÇ ayrı müşteri yaşıyor:** Tedrik · KaraokYMM · Efranca.

⚠️ Ölçüm 2026-09-02, ClickUp taraması.

---

## TEDRİK (prefix: TE / TEWS)

**Ne:** Sipariş ve tedarik akışı, mağaza (tenant) yönetimi, Trendyol entegrasyonu.

**En ileri statü:** PRY-16058 (TE - Sipariş + Tedarik Akışı) — **productıons**

**Açık (lıve-dev):** PRY-16109 (Yönetim Paneli / web-admin) · PRY-16056 (Mağaza
Tenant Yönetimi) · PRY-16055 (Admin Kullanıcı İşlemleri) · PRY-16054 (Trendyol
Sipariş Entegrasyonu)

**Kurumsal kimlik (Buse):** PRY-17740 (Kurumsal Kimlik UI) — **PAUSE**'da. Alt
işleri completed: renk, logo+favicon, liste yüzeyi, görsel ince ayar, tablo
erişilebilirliği, ürün adı.

**Teknik borç (Open):** PRY-17768 (iç paket adları temizliği) · PRY-17769
(paylaşılan paket denetimi zorlanmıyor) · PRY-17770 (tedarik durumu değerleri
standart dışı) · PRY-17771 (tedarikçi PDF marka işareti)

**Web sitesi:** PRY-17591 (TEWS Web Sitesi Hazırlanması, ui) · PRY-17590 (Domain
Alımı, Umutcan)

⚠️ **PRY-16057 / 17932 / 17999 — "TE - Ürün Varlığı (Tablo)" üç kopya**, üçü farklı
listelerde, üçü aynı anda kapanmış.

---

## KARAOK YMM (prefix: yok, KaraokYMM Task List'te)

**Ne:** Mali müşavirlik denetim paneli. Mükellefler, tanımlamalar, sözleşmeler,
evrak yönetimi.

**Bitmiş:** tasarım taşıması (PRY-17942) · kullanıcı yönetimi CRUD (PRY-17961) ·
sidebar→header dropdown (PRY-17962) · sözleşmeler modülü (PRY-17975) · mükellef
bilgi revizesi (PRY-17985) · tanımlamalar revizeleri (PRY-17986)

**Açık (lıve-dev):** PRY-17940 (iskelet) · PRY-17967 (mükellefler modülü CRUD) ·
PRY-17966 (tanımlamalar taşıma + CRUD) · PRY-17965 (telefon kanonu) · PRY-17964
(gerçek kimlik doğrulama, FAZ 2) · PRY-17968 (modallar referans uyumu)

**Yeni açılmış evrak yönetimi talepleri (10 kalem, Open):** PRY-17950 (evrak dosya
incele) · PRY-17951 (firma detayda gelen/giden evrak) · PRY-17952 · PRY-17953 ·
PRY-17954 (cevap bekliyor gün hesabı) · PRY-17955 · PRY-17956 · PRY-17957 (evrak
numarası tarihten) · PRY-17958 (gelen/giden farklı seriler) · PRY-17959

**Ayrıca:** PRY-17948 (sözleşme eklenirken Oda + GİB bildirimi) · PRY-17943
(Toplantı Notları)

⚠️ **Canlı bir revize döngüsü var** — küçük müşteri talepleri aynı gün açılıp
kapanıyor (28 Ağustos'ta dört tane arka arkaya).

---

## EFRANCA (prefix: Efranca)

**Ne:** E-ticaret kurulumu. Marka, website, yetki, kategori, ürün, stok, vitrin,
ödeme, sepet, kasa modülleri.

**Kim:** Mert

**Bitmiş:** PRY-18012 (User Sistemi, 2026-08-29 — en son kapanan) · PRY-18032
(Kurulum Kapanış Doğrulaması §6, completed)

**Açık (lıve-dev, Mert):** PRY-18013 (Repo Üretimi) · PRY-18022 (Proje Hazırlama)
· PRY-18024 (User Sistemi)

⚠️ **PRY-18023 (Efranca - Mock Turu) — "pending approval", MERT'İN ONAYINDA
BEKLİYOR.**

**Modül bloğu (lıve-dev, atanmamış):** PRY-18029 (Marka ve Kurumsal Kimlik §3) ·
PRY-18030 (Website Hazırlığı §4) · PRY-18031 (Yetki ve Menü Düzeni §5) · PRY-18035
(Kategori) · PRY-18036 (Ürün) · PRY-18037 (Stok) · PRY-18038 (Vitrin) · PRY-18039
(Ödeme Yöntemleri) · PRY-18040 (Sepet ve Sipariş) · PRY-18041 (Kasa ve Gider)

---

## Sprint 7'de yapılacaklarla eşleşme

**"Efranca - Revizeler"** (Mert, Çar) → **VAR.** PRY-18046 ("Revizeler", Efranca
Task List, Open, atanmamış). Adı tam eşleşmiyor ama liste Efranca listesi ve bu
hafta açılmış.

Yanında dört somut revize kalemi duruyor — muhtemelen işin içeriği:
- PRY-18047 — Tahsilatta Yuvarlama
- PRY-18048 — Kasa Raporları Gün Gün Ayırma
- PRY-18049 — Sepet temizle ve Boşalt Çalışmıyor
- PRY-18050 — Sepet İçin Yuvarlama işlemi

⚠️ **Mock Turu onayın bekliyor** (PRY-18023) — revizelerle ilişkisi kontrol edilmedi.

---

## Bloke

PR Studio folder'ının tamamında bloke yok. Pause: Tedrik Kurumsal Kimlik UI.
