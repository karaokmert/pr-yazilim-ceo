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

> ⚠️ **Ölçüm tuzağı (2026-08-10):** Clara oturumunu transcript içinde `"Adın Clara"`
> arayarak bulmak GÜVENİLMEZ — sistem prompt ilk 120 KB'da olmayabilir; ilk denemede
> üç oturumun üçü de kaçtı. Kimlik `ps` çıktısından ya da kanon izlerinden (≥2 işaret)
> tespit edilir.

---

## İzlenen oturumlar

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
