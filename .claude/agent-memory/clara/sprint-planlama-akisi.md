---
name: sprint-planlama-akisi
description: Mert'le Çarşamba sprint planlamasının nasıl yürüdüğü — Google Sheets tablosu kaynak, ClickUp kayıt; kişi kişi ilerlenir, task açılır, tarih ve Sonraki Sprint işaretlenir
metadata:
  type: project
---

Sprint planlaması **Çarşamba sabahı** yapılır, Mert ekiple toplantıya girmeden önce.

## Kaynak: Google Sheets, ClickUp değil

Mert haftalık planı **kendi Excel/Sheets tablosunda** tutuyor — kişi × gün ızgarası
(satır kişi, sütun Çar/Per/Cum/Pzt/Sal). Sprint hafta ortasında başlıyor: Çarşamba →
ertesi Salı.

⚠️ **ClickUp'taki Sprint listeleri boş** (Sprint 3–8 hepsi). Sprint kaydı liste
üyeliğiyle değil, task üzerindeki **"Sonraki Sprint" checkbox custom field**'ıyla
tutuluyor → [[clickup-sprint-mekanigi]]

## Akış — kişi kişi, proje proje

Mert sırayı kendisi belirler ("sıradaki Didem", "şimdi Yiğit"). Her kişi için:

1. **Tablodaki işleri oku** — Mert ekran görüntüsü paylaşır ya da metin olarak yazar
2. **ClickUp'ta karşılığını ara** — task var mı, hangi listede, statüsü ne
3. **Yoksa aç** — proje folder'ının Task List'ine, `{Proje} - {İş}` biçiminde
4. **Ata + tarihle + Sonraki Sprint işaretle** — üçü bir arada
5. **Çakışma varsa söyle** — mükerrer task, yanlış etiket, sahipsiz bağımlılık

**Yeni işin ClickUp'ta olmaması normal** — o gün açılacak. "Yok" diye raporlamak
değerli değil; değerli olan ESKİ durum: ne bitmiş, ne bloke, ne sahipsiz.
(Mert'in düzeltmesi 2026-09-02: *"zaten bu taskleri yeni açıcaz, sen eskiyi
tarıyorsun şu an."*)

## Ad eşlemesi tutmuyor — tabloyla ClickUp farklı ad kullanıyor

- **WD** = Wupdoc (ayrı proje değil)
- **TP** = TPWS, Keba folder'ının altında (ayrı folder yok — Mert kararı 2026-09-02)
- **KebaTP** = ClickUp'ta böyle önek yok, iş TPWS adıyla yürüyor
- **Keba** folder'ında iki ürün: KebaAI/ERP (Mert) ve TPWS (Didem)
- **Alesta** = Marwell folder'ında (marka dönüşümü sürüyor)
- **Marketing** diye ayrı folder yok — o Gazi Hastanesi'nin kendisi
- **PR Studio** folder'ında üç müşteri: Tedrik, KaraokYMM, Efranca
- **Adalya** folder'ı yok; işleri "Creative Projeleri" ve "Websites"e dağılmış

## Task açarken

**Modüllü projelerde custom field kullan.** Goat'ta `Goat Modül` (18 seçenekli
dropdown, id `21752efa-2390-4bd1-9118-050346794b81`) var — test task'ları bu alana
göre bölündü, hangi modülün test edildiği ClickUp'tan okunuyor.

**Çok günlü iş** → `start_date` + `due_date` birlikte. Mert'in isteği (2026-09-02):
tabloda iki güne yayılan iş ClickUp'ta da öyle görünsün.

**Şemsiye + alt görev** iyi çalışıyor. Gazi'de 25 SEO işi tek şemsiyeye (PRY-18118)
alt görev olarak bağlandı — 25 satır yerine bir satır, takip kolaylaştı. Mert kendisi
kurdu.

⚠️ `clickup_update_task` **parent alanını değiştiremiyor** — bir task'ı alt görev
yapmak arayüzden yapılır. Mükerrer varsa taşımak yerine kapatmak daha pratik.

## Günlük sprint kontrolü (karar 2026-09-04)

Sprint kurulduktan sonra **Mert isteyince** ("durum ne") günlük kontrol çıkarılır —
otomatik değil, Mert'in tercihi. İçerik üç kalem: kimde ne açık · ne bekliyor ve
**kaç gündür** · tabloya/tarihe göre kayan işler. Bitenler sayılmaz. Kaynak ClickUp,
task'ların "Sprint" custom field'ı üzerinden taranır.

## Rate limit — gerçek sınır

2026-09-02'de ~330 yazma (256 kapatma + 70 task açma/güncelleme) sonrası ClickUp
**491 dakika** rate limit verdi. Büyük temizlik + planlama aynı güne denk gelirse
sona kalan işler yapılamıyor. Sıralamayı buna göre kur: önce planlama, temizlik
sonra.

## Statü seti (space 48321079)

Open · full stack · backend · front · ui · design · creative · operatıon ·
planning · in progress · blockıng · revise · test · pause · pr · pending approval ·
completed · lıve-dev · ready for productıon · productıons · Closed

⚠️ Türkçe klavye izleri var: `blockıng`, `operatıon`, `productıons`, `lıve-dev` —
API'ye aynen böyle yazılmalı.

**"completed" kapanış değildi.** 2026-09-02'de 256 kayıt "completed" ama
`date_closed` boş halde duruyordu; Mert kararıyla hepsi Closed'a çekildi. Bundan
sonra completed = kapanış unutulmuş demek.
