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

## EV — son kapanış (2026-08-11 21:20)

`gunluk/ev/2026-08-11-kapanis-3.md` — **Clara'nın OY yönetim yetkileri tanımlandı.**

Mert `mert/` klasörünü açtı ve proje yöneticiliğini kendi kelimeleriyle yazmaya
başladı (**başlangıç metni, devamı gelecek**). Altı soru soruldu, altısı cevaplandı:

· **kabul kriteri bizim (ClickUp), test dokümanı PA'nın**
· **kanon bekçiliği artık bir KAPI** — *"aç, kontrol et"* deme yetkisi var
· **commit onayı Clara'da, PUSH onayı MERT'te**, push işlemini QA yapar
· **sahada ölçüm YOK** (evde var — moda bağlı)
· **Mert yokken karar Clara'nın**, rapora girer
· **soru süzme dört kademeli**, Mert'e özet gider

**Skill birleşti ve OY'a özelleşti:** `proje-yonetimi` 377→447, kadro ayrı
reference'a çıktı (`references/oy-ekibi.md`, 206 satır, kaynak v8 kanıtlandı).
**WS için ayrı skill yazılacak — yazılmadı.**

**Kanal düzeni değişti:** agent artık **merkezin inbox'ına** yazıyor; Clara her
açılışta eskisini arşivleyip yenisini kuruyor. İki dosya: `setup.py` (fabrika) +
`kanal-acilis.py` (hook).

**EV push kuyruğu BOŞ** — 12 commit gitti (`4f823ed..45acdd2`).

**Mert'i bekleyen:** fabrika kuyruğu **20 commit** (Clara push etmez) · fabrikaya
**üç devir bloğu** (send.py · PA gereksinim kası · setup.py değişikliği) · Goat
kuyruğu **14 commit**.

**Sonraki adım:** fabrika turu.

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

## İlk hareket

**Fabrika modundaysan:** kapanış dokümanındaki **devir bloğunu** Mert'e ver (harita
üçüncü sütunu + bitiş ölçütü, tek tur). Mert'in kararı: *"skill project'e geçince
yapacağımız iş olsun."*

**Yeni iş açma.** Kalan dört kalem: paylaşılan skill description dili (3) ·
`ui-designer` omurgası + dokuz iddia (5) · yıldız topoloji bağımsızlığı (6) · push (7).

**Push bekliyor:** `skill-project` **20** · `pr-yazilim-ceo` **0** (21:20'de push edildi).
Fabrikada commit onayı var, **push onayı ayrı ve alınmadı.**

**Fabrika ekibi AÇIK ama durdu** — dört kutu + iki BE, arşivlenmedi.
**Monitör oturumla ölür**, yeniden kurulur. Yeni kanal:
`--project skill-project` (varsayılan o ama bayrak yine yazılır).
