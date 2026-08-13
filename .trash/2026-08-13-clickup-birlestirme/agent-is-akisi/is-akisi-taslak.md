# Agent iş akışı — taslak v2

**Tarih:** 2026-08-12 · **Yazan:** Clara (fabrika) · **Durum:** TASLAK — kanona girmedi
**Önceki sürüm:** v1 (17:04'te PAM'e okutuldu, **18 soru** geldi, *"kanon yazamam"* dedi)
**Bu sürüm:** 18 sorunun tamamı cevaplandı → `pam-sorulari.md`

⚠️ **Bu bir gereksinim taslağıdır, kanon değil.** Kanonu PAM üretir, PAD yazar, PQA
denetler. Kaynak: bugün sahada kurulup test edilen düzen + Mert'in bugünkü kararları.

---

# 0. v1'e göre ne değişti — okuyan için

| Ne | v1'de | v2'de |
|---|---|---|
| Rol adı | "Clara" | **`kullanıcı`** — OY kanonunda Clara diye bir kavram YOK (ölçüldü: 0 dosya) |
| Sub task sahipliği | assignee sanılıyordu | **başlık öneki** `[FE]` — assignee kullanılmıyor (ölçüldü: hepsi boş) |
| Etkilenen kural | 1 tane | **4 tane** — `CLICKUP-ROLE-STATUS` + `CLICKUP-TRACE-ACTION-APPROVAL` + `QA-APPROVE-ATOMIC` de düşüyor |
| Cascade | 16 dosya | **21 dosya** (PAM ölçtü, v1 eksikti) |
| Beş sub task | şablon gibi anlatılmış | **örnektir** — katman sayısı discovery'den çıkar |
| `DEVIR-*.md` | açık soru | **kalkıyor** — `pause` yorumu yerini tutuyor |
| Kanıt | dört tür, role eşlenecek sanıldı | **çıktı türüne göre** — role göre değil |

---

# 1. Kayıt nerede tutulur

Tek yer: **ClickUp.**

Kalkan iki dosya:
- `_project/TASK-STATUS.md`
- `{modul}/{task}/status.md`

Ve onlarla birlikte **`DEVIR-{hedef}.md`** de kalkıyor (aşağıda 7.2).

Gerekçe (Mert): *"olay akışı sub task'ler sayesinde ClickUp'ta zaten."*

## Geçiş — yürüyen projeler ne olacak

**Tüm projelerde kullanılacak.** Yeni task'lar bu şekilde ilerler.

**Eski task'lar** `TASK-STATUS.md` ve `status.md`'de yaşamaya devam eder. PA bir süre
**ikisini birden** kontrol eder. Agent'lar artık bu dosyalara **yazmaz** — yeni işin
kaydı ClickUp'a gider.

Karar: `kararlar/2026-08-12-task-status-ve-status-md-kalkiyor.md`

---

# 2. Sub task yapısı

## Başlık formatı — ZORUNLU

```
[FE] PRAG - Randevu Müsaitlik - Takvim Görünümü
[BE] PRAG - Randevu Müsaitlik - Şablon, Slot Üretimi
[PA] PRAG - Randevu Müsaitlik - Discovery
```

**Kural:** *"Başlık `[SENİN-KISALTMAN]` ile başlamıyorsa o task'a dokunma."*

**Agent kısaltmaları:** `PA` · `BE` · `FE` · `MB` · `DO` · `QA` · `TE` · `CA` · `UID`

**Neden köşeli parantez (iki alternatif elendi):** alan sırasına dayanan formatlarda
modül adında bir tire geçerse **alan kayar** ve kural sessizce yanlış task'ı işaret
eder. `startswith` ölçümü ayraç sayısından ve modül adından bağımsızdır.

⚠️ **Sahiplik alanı (`assignee`) KULLANILMAZ.** Ölçüldü: bugünkü beş sub task'ın
hepsinde `assignees: []`. Sahiplik başlıktan okunur.

## Kaç sub task — sabit değil

**Beş sub task bir ÖRNEKTİR, şablon değil.**

Sabit olan: **PA'nın iki sub task'ı** (discovery + kapanış).
Değişken olan: **discovery'den çıkan her katman için bir sub task.**

```
PRC-26  Randevu Takvimi                    [ana task]
  ├─ [PA]  Discovery      ← SABİT
  ├─ [UID] Mock           ┐
  ├─ [BE]  Contract       ├ discovery'den çıkar, sayısı değişir
  ├─ [FE]  Ekran          ┘
  └─ [PA]  Kapanış        ← SABİT, baştan açılır, Open durur
```

Katman sub task'ları **discovery'den SONRA** açılır — hangi katmanların gireceği
discovery'den çıkar, önce bilinemez. Bir işte MB/DO/TE/CA girmeyebilir.

## PA'nın iki sub task'ının sebebi — ölçüldü

**Discovery:** ilk turda PA 78 dakika çalıştı ve **ClickUp'ta tek izi yoktu.**
*"PA ne yapıyor"* sorusunun cevabı yalnız kanal kutusundaydı.

**Kapanış:** baştan açılır, `Open` durur. PA'nın cümlesi: *"sahada en sık kaybolan iş
BİTMİŞ AMA KAPANMAMIŞ iştir; kapanış kutusu Open dururken kimse 'bitti' diyemez.
Bu görünürlük kaydı değil, bir KAPI."*

---

# 3. Kim ne açar, kim ne çevirir

**Ana task'ı `kullanıcı` açar.** Task yoksa PA'ya açtırır — o da kullanıcının onayıyla
olur. **Sub task'ları PA serbestçe açar** (ayrı onay gerekmez).

**Agent yalnız kendi sub task'ının statüsünü çevirir.**

Yasak (mutlak): ana task · başkasının sub task'ı · `Closed` · `revise` · task silme

**ANA TASK HER ZAMAN PA'NIN.** Statüsünü yalnız PA çevirir — QA dahil hiçbir agent
dokunmaz.

**QA'nın tek istisnası:** push ettiği **sub task**'ı `live - dev`'e alır (adım 7b).
Bunun dışında statüye dokunmaz.

Karar: `kararlar/2026-08-12-clickup-yazma-yetkisi-kapsam-daraltma.md`

⚠️ **"Clara" kanonda GEÇMEZ.** OY agent kanonunda böyle bir kavram yok (ölçüldü:
`grep -ril clara` → 0 dosya). Kanon `kullanıcı` der. Clara Mert'e özel, onun
bilgisayarında çalışan bir agent'tır; agent'ların dünyasında `kullanıcı` olarak görünür.
Karar: `kararlar/2026-08-12-clara-oy-kanonuna-girmiyor.md`

---

# 4. Akışın sırası

**1 · PA işi alır**
→ ana task `in progress` + kendi discovery sub task'ı `in progress`

**2 · Gereksinim netleştirme — `kullanıcı` ↔ PA, DÖNGÜSEL**

PA discovery'yi soru sormadan yazmaz (`PA-DISC-RISK-CLOSE` / `PA-DISC-NO-TBD`).
Açık riskleri `kullanıcı`ya sorar; cevaplar **yeni sorular doğurur**, tekrar sorar.

Bugünkü testte **üç tur:** 6 risk → 5 türev soru → 5 daha. **11 madde karara bağlandı,
TBD sıfır.** Örnek: *"slot süresi değişince mevcut randevular ne olur"*, *"sekreter
görebilir dedin — randevu ALABİLİR mi"*. Hepsi **iş kararı** — developer'a
devredilemez, PA uyduramaz.

⚠️ PA cevabı doğrudan dokümana ÇEVİRMEZ (`PA-DISC-ANSWER-NOT-REQUIREMENT`).

**3 · Discovery biter**
→ `completed` (kanıt: doküman yolu + commit)
→ katman sub task'ları + kapanış açılır

**4 · Agent işe başlar**
PA'dan handoff alır → **hangi task'ı yapacağını handoff'tan okur** → `in progress` çeker

**5 · Agent bitirir** → `test` çeker (QA'ya devrediyor)

**6 · QA denetler**
- **ONAY** → onay handoff'u yazar, **statüye dokunmaz** (`completed`'ı agent çeker)
- **RED** → task'ı `revise`'a alır → agent düzeltirken `in progress` çeker → bitince
  yine `test`

**7 · Agent QA onayını alınca `completed` çeker**

**7b · QA push ettiğinde push'ladığı sub task'ı `live - dev`'e alır**

⚠️ **QA'nın statüye dokunduğu TEK yer burasıdır** ve sınırı dar: yalnız `live - dev`,
yalnız kendi push'ladığı sub task. Onay anında statüye dokunmaz (`completed` agent'ın).

**Ana task'a QA hiç dokunmaz — ana task her zaman PA'nın.**

**8 · Agent PA'ya sorar** *"bittim, sıradaki ne"* → PA açık sub task'lardan atar
⚠️ Agent havuzdan **kendi iş almaz**

**9 · Tüm katmanlar `completed`** → PA kapanışı `in progress` alır → konsolide eder

---

# 5. Statü seti — ölçüldü, DEĞİŞMİYOR

Ana task ve sub task **aynı seti** kullanır. Mevcut set (18 statü, ClickUp'tan çekildi):

`Open` · `full stack` · `backend` · `front` · `ui` · `operations` · `planning` ·
`in progress` · `blocking` · `revise` · `test` · `pause` · `completed` · `pr` ·
`live - dev` · `ready for production` · `productıons` · `Closed`

**`test` ve `completed` yeni değil** — listede zaten vardı. `pause` da duruyor.
Genel ClickUp terimi ("To Do"/"Done") kullanılmıyor → `CLICKUP-STATUS-SET` yasağına
girmiyor.

**Statü listesi ClickUp'ta ne ise odur** — kanon ona müdahale etmez, olduğu gibi
kullanır. Listede insan developer'ların kullandığı statüler de var (`full stack`,
`backend`, `front`, `ui`, `operations`); bunlar agent'ları ilgilendirmiyor, akış
onları kullanmıyor, o kadar.

⚠️ **Bu bir "v7 artığı temizliği" DEĞİL.** v7/v8 ayrımı **agent kanonundaydı**, ClickUp
listesinde değil — liste canlı ve insanlar da kullanıyor. (Taslak v2'de bu yanlış
kurulmuştu: ölçümde görülen bir statü adı kanon tarihçesiyle eşleştirilip *"artık"* diye
okunmuştu. Mert düzeltti.)

---

# 6. Prod'a çıkış zinciri

```
completed  →  live - dev              operasyon testi bekliyor
           →  ready for production    operasyon testi yapıldı
           →  productıons             prod'a çıktı
```

**`productıons`'a çevirme görevi PA'nındır** — kapanışla birlikte.

## Prod'da elle yapılacak işler — ANA TASK YORUMU

Statü zinciri işin **hangi aşamada** olduğunu söyler; **o aşamada ne yapılması
gerektiğini** söylemez. O bilgi ayrı ve kaybolursa prod patlar.

**Ne girer** (ölçüt tek: prod'a çıkarken elle yapılacak bir iş mi?):
- **SQL** — dev'e uygulandı, prod'da henüz çalışmadı
- **Env / secret** — yeni key eklendi, prod'da yok (⚠️ **değeri yazılmaz**, yalnız key
  adı + nereye — `DO-NO-SECRET-IN-CODE`)
- **Manuel operasyon** — cache temizliği, cron durdurma/başlatma vb.

**Ortak yanları: üçü de kodda görünmez.** `git diff`'te yok, commit'te yok, hiçbir
modül dokümanında toplanmıyor.

**Nereye:** PA ana task'a **`PROD İŞLERİ`** başlıklı yorum düşer.

**Kim bildirir, kim yazar:**
- **QA** katman onayında bildirir (*"dev'e uygulandı / SQL YOK"*)
- **DO** env/secret eklediğinde bildirir (*"prod'da şu key gerekli"*)
- **PA yazar** — ikisi de yoruma kendi yazmaz

**Her not kimin bildirdiği + tarihle durur** — prod'da *"bu hâlâ geçerli mi"*
sorusunun cevabı.

⚠️ **Bildirilen not yazılmazsa prod'a kadar kaybolur — bilginin gelmesi yetmez.**
Ölçülmüş vaka (Egeli, 2026-07): QA prod SQL uyarısını **iki tur tekrarladı**, yazacak
yer olmadığı için PA kendi başlık açtı → dosya not defterine döndü.

Bu, kalkan `TASK-STATUS.md`'nin *"prod geçiş kontrol listesi"* işlevinin karşılığıdır.

---

# 7. Akışı ayakta tutan kurallar

## 7.1 Kanıt zorunlu — "bitti" beyandır, kayıt değildir

**Ölçüt: kanıt ROLE göre değil, ÇIKTI TÜRÜNE göre tanımlanır.**

- **Kod üreten** (BE/FE/MB/UID) → commit hash (*"local, push bekliyor"* işaretli)
- **Denetleyen** (QA) → onay handoff'u
- **Ölçen** (CA/TE) → rapor yolu + ölçüm sayısı
- **Canlıya çıkaran** (DO) → push hash

**Neden role göre değil:** roller her işte yok. TE her işte devreye girmez, UID
girmeyebilir. Rol bazlı liste yazılırsa girmeyen rolün satırı boş kalır ve kural
uygulanamaz görünür.

**UID'in ayrı kanıtı yoktur** — prototip kodunu commit'ler, QA denetler, onay döner.
Zincir zaten var.

Gerekçe (ölçüldü): BE *"iki catch düzelttim"* dedi, **sekizi duruyordu** — QA yakaladı.
Beyan vardı, kanıt yoktu.

## 7.2 Bağlam taşıma — İKİ YÖNLÜ yükümlülük

**PA yazar:** sub task açarken o katmanı ilgilendiren risk kararlarını **yorum** olarak
düşer. Açıklama **kapsamı**, yorum **dayanağı** taşır.

**Agent okur:** işe başlarken task'ın yorumlarını okuyacağını bilir.

⚠️ **Tek yönlü yazılırsa yorum düşer ama okunmaz.** Ölçüldü: PA discovery'yi yazdı, sub
task'ları açtı, ama discovery hiçbir yere bağlanmadı — **UID işi alınca *"kapsam var,
gerekçe yok"* dedi ve haklıydı.**

## 7.3 Yarım kalan iş — `pause` yorumu

İş `pause`'a alınırken yarım kaldıysa **agent task'a comment atar**: nerede kalındı, ne
yarım.

**Bu yüzden `DEVIR-{hedef}.md` KALKIYOR.** O dosyanın kanondaki gerekçesi *"bu bilgi
hiçbir kalıcı belgede yoktur"*tu — artık sub task'ın kendisi kalıcı belge.

## 7.4 Süre — statü süresi tracked'e işlenir

ClickUp statüde geçen süreyi **otomatik tutuyor.** Agent `completed` çektikten sonra
kendi **`in progress` süresini çeker** ve **tracked'e yazar. HESAPLAMAZ.**

**Mekanik (ölçüldü):**
- Çekme: `clickup_get_task_time_in_status` → statü geçmişini verir
- Yazma: `add_time_entry` → tracked alanına işler

Ölçülen örnek (PRC-36): `Open 1h 24m` · **`in progress 45m`** ← tracked'e yazılacak
sayı bu · `test 48m`

**Timer kullanılmaz** — ölçülmüş sebep: `gunluk/ev/2026-08-12-clickup-task-takip-testi.md:45`

✅ **Kapandı — v2'deki tutarsızlık açıklandı:** tracked'de `9569 ms` (9,5 sn) görünüyordu
ama `in progress` **45 dakikaydı.** Sebebi mekanizma arızası değil: **o değer testte bir
kez elle girildi.** Kural zaten bunu düzeltiyor — tracked'e elle değil, **statü
süresinden** yazılır.

## 7.5 Sıra PA'da

Agent havuzdan kendi iş almaz. Bitirince PA'ya sorar, PA atar.

---

# 8. Düşen kurallar — DÖRT tane (v1'de bir tane sanılıyordu)

**1 · `CLICKUP-PA-ONLY-WRITE`** → kapsamı daralıyor (kalkmıyor)

**2 · `CLICKUP-ROLE-STATUS`** → tablo yeniden yazılıyor. Mevcut hâli *"BE/FE/MB/UID/QA/
DO/TE/CA statü SET ETMEZ"* diyor; yeni akışta agent kendi sub task'ını çeviriyor.

**3 · `CLICKUP-TRACE-ACTION-APPROVAL`** → sub task açmak artık ayrı onay istemiyor
(PA serbest). Ana task açmak kullanıcı onayına tabi kalıyor.

**4 · `QA-APPROVE-ATOMIC`** → kural *"onay = STATUS + handoff + PA bilgi, ayrılamaz"*
diyor. `status.md` kalktığı için "STATUS" bileşeni düşüyor; geriye onay handoff'u +
PA bilgi kalıyor.

---

# 9. Kural nereye yazılır — İKİ AYRI İŞ

## 9.1 Akış → `is-akisi` (TEK KAYNAK)

ClickUp adımları **`is-akisi`'nde tek yerde** tanımlanır: hangi statü ne zaman çevrilir,
kim neye dokunur, sıra nasıl ilerler.

**Neden burası:** `is-akisi` zaten dokuz agent'ın `skills:` listesinde (ölçüldü) ve
zaten *"kim kime ne verir, sıra nasıl ilerler"* diyor. ClickUp adımı bu akışın parçası,
ayrı bir konu değil.

**Omurga skill'ler** (`backend` · `frontend` · `mobile` · `quality` · `devops` ·
`ui-designer` · `test-engineer` · `code-auditor` · `project-assistant`) buraya
**ATIF verir — kopyalamaz.**

⚠️ **Neden kopyalanmaz:** aynı kural dokuz yere yazılırsa değişince dokuz dosya
güncellenmeli; biri unutulursa **sessizce sapar.** Fabrikada bu ölçülmüş bir arıza
deseni (yarım cascade — `plugin-dagitim/SKILL.md`, 2026-08-11).

## 9.2 Mekanik → `clickup` skill'i GENELE ÇEVRİLİR

`clickup/SKILL.md` bugün **baştan sona PA diliyle** yazılmış: backlog temizliği,
operasyon köprüsü, discovery task'ı, sprint taraması. Olduğu gibi dağıtılırsa her
developer PA'nın işini de okumuş olur.

**Yapılacak: skill genel dile çevrilir — *"ClickUp nasıl kullanılır"*.**

İçine girecek olan mekanik (rol-nötr):
- Bir task nasıl bulunur, ID nereden okunur
- Statü nasıl çevrilir (çağrı, alan, değer biçimi)
- Yorum nasıl yazılır / okunur
- Süre nasıl çekilir (`get_task_time_in_status`) ve nasıl yazılır (`add_time_entry`)
- ⚠️ **Yazma çağrısının dönüşü ölçüm değildir** — sonucu okuyarak doğrula
  (ölçülmüş: `description` boş göründü/doluydu, `custom_id` null geldi/atanmıştı)
- **Bir task'ın açıklaması yoksa dokümanı vardır** — oraya bakılır

PA'ya özel kalanlar (backlog, sprint, discovery task'ı, prod köprüsü) skill içinde
**ayrı bir bölümde** durur ya da PA omurgasına taşınır.

## 9.3 Araç durumu — ÖLÇÜLDÜ, sorun yok

Dokuz agent'ın frontmatter'ında **araç kısıtı yok**: hepsinde tek satır
`disallowedTools: Workflow`. Yani ClickUp MCP dahil her araç açık.

Sahada da doğrulandı: UID, BE ve PA statü çevirdi, çalıştı. Tek engel `settings.json`
izin katmanıydı, o da açıldı.

⚠️ **Ölçümde çıkan ek bulgu:** `clickup` skill'i **PA'nın bile `skills:` listesinde
YOK.** PA'nın listesi: `behavior · handoff · memory-management · is-akisi ·
pr-yazilim-oy-envanteri · project-assistant`. Skill dosyası var ama kimsenin çantasında
değil — `description`'daki *"clickup"* kelimesiyle tetikleniyor olabilir.

---

# 10. Kapsam

**Bu düzen OY (özel yazılım) içindir.** Websitesi (WS) kanonu **kapsam dışı** — önce
OY'da çalışır hâle getirilecek, sonra WS'e geçilecek.

## ⚠️ Cascade — 21 dosya

`status.md` / `STATUS.md` / `TASK-STATUS` OY kanonunda **21 dosyada** geçiyor
(PAM ölçtü; v1'de 16 sanılıyordu).

Yoğunluk: `proje-dosya-duzeni/SKILL.md` **20 hit** · `orkestrasyon/SKILL.md` 9 ·
`proje-dosya-duzeni/references/mekanik.md` 7

v1'de atlanan beş dosya: `behavior/references/git-komut-detay.md` ·
`commit-review/references/cr-serisi-detay.md` · `is-akisi/references/devops-is-akisi.md` ·
`memory-management/references/icerik-turleri.md` · `proje-islemleri/SKILL.md`

**Tek dosya silme işi değil — cascade.** Yarım kalan cascade fabrikada daha önce bulgu
olmuştu (`plugin-dagitim/SKILL.md`, 2026-08-11).

---

# 11. Açık kalan ölçüm

**Yok.** v2'deki tek açık kalem (süre tutarsızlığı) kapandı — sebebi elle girilen bir
değerdi, mekanizma arızası değil (7.4).

⚠️ Tek bilinen boşluk: **`QA-STATUS-GIT-EVENTS`** — `status.md` kalkınca QA'nın Actions
sonucu nereye yazılacak? Push olayı zaten statüde görünüyor (7b: QA sub task'ı
`live - dev`'e alır); Actions sonucu için yorum yeterli mi, PAM değerlendirmeli.

---

# Kaynaklar

- PAM'in 18 sorusu + cevapları: `fikirler/agent-is-akisi/pam-sorulari.md`
- Saha testi: `gunluk/ev/2026-08-12-clickup-task-takip-testi.md`
- Kapsam daraltma: `kararlar/2026-08-12-clickup-yazma-yetkisi-kapsam-daraltma.md`
- Dosya kaldırma: `kararlar/2026-08-12-task-status-ve-status-md-kalkiyor.md`
- Clara kanona girmiyor: `kararlar/2026-08-12-clara-oy-kanonuna-girmiyor.md`
- Mevcut dosya düzeni kanonu: `skill-project/v8/ozel-yazilim/.claude/skills/proje-dosya-duzeni/SKILL.md`
