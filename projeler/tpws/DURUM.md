# TPWS (Truck Parts) — durum

**ClickUp:** folder `901516509839` (Keba ERP ile AYNI folder) · Task List `901524074948` · Bugfix `901524074949`
**Prefix:** TPWS · **Mert'in tablosunda:** "TP"
**Ne:** Shopify tabanlı e-ticaret — kamyon/araç yedek parça satış sitesi (storefront).
**Kim:** Didem

⚠️ **Keba folder'ının altında yürüyor** — ayrı folder açılmadı, ayrı ürün ama aynı
yerde. Mert kararı (2026-09-02): yeni TP task'ları da bu listeye açılacak.

⚠️ Ölçüm 2026-09-02, ClickUp taraması.

---

## Ne bitti

**Site görsel ve işlevsel olarak bitmiş.** Kapanan iş iki dalga:
- "Suitable for" sekmesi (PRY-17639, 17724, 17729, 17730, 17681)
- Stok doğruluğu (PRY-17638, 17665, 17491)
- Renk / logo / görsel sistemi (PRY-17504, 17503, 17696, 17698)
- Mobil düzen (PRY-17667, 17682, 17566)
- Üyelik sistemi (PRY-17546)
- Kampanya alanı (PRY-17733 kaydırmalı şerit, PRY-17732 açık zemin)
- PRY-17721 — İletişim formu mesaj kaybı [ÇÖZÜLDÜ, commit c799a41]

**Şimdi arama / parça bulucu motoruna geçilmiş** — açık işlerin ağırlık merkezi orada.

---

## Şu an açık

**Parça bulucu / arama (en sıcak damar):**
- **PRY-18088** — Arama sayfasında SAYFALAMA YOK, 308 ürüne erişilemiyor + sonuç
  alakası **(ACİL, high)** — lıve-dev
- **PRY-18090** — Marka + parça tipi + parça sistemi kademeleri bağlansın, 5 kademe
  de çalışsın **(high)** — lıve-dev
- PRY-18089 — Ekipman tipi kademesi filtreye bağlansın (lıve-dev)
- PRY-18083 — Segment filtresinde sıralama: o segmente özgü ürünler önce (lıve-dev)
- PRY-17818 — Segment filtresi ürün sorgusuna bağlansın (lıve-dev)
- PRY-17819 — **Segment etiketi olmayan 413 ürün:** etiket girişi + "evrensel parça"
  kararı bekliyor (planning)

**Mobil ve yayın arızaları:**
- PRY-18079 — Mobil görünümde arama çubuğu yok (planning)
- PRY-18087 — Aynı iş, ikinci kayıt, **pause**'da ⚠️ kopya
- PRY-18085 — Panel ve site yayın dosyalarında aynı tetikleme arızası (planning)
- PRY-18086 — İletişim formu ayarları tanımsız: form çalışmıyor, tanımlanınca
  yeniden yayın şart (planning)

**Shopify bağlantısı ve canlıya geçiş ("creative"):**
- PRY-17515 — Storefront'u gerçek Shopify mağazasına bağla
- PRY-17547 — Favoriler (favoriye ekleme + profilde Favorilerim)
- PRY-17567 — Shopify panel: Clutches bağlantısı + menü içerik düzeltmeleri
- PRY-17660 — Tidio canlı sohbet (canlıya geçişte aktifleştirilecek)

**Teknik borç:** PRY-17731 — Storefront ölçü değerleri tasarım belirteçlerine
bağlansın (25 dosya / 242 kullanım), atanmamış

---

## Bloke

TPWS tarafında bloke yok. (Aynı folder'daki üç bloke ERP tarafına ait —
`projeler/keba-erp/DURUM.md`.)

---

## Sprint 7'de yapılacaklarla eşleşme

Tabloda TP altında üç iş var ama **hiçbirinin ClickUp'ta karşılığı yok:**
- **TP - Mobil Proje Üretimi** (Tarık, Çar) → YOK
- **TP - GEO & SEO İşlemleri** (Didem, Çar) → YOK
- **TP - Mobil APP** (Didem, Per/Cum/Pzt) → YOK
- **KebaTP - Canlı Yayın İşlemleri** (Didem, Cum) → bu adla YOK

⚠️ **Kişi uyuşmazlığı:** TPWS'deki işlerin **hepsi Didem'de**, Tarık'ın burada tek
bir task'ı yok. Tabloda "TP - Mobil Proje Üretimi" Tarık'ta yazıyor. TPWS'de
mobil geliştirme işi de yok — burası Shopify storefront.

⚠️ **Kapsam uyuşmazlığı:** Bu hafta Didem'e TP'de mobil ve SEO işi verilmiş, ama
TPWS'de açık duran şey arama motoru — ve iki tanesi high, biri ACİL etiketli.
Bu işler bu haftaya girmiyor mu, yoksa yeni işler onların üstüne mi geliyor —
**netleşmedi.**
