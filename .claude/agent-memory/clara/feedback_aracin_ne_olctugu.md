---
name: aracin-ne-olctugu
description: Bir sayı verirken aracın NE saydığını doğrula — doğru ölçüt sayma değil varlık kanıtıdır (dört vaka, 2026-08-11)
metadata:
  type: feedback
---

Bir sayı ölçüldüğünde **aracın ne saydığı** doğrulanır. Kanonda zaten *"neyi saydığını
söyle"* var; bu kural bir adım öteye gidiyor: **söylemek yetmiyor, aracın gerçekten onu
saydığını KONTROL ETMEK gerekiyor.**

**Why:** 2026-08-11'de aynı sınıf hata **dört kez** düştü, dört ayrı tarafta:

- **Clara:** `ps aux | grep -c "[a]pi-reward-system"` → **1** aldı, *"servis ayakta"*
  dedi. BE düzeltti: sayılan şey servisi **başlatan kabuk** (`/bin/zsh -c source`),
  servisin kendisi değil. `lsof -iTCP:PORT -sTCP:LISTEN` → **boş.**
- **BE:** aynı hatanın kendi versiyonu — uca vurdu, **200** döndü, *"çalışıyor"* sandı.
  Süreç ölüydü, istekler **kümedeki eski pod'a** gidiyordu. Kendi cümlesi: *"Az önceki
  cevabım benim düzeltmemi ölçmüyordu, eski kodu ölçüyordu."*
- **PA:** `sed` büyük-harf dönüşümünü desteklemedi → **10 uç "YOK"** çıktı, hepsi
  **vardı.** Ve ortak dosya sayımı: **11** sandı, `comm -12` ile **7** çıktı.

BE'nin formülasyonu: *"Sayı bir şey söylüyor ama NEYİN sayıldığını söylemiyorsa, o sayı
kanıt değil."*

**How to apply — doğru ölçütler hep aynı sınıfta: sayma değil VARLIK KANITI.**

- süreç sayısı (`ps | grep -c`) → **port dinleniyor mu** (`lsof -nP -iTCP:P -sTCP:LISTEN`)
- uç 200 dönüyor mu → **hangi kod cevaplıyor** (koda geçici iz bırak, cevapta gör)
- dosya listesi tahmini → **`comm -12`** ile kesişim ölçümü
- grep sonucu, özellikle `0` → **deseni BİLİNEN vakayla test et**

Son madde en önemlisi ve iki agent bağımsız olarak buldu. BE ilk iki denemesinde `0`
aldı, `0`'ı sonuç saymadı — bilinen vakayı desende arayıp deseni **test etti**,
ıskaladığını anladı, düzeltti. PA aynı dersi tersinden söyledi: *"`sed`'in dönüşümünü
bilinen bir isimle test etseydim, 10 ucun 'YOK' çıkmasından şüphelenmeye gerek kalmadan
ÖNCEDEN yakalardım."*

Ayıran soru: **bu sayı bir VARLIK mı gösteriyor, yoksa bir EŞLEŞME mi?** Eşleşme sayısı
aracın desenine bağlıdır ve desen yanlışsa sayı sessizce yanlış olur. Varlık kanıtı
(port, dosya, kesişim) araca değil **duruma** bakar.

Bkz. [[bos-olcum-degil]] — `0`'ın en yanıltıcı cevap olması.
Bkz. [[yazmanin-boyutu-olculur]] — `rc=0` de bir eşleşme, varlık kanıtı değil.
Bkz. [[cakisan-sinyal-dogrulama-degil]] — birden çok sinyal aynı aracın çıktısıysa tek
gerçeğin yansımasıdır.
