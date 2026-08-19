---
name: kanal-kurulumu
description: "Kanal kurulumu ve yönetimi — YALNIZ `/kanal` komutuyla açılır, kendiliğinden tetiklenmez. Yıldız topoloji, merkez inbox düzeni, beş Python betiği, ölçülmüş arıza tarifleri. Kanal her oturumda gerekmiyor; gerektiğinde Mert `/kanal` der."
---

# Kanal kurulumu

Bu skill **yöneticinin işini** taşır: kanal nasıl kurdurulur, nasıl izlenir, arıza nasıl
ayırt edilir.

**Düzen v3 — JSON, mesaj başına dosya, beş betik.** md düzeni (tek dosyaya `>>` ile
ekleme), `tail -F` ile izleme ve elle kurulum **bırakıldı.** Üçü de ölçümle çürütüldü.

## Üç kaynak — hangisi neyi söyler

```
skill-project/tools/kanal/   NASIL yapılır · betikler kendi kullanımını basar
bu skill                     KİM ne yapar · yöneticinin disiplini
references/olcumler.md       KANIT · hangi kural hangi ölçümden çıktı
```

⚠️ **Betiklerin TEK yolu `/Users/karaok/p/ozel-yazilim/skill-project/tools/kanal/`.**
Beş dosya: `setup.py` · `send.py` · `read.py` · `watch.py` · `archive.py`.

Bir dönem `~/.pr-kanal/{proje}/tools/` altında kopyaları vardı ve bir de
`SABLON-JSON.md` diye ayrı bir düzen dosyası. **İkisi de artık yok** — ölçüldü
2026-08-19: dört projenin hiçbirinde `tools/` yok, `SABLON-JSON.md` araması sıfır
sonuç. Bu skill onların silinmesini kendi içinde öngörmüştü (*"git'te değil, dizin
silinirse yeniden üretme tarifi yok"*) ve öngörü gerçekleşti.

**Sonuç:** kopya yol yazılmaz, mutlak kaynak yazılır. Bir düzeltme kaynağa yazılır ve
kopya üretilmez — kopya üretilirse bir sonraki kanal eski kopyadan doğar ve arıza geri
gelir.

---

# Yapı

**Her kanalın bir yöneticisi vardır, her agent'ın iki kutusu olur, her kutunun tek
yazarı vardır.**

```
Yönetici → her agent'ın inbox'ına YAZAR, outbox'ını OKUR
Agent    → kendi outbox'ına YAZAR, kendi inbox'ını OKUR
Agent → Agent : YOK
```

**Tek yazar kuralının gerekçesi v3'te değişti.** md düzeninde **veri bütünlüğü** kuralıydı
— aynı dosyaya iki taraf yazınca mesajlar fiziksel olarak iç içe giriyordu. JSON
düzeninde paylaşılan dosya **yok**, karışma fizikle imkânsız. Kural yine de duruyor ama
artık **atıf ve kimlik** kuralı: kutunun sahibi bellidir ve `send.py` yanlış kutuya
yazmayı yakalar.

Bunu bilmek önemli — bir kuralın gerekçesi çürüdüğünde kural körlemesine savunulmaz,
yeni gerekçesi söylenir.

**Yönetici zorunlu, çünkü akış yöneticisiz de çalışır ama durdurulamaz.** Uçlar
birbirinin kutusunu izlerken kendi kutusunu izlemiyor; merkez bir dur emri bıraksa kimse
görmez. Yöneticinin gerekçesi kontrol değil **müdahale imkânı.**

## Akış — asimetrik

```
Agent → Yönetici : outbox'a doğrudan yazar, onay beklemez
Yönetici → Agent : EKRANA basar → onay alır → SONRA inbox'a yazar
```

Agent'ın soru sorması izin gerektirmez; ona iş gitmesi gerektirir.

**Onay `AskUserQuestion` ile istenir**, metinle değil. Metin olarak *"onay bekliyorum"*
demek atlanabiliyor; araçla sorulunca kapı tık olmadan geçmiyor.

**Kanal iş taşır, yetki taşımaz.** Yönetici `inbox`'a *"şunu yap"* yazar, *"onaylıyorum"*
yazamaz. Onay ekrandan gelir.

---

# Kurulum — betikle, elle değil

```
setup.py     kutu + STATUS.md + boş imleçler (tek komut)
send.py      mesaj yaz (.tmp + os.replace, atomik)
read.py      imleçten oku; imleç kaybında DURUR
watch.py     dizin yoklar, kalıcı yayın kaydı (.announced)
archive.py   okunmamış varsa REDDEDER; devri HANDOVER.json ile taşır
```

Elle kurulan bir düzen *"kurulabilir"* olur ama **"tekrarlanabilir"** olmaz: her okuyan
kendi yorumunu yapar, sapma düzeltilmez ve **yayılır.**

**Kurulumu agent kendi yapar, sen yapmazsın.** Kurulumu yapmayan agent protokolü
öğrenmiyor — hazır bulup kullanıyor ve bir sonraki oturumda bilmiyor. Senin işin
handoff'u yazmak ve akışı izlemek.

## Sıra — atlanmaz

```
1. Hangi projede kanal kurulacağına karar ver
2. HER AGENT kendi kutusunu ve izleyicisini kurar, sonra BEKLER
3. Uçların OUTBOX'larını + kendi inbox'ını tek izleyiciyle izlemeye al
4. İKİ YÖNLÜ TEST
5. Test geçerse gerçek iş başlar
```

**4. adım neden atlanmaz:** doğrulanmamış altyapıya iş yüklenirse iş yapılır ama bir yön
sessiz kalabilir; mesajlar elden taşınır ve kimse fark etmez.

## `--project` bayrağı ZORUNLU

**Kural: `--project` her zaman yazılır**, varsayılanla aynı olsa bile. Açıkça yazılmış
varsayılan bir karardır; atlanmış varsayılan bir boşluktur.

Verilmezse betik `skill-project` kullanır **ve `stderr`'e uyarı basar** (2026-08-11).
Yani atlanan bayrak artık sessiz değil — ama uyarı ekranda kaybolabilir, o yüzden kural
duruyor.

Arızanın şekli bilinir: varsayılan **doğru olduğu sürece görünmez.** Ölçüldü
(`references/olcumler.md`) — dört uç bayrak eksiğini bulmadı, çünkü dördü de varsayılan
projedeydi. Başka bir projede çalışan agent bayrağı atlarsa kutusu fabrikanın dizinine
düşer, `rc=0` alır; uyarıyı okumazsa fark etmez.

**Betiklerin tek kaynağı** yukarıda yazılı: `skill-project/tools/kanal/`. Kopya
üretilmez; agent'a verilen handoff o mutlak yolu taşır.

## Dizin yapısı

```
~/.pr-kanal/{proje}/{rol}-{oturum}/inbox/*.json     ← yönetici yazar
~/.pr-kanal/{proje}/{rol}-{oturum}/outbox/*.json    ← agent yazar
~/.pr-kanal/{proje}/{rol}-{oturum}/STATUS.md
~/.pr-kanal/{proje}/archive/{tarih}/
~/.pr-kanal/{proje}/archive-log.json                ← devir izi
```

**`{oturum}` = `YYYYMMDD-HHMM`** (kanon, 2026-08-07). `setup.py` üretiyor; aynı dakikada
ikinci kurulumu `rc=1` ile reddediyor.

**Kanal proje dışında yaşar.** Müşteri reposuna yazılmaz — `.gitignore` unutulursa kanal
trafiği projeye commit'lenir. `/tmp` de kullanılmaz, uçucu.

---

# İZLEME — en çok hata yapılan yer

## `tail -F` KULLANILMAZ

İki katmanda birden kırık:

**Boş dizinde komut hiç başlamıyor** — zsh eşleşmeyen glob'da komutu çalıştırmıyor, ve
**yeni kutu her zaman boştur.** Yani kurulum anı tam olarak arızanın anı.

**Dolu dizinde kurulsa bile sonrakini görmüyor** — glob kabukta bir kez genişliyor, `tail`
dizini değil o anki dosya listesini izliyor. Yani *"önce bir dosya at, sonra kur"* da
çözüm değil.

**Çözüm: dizin yoklama** (`watch.py`), bedeli 1 saniyelik gecikme.

## `Monitor` aracı şart, `Bash` değil

**`Bash(run_in_background)` süreç çalıştırır ama bildirim üretmez** — çıktıyı dosyaya
yazar, agent'ı uyandırmaz. Süreç listesinde canlı görünür, kimse uyanmaz.

**`Monitor` ve `TaskOutput` deferred** — `ToolSearch("select:Monitor,TaskOutput")` ile
yüklenir.

**İkisi de gelmiyorsa monitör kurulmaz, merkeze bildirilir.** Araç erişimi role göre
değişebiliyor. Doğrulanamayan monitör kurulmamış olandan **daha kötü** — çalıştığı
sanılır ve sessizlik *"mesaj yok"* ile aynı görünür.

**`TaskList` kullanılmaz** — planlama task'larını listeliyor, arka plan süreçlerini
değil. Yanlış araçla **boş döner** ve boş dönüş *"kayıt yok"* gibi okunur.

## Kim neyi izler — merkez ile uç ayrı

```
UÇ     kendi inbox'ını izler       (merkez ona yazar)
MERKEZ uçların OUTBOX'larını izler (uçlar ona yazar) + kendi inbox'ını
```

Bu ayrım v2 şablonunda **yoktu** ve bir uç yakaladı: şablon *"monitör yalnız inbox'ı
izler"* diyordu ama o cümle ucun tarafını anlatıyordu. Merkez uçların outbox'ını izlemek
zorunda, yoksa raporları görmez.

Echo riski yok: merkez `inbox`'a yazar, `outbox`'ı okur — yazdığı yeri izlemiyor.

Merkez **tek izleyiciyle** birden çok kutu izler; hepsi tek `watch.py` çağrısına verilir.

## İki ayrı kayıt — birleştirilmez

```
.cursor      → agent NE OKUDU        (read.py yönetir)
.announced   → izleyici NEYİ BAĞIRDI (watch.py yönetir)
```

Birleştirmek, monitörün bağırmadığı bir mesajı okunmuş saymaya yol açar. **İki farklı
soru, iki farklı kayıt.**

**İzleyici kaydı diskte tutulur.** Monitör oturumla birlikte ölüyor; bellekte tutan sürüm
ölüm ile yeniden kurulum arasında gelen mesajları **yutuyordu.** Mesaj imleçle kurtulur
ama **uyandırma kaybolur** — bekleyen agent beklediğini bilir, mesajın geldiğini bilmez.

**Tasarım ilkesi: gürültü zararsız, kayıp zararlı.** Monitör fazladan bağırırsa imleç
süzer; eksik bağırırsa mesaj hiç görünmez.

**Ama gürültünün tavanı var:** `Monitor` çok olay üreten monitörleri **otomatik
durduruyor** — yani gürültü sonunda **sessizliğe** dönüşür. O yüzden kayıp kutu her turda
değil, durum değişiminde bir kez bağırılır. Bedeli: agent o tek bağırmayı kaçırırsa uyarı
bir daha gelmez.

**Bir bildirim birden çok mesaj taşıyabilir** — araç yakın olayları gruplıyor. Son
dosyaya bakan agent öncekini **atlar ve atladığını fark etmez.** Kural: bildirimde
**imleçten sonrasının tamamı** okunur.

**Merkezin dinlemesi protokolün şartı, tercih değil.** Merkez dinlemezse bütün trafik
durur ve **durduğu görünmez.**

---

# Yazma, okuma, kapanış — kurallar

## `printf` YASAK

`printf` en hızlı yöntemdi ve **ilk testte geçti** — çünkü kaçışlar elle yazılmıştı.
Gerçekçi bir gövdeyle (tırnak + ters bölü) **çıkış kodu 0** verip **bozuk JSON** üretti.

Yani kazancı hız değil, **doğruluk riski** — ve arıza yazan tarafta görünmüyor, okuyan
tarafta patlıyor. `send.py` kullanılır; uzun gövde `--stdin` ile verilir.

**Mutlak yol zorunlu.** Ölçülmüş tek gerçek agent hatası göreli yoldu: iki mesaj sessizce
kayboldu.

**Uzun içerik kanala gömülmez** — dosya yolu verilir. Büyük mesaj imleç kazancını yiyor.

## `type` yalnız dört değer

`TASK` · `INFO` · `QUESTION` · `CLOSE`. `send.py` başkasını `rc=1` ile reddediyor —
kapanış mesajı da **`CLOSE`** ile yazılır.

> ⚠️ Bir dönem dolaşan `KAPANIS` değeri **çalışmaz** — `send.py` onu `rc=1` ile
> reddeder. Doğrusu `CLOSE`.

## İmleç kaybında DURUR

*"Son N"* varsaymak **iki yönlü** sessiz hata üretiyor: yapılmış işler yeniden iş emri
gibi okunur (tekrar iş) **ve** eskiler sessizce atlanır (kayıp iş).

```
imleç dosyası VAR + boş  → kutu hiç okunmadı, KASITLI durum → hepsi okunur, kayıp yok
imleç dosyası YOK + ≤10  → hepsi okunur (güvenli)
imleç dosyası YOK + >10  → OKUMAZ, DURUR, seçenek sunar (rc=2)
```

**Bozuk JSON'da da durur** — imleç bozuk dosyanın önünde bekler. Eskiden atlanıp
ilerliyordu: *"görünür hata + sessiz kayıp."*

## Çıkış kodları — `&&` kesilmeli

```
read.py     0 okundu · 2 DURDUM, karar gerek · 1 hata
send.py     0 yazıldı · 1 geçersiz tür / kutu yok
setup.py    0 kuruldu · 1 kutu zaten var (ezmiyor)
archive.py  0 arşivlendi · 2 REDDETTİ (okunmamış var) · 3 --force, VERİ ATLANDI
```

Bu sınıf `printf`'in yasaklanma sınıfıyla **aynı**: iş yapılmamışken çıkış kodu
*"başarılı"* diyordu. Somut arıza: `read.py && send.py` zincirinde `read.py` durdu, `&&`
geçti ve **okunmamış bir işe cevap yazıldı.**

**`--force` bile sıfır dönmez** — bilinçli atlama bilinçli kalmalı.

### ⚠️ BORU HATTI ÇIKIŞ KODUNU YUTAR — ölçüldü 2026-08-12

`$?` **son komuttan** gelir, betiğin kendisinden değil:

```
python3 send.py <olmayan-kutu> ... ; echo $?        → 1   ✅ doğru
python3 send.py <olmayan-kutu> ... | tail -3 ; echo $?  → 0   ← tail'in kodu
```

**Vaka:** Clara `| tail -3` ile çağırdı, `rc=0` gördü, *"`send.py` çıkış kodu
tutarsız"* diye **fabrikaya bulgu göndermek üzereydi.** Ev Clara ve PAD ikisi de
`rc=1` almıştı; üç ölçümden ikisi doğruydu, yanlış olan Clara'nınkiydi.

Ev Clara yakaladı: *"üç ihtimal var ve hangisi olduğunu ölçmedin — çağırma
biçimini yaz."* Yazınca sebep göründü.

**Kural: çıkış kodu ölçülecekse boru hattı OLMAYACAK.** Ya doğrudan çağır, ya
`${PIPESTATUS[0]}` kullan (bash; zsh'de `$pipestatus[1]`).

**Sınıfı:** ölçüm aracının kendisini doğrulamamak. Bu, `rc=0 yetmez` kuralının
ikinci yüzü — birincisi *"betik yalan söyleyebilir"*, bu *"kabuk yalan
söyleyebilir"*.

## MERKEZ YAYIN — proje Clara'larına toplu mesaj

Araç: **`pr-yazilim-ceo/araclar/tools/clara-yayin.py`** (Clara'nın kendi tezgahı,
`skill-project`'in kanal betiklerinden ayrı).

```
clara-yayin.py --liste                          # kim canlı, kim izliyor
clara-yayin.py --tip INFO --stdin               # tüm canlı Clara'lara
clara-yayin.py --tip TASK --hedef goat --stdin  # tek projeye
clara-yayin.py --tip INFO --stdin --kuru        # yazmadan dene
```

**YALNIZ Clara kutularına yazar** — agent kutularına asla (`CLA-NO-CALL-TEAMS`).
Hedef seçimi ölçümle: izleyicisi **VAR** + kutu **bugünün** olmalı. Ölü kutu
otomatik elenir (ölçüldü: goat'ta iki eski Clara kutusu duruyordu).

### Teslim doğrulanır — `rc=0` YETMEZ

Yazdığı her dosyayı **geri okur** ve gövde uzunluğunu karşılaştırır. `rc=0` yalnız
**hepsi** teslim edilmişse döner.

Bu zorunlu, çünkü ölçüldü (2026-08-11, iki bağımsız vaka): `send.py`'ye `<box>`
argümanı olarak **ajan dizini** verildiğinde (`.../inbox` yerine) betik dosyayı o
dizine yazıyor, `written` basıyor ve **`rc=0`** dönüyor — mesaj teslim edilmiyor.
`send.py` kutunun VAR olup olmadığına bakıyor, **türüne bakmıyor.**

⚠️ **Aynı `rc=0` arızası bir günde üç yerde bağımsız yakalandı:** `send.py` gövde
yutması (sabah) · `npm run build` 10 hata verip exit 0 dönmesi (15:15) · `send.py`
yanlış dizine yazması (15:53). **`rc=0` bir iddiadır, sonucun kendisi değil.**

### Alma tarafı da kurulur — asimetrik doğrulama tuzağı

Ölçüldü aynı gün: yayın kanalı kurulurken **gönderme iki kez doğrulandı, alma hiç
doğrulanmadı.** `ceo/Clara-*/inbox` kutusunda **sıfır izleyici** vardı; Goat'ın iki
cevabı görülmedi. Karşı taraf fark etti (*"almamış olabilirsin, tekrar ediyorum"*),
merkez fark etmedi.

**Kural: yayın kurulduğunda kendi kutunun izleyicisi de kurulur.** Tek yönlü kanal
kanal değildir.

## Kapanış İKİ TARAFLI

Agent kendi kutusunu **tek başına kapatamaz**: outbox'ta okunmamış mesaj varsa
`archive.py` reddediyor, ve o imleç **merkezin.**

```
1. Agent  → outbox'a CLOSE yazar
2. MERKEZ → agent'ın outbox'ını okur (read.py)
3. MERKEZ → arşivler (archive.py)
```

**Neden kapı var:** v2'de arşive taşınan kutunun okunmamış mesajları ve imleci yeni
kutuya hiç geçmiyordu — devir bir **disiplin** meselesiydi, mekanizma değil. Yazan
unutursa kayboluyordu.

**Tek taraflı arşivleme yasak.** Merkez kutuyu taşıdı, agent haber almadı ve ölü adrese
yazdı. Artık arıza sessiz değil (izleyici bağırıyor) ama **gürültü de iş kaybı demek.**

**Silme yasak** — silinen mesaj sessizce gidiyor; izleyici ölmüyor ama silindiğini de
söylemiyor.

### ⚠️ `--force` ARAÇ UYARIRKEN VERİLMEZ — ölçüldü 2026-08-12

`archive.py` okunmamış mesaj varsa **reddeder** ve şunu yazar:
*"the loss is SILENT"*. Bu bir öneri değil, kapıdır.

**Vaka:** ev Clara kutusunu `--force` ile arşivledi. `HANDOVER.json` kanıtı:
`"forced": true` · `inbox: 132` · `inbox_cursor: ""` (boş).
**132 mesaj okunmadan gitti** ve dördü merkezin bekleyen sorularıydı — mekanizma
sorusu, iki skill işi, hatırlatma. Merkez cevap bekledi, ev Clara *"soru
gelmedi"* sandı.

Kendi tespiti: ***"'görmedim' ile 'gelmedi' aynı şey değil."***

**Kural: `--force` yalnız okunmuş bir kutuda kullanılır.** Okunmadıysa önce
`read.py` — ve okunacak vakit yoksa **kutu açık bırakılır.** Açık kutu bir
maliyet değil; kayıp mesaj maliyet.

**İkinci kural: oturum ekranda dururken kanal kapatılmaz.** Ev Clara kapanışı bir
adım olarak uyguladı, oysa oturum sürüyordu — kapatınca **kör oldu.**

### ⚠️ `.cursor` BOŞ KALIYOR — "okundu" izi YOK

Kutularda `.cursor` dosyası var ama **boş.** Yani:

```
ulaştı mı?   → ÖLÇÜLEBİLİR (dosya inbox'ta duruyor)
okundu mu?   → ÖLÇÜLEMEZ
```

**Bunun bedeli iki kez ödendi.** 2026-08-11 gecesi: iki agent cevaplarını yanlış
kutuya yazdı, ikisi *"cevap verdim"* sandı, merkez *"cevap gelmedi"* sandı —
**1 saat 50 dakika.** 2026-08-12: merkez kutuyu ölçtü, *"mesajım orada duruyor,
ulaştı"* dedi — doğruydu ama **okunmamıştı.**

**Davranış kuralı (mekanizma yokluğunun yaması):** iş verildiğinde **okunduğu
bildirilir.** Cevap uzun sürecekse *"aldım, işleniyor"* demek yeter — o tek satır
*"ulaşmadı mı / işleniyor mu"* ayrımını kapatır.

⚠️ Bu bir **yama** ve öyle olduğu biliniyor: bildiren bildirir, bildirmeyen
bildirmez, fark yine görünmez. Asıl çözüm `read.py`'nin cursor'a yazması —
fabrikaya gidecek bulgu.

---

# Canlılık — üç sinyal, biri çalışıyor

**`kill -0 PID` → YANLIŞ.** İki kez çürütüldü: canlı agent'ları ölü gösterdi. `STATUS.md`
PID'i agent'ın kendi süreci değil, onu doğuran kabuğunki olabiliyor ve o kabuk her `Bash`
çağrısında yeniden doğuyor.

**Transcript son değişim zamanı → YANLIŞ, ve daha kötü yönde.** Transcript **proje**
bazlı, kutu bazlı değil — ölçülen kutuların hepsi *"canlı"* çıktı. `kill -0` canlıyı ölü
der (zararsız yanlış); bu **ölüyü canlı** der ve temizlik hiç yapılmaz.

**Kutunun kendi son yazım zamanı → ÇALIŞIYOR.** Tek geçerli sinyal.

**Ama eşik uydurulmaz.** Günlerce bekleyen işler ölçüldü, hiçbiri *"askıda"* değildi.
Çözüm eşik koymak değil **bekleyeni görünür kılmak.** Otomatik ölü-kutu temizliği
yapılmaz — elle doğrulanır.

**`PID` alanı `STATUS.md`'den KALDIRILDI.** Üç turda üç kez düzeltildi, hiçbir turda bir
soruya cevap vermedi. Yerine `BOX` — kutunun kendi yolu, hiçbir sürece bağlı değil.

**Genel ders:** bir alan üç kez düzeltilip hâlâ boş dönüyorsa sorun doldurma biçiminde
değil, **alanın kendisinde.** Üçüncü düzeltmede sorulacak soru *"nasıl doldururum"* değil,
**"bu alan hangi soruya cevap veriyor"**.

---

# Ölçüm tuzakları — merkez bunlara düştü

**Eşzamanlılık sayımla değil zaman damgasıyla sınanır.** Dört agent aynı kutuya yazdı,
karışma sıfır çıktı — ama damgalar dördünün **sırayla** yazdığını gösterdi. Sıfır karışma
*"çakışma engellendi"* demiyor, **"çakışma hiç olmadı"** diyor. Üç uç ilk turda sayıma
bakıp damgalara bakmadı, çünkü **doğrulanan beklenti sorgulanmıyor.**

**"Boş" bir ölçüm değil, okunmamış bir kutunun görünümü.** Merkez dört outbox'ı `ls` ile
tarayıp *"boş"* dedi; rapor 9 dakika önce yazılmıştı. İmleç tutulmadan yokluk iddiası
verilmez.

**Ham metin araması alan adlarıyla gövdeyi ayırmıyor.** Bir karışma taraması 25 *"yabancı
iz"* buldu ve hepsi **yanlış alarmdı** — eşleşen şey kendi yazdığı alan adıydı. Parse
edip gövdeye bakınca sıfır çıktı.

**Bir şablon kendi iddiasını tutmuyorsa o iddia gerçekte bir boşluktur.** v3'ün ilk hâli
iki imleç durumunu ayırdığını yazıyordu, kod ayırmıyordu. Bir uç yakaladı: *"niyet doğru
yazılmış, kod uygulamamış."* Bir kural yazılıyken kodun da onu yaptığı doğrulanır.

---

# HANDOFF ŞABLONU

*"N agent için kanal kur"* dendiğinde sıfırdan düşünülmez. Blok her agent için bir kez,
rol ve proje adı değiştirilerek verilir. Ekrana basılır, kullanıcı taşır.

**Adres handoff'ta verilir.** Agent kanonlarında kanal protokolü **yok** — dört uç bunu üç
kez söyledi. Şablonun yolu dışarıdan verilmezse agent onu aramayı bilmez.

```
KİMDEN → KİME: Clara → {ROL}
TÜR: İŞ — kanal kurulumu · üretim işi DEĞİL

NE: Kendi kanalını kur, izleyicini aç, sonra bekle.

  ARAÇLAR: /Users/karaok/p/ozel-yazilim/skill-project/tools/kanal/

  1. KUTUNU KUR — elle mkdir YOK:

     A=/Users/karaok/p/ozel-yazilim/skill-project/tools/kanal
     python3 $A/setup.py {ROL} --task "{TEK SATIR İŞ}" --project {PROJE}

     `--project` ZORUNLU. Atlanırsa varsayılan `skill-project` olur ve
     stderr'e uyarı düşer — ama kutun yanlış projeye kurulmuş olur ve
     uyarıyı okumazsan rc=0 alıp FARK ETMEZSİN.

     setup.py kalan komutları mutlak yollarla ekrana basar — onları kullan.

  2. İZLEYİCİNİ KUR — `Monitor` ARACIYLA, `Bash` ile DEĞİL.

     Önce ToolSearch("select:Monitor,TaskOutput").
     İKİSİ DE gelmezse monitör KURMA, merkeze bildir — doğrulanamayan
     monitör kurulmamış olandan daha kötüdür.

     command: python3 $A/watch.py <KUTU>/inbox 2>&1 \
                | grep -E --line-buffered 'from=|ERROR:|INFO:|watcher started'
     persistent: true

     `tail -F` KULLANMA — boş dizinde hiç başlamıyor, dolu dizinde
     sonradan geleni görmüyor.

  3. CANLILIĞI DOĞRULA — TaskOutput(<id>, block:false) → status: running
     `TaskList` DEĞİL, o başka defter ve boş döner.

  4. ELLE BİR OKUMA YAP — python3 $A/read.py <KUTU>/inbox

  5. MERKEZE HABER VER:
     python3 $A/send.py <KUTU>/outbox {ROL} {MERKEZ} INFO "kuruldum, izleyici canlı"

NEDEN: Kurulumu sen yaparsan protokolü öğreniyorsun; hazır bulursan
       kullanıyorsun ama bilmiyorsun — ve bir sonraki oturumda
       bilmeyeceksin.

YAPININ ÖZÜ:
  · inbox : merkez yazar, sen OKURSUN
  · outbox: sen yazarsın, merkez OKUR
  · Başka hiçbir kutuya dokunmazsın.

YAZMA: `send.py` kullan. `printf` YASAK — çıkış kodu 0 verip bozuk JSON
       üretiyor, arıza okuyan tarafta patlıyor. Uzun gövde `--stdin` ile.
       Mutlak yol zorunlu. type: TASK|INFO|QUESTION|CLOSE.

OKUMA: bildirim geldiğinde imleçten sonrasının TAMAMINI oku — son dosyayı
       değil. Bir bildirim birden fazla mesaj taşıyabilir. `read.py` rc=2
       verirse DURMUŞTUR, okumamıştır — `&&` ile zincirleme.

KAPANIŞ: outbox'a CLOSE yaz, sonra BEKLE. Kutunu kendin arşivleme —
       okunmamış raporun varsa archive.py seni zaten reddeder (rc=2).

SONRA: BEKLE. Üretim işine başlamıyorsun. Merkez test mesajı yazacak,
       sen outbox'a cevap vereceksin — kanal iki yönde doğrulanacak.
```

---

# Yöneticinin disiplini

Yıldız topolojide trafik tamamen merkezden geçtiği için merkezin disiplini tek denetim
noktasıdır.

**Her olay aktarılmaz — örüntü ve karar aktarılır.** Aktarılacak üç şey: bir **sapma**,
bir **arıza**, ya da bir **karar** gerekiyorsa.

**Rapor değil karar getirilir.** Kullanıcı agent ekranlarını görmüyor.

**Kurulum bitince oturum izlemesi bırakılır, yalnız kanal izlenir.** Agent'ın iç işleyişi
merkezi ilgilendirmiyor.

**Altyapı yöneticinin, içerik kullanıcının.** Kanalın nasıl kurulduğu yöneticinin alanı;
hangi işin verileceği, neyin onaylandığı kullanıcının.

**Uçlar itiraz edebilir olmalı** ve bu bir arıza değil güvenlik ağıdır. Ölçüldü: bir turda
düzeltilen taraf **on kereden fazla merkez** oldu — eşzamanlılık iddiası, canlılık
sinyali, şablonun kendi çelişkisi, okunmamış outbox, `printf`, `PID` alanı, monitör
komutu. Hepsi uçlardan geldi.

**Ve uçlar kendi sonuçlarının neyi kanıtlamadığını da söyledi** — *"bulamamak yokluk
kanıtı değil"*, *"bulgu benim, sınıflandırma senin"*. Merkez bunu bekler, sınıflandırmayı
kendi yapar.

**Ama itiraz da ölçülür.** Bir agent'ın raporundaki mekanik iddia (*"şu araçla kuruldu"*,
*"şu mekanizma çalışıyor"*) ölçüm değildir; aktarmadan önce kendin ölç.

---

# Açık kalemler

**Agent'lar arası gerçek eşzamanlılık** — mevcut mimaride ölçülemiyor (ana döngü sıralı).
Mekanizma kanıtlı, koşul kanıtlanmadı.

**Ölü kutu eşiği** — sinyal bulundu, eşik bir karar. Otomatik temizlik yapılmıyor.

**`Monitor` otomatik durdurma eşiği** — ölçülmedi.

**1000 dosyalı kutu** — en büyük ölçüm 100 dosya.

**Yaşam döngüsü senaryoları otomatik sınanmıyor.** Düzen değişince elle koşulmalı ve
hatırlatan mekanizma yok.

**Araçlara tek nokta bağımlılığı — v3'ün kırılgan yeri.** Betikler `~/.pr-kanal/` altında
ve **git'te değil.** Dizin silinirse yeniden üretme tarifi yok. Özeti: *"v2 kurulabilir
ama kopyalanamazdı; v3 kopyalanabilir ama araçlara bağımlı."* Asset'e dönüşünce kapanır.

**Agent kanonları hâlâ kanalı bilmiyor** — üçüncü kez söylendi. Handoff şablonu geçici
olarak kapatıyor; kalıcı çözüm fabrikanın (PAD) işi.

**Şablonun `KAPANIS` hatası** — PAD'e bildirildi, düzeltilmedi.

## Kapanmış kalemler — artık sorulmaz

**`{oturum}` biçimi** → `YYYYMMDD-HHMM`, Mert kanona aldı (2026-08-07).

**Canlılık ölçütü** → kutunun kendi son yazım zamanı; diğer iki aday çürütüldü.

**`inbox`/`outbox` ayrımı gerekli mi** → evet. İmleçler ayrı: outbox imleci **merkezin**,
inbox imleci **agent'ın.** Tek dizin bunu çözemezdi.

**JSON deposu** → sahada sınandı, dört uç *"üretim işi için engel yok"* dedi.

**İlk kutuyu kim açar** → agent kendi kutusunu `setup.py` ile açar, adres handoff'ta
verilir. Kalıcı düzen bu.

**İş talimatı onay yerine geçer mi** → geçmez. Onay `AskUserQuestion` ile ekrandan alınır.
