---
name: kanal-kurulumu
description: Clara'nın agent kanalı kurma ve yönetme yöntemi — yıldız topoloji, yönetici merkezde, her agent'ın inbox/outbox kutusu. Bu skill'i "kanal kur / N agent için kanal oluştur / kanalı başlat / bu projede kanal düzenini kur" denen her durumda kullan. Ayrıca bir kanal arızası araştırılırken de kullan — mesaj gelmiyor, monitör sessiz, kanal çalışmıyor gibi durumların sebepleri ve ayırt edici testleri burada. Kapsam dışı — fabrikanın kendi kanonu (`agent-project`, PAD'in işi), proje kodu.
---

# Kanal kurulumu

Bu skill **yöntemi** taşır: ne yapılır, hangi sırayla, neden.

Kanıt ve ölçümler: `references/olcumler.md` · karar gerekçeleri:
`kararlar/2026-08-06-kanal-mimarisi.md`

## Yapı — tek cümlede

**Her kanalın bir yöneticisi vardır, her agent'ın iki kutusu olur, her kutunun tek
yazarı vardır.**

```
Yönetici → her agent'ın inbox'ına YAZAR, outbox'ını OKUR
Agent    → kendi outbox'ına YAZAR, kendi inbox'ını OKUR
Agent → Agent : YOK
```

**Neden tek yazar:** aynı dosyaya iki taraf yazdığında çok satırlı mesajlar iç içe
giriyor — bir mesajın gövde satırları başka mesajın bloğuna düşüyor. `>>` atomiklik
garantisi tek bir `write()` çağrısı ve `PIPE_BUF` sınırında geçerli; bir handoff bunun
katı olduğu için bölünüyor. `flock` macOS'ta yok, kilitle çözülmüyor.

Sonucu: bu bir yetki kuralı değil **veri bütünlüğü** kuralı. Yetki kuralı gerekçeli
esnetilebilir; bu esnetildiğinde mesaj **sessizce** bozulur.

**Neden yönetici zorunlu:** yönetici olmadan da akış çalışır, ama **durdurulamaz.** Uçlar
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

**Kanal iş taşır, yetki taşımaz.** Yönetici `inbox`'a *"şunu yap"* yazar,
*"onaylıyorum"* yazamaz. Onay ekrandan gelir.

**Sıra için ayrı dosya kurulmaz.** Birden fazla agent aynı anda yazarsa `outbox`'lar zaten
sıra tutuyor; yönetici ilk işi bitirene kadar diğerlerini ekrana getirmez.

## Kurulum sırası — atlanmaz

```
1. Yönetici iskeleti kurar     (~/.pr-kanal/{proje}/ + arsiv/ + defter)
2. HER AGENT kendi kutusunu ve monitörünü kurar, sonra BEKLER
3. Yönetici her outbox'a bir monitör kurar
4. İKİ YÖNLÜ TEST
5. Test geçerse gerçek iş başlar
```

**2. adım neden agent'ın işi:** kurulumu yapmayan agent protokolü öğrenmiyor, hazır bulup
kullanıyor — ve bir sonraki oturumda bilmiyor.

**4. adım neden atlanmaz:** doğrulanmamış altyapıya iş yüklenirse iş yapılır ama bir yön
sessiz kalabilir; mesajlar elden taşınır ve kimse fark etmez. Sonra sıra baştan kurulur.

## Dizin yapısı

```
~/.pr-kanal/{proje}/{rol}-{oturum}/inbox/mesajlar.md      ← yönetici yazar
~/.pr-kanal/{proje}/{rol}-{oturum}/outbox/mesajlar.md     ← agent yazar
~/.pr-kanal/{proje}/{rol}-{oturum}/DURUM.md
~/.pr-kanal/{proje}/arsiv/
~/.pr-kanal/{proje}/acik-kanallar.md                      ← yöneticinin defteri
```

`{proje}` = çalışılan reponun adı. Sabit yazılmaz — yönetici her projede açılıyor.

**Kanal proje dışında yaşar.** Müşteri reposuna yazılmaz: `.gitignore` unutulursa kanal
trafiği projeye commit'lenir. `/tmp` de kullanılmaz, uçucu.

**Tarih dizini kullanılmaz.** Kanalları böler ama çöp temizlemez, ve iki güne yayılan iş
ikiye bölünür. Temizlik canlılığa göre yapılır.

**`{oturum}` biçimi — açık kalem.** Tanımı verilmediği için sahada üç ayrı biçimde açıldı
ve ikisi aynı dakikada çakıştı. İki aday var: **PID** (tekil, `DURUM.md`'de zaten yazılı)
ya da **iş adı** (aynı rolden iki örneği daha okunur ayırıyor). Bir biçim seçilmeli — iki
biçim bir arada durursa adres tahmin edilemez.

**Ve bir biçim kuralı örneksiz yazılmaz.** Örnek verilmezse her okuyucu kendi yorumunu
yapar, yanlış biçim düzeltilmez — **yayılır.**

## Mesaj biçimi

```markdown
## {gönderen} -> {alıcı} | {YYYY-MM-DD HH:MM:SS}

{gövde}
```

**Yön etiketi filtre için değil atıf için.** Başkasının çıkarımı *"kullanıcı dedi"* diye
aktarılabiliyor; kimin söylediği yazılı kalmazsa zincir uzadıkça iddia güçlenir ama
dayanağı zayıflar.

**Mutlak yol zorunlu.** Göreli yol kullanıldığında mesaj sessizce kaybolabilir.

**Kanal dosyası silinmez, üzerine yazılmaz.** Düzeltme **altına eklenir**, yalnız `>>`
kullanılır. Sebep: dosya yeniden yazılırsa inode değişir; `tail -F` yeniden açmayı
**dener** — yani ölmez — ama açma anıyla arada yazılan satırlar arasında **kayıp
penceresi** kalır, ve dinleyici bu sırada **canlı görünür.** Python `write_text`, `sed -i`
gibi araçlar dosyayı yeniden oluşturur.

## DURUM.md

```markdown
ROL: {rol-adı-küçük-harf-tam}
OTURUM: {oturum-kimliği}
PID: {PID}
BAŞLANGIÇ: {YYYY-MM-DD HH:MM:SS}
İŞ: {tek satır}
DURUM: ACIK
```

`İŞ` alanı zorunlu: aynı rolden iki örnek varsa bu alan ikisini ayırır, yoksa aynı iş
ikisine gider.

**`DURUM` bir beyandır, ölçüm değil** — bir sürecin canlı olduğunu söylemiyor, bir
zamanlar açıldığını söylüyor. Agent güncellemezse kapanmış oturumun kutusu `ACIK` kalır.

**Damga kendi ölçümüyle yazılır, devralınmaz.** Kutuda başka oturumun damgası kalırsa iki
yönde de sessizce yanıltır: canlı agent *"kapanmış"*, kapanmış agent *"canlı"* görünür.

## Monitör — en çok hata yapılan yer

**`Monitor` aracıyla kurulur, `Bash` ile değil.** `Bash` içinde `eval 'tail -F ...'`
çalıştırmak süreç üretir ama **bildirim üretmez** — süreç listesinde canlı görünür, kimse
uyanmaz.

**`Monitor` ve `TaskOutput` deferred araçlardır** — adı var, şeması yok. `ToolSearch` ile
yüklenir, tek çağrı ikisini getirir. **`ToolSearch` bu düzenin bağımlılık kökü:** o da
deferred olsaydı zincir kopardı ve agent fark etmeden `Bash`'e düşerdi.

**Doğrulama `TaskOutput` ile yapılır, `TaskList` ile değil** — ikisi ayrı defter, yanlış
araçla boş döner ve monitör yok sanılır. **Süreç ağacına bakmak da ayırt etmiyor**;
ayıran şey task kaydı.

**Filtre zorunlu, ve `2>&1` ile hata desenleri BİRLİKTE gerekir:**

```
tail -n 0 -F {mutlak-yol}/mesajlar.md 2>&1 \
  | grep -E --line-buffered '^## |tail:|No such file|Permission'
```

Filtresiz `tail` çok olay üretip monitörü düşürüyor. Ama yalnız başlık filtrelemek de
yetmez: **sessizlik başarı değildir** — monitör düşerse hiçbir şey görünmez ve sessizlik
*"mesaj yok"* ile aynı görünür. Ve ikisi ayrı ayrı yetersiz: stderr olay akışı değil,
`2>&1` olmadan hata deseni filtreye hiç ulaşmaz.

**Kanal başına bir monitör.** Tek monitörle dizin izlenmez: `tail -F` glob'u açılışta bir
kez genişliyor, sonradan açılan kanalı hiç yakalamıyor ve bu sessiz.

**Kutu açılışı ile monitör kurulumu aynı adımdır.** Monitör kurulmadan önce yazılan mesaj
hiç gelmiyor.

**Monitör oturum sınırını aşmaz.** Oturum kapanınca izleme biter; yeni oturumda agent
kanalı kurulu görür (dizin var, `DURUM.md` ACIK) ve monitörünün de açık olduğunu
sanabilir. **Kutunun varlığı monitörün varlığı değildir** — açılışta kendi monitörünün
canlılığı doğrulanır.

**Bildirim sayısı mesaj sayısına eşit değildir** — yakın satırlar tek bildirimde
gruplanıyor. Bildirimi *"bir mesaj geldi"* diye okuyup son bloğa bakan agent öncekini
**atlar ve atladığını fark etmez.** Kural: bildirim geldiğinde **son okuduğun yerden
sonrasının tamamı** okunur.

**Merkezin dinlemesi protokolün şartı, tercih değil.** Merkez dinlemezse bütün trafik
durur ve **durduğu görünmez.**

## Okuma — kutu birikince

Tek dosya birikiyor ve her okumada tamamı context'e giriyor. Bir kutu yüzlerce mesaj
taşıdığında okuma maliyeti işin kendisinden büyük olabilir.

**Yalnız yeni mesaj okunur** — son okunan başlıktan sonrası `awk` ile çıkarılır, tüm dosya
`cat` edilmez.

**`Read` inode değişimine bağışıktır, monitör değil.** Monitör sessiz kaldığında kutu elle
okunabilir — kurtarma yolu var.

## Kapanış

İş bitince agent `outbox`'a yazar:

```markdown
## {rol} -> clara | {tarih}

KAPANDI — {tek satır gerekçe}
```

`DURUM.md`'de `DURUM: KAPANDI` olur, yönetici dizini `arsiv/` altına taşır.

**Saat eşiği uydurulmaz.** Uzun bekleme normal olabilir; çözüm eşik koymak değil
**bekleyeni görünür kılmak.** Kapanışı kanal söyler.

**Ölü kanal temizliği yöneticinin işi**, tetiği oturum açılışı — ayrı zamanlayıcı
kurulmaz, çünkü agent çağrılmadan uyanamaz.

**Canlılık ölçütü güvenilmez — açık kalem.** `PID + BAŞLANGIÇ` çifti ölü/canlı ayrımını
yapamadı: canlı bir agent ölü gösterildi. **Temizlik bu hâliyle yanlış sonuç verir; elle
doğrulanır.** Denenmemiş aday: oturum kaydının son değişim zamanı.

---

# HANDOFF ŞABLONU

*"N agent için kanal kur"* dendiğinde sıfırdan düşünülmez. Aşağıdaki blok her agent için
bir kez, rol adı değiştirilerek verilir. Ekrana basılır, kullanıcı taşır.

```
KİMDEN → KİME: Clara → {ROL}
TÜR: İŞ — kanal kurulumu · üretim işi DEĞİL

NE: Kendi kanalını kur, monitörünü aç, sonra bekle.

  1. KUTULARINI KENDİN AÇ — dosyalar BOŞ olarak var olmalı:

     B=~/.pr-kanal/{PROJE}/{ROL}-{OTURUM}
     mkdir -p $B/inbox $B/outbox
     touch $B/inbox/mesajlar.md $B/outbox/mesajlar.md

     Dosya ÖNCE var olmalı — yoksa izleyici boşluğa bağlanır.

  2. DURUM.md YAZ — $B/DURUM.md:
     ROL / OTURUM / PID / BAŞLANGIÇ / İŞ / DURUM: ACIK

     Damgayı KENDİ ölçümünle yaz, kutuda hazır bulduğunu devralma.

  3. MONİTÖRÜNÜ KENDİN KUR — inbox'ını izle:

     `Monitor` ARACIYLA, `Bash` ile DEĞİL. Araç deferred — önce
     `ToolSearch("select:Monitor,TaskOutput")` ile şemayı yükle.

     command: tail -n 0 -F $B/inbox/mesajlar.md 2>&1 \
                | grep -E --line-buffered '^## |tail:|No such file|Permission'
     persistent: true

     Sonra `TaskOutput` ile doğrula — `TaskList` DEĞİL, o başka defter.

NEDEN: Kurulumu sen yaparsan protokolü öğreniyorsun; hazır bulursan
       kullanıyorsun ama bilmiyorsun — ve bir sonraki oturumda
       bilmeyeceksin.

YAPININ ÖZÜ:
  · inbox: Clara yazar, sen OKURSUN
  · outbox: sen yazarsın, Clara OKUR
  · Başka hiçbir kutuya dokunmazsın. Sebep yetki değil VERİ BÜTÜNLÜĞÜ:
    aynı kutuya iki yazar girerse mesajlar fiziksel olarak bozulur.

OKUMA KURALI: bildirim geldiğinde son okuduğun yerden sonrasının
       TAMAMINI oku — son bloğu değil. Bir bildirim birden fazla
       mesaj taşıyabilir.

YAZMA KURALI: kanal dosyası SİLİNMEZ, ÜZERİNE YAZILMAZ. Düzeltme
       altına eklenir, yalnız `>>` kullanılır.

SONRA: BEKLE. Üretim işine başlamıyorsun. Clara test mesajı yazacak,
       sen outbox'a cevap vereceksin — kanal iki yönde doğrulanacak.
```

---

# Yöneticinin disiplini

Yıldız topolojide trafik tamamen merkezden geçtiği için merkezin disiplini tek denetim
noktasıdır.

**Her olay aktarılmaz — örüntü ve karar aktarılır.** Ara adımların anlatısı kullanıcıyı
takipten koparıyor. Aktarılacak üç şey: bir **sapma**, bir **arıza**, ya da bir **karar**
gerekiyorsa.

**Rapor değil karar getirilir.** Kullanıcı agent ekranlarını görmüyor; ona *"ne oldu"*
değil **"ne karar vereceksin"** taşınır.

**Kurulum bitince oturum izlemesi bırakılır, yalnız kanal izlenir.** Agent'ın iç işleyişi
merkezi ilgilendirmiyor. Verilen işin yapılıp yapılmadığı izlenecekse oturum izlemesi
açılır — o zaman da her adım değil sapma aktarılır.

**Uçlar itiraz edebilir olmalı** ve bu bir arıza değil güvenlik ağıdır. Merkez bir kuralı
yanlış aktarırsa uç düzeltir.

**Ama itiraz da ölçülür.** Bir agent'ın raporundaki mekanik iddia (*"şu araçla kuruldu"*,
*"şu mekanizma çalışıyor"*) ölçüm değildir; aktarmadan önce kendin ölç.

**Merkezin kendi ölçümü de sorgulanır.** En sık hata elde kanıt varken yorumlamak: bir
aracın hangi yolla çağrıldığını varsaymak, bir sessizliği ölüm sanmak, bir çıkarımı karşı
tarafa mal etmek. Ayıran soru: **bunu ölçtüm mü, okudum mu?**

**Altyapı yöneticinin, içerik kullanıcının.** Kanalın nasıl kurulduğu, kimin nereye
yazdığı, monitörün nasıl çalıştığı yöneticinin alanı. Hangi işin verileceği, neyin
onaylandığı kullanıcının.

---

# Açık kalemler

Karar bekleyen ya da yeniden ölçülmesi gereken şeyler. Ayrıntı: `references/olcumler.md`

**`{oturum}` biçimi** — PID mi, iş adı mı? İki biçim bir arada durursa defter karışır.

**Canlılık ölçütü** — `PID + BAŞLANGIÇ` güvenilmez çıktı, `DURUM.md` beyanı da gerçeği
göstermiyor.

**İlk kutuyu kim açar** — kanon *"her agent kendi kanalını açar"* diyor ama ilk kurulumda
kanal henüz kanonda yok, agent onu bilmiyor. İstisna mı, kalıcı düzen mi?

**İş talimatı onay yerine geçer mi** — kullanıcı açık bir talimat verdiğinde mesaj metni
ayrıca gösterilmeli mi? Risk: agent talimatı onay sayarsa kapı zamanla kaybolur.

**`inbox`/`outbox` ayrımı gerekli mi** — mesaj başına dosyaya geçilirse yön ayrımı dosya
adından çözülebilir.

**JSON deposu** — mesaj başına dosya ölçüldü (okuma maliyeti düşüyor, kilit gereksiz,
kenar durumlar geçti) ama **sahada sınanmadı.** Geçiş sinyali: bir agent kutuyu
okuyamadığını söylerse ya da okuma maliyeti işi durdurursa.

**Protokol kanona ne zaman girer** — şu an bu skill yaşayan bir taslak; agent'ların
kanonunda yok, her oturumda elden anlatılıyor. Kanona girmesi için sahada olgunlaşması
gerekiyor: eksikleri görülmeden yazılırsa yanlış kalıcı olur.
