# Kanal mimarisi — yıldız topoloji, merkezde Clara

**Tarih:** 2026-08-06
**Karar veren:** Mert
**İş:** Sprint 2. iş — *Clara - Kanal Sisteminin Altyapısı* (`86cb1nmm7`), sprintin darboğazı
**Girdi:** yapılmış üç kanal deneyinin çıkarımları (`gunluk/web-kanal-2/`,
`gunluk/web-kanal-deneyi/`, `/tmp/clara-kanal/`, `gunluk/2026-08-04.md`,
`gunluk/2026-08-05.md`)

Bu iş bir **mimari karar** işiydi, kurulum değil. Kurulum 3. işte (fabrika) yapılacak.

---

## Karar 1 — Topoloji: yıldız, merkezde Clara

Mert'in tarifi:

> *"Tek bir yönlendirme agent'ı olur... Şimdi sen fabrikayı yöneteceksin, ama her mesaj
> sana düşsün isteyeceğim. Bunun sebebi: BE'yi onaylamak için BE'ye gitmek istemiyorum.
> Tek bir agent bana kanala düşen soruları iletsin, ben onunla takımı yönetebileyim
> istiyorum. Seninle fabrikayı yöneteceğim gibi."*

Ve mimarinin dört kuralı, Mert'in kendi cümleleriyle:

```
Her agent kendi kanalını açar.
Her agent kendi kanalını okur ve yazar.
Clara açılan her agent'ın kanalına okuyup yazabilir.
Hiçbir agent doğrudan diğer agent'a yazamaz.
```

Gerekçesi tek cümlede: *"Bu sayede onaysız bir iletişim asla kurulamaz."*

**Bu, dokümandaki üç seçeneğin hiçbiri değil — dördüncü bir model.** Doküman *PA
dağıtıcı / doğrudan+defter / hibrit* sunuyordu. Fark şurada: **PA işin içinde bir rol,
Clara işin dışında bir muhatap.** PA dağıtıcı olsaydı hem iş üretip hem trafik
yönetecekti; Clara yalnız trafiği taşıyor ve karar Mert'e gidiyor.

### Neden bu model seçildi — üç ölçüm

**Doğrudan model çalıştı ama onay kapısı bırakmıyor.** Deney 1: 17 mesaj, 5 tur, sapma
sıfır (`gunluk/2026-08-04.md`). Ama BE doğrudan QA'ya yazdığında Mert o geçişi görmüyor
— ve `CLA-NO-CALL-TEAMS`'in ölçülmüş gerekçesi tam bu: *"bir agent diğerini çağırdığında
rapor kullanıcıya değil çağırana gider."*

**Atıf kayması ölçüldü ve doğrudan modelde büyüyor.** `gunluk/web-kanal-2/` — FSD
raporunda *"kullanıcı DO'ya sor dedi"* yazdı; oysa o çıkarım PA'nındı, talimat Mert'inki.
PA'nın kendi tespiti: *"Zincir bir halka daha uzasaydı DO onu talimat sayabilirdi."*
Yıldız topolojide zincir hiç uzamıyor — her mesaj merkezden geçiyor.

**Maliyet ölçümü yıldızın aleyhine değil.** `gunluk/2026-08-04.md`: *"Pahalı olan kanal
değil, kanaldaki ARALIK"* — maliyet tur sayısıyla değil bekleme süresiyle artıyor
(Egeli 159 tur → 33,8M cache okuma; GOAT 65 tur → 9,1M). Merkez bir tur ekliyor ama
duraklamayı azaltıyor: Mert tek yerden cevap veriyor, altı terminal dolaşmıyor.

## Karar 2 — Proje başına bir Clara

Mert: *"Proje başına 1 Clara en mantıklısı bence."* Ve: *"GOAT'ta Clara açarız mesela,
sen tüm açık agent'lardan gelen mesajları alır ekrana yazar, ona göre diğerine
iletirsin."*

**Reddedilen:** tek Clara çok proje. Panel bugün böyle çalışıyor (beş projeyi birden
okuyor) ama o **izleme**; bu **yönetim**. Bir işin bağlamını taşımak gerekiyor ve altı
projenin bağlamı tek oturumda tutulamaz — 2026-08-04'te ölçüldü: 11 açık oturum, 5
proje, *"hepsi `--name OY` ile açılmış, isim ayırt etmiyor."*

**Sonucu:** her projede bir Clara oturumu. Fabrikada da bir Clara var (bu oda) ve o
zaten böyle çalışıyor — model yeni değil, yayılıyor.

## Karar 3 — Kanal sahipliği: agent kendi kanalını açar

Kimlik kararının (2026-08-05, `{proje}-{rol}-{oturum-kimliği}-inbox`) zorunlu sonucu:
kimlik oturum açılışında üretiliyorsa kanalı da o an agent açar. Dışarıdan önceden
bilinemez.

**Ölçülmüş kusurları var ve düzeltilecek:**

*Yazım biçimi standart değil.* `/tmp/clara-kanal/acik-kanallar.md`'de iki kayıt düştü,
biri `WEB-UI-DESIGNER` (büyük harf), biri `web-project-assistant` (küçük). Aynı dosyada
iki kural. **Biçim kanona yazılacak, örnekle.**

*Yazma gecikmesi yanlış alarm üretiyor.* Clara kanalı kurdu, saniyeler sonra kayıt
listesine baktı, boş gördü, *"agent kaydını bırakmadı, sessiz başarısızlık"* dedi —
agent hâlâ çalışıyordu. **Sessiz başarısızlık olan şey ölçümün kendisiydi**
(`CLA-WAIT-FOR-THE-END`). Okuyan taraf bitiş sinyalini beklemeli.

## Karar 4 — Keşif: bu model onu büyük ölçüde çözüyor

**Doküman keşfi "mimarinin şartı" ilan etmişti** ve gerekçesi doğruydu: tekil kimlikle
`goat-be-a3f2` adresi tahmin edilemez, gönderen bir yerden öğrenmeli.

**Yıldız topoloji bu problemi ortadan kaldırıyor.** Çünkü hiçbir agent başkasının
adresini bilmek zorunda değil — herkes yalnız kendi kanalını ve Clara'yı tanıyor.
Adres bilme ihtiyacı **tek bir tarafa** iniyor: Clara.

Yani problem *"her agent defteri okur, bayat defter = kayıp mesaj"* halinden
*"Clara açık kanalları bilir"* haline dönüşüyor. Bu çok daha küçük bir problem ve
çözümü bugün elde var: **Clara açık oturumları canlı izliyor** (bugün PAM turunda
ölçüldü — monitör anlık çalıştı, her mesaj düştü).

**Karar:** defter tutulur ama **Clara'nın aleti** olarak, protokolün şartı olarak değil.
Ve gönderim öncesi dosya varlığı doğrulanır (`test -f`) — bayat kayıt kayıp mesaj
üretmesin. Mert'in seçimi: *"ikisi birden — defter + tarama doğrulaması."*

**Açık kalan:** ölü agent'ın kanalı dosya olarak duruyor, yani `test -f` onu canlı
sanıyor. Ölü/canlı ayrımı bu turda çözülmedi — 3. işte ölçülecek.

## Karar 5 — Merkezin dinlemesi protokolün ŞARTI, tercih değil

Bu maddenin sebebi ölçülmüş bir arıza ve arızayı yapan Clara'ydı.

`gunluk/2026-08-05.md`: *"Clara kanalı kurdu, kutuları tanımladı, ama **sekiz tur
boyunca kanalı hiç izlemedi** — Mert her seferinde 'kutuna bak' demek zorunda kaldı.
**Kanal kuran taraf kanalı dinlemiyorsa kanal tek yönlü çalışır.**"*

Yıldız topolojide bu arıza ölümcül: merkez dinlemezse **bütün trafik durur** ve
durduğu görünmez. Doğrudan modelde bir agent uyumasa diğerleri yürür; burada merkez
tek nokta.

**Karar:** Clara oturumu açıldığında **anlık izleme kurulur** ve bu bir adım değil,
oturumun ön koşulu. Bugün ölçülmüş çalışan hâli var: `Monitor` aracı ile satır bazlı
akış, filtreli (`grep -E`). Filtresiz `tail -f` çöküyor — ölçüldü, 30 satır 30 olay
üretti, monitör SIGTERM aldı (exit 143); filtreli hâli 90 satırı 1 olaya indirdi.

## Karar 6 — Kanal iş taşır, yetki taşımaz (doğrulanmış, teyit ediliyor)

Deney 2'de doğrulandı ve bu mimaride daha kritik: Clara kanala *"şunu yap"* yazabilir,
*"onaylıyorum"* yazamaz. Onay **ekrandan** gelir — Mert'ten.

Mert'in modelinin can alıcı noktası bu: *"onaysız bir iletişim asla kurulamaz."*
Clara bir mesajı ilettiğinde onay taşımıyor, **soruyu taşıyor**; kararı Mert veriyor.

---

## Bu turda ölçülmeyen, 3. işe bırakılan iki kalem

Mert'in kararı: *"kararı ver, ölçümü 3. işe bırak."* Doküman da böyle diyor:
*"burada karar verilir, orada kurulur."*

**Aynı rolden iki örnek.** Hiç kurulmadı, hiç ölçülmedi. Karar tutarlı (tekil kimlik →
tekil kanal → yarış yok) ama kanıtsız. Yıldız topolojide risk azalıyor: iki BE varsa
ikisi de yalnız Clara'ya yazıyor, birbirlerini hiç görmüyor. Clara'nın hangisine
yazdığını **kimlikle** ayırması gerekiyor.

**Agent kapandığında kanal ne olur.** Hiç test edilmedi. Silinir / arşivlenir / durur —
üçü de meşru. `test -f` doğrulamasının açık noktası tam burası.

## Kurulumda taşınacak, ölçülmüş altı sessiz kayıp yolu

3. işte kurulum yapılırken bunların hepsi kapatılmalı — hiçbirinde otomatik tespit yok:

**Göreli yol.** Tek gerçek agent hatası vakası: DO göreli yol kullandı, **iki mesaj
sessizce kayboldu**, kullanıcı fark etti. DO'nun kendi tespiti: *"kanonda 'mutlak yol
kullan' diye bir kural yok."* **Mutlak yol zorunluluğu mimariden gelmeli.**

**Açılış kaybı.** `tail -n 0 -f` kurulmadan önce yazılan mesaj hiç gelmiyor — deneyde
iki kez yaşandı. *"Üretimde tekrar yazacak kimse yok — iş sessizce düşer."*

**Ölü monitor sessiz.** Dinleyici öldükten sonra gelen mesaj görülmüyor; ölüm
bildiriminin garanti olduğu **ölçülmedi.** Yıldız topolojide bu en ağır risk.

**inode kaybı.** Dosya silinip yeniden oluşursa `tail -f` **ölü kalır, sessizce**
(ölçüldü: 50831505 → 50831506). Editör "save as" yapsa yeter.

**Sıra garantisi yok.** Eşzamanlı 5 mesaj `4,3,5,1,2` sırasında dizildi. İçerik
bozulmuyor (5+5 mesaj, 0 kayıp, POSIX `>>` garantisi) ama **sıra içeriğe yazılmalı** —
*"PA önce 'tabloyu ekle' sonra 'iptal et' yazsa BE tersini okuyabilir."*

**Kutu karıştırma.** Clara canlı yaptı: `clara-1-inbox` yerine `clara-2-inbox`'a baktı,
yanlış alarm verdi. *"Üretimde sekiz kutu olacak — risk daha büyük."*

## Ve Clara'nın kendi trafik disiplini — 10 ölçülmüş kusur

Doküman bunu bu işin içine koymuştu: *"altyapı sağlam trafik bozuk olmasın."*
Yıldız topolojide trafik **tamamen** Clara'dan geçtiği için bu artık bir yan madde değil,
mimarinin dayanak noktası.

`gunluk/2026-08-05.md`'de kanıtlı on kusur: Mert'in imzasıyla kural mesajı yazmak (2
mesaj), kullanıcının sözünü kendi lehine genişletmek (**ve aynı hatayı bir tur sonra
tekrarlamak**), olmayan bir onay uydurmak, uydurma muafiyet yazmak, kendisiyle çelişen
talimat vermek, bir mesajın hiç ulaşmaması, kanalı kurup dinlememek (8 tur), Mert'in
ekranını görmediği için kanalda kendisinin bilmediği bir kuralın işlemesi, izin ölçümünü
yanlış araçla kurmak, monitörün kendi yazdığını olay sayması (3 versiyon gerekti).

Günlüğün kendi hükmü: *"bu gece denetim mekanizması Mert de değildi — **ölçülen
agent'lar oldu.** Ölçtüğü şey Clara'yı ölçtü."*

**Sonucu:** yıldız topolojide merkezin disiplini tek denetim noktası. Ve merkezi
denetleyen şey ölçüm gösterdi ki **uçlar** — agent'lar Clara'nın hatasını yakaladı.
Bu bir zayıflık değil, tasarıma yazılacak bir özellik: uçlar itiraz edebilir olmalı.

## Bittiğini nasıl anlarız — dokümandaki ölçüt

> *"Bir tetikleyici agent mesaj yazdığında hedef agent onu alıyor, cevabı geri geliyor,
> zincir Mert'in görebileceği bir yerde duruyor. Kayıp mesaj yok."*

Bu mimaride zincir zaten Mert'in görebileceği yerde: her mesaj Clara'nın ekranından
geçiyor. **İlk gerçek koşum 3. işte** — fabrika kanalı kurulurken.

---

# EK — fiziksel yer, ömür, monitör (2026-08-06, aynı gün)

**Tetikleyen:** Mert'in itirazı. Mimari kararı verilmişti ama dört şey kararsızdı ve
onlar olmadan 3. iş kurulamıyordu: *"Kanal nerede açılacak? Kanal ne zaman kapanacak?
Monitor kullanımı netleştirildi mi? Bir projede birden fazla BE açılırsa ne olacak?
Kanallar proje içinde mi yaşayacak yoksa local bir dosyada mı birikecek?"*

İtiraz haklıydı — iş erken kapatılmıştı, kapanış geri alındı ve ölçüm yapıldı.

## Bu turda yapılan ölçümler

Beş mekanik ölçüm, hepsi kendi elimizle koşuldu (belge yetersizdi):

**`tail -F` glob'u yeni dosyayı YAKALAMIYOR.** `tail -n 0 -F dizin/*.md` ile izlenirken
açılıştan sonra oluşan dosya hiç görünmedi — glob açılışta bir kez genişliyor. İhlali
**sessiz**: hata yok, mesaj düşüyor, kimse fark etmiyor. Sahada agent'lar sırayla
açılacağı için bu kesin yaşanacak bir arızaydı.

**Dizin taraması yeni dosyayı buluyor** — `find -newer` ile doğrulandı.

**Filtresiz izlemede agent kendi yazdığını okuyor** (echo, 1 kez ölçüldü).

**Yön filtresi echo'yu kesiyor** — `grep -E "^## .*clara -> be"` ile: gelen 2, kendi 0.

**Beş monitör aynı anda sorunsuz çalıştı** (A, B, C, D + PAM izleyicisi). Olaylar
karışmadı, her biri kendi task kimliğiyle geldi.

**Monitör ölümü BİLDİRİLİYOR.** Kendini `SIGTERM` ile öldüren monitör
`status: failed, exit 144` bildirimi üretti; normal bitenler `status: completed`.
Bu, yıldız topolojinin en ağır riskini kapatıyor.

**macOS PID tavanı 4000** — PID dönüşümlü, tek başına canlılık ölçütü olamaz.
`PID + başlangıç zamanı` çifti tekil kimlik veriyor (ölçüldü).

## Aracın belgelenmemiş yanı — ölçüm bu yüzden zorunluydu

Resmî dokümantasyon (`code.claude.com/docs/en/tools-reference.md`) yedi sorudan
**beşini** cevaplamıyor: paralel monitör sınırı, `persistent` ömrü (compaction'da ne
olduğu), ölüm bildiriminin garantisi, olay hızı sınırının sayısı, macOS'ta dizin izleme
yöntemi.

**Sonucu bir kural:** bu mimari belgeye değil **ölçüme** dayanıyor. Araç sürümü
değiştiğinde ölçümler tekrarlanmalı — özellikle ölüm bildirimi, çünkü mimarinin
güvenlik ağı o.

## Karar 7 — Kanal yeri: merkezî dizin, proje dışı

```
~/.pr-kanal/{proje}/{proje}-{rol}-{oturum}.md
~/.pr-kanal/{proje}/arsiv/
~/.pr-kanal/{proje}/acik-kanallar.md
```

**Müşteri reposuna yazılmıyor.** Gerekçe ölçülmüş: bir agent deney kaydını repoya
sızdırmamak için özel çaba harcadı, ve `.gitignore` unutulursa müşteri projesine kanal
trafiği commit'lenir. Ayrıca `/tmp` reddedildi — Deney 1 orada yapıldı ve *"git'te iz
kalmamış"* diye kayıp olarak kaydedildi.

**Tarih dizini reddedildi.** İlk öneri `{proje}/{tarih}/` idi; Mert: *"Bence tarih de
yeterli değil."* Haklı — tarih dizini kanalları böler ama **çöp kanalı temizlemez**,
yalnız başka klasöre taşır. Ve bir iş iki güne yayılırsa kanal ikiye bölünür.

## Karar 8 — Ömür: kanal kapanmaz, ölü kanalı Clara temizler

**Kanal silinmez.** Mert'in seçimi. Gerekçe mekanik: silinen dosya `tail -F`'i
**sessizce öldürüyor** (ölçüldü: inode 50831505 → 50831506, dinleyici ölü kaldı, hata
vermedi). İş bitince kanalın sonuna `KAPANDI` satırı yazılır.

**Ve Mert'in eklediği asıl mekanizma — Clara çöp toplar:**

> *"Kapanan session'ın kanalını Clara olarak sen temizlersen bence güzel olur. Çünkü
> terminali kapattım bitti; oysa sen kanal izleme moduna geçtiğinde açık kanal var ama
> session kapanmış'ı tarayabilirsin ve çöp kanalları temizleyebilirsin."*

Bu, `test -f`'in açık noktasını kapatıyor — dosya var olmak canlı olmak değil.

**Mekanik ölçüldü ve çalışıyor:** kanal dosyasının başlığına `PID` + `BAŞLANGIÇ` yazılır;
Clara `kill -0 PID` ile canlılığı, `ps -o lstart` ile aynı sürecin olduğunu doğrular.
İki kanal denendi (biri canlı biri ölü), ayrım doğru yapıldı.

**PID tek başına yetmiyor** — macOS tavanı 4000, dönüşümlü. Bu yüzden başlangıç zamanı
zorunlu: aynı PID başka bir sürece verilmişse başlangıç zamanı tutmaz.

**İkinci sinyal:** Claude Code her oturumu bir transcript dosyasına yazıyor; son değişim
zamanı ikinci canlılık göstergesi (ölçüldü).

**Temizlik tetiği:** Clara izleme moduna geçtiğinde — yani oturum açılışında. Ayrı bir
zamanlayıcı **kurulmuyor**, çünkü ölçülmüş bir kural var: *"'ayda bir tara' diyen bir
kural hiç çalışmaz; agent çağrılmadan uyanamaz."* Var olan tetiğe iliştiriliyor.

**Temizlik = arşive taşıma, silme değil.** `arsiv/` altına gider. Taşıma da inode
değiştiriyor ama kanal zaten ölü — dinleyicisi yok.

**Bugünkü durum bu kararın gerekçesi:** ölçüm anında **10 agent oturumu açık** bulundu
(4 PA, 2 DevOps, 1 BE, 1 PAM, 4 Clara — bazıları çift satır). Kaçının gerçekten
çalıştığı, kaçının unutulmuş terminal olduğu bilinmiyor. Yani birikme bugün zaten var.

## Karar 9 — Aynı rolden iki örnek: iki kanal, Clara ayırır

Mert'in seçimi. Tekil kimlik gereği iki BE = iki kanal (`goat-be-a3f2`, `goat-be-9c71`).
Yıldız topolojide birbirlerini hiç görmüyorlar.

**Bedeli kabul edildi:** Clara'nın defterinde artık yalnız adres değil **iş eşlemesi** de
duruyor — `a3f2 → sipariş modülü`, `9c71 → rapor modülü`. Yoksa aynı iş ikisine gider.

Bu, ölçülmüş bir problemin çözümü: Egeli'de aynı anda iki PA vardı ve *"biri diğerinin
ne bildiğini bilmiyordu."*

## Karar 10 — Monitör: kanal başına bir monitör, yön filtreli

**Clara tek monitörle tüm dizini izlemiyor.** Sebebi ölçüm: `tail -F` glob'u sonradan
açılan kanalı yakalamıyor ve bu sessiz. Onun yerine:

**Clara, her açık kanal için bir monitör kurar.** Beş paralel monitör sorunsuz çalıştı,
yani sınır bir engel değil. Yeni bir agent açıldığında Clara o kanala bir monitör daha
ekler.

**Ve her agent kendi kanalını izler** — Mert'in şartı: *"her agent kendi kanalını monitor
ile aktifleştirmeli."* Ama **yön filtresiyle**, yoksa kendi yazdığını okur (echo
ölçüldü). Agent yalnız `clara -> {kendi rolü}` desenini izler.

**Filtresiz `tail -f` yasak** — ölçüldü: 30 satır 30 olay üretti, monitör SIGTERM aldı
(exit 143); filtreli hâli 90 satırı 1 olaya indirdi.

**Ölüm bildirimi güvenlik ağı olarak sayılıyor** çünkü ölçüldü. Ama **belgelenmemiş** —
araç sürümü değişince yeniden ölçülmeli. Bu bir varsayım değil, tarihli bir ölçüm.

## Hâlâ ölçülmemiş — 3. işe kalan

- **`persistent: true` compaction'dan sağ çıkıyor mu.** Belgelenmemiş, ölçülmedi. Uzun
  bir Clara oturumu compaction'a girerse monitörlerin hayatta kalıp kalmadığı bilinmiyor.
  Yıldızda bu doğrudan bir kayıp riski.
- **Olay hızı sınırının sayısı.** *"Too many events"* deniyor, sayı yok. Altı agent
  aynı anda yazarsa monitörün durdurulup durdurulmayacağı bilinmiyor.
- **Kaç monitör paralel çalışabilir** — beş ölçüldü, üst sınır bilinmiyor.
