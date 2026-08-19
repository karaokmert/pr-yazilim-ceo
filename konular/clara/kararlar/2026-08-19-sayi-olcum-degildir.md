# Sayı bir ölçüm değildir — `CLA-COUNT-IS-NOT-CONTENT`

**Tarih:** 2026-08-19 · **Karar:** Mert

## Kural

Mert iki CLAUDE.md'ye birden yazdı (global ve proje):

> *"Hiçbir zaman ölçüm sayısal yapılmaz. Hiçbir agent bir yaklaşımı sayısal olarak
> okumaz. Bir dosya, bir kod, bir fikir, bir klasör asla sayıdan ibaret değildir.
> İçerikleri önemlidir."*

Clara kanonuna `CLA-COUNT-IS-NOT-CONTENT` olarak girdi — kritik kurallar bölümünde,
`CLA-LABEL-YOUR-EVIDENCE`'ın hemen yanında. İkisi kardeş: biri *"okuduğunla ölçtüğünü
ayır"* diyor, öteki *"saydığınla okuduğunu ayır"*.

## Ayıran soru

**Bu sayıyı verirken içine baktım mı?**

Bakılmadıysa eldeki bir ölçüm değil, bir kabuk ölçüsü. Kabuk ölçüsü hüküm taşımaz.

Sayı yine de işe yarar ama yalnız bir **soru açar**, bir cevap kapatmaz.

## Neden bu kural gerekti — aynı gün üç ihlal

**Bir.** Yeni fabrika ekibi üretildikten sonra *"agent'ın önündeki kanon 4.800 satırdan
851'e indi, 5,6 kat"* diye övüldü ve rapora yazıldı. O 851 satırın **içinde ne yazdığına
bakılmadı** — kural mı taşıyor, genel tavsiye mi. Kıyas tamamen kabuk üstündeydi.

**İki.** Clara'nın kendi skill'leri denetlenirken ilk ölçüm satır ve kelime sayısıydı.
Mert kesti: *"hâlâ ölçümü satır ile yapıyorsun — senin için satır bekçiliği mi içerik
mi?"*

Bunun üzerine ayrı bir içerik ölçümü koşuldu (her hüküm: ölçülmüş bilgi mi, karar
kuralı mı, genel tavsiye mi) ve sonuç kabuğun tersini gösterdi: **hiçbir skill çöp
değildi.** Asıl arıza ölü adreslerdi — silinmiş bir dizini işaret eden komutlar, var
olmayan bir log dosyasına bağlanan monitör, eskimiş klasör düzeni. **Hiçbiri satır
sayısıyla görünmüyordu.**

**Üç.** Aynı gün `.trash` silinirken *"19 MB, %84'ü kanal trafiği"* denildi. İçindeki
66 karar dosyasının **ne dediği okunmadı**, yalnız sayıldı. Silindiğinde hangi
gerekçenin kaybolduğu bilinmiyor.

## Kanonda düzeltilen iki çelişki

Kural yazıldıktan sonra kanon tarandı, iki satır tersini söylüyordu:

- *"bir sayı üretir, ve sayı tartışmayı bitirir"* → **"sayı tartışmayı bitirmez,
  başlatır"** oldu.
- *"cevabın bir sayıya mı yoksa bir yargıya mı dayanıyor"* → **"bir yargıya mı, bir
  kanıta mı"** oldu; sayı artık kanıt sayılmıyor.

## Sınır

Kural sayıyı yasaklamıyor — **sayıya dayanarak hüküm vermeyi** yasaklıyor. Grep
çekilir, `git log` okunur, dosya sayılır; ama bunlar nereye bakılacağını söyler,
orada ne olduğunu değil.

Ve kısa istenmesi istisna değil: kısaltılacak olan çıktıdır. Okumadan verilen sayı
kısa değil, boştur.
