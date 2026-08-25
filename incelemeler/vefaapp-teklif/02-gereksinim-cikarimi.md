# VefaApp benzeri sistem — gereksinim çıkarımı

**Müşteri talebi:** VefaApp'in benzerini sıfırdan istiyor.
**Kaynak:** vefaapp.com yedi sayfa + JS bundle + store sayfaları (2026-08-25).
**Ölçüm sınırı:** giriş gerektiren panel içleri GÖRÜLMEDİ — panel içeriği API
uçlarından ve ekran metinlerinden ÇIKARILDI, doğrudan ölçülmedi.

---

## İşin özü — bu ne tür bir sistem

Bu bir e-ticaret sitesi değil. **Saha operasyonu olan, çift taraflı bir hizmet
pazaryeri (marketplace).** Üç şeyi bir arada yapıyor:

1. **Abonelik satışı** — aylık tekrar eden bakım paketleri (tek seferlik de var)
2. **Saha iş emri yönetimi** — sipariş bölgedeki esnafa atanır, esnaf gider,
   öncesi/sonrası fotoğraf yükler, rapor üretilir
3. **Esnaf hakediş/komisyon yönetimi** — para havuzda tutulur, komisyon kesilir,
   esnafa IBAN'ına ödenir

Bu üçlü, projenin gerçek ağırlığı. Bakım paketi satmak kolay; **işin sahada
yapıldığını kanıtlamak ve parayı üç taraf arasında doğru bölmek** zor.

---

## Roller — dört ayrı arayüz

**1 · Müşteri (web + mobil)** — sipariş veren, uzakta yaşayan yakın
**2 · Esnaf / Zanaatkar** — sahada işi yapan usta (bakım ustası VE mezar taşı ustası
ayrı ağlar: `hizmetBolgeleriBakim` / `hizmetBolgeleriTas`)
**3 · Saha ekibi** — `/operasyon-haritasi`, harita üzerinden iş takibi
**4 · Yönetici (admin)** — onay, atama, finans, bölge yönetimi

⚠️ **Esnaf ile saha ekibi ayrı roller.** VefaApp'te footer'da iki ayrı giriş var
("Esnaf ve Zanaatkar Başvurusu" / "Saha Ekibi Girişi"). Esnaf dış tedarikçi,
saha ekibi kurum içi denetim/operasyon gibi görünüyor — teklifte bu ayrım
netleştirilmeli.

---

## Müşteri tarafı — ekran ve akış envanteri

### Kamuya açık (SEO kritik)

- **Ana sayfa** — paket vitrini, süreç anlatımı, mezarlık arama, tasarım atölyesi girişi
- **Hizmetler** — dört hizmet türü + paket karşılaştırma + SSS
- **Süreç** — iki ayrı süreç anlatımı: bakım süreci (4 adım) ve mezar taşı süreci (4 adım)
- **Kurumsal** — misyon/vizyon + rakamlar (81 il, 973+ ilçe, 45+ doğrulanmış esnaf, %99)
- **Mezar Taşı Vitrini** — usta portföyü: 29 kayıt, her biri {başlık, şehir(ler),
  usta adı, fiyat, görsel sayısı}. Fiyat aralığı **25.000 ₺ – 350.000 ₺**
- **Bakım Vitrini** — öncesi/sonrası iş portföyü: 13 kayıt, {başlık, görsel sayısı}.
  Fiyat/usta bilgisi YOK — bakım fiyatı pakete bağlı
- **Bölgelerimiz** — SVG Türkiye haritası (81 il tıklanabilir) + il arama + ilçe seçimi
- **Destek**, **Gizlilik**, **Hesap silme** (store zorunluluğu), **Ödeme sonucu**

⚠️ **VefaApp'te vitrin kartları `<button>`, ayrı URL'i yok** — yani her mezar taşı
modelinin ve her bakım işinin kendi sayfası yok, modal açılıyor. **Bu bir SEO
kaybı ve bizim için fırsat:** her vitrin kaydına kendi URL'i verilirse
("uşak beyazı mezar taşı konya") organik trafik gelir. Next.js + SSR bunu verir,
CRA vermiyor.

### Sipariş akışı — bakım

1. Mezarlık seçimi (il → ilçe → mezarlık) VEYA mezarlık adıyla arama
2. Paket seçimi (üç paket × tek seferlik/abonelik)
3. **Opsiyonel: tasarım atölyesi** — mermer rengi seç, şablon seç, toprağa bitki
   ekle; peyzaj bedeli canlı hesaplanır ve pakete eklenir
4. Merhum bilgileri (ad, doğum-vefat yılı), mezar yeri tarifi, özel anma günleri, not
5. Telefon doğrulama (SMS OTP)
6. Sözleşme onayı (mesafeli satış + KVKK)
7. Ödeme (3D Secure, taksit sorgulama, indirim kodu)

### Sipariş akışı — mezar taşı (ayrı akış)

1. Vitrinden iş + usta seçimi
2. Merhum ve mezarlık bilgileri
3. **Ustaya özel sabit fiyat** üzerinden 3D Secure ödeme
4. Usta üretir + mezarlıkta kurar
5. Fotoğraf raporu panele düşer

### Müşteri paneli (`/hesabim`)

Siparişlerim · abonelik durumu ve sonraki ziyaret tarihi · öncesi/sonrası
fotoğraf ve video arşivi · **PDF rapor indirme** · sipariş iptali · profil ve
telefon güncelleme · indirim/referans takibi · sözleşme arşivi

---

## Esnaf tarafı — ekran envanteri

**Başvuru ve onay:** `/esnaf-basvuru` → admin onayı → "doğrulanmış esnaf".
Dijital esnaf sözleşmesi onayı (`esnafSozlesmesi`).

**Bölge talebi:** esnaf hangi il/ilçelerde çalışacağını talep eder, admin
onaylar/reddeder (`bolge-talep-onayla` / `bolge-talep-reddet`).

**İş yönetimi:** atanan siparişler · sipariş durumu güncelleme
(`esnaf/siparis-durum`) · **öncesi fotoğraf yükleme (işe başlamadan)** ·
sonrası fotoğraf/video yükleme · rapor tamamlama

**Finans:** IBAN kaydı · **mevcut bakiye** · **net komisyon** · hakediş takibi

**Portföy:** vitrine iş ekleme (mezar taşı modeli + fiyat, bakım öncesi/sonrası)
→ admin onayından geçiyor (`tasarim-onayla` / `tasarim-reddet`)

---

## Saha ekibi tarafı

**Operasyon haritası** — Leaflet harita üzerinde aktif işler, konum bazlı takip.
Tarayıcı Geolocation API kullanılıyor (esnafın mezarlıkta olduğunun doğrulanması
için olabilir — ÖLÇÜLMEDİ, çıkarım).

---

## Yönetici paneli — ekran envanteri

**Sipariş yönetimi:** tüm siparişler · **esnafa atama** (`siparis-esnaf-ata`) ·
iptal · durum takibi · "Onay Bekleyenler" kuyruğu · "Rapor Bekleniyor" takibi

**Esnaf yönetimi:** esnaf ekle · durum değiştir (aktif/pasif) · rol atama ·
esnaf detay · bölge talebi onay/red · **gerekçeli red** ("Reddetme nedeni,
esnafa iletilecek")

**Portföy denetimi:** vitrine eklenen işlerin onay/reddi

**Finans:** **"Havuzdaki Toplam Para"** · **"Vefa Komisyon Geliri"** ·
"Toplam Aktif Esnaf" · esnaf hakedişleri ve ödeme raporları

**Bölge yönetimi:** iki ayrı bölge seti (bakım / mezar taşı) × il-ilçe-mezarlık
hiyerarşisi · mezarlık kayıt yönetimi (VefaApp'te 264 kayıt)

**İçerik:** paket tanımları ve fiyatları · bitki/şablon kataloğu ve peyzaj
fiyatları · indirim kodları · vitrin içeriği

---

## Teknik gereksinimler — çıkarılan

**Zorunlu:**
- Abonelik/tekrarlayan ödeme (aylık döngü, %16 indirim mantığı, yıllık plan)
- 3D Secure sanal POS + taksit sorgulama + indirim kodu doğrulama
- SMS OTP telefon doğrulama
- **Görsel/video yükleme ve arşiv** — her iş için öncesi/sonrası, çok sayıda
- **PDF rapor üretimi** (otomatik, işlem sonunda)
- Push bildirim (mobil) + e-posta + SMS bildirim
- **Harita:** il/ilçe/mezarlık hiyerarşisi + interaktif harita + konum
- **Tasarım atölyesi:** görsel konfigüratör (mermer rengi, şablon, bitki
  yerleştirme) + canlı fiyat hesaplama
- Rol ve yetki yönetimi (4 rol + admin alt rolleri)
- Komisyon/hakediş hesaplama ve havuz muhasebesi
- KVKK: aydınlatma, hesap silme akışı, veri saklama ("Yasal Nedenlerle Saklanan Veriler")
- Mobil uygulama (iOS + Android) — VefaApp'te var

**Bizim yığınımızla karşılığı (PR Yazılım kanonu):**
- Backend: C# / .NET Core
- Panel + web: Next.js (SSR → **VefaApp'in yapamadığı SEO burada kazanılır**)
- Mobil: React Native / Expo
- Veritabanı: MSSQL (VefaApp Firestore — finansal hesap için ilişkisel model üstün)
- Cache: Redis (mezarlık listesi, vitrin, paket — okuma ağırlıklı)
- Kuyruk: RabbitMQ (PDF rapor üretimi, toplu bildirim, abonelik döngüsü)
- Dosya: Azure Blob (VefaApp Cloudinary)
- Ödeme: yerel sağlayıcı (VefaApp Moka)
- Bildirim: Expo push + NetGSM SMS + mail

---

## Fiyat referansı — VefaApp'in kendi rakamları

**Bakım paketleri (aylık):** Vefa 2.950 ₺ · Huzur 4.400 ₺ · Hatıra 11.500 ₺
**Mezar taşı işleri:** 25.000 ₺ – 350.000 ₺ (usta belirliyor)
**Ek:** peyzaj bedeli (bitki bazlı, değişken)

Bu, müşterinin iş modelini anlamak için önemli: **hem düşük tutarlı tekrarlayan
gelir, hem yüksek tutarlı tek seferlik işlem** aynı sistemde. Ödeme, iade,
komisyon kuralları ikisi için farklı olmak zorunda.
