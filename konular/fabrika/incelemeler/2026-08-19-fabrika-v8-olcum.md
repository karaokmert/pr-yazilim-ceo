# Fabrika v8 ölçümü — hacim ve mimari arıza

Tarih: 2026-08-19
Bağlam: Mert *"iş yapamaz hale geldim v8 agentlarında"* dedi ve sıfırdan yeni bir
fabrika ekibi ürettirmemi istedi. Kanonu yok sayıp ihtiyaçtan başladım. Bu ölçüm o işin
zemini.

## Ölçülen hacim

Dört agent tanımı: **905 satır** (context-analyst 186, qa 206, developer 240,
manager 273).

Beş ortak skill + üç referans: **3.895 satır**. Dağılım (satır):
is-duzeni 1226, behavior 586, yapi-taslari 555, dagitim 416, uretim 386;
referanslar: arac-envanteri 413, kanal 313.

Bir agent işe girdiğinde önündeki kanon: yaklaşık **4.800 satır**.

Kural kimliği sayısı: **138** ayrı kimlik (`grep -rhoE '[A-Z]{2,4}-[A-Z-]{3,}'`,
tekilleştirilmiş).

En büyük skill içindeki tek bölüm: **525 satır** (`is-duzeni` → *Kuruluş hattı*,
216→741. satırlar). Bir iş akışı tarifi yarım kitap.

Teslim edilmiş ürün: `team/` altında iki takım, **31 dosya**.

## Resmi eşiğe göre kıyas — hepsi aşıyor

Claude Code'un kendi `skill-development` rehberi bir eşik veriyor: SKILL.md gövdesi
**1.500–2.000 kelime**, ayrıntı `references/`'a iner. Gerekçesi mekanik — gövde iş
gelince context'e girer, referans yalnız atıfla açılır.

Fabrikanın beş skill'i ölçüldü, **hiçbiri uymuyor** (kelime):
is-duzeni 9.489 · behavior 4.277 · yapi-taslari 3.900 · dagitim 2.880 · uretim 2.559.

En büyüğü eşiğin **4,7 katı**.

## Referans katmanı fiilen kullanılmıyor

Fabrikada iki referans dosyası var (313 + 413 satır) ve bunlara SKILL.md'lerden
**toplam 4 atıf** veriliyor. Üç skill'in (behavior, dagitim, uretim) hiç referansı yok
— hepsi gövdeye yığılmış.

Karşılaştırma: resmi `plugin-dev` plugin'inin **yedi skill'inin yedisinde de**
`references/` klasörü var.

Bu, Mert'in iki şikayetinin aynı kökten geldiğini gösteriyor: *"bir kararın nereye
yazılacağı hâlâ net değil"* (katman geçişi kurulamıyor) ve *"skiller sıradanlaşıyor,
agentlar çok sıkışık"* (o yüzden her şey gövdeye yığılıyor).

## Mimari arıza — asıl bulgu

Resmi `plugin-dev` agent'larında (`agent-creator`, `plugin-validator`,
`skill-reviewer` — 176/183/184 satır) **"skill" kelimesi hiç geçmiyor.** Gövdeleri
skill'e bağımlı değil; kendi kendine yeterli.

Fabrika ise kanonunun büyük kısmını skill'e koymuş ve agent'ın onu **adıyla
çağırmasını** beklemiş. Skill gövdesi kendiliğinden context'e girmediği için (ölçülmüş:
%91 kanon kaybı) yazılan kural agent'ın eline hiç geçmiyor.

**Yani arıza mekanikte değil, mimaride.** Skill'in yüklenmemesi Claude Code'un
davranışı; kanonu skill'e yığmak fabrikanın tercihi. İkincisi düzeltilebilir.

## Bu ölçümün kullanıldığı yer

`~/p/fabrika-v2/IHTIYAC.md` — yeni ekibin gereksinim dokümanı, bölüm 10 ve 11.
Üretilen ekip bu sayıları karşılaştırma zemini olarak taşıyor.

## Sınır

Ölçülen: satır, kelime, kimlik sayısı, referans atfı, resmi örneklerle kıyas.
Ölçülmeyen: bu hacmin sahadaki gerçek token maliyeti (context'e ne kadarının
girdiği ayrıca ölçülmeli), ve 138 kimliğin kaçının fiilen bir davranış ürettiği.
