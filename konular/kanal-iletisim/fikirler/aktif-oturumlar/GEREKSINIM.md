# GEREKSİNİM — Aktif oturumlar defteri + tek Clara kilidi

**Tarih:** 2026-08-13 · **Kaynak:** Mert · **Hedef:** fabrika (kanal betikleri)
**Durum:** gereksinim yazıldı, Mert'in onayı bekleniyor

---

## 1. Ne isteniyor

Mert'in cümlesi:

> *"Her proje için ürettiğimiz folder'a **aktif oturumlar** diye bir alan olmalı.
> Açılan agent oraya açıldığını bilmeli. Kapanışta kanal kapanır. Clara her açılışta
> ve ara ara o dosyanın kanallarla uyumunu kontrol eder.
> **Projede aynı anda birden fazla Clara çalışmasını engellemeliyiz.**"*

İki ayrı şey: **(a)** açık oturumların tek kaydı · **(b)** Clara için tek-oturum kilidi.

## 2. Bugün ne bozuk — ölçüldü

**Aynı rolden birden çok oturum açılıyor ve hiçbir yerde görünmüyor.**
Ölçüm (2026-08-13, `ps`): **6 project-assistant · 4 qa-engineer · 2 FE · 2 BE** açık.

Kutu adı zamandan üretiliyor (`SESSION = %Y%m%d-%H%M`), yani ikinci oturum **yeni kutu**
doğuruyor, eskisi `STATE: OPEN` olarak duruyor. `setup.py`'deki *"kutu zaten var"*
kontrolü (satır 42) **fiilen ölü kod** — isim zamanı taşıdığı için hiç çakışmaz.

**Somut zarar (2026-08-12):** QA *"kutum ...-1246"* dedi; Clara o kutuyu bir dakika önce
arşivlemişti. Adres ölmüştü, mesaj gönderilemedi. Ve tersi: QA açılış hook'undan **eski
merkez adresini** okudu, doğrusunu `ls` ile kendi buldu.

**Merkez seçimi varsayıma dayanıyor:** `setup.py:100` → `sorted(adaylar)[-1]` —
birden çok açık Clara varsa **alfabetik son olanı** seçiyor. *"En yeni doğrudur"*
varsayımı; iki Clara açıksa hangisinin dinlendiği belirsiz.

**Ve `archive-log.json` yalnız KAPANIŞLARI tutuyor** — açılış kaydı hiçbir yerde yok.

## 3. Çözülmüş sayılmayacak şey

⚠️ *"Kutu adresi sabit olsun (rol+proje)"* önerisi **reddedildi** — Mert kesti:
> *"Bu senaryo çalışmaz. 2 QA açılırsa tek kutuya bakarlar. Bu sefer bir mesaj
> ikisine birden gider."*

Doğru: ortak kutuda `.cursor` da çakışır — biri okuyup imleci ilerletince öteki o mesajı
hiç görmez. **Ya çift iş, ya kayıp iş.**

## 4. İstenen davranış

**A · Aktif oturumlar defteri** — `~/.pr-kanal/{proje}/AKTIF-OTURUMLAR.json`

- Agent açılınca kendini **yazar** (rol · kutu yolu · PID · başlangıç zamanı)
- Kapanışta (arşivleme) kendini **siler**
- Clara her açılışta ve ara ara **defter ↔ gerçek kutular** uyumunu kontrol eder:
  - defterde var ama kutusu yok → **ölü kayıt**, temizlenir
  - kutu var ama defterde yok → **kaçak oturum**, deftere eklenir ya da sorulur
  - defterde var, süreç ölmüş → **artık**, kapatılır

**B · Tek Clara kilidi**

Bir projede aynı anda **yalnız bir Clara** çalışır. İkinci Clara açılırsa:
- Defterde açık Clara görürse **uyarır ve durur** — kendiliğinden ikinci merkez kurmaz
- Kullanıcıya sorar: *"bu projede zaten açık bir Clara var (kutu, başlangıç saati).
  Onu devralayım mı, yoksa o kapansın mı?"*

**Neden:** iki Clara varsa agent'lar **hangi merkeze yazacağını bilemez** ve
`sorted()[-1]` varsayımı sessizce birini seçer. Bugün bu fiilen yaşandı.

## 5. Ölçülebilir kabul kriteri

- İki aynı rol açıldığında defterde **iki ayrı satır** görünür (kutuları ayrı kalır)
- İkinci Clara açılınca **kutu kurmaz**, uyarır
- Clara açılışta defteri okur ve **tutarsızlığı raporlar** (ölü kayıt / kaçak oturum)
- Ani kapanmada defter bozulmaz — bir sonraki Clara **artığı görür ve temizler**

## 6. Kapsam dışı

- Kutu adresinin sabitlenmesi (reddedildi, yukarıda)
- İş dağıtımı / kilitleme (iki QA'ya aynı iş gitmesin sorunu ayrı — bu defter onu
  **görünür** kılar ama çözmez)

---

> ⚠️ Bu bir **gereksinim**, kanon değil. Kanonu fabrika üretir (`setup.py` ·
> `archive.py` · açılış hook'u). Clara oraya onaysız yazamaz.
