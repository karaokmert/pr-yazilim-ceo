# FE | 2026-08-13 00:56:36

MEMORY DENETIMI — RAPOR (frontend-developer)
`memory-management` skili acildi (govde + kanon eslemesi yapildi).

═══ SAYILAR ═══
· Denetlenen kayit: 44 dosya + index (45 dosya toplam)
· Index: 49 -> 50 satir (1 satir buyudu; 200 sinirinin cok altinda, arsiv gerekmiyor)
· Celiski bulundu: 2 (ikisi de DUZELTILDI)
· Yeni kayit: 1 · Var olana eklenen: 2 · Isaretlenen (silinmedi): 1
· Yetim dosya: 0 · Kirik pointer: 0 (comm ile iki yonlu dogrulandi)

═══ 1) CELISKI — EN KRITIK BULGU ═══
Iki kayit BIRLESINCE kanonun bir adimini siliyordu. Tek tek bakinca masum,
yan yana koyunca kural kayboluyor:

[C1] tercih_test-gercek-numara-ve-playwright.md
  Kayit diyordu: "Commit oncesi Playwright testi ZORUNLU."
  Kanon diyor  : CODE-TEST-BEFORE-COMMIT — "'test edeyim mi, sen mi edeceksin?'
                 SORULUR" (secenek KULLANICIDA).
  Ihlal: kayit soruyu kaldirip "her zaman ben kostururum"a cevirmis.
  YAPTIM: kayit duzeltildi — tercih korundu ("Mert'in bilinen cevabi: sen kostur")
  ama kanonun soru adimi geri konuldu + BEHAVIOR-PREF-UNDER-CANON atfi eklendi.
  Ayrica "ARAC YOKSA" dali yazildi (bugun fiilen carptigim bosluk).

[C2] tercih_mert-calisma-tarzi.md §1
  Kayit diyordu: "Dogrulamayi 'yapayim mi?' diye SORMA."
  Ihlal: C1 ile birleşince kanonun soru adimini tamamen orturuyordu.
  YAPTIM: IKI SORU AYRISTIRILDI —
    · "Dogrulama YAPILSIN mi?" -> SORULMAZ (Mert'in kurali, kanonla uyumlu)
    · "Testi KIM kostursun?"   -> SORULUR (kanonun istedigi)
  Mert'in tercihi bozulmadi, kanonun kapisi geri acildi.

⚠️ Bu tam da kanonun uyardigi mekanizma: "skil'le celisen ciplak kayit skil'i EZER."
Bugun T2'de Playwright yasaklandiginda bu kayit beni kilitleyebilirdi — kayit
"zorunlu" diyordu, arac yoktu, cikis yolu yaziliydi degildi.

═══ 2) YENI KAYIT (1 tane, bilincli olarak TEK) ═══
refleks_commit-oncesi-kapilar.md — "her iste gecerli, atlanirsa is bozulur" kapilari.
Ictekiler POINTER (kural govdesi kopyalanmadi, MEMORY-POINTER-ONLY):
  build yesil (+exit kodu tuzagi) · motion-dom caret pin (DEPLOY-KIRAN, hic
  tetiklenmemisti) · test sorusu · kanon oz-denetimi · yalniz kod commit +
  paylasilan agac disiplini · BRIEF->BEKLE->COMMIT->HANDOFF sirasi ·
  contract kilidi · alan degisince skil ac · emsal yazar kontrolu.
NEDEN TEK DOSYA: bunlari ayri ayri acsaydim index 8-9 satir sisecekti. Senin
uyarina uydum — dagitmak yerine tek adreste topladim, index'e 1 satir girdi.

═══ 3) VAR OLANA EKLENEN (2 tane — yeni dosya ACMADIM) ═══
Once "var olan bir kayda eklenebilir mi" diye sordum, ikisinde de cevap EVET'ti:
· hata_yokluk-iddiasi-etiketten-kurulmaz.md -> bugunku dersim eklendi:
  "yok" KANITI ile "sonuc su olur" CIKARIMI ayri yazilir. (T3'te text-error icin
  "renksiz basiyor" dedim, olctugum sey "degisken yok"tu — tarayicida gormedim.)
· kazanim_skil-taramasi-dosyadan-degil-alet-cantasindan.md -> eklendi:
  omurgadaki OZET blok skil acma refleksini kapatiyor; uyari metni yetmiyor.
  Tetik "kurali biliyor muyum" degil, "bu alana dokundum mu" olmali.

═══ 4) ISARETLEDIM AMA SILMEDIM (senin kararin) ═══
kapanis-notu.md (goat, 2026-08-11) BAYAT gorunuyor. Olctum:
notun "yarin ilk hareket" dedigi dort kalem goat'ta commit'lenmis —
d4cfbd0c (promosyon bes alan + hafta gunu secici + engelli renk) ve
ea6d2b55 (tarih secici + prototip/olu prop). Yani beklenen is gelmis ve yapilmis.
SILMEDIM cunku kanon (KAPANIS-DEVRAL-TEMIZLE) notu DEVRALAN oturumun temizlemesini
soyluyor — ben devralmadim, denetliyorum. Kapanis indeksine ⚠️ isaret dustum.
Halen acik gorunen iki sey var: test borcu 7 kalem (veri/ortam bekliyor) ve
RedirectUrl bos-adres celiskisi.

═══ TEMIZ CIKANLAR ═══
· Index SAF pointer — icerik tasimiyor, hicbir satir kural govdesi degil. Dogru.
· Kural kodu gecen 10 kaydin hepsi ATIF duzeyinde (govde kopyasi yok).
· Katman suzgeci: proje bilgisi (goat/osinif/egelisaglik haritalari) memory'de
  mesru duruyor — bunlar kodda olmayan "hangi panel neyi tasiyor" haritasi.
· Bugun goat'ta olctugum bulgular memory'ye PROJE KAYDI olarak yazilmadi:
  memory'm user-scope (tum projeler), tek projenin denetim bulgusu oraya ait degil.
  Yalniz genellenebilir DERS yazildi (madde 3).

═══ SANA SORULARIM (2) ═══
1. kapanis-notu.md'yi SILEYIM mi? Bayat oldugu olculdu ama devralma yetkisi
   bende degil. "Sil" dersen temizler, kalici bilgisini once tasirim.
2. C1/C2 celiskileri bir KANON BOSLUGUNU da acti: "dogrulama araci yoksa ne olur"
   dali uc ayri kuralda tanimsiz (T4'te K2 diye raporlanmisti). Memory'me gecici
   cozumu yazdim ama bu AG'ye gitmeli — sen mi tasiyacaksin, ben bir sapma notu
   mu hazirlayayim?

BEKLEDIGIM: iki sorunun cevabi. Sonrakine gecebilirsin, bende is kalmadi.
