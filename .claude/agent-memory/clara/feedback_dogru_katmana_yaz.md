---
name: dogru-katmana-yaz
description: Bir skill güncellenirken kaynağı kopyalama tuzağı — sorun uzunluk değil kapsam; ayıran soru "bu satır burada mı yaşamalı yoksa buradan işaret mi edilmeli".
metadata:
  type: feedback
---

# Skill güncellenirken kaynak kopyalanmaz, işaret edilir

Bir skill yürürlükteki bir kaynağa (şablon, araç, dış doküman) dayanıyorsa, o kaynağın
içeriği skill'e **taşınmaz** — skill ona **götürür.**

**Why:** 2026-08-07'de `kanal-kurulumu` skill'i v3'e güncellenirken şablonun 662 satırı
neredeyse birebir SKILL.md'ye taşındı, dosya **688 satır** oldu. Kısaltma ölçüm
anlatılarını budayarak denendi ve **işe yaramadı** (681). Sebep kısalık değil
**kapsam**dı: şablon zaten yürürlükteki kaynak, skill'in işi onu kopyalamak değildi.
Kapsam düzeltilince 464'e indi — yani sorun cümlelerin uzunluğunda değil, **hangi
bilginin nerede yaşadığında**.

İkinci bedeli daha sinsi: kopyalanan kaynak zamanla **ayrışır.** İki yerde duran aynı
kural biri güncellenince yalan olur ve hangisinin yürürlükte olduğu belirsizleşir.

**How to apply:** Bir skill yazarken/güncellerken her bölüm için sor: **bu satır burada
mı yaşamalı, yoksa buradan işaret mi edilmeli?** Kaynak ayrımını skill'in başına yaz ki
sonraki tur da bilsin. `kanal-kurulumu`'nda kurulan ayrım:

```
dış kaynak (şablon)  NEDEN böyle · ölçüm gerekçeleri
dış kaynak (araçlar) NASIL yapılır · kendi kullanımını basıyor
skill                KİM ne yapar · rolün disiplini
references/          KANIT · hangi kural hangi ölçümden
```

Bu [[uc-katman-body-skill-reference]] kuralının bir alt hâli: orada *body / skill /
reference* ayrılıyor, burada **skill ile dış kaynak** ayrılıyor. Aynı test: bir satır iki
yerde duruyorsa biri fazladır.

Yan kural — **kural ile gerekçe ayrı ömürlü.** Aynı güncellemede çıktı: tek yazar kuralı
md düzeninde *veri bütünlüğü* kuralıydı, JSON düzeninde o gerekçe çürüdü (paylaşılan
dosya yok) ama kural geçerli kaldı — artık *atıf ve kimlik* kuralı. Bir düzen
değiştiğinde kuralların hangisinin **gerekçesi düştü** diye tek tek bakılır; yoksa ya
çürük gerekçe savunulur ya da geçerli kural atılır.
