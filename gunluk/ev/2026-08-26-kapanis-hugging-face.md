# Kapanış — 2026-08-26 · EV (Hugging Face inceleme)

**Süre:** 00:41 → 09:36 · **Tetik:** Mert bir Anthropic dataset linki gönderdi,
konu platformun kendisine açıldı · **Mod:** merak / öğrenme, iş değil

---

## Ne bitti

**Hugging Face platformu uçtan uca incelendi ve kanona yazıldı.**
→ `konular/hugging-face/BILINMESI-GEREKENLER.md`

Gezinme değil ölçüm yapıldı — her iddia için kaynak açıldı:
- `Anthropic/claude-protein-binder-design` — README ham çekildi (kart kesik geliyordu)
- Dataset listeleri API'den çekildi (en çok indirilen 25, Türkçe, kod)
- `openai/gsm8k` ve `python_code_instructions_18k` satırları **açılıp içi gösterildi**
- `TrGLUE` alt test paketleri listelendi
- `FLUX.1-dev` ve `stable-diffusion-v1-4` lisansları karşılaştırıldı
- `OBLITERATUS/Qwen3.8-27B-OBLITERATED` kartı okundu
- Qwen sansürsüz sürümleri sayıldı ve sınıflandı (40+ giriş, 4 grup)

## Kayda değer bulgular

**İndirme sayısı kalite göstergesi değil.** En çok indirilenler listesinin başında
milyonlarca indirme almış, beğenisi sıfıra yakın çöp kayıtlar var. Otomasyon şişirmesi.
Bakılacak yer beğeni + yükleyen hesap.

**Aynı işi yapan iki modelin lisansı zıt olabiliyor.** FLUX.1-dev ticari kullanıma
kapalı (ama çıktısı açık), Stable Diffusion v1.4 tamamen açık. `license: other`
gördüğün yerde metin okunur.

**Ağırlığı açık modelde güvenlik önlemi sökülebiliyor.** Abliteration tekniği;
bedeli MMLU'da ~2 puan. Platform genelinde 1000+ böyle kayıt.

**ARGE turuna doğrudan bağlanan şey: `turkish-nlp-suite/TrGLUE`.** Beş model
karşılaştırılırken kendi soru listemizi uydurmak yerine bu koşulursa ölçüm
tartışılabilir olmaktan çıkar — soruları biz seçmemiş oluruz.

---

## Kendi düzeltmem

**Merak sorusuna amaç sordum, üç tur üst üste.** Mert kesti: *"neden byrda peki
merak gideriyorum clara her şeyi değil?"*

`clara-is-disiplini`'deki "bağlamı tart" kuralını yanlış yere uyguladım — o kural
bir İŞ başlarken geçerli, merak için değil. Ayrıca üç kez "neler var" diye sorulması
benim liste vermemin yetmediğini gösteriyordu; veri setinin İÇİNİ açınca anlaşıldı.

→ Yazıldı: `.claude/agent-memory/clara/feedback_merak_amac_sorma.md`

---

## Ne yarım kaldı

Yok. Konu kapandı.

## Mert'in kararını bekleyen

Yok — bu oturumda karar üretilmedi, öğrenme oturumuydu.

## Ölçüldü ama çözülmedi

**`armand0e/claude-fable-5-claude-code`** — dataset listesinde 367 beğenili bir kayıt.
Adından Claude Code oturumlarının veri seti hâline getirilmiş olduğu anlaşılıyor.
**İçine bakılmadı.** Bizi ilgilendirebilir (kendi ajan çıktılarımızın nasıl
paketlendiği), ama ölçülmedi.

**`OBLITERATUS` kartındaki MMLU sayıları kendi beyanı** — bağımsız doğrulaması yok,
koşulmadı.

---

## Önceki oturumlardan devreden — DEĞİŞMEDİ

- **GPU/LLM ARGE turu** — plan hazır (`incelemeler/gpu-llm-test-kurulumu/ARGE-PLANI.md`),
  üç karar Mert'te (makine · model listesi · Türkçe testinin ağırlığı). İki rakam
  hâlâ bekleniyor: aylık gerçek Claude harcaması · gerçek bağlam token kullanımı.
  ⚠️ Bu oturum ARGE'ye bir girdi ekledi: TrGLUE.
- **Mezarlık teklifi (Emre Telyar)** — `~/Desktop/EMRE TELYAR.docx`; Mert'te ek hizmet
  fiyatları + içindekiler güncellemesi.
- **Fabrika teslimi** — bekleniyor, sorulmayacak.

---

## Bir sonraki hareket

ARGE turu — makine kararı verilip sunucu kiralanacak.
