# Arama disiplini — ölçümler

Bu dosya **kanıt** taşır: skill'deki kuralların hangi ölçümden çıktığı. Skill'den atıfla
çağrılır, kendiliğinden yüklenmez.

Ham kayıtlar: `incelemeler/qdrant-kayit-bicimi/kayit.md` ·
`kararlar/2026-08-06-arama-disiplini.md` · `gunluk/2026-08-06.md`

## Hız — grep vs vektör

**grep:** beş arama **0.041 saniye.**
**Vektör indeksleme:** aynı gövde için **~96 saniye.**

Yani vektör pahalı olan tarafta ve maliyeti indekslemede — arama anında değil.

## Vektörün tam kelimeyi bulamaması (2026-08-06)

*"preload arızası"* tam adıyla arandı. O ifadeyi taşıyan dosya **ilk beş sonuçta hiç
çıkmadı.** grep aynı aramada dosyayı doğrudan buldu.

**Sonucu:** bilinen bir kelime için vektör kullanılmaz.

## Skor aralığı — alakasız ile gerçek ayırt edilemiyor

```
alakasız soru ("2024 Formula 1 şampiyonu kim")   → 0.507
gerçek soru                                       → 0.564
aralık                                            → 0.057
```

787 kayıtlık koleksiyonda ölçüldü. Erken ölçümde (4 kayıt) aralık daha genişti —
koleksiyon büyüdükçe aralık **kapanıyor.**

**Ve MCP skoru hiç göstermiyor** — `qdrant-find` çıktısında skor alanı yok. Yani model
alakalıyı alakasızdan ayırt edemiyor, hepsini bağlam sanıyor.

**Somut vaka:** makarna tarifi soruldu (*"İtalyan mutfağında makarna pişirme süresi"*) ve
dört kanon notunun **hepsi** döndü. Ham skorlara `qdrant-client` ile bakıldığında motor
doğru davranıyordu — en yüksek 0.1565, yani matematiksel olarak alakasız. **Veri katmanı
sağlam, MCP katmanı bilgiyi kesiyor.**

## Kayıt biçimi — üç biçim, aynı 10 soru

```
yapısal blok (dosya olduğu gibi)     → 4/10
anlam birimi (konuya bölünmüş)       → 8/10
anlam birimi + özet eklenmiş         → 8/10 (skorlar DÜŞTÜ)
+ metadata (payload'da)              → 9/10
+ metadata (aranan metne yazılmış)   → 7/10
```

**Anlam birimine bölmek isabeti ikiye katladı.** Sebep: model **514 token**'da doyuyor;
9.692 karakterlik blokta bulgu eriyor.

**Aranan metne ek yazmak düşürüyor** — iki bağımsız kanıt (özet ekleme ve metadata'yı
metne yazma, ikisi de skorları düşürdü). Sinyal seyreltmesi.

## Filtre — 5/7 → 7/7 ama doğruyu yukarı çıkarmıyor

Kayıt türüne göre filtre uygulandığında isabet **5/7'den 7/7'ye** çıktı. Ama iki soruda
doğru cevap **zaten listedeydi, ikinci sıradaydı** — filtre üstündeki yanlışları kaldırdı,
doğruyu yukarı taşımadı.

**MCP filtre desteklemiyor:** `qdrant-find` yalnız `{collection_name, query}` alıyor.

## Tazelik körlüğü

Eskimiş etiketli bir kayıt, aynı konudaki taze kaydı **bastırdı:**

```
eskimiş kayıt → 0.670
taze kayıt    → 0.651
```

**Sonucu:** *"geçersiz"* bilgisi kaydın dışına (haritaya) yazılırsa vektör onu görmüyor.
Kaydın **içine** yazılmalı.

Ve ölçüm anında 797 kaydın **473'ü tarihsizdi** — yani çoğunluk için tazelik sorusu
sorulamıyordu.

## Koleksiyon envanteri (2026-08-06)

43 koleksiyon vardı, **26'sı ölü:** 18 tek notluk, 8 tamamen boş. Ekip için açılmış
kutuların çoğu hiç kullanılmamış.

`COLLECTION_NAME` `.mcp.json`'da **tanımsız** — yani kutu adını her çağrıda model
veriyor. İki oturum farklı ad yazarsa notlar iki kutuya dağılır ve hiçbiri diğerinden
aranmaz.
