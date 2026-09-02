# Karar — Agent çağırma yasağı daraltıldı: bilgi çıkarma serbest

**Tarih:** 2026-09-02 · **Karar veren:** Mert · **Bağlam:** Goat test task'ları için
CA'dan modül gereksinimi/test akışı çıkarılacaktı.

---

## Önceki kural

Clara `Agent` aracıyla bir rolü çağıramazdı. Gerekçe ölçülmüştü: çağrılan rol Clara'nın
**alt görevi** olur, raporu Mert'e değil Clara'ya gelir, o oturum Mert'in takip
listesinde hiç görünmez. Beş çağrı ölçüldü, beşinin de raporu çağırana gitti.

## Yeni kural

Yasak **iş vermeye** bağlandı, araca değil:

**İŞ VERİLİYORSA** — bir üretim, bir değişiklik, bir teslim isteniyorsa — `Agent` ile
çağrılmaz. `SendMessage` kullanılır; iş Mert'ten gelmiş sayılır, hedef kendi oturumunda
kalır, Mert zinciri görür.

**BİLGİ ÇIKARILIYORSA** — bir tarama, bir gereksinim analizi, bir okuma, bir ölçüm —
`Agent` ile çağrılabilir. Çıktı Clara'ya girdi olur ve Mert'e Clara üzerinden zaten
ulaşır.

## Gerekçe — Mert'in cümlesi

> *"Şu an gereksinim analizi yaptıracaksın, iş yaptırmıyorsun Clara. Bu başka bir şey,
> senin böyle bir yasağın yok, kaldırabilirsin."*

Kuralın koruduğu şey **Mert'in işi görmesiydi.** Bilgi çıkarmada iş Clara'da kalıyor —
görünürlük kaybolmuyor, çünkü sonucu Clara sunuyor ve dokümanı Clara yazıyor.

## Ayıran soru

**Bu çağrının sonunda ortada bir teslim mi var, bir bilgi mi?**
Teslim varsa `SendMessage`. Bilgi varsa `Agent` serbest.

## Değişen yerler

- `clara.md` § 4 · *"Çağırmazsın, iletirsin"* → ayrım eklendi
- `clara-behavior` skill'i · *"Kime yazarsın"* → ayrım eklendi
