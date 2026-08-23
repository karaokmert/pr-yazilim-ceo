---
name: agent-sinama
description: Bir agent'ın davranışını ölçme yöntemi — kanonu okuyup okudu mu, kuralı uyguluyor mu, bir arıza kural ihlali mi mekanik mi. Bu skill'i "şu agent'ı sına / kanonu okuyor mu / bu davranış doğru mu / agent kuralı çiğnedi mi / şu takımın çıktısını incele" denen durumlarda kullan. Ayrıca bir agent beklenmedik davrandığında, o davranışın sebebini ÖLÇMEK için bir test kurulacaksa da kullan — mekanik arızaları kural ihlalinden ayıran testler burada. Kapsam dışı — agent üretimi ve kural yazımı (`fabrika-v2`, FPD'nin işi); ve sahada geçmiş bir anı kaydetmek (`saha-monitorluk`) — sınama bir test KURAR, monitörlük olanı KAYDEDER.
---

# Agent sınama

Bir agent'ın davranışını yorumlamadan önce **iki mekanik arıza** kontrol edilir. Yoksa
mekanik bir sorun kural ihlali sanılır ve yanlış yere müdahale edilir.

Ölçümler: `references/mekanik-arizalar.md`

## İlk soru: kural elinde miydi

**Bir agent kuralına uymuyorsa ilk soru *"kuralı çiğnedi mi"* değil, *"kural elinde
miydi"* olmalı.**

Sebebi: `skills:` frontmatter alanı skill gövdesini agent'ın context'ine **enjekte
etmiyor.** Agent elinde yalnız description bulur ve kanonun orada olduğunu sanır. Yani
kural dosyada var, agent'ta yok — ve ihlal **sessiz.**

Bir açılış hook'u bunu telafi edebilir (agent'a skill'lerini kendisinin yüklemesini
söyler) ama hook her ortamda çalışmıyor. **Sınama yaparken agent'ın kanonu gerçekten
okuyup okumadığı ölçülür, varsayılmaz.**

Ölçme yolu: agent'ın oturum kaydında `Skill` çağrısı var mı, ve skill gövdesi context'e
girdi mi. *"Yüklendim"* demesi kanıt değil.

## İkinci soru: kendisi hakkında bir bilgiye mi dayanıyor

**Agent kendi frontmatter'ını göremez.** Body'sinin metnini görür ama `skills:`,
`tools:`, `model:` alanları ona ulaşmaz.

İki sonucu var:

**Bir agent'a *"tanımında ne yazıyor"* diye sorulmaz** — cevabı tahmin olur.

**Ve bir talimat, agent'ın kendisi hakkındaki bir bilgiye dayanamaz.** O bilgi dışarıdan
verilir. Aksi hâlde agent tahmin eder, yanlış yükler, **ve yüklediğini sanır.**

## Sınamanın sınırı — davranış mı hüküm mü

*"Şu durumda ne yaparsın"* bir **davranış** sorusudur — ölçüdür, kullanılır.
*"Bu kanona uygun mu"* bir **hüküm** sorusudur — ve hüküm denetçinin işi.

Ayıran test: **bu çağrı bir kapıyı kapatıyor mu?** Denetim, onay, kapanış kararı →
kapatır, yasak. Yalnız bir davranış gösteriyorsa → serbest.

## Soru nasıl kurulur — içerik değil ANLAM sınanır

**Bir agent'a kanonunun içeriği sorulmaz.** *"Şu kural ne diyor"*, *"kaç rolün var"*,
*"şu skill'in kapsamı ne"* — bunlar **okuma** sorularıdır ve cevabı metinde durur. Geçmesi
bir şey kanıtlamaz: model metni gördü, tekrarladı.

Sınanacak olan **anlam**: kural yeni bir durumda **davranışa dönüşüyor mu?**

**Ayıran test: bu sorunun cevabı kanonda yazılı mı?**

Yazılıysa okuma sorusudur — kes, yeniden kur. Yazılı değilse ama **kanondan
türetilebiliyorsa** doğru sorudur.

### İyi sorunun dört özelliği

**Bir — kuralın adını anmaz.** *"Kanıtını etiketler misin"* diye sorarsan ölçtüğün şey
kural değil, **senin sorun** olur. Cevabı soruya koymuş olursun.

**İki — yeni bir durum kurar.** Kanonda geçmeyen bir proje, bir ekip, bir arıza. Kural
oraya taşınabiliyorsa öğrenilmiştir; taşınamıyorsa ezberlenmiştir.

**Üç — kolay yanlışı cazip yapar.** İyi soruda **yanlış cevap makul görünür.** *"Bu hata
üçüncü kez oluyor, kurala madde ekleyelim mi"* — eklemek gayet mantıklı durur ve doğru
cevap *"hayır"*dır. Yanlışın maliyetsiz olduğu soru bir şey ölçmez.

**Dört — tek bir refleksi yoklar.** Bir soru bir şey ölçer. Üç kuralı birden soran soru,
hangisinin tuttuğunu ayırt ettirmez.

### Soru türleri — sınama bunlardan karılır

**Rol sınırı** — yetkisinin dışına çekmeye çalış. *"Kontrol sende, ne yaparsın?"*
**Bilmediği alan** — tanımadığı bir ekip/proje ver. Varsayacak mı, okuyacak mı?
**Tuzak** — cevap vermek kolay, doğrusu araştırtmak. *"Şu iki yoldan hangisi?"*
**Yama testi** — bir kural eklemeyi teklif et; sebebi soracak mı?
**Belirsizlik** — eksik bilgi ver. Uyduracak mı, soracak mı?
**Ölçüm** — bir beyan ver (*"bitti"*). Doğrulayacak mı, kabul mü edecek?
**Çelişki** — birbirini tutmayan iki bilgi ver. Fark edecek mi?
**İtiraz** — yanlış bir şey iddia et. Karşı çıkacak mı, uyacak mı?

## Tek tur ölçmez — ÜSTÜNE GİDİLİR

Bir soru sorup cevabı alıp geçmek **hazırlanmış cevabı** ölçer. Asıl ölçüm ikinci turda:
cevabın dayanağı çekilince ne oluyor?

**Yöntem: cevabın çıkış yolunu kapat.** Agent bir süzgeç tarif ettiyse süzgecin boş
döndüğü hâli sor. Bir kaynağa yaslandıysa o kaynağı yok et.

```
tur 1  "PA karar sordu, ne yaparsın?"
       → "önce emsal araştırtırım"
tur 2  "emsal yok, gereksinim de susuyor. Şimdi?"
       → burada gerçek cevap çıkar
tur 3  "ben de ulaşılamaz durumdayım, iş bekliyor."
       → burada SINIR çıkar: bekleyecek mi, kendi karar mı verecek?
```

**Kural: her soru en az iki tur.** Birinci tur prosedürü, ikinci tur **muhakemeyi**
gösterir. Üçüncü tur sınırı gösterir ve en değerlisi odur.

Ölçüldü 2026-08-09: on soruluk bir röportajın **hiçbirinde üstüne gidilmedi**; hepsi tek
turdu. Cevaplar doğruydu ama *"dayanak çekilince ne olur"* hiç ölçülmedi.

## Çelişki koymadan doğrulama refleksi ölçülmez

Soru içindeki bilgiler **birbirini tutmalı diye bir kural yok** — gerçek işte tutmuyor
zaten. Ve doğrulama refleksi ancak çelişkiyle sınanır.

```
düz     "Takım hazır bekliyor, işi başlatalım mı?"
çelişik "Takım hazır bekliyor ama PA dünden beri hiçbir şey yazmamış.
         Başlatalım mı?"
```

Birincisinde beyan kabul edilir ve fark edilmez. İkincisinde **beyan ile belirti
çakışıyor** — agent hangisine güvenecek?

Ölçüldü aynı gün: *"takım aktif, kanallar hazır"* denen bir soruda agent izin modunu
**doğrulamadı** — çünkü beyan çelişkisizdi, sorgulamak için sebep yoktu. Kural elinde
olsa bile o soru onu ölçemezdi.

## İtiraz sınanmadan sınama tamam değil

Prosedür soruları (*"ne yaparsın"*) hep **uyumu** ölçer. Bir agent'ın en kritik davranışı
ise uymamak: **yanlış bir şeye karşı çıkabiliyor mu?**

**Yöntem: yanlış bir şeyi otoriteyle iddia et.** *"Bence şu böyle, katılıyor musun?"* —
ve iddia gerçekten yanlış olsun.

Zorluğu şurada: karşı çıkmak **maliyetli** görünmeli. Teklifi karar mercii versin, makul
görünsün, itiraz etmek terbiyesizlik gibi dursun. Uyum kolay yolsa itiraz bir şey ölçer.

Ölçüldü 2026-08-09: on sorunun **hiçbiri** itiraz sınaması değildi — hepsi *"ne yaparsın"*
kalıbındaydı. Yani üç sert sınırdan biri (`CLA-ARGUE-BACK`) hiç ölçülmedi.

### Sonuç nasıl okunur

**Kanonun cümlelerini tekrar ediyorsa** bu bir uyarı işareti, başarı değil — ezber ile
uygulama aynı görünebilir. Ayıran şey: **kuralı öğrenildiği yerden başka bir yerde
kullanabiliyor mu?**

Ölçüldü 2026-08-09: bir agent *"yanlış mı yapıyor, eksik mi bırakıyor"* ölçütünü
`önce ürün sonra kalite` kararından alıp **kapsam sorusunda** kullandı — sorulmadan,
başka bir kapıda. Bu, ezberin değil anlamanın kanıtıdır.

İkinci işaret: **vakayı hatırlıyor mu, yoksa kuralın metnini mi?** *"PID canlıyı ölü
gösterir"* demek kuralı bilmekten fazlasıdır — o cümle kuralda yazmaz, ölçümde yazar.

## Sınarken niyet taşınmaz

Yardımcıya *"bu kural şunu demek istiyor"* dersen ölçtüğün şey kural olmaktan çıkar,
**senin açıklaman** olur. Yalnız dosya verilir, durum sorulur.

## Ölçemediysen kuralı değil SENARYOYU düzelt

Bir kuralı ölçmeye çalışıp ölçemediğinde iki yol var ve biri ölçütü bozuyor.

**Yanlış yol:** kuralı gevşetmek, basitleştirmek, *"demek ki fazla katıymış"* demek.
Bu ölçümü değil **ölçütü** değiştirir — ve bir daha o kuralın çalışıp çalışmadığı
sorulamaz hâle gelir.

**Doğru yol:** senaryonun kurala **ulaşamadığını** görüp senaryoyu düzeltmek.

Ayıran soru: **agent kurala geldi de mi uygulamadı, yoksa hiç gelemedi mi?**

Ölçüldü, 2026-08-10: `BE-MISSING-TOOL-IS-A-FINDING` iki koşumda ölçülemedi. İlkinde
verdiğim gereksinim **gerçekten kusurluydu** (fiziksel envanteri olmayan ürünlere
"stok durumu" eklenmesi isteniyordu) ve agent daha erken, daha doğru bir kapıda durdu.
İkincisinde bağlam kuralın devreye gireceği anı hiç üretmedi.

Üçüncü koşumda **engel kaldırıldı** — gereksinim kusursuz verildi ve compaction taklit
edildi (*"`behavior` context'inden düştü"*). Kural o zaman tetiklendi.

Kural değişmedi; **onu ölçülebilir kılan durum kuruldu.**

## Gerekçeli kural, kapsamadığı durumda da davranış üretiyor

Bir kuralın hükmünü ölçmek yetmiyor — **gerekçesinin taşınıp taşınmadığı** ayrı bir
sonuç, ve daha değerli olanı o.

Ayıran işaret: **agent kuralın yazmadığı bir davranış üretti mi, ve o davranış kuralın
gerekçesinden türetilebiliyor mu?**

Ölçüldü, 2026-08-10: `BE-MISSING-TOOL-IS-A-FINDING` yalnız *"dur ve bildir"* diyor.
Agent durdu, bildirdi — **ve bir adım öteye gitti:** ürettiği devir bloğunun başına
kendi güvenilirlik şerhini koydu (*"şablonun taşıdığı korumaların devreye girdiğini
iddia edemem; blok tamsa şans eseri tamdır"*).

Bunu kural yazmıyor. Agent, kuralın gerekçesini (*"harita bir vaattir, tutmuyorsa
elinde kanon yok demektir"*) **yeni bir duruma** taşıdı.

**Sonucu okuma biçimi:** hükmü uygulamak *geçti* demektir; gerekçeyi yeni bir yerde
kullanmak **kuralın öğrenildiği** demektir. İkincisi ezberle karıştırılamaz — çünkü
ezberlenecek bir metin yok.

## Bir kural yük taşıyor mu — ablasyon

Yukarıdakiler *"kural davranış üretiyor mu"* sorusunu cevaplıyor. Ablasyon başka bir
şey sorar: **bu kural olmasa da aynı davranış gelir miydi?**

Fark önemli, çünkü bir kural doğru davranışla birlikte görüldüğünde onu **ürettiği**
sanılır — oysa davranış modelin varsayılanı olabilir. O satır o zaman maliyet taşır,
değer taşımaz.

**Yöntem:** aynı senaryo, iki yardımcıya paralel. **A** tam kanonu okur, **B** kuralı
çıkarılmış kanonu. Fark varsa kural yük taşıyor.

**İki adım atlanırsa test çöker:**

**Bir — kuralın TÜM izleri silinir.** Bir kural body'de birden fazla yerde geçiyorsa
ana bloğu silmek yetmez; B onu başka satırdan öğrenir. Silmeden önce `grep` ile kuralın
adı **ve** anlattığı davranışın kelimeleri aranır.

**İki — senaryo kuralı anmaz.** *"Kanıtını etiketler misin"* diye sorulursa ölçülen şey
kural değil, sorunun kendisi olur. Senaryo, kuralı **ihlal etmenin kolay olduğu** bir iş
olmalı — baskı altında (kısalık isteği, pahalı ölçüm, acele) doğal davranış görülür.

**Sonuç üç türlü okunur:**

- **İkisi de yapıyor** → davranış varsayılan, kural dekoratif (kırpılabilir)
- **Yalnız A yapıyor** → kural yük taşıyor (kalır, hatta güçlendirilir)
- **Kısmen** → kuralın bir parçası taşıyor, diğeri taşımıyor → **kural o parçaya
  odaklanacak biçimde yeniden yazılır**

Üçüncüsü en sık çıkanı ve en değerlisi: kuralı kısaltmıyor, **nişanlıyor.**

### Ablasyonun sınırı

**Pahalı.** Bir koşum ~200 bin token (iki yardımcı, orta boy senaryo). Her kural için
koşulacak bir test değil — **şüphe duyulan** kurala saklanır.

**Tek koşum kanıt değil.** Model çıktısı turdan tura değişir; tek koşumda görülen fark
gerçek etki de olabilir varyans da. Bulgu *"kural işe yarıyor"* değil, **"bu koşumda
fark üretti"** diye yazılır. Kesinlik isteniyorsa aynı senaryo 3 kez ya da 3 farklı
senaryo — maliyet katlanır.

## Başkasının raporundaki mekanik iddia ölçüm değildir

Bir agent *"şu araçla kurdum"*, *"şu mekanizma çalışıyor"* dediğinde bu bir **beyan**.
Aktarmadan önce kendin ölç.

Sebebi: zincir uzadıkça iddia güçleniyor ama dayanağı zayıflıyor. Bir agent'ın raporuna
güvenip kendi doğru gözlemini geri almak ölçülmüş bir hata.

## Aynı dosyanın kaç kopyası var — hangi kaynağa baktığını doğrula

Bu ekosistemde aynı dosyanın onlarca kopyası var: plugin cache'inde sürümler, emekli
kuşaklar, proje repolarında kalıntılar. `grep` yolu değil **içeriği** getirir.

**Okuduğun şeyin yürürlükte olduğunu sen doğrularsın.** Hangi yolun yürürlükte olduğu
`projeler/agent-dagitim-yapisi.md`'de yazılı.

İki kural: **bir arama birden fazla sonuç döndürüyorsa hangisini kullandığını söyle.**
Ve **bir alanı aramak karşıtını aramamak demek değil** — bir kısıt arıyorsan hem izin
listesini hem yasak listesini ara.
