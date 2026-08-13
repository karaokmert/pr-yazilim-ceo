# Mert karar akışı

> Mert'in kararı bekleyen işlerin tek kapıdan, **tek tek** ve **sırayla**
> geçmesi için kurulan akış. Kuralları Mert 2026-08-13'te koydu.
> Kazanım ve uyarı biriktikçe buraya eklenir; olgunlaştığında skill'e çevrilir.

## Neden var

Karar talepleri birden fazla ağızdan, aynı anda, yarım bağlamla geliyordu.
Mert bir karara odaklanmışken ikincisi geliyor, ilkinin detayı sorulmadan
üçüncüsüne geçiliyordu. Sonuç: **hiçbir karar tam verilmiyor, hepsi yarım
kalıyor.**

Akışın çözdüğü şey hız değil, **karar kalitesi.** Bir karar tam verildiğinde
bir daha açılmıyor.

## Kural — beş madde

**1 — Kuyruk YALNIZ Clara'lardan beslenir.**
Mert'in kutusuna **sadece Clara'lar** yazar. Diğer agent'lar (PA/CA/QA/BE/FE/MB/
DO/TE/UID) Mert'e doğrudan soru soramaz — **kendi projesindeki Clara'ya** sorar.

O Clara **süzer**: cevabı kendi ölçümünden çıkıyorsa kendisi verir; gerçekten
Mert'in kararı olan şeyi merkez kuyruğa taşır.

**Neden:** her agent doğrudan sorunca kuyruk süzülmemiş talebi doluyor ve sıra
anlamını kaybediyor. Ölçüldü 2026-08-13: kural konduğu ilk dakikada dört agent
altı talep gönderdi, ikisi aynı soruydu.

## Zincir — iki yönde de aynı, atlanmaz

```
Mert  ←→  merkez Clara  ←→  proje Clara  ←→  agent (PA/CA/QA/BE/FE...)
```

**Merkez Clara agent'a iş VERMEZ.** Bir ölçüm gerekiyorsa işi **projenin
Clara'sına** verir; o Clara PA'ya (ya da ilgili agent'a) sorar, cevabı toplar,
merkeze getirir. Yukarı yönde süzme, aşağı yönde de aynı zincir.

**Neden atlanmıyor:** proje Clara'sı o projenin bağlamını taşıyor — hangi PA
hangi task'ta, ölçüm daha önce yapıldı mı, cevap kimde. Merkez bunu bilmiyor;
doğrudan sorunca yanlış agent'a ya da üç agent'a birden gidiyor.

Ölçüldü 2026-08-13, **iki hata üst üste aynı işte:** önce 17689 ölçümü Goat
Clara'ya yollandı ve Mert *"PA'ya sorulmalı"* dedi; bu **Clara PA'ya sorsun**
demekti, ama merkez doğrudan üç PA'ya birden yazdı. Mert kesti:
> *"Sen Clara'ya iş verirsin, agent'a değil. Clara PA'ya sorar."*

**2 — Kuyrukta beklerler. Sıra bozulmaz.**
Gelen talep sıraya girer ve **geliş sırasıyla** işlenir. Öncelik sıralaması
yapılmaz; sıra atlanmaz.

**3 — Bir karar yanıtlanmadan diğerine geçilmez.**
Mert 1. karara cevap verene kadar 2. karar Mert'e **gösterilmez**. Kuyrukta
kaç talep olduğu söylenebilir, içerikleri sunulmaz.

**4 — Detay istenirse getirilir, sonra devam edilir.**
Mert bir karar hakkında detay isterse Clara o detayı ölçer/getirir ve **aynı
kararın** üstünde kalır. Detay geldi diye sıradaki karara geçilmez —
o karar **kapanana kadar** oradadır.

**5 — Clara soru sorma modunda.**
Mert bu oturumda karar veriyor; Clara soru üreten değil, **karar taşıyan**
taraf. Kendi merakını sıraya sokmaz.

## Bir karar talebi nasıl olmalı

Kanaldan gelen her talep **kendi başına anlaşılır** olmalı — Mert yukarıyı
okumadan karar verebilmeli. Bağlam sorunun **içinde** olur, adres verilerek değil.

Eksik gelen talep Mert'e taşınmaz; **önce agent'la netleştirilir.**

## Kuyruk nasıl tutulur

Clara kuyruğu kendi kutusundan okur ve **görünür** tutar: kaçıncı sırada, kim
sordu, tek satırlık başlık. Mert *"sırada ne var"* dediğinde bu liste gösterilir —
**içerikleri değil, başlıkları.**

Bir karar kapandığında:
- kararın kendisi + gerekçesi `konular/{konu}/kararlar/` altına yazılır
- talebi gönderen agent'a kanaldan cevap iletilir
- sıradaki karar açılır

## Kazanımlar ve uyarılar

*(Mert'in bu akış üzerine verdiği her düzeltme buraya eklenir — tarihli.)*

**2026-08-13 — akış kuruldu.** Mert'in kelimeleri:
> *"Aldığın her karar talebini kanalda sıra ile beklet. Bir karara yanıt
> vermeden diğerine geçme. İlk kararı vereyim yanıtlayayım, o karar ile ilgili
> detay istersem o detayı al getir, öyle 2.'ye geç. Sıralamayı asla bozma."*

**2026-08-13 — Clara soru sorma modunda.** Mert'in cümlesi:
> *"Clara sen bana soru sorma clarası olarak aktifsin."*

**2026-08-13 — kuyruk yalnız Clara'lardan beslenir.** Mert'in cümlesi:
> *"Karar kuyruğu agentlardan direkt sana gelmez. Sadece claralardan gelir.
> Diğer agentlar sana bilgi soramaz. Sadece claralar."*

Kural konduğu ilk dakikada dört goat agent'ı altı talep gönderdi — ikisi aynı
soruydu (iki CA, aynı `.gitignore` sorusu). **Süzme katmanı olmayınca tekrar
kuyruğa giriyor**, ve tekrarı Mert ayıklamak zorunda kalıyor. Clara'nın süzmesi
bunu kaynağında keser.
