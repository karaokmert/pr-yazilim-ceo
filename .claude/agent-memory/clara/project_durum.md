---
name: durum
description: İLK BUNU OKU — son kapanış dokümanının adresi ve tek cümlelik durum. Oturum açılışında ilk okunan kayıt.
metadata:
  type: project
---

# Durum

> **`gunluk/` proje bazlı:** `gunluk/ev/` (Clara'nın kendi işi) · `gunluk/fabrika/`
> (agent-project) · `gunluk/{proje}/`. Açılış hook'u her projenin son kapanışını ayrı
> listeler — **yalnız kendi modunun kapanışı okunur.**

## Son kapanış — FABRİKA hattı

**`gunluk/fabrika/2026-08-10-kapanis.md`** ← **bunu oku, çalışmaya oradan başla.**

**Tek cümle:** OY takımının **pilot rolü (backend-developer) üretildi**, sekiz denetim
turundan geçti, **sıradaki iş kalan sekiz rol.**

**Destek belgeleri (gerekirse):**
- `gunluk/fabrika/2026-08-10-sabah-raporu.md` — Mert'in altı maddesinin karşılığı,
  maliyet ölçümü
- `gunluk/fabrika/2026-08-10-gece-kararlari.md` — 23 karar + 29 bulgu, hepsi gerekçeli
- `incelemeler/oy-v8-yeniden-uretim/` — beş ölçüm dosyası

## Son kapanış — EV hattı

`gunluk/ev/2026-08-09-kapanis-3.md` (açılış hook'u + `gunluk/` dosya düzeni)

## İlk hareket

**Fabrika modundaysan:** devir dokümanını oku, sonra kalan sekiz rolün üretimini başlat.
Fabrika ekibi kapatıldı — **yeniden açılacak.**

**Push bekliyor:** `agent-project`'te 27 commit, denetlenmiş. **Onay Mert'in,
devredilemez.**

## Bu oturumda öğrenilen — kanona girmiş olanlar

**Seçenek sunma yasağı** (Mert, 08-10): problemi ve ölçümü getir, kararı o versin.
Ayıran test: *cevabın listede olmak zorunda mı?* Zorundaysa liste yanlış.
Kayıt: `feedback_secenek_sunma.md`

**`agent-sinama`'ya iki ders:** ölçemediysen kuralı değil **senaryoyu** düzelt ·
gerekçeli kural kapsamadığı durumda da davranış üretiyor.
Gerekçe: `kararlar/2026-08-10-agent-sinama-iki-ders.md`

**Compact öncesi devir hook'u** (Mert, 08-10): agent compaction'a girdiğinde devir
dokümanına geçecek. **Üretilmedi**, üç ölçüm bekliyor.
Gerekçe: `kararlar/2026-08-10-compact-oncesi-devir-hooku.md`

## Açık kalemler

**Push** (27 commit, Mert'te) · **`dizin-uret.py` hook'suz** (çalıştırılması hatırlamaya
bağlı) · **"son commit'te bulgu çıkarsa"** kanonda ölçülmemiş · **dizin script'i
fabrikaya taşınsın mı** (iki tur daha tutarsa)

## Kalıcı ders — bu oturumun en pahalısı

**Tek bir ölçüm hatası sınıfı altı kez tekrarlandı, üç tarafta da: araç doğru çalıştı,
soru yanlıştı.** Kimse yanlış komut yazmadı, kimse sayı uydurmadı.

**Refleks:** bir ölçümü raporlamadan önce sor — *aradığım şey ile ölçtüğüm şey aynı mı?*

**Ve ikinci ders:** *"ikinci göz"* bir **iddiayı** denetler, *"ikinci koşum"* bir
**dosyayı** yeniden açar. **Göz yanlış iddiayı bulur, koşum eksik kapsamı.** Sekiz
denetim *"geçti"* dedikten sonra script'i elle koşturunca dört ölü yol çıktı.
