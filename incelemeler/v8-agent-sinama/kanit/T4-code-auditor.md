# T4 code-auditor | 2026-08-12 21:57:40

SINAMA T4 — kanon sapmasi avi (CA kendi kanonuna bakiyor)

Yontem: iddiayi olctum, hatirlamadim. Uc bulgunun UCU DE bugun FIILEN carptigim
noktalar — teorik tarama degil. Saglik testi yaptim (bilinen-var desen: 'CA-'
omurgada 5, impact-analysis'te 10 gecis -> grep calisiyor).

═══ S1) CELISKI ═══

BULGU-1: CODE-COUNT-BY-LSP'in "araci yoksa" hali tanimsiz — kural kendini
uygulanamaz kiliyor.
· Kural (code-quality:80): "Tuketici/referans SAYISI bir karari belirliyorsa
  sayiyi LSP verir; grep tarama-kesif aracidir, KARAR ARACI DEGIL."
· Ayni kural (satir 84): "sayi karar veriyorsa IKISI DE kosulur ... cozulmeden
  sayi RAPORLANMAZ."
· CARPTIGI YER (bugun, T3): LSP araci elimde YOKTU. Kurali harfiyen uygularsam
  tuketici sayisi raporlayamam -> ANALIZ'in (A) bolumu (etki yuzeyi, dokunma
  siniri) URETILEMEZ. Ama ayni kanon ANALIZ uretmemi ZORUNLU kiliyor
  (impact-analysis adim 5 + CA-TWO-WAY).
· Yani: "LSP olmadan sayi raporlama" ile "etki haritasi uret" ayni durumda
  carpisiyor. Ben ucuncu yolu KENDIM kurdum (grep + saglik testi + serhte
  "LSP kullanilmadi" ilani). Bu benim yorumum, kanonda yazili degil.
· OLCUM: "LSP yoksa / arac yoksa / erisilemiyorsa" ifadesi code-quality ve
  impact-analysis'te ARANDI -> 0 eslesme. Fallback tanimsiz.
· Not: satir 84 "teyitsiz sifir kanit degildir" diyor — yani tek-arac riskini
  BILIYOR, ama tek arac kaldiginda ne yapilacagini soylemiyor.

═══ S2) BOSLUK ═══

BULGU-2: ANALIZ ciktisinin kalici kayda gecmesi, akisin ADIMI DEGIL.
Dikkat — "kural yok" DEMIYORUM, olctum, kural VAR ama yeri yanlis:
· VAR: impact-analysis:65, "## Referans" basligi altinda: "ANALIZ dosyasi konumu
  (task-folder ara dosyasi, konsolidasyonda MODUL-BILGI'ye iner) ->
  proje-dosya-duzeni."
· SORUN: bu bir REFERANS satiri, akis adimi degil. Akis 6 adim ve olctum:
  adim 5 = "ANALIZ uret", adim 6 = "PA'ya BILGI ver". Ikisinin arasinda
  "NEREYE YAZ" adimi YOK. Cikti uretilir ve devredilir — kalici kayit adimi yok.
· Ustune: proje-dosya-duzeni benim preload listemde DEGIL (agent tanimi satir
  8-14: behavior/handoff/memory-management/is-akisi/oy-envanteri/code-auditor).
  Yani konumu soyleyen skil elimde yok, ona isaret eden satir da baglayici
  olmayan bir yerde duruyor.
· CARPTIGI YER (bugun): T3'te 6537 karakterlik ANALIZ urettim. KANALA yazdim.
  Kanal kapaninca o rapor kaybolur. Kanonum bunu yasaklamadi, cunku
  "nereye yazilir" akista sorulmuyor.
· BEHAVIOR-REFERENCE-NOT-AUTOLOADED bu boslugu buyutuyor: referans satirindaki
  atif ancak ACARSAM baglar; adim olsaydi atlanamazdi.
· NOT (kendi memory'mde ayni sinifin kaydi var): "ciktim ignore edilen yola
  yazilabilir" dersi — ANALIZ-/DOGRULAMA- desenli dosyalar .gitignore'da olabiliyor.
  Bugun goat'ta git status'te tam o desende 5 dosya gordum (baska agentlarin).
  Yani cikti kalici kayda gecse BILE ikinci bir sessiz kayip noktasi var.
  Bu ikisi birlesince: uretilen analizin kaybolmasi kural ihlali OLMADAN mumkun.

═══ S3) FAZLALIK / OLU KURAL ═══

BULGU-3: CA-TWO-WAY ile CA-NO-DIRECTIVE arasindaki sinir tanimsiz — iki kural
birbirinin uzerine biniyor. (T1'de de bunu isaretlemistim, bugun FIILEN carpti.)
· CA-TWO-WAY (omurga:35): "sistemde bu is icin kullanilabilecek yapi ZATEN var mi,
  sifirdan yapmak yerine duzenlenecek mevcut yapi" -> reuse ONERMEMI istiyor.
· CA-NO-DIRECTIVE (omurga): "Rapordaki hicbir satir 'su dosyaya su kodu yaz'
  olamaz ... NASIL duzeltilecegi developer'in karari."
· CARPTIGI YER (bugun, T3): PermissionWrapper bulgusunda "ayni dosyanin ustunde
  ayni sinifin uygulamasi zaten var" yazdim — ve arkasina PARANTEZ ACIP
  "kullanilmasini DAYATMIYORUM, varligini bildiriyorum; secim developer'in"
  eklemek zorunda kaldim. O parantezi kanon soyletmedi; ikisi arasinda kaldigim
  icin kendim urettim.
· Yani sinir kodda degil, agentin ihtiyatinda yasiyor. Ihtiyatli olmayan bir
  oturumda ayni cift, direktife kayar.
· "Bu satir olmasa ne yanlis yapardim" testi: CA-TWO-WAY olmasa reuse'u
  atlardim (yani OLU DEGIL, gerekli). Eksik olan kural degil, ARALARINDAKI SINIR.

═══ BULAMADIGIM / IDDIA ETMEDIGIM ═══
· Gercek OLU kural bulamadim. Omurgadaki 5 CA kuralinin 5'i de bugun tetiklendi
  (CA-NO-DIRECTIVE T2'de, CODE-NO-WRITE T2'de, CA-STATIC-NO-REPRO T3 serhinde,
  CA-OUTPUT-TO-PA T3 basliginda, CA-TWO-WAY T3 (A) bolumunde). Fazlalik YOK.
· Baska agentin kanonu hakkinda hukum vermiyorum. Bir sey GORDUM, isaretliyorum:
  S2'deki "uretilen cikti kalici kayda gecmiyor" sinifi sizin mesajiniza gore
  QA'da da yasanmis. Ayni sinif birden fazla rolde gorunuyorsa bu tekil agent
  sapmasi degil, cekirdek akis boslugu OLABILIR — ama olcmedim, onlarin isi.
  (Kanonumda bu tur tekrar >=3 rolde gorulurse AG sinyali sayilir.)

BEKLEDIGIM: Yok — uc sorunun cevabi teslim edildi. Bulgular AG'ye (fabrikaya)
gidecek malzemedir; ben fabrikaya gitmem, dokuman hazirlar beklerim.
