---
name: onay-brief
description: Mert'e onay için iş sunma ve ONA SORU SORMA biçimi — üç blok brief (şu an ne oluyor / nasıl çözüyorum / nereye dokunuyor) ve her sorunun önüne açıklama koyma kuralı (önce ne okudum-ne gördüm-çelişki nerede, sonra AskUserQuestion). Bu skill'i Mert'e BİR SORU SORULACAK ya da ONAY İSTENECEK her durumda aç: bir karar sorulacakta, seçenek sunulacakta, "şunu yapayım mı", "başlayalım mı", "hangisi olsun", "onayını bekliyorum" denecekte, bir plan sunulacakta, bir işe başlamadan önce kapsam gösterilecekte ya da yönetim modunda durum brief'i verilecekte. Kapsam dışı — başka bir agent'a iş devri (o devir bloğu, kanonda), ve ölçüm sonucunu raporlamak (brief onay ister, rapor bilgi verir).
---

# Onay brief'i

Bu, **Mert'e** onay için sunulan işin biçimi. Devir bloğundan ayrıdır: orada hedef bir
agent, burada **karar veren bir insan.**

Mert'in kararı: **tüm agent'lar dahil, ona sunulan her iş brief'i bu yapıda olur.**
Sebebi kendi cümlesi — *"bu şekilde olması benim kararımı kolaylaştırır."*

## Yapı

Her iş kalemi **üç blok**, bu sırayla:

```
ŞU AN NE OLUYOR   → mevcut durum ve neden yanlış
NASIL ÇÖZÜYORUM   → akış, adım adım (→ ile zincir)
NEREYE DOKUNUYOR  → sabit alanlar, BOŞ OLANLAR DA YAZILIR
```

Sonda üç satır:

```
NEYE DOKUNMUYORUM : dokunulmayan yerler tek tek
EN ÖNEMLİ SINIR   : bu işi yıkabilecek tek şey
AÇIK KARAR        : yok / var · SÜRE: {tahmin}
```

## Üçüncü blok — alanlar türetilir, ezberlenmez

Tek bir soruyu cevaplar: **kim nereye dokunuyor?** Alanlar işin türüne göre değişir,
çünkü herkes başka bir şeye dokunuyor — ama soru ve mantık aynı kalır:

```
backend      → hangi handler · hangi DataLayer · cache · tablo · emsal
frontend     → hangi component · hangi hook · state · stil · emsal
agent üreten → hangi agent body · hangi skill · reference · hook · index
kural yazan  → hangi kural kimliği · hangi katman · cascade · index
ölçüm yapan  → ne ölçüldü · yöntem · kanıt nerede · neyi çürütüyor
kanal işi    → hangi kutu · kim yazar · monitör · kanon etkisi
```

Yani liste ezberlenmez: *"benim işim neye dokunuyor"* sorusunun cevabı ne ise o satırlar
yazılır.

## Boş olanlar da yazılır

*"Tablo: DEĞİŞMİYOR"*, *"Kanon etkisi: yok"* — boş bırakmak **"atladı mı, gerekmiyor
mu"** sorusunu doğuruyor. Yazılmış bir *"yok"* bir karardır; yazılmamış olan bir
boşluktur.

## Teknik terim değil teknik AKIŞ

Bu kalıbın en pahalı dersi ve **ters yönde** öğrenildi: üç denemede teknik detay
**çıkarıldı**, oysa Mert daha fazlasını istiyordu — *"teknik olmasın tabii ki, ama
akışsal da anlatsın istiyorum."*

> terim: *"tek projeksiyonlu sorgu + bellekte eşleştirme"*
> akış: *"mesajlar okunur → ID'ler çıkarılır → güncel bilgi tek sorguda alınır →
> bellekte birleştirilir"*

İkincisi anlaşılıyor **ve aktarılabiliyor.**

## Ölçüm anlatısı girmez — sonuç girer

*"Kaçan link 0, masum engel 100'de 3"* girer; o sayıya nasıl varıldığı **sorulunca**
verilir. Brief onay içindir, kendini anlatmak için değil.

## Kabul ölçütü

Mert'in kendi testi: ***"başka biri bana bu modülü nasıl yaptın dese anlatabiliyor
muyum?"***

Brief bunu sağlamıyorsa yetersizdir — çünkü iki işi birden yapar: onay almak **ve**
Mert'i işin sahibi hâline getirmek.

## Onay `AskUserQuestion` ile istenir

Metinle değil. Metin olarak *"onayını bekliyorum"* demek atlanabiliyor; araçla sorulunca
kapı tık olmadan geçmiyor.

## İKİ ARAÇ ÇAĞRISI — açıklama da araçla, onay da araçla

Mert'in kuralı (2026-08-16): *"Sorularını önce açıklama yaparak, sonra AskUserQuestion'ı
kullanarak yürütmemiz gerekiyor — bu önemli bir kural Clara."* Ve aynı oturumda:
***"her seferinde böyle ilerle."***

**Sertleştirildi (2026-08-17):** *"Question bölümünde yapılan açıklamanın öncelikle ask
tool'u ile anlatılması, sonrasında yine ask tool'u ile onay alınması gerekiyor."*

**Sıra — İKİ `AskUserQuestion` çağrısı:**

```
1. AÇIKLAMA ÇAĞRISI   → question gövdesinde tam açıklama
                         (ne okudum · ne gördüm · çelişki nerede)
                         seçenekler: "Anladım, devam" / "Şu eksik" gibi

2. KARAR ÇAĞRISI      → asıl soru, seçenekler ve her birinin sonucu
```

⚠️ **Neden düz metin yetmiyor:** düz metin açıklama **atlanabiliyor** — okuyucu kutuya
atlayıp seçeneklere bakabiliyor. Araçla sorulunca **kapı tık olmadan geçmiyor.** Onayı
araçla isteme gerekçesinin aynısı; açıklama da bir kapıdır.

**Birinci çağrının biçimi:** açıklama `question` alanının **gövdesinde** durur (uzun
olabilir), seçenekler yalnız kapıyı açar — *"Anladım, devam"* · *"Şu eksik"* ·
*"Yanlış anladın"*. Bu üçüncüsü değerlidir: yanlış çerçeveledim mi, orada düzeltilir.

⚠️ **Ve bu yalnız Clara'nın kuralı değil** — Mert'in ifadesi: *"sen dahil fabrika, özel
yazılım, websitesi agent'ları birebir öğrenmek zorunda."* Üç kanalın hepsinde geçerli.

Açıklamada üç şey olur, bu sırayla:

| | |
|---|---|
| **Ne okudum** | Hangi dosya, hangi satır, hangi cümle — kaynağı adıyla |
| **Ne gördüm** | Bugünkü kanonda ne yazıyor, alıntısıyla |
| **Çelişki nerede** | İkisi neden çatışıyor, ve bu bir *mekanik* sorun mu *tercih* sorunu mu |

### Neden açıklama önce gelir

**Soru tek başına kararı taşıyamaz.** Seçenek metinleri kısadır (bir-iki cümle) ve bir
kararın dayanağı oraya sığmaz. Açıklama olmadan Mert seçeneklere bakıp *"bu ne demek"*
diye sormak zorunda kalıyor — yani soru bir tur kaybettiriyor.

Ve daha sinsi bir zararı var: **açıklamasız soru, sorunun kendisini gizler.** Üç seçenek
sunmak "burada bir karar var" demek; ama *neden* karar gerektiğini göstermiyorsa Mert
seçeneği değil, benim çerçevemi onaylamış oluyor.

### Ayıran test

**Mert bu kutuyu okumadan önceki paragrafı okumasa, kararı verebilir miydi?**

Verebiliyorsa açıklama gereksizdi — soru zaten kendi kendine yetiyordu.
Veremiyorsa açıklama zorunlu, ve atlanırsa karar eksik bilgiyle veriliyor.

### Açıklama ne DEĞİLDİR

**Özet değil.** Mert'in kendi söylediğini ona geri anlatmak açıklama değil gürültüdür.

**Anlatı değil.** Hangi grep'i çektiğim, kaç dosya açtığım oraya girmez — girecek olan
**bulgu**, bulguya nasıl varıldığı değil. (Bir sayı verirken neyi saydığımı söylemek
bunun dışında; o dayanaktır.)

**Savunma değil.** Kendi tercihimi öne çıkaran bir açıklama seçenekleri kâğıt üstünde
bırakır. Tercihim varsa seçeneğin *içinde* "(Önerilen)" olarak durur, açıklamada değil.

### Kutunun kendisi

Açıklamadan sonra gelen soru `AskUserQuestion` ile sorulur — ya da tek bir soru varsa
`★ Question` kutusuyla. İkisi de aynı kuralı taşır: **başlık zorunlu, gövde kendi
kendine yeter, turda bir soru.**

---

**Kalıbın nasıl bulunduğu, tutmayan üç deneme ve Mert'in ham cümleleri:**
`konular/saha-yonetimi/incelemeler/pa-davranis-senaryolari/RAPOR.md`
