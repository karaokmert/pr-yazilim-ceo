# Wupdoc (= WD) — durum

**ClickUp:** folder `138093486` · Task List `234174168` · Bugfix `234174173` · Planning `901524539028` · Proje Planlama Listesi `901506485056`
**Prefix:** WD / WDWS (web sitesi) / WDCP (klinik paneli) / WDAP (admin) / WDAPP (mobil) / WDPAT (hasta) / WDSAL (satış)
**Ne:** Sağlık turizmi doktor-klinik dizin platformu. Hasta doktorları puan/yorum bazında sıralar, talep ve randevu oluşturur. Dört panel.
**Kim:** Uğur (backend) · Tarık (frontend) · Buse (UI) · Safae (içerik/satış operasyonu) · Umutcan · Yiğit

⚠️ **Mert'in tablosundaki "WD" bu projedir** — ayrı bir proje değil. "Top Doctor"
ifadesi buradan geliyor.

⚠️ Ölçüm 2026-09-02, ClickUp taraması.

---

## Ne bitti

**Geliştirme tarafında son kapananlar:** PRY-17631 (Content Yönetimi) · PRY-17633
(Onboarding Yönetimi) · PRY-17634 (First Login İçerik Yönetimi) · PRY-17635 (Doc
Chat Upgrade Metin Yönetimi) · PRY-17784 (Chatwoot Contact Integration) ·
PRY-17860 (V2 Apps Test) · PRY-16929 (Klinik Otomasyonu Webhook Girişi) ·
PRY-16790 (Domain Alınması) · PRY-16787 (Yan Siteler Blog Otomasyonu) · PRY-16801
(Performans Marketing Reklamları)

⚠️ **Kapanan iş hacminin çoğu geliştirme değil operasyon.** Safae'nin haftalık
tekrar eden işleri her hafta yeni ID ile yeniden açılıyor: WDSAL Clinics/Doctors
Entries, WDSAL Follow-up Management, WDPAT Patients Follow-up, WDWS Health Center
& WhatsNews Blog Entries, WDWS Yan Siteler Blog Entries. Son turda buna Dynamic
List Update, Emails Test, Sales Strategy Conversation eklenmiş.

⚠️ **Statü hijyeni:** çoğu task'ta `date_closed` boş. Ekip "completed" statüsüne
çekiyor ama ClickUp'ın kapatma alanı dolmuyor — "ne bitti" sorusu buradan
güvenilir okunmuyor.

---

## Şu an açık

**Ek Hizmetler (Sprint 7'nin ana konusu):**
- **PRY-17888 — WD - Ek Hizmetler UI** (ui, Buse). Açıklaması: *"abonelik
  paketlerinin dışında tek tek satın alınabilecek **beş ek hizmetin (ek kategori,
  aramada öne çıkma, profil işareti, anasayfa listeleme, teklif öne çıkma)**
  satın alma deneyimi tasarlanacak."*
- Dört alt parça, **dördü de Open ve atanmamış:** PRY-17890 (Parça 1: Ek Hizmetler
  Paneli) · PRY-17891 (Parça 2: Hizmet Detayı ve Satın Alma) · PRY-17892 (Parça 3:
  Dönüş Ekranları ve Bırakma) · PRY-17893 (Parça 4: Faturalar görünümü)

**Ödeme sistemi (üç katman paralel, hepsi lıve-dev):**
- Teklif Ödeme: PRY-16178 (backend, Uğur) · PRY-16177 (ui, Buse) · PRY-16179
  (Planning, atanmamış)
- Aylık Ödeme: PRY-16175 (backend, Uğur) · PRY-16176 (front, Tarık) · PRY-16174
  (ui, Buse)

**Indexing / SEO — aynı sorun DÖRT ayrı kayıtta:** PRY-15830 · PRY-17557 (high,
atanmamış) · PRY-17556 (Safae) · PRY-17520 (Planning, Buse)

**Backend (Uğur):** PRY-15274 (Webhook Management) · PRY-15471 (Klinik yeni mesaj
push) · PRY-13813 (Settings update password) · PRY-17531 (Sunucu Taşıma Prod&Dev,
productıons)

**Diğer:** PRY-17767 (V2 Test, atanmamış) · PRY-17632 (Sözleşme Yönetimi, Umutcan)
· PRY-16791 (Follow Up N8N Final, Yiğit) · PRY-16798 (Yan Siteler Server Issue,
Umutcan) · PRY-16789 (Panel Email Design, Umutcan) · PRY-13200 (Mail Template
revize) · PRY-13198 (Reports) · PRY-15689 (Login SMS Issue, Mert)

---

## Bloke

- **PRY-13916 — WD - Search Yaml İşlemleri.** Uğur'da, backend. Wupdoc'un tek
  blokesi ve folder'da **en son güncellenen task.**

⚠️ Bu haftanın "aramada öne çıkma" ve "liste başı gösterim" başlıkları arama
altyapısına oturuyor — bu blokeyle ilişkisi **kontrol edilmedi**, edilmeli.

---

## Planning'de bekleyen

**Wupdoc - Planning:** PRY-17520 (Indexing Fix, high, Buse) · PRY-17482 (Patients
CRM Test/Not, **urgent**, Umutcan) · PRY-17329 (Özel Doctors List Excel) ·
PRY-16179 (Teklif Ödeme front bacağı) · PRY-15493 (Uygulama Versiyon Servis
Kontrolü) · PRY-15472 (Offer UI Redesign)

**Proje Planlama Listesi (eski backlog, hepsi atanmamış, hiç başlamamış):**
PRY-13202 (CRM Doctor Detail Offer Sayfası, high) · PRY-13119 (Send Code via
WhatsApp, high) · PRY-13062 (Sözleşme Onayları, high) · PRY-13053 (Leads/Enquiries
Excel Export) · PRY-13052 (Zoho Entegrasyonu) · PRY-13040 (Onboarding v2) ·
PRY-13032 (Reviews Treatment Ekleme) · PRY-13029 (Expired Hatası) · PRY-12583
(New Appointment Butonu)

---

## Sprint 7'de yapılacaklarla eşleşme (Uğur BE + Tarık FE — 5 iş)

**Beş başlığın hepsi PRY-17888'in açıklama metninde yaşıyor, ayrı task olarak
HİÇBİRİ açılmamış:**

(tablo yazılmaz:)
- **Teklif Öne Çıkartma** → "teklif öne çıkma" ✓
- **Anasayfa Listeleme** → "anasayfa listeleme" ✓
- **Top Doctor Badge** → "profil işareti" (badge = işaret) — muhtemel
- **Liste Başı Gösterim** → "aramada öne çıkma" — ⚠️ **kesin değil**, "anasayfa
  listeleme" ile karışabilir; kapsam netleştirilmeli
- **Ek Kategori İşlemleri** → "ek kategori" ✓

⚠️ **Uğur'un backend bacağı ClickUp'ta hiç yok.** PRY-17888 metni "iş kuralları ve
backend paralel yürüyor" diyor ama bu beş hizmete ait açılmış tek bir backend
task'ı bulunamadı. Uğur'un açık işlerinin tamamı ödeme sistemi, webhook, push
notification ve sunucu taşıma.

⚠️ **Tarık'ın adı hiçbirinde geçmiyor.** Ana task Buse'de (UI turu), dört alt parça
atanmamış.

⚠️ "Top Doctor" ifadesi ClickUp'ta yalnız **doküman** düzeyinde geçiyor: WDWS -
Top Doctor Infinite Scroll, V.1.5.1 altında — eski ve tamamlanmış bir versiyon.

**Safae'nin Sprint 7 işleri** ("Wupdoc Site 1" / "Site 2") bu adla ClickUp'ta yok;
gerçek karşılığı "WDWS - Yan Siteler Blog Entries" adıyla haftalık yürüyor
(PRY-17789, PRY-17897 en yeniler).
