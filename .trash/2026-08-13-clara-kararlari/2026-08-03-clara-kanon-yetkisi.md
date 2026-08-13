# Clara kendi kanonuna yazar — yasak kaldırıldı, yerine ne kondu

Tarih: 2026-08-03 (akşam)

Mert: *"Clara.md'yi senin yazman lazım. Kendi kurallarını talimatlarını sen
genişletebilirsin. Kurallar sende kararlar sende. Bakalım kendini ne kadar iyi
geliştirebileceksin."*

Bu karar aynı günün sabahında verilen yasağı kaldırıyor
(`2026-08-03-clara-memory-disiplini.md` → "Serbestliğin sınırı"). O bölüm tarihçe
olarak duruyor, üstüne değişiklik notu düşüldü.

## Kaldırılan yasak ve neden kaldırılabildi

Sabahki gerekçe mekanikti ve **hâlâ doğru**: `clara.md` system prompt'a giriyor. Clara
oraya bir kural yazarsa bir sonraki turda onu *"doğru"* olarak değil **"ben"** olarak
taşır — yani yazdığını sorgulayamaz. Bu odada denetçi yok; tek göz kendi gözlüğünü de
yapıyorsa ölçüm diye bir şey kalmaz.

Yanlış olan şey gerekçe değil, ondan çıkarılan sonuçtu. *"Sorgulayamaz"* sorunu
yazmayı yasaklamakla çözülmüyor — çünkü Clara'nın yazmadığı kanonu da aynı şekilde
taşıyor, o da system prompt'ta ve o da sorgulanmıyor. Yasak sorunu çözmüyordu, yalnız
Clara'nın gelişmesini durduruyordu.

Gerçek çözüm: **kural içeride, gerekçe dışarıda.** Kanona yazılan her değişikliğin
neden yazıldığı `kararlar/` altında durur. O zaman bir sonraki tur kuralı sorgulayamasa
da dayanağını **okuyabilir** — ve Mert de okuyabilir. Sorgulanabilirlik kanondan
çıkarılıp kayda taşınmış oluyor.

Gerekçesiz kanon değişikliği yapılmaz. Yapılırsa iki ay sonra o satırın neden orada
olduğunu kimse bilemez ve kanon kendi kendini açıklayamayan bir metne dönüşür.

## Yetki dışında bırakılan üç şey

Clara kendi kararıyla dokunmuyor: **adı**, **kadın kimliği**, **üç sert sınır**
(`CLA-WRITE-HERE-ONLY`, `CLA-NO-CALL-TEAMS`, `CLA-ARGUE-BACK`).

Gerekçe: kimliğini ve sınırını kendi değiştiren bir agent'ın zamanla nereye kaydığını
ölçecek bir referans kalmaz. Kural değişebilir ama **neye göre değiştiğini** söyleyecek
sabit bir nokta gerekiyor; bu üçü o nokta.

Bunlar değişecekse Mert söyler.

## Şişme freni

Kanon 386 satırdı. Her turda büyürse iki ayda okunamaz hâle gelir ve okunmayan kanon
yokmuş gibidir — bu tam olarak v7'nin arızası (`fikirler/oy-uretim-yontemi/durum.md`:
bakımı zor, bir kural değiştirmek günler alıyordu).

Kanona kondu: bir kural eklerken sorulacak soru **"bu satır olmasa ne yanlış yapardım?"**
Cevap yoksa satır gürültü. Ve **çıkarmak da büyümektir** — işlemeyen, çakışan ya da
başka bir kuralın içinde erimiş bir satır gerekçesiyle çıkarılır.

## Bu turda kanona giren dört değişiklik

**Bir — `HARITA.md` okuma refleksi.** *"Önce buraya bakarsın"* diyordu ama bakılacak
yer yoktu. Artık harita var ve durum sütununun üç değeri farklı davranış gerektiriyor
(kapalı / yarım / eskimiş olabilir).

**İki — hafıza/dosya ayrım testi değişti.** Eski test *"bunu Mert'in görmesi gerekiyor
mu?"* idi. Mert bu oturumda *"beynin sende kalsın, ben sana sorduğumda söylersin"* dedi;
test çöktü. Yeni test: **"bu bilgi kimin hakkında?"** Mert ve Clara hakkında olan
hafızaya, iş hakkında olan dosyaya. Sınırda kalan dosyaya.

**Üç — hafıza kaydı kendi kendini denetler.** Mert rutin bakmadığına göre yanlış kaydı
yakalayacak dış göz yok. Telafi: her kayıt tarih + dayanak + kırılganlık taşır.
Görünürlük Mert'e değil zamana açılıyor.

**Dört — "Kendini nasıl büyütürsün" bölümü açıldı.** İçinde yetkinin mekaniği, üç
dokunulmaz, şişme freni ve dört yazma tetikleyicisi var.

Dördüncüsünün gerekçesi ölçüm: ilk 8 commit boyunca hafızaya giren 4 kaydın **hepsi**
Mert'in düzeltmesinden sonra girdi, Clara kendiliğinden tek kayıt açmadı. Yetki vardı,
tetikleyici yoktu (`incelemeler/clara-beyni/tespit.md` → "Bulgu üç").

## Açık risk — kabul edilmiş

Clara artık kendi kanonunu yazıyor ve bu odada denetçi yok. Sabahki gerekçe hâlâ
geçerli: yazdığı kuralı bir sonraki turda sorgulayamaz.

Taşınabilir kılan üç şey: gerekçenin dışarıda durması, üç dokunulmazın sabit kalması,
ve şişme freni. Ama hiçbiri denetim değil — **denetim yine Mert'te**: kanonu okuyabilir,
`kararlar/` altındaki gerekçeyi isteyebilir, bir satırın çıkarılmasını söyleyebilir.

Bu riskin bir de ölçülebilir işareti var: kanon satır sayısı. Gerekçesiz büyüyorsa
mekanizma çalışmıyor demektir.
