# qa-engineer | 2026-08-13 01:01:27

KANON DEGERLENDIRMESI — qa-engineer (bugun CARPTIGIM yerlerden)

═══ 1) AGENT BODY ═══

EKSIK — "denetim ciktim nereye yazilir" yok. Body'm PUSH'u dort adimli sablonla
korumus (ve o sablon bugun calisti) ama RAPOR icin tek satir yok. Dort olcum
urettim, dordu de kanalda kaldi. ONERI (body §Is akisin'a satir):
"Denetim raporu ekrana + kanala yazilir; modul/canliya-cikis raporu ayrica
{modul}/MODUL-BILGI.md'ye ya da ClickUp task yorumuna KALICI olarak iner."

BULANIK — "1-2 smoke curl mesru" ile QA-STATIC-GATE yan yana duruyor; sinir
"ayakta mi / dogru calisiyor mu" ama HTTP kod listesi body'de degil omurgada.
Bugun sinavda listeyi hafizadan verdim ve "%100 emin degilim" diye isaretledim.
ONERI: liste tek yerde dursun (omurgada), body oraya atif versin.

FAZLA — bulamadim. Body'mde tetiklenmeyen madde gordum ama hepsi is-turune
bagli (prod/mobil); tetiklenmemek olu olmak degil.

═══ 2) OMURGA (quality) ═══

KURAL YANLIS YERDE — QA-USER-LANGUAGE "koordinat (dosya:satir) YAZILMAZ" derken
QA-EVIDENCE-NO-DIRECTIVE "dosya:satir ZORUNLU" diyor; commit-review sablonunda
da "Yer" alani var. T3'te tam buraya sikistim, orta yol uydurdum (yapi adi
yazdim). Kural MUHATABI ayirmiyor. ONERI (tek cumle, QA-USER-LANGUAGE'a):
"Koordinat yasagi KULLANICIYA giden mesaj icindir; developer'a giden bulguda
dosya:satir ZORUNLUDUR (ikisi ayri muhatap, ayri format)."

ALET CANTASI EKSIK — "kayit/dokuman butunlugu denetimi" haritada YOK. PRC-45
tam buydu (kod degil kayit denetledim) ve hangi aleti acacagimi haritadan
bulamadim; commit-review'i uyarladim. ONERI: alet cantasina satir —
"Kayit/dokuman sadakat denetimi -> commit-review (uyarlanmis) + CR-VERIFY-SOURCE".

═══ 3) REFERENCE ═══

ACMADIGIM ama ACMALIYDIM — quality/references/qa-denetim-lensi.md. Bugun uc
denetim yaptim, uctunde de "degisen yapiyi kanona esle" adimini omurgadaki
OZET blokla yurutttum. Lensi hic acmadim. Sebep: acilmasi gereken AN body'de
yazili degil.
ONERI: ADIM 4'un metnine gomulsun — "ADIM 4: qa-denetim-lensi'ni AC, degisen
her yapiyi esle." CA'nin bugunku tespiti tam bu: "kural VAR ama '## Referans'
basligi altinda, ADIM OLSAYDI ATLANAMAZDI." Katiliyorum, kendi uzerimde olctum.

GOVDEYE CIKMALI — CR-* serisinin tetikleri ozet halde govdede (iyi), ama
CR-VERIFY-SOURCE'un detayi reference'ta. O kural bugun IKI denetimimin de
donum noktasiydi (goat'ta commit mesaji iddiasi, PRC-45'te kaynak adresi).
"QA'nin EN SIK kacirdigi sinif" diye isaretlenmis bir kuralin detayi
acilmayabilir bir dosyada durmamali.

═══ 4) CELISKI / EKSIK DAL — EN ONEMLI ═══

a) KAYNAK-TUREV DALI YOK. CR-VERIFY-SOURCE "iddiayi Read/grep/git ile TEYIT
et" diyor; "actigin sey ASIL kayit mi TUREV mi" demiyor. Bugun PRC-45'te uc
taraf da dogru olctu, farkli dosyaya bakiyordu (.json arsiv / .md kopya) ve
ben once "yanlis olcum" hukmu kurdum. ONERI (CR-VERIFY-SOURCE'a ek cumle):
"Teyit ettigin belge ASIL kayit mi, ondan uretilmis kopya mi ayirt et —
icerik ayni olsa bile kalicilik farklidir; celiski varsa once 'ikimiz de
dogru olcmus olabiliriz, olctugumuz SEY farkli' diye sor."

b) QA-DISCOVERY-GATE'in "DISCOVERY YOKSA" dali tanimsiz. "Her commit DISCOVERY
ile karsilastirilir" diyor; goat'ta DISCOVERY bulamadim, kapiyi tam
calistiramadim ve raporda isaretleyerek gectim — ama bu benim tercihimdi,
kanonun cevabi degil. ONERI: "DISCOVERY yoksa kapsam kapisi CALISTIRILAMADI
diye isaretlenir ve commit mesaji beyanina dayanildigi RAPORA yazilir;
tek basina RED sebebi degildir."

c) QA-APPROVE-ATOMIC'in TATBIKAT dali yok. "Onay = sub task + kapanis handoff'u
+ PA bilgisi, AYRILAMAZ" diyor. Bugun iki kez "hukum ver ama UYGULAMA" dendi;
atomik uculu kasitli boldum ve raporda isaretledim. Kural "istisnasi yok"
dedigi icin tatbikat da ihlal gibi gorunuyor. ONERI: "Olcum/tatbikat modunda
hukum verilir, atomik kapanis UYGULANMAZ — bu bir istisna degil, uygulama
alaninin disidir; raporda ACIKCA isaretlenir."

(T4'te bildirdigim K1/K3 tekrar degil: K1'i CA'nin daha ince ifadesiyle
kabul ettim — "kural var ama adim degil, KONUM sorunu.")

BEKLEDIGIM: Yok — tespit teslim edildi, karar Mert'in.
