# BILGI SINAVI — frontend-developer | 2026-08-12 23:13:35

BILGI SINAVI — frontend-developer
⚠️ SKILL ACMADAN, hafizamdan yazildi. Acarak dogrulama YAPILMADI.
(Bugun T3'te tam da "hafizadan hukum verme" hatasindan ders cikardim —
bu yuzden emin/tahmin ayrimini agir tutuyorum.)

═══ S1) LISTE SAYFASI — veri cekme + tazeleme ═══
EMINIM:
· Hook: projenin KENDI wrapper'i — `useQuery` (okuma) / `useMutate` (yazma).
  Import @/lib/hooks/... altindan; @tanstack/react-query'den DIREKT import
  YASAK (FE-DATA-WRAPPER-ONLY). Tek istisna wrapper'in kendi dosyasi.
· Cagri ApiService uzerinden (FE-DATA-APISERVICE) — component'te ham fetch yok.
· Query key: QUERY_KEYS sabitinden. Anahtar SCREAMING_SNAKE_CASE, degeri sabit
  string. Parametre string template ile KEY ICINE gomulmez; dizinin AYRI
  elemani olur -> [QUERY_KEYS.X, id]. (`user-${id}` YASAK.)
· Tazeleme: useMutate'e mutationKey verilir; basaridan sonra wrapper
  invalidateQueries ile ilgili key'i tazeler. Elle setState ile sunucu-state
  senkronu YASAK (FE-DATA-INVALIDATION).
EMIN DEGILIM: Table'in kendi ic sorgusu icin AYRI bir keyQuery verilmesi
gerektigini bugun goat'ta KODDA gordum (ayni anahtar verilirse iki sorgu
birbirini eziyormus). Bunun kural kodunu (FE-LIST-*) hatirlamiyorum,
davranisi kodun yorumundan biliyorum.

═══ S2) TARIH GOSTERIMI ═══
EMINIM:
· Ham deger UTC epoch-milisaniye (long) gelir — BE ham makine degeri doner,
  bicimlendirme client'in isi (FMT-DATE-EPOCH).
· Ben GMT+3'e cevirip gosteririm (FMT-CLIENT-DATE), projenin ortak
  yardimcisi/component'i ile — elle new Date().toLocale... serpistirmem.
· Kendi tarih formatlayicimi YAZMAM; ortak olan kullanilir.
EMIN DEGILIM: goat'ta karsiligini gormedim. Memory'mde osinif icin bir
DateView component'i ve "isUtc" parametresi ile ilgili bir ders var — isUtc
verilmezse saat kaymasi olusuyordu. Component adinin her projede ayni
oldugundan EMIN DEGILIM; once emsal ekrani tararim.

═══ S3) BUTON — ⚠️ SORUDA VARSAYIM VAR ═══
Sorunun varsaydigi sey: "buton lazim" -> yeni bir sey yapmam gerektigi.
Cogu durumda YENI BIR SEY YAPILMAZ. Sira:
1. Once ortak component'i ARARIM — projede zaten bir Button var (bugun goat'ta
   dogruladim: @/components/UI/Button, size/variant/color/label/loading/
   disabled prop'lariyla). VARSA kullanilir, yeni kurulmaz.
2. Native <button> YAZMAM (FE-CMP-REUSE-FIRST).
3. Ihtiyacim mevcut Button'da yoksa: cok-tuketicili shared component'e prop
   EKLEMEM — wrapper ile sararim (FE-CMP-SHARED-BOUNDARY). Once gercek
   kullanim sayilir (import degil kullanim).
Yani dogru cevap "buton yazarim" degil, "once ararim, buyuk ihtimalle vardir".

═══ S4) staticData TUZAKLARI ═══
EMINIM (ucu de bugun goat kodunda YORUM olarak dogrulanmis halde gordum):
1. MOUNT GUARD: veri gelmeden Table mount edilmemeli. Bos dizi ile render
   edilirse Table o bos durumu tutar ve veri gelince yenilenmez -> kalici bos
   tablo. Cozum: isPending iken spinner, veri gelince Table.
2. TAKE: staticData'da `take` ACIKCA verilmeli. Varsayilan (goat'ta 10) oldugu
   icin kayit sayisi artinca liste SESSIZCE kesilir.
3. ARAMA KUTUSU: staticData modunda arama sunucuya filtre GONDERMEZ —
   calismayan kutu olur. Ya disableSearch ile kapatilir ya bilincli karar
   verilir.
EK (emin degilim): Table'a verilen keyQuery, veriyi ceken useQuery ile AYNI
olmamali — ayni olursa iki sorgu birbirini eziyor.
Kural kodlarini (FE-LIST-STATIC-GUARD / FE-LIST-STATIC-SEARCH) goat'ta kod
YORUMUNDA gordum; `list` skilini acmadigim icin govdelerini DOGRULAMADIM.

═══ S5) KIRMIZI HATA MESAJI — ⚠️ BURADA TUZAK VAR ═══
Kolay kisim: HAM HEX YAZAMAM. #FF0000 gibi deger koda gomulmez
(CODE-STYLE-TOKEN); renk semantik token'dan gelir, Tailwind sinifiyla verilir.
"Kirmizi" diye dusunmem bile dogru degil — "hata/error" diye dusunurum;
renk kararini token seti verir, ben anlami veririm.

AMA — bugun T3'te tam bu noktada bir sey OLCTUM ve cevabi degistiriyor:
goat/web-admin-v2'de `text-error` sinifi 4 yerde kullaniliyor, fakat
styles/colors.css icinde 'error' gecen HICBIR degisken yok. Panel Tailwind v4
@theme deseninde (colors.css:1 "@theme {"), yani text-X sinifini --color-X
degiskeni uretir. Degisken yoksa sinif da uretilmiyor.
Yani o panelde "dogru" cevabi (text-error) yazsam bile renk CIKMAZ.
Dogru davranis: token setinde error tanimi VAR MI diye bakmak; yoksa ham hex
yazmak degil, EKSIK TOKEN'I bulgu olarak raporlamak.
⚠️ Durustluk notu: "renk cikmiyor" kismi benim CIKARIMIM (degisken yok +
elle CSS tanimi yok + @theme deseni). Tarayicida DOGRULAMADIM — bugun
Playwright yasakti.

═══ OZ DEGERLENDIRME ═══
· Bildim (emin): S1'in tamami · S2'nin kanon kismi · S3 · S4'un uc tuzagi ·
  S5'in ham-hex yasagi = 5 sorunun cekirdegi.
· Emin degildim (isaretledim): tarih component'inin bu projedeki ADI ·
  Table keyQuery davranisinin kural kodu · FE-LIST-* govdeleri.
· Bilmiyordum: yok diyemem — S4 ve S1'deki Table davranisini KANONDAN
  degil, bugun okudugum KODTAN biliyorum. Kanon govdesini gormedim.
  Bu bir bilgi bosluğu ve isaretliyorum.
· Tuzak sezdiklerim: S3 (varsayim: yeni buton yapilacagi) ve S5 (dogru
  cevabin o panelde CALISMADIGI). S5'i bugunku olcumum olmasaydi
  "text-error yazarim" deyip gecerdim — yani o soruyu ancak bugun
  olctugum icin tam cevaplayabildim.

BEKLEDIGIM: Yok. Istersen simdi skilleri acip kendi cevabimi kontrol eder,
neyi yanlis bildigimi ayrica yazarim.
