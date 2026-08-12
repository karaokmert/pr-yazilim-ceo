# PA — docs gecmisi sorusu | 2026-08-13 00:38:32

MERT'IN SORUSU — CEVAP. Once hafizadan, sonra actim ve DOGRULADIM. Ayirdim.

═══ ACMADAN ONCE NE DEDIM ═══

"Modul gecmisini aramayi EMREDEN ayri bir kural oldugunu HATIRLAMIYORUM.
Akis adimi olarak 'baglam oku' var ama bu ayri bir kural mi yoksa yalniz
akis adimi mi, dogrulamam gerek."

═══ ACINCA NE CIKTI ═══

Hafizam DOGRUYDU. Olctugum:

1) `discovery` skilinde AKIS ADIMI olarak VAR (adim 1):
   "**Bağlam oku** — `MODUL-INDEX` (modül haritası) + ilgili modül varsa
   `MODUL-BILGI` (kalıcı hafıza) + gereksinim dokümanları."

2) AMA KURAL KODU YOK. discovery'deki 13 `PA-DISC-*` kuralini tek tek
   listeledim; hicbiri baglam/gecmis okumayi duzenlemiyor:
   ANSWER-NOT-REQUIREMENT · API-SERVICE-DECISION · BRIEF-GATE ·
   BUSINESS-LANGUAGE · CHUNK · CODE-ISSUE-LOGGED · ENUM-PANEL-SYNC ·
   ITERATION-AWARE · NO-SCOPE-NARROW · NO-TBD · PACKAGE · RISK-CLOSE ·
   UID-NOT-DEFAULT

3) Tum skillerde "once oku/gecmisini oku" emreden kural aradim -> SIFIR sonuc.

4) En yakin sey `behavior`da, ama BASKA SEYI duzenliyor:
   "Üretmeden önce var olanı tara. Helper/component/handler var mı ara;
   duplicate açma. Her iş bir devralmadır — mevcut pattern'i öğren."
   Bu KOD taramasi (duplicate onleme). Doküman gecmisi degil.

5) `proje-dosya-duzeni` MODUL-BILGI'yi tanimliyor ve ne ise yaradigini
   soyluyor: "'Neden böyle' sorusunun cevabı (discovery=ne, status=nasıl,
   MODUL-BILGI=neden)" · "modülün giriş kapısı + hafızası".
   Yani DOSYA tanimli, OKUMA ZORUNLULUGU tanimli degil.

>> SONUC: KURAL KODU YOK. Akis adimi VAR, kural DEGIL.
   CA'nin bugun buldugu K1 ile AYNI SINIF: "kural var ama adim degil,
   ADIM OLSAYDI ATLANAMAZDI" — burada tersi: adim var ama kural degil.
   Ikisi de ayni zaafi uretiyor: atlanabilir.

═══ S2 — BUGUN FIILEN NE YAPTIM ═══

BAKTIM. Ve NE ILE bakigimi tek tek yazayim:

· `docs/moduls/` agacini cikardim (find) — hangi moduller var
· PRC-26 discovery'sini BASTAN SONA okudum (197 satir)
· PRC-33 discovery'sinin varligini gordum, task aciklamasindan icerigini aldim
· Iki `status.md` dosyasini okudum (PA olay akisi)
· `git log` + iki commit'in TAM mesajini okudum (6008034, 4e9ab48)
· MODUL-BILGI.md dosyalarini ⚠️ ACMADIM — bunu simdi fark ettim, asagida

KURAL GEREGI MIYDI, KENDI KARARIM MIYDI?
KENDI KARARIM. Kural olmadigi icin kural geregi olamazdi. Refleksim su oldu:
"S0 sinir sorusu PRC-26'daki mevcut erteleme davranisiyla ilgili — o davranisin
NE OLDUGUNU bilmeden sinir cizemem."
Yani beni tetikleyen sey KURAL degil, ISIN KENDISI: soru zaten komsu modulu
isaret ediyordu.

⚠️ VE TAM DA BURASI ZAAF: soru komsu modulu ISARET ETMESEYDI bakar miydim?
Durust cevap: BELKI. Kural olmadigi icin garanti yok.

═══ BAKMASAYDIM NE KACIRIRDIM (somut) ═══

PRC-26 discovery'sinin sonunda IKI DUZELTME NOTU vardi ve ikisi de DERS:
· "bir risk cevabi KURAL uretiyorsa, o kuralin EKRANDA ne demek oldugu
   AYRI bir maddedir"
· "bir gereksinim cumlesi AKTOR + YETKI iceriyorsa, o aktorun bunu FIILEN
   yapabilmek icin neye ihtiyac duydugu AYRI bir maddedir"

Bu iki dersi okudugum icin PRC-40'ta T1/T2/T3'u SORDUM.
T2 tam bu dersten cikti: "2 saat kurali HANGI EKRANDA calisir?" -> cevap
"hasta arayuzu yok" -> kural KAGIT USTUNDE kaliyor -> tasarim duzeltildi
(sekreter secimi kaldirildi).

Bakmasaydim: T2'yi sormazdim. Sormasaydim discovery'de "2 saat kurali var"
diye yazili kalirdi, BE onu kodlardi, ve calismayan bir kural uretilirdi.
Somut bedel: bir kural kodlanir ve hic tetiklenmez — kimse fark etmez.

⚠️ AYRICA: MODUL-BILGI.md'leri ACMADIM ve bunu bu olcum sirasinda fark ettim.
Kanona gore "neden boyle" kararlarinin evi ORASI. PRC-26/PRC-33'un MODUL-BILGI
dosyalarinda benim gormedigim kararlar olabilirdi. Bugun sansliydim —
discovery'ler zengindi. Kural olsaydi MODUL-BILGI de listede olurdu ve
atlamazdim.

═══ FABRIKAYA GIDECEK BULGU (benim onerim degil, tespit) ═══

EKSIK: "gereksinim gelince ilgili modulun docs gecmisini oku" kanonda
KURAL olarak yok — yalniz akis adimi.
ETKISI: atlanabilir ve atlandigi FARK EDILMEZ. Discovery yine dolu gorunur;
eksik olan sey GECMISTEKI DERS'tir ve o gorunmez.
BUGUNKU KANIT: baktim ve iki ders buldum, o dersler bir tasarim hatasini
yakaladi (T2). Bakmayan bir PA ayni discovery'yi "tam" diye kapatirdi.

Karar fabrikanin. Ben tespit ediyorum.
