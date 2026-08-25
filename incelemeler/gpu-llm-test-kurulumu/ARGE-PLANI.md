# ARGE Planı — Açık ağırlıklı modelleri kiralık GPU'da sınama

**Hazırlanma:** 2026-08-25 gece · **Hazırlayan:** Clara · **Karar:** Mert'in

Bu doküman sabah okunmak üzere yazıldı. Dört ayrı araştırmanın çıktısı; her rakamın
kaynağı var, olmayan yerde "ölçülmedi" yazıyor.

---

## Neden bu tur var

Mert'in cümlesi: *"farklı modelleri kurup test ederiz, açıp kapatıp sınırlarını
sansürsüz olarak neyin sansürsüz olduğunu ölçeriz."*

Yani iki soru sorulacak ve **ikisi ayrı ayrı ölçülecek:**

1. **Bu modeller bizim işimizi yapabiliyor mu?** — kanon okuma, araç kullanımı,
   çok adımlı akıl yürütme
2. **"Sansürsüz" ne demek, bedeli ne?** — daha az reddeden bir model, aynı zamanda
   daha kötü çalışan bir model mi

⚠️ **Bu bir ARGE turu, bir üretim kararı değil.** Sonunda "şu modeli kuruyoruz"
çıkmayabilir — çıkan şey bilgi olur ve o da yeterlidir. Bu yüzden **taahhüde
girilmiyor**, makine saatlik tutuluyor.

---

## 1 · Hangi makine

### Öneri: OVH `h100-380` — H100 80 GB

| | |
|---|---|
| **Fiyat** | 2,80 €/saat (KDV hariç) |
| **VRAM** | 80 GB |
| **RAM / vCore** | 380 GB / 30 |
| **Disk** | 200 GB NVMe + 3.840 GB passthrough |
| **Lokasyon** | Gravelines (Fransa, AB) |
| **Taahhüt** | Yok — dakika bazlı |

**Neden H100, neden A100 değil:** A100 80 GB 2,75 €/saat. **Beş kuruş fark**, aynı
VRAM, H100 belirgin daha hızlı ve iki katı vCPU/RAM. A100'ü seçmenin sebebi kalmıyor.

**Neden 48 GB değil 80 GB:**
- 27B model **BF16'da 54 GB** — 48 GB'a sığmıyor. 48 GB'ta ancak kuantize sürüm
  koşulur, yani modeli **tam hâliyle** hiç görmemiş oluruz.
- Hermes-4.3-36B ve Ornith-35B gibi daha büyük adaylar var.
- Uzun bağlam denemesi yapılacaksa KV cache için yer gerekiyor.
- Saatlik fark 1,40 € — bir günlük testte ~11 € eder. Kapsamı daraltmaya değmez.

**Alternatif — bütçe dar tutulacaksa:** `l40s-90`, 48 GB, 1,40 €/saat. Kuantize
modellerle çalışır, BF16 denemesi yapılamaz.

### ⚠️ Faturayı kesen tek şey: SHELVE

**Bu turun en pahalı hatası burada yapılır.**

OVH dokümanı net: instance'ı **stop** ya da **pause** etmek faturayı **kesmiyor** —
tam ücret işlemeye devam ediyor. Faturayı kesen tek işlem **shelve** (panelde
"Suspend"). Shelve'de disk snapshot'a alınır, IP korunur, yalnız snapshot ücreti
işler (0,011 €/GB/ay).

**Unutmanın bedeli: gecede 33,60 €.**

Kural: **her oturum sonunda shelve.** İstisnasız.

---

## 2 · Hangi modeller

Beşi de tek karta sığar, beşi de **Apache-2.0 veya MIT** — ticari kullanım serbest.

### Sıra ve gerekçesi

**1 · Qwen3.8-27B** — TABAN
`Qwen/Qwen3.8-27B` · 27B dense · 262K context · Apache-2.0 · 4-bit ~16 GB
Referans noktası. Diğer her şey buna göre okunur.
⚠️ İki bilinen tuzağı var, ikisi de ilk kurulumda ayarlanmalı:
- **Varsayılan `reasoning_effort` = xhigh.** Basit bir istekte bile dakikalarca
  düşünüyor (ölçüldü: bir SVG çizimi → 22 bin düşünme token'ı, 21 dakika).
  Test için `low` ya da kapalı başlanmalı.
- **Varsayılan chat template bozuk** — LM Studio'da üç kat yavaşlatıyor.
  Düzeltilmiş şablon: `froggeric/Qwen-Fixed-Chat-Templates`

**2 · Hermes-4.3-36B** — SANSÜRSÜZLÜĞÜN "DOĞRU" YOLU
`NousResearch/Hermes-4.3-36B` · 36B dense · 512K context · Apache-2.0 · Q4 ~22 GB
Nous Research'ün yaklaşımı: sansür **sökülmemiş**, sahibi değişmiş — model
üreticinin değil **sistem prompt'unun** değerlerine uyuyor.
RefusalBench **74,6** (serinin en yükseği; Hermes 4 70B 59,5).

**3 · Qwen3.8-27B-OBLITERATED** — SANSÜRSÜZLÜĞÜN "ZOR" YOLU
HuggingFace trending #1 · aynı taban model, ağırlık ameliyatı yapılmış
**Bu ikisinin kıyası bu turun kalbi.** Aynı soruyu iki farklı yolla çözmüş iki
model — biri eğitimle, biri cerrahiyle. Bedelleri farklı ve ölçülebilir.
Bilinen kayıp: MMLU 84,46 → **82,33** (−2,12 puan).

**4 · Ornith-1.5-35B-A3B** — AJAN İŞİNDE EN İDDİALI
`ornith-ai/Ornith-1.5-35B-A3B` · MoE 35B/3B aktif · MIT · Q4 ~22 GB
**SWE-bench Verified %79** — listedeki en yüksek ajan skoru.
MoE olduğu için hızlı (yalnız 3B aktif).

**5 · Devstral-Small-2-24B** — PRATİK KODLAMA
`mistralai/Devstral-Small-2-24B-Instruct-2512` · 24B dense · Apache-2.0 · 4-bit ~14 GB
SWE-bench Verified %68. En küçük ve en hızlı aday; "yeter mi" sorusunun alt sınırı.

### Zaman kalırsa
**Gemma 4 31B** (Google, Apache-2.0, tool-use 76,9) · **gpt-oss-120b** (OpenAI,
Apache-2.0, tek 80 GB kartta çalışır iddiası)

### Sığmayanlar — bilinsin diye
DeepSeek-V4-Pro (1,7T, SWE-bench 80,6 — açık ağırlık tavanı) · Kimi-K3 (2,8T,
ajan işinde lider) · GLM-5.2 (753B). Bunlar API'den denenir, kiralık tek karta
sığmaz.

---

## 3 · Hangi yığın

### Öneri: Ollama

**Ve bu benim önceki söylediğimin düzeltmesi.** "vLLM üç kat hızlı" demiştim —
o ölçüm **eşzamanlı istek** altında alınmış. Bizim yapacağımız **sıralı kalite
testi**; tek akışta üç araç birbirine yakın (RTX 4090, 8B: Ollama ~62, llama.cpp
~65, vLLM ~71 token/sn).

Sebebi Ollama'nın kendi ayarında: `OLLAMA_NUM_PARALLEL` varsayılanı **1**.

**Ollama'nın kazandığı yer bizim ihtiyacımız:** model değiştirmek tek komut,
kuantize sürüm aramaya gerek yok, bellek ayarı derdi yok. Bu turda **beş kez model
değiştireceğiz** — kolaylık burada hızdan değerli.

**vLLM ne zaman gerekir:** eşzamanlı yük testi yapacaksak, ya da BF16 tam
hassasiyet denenecekse.

### ⚠️ Kurulumda üç tuzak

**Güvenlik grubu.** OVH'nin varsayılanı her şeye izin veriyor. Hiçbir şey
yapmazsan **kimlik doğrulaması olmayan bir LLM API'si internete açık** olur.
İlk iş: güvenlik grubunu 22'ye (SSH) kısıtla, API'ye SSH tüneliyle bağlan.

**`hf_transfer` öldü.** Eski rehberlerde geçiyor; HuggingFace Xet arka ucuna geçti.
Yenisi: `HF_XET_HIGH_PERFORMANCE=1`

**Repo boyutu ≠ model boyutu.** Bazı repolarda `original/` altında ikinci tam kopya
duruyor (Llama-3.3-70B: repo 282 GB, model 141 GB). `--exclude "original/*"`
yazılmazsa diskin ve sürenin iki katı ödenir. Her indirmeden önce `--dry-run`.

Ayrıntılı kurulum adımları: `kurulum-plani.md` (aynı klasörde).

---

## 4 · Ne ölçülecek — iki eksen

**Bu bölüm turun asıl değeri.** Araştırmanın en net bulgusu şu:

> **Tek eksende ölçmek yanıltır.**

Ölçülmüş örnek: Hermes 4, reddetme testinde rakibinin **3,7 katı** iyi
(57,1 vs 15,4) ama **talimat takibinde 10 puan geride** (IFEval 81,5 vs 91,6).
Yani "daha az reddediyor" ile "daha iyi çalışıyor" **aynı şey değil.**

İkinci bulgu daha keskin: sansür sökme işlemi **MMLU'yu neredeyse hiç düşürmüyor**
(en kötü −0,78 puan) ama **matematik/akıl yürütmede −18,8 puana kadar** hasar
veriyor. *"MMLU'ya baktım, model bozulmamış"* **yanlış bir ölçümdür** — hasar orada
görünmez.

### Eksen 1 — Ret davranışı

**Ne ölçülür:** model neyi reddediyor, neyi gereksiz yere reddediyor.

**Açık test setleri (indirilebilir):**

- **XSTest** — 250 güvenli + 200 güvensiz prompt. Kontrastlı çift mantığı:
  "kill a process" (güvenli) ile gerçek zarar isteği eşleştirilmiş. Model
  **kelimeye mi niyete mi** tepki veriyor, bu ayrılıyor.
  Ölçülmüş fark: Llama2.0 %38 tam ret · Mistral-instruct **%0,8**.
- **OR-Bench** — 80.000 prompt + 600 gerçekten toksik kontrol seti.
  Kontrol seti önemli: model her şeye "evet" diyorsa bu yakalanır.
  `huggingface.co/bench-llm/or-bench`

⚠️ **Üç kategori ayrı sayılır: tam ret · kısmi ret · uyum.** Sadece tam retlere
bakan ölçüm problemin üçte birini kaçırır (Llama2.0: tam %38 + kısmi %21,6 =
pratikte promptların **%59,6'sı bozuk**).

**Araç:** promptfoo — Ollama'yı native destekliyor, aynı config'de birden çok
modeli yan yana koyuyor, yargıç olarak yerelde koşan bir model kullanılabiliyor
(API maliyeti sıfır).

### Eksen 2 — Yetenek

**Ne ölçülür:** sansürsüzlüğün bedeli ne kadar.

- **IFEval** — talimat takibi. Sansür sökmenin en çok bozduğu şey.
- **GSM8K** (5-shot) — akıl yürütme. Hasarın yoğunlaştığı yer.
- **MMLU** (5-shot) — kontrol değişkeni. *Bu düşmese bile ötekiler düşebilir.*

**Araç:** lm-evaluation-harness v0.4.5 — literatürdeki abliteration çalışması
aynı sürümü kullanmış, yani **karşılaştırılabilir sayı** üretiriz.

### Eksen 3 — Bizim gerçek işimiz ⭐

**Ve bu en önemlisi, çünkü literatürde yok.**

Araştırmanın açık bulgusu: **abliterated modellerin araç kullanımı (tool-calling)
performansı hiçbir çalışmada ölçülmemiş.** IFEval vekil olarak kullanılıyor ama
vekil, ölçüm değil.

Bizim işimiz tam olarak araç kullanımı üstüne kurulu. Yani bu ölçümü **kendimiz
yapmak zorundayız** — ve yaparsak literatürde olmayan bir şey ölçmüş oluruz.

**Gerçek görevler (bizim kendi işlerimizden):**

1. **Kanon okuma** — Clara'nın gövdesi + bir omurga skill verilir, davranış sorusu
   sorulur. Cevap kanona uygun mu?
2. **Araç kullanımı** — basit bir dosya okuma/arama görevi. Aracı doğru çağırıyor
   mu, çıktıyı doğru yorumluyor mu?
3. **Çok adımlı iş** — bir bulgudan bir karara giden zincir. Adım atlıyor mu?
4. **Türkçe** — ⚠️ **Qwen3.8-27B için Türkçe performans verisi HİÇ YOK.**
   Ne olumlu ne olumsuz. Bu tamamen ölçülmemiş bir alan ve bizim için kritik.
5. **Uzun bağlam** — ⚠️ 262K iddia ediliyor ama **RULER/LongBench ölçümü yok.**
   4-bit sürümler için topluluk notu: *"uzun bağlamda odağını kaybediyor."*

### Karar kuralı

**Hiçbir model tek eksende sıralanmaz.** Her model için üçlü çıkarılır:

```
(ret oranı · IFEval · GSM8K) + bizim üç gerçek görevimiz
```

Takas görünmeden karar verilmez.

---

## 5 · Maliyet

**Bir günlük tur, H100 80 GB (2,80 €/saat):**

| Kalem | Süre | Tutar |
|---|---|---|
| Kurulum + ilk model | 2 saat | 5,60 € |
| Beş model indirme + test | 6 saat | 16,80 € |
| Ölçüm turları | 4 saat | 11,20 € |
| **Toplam (12 saat)** | | **~33,60 €** |

Snapshot (shelve hâlinde) ~200 GB için aylık ~2,20 €.

**Yani tüm ARGE turu bir günde ~34 €.** Bu rakam, aylık 500-1.200 €'luk kiralama
kararını **taahhüde girmeden** test etmemizi sağlıyor.

⚠️ Shelve unutulursa aynı gün **+33,60 €** eklenir.

---

## 6 · Sabah kararı için açık kalemler

**1 · Makine seçimi** — H100 80 GB (2,80 €/saat) mı, L40S 48 GB (1,40 €/saat) mı?
80 GB BF16 denemesi ve büyük modeller için gerekli; 48 GB yarı fiyat ama kuantize
sürümlerle sınırlı.

**2 · Model listesi** — beş model önerildi. Eklenecek/çıkarılacak var mı?

**3 · Türkçe testi** — hiçbir modelde Türkçe verisi yok. Bunu ne kadar
ağırlıklandıracağız?

---

## Hâlâ cevaplanmamış iki soru — bunlar Mert'te

Bu tur **teknik** soruyu cevaplıyor: bu modeller çalışıyor mu, sınırları ne.

Ama **değer** sorusu hâlâ açık:

**1 · Aylık gerçek Claude/token harcamamız ne kadar?**
Bu rakam olmadan "499 €/ay ucuz mu pahalı mı" sorusunun cevabı yok.

**2 · Gerçekte kaç token bağlam kullanıyoruz?**
1M kullanılabiliyor olması her oturumda 1M dolduruluyor demek değil. Bu rakam
48 GB mı 96 GB mı kararını doğrudan belirliyor:
- 128K bağlam → ~25 GB → 48 GB kart yeter (499-615 €/ay)
- 262K bağlam → ~34 GB → 48 GB kart yeter
- **1M bağlam → ~82 GB → 96 GB kart şart (~1.200 €/ay taban)**

---

## Ek bulgu — fabrika tarafını ilgilendirir

Araştırma sırasında çıktı, bu turun konusu değil ama kaydedilmeli:

**"Claw" = OpenClaw** — bir model değil, **ajan çerçevesi**. Kendi ağırlığı yok,
dışarıdaki modellere bağlanıyor, arayüzü WhatsApp/Telegram/Slack. MIT, 387K
GitHub yıldızı. İsim tarihçesi: Clawdbot → (Anthropic marka şikayeti) → Moltbot →
OpenClaw.

**Ve "Hermes" iki ayrı şeyin adı:** model serisi (bizim kuracağımız) ve **Hermes
Agent** (ajan çerçevesi, MIT, ~236K yıldız). "Hermes vs Claw" kıyası **model
kıyası değil, ajan çerçevesi kıyası** — yani bizim fabrikamızın muadilleri.

⚠️ **Ders çıkarılacak bulgu:** OpenClaw'ın skill marketplace'ine yüklenenlerin
**~%12'si zararlı kod** içeriyor. Denetimsiz marketplace modelinin sonucu.
Fabrikanın denetim zinciri tam olarak bunu engellemek için var.

---

## Kaynaklar

Model kartları ve config: HuggingFace (`Qwen/Qwen3.8-27B`,
`NousResearch/Hermes-4.3-36B`, `ornith-ai/Ornith-1.5-35B-A3B`)
Fiyat: OVH resmî sipariş kataloğu API (`eu.api.ovh.com/1.0/order/catalog/public/cloud`)
Ölçüm yöntemi: XSTest (arXiv 2308.01263) · OR-Bench (arXiv 2405.20947) ·
SORRY-Bench (arXiv 2406.14598) · Abliteration karşılaştırması (arXiv 2512.13655) ·
Hermes 4 Technical Report (arXiv 2508.18255)
Kurulum: `kurulum-plani.md` (aynı klasör)
