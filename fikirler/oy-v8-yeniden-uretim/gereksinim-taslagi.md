# OY takımının fabrikada yeniden üretimi — gereksinim taslağı

**Yazan:** Clara · **Tarih:** 2026-08-09 · **Hedef:** PAM (agent-project)
**Durum:** Mert'in onayına sunulacak taslak. Onaylanınca devir bloğu olarak iletilir.

---

## Neden var

OY takımı sahada çalışıyor ama **kanonunun yarısı agent'ın eline hiç geçmiyor.**

Ölçüldü (PCA, 173 oturum, `agent-project/docs/ozel-yazilim/takim-analizi/saha-olcumu-pca.md`):
- 76 skill'in **35'i (%46) hiç açılmamış**
- 77 reference'ın **48'i (%62) hiç okunmamış**
- 574 kural kimliğinin **352'si (%61) sahada hiç anılmamış**

**Sayılar tek başına bulgu değil.** Bulgu şu dokuz skill: konusu sahada gerçekten
konuşulmuşken kanonu bir kez bile açılmamış — `docker-k8s` 76 oturumda konuşuldu/0
açılış, `notification` 69/0, `dev-environment` 67/0, `e2e-verification` 63/0, `upload`
27/0, `impact-analiz` 21/0, `structural-audit` 4/0, `danisma` 4/0, `figma` 1/0.

Bunlar için *"ihtiyaç doğmadı"* açıklaması **çürütüldü.**

**Yapısal sebep ölçüldü** (Clara, `incelemeler/oy-v8-yeniden-uretim/yapi-olcumu.md`):
her rol yalnız **6-7 skill preload ediyor** — 5 çekirdek (9/9 rolde ortak) + 1 rol
omurgası. Kalan **61 skill hiçbir preload listesinde değil**; tasarım agent'ın iş anında
açmasını varsayıyor, saha bunu doğrulamıyor.

**Bir düzeltme daha ihtiyacı gösteriyor:** OY'nin metin tutarlılığı 2026-07-31'de
ölçülmüştü — *634 ID, 0 yetim, 0 çift tanım, 0 kırık atıf.* Bugün kaynaktan üç ölü MCP
adresi doğrulandı (aşağıda). Yani **tutarlılık ölçümü temiz çıktı, kanon yine de bozuk.**
Ölçüm ekseni dardı.

---

## Ne yapılacak

OY takımı fabrikada **yeniden üretilecek** — taşınmayacak, kopyalanmayacak.

**Ayrım önemli:** taşıma yapılırsa 76 skill olduğu gibi gelir, sahada açılmayan 35'i de
gelir. Yeniden üretim mevcut kanonu **girdi** olarak alır ve fabrikanın kendi
standardıyla yeniden paketler.

### Yazım standardı — Mert'in kararı, 2026-08-09

**Bu altı madde OY v8'in saha deneyiminden çıkarıldı ve üretimi bağlar.** Aşağıdaki her
şey bunlara uyar; çelişki çıkarsa bu bölüm kazanır.

**1. Skill haritası açık olmalı.** Bir agent hangi işi yaparken hangi skill'e gideceğini
net bilmeli. Belirsiz harita = skill çağrılmıyor.

**2. Description içeriği özetlemez, çağrılma anını söyler.** Ölçüldü: **76 skill'in
76'sı da 300 karakteri aşıyor** (medyan 704, max 994, ortalama 712). İstisna yok. Bugünkü
description'lar skill'in *ne içerdiğini* anlatıyor — oysa işi *ne zaman açılacağını*
söylemek.

**3. Her iş için kullanılabilecek skill'ler body'de net belirtilir.** Agent her turda
elinin altında ne olduğunu bilmeli.

**4. Rolün main skill'i, hangi skill'in ne için var olduğunu netler.** Harita tek yerde
durur.

Ölçüldü ve bu maddeyi doğruluyor: bugün beş çekirdek skill'in **her biri diğer dördünün
sınırını kendi başında yeniden anlatıyor** (`is-akisi` → *"biçim handoff'ta, refleks
behavior'da"*; `handoff` → *"sıra is-akisi'nde, kayıt memory'de"*; `behavior` → üçünü
birden). **Aynı sınır haritası dört ayrı yerde yazılı** ve hiçbiri asıl işi yapmıyor.
Tek harita, beş tekrarı birden düşürür.

**5. Preload azdır — ve ölçüt sayı değil, "her turda lazım mı".** Bir şey her turda
lazım değilse preload'a girmez; iş-anına özel olan omurga haritasından çağrılır.

**6. Her skill, reference'ına ne zaman gidileceğini tarifler.** Ölçüldü: 77 reference'ın
48'i hiç okunmamış. Reference'ı olan ama "ne zaman aç" demeyen bir skill, reference'ı
olmayan skill'e denktir.

### Katman kararları — yukarıdaki maddelerin uygulaması

Bunlar Mert'in kararı (2026-08-09/10) ve **birleşme ölçütü konu benzerliği değil, aynı
sahip / aynı refleks:**

**`pr-yazilim-oy-envanteri` → main skill'e taşınır, preload'dan çıkar.** *"Kim ne
yapıyor, elimizde neler var"* okunmak istendiğinde açılır. Ve bir refleksi taşır:
**yeni bir şey eklenirken mutlaka alt yapıya bakılır.** Her turda değil, **bir şey
eklenirken** lazım — bu yüzden çağrılan katmanda.

**`memory-management` → `behavior` içinde yaşar.** Memory ayrı bir iş değil, bir
refleks. (Bugün zaten birbirlerini işaret ediyorlar: memory skill'i *"refleks
behavior'da"* diyor, behavior *"memory disiplini memory-management'ta"* diyor — ayrı
durmalarının tek ürünü bu karşılıklı atıf.)

**`is-akisi` → body'ye iner.** Her agent **kendi** iş hattını taşır: kimden alır, kime
verir, hangi sırayla. Ortak olan kısım (sıra mantığı, devir ilkesi) `behavior`'da
**satır olarak** yer alır.

Gerekçe ölçülmüş: `is-akisi` skill olarak dururken dokuz rol aynı dosyayı okuyup içinden
kendi payını çıkarmaya çalışıyor. Body'ye inince her agent yalnız kendi hattını görür.

**`handoff` → `behavior` içine girer** (Clara'nın kararı, gerekçesi aşağıda).

Devir bloğu formatı dokuz rolde **birebir aynı** ve iş biterken kullanılan bir
**refleks** — memory ile aynı sınıf. Üç gerekçe:

- **"Ayrı skill kalsın, iş bitince çağrılsın" sahada denendi ve düştü.** Bugün `handoff`
  ayrı skill *ve preload'da* — en avantajlı konumda. Buna rağmen *"preloaded ≠ okunmuş"*
  dersi beş kayıtta yazılı. Preload'dan çıkarmak durumu kötüleştirir.
- **Body'ye koymak cascade borcu üretir** — dokuz body'de aynı format tekrarlanır, biri
  değişirse dokuzu değişmeli. Fabrikanın `atif-haritasi` işi tam bu yüzden yarım
  (beş cascade onarımı PAD'de bekliyor).
- `is-akisi` body'ye indiğinde *"kime"* zaten orada olur; geriye kalan devir **biçimi**
  gerçekten ortaktır.

**Sonuç — preload iki skill:**
1. **`behavior`** — karakter + memory disiplini + devir biçimi + ortak akış ilkesi
2. **rol omurgası** — kendi aleti ve **skill haritası** (madde 4)

Geri kalan her şey çağrılan katmanda: envanter (bir şey eklenirken), alet skill'leri
(iş anında, omurga haritasından).

**Bu bir hipotez değil karar; ama uygulaması PAD'in.** Birleştirme sırasında bir kural
düşerse ya da çelişirse `status.md`'ye yazılır (n8n'de rol birleştirmesi sessizce
yapıldı — tekrarlanmayacak).

### Üç aşama, sıralı

**Aşama 1 — ortak katman.** Dokuz rolün paylaştığı zemin sabitlenir: `behavior`'ın
birleşik hâli, kural kimlik düzeni, katman ölçütü (hangi kural body'ye, hangisi skill'e,
hangisi reference'a), rol omurgası şablonu ve **skill haritası biçimi**. Bu aşama
tartışma değil **derleme** — ölçütler zaten ölçülmüş hâlde mevcut (girdilere bakınız).

**Aşama 2 — pilot rol: `backend-developer`.** Bir rol baştan sona üretilir ve sahada
ölçülür.

*Seçim gerekçesi:* sahada en çok konuşulan konular (`docker-k8s` 76 oturum,
`dev-environment` 67) backend'e komşu — yani pilot en hızlı sınanır. Body 105 satır,
dokuz rolün medyanı; uçlarda değil.

**Aşama 3 — kalan sekiz rol.** Pilot ölçümü geçerse akıtılır. Geçmezse ortak katman
düzeltilir ve pilot tekrarlanır.

### Kabul ölçütü — bu işin en önemli maddesi

**Bir rolün bittiğinin ölçütü "dosya üretildi" DEĞİL, "sahada açıldı"dır.**

Gerekçe: OY'nin bugünkü hastalığı tam olarak bu. Dosyaları tutarlı ölçüldü, sahada
yarısı açılmadı. Aynı kabul ölçütüyle yeniden üretilirse **aynı sonuç çıkar.**

Fabrikanın kendi kanonunda bu kapı yok — PQA'nın kapanış raporundaki *"katman-2
boşluğu"*: kanondaki tüm test/denetim hükümleri **dosya** için yazılmış, bir plugin'in
gerçekten yüklendiğini ölçen kapı yok.

**Bu iş o kapıyı kendi içinde kurar.**

**Geçme eşiği — yöntem PAD/PCA'nın, eşik burada sabit:**

- **Kaç iş koşturulur:** en az **üç** ayrı iş. Biri yetmez — tek işte açılmayan bir
  skill'in sebebi "o iş o konuya girmedi" olabilir, ayırt edilemez.
- **Hangi işler:** üçü de o rolün **kendi sahasından gerçek iş** olacak, sentetik
  senaryo değil. Pilot rol backend olduğu için üçünün en az biri sahada en çok
  konuşulan konudan seçilir (`docker-k8s` 76 oturum, `dev-environment` 67).
- **Neyin açılması beklenir:** rolün **preload listesinin tamamı** (`behavior` + rol
  omurgası). Preload edilen bir skill hiç açılmadıysa preload çalışmıyor demektir —
  bu bir arıza, tercih değil.
- **Alet katmanı için eşik — bu işin asıl sınavı:** işin konusuna karşılık gelen alet
  skill'i **açılmış olmalı.** Ölçüt sayı değil **eşleşme** — *"konu geçti, alet
  açılmadı"* vakası **sıfır** olmalı. OY'nin bugünkü yarası tam bu (dokuz vaka) ve
  yeni yapı bu yarayı kapatmak için kuruldu: preload daraldı, yük **skill haritasına**
  bindi. Harita çalışmıyorsa bu ölçüm onu gösterir.
- **Reference için eşik:** açılan bir skill'in reference'ı, o iş onu gerektiriyorsa
  okunmuş olmalı. (Madde 6'nın sınavı — 77 reference'ın 48'i hiç okunmamıştı.)
- **Geçmedi sayılır:** yukarıdakilerden biri tutmazsa. Rapor "kaç skill açıldı" değil,
  **"hangi beklenen skill açılmadı ve o oturumda konusu geçti mi"** biçiminde yazılır.

**Yöntem PAD/PCA'ya bırakılır** (`ISD-SCOPE-NOT-METHOD`) — nasıl ölçüleceği, hangi
telemetriyle sayılacağı onların kararı. Eşik yukarıda sabit.

### Rol sayısı kararı — dokuz rol sorgulanacak

Fabrikada **rol açma testi yok** (arandı, `.claude/skills/` altında sıfır sonuç; skill
için üç soruluk kapı var, rol için hiçbir şey). Fabrika bunu kendi eksiği olarak yazmış —
`docs/fabrika/uretim-refleksi/`, PAD kuyruğunda.

**Ayrı iş açılmıyor; bu işin içinde çözülüyor — ve `uretim-refleksi` beklenmiyor.**

`docs/fabrika/uretim-refleksi/` işi **PAD kuyruğunda ve üretimi başlamamış.** Bu iş
onu beklemez. Sıra şu: **PAM aşama 1'de rol açma ölçütünü OY'nin dokuz rolünden
çıkarır** — yani ölçüt soyut olarak değil, elindeki dokuz gerçek rolün sınırlarına
bakarak yazılır. Ölçüt bu işin çıktısıdır ve `uretim-refleksi`'ne **girdi olarak
devredilir**; tersi değil.

Gerekçe: `uretim-refleksi` fabrikanın genel refleksini kuruyor, bu iş ise dokuz
somut role bakıyor. Somuttan çıkan ölçüt soyut olandan daha güvenilir — ve fabrika
zaten bunu bir kez yaptı: OY'nin altı standardı ölçülerek çıkarıldı, teoriden değil.

**İki iş aynı dosyaya dokunmaz** — bu işin çıktısı `docs/ozel-yazilim/` altında,
`uretim-refleksi` fabrikanın kendi kanonunda. Cascade gerekirse o ayrı turdur
(`ISD-ONE-TEAM-PER-TURN`).

Emsal uyarısı: n8n'de gereksinim 4 rol yazdı, ürün 3 rol çıktı (koşturan rolü QA'ya
birleşti) — **ama o birleştirme gereksinime yazılmadı.** Bu işte rol sayısı değişirse
gerekçesiyle `status.md`'ye yazılacak.

Dokuz rolün mevcut sınırları keskin çizilmiş ve ilk bakışta savunulabilir (ör. QA
statik kapı / TE çalıştıran tek agent — ikisi ayrı). Karar ölçütten çıkacak, sezgiden
değil.

### Taşınmayacak üç kusur — yeni takımda doğru yazılacak

Mevcut kanonda üç ölü MCP adresi var ve **kopyalanırsa yeni takıma aynen geçer.**
Kaynaktan doğrulandı (2026-08-09):

- `skills/mobile-release/SKILL.md:66` — smoke test adımı
- `skills/mobile-release/SKILL.md:68` — izin kontrolü
- `skills/e2e-verification/references/maestro-mekanik.md:53` — **sorun giderme talimatı**

Üçünde de `mcp__maestro__*` yazıyor. Doğrusu `mcp__plugin_ozel-yazilim_maestro__*` ve
o desenin kanonda **sıfır kullanımı var.**

Üçüncüsü en zararlısı: talimat *"araçlar görünmüyorsa `mcp__maestro__*` iznini kontrol
et"* diyor — agent yanlış deseni arıyor, bulamıyor, *"iznim yok"* sonucuna varıyor.
Oysa izin var, adı başka. **Talimat kendi amacının tersini üretiyor.**

**Genel ders — bu üçüyle sınırlı değil:** bu kusurlar 2026-07-31'de yapılan bir
tutarlılık ölçümünde yakalanmamıştı (o ölçüm *0 kırık atıf* demişti) çünkü **dosya
atıflarını taradı, araç adlarını taramadı.** Yeniden üretimde atıf denetimi **araç
adlarını, MCP namespace'lerini ve komut adlarını da kapsamalı.**

---

## Kapsam dışı

**Sahadaki v8'e dokunulmayacak.** Yürürlükteki plugin (`ozel-yazilim@pryazilim-agents`
0.6.1) çalışmaya devam eder. Geçiş, yeni takım ölçüldükten sonra ayrı bir karardır.

**Üretim yeri:** `agent-project/team/` altında, `n8n-otomasyon`'un yanında. Orada
2026-08-02'de açılmış **boş** bir `team-1-oy/` klasörü duruyor. Adlandırma PAM'in
kararı — o yer tutucu kullanılabilir ya da fabrikanın adlandırma standardına uygun
yeni bir ad verilip boş klasör silinebilir. **Karar ne olursa olsun ortada iki klasör
kalmayacak.**

**Sahadaki v8'de ayrı bir onarım işi açılmayacak.** Bilinen kusurlar (aşağıdaki üç ölü
MCP adresi dahil) mevcut plugin'de düzeltilmeyecek — yeni takımda doğru üretilecekler.

**Websitesi (WS) takımı bu işin kapsamında değil.** İkinci takım olarak sonra gelecek.

---

## Girdiler — hazır, taranmış

### Fabrikanın kendi çıkarımı (birincil)

`agent-project/docs/ozel-yazilim/takim-analizi/` — bugün üretildi, denetimden geçti:
- `standart-cikarimi.md` — **OY'nin doğru yaptığı altı standart**, beşi ölçülerek
  çıkarıldı: çekirdek skill seti · üç katmanlı sınıflama (omurga/öz/alet) · "uçlu"
  deseni · tek-kaynak kuralı · body ölçütü · kapı haritası
- `rapor-analiz-plan.md` — saha ölçümü + analiz + altı kalemlik plan
- `saha-olcumu-pca.md` — 173 oturumluk ham ölçüm

### skill-project analiz havuzu (ölçüt taşıyanlar)

`/Users/karaok/p/ozel-yazilim/skill-project/docs/` — ~50 bin satır tarandı,
**~20 dosya doğrudan kullanılabilir.** Bunlar zamana bağlı **sayı** değil **ölçüt**
taşıyor:

- `agent-dogrulama/10-KATMAN-TANIMI-olculmus.md` — katman ayrımının ölçülmüş tanımı
  (*"ölçüt konu değil, ihlalin doğası"*). A/B ile sınanmış.
- `agent-dogrulama/11-ID-STANDARDI-onerisi.md` — kural ID standardı, 17 çakışma → 3
  sınıf + prefiks taksonomisi. **Havuzun en değerli tek dosyası.**
- `agent-dogrulama/12-KAPANIS-ID-DOGRULAMA.md` + `13-UC-IS-KAPANIS.md` — uygulama
  doğrulaması, body ID seçim ölçütü (`STD-BODY-ID-CRITERION`)
- `agent-dogrulama/04-skil-sayisi-karari.md` — skill sayısı kararı + **yeni skill açma
  ölçütü (S1/S2/S3)**
- `agent-dogrulama/09-KONSOLIDE-v7-v8-7-agent.md` — v7→v8 geçişinde ne kaybedildi:
  5 mekanizma, 10 kayıp, 7 kazanım, 14 onarım
- `agent-dogrulama/08-v8-eksik-envanteri.md` — **açık** eksik envanteri
  (*"bilgi kaybı %15, görünürlük kaybı %73"*)
- `agent-dogrulama/HOOK-ADAYLARI.md` — 29 mutlak → 6 hook adayı, üç süzgeç sorusu
- `v8-calisma/rules/management/*-skill-karar.md` (8 dosya) — sekiz rolün kimlik ve
  sınır kararları
- `v8-calisma/skill-planlama/skill-gruplama-onerisi.md` — nihai skill listesi,
  birleştirme ölçütü *"aynı iş-anı + aynı agent"*
- `v8-calisma/eksikler/00-BOSLUK-TESPITI.md` — 68 skill'in reference durumu, üç
  kategori

**Koşullu girdi** (geçerli ama v8'in o günkü yapısına atıflı — kopyalanacak metin değil,
kaçırılmaması gereken kural listesi olarak taranmalı): `agent-dogrulama/SONUC-*` 9 rol
raporu, `v8-calisma/eksikler/*/*-mekanik.md` 19 taslak.

### OY'nin kendi memory'si — kanona taşınacak saha bilgisi

**Tam kayıt:** `pr-yazilim-ceo/incelemeler/oy-v8-yeniden-uretim/memory-taramasi.md`

Dokuz kutu, **936 KB, ~198 dosya** tarandı. **~2/3'ü kanona taşınmalı, ~1/3'ü çöp.**

**Bu kanonun bir eksiğini gösteriyor ve gereksinimi doğrudan etkiliyor: kanon "ne
yapılır"ı söylüyor, "nasıl yanılırsın"ı söylemiyor.** Dokuz kutunun en kalın dosyaları
kural değil, **aracın sessizce yalan söylediği an** kayıtları — ve her biri agent kanonu
okumuş olmasına rağmen düşmüş.

**Sessiz kırılma envanteri kanonda yok — yeni takımda olmalı.** Ortak imza: *derleme
yeşil / araç sessiz / hata yok gibi görünür.* Örnekler: `HandlerOptions` varsayılanları
açık (endpoint herkese açık kaldı) · `Enum.IsDefined` + byte enum `(int)` cast derleme
yeşil çalışma anında patlıyor · `mutationFn: ApiService.x` → `this` kopuyor, tsc
yakalamıyor · `DateView isUtc` ters sezgisel ve **çoğunluk deseni yanlış** (102'de 42) ·
`grep -c` çoklu dosyada koşulu kırıyor · `git rev-parse` olmayan dosyada exit 0 · LSP
0 sonuç ≠ tüketici yok · `gh run list` hata vermeden boş bekliyor · `nc -z` VPN arkasında
24/24 "açık" diyor.

En ağır vaka: **uydurma numaraya gerçek SMS gitti** — agent iki gerçek aboneye SMS
yolladı ve *aynı turda* kendi raporuna *"dev'de SMS sağlayıcısı canlı"* yazmıştı.

**Dört kural adayı — memory'de tekrar ettiği için güçlü:**
- *"Emsal kanon değil"* — **altı kayıt, beş kutu**, bağımsız yazılmış
- *"Kendi ölçüm aracından şüphelen"* — beş kayıt, üç kutu
- *"Ekranda doğrula, kod okuması yetmez"* — üç uçta aynı ders (*build yeşili doğrulama
  sayılmaz*)
- *"Push onayı atlanmaz"* — üç kez tekrarlandı

**Skill boşlukları — kanon eksik, agent kendi notuyla doldurmuş:** LIVE DEV geri-besleme
kolu (`is-akisi` madde 7'de bitiyor, gerçek akış devam ediyor) · dış insan katkısının
içeri alınması · sprint planlama yöntemi (18KB, PA kendi kanonunu memory'de yazmış) ·
onay brief kalıbı (*"skill gelince SİL"* damgalı) · telepresence çoklu servis tarifi
(15KB, *"2/2 tuttu"* işaretli) · enum tüketici sayımı · prod dayanıklılık üçlüsü.

**Bir araç boşluğu:** `ozel-yazilim` plugin'inde **ClickUp MCP'si yok**, ama PA kanonu
ClickUp'ı zorunlu tutuyor (`CLICKUP-TASK-FIRST`). Şu an `websitesi` plugin'inin MCP'si
kullanılıyor — **yalnız OY kurulu bir makinede PA kanonun emrettiği işi yapamaz.**

**Beş kanon–saha çelişkisi taşınacak, silinmeyecek:** `ENUM-BYTE` (kanon byte, saha
int) · `CQ-COMMENT-WHY` (kanon yasak, sahada 74 satır) · NVARCHAR standartları (canlı DB
sorgusuyla doğrulandı: hepsi MAX) · `BE-PERF-SQL-SIDE` (bir DataLayer **iki deseni
birden** taşıyor, agent tuzağa düşüp yanlış yönlendirme yaptı) · `PA-DISC-CHUNK`
(kullanıcı kanonun tersine karar verdi).

Taşıma biçimi: *"kanon sahadan ileride, mevcut koda dokunma"* notuyla. Aksi hâlde emsale
bakan agent yanılır.

**Canlı borç — düşmemeli:** QA kapanış indeksinde 2 açık devir + 3 açık prod kapısı ·
DO'da egelisaglik prod secret'ları **dış IP** kullanıyor (DB portları dünyaya açık,
kullanıcı teyitli), osinif probe yok, ingress otomasyon dışı.

**Ve bir uyarı — üretim sırasını etkiler:** kutu doluluğu kanon kalitesini değil
**sahaya çıkma sıklığını** ölçüyor. `ui-designer` kutusu **boş**, `test-engineer` 3
dosya — kanonları iyi olduğu için değil, hiç sahaya çıkmadıkları için. **Memory'si
olmayan agent kanonun eksiğini raporlayamaz;** yeniden yazımda en riskli iki rol bunlar.

### Uyarı — havuzun sayılarına değil ölçütlerine güvenilecek

`V8-TAMAMLAMA-DURUM.md` 12 maddenin kapandığını söylüyor, ama aynı klasördeki
`DENETIM-BRIEF-v8-tamamlama.md` üç ölçüm aracı hatası bildiriyor ve biri geçmiş *"cache
doğrulandı"* beyanlarını geçersiz kılmış (Türkçe ünsüz yumuşaması yüzünden regex 54
satırı hiç denetlememiş). Hata bulunup düzeltilmiş, sonra 102/102 sapma sıfır ölçülmüş —
**ama ders duruyor: bu havuzdaki sayılar kendi içinde denetlenmemiş olabilir, ölçütler
sağlam.**

---

## Ölçülmüş mekanik — üretim kararını doğrudan etkileyen

**61/76 skill preload dışı olması OY'nin tasarım tercihiydi**, kaza değil. Omurga skill'i
bir *"iş → hangi alet"* eşlemesi taşır, agent iş anında açar. **Sahada tutmadı.**

**Ama sebep ayırt edilmedi ve üç aday var** (PAM'in analizi):
1. Omurga tablosu okunmuyor olabilir
2. Okunuyor ama tetikleme kararı verilmiyor olabilir
3. Agent kuralı zaten bildiğini sanıp açmıyor olabilir

**Üçü farklı çözüm ister** — biri description düzeltmesi, biri preload'a alma, biri
birleştirme. Aşama 1'de bu ayrım yapılmalı; yapılmazsa yanlış katman düzeltilir.

**Emsal uyarısı:** PAM ilk turda tam bu hatayı yaptı — yarayı doğru gördü (%62 reference
okunmamış), sebebini yanlış koydu (*"hook bozuk"*). Saha ölçümü hook'un çalıştığını
gösterdi. Yanlış teşhis yanlış çözüm üretecekti.

---

## Cevaplanmamış sorular — PAM'e bırakılan

**Alet katmanı ne olacak?** Kalsın mı, preload'a mı girsin, birleşip azalsın mı. Cevap
yukarıdaki üç adayın hangisinin doğru çıktığına bağlı.

**Reference katmanı nasıl paketlenecek?** 77 dosyanın 48'i hiç okunmamış. Aynı yapıyla
üretilirse aynı sonuç beklenir.

### Ölçümün bilinen sınırları — cevap beklenmiyor, bilinmesi gerekiyor

Bunlar PAM'e sorulan sorular değil; **elimizdeki ölçümün nereyi görmediği.** Bir karar
bu alanlara dayanacaksa dayanağın zayıf olduğu bilinsin diye yazıldı.

**Rol başına oturum sayısı ölçülemedi** — PCA denedi, `subagent_type` sayımı güvenilmez
çıktı (agent'lar terminal profilinden doğrudan açılıyor olabilir). Yani hangi rolün
sahada ne kadar çalıştığını bilmiyoruz.

**Mobil ve tasarım skill'lerinin neden açılmadığı ölçülmedi** — iş çalışılmadığı için mi,
kanon açılmadığı için mi. Bu iki rol için *sessizlik / yara* ayrımı yapılamıyor;
dolayısıyla o rollerin sessizliği yara kanıtı sayılmamalı.

---

## Haberleşme

**Kanal betikleri fabrikanın git deposunda değil** — n8n'in `KURULUM.md`'si bunu iki
önkoşuldan biri olarak başa yazıyor. Bugün bir makinede `~/.pr-kanal/` altında duruyorlar.

**Bu iş durdurulmayacak, ama sınır işaretlenmiştir:** OY takımı üretilir ve betikler
taşınmamışsa takım kurulur ama **konuşamaz.** PAD bu işte kanal assetini de taşırsa
sorun kapanır; taşımazsa `KURULUM.md`'ye aynı önkoşul yazılır.

---

## Açık riskler

**Ölçek riski — en büyüğü.** Fabrikanın tek ürünü n8n: **3 rol / 7 skill / 82 kural**,
~15 saat, 5 denetim turu (üçü GEÇMEDİ), ilk 5,5 saatte sıfır çıktı. OY: **9 rol / 76
skill / 574 kural** — skill sayısında 11 kat.

Kanonda **iş hacmine dayalı parçalama ölçütü yok.** `ISD-ONE-TEAM-PER-TURN` takım
sayısına bakar, `BHV-READ-FULL` dosya boyutuna; `BHV-LIST-BEFORE-RUNNING` hacim sorusunu
açıkça reddeder. Sahada bölme PAM'in kararıyla yapılmış, ölçütü **hata sınıfı farkı**.

**Bu yüzden aşamalı kurgu seçildi** — üç aşama tek iş değil, sıralı üç iştir. Aşama 2
bitmeden aşama 3 açılmaz.

**Sapma belgelenmemesi riski.** n8n'de gereksinim 4 rol yazdı, ürün 3 rol çıktı ve
birleştirme kararı gereksinime yazılmadı. Bu işte rol sayısı, skill sayısı ya da katman
kararı gereksinimden saparsa **sapma ve gerekçesi `status.md`'ye yazılır.**

**Fabrikanın kendi yükü.** `docs/fabrika/` altında **19 iş klasörü** var (`gereksinim.md`
ya da `status.md` içerenler), **18'inde `STATE:` satırı yok** — kendi kanonu
`ISD-KEEP-STATUS` kendi işlerinde uygulanmamış; `STATE:` taşıyan tek iş
`uretim-refleksi`. Üretim başlamamış altı iş, yarım kalmış üç iş var. Bu iş sıraya
girdiğinde PAM'in kuyruğu zaten dolu.

---

## Doğrulama eşikleri

**Aşama 1 geçti sayılır:** birleşik `behavior` + rol omurgası şablonu + **skill haritası
biçimi** + kural ID standardı + katman ölçütü + rol açma ölçütü yazılı ve denetimden
geçti. Ayrıca **description biçimi**: madde 2'nin sınavı — üretilen her description
*ne zaman açılacağını* söylüyor mu, içerik özeti mi.

**Aşama 2 geçti sayılır:** pilot rol kuruldu **ve sahada gerçek bir iş koşturuldu**;
preload edilen skill'lerin açıldığı ölçüldü. Dosya denetimi tek başına yeterli değil.

**Aşama 3 geçti sayılır:** sekiz rol üretildi, her biri aynı saha ölçümünden geçti,
`docs/filo/durum.md` güncellendi. (O dosyanın `## Kurulmuş takımlar` bölümü bugün
`Henüz yok.` diyor — n8n üretildiği hâlde filo kaydına işlenmemiş. Aynı boşluk bu
takımda tekrarlanmayacak.)
