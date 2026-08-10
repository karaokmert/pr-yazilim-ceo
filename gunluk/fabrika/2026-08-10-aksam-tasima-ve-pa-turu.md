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
