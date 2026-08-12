# PAM'in soruları — iş akışı taslağı testi

**Tarih:** 2026-08-12 17:04 · **Test:** `is-akisi-taslak.md` PAM'e okutuldu
**Sonuç:** *"Hayır. Cevap beklemem gerekiyor."* — 18 soru

⚠️ **Bu bir ÖLÇÜMDÜR, iş devri değil.** PAM rolündeki isimsiz bir yardımcıya taslak
okutuldu, *"ne anladın, ne sorman gerekir, kanon yazabilir misin"* diye soruldu.
Niyet taşınmadı — doküman savunulmadı, iyileştirme istenmedi.

**Nasıl kullanılır:** her sorunun altında `### CEVAP` alanı var. Oraya yaz.
`[MERT]` işaretli olanlar senin kararın; `[CLARA]` bende; `[ÖLÇÜM]` ev Clara'sının
mekanizma cevabını bekliyor.

---

# PAM'in genel hükmü

> *"Hayır, kanon yazamam. Cevap beklemem gerekiyor. Gerekçem üç maddede, ve bunlar
> 'eksik detay' değil, **yazma biçimini belirleyen** açıklar."*

Üç gerekçesi:
1. Clara sorusu kanonun **iskeletini** belirliyor
2. Mekanizma sorusu kuralın **ölçülebilirliğini** belirliyor
3. Mevcut kanonla çatışmaların **bilinçli mi kaza mı** olduğu bilinmiyor

**Yazmaya başlayabileceği tek parça:** cascade envanteri (21 dosyanın hangisi
işlevsel bağımlı, hangisi sadece anıyor). Onay isterse paralelde çıkarabileceğini
söyledi. ⚠️ Bu bir ÜRETİM — ona iş vermek olur, devir bloğu gerekir.

---

# GRUP 1 — Clara (iskeleti belirliyor)

## 1 · Clara OY kanonunda rol olarak tanımlanacak mı? `[CLARA]`

Akışın 2., 4. ve 5. adımı Clara'ya bağlı ama OY kadrosu dokuz rol ve Clara hiçbiri değil.

PAM: *"Clara bir agent mı, bir insanın adı mı, yoksa 'kullanıcı' rolünün bu bağlamdaki
adı mı — bilmiyorum, ve tahmin etmiyorum çünkü üç ihtimal üç farklı kanon metni demek."*

### CEVAP
Mert 2026-08-12'de karar verdi: **kanona GİRMEZ.** Clara perde arkasında kalır,
agent'a giden her şey `kullanıcı`dan geliyor gibi görünür.
Karar: `kararlar/2026-08-12-clara-oy-kanonuna-girmiyor.md`
→ Taslakta her `Clara` ifadesi `kullanıcı` olacak.

- Clara Sadece bana özel ve bbenim pc de çalışan bir agent. Benim yapmam gerkeen işleri birlikte yapıyoruz. Bu nedenle clara yerine sadece kullanıcı bilgisi yazılır. 

## 2 · Clara yoksa akış ne oluyor? `[CLARA]`

OY agent'ları başka kullanıcılarca da çalıştırılıyor (`BEHAVIOR-KNOW-USER`). Kanona
"Clara" yazılırsa Clara'sız her oturumda kural askıda kalır.

PAM kendi cevabını da önerdi: *"Clara'nın yaptığı işlerin kanondaki karşılığı zaten
'kullanıcı' olabilir — o zaman kanon 'kullanıcı' der, Clara özel bir kullanıcıdır."*

⚠️ PAM'in yakaladığı tuzak: *"dokümanın kendisi tam bu tuzağa dikkat çekiyor —
'kural kendisini askıya alacak meşru bir yol tanımlamadı'. **Aynı hatayı ters yönden
yapmak istemiyorum.**"*

### CEVAP
PAM'in önerisi doğru ve Mert'in kararıyla örtüşüyor: kanon `kullanıcı` der.
→ Soru 1 ile birlikte kapandı.

---

# GRUP 2 — Mevcut kanonla çatışma (PAM ölçtü)

## 3 · `CLICKUP-ROLE-STATUS` tablosu tamamen yeniden mi yazılıyor? `[CLARA]`

Mevcut kanon (`clickup/SKILL.md:38-42`): *"BE/FE/MB/UID/QA/DO/TE/CA → statü SET ETMEZ.
Durumu handoff'la PA'ya bildirirler, PA çeker."* Doküman ise agent'ın kendi sub task'ını
çevirdiğini söylüyor — **doğrudan çelişki.**

PAM: *"Doküman yalnız `CLICKUP-PA-ONLY-WRITE`'ı etkilenen kural olarak anıyor, ama
`CLICKUP-ROLE-STATUS` da düşüyor. Bu bilinçli mi?"*

### CEVAP
Evet, bilinçli — ama taslakta yazılmamıştı, **Clara'nın eksiği.** Kapsam daraltma
kararı bu tabloyu da değiştiriyor. Gereksinime yazılacak.

Main Taskin yönetimi daima pa da pa discovery. yazdıktan sonra hangi agentlara iş verecekse onlar için sub task açar. Sub task bir status.md takibi gibidir. 

Agent işe başlarken pa dan sub task handoff u alır. Hangi taski yapacağını handoffdan okur. 

taski başaldığında inprogress e alır taski bitirince test statusune alıp qa e devret 

qa taski revizeye alır agent işi yaparken tekrar in progress e alır. 

QA e gidekren yine teste alır. QA onay handoff u verdiğinde agent taskini completede a alır ve bitti ve in progress süresini set time olarak taske işler bu taske ne kadar vakit harcağını bildirmiş olur. süre click up dan alınmalıdır. 

## 4 · Statü seti değişiyor mu? `[MERT]`

Mevcut set: `Open · planning · in progress · pause · live - dev · ready for production ·
productıons · revise · Closed`

Dokümandaki akışta **`test` ve `completed` var, `pause` yok.**

⚠️ PAM'in uyarısı: *"`test`/`completed` yeni statüler mi, sub task'lara özel ayrı bir
set mi? Genel ClickUp terimlerini kullanıyorsa **kanon yasağına giriyor** —
`CLICKUP-STATUS-SET` genel ClickUp statülerini ('To Do'/'Done') açıkça yasaklıyor."*

Ek soru: ana task ve sub task **farklı statü setleri** mi kullanıyor? `pause`'un yerini
`test` mi aldı?

### CEVAP

hayır hepsi aynı statuleri kullanıyor. MAin Task sadece bu hale geliyordu. 

ama sub taskler geldi. ve task listesi güncellendi. 

PRY-17371 bu taskin geçebileceği statuslere bakılarak örnek olsun diye task status listemiz kontrol edilebilir ve isimleri güncellenebilir.

---
**CLARA ÖLÇÜMÜ (17:2x, ClickUp'tan doğrudan — `expand_statuses`):**

Onaylıyorum, haklısın. `Task Denemesi` listesinin tam seti **18 statü**:

`Open` · `full stack` · `backend` · `front` · `ui` · `operations` · `planning` ·
`in progress` · `blocking` · `revise` · **`test`** · `pause` · **`completed`** ·
`pr` · `live - dev` · `ready for production` · `productıons` · `Closed`

- `test` ve `completed` **zaten vardı** — PAM'in "yeni statü mü" endişesi yersiz
- `pause` **kaldırılmadı**, akış onu kullanmıyor sadece
- Ana task ve sub task **aynı seti** kullanıyor
- Genel ClickUp terimi yok → `CLICKUP-STATUS-SET` yasağına girmiyor

⚠️ **Kimsenin sormadığı bulgu — sette v7 artığı duruyor:**
`full stack` · `backend` · `front` · `ui` · `operations`

Bunlar **insan developer'lar** içindi ve kaldırılan `CLICKUP-ROLE-STATUS`'un gerekçesi
tam buydu (*"tablo v7'den gelmişti"*). Sette duruyorlar ve **hiçbir kanon onları
yasaklamıyor** — bir agent yanlışlıkla `front` çekebilir.

→ Senin "isimleri güncellenebilir" notunla birleşiyor: bu beş statü **silinmeli ya da
kanonda açıkça yasaklanmalı.** 


## 5 · `CLICKUP-TRACE-ACTION-APPROVAL`'ın sırası tersine mi dönüyor? `[CLARA]`

Mevcut kanon sub task açmayı ve yorum yazmayı **açık kullanıcı onayı zorunlu** iz-bırakan
aksiyon sayıyor.

Yeni akışta: PA discovery biter bitmez sub task'ları açıyor (adım 3), yorumları düşüyor
(6.2), ve **onay adım 4'te sonra geliyor.**

PAM: *"Sıra tersine mi dönüyor, yoksa PA açmadan önce mi onay alıyor?"*

### CEVAP

Main taskler artık benim tarafımdan açılıyor. Kullanıcı açıyor. Eğer task yoksa pa ya açtırıyorum. Bu noraml benim oanyımla açılıyor. Sub taskler ise pa ya serbest 


## 6 · Statü tarafı gevşiyor — OKUMA tarafı ne oluyor? `[ÖLÇÜM]`

Mevcut kanon `CLICKUP-PA-ONLY-WRITE`'ın *"ClickUp'ı yalnızca PA okur/yazar"* hükmünün
statü tarafı olduğunu söylüyor — ikisi aynı hüküm.

PAM: *"Şimdi statü tarafı gevşiyor — **okuma** tarafı ne oluyor? Agent kendi sub task'ını
okuyabilecek mi? Okuyamıyorsa statüsünü nasıl çevirecek, ID'sini nereden alacak?"*

### CEVAP
Mekanizma ölçümüne bağlı (ev Clara'sına 16:06'da soruldu).

## 7 · `clickup` skili kimin çantasına giriyor? `[MERT]`

Ölçülmüş durum: skill BE/FE/MB/UID'in çantasında **YOK** (4 agent body'sinde 0 hit) —
ve bu, kaldırılan kuralın gerekçelerinden biriydi.

PAM: *"Agent artık statü çevirecekse bu skil sekiz agent'ın çantasına mı giriyor, yoksa
`is-akisi` referanslarına gömülü **minimal bir bölüm** mü yazılıyor? Bu, kanonun nereye
yazılacağını belirliyor."*

### CEVAP
is-akisinda bu açıkca yazmalı. Click up skill bu sisteme göre güncellenmeli ve click up skill i iş akışına tanımlanmalı. bu sayede her agent ulaşabilir olmalı. 

Click up yönetimi skill inde bir taskin açıklaması yoksa dokumanı vardır kısmı belirtilmeli. 

---

# GRUP 3 — Cascade kapsamı

## 8 · Cascade 16 değil 21 dosya — hangisi doğru? `[CLARA]`

PAM ölçtü ve Clara'nın sayımını çürüttü. **21 dosya**, Clara'nın listelemediği beşi:
- `behavior/references/git-komut-detay.md`
- `commit-review/references/cr-serisi-detay.md` (5 hit)
- `is-akisi/references/devops-is-akisi.md`
- `memory-management/references/icerik-turleri.md`
- `proje-islemleri/SKILL.md`

Yoğunluk da eksikti: `proje-dosya-duzeni/SKILL.md` tek başına **20 hit**,
`orkestrasyon/SKILL.md` 9, `mekanik.md` 7.

PAM: *"Sayı eksikse cascade yarım kalır — dokümanın kendi uyardığı hata
(`plugin-dagitim` vakası) bu."*

### CEVAP
PAM haklı, Clara'nın sayımı eksikti. 21 doğru. Taslak düzeltilecek.

## 9 · Websitesi (WS) kanonu kapsamda mı? `[MERT]`

WS tarafında da `STATUS.md` düzeni var: `website-planning/assets/STATUS-template.md`,
`web-clickup/SKILL.md`, `web-is-akisi` vd. Doküman yalnız OY diyor.

PAM: *"WS dışarıda kalıyorsa iki aile ayrışıyor — bu bilinçli mi, yoksa WS ayrı bir
gereksinim olarak sonra mı gelecek?"*

### CEVAP
Hayır OY de bu sistemi çalışır hale getirip sonra OY agentlarına geçeceğiz .

## 10 · `DEVIR-{hedef}.md` kalıyor mu kalkıyor mu? `[MERT]`

⚠️ PAM karar vermeyi **reddetti**: *"Ben karar veremem — bu bir ölçüm sorusu, kanon
sorusu değil."*

Sorusu şu: *"Ölçüm yapılacak mı, yoksa `DEVIR-*.md` şimdilik **yerinde bırakılıp** kanon
ona dokunmadan mı yazılsın? İkincisi güvenli ve cascade'i küçültür; ilkini bekleyeceksem
kanon o kadar gecikir."*

### CEVAP

**MERT (17:39):** İş `pause` alınırken yarım kaldıysa **agent task'a comment atabilir.**
Ayrıca **PA task'ı açarken bir yorum da ekliyor — agent bunu okuyacağını bilmeli.**

---
**CLARA — soru neydi + cevabın ne çözdüğü:**

*Soru neydi:* Kanonda `DEVIR-{hedef}.md` diye bir dosya tanımlı. Bir iş **tek turda
bitmezse** (araya başka iş girdi, working tree'de yarım parça kaldı), devralan agent'ın
*"nerede kaldık, ne yarım"* bilgisine ihtiyacı olur. Kanonun gerekçesi: *"bu bilgi
hiçbir kalıcı belgede yoktur — `status.md` olay akışını tutar, working tree'nin yarım
hâlini tutmaz."* PAM sordu: `status.md` kalkarken bu dosyaya da dokunulacak mı?

*Cevabın ne çözüyor:* **`DEVIR-*.md` gerekmiyor.** `pause` yorumu aynı bilgiyi taşıyor
ve **kalıcı evi ClickUp** — yani dosya açmadan çözülüyor. Kanondaki gerekçe (*"kalıcı
belge yok"*) artık geçerli değil, çünkü sub task'ın kendisi kalıcı belge.

⚠️ **İkinci cümlen AYRI bir kural ve bugün ölçülmüş bir eksiği kapatıyor:**
*"PA task açarken yorum ekler, agent bunu okuyacağını bilmeli."*

Bugünkü testte tam bu eksikti: PA discovery'yi yazdı, sub task'ları açtı, ama discovery
hiçbir yere bağlanmadı — **UID işi alınca *"kapsam var, gerekçe yok"* dedi ve haklıydı.**

→ Kural iki yönlü olmalı: PA yorumu **yazar** (yükümlülük) + agent yorumu **okur**
(yükümlülük). Tek yönlü yazılırsa yorum düşer ama okunmaz.

→ Cascade küçülüyor: `DEVIR-*.md` kaldırılıyor, `status.md` ile birlikte gidiyor. 


---

# GRUP 4 — Ölçülebilirlik (en sert bulgu)

## 11 · "Kendi sub task'ı" agent tarafında nasıl doğrulanıyor? `[ÖLÇÜM]`

⚠️ **PAM'in en sert bulgusu — kararın kendi gerekçesini boşa çıkarabilir:**

> *"ID handoff'ta geliyorsa kural 'handoff'taki ID dışında hiçbir task'a dokunma' diye
> yazılır — **ölçülebilir.** Agent kendi arıyorsa kural 'kendi sub task'ı' diye yazılır —
> ve bu **ölçülemez**, çünkü agent neyin kendisine ait olduğuna kendi karar verir. Bu,
> kararın kendi gerekçesini boşa çıkarır: sınır sahiplikle çizilecekti, ama sahiplik
> agent'ın kendi yorumuysa yine talimat seviyesine düşer."*

### CEVAP
**CLARA ÖLÇÜMÜ — cevap ClickUp'tan alındı (ev Clara mesajları okumadan kapandı).**

**Bugün ölçülemez durumda ve PAM haklı.**

Beş sub task'ın hepsinde `assignees: []` — hiçbirinde atanmış kişi yok.
Ölçülen: `86cb4bb3e` (PRC-36, FE) → `"assignees":[]`

Yani agent'ın *"bu benim task'ım"* demesinin ClickUp tarafında **dayanağı yok.**
Bugün işe yarayan iki şey: **başlıktaki rol öneki** + **handoff'ta verilen ID**.
İkisi de metin, ikisi de yorum gerektiriyor.

PAM'in uyarısı doğrulandı: *"sahiplik agent'ın kendi yorumuysa yine talimat seviyesine
düşer."*

**→ Soru 12'deki kararın bunu çözüyor** (başlık formatı sabitleniyor). Ölçülebilirlik
oradan gelecek — aşağıya yazdım.

## 12 · Sub task'ta sahiplik alanı var mı? `[ÖLÇÜM]`

Doküman katman sub task'larının **"sahipsiz"** açıldığını söylüyor (adım 3).

PAM: *"Sahipsizse 'kendi sub task'ı' nasıl tanımlanıyor — **assignee alanından** mı,
**başlıktaki rol önekinden** mi (`BE Contract`), **handoff'tan** mı? Üçü üç farklı kanon
metni demek."*

### CEVAP
assign olmayacak. Task Başlığında yazar. {ONEK-Proje}-{Agent-Shortcode}- Task başlığı

---
**CLARA ÖLÇÜMÜ + BİR UYARI:**

Ölçüm: `assignees` alanı **var ama boş** (beş sub task'ın hepsinde). Yani bugün fiilen
zaten başlıktan okunuyor — kararın mevcut durumu **sabitliyor.**

⚠️ **Ama bir şey netleşmeli, yoksa kural yine ölçülemez kalır.**

Bugünkü başlıklar şöyle: `PRAG - Randevu Müsaitlik - FE - Takvim Görünümü...`
Senin formatın: `{ONEK-Proje}-{Agent-Shortcode}- Task başlığı`

İkisi **aynı değil** — bugünkünde araya modül adı giriyor (*"Randevu Müsaitlik"*).
Format sabitlenmezse agent kendi payını **yine yorumla** bulur ve `CLA-FIX-THE-CAUSE`
açısından hiçbir şey değişmez.

**Netleşmesi gereken:** ayraç ne (` - ` mi `-` mi), agent kısaltmaları tam liste
(PA/BE/FE/MB/DO/QA/TE/CA/UID), modül adı formatın parçası mı değil mi.

---
## ✅ KARAR (Mert, 17:4x) — köşeli parantez, başta

```
[FE] PRAG - Randevu Müsaitlik - Takvim Görünümü
[BE] PRAG - Randevu Müsaitlik - Şablon, Slot Üretimi
[PA] PRAG - Randevu Müsaitlik - Discovery
```

**Kural — tek satırda ölçülebilir:**
> *"Başlık `[SENİN-KISALTMAN]` ile başlamıyorsa o task'a dokunma."*

**Neden bu format kazandı (diğer ikisi elendi):**

- `{PROJE} - {AGENT} - {başlık}` → alan sırasına dayanıyor; modül adı başlıkta yok
- `{PROJE} - {MODÜL} - {AGENT} - ...` (sahadaki) → ⚠️ **modül adında tire geçerse
  alan kayar** ve kural sessizce yanlış task'ı işaret eder
- **Köşeli parantez** → `startswith` ile ölçülür, ayraç sayısından ve modül adından
  **bağımsız.** Metin yorumu gerekmiyor.

**`CLA-FIX-THE-CAUSE` açısından:** sınır artık gerçekten **mekanizmada** — agent
"bu benim mi" diye yorum yapmıyor, dizgenin başına bakıyor. Kararın gerekçesi kurtuldu.

**Sahadaki başlıklar bu formata çevrilecek** (bugünkü beş sub task dahil).

**Agent kısaltmaları (tam liste):** `PA` · `BE` · `FE` · `MB` · `DO` · `QA` · `TE` ·
`CA` · `UID` 

## 13 · QA "statüye dokunmaz" ile `QA-APPROVE-ATOMIC` çelişiyor mu? `[CLARA]`

Doküman çelişmediğini söylüyor (CA beş dosyada doğrulamış). Ama PAM başka bir kural buldu:

`QA-APPROVE-ATOMIC`: *"onay = STATUS + developer kapanış handoff'u + PA BİLGİ, **ayrılamaz**"*

PAM: *"Buradaki 'STATUS' kelimesi `status.md` dosyasını mı, ClickUp statüsünü mü
kastediyor? Dosya kalkıyorsa bu kural ya anlamsızlaşıyor ya da ClickUp statüsüne kayıyor
— ikincisiyse **doğrudan çelişki** var."*

### CEVAP

Status.md artık kalkıyor. Gerek yok. bence ? 

## 14 · Süre hangi alandan, hangi araçla çekiliyor? `[ÖLÇÜM]`

Ve *"timer kullanılmaz"*ın ölçülmüş sebebi dokümanda **yok**, sadece var olduğu yazıyor.

PAM: *"Kanona gerekçesiz kural yazmam."*

### CEVAP
**CLARA ÖLÇÜMÜ — iki ayrı alan var, karıştırılmamalı:**

**1) Statüde geçen süre — OTOMATİK, ClickUp tutuyor.**
Çağrı: `clickup_get_task_time_in_status`. Ölçülen (PRC-36):
```
Open        : 1h 24m
in progress :    45m   ← agent'ın tracked'e yazacağı sayı BU
test        :    48m
```
Yani agent hesaplamıyor, **çekiyor** — "çekilir, hesaplanmaz" doğru, mekanizması bu.

**2) Tracked time — AYRI alan, elle yazılıyor.**
Aynı task'ta `time_spent: 9569` (ms). Çağrı: `add_time_entry`.

⚠️ **Kimsenin sormadığı bulgu — iki sayı örtüşmüyor:**
`9569 ms` = **9,5 saniye**. Ama aynı task `in progress`'te **45 dakika** durmuş.

Ya test sırasında sembolik bir değer yazıldı, ya mekanizma tutmadı. **Ölçülmeli** —
çünkü "agent süresini çekip yazar" kuralı bugün sahada doğru işlememiş olabilir.

**Timer gerekçesi** ev Clara'sının ölçüm dosyasında (`...clickup-task-takip-testi.md:45`),
taslağa taşınmamış.

## 15 · Kanıt tablosu dört satır — tam liste mi? `[MERT]`

Dört tür var: kod (commit hash) · denetim (QA handoff'u) · CA raporu (yol + ölçüm) ·
canlı (push hash).

PAM: *"Dört tür **dokuz rolü kapsamıyor.** UID mock'unun kanıtı ne (commit mi, ekran
görüntüsü mü)? TE'nin, DO'nun, PA discovery'sinin kanıtı ne?"*

Ayrıca PAM biçim uyarısı yaptı: *"Bu repo tablo yazmıyor, ve kanon metninde tablo bir
kuralın gerekçesini keser. Kanona geçerken gerekçeli düz metne açmam gerekecek."*

### CEVAP

**MERT (17:39):** *"Kanıt neyin kanıtı?"* → **QA okeyleyip UID'e döndüğünde**;
**TE her işte işe girmez.**

---
**CLARA — soru neydi + cevabın benim çözümümü de düzeltti:**

*Kanıt neyin kanıtı:* Agent *"bittim"* dediğinde **bunu gösteren şey.** Taslakta
tanımsız kalmış, haklı olarak sormuşsun.

Sebebi: *"bitti"* bir **beyandır**, kayıt değil. Agent `completed` çekince ClickUp
"bitti" der ama **neyin bittiğini** göstermez. Bugün ölçüldü: BE *"iki catch
düzelttim"* dedi, **sekizi duruyordu** — QA yakaladı. Beyan vardı, kanıt yoktu.

*Cevabın ne düzeltti:* **Hem PAM'in itirazı hem benim çözümüm fazla kapsamlıydı.**

PAM *"dört tür dokuz rolü kapsamıyor"* dedi, ben de her role ayrı kanıt aramaya
başladım. İkisi de yanlış varsayıma dayanıyordu:

- **UID'in ayrı kanıtı yok** — prototip kodunu commit'ler, QA denetler, onay döner.
  Zincir zaten var: **commit hash + QA onay handoff'u.**
- **TE her işte devreye girmiyor** — katmanlar discovery'den çıkıyor (soru 18).
  Girmediği işte kanıtı da olmaz.

**Doğru ölçüt: kanıt ROLE göre değil, ÇIKTI TÜRÜNE göre tanımlanır.**
Kod üreten commit verir (BE/FE/MB/UID aynı) · denetleyen onay handoff'u verir ·
ölçen rapor yolu verir · canlıya çıkan push hash verir.

→ Mevcut dört tür **yeterli.** Eksik olan tek şey "dokuz role tek tek eşlenmeli"
varsayımıydı ve o varsayım yanlıştı. Taslakta bu ölçüt açıkça yazılacak. 

---

# GRUP 5 — Kapsam ve yürürlük

## 16 · Bu düzen tüm OY projelerine mi, yeni projelere mi? `[MERT]`

Yürüyen projelerde `TASK-STATUS.md` ve `status.md` dosyaları **dolu duruyor.**

PAM: *"Kanon değişince eski dosyalar ne oluyor — siliniyor mu, arşivleniyor mu, yerinde
bırakılıp yeni işler ClickUp'a mı yazılıyor? Geçiş kuralı yazılacaksa bunu bilmem
gerekiyor."*

### CEVAP
Tüm projelerde kullanılacak. Yeni taskler bu şekilde ilerleyecek. Eski taskler tast status ve status md de yaşamaya devam edecek. PA bir üsre ikisinide kontrol etmeli ama artık agentlar status.md ya da task status a yazmazlar. (Kural koyarken buryay yazma demek yok. Ne yapılacaksa onu açıklayalım.)

## 17 · `TASK-STATUS`'un prod-geçiş içeriği ClickUp'ta nereye gidiyor? `[MERT]`

⚠️ **PAM'in "en somut endişesi" — ve Clara bunu kararı yazarken görmedi.**

Mevcut kanonda o dosyanın işlevi yalnız kuyruk değil: *"prod'a çıkarken **elle yapılacak**
işler — SQL / env / manuel operasyon; kodda görünmez, **unutulursa prod patlar.**"*

PAM: *"Karar gerekçesi 'kuyruk ClickUp'ın işi' diyor ve kuyruk kısmı doğru, ama dosyanın
taşıdığı **prod-patlatan iş listesi** kısmının ClickUp karşılığı dokümanda
gösterilmemiş."*

Seçenekler: ana task yorumu mu · ayrı bir sub task mı · `sql.md` zaten karşılıyor mu?

### CEVAP
Taskler live dev : operasyon testi bekliyor. 
Operasyon testi yapılan task ready for production a geçer. 
Prod a geçen taskler ise production statusune alınır. 
Prod a geçen taskleri production a çevirme görevi PA nındır kapanışla birlikte 




## 18 · Beş sub task sabit şablon mu, örnek mi? `[CLARA]`

Örnekte UID/BE/FE var; **MB, DO, TE, CA yok.**

PAM: *"Katmanlar discovery'den çıkıyorsa şablon **değişken** demektir — o zaman kanon
'beş sub task' değil **'discovery'den çıkan her katman için bir sub task + PA'nın iki
sabit sub task'ı'** der. Doğru okuma bu mu?"*

### CEVAP
PAM'in okuması doğru. Taslak yanlış anlatmış — beş sub task bir ÖRNEKTİ, şablon değil.
Düzeltilecek.
 
---

# PAM'in tanımadığı kavramlar

- **Clara** — *"OY kadrosunda böyle bir rol yok. Üç ihtimal üç farklı kanon metni demek."*
- **"ev Clara'sı" vs "fabrika Clara'sı"** — *"iki farklı Clara olduğu ima ediliyor, bu
  ayrımı hiç tanımıyorum."*
- **`test` / `completed` statüleri** — OY statü setinde yoklar
- **`PRC-26` / `PRC-37`** — proje kodu olduğunu tahmin ediyor ama hangi proje bilmiyor

**Tanıdık olanlar (sorun yok):** PA, UID, BE, FE, QA, CA · `PA-DISC-RISK-CLOSE` ·
`PA-DISC-NO-TBD` · `PA-DISC-ANSWER-NOT-REQUIREMENT` · `HANDOFF-QA-CLOSES-DEV`
— dördünü de OY kanonunda doğruladı, *"doğru anılmışlar"* dedi.

---

# Dağılım

**Cevabı Clara'da (5):** 1 · 2 · 3 · 8 · 18 → dördü zaten cevaplandı, 5 ve 13 açık
**Ölçüm bekliyor (4):** 6 · 11 · 12 · 14 → hepsi mekanizma sorusuna bağlı
**Mert'in kararı (6):** 4 · 7 · 9 · 10 · 15 · 16 · 17
