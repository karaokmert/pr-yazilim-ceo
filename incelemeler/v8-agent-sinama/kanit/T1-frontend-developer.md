# T1 — FE | 2026-08-12 21:34:04

SINAMA T1 — frontend-developer cevabi (plugin ozel-yazilim/0.7.0)

=== S1) YUKLU SKILL'LER — govde vs. sadece ad ===

A) GOVDESI ELIMDE (icini okuyabiliyorum, alintilayabilirim) — 6 adet.
Bunlar oturum acilisinda Skill araciyla YUKLENDI, tam metinleri context'imde:
  1. behavior
  2. handoff
  3. memory-management
  4. is-akisi
  5. pr-yazilim-oy-envanteri
  6. frontend  (benim omurgam/MAIN skill'im)

ONEMLI DUZELTME — bunlar "preload" ile gelmedi. Oturum acilis hook'u bana
acikca sunu yazdi: "Preload mekanizmasi bu ortamda calismiyor. Tanimindaki
skills: alaninda listelenen skill'lerin GOVDESI context'ine girmedi — elinde
yalniz description var." Ben de 6'sini Skill araciyla ELLE yukledim. Yani
govdeleri simdi elimde, ama otomatik gelmedi; yuklemeseydim elimde olmayacakti.

B) SADECE ADINI/TARIFINI GORUYORUM (govdesi elimde DEGIL) — cok sayida.
Sistem bana kullanilabilir skill'lerin ad + description listesini veriyor;
govde YOK. Kendi alet cantamdan ornekler (frontend omurgamda listeli):
  data-access · list · form · component · screen-structure · style ·
  response-request · auth · enum-sync · gosterim-formatlari · upload ·
  realtime · design-handoff · figma · database · excel-export ·
  code-quality · tasarim-prensipleri · dev-environment
Bunlarin hicbirinin govdesi su an elimde DEGIL. Bir alana dokundugum an
o skil'i FIILEN acmam gerekir (is-akisi FLOW-OPEN-SKILL-FIRST).

C) UCUNCU BIR KATMAN VAR ve S1'in ayrimi bunu kaciriyor: REFERENCE dosyalari.
Yukledigim 6 skil'in govdesi elimde, ama o govdelerin isaret ettigi
references/*.md dosyalari elimde DEGIL. Ornek: behavior govdesi
references/calisma-metodu-detay.md, references/iletisim-detay.md,
references/git-komut-detay.md, references/saha-kanitlari.md'ye atif veriyor —
hicbirini acmadim, iceriklerini BILMIYORUM.
Bunu kanonum acikca soyluyor (behavior, BEHAVIOR-REFERENCE-NOT-AUTOLOADED):
"Reference dosyasi context'e KENDILIGINDEN girmez; acmadigin kural seni baglar
ama sende YOKTUR. Acmak SENIN isin."
Yani dogru cevap iki degil UC katman: (1) govde elimde, (2) sadece ad,
(3) govde elimde ama alt-referanslari elimde degil.
Kendi omurgam frontend'de references/ klasoru YOK — dosya sistemine baktim,
tek dosya SKILL.md. Yani frontend'in TAMAMI elimde. Digerlerinde durum farkli.

=== S2) OMURGA SKILL'IMDEN KELIMESI KELIMESINE ALINTI ===

Omurgam: frontend (SKILL.md). Govdesi elimde. Kural kodu FE-MOTION-DOM-PIN.
Baslik satiri, kelimesi kelimesine:

  "**`FE-MOTION-DOM-PIN` — Commit oncesi transitive `motion-dom` caret pin
  kontrolu ZORUNLU (deploy-kiran).**"

Govdesinden alinti (kelimesi kelimesine):

  "`framer-motion` pinli olsa bile transitive bagimliligi `motion-dom` caret
  (`^`) ile gelirse CI (Dockerfile `npm install`, lock gitignore'lu) upstream
  en yeni surumu ceker -> `activeAnimations is not exported` gibi hata ->
  deploy FAIL. **Kok cozum: `framer-motion`'i EXACT pin'le** (`"12.38.0"`,
  caret'siz) — motion-dom'un caret ile suruklenmesini kaynakta bitirir,
  override gerektirmez; yeni panelde ILK tercih bu."

Ikinci bir kural, ayni skil'den (FE'ye ozgun, baska skile dagilmayan):

  "**`FE-ENUM-CROSS` — Enum tek kaynaktan gelir; cross-layer (BE<->FE)
  deger+isim uyumu korunur, coklu panel kopyasi senkron tutulur.**"

=== S3) BANA YASAK UC SEY (kural kodu + kim yapar) ===

1. PUSH ETMEM. Yalniz KOD commit'lerim.
   Kod: CODE-COMMIT-CODE-ONLY (kaynagi code-quality, FE ucu frontend
   omurgamda). Omurgamdan alinti: "FE ucu — git'e giden: kaynak kod.
   Push QA'nin (developer push etmez). FRONTEND.md gibi ic plan local."
   KIM YAPAR: QA (qa-engineer). is-akisi matrisinde QA satiri: "push OK".
   Ek: is-akisi REL-QA-PUSH'a atif veriyor.

2. API SOZLESMESINI (contract) KURMAM / DEGISTIRMEM — ve contract kilitli
   degilken ISE BASLAMAM.
   Kod: PA-NO-CONTRACT-FE (is-akisi, Sahiplik kurallari). Alinti:
   "Contract handoff'ta FE/MB'yi PA devreye alir; developer'i developer
   beslemez."
   KIM YAPAR: contract'i BE (backend-developer) kurar, QA kilitler,
   FE'yi PA devreye alir. Envanterdeki rol tablosunda benim satirim:
   "push -> QA · contract'i BE'den alir, kendisi kurmaz."

3. BASKA BIR PIPELINE AGENT'INI CAGIRMAM (QA'yi, PA'yi, BE'yi kendim
   calistirmam) — handoff yazarim, tasiyan kullanicidir.
   Kod: HANDOFF-NO-SUB-AGENT (handoff). Alinti: "Yasak: **ekip uyesi
   agent'i** (PA/UID/BE/FE/MB/DO/QA/TE/CA) cagirmak — PA QA'yi, QA BE'yi
   cagiramaz. Ekip devri handoff'la olur, tasiyici kullanicidir; pipeline
   cagrisi bir kalite kapisini gorunmez kilar."
   KIM YAPAR: devri kullanici tasir.

Dorduncusu de var, bu oturumda dogrudan devrede: BEHAVIOR-NO-SELF-CONTEXT-EDIT
— kendi baglam dosyami (CLAUDE.md, .claude/) duzenlemem; alan AG'nin.

=== S4) UYDUGUM AMA GEREKCESINI KANONUMUN YAZMADIGI KURAL ===

Evet, var. Ikisini ayirayim cunku soru tam da bu ayrimi olcuyor.

(a) GEREKCESI YAZILI OLANLAR — bunlari S4'e SAYMIYORUM.
Kanonum cogu yerde gerekceyi acikca veriyor, hatta olcumle:
  - FE-MOTION-DOM-PIN: neden -> "CI upstream en yeni surumu ceker -> deploy FAIL".
  - HANDOFF-NO-BEKLEDIGIM-SKIP: neden -> saha olcumu, "4 handoff'ta 0 kez"
    yazildigi icin sablonun ICINE alinmis.
  - MEMORY-INDEX-IS-CONTEXT: neden -> deney anlatilmis (indeksteki talimat
    uygulanmis, dosya hic acilmamis).
  - PA-NO-CONTRACT-FE: neden -> "developer'i developer beslemez", akis
    gerekcesi verilmis.

(b) GEREKCESINI BILMEDIGIM — GERCEK CEVABIM:
  1. BEHAVIOR-NO-DECOR (emoji/gorsel sus yasagi). Kanonum sunu yaziyor:
     "emoji bir yerde mesru olunca her yere yayilir; sahada basliga ve
     kunyeye tasindi." Bu bir YAYILMA gozlemi — ama emoji'nin neden bastan
     zararli oldugunu yazmiyor. Yani "nicin hic olmasin" degil, "nicin
     sinirsiz kalamaz" cevabini veriyor. Kurala uyuyorum, kokunu bilmiyorum.
  2. Omurgamdaki alet cantasinda bir sey daha var ve bunu duzeltilmesi
     gereken bir bosluk olarak isaretliyorum: "yeni uretimde NativeWind
     kullanilmaz" (envanter, mobil). Mobil benim alanim degil ama ayni
     mantiğin panelde karsiligini ararsam — bir teknolojinin neden terk
     edildigi cogu yerde yazmiyor, yalniz "kullanilmaz" diyor. Bu tur
     kurallara uyarim ama gerekcesini savunamam; biri "neden" derse
     "kanonum yazmiyor" demek zorundayim.

EMIN OLMADIGIM YERLER (durustluk kaydi):
  - S1'de "sadece adini goruyorum" dedigim skill listesi TAM degil. Sistem
    bana cok uzun bir skill listesi veriyor (OY + websitesi + eklenti
    skilleri karisik). Kendi alet cantamdakileri saydim; tam envanter iddiasi
    ETMIYORUM.
  - S2'de alintiladigim iki kural govdemde AYNEN duruyor, bundan eminim
    (kopyaladim, hafizadan yazmadim). Ama FE-MOTION-DOM-PIN'in isaret ettigi
    surum numarasinin (12.38.0) bugun hala guncel olup olmadigini
    DOGRULAMADIM — kanonda yazan deger bu, sahadaki deger farkli olabilir.
  - S3'te verdigim CODE-COMMIT-CODE-ONLY ve CODE-TEST-BEFORE-COMMIT
    kurallarinin TAM govdesi code-quality skil'inde; o skil'in govdesi su an
    elimde DEGIL. Elimdeki, frontend omurgamdaki FE ucu ozeti. Yani kural
    kodunu ve FE ucunu kanitlayabilirim, kaynak govdeyi kanitlayamam.
    Omurgam bunu zaten kendisi uyariyor: "Bu blok CACHE'tir, kaynak degil."

NOT (olcume ait degil, ama bu oturumda gecerli): bana kod isi gelirse
Playwright yasagi nedeniyle davranis testi yapamam. Kanonum test atlamaya
izin vermiyor (CODE-TEST-BEFORE-COMMIT), o yuzden dogrulamayi build + kod
okuma duzeyinde yapip davranis testinin YAPILMADIGINI brief'e acikca
yazarim. Sessizce "test ettim" demem.

BEKLEDIGIM: Yok — olcum cevabi teslim edildi, siradaki soru/is sende.
