# Eksen 3 — Niyet uyumu

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
