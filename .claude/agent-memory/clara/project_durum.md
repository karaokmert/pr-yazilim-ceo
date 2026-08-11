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

## ⚠️ FABRİKA ADRESİ: `/Users/karaok/p/ozel-yazilim/skill-project`

`agent-project` kapatıldı — referans, açılış hook tetiği kaldırıldı.
Fabrika oturumu **`skill-project` penceresinden** açılır.

---

## FABRİKA — son kapanış (2026-08-11 21:30)

**`gunluk/fabrika/2026-08-11-kapanis-3.md`** ← **bunu oku, oradan başla.**
Günlük: `gunluk/fabrika/2026-08-11.md`

**Tek cümle:** Kanal açılış hook'u kuruldu (sahada iki kez doğrulandı) ve dört
turluk bir push denetimi koştu — dört engelleyici kapatıldı, PAD son düzeltmeyi
yaparken oturum kapandı.

**İlk hareket:** `~/.pr-kanal/skill-project/` altındaki **beş kutuyu oku
(`read.py`) → arşivle (`archive.py`)** → yeni kanal kur. Kapanış iki taraflı;
okunmamış mesaj varsa `archive.py` reddeder (rc=2), o imleç merkezin.

**Sonra:** push kararını Mert'e getir — kuyruk **20 commit**, 5 Ağustos'tan beri.

## Yarım kalan

**PAD** — E3'ün kalan cümlesi (`plugin-dagitim/references/surum-karari.md:96`,
`QA-EDIT-VERSION-ONLY`) + dört kırık atıf. **Çalışma ağacında duruyor**, commit
edilmedi.

**PQA** — PAM'in K10 commit'inin (`0f7e9e2`) denetimi. PAM iki soru sordu:
kaldırılan paragraf *kayıt* mıydı yoksa hükmün gerekçesi de gitti mi ·
`CLAUDE.md` ürün tarafında, `PAM-WRITE-DOCS-ONLY` sınırı.

## Mert'in kararını bekleyen

1. **Push** — `skill-project` 20 commit. Fabrikada commit onayı var, **push onayı
   ayrı ve alınmadı.**
2. **Yürürlükteki gerilim** — `PQA-NO-FILE-EDIT` (*"istisnasız"*) ↔
   `dagitim/SKILL.md:116` `DAG-BUMP-BY-AUDITOR` (*"tek istisnası budur"*). İkisi de
   yürürlükte. İşaretlendi, ayrı işe.
3. **16 kalem "eksik bırakıyor"** — PCA'nın 19 kaleminden üçü kapatıldı; kalanlar:
   47 kimlik `rules-index.json`'da yok · sekiz skill symlink · tekrar eden
   description'lar.
4. **Sprint yapısı işi — BAŞLANMADI.** Mert 16:00'da istedi: *"Goat, Egeli, Osinif
   sprint yapısını oku, fabrika ekibiyle incele, skill hâline getirmeye çalış."*
   İlk ölçüm: üç proje üç farklı yapı; **Osinif'te bir sprint düzeni çöpe atılmış**
   (`docs/trash/_sprint-2026-08`) — en değerli girdi o olabilir.
   **Açık soru:** inceleme Clara'da mı, PAM'e mi verilecek?

## EV hattı — son kapanış (2026-08-11 21:20)

`gunluk/ev/2026-08-11-kapanis-3.md` — Clara'nın OY yönetim yetkileri tanımlandı.
**EV push kuyruğu BOŞ.** Goat kuyruğu 14 commit.

Altı karar: kabul kriteri bizim/test dokümanı PA'nın · kanon bekçiliği bir KAPI ·
**commit onayı Clara'da, PUSH onayı Mert'te** · sahada ölçüm yok · Mert yokken
karar Clara'nın · soru süzme dört kademeli.

## Kanal

**Beş kutu açık, hiçbiri arşivlenmedi** (clara merkez + PAM/PQA/PAD/PCA).
**Monitör oturumla ölür.** Yeni kanal `--project skill-project`.

Agent artık **merkezin inbox'ına** yazıyor; Clara her açılışta eskisini arşivleyip
yenisini kuruyor (`setup.py` + `~/.claude/hooks/kanal-acilis.py`).
