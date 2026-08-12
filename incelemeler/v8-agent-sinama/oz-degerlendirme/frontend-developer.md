# frontend-developer | 2026-08-13 01:01:20

IKINCI TUR — KANON DEGERLENDIRMESI (frontend-developer)
Hepsi bugun CARPTIGIM yerlerden; teorik tarama yok.

═══ 1) AGENT BODY ═══

[1a] EKSIK — "raporla" var, "nereye" yok.
  Body: "Sistemik bug'da kok neden teshisi yapmaz, YAPILANDIRILMIS RAPORLA PA'ya
  yonlendirirsin" (satir 34 + 78). Bugun T3'te tam bunu yaptim (text-error, 4
  tuketici) ve raporun kalici evi olmadigi icin kanalda kaldi.
  ONERI (cumle): "Yapilandirilmis rapor ekrana basilir ve PA'ya BILGI blogu ile
  gider; dosya olarak yazilmaz (`HANDOFF-SCREEN-ONLY`). Kalici kayit gerekiyorsa
  yeri `{modul}/MODUL-BILGI.md` — acmasi PA'nin isi."

[1b] BULANIK — "senior karari sende" ile "direktif alma" siniri.
  Body "component/hook/state/isimlendirme karari SENIN" diyor. Ama QA revize
  verdiginde nereye kadar tartisabilecegim yazili degil. Bugun sinanmadi
  (T5'te de "olculmedi" diye isaretledim) ama gercek iste carpar.
  ONERI: "QA bulgusu KANIT ile gelir; katilmiyorsan olcup karsi kanit sunarsin —
  savunma degil olcum. Ikinci turda hukum QA'nin."

[1c] FAZLA — bulamadim. Body'de tetiklenmeyen satir gormedim.

═══ 2) OMURGA SKILI ═══

[2a] KURAL YANLIS YERDE — "Operatif cekirdek" blogu (12 kural ozeti).
  Blok kendi uyarisini tasiyor ("CACHE'tir, skili acmak yine ZORUNLU") ve BEN
  YINE ATLADIM: `style` acmadan stil hukmu verdim (T3). Uyari metni calismiyor.
  ONERI: ozete kuralin HUKMUNU yazma, yalniz ADINI + "govde: {skil}" yaz.
  Cevabi goren skili acmiyor; adresi goren aciyor.

[2b] ALET CANTASI — eksik bulmadim. Bugunku islerin hepsinin adresi vardi
  (realtime dahil, satir 23). Denetim isi yoktu ama o zaten FE'nin rolu degil.

[2c] GEREKCESIZ KURAL — bulamadim. Aksine `FE-MOTION-DOM-PIN` gerekcesi en iyi
  yazilmis kurallardan (deploy neden kiriliyor, kok cozum vs telafi ayrimi).

═══ 3) REFERENCE DOSYALARI ═══

[3a] BUGUN ACMAM GEREKEN AMA ACMADIGIM: `data-access/references/mekanik.md`.
  T3'te QUERY_KEYS cakisma/naming hukmu verdim; o reference'ta "mevcut QUERY_KEYS
  cakisma borcu" yaziyormus (govde atif veriyor). Acsaydim goat'taki 24 SCREAMING
  anahtarin bilinen bir borc mu yoksa yeni sapma mi oldugunu bilirdim.

[3b] GOVDEYE CIKMALI: `behavior/references/git-komut-detay.md` icindeki pre-commit
  maddeleri. Bugun paylasilan agacta calistik ve `git add .` yasagi KANALDAN geldi,
  kanondan degil. Reference acilmazsa bu kural yok sayilir — ve bedeli baskasinin
  isini commit'lemek.
  ONERI: pre-commit uc madde omurga/govde seviyesine cikarilsin.

═══ 4) CELISKILER — "DAL YOK" SINIFI ═══

[4a] (T4'te K2 olarak raporlandi, tekrar yazmiyorum: arac yoksa dali.)

[4b] YENI — `FE-CMP-SHARED-BOUNDARY` dalsiz.
  Kural: cok-tuketicili shared component'e prop EKLEME, wrapper ile sar.
  Dal yok: ya ihtiyac wrapper ile KARSILANAMIYORSA? (or. component'in ic
  render mantigini degistirmek gerekiyor — sarmalayarak cozulmez).
  ONERI: "Wrapper yetmiyorsa DUR: etki yuzeyini olc (LSP), bulguyu PA'ya BILGI
  olarak tasi, kapsam karari onun. Kendi basina shared component'i degistirme."

[4c] YENI — `FE-ENUM-CROSS` coklu panelde dalsiz.
  Kural: "coklu panel kopyasi SENKRON tutulur." Dal yok: senkronlayacagim ikinci
  panel BENIM ISIM DEGILSE? (baska developer'da acik is olabilir, ezerim).
  ONERI: "Diger panelde ayni enum'a dokunulmus mu `git log` ile bak; acik is varsa
  senkronu kendin yapma, PA'ya bildir."

BULAMADIM DEDIKLERIM: 1c · 2b · 2c. Uydurmadim.
SINIRIM: bugun 9 skil actim (76'nin ~%12'si). Acmadigim skillerde celiski
olabilir — "yok" demiyorum, BAKMADIM diyorum.
