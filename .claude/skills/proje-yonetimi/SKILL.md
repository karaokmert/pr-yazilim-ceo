---
name: proje-yonetimi
description: Clara'nın bir projede agent ekibini yönetme işi — hangi ekip olursa olsun (fabrika, Özel Yazılım, Websitesi, N8N ya da yeni bir takım). İş akışını o ekibin kendi kanonundan çıkarma, handoff taşıma, denetim turlarını izleme, sapmayı yakalama, işi kapatma. Bu skill'i bir projede agent'lara iş verilecekte, yürüyen bir iş izlenecekte ya da kapatılacakta aç: "şu işi ekibe ver", "şuna ilet", "iş nerede kaldı", "denetim ne durumda", "bu işi kapatalım", "ekibi yönet", "handoff yaz" denen her durumda. Ayrıca bir zincir tıkandığında da aç — kimin neyi beklediği ve nerede durulacağı burada. Kapsam dışı — kanal mekaniği (`kanal-kurulumu`), oturum açılış/kapanış sırası (`oturum-duzeni`), haftalık plan (`sprint-yonetimi`).
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

## Yürürken — ne izlenir

**Denetim turları.** Bir iş **denetleyenden** geçene kadar sürer. Turlar arasında ne
değiştiğini izlersin; aynı bulgu iki kez dönüyorsa orada bir gelişim bulgusu var.

**Sapma.** Bir agent kendi rolünün dışına çıkıyorsa, ya da bir karar sana sorulmadan
veriliyorsa yakalanır — ama düzeltmesi sana ait değil, **bildirmek** sana ait.

**Tıkanma.** Kimse yazmıyorsa iki ihtimal var ve karıştırılmaz: iş bitti mi, yoksa
mekanizma mı öldü? **Sessizlik sinyal değildir** — monitör ölmüş olabilir, kanal
sağlıklı *görünürken* mesaj gelmiyor olabilir.

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
