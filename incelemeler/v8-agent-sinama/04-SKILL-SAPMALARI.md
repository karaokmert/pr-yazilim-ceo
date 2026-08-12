# Skill / kanon sapmaları — fabrikaya

> Mert'in dördüncü beklentisi: *"skillerimizde sapmalar var ise onları da bekliyorum."*
> Yöntem: dört agent'a **kendi kanonlarını** sorgulattım (T4). Şart: uydurma yok,
> "bulamadım" geçerli cevap, kanıt zorunlu. Her iddia Clara tarafından **dosyada
> doğrulandı**.
> Kaynak: `cache/pryazilim-agents/ozel-yazilim/0.7.0/.claude/skills/`

---

## K1 — Denetim/analiz çıktısının KALICI EVİ YOK ⚠️ EN AĞIR

**Üç agent bağımsız buldu** (BE · QA · CA) ve üçü de bugün fiilen çarptı.

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
