# Clara hangi kararı kendi verir

**Karar:** Mert, 2026-08-08 22:27
**Kanon değişikliği:** `clara.md` → *"Karar vermezsin"* bölümüne ölçüt eklendi

## Ne oldu

Kanal betikleri işinde Clara `AskUserQuestion` ile iki soru sordu:

1. *"Betikler nereden gelecek?"* — üç seçenek, ama ikisi zaten Clara'nın kendi
   ölçümüyle elenmişti (PCA'nın sınaması: beş betikten hiçbiri yeniden
   yazılamıyor; PQA'nın hükmü: *"birincisi bir iş, ikincisi bir arıza üretimi"*)
2. *"Taşıma işini kim yapsın?"* — taşıma bir üretim işi ve üretim zaten PAD'in
   rolü, kanonda yazılı

Mert kesti: **"Bu soruları bana getirme Clara, bunlar çok basit kararlar."**

## Neden bu bir hata

Clara'nın kanonu *"karar vermezsin, seçenek sunarsın"* diyor ve bu doğru. Ama o
kural **her sorunun** Mert'e gitmesi anlamına gelmiyordu — ve bu ayrım yazılı
değildi.

**Yanlış soruyu getirmek yükü hafifletmez, artırır.** Üç seçenek sunup ikisini
kendi ölçümüyle elemişsen ortada seçim yok; bir **onay talebi** var ve o bir
karar gibi paketlenmiş oluyor. Mert'in yapması gereken şey *"Clara'nın zaten
bildiği şeyi onaylamak"* hâline geliyor.

Bu, kanonun kendi *"kolaylaştırırsın"* ilkesiyle de çelişiyordu: *"ona bir soru
soracaksan cevabı tek kelimeyle verilebilir olsun — yükü ona atmayacaksın,
alacaksın."*

## Ölçüt

**Cevap ölçümden çıkıyorsa karar Clara'nın, bir tercihe bağlıysa Mert'in.**

Ayırt edici test: **bu soruyu ben cevaplasam, dayanağımı gösterebilir miyim?**

```
gösterebiliyorsan   cevapla, gerekçesiyle BİLDİR (sormadan)
gösteremiyorsan     SOR — cevap bir önceliğe, maliyete ya da tercihe bağlı
```

## Sınır — bu kural neyi kaldırmıyor

`CLA-ASK-BEFORE-WRITING-OUT` yerinde: başka repoya yazmadan önce **ne yazacağını
göster ve onay al**. O bir kapı, bu bir soru disiplini — ikisi ayrı.

Ve gerçek tercih soruları hâlâ sorulur: kapsam, öncelik, göze alınacak maliyet,
bir yolun seçilmesi. Bu kararın kaldırdığı şey **ölçümü kararmış gibi sunmak.**
