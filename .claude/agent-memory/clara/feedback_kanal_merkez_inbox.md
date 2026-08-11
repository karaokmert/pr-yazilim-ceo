---
name: kanal-merkez-inbox
description: Agent artık merkezin inbox'ına yazıyor, kendi outbox'ına değil. Clara her açılışta eski kutusunu arşivleyip yenisini kurar — "en yeni = aktif" garantisi buradan geliyor.
metadata:
  type: feedback
---

**Agent'lar merkezin (Clara'nın) inbox'ına yazar**, kendi outbox'larına değil.
Clara her açılışta **eski `clara-*` kutularını arşivler**, yenisini kurar.

**Why:** Mert'in cümlesi (2026-08-11): *"Her mesajını ekranla birlikte kanala yaz.
Kanala yazmadığın mesajlar Mert'e düşmez. Tek ekranda kanal üzerinden takip ediliyor
tüm agentlar."* Eski düzende Clara N kutuyu tek tek taramak zorundaydı ve bir kutuyu
atlaması **sessiz** oluyordu.

Eskiyi kapatmak zorunlu çünkü **"aktif kutu hangisi" ölçülemiyor** — üç ölçüt denendi,
üçü de çürüdü: `STATE: OPEN` *"arşivlenmedi"* demek (Goat'ta 8 ölü kutu OPEN göründü) ·
`ps` projeyi vermiyor (her Clara'nın cwd'si `pr-yazilim-ceo`) · zaman eşiği uydurma.

**Belirsizlik ölçümle değil DÜZENLE kalktı:** her açılışta eski kapanırsa
**en yeni = aktif** olur. `CLA-FIX-THE-CAUSE`'un uygulanışı — ölçütü iyileştirmek
yerine ölçümü gereksiz kılmak.

**How to apply:**
· Açılışta hook sana ne yapacağını söyler (arşivle → kur → izleyici).
· ⚠️ `archive.py` **okunmamış mesaj varsa arşivlemeyi reddeder** — önce `read.py`.
  `--force` kaybı sessizleştirir, son çare.
· Değişen iki dosya: `skill-project/tools/kanal/setup.py` (merkez adresini bulup
  agent'a basar) · `~/.claude/hooks/kanal-acilis.py` (Clara kapısı + agent metni).
· **Kanon küçük harf `clara-`.** Sahada büyük harfli eski kutular var; tarama
  `.lower()` ile ikisini de buluyor.

⚠️ **Hook'a tip imzası yazılmaz.** Sistem `python3` = 3.9; `Path | None` 3.10+
sözdizimi ve import anında `TypeError` veriyor — **hook hiç çalışmaz, sessizce.**
Ölçüldü 2026-08-11, iki senaryoda da patladı.

İlgili: [[proje-yonetimi-yetkileri]]
