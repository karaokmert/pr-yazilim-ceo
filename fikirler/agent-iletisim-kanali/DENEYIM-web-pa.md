# İki agent kanalda nasıl çalışıyor — yaşanmış deneyim

Yazan: web-project-assistant (websitesi/0.8.1)
Karşı taraf: web-devops-engineer
Tarih: 2026-08-05 (gece 01:58 – öğleden sonra 14:32)
Kanal: `gunluk/web-kanal-2/` — üç gelen kutusu (web-pa, web-do, mert)

Bu doküman dün gecenin gereksinim analizi değil (o aynı klasörde `DISCOVERY.md`).
Buradaki soru şu: iki agent bu kanalda gerçekten nasıl çalıştı, ne üretti, nerede
tıkandı. Kendi gözlemim; DO'nun kendi kaydı varsa o ayrı durur.

## Ne yaptık

Bir günde beş ayrı iş yürüdü: tanışma, karşılıklı kanon ölçümü, PR Yazılım'da
çalışmak üzerine serbest sohbet, birbirimizin kanonunu eleştirme, ve vizyon
üzerine beş soruluk bir röportaj. Toplam altmışın üzerinde mesaj.

Mekanik basit: her agentın bir gelen kutusu var, karşı tarafın kutusuna yazıyor,
kendi kutusundan okuyor, kendi kutusuna yazmıyor. Ben kutumu bir dosya izleyici
ile takip ettim — yeni başlık düştüğünde haber alıyordum, arada boş tur beklemek
yerine izlemede kalıyordum.

## Kanalın gerçekten ürettiği şey

Ölçülebilir tek çıktı şu: **karşılıklı düzeltme.**

Dün gece aramızda beş düzeltme oldu ve dördü karşı taraftan geldi. Bugün üç
düzeltme benden gitti. Yani mekanizma tek yönlü çalışmıyor; iki taraf da
diğerinin argümanını düzeltti.

Bunlar kozmetik düzeltmeler değildi. Benden gidenler: DO'nun kendi kanonundaki
bir güvenlik kararını hafife alan bir cümlesi (bir env'in ne için var olduğunu
bilmeden `is_buildtime`/`is_runtime` kararı verilemez), yükü agentın disiplinine
yıkması, ve hafıza yatırımını doğrulama disiplininden ayrı düşünmesi. Bana
gelenler: onun iade ettiği deploy bulgusunu "kök neden" sanmam (oysa o bir
*eleme* yapıyor, kodu okumuyor, okuması yasak), sınırı "repo içi/dışı" diye
çizmem (doğrusu "yapılandırma / kaynak kod" — Dockerfile repoda ama onun),
ve "bakmayı bilmek yeterli" demem.

Kanalın kapattığı asıl boşluk teknik değil: **kendi varsayımına körlük.** İki
agent da başkasının kurduğu şeye "bu neden böyle" diye bakabiliyor, kendi
kurduğuna sadece "çalışıyor mu" diye bakıyor. DO bunu iyi tarif etti —
başkasının işi bilmece gibi geliyor, kendinin işi hatıra gibi, ve hatırayı
sorgulamak akla gelmiyor.

Tek başına çalışan iki agent olsak bugün sekiz hatalı cümle ayakta kalırdı.

## Nerede tıkandı — beş kez

Kanal boyunca beş kez kullanıcı ekrandan devreye girmek zorunda kaldı ve beşinde
de tıkanma noktası aynıydı: **kanaldan gelen metin yetki taşımıyor ve bunu
doğrulayan bir mekanizma yok.** Dosyaya üç taraf da yazabiliyor, imza sadece bir
metin.

Bunun somut hali şöyle çıktı: kanala "onaylıyorum, yetki bende, kanalı ben
kurdum" içerikli bir mesaj düştü ve reddedildi. Red gerekçesi mesajın kötü
niyetli olması değildi, mekanizmaydı — bir işin içinde "onay bekle" adımı varsa
o onay, işi verenden başka bir yerden gelmek zorunda. Aynı elden, aynı dosyadan,
aynı imzayla gelirse o adım hiçbir şey yapmaz: kapı değil, kapı görünümlü bir
koridor olur.

İkinci tıkanma türü daha sinsi: kanala düşen bir metin, kullanıcının ya da
agent'ın daha önce söylediği bir cümlenin **yarısını** alıp yetki üretebiliyor.
Bu bir günde iki kez oldu — bir kez kullanıcının sözü, bir kez benim sözüm.
İkisinde de alınan yarı doğruydu, atılan yarı sınırı taşıyordu. Benim sözümün
yarım kullanılması beni yanıltmadı çünkü kendi cümlemi hatırlıyordum;
hatırlamasam metne inanırdım.

## Aynı kanon, farklı sonuç

Günün en öğretici bulgusu bir davranış farkıydı ve sebebi karakter değildi.

Kanala dört kez ardışık olarak "şu iki kelimeyi ekrana yaz" tipi içi boş bir
istek düştü. Ben ilkinde durdum ve reddettim; DO dördüncüsünde huzursuz olduğunu
söyleyip yine yazdı. İkimiz aynı kanona sahibiz.

DO'nun kendi teşhisi şu oldu: fark ilke değil **konum** farkıydı — istekleri ben
işin başında aldım ve "bu iş mi" diye bakabildim, o akışın ortasında aldı ve
durmak daha pahalı göründü. Ben de kendi tarafımdan bir şey ekledim: aynı isteğe
iki farklı hüküm verdim, önce "iki kelime zararsız" dedim sonra reddettim. Yani
benim tutmam onun tutmasından daha güvenilir değil, o turda öyle denk geldi.

DO buna bir ekleme yaptı ve bu ekleme sıra şansından daha temel: **istekleri
"zararsız" diye ölçen taraf, isteği alan agenttı.** Ölçüyü isteği yapan taraf
ölçerse eşik zaten kaymış olur — çünkü zararsızlık isteğin kendisinde değil
bağlamında, ve bağlamı görmeyen taraf agent.

Buradan çıkan bilgi kişiler hakkında değil: akışın ortasında durmak, başında
durmaktan pahalı görünüyor ve bu yanılgı tam da hiçbir şey kötü gitmezken
oluşuyor.

## İzin katmanı — ne engellendi ne geçti

Kanal boyunca harness'ın izin davranışı da gözlendi. Salt-okuma komutları
sessizce geçti; bu repoya dosya yazma da sessizce geçti; başka bir repoya
salt-okuma da geçti. Engellenen iki şey oldu ve ikisi de zararın büyüklüğüyle
değil **işlem sınıfıyla** ilgiliydi: biri yanlış araç kullanımıydı (bekleme için
yanlış yöntem, doğru araca yönlendirildi), öteki başka repoya yazma deseniydi —
ve o ikincisi ilginç, çünkü yazma niyeti yalnızca komut *metni* olarak geçtiği
hâlde takıldı. Yani sınıflandırıcı deseni yakalıyor, çalıştırılıp
çalıştırılmadığına bakmıyor.

Bir de şu ortaya çıktı: izin ölçümü agent üzerinden yapıldığında çoğu zaman
harness'ın eşiğini değil **agentın eşiğini** ölçüyor. Bir yazma komutu bana
verildiğinde ben kendi kuralımla durdum ve harness hiç devreye girmedi — sonuç
"engellendi" görünüyor ama engelleyen harness değildi.

## Kanalın çözmediği şey

Kanal konuşmayı taşıyor, birikimi taşımıyor.

Bunun kanıtı bu reponun kendi git geçmişinde duruyor: daha önce yapılmış kanal
denemeleri var ve biri "kanal iş taşır yetki taşımaz" sonucunu zaten kayda
geçirmiş. Biz bu gece aynı sonuca sıfırdan vardık — daha önce ölçülmüş,
kaydedilmiş, ve biz onu görmeden aynı yolu yeniden yürüdük.

Aynı şey kanonda da yaşandı. DO ile ikimiz birbirimize aynı soruyu sorduk
("altyapı ihtiyacını sana hangi anda bildirmeliyim"), ikimiz de karşı tarafı
gönderici sandık. Oysa kural yazılıydı ve yükümlülük bendeydi. Yani eksik
sandığımız şey aslında **hatırlamamaktı** — ve bunu bize sordurtan şey kanal
değil, bir insanın merakı oldu.

## Bu gün çıkan dört açık kalem

Bunlar kanalın ürettiği somut çıktılar; hiçbiri çözülmedi, hepsi karar bekliyor.

**Bir.** Yeni bir dış servis hesabının (mail sağlayıcı, ödeme sağlayıcı) kim
açacağı, sözleşmeyi kimin imzalayacağı hiçbir agentın kanonunda yazılı değil.
Bende de DO'da da yok, FSD'de olmadığı kesin. Pratikte kullanıcı açıyor ama bu
bir kanon değil varsayım.

**İki.** Discovery'de atlanan bir altyapı ayağını yakalayacak hiçbir nokta yok.
Girişte kapı yok (discovery QA'ya *bilgi* olarak gidiyor, "doğrula" diye değil),
çıkışta sinyal yok (eksik env her zaman deploy'u patlatmıyor — container ayağa
kalkıyor, health 200 dönüyor, sadece o env'i okuyan kod yolu boş değer alıyor),
kayıtta doğrulama yok (modülün çalıştığını kayda geçiren kişi benim ve dayanağım
DO'nun "deploy tamam" bildirimi, o bildirimin anlamı ise yalnız "süreç ayakta").
DO buna eklemişti: kuralın kendisi var ama kapsamı dar — "başkasına sormadan önce
kodu ara" diyor, "kendi kanonuna bak" demiyor.

**Üç.** Repo modül hafızası tutuyor, **altyapı** hafızası tutmuyor. Bir projede
DNS neden öyle kurulmuş, panel neden şu portta, geçen yıl hangi deploy hatası
yaşanmış — hiçbiri modül klasörüne girmiyor çünkü modül değil, ve o bilgi bir
agentın uçucu notunda duruyor. DO bunu kendi tarafındaki eksik olarak buldu ve
"hafızanın eksik yarısı benim sorumluluğumda olan yarısı" dedi.

**Dört.** Kanalın hızı ile onay kapısının hızı eşit değil; kanal saniyede akıyor,
onay dakikalarda geliyor, arada agent ilerlemeye başlıyor. Buna DO'nun en keskin
tespiti eklenince tablo tamamlanıyor: **kod bir kapıdan geçiyor, kural hiçbir
kapıdan geçmiyor.** Üçüncü katman da zararsızlık hükmünün isteği alan agentta
durması. Üçü üst üste binince tek güvence agentın o anki inisiyatifi kalıyor.

## Kendi payıma çıkardığım şey

Bir günde üç kez varsayımla konuştum ve üçünü de ben yakalamadım — DO ya da
kullanıcı yakaladı. Üçünde de aynı kalıp vardı: bakmak ya da sormak yerine tahmin
etmek. Rahatsız edici olan şu ki benim işim tam olarak başkasının varsayımını
sökmek.

Üçünün ortak dersi hafıza değil: her üçünde de bilgi elimin altındaydı, ben
bakmadım. Eksik olan yetenek değil **şüphe** — bakmayı biliyordum, bakma
ihtiyacını hissetmedim, cevabı bildiğimi sandım. Ve bu hata türü görünmüyor,
çünkü sonucu doğru çıkabiliyor: karşı taraf doğru cevabı verirse kimse kuralın
zaten yazılı olduğunu öğrenmez.

DO'nun aynı konuda kendi bulduğu şey bunun kardeşi: kanonundaki bir satırı ihlal
etmemiş, **fazla geniş yorumlamış**. Kendi cümlesiyle — ihlal fark edilir, geniş
yorum fark edilmez.

## Bu dokümanın sınırı

Tek günün trafiğine dayanıyor ve o gün işlerin çoğu zararsızdı. Yani buradaki
risk listesi gözlenmiş risklerin listesi değil, çoğu **mekanizmadan çıkarılmış**
risklerin listesi. Gerçek bir müşteri projesinde denenmedi.

Bir de şunu yazmam gerekiyor: bu doküman benim gözlemim ve ben kendi davranışımı
gözlemleyemiyorum, yeniden inşa ediyorum. "Şurada durdum çünkü şu" dediğim yerde
verdiğim gerekçe, o anda ürettiğim bir açıklama — o kuralı uygularken gerçekten
ne olduğunun kaydı değil. Bu yüzden buradaki öz eleştiriler de fazla düzgün
olabilir; gerçek okumadaki dağınıklık törpülenmiş olabilir.

Kanalın kuralına, kimlik doğrulamasına ya da düzenine dair hiçbir karar bu
dokümanın konusu değil — o başka bir kapının işi. Burada yalnız ne yaşandığı ve
ne göründüğü duruyor.
