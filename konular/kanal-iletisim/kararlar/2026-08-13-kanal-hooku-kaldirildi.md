# Kanal açılış hook'u kaldırıldı — geçici, yeni yöntem gelecek

**Tarih:** 2026-08-13 · **Karar:** Mert · **Uygulayan:** Mert (settings.json kendi düzenledi)
**Durum:** yürürlükte · ⚠️ **geçici** — *"sonra başka bir yöntemle geçiş yapacağız"*

## Karar

`~/.claude/settings.json` → `SessionStart` dizisinden `kanal-acilis.py` çağrısı çıkarıldı.

Mert'in cümlesi: *"Hiçbir agent açılışta kanal kurma hook'unu çalıştırmasın.
`preload-skills.py` tek başına kalsın. **Sen dahil herkes** — hook ile kanal
kurulumunu kaldıralım."*

## Neden

Kanal düzeni **bozuk** olduğu ölçüldü ve yeniden tasarlanacak. Bozuk bir düzeni
her oturumda otomatik kurmak, arızayı çoğaltıyor.

**Ölçülen arızalar:**
- Kutu adı **zamandan** üretiliyor (`SESSION=%Y%m%d-%H%M`) → aynı rol ikinci kez
  açılınca **yeni kutu** doğuyor, eskisi `OPEN` kalıyor.
  Ölçüldü: `qa-engineer-20260812-1246` + `-2127` (aynı rol, iki adres)
- `setup.py:42` *"kutu zaten var"* kontrolü **ölü kod** — isim zamanı taşıdığı için
  hiç çakışmaz
- Merkez seçimi varsayıma dayanıyor: `sorted(adaylar)[-1]` — iki Clara açıksa
  hangisinin dinlendiği belirsiz
- **Somut zarar (2026-08-12):** QA *"kutum ...-1246"* dedi, Clara o kutuyu bir dakika
  önce arşivlemişti; adres ölmüştü. Ve QA hook'tan **eski merkez adresini** okudu.

## Ne değişti / ne değişmedi

**Kesildi:** agent'lar (ve Clara) açılışta kanal talimatı **almıyor.**
**Duruyor:** `~/.claude/hooks/kanal-acilis.py` (12.8 KB) — silinmedi, çağrılmıyor.
**Dokunulmadı:** Git özeti hook'u · `PostCompact` · `Notification` · `Stop`
**Zaten temizdi:** `preload-skills.py` — içindeki iki "kanal" kelimesi yorum satırı.

## ⚠️ Bilinen bedel

Hook'un kendi gerekçesi şunu söylüyordu:
> *"Kanal protokolü OY ve Websitesi agent'larının kanonunda HİÇ YOK — ölçüldü
> 2026-08-11, plugin cache'inde sıfır eşleşme. Bu boşluk bugüne kadar **elle**
> kapatılıyordu: Clara her agent için handoff yazıp adresi veriyordu."*

Yani **o yamaya geri dönüldü:** yeni düzen kurulana kadar bir yönetim oturumunda
agent'lara kanal adresini **Clara elle** verecek. Ve Clara bunu bir kez atladı
(2026-08-12, QA'nın kutusu).

## Sıradaki — açık gereksinim

`fikirler/aktif-oturumlar/GEREKSINIM.md` — aktif oturumlar defteri + tek Clara kilidi.
Mert'in kararları oraya işlendi:
- İkinci QA **kapasite kararıdır ve Mert verir** (*"bir QA daha açtım"* der, Clara
  kaynağı bilir ve işi dağıtır)
- Sabit kutu adresi **reddedildi** (*"2 QA açılırsa tek kutuya bakarlar, bir mesaj
  ikisine birden gider"*)

**Henüz karara bağlanmadı:** Clara kilidi sert mi yumuşak mı · defteri kim yazar.
