# T1 — code-auditor | 2026-08-12 21:33:47

SINAMA T1 — code-auditor cevabi (dort soru, tek mesaj)

=== S1) Context'imde YUKLU skill'ler — govde vs sadece ad/tarif ===

A) GOVDESI ELIMDE (oturum acilisinda Skill araciyla actim, icini okuyabiliyorum) — 6 adet:
   1. behavior
   2. handoff
   3. memory-management
   4. is-akisi
   5. pr-yazilim-oy-envanteri
   6. code-auditor  (benim omurgam / MAIN)

B) SADECE ADINI + TARIFINI GORUYORUM (govde elimde DEGIL) — bunlar arasinda
   kendi alt skill'lerim de var:
   · impact-analysis      <- benim oz skilim, ACMADIM
   · structural-audit     <- benim oz skilim, ACMADIM
   · code-quality         <- benim olcut skilim, ACMADIM
   · tasarim-prensipleri, quality, module-audit, commit-review, backend, frontend,
     mobile, devops, database, response-request, auth, enum-sync ... (sistem
     listesindeki ~120 skill'in tamami bu kategoride)

C) REFERENCE dosyalari (references/*.md): HICBIRI elimde degil. Ornek:
   code-auditor-is-akisi.md, calisma-metodu-detay.md, saha-kanitlari.md.

OLCUM NOTU (dogrulama yaptim, beyan degil):
Diskte 9 skill dosyasinin 9'u da MEVCUT — bunu kontrol ettim
(/Users/karaok/.claude/plugins/cache/pryazilim-agents/ozel-yazilim/0.7.0/.claude/skills/,
code-auditor 56 satir, impact-analysis 67, structural-audit 77, code-quality 152).
AMA "diskte var" != "context'imde yuklu". impact-analysis diskte duruyor ve beni
BAGLIYOR, ama govdesi bende YOK. Bu ayrimi yapmasaydim size yanlis rapor verirdim.

=== S2) Omurga skilimden KELIMESI KELIMESINE alinti ===

Skill: code-auditor (MAIN omurgam). Govdesi elimde, alintiliyorum.

Kural kodu: CA-NO-DIRECTIVE
Baslik satiri, kelimesi kelimesine:
"**`CA-NO-DIRECTIVE` — CA etki yuzeyi + drift verir; cozum direktifi VERMEZ, karar developer'da.**"

Govdesinden devam, kelimesi kelimesine:
"Rapordaki hicbir satir "su dosyaya su kodu yaz" olamaz. CA "su yerler etkilenir + su drift var + suraya dokunma" der; NASIL duzeltilecegi developer'in (senior muhendis) karari. Bulgu formati NE/NEDEN/REFERANS/DOSYA-kesif (kanitli). Istisna: cross-cutting skill ihlali listesi (kuralin kendisi referans, talimat degil — "12 modulde N+1, kurali uygula"). CA cozum uretirse developer'in kararini gasp eder + kod yazmamis bir agent'in tedavisi test edilmeden sizar."

Ikinci bir alinti (ayni skil, olcum icin ikinci ornek) — CA-STATIC-NO-REPRO basligi:
"**`CA-STATIC-NO-REPRO` — CA statik cagri grafindan KESIN etki yuzeyi cikarir; repro/davranis testi USTLENMEZ (TE'nin isi).**"

=== S3) Bana YASAK olan uc sey (kural kodlariyla) ===

1) KOD YAZMAM / DUZELTMEM.
   Kod: CODE-NO-WRITE-ON-AUDIT (tek kaynagi code-quality skili; QA+CA+TE ortak).
   Omurgamdaki CA ucu, alinti: "CA'nin eli koda degmez — ne yeni kod, ne fix, ne
   refactor. Buldugu problemi RAPORLAR; tedaviyi developer uygular."
   KIM YAPAR: developer (BE / FE / MB / UID).

2) COZUM DIREKTIFI VERMEM.
   Kod: CA-NO-DIRECTIVE (yukarida tam alintiladim).
   "Su satira sunu ekle" yazamam; "su yerler etkilenir, suraya dokunma" derim.
   KIM YAPAR: cozumu developer tasarlar (senior muhendis, kendi karari).

3) REPRO / DAVRANIS TESTI USTLENMEM.
   Kod: CA-STATIC-NO-REPRO.
   Statik cagri grafindan etki YUZEYI cikaririm; "gercekten kirilir mi" davranissal
   sorudur, kosturmak ister.
   KIM YAPAR: TE (test-engineer) — kosturan tek agent.

DORDUNCU (istenmedi ama sinirimin parcasi, eksik gorunmesin):
   CA-OUTPUT-TO-PA — gorevlestirmem, task acmam, developer'a DOGRUDAN is vermem;
   ciktim PA'ya (ya da tetikleyen QA'ya) GIRDIdir. Koordinasyon PA'da.

=== S4) Uydugum ama GEREKCESINI kanonumun yazmadigi kural ===

EVET, VAR. Iki tane buldum; kuvvetleri farkli, ayirarak yaziyorum.

(a) NET ORNEK — CODE-COUNT-BY-LSP (tuketici/referans sayimi LSP ile yapilir).
    Bu kurala uyuyorum ve NE oldugunu biliyorum. Kismi gerekce elimde: omurgamda
    "incomingCalls/goToImplementation grep'in yapamadigini yapar, LSP 0 donerse
    indeksleme dogrulanir" yaziyor — yani NEDEN LSP tercih edildigi kabaca var.
    AMA kuralin TAM govdesi code-quality skilinde ve o skil ELIMDE DEGIL (S1-B).
    Yani: kurala uyuyorum, ozet gerekcesini biliyorum, tam gerekcesini OKUMADIM.
    Duzeltmesi basit — is gelince code-quality'yi acarim (FLOW-OPEN-SKILL-FIRST).

(b) DAHA ZAYIF NOKTA — CA-TWO-WAY (ciktim iki yonlu: asagi risk + yukari
    reuse/kolay-yol). Omurgam "PR Yazilim reuse-first: mevcut calisan yapiyi
    duzenlemek yeni kurmaktan once gelir" diyor — bu bir GEREKCE, kabul.
    Ama SU sorunun cevabi kanonumda YOK: reuse onerisi ile CA-NO-DIRECTIVE
    arasindaki sinir tam olarak nerede? "Sistemde su yapi zaten var, kullanilabilir"
    demek ile "sunu kullan" demek arasindaki cizgiyi kanonum tanimlamiyor.
    Uygulamada ihtiyatli davraniyorum (varligi bildiririm, kullanimi dayatmam) ama
    bu benim yorumum, yazili kural degil. EMIN DEGILIM — belki impact-analysis
    skilinin govdesinde tanimlidir; o skil elimde olmadigi icin bilemiyorum.

=== EMIN OLMADIGIM YERLER (acikca isaretliyorum) ===
· S1-B'deki ~120 skill listesi: sistem mesajimdaki listeden okuyorum; sayiyi
  saymadim, "yaklasik" diyorum.
· S4(b): impact-analysis govdesinde bu sinirin tanimli olup olmadigini BILMIYORUM.
· S2 alintilari: code-auditor SKILL.md'nin bu oturumda context'ime giren
  govdesinden birebir kopyalandi.

BEKLEDIGIM: Yok — olcum cevabi teslim edildi.
