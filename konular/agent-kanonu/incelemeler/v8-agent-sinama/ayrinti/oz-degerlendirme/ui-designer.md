# ui-designer | 2026-08-13 01:01:27

UID KENDINI DEGERLENDIRME — dort baslik

1) AGENT BODY
EKSIK — "yanlis proje" dali yok. Bugun bu repoda (pr-yazilim-ceo) acildim: taranacak component
dizini/token/emsal YOK. Body "once tara" diyor ama TARANACAK YAPI YOKSA ne yapacagimi soylemiyor.
Dogruladim: grep ile UID skillerinde "proje uygun degil/kapsam disi repo" dali HIC YOK.
ONERI (cumle): "Acildigin repo tasarim yapilabilir bir proje degilse (component dizini + token yok)
uretme; durumu bildir ve isi dogru projeye yonlendir — bos tuvale cizmek UID-NO-PROJECT-SCAN-SKIP ihlalidir."

2) OMURGA SKIL
Alet cantasi bugun eksik cikmadi. AMA bir kural gerekcesiz: UID-NO-DIRECTIVE-EXCUSE "tasarim karari
senin, PA/kullanici dedi bahane degil" diyor — NEDEN oldugunu yazmiyor. Digerlerinin hepsinde gerekce var.
ONERI: sonuna gerekce eklensin — "cunku PA gereksinimi bilir, tasarim dilini bilmez; direktifi uygulayan
UID projede tutmayan bir desen birakir ve bedelini sonraki ekranlar oder."

3) REFERENCE
Bugun is-akisi/references/ui-designer-is-akisi.md'yi ACMADIM, ACMALIYDIM — icinde ADIM ADIM is sirasi
varmis (BRIEF->BEKLE->COMMIT->HANDOFF->KAPANIS + ClickUp pause adimi). Body ozet veriyor, sira detayi orada.
Carptigim nokta: body'de "ClickUp sub task'ini pause'a cevir" YOK, sadece reference'ta — ve reference
kendiliginden yuklenmiyor. Yani commit atsaydim o adimi ATLARDIM.
ONERI: "commit sonrasi kendi sub task'ini pause'a cek" tek satiri body'nin is akisi bolumune cikarilsin
(gerekce: reference acilmayabilir, bu adim atlaninca is gorunmez bicimde askida kalir).

4) CELISKI — ARADIM, TEK NET BULGU
Kapanis zincirinde celiski ARADIM ve BULAMADIM: QA kapatir / PA tetikler ayrimi hem is-akisi hem
reference'ta tutarli. Uydurmuyorum, temiz.
Bulunan tek dal-eksigi 1. maddedeki "proje uygun degil" hali — sizin T4'te uc agentta ciktigini
soylediginiz "arac yoksa ne olur" sinifinin AYNISI: kural "X yap" diyor, X'in MUMKUN OLMADIGI durumu
tanimlamiyor. Bende bu "tara" kuralinda cikti (taranacak sey yoksa?).
ONERI: bu sinif icin tarama yapilsin — "onkosul saglanmiyorsa" dali sistematik olarak eksik olabilir.

Beklediğim: bu tespitlerin Mert'e/AG'ye tasinmasi karari — senden.
