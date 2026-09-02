# Keba ERP — durum

**ClickUp:** folder `901516509839` (TPWS ile AYNI folder) · Task List `901524074948` · Bugfix `901524074949` · Planning `901524534409`
**Prefix:** KebaAI / KebaERP / KebaAP
**Ne:** Netsis entegrasyonlu ERP. Şirket, cari, banka, stok/ürün, kredi modülleri.
**Kim:** Mert

⚠️ **Bu folder'da iki ayrı ürün yaşıyor.** Öteki: TPWS (Truck Parts e-ticaret
sitesi, Didem'de) — ayrı klasörde: `projeler/tpws/`. Bu ayrım görülmeden Keba
listesi anlamsız.

⚠️ Ölçüm 2026-09-02, ClickUp taraması.

---

## Ne bitti

**PRY-17801 — KebaERP Netsis Gerçek Entegrasyon (mock'tan canlıya).** Bu projenin
kilometre taşı: entegrasyon artık gerçek Netsis'e bağlı.
**PRY-16782 — Keba Entegrasyon İşlemleri.**
**PRY-18055 — KebaAP Şirket Oluşturma İşlemleri** (completed).
**PRY-18026 — KebaAI Cari Yönetimi** (completed).
**PRY-18034 — KebaAI Krediler** (Netsis araştırması + entegrasyon, completed).

---

## Şu an açık

**Şirket ve kurulum:** PRY-17987 (Netsis Şirket Yönetimi, lıve-dev) · PRY-16181
(Proje Kurulumu) · PRY-16182 (Logo Entegrasyon) · PRY-17737 (Entegrasyon,
atanmamış) · PRY-18033 (Yönetim Paneli Temizliği / ERP kopyaları, atanmamış)

**Cari:** PRY-18044 (**bloke**) · PRY-18045 (Cari IBAN + Hesap Hareketi
Eşleştirme, Open)

**Banka:** PRY-18027 (Banka Hesap Hareketleri / Netsis Canlı, lıve-dev) ·
PRY-18042 (**bloke**)

**Stok / ürün:** PRY-18028 (Ürün Stok Yönetimi / Netsis Canlı, lıve-dev) ·
PRY-18043 (**bloke**)

---

## Bloke — ÜÇÜ DE ATANMAMIŞ, ÜÇÜ DE AYNI GÜN (2026-08-30)

- **PRY-18042** — Banka Ekranı Portal Kaydına Bağlanması
- **PRY-18043** — Ürün Detayları Tam Eşleme (çift yönlü)
- **PRY-18044** — Cari Tam Eşleme + Borç/Alacak Görünümü

**Örüntü:** ERP'nin üç ana modülünün de temel entegrasyonu çalışıyor (lıve-dev)
ama **Netsis ile birebir eşleştirme adımı** üçünde birden tıkanmış. Aynı gün
üçünün birden bloke işaretlenmesi tek bir ortak sebebi işaret ediyor —
⚠️ bu bir çıkarım, ölçülmedi.

---

## Sprint 7'de yapılacaklarla eşleşme (Mert — 4 iş)

- **Stok ve Ürün İşlemleri** → VAR. PRY-18028 (lıve-dev) + PRY-18043 (**bloke**).
  Haftanın işi büyük ihtimalle 18043'ün blokesini açmak.
- **Banka Hareketleri Entegrasyonu** → VAR. PRY-18027 (lıve-dev) + PRY-18042
  (**bloke**) + PRY-18045 (Open).
- **Teklif İşlemleri** → **YOK.** Keba folder'ında teklif/sipariş/fiyat teklifi
  geçen tek bir kayıt yok.
- **Plugin İşlemleri** → **YOK.** Plugin geçen hiçbir Keba kaydı yok.

⚠️ Çalışılacak iki başlığın ana engelleri "blockıng" statüsünde ve **kimseye
atanmamış** duruyor.

---

## Planning (durgun)

PRY-17351 (TPWS - Tasarımın Tamamlanması) · PRY-17352 (TPDP - Reklam Planlaması) ·
PRY-17353 (TPWS - Clarity Raporu) — üçü de TPWS tarafına ait, hepsi "team",
hepsi atanmamış.
