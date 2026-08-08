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

---

## İkinci uyarı, ertesi gün 01:53 — kural yazıldı ama hız yine yetmedi

Mert: *"24 saatte bir takım kurulumunu bitiremedin biraz ilerle artık!"*

**Kural 22:33'te kanona yazılmıştı ve ürün 22:37'de doğdu** — o kısım işledi.
Ama 22:48'den 01:51'e kadar **üç saat** daha geçti ve commit hâlâ yok.

### Bu sefer sebep farklı — ve daha ince

İlk vakada sebep *mükemmelleştirme* idi (denetim turları dönüyordu, ürün yoktu).
İkincisinde ürün **var** ve ilerliyor; kaybedilen şey **görünürlük**:

```
22:48  PAD son bildirimini yaptı (ADIM 1-3 bitti)
       ↓ üç saat sessizlik
01:49  Clara ölçtü: dört body yazılmış, ama index yok, commit yok
01:51  PAD: "ADIM 5'teyim, tıkanmadım" — bir dakikada cevap verdi
```

**İki taraflı eksik, ve çözümleri farklı:**

```
PAD tarafı    uzun üretim bloğunda ara bildirim yok     → DİSİPLİN
Clara tarafı  üç saat kutunun yazım zamanına bakmadı    → MEKANİZMA
```

İkincisi Clara'nın **aynı gün ikinci kez** yaptığı eksik. PCA'nın ölçümüyle
sabitlenmişti: *merkez ucun dosya yazım zamanına bakabiliyor ve o sinyal monitöre
bağımlı değil.* Sinyal elindeydi, kullanılmadı.

**Uygulanan ölçüt:** bir üretim bloğu 30 dakikayı aşıyorsa tek satır bildirim
(*"X'teyim, Y kaldı"*), cevap beklemeden. Bekleme ücreti yok, iş bölünmüyor.

### Ve PAD'in kendi ölçümü bir arıza yakaladı — bu gecikme değil, kazanç

ADIM 5'e girerken kimlikleri **elle saymadı, grep'le ölçtü**:

```
82 kural tanımı
11 KİMLİK İKİ KEZ TANIMLANMIŞ
18 body atfı — yetim yok (bu taraf temiz)
```

**Sebep bir üretim SIRASI tuzağı, dikkatsizlik değil:** ortak skiller önce, rol
skilleri sonra yazıldı; rol skilinde kural *"burada da anlatmalı"* diye **tanım**
biçimiyle yazıldı, atıf biçimiyle değil. Üstelik bu takımın kanonunda buna karşı
kuralı **PAD'in kendisi** yazmıştı.

Tekrarlanabilir olduğu için kayda değer — bir sonraki takımı üreten bu tuzağı
bilmeli.

### Mert'in iki içerik itirazı (01:53)

**İsimler görev adı, rol adı değil.** `n8n-planlayan / ureten / kosturan /
denetci` — hepsi **fiil**. Emsalde `backend-developer`, `qa-engineer` var: bunlar
**meslek**. Ölçüt: *bir insan bu unvanla işe alınabilir mi?* `DAG-NAME-BY-ROLE`
zaten bunu istiyor ve PAD'in kanonunda vardı — **kural elindeydi, uygulanmadı.**

**Dört kişi gerekli mi — ölçülmedi.** PAM'in ölçümü *"ayrık malzeme yok → üretici
bölünmez"* diyordu, yani **dokuz değil dört**. Ama *"neden üç ya da iki değil"*
hiç sorulmadı. Şu anki gerekçe *"emsal böyleydi"* seviyesinde ve yetersiz.

Ölçüm sorusu her rol için tek: **bu rol kaldırılırsa işi kim yapar ve ne
kaybedilir?** Birleştirme adayları: planlayan+üreten (gereksinimin kendisi bu
ikisinin *"anormal yakın"* olduğunu yazıyor), koşturan+denetçi (ikisi de
*"çalışmıyor"* diyebiliyor, fark kapı yetkisi).

**Azaltma çıkarsa azaltılacak** — yalın üretim kuralı: ihtiyaç doğmadan kapasite
kurulmaz, her rol bir bakım maliyeti.

**Sıra bilinçli kuruldu:** rol sayısı → isimlendirme → çift tanım temizliği →
index/test/commit. Tersi sırada temizlik iki kez yapılırdı.
