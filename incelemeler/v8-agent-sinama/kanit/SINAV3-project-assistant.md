# SINAV 3 — project-assistant | 2026-08-12 23:39:23

SINAV 3 — SKILL HARITASI. Skill ACMADIM.
(Not: `discovery` + `clickup` bu oturumda ZATEN acikti, context'imde duruyor.)

═══ SEN-1: "Hasta kayit ekrani" — mevcut projeye ekleniyor ═══

ACACAKLARIM (sirayla):
1. `clickup` — task var mi/acilacak mi; gereksinim ACIKLAMADA ve YORUMDA olabilir
2. `proje-dosya-duzeni` — modul dokumani nerede, discovery nereye yazilacak
3. `discovery` — asil is: gereksinimi is diline cevir, riskleri kapat, B1-B9 tara
4. `impact-analiz` — ⚠️ KRITIK: "mevcut projeye ekleniyor" dedin. Yeni yapi degil,
   var olana dokunuyor. Etki analizi CA'ya gider, koordinasyonu bu skilde.

ACMAYACAKLARIM:
· `project-planning` — o SIFIRDAN proje icin; burada proje zaten var
· `bug-triyaj` — hata yok, yeni is var

⚠️ SIRA NOTU: impact-analiz'i discovery'den SONRA yaziyorum. Kanonda
"discovery ONCE, CA SONRA" diye bir sira oldugunu hatirliyorum ama
kural adindan EMIN DEGILIM.

═══ SEN-2: Sifirdan yeni proje, buyuk resim ═══

ACACAKLARIM:
1. `project-planning` — tam bu is: kapsami platformlara bol (admin/mobil/web/API),
   modul kirilimi cikar, eksik on-dokumani soruyla ac
2. `proje-dosya-duzeni` — docs duzeni sifirdan kurulacak
3. `clickup` — task yapisi kurulacak (ama bu ADIM 3, once buyuk resim)

ACMAYACAKLARIM:
· `discovery` — HENUZ degil. Discovery MODUL bazli; once buyuk resim,
  modul kirilimi cikinca her modul icin ayri discovery gelir.
· `proje-islemleri` — o DEVRALINAN projeye ilk temas icin; bu SIFIRDAN.
  (Ikisi karisir, ayirdim.)

═══ SEN-3: "Panelde bir sayfa acilmiyor" ═══

ACACAKLARIM:
1. `bug-triyaj` — sikayeti islevsel parcalara ayirmak, hangi katmanin bozuldugunu
   bulmak, dogru kapiya yonlendirmek
2. `clickup` — bugfix task'i var mi/acilacak mi + `revise` statusundeyse
   comment'te sebep durur

MUHTEMELEN:
3. `impact-analiz` — YALNIZ derin/yayilan bir sey cikarsa (CA'ya gidecekse)

ACMAYACAKLARIM:
· `discovery` — bu yeni is degil, bozuk is
· Kok-neden teshisi bende DEGIL: kosturarak gorulecekse TE, derin statik CA.
  Ben parcalar, yonlendiririm.

═══ SEN-4: Devam eden projeye ilk temas, docs karisik ═══

ACACAKLARIM:
1. `proje-islemleri` — devralma + docs duzenini elden gecirme tam bu skilde
2. `proje-dosya-duzeni` — duzenin KANONU burada (proje-islemleri onu KULLANIR)
3. `clickup` — devralinan backlog'un gercek durumu; statuye guvenilmez,
   kod/git ile dogrulanir

⚠️ AMA ONCE: kendiliğimden BASLAMAM. Duzeni gorup "elden gecireyim" demek
yasak (`PA-NO-FORCED-FLOW` + proje-islemleri'nde ayri bir kural oldugunu
hatirliyorum, adindan emin degilim). Kullanicinin acik karari gerekir.

═══ SEN-5: "Sence nasil yapsak, ne dusunuyorsun" ═══

ACACAGIM: `danisma` — tek skil.

NEDEN: bu DANISMA, EYLEM degil. Konusurum, dokuman URETMEM, akis BASLATMAM.
Discovery acmak burada YANLIS olur — isin nasil yapilacagi netlesmeden
discovery acmak YANLIS GEREKSINIMI belgelemektir.

ACMAYACAKLARIM: `discovery` · `clickup` · `impact-analiz` — hicbiri.
Task bile acmam. Kullanici "tamam bunu yapalim" diye ACIK karar verirse
o zaman EYLEM'e gecerim ve discovery acilir.
⚠️ Ortuk ima yetmez — bunun ayri bir kural oldugunu hatirliyorum
(`PA-DANISMA-NO-AUTO-EXIT` gibi bir ad), adindan tam emin degilim.

═══ OZ DEGERLENDIRME ═══

Emin oldugum: 5/5 senaryoda hangi skilin ACILACAGINDAN eminim.
Tahmin ettigim: 3 KURAL ADI (impact sirasi · proje-islemleri self-trigger ·
  danisma auto-exit) — kuralin VARLIGINDAN eminim, ADINDAN degil. Isaretledim.
Bilmedigim: 76 skilin cogu. Ben yalniz KENDI alet cantami biliyorum
  (8-10 skil) + ortak cekirdek. Developer skillerini (backend, component,
  data-access...) ADIYLA taniyorum ama ICERIGINI bilmiyorum — zaten benim
  acmam gereken skiller degil.

⚠️ BIR SEY EKLEYEYIM: bes senaryonun HICBIRI rol disi degildi. "Rol disiysa
durdur" diye uyarmissin — o tuzagi aradim, bulamadim. Hepsi PA isi.
Yanlissa soyle.
