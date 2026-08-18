# Ölçüm — kapsam çizerken hükmün yerlerini saymak

**Tarih:** 2026-08-14 · **Ölçen:** PAM (kendi deseni) · **Kayıt:** Clara

## Desen

PAM'in kendi cümlesi:

> *"Kapsamı çizerken hükmün **KENDİSİNİ** değil, hükmün **BULUNDUĞU YERLERİ** sayıyorum.
> Oysa aynı hüküm kimlik anmadan başka yerlerde de yaşıyor."*

## Üç vaka, aynı gün

| # | Ne oldu | Ne kaçtı |
|---|---|---|
| 1 | Kanal işinde kapsam **iki metinle** çizildi | Üçüncü metin çelişkinin **gerçek tarafıydı** |
| 2 | Body turunda **dokuz body arası** cascade düşünüldü | **Dosya içi** cascade hiç düşünülmedi → Bulgu 2 oradan çıktı |
| 3 | Revizede kapsam *"açılış paragrafı ile On-demand arası"* çizildi | BE satır 64'teki üçüncü iz dışarıda kaldı — PAD buldu |

Üçünde de **ölçüm doğru, kapsam eksik.** Sayılan yerler doğru sayıldı; sayılmayan yer
hiç görünmedi.

## Neden bu sınıf hata sessiz

Kapsam **geniş** yazılırsa: ölçülmemiş alan ölçülmüş sanılır — okuyan bir eksik görmez.
Kapsam **dar** çizilirse: ölçüm sınırlanır ama bu **görünür**, biri fark eder.

Buradaki üç vaka ikinci türden — ve üçünde de fark eden **başkası** oldu (PAD iki kez,
çelişkinin kendisi bir kez). Yani mekanizma çalıştı ama **bir tur maliyetiyle.**

## Kanonda karşılığı var

`ISD-CASCADE-COVERS-DESCRIPTIONS` tam bunu söylüyor: aynı hüküm kimlik anmadan başka
yerlerde yaşayabilir.

⚠️ **Yani eksik olan hükmün varlığı değil, uygulaması.** PAM'in kendi tespiti:
*"Kanonda hüküm zaten var."*

## Kural yazılmadı — gerekçe

Yeni kural yazmak burada **yama** olurdu (`CLA-FIX-THE-CAUSE`): mevcut hüküm doğru,
üstüne ikinci bir hüküm eklemek sebebi kaldırmaz.

**Sebep ne:** kapsam çizilirken sorulan soru *"bu hüküm nerede yazılı?"* — oysa
sorulması gereken *"bu hüküm başka nerede, başka adla yaşıyor olabilir?"*

Birinci soru bir **arama**, ikincisi bir **şüphe**. Arama tarama ile biter, şüphe
okuma ile.

## İzlenecek

Bu desen dördüncü kez görülürse — ve PAM dışında birinde görülürse — kişisel değil
**yapısal** demektir. O zaman hükmün kendisi değil, hükmün **nasıl uygulandığı**
sorgulanır.

---

## Ek — ikinci sınıf: YANLIŞ ADRES (2026-08-16)

Yukarıdaki üç vaka **dar kapsam**. Dördüncü bir vaka çıktı ve **ayrı sınıftan.**

**Ne oldu:** Clara, BE'deki *"PA'ya BİLGİ"* çelişkisini PAM'e taşırken karşı kaynağın
*"UID body'sinde ve `backend` skilinde"* olduğunu **söyledi.** PAM grep çekti —
`İSTİSNA` kelimesi o iki yerde **hiç geçmiyordu.**

Gerçek kaynak başka dosyadaydı: `is-akisi/references/ui-designer-is-akisi.md:64`.
Clara doğru satırı görmüş, **yanlış adresle taşımıştı.**

### PAM'in ayrımı — ve haklı

> *"Yanlış adres, dar kapsamdan DAHA tehlikeli. Dar kapsam eksik iş üretir — fark
> edilince tamamlanır. Yanlış adres ise üreticiyi olmayan bir kaynağa götürür; o da
> bulamayınca ya sorar (tur kaybı) ya kendi yorumuyla doldurur (**sessiz sapma**)."*

| Sınıf | Ne üretir | Görünür mü |
|---|---|---|
| **Dar kapsam** | eksik iş | evet — biri fark eder, tamamlanır |
| **Yanlış adres** | üretici kaynağı bulamaz | **hayır** — yorumla doldurulursa sessiz |

### Ayıran refleks

Kanonda zaten var (`CLA-LABEL-YOUR-EVIDENCE` + *"hangi kaynağa gittiğini doğrula"*),
ama bu vaka yeni bir kılıf gösteriyor: **doğru satırı okuyup yanlış dosyaya atfetmek.**

Arama sonucu birden fazla dosya döndürdüğünde hangisinden okunduğu **not edilmeli** —
"gördüm" ile "şurada gördüm" arasındaki fark, karşı tarafın bulabilmesi.

**Yakalanma sebebi:** PAM ölçtü. Clara *"doğrula, güvenme"* demişti — o satır olmasaydı
PAD yanlış kaynağa gidecekti.

---

## Ek 2 — üçüncü sınıf: ARACIN KENDİSİ (2026-08-16)

İlk üç vaka **dar kapsam** (muhakeme), dördüncüsü **yanlış adres** (aktarım). Beşincisi
ikisi de değil: **arama doğru yapıldı, araç yanlış cevap verdi.**

### Vaka — "dört body'de harita yok"

Clara ölçtü: *"Alan → skil"* haritası beş body'de var, dörtünde yok (CA, QA, TE, UID).
PCA satır bazlı ölçtü: **dokuz body'nin dokuzunda da iş→skill eşlemesi var.**

Doğrulandı (Clara, aynı gün): CA satır 54-55, TE 53-55, UID 60-63 — hepsinde
`X işi → \`skill\`` kalıbı duruyor.

**Farklı olan yalnız BAŞLIK:**

| Body | Başlık |
|---|---|
| BE · FE · MB · DO | *"Alan → skil"* |
| PA | *"İş türü → skil"* |
| CA · TE | madde işaretli, başlıksız |
| UID | düz satır |
| QA | yalnız tablo |

*"Yok"* sonucu **başlık aramasından** çıktı, eşlemenin yokluğundan değil.

### Neden bu ayrı bir sınıf

| Sınıf | Sebep | Çözümü |
|---|---|---|
| Dar kapsam | *"nerede yazılı"* diye arandı | **şüphelen** — "başka nerede, başka adla" |
| Yanlış adres | doğru satır, yanlış dosya | **not al** — hangi dosyadan okuduğunu yaz |
| **Araç körlüğü** | arama doğru, araç yanlış cevap verdi | **ölçüm biçimini değiştir** |

İlk ikisi muhakeme ile düzelir; üçüncüsü düzelmez — çünkü sorgulanacak bir muhakeme yok,
sorgulanacak olan **aracın kendisi.**

### PCA'nın ikinci bulgusu — backtick yutma

PCA ölçtü: tüm-gövde backtick araması, **satır sınırını aşan** backtick çiftlerini komşu
satırlardan eşleştirip aradaki metni **yutuyor.** BE'de aynı arama 4 vs 35 sonuç vermiş,
ve yutulan blokların başında haritanın kendisi varmış.

⚠️ **DÜZELTİLDİ 18:38 — arıza DOĞRULANDI, önceki not yanlıştı.**

İlk hâli: *"Clara doğrulamayı denedi, üretemedi — arıza PCA'nın sorgusuna özel olabilir,
doğrulanmadı."*

**PQA sınadı ve üretti.** Eksik adım bulundu: Clara **ham backtick** saymıştı; PCA'nın
yöntemi ham saymıyor, **gerçek skill envanterine (77 klasör) karşı eşleştiriyor.** O adım
eklenince:

| yöntem | sonuç |
|---|---|
| tüm gövde araması | **4** skill adı |
| satır satır arama | **35** skill adı |

Dosyadaki sayıyla birebir. Mekanizma da doğrulandı: BE gövdesinde **22 çok-satırlı
backtick eşleşmesi** var ve yutulanların içinde *"Alan → skil"* haritası duruyor.

### ⚠️ Asıl ders — "üretemedim" ≠ "yanlış"

PAM'in tespiti:

> *"Senin üretememen bir **çürütme** değildi, bir **tekrar denemesiydi** ve yöntemin bir
> adımı eksikti. İkimiz de bunu 'doğrulanamadı' diye işaretledik — oysa doğru etiket
> **'tekrarlanamadı, sebebi bilinmiyor'** olmalıydı."*

| Etiket | Ne yapar |
|---|---|
| *"doğrulanamadı"* | iddiayı **zayıflatır**, soru kapanır |
| *"tekrarlanamadı, sebebi bilinmiyor"* | soruyu **açık bırakır** |

PQA soruyu açık gördüğü için peşine düştü ve buldu. Kapalı etiketle kimse bakmazdı.

Bu `CLA-LABEL-YOUR-EVIDENCE`'ın bir kılıfı: **kendi ölçümünün başarısızlığını da doğru
etiketle.** *"Ben üretemedim"* bir gözlemdir; *"doğrulanmadı"* bir hükümdür.

### Ayıran refleks

**Bir yapıyı başlığıyla arama — kalıbıyla ara.** Başlık yazarın tercihi, kalıp işin
kendisi. Dokuz body'de aynı iş beş farklı başlıkla yazılmış ve dördü görünmedi.

**Ve iki bağımsız kişi aynı gün aynı araçla aynı tipte eksik ölçüm yaptı** (Clara ve PAM).
Bu, kişisel bir dikkat sorunu olmadığının işareti.

---

## Ek 3 — dördüncü sınıf: ADRES BAYATLAMASI (2026-08-16)

Öncekiler: dar kapsam (muhakeme) · yanlış adres (aktarım) · araç körlüğü (ölçüm biçimi).
Dördüncüsü **zamanla oluşuyor** — verildiği an doğruydu.

### Vaka

Clara PAD'e bir karar dosyasının adresini verdi (18:22, `2026-08-14-body-acilis-paragrafi.md`).
Sonra o dosyadaki gövde metni **değişti** (Tip 2 kararı, 18:25 — bir cümle çıkarıldı).

Adres hâlâ geçerli bir dosyayı gösteriyor ama **eski içeriği** taşıyor. PAD oradan alsaydı
silinen cümleyi geri getirecekti.

PAM yakaladı ve düzeltmeyi PAD'e bildirdi.

### PAM'in tespiti

> *"Bu `ISD-POINT-DONT-PASTE`'in bir yan etkisi: adres vermek kopyalamaktan iyi, ama
> **adres de bayatlıyor.**"*

### Neden kopyalamak da çözüm değil

| Yöntem | Riski |
|---|---|
| **Kopyala** | kaynaktan ayrışır — iki metin, biri güncellenir öteki kalır |
| **Adres ver** | kaynak değişirse adres bayatlar — aynı yol, farklı içerik |

İkisi de aynı sorunun iki yüzü: **bir bilgi iki zaman diliminde iki farklı hâlde.**

### Ayıran refleks

**Bir karar dosyası düzeltildiğinde, ona atıf veren açık devir blokları da güncellenir.**

Ayıran soru: *bu dosyanın adresini kime verdim ve o iş hâlâ açık mı?* Açıksa düzeltme
tek başına yetmez — atıf verilen yere haber gider.

Bu, cascade'in bir biçimi: değişen şey dosya değil, **dosyaya bakan gözler.**

---

## Ek 4 — sadeleştirme: dört sınıf değil, iki cümle (2026-08-16)

Yukarıda dört sınıf birikti. PAM bir sadeleştirme önerdi ve haklı:

> *"Üç ayrı vaka, üç farklı sebep — ortak olan tek şey **'tarama kapatmaz'**. Belki de
> kayda geçmesi gereken şey arızanın kendisi değil, o sonuç."*

### Üç kaçırma, aynı gün, üç ayrı sebep

| Kim | Ne kaçtı | Sebep |
|---|---|---|
| Clara | dört body'de "harita yok" | **başlık** arandı, kalıp değil |
| PAD | `self-check.md`'de eşleşme | *"AYNI"* büyük harfle yazılıydı |
| PCA | BE'de 4 vs 35 skill adı | backtick satır sınırını aşıyordu |

Üçü de **doğru arama** yaptı. Üçü de eksik cevap aldı. Sebepler ortak değil — çözümleri
de ortak değil. Ama **sonuç ortak.**

### Kalıcı hâli — iki cümle

**Tarama aday üretir, okuma kapatır.** Bir sorunun *"hepsi bu mu"* cevabı taramadan
çıkmaz; tarama nereye bakılacağını söyler.

**Bir yapıyı başlığıyla arama, kalıbıyla ara.** Başlık yazarın tercihi, kalıp işin
kendisi. Dokuz body'de aynı iş beş farklı başlıkla yazılmıştı.

⚠️ Yukarıdaki dört sınıf **silinmiyor** — vaka kaydı olarak duruyor, çünkü biri bir gün
*"bunu nereden biliyoruz"* diye sorar. Ama **kural olarak taşınacak olan bu iki cümle.**

### Beşinci vaka — PAM'in kendi tespiti

Ana argümanı *"borç var, temerrüt yok"* idi. Ama **karşı argümanında** BE'nin 21 vs 16
farkını kendi yazmıştı — yani tezini çürüten veriyi görüp *"karşı argüman"* rafına
koydu.

Bu dar kapsam değil (veri elindeydi), araç körlüğü değil (ölçüm doğruydu). Ayrı bir
şey: **kendi tezini çürüten veriyi ayrı bir başlığa koymak.**

Tek vaka — kural yazılmıyor. Ama işaret: *"karşı argüman"* bölümü bazen ana argümanın
mezarı oluyor ve yazan fark etmiyor.

---

## Ek 5 — altıncı sınıf: EKSİK ÖLÇÜT (2026-08-16)

Öncekiler: dar kapsam · yanlış adres · araç körlüğü · adres bayatlaması · karşı argüman
mezarı. Altıncısı **talimatın kendisinde.**

### Vaka

Clara kapanış talimatı yazdı: *"memory'sini düzenlesin — **biten işin** `project` kaydı
silinsin, ders kayıtları kalsın."* PAM aynen taşıdı, **üç agent'a** gitti.

**PAD sapma bildirdi ve haklıydı:** kendi `project_devreden-isler-20260816.md` kaydı
biten işin değil **devreden** işin kaydıydı. Silseydi kaybolacaklar:

- 2026-08-14 karar dosyasının gövde metninin **bayat** olduğu
- türetmenin bir kaynağı (PA'nın `dev-deploy` eşlemesi) **yok edeceği**

Yarın yeni oturum bunları bilmeden başlarsa **ikisinde de aynı hataya düşer.**

### Doğru ölçüt

> **Biten işin kaydı silinir, DEVREDEN işin kaydı kalır.**

Bu ayrım cümlede yoktu. İkisi de (yazan ve taşıyan) yalnız *"bugün biten iki işi"*
düşünüyordu.

### Neden ayrı bir sınıf

| Sınıf | Nerede |
|---|---|
| Dar kapsam · yanlış adres · araç körlüğü | **ölçümde** |
| Adres bayatlaması | **zamanda** |
| **Eksik ölçüt** | **talimatın kendisinde** |

Öncekiler bir şeyi *bulamamak*; bu bir şeyi *yanlış tarif etmek.* Ölçüm doğruydu — ölçüt
eksikti.

### ⚠️ Ayıran gözlem — uygulayan gördü

PAM'in cümlesi: *"Talimatı ben taşıdım, sen yazdın, **ikimiz de eksiği görmedik;
uygulayan gördü.**"*

Bu, bir yönetim dersi: **talimatı yazan ve taşıyan aynı körlüğü paylaşabiliyor** — ikisi
de aynı zihinsel resme bakıyor. Kıran şey, o talimatı kendi somut durumuna uygulayan
kişi.

Ve bu ancak **uygulayan bildirirse** görünüyor. PAD bildirmeseydi kayıt sessizce
silinecekti.

Kanonda zaten var (`CLA-ASK-BEFORE-WRITING-OUT`'un gerekçesi: hedef kıdemlidir, direktif
değil iş anlatılır) ama bu vaka yeni bir kılıf gösteriyor: **bir talimat da bir ölçüt
taşır ve o ölçüt eksik olabilir.**

---

## Ek 6 — asıl desen: kökü ölçen koymuyor (2026-08-16)

Yukarıda altı sınıf birikti. PAM bir üst-desen gösterdi ve üç vakayla destekledi.

### Üç vaka, hepsi aynı gün

| Kim ölçtü | Kaç kez | Kökü kim koydu |
|---|---|---|
| PQA — denetlenmemiş commit boşluğu | 4 | **PAD** (*"sahiplik iletim yükümlülüğünü kaldırmıyor"*) |
| PAM — dar kapsam | 3 | **Clara** (*"arama değil şüphe"*) |
| Clara — eksik ölçüt (kapanış talimatı) | 1 | **PAD** (*"biten ≠ devreden"*) |

Üçünde de **ölçen ile kökü koyan farklı kişi.**

### PAM'in tespiti

> *"Bu tesadüf olmayabilir: **kendi vakanı sayarken deseni göremiyorsun**, çünkü her
> vaka sana ayrı bir hata gibi görünüyor."*
>
> *"Kökü genellikle ölçen değil, **ölçüme dışarıdan bakan** koyuyor."*

### Neden böyle

Ölçen kişi **vakanın içindedir** — her vakanın kendi bağlamı, kendi gerekçesi var ve o
gerekçeler birbirine benzemiyor. PQA dört vakayı ayrı ayrı doğru ölçtü ve dördünü de
*"farklı yoldan yakalandı"* diye kaydetti. Ortak sebebi görmedi çünkü **farklılıklara
bakıyordu.**

Dışarıdan bakan kişi bağlamı bilmiyor — ve tam bu yüzden yalnız **ortak olanı** görüyor.

### Pratik sonucu

**Bir deseni kendi ölçümünden çıkarmayı bekleme.** Dört vaka biriktirdiysen ve kök
çıkmadıysa, bu senin dikkatsizliğin değil — konumun.

O zaman yapılacak şey daha çok ölçmek değil, **ölçümü başkasına okutmak.**

⚠️ Bu, `CLA-NO-CALL-TEAMS`'in ölçüm istisnasıyla uyumlu: isimsiz bir yardımcıya *"bu üç
vakada ortak olan ne"* diye sormak bir hüküm istemek değil, bir **bakış** istemektir.

---

## Ek 7 — yarım alıntı: ölçülünce DOĞRU çıkar (2026-08-16)

Bugünün en ince bulgusu ve öncekilerden yapıca farklı.

### Vaka

Clara bir karar dosyasından alıntı verdi:

> *"Arıza her açılışta tetikleniyor"*

Kaynakta cümle şöyleymiş:

> *"Arıza her açılışta tetikleniyor, **ama yalnız merkez kapalıyken görünüyor.**"*

**Kesilen kısım hükmün diğer yarısıydı.**

### ⚠️ Neden bu ayrı bir sınıf — PQA'nın ayrımı

| Alıntı türü | Ölçülünce ne olur |
|---|---|
| **Yanlış** alıntı | **ÇÖKER** — kaynakta yok, bitti |
| **Yarım** alıntı | **DOĞRU ÇIKAR** — grep eşleşir, devamına bakılmazsa görünmez |

PQA yarım alıntıyı grep'lediğinde **eşleşti** — yani *"doğru"* göründü. Bulduğu şey
eşleşme değil, **cümlenin devamına bakması** oldu.

### Kural hâli

**Alıntı doğrulaması *"bu cümle orada var mı"* ile bitmiyor — *"bu cümle orada BÖYLE Mİ
bitiyor"* diye devam ediyor.**

### Bu vakada ne kaybedilmişti

Kesilen yarım bir **soru** doğuruyordu ve o soru yarım alıntıda hiç doğmuyordu:

> **Merkez açıkken de tetikleniyorsa, kaç kez sessizce oldu?**

Bugünkü vakada arızayı görünür kılan şey **merkezin kapalı olması**ydı. Yani gördüğümüz
şey arızanın kendisi değil, **görünür olan kısmı.**

Ölçülmedi — yarınki gereksinimin kapsamına girdi.

---

## Ek 8 — gereksinimin yönü: eksik arama, katman ekle (2026-08-16)

PQA kendi risk tarifini düzeltti ve düzeltme **gereksinimin yönünü** değiştirdi:

> *"Adayın gerekçesi **'PQA'nın rutini kırılgan'** değil, **'tek rutin kırılgan, ikinci
> ölçüm gerekiyor'** olmalı. Fark önemli: birincisi **bende bir eksik arar**, ikincisi
> **zincirde bir katman ekler.**"*

### Neden bu ayrım kritik

Birincisi bir **yama** olurdu (`CLA-FIX-THE-CAUSE`): bir personelin dikkatini artırmaya
çalışmak — sebep yerinde kalır, üstüne uyarı eklenir.

İkincisi **sebebi kaldırıyor**: tek noktaya bağlı bir kapı, ikinci bir ölçümle yapısal
olarak güvenli hâle gelir.

### Ve o katman bugün zaten çalıştı — yazılı olmadan

Üç kez, üç ayrı elden:

| Kim | Ne yaptı |
|---|---|
| Clara | onay öncesi kapsamı ölçtü → **dokuzuncu commit** yakalandı |
| PAM | kapsamı üçüncü kez yeniden bildirdi → **üç→beş** değişimi görünür oldu |
| PQA | push anında ölçtü → rutin kapı |

**Gereksinim var olan bir davranışı yazıya geçirecek** — sıfırdan bir şey icat etmeyecek.
Bu, kabul edilme ihtimalini de yükseltiyor: kimse yeni bir yük almıyor, herkes zaten
yaptığını yazılı hâle getiriyor.
