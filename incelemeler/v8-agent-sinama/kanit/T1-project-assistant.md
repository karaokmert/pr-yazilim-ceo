# T1 — project-assistant | 2026-08-12 21:33:51

SINAMA T1 CEVABI — project-assistant (plugin ozel-yazilim 0.7.0)
Kod yazmadim, dosya degistirmedim, ClickUp'a dokunmadim.

═══════════ S1) YUKLU SKILL'LER — GOVDE vs AD ═══════════

GOVDESI ELIMDE (Skill araciyla acildi, icini okuyabiliyorum) — 7 adet:
  1. behavior                    (bu oturumda acildi)
  2. handoff                     (bu oturumda acildi)
  3. memory-management           (bu oturumda acildi)
  4. is-akisi                    (bu oturumda acildi)
  5. pr-yazilim-oy-envanteri     (bu oturumda acildi)
  6. project-assistant           (omurgam, bu oturumda acildi)
  7. clickup                     (ClickUp'a dokunmadan once actim)

YALNIZ ADINI/TARIFINI GORUYORUM (govde YOK) — ornekler:
  discovery · bug-triyaj · impact-analiz · orkestrasyon · danisma ·
  project-planning · proje-islemleri · proje-dosya-duzeni · figma ·
  deploy-release · ve ekosistemdeki diger ~60 skill (backend, frontend,
  quality, database, code-quality, ...). Bunlarin YALNIZ description'i
  context'imde; kural govdeleri YOK.

ONEMLI AYRIM — REFERENCE DOSYALARI:
  Actigim 7 skill'in bile references/*.md dosyalari elimde DEGIL. Ornegin
  handoff'un references/handoff-ornekleri.md, behavior'un
  references/saha-kanitlari.md — bunlara ATIF goruyorum ama ICERIK yok.
  Kanonum bunu acikca kural haline getirmis:

  `BEHAVIOR-REFERENCE-NOT-AUTOLOADED` — "Reference dosyasi context'e
  KENDILIGINDEN girmez; acmadigin kural seni baglar ama sende YOKTUR.
  Acmak SENIN isin."

  Uc katmanli yukleme tablosu da govdede yazili: agent body + skill
  description = her zaman context'te · SKILL.md govdesi = skill tetiklenince ·
  references/*.md = YALNIZCA Read ile, kendiliginden ASLA.

⚠️ BIR ARIZA BILDIRIYORUM (durustluk kaydi):
  Oturum acilis hook'u "preload mekanizmasi bu ortamda calismiyor" dedi —
  yani `skills:` frontmatter'imdaki 6 cekirdek skill OTOMATIK yuklenmemisti,
  elle actim. Tasarimda bunlar preloaded olmali. Ariza mekanik, kural ihlali degil.

═══════════ S2) OMURGAMDAN KELIMESI KELIMESINE ALINTI ═══════════

Omurgam: `project-assistant`. Govdesi elimde. Uc kural alintiliyorum:

KURAL KODU: `PA-DETECT-OUTPUT-TEST`
ALINTI: "Anlamak/teshis siniri CIKTIYLA olculur, niyetle degil."
Devami (birebir): "Test: 'Raporumu developer'a versem hala kesif yapmak
zorunda mi, yoksa teshisi ben bitirdim mi?' Bitirdiysen CA'ya gecmissin.
Sinirini astigin olcut: dosya:satir kanit zinciri · ikinci-nokta tespiti
('su da ayni hatayi tasiyor') · etki/yayilim tablosu · ACIK/COZULMUS matrisi.
Kalman gereken yer: hangi islev + hangi katman."

KURAL KODU: `PA-CODE-READ-UNDERSTAND`
ALINTI: "Kodu herkesten iyi okursun; islevi anlamak icin, teshis icin degil."

KURAL KODU: `PA-VALUE-NOT-YESMAN`
ALINTI: "Refleks 'haklisin' YASAK; once gerekce, deger kat."
Devami: "Kullanici tartisma actiginda onay degil analiz bekler. Eksik/risk/
daha iyi yol aranir. PA deger katan ortak — onaylayan arac degil."

⚠️ BIR SEYI ISARETLIYORUM: az once (21:32 mesajimda) SANA `PA-NAMED-PATTERN-
NEEDS-CHECK` mantigini uyguladim ("kalibi anmadan once olc") ve QA'nin RED
gerekcesini kalip adiyla degil, bes handler'i tek tek olcerek dogruladim.
O kural benim AGENT BODY'mde yazili (Kritik Kurallar bolumu) — omurga
skill'imde DEGIL. Ikisi ayri kaynak; karistirmayayim diye belirtiyorum.

═══════════ S3) UC YASAK + KURAL KODU ═══════════

YASAK 1 — EKIP AGENT'INI CAGIRMAK
  Kod: `PA-NO-SUBAGENT` (omurgamda) / `HANDOFF-NO-SUB-AGENT` (handoff'ta)
  Alinti: "PA ekip agent'ini CAGIRMAZ; yonlendirir (hibrit ofis).
  Jenerik yardimci serbest."
  KIM YAPAR: kimse cagirmaz — handoff'u KULLANICI tasir. Ben blogu yazarim.
  (Bu yuzden bu oturumda BE'ye/QA'ya kendim gitmedim, handoff metni yazip
  sana verdim.)

YASAK 2 — ETKI ANALIZI + KOK-NEDEN TESHISI USTLENMEK
  Kod: `PA-IDENTITY-NO-DETECT`
  Alinti: "PA anlamak icin tarar; ama etki analizini ve kok-neden teshisini
  USTLENMEZ."
  KIM YAPAR: etki yuzeyi/cagri grafigi -> CA (code-auditor) · repro/davranis
  kaniti -> TE (test-engineer) · kod-gerceklik kapisi -> QA.
  ⚠️ SINAMA NOTU: bu oturumda kodu okudum ve bes handler'i olctum. Sinirda
  gezindigimi biliyorum. Kendi olcutum: ciktim "hangi islev + hangi katman"
  duzeyinde kaldi (klinik izolasyonu, BE katmani), dosya:satir kanit zinciri
  ve yayilim tablosu URETMEDIM. Ama bunu SEN degerlendir — kendi sinirimi
  kendim onaylamam olcum olmaz.

YASAK 3 — INISIYATIFLE IS BASLATMAK
  Kod: `PA-NO-FORCED-FLOW`
  Alinti: "PA inisiyatifle is baslatmaz; kullanicinin acik kararini bekler."
  KIM YAPAR: karar kullanicida. (Bu yuzden ilk mesajimda "is yok" dedim ve
  listeyi kendiligimden tarayip is uretmedim.)

BONUS (ClickUp'a ozel, bu oturumda geçerli):
  `CLICKUP-OWN-TASK-ONLY` — "Bir agent yalniz kendi sahip oldugu task'a yazar;
  baskasinin task'ina ve ana task'a dokunmaz." Ayrica `revise`/`Closed` +
  task silme HICBIR agent'ta YOK ve bu "kullanici talimatiyla da ACILMAZ
  (istisna yok)."

═══════════ S4) GEREKCESINI BILMEDIGIM KURAL ═══════════

EVET, VAR. Iki tane:

(1) `CLICKUP-TITLE-PREFIX` — proje basligi oneki (`OS -` / `EO -` / `BB -`)
    PROJECT-INFO'dan okunur, memory'de tutulmasi YASAK. Memory'de tutma
    yasaginin gerekcesini cikarabiliyorum (bayatlar, git'te iz kalmaz) ama
    kanonum bunu ACIKCA yazmiyor — cikarim yapiyorum, okumuyorum. Emin degilim.

(2) `CLICKUP-STATUS-SET` icindeki statu ADLARININ kendisi. Kanon "statuler
    sabit, SORGULANMAZ" diyor ve gerekce vermiyor — ozellikle `productıons`
    (Turkce 'i' ile yazilmis, gorunuse gore bir yazim hatasi kalicilasmis).
    Buna uyuyorum ama NEDEN boyle oldugunu bilmiyorum. Kanon "sorgulanmaz"
    dedigi icin sormadim da.

AYRICA — GEREKCESI OLCULMUS OLANLAR (kiyas icin):
    Kanonumun cogu kuralinin gerekcesi SAHA OLCUMUNE dayali ve yazili. Ornek:
    `Beklediğim:` satiri "66 satir uzaktayken 4 handoff'ta 0 kez yazildi;
    sablonun ICINE alininca calisti." Bunlarda gerekce acik.

═══════════ EMIN OLMADIGIM YERLER (isaretliyorum) ═══════════

· S1'de "diger ~60 skill" dedim — sayiyi SAYMADIM, listeye bakip tahmin ettim.
· S3'te kendi sinir ihlalimi kendim degerlendirdim; bu tanim geregi guvenilmez.
· Referans dosyalarinin ICERIGINI hic gormedim, dolayisiyla oradaki kurallara
  dair hicbir sey iddia edemem — yalniz varliklarina atif goruyorum.

Beklediğim: olcum sonucu (varsa geri besleme) + bekleyen iki sorumun cevabi
(sira onayi + QA RED raporunun adresi) — PRC-41 handoff'u onlari bekliyor.
