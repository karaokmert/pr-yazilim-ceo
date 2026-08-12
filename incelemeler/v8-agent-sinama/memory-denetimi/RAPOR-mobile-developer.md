# mobile-developer | 2026-08-13 00:51:37

MB -> Clara | MEMORY DENETIMI RAPORU (4 madde tamam)

DENETLENEN: 4 kayit + index. Hepsi ground-truth ile osinif kodunda dogrulandi
(kanon MEMORY-GROUND-TRUTH okuma tarafi). Acilan skiller: memory-management,
style-mobile (+mekanik), enum-sync, state-mobile (+mekanik), data-access-mobile.

1) SKILL UYGUNLUK
· Mesru icerik turleri: 4/4 uygun (2 feedback=ders, 2 project=osinif durumu).
· MEMORY-RIGHT-LAYER ihlali: YOK. Skil'de olmasi gereken kural memory'ye yazilmamis;
  kayitlar skilin SESSIZ kaldigi tuzaklari tutuyor — memory'nin mesru isi.
· Index SAF pointer: evet, icerik tasimiyor.
· Bayat kayit: 1 bulundu (asagida).

2) KANON CELISKISI — 1 BULGU, DUZELTILDI
· mb-emsal-vs-kanon-catismasi: kayit "NativeWind/inline style catismasi COZULMEDI,
  AG'ye raporla" diyordu. GERCEK: style-mobile MB-STYLE-STYLESHEET + mekanik reference
  bunu KARARA BAGLAMIS — "mevcut NativeWind projesi korunur, className ihlal DEGIL;
  yeni projede kurulum yasak". Yani cozulmus bir catismayi ben hala acik saniyordum
  → sonraki oturumda AG'ye gurultu raporlardim.
· Sayim (osinif/src/mobile-student): className=472, nativewind 4.2.1 KURULU,
  inline style={{=47, StyleSheet.create=9 dosya. Kaydimdaki "40 inline" olgusu dogru
  ama CERCEVESI yanlisti.
· YAPILAN: kayit duzeltildi — ground-truth sayimi eklendi, "raporlamadan ONCE skilin
  mekanik reference'ini ac, cozulmus mu bak" adimi 1. sira yapildi. Silmedim: geriye
  kalan gercek drift var (STATIK inline obje hala kanon disi, className degil — ikisi
  karistirilmasin diye ayrimi yazdim).
· Diger 3 kayitta celiski YOK. Not: fail-open kaydindaki "BE enum'una client-ozel
  UNKNOWN ekleme" satiri enum-sync ENUM-CLIENT-COPY ile CELISMIYOR, onu tamamliyor.

3+4) YENI KAYIT — 1 DOSYA (ikisini BIRLESTIRDIM)
· mb-is-basi-refleks-karti.md — index'i sismemek icin madde 3 ve 4 tek dosyada;
  ikisi de ayni soruya cevap veriyor ("is baslarken elimde ne olmali").
· Icerik POINTER-ONLY (kural govdesi kopyalanmadi, MEMORY-POINTER-ONLY):
  - Her iste gecerli 7 kural (cross-platform/iPad, tsc --noEmit AYRI adim,
    test-oncesi, yalniz-kod-commit, models elle senkron, is sonu sirasi, kendi olayim)
  - Sessiz arizalar 4: provider SIRASI (derleme yakalamaz, gesture sessizce olur),
    zarf ag hatasini yutar (throw etmez — TestFlight arizasinin koku), dinamik query key,
    enum degeri proje-ozel
  - Refleksin YANLIS oldugu 5 yer: wizard adimi route degil, TanStack dogrudan import,
    sunucu verisi Context'e, emsalden hardcode tasima (+agent-yazimi emsal tuzagi),
    contract kilidi

INDEX: 6 satir -> 7 satir (+1). Yetim dosya yok (5/5 pointer'li). Limit 200, sorun yok.
DIGER GUNCELLEME: osinif-acik-kalemler'e "2026-08-13 dogrulandi, ucu de HALA ACIK"
satiri eklendi (AppVersionGate.tsx:19 duruyor, package-lock untracked, app.config yok)
— 13 gunluk kayda korlemesine guvenilmesin diye.

SANA SORUM (1 tane): Duzelttigim NativeWind catismasi bir AG sinyali olabilir —
kayit "AG'ye raporla" diyordu, ben skilde cozulmus buldum. Yani sistem DOGRU calismis
(catisma raporlanmis, AG karara baglamis, skile islenmis) AMA geri bildirim halkasi
kapanmamis: terfi olan kaydin memory'den DUSURULMESI gerekiyordu (MEMORY-PROPOSAL-BRIDGE
"terfi olunca sil" diyor). Bu bireysel benim atlamam mi, yoksa "AG bir oneriyi kabul
edince ilgili agent'a haber dusmuyor" diye yapisal bir bosluk mu — sence hangisi?
Yapisalsa AG'ye tasinacak bir bulgu olabilir.

Beklediğim: yukaridaki soruya gorusun; baska is varsa hazirim.
