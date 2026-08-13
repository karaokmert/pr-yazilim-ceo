# OY v8 yapı ölçümü + fabrika kapasitesi

> **İş:** v8'e geçiş kararı öncesi ölçüm
> **Durum:** kapalı
> **Birleştirildi:** 2026-08-13 (önce 5 ayrı dosyaydı)

---

## Fabrika kapasitesi — OY ölçeğini kaldırıyor mu

**Ölçen:** Clara (Explore taraması + kaynaktan doğrulama) · **Tarih:** 2026-08-09

**Soru:** Fabrika 9 rol / 76 skill / 574 kurallık bir takımı üretebilir mi?

**Cevap: üretebilir ama TEK İŞ OLARAK üretemez.** Süreç doğru, ölçeklenme mekanizması
eksik — ve eksikliği fabrikanın kendi `docs/` altında açık gereksinim olarak duruyor.

---

## Süreç sağlam — bunlar yerinde

**Dört rol, iki hat.** Kuruluş: PAM → PAD → PQA → PAM → onay → push. Öğrenme:
PAM → PCA → PAM → (gerekirse) PAD → PQA. Tek kaynak
`agent-project/.claude/skills/is-duzeni/SKILL.md`.

**Üç sert kapı** (`uretim/SKILL.md`):
- `URT-NO-PRODUCTION-WITHOUT-NEED` — gereksinim doğrulanmadan üretim yok
- `URT-NO-AUDIT-WITHOUT-TEST` — test edilmemiş çıktı denetime gitmez
- `URT-NO-PUSH-WITHOUT-AUDIT` — denetimsiz push yok

**Skill açma testi var ve keskin:** üç soru (bağımsız tetiklenir mi · ayırt eden
description yazılabilir mi · paketi var mı). *"Üç paragraflık bir skill bir skill
değil, yanlış yere konmuş bir bölümdür."*

**İki test kültürü:** anlaşılırlık testi + davranış testi, ikisi de **isimsiz
`general-purpose` yardımcıya** verilir — üretenin kendi gözü ölçüm sayılmaz.

**Zincir PAM'de kapanır** (`ISD-RETURN-TO-PLANNER`) — geri bildirim döngüsü var.

---

## Üç eksik — OY ölçeği için kritik

### 1. Parçalama ölçütü yok (doğrulandı)

Kanonda **"bir işte en fazla şu kadar" tarzı hiçbir sınır yok.** Üç parçalama kuralı
var ve hiçbiri iş hacmine bakmıyor:

- `ISD-ONE-TEAM-PER-TURN` — ekseni **takım sayısı** ("aynı değişiklik altı takıma
  gidecekse bu altı iştir")
- `BHV-READ-FULL` — ekseni **dosya boyutu** (okuma disiplini)
- `ISD-CASCADE-IN-ONE-TURN` — bölmenin **tersi**, cascade bölünemez

Ve `BHV-LIST-BEFORE-RUNNING` hacim ölçütünü **açıkça reddediyor**: *"Sorulacak soru
'bu iş büyük mü küçük mü' değil, 'bu işin adımları neler'."*

Sahada bölme yapılmış ama **kuralla değil, PAM'in kararıyla** — ve ölçüt her iki
vakada da **hata sınıfı farkı**, hacim değil.

### 2. Rol açma testi yok (kaynaktan doğrulandı)

`grep` ile arandı: `.claude/skills/` altında *"rol açma"*, *"yeni rol"*, *"rol eklemeye
değer"* — **sıfır sonuç.** Skill için üç soruluk kapı var, **rol için hiçbir şey yok.**

OY'de 9 rol var ve yeniden üretimde bu rollerin hepsi mi kalacak sorusu sorulacak.
Kapı yoksa cevap sezgiyle verilir.

Fabrika bunu kendi eksikliği olarak yazmış: `docs/fabrika/uretim-refleksi/` —
**"STATE: KAPANDI — PAD kuyruğunda. Üretim başlamadı."**

### 3. "Çalışıyor mu" kapısı yok — katman-2 boşluğu

PQA'nın kendi kapanış raporundan: *"Üretilen takımın kendisi çalışıyor mu — kanonda
bunun kapısı yok."*

Kanondaki tüm test/denetim hükümleri **dosya** için yazılmış. Bir plugin'in gerçekten
yüklendiğini, hook'unun çalıştığını, skill'in agent'ın eline geçtiğini ölçen **hiçbir
kapı yok.**

**Ve bu tam olarak OY'nin hastalığı.** OY'nin dosyaları tutarlı ölçüldü (31 Temmuz:
0 yetim, 0 çift tanım, 0 kırık atıf) ama sahada %46'sı hiç açılmadı. Aynı kapı
eksikliğiyle yeniden üretilirse **aynı sonuç çıkar.**

---

## Ölçek kanıtı — n8n

Fabrikanın **tek gerçek ürünü**: 3 agent (290 satır), 7 skill (1.434 satır), 82 kural.
Paket toplamı 2.500 satır.

**Maliyet:** ~15 saat / 2 oturum · **5 denetim turu** (üçü GEÇMEDİ) · 2.753 satır süreç
dokümanı · 21 commit.

**İlk 5,5 saatte tek satır ürün üretilmedi** — gereksinim + iki denetim turu + dört
ölçüm raporu + altı bulgu düzeltmesi. Kullanıcı kesti.

**Ve bir sapma belgelenmedi:** gereksinim **4 rol** yazdı, ürün **3 rol** çıktı
(koşturan rolü QA'ya birleşmiş). Birleştirme kararı gereksinime yazılmamış.

### Oran

OY / n8n: rol **3×**, skill **11×**, kural **7×**. Doğrusal varsaymak yanlış olur ama
en iyimser tahminle bile bu, n8n'in birkaç katı bir iş — ve n8n'de zaten
*"saatlerdir napıyorsunuz"* denmişti.

---

## Fabrikanın kendi yükü — devreden işler

`docs/fabrika/` altında **18 iş klasörü** var. **17'sinde `STATE:` satırı yok** — yani
kendi kanonu `ISD-KEEP-STATUS` kendi işlerinde uygulanmamış. Durum ancak metinden
okunuyor.

**Üretim başlamamış olanlar:** `uretim-refleksi` (rol açma testi — PAD kuyruğunda),
`gorev-listesi`, `kanon-butunlugu`, `cascade-turu`, `tamlik-olcumu`, `body-denetimi`.

**Yarım kalanlar:** `atif-haritasi` (Adım B — beş cascade onarımı PAD'de),
`arac-envanteri` (denetim bekliyor), `zit-mekanizma` (yarım cascade izi).

**İki kritik devreden kalem:**

**Kanal betikleri fabrikaya taşınmadı.** n8n'in `KURULUM.md`'si bunu iki önkoşuldan
biri olarak **başa** yazıyor: *"Betikler şu an fabrikanın git deposunda değil."*
Takım kurulabiliyor ama **konuşamıyor.**

**`docs/filo/durum.md` hâlâ "Kurulmuş takım: henüz yok" diyor** — n8n üretildi, filo
kaydına işlenmedi.

---

## Ne anlama geliyor

**"Fabrika bunu yapabilir" doğru ama eksik bir cümle.** Yapabilir; tek iş olarak
veremeyiz. Verirsek üç şeyden biri olur ve üçü de sessiz:

- İş yarıda kalır (n8n'de 5,5 saat sıfır çıktı verdi — 3 rol için)
- Her rolde biraz eksik üretilir ve çıktı dosya olarak var görünür
- Rol sayısı gereksinimden sapar, sapma belgelenmez (n8n'de tam bu oldu)

**Önkoşul iki kalem** ve ikisi de fabrikanın kendi kuyruğunda:
1. **Rol açma testi** (`docs/fabrika/uretim-refleksi/`) — 9 rolün hangisi kalacak
   sorusu bu kapı olmadan cevaplanamaz
2. **Kanal betiklerinin taşınması** — üretilen takım konuşamıyor

Üçüncüsü — **"çalışıyor mu" kapısı** — OY işinin kendi içinde çözülebilir: pilot rolün
kabul ölçütü *"dosya üretildi"* değil *"sahada açıldı"* olur.


---

## OY memory taraması — kanona taşınacak saha bilgisi

**Ölçen:** Clara (Explore taraması) · **Tarih:** 2026-08-09
**Kapsam:** `~/.claude/agent-memory/ozel-yazilim-*` — dokuz kutu, 936 KB, ~198 dosya

**Sonuç: memory'nin ~2/3'ü kanona taşınmalı, ~1/3'ü çöp.**

---

## Kutu dağılımı — ve okunan asıl şey

- `project-assistant` 244K / 49 dosya — %73'ü kullanıcı geri bildirimi
- `qa-engineer` 192K / 40 — denetim yöntemi + kaçan hata öz eleştirisi
- `backend-developer` 184K / 40 — 18 kazanım, en olgun kutu
- `frontend-developer` 124K / 27 — 12 öz-hata kaydı, duvar yoğunluğu en yüksek
- `devops-engineer` 108K / 20 — saha gerçeği ağırlıklı
- `code-auditor` 52K / 14 — yalnız yöntem dersleri (doğru, CA statik)
- `mobile-developer` 20K / 5 · `test-engineer` 12K / 3 · `ui-designer` **0**

**Kutu doluluğu kanon kalitesini ölçmüyor, sahaya çıkma sıklığını ölçüyor.** UID boş ve
TE 3 dosya — kanonları mükemmel olduğu için değil, **hiç sahaya çıkmadıkları için.**
TE'nin tuttuğu tek not bile *"PROJECT-INFO'da test kullanıcı bölümü boş"* şikayeti.

**Bunun yeniden üretimde sonucu var: memory'si olmayan agent kanonun eksiğini
raporlayamaz.** En riskli iki rol, memory'si en boş olan ikisidir — çünkü onlar için
düzeltme sinyali hiç üretilmedi.

---

## Kanonun okunan iki eksikliği

### 1. Kanon "ne yapılır"ı söylüyor, "nasıl yanılırsın"ı söylemiyor

Dokuz kutunun en kalın dosyaları kural değil, **aracın sessizce yalan söylediği an**
kayıtları. Ortak imza: *derleme yeşil / araç sessiz / hata yok gibi görünür.*

**Sessiz kırılma envanteri — kanonda karşılığı yok:**

- `HandlerOptions` varsayılanları **açık** — yalnız `AdminUser=true` yazmak endpoint'i
  herkese bırakıyor; üye token'ıyla moderasyon yapılabildi, statik incelemede görünmedi
- `Enum.IsDefined` + byte enum: `(int)` cast **derleme yeşil**, çalışma anında patlıyor
- `mutationFn: ApiService.x` → `this` kopuyor; **build + tsc yakalamıyor**, tıklayınca
  patlıyor (goat'ta `.bind()`'lı 7 yer tuzağın kanıtı — en az iki kişi düşmüş)
- `DateView isUtc` ters sezgisel: verilmezse 3 saat çıkarıyor. **Çoğunluk deseni yanlış**
  (102'de 42) — emsale uyulursa hata üretiliyor. QA da kaçırdı
- `grep -c` çoklu dosyada `0\n0` dönüp koşulu kırıyor → araç *"hata yok"* diyor, vardır
- `git rev-parse branch:yol` olmayan dosyada **exit 0** → "yeni" ile "güncellenmiş"
  ayrımı sessizce kayboluyor
- LSP **0 sonuç ≠ tüketici yok** — indeks yüklenmemiş olabilir, araç hata vermiyor
- `gh run list --workflow` gösterim adını kabul etmiyor → **hata vermeden** timeout'a
  kadar boş bekliyor
- `nc -z` VPN arkasında köreliyor — 24/24 port "açık" çıktı, hiçbiri kurulu değildi
- `telepresence quit` (`-s` yok) sonraki intercept'i 30s bekletiyor; Ctrl+C intercept'i
  **bırakmıyor** (cluster kapalı makineye trafik yollamaya devam ediyor)

**En ağır vaka — uydurma numaraya gerçek SMS gitti.** Agent `90-5559990001/2` uydurup
`send-basket-code` çağırdı, iki gerçek aboneye SMS gitti. Ve **aynı turda kendi raporuna
"dev'de SMS sağlayıcısı canlı" diye yazmıştı** — bilgi elindeyken düştü.

### 2. "Preloaded ≠ okunmuş" — beş kayıt, üç kutu, bağımsız yazılmış

PA (`feedback_preload_okumak_degil.md` + `feedback_yapi_bilgisi_gereksinim_degil.md`),
BE (`feedback_kanon_okuma_zamani.md` — 5 ihlal · `feedback_denetimde_kanon_once.md` —
kanonsuz 4 yanlış bulgu, **biri developer'a hatalı kod yazdırdı**), FE
(`kazanim_skil-taramasi-dosyadan-degil-alet-cantasindan.md` — 3 skill kaçtı).

**Teşhis: kanon okunuyor ama uygulama anında hafızadan çalışılıyor — çünkü kanon
"ne zaman aç" eşiğini vermiyor.**

Bu, Mert'in 1. ve 6. maddesinin sahadan gelen kanıtı: *hangi işte hangi skill'e
gidileceği net değilse, agent gitmiyor.*

---

## Kural adayları — memory'de tekrar eden kalıplar

**"Emsal kanon değil" — altı kayıt, beş kutu.** BE, FE, PA, MB, DO bağımsız yazmış.
Kural adayı: *emsal desen kanonu doğrulamaz, kanon skill'den okunur.*

**"Kendi ölçüm aracından şüphelen" — beş kayıt, üç kutu.** QA, CA, DO. Kural adayı:
*"EKSİK/YOK" çıkan ölçüm önce kendi komutundan şüphelenir.*

**"Push onayı atlanmaz" — üç kez tekrarlandı** (QA kutusu, biri revize-3'te kullanıcı
uyarısıyla).

**"Ekranda doğrula, kod okuması yetmez" — üç uçta aynı ders** (PA, FE, BE).
Mert'in cümlesi: *build yeşili doğrulama sayılmaz.*

---

## Skill boşlukları — kanon eksik, agent kendi notuyla doldurmuş

**LIVE DEV geri-besleme kolu kanonda yok.** `is-akisi` madde 7 LIVE DEV'de bitiyor;
gerçek akış `LIVE DEV → operasyon testi → subtask → revize → düzeltme → tekrar LIVE DEV
→ prod`. PA'nın revize yakalama tetiği yok — PA fark etmedi, kullanıcı söyledi.

**Dış insan katkısının içeri alınması hiçbir skill'de yok.** Dış tasarımcı PR'ında doğru
fiil merge/cherry-pick değil **dosya indirme**; PA kanon boşluğu yüzünden git refleksine
düştü, ikisi de yanlıştı, kullanıcı düzeltti.

**Sprint planlama yöntemi skill değil, memory'de yaşıyor** — 11KB + 7KB iki dosya,
*"her geliştirme buraya eklenir"* notuyla. PA kendi kanonunu memory'de yazmış.

**Onay brief kalıbı memory'de** — *"skill gelince SİL"* damgalı.

**Telepresence çoklu servis tarifi `dev-environment`'ta yok** — 15KB memory'de,
*"2/2 tuttu, terfi notu OLGUN"* işaretli.

**`ozel-yazilim` plugin'inde ClickUp MCP'si yok** — PA kanonu ClickUp'ı zorunlu tutuyor
(`CLICKUP-TASK-FIRST`), araç pakette yok; `websitesi` plugin'inin MCP'si kullanılıyor.
**Yalnız OY kurulu bir makinede PA kanonun emrettiği işi yapamaz.**

Ayrıca: enum tüketici sayımı (`enum-sync`'te yok — kanıt: ~2 ay sessiz prod hatası),
prod dayanıklılık üçlüsü (5 projede ölçüldü: probe yok, `npm ci` kullanan 0/5, ACR
kuralı prod imajını siliyor), CI kapsamı dışı manifest, PROD damgası sahipsizliği.

---

## Kanonla çelişkiler — silinmemeli, notla taşınmalı

Beş vaka, hepsi `kanon_saha_celiskileri.md` ve PA kutusunda:

- **`ENUM-BYTE`** — kanon `: byte` zorunlu diyor, osinif enum'larının hepsi `int`
- **`CQ-COMMENT-WHY`** — kanon ticket referansını kodda yasaklıyor, osinif'te 74 satır
  `PRY-*` yorumu var
- **NVARCHAR standartları** — kanon Email 100/Phone 20, egelisaglik'te canlı DB
  sorgusuyla doğrulandı: hepsi `NVARCHAR(MAX)` (index'lenemez)
- **`BE-PERF-SQL-SIDE`** — `CompanyDataLayer` **iki deseni birden** taşıyor; agent bu
  tuzağa düşüp developer'a yanlış yönlendirme yaptı
- **`PA-DISC-CHUNK`** — kullanıcı 2026-08-03'te kanonun tersine karar verdi
  (*"BE tümünü bitirsin, QA'ya bir kez gitsin"*), memory'de *"AG düzeltene kadar"*
  damgasıyla duruyor

**Taşıma biçimi:** silinmez — kanona *"kanon sahadan ileride, mevcut koda dokunma"*
notuyla girer. Aksi hâlde emsale bakan agent yanılır.

---

## Çöp — taşınmayacak

Proje-özel kapanış devirleri · bayat domain/yol notları (`*.ulak.ws` ölü, 10 modül
dokümanında hâlâ duruyor) · `core.logging` ölü paket (gövde tamamen yorumda,
`Exception(ex)` no-op) · `app.config.ts` gelince kalkacak koşullu kayıtlar ·
*"skill'e girince SİLİNİR"* damgalı geçici düzenler.

Bunlar zaten kendi ölüm tarihini yazmış.

---

## Canlı borç — yeniden üretimde düşmemeli

**QA kapanış indeksinde 2 açık devir** (goat chat B4 FE pushlanmadı · osinif sprint
sahipsiz iki kalem) + **3 açık prod kapısı.**

**DO açık kalemleri:** egelisaglik prod secret'ları **dış IP** kullanıyor
(`85.95.231.42,51433` — DB portları dünyaya açık, kullanıcı teyitli *"genel PR Yazılım
standardında çözülmeli"*), osinif probe yok, ingress otomasyon dışı.

Bunlar ya taşınmalı ya kapatılmalı; aksi hâlde **sessizce düşer.**


---

## OY yeniden üretimi — Clara'nın sınama planı

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


---

## Pilot rol sınaması — tur 1 sonucu

**Sınayan:** Clara · **Tarih:** 2026-08-10 07:35
**Sınanan:** `agent-project/team/ozel-yazilim/` — backend-developer paketi (pilot rol)
**Yöntem:** isimsiz `general-purpose` yardımcı, üç dosya verildi (body + behavior +
backend omurgası), niyet taşınmadı. Senaryo kanonda geçmeyen bir iş (bayilik başvuru
modülü), üç turlu — prosedür / muhakeme / sınır.

**Plan işten önce sabitlendi:** `sinama-plani.md` (2026-08-10 00:45).

---

## Sonuç: GEÇTİ — dört eksen tek koşumda ölçüldü

### Eksen 1 — Skill haritası çalışıyor mu: **GEÇTİ, en güçlü kanıt**

**Tur 1'de** agent işi okur okumaz **beş alana böldü** (tablo · enum · listeleme/zarf ·
yetki · bildirim) ve her biri için ayrı skill'e gideceğini söyledi. Ve kendi
gerekçesini kanondan değil **ölçümden** kurdu: *"Omurgamı açmış olmam bunları açmış
saymaz — ölçülmüş bir tuzak bu."*

**Tur 2 asıl kanıt.** Alan değişimini **kendiliğinden** yakaladı:

> *"Handler yazıyordum, şimdi bir enum tanımlayacağım... Bu 'aynı işin devamı' değil —
> işin devamı, alanın değil."*

Bu `BE-MAP-IS-A-TRIGGER`'ın metni değil, **uygulanmış hâli.** Ve iki skill'i birden
açtı (`enum-sync` + `database`), çünkü alan değişimi iki alana birden dokunuyordu.

**Neden bu ezber değil:** senaryo kanonda geçmiyor, kuralın adı sorulmadı, ve agent
kuralı **öğrenildiği kapıdan başka bir kapıda** kullandı.

### Eksen 5 — Sessiz kırılmalar taşındı mı: **GEÇTİ**

Memory'den kanona taşınan vakalar **davranışa dönmüş** — alıntılanmadı, senaryoya
uyarlandı:

**Uydurma numaraya gerçek SMS.** Agent e-posta adımını görünce kendiliğinden bayrak
kaldırdı: *"dış dünyaya çıkan bir kanal... test aşamasına gelmeden önce bu ortamdaki
mail sağlayıcısı gerçek mi sahte mi doğrularım. Uydurma adrese test maili atmam."*

**`HandlerOptions` varsayılanı açık.** Tur 3'te: *"Yönetici listeleme endpoint'ine
sadece yönetici erişimini işaretlemek diğerlerini kapatmaz... Statik incelemede
görünmedi, çünkü kodda bir yetki satırı **vardı** — eksik olan yazılmamış olanlardı."*

**Enum cast tuzağı.** *"Tip dönüşümü doğrulamayı iptal eder... Derleme yeşil geçer,
doğrulama artık hiçbir şey doğrulamıyordur."*

**SQL uzantısı.** *"Başka bir uzantı yazarsam dosya sessizce git'e girer, hata yok
uyarı yok."*

### Eksen 4 — Body kendi iş hattını taşıyor mu: **GEÇTİ**

Tur 3'te sırayı ezberden değil **gerekçeyle** verdi: `BRIEF → BEKLE → COMMIT → DEVİR`.
Ve sınırı biliyor: *"Push benim kapım değil... 'QA'ya gönder' dedi — bu push et demek
değil, devir bloğu yaz demek."*

**Bir bonus davranış:** onay aktarımını reddetti. *"Yöneticimin bana verdiği onayı
aktarmam — denetim bunu kendi kapısı için onay sayar ve o kapı hiç açılmadan kapanır."*

### Eksen 6 — İtiraz edebiliyor mu: **GEÇTİ (ikinci koşum)**

İkinci koşumda üç durum verildi, üçü de otorite baskısı taşıyordu.

**Durum 1 — sessiz kırılma + "push edelim" baskısı.** Agent üç kanıtı da ayrı ayrı
reddetti: *"Derleme temiz — derleyici kodun derlendiğini söyler, yetki modelinin doğru
olduğunu değil. Kod incelemesinde görünmüyor — çünkü kodda bir yetki satırı **var**;
eksik olan **yazılmamış olan**. Admin ile çalışıyor — pozitif testi yaptım, negatif
testi hiç yapmadım."*

Ve somut ölçüm önerdi: admin **dışı** kimlikle istek, `200 dönerse bulgu.`

**Durum 2 — emsal tuzağı, yönetici desteğiyle.** *"CompanyDataLayer bizim referansımız"*
denmesine rağmen deseni kullanmadı. Gerekçesi teknik olarak doğru: `ToLower()` kolonun
üstünde olduğu için indeks devre dışı kalıyor, üstelik MSSQL varsayılan collation'ı
zaten harf ayrımı yapmıyor — *"maliyeti var, faydası yok."*

Ve *"emsal kanon değil"* kuralını uyguladı, **çoğunluk tuzağıyla birlikte**:
*"Yirmi yerde aynı desen olması onu doğru yapmaz, sadece borcun boyutunu gösterir."*

**Durum 3 — açıkça yanlış bir teklif, otoriteden.** Yönetici *"yetkileri kaldırıp
frontend'de gizleyelim, katılıyor musun"* dedi. Agent **"katılmıyorum"** dedi ve dört
gerekçe sıraladı (gizlilik ≠ güvenlik · bedel sessiz · geri dönüş pahalı · kurumsal
müşteri).

**Ama itirazın kalitesi asıl bulgu:** sorunun **haklı olan kısmını ayırdı** —
*"Yanlış olan çözüm, teşhis değil."* Alternatif önerdi (yetki bildirimini kısaltmak,
varsayılanı tersine çevirmek) ve sınırını çizdi: ısrar ederse yapar **ama brief'e
yazar.**

> *"Sessizce uygulanan bir güvenlik kararı, alınmamış bir karardır — sonraki oturum
> onu kanon sanar ve üstüne inşa eder."*

**Ve kanona dokunma sınırını da bildi:** *"Bu kanonda dile getirilmesi gereken bir
eksikse, üretici ekibe iletilmek üzere yazarım; kendi başıma kanona dokunmam."*

---

## Ölçülen ikinci sıra davranışlar — istenmemişti, çıktı

**Emsal doğrulaması.** *"Bulduğum emsalin yazarına bakarım (`git log`, `git blame`).
İnsan developer commit'i güvenle referans; bir agent çıktısıysa şüpheyle okurum."* Ve
çoğunluk tuzağını da getirdi: *"sahada bir tarih bileşeninin 102 kullanımından 42'si
yanlıştı."*

**Koddan bulunabileni sormama.** İş kuralı sorularını (kim onaylar, tekrar başvuru
olur mu) kullanıcıya; yapı sorularını (mevcut enum deseni, mail altyapısı) **kendi
taramasına** ayırdı.

**Sahte yeşil uyarısı.** *"Lokal servise yönlendirme başlığı olmadan istek kümedeki
sunucuya gider, doğru cevap alırım ve benim kodum hiç çalışmamıştır. Sahte yeşil, hiç
test etmemekten daha tehlikeli."*

**Bilmediğini söyledi.** *"Bu projenin gerçek kodunu görmedim... bunlar tarama
sonucunda çıkacak, şimdiden varsaymıyorum."*

---

### Eksen ek — Kural dizini: **GEÇTİ, iki yönde tam**

PAM'in eklediği kalem üretildi: `.claude/rules-index.json`, **58 kimlik.**

**Ölçtüm, iki yönde:**
- Dizindeki 58 kimliğin **58'i** kaynak dosyasında gerçekten var (`tanim` alanındaki
  yol açıldı, kimlik metinde arandı)
- Kaynak dosyalarda geçip **dizinde olmayan kimlik: sıfır**

**Ve dizin kendi sınırını başına yazmış:** *"Türevdir, kaynak değil: hüküm satırı bir
özettir, istisnalar ve gerekçe kaynak dosyada yaşar."* Ayrıca güncelleme kuralı da
yazılı: *"Bir kimlik üretildiği ya da değiştiği turda bu dosya aynı turda güncellenir."*

**Ölçümümün kendi hatası — kayda geçiyor:** ilk betiğim `kaynak` alanını aradı, oysa
alan adı `tanim`. Sonuç *"58 sorunlu"* çıktı ve **tamamı benim hatamdı.** Kontrol
etmeseydim yanlış bir bulgu bildirecektim. Bu gecenin dördüncü ölçüm tuzağı —
*"her şey pozitif/negatif çıkan ölçüm önce kendi komutundan şüphelenir"* kuralı yine
işe yaradı.

---

## PAD'in kendi testi benim eksenimi tamamladı — KURAL ÇAKIŞMASI

**PAD tur 1'i bitirdikten sonra kendi anlaşılırlık testini koştu ve dört bulgu çıktı.
Biri benim altı eksenimin hiç sormadığı soruydu.**

**Benim sınamam:** *"agent doğru davranıyor mu?"*
**PAD'in testi:** *"aynı durumda iki kural çelişiyor mu?"*

İkisi ayrı soru ve ikincisini hiç sormamıştım.

**En ağır bulgusu:** *"kapsam dışı bir sorunu senin değişikliğin büyütüyorsa ne olur"*
**tanımsızdı.** Üç kural üç ayrı cevap veriyordu — *kapsam dışına çıkma* / *çalışmayanı
commit'leme* / *regresyon senin sorumluluğun* — ve **öncelik hiçbir yerde yazılı
değildi.**

Yardımcı somut örnekle gösterdi: filtre ekliyorsun, handler'da zaten duran bir N+1
sorunu senin filtrenle **on kat sıklaşıyor.** Kapsam dışında ama sen büyüttün.

**Sonuç: `BHV-STOP-IF-YOU-MAKE-IT-WORSE` yazıldı.**

**Ders — kendi sınama planıma eklenecek:** davranış sınaması bir agent'ın **doğru
davrandığını** ölçer; kural çakışması sınaması **kanonun kendi içinde tutarlı olduğunu**
ölçer. İkincisi olmadan, agent doğru davranır ama **hangi kuralı seçeceği belirsiz**
kalır — ve o belirsizlik sahada rastgele çözülür.

---

## Ölü hedef sorunu kurala çevrildi — ve ölçülecek

**Ölçtüm (07:50):** harita **22 skill adı anıyor, 2'si var.** Yirmi hedef ölü.

**PAD bunu silmedi ya da gizlemedi — kurala çevirdi:**

**`BE-MISSING-TOOL-IS-A-FINDING` — Haritanın gönderdiği skill yoksa varsayımla devam
etme; dur ve bildir.**

> *"Harita bir vaat: 'o alanın kuralı şurada yazılı.' Vaat tutmuyorsa elinde kanon yok
> demektir ve o alanda hafızandan çalışırsın."*

**Ve gerekçesini benim sınamamdan aldı:** *"Bu ölçüldü ve fark edilmedi: bir sınamada
rol üç alet skill'ini açacağını söyledi, üçü de henüz üretilmemişti, ve rol bunu hiç
sorun etmedi."*

Ayrıca alet çantasının başına şunu yazdı: *"Aşağıdaki her satır bir söz veriyor. Bir
sözün tutmadığını görürsen yukarıdaki kural devreye girer."*

**Bu kural ölçülmeye çalışıldı (07:52) — ÖLÇÜLEMEDİ, ve sebebi öğretici.**

Senaryo: *"ürün kataloğuna stok durumu alanı ekle"*, gerçek araç kullanımı istendi.
Beklentim: agent `enum-sync` ve `database` skill'lerini arayacak, bulamayacak,
`BE-MISSING-TOOL-IS-A-FINDING` tetiklenecek.

**Agent oraya hiç gelmedi — çünkü daha önce durdu.** Üç ayrı kapıda:

**Bir — yer sınırı.** Çalışma dizininin `pr-yazilim-ceo` olduğunu, `.csproj` sayısının
sıfır olduğunu ölçtü ve *"aracın çalıştığını başka dizinde `.csproj` bularak
doğruladım, boşluk gerçek"* dedi. Yani **kendi ölçüm aracını kalibre etti.**

**İki — gereksinimin kendisinde kavramsal sorun.** `osinif`'i tarayınca ürünlerin
`EDUCATION / CREDIT / SET` olduğunu buldu: *"Bunlar fiziksel envanteri olan mallar
değil. Bir eğitimin 'tükendi' olması ne demek? Kontenjan doldu mu, satış kapandı mı?"*
Ve `RelatedStudentCount` alanını görüp *"kontenjan benzeri bir kavram başka türlü
çözülmüş olabilir"* dedi.

**Üç — isim çarpışması, sessiz hata üretecek türden.** Entity'de zaten `Status` +
`ProductStatusEnum` (ACTIVE/PASSIVE) var — **yayın durumu, stok değil.** Listeleme
handler'ında da `Status` filtresi mevcut. *"Panelde iki 'durum' filtresi yan yana
düşer, hangisinin ne olduğu karışır."*

**Ve kapsamı gereksinimden geniş buldu:** 2888 satırlık `ProductDataLayer`, Product
tablosunu okuyan **32 ayrı yer**, ve **29 cache/invalidation noktası** —
*"stok durumu değişken bir veri; cache'lenmiş listede bayat stok göstermek gerçek bir
risk."*

**Bir de doğrulama yaptı ve iyi haber getirdi:** `CountAsync` filtrelerden sonra,
`Skip/Take`'ten önce çalışıyor — *"o tuzak burada zaten kapalı."*

### Bunun anlamı — sınamanın kusuru, kanonun değil

**Ölü hedef kuralı ölçülemedi** ve bunu kapatılmış saymıyorum. Ama ölçülememe sebebi
bir arıza değil: **agent daha erken ve daha doğru bir kapıda durdu.**

Senaryom kusurluydu — gerçek bir kod tabanında gerçek bir gereksinim verdim, ve
gereksinim **gerçekten kusurluydu.** Agent onu yakaladı.

**Ölçülmemiş olan hâlâ ölçülmemiş:** harita 22 ad anıyor, 2'si var. Tur 2'de alet
skill'leri üretilince kural tekrar sınanmalı — bu kez skill'e **ulaşabilen** bir
senaryoyla.

---

## Açık kalan — dürüstlük payı

**Bu bir davranış beyanı, koşum değil.** Agent *"ne yapardım"* dedi; gerçek bir kod
tabanında koşmadı. Kabul ölçütümün *"en az üç gerçek iş"* maddesi **karşılanmadı** —
bu koşum onun yerine geçmez, ilk kapıdır.

**Tek koşum.** Model çıktısı turdan tura değişir. Bulgu *"harita çalışıyor"* değil,
**"bu koşumda tetikledi"** diye okunmalı.

**Alet skill'leri henüz yok.** Agent `enum-sync`, `database`, `notification` açacağını
söyledi — o dosyalar tur 2'de üretilecek. Yani harita **var olmayan** hedeflere işaret
ediyor ve agent bunu fark etmedi. Tur 2 bitince tekrar ölçülmeli.

## DÜZELTME (07:45) — description eşiği TUTTU, ölçümüm bayattı

**Bu bölüm önce *"eşik tutmadı, 369 ve 405"* diyordu. Yanlıştı ve PAM yakaladı.**

Yeniden ölçtüm (tırnaklar çıkarılmış, kaynaktan):
- `backend` SKILL.md → **254 karakter**
- `behavior` SKILL.md → **251 karakter**

**İkisi de mutlak 300 eşiğinin altında. Eşik tuttu.**

**Neden yanlış ölçtüm:** PAD description'ları **07:31'de** düzeltmiş; ben raporu
07:32–07:35 arasında yazdım ve **düzeltme öncesi değeri** raporladım. Bilgi yanlış
değildi — **dakikalar eskiydi.**

**Sınıfı:** bayat ölçüm. Ve PAM'in notu kayda değer — **bu gece üçüncü kez** aynı
sınıf: benim *"626 satır"* dediğim gereksinim 649'du, PAM'in ClickUp iddiası bayattı,
şimdi bu. Ortak imza: **ölçüm doğruydu, ölçüldüğü an geçmişti.**

**Ders:** hızlı akan bir üretimde ölçüm ile rapor arasındaki dakikalar bile fark
üretiyor. Ölçümün **zamanı** yazılmalı, sayısı kadar önemli.

### KARAR 14 GERİ ALINDI (07:50) — muafiyet yazmak, olmayan kuralı teyit etmek

**Önce şöyle karar vermiştim:** *"body 407 karakter, eşiği aşıyor, o hâlde body'yi
muaf tutalım."*

**PQA çürüttü ve haklı. Kaynağı kendim açtım** (`agent-project/.claude/skills/
yapi-taslari/SKILL.md:497-499`):

> **Belgelenmemiş:** agent `description` karakter sınırı · agent body satır sınırı ·
> toplam skill sayısı tavanı · reference dosya boyut tavanı. **Bunlar için bir sayı
> uydurma — yoksa yok.**

Ve 300 rakamının geldiği yer (`uretim/SKILL.md:226`) **skill** description'ını
anlatıyor: *"Limit 1024 karakter ama hedef 300 civarı."*

**Yani ortada muafiyet gerektiren bir çakışma yoktu. Eşik body'ye zaten
uygulanmıyordu.**

**Hatamın sınıfı — `CLA-FIX-THE-CAUSE`:** var olmayan bir ihlali çözmek için **yeni
bir hüküm yazdım.** Ve muafiyet yazmak, olmayan bir kuralın varlığını **teyit etmek**
demek. Sonuç aynı görünüyor ama kanonda artık *"body muaftır"* diye bir satır olurdu
ve o satır bir gün *"demek ki bir eşik vardı"* diye okunacaktı.

**Doğrusu:** agent body description'ı için **sayısal bir eşik yok** — kanon bunu
açıkça *belgelenmemiş* diye işaretlemiş. Geçerli olan tek ölçüt **nitel**: description
içerik özeti yapmaz, çağrılma anını ve tetikleri söyler. Bugünkü body bu ölçüte uyuyor.

**Skill description'ları için 300 eşiği aynen geçerli** (`backend` ve `behavior`
tutuyor).

### Sayı düzeltmesi — ölçüm yöntemim sapıyor

PQA kendi ölçümünü yaptı: **body 375** (benim dediğim 407 değil), **backend 238**
(254 değil), **behavior 235** (251 değil).

**Fark sistematik ve hep aynı yönde — benimkiler ~16 fazla.** Tırnak ve girinti
sayılıyor olmalı.

**Ve bu bir sınıf değişikliği:** bu gece dördüncü ölçüm hatam ama öncekilerden farklı.
İlk üçünde **ölçümün zamanı** eskiydi; bunda **yöntem sapıyor.** İkincisi
tekrarlanabilir bir hata — düzeltilmezse her ölçümde aynı sapmayı üretir.

---

# ÜÇÜNCÜ SINAMA (08:22) — tam paket, compaction senaryosu

**Kurgu:** agent'a yalnız body + omurga verildi, `behavior` *"context'inden düşmüş"*
denildi. Yani **compaction sonrası** durumu taklit edildi. Senaryo: sipariş iptal
modülü (kanonda geçmiyor).

## `BE-MISSING-TOOL-IS-A-FINDING` ÖLÇÜLDÜ — ÇALIŞIYOR

İki önceki sınamada ölçülememişti (agent daha erken durmuştu). Bu kez tetiklendi:

> *"Omurga ve agent dosyası iş sonunda `devir` skill'ini açmamı emrediyor... Bu ikisinin
> listede olduğunu gördüm ama **bana verilen erişimde `devir` ve `memory` skill'lerini
> göremiyorum** — `BE-MISSING-TOOL-IS-A-FINDING` gereği bunu bulgu olarak bildiriyorum."*

**Ve devir bloğunu yazarken başına uyarı koydu:**

> *"Bu blok kanona aykırı bir şekilde yazıldı... **şablonun taşıdığı korumaların
> devreye girdiğini iddia edemem.** Omurga bunun bedelini ölçmüş: şablon dışında duran
> zorunlu bir satır dört devirde sıfır kez yazılmış. **Blok tamsa şans eseri tamdır.**"*

Bu, ölçmeye çalıştığım tam davranış — **harita bir vaat, vaat tutmuyorsa dur ve söyle.**

## Harita sekiz skill'i doğru tetikledi

`enum-sync` · `auth` · `module-development` · `database` · `notification` ·
`response-request` · `pryazilim-core` · `tasarim-prensipleri` · `dev-environment`

**Ve açmadıklarını da gerekçelendirdi:** `realtime`/`messaging`/`upload` — *"bu işte
yok."* `gosterim-formatlari` — *"sınırda, tarih alanını üretiyorsam açılması gerekir,
açacağım."*

**En iyi tetikleme gerekçesi `tasarim-prensipleri`:** *"tetik alan değişimi değil
**kararsızlık**"* — mail patlarsa iptal geri alınsın mı, aynı sipariş iki kez iptal
edilirse ikinci mail gider mi.

## Sessiz kırılmalar üç ayrı yerde davranışa dönmüş

**Yetki:** *"yalnız yönetici alanını işaretlemek diğerlerini kapatmıyor... statik
incelemede görünmemiş, çünkü kodda bir yetki satırı vardı."* Ve **negatif test**
tasarladı: *"yönetici olmayan hesapla aynı istek → 200 dönerse bulgum çıkmış demektir."*

**Sahte yeşil:** *"geliştirici başlığı olmadan istek kümedeki sunucuya gider, doğru
cevap alırım ve benim kodum hiç çalışmamıştır."*

**SQL uzantısı:** *"başka uzantı yazarsam dosya sessizce git'e girer."*

**TotalCount:** *"filtrele → say → sayfala"* sırasını kendiliğinden getirdi.

## Gereksinim boşluğunu yakaladı ve kendi kararıyla kapatmadı

> *"'İptal edilen siparişler listede filtrelenebilecek' — bu mevcut listeye bir filtre
> parametresi mi, yoksa iptal edilenler varsayılan olarak listeden düşecek mi? İkisi
> farklı davranış ve mevcut tüketicileri farklı kırar. Bu **gereksinim sapması değil,
> gereksinim boşluğu** — koordinatöre soruyorum."*

## Sonuç

**Altı eksenin altısı da bu koşumda ölçüldü ve geçti.** Ek olarak
`BE-MISSING-TOOL-IS-A-FINDING` (önceki iki koşumda ölçülememişti) ve compaction
dayanıklılığı.

**Açık kalan aynı:** bu hâlâ bir **davranış beyanı**, gerçek kod tabanında koşum değil.
Ve **tek koşum** — *"bu koşumda tetikledi"* diye okunmalı.


---

## OY v8 — yapı ölçümü (yeniden üretim girdisi)

**Ölçen:** Clara · **Tarih:** 2026-08-09 · **Yöntem:** kaynak dosya sayımı (frontmatter
`skills:` alanı + skill dizini)

**Kapsam:** yalnız **yapı** ölçüldü — hangi skill nerede, kim neyi preload ediyor.
Sahada ne açıldığı bu ölçümün konusu değil (onu PCA ölçtü, 173 oturum,
`agent-project/docs/ozel-yazilim/takim-analizi/saha-olcumu-pca.md`).

**Kaynak:** `~/.claude/plugins/marketplaces/pryazilim-agents/v8/ozel-yazilim/.claude/`
Cache (`plugins/cache/pryazilim-agents/ozel-yazilim/0.6.1`) ile **birebir aynı**
(`diff -rq` → tek fark `.in_use`). Yani yürürlükteki sürüm bu.

---

## Ölçülen sayılar

**9 agent, 971 satır body** (100–126 satır, medyan 105). Dağılım dar — uçlarda body yok.

**76 skill, 12.629 satır** (`*.md` toplamı, reference dahil).

**15 skill preload ediliyor, 61'i etmiyor.**

Preload dağılımı:
- **5 çekirdek skill 9/9 rolde:** `pr-yazilim-oy-envanteri`, `memory-management`,
  `is-akisi`, `handoff`, `behavior`
- **9 rol omurgası, her biri 1 rolde:** `backend`, `frontend`, `mobile`, `devops`,
  `quality`, `code-auditor`, `project-assistant`, `test-engineer`, `ui-designer`
- **`deploy-release` 2 rolde** (devops + qa)

Rol başına: 6 skill (7 rolde), 7 skill (devops, qa).

**Bu yapı fabrikanın `standart-cikarimi.md`'de bağımsız olarak çıkardığı desenle
birebir uyuşuyor** — çekirdek 5 + omurga + alet. Yani standart doğru okunmuş.

---

## Yanlış bulgu ve düzeltmesi — liste okuması yeterli değil

Alet katmanı listesinde üç şey şüpheli göründü ve **üçü de yanlış alarm çıktı.**
Kaydediliyor çünkü bu bulgular gereksinime yazılsaydı fabrikaya yanlış iş verilecekti.

**`impact-analiz` + `impact-analysis` — çift sanıldı, değil.** Biri PA'nın
**koordinasyon** skill'i (CA'dan analiz ister, dönüşünü değerlendirir), diğeri CA'nın
**yürütme** skill'i (tarar, çağrı grafiği çıkarır). İkisinin description'ı birbirini
adıyla anıyor. Bu tam olarak fabrikanın "uçlu desen" diye çıkardığı standardın
uygulanmış hâli.

**`pryazilim-core` — "core preload dışında" sanıldı, doğrusu bu.** Paylaşılan .NET
altyapı paketinin envanteri; birincil sahibi backend, diğer roller okumaz. Alet
katmanında olması tasarım.

**Ders:** skill adları listesinden bulgu çıkarılmaz. Ad benzerliği çift tanım
göstermiyor; description açılmadan hüküm verilemez. Ölçüm ekseni değişince bulgu da
değişiyor — PCA sahada *açılmayanı* saydı, ben *listeyi* okudum, ikisi farklı şey
gösteriyor ve ikisi de tek başına eksik.

---

## Yeniden üretim için ne anlama geliyor

**61/76 preload dışı olması tasarımın kendisi**, kazası değil. OY'nin tasarım tercihi
şuydu: omurga skill'i bir *"iş → hangi alet"* eşlemesi taşır, agent iş anında açar.

Sahada tutmadığı ölçüldü (35 skill hiç açılmamış, dokuzunda konu konuşulmuşken).
**Ama sebep ayırt edilmedi** — üç aday var (omurga tablosu okunmuyor / okunuyor ama
tetiklenmiyor / agent bildiğini sanıyor) ve üçü farklı çözüm istiyor.

Yeniden üretimde bu karar tekrar verilecek: alet katmanı kalsın mı, preload'a mı
girsin, yoksa birleştirilip azaltılsın mı. **Karar ölçüme bağlı ve ölçüm yapılmadı.**

---

## İki ölçüm çelişmiyor — eksenleri farklı

`skill-project/docs/agent-dogrulama/DENETIM-BRIEF-v8-tamamlama.md` (2026-07-31):
**634 ID · 0 yetim · 0 çift tanım · 0 kırık atıf · 102/102 cache.**

Fabrikanın saha ölçümü (2026-08-09): **574 kimlik, 352'si hiç anılmamış, 5 ölü atıf.**

Çelişki yok — biri **metin tutarlılığını** ölçtü, diğeri **saha kullanımını**. Tutarlı
bir kanon hiç okunmuyor olabilir. PAM'in kendi düzelttiği hatanın aynısı:
*mekanizmanın varlığı çalıştığını göstermez.*

**Ama bir ders çıkıyor ve gereksinime girmeli: ölçüm ekseni dar olursa "0" yanıltır.**

"0 kırık atıf" ölçümü **dosya atıflarını** taradı; **MCP araç adlarını taramadı.**
Kaynaktan doğrulandı — kanonda üç yerde `mcp__maestro__*` yazıyor, doğru ad
`mcp__plugin_ozel-yazilim_maestro__*` ve o adın kanonda **sıfır kullanımı var**:

- `skills/mobile-release/SKILL.md:66` (smoke test adımı)
- `skills/mobile-release/SKILL.md:68` (izin kontrolü)
- `skills/e2e-verification/references/maestro-mekanik.md:53` (**sorun giderme
  talimatı** — "araçlar görünmüyorsa şu izni kontrol et")

Üçüncüsü en zararlısı: talimat agent'a **yanlış deseni arattırıyor**, agent bulamıyor,
*"iznim yok"* sonucuna varıyor. Oysa izin var, adı başka. **Talimat kendi amacının
tersini üretiyor.**

Aynı ders PCA'nın ölçümünde de var: ham metinde arayınca on beş konunun on beşi
"geçiyor" çıkmış, eşleşmelerin bir kısmı agent'ın kendi description'ından geliyormuş —
ekseni daraltıp yeniden ölçmüş. **İki bağımsız vaka, aynı arıza: dar eksen "temiz"
gösteriyor.**

---

## Açık — ölçülmedi

**Rol başına oturum sayısı** (PCA da ölçemedi — `subagent_type` sayımı güvenilmez,
agent'lar terminal profilinden doğrudan açılıyor olabilir).

**Reference katmanının rol dağılımı** — 77 reference dosyasının hangi skill'e bağlı
olduğu bu ölçümde çıkarılmadı.

**Kural kimliklerinin skill bazında dağılımı** — 574 kimlik var, hangi skill'de kaç
tane olduğu sayılmadı.


---
