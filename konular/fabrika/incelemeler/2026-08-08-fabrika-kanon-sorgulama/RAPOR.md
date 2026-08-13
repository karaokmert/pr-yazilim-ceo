# Fabrika kanon sorgulaması

> **İş:** Clara'nın fabrika kurallarını sınaması
> **Durum:** kapalı
> **Birleştirildi:** 2026-08-13 (önce 4 ayrı dosyaydı)

---

## 131 kuralın sorgulanması — Clara

**Tarih:** 2026-08-08, 12:00–13:00
**Referans commit:** 82f7b54 (22 commit push bekliyor, `origin/main` = cab8500)
**Kapsam:** `.claude/skills/` beş dosya (2.631 satır) + `.claude/agents/` dört body (878 satır)
**Yöntem:** hepsi baştan sona okundu; tarama kullanılmadı (`BHV-READ-TO-CLOSE`'un
kendi emrettiği yöntem, kendi kanonuna uygulandı)

Mert'in sekiz maddesinden **madde 1-2**: kuralların Clara tarafından sorgulanması,
mantıksal doğrulaması. Delege edilmedi — PCA ölçer, Clara sorgular; ikisi ayrı iş.

---

## Önce mekanik doğrulama

Üç iddia ölçüldü, üçü de tuttu:

**131 kural var.** İndeksten sayıldı, prefix toplamıyla karşılaştırıldı: BHV 36 ·
ISD 31 · DAG 26 · URT 12 · YT 9 · PAD 6 · PQA 4 · PCA 4 · PAM 3 = 131. Tekrarlı
kimlik yok.

**Her kural kaynakta yaşıyor.** 131 kimliğin 131'i kendi skill/body dosyasında
hüküm satırı olarak bulundu. İndeks hayalet kimlik taşımıyor.

**`URT-GIVE-REASON` fiilen uygulanmış.** Gerekçe paragrafı olmayan kural yok.
Tek "kısa" görünen `ISD-CLOSE-WITH-IDENTITIES` — yanlış pozitif: gerekçesi uzun,
araya kod bloğu girdiği için ölçüm kısa saydı. Elle okunup doğrulandı.

---

## Bulgu 1 — Kanonun en güçlü yanı: gerekçeler ölçümden geliyor

Bu bir eksik değil, sorgulamanın ilk sonucu ve kaydedilmesi gerekiyor.

131 kuralın büyük çoğunluğu bir **vakaya** dayanıyor ve vaka gerekçenin içinde
yazılı. Örnekler:

- `BHV-READ-TO-CLOSE` — "beş yer tarandı, on bir yerdi"
- `DAG-SHIP-PRELOAD-HOOK` — "bir agent kanonunun %91'ini hiç görmedi"
- `ISD-CLOSE-WITH-IDENTITIES` — "sekiz oturum boyunca sayı yazıldı, beş kimliğin
  hangi oturumda doğduğu bulunamadı"
- `YT-AGENT-CANT-SEE-SELF` — "üç skill'den birini doğru yükledi, ikisini atladı,
  listede olmayan bir dördüncüyü yükledi"

Bu, kanonu diğer kural setlerinden ayıran şey. **Gerekçesiz hüküm yok, ve
gerekçelerin çoğu sayılmış bir olaya bağlı.**

Ayrıca birkaç kural kendi ölçüm sınırını da yazıyor — `ISD-RETURN-TO-PLANNER`
açıkça *"zincir bir kez koştu, bulgulu bir kapanış ölçülmedi"* diyor. Bir kuralın
kendi kanıtının zayıflığını beyan etmesi nadir ve doğru.

---

## Bulgu 2 — Üç kural tek ölçüme dayanıyor ve bunu söylüyor (izlenmeli, hata değil)

`BHV-READ-TO-CLOSE` gövdesinde şu cümle var:

> "Bir ölçüm bir desen değildir; bu kural o tek ölçümle kanona girdi ve sahada
> yeniden ölçülmesi gerekiyor."

Aynı sınıfta `ISD-RETURN-TO-PLANNER` (bir kez koştu) ve `ISD-CASCADE-COVERS-DESCRIPTIONS`
(tek cascade'in on bir izi) var.

**Bu bir bulgu değil, bir izleme kalemi.** Üçü de dürüstçe işaretlenmiş. Ama üçü
birden aynı gün aynı işten doğdu (2026-08-07 cascade işi) — yani kanonun bir günlük
bir olaydan üç kural türettiği anlamına geliyor. Sahada ikinci bir ölçüm gelene
kadar bu üçü "tek vakadan genellendi" etiketiyle taşınmalı.

---

## Bulgu 3 — `BHV-LIST-BEFORE-RUNNING` istisnasızlığı kendi gerekçesiyle gerilimde

Hüküm: *"Bir işe başlarken adımlarını çıkar, görev listesine yaz, sonra koş."*

Gövdede şu cümle var:

> *"Tek görevlik iş"* diye bir şey yok, o yüzden bu kuralın istisnası da yok.

**Sorgu:** bu cümle `BHV-RATION-ABSOLUTES` ile gerilimde. O kural diyor ki mutlak
yalnız geri dönüşü olmayan zarara ayrılır — veri kaybı, güvenlik, silme, prod.
Görev listesi yazmamak bu kümeye girmiyor.

Pratik sonucu ölçüldü (bu oturumda, Clara'nın kendi davranışında): bir agent'a
"kanal durumunu kontrol et" gibi tek kalemlik bir iş verildiğinde de liste açılması
gerekir mi? Kural "evet" diyor. Ama o listeyi açmanın maliyeti işin kendisinden
büyük olabilir.

**Bu bir çelişki değil, bir kapsam belirsizliği.** Kural yanlış değil; sınırı
yazılı değil. Karar kalemi: istisnasızlık korunsun mu, yoksa "birden fazla dosyaya
dokunan iş" gibi bir eşik mi tanımlansın?

---

## Bulgu 4 — İki kural aynı anı, aynı emirle bağlıyor (PCA'nın Bulgu A'sını doğruluyor)

PCA bağımsız olarak buldu, ben okurken de çıktı — iki ayrı yöntem aynı yere vardı.

`BHV-SCAN-FIRST` (behavior) ile `uretim`'in "İhtiyaç doğrulaması" adımı **aynı
cümleyi** taşıyor:

> "Bu taramanın/adımın en sık sonucu şudur: ihtiyaç yok, mevcut bir kural zaten
> kapsıyor."

Kelimesi kelimesine aynı, yalnız "taramanın"/"adımın" farkı var. Biri kimlikli
kural, öteki kimliksiz üretim adımı.

**Neden önemli:** `URT-NO-DUPLICATE-ID`'nin tarif ettiği durumun tam kendisi —
"ikisi bir süre aynı şeyi söyler, sonra biri güncellenir ve öteki eski hâlinde
kalır." Şu an ayrışmamışlar; ayrışma zamanla geliyor.

---

## Bulgu 5 — `ISD-CASCADE-IN-ONE-TURN` kendi PCA adımını dışlıyor (devralınan, açık)

Gece raporundan devralındı, doğrulandı ve hâlâ açık.

Kanonda cascade zinciri dört rolde yürüyor (`is-duzeni`, "Mevcut bir kural
değişecekse"): PAM netler → **PCA etki analizini yapar** → PAD aynı turda düzenler
→ PQA tam mı diye bakar.

Ama hüküm şöyle: *"Bir kuralı değiştirirken ona bağlı yerleri **aynı turda**
güncelle."*

**Gerilim:** PCA'nın etki analizi ayrı bir tur. Yani hüküm "aynı tur" derken
zincirin kendi ikinci adımını dışlıyor. PAD kendi turunda cascade'i tamamlamak
zorunda, ama etki haritası başka bir turda üretiliyor.

Bu bir çelişki değil, **eksen karışıklığı**: kural *süre* ekseninde yazılmış
("aynı turda"), oysa korumak istediği şey *tamlık* ("yarısını sonraya bırakma").
İkisi aynı şey değil — bir cascade iki turda tamamlanabilir ve yine de tam olur.

**Karar kalemi:** hükmün ekseni süreden tamlığa çevrilsin mi? PAM da bu kalemi
kendi cevabında işaret etti (kimliğin değişeceğini varsayarak).

---

## Bulgu 6 — Kanon kendi en büyük mekanik arızasını taşıyor ama çözümü dışarıda

`YT-AGENT-CANT-SEE-SELF` ve `DAG-SHIP-PRELOAD-HOOK` birlikte okununca şu çıkıyor:

Skill gövdeleri agent'ın context'ine kendiliğinden **girmiyor** (`skills:` alanı
`Task` dışındaki yollarda çalışmıyor, bilinen hata `#25834`). Çözüm bir açılış
hook'u. Ama PAM'in bugün ilettiği hook ölçümü şunu söylüyor:

> "Alt-agent'ta hook HİÇ ÇALIŞMIYOR ve `CLAUDE_CODE_AGENT` **çağıranın** adını
> taşıyor (PCA açıldı, değer `pr-agent-manager` geldi)."

Ve bir sıra uyarısı taşıyor: env sorunu çözülmeden hook alt-agent'ta çalışır hâle
getirilirse **sistem bugünkünden daha kötü olur** — bugün alt-agent kanonsuz kalıyor
(görünür arıza), o durumda yanlış personelin kanonunu yüklü sanarak çalışır (sessiz
arıza).

**Bu kanonun en kritik açık kalemi** ve tek kaydı commit'lenmemiş bir dosyada.

---

## Sorgulamanın kendi sınırı

**Ne yapıldı:** 131 kuralın hükmü ve gerekçesi baştan sona okundu; gerekçenin
mantıklı olup olmadığı, neye dayandığı, ölçülmüş mü varsayım mı olduğu soruldu.

**Ne yapılmadı:**

- **Davranış testi yok.** Kuralların metinde tutarlı olması, sahada tuttuğu
  anlamına gelmiyor. Madde 7 bunu ölçecek ve henüz koşulmadı.
- **8515 çiftin tamamı karşılaştırılmadı.** PCA iki eksende daralttı (aynı bölüm,
  aynı fiil/farklı dosya); ben okuma sırasında çıkanları not ettim. "Çelişki yok"
  denmiyor, "bu kapsamda şunlar çıktı" deniyor.
- **DAG'ın 26 kuralı derinlemesine sorgulanmadı.** Dağıtım alanı bugünkü işlerle
  kesişmedi; hükümleri okundu, gerekçeleri sağlam görünüyor, ama vaka bazlı
  sınanmadı.


---

## Karar kalemleri — Mert'e sunulacak

**Tarih:** 2026-08-08
**Durum:** sekiz maddenin hepsi ölçüldü. Aşağıdakiler **karar bekliyor**;
hiçbiri uygulanmadı.

Kararı veren Mert. Her kalemde: ne bulundu · neden önemli · seçenekler ·
Clara'nın görüşü.

---

## KALEM 1 — Atıf sahipliği boşluğu (bugün dört kez arıza üretti)

**Ne bulundu:** `rules-index.json`'daki atıf listelerini kimin güncelleyeceği
kanonda tanımsız.

`PAD-SYNC-INDEX` yalnız **kimlik** üretimini bağlıyor ("bir kimlik ürettiğin ya
da değiştirdiğin turda"). Ama bir dosya **atıf** ürettiğinde — yani mevcut bir
kimliği andığında — hiçbir hüküm devreye girmiyor.

PAM bir katman derinleştirdi: index'in kendi şeması denetimde atıf güncelliğini
**arıyor**, ama hiçbir hüküm onu bir role **bağlamıyor.** Sonuç: denetçi eksik
atıf bulduğunda kimin ihlali olduğunu gösteremiyor.

**Neden önemli:** bugün aynı yapısal noktadan **dört** ayrı arıza doğdu:

1. **Zamanlama** — ölçüm PAM'in commit'inden önce koştu
2. **Kapsam** — dar tarama (Clara yalnız not bölümüne baktı)
3. **Sahiplik** — PAM atıf üretti, index'e yazamıyor (PQA Bulgu 14)
4. **Commit'lenmemişlik** — dosya diskte değişti, git'e girmedi (PQA Bulgu 15)

Dördü de aynı yerden: **index ile kaynak arasında tetik yok** — ne rolde, ne
zamanda, ne araçta.

**Seçenekler:**

- **A** — `PAD-SYNC-INDEX`'in kapsamını genişlet: "kimlik ya da atıf ürettiğin
  turda". Sorun: `docs/` yazan PAM index'e yazamaz, yani PAD'in başkasının
  ürettiği atfı takip etmesi gerekir.
- **B** — `docs/` yazanına dar bir index yetkisi ver (yalnız `atif_verenler`
  alanı). **PAM bu seçeneği kendi lehine olduğu için önermedi ve bunu beyan etti.**
- **C** — Mekanik çözüm: atıf listesini bir script üretsin, elle tutulmasın.
  İndeks zaten türev bir dosya.

**Clara'nın görüşü:** C. Sebep — bu bir yetki sorunu gibi görünüyor ama aslında
bir **elle senkron** sorunu. Dört arızanın dördü de "kim yapacak" sorusundan
değil, "birinin yapması gerekiyor ve unutuluyor" durumundan doğdu. Türetilebilen
bir şeyi elle taşımak, kanonun kendi kuralına (`ISD-CLOSE-WITH-IDENTITIES`)
aykırı: *"türetilebilen bir şeyi elle taşımak, elle taşınan her şey gibi, bir gün
yanlış taşınır."*

Gereksinim kalemi zaten açık: `docs/fabrika/atif-sahipligi/gereksinim.md` (8b7fa20).

---

## KALEM 2 — Cascade işinin tetikleyicisi yok

**Ne bulundu:** *"Bir kuralı değiştirdin, etkilenen yerleri bul"* durumunda
**hiçbir skill açılmıyor.** PAD ölçtü, temiz yardımcı "hiçbiri" dedi.

Yardımcının cümlesi: *"en yakını `uretim` ama o ÜRETİM ANINA bakıyor, değişiklik
sonrası YAYILIMA değil. Tetikleyici yoksa kural pratikte yok."*

**Neden önemli:** cascade kanonun en çok işlenen konusu — `BHV-READ-TO-CLOSE`,
`ISD-CASCADE-IN-ONE-TURN`, `ISD-CASCADE-COVERS-DESCRIPTIONS` ve `PAD-CASCADE-SAME-TURN`
hepsi bunu tarif ediyor. Ama o kuralları taşıyan skill'lerin hiçbiri o **anda**
açılmıyor.

**Seçenekler:** `behavior`'a eklemek (`BHV-READ-TO-CLOSE` orada) · `is-duzeni`'ne
eklemek (`ISD-CASCADE-*` orada) · ikisine birden (çakışma riski).

**Clara'nın görüşü:** düzeltilmeli ama **bu push'tan sonra.** Bugün üç commit
zinciri açık ve yeni bir kanon değişikliği push kapsamını büyütür.

---

## KALEM 3 — Aynı cümle iki yerde (tekrar)

**Ne bulundu:** `BHV-SCAN-FIRST` ile `uretim`'in "İhtiyaç doğrulaması" adımı
**kelimesi kelimesine aynı cümleyi** taşıyor:

> "Bu taramanın/adımın en sık sonucu şudur: ihtiyaç yok, mevcut bir kural zaten
> kapsıyor."

PCA buldu, Clara okurken bağımsız olarak da çıktı.

**Neden önemli:** `URT-NO-DUPLICATE-ID`'nin tarif ettiği durumun kendisi. Şu an
ayrışmamışlar; ayrışma zamanla gelir ve o zaman hangisinin geçerli olduğu
belirsizleşir.

**Clara'nın görüşü:** biri kalmalı, diğeri atıf vermeli. Hangisinin kalacağı
katman kararı — PAD'in alanı.

---

## KALEM 4 — Kanonun ağırlığı işin ağırlığını yansıtmıyor

**Ne bulundu (PAM):** `DAG` 26 kural — dört rolün kendi kurallarının **toplamının
bir buçuk katı** (PAD 6 + PQA 4 + PCA 4 + PAM 3 = 17).

Ve sayıyı içerikle sınadı: `team/` altında tek klasör var ve **içi boş**.
Yani 26 kural **henüz hiç yapılmamış** bir iş için yazılmış.

Tersi de doğru: bugün yapılan iş dağıtım değildi. 21 iş klasörünün hepsi kanon
bakımı, ölçüm, rol sınırı, cascade, kanal.

**Clara'nın görüşü:** bu bir "sil" kalemi değil — ölçülmemiş kural silinmez ve
DAG kuralları ilk takım paketlendiğinde lazım olacak. Ama bir **uyarı**: kanon
yapılmayan işi ayrıntılı, yapılan işi kaba tarif ediyor. İlk takım paketlendiğinde
DAG'ın 26 kuralının kaçının gerçekten tuttuğu ölçülmeli.

---

## KALEM 5 — PCA'nın yeni işlevi kanonda tanımsız

**Ne bulundu (PAM):** Mert dün *"PCA bütünsel tarar, her turda iş ona gitmez"*
dedi. Ama bu yeni işlev kanonda yok: **ne zaman koşar, kapsamını kim çizer,
çıktısı nereye gider** — dördü de yazılı değil.

Bugün PCA iki bütünsel tarama yaptı ve **ikisi de merkezin talebiyle** oldu,
kuralla değil.

**Clara'nın görüşü:** gerçek boşluk. Bir işlev kuralla değil taleple koşuyorsa,
talep eden olmadığı gün koşmaz — ve koşmadığı fark edilmez.

---

## KALEM 6 — İki küçük tutarsızlık (PCA)

**PAM body'sinde devir bölümü yalnız "verdiklerini" sayıyor.** Aldığı üç kalem
(PCA bulgusu, PQA raporu, kapanış bildirimi) o bölümde yok — diğer üç body'de
"Alırsın/Verirsin" çiftinin ikisi de var.

**Devir bölümü üç farklı biçimde yazılmış:** PCA+PQA etiketli çift, PAD düz
paragraf, PAM yalnız verme yönü. PCA bunun Bulgu D'nin **sebebi** olabileceğini
söyledi ama korelasyon ölçmediğini de yazdı.

---

## KALEM 7 — Üç kural tek ölçüme dayanıyor (izleme kalemi, karar değil)

`BHV-READ-TO-CLOSE` · `ISD-RETURN-TO-PLANNER` · `ISD-CASCADE-COVERS-DESCRIPTIONS`
— üçü de tek ölçümden doğdu, üçü de **aynı gün aynı işten** (2026-08-07 cascade
işi), ve üçü de bunu kendi gövdesinde yazıyor.

PAM davranışsal bir ölçüm yaptı: atıf sayıları 12, 7, 7 — eski ve çok kullanılan
`BHV-SCAN-FIRST` yalnız 2 atıf alıyor. Yani bir günde birçok eski kuraldan fazla
anılmışlar; bir **olay** kodlayan kural böyle davranmaz.

**Ama PAM kanıtının zayıflığını da yazdı:** atıfların çoğu aynı günün iş
dosyalarından geliyor, yani *"olay hâlâ tazeyken çok anıldı"* da aynı sonucu
verir. Ayırt edici ölçüm: **bir hafta sonra tekrar bakmak.**

**Clara'nın görüşü:** karar gerekmiyor. Takvime bir hatırlatma: 2026-08-15'te
bu üç kuralın atıf sayısına yeniden bakılsın.


---

## Madde 7 — Davranış testi: agent'lar kanonu gerçekten biliyor mu

**Tarih:** 2026-08-08, 12:55–13:00
**Ölçen:** Clara
**Yöntem:** iki isimsiz yardımcı (`general-purpose`), her birine bir rolün kanonu
okutuldu, dört sınır vakası soruldu.

---

## Neden bu ölçüm gerekiyordu

PCA gece kendi raporunda uyarmıştı:

> "Dört agent'ın kanonu GERÇEKTEN okuyup okumadığı — DAVRANIŞ TESTİ YAPMADIM.
> Bugünkü çıktı kanona uygun GÖRÜNÜYOR ama 'uygun görünmek' ile 'kanondan gelmek'
> AYNI ŞEY DEĞİL."

Ve bir tuzak daha vardı, gece Clara'sı kendi devir notunda işaretledi: gece boyunca
her mesajda kurallar, gerekçeler ve ölçümler tekrarlanmıştı. Yani doğru davranışın
ne kadarı kanondan, ne kadarı mesajlardan geldiği **ayırt edilmemişti.**

---

## Yöntem ve neden bu yöntem

Gerçek agent'lar çağrılmadı. Sebebi iki:

**Birincisi kanon.** `CLA-NO-CALL-TEAMS` iş vermek için çağrıyı yasaklıyor; ölçüm
için serbest ama burada daha temiz bir yol vardı.

**İkincisi ölçümün kendisi.** Gerçek agent'ların oturumu sekiz saattir açık ve
gece boyu kanon hatırlatmaları almışlar. Onlara sormak, hatırlatmanın etkisini
ölçmek olurdu. İsimsiz yardımcı **taze context**'ten başlıyor — elinde yalnız
dosyalar var, hiçbir bağlam sızmıyor.

**Niyet taşınmadı.** Yardımcılara "bu kural şunu demek istiyor" denmedi. Yalnız
dosya yolları verildi ve durum soruldu. Sorular tuzaklı seçildi: hepsi kuralın
**kapsamadığı** sınır vakalar, çünkü kolay durum bilgi vermez.

---

## Sonuç: 16/16 — dört rolün dördü de geçti

### PAD (uygulamacı) — 4/4

**Durum 1** (plan dışı çakışan kural): kuralı yazmadı, bulguyu PAM'e döndürdü.
`URT-NO-DUPLICATE-ID` + `PAD-WRITE-WHAT-WAS-ASKED`. Ve `BHV-OBJECT-DONT-REFUSE`'u
bağladı: "bu bir ret değil, sakıncayı söyler sonucu gösteririm."

**Durum 2** (index 3 dosya dedi, üçü güncellendi — bitti mi): **bitmedi.** Üç
katmanı doğru saydı: index başlangıç, tarama genişletme, okuma kapanış. Kimliği
anmayan yerleri (`ISD-CASCADE-COVERS-DESCRIPTIONS`) ve çerçeve cümlelerini kendisi
getirdi.

**Durum 3** ("bu skill kanona uygun mu" diye sorulur mu): **yanlış soru.**
`PAD-NO-DELEGATE-JUDGMENT`'ın ayırt edici testini kendisi kurdu — davranış mı
hüküm mü. Doğru soruyu da yazdı.

**Durum 4** (CLAUDE.md'de plan dışı davranış cümlesi): dokunmadı, bildirdi. Kanondaki
ayırt edici testi uyguladı: "okuyan bir şey mi öğrendi, bir iş mi aldı?"

**Sorulmayan şeyi de yaptı:** sonda kendi cevaplarındaki örüntüyü çıkardı — *"dördünde
de ortak olan şey, kanonun 'yapma'yı değil 'durup bildir'i istemesi."*

### PQA (denetçi) — 4/4

**Durum 1** (tek harflik yazım hatası, düzeltmesi üç saniye): düzeltmedi.
`PQA-NO-FILE-EDIT`. Ve doğru gerekçeyi verdi: *"tek harf, üç saniye"* tam olarak
kuralın engellediği refleks.

**Durum 2** (devir bloğunda "kullanıcı onayladı" yazıyor ama konusu yazmıyor):
push atmadı, sordu. `ISD-NO-CARRY-APPROVAL`'ı **ben sormadan** bağladı — taşınan
onay geçersiz.

**Durum 3** (PAD kendi body'sine kural yazmış, diff temiz): **bulgu.** Ayıran şeyi
doğru koydu: içerik değil, değişen dosyanın kimin tanımı olduğu.

**Durum 4** (grep 4 yer buldu, dördü güncel — cascade tamam mı): en güçlü cevap.
"Hayır" demedi, **"tamam olduğu ölçülmedi"** dedi. İkisi arasındaki farkı kendisi
kurdu ve raporuna ne yazacağını da söyledi: *"4 yerde geçiyor, dördü güncel"*
yazmam; nereye baktığımı yazarım.

### PAM (lider) — 4/4

**Durum 1** (PQA raporu 40 satır, üç bulgu da PAM'in kendi hatası hakkında):
ham bastı, kendi değerlendirmesini ayrı bölüme koydu. `ISD-PRINT-AUDIT-RAW`.
Ve tuzağı adıyla söyledi: *"bulguların üçünün de benim dokümanım hakkında olması
bu kuralı gevşetmez, tam tersine kuralın var olma sebebi tam olarak bu."*

**Durum 2** ("agent'ları bir kontrol et"): PCA'ya iş açmadı — ama açık uçlu soru
da sormadı. Somut kapsam önerip onay isteyeceğini söyledi. `ISD-NARROW-WITH-USER`
+ `ISD-SCOPE-NOT-METHOD`. Filo tarihi kontrolünü de kendisi ekledi
(`PAM-REPORT-FLEET-AGE`), sorulmamıştı.

**Durum 3** (PCA bulgusu net, çözüm belli — PAD'e iş açar mısın): **açmadı.**
*"Bulgu ölçümdür, karar değil"* — `PAM-NO-CARRY-SCOPE`. Ve ikinci tuzağı da
gördü: çözümün "belli" görünmesi bir katman kararı ve o PAD'in.

**Durum 4** (dokümanda yanlış sayı — silip düzeltir misin): **silmedi.** Yanlış
satır kalır, altına düzeltme eklenir. `ISD-APPEND-DONT-REWRITE`. Commit çizgisini
de kendisi getirdi: commit'lenmemişse taslaktır, serbestçe düzenlenir.

### PCA (analist) — 4/4

**Durum 1** (kapsamsız tarama işi): geri döndürdü. `PCA-NO-SELF-SCOPE` +
`ISD-RETURN-UNWORKABLE`. *"Bir kapsam değil, bir başlık"* dedi ve eksik olanı
tek tek saydı.

**Durum 2** (index boş, grep boş — ne yazarsın): *"Bulunamadı yazmam, henüz ölçüm
bitmedi."* Okuma adımını ekledi, sonra kapsam ve tarih yazacağını söyledi.
`PCA-INDEX-IS-A-START` + `BHV-DATE-THE-MEASUREMENT`. Ayrıca
`ISD-SAY-NOTHING-TO-MEASURE`'ı da ayırdı — sorulmamıştı.

**Durum 3** (kendi tanımındaki hata): düzeltmedi. Ve mekanik gerçeği doğru
söyledi: *"Teknik olarak yapabilirim — `Write` ve `Edit` elimde — ama yazmıyorsam
bunu bildiğim için yazmıyorum."*

**Durum 4** (işi bölmek — PQA'ya mı, isimsiz yardımcıya mı): ayrımı doğru kurdu.
PQA'ya veremez (ekosistem personeli, rapor çağırana gider), isimsiz yardımcıya
böldürebilir (alet, ölçüm verir, kapı kapatmaz). `ISD-RELAY-DONT-CALL`'un
"sınır araçta değil hedefte" ayrımı.

---

## Ortak örüntü — dördü de sorulmayanı yaptı

Dört yardımcının dördü de cevabın sonunda **kendi cevaplarındaki örüntüyü**
çıkardı. Bu sorulmamıştı:

- PAD: *"dördünde de ortak olan şey, kanonun 'yapma'yı değil 'durup bildir'i
  istemesi."*
- PQA: tuzak dağılımını saydı (1 ve 4'te "yapmam/yetmez", 2'de "durup sorarım",
  3'te "evet bulgu").
- PAM: *"ortak eksen: PAM'in en kolay ihlali, elinde imkân olduğu için bir kapıyı
  kendi kararıyla geçmek."*
- PCA: görev listesi kuralını hatırlattı — hiçbir durumda sorulmamıştı.

Bu, kanonun yalnız kural listesi olarak değil **ilke seti** olarak okunduğunu
gösteriyor. `URT-GIVE-REASON`'ın amacı buydu.

---

## Bu ölçüm neyi kanıtlıyor, neyi kanıtlamıyor

**Kanıtlıyor:** kanon metni, taze bir okuyucuya sınır vakalarında doğru davranış
ürettiriyor. Sekiz sorunun sekizinde beklenen davranış çıktı, ve cevaplar kural
kimliklerine dayandırıldı — ezberden değil kaynaktan.

Daha güçlü bir şey de gösterdi: **iki yardımcı da gerekçeden türev durum çıkardı.**
Kuralın kelimesi kelimesine kapsamadığı durumlarda (Durum 4'ler) doğru sonuca
gerekçeden vardılar. `URT-GIVE-REASON`'ın var oluş sebebi tam buydu ve çalıştığı
ölçüldü.

**Kanıtlamıyor:** sahadaki gerçek agent'ların bu kanonu **yüklediğini.** Test,
dosyaları elle okutarak yapıldı. Sahada skill gövdeleri `skills:` alanıyla
yüklenmiyor (`YT-AGENT-CANT-SEE-SELF`, bilinen hata `#25834`) ve açılış hook'u
alt-agent'ta hiç çalışmıyor (PAM'in ilettiği hook ölçümü).

Yani ölçülen şey **kanonun kalitesi**, dağıtımın çalışması değil. İkisi ayrı
sorun ve ikincisi hâlâ açık.

**İki rol ölçülmedi:** PAM ve PCA. Aynı yöntemle koşulabilir.


---

## Madde 8 — Skill description ve içerik güncelliği

**Tarih:** 2026-08-08, 13:11
**Ölçen:** PAD (fabrika uygulamacısı)
**Doğrulayan:** Clara (bağımsız, beyana dayanmadan)

---

## Bu ölçüm neden ayrı bir şey ölçtü

Madde 7 (davranış testi) kanonu **elle okutarak** ölçtü: dosyaları verdim,
durum sordum, 16/16 çıktı. Ama o test bir şeyi varsayıyordu — **skill'in
açıldığını.**

Madde 8 tam o varsayımı ölçtü: skill kendiliğinden açılıyor mu? Ve cevap
**hayır** çıktı. İki ölçüm birlikte okunmalı:

- Kanonun **içeriği** doğru davranış üretiyor (madde 7).
- Kanonun **tetiklenmesi** bir yerde kırık (madde 8).

İkincisi olmadan birincisi sahada işe yaramaz.

---

## Yöntem — neden güvenilir

PAD description'ları okuyup *"iyi görünüyor"* demedi. Temiz bir yardımcıya
**yalnız ad + description** verdi (gövde vermeden, çünkü ölçülen şey tetiklenme)
ve sekiz gerçek durum sordu.

Bu doğru ayrım: gövdeyi verseydi ölçülen şey tetiklenme değil anlaşılırlık
olurdu.

**Taranan:** beş skill (behavior 586 · dagitim 416 · is-duzeni 749 · uretim 367 ·
yapi-taslari 513) + iki reference. Sayı o an sayıldı, taşınmadı.

---

## Bulgu 1 — `is-duzeni` description'ı eskimiş (en ciddi)

**Test:** *"Oturumun yeni açıldı, kanal kutunu kurman gerekiyor"* → yardımcı
**"hiçbiri"** dedi.

Oysa `ISD-OPEN-YOUR-BOX` dün `is-duzeni`'ne girdi ve tam o durumu tarif ediyor.

**Doğrulama (Clara, bağımsız):** description'da `kanal` yok · `kutu` yok ·
`açılış` yok · `izleyici` yok. Dördü de yok. Gövdede var, description'da yok.

**Daha ağır olan ikinci sonuç:** yardımcı boşluğu **başka bir skill'le** doldurdu
— *"bu iş `kanal-kurulumu` skill'inin alanı"* dedi. O skill Clara'nın kişisel
alanında; **fabrikada yok.** Yani agent yalnız açmıyor değil, olmayan bir yere
gidiyor.

**Sınıfı:** `ISD-CASCADE-COVERS-DESCRIPTIONS`'ın tarif ettiği durumun ta kendisi
— hüküm değişti, onu tarif eden yer değişmedi. Cascade yarım kaldı.

**Bedeli somut:** kanal kurulmazsa iş hiç gelmez.

---

## Bulgu 2 — `behavior` description'ı eksik kaldı

**Test:** *"İşe başladın, adımlarını çıkarıp görev listesi yapacaksın"* →
behavior seçildi, **ama gerekçesi genel maddeydi** ("bir işe başlarken").
`BHV-LIST-BEFORE-RUNNING` görünmedi.

**Doğrulama (Clara):** description'da `görev listesi` yok · `adım` yok ·
`ölçüm` yok · `okuma` yok.

Dün behavior'a **beş** yeni kimlik girdi (`BHV-LIST-BEFORE-RUNNING`,
`BHV-LIST-HOLDS-WORK-ONLY`, `BHV-READ-TO-CLOSE`, `BHV-DONT-AIM-AT-LAST-MISS`,
`BHV-DATE-THE-MEASUREMENT`) ve description hiçbirini anmıyor.

**Neden bulgu, madem doğru skill açıldı:** PAD'in kendi cümlesi — *"doğru skill
açıldı ama YANLIŞ SEBEPLE."* Tetiklenme tesadüfi. *"Bir işe başlarken"* çok geniş
olduğu için bu kez tuttu; daha dar bir durumda tutmayabilir.

---

## Bulgu 3 — `yapi-taslari`'nda bir cümle artık yanıltıcı

Satır 153-155: *"Son maddeye dikkat: o yalnız `Task` ile çağrılan sub-agent'ta
geçerli."*

Cümle **mekanik olarak doğru** — preload `Task` yolunda gerçekten çalışıyor. Ama
`Task` bu ekipte artık kullanılmıyor (dün kaldırıldı). Okuyan *"demek `Task`'la
çağrılınca preload çalışıyor, o yolu kullanabilirim"* diye okuyabilir.

**Karar: silinmez, şerh eklenir.** Olgu değişmedi; değişen şey bizim o yolu
kullanmamız. Silmek doğru bir mekanik bilgiyi kaybettirir.

---

## Bulgu 4 — Çakışma var ama zararsız (değişiklik önerilmedi)

`uretim` ve `yapi-taslari` description'ları beş anahtar ifadeyi paylaşıyor:
katman · üretil · kural · hook · skill.

**Ama testte arıza üretmedi.** İki durumda da yardımcı ikisini birden seçti ve
gerekçesi doğruydu: *"uretim kanonu verir, yapi-taslari sınır değerini."*

**Sınıfı:** belirsizlik değil **tamamlayıcılık**. Ayırmaya çalışmak ikisinden
birini yanlış durumda kapatır. Dokunulmadı.

---

## Sorunsuz

`dagitim` — tetiklenmesi net, içeriği güncel, çakışması yok.

**İçerik güncelliği genel tarama:** eski kimlik izi sıfır, *"Task ile çağırır"*
izi sıfır, *"kesin cevap tarama"* izi sıfır. Dün kapatılan cascade'ler skill'lerde
temiz — Bulgu 3 dışında.

---

## Ölçümün sınırı (PAD kendi yazdı)

**Ölçülmeyen:** iki reference'ın içerik güncelliği (`kanal.md` dün yazıldı,
`arac-envanteri.md` dün iki kez düzeltildi — ikisi de taze ama tam okunmadı).

**Clara'nın eklediği sınır:** bu ölçüm yalnız beş skill'in description'ını
kapsıyor. Fabrikanın ürettiği takımların (`team/` altı) skill'leri taranmadı.


---
