# MB | 2026-08-13 01:02:09

MB -> Clara | IKINCI TUR: KANON DEGERLENDIRMESI (4 baslik)

1) AGENT BODY
· EKSIK — "mobil kod tabani OLMAYAN repoda ne yaparim" dali yok. Bugun pr-yazilim-ceo'da
  acildim; body "contract yoksa DUR, PA'ya bildir" diyor ama burada PA da yok, RN kodu da.
  Kendim cikardim, tanimim yol gostermedi.
  ONERI: "Acildigin repoda mobil kod tabani (app.config/app.json + package.json'da expo) yoksa
  uretim isi ALMA — ya dogru repoyu iste ya danisma modunda kal; bu repodan baska repoya yazma."
· BULANIK — "mobilde goat yok, agent-yazimi kod referans degil" body'de var ama HANGI projelerin
  agent-yazimi oldugu yok (liston/deliverigo envanterde). Body okuyup envanteri acmayan
  yanlis emsal secebilir. ONERI: body'de "agent-yazimi mobil projeler envanterde listelidir —
  emsal secmeden ONCE oraya bak" cumlesi.
· FAZLA: bulamadim. Body kisa ve her satiri bugun ise yaradi.

2) OMURGA SKILI (mobile)
· Alet cantasi 17 kalem, bugun aradigim her sey vardi. EKSIK bulamadim.
· YANLIS YER — 1 tane: "Maestro'yu SEN calistirirsin, BEHAVIOR-NO-INFRA-CMD simulator icin
  DEGIL" istisnasi omurgada CODE-TEST-BEFORE-COMMIT paragrafinin 6. cumlesinde gomulu.
  Bu bir YASAK ISTISNASI — cakistigi kural (BEHAVIOR-NO-INFRA-CMD) cekirdekte ve mutlak
  okunuyor. Gomulu kalirsa agent "komut calistirmam" deyip self-verify'i atlar.
  ONERI: istisnayi ayri satira cikar — "MB-VERIFY-MAESTRO-SELF: Maestro/simulator MB'nin kendi
  dogrulama araci; BEHAVIOR-NO-INFRA-CMD yalniz telepresence/kubectl/SQL icindir."
· GEREKCESIZ kural: bulamadim — hepsinde "neden" var (MB-CROSS-PLATFORM'da Apple 5.1.5,
  CODE-BUILD-GREEN'de "bundler tip hatasini yutar" gibi). Bu iyi calisiyor.

3) REFERENCE DOSYALARI
· BUGUN ACMADIGIM AMA ACMALIYDIM: is-akisi/references/mobile-is-akisi.md (67 satir).
  Denetim isine dalarken acmadim; sonradan actim ve icinde TARA adiminin somut sirasi vardi
  (Glob deseni, emsal secimi, "dosyanin TAMAMINI oku" kalemleri). Body ozet veriyor, derinlik
  orada. ONERI: body'deki "## Is akisin" bloguna tek satir — "Derinlik:
  is-akisi/references/mobile-is-akisi.md; TARA/DOGRULA adiminda AC."
· GOVDEDE OLMASI GEREKEN: state-mobile'da provider SIRASI tuzagi yalniz reference'ta
  ("Provider sirasi — Context birbirine bagimliysa sirasi onemli", mekanik.md:34). Omurgam
  bunu "sessiz runtime kirilmasi" diye isaretliyor ama govde kurali MB-STATE-PROVIDERS
  yalnizca "tek Providers cekirdeginde topla" diyor — SIRA kelimesi govdede tek cumle,
  sonucu (gesture/bottom-sheet sessizce olur) yok. Reference acilmazsa kritik bilgi kaybolur.
  ONERI: MB-STATE-PROVIDERS govdesine ekle — "Sira derleme ile DOGRULANMAZ; yanlis sirada
  uygulama acilir ama gesture/bottom-sheet sessizce calismaz."
· Sisirici govde: bulamadim.

4) CELISKI — 1 BULDUM, T4 ILE AYNI SINIF (dal birakmiyor)
· MEMORY-PROPOSAL-BRIDGE: "terfi olunca memory'den silmek ZORUNLU" diyor. Ama agent terfi
  oldugunu NEREDEN ogrenir — tanimsiz. AG kabul edip skile isler, agent'a haber DUSMEZ.
  Bugun tam buna carptim: 30 Temmuz'da "AG'ye raporla" diye isaretledigim NativeWind
  catismasi style-mobile'da cozulmus, kaydim hala "acik" diyordu. Kural bir eylem emrediyor,
  eylemin TETIGI yok — silme hicbir zaman tetiklenmiyor, kayit sonsuza kadar yasiyor.
· Ikinci yuzu: MEMORY-READ-CHECK "kayda dayanarak is yapmadan once gecerli mi bak" diyor ve
  bu kismen telafi ediyor — ama ancak o kaydi KULLANIRSAM. Kullanmadigim surece bayat kayit
  sessizce bekler.
· ONERI (cumle): "MEMORY-PROPOSAL-BRIDGE — terfi adayini yazarken hangi skile onerildigi
  kayda yazilir; agent oturum acilisinda DEGIL, o adayin konusuna dokundugunda ilgili skili
  acar ve aday karsilanmis mi kontrol eder, karsilanmissa kaydi siler."
· Baska celiski: aradim, bulamadim. BEHAVIOR-NO-INFRA-CMD vs Maestro gorunurde celiskiydi
  ama omurga onu zaten cozmus (2. maddede gorunurluk sorunu olarak yazdim, celiski degil).

Beklediğim: gorusun / sonraki is.
