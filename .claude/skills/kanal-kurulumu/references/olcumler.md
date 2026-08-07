# Kanal kurulumu — ölçümler

Bu dosya **kanıt** taşır: skill'deki kuralların hangi ölçümden çıktığı. Skill'den atıfla
çağrılır, kendiliğinden yüklenmez.

**İki bölüm var ve karıştırılmaz:**

- **YÜRÜRLÜKTEKİ (v3, JSON)** — bugünkü kuralların dayanağı
- **TARİHÇE (v2, md)** — çürütülmüş ya da geride bırakılmış düzenin ölçümleri.
  Yanlış değil, **eski.** Bir kuralın neden bırakıldığını açıklıyorlar; yeni bir karar
  bunlara **dayandırılmaz.**

Ham kayıtlar: `gunluk/2026-08-07-kanal-json-saha-sinamasi.md` ·
`gunluk/2026-08-07-kapanis.md` · `kararlar/2026-08-06-kanal-mimarisi.md` ·
`gunluk/2026-08-06.md`

Yürürlükteki düzen ve komutlar: `~/.pr-kanal/{proje}/SABLON-JSON.md`

---

# YÜRÜRLÜKTEKİ — v3 (JSON, 2026-08-07)

## `tail -F` iki katmanda kırık — dört uç bağımsız ölçtü

**Katman 1 — boş dizinde komut hiç başlamıyor.** Kabuk zsh; eşleşmeyen glob'da
`no matches found` verip komutu **çalıştırmıyor.** Yeni kutu her zaman boş olduğu için
kurulum anı tam olarak bu an. İki uç bunu **bağımsız** ölçtü — bağımsız tekrar bir
bulgunun gücüdür, ikisi de kayda geçti.

**Katman 2 — dolu dizinde kurulsa bile sonrakini görmüyor.** `ps` kanıtı:

```
86105 tail -n 0 -F /tmp/gt3/aaa.json
```

`tail`'e dizin değil **dosya listesi** gidiyor — glob kabukta bir kez genişliyor. Yani
*"önce bir dosya at, sonra monitör kur"* da çözüm değil.

Bir ucun ayrımı: *"Katman 2'de en az yarım çalışan bir şey var; burada hiç yok."*

**Çözüm:** dizin yoklama (`watch.py`). Boş dizinde kurulup sonra yazılan mesajı yakaladığı
ölçüldü. Bedeli 1 saniyelik gecikme.

## `printf` sessizce bozuk JSON üretiyor

`printf` en hızlıydı (0 ms, en az token) ve **ilk testte geçti** — çünkü kaçışlar elle
yazılmıştı. Gerçekçi gövdeyle tekrar:

```
Kullanıcı "şunu" dedi
yol: C:\temp\yeni
```

Sonuç: **çıkış kodu 0** (başarılı dedi) ama üretilen dosya **bozuk JSON.** Aynı gövde
`python3` ile sorunsuz. Bağımsız doğrulandı.

Araç çağrısı sayısı dört yöntemde de **1**, token farkı ~42 — yani hız ekseninde ayrım
yok. Ayrım **doğruluk** ekseninde.

`jq` seçilmedi: makinede varlığı garanti değil, boş kutuda 5 kat hızlı ama dolu kutuda
eşitleniyor, dosya başına bir süreç açıyor (100 dosya = 100 süreç).

## İmleç kaybı iki yönlü sessiz hata üretiyordu

12 iş emri, imleç silinmiş, eski *"son 10"* varsayılanı:

```
10 YAPILMIŞ iş yeniden iş emri gibi okundu  → tekrar iş
 2 mesaj sessizce atlandı                   → kayıp iş
```

İkisi de sessiz. Varsayılan kaldırıldı.

**Ve iki durum kodda gerçekten ayrılmıyordu.** v3'ün ilk hâli *"imleç var+boş"* ile
*"imleç yok"*u ayırdığını **iddia ediyordu ama kod ikisini de `""` yapıp aynı dala
düşürüyordu.** Bir uç yakaladı: *"niyet doğru yazılmış, kod uygulamamış."*

## Bozuk JSON'da imleç ilerliyordu

Eskiden bozuk dosya atlanıp imleç ilerliyordu — bozuk mesaj bir daha görünmüyordu.
Tarifi: *"görünür hata + sessiz kayıp."* Artık imleç bozuk dosyanın önünde duruyor.

## Çıkış kodları — iş yapılmamışken "başarılı"

Üç uç bağımsız aynı sınıfı getirdi. Somut senaryo:

```bash
python3 $A/read.py $KUTU/inbox && python3 $A/send.py $KUTU/outbox ... "cevap"
```

`read.py` durdu, hiçbir şey okunmadı, `&&` geçti → **okunmamış bir işe cevap yazıldı.**

Ayrıca: olmayan dizinde `rc=0` dönüyordu, yani yanlış yol *"yeni mesaj yok"* gibi
davranıyordu — bu tam olarak *"mutlak yol zorunlu"* kuralının koruduğu arızanın kendisi.

`--force` da `rc=0` dönüyordu: bilinçli veri atlama normal başarı gibi görünüyordu.
Artık `rc=3`.

## Okuma maliyeti bir fonksiyon, sabit oran değil

Bir uç kendi kutusunda **3.6 kat** ölçtü, şablon **45 kat** diyordu. Çelişki değil:

```
maliyet ≈ (imleçten sonraki mesaj sayısı) × (ortalama mesaj boyutu)
```

```
imleç güncel            → 0 token
10 mesaj geride         → 899 token
imleçsiz tüm kutu (100) → 10.499 token
110 KB tek mesaj        → 31.446 token
```

Yani kazanç kutu boyutuna **ve** imleç mesafesine bağlı; sabit çarpan değil. Büyük mesaj
kazancı yiyor — uzun içerik kanala gömülmez, **dosya yolu verilir.**

## Çok yazarlı yazma — mekanizma kanıtlı, agent eşzamanlılığı ölçülemedi

**Mekanizma DOĞRULANDI.** Bariyerli 4-process testi: 522 bayt gövde (`PIPE_BUF` 512'nin
**üstünde**, yani md düzeninin kırıldığı eşiğin ötesi), **97/99 yazar değişimi** (gerçek
iç içelik), 7.5 ms pencere → **100/100 geçerli, 0 karışma, 0 kayıp.**

Kıyas: md düzeninde aynı koşul **20 blokta 423 yabancı gövde satırı** üretti.

**Agent eşzamanlılığı ÖLÇÜLEMEDİ.** Dört agent aynı kutuya 100 mesaj yazdı, 0 karışma.
Ama zaman damgaları: **yazar değişimi 3/99, kesişen ikili 0/6** — dördü sırayla yazdı,
aralarda 2.3s / 2.3s / 27s.

Yani sıfır karışma *"çakışma engellendi"* demiyor, **"çakışma hiç olmadı"** diyor. Agent
ana döngüsü sıralı; *"eşzamanlı yaz"* demek eşzamanlılık üretmiyor.

**Yöntem dersi:** eşzamanlılık iddiası **sayımla değil zaman damgasıyla** sınanır. Üç uç
(merkez dahil) ilk turda sayıma bakıp damgalara bakmadı — çünkü sayım beklentiyi
doğruluyordu. **Doğrulanan beklenti sorgulanmıyor.**

## Canlılık — üç sinyal, 11 kutuda yan yana

**`kill -0 PID` → YANLIŞ.** İkinci kez çürütüldü: iki **canlı** agent'ı ölü gösterdi (biri
0.4 dakika önce yazmıştı). Sebep: `STATUS.md`'deki PID agent'ın kendi süreci değil, onu
doğuran kabuğun PID'i olabiliyor ve o kabuk her `Bash` çağrısında yeniden doğuyor.

**Transcript son değişim zamanı → YANLIŞ, ve daha kötü yönde.** Merkez bunu *"çalışan
aday"* diye işaretlemişti; çürütüldü ve bağımsız doğrulandı: transcript **proje** bazlı,
kutu bazlı değil (`agent-project` klasöründe **58 transcript, 5 kutu**). 11 kutunun hepsi
*"0 dakika"* çıktı — **ölü kutuyu canlı gösteriyor.** Ve bazı projeler için transcript
klasörü **yok**, sinyal hiç üretilemiyor.

`kill -0` canlıyı ölü der (zararsız yanlış); bu ölüyü canlı der (temizlik hiç yapılmaz).

**Kutunun kendi son yazım zamanı → ÇALIŞIYOR.**

```
canlı dörtlü      0–3 dk
merkez            30 dk  (canlı, sadece sessiz)
başka proje ikili 202 dk
başka proje ikili 1022 dk
```

Tek sinyalle temiz ayrım. **Ama eşik uydurulmaz:** 42 ve 48 saat bekleyen işler vardı,
hiçbiri *"askıda"* değildi.

## `PID` alanı — üç turda ölçüldü, kaldırıldı

```
os.getppid()            → dört kutuda DÖRT FARKLI şey
pgrep'e çevrildi        → "?" yazdı ("bir değer değil")
NOT FOUND (...) yapıldı → dört kutunun DÖRDÜNDE de NOT FOUND
```

Sebep ölçüldü: `pgrep -f "claude --agent <rol>"` **merkezin** kabuğundan çalışınca
buluyor (PID 30590 döndü), agent'ın **kendi alt-sürecinden** görmüyor. Yani alan iki işi
de yapmıyordu — canlılık ölçütü değildi **ve kimlik de vermiyordu.**

**Genel ders:** bir alan üç kez düzeltilip hâlâ boş dönüyorsa sorun doldurma biçiminde
değil, **alanın kendisinde.**

## Arşivleme — devir disiplinle taşınıyordu, kayboluyordu

v2'de arşive taşınan kutunun okunmamış mesajları ve imleci yeni kutuya **hiç geçmiyordu.**
Ölçüm: arşivdeki dört gece kutusunda `.cursor` dosyası sayısı **0**.

**Tek taraflı arşivleme:** merkez kutuyu taşıdı, agent haber almadı ve **ölü adrese
yazdı.**

## İzleyici kaydı bellekteyken mesaj yutuyordu

Önceki sürüm başlarken mevcut dosyaları **bellekte** atlıyordu. Sonucu: monitör ölür,
arada iki mesaj gelir, monitör yeniden kurulur → ikisi de *"mevcut"* sayılıp **hiç
bildirilmez.** Mesaj imleçle kurtulur ama **uyandırma kaybolur.**

Alternatif (hepsini yayan sürüm) kayıp vermiyordu ama yeniden başlatmada okunmuş mesajları
tekrar bildiriyordu. Üçüncü yol seçildi: diskte `.announced`.

**Bildirim ≠ mesaj:** sahada doğrulandı — 3 mesaj, **1 bildirim**, gövdesinde üç satır.

**Ve `Monitor` çok olay üreten monitörleri otomatik durduruyor** — yani gürültü sonunda
**sessizliğe** dönüşür. Kayıp kutu bu yüzden her turda değil, durum değişiminde bir kez
bağırılıyor. Bedeli: agent o tek bağırmayı kaçırırsa uyarı bir daha gelmez.

## Geçiş anı körlüğü — `[LEGACY-FORMAT]`

Dört uç kapanış mesajını eski araçla yazdı, yeni `watch.py` onları **`from=? type=?`**
gösterdi. Kayıp yoktu (dosya görüldü, bildirim geldi) ama **kim yazdı görünmüyordu.**

Sessiz çeviri yapılmadı: *"hangi format"* bilgisi kaybolur ve geçişin bittiği ölçülemez.

## Ham metin araması alan adlarıyla gövdeyi ayırmıyor

Bir karışma taraması 25 *"yabancı iz"* buldu ve **yanlış alarmdı** — eşleşen şey kendi
yazdığı `"alici": "clara"` alanıydı. Parse edip **gövdeye** bakınca 0 çıktı.

Aynı sınıf merkezin kendi çeviri işinde iki kez patladı: `("tur","type")` çevirisi
`return` içindeki heceyi yakaladı (`retypen`), sonra `OTURUM` bozuldu (`OMSGTYPEUM`). Ve
`OMSGTYPEUM` **geçerli Python'du** — syntax kontrolü yakalamazdı, uçtan uca koşum yakaladı.

## Sıfır bağlamlı sınama — en değerli ölçüm

Dört uç `--project` eksiğini **bulmadı**, çünkü dördü de `agent-project`'teydi. Bağlamı
olmayan bir yardımcı gördü. **Şablonun tüm örnekleri yazanın kendi bağlamını taşıyordu.**

Yardımcının kendi tespiti: *"başarımın taşıyıcısı şablonun anlatımı değil, araçların kendi
kendini anlatması oldu"* — `setup.py` kalan üç komutu mutlak yollarla basıyor.

Ve adres sorusu: *"verilmeseydi aramayı bilmezdim; sıfır bağlamla açılan bir agent için
cevap HAYIR olurdu."*

## Araç erişimi role göre değişiyor

Sıfır bağlamlı sınamada yardımcının araç listesinde `Monitor` vardı ama **`TaskOutput`
yoktu** — canlılık doğrulama adımı o ortamda koşulamadı.

Ama bunun *"role göre değişiyor"* kanıtı olmadığını ölçen uç kendisi söyledi:
*"`ToolSearch` ikisini de getirdi ama bu 'role göre değişiyor' kanıtı değil."*

## Merkezin kendi hataları — hepsi tek sınıftan

**"Yazıldı ama okunmadı":** merkez kanonda *"merkezin dinlemesi şart"* yazılıyken kendi
monitörünü kurmadı, imleç tutmadı, dört outbox'ı `ls` ile taradı ve *"outbox'ın boş"* dedi
— rapor **9 dakika** önce yazılmıştı.

**"Boş" bir ölçüm değil, okunmamış bir kutunun görünümü.**

**Ölçümün ölçtüğü şey doğrulanmadı:** çakışma testinde 100 dosya / 0 karışma görülüp
*"hedef kapandı"* dendi. Ayırt edici sinyal (zaman damgaları) eldeydi, bakılmadı — çünkü
sayım beklentiyi doğruluyordu.

---

# TARİHÇE — v2 ve öncesi (md düzeni)

Aşağıdaki ölçümler **geçerli ama yürürlükte değil.** md düzeni ve `tail -F` bırakıldı;
bu bölüm *"neden bırakıldı"* sorusunun cevabıdır. **Yeni bir karar buraya dayandırılmaz.**

## Tek yazar kuralı — md düzeninde veri bütünlüğü kuralıydı

**Aynı kutuya iki yazar:** 20 blokta **423 yabancı gövde satırı** (iki bağımsız koşum).
Bir mesajın gövde satırları başka mesajın bloğunun içine düştü.

**Tek yazarlı kutu:** karışma **sıfır** — 20 çok satırlı handoff, dört kutuya eşzamanlı
60 mesaj.

**Mekanik sebep:** POSIX `>>` atomiklik garantisi tek bir `write()` çağrısı ve `PIPE_BUF`
sınırında geçerli — bu makinede **512 bayt.** Bir handoff bunun onlarca katı olduğu için
bölünüyor. `flock` macOS'ta **yok.**

**v3'te ne değişti:** iki yazarın paylaştığı dosya kalmadı; kural veri bütünlüğü kuralı
olmaktan çıkıp **atıf ve kimlik** kuralına dönüştü.

## Monitör — md düzeninde ölçülen üç hata

**`Bash` içinde `eval 'tail -F ...'`:** süreç üretiyor, **bildirim üretmiyor.** Bir agent
böyle kurdu, *"kurdum, ölçtüm, canlıydı"* dedi — mesajlar ona hiç düşmedi. **Bu kural
v3'te de geçerli** (aracın davranışı düzenden bağımsız).

**Süreç ağacı ayırt etmiyor:** `Monitor` aracı da arka planda `zsh -c ... eval` kalıbı
kullanıyor. Ayıran şey **task kaydı.** (v3'te geçerli.)

**`TaskList` boş dönüyor, `TaskOutput` doğru:** ikisi ayrı defter. (v3'te geçerli.)

**Filtresiz `tail`:** ~30 satırlık mesaj **30 olay** üretti, monitör SIGTERM aldı
(exit 143). Filtreli hâli 90 satırı 1 olaya indirdi.

**`2>/dev/null` ile hata deseni ulaşmıyor:** stderr olay akışına girmiyor. (Filtre kuralı
v3'te de geçerli, yalnız komut değişti.)

**Paralel monitör:** beş monitör aynı anda sorunsuz çalıştı.

**Monitör ölümü bildiriliyor:** kendini `SIGTERM` ile öldüren monitör
`status: failed, exit 144` bildirimi üretti. Belgede yok, ölçümle bulundu.

## inode değişimi — md düzenine özgü

İlk ölçüm *"silinen dosya `tail -F`'i sessizce öldürüyor"* dedi (inode
50831505 → 50831506). İkinci ölçüm düzeltti: `-F` yeniden açmayı **deniyor**, ama açma
anıyla arada yazılan satırlar arasında **kayıp penceresi** kalıyor.

**v3'te konusuz:** dosyanın üzerine yazılmıyor, her mesaj ayrı dosya. Ama *"silme yasak"*
kuralı **başka gerekçeyle** duruyor: silinen mesaj sessizce gidiyor.

## Açılış kaybı

Bir mesaj 18:12'de yazıldı, monitör 18:20'de kuruldu. **Aradaki sekiz dakikada kanal
sessiz kaldı**, mesaj elden taşındı. Deneyde iki kez yaşandı.

**v3'te azaldı ama kapanmadı:** `.announced` kalıcı olduğu için yeniden kurulan izleyici
kaçırdığını bağırıyor. İlk kurulumdan önceki pencere hâlâ var.

## Biçim sapması — "oturum" tanımsız kalınca

Dört agent **üç farklı** biçimde kutu açtı:

```
-ilk                    (elle etiket, yönetici açtı)
-kanal-kurulumu         (iş adı)
-20260806-2345          (tarih-saat)
-20260806-2345          (tarih-saat — AYNI dakika)
```

Son ikisi aynı dakikada açıldı, ikisi de `2345` aldı. Sebep: şablonda `{oturum}` yazılıydı
ama **örnek verilmemişti.**

**Kapandı:** `YYYYMMDD-HHMM`, `setup.py` üretiyor. Aynı dakika çakışması `rc=1` ile
reddediliyor.

## Onaysız düzen — akıyor ama durdurulamıyor

İki agent doğrudan (yöneticisiz) konuşturuldu: 6 mesaj, ~2 dakika ritim, protokol sapması
sıfır. **Akış çalıştı.**

Ama yönetici durdurma mesajını kanala bıraktı ve **ikisi de görmedi** — her biri karşı
tarafın kutusunu izliyordu, kendi kutusunu değil.

**Sonucu:** yöneticinin gerekçesi kontrol değil **müdahale imkânı.** (v3'te geçerli.)

## Okuma maliyeti — md düzeninde

Bir `outbox` bir günde **48.409 byte / 20 mesaj** oldu. Agent her okumada tamamını
context'e alıyordu: **13.831 token.** Yalnız son mesaj okunsaydı **691 token.** Yirmi
okumada fark: **262.794 token.**

Bu ölçüm JSON düzenine geçişin ana gerekçesiydi.

## Mesaj uzunluğu

Agent'lar doğal olarak uzun yazıyor: bir testte mesaj başına ~5.600 karakter, bir
gereksinim dosyası 9.870 byte. Kanalda uzunluk sınırı yok.

## Kalıcılık boşluğu — dört bağımsız uç aynı şeyi söyledi

> *"Bunu bilmemin tek sebebi senin bu mesajı yazmış olman."*
> *"Kanal kurulumu kanonumda yok, yarın bilmeyeceğim."*
> *"Her sabah kutumu ve monitörümü talimatla kurmam gerekecek."*
> *"Bugün bunları bana sen yazdın; yarın yazan olmazsa kurulum yapılmaz."*

Ve bir düzeltme: *"sekiz agent olduğunda hiçbiri kurulumu bilmez"* **yanlış tarihli** —
**bir agent, bir sonraki oturumda** bilmiyor.

**Hâlâ açık.** v3 bunu kapatmıyor; üçüncü kez söylendi.

## JSON deposu tasarımı — geçiş öncesi ölçüm

Claude Code'un kendi task mekanizmasından öğrenilen kalıp: `.lock`, `.highwatermark`,
`{n}.json`. **Kilit gereksiz çıktı** — çakışma numara paylaşımından doğuyordu; dosya adı
`{zaman}-{yazar}.json` olursa paylaşılan hiçbir şey yok.

```
kilitli   : 30/30 dosya, sıfır çakışma, 22.2 ms/mesaj
kilitsiz  : 45/45 dosya, sıfır çakışma,  6.4 ms/mesaj
okuma     : 45 kat az byte
```

**Kenar durumlar — on senaryo, hepsi geçti.** Mikrosaniye çözünürlüğü 200 aralıksız
mesajda yetti · çok satırlı gövde + `"` + `'` + backtick + `$` + `\` + iç içe JSON
bozulmuyor · Türkçe ve emoji korunuyor (`ensure_ascii=False` şart) · 1000 dosyada
listeleme+sıralama **0.9 ms**, imleç sonrasını bulma **0.04 ms** · yanlış kutuya yazma
dosya adından yakalanıyor.

**Bu tasarım sahada sınandı ve geçti** (2026-08-07) — artık tarihçe değil, yürürlükte.

## Reddedilen alternatifler

**`SendMessage` / agent teams:** agent team **tek bir oturumun içinde** kurulur;
mailbox'lar `~/.claude/teams/{takım}/inboxes/` altında ve o yollar yalnız aynı takımın
üyelerine bilinir. **Ayrı terminalde açılan oturum hiçbir takımın üyesi değil.**

İki şey öğrenildi: Claude Code'un kendi çözümü de **dosya tabanlı**, ve onların mailbox'ı
**uçucu** — oturum bitince siliniyor. Bizimki kalıcı ve bu bir kesintiden sağ çıkmayı
sağladı.

**`memory` MCP'si:** oturumlar arası paylaşılıyor (ölçüldü) ama deposu yine dosya
(`memory.jsonl`) ve varsayılan yolu **npx cache'inin içi** — cache temizlenirse veri
kaybolur.

**`CronCreate`:** agent açmıyor, **prompt zamanlıyor.** Oturum kapanınca siliniyor, 7 gün
ömrü var.

## Belge yetersizliği

Resmî dokümantasyon (`code.claude.com/docs/en/tools-reference.md`) `Monitor` hakkında
**7 sorudan 5'ini** cevaplamıyor: paralel monitör sınırı, `persistent` ömrü, ölüm
bildiriminin garantisi, olay hızı sınırının sayısı, macOS'ta dizin izleme yöntemi.

**Sonucu:** skill'deki monitör kuralları **ölçüme** dayanıyor, belgeye değil. Araç sürümü
değişirse yeniden ölçülmeli. (v3'te geçerli.)
