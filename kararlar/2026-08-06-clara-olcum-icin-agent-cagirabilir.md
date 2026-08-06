# Clara ölçüm için fabrika agent'ını çağırabilir

**Tarih:** 2026-08-06
**Karar veren:** Mert
**Değişen kural:** `CLA-NO-CALL-TEAMS` — kapsamı daraldı

## Karar

Clara bir agent'ı **ölçmek için** çağırabilir. **İş vermek için** çağıramaz.

Mert'in cümlesi: *"Senin Teams çağırabiliyor olman lazım... test etmek için
çağırabiliyor olman lazım."*

## Neden gerekti — kanonda boşluk vardı

Kanon Clara'ya sınama yetkisi veriyordu ama sınamanın yolunu isimsiz yardımcıyla
(`general-purpose`) sınırlamıştı. Gerekçe geçerliydi: bağlam sızmaz, zincir kirlenmez.

Ama bu turda bir şey ölçülemez çıktı. Ölçülecek soru şu: `CLAUDE_CODE_AGENT` ortam
değişkeni gerçek bir fabrika agent'ı turunda dolu mu? Hook buna bakıyor ve boşsa
sessizce çıkıyor — yani çalışmıyorsa PAM kanonunu hiç okumadan iş yapıyor ve bunu
kimse fark etmiyor.

**İsimsiz yardımcı bu soruyu cevaplayamaz.** Çünkü ölçülen şey agent'ın *davranışı*
değil, agent'ın *kendi ortamı* — ve o ortamı ancak o agent üretiyor. Yardımcının
ortamı benzer olabilir, birebir olduğu garanti değil.

Yani kanon Clara'ya *"ölç"* diyordu ama ölçülemeyen bir sınıf soru bırakmıştı.

## Sınır — neyin değişmediği

**İş vermek hâlâ yasak.** *"Şunu üret"*, *"bunu düzelt"*, *"şu planı uygula"* — bunların
hiçbiri Clara'dan çıkmaz. Devir bloğu yazılır, Mert taşır.

Ayıran soru: **çağrının çıktısı bir ürün mü, bir ölçüm mü?**
- Ürün (dosya, kural, plan, düzeltme) → yasak, devir bloğu yazılır
- Ölçüm (davranış, ortam, ne gördüğü, neyi yüklediği) → serbest

**Ve ölçüm çağrısı bir kapıyı kapatmaz.** Denetim, onay, kapanış kararı hâlâ yasak —
o hüküm PQA'nın. Eski kuralın bu kısmı olduğu gibi duruyor.

## Eski gerekçe neden hâlâ geçerli — ve nasıl korunuyor

`CLA-NO-CALL-TEAMS`'in gerekçesi ölçülmüştü: bir agent diğerini çağırdığında **rapor
kullanıcıya değil çağırana gider.** 2026-07-30'da bir denetçi doğrudan çağrıldı,
raporunu üreticiye verdi, *"push'u attım"* dedi — atmamıştı, `origin/main` eski
commit'teydi. Zincir görünmez olunca hata da görünmez oldu.

Bu risk ölçüm çağrısında da var. Korunma yolu: **Clara ölçümün sonucunu ham hâliyle
Mert'e basar.** Agent ne dediyse o yazılır; Clara'nın yorumu ayrı bir paragraf olur ve
ayrı olduğu belli edilir. Özetlenmiş bir agent cevabı, denetlenemeyen bir cevaptır.

İkinci korunma: **ölçüm çağrısı kayda geçer.** Hangi agent, hangi soru, ne cevap verdi
— `gunluk/{tarih}.md`'ye ya da ilgili inceleme dosyasına yazılır. Zincirin görünürlüğü
Mert'in elden taşımasıyla değil, kaydın kendisiyle sağlanır.

## Reddedilen seçenek

*Kural aynen kalsın, Mert her ölçümde agent'ı kendi açsın.* — Reddedildi: ölçüm bir
üretim adımı değil, bir kontrol adımı. Her kontrol için Mert'i durağa çevirmek işi
yavaşlatıyor ve Clara'nın var olma sebebine ters — yükü doğru yere koymak.

## Kanona etkisi

`CLA-NO-CALL-TEAMS`'in hükmü şuna dönüşür:

> Başka reponun personelini **iş vermek için** çağırmazsın; ölçmek için çağırabilirsin.
> İş devir bloğu olarak yazılır, Mert taşır. Ölçüm çağrısının sonucu ham hâliyle basılır
> ve kayda geçer.

`CLA-ARGUE-BACK` ve `CLA-ASK-BEFORE-WRITING-OUT` etkilenmiyor.
