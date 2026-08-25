# Panel içleri — ÖLÇÜLDÜ (bundle kaynak kodundan, 2026-08-25)

⚠️ **Bu dosyadaki her şey ölçüm, çıkarım değil.** Kaynak: `main.c8b20dfb.js`
içindeki React component kodu. Panel arayüzleri client-side render olduğu için
tüm sekme adları, buton etiketleri, durum değerleri ve veri modeli bundle'da
açık duruyor. Giriş yapılmadan okundu.

---

## Veri modeli — Firestore koleksiyonları (7)

`users` · `orders` · `subscriptions` · `orderContacts` ·
`partner_applications` · `partner_designs` · `district_requests`

**Okunan anlam:** sipariş (tek seferlik) ve abonelik (tekrarlayan) **ayrı
koleksiyonlar** — iki farklı ürün hattı. `orderContacts` ayrı tutulmuş
(iletişim bilgisi sipariş kaydından ayrı → KVKK/gizlilik ayrımı).
`partner_*` = esnaf başvuruları ve portföy tasarımları. `district_requests` =
esnafın ilçe/bölge talebi.

---

## Üç panelin sekme yapısı — kesin

### Müşteri paneli (`/hesabim`) — 3 işlevsel sekme
`overview` (Abonelik Özeti) · `gallery` (Bakım Raporları & Fotoğraflar) ·
`profile` (Profil & Abonelik Yönetimi) + `kvkk` / `gizlilik` görüntüleme

**Ölçülen ekran öğeleri:**
- "Aktif Abonelik" sayacı / "Abonelik Yok"
- "Aktif Abonelikleriniz" listesi
- **"Otomatik Yenileme" aç/kapa anahtarı** (`autoRenew`) — *"Süresi bitince
  otomatik uzatılır"*
- "Aboneliği İptal Et" · "Siparişi İptal Et"
- "Raporu Görüntüle" · "Yazdır" (PDF)
- "Hizmeti Değerlendir" (puan/yorum bırakma)
- "Özel Anma Günleri" · "Yakınlık Derecesi" · "Mezar Yeri Tarifi"
- "Hesap Özeti" · "Kalıcı Olarak Sil" (hesap silme)

### Esnaf paneli (`/esnaf`) — 5 sekme
`pool` (İş Havuzu) · `active` (Aktif Görevler) · `completed` (Tamamlananlar) ·
`wallet` (Cüzdanım) · `profile` (Profil & Bölge)

⚠️ **EN ÖNEMLİ BULGU — iş dağıtımı iki yollu:**
- **"İş Havuzu"** — atanmamış işler havuzda listelenir, esnaf **"Görevi Üstlen"**
  butonuyla kendisi alır (self-service, ilk gelen alır)
- **"İşi Manuel Ata"** — admin bir işi belirli esnafa doğrudan atar
  (`assignedPartnerId`)

Yani sistem **hem otomatik/gönüllü hem manuel atama** destekliyor. Sekme
yanlarında bekleyen iş sayısı badge olarak gösteriliyor.

- **"İşi Tamamla" butonu fotoğraf yüklenmeden PASİF** — buton metni
  *"Önce Fotoğrafları Yükleyin"* oluyor. **Fotoğraf, iş kapatmanın ön koşulu
  ve bu kural kodda zorlanmış.**
- Cüzdan: IBAN kaydet, bakiye, net komisyon
- Profil & Bölge: hizmet ili/ilçesi talebi ("Talep Gönder", "Şehir Talepleri")

### Admin paneli (`/admin`) — 10 sekme
`overview` (Genel Bakış) · `orders` (Siparişler) · `subscriptions` (Abonelikler) ·
`partners` (Saha Ekibi) · `applications` (Başvurular) · `demands` (Şehir
Talepleri) · `designs` (Tasarım Onayları) · `finances` (Finans) ·
`map` (Saha Haritası) · `reviews` (Yorumlar)

**Ölçülen ekran öğeleri:**
- "Yeni Usta Ekle" · "Aktif Usta" · "Toplam Aktif Esnaf" · "Doğrulandı" ·
  "Yetkisi İptal Edildi"
- **"Fotoğrafları Reddet"** — admin esnafın yüklediği fotoğrafı reddedip
  yeniden çekilmesini isteyebiliyor (kalite kapısı)
- "Onayla" / "Reddet" (başvuru, tasarım, şehir talebi)
- "Havuzdaki Toplam Para" · "Vefa Komisyon Geliri" · **"Detaylı Excel Raporu
  İndir"**
- "Saha Haritası" — işlerin harita üzerinde görünümü
- "Sistem Durumu" · "Memnuniyet" · "Aktif İl"
- "Galeriden Sil" (içerik yönetimi)

⚠️ **Admin panelinde sekme adı "Saha Ekibi" ama içerik esnaf yönetimi**
("Yeni Usta Ekle", "Aktif Usta"). **`/operasyon-haritasi` ayrı bir panel DEĞİL —
admin panelinin `map` sekmesidir.** Yani sistemde üç panel var: müşteri, esnaf,
admin. Saha ekibi = esnaf; ayrı bir dördüncü panel yok.

---

## Sipariş durum seti — ölçülen

`pending` (Bekliyor) → `approved` / atandı → `fulfilled` / `done`
(Tamamlandı) · `rejected` (Reddedildi) · İptal Edildi

Ödeme: `billingMethod: "moka_recurring"` (abonelik) ·
`paymentStatus: "failed_final"` (tahsilat kalıcı başarısız)

⚠️ **`moka_recurring` ve `failed_final` → gerçek tekrarlayan ödeme altyapısı
var ve başarısız tahsilat yönetimi kodlanmış.** Abonelik "isim" değil,
sağlayıcı seviyesinde otomatik tahsilat.

---

## Esnaf sözleşmesinden okunan ticari model

Bundle içindeki sözleşme metninden: *"Esnaf Payı, Esnaf'ın beyan ettiği IBAN'a
Şirket tarafından **aylık periyotlarla** ödenir."*

→ Platform tahsil eder, komisyonu keser, esnafa aylık toplu öder.

---

## Teklif için sonuç — kapsam kararları

**1 · Abonelik: GERÇEK tekrarlayan ödeme.** `autoRenew` anahtarı, `moka_recurring`
tahsilat yöntemi, `failed_final` durumu, "Aboneliği İptal Et". Bu teklifte
**tekrarlayan ödeme + başarısız tahsilat yönetimi + otomatik yenileme** olarak
yer almalı. Tek seferlik sipariş ayrı akış (ayrı koleksiyon).

**2 · Panel sayısı: ÜÇ, dört değil.** `/operasyon-haritasi` admin'in bir sekmesi.
Önceki çıkarımım ("saha ayrı panel") **yanlıştı** — ölçüm düzeltti.

**3 · Mezar taşı hattı ayrı bir ürün.** `partner_designs` koleksiyonu +
"Tasarım Onayları" admin sekmesi + vitrin (29 kayıt, 25.000–350.000 ₺,
usta fiyatlı). Bakımdan bağımsız akış.

**4 · İş dağıtımı iki yollu** (havuz + manuel atama). Mert'in tarif ettiği model
sadece manuel atama — havuz/üstlenme mekaniği **kapsam dışı bırakılabilir**,
bu bir sadeleşme.

**5 · Fotoğraf kalite kapısı var.** Esnaf yükler, admin reddedebilir
("Fotoğrafları Reddet"), müşteri sonra görür. Yani rapor müşteriye
**admin onayından sonra** açılıyor.

**6 · Değerlendirme/yorum sistemi var** ("Hizmeti Değerlendir", admin
`reviews` sekmesi, "Memnuniyet" metriği).

**7 · Excel raporu** admin finans sekmesinde ("Detaylı Excel Raporu İndir").
