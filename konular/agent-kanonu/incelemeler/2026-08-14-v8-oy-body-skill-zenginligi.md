# V8 Özel Yazılım — Body Skill Zenginliğini Nasıl Tarif Ediyor?

**Ölçüm:** 2026-08-14 · **Kaynak:** `v8/ozel-yazilim` (plugin 0.7.0) · 9 agent body
**Soru:** agent açılışta *"elimde bir sürü skill ve düzen var"* bilgisini body'den alıyor mu?

---

## Sonuç önce — üç bulgu

### 1. Hiçbir body kaç skill olduğunu söylemiyor

Dokuz body'nin **hiçbirinde** bir sayı yok. Ne *"77 skill"*, ne *"21 alet"*, ne *"12 alan skili"*.
Agent açılışta arkasında ne kadar birikim olduğunu **bilmiyor** — yalnız *"skiller (kanon)"* diye bir kategori adı görüyor.

### 2. On-demand skillerin yarısının adı body'de hiç geçmiyor

| Agent | On-demand skill | Body'de adı geçen | Kapsam |
|---|---:|---:|---:|
| project-assistant | 10 | 8 | **%80** |
| ui-designer | 12 | 7 | **%58** |
| backend-developer | 21 | 16 | **%76** |
| frontend-developer | 19 | 8 | **%42** |
| mobile-developer | 19 | 9 | **%47** |
| qa-engineer | 17 | 5 | **%29** |
| test-engineer | 10 | 3 | **%30** |
| code-auditor | 6 | 4 | **%67** |
| devops-engineer | 12 | 7 | **%58** |
| **TOPLAM** | **126** | **67** | **%53** |

Yani agent'ın işi sırasında açması beklenen skillerin **%47'i body'de hiç anılmıyor.**
Body onları *"omurgaya bak, liste orada"* diye devrediyor — ama omurga on-demand, yani açılışta context'te değil.

### 3. Zenginlik "kategori" olarak tarif ediliyor, "envanter" olarak değil

Dokuz body'nin dokuzunda da aynı paragraf var: **"Tek başına çalışmıyorsun."**
Ve dokuzu da aynı kalıbı kullanıyor: *"Elinde yalnız X yok: skiller (kanon), referans projeler, modül dokümanları … var."*

`skiller (kanon)` — **iki kelime.** Referans projelerle, modül dokümanlarıyla, ClickUp'la aynı cümlede, aynı ağırlıkta, sıradaki bir kalem olarak.
77 skillik bir kütüphane ile 4 referans projesi bu cümlede **eşit** görünüyor.

---

## Bunun sonucu ne

Agent açılışta şunu biliyor: *"skiller var, okumalıyım."*
Agent açılışta şunu **bilmiyor**: *"kaç tane var, hangi alanları kapsıyor, benim işimin kaç ayrı skili var."*

Fark şurada: birincisi bir **uyarı**, ikincisi bir **harita**. Uyarı davranış değiştirmez — agent zaten okuması gerektiğini biliyor, sorun ne okuyacağını bilmemesi.

Ve body'nin devrettiği yer sorunu çözmüyor: *"tam liste omurgada"* deniyor ama omurga (`backend`, `quality`, `frontend`…) **preload** — yani açılışta yüklü. Sorun listenin yerinde değil, **listenin sayısız olmasında**: agent 21 aletlik bir çantayı 3 aletlik bir çantadan ayırt edemiyor.

---

# Agent

## project-assistant

**Body gövdesi:** 120 satır · **Skill bölümü:** var (`## Skiller`)

### Body skillerin zenginliğini nasıl tarif ediyor

**"Tek başına çalışmıyorsun" paragrafı:**

> Elinde yalnız kullanıcının cümlesi yok: skiller (kanon), ClickUp task/comment/Doc'ları, modül dokümanları, kod ve referans projeler var. Aradığın cevapların çoğu zaten yazılı — gereksinim üretmeden önce **onları okursun**. Koddan/dokümandan bulunabilecek şeyi kullanıcıya sormak z

→ Skiller burada **`skiller (kanon)`** olarak, diğer kaynaklarla aynı sırada anılıyor. Sayı yok, kapsam yok, alan yok.

**`## Skiller` bölümü ne diyor:**

> **Preload (çekirdek + omurga):** `behavior` · `handoff` · `memory-management` · `is-akisi` · `pr-yazilim-oy-envanteri` · `project-assistant` (alet çantası + kimlik).

> **On-demand — iş türü değişince AÇILIR, tur başında bir kez değil.** PA işi tek tür değildir ve her türün AYRI skili, ayrı kuralları var. Hangi işi yapıyorsan **o anda** onun skilini açarsın; tür değişince (discovery→ClickUp, planlama→triyaj) yeniden açarsın. Omurgayı (`project-assistant`) açmış olm

> **İş türü → skil** (tam liste: `project-assistant` omurga → Alet çantası):

### Ölçüm

| | |
|---|---|
| Preload skill | 8 (body hepsini adıyla sayıyor ✅) |
| On-demand skill | 10 |
| Bunlardan body'de adı geçen | **8** (%80) |
| Body'de sayı belirtiliyor mu | **HAYIR** |

**Body'de adı hiç geçmeyen on-demand skiller (2):**

`figma` · `proje-dosya-duzeni`

---

## ui-designer

**Body gövdesi:** 93 satır · **Skill bölümü:** var (`## Skiller`)

### Body skillerin zenginliğini nasıl tarif ediyor

**"Tek başına çalışmıyorsun" paragrafı:**

> Elinde yalnız bu projenin kodu yok: skiller (kanon), design token'ları, component catalog, referans projeler ve emsal ekranlar var. Aradığın cevapların çoğu zaten yazılı — sen üretmeden önce **onları okursun**. Hız uğruna atlama: hafızadan seçilen renk/spacing, catalog'u okuyan b

→ Skiller burada **`skiller (kanon)`** olarak, diğer kaynaklarla aynı sırada anılıyor. Sayı yok, kapsam yok, alan yok.

**`## Skiller` bölümü ne diyor:**

> **Preload (çekirdek + omurga):** `behavior` · `handoff` · `memory-management` · `is-akisi` · `pr-yazilim-oy-envanteri` · `ui-designer` (alet çantası + kimlik).

> **On-demand — dokunma anında AÇILIR, iş başında bir kez değil.** Tasarım işi tek alan değildir: token/design system, prototip sayfa, Figma girdisi, hazır kod dönüştürme, devir — her birinin AYRI skili var. Hangi alana dokunuyorsan **o anda** onun skilini açarsın; girdi tipi değişince (Figma→gereksin

> **Skil açmak yavaşlatmaz — açmamak geri söktürür.**

### Ölçüm

| | |
|---|---|
| Preload skill | 6 (body hepsini adıyla sayıyor ✅) |
| On-demand skill | 12 |
| Bunlardan body'de adı geçen | **7** (%58) |
| Body'de sayı belirtiliyor mu | **HAYIR** |

**Body'de adı hiç geçmeyen on-demand skiller (5):**

`code-quality` · `database` · `enum-sync` · `response-request` · `tasarim-prensipleri`

---

## backend-developer

**Body gövdesi:** 92 satır · **Skill bölümü:** var (`## Skiller`)

### Body skillerin zenginliğini nasıl tarif ediyor

**"Tek başına çalışmıyorsun" paragrafı:**

> Elinde yalnız bu projenin kodu yok: skiller (kanon), referans projeler (emsal insan-developer kodu), modül dokümanları ve `pryazilim.core` envanteri var. Aradığın cevapların çoğu zaten yazılı — sen üretmeden önce **onları okursun**. Hız uğruna atlama: "hafızamdan biliyorum" diyer

→ Skiller burada **`skiller (kanon)`** olarak, diğer kaynaklarla aynı sırada anılıyor. Sayı yok, kapsam yok, alan yok.

**`## Skiller` bölümü ne diyor:**

> **Preload (çekirdek + omurga):** `behavior` · `handoff` · `memory-management` · `is-akisi` · `pr-yazilim-oy-envanteri` · `backend` (alet çantası + kimlik).

> **On-demand — dokunma anında AÇILIR, iş başında bir kez değil.** Backend işi tek alan değildir: handler, DataLayer, tablo/migration, enum, yanıt zarfı, kimlik, core yardımcı — her birinin AYRI skili ve ayrı kuralları var. Hangi alana dokunuyorsan **o anda** onun skilini açarsın; alan değişince (kod→

> Atlarsan ne olur, ölçüldü: kanonu hafızadan uygulayan BE kendi kodunda 3 ihlal taşıdı (ticket-yorum, iki iş yapan metod, sessiz kritik hata); skiller açılınca hepsi çıktı. **Skil açmak yavaşlatmaz — açmamak geri söktürür.**

### Ölçüm

| | |
|---|---|
| Preload skill | 6 (body hepsini adıyla sayıyor ✅) |
| On-demand skill | 21 |
| Bunlardan body'de adı geçen | **16** (%76) |
| Body'de sayı belirtiliyor mu | **HAYIR** |

**Body'de adı hiç geçmeyen on-demand skiller (5):**

`api-project` · `code-quality` · `dev-environment` · `gosterim-formatlari` · `tasarim-prensipleri`

---

## frontend-developer

**Body gövdesi:** 99 satır · **Skill bölümü:** var (`## Skiller`)

### Body skillerin zenginliğini nasıl tarif ediyor

**"Tek başına çalışmıyorsun" paragrafı:**

> Elinde yalnız bu projenin kodu yok: skiller (kanon), referans projeler (emsal insan-developer kodu), modül dokümanları ve API.md sözleşmesi var. Aradığın cevapların çoğu zaten yazılı — sen üretmeden önce **onları okursun**. Hız uğruna atlama: "hafızamdan biliyorum" diyerek yazdığ

→ Skiller burada **`skiller (kanon)`** olarak, diğer kaynaklarla aynı sırada anılıyor. Sayı yok, kapsam yok, alan yok.

**`## Skiller` bölümü ne diyor:**

> **Preload (çekirdek + omurga):** `behavior` · `handoff` · `memory-management` · `is-akisi` · `pr-yazilim-oy-envanteri` · `frontend` (alet çantası + kimlik).

> **On-demand — dokunma anında AÇILIR, iş başında bir kez değil.** Frontend işi tek alan değildir: component, form, liste, veri katmanı, stil, enum, gösterim formatı — her birinin AYRI skili ve ayrı kuralları var. Hangi alana dokunuyorsan **o anda** onun skilini açarsın; alan değişince (component→form

> Atlarsan ne olur, ölçüldü: kanonu hafızadan uygulayan developer kendi kodunda ihlal taşıdı; skiller açılınca hepsi çıktı. **Skil açmak yavaşlatmaz — açmamak geri söktürür.**

### Ölçüm

| | |
|---|---|
| Preload skill | 6 (body hepsini adıyla sayıyor ✅) |
| On-demand skill | 19 |
| Bunlardan body'de adı geçen | **8** (%42) |
| Body'de sayı belirtiliyor mu | **HAYIR** |

**Body'de adı hiç geçmeyen on-demand skiller (11):**

`auth` · `code-quality` · `database` · `design-handoff` · `dev-environment` · `excel-export` · `figma` · `realtime` · `response-request` · `screen-structure` · `tasarim-prensipleri`

---

## mobile-developer

**Body gövdesi:** 97 satır · **Skill bölümü:** var (`## Skiller`)

### Body skillerin zenginliğini nasıl tarif ediyor

**"Tek başına çalışmıyorsun" paragrafı:**

> Elinde yalnız bu projenin kodu yok: skiller (kanon), referans projeler (emsal insan-developer kodu), modül dokümanları ve BE'nin API sözleşmesi var. Aradığın cevapların çoğu zaten yazılı — sen üretmeden önce **onları okursun**. Hız uğruna atlama: "hafızamdan biliyorum" diyerek ya

→ Skiller burada **`skiller (kanon)`** olarak, diğer kaynaklarla aynı sırada anılıyor. Sayı yok, kapsam yok, alan yok.

**`## Skiller` bölümü ne diyor:**

> **Preload (çekirdek + omurga):** `behavior` · `handoff` · `memory-management` · `is-akisi` · `pr-yazilim-oy-envanteri` · `mobile` (alet çantası + kimlik).

> **On-demand — dokunma anında AÇILIR, iş başında bir kez değil.** Mobil işi tek alan değildir: ekran, navigasyon, state, stil, veri katmanı, permission, release — her birinin AYRI skili ve ayrı kuralları var. Hangi alana dokunuyorsan **o anda** onun skilini açarsın; alan değişince (ekran→state, stil→

> Atlarsan ne olur, ölçüldü: kanonu hafızadan uygulayan developer kendi kodunda ihlal taşıdı; skiller açılınca hepsi çıktı. **Skil açmak yavaşlatmaz — açmamak geri söktürür.**

### Ölçüm

| | |
|---|---|
| Preload skill | 6 (body hepsini adıyla sayıyor ✅) |
| On-demand skill | 19 |
| Bunlardan body'de adı geçen | **9** (%47) |
| Body'de sayı belirtiliyor mu | **HAYIR** |

**Body'de adı hiç geçmeyen on-demand skiller (10):**

`auth` · `code-quality` · `design-handoff` · `dev-environment` · `gosterim-formatlari` · `local-payment` · `mobile-release` · `realtime` · `response-request` · `tasarim-prensipleri`

---

## qa-engineer

**Body gövdesi:** 129 satır · **Skill bölümü:** var (`## Skiller`)

### Body skillerin zenginliğini nasıl tarif ediyor

**"Tek başına çalışmıyorsun" paragrafı:**

> Elinde yalnız bu commit'in diff'i yok: skiller (kanon), denetim lensi, referans projeler ve modül dokümanları var. Denetlediğin kuralı **okumadan** "uygun" demek en sık kaçıran reflekstir — kapı sensin, hafızadan denetim kapıyı deler. Yavaş okumak, kaçan hatayı prod'da bulmaktan 

→ Skiller burada **`skiller (kanon)`** olarak, diğer kaynaklarla aynı sırada anılıyor. Sayı yok, kapsam yok, alan yok.

**`## Skiller` bölümü ne diyor:**

> **Preload (çekirdek + omurga):** `behavior` · `handoff` · `memory-management` · `is-akisi` · `pr-yazilim-oy-envanteri` · `quality` (alet çantası + kimlik) · `dev-deploy` (push/merge kanonu) · `prod-deploy` (canlıya çıkış zinciri).

> ⚠️ **Yüklü olmak açmış saymaz.** `dev-deploy` context'inde duruyor ama PUSH ŞABLONU'nun koruması okumaktan değil **yazmaktan** gelir: push anında dört adımı çıktına sırayla yazarsın. Okumak sessizce atlanır, yazılmayan adım görünür. Aynısı prod için: zinciri yüklü sanmak yetmez, hangi adımda olduğun

> **On-demand — denetim türü değişince AÇILIR, tur başında bir kez değil.** Denetim tek tür değildir: commit inceleme, modül/consistency audit, canlıya çıkış, kaçan hata analizi — her birinin AYRI skili ve ayrı kapı kuralları var. Hangi türü yapıyorsan **o anda** onun skilini açarsın; tür değişince ye

### Ölçüm

| | |
|---|---|
| Preload skill | 8 (body hepsini adıyla sayıyor ✅) |
| On-demand skill | 17 |
| Bunlardan body'de adı geçen | **5** (%29) |
| Body'de sayı belirtiliyor mu | **HAYIR** |

**Body'de adı hiç geçmeyen on-demand skiller (12):**

`auth` · `code-auditor` · `database` · `enum-sync` · `escaped-bug-analysis` · `module-audit` · `module-development` · `orkestrasyon` · `production-audit` · `response-request` · `setup-ozelyazilim-plugin` · `style-mobile`

---

## test-engineer

**Body gövdesi:** 89 satır · **Skill bölümü:** var (`## Skiller`)

### Body skillerin zenginliğini nasıl tarif ediyor

**"Tek başına çalışmıyorsun" paragrafı:**

> Elinde yalnız çalışan uygulama yok: skiller (kanon), DISCOVERY, modül dokümanları, API sözleşmesi ve emsal senaryolar var. Senaryoyu **okumadan** üretmek eksik kapsam demektir; kaçan yol prod'da hata olur. Yavaş okumak, kaçan senaryodan ucuzdur. Bulgu üretirken kanıt zinciri kur:

→ Skiller burada **`skiller (kanon)`** olarak, diğer kaynaklarla aynı sırada anılıyor. Sayı yok, kapsam yok, alan yok.

**`## Skiller` bölümü ne diyor:**

> **Preload (çekirdek + omurga):** `behavior` · `handoff` · `memory-management` · `is-akisi` · `pr-yazilim-oy-envanteri` · `test-engineer` (alet çantası + kimlik).

> **On-demand — mod değişince AÇILIR, tur başında bir kez değil.** Test işi tek mod değildir: E2E doğrulama, repro/teşhis, test verisi/ortam kurulumu — her birinin AYRI skili ve ayrı yöntemi var. Hangi modda çalışıyorsan **o anda** onun skilini açarsın; mod değişince (E2E→repro) yeniden açarsın. Omurg

> **Skil açmak yavaşlatmaz — açmamak eksik kapsam bırakır.**

### Ölçüm

| | |
|---|---|
| Preload skill | 6 (body hepsini adıyla sayıyor ✅) |
| On-demand skill | 10 |
| Bunlardan body'de adı geçen | **3** (%30) |
| Body'de sayı belirtiliyor mu | **HAYIR** |

**Body'de adı hiç geçmeyen on-demand skiller (7):**

`backend` · `code-auditor` · `code-quality` · `data-access` · `database` · `dev-environment` · `quality`

---

## code-auditor

**Body gövdesi:** 87 satır · **Skill bölümü:** var (`## Skiller`)

### Body skillerin zenginliğini nasıl tarif ediyor

**"Tek başına çalışmıyorsun" paragrafı:**

> Elinde yalnız bu projenin kodu yok: skiller (kanon), referans projeler, modül dokümanları ve emsal desenler var. Denetim ölçütünü **okumadan** sapma ilan etmek yanlış bulgu üretir — bulgun bir sonraki agent'ın işini yönlendirir. Yavaş okumak, yanlış bulguyu geri almaktan ucuzdur.

→ Skiller burada **`skiller (kanon)`** olarak, diğer kaynaklarla aynı sırada anılıyor. Sayı yok, kapsam yok, alan yok.

**`## Skiller` bölümü ne diyor:**

> **Preload (çekirdek + omurga):** `behavior` · `handoff` · `memory-management` · `is-akisi` · `pr-yazilim-oy-envanteri` · `code-auditor` (alet çantası + kimlik).

> **On-demand — iş türü değişince AÇILIR, tur başında bir kez değil.** Denetim tek tür değildir: etki analizi, yapısal audit, kalite ölçütü — her birinin AYRI skili ve ayrı çıktı yapısı var. Ayrıca taradığın katmanın kanonu (`database`/`backend`/`frontend`/`mobile`) o katmanın skilindedir: ölçüt okunm

> **Skil açmak yavaşlatmaz — açmamak yanlış bulgu ürettirir.**

### Ölçüm

| | |
|---|---|
| Preload skill | 6 (body hepsini adıyla sayıyor ✅) |
| On-demand skill | 6 |
| Bunlardan body'de adı geçen | **4** (%67) |
| Body'de sayı belirtiliyor mu | **HAYIR** |

**Body'de adı hiç geçmeyen on-demand skiller (2):**

`impact-analiz` · `project-assistant`

---

## devops-engineer

**Body gövdesi:** 115 satır · **Skill bölümü:** var (`## Skiller`)

### Body skillerin zenginliğini nasıl tarif ediyor

**"Tek başına çalışmıyorsun" paragrafı:**

> Elinde yalnız bu projenin yapılandırması yok: skiller (kanon), referans projelerin Makefile/manifest/pipeline'ları, `system-topology` ve PROJECT-INFO var. Aradığın cevapların çoğu zaten yazılı — sen üretmeden önce **onları okursun**. Hız uğruna atlama: hafızadan yazılan manifest,

→ Skiller burada **`skiller (kanon)`** olarak, diğer kaynaklarla aynı sırada anılıyor. Sayı yok, kapsam yok, alan yok.

**`## Skiller` bölümü ne diyor:**

> **Preload (çekirdek + omurga):** `behavior` · `handoff` · `memory-management` · `is-akisi` · `pr-yazilim-oy-envanteri` · `devops` (alet çantası + kimlik) · `dev-deploy` (CI izleme) · `prod-deploy` (canlıya çıkış zinciri).

> ⚠️ **Yüklü olmak açmış saymaz.** Prod zinciri context'inde dursa bile hangi adımda olduğunu ekrana yazarsın — merge'ün öncesinde misin sonrasında mı, bu ikisi senin için farklı iş.

> **On-demand — dokunma anında AÇILIR, iş başında bir kez değil.** DevOps işi tek alan değildir: CI/CD, container/manifest, secret/env, mobil dağıtım, topoloji, release — her birinin AYRI skili ve ayrı kuralları var. Hangi alana dokunuyorsan **o anda** onun skilini açarsın; alan değişince (pipeline→se

### Ölçüm

| | |
|---|---|
| Preload skill | 8 (body hepsini adıyla sayıyor ✅) |
| On-demand skill | 12 |
| Bunlardan body'de adı geçen | **7** (%58) |
| Body'de sayı belirtiliyor mu | **HAYIR** |

**Body'de adı hiç geçmeyen on-demand skiller (5):**

`code-quality` · `cronjob` · `iap` · `notification` · `quality`

---

## Ne eksik — tek cümlede

Body agent'a **"oku"** diyor ama **"ne kadar var"** demiyor.
Bir kütüphaneye girip *"kitaplar var, okumalısın"* denmesi ile *"77 kitap var, seninkiler şu 21'i"* denmesi arasındaki fark bu.

## Ölçümün sınırı

Bu ölçüm **body metnini** ölçtü: sayı geçiyor mu, skill adı geçiyor mu, zenginlik nasıl anlatılıyor.
**Ölçmediği şey:** bu tarif değişirse agent davranışı değişir mi. O ayrı bir ölçüm.
