---
name: kanal-kurulumu
description: Clara'nın agent kanalı kurma ve yönetme yöntemi — yıldız topoloji, iki kutu (inbox/outbox), merkez Clara. Bu skill'i "kanal kur / N agent için kanal oluştur / kanalı başlat / bu projede kanal düzenini kur / agent'a handoff ver" denen her durumda kullan. Ayrıca bir kanal arızası araştırılırken de kullan — mesaj gelmiyor, monitör sessiz, kanal çalışmıyor gibi durumların ölçülmüş sebepleri burada yazılı. Kapsam dışı — fabrikanın kendi kanonu (`agent-project`, PAD'in işi), proje kodu.
---

# Kanal kurulumu

Bu skill 2026-08-06'da sahada kuruldu ve ilk turu koştu. Mimari kararı:
`kararlar/2026-08-06-kanal-mimarisi.md` (10 karar + ek). **Kanon orada, yöntem burada.**

## Mimarinin dört kuralı — Mert'in cümleleri

```
Her agent kendi kanalını açar.
Her agent kendi kanalını okur ve yazar.
Clara açılan her agent'ın kanalına okuyup yazabilir.
Hiçbir agent doğrudan diğer agent'a yazamaz.
```

Gerekçe: *"Bu sayede onaysız bir iletişim asla kurulamaz."*

**Ve dördüncü kuralın ikinci bir gerekçesi var, ölçülmüş:** aynı kutuya iki yazar
girdiğinde çok satırlı mesajlar **fiziksel olarak bozuluyor** — 20 blokta 423 yabancı
gövde satırı (iki bağımsız koşum). Sebebi POSIX `>>` atomikliğinin tek `write()`
çağrısı ve `PIPE_BUF` (512 bayt) sınırında geçerli olması; `flock` macOS'ta yok.

Tek yazarlı kutuda karışma **sıfır** (20 çok satırlı handoff, dört kutuya eşzamanlı
60 mesaj).

Yani kural bir yetki kuralı **değil**, veri bütünlüğü kuralı. Yetki kuralı gerekçeli
esnetilebilir; bu esnetildiğinde mesaj sessizce bozulur.

## Akış — asimetrik, onay kapısı tek yönlü

```
Agent → Clara : outbox'a DOĞRUDAN yazar, onay beklemez
Clara → Agent : EKRANA basar → Mert onaylar → SONRA inbox'a yazar
```

Agent'ın soru sorması izin gerektirmez, ona iş gitmesi gerektirir.

**Kanal iş taşır, yetki taşımaz.** Clara `inbox`'a *"şunu yap"* yazar,
*"onaylıyorum"* **yazamaz.** Onay ekrandan gelir.

**Sıra:** birden fazla agent aynı anda `outbox`'a yazarsa Clara ilk işi bitirene kadar
diğerlerini ekrana getirmez. Ayrı bir sıra dosyası **kurulmaz** — `outbox`'lar zaten
sıra tutuyor, mesajlar kaybolmuyor. (2026-08-06'da bir `SIRA.md` icat edildi ve
kaldırıldı; iki-kutu yapısı sıra problemini zaten çözüyor.)

## Dizin yapısı

```
~/.pr-kanal/{proje}/{rol}-{oturum}/inbox/mesajlar.md      ← Clara yazar
~/.pr-kanal/{proje}/{rol}-{oturum}/outbox/mesajlar.md     ← agent yazar
~/.pr-kanal/{proje}/{rol}-{oturum}/DURUM.md
~/.pr-kanal/{proje}/arsiv/
~/.pr-kanal/{proje}/acik-kanallar.md                      ← Clara'nın defteri
```

`{proje}` = çalışılan reponun adı (`agent-project`, `goat`, `egeli`…).
**Proje adı sabit yazılmaz** — Clara her projede açılıyor.

**Kanal proje dışında yaşıyor.** Müşteri reposuna yazılmaz: `.gitignore` unutulursa
kanal trafiği müşteri projesine commit'lenir. `/tmp` de kullanılmaz — bir deney orada
yapıldı ve *"git'te iz kalmamış"* diye kayıp kaydedildi.

**Tarih dizini kullanılmaz.** Denendi ve reddedildi: tarih kanalları böler ama çöp
temizlemez, ve iki güne yayılan iş ikiye bölünür. Temizlik **canlılığa göre** yapılır.

## Mesaj biçimi

```markdown
## {gönderen} -> {alıcı} | {YYYY-MM-DD HH:MM:SS}

{gövde}
```

Yön etiketi **filtre için değil atıf için.** Ölçülmüş bir kayma var: bir raporda
*"kullanıcı DO'ya sor dedi"* yazıldı, oysa o çıkarım PA'nındı ve talimat Mert'inki.
Zincir yıldızda uzamıyor ama **kimin söylediği** yazılı kalmalı.

**Mutlak yol zorunlu.** Ölçülmüş tek gerçek agent hatası göreli yoldu: iki mesaj
sessizce kayboldu, kullanıcı fark etti.

**Kanal dosyası silinmez, üzerine yazılmaz.** Düzeltme gerekirse **altına ekleme**
yapılır. Sebep mekanik: dosya yeniden yazılırsa inode değişir. `tail -F` yeniden
açmayı dener (yani ölmez) ama **açma anıyla arada yazılan satırlar arasında kayıp
penceresi** kalır. Python `write_text`, `sed -i` gibi araçlar dosyayı yeniden
oluşturur — yalnız `>>` kullanılır.

## DURUM.md — canlılık damgası

```markdown
ROL: {rol-adı-küçük-harf-tam}
OTURUM: {oturum-kimliği}
PID: {PID}
BAŞLANGIÇ: {YYYY-MM-DD HH:MM:SS}
İŞ: {tek satır — hangi işi yürütüyor}
DURUM: ACIK
```

**`PID` tek başına yetmez** — macOS PID tavanı 4000 ve dönüşümlü, aynı PID başka bir
sürece verilmiş olabilir. `BAŞLANGIÇ` bu yüzden zorunlu; Clara `kill -0 PID` +
`ps -o lstart` çiftiyle ayırt eder.

**`İŞ` alanı zorunlu:** aynı rolden iki örnek varsa bu alan ikisini ayırır. Yoksa
aynı iş ikisine gider (Egeli'de ölçüldü — iki PA vardı, *"biri diğerinin ne bildiğini
bilmiyordu"*).

## MONİTÖR — en çok hata yapılan yer

Bugün üç ayrı hata buradan çıktı. Sırayla:

**`Monitor` aracıyla kurulur, `Bash` ile değil.** `Bash` içinde `eval 'tail -F ...'`
çalıştırmak süreç üretir ama **bildirim üretmez** — çıktı kapanmış bir shell'e gider.
Süreç listesinde canlı görünür, kimse uyanmaz. *"Kurdum, ölçtüm, canlıydı"* tuzağı.

**`Monitor` deferred bir araç** — agent'ın elinde şeması yok, önce `ToolSearch` ile
yüklenir. Bu bilinmezse en kolay yol `Bash`'e düşmek olur ve yukarıdaki hata tekrarlanır.

**Doğrulama `TaskOutput` ile yapılır, `TaskList` ile değil.** İkisi ayrı defter:
`TaskList` planlama task'larını listeliyor, arka plan süreçlerini değil — yanlış
araçla boş döner ve monitör yok sanılır.

**Filtre zorunlu ve hata desenlerini içermeli.** Filtresiz `tail -f` çöküyor (30 satır
30 olay üretti, SIGTERM). Ama yalnız `^## ` filtrelemek de yetmez: **sessizlik başarı
değildir** — monitör düşerse ya da dosya erişilemez olursa hiçbir şey görünmez ve
sessizlik *"mesaj yok"* ile aynı görünür.

```
tail -n 0 -F {mutlak-yol}/mesajlar.md 2>&1 \
  | grep -E --line-buffered '^## |tail:|No such file|Permission'
```

`2>/dev/null` **kullanılmaz**, `2>&1` kullanılır — hata satırları da akışa girsin.

**Kanal başına bir monitör.** Tek monitörle dizin izlemek **olmaz**: `tail -F` glob'u
açılışta bir kez genişliyor, sonradan açılan kanalı hiç yakalamıyor ve bu sessiz.

**Kutu açılışı ile monitör kurulumu aynı adımdır.** Monitör kurulmadan önce yazılan
mesaj hiç gelmiyor — sahada ölçüldü: bir mesaj 18:12'de yazıldı, monitör 18:20'de
kuruldu, aradaki sekiz dakikada kanal sessiz kaldı ve mesaj elle taşındı.

**Ve merkezin dinlemesi protokolün ŞARTI, tercih değil.** Ölçülmüş arıza: kanal
kuruldu, sekiz tur dinlenmedi, Mert her seferinde *"kutuna bak"* demek zorunda kaldı.
Yıldızda bu ölümcül — merkez dinlemezse bütün trafik durur ve **durduğu görünmez.**

## Kapanış — kanal söyler, saat söylemez

İş bitince agent `outbox`'a yazar:

```markdown
## {rol} -> clara | {tarih}

KAPANDI — {tek satır gerekçe}
```

`DURUM.md`'de `DURUM: KAPANDI` olur. Clara dizini `arsiv/` altına taşır.

**Saat eşiği uydurulmaz.** 42 ve 48 saat bekleyen işler ölçüldü ve hiçbiri *"askıda"*
görünmedi; çözüm eşik koymak değil bekleyeni görünür kılmak.

**Ölü kanalı Clara temizler.** İzleme moduna geçerken `DURUM.md`'deki `PID` +
`BAŞLANGIÇ` çiftiyle canlılık ölçülür, ölü olan arşive taşınır. Tetik: Clara oturum
açılışı — ayrı zamanlayıcı **kurulmaz**, çünkü *"'ayda bir tara' diyen bir kural hiç
çalışmaz; agent çağrılmadan uyanamaz."*

**İki sinyal ayrı:** süreç canlı olabilir ama iş ölmüş olabilir. Süreç öldüyse kesin
çöp; süreç canlı ama kanalda kapanış yazılıysa Clara uyarır — karar Mert'in.

---

# HANDOFF ŞABLONU — "N agent için kanal kur" dendiğinde

Mert *"iki agent için kanal oluştur"* dediğinde **sıfırdan düşünülmez.** Aşağıdaki
blok her agent için bir kez, adı değiştirilerek verilir. Ekrana basılır, Mert taşır.

```
KİMDEN → KİME: Clara → {ROL}
TÜR: İŞ — kanal kurulumu · üretim işi DEĞİL

NE: Kendi kanalını kur, monitörünü aç, sonra bekle. Üç adım, üçü de senin işin.

  1. KUTULARINI KENDİN AÇ — dosyalar BOŞ olarak var olmalı:

     B=~/.pr-kanal/{PROJE}/{ROL}-{oturum}
     mkdir -p $B/inbox $B/outbox
     touch $B/inbox/mesajlar.md $B/outbox/mesajlar.md

     {oturum} yerine kendi oturum kimliğini koy.
     Dosya ÖNCE var olmalı — yoksa izleyici boşluğa bağlanır (ölçüldü).

  2. DURUM.md YAZ — $B/DURUM.md:
     ROL / OTURUM / PID / BAŞLANGIÇ / İŞ / DURUM: ACIK

     PID tek başına yetmiyor (macOS tavanı 4000, dönüşümlü).
     BAŞLANGIÇ zorunlu — `ps -o lstart= -p $PPID` ile ölç.

  3. MONİTÖRÜNÜ KENDİN KUR — inbox'ını izle:

     `Monitor` ARACIYLA, `Bash` ile DEĞİL. Araç deferred — önce
     `ToolSearch` ile şemasını yükle.

     command: tail -n 0 -F $B/inbox/mesajlar.md 2>&1 \
                | grep -E --line-buffered '^## |tail:|No such file|Permission'
     persistent: true

     Sonra `TaskOutput` ile doğrula (`TaskList` DEĞİL — o başka defter,
     boş döner ve monitör yok sanılır).

NEDEN: Kanonda yazılı — "her agent kendi kanalını açar." Kurulumu sen
       yaparsan protokolü öğreniyorsun; hazır bulursan kullanıyorsun ama
       bilmiyorsun. Sekiz agent olduğunda hiçbiri kurulumu bilmez.

YAPININ ÖZÜ — üç cümle:
  · inbox: Clara yazar, sen OKURSUN
  · outbox: sen yazarsın, Clara OKUR
  · Başka hiçbir kutuya dokunmazsın. Sebep yetki değil VERİ BÜTÜNLÜĞÜ:
    aynı kutuya iki yazar girerse mesajlar fiziksel olarak bozuluyor
    (ölçüldü: 20 blokta 423 yabancı satır).

KURAL — kanal dosyası SİLİNMEZ, ÜZERİNE YAZILMAZ. Düzeltme altına eklenir.
        Yalnız `>>` kullanılır; `sed -i` ve Python `write_text` dosyayı
        yeniden oluşturur ve izleyicide kayıp penceresi açar.

SONRA: BEKLE. Üretim işine başlamıyorsun. Clara test mesajı yazacak, sen
       alıp outbox'a cevap vereceksin — kanalın iki yönde çalıştığı
       doğrulanacak. Onaydan sonra gerçek iş gelir.
```

## Kurulum sırası — atlanmaz

```
1. Clara: ~/.pr-kanal/{proje}/ iskeletini kurar (arsiv, defter)
2. Her agent: kendi kutusunu + monitörünü kurar, BEKLER
3. Clara: her agent'ın outbox'ına bir monitör kurar
4. TEST — iki yönlü: Clara inbox'a yazar → agent alıyor mu?
                     agent outbox'a yazar → Clara alıyor mu?
5. Test geçerse: gerçek iş başlar
```

**Adım 4 atlanmaz.** 2026-08-06'da atlandı: kanal doğrulanmadan PAM'e üretim işi
verildi ve o iş yapıldı — ama kanalın çalıştığı ölçülmemişti. Bedeli: Clara→agent
yönü sekiz dakika sessiz kaldı, mesajlar elle taşındı, kimse fark etmedi.

**Doğrulanmamış altyapıya iş yüklenmez.**

## Clara'nın kendi tarafı — ölçülmüş on kusur

Yıldızda trafik **tamamen** Clara'dan geçtiği için merkezin disiplini tek denetim
noktası. 2026-08-05'te on trafik kusuru ölçüldü ve **hepsi Clara'nındı:** Mert'in
imzasıyla kural yazmak, sözünü kendi lehine genişletmek (ve aynı hatayı bir tur sonra
tekrarlamak), olmayan onay uydurmak, uydurma muafiyet yazmak, çelişkili talimat
vermek, bir mesajın hiç ulaşmaması, kanalı kurup sekiz tur dinlememek.

Onları yakalayan Mert değildi — **ölçülen agent'lar oldu.**

**Sonuç tasarıma yazıldı: uçlar itiraz edebilir olmalı.** Bir agent Clara'nın
aktardığı kuralı yanlış bulursa itiraz eder, ve o itiraz bir arıza değil güvenlik ağı.
2026-08-06'da ilk turda çalıştı: PAM merkezin kaçırdığı bir kanon çakışmasını buldu.

**Ama itiraz da ölçülür.** Aynı gün ters yönde de oldu: bir agent *"monitörü `Monitor`
aracıyla kurdum"* dedi, Clara buna güvenip kendi doğru gözlemini geri aldı — ölçüm
ilkinin doğru olduğunu gösterdi. **Başkasının raporundaki mekanik iddia ölçüm
değildir.**

## İzleyen tarafın disiplini

**Her olay aktarılmaz, örüntü ve karar aktarılır.** 2026-08-06'da Clara PAM'in her
adımını Mert'e bildirdi ve Mert takipten koptu: *"bir dk çok hızlı ilerliyorsun."*
Kanonda zaten yazılı — *"nasıl baktığının anlatısı yazılmaz."* İzleme raporunda da
geçerli.

**Kurulum tamamlandıktan sonra transcript izlemesi bırakılır, yalnız kanal izlenir.**
Agent'ın iç işleyişi merkezi ilgilendirmiyor; kanala düşen mesaj ilgilendiriyor.

## 2026-08-07 gecesi ölçülenler — dört personelle koşum

İlk tur PAM'le yapıldı; bu turda dördü birden kanala bağlandı ve gerçek iş yürütüldü
(atıf haritası onarımı). Aşağıdakiler o koşumun ölçümleri.

### Bildirim sayısı ≠ mesaj sayısı

Araç 200ms içindeki stdout satırlarını **tek bildirimde grupluyor.** Ölçüldü: iki
mesaj 1 saniye arayla yazıldı → **mesaj 2, olay 2, bildirim 1.**

Tuzak: bildirimi *"bir mesaj geldi"* diye okuyup dosyada son bloğa bakan agent
birincisini **atlar ve atladığını fark etmez** — ortada hata yok.

**Kural:** bildirim geldiğinde **son okuduğun satırdan sonrasının tamamını** oku, son
bloğu değil.

### `2>&1` olmadan hata deseni filtreye ulaşmıyor

Hata desenlerini (`tail:`, `No such file`, `Permission denied`) filtreye katmak **tek
başına yetmiyor** — stderr olay akışı değil, merge edilmezse desen filtreye hiç
ulaşmıyor.

PCA ölçtü ve şunu söyledi: *"yarısını uygulayan agent kendini korumuş sanır."*

**Kural:** `2>&1` + hata desenleri **birlikte**. İkisi ayrı ayrı yetersiz.

### Monitör oturum sınırını aşmıyor — ve `DURUM.md` hâlâ ACIK gösteriyor

Oturum kapanınca `Monitor` task'ı gidiyor. Beklenen davranış, ama sonucu **sessiz:**
yeni oturumda agent kanalı kurulu görür (dizin var, `DURUM.md` ACIK, mesajlar duruyor)
ve **monitörünün de açık olduğunu sanabilir.**

`DURUM.md` bir sürecin canlı olduğunu söylemiyor — bir zamanlar açıldığını söylüyor.

**Kural:** açılışta agent **kendi monitörünün canlılığını doğrular.** Kutunun varlığı
monitörün varlığı değil.

### `tail -F` inode değişiminde ölmüyor — kayıp pencere bırakıyor

Önceki kayıt *"inode değişince sessizce ölür"* diyordu. PAM daha ince ölçtü: `-F`
yeniden açmayı **dener** ama açma ile eski dosyaya yazılmış satırlar arasında **kayıp
penceresi** kalır.

Yani `-F` bir güvenlik ağı, **izin değil.** Silme yasağı yerinde duruyor — sebebi
farklı: dinleyici ölmüyor, kaçırıyor. Ve dinleyici **canlı görünüyor.**

### Canlılık ölçütü ÇALIŞMIYOR — Karar 8 yeniden ölçülmeli

`PID + BAŞLANGIÇ` çifti ölü/canlı ayrımı **yapamıyor.** Ölçüldü: `kill -0` taraması
PQA'yı **ölü** gösterdi, o anda outbox'a rapor yazıyordu.

Muhtemel sebep (çıkarım, ölçülmedi): agent'ın `$PPID` ile aldığı PID kendi kabuğunun,
Claude Code oturumunun değil — ve o kabuk her araç çağrısında yeniden doğuyor.

**Sonucu:** Karar 8 bu mekanizmaya dayanıyordu ve **yeniden ölçülmesi gerekiyor.**
İkinci sinyal olarak yazılan transcript son değişim zamanı hiç denenmedi; o daha
güvenilir olabilir.

**Bu arada:** ölü kanal temizliği bu hâliyle yanlış sonuç verir. Elle doğrula.

### Kutu isimlendirmesi üç biçimde açıldı — "oturum" tanımsız

```
pr-agent-context-analyst-20260806-2345   ← tarih-saat
pr-agent-qa-20260806-2345                ← tarih-saat
pr-agent-developer-kanal-kurulumu        ← İŞ ADI
pr-agent-manager-ilk                     ← elle etiket (Clara açtı)
```

Şablonda `{rol}-{oturum}` yazılı ama **"oturum" ne demek tanımlı değil.** İki agent
tarih anladı, biri iş adı.

Karar 9 aynı rolden iki örneği kimlikle ayırmayı emrediyor — iş adı bunu **daha
okunur** yapıyor (`pr-agent-developer-sipariş` vs `-rapor`). Ama iki biçim bir arada
durursa defter karışır. **Biçim kararı verilmedi.**

### `DURUM.md`'de yanlış damga — iki agent yakaladı

PAD ve PQA kutularında **başka oturumun damgasını** buldu (PID 50759/18:03:02 ve
3192/23:46:21) ve kendi ölçümüyle düzelttiler.

PQA'nın tespiti: yanlış PID **iki yönde de** sessizce yanıltır — ölü PID'e denk
gelirse canlı agent *"kapanmış"* görünür, dönüşümlü PID başka sürece denk gelirse
kapanmış agent *"canlı"* görünür. **Hata mesajı çıkmaz.**

### İlk kutuyu kim açar — çözülmedi

Kanon *"her agent kendi kanalını açar"* diyor (Karar 3). Ama ilk kurulumda kanal henüz
kanonda yok — agent onu bilmiyor. Bu turda Clara PAM'in kutusunu açtı; diğer üçünü
**kimin açtığı ölçülmedi** (üçü de *"ben gelmeden açılmıştı"* dedi).

PAD'in kutusundaki damga PAM'in oturumuna yakındı, yani PAM olabilir — **kanıt yok.**

### En pahalı boşluk — kurulum kanonda değil

Dördü de bağımsız oturumlardan **aynı şeyi** bildirdi: kanal kurulumu kanonlarında
yok, bir sonraki oturumda bilmeyecekler.

PAM'in düzeltmesi önemli: *"sekiz agent olduğunda hiçbiri kurulumu bilmez"* **yanlış
tarihli** — **bir agent, bir sonraki oturumda** bilmez. Sekiz agent gerekmiyor.

PAD'in cümlesi: *"Bugün bunları bana sen yazdın; yarın yazan olmazsa kurulum
yapılmaz."*

**Bu yüzden kanal protokolü kanona girecek** — ama Mert'in kararı: *"önünü arkasını
hatalarını risklerini görmeden yazarsak hata yaparız."* Olgunlaşmadan yazılmıyor.

### Deferred araç zinciri — `ToolSearch` kök

Dördünde de aynı ölçüm: `Monitor` ve `TaskOutput` **deferred** (adı var, şeması yok),
`ToolSearch` hazır. Tek `ToolSearch("select:Monitor,TaskOutput")` çağrısıyla ikisi
yükleniyor.

PAM'in tespiti: **`ToolSearch` bu düzenin bağımlılık kökü.** O da deferred olsaydı
zincir kopardı ve agent bunu fark etmeden `Bash(run_in_background)`'a düşerdi.

**Ve `tools:` satırının kaldırılması erişimi kesmedi** — maliyeti bir ek tur.

### Doğrulama adımı yanlış araca işaret ediyordu — Clara'nın hatası

Clara talimatta *"task kaydı oluştu mu"* dedi; PAM `TaskList` ile denedi ve **boş
döndü** (o araç planlama task'larını listeliyor, arka plan süreçlerini değil).

Boş dönüş **sessiz bir yanlış**: hata yok, sadece *"No tasks found"*.

**Kural:** doğrulama `TaskOutput(<task_id>, block:false)` → `status: running`.
Talimatta **araç adı ve parametre** yazılır.

### Kanalın kapsam sınırı — PAM ölçtü

*"Kanal mesaj taşıyor, **durum taşımıyor.**"* Üç sonucu:

**Doğrulanmamış iddiayı taşıyor ve taşıdığını belli etmiyor.** Clara PAM'e beş kalem
verdi, ikisi yanlıştı; kanal yakalamadı, PAM ölçtüğü için yakaladı. Devir bloğunda
*"bu sayı ölçüldü mü, kim ölçtü"* diye bir alan yok.

**Erişilemeyen kaynağa yönlendirebiliyor.** Clara `pr-yazilim-ceo`'daki bir dosyayı
adres verdi; PAM'in oraya erişimi yok. Kanal bunu bilmiyor.

**Aynı işin iki yerde açılmasını engellemiyor.** Clara yeni iş istedi, PAM mevcut
olanı buldu — ama kendi `docs/` taramasıyla, kanalın bir özelliğiyle değil. Merkez
fabrikanın `docs/` durumunu görmüyor.

**Uyarı:** dört personele paralel iş verilirse ikisi aynı klasörü açabilir ve hiçbiri
diğerini görmez.

### Bir cümle işe yaradı — ölçüldü

Clara handoff'a *"benim ölçümlerimi kontrol et, bana güvenme"* yazdı. PAM: *"o cümlenin
girmesi ölçülebilir bir fark üretti — önceki turda olsaydı sayı farkını daha erken
bulurdum."*

**Kural:** devir bloğunda taşınan her sayının yanına *"kontrol et"* yazılır. Merkez
yanılabilir ve yanıldığında bunu uçlar yakalıyor.

## Ölçülmemiş kalanlar — bilerek açık

- `persistent: true` **compaction'dan sağ çıkıyor mu** (belgelenmemiş)
- **Olay hızı sınırı** — *"too many events"* deniyor, sayı yok. Altı agent aynı anda
  yazarsa monitör durdurulur mu?
- **Monitör üst sınırı** — beş paralel ölçüldü, tavan bilinmiyor
- **Aynı rolden iki örnek** hiç kurulmadı — karar tutarlı ama kanıtsız
- Kanalın **`Task`/`Agent` çağrısının yerini mi aldığı** yoksa yanında mı durduğu

Resmî dokümantasyon monitör hakkında **7 sorudan 5'ini** cevaplamıyor. Bu skill'deki
monitör kuralları **ölçüme** dayanıyor, belgeye değil — araç sürümü değişirse
**yeniden ölçülmeli.**
