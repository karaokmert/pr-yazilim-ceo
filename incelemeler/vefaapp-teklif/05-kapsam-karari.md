# Mezarlık Bakım Projesi — kapsam kararı (Mert ile netleşti, 2026-08-25)

⚠️ **Teklifte referans sistemin adı GEÇMEYECEK.** İş kendi dilimizle tarif
edilir; VefaApp yalnız iç ölçüm kaynağıdır.

---

## Karar edilen kapsam

### Arayüzler — dört

1. **Web sitesi + müşteri üye alanı** (kamuya açık + giriş sonrası)
2. **Müşteri mobil uygulaması** — iOS + Android
3. **Saha personeli mobil uygulaması** — iOS + Android
4. **Yönetici paneli** (web)

⚠️ **Esnaf/tedarikçi paneli YOK.** Saha personeli kurum çalışanı; hakediş,
komisyon, cüzdan, IBAN, esnaf sözleşmesi, bölge talebi **kapsam dışı.**

### Ürün hatları — iki

**A · Bakım hizmeti**
- Paket seçimi (kademeli paketler, ziyaret sıklığı ve rapor tipi farklı)
- **Hem abonelik hem tek seferlik** — iç içe çalışır, ayrı veri hatları
- Abonelik: otomatik tekrarlayan tahsilat · otomatik yenileme aç/kapa ·
  başarısız tahsilat yönetimi · iptal · sonraki ziyaret takibi ·
  aylık/yıllık seçenek (yıllık indirimli)
- Görsel konfigüratör ile peyzaj ekleme → tutar pakete eklenir

**B · Mezar taşı yapımı**
- Galeriden iş seçimi (referans galerisi, personel etiketli, fiyatlı)
- **Tıkla → sipariş → online ödeme** (tek seferlik, yüksek tutar)
- Üretim ve kurulum aşamaları takibi
- Tamamlanma fotoğraf raporu

### İş akışı — tek yönlü

Müşteri sipariş verir → **admin saha personeline atar** → personel mezarlığa
gider, öncesi fotoğrafını çeker, işi yapar, sonrası fotoğrafını çeker, kapatır
→ rapor üretilir → müşteri panelinde/uygulamasında görür.

⚠️ Referansta iki yollu dağıtım var (iş havuzu + gönüllü üstlenme). **Bizde
yalnız manuel atama** — sadeleşme.

### Fotoğraf kanıt zinciri

- Öncesi fotoğrafı yüklenmeden iş **kapatılamaz** (kodda zorlanan kural)
- Sonrası fotoğrafı + (pakete göre) video
- Otomatik **PDF rapor** üretimi
- Müşteriye bildirim (push + mail/SMS)
- ⚠️ **AÇIK KARAR:** admin rapor onay kapısı olacak mı? Referansta var
  ("Fotoğrafları Reddet" → personel yeniden çeker, müşteri sonra görür).
  Mert'e sorulacak.

### Yönetici paneli — modüller

- **Sipariş masası** — tüm siparişler, atama, iptal, durum takibi, bekleyen kuyruklar
- **Abonelik yönetimi** — aktif abonelikler, tahsilat durumu, yenileme, iptal
- **Saha personeli yönetimi** — personel oluşturma, yetki, aktif/pasif
- **Galeri yönetimi** — iş ekle, fotoğraf yükle, personel etiketle, fiyat, yayınla
- **Saha haritası** — işlerin harita üzerinde konumsal görünümü
- **Bölge yönetimi** — il / ilçe / mezarlık hiyerarşisi ve kayıtları
- **Fiyat ve katalog yönetimi** ⭐ — paket fiyatları, bitki/hizmet kataloğu,
  mermer/ek hizmet farkları, aylık-yıllık oran. **Referansta YOK** (kodda sabit)
- **İndirim kodu yönetimi**
- **Finansal raporlama** — ciro, tahsilat, Excel dışa aktarım
- **Değerlendirme/yorum yönetimi** — müşteri puanı ve yorumları

### Teknik gereksinimler

- Tekrarlayan ödeme (sanal POS abonelik) + 3D Secure + taksit
- SMS OTP telefon doğrulama
- Çok sayıda fotoğraf/video yükleme ve arşiv
- Otomatik PDF rapor üretimi (kuyruk üzerinden)
- Push bildirim (iki mobil uygulama) + mail + SMS
- İnteraktif harita + il/ilçe/mezarlık hiyerarşisi + konum
- Görsel konfigüratör (2D katmanlı, canlı fiyat)
- Rol/yetki yönetimi
- KVKK: aydınlatma, hesap silme akışı, veri saklama
- ⚠️ **AÇIK KARAR:** saha uygulaması çevrimdışı çalışacak mı? Mezarlıklar
  şehir dışında, bağlantı zayıf. Teknik olarak pahalı ama atlanırsa saha
  kullanamaz.

---

## PR Yazılım yığını ile karşılığı

- Backend: C# / .NET Core
- Web: Next.js (SSR → referansın yapamadığı SEO burada kazanılır)
- Mobil: React Native / Expo (iki uygulama)
- Veritabanı: MSSQL
- Cache: Redis
- Kuyruk: RabbitMQ (PDF rapor, toplu bildirim, abonelik döngüsü)
- Dosya: Azure Blob
- Ödeme: yerel sağlayıcı (tekrarlayan ödeme destekli)
- Bildirim: Expo push + NetGSM + mail

---

## Fiyat gerçeği — kayda geçiyor

**Mert'in fiyatı: 300.000 ₺ + KDV.**

Karşılaştırma (kendi teklif formatımız, VisViva Medu):
**24.500 € ≈ 1.150.000 ₺** · 6 ay · 4 panel · **mobil uygulama YOK** ·
**tekrarlayan ödeme YOK** · **saha operasyonu YOK**

Bu kapsam VisViva'dan ağır: iki mobil uygulama, iki ürün hattı, tekrarlayan
ödeme, saha kanıt zinciri, görsel konfigüratör var.

**Mert'e sunulan üç yol (karar bekliyor):**
1. Kapsamı böyle yaz, fiyatı 300.000 bırak (stratejik/referans projesi)
2. V1/V2 diye kes — 300.000'e sığan bir ilk faz tanımla
3. Fiyatı yeniden değerlendir
