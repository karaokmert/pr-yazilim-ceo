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

## EV — son kapanış (2026-08-11 10:00)

`gunluk/ev/2026-08-11-kapanis.md` — **19 saatlik saha izleme oturumu.**
Mert'in yönetimi kaydedildi (referans örnek): 15 düzeltme · 51 hamle · 16 kural
→ `incelemeler/proje-claralari/kayit.md`

**Üç karar Mert'te:** (1) proje yönetimi Clara'da mı PA'da mı — ölçüldü,
düzeltmelerin 11/12'si proje yürütme · (2) SCRUB: agent'lar `default` modda,
`auto`'ya geçmiyor · (3) kanal protokolü skill'de yok ama **memory'de var.**

**Sonraki adım:** analiz + planlama oturumu.

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
