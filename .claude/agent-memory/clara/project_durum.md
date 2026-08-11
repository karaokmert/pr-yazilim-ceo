---
name: durum
description: İLK BUNU OKU — son kapanış dokümanının adresi ve tek cümlelik durum. Oturum açılışında ilk okunan kayıt.
metadata:
  type: project
---

# Durum

> **`gunluk/` proje bazlı:** `gunluk/ev/` (Clara'nın kendi işi) · `gunluk/fabrika/`
> (fabrika hattı) · `gunluk/{proje}/`. Açılış hook'u her projenin son kapanışını ayrı
> listeler — **yalnız kendi modunun kapanışı okunur.**

## EV — son kapanış (2026-08-11 18:22)

`gunluk/ev/2026-08-11-kapanis-2.md` — **Clara'nın proje rolü tanımlandı.**

**Üç kök kapatıldı** (dünkü 17 düzeltmenin kaynağı) ve üçü tek yere bakıyormuş:
Mert'in cümlesi — *"beni proje takibinden kopartırsa Clara devre dışı kalır."*
· Kök 1 sınır → rol tanımsızdı, tanımlandı (**yönetim temsilcisi / PMO Assistant**)
· Kök 2 sunum → kural yanlıştı (%92 haklı ihlal), iki tur tipine ayrıldı
· Kök 3 takip → liste güncellenmiyor değil **hiç açılmıyordu** (`CLA-TRACK-WHAT-YOU-SEND`)

**Beş karar dosyası** yazıldı, kanona işlendi (`proje-yonetimi` 246→377 satır).
**Merkez yayın kanalı** kuruldu: `tools/clara-yayin.py` (yalnız Clara kutuları,
teslim doğrulamalı).

**Mert'i bekleyen:** Goat push kuyruğu **14 commit** (CA denetimi 17:50'de başladı,
sonuç gelmedi) · fabrikaya **iki devir bloğu** (send.py inbox kontrolü + PA gereksinim
kası) · EV push kuyruğu 8 commit.

**Sonraki adım:** fabrika turu — devir blokları hazır, ve listedeki üçüncü durak
(fabrika + OY v8 ekibi) hiç açılmadı.

## ⚠️ FABRİKA ADRESİ DEĞİŞTİ (2026-08-11)

**Fabrika `/Users/karaok/p/ozel-yazilim/skill-project`'te.**
`agent-project` kapatıldı — referans, açılış hook tetiği kaldırıldı.

**Fabrika oturumu `skill-project` penceresinden açılır.**

## Son kapanış — FABRİKA hattı

**`gunluk/fabrika/2026-08-11-kapanis-2.md`** ← **bunu oku, çalışmaya oradan başla.**

**Tek cümle:** Repo taşınması kapatıldı (141 dosya kurtarıldı, adresler düzeltildi,
kanal varsayılanı + tek kaynak) — sıradaki iş **PAM'e tek tur, iki kalem**; devir
bloğu kapanış dokümanında hazır.

**Destek belgeleri (gerekirse):**
- `gunluk/fabrika/2026-08-11-sabah-brief.md` — kalan **dört kararın** tam metni
- `gunluk/fabrika/2026-08-11-kapanis.md` — sekiz rol turunun kapanışı
- `kararlar/2026-08-11-fabrika-skill-projecte-tasindi.md` — taşınmanın gerekçesi

## Son kapanış — EV hattı

`gunluk/ev/2026-08-10-kapanis.md`

## İlk hareket

**Fabrika modundaysan:** kapanış dokümanındaki **devir bloğunu** Mert'e ver (harita
üçüncü sütunu + bitiş ölçütü, tek tur). Mert'in kararı: *"skill project'e geçince
yapacağımız iş olsun."*

**Yeni iş açma.** Kalan dört kalem: paylaşılan skill description dili (3) ·
`ui-designer` omurgası + dokuz iddia (5) · yıldız topoloji bağımsızlığı (6) · push (7).

**Push bekliyor:** `skill-project` 15 · `agent-project` 1 · `pr-yazilim-ceo` 59+.
Commit onayı var, **push onayı ayrı ve alınmadı.**

**Fabrika ekibi AÇIK ama durdu** — dört kutu + iki BE, arşivlenmedi.
**Monitör oturumla ölür**, yeniden kurulur. Yeni kanal:
`--project skill-project` (varsayılan o ama bayrak yine yazılır).
