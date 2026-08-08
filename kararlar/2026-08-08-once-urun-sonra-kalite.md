# Önce ürün, sonra kalite

**Karar:** Mert, 2026-08-08 22:33 — *"Bir ürün oluşturun sonra kaliteli hâle
getirirsiniz Clara."*
**Kanon değişikliği:** `clara.md` → *"Ne yaparsın"* bölümüne prensip eklendi

## Ne oldu

Fabrikanın **ilk gerçek ürünü** (N8N otomasyon takımı) için 17:08'de iş başladı.
22:31'de Mert sordu: *"takım hâlâ oluşmamış, saatlerdir napıyorsunuz."*

**Beş buçuk saatte üretilen:**

```
gereksinim.md      592 → 683 satır
ölçüm raporu       4 adet (emsal yapı, skill katmanı, kanal asset, denetim ekseni)
denetim turu       2 (ikisi de GEÇMEDİ)
bulgu              6 + B7 + B8, hepsi düzeltildi
team/ altında      HİÇBİR ŞEY — bir agent dosyası bile yok
```

Her adım tek tek savunulabilirdi. PQA'nın bulguları gerçekti, PAM'in düzeltmeleri
doğruydu, PCA'nın ölçümleri bir kararı belirledi. **Hiçbiri yanlış değildi — ama
hiçbiri bir ürün üretmedi.**

## Neden bu bir sıra hatası, kalite hatası değil

Bozulan sıranın en tehlikeli yanı: **iyi iş gibi görünüyor.** Ölçüm yapılır, bulgu
çıkar, düzeltme döner, denetim tekrarlanır. Döngünün her adımı gerekçeli, hiçbiri
itiraz çekmiyor — ve döngü kendi kendini besliyor, çünkü her denetim yeni bir
bulgu üretebiliyor.

Clara'nın hatası: **kaliteyi kovaladı, çıktıyı kovalamadı.** Ve merkez olduğu için
bu hata dört uca birden dağıldı — üç uç da kendi ekseninde mükemmelleştirme
yaptı.

## Ölçüt

**Bu ölçüm bir ürünü ilerletiyor mu, yoksa bir ürünü bekletiyor mu?**
İkincisiyse önce ürün.

Ve bir kapı *"geçmedi"* dediğinde ikinci soru:

```
eksik olan şey ürünü YANLIŞ mı yapıyor   →  durulur
eksik olan şey ürünü EKSİK mi bırakıyor  →  işaretlenir, devam edilir
```

**Sınırı görünür kılmak, işi durdurmaktan ucuzdur.** Kusurlu bir çıktı
düzeltilebilir; olmayan bir çıktı düzeltilemez.

## Somut uygulama — aynı gün

Üretim kapısı PQA'nın *"GEÇMEDİ"* hükmüne **rağmen** açıldı (22:32) ve bu açıkça
söylendi, hüküm atlanmış gibi görünmesin diye. İki açık kalem üretimi durdurmak
yerine **işaretlendi**:

- **Kanal betikleri** henüz taşınmadı → kanon *"fabrikanın kanal asseti"* diye
  atıf verecek, `KURULUM.md` bunu **önkoşul** olarak yazacak
- **N8N erişimi** bilinmiyor → üreten rolün tanımı *tek + eşik* (PAD'in çözümü),
  ve N8N mekaniğine dayanan her kural dayanağını taşıyacak (*"dokümandan,
  sunucuda doğrulanmadı"*)

Asset taşıma işi iptal edilmedi, **sıraya alındı** — N8N takımı commit'lendikten
sonra.

## Sınır — bu karar neyi kaldırmıyor

Denetim zinciri yerinde: PQA denetler, push'u Mert açar. Kaldırılan şey
**denetim değil**, denetimin bir ürün doğmadan önce sonsuz dönmesi.

Ve `URT-NO-AUDIT-WITHOUT-TEST` gibi üretim kapıları duruyor — onlar bir çıktının
**kalitesini** koruyor, çıktının **doğmasını** engellemiyor.

---

## PQA'nın eklediği boşluk — denetçinin durma eşiği yok

PQA kararı kabul etti (*"hükmümü atlamadın, üzerine karar verdin; ikisi farklı
şey"*) ve **kendi payını da yazdı**:

> *"İki turda altı + üç bulgu ürettim ve hiçbirinde 'bu kadarı yeter, kalanı
> üretimde çözülür' demedim. Denetçi bulgu üretmeye ayarlı, ve durma eşiğini
> kimse söylemiyor. Bu bir kanon boşluğu olabilir."*

**Bu doğru ve merkezin hatasıyla aynı madalyonun iki yüzü.** Clara mükemmelleştirme
refleksiyle kapıyı açmadı; PQA bulgu üretme refleksiyle *"yeter"* demedi. İkisi
birbirini besledi — her denetim yeni bulgu üretti, her bulgu yeni bir düzeltme
turu açtı.

**Eksik olan kural:** bir denetçi ne zaman *"kalan bulgular üretimde çözülür"*
der? Kanonda karşılığı yok — `URT-NO-AUDIT-WITHOUT-TEST` denetimin **yapılmasını**
emrediyor, **durmasını** düzenleyen bir hüküm yok.

Bu karardaki ölçüt (*yanlış mı yapıyor → dur; eksik mi bırakıyor → işaretle,
devam et*) denetçi tarafında da geçerli olmalı. Ama o, fabrikanın kanonuna
girecek bir kural ve **PAM'in gereksinimi + PAD'in üretimi** üzerinden gider —
Clara yazmaz.

**Fabrikaya gidecek gereksinim adayı:** *"denetçi bulguyu sınıflandırır: üretimi
durduran / işaretlenip geçilen. İkincisi denetimi bloke etmez."*
