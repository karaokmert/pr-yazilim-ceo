# Agent memory envanteri — 1537 dosya yetim, ortak konu SIFIR

**Tarih:** 2026-08-06
**Soru:** Mert'in *"agent memory'leri localde kalınca göremiyorum, neler var neler
bayat takip edilemiyor"* problemi ölçüldü.
**Script:** `sprint/memory-envanter.py`

## Neden bu ölçüm yapıldı

Qdrant ARGE'si sırasında Mert asıl niyetini söyledi: MCP'yi arama için değil
**görünürlük** için kurdurmuştu. Sonra düzeltti: *"görünürlük arama yoksa bir işe
yaramaz ki, agent bu memory'yi aktif kullanabilmeli ki görünürlük kazanımı olsun."*

İkisi ayrı iş ve ikisi de ölçülmemişti.

## Ölçüm 1 — 1744 dosya var, 1537'si yetim

`~/.claude/agent-memory` altında **20 v7 adlı kutu (1537 dosya)** ve **13 plugin adlı
kutu (207 dosya)**. Toplam 8.4 MB.

Sebep v7→v8 plugin geçişi: agent adı değişti (`qa-engineer` →
`ozel-yazilim-qa-engineer`), memory yolu adla belirlendiği için **yeni kutu açıldı,
eskisi terk edildi.**

Bölünmüş çiftler (eski → yeni):

- `project-assistant` **259** → `ozel-yazilim-project-assistant` 43
- `qa-engineer` **214** → `ozel-yazilim-qa-engineer` 35
- `backend-developer` **192** → `ozel-yazilim-backend-developer` 34
- `devops-engineer` **101** → 13, `frontend-developer` **94** → 23
- `web-qa-engineer` **87** → 12, `test-engineer` **61** → 3
- `web-fullstack-developer` **55** → 8, `code-auditor` **46** → 10
- `mobile-developer` 42 → 5, `web-devops-engineer` 26 → 3, `ui-designer` 19 → 6

Plugin karşılığı **hiç olmayan** (tam yetim): `agent-generator` 183, `ag-qa` 98,
`pr-agent-manager` 36, `web-test-engineer` 7, üç küçük kutu.

## Ölçüm 2 — ORTAK KONU SIFIR, her çiftte, istisnasız

Dosya adlarından konu seti çıkarıldı ve karşılaştırıldı:

- `project-assistant`: 258 eski konu / 42 yeni konu → **ortak 0**
- `qa-engineer`: 213 / 34 → **ortak 0**
- `backend-developer`: 191 / 33 → **ortak 0**
- `devops-engineer`: 100 / 12 → **ortak 0**
- `frontend-developer`: 93 / 22 → **ortak 0**
- diğer sekiz çift → hepsinde **ortak 0**

**Yeni kutular eskiden hiçbir şey devralmadı.** v8 agent'ları sıfırdan başladı; altı
aylık birikim olduğu yerde kaldı.

Bu, CLAUDE.md'de yazılı olan durumun ölçülmüş hâli: *"Tüm agentlar v8 olarak yeni bir
sürüme geçti... memoryler temiz."* Kabul edilmiş bir maliyetti — ama **1537 dosya**
olduğu bilinmiyordu.

## Ölçüm 3 — kaybedilen şey teori değil SAHA BİLGİSİ

Yalnız eski kutuda olan konulardan örnekler:

**Altyapı erişimi:** `a101egeli_kubeconfig`, `a101egeli_telepresence`,
`egelisaglik_api_finance_setup`, `deliverigo_infra`

**Çarpılmış duvarlar:** `azure_sp_secret_expiry_toplu_rebuild`,
`docker_hub_rate_limit_paralel_panel`, `ci-fail-altyapi-vs-kod`,
`coolify-env-buildtime-log-sizinti`

**Düşülmüş tuzaklar:** `hata-dersi_sqlserver-coklu-yol-cascade`,
`hata-dersi_turbo-cache-bozuk-veri-maskeleme`,
`hata-dersi_middleware-cerez-imza-dongu`, `caret-dep-regresyon-pin`

**Proje denetim geçmişi:** `deliverigo_audits_2026_06` + 5 modül kaydı,
`egelisaglik_audit_2026_04`, `balkanbee_readonly_olcum_7modul`

**Test verisi/kullanıcıları:** `a101egeli-test-user`,
`a101egeli-expert-company-test-user`, `deliverigo-test-user`

## Ölçüm 4 — TAZELIK: saha bilgisi hâlâ geçerli, fabrika kayıtları değil

v7 işareti taranan desenler: `skill-project`, `v7`, `.claude/skills/`,
`docs/v8-calisma`, `release tag`.

**Saha agent'ları %0-5:** `web-qa-engineer` %0, `qa-engineer` %2, `devops-engineer`
%2, `project-assistant` %3, `code-auditor` %4, `backend-developer` %5,
`frontend-developer` %5.

**Fabrika agent'ları yüksek:** `pr-agent-manager` **%66**, `agent-generator` **%38**,
`ag-qa` **%29**.

Yani saha bilgisi eski dünyaya bağlı değil — müşteri altyapısı, tuzaklar, test verisi
bugün de geçerli. Fabrika kayıtları ise eski fabrikanın kanonuna dayanıyor.

**Karar tablosu:** ortüşme sıfır + v7 işareti düşük = **TAŞI** (gerçek kayıp, gerçek
değer). Fabrika kutuları = ayrı muamele.

## Ölçüm 5 — bayatlık ölçütü olarak TARİH ÇALIŞMIYOR

`project-assistant` son yazma **2026-08-04** — yani "taze" görünüyor. Ama o tarih v7
agent'ının son çalışması; bugünkü PA o kutuya hiç bakmıyor.

30+ gündür dokunulmayan yalnız iki klasör var (`web-test-engineer` 33 gün,
`pr-memtest` 32 gün). Yani `ls -la` ile bakınca **her şey taze görünüyor** ve %88'i
ölü.

**Gerçek ölçüt:** klasör adı yürürlükteki agent adıyla eşleşiyor mu. Tarih değil.

## Ölçüm 6 — agent kendi kutusunu nasıl görüyor (mekanik)

Kanon (`ozel-yazilim/memory-management/SKILL.md`) iki şey diyor:

- `memory: user` → `~/.claude/agent-memory/{agent-adı}/MEMORY.md`, ve
  **auto-injection ilk 200 satır / 25 KB'ı yükler.**
- *"Açılışta proaktif okunmaz. İşe/soruya bağlı okunur"* (`MEMORY-NO-OPEN-SCAN`) —
  yani **dosyalar `Read` gerektiriyor**, indeks otomatik gelir.

Kanonun kendi cümlesi: *"İndeks EMİR taşır — dosyalar taşımaz."*

**Sonucu:** agent kendi kutusunda indeksi görüp dosya açabilir. Başka kutuda ne
olduğunu **bilemez** — adı eşleşmiyor, indeksi yüklenmiyor.

## Çıkan tasarım — kendi kutusu İNDEKS, arşiv ARAMA

İki erişim ihtiyacı var ve çözümleri farklı:

**Kendi kutusu (43 kayıt) → indeks yeterli, arama gereksiz.** Ölçüldü
(`incelemeler/qdrant-kayit-bicimi/`): 20 kayıtta `MEMORY.md` indeksi **10/10**, Qdrant
**4/10**. Sebep: indeks satırını insan yazıyor ve kaydın *ne işe yaradığını* söylüyor;
vektör kaydın *neye benzediğini* ölçüyor.

**Arşiv (259 kayıt) → indeks çözümü çalışmaz.** 259 satırlık indeks auto-injection'ın
200 satır sınırını aşıyor (kanonda yazılı) ve context'i şişirir. Burada arama
gerekiyor — ve grep yetmez, çünkü agent'ın aklına gelmeyen kelimeyi bulamaz.

**Arşiv aramasının şartı (bugün ölçüldü):** filtre zorunlu
(`agent=qa-engineer`, `proje=a101egeli`) — filtresiz isabet 5/7, filtreli 7/7. **Ve
filtre MCP'den kullanılamıyor** (`qdrant-find` yalnız `{collection_name, query}`
alıyor).

## Açık kalemler — karar Mert'te

**1. Taşınacak mı, arşiv olarak mı kalacak?** 1537 dosyada değer ölçüldü ama taşımak
uzun iş: her kayıt yeni kutuya kopyalanmaz — indeks 200 satır sınırına takılır. Yani
taşıma = seçme + özetleme, mekanik kopya değil.

**2. Fabrika kutuları (317 dosya: agent-generator + ag-qa + pr-agent-manager) ne
olacak?** v7 işareti %29-66. Yeni fabrika (`agent-project` PAM/PAD/PQA/PCA) bunları
devralmadı ve devralması gerekip gerekmediği bu odanın konusu değil — fabrikanın.

**3. Arşiv arama kapısı hangi araçla?** Qdrant'ın yeri burası ama filtre MCP'den
çalışmıyor. Üç yol `kararlar/2026-08-06-arama-disiplini.md`'de.

**Ölçülmedi:** kayıtların içerik kalitesi (dosya adlarından değer çıkarıldı, gövdeler
tek tek okunmadı), aynı bilginin iki kutuda farklı adla durup durmadığı (ad bazlı
ortüşme sıfır ama içerik bazlı ölçülmedi).
