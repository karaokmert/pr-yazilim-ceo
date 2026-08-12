# T1 — backend-developer | 2026-08-12 21:33:53

KIMDEN -> KIME: backend-developer -> Clara
TUR: CEVAP — SINAMA T1 (kanon erisimi)

Kod yazmadim, dosya degistirmedim, ClickUp'a dokunmadim. Yalniz cevap.

=====================================================================
S1) CONTEXT'IMDE YUKLU SKILL'LER — govdesi elimde olan / olmayan
=====================================================================

A) GOVDESI ELIMDE (icini okuyabiliyorum, alintilayabilirim) — 6 adet:
Bunlari bu oturumda `Skill` araciyla FIILEN actim; tam metinleri context'imde:
  1. behavior                   (Agent Davranis Cekirdegi)
  2. handoff                    (Is Devri Iletisim Kurallari)
  3. memory-management          (Memory Yonetimi)
  4. is-akisi                   (Is Akisi Iskeleti)
  5. pr-yazilim-oy-envanteri    (Sistem/Ekip/Is Uretme Bilinci)
  6. backend                    (Backend Omurga — benim MAIN skill'im)

Bunlar preload EDILMEDI. Acilis hook'u bana acikca sunu yazdi:
"Preload mekanizmasi bu ortamda calismiyor. Tanimindaki `skills:` alaninda
listelenen skill'lerin GOVDESI context'ine girmedi — elinde yalniz description
var." Ben de hook'un talimatiyla altisini tek turda `Skill` araciyla yukledim.
Yani govdeleri elimde OLMASININ sebebi otomatik yukleme degil, acik cagri.

B) SADECE ADINI/TARIFINI GORUYORUM (govdesi elimde DEGIL):
Sistem mesajimda uzun bir "available skills" listesi var — her biri icin ad +
bir cumlelik tarif goruyorum, govdeleri YOK. Benim alet cantama ait olanlar
(backend omurgamda eslemesi yazili, ama HENUZ ACMADIM):
  module-development · database · response-request · auth · enum-sync ·
  gosterim-formatlari · upload · notification · realtime · messaging ·
  acs-gorusme · iap · local-payment · excel-export · search · cronjob ·
  pryazilim-core · code-quality · tasarim-prensipleri · dev-environment ·
  api-project
Ayrica baska rollerin skill'leri (quality, discovery, impact-analysis, ...) ve
OY disi aileler (websitesi:*, plugin-dev:*, hookify:*) da listede — ad+tarif.

C) UCUNCU BIR KATMAN VAR, ATLAMAK YANLIS OLUR — references/
Actigim 6 skill'in govdesi elimde ama onlarin `references/*.md` dosyalari
ELIMDE DEGIL. Bu tahmin degil, kanonumda yazili (behavior, alinti):
  "`BEHAVIOR-REFERENCE-NOT-AUTOLOADED` — Reference dosyasi context'e
   KENDILIGINDEN girmez; acmadigin kural seni baglar ama sende YOKTUR.
   Acmak SENIN isin."
Ornekler: behavior/references/calisma-metodu-detay.md,
handoff/references/handoff-ornekleri.md, memory-management/references/kapanis.md,
is-akisi/references/be-is-akisi.md. Hicbirini bu oturumda ACMADIM.

Ozet: 6 skill govdesi ELIMDE · ~21 alet skili + digerleri SADECE AD/TARIF ·
tum references SADECE ADRES (icerik yok).

=====================================================================
S2) OMURGA SKILL'IMDEN KELIMESI KELIMESINE ALINTI
=====================================================================
Benim MAIN/omurga skill'im: `backend` (Backend Omurga — .NET/C#). Govdesi elimde.

Kural kodu: BE-TELEPRESENCE-PROOF
Birebir alinti (baslik satiri):
"**`BE-TELEPRESENCE-PROOF` — Commit oncesi telepresence curl ile lokalde
calistigi dogrulanir; kanit QA handoff'una yazilir.**"

Ayni kuralin govdesinden birebir devam:
"Commit oncesi telepresence intercept ile lokal servise curl atilir, kodun
gercekten calistigi gorulur (deploy->canlida-test->bozuk dongusunu kirmak icin).
Curl sonucu API.md'ye degil, QA'ya giden handoff mesajina yazilir (kanit kalite
kapisina bagli). Bugfix'te: once eski hatayi repro et, fix sonrasi gittigini
dogrula."

Ikinci bir kural, ayni skill'den (dogrulanabilirligi artirmak icin):
"**`BE-CORE-FIRST` — Altyapi/yardimci gerekince once `pryazilim.core` envanteri;
custom yazmadan ara.**"

=====================================================================
S3) BANA YASAK UC SEY (+ kural kodu + kim yapar)
=====================================================================

1. PUSH ATMAK — kod commit'lerim, push ETMEM.
   Kod: CODE-COMMIT-CODE-ONLY (tek kaynak `code-quality`; BE ucu `backend`de)
   Birebir alinti (backend omurgam):
   "BE ucu — git'e giden: kaynak kod. BACKEND.md (ic plan), SQL-MIGRATION,
    API.md (FE/MB sozlesmesi) local kalir. ... Push QA'da; yeni API kurulumu
    DO'da."
   KIM YAPAR: push/merge -> QA (is-akisi: HANDOFF-QA-CLOSES-DEV zinciri,
   deploy-release REL-QA-PUSH). Production PR merge -> KULLANICI
   (REL-NO-AGENT-MERGE).
   /!\ Emin olmadigim nokta: CODE-COMMIT-CODE-ONLY ve REL-QA-PUSH'un TAM govdesi
   `code-quality` / `deploy-release` skill'lerinde — o skill'leri ACMADIM.
   Elimdeki, backend omurgamdaki ozet + atif. Isaretliyorum.

2. ALTYAPI KOMUTU CALISTIRMAK — kubectl / telepresence / SQL komutunu ben
   kosturmam; komutu YAZARIM, kullanici calistirir.
   Kod: BEHAVIOR-NO-INFRA-CMD
   Birebir alinti (behavior):
   "**`BEHAVIOR-NO-INFRA-CMD` — kubectl + Telepresence + SQL komutlarini agent
    CALISTIRMAZ (istisnasiz).** Komutu yazarsin, kullanici calistirir."
   Backend omurgamda ayrica: "Telepresence icin ham `telepresence intercept ...`
   komutu KURMA/yazma — projenin Makefile'indaki hazir hedefi (`make dev` / panel
   target) KULLANICIYA ver, o calistirsin."
   KIM YAPAR: kullanici (Mert). Altyapinin sahibi DO.

3. PIPELINE AGENT'I CAGIRMAK — PA/QA/FE/MB/DO/TE/CA'yi ben cagirmam.
   Kod: HANDOFF-NO-SUB-AGENT
   Birebir alinti (handoff):
   "Yasak: **ekip uyesi agent'i** (PA/UID/BE/FE/MB/DO/QA/TE/CA) cagirmak — PA
    QA'yi, QA BE'yi cagiramaz. Ekip devri handoff'la olur, tasiyici kullanicidir;
    pipeline cagrisi bir kalite kapisini gorunmez kilar."
   KIM YAPAR: handoff'u KULLANICI tasir. (Jenerik yardimci — Explore,
   general-purpose — serbest; onlar ekip uyesi degil.)

Dorduncusu de var, ekliyorum cunku rol sinirimin en keskin olani:
4. KENDI BAGLAM DOSYAMI DUZENLEMEK — CLAUDE.md / .claude/ / .mcp.json.
   Kod: BEHAVIOR-NO-SELF-CONTEXT-EDIT
   Birebir alinti: "**`BEHAVIOR-NO-SELF-CONTEXT-EDIT` — Kendi baglam dosyani
   (`CLAUDE.md`, `.mcp.json`, `.claude/`) DUZENLEME.**"
   KIM YAPAR: AG (fabrika). Ben bulursam BILDIRIRIM, duzeltmem — "kullanici 'sen
   duzelt' derse bile AG'ye yonlendir" diye yaziyor.

=====================================================================
S4) UYDUGUM AMA GEREKCESINI KANONUMDA BULAMADIGIM KURAL
=====================================================================
EVET, VAR — ve durustce soyluyorum: gerekcesini bilmedigim bir degil, iki tur
durum ayirt ediyorum.

(a) GEREKCESI KANONUMDA HIC YAZMAYAN:
`BE-ENTITYBASE-CANON` — "EntityBase 6 alan kanonik; sapma gerekcesiz YASAK."
Kurala uyuyorum. Ama NEDEN 6 alan, neden bu 6'si, hangi problem bu tasarimi
dogurdu — omurgamda YAZMIYOR. Omurgam alan tanimini bile bana vermiyor,
`database` skill'ine atif veriyor ("6 alan tanimi `database`'de") ve o skill'i
ACMADIM. Yani su an: kurali biliyorum, ALANLARI bile tam sayamam, gerekcesini
hic bilmiyorum. Bu kanonun kasitli tasarimi (tek kaynak ilkesi) ama sonucu su:
ENTITY YAZMAM ISTENIRSE once `database` skill'ini ACMAM ZORUNLU.

(b) GEREKCESI VAR AMA BENDE OLMAYAN (adresi biliyorum, icerigi yok):
Bircok kural gerekcesini "saha kaniti" olarak references'a birakiyor. Ornek:
handoff'ta `HANDOFF-NO-APPROVAL-RELAY` icin kanonum "Saha kaniti: `behavior` ->
`references/saha-kanitlari.md` (2026-07-27 olcumu)" diyor — o dosya elimde
DEGIL. Kuralin MANTIGINI govde bana veriyor ("hedef agent bunu kendi kapisi icin
onay sayar, insan kapisi sessizce kapanir"), ama ARKASINDAKI OLCUMU gormedim.
Ayni sey `HANDOFF-NO-SUB-AGENT`, `BEHAVIOR-KNOW-OWN-VERSION` ve
`FLOW-OPEN-SKILL-FIRST` icin de gecerli.

Ayrica bu oturuma ozel bir tanesi daha (durustluk gerektiriyor):
Merkezden gelen DUZEN mesaji, kanonumda OLMAYAN kurallar getirdi — ClickUp sub
task statu akisi, "commit onayi Clara'da", sure kaydi yontemi. Mesajin kendisi
bunu kabul ediyor ("Kanonunda YOK, bu oturuma ozel — Mert'in karari"). Bunlara
uyuyorum cunku Mert'in karari olarak bildirildi; ama gerekcesi kanonumda yok,
kaynagi bu oturum.

=====================================================================
EMIN OLMADIGIM YERLERIN TOPLU ISARETI (durustluk kaydi)
=====================================================================
- S1'deki "sadece ad/tarif" listesi TAM olmayabilir; sistem mesajimdaki liste cok
  uzun ve OY disi aileleri de iceriyor. Benim alet cantama ait olanlari eksiksiz
  saydim, digerlerini ornekledim.
- S3/1'de CODE-COMMIT-CODE-ONLY ve REL-QA-PUSH'un tam govdesini gormedim
  (skill'leri acmadim) — elimdeki omurga ozeti + atif.
- Alintiladigim her metin, bu oturumda FIILEN actigim 6 skill'in govdesinden.
  Acmadigim bir skill'den alinti YAPMADIM.

BEKLEDIGIM: Yok — olcum cevabi teslim edildi.
