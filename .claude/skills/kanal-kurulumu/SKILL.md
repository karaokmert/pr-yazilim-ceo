---
name: kanal-kurulumu
description: Clara'nın agent kanalı kurma ve yönetme yöntemi — yıldız topoloji, yönetici merkezde, her agent'ın inbox/outbox kutusu, JSON düzeni ve beş Python betiği. Bu skill'i "kanal kur / N agent için kanal oluştur / kanalı başlat / bu projede kanal düzenini kur" denen her durumda kullan. Ayrıca bir kanal arızası araştırılırken de kullan — mesaj gelmiyor, monitör sessiz, kanal çalışmıyor gibi durumların sebepleri ve ayırt edici testleri burada. Kapsam dışı — fabrikanın kendi kanonu (`agent-project`, PAD'in işi), proje kodu.
---

# Kanal kurulumu

Bu skill **yöneticinin işini** taşır: kanal nasıl kurdurulur, nasıl izlenir, arıza nasıl
ayırt edilir.

**Düzen v3 — JSON, mesaj başına dosya, beş betik.** md düzeni (tek dosyaya `>>` ile
ekleme), `tail -F` ile izleme ve elle kurulum **bırakıldı.** Üçü de ölçümle çürütüldü.

## Üç kaynak — hangisi neyi söyler

```
~/.pr-kanal/{proje}/SABLON-JSON.md   NEDEN böyle · kuralların ölçüm gerekçesi
~/.pr-kanal/{proje}/tools/           NASIL yapılır · betikler kendi kullanımını basar
bu skill                             KİM ne yapar · yöneticinin disiplini
references/olcumler.md               KANIT · hangi kural hangi ölçümden çıktı
```

**Şablon burada tekrar edilmez.** Bir kuralın ölçüm ayrıntısı gerektiğinde şablon açılır;
buraya kopyalanırsa iki kaynak ayrışır ve hangisinin yürürlükte olduğu belirsizleşir.

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

`setup.py --project` verilmezse varsayılan **`agent-project`.** Yani başka bir proje için
kanal kuran agent bayrağı atlarsa kutusu **fabrikanın dizinine** düşer, `rc=0` alır ve
**fark etmez.**

**Kural: `--project` her zaman yazılır**, `agent-project` olsa bile. Açıkça yazılmış
varsayılan bir karardır; atlanmış varsayılan bir boşluktur.

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

> ⚠️ `SABLON-JSON.md` kapanış örneğinde `KAPANIS` yazıyor ve o komut **çalışmaz.**
> Şablon hatası, PAD'e bildirildi. Doğrusu `CLOSE`.

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

  ARAÇLAR: ~/.pr-kanal/{PROJE}/tools/
  DÜZEN  : ~/.pr-kanal/{PROJE}/SABLON-JSON.md   ← neden böyle olduğu burada

  1. KUTUNU KUR — elle mkdir YOK:

     A=~/.pr-kanal/{PROJE}/tools
     python3 $A/setup.py {ROL} --task "{TEK SATIR İŞ}" --project {PROJE}

     `--project` ZORUNLU. Atlanırsa varsayılan `agent-project` olur, kutun
     yanlış projeye düşer, rc=0 alırsın ve FARK ETMEZSİN.

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
