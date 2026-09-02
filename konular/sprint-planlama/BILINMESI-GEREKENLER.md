# Sprint planlama — bilinmesi gerekenler

Mert'in haftalık sprint planlamasında Clara'nın rolü, ClickUp'ın gerçek düzeni ve
2026-09-02'de ölçülen sistemik sorunlar.

---

## Planlama nasıl yürüyor

**Sprint Çarşamba sabahı başlar**, ertesi Salı biter. Mert ekiple toplantıya
girmeden önce Clara ile planı ClickUp'a işler.

**Kaynak Google Sheets, kayıt ClickUp.** Mert haftalık planı kendi tablosunda tutuyor
— kişi × gün ızgarası. ClickUp o planın kaydı, kaynağı değil.

**Akış kişi kişi.** Mert sırayı belirler ("sıradaki Didem"), tablodaki işleri verir,
Clara ClickUp'ta karşılığını arar, yoksa açar, atar, tarihler, "Sonraki Sprint"
işaretler.

⚠️ **Yeni işin ClickUp'ta olmaması normal** — o gün açılacak. Mert'in düzeltmesi:
*"zaten bu taskleri yeni açıcaz, sen eskiyi tarıyorsun şu an."* Değerli olan eski
durum: ne bitmiş, ne bloke, ne sahipsiz.

---

## ClickUp'ın gerçek düzeni

**Space:** PR Team (48321079), workspace 24450758, task öneki `PRY-`.

**Sprint listeleri boş ve öyle kalıyor.** Sprint 3–8 listeleri var ama hiçbirinde
task yok. Sprint üyeliği **task üzerindeki "Sonraki Sprint" checkbox** ile tutulur
(`a320e4f0-8618-453a-b808-92f125fa2f4e`). Otomasyon task'ı sprint listesine kendisi
taşır.

⚠️ `clickup_filter_tasks` sprint listelerini boş gösteriyor — doğrulama için task'ın
kendi **"Sprint" short_text alanına** bak (`8770d739-932e-4711-ac30-f0a824a559aa`).
Mert bu alanı otomasyonla dolduruyor: *"Ben otomatik yazıyorum ki sen kontrol
ettiğinde oku diye."*

**Ad eşlemesi tutmuyor** — tablo ile ClickUp farklı adlar kullanıyor:
WD = Wupdoc · TP = TPWS (Keba folder'ı altında) · KebaTP diye önek yok · Keba
folder'ında iki ürün var (KebaAI/ERP → Mert, TPWS → Didem) · Alesta Marwell'de ·
"Marketing" folder'ı Gazi'nin kendisi · PR Studio'da üç müşteri (Tedrik, KaraokYMM,
Efranca) · Adalya'nın folder'ı yok, işleri Creative Projeleri ve Websites'a dağılmış.

**Statü setinde Türkçe klavye izleri var:** `blockıng`, `operatıon`, `productıons`,
`lıve-dev` — API'ye aynen böyle yazılır.

**Rate limit gerçek bir sınır.** ~330 yazma sonrası 491 dakika limit geldi. Büyük
temizlik ile planlama aynı güne denk gelmemeli; planlama önce.

---

## 2026-09-02'de ölçülen sistemik sorunlar

### 1 · "completed" kapanış değildi — 256 kayıt

Space genelinde 256 task "completed" statüsündeydi ama `date_closed` boştu; ClickUp
onları **açık iş** sayıyordu. Herkesin yükü şişik görünüyordu.

Nerede birikmiş: Keba 57 · Wupdoc 43 · Gazi 34 · ListON 24 · PR Studio 11 · Marwell
12 · Venture Studio 11 · Goat 11 · Egeli 7 · Websites 7.

**Bu bir alışkanlık sorunuydu, kaza değil.** En eski kayıt PRY-14060'a kadar
gidiyor — bir yıla yakın süredir iş bitiyor, "completed" işaretleniyor, kimse
Closed'a çekmiyor.

**Ve birikme kendini besliyordu:** kapanış disiplini olmayınca bir işin zaten var
olduğu görülmüyor, tekrar açılıyor. Websites'ta GPWS favicon ve açılır menü işleri
iki ayrı numarayla kayıtlı (17588/17589 ve 17913/17914); Keba'da 16183–16186 ile
16783–16785 aynı başlıkları taşıyor.

→ Karar: `kararlar/2026-09-02-completed-kapanis-demektir.md`

### 2 · Sahipsiz kritik işler

**PR Template hattı komple sahipsiz** — 9 iş, ikisi urgent güvenlik yükseltmesi
(astro 7.2.9, next 16.3.3), ikisi pause'da. Bu şablon tüm yeni projelerin temeli;
açık orada durursa her yeni projeye iniyor.

**ListON'da beş urgent/high sahipsiz** — EIDS IP bildirimi yanlış (PRY-17906),
www'suz domain 404 (PRY-17905), kayıtta OTP SMS hiç gitmiyor (PRY-15885), ve
**PRY-17908 doğrudan Mert'in cevabını bekliyor** (EIDS için 8 kalem teyit).

**Goat'ta üç sahipsiz kritik** — PRY-17542 anasayfa içeriği kalıcı siliyor (urgent,
veri kaybı) · PRY-17560 yayında sahte veri gösteriliyor · PRY-17478 boost başlatma
patlıyor.

**Keba ERP'de üç bloke, üçü de atanmamış, üçü de 2026-08-30'da aynı gün** —
banka (18042), ürün (18043), cari (18044) "tam eşleme" adımları. Tek bir ortak sebep
olma ihtimali yüksek; ölçülmedi.

**Egeli Planning listesi** 51 kalemlik "customer" statüsünde talep havuzu — hiçbiri
atanmamış, hiçbiri iş emrine dönmemiş. Bu bir liste değil, kapanmamış toplantı çıktısı.

### 3 · Kopya task birikimi

Gazi'de "Kurulan reklamların düzenli takibi ve optimizasyonu" **altı ayrı kopya**
halinde açık. "SEO raporlaması" iki, "bütçe revizesi" iki, "düşük bütçeli Google Ads"
iki kopya. ListON'da en az beş çift (mahalle bilgisi, cta height, empty state, talep
tip). PR Studio'da "TE - Ürün Varlığı" üç kopya.

### 4 · Kişi eşleşmesi tutmuyordu

Sprint 7 planında Umutcan'ın Goat'ta hiç açık task'ı yoktu ama Goat'ta iki iş
verilmişti; Didem'in BT'de hiç task'ı yoktu ama BT'de çalışacaktı; Yiğit'in PR
Yazılım'da tek işi vardı ve o da kapanmıştı ama dört iş verilmişti.

Sebep: haftalık plan ClickUp'tan bağımsız yaşıyor. Sprint 7'nin 42 iş kaleminden
ClickUp'ta gerçek kaydı olan **üç tanesiydi** (PRY-18084, 18082, 18046).

---

## Sprint 7'de kurulan düzen

**Task açma biçimi:** `{Proje} - {İş}` · proje folder'ının Task List'ine · atama +
tarih + "Sonraki Sprint" bir arada.

**Modüllü projede custom field.** Goat'ta `Goat Modül` (18 seçenekli dropdown,
`21752efa-2390-4bd1-9118-050346794b81`) — test task'ları buna göre bölündü, hangi
modülün test edildiği ClickUp'tan okunuyor.

**Şemsiye + alt görev.** Gazi'de 25 SEO işi tek şemsiyeye (PRY-18118) bağlandı.
25 satır yerine bir satır; takip kolaylaştı. Mert kurdu.

⚠️ `clickup_update_task` **parent alanını değiştiremiyor** — bir task'ı alt görev
yapmak arayüzden yapılır. Mükerrer varsa taşımak yerine kapatmak pratik.

**Çok günlü iş** → `start_date` + `due_date` birlikte.

---

## Üretilen panolar

**Sprint 7 Çizelgesi** — kişi × gün ızgarası, Excel görünümü. Task'a tıklayınca
açıklama, doküman bağlantısı, bağımlılıklar; gün değiştirme; değişiklikler altta
birikiyor, "Değişiklikleri al" ile metin çıkıyor.
https://claude.ai/code/artifact/7a670677-4cb9-45e0-9157-9467c063ade7

**Bekleyen İş Envanteri** — Sprint 7 dışında bekleyen işler, kişi bazında, proje
kırılımıyla; her işin ne beklediği (bloke / durdurulmuş / onayda / dev'de / canlıda
kapatılmamış / inceleme / planlamada).
https://claude.ai/code/artifact/b1134970-d602-4784-8d37-f31b5722e210

---

## Açık kalanlar

**Rate limit sebebiyle işlenemedi** (2026-09-02, ~8 saat bekleme):
- PRY-18109 (TUERP Fatura) start date 07.09 → due 08.09
- PRY-18115 (TP Mobil APP) start date 03.09 → due 07.09
- PRY-18046 (Efranca Revizeler) mükerrer, kapatılacak — yenisi PRY-18149

**Sprint point:** Mert istedi ama ClickUp'ta karşılık gelen alan bulunamadı. Mevcut
custom field'lar: Assign Date · People · Project Name · İş Sırası (number) ·
Sonraki Sprint · Sprint Task · Sprint (short_text). Sprint Points ClickApp'i kapalı
olabilir. **Karar bekliyor.**

**Proje ve task takibi geliştirilecek** — Mert'in ifadesi. Bugünkü panolar ilk adım.
