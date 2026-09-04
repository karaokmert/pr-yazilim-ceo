# Agent hafızası (RAG) — bilinmesi gerekenler

Kaynak: 2026-09-04 ARGE turu, Mert + Clara. Konu: agent'lara kalıcı anlamsal
hafıza — self-hosted Qdrant + Türkçe embedding.

---

## İşin hikâyesi — neden ikinci deneme

**Birinci deneme (2026-08 başı):** Qdrant kuruldu, 44 koleksiyon doldu, çalıştı —
ve Mert kapattı: *"mantıklı bulmadık ve kullanmadık."* Ölen şey teknik değil
kullanım değeriydi. (Karar: `konular/olcum-arama/kararlar/2026-08-16-vektor-cikti-grep-disiplini-girdi.md`)

**İkinci denemenin tetiği (2026-09-04):** Mert resmi Qdrant MCP'yi yetersiz bulup
bir repo forkladı; Türkçe embedding modelini bilgisayarına kurmak zorunda kaldı,
cache sorunları yaşadı, verim alamadı. Asıl acı: **embedding'in bilgisayarda
koşması.** Çözüm yönü: embedding + Qdrant sunucuya, MCP ince istemci.

⚠️ Birinci denemenin dersi açık duruyor: altyapı değeri kendiliğinden üretmez.
"Kurduk ama kullanmadık" sonucu bu sefer **kullanımla ölçülecek.**

---

## Zemin kararı

Araç sunucusu (ekip self-hosted araçları; VPN + Coolify burada) zemini **Coolify
kalıyor** — K8s bu masada değil. Ölçüldü: Coolify K8s üstünde çalışmıyor
(Docker/Swarm, K8s "coming soon").
→ `konular/altyapi/kararlar/2026-09-04-arac-sunucusu-zemini-coolify.md`

Mimari: **Qdrant container + TEI (text-embeddings-inference) container** Coolify'da,
MCP yalnız HTTP istemcisi. Bilgisayarda model ve cache kalmaz.

---

## Türkçe embedding modeli — ölçüm kaynağı ve adaylar

**Ölçüm kaynağı: TR-MTEB** (EMNLP 2025 Findings, `huggingface.co/trmteb`) —
Türkçe'ye özel benchmark, 6 görev, 26 veri seti. Kendi soru listemizi uydurmak
yerine bu kullanılır (TrGLUE prensibi, bkz. `konular/hugging-face/`).

**TR-MTEB Tablo 2'den okundu (2026-09-04):**

- **multilingual-e5-large** — açık modellerin birincisi: Mean 66.82, Retrieval
  60.62, STS 81.18. 560M parametre, 1024 boyut. Lisans MIT (⚠️ kurulumda model
  kartından doğrulanacak).
- **multilingual-e5-base** — Mean 64.26, Retrieval 58.29. 278M parametre — CPU
  sunucuda makul olan bu.
- **multilingual-e5-small** — Retrieval 56.53, 118M. En hafif kabul edilebilir.
- **gte-multilingual-base** — Mean 64.49, Retrieval 57.51. Apache-2.0.
- text-embedding-3-small (OpenAI) — Retrieval 64.99 ile tablonun retrieval
  birincisi ama API-only, self-hosted değil. Bilgi olarak duruyor.
- BGE-M3 **tabloda yok** — TR-MTEB test etmemiş. "Türkçe'de iyi" iddiası bizim
  için ölçüsüz kalır.
- LaBSE ve paraphrase-multilingual ailesi retrieval'da belirgin geride (46-49).

**Öneri (Clara):** TEI + **multilingual-e5-base** ile başla; verim yetmezse
large'a geçiş tek env değişikliği. TEI ikisini de destekliyor.

⚠️ **E5 tuzağı:** e5 ailesi girdi öneki ister — sorguya `query: `, belgeye
`passage: ` eklenmezse retrieval kalitesi sessizce düşer. MCP istemcisi bunu
eklemek zorunda. (Mert'in ilk denemesindeki "verim alamadım"ın bir sebebi bu
olabilir — hangi modeli kullandığı sorulmadı, ölçülmedi.)

⚠️ **FastEmbed cache tuzağı** (kayıtlı): model varsayılanda geçici alana iner,
`FASTEMBED_CACHE_PATH` şart. Sunucu mimarisinde FastEmbed devre dışı kalacağı
için bu tuzak kökünden kalkıyor.

---

## MCP istemcisi — fork okundu (2026-09-04)

**Repo: `karaokmert/qdrant-mcp`** (Andrew Lewin'in qdrant-mcp'sinin fork'u;
Mert'in hatırladığı `mcp-server-qdrant` adı resmi Qdrant reposudur, fork o değil).

**Mert'in fork'a eklediği (2025-08-13 commit'leri):** dinamik koleksiyon desteği —
tüm araçlara isteğe bağlı `collection_name`, yanıtlarda koleksiyon bilgisi, tek
sunucuyla çok koleksiyon. **Resmi MCP'nin yetersizliği buydu: tek koleksiyon +
FastEmbed'e kilitli embedding.** Fork'un gereksinim listesi = çoklu koleksiyon +
embedding sağlayıcı seçimi.

**Fork'un bugünkü iki eksiği (okundu, satır düzeyinde):**
1. `embeddings/openai.py:37` — `base_url` api.openai.com'a **hardcode**. TEI
   OpenAI-uyumlu `/v1/embeddings` sunduğu için tek satır + env değişkeniyle
   (`OPENAI_BASE_URL`) fork self-hosted TEI'ye bağlanabilir. Küçük yama.
2. **e5 öneki yok** — `query:`/`passage:` hiçbir sağlayıcıda eklenmiyor. mE5
   kullanılacaksa store→`passage: `, find→`query: ` MCP'de eklenmeli. Küçük yama.

**Lokal acının kök sebebi doğrulandı:** fork'ta iki sağlayıcı var (openai /
sentence-transformers); Türkçe model için sentence-transformers seçilince model
bilgisayara indi — cache ve verim sorunu oradan. TEI'ye geçince bu yol kapanıyor,
sentence-transformers sağlayıcısına hiç gerek kalmıyor.

---

## Mert'in beklentisi — gereksinim (2026-09-04, kendi ağzından)

*"Pluginlerim var, agentların yaşadığı — ekibe veriyorum, artık onlar da bunu
kullanıyor. Projeler için collectionlar olsun. Kararlar collectionda yaşasın.
Skill önerileri collectionda yaşasın. Kişisel tercihler collectionda yaşasın.
Türkçe anlamlı gruplanabilir olsun."*

Çözülen: geçen denemenin ölüm sorusu ("ne yazılacak") artık cevaplı — dört
içerik sınıfı: **proje dersleri · kararlar · skill önerileri · kişisel
tercihler.** Tüketici: plugin'lerle dağıtılan saha ekipleri (OY/WS/n8n) +
Clara. Dağıtım kanalı: MCP tanımı plugin'lere eklenir.

## Kurumsal konum ve ufuk (Mert, 2026-09-04)

Bu araç bir iç deney değil — **PR Venture Studio'nun (AI şirketi) ilk altyapı
servisi.** Adresi `rag.prventurestudio.com` (domain stratejisi:
`konular/altyapi/BILINMESI-GEREKENLER.md`).

Mert'in ufku: *"şimdilik bizim agentların hafızası ama ileride ürünlere de
altyapı olabilir — mesela Keba AI projesini buraya bağlayarak test ederiz."*

⚠️ Tasarım sonucu: ürün kapısı bugün KURULMAZ (yalın üretim) ama KAPATILMAZ —
Qdrant'ın API key + koleksiyon modeli ayrımı zaten taşıyor; bugünkü tek
gereği adres/SSL/erişimin baştan düzgün kurulması. Keba AI projesi Clara'ya
henüz anlatılmadı — bağlama günü gelince tanışılacak.

## Büyük test sonuçları (2026-09-04, mE5-base)

**Kayıt yöntemi:** hüküm > blok. 16 soruluk sette hüküm yöntemi 15/15 ilk
sırada (İngilizce, tek kelime, belirti dili dahil); blok yöntemi 3 soruda
kaçırdı — en öğreticisi "lisans": doğru bilgi büyük blokta gömülünce 5.
sıraya düştü. **Bir kayıt bir fikir taşır.** Filtre yalnız hüküm yönteminde
anlamlı. Eşik bandı: doğru 0.82-0.88, alakasız ~0.77 — "cevap yok" eşiği
~0.80 adayı, büyük veriyle yeniden ölçülecek.

**Mükerrer hüküm bulgusu:** iki ayrı kaynaktan çıkarılan benzer hükümler
sıralamada birbiriyle yarışıyor (ikisi de doğru ama sıra bölünüyor) —
yükleme hattına tekilleştirme adımı gerekecek.

**Kanal testi (kör agent, 8 soru — local dosya vs Qdrant):**
- Doğruluk: İKİSİ DE 8/8. Bu repo iyi örgütlü olduğu için grep tarafı da bulabildi.
- Maliyet: Qdrant 8 araç çağrısı / ~92K token / 75 sn · Dosya 15 çağrı /
  ~116K token / 95 sn. Qdrant soru başına TEK aramayla, sabit ve öngörülebilir
  maliyetle cevapladı.
- Derinlik farkı: dosya tarafı iki soruda daha zengin cevap verdi (örn.
  sprint custom field ID'si ham dosyada var, hüküm özetinde yok).
- **Tasarım sonucu: iki kanal rakip değil KATMAN.** Hafıza ilk durak (ucuz,
  tek arama, hüküm + kaynak adresi) → derinlik gerekirse adresteki dosya
  açılır. "Hüküm merkezde, doküman repo'da" ilkesi kanal testiyle doğrulandı;
  kaynak_adres alanı bu köprünün kendisi.
- Sınır: tek koşum, tek repo, 8 soru — varyans ölçülmedi; dosya tarafının
  başarısı bu reponun düzenli oluşuna borçlu, çapraz-proje soruda ölçülmedi.

Test düzeneği: `test/hafiza_testi.py` (tekrar koşulabilir) · veri:
`test/gercek_hukumler.jsonl` (120 hüküm + 36 elle) · arama CLI:
`test/hafiza_ara.py`. Bekleyen: mE5-large karşılaştırması (MODEL_ID değişimi
Mert'te).

## Açık kalanlar

1. **Koleksiyon şeması ve sahiplik kuralları** — Clara önerisi Mert'le
   tartışılıyor (bkz. PLAN Aşama 4). Kritik ilke adayı: hafızaya doküman değil
   KISA HÜKÜM yazılır (ders/karar/tercih/öneri); dokümanın evi repo'da kalır —
   çift ev arızası (iki yol tek kayıt) böyle önlenir.
2. **Fork yamasını kimin yapacağı** — iki küçük değişiklik (base_url + e5
   öneki). Clara üretim yapmaz; Mert elden yapar ya da bir agent'a verilir.
3. **Sunucuda GPU var mı** — model boyu seçimini etkiler. Sorulmadı; mE5-base
   CPU'da makul, büyütme kararı kullanımdaki gecikmeye göre.
4. **PulseMCP taraması (2026-09-04):** vektörsüz alternatifler var — Basic
   Memory (markdown + anlam grafiği, listenin en popüleri), Memory Kernel
   (SQLite FTS5). Türkçe'de kelime-bazlı aramanın tuzağı bilindiğinden vektör
   yolu seçildi; bunlar elenmiş değil, ölçülmemiş.
