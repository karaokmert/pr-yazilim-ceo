# Hugging Face — bilinmesi gerekenler

Kaynak: 2026-08-26 gecesi Mert ile inceleme oturumu. Platform gezildi, örnekler
açılıp içine bakıldı. ARGE turunda model indirilirken bu dosya açılır.

---

## Platform ne

Yapay zekâ modellerinin dağıtım kanalı. Beş bölüm: **Models** (eğitilmiş ağırlık
dosyaları) · **Datasets** (veri setleri) · **Spaces** (çalışan demolar) ·
**kütüphaneler** (`transformers`, `datasets` — kod içinden model adı yazınca iniyor) ·
**Inference** (onların sunucusunda çalıştırma, ücretli — bizim ilgi alanımız değil).

Sektörün fiilî standardı: bir model yayınlandığında ilk buraya konuyor.

---

## Model seçerken bakılacak üç şey

**1 · Kim yüklemiş.** Resmi hesap mı (`Qwen/`, `openai/`, `allenai/`), birey mi.
Aynı isim altında çok farklı davranan sürümler dolaşıyor.

**2 · Beğeni sayısı — indirme DEĞİL.** Ölçüldü: en çok indirilenler listesinin
başında `KakologArchives`, `ayuo/hd_tmp`, `Dagonulca/figofigofigofigo` gibi
milyonlarca indirme almış, beğenisi sıfıra yakın çöp kayıtlar duruyor. İndirme
sayısı bir otomasyonun defalarca çekmesinden şişiyor. **İndirme kalite göstergesi
değil.**

**3 · `base_model` satırı.** Hangi orijinali işaret ediyor.

---

## Lisans — müşteri işine model koyarken belirleyici

**Ölçülmüş iki zıt örnek:**

`black-forest-labs/FLUX.1-dev` (görsel üretme, 12B) — lisans alanı `other`, adı
**FLUX.1 [dev] Non-Commercial License**. Model kartı KAPALI, girmek için hesap açıp
şartları kabul etmek gerekiyor. Kritik ayrım: **modelin kendisi ticari kullanılamaz,
ürettiği görseller kullanılabilir.**
→ Teklife görsel hazırlamak serbest · müşteri paneline "görsel üret" düğmesi koymak
YASAK. İkincisi için ya ticari lisans satın alınır ya **FLUX.1-schnell** kullanılır
(Apache-2.0, kısıtsız, kalitesi bir tık düşük).

`CompVis/stable-diffusion-v1-4` (aynı işi yapan 2022 modeli) — `creativeml-openrail-m`,
**ticari kullanıma açık.** Aynı işi yapan iki model, iki farklı hukuki sonuç.

⚠️ `license: other` gördüğün her yerde metin okunur — standart lisans değil, özel
yazılmış demektir.

**Serbest olanlar:** Apache-2.0, MIT, OpenRAIL-M. **Şartlı:** Llama lisansı.
**Yasak:** non-commercial olanlar.

---

## Veri setleri — dört işe yarıyor

Yapısı hep aynı: bir tablo, birkaç sütun. Fark ne için kullanıldığında.

**Eğitim yakıtı** — ham metin yığını (`allenai/c4`, `m-a-p/FineFineWeb`).
Türkçe: `hasankursun/turkish-corpus-100b`, `ytu-ce-cosmos/Cosmos-Turkish-Corpus-v1.0`,
`turkish-nlp-suite/BellaTurca`. Biz model eğitmiyoruz — doğrudan işimize yaramıyor.

**Ölçüm seti — BİZE YARAYAN.** Soru + doğru cevap. `openai/gsm8k` (matematik,
8 bin satır, cevap `#### 72` biçiminde). Türkçe karşılığı
**`turkish-nlp-suite/TrGLUE`** — tek test değil, dokuz alt test paketi (`cola`
cümle doğru kurulmuş mu · `mnli` iki cümle çelişiyor mu · `qnli` paragraf soruyu
cevaplıyor mu), her biri train/validation/test bölümleriyle.
→ **ARGE turunda beş model karşılaştırılırken kendi soru listemizi uydurmak yerine
bu kullanılır — soruları biz seçmemiş oluruz, ölçüm tartışılabilir olmaktan çıkar.**

**Öğretme seti** — istek + beklenen cevap (`iamtarun/python_code_instructions_18k_alpaca`:
instruction / input / output / prompt sütunları).

**Bilimsel sonuç yayını** — `Anthropic/claude-protein-binder-design` bu sınıfta.

---

## Neden herkes bedava model yüklüyor

Yükleyene göre sebep değişiyor:

**Büyük şirketler — dağıtım savaşı.** Meta/Alibaba modeli bedava veriyor, çünkü
gelir modelleri API satmak değil. Rakibin (OpenAI, Anthropic) satabildiği şeyi
bedavaya düşürüyor. Alibaba'da daha net: **model yem, sunucu ürün** — Qwen bedava,
ciddi kullanan Alibaba Cloud kiralıyor.

**Küçük şirketler — satış hunisi.** Black Forest Labs: schnell bedava · dev kısıtlı ·
pro paralı.

**Üniversiteler — atıf.** Makale yayınlarken model de yayınlanmazsa doğrulanamaz.
Stable Diffusion'ı yükleyen `CompVis` bir Alman üniversite grubu.

**Bireyler — itibar.** Görünürlük, iş teklifi.

**Asıl mekanizma:** kapalı model tek şirketin elinde gelişir, açık model binlercesinin
elinde. CompVis vasat bir model yayınladı, iki yılda topluluk üstüne binlerce varyant
kurdu — tek başına yapamayacağı gelişmeyi bedavaya aldı.

**Bizim için sonucu:** açık modeller kapalıların peşinden geliyor ama arayı kapatıyor.
ARGE turunun sorusu "açık model Claude kadar iyi mi" değil — **"hangi işlerimizde
açık model yeter"**; yettiği yerde maliyet sıfıra iniyor.

---

## Aynı modelin kırk sürümü — neden

Ölçüldü: tek bir model (Qwen3.8-27B) için 40+ sansürsüz giriş, platform genelinde
`abliterated` etiketiyle 1000+ kayıt. Ama **çoğu farklı model değil**, dört gruba
ayrılıyor:

**Gerçekten farklı olanlar — bir avuç.** `huihui-ai`, `OBLITERATUS`, `orcarouter`,
`0bserverx`. Filtreyi kendi yöntemiyle sökenler; fark yöntemde (hangi katman, ne
kadar agresif, karşılığında ne kadar zekâ kaybı).

**Format çevirileri — çoğunluk.** `-GGUF` (normal bilgisayar: Ollama/LM Studio) ·
`-MLX` (Apple Silicon) · `-AWQ`/`-FP8`/`-NVFP4` (sıkıştırılmış, az bellek).
Yeni model değil, aynı modelin ambalajı. `mradermacher` hesabının listede yedi
girişi var — model üretmiyor, **format çeviren bir servis.**

**Sıkıştırma dereceleri.** `3.69bpw-12GB` gibi; herkes kendi donanımına göre sürüm
çıkarıyor.

**Kopya ve isim şişirme.** `PHILADELPHIA-CLASS`, `AEON-ULTIMATE`, `PristinelyUncensored`
— indirmesi düşük, beğenisi tek haneli.

Sebep mekanik: yükleme bedava ve yarım saatlik iş · herkesin donanımı farklı ·
itibar biriktiriliyor.

---

## Sansürsüz (abliterated) modeller

`OBLITERATUS/Qwen3.8-27B-OBLITERATED` incelendi. Resmi Qwen alınmış, ağırlıklarda
"reddet" davranışını üreten yön bulunup **silinmiş** — yeniden eğitim değil, doğrudan
ağırlık müdahalesi.

**Bedeli kendi kartında yazılı:** MMLU %84,5 → %82,3. Filtre sökülünce model
biraz aptallaşıyor. ⚠️ Bu sayı kendi beyanı, bağımsız doğrulaması yok, koşulmadı.

**Lisans Apache-2.0 görünüyor** (orijinalden geliyor) — teknik olarak ticari
kullanıma açık. **Ama müşteriye teslim edilecek şey değil:** hiçbir talebi
reddetmeyen bir model müşteri panelinde çalışıyorsa riskin sahibi biziz.

Meşru kullanımı var: güvenlik testi (`ai-safety-research`, `red-team` etiketleri).
Bir sistemin kötüye kullanıma dayanıklılığını ölçmek için reddetmeyen model gerekiyor.

**Yapısal gerçek:** ağırlığı açık modelde güvenlik önlemleri SÖKÜLEBİLİR.
İndirilebilen ağırlık, değiştirilebilen ağırlıktır.

---

## Dosya formatı — güvenlik

`.bin` eski format, açıldığında **kod çalıştırabiliyor.** `.safetensors` bu yüzden
çıktı — sadece sayı taşıyor. İndirirken `.safetensors` tercih edilir.
2022 öncesi modellerde ikisi birden bulunuyor (geçiş dönemi).

Platform açık — model yükleyen herkes yükleyebiliyor. Kurumsal kullanımda bakılan:
kim yüklemiş, dosya formatı ne.

---

## Bir "model" tek dosya değil

Görsel modellerde klasörlerden oluşuyor: `text_encoder/` (metni anlayan) ·
`unet/` (resmi çizen) · `tokenizer/` (metni parçalayan sözlük) · `safety_checker/`
(çıktı filtresi) · `scheduler/` (kaç adımda çizileceği). Dil modellerinde tek gövde.
