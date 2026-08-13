# QA | 2026-08-13 00:58:42

MEMORY DENETIMI RAPORU — qa-engineer

═══ SAYILAR ═══
Denetlenen kayit : 54 dosya + 1 index (satir satir tarandi)
Bulunan celiski  : 1 gercek (duzeltildi) + 2 yapisal tutarsizlik (duzeltildi)
Yeni kayit       : 1 acildi · 1 VAR OLANA eklendi (yeni acmadim)
Index            : 63 satir -> 63 satir (1 eklendi, 1 kaldirildi) · 12.075 bayt
                   (25KB sinirinin YARISINDA, 200 satir sinirinin cok altinda)
Yetim/olu pointer: 0 (kapanis indeksi dahil dogrulandi)

═══ 1) KANONLA CELISEN KAYIT — 1 BULDUM, DUZELTTIM ═══
Dosya: feedback_be_onayi_push_bekletme.md
Kayit diyordu: "Push edeyim mi diye ayri onay BEKLEMEM. Kullanici acikca
  'bekle' demedikce ONAY = PUSH."
Kanon diyor (REL-QA-NO-PUSH-ALONE): "Denetim GECTI ≠ push. Kullanici 'tamam'
  + diff onayi verince push eder. Onaysiz push, denetimden gecmis kod olsa
  bile YASAK." + REL-APPROVAL-USER-ONLY.
>> Bu TAM OLARAK kanonun uyardigi sinif: ciplak kayit skili EZER. Bayraksizdi.
Sonraki oturumda bunu okuyup onaysiz push atabilirdim — bugun T2'de
reddettigim seyin ta kendisi, kendi memory'mden gelseydi.

NASIL COZDUM (silmedim): Kullanicinin 2026-08-04 uyarisi KAPSAM hakkindaydi
("BE'yi FE bitene kadar bekletme"), KAPI hakkinda degil. Ikisi celismiyor.
Kaydi ona gore duzelttim + neden duzeltildigini ve kanon alintisini icine
yazdim. Kardes kayit (qa_push_kapisi_be_yeterli) bu ayrimi zaten dogru
yapmisti: "push'un TETIGI hala kullanicida" — yani celiski tek kayittaydi.

═══ 2) YAPISAL TUTARSIZLIK — 2 ═══
a) MEMORY.md'ye kapanis notu DOGRUDAN yazilmisti (goat 2026-08-12).
   KAPANIS-INDEX-POINTER bunu ismen yasakliyor: uc kademe olmali
   (MEMORY.md -> kapanis indeksi -> not). Indexe yazilan devir notu pasif
   kayit degil, sonraki oturumun davranis talimati olur.
   -> MEMORY.md'den kaldirdim, kapanis indeksine tasidim.
b) Index "su an IKI acik" diyordu, kapanis indeksinde UC not vardi (+1'i
   MEMORY.md'de) = fiilen DORT. Bayat sayi.
   -> "DORT acik (goat x2 · liston · osinif)" olarak duzelttim + kapanis
   indeksindeki bicim tutarsizligini (bir satir farkli formatta) tekillestirdim.

⚠️ ILK OLCUMUM YANLISTI, DUZELTTIM: uc kapanis dosyasini "YETIM" diye
tespit etmistim — cunku yalniz MEMORY.md'de aradim. Kanon UC KADEME
ongoruyor; dosyalar kapanis indeksinden bagliydi. Yanlis kapsamda olcum.
Kendi kuralimi kendime uyguladim (bugun ucuncu kez): "EKSIK cikan olcum
once KENDI komutundan supelenir."

═══ 3) HER ISTE LAZIM OLAN KURAL — 1 YENI KAYIT ═══
qa_is_basi_skil_acma_refleksi.md
Icerik: is turu belli olunca O ISIN skilini FIILEN ac; omurga (quality)
yuklu olmak alt skili acmis SAYMAZ. Is->skil eslemesi + "tetik alan
degisimi, tur basi degil" uyarisi.
Neden bu: bugun T1'de kendi olctugum ariza — en sik yaptigim is COMMIT
INCELEME ve `commit-review` oturum acilisinda elimde DEGILDI. Gercek
denetim gelince once onu actim, ama "hazirim" hissiyle baslasaydim akisi
hafizadan uygulardim. Olcut senin verdigin: "atlarsam is bozulur mu" -> EVET.
⚠️ Kural GOVDESINI kopyalamadim (MEMORY-POINTER-ONLY) — pointer + eslemeler.

═══ 4) GOZDEN KACABILECEK — VAR OLANA EKLEDIM, YENI ACMADIM ═══
qa_kazanim_kendi_olcum_komutumu_dogrula.md icine iki madde:
· KAYNAK-TUREV (kayit anlaminda): bir belgeyi kanit diye acarken "bu ASIL
  kayit mi, okunabilirlik icin uretilmis KOPYA mi". Bugunku PRC-45 vakasi
  kanit olarak icine yazildi — uc taraf da dogru olctu, farkli dosyaya
  bakiyordu. CR-VERIFY-SOURCE "adresi ac" dedirtiyor ama "actigim ASIL mi"
  sordurmuyor; kural yariya kadar goturuyor.
· BIRIM KONTROLU: sayiya dayanan bulguda karakter/bayt karismasin. Bu
  denetimde bizzat carptim — `awk length` Turkce metinde BAYT sayiyor,
  214 bayt ≈ 190 karakter. Yanlis birimle 50 satiri "ihlal" diye
  raporlayacaktim, python ile karakter olarak yeniden olctum.
Neden yeni kayit ACMADIM: ayni aile (olcum guvenilirligi), var olan kayit
zaten "kaynak mi turev mi" ifadesini kullaniyordu — dosya anlaminda. Index
sismesin diye oraya bagladim.

═══ SANA SORUM — 1 KALEM, KARAR SENIN/MERT'IN ═══
Index'teki 51 pointer'in 50'si 150 KARAKTER sinirini asiyor (ortalama 214,
max 276). MEMORY-INDEX-ONLY "her kayit TEK satir (≤150 kar)" diyor.
DUZELTMEDIM ve sebebini yaziyorum:
· Kuralin AMACI index'i 200 satir / 25KB sinirinda tutmak. Benim index'im
  63 satir / 12KB — sinirin YARISINDA. Amac karsilaniyor.
· 50 satiri 150'ye kirpmak, her satirdaki "kanca" bilgisini (hangi projede,
  hangi tuzak) kesmek demek — index'in ise yarayan tarafi tam da o.
· Yani: kuralin HARFI ihlal, AMACI saglam. Kendi olcutumle "RED etmezsem
  bedeli var mi" -> yok.
Kendi memory'mde kural esnetme kararini TEK BASIMA vermek dogru olmaz.
Iki secenek: (a) boyle kalsin, kural amac-bazli okunsun · (b) kirpayim,
harfe uyayim. Senin/Mert'in karari.

EMIN OLMADIGIM BASKA SEY YOK. Silme yapmadim (hicbir kayit silinmedi);
duzeltmelerin hepsi gerekcesiyle birlikte kaydin ICINE yazildi.

BEKLEDIGIM: index satir-uzunlugu karari (a/b). Sonraki agent'a gecebilirsin.
