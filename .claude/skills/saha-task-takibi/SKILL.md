---
name: saha-task-takibi
description: "Bu skill şu durumlarda kullanılır: bir OY projesinde agent'lara verilen işin ClickUp'ta kaydı tutulurken. Tetikleyici ifadeler — \"sub task aç\", \"task nerede\", \"statüsü ne\", \"kim ne yapıyor\", \"iş kaydedildi mi\", \"sabah dökümü\", \"kaç saat sürdü\", \"bu iş görünmüyor\", \"kanıt eklendi mi\". Ayrıca bir agent iş bitirdiğinde kaydın tam olup olmadığı ölçülürken, bir işin ne kadar beklediği sorulduğunda ve paylaşılan repoda commit atılacakken de kullanılır. Kapsam dışı — ClickUp aracının kendi sınırları (`clickup-duzeni`), ekibin yönetimi ve rol sınırları (`proje-yonetimi`), haftalık plan (`sprint-yonetimi`)."
---

# Sahada işin kaydı — ClickUp task takibi

Bu skill bir OY projesinde **verilen işin izini** tutar: sub task nasıl açılır, statü
nasıl akar, kanıt neden zorunlu, süre nereden okunur, sabah dökümü ne gösterir.

Yönetimin kendisi `proje-yonetimi`'nde; burası yalnız **kayıt.** ClickUp aracının
ölçülmüş sınırları (yazmanın güvenilmezliği, aramanın kaçırması, süre alanı çakışması)
`clickup-duzeni`'nde — buraya kopyalanmaz.

**Tetik: bir işe başlanıyor.** Bu bölüm bir seçenek değil, sahanın omurgası —
bozulduğunda kimin hangi işi bitirdiği belirsizleşir ve işler yarım kalır.

*Mert'in teşhisi, 2026-08-12: "Projelerde akışlar birbirine girdi, kimin hangi işi
bitirdiği belli olmadan diğer işe gidildi, bu nedenle her task yarım kaldı."*

### Neden ClickUp tek başına çözmüyordu

Araç zaten vardı. Arıza aracın yokluğu değil, **kimin yazdığıydı**: kanona göre
ClickUp'a yalnız PA yazıyor (`CLICKUP-PA-ONLY-WRITE`), gerçek iş agent'ta ilerliyor,
araya Clara giriyor. Üç katman, tek gerçek — ve kayıt gerçeğin bir tur gerisinde.

Asıl kırılma daha derinde: ***"bitti" bir beyandır, kayıt değildir.*** Beyan üstüne
akış ilerliyor, sonra denetim *"eksik"* diyor ve iş geri geliyor — ama o arada agent
başka işe başlamış oluyor. **İki iş de yarım.**

### Üç fiil, çakışma yok

**PA açar** — discovery bitince katman sub task'larını **sahipsiz** açar (atama iş
verilirken olur), ve öncelik taşır. **Hiçbir agent yeni sub task açmaz.**

**Agent yürütür** — kendi sub task'ının statüsünü kendi çeker.

⚠️ **Sınır kesindir ve fabrika kararıdır** (2026-08-12): agent **YALNIZ kendi sub
task'ının** statüsünü çevirir. Ana task · başkasının sub task'ı · `Closed` · task
silme → **mutlak yasak.**

**"Kendi sub task'ı" başlık önekinden okunur** — `[FE] PRAG - Takvim Görünümü`.
Kural tek cümle: ***"başlık senin kısaltmanla başlamıyorsa dokunma."*** Sınır böylece
talimata değil **okunabilir bir işarete** bağlanır; agent'ın hangi ID'yi aldığına ya da
kimin ne dediğine bakmaz.

**Ana task her zaman PA'nındır.** Tek istisna: QA, push ettiği sub task'ı `live - dev`'e
alır.

Kararın mantığı: sınır **talimatla** değil **sahiplikle** çiziliyor. Testte agent'ları
sınırlayan şey bir talimattı — ve talimat bir oturumun içinde yaşar, mekanizma yaşamaz.
Gerekçe: `konular/clickup-is-takibi/uygulananlar/2026-08-12-clickup-task-takip-duzeni.md`.

**Clara okur ve TIKANANI İŞARETLER** — iş açmaz, sıra vermez. Durumu okur, sapmayı
gösterir, ve **karar bekleyen işi `blocked`'a alıp comment'ler.**

### Akış DURMAZ — bekleyen iş blocked'a alınır

> **Mert'ten yanıt gelmiyorsa beklemezsin — o task'ı `blocked`'a alır, sebebini
> comment'e yazar, SIRADAKİ işe geçersin.**

*Mert'in cümlesi (2026-08-14): "Karar bekleyen iş varsa ve benden yanıt gelmiyorsa
diğer taske geçersin. 10 task varken 6'sı bitse yeter. 4 taski kendin blocked'a alır
comment atarsın, geldiğimizde neresi tıkandı görürüz."*

**Ölçüt on üzerinden altı.** Tamamının bitmesi beklenmez; **tıkananın görünür
olması** beklenir. Bir tıkanma comment'lenmişse iş kaybolmamıştır — sen döndüğünde
nerede durduğu okunur.

Comment'te üç şey: **ne bekleniyor · kimden · neden ilerlenemiyor.**

⚠️ **Bu `blocked` işareti Clara'nın tek statü yetkisidir.** Başka hiçbir statüye
dokunmazsın — `in progress`, `test`, `completed` hepsi sahibinin.

### Ana task altında BEŞ sub task

```
PRC-26  Randevu Takvimi              [in progress]
  └ PA   Discovery                    ← PA'nın kendi işi de görünür
  └ UID  Mock
  └ BE   Contract
  └ FE   Ekran
  └ PA   Kapanış                      ← baştan Open durur
```

**PA'nın iki sub task'ı olmasının sebebi ölçüldü:** ilk turda PA 78 dakika çalıştı
(discovery, üç soru turu, sub task açılışı, yorumlar) ve ClickUp'ta **tek izi yoktu.**
*"PA ne yapıyor"* sorusunun cevabı yalnız kanal kutusundaydı.

**Kapanış sub task'ı baştan açılır, sonda değil.** Gerekçesi PA'nın kendi cümlesi:
*"sahada en sık kaybolan iş **bitmiş ama kapanmamış** iştir; kapanış kutusu Open
dururken kimse 'bitti' diyemez. Bu bir görünürlük kaydı değil, bir **kapı**."*

### Sıra

```
PA işi alır → ana task 'in progress' + kendi discovery sub task'ı 'in progress'
  ↓
Discovery biter → discovery 'completed' (kanıt: doküman yolu + commit)
                + AYNI ANDA katman sub task'ları (sahipsiz) + kapanış sub task'ı açılır
  ↓
Katmanlar yürür → her agent kendi sub task'ında
  ↓
Hepsi 'completed' → PA kapanışı 'in progress' alır → konsolide eder
                  → ana task 'live - dev' + kapanış notu → kapanış 'completed'
```

**Katman sub task'ları discovery'den SONRA açılır** — hangi katmanların gireceği
discovery'den çıkar, önce açılamaz.

### Statü akışı ve kapatma yetkisi

```
Open → in progress → test (QA'ya devrederken, agent çeker)
     → QA onayı → completed (yine AGENT çeker)
RED gelirse → revise → düzeltilir → tekrar test
```

**Kapatma yetkisi QA'da, kaydın eli sahibinde.** QA statüye **dokunmaz**, onay
handoff'u verir; `completed`'ı developer kendi çeker.

Bu ayrım `HANDOFF-QA-CLOSES-DEV` ile çelişmiyor — o kural **session** kapanışını
düzenliyor, ClickUp statüsünü değil (CA beş dosyada doğruladı).

⚠️ **Ayrı bir QA sub task'ı AÇILMAZ.** Katman denetimi o katmanın sub task'ında biter;
ayrı kutu aynı denetimi iki yerde gösterir — biri gerçek, biri türev, ve *"hangisi
doğru"* sorusu doğar. **"QA şu an ne bekliyor" sorusunun cevabı: `test` statüsündeki
sub task'lar.** QA'nın kendi sub task'ı yalnız tek başına duran bir iş için açılır
(push öncesi toplu değerlendirme, production audit).

### Kanıt zorunlu — statünün dayanağı

Kanıtı olmayan statü geçişi yapılmaz. Böylece *"bitti"* beyan olmaktan çıkıp **kayıt**
olur, ve kayıt yalan söylemez.

**Kanıt ROLE göre değil, ÇIKTI TÜRÜNE göre tanımlanır** (fabrika kararı 2026-08-12).
Yani *"BE ne kanıt verir"* diye sorulmaz, *"ortaya ne çıktı"* diye sorulur — aynı rol
farklı işlerde farklı çıktı üretir.

**Kod** çıktıysa commit hash · **denetim** çıktıysa onay handoff'u · **rapor/analiz**
çıktıysa dosya yolu + ölçüm sayısı · **canlı** çıktıysa push hash · **doküman** çıktıysa
yolu + commit.

**Local commit uzak repoda görünmez** — BE/FE/MB local commit'ler, push QA'da. Kanıt
`commit 9a3f2c1 (local, push bekliyor)` diye **işaretlenir**, yoksa doğrulayan taraf
*"yok, uydurmuş"* sanır.

### Süre — completed sonrası, kayıttan kayda

**Ölçülen tek şey `in progress`.** `Open` süresi ölçülmez, raporlanmaz, kapanış notuna
yazılmaz.

*Mert'in kuralı, 2026-08-12: "Open süresiyle ilgilenmiyorum, sadece in progress
istiyorum. Zincirde bir agent'ın uzun süre beklemesi başka işte olabilir, ben tercih
etmişimdir. **Agent'ın boşta beklemesi verimsizlik olarak okunamaz.**"*

⚠️ Bu bir çerçeve hatasıydı ve Clara yaptı: oturum boyunca `Open` süreleri ölçülüp
*"BE 108 dakikadır boşta"* diye raporlandı — **sorun gibi sunuldu.** Sıra Mert'in ve
PA'nındır; bekleme bir karardır. Doğru ölçüm yanlış kutuya girdi.

Agent `completed` çektikten **sonra** kendi `in progress` süresini ClickUp'tan çekip
tracked time'a yazar.

```
clickup_get_task_time_in_status(task_id)
  → status_history içinde status=='in progress' satırının total_time_minutes
  → clickup_add_time_entry(task_id, start, duration)
```

⚠️ **Süre okumanın üç tuzağı `clickup-duzeni` skill'inde** — alan adı çakışması
(`total_time_minutes` iki yerde, farklı şey söylüyor), `since`'in başlangıç olmaması,
timer'ın paralel çalışmaması. Ölçümleri ve vakaları orada; buraya kopyalanmaz.

Sebebi bu skill'in kendi kuralı: aynı gerçek iki yerde durursa biri bayatlar ve
*"hangisi doğru"* sorusu doğar. Süre okunacaksa o skill açılır.

**Burada geçerli olan tek kural: sayı hesaplanmaz, çekilir.** Elle hesaplanan süre ile
kayıttaki ayrışırsa hangisinin doğru olduğu tartışılır ve tartışma işi durdurur.

### Bağlam taşıma — kapsam açıklamada, DAYANAK yorumda

**Sub task açmakla iş bitmez, dayanağı da gitmeli.** Ölçüldü: PA discovery'yi yazdı,
sub task'ları açtı, ama discovery hiçbir yere bağlanmadı — UID işi alınca *"kapsam
var, gerekçe yok"* dedi ve haklıydı.

**Açıklama = KAPSAM** (ne yapılacak) · **Yorum = DAYANAK** (neden böyle). İkisi ayrı
ömürlü: dayanak değişirse yeni yorum düşer, kapsam sabit kalır.

PA her sub task'a **o katmanı ilgilendiren** risk kararlarını yorum olarak düşer —
kopya değil, katmana özel. Ve discovery kalıcı bir eve yazılır (`docs/` altına,
commit'lenir) — `/tmp` kalıcı değildir, zincirin ilk halkası uçar.

**Bu mekanizmanın çalıştığı ölçüldü:** UID, PA'nın yorumundaki bir nottan (*"farklı
süreli slotlar yan yana görünebilir"*) kendi planında olmayan bir gereksinim çıkardı
ve ızgarayı ona göre kurdu.

### Olay akışı ClickUp'ta — `status.md` ve `TASK-STATUS.md` KALKTI

Fabrika kararı (2026-08-12): olay akışı **sub task'larda zaten tutuluyor** — statü
geçişleri zaman damgalı, yorumlar dayanağı taşıyor, süre kayıtlı. Ayrıca `docs/` altında
bir olay dosyası tutmak **aynı gerçeği iki yerde** anlatır ve ikisi ayrışınca *"hangisi
doğru"* sorusu doğar.

Kalkanlar: `status.md` · `TASK-STATUS.md` · `DEVIR-{hedef}.md`.
Duran: `discovery.md` · `MODUL-BILGI.md` (*"neden böyle"* hafızası) · `MODUL-INDEX.md`.

⚠️ **Prod'da elle yapılacak işler** ana task'ın yorumuna `PROD İŞLERİ` başlığıyla
düşülür — `TASK-STATUS.md` kalktığı için o bilgi başka yere gitmez.

### Sabah dökümü — hatırlanmaz, okunur

Mesai bitiminde **ana task'lar `pause`**, sub task'lar olduğu gibi kalır. Ertesi sabah
durum ClickUp'tan okunur.

Dökümü Clara basar, **sana ve PA'ya** gider — agent'lara değil. **Sıra PA'nındır.**

```
Dün kaldığımız yer
  PRC-26 [pause]  └ FE  form validasyonu   [in progress]  dün 16:40
  PRC-27 [pause]  └ BE  sorgu              [test]         QA'da, dün 17:00'dan beri
  PRC-28 [pause]  └ —   sub task yok       PA henüz iş vermemiş
```

Üçüncü satır kritik: **sub task'ı olmayan ana task, hiç başlamamış iş demektir.**

⚠️ *"Kaldığın yerden devam et"* bir **hatırlatma**, iş emri değil — ama agent için
ikisi aynı görünür. Önce döküm basılır, **sonra PA sıra verir**, sonra agent hareket
eder. Ve agent oturumları gece kapandığı için hatırlatmaya **sub task + ana task ID**
eklenir; bellek ClickUp'ta, agent'ta değil.

### İş bitince — "sıradaki ne" PA'ya sorulur

Agent sub task'ını `completed` yapar, **PA'ya sorar** *"bittim, sıradaki ne"*. PA açık
sub task'lara bakar (yeni açmaz), önceliğe göre **atar**, agent `in progress` alır.

**Agent havuzdan kendi iş ALMAZ** — sıra PA'nındır.

Bunun yan faydası: *"işim bitti"* artık bir **olay**. Havuzdan kendi alsaydı sessizce
devam ederdi ve boşta çıktığı an hiç görünmezdi. Clara iki şeyi ölçer: **soru PA'ya
ulaştı mı** (taşımazsa agent bekler) ve **cevap ne kadar gecikti** — bu agent'ın hızı
değil **devrin hızı**.

### Clara'nın ölçtüğü üç şey

**Tıkanma** — bir sub task ne kadardır `in progress` ya da `test` statüsünde. (`Open`
sayılmaz — orada bekleyen iş henüz başlamamıştır ve bu bir karardır, arıza değil.)
**Kapasite** — bir agent'ta kaç açık sub task var.
**Darboğaz** — havuzda kaç iş bekliyor. *Personel kararı bu sayıyla verilir, sezgiyle
değil.*

Üçü de **ölçülebilir**, Clara'nın hatırlamasına bağlı değil.

### Sessiz arıza — yazma çağrısının dönüşü ölçüm değildir

ClickUp'ın create ve özet yanıtları **eksik alan döndürebiliyor.** Ayıran soru:
*bu alanı gördüm mü, yoksa yazma çağrısının söylediğine mi güveniyorum?* İkincisiyse
ölçüm değil beyandır — ve beyana bakıp düzeltmeye kalkarsan var olan içeriğin üstüne
yazarsın.

Vakalar, ölçüm ve doğrulama yöntemi `clickup-duzeni`'nde; buraya kopyalanmaz.

### Paylaşılan çalışma ağacı — `git add .` YASAK

Tek repoda birden çok agent çalışır (PA `docs/`, UID/FE kod, BE `api/`). `git add .`
çeken taraf **diğerinin yarım dosyalarını kendi commit'ine katar** — ve o an "kimin ne
yaptığı" kaybolur, yani çözülmek istenen şeyin tam tersi olur.

⚠️ **`git add .` kullanmamak YETMİYOR — stage ORTAK bir alandır.** `git add <kendi
yolun>` bile **mevcut stage'in üstüne** ekler; başkası dosyalarını stage'leyip henüz
commit atmadıysa onlar da senin commit'ine girer.

Ölçüldü: PA kurala tam uydu (`git add docs`), stage'i kontrol etti ve içinde FE'nin
**24 dosyası** çıktı. Commit atsaydı FE'nin yarım işini götürecekti.

**Üç adım, atlanmaz:**
`git add <kendi yolun>` → `git diff --cached --name-only` ile **doğrula** → yabancı
dosya varsa `git reset` + kendi dosyalarını tek tek ekle → commit → `git show --stat`.

⚠️ **`git reset` başkasını etkiler:** stage'i tamamen boşaltır, diğerlerinin
stage'lediği dosyalar da düşer (içerik kaybolmaz, yeniden stage'lenmeli). **Çektiysen
kanala haber ver** — sessiz yapma.

Build artıkları (`obj/`, `bin/`, `*.tsbuildinfo`) `.gitignore`'a — yol bağımsız
kalıpla (`obj/`, `api/**/obj/` değil).

⚠️ **Bu kural OY kanonunda YOK** — *"developer yalnız KOD commit'ler"* var, *"yalnız
KENDİ yolunu stage'ler"* yok. Yeni bir projede **iş vermeden önce hatırlatılır.**

