# VefaApp — teknik envanter (ölçüldü, 2026-08-25)

Kaynak: canlı site + JS bundle (`main.c8b20dfb.js`, 1.2 MB) + store sayfaları.
**Ölçüm yöntemi:** HTTP ile HTML/bundle çekildi, statik metin analizi yapıldı.
**Kapsam dışı (BAKILMADI):** giriş gerektiren ekranlar (müşteri/esnaf/admin panelleri
içi), mobil uygulama içi akışlar, backend API cevap gövdeleri.

## Şirket ve ürün

- **VEFAAPP BİLGİ TEKNOLOJİLERİ A.Ş.** (Maslak/İstanbul, 0850 305 97 48)
- Kendini "Türkiye'nin ilk dijital mezar bakım sistemi" olarak konumlandırıyor
- Web + iOS (`id6785254561`) + Android (`com.vefaapp.mobile`) — **mobil yayında**
- Analytics: Google Analytics (G-M8LM8MSQQT) + Microsoft Clarity

## Teknoloji yığını (mevcut sistem — BİZİM KANONUMUZUN DIŞINDA)

- **Frontend:** React (Create React App) — tek 1.2 MB bundle, `/static/js/`.
  Next.js DEĞİL → SSR yok, SEO zayıf. HTML gövdesi 2 KB boş `<div id="root">`.
- **Backend:** `vefa-backend-production.up.railway.app` (Railway PaaS)
- **Veritabanı:** Firebase / **Firestore** (NoSQL)
- **Auth:** Firebase Auth (Google girişi, telefon/SMS doğrulama, reCAPTCHA, MFA izleri)
- **Dosya/görsel:** Cloudinary
- **Ödeme:** Moka United (taksit sorgulama var)
- **Push:** Firebase Cloud Messaging (FCM)
- **Harita:** Leaflet + OpenStreetMap + tarayıcı Geolocation API
- **PWA:** manifest var, standalone, tema `#134B36` (koyu yeşil)

## Rota envanteri (bundle'dan çıkarıldı — 17 rota)

Kamuya açık: `/` `/hizmetler` `/surec` `/kurumsal` `/mezar-tasi-vitrini`
`/bakim-vitrini` `/bolgelerimiz` `/destek` `/gizlilik-politikasi` `/app`
`/odeme-sonuc` `/hesap-silme`

Rol alanları: `/hesabim` (müşteri) · `/esnaf` + `/esnaf-basvuru` (esnaf/usta)
· `/admin` (yönetici) · `/operasyon-haritasi` (saha)

## API uçları (bundle'dan çıkarıldı — 22 uç)

**Admin:** `bolge-talep-onayla` · `bolge-talep-reddet` · `esnaf-durum` ·
`esnaf-ekle` · `esnaf/{id}` · `rol-ata` · `siparis-esnaf-ata` · `siparis-iptal` ·
`siparis/{id}` · `tasarim-onayla` · `tasarim-reddet`

**Esnaf:** `esnaf/siparis-durum`

**Müşteri:** `kullanici/profil` · `kullanici/sozlesme-onayla` ·
`kullanici/telefon-guncelle` · `musteri/siparis-iptal`

**Ödeme:** `odeme-baslat` · `odeme/taksit-sorgula` · `indirim-kodu-dogrula`

**Doğrulama:** `telefon-dogrula-genel` · `telefon-kod-gonder` · `telefon-kod-dogrula`

## Ekran metinlerinden okunan işlevler

**Admin finansal:** "Havuzdaki Toplam Para" · "Vefa Komisyon Geliri" ·
"Toplam Aktif Esnaf" → komisyon havuzu ve hakediş yönetimi var

**Esnaf finansal:** "IBAN Bilgisi" · "IBAN Kaydedildi" · "Mevcut Bakiyeniz" ·
"Net Komisyon" → esnaf kendi bakiyesini ve komisyonunu görüyor

**Onay akışı:** "Onay Bekleyenler" · "Onay Bekliyor" ·
"Reddetme nedeni (esnafa iletilecek, opsiyonel)" → admin onay/red gerekçeli

**Bakım takibi:** "Rapor Bekleniyor" · "Sonraki Ziyaret" · "Videolu rapor"

**Mezar konumu:** "Mezar Yeri Sorgulama" · "Mezar Yeri Tarifi" ·
e-Devlet linkleri (`turkiye.gov.tr/...mezar-yeri-sorgulama`) + belediye
(`mebis.ankara.bel.tr`) → konum tespiti dış kaynaklara yönlendiriyor

**İki ayrı hizmet bölgesi seti:** `hizmetBolgeleriBakim` · `hizmetBolgeleriTas`
→ bakım ve mezar taşı için AYRI bölge/esnaf ağı

**Tasarım atölyesi:** "Mermer Rengi" · "Toplam Peyzaj Bedeli" · bitki adları
(Lavanta, Biberiye) · şablonlar → 3D/2D görsel konfigüratör, fiyat canlı hesaplanıyor

**Esnaf sözleşmesi:** `esnafSozlesmesi` → dijital sözleşme onayı

## Ticari model (siteden okundu)

**Üç bakım paketi, aylık abonelik + tek seferlik seçeneği:**
- Vefa 2.950 ₺/ay — ayda 1 ziyaret, temizlik, fotoğraflı rapor
- Huzur 4.400 ₺/ay — + çiçek dikimi, toprak bakımı, **videolu** rapor
- Hatıra 11.500 ₺/ay — ayda 2 ziyaret, 2 özel gün anma ziyareti, yazı yenileme,
  atanmış kıdemli uzman

**Düzenli (abonelik) planda %16'ya varan indirim** → tek seferlik / abonelik ikili
fiyatlandırma

**Ek gelir kalemleri:** peyzaj bedeli (tasarım atölyesinden, pakete eklenir) ·
mezar taşı yapımı (vitrinden usta seçilerek sipariş)

## Hizmet kapsamı

- **81 il, tüm ilçeler** iddiası · **264 kayıtlı mezarlık** (İstanbul ağırlıklı)
- İl/ilçe listesi bundle içinde gömülü (statik veri)
- Dört hizmet türü: peyzaj & ekim · mermer temizliği · düzenli sulama · fiziki kontrol

## Teklif için kritik ayrımlar

1. **Mevcut sistem NoSQL (Firestore), bizim kanon MSSQL.** Benzerini yaparken
   ilişkisel modele geçilecek — bu bir kayıp değil kazanç (finansal raporlama,
   komisyon hesabı, abonelik döngüsü ilişkisel modelde çok daha sağlam).
2. **Mevcut sistem CRA, SEO yok.** Next.js ile yapılırsa bu bir üstünlük olur —
   mezarlık adıyla organik arama trafiği bu iş için kritik.
3. **Marketplace finansal akışı var** (havuz, komisyon, IBAN, hakediş). Bu
   teklifin en riskli ve en değerli parçası — basit e-ticaretten farklı.
4. **Mobil uygulama zaten yayında.** Benzeri isteniyorsa mobil kapsamda mı,
   dışında mı — kapsam kararı.
