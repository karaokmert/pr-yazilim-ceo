---
name: ekip-disi-sanma
description: Envanterde çıkan bir isim/branch "dış taraf" varsayılmaz — rol ölçülür, çıkarılmaz (Mert 3 kez düzeltti, 2026-08-11)
metadata:
  type: feedback
---

Bir envanterde, `git log`'da ya da bir kayıtta çıkan **isim veya branch için rol
uydurulmaz.** "Bu kim, ekipte mi, ne yapıyor" sorusu **sorulur.**

**Why:** 2026-08-11'de Goat'ta Buse'nin branch'indeki on commit *"sprint dışı"*
diye çerçevelendi — *"kapsam genişler"*, *"ayrı planlamaya kalsın"* denildi ve
Mert'e **kapsam kararı** olarak sunuldu. Oysa Buse **ekipte**: Goat'ın FE
işlerinin bir bölümünü yapıyor, işini bitirip Mert'e yollamıştı. Branch bir
"mock kaynağı" değil, **teslim edilmiş iş.**

Mert üç kez düzeltti. Üçüncüsünde tam tarifi verdi ve amacı söyledi: *"bu
Buse'nin yaptığı işi 2. göz olarak incelememiz anlamına gelir."*

Hatanın mekaniği: `git log` çıktısındaki bir branch adından **rol** çıkarıldı.
Rol çıkarımı ölçüm değil, **tahmin** — ve tahmin edilen rol yanlışsa bütün
çerçeve yanlış kurulur. "Sprint dışı" etiketi bir işi kapsam dışına atar; o iş
aslında **incelenmesi gereken teslim** ise, etiket işi görünmez yapar.

**How to apply:** bir isim/branch/kayıt karşına çıktığında ve rolü belli
değilse — *"bu kim ve ne yapıyor"* diye **sor.** İki sinyal yeterli değil:
bir branch adının "mock" içermesi onun bir prototip olduğunu göstermez, ve bir
commit'in bizim task listemizde olmaması onun **sprint dışı** olduğunu
göstermez — yalnız **bizim listemizde olmadığını** gösterir.

Ayıran soru: **bu işi kimin yaptığını ÖLÇTÜM mü, yoksa dosyadan mı çıkardım?**

Bkz. [[olcum-yerine-yorum]] — aynı sınıf hata, farklı yüzey.
Bkz. [[hatirladigim-kayittir]] — kafadaki hazır çerçeve de bir kayıttır.
