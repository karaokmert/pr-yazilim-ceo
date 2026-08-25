# Teklif düzenleme kararları — Emre Telyar / Mezarlık Bakım Projesi

**Doküman:** `~/Desktop/EMRE TELYAR.docx`
**Bu dosya:** yapılacak düzenlemelerin kaydı. Karar burada, uygulama Mert'te.
**Tarih:** 2026-08-25

---

## Neden bu düzenleme doğdu

Mert'in tespiti: *"Ek hizmetler yetersiz ve karışık geldi bana, fiyatı
artırmak için daha fazla ek hizmet üretmeliyiz gibi düşünüyorum. Ayrıca
bunlara da ek bedeller yazmak lazım gibi."*

**Clara'nın itirazı ve kabul edilen kısmı:** ek hizmet *üretilerek*
çoğaltılmaz, kapsamdan *ayrılarak* bulunur. Uydurulmuş kalem müşteriye
şişirme gibi görünür ve baz paketin güvenilirliğini düşürür. Aşağıdaki
kalemler ya bazda olup ayrılabilir olanlar ya da referans sistemde
ölçülmüş gerçek işlevlerdir.

---

## KARAR 1 — Bazdan ek hizmete taşınacak

### İndirim ve Kampanya Yönetimi
**Şu an:** baz pakette, admin panel modülü olarak listeli
**Yeni yeri:** ek hizmet
**Gerekçe:** Referans sistemde sunucu taraflı doğrulanan tek dinamik fiyat
bileşeni. Sistemin çalışması için zorunlu değil — müşteri indirim kodu
kullanmadan da satış yapar.
**Dokümanda dokunulacak yer:** Bölüm 4.4 (Yönetici Paneli) madde listesinden
çıkarılacak · Bölüm 9 Teklif İçeriği listesinden çıkarılacak · Ek Hizmetler
bölümüne açıklamalı madde eklenecek · Ek Hizmetler fiyat tablosuna satır

---

## KARAR 2 — Ek hizmete YENİ eklenecek

### Değerlendirme ve Yorum Sistemi
**Kaynak:** referans sistemde ölçüldü (müşteri "Hizmeti Değerlendir",
admin `reviews` sekmesi, "Memnuniyet" göstergesi)
**Kapsam:** müşterinin hizmet sonrası puan ve yorum bırakması, yönetici
panelinden yorumların izlenmesi ve yayın kontrolü, memnuniyet göstergesi
**Not:** Şu an teklifte **hiç yok** — ne bazda ne ek hizmette. Yeni kalem.
**Dokümanda dokunulacak yer:** Bölüm 4.4'e girmeyecek (ek hizmet) ·
Ek Hizmetler bölümüne açıklamalı madde · fiyat tablosuna satır

### Muhasebe / Fatura Entegrasyonu
**Kaynak:** Mert'in kararı — referansta yok, iş modeline uyuyor
**Kapsam:** e-fatura / e-arşiv entegrasyonu, satış ve tahsilat kayıtlarının
muhasebe sistemine aktarılması
⚠️ **AÇIK:** hangi muhasebe sistemi (Logo, Mikro, Paraşüt, Netsis…)?
Teklifte sağlayıcı adı verilecekse belirlenmeli; verilmeyecekse
"anlaşmalı e-fatura sağlayıcısı" denir. **Mert'e sorulacak.**
**Dokümanda dokunulacak yer:** Ek Hizmetler bölümü + fiyat tablosu

### Özel Gün Anma Ziyareti Modülü
**Kaynak:** referansın en üst paketinde var (Hatıra, 11.500 ₺/ay —
"belirlediğiniz 2 özel günde anma ziyareti")
**Kapsam:** vefat yıldönümü, doğum günü, dini bayram arifesi gibi tarihlerin
tanımlanması, ziyaretin otomatik planlanması, hatırlatma bildirimi,
ziyaret sonrası özel rapor
**Not:** Şu an müşteri panelinde "Özel Anma Günleri" alanı var ama
**modül olarak ayrı değil.** Ayrıştırılacak.
**Dokümanda dokunulacak yer:** Ek Hizmetler bölümü + fiyat tablosu
⚠️ Bölüm 4.1 ve 4.2'de "özel anma günleri" geçiyor — çelişki olmaması için
oradaki ifadeler gözden geçirilmeli (veri girişi bazda, otomatik planlama
ek hizmette).

### Çoklu Dil Desteği
**Kaynak:** Clara önerisi, Mert onayladı
**Gerekçe:** yurt dışında yaşayan vatandaş bu işin **ana hedef kitlesi** —
teklifin Amaç bölümü bunu zaten söylüyor. Almanca/İngilizce arayüz gerçek
ihtiyaç.
**Kapsam:** arayüz metinlerinin çoklu dil yönetimi, yönetici panelinden dil
ekleme, içeriklerin dile göre tanımlanması
**Dokümanda dokunulacak yer:** Ek Hizmetler bölümü + fiyat tablosu

---

## KARAR 3 — Ek hizmete GİRMEYECEK

### Excel / Detaylı Raporlama
**Mert:** *"Excel detaylı raporlamayı çıkartalım, ek hizmette olmaz bence o."*
**Sonuç:** Bazda kalır. Şu an Bölüm 4.4'te "Finansal Raporlama: … Excel
formatında dışa aktarım" olarak geçiyor — **değişiklik yok, olduğu gibi
kalacak.**

### Kurumsal / Toplu Hesap
**Mert:** *"Kurumsala gerek yok."*
**Sonuç:** Hiç eklenmeyecek. Clara önerisiydi, reddedildi.

### Müşteri Mobil Uygulaması · Görsel Peyzaj Tasarım Aracı
**Durum:** Clara bazdan çıkarmayı önerdi (seçenek A), Mert bu ikisini
**seçmedi** — bazda kalıyorlar.
**Sonuç:** değişiklik yok.

---

## Düzenleme sonrası ek hizmet listesi — 8 kalem

Mevcut 4:
1. Mezar Taşı Satış Hattı
2. Dış Tedarikçi (Usta) Ağı Modülü
3. Saha Uygulaması Çevrimdışı Çalışma
4. PayTR Harici Sanal POS Entegrasyonu

Yeni 4:
5. İndirim ve Kampanya Yönetimi *(bazdan taşındı)*
6. Değerlendirme ve Yorum Sistemi *(yeni)*
7. Muhasebe / Fatura Entegrasyonu *(yeni)*
8. Özel Gün Anma Ziyareti Modülü *(yeni)*
9. Çoklu Dil Desteği *(yeni)*

→ **Toplam 9 kalem.**

---

## Açık kalan — Mert'in kararı bekleniyor

**1 · Fiyatlar.** Dokuz kalemin her birine bedel yazılacak. Mert kendi mi
koyacak, yoksa Clara iş yüküne dayalı öneri mi getirecek — **sorulmadı,
cevap gelmedi.**

**2 · Muhasebe entegrasyonunda sağlayıcı adı** verilecek mi
(Logo/Mikro/Paraşüt vb.), yoksa genel mi bırakılacak.

**3 · Özel anma günü çelişkisi.** Bölüm 4.1/4.2'de bu alan bazda görünüyor;
modül ek hizmete alınınca ifadeler ayrıştırılmalı.

---

## Dokümanda dokunulacak yerlerin listesi

**Bölüm 4.4 — Yönetici Paneli:** "İndirim Kodu Yönetimi" maddesi çıkarılacak

**Bölüm 9.1 — Teklif İçeriği:** listeden "İndirim ve kampanya yönetimi"
çıkarılacak *(şu an "Fiyat ve katalog yönetimi" var — indirim ayrı satır
değil, kontrol edilmeli)*

**Bölüm 9.2 — Ek Hizmetler (açıklamalı):** beş yeni açıklamalı madde

**Bölüm 9.6 — Ek Hizmetler tablosu:** dört satırdan dokuz satıra, her satıra
fiyat

**Bölüm 4.1 / 4.2:** özel anma günü ifadeleri gözden geçirilecek
