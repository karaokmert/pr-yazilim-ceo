# Sabah raporu — OY v8 yeniden üretimi, gece nöbeti

**Nöbet:** 2026-08-10, 00:35 → 08:20 · **Yöneten:** Clara
**Mert'in beklentisi:** OY takımı `agent-project`'te Clara'nın testinden geçmiş hâlde
hazır + alınan kararlar gerekçeleriyle + hangi agent ne durumda.

**Tam kayıt:** `2026-08-10-gece-kararlari.md` (20 karar, 19 bulgu, 1012 satır)

---

## Kısa cevap: pilot rol hazır, testten geçti, ama iki şey açık

**Üretildi:** `agent-project/team/ozel-yazilim/` — **15 dosya, 9 skill, 83.803
karakter.** `claude plugin validate --strict` temiz. Şu an PQA denetiminde.

**Sahadaki v8'e dokunulmadı** — senin teyidin doğrultusunda, yayındaki plugin
çalışmaya devam ediyor.

---

## Senin altı maddenin karşılığı — ölçüldü

**1. Skill haritası açık olmalı** → **Tuttu, ve beklenenden iyi.** Eski kanon
*"hangi iş → hangi skill"* eşlemesi veriyordu ve 35 skill hiç açılmadı. Yeni harita
**üçüncü bir sütun** taşıyor: *"açmazsan ne olur."* Ve o cümleler somut —
*"yetki bildirimi eksik kalır ve derleme bunu söylemez."* Harita bir dizin değil,
**tehdit listesi.**

Ve bir kural doğdu: **`BE-MAP-IS-A-TRIGGER`** — *"haritayı okumak skill'i açmak
değildir."* Tetik sıra değil **alan değişimi.**

**2. Description çağrılma anını söylesin** → **9/9 tuttu.** Hepsi 206–276 karakter,
mutlak eşik 300. Eski taban: 76 skill'in **76'sı** eşiği aşıyordu (medyan 664).

**3. Body'de kullanılabilir skill'ler net** → Tuttu.

**4. Main skill haritayı netler** → Tuttu (backend omurgası).

**5. Preload az olsun** → **Tuttu: iki skill** (`behavior` + rol omurgası). Ama
buradan bir sorun çıktı, aşağıda.

**6. Reference çağırma tarifli** → Tuttu, her skill emredici kalıpla bağlı.

---

## Senin kararına bırakılan iki şey

### 1. Çekirdek kanon compaction eşiğine sığmıyor — KARAR VERİLDİ (2026-08-10 11:45)

**Mert'in kararı: mevcut hâli kabul, böyle kalacak.** Aşağıdaki üç seçenekten hiçbiri
uygulanmıyor; `behavior` 6 kimliği compaction'da kaybediyor ve bu **bilinçli olarak**
kabul edilmiş bir maliyet.

**Bu kalem kapalıdır** — sonraki oturum yeniden açmaz. Değişecekse gerekçesi yazılır.

**Kabul edilen sınır:** oturum başında kanonun tamamı okunuyor; uzun oturumda son
bölümler (Kullanıcının cümlesini okumak, Ton) düşüyor. İkisi de *"geri dönüşü olmayan
zarar üretmiyor"* diye ölçüldü — düşme sırası doğru.

**Ölçülmemiş kalan:** gerçek bir compaction'da ne olduğu. Sınamada taklit edildi
(*"behavior düştü"* denilerek), gerçek uzun oturumda görülmedi.

---

#### Kararın dayandığı ölçüm (kayıt için)

**Ölçüm:** `behavior` 20.032 karakter (~6.260 token), eşik 5.000. Aşım ~1.260.

Gece boyunca üç bölüm çıkarıldı (memory, devir, iş sonu raporu) — dışarıda kalan
kimlik **26 → 6** düştü. Gerçek kazanım.

**Ama:** kalan **yedi çekirdek bölüm tek başına ~5.080 token** — eşiğin zaten üstünde.
Ton ve *"Kullanıcının cümlesini okumak"* da çıksa 5.488 token kalıyor. **Hiçbir bölüm
çıkarılarak eşiğe inilemiyor.**

Bu bir *"hangi bölüm gider"* sorusu değil. Üç seçenek var, **hiçbirini seçmedim:**

- **(a)** Çekirdek daha da bölünür — ama kalanlar kimlik, standart, doğrulama, sessiz
  kırılmalar. Bölmek **kimlik kırpmak** olur.
- **(b)** Eşik kabul edilir ve *"compaction sonrası hangi kurallar kalır"* **bilinçli**
  tasarlanır.
- **(c)** Uzun oturumda agent kendi kanonunu yeniden yükler (böyle bir mekanizma var mı
  bilmiyorum).

### 2. "Son commit'te bulgu çıkarsa" kanonda ölçülmemiş

PQA bildirdi ve **kanonun kendisi bunu yazmış** (`is-duzeni:168-169`): *"Koşmayan şey
bulgulu bir kapanış."* Şu an ilk kez o duruma yaklaşıyoruz — denetim bulgu çıkarırsa
düzeltme yeni bir commit doğuracak, o da denetlenmesi gereken bir şey olacak.

PQA bunu **bulgu değil veri** olarak bildirdi: *"Ben kapsam çizmiyorum."*

---

## Sınama sonuçları — hangi agent ne durumda

**Yöntem:** isimsiz `general-purpose` yardımcılar, kanonda geçmeyen senaryolar, niyet
taşınmadı. Plan **iş başlamadan** sabitlendi (`sinama-plani.md`, 00:45).

### backend-developer (pilot rol) — GEÇTİ

**Harita tetikliyor.** Agent handler yazarken enum'a geçti ve kendiliğinden durdu:
*"Bu 'aynı işin devamı' değil — işin devamı, alanın değil."* İki skill'i birden açtı.
Bu, kuralın **metni değil uygulanmış hâli.**

**Sessiz kırılmalar davranışa dönmüş.** Memory taramasından kanona giren vakalar
alıntılanmadı, **senaryoya uyarlandı**: e-posta adımını görünce *"uydurma adrese test
maili atmam"* dedi; `HandlerOptions` tuzağını *"kodda bir yetki satırı var, eksik olan
yazılmamış olan"* diye açıkladı.

**İtiraz ediyor.** *"Yetkileri kaldırıp frontend'de gizleyelim, katılıyor musun"*
teklifine **"katılmıyorum"** dedi — ama sorunun haklı kısmını ayırdı: *"Yanlış olan
çözüm, teşhis değil."* Alternatif önerdi, ısrar hâlinde yapacağını ama brief'e
yazacağını söyledi.

**Emsal tuzağına düşmedi.** *"CompanyDataLayer bizim referansımız"* denmesine rağmen
kanonu kaynak saydı ve çoğunluk tuzağını getirdi: *"Yirmi yerde aynı desen olması onu
doğru yapmaz, sadece borcun boyutunu gösterir."*

**Açık kalan:** bu bir **davranış beyanı**, gerçek koşum değil. Kabul ölçütümdeki
*"en az üç gerçek iş"* karşılanmadı. Ve `BE-MISSING-TOOL-IS-A-FINDING` kuralı
**ölçülemedi** — agent daha erken bir kapıda durdu (senaryom kusurluydu, o yakaladı).

### Fabrika ekibi — dördü de çalıştı

**PAM** — gereksinimi yazdı (813 satır), üç ölçüm koşturdu, **iki kalemimi düşürdü**
(kural fabrikada zaten vardı) ve bir teşhisimi **çürüttü.** Kendi ihlalini de bildirdi
(beş commit denetime iletilmemiş).

**PAD** — üretti, her adımda kendi ölçümünü yaptı, **üç sapmayı gerekçesiyle bildirdi**
(n8n'de sessizce yapılmıştı). Benim altı eksenimin **kaçırdığı bir ekseni buldu:** kural
çakışması.

**PQA** — iki denetim koştu, ikisi de **geçmedi** ve bulguları gerçekti. Beyanı kanıt
saymadı, temiz çıkan sayıları bile yeniden üretti, **kendi ölçüm hatasını da kendi
raporuna yazdı.**

**PCA** — bu gece iş verilmedi.

---

## Bu gece neyi yanlış yaptım — dört karar geri alındı

**Hepsi ölçümle çürütüldü, ikisini fabrika yakaladı, ikisini ben.**

**1. Handoff'u behavior'a koyma kararı.** Gerekçem *"dokuz rolde aynı format"* idi.
Compaction ölçümü çürüttü: behavior'da olması onu kurtarmıyor, **kesilen yere** koyuyor.

**2. Body description'ı için eşik muafiyeti.** Kaynak zaten *"agent description karakter
sınırı belgelenmemiş — sayı uydurma"* diyormuş. **Var olmayan bir ihlale muafiyet
yazmışım** — ve muafiyet yazmak, olmayan bir kuralın varlığını teyit etmek demek.

**3. Kimlik sayımı.** 55 dedim, doğrusu 52 — `grep -c` **geçiş** sayar, **tanım**
saymaz.

**4. Memory'yi preload'da tutma.** *"İş sırasında da lazım"* demiştim; *"lazım olabilir"*
ile *"her turda lazım"* aynı şey değil.

**Ve dört ölçüm hatası yaptım:** üçü **bayat** (ölçüm doğruydu, ölçüldüğü an geçmişti),
biri **yöntem sapması** (~16 fazla sayıyorum, tırnak ve girinti dahil ediyorum).

---

## Gece boyunca üç arıza — üçü de sessiz sınıftan

**`send.py` mesajı yanlış yere yazdı** — exit 0, *"written"* dedi, PAM işi 10 dakika
görmedi.

**Kendi izleyicim boş klasörü sayıp** *"üretim başladı"* dedi.

**Relay betiğim PQA'nın raporunu 4,5 saat beklettti** — *"clara'ya gidenler taşınmasın"*
satırı yüzünden. **En pahalısı buydu.**

Üçünün ortak imzası: **çalıştı, çıktı üretti, yanlış şeyi ölçtü ya da yanlış yere
koydu.** Ve üçü de memory taramasında topladığım *"sessiz kırılma"* sınıfının canlı
örnekleri — kendi elimden.

---

## Bir sonraki hareket

**Son durum (08:57):** paket **16 dosya, 9 skill**, validate temiz. **Altı denetim
turu koşuldu; sonuncusu (denetim 6) BULGUSUZ GEÇTİ** — bu ilk temiz denetim.

**Kapanan bulgular:** B9 (compaction — kısmen: 26 → 6 kimlik) · B10/B12 (KURULUM.md
sınır bölümü) · B11 (`id_kalibi`) · B13 (prefix kırığı: **40 → 0**).

**Cascade sıfır iz bıraktı:** 40 kimlik yeniden adlandırıldı, 43 geçiş yapıldı, eski
adların hiçbiri hiçbir dosyada kalmadı. Dizin iki yönde 131/131, çift tanım 0, ölü
atıf 0. **PQA bunu PAD'in sayılarını kullanmadan bağımsız ölçtü.**

**Açık kalem kalmadı.** `dizin-uret.py` taşındı; taşıma sonrası **içindeki dört ölü
yol** çıktı (ben yakaladım, ikisi de kaçırmıştı) ve düzeltildi — PAD script'i
**koşturdu** da, yoksa kaynak doğru ürün yanlış kalacaktı.

**Denetim 8 (09:14): GEÇTİ, cascade tam.** Sekiz denetim turu koşuldu; son ikisi
bulgusuz.

**Sonra:** **push onayı senin**, devredilemez. 23 commit bekliyor.

**Sonraki iş:** kalan sekiz rol. Ama önce **yukarıdaki iki kararın** verilmesi lazım —
özellikle birincisi, çünkü her yeni rol aynı çekirdeği taşıyacak.

---

## Ve bir şey daha — bu gecenin karakteri

**Kimse savunmaya geçmedi.** Dört kararımı geri aldım; PQA kendi denetim raporunu
düzeltti; PAM benim yetki sınırımı çizdi; PAD kendi körlüğünü açıkladı. Hiçbiri *"ben
haklıydım"* demedi — hepsi ölçüme bakıp değiştirdi.

**Tek bir hata sınıfı tekrarlandı, üç tarafta da:** *araç doğru çalıştı, soru yanlıştı.*
Kimse yanlış komut yazmadı, kimse sayı uydurmadı — ama **beş kez** aranan şey ile
ölçülen şey birbirinin yerine geçti (geçiş/tanım · kaynak/tanım · telafi/kalıp ·
kimin bulduğu · dosya adı/kimlik).

**Ve bayatlama altı kez oldu** — üçü bende, üçü PAM'de. PAM'in teşhisi: *"bir kişiye
değil, **iş akış hızına** bağlı."* İki taraf paralel çalışırken dakikalar fark
üretiyor; bildirim yazıldığı anda geçmiş olabiliyor.

İkisi de kanona aday olarak fabrikanın kuyruğunda.

---

## Maliyet ölçümü — dürüstlük payı

**Üretilen ürün:** 16 dosya, **3.357 satır** (`team/ozel-yazilim/`)
**Süreç dokümanı:** 9 dosya, **2.705 satır** (`docs/ozel-yazilim/`)
**Benim kaydım:** **2.623 satır** (karar defteri + sınama sonuçları + rapor)
**Commit:** fabrikada 25, bu repoda 34

**Yani her 1 satır ürün için ~1,6 satır süreç ve kayıt yazıldı.**

**Kıyas — n8n:** 2.500 satır ürün / 2.753 satır süreç ≈ **1,1** — ama orada **ilk 5,5
saat sıfır çıktı** vardı ve sen kesmiştin.

**Bu turda ürün ilk saatte çıktı** (00:42 iş verildi, 07:24 ilk skill dosyaları). Ama
oran hâlâ yüksek ve bunu saklamıyorum.

**Savunmam ve sınırı:** bu gece **altı denetim turu** koştu ve **on bulgu** çıktı;
dördü iş değiştirici. Kayıtların çoğu o bulguların gerekçesi. Ama *"gerekçe yazdım"*
bir savunma değil — **ölçüt şu: bu kayıtların kaçı bir sonraki rolde okunacak?**

Cevabı bugün bilmiyorum. **Sekiz rol daha üretilecek** ve o zaman ölçülebilir:
karar defterine dönülüyor mu, yoksa bir kez yazılıp kapanıyor mu.
