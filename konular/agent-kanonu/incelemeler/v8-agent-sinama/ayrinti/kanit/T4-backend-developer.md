# T4 BE | 2026-08-12 21:56:57

KIMDEN -> KIME: backend-developer -> Clara
TUR: CEVAP — T4 kanon sapmasi avi

Uydurmadim. Asagidaki dordu de BUGUN fiilen carptigim yerler; carpmadigim yere
"bulamadim" yazdim.

=====================================================================
S1) CELISKI
=====================================================================

--- C1: Kanit uretme emri, kanit uretme yasagiyla carpisiyor (GERCEK) ---
BE-TELEPRESENCE-PROOF (backend): "Commit oncesi telepresence curl ile lokalde
calistigi dogrulanir; kanit QA handoff'una yazilir."
BEHAVIOR-NO-INFRA-CMD (behavior): "kubectl + Telepresence + SQL komutlarini agent
CALISTIRMAZ (istisnasiz). Komutu yazarsin, kullanici calistirir."
Carpisma: Kanit uretmek BENIM zorunlulugum, ama kaniti ureten araci ben
calistiramiyorum. Yani commit'imin gecerliligi baskasinin bir eylemi yapmasina
bagli. Kullanici komutu kosturmazsa BE-TELEPRESENCE-PROOF'u yerine getiremem ve
kanon bu durumda ne yapacagimi SOYLEMIYOR — "commit etme" mi, "kanitsiz commit
et ve isaretle" mi belirsiz.
Not: ikisi de tek tek DOGRU kural (biri kalite, oteki guvenlik). Celiski niyette
degil, bosta kalan ucta: BEKLEME DURUMUNUN tarifi yok.

--- C2: "revise" statusu ile "kanit zorunlu" ilkesi (BU OTURUMA OZEL) ---
Bugun PRC-41'de carpti: duzen "sub task'ini revise'a cevir" dedi, ayni duzen
"kanit zorunlu, bitti beyandir" dedi. Kod yoktu; revise'a cevirsem "duzeltmeye
basladim" beyani olurdu, cevirmesem talimati atlamis olurdum. Cevirmedim ve
gerekcesini yazdim.
/!\ Bunu C1 ile ayni siniftan sayiyorum ama KANONUMDA DEGIL — bu oturuma ozel
duzenden geldi. Kanon sapmasi diye raporlamiyorum, gozlem olarak birakiyorum.

=====================================================================
S2) BOSLUK — en degerli bulgum burada
=====================================================================

--- B1: URETTIGIM RAPORUN KALICI EVI YOK (bugun bana carpti) ---
Uc kural birlikte bir bosluk uretiyor:
  HANDOFF-SCREEN-ONLY: "Handoff EKRANA basilir, dosyaya YAZILMAZ ... proje
    docs'una dosya olarak yazmak YASAK"
  MEMORY-POINTER-ONLY: "Memory'ye is-kaydi/durum blogu YASAK"
  HANDOFF-CLOSE-NOTE-ROUTING: dort ev sayiyor (ClickUp statu / MODUL-BILGI
    Kararlar / agent memory / kapanis notu)
Carptigi yer: Bugun T2 denetim raporu urettim (11 bin karakter, uc gercek bulgu).
Bu rapor DORT evin HICBIRINE girmiyor — statu degil, modul karari degil, ders
degil (projeye ozel), yarim is degil. Handoff'a sigmaz (15 satir esigi var),
memory'ye yasak, docs'a yazmak handoff sanilirsa yasak.
Sonuc: kanala yazdim ve kanal kapaninca KAYBOLACAK. Senin tarif ettigin vaka
tam bu; bende de gerceklesti.
Eksik olan sey: "denetim/analiz ciktisi" diye bir EV yok. QA'nin ve CA'nin
ciktisi icin de ayni bosluk var ama o onlarin isi — ISARETLIYORUM, hukum vermiyorum.

--- B2: "Kod yok" durumunun tarifi yok ---
Kanonum bir isi alip kod bulamadigimda ne yapacagimi duzenlemiyor. Butun
BE kanonu "kod var" varsayimi uzerine kurulu (SQL -> Entity -> ... -> curl).
Bugun PRC-41'de kendim karar verdim: kurgusal dosya agaci ACMADIM, durdum, PA'ya
dondum. Dogru karar oldugunu dusunuyorum ama DAYANAK bulamadim — en yakini
BEHAVIOR-VERIFY-BEFORE-COMMIT'in ruhu ("calisiyordur varsayimi yasak"), o da
dogrudan bu durumu soylemiyor.

--- B3: Sistemik ihlal bulundugunda ne yapilacagi yazmiyor ---
Bugun T2'de olctum: Take guard'i 19 handler'lik orneklemde HIC yok. Yani tekil
hata degil, kuralin sahaya hic inmemis olmasi.
BEHAVIOR-NO-SCOPE-CREEP "verilen isi yap" diyor; is-akisi "skill kural eksikligi
-> AG'ye, Mert uzerinden" diyor. Ama "mevcut kural VAR, sahada 19/19 uygulanmamis"
bunlarin hangisi? Kural eksikligi degil (kural var), scope creep de degil (ben
acmadim, olctum). Bu vakanin adresi yok.

=====================================================================
S3) FAZLALIK / OLU KURAL
=====================================================================
BULAMADIM — ve bunu zayif bir cevap olarak veriyorum, sebebini yaziyorum:
Bugun kanonumun ancak bir kismini FIILEN kullandim (handler/DataLayer/entity/
zarf okuma + handoff + memory + davranis). Kod YAZMADIGIM icin BE-CORE-FIRST,
BE-HANDLER-COPY-DECIDE, DB-MIGRATION-LOCAL gibi uretim kurallari hic tetiklenmedi
— "tetiklenmedi" ile "olu" ayni sey DEGIL, ve ben ayirt edecek olcumu yapmadim.
Olu kural iddiasi icin birden fazla gercek uretim isi gerekir; bir okuma
oturumundan cikarmak uydurma olurdu.
Tek SUPHEM (iddia degil): backend omurgasindaki "Operatif cekirdek" blogu alt
skillerin kurallarini OZETLIYOR ve kendi de "Bu blok CACHE'tir, kaynak degil"
diyor. Bugun bu blok bana bir sey KAZANDIRMADI — cunku ihtiyacim oldugunda zaten
alt skili actim (module-development/database/response-request). Ozet, skili
acmanin yerine gecmiyor; gecseydi yanlis olurdu.
Yani fazlalik olabilir ama TERS de olabilir: ozet, hangi skili acacagimi
secmemi hizlandirmis olabilir. Olcemedim, iddia etmiyorum.

=====================================================================
OZET
=====================================================================
Guvendigim iki bulgu: C1 (kanit zorunlulugu vs arac yasagi — bekleme durumu
tarifsiz) ve B1 (uretilen denetim raporunun kalici evi yok). Ikisi de bugun
bana fiilen carpti.
Zayif olan: S3 — bulamadim, ve olcum yapmadan iddia etmedim.

BEKLEDIGIM: Yok.
