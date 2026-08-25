# Kapanış — 2026-08-25 · EV (GPU/LLM ARGE araştırması)

**Süre:** 04:27 → 05:30 · **Tetik:** Mert uyudu, gece araştırması bırakıldı

---

## Ne bitti

**Beş araştırma koşuldu, ARGE planı yazıldı.**

Başlangıç sorusu: Hetzner GEX44 (RTX 4000 SFF Ada, 20 GB) alıp Qwen3.8-27B kurmak
mantıklı mı?

**Cevap: hayır — ama fikir sağlam, makine yanlış.**

### Üretilen dosyalar

- `incelemeler/gpu-llm-test-kurulumu/ARGE-PLANI.md` — sabah okunacak plan
- `incelemeler/gpu-llm-test-kurulumu/kurulum-plani.md` — adım adım kurulum

### Ölçülen teknik gerçekler

**Qwen3.8-27B gerçek bir model** (14 Ağustos 2026, Apache-2.0). Benim bilgi kesim
tarihimin dışındaydı — tahmin etmek yerine açıp baktım, iyi ki baktım.

**Mimari bulgusu:** 64 katmanın **48'i Gated DeltaNet** (KV cache tutmaz),
yalnız 16'sı normal attention. Token başına KV maliyeti klasik bir modelin
**dörtte biri** — 64 KB/token. Config'ten hesaplandı, bağımsız ölçümle birebir tuttu.

**Bağlam-VRAM tablosu (ölçülmüş):** 32K→20 GB · 64K→22 GB · 128K→26 GB ·
262K→~34 GB · 1M→~82 GB

**Model ağırlığı:** 4-bit 16,5 GB · FP8 ~31 GB · BF16 ~54 GB

### Fiyat tablosu (KDV hariç, 25 Ağustos)

**48 GB sınıfı (aylık kiralama):** LeaderGPU A6000 **499 €** · LeaseWeb L40S
**615 €** · Contabo L40S 690 € · Hetzner auction RTX 6000 Ada **771 €**
(kurulum yok, stok anlık) · OVH L40S 1.008 €

**24 GB:** LeaderGPU RTX 4090 **299 €** · OVH L4 540 € · Hetzner GEX44 (20 GB)
232 € + 114 € kurulum

**80-96 GB (1M bağlam için):** OVH A100 1.100 € · Hetzner GEX131 (96 GB)
**1.197 € + 599 € kurulum** · OVH H100 1.940 €

**Saatlik (test için):** OVH H100 80 GB **2,80 €/saat** · A100 80 GB 2,75 € ·
L40S 48 GB 1,40 € — dakika bazlı, taahhütsüz

---

## Yanıldığım ve düzelttiğim üç şey

**1 · "Uzun bağlamda VRAM biter."** Standart transformer KV cache varsayımıyla
söylemiştim. Model hibrit mimari kullanıyor, KV maliyeti dörtte bir. İtirazımın
teknik dayanağı çöktü.

**2 · "Hetzner'de 24 GB+ yoktur."** Var — GEX131 (96 GB) ve auction'da RTX 6000
Ada (48 GB).

**3 · "vLLM üç kat hızlı."** O ölçüm **eşzamanlı istek** altında alınmış. Tek
akışta üç yığın birbirine yakın. Sıralı kalite testi için Ollama daha pratik.

**Ve bir kez fazla ileri gittim:** Mert "sunucuya kurup test edeyim" dediğinde
bunu iş sunucusu diye okuyup kurumsal duruş dersi verdim. Sormadan varsaymışım —
kastettiği iş dışı kendi merakıydı. Özür diledim.

---

## Ne yarım kaldı

**Sabah kararı bekleyen üç şey (ARGE-PLANI.md'de yazılı):**
makine seçimi (H100 80 GB mı L40S 48 GB mi) · model listesi · Türkçe testinin
ağırlığı

---

## Mert'in kararını bekleyen — iki rakam

Bunlar oturum boyunca **beş kez soruldu, cevap gelmedi.** Teknik taraf kapandı
ama değer sorusu bunlarsız cevaplanmıyor:

**1 · Aylık gerçek Claude/token harcamamız.** Bu rakam olmadan "499 €/ay ucuz mu
pahalı mı" sorusunun cevabı yok.

**2 · Gerçekte kaç token bağlam kullanıldığı.** 1M *kullanılabiliyor* olması her
oturumda 1M *dolduruluyor* demek değil. 48 GB (500-615 €) ile 96 GB (1.200 €)
arasındaki kararı doğrudan bu belirliyor.

---

## Ölçüldü ama çözülmedi

**Türkçe verisi hiçbir modelde yok.** Qwen3.8-27B dahil — ne olumlu ne olumsuz.
Tamamen ölçülmemiş alan.

**Uzun bağlamda kalite ölçülmemiş.** 262K iddia ediliyor ama RULER/LongBench
sayısı yok. 4-bit sürümler için topluluk notu: *"uzun bağlamda odağını
kaybediyor."*

**Araç kullanımı ve sansürsüzleştirme ilişkisi literatürde yok.** Abliterated
modellerin tool-calling skoru hiçbir çalışmada ölçülmemiş. Bizim işimiz tam
orada — ölçersek literatürde olmayan bir şey ölçmüş oluruz.

**Qwen3.8-27B'nin iki bilinen arızası:** varsayılan reasoning seviyesi en yüksek
(basit istekte 22 bin düşünme token'ı, 21 dakika) ve "az düşün" ayarı yok
sayılıyor · varsayılan chat template bozuk, üç kat yavaşlatıyor.

---

## Ek bulgu — fabrikayı ilgilendirir

**"Claw" = OpenClaw**, bir model değil ajan çerçevesi (MIT, 387K yıldız).
**"Hermes" iki ayrı şeyin adı:** model serisi ve Hermes Agent (ajan çerçevesi).
"Hermes vs Claw" kıyası model kıyası değil, **ajan çerçevesi kıyası** — yani
fabrikamızın muadilleri.

⚠️ OpenClaw skill marketplace'ine yüklenenlerin **~%12'si zararlı kod** içeriyor.
Denetimsiz marketplace modelinin sonucu — fabrikanın denetim zinciri tam olarak
bunu engellemek için var.

---

## Bir sonraki hareket

**Sabah:** ARGE-PLANI.md okunur, üç karar verilir, sunucu kiralanır, kurulum
birlikte yapılır.

**Ve iki rakam hâlâ bekliyor** — aylık harcama ve gerçek bağlam kullanımı.
