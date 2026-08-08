# N8N otomasyon takımı — tasarım kararları

**Durum:** yarım (üretim PAD'de, push kapısında duracak)
**Başladı:** 2026-08-08 17:08 · Mert'in gereksinimi
**Not:** Mert bunu bir **test işi** olarak veriyor; ekip bilmiyor, onlar için gerçek üretim.

## Kapsam (Mert, 17:08)

Takım otomasyonu **hem tasarlar hem kurar** — çıktı bir tasarım dokümanı değil,
N8N sunucusunda çalışan otomasyon. Mevcut otomasyonların bakımı ikincil.

Erişim **belirsiz** işaretlendi. Clara ölçtü: iki repoda, ortam değişkenlerinde ve
MCP kaydında N8N'e dair hiçbir teknik iz yok.

## PAM'in ölçümü — tasarımı belirleyen üç mekanik

PAM `docs.n8n.io`'yu **kendi kararıyla** okudu (kaynak verilmemişti):

1. **Bir node gelen her veri öğesi için ayrı çalışır.** Tek öğeyle geçen otomasyon
   üç öğeyle kırılabilir — *"çalıştı"* tek çalıştırmayla kanıtlanamaz.
2. **Elle çalıştırma ile aktivasyon ayrı şey.** Editörde çalışan otomasyon tetik
   altında farklı davranabilir.
3. **Credential workflow'dan ayrı durur.** Otomasyonun mantığı taşınabilir,
   kimliği taşınamaz — "kuruldu" denen otomasyon credential eksikliğinden
   sessizce çalışmıyor olabilir.

### Erişim ucu — daraldı, kapanmadı

Public REST API **var** (dokümanda *"GUI'de yapabildiklerinizin çoğu"*; bir
*"API'yi kapat"* talimatının bulunması varsayılanın açık olduğunu gösteriyor).
Ama **yüzeyi ölçülemedi** — endpoint listesi, kimlik başlığı, credential'ın
API'den yönetilip yönetilemediği. Dört deneme, dördü 404; `docs.n8n.io`
sitemap'inde public API bölümü yok. PAM tahmin etmedi, ölçemediğini söyledi.

**Neden kritik:** API workflow oluşturabiliyorsa takım otomasyonu doğrudan kurar.
Kuramıyorsa üretebileceği en fazla içe aktarılabilir bir tanım olur — yani
*"hem tasarlar hem kurar"* kapsamı **teknik olarak karşılanamaz.**

## Rol sayısı kararı — dört

**PAM'in çıkarımı (emsal ölçümünden):** rol sayısı fazlardan değil **ayrık
malzeme sayısından** çıkıyor.

Faz ekseni iki emsalde de özdeş (planla → üret → statik denetle → dinamik koştur
→ dağıt). 9−7=2 farkın **tamamı** üretici rolünün bölünmesinden: OY'de yığınlar
ayrık (backend/frontend/mobil, kod paylaşımı yok, aralarında `API.md` **sözleşmesi**
var), WS'de üretici tek çünkü devredilecek şey yok.

**Malzeme ayrıksa sözleşme gerekir, sözleşme varsa rol sınırı oradan geçer.**

N8N'de o koşul **yok** — node'lar aynı tuvalde, aynı veri yapısını paylaşıyor,
elle senkronlanan sözleşme dosyası yok. Yani OY'nin üç üretici rolünü doğrulayan
koşul burada mevcut değil.

```
planlayan/gereksinim  otomasyon ihtiyacını gereksinime çevirir
üreten                workflow'u kurar (node, bağlantı, expression)
koşturan/doğrulayan   gerçek veriyle koşturur, veri çokluğunu sınar
denetçi + kapı        kanona uygunluk + aktivasyon kapısı
```

**Koşturanın ayrı kalma gerekçesi mevcut:** veri-çokluğu mekaniği. Üretenin kendi
otomasyonunu tek örnek veriyle doğrulaması *"sahte yeşil"* üretir (emsalin kendi
terimi). **DO/altyapı rolü yok** — sunucu zaten var, kurulacak altyapı yok.

## Üç rol kesişmesi

**(a) üreten ↔ koşturan** — üretenin kendi işini denemesi kaçınılmaz. Sınır
*"kim çalıştırır"* değil, **"kim hüküm verir"**. Emsalde iki farklı çözüm var;
OY'ninki seçildi (kanıt üretende, kapı davranış testi yapmaz). Gerekçe: WS'de
sınır bulanıklaşıyor, yeni bir takımda bulanık sınırı baştan almanın sebebi yok.

**(b) denetçi ↔ koşturan** — koşturanın bulgusu akışı **durdurmaz**, denetçininki
durdurur.

**(c) planlayan ↔ üreten** — **PAM'in kendi bulduğu, emsalde karşılığı yok.**
N8N'de gereksinim ile tasarım birbirine çok yakın: *"her yeni müşteri kaydında
şunu yap"* neredeyse node dizisinin kendisi. Emsalde iş dili ile teknik dil
arasında doğal mesafe var, burada o mesafe küçük. Önlem yazılmazsa planlayan
fiilen tasarım yapar, üreten kopyalayıcı olur. **Gereksinimin en özgün kalemi.**

## Doğrulama eşiği — üç kademe

*"Başarılı çalıştı"* ile *"doğru çalıştı"* ayrı şey:

1. Elle çalıştırma geçti mi (**en zayıf kanıt**)
2. **Çok öğeli** veriyle geçti mi (asıl risk — node her öğe için ayrı koşuyor)
3. **Aktif** hâlde tetikle geçti mi (elle çalıştırma bunu kanıtlamaz)

**Şerh:** bazı hata ayıklama özellikleri (Debug in editor, pinned data) dokümanda
*"n8n Cloud ve kayıtlı Community planları"* için yazılı. Bizim sunucuda geçerli mi
**ölçülmedi** — geçerli değilse doğrulama yöntemi değişir.

## Üç kırılgan yer

1. **Erişim ucu** — takımın ne yapabileceği buna bağlı, diğer her şey bunun
   üstüne kuruluyor.
2. **Credential** — workflow'dan ayrı; "kuruldu" denen otomasyon kimlik eksik
   olduğu için çalışmıyor olabilir ve bu **sessiz arıza**. Ayrıca: agent bir
   credential'ı görmeli mi? Yeni bir risk sınıfı.
3. **Aktivasyon** — geri alınamaz. Push yanlış giderse revert var; aktif
   otomasyon yanlış giderse **yapılmış iş yapılmış olur.**

## Kararlar

**Clara'nın verdiği (Mert'in önceki kararlarından türetildi):**

- **S2 erişim** → "bilinmiyor" (Mert 17:08). Üreten rolün tanımı **iki dallı**
  yazılacak: A) API ile doğrudan kurar, B) içe aktarılabilir tanım üretir.
  Karar gelince dal seçilir, tasarım yeniden yazılmaz.
- **S3 sunucu yönetimi** → takımın işi **değil.** Mert *"n8n'de yapmak
  istediğimiz otomasyonları yönetecek"* dedi — sunucuyu değil.
- **S4 aktivasyon** → **kullanıcı onayıyla.** Bu ekosistemde geri alınamaz her iş
  kullanıcı onayına bağlı (push kapısı, prod müdahale).

**Mert'e giden (17:21 itibariyle açık):**

- **S1 — otomasyon çeşitliliği.** Tek tip mi, çok çeşitli mi? Not: çeşitlilik
  çıksa bile PAM'in ölçütüyle bölünme haksız (sözleşme yok).
- **S5 — agent credential görebilir mi?** Görmezse "kuruldu ama çalışmıyor"
  riski, görürse agent'a kimlik bilgisi yetkisi. **Yeni risk sınıfı.**

İkisi de rol sayısını değiştirmiyor — dört rol iskeleti ikisinden bağımsız yazılabilir.

---

## Çapraz kontrol TUTTU — iki uç bağımsız aynı sonuca vardı (17:23)

PAM ve PCA'ya aynı soruyu sormadım; PAM gereksinim çıkardı, PCA emsali okudu.
İkisi de **7→9 farkının yeni rol değil, tek üretici rolünün bölünmesi** olduğunu
buldu ve ikisi de bölünmenin koşulunu **sözleşme** olarak gösterdi.

**PCA bölünmenin bedelini sayıyla ölçtü:** A ailesinde `API.md`/contract/sözleşme
kelimesi **sıfır kez** geçiyor — tek üretici olunca sözleşme kafanın içinde kalıyor.
Bölününce yazılı kontrat zorunlu olmuş ve etrafına kapı zinciri kurulmuş
(BE yazar → QA kilitler → PA tetikler → FE/MB tüketir). Üstelik BE ile FE/MB
arasında **doğrudan handoff yok** — üçü de tek adrese veriyor.

**Karara etkisi:** rol bölmek ücretsiz değil, **bir sözleşme + bir kapı zinciri
maliyeti** getiriyor. N8N'de bölünmeyi haklı çıkaracak ayrık malzeme yok.
Dört rol kararı iki bağımsız ölçümle destekleniyor.

### PCA'nın iki yapısal bulgusu — üretime taşınacak

**Şablon tutarlılığı iki ailede farklı.** A: 10-11 bölüm BÜYÜK HARF. B: 7 bölüm
cümle dili, **dokuz rolde sıfır sapma**. Ve B'de body'ye hangi kuralın gireceğine
dair bir **seçim ölçütü** var, A'da yok — dokuz dosyada birebir aynı cümle:
*"ihlali SESSİZ olduğu için anılır"*. N8N takımı B iskeletini almalı.

**A'da iki çakışma var, B'de ayrılmış.** (a) *"Etki analizi"* hem PA'nın hem
CA'nın YAPAR sütununda, aynı Türkçe tetik iki description'da birden; B'de
`PA-IDENTITY-NO-DETECT` ile ayrılmış ve **sınır araçla değil ÇIKTIYLA** ölçülüyor.
(b) QA ve CA aynı adla, aynı dizine, aynı grep'le rapor üretiyor.

### Fabrikanın kendi kanonunda arıza — Clara doğruladı

`web-fullstack-developer.md:70`: *"Tool seviyesinde de kapalı (frontmatter
`tools:` whitelist'inde `Agent`/`Task` YOK)"*. **Ölçüm: yedi dosyanın hiçbirinde
`tools:` alanı yok** (`grep -c "^tools:"` → hepsi 0).

Metin var olmayan bir mekanizmaya **güvenlik dayandırıyor.** Ve bu bir kaza değil:
2026-08-07'de Mert *"hiçbir agent'a `tools:` kısıtı yazılmaz, yasak araca değil
hedefe bağlı"* kararını verdi. Alan kaldırılmış, ona atıf veren cümle kalmış.

`kararlar/BEKLEYEN-cerceve-cumlesi-geride-kaliyor.md` örüntüsünün **yeni vakası** —
ve N8N takımı bu emsalden üretileceği için **şimdi yakalanmazsa kopyalanır.**

### PCA'nın kendi şerhi

*"Skill/reference/hook katmanı okunmadı — body'ler kuralın gövdesini skill'e
havale ediyor, yani kanonun büyük kısmı bu ölçümün dışında."* Ayrıca hangi ailenin
daha yeni olduğu ve hangi ayrımın **sahada** tuttuğu ölçülmedi — bu bir **metin**
ölçümü. Boşluk PCA'ya iş olarak geri verildi (17:24).

---

## Skill katmanı ölçümü — PCA, 17:41

Rapor: `agent-project/docs/fabrika/n8n-takimi/emsal-skill-katmani-bulgu.md`

### İki aile aynı hacmi farklı paketlemiş

```
A (websitesi)    16 skill ·  3.602 skill +  8.181 reference = 11.783
B (ozel-yazilim) 76 skill ·  6.609 skill +  5.899 reference = 12.508
```

Toplam fark %6 — pratikte aynı. Fark hacimde değil **yerde**: A ağırlığı
**reference**'ta tutuyor (%69), B **skill**'de (%53). Skill başı ortalama:
A 225 satır, B 86.

**Mekanik sonucu kritik:** reference `Read` ile açılır — agent onu **bilerek**
açmalı. Skill description ile **tetiklenir**. Yani aynı bilgi, bir düzende
kendiliğinden gelir, diğerinde aranması gerekir.

Somut örnek: frontend bilgisi A'da tek skill (299 satır) + 7 reference; B'de
omurga (91) + altı ayrı skill (component/form/list/style/data-access/screen).

### B'nin üç katmanı — skiller kendini etiketliyor

`omurga 10 · öz skili 31 · alet skili 28`. Kalan 61 skill hiçbir frontmatter'da
yok ve bu **eksik değil tasarım**: omurga bir *"alet çantası"* tablosu taşıyor
(iş → skill eşlemesi).

**Bölünme ekseni konu değil, ROLLERİN KESİŞTİĞİ YER.** 18 skill "uçlu" deseninde:
*"Üç uçlu: BE ÜRETEN uç, FE+MB TÜKETEN uç"*. Kapanış klişesi hep aynı:
*"Tek kaynak: kopyalamaz, buraya atıf verir."*

### Skill dağıtımı bir YETKİ mekanizması

`clickup/SKILL.md:49` — *"clickup skili BE/FE/MB/UID'in çantasında yok (ölçüldü:
4 agent body'sinde 0 hit) — yani statü set etme görevi verilse fiilen yapılamaz."*

**Yasak yazmadan yasaklamak.** N8N takımında üreten rolün N8N'e yazan tek rol
olması aynı mekanizmayla kurulabilir.

### `URT-BODY-BY-SILENCE` ölçütü skill tarafında da var

Ama **farklı işlevde**: body'de kuralın neden **anıldığını**, skill'de neden
**var olduğunu** gerekçelendiriyor (bir skill bütünüyle *"sessiz-hata sınıfı"*
diye etiketlenebiliyor).

**İş bölümü kuralı:** dokuz omurganın dokuzunda aynı açılış — *"Bu skil X'i
ANLATMAZ (o Y)"*. Ve çatışma çözümü yazılı: `is-akisi/SKILL.md:100` —
*"çelişki varsa MATRİS KAZANIR, body düzeltilir."*

**A'da skill sınıf taksonomisi YOK** (alet/öz etiketi 0/16, "Tek kaynak" 0/16).
Tetikleyici listesi yalnız 2/16 skill'de; B'de seçim mantığı *"kullanıcının
ağzından çıkacak hâl"* — teknik terim değil **şikâyet cümlesi**.

### Arıza yaygınlığı — beş vaka, üçü aynı örüntü

PCA verilen dört deseni **başlangıç** saydı, beş ayrı eksende taradı
(*"tek eksene dayansaydım körlük üretirdi"*). Beş gerçek vaka, dördü A ailesinde:

1. `tools:` whitelist iddiası (A) — tek satır, tek dosya
2. Preload listesi eksik (B) — gövdede kullanılan skill preload satırında yok
3. Erişilemez kaynağa atıf — **ve önemli bir ayrım**: A *"önce kanona bak: <yol>"*
   diyor (**uygulanamaz** talimat), B *"bu plugin'den ERİŞİLEMEZ — AG'ye iletilir"*
   diyor (**uygulanabilir** yönlendirme). Aynı bilgi, biri kullanılamaz.
4. Tanımsız kimlik (A) — `I8` üç yerde atıflı, hiçbir yerde tanımlı değil
5. Ayrışmış çift kaynak (A) — aynı hüküm iki dosyada tam metin, gerekçeleri
   **zaten farklı**. Çift kaynak bilinçli tutulsa bile ayrışıyor.

**Sonuç: arıza yaygın DEĞİL ama sınıfı tekrar ediyor.** 1, 3 ve 4 aynı örüntü —
*kaynak taşınmış/kaldırılmış, atıf veren cümle geride kalmış.*
`kararlar/BEKLEYEN-cerceve-cumlesi-geride-kaliyor.md`'nin üç yeni vakası.

**Temiz çıkanlar (kapsam beyanı):** reference yolları A 7/7 mevcut · kimlik
atıfları A 6/6 mevcut · "Preloaded" iddiası iki ailede de **destekli** —
ikisinde de SessionStart hook'u var ve upstream bug numarasıyla
(`claude-code#15178`) boşluğu bilinçle telafi ediyor.

### PCA'nın kendi şerhi

Reference **gövdeleri** okunmadı (14.080 satır) · üretici katman (`marketplaces/`)
kapsam dışıydı, `uretim-standardi` skill'inin kendisi okunmadı — **fabrikanın
kanon üretim standardı orada yaşıyor olabilir, N8N işi için doğrudan girdi** ·
ve hangi granülerliğin (16 mi 76 mı) sahada **daha az hata ürettiği ölçülmedi**.

---

## PQA denetimi — kanonun zemini sorgulandı (18:29)

PQA gereksinimi onaylamadı, **altındaki zemini** sorguladı. Sekiz bulgu; dördü
doğrudan tasarımı değiştiriyor.

### En sert bulgu: test kanonu doküman için yazılmış

Kanondaki üç test kuralı (`PAD-TEST-BEFORE-HANDOFF`, `URT-NO-AUDIT-WITHOUT-TEST`,
`ISD-SHOW-TEST-SCOPE`) **doküman üretimi** için kurulmuş. Birincisinin kendi
gerekçesi (body 198-200): *"PQA kuralın YAZILIŞINI denetler, İŞLEYİP İŞLEMEDİĞİNİ
değil."*

Doküman için doğru. **N8N'de bozuluyor** — orada ürün zaten bir işleyiş.
Workflow JSON'ı kanona uygun yazılmış olabilir ve çalışmayabilir.

**Sonuç:** mevcut kanonla PQA bir N8N çıktısını onaylarsa onayladığı şey
*"dosya doğru yazılmış"*tır. *"Otomasyon çalışıyor"* iddiasını denetleyen
**hiçbir kural yok.**

### Çatışma adayı: denetçi doğrulayamıyor

`PQA-NO-FILE-EDIT` (denetlediğine el sürme) ile `PQA-VERIFY-DONT-TRUST`
(beyanı kanıt sayma, ölçümü kendin yap) dokümanda çelişmiyor — okuyarak ölçmek
mümkün. N8N'de çelişiyor: *"çalıştırarak ölçmek dokunmak mı, değil mi"* —
**kanonda cevabı yok.** İki kural ilk kez aynı yerde.

PQA bir emsal de gösterdi: `DAG-BUMP-BY-AUDITOR` zaten *"PQA'nın dosyaya el
sürmeme kuralının TEK istisnası"* ve gerekçesi yazılı (*"sebep rol değil SIRA"*).
Ama **ne yapılacağını söylemedi** — `PQA-NO-PROPOSE-FIX`'e uydu.

### Dört kapının dördü de İÇERİ bakıyor

`URT-NO-PRODUCTION-WITHOUT-NEED` · `URT-NO-AUDIT-WITHOUT-TEST` ·
`URT-NO-PUSH-WITHOUT-AUDIT` · `ISD-COMMIT-THEN-PUSH` — dördü de **repo** içine
dokunan işe göre kurulmuş. En riskli kapı (push) bile yalnız git'i koruyor.

**N8N'de ürün kabul edilmeden ÖNCE bir sunucuya yazılıyor olabilir — yani en
riskli an, kanonun hiç kapı koymadığı an.**

Ölçüm: *"prod / canlı / geri dönüşü olmayan zarar"* ifadeleri tüm kanonda **tek**
yerde geçiyor (`BHV-RATION-ABSOLUTES`) ve orada bile bir **yazım** ölçütü —
*"mutlak ne zaman yazılır"*. Dış sisteme dokunan **işi** düzenleyen hüküm yok.

### DAG sayımı keskinleşti

PQA ölçtü: `team/team-1-oy/` var ama **içi tamamen boş (0 dosya)**, ve
`.claude-plugin/marketplace.json` **hiç yok.** Yani DAG'ın 26 kuralının hiçbiri
bir kez bile koşmadı — **26/26 sınanmamış.**

```
14 gerçekten devreye girecek   paketleme (5) + hook (6) + sürüm (3)
 5 muhtemelen                  MCP (3, N8N konuşacaksa) + kurulum (2)
 7 yine boşta                  sistem paketi · izin ayrımı · ad/renk/ikon
```

**PQA'nın notu:** boşta kalan 7 kozmetik değil — *"koşulmadan doğru
sanılacaklar."*

Ayrıca `DAG-RUN-HOOK-SCRIPTS` **kendi kaynağında** *"bugün bu makinede tek başına
kanıt sayılabilecek script YOK"* diyor. Yani hook doğrulama tarafı zaten bilinen
bir boşluk üstüne oturuyor — bu işte ilk kez bedeli ödenecek.

### PQA'nın kendi şerhi

*"DAG'ın 26 kuralının gerekçeleri ÖLÇÜMDEN değil TASARIMDAN geliyor. Bu iş onları
ilk kez sınayacak; sınanan kuralın yanlış çıkması bir başarısızlık değil, ölçümün
ta kendisi."*

---

## PAD'in ölçümü — iki kanıtlı kapanış (18:30)

**`uretim-standardi` PAD'in kanonunda YOK.** Üç yoldan kanıtladı: skill listesinde
yok (beş skill var: behavior, is-duzeni, uretim, yapi-taslari, dagitim) ·
`rules-index.json`'da `STD-` prefixi **sıfır** · fabrikanın hiçbir dosyası ona
atıf vermiyor (grep temiz).

**Yani PCA'nın işaret ettiği boşluk gerçek:** fabrikanın üretim standardı v7
kuşağında kalmış (268 satır + 6 reference), bugünkü üreticinin **elinde değil.**
PAD skill'i okudu, kendi kanonuyla farkını ölçüyor.

**İki dallı rol tanımının kanonda emsali YOK.** 139 kural tanımının hiçbiri bir
rolü iki dallı tanımlamıyor; koşullu görünen 6 tanesi kuralın *uygulanıp
uygulanmayacağını* belirliyor, rolün *ne yaptığını* ikiye bölmüyor.

**Ters yönde emsal buldu:** `YT-ASSUME-BACKGROUND` belirsizliği dallandırmıyor,
**tek varsayıma sabitliyor.**

**Bu Clara'nın kararına karşı bir bulgu** (üreten rolü iki dallı bırakma kararı,
17:21). Kayda geçti; PAD'in tam cevabı beklenecek.

---

## Denetim GEÇMEDİ — kapı çalıştı (18:33)

PQA gereksinimi **reddetti**: altı bulgu, ikisi üretimi bloke ediyor.
Kendi kapsamını da yazdı: 592 satır tam okuma (diff değil), PCA'nın 450 satırı,
iki commit doğrulaması, anılan dört kimliğin index'e karşı tek tek kontrolü.

**B1 — merkez koruması yarım.** Fabrikada koruma **iki parçalı**, gereksinim
birini almış. Ve kapanış bölümü **edilgen** yazılmış (*"sonuç planlayana DÖNER"*).
PQA'nın gösterdiği tarih: fabrikada aynı kural 2026-08-07'de **özne kazandı,
çünkü öznesiz hâli sahada kırıldı** — üç commit denetlenmeden kaldı, çünkü
hiçbiri kendine *"ilet"* demiyordu. Yeni takım aynı cümleyle başlıyor.

**B2 — PCA'nın İKİNCİ ölçümü gereksinimde yok.** `emsal-skill-katmani-bulgu.md`
(510 satır, 92 SKILL.md) hiç işlenmemiş. Zamanlama: gereksinim 17:26'da
commit'lendi, ölçüm 17:40'ta bitti. **Clara'nın iş sırası kurgusundan.**

Ve dördüncü bir şey: **her iki PCA dosyası da commit'lenmemiş** — commit'li bir
belge, versiyonsuz bir dosyaya atıf veriyor.

**B3-B6 (bloke etmeyen):** dal seçim anı tanımsız · `status.md` yok, günlük
gereksinimin içinde · bir ölçümün öznesi yazılmamış (PCA ölçtü, edilgen yazıldı) ·
gereksinim *"var olmayan mekaniğe dayanma"* dersini yazıyor ama kanal düzenini
emsal alıyor — **kanal betikleri git'te değil.**

**PQA üç şeyi de ONAYLADI (kayıt için):** PAM'in *"sınırı aştım mı"* şüphesi
**yersizmiş** — üç *"kanonda ne bulunmalı"* cümlesi de ne isteniyor söylüyor,
nasıl yazılacağını değil. `PAM-WRITE-DOCS-ONLY` korunmuş. Ve olçüt uyarlaması
**haklı** ama **çift değiştirmiş** (emsalde planlayan↔denetçi, burada
planlayan↔üreten) ve bu yazılmamış — boşluk değil **eksik şerh**.

## PAD'in planı — Clara'nın kararını çürüttü (18:33)

**İki dallı rol tanımı kararı GERİ ALINDI.** Clara 17:21'de üreten rolü iki
dallı bıraktırmıştı. PAD ölçtü: 139 kural tanımının hiçbiri rolü ikiye bölmüyor;
koşullu görünen altısı kuralın *uygulanıp uygulanmayacağını* belirliyor.

**Ters yönde emsal:** `YT-ASSUME-BACKGROUND` belirsizliği dallandırmıyor, **tek
varsayıma sabitliyor** — ve o kuralın **ilk hâli dallanmıştı, ölçüm düzeltti.**

**PAD'in gerekçesi Clara'nınkinden güçlü:** dallı tanım belirsizliği çözmüyor,
**her tura dağıtıyor** — agent her işin başında *"hangi daldayım"* diye soruyor
ve cevap rol tanımından çıkmıyor.

**Çözüm — tek tanım + eşik:** rolün işi tek cümleyle sabitlenir (*"otomasyonu
çalışır hâle getirir"*), sonra bir eşik kuralı: çalışır hâlde değilse bu
**söylenir** ve kapsam daralması olarak işaretlenir. Fark: dallı tanımda iki meşru
sonuç var, agent seçer; eşikli tanımda **tek meşru sonuç** var, diğeri
**bildirilmesi gereken sapma.** PQA bağımsız olarak aynı yere baktı (B3).

**Katman kararı — A yönünde ama emsal ölçeğinde değil.** 4 rol için 5-6 skill,
ağırlık `SKILL.md`'de, reference **yalnız mekanik** için.

Asıl gerekçe **hook ölçümü** — PAD dosyadan doğruladı, iddiaya güvenmedi:
A ailesinin `preload-skills.py`'si *"Skill aracını kullan, Read gövdeyi parçalı
getirir"* diyor. Yani **hook SKILL'i kurtarıyor, REFERENCE'i kurtarmıyor** — ve
A kanonunun %69'u reference'ta. PAD kendi ölçülmüş yarasını dayanak yaptı:
*"fabrikada bir agent kanonunun %91'ini hiç görmedi."*

**Ve `uretim-standardi` yetim çıktı.** PAD üç yoldan kanıtladı (skill listesi ·
`STD-` prefixi sıfır · grep'te sıfır atıf), skill'i okudu (268 satır),
örtüşme ölçtürdü: 21 STD kimliğinden **4 doğrudan karşılıklı, 12 karşılıksız**;
ters yönde PAD'de olup onda olmayan 13+ kimlik (`YT-*` serisinin tamamı — o seri
preload açığının keşfinden **sonra** doğdu). Kendi kanonuyla üretecek, üç STD
kalemini **yöntem** olarak kullanacak (ground-truth · dış-dayatma/bizim-tercih
işaretlemesi · ölçemedim-vs-temiz).

**Clara'nın kararları (18:42):** ayrı `rules-index` + ayrı kimlik uzayı (fabrika
prefixleriyle çakışmayacak) · ADIM 0 (N8N ground-truth) **kapsamda ama bekliyor,
atlanmıyor** — o zamana kadar N8N'e dayanan her kural dayanağını taşıyacak.

## Clara'nın hatası — PCA itiraz etti, haklıydı (18:42)

Clara PCA'ya *"dosyaları commit'le"* dedi. **PCA reddetmedi, itiraz etti:** commit
onun işi değil — kendi tanımı açık (*"ürettiğini PAD commit'ler"*),
`ISD-COMMIT-THEN-PUSH` `docs/` altını PAM'e veriyor.

**PCA'nın gerekçesi:** *"elimde imkân var, yetki yok"* — `ISD-STAY-IN-ROLE`'ün
lafzı. Ve asıl uyarı: *"sınır metinle çizili, aşındığı an görünmüyor"* — bir kez
commit atsa, bir sonraki turda *"zaten commit'liyordum"* gerekçesiyle başka
dosyaya uzanabilir.

**Clara'nın hatasının adı:** bulguyu doğru gördü, **çözümü kanona bakmadan verdi.**
Bir şeyin yapılması gerekmesi, onu **kimin** yapacağını söylemiyor. Karar geri
alındı, iş PAM'e gitti.

**Ve PCA itiraz ederken çözümü de taşıdı** — iki dosyanın kapsam özetini çıkarıp
PAM'in işini kolaylaştırdı. `BHV-OBJECT-DONT-REFUSE` böyle işliyor.

---

## İkinci denetim: GEÇMEDİ — ama sebebi tek ve karar Mert'te (22:24)

**Altı bulgunun altısı da gerçekten kapandı, yeni bulgu yok.** PQA kapsamını
yine açıkça yazdı: `gereksinim.md` tamamı (683 satır, diff değil), `status.md`
(160), PCA'nın asset ölçümü (217), iki commit'in kapsam doğrulaması.

Geçmeme sebebi **tek**: iki önkoşulun birbirine bağlı olduğu görülmemiş.

### PAM'in iki sorusuna cevap

**S1 — B1'in özne çözümü kopya olmadan aynı korumayı sağlıyor mu?** **EVET, ve
kopyalamaması DOĞRU karardı.** Fabrikanın cümlesi üç rol tanıyor; bu takımın
zinciri **dört** rol ve merkez aynı zamanda bir rol — birebir taşınsaydı
*"planlayan kendi işini kendine iletir"* gibi bir adım üreterek **yanlış**
olurdu. Korumanın özü korunmuş: her adımın öznesi var, son halka ayrı bir elde
bitiyor. Üstelik **fabrikadakinden daha güçlü** yazılmış, çünkü bedel farkı da
yazılmış: *"orada denetlenmemiş bir commit kalıyordu, burada denetlenmemiş bir
otomasyon aktive edilebilir."*

**S2 — önkoşulu işaretlemek yeterli mi?** **İkisi aynı sınıfta değil.**
Ölçüt: önkoşul PAD'in **üretim anında** yapacağı işi durduruyor mu, yoksa takım
**sahada** çalışırken mi çıkar?

```
N8N mekaniği şerhi  →  İŞARETLEMEK YETERLİ. PAD'in şu an yapacağı iş
                        (rol body'leri, skill katmanı, kimlikler) mekaniğin
                        doğruluğundan bağımsız. Yanlış çıkarsa düzeltilecek
                        şey kural METNİ olur ve hattan geçer.
Kanal betikleri     →  KAPANMALI. PAD üretim anında tıkanır: "kanal düzeni
                        kur" talimatı yazılacak ve kuracağı şeyin kaynağı yok.
```

### B7 — üçüncü edilgen vaka VAR (hafif)

PAM *"aynı belgede iki kez özne düşürmüşüm"* deyip üçüncüsünü sormuştu.

**PQA'nın yöntemi kayda değer:** ekseni PAM'in bulduklarına göre **seçmedi** —
`BHV-DONT-AIM-AT-LAST-MISS`, *"geçmiş bulguya nişan alan arama geçmiş bulguyu
bulur."* Bağımsız eksen kullandı: *"bir işi tarif eden ama o işi KİMİN yapacağını
söylemeyen cümle."* 38 satır çıktı, okuyarak ayıkladı.

Sonuç: üç yerde aynı sınıf, **ikisi eksik biri temiz** — ve üçü de *"kanonda ne
bulunmalı"* cümlelerinde yoğunlaşıyor. PQA'nın yorumu: o cümleler bir **hükmü**
tarif ediyor ve hükmün öznesi kural yazılırken belirlenecek sanılmış olabilir.

**Ağırlık: hafif**, üretimi bloklamaz — PAD kural yazarken zaten özne vermek
zorunda (`URT-` kanonu istiyor). Ama B1'in kendi dersi *"öznesiz bırakılan adımı
kimse üstlenmez"* ve o ders belgenin kendi içinde üç yerde uygulanmamış.

### S4 — PCA'nın ölçümü B6'nın AĞIRLIĞINI değiştiriyor

PAM'in çözümü (iki yol + karar kullanıcıda) **doğru ama artık eksik** — çünkü
yazıldığında bu ölçüm yoktu.

**İkinci yol fiilen kapalı.** PAM ikinci yolun bedelini *"iki ayrı uygulama
doğar, zamanla ayrışır"* diye yazmıştı. PCA'nın ölçümü bu bedeli **düzeltiyor**:
beş betikten hiçbiri uyumlu biçimde yeniden yazılamıyor, ayrışma *"zamanla"*
değil **anında** oluşuyor, ve beşten dördü sessiz sınıfta — **yanlış yeniden
üretim çalışır görünüyor.**

> PQA'nın cümlesi: *"iki yol eşit değil: birincisi bir iş, ikincisi bir arıza
> üretimi."*

**Ve boşluk gereksinimde olduğundan küçük görünüyor.** PAM `kanal.md`'den doğru
alıntı yapmış ama `kanal.md` boşluğun **varlığını** biliyor, büyüklüğünü değil —
büyüklüğü anlatan cümle (`SABLON:647-648`) git'e **hiç geçmemiş.** Yani PAM
**eksik bir kaynaktan doğru alıntı** yapmış.

**Sonuç:** önkoşul *"karar bekliyor"* değil, **"tek uygulanabilir yol var ve o
yol fabrikanın bekleyen bir işi."** İki yol arasında seçim gibi sunulursa
kullanıcı **olmayan bir seçeneği** seçebilir.

### B8 — asıl tıkayan bulgu: B1, B6'ya BAĞLI

Gereksinimin kendi yazdığı desen: *"koruma mekanizmayla sağlanabiliyorsa metinle
bırakılmaz"* + ters yönü *"mekanizmanın varlığı doğrulanmadan ona atıf
verilmez."*

PQA mekanizmaya yaslanan üç yer buldu (sat. 307/311, 347-356, 642-643) ve
**üçü de aynı mekanizmaya yaslanıyor: kanal kutusu.** O mekanizmanın bu takımda
var olacağı **doğrulanmamış** — kaynağı B6'nın önkoşulu.

**Yani belgenin kendi yazdığı ters-yön kuralı, kendi B1 çözümüne
uygulanmamış.** B1 *"koruma iyi niyete dayanmasın, mekanizmaya dayansın"* diyor;
dayandığı mekanizmanın kurulup kurulamayacağı açık kalem.

**Bu bir çelişki değil, bir BAĞIMLILIK** — ve görülmemiş olması bulgu. PQA
doğruladı: sat. 347-356 ile sat. 313-329 birbirini **anmıyor.**

### Kapı açılırsa ne olur

PAD *"kanal düzeni kur"* ve *"denetçinin raporu kalıcı olsun"* talimatlarını
**birlikte** alacak; ikincisi birincinin kurulmasına bağlı ve birincinin kaynağı
yok. PAD ya tıkanır (**izin-bekleme değil, malzeme-yok sınıfı**) ya kendi
çözümünü uydurur — ve `PAD-WRITE-WHAT-WAS-ASKED` gereği uyduramaz, bildirmek
zorunda. **Yani kapı açılırsa iş birinci turda geri döner.**

### Geçmek için gereken üç şey

1. **B6 önkoşulunun kapanması** — karar verilmesi, ve PCA'nın ölçümünün karara
   girdi olması (iki yol eşit değil)
2. **B1 ile B6 arasındaki bağımlılığın belgede görünür olması**
3. B7'deki üç öznesiz cümle — **hafif**, üretimi bloklamaz

N8N mekaniği şerhi üretimi **bloklamıyor.**

---

## ÜRÜN DOĞDU (22:37) — ve sıra değişikliği işledi

Mert 22:31'de kesti (*"takım hâlâ oluşmamış, saatlerdir napıyorsunuz"*), 22:32'de
üretim kapısı açıldı, **22:37'de `team/n8n-otomasyon/` gerçek oldu.** Beş buçuk
saatlik sıfırdan sonra altı dakika.

```
22:37   plugin.json · KURULUM.md · hooks/ · marketplace.json     300 satır
22:39   + n8n-davranis/SKILL.md                                  528 satır
22:42   + n8n-is-duzeni/SKILL.md                                 781 satır
```

**`DAG-REGISTER-IN-MARKETPLACE` ilk kez sahada koştu.** Kökteki
`.claude-plugin/marketplace.json` **hiç yoktu** — PQA'nın ilk denetimdeki tespiti
kapandı. 26 DAG kuralından ilki ölçüldü.

### Kapı "geçmedi" hükmüne rağmen açıldı — ve bu doğru işledi

İki açık kalem **durdurulmadı, işaretlendi**: kanal betikleri (`KURULUM.md`'ye
önkoşul olarak) ve N8N erişimi (üreten rolün tanımı tek+eşik).

PQA kararı kabul etti ve ayrımı kendisi kurdu: *"hükmümü atlamadın, üzerine karar
verdin; ikisi farklı şey."*

### PAM Clara'nın kararındaki belirsizliği kapattı

Clara *"sıraya alındı"* demişti. PAM ayırdı:

```
ÜRETİMİ bloklamıyor  →  PAD "kanal düzeni şöyle işler" yazabilir
KURULUMU bloklar     →  betikler pakete girmezse takım kurulur ama KONUŞAMAZ
```

*"Bu ayrım olmadan 'sırada' kelimesi 'sorun değil' gibi okunur."* Ve yetkiyi
aşmış olabileceğini **kendisi sordu.**

**PQA'nın hükmü: ÇIKARIM, karar değil.** Ölçütü: *"bir cümle KARAR ise farklı
karar verilebilirdi; ÇIKARIM ise verilen karardan zaten çıkıyor ve tersi bir olgu
hatası olurdu."* Ters testi de yaptı — PAM *"o zaman önce betikler taşınsın"*
deseydi **karar** olurdu; dememiş.

Ve bu çıkarım üçüncü denetimin ölçütünü de belirledi: kurulum bütünlüğü eksenini
koşarken kanal betiklerinin pakette olup olmadığına bakılacak — *"yazılmasaydı
'sırada' diye geçiştirilebilirdi."*

### PAM kendi kuralını kendine uygulamadığını kabul etti

B8'in özü: B1 çözümü (*"denetçinin raporu kalıcı dursun"*) bir **mekanizmaya**
yaslanıyordu ve o mekanizmanın kurulabilirliği açık kalemdi.

**Ve ters-yön kuralını aynı belgede PAM'in kendisi yazmıştı:** *"doğrulanmamış
bir mekanizmaya yaslanan kural, hiç koruma olmamasından KÖTÜDÜR çünkü koruma
varmış gibi görünür."* Kuralı yazdı, kendi çözümüne uygulamadı — ve **silmedi,
gereksinime yazdı**: *"öğrenilecek olan şey tam o."*

Bağı **iki yönlü** yazdı. PQA ölçtü — **iki kaynak değil, iki bakış**:

```
kanal betiği tarafı   "bu önkoşul kapanmazsa NELER kırılır"  → aşağı bakıyor
merkez gerilimi       "bu koruma NEYE dayanıyor"             → yukarı bakıyor
```

*"Bir okuyucu yalnız B'yi okusa 'bu koruma neye dayanıyor' öğrenir ama 'önkoşul
kapanmazsa başka ne kırılır' öğrenemez."* PQA'nın şerhi: bugün tek kaynak,
**kalıcı garanti değil** — ayrışma ancak biri değiştiğinde görülür.

### PAM'in üçüncü özne düşürmesi — alışkanlık teşhisi

*"B1 kapanışı (edilgen), B5 ölçüm atfı, şimdi bu ikisi. Bir kere hata, üç kere
alışkanlık."* Ve öz eleştirisi Clara'nınkinden sert:

> *"Kanonum `BHV-NO-RUSH` kapsam daraltmayı meşru sayıyor AMA 'söylenmesi'
> şartıyla. Ben daraltmadım, DERİNLEŞTİRDİM, ve o seçimi hiç söylemedim. Yani
> sessizce genişleyen bir iş ürettim ve durdurması kullanıcıya kaldı."*

### PCA kendi cümlesini çürüttü — ölü monitör kapandı

22:18'de *"oturum devam ediyor, monitörüm 19:06'da öldü"* demişti (bu B'yi ima
ediyordu: oturum içi ölüm, kural gerektirir). **Transcript'ten ölçtü:**

```
en büyük boşluk    189.5 dk   19:06:50 → 22:16:22   (ikincinin DÖRT katı)
boşluktan sonraki ilk kayıt    "Continue from where you left off"
dosya sistemi      19:06 sonrası eski oturum dizininde HİÇ yazım yok
```

**Sonuç: üç vaka da oturum-arası.** PAM'in *"deterministik"* çıkarımı zayıflamadı,
**güçlendi**. Mevcut kanon (`ISD-OPEN-YOUR-BOX`) yeterli — periyodik canlılık
kuralı için **veri yok**.

Ve kapatmadığı şey doğru: *"bu ölçüm 'monitör oturum içinde ölmez' demiyor,
'bugün ölmedi' diyor."* `Monitor`'ün otomatik durdurma eşiği hâlâ ölçülmedi ve
PCA'nın vakası ona hiç yaklaşmadı (105 dakikada 7 olay).

### PCA'nın davranış testi hazır — 16 soru, 8 eksen

Clara altı eksen vermişti (üç kesişme + üç risk); PCA **iki eksen daha** çıkardı
(*"başarılı çalıştı ≠ doğru çalıştı"* ve *"üç eşik ayrı ayrı yazılır"*) ve
birincisini **dört rolde birden** sınadı — gereksinim onu *"rol-üstü"* diye
işaretlemiş.

Üç tasarım kararı gerekçeli: **rol adı hiçbir soruda geçmiyor** (agent kendi
rolünü kanonundan bilmeli) · **vakaların çoğu meşru görünüyor** (*"bariz yanlış
bir istek her kanonu geçer — sınır ihlali CAZİP olduğunda ölçülür"*) · **üç
soruda bilgi eksik bırakıldı** (doldur mu, bildir mi, bekle mi — rol sınırının en
keskin ölçümü).

**Cevap anahtarı yok** ve gerekçesini kendi de gördü: *"beklenen davranışı yazan
kişi testi kendi beklentisine göre kurmuş olur."*

Üç şerh: zorluk kalibrasyonu yapılmadı (*"hepsi geçerse bu kanonun sağlam
olduğunu değil SORULARIN KOLAY olduğunu da gösterebilir"*) · çok-rollü vaka yok ·
iki soru B dalı varsayıyor.

---

## ROL SAYISI: DÖRT → ÜÇ (2026-08-09 01:58)

**Mert'in itirazı ölçüldü ve haklı çıktı.** *"Dört kişi gerekli mi gerçekten"* —
gerekli değilmiş. Koşturan ile denetçi birleşti.

Ölçüm sorusu her rol için tek: **kaldırılırsa işi kim yapar ve ne kaybedilir?**

```
üreten      kaldırılırsa N8N'e yazan kimse kalmaz            KALIR
planlayan   kullanıcının muhatabı ve gereksinim yazan kalmaz  KALIR
denetçi     aktivasyon kapısı üreticiye düşer                 KALIR
koşturan    → "hiçbir şey kaybedilmiyor"                      ELENDİ
```

### Koşturan neden elendi — üç ölçüm

**(1) Kuralın üçte biri rolün KENDİ VARLIĞINDAN doğan riski yönetiyordu.**
Koşturma skilinde 9 kural vardı, **3'ü sınır kuralıydı** (`FINDING-NOT-FIX`,
`FINDING-DOESNT-STOP`, `DONT-FIX-WHAT-YOU-MEASURE`) ve üçü de aynı şeyi
koruyordu: *"ölçtüğün şeye dokunma, hüküm verme."*

Rol birleşince o üç kural **gereksizleşiyor** — koruduğu sınır ortadan kalkıyor.
Kanon küçülüyor ve küçüklüğü bir kayıp değil.

**(2) Ayıran tek şey KAPI YETKİSİYDİ.** İkisi de ölçer, ikisi de *"çalışmıyor"*
diyebilir; fark yalnız birinin sözünün akışı durdurması. Bu bir **rol** farkı
değil **yetki** farkı — ve yetki tek rolde de taşınabilir.

**(3) Üretici/denetçi omurgası korunuyor.** Asıl ayrım *"ölçen ile üreten"*,
*"ölçen ile hüküm veren"* değil. Birleşmiş rol hâlâ üretenden **bağımsız**:
kendi kurmadığı bir akışı ölçüyor.

**Karşı argümanı da ölçtü:** emsalde (OY, 9 rol) TE ile QA ayrı ve gerekçe
*"kapı da test koştururssa sınır bulanıklaşır."* Ama o gerekçe **iki rol varken**
geçerli — tek rol varken bulanacak sınır yok. Emsalin dokuz rolü ayrık
yığınlardan doğuyor; burada o koşul yok.

### Planlayan + üreten birleşmesi REDDEDİLDİ — ve gerekçesi ince

Gereksinimin kendi (c) maddesi bu ikisinin *"anormal yakın"* olduğunu yazıyordu.
PAD'in çıkarımı: **yakınlık birleştirme gerekçesi değil, AYIRMA gerekçesi.**

Birleşirse tek el hem *ne isteneceğine* hem *nasıl yapılacağına* karar verir ve
kullanıcının istediğinden sapma **hiçbir yerde görünmez** — çünkü
karşılaştırılacak bir gereksinim belgesi olmaz. Gereksinimin cümlesi: *"ikisi de
sessizdir."*

*"Sınırın kendiliğinden korunmadığı yerde yazılı olması gerekiyor."*

### Üç rol

```
1. gereksinimi yazan + merkez
2. otomasyonu kuran
3. ölçen + kapı
```

**Kazanılan:** üç kural, bir agent body'si, bir skill ve sürekli bir bakım
maliyeti. *"İhtiyaç doğmadan kapasite kurulmaz"* kuralına uyuyor.

**PAD'in şerhi:** bu bir **metin** ölçümü. Sahada tek rolün iki işi taşıyıp
taşımadığı ölçülmedi — ilk üç işte *"ölçüm ile hüküm aynı turda mı veriliyor"*
diye bakılmalı. *"Ayrışma görülürse rol yeniden bölünebilir; bölmek
birleştirmekten kolay."*

### Çift tanım temizliği de bitti

```
önce   82 tanım · 11 çift · 18 atıf (yetim yok)
sonra  71 tanım · 71 tekil · SIFIR çift · sıfır yetim
```

Ölçüm tekrarlandı, beyanla kapatılmadı.
