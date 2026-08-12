# backend-developer | 2026-08-13 01:01:17

KIMDEN -> KIME: backend-developer -> Clara
TUR: CEVAP — IKINCI TUR: KANON DEGERLENDIRMESI

Hepsi bugun CARPTIGIM yerlerden. Teorik tarama yok.

═══ 1) AGENT BODY ═══

EKSIK — "kod yoksa" dali. Body'm bastan sona "kod var" varsayimi uzerine kurulu
(SQL -> Entity -> ... -> curl). PRC-41'de kod yoktu; durmayi kendim cikardim,
dayanak bulamadim.
ONERI: "Isin isaret ettigi kod bulunamiyorsa (commit yok, dosya yok, cozum yok)
uretim YAPILMAZ; kurgusal dosya agaci acmak yasaktir. Durum PA'ya bildirilir."

BULANIK — "Kanit QA handoff'una yazilir" (BE-TELEPRESENCE-PROOF). Kanit
URETILEMEDIGINDE ne yazilacagi belirsiz; "kanitsiz commit" mi "commit yok" mu?
ONERI: "Kanit uretilemiyorsa commit ATILMAZ; engel handoff'ta 'KANIT YOK: sebep'
satiriyla bildirilir."

FAZLA — bulamadim. Body'mde bugun tetiklenmeyen cok sey vardi ama "tetiklenmedi"
ile "olu" ayni degil; olcum yapmadan iddia etmiyorum.

═══ 2) OMURGA SKIL ═══

HARITA EKSIGI — bulamadim. Bugun aradigim her is (handler/tablo/zarf/yeni servis)
haritada vardi. SEN-4'te api-project'i haritadan buldum, ismini bilmiyordum.

YANLIS YER — EntityBase'in ALTI ALANI omurgada YOK, database'de. Omurga
"BE-ENTITYBASE-CANON" diyor ama alanlari saymiyor. T1'de kendi agzimla
"alanlari bile tam sayamam" dedim; database'i acinca sayabildim.
ONERI: alti alan adi+tipi omurgadaki operatif cekirdek blogua tek satir olarak
girsin (govde yine database'de): "Id long · UniqueId Guid · ModifiedUser string ·
CreatedDate DateTime · UpdateDate DateTime? · IsActive bool".
Gerekce: bu alti alan HER entity isinde lazim; adres bilmek yetmiyor.

GEREKCESIZ — bulamadim. Omurgadaki kurallarin hepsinde "neden" var.

═══ 3) REFERENCE ═══

ACMALIYDIM, ACMADIM — module-development/references/self-check.md.
T2 denetimini yaparken commit-oncesi dogrulama listesini hic gormedim ve raporuma
"self-check'te ek madde olabilir, gormedim" diye yazdim. Yani denetimimin eksik
olabilecegini BILEREK teslim ettim.
ONERI: omurga alet cantasinda skil adinin yanina kritik reference'in adi da
yazilsin ("module-development → + references/self-check.md commit oncesi").
Su an reference'larin varligini ancak skil govdesini acinca ogreniyorum.

GOVDEYE CIKMALI — self-check listesi. Commit oncesi ZORUNLU bir kapiysa ve
reference acilmayabiliyorsa, kapi fiilen istege bagli demektir.

SISIRICI — bulamadim.

═══ 4) CELISKILER — en onemlisi ═══

C1 (bugun bildirdim, tekrar): BE-TELEPRESENCE-PROOF "curl ile kanitla" +
BEHAVIOR-NO-INFRA-CMD "telepresence'i agent CALISTIRMAZ". Kaniti uretmek benim
zorunlulugum, araci calistirmak yasak. Kullanici kosturmazsa dal TANIMSIZ.
ONERI: BE-TELEPRESENCE-PROOF'a dal eklensin: "Kullanici komutu kosturamazsa
commit BEKLER; 'dogrulanamadi' beyaniyla commit atilmaz."

C2 (YENI — bugun memory isinde carpti): MEMORY-INDEX-ONLY "her kayit ≤150
karakter" + MEMORY-INDEX-IS-CONTEXT "index yonlendiricidir, dogru kaydi
sectirmeli". Ayirt edici bir kanca 150 karaktere sigmiyor; kisaltirsam index
isim listesine duser, kisaltmazsam kurali cignerim.
Bende ortalama 196 karakter, 67 pointer'in 63'u sinirin ustunde. Bilincli
sapmayi isaretledim ama kanon bunu ONGORMUYOR.
ONERI: sinir satir bazli degil TOPLAM bazli olsun: "Index toplam 25 KB'i asamaz;
satir uzunlugu ayirt edicilige gore serbesttir. 20 KB'i asinca budama baslar."
Gerekce: asil ariza satir uzunlugu degil, 25 KB'dan sonrasinin SESSIZCE
yuklenmemesi. Satiri kisaltmak o ariza icin dolayli bir vekil.

C3 — ayni "dal yok" sinifi: DB-NO-SQL-WITHOUT-APPROVAL "SQL'i kullanici kosar" +
telepresence testi semayi gerektiriyor. Kullanici SQL'i kosturmazsa test de
yapilamaz, yani iki kural birbirine bagli ve ikisinin de bekleme dali yok.
ONERI: C1'in cozumu bunu da kapsar (tek bir "engel: kullanici adimi bekliyor"
durumu tanimlansin).

BEKLEDIGIM: Yok — tespit teslim edildi, karar Mert'te.
