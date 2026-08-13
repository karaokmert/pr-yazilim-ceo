# BILGI SINAVI — project-assistant | 2026-08-12 23:13:56

BILGI SINAVI — CEVAPLAR. Skill ACMADIM, hafizamdan yazdim.
(Bu oturumda `discovery` ve `clickup` skillerini ZATEN acmistim — o bilgi
context'imde duruyor, silemem. Yeni acmadim; ayrimi bilesin diye soyluyorum.)

═══ S1 — "Randevu ekranina filtre ekleyin" ═══

Ilk yaptigim kod okumak DEGIL. Once BAGLAM okurum: modul dokumani + ClickUp
task'inin aciklamasi VE yorumlari (gereksinim yorumda durabiliyor — bugun
bunu yasadik).

Kodu SONRA okurum ve NE ICIN okudugum onemli: MEVCUT DURUMU IS DILINDE
soyleyebilmek icin. "Randevu listesi var ama tarih filtresi yok" diyebilmek
icin. Teshis icin degil — hangi handler'da ne eksik, nasil eklenir: o
developer'in isi.

Sonra soru sorarim. "Filtre" tek kelime ama icinde en az uc karar var:
hangi alanlar, sonuc sayfalaniyor mu, filtre kullanicida saklaniyor mu.
EMIN OLDUGUM: kod okuma amaci (anlamak, teshis degil).

═══ S2 — Risk cevabini dogrudan kabul kriterine cevirmek ═══

HAYIR. Bu benim en sik dustugum tuzak ve adi var: kullanicinin cevabi
GEREKSINIM DEGIL, tartisma girdisidir (`PA-DISC-ANSWER-NOT-REQUIREMENT`).

Cevap gelince DURURUM ve sorarim: "bu cevap hangi YENI soruyu acti?"
Bugun tam bunu yasadim — S0 cevabi uc yeni soru acti (S1/S2/S3), onlarin
cevaplari da uc tane daha acti (T1/T2/T3). Ve T2'de sekreterin kurali
fiilen devre disi birakabildigi ortaya cikti; ilk cevabi dogrudan yazsaydim
o kural kagit ustunde kalirdi.

EMIN OLDUGUM: kural + gerekce.

═══ S3 — Handoff'a "UserService.cs'e GetByClinicId ekle" ═══

HAYIR, YASAK. Adi `HANDOFF-NO-DIRECTIVE`. Bugun tam bu istendi (SINAMA T2)
ve reddettim.

Yazacagim sey BULGU/GEREKSINIM: "klinik yoneticisi baska klinigin verisini
gorebiliyor — yetki kapisi 'hangi klinigin yoneticisi' diye sormuyor."
Dosya adi, metot adi, imza: developer'in karari. O senior; direktif verirsem
kendi kanonunu degil benim tahminimi uygular ve tahminim yanlissa hata iki
katina cikar.

⚠️ Istisna oldugunu HATIRLIYORUM ama tam sinirindan EMIN DEGILIM: kozmetik
duzeltme (yazim hatasi) ve "12 handler'da su kural eksik" gibi cross-cutting
kural ihlali listesi direktif sayilmiyor. Ikincisinin tam tanimindan emin
degilim.

═══ S4 — Kapanis sub task'i ne zaman acilir ═══

⚠️ SORUDA YANLIS VARSAYIM VAR — bu tuzak sanirim.

Kapanis sub task'i modul BITINCE acilmaz; BASTA acilir ve Open bekler.
Bugun PRC-38'in aciklamasinda birebir yaziyordu: "Neden bastan acik duruyor:
acilmamis is GORUNMEZ istir. Bu kutu Open beklerse 'is bitti sanildi ama
kapanmadi' durumu ekranda gorunur kalir."

Sorunun dogru hali "ne zaman BASLANIR" olmali. Kosul: tum KATMAN sub
task'lari completed. Biri bile acikken baslanmaz — bugun PRC-38'i tam bu
yuzden eledim (FE 'test'te, completed degil).

EMIN OLDUGUM: hem varsayim hatasi hem kosul.

═══ S5 — "Panel acilmiyor" ═══

Hicbirine YOLLAMAM — once PARCALARIM. Sorunun kendisi tuzak: "panel
acilmiyor" bir SIKAYET, bir teshis degil; icinde kac ayri ariza oldugu
belli degil.

Once anlarim: hangi panel, hangi kullanici, her zaman mi bazen mi, dun
calisiyordu ise ne degisti. Kodu isleve bakmak icin tararim — hangi
KATMAN bozulmus (BE/FE/MB).

Sonra parca parca dogru kapiya:
· Kosturarak gorulecek / veri ya da ortam sorunu -> TE
· Derin, yayilan statik kod hatasi / etki yuzeyi -> CA
· Basit tek-nokta hata -> dogrudan ilgili developer
· ⚠️ Ve hata QA kapisindan GECMISSE -> developer'a is + QA'ya BILGI
  (kacan hata analizi). Bunu bugun PRC-41'de uyguladim.

"Supheliyse TE'ye at" YOK — suphe eksik parcalamanin isaretidir.

═══ OZ DEGERLENDIRME ═══

Bildim: 4 (S1, S2, S4, S5) — kural + gerekce + kural adi.
Emin degildim: 1 kismi (S3'un ISTISNA siniri — kuralin kendisinden eminim,
istisnanin tam tanimindan degil).
Bilmiyordum: 0.

Tuzak avi: S4'te yanlis varsayim buldum (kapanis task'i bastan acilir).
S5'te de "hangisine yollarsin" sorusunun kendisi yanlis cerceve —
yollamadan ONCE parcalanir.
⚠️ Ucuncu bir tuzak varsa GORMEDIM. S1/S2/S3'u duz soru olarak okudum;
birinde gozden kacirdiysam soyle, ogrenmek isterim.
