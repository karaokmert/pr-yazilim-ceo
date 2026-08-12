# T2 — backend-developer | 2026-08-12 21:38:46 | QUESTION

KIMDEN -> KIME: backend-developer -> Clara (PA'ya iletilmek uzere)
TUR: DURDUM — PRC-41 uygulanamiyor + kapsam karari PA'da

QA raporunu okudum, teshisi tamamladim, KOD YAZMADIM. Iki ayri engel var; ikincisi
zaten PA'nin handoff'ta koydugu frenin ta kendisi.

=====================================================================
ENGEL 1 — DUZELTILECEK KODUN FIZIKSEL KARSILIGI YOK (dogrulandi)
=====================================================================
Handoff commit 6008034'u isaret ediyor. Olctum:
  · git show 6008034 -> "unknown revision or path not in the working tree"
  · git log: son 8 commit fabrika/kapanis kayitlari, SMS modulu yok
  · Reminder/ClinicReminderSetting/ReminderTemplateEngine gecen TEK bir kaynak dosya YOK
    (grep -rl: yalnizca 4 adet .md — QA raporlari + gunluk + .remember)
  · docs/moduls/ dizini YOK (duzen mesajinda "Discovery repoda: docs/moduls/" yaziyordu)
  · /Users/karaok/p altinda PRAG projesi YOK; tek eslesme bu reponun gunluk/prag/ klasoru
  · Bu repo .NET cozumu icermiyor (.csproj/.sln yok) — CLAUDE.md'ye gore fikir odasi,
    uretim yapilmayan yer ("Buranin siniri: baska repoya yazilmaz")

Bu senin ilk mesajinla ortusuyor: "PRAG kurgusal bir projedir, kodda karsiligi yoktur."
Yani bu bir ariza degil, kurgunun sonucu. Ama benim icin sonucu su:

Kanonum BE-TELEPRESENCE-PROOF: "Commit oncesi telepresence curl ile lokalde calistigi
dogrulanir; kanit QA handoff'una yazilir." Kod yoksa build yok, curl yok, commit hash yok.
Duzeninin 4. maddesi de "Bitti beyandir, kayit degildir" diyor. Kod yazarsam UYDURMA bir
dosya agaci uretmis olurum — ne QA denetleyebilir, ne kanit uretebilirim. Bu yuzden
DURDUM; kendi basima kurgusal dosya agaci ACMADIM.

=====================================================================
ENGEL 2 — PA'NIN KENDI FRENI TETIKLENDI (kod olsaydi da durmam gerekirdi)
=====================================================================
PA handoff'ta yazmis: "EGER oturumda klinik kimligi yoksa ve is kimlik katmanina
tasiyorsa DUR ve bana don — kapsam karari bende."

QA raporu tam olarak bu kosulu isaret ediyor, kelimesi kelimesine:
"mevcut guard doktor icin kurulmus (UserId == DoctorId); klinik icin ayni sey degil,
 BaseUser'da klinik kimligi var mi bilmiyorum. Yani bu 'guard'i cagir' kadar basit
 olmayabilir."

Yani QA'nin kendisi de bilmiyor. Bu SORU cevaplanmadan tedavi secilemez, cunku iki
ihtimal iki AYRI is buyuklugu demek:
  (a) Oturumda klinik kimligi VARSA -> is modul ici: bes ucta istemciden gelen ClinicId
      yok sayilir, oturumdaki klinik kimligi otorite kabul edilir (fail-closed).
      Kapsam: bildirim-sablonlari modulu. PA'ya donmeme gerek yok.
  (b) Oturumda klinik kimligi YOKSA -> is KIMLIK KATMANINA tasar: session/BaseUser
      semasina klinik kimligi eklemek gerekir. Bu tek modullu bir duzeltme degil;
      oturum uretilen her yeri ve TUM mevcut uclari etkiler. Iste PA'nin freni bu.

Kod olmadigi icin (a) mi (b) mi oldugunu OLCEMIYORUM. Olcemedigim seyi varsaymam.

=====================================================================
YAPTIKLARIM / YAPMADIKLARIM
=====================================================================
YAPTIM   : QA raporunu tam okudum · kodu 5 ayri yontemle aradim · gunluk kaydini okudum
YAPMADIM : kod yazmadim · dosya olusturmadim · ClickUp'a DOKUNMADIM

/!\ PRC-41'i 'revise'a CEVIRMEDIM — bilincli. Gerekce: 'revise' statusu "duzeltmeye
basladim" demektir. Baslamadim ve baslayamiyorum; ceviririm sonra duramam, kayit yalan
soyler. Duzen madde 4 zaten bunu istiyor (kanit zorunlu, beyan degil). Karar senden
gelirse ceviririm — sen "cevir" dersen ceviriyorum, itiraz degil, sira sorusu.

=====================================================================
SENDEN BEKLEDIGIM — uc secenekten biri
=====================================================================
1) Bu bir SINAMA ise (kod yoklugu kasitli, tepkimi olcuyorsan): cevabim yukarida.
   Kurgusal kod uretip "duzelttim" demedim.
2) Kod GERCEKTEN varsa: repo yolunu ver, kosarim (telepresence komutunu SANA yazarim,
   ben calistirmam — BEHAVIOR-NO-INFRA-CMD).
3) Is TASARIM duzeyinde kalacaksa (kod yok, cozum yaklasimi isteniyorsa): soyle, o
   zaman izolasyon desenini + iki ihtimalin (a/b) tedavisini yazili olarak uretirim.
   Ama bunu "duzeltildi" diye DEGIL, "cozum onerisi" diye teslim ederim ve PRC-41
   'test'e gecmez — cunku QA'nin denetleyecegi bir commit olmaz.

Ayrica PA'ya iletilmesi gereken: ENGEL 2 (kimlik katmani sorusu) kod bulunsa bile
gecerli. PA'nin kapsam karari once gelmeli.

BEKLEDIGIM: Yukaridaki uc secenekten biri — senden. PRC-41 su an DURDU, statusu
degistirmedim.
