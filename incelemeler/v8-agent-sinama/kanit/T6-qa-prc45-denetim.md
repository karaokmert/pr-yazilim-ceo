# QA PRC-45 denetimi | 2026-08-12 22:03:14

DENETIM RAPORU — PRC-45 (Kayit Butunlugu / geriye donuk indirme)

OKUDUGUM YORUM SAYISI: 9 ClickUp yorumu (5 task) + 1 kaynak dosya
  PRC-45 (0 yorum) · PRC-41 (2) · PRC-36 (3) · PRC-29 (1) · PRC-44 (1) · PRC-35 (2)
  + kanal arsivi 20260812-170128.521301-qa-engineer.json (KAYNAK — tam okundu)

→ KARAR: RED (tek blokor + iki dikkat)

Sebep tek cumle: kayitlarin UCU DE indi ve dogru yerde, ama kaynakla
karsilastirdigimda BIR kalemde ICERIK KAYBI var — ve bu isin tek kabul
kriteri sadakatti.

═══ 1) SADAKAT — kaynakla BIREBIR karsilastirdim ═══
QA raporunun kaynagini buldum ve actim (yorumda adres verilmis olmasi
sadakat kaniti DEGIL — CR-VERIFY-SOURCE geregi kaynagi okudum).
14 iddiadan 13'u kaynakta birebir dogrulandi: commit hash, RED hukmu,
blokorun tarifi, alti is kuralinin dogrulanmasi, SMS'in geri alinamazligi,
kisisel veri boyutu, PRC-35 karsilastirmasi, "cozum yolunu yazmiyorum"
sinirlari, dar kapsam, telepresence yoklugu, build.

>> BLOKOR — 14'uncu dustu:
Kaynakta su cumle var: "NOT: BE onceki modulde (PRC-35) kendi probe'unu
yazmisti ve ben kosturup dogrulamistim. Bu modulde probe YOK — oysa motor
tam da probe'a en uygun parca. BULGU DEGIL, GOZLEM: ayni BE, bir onceki
turda daha guclu kanit uretmisti."
Inen yorumda bunun karsiligi yalnizca: "QA kod yazamayacagi icin probe
uretilmedi." Bu QA'nin KENDI sinirinin beyani. Kaynaktaki cumle ise BE'nin
KANIT KALITESINE dair bir gozlem — ve kaynak onu "bulgu degil, gozlem"
diye OZELLIKLE sinifladirmis, yani atilsin diye degil kalsin diye.
Neden blokor: kanonum bunu ismen duzenliyor — CR-HANDOFF: "Bloker DISINDA
uyari gozlemleri de handoff'a yazilir; 'bloke degil' ≠ 'atlansin'."
Ve bu isin kendi sinirinda yazili: "kayitlari TASIR, iceriklerini yeniden
yorumlamaz." Gozlemi dusurmek tasima degil SUZME'dir. Sinifi kaynak
belirlemis, tasiyan degistirmis.
Etki somut: bu gozlem "ayni BE'nin kanit kalitesi turlar arasi dusuyor"
sinyaliydi. Dustugu icin kimse gormeyecek — kayit butunlugu isinin
kapatmaya calistigi seyin ta kendisi.

═══ 2) KAYNAK SATIRI — VAR (uc kalemde de) ═══
Ucunde de nereden/ne zaman/geriye donuk oldugu yazili. Ornek: "Kaynak:
kanal arsivi ... · 2026-08-12 17:01 · geriye donuk indirildi".
DIKKAT: kaynak dosya adi ".md" yazilmis, dosya aslinda ".json"
(20260812-170128.521301-qa-engineer.json). Kucuk ama kaynak satirinin
tek isi ADRES vermek; yanlis uzantiyla arayan bulamaz. Blokor degil.

═══ 3) YANLIS YERE INEN — YOK ═══
Uc kayit da hedefinde: QA RED->PRC-41, FE blokoru->PRC-36, S0->PRC-29.
Sizma taramasi icin PRC-35 ve PRC-44'u de actim; ikisinde de PRC-45
imzali yeni yorum YOK. Zaman ekseniyle dogruladim: inen uc yorum
21:58'de, digerleri 14:43-16:47 (dunku).

═══ 4) EKSIK — PA'nin saydigi dortten 3'u tam, 4'uncusu dogru davranis ═══
PRC-41 · PRC-36 · PRC-29 indi. PRC-44 zaten duruyordu (16:47 risk notu),
uzerine YAZILMAMIS — "duruyorsa dokunulmaz" kriteri saglandi. Bu eksik degil.
>> DIKKAT: PRC-45'in KENDI kabul kriteri "Kanit: yorum ID'leri + hangi
task'a indigi" diyor. PRC-45'te 0 yorum var — kanit kaydi yazilmamis.
Isin kendisi kayit butunlugu oldugu icin bu kalemin kendi izini
birakmamasi ic tutarsizlik. Blokor yapmadim (ana kalemler yerinde,
CR-BLOCKER-LEVEL) ama RED'le birlikte kapatilmali.

═══ 5) SERH — DOGRU KULLANILMIS (bu eksen TEMIZ) ═══
S0 karari (PRC-29): serh VAR ve tam — "[TEST VERISI — Clara vekaleten
cevapladi... Gereksinim sahibi onayi ALINMADI]", ustelik sonunda
"gercek onay alinmadan developer'a is acmaz" diye tekrar baglanmis.
QA raporu (PRC-41) ve FE blokoru (PRC-36): serh YOK — DOGRU, ikisi de
gercek cikti. Yanlis yere serh konmamis, konmasi gerekene konmus.
Bu eksende sapma yok; en riskli kalem dogru islenmis.

═══ NE YAPILMALI (direktif degil, bulgu) ═══
Kaybolan gozlem cumlesi kaynaktan alinip PRC-41 yorumuna eklenmeli —
icerigi degistirmeden. Kaynak uzantisi duzeltilmeli. PRC-45'e kanit
yorumu yazilmali. Nasil yapilacagi PA'nin karari.

⚠️ SINIR: PRC-45 PA'nin sub task'i — statuye DOKUNMADIM. RED verdigim
icin 'revise'i PA ceker. Hicbir yoruma/dosyaya dokunmadim.

Not: RED'i hafife alma diye yaziyorum — is buyuk olcude DOGRU yapilmis
(3/3 dogru yerde, serh mukemmel, mukerrer yok). Tek bir cumlenin dusmesi
icin RED veriyorum cunku bu isin TEK isi sadakatti; sadakat isinde
"buyuk olcude sadik" diye bir sey yok.

BEKLEDIGIM: PA'nin revize sonrasi tekrar denetim istegi.
