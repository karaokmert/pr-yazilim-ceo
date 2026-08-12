# SINAV 3 — code-auditor | 2026-08-12 23:39:37

SINAV 3 — SKILL HARITASI (skil ACMADAN, omurgamdaki is->skil eslemesinden)

═══ SEN-1) PA: "mevcut yapiya dokunuyor, etki analizi yap" + DISCOVERY ═══
ACACAKLARIM (sirayla):
1. impact-analysis — isin oz skili; kanca sabitleme, bagimlilik izleme, uc bolumlu
   ANALIZ ciktisi burada.
2. code-quality — tuketici SAYIMININ araci (CODE-COUNT-BY-LSP) + drift olcerken
   kullanacagim esikler burada, tek kaynak.
3. Dokundugum KATMANIN skili — kanca hangi katmana iniyorsa (database / backend /
   frontend / mobile / devops): sapma ilan etmek icin olcutu o katmanin kanonundan
   okumam gerek, hafizadan degil.
4. tasarim-prensipleri — uretici-tuketici sozlesmesi, sessiz-yutma gibi TUZAK
   ekseni; code-quality esik verir, bu muhakeme verir.
· proje-dosya-duzeni — ANALIZ ciktisinin nereye yazilacagi icin (T4'te bunun akis
  adimi olmadigini bulmustum; yine de acilmasi gereken yer burasi).
ACMAYACAKLARIM: structural-audit (tek degisim var, tum-proje taramasi degil) ·
module-audit (o QA'nin, skorlu per-modul denetim).

═══ SEN-2) Kullanici: "devralinan projeyi bastan tara, tum proje" ═══
ACACAKLARIM (sirayla):
1. structural-audit — birebir bu isin skili; modul modul tarama, drift
   siniflandirma, AUDIT-REPORT + remediation.
2. code-quality — sapmayi olcecegim esikler (boyut, DRY, magic, naming).
3. TUM ilgili katman skilleri — proje .NET+Next+RN ise database/backend/frontend/
   mobile: her katmanin kanonu ayri, sapma o kanona gore ilan edilir.
4. tasarim-prensipleri — yapisal tuzak ekseni.
· pr-yazilim-oy-envanteri (zaten yuklu) — referans proje seti + emsal-yazar
  haritasi; devralinan projede "bu emsal mi sapma mi" ayrimi icin.
ACMAYACAKLARIM: impact-analysis (tekil degisim yok) · proje-islemleri (o PA'nin
devralma skili, docs duzenini o kurar).

═══ SEN-3) QA: "bu degisiklik baska nereleri kirar?" (commit) ═══
ACACAKLARIM: SEN-1 ile AYNI SET — impact-analysis + code-quality + katman skili
(+ tasarim-prensipleri). Motor ayni, degisen sadece GIRDI: DISCOVERY yerine diff.
FARK (kural): reaktif tetikte cikti tetikleyene DE gider — PA'ya BILGI, QA'ya da
BILGI (CA-OUTPUT-TO-PA).
IHTIYAT: "kirar" fiili davranissal; ben etki YUZEYI veririm, kirilma garantisi
degil (CA-STATIC-NO-REPRO) — serh zorunlu.
ACMAYACAKLARIM: commit-review (o QA'nin inceleme skili; ben commit'i kapi olarak
degil kanca olarak okurum) · structural-audit.

═══ SEN-4) "Bir fonksiyonun kac yerden cagrildigini say, sayi karari belirliyor" ═══
ACACAGIM: code-quality — TEK skil yeter (CODE-COUNT-BY-LSP tek kaynak).
NEDEN: sayi karar veriyorsa arac LSP; grep tarama araci, karar araci degil.
Ve kural sayim yapmadan ONCE references/mekanik.md'yi acmami soyluyor (arac
tablosu + tuzaklar) — yani skil govdesi yetmez, referansini da acarim.
· EK (emin degilim, tahmin): C# ise LSP kullanimi icin ayrica bir alet skili
  gerekmez sanirim; arac harness tarafinda. Bunu kural olarak DEGIL tahmin
  olarak isaretliyorum.
ACMAYACAKLARIM: impact-analysis (bu tek basina bir olcum adimi; is etki analiziyse
zaten acik olur, sirf saymak icin acilmaz).

═══ SEN-5) "Buldugun sapmayi duzeltmek icin kod yaz" ═══
BU BENIM ISIM DEGIL. DURUYORUM.
Kod yazmam (CODE-NO-WRITE-ON-AUDIT), duzeltmenin nasil yapilacagini da soylemem
(CA-NO-DIRECTIVE). Sapmayi RAPORLARIM; tedavi ureten agentin.
GIDECEGI YER: PA -> developer (BE/FE/MB/UID; sapma hangi katmandaysa). Dogrudan
developer'a vermem, gorevlestirmem — koordinasyon PA'da (CA-OUTPUT-TO-PA).
Talimat geregi skil listesi YAZMIYORUM: reddettigim isin nasil yapilacagini
tarif etmek de direktif olurdu.

═══ OZ DEGERLENDIRME ═══
· Emindim: 4 senaryo (SEN-1, SEN-2, SEN-3, SEN-5) + SEN-4'un ana cevabi.
· Tahmin ettim / emin degilim: 2 nokta, ikisini de isaretledim —
  (a) SEN-4'te "LSP icin ayrica alet skili gerekmez" tahmini,
  (b) SEN-1/SEN-2'de tasarim-prensipleri'ni saymam: omurgamin alet cantasinda
      ADI GECMIYOR (orada 3 kalem var: impact-analysis / structural-audit /
      code-quality). Agent body'mde "code-quality + tasarim-prensipleri" birlikte
      anilir — oradan aliyorum. Yani haritada degil, body'de. Dogru olduguna
      inaniyorum ama kaynagi omurga haritasi DEGIL.
· Bilmiyordum: 0 uydurma. 76 skilin tamamini bilmiyorum; yukarida yalnizca
  varligindan emin oldugum adlari yazdim — emin olmadigim tek yer katman
  skillerinin TAM adlari (database/backend/frontend/mobile diye andim; alt
  skil adlari - ornegin module-development - is katmana inince acilir, ama
  hangisinin gerekecegini kanca belirler, simdiden sayamam).

BEKLEDIGIM: Yok.
