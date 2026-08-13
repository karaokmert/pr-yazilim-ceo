# CA | 2026-08-13 00:57:56

MEMORY DENETIMI — code-auditor raporu

═══ SAYILAR ═══
· Denetlenen kayit: 24 dosya + index (25 dosya -> 26 oldu)
· Index: 33 satir -> 35 satir (+2). Siserek degil, iki POINTER eklendi.
· Yeni dosya acilan: 1 · VAR OLANA eklenen: 3 (yeni dosya acmamak icin once
  "eklenebilir mi" diye baktim — uc kez evet cikti)
· Celiski bulunan: 0 (asagida gerekcesi)
· Silinen/budanan: 0 (bayat kayit cikmadi — dogruladim, iddia etmedim)

═══ 1) SKILL UYUMU — TEMIZ ═══
· Mesru icerik turleri: tum kayitlar tur #4 (ders/deneyim) ve #5 (hata+kazanim);
  bir tanesi #7 (skill-oneri). Uyumlu.
· MEMORY-RIGHT-LAYER: skilde yasamasi gereken bir kural memory'ye kopyalanmis MI
  diye tarandi -> HAYIR. Kayitlar kural METNI degil, kuralin UYGULAMA tuzagini
  tasiyor (mesru fark).
· Index SAF: her satir tek satir pointer, kural govdesi yok. MEMORY-INDEX-ONLY OK.
· MEMORY-NO-ORPHAN: 24 dosyanin 24'u de referansli (21 index, 3 kapanis-index).
  Yetim YOK — tek tek dogrulandi, goz kararı degil.
· Uc kademe korunmus: MEMORY.md -> kapanis-index.md -> kapanis notu
  (KAPANIS-INDEX-POINTER OK).

═══ 2) KANON CELISKISI — BULAMADIM (ve bunu OLCEREK soyluyorum) ═══
Celiski aramak icin en riskli kaydi sectim: kapanis_goat-search-indexing (uc somut
IDDIA tasiyor). Ucunu de goat reposunda kosturdum:
· ".gitignore 61-63 analiz ciktilarini yutuyor" -> DOGRU (satirlar yerinde)
· "iki ANALIZ raporu commit'lenemiyor" -> DOGRU (git check-ignore ikisini de
  .gitignore:62'ye baglıyor)
· "BACKEND-BORC.md tracked, bulgular orada yasiyor" -> DOGRU (git ls-files teyit)
Yani kayit BAYAT DEGIL, hala CANLI ve bulgu hala SAHIPSIZ.
Diger kayitlar kanonla celismiyor; hepsi kanonun UYGULAMA tarafini kesiyor.
NOT: "celiski yok" demek kolaydi; en kirilgan kaydi olcup soyluyorum.

═══ 3+4) EKLENENLER ═══
A) VAR OLANA EKLENDI (yeni dosya ACILMADI):
1. ders_is-dili-veri-modeli-farki <- bugunku DAR-KANCA dersi.
   "Kancayi veri akisindan sabitle" kuralini BILEREK uyguladim ve yine eksik
   taradim: kancayi duzeltmenin SOZDIZIMINE (startsWith) daralttim, "===" varyantini
   sayip icine bakmadim -> dorduncu menuyu kacirdim.
   Eklenen kural: "kanca dogru mu" ile "kanca genis mi" AYRI kararlar; saydigin
   ama acmadigin sayi rapora girmez.
2. ders_makine-karsilastirma-ikinci-kanit <- BOZUK METRIK sinifi.
   Ailenin ucuncu yuzu: arac calisir, sayi uretir, YANLIS SEYI olcer (ClickUp'ta
   ayni adli iki alan; ve iki revize turu gecen isin 1 dk gorunmesi).
3. ders_lsp-sessiz-sifir <- "LSP ARACI HIC YOKSA" dali.
   Kanonda tanimsiz oldugunu olctum (0 eslesme). Kilitlenmemek icin uc adim +
   serh zorunlulugu yazildi.

B) YENI DOSYA (1 adet): ders_ciktinin-kalici-evi.md
   Gerekce: mevcut ders_ciktim-ignore-edilen-yola-yazilabilir IKINCI kayip
   noktasini anlatiyor (ignore). Bu yeni kayit BIRINCI kayip noktasini anlatiyor
   (kalici kayit adiminin hic olmamasi). Ayri sebep, ayri cozum -> ayri dosya.
   Ikisi birbirine link'li.

C) TERFI ADAYI ISARETLENDI: [skill-oneri] Denetim ciktisinin kalici evi.
   Esik: kendi kanonuma gore >=3 bagimsiz noktada tekrar = yapisal bosluk.
   Bugun CA+BE+QA ayni gun bagimsiz buldu -> esik ASILDI, AG sinyali.

D) EKLEMEDIGIM (bilerek): CA-NO-DIRECTIVE / CODE-NO-WRITE gibi kimlik kurallarini
   memory'ye YAZMADIM. Sebep MEMORY-POINTER-ONLY: kural METNI kopyalanirsa skil
   degisince memory yalan soyler. Omurgam zaten HER oturumda yuklu — kopyalamak
   koruma eklemez, cift kaynak yaratir. Gorev 3'un olcutunu ("atlarsam bozulur mu")
   bu yuzden "kanonun SOYLEMEDIGI ama her isimde carpan sey" diye uyguladim.

═══ ⚠️ SANA SORMAK ISTEDIGIM (2 kalem) ═══
1. KAPANIS NOTLARI: uc acik kapanis var (liston, goat-agustos, goat-search-indexing).
   Kanonum "devralinan kapanis notu temizlenir" diyor (KAPANIS-DEVRAL-TEMIZLE) ama
   ucu de HENUZ DEVRALINMADI (PA karari bekliyorlar). Dokunmadim — dogru mu?
   Bunlar bekledigi kararlari alirsa temizlenmeli; karar bende degil.
2. BUGUNKU OTURUM icin kapanis notu ACMADIM. Sebep: yarim is yok, devredilecek
   durum yok (sinama bitti, ders kayitlari zaten yazildi). Kanonum "devredilecek
   yarim is YOKSA yazilmaz" diyor. Ama sen sabaha kadar calisiyorsun ve baska
   agentlara sirayla gececeksin — bu oturumdan devredilmesi gereken bir sey
   gorursen soyle, acarim.

BEKLEDIGIM: Yukaridaki iki soruya yanit (ozellikle 1 — kapanis notlarina
dokunayim mi). Is bitti, memory yazildi.
