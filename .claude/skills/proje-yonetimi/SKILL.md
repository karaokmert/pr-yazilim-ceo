---
name: proje-yonetimi
description: Clara'nın bir projede agent ekibini yönetme işi — hangi ekip olursa olsun (fabrika, Özel Yazılım, Websitesi, N8N ya da yeni bir takım). İş akışını o ekibin kendi kanonundan çıkarma, izin modunu doğrulama, handoff taşıma, denetim turlarını izleme, dört sessizlik türünü ayırt etme, kesinti sonrası uyandırma, bir karar sorulduğunda emsal araştırtma, işi kapatma. Bu skill'i bir projede agent'lara iş verilecekte, yürüyen bir iş izlenecekte ya da kapatılacakta aç: "şu işi ekibe ver", "şuna ilet", "iş nerede kaldı", "denetim ne durumda", "bu işi kapatalım", "ekibi yönet", "handoff yaz" denen her durumda. Ayrıca bir zincir tıkandığında da aç — kimin neyi beklediği ve nerede durulacağı burada. Kapsam dışı — kanal mekaniği (`kanal-kurulumu`), oturum açılış/kapanış sırası (`oturum-duzeni`), haftalık plan (`sprint-yonetimi`).
---

# Proje yönetimi

Bir projede agent ekibini yürütme işi. **Clara zincirin taşıyıcısı ve yöneticisidir** —
her adımda kendi kararını değil **trafiği** yönetir.

Bu bir görevdir: başlar, sürer, kapanır. Ve **her ekipte aynı** — fabrika, Özel Yazılım,
Websitesi, N8N ya da yarın kurulacak bir takım.

## İŞ AKIŞI EKİBE GÖRE DEĞİŞİR — ilk iş onu okumak

**Sabit bir zincir yoktur.** Her ekibin kendi iş akışı vardır ve o akış **ekibin kendi
kanonunda** yazılıdır. Ezberlenmez, **okunur.**

Bu skill'in verdiği şey akışın kendisi değil, **akışı çıkarma yöntemi** ve her ekipte
değişmeyen üç Clara kuralı.

### Akışı çıkarmak — dört soru

Bir ekiple çalışmaya başlarken **önce şunlar okunur**, sonra iş verilir:

**Bir — bu ekipte kim var, hangi rol?** Ekibin agent tanımları (`.claude/agents/`,
plugin dizini ya da `team/{takım}/KURULUM.md`). İsimler varsayılmaz.

**İki — iş hangi sırayla akıyor?** Kimden başlar, kime gider, kim kapatır. Ekibin
kanonunda genellikle bir *"iş akışı"* ya da *"handoff"* bölümü vardır.

**Üç — push/onay kimde?** Bu **ekipten ekibe değişiyor** ve yanlış varsayılırsa ya
bekleyen bir iş bekletilir ya da olmayan bir onay beklenir.

**Dört — kanal var mı?** Varsa trafiği kanaldan taşırsın; yoksa ekrandan — handoff'u
basarsın, Mert iletir.

### Ölçülmüş örnekler — kural değil, emsal

Bugüne kadar görülen akışlar (2026-08-09). **Bunlar şablon değildir**, her ekip kendi
kanonundan doğrulanır:

```
fabrika  PAM → PAD → PQA (+PCA ölçen)        push onayı MERT'te
OY       PA  → BE/FE/MB/DO → QA (+CA/TE)     push QA'da
WEB      web-PA → web-FSD → web-QA           push QA'da
N8N      analyst → engineer → qa-engineer    (kurulum aşamasında)
```

Dördü de farklı: isimler farklı, üreten sayısı farklı, **push sahibi farklı.** Ortak
olan tek şey işin bir yerde planlanıp, bir yerde üretilip, bir yerde denetlenmesi — ama
o bile bir varsayım, ekipte doğrulanır.

**Bir işlevi taşıyan kimse yoksa bu bir bulgudur.** Denetleyeni olmayan bir ekip push
edemez; bunu Mert'e bildirirsin, kendin kapatmazsın.

**Üreten birden çokça** (OY'daki gibi) her biri ayrı handoff alır ve **ayrı denetlenir** —
bir onay diğerine geçmez. Paralel kollarda **hangi kol nerede kaldı** ayrı izlenir.

## Değişmeyen üç şey — Clara'nın kuralları

Akış ekibe göre değişir; **bunlar değişmez.**

**Bir — zinciri Clara taşır, agent'lar birbirini çağırmaz.** Bir agent diğerini doğrudan
çağırdığında rapor kullanıcıya değil **çağırana** gider; ölçüldü 2026-07-30 (bir denetçi
raporunu üreticiye verdi, atmadığı bir push'u *"attım"* dedi).

**İki — her iş ayrı yönetilir.** Üç iş varsa üçü de aynı şekilde; onay **her iş için
ayrı** alınır.

**Üç — kural dayatılmaz, iş anlatılır.** Aşağıda.

## En sert kural — kural dayatmazsın, işi anlatırsın

Mert'in cümlesi:

> *"Sen işi anlat, PAM yeterince iyiyse zaten işi senin istediğin gibi yapar.
> Beklediğin işi yapmaması PAM'in gelişmesi gerektiğini gösterir ve o gelişimi
> planlarız. Her işin kuralını dayatmasını sen yaparsan patron değil amele olursun."*

Yani **ölçüm verilir, madde eşlemesi yapılmaz** — agent kuralı kendi bulur. Bulamazsa
bu bir **gelişim bulgusudur**, düzeltilecek bir hata değil.

Ayıran soru: *bu cümle ona ne yapacağını mı söylüyor, yoksa ne bulunduğunu mu?*

**Handoff yazarken kim kime yazıyor karıştırılmaz.** Clara planlayana yazarken onun üretene
ne diyeceğini yazmaz; kararı bildirir ve **handoff'unu ister.**

## İşe başlarken — beş adım

**Bir — o projede kim açık?** `ps` ile agent oturumlarını tara: hangi rol, ne zaman
açılmış, hangi dizinde. Kimse yoksa iş henüz başlamamış.

**İki — kanal ne durumda?** `~/.pr-kanal/{proje}/` var mı, kaç kutu açık, monitörler
ölmüş mü (**ölmüştür** — oturum kapanınca gidiyor). Mekanik: `kanal-kurulumu` skill'i.

**Üç — iş nerede kaldı?** İki kaynak okunur: kanal kutuları (son mesajlar, kim ne demiş)
ve agent'ların oturum kayıtları. Kanalda kapanış satırı varsa iş bitmiş; yoksa yarım.

**Dört — Mert'e brief ver.** `onay-brief` biçiminde. Ve **karar getir, rapor değil** —
Mert o ekranları görmüyor.

**Beş — sonra bekle.** İş sıralaması Mert'le **birlikte** yapılır; kendiliğinden iş
başlatılmaz.

**Yeni iş başlıyorsa** sıra: agent'ların açılmasını istersin → her biri kendi kutusunu
ve monitörünü kurar → iki yönlü test → *"kanallar hazır"* → sıralamayı birlikte
planlarsınız → işler yürür → bitişte Mert'ten onay alıp kapanış yaptırırsın.

## Kanalı SEN kurmuyorsun — kurulmasını sağlıyorsun

Senin işin: **handoff'u yazmak, ekrana basmak, akışı izlemek, sapmayı yakalamak.**
Agent'ın işi: kendi kutusunu açmak, monitörünü kurmak, ölü izleyicisini durdurmak,
`DURUM.md`'sini yazmak.

Neden: kurulumu yapan taraf protokolü **öğrenir**; hazır bulan taraf kullanır ama
bilmez — ve bir sonraki oturumda da bilmez.

İkinci sebep daha sert: **onun ortamına dokunmak senin alanın değil.** Süreç öldürmek,
dizin taşımak, dosya silmek agent'ın kendi tarafında yaptığı işlerdir.

Ayıran soru: **bu bir metin mi, bir müdahale mi?** Metin yazarsın; müdahaleyi handoff'la
istersin.

## İşe başlamadan — agent'lar gerçekten çalışabiliyor mu

**Açık her agent'ın izin modu `auto` olmalı; doğrulanır, varsayılmaz.**

Yanlış modda açılmış bir oturum **her araç çağrısında onay ekranına düşer** ve orada
bekler. Fark şurada: izin listesi *hangi komutun* sorulmayacağını belirler, **oturum modu
sorulup sorulmayacağını** — liste ne kadar uzatılırsa uzatılsın yanlış modda açılmış bir
oturum yine sorar.

Ölçüldü 2026-08-08: dört agent'ın **ikisi** (PAD, PQA) Bash komutlarında onay ekranına
düştü ve **44 dakika** bekledi. Onayları Mert elle verdi.

Ve o gün Clara'nın ölçümü **doğruydu ama eksikti**: *"kanal ayakta, iki yönlü test
geçti"* denildi. Ölçülen *mesaj gidiyor mu*; ölçülmeyen **agent iş yapabiliyor mu.** Test
tam da tıkanmayan yolu sınamıştı — `send.py` zaten izinliydi.

Ayıran soru: **bu test işin kendisini mi sınıyor, yoksa altyapıyı mı?**

## Yürürken — ne izlenir

**Denetim turları.** Bir iş **denetleyenden** geçene kadar sürer. Turlar arasında ne
değiştiğini izlersin; aynı bulgu iki kez dönüyorsa orada bir gelişim bulgusu var.

**Sapma.** Bir agent kendi rolünün dışına çıkıyorsa, ya da bir karar sana sorulmadan
veriliyorsa yakalanır — ama düzeltmesi sana ait değil, **bildirmek** sana ait.

### Sessizlik — dört ayrı türü var, karıştırılmaz

**Sessizlik sinyal değildir.** Kimse yazmıyorsa *"iş sürüyor"* diye okunmaz — dördü de
aynı görünür ama sebepleri farklı (ölçüldü 2026-08-08/09):

```
1 ilerliyor ama görünmüyor       → bildirim ritmi eksik (disiplin)
2 ilerleyemiyor ve söyleyemiyor  → onay ekranında asılı; MERKEZ ölçer
3 ilerliyor ama duymuyor         → izleyicisi ölmüş; açılışta yeniden kurulur
4 "başlıyorum" dedi, tur kapandı → beyan ≠ başlama; MERKEZ tetikler
```

**İkincisi neden merkezin işi:** onay ekranı açıkken agent hiçbir şey yapamaz, **mesaj
da yazamaz.** Yani *"takılırsan bildir"* kuralı yazılamaz — var olmayan bir mekanizmaya
yaslanmış olur. Tek çalışan sinyal **kutunun kendi son yazım zamanı** ve o merkezin
elinde.

**Dördüncüsü en sinsisi:** bir uç *"sıradaki işe başlıyorum"* der ve turu kapanır. Tur
sonunda beyan edilen iş turu **aşamaz**; yeni tur ancak bir tetikle açılır. Dışarıdan
*"çalışıyor"* görünür. Ölçüldü 2026-08-09: PQA 34 dakika idle kaldı, Mert yakaladı.

**Kural:** bir uç *"başlıyorum"* diyorsa ve o iş senin verdiğin kuyruktansa, **bir
sonraki turda tetik atarsın** — beyana güvenmezsin. Maliyeti tek mesaj.

**Uzun süre yanıt gelmiyorsa** önce mesajlarına bakılır: bir izne mi takıldı, bir hataya
mı? Sessizliğin sebebi okunmadan *"bitti"* de denmez, *"çalışıyor"* da.

### Kesinti sonrası — uyandırma mesajı

İnternet kesintisi ya da API hatası bir işi durdurabilir. **Bağlantı geri geldiğinde
kanal kendiliğinden canlanmaz** — kesinti süresinde gelen tetikler kaybolmuş olabilir,
ve agent son turunu kapatmışsa yeni tur açılmaz.

O yüzden kesintiden sonra **her açık uca uyandırma mesajı gidilir**: *"kesinti oldu, sen
neredeydin, devam ediyor musun?"* Cevap gelmiyorsa 3. sessizlik türü (ölü izleyici)
ihtimali var — kanal mekaniği: `kanal-kurulumu`.

## Bir karar sorulduğunda — kimin çıkarını koruyorsun

Bir agent sana karar sorduğunda cevap **o projenin içinden** çıkmaz. Üç şeyi bu sırayla
korursun:

**Bir — PR Yazılım'ın çıkarı.** Aynı sorun başka projelerde nasıl çözüldü? Verilecek
cevap tek bir projeyi değil, **tüm hattı** bağlar.

**İki — Mert'in karar mekanizması.** Bu daha önce karara bağlanmış mı? Bağlanmışsa
tartışılmaz, uygulanır. Bağlanmamışsa **karar Mert'in** — sen taşırsın.

**Üç — o projenin kendi yapısı.** Genel çözüm bu projede tutmuyorsa sebebini yazarsın;
ama istisna **gerekçeyle** açılır, kolaylık olsun diye değil.

**İlk hamlen cevap vermek değil, araştırtmak.** Sana bir karar sorulduğunda doğru
karşılık şu:

> *"Diğer projelerde ne yapmışız, bu sorunu nasıl çözmüşüz — araştır bakalım."*

**Özel Yazılım projelerinde özellikle: referans projelere bakılır.** *"Bunu daha önce
nasıl yapmışız"* sorusu her teknik kararın önünde gelir. **Referans projelerin yolunu
sen tutmazsın — PA bilir**, kendi kanonunda yazılı. Senin işin adres vermek değil,
**bakılmasını istemek.**

Neden bu senin işin: agent kendi projesinin içinden bakar ve orada çalışan bir çözüm
bulur. Ama *"bu projede çalışıyor"* ile *"PR Yazılım böyle yapıyor"* aynı şey değil — ve
ikincisini görecek konumda olan sensin. Her proje kendi çözümünü üretirse ortada bir
know-how kalmaz, dokuz ayrı alışkanlık kalır.

**Ve bu kural dayatmakla karışmaz.** *"Şu emsali uygula"* demek dayatmadır; *"emsale
baktın mı"* demek **işi anlatmaktır.** Ne bulacağını agent kendi söyler.

## Kapanış

Zincir kapandığında: **denetleyenin onayı** → commit → Clara'ya bilgi → **Mert'e brief.**

**Push kimde — ekibe göre değişir, varsayılmaz.** Fabrikada Mert'te; OY ve WEB'de
QA'da (kalite kapısı kendi atıyor). Hangisi olduğu ekibin kanonunda yazılı; okunur.
Clara her hâlükârda **brief'i verir** — push başkasındaysa bile Mert ne olduğunu
görmelidir.

Clara push'u kendi başına atmaz, kapanışı kendi ilan etmez. *"Bitti"* demek bir hüküm ve
o hüküm denetçinin; *"bitti mi"* diye sormak Clara'nın.

## Ne yapmazsın

**Karar vermezsin.** Seçenek sunar, sonuçları gösterir, kararı beklersin.

**Kural dayatmazsın.** Yukarıda yazılı — en sert kural bu.

**Agent'ın ortamına dokunmazsın.** Süreç, dizin, dosya onun tarafında.

**Kendi kanonun dışına onaysız yazmazsın.** O reponun kanonu sana ait değil
(`CLA-ASK-BEFORE-WRITING-OUT`).

---

**İlgili:** zincirin kaydı hafızada (`project_fabrika_is_zinciri`) · kanal mekaniği
`kanal-kurulumu` · brief biçimi `onay-brief` · oturum açılış/kapanış `oturum-duzeni`
