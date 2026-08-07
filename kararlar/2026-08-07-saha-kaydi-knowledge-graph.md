# Saha kaydı knowledge graph'a yazılır

**Tarih:** 2026-08-07
**Karar veren:** Mert
**Durum:** Yürürlükte (şimdilik — Qdrant ölçüldü, elendi)

## Karar

Monitörlükte tutulan her kayıt — proje durumu, sprint, kararlar, agent arızaları
ve kazanımları — **knowledge graph MCP'ye** (`mcp__plugin_ozel-yazilim_memory__`)
yazılır.

Mert'in cümlesi: *"bence knowledge graph ile ilerleyelim şimdilik, bunu kanona
yazalım. Takip ve kayıt buraya yapılsın, arama bulma ilişki bilgileriyle."*

## Neden — üç seçenek ölçüldü

Aynı GOAT bilgisi üç yapıya da yazıldı ve aynı sorularla sınandı.

### 1. Qdrant, ayrı koleksiyonlar (`clara-goat-durum`, `-sprint`, `-kararlar`…)

**Artısı:** anlam eşleşmesi çalışıyor. *"Sponsoru cezalandırmak istersek"* diye
soruldu — kayıtta "cezalandırmak" kelimesi yok, "yaptırım" var; doğru kaydı
getirdi. *"Hangi kuralı defalarca tekrar etmek zorunda kaldım"* → doğru arıza.

**Eksisi:** alaka eşiği yok. *"İtalyan mutfağında makarna pişirme süresi"*
sorusuna sponsor statüleri kaydı döndü. 1 kayıtta zararsız, 50 kayıtta her sorgu
alakasız şeyler döndürür ve model onları bağlam sanır.

### 2. Qdrant, tek koleksiyon + etiket (`clara-saha`, `[GOAT] [DURUM]` etiketli)

**Mert'in önerisiydi, ÖLÇÜLDÜ VE ÇALIŞMADI.** Dört kayıt yazıldı (2 GOAT,
1 OSİNİF, 1 agent arızası). İki soru soruldu:

- *"GOAT durum nerede kaldık"* → **dört kaydın hepsi döndü**, üstelik birinci
  sırada agent arızası geldi
- *"agent arıza tekrarlayan uyarı"* → yine **dört kayıt birden**

Sebep: `qdrant-find` eşik uygulamıyor, `limit` parametresi yok — koleksiyondaki
her şeyi alaka sırasına dizip döndürüyor. Etiket metne giriyor ama sıralamayı
belirleyecek ağırlık taşımıyor; anlam gövdeden geliyor.

**Ayrı koleksiyon bunu çözer çünkü ayrımı arama değil ADRES yapar** — ama o zaman
5 proje × 3 alan + 2 agent alanı = 17 koleksiyon eder.

### 3. Knowledge graph (SEÇİLEN)

**Artısı — Qdrant'ın yapamadığı iki şey:**

- **İlişki tutuyor.** `open_nodes("GOAT")` tek çağrıda GOAT'ı ve ona bağlı her
  şeyi verdi: iki task, bir arıza, ilişki türleriyle. Qdrant'ta bunun için üç
  ayrı koleksiyona ayrı ayrı sormak gerekir.
- **Yanlış cevap vermiyor.** *"Makarna pişirme süresi"* → boş döndü. Alakasız
  sonucu bağlam sanma riski yok.

**Eksisi:** arama kelime bazlı. *"Sponsoru cezalandırmak"* → boş döndü (kelime
kayıtta yok). *"Yayından kaldır"* → doğru sonuç + ilişkiler.

**Kabul edilen bedel:** doğru kelimeyi bilmek gerekiyor. Karşılığında yapı ve
kesinlik kazanılıyor — ve asıl ihtiyaç ("hangi projede nerede kaldık, sprint ne
durumda") bir **yapı** sorusu, anlam sorusu değil.

## Yazılan kayıt düzeni

**Varlık tipleri:** `proje`, `task`, `karar`, `ariza`, `kazanim`, `agent`

**İlişki örnekleri (aktif çatı):**
- `PRY-17449` → `GOAT` : *sprintinde yer alır*
- `karar-sponsor-statuleri` → `PRY-17449` : *kapsamında alındı*
- `ariza-dort-kontrol` → `project-assistant` : *agentını etkiliyor*
- `ariza-dort-kontrol` → `GOAT` : *projesinde gözlendi*
- `kazanim-dort-kaynakli-okuma` → `ariza-dort-kontrol` : *arızasını çözer*
- `kazanim-dort-kaynakli-okuma` → `PRY-17455` : *işinde kanıtlandı*

Son iki ilişki türü kritik: **kazanım hangi arızayı çözüyor** ve **hangi işte
kanıtlandı** — Mert'in "ikinci denemede başarılıysa skill'e taşınır" eşiği bu
bağdan okunur.

## Qdrant'a ne oldu

Silinmedi (Mert: *"kalsın, bir şey silme"*). Yazılan koleksiyonlar duruyor:
`clara-goat-durum`, `clara-goat-sprint`, `clara-goat-kararlar`,
`clara-agent-arizalar`, `clara-agent-kazanimlar`, `clara-saha`.

**İleride açılabilecek kapı:** "eski bir kararı kelimesini hatırlamadan ara"
ihtiyacı doğarsa Qdrant ikinci katman olarak eklenebilir. Şimdilik ihtiyaç
doğmadı — kapasite kurulmuyor.

## İlgili

- `gunluk/2026-08-06.md` — monitörlüğün dört göreve ayrılması
- `.claude/agent-memory/clara/feedback_monitorluk_dort_gorev.md`
