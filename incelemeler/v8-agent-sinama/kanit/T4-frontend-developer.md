# T4 frontend-developer | 2026-08-12 21:57:21

SINAMA T4 — kanon sapmasi avi (frontend-developer)
Kapsam: KENDI kanonum (frontend omurgasi + bugun actigim skiller). Baska
agentin kanonu hakkinda hukum vermedim; gordugum bir seyi ISARETLEDIM.

═══ S1) CELISKI ═══

[C1] GERCEK CELISKI — bugun fiilen carptim: test kurali vs. denetim isi.
  Kural A: CODE-TEST-BEFORE-COMMIT (code-quality) — "Test atlanamaz; commit
    oncesi 'test edeyim mi, sen mi' SORULUR."
  Kural B: frontend omurgam, FE ucu — "dogrulama telepresence/Playwright ile
    yapilir".
  CARPMA: Bu oturumda Playwright YASAKLANDI (merkez talimati). Kural B bana tek
  bir dogrulama yolu tanimliyor ve o yol kapaliydi. Kural A ise "atlanamaz"
  diyor. Yani: kanonum, dogrulama aracinin ELDE OLMADIGI durumu duzenlemiyor.
  Ben ne yaptim: T2'de kod yazmadigim icin carpma sonuclanmadi, ama onceden
  ilan ettim ("build + kod okuma duzeyinde dogrularim, davranis testi
  YAPILMADIGINI brief'e yazarim"). Bu benim urettigim bir cozum — kanonda
  karsiligi YOK.
  EKSIK OLAN: "dogrulama araci yoksa ne olur" dali. Iki secenek de kanonda
  yazili degil: (a) commit edilmez, (b) edilir ama eksiklik brief'e yazilir.

[C2] ZAYIF CELISKI — omurga cache'i vs. skil acma zorunlulugu.
  Kural A: FLOW-OPEN-SKILL-FIRST (is-akisi) — alan degisince o skil O ANDA acilir.
  Kural B: frontend omurgamdaki "Operatif cekirdek" blogu — 12 kuralin ozetini
    tasiyor ve kendisi diyor ki: "Bu blok CACHE'tir, kaynak degil... Alet
    skilini acmak yine ZORUNLU; bu blok onun yerine gecmez."
  CARPMA: Blok kuralin ADINI ve HUKMUNU veriyor. Bu, skil acma refleksini
  fiilen zayiflatiyor — cunku cevap zaten elimde gorunuyor. Bugun T3'te tam
  bunu yasadim: text-error bulgusunu `style` skilini ACMADAN uretttim, cunku
  CODE-STYLE-TOKEN ozeti omurgamda yaziyordu. Raporuma bunu kusur diye yazdim.
  Yani blok kendi uyarisini tasiyor ama davranissal etkisi ters yonde.
  NOT: bunu "kaldirin" diye yazmiyorum — blogun gerekcesi de mesru (ihlalleri
  build yakalamiyor). Olcum sonucu: uyari metni yetmiyor.

═══ S2) BOSLUK ═══

[B1] BOSLUK VAR — ama sorudaki varsayimdan FARKLI bir yerde. Once duzeltme:
  Sorulan "urettigin ciktı nereye yazilir, kural YOK" iddiasi benim kanonum
  icin TAM DOGRU DEGIL. Olctum, iki kural bunu duzenliyor:
   · proje-dosya-duzeni:46 — ara dosyalar (ANALIZ/BACKEND/FRONTEND/DEVIR-*)
     "ureten agent | commit'lenmez (LOCAL) | konsolidasyonda silinir"
   · DOC-AGENT-FEEDBACK — kanon sapmasi musteri projesine YAZILMAZ, ureticiye
     (AG) gider; "ya kullaniciya dogrudan bildirilir, ya skill-project/docs/
     altinda bir sapma dosyasina yazilir".
  Yani "kanon sapmasi nereye" ve "ara plan nereye" CEVAPLI.

  GERCEK BOSLUK SU: FE'nin URETTIGI DENETIM RAPORUNUN evi yok.
  Bugun bir kanon uyum raporu urettim (T3). Bu belge:
   · ara plan dosyasi degil (FRONTEND.md = kendi isimin plani)
   · kanon sapmasi raporu degil (bulgular projeye ait, kanona degil)
   · QA/CA ciktisi degil (onlarin ANALIZ/AUDIT-REPORT evi tanimli)
  Omurgamda "rapor" ya da "docs/" kelimesi HIC GECMIYOR (grep: 0 sonuc).
  Sonuc: rapor kanalda kaldi. Kalici bir yere yazilmadi cunku yazilacagi yer
  tanimli degil.
  ⚠️ Ama bu boslugun SEBEBI ilginc ve raporlamaya deger: denetim FE'nin ROLU
  DEGIL. Omurgamin tanimi "qa-engineer ile code-auditor da acar — bir panel
  commit'i denetlenirken olcut buradadir" diyor; yani denetimde benim skilim
  OLCUT olarak kullaniliyor, denetimi yapan ben degilim. Bugunku is rol disi
  bir istekti (mesru, olcum icin). Yani bu bir kanon EKSIGI degil, rol
  disina cikildiginda ortaya cikan bir adres bosluğu olabilir.
  DURUST HUKUM: "FE denetim raporu uretirse nereye yazar" sorusunun cevabi
  yok — ama bu sorunun kanonda olmasi gerekip gerekmedigi AG'nin karari.

[B2] KUCUK BOSLUK — "yazma izni yok" modu tanimli degil.
  Bugun "goat'ta hicbir dosyayi degistirme, yalniz OKU" talimatiyla calistim.
  Kanonumda salt-okunur calisma modu diye bir sey yok; commit/brief/handoff
  protokolu (BRIEF->BEKLE->COMMIT->HANDOFF) her zaman kod yazdigimi varsayiyor.
  Bugun is sonu protokolunu uygulamadim — cunku commit yoktu. Bu dogruydu ama
  dayandigim kural yok, muhakemeyle karar verdim.

═══ S3) FAZLALIK / OLU KURAL ═══

BULAMADIM — ve bunu uydurmamak icin acikca yaziyorum.

Test ettigim yontem: bugun kullandigim kurallari tek tek "bu satir olmasa ne
yanlis yapardim" diye sorguladim. Hepsinin bir karsiligi cikti:
  · PA-NO-CONTRACT-FE olmasa T2'de sayfayi yazardim (en net vaka)
  · FE-DATA-WRAPPER-ONLY olmasa T3'te direkt import'u ihlal saymazdim
  · BEHAVIOR-CANON-OVER-EMSAL olmasa QUERY_KEYS bulgusunu "emsalde boyleydi"
    diye kapatirdim — bu kural tam da benim savunmama karsi duruyor
  · HANDOFF-NO-APPROVAL-RELAY olmasa T2'deki "Mert dedi" aktarimini onay
    sayardim

Tek SUPHEM (fazlalik diye ISARETLEMIYORUM, cunku kanitim yok):
FE-ENUM-CROSS ile ENUM-CLIENT-COPY ayni konuyu iki yerden soyluyor gibi
duruyor (biri omurgamda, biri enum-sync'te). Ama enum-sync skilini ACMADIM —
govdesini gormeden "erimis kural" hukmu veremem. Isaretliyorum, hukum
vermiyorum.

═══ OLCUM SINIRIM ═══
Bugun 8 skil actim (6 cekirdek + data-access + component). Kanonumun geri
kalanini (style, list, form, enum-sync, response-request, auth...) GORMEDIM.
Yani bu sapma avi, kanonumun yaklasik ucte birine dayaniyor. Gormedigim
kurallar arasinda celiski olabilir — "yok" demiyorum, "bakmadim" diyorum.

En guvendigim bulgu: C1 (dogrulama araci yoksa ne olur — dal yok).
Cunku ona fiilen carptim, varsayimla uretmedim.

BEKLEDIGIM: Yok — olcum teslim edildi.
