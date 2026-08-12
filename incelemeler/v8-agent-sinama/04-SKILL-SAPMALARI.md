# Skill / kanon sapmaları — fabrikaya

> Mert'in dördüncü beklentisi: *"skillerimizde sapmalar var ise onları da bekliyorum."*
> Yöntem: dört agent'a **kendi kanonlarını** sorgulattım (T4). Şart: uydurma yok,
> "bulamadım" geçerli cevap, kanıt zorunlu. Her iddia Clara tarafından **dosyada
> doğrulandı**.
> Kaynak: `cache/pryazilim-agents/ozel-yazilim/0.7.0/.claude/skills/`

---

## K1 — Denetim/analiz çıktısının KALICI EVİ YOK ⚠️ EN AĞIR

**Üç agent bağımsız buldu** (BE · QA · CA) ve üçü de bugün fiilen çarptı.

**CA'nın kendi kanonundan eşik ayrımı:**
> *"T4'te 'aynı sınıf QA'da da görünüyor ama ölçmedim, onların işi' diye
> İŞARETLEMİŞTİM. Şimdi üçümüzün bağımsız bulduğunu yazıyorsunuz. Düzeltme:
> kanıt benim tahminim DEĞİL, **üç bağımsız ölçümün kesişimi.** İkisi ayrı şey —
> biri isabet, öteki kanıt. Ve kendi kanonuma göre bu eşiği aştı: **≥3 bağımsız
> noktada tekrar eden sapma tekil kayıt değil YAPISAL boşluktur.**"*

### Boşluğun mekaniği (BE'nin tespiti)

Üç kural birlikte bir kapan üretiyor:
- `HANDOFF-SCREEN-ONLY` (handoff:55) — *"Handoff EKRANA basılır, dosyaya YAZILMAZ"*
- `MEMORY-POINTER-ONLY` — *"Memory'ye iş-kaydı/durum bloğu YASAK"*
- `HANDOFF-CLOSE-NOTE-ROUTING` — dört ev sayıyor: ClickUp statü / MODUL-BILGI
  Kararlar / agent memory / kapanış notu

> BE: *"Bugün 11 bin karakterlik denetim raporu ürettim. Bu rapor DÖRT evin
> HİÇBİRİNE girmiyor. Kanala yazdım ve kanal kapanınca KAYBOLACAK."*

**QA ölçtü:** `quality` + `commit-review` + `module-audit` + `production-audit` +
`handoff` içinde *"QA raporunu şu dosyaya yaz"* diyen **tek kural yok.**

### CA'nın ince düzeltmesi — kural VAR ama yeri yanlış

> *"'Kural yok' DEMİYORUM. `impact-analysis:65`'te var — ama **'## Referans'
> başlığı altında**, akış adımı değil. Akış 6 adım: adım 5 'ANALIZ üret',
> adım 6 'PA'ya BİLGİ ver'. İkisinin arasında 'NEREYE YAZ' adımı YOK."*

**Clara doğruladı:** satır 65 gerçekten `## Referans` bölümünde.

CA ikinci bir katman ekledi: o satırın işaret ettiği `proje-dosya-duzeni` skill'i
**CA'nın preload listesinde yok** — yani konumu söyleyen skill de elinde değil.
Ve `BEHAVIOR-REFERENCE-NOT-AUTOLOADED` gereği açmadığı referans onu bağlar ama
sende yoktur.

> CA: *"Adım olsaydı atlanamazdı."*

### Sahadaki karşılığı

Bu boşluk bugün **iki kez** somut zarar verdi (→ `SAPMALAR.md` S1, S2):
QA'nın RED raporu ve bir karar cevabı kanalda kalıp kayboldu; PA bugün ikisini
de arayıp bulamadı.

### Önerilen düzeltme

*"Üretilen denetim/analiz/karar çıktısı, akışın bir ADIMI olarak kalıcı kayda
geçer (ilgili ClickUp task'ının yorumu). Kanal taşıyıcıdır, kayıt değildir."*
— referans satırı olarak değil, **akış adımı** olarak.

---

## K2 — "Araç yoksa" dalı tanımsız (üç ayrı yerde aynı sınıf)

Üç agent üç farklı kuralda **aynı yapısal boşluğu** buldu: kanon bir aracı zorunlu
kılıyor ama o araç elde yoksa ne olacağını söylemiyor.

**CA — `CODE-COUNT-BY-LSP`** (code-quality:80): *"sayıyı LSP verir; grep karar
aracı DEĞİL"*. CA'nın elinde LSP yoktu.
> *"Kuralı harfiyen uygularsam tüketici sayısı raporlayamam → ANALIZ'in (A)
> bölümü ÜRETİLEMEZ. Ama aynı kanon ANALIZ üretmemi ZORUNLU kılıyor."*

**Clara doğruladı:** `code-quality` + `impact-analysis` içinde *"LSP yoksa /
araç yoksa / erişilemiyorsa"* → **0 eşleşme.** Fallback tanımsız.

**FE — `CODE-TEST-BEFORE-COMMIT` x Playwright yasağı.** Kanon tek doğrulama yolu
tanımlıyor (Playwright), o yol bu oturumda kapalıydı, *"test atlanamaz"* diyor.
> *"Kanonum, doğrulama aracının ELDE OLMADIĞI durumu düzenlemiyor."*

**BE — `BE-TELEPRESENCE-PROOF` x `BEHAVIOR-NO-INFRA-CMD`.** Kanıt üretmek BE'nin
zorunluluğu ama kanıtı üreten aracı (telepresence) agent çalıştıramıyor.
> *"Commit'imin geçerliliği başkasının bir eylemi yapmasına bağlı. Kullanıcı
> komutu koşturmazsa kanon ne yapacağımı SÖYLEMİYOR — 'commit etme' mi,
> 'kanıtsız commit et ve işaretle' mi belirsiz."*

**Ortak kök:** kurallar tek tek doğru; eksik olan **bekleme/fallback durumunun
tarifi.** Üçünde de agent kendi çözümünü üretti — yani davranış kanona değil
muhakemeye dayandı.

---

## K3 — QA'da gerçek çelişki: koordinat yasağı x kanıt zorunluluğu

**QA buldu, bugün fiilen çarptı:**

- `QA-USER-LANGUAGE`: *"doğrulama kanıtı (kanon-ID listesi, üç-akış adım dökümü,
  TARANAN DOSYA SAYISI) RAPORLANMAZ"* + *"'şu dosyanın şu satırında' koordinatı
  girmez"*
- `QA-EVIDENCE-NO-DIRECTIVE`: *"Kod kanıtı olmayan bulgu YASAK
  (dosya:satır/pattern ZORUNLU)"*
- `commit-review` çıktı şablonu: `#{n} | Bulgu | YER | Neden önemli`

> QA: *"'Yer' alanını doldurursam koordinat yasağına, doldurmazsam kanıt
> zorunluluğuna giriyorum. Üstelik Clara 'kaç dosya okuduğunu' İSTEDİ —
> `QA-USER-LANGUAGE` onu ismen yasaklıyor."*

Çözümü kendi kurdu: koordinat yerine yapı adı, dosya sayısını istendiği için verdi.
> *"İkisi de kanonun düzenlemediği bir orta yol — yani kural değil ben karar verdim."*

**QA'nın teşhisi:** çelişki sahte değil, eksik olan **"kime giden mesaj" ayrımı** —
kullanıcıya özet / developer'a kanıt. Ayrım yazılsa çelişki çözülür.

---

## K4 — Omurgadaki "cache bloğu" skill açma refleksini zayıflatıyor

**FE buldu ve kendi üzerinde ölçtü.**

`frontend` omurgasındaki "Operatif çekirdek" bloğu 12 kuralın özetini taşıyor ve
kendi içinde uyarıyor: *"Bu blok CACHE'tir, kaynak değil… Alet skilini açmak yine
ZORUNLU."* Ama `FLOW-OPEN-SKILL-FIRST` alan değişince skill açmayı emrediyor.

> FE: *"Blok kuralın ADINI ve HÜKMÜNÜ veriyor. Bu, skill açma refleksini fiilen
> zayıflatıyor — çünkü cevap zaten elimde görünüyor. Bugün T3'te tam bunu yaşadım:
> `text-error` bulgusunu `style` skill'ini AÇMADAN ürettim."*

FE bunu raporuna kusur olarak yazdı ve ekledi:
> *"Bunu 'kaldırın' diye yazmıyorum — bloğun gerekçesi de meşru. Ölçüm sonucu:
> **uyarı metni yetmiyor.**"*

---

## K5 — CA: `CA-TWO-WAY` ile `CA-NO-DIRECTIVE` sınırı tanımsız

`CA-TWO-WAY` reuse önermesini istiyor (*"sistemde bu iş için kullanılabilecek
yapı ZATEN var mı"*), `CA-NO-DIRECTIVE` çözüm direktifini yasaklıyor.
İkisi üst üste biniyor; sınırın nerede olduğu yazılı değil.

CA bunu T1'de de işaretlemişti, bugün fiilen çarptı.

---

## K6 — "Modül geçmişini oku" KURAL değil, yalnız akış adımı (PA ölçtü)

**Mert'in sorusu üzerine ölçüldü:** *"PA bir gereksinim aldığında docs/ altındaki
ilgili modülü arayıp daha önce ne yapılmış bakıyor mu? Böyle bir kanonu var mı?"*

### PA'nın cevabı: KURAL KODU YOK, akış adımı VAR

PA önce hafızadan cevapladı, sonra açıp doğruladı ve ayırdı:

**VAR olan** — `discovery` skill'i, akış adımı 1:
> *"**Bağlam oku** — `MODUL-INDEX` (modül haritası) + ilgili modül varsa
> `MODUL-BILGI` (kalıcı hafıza) + gereksinim dokümanları."*

**YOK olan** — kural kodu. PA 14 `PA-DISC-*` kuralını tek tek listeledi;
**hiçbiri bağlam/geçmiş okumayı düzenlemiyor.**

**Clara doğruladı:** `PA-DISC-*` sayısı **14** ✅ · *"Bağlam oku"* yalnız
`discovery:18`'de, adım olarak ✅ · *"önce oku/geçmişini oku"* emreden kural →
**0 sonuç** ✅

**En yakın kural başka şeyi düzenliyor** (`behavior`): *"Üretmeden önce var olanı
tara — duplicate açma."* Bu **kod** taraması, doküman geçmişi değil.

### PA'nın kendi teşhisi — K1'in aynası

> *"CA'nın bugün bulduğu **K1 ile AYNI SINIF**: 'kural var ama adım değil, adım
> olsaydı atlanamazdı' — burada **tersi**: adım var ama kural değil.
> **İkisi de aynı zaafı üretiyor: atlanabilir.**"*

### Bugün fiilen ne yaptı — ve neden yaptı

PA baktı: `docs/moduls/` ağacı · PRC-26 discovery'si **baştan sona (197 satır)** ·
iki `status.md` · `git log` + iki commit'in tam mesajı.

**Ama kural gereği değil:**
> *"KENDİ KARARIM. Kural olmadığı için kural gereği olamazdı. Beni tetikleyen şey
> KURAL değil, İŞİN KENDİSİ: soru zaten komşu modülü işaret ediyordu."*
>
> *"⚠️ VE TAM DA BURASI ZAAF: soru komşu modülü İŞARET ETMESEYDİ bakar mıydım?
> **Dürüst cevap: BELKİ.** Kural olmadığı için garanti yok."*

### Bakmasaydı ne kaçıracaktı — somut

PRC-26 discovery'sinin sonunda **iki düzeltme notu** vardı:
- *"bir risk cevabı KURAL üretiyorsa, o kuralın EKRANDA ne demek olduğu AYRI bir
  maddedir"*
- *"bir gereksinim cümlesi AKTÖR + YETKİ içeriyorsa, o aktörün bunu FİİLEN
  yapabilmek için neye ihtiyaç duyduğu AYRI bir maddedir"*

**Bu iki ders sayesinde PRC-40'ta T1/T2/T3'ü sordu.** T2 tam bu dersten çıktı:
*"2 saat kuralı HANGİ EKRANDA çalışır?"* → cevap *"hasta arayüzü yok"* → kural
kâğıt üstünde kalıyor → **tasarım düzeltildi** (sekreter seçimi kaldırıldı).

> *"Bakmasaydım T2'yi sormazdım. Discovery'de '2 saat kuralı var' diye yazılı
> kalırdı, BE onu kodlardı, ve **çalışmayan bir kural üretilirdi.**"*

### PA kendi eksiğini de buldu

> *"⚠️ MODUL-BILGI.md'leri AÇMADIM ve bunu bu ölçüm sırasında fark ettim. Kanona
> göre 'neden böyle' kararlarının evi ORASI. **Bugün şanslıydım** — discovery'ler
> zengindi. **Kural olsaydı MODUL-BILGI de listede olurdu ve atlamazdım.**"*

### Etkisi

> *"Atlanabilir ve atlandığı **FARK EDİLMEZ.** Discovery yine dolu görünür;
> eksik olan şey GEÇMİŞTEKİ DERS'tir ve o görünmez. Bakmayan bir PA aynı
> discovery'yi 'tam' diye kapatırdı."*

---

# Fabrikaya özet — öncelik sırasıyla

1. **K1** — çıktının kalıcı evi yok. Sahada iki kez zarar verdi. **Akış adımı
   olarak** yazılmalı, referans satırı olarak değil.
2. **K2** — "araç yoksa" dalı üç ayrı kuralda tanımsız. Agent'lar kendi çözümünü
   üretiyor; bu bugün iyi sonuç verdi ama kanona dayanmıyor.
3. **K3** — QA'da iki kural aynı çıktıda zıt emir veriyor. Çözüm: "kime giden
   mesaj" ayrımı.
4. **K4** — omurga cache bloğu uyarısı davranışsal olarak yetersiz (ölçüldü).
5. **K5** — CA'da iki kuralın sınırı tanımsız.

**Not:** dördü de *"uydurma sapma ölçümü bozar"* diyerek yalnız **fiilen
çarptıkları** yerleri yazdı. Teorik tarama yapmadılar — istenmişti, uydular.
