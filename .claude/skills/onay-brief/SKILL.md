---
name: onay-brief
description: Mert'e onay için iş sunma biçimi — üç blok (şu an ne oluyor / nasıl çözüyorum / nereye dokunuyor) + üç kapanış satırı, ve alan listesinin işe göre nasıl türetildiği. Bu skill'i Mert'ten bir işe onay istenecekte aç: bir plan sunulacakta, "şunu yapayım mı", "başlayalım mı", "onayını bekliyorum" denecekte, bir işe başlamadan önce kapsamı gösterilecekte ya da yönetim modunda ona durum brief'i verilecekte. Kapsam dışı — başka bir agent'a iş devri (o devir bloğu, kanonda), ve ölçüm sonucunu raporlamak (brief onay ister, rapor bilgi verir).
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

---

**Kalıbın nasıl bulunduğu, tutmayan üç deneme ve Mert'in ham cümleleri:**
`konular/saha-yonetimi/incelemeler/pa-davranis-senaryolari/RAPOR.md`
