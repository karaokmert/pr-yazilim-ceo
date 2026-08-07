# Kanal kurulumu — ölçümler

Bu dosya **kanıt** taşır: skill'deki kuralların hangi ölçümden çıktığı. Skill'den atıfla
çağrılır, kendiliğinden yüklenmez.

Ham kayıtlar: `kararlar/2026-08-06-kanal-mimarisi.md` · `gunluk/2026-08-06.md` ·
`gunluk/web-kanal-2/` · `gunluk/web-kanal-deneyi/`

## Tek yazar kuralı — neden veri bütünlüğü kuralı

**Aynı kutuya iki yazar:** 20 blokta **423 yabancı gövde satırı** (iki bağımsız koşum).
Bir mesajın gövde satırları başka mesajın bloğunun içine düştü.

**Tek yazarlı kutu:** karışma **sıfır** — 20 çok satırlı handoff, ve dört kutuya
eşzamanlı 60 mesaj.

**Mekanik sebep:** POSIX `>>` atomiklik garantisi tek bir `write()` çağrısı ve `PIPE_BUF`
sınırında geçerli — bu makinede **512 bayt.** Bir handoff bunun onlarca katı olduğu için
birden fazla çağrıya bölünüyor. `flock` macOS'ta **yok**, yani kilitle çözülmüyor.

## Monitör — üç ayrı hata ölçüldü

**`Bash` içinde `eval 'tail -F ...'`:** süreç üretiyor, **bildirim üretmiyor.** Süreç
listesinde canlı görünüyor. Ölçülen vaka: bir agent böyle kurdu, *"kurdum, ölçtüm,
canlıydı"* dedi — ve mesajlar ona hiç düşmedi.

**Süreç ağacı ayırt etmiyor:** `Monitor` aracı da arka planda `zsh -c ... eval` kalıbı
kullanıyor. Ayıran şey **task kaydı.**

**`TaskList` boş dönüyor, `TaskOutput` doğru:** ikisi ayrı defter. `TaskList` planlama
görevlerini listeliyor, arka plan süreçlerini değil. Bir ölçümde `Monitor` task ID verdi
ama `TaskList` boş döndü — çelişki değil, yanlış araç.

**Filtresiz `tail`:** ~30 satırlık mesaj **30 olay** üretti, monitör SIGTERM aldı
(exit 143). Filtreli hâli 90 satırı **1 olaya** indirdi.

**`2>/dev/null` ile hata deseni ulaşmıyor:** stderr olay akışına girmiyor. `2>&1` ile
merge edilmezse `tail:`, `No such file` gibi desenler filtreye hiç ulaşmıyor — yani
yarısını uygulayan kendini korumuş sanıyor.

**Paralel monitör:** beş monitör aynı anda sorunsuz çalıştı, olaylar karışmadı.

**Monitör ölümü bildiriliyor:** kendini `SIGTERM` ile öldüren monitör
`status: failed, exit 144` bildirimi üretti; normal bitenler `completed`. Belgede yok,
ölçümle bulundu.

**Bildirim ≠ mesaj:** araç 200 ms içindeki satırları tek bildirimde gruplıyor. Ölçüldü:
iki mesaj 1 saniye arayla yazıldı → mesaj 2, olay 2, **bildirim 1.**

## `tail -F` glob'u sonradan açılan dosyayı yakalamıyor

`tail -n 0 -F dizin/*.md` ile izlenirken açılıştan sonra oluşan dosya **hiç görünmedi** —
glob açılışta bir kez genişliyor. İhlali **sessiz.**

`find -newer` ile dizin taraması yeni dosyayı buluyor.

## inode değişimi — ölmüyor, kayıp penceresi bırakıyor

İlk ölçüm *"silinen dosya `tail -F`'i sessizce öldürüyor"* dedi (inode
50831505 → 50831506, dinleyici ölü kaldı).

İkinci ölçüm düzeltti: `-F` yeniden açmayı **deniyor** — üçüncü satır yeni dosyadan
geldi. Ama açma anıyla eski dosyaya yazılmış satırlar arasında **kayıp penceresi** kalıyor.
Yani `-F` bir güvenlik ağı, izin değil.

**`Read` bu tuzağa bağışık:** inode'u değişmiş dosya `Read` ile açıldı ve bulundu. Tuzak
yalnız izleyiciyi etkiliyor.

## Açılış kaybı — sahada ölçüldü

Bir mesaj 18:12'de yazıldı, monitör 18:20'de kuruldu. **Aradaki sekiz dakikada kanal
sessiz kaldı** ve mesaj elle taşındı. Deneyde iki kez yaşandı.

## Canlılık ölçütü — ÇALIŞMIYOR

`PID + BAŞLANGIÇ` çifti ölü/canlı ayrımını **yapamadı:** `kill -0` taraması bir agent'ı
**ölü** gösterdi, o anda `outbox`'a rapor yazıyordu.

Muhtemel sebep (çıkarım, ölçülmedi): agent'ın `$PPID` ile aldığı PID kendi kabuğunun —
Claude Code oturumunun değil — ve o kabuk her araç çağrısında yeniden doğuyor.

**macOS PID tavanı 4000** ve dönüşümlü, yani PID tek başına yetmiyor. `BAŞLANGIÇ` zorunlu
ama yukarıdaki arıza ikisini birden geçersiz kılıyor.

**Yanlış damga vakası:** iki agent kutularında **başka oturumun damgasını** buldu ve kendi
ölçümüyle düzeltti. Yanlış PID iki yönde de sessizce yanıltıyor — ölü PID'e denk gelen
canlı agent *"kapanmış"*, dönüşümlü PID başka sürece denk gelen kapanmış agent *"canlı"*
görünüyor.

**Denenmemiş aday:** oturum kaydının (transcript) son değişim zamanı.

## Okuma maliyeti

Bir `outbox` bir günde **48.409 byte / 20 mesaj** oldu (ortalama 2.420 byte/mesaj). Agent
her okumada tamamını context'e alıyor: **13.831 token.** Yalnız son mesaj okunsaydı
**691 token.** Yirmi okumada fark: **262.794 token.**

## Biçim sapması — "oturum" tanımsız kalınca

Dört agent **üç farklı** biçimde kutu açtı:

```
-ilk                    (elle etiket, yönetici açtı)
-kanal-kurulumu         (iş adı)
-20260806-2345          (tarih-saat)
-20260806-2345          (tarih-saat — AYNI dakika)
```

Son ikisi aynı dakikada açıldı, ikisi de `2345` aldı. Aynı rolden iki örnek olsaydı
kutular çakışırdı.

**Sebep:** şablonda `{oturum}` yazılıydı ama **örnek verilmemişti.**

## Onaysız düzen — akıyor ama durdurulamıyor

İki agent doğrudan (yöneticisiz) konuşturuldu: 6 mesaj, ~2 dakika ritim, protokol sapması
sıfır, bozulma sıfır. **Akış çalıştı.**

Ama yönetici durdurma mesajını kanala bıraktı ve **ikisi de görmedi** — çünkü her biri
karşı tarafın kutusunu izliyordu, kendi kutusunu değil.

**Sonucu:** yöneticinin gerekçesi kontrol değil **müdahale imkânı.**

## Mesaj uzunluğu

Agent'lar doğal olarak uzun yazıyor: hukuk testinde mesaj başına ~5.600 karakter, bir
gereksinim dosyası 9.870 byte. Kanalda uzunluk sınırı yok.

## Kalıcılık boşluğu — dört bağımsız uç aynı şeyi söyledi

Dört agent, ayrı oturumlar, birbirlerini görmüyorlar:

> *"Bunu bilmemin tek sebebi senin bu mesajı yazmış olman."*
> *"Kanal kurulumu kanonumda yok, yarın bilmeyeceğim."*
> *"Her sabah kutumu ve monitörümü talimatla kurmam gerekecek — bir engel değil, bir
> maliyet."*
> *"Bugün bunları bana sen yazdın; yarın yazan olmazsa kurulum yapılmaz."*

Ve bir düzeltme: *"sekiz agent olduğunda hiçbiri kurulumu bilmez"* **yanlış tarihli** —
**bir agent, bir sonraki oturumda** bilmiyor. Sekiz agent gerekmiyor.

## JSON deposu tasarımı — ölçüldü, sahada sınanmadı

Claude Code'un kendi task mekanizmasından öğrenilen kalıp: `.lock` (0 byte, varlık =
kilit), `.highwatermark` (sayaç), `{n}.json` (mesaj başına dosya).

**Ve kilit gereksiz çıktı.** Çakışma numara paylaşımından doğuyordu; dosya adı
`{zaman}-{yazar}.json` olursa paylaşılan hiçbir şey yok.

```
kilitli   : 30/30 dosya, sıfır çakışma, 22.2 ms/mesaj
kilitsiz  : 45/45 dosya, sıfır çakışma, 6.4 ms/mesaj
okuma     : 45 kat az byte
```

**Kenar durumlar — on senaryo, hepsi geçti:**

Mikrosaniye çözünürlüğü aynı yazarın **200 aralıksız** mesajında yetti (200 tekil ad) ·
çok satırlı gövde + `"` + `'` + backtick + `$` + `\` + iç içe JSON bozulmuyor · Türkçe ve
emoji korunuyor (`ensure_ascii=False` şart) · 1000 dosyada listeleme+sıralama **0.9 ms**,
imleç sonrasını bulma **0.04 ms** · yanlış kutuya yazma **dosya adından** yakalanıyor.

**Üç madde ekledi:**

**Yarım yazılmış dosya — risk gerçek.** Okuyan yazma sürerken açarsa `JSONDecodeError`.
Çözüm ölçüldü: **geçici ada yaz + `mv`** (aynı dosya sisteminde atomik), `.tmp` artığı
kalmıyor.

**Büyük mesaj kazancı yiyor.** 110 KB'lık tek mesaj bozulmuyor ama **31.446 token** —
tasarım mesaj boyutu makul olduğunda kazandırıyor.

**İmleç silinirse tüm kanal yeni sayılıyor** — 1000 mesajlık kanalda **69.429 token.**
Varsayılan gerekli: imleç yoksa son 10 mesaj.

## Reddedilen iki alternatif

**`SendMessage` / agent teams:** agent team **tek bir oturumun içinde** kurulur; mailbox'lar
`~/.claude/teams/{takım}/inboxes/` altında ve o yollar yalnız aynı takımın üyelerine
bilinir. **Ayrı terminalde açılan oturum hiçbir takımın üyesi değil.**

İki şey öğrenildi: Claude Code'un kendi çözümü de **dosya tabanlı** (yani dosya kullanmak
yanlış değil), ve onların mailbox'ı **uçucu** — oturum bitince siliniyor, mesaj geçmişi
tutulmuyor. Bizimki kalıcı ve bu bir kesintiden sağ çıkmayı sağladı.

**`memory` MCP'si:** oturumlar arası **paylaşılıyor** (ölçüldü: bir oturum düğüm yazdı,
diğeri okudu ve gözlem ekledi). Ama deposu yine dosya (`memory.jsonl`) ve varsayılan yolu
**npx cache'inin içi** — cache temizlenirse ya da paket sürümü değişirse veri kaybolur.

**`CronCreate`:** agent açmıyor, **prompt zamanlıyor.** Oturum kapanınca siliniyor, 7 gün
ömrü var — *"her sabah kanal kurulumu"* için kullanılamaz.

## Belge yetersizliği

Resmî dokümantasyon (`code.claude.com/docs/en/tools-reference.md`) `Monitor` hakkında
**7 sorudan 5'ini** cevaplamıyor: paralel monitör sınırı, `persistent` ömrü, ölüm
bildiriminin garantisi, olay hızı sınırının sayısı, macOS'ta dizin izleme yöntemi.

**Sonucu:** skill'deki monitör kuralları **ölçüme** dayanıyor, belgeye değil. Araç sürümü
değişirse yeniden ölçülmeli.
