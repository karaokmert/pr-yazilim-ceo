# Kapanış — 2026-08-25 · EV (Mezarlık Bakım Projesi teklifi)

**Tetik:** Mert teklif işi için oturum açtı · **Müşteri:** Emre Telyar

---

## Ne bitti

**Teklif dokümanı üretildi ve teslim edildi.**
`~/Desktop/Mezarlik Bakim Platformu - PR Yazilim Teklif.docx`

Mert'in şablonu (`~/Desktop/Mezarlık Bakım Projesi .docx`, VisViva Medu teklifi)
kopyalanıp gövdesi değiştirildi. Kapak, logo, başlık/altbilgi, paragraf
stilleri ve **anlatım dili** birebir korundu — Mert'in talimatı:
*"metinleri anlatımı içeriği koru mutlaka sadece düzenle."*

### Referans inceleme — ölçüm dosyaları

`incelemeler/vefaapp-teklif/` altında beş doküman:
- `01-teknik-envanter.md` — yığın, rota ve API envanteri
- `02-gereksinim-cikarimi.md` — ilk çıkarım (bir kısmı sonradan düzeltildi)
- `03-panel-icleri-olcum.md` — **panel içleri ÖLÇÜLDÜ**
- `04-fiyatlama-mekanigi.md` — fiyat ve konfigüratör mekaniği
- `05-kapsam-karari.md` — Mert ile netleşen kapsam

### Ölçüm yöntemi — kayda değer

Referans sistem **Create React App** (Next.js değil), client-side render.
Bu yüzden **panel arayüzlerinin tüm kaynak kodu JS bundle'ında açık** —
giriş yapmadan sekme adları, buton etiketleri, durum değerleri, Firestore
koleksiyon adları ve fiyat sabitleri okundu.

Bundle: `main.c8b20dfb.js` (1.2 MB). Playwright ile sayfa gezildi, bundle
`curl` ile çekilip Python ile analiz edildi.

---

## Yanıldığım ve düzelttiğim iki şey

**1 · "Dört panel var, biri saha paneli."** Mert *"esnaf saha panellerine emin
misin?"* diye sordu, ölçüm yapıldı: `/operasyon-haritasi` ayrı panel DEĞİL,
admin panelinin `map` sekmesi. Üç panel var (müşteri/esnaf/admin).
**Sen sormasan düzelmezdi** — emin konuşmuşum, değildim.

**2 · Dosyayı bozdum ve "sağlam" dedim.** İçindekiler tablosunu düzeltirken
`<w:t>` içindeki biçim etiketlerini de sildim, XML kapanışı bozuldu, Word
açmadı. **Üstelik "ZIP sağlam" diye doğrulamıştım** — zip sağlamdı, içindeki
XML değildi. Yanlış şeyi ölçtüm.
**Ders:** bir dosyanın açıldığını doğrulamak = onu açan bir araçla denemek
(`textutil -convert`), arşiv bütünlüğüne bakmak değil.

**3 · Word "salt okunur" açıyordu** — sebep dosya içinde koruma değil,
macOS `com.apple.quarantine` genişletilmiş özniteliği. `xattr -d` ile
kaldırıldı. Yeni üretilen her docx'te tekrar edecek.

---

## Kapsam — Mert'le netleşen

**Dört arayüz:** web sitesi + müşteri üye alanı · müşteri mobil (iOS+Android) ·
saha personeli mobil (iOS+Android) · yönetici paneli

**İki ürün hattı:** bakım hizmeti (abonelik + tek seferlik, iç içe) ·
mezar taşı yapımı (galeriden tıkla → sipariş → online ödeme)

**İş akışı:** müşteri sipariş → admin saha personeline atar → personel gidip
yapar, öncesi/sonrası fotoğraf yükler → müşteri görür

**Kapsam DIŞI (Mert'in kararı):** esnaf/tedarikçi paneli, hakediş, komisyon,
IBAN, esnaf sözleşmesi, bölge talebi, iş havuzu/gönüllü üstlenme

**Ek hizmet olarak ayrıldı:** mezar taşı satış hattı · dış tedarikçi ağı ·
saha uygulaması çevrimdışı çalışma

⚠️ **Abonelik ve müşteri mobil uygulamasını ek hizmete koymayı önerdi, itiraz
ettim ve kabul etti:** abonelik ayrılabilir bir modül değil (veri modeli
kararı, sonradan eklenirse sipariş modeli yeniden yazılır); müşteri mobil
uygulaması ise bu işin varlık şartı (push bildirim olmadan "raporunuz hazır"
haberi gitmiyor). Görsel konfigüratörü de aynı sebeple baza aldım — satışın
kendisi.

---

## Fiyat — Mert'in kararı

- **Baz paket: 300.000 ₺ + KDV**
- Sunucu: 250 $/ay + KDV (şablondan)
- Bakım: **500 $/ay + KDV** — yalnız hata giderme + ayakta tutma, yeni
  geliştirme YOK
- Adam saat: **40 $ + KDV**
- Ek hizmetler: fiyatsız listelendi, Mert koyacak
- Süre: 6 ay (24 hafta), başlangıç 15.09.2026

⚠️ **Üç kez söyledim, kayda geçiyor:** bu kapsam 300.000 ₺'nin belirgin
biçimde üstünde. Karşılaştırma kendi şablonumuz — VisViva Medu 24.500 €
(~1,15M ₺), 6 ay, 4 panel, **mobil uygulama yok, tekrarlayan ödeme yok,
saha operasyonu yok.** Mert fiyatı bilerek koydu; gerekçesini söylemedi.
Teslim baskısı geldiğinde bu not hatırlanmalı.

---

## Ölçüldü ama teklife girmedi — bilinmesi gerekenler

**Referansta fiyat yönetimi YOK.** Paketler (2.950/4.400/11.500 ₺), dokuz
bitki fiyatı, mermer farkları — hepsi kaynak koda gömülü. Fiyat değiştirmek
için yeniden yayın gerekiyor. **Bizim teklifte panel yönetimi var** — somut
üstünlük olarak yazıldı.

**"%16 indirim" hesaplanmıyor, sabit yazılmış.** Gerçek oranlar %15,3 / %16,8
/ %17,4 çıkıyor.

**Tasarım atölyesi 3D değil** — statik PNG'lerle 2D katmanlı kompozisyon.
Teklifte "görsel peyzaj tasarım aracı" denildi, "3D" denilmedi.

**Vitrin kartlarının ayrı URL'i yok** (modal açılıyor) → SEO kaybı. Bizim
teklifte "her kayıt kendi adresine sahip olacak" diye yazıldı.

**Açık kalan iki teknik karar** (teklifte var, kararı verilmedi):
- Admin rapor onay kapısı olacak mı? (referansta var: "Fotoğrafları Reddet")
- Saha uygulaması çevrimdışı çalışması — ek hizmete kondu ama mezarlıklarda
  bağlantı zayıf; müşteri sahada yaşayınca zorunlu hâle gelir

---

## Bir sonraki hareket

Mert dosyayı açıp inceleyecek. Ek hizmet fiyatlarını koyacak.
Word'de içindekiler tablosu güncellenmeli (sağ tık → Alanı Güncelle).
