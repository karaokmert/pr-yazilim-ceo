# Egeli — durum

**ClickUp:** folder `90156234741` · Task List `901524526603` · Bugfix `901524526497` · Planning `901524533638`
**Prefix:** EO / EOAP / EO-APP · **Kim:** Mert
**Ne:** İSG (iş sağlığı ve güvenliği) yönetim sistemi. Firma, uzman, personel, sertifika, evrak, muhasebe-fatura modülleri. Web + mobil.

⚠️ Ölçüm 2026-09-02, ClickUp taraması.

---

## Ne bitti

**Son dönem odağı:** toplu Excel işlemleri + toplu uzman atama + sertifika revizeleri.
Kapananlar: PRY-16160 (Toplu Uzman Atama) · PRY-16130 (Excel export) · PRY-16125
(Eğitim Statüleri) · PRY-16102/16060 (Toplu Uzman Atama geliştirmeleri) · PRY-16073
(Şube-Merkez gösterimi) · PRY-16069 (Cari Kodu) · PRY-16051 (Toplu Excel
tutarlılık) · PRY-15772/15771/15764 (sertifika revizeleri)

⚠️ **Kapanış toplu yapılıyor** — 2026-08-16'da 15+ task tek anda, öncesinde
2026-08-09'da benzer bir dalga. Yani tek tek değil topluca kapatılıyor.

---

## Şu an açık

**Kod tarafında yürüyen görünür tek iş:**
- **PRY-15871 — EgeliAP Excel ile yüklemede sütun format hatası** (full stack, Mert)
- PRY-15855 — [UI] Dashboard Revizesi, metrikler ve uzman aktivitesi (lıve-dev,
  high, atanmamış)
- PRY-15768 — Eğitim eklerken video ve test olmadan ekleyebilelim (lıve-dev, Mert)

**Açık işin neredeyse tamamı Planning listesinde "customer" statüsünde** — 51
kalem, hepsi 2026-08-30 civarı güncellenmiş. ⚠️ Bunlar kod işi değil, **henüz iş
emrine dönmemiş müşteri talep havuzu.** Şemsiye task'lar altında gruplanmış:

- **Muhasebe & Fatura** (PRY-18073 şemsiye): firma fatura döngüsü, fatura notları,
  faturası kesilmeyen cari ünvanı, bedelsiz firmalar, aylık/3 aylık/yıllık yapı
- **Firma İşlemleri** (PRY-18071): carisi olmayan firmalar, firma status, toplu
  uzman atamasını kaldırma, toplu firma indir, firmaya verilen hizmet tanımı
- **Uzman & Atama** (PRY-18074): İK uzman yönetimi, uzman bölge yapısı, uzman
  dashboard dakika hesabı, ISG Katip atama durumu/onayı, tehlike sınıfı
- **Personel** (PRY-18075): toplu yüklemede şirket değişmiyor, pasife alma,
  belge yükleme, SGK sicil DETSIS, tekil personel ekle, kimlik fotoğrafıyla
  personel oluşturma, SMS şifre yeniden gönder
- **Sertifika & Evrak** (PRY-18077): süre geçerliliği, dosya yükleme, eskiyen
  evraklar, uygunsuzluk ekle, ISG hizmet raporu
- **Rapor & Dashboard** (PRY-18072): rapor altyapısı, yeni cariler, atama
  bekleyenler, şirket panelinde şube/rapor görüntüleme
- **Entegrasyon:** PRY-18068 (CRM & Mikro Entegrasyonu) · PRY-18070 (Yeni Firma
  Atama & Muhasebe) · PRY-17452 (Proje Alt Yapı Düzeni) · PRY-17453 (Expert Panel
  Sorunu) · PRY-18076/16251/16250 (Medivita senkronizasyonu)

---

## Bloke

Yok.

---

## Sprint 7'de yapılacaklarla eşleşme (Mert — Pzt+Sal)

**"Egeli İşlemleri"** → ClickUp'ta bu isimle task YOK. Bu bir haftalık plan
başlığı; karşılığı folder'ın kendisi. Kod tarafında eşleşen tek aktif iş
PRY-15871 (Excel sütun format hatası).

⚠️ **Asıl soru şu:** 51 kalemlik müşteri talep havuzu duruyor ve hiçbiri iş
emrine dönmemiş. "Egeli İşlemleri" bu havuzdan seçim yapmak mı, yoksa başka bir
şey mi — netleşmedi.
