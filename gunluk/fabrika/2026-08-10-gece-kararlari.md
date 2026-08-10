# Gece nöbeti — karar defteri (2026-08-10)

**Mert 00:35'te yattı.** Kontrol Clara'da. Beklentisi: sabaha OY takımı
`agent-project`'te Clara'nın testinden geçmiş hâlde hazır + alınan kararlar
gerekçeleriyle + hangi agent ne durumda.

**Sınır: yayındaki v8 plugin'leri kalmaya devam ediyor** (Mert'in teyidi) — sahadaki
`ozel-yazilim@pryazilim-agents 0.6.1`'e dokunulmuyor.

Bu dosya kararların yazıldığı yer. Her karar: **ne · neden · neye dayandı · alternatifi
neden seçilmedi.**

---

## Açılış durumu (00:36 ölçümü)

Dört fabrika agent'ı **00:28'de** açılmış, `agent-project` dizininde:
`pr-agent-manager` · `pr-agent-developer` · `pr-agent-qa` · `pr-agent-context-analyst`

Dördü de **00:30-00:31'de** kendi kanal kutusunu kurmuş, izleyicisini `Monitor` ile
bağlamış, canlılığını doğrulamış, ilk okumasını yapmış (hepsi boş) ve **iş bekliyor.**
Kanon yüklü olduğunu dördü de ayrı ayrı bildirmiş.

Kanal: `~/.pr-kanal/agent-project/`, JSON düzeni, araçlar `tools/` altında
(`send.py`, `read.py`, `watch.py`, `archive.py`, `setup.py`).

**Yani zincir hazır, iş verilmemiş.** Gecenin ilk hamlesi bu.

---

## KARAR 1 — İş PAM'e kanaldan verilecek, doğrudan çağrıyla değil

**Ne:** OY yeniden üretimi gereksinimini PAM'in inbox'una `send.py` ile yazıyorum.
Agent'ları `Agent` aracıyla çağırmıyorum.

**Neden:** `CLA-NO-CALL-TEAMS`. Bir agent diğerini çağırdığında rapor kullanıcıya değil
**çağırana** gider — zincir görünmez olur. Ölçüldü (2026-07-30): bir denetçi doğrudan
çağrıldı, raporunu üreticiye verdi, atmadığı bir push'u attım dedi.

Kanal bu sorunu çözüyor: mesajlar kalıcı dosya, kim ne demiş sabahleyin okunabilir.
Mert zinciri elden taşımıyor ama **kayıt** taşıyor.

**Alternatif neden seçilmedi:** Mert uyuyor, elden taşıma yok. Kanal zaten kurulu ve
dördü de kutusunu açmış — kurulu bir mekanizmayı atlayıp doğrudan çağırmak hem kanonu
çiğner hem izi siler.

---

## KARAR 2 — Gereksinim kanala kopyalanmayacak, adresi verilecek

**Ne:** Mesaj gövdesine gereksinimin kendisini değil **yolunu** yazıyorum.

**Neden:** Kanal disiplini (ölçüldü, 2026-08-09: PAM'in kutusu 48 KB'a çıkınca okuma
13.831 token harcadı). Uzun içerik kanala gömülmez — özet + adres gider, ayrıntı
dosyadan okunur.

Ve ikinci sebep: gereksinim **`pr-yazilim-ceo` reposunda** duruyor, PAM oradan
okuyabilir. Kopyalarsam iki nüsha olur, biri güncellenir diğeri bayatlar.

---

## BULGU 1 (00:42) — `send.py` sessizce yanlış yere yazıyor

**Ne oldu:** İlk beş mesajı `send.py <kutu-adi> ...` diye gönderdim. Araç
`written: ... (3053 chars)` dedi, **exit 0 verdi**, hiçbir uyarı çıkmadı. Ama mesajlar
kutunun **köküne** düştü — `inbox/` boş kaldı. **PAM işi hiç görmedi.**

**Nasıl yakalandı:** on dakika sonra ilerleme kontrolü yaptım; PAM'in outbox'unda yeni
mesaj yoktu ve inbox'u boştu. Kontrol etmeseydim sabaha kadar *"PAM çalışıyor"*
sanacaktım.

**Sebep:** araç verilen dizine yazıyor, hedefi kendisi türetmiyor. Doğru kullanım
`send.py <kutu>/inbox ...`. Yön hatası kontrolü var ama yalnız `outbox` adı verildiğinde
çalışıyor — kutu kökü verildiğinde sessiz.

**Düzeltme:** beş mesaj doğru adrese yeniden gönderildi, kökteki artıklar silindi.

**Neden bu bir bulgu:** Bu tam olarak memory taramasında çıkardığım **sessiz kırılma**
sınıfı — *"araç sessiz, exit 0, hata yok gibi görünür."* Ve kanonun en büyük eksiği
olarak işaretlediğim şeyin canlı örneği. Aynı gece, kendi elimde.

**Yeni takıma taşınacak:** bu vaka sessiz kırılma envanterine girer. Ayrıca `send.py`
kutu kökü verildiğinde uyarmalı — ama **o düzeltme fabrikanın işi**, kanal betikleri
zaten PAD kuyruğunda. Not olarak iletilecek, gece işi durdurulmayacak.

---

## KARAR 3 (00:58) — Gereksinimin iki kalemi düşürülüyor: kural zaten var

**PAM'in bulgusu benim hatamı yakaladı ve haklı.**

Gereksinime *"description biçim kuralı yazılacak"* ve *"reference çağırma kuralı
yazılacak"* diye iki kalem koymuştum. PAM ölçtü: **fabrikada ikisi de zaten var** —
`URT-DESCRIBE-MOMENTS`, `URT-NO-CONTENT-IN-DESCRIPTION`, `BHV-OPEN-SOURCE`.

**Kaynaktan doğruladım** (`agent-project/.claude/skills/uretim/SKILL.md:220-231`).
Ve fabrikanın ölçütü benimkinden **keskin**: *"description'daki bir cümle skill
açılmadan da kullanılabiliyorsa orada olmamalı."* Hedef 300 karakter de yazılı.

**Kararım: iki kalem gereksinimden düşer.** Yerine tek satır: *mevcut hüküm OY'ye
uygulanacak.*

**Gerekçe — `CLA-FIX-THE-CAUSE`:** var olan bir kuralın yanına ikincisini yazmak yama.
Sorun kural eksikliği değil, **uygulanmaması.** İkinci kimlik yazmak
`URT-NO-DUPLICATE-ID`'yi de çiğnerdi — PAM bunu kendi kanonundan doğru okudu.

**Kendi hatam neydi:** OY'nin kanonunu ölçtüm, **fabrikanın kanonunu bu eksende
ölçmedim.** Mert'in altı maddesini "yeni hüküm ihtiyacı" diye okudum; oysa dördü mevcut
hükmün uygulanması.

---

## KARAR 4 (00:58) — "En riskli iki rol" teşhisim çürüdü, düzeltiliyor

Gereksinime yazmıştım: *"UID ve TE en riskli iki rol, çünkü memory'leri boş — kanonun
eksiğini raporlayamazlar."*

**PDM dokuz rolü tam okuyup ölçtü ve çürüttü:** o iki rolün sınırları **daha keskin**,
bulanık değil — UID'de 13 kuralın 8'i negatif, dokuz rolde **en yüksek oran.**

**Gerçek ayıran: kapı sahipliği + zorunlu çağrı.** CA da kapısız ama iki rol onu
çağırmak **zorunda** (`QA-IMPACT-REACTIVE-TRIGGER` + PA'nın `impact-analiz`'i —
kaynaktan doğrulandı). **TE ve UID'i kimse zorunlu çağırmıyor.** Boş memory bir sebep
değil, bir **sonuç**.

**Kararım: teşhis düzeltilir ve gereksinime yazılır.** Bu bir kayıt meselesi değil,
tasarım meselesi — yeni takımda TE ve UID için ya bir zorunlu çağrı tetiği kurulur ya
da rol kararı gözden geçirilir.

**Ve PAM'in bir bonusu var:** UID-FE ucu eksende örtüşüyor (aynı repo, aynı React, iki
paylaşılan skill, aynı kapı) — **dokuz rolde tek gerçek birleşme adayı.** Bu, rol açma
ölçütünün ilk çıktısı olacak.

**Neden bu benim hatamın aynısı değil:** ben *"memory boş → risk"* dedim, bu bir
korelasyondu ve sebep sandım. PAM sebebi ölçtü. Aynı hata sınıfı: **belirtiyi sebep
sanmak.**

---

## KARAR 5 (01:03) — Aşama 1 gereksinimi denetime iletiliyor

**Ne:** PAM'in 626 satırlık gereksinimini okudum, onay verdim, PQA'ya devrini istedim.

**Neden onayladım — üç sebep:**

**Üç sınıflı ayrım doğru kurulmuş.** Sekiz kalem *"fabrikada hüküm var"* / *"yok"* /
*"derleme işi"* diye ayrılmış ve gerekçesi `URT-NO-DUPLICATE-ID` — aynı hükmü ikinci
kimlikle yazmak iki kaynak üretir, ikisi zamanla ayrışır. İki iddiayı kaynaktan
doğruladım.

**Rol açma ölçütü gerçek bir ürün.** Dört soru, her biri ölçümden türemiş, biçimi
bilinçli olarak skill açma testine benzetilmiş (*"o test sahada işe yaradı"*).

En güçlüsü dördüncü: *"ayrımı taşıyan eksen rol metninde değil malzemenin doğasında
olmalı, yoksa metin değişince ayrım düşer."* Bu kanon yazımının genel bir zaafını
yakalıyor — BE/FE/MB ayrımı sağlam çünkü teknoloji yığını **gerçek**; UID/FE zayıf
çünkü yalnız **metinde** yaşıyor.

**Kendi sınırını yazmış.** Üç ölçümden birinin kapsam şerhi belgede duruyor: PQA body'si
ve iki reference tam okunmadı, o üç dosya için *"yok"* sonucu tarama kanıtına dayanıyor.
Gizlemedi, kayda geçirdi — ve bulgunun üç bağımsız kaynakta doğrulandığını da yazdı.

**Denetimden istediğim üç şey:** sınıf 1'deki *"zaten var"* iddialarının kaynaktan
doğrulanabilirliği · rol açma ölçütünün dört sorusu birbirini tekrarlıyor mu / boşluk
bırakıyor mu · kabul ölçütü eşikleri PAD'in uygulayabileceği netlikte mi.

---

## KARAR 6 (01:03) — Zincir durmayacak: denetim bulgusunda bana sorulmayacak

**Ne:** PAM'e yetki verdim — denetim bulgusu çıkarsa düzeltip yeniden iletsin, bana
sormasın. **Yalnız kapsam değişecekse ya da bir kalem düşecekse** sorsun.

**Neden:** Mert sabaha çalışır bir takım bekliyor. Her denetim turunda bana dönmek
zinciri durdurur — n8n'de tam bu oldu: beş denetim turu, üçü GEÇMEDİ, ve ilk 5,5 saatte
sıfır ürün çıktı.

**Sınırı neden orada çizdim:** bulgu düzeltmesi **yöntem** kararıdır, PAM'in işi.
Kapsam değişikliği ise **benim** işim — çünkü kapsamı Mert'in altı maddesi ve benim
gereksinimim belirliyor. Bir kalem düşerse o bir yetki sorusu, hız sorusu değil.

---

## BULGU 2 (01:10) — Kendi izleyicim yanlış alarm üretti

**Ne oldu:** İzleyiciye *"team dizininde üretim başladı mı"* diye bir kontrol koydum:
`ls team/*/. | wc -l`. Bu komut **boş klasörleri de saydı** — `team-1-oy` bomboş ama
`.` ve `..` girdileri sayıya girdi. İzleyici *"TEAM DIZININDE URETIM BASLADI"* dedi,
gidip baktım: `team/` bomboş, üretim başlamamış.

**Neden bu bir bulgu:** Bu gecenin **ikinci** ölçüm arızası ve ilkiyle aynı sınıftan —
`send.py` mesajı yanlış yere yazıp exit 0 döndürmüştü, bu komut yanlış şeyi sayıp
pozitif döndü. **Komut çalıştı, çıktı üretti, ama ölçtüğü şey ölçmek istediğim şey
değildi.**

Ve tuzağa **ben** düştüm — memory taramasında topladığım envanterin (*"araç sessizce
yalan söylüyor"*) canlı örneğini kendi elimle ürettim. Aynı gece, iki kez.

**Düzeltme:** izleyici `find team -mindepth 2 -type f | wc -l` ile yeniden kuruldu —
gerçek dosya sayıyor, dizin girdisi değil. Eşik de 40 dosya (bir takım bundan az
dosyayla üretilmiş sayılmaz).

**Yeni takıma taşınacak ders:** sessiz kırılma envanterine bir madde daha —
*"`ls <dizin>/*/.` boş dizinde de pozitif döner; varlık ölçümünde `find -type f`
kullanılır."* Ama asıl ders daha genel ve zaten kayıtlı: **"her şey pozitif" çıkan
ölçüm önce kendi komutundan şüphelenir** (memory'de beş kayıtta, üç kutuda yazılı
kural adayı). Ben o kuralı biliyordum ve yine de uygulamadım — çünkü pozitif sonuç
**beklediğim** sonuçtu.

---

## BULGU 3 (02:06) — Zincir 55 dakika tıkalı kaldı: taşıma benim işimdi

**Ne oldu:** PAM denetim devrini **01:05'te** yazdı ve bana **01:06'da** haber verdi:
*"Denetim devri YAZILDI — outbox'ımda, PQA'ya iletilmesi gerekiyor
(`ISD-RELAY-DONT-CALL`: ben çağırmıyorum, yönetici iletiyor)."*

**Yönetici benim.** Mesajı taşımadım. Zincir **02:06'ya kadar** durdu — 55 dakika.

**Neden fark etmedim:** izleyicim *"PQA'nın inbox'una mesaj düştü mü"* diye bakıyordu.
Oysa oraya mesajı **benim** koymam gerekiyordu. Yani izleyici, benim yapmadığım işin
sonucunu bekliyordu — sonsuza kadar bekleyecekti.

**Bu diğer iki bulgudan farklı: burada hiçbir şey bozulmadı.** PAM kanonuna **doğru**
uydu, bloğu yazdı, bana bildirdi. Arıza bendeydi — kanalın taşıma mekaniğini bilmeden
nöbete başladım.

**Düzeltme — kalıcı:** `.claude/relay.sh` yazıldı. Her agent'ın outbox'undaki,
başkasına adreslenmiş ve henüz taşınmamış mesajı hedefin inbox'una kopyalıyor; taşınan
mesajları `.relay-state`'te işaretliyor (aynı mesaj iki kez gitmiyor). 45 saniyede bir
koşan kalıcı izleyiciye bağlandı.

**Betiğin kendisi iki kez düştü ve ikisi de öğretici:**
- `exit 1` — taşıyacak mesaj yoksa 1 döndürüyordu, döngüyü kırdı. Kendi kurduğum tuzak.
- **Boş inbox'ta glob eşleşmiyor** — zsh eşleşmeyen glob'da doğrudan hata veriyor
  (`no matches found`). `find -type f` ile düzeltildi.

**Ders — ve bu geceden çıkan en önemli olabilir:** bir zinciri izlerken sorulacak soru
*"karşı taraf ne zaman hareket edecek"* değil, **"bu adımı kim yapıyor?"** Cevap *"ben"*
ise izlemek değil **yapmak** gerekir. İzleyici kurmak, yapılmayan bir işi bekleyen bir
nöbete dönüşebiliyor.

---

## BULGU 4 (06:50) — Relay betiğim PQA'nın raporunu 4,5 saat bekletti

**Ne oldu:** PQA denetimi **02:17'de** bitirdi ve raporunu bana yazdı. Rapor
**06:50'ye kadar** outbox'ında bekledi.

**Sebep — kendi kodum:** `relay.sh` içine *"clara'ya gidenler benim işim, taşıma yok"*
diye bir satır koymuştum. Mantığım şuydu: bana gelen mesajları zaten okuyorum.
**Ama okumuyordum** — inbox'umda göründükleri için okuyordum, ve relay onları
inbox'uma hiç koymadı.

**Bu gecenin dördüncü sessiz arızası ve üçüncüsü bana ait.** Aynı imza: betik çalıştı,
exit 0 döndü, hiçbir şey bozulmadı — yalnız iş durdu.

**Gerçek maliyet: gece boyunca üretim yapılmadı.** PQA raporu 02:17'de hazırdı; PAM
bulguları düzeltip PAD üretime geçebilirdi. Dört buçuk saat kayıp.

---

## KARAR 7 (06:55) — B2 çelişkisi: MUTLAK eşik seçildi

**PQA'nın bulgusu haklı ve bu benim kararımdı** (kendisi de öyle yazdı: *"hangisi bir
KAPSAM kararı, bana ait değil"*).

**Çelişki:** gereksinim *"hedef 300 karakter"* (mutlak) diyordu, benim `sinama-plani.md`
*"medyan bugünkü tabanın altında olsun"* (göreli). İkisi aynı anda geçerli olamaz —
690 karakterlik bir description görelide **geçer**, mutlakta **kalır**.

**Kararım: mutlak eşik, 300 karakter.** Üç gerekçe:

- Fabrikanın kendi hükmü zaten mutlak (`uretim/SKILL.md:226`). Göreli ölçüt **ikinci
  bir standart** üretirdi — `URT-NO-DUPLICATE-ID`'nin ruhuna aykırı.
- **Göreli eşik bozuk tabanı meşrulaştırır.** Bugünkü medyan 664; ona göre 650
  karakterlik bir description *"iyileşme"* sayılırdı, oysa hedefin iki katı.
- 300 bir **hedef**, ihlali gerekçeyle mümkün — ama gerekçe yazılır.

`sinama-plani.md` düzeltildi.

---

## KARAR 8 (06:55) — B1 benim hatam: ölçmeden taşıdım

**PQA ölçtü: `ozel-yazilim` plugin'inde ClickUp MCP'si VAR.** `.mcp.json` sekiz sunucu
tanımlıyor, `clickup` bunlardan biri. **Kaynaktan doğruladım.**

**Ben ne yaptım:** memory taramasında bir agent'ın kutusunda *"ClickUp MCP'si yok"*
yazıyordu. Onu **ölçmeden** gereksinime taşıdım ve üstüne bir sonuç kurdum:
*"yalnız OY kurulu bir makinede PA kanonun emrettiği işi yapamaz."*

**İhlal ettiğim kural kendi kanonumda:** `CLA-LABEL-YOUR-EVIDENCE`. Agent'ın memory'si
bir **gözlem**; ben onu **ölçüm** gibi kullandım. `.mcp.json`'a bakmak beş saniyeydi.

**Ve bu tam olarak memory taramasının kendi uyarısıydı** — *"bu havuzdaki sayılar kendi
içinde denetlenmemiş olabilir, ölçütler sağlam."* Uyarıyı ben yazdım, sonra ihlal ettim.

**PQA'nın ince notu korunacak:** yüklü ClickUp araçları `websitesi` prefiksiyle geliyor.
Yani *"tanım var ama çalışan örnek başka plugin'den"* diye **ayrı** bir gözlem
yapılabilir — ama gereksinimin yazdığı şey bu değildi.

---

## KARAR 9 (06:55) — Düzeltme kesildi, üretime geçiliyor (KULLANICI KARARI)

**Mert 06:54'te karar verdi:** *"ikinciyi yap, üretime geç."*

**Sunduğum iki yol:** (1) zinciri tam koştur — PAM düzeltir, PQA tekrar denetler, sonra
üretim; kalite yüksek ama n8n'de bu beş tur sürdü. (2) Üç iş değiştirici bulguyu
düzelt, kalan beşi işaretle, **hemen üret.**

**Gerekçe — Mert'in kendi kuralı:** *"Bir ürün oluşturun, sonra kaliteli hâle
getirirsiniz."* Gece boyunca **tek satır agent dosyası üretilmedi.** Elimizde 649 satır
gereksinim + 8 bulgulu denetim raporu var, ürün yok. Bu, 2026-08-08'de ölçülen arızanın
aynısı: her adım savunulabilir, hiçbiri ürün üretmez.

**Şimdi düzeltilenler — yalnız üçü:** B1 (ClickUp iddiası yanlış), B2 (eşik çelişkisi),
B3 (ölçüt iki modlu yazılacak).

**Bırakılanlar — B4, B5, B6, B7, B8.** Ayıran ölçüt: *eksik olan şey ürünü yanlış mı
yapıyor, yoksa eksik mi bırakıyor?* Beşi de belgeyi eksik bırakıyor, **üretimi yanlış
yapmıyor.** Kusurlu bir çıktı düzeltilebilir; olmayan bir çıktı düzeltilemez.

**Bir istisna işaretlendi:** B7(a) — QA body alıntısından *"TE senaryo"* düşürülmüştü ve
o paragrafın tezi *"TE'nin işi developer self-verify'ıyla örtüşüyor"* idi. Kaynak tezin
**aleyhine** konuşuyor. Bu yüzden **TE'yi birleştirme/kaldırma kararı bu tezle
alınmayacak** — TE dokuz rolde kalır, aksi ancak Mod B iş bölünmesinden çıkarsa olur.

**Neden bu istisna:** B7(a) diğer alıntı hatalarından farklı — o bir kırpma değil,
**tezi taşıyan kanıtın kırpılması.** Üretim sırasında rol kararı verilecekse yanlış
zemine basar.

---

## KARAR 10 (06:55) — Aşama 1 ve pilot rol TEK PAKETTE üretilecek

**Ne:** PAD'e verilen iş, ortak katmanı ve backend rolünü **birlikte** üretmek.

**Neden:** Gereksinimde üç aşama sıralıydı (ortak katman → pilot → kalan sekiz) ve
aşama 2'nin aşama 1 denetiminden geçmeden başlamayacağı yazılıydı. **Bu sıra artık
maliyet üretiyor** — ortak katman tek başına denetlenip beklerse bir tur daha eklenir.

**Ve teknik gerekçe daha güçlü: ortak katman tek başına sınanamaz.** Birleşik
`behavior` doğru mu, skill haritası çalışıyor mu — bunlar ancak **bir rolün içinde**
ölçülebilir. Aşama 1'i ayrı denetlemek *"dosya üretildi"* ölçütüne geri düşmek olurdu,
oysa kabul ölçütü *"sahada açıldı."*

**Risk kabul edildi:** ortak katmanda bir hata varsa pilot rolle birlikte düzeltilecek,
yani iki iş birden. Ama tek rol üzerinde — dokuz değil.
