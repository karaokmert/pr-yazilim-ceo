# Kanal kutusunun `{oturum}` biçimi `YYYYMMDD-HHMM` oldu

**Tarih:** 2026-08-07 · **Karar:** Mert · **Durum:** kapalı

## Karar

Kanal kutusu adresindeki `{oturum}` alanı **`YYYYMMDD-HHMM`** biçiminde yazılır.

```
~/.pr-kanal/{proje}/{rol}-{YYYYMMDD-HHMM}/
```

`setup.py` bunu otomatik üretiyor; agent elle yazmıyor. Aynı dakikada ikinci kurulum
`rc=1` ile reddediliyor (mevcut kutu ezilmiyor).

## Neden karar gerekti

Biçim tanımsızdı ve sahada **üç ayrı biçimde** kutu açıldı: elle etiket (`-ilk`), iş adı
(`-kanal-kurulumu`) ve tarih-saat. İkisi aynı dakikada açıldı ve **aynı damgayı** aldı —
aynı rolden iki örnek olsaydı kutular çakışacaktı.

Sebep şablonda `{oturum}` yazılı olmasına rağmen **örnek verilmemiş olmasıydı.** Örneksiz
bir biçim kuralı her okuyucunun kendi yorumunu üretiyor ve yanlış biçim düzeltilmiyor,
**yayılıyor.**

## Neden iş adı değil tarih-saat

İki aday vardı. Üç uç bağımsız **tarih-saat**i seçti ve gerekçesi şu:

**İş adı ayırt edici değil.** Aynı rolden ikinci bir örnek açıldığında iş adı iki kutuyu
ayırmıyor — ikisi de aynı işin parçası olabilir. Tarih-saat her zaman tekil.

**Tarih-saat sıralanabilir.** Kutular alfabetik sıralandığında kronolojik sıraya giriyor;
arşivde ve `archive-log.json`'da devri bulmak kolaylaşıyor.

**PID adaylığı zaten düşmüştü** — `PID` alanı `STATUS.md`'den kaldırıldı, çünkü üç turda
ölçüldü ve hiçbir soruya cevap vermedi (ayrıntı: `kanal-kurulumu` skill'i).

## Bu kararın kapattığı şey

`kanal-kurulumu` skill'inde *"`{oturum}` biçimi — açık kalem"* diye duran madde kapandı.
Artık tartışılmaz; değişecekse neden değiştiği yazılır.

## Sınırı

Bu karar **biçimi** sabitliyor, **çözünürlüğü** değil. Dakika çözünürlüğü aynı rolden aynı
dakikada iki kutu açılmasını engelliyor (`rc=1`) — ve bu bilinçli: kasıtlı ikinci kurulum
bir dakika bekler. Saniye çözünürlüğüne ihtiyaç doğarsa yeniden karar gerekir.
