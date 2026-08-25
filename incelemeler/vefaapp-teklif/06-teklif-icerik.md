# MEZARLIK BAKIM VE HİZMET PLATFORMU
## Ön Dokümantasyon & Teklif

**Versiyon:** V.1 · **Tarih:** 25.08.2026 · **Açıklama:** TEKLİF

---

# 1 · Proje Tanımı

## 1.1 · Amaç

Bu projenin temel amacı; şehir dışında veya yurt dışında yaşayan
vatandaşlarımızın, sevdiklerinin ebedi istirahatgahlarına mesafeye rağmen
gereken özeni gösterebilmesini sağlayan, uçtan uca **denetlenebilir ve
kanıtlanabilir** bir dijital hizmet platformu kurmaktır.

Bu iş, klasik bir e-ticaret ya da randevu sisteminden ayrılır: satılan şey bir
ürün değil, **sahada yapılan ve yapıldığı kanıtlanması gereken bir hizmettir.**
Platformun değeri, hizmetin kendisinden çok **hizmetin yapıldığına dair
güvenden** doğar. Bu nedenle sistemin omurgası, her ziyaretin öncesi ve sonrası
görsel kanıtla belgelendiği bir izlenebilirlik zinciri üzerine kurulmuştur.

Platformun hedefleri:

**Mesafeyi Ortadan Kaldırmak:** Müşterinin fiziksel olarak bulunamadığı bir
işlemi, kendi gözüyle görmüş gibi takip edebilmesini sağlamak. Her ziyaret
öncesi/sonrası fotoğraf ve video ile raporlanır; rapor otomatik olarak PDF
formatında müşterinin erişimine açılır.

**Tekrar Eden Gelir Modeli:** Bakım hizmetinin doğası gereği süreklilik
gerektirmesinden yararlanarak, tek seferlik satış yerine **abonelik temelli
sürdürülebilir bir gelir yapısı** kurmak. Sistem, aylık ve yıllık planları,
otomatik tahsilatı ve yenileme döngüsünü kendi başına yönetir.

**Saha Operasyonunun Dijitalleşmesi:** Sahadaki personelin işini telefonundan
yürüttüğü, konumuyla doğrulandığı ve görsel kanıt yüklemeden işi
kapatamadığı bir operasyon disiplini kurmak. Kanıt olmadan iş kapanmaz —
bu bir tercih değil, sistemin kuralıdır.

**Ölçeklenebilir Teknoloji Altyapısı:** PR Yazılım'ın C# (.NET Core), MSSQL,
Redis ve RabbitMQ mimarisi üzerine inşa edilen platformun, artan il/ilçe
kapsamına, büyüyen personel ağına ve yeni hizmet kalemlerine tam uyumlu
kalmasını sağlamak.

## 1.2 · Kapsam

Proje, birbirine entegre **dört arayüz** ve bunları besleyen teknik servisler
olarak bütünleşik bir yapıda geliştirilecektir:

**Web Sitesi ve Müşteri Üye Alanı:** Hizmetin tanıtıldığı, paketlerin
karşılaştırıldığı, siparişin oluşturulduğu ve müşterinin raporlarını takip
ettiği ana arayüz. SEO odaklı geliştirilir — mezarlık ve bölge bazlı organik
arama trafiği bu iş için kritik bir müşteri kaynağıdır.

**Müşteri Mobil Uygulaması (iOS + Android):** Müşterinin siparişini takip
ettiği, öncesi/sonrası fotoğrafları gördüğü ve anlık bildirim aldığı uygulama.
Bu iş uzaktaki insan için kuruludur; "raporunuz hazır" bildiriminin telefona
düşmesi hizmetin algılanan değerini doğrudan belirler.

**Saha Personeli Mobil Uygulaması (iOS + Android):** Personelin günlük
görevlerini gördüğü, mezarlıkta konumuyla doğrulandığı, öncesi/sonrası
görselleri yüklediği ve işi kapattığı operasyon aracı.

**Yönetici Paneli:** Siparişlerin personele atandığı, aboneliklerin izlendiği,
fiyat ve katalogların yönetildiği, finansal raporların alındığı üst düzey
kontrol arayüzü.

**Genişletilebilir Altyapı:** Mimari, ek hizmet kalemlerinin (mezar taşı satış
hattı, dış tedarikçi ağı) sonradan eklenmesine uyumlu ve ölçeklenebilir şekilde
tasarlanacaktır.

## 1.3 · Teknik Alt Yapı

Sistem, PR Yazılım'ın kurumsal performans ve güvenlik standartlarını temsil
eden modern bir teknoloji yığını üzerine inşa edilecektir:

**Backend (Arka Yüz):** Veri merkezi ve iş mantığı süreçleri **C# (.NET Core)**
ile kurumsal standartlarda geliştirilecektir.

**Frontend (Ön Yüz):** Web arayüzleri, SEO dostu ve hız odaklı **Next.js**
framework'ü ile geliştirilecektir. Sunucu taraflı render sayesinde mezarlık ve
bölge sayfaları arama motorlarında görünür olur.

**Mobil Uygulamalar:** İki uygulama da **React Native (Expo)** ile
geliştirilecek; tek kod tabanından iOS ve Android sürümleri üretilecektir.

**Veritabanı Yönetimi:** İlişkisel veri yapısı için **MSSQL** tercih
edilecektir. Abonelik döngüsü, tahsilat kayıtları ve finansal raporlama
ilişkisel model gerektiren süreçlerdir.

**Performans ve Hız:** Mezarlık listesi, paket tanımları ve katalog gibi okuma
ağırlıklı veriler için **Redis** cache mekanizması kullanılacaktır.

**Mesajlaşma ve Asenkron Süreçler:** PDF rapor üretimi, toplu bildirim
gönderimi ve abonelik tahsilat döngüsü gibi arka plan işlemleri için
**RabbitMQ** mesaj kuyruğu altyapısı kurulacaktır.

**Görsel ve Doküman Yönetimi:** Saha görselleri ve raporlar **Azure Blob
Storage** üzerinde saklanacaktır.

**Bildirim Altyapısı:** Anlık bildirimler için push servisi, bilgilendirmeler
için SMS ve e-posta entegrasyonu kurulacaktır.

---

# 2 · Proje Geliştirme Süreçleri

## 2.1 · Alt Yapı Planlaması

Sözleşmenin imzalanmasının ardından, teklifte planlanan ana ve ek modüllere
ilişkin detaylı bir planlama dokümanı hazırlanır. Bu aşamada modüllerin
kapsamı ve önceliklendirmesi netleştirilerek proje yol haritası
kesinleştirilir.

## 2.2 · Tasarım Planlaması

Modüller kesinleştirildikten sonra tasarım hazırlama süreci başlar. Belirlenen
yazılım planlamasına uygun şekilde her modülün arayüzü tasarlanır ve bu
tasarımlar üzerinden etkileşimli bir prototip oluşturulur. Hazırlanan prototip,
proje sorumlusuna sunulur ve düzenlenen tasarım toplantısında geri bildirimler
alınır. Toplantıda belirlenen revizeler uygulandıktan ve nihai tasarım onayı
alındıktan sonra yazılım geliştirme aşamasına geçilir.

## 2.3 · Yazılım Geliştirme Süreci

Onaylanan tasarım üzerinden yazılım geliştirme süreci başlar. Projenin
ihtiyaçlarına göre belirlenen önceliklendirme doğrultusunda Backend (alt yapı
yazılımı), Frontend (ön yüz yazılımı) ve Mobil geliştirmeleri eş zamanlı
yürütülür. Projenin kapsamına bağlı olarak iki ya da üç haftalık döngülerle
tamamlanan modüller test ortamına alınır ve müşterimizin belirlediği proje
yöneticisinin bu modülleri test etmesi beklenir. Modüllerin prototipte ve
sözleşmede tanımlandığı şekilde çalıştığına dair onay alınır. Bunun yanı sıra,
projenin hedef kitlesinin gerçek kullanım koşullarını yansıtan kullanım
testlerinin yapılması da önerilir.

## 2.4 · Test & QA

Önceliklendirilen modüllerin tamamlanmasının ardından proje ekibimiz,
modüllerin doğru ve istenildiği gibi çalıştığını doğrulamak amacıyla haftalık
genel testler gerçekleştirir. Bu aşamada müşterimizin belirlediği proje
yöneticisinden de projeyi test etmesi ve tamamlanan modülleri uçtan uca
kullanması beklenir.

Bu projede test sürecinin bir özelliği vardır: **saha operasyonu gerçek
koşullarda denenmelidir.** Saha personeli uygulamasının bir mezarlıkta, gerçek
şebeke koşullarında ve gerçek görsel yükleme hacmiyle test edilmesi
önerilmektedir.

İyileştirme veya akış değişikliği talepleri, mümkün olduğunca yayına alma
sonrasına bırakılır. Bu güncellemelerin yayın öncesine alınması talep edilirse
ek geliştirme bedeli hesaplanarak müşteriye bildirilir ve onaylanması durumunda
ilgili versiyonun proje bedeline eklenir. Tüm modüllerin test ve onay süreci
tamamlandığında proje teslim edilmiş kabul edilir. PR Yazılım, garanti süresi
boyunca oluşabilecek modül hatalarına ücretsiz destek sağlar.

## 2.5 · Deployment (Yayına Alma)

Yayına alma süreci, projenin boyutuna göre bölümlere ayrılarak parçalı şekilde
yürütülebilir. Bu yaklaşım, ön hazırlık yapılmasına ve canlıya geçişin
kontrollü ilerlemesine olanak tanır. Örneğin yönetici paneli ve saha personeli
uygulaması tamamlandığında canlıya alma işlemi başlatılabilir ve operasyon
sınırlı bölgede gerçek veriyle çalışmaya başlayabilir. Geliştirme süreci
kesintisiz devam eder; test aşaması tamamlanan her modül sırasıyla canlı
ortama alınır.

**Mobil uygulamaların mağaza süreçleri:** iOS App Store ve Google Play Store
yayın süreçleri PR Yazılım tarafından yürütülür. Mağaza inceleme süreleri
platform sağlayıcılarının kontrolündedir ve proje takvimine dahil edilemez.

---

# 3 · Proje Kaynakları ve Maliyetleri

## 3.1 · Fiziksel Sunucu

Aylık fiyatlandırılır. Türkiye lokasyonlu bir sunucu olarak %98 uptime
garantisi bulunur.

**Aylık: 250 $ + KDV**

Sunucu, sözleşmenin imzalanması ile birlikte aktifleştirilecektir.

## 3.2 · SMS Entegrasyonu

Kullanıcılara gönderilecek SMS bilgilendirmeleri ve telefon doğrulama işlemleri
için NETGSM alt yapısı kullanılacaktır. **Net GSM paketleri ile
ücretlendirilir.**

Bu projede SMS opsiyonel değildir: sipariş sürecinde telefon doğrulaması
güvenlik gereksinimidir.

## 3.3 · Mail

Kullanıcılarınıza göndermek istediğiniz otomatik sistem mailleri için
Mailchimp alt yapısı kullanılacaktır. **Mailchimp paketleri ile
ücretlendirilir.**

## 3.4 · Ödeme Altyapısı

Sanal POS ve tekrarlayan ödeme (abonelik) altyapısı için anlaşmalı bir ödeme
sağlayıcısı kullanılacaktır. **Sağlayıcı komisyon oranları ve entegrasyon
bedelleri müşteri ile sağlayıcı arasındaki anlaşmaya tabidir.**

⚠️ Abonelik altyapısı, ödeme sağlayıcısının **tekrarlayan ödeme (recurring)
desteği** bulunmasını gerektirir. Sağlayıcı seçimi bu şartla yapılmalıdır.

## 3.5 · Görsel Depolama

Saha görselleri ve video raporları için Azure Blob Storage kullanılacaktır.
**Kullanım hacmine göre ücretlendirilir.**

⚠️ Bu projede depolama maliyeti zamanla artan bir kalemdir: her ziyaret
öncesi/sonrası görsel üretir ve bu görseller müşteri arşivi olarak saklanır.
Saklama süresi politikası proje planlamasında belirlenecektir.

---

# 4 · Paneller & Arayüzler

Platform, kullanıcı rollerine göre özelleştirilmiş, birbirine entegre **dört
ana arayüzden** oluşmaktadır.

## 4.1 · Web Sitesi & Müşteri Üye Alanı

Next.js teknolojisiyle geliştirilen bu arayüz, platformun dış dünyaya açılan
vitrinidir. Hem bir tanıtım ve satış kanalı hem de müşterinin hizmetini takip
ettiği kişisel alandır.

**Kamuya açık bölüm:**
- **Hizmet ve Paket Vitrini:** Bakım paketlerinin karşılaştırmalı sunumu,
  aylık/yıllık plan seçenekleri ve kapsam detayları
- **Bölge ve Mezarlık Arama:** İnteraktif Türkiye haritası üzerinden il/ilçe
  seçimi ve mezarlık adıyla arama
- **İş Galerisi:** Tamamlanmış bakım ve mezar taşı çalışmalarının öncesi/sonrası
  görsellerle sunulduğu güven vitrini. Her kayıt kendi adresine sahip olacak
  şekilde geliştirilir — arama motorlarından organik trafik kazanımı sağlanır
- **Süreç Anlatımı:** Siparişten raporlamaya kadar işleyişin şeffaf sunumu
- **Kurumsal ve Yasal Bölümler:** Hakkımızda, iletişim, SSS, KVKK aydınlatma
  metni, gizlilik politikası, mesafeli satış sözleşmesi

**Sipariş akışı:**
- Mezarlık seçimi (il → ilçe → mezarlık) veya doğrudan arama
- Paket seçimi (abonelik / tek seferlik, aylık / yıllık)
- **Görsel Peyzaj Tasarım Aracı:** Mezar görseli üzerinden mermer rengi seçimi,
  hazır şablon uygulama ve toprak alanına bitki yerleştirme. Seçilen kalemlerin
  bedeli canlı hesaplanır ve pakete eklenir
- Merhum bilgileri, mezar yeri tarifi, özel anma günleri ve müşteri notları
- Telefon doğrulaması (SMS)
- Sözleşme onayı
- 3D Secure güvenli ödeme, taksit seçenekleri ve indirim kodu uygulaması

**Müşteri üye alanı:**
- Aktif abonelikler, sonraki ziyaret tarihi, otomatik yenileme kontrolü
- Sipariş geçmişi ve durum takibi
- **Rapor arşivi:** her ziyaretin öncesi/sonrası görselleri, video raporları ve
  indirilebilir PDF raporları
- Abonelik iptali ve sipariş iptali
- Profil, iletişim bilgisi ve şifre yönetimi
- Hizmet değerlendirme ve yorum bırakma
- Hesap silme talebi (yasal gereklilik)

## 4.2 · Müşteri Mobil Uygulaması (iOS + Android)

React Native ile geliştirilen, müşterinin hizmetini avucunun içinden takip
ettiği uygulamadır. Bu iş uzaktaki insan için kurulmuştur; anlık bildirim
hizmetin algılanan değerini doğrudan belirler.

- **Anlık bildirim:** ziyaret gerçekleştiğinde, rapor hazırlandığında, tahsilat
  alındığında veya bir aksiyon gerektiğinde telefona düşen bildirimler
- Sipariş ve abonelik takibi
- Öncesi/sonrası görsel ve video arşivi
- PDF rapor görüntüleme ve paylaşma
- Yeni sipariş oluşturma ve ödeme
- Özel anma günü hatırlatmaları
- Profil ve abonelik yönetimi

## 4.3 · Saha Personeli Mobil Uygulaması (iOS + Android)

Sahadaki personelin işini yürüttüğü operasyon aracıdır. Bu uygulama, platformun
güven iddiasının teknik dayanağıdır: **kanıt yüklenmeden iş kapanmaz.**

- **Günlük görev listesi:** personele atanmış ziyaretler, konuma göre
  sıralanmış; her görevde paket kapsamı ve yapılacak işler açık
- **Mezar konum yardımı:** mezarlık içi tarif, varsa konum bilgisi ve
  referans görsel — sahanın en zaman kaybettiren problemi doğru mezarı bulmaktır
- **Konum doğrulaması:** personelin mezarlıkta bulunduğunun teyidi
- **Öncesi görsel yükleme:** işe başlamanın ön koşulu; görsel yüklenmeden
  işlem adımları açılmaz
- **İş kontrol listesi:** pakete göre değişen yapılacaklar listesi
  (ot temizliği, mermer yıkama, sulama, çiçek dikimi vb.) ve tamamlanma
  işaretlemesi
- **Sorun bildirimi:** mezar taşında kayma, mermerde çatlak gibi fiziki
  durumların görselle raporlanması — müşteriye ayrı uyarı olarak iletilir ve
  ek hizmet satışına imkân tanır
- **Sonrası görsel ve video yükleme**
- **İşi kapatma:** kanıt tamamlanmadan kapatma butonu aktif olmaz
- Tamamlanan işler geçmişi

## 4.4 · Yönetici Paneli

Tüm sistemin veriye dayalı yönetildiği, operasyonel ve finansal akışın kontrol
edildiği en üst düzey arayüzdür.

- **Genel Bakış:** aktif sipariş ve abonelik sayıları, bekleyen işler, günlük
  operasyon özeti, memnuniyet göstergeleri
- **Sipariş Masası:** tüm siparişlerin listesi, filtreleme, detay görüntüleme,
  **personele atama**, iptal ve durum yönetimi
- **Abonelik Yönetimi:** aktif abonelikler, tahsilat durumları, başarısız
  tahsilat takibi, yenileme ve iptal işlemleri
- **Saha Personeli Yönetimi:** personel oluşturma, yetkilendirme, hizmet bölgesi
  tanımlama, aktif/pasif durum yönetimi ve performans takibi
- **Saha Haritası:** açık ve tamamlanmış işlerin harita üzerinde konumsal
  görünümü, bölge yoğunluk takibi
- **Bölge ve Mezarlık Yönetimi:** il / ilçe / mezarlık hiyerarşisi, mezarlık
  kayıtları ve hizmet verilen bölgelerin tanımlanması
- **Galeri Yönetimi:** tamamlanmış işlerin vitrine eklenmesi, görsel yükleme,
  personel etiketleme, yayınlama ve kaldırma
- **Fiyat ve Katalog Yönetimi:** paket tanımları ve fiyatları, aylık/yıllık
  oranlar, bitki ve ek hizmet kataloğu, mermer seçenekleri — tümü panelden
  yönetilir, fiyat değişikliği için yazılım güncellemesi gerekmez
- **İndirim Kodu Yönetimi:** kod oluşturma, oran ve geçerlilik tanımlama,
  kullanım takibi
- **Finansal Raporlama:** ciro, tahsilat, abonelik geliri, paket bazlı dağılım
  ve Excel dışa aktarım
- **Değerlendirme Yönetimi:** müşteri puan ve yorumlarının izlenmesi ve
  yayın kontrolü
- **Rol ve Yetki Yönetimi:** yönetici kullanıcıları ve erişim seviyeleri

---

# 5 · Gereksinimler

## 5.1 · Abonelik ve Tekrarlayan Ödeme Altyapısı

Platformun ticari omurgası. Bakım hizmeti doğası gereği süreklilik gerektirdiği
için sistem, tek seferlik satış ile abonelik satışını **iç içe** yürütecek
şekilde kurulur.

- **Aylık ve yıllık plan yönetimi:** yıllık planlarda indirimli fiyatlandırma
- **Otomatik tahsilat:** ödeme sağlayıcısı üzerinden tekrarlayan ödeme
- **Otomatik yenileme kontrolü:** müşterinin açıp kapatabildiği yenileme tercihi
- **Başarısız tahsilat yönetimi:** yeniden deneme döngüsü, müşteri
  bilgilendirme ve hizmet askıya alma kuralları
- **Ziyaret döngüsü üretimi:** abonelik planına göre ziyaretlerin otomatik
  oluşturulması ve takvimlenmesi
- **İptal ve iade süreçleri**
- **Tek seferlik sipariş** akışının abonelikten bağımsız çalışması

## 5.2 · Saha Operasyonu ve Kanıt Zinciri

Platformun güven iddiasının teknik karşılığı.

- **İş atama:** yönetici tarafından personele atama, bölge ve müsaitlik bazlı
- **Konum doğrulaması:** personelin mezarlıkta bulunduğunun teyidi
- **Zorunlu görsel kanıt:** öncesi görseli yüklenmeden iş başlatılamaz,
  sonrası görseli yüklenmeden iş kapatılamaz
- **Otomatik PDF rapor üretimi:** işlem kapandığında rapor kuyruk üzerinden
  üretilir ve müşteri arşivine eklenir
- **Video rapor desteği:** üst paketlerde video kaydı
- **Sorun bildirimi:** fiziki hasar ve durum tespitinin görselle raporlanması

## 5.3 · Görsel Peyzaj Tasarım Aracı

Müşterinin satın alma kararını görselleştiren ve ek gelir üreten satış aracı.

- Mezar görseli üzerinde mermer rengi ve doku seçimi
- Hazır peyzaj şablonlarının uygulanması
- Toprak alanına bitki yerleştirme ve kaldırma
- Baş taşına isim ve tarih yazımı önizlemesi
- **Canlı fiyat hesaplama:** seçilen her kalemin bedeli anında toplanır
- Seçimin sipariş akışına taşınması ve pakete eklenmesi
- Bitki ve seçenek kataloğunun yönetici panelinden yönetilmesi

## 5.4 · Bölge, Mezarlık ve Harita Yönetimi

- **81 il ve ilçe hiyerarşisi:** hizmet verilen bölgelerin tanımlanması
- **Mezarlık kayıt yönetimi:** mezarlık ekleme, konum tanımlama, hizmet durumu
- **İnteraktif harita:** müşteri tarafında bölge keşfi, yönetici tarafında
  operasyon takibi
- **Mezarlık adıyla arama** ve bölge bazlı filtreleme
- Personelin hizmet bölgesi eşleştirmesi

## 5.5 · Bildirim ve Performans Katmanı

- **Anlık bildirim (Push):** iki mobil uygulama için ayrı bildirim kanalları
- **SMS bildirim ve doğrulama:** telefon doğrulama, kritik durum bilgilendirmesi
- **E-posta bildirim:** rapor hazır, tahsilat, abonelik hatırlatma
- **Mesaj kuyruğu (RabbitMQ):** PDF rapor üretimi, toplu bildirim ve abonelik
  tahsilat döngüsü gibi yoğun işlemlerin sistem performansını etkilemeden arka
  planda yönetilmesi
- **Önbellek (Redis):** mezarlık listesi, paket ve katalog gibi okuma ağırlıklı
  verilerin hızlı sunulması

## 5.6 · Yasal Uyum ve Veri Yönetimi

- KVKK aydınlatma metni ve açık rıza yönetimi
- Mesafeli satış sözleşmesi ve dijital onay kaydı
- **Hesap silme akışı:** mobil mağaza politikalarının zorunlu kıldığı süreç
- Yasal saklama yükümlülüğü olan verilerin ayrıştırılması
- Kişisel verilerin sipariş kaydından ayrı yönetimi

---

# 6 · Proje Süresi

Projenin tüm fikri mülkiyet ve know-how hakları Müşteriye aittir. Bu nedenle
proje süreci, modüllerin önceliklendirilmesine ve Müşteri onaylarına bağlı
olarak ilerleyecektir.

Her modül ve aşamada etkin test, onay ve aksiyon süreçleri yürütülecektir.
Geliştirme süreci her üç haftada bir milestone (kilometre taşı) ile
yapılandırılacak; her milestone sonunda tamamlanan modüller test ortamına
alınarak Müşteriye sunulacak ve değerlendirme toplantısı düzenlenecektir.

**Proje toplam süresi 6 ay (24 hafta) olarak planlanmaktadır.**

## 6.1 · Plan

- **Proje Dokümantasyonu:** 3 hafta
- **Tasarım & Prototip Süreci:** 5 hafta
- **Yazılım Geliştirme:** 14 hafta
- **Test, QA & Yayına Alma:** 2 hafta

Tüm fazlar boyunca her üç haftada bir milestone gerçekleştirilecek; tamamlanan
modüller Müşteri ile birlikte test ve değerlendirme toplantısında gözden
geçirilecektir.

⚠️ **Mobil uygulama mağaza süreçleri:** iOS App Store ve Google Play Store
inceleme süreleri platform sağlayıcılarının kontrolündedir. Bu süreler proje
takvimine dahil edilmemiştir.

## 6.2 · Proje Başlangıç Tarihi

Sözleşmenin imzalanması durumunda, dokümantasyon süreci **15.09.2026** tarihi
itibarıyla başlatılabilir durumda olacaktır.

---

# 7 · Ek Ücretler & Bakım

## 7.1 · Güncelleme ve Akış Değişimleri

Proje geliştirme süresinde karar verilenden farklı bir akış istenmesi
durumunda projeye ek maliyetler oluşabilecektir.

Karar kriteri, proje dokümanına ek olarak demo hazırlanan proje tasarımı
olacaktır. Backend yazılımına geçildikten sonra yapılacak tasarım ve işleyiş
değişimleri projede ek maliyet yaratacaktır.

Proje kapsamının tasarım aşamasında genişletilmek istenmesi durumunda ek
maliyetler oluşacaktır.

## 7.2 · Bakım İşlemi

Uygulama yayına alındıktan sonra **3 ay boyunca** PR Yazılım hata giderme
garantisi altındadır. Bu süreç içerisinde yazılımsal bir bug bulunması
durumunda PR Yazılım tarafından ücretsiz düzeltilecektir.

**Garantiye dahil olmayan işlemler:**
- Versiyon güncellemesi sebebi ile oluşan sorunlar
- Akış, tasarım, metin ya da veri değişimleri
- Ek modül eklenmesi işlemleri
- Modüllere ek veri eklenmesi işlemleri

**Garanti sonrası bakım anlaşması:**

Proje yayına alındıktan sonra aylık bakım anlaşması yapılabilir. Bu anlaşma ek
bir sözleşme olacaktır.

**Aylık Bakım Bedeli: 500 $ + KDV**

Bakım anlaşması kapsamı:
- Yazılımsal hata giderme (bug fix)
- Sistemin ayakta tutulması, servis ve altyapı izleme
- Kütüphane ve güvenlik güncellemeleri
- Mobil uygulama işletim sistemi uyum güncellemeleri

⚠️ **Bakım anlaşması yeni geliştirme içermez.** Yeni modül, akış değişikliği,
tasarım revizyonu ve içerik geliştirmeleri adam-saat üzerinden ayrıca
ücretlendirilir.

**Adam Saat Karşılığı: 40 $ + KDV**

---

# 8 · Kaynak Kod

Proje alt yapısı PR Yazılım'a ait birçok deneyim içerecektir. Bu nedenle proje
kaynak kodlarının devri istenirse ek ücret talep edilecektir. Bu ücrete;

- Yeni ekip eğitim masrafları (1 ay)
- PR Yazılım'a ait teknolojilerin ulaşılabilir ve kullanılabilir hale
  getirilmesi süresi

dahil olacaktır. Proje geliştirme sürecinde yaşanan tüm deneyimlerin
aktarılması dahildir.

---

# 9 · Teklif

## 9.1 · Baz Paket

**Mezarlık Bakım ve Hizmet Platformu — Versiyon 1**

Kapsam:
- Web Sitesi & Müşteri Üye Alanı
- Müşteri Mobil Uygulaması (iOS + Android)
- Saha Personeli Mobil Uygulaması (iOS + Android)
- Yönetici Paneli
- Bakım hizmeti hattı (abonelik + tek seferlik, iç içe)
- Abonelik ve tekrarlayan ödeme altyapısı
- Saha operasyonu ve zorunlu görsel kanıt zinciri
- Otomatik PDF rapor üretimi
- Görsel peyzaj tasarım aracı
- Bölge, mezarlık ve harita yönetimi
- Fiyat ve katalog yönetimi
- İş galerisi (vitrin)
- Bildirim altyapısı (push + SMS + e-posta)

**BAZ PAKET TOPLAM: 300.000,00 ₺**

## 9.2 · Ek Hizmetler

Aşağıdaki modüller baz pakete dahil değildir; talep edilmesi durumunda ayrıca
fiyatlandırılır. Baz paket mimarisi bu modüllerin sonradan eklenmesine uyumlu
olarak tasarlanır.

**Mezar Taşı Satış Hattı**
Galeriden model seçimi, sipariş oluşturma, online ödeme, üretim ve kurulum
aşamaları takibi, tamamlanma raporu. Bakım hattından bağımsız ikinci ürün
hattı.

**Dış Tedarikçi (Usta / Esnaf) Ağı Modülü**
Kuruma bağlı olmayan dış ustaların sisteme dahil edilmesi: başvuru ve onay
süreci, tedarikçi paneli, hizmet bölgesi talep yönetimi, iş dağıtım havuzu,
hakediş ve komisyon hesaplaması, IBAN ve ödeme takibi, dijital tedarikçi
sözleşmesi.

**Saha Uygulaması Çevrimdışı Çalışma**
Şebeke bulunmayan mezarlıklarda görsel çekimi ve iş kaydının cihazda
tutulması, bağlantı sağlandığında otomatik yükleme.

## 9.3 · Ödeme Planı

- Proje bedelinin **%50'si**, sözleşmenin imzalanması ile peşin olarak
  ödenecektir.
- Kalan **%50'lik** tutar, proje süresi (6 ay) boyunca aylık fatura karşılığı
  **6 eşit taksit** halinde ödenecektir.

## 9.4 · Teklif Koşulları

- Fiyatlara KDV dahil değildir.
- Proje ödemesi birçok hizmet ödemesi ile yapılacağı için her ayın ilk 5
  gününde yapılması gerekmektedir. Yapılacak ödemelerin gecikmesi durumunda
  çalışmalar kesintiye uğrayacaktır.
- Sunucu, SMS, e-posta, ödeme sağlayıcısı ve görsel depolama bedelleri proje
  bedeline dahil değildir; ilgili sağlayıcılar tarafından ayrıca
  faturalandırılır.
- Teklif, teklif tarihi itibariyle **10 gün** içinde sözleşmenin imzalanması
  ile geçerlidir.
