---
name: durum
description: İLK BUNU OKU — son kapanış dokümanının adresi ve tek cümlelik durum. Oturum açılışında ilk okunan kayıt.
metadata:
  type: project
---

# Durum

**Son kapanış:** `gunluk/2026-08-07-kapanis-3.md` — oku, çalışmaya başlayabilirsin.
Aynı günün önceki ikisini iptal etmiyor, üstüne ekliyor.

**Tek cümlede:** Fabrikanın kanalı ayağa kalktı ve kanonu bir günde baştan elden
geçti — `Task` çağrısı kaldırıldı, iletişim kanala taşındı, kural sayısı 123→131.
On altı denetim turu, on üç bulgu, hepsi kapandı.

## Şu an nerede

**GÖREV DEVREDİLDİ.** Mert 2026-08-07 01:34'te sekiz maddelik bir gece görevi
verdi (fabrikayı push'a hazır hâle getir: tüm kuralları sorgula, çelişkileri
temizle, agent'ların kuralları bildiğini doğrula). Context dolduğu için **yeni bir
Clara oturumu** açıldı ve devir yazıldı:
`~/.pr-kanal/agent-project/clara-ceo-20260807-1653/inbox` (6.072 karakter).

Bu oturum kapandı, izleyicileri durduruldu.

## Beklemede

**PUSH — 22 commit, on bir iş.** Brief: `gunluk/2026-08-07-push-brief.md`
PQA denetim onayı verildi. Mert: *"Push'un bir acelesi yok, çalışıyoruz zaten."*

**Karar defteri — yedi kalem:** `gunluk/2026-08-07-mert-e-sorulacaklar.md`
En kritik üçü: push kapsamı · iki commit'lenmemiş dosya (index'te on kural onlara
atıf veriyor) · index paralel düzende güncel kalamıyor.

## Ölçülmemiş — gece görevinin merkezi

**Agent'ların kanonu GERÇEKTEN bilip bilmediği hiç sınanmadı.** PCA'nın uyarısı:
*"kanona uygun görünmek ile kanondan gelmek aynı şey değil."*

Ve bir risk: bu oturumda merkez **çok fazla bağlam taşıdı** — her mesajda
gerekçeler tekrarlandı. Doğru davranışın ne kadarı kanondan, ne kadarı merkezin
mesajlarından, ayırt edilmedi.

## Bugün ölçülen üç ders

**Dört taraf da aynı kuralı aynı gün ihlal etti** — `BHV-DATE-THE-MEASUREMENT`
kanona girdi ve PAM, PAD, PQA, Clara dördü de kaynağa bakmadan hatırlananı taşıdı.

**Kendi dosyasına bakan göz kör, ve sistematik** — dört kez, dört farklı elde.

**Eksen devredilebiliyor** — günün örüntüsünü (*"her tur bir öncekinin açığını
kapatır"*) kıran tek örnek: PAD, PQA'nın eksenini kendi üstüne koşturdu ve aynı
sınıftan bulgu buldu.
