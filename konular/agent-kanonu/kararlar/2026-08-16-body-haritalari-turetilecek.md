# Karar — body'deki "iş → skill" haritaları türetilecek

**Tarih:** 2026-08-16 18:33 · **Karar mercii:** Clara (ölçümle)
**Yetki:** Mert, 18:31 — *"sorular ölçümle yanıtlanabilirse sen yönlendir, kritik
olanları bana getir."*

## Soru

Mert'in kuralı (2026-08-14): **body skill saymaz, isim vermez.** Gerekçesi: sayı
bayatlar, isim listesi **çift kaynak** olur (body ↔ omurga cascade borcu).

Ama dokuz body'de `X işi → \`skill\`` haritaları var. Kalksın mı, kalsın mı?

## Ölçüm

**PCA (2026-08-16):** 263 skill adı kullanımı, **65'i yönlendirme**, bunların **62'si
çift kaynak.** BE'de harita omurganın **tam alt kümesi** — sıfır özgün bilgi. Dokuz
rolde aynı desen; hiçbirinde body omurgadan geniş değil.

**Clara doğruladı** (`backend/SKILL.md:10-33` ↔ `backend-developer.md`):

| | |
|---|---|
| Omurga çantası | **21** eşleme |
| Body haritası | 17 (16 ortak + `backend` kendi adı) |
| Omurgada var, body'de **hiç yok** | **5** |

`api-project` · `code-quality` · `dev-environment` · `gosterim-formatlari` ·
`tasarim-prensipleri` — beşi de body'nin tamamında backtick'li **sıfır** kez geçiyor.

## ⚠️ Asıl bulgu — temerrüt zaten düşmüş

PAM'in önermesi: *"Çift kaynak gerçek ama bedeli ölçülmedi. Borç var, temerrüt yok."*

**Yanlış.** Harita **beş eşleme eksik** ve bu eksiklik bugüne kadar fark edilmemiş.
Borç ödenmemiş durumda.

Ve bedeli somut: BE en yüklü rol (21 on-demand skill) ve açılışta gördüğü harita beş
eksik — aralarında `code-quality` ve `tasarim-prensipleri` var, yani **her** backend
işinde geçerli olan ikisi.

PAM bunu kendi **karşı argümanında** zaten yazmıştı; ana argümanı onu görmemişti.

## Karar

**Haritalar SİLİNMEZ ama ELLE YAZILMAZ — omurga çantasından TÜRETİLİR.**

### Üç gerekçe

**1. İşlev gerçek** (PAM'in ikinci gerekçesi, ölçümle çürütülemedi). Body her oturumda
yükleniyor, omurga yalnız açılınca. Harita silinirse agent açılışta hangi işin hangi
skille eşlendiğini görmez — ve **bugünkü işin tamamı tam bu sorunu çözmek içindi.**
Silmek iki işi birbirine iptal ettirir.

**2. Çift kaynak gerçek ve temerrüt düşmüş** (yukarıdaki ölçüm).

**3. İkisi aynı anda ancak türetmeyle çözülür.**

| Seçenek | Sonuç |
|---|---|
| Kalsın | borç sürer, eksilme sessiz devam eder |
| Kalksın | işlev gider, bugünkü iş iptal olur |
| **Türetilsin** | **ikisi de çözülür** |

### Neden "kural netleşsin" seçilmedi

`CLA-FIX-THE-CAUSE`: *"kural netleşsin"* bir **yama** olurdu — çift kaynak yerinde
kalır, üstüne bir tanım eklenir. Sebep kaldırılmıyor, **meşrulaştırılıyor.**

## İş açılmadan önce bilinmesi gerekenler

**a) PA'nın `dev-deploy` eşlemesi GERÇEK TEK KAYNAK** (PCA ölçtü) — omurga çantasında
da preload satırında da yok. Türetme yapılırsa **kaybolur.** Önce omurgaya taşınmalı.

**b) 62 sayısı ÜST SINIR olabilir.** PCA'nın *"neye bakmadım"* 2. maddesi: omurgaların
çanta **dışı** bölümleri okunmadı. QA/DO'daki `prod-deploy` tam o sınıftan çıktı
(preload satırında bulundu). Doğrulanmalı — karar bu sayıya dayanıyor.

**c) Türetme mekaniği belirsiz** — betikle mi (senkron ama araç bakımı doğar), üretim
anında elle mi (PAD kopyalar, PQA eşitliği denetler)? Tasarım kararı, ölçüm ister.

## Sıra

**Bugün açılmıyor.** Kalem 1+2 PAD'de koşuyor, Tip 2 ona eklenecek. Bu iş sırada;
kapsamı PAM hazırlayacak.
