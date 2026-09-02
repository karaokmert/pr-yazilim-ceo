# ListON — durum

**ClickUp:** folder `901513786265` · Task List `901520399991` · Bugfix `901520399998` · Planning `901524533470`
**Prefix:** LO / LOAP / LOAPP / LOWS · **Task ID bandı:** PRY-152xx–PRY-180xx
**Ne:** Emlak talep-teklif platformu. Üye talep açar, emlakçı teklif verir. Mobil app + admin panel + web sitesi.
**Kim:** Buse (ana geliştirici) · Mert (planning ve onay)

⚠️ Ölçüm 2026-09-02, ClickUp taraması. Durum bilgisi bir hafta içinde eskir.

---

## Ne bitti

**EIDS (e-Devlet kimlik doğrulama) entegrasyonu** — son dönemin ana işi. Rol bazlı
bölünmüş: BE yetki doğrulama, DO taklit uç, FE, MB üç parça, BE mevcut emlakçılar,
FE dönüş sayfası. Hepsi completed.

**Görsel/medya hattı** — BE/FE/MB/QA dört ayak, hepsi completed.

**UI revize dalgası** — onboarding, talep tipi yönetimi, kart tasarımları, yatırım
fırsatı detayı, mahalle bilgisi, CTA buton, emlakçı home empty state.

**Daha önce kapanmış modüller:** Teklif İşlemleri (link teklif + acil etiket +
kredi hareketleri), Kredi/Kontör Yönetimi, In-App Ödeme, Emlakçı Başvuru,
Tanımlamalar, Admin Panel UI, App Full UI, Web Sitesi Kurulumu (Next.js),
Push/Bildirim Sistemi, Dashboard, Mobil Hesap Silme.

⚠️ **İki hatta FE ayağı geride kalmış** — kardeşleri completed, bunlar hâlâ Open:
- PRY-17811 (FE - Yerel geliştirme anahtarı, panel tarafı)
- PRY-17830 (FE - Talep tipi/amacı, panel tarafı)

---

## Şu an açık — konu damarları

**EIDS devamı** — PRY-17908 (Mert'ten beklenen bilgiler ve teyitler, 8 kalem) urgent
ve **atanmamış** · PRY-17906 (bakanlığa bildirilen IP'ler sunucumuzun adresi değil)
high · PRY-17894 (sağlık kontrolü ucu) · PRY-17372 (İlan EIDS No, lıve-dev)

**Bildirim sistemi** — PRY-17802 (panelde canlı bildirim hiç gelmiyor) high ·
PRY-17807 (mobilde canlı bildirim kanalı dinlenmiyor) · PRY-17826 (push kaydı
sessizce başarısız olabiliyor) · PRY-15892 (in-app bildirim listesi + okundu
endpoint'leri yok) · PRY-17808 · PRY-17912 · PRY-15981

**Teklif akışı** — PRY-15850 (manuel teklif dinamik alanlar, RegionalRequestDetail'e
ListingTypeId) high atanmamış · PRY-15891 (VIEWED durumu backend'de yok) ·
PRY-15896 (Gelen Teklifler endpoint'i yok) · PRY-15897 (kapanan talebe gelen
teklifler görünmüyor) · PRY-15899 (firma adı dönmüyor) · PRY-15894/15895 (teklif
sayıları dönmüyor) · PRY-15970 (teklif detay map) · PRY-17851 (sahipsiz teklif
görselleri depoda birikiyor)

**Talep akışı** — PRY-15964 (**bloke**) · PRY-17861 (yatırım talebinde konum
zorunlu tutulmamalı) · PRY-17853 (talep oluşturmada uydurma değerler) ·
PRY-15969 (akış redesign) · PRY-15979 · PRY-15984 · PRY-15985/15986 · PRY-15987

**Emlakçı profil / kayıt** — PRY-15963 (**bloke**) · PRY-15885 (kayıtta telefon
doğrulama OTP SMS'i hiç gitmiyor) **urgent, atanmamış** · PRY-15898 · PRY-15983 ·
PRY-15901 · PRY-15965 · PRY-15962 (country code — proje kararı bekliyor) ·
PRY-17857 · PRY-18059 (SMS akışında telefon ve mesaj içeriği loglanıyor)

**Paket / kredi / abonelik** — PRY-15844 (aktif paket cüzdanda görünmüyor) ·
PRY-15902 (get-active-subscription yok) · PRY-15879 · PRY-15880 (kredi satın alma
PackageName NOT NULL) · PRY-15961

**Bölge yönetimi** — PRY-15828 (paketsiz realtor bölge seçimi akış hatası, Mert) ·
PRY-15833 (RealtorRegion primary kaydı + DistrictId eksik) · PRY-15987

**UI redesign yığını** — 20+ kalem, çoğu lıve-dev

**İçerik dürüstlüğü kümesi** — PRY-17854 (panelde sabit/uydurma bilgiler) ·
PRY-17855 (sitede uydurma metrikler, olmayan iletişim bilgileri, eksik yasal
alanlar) · PRY-17856 (mobilde bilinmeyen yerine uydurma varsayılan)

**Altyapı / güvenlik** — PRY-17907 (**ayrı prod ortamı yok, tek sunucu hem deneme
hem canlı**) · PRY-17799 (yayın hattı mağazaya koşulsuz gönderim) high ·
PRY-17806 · PRY-17905 (liston.com.tr www'suz 404) high · PRY-17859 (yönetici şifre
kuralı sıradan kullanıcıdan zayıf) · PRY-17858 (bakım modu) · PRY-17852 (panelde
şifre değiştirme hiçbir yere yazmıyor — sahte başarı) **pause**

---

## Bloke

- **PRY-15964** — Talep Düzenleme "Geçersiz Talep ID'si" hatası. Backend, atanmamış.
- **PRY-15963** — Avatar yüklendikten sonra hesabımda görünmüyor. Backend, atanmamış.

---

## Planning'de bekleyen (henüz başlamamış)

**26 Ağustos müşteri toplantısından çıkmış, açıklamaları DOLU:**
- **PRY-17980 (LOAP - Portföy Yönetimi)** — portföy ekleme EIDS doğrulamalı,
  portföy süresi EIDS süresiyle sınırlı, pakete bağlanabilir (paket içinden sayı
  yönetimi), teklif verirken seçilebilir/eklenebilir, link paylaşımı, teklif
  adımında portföye ekleme akışı
- **PRY-17981 (LOAP - Bölge Yönetimi)** — emlakçı bölge seçimi şehire bağlanıyor;
  bildirim ayarlarına "Gelecek Talepler → bölgenin ilçelerinden seç"
- **PRY-17979 (LOAP - Satıcı Tipleri)** — Gayrimenkul Sahibi / Gayrimenkul
  Danışmanı, kayıt ol akışına
- PRY-17978 (Kayıt olurken / Gayrimenkul Satmak İstiyorum) — açıklama boş
- PRY-17982 — başlık tek harf "L", kazara açılmış boş kayıt
- PRY-17800 (EAS bulut derleyicisi yeni Node sürümü) — sonraki mobil sürümün
  ön koşulu

**"team" statüsünde eski kuyruk (hepsi Mert'te, çoğu açıklaması boş):** SMS
İşlemleri · Paket İşlemleri Market Entegrasyonu · DataLayer Modernizasyon (eski
borçlar) · Talep Yönetimi (high) · Proje Ayarları · Push Notification & Device
Token · Anasayfa · Öne Çıkan İlanlar & Yatırım Fırsatları · Layout Üye · Üye
Yönetimi · Paket Yönetimi · Site Ayarları

**"planned":** Realtor Fatura Bilgileri · İndirim Kuponları Modül

---

## Sprint 7'de yapılacaklarla eşleşme (Buse — 6 iş)

**31 Ağustos'ta dört task açılmış ama DÖRDÜNÜN DE AÇIKLAMASI BOŞ**, hiçbiri
Buse'ye atanmamış, statüleri "full stack":
- PRY-18051 — Emlakçı Kayıt ve Üyelik Doğrulama
- PRY-18052 — Portföy Yönetimi
- PRY-18053 — Paket & Kredi Yönetimi
- PRY-18054 — Bölge Yönetimi Revizeleri

Kapsam bu task'larda değil, **Planning'deki eski kayıtlarda** (yukarıda) ve
**PRY-18057 (LO - Emlakçı Belge Yönetimi)** içinde — o task PRY-18051'in ne
yapacağını anlatıyor: mobildeki "başvurunuz inceleniyor" bekleme ekranı
kaldırılıyor, kimlik belgesi ekleniyor (bireysel üyeler), belge onay/red panelde
Başvurular'dan emlakçı detayına taşınıyor. Belge onay/red bildiriminin kodda hiç
olmadığı da orada yazılı.

**Karşılığı hiç olmayan iki başlık:** Proje Planlaması · Teklif Yönetimi

⚠️ **Teklif Yönetimi'nin içeriği Portföy'ün içinde** — PRY-17980 "teklif verirken
portföy seçilecek / teklif adımında portföye ekleme akışı" diyor. İki başlık ayrı
gereksinim olarak yazılırsa çakışırlar.

⚠️ **Portföy EIDS'e bağımlı** ve EIDS'te PRY-17908 (urgent, atanmamış, Mert'ten
8 kalem bilgi bekliyor) açık duruyor. O kapanmadan portföye girilirse iş yarıda
kalır.

⚠️ **Her başlığın altında ona ait açık bugfix'ler var ama hiçbiri şemsiyeye
bağlanmamış** — iş yapılırken tek tek bulunması gerekecek. Örneğin Emlakçı Kayıt
altında PRY-15885 (OTP SMS gitmiyor, urgent).

---

## Dikkat: tekrar eden kayıtlar

- **PRY-17370 / 17371 / 17372** — üçü de "LO - İlan EIDS No Geliştirmesi"
- **PRY-15988 ↔ 16214** (mahalle bilgisi) · **15972 ↔ 16213** (cta height) ·
  **15924 ↔ 16210** (empty state) · **16165 ↔ 16166** (talep tip yönetimi) —
  her çiftte biri kapalı, biri açık
- **PRY-15898 / 15983 / 15963** — üçü de emlakçı profil fotoğrafı, aynı sorunun
  üç parçası, ayrı ayrı duruyor
- **PRY-15426 ↔ 18053** (paket) · **17981 ↔ 18054** (bölge) · **17980 ↔ 18052**
  (portföy) — aynı konu Planning ve Task List'te ikişer kayıt

## Genel gözlem

Yüksek öncelikli işlerin neredeyse hepsi **atanmamış.** Atama yalnız Mert ve Buse
üzerinde toplanıyor, geri kalan onlarca task sahipsiz duruyor.
