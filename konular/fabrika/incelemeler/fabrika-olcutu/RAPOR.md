# Fabrika ölçütü — zayıf noktalar ve saha davranışı

> **İş:** fabrikanın üretim kalitesi ölçümü
> **Durum:** yarım
> **Birleştirildi:** 2026-08-13 (önce 3 ayrı dosyaydı)

---

## Fabrika neye göre ölçülür — kuruluş oturumundan çıkarıldı

Tarih: 2026-08-03 (gece)

Mert sordu: *"Fabrikamız ne kadar iyi?"* — ve itiraz etti: ölçülecek şey ürettiği ürün
değil, **kendi yapılanması** (*"önce kendisi bizim istediğimiz gibi mi, onu bilmezsek
ürettikleri çöp olur"*).

İtiraz doğruydu ama bir eksik vardı: *"bizim istediğimiz gibi"* bir ölçüt değil, bir
dilek. Ölçüt yazılı değildi — **ta ki kuruluş oturumu okunana kadar.**

## Kaynak ve yöntem

`~/.claude/projects/-Users-karaok-p-ozel-yazilim-skill-project/a6c6fcb6-...jsonl`
— 13,5 MB, 6736 satır, 869 kullanıcı mesajı, 2026-07-31 23:26 → 08-03 11:39.

Bütün okunamadı (bağlamın birkaç katı). Dört paralel tarama yapıldı: niyet, kararlar,
kronoloji, zayıf noktalar. **Yöntem sınırı: taramalar anahtar kelimeye dayalı** — o
kelimelerle söylenmemiş bir şey kaçmış olabilir.

Aşağıdaki alıntılar Mert'in kendi cümleleri, birebir.

## Fabrikanın ölçütü — dört şart

### Bir: sıfırdan üretme

> *"OY v8 i düzelt bir kriter değil, sonuç adımı. Bizim bu ekipten beklentimiz OY v8
> hiç olmasaydı onu üretecekleri adımları bilemeleriydi."*

Bu ana ölçüt. Fabrika mevcut bir takımı onaran değil, **yokken kurabilen** ekip olmalı.

### İki: alan bağımsızlığı

> *"PR Yazılım için yazılım geliştirme ekibi kur başka bir konu ama marketing ekibi kur
> başka bir konu. Bizim üretici kadromuz bu ikisini de yapamazsa sorun doğar."*

> *"Mesela game development agent takımı kurmak istiyorum. Ya da N8n yönetim ekibi. Ya
> da bir haber portalı yönetim agent takımı — bu örneği sayısız çoğaltabiliriz."*

Yani fabrika yazılıma özgü olmamalı. Bugünkü kanonu bu açıdan hiç sınanmadı.

### Üç: kestirmeden yapmama

> *"PAM'a yeni bir agent takımı kurmak istiyoruz dediğimde ne yapacak, nasıl davranacak,
> hedefi ne — tamamen öğrenir ve **bunu kestirmeden yapmaz.** Bunun için çalıştığı
> reponun en büyük hakimi olmalıdır."*

> *"Bu gereksinimi belirlemek için ön hazırlık — bu çok uzun sürebilir, belki günler alır
> ama detaylandır."*

Yavaşlık burada bir kusur değil şart. Fabrikanın *"hız doğru çözüm değildir"* kuralı
buradan geliyor.

### Dört: bakım kabiliyeti

> *"Sahada 8 takım kurduk diyelim, 6 ay sonra behavior neredeyse hepsinde benzer ama bir
> şey değiştirmek istiyorum — tüm takımlarda bu düzenleme yapılmalı kararı alabiliyor
> muyuz? Yani genel agent takımlarımızın bakımından, yeni özelliklerden kim sorumlu?"*

Bu v7'nin ölçülmüş arızasının doğrudan karşılığı: *"bir kural değişimi günlerimi
alıyordu, mutlaka çelişkiler kalıyordu."*

## Rollerin ayrılma gerekçesi — Mert'in kendi cümleleri

**PAM ile PAD neden ayrı:**

> *"Lider sadece plan ve analiz yapmalı. İşi yazan, nereye yazacağını netleyen kişi
> uygulamacı olmalı. Takım liderinin netliği görevi tam anlamak olmalı."*

Ayrımın gerekçesi iş bölümü değil: **belirsiz talebi net gereksinime çevirmek kendi
başına bir iş.**

**PQA neden ayrı göz:** OY'deki QA akışına dayandırıldı —
> *"QA reddeder, developer düzeltir, onayda PA'ya bilgi gider. Burada da böyle olmalı.
> Sürekli 2 yere handoff taşınmaz."*

Push sahipliği: *"push işini QA yapmalı her zaman. Kendi body'sini kimse düzeltemez;
sorun PAM'a iletilir, PAM PAD'e, PQA inceler ve push'lar."*

**PCA neden var:** iki iş için — dış dünya araştırması (*"game developer ne bilmeli? İş
ilanlarına bile bakabilir, CV'ler inceleyebilir"*) ve etki analizi (*"6 takımda da bu
senaryo var der"*).

**Ve dörtlü sayısı bile sorgulanmak üzere verildi:**
> *"Bana kalırsa PA gibi, FSD, QA ve CA gibi bir dörtlüye ihtiyacımız var **ama asla
> doğru kabul etme.**"*

> *"Belki 2 agent üretip skill/command ile yönetimi daha doğru bulacağız. Amacımız tek
> doğruyu kabul edip işimize uydurmak değil."*

## Reddedilenler — kanona geçmeyen gerekçeler

Bunlar fabrikanın **ne olmadığını** tanımlıyor ve hiçbiri kanonda gerekçesiyle durmuyor.

**Orkestratör modeli reddedildi.** Claude *"sadece lider konuşsun, diğerleri arkasında
subagent olsun"* önerdi:
> *"Ben hepsiyle muhattap olmayı seviyorum. Handoff'u taşıma işi beni kontrollü tutuyor.
> Kime ne iş verildiğini görüyorum, bu sayede hatayı yakalayıp müdahale edebiliyorum."*

**Ortak çekirdek behavior plugin'i reddedildi.**
> *"Bence hiçbiri ortak olamaz. Çünkü fabrika behavior'a bak, web'e bak, OY'ye bak — her
> şeyi farklı bunların. İsimlendirmeleri bile farklı olmalı ki çakışmasınlar."*

**Toptan taşıma reddedildi.**
> *"Bence hiçbir şeyi direkt taşımayalım. Yavaş yavaş taşıyalım, ürete ürete gidelim."*
> *"Örnekleri inceleyelim, esinlenelim ama bire bir asla taşımayalım."*

**İlk `CLAUDE.md` üç kez reddedildi** ve gerekçesi bir kural üretti:
> *"Mesela 4 agent'i söylemesine gerek yok. İlerde 5 olursa ne olacak? CLAUDE.md üst
> bakıştır."*

**Okunmaz rapor reddedildi — üç kez.**
> *"Ürettiğin raporların hiçbiri insan okumasına uygun değil."*
> *"Bak yine kocaman bir duvar. 5 soru sordun, açıklamalar yazdın, hepsi yukarıda koca
> bir blok — hangisini okuyup yanıt vereyim, 10 dk sürer."*
> *"12 soru var ama hiçbirini anlamadım; dokümanı okumak zorunda değilim ki?"*

Bu üç kez tekrarlanan tek şikâyet. **Fabrikanın ölçütlerinden biri olmalı:** ürettiği
agent'ın çıktısı insan okunabilir mi.

## Fabrika bitmedi — beklemeye alındı

Kronoloji bunu net gösteriyor. 2026-08-02 23:35'te ilk fabrika commit'i düştü. Aynı
gece preload arızası bulundu ve 23:50'de:

> *"AG'ye yeni bir sürüm çıkartmasını söyledim. PAM ekosistemi şimdilik beklesin,
> fabrika yapısı vs hepsi beklesin."*

O günden beri fabrika üzerinde yapılan iş yalnız **kendi ayarları** oldu
(`docs/fabrika/` altında beş klasör: açılış hooku, atıf haritası, ekip kurulumu, hook
sonrası temizlik, tek muhatap).

Yani *"fabrika ne kadar iyi"* sorusunun cevabı: **bilinmiyor, çünkü hiç sınanmadı.**
Sınanmaya başladığı gece daha büyük bir arıza çıktı.

Ve `team/` klasörü boş — `dagitim` skill'i (20 kural) hiçbir gerçek paket üzerinde
denenmedi.

## Mert'in kendi teşhisi — sorun nerede

> *"Sorun fabrika mimarisinde bence. Agent body'de ne olmalı, hook nasıl kurulmalı,
> agent skill'i hangi aşamada okur nasıl tetiklenir... kesinleştiremediğimiz için
> ürettiğimiz dokümanlar teoride harika ama içerikleri doğru yönlendirmeyi taşımıyor.
> Sayısal ölçümler doğru ama pratik problemli ve **PAM sürekli sayı ölçüyor, kural
> ölçüyor, içerik akış progress'i doğru yorumlamıyor.**"*

> *"Docs folder'ı içinde o kadar fazla ölçüm yaptım ki. Binlerce analiz yaptım, binlerce
> gereksinim belirledim ama **yöntemi kuramadım.**"*

Bu ikinci alıntı önceki kuşağın teşhisiyle birebir aynı
(`kararlar/2026-08-02-clara-kurulumu.md` → *"Clara hep tasarladı, hiç iş yapmadı"*).
Yani örüntü kişide değil düzende: **ölçüm bol, kapanış yok.**

## Clara da sınanmak üzere kuruldu — ve sınanmadı

Aynı oturumda bu oda açıldı. Mert'in cümlesi:

> *"İşte o yüzden Clara'ya verelim bu işi dedim. Clara ilk saha deneyimini yaşasın.
> **Sonra onu ölçelim, bakalım gerçekten iyi mi, işi doğru yönetti mi?**"*

Bu ölçüm yapılmadı. `incelemeler/clara-ilk-sinama/kayit.md` kanonun **kurulum**
sınamasıdır (dört baskı testi, agent kullanılmadan önce); saha performansı ölçümü
değil.

## Sıradaki adım — karar bekliyor

Ölçüt artık var (yukarıdaki dört şart). Fabrikayı bu ölçütle okumak mümkün.

Ama asıl soru Mert'te ve bu turda soruldu, cevap alınmadı: **fabrika bugünkü hâlinden
devam mı edecek, yoksa preload dersiyle baştan mı kurulacak?**

İkisi farklı iş. Devam etmek fabrikayı ölçütle denetleyip eksik kapatmak; baştan kurmak
ise fabrikanın kendi kanonunu yeniden yazmak — ve o iş fabrikanın kendi eliyle
yapılamaz (`BHV-NO-SELF-CONFIG`).

---

# GÜNCELLEME — dört şartın durumu ölçüldü (2026-08-06)

Bu dosya ölçütü tanımlıyor. Ölçüt **değişmedi**; aşağıdaki satırlar şartların
2026-08-06'daki karşılanma durumunu ekliyor. Ölçümün tamamı:
`incelemeler/fabrika-denetimi/` (dört eksen + `eksikler.md`).

**Bir: sıfırdan üretme — KARŞILANMIYOR, en zayıf halka.**
Hedef cümle kanona geçmiş (`dagitim/SKILL.md:11`) ama **yöntem yok.** Bir takımın kendi
tasarımı — hangi roller, kaç personel, devir hattı — hiçbir dosyada tanımlı değil.
Elde iki uç var, arası boş: PAM'de 15 satır tutum (*"acele etme, günler sürebilir"*),
PCA'da ölçüm tarifi (*"hangi roller var"*) — ve `PCA-NO-PROPOSE-RULE` PCA'yı
bulgudan role geçmekten men ediyor. PAM'e verilen tek bitiş testi *"PAD katman kararı
verebilir mi"*, yani rol mimarisinin doğruluğunu ölçen eşik yok.
Ve `team/` boş: sahada bir kez bile denenmedi.

**İki: alan bağımsızlığı — BEKLENENDEN İYİ.**
123 kuralın hüküm cümlelerinin **hiçbirinde** yazılım domain terimi yok (`frontend` 0,
`API` 0, `.NET` 0, `React` 0; `backend` 2 / `developer` 5 yalnız gerekçe içinde biçim
örneği). Araç varsayımı yoğun (`plugin` 74, `push` 45) ama bu engel değil — marketing
takımı da plugin olacak. Gerçekten anlamsız kalan üç kalem var
(`ISD-APPEND-DONT-REWRITE`'ın ayrım ölçütü *"commit"*; `CLAUDE.md:199` kod varsayımı;
`behavior:209` grep talimatı). Asıl boşluk birinci şartla aynı.

**Üç: kestirmeden yapmama — KARŞILANIYOR, en iyi karşılanan.**
Bu şartı zorlayan kural yoğunluğu diğer dördünün toplamından fazla (`BHV-NO-RUSH`,
`BHV-READ-FULL`, `BHV-OPEN-SOURCE`, `BHV-NO-GUESS`, `BHV-SCAN-FIRST`,
`BHV-FOUR-PHASES`, `BHV-PROVE-DONE`, `BHV-BUILD-ON-FINDINGS` + üç üretim kapısı).
*"Günler alabilir ama detaylandır"* cümlesi `pr-agent-manager.md:81-88`'e neredeyse
birebir geçmiş. Yumuşak boşluk: *"reponun en büyük hakimi olmalı"* kısmı yazılı değil —
okuma yükümlülüğü iş bazlı, hâkimiyet bir durum ama kanondaki her şey bir refleks.

**Dört: bakım kabiliyeti — YUKARIDAKİ TESPİT GEÇERSİZ, düzeltiliyor.**
Bu dosyada *"kısmen — refleks var, mekanizma yok"* yazıyordu. **Yanlış:** madde
2026-08-02'de kapatılmış (`docs/fabrika/ekip-dogrulama/oturum-06-filo-bakimi.md`) ve o
tarih bu kaydın yazılmasından önce. Yapı var: sorumlu isimli (PAM,
`PAM-REPORT-FLEET-AGE`), yayılma sırası dört rolde tanımlı (`is-duzeni:267-327`), iki
kural koruyor.

Karşılanmama sebebi başka ve iki tane: **yapı sıfır kez koştu**
(`docs/filo/durum.md`: *"Son filo taraması — Yapılmadı"*) ve **cascade haritası boş**
(`atif_verenler` 112/123 kuralda boş, anılan 38 kimliğin 28'i atıfsız). Yani *"6 ay
sonra tüm takımlarda değiştirebilir miyiz"* sorusunun cevabı bugün haritaya bakarak
hayır — cascade elle grep gerektiriyor.

Mimari bedel (karar değil, bilgi): ortak çekirdek yok — 8 takımda bir behavior
değişikliği **8 ayrı iş** ve `ISD-ONE-TEAM-PER-TURN` bunu zorunlu kılıyor.

**Beş: insan okunabilir çıktı — YARISI KARŞILANIYOR, dördüncü tekrarda.**
Rapor **biçimi** için 7 kural var ve iyi yazılmış. Ama üç şikâyetten ikisinin geldiği an
— **soru sorma anı** — kanonun kapsamı dışında: `BHV-SHAPE-REPORT` kendi kapsam
cümlesiyle o anı açıkça dışarıda bırakıyor (`:373-376`). Soru sayısını sınırlayan ya da
blok biçimini düzenleyen kural yok; uzunluk sınırı sayı olarak hiçbir yerde yok
(`CLAUDE.md:132` tutum bildiriyor, kimliksiz ve *"agent üretirken"* kapsamına yazılmış).
`docs/filo/durum.md:120-133`: *"Dört oturumdur aynı şikâyet... Kapsamı çizilmedi, iş
açılmadı."* Tanınmış gerilim: `ISD-PRINT-AUDIT-RAW` denetim raporunun özetlenmesini
yasaklıyor, gerekçesi ölçülmüş.

## Açık soru kapandı

Bu dosyanın sonundaki soru — *"fabrika bugünkü hâlinden devam mı edecek, yoksa preload
dersiyle baştan mı kurulacak?"* — 2026-08-05'te Mert tarafından cevaplandı: **devam,
yapılandırılacak.** Ve 2026-08-06 ölçümü bu kararı destekliyor: teknik kat sağlam,
onarılacak mimari yok. Gerekçe: `kararlar/2026-08-05-sprint-planlama-kararlari.md`.


---

## Fabrika sahada nasıl çalıştı — vizyonla karşılaştırma

Tarih: 2026-08-03 (gece)

Mert sordu: *"Fabrikanın konuşmalarını oku — ne yapıyorlar, vizyona uygun mu
ilerliyorlar?"*

Ölçüt `kayit.md`'de duruyor (dört şart, Mert'in kendi cümlelerinden). Bu dosya
fabrikanın **fiilî davranışını** o ölçütle karşılaştırıyor.

## Kaynak ve yöntem

`~/.claude/projects/-Users-karaok-p-agent-project/` — 41 oturum tarandı (`git log`
değil, oturum kayıtları). Beş büyük oturum satır satır okundu, toplam ~4.700 satır.

Önce bir sayım yapıldı: hangi oturumlarda `Task`/`Agent` ile ekip personeli çağrılmış.
Sonuç: **41 oturumun 2'sinde.** Bu iki oturum ayrıntılı incelendi
(`90eeb9a2`, `58749256`), ayrıca üç büyük iş oturumu (`b34a383a`, `fedec8f1`,
`3fa67e0d`).

## Zincir çalıştı — ve iyi çalıştı

İlk sayım yanlış yorumlanabilirdi (*"2/41, zincir işlemiyor"*). Ölçüm tersini gösterdi:
zincir iki kez döndü ve **ikisinde de düzgün döndü.**

`58749256` oturumu (2026-08-03 akşamı) tam alternasyon yaptı: PAM → PAD → PQA → PAD →
PQA → PAD → PQA → PAD → PQA → PAD → PQA. **Beş PAD turu, beş PQA turu.**

**11 çağrının 11'i yapılandırılmış devir bloğuyla** başladı — `KİMDEN → KİME`, `TÜR`,
`NE`, `NEDEN`, `NEREYE BAK`, `BEKLEDİĞİM`. Serbest metin yok. Push çağrısında ayrı bir
`KULLANICI ONAYI` alanı ve Mert'in birebir cümlesi vardı (*"b onaylıyorum"*), PQA
bunu doğruladı: *"varsaymadım, bloktan okudum."*

**Beş denetim turu, dördü RED, toplam 7 bulgu.** Hiçbir tur *"onaylandı"* diye geçmedi.

PQA'nın en değerli yakalaması üçüncü turda: PAM işi *"kapandı"* diye gönderdi, PQA
commit eksiğini buldu —

> *"Working tree'de `rules-index.json` değişik, staged alan boş. Onay gelip push atarsam
> sahaya inen şey PAD'in düzelttiği hüküm değil, benim iki tur önce reddettiğim bayat
> hüküm olur. Dosya diskte doğru görünür. Bu ayrımı kimse fark etmez, çünkü herkes
> çalışma ağacını okur."*

PAM bunu üzerine aldı: *"Bu bulguyu ben kaçırdım ve kayda geçti."*

PQA hiçbir yerde beyanı kanıt saymadı — `git show`, `git log -S`, JSON parse, karakter
karşılaştırma ile ölçtü. Ve kendi sınırını korudu: *"Denetlediğim dosyaya dokunmadım
(`PQA-NO-FILE-EDIT`), çözüm önermedim (`PQA-NO-PROPOSE-FIX`)."*

**Kural ihlali bulunamadı.** PAD plan dışına yazmadı; yazma bloklandığında dolanmayı
denemedi ve yarım işi devretmedi (*"cascade yarım, PQA'ya devretmiyorum, PAM'a
dönüyorum"*). Commit PAD attı, push PQA attı — doğru bölüşüm.

PAD `general-purpose` çağırdı (7 kez) ama bu kanon gereği: yazdığı kuralı isimsiz
yardımcıya okutup davranış sınaması. Ve gerçek bulgu üretti: *"5 durum soruldu, biri
YANLIŞ çıktı. Suçlu metnimdi."*

## Kendi kusurunu bulma refleksi çalışıyor

Üç ayrı örnek, üçü de kimse söylemeden:

**PAD kapanışta:** *"PQA'nın denetlediğini göremiyorum, onun transkriptinde değilim.
'Denetimden geçti' yazmam beyanı kanıt saymak olurdu."*

**PQA ikinci turda:** kendi ürettiği bulgunun düzeltmesinde yeni bir bulgu buldu —
*"Bulgu 1 ve 2'nin düzeltilmesi sırasında aynı ayrışma bir kez daha üretildi, bu kez
ters yönde."*

**PQA daha önce (`fedec8f1`):** `ISD-KEEP-CHAIN-ONE-DEEP` hükmünün **sahayı yanlış
tarif ettiğini** ölçtü — hüküm *"`Task` yalnız PAM'de durur"* diyordu, ölçüm `Task`'ın
PAD'de de olduğunu gösterdi. Kural aynı gün düzeltildi (araçtan davranışa:
*"Personeli yalnız PAM çağırır"*).

**Ve PAM kendi hatasını dokümandan düzeltti:** push sonrası `WebFetch` ile subagent
dokümanını okudu ve *"sana 'sub-agent'lar yalnız arka planda çalışıyor' dedim, yanlış —
arka plan varsayılan ama zorunlu değil. Yani bu oturumdaki beş turluk karanlığı
önleyebilirdim"* dedi.

## Ölçütle karşılaştırma — dört şart

### Kestirmeden yapmama: ✅ karşılanıyor, hatta fazlasıyla

Beş turluk revize döngüsü, her turda ölçüm, hiçbir turda *"yeterince iyi"* denmedi.
Ama bunun bir bedeli var ve Mert onu söyledi:

> *"Baksana minik bir iş 2 saatimizi aldı, bu böyle olur mu hiç?"*

PAM savunmadı: *"Haklısın ve bunu savunmayacağım. Beş ayrı iş, dokuz commit. Bunlar
'minik iş' değildi — ama minik bir iş gibi başladılar, ve bence asıl problem bu."*

Yani şart karşılanıyor ama **iş kapsamının başta doğru ölçülmesi** ayrı bir boşluk.

### Bakım kabiliyeti: ⚠️ kısmen — refleks var, mekanizma yok

Fabrika bugün kendi kanonundaki üç hükmü düzeltti, biri sahayı yanlış tarif ettiği için.
Yani **kendi bakımını yapabiliyor.**

Ama filo bakımı (8 takım senaryosu) hâlâ sahipsiz — bkz. `zayif-noktalar.md`. Ve daha
somut bir kayıp var, `3fa67e0d` oturumunda tespit edilip iki gün sonra doğrulandı:

> *"Gerçek kayıp: öz-denetim komutları. Eski AG'de `AG-SELF-AUDIT-RUN` vardı — 'düzeni
> koruyan şey senin dikkatin değil, çalıştırdığın komut; dikkat yorulur, komut
> yorulmaz.' Bugün böyle bir şey yok. `.claude/` altında tek bir script yok."*

Doğrulandı: PQA index senkronunu **elle** Python one-liner'larıyla ölçtü, PAD index'i
`/tmp/index-guncelle.py` gibi tek kullanımlık script'lerle güncelledi. Bugün tuttu —
*"ama tutmasının sebebi kapı değil dikkat."*

### Sıfırdan üretme: ❌ hiç sınanmadı

**`team/` klasörüne bugüne kadar hiç commit atılmamış.** `git log -- team/` boş.
`team/team-1-oy/` var ama git'te izi yok.

Ölçülen üç büyük iş oturumunun **üçü de fabrikanın kendi yapılanmasıydı:**
- `b34a383a` (2,2 MB) — açılış hook'u + kendi personel body'leri + `CLAUDE.md`
- `fedec8f1` (1,2 MB) — aynı işin denetimi
- `58749256` (1,2 MB) — bağlam dosyası yetkisi (yine kendi kanonu)

Değişen her dosya `.claude/` ya da `docs/fabrika/` altında. Mert'in kendi kapsam
cümlesi bunu doğruluyor: *"Kapsam `.claude/skills/` ile sınırlı — `team/` altı dışarıda
kalmalı."*

Yani ana ölçüt — *"OY v8 hiç olmasaydı onu üretecek adımları bilmek"* — **hiç
denenmedi.** Fabrika adımları yazdı, 121 kurala bağladı, ama bir kez yürümedi.

### Alan bağımsızlığı: ❌ ölçülemez

Fabrika yalnız kendi üstünde çalıştı; farklı bir alanda (marketing, oyun, n8n) hiç
sınanmadı. Bu şart sıfırdan üretme denenmeden ölçülemez.

## PCA hiç çağrılmadı

İki zincir oturumunun ikisinde de `pr-agent-context-analyst` **tool çağrısı yok.**
Metinde 400'den fazla anılmış, bir kez çalıştırılmamış.

Bu bir ihlal değil ama bir işaret: dört personelin biri hiç iş görmedi. Kuruluşta
Mert'in şerhi vardı — *"dörtlüye ihtiyacımız var ama asla doğru kabul etme"* ve
Claude'un önerisi *"üçle başla, dördüncüyü ölçerek ekle"* idi. Dördüncü eklendi,
ölçüm yapılmadı.

## Harness kaynaklı iki kayıp

**`Task` oturum içinde aktifleşmiyor.** `90eeb9a2`'de PAM'in frontmatter'ına `Task`
eklendi ama oturum başında yüklenen araç listesi değişmedi:
*"Frontmatter değişikliği çalışan oturumda etkili olmuyor."* Sonuç: o oturumun
tamamı elle yürüdü — PAM 6 blok bastı, Mert taşıdı.

**`SendMessage` çalışmadı** (`"exists but is not enabled in this context"`). PAM
PAD'i devam ettirmek yerine her turda **yeni agent** açmak zorunda kaldı — beş turluk
döngünün her turu taze context. Bu, iki saatlik sürenin bir sebebi.

## Sonuç — fabrikanın sorunu kalite değil

Ölçülen davranış vizyonla **uyumlu**: zincir düzgün dönüyor, denetim gerçek bulgu
üretiyor, roller birbirine karışmıyor, kendi kusurunu buluyor, beyanı kanıt saymıyor.
Bunlar taklit edilemez şeyler — kanon davranışa dönüşmüş.

Uyumsuz olan tek şey **nerede çalıştığı.** Fabrika 121 kural, sekiz commit, üç kanon
düzeltmesi üretti ve hepsi kendi üstüne. `team/` boş.

Yani teşhis: **fabrika iyi kurulmuş, hiç saha görmemiş.** Ve kuruluş oturumunun kendi
uyarısı duruyor:

> *"Riskli olan bu hâl değil, bu hâlin uzaması. Boşta duran bir kanon zamanla
> gerçeklikten kayar ve kimse fark etmez."*

## Sıradaki adım — karar bekliyor

En küçük gerçek iş `team/` altına bir takım paketlemek. Bir hamlede dört şeyi birden
sınar: sıfırdan üretme adımları, `dagitim` skill'inin 20 kuralı (sıfır test), push
kapısı, ve alan bağımsızlığı (OY dışı bir alan seçilirse).

İkinci aday: öz-denetim script'i (`AG-SELF-AUDIT-RUN`'ın karşılığı) — çünkü bugünkü
denetim dikkate dayanıyor ve dikkat yorulur.


---

## Fabrikanın bilinen zayıf noktaları — kuruluş oturumundan

Tarih: 2026-08-03 (gece) · Kaynak: aynı oturum, `a6c6fcb6-...jsonl`, 6736 satır

Bu dosya `kayit.md`'nin eşi. Orada fabrikanın **ölçütü** var (ne olması gerektiği),
burada **kendi kanonunun kabul ettiği zayıflıklar** var.

Yöntem: dört paralel tarama, anahtar kelime eksenli. **Sınır: o kelimelerle
söylenmemiş bir şey kaçmış olabilir.**

Bir uyarı — transcript'te `[user]` etiketli uzun mesajların çoğu Mert'in değil, o
oturumda çalıştırılan **sınama agent'larının** raporudur. Aşağıda kimin söylediği
ayrılmıştır.

## En büyük boşluk — filo bakımı sahipsiz

Mert'in sorusu (kendi cümlesi):

> *"Sahada 8 takım kurduk diyelim, 6 ay sonra behavior neredeyse hepsinde benzer ama
> bir şey değiştirmek istiyorum — tüm takımlarda bu düzenleme yapılmalı kararı
> alabiliyor muyuz? Claude Code'a bir özellik geldi, hoop diye tüm agent'larda
> kullanılsın istiyoruz — bu taramayı nasıl yapıyoruz? Yani genel agent
> takımlarımızın bakımından, yeni özelliklerden kim sorumlu?"*

Oturumda **cevaplanmadı.** *"Ayrı bir oturuma bırakıldı, orada muhtemelen yeni bir rol
ya da yeni bir hat çıkacak"* denildi — **o oturum hiç olmadı.**

Dört alt soru sahipsiz kaldı: bir `behavior` değişikliği 8 ayrı iş mi açar; yeni Claude
Code özelliğini kim fark eder; `yapi-taslari` skill'ini kim güncel tutar (ölçülmüş
mekanik taşıyor — mekanik değişirse skill yanlışa döner); kimlik çakışmasını kim ölçer.

**Bu boşluk fabrikanın var olma sebebiyle aynı.** v7'nin ölçülmüş tek arızası bakım
zorluğuydu (*"bir kural değişimi günlerimi alıyordu"*). Fabrika onu çözmek için kuruldu
ve bakım sorusu fabrikada da sahipsiz kaldı.

`docs/filo/durum.md` ve `PAM-REPORT-FLEET-AGE` kuralı var — ama o yalnız *"tarama
tarihi eskiyse söyle"* diyor. Taramayı kimin yapacağı, neyi tarayacağı, bulguyu kimin
takıma çevireceği yazılı değil.

## Fabrika kendi skill'lerini hiç açmadı — ölçüldü

7 oturumun **7'sinde de `Skill` aracı çağrısı sıfır.**

Daha ağırı: dört fabrika oturumunda `skill_listing` attachment'ı da yok — yani
kullanılabilir skill listesi context'e hiç girmemiş.

PAD skill dosyalarına 29 kez erişti, hepsi `Read`/`Bash` ile ve hep aynı ikisine
(`is-duzeni` + `behavior`). **`uretim` ve `dagitim` gövdesi bir kez bile açılmadı.**

1.319 kural anması, 147 farklı kimlik sayıldı — ama çoğu *sayma* bağlamında, uygulama
değil. 32 hayalet kimlik: transcript'te var, kanonda yok.

## `dagitim` — 20 kural, sıfır test

İkinci en kalabalık skill. Üreten agent'ın kendi şerhi:

> *"`team/team-1-oy/` şu an boş ve bu repoda henüz `marketplace.json` yok — bu skill ilk
> gerçek paketlemeden önce yazıldı, kuralların hiçbiri gerçek bir artifact üzerinde
> sınanmadı."*

Ve soru-cevapla sınanamaz, çünkü kuralları mekanik. Tek yol gerçekten bir takım
paketlemek.

## Araç kısıtı sahada tutmadı

PQA'nın frontmatter'ında `Write`/`Edit` **yok.** Sahada **4 Write + 1 Edit** yaptı,
hepsi başarılı, hata dönmedi.

Ölçüm agent'ının cümlesi: *"beyan edilen tool seti sahada uygulanmamış — agent kendisine
tanımlanmamış aracı çağırdı ve harness izin verdi."*

Bu bugün OY tarafında ölçülen şeyle birleşince tablo tamamlanıyor
(`incelemeler/agent-arac-envanteri/kayit.md`): OY'de kısıt hiç yok, fabrikada kısıt var
ama **işlemiyor.** Yani *"denetçi kod yazmaz"* iki tarafta da yalnız metne dayanıyor.

## Çözülmemiş kanon çelişkileri

**`BHV-FLAG-INHERITED` ↔ `BHV-SCAN-BEFORE-CREATE`** — çakıştığı fark edildi,
*"bildireyim mi düzelteyim mi"* diye soruldu, **boşluk etiketiyle bırakıldı.**

**`BHV-RATION-ABSOLUTES` kendi metniyle çelişiyor** — kural mutlaklığı BÜYÜK HARFE
bağlanmış, ama aynı skill'de *"hiçbiri atlanmaz"*, *"rapora girmez"*, *"dokunma"* gibi
küçük harfli mutlak kipler var ve okuyan agent için aynı etkiyi yapıyor.
*"Ölçüt tipografi değil dil olmalı"* denildi, düzeltilmedi.

**PQA'nın kimlikleri kendi yasakladığı deseni taşıyor** (`PQA-NO-FILE-EDIT`,
`PQA-NO-PROPOSE-FIX` — `NO-` deseni). PQA kendi buldu ve *"ölçmediğim için bulgu diye
yazmıyorum"* dedi.

Örüntü tek cümleyle özetlenmiş: **"Kural bir tarafa yazılmış, karşı taraf boşta."**

## Kanonun yalnız yasak tarafı sınandı

Clara'nın kendi meta-ölçümü (aynı oturumda):

> *"Bütün testler 'şunu yapma' biçimindeydi, agent direndi. Yasak testleri kanonun
> güvenliğini ölçüyor, faydasını ölçmüyor. Elimizdeki güven, kapsadığı alanın
> yarısından geliyor."*

Yani fabrikanın *"doğru şeyi üretebildiği"* hiç ölçülmedi. Bugüne kadar ölçülen tek şey
yanlış şeyi üretmeyi reddettiği.

## Ortak `memory: project` denetimi deliyor

> *"PAD 'bu kuralı şu yüzden böyle yazdım' diye memory'ye not düşerse, PQA onu okur ve
> artık dosyaya değil gerekçeye bakar. Denetim biter. Ve ihlali sessiz: kimse memory'yi
> paylaşmaya karar vermedi, öyle geldi."*

Not: memory agent adıyla ayrışıyor (`.claude/agent-memory/<agent-adı>/`), yani teknik
karışma yok. Risk, ikisinin de aynı repoya yazması ve **memory'yi hiçbir denetimin
okumaması.** Clara bunu kurala bağlamayı önerdi, Mert: *"yok yazma."*

## Plandan sapmayı yakalayacak göz yok

> *"Boşluk bildirilmezse denetim zincirinde onu yakalayacak hiçbir göz yok — PQA planı
> değil dosyayı denetler, PAM revize turlarına girmiyor."*

`PAD-NO-SILENT-DEVIATION` bunu kurala bağlıyor ama kural agent'ın kendi bildirimine
dayanıyor; bildirmezse mekanizma yok.

## Ertelenmiş işler — hepsi aynı koşula bağlı

Neredeyse tamamı **"ilk gerçek takım kurulana kadar"**:

- v8'in yeniden ölçülmesi (adil sınav görmedi — kanonunun %91'ini görmemişti)
- Preload listesinin daraltılması (açılış maliyeti ~%15 context ≈ 30 bin token,
  21 bini skill)
- Kimlik öneki / namespace (8 takımda `BHV-NO-RUSH` çakışması gerçek risk ama
  ölçülmemiş ihtiyaca kural yazılmadı)
- PAM'in alan bilgisi toplama yöntemi (PCA body'sinde, ilk araştırmadan sonra skill'e
  terfi edecek)
- Fabrika ve CEO odası için hook (ikisi plugin değil; `CLAUDE.md`'ye açılış kuralı
  yazıldı, **denendi ve tutmadı** — agent kuralı gördü, *"devam edeceksek yükleyeceğim"*
  dedi. Mert: *"kalsın şimdilik böyle."*)
- Migration (164 bin kelime reference, ne kadarı gerekli bilinmiyor)

**Ve terfi hattı tanımlı ama koşmuyor:** *"Öneri kutusunda 40+ aday birikmiş, 'İşlenmiş:
henüz yok' yazıyordu. Terfi zinciri kuruldu ama koşmadı, çünkü kimse tetiklemiyordu.
Bu boşluk yeni değil, tekrarlıyor — ve bu sefer daha sinsi: bizde öneri kutusu bile
yok."*

## Açık kalan teknik sorular

**`SessionStart` matcher'ı** oturumun nasıl başladığını eşliyor (`startup|resume|clear|
compact|fork`), agent adını değil. `hooks.json`'da `"matcher": "ozel-yazilim:.*"`
yazılmış. Soru cevaplanmadı: eşleşmeyen matcher hook'u tamamen susturur mu, yoksa yok
sayılıp hook yine çalışır mı? *"Birincisinde telafi tamamen sessizce ölür."*

**AG'nin 16/16 doğrulaması nasıl yapıldı** — script doğrudan mı, hook zinciri üzerinden
mi? Doğrudansa matcher hiç sınanmamış olur. Soruldu, cevaplanmadı.

**GitHub issue'ları doğrulanmadı.** `#25834` gerçekten kapandı mı, düzeltme sürümü var
mı — *"eğer düzeltildiyse hook'a gerek kalmaz."* Oturumdaki şerh: *"bu linkleri ben
doğrulamadım, araştırmayı yapan agent getirdi."*

**`/doctor` + `/context` hiç koşulmadı** — 76 skill listeleme bütçesini taşırıyor mu.
İki kez teklif edildi, gerçek bir OY projesinde yapılması gerekiyor.

**Skill listeleme bütçesi context'in %1'i** ve taşınca **en az çağrılan skill'in
açıklaması düşürülüyor** → kendini besleyen sarmal: *"az çağrılan skill'in açıklaması
silinir → daha da az çağrılır → tamamen kaybolur."* 76 skill'lik kütüphane için
doğrudan risk, ölçülmedi.

**Kanıt eşiği yok.** `STD-GROUND-TRUTH` *"yaygınsa geçerli"* diyor, sayı vermiyor. Dış
sistemlerde de yok. *"Bu soruyu kimse çözmemiş, siz kendi eşiğinizi koymak
zorundasınız"* — konmadı.

**Kapıyı kim kapatsın — agent mı mekanizma mı?** Bugün QA push ediyor. Karşılaştırılan
sistemde CI kapatıyor, LLM yalnız yorum yapıyor. Cevaplanmadı.

## Kapanmamış kanon ihlali

`messaging/SKILL.md:40` örnek kodu `new HttpClient()` gösteriyor;
`data-access.md:49` bunu socket exhaustion gerekçesiyle yasaklıyor.
*"Örnek kod en çok kopyalanan şeydir."*

## Bu kayıttan çıkan tek sonuç

Fabrika **kâğıt üzerinde sağlam, sahada hiç sınanmadı.** Kendi kusurunu bulabildiği
ölçüldü (oturum-07 sayaç hatası), yasak tarafı direndiği ölçüldü — ama üretim tarafı,
bakım tarafı ve paketleme tarafı hiç denenmedi.

Ve oturumun kendi uyarısı duruyor: *"Riskli olan bu hâl değil, bu hâlin uzaması. Boşta
duran bir kanon zamanla gerçeklikten kayar ve kimse fark etmez."*


---
