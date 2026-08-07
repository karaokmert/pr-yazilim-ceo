---
name: kayit-kapanis-notu
description: Günlüğe yazılan bir açık bulgu kapandığında üstüne kapanış notu düşülür — bayat kayıt yanlış bulgu üretir
metadata:
  type: feedback
---

Günlüğe *"şu hâlâ yanlış"* diye yazılan bir bulgu **kapandığında**, o satırın
üstüne **kapanış notu** düşülür — tarih ve commit ile. Satır silinmez
(`ISD-APPEND-DONT-REWRITE` ekseni), üstüne yazılır.

**Why:** 2026-08-07'de PCA yetenek analizi yaparken buldu: günlükte *"`PCA-INDEX-
IS-A-START` hâlâ taramayla doğrula diyor"* yazıyordu. Dosyaya baktı — **artık
demiyordu**, aynı gün düzeltilmişti.

PCA'nın cümlesi: *"Günlük o anın fotoğrafı ve sonra kapanmış, ama günlükte
kapandığı yazmıyor. Ben bugün o satırı okuyup 'PCA'nın kuralı çelişkili' diye
bulgu yazabilirdim — dosyaya bakmasaydım."*

Yani **bayat kayıt yanlış bulgu üretir.** Ve bu, Clara'nın kendi ölçtüğü sorunun
aynısı: *"dört yazma tetiği var, sıfır kapanma tetiği"* — günlüğün kendisi de o
sınıfta.

**How to apply:** Bir bulgu kapandığında (commit atıldı, düzeltme doğrulandı) o
turda günlükteki satırı bul ve altına tek satır ekle:

```
> **KAPANDI (tarih, saat, commit):** ne düzeldi + neden bu not düşüldü
```

Ayıran soru: **bu satır bir DURUM mu bildiriyor, bir OLAY mı?** Durum
(*"şu an şöyle"*) kapanır ve kapanışı yazılmalı. Olay (*"şu oldu"*) kapanmaz,
dokunulmaz.

Aynı ders `BHV-DATE-THE-MEASUREMENT` ile aynı kökten: bir ölçüm tarihsizse ya da
kapanışı yazılmamışsa, okuyan onu **güncel** sanır.
