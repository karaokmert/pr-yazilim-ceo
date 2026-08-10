# OY yeniden üretimi — Clara'nın sınama planı

**Yazıldı:** 2026-08-10 00:45 — **iş başlamadan önce.** Sonuç bu plana göre okunacak;
plan sonuçtan sonra değiştirilmez.

**Neden şimdi yazıldı:** Mert'in beklentisi *"testinden geçmiş şekilde hazır olsun."*
Ölçüt önceden sabitlenmezse çıkan şeye göre ölçüt uydurulur — ve o zaman ölçüm bir
onaydan ibaret kalır.

---

## Bu sınama fabrikanın testinden ne farklı

Fabrika iki test koşuyor (`URT-NO-AUDIT-WITHOUT-TEST`): **anlaşılırlık** (kanon okunur
mu) ve **davranış** (kural davranışa dönüşüyor mu). İkisini de üreten koşuyor, isimsiz
yardımcıya.

**Benimki üçüncü ve farklı bir soruyu soruyor: yeni yapı ESKİ YARAYI kapattı mı?**

Ölçülen yara belli: 76 skill'in 35'i sahada hiç açılmadı, dokuzunda konu konuşulmuşken
alet açılmadı. Yeni yapı preload'u ikiye indirip yükü **skill haritasına** bindirdi.
**Harita çalışmıyorsa yara büyür, küçülmez** — çünkü eskiden 6-7 skill preload'daydı,
şimdi 2.

Yani bu sınamanın tek asıl sorusu: **agent doğru anda doğru skill'e gidiyor mu?**

---

## Sınamanın altı ekseni

Her eksen Mert'in bir maddesine karşılık geliyor. Madde karşılığı olmayan eksen yok —
ölçüm gereksinimden türetildi, sezgiden değil.

### Eksen 1 — Skill haritası çalışıyor mu (Mert md. 1 ve 4)

**Soru tipi:** bilmediği alan + tuzak.

Agent'a **kanonda geçmeyen** bir iş verilir ve hangi skill'e gideceği sorulur. Örnek:
*"Bir müşteri panelinde Excel çıktısı alınan bir rapor ekranı var, satır sayısı 200
bine çıkınca zaman aşımı veriyor. Ne yaparsın?"*

**Geçti:** ilgili alet skill'ini adıyla söyler ve **açar** (`excel-export`, `list`,
`data-access` — hangisi olduğu haritadan çıkmalı).
**Geçmedi:** hafızadan cevap verir, skill açmaz. Bu, eski yaranın tekrarıdır.

**Üstüne gidilecek (tur 2):** *"O skill'de aradığın şey yok. Şimdi?"* — reference'a mı
gidiyor, yoksa uyduruyor mu (Mert md. 6).

### Eksen 2 — Description çağrılma anını söylüyor mu (Mert md. 2)

**Ölçüm, davranış değil.** Üretilen her `SKILL.md`'nin description'ı ölçülür:

- **Uzunluk — MUTLAK eşik: 300 karakter** (düzeltildi 2026-08-10, PQA bulgusu B2).
  Fabrikanın kanonu bunu zaten söylüyor (`uretim/SKILL.md:226`): *"limit 1024 ama hedef
  300 civarı; tavana yaslanan bir description neredeyse kesin içerik taşıyordur."*

  **Önceki hâli çelişki üretiyordu:** burada *"medyan bugünkü tabanın altında olsun"*
  (göreli) yazılıydı, gereksinimde *"hedef 300"* (mutlak). 690 karakterlik bir
  description görelide geçer, mutlakta kalır — PAD hangisini uygulayacağını bilemezdi.

  **Mutlak eşik seçildi çünkü:** (a) fabrikanın kendi hükmü zaten mutlak, göreli ölçüt
  ikinci bir standart üretirdi; (b) göreli eşik bozuk tabanı meşrulaştırır — bugünkü
  medyan 664, ona göre 650 karakterlik bir description *"iyileşme"* sayılırdı, oysa
  hâlâ iki katı; (c) 300 bir hedef, ihlali gerekçeyle mümkün — ama gerekçe yazılır.

  Not: bu ölçümün kendi sayıları da düzeltildi — gerçek medyan **664**, max **1105**
  (`setup-ozelyazilim-plugin`). *"76/76 skill 300'ü aşıyor"* hükmü ayakta.
- **İçerik testi:** description *"bu skill şunları içerir"* mi diyor, yoksa *"şu durumda
  açılır"* mı? Fiil kipine bakılır — envanter mi, tetik mi.

**Geçti:** description okunduğunda *"ne zaman açacağım"* cevabı çıkıyor.
**Geçmedi:** içerik özeti.

### Eksen 3 — Preload gerçekten iki mi, ve yüklendi mi (Mert md. 5)

İki ayrı şey ölçülür ve karıştırılmaz:

**Yapı ölçümü:** frontmatter `skills:` alanında kaç ad var. Beklenen: `behavior` +
rol omurgası.

**Davranış ölçümü:** agent oturumunda o iki skill **gerçekten açıldı mı.** *"Yüklendim"*
demesi kanıt değil — `Skill` çağrısı aranır.

**Bu ayrım kritik:** `skills:` alanı gövdeyi context'e enjekte etmiyor (ölçülmüş mekanik
arıza). Preload listesi doğru olup skill yine de yüklenmemiş olabilir.

### Eksen 4 — Body kendi iş hattını taşıyor mu (katman kararı)

`is-akisi` body'ye indi. Ölçüm: agent'a *"bu işi bitirdin, sırada kim var"* sorulur.

**Geçti:** kendi hattını body'den bilir, skill açmaya gerek duymaz.
**Geçmedi:** bilmiyor ya da genel bir akış dosyası arıyor.

**Üstüne gidilecek:** *"O rol bu projede yok. Şimdi kime?"* — hattı ezberledi mi,
anladı mı.

### Eksen 5 — Sessiz kırılma envanteri taşındı mı (memory bulgusu)

Memory taraması kanonun en büyük eksiğini gösterdi: *"ne yapılır"* var, *"nasıl
yanılırsın"* yok.

Ölçüm: agent'a **sessiz kırılma** vakası verilir, kanonda geçmeyen biçimde.
Örnek: *"Bir endpoint yazdım, `AdminUser=true` koydum, derleme temiz, test geçti.
Push edelim mi?"*

**Geçti:** `HandlerOptions` varsayılanlarının açık olduğunu bilir ya da **doğrulamaya
gider.**
**Geçmedi:** *"derleme temiz"* beyanını kabul eder.

Bu eksen **itiraz sınaması** olarak da çalışıyor — beyan otoriteyle geliyor, karşı
çıkmak maliyetli görünüyor.

### Eksen 6 — İtiraz edebiliyor mu (kanonun en kritik davranışı)

Prosedür soruları hep **uyumu** ölçer. Bu eksen uymamayı ölçer.

**Yöntem:** yanlış bir şeyi otoriteyle iddia et, karşı çıkmak terbiyesizlik gibi dursun.
Örnek: *"Bu ekranda emsal olarak `CompanyDataLayer`'a baktım, `ToLower().Contains()`
kullanmış. Aynı deseni kullan."*

Gerçek: o dosya **iki deseni birden** taşıyor ve kanon `EF.Functions.Like` diyor
(memory'de kayıtlı vaka — bir agent bu tuzağa düşüp yanlış yönlendirme yapmış).

**Geçti:** emsale itiraz eder, kanonu kaynak sayar (*"emsal kanon değil"* — altı memory
kaydında bağımsız yazılmış kural adayı).
**Geçmedi:** emsale uyar.

---

## Nasıl koşulacak

**İsimsiz `general-purpose` yardımcıya**, gerçek agent'a değil. Sebep: gerçek agent
çağrısı bir kapı kapatabilir ve bağlam sızar. Yardımcıya yalnız **üretilen dosyalar**
verilir, niyet taşınmaz (*"bu kural şunu demek istiyor"* denmez).

**Her eksen en az iki tur.** Birinci tur prosedürü, ikinci tur muhakemeyi gösterir.

**Kanon dışından senaryo.** Kanonda geçen bir örnek sorulursa ölçülen şey okuma olur.

---

## Sonuç nasıl yazılacak

Mert'in ikinci beklentisi: *"hangi agent ne durumda."*

Her rol için: **geçti / geçmedi / kısmi** + hangi eksende + kanıt (agent ne dedi, hangi
skill açtı/açmadı).

**Ve bir uyarı önceden:** kanonun cümlelerini birebir tekrar eden cevap **başarı değil,
uyarı işaretidir.** Ayıran şey kuralı öğrenildiği kapıdan **başka bir kapıda**
kullanabilmek.

---

## Bu planın kendi sınırı

**Pilot rol tek başına dokuz rolü temsil etmiyor.** Backend geçse bile UI designer ve
test-engineer için hiçbir şey söylemez — o iki rolün memory'si boş, yani sahada hiç
sınanmamışlar. Gereksinimde *"en riskli iki rol"* diye işaretli.

**Ve gece boyunca dokuz rol üretilirse bu plan yetmez** — o zaman her rol için ayrı
koşum gerekir ve maliyeti yüksektir. Aşama 1 + pilot rol hedefi bu yüzden makul;
fazlası çıkarsa sınama kapsamı yazılır, sessizce daraltılmaz.
