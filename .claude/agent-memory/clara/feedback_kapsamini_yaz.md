---
name: kapsamini-yaz
description: Bir ölçüm yaparken neye BAKMADIĞINI da yaz — dar kapsam yanlış değil, yazılmamış kapsam yanlış; DÖRT kez ölçüldü ve dördüncüsünde kural elimde olduğu hâlde ihlal edildi
metadata:
  type: feedback
---

Bir ölçüm sunarken **neye bakmadığını** da yaz. Dar kapsam bir hata değil;
**yazılmamış** kapsam hatadır.

**Why:** 2026-08-08'de bu üç kez ölçüldü ve üçünde de kapsamı yazmak bir sonraki
ölçümü mümkün kıldı.

Clara index atıflarını taradı ve yazdı: *"yalnız ilk 40 satırı (not bölümü)
taradım, GÖVDELERİ TARAMADIM."* PAD sonra 69 dosyanın tam gövdesini taradı.

- **Birinci turda** geniş tarama bir şey çıkarmadı — dar kapsam yeterliymiş.
- **İkinci turda iki yeni atıf çıkardı** — dar kapsam yetersizmiş.

PAD'in cümlesi: *"kapsamını yazmış olması bu ölçümü mümkün kıldı; yazmasaydı
'tarandı' der geçerdik ve iki atıf sessizce eksik kalırdı."*

Ve tersi de doğru: PAD kendi ilk ölçümünün kapsamının dar olduğunu **kendisi
buldu** (madde 8'de cascade durumu hiç sorulmamıştı) — çünkü sekiz durumu tek
tek yazmıştı.

Bu `BHV-DATE-THE-MEASUREMENT`'ın Clara tarafındaki karşılığı: *"kapsamı
yazılmamış 'bulunamadı' bir beyandır, sonuç değil."*

**How to apply:** her ölçüm sonucunun sonuna iki satır: **ne ölçüldü** ve **neye
bakılmadı**. İkincisi olmadan bir sonraki ölçüm "bu zaten tarandı" diye
atlanır — ve atlandığı fark edilmez.

## ⚠️ DÖRDÜNCÜ VAKA — 2026-08-12, kural elimdeyken ihlal edildi

Cascade ölçümünde *"21 dosya"* dendi. **Ne** arandığı yazıldı (`status.md` /
`STATUS.md` / `TASK-STATUS`), **nerede** arandığı yazılmadı — kapsam
`.claude/skills/` idi, hiçbir yere geçmedi.

Sonra aynı hata iki kez daha, aynı zincirde:

```
21  Clara → dosya adı ekseni      (kapsam yazılmadı)
36  PAM   → kavram + adres ekseni (kapsam yazılmadı)
40  PAD   → agent body'leri       (KAPSAM YAZILDI → fark oradan görüldü)
```

**Zincir PAD'de kırıldı** çünkü o kapsamını yazdı: *"agent BODY'lerini de
taradım."*

PAM kendi payını buldu ve sınıfını doğru koydu: *"Kapsamımı `.claude/skills/`
ile sınırlı tuttum. Bu tek başına hata değil — hata **kapsamı yazmamak.**
Yazsaydım body boşluğu **ölçüm anında** görünürdü."*

**Bu vakanın öğrettiği yeni şey — maliyetin kime çıktığı:**

> Kapsamsız bir ölçüm, **sonraki ölçümcüyü de kör bırakır.**

Çünkü kapsam yazılmadığında okuyan onu *"her yer"* sanır; sonraki ölçümcü aynı
yerden başlamaz, orasının taranmış olduğunu sanır. Yani bedel ölçümü yapanın
değil, **ondan sonra gelenin** üstüne kalır.

**Ve asıl uyarı: kural elimdeydi ve yine ihlal edildi.** Bu kayıt üç vakayla
zaten açıktı. Demek ki sorun kuralın varlığında değil **tetiğinde** — kapsam,
ölçüm *bittiğinde* değil, sayı *ilk telaffuz edildiğinde* yazılmalı. Bir sayıyı
cümleye koyarken kapsamı da aynı cümleye koy; sonraya bırakılan hiç yazılmıyor.

İlgili: [[olcum-yerine-yorum]], [[maliyet-tahmini-olcum-degil]]
