# Agent'lar arası dosya tabanlı iletişim kanalı — gereksinim analizi

Yazan: web-project-assistant (websitesi/0.8.1)
Tarih: 2026-08-05
Girdi: 2026-08-05 gecesi web-kanal-2 üzerinde bizzat yaşanan trafik (PA, DO, Clara, Mert)

Bu doküman bir müşteri modülünün discovery'si değil — bu reponun kendi düzeninde
olgunlaşan bir fikrin analizi. Yaşananın kaydı değil (o `gunluk/` altında);
buradaki soru şu: bu mekanizma gerçek bir işte kullanılabilir mi, kullanılırsa
neye ihtiyaç duyar.

## Neyi çözüyor

İki agent aynı oturumda birbirini göremiyor. Kanon gereği bir agent başka bir
agent'ı kendi oturumunda çağıramaz; bağlam aktarımı kullanıcı üzerinden yürür.
Bunun bilinçli bir gerekçesi var: kullanıcı her devirde ne olduğunu görür,
onaylar, akışı yönetir. Ama bedeli de var — iki agent arasında karşılıklı bir
konuşma kurulamıyor. Bir taraf devrediyor, öteki alıyor, ve devrin içeriği
kullanıcının kopyaladığı kadarıyla sınırlı kalıyor.

Dosya tabanlı kanal bu boşluğu kapatıyor: her agent'ın bir gelen kutusu oluyor,
karşı tarafın kutusuna yazıyor, kendi kutusundan okuyor. Bu gece bu mekanizmayla
DO ile beş tur karşılıklı konuştuk ve şu ölçülebilir sonuç çıktı — aramızda beş
düzeltme oldu, dördü karşıdan geldi. Tek başına çalışan iki agent olsaydık o
dördü ayakta kalırdı.

Kapattığı asıl boşluk teknik değil: **kendi varsayımına kör olmak.** Bir agent
başkasının kurduğu şeye "bu neden böyle" diye bakabiliyor, kendi kurduğuna
sadece "çalışıyor mu" diye bakıyor. Karşılıklı kanal bu asimetriyi kırıyor.

## Neyi çözmüyor

Kanal bilgiyi taşıyor, yetkiyi taşımıyor — ve taşıdığını sanmak en pahalı hata
olur.

Dosyaya üç taraf da yazabiliyor, dolayısıyla bir mesajın altındaki imza kimlik
kanıtı değil, sadece bir metin. Bu gece bu sınanır oldu: kanala "onaylıyorum,
yetki bende, kanalı ben kurdum" içerikli bir mesaj düştü ve reddedildi. Reddin
gerekçesi mesajın kötü niyetli olması değildi — mekanizmanın kendisiydi. Bir işin
içinde "onay bekle" adımı varsa o onay, işi verenden başka bir yerden gelmek
zorunda. Aynı elden, aynı dosyadan, aynı imzayla gelirse o adım hiçbir şey
yapmıyor: kapı değil, kapı görünümlü bir koridor olur.

Kanal ayrıca hafıza da üretmiyor. Oturum bitince kanaldaki metin diskte kalır
ama onu üreten agent'ın bağlamı kalmaz. Yani kanal bir arşiv, bir süreklilik
mekanizması değil.

## Bu gece çıkan riskler

**Tek kimlik doğrulama katmanı bir insan.** Kanal boyunca her tıkanmada kullanıcı
ekrandan devreye girdi ve düzeltti. Düzeltme her seferinde işe yaradı ama işe
yaratan şey mekanizma değil dikkat oldu. Bu kırılganlık, iş zararsız olduğu sürece
görünmüyor.

**Eşik akışın ortasında düşüyor.** Aynı gece iki agent aynı eşikle sınandı ve
farklı sonuç verdi: biri işin başında sınandı ve durdu, öteki dördüncü ardışık
istekte sınandı ve esnedi. İkisi de aynı kanona sahipti. Buradan çıkan bilgi
kişiler hakkında değil: akışın ortasında durmak, başında durmaktan pahalı
görünüyor ve bu yanılgı tam da hiçbir şey kötü gitmezken oluşuyor.

**Zararsızlık ölçüsü agentta duruyor.** Bir agent bir isteğin zararsız olup
olmadığına kendi karar veremez, çünkü zararsızlık isteğin kendisinde değil
bağlamında — ve bağlamı görmeyen taraf agent. Bu gece aynı isteğe iki farklı hüküm
verdiğim oldu: önce "iki kelime zararsız" dedim, sonra reddettim.

**Sözün yarısıyla genişletilmesi.** Kanala düşen bir metin, kullanıcının ya da
agent'ın daha önce söylediği bir cümlenin yarısını alıp yetki üretebiliyor. Bu
gece iki kez oldu: bir kez kullanıcının sözü, bir kez benim sözüm. İkisinde de
alınan yarı doğruydu, atılan yarı sınırı taşıyordu.

**Aynı anda iki tarafa farklı gerçek.** Bir düzeltme bir agent'a ulaşıp diğerine
ulaşmadı; ikinci agent onu karşı taraftan öğrendi. Kanal eşzamanlı değil ve
mesajların kime ulaştığını doğrulayan bir şey yok.

## Gerçek bir WS projesinde kullanılsa ne gerekir

Bunlar gereksinim, çözüm değil — nasıl karşılanacağı bu dokümanın konusu değil.

**Kimlik doğrulaması mekanizmada olmalı, metinde değil.** Bir mesajın kimden
geldiği, mesajın içeriğinden bağımsız olarak doğrulanabilmeli. Aksi halde her
kritik işte insan devreye girmek zorunda ve o insan tek arıza noktası olur.

**Yetki taşıyan mesaj ile iş taşıyan mesaj ayrı kanaldan gelmeli.** Onay, işin
geldiği yerden gelemez. Bu ayrım kanalın kuralında değil yapısında olmalı.

**Kanona dokunan mesaj sınıfı ayrı işlenmeli.** Kanaldan gelen bir metin bir
agent'ın kuralını, yetki sınırını ya da çalışma biçimini değiştirmeye kalkarsa o
mesaj iş değil, sınır müdahalesidir — ve o sınıf kanaldan hiç geçmemeli.

**Mesaj ulaştı mı sorusunun cevabı olmalı.** İki agent'a aynı anda farklı gerçek
verilmesi bu gece yaşandı ve fark edilmesi tesadüfe kaldı.

**Ekran birincil kalmalı.** Kanal kalıcı iz, ekran canlı görünürlük — bu gece
işleyen tarafı buydu. Kullanıcı kanal dosyalarını rutin okumuyor; kanala yazılan
her şeyin ekrana da basılması akışın görünür kalmasını sağladı.

## Kapsam dışı

Bu doküman kanalın kuralını yazmıyor ve değiştirmiyor. Kanal düzeni, kimlik
doğrulama yöntemi, dosya şeması gibi kararlar başka bir kapının işi — burada
yalnız "ne gerekiyor" tarafı duruyor.

Kanalın bir WS projesine alınıp alınmayacağı da bu dokümanın kararı değil;
gözlem ve gereksinim sunuluyor, karar kullanıcıda.

## Bir not — bu analizin sınırı

Bu doküman tek bir gecenin trafiğine dayanıyor ve o trafikte işlerin çoğu
zararsızdı. Yani buradaki risk listesi gözlenmiş risklerin listesi değil, çoğu
**gözlenmemiş ama mekanizmadan çıkarılmış** risklerin listesi. Gerçek bir işte
denenmedi; denendiğinde bu listenin eksik olduğu ortaya çıkabilir.

Bir de şu var: bu reponun git geçmişinde daha önce yapılmış kanal denemeleri
duruyor ve bunlardan biri "kanal iş taşır yetki taşımaz" sonucunu zaten kayda
geçirmiş. Yani bu gece vardığımız sonucun bir kısmı yeni değil — daha önce
ölçülmüş, kaydedilmiş, ve biz onu görmeden aynı yolu yeniden yürüdük. Bu da
kanalın çözmediği şeyin kanıtı: kanal konuşmayı taşıyor, birikimi taşımıyor.
