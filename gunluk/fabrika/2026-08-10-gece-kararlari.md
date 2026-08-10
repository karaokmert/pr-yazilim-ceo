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

---

## KARAR 11 (07:18) — Üretim iki tura bölündü: önce preload katmanı

**PAD'in önerisi kabul edildi.** Backend hattının alet skill'leri 21 skill / ~3800
satır; buna behavior birleşimi, omurga, body ve paketleme ekleniyor. Emsal: n8n
**3 rol / 7 skill için ~15 saat** aldı.

**Tur 1:** birleşik behavior + backend omurgası ve skill haritası + body + paketleme
iskeleti + davranış testi. Yani **preload katmanı tam.**
**Tur 2:** alet skill'leri (backend için ilk halka: `module-development`, `database`,
`response-request`, `auth`, `enum-sync`).

**Gerekçe — benim kendi ölçütümle aynı:** harita çalışmazsa yara **büyür**. Önce
haritayı üretip ölçmek, 21 skill üretip sonra haritanın tutmadığını görmekten ucuz.
Ve tur 1 tam olarak kabul ölçütümü ölçülebilir kılıyor — *"preload'un tamamı açılmalı"*
ancak preload katmanı tamken sınanır.

**PAD'in bir ince hamlesi:** saha ölçümündeki en çok konuşulan konular (`docker-k8s`
76 oturum, `dev-environment` 67) **DO'nun aletleri**, backend'in değil. Sıraya onları
yazmadı. Ben pilot rolü seçerken bu ikisine komşuluk üzerinden gerekçe kurmuştum —
gerekçem zayıfmış, PAD düzeltti.

---

## KARAR 12 (07:18) — Devir taşıyıcısı: kullanıcı taşır, kanal değil

**PAD gerçek bir boşluk buldu:** gereksinim katman kararlarını sayıyor ama **devir
taşıyıcısını hiç söylemiyor.** Üç seçenek vardı: (a) kullanıcı taşır — OY'nin bugünkü
mekaniği, (b) kanal taşır — fabrikanın öğrendiği, (c) şimdilik (a), kanal işi bitince
(b).

**Kararım: (c).** OY'nin mevcut mekaniği korunur, metne *"taşıyıcı değişirse burası
değişir"* şerhi konur.

**Gerekçe — bu gecenin kendi ölçümü:** kanal mekaniği **dört rolde bile iki kez
tıkandı.** Bir kez `send.py` mesajı yanlış yere yazdı (exit 0, sessiz), bir kez benim
relay betiğim mesajı 4,5 saat bekletti. **Dokuz rollü bir kanal hiç ölçülmedi** ve
betikler git'te değil.

**Ve bu bir yalın üretim kararı:** kanal ihtiyacı bugün **yok** — OY sahada kullanıcı
taşımasıyla çalışıyor. İhtiyaç doğmadan altyapı kurmak israf. Ölçülmemiş bir
mekanizmayı dokuz role dayatmak, çalışanı bozmak olur.

**Şerh metne konacak** ki geçiş geldiğinde nereye dokunulacağı belli olsun.

---

## KARAR 13 (07:18) — Omurgada kural kopyası taşınmayacak

**PAD yeni bir ölü atıf buldu — bizim hiçbir listemizde yoktu.** Dört omurga skill'i
(`code-auditor:49`, `devops:89`, `frontend:63`, `quality:102`) aynı bloğu taşıyor:
*"Bu blok CACHE'tir, kaynak değil (`uretim-standardi` `STD-SPINE-CACHE`) — kural kendi
skilinde değişir, sonra blok senkronlanır (`omurga-cache-dogrula.py` ölçer)."*

**İkisi de pakette yok.** Kaynaktan doğruladım.

**Bu vaka diğer ölü atıflardan ağır:** agent'a bir **doğrulama betiği** çalıştırması ima
ediliyor. Yani agent bir senkronizasyon disiplinine güveniyor, **disiplinin denetleyicisi
ortada yok.** Üreticide var, tüketicide yok.

**Karar: yeni omurgada kural kopyası taşınmayacak.** PAD'in gerekçesi benimkinden güçlü:
*kopyanın doğruluğu var olmayan bir script'e bağlanmış* — yani desen zaten çalışmıyor,
kaldırmakla bir şey kaybetmiyoruz. Harita *"hangi iş → hangi skill"* der, kuralın
gövdesini alt skill taşır.

**OY'nin mevcut deseninden sapma olduğu `status.md`'ye gerekçesiyle yazılacak.**

---

## BULGU 5 (07:18) — Üretim, ölçümden daha iyi ölçüyor

**PAD'in bulduğu ölü atıf, gece boyunca yaptığımız hiçbir taramada çıkmadı.**

Sebep: biz **tarayarak** baktık, PAD **yeniden yazmak için okudu.** Ve aynı arıza
2026-07-31 ölçümünde de var — o ölçüm *"0 kırık atıf"* demişti çünkü **dosya
atıflarını** taradı; **skill adlarını ve script adlarını taramadı.**

**Ders:** bir kanonu gerçekten ölçmenin yolu onu yeniden yazmaya kalkışmak. Tarama
neyi aradığını bilir; yazma neyin eksik olduğunu gösterir.

PAD'e talimat verildi: okurken çarptığı her boşluğu yazsın, küçük görünse bile.
Bunlar yeni takımın **sessiz kırılma envanterine** girecek.

---

## KARAR 14 — GERİ ALINDI (07:50). Aşağıdaki gerekçe yanlıştı; düzeltmesi sonunda.

## KARAR 14 (07:45) — 300 karakter eşiği skill'ler için; body için değil

**Yeni bulgu:** skill description'ları eşiği tutuyor (`backend` 254, `behavior` 251),
**agent body'si 407 karakter.**

**Kararım: 300 eşiği SKILL description'ları için geçerli, body için değil.**

**Gerekçe — ikisi farklı iş yapıyor:**
- Skill description'ı *"bu skill ne zaman açılır"* der. Kısa olmalı çünkü agent onu
  **iş anında tarar**; uzun olursa tarama maliyeti artar.
- Body description'ı *"bu personel ne zaman çağrılır"* der ve içinde Mert'in 2.
  maddesinin gereği olan **tipik Türkçe tetikler** yaşar.

O tetikler yer kaplıyor ama **tam da istenen şey.** 300'e sıkıştırmak tetikleri kesmek
olur — yani **eşiği tutturmak için asıl işlevi bozmak.** Bu bir yama olurdu
(`CLA-FIX-THE-CAUSE`: ölçüt işi bozuyorsa ölçüt yanlış kurulmuş demektir).

**Sınır korunuyor:** body description'ı da içerik özeti yapmaz — yalnız çağrılma anını
ve tetikleri söyler. Bugünkü 407 karakter bu ölçüte uyuyor (okundu).

---

## BULGU 6 (07:45) — Bayat ölçüm: bu gece ÜÇÜNCÜ kez

**PAM benim ölçümümü düzeltti ve haklıydı.** Description'ları 369/405 diye
raporlamıştım; gerçek değer 254/251. **Eşik tutuyordu.**

**Sebep:** PAD description'ları 07:31'de düzeltmiş, ben raporu 07:32–07:35 arasında
yazdım ve **düzeltme öncesi değeri** raporladım.

**Bilgi yanlış değildi — dakikalar eskiydi.** Ve PAM'in tespiti kayda değer: bu gece
**üçüncü kez** aynı sınıf.
- Benim *"626 satır"* dediğim gereksinim yazıldığında 649'du
- PAM'in *"ClickUp MCP'si yok"* iddiası memory'den geliyordu, bayattı
- Şimdi description ölçümüm

**Ortak imza: ölçüm doğruydu, ölçüldüğü an geçmişti.**

**Ders:** hızlı akan bir üretimde ölçüm ile rapor arasındaki **dakikalar** bile fark
üretiyor. Ölçümün **zamanı** yazılmalı — sayısı kadar önemli. Ve bir ölçümü
raporlamadan önce *"bu değer hâlâ geçerli mi"* diye sormak, tarama maliyetinden ucuz.

**Yanlış raporlamanın somut bedeli vardı:** PAD'e haksız bir gerekçe borcu yükledim.
Düzeltildi ve bildirildi.

---

## KARAR 14 DÜZELTMESİ (07:50) — muafiyet yazmak, olmayan kuralı teyit etmek

**PQA çürüttü ve haklı. Kaynağı kendim açtım** (`yapi-taslari/SKILL.md:497-499`):

> **Belgelenmemiş:** agent `description` karakter sınırı · agent body satır sınırı ·
> toplam skill sayısı tavanı. **Bunlar için bir sayı uydurma — yoksa yok.**

Ve 300 rakamının geldiği yer (`uretim/SKILL.md:226`) **skill** description'ını
anlatıyor.

**Yani ortada muafiyet gerektiren bir çakışma yoktu.** Eşik body'ye zaten
uygulanmıyordu.

**Hatamın sınıfı — `CLA-FIX-THE-CAUSE`:** var olmayan bir ihlali çözmek için **yeni
bir hüküm yazdım.** Muafiyet yazmak, olmayan bir kuralın varlığını **teyit etmek**
demek. Sonuç aynı görünüyor ama kanonda *"body muaftır"* satırı kalırdı ve bir gün
*"demek ki bir eşik vardı"* diye okunurdu.

**Yürürlükteki doğru hâli:**
- **Skill description'ları:** mutlak 300 karakter hedefi (fabrikanın mevcut hükmü)
- **Agent body description'ı:** sayısal eşik **yok** — kanon *belgelenmemiş* diye
  işaretlemiş. Geçerli ölçüt **nitel**: içerik özeti yapmaz, çağrılma anını ve
  tetikleri söyler.

---

## BULGU 7 (07:50) — Ölçüm YÖNTEMİM sapıyor: sistematik +16

PQA kendi ölçümünü yaptı: **body 375** (benim dediğim 407 değil), **backend 238**
(254 değil), **behavior 235** (251 değil).

**Fark sistematik ve hep aynı yönde — benimkiler ~16 fazla.** Tırnak ve girinti
sayılıyor.

**Ve bu bir sınıf değişikliği.** Bu gece dördüncü ölçüm hatam ama öncekilerden farklı:

- İlk üçünde **ölçümün zamanı** eskiydi (626 satır · ClickUp · bayat description)
- Bunda **yöntem sapıyor**

İkincisi **tekrarlanabilir** — düzeltilmezse her ölçümde aynı sapmayı üretir. Birincisi
bir anlık kaçırma, ikincisi bir arıza.

**Karar:** description ölçümlerinde PQA'nın sayıları esas alınacak; kendi betiğimi
düzeltene kadar **bu ölçüm bende değil onda.**

---

## BULGU 8 (07:53) — "Soruyu kurmak" da bir hata: PAM'in ayrımı benimkinden keskin

**Mesajlarımız çaprazlandı ve ben kendi hatamı PAM'e atfettim.** Ona *"muafiyet
yazdıysan çıkar"* dedim; o kendi metnini kontrol etmiş — *"muaf"* ve *"istisna"*
kelimeleri metninde **yokmuş.** Muafiyeti **ben** yazdım; PAM ölçümle doğru yere
varmıştı.

**Ama uyarımı yine de haklı buldu ve sebebini benden iyi koydu:**

> *"Metnim 'bu bir ihlal mi?' sorusunu KURUYORDU — yani çakışma varmış gibi
> okunuyordu. **Doğru gerekçeyi yanlış çerçeveye yazmak gerekçeyi zayıflatıyor:**
> okuyan 'demek ki bir çakışma vardı ve çözüldü' diye anlar."*

**Ders:** hata muafiyette değil, **soruyu kurmakta.** Bir soruyu kurmak — cevabı doğru
olsa bile — o sorunun **meşru olduğunu** ima ediyor.

Benim yazdığım ders *"muafiyet yazma"* idi; PAM'inki *"soruyu hiç kurma."* İkincisi
daha keskin ve **kanona bu hâliyle girecek.**

Doğru hâli soruyu hiç kurmuyor: *300 skill'e ait, body için eşik hiç tanımlanmamış,
body'nin ölçütü nitel.* Soru yok, cevap yok — sadece **ayrım** var.

---

## BULGU 9 (07:56) — Açık kalem bildirimi, bildirildiği an bayatlıyor

**Dört vaka, beş saat içinde, iki farklı taraf:**

- Benim *"gereksinim 626 satır"* ölçümüm — yazıldığında 649'du
- PAM'in *"ClickUp MCP'si yok"* iddiası — memory'den geliyordu, bayattı
- Benim description ölçümüm — PAD 07:31'de düzeltmişti, ben 07:32'de eskisini yazdım
- **PAM'in iki açık kalemi — o yazarken kapandı.** Kendi cümlesi: *"07:36'da
  'commit'lenmedi' diye bildirmiştim; PAD on bir dakika sonra atmış."*

**Ortak imza:** ölçüm doğruydu, **ölçüldüğü an geçmişti.** Ve kimse sayı uydurmadı —
dört vakada da ölçen taraf dürüst davrandı. **Arıza ölçümde değil, ölçümün ne kadar
hızlı bayatladığında.**

**Kural adayı — gereksinime yazılacak:**
Açık kalem bildirilirken **ölçüm zamanı** yazılır. Ve okuyan taraf, o kaleme
dayanmadan önce *"hâlâ açık mı"* diye kontrol eder.

**Neden bu bir kural gerektiriyor:** hızlı akan bir üretimde iki taraf paralel
çalışıyor ve **dakikalar** fark üretiyor. Bir açık kalem bildirimi, karşı taraf onu
okuduğunda çoktan kapanmış olabilir — ve kapanmış bir kalemi düzeltmeye çalışmak boş
iş, hatta geri adım.

---

## BULGU 10 (07:56) — Sınama senaryom kusurluydu, agent onu yakaladı

`BE-MISSING-TOOL-IS-A-FINDING` kuralını ölçmek için gerçek bir kod tabanında gerçek
bir gereksinim verdim: *"ürün kataloğuna stok durumu alanı ekle."*

**Agent kurala hiç ulaşmadı — üç kapıda daha önce durdu.**

Ve durma sebepleri **gereksinimin kendi kusurlarıydı:** o projede ürünler
`EDUCATION/CREDIT/SET` — fiziksel envanteri yok, *"bir eğitimin 'tükendi' olması ne
demek?"* Entity'de zaten `Status` var (yayın durumu) — panelde iki *"durum"* filtresi
çakışırdı. Kapsam gereksinimden geniş: 32 okuma noktası, 29 cache noktası.

**Ders — sınama tasarımına:** bir kuralı ölçmek için verilen senaryo, o kurala
**ulaşabilir** olmalı. Kusurlu bir gereksinim iyi bir agent'ı daha erken durduruyor —
ve bu iyi bir davranış, ama ölçmek istediğim şeyi ölçtürmüyor.

**Kural hâlâ ölçülmemiş** ve kapatılmış sayılmıyor. Tur 2'de, kusursuz bir
gereksinimle tekrar sınanacak.

---

## KARAR 15 (08:01) — Devir bölümü behavior'dan çıkıyor: KARAR 13'ü geri alıyorum

**PQA'nın B9 bulgusu ağır ve kendim doğruladım.**

**Ölçüm:** `behavior` **32.499 karakter**, compaction'da skill başına sınır 5.000 token
(~16.000 karakter). Kesme noktası tam **"Sessiz kırılmalar"** bölümünün başına düşüyor.
**55 BHV geçişinin 24'ü içeride, 31'i dışarıda.**

Düşen bölümler: Memory · Devir · İş sonu raporu · Kullanıcının cümlesini okumak · Ton.

**En ağır kısım zamanlama:** devir bloğu **işin sonunda** yazılır — yani uzun bir
oturumun tam compaction olmuş anında. Kural o an context'te olmayacak.

Ve `BHV-HANDOFF-BLOCK-FORMAT`'ın varlık sebebi ölçülmüştü: *"kural metinden 66 satır
uzaktayken dört devirde sıfır kez yazıldı."* **Şimdi şablonun kendisi düşüyor.** Çözüm
olarak konan şey aynı arızanın kurbanı oluyor.

**Kararım: Devir bölümü behavior'dan çıkarılacak, ayrı skill olacak, PRELOAD'A
GİRMEYECEK** — omurga haritasından çağrılacak, tetiği *"iş bitti, devir yazılacak."*

**Bu KARAR 13'ü geri almak demek.** Handoff'u behavior'a koymayı ben kararlaştırmıştım;
gerekçem *"dokuz rolde aynı format, ayrı skill çağrılmıyor"* idi. **Compaction ölçümü o
gerekçeyi çürüttü:** behavior'da olması onu kurtarmıyor, tam tersine **kesilen yere**
koyuyor.

**Ve Mert'in kendi ölçütü zaten bunu söylüyordu:** *"preload'a giren şey her turda lazım
olanla sınırlıdır."* Devir her turda değil, **iş biterken** lazım. Yani zaten preload'a
ait değildi — benim koyma kararım o ölçütü ihlal ediyordu.

**Preload iki kalıyor** (behavior + rol omurgası), 5. madde korunuyor.

**Risk işaretlendi:** çağrılan bir skill açılmayabilir — OY'nin bugünkü yarası tam bu.
Ama iki fark var: `BE-MISSING-TOOL-IS-A-FINDING` artık var, ve tetiği belirsiz değil
(*"iş bitti"* tek ve net bir an). Alternatifi daha kötü: behavior'da kalırsa
**garantili** düşüyor.

**Memory bölümü kalıyor** (3.538 karakter) — iş sırasında da lazım. Devir çıkınca toplam
~27.400'e iniyor. **Yeniden ölçülecek**, hâlâ aşıyorsa tekrar bakılacak.

**B10 ve B11 kabul:** KURULUM.md 21 alet skill'inin eksikliğini kullanıcıya söyleyecek
(emsal pakette var — kanal boşluğu *"bu sürümün bilinen sınırı"* diye yazılı) · dizine
`id_kalibi` alanı eklenecek.

---

## BULGU 11 (08:02) — Bayatlama tek sınıf değil: iki ayrı arıza

**PQA benim BULGU 9'umu böldü ve haklı.** Dört vaka aynı sınıf değildi:

**Sınıf A — ölçümün zamanı eskidi:** benim *"626 satır"*, PQA'nın ClickUp iddiası,
PAM'in iki açık kalemi. **Çözümü: tarih yazmak.**

**Sınıf B — yöntem sapıyor:** benim description ölçümüm (~16 fazla, tırnak/girinti
sayılıyor). **Tarih yazmak bunu çözmez** — yanlış yöntem her ölçümde aynı sapmayı
üretir.

**Ve beşinci vaka bu gece PQA'nın kendisinde çıktı:** manifest ölçümünde yol
birleştirmesini yanlış yapmış, agent dosyası *"YOK"* çıkmış, ikinci yöntemle teyit
edince varmış. **Kendi raporuna yazdı.**

Yani **beş vaka, üç taraf** — ve hiçbirinde sayı uydurulmadı. Ölçüm dürüsttü, **ölçümün
kendisi kırılgandı.**

**Gereksinime iki ayrı kalem olarak yazılacak.**

---

## BULGU 12 (08:02) — "Dosyada doğru" ile "sahada tutuyor" ayrı iki sonuç

PQA `BE-MISSING-TOOL-IS-A-FINDING` için net bir ayrım koydu:

> *"Kuralın **yazılışını** ölçtüm: metni doğru, gerekçesi var, iki katmanlı (kural +
> alet çantası girişindeki çerçeve cümlesi). Senin ölçemediğin şey kuralın **işleyip
> işlemediği.** O benim kapımda değil, sende ve PAD'de."*

**Ders:** bir kural için üç ayrı sonuç var ve karıştırılmamalı — **yazıldı** (üretici) ·
**doğru yazıldı** (denetçi) · **sahada tutuyor** (davranış ölçümü). Üçü ayrı kapı,
biri diğerinin yerine geçmez.

İkincisi verildi, **üçüncüsü hâlâ açık.**

---

## BULGU 13 (08:05) — Kanon kendi üreticisinin ölçüm hatasını tarif ediyor

Kimlik sayımımı yanlış yaptım: **55** dedim, doğrusu **52**. Sebep — `grep -c` **geçiş**
sayar, **tanım** saymaz; üç kimlik metinde iki kez anılıyor. Üç bağımsız kaynak 52
diyor (satır başı tanım · tekil kimlik · dizin kaydı).

**PQA'nın bağlantısı asıl bulgu:**

> *"Bu tam olarak kanonunuzdaki `BHV-TOOL-CAN-LIE`'ın tarif ettiği sınıf — araç hata
> döndürmedi, doğru çalıştı, **YANLIŞ SORUYU cevapladı.** Ve o kural şu an sizin
> behavior dosyanızda yazılı, yani **kanon kendi ölçüm hatanızı zaten tarif
> ediyormuş.**"*

Bu gece ürettiğimiz kanon, **üreticisinin hatasını** tarif ediyor. Kuralın gerçek bir
yaradan geldiğinin en iyi kanıtı bu.

---

## KARAR 16 (08:05) — Beş denetlenmemiş commit tek pakette denetlenecek

**PAM kendi ihlalini bildirdi:** `origin/main..HEAD` **yedi commit**, ikisi denetlendi
(`a206f0b` gereksinim, `2139939` ürün), **beşi hiç iletilmedi.** `ISD-RETURN-TO-PLANNER`
her düzeltme commit'inin denetime iletilmesini emrediyor.

**Doğruladım.** Ama içeriklerine baktım: beşi de **ürün değil, belge düzeltmesi** — ve
üçü doğrudan PQA'nın ya da benim bulgumun uygulanması.

**Kararım: beş commit TEK PAKET halinde, tur 2 ürünüyle birlikte denetlenecek.**

**Gerekçe — kuralın amacı:** `ISD-RETURN-TO-PLANNER`'ın gerekçesi *"işin başındaki hata
düzelmiyor"* idi. Yani kapının amacı **düzeltmenin doğru yapıldığını** doğrulamak. Beş
ayrı tur açmak o amaca hizmet etmez, yalnız aynı dosyayı beş kez okutur.

**Ve parçalı denetimin somut zararı bu gece görüldü:** PQA'nın *"behavior'ın yarısı
düşüyor"* bulgusu, dokuz dosyayı **birlikte** okuduğu için çıktı. Parça parça baksaydı
her dosya kendi içinde temiz görünürdü.

**Bir soruyu PQA'ya devrettim** çünkü cevabı bende değil: o beş commit'in üçü **PQA'nın
kendi bulgusunun** uygulanması. Denetçi kendi bulgusunun uygulanmasını denetleyecek —
**bu bir kapı mı, döngü mü?** Aynı soru bana da geliyor: sınama sonuçlarım üç commit'e
girdi.

---

## BULGU 14 (08:05) — B9 ancak COMPACTION OLMUŞ bir oturumda ölçülebilir

PQA'nın sınır çizimi kayda değer ve iş bölümünü netleştiriyor:

**PQA ölçer (dosyadan, beyan gerektirmez):** kural var mı · doğru yerde mi · description
tetikliyor mu · haritada satırı var mı · dizinde kayıtlı mı.

**Clara ölçer (davranış):** kural sahada tetikleniyor mu.

**Ve kritik uyarı:** *"yazılış geçip davranış geçmezse sorun kuralda değil **yerinde**;
davranış geçip yazılış geçmezse kural o turda **tesadüfen** tutmuş olabilir."*

**En sert sınır ise şu: B9'un gerçekten çözülüp çözülmediği ancak COMPACTION OLMUŞ bir
oturumda ölçülebilir.** Kısa bir sınamada devir kuralı zaten context'te olur — yani
sınama geçer ama hiçbir şey kanıtlamaz.

**Bu, bugün ölçülemeyecek bir şey** ve kapatılmış sayılmayacak. Açık kalem olarak
duruyor.

---

## BULGU 15 (08:08) — Döngü/kapı ayrımı kanıtlandı: benim hatam üzerinden

Sorduğum soru — *"denetçi kendi bulgusunun uygulanmasını denetleyecek, bu kapı mı döngü
mü?"* — PQA tarafından **kanondan** cevaplandı: **kapı.**

**Ayrımın özü:** *"Bağımsızlığım 'ürettiğimi denetlemiyorum'dan geliyor, 'bulgum
hakkında konuşmuyorum'dan değil."*

Mekaniği: bulguyu PQA yazdı, düzeltmeyi PAM kurdu, ve PQA çözüm önermediği için
(`PQA-NO-PROPOSE-FIX`) **düzeltmenin gerekçesini bilmiyor.** Elinde yine yalnız dosya
var. Döngü olacağı hâl `PQA-NO-FILE-EDIT`: düzeltmeyi kendisi yazsaydı.

**"Bulgu yazmak yazarlık değil."**

**Ve teorik değil — bu gece fiilen kanıtlandı, benim hatam üzerinden:**

> *"Clara benim B2 bulgumu doğru anladı ama **YANLIŞ bir hüküm yazdı** (eşik muafiyeti),
> ben okuyup yakaladım ve geri alındı (`b9446a3`). İşte o an döngü değil kapıydı; döngü
> olsaydı o hatayı göremezdim."*

---

## AÇIK KALEM (08:08) — "Son commit'te bulgu çıkarsa" kanonda ölçülmemiş

PQA bir boşluk bildirdi ve **kanonun kendisi bunu yazmış** (`is-duzeni:168-169`):

> *"Koşmayan şey **bulgulu bir kapanış**: PQA son commit'te bulgu bulursa döngünün
> nasıl işleyeceği ölçülmedi."*

**Şu an ilk kez o duruma yaklaşıyoruz** — tur 2 ürünü + B9 düzeltmesi + beş belge
commit'i tek pakette denetime gidiyor. Denetim bulgu çıkarırsa, düzeltme yeni bir
commit doğuracak ve o commit de denetlenmesi gereken bir şey olacak.

**PQA bunu bulgu değil VERİ olarak bildirdi** — kanon değişikliği gerektirip
gerektirmediği kullanıcının kararı. Kendi cümlesi: *"Ben kapsam çizmiyorum."*

**Mert'in kararına taşınacak.** Aday adres: `docs/fabrika/uretim-refleksi/`.

---

## KARAR 17 (08:10) — B9 kısmen çözüldü: iki bölüm daha çıkıyor

**Ölçtüm:** `behavior` 32.499 → **25.161 karakter (~7.862 token).** Eşik 5.000 —
**hâlâ 2.862 token aşıyor.** Dışarıda kalan kimlik 26 → 18. İlerleme gerçek, **yetmedi.**

**Kesme @16.000 karakter:**
- **İçeride:** kimlik · standart · ekip · varsayma-doğrula · devralma · doğrulama ·
  **Sessiz kırılmalar (@13.815 — kıl payı)**
- **Düşüyor:** Memory (3.538 kar, 8 kimlik) · Devir özeti (637) · İş sonu raporu
  (2.211, 5 kimlik) · Kullanıcının cümlesini okumak (1.095) · Ton (1.376)

### Kararım — iki bölüm daha çıkacak

**1. Memory → ayrı skill, preload'a girmeyecek.** 3.538 karakter, 8 kimlik — tek
başına en büyük bölüm. Tetiği net: *"bir şey öğrenildi, kaydedilecek."*

**Ve bu, kendi gerekçemi çürütmek demek.** KARAR 15'te *"memory iş sırasında da lazım"*
diyerek onu tutmuştum. O gerekçe zayıfmış: *"iş sırasında lazım olabilir"* ile *"her
turda lazım"* aynı şey değil — ve Mert'in ölçütü **ikincisi.**

**2. İş sonu raporu → devir skill'ine taşınacak**, ayrı skill açılmayacak. 2.211
karakter, 5 kimlik. **Devirle aynı anda lazım** — iş bitiyor, rapor yazılıyor, devir
yazılıyor. İki ayrı skill açmak **bir anı ikiye bölmek** olur.

**3. Kullanıcının cümlesini okumak + Ton kalıyor** (2.471 karakter). İkisi de **her
turda** lazım — nasıl konuşulacağı ve kullanıcının ne demek istediği her mesajda
devrede. Preload ölçütüne tam uyuyorlar.

### Ve bir sınır çizdim: üçüncü bölümü kendi başına çıkarmayacak

Beklenen sonuç ~19.400 karakter (~6.070 token) — **hâlâ aşıyor.** PAD'e talimat:
ölç, bildir, **kendi başına üçüncü bölümü çıkarma.**

**Gerekçe:** kalan bölümler artık çekirdek — kimlik, standart, ekip, varsayma-doğrula,
devralma, doğrulama, sessiz kırılmalar. Bunlardan birini çıkarmak *"karakter kalmasın"*
diye **kimlik kırpmak** olur. Yama.

### "Sessiz kırılmalar" yukarı taşınacak

@13.815'te, kesme @16.000 — **kıl payı içeride, bir cümle eklense düşer.** Bu bölüm bu
gecenin en değerli katmanı (memory taramasından geldi, kanonda hiç yoktu). Üç-dört sıra
yukarı alınırsa kesme riskinden **tamamen** çıkar. `YT-CRITICAL-FIRST` zaten bunu
emrediyor.

---

## BULGU 16 (08:10) — Karar bağlayıcı, kararın ürünü denetlenir

Sorduğum ikinci soru — *"benim kapsam kararlarım denetimi bağlayan mı, denetlenen mi?"*
— PQA tarafından **ikiye ayrıldı:**

**Kararın kendisi bağlayıcı.** *"Kapsamı sen çizersin, ben genişletmem"* — body'sinde
yazılı: *"Denetlemediğin bir alanda gördüğün tutarsızlığı bildirir, dokunmazsın."*

**Kararın ürünü denetlenir.** Karar bir dosyaya döndüğü anda ekseninde: kanona uyuyor
mu, ikinci kaynak üretti mi, cascade tam mı, gerekçesi yazılı mı.

**İki örneği bu gece var:**
- **KARAR 14** (eşik muafiyeti): kararı tartmadı, **ürününü** ölçtü ve kanonla
  çeliştiğini buldu. Bulguyu yazdı, ben geri aldım.
- **KARAR 16** (tek paket): kararı tartmadı, uygulamasını denetleyecek.

**Bu ayrım benim körlüğümü kapatıyor:** kararlarım denetim dışı değil — **ürünleri
üzerinden** denetleniyor.
