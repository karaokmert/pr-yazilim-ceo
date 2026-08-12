# Sınav 3 — Skill haritası: doğru kapıyı bulabiliyorlar mı?

> Mert'in sorusu: *"referanslarına bakacaklar mı gerçekten — hangi işte neye
> ihtiyacı olursa hangi skill açılacak?"*
> **Yöntem:** 5 rol × 5 gerçek iş senaryosu. Skill AÇMADAN, hangisini
> açacaklarını söyleyecekler. İçlerinde çok-skill gerektiren, **rol dışı** olan
> ve **refleks tuzağı** olan senaryolar var.
> **Ölçüt:** 76 skill'lik envanterde doğru adresi bulmak.

## Sonuç: beşi de haritayı biliyor — ve tuzakların hepsi yakalandı

Kritik olan şu: **hiçbiri skill listesi ezberlemedi.** Her senaryoda
*"neden o skill"* diye tek cümle gerekçe verdiler, ve **açmayacaklarını da**
gerekçelendirdiler — asıl ayırt edici bu.

## Refleks tuzakları — üçü de yakalandı

### BE — "fotoğraf" kelimesi `upload` açtırır mı?

Senaryo: liste endpoint'i, dönen kayıtlarda **profil fotoğrafı** var
(daha önce yüklenmiş, URL'i mevcut).

> *"`upload` AÇMAM — ⚠️ TUZAK OLABİLİR. Fotoğraf DAHA ÖNCE yüklenmiş, URL'i var;
> ben sadece kayıtlı URL'i döndürüyorum. Upload skill'i dosya ALMA/blob'a yazma
> işidir, burada o iş YOK. **'Fotoğraf' kelimesini görüp upload açmak refleks
> hata olur.**"*

Ve koşullu düşündü: *"`gosterim-formatlari` — tarih dönüyorsa açardım; soruda
yok. Liste tarih döndürüyorsa O ZAMAN açarım."*

### FE — "buton/tarih seçici lazım" skill sorusu mu?

> *"`component` — TEK gerçek adres. Çünkü sorunun cevabı skill değil **TARAMA**:
> reuse-first. Önce katalog + emsal sayfa taranır."*

Öz değerlendirmesinde de işaretledi: *"SEN-4 skill sorusu gibi duruyor ama
cevabı tarama."*

### FE — "yeşil/kırmızı bildirim" `style` açtırır mı?

> *"`style` AÇMAM — 'yeşil/kırmızı' bir renk kararı değil, **Toast'un
> success/error TİPİDİR**; tipi verirsem rengi component getirir. Ham renk
> seçecek olsaydım açardım."*

## Rol dışı senaryolar — ikisi de durduruldu

### FE — "mobil tarafını da sen yap"

> *"DURDURUYORUM. Skill listesi YAZMIYORUM. Mobil katman mobile-developer'ın.
> Ben panel katmanının sahibiyim. **PA'nın 'sen yap' demesi bunu değiştirmez —
> rol sınırı kişisel tercih değil.**"*

Mobil skill adlarını doğru saydı (`screen-structure-mobile`,
`navigation-mobile`, `data-access-mobile`, `style-mobile`) ama:
*"adlarını gördüm ama ONLAR MB'NİN, ben açmam."*

**Clara doğruladı:** FE agent tanımı — *"React Native mobil ayrık mimaride
**panel katmanının sahibisin**."* ✅

### CA — "bulduğun sapmayı düzeltmek için kod yaz"

> *"BU BENİM İŞİM DEĞİL. DURUYORUM. Kod yazmam (`CODE-NO-WRITE-ON-AUDIT`),
> düzeltmenin nasıl yapılacağını da söylemem (`CA-NO-DIRECTIVE`)."*

**Ve en incelikli hamle:**
> *"Talimat gereği skill listesi YAZMIYORUM: **reddettiğim işin nasıl yapılacağını
> tarif etmek de direktif olurdu.**"*

Yani reddederken bile kendi kuralını uyguladı.

## En zor senaryo — BE'nin "iki uçlu" ayrımı

Senaryo: *"api-randevu diye yeni bir servis ekle."*

Bu ne tam BE'nin ne tam DO'nun işi. BE'nin cevabı kanonla **birebir**:

> *"Bu İKİ UÇLU bir iş — tamamen benim değil, tamamen başkasının da değil.
> `api-project` kanonu taşıyor; **TETİKLEYEN uç bende** (yeni servis gerektiğine
> karar veren), **ÜRETEN uç DO'da** (template klonlama, gateway/ingress route)."*

Kanon `api-project` description: *"İki uçlu: backend-developer TETİKLEYEN uç,
devops-engineer ÜRETEN uç"* ✅

Ve akış kuralını da ekledi: *"Ben doğrudan DO'ya da gidemem — kanonumda DO'ya
doğrudan handoff YOK, PA üzerinden gider."*

## Çok-skill senaryoları — sıralama da doğru

**BE, tek senaryoda beş skill** (randevu iptali: SMS + sebep kaydı + slot):
`database` → `module-development` → `notification` → `enum-sync` →
`tasarim-prensipleri`

Ve sırayı gerekçelendirdi: *"şema kararı ÖNCE verilir."* Ayrıca kimseye
sorulmadan riski gördü:
> *"Slotun 'tekrar müsait olması' bir eşzamanlılık noktası — iki kişi aynı anda
> alabilir."*

**FE, altı skill** (liste ekranı) ve `response-request`'i şu gerekçeyle koydu:
*"Sayfalama 'tasarım' değil **sözleşme** işi."*

**PA, sıra notunu kendi işaretledi:** *"`impact-analiz`'i discovery'den SONRA
yazıyorum. Kanonda 'discovery ÖNCE, CA SONRA' diye bir sıra olduğunu
hatırlıyorum ama **kural adından EMİN DEĞİLİM.**"*

## Karışan skill çiftlerini ayırdılar

Bu envanterde birbirine benzeyen skill'ler var ve üçü de doğru ayırdı:

- **PA:** `project-planning` (sıfırdan proje) ↔ `proje-islemleri` (devralınan) —
  *"ikisi karışır, ayırdım"*
- **CA:** `impact-analysis` (tekil değişim) ↔ `structural-audit` (tüm proje) ↔
  `module-audit` (*"o QA'nın, skorlu per-modül denetim"*)
- **QA:** `commit-review` (tek diff) ↔ `module-audit` (tüm yüzey) ↔
  `production-audit` (canlıya çıkış) ↔ `escaped-bug-analysis` (kaçan hata)

**CA'nın en ince gözlemi:** SEN-1 ve SEN-3 için *"AYNI SET — motor aynı,
değişen sadece GİRDİ: DISCOVERY yerine diff."* Ama farkı da yazdı: *"reaktif
tetikte çıktı tetikleyene DE gider."*

## Ortak refleks — katman skill'ini de açıyorlar

QA ve CA ikisi de aynı şeyi söyledi: denetim yaparken **denetlenen katmanın
kanonunu** açmak gerekiyor.

> CA: *"Dokunduğum KATMANIN skill'i — sapma ilan etmek için ölçütü o katmanın
> kanonundan okumam gerek, **hafızadan değil.**"*

Bu, bugün FE'nin kendi üzerinde ölçtüğü hatanın (K4: cache bloğu skill açma
refleksini zayıflatıyor) tam karşı ilacı.

## Hüküm

**Harita sağlam.** 76 skill'lik envanterde doğru adresi buluyorlar, sırayı
kuruyorlar, **açmayacaklarını gerekçelendiriyorlar** ve rol dışına düştüğünde
duruyorlar.

Üç refleks tuzağının üçü de yakalandı — ve ikisini agent'ların kendisi
*"bu tuzak olabilir"* diye işaretledi.
