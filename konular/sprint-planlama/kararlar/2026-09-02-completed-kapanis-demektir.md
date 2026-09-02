# "completed" statüsü kapanış demektir

**Tarih:** 2026-09-02
**Karar veren:** Mert
**Bağlam:** Sprint 7 planlaması sırasında Didem'in açık iş listesi çıkarılırken
`include_closed: false` filtresine rağmen 60+ "completed" kayıt geldi.

## Ne bulundu

Space genelinde **256 task** "completed" statüsündeydi ve `date_closed` alanı
boştu. ClickUp bu kayıtları açık iş sayıyordu; herkesin yükü olduğundan şişik
görünüyordu.

En eski kayıt PRY-14060'a kadar gidiyor — yaklaşık bir yıllık birikim.

## Neden tereddüt edildi

Statü setinde beş ayrı "bitmiş" durumu var: `completed`, `lıve-dev`,
`ready for productıon`, `productıons`, `Closed`. Beş varsa `completed`'ın kendine
ait bir anlamı olabilirdi — örneğin "developer bitirdi, QA bekliyor".

Bu ihtimal Mert'e soruldu.

## Karar

**completed = kapanış unutulmuş.** Ara durum değil. 256 kayıt Closed'a çekildi,
hiçbiri hata vermedi.

Bundan sonra bir iş "completed" işaretlendiğinde kapanmamış sayılır ve Closed'a
çekilmesi gerekir.

## Reddedilen seçenekler

**Sadece Didem'de denemek** — hasar dar kalırdı ama sorun tüm ekipte olduğu için
yarım temizlik anlamsızdı.

**completed'ı ara durum saymak** — o zaman panolarda ayrı kategori olarak
gösterilecekti, yük hesabına katılmayacaktı. Mert bunu seçmedi; statünün anlamı
kapanış olarak sabitlendi.

## Sonucu

Temizlik üç projenin fiilen bitmiş olduğunu ortaya çıkardı: ListON'un EIDS hattı
(BE/FE/MB/QA/TE/CA/DO zincirinin tamamı), GaziMWS (veri modelinden Lighthouse
doğrulamasına dokuz adım), Egeli'nin üç chunk'ı.

Ayrıca kopya task sorununun sebebi görüldü: kapanış disiplini olmayınca bir işin
zaten var olduğu görülmüyor, tekrar açılıyor.
