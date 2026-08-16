# V8 Özel Yazılım — Yönlendirme Uyum Ölçümü

**Ölçüm:** 2026-08-14 · **Kaynak:** `v8/ozel-yazilim` (plugin 0.7.0)
**Soru:** main skill'in *"ne zaman gidersin"* yönlendirmesi, hedef skill'in kendi `description`'ı ile uyumlu mu?

---

## Sonuç önce

**Uyumsuzluk yok — ama yönlendirme tek yönlü çalışıyor.**

| Ölçüm | Sonuç |
|---|---|
| Main SKILL.md'deki yönlendirme satırı | 233 satır, 154 (main→hedef) çifti |
| Menü biçiminde (`- **tetik** → \`skill\``) | **111 (%72)** — agent tarayarak bulabilir |
| Ok içinde ama menü değil | 23 (%15) |
| Düz metne gömülü | **20 (%13)** — agent ancak okuyarak bulur |
| Tetik kelimesi hedef desc'te hiç geçmeyen | **0** (5 aday çıktı, beşi de çok-hedefli satır artefaktı) |
| Anlamca uyumsuz çift | **0** (düşük örtüşmeli 8 çift elle okundu, hepsi uyumlu) |

Yani **main skill → hedef skill yönü sağlam.** Agent menüye bakarsa doğru skile gidiyor.

### Asıl bulgu: ters yön zayıf

Skill'ler agent'ın context'ine iki yoldan girer: (1) main skill'in menüsünden okuyarak, (2) **kendi `description`'ı tetiklenerek.** İkinci yol için description'ın *"ne zaman"* sorusuna cevap vermesi gerekir.

Main'in yönlendirdiği 58 skill'in description tipi:

| Tip | Sayı | Ne yapar |
|---|---|---|
| **DURUM** ("şu iş geldiğinde açılır") | 29 | Kendi başına tetiklenir |
| **İKİSİ** (hem ne olduğu hem ne zaman) | 27 | Tetiklenir ama gecikmeli |
| **İÇERİK** (yalnız "şu kurallar burada") | 2 | **Kendi başına tetiklenmez** |

Ve "İKİSİ" sınıfının **21'i "ne olduğu" cümlesiyle başlıyor**, "ne zaman" ile değil:

- `api-project` — *"PR Yazılım yeni API servisi ekleme sözleşmesi (.NET, ortak alet skili)."*
- `auth` — *"PR Yazılım ortak kimlik/oturum sözleşmesi (alet skili)."*
- `backend` — *"backend-developer'ın omurga skili, preload edilir."*
- `code-auditor` — *"code-auditor'ın omurga skili, preload edilir."*
- `code-quality` — *"PR Yazılım ortak kod kalitesi sözleşmesi (alet skili)."*
- `component` — *"PR Yazılım frontend component öz skili (Next.js panel / React)."*
- `cronjob` — *"PR Yazılım ortak zamanlı iş sözleşmesi (alet skili)."*
- `database` — *"PR Yazılım veritabanı sözleşmesi (MSSQL + EF Core, ortak alet skili)."*
- `design-handoff` — *"PR Yazılım tasarım→kod devir sözleşmesi (alet skili)."*
- `dev-environment` — *"PR Yazılım ortak lokal geliştirme ortamı sözleşmesi (alet skili)."*
- `devops` — *"devops-engineer'ın omurga skili, preload edilir."*
- `enum-sync` — *"PR Yazılım ortak enum senkron sözleşmesi (alet skili)."*
- `excel-export` — *"PR Yazılım Excel üretim/okuma sözleşmesi (.NET, ortak alet skili)."*
- `figma` — *"PR Yazılım Figma MCP protokolü (alet skili) — çift yön."*
- `frontend` — *"frontend-developer'ın omurga skili, preload edilir."*
- `gosterim-formatlari` — *"PR Yazılım ortak gösterim/serialize sözleşmesi (alet skili)."*
- `iap` — *"PR Yazılım ortak uygulama-içi satın alma sözleşmesi (alet skili)."*
- `mobile` — *"mobile-developer'ın omurga skili, preload edilir."*
- `notification` — *"PR Yazılım ortak haber ulaştırma sözleşmesi (alet skili)."*
- `proje-dosya-duzeni` — *"PR Yazılım proje doküman düzeni kanonu (ortak alet skili)."*
- `project-assistant` — *"project-assistant'ın omurga skili, preload edilir."*
- `quality` — *"qa-engineer'ın omurga skili, preload edilir."*
- `realtime` — *"PR Yazılım ortak canlı bildirim sözleşmesi (alet skili)."*
- `response-request` — *"PR Yazılım ortak iletişim sözleşmesi (alet skili)."*
- `tasarim-prensipleri` — *"PR Yazılım ortak tasarım prensipleri sözleşmesi (alet skili)."*
- `test-engineer` — *"test-engineer'ın omurga skili, preload edilir."*
- `ui-designer` — *"PR Yazılım ui-designer omurga skili (MAIN)."*
- `upload` — *"PR Yazılım ortak dosya yükleme sözleşmesi (alet skili)."*

**Neden önemli:** description'ın ilk cümlesi eşleştirmede en ağır basan yer. *"PR Yazılım ortak kimlik/oturum sözleşmesi (alet skili)"* diye başlayan bir skill, agent *"401 alıyorum"* diye düşündüğünde kendiliğinden tetiklenmez — main skill menüsünü okumak zorundadır.

**Yani bugünkü sistem çalışıyor ama tek bacaklı:** main skill menüsü kalkarsa 21 skill sessizce erişilemez hale gelir.

---

# Skill Listesi

## Main Skill: `project-assistant`  *(agent: project-assistant)*

**Main desc:** project-assistant'ın omurga skili, preload edilir. Bir talep geldiğinde hangi öz skilin açılacağına karar verilirken, PA'nın bir işi üstlenip üstlenmeyeceği sorulduğunda ve rol sınırı belirsizleştiğinde geçerlidir. Yalnı…

### Preloaded skiller

**`behavior`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin ortak davranış çekirdeği (preloaded) — her agentın karakteri, çalışma refleksi, kalite sahipliği, iletişim tarzı, git disiplini. Tüm pipe…
- **Main ne olarak tanımlıyor:** Test: **"Raporumu developer'a versem hâlâ keşif yapmak zorunda mı, yoksa teşhisi ben bitirdim mi?"** Bitirdiysen CA'ya geçmişsin. Sınırı aştığın ölçüt…

**`handoff`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin handoff (iş devri) iletişim kuralları (ortak çekirdek, preloaded) — bir agent başka bir agent'a iş/bilgi iletirken UYACAĞI biçim. Tüm pip…
- **Main ne olarak tanımlıyor:** Ekip üyesi agent'ı (UID/BE/FE/MB/DO/QA/TE/CA) çağırmak yasak — PA "CA'ya git", "TE repro etsin" der (yönlendirme), kendisi çağırmaz. İş bağlamını hazı…

**`memory-management`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin memory yönetim kurallar bütünü (ortak çekirdek, preloaded) — memory'ye NE yazılır, NE yazılmaz, çelişki nasıl işaretlenir, index nasıl ko…
- **Main ne olarak tanımlıyor:** Ortak davranış (karakter, iletişim, git, commit)

**`is-akisi`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin iş akışı iskeleti (ortak çekirdek, preloaded) — kim kimden ne alır, kime ne devreder, iş hangi sırayla ilerler. Tüm pipeline agent (PA, U…
- **Main ne olarak tanımlıyor:** - ⚠️ **ClickUp'a dokunmadan ÖNCE `clickup` skilini AÇ — istisnasız.** Task okumak ≠ comment okumak: gereksinim comment'te durabilir. Saha kanıtı: skil…

**`pr-yazilim-oy-envanteri`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım (OY) sistem, ekip ve iş üretme bilinci (üst skil, tüm OY agentları preload). Üç bölüm: TEKNOLOJİ VE İŞLEYİŞ (biz neyle çalışırız — altyapı, yığın,…
- **Main ne olarak tanımlıyor:** Ortak davranış (karakter, iletişim, git, commit)

**`dev-deploy`** 

- **Desc ne diyor:** Bir değişiklik dev ortamına alınırken açılır: developer commit'ini QA'ya devrederken, QA denetimden geçirip `main`'e push ederken, push öncesi kapsam ve branch koruması k…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`prod-deploy`** 

- **Desc ne diyor:** Bir iş canlıya (production) çıkarılırken açılır: kullanıcı 'canlıya alalım / production'a geçeceğiz / prod'a çıkalım' dediğinde, prod PR'ı açılırken, canlıya çıkış tarama…
- **Main ne olarak tanımlıyor:** Prod'a çıkış git akışı (branch→ortam, PR, merge)

### On-demand skiller

**`bug-triyaj`** — desc tipi: **DURUM**

- **Desc ne diyor:** Bir hata, şikayet ya da 'şu çalışmıyor' bildirimi geldiğinde açılır: şikayet işlevsel parçalara ayrılırken, bir parçanın kod hatası mı işlev-testi/veri sorunu mu olduğu s…
- **Main ne olarak tanımlıyor:** Hata / şikayet / bug triyajı
- **Uyum:** ✅ uyumlu

**`clickup`** — desc tipi: **DURUM**

- **Desc ne diyor:** ClickUp'a dokunulacak her anda açılır: bir task ya da sub task'ın statüsü değiştirilirken, task açılırken, comment yazılırken, sprint/backlog durumu taranırken, müşteri t…
- **Main ne olarak tanımlıyor:** Task açma / statü / backlog
- **Uyum:** ✅ uyumlu

**`danisma`** — desc tipi: **DURUM**

- **Desc ne diyor:** Kullanıcı bir soru, fikir ya da 'nasıl yapsak' getirdiğinde açılır: bir yaklaşım tartışılırken, seçenekler karşılaştırılırken, 'ne düşünüyorsun / fikrin ne' denildiğinde …
- **Main ne olarak tanımlıyor:** Soru / fikir / "nasıl yapsak" / ARGE
- **Uyum:** ✅ uyumlu

**`discovery`** — desc tipi: **DURUM**

- **Desc ne diyor:** Yeni bir modül, feature ya da ekran talebi geldiğinde açılır: gereksinim netleştirilirken, discovery.md yazılırken, ekran ve aksiyon listesi çıkarılırken, hangi katmanlar…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* PA'nın alet çantası ve kendine özgü kimlik kanonu. "Nasıl discovery yazılır"ı ANLATMAZ (o `discovery`) — hangi işte hangi aletin açılacağını…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`figma`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım Figma MCP protokolü (alet skili) — çift yön. Figma'dan tasarım okuma (design→code: metadata→token→context sırası, element eşleştirme tablosu, token bütçesi) ve…
- **Main ne olarak tanımlıyor:** Figma'dan tasarım okuma
- **Uyum:** ✅ uyumlu

**`impact-analiz`** — desc tipi: **DURUM**

- **Desc ne diyor:** Mevcut yapıya dokunan ya da yayındaki bir projeye giren bir iş geldiğinde açılır: 'bu nereleri etkiler / ne kırılır' sorusu doğduğunda, CA'dan etki analizi istenirken, de…
- **Main ne olarak tanımlıyor:** Mevcut yapıya dokunan iş / CA etki analizi koordinasyonu
- **Uyum:** ✅ uyumlu

**`orkestrasyon`** — desc tipi: **DURUM**

- **Desc ne diyor:** Bir modül kapatılırken, session kapanışında kimin işi askıda kaldığı çıkarılırken, QA bir discovery sapması bildirdiğinde ve iş canlıya (prod) çıkarılırken açılır. 'Modül…
- **Main ne olarak tanımlıyor:** Kapanış session takibi / sapma değerlendirme / prod release
- **Uyum:** ✅ uyumlu

**`proje-dosya-duzeni`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım proje doküman düzeni kanonu (ortak alet skili). Bir OY projesinin docs/ altındaki dosya düzeni burada tek kaynak olarak tanımlıdır: _project/ iki zorunlu dosya…
- **Main ne olarak tanımlıyor:** Dosya düzeni kanonu (klasör/task-folder/MODUL-BILGI/nereye ne konur)
- **Uyum:** ✅ uyumlu

**`proje-islemleri`** — desc tipi: **IKISI**

- **Desc ne diyor:** Bir projeye ilk kez girilirken açılır: proje devralınırken, 'bu projeyi devralıyoruz / düzeni elden geçirelim' denildiğinde ve docs düzeni kurulurken ya da eski/karışık b…
- **Main ne olarak tanımlıyor:** Projeye ilk temas / devralma / docs düzeni kurma-elden geçirme
- **Uyum:** ✅ uyumlu

**`project-planning`** — desc tipi: **DURUM**

- **Desc ne diyor:** Sıfırdan yeni bir proje kurulurken açılır: müşteri kapsamı platformlara (admin/mobil/web/API) bölünürken, modül kırılımı çıkarılırken, eksik ön-doküman doğru sorularla aç…
- **Main ne olarak tanımlıyor:** Sıfırdan yeni proje / büyük resim / platform kırılımı
- **Uyum:** ✅ uyumlu

---

## Main Skill: `ui-designer`  *(agent: ui-designer)*

**Main desc:** PR Yazılım ui-designer omurga skili (MAIN). UID'in alet çantası: girdi kaynağını tanıyıp doğru moda/skile geçme haritası + UID'e özgün iş kuralları (almak değil çevirmek, iteratif kullanıcı süreci, FE'ye kayıpsız devir, …

### Preloaded skiller

**`behavior`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin ortak davranış çekirdeği (preloaded) — her agentın karakteri, çalışma refleksi, kalite sahipliği, iletişim tarzı, git disiplini. Tüm pipe…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`handoff`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin handoff (iş devri) iletişim kuralları (ortak çekirdek, preloaded) — bir agent başka bir agent'a iş/bilgi iletirken UYACAĞI biçim. Tüm pip…
- **Main ne olarak tanımlıyor:** **Kendi olayını kendin yazarsın → `handoff` `HANDOFF-STATUS-OWN-EVENTS`** (tek kaynak, 9 agent ortak).

**`memory-management`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin memory yönetim kurallar bütünü (ortak çekirdek, preloaded) — memory'ye NE yazılır, NE yazılmaz, çelişki nasıl işaretlenir, index nasıl ko…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`is-akisi`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin iş akışı iskeleti (ortak çekirdek, preloaded) — kim kimden ne alır, kime ne devreder, iş hangi sırayla ilerler. Tüm pipeline agent (PA, U…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`pr-yazilim-oy-envanteri`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım (OY) sistem, ekip ve iş üretme bilinci (üst skil, tüm OY agentları preload). Üç bölüm: TEKNOLOJİ VE İŞLEYİŞ (biz neyle çalışırız — altyapı, yığın,…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

### On-demand skiller

**`code-quality`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak kod kalitesi sözleşmesi (alet skili). Dosya/metot boyut eşiği, tekrar→helper, god-object yasağı, tek-sorumluluk, yorum disiplini, magic string/number yas…
- **Main ne olarak tanımlıyor:** Kod kalite eşiği
- **Uyum:** ✅ uyumlu

**`component`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım frontend component öz skili (Next.js panel / React). Ortak component katalog + reuse-first (native HTML yerine proje component), naming/export/boyut disiplini,…
- **Main ne olarak tanımlıyor:** Component yazım kanonu (reuse-first, PascalCase)
- **Uyum:** ✅ uyumlu

**`database`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım veritabanı sözleşmesi (MSSQL + EF Core, ortak alet skili). EntityBase 6 alan, canonical veri tipleri, property ordering, isimlendirme, NVARCHAR uzunlukları, by…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* - `DH-ENTITYBASE` — Her mock entity EntityBase 6 alanını taşır (kanon: `database`).
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`design-handoff`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım tasarım→kod devir sözleşmesi (alet skili). Mock data formatı (EntityBase 6 alan, casing, byte enum, epoch tarih, response wrapper) ve design token mimarisi (ka…
- **Main ne olarak tanımlıyor:** Mock format / token mimarisi / mock→gerçek devir
- **Uyum:** ✅ uyumlu

**`design-system`** — desc tipi: **IKISI**

- **Desc ne diyor:** Tasarımı komple değiştirelim / yeni bir görsel dil kuralım / temayı yenile / bu component'i tasarla' denildiğinde açılır: token seti üretilirken ya da revize edilirken (r…
- **Main ne olarak tanımlıyor:** Tasarım sistemini kur/değiştir (token/component/tema, "tasarımı komple değiştir")
- **Uyum:** ✅ uyumlu

**`enum-sync`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak enum senkron sözleşmesi (alet skili). Enum kaynağı (library-datatype), byte tipi, 1-tabanlı değer ve BE→client senkron kuralı burada tek kaynak olarak ta…
- **Main ne olarak tanımlıyor:** Enum görünen etiket (değer BE-özel)
- **Uyum:** ✅ uyumlu

**`figma`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım Figma MCP protokolü (alet skili) — çift yön. Figma'dan tasarım okuma (design→code: metadata→token→context sırası, element eşleştirme tablosu, token bütçesi) ve…
- **Main ne olarak tanımlıyor:** Figma tasarımı okuma (MCP protokol)
- **Uyum:** ✅ uyumlu

**`prototype-page`** — desc tipi: **DURUM**

- **Desc ne diyor:** Şu ekranı tasarla / sıfırdan bir mock çıkar / prototip sayfa yap / bir ekran denemesi görelim' denildiğinde açılır: sayfa iskeleti kurulurken, tablo kolonlarının ve form …
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* UI-designer'ın alet çantası ve kendine özgü iş kanonu. UID = çeviri/aktarım agent'ı: dış bir görsel/yapı kaynağını PR Yazılım kanonuna çevir…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`reference-to-code`** — desc tipi: **IKISI**

- **Desc ne diyor:** Bu sayfa gibi yap / şu siteyi aktar / bu projenin ekranını çevir / şu kodu incele' denildiğinde açılır: dış bir kaynak (başka projenin kodu ya da canlı bir web sayfası) P…
- **Main ne olarak tanımlıyor:** Referans proje kodu / canlı sayfa çevirme (Playwright ekstraksiyon)
- **Uyum:** ✅ uyumlu

**`response-request`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak iletişim sözleşmesi (alet skili). API istek/yanıt zarfı {succeeded, message, data}, liste zarfı {Data, TotalCount} ve pagination (Page + Take, 1-tabanlı)…
- **Main ne olarak tanımlıyor:** Alan adı casing (PascalCase) / response zarfı
- **Uyum:** ⚠️ kelime örtüşmesi düşük (elle okundu: anlamca uyumlu)

**`screen-structure`** — desc tipi: **DURUM**

- **Desc ne diyor:** PR Yazılım web ekran yapısı ortak aleti (Next.js panel). Bir ekranın dosya/sorumluluk iskeleti: route dosyası ince kabuk → sayfa component'i (components/Pages/{Domain}/) …
- **Main ne olarak tanımlıyor:** Ekran iskeleti / route kabuk / sayfa yerleşimi
- **Uyum:** ✅ uyumlu

**`tasarim-prensipleri`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak tasarım prensipleri sözleşmesi (alet skili). Dil-nötr mühendislik tuzakları ve karar prensipleri burada tek kaynak olarak tanımlıdır: hata izolasyonu, se…
- **Main ne olarak tanımlıyor:** tasarım tuzakları
- **Uyum:** ✅ uyumlu

---

## Main Skill: `backend`  *(agent: backend-developer)*

**Main desc:** backend-developer'ın omurga skili, preload edilir. Bir backend işi geldiğinde hangi aletin açılacağına karar verilirken, commit öncesi doğrulamanın ne olduğu sorulduğunda ve rol sınırı belirsizleştiğinde geçerlidir. qa-e…

### Preloaded skiller

**`behavior`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin ortak davranış çekirdeği (preloaded) — her agentın karakteri, çalışma refleksi, kalite sahipliği, iletişim tarzı, git disiplini. Tüm pipe…
- **Main ne olarak tanımlıyor:** Commit öncesi telepresence intercept ile lokal servise curl atılır, kodun gerçekten çalıştığı görülür (deploy→canlıda-test→bozuk döngüsünü kırmak için…

**`handoff`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin handoff (iş devri) iletişim kuralları (ortak çekirdek, preloaded) — bir agent başka bir agent'a iş/bilgi iletirken UYACAĞI biçim. Tüm pip…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`memory-management`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin memory yönetim kurallar bütünü (ortak çekirdek, preloaded) — memory'ye NE yazılır, NE yazılmaz, çelişki nasıl işaretlenir, index nasıl ko…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`is-akisi`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin iş akışı iskeleti (ortak çekirdek, preloaded) — kim kimden ne alır, kime ne devreder, iş hangi sırayla ilerler. Tüm pipeline agent (PA, U…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`pr-yazilim-oy-envanteri`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım (OY) sistem, ekip ve iş üretme bilinci (üst skil, tüm OY agentları preload). Üç bölüm: TEKNOLOJİ VE İŞLEYİŞ (biz neyle çalışırız — altyapı, yığın,…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

### On-demand skiller

**`acs-gorusme`** — desc tipi: **DURUM**

- **Desc ne diyor:** Sesli ya da görüntülü görüşme işi kurulurken açılır: canlı görüşme odası açılırken, katılımcı token'ı üretilirken, görüşme kaydı başlatılırken ve 'canlı ders / video görü…
- **Main ne olarak tanımlıyor:** Sesli/görüntülü görüşme, oda, kayıt (ServerCallId tuzağı)
- **Uyum:** ✅ uyumlu

**`api-project`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım yeni API servisi ekleme sözleşmesi (.NET, ortak alet skili). Mevcut solution'a yeni bir 'api-{domain}' servisi eklenirken bu skil açılır: dotnet-template'teki …
- **Main ne olarak tanımlıyor:** Yeni API servisi ekleme
- **Uyum:** ✅ uyumlu

**`auth`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak kimlik/oturum sözleşmesi (alet skili). GUID session (Redis, JWT değil), token header, prefix→rol eşlemesi ve 401 tanıma burada tek kaynak olarak tanımlıd…
- **Main ne olarak tanımlıyor:** Kimlik / session / token / `CheckAccess`
- **Uyum:** ✅ uyumlu

**`code-quality`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak kod kalitesi sözleşmesi (alet skili). Dosya/metot boyut eşiği, tekrar→helper, god-object yasağı, tek-sorumluluk, yorum disiplini, magic string/number yas…
- **Main ne olarak tanımlıyor:** Kod yazarken boyut/isim/DRY/null-guard sınırı
- **Uyum:** ✅ uyumlu

**`cronjob`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak zamanlı iş sözleşmesi (alet skili). K8s CronJob mekanizması (tek Main() console app), BE'nin iş mantığı yazması ve DO'nun schedule deploy etmesi burada t…
- **Main ne olarak tanımlıyor:** Zamanlı iş (job-cron mantığı)
- **Uyum:** ✅ uyumlu

**`database`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım veritabanı sözleşmesi (MSSQL + EF Core, ortak alet skili). EntityBase 6 alan, canonical veri tipleri, property ordering, isimlendirme, NVARCHAR uzunlukları, by…
- **Main ne olarak tanımlıyor:** Tablo / entity / şema / migration / EntityBase
- **Uyum:** ✅ uyumlu

**`dev-environment`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak lokal geliştirme ortamı sözleşmesi (alet skili). Makefile hedefleri, Telepresence intercept (x-dev-user) ve lokal doğrulama akışı burada tek kaynak olara…
- **Main ne olarak tanımlıyor:** Lokal doğrulama (`make dev TARGET=api-X`, telepresence intercept)
- **Uyum:** ✅ uyumlu

**`enum-sync`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak enum senkron sözleşmesi (alet skili). Enum kaynağı (library-datatype), byte tipi, 1-tabanlı değer ve BE→client senkron kuralı burada tek kaynak olarak ta…
- **Main ne olarak tanımlıyor:** Enum kaynağı / byte / senkron
- **Uyum:** ✅ uyumlu

**`excel-export`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım Excel üretim/okuma sözleşmesi (.NET, ortak alet skili). NPOI (Apache-2.0) ile Excel export/import: merkezi ExcelOperationDataLayer + IExcelFile marker + kolon …
- **Main ne olarak tanımlıyor:** Excel içe/dışa aktarma
- **Uyum:** ⚠️ kelime örtüşmesi düşük (elle okundu: anlamca uyumlu)

**`gosterim-formatlari`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak gösterim/serialize sözleşmesi (alet skili). Telefon (pure ↔ +90), tarih-saat (UTC epoch-ms ↔ GMT3 gösterim) ve tutar biçimleri burada tek kaynak olarak t…
- **Main ne olarak tanımlıyor:** Tarih (epoch/`ToJSTime`) / tutar / telefon üretimi
- **Uyum:** ✅ uyumlu

**`iap`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak uygulama-içi satın alma sözleşmesi (alet skili). RevenueCat 3-katman (MB SDK satın alır, BE API sorgulayarak doğrular, DO store ürün tanımlar) burada tek…
- **Main ne olarak tanımlıyor:** Uygulama-içi satın alma doğrulama (RevenueCat pull)
- **Uyum:** ✅ uyumlu

**`local-payment`** — desc tipi: **ICERIK**

- **Desc ne diyor:** PR Yazılım ortak yerel ödeme sözleşmesi (alet skili). Yerel ödeme sağlayıcısı (Paytr/Stripe/havale gibi harici sağlayıcı) üzerinden kredi kartı/abonelik/havale ödeme akış…
- **Main ne olarak tanımlıyor:** Yerel ödeme (Paytr)
- **Uyum:** ✅ uyumlu

**`messaging`** — desc tipi: **DURUM**

- **Desc ne diyor:** Bir sohbet ya da mesajlaşma modülü kurulurken açılır: mesajın nasıl saklanacağına karar verilirken, sohbet listelenip sayfalanırken ve mesajın karşı tarafa anlık iletilme…
- **Main ne olarak tanımlıyor:** Uygulama-içi sohbet / mesajlaşma (blob + jsonl)
- **Uyum:** ✅ uyumlu

**`module-development`** — desc tipi: **IKISI**

- **Desc ne diyor:** Bir endpoint ya da modül baştan sona yazılacağında açılır: handler kurulurken, veri katmanına dokunulurken, yetki bildirimi ve doğrulama eklenirken, önbellek kullanılırke…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* Backend-developer'ın alet çantası ve kendine özgü iş kanonu. Bu skil "nasıl handler yazılır"ı ANLATMAZ (o `module-development`) — hangi işte…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`notification`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak haber ulaştırma sözleşmesi (alet skili). Push (Expo) + mail + SMS + in-app kanalları, RabbitMQ kuyruk + job-consumer üretimi ve kanal altyapısı burada te…
- **Main ne olarak tanımlıyor:** Mail / SMS / push üretimi (kuyruk + consumer)
- **Uyum:** ✅ uyumlu

**`pryazilim-core`** — desc tipi: **DURUM**

- **Desc ne diyor:** Yardımcı bir kod yazılmadan ÖNCE açılır: OTP ya da rastgele değer üretilirken, toplu iş parçalara bölünürken, önbellek sayacı veya kuyruk retry'ı kurulurken, güvenli pars…
- **Main ne olarak tanımlıyor:** Hazır core yardımcı (CheckVal/DataGenerator/CacheManager...)
- **Uyum:** ✅ uyumlu

**`realtime`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak canlı bildirim sözleşmesi (alet skili). api-websocket (Node/socket.io, ayrı runtime), BE'nin event'i HTTP ile bildirmesi ve client'ın socket dinlemesi bu…
- **Main ne olarak tanımlıyor:** Canlı bildirim (websocket event POST)
- **Uyum:** ✅ uyumlu

**`response-request`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak iletişim sözleşmesi (alet skili). API istek/yanıt zarfı {succeeded, message, data}, liste zarfı {Data, TotalCount} ve pagination (Page + Take, 1-tabanlı)…
- **Main ne olarak tanımlıyor:** Yanıt zarfı / pagination `Page`+`Take` / hata formatı
- **Uyum:** ✅ uyumlu

**`search`** — desc tipi: **DURUM**

- **Desc ne diyor:** Bir projeye tam-metin ya da facet arama eklenirken açılır: arama index'i kurulurken ya da yeniden kurulurken, doküman senkronu yazılırken, öneri/autocomplete eklenirken v…
- **Main ne olarak tanımlıyor:** Arama altyapısı
- **Uyum:** ✅ uyumlu

**`tasarim-prensipleri`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak tasarım prensipleri sözleşmesi (alet skili). Dil-nötr mühendislik tuzakları ve karar prensipleri burada tek kaynak olarak tanımlıdır: hata izolasyonu, se…
- **Main ne olarak tanımlıyor:** kod tasarlarken tuzak/karar (hata izolasyonu, idempotency, sözleşme bütünlüğü)
- **Uyum:** ✅ uyumlu

**`upload`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak dosya yükleme sözleşmesi (alet skili). FormData multipart istek, BE FormFile→Azure blob depolama ve URL dönüşü burada tek kaynak olarak tanımlıdır. Üç uç…
- **Main ne olarak tanımlıyor:** Dosya/görsel yükleme (FormFile → Azure blob)
- **Uyum:** ✅ uyumlu

---

## Main Skill: `frontend`  *(agent: frontend-developer)*

**Main desc:** frontend-developer'ın omurga skili, preload edilir. Bir panel işi geldiğinde hangi aletin açılacağına karar verilirken, commit öncesi doğrulamanın ne olduğu sorulduğunda ve rol sınırı belirsizleştiğinde geçerlidir. qa-en…

### Preloaded skiller

**`behavior`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin ortak davranış çekirdeği (preloaded) — her agentın karakteri, çalışma refleksi, kalite sahipliği, iletişim tarzı, git disiplini. Tüm pipe…
- **Main ne olarak tanımlıyor:** FE ucu. Genel kanon çekirdekte (`behavior` `BEHAVIOR-VERIFY-BEFORE-COMMIT`) — burada tekrarlanmaz. FE'ye özgü mekanik: doğrulama telepresence/Playwrig…

**`handoff`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin handoff (iş devri) iletişim kuralları (ortak çekirdek, preloaded) — bir agent başka bir agent'a iş/bilgi iletirken UYACAĞI biçim. Tüm pip…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`memory-management`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin memory yönetim kurallar bütünü (ortak çekirdek, preloaded) — memory'ye NE yazılır, NE yazılmaz, çelişki nasıl işaretlenir, index nasıl ko…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`is-akisi`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin iş akışı iskeleti (ortak çekirdek, preloaded) — kim kimden ne alır, kime ne devreder, iş hangi sırayla ilerler. Tüm pipeline agent (PA, U…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`pr-yazilim-oy-envanteri`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım (OY) sistem, ekip ve iş üretme bilinci (üst skil, tüm OY agentları preload). Üç bölüm: TEKNOLOJİ VE İŞLEYİŞ (biz neyle çalışırız — altyapı, yığın,…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

### On-demand skiller

**`auth`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak kimlik/oturum sözleşmesi (alet skili). GUID session (Redis, JWT değil), token header, prefix→rol eşlemesi ve 401 tanıma burada tek kaynak olarak tanımlıd…
- **Main ne olarak tanımlıyor:** Token gönderimi / 401 / logout
- **Uyum:** ⚠️ kelime örtüşmesi düşük (elle okundu: anlamca uyumlu)

**`code-quality`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak kod kalitesi sözleşmesi (alet skili). Dosya/metot boyut eşiği, tekrar→helper, god-object yasağı, tek-sorumluluk, yorum disiplini, magic string/number yas…
- **Main ne olarak tanımlıyor:** Kod kalite eşiği
- **Uyum:** ✅ uyumlu

**`component`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım frontend component öz skili (Next.js panel / React). Ortak component katalog + reuse-first (native HTML yerine proje component), naming/export/boyut disiplini,…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* Frontend-developer'ın alet çantası ve kendine özgü iş kanonu. "Nasıl component yazılır"ı ANLATMAZ (o `component`) — hangi işte hangi aletin …
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`data-access`** — desc tipi: **DURUM**

- **Desc ne diyor:** Panelde API'ye bağlanılacakken açılır: veri çeken ya da yazan bir hook yazılırken, query key belirlenirken, bir mutasyondan sonra hangi verinin tazeleneceğine karar veril…
- **Main ne olarak tanımlıyor:** Veri çekme/yazma (useQuery/useMutate/QUERY_KEYS/ApiService)
- **Uyum:** ✅ uyumlu

**`database`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım veritabanı sözleşmesi (MSSQL + EF Core, ortak alet skili). EntityBase 6 alan, canonical veri tipleri, property ordering, isimlendirme, NVARCHAR uzunlukları, by…
- **Main ne olarak tanımlıyor:** Response modeli alan adı / byte enum / tarih tüketimi
- **Uyum:** ✅ uyumlu

**`design-handoff`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım tasarım→kod devir sözleşmesi (alet skili). Mock data formatı (EntityBase 6 alan, casing, byte enum, epoch tarih, response wrapper) ve design token mimarisi (ka…
- **Main ne olarak tanımlıyor:** Mock→gerçek API geçişi / token kullanımı
- **Uyum:** ✅ uyumlu

**`dev-environment`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak lokal geliştirme ortamı sözleşmesi (alet skili). Makefile hedefleri, Telepresence intercept (x-dev-user) ve lokal doğrulama akışı burada tek kaynak olara…
- **Main ne olarak tanımlıyor:** Lokal doğrulama (panel lokal + dev domain; intercept API ucunda, x-dev-user)
- **Uyum:** ✅ uyumlu

**`enum-sync`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak enum senkron sözleşmesi (alet skili). Enum kaynağı (library-datatype), byte tipi, 1-tabanlı değer ve BE→client senkron kuralı burada tek kaynak olarak ta…
- **Main ne olarak tanımlıyor:** Byte enum tüketimi / senkron
- **Uyum:** ✅ uyumlu

**`excel-export`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım Excel üretim/okuma sözleşmesi (.NET, ortak alet skili). NPOI (Apache-2.0) ile Excel export/import: merkezi ExcelOperationDataLayer + IExcelFile marker + kolon …
- **Main ne olarak tanımlıyor:** Excel indirme sunumu
- **Uyum:** ✅ uyumlu

**`figma`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım Figma MCP protokolü (alet skili) — çift yön. Figma'dan tasarım okuma (design→code: metadata→token→context sırası, element eşleştirme tablosu, token bütçesi) ve…
- **Main ne olarak tanımlıyor:** Figma'dan kod üretme
- **Uyum:** ✅ uyumlu

**`form`** — desc tipi: **DURUM**

- **Desc ne diyor:** Panelde bir form yazılacakken açılır: kayıt ekleme ya da düzenleme ekranı kurulurken, alan doğrulaması yazılırken, formun modalda mı ayrı sayfada mı duracağına karar veri…
- **Main ne olarak tanımlıyor:** Form / validasyon / input
- **Uyum:** ✅ uyumlu

**`gosterim-formatlari`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak gösterim/serialize sözleşmesi (alet skili). Telefon (pure ↔ +90), tarih-saat (UTC epoch-ms ↔ GMT3 gösterim) ve tutar biçimleri burada tek kaynak olarak t…
- **Main ne olarak tanımlıyor:** Tarih (epoch→GMT3) / tutar / telefon gösterimi
- **Uyum:** ✅ uyumlu

**`list`** — desc tipi: **IKISI**

- **Desc ne diyor:** Panelde bir liste ya da tablo ekranı yazılacakken açılır: kolonlar tanımlanırken, sayfalama bağlanırken, filtre ve sıralama eklenirken, bir kayıt silinip tablonun tazelen…
- **Main ne olarak tanımlıyor:** Tablo / liste / pagination tüketimi / filtre
- **Uyum:** ✅ uyumlu

**`realtime`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak canlı bildirim sözleşmesi (alet skili). api-websocket (Node/socket.io, ayrı runtime), BE'nin event'i HTTP ile bildirmesi ve client'ın socket dinlemesi bu…
- **Main ne olarak tanımlıyor:** Realtime (SocketContext dinleme)
- **Uyum:** ⚠️ kelime örtüşmesi düşük (elle okundu: anlamca uyumlu)

**`response-request`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak iletişim sözleşmesi (alet skili). API istek/yanıt zarfı {succeeded, message, data}, liste zarfı {Data, TotalCount} ve pagination (Page + Take, 1-tabanlı)…
- **Main ne olarak tanımlıyor:** Yanıt zarfı unwrap / pagination sözleşmesi
- **Uyum:** ✅ uyumlu

**`screen-structure`** — desc tipi: **DURUM**

- **Desc ne diyor:** PR Yazılım web ekran yapısı ortak aleti (Next.js panel). Bir ekranın dosya/sorumluluk iskeleti: route dosyası ince kabuk → sayfa component'i (components/Pages/{Domain}/) …
- **Main ne olarak tanımlıyor:** Ekran iskeleti / route ince kabuk / domain klasörleme
- **Uyum:** ✅ uyumlu

**`style`** — desc tipi: **DURUM**

- **Desc ne diyor:** Panelde görsel bir şey yazılacakken açılır: bir ekrana ya da component'e stil verilirken, renk/tipografi/spacing seçilirken, duruma göre değişen sınıflar birleştirilirken…
- **Main ne olarak tanımlıyor:** Stil / Tailwind / token kullanımı
- **Uyum:** ✅ uyumlu

**`tasarim-prensipleri`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak tasarım prensipleri sözleşmesi (alet skili). Dil-nötr mühendislik tuzakları ve karar prensipleri burada tek kaynak olarak tanımlıdır: hata izolasyonu, se…
- **Main ne olarak tanımlıyor:** tasarım tuzakları
- **Uyum:** ✅ uyumlu

**`upload`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak dosya yükleme sözleşmesi (alet skili). FormData multipart istek, BE FormFile→Azure blob depolama ve URL dönüşü burada tek kaynak olarak tanımlıdır. Üç uç…
- **Main ne olarak tanımlıyor:** Dosya/görsel yükleme (FormData)
- **Uyum:** ✅ uyumlu

---

## Main Skill: `mobile`  *(agent: mobile-developer)*

**Main desc:** mobile-developer'ın omurga skili, preload edilir. Bir mobil işi geldiğinde hangi aletin açılacağına karar verilirken, iOS ile Android arasında ayrı koşum gerekip gerekmediği sorulduğunda ve rol sınırı belirsizleştiğinde …

### Preloaded skiller

**`behavior`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin ortak davranış çekirdeği (preloaded) — her agentın karakteri, çalışma refleksi, kalite sahipliği, iletişim tarzı, git disiplini. Tüm pipe…
- **Main ne olarak tanımlıyor:** MB ucu. Genel kanon çekirdekte (`behavior` `BEHAVIOR-VERIFY-BEFORE-COMMIT`) — burada tekrarlanmaz. MB'ye özgü mekanik: doğrulama Maestro/gerçek cihazl…

**`handoff`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin handoff (iş devri) iletişim kuralları (ortak çekirdek, preloaded) — bir agent başka bir agent'a iş/bilgi iletirken UYACAĞI biçim. Tüm pip…
- **Main ne olarak tanımlıyor:** **Kendi olayını kendin yazarsın → `handoff` `HANDOFF-STATUS-OWN-EVENTS`** (tek kaynak, 9 agent ortak).

**`memory-management`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin memory yönetim kurallar bütünü (ortak çekirdek, preloaded) — memory'ye NE yazılır, NE yazılmaz, çelişki nasıl işaretlenir, index nasıl ko…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`is-akisi`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin iş akışı iskeleti (ortak çekirdek, preloaded) — kim kimden ne alır, kime ne devreder, iş hangi sırayla ilerler. Tüm pipeline agent (PA, U…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`pr-yazilim-oy-envanteri`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım (OY) sistem, ekip ve iş üretme bilinci (üst skil, tüm OY agentları preload). Üç bölüm: TEKNOLOJİ VE İŞLEYİŞ (biz neyle çalışırız — altyapı, yığın,…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

### On-demand skiller

**`auth`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak kimlik/oturum sözleşmesi (alet skili). GUID session (Redis, JWT değil), token header, prefix→rol eşlemesi ve 401 tanıma burada tek kaynak olarak tanımlıd…
- **Main ne olarak tanımlıyor:** Token gönderimi / 401 / saklama (SecureStore)
- **Uyum:** ⚠️ kelime örtüşmesi düşük (elle okundu: anlamca uyumlu)

**`code-quality`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak kod kalitesi sözleşmesi (alet skili). Dosya/metot boyut eşiği, tekrar→helper, god-object yasağı, tek-sorumluluk, yorum disiplini, magic string/number yas…
- **Main ne olarak tanımlıyor:** Kod kalite eşiği
- **Uyum:** ✅ uyumlu

**`data-access-mobile`** — desc tipi: **DURUM**

- **Desc ne diyor:** Mobil tarafta API'ye bağlanılacakken açılır: veri çeken ya da yazan bir hook yazılırken, servis katmanına dokunulurken, query key belirlenirken ve bir mutasyondan sonra h…
- **Main ne olarak tanımlıyor:** Veri çekme (useResponse/useRequest/servis/query key)
- **Uyum:** ✅ uyumlu

**`design-handoff`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım tasarım→kod devir sözleşmesi (alet skili). Mock data formatı (EntityBase 6 alan, casing, byte enum, epoch tarih, response wrapper) ve design token mimarisi (ka…
- **Main ne olarak tanımlıyor:** — *(yönlendirme bulunamadı)*
- **Uyum:** ⚠️ yönlendirmesiz

**`dev-environment`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak lokal geliştirme ortamı sözleşmesi (alet skili). Makefile hedefleri, Telepresence intercept (x-dev-user) ve lokal doğrulama akışı burada tek kaynak olara…
- **Main ne olarak tanımlıyor:** Lokal doğrulama (uygulama lokal + dev domain; intercept API ucunda, x-dev-user)
- **Uyum:** ✅ uyumlu

**`enum-sync`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak enum senkron sözleşmesi (alet skili). Enum kaynağı (library-datatype), byte tipi, 1-tabanlı değer ve BE→client senkron kuralı burada tek kaynak olarak ta…
- **Main ne olarak tanımlıyor:** Byte enum tüketimi / senkron
- **Uyum:** ✅ uyumlu

**`gosterim-formatlari`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak gösterim/serialize sözleşmesi (alet skili). Telefon (pure ↔ +90), tarih-saat (UTC epoch-ms ↔ GMT3 gösterim) ve tutar biçimleri burada tek kaynak olarak t…
- **Main ne olarak tanımlıyor:** Tarih (epoch→GMT3) / tutar / telefon
- **Uyum:** ✅ uyumlu

**`iap`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak uygulama-içi satın alma sözleşmesi (alet skili). RevenueCat 3-katman (MB SDK satın alır, BE API sorgulayarak doğrular, DO store ürün tanımlar) burada tek…
- **Main ne olarak tanımlıyor:** Uygulama-içi satın alma (RevenueCat SDK)
- **Uyum:** ✅ uyumlu

**`local-payment`** — desc tipi: **ICERIK**

- **Desc ne diyor:** PR Yazılım ortak yerel ödeme sözleşmesi (alet skili). Yerel ödeme sağlayıcısı (Paytr/Stripe/havale gibi harici sağlayıcı) üzerinden kredi kartı/abonelik/havale ödeme akış…
- **Main ne olarak tanımlıyor:** Yerel ödeme
- **Uyum:** ✅ uyumlu

**`mobile-release`** — desc tipi: **DURUM**

- **Desc ne diyor:** Mobil uygulama store'a çıkarılacağında açılır: EAS build ya da submit koşulurken, TestFlight veya Play Internal'a gönderilirken, release tetikleyicisi kurulurken, eas.jso…
- **Main ne olarak tanımlıyor:** Release/EAS/store
- **Uyum:** ✅ uyumlu

**`navigation-mobile`** — desc tipi: **IKISI**

- **Desc ne diyor:** Mobil uygulamada ekranlar arası geçişe dokunulacakken açılır: yeni bir route eklenirken, stack ya da tab yerleşimi kurulurken, giriş yapmamış kullanıcının yönlendirilmesi…
- **Main ne olarak tanımlıyor:** Navigasyon (Expo Router, route grup, deep-link)
- **Uyum:** ✅ uyumlu

**`notification`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak haber ulaştırma sözleşmesi (alet skili). Push (Expo) + mail + SMS + in-app kanalları, RabbitMQ kuyruk + job-consumer üretimi ve kanal altyapısı burada te…
- **Main ne olarak tanımlıyor:** Push bildirim tüketme (Expo token, deep-link)
- **Uyum:** ✅ uyumlu

**`realtime`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak canlı bildirim sözleşmesi (alet skili). api-websocket (Node/socket.io, ayrı runtime), BE'nin event'i HTTP ile bildirmesi ve client'ın socket dinlemesi bu…
- **Main ne olarak tanımlıyor:** Realtime (SocketContext dinleme)
- **Uyum:** ⚠️ kelime örtüşmesi düşük (elle okundu: anlamca uyumlu)

**`response-request`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak iletişim sözleşmesi (alet skili). API istek/yanıt zarfı {succeeded, message, data}, liste zarfı {Data, TotalCount} ve pagination (Page + Take, 1-tabanlı)…
- **Main ne olarak tanımlıyor:** Yanıt zarfı unwrap / pagination
- **Uyum:** ✅ uyumlu

**`screen-structure-mobile`** — desc tipi: **DURUM**

- **Desc ne diyor:** Yeni bir mobil ekran yazılacakken açılır: route dosyası ile ekran component'i ayrılırken, liste/form/detay ekranı kurgulanırken ve bir ekran büyüyüp parçalara bölünmesi g…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* Mobile-developer'ın alet çantası ve kendine özgü iş kanonu. "Nasıl ekran kurulur"u ANLATMAZ (o `screen-structure-mobile`) — hangi işte hangi…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`state-mobile`** — desc tipi: **DURUM**

- **Desc ne diyor:** Mobil tarafta ekranlar arası taşınan bir veri tutulacakken açılır: context ya da provider kurulurken, kullanıcı bilgisi uygulama genelinde paylaşılırken, çok adımlı bir f…
- **Main ne olarak tanımlıyor:** Client state (Context/Providers, wizard)
- **Uyum:** ✅ uyumlu

**`style-mobile`** — desc tipi: **DURUM**

- **Desc ne diyor:** Mobil tarafta görsel bir şey yazılacakken açılır: bir ekrana stil verilirken, renk/tipografi/spacing seçilirken, iOS ile Android arasında görünüm farkı çıktığında ve 'bur…
- **Main ne olarak tanımlıyor:** Stil (StyleSheet, tema)
- **Uyum:** ✅ uyumlu

**`tasarim-prensipleri`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak tasarım prensipleri sözleşmesi (alet skili). Dil-nötr mühendislik tuzakları ve karar prensipleri burada tek kaynak olarak tanımlıdır: hata izolasyonu, se…
- **Main ne olarak tanımlıyor:** tasarım tuzakları
- **Uyum:** ✅ uyumlu

**`upload`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak dosya yükleme sözleşmesi (alet skili). FormData multipart istek, BE FormFile→Azure blob depolama ve URL dönüşü burada tek kaynak olarak tanımlıdır. Üç uç…
- **Main ne olarak tanımlıyor:** Dosya/görsel yükleme (FormData)
- **Uyum:** ✅ uyumlu

---

## Main Skill: `quality`  *(agent: qa-engineer)*

**Main desc:** qa-engineer'ın omurga skili, preload edilir. Bir denetim işi geldiğinde hangi aletin açılacağına karar verilirken, her denetimde geçerli çekirdek kanon gerektiğinde (statik kapı, diff dışı tam okuma, kanıtsız bulgu yasağ…

### Preloaded skiller

**`behavior`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin ortak davranış çekirdeği (preloaded) — her agentın karakteri, çalışma refleksi, kalite sahipliği, iletişim tarzı, git disiplini. Tüm pipe…
- **Main ne olarak tanımlıyor:** Mesaj dili ortak kanon (`behavior` `BEHAVIOR-SELF-CONTAINED-MESSAGE`) — burada tekrar tanımlanmaz.

**`handoff`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin handoff (iş devri) iletişim kuralları (ortak çekirdek, preloaded) — bir agent başka bir agent'a iş/bilgi iletirken UYACAĞI biçim. Tüm pip…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`memory-management`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin memory yönetim kurallar bütünü (ortak çekirdek, preloaded) — memory'ye NE yazılır, NE yazılmaz, çelişki nasıl işaretlenir, index nasıl ko…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`is-akisi`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin iş akışı iskeleti (ortak çekirdek, preloaded) — kim kimden ne alır, kime ne devreder, iş hangi sırayla ilerler. Tüm pipeline agent (PA, U…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`pr-yazilim-oy-envanteri`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım (OY) sistem, ekip ve iş üretme bilinci (üst skil, tüm OY agentları preload). Üç bölüm: TEKNOLOJİ VE İŞLEYİŞ (biz neyle çalışırız — altyapı, yığın,…
- **Main ne olarak tanımlıyor:** Sistem/işleyiş/teknoloji bağlamı

**`dev-deploy`** 

- **Desc ne diyor:** Bir değişiklik dev ortamına alınırken açılır: developer commit'ini QA'ya devrederken, QA denetimden geçirip `main`'e push ederken, push öncesi kapsam ve branch koruması k…
- **Main ne olarak tanımlıyor:** Push / merge / Actions takibi

**`prod-deploy`** 

- **Desc ne diyor:** Bir iş canlıya (production) çıkarılırken açılır: kullanıcı 'canlıya alalım / production'a geçeceğiz / prod'a çıkalım' dediğinde, prod PR'ı açılırken, canlıya çıkış tarama…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

### On-demand skiller

**`auth`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak kimlik/oturum sözleşmesi (alet skili). GUID session (Redis, JWT değil), token header, prefix→rol eşlemesi ve 401 tanıma burada tek kaynak olarak tanımlıd…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* zarf→`response-request`, kimlik→`auth`. (Kanon orada tek kaynak; QA okur, kopyalamaz.)
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`backend`** — desc tipi: **IKISI**

- **Desc ne diyor:** backend-developer'ın omurga skili, preload edilir. Bir backend işi geldiğinde hangi aletin açılacağına karar verilirken, commit öncesi doğrulamanın ne olduğu sorulduğunda…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* tam kanon: BE→`backend`(+alt), FE→`frontend`(+alt), MB→`mobile`(+alt), DB→`database`, enum→`enum-sync`,
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`code-auditor`** — desc tipi: **IKISI**

- **Desc ne diyor:** code-auditor'ın omurga skili, preload edilir. Bir denetim ya da etki işi geldiğinde hangi öz skilin açılacağına karar verilirken, CA'nın bir işi üstlenip üstlenmeyeceği s…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* > tarayamaz (snapshot CA'da) → `code-auditor`'a reaktif etki analizi handoff'u, IMPACT ile incele.
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`code-quality`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak kod kalitesi sözleşmesi (alet skili). Dosya/metot boyut eşiği, tekrar→helper, god-object yasağı, tek-sorumluluk, yorum disiplini, magic string/number yas…
- **Main ne olarak tanımlıyor:** Kod kalite eşiği / teknik borç ölçümü
- **Uyum:** ✅ uyumlu

**`commit-review`** — desc tipi: **DURUM**

- **Desc ne diyor:** Bir commit ya da PR incelenecekken açılır: developer 'inceleme yapılabilir' dediğinde, push öncesi birikmiş commit'ler toplu değerlendirilirken, dış bir PR gözden geçiril…
- **Main ne olarak tanımlıyor:** Commit/PR statik inceleme
- **Uyum:** ✅ uyumlu

**`database`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım veritabanı sözleşmesi (MSSQL + EF Core, ortak alet skili). EntityBase 6 alan, canonical veri tipleri, property ordering, isimlendirme, NVARCHAR uzunlukları, by…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* tam kanon: BE→`backend`(+alt), FE→`frontend`(+alt), MB→`mobile`(+alt), DB→`database`, enum→`enum-sync`,
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`enum-sync`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak enum senkron sözleşmesi (alet skili). Enum kaynağı (library-datatype), byte tipi, 1-tabanlı değer ve BE→client senkron kuralı burada tek kaynak olarak ta…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* tam kanon: BE→`backend`(+alt), FE→`frontend`(+alt), MB→`mobile`(+alt), DB→`database`, enum→`enum-sync`,
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`escaped-bug-analysis`** — desc tipi: **DURUM**

- **Desc ne diyor:** QA kapısından geçmiş bir kodda hata çıktığında açılır: PA 'bu kod denetimden geçmişti ama yayında/dev'de patladı' diye bildirdiğinde, hangi kontrolün atlandığı çıkarılırk…
- **Main ne olarak tanımlıyor:** Kaçan hata
- **Uyum:** ✅ uyumlu

**`frontend`** — desc tipi: **IKISI**

- **Desc ne diyor:** frontend-developer'ın omurga skili, preload edilir. Bir panel işi geldiğinde hangi aletin açılacağına karar verilirken, commit öncesi doğrulamanın ne olduğu sorulduğunda …
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* tam kanon: BE→`backend`(+alt), FE→`frontend`(+alt), MB→`mobile`(+alt), DB→`database`, enum→`enum-sync`,
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`mobile`** — desc tipi: **IKISI**

- **Desc ne diyor:** mobile-developer'ın omurga skili, preload edilir. Bir mobil işi geldiğinde hangi aletin açılacağına karar verilirken, iOS ile Android arasında ayrı koşum gerekip gerekmed…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* tam kanon: BE→`backend`(+alt), FE→`frontend`(+alt), MB→`mobile`(+alt), DB→`database`, enum→`enum-sync`,
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`module-audit`** — desc tipi: **DURUM**

- **Desc ne diyor:** Bir modülün tamamı denetlenecekken açılır: 'consistency audit / modül denetimi / modül kapanış kontrolü' denildiğinde, bir modül ya da panel bütünüyle gözden geçirilirken…
- **Main ne olarak tanımlıyor:** Modül kapanışı / consistency audit
- **Uyum:** ✅ uyumlu

**`module-development`** — desc tipi: **IKISI**

- **Desc ne diyor:** Bir endpoint ya da modül baştan sona yazılacağında açılır: handler kurulurken, veri katmanına dokunulurken, yetki bildirimi ve doğrulama eklenirken, önbellek kullanılırke…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* **Handler / model sözleşmesi** (`module-development`)
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`orkestrasyon`** — desc tipi: **DURUM**

- **Desc ne diyor:** Bir modül kapatılırken, session kapanışında kimin işi askıda kaldığı çıkarılırken, QA bir discovery sapması bildirdiğinde ve iş canlıya (prod) çıkarılırken açılır. 'Modül…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* QA yalnız kendi olaylarını düşer: commit onayı, push, Actions sonucu. **Durum** kendi ClickUp sub task'ında, **gerekçe** ("şu Actions şu yüz…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`production-audit`** — desc tipi: **DURUM**

- **Desc ne diyor:** Bir iş canlıya çıkarılmadan önce açılır: PA 'canlıya geçecek, taramayı başlat' dediğinde, prod SQL'i doğrulanır ya da modelden üretilirken ve canlı veriye dokunacak değiş…
- **Main ne olarak tanımlıyor:** Canlıya çıkış taraması
- **Uyum:** ⚠️ kelime örtüşmesi düşük (elle okundu: anlamca uyumlu)

**`response-request`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak iletişim sözleşmesi (alet skili). API istek/yanıt zarfı {succeeded, message, data}, liste zarfı {Data, TotalCount} ve pagination (Page + Take, 1-tabanlı)…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* zarf→`response-request`, kimlik→`auth`. (Kanon orada tek kaynak; QA okur, kopyalamaz.)
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`setup-ozelyazilim-plugin`** — desc tipi: **HICBIRI**

- **Desc ne diyor:** ozel-yazilim plugin'i kurulduktan sonra kullanıcının PC'sini PR Yazılım özel-yazılım agent ekosistemiyle çalışmaya hazırlayan interaktif kurulum sihirbazı. Kullanıcı bir …
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* Agent yapılandırması **global (user) scope'ta** yaşar (`setup-ozelyazilim-plugin` `SETUP-MCP-GLOBAL-ONLY`). Proje kopyası çift kaynaktır: bi…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`style-mobile`** — desc tipi: **DURUM**

- **Desc ne diyor:** Mobil tarafta görsel bir şey yazılacakken açılır: bir ekrana stil verilirken, renk/tipografi/spacing seçilirken, iOS ile Android arasında görünüm farkı çıktığında ve 'bur…
- **Main ne olarak tanımlıyor:** Cross-platform şüphesi (native/keyboard/safe-area/permission)
- **Uyum:** ✅ uyumlu

---

## Main Skill: `test-engineer`  *(agent: test-engineer)*

**Main desc:** test-engineer'ın omurga skili, preload edilir. Bir test, repro ya da veri işi geldiğinde hangi modun açılacağına karar verilirken, TE'nin bir işi üstlenip üstlenmeyeceği sorulduğunda ve rol sınırı belirsizleştiğinde geçe…

### Preloaded skiller

**`behavior`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin ortak davranış çekirdeği (preloaded) — her agentın karakteri, çalışma refleksi, kalite sahipliği, iletişim tarzı, git disiplini. Tüm pipe…
- **Main ne olarak tanımlıyor:** Ortak davranış (karakter, iletişim, git, commit)

**`handoff`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin handoff (iş devri) iletişim kuralları (ortak çekirdek, preloaded) — bir agent başka bir agent'a iş/bilgi iletirken UYACAĞI biçim. Tüm pip…
- **Main ne olarak tanımlıyor:** Ortak davranış (karakter, iletişim, git, commit)

**`memory-management`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin memory yönetim kurallar bütünü (ortak çekirdek, preloaded) — memory'ye NE yazılır, NE yazılmaz, çelişki nasıl işaretlenir, index nasıl ko…
- **Main ne olarak tanımlıyor:** Ortak davranış (karakter, iletişim, git, commit)

**`is-akisi`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin iş akışı iskeleti (ortak çekirdek, preloaded) — kim kimden ne alır, kime ne devreder, iş hangi sırayla ilerler. Tüm pipeline agent (PA, U…
- **Main ne olarak tanımlıyor:** Ortak davranış (karakter, iletişim, git, commit)

**`pr-yazilim-oy-envanteri`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım (OY) sistem, ekip ve iş üretme bilinci (üst skil, tüm OY agentları preload). Üç bölüm: TEKNOLOJİ VE İŞLEYİŞ (biz neyle çalışırız — altyapı, yığın,…
- **Main ne olarak tanımlıyor:** Ortak davranış (karakter, iletişim, git, commit)

### On-demand skiller

**`backend`** — desc tipi: **IKISI**

- **Desc ne diyor:** backend-developer'ın omurga skili, preload edilir. Bir backend işi geldiğinde hangi aletin açılacağına karar verilirken, commit öncesi doğrulamanın ne olduğu sorulduğunda…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* > ℹ️ **Bu omurga `## Operatif çekirdek` cache bloğu TAŞIMAZ — bilinçli.** TE **2** dış kurala bağımlı (`BEHAVIOR-NO-INFRA-CMD` alet çantasın…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`code-auditor`** — desc tipi: **IKISI**

- **Desc ne diyor:** code-auditor'ın omurga skili, preload edilir. Bir denetim ya da etki işi geldiğinde hangi öz skilin açılacağına karar verilirken, CA'nın bir işi üstlenip üstlenmeyeceği s…
- **Main ne olarak tanımlıyor:** Rol sınırı: statik kök-neden + çağrı grafı
- **Uyum:** ⚠️ kelime örtüşmesi düşük (elle okundu: anlamca uyumlu)

**`code-quality`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak kod kalitesi sözleşmesi (alet skili). Dosya/metot boyut eşiği, tekrar→helper, god-object yasağı, tek-sorumluluk, yorum disiplini, magic string/number yas…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* **Denetleyen kod yazmaz → `code-quality` `CODE-NO-WRITE-ON-AUDIT`** (tek kaynak, QA+CA+TE ortak).
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`data-access`** — desc tipi: **DURUM**

- **Desc ne diyor:** Panelde API'ye bağlanılacakken açılır: veri çeken ya da yazan bir hook yazılırken, query key belirlenirken, bir mutasyondan sonra hangi verinin tazeleneceğine karar veril…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* Test verisi = sistemin kendi kapılarından geçmiş veri. "API ve arayüz tek sınırdır": TE ya paneli/mobili kullanarak (insan gibi) ya da endpo…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`database`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım veritabanı sözleşmesi (MSSQL + EF Core, ortak alet skili). EntityBase 6 alan, canonical veri tipleri, property ordering, isimlendirme, NVARCHAR uzunlukları, by…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* Test verisi = sistemin kendi kapılarından geçmiş veri. "API ve arayüz tek sınırdır": TE ya paneli/mobili kullanarak (insan gibi) ya da endpo…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`dev-environment`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak lokal geliştirme ortamı sözleşmesi (alet skili). Makefile hedefleri, Telepresence intercept (x-dev-user) ve lokal doğrulama akışı burada tek kaynak olara…
- **Main ne olarak tanımlıyor:** Projeyi ayağa kaldırma (Makefile hedefleri, make dev)
- **Uyum:** ✅ uyumlu

**`e2e-verification`** — desc tipi: **DURUM**

- **Desc ne diyor:** E2E test et / senaryo testi / uçtan uca dene / modülü test et / test at' denildiğinde ve PA 'modül bitti, senaryo testi' diye devrettiğinde açılır: DISCOVERY'den senaryo …
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* TE'nin alet çantası ve kendine özgü kimlik kanonu. "Nasıl E2E yapılır" / "nasıl repro edilir" / "nasıl veri kurulur"u ANLATMAZ (o `e2e-verif…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`quality`** — desc tipi: **IKISI**

- **Desc ne diyor:** qa-engineer'ın omurga skili, preload edilir. Bir denetim işi geldiğinde hangi aletin açılacağına karar verilirken, her denetimde geçerli çekirdek kanon gerektiğinde (stat…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* > ℹ️ **Bu omurga `## Operatif çekirdek` cache bloğu TAŞIMAZ — bilinçli.** TE **2** dış kurala bağımlı (`BEHAVIOR-NO-INFRA-CMD` alet çantasın…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`repro-diagnosis`** — desc tipi: **DURUM**

- **Desc ne diyor:** Bu hatayı yakala / neden çalışmıyor / repro et / çıkan hatayı bul' denildiğinde ve PA bug triyajından işlev-testi, veri ya da UX gerektiren bir bug devrettiğinde açılır: …
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* TE'nin alet çantası ve kendine özgü kimlik kanonu. "Nasıl E2E yapılır" / "nasıl repro edilir" / "nasıl veri kurulur"u ANLATMAZ (o `e2e-verif…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`test-data-setup`** — desc tipi: **DURUM**

- **Desc ne diyor:** Test verisi hazırla / test ortamı kur / toplu veri gir / test kullanıcısı aç' denildiğinde ve bir E2E ya da repro işi gerçekçi veri gerektirdiğinde açılır: dataset toplan…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* TE'nin alet çantası ve kendine özgü kimlik kanonu. "Nasıl E2E yapılır" / "nasıl repro edilir" / "nasıl veri kurulur"u ANLATMAZ (o `e2e-verif…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

---

## Main Skill: `code-auditor`  *(agent: code-auditor)*

**Main desc:** code-auditor'ın omurga skili, preload edilir. Bir denetim ya da etki işi geldiğinde hangi öz skilin açılacağına karar verilirken, CA'nın bir işi üstlenip üstlenmeyeceği sorulduğunda ve rol sınırı belirsizleştiğinde geçer…

### Preloaded skiller

**`behavior`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin ortak davranış çekirdeği (preloaded) — her agentın karakteri, çalışma refleksi, kalite sahipliği, iletişim tarzı, git disiplini. Tüm pipe…
- **Main ne olarak tanımlıyor:** Ortak davranış (karakter, iletişim, git, commit)

**`handoff`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin handoff (iş devri) iletişim kuralları (ortak çekirdek, preloaded) — bir agent başka bir agent'a iş/bilgi iletirken UYACAĞI biçim. Tüm pip…
- **Main ne olarak tanımlıyor:** Ortak davranış (karakter, iletişim, git, commit)

**`memory-management`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin memory yönetim kurallar bütünü (ortak çekirdek, preloaded) — memory'ye NE yazılır, NE yazılmaz, çelişki nasıl işaretlenir, index nasıl ko…
- **Main ne olarak tanımlıyor:** Ortak davranış (karakter, iletişim, git, commit)

**`is-akisi`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin iş akışı iskeleti (ortak çekirdek, preloaded) — kim kimden ne alır, kime ne devreder, iş hangi sırayla ilerler. Tüm pipeline agent (PA, U…
- **Main ne olarak tanımlıyor:** Ortak davranış (karakter, iletişim, git, commit)

**`pr-yazilim-oy-envanteri`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım (OY) sistem, ekip ve iş üretme bilinci (üst skil, tüm OY agentları preload). Üç bölüm: TEKNOLOJİ VE İŞLEYİŞ (biz neyle çalışırız — altyapı, yığın,…
- **Main ne olarak tanımlıyor:** Ortak davranış (karakter, iletişim, git, commit)

### On-demand skiller

**`code-quality`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak kod kalitesi sözleşmesi (alet skili). Dosya/metot boyut eşiği, tekrar→helper, god-object yasağı, tek-sorumluluk, yorum disiplini, magic string/number yas…
- **Main ne olarak tanımlıyor:** Ortak kod kalite ölçütü (boyut/DRY/magic/naming denetim eşiği)
- **Uyum:** ✅ uyumlu

**`impact-analiz`** — desc tipi: **DURUM**

- **Desc ne diyor:** Mevcut yapıya dokunan ya da yayındaki bir projeye giren bir iş geldiğinde açılır: 'bu nereleri etkiler / ne kırılır' sorusu doğduğunda, CA'dan etki analizi istenirken, de…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* CA analiz/rapor üretir → isteyene BİLGİ verir (PA proaktif tetikse PA'ya, QA reaktif tetikse QA'ya da). CA developer'a DOĞRUDAN iş vermez, C…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`impact-analysis`** — desc tipi: **DURUM**

- **Desc ne diyor:** Bir etki analizi işi geldiğinde açılır: 'bu değişiklik nereleri etkiler / ne kırılır' sorusu sorulduğunda, PA bir DISCOVERY ile mevcut yapıya dokunan iş getirdiğinde, QA …
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* CA'nın alet çantası ve kendine özgü kimlik kanonu. "Nasıl etki analizi yapılır" / "nasıl audit yapılır"ı ANLATMAZ (o `impact-analysis` / `st…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`module-audit`** — desc tipi: **DURUM**

- **Desc ne diyor:** Bir modülün tamamı denetlenecekken açılır: 'consistency audit / modül denetimi / modül kapanış kontrolü' denildiğinde, bir modül ya da panel bütünüyle gözden geçirilirken…
- **Main ne olarak tanımlıyor:** Ortak kod kalite eşiği (boyut/DRY/magic/naming)
- **Uyum:** ⚠️ çok-hedefli satır

**`project-assistant`** — desc tipi: **IKISI**

- **Desc ne diyor:** project-assistant'ın omurga skili, preload edilir. Bir talep geldiğinde hangi öz skilin açılacağına karar verilirken, PA'nın bir işi üstlenip üstlenmeyeceği sorulduğunda …
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* **Denetleyen sınırı** (`code-quality` · `project-assistant`)
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`structural-audit`** — desc tipi: **DURUM**

- **Desc ne diyor:** Kod denetimi / yapısal tarama / tüm projeyi tara / proje sağlık kontrolü / modülleri karşılaştır' denildiğinde açılır: bir proje modül modül taranırken, kanon sapması ve …
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* CA'nın alet çantası ve kendine özgü kimlik kanonu. "Nasıl etki analizi yapılır" / "nasıl audit yapılır"ı ANLATMAZ (o `impact-analysis` / `st…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

---

## Main Skill: `devops`  *(agent: devops-engineer)*

**Main desc:** devops-engineer'ın omurga skili, preload edilir. Bir altyapı işi geldiğinde hangi aletin açılacağına karar verilirken, prod'a dokunulup dokunulamayacağı sorulduğunda ve rol sınırı belirsizleştiğinde geçerlidir. qa-engine…

### Preloaded skiller

**`behavior`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin ortak davranış çekirdeği (preloaded) — her agentın karakteri, çalışma refleksi, kalite sahipliği, iletişim tarzı, git disiplini. Tüm pipe…
- **Main ne olarak tanımlıyor:** Hükmün tek kaynağı `behavior` `BEHAVIOR-NO-INFRA-CMD` (tüm agentlar); bu ID **DO ucudur** — prod/cluster komutları en çok burada üretilir. DO tarafı:

**`handoff`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin handoff (iş devri) iletişim kuralları (ortak çekirdek, preloaded) — bir agent başka bir agent'a iş/bilgi iletirken UYACAĞI biçim. Tüm pip…
- **Main ne olarak tanımlıyor:** **Kendi olayını kendin yazarsın → `handoff` `HANDOFF-STATUS-OWN-EVENTS`** (tek kaynak, 9 agent ortak).

**`memory-management`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin memory yönetim kurallar bütünü (ortak çekirdek, preloaded) — memory'ye NE yazılır, NE yazılmaz, çelişki nasıl işaretlenir, index nasıl ko…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`is-akisi`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım ekibinin iş akışı iskeleti (ortak çekirdek, preloaded) — kim kimden ne alır, kime ne devreder, iş hangi sırayla ilerler. Tüm pipeline agent (PA, U…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`pr-yazilim-oy-envanteri`** — *ortak çekirdek*

- **Desc ne diyor:** PR Yazılım özel yazılım (OY) sistem, ekip ve iş üretme bilinci (üst skil, tüm OY agentları preload). Üç bölüm: TEKNOLOJİ VE İŞLEYİŞ (biz neyle çalışırız — altyapı, yığın,…
- **Main ne olarak tanımlıyor:** — *(main SKILL.md içinde yönlendirme satırı yok; preload olduğu için gerekmiyor)*

**`dev-deploy`** 

- **Desc ne diyor:** Bir değişiklik dev ortamına alınırken açılır: developer commit'ini QA'ya devrederken, QA denetimden geçirip `main`'e push ederken, push öncesi kapsam ve branch koruması k…
- **Main ne olarak tanımlıyor:** Git akışı / push-merge sahipliği / deploy rol paylaşımı

**`prod-deploy`** 

- **Desc ne diyor:** Bir iş canlıya (production) çıkarılırken açılır: kullanıcı 'canlıya alalım / production'a geçeceğiz / prod'a çıkalım' dediğinde, prod PR'ı açılırken, canlıya çıkış tarama…
- **Main ne olarak tanımlıyor:** DO kubectl/telepresence/SQL komutlarını YAZAR ama çalıştırmaz — kullanıcı çalıştırır (yanlış cluster/context riski). Prod işi öncesi doğru context tey…

### On-demand skiller

**`api-project`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım yeni API servisi ekleme sözleşmesi (.NET, ortak alet skili). Mevcut solution'a yeni bir 'api-{domain}' servisi eklenirken bu skil açılır: dotnet-template'teki …
- **Main ne olarak tanımlıyor:** Yeni API servisi kurulumu (template klonlama)
- **Uyum:** ✅ uyumlu

**`ci-cd`** — desc tipi: **DURUM**

- **Desc ne diyor:** Bir CI/CD işi geldiğinde açılır: yeni bir servis için workflow kurulurken, deploy tetiği ya da branch→ortam eşlemesi ayarlanırken, path filtresi yazılırken, action sürüml…
- **Main ne olarak tanımlıyor:** CI/CD pipeline (workflow, deploy tetiği, branch→ortam)
- **Uyum:** ✅ uyumlu

**`code-quality`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak kod kalitesi sözleşmesi (alet skili). Dosya/metot boyut eşiği, tekrar→helper, god-object yasağı, tek-sorumluluk, yorum disiplini, magic string/number yas…
- **Main ne olarak tanımlıyor:** Kod kalite eşiği
- **Uyum:** ✅ uyumlu

**`cronjob`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak zamanlı iş sözleşmesi (alet skili). K8s CronJob mekanizması (tek Main() console app), BE'nin iş mantığı yazması ve DO'nun schedule deploy etmesi burada t…
- **Main ne olarak tanımlıyor:** Zamanlı iş deploy (K8s CronJob)
- **Uyum:** ✅ uyumlu

**`dev-environment`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak lokal geliştirme ortamı sözleşmesi (alet skili). Makefile hedefleri, Telepresence intercept (x-dev-user) ve lokal doğrulama akışı burada tek kaynak olara…
- **Main ne olarak tanımlıyor:** Makefile kanonu + telepresence intercept altyapısı
- **Uyum:** ✅ uyumlu

**`docker-k8s`** — desc tipi: **DURUM**

- **Desc ne diyor:** Container ya da Kubernetes tarafına dokunulacağında açılır: Dockerfile yazılırken ya da değiştirilirken, deployment/job manifesti kurulurken, ingress route eklenirken, re…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* DevOps-engineer'ın alet çantası ve kendine özgü iş kanonu. DO kaynak kod yazmaz ama Makefile/Dockerfile/CI-YAML/K8s-manifest yazar, projeyi …
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`env-config`** — desc tipi: **IKISI**

- **Desc ne diyor:** Bir env değeri ya da gizli değer işi geldiğinde açılır: yeni secret eklenirken, bir env değişkeninin build-time mı runtime mı olduğuna karar verilirken, credential inject…
- **Main ne olarak tanımlıyor:** Env / secret (build-time vs runtime, çift-güncelleme)
- **Uyum:** ✅ uyumlu

**`iap`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak uygulama-içi satın alma sözleşmesi (alet skili). RevenueCat 3-katman (MB SDK satın alır, BE API sorgulayarak doğrular, DO store ürün tanımlar) burada tek…
- **Main ne olarak tanımlıyor:** IAP store ürünü + RevenueCat key
- **Uyum:** ✅ uyumlu

**`mobile-release`** — desc tipi: **DURUM**

- **Desc ne diyor:** Mobil uygulama store'a çıkarılacağında açılır: EAS build ya da submit koşulurken, TestFlight veya Play Internal'a gönderilirken, release tetikleyicisi kurulurken, eas.jso…
- **Main ne olarak tanımlıyor:** Mobil dağıtım (EAS build/submit, store, credential)
- **Uyum:** ✅ uyumlu

**`notification`** — desc tipi: **IKISI**

- **Desc ne diyor:** PR Yazılım ortak haber ulaştırma sözleşmesi (alet skili). Push (Expo) + mail + SMS + in-app kanalları, RabbitMQ kuyruk + job-consumer üretimi ve kanal altyapısı burada te…
- **Main ne olarak tanımlıyor:** Consumer job deploy + push/mail/sms credential
- **Uyum:** ✅ uyumlu

**`quality`** — desc tipi: **IKISI**

- **Desc ne diyor:** qa-engineer'ın omurga skili, preload edilir. Bir denetim işi geldiğinde hangi aletin açılacağına karar verilirken, her denetimde geçerli çekirdek kanon gerektiğinde (stat…
- **Main ne olarak tanımlıyor:** *(menü satırı DEĞİL — düz metne gömülü)* DO altyapı girdilerini ekler (`.telepresence/`, build, `.maestro/`, env), PA doküman girdilerini (`docs/moduls/**/*.sql`). İki taraf da **ek…
- **Uyum:** ⚠️ **agent tarayarak bulamaz** — ancak main skill'i baştan sona okursa görür

**`system-topology`** — desc tipi: **DURUM**

- **Desc ne diyor:** Bu proje nelerden oluşuyor / ne neye bağlı / hangi birim nerede koşuyor' sorusu doğduğunda açılır: bir deploy kararı verilirken birim tipi ve bağımlılıkları çıkarılırken,…
- **Main ne olarak tanımlıyor:** Sistem topolojisi (birim tipleri, bağımlılık, service/route naming)
- **Uyum:** ⚠️ kelime örtüşmesi düşük (elle okundu: anlamca uyumlu)

---

## Ölçümün sınırı

Bu ölçüm **metin uyumunu** ölçtü: yönlendirme satırı ile hedef description aynı şeyi söylüyor mu.
**Ölçmediği şey:** agent gerçek bir iş sırasında o satıra bakıyor mu, yoksa tahmin mi ediyor.
Onun cevabı ancak davranış ölçümünden çıkar — bir agenta iş verip hangi skilleri açtığını saymaktan.
