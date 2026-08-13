# PA memory denetimi | 2026-08-13 00:50:07

MEMORY DENETIMI TAMAM. Rapor + iki soru.

═══ SAYILAR ═══
Denetlenen : 69 memory dosyasi + index (76 -> 77 satir)
Celiski    : 1 GERCEK (duzeltildi) · 1 SAHTE ALARM (olctum, curudu)
Yeni kayit : 1 dosya · 1 kayda EKLEME yapildi (yeni dosya acmadim)
Index      : 76 -> 77 satir · 12.121 karakter (esik 200 satir / 25KB — RAHAT)

═══ 1) GERCEK CELISKI — DUZELTILDI ═══

`arge_clickup_mcp_eksik.md` icinde `CLICKUP-PA-ONLY-WRITE` kurali aniliyordu.
O kural DUSMUS: kanonda artik yalniz TARIHCE olarak geciyor, yerine
`CLICKUP-OWN-TASK-ONLY` gelmis (her agent kendi task'ina yazar, PA'nin tekeli yok).

Neden tehlikeliydi: kayit "PA'nin ClickUp tekeli var" diyordu. Bugun ben BE'nin
sub task'ina dokunmadim, PRC-45'i kendim cevirdim — dogru davrandim ama KAYIT
bana yanlisini soyluyordu. Kanonun dedigi sey aynen bu: "skille celisen ciplak
kayit skili EZER."

Yaptigim: kural adini cikardim + serh dustum (ne zaman/neden dustugu yazili).
Kaydin GERI KALANI gecerli — ClickUp MCP'sinin ozel-yazilim plugin'inde
OLMADIGINI bugun ben de dogruladim (websitesi plugin'inin araclarini kullandim).
Kayda "2026-08-13'te yeniden dogrulandi" notu dustum.

═══ 2) SAHTE ALARM — OLCTUM, CURUDU (bunu ayri yaziyorum) ═══

Bes dosyada `TASK-STATUS.md` atfi buldum (9 gecis). Kanonda o dosya KALKMIS
gorunuyor — "bayat atif, temizle" diye baslayacaktim.

OLCTUM ONCE: dort projeye de baktim.
  goat 202 satir · egelisaglik 60 · liston 105 · osinif 115 — DORDUNDE DE VAR.

Yani atiflar BAYAT DEGIL, GECERLI. Kanon yeni duzeni tarif ediyor ama gercek
projeler henuz tasinmamis. Silseydim CALISAN yonlendirmeleri yok edecektim.

⚠️ Bunu ayrica yaziyorum cunku bugun ucuncu kez ayni seye carptim: kanonun
dedigi ile sahanın durumu ayri seyler ve hakem SAHA (kod/dosya). "Kanonda yok"
demek "projede yok" demek degil.

═══ 3) HER ISTE LAZIM — VAR OLAN KAYDA EKLEDIM ═══

Yeni dosya ACMADIM (index sismesin dedin). `feedback_preload_okumak_degil.md`
zaten "cikti uretmeden once skili AC" tetik listesi tutuyordu; iki madde ekledim:

· `clickup` skili — ClickUp'a dokunmadan once AC (task okumak != comment okumak)
· ⚠️ DISCOVERY'DE KANONUN EMRETMEDIGI ADIM: gereksinim gelince ILGILI MODULUN
  DOCS GECMISINI oku (komsu discovery + MODUL-BILGI). Mert'in bugun sordugu sey.
  Kaydin icine sunu yazdim: bu bir AKIS ADIMI, KURAL DEGIL — atlanabilir ve
  atlandigi FARK EDILMEZ. Olculmus kazanci da yazdim (komsu discovery'deki iki
  ders -> uc ek soru -> kagit ustunde kalan bir kural yakalandi).

═══ 4) GOZDEN KACAN — 1 YENI DOSYA ═══

`feedback_sure_kaydi_ters_olcum.md` (index pointer: 145 karakter, esik altinda)

Icerigi: sure kaydi IKI YONDEN yaniltiyor —
· duvar saatini olcer (FAZLA sayar): 326 dk kayitli / ~12 dk fiili
· revize turlarini HIC olcmez (EKSIK sayar): 1 dk kayitli / ~17 dk gercek,
  arada IKI tam RED->revize turu
Sonuc TERS: iki kez RED alip duzelten is, ilk turda gecen isten KISA gorunur.
+ kota tuzagi (kalici kayit katmani tamamen kapanabilir -> repoya yaz).

Neden yeni dosya: mevcut hicbir kayda ait degil (statu anlami ile ilgili degil,
olcum kusuru). Ve "her iste lazim" degil — sure kaydi girerken lazim.

═══ SANA IKI SORU ═══

S1) INDEX'TE 57 SATIR 150 KARAKTERI ASIYOR (en uzunu 279).
    Kanon "her kayit TEK satir, <=150 karakter" diyor. Toplam 12.121 karakter,
    yani 25KB esiginden UZAK — islevsel bir sorun YOK, ama kural ihlali VAR.
    Benim bu turda ekledigim satir 145 (kurala uygun).
    57 satiri kisaltmak buyuk bir is ve BUGUNUN isi degil. Dokunmadim.
    Sen ne dersin — birakayim mi, yoksa ayri bir is olarak mi acilsin?

S2) BUDAMA YAPMADIM — emin olamadigim icin.
    69 dosyanin bazilari kapanmis islere ait olabilir (`MEMORY-PRUNE`: is
    kapaninca olu tutanak cikarilir). Ama hangi isin kapandigini bilmiyorum —
    goat/liston/egelisaglik/osinif kayitlari CANLI projeler ve ben o projelerin
    bugunku durumunu gormedim.
    Kanon "emin degilsen SILME, isaretle ve bildir" diyor. Bildiriyorum:
    budama yapilmadi, gerekcesi bu.

Beklediğim: S1 + S2 karari. Baska bir sey istersen yazarim.
