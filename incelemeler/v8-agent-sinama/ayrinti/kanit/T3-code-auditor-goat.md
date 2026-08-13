# T3 CA — Goat etki analizi | 2026-08-12 21:45:54

ANALIZ — goat / commit 680109a0 (menu sahiplik kurali + ayrac zorunlulugu)
Tetik: Clara (T2 sinama). Cikti PA'ya girdidir (CA-OUTPUT-TO-PA).
Yazar kontrolu: commit yazari mert@pryazilim.com -> AGENT cikti. Emsal olarak
supheyle bakilir (oy-envanteri: dongusel referans riski). Kanonu bu commit'ten
DEGIL skilden okudum.

OLCUM DOKUMU (kac dosya / kac cagri)
· Taranan panel/uygulama: 34 (src/ altinda) — 4'u web paneli
· Menu.tsx dosyasi: 3 (commit 3'une de dokundu)
· isUnderPath TANIM: 3 · KULLANIM: 14
· pathname/path.startsWith tum noktalar: 2 (commit disi)
· pathname === tam esitlik: 9
· menuItems export: 1 · tuketici: 2 (PermissionWrapper + useSubmenuPosition)
· Etkilenen dosya satir toplami: 2005
· Grep saglik testi yapildi: bilinen-var desen (usePathname) 44 dosya -> grep calisiyor
  (iki kez sessiz-sifir yakaladim: zsh glob + coklu-dosya degiskeni; ikisini de duzelttim)

═══ (A) ETKI HARITASI ═══

KANCA NOKTASI (isim degil veri akisi): "pathname ile bir menu yolunun
karsilastirilmasi" — bu davranisin SET edildigi ve OKUNDUGU tum noktalar.

DOGRUDAN ETKI — 3 panel, hepsi commit kapsaminda:
· web-admin-v2/…/Menu.tsx (860 satir) — isActive
· web-sponsor-v2/…/Menu.tsx (661) — isItemActive
· web-streamer/…/Menu.tsx (431) — isItemActive
Uc panelde de sahiplik blogu (baskaGrupSahipleniyor) 2'ser gecis: ozdes uygulama.

ETKI YUZEYINDE AMA COMMIT'IN DOKUNMADIGI IKI NOKTA (asil bulgu):

[1] web-sponsor-v2/lib/contexts/PermissionWrapper.tsx:23
    getPermissionForPath -> `item.path.startsWith(pathname)`
    Zincir KAPALI ve olculdu: Menu.tsx menuItems'i EXPORT eder (tek export) ->
    PermissionWrapper tek tuketicidir -> dondurdugu permission izin kararini besler
    (satir 40-47: requiredPermission -> user.PermissionList.includes).
    Iki ozellik: (a) argumanlar TERS — commit'teki tum karsilastirmalar
    isUnderPath(pathname, basePath) yonunde; burada item.path.startsWith(pathname).
    (b) ayrac YOK.
    Yani commit'in DUZELTTIGI veri yapisini (menuItems) tuketen bir nokta, ayni
    yol-karsilastirma sinifinda ve duzeltmenin disinda kaldi.
    Sonucu menu vurgusu DEGIL, izin kapisidir.

[2] web-site/middleware.ts:15
    `PRIVATE_ROUTES.some(route => nextUrl.pathname.startsWith(route))` — ayracsiz.
    web-site, commit'in hic dokunmadigi 4. panel.
    Sonucu login yonlendirmesidir (satir 23-25).

DOKUNMA SINIRI (neye dokunulmamali):
· Sahiplik kuralinin "acikca listelenmemis sayfa ust grubu yakar" istisnasi —
  commit mesajinda ilk tasarimin GERI ALINDIGI yaziyor (detay/ekle sayfalarinda
  menu tamamen sonuyormus). Bu istisna daraltilirsa ayni gerileme geri gelir.
· menuItems'in export'u: gorunuste ic veri, fiilen izin katmaninin girdisi.
  Menu siralamasi/gruplamasi degistirilirse PermissionWrapper'in dondurdugu
  permission da degisir — ilk eslesen item'i doner, siraya duyarli.
· useSubmenuPosition (3 panel) menuItems tuketir ama yol karsilastirmasi YAPMAZ
  (olculdu: 3 dosyada 0 eslesme) -> etki disinda.

YUKARI YON / REUSE (CA-TWO-WAY):
· isUnderPath uc panelde 3 kez KOPYA olarak tanimli, govdeleri mantiksal ozdes.
  Repoda paylasilan web katmani ARANDI: paneller ayri Next uygulamalari, ortak
  lib yok -> bugunku yapida kopya kacinilmaz gorunuyor. Bu bir bulgu degil,
  PA'nin bilmesi gereken bir kisit.
· PermissionWrapper icin sifirdan bir yol-karsilastirici YAZILMASINA gerek yok:
  ayni dosyanin ustunde ayni sinifin uygulamasi zaten var. (Kullanilmasini
  DAYATMIYORUM — varligini bildiriyorum; secim developer'in.)

═══ (B) STANDART / DRIFT ═══

DRIFT-1 (kanit kuvveti: KESIN, envanter) — ayrac zorunlulugu 3 panelde uygulandi,
2 noktada uygulanmadi. Commit mesajinin kendi gerekcesi ("bugun cakisan yol yoktu
ama benzer iki adres eklenince sessizce ayni bug cikardi") bu iki nokta icin de
gecerli; commit o mantigi menude uygulayip ayni repodaki iki yol-karsilastirmasina
tasimamis. REFERANS: commit'in kendi kurali.

DRIFT-2 (KESIN) — CQ-NO-MAGIC sapmasi, web-admin-v2/Menu.tsx:507.
Yeni yazilan isUnderPath'te ciplak "/" kullanilmis; kardes iki panel ayni satirda
rota sabiti kullaniyor (APP_ROUTES.HOME / Y.HOME). Admin paneli APP_ROUTES'u ZATEN
import ediyor ve ayni dosyada kullaniyor (satir 7, 57, 66) — ve APP_ROUTES.HOME
degeri "/" (dogrulandi: route.ts:7). Yani deger ozdes, DAVRANIS FARKI YOK; saf
kanon sapmasi + kendi dosyasindaki desenden sapma.

POZITIF NOTLAR (kanon geregi pozitif de yazilir):
· Yorumlar NEDEN'i anlatiyor, ne yaptigini degil -> CQ-COMMENT-WHY uyumlu.
  Ticket numarasi govdeye gomulmemis (PRY-17447 commit mesajinda, kodda degil).
· Sahiplik kurali uc panelde ozdes uygulanmis — tek-tarafli degisim yapilmamis.
· Commit mesajinda GERI ALINAN ilk tasarim ve sebebi yazili; bu, sonraki okuyucuyu
  ayni asiri-duzeltmeden korur.
· sponsor/streamer'da alt oge kontrolu === iken ayracli hale gelmis; commit bunu
  "iyilesme, grup davranisi degismiyor" diye isaretlemis — ben de grup dalinin
  ayri kod yolu oldugunu dogruladim (submenu dali once donuyor).

═══ (C) ALTYAPI ETKISI ═══
YOK. Degisiklik uc frontend dosyasinda, yalniz istemci-tarafi yol karsilastirmasi.
Yeni secret/env/ingress/queue/servis gerekmiyor -> DO'ya is dusmuyor.
(middleware.ts bulgusu Next.js runtime'inda calisir ama mevcut dosya; bu commit
altyapi yuzeyine dokunmuyor.)

═══ STATIK SERH (CA-IMPACT-STATIC-SHERH) ═══
Bu cikti STATIK okumaya dayanir. Uc kuvvet ayrimi:
· ENVANTER (kesin): kac dosya, kac tanim, kac kullanim, hangi satir — grep ile sayildi.
· ZINCIR (kesin): menuItems -> PermissionWrapper -> izin karari; export/import
  olcumuyle kapali.
· DAVRANIS (OLCULMEDI): "bu iki nokta bugun istismar edilebilir mi" sorusunu
  CEVAPLAMIYORUM. web-site'ta bugun /hesabim ile cakisan bir rota YOK (route.ts
  tarandi) — yani bugun somut bir acik GORMEDIM. Bulgunun kuvveti "bugun acik var"
  degil, "ayni bug sinifi, ayni repoda, duzeltmenin disinda". Kirilma garantisi
  degildir; kosturarak dogrulamak TE'nin isidir (CA-STATIC-NO-REPRO).
· LSP KULLANILMADI: TS icin findReferences birincil arac (CODE-COUNT-BY-LSP) ama
  bu oturumda LSP araci elimde yok. Grep ile calistim ve saglik testi yaptim
  (bilinen-var desen 44 dosya dondu). Tuketici sayilari DUSUK ve dosya adlariyla
  capraz dogrulandi (menuItems tek export, tek import) — ama teyitsiz sifir kanit
  degildir; sayiya dayali bir karar verilecekse LSP ile teyit onerilir.

SINIRLARIM: kod yazmadim, dosya degistirmedim (yalniz okudum), direktif vermedim,
repro yapmadim. Bulgularin NASIL duzeltilecegi developer'in karari.

BEKLEDIGIM: Karar PA'da/sizde — bu iki nokta kapsama alinacak mi, ayri is mi.
