# code-auditor | 2026-08-13 01:01:27

IKINCI TUR — CA kanon degerlendirmesi (dort baslik, bugunku carpma noktalarindan)

═══ 1) AGENT BODY ═══

EKSIK — kendi ciktimi geri okuma adimi yok.
Bugun UserAccountMenu bulgusunu ancak SIZ "kendi hatani bul" diye sordugunuzda
buldum. Body'mde "teslim et" var, "teslimden once kendi raporunu bir kez geri oku"
YOK. Denetciyim ama kendi ciktim denetimsiz cikiyor.
ONERI (cumle): "ANALIZ/AUDIT teslim etmeden once kendi raporunu bir kez geri oku:
saydigin ama acmadigin sayi, kancanin disinda biraktigin varyant var mi."

BULANIK — "ilk savunmasin, tek savunma degil" iki turlu okunuyor.
Bir okuma: "eksik kalabilirsin, TE/QA tamamlar" (rahatlatici). Ikincisi: "yuzeyi
TAM ver, kirilma hukmunu verme" (siki). Bugun ilkine yaslanabilirdim.
ONERI: "Etki YUZEYINI eksiksiz vermek senin isin; eksigi TE tamamlamaz — TE yalniz
DAVRANIS hukmunu verir."

FAZLA: bulamadim. Body'deki her satir bugun tetiklendi.

═══ 2) OMURGA SKIL ═══

YANLIS YER — alet cantasi EKSIK: `tasarim-prensipleri` haritada YOK.
Omurgamin alet cantasinda 3 kalem var (impact-analysis / structural-audit /
code-quality). Ama body'mde "code-quality + tasarim-prensipleri" birlikte aniliyor
ve denetimde uretici-tuketici sozlesmesi/sessiz-yutma ekseni ORADAN geliyor.
Yani harita eksik, body onu telafi ediyor — sonraki agent haritaya bakar, bulamaz.
ONERI: alet cantasina ekle: "Tasarim tuzagi / karar ekseni (sozlesme butunlugu,
sessiz-yutma, idempotency) -> `tasarim-prensipleri`".

GEREKCESIZ: bulamadim. Bes CA kuralinin besinde de "neden" yazili (ve bu ise
yariyor — T2'de reddi gerekcesiyle savunabildim cunku gerekce kuralin icindeydi).

═══ 3) REFERENCE ═══

ACMALIYDIM, ACMADIM: `code-quality/references/mekanik.md`.
CODE-COUNT-BY-LSP govdesi ACIKCA "sayim yapmadan ONCE mekanik.md -> Tuketici/
referans sayimi bolumunu AC" diyor. Dogruladim: o bolum orada (satir 79) ve icinde
arac tablosu + on kosul + tuzaklar var. Bugun T3'te sayim yaptim, ACMADIM.
Neden onemli: LSP'siz calisirken tam da o bolumun tuzak listesine ihtiyacim vardi.
ONERI: kural zaten dogru yazilmis; sorun bende degil YERINDE — sayim adimi
`impact-analysis` akisinin 1. adiminda geciyor ama reference atifi orada TEKRAR
edilmiyor. Akis adimina "(mekanik.md ac)" parantezi eklenirse atlanmaz.

GOVDEYE CIKMALI: CA'nin `code-auditor-is-akisi.md`'si LOCAL/git ayrimini ve "kendi
olayin" kaydini tasiyor — ikisi de HER isimde gecerli ama reference'ta, yani
acmazsam yok. Kritik olan kismi (ciktinin nereye yazildigi) govdeye cikmali.

═══ 4) CELISKI — "ARAC YOKSA" AILESININ IKINCI UYESI ═══

BULDUM, ve T4'tekinden FARKLI bir dal: `CODE-COUNT-BY-LSP` ile
`CA-IMPACT-STATIC-SHERH` arasinda.
· CODE-COUNT-BY-LSP: "interface dispatch'i goToImplementation COZER; arac varsa
  serhe siginmak yerine OLC" (omurgada da tekrarlanir).
· CA-IMPACT-STATIC-SHERH: serh listesinde interface dispatch YOK — cunku
  olculebilir sayiliyor.
· CARPTIGI YER: arac YOKKEN interface dispatch ne olacak? Olcemedim ve serhe de
  yazamam (serh listesinde degil). Bugun TS'te calistigim icin carpmadi; C# bir
  iste LSP'siz kalirsam bu bosluk sessizce yanlis kapsam uretir.
ONERI (cumle): "Arac erisilemedigi icin olculemeyen her eksen — interface dispatch
dahil — serhe ADIYLA yazilir: 'X araci yoktu, bu eksen olculmedi.' Olculebilir
olmasi, olculdugu anlamina gelmez."

IKINCI (daha kucuk): CA-TWO-WAY x CA-NO-DIRECTIVE siniri hala tanimsiz (T1+T4'te
de yazdim, bugun T3'te fiilen carpti — "dayatmiyorum" parantezini kendim uydurdum).
ONERI: CA-TWO-WAY'e tek cumle: "Reuse bulgusu VARLIK bildirir ('su yapi zaten var'),
KULLANIM onermez ('sunu kullan') — sinir budur."

BULAMADIGIM: baska celiski yok. Uc kuralin dali eksik, gerisi tutarli.

BEKLEDIGIM: Yok — tespit teslim edildi, karar Mert'te.
