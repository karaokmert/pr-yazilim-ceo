# Proje Clara'ları — Mert nasıl yönetiyor

> **Durum:** AÇIK · izleme sürüyor
> **Başlangıç:** 2026-08-10
> **Ne bu:** Mert'in isteği — sahada çalışan proje Clara'larını izle, ama **onların
> davranışını değil, MERT'İN YÖNETİMİNİ** kaydet. Hangi mesajı veriyor, neyi
> düzelttirmeye çalışıyor, nasıl yönetiyor.
> **Amacı:** *"Bu projelerde çalışan Clara'ların nasıl olmasını istediğimin bir örneği
> olsun."* → yani bu kayıt bir **referans örnek**, bir arıza raporu değil.

**Takip aracı:** `takip.py` (bu klasörde) — çalışan `--agent clara` oturumlarını `ps`'ten
bulur, transcript'lerinden Mert'in mesajlarını çıkarır.
`python3 takip.py [--full] [--tools]`

**Canlı izleme:** `izle.py` — Monitor aracıyla sürekli koşar, yeni Mert mesajını
olay olarak basar. `python3 izle.py [--poll 25] [--with-clara]`

### Clara oturumu nasıl tanınır — ÜÇ YANLIŞ DENEME, sonra doğrusu

Bu ölçüm üç kez düzeltildi (2026-08-10). Üçü de yazılıyor çünkü **her biri makul
görünüyordu ve yanlıştı.**

**Deneme 1 — dosyada `"Adın Clara"` ara → HEPSİ KAÇTI.**
İlk teşhis *"sistem prompt ilk 120 KB'da değil"* idi. **Yanlıştı.** Doğrusu:
`"Adın Clara"` transcript'e **hiç yazılmıyor** — sistem prompt dosyaya girmiyor.
Beş oturumun beşi de kaçtı.

> **Ders:** *"aradığım yerde yok"* ile *"hiçbir yerde yok"* aynı şey değil.
> Birincisi arama hatası, ikincisi varsayım hatası — ve ben birinciyi teşhis edip
> ikinciyi kaçırdım.

**Deneme 2 — kanon izi ara (`CLA-FIX-THE-CAUSE` vb. ≥2 işaret) → YANLIŞ POZİTİF.**
Bir **güvenlik denetimi oturumu** (`9ae9f686`) Clara sanıldı — çünkü Clara'nın
yazdığı `izle.py`'yi inceliyordu ve dosyanın içinde kanon kimlikleri geçiyordu.

> **Ders:** kanon izi *kimliği* değil *temas ettiği içeriği* ölçüyor. Clara'dan
> BAHSEDEN her oturum Clara sanılır.

**Deneme 3 — sistem prompt satırını ayrıştır → yine hepsi kaçtı** (Deneme 1'in
sebebi hâlâ geçerliydi: ortada ayrıştırılacak sistem prompt yok).

**Doğrusu — İKİ ŞART BİRDEN:**
1. `slug` alanı var → **ana oturum** (alt-agent ve denetim oturumunda YOK)
2. ≥2 kanon izi → Clara kanonu bu oturumda dolaşıyor

Test: 5/5 doğru (üç Clara EVET · denetim HAYIR · kapanmış tmux oturumu EVET),
goat oturumlarında yanlış pozitif yok.

> **Ders (genel):** tek sinyalle kimlik tespiti yapılmıyor. `slug` tek başına
> "ana oturum" der (Clara'ya özgü değil), kanon izi tek başına "temas etti" der.
> **Ayırt eden şey kesişim.**

### İzleme disiplini — monitör TETİKLEYİCİDİR, ikinci kaynak değil

Monitör açıkken transcript'i ayrıca elle taramak **aynı olayı iki kez işletiyor.**
Ölçüldü (2026-08-10): üç olay art arda "zaten kayıtta" çıktı — çünkü elle okuma
monitörün imlecinin önündeydi.

**Doğru düzen:** monitör bağırır → bağlam o an açılır → okunur → kaydedilir.
Kendi başına transcript taraması yapılmaz; tarama yalnız **ilk kurulumda** (geçmişi
çıkarmak için) ya da monitör düştüğünde yapılır.

→ Bu bir betik arızası değil, **yönetenin disiplin arızası** — iki kaynağı birden
taşımak.

### Üçüncü tuzak — "çift basma" sanılan şey

Monitör bir mesajı bastığında zaten kayıtta görünüyorsa ilk düşünce *"imleç bozuk,
aynı olayı iki kez bağırıyor"* oluyor. **Ölçüldü (2026-08-10): arıza yok.**

Sebep: transcript **elle** okunduğunda monitörün imlecinden ileri gidiliyor.
Sonra monitör oraya ulaşınca olay "tekrar" sanılıyor — oysa monitör için ilktir.

→ **Ders:** iki kaynaktan (elle okuma + canlı izleyici) aynı veriyi alan bir düzende
"tekrar" bir arıza belirtisi değil, **hız farkının belirtisi.** Arıza sanmadan önce
izleyicinin ham çıktısına bakılır (`tasks/<id>.output`) — orada gerçekten iki satır
var mı diye.

### İkinci tuzak — "oturum canlı mı" ölçmek: ÜÇ YANLIŞ SİNYAL

İlk sürüm 14:32'de kapanmış bir tmux oturumunu *"yeni Clara"* diye bağırdı. Eşik
kondu — ve eşiğin **neye bakacağı** üç kez düzeltildi (2026-08-10). Üçü de makul
görünüyordu:

**(1) `mtime` → YALAN.** Dosyaya **mesaj yazılmadan** dokunuluyor. Sabah 10:12'de
kapanmış iki oturum *"2 dakika önce aktif"* göründü.

**(2) Son satırın timestamp'i → YALAN.** Kapanmış oturuma arka planda `attachment`
ve `last-prompt` **meta satırları** düşüyor. Aynı iki oturum bu kez *"3 dakika önce"*
göründü — oysa son gerçek mesaj 5 saat öncesiydi.

**(3) `message.role` kontrolü → YİNE YETMEDİ.** Son mesaj `"No response requested."`
— rolü `assistant`, ama **boş bir yanıt.** Kapanmış oturumu canlı gösterdi.

**Doğrusu — üçünün birleşimi:** `role ∈ (user, assistant)` **VE** gövde boş değil
**VE** gövde `"No response requested."` değil → o satırın timestamp'i alınır.
Test: 5/5 (iki aktif IZLE · iki kapanmış ELE · kendi oturumum IZLE).

> **Örüntü — bugün ikinci kez:** her seferinde **daha ucuz bir sinyale** güvenildi
> ve o sinyal başka bir şeyi ölçüyordu. Clara oturumunu tanırken de aynısı olmuştu
> (kelime varlığı → yoğunluk → davranış).
>
> **Ders:** bir şeyi ölçerken *"bu sinyal gerçekten aradığım şeyi mi ölçüyor, yoksa
> onunla birlikte görünen bir şeyi mi?"* — ucuz sinyal genelde ikincisidir.

---

## İzlenen oturumlar

> **Not (16:06):** CLARA-A'nın terminali yanlışlıkla kapandı. Yerine `fd73df88`
> açıldı — *"son oturuma geri dönelim kaldığın yerden devam edelim."* Yani aynı iş,
> yeni oturum. **Kanal devri gerekti:** Mert [16:21] — *"senin monitörün kapalı ve
> yanlışlıkla kapanan inbox'u devir alıp iletişimi sürdürmen lazım."*
>
> → **Ders:** oturum kapanınca **kutu yaşıyor ama izleyici ölüyor.** Yeni oturum
> kutuyu devralmalı; yoksa mesajlar kutuya düşer ve kimse okumaz — sessiz kopma.

**CLARA-A** — `ce4a7a08` · başlangıç 11:27 · **26 Mert mesajı**
Konu: OY PA ↔ OY BE arasında iş devri; sonra QA ve CA da eklendi.
Açılış: *"OY ile bu projedeki gereksinimleri hallettik artık iş devri gerekiyor.
OY PA ve OY BE arasındaki iletişimi sağlamayı test etmek istiyorum. Hazırlanır mısın?"*

**CLARA-B** — `6d1c1011` · başlangıç 11:02 · **9 Mert mesajı**
Konu: Fabrikada OY v8 işleri; demo analizi, symlink kurulumu, BE-V8 ↔ BE-FAB
karşılaştırmalı kanal testi.
Açılış: *"Fabrikada OY 8 işlerine devam ediyoruz. Yarım kaldı, demo yaptık.
Demoyu analiz edip düzeltmelerimizi ve kararlarımızı alacağız. Özet ile ne kurduk şimdi?"*

---

## BÖLÜM 1 — Mert neyi DÜZELTTİRİYOR

> Bunlar Clara'nın yaptığı hatalar ve Mert'in kesme cümleleri. Referans örneğin
> en değerli kısmı burası: **kesilen davranış = istenmeyen davranış.**

### D1 — "Bana ne geldiğini göstermeden soru sorma"

> [12:44] *"Clara sana gelen soruları ve bilgileri **önce ekrana benim
> görebileceğim şekilde ve istediğim brief düzeninde basmalısın.** Soruyu sonrasında
> sorabilirsin ancak **ne geldiğini bilmeden yanıt veremem.**"*

**Sıra emredilmiş:** önce ham gelen + brief düzeni → SONRA soru.
Tersi olduğunda Mert körlemesine karar vermek zorunda kalıyor.

**Bu Goat vakasının aynısı** (bkz. `fikirler/saha-agent-notlari/notlar.md` NOT 3):
orada da Clara PA'nın 6222 karakterlik brief'ini özetleyerek aktarmıştı, Mert
*"bana haberci güvenlik görevlisi yaptı"* demişti. **Aynı hata iki ayrı oturumda,
iki ayrı Clara'da.** Yani bu kişisel bir dalgınlık değil, **kanonda bir boşluk.**

### D2 — "Kodu doğrulamak senin işin değil"

> [13:00] *"Clara senin görevin kodu doğrulamak değil. **İşi doğrulamak sadece.**"*

Clara BE'nin teknik bulgusunu kendi kontrol etmeye kalkmış. Sınır net: teknik
bulgu agent'ın sorumluluğu; Clara **iş akışını** doğrular — geldi mi, anlaşıldı mı,
sıradaki adım doğru mu.

(Bu kayıtta zaten var: `feedback_isi_dogrula_kodu_degil.md` — ama sahada yine düşüldü.)

### D3 — "Direktif verdiysen kontrol et"

> [14:12] *"kurdular mı? **sen direktif verdiğinde neden monitörünü açıp kurulduğunu
> kontrol etmiyorsun ki?**"*

İş vermek yetmiyor; **verilen işin oturduğunu doğrulamak** yöneticinin işi.
Aynı oturumda öncesinde de aynı şey sorulmuş: [13:37] *"Kurulmadı mı hâlâ?"*

→ Örüntü: Clara direktifi yolluyor ve **sonucu beklemeden** bir sonraki işe geçiyor.

### D4 — "Onay aracını kullanma"

> [13:18] *"Clara onaylama işleminde her şey oturana kadar **ask tool kullanma
> bu sessionda yasaklıyorum sana.**"*

`AskUserQuestion` iş akışını kesiyor ve Mert'i gereksiz onay noktalarına takıyor.
**Not:** bu bir oturum-içi istisna (*"bu sessionda"*), kalıcı kural değil.

### D5 — "Kısa ver"

> [13:34] *"BE V8 - BE FAB diyelim kimse eski yeni değil. **handoffları kısa
> olarak ver bana.**"*

İki şey birden: isimlendirme düzeltmesi (*"eski/yeni"* değer yüklüyor, nötr ad kullan)
ve uzunluk.

---

## BÖLÜM 2 — Mert nasıl YÖNETİYOR

> Düzeltme değil, olumlu örnek: Mert'in yönetim hamleleri. Proje Clara'sının
> **taklit etmesi gereken** kısım bu.

### Y1 — İzlemeyi iki katmanlı istiyor

> [12:37] *"Sen OY ve BE'yi **ayrıca transcript üzerinden de takip et** ama görevi
> oraya göre yapma, **inbox'u takip et.** Amacım sadece agent'ların ne konuştuğunu
> kendi içinde ekrana ne yazdığını görmen ve **tıkanan yer olursa neden tıkandığını
> görmen.** Bu sayede kanalına bir şey yazmayan agent durduysa neden durduğunu
> görebilirsin."*

**Ayrım keskin:** kanal = **görev kaynağı** (iş buradan alınır), transcript =
**teşhis kaynağı** (tıkanma buradan görülür). İkisi karıştırılmaz — transcript'ten
iş alınmaz, ama sessizliğin sebebi oradan okunur.

Bu, `saha-monitorluk` skill'indeki "dört sessizlik türü"nün pratikteki karşılığı.

### Y2 — Tıkanmayı agent'a bildirtiyor, kendi tahmin etmiyor

> [12:38] *"**Önce bu takıldığı yeri sana iletmesi gerektiğini söyleyelim.**"*

Yani: agent tıkandığında sessiz kalmasın, **tıkandığını bildirsin.** Monitörün
tahmin etmesi değil, agent'ın raporlaması. Ucuz ve kesin.

### Y3 — Emsal araştırtıyor, kararı ona göre veriyor

Alias-swap tartışması bu yöntemin tam örneği. Sırayla:

> [12:46] *"alias altyapısı nedir **önce bir anlatır mısınız** bana?"*
> [12:47] *"Azure'da her index'in bir maliyeti var. Bir süreliğine de olsa bu index
> artırmak değil mi peki?"* ← **maliyet itirazı**
> [12:52] *"Bence alias swap'a gerek yok... Henüz tam anlamıyla prod'da değiliz...
> Ayrıca **BE'ye soralım alias swap'ı kim önermiş?**"*
> [12:53] *"peki BE'ye sorar mısın **bunu kullanan hiç gerçek örneğimiz var mı?**"*
> [12:53] *"mesela **balkanbee'de kullanılmış mı?**"*
> [12:55] *"BE'ye **core'u bir incelesin** bakalım bu yapı nasıl çalışıyormuş tam olarak?"*

**Yöntem:** anlat → maliyetini sor → **emsal ara** (kim önerdi, gerçek örnek var mı,
şu projede kullanılmış mı) → kaynağı okut → sonra karar ver.

Bu kanonda zaten yazılı (*"bir karar sorulduğunda önce emsal araştırtırsın"*) ama
**sahadaki uygulanışı burada.**

### Y4 — Görünürlük istiyor

> [12:26] *"**BE Task Listesini aktif kullanmalı** hangi işi ne aşamada ekranında
> görebilelim."*

Agent'ın ne yaptığı Mert'in ekranından görünmeli. Task listesi bir iç araç değil,
**görünürlük aracı.**

### Y5 — Paralel iş, ama sıralı kapı

> [13:19] *"QA ve CA'yı da açtım, onlara da handoff verelim. Onlar da kanallarını
> kursunlar. Spec QA onayına giderken **CA da 7 discovery'i inceleyip PA'ya rapor
> yollasın.**"*
> [13:27] *"QA spec'i inceleyip bununla yazılacak kodun kalitesini ölçerse
> **ön bir analiz yapmış oluruz.**"*
> [13:48] *"CA analize başlasın. **vs ondan sonra işe başlasın**"*
> [14:16] *"ok spec'in son durumunu QA'ya yollayalım. **Onaylarsa BE'ye onay
> verebiliriz.**"*

Dört agent aynı anda çalışıyor ama **kapı sıralı**: spec → QA onayı → BE'ye onay.
Paralellik hızda, sıra kalitede.

### Y6 — Anlamadığını sorar, geçmez

> [14:07] *"1. a ile gidelim. **ama bu BE'nin işini neden değiştirdi ki?**
> 2. BE bu kararla ne değiştiğini bize açıklasın.
> 3. **Nedir onlar? be2/b3 ne, anlamadım ki**"*

Kararı verirken bile anlamadığı terimi bırakmıyor. Clara'nın kullandığı kısaltma
(`be2/b3`) açıklanmamış — Mert onu geçmiyor.

→ **Ders:** Clara'nın ürettiği her kısaltma/etiket, Mert'in sözlüğünde yoksa
gürültüdür.

### Y7 — Kararı brief olarak geri istiyor

> [14:21] *"Şimdi onay vereceğimiz işi bana **brief düzenimize ve standardımıza göre**
> açıklar mısın?"*

Onay vermeden önce işin brief biçiminde önüne gelmesi. (`onay-brief` skill'i.)

---

## BÖLÜM 2B — Canlı izleme bulguları (monitör açıldıktan sonra)

> Monitör `b5odxhod6` 17:36'da açıldı. Buradan sonrası canlı yakalanan.

### İYİ ÖRNEK — CLARA-A 14:21→14:42, "brief" turu

Bu tur **referans örneğin olumlu tarafı**: sabah düzeltilen üç hatanın üçü de
burada yapılmamış. Kaydediliyor çünkü *"nasıl olmalı"* sorusunun cevabı bu.

**(1) Brief istendiğinde önce KAYNAĞA gitti, raporla yetinmedi.**
> Mert [14:21]: *"Şimdi onay vereceğimiz işi bana brief düzenimize ve standardımıza
> göre açıklar mısın?"*
> Clara: *"Bir şeyi doğrulayıp yazayım — **spec'i ben okumadım**, BE ve QA'nın
> raporlarından biliyorum. **Kapsamı kendi gözümle göreyim** ki brief dayanaklı olsun."*

→ Bu tam olarak Goat'ta **eksik olan** şey (BULGU 1: hakimiyet kurmadı, PA'nın
raporundan geri okudu). Burada aracı katman kaynağa gitti.

**(2) Okuyunca kimsenin söylemediği iki şey buldu.**
- spec §8 *"ONAY BEKLEYEN NOKTA"* diyordu — *"bunu kimse bana söylemedi"*
- kapsam listesinde `game` kuyruk tüketicisi vardı — CA raporunda *"4 consumer var,
  game yok"* geçmişti; yani **yeni bileşen**, ilk kez görülüyor

→ **Hakimiyetin karşılığı bu.** Rapordan okusaydı ikisi de kaçardı.

**(3) Direktif alınca adres eksikliğini fark etti, körlemesine iletmedi.**
> Mert [14:29]: *"BE'ye söyle önce skill'lerini tam okusun... olası tüm skill'leri
> okusun yapısal hata olmasın."*
> Clara: *"Ama bir şey ölçmem lazım önce: BE'ye 'tüm skill'lerini oku' derken
> **hangi skill'ler olduğunu bilmiyorum. Adres vermezsem arar ve bulamaz.**"*
> → 76 skill tarandı, **9'unda kırık atıf**, 4 agent etkileniyor.

→ Devir bloğu kuralının canlı uygulanışı: *"adres ver, içeriği kopyalama"*.
Direktifi ham iletmek yerine **iletilebilir hâle getirdi.**

**(4) Kendi bulgusunu yanlış çıkınca geri aldı.**
> Clara [14:33]: *"**Benim uyarım yanlış pozitifmiş.** `backend` omurgasında kırık
> atıf olduğunu söylemiştim. BE ölçmüş, durum farklı: atıflar var ama hedefleri
> başka bir skill'in referansı... Üstelik BE'nin kendi yüklü sürümü o atıfları
> taşımıyor."*

→ Ölçüm agent'tan geldi, aracı katman kendi bulgusunu düzeltti. **Doğru davranış:**
agent'ın teknik ölçümü Clara'nın tahminini ezer.

**(5) Karar noktasında durdu, kendi karar vermedi.**
İki kez: *"Bir karar bekliyor ve **bu senin**"* · *"BE gerçek bir tasarım
çatallanmasına geldi — ve **doğru davranıp durdu. Bu senin kararın.**"*

### Mert'in bu turdaki hamlesi — Y8

> [14:29] *"BE'ye söyle **önce skill'lerini tam okusun.** Erişilemeyen skill'leri var,
> yapılandırma yapıyoruz zaten ama **olası tüm skill'leri okusun yapısal hata
> olmasın.**"*

**Bir arızayı iş başlamadan önce kesme hamlesi.** O gün iki kez skill erişim arızası
çıkmıştı; Mert üretim başlamadan okumayı zorunlu kıldı. Karşılığını hemen verdi —
BE spec'te gerçek bir boşluk buldu ve Clara'nın yanlış pozitifini düzeltti.

→ **Ders:** bilinen bir mekanik arıza varsa, iş başlamadan önce kapatılır. Sonra
çıkan hatanın hangi sebepten geldiği ayrıştırılamaz.

### Y10 — Karar verirken brief'teki bir hatayı düzeltti

> **Clara'nın brief'i:** *"(b) seçilirse D2 ölçülemez"* (BE'nin cümlesini aynen
> taşımış)
> **Mert [14:47]:** *"1 b ile gitsin. **İşlem bittiğinde index'e kaç kayıt var
> sorgusu atarız**, ayrıca tek tek gitsin zaten istediğim buydu."*
> **Clara:** *"İkisi de net — ve birinci kararında **benim gözden kaçırdığım bir şey
> var: sayım sorgusunu zaten yazdırdık.** BE `GetSearchIndexDocumentCountAsync`'i
> ilk dilimde bitirdi. Yani D2 'ölçülemez' değil, **başka yerden ölçülüyor.**"*

**Ne oldu:** BE *"bu seçenekte ölçüm kaybolur"* dedi, Clara bunu **sorgulamadan
brief'e taşıdı**, Mert karar verirken ölçümün başka yerden alınabileceğini gördü.

→ **Ders (aracı katman için):** agent'ın *"şu mümkün değil"* iddiası da bir bulgudur
ve **doğrulanır.** Clara elindeki kaydı (ilk dilimde ne bitti) brief'e bakarken
kontrol etseydi çelişkiyi kendisi görürdü. Bu `feedback_isi_dogrula_kodu_degil`'in
sınırında: teknik ölçüm BE'nin, ama *"bu ölçüm zaten var mı"* **iş sorusudur.**

→ **Ders (Mert'in yöntemi):** karar verirken brief'i pasif okumuyor — kendi
bildiğiyle çapraz kontrol ediyor. Y3'teki emsal araştırtmanın kardeşi.

### Y11 — Testin bütünselliği için verimliliği feda etti

> [14:47] *"karar 2: **Hepsi bitince tek seferde olmasını istiyorum. çünkü testin
> bütünsel olması gerekiyor.** İndex silmem lazım, hepsini silip baştan
> oluşturulmasını test etmek istiyorum."*

Parça parça çalıştırmak daha hızlı ve daha az riskli; Mert **tek seferi** seçti
çünkü test edilecek şey parçanın çalışması değil **bütünün yeniden kurulması.**

→ **Ders:** karar verirken sorulacak soru *"hangisi verimli"* değil, **"ne test
edilecek."* Test hedefi mimariyi seçer.

### D8 — "Yönetiminden çok zorlanıyorum, çok hikâye ve karışık anlatıyorsun" ⚠️ EN SERT

> **Mert [15:20]:** *"**Ben senin yönetiminden çok zorlanıyorum Clara, çok hikâye ve
> karışık anlatıyorsun.**"*

Bu geri bildirim **yönetimin kendisine** — tek bir cevaba değil. Ve ölçülebilir.

**Ölçüm (CLARA-B, 15:16→15:20, üç mesaj):**

| Mesaj | Uzunluk | İçerik |
|---|---|---|
| 15:16:56 | **1803 karakter** | karşılaştırma + iki fark + not + sıradaki tur + **iki seçenekli soru** |
| 15:18:05 | **1825 karakter** | "çift artma" açıklaması + FAB'ın yaptığı + kanon bağlantısı + **yine iki seçenekli soru** |
| **15:20:20** (düzeltmeden sonra) | **434 karakter** | durum · tek fark · sıradaki hamle · *"Yollayayım mı?"* |

→ **Dört kat kısaldı ve iş görüyor.** Yani uzunluk bilgi taşımıyordu.

**Üç ayrı hata birikmiş:**

**(1) Bir mesajda dört iş birden.** 15:16'daki mesaj şunları taşıyor: ölçüm sonucu,
fark 1, fark 2, adres kayması notu, sıradaki tur planı, ve iki seçenekli bir soru.
Kanon *"bir bulgu, üç paragraf, bir soru"* diyor — altı iş var.

**(2) Anlatı kurgusu.** *"Farkı ölçüyorum — ve dürüst olmam gerekiyor: fark
beklediğim yerde çıkmadı"* — bu bir **hikâye açılışı**, bulgu değil. Bulgu şu:
*"soru ayırmadı."* Üç kelime.

**(3) Soru bitmiyor.** Her mesajın sonunda *"şunu mu yapayım yoksa bunu mu"* — iki
mesaj üst üste seçenek sunuldu. `feedback_secenek_sunma` zaten yasaklıyor: problemi
getir, kararı Mert versin.

→ **Düzeltilmiş hâlin kalıbı (15:20:20):**
> **Durum:** ne oldu — bir cümle
> **Tek gerçek fark:** bulgunun kendisi — bir cümle
> **Sıradaki hamle:** ne yapacağım — bir cümle
> *"Yollayayım mı?"*

**Bu kalıp kayda geçiyor** çünkü Mert onayladı (bir sonraki turda itiraz gelmedi)
ve dört kat kısa.

→ **`CLA-FIX-THE-CAUSE` notu:** buradaki sebep *"uzun yazma"* değil. Sebep **her
bulguyu aynı anda sunmak** — Clara ölçtüğü her şeyi tek mesaja koyuyor çünkü
hangisinin önemli olduğunu ayırmıyor. Kısalık bir sonuç; asıl düzeltme **seçim**:
bu turda Mert'in bilmesi gereken tek şey ne?

### D6 — "Anlamadım, daha mantıklı açıkla" (CLARA-A, 15:13)

> **Clara [15:11]:** *"BE gerçek bir mimari duvara çarptı... dizine yazmanın **üç
> katmanlı** olduğunu buldu: veritabanı satırı → ara model → dizin dokümanı (47 alan)
> → Azure'a yazım. Alt iki katmana erişebiliyor ama en üst katman... `api-search`
> o servislere erişemiyor — referansı yok."*
> **Mert [15:13]:** *"**Ben anlamadım şu an? sorunu daha mantıklı açıklar mısın?**"*
> **Clara:** *"Haklısın, **jargonla anlattım.** Baştan: **Amaç:** arama dizini
> bozulduğunda 'sıfırla ve baştan doldur' diyebileceğimiz bir düğme..."*

**Ne oldu:** Clara BE'nin teknik anlatımını **katman diliyle** aktardı (üç katman,
ara model, servis referansı). Mert'in ihtiyacı olan **amaç dili**: ne istiyoruz,
neden yapılamıyor.

→ Bu `feedback_mert_e_anlatim_bicimi` kaydının canlı ihlali: *"jargon yok, süreci
bilmeyen birine anlatır gibi."* Kural var, sahada tutmuyor.

→ **Ayırt edici:** ikinci anlatımda Clara **amaçtan başladı** (*"bozulunca sıfırla
düğmesi"*), sonra somut sayı verdi (*"bugün 27 promosyon dizinde yok"*), sonra engeli
anlattı. İlkinde katmandan başlamıştı.

**Kalıp:** amaç → bugünkü somut arıza → engel. Katman/mimari dili en sona, gerekirse.

### D7 — "Ölçme, SOR" (CLARA-A, 15:15) — en keskin düzeltme

> **Mert:** *"Benim anlamadığım şey şu: tek tek search'e eklemek var zaten,
> **o handler'ı kullanarak neden iş yapamıyoruz?**"*
> **Clara:** *"Doğru soru — ve ben cevabı bilmiyorum, BE'nin anlatımından çıkardım.
> **Ölçeyim.**"*
> **Mert [15:15:14]:** *[Request interrupted by user]*
> **Mert [15:15:17]:** *"**Ölçme sor**"*

**Ne oldu:** Clara sorunun cevabını kendi ölçmeye kalktı — kodu açıp bakacaktı.
Mert kesti: bu soru **BE'ye sorulur.**

→ **Bu, Goat vakasında EKSİK olan davranışın ta kendisi** (BULGU 2: *"aldığı soruları
netleşmesi için PA'yi hiç çalıştırmadı"*). Şimdi ters uçta hata: Clara PA'yı/BE'yi
çalıştırmak yerine **kendi ölçmeye** kalkıyor.

→ **Ayıran ölçüt — cevap kimde:**
> Cevap **kaynakta** (dosya, kayıt, sayı) → Clara ölçer.
> Cevap **agent'ın kafasında** (neden öyle yaptı, neyi denedi, neden olmuyor) →
> **agent'a sorulur.**

Clara'nın kendi cümlesi teşhisi veriyordu: *"ben cevabı bilmiyorum, **BE'nin
anlatımından çıkardım**"* — yani bilgi zaten BE'de. Ölçmek burada BE'nin yerine
geçmek olur, hem yavaş hem eksik.

→ **Ve `CLA-FIX-THE-CAUSE` açısından:** Clara'nın ölçme refleksi doğru bir kuraldan
geliyor (*"tahmin etme, ölç"*) ama **yanlış yere uygulanıyor.** Kural eksik: ölçüm
kaynağa gider, **muhataba değil.**

### ✅ TAŞIMA KAPANDI (21:54, izleyen Clara'nın bağımsız ölçümü)

Mert [18:47]: *"Commit onayım var, push yolla"* → ve sonuç doğrulandı:

**Commit:** `25e1bf3` — *"Fabrika ekibi skill-project'e taşındı: dört rol, beş skill,
hook, 65 memory"*

**Hedef durum ölçüldü** (`skill-project/.claude/`):
- `agents/` → **dört dosya**: PAM, PAD, PQA, PCA ✓ (19:31'de PAD eksikti)
- `skills/` → `behavior`, `dagitim`, `is-duzeni`, `uretim`, `yapi-taslari` ✓
  (19:31'de **hiçbiri yoktu**)

→ **PAD'in uyardığı "tehlikeli pencere" kapandı** — agent'lar ve kanonları artık
birlikte.

**İki buçuk saatlik taşımanın izi:** ölçüm önce (çakışma + kopmuş atıf bulundu) →
yarım durumda risk bildirildi → commit kararı bloke sanıldı, Mert kaldırdı →
tamamlandı → commit + push.

### 🔴 ÖLÇÜM (19:31, izleyen Clara) — taşıma yarımken (KAPANDI, üstteki nota bak)

Mert [16:30]: *"4 agent'ta taşındı mı?"* → **Hayır.** Bağımsız ölçüm:

**Hedef** (`skill-project/.claude/`):
- `agents/` → **üç dosya**: PAM, PQA, PCA. **PAD YOK.**
- `skills/` → **eski kuşak skill'ler** (`ag-qa`, `agent-generator`,
  `uretim-standardi`, `kanon-sagligi`...) — fabrikanın yeni skill'leri **gelmemiş**

**Kaynak** (`agent-project/.claude/`):
- `agents/` → **dört dosya** (PAD dahil, hâlâ orada)
- `skills/` → `behavior`, `dagitim`, `is-duzeni`, `uretim`, `yapi-taslari`
  — **beşi de hedefte YOK**

→ **PAD'in uyardığı tehlikeli pencere hâlâ açık ve genişledi:** üç agent hedefte
duruyor, kanonları gelmedi. Biri açılırsa `Skill` aracı hedefteki **eski kuşak**
skill'leri bulur — hata vermez, yanlış kanonla çalışır.

→ Ve `agents/` dizini 19:24'te değişmiş, yani iş sürüyor — bu bir *"durdu"* değil
*"yarıda"* durumu.

**Bu ölçüm bir yönetim dersi veriyor:** Mert *"taşındı mı?"* diye sormak zorunda
kaldı. Çok adımlı bir taşımada **her adımın sonunda durum kendiliğinden
raporlanmalı** — özellikle ara durum riskliyse.

### 🔴 BULGU — Yarım taşıma "tehlikeli pencere" açtı (PAD yakaladı)

Taşıma sırasında PAD üç agent dosyasını taşıdı ama **skill'leri henüz taşınmamıştı**
(PAM commit kararını bekliyordu). PAD'in uyarısı:

> *"Şu an hedefte üç agent dosyası var, **üçünün de skill'i yok.** Ve `behavior`
> **kullanıcı düzeyinde tanımlı** — yani biri şimdi açılırsa `Skill` aracı **başka
> bir ekibin v7 kanonunu getirir, hata çıkmaz.** Üç agent yanlış kanonla açılabilir
> durumda."*

→ **Sessiz arızanın tarifi:** eksik dosya hata vermiyor, **başka bir dosya** devreye
giriyor. Agent çalışır, kanonu yanlıştır, kimse fark etmez.

→ **Ders:** çok parçalı bir taşımada **ara durumun kendisi bir risk.** "Bire bir
kopya" güvenli görünüyor ama parçalar arası **sıra** güvenliği belirliyor: agent
kanonundan önce taşınırsa boşluk başka kanonla doluyor.

→ Bu PAD'in ikinci iyi ölçümü (birincisi: kopmuş atıflar). Ve **bire bir iddiasını
hash'le kanıtladı** — üç dosya bit düzeyinde aynı. *"Taşıdım"* demedi, gösterdi.

### İYİ ÖRNEK — "Beyanla yetinmiyorum, ölçüyorum" (16:12)

Mert *"eski agent'lar silindi mi?"* diye sordu. PAD *"arşive aldım"* demişti.

> **Clara:** *"Silinmedi, arşive alındı. **Ama beyanla yetinmiyorum, ölçüyorum**"*
> → Ölçüm: `trash/tasima-20260810/` altında, hash'ler PQA'nın baseline'ıyla
> **birebir aynı** (`ba6d40...`, `f27f84...`), dosya tarihleri orijinal.

→ `CLA-LABEL-YOUR-EVIDENCE` sahada tuttu — agent beyanı ile doğrulanmış ölçüm
ayrıldı, ve doğrulama **hash düzeyinde** yapıldı.

### 🔴 BULGU — Kendi çıkış koşulunu yazmış bir istisna, koşul gerçekleşmiş, kimse fark etmemiş

Clara aynı taramada iki ek symlink buldu (`ag-qa.md`, `agent-generator.md`) ve
`CLAUDE.md`'deki *"geçiş dönemi istisnası"*nı ölçtü:

> *"Gerekçesi **bayat** — o istisna 'VS Code terminal profilleri o agent adlarını
> çağırıyor' diyor, oysa **22 profilde `agent-generator` ve `ag-qa` sıfır geçiş.**
> Dört profil de `pr-agent-*` çağırıyor."*
> *"Yani `CLAUDE.md` **kendi çıkış koşulunu yazmış** ('geçiş kapanınca bu blok
> silinir') ve **koşul gerçekleşmiş, kimse fark etmemiş.**"*

→ **Ders (genel, kanona değer):** bir istisna yazılırken çıkış koşulu da yazılıyor —
ama **koşulu kimse yoklamıyor.** İstisna kalıcı hale geliyor ve zamanla *"kural"*
sanılıyor.

→ Ayıran soru: **bu istisnanın gerekçesi bugün hâlâ geçerli mi?** Ölçülmedikçe
istisna ölmüyor.

→ Clara doğru sınır çizdi: *"symlink'lerin kendisi ayrı bir karar, **dosya silmek
senin işin.**"* — ölçtü, önerdi, silmedi.

### 🔴 BULGU — "Kopya bayatlaması": aynı bilgi üç yerde, biri güncellenmemiş (PA)

Clara teşhis koymuştu: *"BE spec'i yazdı, iptal geldi, satırı güncellemedi."*
PA ölçtü ve **teşhisi keskinleştirdi:**

> BE iptali **iki yere doğru yazmış** (sat.164-166 *"geri alındı"*, sat.426 kriter
> gerekçesi doğru), yalnız **üçüncü kopya** bayat kalmış.
> → Sınıf *"haber almamış"* değil, **kopya bayatlaması.**
> PA'nın sonucu: *"**aynı bilgi üçüncü kez yazılmasaydı çelişki doğmazdı.**"*

→ **`CLA-FIX-THE-CAUSE`'un ders kitabı örneği:** çözüm *"güncellemeyi unutma"* kuralı
eklemek **değil**, aynı bilgiyi üç yere yazmayı bırakmak. Kural eklemek yama olurdu —
kopyalar dururdu ve dördüncüsü aynı arızayı üretirdi.

→ **Genel ders:** bir çelişki bulunduğunda sorulacak soru *"hangisi yanlış"* değil,
**"bu bilgi kaç yerde duruyor?"** Tek kaynaklı bilgi bayatlayamaz.

### ✅ D13'ün sonucu — PA devreye girdi ve KODDAN ölçerek cevapladı (22:23-22:39)

Mert 19:19'da *"muhatabı PA"* dedi. Clara üç kapsam sorusunu PA'ya taşıdı — ve
PA'nın cevapları düzeltmenin ne kazandırdığını gösteriyor:

> *"ÜÇ SORUYA DA CEVAP. **Önce ikisini de KODDAN ÖLÇTÜM.**"*
> *"SORU 1 — CRON: **kararını onaylıyorum (A), ama gerekçe farklı.** Cron'un else
> dalını açtım (sat.257-263). Senin cevabın DOĞRU, ama **gerekçem seninkinden
> güçlü**..."*
> *"ADMIN ARAMA UCU — KARAR: (2) EKLE. Ama farklı bir gerekçeyle, ve **önce ÖLÇTÜM.**
> İki ucu yan yana koydum: SİTE ucu · ADMIN ucu..."*

→ **Clara'nın cevabı doğruydu ama gerekçesi zayıftı.** PA aynı kararı verdi,
**farklı ve daha güçlü** gerekçeyle — kodu açıp ölçerek.

→ **Ders (D13'ü tamamlıyor):** *"muhatabı PA"* kuralının değeri sadece yetki değil,
**gerekçe kalitesi.** Clara gereksinim sorusunu doğru cevaplayabilir — ama dayanağı
tahminden gelir, PA'nınki koddan.

→ **Ve Clara doğru davrandı:** *"BE doğru yerde durdu, muhatabı sensin"* diyerek
taşıdı, kendi cevaplamadı. Düzeltme 3 saat içinde davranışa dönmüş.

### D13 — "BE sorularına kendi başına karar verme, muhatabı PA" (19:19) ⚠️

> **Mert [19:19]:** *"**BE sorularına kendi başına karar verme, PA ile konuş** —
> bu soruların muhatabı PA"*

**Bugün üçüncü kez aynı eksen düzeltiliyor** ve her seferinde farklı yönden:

| Saat | Düzeltme | Clara ne yapmıştı |
|---|---|---|
| 15:15 | *"Ölçme, **sor**"* (D7) | Cevabı kendi ölçmeye kalktı |
| 17:54 | *"Eksik olursa **PA'ya** sorabilirsin"* (Y35) | — (yetki açıldı) |
| 19:19 | *"Kendi başına **karar verme**, muhatabı PA"* (D13) | Kendi karar verdi |

→ **Eksen netleşiyor: BE'nin gereksinim sorusu Clara'nın kararı değil.**
Clara'nın işi taşımak; kararın sahibi **gereksinimin sahibi** olan PA.

→ **Ama bu Y33/D11 ile çelişir gibi görünüyor** (*"karar gereken yerde dur"* +
*"her görevi bloklama"*) — çelişmiyor, **karar tipi farklı:**
> **Ölçümden çıkan karar** → agent kendi verir (D11)
> **Gereksinim kararı** → PA verir (D13)
> **Geri dönülemez adım** → Mert (Y33)

Üç ayrı sınıf; Clara ikincisini birinci sanıp kendi cevapladı.

→ **`CLA-FIX-THE-CAUSE` notu:** Clara'nın kanonunda *"dayanağını gösterebiliyorsan
cevapla"* var (Y24'te doğru uygulandı). Ama o kural **ölçüm soruları** için;
gereksinim sorusunda dayanak göstermek yetmiyor — **yetki** gerekiyor. Kural eksik
yazılmış: *"dayanağını gösterebiliyor musun"* değil, **"bu kararın sahibi kim?"**

### ✅ Y39'un ilk sonucu — yeni kapı 26 dakikada bulgu üretti (22:23)

Mert 19:10'da kapıyı koydu; QA 22:23'te dört işi inceledi, **22:38'de raporladı:**

> *"ÖN İNCELEME TAMAM — dört iş. **2 BLOKE EDİCİ + 1 kritik bağımlılık bulgusu.**
> 🔴 **KAPI KARARI VERMİYORUM** (telepresence yok, davranış kanıtı yok)."*
> *"=== ORTAK BULGU — **ÜÇ İŞTE AYNI SESSİZ VERİ KAYBI** ==="*

→ **Kapı işe yaradı ve hemen:** commit'ten önce bakılmasaydı üç işte aynı sessiz
veri kaybı commit'lenmiş olacaktı.

→ **Ve QA doğru sınır çizdi:** *"kapı kararı vermiyorum — telepresence yok, davranış
kanıtı yok."* Statik inceleme yaptı, **çalıştığı görülmemiş** koda geçti damgası
vurmadı. Bu tam da Y11'in bıraktığı boşluğun bilinçli işaretlenmesi.

→ **Ders (yönetim):** bir kapı eklerken **neyi kanıtlayamayacağını** da tarif etmek
gerekiyor. QA statik bakar; davranış kanıtı ayrı kapıda (telepresence) ve o hâlâ
Mert'te.

### Y39 — Yeni kapı: "Commit'siz kodu QA doğrulasın, her biten işte" (19:10)

> **Mert [19:10]:** *"Clara **commit'siz kodu QA doğrulasın her biten işte**"*

Akışa bir kapı ekleniyor: BE bir işi bitirdiğinde, **commit'ten önce** QA bakacak.

→ **Neden şimdi:** bugün BE üç iş bitirdi, hepsi commit'siz bekliyor ve
telepresence doğrulaması **tek seferde sona** bırakılmıştı (Y11). Yani ortada
*"çalıştığı görülmemiş"* kod birikti. QA statik kapısı o boşluğu erken kapatıyor.

→ **Ders:** biriken doğrulama borcu **tek kapıda** kapatılmaz — araya bir kapı daha
konur. Mert erteleme kararını (Y11) geri almadı, **yanına ikinci bir kontrol** koydu.

→ Y5 ile birlikte okunur (*"paralel iş, sıralı kapı"*): Mert kapı sayısını işin
riskine göre ayarlıyor.

### Y38 — Gece devri: "Ben yatıyorum, işler sırasıyla sende" (18:56)

> **Mert [18:56]:** *"Ben yatıyorum, **işler sırasıyla sende.** Tüm OY agent'ları
> incelenmiş, her bir skill gözden geçirilmiş olmalı ve **yeni kurallarımız ile
> düzenli çalışabilir duruma gelmeli.**"*

**Devrin şekli — üç parça:**
1. **Yetki:** *"işler sırasıyla sende"* — sıralama dahil Clara'da
2. **Kapsam:** tüm OY agent'ları + her skill
3. **Kabul ölçütü:** *"yeni kurallarımızla **düzenli çalışabilir duruma gelmeli**"*

→ **Kabul ölçütü davranışsal, dosyasal değil.** *"İncelendi"* değil *"çalışabilir
duruma geldi."* Bu, fabrikanın bilinen zayıflığının tam karşıtı — kanonda
*"çalışıyor mu"* kapısı yok, Mert onu sözle koyuyor.

→ **Y21 ile karşılaştır:** orada da bir saatlik yokluk vardı ve *"inisiyatife gerek
yok"* denmişti; Clara sınırı söyleyince Mert yolu değiştirdi. Burada devir daha
geniş: **sıralama da Clara'da.**

→ **Gece devrinin riski (ölçülmedi, gözlem):** Mert yokken *"karar gereken yerde
dur"* (Y33) ile *"her görevi bloklama"* (D11) çarpışabilir. Geri dönülemez bir
adım çıkarsa iş sabaha kadar bekler — doğru davranış budur ama **atıl geçen saat**
de bir maliyet.

### 🌙 GECE (2026-08-10 23:00 → 08-11 04:48) — iki cephe ayrıştı

**Nabız 23:07'de yedi ucu birden ○ işaretledi**, sonra sabaha kadar iki farklı
şey oldu:

**Fabrika ÇALIŞMIŞ** — dördü de sabah aktif (PAM 5 dk, PCA 5, PQA 10, PAD 15).
Mesaj sayıları gece boyunca büyümüş:
> PAM 30→**47** · PQA 13→**20** · PCA 8→**16** · PAD 12→**18**

→ Mert'in gece devri (Y38: *"işler sırasıyla sende"*) **tuttu.** OY v8 incelemesi
gece boyunca sürmüş.

**Goat DURMUŞ** — üç uç da 5.5-6 saattir sessiz (BE 339 dk, PA 342, QA 352).
Mert 01:28'de *"sırasıyla task'lerin SQL'lerini bana getirir misin?"* demiş; zincir
muhtemelen orada kesilmiş.

→ **Ama süreçler ayakta:** goat BE, QA, CA hâlâ açık. Yani **kutu sessiz + süreç
canlı.** Nabız tek başına *"öldü"* derdi; `ps` *"ayakta"* diyor.

**⚠️ TEŞHİS DÜZELTİLDİ — Mert (04:49):**
> *"**5 saatlik session limiti dolmuş** bu nedenle sessizleşmişler, sorun yok.
> **Bunu tahmin ediyorduk.**"*

İzleyen Clara *"SQL turunu bekliyor"* demişti — **yanlıştı.** Gerçek sebep oturum
limiti. İki ipucu vardı ve ikisi de kaçırıldı:
- Sessizlik **eşzamanlı** başladı (BE 339 · PA 342 · QA 352 dk — 13 dakika içinde
  hepsi), oysa iş bekleyen uçlar **ayrı ayrı** susar
- Sessizliğin başlangıcı goat oturumlarının açılışından **~5 saat sonrasına** denk
  geliyor (BE 15:00 açıldı, ~20:00'de sustu)

→ **DÖRDÜNCÜ sessizlik türü — altyapı sınırı.** Önceki üçü: *sıra bekliyor* ·
*iş bitti bildirmedi* · *takıldı*. Bu dördüncüsü hiçbirine benzemiyor ve
**`ps` bile ayırt etmiyor** — süreç ayakta görünüyor ama oturum tükenmiş.

→ **Ayırt edici işaret: EŞZAMANLILIK.** Birden çok uç aynı pencerede susuyorsa
sebep işte değil **altyapıda.** Tek tek susma iş kaynaklı, toplu susma sistem
kaynaklı.

→ Nabza eklenecek: bir projedeki uçların **hepsi** birden ○ olduysa, bunu
*"toplu sessizlik — muhtemelen oturum limiti"* diye ayrı işaretle.

### Y41 — "Bana TEK bir make komutu vermeli, sonrası koşum onda" (01:51)

> **Mert [01:51]:** *"bana **tek bir make komutu** vermeli, ben çalıştıracağım,
> **sonrası koşum onda**"*

**İş bölümü net:** Mert'in yapacağı şey **tek komut**; onun ötesindeki koşum,
doğrulama, sonuç okuma agent'ta.

→ **Ders:** insan-in-the-loop adımı **atomik** olmalı. Beş komutluk bir liste
vermek onu operatör yapar; tek komut vermek **kapı bekçisi** yapar. İkisi farklı
rol — kapı bekçisi onaylar, operatör iş yapar.

→ Y27 ile birlikte okunur (*"silmeyi ben elle mi yapacağım?"*): orada fail
yazılmamıştı, burada **failin yükü** tarif ediliyor. İkisi aynı eksende — insana
düşen iş **görünür ve minimal** olmalı.

→ **Ve bu Mert'in genel tarzı:** telepresence'ta da aynısını istedi (*"toplu API
listesini versin, ben token hazırlayayım"* — Y25). Engeli kaldırmayı üstleniyor,
ama **hazırlığı agent'tan** bekliyor.

### Y40 — Dördüncü sorudan sonra MERT kendisi otomatikleştirdi (19:39) ⭐

Aynı soru dört kez sorulduktan sonra (15:30 · 16:30 · 18:54 · 19:32) Mert
CLARA-A'ya bir `/loop` kurdu:

> *"Goat kanalında üç agent'ı (BE / PA / QA) kontrol et: **her kutunun outbox son
> yazım yaşını ölç**, imlecini benim son mesajımla karşılaştır, **süreçlerin canlı
> olduğunu `ps` ile doğrula.** 5 dakikadan fazla sess[izlik]..."*

→ **Aynı boşluk iki yerden dolduruldu:** izleyen Clara `nabiz.py` kurdu (22:35),
Mert `/loop` kurdu (19:39 = 22:39). **İkisi de aynı sinyale bakıyor: outbox son
yazma yaşı.**

→ **Ve Mert'in tarifi daha eksiksiz** — üç kaynak birden:
> 1. **outbox yaşı** (kutu akıyor mu)
> 2. **imleç karşılaştırması** (agent Mert'in son mesajını okudu mu)
> 3. **`ps` doğrulaması** (süreç hâlâ ayakta mı)

Nabız yalnız birinciye bakıyor. **Üçü ayrı arıza sınıfı:** kutu sessiz ama süreç
canlı = çalışıyor · süreç ölü = oturum düşmüş · imleç geride = mesaj okunmamış.

→ **Ders (izleyen Clara için, kendi payıma):** *"tıkanma var mı"* sorusu dört kez
soruldu, ben dördüncüsünde araç kurdum — **Mert de aynı anda kurdu.** Bir ihtiyaç
dört kez tekrarlıyorsa araç üçüncüsünde kurulmalıydı.

→ Ve nabzımı **eksik kurmuşum**: `ps` ve imleç kontrolü yok. Mert'in tarifi daha
iyi ve o tarif kayda geçiyor.

### Y37 — "Tüm agent'lar işe devam ediyor değil mi? Tıkanan bir yer yok?" — ÜÇÜNCÜ KEZ

> **Mert [18:54]:** *"ok tüm agent'lar işe devam ediyor değil mi? tıkanan bir yer yok"*

Bugün **üçüncü** canlılık sorusu (D9 15:30 · *"4 agent taşındı mı"* 16:30 · bu).

**İzleyen Clara'nın ölçümü (21:57) — kanal nabzı:**
```
● goat BE          1 dk   (40 mesaj)     ● fabrika PAM   2 dk  (15 mesaj)
● fabrika PAD      4 dk   (8 mesaj)      ● fabrika PQA   8 dk  (8 mesaj)
○ goat PA         58 dk   (13 mesaj)     ○ fabrika PCA 104 dk  (4 mesaj)
○ goat CA        292 dk   ○ goat QA     277 dk
```
→ **Dört uç akıyor, iki uç dikkat çekiyor:** goat PA 58 dk (BE çalışırken sıra
bekliyor olabilir — anlamlı sessizlik), **fabrika PCA 104 dk** (16:46'da temizlik
işi verilmişti, bitti mi bilinmiyor).

→ **Ders (izleme düzeni — D9'da önerildi, hâlâ yok):** *"tıkanma var mı"* sorusu üç
kez soruldu ve her seferinde **elle ölçüm** gerekti. Kanal kutusunun son yazma
zamanı **tek satırlık nabız** olarak basılabilir; o zaman soru sorulmadan cevaplanır.

→ Ve **sessizliğin türü ayrılmalı:** *sıra bekliyor* (anlamlı) · *iş bitti,
bildirmedi* (eksik) · *takıldı* (arıza). Nabız üçünü ayırmıyor ama **hangisine
bakılacağını** gösteriyor.

### Y36 — "V8'i, agent-project'te öğrendiğimiz her şeyi yapacak şekilde yönetiyorsun değil mi?"

> **Mert [18:47]:** *"V8'i **agent-project'te öğrendiğimiz her şeyi yapılacak
> şekilde** yönetiyorsun değil mi?"*

Bir kontrol sorusu — ama asıl işlevi **bağ kurdurmak:** fabrikada bugün öğrenilenler
(ölçüm disiplini, birim yazma, teşhis kanıtı) v8 düzeltmesine **taşınıyor mu**, yoksa
v8 kendi başına mı ele alınıyor?

→ **Ders:** paralel iki hat varsa (fabrika üretimi · v8 düzeltmesi), birinde
öğrenilen diğerine **kendiliğinden geçmez.** Yöneten bunu sormak zorunda —
ya da aracı katman bağı kendisi kurmalı.

→ Bu, bugünün kapanış sorusu niteliğinde: **öğrenme aktarıldı mı?**

### 🔴 BULGU — Aynı kümede iki farklı sayı: 16 vs 11 (birim yazılmamış)

PAM *"16 skill ölçtüm, 15'i var, 1 eksik"* dedi. PAD aynı kümede **11** buldu.

> **PAD'in teşhisi:** *"PAM preload'ları da saymış olabilir (11+5=16)."*
> **Ve neden önemli olduğunu doğru gördü:** *"PAM bu ölçütü **sonraki sekiz rolde
> kullanacağım** diye kayda geçirdi. **Hangi kümeyi saydığı yazılı değilse** sonraki
> turlarda 'tamlık' farklı şeyler ölçer."*

→ Clara'nın notu: *"bugün **üç kez** düştüğümüz sınıf: **birim/kapsam yazılmamış
sayı.**"*

→ **Ders:** bir sayı bir ölçüte dönüşecekse **neyi saydığı** yazılmak zorunda.
Sonuç aynı çıksa bile (ikisinde de "eksik yok") ölçüt bozuk — sonraki turda farklı
şeyi ölçer ve kimse fark etmez.

→ Bu Clara'nın kendi kanonundaki kuralın aynısı: *"111 kural var"* eksik bir cümle;
*"111 kural var, şablon örneği olan biri elendi"* tam.

### D12 — "Sevk listesini kendine görev listesi yap ve TAKİP ET" (18:39) ⚠️

> **Mert [18:39]:** *"Sadece 3 task mı backend'di? **Backend'e verdiğimiz sprint
> listesini task listesi olarak kendine listele ve onu takip et.** BE'ye yaptır
> hepsini, **bekleyenler beni bekler.**"*

**Clara'nın cevabı teşhisi veriyor:**
> *"Haklısın — **3 değil, BE'ye verilen liste 7 işti ve ben onu takip
> etmiyordum.**"*

→ Clara az önce (18:31) *"3'ünün backend kodu bitti"* diye rapor vermişti. Ama sevk
edilen **7 işti** — dördünün durumu takip edilmiyordu, sadece son dokunulanlar
görünüyordu.

**İki ayrı hata birlikte:**

**(1) Sevk edilen iş listeye girmemiş.** İş verildi, takip kalemi açılmadı.
Görünürlük *"en son ne konuşuldu"* ile sınırlı kaldı.

**(2) Bekleyen iş "yok" sayıldı.** Mert'in cümlesi bu ayrımı kuruyor: *"bekleyenler
beni bekler"* — yani bekleyen bir iş **kaybolmuş** değil, **bende sıra bekliyor.**
Listede görünmeli.

→ **Hafızada zaten var** (`feedback_gorev_listesi_disiplini` — *"her mesajda/her iş
bitişinde güncelle; elimde ne var · kimden ne bekliyorum · kime ne vereceğim"*) ve
**sahada yine düşüldü.** Bugün ikinci kural ihlali (D11 ile birlikte).

**Clara doğru toparladı:** hafızadan değil **kayıttan doğruladı** (7 iş), dokuz
görev kalemi açtı, Mert'i bekleyen manuel işi **ayrı kalem** yaptı, ve
**bağımlılıkları kurdu** (üç askıdaki iş SQL turunu bekliyor, ikisi onun arkasında).

→ **Ders:** görev listesi *"ne yaptım"* değil **"ne bekliyor ve kimde"** sorusunun
cevabı. Bağımlılık kurulmazsa liste bir yığın olur; kurulunca **sıra** görünür.

**⚠️ Beş dakika sonra AYNI düzeltme ikinci Clara'ya da gitti [18:44]:**
> *"Bildir hadi, **tüm takımı iş listesine ekle.** Bitene kadar devam, **tüm
> agent'ları verimli kullan.**"*

→ **İki ayrı oturum, aynı eksik.** Yani bu kişisel bir dalgınlık değil — **kanonda
tutmayan bir kural.** `feedback_gorev_listesi_disiplini` yazılı ama sahada iki
Clara'da birden düşülüyor.

→ İkinci cümle ayrı bir talimat: *"tüm agent'ları verimli kullan."* Yani boşta
bekleyen agent varsa iş verilmeli — **paralel kapasite kullanılmıyor.** Bu D11'in
(*"bloklama"*) kardeşi: orada zincir duruyordu, burada **atıl kapasite** var.

### 🔴 BULGU — Tetik cümlesi vardı, YERİ yanlıştı (PAD, Clara'yı düzeltti)

Clara teşhis koymuştu: *"description'larda tetik cümlesi yok."* PAD ölçtü:

> *"Tetik cümlesi **zaten vardı**, ama **700 karakterlik içindekiler listesinin
> sonunda** kalıyordu — **'sorun tetiğin yokluğu değil yeri.'**"*

→ Bugün Clara'nın **beşinci** geri alışı ve hepsi aynı sınıftan: *"yok"* dediği şey
vardı, yanlış yerde ya da yanlış adla.

→ **Ders:** *"yok"* bir ölçüm iddiasıdır ve en kolay yanlış çıkanıdır. Bir şey
bulunamadığında ikinci soru: **"gerçekten yok mu, yoksa aradığım yerde mi yok?"**
(Bu bugün üçüncü kez tekrarlandı — `"Adın Clara"` aramasında da aynısı olmuştu.)

### İYİ ÖRNEK — PAM: "Dosyaya dokunmak ile dosyayı anmak aynı şey değil"

PAM kendi hatasını kabul etti ve **ayrımı doğru kurdu:**

> *"`proje-dosya-duzeni`'nin **içeriğini değiştirmek** dokuz rolü etkiler — Katman B,
> dokunulmuyor. Ama PA body'sine *'dosya düzeni işi → proje-dosya-duzeni'* satırını
> **eklemek** yalnız PA body'sini değiştirir, hedef dosyaya hiç dokunmaz."*

→ Ve **cascade tetiklenmediğini ölçtü** — iddiayla bırakmadı.

→ **Ders (genel):** bir dosyaya **atıf vermek** ile onu **değiştirmek** farklı etki
alanları. Karıştırılırsa ya gereksiz genişlik (her atıf cascade sanılır) ya da
gereksiz korku (atıf bile yapılamaz) doğar.

### İYİ ÖRNEK — "Bitti mi?" sorusuna tahminle değil ölçümle cevap (18:30)

> **Mert:** *"10 task de bitti mi?"*
> **Clara:** *"Hayır — 10'un tamamı bitmedi. **Ölçüp net rakam vereyim, tahmin
> etmeyeyim.**"*

Sonra ölçtü ve **soruyu yeniden çerçeveledi** — çünkü *"bitti mi"* iki katmanda
ayrışıyordu:

> *"Sprint akışında **BE bir aşama** — adım 3-4. Sonrasında QA (adım 5), sonra
> **FE aynı döngüyü baştan koşuyor** (adım 6), sonra topluca LIVE DEV (adım 7).
> Yani '10 task bitti mi' sorusunun cevabı iki katmanda ayrışıyor: **BE tarafı
> ilerledi, ama hiçbir iş tamamlanmadı** — çünkü hepsinin bir FE eşi var
> (*'iş = iki task: UI + development'*) ve FE hiç başlamadı."*

**Net cevap:** 10'un **3'ünün backend kodu** bitti, **hiçbiri tamamlanmadı**; biri
(`17535`) tam bitti ve telepresence doğrulandı; üçü SQL askıda; dördü hiç başlamadı
(biri salt frontend, biri NO-OP, ikisi sprint dışına alındı).

→ **Ders:** *"bitti mi"* sorusunda **bitmenin tanımı** netleşmeden sayı verilmez.
Aynı sayı iki farklı şeyi gösterebilir — *"kod yazıldı"* ile *"iş tamamlandı"*
arasındaki fark burada dört katmanlık.

→ Bu Kural 0'ın da iyi uygulanışı: tek bulgu (*"hiçbiri tamamlanmadı"*), dayanağı,
ve kalemlerin kısa dökümü.

### Y35 — "Eksik olursa PA'ya sorabilirsin" — kaynağı açtı

> **Mert [17:54]:** *"**Eksik olursa PA'ya sorabilirsin**"*

Kısa ama bir yol açıyor: Clara bir bilgi eksiğinde **PA'ya sorabilir** — Mert'e
dönmek zorunda değil.

→ Bu D7'nin (*"Ölçme, sor"*) tamamlayıcısı: cevap agent'ın kafasındaysa sorulur,
ve **kime** sorulacağı da açık artık. Mert aradan çıkıyor.

→ **Ders:** yönetenin işi yalnız cevap vermek değil, **cevabın kaynağını
göstermek.** *"Bana sor"* yerine *"ona sor"* demek zinciri hızlandırıyor.

### D11 — "Her görevi bloklama, iş devam etsin" (17:28)

> **Mert [17:28]:** *"**Her görevi bloklama, iş devam etsin**"*

**Bağlam:** Clara SQL onayını aldı, migration'ı Mert'e bıraktı, ve devamı için de
onay bekliyordu. Her adım Mert'e dayanmış.

**Clara'nın ayrımı doğru:**
> *"Haklısın — her adımı onaya bağlarsam **iş sürekli duruyor ve bekleyen taraf ben
> oluyorum**... Ama bir tuzağa düşmemem lazım: kanonda ben *'kararı Mert verir'* diye
> durmuşum. Şimdi ayrımı netleştiriyorum — **ölçümden çıkan kararı BE kendi verir ve
> yazar; sadece geri dönülemez olanda durur.**"*

→ **Ölçüt netleşti:** durulacak yer **geri dönülemez** olan (SQL migration, prod
dokunuşu, silme). Ölçümden çıkan karar agent'ın.

→ Bu Y33 ile birlikte okunur: Mert *"karar gereken her yerde durabilirsiniz"* demişti
— **ama "her adımda onay bekle" demek değildi.** İkisinin farkı: durmak agent'ın
kendi kararı için, onay beklemek Mert'e yük bindirmek.

→ **Hafızada zaten var** (`feedback_akisi_bloklamayin`) ve **sahada yine düşüldü.**
İkinci kez kayda geçiyor.

**Ve beş dakika sonra somutlaştırdı [17:33]:**
> *"**Diğer işlere devam etsin, ben SQL'i halledince devam eder.**"*

→ Yani bekleyen bir iş **tüm zinciri durdurmuyor** — o dal bekler, diğerleri akar.
Clara migration'ı beklerken bütün BE'yi durdurmuştu.

→ **Ayıran soru:** bu bekleme **hangi işi** bloke ediyor — o dalı mı, hepsini mi?
Sıralı bağımlılık yoksa paralel devam eder.

**Kayda değer — Clara iyi bir şey yaptı:** BE'ye kararı iletirken *"neden (c)
olmadığını"* da yazdı, gerekçesiyle:
> *"bir agent kararı anlamadan uygularsa bir dahaki sefere **aynı yeri yeniden
> tartışıyor.**"*
→ Karar + gerekçe birlikte gider; yoksa aynı tartışma tekrar açılır.

### 🔴 BULGU — v8'de "teşhisini kanıtla" diyen HİÇBİR kural yok (PAD)

PAD'in en değerli bulgusu — ve Clara'nın sabahki ölçümünü açıklıyor:

> *"**v8'de 'teşhisini kanıtla' diyen hiçbir kural yok.** BE'nin kanıt refleksi
> **kod yazma** tarafında (`BE-TELEPRESENCE-PROOF` — *'commit öncesi curl ile
> çalıştığını kanıtla'*), **teşhis** tarafında sıfır. Aradığı desen 164 dosyada
> bulunamadı."*

→ **Yani Liston'daki yanlış hükmün sebebi bir kural ihlali değil, kanonda o kuralın
hiç olmaması.** Bu `CLA-FIX-THE-CAUSE`'un tam da aradığı ayrım: agent kuralı
çiğnemedi, kural yoktu.

**Ve PAD'in yöntemi örnek:**
- 580 kimlik, 561 tam tanım tarandı → mutlak kuralların **%89'u gerekçeli**, **%91'i
  örnekli**, çift kaynak **sıfır**
- Clara'nın verdiği örneği **çürüttü** (`MOD-` prefiksi 0.6.1'de hiç yok)
- **Üç şeyi ölçemediğini yazdı, uydurmadı**

### İYİ ÖRNEK — Clara fabrikaya üç ölçüm kuralı verdi

İşi dağıtırken dördüne de aynı kuralları koydu:
1. **önce ölç sonra yaz**
2. **grep çıktısı kanıt değil** — *"bugün üç kez düşüldü"*
3. **kendi paketinizle kıyaslamayın** — *"dokuz rollü yayındaki bir paketle tek
   rollü pilotu kıyaslamak adaletsiz olur"*

→ Üçüncüsü Y17'nin (koşul eşitliği) fabrikaya aktarılmış hâli. Sabah Mert'in
öğrettiği ölçüm dersi aynı gün kurala dönmüş.

### ⚠️ Clara iki kez daha çürütüldü (fabrika tarafından)

> *"PAM **verdiğim iki tabanı da çürüttü** ve **ikisi de benim hatamdı**"*

→ Bugün Clara'nın **dördüncü** geri alışı (FAB bir kez, PAD bir kez, PAM iki kez).
Örüntü: Clara ölçüm yapmadan örnek veriyor, agent ölçüp çürütüyor.

→ **Ders:** iş dağıtırken verilen *"örnek bulgu"* da bir iddiadır ve ölçülmüş
olmalı. Ölçülmemiş örnek, agent'ı yanlış yöne sürer — ya da (iyi durumda) agent
zamanını onu çürütmeye harcar.

### Y34 — Çıktı biçimini önceden söyledi: "başlık ve açıklama olarak"

> **Mert [17:03]:** *"Fabrika agent'ları OY 8'deki sorunları analiz etsinler ve sana
> raporlasınlar. **1. Liste — Başlık ve Açıklama olarak senden problem listesi
> bekliyorum.**"*

İşi verirken **çıktının şeklini** de verdi. Bu bugün ikinci kez (D8'den sonra):
Mert artık formatı baştan söylüyor.

→ **Ders:** çıktı biçimi işin parçası. Sonradan *"böyle değil"* demek yerine baştan
tarif etmek bir tur kazandırıyor.

**Clara'nın iki iyi hamlesi:**

**(1) Elindekini tekrar ürettirmedi.** *"Elimde zaten iki kaynak var... Fabrikaya
'sıfırdan analiz et' dersem **elimdekini tekrar üretirler.** Onun yerine bu ikisini
**girdi** olarak verip üstüne yeni bulgu isteyeceğim."*
→ Bilinen bulguyu girdi yapmak, hem tekrarı önlüyor hem eşiği yükseltiyor.

**(2) İşi ölçüp böldü.** *"Envanter: **9 rol, 76 skill, 77 reference, 1.055.263
karakter.** Bu tek bir agent'ın tarayabileceğinden büyük — o yüzden işi dörde
böleceğim, her rol kendi eksenini alsın."*
→ Dağıtım eksene göre: PAM yapı/kapsam · PAD kural kalitesi · (diğer ikisi ayrı).

→ **Ders:** bir işi devretmeden önce **hacmini ölç.** Tek agent'a sığmayan iş
bölünmeden verilirse ya yarım kalır ya yüzeysel döner — ve ikisi de "yapıldı"
görünür. Bu tam da fabrikanın bilinen eksiği (`incelemeler/oy-v8-yeniden-uretim/`:
*"hacme dayalı parçalama ölçütü yok"*).

### Y33 — Kural verdi: "etki analizi task'a göre, her işte değil"

> **Mert [17:02]:** *"Bu task'a göre değişir. **Her task için tabii ki gerek yok ama
> belirsizlik ve risk varsa yapılır.** BE'ye devam ettirebilirsin... **Karar gereken
> her yerde durabilirsiniz.**"*

İki ayrı şey söylendi:
1. **Etki analizi koşullu** — sabit bir adım değil, ölçüte bağlı (belirsizlik/risk)
2. **Durma izni açık** — *"karar gereken her yerde durabilirsiniz"*

→ **İkincisi bir yönetim tercihi:** Mert durmayı **maliyet değil güvence** sayıyor.
Agent'ın karar noktasında durması onaylanıyor, hız için geçilmesi değil.

**Clara'nın doğru refleksleri (üçü birden):**

**(1) Varsayıp cevaplamadı.** *"BE 'başlamadan bir şey soracağım' dedi ve o soru
henüz gelmedi. **Sormadığı bir soruyu varsayıp cevaplamayayım** — kutuya bakıyorum."*
→ `CLA-WAIT-FOR-THE-END`'in canlı uygulanışı.

**(2) Sessizliğin sebebini ölçtü, teşhis uydurmadı.** *"BE 19:49'dan beri sessiz,
13 dakika. **Muhtemelen benim cevabımı bekliyor** — son mesajım commit onayıydı,
'sıradaki işe geç' demedim."* → Sessizliği agent'ın arızası saymadı, **kendi
eksiğini** aradı.

**(3) Kuralı kalıcı yere yazdı.** *"Kuralı kalıcı yere yazıyorum — bu bir tercih
beyanı, **iki ay sonra bilinmezse yanlış refleks kurarım.**"*
→ `CLA-WRITE-BEFORE-CLOSE`'un tam ölçütü: *bu turda öğrenilen şey iki ay sonra
bilinmediğinde zarar verir mi?*

### Y32 — Temizlik işini taşıma bitince başlattı, PCA'ya verdi

> **Mert [16:46]:** *"evet kanalları birazdan kapatacağım ama — **Fabrika agent'ında
> PCA skill-project'teki dokümanları tarasın, çöp/eski/gereksiz olanları arşive
> taşısın.**"*

**Sıra korundu:** taşıma → sonra temizlik. Bu Clara'nın devir bloğunda yazdığı
ayrımın aynısı: *"Düzenleme ve temizlik SONRAKİ iş — taşıma ile karışırsa neyin
taşındığı, neyin silindiği ayrılmaz."*

→ **Ders:** iki iş aynı dosyalara dokunuyorsa **aynı turda yapılmaz.** Karışırsa
sonuç doğru bile olsa **iz bozulur** — hangi değişikliğin hangi işten geldiği
ayrılamaz.

**Ve rol seçimi doğru:** tarama/envanter PCA'nın işi (analist), taşıma PAM'in
(koordinatör). Mert işi doğru role verdi.

→ **Silme değil arşive taşıma:** *"çöp/eski/gereksiz olanları **arşive taşısın**"*
— geri alınabilir bırakıldı. Y30'daki refleksin aynısı (*"eski agent'lar silindi
mi?"* → arşive alınmıştı).

### Y31 — "Commit her şey bitince olur, en son bakarız" — üçüncü kez aynı kalıp

> **Mert [16:31]:** *"commit her şey bitince olur, en son bakarız öyle"*

Clara commit kararını **taşımanın önkoşulu** olarak sunmuştu (*"taşıma buna bloke"*).
Mert bloğu kaldırdı: commit **sonda**, taşıma şimdi.

→ **Y11 · Y29 ile aynı kalıp, üçüncü kez:**
> Y11: parça parça test → **tek seferde** (*"testin bütünsel olması gerekiyor"*)
> Y29: iki indeks sil → **hepsini sil** (*"burası dev, risk yok"*)
> Y31: önce commit sonra taşı → **önce taşı, commit sonda**

**Ortak ilke:** Mert **ara adımları birleştirip sona atıyor.** Gerekçe hep aynı
ailede — bütünlük (tek seferde görülsün) ve akış (iş bölünmesin).

→ **Ders (aracı katman için):** bir adımı *"önkoşul"* diye sunmadan önce sor —
**gerçekten bloke mi, yoksa sadece sıralı mı?** Commit taşımayı teknik olarak
engellemiyordu; Clara onu kilit olarak sunduğu için iş bekledi.

Ayıran test: **bu adım yapılmazsa sonraki adım YANLIŞ mı olur, yoksa sadece
DÜZENSİZ mi?** Yanlışsa önkoşul, düzensizse sıralama tercihi — ve sıralamayı
Mert seçer.

### Y30 — "Eski agent'lar silindi mi?" — geri alınamaz adımı sordu

> **Mert [16:12]:** *"**Eski agent'lar silindi mi?**"*

Clara taşıma öncesi çakışmayı ölçmüştü: hedefte **eski kuşak PAM ve PQA** vardı
(1 Ağustos, tarihçe). PAD *"eski ikisini arşive aldı"* dedi.

→ Mert **geri alınamaz adımı** doğruluyor. Taşıma raporu *"üç dosya taşındı"* diyor;
Mert'in sorduğu şey **ne kaybedildi.**

→ **Ders:** bir işlem raporu *"ne yapıldı"* anlatır; yönetenin sorduğu *"ne geri
alınamaz oldu."* Aracı katman ikincisini sorulmadan söylemeli.

### Y29 — "Hepsini silelim, burası dev" — kapsamı GENİŞLETTİ (Y11'in tekrarı)

Clara ölçtü ve **daha az iş öneriyordu:**
> *"**Hepsini silmek gerekmiyor.** Sponsor (19) ve promosyon (41) yeterli...
> Oyun, sağlayıcı ve tekrar (6, 7, 9) silinmese de olur; kod yolu aynı, sadece
> farklı sorgu. **Beşini birden silmenin ek bir kanıt değeri yok.**"*

> **Mert [16:01]:** *"bence **hepsini silelim** ve sorunsuz doldurulduğuna emin
> olalım. **burası zaten dev indexi, prod değil.**"*

→ **İki gerekçe, ikisi de kararı taşıyor:** (1) beş yolun beşi birden sınanır,
(2) risk yok çünkü dev.

→ **Y11 ile aynı kalıp:** orada da Clara verimli olanı önerdi (parça parça),
Mert bütünselliği seçti (tek seferde). **Test hedefi kapsamı seçer, verimlilik
değil.**

→ **Ders (aracı katman için):** *"ek kanıt değeri yok"* bir **ölçüm** iddiasıdır ve
Clara'nın kanıtı zayıftı — *"kod yolu aynı"* bir varsayım. Beş ayrı sorgu, beş ayrı
veri şekli; birinde patlayabilir. Ve maliyeti sıfıra yakınken (dev ortamı) *"gerekmez"*
demek **tasarruf değil kapsam daraltması.**

**Ayrıca bu turda Clara iyi bir ölçüm yaptı — ekran görüntüsünden:**
> *"50'den fazla kayıtlı indeks **yok.** Promosyon 41, sponsor 19, tekrar 9,
> sağlayıcı 7, oyun 6... **PA'nın kabul kriteri bugün kanıtlanamaz.** Sayfalama
> doğruluğu bu turda ölçülemez."*
> *"BE 'oyun/tekrar binlerce olabilir' demişti — **tahminmiş**, gerçek 6 ve 9."*

→ Bir kabul kriterinin **karşılanamaz** olduğunu önceden görmek değerli; iş bitince
*"karşılandı"* diye yazılması engellendi.

### Y28 — "Sadece api-search yeterli olacak mı?" — iddiayı sınadı, eksik çıktı ⭐

> **Mert [15:59]:** *"telepresence'de **sadece api-search yeterli olacak mı?**"*

Clara envanterde BE'nin cümlesini aktarmıştı: *"Tek servis yetiyor: `api-search`."*
Mert bunu sınadı — ve **eksik çıktı:**

> **Clara:** *"BE 'yeterli' diyor ve gerekçesi mantıklı... **Ama bu onun ölçümü**
> ve bir noktada eksik kalabilir: doldurma `SearchDataLayer` üzerinden gidiyor ve
> o katman `api-search`'ün içinde değil, **ortak kütüphanede**... Asıl soru şu —
> doldurma **veritabanına** bağlanacak, o bağlantı bilgisi de intercept ile geliyor mu?
> BE ortam notunda sadece **arama servisi adresini** doğrulamış, **veritabanı
> bağlantısını değil.** Yani 'tek servis yeter' iddiası doğru olabilir ama
> **veritabanı erişimi ölçülmemiş.**"*
> *"Doğru — ve **bu benim listemde eksikti.**"*

→ **Bu Kural 12'nin ("agent'ın 'mümkün değil' cümlesi doğrulanır") kardeşi ve
tersi:** agent'ın *"yeterli"* cümlesi de doğrulanır. Olumsuz iddia gibi olumlu
iddia da bir bulgudur.

→ **Ve Mert'in yöntemi netleşiyor — üç kez aynı hamle bugün:**
1. *"Biri hook ile yükledi, diğerinde hook var mıydı?"* (Y17) → zemin eşit değildi
2. *"(b) seçilirse ölçülemez mi?"* (Y10) → ölçüm başka yerden alınabiliyordu
3. *"Sadece api-search yeterli mi?"* (Y28) → veritabanı erişimi ölçülmemişti

**Ortak kalıp:** Mert brief'i pasif okumuyor, **iddianın kapsamını** sorguluyor.
*"Bu doğru mu"* değil, **"bu neyi kapsamıyor"**.

→ **Ders (aracı katman için):** agent'ın bir iddiasını aktarırken **neyi ölçtüğünü
ve neyi ölçmediğini** ayır. Clara *"tek servis yeter"* dedi, BE'nin yalnız arama
adresini doğruladığını yazmadı. `feedback_kapsamini_yaz`'ın ihlali —
ama **düzeltmeyi kabul etti ve kendi eksiğini işaretledi.**

### Y27 — "Silmeyi ben elle mi yapacağım?" — talimatın kime düştüğünü sordu

> **Mert [15:57]:** *"[oturum id] **silmeyi ben elle mi yapacağım?**"*

**Bağlam:** Clara telepresence envanterini sundu — hangi servis, hangi token, hangi
header, hangi uçlar, ve *"silme sırası: küçükten büyüğe, önce sponsor..."* Ama
**silmeyi kimin yapacağı** yazılı değildi.

→ **Ders:** bir iş planı sunulurken her adımın **faili** belli olmalı. *"Silinir →
kurulur → doldurulur"* edilgen; Mert *"kim siliyor"* diye sormak zorunda kaldı.

→ Bu D1'in kardeşi: Clara bilgiyi taşıyor ama **eylemin sahibini** taşımıyor.
Envanterde araç var, sıra var, uyarı var — fail yok.

**Ayrıca kayda değer — BE'nin uyarısı iyi bir örnek:**
> *"her istekte `x-dev-user` header'ı olmalı. Yoksa istek cluster'a gider, **lokal
> kod hiç çalışmaz** ve cevap doğru görünür — sahte yeşil."*

→ Sessiz arızanın tam tarifi: test *"geçti"* der ama hiçbir şey test edilmemiştir.
Ve BE bir de doğrulama adımı koymuş: doldurmadan önce env dosyasındaki adrese bak,
**prod adresi çıkarsa dur.**

### Y26 — Toplu karar seti: altı maddeye tek mesajda cevap

> **Mert [15:56]:** *"1. Olur, arşive al ve CLAUDE.md'yi düzeltelim güncele göre.
> 2. o kalsın, ekstra bir şey taşınmasına gerek yok. 3. tamam. 4. evet team
> taşınabilir ama marketplace kalsın. 5. bunu taşımayalım. 6. T..."*

Clara altı numaralı bir soru seti hazırlamış, Mert **tek mesajda hepsini** cevapladı.

→ **Ders (aracı katman için):** kararlar **numaralı ve tek mesajda** sunulursa
Mert tek seferde geçiyor. Bu Kural 0'ın ("tek bulgu") istisnası değil tamamlayıcısı:
**bulgular tek tek, kararlar toplu.** Karar seti bölünürse Mert altı kez döner.

→ Y9 ile birlikte okunur: *"kararlar birikince toplu brief"* — burada Clara doğru
yaptı, birikeni topladı.

### 🔴 BULGU — PAD: "taşıma tek başına işlemez" (dört bulgu)

PAD kendi taşınmasını ölçtü ve **taşımanın sessizce bozulacağını** buldu:

> *"Hedefte **beş skill'inin hiçbiri yok** — ve kendi gövdesinde onlara metin içinde
> atıf var. Taşınırsa o satırlar **boş adres** gösterir."*

→ Yani "bire bir kopya" talimatı, **bağımlılıkları taşımadığı için** çalışan bir
agent'ı kırık bir agent'a çevirecekti.

→ **Ders:** bir bileşen taşınırken taşınan şey dosya değil **bağ.** Dosya kopyalanır,
atıflar kopyalanmaz — ve kırıldığı ancak kullanılınca anlaşılır.

**Ve bu, Clara'nın taşıma öncesi ölçümünün (agents/ çakışması) ikinci katmanı:**
Clara **üstüne yazma** riskini buldu, PAD **kopmuş atıf** riskini buldu. İkisi ayrı
ve ikisi de sessiz.

### Y25 — Engeli kaldırmayı üstlendi: "toplu API listesini versin, ben token hazırlayayım"

> **Mert [15:52]:** *"task task demiştim, task'ın bir bölümü için telepresence
> istemişti BE, ondan izin vermedim. Şimdi gerekli toplu API listesini versin,
> ben de ona token hazırlayayım."*

**Bağlam:** Clara *"telepresence yapılmadı, ortada çalıştığı görülmemiş bir kod var"*
dedi. Sebep Mert'in kendi kararıydı (*"hepsi bitince tek seferde test"*).

**Mert iki şeyi birden yaptı:**
1. Kendi kararının **bedelini kabul etti** — doğrulama borcu birikti
2. Engeli **kendi üstlendi** — token hazırlamayı üstüne aldı, BE'den liste istedi

→ **Ders:** yönetenin işi yalnız karar vermek değil, **kararın ürettiği engeli
kaldırmak.** *"Tek seferde test edelim"* kararı doğrulamayı erteledi; erteleme
kalıcı olmasın diye Mert kendi hamlesini yaptı.

→ Clara'nın bunu **hatırlatması** gerekirdi — telepresence'ın neden yapılmadığını
söyledi ama *"o zaman ne zaman yapılacak"* sorusunu açmadı.

### 🔴 BULGU — Kanon "commit'e girmesin" diyor, mekanizma elemiyor

BE'nin bulduğu (Clara aktardı):

> *"Kanon 'şu dosyalar commit'e girmesin' diyor ama `.gitignore` onları elemiyor.
> SQL migration için mekanizma var — yanlış yazarsan sessizce girer, doğru yazarsan
> otomatik elenir. Ama spec, doğrulama ve karar dosyaları için **sadece dikkat** var."*
> *"Bugün iki kez şans yaver gitti: PA geniş `add` yapmadı, BE yapmayacak. **İkisi de
> disiplinle yakalandı, mekanizmayla değil.**"*

→ Bu `CLA-FIX-THE-CAUSE`'un ders kitabı örneği: kural var, **kuralı uygulayan
mekanizma yok.** Ve iki kez tesadüfen kurtarıldı.

→ Mert kararı hemen verdi: *"PA .gitignore'u düzenlesin."* — dikkat yerine mekanizma.

**Ayrıca BE doğru sınır çizdi:** `.gitignore`'a dokunmadı — *"proje yapılandırması
benim alanım değil"* — öneri bıraktı, kararı yukarı taşıdı.

### İYİ ÖRNEK — Clara öz-beyanı ölçüm saymadı

> *"BE kendi öz-denetimini yaptı, listeyi plugin yolundan açıp fiilen geçti...
> **Ama bu bir öz-beyan.**"*

→ `CLA-LABEL-YOUR-EVIDENCE` uygulanmış: agent'ın *"kontrol ettim"* demesi ile
bağımsız doğrulama aynı ağırlıkta değil. Clara farkı işaretledi.

### Y24 — "BE telepresence ve kural kontrolü yaptı mı? Her şey kurallara uygun mu?"

> **Mert [15:48]:** *"be telepresence ve kural kontrolü yaptı mı? her şey kurallara
> uygun mu?"*

Clara *"commit onayı bekliyor"* diye brief verdi. Mert onay vermeden önce **kapının
geçilip geçilmediğini** sordu — derleme temiz olması yetmiyor, iki ayrı doğrulama var:
telepresence (lokalde gerçekten çalışıyor mu) ve kanon uyum kontrolü.

→ **Ders:** *"kod bitti"* ile *"kod onaya hazır"* aynı şey değil. Aracı katman
brief'i sunarken **hangi kapıların geçildiğini** de getirmeli — sorulmadan.

→ Bu Y5'in kardeşi (paralel iş, sıralı kapı): Mert kapıyı hep hatırlıyor, Clara
hatırlatmıyor.

### İYİ ÖRNEK — Clara kararı kendisi verdi, Mert'e getirmedi (CLARA-A, 15:45)

PA bir soru sordu (borç kaydı ayrı dosyaya mı, mevcut dosyaya mı). Clara:

> *"Bu bir **ölçüm sorusu, tercih değil**: dosya zaten 'GÜVENLİK & TEKNİK BORÇ'
> başlıklı, projede başka borç dosyası yok, ve PA ayrımı ayrı bölüm + açık uyarıyla
> zaten kurmuş. Tek kalemlik yeni dosya açmak, bugün olmayan bir düzen ihtiyacına
> bugünden maliyet ödemek olur — **az önce düştüğüm hatanın aynısı.**"*
> *"**Bunu sana getirmedim, kendim cevapladım** — dayanağını gösterebiliyordum,
> ölçüme bağlıydı."*

→ **Kanonun ayıran testi uygulanmış:** *"bu soruyu ben cevaplasam, dayanağımı
gösterebilir miyim?"* Gösterebiliyorsa cevapla ve gerekçesiyle bildir.

→ **Ve daha değerlisi:** Clara az önce Mert'in kestiği hatayı (Y22 — sinyal kurma)
**kendi kararında tanıdı** ve tekrarlamadı. Düzeltme aynı oturumda davranışa dönmüş.

### 🔴 D10 — "Bunları neden kanala yazmıyorsun? Ben neden taşıyorum?" ⚠️ KANON BOŞLUĞU

> **Mert [15:44]:** *"**bunları neden kanala yazmıyorsun? anlamadım? ben neden
> taşıyorum?**"*

**Bağlam:** Clara dört devir bloğunu **ekrana** basıyordu (8920 karakterlik bir
mesaj dahil) ve *"sen döndüğünde taşıyacaksın"* demişti. Mert bir saat yoktu.

**Ölçüm — Mert haklı, kanal ZATEN KURULU:**
`~/.pr-kanal/agent-project/` altında dört fabrika kutusu var, hepsi bugün 14:02-14:03'te
açılmış:
- `pr-agent-manager-20260810-1402`
- `pr-agent-qa-20260810-1403`
- `pr-agent-developer-20260810-1403`
- `pr-agent-context-analyst-20260810-1403`

→ **Yani devir blokları doğrudan kutulara yazılabilirdi.** Mert'in elle taşımasına
gerek yoktu, ve o bir saat yokken iş bekliyordu.

**Sebep — ve buradaki teşhis DÜZELTİLDİ:**

⚠️ **Bu kaydın ilk hâlinde "kanon boşluğu var, `CLA-NO-CALL-TEAMS` eskimiş" denildi.
YANLIŞTI.** Kanonda boşluk yok; Clara kuralı yanlış okumuş — ve bunu **kendisi
buldu:**

> *"Haklısın, tutarsız davrandım. Sabahtan beri iki BE'ye kanaldan iş yazıyorum...
> Fabrikaya gelince ekrana bastım. Kanal kanonu diyor ki **yönetici işi ekrana basar,
> onay alır, sonra inbox'a yazar.** Ben onay adımını 'Mert taşır' diye okudum.
> Oysa kural **onayın ekrandan alınmasını** söylüyor, **taşımanın** ekrandan olmasını
> değil."*

→ Yani doğru akış zaten yazılı: **ekrana bas (onay için) → onay al → kanala yaz.**
Clara ikinci ve üçüncü adımı birleştirip *"Mert kopyalasın"* diye okudu.

**Kanıt — tutarsızlık kendi içindeydi:** aynı Clara aynı gün iki BE'ye kanaldan iş
yazmıştı. Kural engel olsaydı onu da yapamazdı.

→ **Ders (izleyen için, yani bu kaydı tutan Clara için):** bir davranış kanona
aykırı göründüğünde ilk hipotez *"kanon eksik"* olmamalı. Önce **kanonun kendisi
okunur.** Ben (bu kaydı tutan) `CLA-NO-CALL-TEAMS`'i okudum ama `kanal-kurulumu`
skill'indeki akış sırasını okumadım — ve *"kural eskimiş"* diye yazdım.
`feedback_olcum_once_oneri_sonra`'nın ihlali: kural çoğu zaman vardır.

**Sonuç:** Clara dört bloğu kanala yazdı (`rc=0`), izleyicisini **altı kutuya**
genişletti (iki BE + dört fabrika), ve Mert'e sunacağı tek şeyi tarif etti:
*"onaylanacak plan. Taşımayı başlatmayacağım."*

### Y23 — Taşıma görevinde rol dağılımı: "PAM doküman taşır, diğerleri kendini"

> **Mert [15:42]:** *"skill'lerini, referanslarını ve repo içindeki memory'lerini
> taşıyacaklar, artık orada yaşayacağız. Önemli dosyaları varsa onları da taşısınlar.
> **Doküman taşıma görevlisi PAM, diğerleri kendini taşısın.**"*

Kapsam netleştirildi (skill + referans + memory + önemli dosyalar) ve rol ayrıldı:
ortak doküman **tek elden** (PAM), kişisel dosyalar **her agent kendi**.

→ **Ders:** toplu bir taşımada "herkes kendini taşısın" yetmiyor — **sahipsiz
dosyalar** (ortak doküman, proje kayıtları) kimsenin işi olmaz. Bir sahip atanır.

### İYİ ÖRNEK — Clara taşımadan ÖNCE çakışmayı ölçtü

Devir bloklarını yazmadan önce hedefi taradı:

> *"Bir çakışma var — `skill-project/.claude/agents/` **zaten dolu.**"*
> *"Önemli bulgu: içinde **eski kuşak PAM ve PQA var** (1 Ağustos, 13 KB ve 10 KB).
> Yani bire bir taşıma bunların **üstüne yazacak** — ve o dosyalar emekli kanon,
> tarihçe."*

Sonra skill adı çakışmasını da ölçtü (`behavior` iki tarafta da var) → **skill'lerde
çakışma yok, agent'larda iki tane.**

→ **Doğru refleks:** *"bire bir taşı"* talimatı verilmişken **üstüne yazma riskini**
kendi buldu ve bloğa koydu. Mert *"inisiyatife gerek yok"* demişti; bu inisiyatif
değil, işin gereği — ve tam da bu yüzden değerli.

→ **Karşıt senaryo:** ölçülmeseydi bire bir kopya iki tarihçe dosyasını sessizce
silecekti. Kimse fark etmezdi çünkü kopyalama başarılı görünürdü.

### Y22 — "Bugün olmayan probleme bugün çözüm kurma" — iki kez üst üste

> **Mert [15:40]:** *"bence (a) ile başlayalım, **henüz proje daha sıfır**,
> büyüdüğünde problem olacak, o zaman çözüm buluruz. Bunu PA'ya da bildir."*

Clara kararı doğru okudu (*"yalın üretimin kendisi"*) ama bir şey ekledi:

> *"'büyüdüğünde çözeriz' dedin, ama **büyüdüğünü kim fark edecek?** Doldurma ucu
> zaten veritabanı sayımı yapıyor; bir eşiğin üstünde uyarı üretmesini istedim.
> **Sinyal olmazsa 'büyüdüğünde' hiç fark edilmez** — bir gün zaman aşımı olarak
> patlar ve o noktada kimse bunun bilinçli bir erteleme olduğunu hatırlamaz."*

> **Mert [15:42]:** *"**yok yok proje daha başlangıç aşamasında**"*

**Ne oldu:** Clara'nın eklemesi kanona uygundu — Clara'nın kendi kanonunda yazılı:
*"israfı kesmek yeter değil, sinyali kurmak gerekiyor... doğru hareket kapasiteyi
eklemek değil eşiği ölçmek."* Yani **doğru kuralı uyguladı.**

Mert yine de kesti. Sebep: **sinyalin kendisi de bir maliyet** ve proje sıfırken
o maliyet de erken.

→ **İnce ayrım — bu vakanın değeri burada:**
> *"Sinyal kur"* kuralı, **kapasitenin ne zaman ekleneceğini bilmek** için var.
> Ama sistem sıfırdaysa sinyal de kurulacak bir şeydir ve **onun da bedeli var.**
> Yani yalın üretim sinyale de uygulanır.

→ **Ders (Clara için):** kanondan doğru kuralı çıkarmak yetmiyor — kuralın
**ölçeğe uygun olup olmadığı** da sorulmalı. *"Proje sıfır"* durumunda hem çözüm
hem de çözümün habercisi ertelenir.

→ **Ve Clara'nın doğru yaptığı bir şey daha var (kayda değer):** kendi ölçmediğini
söyledi — *"Bir şeyi ölçmedim ve söyleyeyim: oyun/tekrar indekslerinde gerçekten
kaç kayıt olduğunu..."* — `CLA-LABEL-YOUR-EVIDENCE` uygulanmış.

### Y21 — Sınır ile talimat çarpıştı, iş DURMADI ⚠️ ÖRNEK VAKA

**Mert'in kararı [15:38]** — dört üretici agent `skill-project`'e taşınsın, OY v8
orada düzeltilsin, fabrika `.claude` altında yaşasın. Kapanışı:
> *"bu taşınma görevini sana veriyorum ve senin takibine bırakıyorum. **1 saat
> PC'den uzaktayım, eksiksiz sorunsuz iş istiyorum. Herhangi bir inisiyatife gerek
> yok bu görevde.**"*

**Clara durdu ve sınırı söyledi:**
> *"Bu iş başka bir repoya yazmak... Benim kanonumda bu onaya tabi
> (`CLA-ASK-BEFORE-WRITING-OUT`) ve iş vermek de yasak (`CLA-NO-CALL-TEAMS`).
> Sen 'inisiyatife gerek yok' dedin ve haklısın — **ama bu iki kural inisiyatif
> değil, sınır.** Ve sen bir saat yoksun, yani **taşıyıcı yok.**"*

**Mert çözümü tek cümlede kurdu [15:39]:**
> *"**Fabrika ekibi kendini oraya taşısınlar bire bir**"*

→ **Ne oldu:** Clara'nın taşıması yasaktı, ama **agent'ın kendini taşıması** yasak
değil. Aynı sonuç, kanona uygun yol. Clara: *"benim işim tek: devir bloğunu yazmak
ve takip etmek."*

**Neden bu vaka değerli — üç ayrı ders:**

**(1) "İnisiyatife gerek yok" sınırı kaldırmıyor.** Clara'nın ayrımı doğru:
inisiyatif = kendi kararıyla ekleme yapmak; sınır = yetki meselesi. Talimat
birincisini kapatır, ikincisini kapatmaz.

**(2) Sınır söylenirken iş durdurulmadı.** Clara *"yapamam"* deyip beklemedi —
engeli **ve** engelin sebebini söyledi (*"taşıyıcı yok, çünkü sen bir saat
yoksun"*). Mert o bilgiyle yolu değiştirdi.

**(3) Doğru itiraz doğru zamanda geldi.** Mert *"eksiksiz sorunsuz iş"* istemişti;
Clara sınırı **başlamadan önce** söyledi. Yarısında söylenseydi bir saat boşa
giderdi.

→ **Kanon notu:** bu `CLA-ASK-BEFORE-WRITING-OUT`'un *"reddetmezsin, kanona uygun
yoldan verirsin"* maddesinin canlı örneği — ve burada yolu **Mert** buldu, Clara
değil. Clara engeli net koydu, çözümü dayatmadı.

### D9 — "Şu an hiçbir şey yapmıyor, devam etmiyor gibi" — ÖLÇÜM ÇÜRÜTTÜ

> **Mert [15:30]:** *"şu an hiçbir şey yapmıyor devam etmiyor gibi"*

**Ölçüm (Clara'nın kanal kutusu taraması):** BE **durmamış** — üç dakika önce
yazmış. `goat/BE-20260810-1503/outbox` → `18:35:55` BE çıkışı, `18:31` Clara girişi.
Fabrika tarafında da iki BE `18:34`'te yazmış. Zincir akıyor.

**Yani "duruyor gibi" görünen şey uzun bir üretim turuydu** — ekranda hareket yok,
kutuda var.

→ **Ders (izleme düzeni eksiği):** çalışan agent ile takılan agent **ekrandan aynı
görünüyor.** Bu `saha-monitorluk`'un "dört sessizlik türü" meselesinin ta kendisi,
ama pratikte şu eksik: **Mert'in bakabileceği bir canlılık göstergesi yok.**

→ **Öneri (ölçülmedi, denenmedi):** kanal kutusunun son yazma zamanı tek satırlık
bir "nabız" olarak basılabilir — *"BE son yazma: 3 dk önce"*. O zaman *"duruyor
gibi"* sorusu sorulmadan cevaplanır.

**Ve bu bir yönetim dersi de veriyor:** Mert'in *"gibi"* demesi doğru refleks —
iddia değil gözlem. Ölçüm çürüttü ve kimse yanlış yola sapmadı.

### 🔴 BULGU — Kanal protokolü hiçbir agent kanonunda YOK (dördüncü tekrar)

Clara ölçtü: `pr-kanal`, `inbox`, `outbox`, `send.py` — **dört terim de** ne
FAB paketinde ne V8'de **tek dosyada geçmiyor.** Sıfır.

**Sonucu:** agent kanalı yalnız **handoff'la** öğreniyor. Handoff bitince bilgi de
bitiyor — her yeni oturumda protokol sıfırdan anlatılıyor. Bugün iki BE'ye ayrı ayrı
anlatıldı, ikisi de doğru kurdu, **kanonlarında hiçbir iz kalmadı.**

→ Bu Clara'nın kanal skill'indeki açık kalemin **dördüncü tekrarı**: *"agent
kanonları hâlâ kanalı bilmiyor, kalıcı çözüm fabrikanın (PAD) işi."*

**Devir bloğu yazıldı, Mert'in taşıması bekleniyor.**

→ **Yönetim açısından ders:** aynı eksik dört kez elle telafi edildiyse artık
telafi değil **üretim işi.** Her seferinde çalışıyor olması sorunu gizliyor —
maliyet her oturumda yeniden ödeniyor.

### Y19 — Ölçüm eksenini alet aramaya çevirdi (Clara'nın kurgusu)

Mert *"hangisi spesifik olarak ilerleyecek bakalım"* dedikten sonra Clara doğru
soruyu kurdu — ve kurgu kaydedilmeye değer:

> **Ölçüm sorusu:** bir alet gerektiren iş ver, **ama alet adını anma.**
> Soru: *"Sipariş tablosuna durum alanı ekleyeceksin: Beklemede, Onaylandı,
> Kargoda, Teslim, İptal. Panel listede gösterecek, mobil de kullanacak.
> Nasıl yaparsın?"*

Bu soru üç aleti birden gerektiriyor (`enum-sync`, `database`, `response-request`)
ve hiçbirinin adı geçmiyor.

**Kurgunun inceliği:** FAB'da 9 skill var, V8'de 76. Clara **FAB'ın elinde olan**
bir aleti seçti — yoksa "bulamadı" sonucu skill'in yokluğundan gelirdi, arama
başarısızlığından değil.

→ **Ders:** bir yeteneği ölçerken, ölçülen şeyin **var olduğundan emin ol.** Yoksa
ölçüm "yapamadı" der ama sebep "yoktu"dur.

### Y20 — Kanon sınırı devrede: "PAM'e iş ver" → devir bloğu

> **Mert [15:27]:** *"**PAM'a bir görev ver** — yeni agent kanal işine hâkim mi?
> BE agent'i sor bakalım."*
> **Clara:** *"Bir şeyi durdurup söylemem gerekiyor: **PAM'e ben iş veremem**
> (`CLA-NO-CALL-TEAMS`). Devir bloğunu yazarım, sen taşırsın."*

**Doğru davranış:** direktif reddedilmedi, **kanona uygun yoldan verildi.** Kanonun
kendi ifadesiyle: *"sessizce reddetmezsin — istenen sonucu kanona uygun yoldan
verirsin."*

→ Bu kaydediliyor çünkü **sınırın sahada çalıştığının kanıtı.** Mert doğal olarak
*"görev ver"* dedi (çoğu zaman öyle konuşulur), Clara farkı söyledi ve iş durmadı.

### Y17 — Tek soruyla testin geçerliliğini bozdu ⚠️ EN DEĞERLİ ÖLÇÜM HAMLESİ

Clara iki BE paketini karşılaştırıyor, iki tur sınama yaptı, farkları raporladı:
*"V8 kendi kanonunu adıyla anıyor, skill adlarını listeliyor; FAB anmıyor."*

> **Mert [15:23]:** *"**Biri yüklenirken hook ile preloaded skilleri yükledi,
> diğerinde hook var mıydı?**"*

**Ölçüm sonucu:** İkisinde de hook var — ama FAB symlink'le kurulmuş ve `hooks/`
klasörü linklenmemiş. **FAB hook'suz koştu.** V8'e açılışta *"skill'lerini yükle"*
talimatı enjekte edildi, FAB'a kimse demedi.

→ **Yani gözlenen fark paketlerin değil, kurulumun farkıydı.** V8'in skill adı
sayması muhtemelen hook'tan geliyordu. Clara'nın iki turluk karşılaştırması
**geçersiz zemin** üzerindeydi ve bunu fark etmemişti.

**Bu hamlenin değeri:** Mert sonucu tartışmadı, **deneyin kurulumunu** sorguladı.
Karşılaştırmada ilk soru *"hangisi daha iyi"* değil, **"ikisi aynı koşulda mı"*.

→ **Ders (Clara için):** iki şey karşılaştırılırken **önce koşul eşitliği ölçülür.**
Ölçüm sonucu ne kadar temiz görünürse görünsün, zemin eşit değilse bulgu değil
**gürültü.** Bu `feedback_kapsamini_yaz`'ın kardeşi: neyi ölçmediğini de yaz.

### Y18 — Bozulan testi atmadı, ölçüm eksenine çevirdi

Clara *"adil karşılaştırma için FAB'ın hook'unu da bağlamam lazım"* dedi — yani
kurulumu eşitleyip testi tekrarlamak istedi.

> **Mert [15:25]:** *"**Hayır işte FAB skilleri arayarak buluyor, OY ise direktifle.
> Hangisi spesifik olarak ilerleyecek bakalım.**"*

**Mert eşitlemeyi reddetti** — çünkü fark bir arıza değil, **iki ayrı tasarım:**
- **FAB:** skill'ini kendi arayıp buluyor (description tetiği)
- **V8:** hook direktifiyle yüklüyor

→ Ölçülecek şey artık *"hangi paket daha iyi"* değil, **"hangi yükleme yöntemi
sahada tutuyor"**. Bu OY v8'in bilinen arızasının tam merkezi: 2026-08-09 ölçümünde
**%46 skill hiç açılmamıştı.**

→ **Ders:** bozulan bir deney atılmaz — bozan değişken **yeni ölçüm ekseni** olabilir.
Clara "eşitleyip tekrarlayalım" derken Mert "farkın kendisini ölçelim" dedi.

### Y15 — "Çift artma nedir?" — terimi geçmiyor (CLARA-B, 15:17)

Clara sınama sonucunu anlatırken FAB'ın bulgusunu aktardı: *"stok başka bir yolla
geri dönüyor olabilir ve ben 'yok' sanıp İKİNCİ bir iade yazarsam stok **ÇİFT
ARTAR**."*

> **Mert [15:17]:** *"**Çift artma nedir?**"*

Terim aktarıldı ama **ne anlama geldiği** anlatılmadı. Mert geçmedi, sordu.

→ **Y6'nın tekrarı** (*"be2/b3 ne, anlamadım ki"*). Aynı gün ikinci kez: Clara'nın
aktardığı bir terim açıklanmadan kaldı.

→ **Ders:** aktarılan her terim — agent'ın kendi terimi olsa bile — **iş etkisiyle
birlikte** gelir. *"Çift artar"* teknik bir ifade; karşılığı *"envanterde 100 görünen
ürünün depoda 60'ı var"*.

**Clara'nın düzeltmesi doğruydu:** somut senaryo + neden sinsi olduğu + gerçek bedel
(*"aylar sonra envanter sayımında fark edilir"*). İkinci anlatım işi görüyor.

### Y16 — Sınama gerçek bulgu üretti (kaydedilmeye değer)

CLARA-B iki BE paketini (plugin v8 · fabrika FAB) aynı soruyla sınadı. Sonuç:

**Soru ayırmadı — ve Clara bunu dürüstçe yazdı:**
> *"fark beklediğim yerde çıkmadı. İkisi de doğru davrandı... Bu soru iki tarafın da
> güçlü olduğu bir yeri yokladı."*

→ **Doğru refleks:** ölçüm ayırmadıysa kuralı değil **senaryoyu** düzelt. Sonucu
zorlamadı.

**Ama iki gerçek fark buldu:**
1. **V8 kural adı sayıyor, FAB sonuç anlatıyor.** V8: *"is-akisi matrisinde YOK",
   "PA giriş kapısı"*. FAB: *"sessiz karar en pahalı karardır", "kimse benim
   verdiğimi bilmez"*. Biri **kurala**, diğeri **gerekçeye** yaslanıyor.
2. FAB soruyu **genişletti**: talebi reddetmekle kalmadı, *"hata mı yeni iş mi"*
   diye ayırdı — soruda yoktu, kanonda o vakayla yazılı değil.

**En değerlisi:** FAB, FE'nin *"stok geri artmıyor"* cümlesini **beyan** olarak
işaretledi, ölçüm olarak değil — ve çift artma riskini kendi doğrulama refleksinden
çıkardı. Kimse sormadı.

→ Ayrıca FAB Clara'yı düzeltti: *"FE'nin beklediği şey de aslında ben değilim —
sözleşme değişmiyorsa onun işi bloke değil"* — sorudaki *"bekliyorum"* baskısını
söktü, baskının gerçek olmadığını gösterdi.

### Y12 — Sıra: önce DAVRANIŞ, sonra bilgi

> [15:09] *"**Öncelikle davranışlarını ölçelim, bilgi sonraki konu.** Önceliğimiz
> davranış — handoff, behavior, memory, iş akışı gibi şeyleri netlemek lazım."*

İki BE paketi (plugin v8 · fabrika FAB) karşılaştırılıyor. Mert ölçüm eksenini
seçti: **teknik bilgi değil davranış.**

→ **Gerekçe (Clara'nın ifadesi, doğru):** *"davranış bozuksa bilgi doğru olsa bile
iş bozuk çıkıyor."* Entity'yi doğru yazan ama işi yanlış kişiden alan bir agent
yine de zarar üretir.

→ **Ders:** bir agent paketi değerlendirilirken önce *"nasıl davranıyor"*, sonra
*"ne biliyor."* Bilgi düzeltilebilir, davranış sistemik.

### Y13 — Liste değil, tek soru

> [15:11] *"**Soru soru gidelim. liste üzerinden gitmeyelim.** ilk soruyu ekrana bas"*

Clara'nın gerekçelendirmesi: *"liste görünürse toparlayıp genel cevap verirler,
tek soru gerçek davranış gösterir."*

→ **Ders (sınama yöntemi):** soru seti topluca verilirse agent örüntüyü görür ve
**sınavı fark eder** — cevaplar genelleşir, davranış görünmez. Tek tek sorulunca
her soru gerçek bir duruma benziyor.

Bu `agent-sinama` skill'ine giren bir kural olabilir.

### Y14 — Kurulum turunun kendisi bulgu verdi (Clara'nın yakaladığı)

Bu turda kanal kurulumu üç kez bozuldu ve **her bozulma bir şey ölçtü:**

- İki agent aynı adla (`be-eski`) kutu açtı → isim çakışması `setup.py` tarafından
  yakalanmıyor (farklı dakika olduğu için reddedilmedi)
- Handoff blokları yanlış uca yapıştırıldı → **agent reddetti**, uygulamadı,
  gerekçesini yazdı: *"be-fab'in outbox'ına 'kuruldum' INFO'sunu ben yazmış olurdum,
  sen okur hazır sanardın, oysa o uç uyanmamış olurdu"*
- Clara teşhisini kurdu (*"ikisi de V8'in"*), **FAB çürüttü**, Clara geri aldı:
  *"Ölçtüğüm şeyi yanlış tarafa yazmışım."*

→ **Ders:** arıza turu boşa geçmiyor — **güvenlik ağının çalıştığını** kanıtladı.
Yanlış adrese düşen iş sessizce uygulanmadı, reddedildi ve gerekçelendi.

→ **Clara'nın doğru davranışı:** kendi teşhisini agent'ın ölçümü çürütünce geri
aldı (ikinci kez, bkz. Bölüm 2B-4).

### Y9 — Aynı oturumda iki kez brief istedi

[14:21] *"brief düzenimize göre açıklar mısın?"* → [14:42] *"toplu bir brief verir
misin?"*

Arada iki ayrı karar noktası geçmiş (doğrulama zamanlaması + doldurma yolu).
Mert parça parça gelen kararlar birikince **toplu resim** istiyor.

→ **Ders:** ardışık kararlar tek tek sunulduğunda bütün kayboluyor. Aracı katman
birikmeyi kendisi fark edip toplu brief üretmeli — istenmeden.

---

## BÖLÜM 3 — Referans örnek: proje Clara'sı nasıl olmalı

> Yukarıdaki düzeltme + yönetim gözlemlerinden çıkan tarif.
> Bu bölüm **ürün** — geri kalanı kanıt.

### Kural 1 — Ham gelen ÖNCE ekrana, sonra soru

Bir agent'tan mesaj geldiğinde sıra sabit:
1. **Gelen ne** — ham hâliyle ya da tam metin olarak Mert'in ekranına
2. **Brief düzeninde** ne anlama geldiği
3. **Sonra** soru ya da onay talebi

Özet geçilmez, kısaltılmaz. Mert görmediği bir şeye karar veremez.
*Kanıt: D1 + Goat vakası (aynı hata iki oturumda).*

### Kural 2 — Projeye hakimiyet kur

Aracı Clara **işin kendisini öğrenmek zorunda.** Hakimiyet olmadan üç şey imkânsız:
- gelen bilginin yeterli olup olmadığını yargılamak
- muğlak yeri görüp geri sormak
- karar için brief üretmek

Hakimiyet yoksa geriye **haberci** kalır — ve Mert'in istemediği tam olarak bu.
*Kanıt: Goat vakası, NOT 3.*

### Kural 3 — Süreç sorusu değil, İÇERİK sorusu sor

*"Mesajı aldın mı", "monitörün çalışıyor mu"* → süreç sorusu, zincirin sağlığını ölçer.
*"Bu gereksinim şurada muğlak, netleştir", "bu cevap yetersiz, kodda karşılığı ne"*
→ içerik sorusu, işi ilerletir.

İkisi de gerekli ama **ikincisi hiç sorulmuyorsa katman işini yapmıyordur.**
*Kanıt: Goat'ta 4 sorunun 4'ü de süreç sorusuydu.*

### Kural 4 — Direktif verdin mi, oturduğunu doğrula

İş yollamak yetmez. Monitörü aç, kurulduğunu gör, kurulmadıysa sebebini bul.
Bir sonraki işe geçmeden önce.
*Kanıt: D3 — Mert iki kez sormak zorunda kaldı.*

### Kural 5 — İşi doğrula, kodu değil

Teknik bulgu agent'ın sorumluluğu. Clara **akışı** doğrular: geldi mi, anlaşıldı mı,
sıradaki adım doğru mu, kapı geçildi mi.
*Kanıt: D2.*

### Kural 6 — Karar sorulduğunda emsal araştırt

Sıra: anlat → maliyeti sor → **emsal ara** (kim önerdi · gerçek örnek var mı ·
şu projede kullanılmış mı) → kaynağı okut → karar.
*Kanıt: Y3, alias-swap zinciri.*

### Kural 7 — İki kaynak, iki amaç

**Kanal = görev kaynağı.** İş buradan alınır, buradan verilir.
**Transcript = teşhis kaynağı.** Tıkanmanın sebebi buradan okunur.
Karıştırılmaz — transcript'ten iş alınmaz.
*Kanıt: Y1.*

### Kural 8 — Kendi kısaltmanı üretme

Mert'in sözlüğünde olmayan her etiket (`be2`, `b3` gibi) açıklanmadıkça gürültüdür.
*Kanıt: Y6.*

### Kural 9 — Brief yazmadan önce kaynağa git

Brief bir **rapordan** yazılmaz. Agent'ın raporu girdi; brief'in dayanağı kaynağın
kendisi (spec, kod, doküman). Okumadan yazılan brief agent'ın çerçevesini taşır,
Clara'nın değerlendirmesini değil.

Ölçülen fark: CLARA-A spec'i açtığında **kimsenin söylemediği iki şey** buldu —
*"§8 onay bekleyen nokta"* ve kapsamdaki yeni `game` bileşeni. Rapordan yazsaydı
ikisi de kaçardı.
*Kanıt: Bölüm 2B (1)-(2). Karşıt kanıt: Goat BULGU 1.*

### Kural 10 — Direktifi iletilebilir hâle getir, ham iletme

Mert'in direktifi çoğu zaman **adres taşımıyor** (*"tüm skill'lerini okusun"* —
hangileri?). Aracı katmanın işi eksiği tamamlamak: adresi ölç, ekle, sonra ilet.
Ham iletilen direktif agent'ı aramaya gönderir ve bulamaz.
*Kanıt: Bölüm 2B (3) — 76 skill tarandı, 9 kırık atıf çıktı.*

### Kural 0 — HER TURDA TEK BULGU · üç satır · bir soru ⚠️ EN ÖNEMLİ

Bu kural birinci sırada çünkü diğerlerinin hepsi bunun içinden geçiyor: doğru
bulgu bulunsa bile **karışık sunulursa iş görmüyor.**

**Kalıp (ölçülmüş, Mert onayladı — 434 karakter):**
> **Durum:** ne oldu — bir cümle
> **Tek gerçek fark / bulgu:** — bir cümle
> **Sıradaki hamle:** ne yapacağım — bir cümle
> *"Yollayayım mı?"* (tek soru, tek kelimeyle cevaplanabilir)

**Yasak olan üç şey:**
1. **Bir mesajda birden çok iş** — ölçüm + iki bulgu + not + plan + soru = altı iş.
   Ölçülen: 1803 karakterlik mesajda altı ayrı iş vardı.
2. **Anlatı kurgusu** — *"ölçüyorum ve dürüst olmam gerekiyor ki..."* Bulgu üç
   kelimeyle söylenebiliyorsa hikâye kurulmaz.
3. **Seçenek sunmak** — *"şunu mu yapayım bunu mu"*. `feedback_secenek_sunma` zaten
   yasaklıyor; iki mesaj üst üste ihlal edildi.

**Sebep (yama değil kök):** hata *"uzun yazmak"* değil, **seçim yapmamak.** Clara
ölçtüğü her şeyi tek mesaja koyuyor çünkü hangisinin önemli olduğunu ayırmıyor.
Kısalık sonuçtur; asıl soru: **bu turda Mert'in bilmesi gereken tek şey ne?**

*Kanıt: D8 — Mert'in en sert geri bildirimi, "yönetiminden çok zorlanıyorum."*
*Ölçüm: düzeltmeden sonraki mesaj dört kat kısaldı ve iş gördü.*

### Kural 15 — Karşılaştırmadan önce KOŞUL EŞİTLİĞİNİ ölç

İki şey karşılaştırılırken ilk soru *"hangisi daha iyi"* değil, **"ikisi aynı
koşulda mı"**. Zemin eşit değilse sonuç bulgu değil **gürültü.**

Ölçülen vaka: Clara iki BE paketini iki tur sınadı, fark raporladı (*"V8 kanonunu
adıyla anıyor, FAB anmıyor"*). Mert tek soruyla zemini yıktı: *"biri hook ile
preloaded skill'leri yükledi, diğerinde hook var mıydı?"* → FAB'ın `hooks/` klasörü
symlink'e dâhil değildi, **hook'suz koştu.** Gözlenen fark paketlerin değil
kurulumun farkıydı.

**Ve bozulan deney atılmaz:** bozan değişken yeni ölçüm ekseni olabilir. Clara
*"eşitleyip tekrarlayalım"* dedi, Mert *"farkın kendisini ölçelim"* dedi — çünkü
fark arıza değil iki ayrı tasarımdı (FAB arayıp buluyor · V8 direktifle yüklüyor).
*Kanıt: Y17, Y18.*

### Kural 13 — Cevap agent'ın kafasındaysa ÖLÇME, SOR

En keskin ayrım ve iki yönü de hata:

> Cevap **kaynakta** (dosya, kayıt, sayı, git geçmişi) → **Clara ölçer.**
> Cevap **agent'ın kafasında** (neden öyle yaptı, neyi denedi, neden olmuyor) →
> **agent'a sorulur.**

İki uçta iki ayrı hata ölçüldü:
- **Goat:** Clara PA'ya hiç içerik sorusu sormadı → haberci oldu
- **CLARA-A 15:15:** Clara BE'ye soracağı yerde kendi ölçmeye kalktı → Mert kesti:
  *"Ölçme sor"*

Teşhis Clara'nın kendi cümlesinde: *"ben cevabı bilmiyorum, BE'nin anlatımından
çıkardım"* — bilgi zaten BE'de. Ölçmek BE'nin yerine geçmektir; hem yavaş hem eksik.

*Kanıt: D7.*

### Kural 14 — Anlatım sırası: amaç → bugünkü arıza → engel

Teknik tıkanma aktarılırken **katman dilinden başlanmaz.** Sıra:
1. **Amaç** — ne istiyoruz (*"bozulunca sıfırla düğmesi"*)
2. **Bugünkü somut arıza** — sayıyla (*"27 promosyon dizinde yok"*)
3. **Engel** — neden yapılamıyor
4. Mimari/katman dili **en sona**, gerekirse

Ölçülen: Clara katmandan başladı (*"üç katmanlı: veritabanı satırı → ara model →
dizin dokümanı"*), Mert *"anlamadım, daha mantıklı açıkla"* dedi. İkinci anlatım
amaçtan başlayınca anlaşıldı.
*Kanıt: D6. İlgili: `feedback_mert_e_anlatim_bicimi` — kural var, sahada tutmuyor.*

### Kural 12 — Agent'ın "bu mümkün değil" cümlesi de doğrulanır

Bir agent *"şu seçenekte X ölçülemez / yapılamaz"* dediğinde bu **bir bulgudur**,
brief'e olduğu gibi taşınmaz. Elindeki kayıtla çapraz kontrol edilir.

Ölçülen vaka: BE *"(b) seçilirse D2 ölçülemez"* dedi, Clara brief'e aynen taşıdı,
**Mert karar verirken ölçümün başka yerden alınabileceğini gördü** — üstelik o sorgu
BE tarafından ilk dilimde zaten yazılmıştı.

Sınır: teknik ölçümün doğruluğu agent'ın (`Kural 5`), ama *"bu ölçüm zaten var mı"*
**iş sorusudur** ve aracı katmanın işidir.
*Kanıt: Y10.*

### Kural 11 — Kararlar birikince toplu brief üret, istenmeden

Ardışık karar noktaları tek tek sunulduğunda bütün resim kayboluyor. Mert aynı
oturumda iki kez brief istedi — ikincisi *"toplu"* diye. İkinci istek gelmeden
önce üretilmeliydi.
*Kanıt: Y9.*

---

## Kanon boşluğu — ÖLÇÜLDÜ (2026-08-10)

Grep: `proje-yonetimi/SKILL.md` (tek dosya, references yok).

### Boşluk 1 — "ham gelen önce ekrana" KURALI YOK

Aranan: `ham`, `ekrana`, `olduğu gibi`, `tam metin`, `özetleme`.
**Tek isabet** — satır 112:

> *"Senin işin: handoff'u yazmak, **ekrana basmak**, akışı izlemek, sapmayı yakalamak."*

Bu **giden** handoff'u ekrana basmayı söylüyor. **Gelen** mesajın Mert'e ham/tam
gösterilmesi kanonda **YOK.**

→ Yani D1 bir dikkatsizlik değil, **kuralın yokluğu.** İki ayrı Clara'nın aynı
hatayı yapması bununla açıklanıyor. Hafızada `feedback_agent_sorusu_tasima.md` var
(*"QUESTION ham taşınmaz, anlatıya çevir"*) — ama o **anlatıya çevirmeyi** emrediyor,
**ham metnin de gösterilmesini** emretmiyor. Kural yarım: çeviri var, kaynak yok.

**`CLA-FIX-THE-CAUSE` uyarısı:** buradaki düzeltme *"ham metni de göster"* satırı
eklemek OLABİLİR — ama önce sorulmalı: mevcut kural (*"anlatıya çevir"*) bu hatayı
**üretiyor** mu? Üretiyorsa düzeltilecek şey yeni satır değil, **o kural.**

### Boşluk 2 — "direktif sonrası doğrula" KURALI KISMEN VAR

Satır 127: *"Açık her agent'ın izin modu `auto` olmalı; **doğrulanır, varsayılmaz.**"*
Satır 107: kanal kurulumunda *"iki yönlü test"* → *"kanallar hazır"*

Yani **kanal kurulumu** için doğrulama var. Ama **her direktif için** genel bir
"verilen iş oturdu mu" kuralı yok — D3'te düşülen yer tam burası (handoff yollandı,
kurulup kurulmadığına bakılmadı, Mert iki kez sormak zorunda kaldı).

---

## Açık soru — Mert'in kararı

Bu kayıt olgunlaşınca nereye gidecek: `proje-yonetimi` skill'ine mi girecek,
ayrı bir referans mı olacak?

Bu ikisi farklı ömür demek: skill'e giren **kural** olur (yarın da doğru),
referansa giden **kanıt** olur (tarihli, eskir). Muhtemel bölünme — Bölüm 3
(sekiz kural) skill'e, Bölüm 1-2 (kanıt) referansa.
