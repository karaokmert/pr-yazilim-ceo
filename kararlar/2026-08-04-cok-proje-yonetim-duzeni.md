# Çok proje yönetim düzeni — Clara merkezli kanal + oturum belleği

**Tarih:** 2026-08-04
**Karar veren:** Mert
**Durum:** İlke kararı verildi, üretim parçaları PAM'e gitmedi

## Neden bu karara ihtiyaç duyuldu

Mert aynı anda birden fazla projede çalışıyor ve her projenin agent'ları ayrı
pencerelerde açık. Handoff'ları pencere pencere elle taşıyor.

**Ölçüldü (2026-08-04, 18:49):** o an açık **11 agent oturumu** vardı — dördü PA.
Dağılım: GOAT'ta PA, egelisaglik'te iki PA + QA + FE, platin-agent-web'te PA
(23 saattir açık), agent-project'te PAM (16 saat), skill-project'te bir
`agent-generator` oturumu (emekli rol — aşağıda).
Hepsi `--name OY` ile açılmış, isim ayırt etmiyor.

**Ayrı bir bulgu: AG (Agent Generator) emekli, agent'lar bilmiyor.** Mert'in
cümlesi: *"AG öldü artık, agent'lar hâlâ onu biliyor ama bizim PAM'ımız var."*
Agent üretimi artık `agent-project`'teki fabrikada (PAM/PAD/PQA/PCA).

Ölçüldü, aynı gün: PA kanonundaki bir hatayı düzeltmeyi doğru şekilde reddetti
ama *"AG'ye gidecek bulgu dokümanı hazırlarım"* dedi — yani **kanonu onu ölü bir
kapıya yönlendiriyor.** Kullanıcının global `CLAUDE.md`'sinde de *"agent, skill,
reference güncellemeleri AG ile yapılır"* yazıyor.

Sonuç: bu düzenin ürettiği her gereksinim PAM'e gider, ve agent kanonlarındaki
AG referansları düzeltilmeli (bu da PAM'in işi).

**Ve tek bir işin kaç durak gezdiği ölçüldü.** Egeli'de `PRY-16152` (CRM sayı
girişi) bugün dört ayrı oturumdan geçti: Mert hatayı bildirdi → PA; PA'nın
handoff'u yapıştırıldı → FE; FE'nin handoff'u yapıştırıldı → QA; QA'nın bilgisi
→ PA. Üç elle taşıma, bir hata ayıklama işi için.

İki oturumda **kullanıcı mesaj sayısı 1** — o pencere yalnızca handoff yapıştırmak
için açılmış. O pencerenin tüm varlığı bir taşıma işlemi.

## Mert'in hedefi (kendi cümleleriyle)

*"Bir ekranda projelerimi yönetebilmek istiyorum."*
*"Önden çok sıkı net düşünülmüş dokümanlar üretip, işi PA ile tüm detayları ile
netleyip sonrasında işi başlatmak istiyorum."*
*"Her agent'ın aldığı kararları da yönetebilmek istiyorum — kontrolümüzden
çıkmasın ama bir yandan da süreç sürekli tıkanmasın."*
*"Hem bu sayede gelişim alanlarını görelim ve agent'ları iyileştirelim, hem de
projelerin gelişiminde hız kazanalım."*

## Kararın kendisi — üç parçalı iş bölümü

### 1. Kanal: iş taşıma katmanı (Clara'nın işi)

Her agent kendi kanal dosyasına yazar, Clara okur, Mert onaylar, Clara yanıtı
ilgili kanala yazar. Agent'lar birbirini görmez — tek irtibat Clara.

**Clara çağırmaz, yazar.** Kanala metin bırakmak iş vermektir; `Task` ile agent
açmak çağırmaktır ve yasaktır (`CLA-NO-CALL-TEAMS`). Ayrım tekniğe benziyor ama
değil: Clara çağırırsa rapor Mert'e değil Clara'ya gider ve zincir görünmez olur.
Kanal düzeninde rapor kanalda durur, ikisi de okur.

### 2. Oturum belleği: iş bölümü — agent detayı, Clara özeti

**Bu kararın en önemli maddesi ve Mert'in düzeltmesiyle şekillendi.**

Clara'nın ilk önerisi iki yol sunmuştu: (a) agent'lar devir yazar, (b) Clara
oturum kayıtlarını okuyup çıkarır. Mert ikisini rakip değil **iş bölümü** olarak
kurdu:

> *"Sen kanala mesaj bırakırsan agent'lar kendi içeriklerini normal proje içine
> memory'ye kayıt eder, sen sadece onlardan özeti tutarsın — bu senin işini
> kısaltır. Öteki türlüsü çok uzun bile sürebilir."*

**Doğru, ve Clara'nın okuma yolu bunun yerine geçemez.** Ölçüldü: Egeli'nin dört
oturumunu tarayıp bir işin izini sürmek dakikalar aldı ve **niyet hâlâ
görünmedi** — bir PA'nın *"şunu yapmayı düşünüyordum"* cümlesi kayıtta yok.
Altı projeye çıkınca ölçeklenmez. Agent bir paragraf yazarsa iş biter.

Bölüm şu:
- **Agent** kendi projesinin memory'sine yazar: detay, kod bağlamı, kararın
  gerekçesi. Zaten oraya ait ve kanonunda kapanış protokolü var.
- **Clara** yalnız özeti tutar: kim, hangi projede, ne yaptı, nerede kaldı, ne
  bekliyor. Clara detayı tekrar etmez — **indeksini tutar.**

Böylece *"nerede kaldık Clara"* sorusunun cevabı tek yerde olur.

### 3. Kural agent'ın kanonunda yaşar, Clara'nın mesajında değil

Mert `pause` diye bir **skill** tarif etti: Clara *"pause"* der, ne yazılacağını
agent'ın kendi kanonu söyler.

**Bu doğru tasarım.** Clara ne yazacağını her seferinde söylerse biçim tutmaz —
her turda farklı yazar. Kural skill'de olursa biçim sabit kalır ve Clara'nın
mesajı tek kelimeye iner.

## Ölçülmüş dayanaklar

**Kanon sahada çalışıyor.** 2026-08-04 kanon ölçümü: PA ve UID 90+ kural ID'sini
biliyor, yedi davranış durumunun hepsini doğru ayırdı. Sınır dedikleri yerde işi
bırakmadılar, doğru kapıya yönlendirdiler. Yani bu düzenin dayandığı zemin sağlam.

**Mert agent'ları düzeltmiyor, besliyor.** Egeli PA oturumundaki 21 mesaj
incelendi: neredeyse hepsi karar (*"A prod'a al, B live dev'e"*), bilgi
(*"veritabanına her zaman 90-purephone ile girer"*) ya da yön
(*"excel yüklendiği an inceleyelim, db'ye girmesin"*). **Yalnız ikisi düzeltme**
(*"firma yönetimi nedir, nereden buldun bunu"* ve *"bir task'ın açıklaması yoksa
dokümanı vardır"*).

Bunun tasarıma sonucu: kapı **denetim** kapısı değil **besleme** kapısı olmalı.
Mert'in yükü agent'ı kontrol etmek değil, ona kendisinde olan bilgiyi vermek.

**İyi PA neye benziyor — GOAT örneği.** Aynı kanonu taşıyan GOAT PA'sı üç şey
yaptı: (1) PR'ın atıf verdiği iki dokümanın yokluğunu buldu ve sebebini git
geçmişinde aradı — `.gitignore` değil, hiç oluşturulmamış; (2) Mert'in
*"ClickUp'ta vardır zaten"* varsayımını doğruladı ama **yeni söylediği şeyin
orada olmadığını** gösterdi; (3) varsayımını etiketledi:
*"tek şeyi varsayarak ilerliyorum, yanlışsa söyle"* — tıkanmadı ama sessizce de
karar vermedi.

Egeli PA'sı ise *"firma yönetimi"* diye bir şey uydurdu. **Kanon aynı, davranış
farklı** — sebebi ölçülmedi (oturum yaşı mı, işin türü mü?). Bu açık bir soru.

**Boşta bekleyen oturum token yemiyor.** Ölçüldü: maliyet tur sayısıyla artıyor,
bekleme süresiyle değil. Egeli'nin 159 turluk oturumu 33.8M cache okuma;
GOAT'ın 65 turluk oturumu 9.1M. cache_write payı her oturumda küçük (0.3–1.7M),
yani cache sürekli baştan kurulmuyor.

**Önceki kayıt düzeltildi:** 2026-08-04 gecesi *"boşta kalan agent uyanınca cache
resetlenir, maliyet kesintiden gelir"* diye bir kayıt tutulmuştu; bu ölçüm onu
desteklemiyor. Yani **açık oturumu kapatmak için token gerekçesi yok** — kapatma
gerekçesi başka (aynı projede iki PA birbirini bilmiyor), maliyet değil.

## Kabul edilen gerilim: kontrol vs. tıkanma

Mert'in hedefinde bir gerilim var ve karar onu çözmüyor, **yönetiyor:**

Her kararı Mert onaylarsa onay kuyruğu oluşur — 6 proje × 4 agent = her turda
okunacak 24 blok, bugün taşıdığı handoff'lardan daha yorucu. Hiçbirini
onaylamazsa iki hafta sonra ne olduğu bilinmeyen bir yapı çıkar.

Çözüm ortada bir yer değil: **hangi kararın Mert'e geldiğinin kuralı.**
Dayanak PA'nın kendi tespiti — kanon yasakları ID'liyor, görevleri ID'lemiyor.
Yani agent'lar *"yapmam"* dedikleri yerde zaten duruyor; duramadıkları yer
*"yaptım ama farklı yaptım."* Kapı oraya konmalı.

## Üretilmesi gerekenler (PAM'in işi, henüz devredilmedi)

1. **`pause` skill'i** — yok. Agent olmayan bir skill'i çağıramaz. Clara *"pause"*
   dediğinde ne yazılacağını tanımlayan kural bu skill'de yaşar.
2. **Oturum açılışında kanal Monitor'ı kurma kuralı** — bugün ölçüldü: agent kendi
   Monitor'ı olmadan kanalı görmüyor, iş kanalda sessizce bekliyor. Bu her
   seferinde Clara'nın hatırlatması gereken bir şey olmamalı, kanonda olmalı.
3. **Oturum açılışında "nerede kaldık" okuma kuralı** — Mert'in cümlesi:
   *"her session açılışında ilk mesaj olarak yarım kaldığımız yeri okumalarını
   sağlayabiliriz."*

## Açık sorular

- **Aynı kanon, farklı davranış:** GOAT PA'sı kaynağa gidiyor, Egeli PA'sı uydurdu.
  Sebep oturum yaşı mı (Egeli'deki 01:55'ten beri açık), işin türü mü, context
  doluluğu mu? Ölçülmedi.
- **Aynı projede iki PA** (Egeli'de 13:58 ve 01:55) — biri diğerinin ne bildiğini
  bilmiyor. Tekilleştirme kuralı gerekiyor mu?
- **Kapının yeri:** "yaptım ama farklı yaptım" durumunu agent'ın kendisi
  bildirmeli mi, yoksa Clara mı yakalamalı?

## İlgili kayıtlar

- `gunluk/2026-08-04.md` — kanal deneyleri (üç tur) + kanon ölçümü, tam kayıt
- `.claude/agent-memory/clara/project_kanal_testleri.md`
- `.claude/agent-memory/clara/project_kanon_olcumu.md`
