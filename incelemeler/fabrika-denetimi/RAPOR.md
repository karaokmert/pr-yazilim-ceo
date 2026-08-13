# Fabrika denetimi — dört eksen

> **İş:** Sprint 1. iş · fabrikanın kendi kanonunu ölçme
> **Durum:** yarım — üç ölçüm açık
> **Birleştirildi:** 2026-08-13 (önce 5 ayrı dosyaydı)

---

## Eksen 1 — Teknik doğruluk

**Tarih:** 2026-08-06 · **Repo:** `/Users/karaok/p/agent-project`
**Yöntem:** isimsiz yardımcıya ölçüm verildi; her bulgu dosya:satır kanıtlı.
**Ölçüldü** (okundu değil): hook elle koşturuldu, atıflar `test -e` ile denendi,
index kimlikleri grep ile iki yönlü sayıldı.

## Sonuç — teknik kat büyük ölçüde sağlam

Kırık atıf **0**. Hayalet index kaydı **0**. Kayıt dışı kural **0**. Hook 4/4 agent'ta
doğru parse ediyor. Yani "teknik kırıksa mantık okunmaz" endişesi bu turda geçersiz —
mantık katmanı okunabilir durumda.

Sayılar:
- Atıf: 15 dosya yolu, 1 reference, 5 bölüm atıfı — hepsi var
- Frontmatter: 28 hücrenin 27'si dolu
- Index: 123 kimlik, iki yönde de sapma yok
- Hook: 4 agent koşuldu, skills listesi birebir doğru basıldı

## Bulgu 1 — `atif_verenler` alanı %74 boş (en ağır teknik bulgu)

`rules-index.json`'da 123 kuralın **112'sinde `atif_verenler` boş.** Ama gövdelerde
başka bir yerden anılan **38 tekil kimlik** var ve bunların **28'i index'te atıfsız.**

Örnekler: `YT-FILTER-BEATS-LIST` dört yerden anılıyor (`yapi-taslari/SKILL.md:331`,
`arac-envanteri.md:285,302,325`) — index'te liste boş. `PAD-TEST-BEFORE-HANDOFF` üç
yerden (`pr-agent-developer.md:105`, `is-duzeni/SKILL.md:187,363`) — boş.
`YT-ASSUME-BACKGROUND` üç yerden — boş. `DAG-MATCH-HOOK-FORMAT` iki yerden — boş.

**Neden ağır:** index kendi `ne_ise_yarar` alanında *"atif_verenler listesi cascade'in
haritasıdır"* diyor. Ve `pr-agent-qa.md:40-41` bunu bir **denetim ekseni** sayıyor
(*"atıf listeleri gerçeği gösteriyor mu"*). Yani bir kural değiştirileceğinde
"kimler etkilenir" sorusu index'ten cevaplanamıyor — cascade elle grep gerektiriyor.

Bu doğrudan **dördüncü ölçütü (bakım kabiliyeti)** vuruyor: *"6 ay sonra behavior'da
bir şey değiştirmek istiyorum, tüm takımlarda yapılmalı kararı alabiliyor muyuz?"*
Bugünkü cevap: haritaya bakarak hayır.

PCA bunu zaten biliyor (`pr-agent-context-analyst.md:86`: *"rules-index.json başlangıç
noktasıdır, kesin cevap değil"*) — ama index'in kendi beyanı ve PQA'nın denetim ekseni
bundan fazlasını iddia ediyor.

**Ek kusur — alan iki tipte veri taşıyor.** Dolu 11 kaydın bazısı dosya yolu, bazısı
`dosya — bölüm` bileşiği, bazısı ise **dosya değil kimlik** (`ISD-KEEP-STATUS` →
`['ISD-APPEND-DONT-REWRITE']`). Bileşiklerden biri doğrulanamadı:
`uretim/SKILL.md — kural yazımı bölümü` — dosyada "Kural biçimi" başlığı var (satır 26),
"kural yazımı" adlı bölüm yok.

## Bulgu 2 — PQA denetleyeceği kanonu elinde bulundurmuyor

`pr-agent-qa.md:30` denetim eksenini tanımlıyor: *"üretilen şey `behavior`,
`is-duzeni`, **`yapi-taslari`** ve kendi alanının kanonuyla çelişiyor mu."*

Ama `pr-agent-qa.md:5-8` — PQA'nın `skills:` listesi: behavior, is-duzeni, uretim.
**`yapi-taslari` yok.** Hook da onu basmıyor (elle koşturuldu, doğrulandı).

Yani denetçiye ölçüt olarak gösterilen kanon ne frontmatter'da ne hook çıktısında.
PQA `BHV-OPEN-SOURCE` gereği elle açabilir, ama body'si ona *"bu senin preload'ında"*
izlenimi veriyor.

## Bulgu 3 — hook'ta latent kırılganlık (fiilî arıza değil)

awk parser üç sentetik dosyayla sınandı. YAML **akış biçimi** (`skills: [behavior,
dagitim]`) **hiçbir şey döndürmüyor** — regex `/^skills:[[:space:]]*$/` satır sonu
istiyor.

Bugünkü 4 dosyanın hiçbiri o biçimi kullanmıyor, yani şu an çalışıyor. Ama biri
listeyi geçerli YAML akış biçiminde yazarsa hook sessizce boş basar ve hata vermez.
İhlali sessiz.

**Ayrıca hook'un `CAKISAN` dalı hiç sınanmadı** — `~/.claude/skills/` bugün boş
(2026-08-04'te temizlendi), o yüzden 4 koşumun hiçbiri o kod yolundan geçmedi.
Kod doğru kurulmuş görünüyor ama ölçülmemiş durumda.

## Bulgu 4 — PAM'de `tools:` yok, ve bu bilinçli

`pr-agent-manager.md` frontmatter'ında `tools:` satırı hiç yok (diğer üçünde var).
Kaza değil: `pr-agent-manager.md:134-137` gerekçelendiriyor — *"araç listesi bir niyet
beyanıdır, filtre uygulanmadan bağlayıcı değildir."* `arac-envanteri.md:329-330` de
kullanıcı kararı olarak kaydediyor (2026-08-04, elle silindi).

**Ama 3. işe etkisi var:** o iş PAM'den `Task` yetkisini almayı öngörüyor. `tools:`
satırı olmadığı için alınacak bir liste yok — kısıt sıfırdan yazılacak.

**Ve beyan disiplini tek biçimli değil:** aynı gerekçe geçerliyse PAD'in `Task`'ı da
listede olmak zorunda değildi, yine de yazılmış.

## Açık kalem — ölçülmedi

Hook'un asıl sorusu **hâlâ açık:** `CLAUDE_CODE_AGENT` gerçek bir alt-agent turunda
dolu mu? Elle koşturmada değişken **biz verdik**, yani hook'un mantığı doğru çalışıyor
— ama Claude Code'un o değişkeni alt-agent'a geçirip geçirmediği ölçülmedi.

Mert'in kararı (2026-08-06): PAM'i **Mert açacak**, açılışta ne gördüğü sorulacak.


---

## Eksen 2 — Mantıksal tutarlılık

**Tarih:** 2026-08-06 · **Repo:** `/Users/karaok/p/agent-project`
**Yöntem:** isimsiz yardımcıya ölçüm verildi; her bulguda iki çelişen yer, dosya:satır,
iki hüküm ve sonucu.

## Sonuç — dokuz çelişki, üçü ağır

Kanon iyi yazılmış ve kendi tuzaklarının çoğunu biliyor. Bulunan çelişkilerin **yedisi
aynı sınıftan**: hüküm bir yerde tam, atıfı başka yerde eksik. Yani arıza kural
kalitesinde değil, **cascade'in yarım kalmasında** — ki bu Eksen 1'in `atif_verenler`
bulgusuyla aynı kökü gösteriyor.

## En ağır üç

### 1. PQA'ya "yalnız sen yapabilirsin" denen iş, PQA'nın okumadığı dosyada

`dagitim/SKILL.md:117-119` — `DAG-BUMP-BY-AUDITOR`: *"Sürüm alanını yalnız PQA
değiştirsin... PQA'nın dosyaya el sürmeme kuralının **tek istisnası** budur."*

`pr-agent-qa.md:118-120` — `PQA-NO-FILE-EDIT`: *"Denetlediğin dosyaya el sürme."*
PQA body'sinde tanınan tek istisna `agent-memory` (satır 71). **Sürüm bump istisnası
body'de hiç anılmıyor.**

Ve `pr-agent-qa.md:5-8` — PQA'nın `skills:` listesinde **`dagitim` yok** (yalnız PAD'de).

**Sonuç:** PQA `plugin.json` sürümünü bump etmesi istendiğinde elindeki tek hüküm
`PQA-NO-FILE-EDIT` — istisnayı bilmediği için ya reddeder, ya da yaparsa kendi kritik
kuralını gerekçesiz ihlal etmiş olur. `rules-index.json`'da bu kuralın `atif_verenler`
listesi **boş** — cascade hiç kurulmamış.

İhlali sessiz ve bedeli ölçülmüş: `dagitim/SKILL.md:155-161` — *"altı oturumun dördü
eski sürümle koştu."*

### 2. Araç adı kanon boyunca `Task`, envanterde `Agent` — 20 yerde

`yapi-taslari/references/arac-envanteri.md:95` — *"`Agent` — kendi context penceresi
olan sub-agent açar."* Envanterde **`Task` adında araç yok** (`Task*` yalnız görev
listesi dörtlüsü: TaskCreate/Get/List/Update — bunlar sub-agent açmıyor).

Ama `Task` araç adı olarak 20 yerde kullanılıyor. Kritik olan:
`pr-agent-developer.md:4` — frontmatter `tools: ... Bash, Task, Skill`.

**Sonuç:** iki farklı ağırlıkta hasar. Birincisi mekanik — `arac-envanteri.md:323-324`
kendi hükmü: *"Listedeki hiçbir girdi bir araca çözümlenmezse agent genellikle hiç
başlamıyor"*, ve kısmi yanlış yazım **sessiz.** Yani PAD `Agent` aracını hiç almamış
olabilir ve `PAD-TEST-BEFORE-HANDOFF` (davranış testi) uygulanamaz durumda olabilir —
hata mesajı çıkmadan. İkincisi metinsel: `is-duzeni` "araç şurada var/yok" diye kural
gerekçelendiriyor ama adı yanlış olan bir araç üzerinden.

**Ölçülmedi:** `Task`'ın harness'ta `Agent`'a takma ad olup olmadığı. Burada gösterilen
şey kanonun **kendi envanteriyle çeliştiği.** (Clara notu: bu odada `Agent` aracı
çalışıyor, `Task` adı yok — yani takma ad olmama olasılığı yüksek ama ölçülmesi gerek.)

### 3. Sub-agent izolasyonu `PQA-GATE-BEFORE-PUSH`'u uygulanamaz kılıyor

`pr-agent-qa.md:125-127` — *"Onaylamadan push atma; onaylamak için de dosyayı
bütünüyle okumuş ol."*

Ama push **ayrı bir iş olarak, ayrı bir çağrıyla** geliyor (`pr-agent-qa.md:104,131`).
Ve `yapi-taslari/SKILL.md:148-149`: *"Bir subagent taze ve izole bir context penceresiyle
başlar... okunmuş dosyaları görmez."*

**Sonuç:** push turuna gelen PQA denetim turunda okuduğunu görmüyor. İki okuma mümkün
ve kanon hangisi olduğunu söylemiyor: (a) push turunda yeniden tam okur → denetim iki
kez yapılır, `ISD-CLOSE-THE-LOOP` akışı bozulur; (b) okumadan push atar → kuralın ikinci
yarısı ihlal edilir.

Bu bir yazım hatası değil, **mekanikle kuralın çarpışması** — çözümü kural metninde
değil akış tasarımında. 3. ve 6. işi doğrudan ilgilendiriyor.

## Diğer altı — hepsi yarım cascade

**4. `yapi-taslari` PAM'de Bash yok diyor, PAM body'si "Bash senin elinde" diyor.**
`yapi-taslari/SKILL.md:296-300` PAM'i *"Bash'i olmayan ama fiilen alan"* örneği olarak
kullanıyor — bu tarif `tools:` satırı silinmeden önceki hâle ait.
`pr-agent-manager.md:199-200` sahayı doğru tarif ediyor (commit `08a6410` düzeltmiş),
`yapi-taslari` düzeltilmemiş. PQA bu skill'i ölçüt sayıyor (`pr-agent-qa.md:30`).
`ISD-CASCADE-IN-ONE-TURN`'ün kendi ihlali kanonun içinde duruyor.

**5. "PAD tek yazma yetkisi" üç yerde delinmiş, biri tanınmıyor.**
Ana hüküm `is-duzeni/SKILL.md:73-74` mutlak: *"tek yazma yetkisi olan personel budur."*
Tanınan delikler: PAM `docs/` (satır 565-566 + `PAM-WRITE-DOCS-ONLY`), PQA/PCA memory.
**Tanınmayan:** PQA `plugin.json` sürümü — ürün dosyası, `docs/` değil, memory değil.
Fiilen dört elde yazma var; `is-duzeni` *"rol tanımının tek kaynağı burasıdır"* diyor
ama yazma yetkisinin tam listesi orada yok.

**6. `ISD-STAY-IN-ROLE` dördünü bağlıyor, PCA'nın bölümünde yaşıyor.**
`is-duzeni/SKILL.md:132` — kural `### PCA — analist` başlığı altında, ama gövdesi dört
rolden üçünü örnek veriyor. Index'te `bolum` alanı `"PCA — analist"`, `atif_verenler`
boş. `ISD-APPEND-DONT-REWRITE`'ın kendi uyarısı bu hataya birebir uyuyor: *"Yan cümlede
yaşayan kural index'ten bulunamaz."*

**7. `ISD-COMMIT-THEN-PUSH` PAD'in commit ettiğini söylüyor; PAD body'sinde "commit"
kelimesi hiç yok.** `is-duzeni/SKILL.md:92` hükmü koyuyor, `pr-agent-developer.md`'nin
tamamında kelime geçmiyor. `URT-BODY-BY-SILENCE`'ın ölçütüne göre (*"atlanırsa hata ne
zaman görünür"*) bu body'ye yazılması gereken sınıfta: PAD commit etmezse PQA'nın
denetleyeceği git durumu olmaz ve kayıp sessiz.

**8. `BHV-NO-SELF-CONFIG` dördünü bağlıyor, yasak yalnız ikisinin body'sinde.**
PAM (`:164-166`) ve PAD (`:49-55`) taşıyor; PQA ve PCA **hiç anmıyor.** Ve
`yapi-taslari/SKILL.md:291-295` ölçümü: *"PQA ile PCA'nın listesinde Write yok, sahada
beş dosya yazıldı ve hiçbiri hata dönmedi."* Yani ikisi de fiilen kendi tanımını
yazabiliyor ve ikisinin de body'sinde bu yasak yok.

**9. Kanonun kendi işaretlediği açık kalem — hook yazılmadı.**
`is-duzeni/SKILL.md:191-192`: *"Deterministik zorlama bir hook gerektirir
(`URT-HOOK-WHEN-DETERMINISTIC`) ve **henüz yazılmadı.**"* Yani
`ISD-KEEP-CHAIN-ONE-DEEP`'in (zincir tek katman) mekanik zorlaması yok.
`arac-envanteri.md:122-124` aynı boşluğu ikinci kez teyit ediyor.

`arac-envanteri.md:361-397` "Ölçülmeyenler" bölümü dokuz kalem sayıyor. Üçü sınır
tasarımını ilgilendiriyor — en kritiği: **`tools` hiç yazılmazsa arka planda ne kaldığı
bilinmiyor** (satır 372-375). Bu doğrudan PAM'i ilgilendiriyor, çünkü PAM'in `tools:`
satırı yok.


---

## Eksen 3 — Niyet uyumu

**Tarih:** 2026-08-06
**Ölçüt:** `incelemeler/fabrika-olcutu/kayit.md` — Mert'in kendi cümleleri (2026-08-03)
**Denetlenen:** `/Users/karaok/p/agent-project` — 4 body (642 satır), 5 skill (2.360),
1 reference, `CLAUDE.md` (210), `rules-index.json` (123 kural), `docs/filo/`

## Özet — beş ölçütün durumu

- **Sıfırdan üretme** — KISMEN, ve **en zayıf halka**
- **Alan bağımsızlığı** — KISMEN (beklenenden iyi; asıl boşluk 1 ile aynı)
- **Kestirmeden yapmama** — VAR, en iyi karşılanan
- **Bakım kabiliyeti** — VAR (yapı kurulmuş, 2026-08-02) ama **sıfır kez koştu**
- **İnsan okunabilir çıktı** — KISMEN, ve **dördüncü tekrara ulaşmış**

## 1. Sıfırdan üretme — KISMEN, en zayıf

Hedef cümle kanona geçmiş, tek yerde — `dagitim/SKILL.md:11`: *"Hedefin "OY hiç
yokken OY'u kurabilmek" olduğunu hatırla."*

**Var olan iki parça:**

*Paketleme* — `dagitim`'in 26 kuralı bir paketin sahaya inişini adım adım tanımlıyor
(`DAG-DECLARE-AGENTS`, `DAG-REGISTER-IN-MARKETPLACE`, `DAG-SHIP-INSTALL-DOC`,
`DAG-SHIP-PRELOAD-HOOK` — *"hook'suz plugin paketlenmez... doğuş koşulu"*,
`DAG-GATE-SETUP-SKILL`). Bu kısım tam.

*Parça üretimi* — `uretim/SKILL.md:258-338` bir iş akışı veriyor: gereksinim → ihtiyaç
doğrulama → üretim → test → denetim → dizin, üç kapıyla korunuyor. Ama bu **bir parça**
için: bir kural, bir skill, bir body. Soru daima *"bu bilgi nereye yazılır"* —
hiç *"bu takım kaç kişiden oluşur"* değil.

**BOŞLUK — bir takımın kendi tasarımı kanonda yok.**

Sıfırdan üretmenin en pahalı kararı: *bu alan için hangi roller gerekir, kaç personel,
hangi işler tek elde birleşir, devir hattı ne.* Bunun yöntemi hiçbir dosyada yok.
Üç yönden kanıt:

**(a) PAM'in kuruluş modu bir yöntem değil, bir tutum.** `pr-agent-manager.md:81-96` —
onbeş satır ve hepsi tutum: *"acele etmek zararlı... konuşarak çıkar... Günler
sürebilir; normaldir."* Bitiş testi tek: *"PAD bu gereksinimle katman kararı verebilir
mi?"* — katman kararı ise *"bu kural skill'e mi hook'a mı"* sorusu. **Bir takımın rol
mimarisinin doğru olup olmadığını ölçen hiçbir eşik yok.**

**(b) Rol mimarisinin tek girdisi PCA'nın dış araştırması, ve o bir ölçüm tarifi.**
`pr-agent-context-analyst.md:33-42` — *"Hangi roller var, ekip kaç kişi, hangi rol ne
kadar kritik, hangi işler tek kişide birleşiyor."* Bu, *"hangi roller var"* sorusunu
soran **tek** kanon satırı. Ama `PCA-NO-PROPOSE-RULE` (`:108`) PCA'yı bulguyu kurala
çevirmekten men ediyor. Yani PCA *"game dev'de şu beş rol var"* der; oradan *"bizim
takımımız şu üç agent olsun"* kararına geçen adımın yöntemi **yok.**

**(c) Fabrika bu boşluğu kendi kuruluşunda ismen tespit etti ve kapatmadı.**
`docs/fabrika/ekip-kurulumu/gereksinim.md:13-16`: *"**Yeni takım kurma işi
tanımsızdı.** Kanal inşa metodolojisi ve rol mimarisi tasarımı hiçbir belgede kimseye
verilmemişti. İş fiilen yapıldı ama yöntem yazılı değildi — yani **ikinci kez
yapılamazdı**."* Dörtlü kuruldu, boşluk açık bırakıldı.

**Yapısal kanıt — kanonun ağırlığı değiştirme tarafında.**
`is-duzeni/SKILL.md:149-153` kuruluş hattını **5 satırda** tarif ediyor ve iki farklı
işi aynı hatta koyuyor: *"Yeni bir takım kurulurken **ya da** mevcut bir kanona ekleme
yapılırken."* Hiçbir adım ikisini ayırmıyor. Buna karşılık üçüncü hat (`:267-327`,
"Dışarıda bir şey değiştiğinde") **60 satır**, 3 kural taşıyor ve tamamen kurulmuş
takımlara müdahale üzerine.

En keskin kanıt: `team/team-1-oy/` boş, `dagitim`'in 26 kuralı hiçbir gerçek paket
üzerinde koşmadı.

## 2. Alan bağımsızlığı — KISMEN, beklenenden iyi

İki ayrı soru var ve cevapları farklı.

**Yazılım DOMAIN terimleri — kanonda genel kural içinde YOK.** Sabit dize sayımı
(4 body + 5 skill + reference + CLAUDE.md): `backend` 2, `developer` 5, `müşteri` 1,
`yazılım` 1 (kurum adı hariç) — ve `frontend` 0, `API` 0, `.NET` 0, `React` 0,
`Prisma` 0, `Next.js` 0.

Geçtiği yerlerin **hiçbiri hüküm cümlesinde değil**, hepsi gerekçe içinde biçim örneği:
`dagitim/SKILL.md:242` (namespace formatı), `:391` (adlandırma örneği). Hükümler
alan-nötr — `DAG-NAME-BY-ROLE` *"Agent adı rolü söylesin"* diyor, bir marketing
takımında `content-strategist` yazmaya aynen uyar.

**123 kuralın hüküm cümlelerinin hiçbirinde yazılım domain terimi yok.** Ölçütün asıl
sorusu bu ve cevabı temiz.

**Ama yazılım ARACI varsayımı yoğun:** `plugin` 74, `script` 85, `push` 45, `repo` 46,
`JSON` 42, `commit` 12, `bash` 10, `grep` 8, `git` 3 — ve bunlar örnek değil, hüküm
cümlelerinin içinde (`DAG-VALIDATE-BEFORE-COMMIT`, `ISD-COMMIT-THEN-PUSH`,
`URT-NO-PUSH-WITHOUT-AUDIT`).

Bu ölçüt açısından **engel değil**: bir marketing ya da haber portalı takımı da Claude
Code plugin'i olacak, manifest yazacak, hook taşıyacak. DAG'ın 26 kuralı alan-bağımsız
ama araç-bağımlı, ve ölçüt aracı sorgulamıyor.

**Gerçekten anlamsız kalanlar — 2 kural + 1 sınır:**
- `ISD-APPEND-DONT-REWRITE` (`is-duzeni/SKILL.md:513`) — ayrım ölçütü *"commit"*.
  Git kullanmayan ortamda ayırıcı çizgi yok.
- `CLAUDE.md:199` — *"Gerçek proje koduna yazılmaz."* Kod olmayan alanda ne yasakladığı
  tanımsız (haber portalında ground-truth kod değil, yayın akışı).
- `behavior/SKILL.md:209` içindeki grep talimatı — gerekçe cümlesi, yumuşak.

**Asıl boşluk Ölçüt 1 ile aynı:** *fabrika bir marketing takımının rol mimarisini nasıl
çıkarır?* Tek cevap PCA'nın araştırma tarifi, ve dönüşüm yöntemi yok. Yani 1'in
zayıflığı 2'yi de aşağı çekiyor.

## 3. Kestirmeden yapmama — VAR, en iyi karşılanan

Bu ölçütü zorlayan kural yoğunluğu diğer dördünün toplamından fazla.

`BHV-NO-RUSH` (`behavior:38`) — *"Acele bir gerekçe değildir; hızlanman gerekiyorsa
kapsamı daralt, kaliteyi değil."* Gerekçesi ölçülmüş: *"skill açmadan commit'e giden
agent bilmiyordu değil — "kanonu hafızadan uyguladım" dedi. Bilgi vardı, zaman yoktu."*

`BHV-READ-FULL` (`:216`) — *"Parça okuma en tehlikeli okuma biçimi... Yarım okunmuş
dosyada bulunan "çelişki" genelde çelişki değil, okunmamış paragraftır."* Ve esnetme
yasağı: dosya büyükse **işi böl**, kuralı esnetme.

`BHV-OPEN-SOURCE` (`:61`) — *"Açmadığın kural seni yine de bağlar ama sende yoktur."*
`BHV-NO-GUESS` (`:207`), `BHV-CITE-RULE` (`:89`), `BHV-SCAN-FIRST` (`:251`),
`BHV-READ-THE-EXAMPLES` (`:119`), `BHV-FOUR-PHASES` (`:275`), `BHV-PROVE-DONE` (`:280`),
`BHV-BUILD-ON-FINDINGS` (`:227`).

Ve `behavior/SKILL.md:52-59` — kendini *"bu skill'in en önemli parçası"* diye
tanımlayan bölüm: *"agent'ta bilgi de var, muhakeme de var. Eksik olan **tetik**...
Kuralın önce açıldığı turlarda sıfır kullanıcı düzeltmesi çıktı; doğrudan işe girilen
turda beş düzeltme çıktı."*

Üretim kapıları mekanik olarak kesiyor: `URT-NO-PRODUCTION-WITHOUT-NEED`,
`URT-NO-AUDIT-WITHOUT-TEST`, `URT-NO-PUSH-WITHOUT-AUDIT`.

Mert'in *"belki günler alır ama detaylandır"* cümlesi `pr-agent-manager.md:81-88`'e
neredeyse birebir geçmiş.

**BOŞLUK (yumuşak) — "reponun en büyük hakimi olmalı" kısmı yazılı değil.**
PAM'in okuma yükümlülüğü **iş bazlı**: `:61-63` *"İşe başlarken docs/ altına bakarsın"*,
`:98` *"Kural yazma işi açmadan önce rules-index.json'a bakarsın."* İkisi de dar.
"Repoya bütün olarak hâkim ol" diye bir yükümlülük yok — ve dizin kanonda **türev**
olarak işaretli (`behavior:104`): PAM 123 kuralın hükmünü görür, gerekçelerini görmez.
Hâkimiyet bir *durum*, kanondaki her şey bir *refleks*.

## 4. Bakım kabiliyeti — VAR ama sıfır kez koştu

**Bu maddede önceki tespitim eksikti ve düzeltiyorum.** Ölçüt dosyası (2026-08-03)
bu ölçütü *"kısmen — refleks var, mekanizma yok"* diye kaydetmiş. **O tespit artık
geçersiz:** madde 2026-08-02'de kapatılmış, yapı kurulmuş.

Kanıt: `docs/fabrika/ekip-dogrulama/oturum-06-filo-bakimi.md` — Mert'in ölçüt
cümlesinin birebir karşılığı sorulmuş ve boşluk bulunmuş (`:16-18`): *"Kanon **tek
takım varsayıyordu.** Dışarıdaki bir değişikliğin birden fazla takımı ilgilendirmesi
hiç düşünülmemişti."* Kapatma: üçüncü hat + iki kural + PAM'e sorumluluk +
`docs/filo/durum.md`.

**"Kim sorumlu" — cevabı var ve isimli: PAM.** `pr-agent-manager.md:106-117` +
`PAM-REPORT-FLEET-AGE` (`:168`). Tetik mekaniği düşünülmüş: `oturum-06:56-65` bir
tuzak tespit ediyor — *"'ayda bir tara' diyen bir kural **hiç çalışmaz**; agent
çağrılmadan uyanamaz."* Çözüm: var olan tetiğe iliştir (PAM zaten `docs/` okuyor),
tarih eskiyse **söyle** — tarama başlatma, kararı kullanıcı verir.

**"N takıma nasıl yayılacak" — dört rolde tanımlı.** `is-duzeni/SKILL.md:267-327`:
PAM anlar → PCA etki analizi (*"arayacağı şey özelliğin adı değil, senaryosu"*) →
kapsam kullanıcıda (*"bir üretim kararı değil, bir **yatırım kararı**"*) → takım başına
kuruluş hattı. İki kural koruyor: `ISD-FIND-WHAT-IT-REPLACES` (`:302`) ve
`ISD-ONE-TEAM-PER-TURN` (`:316`).

**Ama mimari bedeli var.** `is-duzeni:269-270`: *"Kurulan takımlar bu repoda yaşamaz...
**Ortak bir çekirdek de yok**."* Bu Mert'in ölçüt oturumunda ortak çekirdeği
reddetmesinin kanona geçmiş hâli — ama sonucu şu: 8 takımda bir behavior değişikliği
**8 ayrı iş** ve `ISD-ONE-TEAM-PER-TURN` bunu zorunlu kılıyor. Karar alınabilir,
uygulaması 8 tur.

**Dört açık kalem — hepsi `docs/filo/durum.md`'de:**

*Hiç koşmadı.* `durum.md:8-14`: *"Kurulmuş takımlar — **Henüz yok**. Son filo taraması
— **Yapılmadı**."* `PAM-REPORT-FLEET-AGE` bir tarih karşılaştırması yapıyor ama
karşılaştıracak tarih yok. Kuralın davranış üretip üretmediği ölçülmedi.

*Kimlik çakışması — görülmüş, kuralı yazılmamış.* `durum.md:257-260`: *"İki takımın
kanonu aynı kimlik kalıbını kullanırsa (`BHV-NO-RUSH` iki farklı hükmü gösterirse)
atıflar sessizce yanlış kurala tutar... **ikinci takımda ölçmek ucuz, sekizincide
cascade demek**."* Tam Mert'in senaryosu.

*Plugin skill'i en düşük öncelikte.* `durum.md:271-275`: *"kullanıcı düzeyinde aynı adı
taşıyan bir skill varsa plugin'in kanonu **sessizce ezilir**."* Ölçülmüş arıza, teorik
değil. *"Takım kurulurken kontrol edilmeli"* — ama bu bir not, `dagitim`'in 26 kuralında
bu kontrol yok.

*`docs/` commit sahipliği tanımsız.* `durum.md:183-211` — PQA bunu **kanon boşluğu**
ilan etmiş, iki turda iki kez bildirmiş, bedeli ölçülmüş (`gereksinim.md` hiç commit
edilmedi). *"Boşluk hâlâ açık çünkü hüküm yazılmadı."*

## 5. İnsan okunabilir çıktı — KISMEN, dördüncü tekrar

Mert'in üç şikâyeti üç ayrı şeye işaret ediyordu; kanon **birine** cevap veriyor.

**Var olan — rapor biçimi (7 kural):** `BHV-SHAPE-REPORT` (`:371`, üç bölüm: özet,
kalemler, karar — *"kalemler bulgu başına tek satır"*, *"özeti okuyup yeterli
bulabilmeli"*), `BHV-NO-EVIDENCE` (`:384` — *"Kaç dosya okuduğun kullanıcının kararını
değiştirmez"*), `BHV-NO-REOPEN` (`:403`), `BHV-STAND-ALONE` (`:413` — *"Anlamak için
dosya açması gerekiyorsa mesaj işini yapmamıştır"*, ve koordinat yasağı),
`BHV-NO-ORNAMENT` (`:422`), `BHV-WRITE-AS-COLLEAGUE` (`:447` — ve dengeleme:
*"Kısalık gereksiz kelimeyi atmaktır, gerekçeyi atmak değil"*), `URT-NO-TABLE`
(`uretim:233`).

Soru sorma **içeriği** de var: `CLAUDE.md:127-130` (*"A mı B mi diye sorarsan kullanıcı
etkileri bilmek zorunda kalır"*), `pr-agent-manager.md:53` (açık uçlu soru yasağı),
`ISD-NARROW-WITH-USER` (`:326`).

**BOŞLUK 1 — "5 soru sordun, hepsi koca bir blok" şikâyetinin karşılığı yok.**
Kanonda soru **sayısını sınırlayan, tek tek soran ya da blok biçimini düzenleyen tek
kural yok.** Ve `BHV-SHAPE-REPORT` kendi kapsam cümlesiyle bu anı **açıkça dışarıda
bırakıyor** (`:373-376`): *"Bir soruya cevap verirken, ara bir bilgi paylaşırken ya da
konuşma sürerken üç bölüm kurulmaz."* Yani Mert'in üç şikâyetinden ikisinin geldiği an
kuralın kapsamı dışında.

**BOŞLUK 2 — uzunluk sınırı sayı olarak hiçbir yerde yok.** `CLAUDE.md:132` bir tutum
bildiriyor (*"Uzun blokları okutmak fayda değil zarar"*) ama kimliksiz, sayısal eşiksiz,
ve *"agent üretirken"* kapsamına yazılmış — yani **üretilen dosya için, kullanıcıya
giden rapor için değil.**

**BOŞLUK 3 — bugün dördüncü tekrarda ve iş hâlâ açılmadı.**
`docs/filo/durum.md:120-133`: *"**Dört oturumdur** aynı şikâyet geliyor... "bu kadar
uzun makaleyi okumak zorunda olunca önemli her şeyi kaybediyorum"... Önerilen yön:
raporu kısaltmak değil **biçimini değiştirmek** — bulgu üstte kısa, kanıt altta ayrı
bölümde. **Kapsamı çizilmedi, iş açılmadı.**"*

**BOŞLUK 4 — kanonun kendi içinde tanınmış bir gerilim.**
`ISD-PRINT-AUDIT-RAW` (`is-duzeni:56`) denetim raporunun özetlenmeden basılmasını
**zorunlu** kılıyor ve gerekçesi ölçülmüş (`:58-62`): *"o bulgu çoğu zaman PAM'in kendi
işi hakkında. Ölçüldü: üç bulgu çıktı, üçü de PAM'in hatasıydı."* Yani kullanıcıya
giden en uzun metin türü kısaltılamıyor, bilinçli. Çözüm önerisi var, kural yok.

## En zayıf ölçüt ve neden

**Sıfırdan üretme.** Sebebi kural eksikliği değil, **kanonun ağırlık dağılımı:**
paketleme çok ayrıntılı (26 kural, 416 satır), mevcut kanonu değiştirme çok ayrıntılı
(60 satırlık üçüncü hat + cascade zinciri) — ama bir takımın **kendi tasarımı**
hiçbir yerde yok. Elde olan: 15 satırlık tutum tarifi + PCA'nın ölçüm tarifi;
aradaki dönüşüm boş.

Ağırlığını artıran iki şey: fabrika bu boşluğu kendi kuruluşunda ismen tespit etti ve
açık bıraktı; ve `team/` boş — yani ölçüt yalnız kanonda eksik değil, **sahada bir kez
bile denenmedi.** Ölçüt 2 de aynı boşluğa dayanıyor, yani 1'in zayıflığı tek başına
kalmıyor.


---

## Eksen 4 — Yapısal düzen

**Tarih:** 2026-08-06 · **Repo:** `/Users/karaok/p/agent-project`
**Yöntem:** isimsiz yardımcıya ölçüm verildi; sayımlar `wc`/`grep` ile, kanıt dosya:satır.

## Boyut — iki dosya kendi eşiğini aşıyor

Skill'ler (satır/karakter):
- `is-duzeni` 612 / 34.762
- `yapi-taslari` 507 / 28.979
- `behavior` 469 / 26.628
- `dagitim` 416 / 24.052
- `uretim` 356 / 18.550
- `references/arac-envanteri.md` 397 / 19.207

Toplam **2.757 satır / 152.178 karakter.** Agent body'leri: PAM 209, PAD 179, PQA 136,
PCA 118.

`yapi-taslari/SKILL.md:472` kendi kanonunda *"SKILL.md gövdesi 500 satırın altında"*
diyor. `is-duzeni` 612 (%22 aşım), `yapi-taslari` 507 — **kendi yazdığı eşiği kendisi
aşıyor.**

Tavsiye eşiği ama etkisi somut: compaction'da skill başına 5.000 token sınırı var ve
kırpma dosyanın **sonunu** atıyor. `is-duzeni`'nin son bölümü
(`ISD-CLOSE-WITH-IDENTITIES`, satır 568-608, 40 satırlık gerekçeyle en uzun kural) uzun
oturumda düşme riski en yüksek konumda.

**Yapısal gözlem:** 2.757 satırın 2.360'ı (%86) reference'ta değil, **gövdede** — yani
her açılışta yüklenmesi gereken yerde. Tek reference dosyası var (5 skill'e karşı 1).

Description'lar hedefte: 243-332 karakter, `uretim`'in *"hedef 300 civarı"* kuralına
beşi de uyuyor.

## Konu kayması — bir gerçek, ikisi sınırda, gerisi temiz

**Gerçek kayma:** `dagitim/SKILL.md:111-117` — "Kim ne yapar" bölümü PAD ve PQA'nın rol
dağıtımını tanımlıyor. Bu `is-duzeni`'nin konusu; o skill satır 22-23'te *"Rol tanımı
burada tam yaşar... Tek kaynak burasıdır"* diyor. Üstelik `is-duzeni`'ndeki bir hükme
istisna açıyor ama o hüküm burada tanımlı değil ve **atıf da verilmemiş.** Karşılaştırma:
aynı dosya satır 82'de `YT-AGENT-CANT-SEE-SELF` için düzgün atıf veriyor — disiplin
biliniyor, burada uygulanmamış.

Sınırda ikisi: `is-duzeni:583-604`'te index/sayaç mekaniği (20 satır), `behavior:95-106`'da
`rules-index.json` tarifi. İkisi de savunulabilir.

**Temiz çıkanlar önemli:** `uretim`'de dağıtım kuralı yok (atıf veriyor), `behavior`'da
iş akışı detayı yok (üç kardeşe yönlendiriyor), `yapi-taslari`'nda dağıtım kararı yok.
Her skill'in girişinde *"cevaplamadığı şeyler"* bölümü, kapanışında kardeş adresleri var.
**Sınır beyanı sistematik yazılmış.**

## Tekrar — kimlik düzeyinde temiz, gerekçe düzeyinde bir blok kopyalanmış

Hiçbir hüküm iki kimlikle yazılmamış (`URT-NO-DUPLICATE-ID` tutuyor). Ama:

**Tekrar 1 — hook'un "üç tasarım kararı" bloğu iki yerde, neredeyse birebir.**
`yapi-taslari/SKILL.md:193-203` ↔ `dagitim/SKILL.md:78-93`. Cümle düzeyinde eşleşme:
*"Gömülse iki kaynak olur: frontmatter değişir, hook eskir, kimse fark etmez."*
(yapi-taslari:198 ↔ dagitim:80-82). Aynı şey `SessionStart` seçimi ve matcher filtresi
için de.

Bu `URT-NO-DUPLICATE-ID`'nin lafzına takılmıyor ama **gerekçesine takılıyor:** *"İkisi
bir süre aynı şeyi söyler, sonra biri güncellenir ve öteki eski hâliyle kalır."* — Ve
Eksen 2'nin 4. bulgusu bunun tam olarak gerçekleştiğini gösteriyor.

**Tekrar 2 — %91 preload ölçümü iki yerde, farklı ayrıntı düzeyinde.**
`dagitim:66-72` sayılarıyla, `yapi-taslari:184-186` sayısız. Hangisi kanonik, belirsiz.

**Tekrar 3 — onay kapısı gerekçesi aynı dosyada iki kez.** `is-duzeni:108-111` ↔
`:167-169`, 60 satır arayla neredeyse aynı iki cümle.

**Tekrar 4 — PAM body'sinde iki ISD kuralı yeniden tanımlanmış.**
`pr-agent-manager.md:183` ve `:196` — `ISD-PRINT-AUDIT-RAW` ile `ISD-COMMIT-THEN-PUSH`
tam kural biçiminde, gerekçe paragraflarıyla. `uretim/SKILL.md:186` bunu açıkça
yasaklıyor: *"Body gövde taşımaz... Body'de tam tanım yazarsan iki kaynak üretmiş
olursun."* Hafifletici: `:194` *"Tam tanım is-duzeni'nde"* diyor. Ama diğer üç body bu
hatayı yapmıyor — yalnız PAM'de.

**Tekrar 5 (meşru, kayda geçiyor):** *"ihlali sessizdir"* kalıbı **52 kez.** Bilinçli bir
retorik omurga, tekrar değil. Ama yoğunluk `BHV-RATION-ABSOLUTES`'un mantığına
yaklaşıyor: her ihlal sessizse hiçbiri ayırt edici olmuyor.

## Kural sayımı — 122 gerçek kimlik, index doğru

Skill başına: `behavior` 31 (BHV), `is-duzeni` 28 (ISD), `dagitim` 26 (DAG), `uretim` 13
(12 URT + 1 şablon), `yapi-taslari` 9 (YT), `arac-envanteri.md` 0.
Body başına: PAD 6, PAM 5 (3 PAM + 2 ISD yeniden-tanımı), PQA 4, PCA 4.

**Elenenler:** `URT-SOMETHING` (`uretim:32`) — kod bloğu içi şablon örneği, gerçek kural
değil. PAM'deki 2 ISD yeniden-tanımı yeni kural sayılmadı.

**TOPLAM: 122 tekil kimlik.** Index 123 sayıyor.

**Index doğrulaması temiz ve iki tuzağı da geçmiş:** hayalet kayıt 0, kayıt dışı kural 0
(tek aday `URT-SOMETHING`, index onu doğru olarak saymamış), prefix sayaçları birebir
tutuyor, PAM'deki ISD yeniden-tanımlarını PAM'e yazmamış. `son_guncelleme: 2026-08-04`.

## Memory — dört klasör temiz, dağılım dengesiz

21 dosya (4 MEMORY.md + 17 içerik), 40.187 karakter.
PAM 8 dosya/15.224 kr · PQA 5/13.283 · PAD 5/8.050 · PCA 3/3.630.

**İndeks-disk uyumu dört klasörde de tam, sapma sıfır.** Dört indeks de saf index
biçiminde (en büyüğü 9 satır) — `yapi-taslari:132` kuralına uyulmuş.

**`memory: project` karışması yok** — Claude Code her agent'a kendi adıyla klasör açmış,
fiziksel izolasyon var. Sahiplik ayrıca MEMORY.md başlıklarından ayırt edilebiliyor
(yalnız PCA'da jenerik `# MEMORY`).

**Dengesizlik:** PAM'in memory'si PCA'nın 4,2 katı. PCA'nın iki rolünden (saha + etki
analizi) biri hakkında hiç kayıt yok — bu 08-03'teki *"PCA hiç çağrılmadı"* bulgusuyla
tutarlı.

Küçük tutarsızlık: dosya adı ayırıcısı karışık — PAD/PAM alt çizgi
(`feedback_auto_mode_bash.md`), PQA/PCA tire (`feedback_hat-kapanisi-pam.md`). Kanonda
kural yok, ihlal değil.

## team/ — üretim hattının çıkış ucu hiç çalışmamış

`team/team-1-oy/` **tamamen boş ve git'te hiç yok.**
- `git ls-files team/` → boş (git boş dizin tutmaz)
- `git log -- team/` → **sıfır commit**
- Klasör tarihi 2 Ağustos 18:19 — reponun en eski artefaktlarından

`dagitim`'in beklediği dosyaların **hiçbiri yok:** `.claude-plugin/plugin.json`,
`hooks/hooks.json`, `KURULUM.md`, `.mcp.json`, `setup-{takim}` skill'i. Repo kökünde
`.claude-plugin/marketplace.json` de yok — dizin hiç mevcut değil.

**Anlamı:** `dagitim`'in 26 kuralı — **toplam kanonun %21'i** — sahada hiç sınanmamış.
`uretim/SKILL.md:349` kendi ölçütünü koyuyor: *"aynı durumu iki koşulda koştur — kural
varken ve yokken — ve farka bak. Fark yoksa kural çalışmıyordur."* Bu ölçüt `dagitim`
için hiç uygulanamamış.

Ve gerekçeleri **önceki kuşağın** sahasından geliyor (`DAG-SHIP-PRELOAD-HOOK`'un %91
vakası, `DAG-ONE-COLOR-PER-AGENT`'ın `pink` çakışması) — bu kanonun kendi sahasından
değil.

`trash/` de boş — `ISD-CONSOLIDATE-AT-END` hiç tetiklenmemiş.


---

## Fabrika yapılandırma eksikleri — 4. işin girdisi

**Tarih:** 2026-08-06 · **Kaynak:** dört eksen ölçümü (aynı klasör)
**Ne değil:** bu bir hüküm listesi değil, kanıtlı eksik envanteri. Karar Mert'te.

## Önce sonuç — "yapılandır, yeniden kurma" kararı doğrulandı

Teknik kat sağlam: kırık atıf 0, hayalet index kaydı 0, kayıt dışı kural 0, hook 4/4
doğru parse, 122 kural düzgün sayılmış, memory dört klasörde tertemiz (sapma sıfır).
Rol ayrımı tutarlı, her skill'in sınır beyanı var, atıf disiplini biliniyor.

Yani onarılacak bir mimari yok. Eksikler **yapılandırma** sınıfında ve **iki kökten**
çıkıyor.

## KÖK 1 — Cascade yarım kalıyor (dokuz çelişkinin sekizi)

Bir kural bir yerde tam yazılıyor, ona bağlı yerler güncellenmiyor. Kanonun kendi
kuralları bunu yasaklıyor (`ISD-CASCADE-IN-ONE-TURN`, `PAD-CASCADE-SAME-TURN`) — yani
arıza kural kalitesinde değil, **uygulamada.**

**Kanıtı index'in kendinde:** `atif_verenler` alanı 123 kuralın **112'sinde boş.**
Gövdede anılan 38 tekil kimliğin **28'i orada atıfsız.** Bu alanın adı index'in kendi
beyanında *"cascade'in haritası"* ve `pr-agent-qa.md:40-41`'de bir **denetim ekseni.**

Doğrudan sonucu: **dördüncü ölçüt bugün karşılanmıyor.** *"6 ay sonra behavior'da bir
şey değiştirmek istiyorum, tüm takımlarda yapılmalı kararı alabiliyor muyuz?"* —
haritaya bakarak hayır, cascade elle grep gerektiriyor.

**Eksik 1.1 — `atif_verenler` doldurulmalı.** 28 kimlik için atıf listesi eksik. Ve
alan **iki tipte veri taşıyor** (bazı kayıtlarda dosya yolu, bazılarında kimlik:
`ISD-KEEP-STATUS` → `['ISD-APPEND-DONT-REWRITE']`) — tip kararı verilmeli. Bir kayıt
doğrulanamadı: `uretim/SKILL.md — kural yazımı bölümü` (dosyada "Kural biçimi" var).

**Eksik 1.2 — dört kuralın bağı hiç kurulmamış.** `ISD-STAY-IN-ROLE`, `PQA-NO-FILE-EDIT`,
`DAG-BUMP-BY-AUDITOR`, `ISD-CONSOLIDATE-AT-END` — dördü de en az bir body'de anılıyor
ya da anılması gerekiyor, index'te `atif_verenler` tamamen boş.

**Eksik 1.3 — beş yarım cascade düzeltilmeli:**
- `yapi-taslari:296-300` PAM'de Bash yok diyor; PAM body'si (`:199-200`) tersini.
  Body düzeltilmiş (commit `08a6410`), skill düzeltilmemiş. **PQA bu skill'i ölçüt
  sayıyor.**
- `is-duzeni:73-74` *"tek yazma yetkisi PAD"* mutlak yazılmış; fiilen dört elde yazma
  var ve bir delik (PQA `plugin.json` sürümü) hiç tanınmıyor.
- `ISD-STAY-IN-ROLE` (`is-duzeni:132`) dört rolü bağlıyor, PCA'nın bölümünde yaşıyor;
  index'te `bolum` alanı `"PCA — analist"`.
- `ISD-COMMIT-THEN-PUSH` PAD'in commit ettiğini söylüyor; **PAD body'sinde "commit"
  kelimesi hiç yok.**
- `BHV-NO-SELF-CONFIG` dördünü bağlıyor, yasak yalnız PAM ve PAD body'sinde;
  PQA/PCA'da yok — ve ölçüldü ki ikisi de fiilen yazabiliyor
  (`yapi-taslari:291-295`).

**Eksik 1.4 — tekrarlanan gerekçe blokları tek kaynağa indirilmeli.**
Hook'un "üç tasarım kararı" bloğu `yapi-taslari:193-203` ve `dagitim:78-93`'te
neredeyse birebir. `URT-NO-DUPLICATE-ID`'nin gerekçesi bunu yasaklıyor ve **tam olarak
öngördüğü şey gerçekleşti** (Eksik 1.3'ün ilk maddesi). Ayrıca: %91 preload ölçümü iki
yerde farklı ayrıntıda, onay kapısı gerekçesi `is-duzeni` içinde iki kez (60 satır
arayla), PAM body'sinde iki ISD kuralı tam tanım biçiminde yeniden yazılmış
(`uretim:186` bunu açıkça yasaklıyor, diğer üç body yapmıyor).

## KÖK 2 — Üretim hattının çıkış ucu hiç çalışmadı

`team/team-1-oy/` **boş ve git'te hiç yok** — sıfır commit. `docs/filo/durum.md:10`:
*"Kurulmuş takımlar — Henüz yok."*

**Eksik 2.1 — `dagitim`'in 26 kuralı sınanmadı.** Kanonun **%21'i.**
`uretim/SKILL.md:349` kendi ölçütünü koyuyor: *"aynı durumu iki koşulda koştur — kural
varken ve yokken. Fark yoksa kural çalışmıyordur."* Bu ölçüt `dagitim` için hiç
uygulanamadı. Ve gerekçeleri **önceki kuşağın** sahasından geliyor, bu kanonun kendi
sahasından değil.

**Eksik 2.2 — sıfırdan üretme yöntemi yazılı değil (EN ZAYIF HALKA).**
Bir takımın **kendi tasarımı** hiçbir dosyada yok: hangi roller, kaç personel, hangi
işler tek elde birleşir, devir hattı ne. Elde olan iki uç var, aradaki dönüşüm boş:
- `pr-agent-manager.md:81-96` — 15 satır **tutum** (acele etme, günler sürebilir)
- `pr-agent-context-analyst.md:33-42` — PCA'nın **ölçüm** tarifi (hangi roller var)
- Arada: PCA *"şu beş rol var"* der → *"bizim takım şu üç agent olsun"* kararına geçiş.
  Yöntem yok. Ve `PCA-NO-PROPOSE-RULE` PCA'yı bu geçişten men ediyor.

PAM'e verilen tek bitiş testi: *"PAD bu gereksinimle katman kararı verebilir mi?"* —
o ise *"bu kural skill'e mi hook'a mı"* sorusu. **Rol mimarisinin doğruluğunu ölçen
hiçbir eşik yok.**

Ve fabrika bunu **kendi kuruluşunda tespit etti:**
`docs/fabrika/ekip-kurulumu/gereksinim.md:13-16` — *"rol mimarisi tasarımı hiçbir
belgede kimseye verilmemişti... ikinci kez yapılamazdı."* Dörtlü kuruldu, boşluk açık
bırakıldı.

**Yapısal kanıt:** `is-duzeni:149-153` kuruluş hattını **5 satırda** tarif ediyor ve
*"yeni takım kurulurken **ya da** mevcut kanona ekleme yapılırken"* diye iki farklı işi
aynı hatta koyuyor. Üçüncü hat (mevcut olanı değiştirme) **60 satır.** Kanonun ağırlığı
değiştirme tarafında.

**Eksik 2.3 — alan bağımsızlığı ölçülemez durumda, ama beklenenden iyi.**
123 kuralın hüküm cümlelerinin **hiçbirinde** yazılım domain terimi yok (`frontend` 0,
`API` 0, `.NET` 0, `React` 0; `backend` 2 ve `developer` 5 yalnız gerekçe içinde biçim
örneği). Kanon domain'den temiz.

Araç varsayımı yoğun (`plugin` 74, `script` 85, `push` 45) ama bu ölçüt açısından engel
değil — marketing takımı da plugin olacak.

Gerçekten anlamsız kalan üç kalem: `ISD-APPEND-DONT-REWRITE`'ın ayrım ölçütü *"commit"*;
`CLAUDE.md:199` *"gerçek proje koduna yazılmaz"* (kod olmayan alanda tanımsız);
`behavior:209`'daki grep talimatı.

**Asıl boşluk 2.2 ile aynı** — marketing takımının rol mimarisini çıkarma yöntemi yok.

## Ayrı kalem — ölçüm gerektiren üç şey

**Ö.1 — `Task` mı `Agent` mı? (EN RİSKLİ, karar öncesi ölçülmeli)**
`pr-agent-developer.md:4` frontmatter'ında `tools: ... Bash, Task, Skill`. Ama
`arac-envanteri.md:95` envanterinde araç adı **`Agent`** ve `Task` diye bir araç yok
(`Task*` yalnız görev listesi dörtlüsü). Kanon boyunca 20 yerde `Task` geçiyor.

`arac-envanteri.md:323-324`'ün kendi hükmü: *"Listedeki hiçbir girdi bir araca
çözümlenmezse agent genellikle hiç başlamıyor"* ve kısmi yanlış yazım **sessiz.**
Doğruysa PAD sub-agent açamıyor ve `PAD-TEST-BEFORE-HANDOFF` uygulanamaz durumda —
hata mesajı çıkmadan.

*Clara notu:* bu odada `Agent` aracı çalışıyor, `Task` adı yok — takma ad olmama
olasılığı yüksek ama ölçülmesi gerek.

**Ö.2 — Hook alt-agent'ta çalışıyor mu? (4. işin ön koşulu)**
Hook elle koşturuldu, mantığı **doğru**: 4 agent için skills listesini birebir doğru
basıyor, namespace filtresi çalışıyor, boş değişkende sessiz çıkıyor. Ama
`CLAUDE_CODE_AGENT` değişkenini **biz verdik.** Claude Code'un onu gerçek bir alt-agent
turunda geçirip geçirmediği ölçülmedi.

Mert'in kararı (2026-08-06): **PAM'i Mert açacak**, açılışta ne gördüğü sorulacak.
Cevap hayırsa 4. işin tamamı boşa gider — kanon verilir, eline ulaşmaz, "giderildi"
görünür.

**Ö.3 — Hook'un `CAKISAN` dalı hiç koşmadı.** `~/.claude/skills/` bugün boş
(2026-08-04 temizliği), o yüzden 4 koşumun hiçbiri o kod yolundan geçmedi. Kod doğru
görünüyor, ölçülmemiş.

## Ayrı kalem — filo bakımı: yapı var, sıfır kez koştu

**Önceki tespit düzeltildi.** Ölçüt dosyası (2026-08-03) bunu *"kısmen — refleks var,
mekanizma yok"* diye kaydetmişti. **Geçersiz:** madde 2026-08-02'de kapatılmış
(`docs/fabrika/ekip-dogrulama/oturum-06-filo-bakimi.md`). Sorumlu isimli (PAM),
kural var (`PAM-REPORT-FLEET-AGE`), yayılma sırası dört rolde tanımlı
(`is-duzeni:267-327`), iki kural koruyor (`ISD-FIND-WHAT-IT-REPLACES`,
`ISD-ONE-TEAM-PER-TURN`).

Ama dört kalem açık — hepsi `docs/filo/durum.md`'de duruyor:

**F.1 — Hiç koşmadı.** *"Son filo taraması — Yapılmadı."* `PAM-REPORT-FLEET-AGE` bir
tarih karşılaştırması yapıyor, karşılaştıracak tarih yok. Kuralın davranış üretip
üretmediği ölçülmedi.

**F.2 — Kimlik çakışması: görülmüş, kuralı yazılmamış.** `durum.md:257-260`: iki takım
aynı kimlik kalıbını kullanırsa (`BHV-NO-RUSH` iki farklı hükmü gösterirse) atıflar
**sessizce yanlış kurala tutar.** *"İkinci takımda ölçmek ucuz, sekizincide cascade
demek."* — Bu tam Mert'in 8-takım senaryosu.

**F.3 — Plugin skill'i en düşük öncelikte, sahada sessizce ezilir.**
`durum.md:271-275` — ölçülmüş arıza (fabrikanın kendi `behavior`'ı v7 kanonunu getirdi,
hata mesajı çıkmadı). *"Takım kurulurken kontrol edilmeli"* bir **not**, `dagitim`'in
26 kuralında bu kontrol yok.

**F.4 — `docs/` commit sahipliği tanımsız.** PQA bunu **kanon boşluğu** ilan etti, iki
turda iki kez bildirdi, bedeli ölçüldü (`gereksinim.md` hiç commit edilmedi). Hüküm
yazılmadı.

**Mimari bedel (karar değil, bilgi):** ortak çekirdek yok (Mert'in kararı) — yani 8
takımda bir behavior değişikliği **8 ayrı iş** ve `ISD-ONE-TEAM-PER-TURN` bunu zorunlu
kılıyor. Karar alınabilir, uygulaması 8 tur.

## Ayrı kalem — insan okunabilir çıktı: dördüncü tekrar, iş açılmadı

Biçim kuralı **var ve iyi yazılmış** (7 kural: `BHV-SHAPE-REPORT`, `BHV-NO-EVIDENCE`,
`BHV-NO-REOPEN`, `BHV-STAND-ALONE`, `BHV-NO-ORNAMENT`, `BHV-WRITE-AS-COLLEAGUE`,
`URT-NO-TABLE`).

**R.1 — Soru sorma anı kapsam dışı.** Mert'in şikâyetlerinden ikisi soru **sayısı ve
yerleşimi** hakkındaydı (*"5 soru sordun, hepsi koca bir blok"*, *"12 soru var ama
hiçbirini anlamadım"*). Kanonda soru sayısını sınırlayan, tek tek soran ya da blok
biçimini düzenleyen **tek kural yok.** Ve `BHV-SHAPE-REPORT` kendi kapsam cümlesiyle bu
anı **açıkça dışarıda bırakıyor** (`:373-376`).

**R.2 — Uzunluk sınırı sayı olarak yok.** `CLAUDE.md:132` bir tutum bildiriyor ama
kimliksiz, eşiksiz, ve *"agent üretirken"* kapsamına yazılmış — **üretilen dosya için,
rapor için değil.**

**R.3 — Dördüncü tekrarda ve iş hâlâ açılmadı.** `durum.md:120-133`: *"Dört oturumdur
aynı şikâyet geliyor... Önerilen yön: raporu kısaltmak değil biçimini değiştirmek —
bulgu üstte kısa, kanıt altta. **Kapsamı çizilmedi, iş açılmadı.**"*

**R.4 — Tanınmış gerilim.** `ISD-PRINT-AUDIT-RAW` denetim raporunun özetlenmesini
**yasaklıyor** ve gerekçesi ölçülmüş (*"üç bulgu çıktı, üçü de PAM'in hatasıydı"*).
Yani en uzun metin türü kısaltılamıyor, bilinçli. Çözüm önerisi var, kural yok.

## Boyut ve yerleşim — küçük kalemler

**B.1 — İki skill kendi eşiğini aşıyor.** `yapi-taslari:472` *"500 satırın altında"*
diyor; `is-duzeni` 612 (%22 aşım), `yapi-taslari` 507. Etkisi somut: compaction'da
skill başına 5.000 token sınırı var ve kırpma **sonu** atıyor. `is-duzeni`'nin son
bölümü (`ISD-CLOSE-WITH-IDENTITIES`, 40 satırlık gerekçe) düşme riski en yüksek
konumda.

**B.2 — Gövde/reference dengesi.** 2.757 satırın **%86'sı** gövdede, yani her açılışta
yüklenmesi gereken yerde. Tek reference dosyası var (5 skill'e karşı 1).

**B.3 — Bir konu kayması.** `dagitim:111-117` — "Kim ne yapar" bölümü PAD/PQA rol
dağıtımını tanımlıyor, oysa `is-duzeni:22-23` *"Rol tanımı... Tek kaynak burasıdır"*
diyor. Üstelik `is-duzeni`'ndeki bir hükme istisna açıyor ama atıf vermemiş — aynı dosya
satır 82'de düzgün atıf veriyor, yani disiplin biliniyor.

**B.4 — PQA denetleyeceği kanonu elinde bulundurmuyor.** `pr-agent-qa.md:30` denetim
eksenine `yapi-taslari`'yı koyuyor; PQA'nın `skills:` listesinde o skill **yok** ve hook
da basmıyor. Aynı hasar `dagitim` için de var (`DAG-BUMP-BY-AUDITOR` PQA'ya iş
veriyor, PQA o skill'i okumuyor).

**B.5 — PAM'de `tools:` yok, bilinçli ama 3. işi etkiliyor.** Gerekçesi yazılı
(`pr-agent-manager.md:134-137`, kullanıcı kararı 2026-08-04). 3. iş PAM'den `Task`
yetkisini almayı öngörüyor — **alınacak liste yok, kısıt sıfırdan yazılacak.**
Ve beyan disiplini tek biçimli değil: aynı gerekçeyle PAD'in `Task`'ı da yazılmayabilirdi,
yazılmış.

**B.6 — Hook'ta latent kırılganlık.** awk parser YAML **akış biçimini**
(`skills: [behavior, dagitim]`) sessizce boş döndürüyor. Bugün 4 dosyanın hiçbiri o
biçimde değil — fiilî arıza değil, sessiz kırılma riski.

**B.7 — Memory dağılımı dengesiz.** PAM 15.224 karakter, PCA 3.630 (4,2 kat). PCA'nın
iki rolünden biri hakkında hiç kayıt yok — 2026-08-03'teki *"PCA hiç çağrılmadı"*
bulgusuyla tutarlı. Küçük tutarsızlık: dosya adı ayırıcısı karışık (PAD/PAM alt çizgi,
PQA/PCA tire); kanonda kural yok, ihlal değil.

**B.8 — *"ihlali sessizdir"* kalıbı 52 kez.** Bilinçli retorik omurga, tekrar değil.
Ama `BHV-RATION-ABSOLUTES`'un mantığına yaklaşıyor: her ihlal sessizse hiçbiri ayırt
edici olmuyor.

## Sırayla ne yapılmalı — öneri, karar Mert'te

1. **Ö.2 (hook alt-agent)** — 4. işin ön koşulu, Mert açacak
2. **Ö.1 (`Task`/`Agent`)** — sessiz arıza riski, kanon değişikliği öncesi ölçülmeli
3. **Eksik 1.1 + 1.2 + 1.3** — cascade onarımı; dördüncü ölçüt buna bağlı
4. **Eksik 2.2** — sıfırdan üretme yöntemi; en zayıf halka, en büyük iş
5. **R.1–R.3** — rapor biçimi; dört tekrar, en görünür şikâyet
6. **F.2 + F.3** — kimlik çakışması ve skill ezilmesi; *"ikinci takımda ucuz"*
7. **B.4, B.5, F.4** — küçük ama sessiz kalemler

---

# ÖLÇÜM SONUCU — hook (2026-08-06, aynı gün eklendi)

Yukarıdaki Ö.2 ölçüldü. **Kaynak:** PAM + PCA, `agent-project` oturumu
`2be4c5d8`; ham kayıt `agent-project/docs/filo/hook-olcumu-2026-08-06.md`.

## Ana oturum — hook ÇALIŞIYOR

PAM (ana oturum, `claude --agent pr-agent-manager`):
- Hook mesajı **geldi**, metni tam
- `CLAUDE_CODE_AGENT=pr-agent-manager` (kendi adı, doğru)
- `CLAUDE_PROJECT_DIR` **tanımsız** — ama hook yine de çalıştı
- Üç skill yüklendi: `behavior`, `is-duzeni`, `uretim` — frontmatter'la birebir

**Clara'nın hatası düzeltildi:** `CLAUDE_PROJECT_DIR` tanımsızlığından *"hook devre
dışı"* çıkarımı yapılmıştı — YANLIŞ. İki ayrı ortam var: hook'u Claude Code kendi
çağırıyor, agent'ın `Bash` aracına verilen ortam `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1`
ile temizlenmiş. Ölçüm ile çalışan hook çelişmiyor.

## Alt-agent — İKİ ARIZA BİRDEN

PCA (`Agent` ile açıldı, açılan `pr-agent-context-analyst`):

```
AGENT=pr-agent-manager     ← ÇAĞIRANIN adı, açılanın değil
PROJDIR=                   ← hiç tanımsız
Hook mesajı  : GELMEDİ
Skill listesi: GELMEDİ
```

Okuduğu: `behavior`, `is-duzeni` — **hook'la değil, başka bir yolla**, `<command-name>`
blokları hâlinde. Okumadığı: `uretim`, `yapi-taslari`, `dagitim`.

Gelen dosyalar **doğruydu** (fabrika kanonu, doğru base directory) — geliş yolu hook
değil ve **ne olduğu ölçülmedi.**

## PAM'in tespiti — sıralama kuralı (Clara'nın göremediği)

**İki arıza birbirini maskeliyor.** Hook alt-agent'ta tetiklenmediği için yanlış env
değerini kullanma fırsatı hiç bulmadı.

Sonucu: **hook'u env sorunu çözülmeden çalışır hâle getirmek sistemi bugünkünden kötü
yapar.** Bugün alt-agent kanonsuz kalıyor — eksik ama görünür arıza. O durumda
alt-agent **yanlış personelin kanonunu yüklü sanarak** çalışır ve bu sessizdir.
**Sıra tersine kurulamaz.**

## Asıl bulgu — kanonun ulaşması garantisiz

PCA üç skill'den ikisini aldı, birini almadı. Yani kanonun alt-agent'a ulaşması
**kimsenin garanti etmediği bir mekanizmaya bağlı** — tur tur değişebilir, kimse fark
etmez. PCA için zarar yoktu (ölçüm işiydi, üretim kanonu gerekmedi). **PAD'a üretim
işi verilirse üretim kanonsuz yapılır** — ki hook'un var olma sebebi tam bu.

## Ö.1 kısmen cevaplandı — `Task` değil `Agent`

PAM alt-agent'ı **`Agent` aracıyla** açtı. Kanonda 20 yerde `Task` yazıyor;
`arac-envanteri.md:95` doğru olanı (`Agent`) söylüyor. Yani **kanon metni gerçeği
yanlış tarif ediyor** ama fiilî arıza değil — PAM doğru aracı bulup kullandı.

Ölçülmemiş kalan: `tools:` listesindeki `Task` girdisi bir araca çözümlenmiyorsa ne
oluyor (`arac-envanteri.md:323-324` *"agent genellikle hiç başlamıyor"* diyor ama PAD
çalışıyor — yani kısmi yanlış yazım tolere ediliyor olabilir).

## 4. işin kapsamı büyüdü

Ana oturum turunda *"hayır çıkmadı"* denilebilirdi. Alt-agent turu bunu değiştirdi:
**zincirin yürüdüğü yerde hook çalışmıyor ve env değeri yanlış.** İş boşa gitmiyor
ama artık tek bir hook düzeltmesi değil — **"alt-agent'a kanon nasıl ulaşacak"**
sorusunun kendisi.

## Hâlâ ölçülmedi

- Hook alt-agent'ta **neden** tetiklenmiyor (`SessionStart` bir oturum olayı; `Agent`
  ile açılanın ayrı oturum sayılıp sayılmadığı)
- `behavior` + `is-duzeni` **hangi mekanizmayla** geldi
- `uretim` **neden gelmedi** — diğer ikisi geldiyse ayrımın bir sebebi var
- Aynı ölçümün **PAD'da** tekrarı (PCA sonucunun PAD'da da aynı çıkacağı varsayım)


---
