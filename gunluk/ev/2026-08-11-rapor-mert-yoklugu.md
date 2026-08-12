# Gece raporu — 23:08 → 00:32

> Mert 23:43'te yattı, kontrol Clara'da. Push kapısı devredildi
> ("kararlar sana düşer, push onayı gelirse sen Python'unla yap").

## Sonuç — üç projenin üçü de yayınlandı, kuyruklar sıfır

**GOAT** — 51 commit, iki push
· `f3427c5c..10c27ee5` (50 commit) → Actions: web-admin-v2 #153 ✓ · web-site #186 ✓
· `10c27ee5..3574aa88` (1 commit, sponsor 2FA) → web-sponsor-v2 #81 ✓
· Kuyruk 0. **2FA sızıntısı iki panelde de kapandı.**

**EGELİ** — 9 commit
· `da52590..736378f` → Actions **14/14 yeşil**, PRY-17576 **live dev'de**
· QA üç katman doğruladı: sayım + log içeriği (`Compiled successfully`) + smoke
  (adresleri kaynaktan okuyarak). Kuyruk 0.

**FABRİKA** — 32 commit
· `3c54b57..4666a8a` → kuyruk 0. Bu repoda koruma bypass'ı gerekmedi.
· 00:09'da **reddetmiştim** (24 commit ölçülmemişti); ölçtüler, tanım netleşti:
  26 denetlendi · 5 kayıt dosyası (denetim dışı) · 1 QA'nın kendi commit'i
  (yapısal sınır). Koşul bu tanımla karşılandı.

## Nasıl yapıldı — her push ön kontrollü

Betiğe ön kontrol koydum: branch/HEAD/kuyruk pakete uymuyorsa **iptal**.
· 23:47 Goat — **iptal etti**: kuyruk 47→49 büyümüş, çalışma ağacında FE'nin
  yarım 2FA işi vardı. Push atmadım, sebebini yazdım.
· 00:09 Fabrika — **reddettim**: denetim eksikti.
· Diğer üçünde zemin uyuştu, işlem yapıldı.

Kontrol çalıştı ve iki kez durdurdu. Bugün iki kez yaşanan "başkası çalışırken
git işlemi" kazasının üçüncüsü olmadı.

## Senin onayını bekleyen

**1. Egeli'de iki branch silme** — `pazarlama-v0.1-demo` + `V2607-Sprint80`.
İkisi de doğrulandı, içerikleri main'de. Silme kapısı **açılmadı**, bekliyor.

**2. `PRY-17534` "Deploy İşlemleri"** — statüsü *productions* ama beş yüzeyde
birden iz yok (commit/branch/stash/kod/belge) ve **işlevi bilinmiyor.**
Soru: bu task ne işi kaydediyordu?

**3. Kanon değişikliği** — ölçüm kuralı keskinleştirildi: *"ölçüm kimin işini
denetliyor"*. Bir agent'ın beyanı sınanacaksa o agent'a sordurulmaz.
İtiraz edersen geri dönülür.

**4. `tools/` sahipliği boşluğu** (fabrika) — PQA buldu: *"bugün doğru işlemesi
düzenin değil, iyi niyetin sonucu."*

**5. Düzen sorusu** — aynı dizinde birden fazla agent. Bugün iki kez vurdu
(bir kaza, bir kıl payı). Yarına bıraktın.

**6. `PRY-15871`** — bekleme kararı, "yarın bakalım" dedin.

## Sahada verilen kararlar (itiraz edersen geri dönülür)

· **Egeli:** şema kolonu eklenmeyecek (ölçüm: manuel kaldırmada da iz yok,
  boşluk zaten var — yarım çözüm tam çözümden yanıltıcı). Denetim izi eksiği
  **teknik borç** olarak ayrı task'a yazıldı.
· **Egeli:** atlanan satırlar hata sayacına girmeyecek, rapor üç sayıyı ayırıyor.
· **Goat:** kapsam sapması (9 vs 8) kapatıldı, işlem yok.
· **Goat:** merge commit'inin kimliği düzeltilmedi — geçmişi yeniden yazmak
  kozmetik kazanç için yapısal risk. Yerine iz bırakıldı.

## Öne çıkan iş

**2FA'nın iki yüzü (Goat).** Senin sorduğun soru bir hata ortaya çıkardı:
`IsRequiredTwoFactor` varsayılanı `true` ve panel alanı hiç göndermiyordu —
yani bir yönetici kaydı **her güncellendiğinde zorunluluk sessizce geri
geliyordu.** Hem admin hem sponsor tarafında kapatıldı. FE kopyalamadı,
uyarladı (alan adları farklı; kör kopyalama sessizce çalışmayan form üretirdi).

**`atif-tarama.py` arızası (fabrika).** Script her koşumda index'in tarihini
dört gün geriye alıyordu. PQA kendi buldu, kendini aklamadı (*"karar veren el
benim elim olmamalı"*), PAD **sebebi kaldırdı** — yamalamadı. Kanıt
idempotency ile verildi: iki koşum, iki kez temiz ağaç.

## Sabaha hazır işler

**Goat:** BE iki detay ucu alanı (telepresence gerektirmez) · BE RedirectUrl
(askıda, telepresence) · TE davranış testi (2FA iki panel + tipografi 17 nokta)
· QA log içeriği doğrulaması

**Egeli:** ekip boşta, PA son ölçümde

**Fabrika:** ekip boşta, kuyruk sıfır

## ⚠️ TE için kritik not — kaybolmasın

QA'nın uyarısı: *"Detay uçları alanı dönmediği için form her açılışta ZORUNLU
gösterecek. TE 'kaldırdım ama yine zorunlu görünüyor' derse BU BEKLENEN — hata
değil. Gerçek test: kaldır, kaydet, DB/BE tarafında false kaldı mı."*
Bu not olmasaydı TE doğru çalışan bir işi bug olarak raporlayacaktı.

## ⚠️ Prod notu

Egeli'de prod'da olup main'de olmayan **69 commit** var (prod-only config).
Prod'a çıkışta merge stratejisi **merge commit** olmalı — squash/rebase onları
sessizce siler.
