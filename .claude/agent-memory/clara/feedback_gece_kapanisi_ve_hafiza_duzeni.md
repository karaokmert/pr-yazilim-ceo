---
name: gece-kapanisi-ve-hafiza-duzeni
description: Uzun/gece oturumu kapanırken kapanış dokümanı yazılır ve hafızaya tek satır düşer; project kayıtları iş bitince silinir — hafıza şişmez
metadata:
  type: feedback
---

Uzun bir oturum (özellikle Mert uyurken yürütülen gece işi) kapanırken **iki şey**
yapılır: kapanış dokümanı yazılır, ve hafızaya **tek satırlık** durum kaydı düşer.

**Why:** Mert'in kuralı, 2026-08-07: *"Gece görevlerinde kapanış dokümanı da yaz ki
sabah yeni session ile başlayabilelim. İlerlemeleri mutlaka hafızana al — yeni session
okuyarak başlayabilsin, sürekli context taşımayalım. Ama memory düzenini iyi yap ki
şişme olmasın."*

İki ihtiyaç birbiriyle çekişiyor: yeni oturum **bağlamı okuyarak** başlamalı ama hafıza
**şişmemeli.** Çözüm ikisini ayırmak — ayrıntı dosyada, işaret hafızada.

## Kapanış dokümanı — `gunluk/{tarih}-kapanis.md`

Bir oturumu kapatırken yazılır ve **yeni oturumun ilk okuyacağı şey** olur. Beş şey
taşır:

**Ne bitti** — ölçülmüş, denetlenmiş, commit'lenmiş olan. Commit hash'leriyle.
**Ne yarım kaldı** — nerede duruyor, kimde, ne bekliyor.
**Mert'in kararını bekleyen** — madde madde, her birinin ne olduğu ve neden onun kararı.
**Ölçüldü ama çözülmedi** — kayda geçmiş, iş açılmamış kalemler.
**Bir sonraki oturumun ilk hareketi** — tek cümle.

Ölçüt: **yeni oturum bu dosyayı okuyup çalışmaya başlayabilmeli.** Konuşma geçmişi
gerekmemeli.

## Hafızaya ne girer — tek satır, `project` tipinde

Kapanış dokümanının **adresi** ve **tek cümlelik durumu.** Ayrıntı değil.

```
Şu an nerede: {tek cümle} → {kapanış dokümanının yolu}
```

Sebep: hafıza her oturumda yükleniyor, kapanış dokümanı yalnız gerektiğinde okunuyor.
Ayrıntıyı hafızaya koymak her oturuma bedel yükler.

## Şişmeyi önleyen kural — `project` kayıtları GEÇİCİ

Ayrım tipe göre:

**`user` ve `feedback` kalıcıdır.** Mert'in nasıl çalıştığı, düzeltilmesi gereken bir
davranış, doğrulanmış bir yaklaşım — bunlar iş bitince değer kaybetmez.

**`project` GEÇİCİDİR.** İş bitince o kaydın değeri düşer ve **silinir** — ayrıntı
zaten günlükte ve `HARITA.md`'de duruyor.

Ölçüldü (2026-08-07): hafıza 23 dosya / 943 satırdı ve en büyük dosya
`project_sprint_3_kanal_kurulumu.md` (**149 satır**) — içeriğinin çoğu **bitmiş** işi
anlatıyordu. Üç `project` kaydı toplam 260 satır tutuyordu, yani hafızanın **%28'i**
tamamlanmış işlerin ayrıntısıydı.

**Ve bu kanonla çelişiyordu:** kanon *"iş hakkında olan dosyaya gider, sen/Mert
hakkında olan hafızaya"* diyor. Üç `project` kaydı o kuralın ihlaliydi.

## Kapanışta yapılacak temizlik

Bir iş bittiğinde ilgili `project` kaydı **silinir**, `MEMORY.md` satırı kaldırılır.
Yerine bırakılan şey: günlükteki kayıt + `HARITA.md` satırı + (varsa) `kararlar/`
dosyası.

**Ölçüt:** *bu kaydı silsem, iki ay sonra bir şeyi bilemez miyim?* Cevap hayırsa —
çünkü günlükte var — sil. Cevap evetse o kayıt `project` değil, `feedback` ya da
`user`; tipini düzelt.

**How to apply:** Oturum kapanırken sırayla — kapanış dokümanını yaz, bitmiş `project`
kayıtlarını sil, `MEMORY.md`'yi tek satıra indir, commit at.

İlgili: [[feedback_gunluk_kayit]] · [[feedback_indeks_emir_tasir]]
