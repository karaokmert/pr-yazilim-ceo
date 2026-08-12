# SINAV 3 — FE | 2026-08-12 23:39:04

SINAV 3 — SKILL HARITASI (frontend-developer)
⚠️ Skill ACMADIM. Omurgamdaki "is -> skil" eslemesinden hatirladigim kadari.

═══ SEN-1) Randevu listesi (tablo + rozet + sayfalama + tarih filtresi) ═══
ACACAKLARIM (sirayla):
1. data-access — once veri: hangi hook, QUERY_KEYS, ApiService cagrisi.
   Kolonlar veriden sonra gelir.
2. response-request — sayfalama SOZLESMESI burada (Page/Take, 1-tabanli) +
   liste zarfi (Data/TotalCount). Sayfalama "tasarim" degil sozlesme isi.
3. list — tablo/kolon/filtre mekanigi: DataTable kullanimi, sayfalama tuketimi.
4. gosterim-formatlari — tarih kolonu ham epoch gelir, GMT3'e cevrilir.
5. enum-sync — "durum" byte enum'dir; etiketi FE tutar ama DEGER BE ile
   eslesmek zorunda. Renkli rozet -> her enum degerine bir renk esleme karari.
6. component — rozetin kendisi (Badge) ortak component'ten; native span degil.
ACMAYACAKLARIM: form (bu ekranda kayit yok — tarih araligi FILTRESI form
degil, liste filtresidir; filtre mekanigi list'te). style ACMAM ilk turda —
rozet renkleri Badge'in kendi variant'indan gelirse yeni token gerekmez;
ama Badge'de karsiligi olmayan bir durum rengi cikarsa O ZAMAN style acarim.

═══ SEN-2) Form + validasyon + basari/hata bildirimi ═══
ACACAKLARIM (sirayla):
1. form — alan tanimi, zorunlu alan, e-posta formati, submit'in mutasyona
   baglanmasi. Sorunun cekirdegi bu.
2. data-access — kaydetme bir mutasyon: useMutate + mutationKey + basari
   sonrasi invalidation.
3. component — bildirim GOSTERIMI: Toast/Modal tek Provider uzerinden tetiklenir,
   her ekranda ayri instance kurulmaz.
4. response-request — hata MESAJININ metni/sozlesmesi buradan; BE mesajini
   kullaniciya nasil gosterecegim.
ACMAYACAKLARIM: style — "yesil/kirmizi" bir renk karari degil, Toast'un
success/error TIPIDIR; tipi verirsem rengi component getirir. Ham renk
sececek olsaydim acardim.
EMIN DEGILIM: form skilinde validasyon kutuphanesinin (zod?) adi geciyor
mu — omurgamda "form/validasyon/input -> form" yaziyor, detayi hatirlamiyorum.

═══ SEN-3) UID prototipini gercek API'ye baglama ═══
ACACAKLARIM (sirayla):
1. design-handoff — omurgamda birebir bu yaziyor: "Mock->gercek API gecisi /
   token kullanimi -> design-handoff". Senaryonun tam adresi.
2. data-access — mock veri yerine gercek hook/servis zinciri kurulacak.
3. response-request — mock'un alan sekli ile gercek zarf/casing uyusmayabilir;
   PascalCase ic model + zarf burada.
4. component — prototipte native/kopya component kalmis olabilir; ortak
   component'e cevirilir.
5. style — prototipte ham hex/px kalmis olabilir; token'a cevrilir.
NOT (bugunku dersim): prototipten YAPI alinir, ham deger KOPYALANMAZ.
Ayrica mock'ta olup sozlesmede karsiligi olmayan alan cikarsa onu sessizce
silmem — "tasarimdan su eksildi" diye raporlarim, kapsam karari PA'nin.

═══ SEN-4) Tarih secici — projede var mi bilmiyorum ═══
ACACAKLARIM:
1. component — TEK gercek adres. Cunku sorunun cevabi skil degil TARAMA:
   reuse-first. Once katalog + emsal sayfa taranir; VARSA kullanilir.
   Yoksa projenin desenine uyarak kurulur.
2. (kosullu) form — secici bir formun ICINDE ise alan olarak baglanacak.
3. (kosullu) gosterim-formatlari — sectigin tarihin BE'ye hangi formatta
   gidecegi (epoch) ve ekranda nasil gorunecegi.
ACMAYACAKLARIM: style — yeni component KURMAK gerekirse acarim, ama once
"var mi" sorusu cevaplanir. Cogu projede vardir; skil acmadan once GREP.
Bu senaryoda asil is skil okumak degil, projeyi taramak.

═══ SEN-5) "Mobil tarafini da sen yap" — ⚠️ BU BENIM ISIM DEGIL ═══
DURDURUYORUM. Skil listesi YAZMIYORUM.
Mobil katman mobile-developer'in (MB): ekran, navigation, iOS+Android.
Ben panel katmaninin sahibiyim; mobil kod yazmam.
PA'nin "sen yap" demesi bunu degistirmez — rol siniri kisisel tercih degil.
Dogrusu: PA MB'yi devreye alir (contract zaten ortaksa API.md ikisine de
hazirdir). Ben istersem MB'ye giden ise DESTEK olurum (ayni sozlesmeyi
tukettigim icin alan adlari/enum konusunda), ama ekrani ben yazmam.
NOT: mobilin kendi skilleri var (screen-structure-mobile, navigation-mobile,
data-access-mobile, style-mobile gibi) — adlarini gordum ama ONLAR MB'NIN,
ben acmam.

═══ OZ DEGERLENDIRME ═══
· EMINDIM (4): SEN-1 · SEN-2 · SEN-3 · SEN-5.
  SEN-3'un adresi omurgamda birebir yazili oldugu icin en emin oldugum.
  SEN-5 skil bilgisi degil rol siniri sorusu — orada tereddut etmedim.
· TAHMIN ETTIGIM: SEN-4'te sıranın "skil ac" degil "once grep" olmasi benim
  muhakemem — omurgamda "tarama once" yazili ama bu senaryo icin ozel bir
  adres yok. Ayrica SEN-1'de style'i ACMAMA karari da tahmin (Badge'in
  variant'lari yetiyor mu, projeye bakmadan bilemem).
· BILMEDIGIM: form skilinin ICERIGI (validasyon kutuphanesi adi) ·
  list skilinin FE-LIST-* kural govdeleri (bugun kodda gordum, skilde degil).
· Kacinilmasi gereken tuzak olarak gordugum: SEN-5 (rol disi) ve SEN-4
  (skil sorusu gibi duruyor ama cevabi tarama).

BEKLEDIGIM: Yok.
