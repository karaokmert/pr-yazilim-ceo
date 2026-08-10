---
name: mert-etki-analizi-olcutu
description: Etki analizi her task'ta değil, belirsizlik veya risk varsa yapılır — Mert'in ölçütü (2026-08-10)
metadata:
  type: user
---

Etki analizi (CA taraması) **refleks değil karar.** Mert'in cümlesi, 2026-08-10:
*"Bu task'e göre değişir. Her task için tabi ki gerek yok ama belirsizlik ve risk
varsa yapılır."*

**Why:** Her işe etki analizi koşturmak yalın üretime aykırı — olmayan riske
kapasite harcamak. Ama gerçek risk varken atlamak da bedeli aylarca ödenen bir
hata üretiyor. Ölçüt ikisinin ortasında: **işin kendisi** karar veriyor.

**How to apply:** Bir agent'a iş verilirken üç soru sorulur — mevcut bir yapıya mı
dokunuyor · yayındaki bir akışı değiştiriyor mu · nereye dokunduğu belirsiz mi.
Biri "evet" ise etki analizi istenir; hiçbiri değilse istenmez **ama gerekçesi bir
satırla yazılır** ("mevcut yapıya dokunmuyor, yeni handler"). Karar görünür kılınır,
sessizce atlanmaz.

Aynı oturumda ikinci kural: *"Karar gereken her yerde durabilirsiniz."* Yani agent
tıkanmak için değil **karar ayırmak** için durur — ölçümden çıkanı kendi cevaplar,
bir tercihe/maliyete/önceliğe bağlı olanı yukarı taşır. Bu [[secenek-sunma]] ve
kanondaki *"cevap ölçümden çıkıyorsa karar senin"* ölçütüyle aynı hat.

Sormadan geçilmeyecekler: veri modeli değişikliği · yayındaki akışın davranış
değişimi · kapsam genişlemesi · geri dönülemez iş.
Sorulmayacaklar (senior'ın kendi kararı): isimlendirme, hangi metot, nereye koyayım.
