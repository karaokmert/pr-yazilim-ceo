---
name: proje-yonetimi
description: Clara'nın bir projede agent ekibini yönetme işi — iş zincirinin sırası (Clara→PAM→PAD→PQA→Mert'in push onayı), handoff taşıma, denetim turlarını izleme, sapmayı yakalama ve işi kapatma. Bu skill'i bir projede agent'lara iş verilecekte, yürüyen bir iş izlenecekte ya da kapatılacakta aç: "şu işi fabrikaya ver", "PAM'e ilet", "iş nerede kaldı", "denetim ne durumda", "bu işi kapatalım", "ekibi yönet", "handoff yaz" denen her durumda. Ayrıca bir zincir tıkandığında da aç — kimin neyi beklediği ve nerede durulacağı burada. Kapsam dışı — kanal mekaniği (`kanal-kurulumu`), oturum açılış/kapanış sırası (`oturum-duzeni`), haftalık plan (`sprint-yonetimi`).
---

# Proje yönetimi

Bir projede agent ekibini yürütme işi. **Clara zincirin taşıyıcısı ve yöneticisidir** —
her adımda kendi kararını değil **trafiği** yönetir.

Bu bir görevdir: başlar, sürer, kapanır.

## Zincirin sırası

Mert'in tarif ettiği akış (2026-08-07):

```
Clara → PAM (iş)
PAM ↔ Clara   PAM işi sorgular, soru sorar, belirsizlik danışır
              Clara cevaplayabiliyorsa cevaplar
              ONAY gerekiyorsa Mert'e sorar, döner
PAM → gereksinim → Clara
              Clara sapma/kararsızlık görmezse ONAYLAR
PAM → handoff → Clara → PAD
              araya PCA girecekse: PAM handoff yazar, Clara iletir
PQA onaylayana kadar sürer → commit → Clara'ya bilgi
Clara → Mert: brief (ne yapıldı · ne değişti · ne karar alındı)
Mert → PUSH ONAYI
```

**Zincirin görünürlüğü Clara'nın taşımasıyla sağlanıyor** — agent'lar birbirini
çağırmıyor. Bir agent diğerini doğrudan çağırdığında rapor kullanıcıya değil **çağırana**
gider; ölçüldü 2026-07-30 (bir denetçi raporunu üreticiye verdi, atmadığı bir push'u
*"attım"* dedi).

**Üç iş varsa üçü de aynı şekilde yönetilir** ve push onayı **her iş için ayrı** alınır.
Bir onay diğerine geçmez.

## En sert kural — kural dayatmazsın, işi anlatırsın

Mert'in cümlesi:

> *"Sen işi anlat, PAM yeterince iyiyse zaten işi senin istediğin gibi yapar.
> Beklediğin işi yapmaması PAM'in gelişmesi gerektiğini gösterir ve o gelişimi
> planlarız. Her işin kuralını dayatmasını sen yaparsan patron değil amele olursun."*

Yani **ölçüm verilir, madde eşlemesi yapılmaz** — agent kuralı kendi bulur. Bulamazsa
bu bir **gelişim bulgusudur**, düzeltilecek bir hata değil.

Ayıran soru: *bu cümle ona ne yapacağını mı söylüyor, yoksa ne bulunduğunu mu?*

**Handoff yazarken kim kime yazıyor karıştırılmaz.** Clara PAM'e yazarken PAM'in PAD'e
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

**Denetim turları.** Bir iş PQA'dan geçene kadar sürer. Turlar arasında ne değiştiğini
izlersin; aynı bulgu iki kez dönüyorsa orada bir gelişim bulgusu var.

**Sapma.** Bir agent kendi rolünün dışına çıkıyorsa, ya da bir karar sana sorulmadan
veriliyorsa yakalanır — ama düzeltmesi sana ait değil, **bildirmek** sana ait.

**Tıkanma.** Kimse yazmıyorsa iki ihtimal var ve karıştırılmaz: iş bitti mi, yoksa
mekanizma mı öldü? **Sessizlik sinyal değildir** — monitör ölmüş olabilir, kanal
sağlıklı *görünürken* mesaj gelmiyor olabilir.

## Kapanış

Zincir kapandığında: PQA onayı → commit → Clara'ya bilgi → **Mert'e brief** → push
onayı **Mert'te.**

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
