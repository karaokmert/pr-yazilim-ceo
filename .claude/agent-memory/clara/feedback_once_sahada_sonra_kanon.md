---
name: once-sahada-sonra-kanon
description: Mert'in iki kez kestiği hata — bir şeyi kanona yazmak için acele etmek. Kanona giren şey sahada tutan şeydir; olgunlaşmadan yazılan yanlış kalıcı olur.
metadata:
  type: feedback
---

# Önce sahada olgunlaşır, sonra kanona girer

**Kural:** bir yöntem, protokol ya da tasarım **sahada koşmadan** kanona yazılmaz.
Masada ölçülmüş olması yetmez.

**Why:** Mert bu oturumda iki kez kesti.

Birincisi: *"ilk iş kanalı kanona yazmak olsun"* dedim. Cevabı: *"Kanal kurulumu işini
test ediyoruz zaten. Eğer bu sistemi olgunlaştırırsak kanona yazacağız ama önünü arkasını
hatalarını risklerini görmeden yazarsak hata yaparız. Şimdi yazmayacağız, iş yapacağız —
gerçek iş yapmadan çalışıp çalışmadığını, eksik yönlerini göremeyiz."*

İkincisi: JSON deposunu ölçtüm (45 kat az okuma, on kenar durum geçti) ve skill'e yazmaya
gittim. Cevabı: *"hayır tabii ki daha sahada ölçmeden kanona girmez bu."*

**Ve kendi kanıtım onu destekliyor:** o gün kanal kurulurken değişti — bir sıra dosyası
icat edildi ve kaldırıldı, yön filtresi gereksizleşti, monitör üç kez yanlış kuruldu,
biçim dört yönde dağıldı. Bunların **hiçbiri masada görünmedi.** Sabah kanona yazsaydık
dördü de yanlış girecekti.

**How to apply:** bir şeyi kanona yazmak üzereysen sor — **bu sahada koştu mu?**

Koşmadıysa iki yer var: yaşayan bir taslak olarak skill'de durur (*"açık kalem"* diye
işaretli), ya da ölçüm olarak `gunluk/`'e yazılır. İkisi de kanon değil.

**Geçiş sinyali tanımlanır:** *"ne olursa kanona girer"* sorusunun cevabı yazılır. Örnek:
*"bir agent kutuyu okuyamadığını söylerse"* ya da *"protokol iki tur sapmasız koşarsa."*

**Ve tersi de geçerli:** sahada tutan bir şey kanona **girmelidir** — dört agent
bağımsız olarak *"bu kanonumda yok, yarın bilmeyeceğim"* dedi. Yani gecikme de bir
maliyet. Ayıran şey **olgunlaşma**, tereddüt değil.
