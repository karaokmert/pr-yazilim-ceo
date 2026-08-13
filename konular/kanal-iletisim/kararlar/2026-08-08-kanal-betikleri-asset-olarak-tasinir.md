# Kanal betikleri fabrikaya asset olarak taşınır

**Karar:** Mert, 2026-08-08 22:26
**Tetik:** N8N takımı üretim kapısı — PQA ikinci denetimde B8 bağımlılığını buldu

## Karar

**Beş kanal betiği (532 satır) + `SABLON-JSON.md` (661 satır) `agent-project`
git'ine asset olarak taşınır.** N8N takımı kanal düzenini oradan alır.

**Taşıma işini PAD yapar, ayrı bir iş olarak** — N8N üretiminden **önce**, kendi
turunda. PQA denetler, push'u Mert açar. Sonra N8N kapısı açılır.

Bu, 2026-08-07'de kararı verilmiş ama **yapılmamış** bir işin yürütülmesi.

## Gerekçe

**Diğer iki yol eşit değildi ve bu ölçüldü.**

PAM gereksinimde iki yol yazmıştı (asset olarak taşı / takım kendi mekanizmasını
kursun) ve ikinciyi *"iki uygulama doğar, zamanla ayrışır"* diye tartmıştı.
**PCA'nın ölçümü bu tartıyı düzeltti** — ve yöntemi önemli: kendi okumasıyla
cevaplayamayacağını söyleyip (*"betikleri gördüm, tarafsız değerlendiremem"*)
temiz bağlamlı bir yardımcıya sınattı, `tools/` açmasını yasakladı.

**Sonuç: beş betikten hiçbiri uyumlu biçimde yeniden yazılamıyor.** Ayrım keskin:

```
tel-üstü biçim  TARİF EDİLMİŞ    mesaj JSON'u (tam şema), dosya adı deseni,
                                 STATUS.md, çıkış kodları, atomik yazma
durum biçimi    EDİLMEMİŞ        .cursor iç yapısı, .announced, HANDOVER.json
                                 şeması, archive-log.json, arşiv hedef dizini
```

Yani **iki kanal birbirinin mesajını okur ama birbirinin nerede kaldığını
bilmez.** Ve **ayrışmaların beşte dördü sessiz sınıfta** — yanlış yeniden üretim
**çalışır görünüyor.** En kritiği `.cursor`: biçimi farklı olursa `read.py` ya
imleci okuyamaz ya boş sayıp **hepsini yeniden okur** — kanal kanonunun kendi
yasakladığı iki yönlü sessiz hata. `HANDOVER.json` ayrışırsa **devir sessizce
kaybolur**, ki mekanizmanın var olma sebebi tam buydu.

**PQA'nın hükmü:** *"iki yol eşit değil — birincisi bir iş, ikincisi bir arıza
üretimi."*

**Ve boşluk gereksinimde olduğundan küçük görünüyordu.** PAM `kanal.md`'den
doğru alıntı yapmıştı ama `kanal.md` boşluğun **varlığını** biliyor,
büyüklüğünü değil — büyüklüğü anlatan cümle (`SABLON:647-648`, *"şablon 'nasıl
yapılır'ı cevaplamıyor, onu araçlar cevaplıyor"*) git'e **hiç geçmemiş.**
Eksik bir kaynaktan doğru alıntı.

## Bu kararın kapattığı bağımlılık

PQA'nın B8 bulgusu: gereksinimin **B1 çözümü B6'ya bağlı** ve bu görülmemişti.

B1 *"denetçinin raporu kalıcı olarak dursun"* diyor — bir **mekanizmaya**
yaslanıyor (kanal kutusu). O mekanizmanın bu takımda kurulup kurulamayacağı
B6'nın önkoşuluydu. Yani belgenin kendi yazdığı ters-yön kuralı
(*"mekanizmanın varlığı doğrulanmadan ona atıf verilmez"*) kendi B1 çözümüne
uygulanmamıştı.

**Birinci yol seçildiği için B1'in koşulu da sağlanmış oluyor.**

## Yan kazanç

Fabrikanın **kendi** kanalı da silinmeye dayanıklı hâle geliyor. Bugünkü ölçüm
şunu gösterdi: `~/.pr-kanal/` silinirse git'teki 2552 satırlık kanon kanalı
**geri getiremiyor.** Bu, N8N işinden bağımsız bir kırılganlıktı.

## Sıra

```
1. PAD betikleri taşır (ayrı tur)     ← şimdi
2. PQA denetler
3. Mert push'u açar
4. PAM gereksinimde B1↔B6 bağımlılığını görünür kılar + B7 (üç öznesiz cümle)
5. PQA üçüncü denetim
6. N8N üretim kapısı açılır
```

## Kapsam dışı bırakılan

**Betiklerin içeriği okunmadı** — PCA kasıtlı okumadı (sınamanın geçerliliği
buna bağlıydı), PQA da okumadı ki aynı sınama tekrar koşulabilsin. Yani
*"betikler belgelenmemiş davranış taşıyor mu"* sorusu **açık** ve taşıma
sırasında cevaplanabilir.

**`SABLON:487`'nin yanlış tarifi** (`HATA:` yazıyor, betikler `ERROR:` basıyor —
PAD ölçtü: `ERROR:` 14, `HATA:` 0) ayrı bir kalem. Taşıma sırasında düzeltilmesi
doğal ama bu kararın konusu değil.
