# Ölçüm — denetlenmemiş commit boşluğu ve tek nokta arızası

**Tarih:** 2026-08-16 · **Bulan:** PQA (push kuyruğu ölçümü) · **Kayıt:** Clara

## Olay

PQA 18:33'te push kuyruğunu ölçtü ve **iki denetlenmemiş commit** buldu
(`e216917`, `95ea651`). Birini PAM commit'lemiş ve **iletmemişti.**

PAM'in kendi tespiti:

> *"Bu tam da bu sabah PQA'ya kendi yazdığım cümlenin ihlaliydi: 'iş kapandı sanılır,
> sonrasında atılan commit kimsenin listesine girmez ve sessizce push'a girer.'
> Doğru teşhisi koyup **aynı gün iki kez ihlal ettim.**"*

## Sebep — kural dar yazılmış

`ISD-RETURN-TO-PLANNER` *"kendi belgemi commit'leyip iletirim"* diyor. **Başka
commit'ler için özne yok.** PCA'nın bulgusu PAM'in *"belgesi"* değildi — ama commit'i
PAM attı.

Yani kural bir **sahiplik** tanımına dayanıyor ve sahipliği belirsiz commit'ler
boşluktan geçiyor.

## ⚠️ PQA'nın asıl bulgusu — tek nokta arızası

> *"Bu boşluk bugün **üç commit'ten** geçti ve üçü de **farklı yoldan** yakalandı — biri
> devir bloğunda dolaylı geçti, ikisi benim kapsam ölçümümle çıktı. Yani yakalanma
> yöntemi her seferinde başkaydı, yani **tekrarlanabilir bir kapı yok.**
>
> Kapıyı şu an `PQA-GATE-BEFORE-PUSH` tutuyor ve o benim tarafımda. Ama bir kapının tek
> tarafta olması onu **TEK NOKTA ARIZASI** yapar: **ben ölçmezsem kimse ölçmez.**"*

### Neden bu ciddi

Denetçinin arızası bugün ayrıca ölçüldü (`2026-08-14-gonderilmeyen-mesaj-arizasi.md`):
gönderilmemiş bir bulgu ile hiç bulunmamış bir bulgu **dışarıdan aynı görünür.**

İkisi birleşince: PQA ölçmezse denetlenmemiş commit push'a girer, **ve bu görünmez.**

## Durum — kural yazılmadı

PQA bunu **bulgu yazmadı**, doğru davrandı: kanon boşluğu, o turun ürünü değil.

**Bir sonraki kanon işinin adayı.** Ölçülmesi gereken: kapı ikinci bir tarafta nasıl
kurulur — yoksa sahiplik tanımı mı genişletilir (*"attığın her commit'i iletirsin"*)?

## Yan kayıt — PAM dersi hemen uyguladı

`36eceb1`'i atarken **iletti**, sonradan hatırlamadı. Aynı turda düzeltme.

---

## Dördüncü işleyiş — ve ilk kez onay kapısına kadar geldi (18:48)

PAM toplu onayı **sekiz commit** diye sundu. Clara ölçtü: **dokuz.** Arada `36e5e55`
(PAD memory) eklenmişti — **ve o commit denetlenmemişti.**

Yani onay *"hepsi denetlendi"* varsayımıyla gidiyordu ve varsayım yanlıştı. Ölçülmeseydi
**denetlenmemiş bir commit push'a girecekti.**

Boşluk bugün **dört kez** işledi ve dördü de **farklı elden** yakalandı:

| # | Nasıl yakalandı |
|---|---|
| 1 | devir bloğunda dolaylı geçti — **şans** |
| 2, 3 | PQA'nın kapsam ölçümü |
| 4 | **Clara'nın onay öncesi ölçümü** |

**Sıfır tekrarlanabilir kapı.** Her seferinde başka bir yöntem tuttu.

## ⚠️ PQA kendi kapısının sınırını ilan etti

> *"18:44'te sana 'sekiz commit, kapı açık' dedim. **O an doğruydu.** 18:45'te dokuzuncusu
> geldi ve **ben fark etmedim** — çünkü kapımı **push anında** açıyorum, onay beklerken
> değil. Kapımın tasarımı bu ve bugün işe yaradı, ama 'kapı açık' dediğim anla push anı
> arasındaki boşlukta commit girebiliyor.
>
> Bunu bilerek söylüyorum: benim **'kapı açık' beyanım bir ZAMAN DAMGASI taşıyor** ve o
> damgadan sonrası **kapsam dışı.**"*

Bu bir bulgu değil, **bir sistem tarifi** — denetçinin kendi kapsamının sınırını ilan
etmesi. Ve bugünün en olgun çıktısı.

### Ortaya çıkan yapı

```
PQA "kapı açık" der  →  [ BOŞLUK ]  →  onay gelir  →  PQA push anında yeniden ölçer
                          ↑
                    commit girebilir
```

Kapı push anında **kapanıyor** (PQA-GATE-BEFORE-PUSH doğru çalışıyor). Ama *"kapı açık"*
beyanı ile push arasındaki pencerede giren commit **onay kapsamına sızıyor** — çünkü
onayı veren kişi eski sayıya bakıyor.

**Bugün bu pencereyi Clara'nın ölçümü kapattı.** Ama o bir kural değil, bir refleksti.

## Gereksinim adayının gerekçesi — dördüncü kez güçlendi

Ölçülmesi gereken iki soru:

1. Kapı ikinci bir tarafta nasıl kurulur (tek nokta arızası kalkar mı)?
2. *"Kapı açık"* beyanına **zaman damgası + commit hash'i** eklenirse pencere kapanır mı?
   (Onayı veren, beyanın hangi HEAD'e ait olduğunu görür.)

İkincisi ucuz görünüyor ama **ölçülmedi** — öneri değil, aday.
