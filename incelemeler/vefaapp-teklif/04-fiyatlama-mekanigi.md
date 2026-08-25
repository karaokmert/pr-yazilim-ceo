# Fiyatlama ve konfigüratör mekaniği — ÖLÇÜLDÜ (bundle'dan, 2026-08-25)

## Paketler — koda SABİT gömülü, admin'den yönetilmiyor

```
Vefa Paketi    aylık 2.950 ₺  · yıllık 30.000 ₺  (yıllık ay eşdeğeri 2.500 ₺)
               ayda 1 ziyaret · Fotoğraflı rapor
Huzur Paketi   aylık 4.400 ₺  · yıllık 43.920 ₺  (ay eşdeğeri 3.660 ₺)
               ayda 1 ziyaret · Videolu rapor
Hatıra Paketi  aylık 11.500 ₺ · yıllık 114.000 ₺ (ay eşdeğeri 9.500 ₺)
               ayda 2 ziyaret · Tam kapsamlı video raporu
```

Her paketin alanları: `monthlyPrice` · `yearlyTotal` · `yearlyEquivalent` ·
`schedule` · `visitsPerMonth` · `reportType` · `features[]` · `bonusFeatures[]`

⚠️ **"%16 indirim" hesaplanmıyor — sabit yazılmış.** Yıllık tutar ayrı bir alan
olarak gömülü (`yearlyTotal`), aylık × 12'den türetilmiyor. Ekranda gösterilen
"%16 İndirim" etiketi statik bir metin.

**Doğrulama:** Vefa aylık 2.950 × 12 = 35.400 ₺, yıllık 30.000 ₺ →
gerçek indirim ~%15,3. Huzur: 4.400 × 12 = 52.800, yıllık 43.920 →
~%16,8. Hatıra: 11.500 × 12 = 138.000, yıllık 114.000 → ~%17,4.
Yani "%16'ya varan" ifadesi üç paketin ortalamasını temsil eden pazarlama dili.

## Peyzaj / bitki kataloğu — koda SABİT gömülü (9 bitki)

```
Lavanta              300 ₺
Sedum (Damkoruğu)    220 ₺
Yayılıcı Kekik       240 ₺
Biberiye             275 ₺
Zambak               400 ₺
Adaçayı              260 ₺
Lantana              285 ₺
Bodur Defne          450 ₺
```
Her kayıt: `id` · `name` · `price` · `color` · `fill` · `img` (PNG görseli)

## Mermer / ek hizmet farkları — koda SABİT gömülü

```
Siyah Granit Farkı   600 ₺
Gri Mermer Farkı     300 ₺
Özel Mermer Cilası   300 ₺   "Mermerin ömrünü uzatır ve ilk günkü gibi parlatır"
Mermer Kuşluk        250 ₺   "Kuşların su içebileceği şık bir oyuk eklenir"
```

## Tasarım atölyesi — nasıl çalışıyor

**Tarayıcıda, sunucuya gitmeden:**
1. Mezar görseli üzerinde **baştaşına tıklayıp isim ve tarih yazılıyor**
   (textarea placeholder "TIKLA & İSİM YAZ", input "1900 - 20XX")
2. **Mermer rengi seçiliyor** → varsa fiyat farkı eklenir
3. **Hazır şablon seçilebiliyor** ("ŞABLONLAR" butonu)
4. **Toprak alanına tıklanarak bitki ekleniyor** — 8 yerleştirme noktası (+)
5. **"Peyzaj Fiyat Özeti"** canlı güncelleniyor: *"Toplam Peyzaj Bedeli +X ₺"*
6. Not: *"Bu tutar, seçeceğiniz pakete eklenecektir"*
7. "PAKET SEÇİMİNE DEVAM ET" → seçim sipariş akışına taşınıyor

⚠️ Görseller statik PNG (`/images/lavanta.png` gibi) — gerçek 3D değil,
**2D katmanlı görsel kompozisyon.** Teklifte "3D" demek yanlış olur;
doğrusu "görsel konfigüratör" ya da "interaktif tasarım aracı".

## Ödeme akışı — ölçülen alanlar

Siparişte sunucuya giden veri (`siparisData`):
`musteriAdi` · `musteriEmail` · `musteriTelefon` · **`toplamFiyat`** ·
`discountCode` · `discountPercent` · `priceBeforeDiscount`

**İndirim kodu sunucuda doğrulanıyor:** `/api/indirim-kodu-dogrula` →
`{kod, yuzde}` döner. Yani indirim oranı **admin tanımlı ve sunucu taraflı** —
tek dinamik fiyat bileşeni bu.

**Taksit:** `/api/odeme/taksit-sorgula` → `installmentNumber` ve `toplamTutar`
listesi döner; kullanıcı taksit seçince toplam değişiyor.

**3D Secure:** ödeme başlatılınca `threeDUrl` dönüyor, kullanıcı yönlendiriliyor.
Kart alanları formda toplanıyor (`Kart Numarası`, `cvc`).

---

## Teklif için sonuç — kritik ayrım

**Referans sistemde fiyat yönetimi YOK.** Paketler, bitki fiyatları, mermer
farkları, yıllık tutarlar — hepsi kaynak koda gömülü. Fiyat değişikliği için
**kod değiştirip yeniden yayınlamak** gerekiyor. Admin panelinde paket/fiyat
yönetimi sekmesi yok (10 sekme sayıldı, biri değil).

Dinamik olan tek şey: **indirim kodları** (sunucuda doğrulanıyor) ve
**mezar taşı fiyatları** (ustanın kendi girdiği, `partner_designs`).

**Bu bizim için hem fırsat hem karar noktası:**

**Fırsat** — "fiyatlarınızı panelden yönetin, kod değişikliği gerekmez"
somut bir üstünlük. Mevsimsel fiyat, kampanya, bölgesel farklılaştırma
mümkün olur.

**Karar** — fiyat yönetimi modülü kapsama girerse iş artar: paket CRUD,
bitki/hizmet kataloğu CRUD, fiyat geçmişi (abonelikteki müşterinin fiyatı
değişmemeli — bu ayrı bir kural), yıllık/aylık oran yönetimi.

⚠️ **Abonelikte fiyat sabitleme sorusu:** referans sistemde fiyat kodda sabit
olduğu için bu problem hiç doğmamış. Bizde fiyat panelden yönetilirse,
"abone olmuş müşterinin fiyatı zam görünce ne olacak" sorusu doğar ve
cevabı sözleşmeye yazılmalı. Bu teklif yazarken konuşulacak bir madde.
