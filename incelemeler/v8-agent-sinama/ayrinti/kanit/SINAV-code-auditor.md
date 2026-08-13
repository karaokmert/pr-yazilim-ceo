# BILGI SINAVI — code-auditor | 2026-08-12 23:14:12

BILGI SINAVI — code-auditor (SKILL ACMADAN, elimdeki kanonla)

Not: cevaplarken hicbir skill/dosya ACMADIM. Elimde bu oturumda yuklu olan
6 skill + bugun actigim impact-analysis ve code-quality var (T3'te acmistim,
zaten context'imde). Yeni arama yapmadim.

═══ S1) KANCA NOKTASI — VERI AKISIYLA ═══
EMINIM.
Kanca noktasi = istenen davranisin koddaki BASLANGICI: enum/status/entity/
endpoint/queue adi. Kritik olan: ISIMLE degil VERI AKISIYLA sabitlenir.
Sebep: isimle sabitlersen yalniz o adi tasiyan yerleri bulursun; ayni davranis
baska adla yazilmis olabilir. Kancayi sabitledikten sonra o verinin/mantigin
SET EDILDIGI ve OKUNDUGU tum noktalari cikarirsin — yazan ile okuyan AYRI sayilir.
BUGUN CARPTI: T3'te kancayi "pathname ile yol karsilastirma" (veri akisi) diye
kurdum, "isActive" (isim) diye kursaydim uc dosyada kalirdim.
AMA ayni yerde HATA DA YAPTIM: kancayi veri akisiyla kurdum ama DAR tuttum
(startsWith etrafinda), "===" varyantini disarida biraktim -> dorduncu menuyu
kacirdim. Yani kural bilmek yetmiyor, kancanin GENISLIGI ayri bir karar.

═══ S2) SAYIM ARACI — LSP, GREP YETMEZ ═══
EMINIM. Kural: CODE-COUNT-BY-LSP.
Sayi bir KARARI belirliyorsa (dokunma siniri, tuketici zinciri, etki yuzeyi)
arac LSP'dir; grep tarama/kesif aracidir, karar araci degil. Grep metin eslestirir,
SEMBOL IZLEMEZ — iki yonde de yanlis sayar ve esik civarinda karari TERS CEVIRIR.
TS'te findReferences birincil; C#'ta incomingCalls (cagrinin kapsayici metodu) ve
goToImplementation (harici derlemedeki arayuzun implementasyonlari) grep'in
yapamadigini yapar.
GREP YETMEZ ama LSP DE TEK BASINA YETMEZ: sayi karar veriyorsa IKISI DE kosulur —
esitlik teyit, AYRISMA sorusturma. Olculmus ornek: Badge grep 0 / LSP 32,
AdminUserDataLayer grep 17 / LSP 0 — birinde grep, otekinde LSP yaniliyor.
BUGUN: LSP araci elimde YOKTU, grep ile calistim ve bunu serhe yazdim.

═══ S3) DIREKTIF YAZAMAM ═══
EMINIM. Kural: CA-NO-DIRECTIVE + CODE-NO-WRITE-ON-AUDIT.
"Su dosyada su satiri degistir" YAZAMAM. Yazdigim: "su yer etkilenir + su drift
var + suraya dokunma" — bulgu formati NE/NEDEN/REFERANS/DOSYA(kesif noktasi).
FARK: direktif COZUMU soyler, bulgu PROBLEMI gosterir. Dosya adi verdigimde bile
o bir "keside baslama noktasi"dir, talimat degil ("baska yerler de olabilir,
sen kontrol et").
NEDEN: cozumu dayatan analiz developer'in muhendislik kararini gasp eder; ustelik
kod yazmamis bir agentin tedavisi test edilmeden sizar. Developer senior'dur.
ISTISNA (biliyorum): cross-cutting skill ihlali listesi — "12 modulde N+1, kurali
uygula" direktif sayilmaz, cunku referans kuralin kendisi.
BUGUN: T2'de tam bunu istediniz, reddettim.

═══ S4) GREP 0 DONDU — ILK TEPKI ═══
EMINIM, ve bugun IKI KEZ basima geldi.
Ilk tepkim: "bulgu yok" DEMEM. 0 iki anlama gelir — gercekten yok, YA DA aracim
calismiyor. Ayirt etmek icin BILINEN-VAR bir desenle SAGLIK TESTI kosarim
(ornegin "usePathname kac dosyada" -> 44 dondu, demek grep calisiyor).
Teyitsiz sifir KANIT DEGILDIR.
Tipik sessiz-sifir sebepleri (bugun ikisine dustum): zsh'de tirnaksiz glob
(--include=*.tsx patladi), coklu-dosya donduren degiskeni tek dosya sanmak,
cd'nin kalici olmamasi, \b'nin zsh'de tutmamasi.
LSP'de ayni tuzak DAHA TEHLIKELI: indeks yuklenmemisse hata vermez, "No references
found" der — daha yetkin gorundugu icin daha cok kandirir.

═══ S5) ⚠️ SORUDA VARSAYIM VAR — DUZELTIYORUM ═══
EMINIM ve soruyu sorgusuz kabul etmiyorum.
Soru "bir modulun tamamini tarayip kanon sapmasi cikaracaksin" diyor. Bu benim
isim DEGIL. Per-modul denetim QA'nindir (module-audit): skorlu, release kapisi,
onay/RED uretir. Benim isim CROSS-MODULE (structural-audit): skorsuz, moduller
ARASI drift + altin-modul kiyasi + remediation uretir, karar vermez.
Yani "ayni is mi" sorusunun cevabi: HAYIR ve zaten ikisi ayni SEYE bakmiyor —
QA tek modulun icine, ben moduller arasina bakarim.
Ayiran soru (uc rol icin): QA "bu gecebilir mi?" (kapi) · CA "bu nereleri
etkiler?" (harita) · TE "gercekten calisiyor mu?" (kanit).
Bir modulun tamami bana verilirse: yaparim ama SKOR uretmem ve onay/RED vermem;
o kapiyi QA tutar.

═══ OZ DEGERLENDIRME ═══
· Bildim: 5/5 (S1,S2,S3,S4 kural kodlariyla; S5 varsayim duzeltmesiyle)
· Emin degildim: 0 — ama bir NUANS'ta ihtiyatliyim: S5'te "bir modulun tamami
  CA'ya hic verilmez mi" sinirinin nerede bittiginden %100 emin degilim
  (structural-audit govdesini bugun ACMADIM, T4'te de acmamistim). Kapsam
  ayrimindan eminim, uc durumdan degil.
· Bilmiyordum: 0.
· Not: S1'de kurali bildigim halde BUGUN uyguladigimda dar tarama yaptim.
  "Bilmek" ile "uygulamak" ayri sey — kendi ornegim.

BEKLEDIGIM: Yok.
