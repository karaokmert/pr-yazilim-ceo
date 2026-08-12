# GEREKSİNİM — OY ClickUp task takip düzeni

**Tarih:** 2026-08-12 · **Kaynak:** Clara (yönetim) · **Hedef:** PAM (fabrika)
**Kapsam:** Özel Yazılım (OY). Websitesi kapsam dışı — sonra.

---

# 1. Ne isteniyor

OY projelerinde bir işin **kaydı dosyadan ClickUp'a taşınıyor**, ve bu taşınma
agent'ların ClickUp yazma yetkisini de değiştiriyor.

Bu düzen sahada kuruldu ve beş agent'la (PA/UID/BE/FE/QA) canlı test edildi. Test
sırasında mevcut kanon **oturuma özel askıya alındı** — kalıcı değil. Kanonun ne
diyeceği karara bağlanmazsa her projede aynı istisna yeniden açılır ve kural fiilen
ölür.

---

# 2. Kayıt yeri: ClickUp

## Kalkan dosyalar

- `_project/TASK-STATUS.md`
- `{modul}/{task}/status.md`
- `{modul}/{task}/DEVIR-{hedef}.md`

## Olay akışı nereye gidiyor — ClickUp'a DEĞİL

⚠️ **ClickUp'ta task YALNIZ STATÜ tutar.** Olay akışı ClickUp'a yazılmaz.

**Olay akışı her agent'ın kendi memory'sine gider:** agent memory index'inde
**`İŞLER`** diye bir index açar, altına iş statülerini yazar.

**Kapanışta memory düzenlenir:** iş biterken kayıt **kazanıma** ya da **biten işe**
çevrilir. Olay günlüğü birikmez, **akar** — `status.md`'nin *"not defterine dönme"*
arızası baştan engellenir.

**Yorum yalnız önemli durum için yazılır** — her olay için değil.

**Yorum daima yazan agent'ın adını içerir.** Gerekçe (ölçüldü): ClickUp yorumları
**tek kullanıcı adıyla** gidiyor. Dokuz agent yorum düşse hepsi aynı isimle görünür —
ad yazılmazsa kimin yazdığı ayırt edilemez, **kayıt sahipsiz kalır.**

## `HANDOFF-STATUS-OWN-EVENTS` — hükmü kalır, nesnesi değişir

Kimlik: *"Her agent STATUS'a yalnız kendi olayını yazar; başkasının olayına dokunmaz.
STATUS'u PA commit'ler."* (`handoff/SKILL.md:113` — sekiz dosya atıf veriyor, **dokuz
agent'ın ortak kuralı**)

**Hüküm aynen kalır.** Nesnesi değişir: STATUS dosyası değil, **agent'ın kendi
memory'si.**

Ve nesne değişince kural **daha güçlü** oluyor: kendi memory'sine zaten başkası
yazamaz. Önce paylaşılan bir dosyada disiplinle korunan şey, artık **yapısal olarak**
garanti.

*"STATUS'u PA commit'ler"* kısmı düşer — commit'lenecek dosya yok.

`DEVIR-*.md` için ayrıca: o dosyanın kanondaki gerekçesi *"bu bilgi hiçbir kalıcı
belgede yoktur"*tu. Artık sub task'ın kendisi kalıcı belge — yarım kalan iş `pause`
yorumuyla kayda geçiyor (§6.3).

## Geçiş

**Tüm projelerde kullanılır.** Yeni task'lar bu düzenle ilerler.

**Eski task'lar** mevcut dosyalarında yaşamaya devam eder; PA bir süre ikisini birden
kontrol eder. **Agent'lar bu dosyalara artık yazmaz** — yeni işin kaydı ClickUp'a gider.

---

# 3. Sub task yapısı

## Başlık formatı — ZORUNLU

```
[FE] PRAG - Randevu Müsaitlik - Takvim Görünümü
[BE] PRAG - Randevu Müsaitlik - Şablon, Slot Üretimi
[PA] PRAG - Randevu Müsaitlik - Discovery
```

**Kural:** *"Başlık `[SENİN-KISALTMAN]` ile başlamıyorsa o task'a dokunma."*

**Kısaltmalar:** `PA` · `BE` · `FE` · `MB` · `DO` · `QA` · `TE` · `CA` · `UID`

**Gerekçe:** sahiplik ölçülebilir olmalı. Alan sırasına dayanan formatlarda (`PROJE -
MODÜL - AGENT - başlık`) modül adında bir tire geçerse **alan kayar** ve kural sessizce
yanlış task'ı işaret eder. `startswith` ölçümü ayraç sayısından bağımsızdır.

**`assignee` alanı KULLANILMAZ.** Ölçüldü: sahadaki beş sub task'ın hepsinde
`assignees: []`. Sahiplik başlıktan okunur.

## Kaç sub task

**Sabit:** PA'nın iki sub task'ı — **discovery** ve **kapanış**.
**Değişken:** discovery'den çıkan her katman için bir sub task.

```
{ana task}
  ├─ [PA]  Discovery      SABİT
  ├─ [UID] Mock           ┐
  ├─ [BE]  Contract       ├ discovery'den çıkar, sayısı işe göre değişir
  ├─ [FE]  Ekran          ┘
  └─ [PA]  Kapanış        SABİT — baştan açılır, Open durur
```

Katman sub task'ları **discovery'den SONRA** açılır: hangi katmanların gireceği
discovery'den çıkar, önce bilinemez. Bir işte MB/DO/TE/CA girmeyebilir.

**PA'nın iki sub task'ının gerekçesi (ölçüldü):**

*Discovery:* PA bir işin ilk turunda 78 dakika çalıştı — discovery yazdı, üç tur soru
sordu, sub task açtı, yorum düştü — ve **ClickUp'ta tek izi yoktu.** *"PA ne yapıyor"*
sorusunun cevabı hiçbir kayıtta değildi.

*Kapanış:* baştan açılır ve `Open` durur. **Bu bir görünürlük kaydı değil, bir kapı** —
kapanış kutusu açıkken kimse *"bitti"* diyemez. Sahada en sık kaybolan iş **bitmiş ama
kapanmamış** iştir.

---

# 4. Kim neye dokunur

**Ana task'ı `kullanıcı` açar.** Task yoksa PA'ya açtırır, kullanıcı onayıyla.
**Sub task'ları PA serbestçe açar** — ayrı onay gerekmez.

**Ana task her zaman PA'nındır.** Statüsünü yalnız PA çevirir.

**Agent yalnız kendi sub task'ının statüsünü çevirir.**

**Mutlak yasak:** ana task · başkasının sub task'ı · `Closed` · `revise` · task silme

**QA'nın tek statü yetkisi:** push ettiği **sub task**'ı `live - dev`'e alır (§5, adım 7b).
Onay anında statüye dokunmaz — `completed`'ı agent çeker.

---

# 5. Akış

**1 ·** PA işi alır → ana task `in progress` + kendi discovery sub task'ı `in progress`

**2 · Gereksinim netleştirme — `kullanıcı` ↔ PA, DÖNGÜSEL**

PA discovery'yi soru sormadan yazmaz (`PA-DISC-RISK-CLOSE` / `PA-DISC-NO-TBD`). Açık
riskleri `kullanıcı`ya sorar; cevaplar **yeni sorular doğurur**, tekrar sorar.

Ölçülen tur: 6 risk → 5 türev soru → 5 daha = **11 madde karara bağlandı, TBD sıfır.**
Örnek: *"slot süresi değişince mevcut randevular ne olur"*, *"sekreter görebilir dedin —
randevu ALABİLİR mi"*. Hepsi **iş kararı**: developer'a devredilemez, PA uyduramaz.

PA cevabı doğrudan dokümana çevirmez (`PA-DISC-ANSWER-NOT-REQUIREMENT`).

**3 ·** Discovery biter → `completed` (kanıt: doküman yolu + commit)
→ katman sub task'ları + kapanış açılır

**4 ·** Agent PA'dan handoff alır → hangi task'ı yapacağını **handoff'tan okur** →
`in progress` çeker

**5 ·** Agent bitirir → `test` çeker (QA'ya devrediyor)

**6 ·** QA denetler
- **ONAY** → onay handoff'u yazar, statüye dokunmaz
- **RED** → `revise`'a alır → agent düzeltirken `in progress` çeker → bitince yine `test`

**7 ·** Agent QA onayını alınca `completed` çeker

**7b ·** QA push ettiğinde push'ladığı sub task'ı `live - dev`'e alır

**8 ·** Agent PA'ya sorar *"bittim, sıradaki ne"* → PA açık sub task'lardan atar.
**Agent havuzdan kendi iş almaz.**

**9 ·** Tüm katmanlar `completed` → PA kapanışı `in progress` alır → konsolide eder

---

# 6. Kurallar

## 6.1 Kanıt zorunlu — "bitti" beyandır, kayıt değildir

**Kanıt ROLE göre değil, ÇIKTI TÜRÜNE göre tanımlanır:**

- **Kod üreten** (BE/FE/MB/UID) → commit hash (*"local, push bekliyor"* işaretli)
- **Denetleyen** (QA) → onay handoff'u
- **Ölçen** (CA/TE) → rapor yolu + ölçüm sayısı
- **Canlıya çıkaran** (DO) → push hash

**Neden role göre değil:** roller her işte yok. TE her işte devreye girmez, UID
girmeyebilir. Rol bazlı liste yazılırsa girmeyen rolün satırı boş kalır.

**UID'in ayrı kanıtı yoktur** — prototip kodunu commit'ler, QA denetler, onay döner.

**Gerekçe (ölçüldü):** BE *"iki catch düzelttim"* dedi, **sekizi duruyordu** — QA
yakaladı. Beyan vardı, kanıt yoktu.

## 6.2 Bağlam taşıma — İKİ YÖNLÜ yükümlülük

**PA yazar:** sub task açarken o katmanı ilgilendiren risk kararlarını **yorum** olarak
düşer. Açıklama **kapsamı**, yorum **dayanağı** taşır.

**Agent okur:** işe başlarken task'ın yorumlarını okuyacağını bilir.

**Tek yönlü yazılırsa yorum düşer ama okunmaz.** Ölçüldü: PA discovery'yi yazdı, sub
task'ları açtı, ama discovery hiçbir yere bağlanmadı — **UID işi alınca *"kapsam var,
gerekçe yok"* dedi.**

## 6.3 Yarım kalan iş — `pause` yorumu

İş `pause`'a alınırken yarım kaldıysa **agent task'a comment atar**: nerede kalındı,
ne yarım.

## 6.4 Süre — statü süresinden tracked'e

ClickUp statüde geçen süreyi otomatik tutuyor. Agent `completed` çektikten sonra kendi
**`in progress` süresini çeker** ve **tracked'e yazar. HESAPLAMAZ.**

Mekanik: çekme `clickup_get_task_time_in_status` · yazma `add_time_entry`

Ölçülen örnek: `Open 1h 24m` · **`in progress 45m`** ← tracked'e yazılacak sayı ·
`test 48m`

**Timer kullanılmaz.**

## 6.5 Sıra PA'da

Agent havuzdan kendi iş almaz. Bitirince PA'ya sorar, PA atar.

---

# 7. Statü seti

Ana task ve sub task **aynı seti** kullanır. Set ClickUp'ta tanımlı olandır; kanon ona
müdahale etmez.

`Open` · `full stack` · `backend` · `front` · `ui` · `operations` · `planning` ·
`in progress` · `blocking` · `revise` · `test` · `pause` · `completed` · `pr` ·
`live - dev` · `ready for production` · `productıons` · `Closed`

Listede insan developer'ların kullandığı statüler de var (`full stack`, `backend`,
`front`, `ui`, `operations`) — akış onları kullanmaz, agent'ları ilgilendirmez.

Genel ClickUp terimi ("To Do"/"Done") kullanılmaz.

---

# 8. Prod'a çıkış

```
completed  →  live - dev              operasyon testi bekliyor
           →  ready for production    operasyon testi yapıldı
           →  productıons             prod'a çıktı
```

**`productıons`'a çevirme görevi PA'nındır** — kapanışla birlikte.

## Prod'da elle yapılacak işler → ANA TASK YORUMU

Statü işin **hangi aşamada** olduğunu söyler; **o aşamada ne yapılması gerektiğini**
söylemez. O bilgi ayrıdır ve kaybolursa prod patlar.

**Ne girer** (ölçüt tek: prod'a çıkarken elle yapılacak bir iş mi?):
- **SQL** — dev'e uygulandı, prod'da henüz çalışmadı
- **Env / secret** — yeni key eklendi, prod'da yok (**değeri yazılmaz**, yalnız key adı
  + nereye — `DO-NO-SECRET-IN-CODE`)
- **Manuel operasyon** — cache temizliği, cron durdurma/başlatma

**Ortak yanları: üçü de kodda görünmez.** `git diff`'te yok, commit'te yok, hiçbir modül
dokümanında toplanmıyor.

**Nereye:** PA ana task'a **`PROD İŞLERİ`** başlıklı yorum düşer.

**Kim bildirir:** QA katman onayında (*"dev'e uygulandı / SQL YOK"*) · DO env/secret
eklediğinde (*"prod'da şu key gerekli"*). **İkisi de yoruma kendi yazmaz — PA yazar.**

**Her not kimin bildirdiği + tarihle durur** — prod'da *"bu hâlâ geçerli mi"* sorusunun
cevabı.

**Gerekçe (ölçülmüş vaka, Egeli 2026-07):** QA prod SQL uyarısını **iki tur
tekrarladı**, yazacak yer olmadığı için PA kendi başlık açtı → dosya not defterine
döndü. **Bildirilen not yazılmazsa prod'a kadar kaybolur; bilginin gelmesi yetmez.**

---

# 9. Kural nereye yazılır — İKİ AYRI İŞ

## 9.1 Akış → `is-akisi` (TEK KAYNAK)

Hangi statü ne zaman çevrilir, kim neye dokunur, sıra nasıl ilerler — **tek yerde.**

**Neden:** `is-akisi` zaten dokuz agent'ın `skills:` listesinde (ölçüldü) ve zaten
*"kim kime ne verir"* diyor. ClickUp adımı bu akışın parçası.

**Omurga skill'ler** (`backend` · `frontend` · `mobile` · `quality` · `devops` ·
`ui-designer` · `test-engineer` · `code-auditor` · `project-assistant`) buraya **atıf
verir, kopyalamaz.**

**Neden kopyalanmaz:** aynı kural dokuz yere yazılırsa değişince dokuz dosya
güncellenmeli; biri unutulursa **sessizce sapar.**

## 9.2 Mekanik → `clickup` skill'i GENELE ÇEVRİLİR

`clickup/SKILL.md` bugün **baştan sona PA diliyle** yazılmış (backlog temizliği,
operasyon köprüsü, discovery task'ı, sprint taraması). Olduğu gibi dağıtılırsa her
developer PA'nın işini de okumuş olur.

**Skill *"ClickUp nasıl kullanılır"* olarak genel dile çevrilir.** İçine girecek
mekanik (rol-nötr):

- Bir task nasıl bulunur, ID nereden okunur
- Statü nasıl çevrilir (çağrı, alan, değer biçimi)
- Yorum nasıl yazılır / okunur
- Süre nasıl çekilir ve nasıl yazılır
- **Yazma çağrısının dönüşü ölçüm değildir** — sonucu okuyarak doğrula. Ölçüldü:
  `description` boş göründü (doluydu), `custom_id` null geldi (atanmıştı). Özet/create
  yanıtları eksik alan döndürebiliyor; düzeltmeye koşulsaydı var olan açıklamaların
  üstüne yazılacaktı.
- **Bir task'ın açıklaması yoksa dokümanı vardır** — oraya bakılır

PA'ya özel kalanlar (backlog, sprint, discovery task'ı, prod köprüsü) skill içinde ayrı
bir bölümde durur ya da PA omurgasına taşınır.

## 9.3 Araç durumu

**Kısıt yok.** Dokuz agent'ın frontmatter'ında tek satır: `disallowedTools: Workflow`.
ClickUp MCP dahil her araç açık.

Sahada doğrulandı: UID, BE ve PA statü çevirdi, çalıştı.

⚠️ `clickup` skill'i bugün **hiçbir agent'ın `skills:` listesinde yok** — PA'da bile.
PA'nın listesi: `behavior · handoff · memory-management · is-akisi ·
pr-yazilim-oy-envanteri · project-assistant`.

---

# 10. Etkilenen kanon

## Düşen / değişen kurallar

**`CLICKUP-PA-ONLY-WRITE`** — kalkmıyor, **kapsamı daralıyor.** Agent kendi sub task'ına
dokunur; ana task, başkasının task'ı, `Closed`, `revise`, silme mutlak yasak kalır.

⚠️ **Kural YANLIŞ olduğu için değil, DAYANDIĞI GERÇEK DEĞİŞTİĞİ için düşüyor.**

Kuralın kendi metni gerekçesini bir **araç kısıtına** bağlıyor: *"v8'de `clickup` skili
BE/FE/MB/UID'in çantasında YOK (ölçüldü: 4 agent body'sinde 0 hit) — yani statü set etme
görevi verilse **fiilen yapılamaz**."*

**O kısıt kalkmış** (§9.3: dokuz agent'ta araç kısıtı yok) ve sahada üç agent statü
çevirmiş.

**Yerine geçecek şey *"PA-ONLY kalksın"* DEĞİL:**
> *"Yetki artık ARAÇ KISITIYLA değil SAHİPLİKLE çiziliyor."*

Ayrımın önemi: talimat bir oturumun içinde yaşar, **mekanizma yaşamaz.** Bugünkü test
kuralın *"kullanıcı talimatıyla da AÇILMAZ"* maddesine rağmen o yoldan yürüdü — sınır
sahiplikle çizilirse istisnaya ihtiyaç kalmıyor.

**`CLICKUP-ROLE-STATUS`** — tablo yeniden yazılıyor. Mevcut hâli *"BE/FE/MB/UID/QA/DO/
TE/CA statü SET ETMEZ"* diyor.

**`CLICKUP-TRACE-ACTION-APPROVAL`** — sub task açmak ayrı onay istemiyor (PA serbest).
Ana task açmak kullanıcı onayına tabi kalıyor.

**`QA-APPROVE-ATOMIC`** — *"onay = STATUS + handoff + PA bilgi, ayrılamaz"* diyor.
`status.md` kalktığı için STATUS bileşeni düşüyor.

**`QA-STATUS-GIT-EVENTS`** (`quality/SKILL.md:169`) — *"QA kendi git olaylarını
STATUS'a yazar."* ⚠️ **Bu kalem karara bağlanmadı.** Push olayı artık statüde görünüyor
(§5 adım 7b), ama **Actions sonucu** nereye yazılacak? Değerlendirme PAM'de.

## Cascade — 36 dosya (üç eksenden ölçüldü)

| Eksen | Dosya |
|---|---|
| Dosya adı (`status.md` / `STATUS.md` / `TASK-STATUS`) | 21 |
| STATUS **kavramı** (tarif cümleleri — dosya adı anılmıyor) | 35 |
| `DEVIR-` dosyası | 6 |
| **Birleşik** | **36** |

⚠️ **Dosya adı ekseni yetmiyor:** kimliği ya da dosya adını anmayan **tarif cümleleri**
hiçbir aramaya düşmüyor. Gözden kaçan 15'in içinde `quality/SKILL.md` var — açık kalemin
yaşadığı yer.

Kavram ekseninde çıkan ek dosyalar: `quality/SKILL.md` ·
`is-akisi/references/qa-engineer-is-akisi.md` · `project-assistant/SKILL.md` ·
`behavior/SKILL.md` · `devops/SKILL.md` · `mobile/SKILL.md` · `ui-designer/SKILL.md`

Yoğunluk: `proje-dosya-duzeni/SKILL.md` **20 hit** · `orkestrasyon/SKILL.md` 9 ·
`proje-dosya-duzeni/references/mekanik.md` 7

Diğerleri: `behavior/references/git-komut-detay.md` ·
`commit-review/references/cr-serisi-detay.md` ·
`is-akisi/references/{backend,frontend,mobile,devops,ui-designer}-is-akisi.md` ·
`memory-management/references/{icerik-turleri,kapanis}.md` · `proje-islemleri/SKILL.md` ·
`handoff/SKILL.md` + `references/handoff-ornekleri.md` · `clickup/references/
clickup-workflows.md` · `commit-review/SKILL.md` · `ui-designer/SKILL.md`

**Tek dosya silme işi değil — cascade.** Her dosyada `status.md`'nin *işlevsel bağımlı*
mı yoksa sadece *anılan* mı olduğu ayrılmalı; ilkinde kural değişir, ikincisinde yol
düzeltmesi yeter.
