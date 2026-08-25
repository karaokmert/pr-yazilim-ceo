---
name: project-durum
description: Son kapanış dokümanının adresi ve tek cümlelik durum — her oturum açılışında İLK okunur
metadata:
  type: project
---

**Son iş: GPU/LLM ARGE araştırması (EV, 2026-08-25 gece).**
Kapanış: `gunluk/ev/2026-08-25-kapanis-gpu-llm-arge.md`
Plan: `incelemeler/gpu-llm-test-kurulumu/ARGE-PLANI.md` (sabah okunacak)

## BİLMEDEN İŞE BAŞLAMA

**1. Clara 2026-08-23'te sıfırdan yeniden kuruldu.** Gövde altı grup; omurga üç skill
(`clara-main`, `clara-is-disiplini`, `clara-behavior`) ve bunları açılışta açan hook
`~/.claude/hooks/agent-omurga-acilis.sh`. Skill'ler preload EDİLMİYOR.

**2. Yetki devri yapıldı.** Yetki sınırı yok, tek onay kapısı Mert. Agent'ı `Agent`
ile ÇAĞIRMAK yasak, `SendMessage` ile İLETMEK serbest.

**3. Fabrika `fabrika-v2`'de, üç rol: FPA / FPD / FQA.**

**4. Qdrant KAPALI.** `grep -l` kullanma, satır göster (`-h`).

## AÇIK — devam eden

**GPU/LLM ARGE turu — sabah kurulacak.** Sunucu kiralanacak (OVH, saatlik,
taahhütsüz), üstüne sırayla 5 model kurulup test edilecek. Üç karar Mert'te:
makine seçimi (H100 80GB 2,80€/sa vs L40S 48GB 1,40€/sa) · model listesi ·
Türkçe testinin ağırlığı.
⚠️ OVH'de instance STOP faturayı KESMİYOR — SHELVE gerekiyor (gecede 33,60€).

**Mert'ten iki rakam bekleniyor** (5 kez soruldu, gelmedi): aylık gerçek Claude
harcaması · gerçekte kaç token bağlam kullanıldığı. İkisi de kiralama kararını
belirliyor.

**Fabrika teslimi bekleniyor.** Üç gövde yazıldı (`8b62b61` fabrika reposunda).
Teslimde sorulacak üç kalem: `konular/fabrika-kisilik/TESLIMDE-SORULACAK.md`.
⚠️ Mert'in kararı: *"iş bitti derlerse sor, o zamana kadar bekle."*

**Fabrikaya handoff (23 Ağustos'tan devreden)** — Clara gövdesinin altı grubu ve
zayıflık kuralı fabrikaya anlatımla geçmeli.

**`oy-cache-bloklari`** — iş emri yazıldı (`8d443d6`), FPD'ye hiç gitmedi.
