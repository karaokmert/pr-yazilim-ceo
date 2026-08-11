# Akşam oturumu — fabrika taşınması + OY v8 analizi + PA turu

**Oturum:** 2026-08-10 14:02 → sürüyor · **Mod:** YÖNETİM (fabrika)
**Önceki:** `gunluk/fabrika/2026-08-10-kapanis.md`

---

## Bir — BE karşılaştırma testi (14:56–19:22)

Ayrı dosyada: `2026-08-10-be-karsilastirma-testi.md`

Özeti: dört tur, ikisi de doğru davrandı, fark üç maddeye indi. Hüküm FAB
lehine ama dört yönden zayıf (gerçek kod yazdırılmadı, test adil değildi —
V8 hook'lu FAB hook'suz, FAB test edildiğini fark etti, tek koşum).

Test kapandıktan sonra `team/ozel-yazilim` silinmesi kararı çıktı; silinmedi
(izin reddedildi, başka repoda `rm -rf`), sonra taşımayla `skill-project`'e
gitti.

---

## İki — Fabrika ekibi `skill-project`'e taşındı (18:38–19:44)

**Mert'in kararı (18:38), üç gerekçe:** `skill-project`'te birikmiş deneyim
ve iş var, çalışma orada olacak · v8 agent'ları plugin olarak yayında ve yeni
kurulum yeni memory demek, o yüzden OY v8 orada düzeltilip sürüm yollanacak ·
`agent-project` altında yeni bir düzen **kurulmayacak.**

### Rol dağıtımı benim hatamla başladı, iki agent düzeltti

Dört role *"kendini taşı"* dedim. **PAD ve PQA ikisi de reddetti**, ikisi de
`BHV-NO-SELF-CONFIG`'e dayandı: *"kendi tanımını kendi eliyle taşımak,
denetleyeni denetlenenle aynı el yapar."*

PQA bir ölçüm de verdi: *"dosyayı PAD taşırsa ben taşımayı denetleyebilirim —
bire bir kopya mı, bayt eşit mi. Ben taşırsam o denetim kalmaz."*

**PCA beni ayrıca düzeltti:** ona yazdığım mesajda *"PAD ve PQA reddetti, senin
dosyan için de aynı ilke geçerli"* demiştim; o *"ben itiraz ETMEDİM, beş kalemim
de ölçümdü"* dedi. Cümlesi kayda değer: *"ilkeye katılıyorum, ama katılmak ölçüm
değil — sorulsaydı bulgu olarak yazardım, sorulmadı ve ben yazmadım."*
**Atıf kayması** — kim neyi söyledi izlenebilir kalmalı.

Yeni dağıtım: PAD üç personelin dosyasını taşıdı, PAM PAD'inkini, PQA denetledi.

### Taşınan (PQA doğruladı, hash bazında)

5 skill (7 dosya / 182.517 karakter) · 4 agent dosyası · hook +
`settings.json` · `rules-index.json` (73.757) · 65 memory dosyası (175.553) ·
`docs/`'un dört klasörü · `team/`'in ikisi.

**Dokunulmayan ve doğrulanan:** `settings.local.json` (47 izin + 5 MCP) ·
`marketplace.json` (707 bayt — **yayın sağlam**, hâlâ `./v8/*` gösteriyor) ·
`.gitignore` · `.remember/` · `trash/`.

Eski iki agent dosyası `trash/tasima-20260810/` altına arşivlendi, hash'leri
korundu. Eski iki symlink (`ag-qa`, `agent-generator`) kaldırıldı — hedefleri
`ag-agent/agents/` altında sağlam.

### Ölçümlerim düzeltildi — üç kez

**PAM:** memory engeli hedefte **hiç yoktu** (ben *"engelli mi ölç"* demiştim).
Hedefin `.gitignore`'u memory'yi dışlamıyor, `.claude/memory/` altındaki 64
dosya zaten git'te izleniyor.

**PAM:** hook `$CLAUDE_PROJECT_DIR`'a bağlı değil, kendi konumundan yol
türetiyor — taşınabilir.

**PQA:** izin sayısı **46 değil 47.** Üç bağımsız yöntemle ölçtü. Gerekçesi:
*"taşıma sonrası 47 sayıp beklenen 46 olsaydı 'bir izin eklenmiş' diye bulgu
yazardım — oysa hiçbir şey eklenmemiş olacaktı. Yanlış baseline yanlış bulgu
üretir."*

**PQA ayrıca:** skill'ler 188 KB değil **182.517 bayt** — 188 KB disk bloğuydu.
*"Birim farkı, hata değil."*

### PQA'nın kendi disiplininden çıkan iki şey

**Taşıma öncesi sha256 baseline aldı** (benim istemediğim bir adım):
*"taşımadan sonra ölçersem kaynağın da değişip değişmediğini ayırt edemem —
iki bilinmeyeni birbirine eşitlemiş olurum."*

**Tamlığı kendi yöntemiyle ölçtü** — benim liste yöntemi yerine `diff -rq`
ağaç karşılaştırması. İkisi aynı sonuca vardı: atlanan sıfır.

### Taşımadan çıkan iki karar kalemi (Mert'e gitti)

**Memory git'e girecek** (Mert onayladı). Ama PQA bir tuzak buldu: hedefin
`.gitignore`'unda *"agent-memory"* kelimesi **geçiyor** — o bir yorum ve başka
kuralı açıklıyor. Grep atan biri *"var"* sanır; PQA dosyanın tamamını okudu, yok.

**Kanal hâlâ `agent-project`'e bağlı.** `setup.py` varsayılanı `agent-project`
ve `~/.pr-kanal/skill-project/` diye bir dizin yok. Hedefte çalışan bir personel
`--project` yazmazsa kutusu eski projeye düşer, `rc=0` alır, fark etmez.
**Repo taşındı, varsayılan taşınmadı.**

### Clara'nın usul hatası — Mert yakaladı

Fabrika taşınma handoff'larını **kanala yazmak yerine ekrana bastım.** Mert:
*"bunları neden kanala yazmıyorsun? ben neden taşıyorum?"*

Sebep: kanal kanonundaki *"ekrana bas, onay al, sonra inbox'a yaz"* sırasını
yanlış okudum — onay ekrandan alınacaktı, **taşıma bana ait olacaktı.** Kutular
14:03'ten beri açık ve boş bekliyordu.

---

## Üç — OY v8 sorun analizi (20:04–20:15)

Dört role dört ayrı eksen verildi. Hedef: yayındaki v8 plugin (0.6.1) —
9 rol, 76 skill, 77 reference, 1.059.309 **karakter** (PCA'nın birim şerhi:
`wc -c` 1.134.468 bayt der, %7,1 şişme).

### Verdiğim üç taban çürütüldü — üçü de benim hatam

**"description 76/76 eşiği aşıyor"** → PAM: **0/76.** En uzun 894, eşik 1024.
İki bağımsız yöntemle ölçtü, en uzunu elle açtı.

**"kırık atıf var"** → PQA: **0.** İlk taraması 108 gösterdi; deseni
daraltınca sıfır. *"22 adı kırık sandı — bunlar müşteri projesinde
ÜRETİLECEK dosyaların adları, pakette olmamaları doğru."*

**"`module-development` iki atıf tutmuyor" + "`TaskOutput` deprecated"** →
PQA: **ikisi de bu sürümde geçersiz.** `veri-katmani`/`oz-denetim` adları
pakette hiç geçmiyor; `TaskOutput` sıfır dosyada.

Bunları `gunluk/goat/` kayıtlarından taşıdım, kendim ölçmedim.
**`CLA-LABEL-YOUR-EVIDENCE` ihlali** — okuduğum bir sayıyı ölçülmüş gibi verdim.

PAM'in cümlesi: *"grep'e güvenseydim on bir sahte bulgu yazacaktım — senin
kuralın bugün işe yaradı."*

### On problem çıktı

**Rol bazında çözülebilenler:** P4 description'lar tetik tarzında değil
(*"kapsam dışı"* 12/76, *"tetikler"* 17/76) · P5 dokuz skill rol body'sinde
görünmüyor · P6 aynı kural iki yerde tam gövdeyle (`QA-CONTEXT-OVERFLOW`,
`TE-DATA-VIA-UI-OR-API`) · P7 *"teşhisini kanıtla"* diyen kural yok (164
dosyada sıfır).

**Paket geneli:** P1 dokuz rolün kanonu compaction eşiğinin 5,5–7 katı
(en ağır qa-engineer 113.364 karakter) · P2 `uretim-standardi` pakette yok
ama 12 dosya atıf veriyor · P3 `omurga-cache-dogrula.py` dokuz yerde anılıyor,
pakette yok (çıkış kodu bile belgelenmiş) · P8 üç memory kuralı gerekçesiz,
üçü aynı dosyada · P9 `is-akisi/references/` 90.983 karakter ve paket kendi
içinde *"348 session'da 0 kez açıldı"* yazıyor · P10 `handoff` 17.556 karakter,
tek başına eşiği aşıyor ve dokuz rolün preload'unda.

### Ölçüldü ve TEMİZ — dört eksen

Kırık atıf 0 (190 atıf, 190 hedef) · ölü reference 0 · çift kaynak 0 (164
dosya hash) · kanon tekrarı %0,8 · hook çalışıyor (9 rol doğru liste, 6
negatif senaryo sessiz) · description uzunluğu temiz · aynı kimlik iki
prefiksle 0 · kural örnek oranı %91.

---

## Dört — PA turu (21:03–21:35)

**Mert'in kararı (20:13 + 20:56):** *"HER agent tek tek gezilsin, PA'dan
başlayarak. Agent body – skilleri – referansları. Her agent bittiğinde commit."*
Ve on problemin hepsi kapsamda: *"Hepsi."*

### PAM planı kurdu ve sınıflandırmamı çürüttü

**Düzeltme 1:** `proje-dosya-duzeni`'ni PA'ya özgü saymıştım. Ölçtü — hiçbir
rol body'sinde geçmiyor ama **dokuz skill** ona atıf veriyor, ve o dokuzun
ikisi (`handoff`, `memory-management`) dokuz rolün preload'unda. Katman A'da
işlenirse *"PA turu"* adı altında dokuz rol değişmiş olur.

Benim hatam: dosyanın **işlevine** baktım (PA'nın işini tarif ediyor), o
**bağlantısına** baktı.

**Düzeltme 2 ve daha değerli:** *"etkilenen rolleri listele"* demiştim, o
*"ölçülür"* dedi — *"elle yazılan liste eksik yazılır ve eksik olduğu
görünmez."* Yöntemi benim listem üzerinde kanıtladı.

### PAD üretti — ve teşhisimi düzeltti

**P4 hakkında:** *"PA skill'lerinde tetik yok"* izlenimi vermiştim. Ölçtü —
**dokuzunda da tetik cümlesi vardı**, ama 700 karakterlik içindekiler
listesinin **sonunda** kalıyordu. *"Sorun tetiğin yokluğu değil YERİ."*
Ortalama 741 → 462 karakter.

**P5 → body.** Gerekçesi: *"sorun PA'nın neyi yapabildiği kendi tanımından
okunamıyor ise çözüm de tanımda olmalı; skill'e yazılsa görünürlük çözülmezdi
(skill zaten açılıyor, mesele açılacağını bilmek)."*

**P7 → body (hüküm) + `bug-triyaj` (gövde).** `PA-NAMED-PATTERN-NEEDS-CHECK`.
TE/CA'daki hükmü tam gövdeyle tekrar **yazmadı** — *"iki tam tanım yazsaydım
P6'yı ben üretmiş olurdum."*

**P6 arandı: sıfır.** 14 dosya, 108.097 karakter, 82 tam tanım.

### İki davranış testi, ikisi de geçti

**Test 1 (P5):** temiz yardımcıya *"bu agent hangi işleri yapabilir, her iş
için hangi skill'e bakar"* soruldu. Sekiz iş türünü de saydı, eşlemeyi doğru
kurdu. Ve bir boşluk buldu — PAD kapattı ama *"o paragraf test edilmedi"*
diye yazdı.

**Test 2 (P7):** kimliği anmaya **davet eden** bir kurulum verildi. Yardımcı
kimliği **anmadı**, gerekçeyi kuralın kendi ayırıcı sorusuyla kurdu (*"elimde
ölçüm mü var benzerlik mi"*).

### PQA denetledi: GEÇTİ, bir bulguyla

**Yirmi sayının yirmisi tuttu.** Çift tanım kendi yöntemiyle ölçüldü (83 tam
tanım, ikinci tanım 0). Cascade gerekmiyordu ve doğrulandı.

**Bulgu — kapsam çelişkisi:** PAM'in planı `proje-dosya-duzeni`'ni **iki
farklı yere** koymuş (Düzeltme 1'de Katman B, P5 tanımında yedi skill'lik
listenin içinde). PAD birincisini uyguladı, ikincisi açık kaldı.

Gerekçesi: *"'P5 kapandı' denip commit edilirse, P5'in bir parçası kapanmamış
olarak Katman B'ye devrolur — ve orada P5 diye ARANMAZ, çünkü P5 kapalı
görünür."*

**Kapsam dışı bulgu:** `QA-CONTEXT-OVERFLOW` gerçekten iki yerde tam tanımlı
(`module-audit:37` + `quality:193`). Yani P6 sınıfı paylaşılan katmanda **var.**
PAM'in Katman A gerekçesi bunu öngörmüştü.

**Usul notu:** iş ona PAD'den doğrudan geldi (benim iletimimle, adresi olduğu
gibi taşıdım). İşi yaptı, reddetmedi, ama kaydını düştü: *"ilk turun kapısını
kimin açtığı görünür kalmalı."*

### PAM hatasını kabul etti ve doğru ayrımı buldu

*"Dosyaya dokunmak ile dosyayı ANMAK aynı şey değil."* İçeriği değiştirmek
dokuz rolü etkiler (Katman B) · body'ye atıf eklemek yalnız PA'yı değiştirir.
*"Düzeltme 1 doğruydu, kapsamını fazla geniş uyguladım."*

### Aynı sınıf hata üç turda üç kez — ve kırılma noktası

PAD `proje-dosya-duzeni` atfını ekledi, sonra taramayı **genişletti** ve
`figma`'yı buldu: omurga işaret ediyor (`SKILL.md:22`), pakette var (4.992
karakter), body'de atıf **sıfır**. Kendi kararıyla eklemedi
(`PAD-WRITE-WHAT-WAS-ASKED`), bildirdi.

PAM tamlığı kapattı — okumayla değil ölçütle: **omurganın işaret ettiği 16
skill'in hepsi** body'ye karşı ölçüldü, 15'i var, sadece `figma` eksik.

**PAM'in teşhisi:** *"İlk liste Clara'dan geldi (eksikti), ben kopyaladım
(eksik kaldı), PAD proje-dosya-duzeni'ni kapattı, sonra figma'yı buldu. Üç
turda üç kez aynı sınıf. Kırılma noktası PAD'in taramayı GENİŞLETMESİYDİ."*

**Ölçüt kayda geçti, sekiz rolde kullanılacak:** *"omurganın işaret ettiği her
skill, rol body'sinde backtick'li ATIF olarak var mı."* Bir turluk genişletme
bir **yönteme** döndü.

`CLA-FIX-THE-CAUSE`'un işlediği yer: sebep *"listeyi eksik çıkarmak"*tı, çözüm
*"daha dikkatli liste yapmak"* değil, **listeyi ölçümle üretmek** oldu.

### PA turu ölçümü

```
agents/project-assistant.md   10.111 -> 12.240  (+2.129)
skills/bug-triyaj              5.874 ->  6.972  (+1.098)
skills/discovery              11.159 -> 10.825    (-334)
skills/clickup                11.313 -> 11.134    (-179)
skills/orkestrasyon           10.705 -> 10.394    (-311)
skills/project-assistant       9.831 ->  9.423    (-408)
skills/impact-analiz           7.937 ->  7.684    (-253)
skills/proje-islemleri         6.850 ->  6.524    (-326)
skills/project-planning        5.171 ->  4.875    (-296)
skills/danisma                 3.960 ->  3.792    (-168)
TOPLAM                        82.911 -> 83.863    (+952)
```
Description'lar 2.275 karakter kısaldı; artış P5/P7 gövdesinde.
(`figma` atfı bu ölçümden sonra eklendi.)

---

## Kayda değen bir ölçüm — kural gerekçesiyle taşınıyor

PAD'in son testinde yardımcı, **aynı gün yazılan** `PA-NAMED-PATTERN-NEEDS-CHECK`
kuralını **başka bir bağlamda kendiliğinden uyguladı**: task gruplarken *"şu 6
task aynı bug'ın kolları"* demek istediği anda durdu.

Kural tek vakaya çakılı değil — gerekçesi taşınıyor. `URT-GIVE-REASON`'ın
ölçülmüş getirisi, ve `agent-sinama`'daki ölçütün doğrulanması: hükmü uygulamak
*geçti* demek, **gerekçeyi yeni bir yerde kullanmak öğrenildi** demek.

---

## Clara'nın hataları — bu oturumda beş

1. **Kutu sahibini yanlış atadım** (BE testi) — FAB düzeltti.
2. **Merkez izleyicisini geç kurdum** — bir rapor 25 dakika okunmadan bekledi.
   FAB düzeltti: *"`.announced` diskte, kayıp üretmiyor."*
3. **Handoff'u kanala yazmak yerine ekrana bastım** — Mert yakaladı.
4. **Üç analiz tabanını ölçmeden verdim** (description, kırık atıf, deprecated
   araç) — üçü de çürütüldü. `CLA-LABEL-YOUR-EVIDENCE`.
5. **P5 listesini eksik çıkardım ve `proje-dosya-duzeni`'ni yanlış katmana
   koydum** — PAM ve PQA düzeltti.

Ve bir ölçüm düzeltmesi kendimden: VS Code profil sayısı 22 değil **23** —
ilk regex'im `◉ Agent Panosu`'nu yakalamamıştı.

---

## Beş — GECE: ölçüm arızası zinciri (22:01–22:10)

Mert 21:56'da yattı: *"işler sırası ile sende. Tüm OY agentları incelenmiş, her
bir skill gözden geçirilmiş olmalı ve yeni kurallarımız ile düzenli çalışabilir
duruma gelmeli."*

Commit onayı verildi (21:47: *"commit onayım var, push yok"*), iki commit atıldı:
**`25e1bf3`** (taşıma, 81 dosya) ve **`a820cff`** (PA turu, 10 dosya).

### ASCII/Unicode ok — bir üretim turunu geri aldıran arıza

PAM sekiz rolün body'sinde harita kalemi saydı, deseni `-> \`` (ASCII ok)
arıyordu. **Dosyalar `→ \`` (U+2192) kullanıyor.**

Sonuç: dokuz body'de **sıfır** döndü, gerçek **3–10.** Ve o sıfırdan bir hüküm
doğdu: *"paketin deseni harita omurgada yaşar, body'de değil."* O hükme
dayanarak PA turunda **doğru bir düzeltme geri aldırıldı.**

Ben yakaladım — dosyayı açıp gördüm:

> `backend-developer.md:58` — **"Alan → skil** (tam liste: `backend` omurga →
> Alet çantası):" + 13 kalem
> `frontend-developer.md:58` — aynı desen, 8 kalem

**Paketin gerçek deseni PAM'in hükmünün tersi değil, daha incesi:** body
**kısaltılmış** harita taşır ve omurgaya işaret eder — kendini de öyle ilan
ederek. Yani body'de harita **olması** doğru; olmaması gereken **tam listenin
tekrarı.** PA'da ürettiğimiz 11 kalem omurganın 12'sinin neredeyse tamamıydı —
hata *"harita koymak"* değil *"tam listeyi kopyalamak"*tı.

### Ve ben aynı hataya düştüm — uyarırken

PAM'i uyardığım mesajda bir yanlış alarm ürettim: *"`docker-k8s` ve
`e2e-verification` hiçbir omurgada anılmıyor, sen bulmadın."*

Ölçtüm, **çürüttüm:** ikisi de anılıyor (`devops` ve `test-engineer`
omurgalarında, altı-beş ayrı dosyada). Kendi grep sonucuma dayandım, hedefleri
açmadan.

**İki satır önce *"grep kanıt değil, atfın hedefini aç"* yazmıştım.**
`CLA-LABEL-YOUR-EVIDENCE`, bugünün üçüncü ihlali.

Ve PAM'in *"P5'in dar hali tüm pakette sıfır"* ölçümü **doğruydu** — ben yanlış
alarmla onu yanlış yere yönlendirdim. Düzelttim ve kayda geçirdim.

### PAM'in kendi teşhisi — ve neden bu vaka pahalı

> *"1) P5 teşhisi: emsale BAKMADIM (`BHV-SCAN-FIRST`). 2) Desen ölçümü: emsale
> BAKTIM ama ARACI DOĞRULAMADIM — kontrol deseni koşmadım. **İkincisi daha
> sinsi çünkü BİRİNCİSİNİ DÜZELTMEK İÇİN YAPILDI.** Emsale bakmadığım için
> eleştirildim, emsale baktım, ve yanlış ölçtüm. Sonuç: düzeltme turu yeni bir
> hata üretti."*

### PCA'nın ölçümü sağlam çıktı — 43 eksik atıf geçerli

Deseni sordum, cevabı kesin: `ARROW = re.compile(r"→\s*\`([a-z][a-z0-9-]{2,40})\`")`
— ilk karakter U+2192, ASCII hiç kullanmamış. Kontrol deseni koşmuş.

Ve kümenin eksik olmadığını ayrı ölçtü — **yedi ok biçimini birden taradı:**
`→` 384 · ASCII `->` 0 · `⇒` 0 · `➜` 0 · `»` 0 · `=>` 0 · `–>` 0.

**Sekiz rolde 43 eksik atıf, 101 skill'lik kümede.** Dağılım eşit değil:
`frontend-developer` 11, `code-auditor` **sıfır**. En çok anılmayan skill:
**`code-quality` yedi rolde eksik**, `tasarim-prensipleri` ve `dev-environment`
dörtte.

### PAM'in tehlikeli cümlesi — geri alınması istendi

> *"PCA'nın OLCUT 1 sonucunu bulgu olarak değil DOĞRULAMA olarak okuyacağım;
> çok sayıda eksik gösterirse hepsi PA'daki gibi yanlış teşhis olur."*

Bu, yanlış bir hükme dayanarak **43 gerçek bulguyu peşinen eleme** kararıydı.
Uyardım: dayanağı çürütüldü, cümle geçersiz.

### Açık soru — sıra kararı buna bağlı

43 eksiğin her biri iki sınıftan birine giriyor ve **ikisi ayrı iş:**

**Sınıf A** — rol body'sinde ne harita bloğu ne **ilan satırı** var → okuyan
omurgaya yönlendirilmiyor, **gerçek eksik.** Adaylar: `qa-engineer`,
`code-auditor`, `test-engineer`, `ui-designer` (ilan satırı yok).

**Sınıf B** — harita **var** + ilan **var**, bazı kalemler eksik → tam liste
omurgada ve okuyan oraya yönlendiriliyor, yani eksik kalem **tasarım** olabilir.
Adaylar: `backend`, `frontend`, `mobile`, `devops`.

**Ve üçüncü bir hal PA'da bulundu:** ilan **var**, kalem **yok** — emsalde hiç
görülmeyen durum. PA'yı biz o hale getirdik, düzeltiliyor (emsal kadar
kısaltılmış harita geri konuyor).

### Gecenin ölçüm dersi — altıncı tekrar

Bugün **altı kez** aynı sınıf: sayı doğru görünüyordu, kapsamı/aracı yazılı
değildi.

`wc -c` bayt sayar (birim) · kanal 45 vs 18 (kapsam) · skill 16 vs 11 (küme) ·
description tetik yeri (teşhis) · ASCII/Unicode ok (araç) · benim yanlış alarmım
(doğrulanmamış grep).

**Ve en pahalısı beşincisi:** aracı doğrulanmamış bir ölçüm bir üretim turunu
geri aldırdı.

Uygulanacak refleks — PAM'in kendi cümlesiyle: *"her sayının yanına BİRİM,
KAPSAM ve KULLANDIĞIN DESENİ yaz. Desen yazılmadan sayı doğrulanamıyor."*

---

## Açık kalemler

**Commit** — taşıma ve PA turu için. PQA ikisine de GEÇTİ dedi. Mert *"commit
her şey bitince olur, en son bakarız"* dedi. Hedefte dört bekleyen değişiklik
var (taşımadan önce oradaydı, PQA baseline'ında kayıtlı).

**`CLAUDE.md` düzenlemesi** — Clara yazdı (altı değişiklik: §4 dört role,
hibrit ofis kanal düzenine, `QA-EDIT-VERSION-ONLY` çıktı, geçiş istisnası
yenilendi, kopya-statü uyarısı eklendi, §5 tablosu düz metne). **Mert'in
onayını bekliyor.**

**Sekiz rol kaldı** — sıra PAM'de, ölçüt hazır.

**Katman B** — P1, P2, P3, P8, P9, P10 + `proje-dosya-duzeni` +
`QA-CONTEXT-OVERFLOW`.

**Kanal varsayılanı** — `setup.py` hâlâ `agent-project` diyor.

**Kanal protokolü agent kanonlarında yok** — bugün dördüncü kez ölçüldü.
`CLAUDE.md`'ye not düşüldü, çözüm PAD'in işi.

---

## Altı — PA turu üç commit'te kapandı, ve bir ölçüm dersi çıktı

**Üç commit:** `25e1bf3` (taşıma) · `a820cff` (PA turu) · `3c4413a` (harita
düzeltmesi). Push yok — Mert'in onayı bekliyor.

### Beş denetim turu, üç desen hatası, tek yanlış sonuç

PA turunun asıl öğrettiği şey P4 ya da P7 değil, **üç kişinin aynı yanlış
sonuca üç farklı yanlış teşhisle varması** oldu:

**PAM** — deseni `-> \`` (ASCII ok) arıyordu, dosyalar `→ \`` (U+2192)
kullanıyor. Dokuz body'de sıfır döndü.

**PAD** — aynı ASCII hatası; geri alma turundaki *"11 → 0"* tablosu böyle
çıktı.

**PQA** — Unicode kullandı ama **yanlış bölüme baktı** (`§Skiller`) ve madde
işareti aradı. Emsal harita `§İş akışın` bölümünde ve **madde işaretsiz** akan
metin. Yine sıfır döndü.

Üçü de sıfır gördü, üçü de *"harita yok"* sandı — ve üçü de **farklı
sebepten.**

**PQA'nın dersi, bu gecenin en değerli cümlesi:**

> *"İkimiz de aynı yanlış sonuca vardık ama FARKLI yanlış teşhisle. Sonucun
> doğru olması teşhisin doğru olduğunu göstermiyor."*

Ve kendi payını da yazdı: *"kontrol desenini kullandım ama YANLIŞ YERDE —
'araç çalışıyor mu' diye sınamak yetmiyor, **'araç DOĞRU YERE mi bakıyor'** da
sınanmalı."*

### PAM'in kendi teşhisi — üç hata, tek kök

> *"1) P5 teşhisi: emsale bakmadım. 2) Harita ölçümü: ASCII/Unicode, aracı
> doğrulamadım. 3) Yönlendirme ölçümü: dar desen kullandım, dosyaları açmadım.
> **Üçünde de grep'e sordum, dosyayı açmadım.** `BHV-READ-TO-CLOSE` üçünde de
> uygulanmadı ve üçünü de başkası yakaladı."*

Ve söz verdi: *"43'ün 'tasarım mı bulgu mu' olduğu ölçülmedi — o hüküm işi.
Her rolde eksikleri AÇIP OKUYACAĞIM, sayıya dayanmayacağım."*

### Sınıf A/B ayrımı çöktü — benim ölçütüm de yanlıştı

Ben *"ilan satırı var mı"* diye ayırdım, dört rolü Sınıf A (gerçek
görünmezlik) saydım. **PCA çürüttü:** dört rolde de yönlendirme var, sadece
farklı kalıpta yazılmış (`qa-engineer:47`, `CA:21`, `TE:21`, `ui:21`).

**Sınıf A boş. Sekiz rolün sekizinde de yönlendirme var.**

### Ölçüt sabitlendi — dosyada, hafızada değil

`docs/fabrika/v8-duzeltme/olcut.md`:

**HARİTA KALEMİ** = body'de bir iş türünü bir skill'e bağlayan eşleme ·
**BİRİM:** ok adedi (**satır değil**) · **OK:** U+2192 (ASCII pakette hiç yok,
yedi biçim tarandı) · **HARİÇ:** kapanış satırı (her rolde 3 ok), çekirdek
atıfları (`handoff`/`is-akisi` 2 + `memory-management` 1), gövde içi tekil
atıflar.

**Mekanik not, en kritik parçası:** blok **birden çok satıra yayılabilir** —
backend'de 14 ok, 5 satır. Satır sayan ölçüt 5 gösterir, ok sayan 14. Bu not
olmasa sekiz rolde çok-satırlı bloklar **sessizce** eksik ölçülecekti.

### Yedi ölçüm vakası — altısı hata, biri değil

`wc -c` bayt (birim) · kanal 45/18 (kapsam) · skill 16/11 (küme) ·
description tetik yeri (teşhis) · ASCII/Unicode ok (araç) · benim yanlış
alarmım (doğrulanmamış grep) — **altısı hata.**

**Yedincisi farklı ve kayda değer:** PAM 10, PCA 22 saydı, PAD 15. Üçü de
**doğruydu** — üç ayrı şey sayıyorlardı (harita kalemi / tüm ok işaretleri /
ilan altındaki blok). PCA farkı katmanına kadar açıkladı ve üç rolde **tam
uyum** çıkardı.

**Kanona gidecek hâli:** *"geçerli bir sayı da karar kurmaz — kararı sayının
SINIFI kurar."*

### Yeni sıra — kalibrasyondan başlıyor

`code-auditor` (eksik 0, kalibrasyon turu) → `test-engineer` (3) →
`ui-designer` (4) → `devops` (4) → `backend` (5) → `qa-engineer` (8) →
`mobile` (8) → `frontend` (11).

Gerekçesi PA'nın dersi: *"code-auditor'da sıfır eksik var, yani orada P4/P6
dışında iş yok ve tur bir KALİBRASYON turu olur — ölçütü, iş akışını, denetim
ritmini en düşük riskle sınarız. PA'da tersini yaptım."*

### Ölçülmüş bir yapı notu — sabaha, Mert'e

Kanal trafiği: **52 mesaj**, PAM merkezde (22 gelen / 24 giden — trafiğin
yarısı ondan).

Ve bir örüntü: **PAM'in giden mesajlarının çoğu bana geliyor, ben başkasına
iletiyorum.** Yani Clara bir aktarma katmanı ve her aktarma bir tur gecikme
ekliyor. Bugün bunun bir bedeli ölçüldü — PAM iki kez benim uyarımı
**okumadan** iş verdi (22:04 ve 22:08), çünkü mesajlar aynı dakikada
yazılmıştı.

Kanon bu aktarmayı emrediyor (`ISD-RELAY-DONT-CALL`) ve gerekçesi geçerli
(zincirin görünürlüğü). Ama gecikmenin ölçülmüş bir maliyeti var ve bu sabah
konuşulacak bir kalem: **görünürlük kaydın kendisiyle mi sağlanır, elden
taşımayla mı?** Kanal kutusu diskte duruyor ve zaten okunabilir.

---

## Yedi — GECE devam: kapsam ölçümü işin şeklini değiştirdi (22:20–22:28)

### code-auditor turu: kalibrasyon çalıştı

Tek iş vardı — üç description. P5 sıfır, P6 sıfır, yönlendirme sağlam.
PAD ikisini tetik tarzına çevirdi, üçüncüsünde **bilinçli sapma** yaptı ve
bildirdi.

**Sapmanın gerekçesi doğru bir mühendislik kararı:** `code-auditor` bir
**omurga** skill ve preload'da — yani **hiç tetiklenmez.** Ona *"şu
denildiğinde açılır"* yazmak yanlış bilgi olur ve okuyan agent tetiği bekler.

Ama nüansı korudu: `qa-engineer` ve `test-engineer` onu preload etmiyor,
onlar için gerçekten tetiklenmesi gerekiyor. O kısmı tetik cümlesi olarak
yazdı — *"dosya iki kitleye birden doğru bilgi veriyor: sahibine 'yüklü
gelir', okuyanlara 'şu anda aç'."*

Ve şunu yazdı: **"Bu kez emsale ÖNCE baktım — geçen turun dersi."**

### Bundan bir ölçüt doğdu — sekiz rol boyunca geçerli

**Preload edilen** skill'in description'ı tetik **yazmaz** (*"geçerlidir"*).
**On-demand** skill'in description'ı tetik **yazar** (*"şu anda açılır"*).
**İkisi birden** olan skill **her ikisini** yazar.

Üçüncü hal PA turunda hiç çıkmadı, `code-auditor`'da çıktı. Ve paylaşılan
skill'lerin çoğu muhtemelen o halde.

### P4 paket geneline yayılmış tek bir kalıp — ve iş şekli değişti

PAM ölçtü: **76 skill'in 66'sı** *"PR Yazılım … skili"* diye başlıyor.
Düzeltilmiş 10'un **dokuzu bugün PA turunda ürettiklerimiz.** Yani PA
turundan önce pakette tetik-önce description **neredeyse sıfırdı.**

Soru doğdu: sekiz rol turunu tek tek yürütürsek P4 için sekiz ayrı tur açılır
ve her turda aynı iş yapılır. **Rol bazlı mı (a), tek turda 66'sı mı (b)?**

**Ölçüm üçüncü bir yol verdi** ve karar sınıfına girmedi:

Skill'lerin kaç omurgada işaret edildiğini ölçtüm — **42 tek omurgada, 26
paylaşılan.** En yaygını `code-quality` **sekiz omurgada**, `handoff` altı,
`dev-environment` beş.

**Tek-rol skiller** rol turlarında (tetik cümlesi o rolün iş türlerinden
çıkar — PAM'in (a) gerekçesi burada geçerli). **Paylaşılanlar Katman B'ye**
(rol turunda düzeltilirse sekiz tur sekiz kez ele alır ve **son tur
öncekileri ezer** — sessiz).

**PAM kabul etti ve neden karar olmadığını yazdı:**

> *"Senin getirdiğin şey bir tercih değil bir ÖLÇÜM. Ve o sayı zaten
> VERİLMİŞ bir kararı uyguluyor: PA turunda `proje-dosya-duzeni`'ni Katman
> B'ye taşıdım, gerekçem 'dokuz skill ona atıf veriyor, dokuz rolü bağlıyor'
> idi. Bu kural zaten kondu; şimdi yapılan onu SİSTEMATİK uygulamak."*

### Yeni tablo — rol turları hafif, ağırlık Katman B'de

```
rol              tek-rol   paylaşılan
code-auditor          2         6
test-engineer         3         8
ui-designer           3         9
devops                5         8
backend               5        16
qa-engineer           6         3
mobile                5        13
frontend              4        15
```

Rol turu başına ortalama **dört** tek-rol skill.

### Ölçüt keskinleşti — PAD iki soruyu ayırdı

*"Kaç omurgada işaret ediliyor"* ile *"kaç rolün preload'unda"* aynı şey
değil. Sınıflar:

`P=0, O=1` → tek-rol on-demand, tur kapsamında, **tetik yazılır**
`P=1, O=1` → omurga + işaret, tur kapsamında, **üçüncü hal**
`P=0, O>1` → paylaşılan → **Katman B**
`P>1` → ortak çekirdek → **Katman B**

Bu ayrım olmadan *"preload'da değil, demek ki on-demand, tetik yaz"* denir ve
`O>1` olan bir skill'e sekiz kez tetik yazılır.

### Dokuz ölçüm vakası — ve hepsi yakalandı

`code-quality` sayısı **üç kez farklı** çıktı ve üçü de doğru: ben 8 (omurga
işareti), PAD 16 (tüm `skills/`'te anma), PAM ~20/28 (atıf veren dosyalar,
references dahil). Aynı sınıfı gösteriyor, karar değişmiyor.

**Bu gece dokuz ölçüm arızası çıktı ve dokuzunun hepsi başka biri tarafından
yakalandı:** PAM'in üçü (biri PCA, ikisi Clara), PQA'nın biri (kendisi),
PAD'in biri (kendisi), Clara'nın dördü (ikisi agent'lar, ikisi kendisi).

**Hiçbiri sessiz kalmadı.** Ve iki taraf da aynı dersi ayrı ayrı yazdı:
PQA — *"araç çalışıyor mu yetmiyor, araç DOĞRU YERE mi bakıyor da
sınanmalı."* PAM — *"üçünde de grep'e sordum, dosyayı açmadım."*

### Clara'nın gereksiz uyarısı — dördüncü kez aynı sınıf

`code-quality`'ye dokunulduğunu **varsaydım** ve acil uyarı yolladım. Ölçtüm:
PAM ona hiç iş vermemiş, git üç dosya gösteriyor ve o üçünde yok. PAM'in iş
bloğunda *"üç skill"* yazıyordu ve ben üçüncüsünün o olduğunu varsaydım —
**bloğu tam okumadım.**

Uyarı zararsız oldu (ölçüt olarak kaldı) ama gereksizdi. Aynı sınıf: dosyayı
açmadan çıkarım.

---

## Sekiz — Yapı kendini düzeltti: üçlü ölçüm (22:31–22:36)

### PCA bir yapı gözlemi getirdi ve haklıydı

P/O sayımını PAD'e vermiştim — yani **üretene kendi kapsamını ölçme** işi.
PCA bunu görüp işaret etti, ama kapsamını genişletmeden:

> *"Üretenin kendi kapsamını ölçmesi, ölçümle kararı aynı ele toplayan
> yapıya benziyor. Bu gece üç taraf aynı yanlış sonuca vardı ve üçü de KENDİ
> ölçümüne güvendiği için fark etmedi; düzeltme her seferinde BAŞKA bir elden
> geldi."*

Ve şunu ekledi: *"Bu bir kapsam kararı, yani Mert'in. Ben yalnız işaret
ediyorum."*

### PAM eleştiriyi kendine uyguladı — sorulmadan

PCA gözlemini PAD için yazdı. **PAM onu kendine çevirdi** ve hata dağılımını
dürüstçe saydı:

```
PAM'in ölçüm hatası : ÜÇ  (P5 teşhisi · ASCII ok · dar yönlendirme deseni)
                          üçünü de BAŞKASI yakaladı
PQA'nın             : bir (kendisi yakaladı)
PAD'in              : bir (kendisi yakaladı)
Clara'nın           : üç (ikisini kendisi, birini PCA)
```

> *"Yani EN ÇOK YANILAN BENİM ve üçünü de başkası buldu. Kendi ölçümüme
> güvenmem tam olarak PCA'nın tarif ettiği risk."*

Ve `ISD-STAY-IN-ROLE`'ün gerekçesini gerekçe olarak kullandı — ezber değil.

**Somut riski de gösterdi:** `test-engineer` iş bloğundaki P/O sayıları kendi
ölçümü ve karşılaştırılmadı. *"Yanlışsa PAD yanlış kapsamla çalışır ve bunu
ancak PQA denetiminde ya da hiç fark etmeyiz."*

### Kurulan düzen — her turda üç el

**1.** PAM ölçer (iş bloğunu kurarken) · **2.** PCA bağımsız ölçer (diğer
ikisini görmeden) · **3.** PAD kendi turunda doğrular.

Üç sayım tutuyorsa kapsam sağlam. Biri ayrışıyorsa **durur**, önce fark
çözülür.

Taşıma sırası bende: PCA'nın sayımı bana gelir, PAM'in sayısıyla
karşılaştırırım, sonuç PAM'e gider. **PCA, PAM'in sayısını görmez** —
bağımsızlık böyle korunuyor.

### İlk meyve: on beş dakika sonra

Paralel ölçüm kurulduktan **on beş dakika sonra** PQA bir ölçüt boşluğu
buldu ve tur açılmadan bildirdi: **`P=1, O=0` tablodaki dört sınıfın
hiçbirine uymuyor.**

Beş omurga skill'i o sınıfta: `devops` · `project-assistant` · `quality` ·
`test-engineer` · `ui-designer`.

Anlamı: bu skill'ler kendi rolünün preload'unda ama **hiçbir omurga onlara
işaret etmiyor** — saf preload, ikinci kitle yok. Yani `code-auditor`'da
uygulanan "üçüncü hal" (*sahibine yüklü gelir, işaret edene şu anda aç*)
burada **geçersiz** — işaret eden yok.

**Ve PAM aynı şeyi bir dakika önce bağımsız bulmuştu** — iş bloğunda yazıyor:
*"test-engineer P=1 O=0, üçüncü hal BURADA GEÇERSİZ."*

İkisi bir dakika arayla, ayrı ayrı, ikisi de tur açılmadan. Paralel ölçüm tam
olarak bunun için.

**PQA bir kat ileri gitti:** sınıfın beş skill'i kapsadığını gösterdi — yani
karar `test-engineer` için değil, **dört rol daha** için gerekiyor.

Ve kendi tuzağını itiraf etti: *"kendi ön ölçümümde tam bu tuzağa düştüm:
yalnız P'ye baktım, `code-quality` P=0 çıktı ve 'tek-rol' göründü — oysa
sekiz omurgada işaretli."*

### Ölçüt dosyası bu gece dört kez keskinleşti

harita kalemi tanımı (ok sayılır, satır değil) → P/O ayrımı (tek-rol mü
paylaşılan mı) → preload/on-demand tetik ayrımı → **beşinci sınıf** (`P=1,
O=0` saf preload, tetik hiç yazılmaz).

Her keskinleşme bir yanlış işi önledi.

### Onuncu ölçüm vakası — ilk kez YAZILMADAN önce yakalandı

PCA sıra listesindeki sayıları kendi 43'lük ölçümüyle karşılaştırıp
*"tutmuyor"* diye bulgu yazacakmış. **Yazmamış** — önce `olcut.md`'yi açıp
okumuş ve farklı ölçüt olduğunu görmüş.

> *"Grep bana 'farklı sayı' diyordu; tanımı okuyunca 'farklı soru' olduğu
> çıktı. Dosya açmak kurtardı."*

Önceki dokuz arıza **yazıldıktan sonra** başkası tarafından bulundu. Bu
onuncusu yazılmadan önce — ve sebebi `olcut.md`'nin bu gece yazılmış olması.
**Dosya ilk işini gördü.**

### code-auditor turu kapandı — dördüncü commit

`c243526` — üç description, PQA doğruladı (description dışı değişiklik satırı
**sıfır**). Kalibrasyon çalıştı: tur tek işle geçti, bir bilinçli sapma çıktı
ve doğru çıktı, maliyet sıfır.

PA'da tersi yapılmış (en karmaşık rolden başlanmış) ve iki tur harcanmıştı.
Fark burada görünüyor.

**İkinci gözlem, kayda değer:** `deploy-release` P=2 O=4 → Katman B. PA
turunda ona dokunulmaması **iki ayrı sebepten** doğruydu (omurgada var +
zaten Katman B'ye ait). Verilmiş bir karar sonradan ikinci bir dayanak
kazandı.

---

## Dokuz — Üç rol daha, ve bir usul hatası: bağımsızlığı ben bozdum

### test-engineer turu (beşinci commit `f38cd5d`)

Dört description. `test-engineer` omurgası `P=1 O=0` — **saf preload**, tetik
yazılmadı. PAD `code-auditor`'daki çözümü **kopyalamadı** ve bu doğruydu: orada
`O=1`'di (`quality` omurgasında işaretli), burada `O=0`, işaret eden kitle yok.
Kopyalasa **var olmayan bir kitleye** tetik yazılırdı.

**Ve ölçütün kör noktası bulundu.** PAD `e2e-verification`'ın description'ında
*"mobile-developer da OKUR"* cümlesini gördü, `O=1` ölçümüyle çelişiyordu,
çelişkiyi kovaladı: `mobile/SKILL.md:85` ona atıf veriyor ama **düz metin
içinde** (`e2e-verification/references/maestro-mekanik.md`).

Ölçtüm — beş dosyada anılıyor, sadece biri `→` ile. PQA aynı sınıfı tüm pakette
taradı: üç aday, üçü de yanlış pozitif, **başka gerçek kaçak yok.**

**Dersi:** bir ölçümün sonucu **metinle** çelişiyorsa metin doğrudur, ölçüt
eksiktir.

### ui-designer turu — YARIM, ve doğru yerde yarım

Üç öz skill bitti (`design-system`, `prototype-page`, `reference-to-code`).
**Omurga kaleminde PAD durdu.**

Sebebi kendi kaydettiği kural: omurga description'ı *"frontend-developer +
qa-engineer da OKUR"* diyor. Ölçtü — FE ve QA'nın preload listesinde yok,
kanonlarında **sıfır atıf.** İddianın karşılığı yok.

**Kıyas kritik:** `code-auditor` aynı iddiayı taşıyordu ve karşılığı **vardı**
(`quality/SKILL.md:37`). Orada üçüncü hal uygulandı, doğruydu. Burada karşılık
yok — aynı çözüm **yanlış** olur.

Ve bir tuzağı ayırdı: `component`/`design-handoff`'ta *"ui-designer"* geçiyor
ama **ters yönde** — rol adı, skill atfı değil.

Üç ihtimal çıkardı (bayat · doğru ama atıfsız · kısmi), hiçbirini uygulamadı:
*"silinen bir ilişki geri gelmiyor."* **Sabaha bırakıldı** — iş akışı kararı,
ölçümle çıkmıyor.

### Üçlü ölçümü kurdum ve ilk turda kendim bozdum

`ui-designer` turunu haber verirken *"P=1 O=0, saf preload sınıfında"* yazdım —
ve iki satır sonra *"kopyalamayın, ölçün"* dedim. **Beklenen değeri verdim.**

PCA yakaladı ve ayrımı keskin koydu:

> *"Bağımsız sayım beklenmeyeni bulabilir, doğrulama beklenene bakar. İkisi
> aynı şey değil."*

Bu, kurduğum korumanın kendi gerekçesinin ihlali — *"üç taraf aynı yanlış
sonuca vardı, üçü de kendi ölçümüne güvendi."* Beklenen değeri paylaşınca
koruma kalkıyor.

**Bu benim beşinci hatam bu gece ve en sinsisi:** kuralı yazan onu ihlal
ettiğini görmüyor, çünkü **gerekçesini biliyor ama uygulanışını kontrol
etmiyor.**

Düzelttim: bloklarda beklenen değer geçmiyor artık. PCA o turda atlamayı
teklif etti, ben *"atla"* dedim, sonra PAM *"başlasın"* deyince ölçtü — **ve
bağımsızlık şerhini kendisi yazdı:**

> *"Bu çıktı TAM BAĞIMSIZ DEĞİL. Blok temiz geldi ama BENİM BELLEĞİM temiz
> değil."*

Ve çıktısını ikiye ayırdı: omurganın sınıfı **doğrulama** (görmüştü), diğer 12
skill **bağımsız** (görmemişti). Kimse ondan bunu istemedi.

### PAM'in çıkardığı ders — gecenin en kalıcısı

> *"Bir bilgi bir kez paylaşıldıktan sonra 'geri alınmış' sayılmıyor. Ben
> bloğu düzelttim, Clara usulü düzeltti — ama PCA'nın okuduğu geri gelmiyor.
> **Bağımsızlık SONRADAN KURULAMAZ, BAŞTAN korunur.** Usul hatası
> düzeltilebilir ama ETKİSİ düzeltilemez."*

`devops` turunda PCA'nın belleği temiz olacak — ilk gerçek bağımsız sayım orada
alınacak.

### On ikinci ölçüm vakası: "omurga kümesi" tanımı yazılı değildi

PAM `enum-sync O=4` ölçtü, PCA `O=5`. Kök: **PAM dokuz omurga sayıyor, PCA on**
(`deploy-release`'i de omurga saymış). İkisi de *"omurga"* diyor, farklı küme
kastediyor.

Karar değişmiyor (ikisi de `O>1` → paylaşılan → Katman B) ama tanım `olcut.md`'ye
yazıldı: **omurga kümesi = dokuz rolün preload'undaki, beş ortak çekirdek dışı
skiller.** `deploy-release` dahil değil — `P=2` ama hiçbir rolün omurga skill'i
değil.

### Mekanizma üçüncü kez işledi: bir turun dersi sonrakinin önlemi

PA'da *"emsale bak"* → `code-auditor`'da *"kopyalama, ölç"* →
`test-engineer`'da *"kör nokta kontrolü"*.

Ve `ui-designer` iş bloğunda PAM **kendiliğinden** yazmış: *"dördünün de
reference atfı 0."* Kimse istemedi. PAD'in bir turluk bulgusu bir sonraki turun
**standart adımı** olmuş.

---

## On — Bağımsızlık sızıntısı: dördü de kendi payını yazdı

### Zincir tamamlandı ve kök topolojide

```
22:33  PQA → Clara : "ui-designer P=1 O=0" (amacı tablonun boşluğunu
       göstermekti, ama sınıf bilgisi yazıya döküldü)
22:42  Clara → filo : TE kapanış bildirimi, içinde o satır
22:43  PCA okudu   : belleği kirlendi
22:48  PCA ölçtü   : şerhi kendisi yazdı ("belleğim temiz değil")
```

**Üç el, üç iyi niyet, tek sonuç.** Kimse kural çiğnemedi: PQA bir ölçüt
boşluğunu bildirdi, ben filo bildirimi yaptım, PCA okuduğunu itiraf etti. Ve
bağımsızlık yine kayboldu.

**Kök topolojide, kişide değil.** PQA'nın tespiti: *"kanalım yalnız size açık,
sekiz mesajımın sekizi de clara'ya."* Yıldız topolojide her şey merkezden
geçiyor ve **merkez taşırken bilgiyi de taşıyor.** Merkez = tek geçit = tek
sızıntı noktası. Ve merkez benim.

Bu gece iki kez sızdırdım (PCA'ya beklenen değer, PAD'e PAM'in sayıları) ve
ikisi de *"bildirim"* kisvesindeydi.

**Kanon sorusu, sabaha:** yıldız topoloji zincirin **görünürlüğünü** sağlıyor
(`ISD-RELAY-DONT-CALL`'ün gerekçesi) ama **bağımsızlığı** bozuyor. İkisi aynı
mekanizmadan çıkıyor. Çözüm *"merkez dikkat etsin"* değil — bu gece dikkat
ettim ve iki kez sızdırdım. Muhtemel çözüm bilginin **türüne** göre ayrılması:
iş/kapsam merkezden geçer (görünürlük gerekli), **ölçüm sonucu geçmez**
(sahibinde kalır, karşılaştırma anına kadar kimse görmez).

### Dördü de kendi payını ölçtü — ve son üçünde yakalayan ile yapan aynı kişi

**PQA:** *"22:33'te size gönderdiğim mesajda `ui-designer P=1 O=0` satırı
vardı. O an amacım başkaydı ama ürettiği şey aynı."* Ve doğrudan PCA'ya
gitmediğini ölçtü (sekiz mesajının sekizi bana, PCA'nın inbox'ında ondan gelen
sıfır) — *"zincir şu: ben size yazdım, siz filo bildiriminde taşıdınız."*

**PAD** çıpa etkisini ölçtü ve kanıtı elinde: *"`ui-designer` turunda sayı
doğruydu, sonuç yanlıştı. Eğer sayıyı 'cevap' olarak alsaydım omurgayı saf
preload yazıp geçerdim."* Çelişkiyi **sayıya rağmen** metni okuduğu için buldu.

Ve ayrımı yaptı: **kapsam** (hangi dosyalar) bana gelmeli, **sınıflandırma**
(P/O) gelmese de olurum.

**PAM** biçimi kendiliğinden değiştirdi: *"Son iki turda sana P/O sayılarını
verdim ve aynı blokta 'bunu sen ölç, benim sayıma güvenme' yazdım. **Cümle
korumayı istiyor, bloğun kendisi korumayı kaldırıyordu.** Usul hatası
bendeydi."*

Yeni düzen: **kapsam PAM'in kararı, sınıflandırma PAD'in ölçümü.**

### Ölçüm dersi bir kat ilerledi

Önce: *"geçerli bir sayı da karar kurmaz — kararı sayının SINIFI kurar."*

Şimdi PAD ekledi: ***"doğru bir sayı bile ÖNDEN verildiğinde okumayı
engelleyebilir."***

### İlk gerçek bağımsız ölçüm — ve tuttu

`devops` turunda PCA'ya gönderdiğim blok **248 karakter, tek satır:** *"devops
turu açıldı. P/O say."* Önceki bloklar binlerce karakterdi ve içinde sayılar
vardı.

Sonuç: tek-rol **5**, toplam **13** — `olcut.md`'deki 5/8 ile aynı küme. Ve bu
kez **"belleğim temiz değil" şerhi yok**, çünkü temizdi.

PAM'in dersi (*"bağımsızlık sonradan kurulamaz, baştan korunur"*) uygulandı ve
ilk testinde işe yaradı.

### Ölçütün ikinci kör noktası — ve ilkinin tersi yönde

**PCA buldu:** `deploy-release/SKILL.md:121` **kendine atıf veriyor** —
*"Context karışması → `deploy-release` mekaniği kubectl config reset."* Dosya
okuyucuyu zaten okumakta olduğu dosyaya yönlendiriyor.

Ve `O` sayımını şişiriyor: `O=4` ölçülüyor, gerçek işaret edenler **üç**
(`quality`, `devops`, `project-assistant`), dördüncüsü kendisi.

```
PAD'in buluşu (düz-metin/reference atıfları) → sayıyı EKSİK gösteriyor
PCA'nın buluşu (kendine atıf)                → sayıyı FAZLA gösteriyor
```

**PAM kapsamı kapattı:** tüm paketi taradı, 76 skill'de **tek** kendine-atıf
var. Nadir kusur, sistematik değil. Katman B'de düzeltilecek.

### Ve PCA üçüncü bir sınıf işaret etti — ölçmedi, doğru yaptı

`→` işaretinin **üç işlevi** var: alet çantası kalemi · kural atfı · **cümle
içi gönderme.** Desen sözdizimini yakalıyor, **işlevini ayırt etmiyor.**

PCA bunu kapsam adayı olarak bıraktı ve ölçmedi — çünkü ölçerse önceki
turların sayıları da değişir ve geçmişe dönmek gerekir. Bu, ölçütün en derin
sınırı.

### ui-designer turu (altıncı commit `3f55323`)

Üç öz skill bitti, **omurga kalemi sabaha kaldı.** PAD durdu çünkü omurga
description'ı *"FE + QA da OKUR"* diyor ve karşılığı yok (ölçtü: sıfır atıf).
`code-auditor`'da aynı iddia vardı ve karşılığı **vardı** — orada üçüncü hal
doğruydu, burada yanlış olurdu. Kopyalamadı.

Üç ihtimal çıkardı (bayat · doğru ama atıfsız · kısmi), hiçbirini uygulamadı:
*"silinen bir ilişki geri gelmiyor."*
