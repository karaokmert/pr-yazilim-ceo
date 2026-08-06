---
name: saha-izleme-yontemi
description: Saha izlemeyi nasıl kurarım — panel + canlı takip script'i, nerede duruyorlar, ölçülmüş iki tuzak. Oturum izleme istendiğinde ARAMADAN kur.
metadata:
  type: feedback
---

Mert *"agent'ları izle / takip et / monitör ol"* dediğinde **aramadan** şunu kur:

**1. Panel (arka planda sürekli koşar):** `panel/topla.py` — 10 sn'de bir
`~/.claude/projects/*/*.jsonl` tarar, `panel/durum.json` yazar. `panel/index.html`
onu `file://` ile çizer. Koşuyor mu: `ps aux | grep topla.py`.
`durum.json` şeması: `{guncelleme, acik_surec, proje_sayisi, oturumlar[]}`,
her oturum `{proje, oturum, rol, baslik, son_hareket, son_hareket_sn, son_kim,
son_mesaj, bekleme, bekleme_ne, skiller[], canli}`.

**2. Canlı takip:** `/tmp/clara-takip.py` — `Bash run_in_background` ile başlat.
15 sn'de bir yeni satırları okur, Mert mesajı / agent sorusu / handoff / izin
beklemesi basar. İzlenen beş proje script'in `PROJ` sözlüğünde sabit.

**Rol tespiti:** oturum kaydının başındaki `agent-setting` / `agent-name` /
`custom-title` satırlarından okunur. Süreç listesiyle eşleştirme denendi, roller
`?` kaldı — kayıttan okumak kesin sonuç verir.

**Why:** 2026-08-06'da Mert *"her açılan session'u görebiliyordun, bu kazanımları
unutmandan çok rahatsızım"* dedi. Bulguların hepsi kayıtlıydı ama YÖNTEM değildi;
üç dosya okuyup bulmam gerekti. Bulgu kaydı yöntem kaydının yerine geçmiyor.

**How to apply:** izleme istendiğinde önce `ps aux | grep topla.py` ile panelin
koşup koşmadığına bak, koşmuyorsa başlat; sonra canlı takibi arka planda aç.
Yeni proje izlenecekse `/tmp/clara-takip.py` içindeki `PROJ` sözlüğüne ekle.

## Ölçülmüş iki tuzak (script'te düzeltilmiş — bozmadan koru)

**İzin tespitinde yarış koşulu.** `tool_use` görülür görülmez "izin bekliyor"
demek yalancı pozitif üretir; normal onaylı çağrıda da `tool_use` ile
`tool_result` arasında milisaniye var. Çözüm: bir tur (15 sn) bekle, sonuç hâlâ
yoksa duyur.

**Handoff tespitinde varlık vs konum.** `"HANDOFF" in metin` bir VARLIK testi;
ölçülmek istenen KONUM. Agent'lar kendi çıktıları hakkında konuşuyor
(*"handoff'u yeşil ışık sayıyorum"*) ve sistematik yalancı pozitif çıkıyor.
Çözüm: satır başında `---HANDOFF` / `HANDOFF (` / `**HANDOFF` kalıbı ara.

İlgili: [[saha-izleme-rolu]], [[olcum-kaynaga-git]]
