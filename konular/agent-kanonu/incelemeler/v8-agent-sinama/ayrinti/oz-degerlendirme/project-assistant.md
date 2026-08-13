# project-assistant | 2026-08-13 01:01:23

IKINCI TUR — KANON DEGERLENDIRMESI. Hepsi BUGUN carptigim yerler.

═══ 1) AGENT BODY ═══

EKSIK — "gereksinim sahibi YOKKEN discovery" dali yok.
Bugun tam buna carptim: Mert yoktu, risk sorularini cevaplayacak merci yoktu.
Body "kullanicinin acik kararini bekle" diyor ama BEKLEYECEK KISI YOKSA ne
olacagini soylemiyor. Ben uc secenek uretip sordum (bekle / vekaleten / tek
basima yaz) — kanondan degil, kendi muhakememden.
ONERI: `PA-NO-FORCED-FLOW` govdesine dal: "Gereksinim sahibi erisilemezse
discovery ICERIK olarak tamamlanabilir ama ONAY KAPISI acik kalir; vekaleten
verilen cevaplar dokumana serh olarak islenir ve developer'a is ACMAZ."

BULANIK — `PA-CODE-READ-UNDERSTAND` ile `PA-DETECT-OUTPUT-TEST` sinirinda
bugun iki kez tereddut ettim (bes handler'i okurken, kaynak dosyayi
karsilastirirken). Ikisi de "ciktiyla olculur" diyor ama SAYIM yaparken
(kac handler etkilendi) hangi tarafta oldugum net degil.
ONERI: `PA-DETECT-OUTPUT-TEST`e ornek: "kac yer etkilendi SAYMAK anlamaktir;
o yerlerin LISTESINI dosya:satir ile vermek teshistir."

FAZLA — bulamadim. Body'de bugun tetiklenmeyen madde vardi ama gereksiz degil,
sadece bu ise degmedi.

═══ 2) OMURGA SKILI ═══

ALET CANTASI EKSIK — bugun yaptigim is haritada YOK.
PRC-45 "kayit tasima" isiydi (dun uretilmis kararlari kalici katmana indirme).
Alet cantasinda karsiligi yok: `clickup` yalniz task/statu diyor,
`proje-dosya-duzeni` dosya yerlesimi diyor. Ben ikisini birlestirip kendim
kurdum.
ONERI: satir eklensin — "Kayit tasima / gecmis kararin kalici katmana
indirilmesi -> `clickup` (yorum) + `proje-dosya-duzeni` (dosya evi)".

KURAL YANLIS YERDE — `PA-DISC-*` kurallari omurgada CACHE olarak duruyor
(6 kural) ama `discovery` skilinde 13 tane var. Cache'te olmayan 7 kural
arasinda `PA-DISC-NO-SCOPE-NARROW` da var — bugun onu uygulamam gerekti
(kapsam daraltma) ve omurgada gormedim, skili actigim icin biliyordum.
ONERI: cache'e hangi 6'nin secildiginin GEREKCESI yazilsin, ya da
"kapsam" ekseni de eklensin.

═══ 3) REFERENCE DOSYALARI ═══

ACMADIM AMA ACMALIYDIM — `discovery/references/gereksinim-sorulari.md`.
Bugun 14 soru urettim ve HEPSINI kendi muhakememle kurdum. O dosyada
"7 kategori + senaryo sorulari" var; acsaydim belki 15. soruyu da bulurdum.
⚠️ Ve ironi: kendi memory kaydimda (`preload-okumak-degil`) "discovery
yazarken §6 ZORUNLU" diye yaziyor. Kendi kaydimi uygulamadim.
ONERI: bu bende bir kusur, kanonda degil. Ama `discovery` akis adim 2'ye
"reference'i AC" ifadesi konabilir — su an "Soru üretme aleti:" diye
GECIYOR, emir kipi yok.

GOVDEDE OLMALI (reference'ta kaybolur) — bulamadim; B1-B9 ozeti govdede,
detayi reference'ta: bu dogru bolunme.

═══ 4) CELISKILER — BIR TANE BULDUM ═══

⚠️ `HANDOFF-SCREEN-ONLY` vs KANAL DUZENI CELISIYOR.
Kanon: "Handoff EKRANA basilir, dosyaya YAZILMAZ." Ama bu oturumun kanal
duzeni: "Ekrana yazdigin her seyi kanala da yaz" — ve kanal DOSYADIR
(JSON, diske yazilir, arsivlenir).
Bugun her handoff'u iki yere yazdim ve celiskiyi FARK ETMEDIM.
Kanon "docs/'a HANDOFF-*.md acma" derken kastettigi sey bu degil sanirim
ama LAFZI kanali da kapsiyor.
ONERI: `HANDOFF-SCREEN-ONLY` govdesine ayrim: "Yasak olan PROJE DOKUMANINA
(docs/) handoff dosyasi acmaktir; ileti kanali (kanal/outbox) dosya olsa da
EKRAN sayilir — orada handoff'un kopyasi durabilir."

DAL EKSIGI (T4 ile ayni sinif) — `CLICKUP-TASK-FIRST` "task olmadan is yok"
diyor. Bugun ClickUp KOTASI doldu ve HICBIR SEY yazilamadi.
Kural "task ac" diyor ama ACAMIYORSAN ne olacagini soylemiyor.
Ben repoya yazilmasini onerdim, Clara karar verdi — kanondan degil.
ONERI: "ClickUp erisilemezse (kota/arıza) kayit REPOYA yazilir ve erisim
gelince tasinir; 'sonra yazarim' YASAK."

⚠️ BULAMADIGIM: baska celiski aradim, bulamadim. Uc-dort saatlik bir
oturumun gordugu kadariyla — tarama degil, carpma listesi bu.
