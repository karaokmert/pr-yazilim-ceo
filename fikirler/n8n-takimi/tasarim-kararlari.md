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
