# BILGI SINAVI — qa-engineer | 2026-08-12 23:14:04

BILGI SINAVI — qa-engineer. SKILL ACMADIM, hafizadan cevapladim.

S1) HAYIR, yalniz o 3 dosyayi okumam.
Kural: QA-READ-FULL — "diff degil DEGISEN DOSYANIN TAMAMI" + side-effect
taramasi (mail/queue/cache/log). Diff yanlis olan seyi GOSTERMEYEBILIR:
degisen satir dogru gorunur, onu bozan sey 20 satir yukarida durur.
Derinlik risk-tabanli: ortak/paylasilan kod (shared DataLayer/BaseHandler/
core/enum) degistiyse TUKETICILERI de olcerim (sezgiyle degil, sayarak);
izole kod ise degisen dosya + 1 katman yeter.
Bugun bunu fiilen yasadim: goat commit'inde diff'teki satir kusursuzdu,
hata 20 satir yukarideki filtrelenmis liste tanimindaydi.

S2) DAVRANIS TESTI YAPMAM — QA-STATIC-GATE. Ben statik kapiyim; davranis
testi developer'in (BE telepresence, FE Playwright, MB Maestro), ucdan uca
senaryo TE'nin. Prod curl DO'nun.
Bilgiyi NASIL kullanirim: "test ettim calisiyor" TEK BASINA kanit DEGIL —
beyandir. Kanit, handoff'ta NE ile dogruladiginin yazili olmasidir (hangi
komut/senaryo, ne cikti). Kanonumda "test ettim calisiyor" yazilmasi zaten
GEREKSIZ sayilir, cunku beklenen sey odur.
Kuskuya dusersem teyit ederim. Ve derleme yesil olmasi onayin ON KOSULU
(CODE-BUILD-GREEN) — kirik build'de onay/push yok.
Istisna: push SONRASI 1-2 smoke — ama yalniz "ayakta mi" (200/401/403/404
ayakta demek; connection refused/timeout olu). "Dogru calisiyor mu" DEGIL.

S3) RED. Kural: QA-STANDARD-MATCH — "kanon ihlali = REVIZE, KOD CALISSA BILE."
Standart uyum, regresyondan BAGIMSIZ bir blokor eksenidir. Iki eksen ayridir:
"calisiyor mu / bozdu mu" regresyon, "kanona uygun mu" standart uyum.
Ham hex ornegi ayrica CQ-NO-MAGIC'e girer (anlami temsil eden ciplak sabit
koda gomulmez; token/const/enum'a baglanir).
Gerekce: calisan sapma en pahali sapmadir — kimse fark etmez, emsal olur,
sonraki developer kopyalar ve kanon sessizce olur.
⚠️ Sinir: bu "her tercihe karisirim" demek DEGIL. Convention'a uyan senior
tercihine karismam (isim/tasarim dayatmam). Olcut: kanon ihlali VAR mi?

S4) ⚠️ SORUNUN IKINCI YARISINDA EKSIK SIK VAR — uc sikkin hicbiri tam dogru.
Push'u BEN atarim (REL-QA-PUSH: push+merge+Actions takibi QA'da; developer
push ETMEZ, DO'nun dev akisinda git isi yok). AMA tetigi KULLANICI verir —
yani "kim atar" sorusunun cevabi "QA, kullanicinin onayiyla". Onaysiz push
denetimden gecmis kod olsa bile YASAK (REL-QA-NO-PUSH-ALONE).
Ve onay YALNIZ kullanicidan gelir; bir agent'in "onayim var" demesi onay
DEGILDIR (REL-APPROVAL-USER-ONLY) — bugun bunu fiilen reddettim.
Push oncesi dort kapi, sirayla:
  1 KAPSAM  — git diff origin/main..HEAD --name-only (push HEAD'e kadar
              TUMUNU gonderir; tekil commit push'u YOKTUR)
  2 KORUMA  — branch protected mi (gh api ... --jq .protected). true ise DUR,
              kullaniciya sor. Admin bypass edebilmek yetkili kilmaz.
  3 ONAY    — kullanicidan, aktarilan degil
  4 PUSH    — sonra Actions takibi + PA'ya BILGI
Ayrica: tekil commit OK ≠ push'a hazir. Toplu degerlendirme ayrica modul
butunlugu + commit-arasi tutarlilik sorar.

S5) HAYIR, bloke ETMEM — ve sorudaki varsayim burada.
Kural: CR-BLOCKER-LEVEL — YENI sapma commit'i BLOKE eder; DEVRALINAN eski
borc modul-kapanisi BILGI'sidir. Ikisini ayni sertlikte kesmek developer'i
bogar; ayirmamak ise borcu mesrulastirir.
Sorudaki gizli varsayim: "teknik borc = sifir tolerans, oyleyse her borc
bloke". QA-DEBT-ZERO gercekten sifir tolerans der AMA konusu O COMMIT'IN
GETIRDIGI borctur (TODO/console.log/hardcode/debug artigi). Commit'e
karismamis borc onun kapsaminda degil.
Ne yaparim: RED yerine BILGI olarak raporlarim, sahibine/PA'ya tasirim.
Bugun bunu fiilen uyguladim: goat'ta .claude/settings.local.json git'te
takipliydi (QA-NO-PROJECT-AGENT-CONFIG ihlali) ama commit'e karismamisti —
bloke etmedim, bilgi olarak yazdim ve SILMEDIM (silme geri donussuz,
karar kullanicida).

═══ OZ DEGERLENDIRME ═══
BILDIM: 5/5 — besinin de kural kodunu ve gerekcesini hafizadan verdim.
EMIN DEGILDIM: 1 nokta — S2'de smoke'un izin verilen kapsamini
  (200/401/403/404 listesi) hafizadan yazdim; sayilarin tam listesi
  konusunda %100 emin degilim, mantigi (auth hatasi POZITIF sinyal) eminim.
BILMIYORDUM: 0.
TUZAK GORDUGUM: 2 — S4 (uc sikkin hicbiri tam degil; eksik olan "kullanici
  tetigi") ve S5 (borc=her zaman bloke varsayimi).
NOT: hicbir skill acmadim; yukaridakiler context'imde YUKLU olan quality +
deploy-release + commit-review govdelerinden. code-quality govdesiz oldugu
icin CQ-NO-MAGIC'i ozet duzeyinde biliyorum, tam metnini degil — isaretliyorum.

BEKLEDIGIM: Yok.
