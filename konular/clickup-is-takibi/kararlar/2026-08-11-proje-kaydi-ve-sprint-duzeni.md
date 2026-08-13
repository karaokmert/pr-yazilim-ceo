# Proje kaydı ve sprint düzeni — ClickUp ana kaynak, repo tezgah

> **Karar tarihi:** 2026-08-11 · **Karar:** Mert
> **Bağlı karar:** `kararlar/2026-08-11-clara-proje-rolu.md`

## Problem

Clara'nın yeni rolünde gereksinim ve sprint planı üretmek var (birinci iş) ama
bunların **nerede yaşayacağı** tanımsızdı.

Bugünkü durum: `projeler/` klasörü var, içinde iki altyapı dokümanı duruyor
(`agent-dagitim-yapisi.md`, `envanter.md`) — **proje kaydı yok.** `sprint/` klasörü
var, içinde bir hafta eskimiş tek sprint dosyası ve Python deneyleri.

## Karar 1 — ClickUp ana kaynak, repo çalışma alanı

> **Kesinleşen ClickUp'ta yaşar. Repo Clara'nın tezgahıdır.**

**ClickUp'ta yaşayanlar:**
- Sprint planı (proje bazlı)
- Gereksinim · user story · test case · beklenen davranış
- Task'lar (sprint task'ı ve iş task'ı)

Emsal biçim: ClickUp doc `qa5p6-234675` (*EO - Tekil Eğitim Atama*) — operasyon
başlığı → katman task linkleri (Doküman/UI/Fullstack) → sprint kalemleri →
her kalemin gereksinim maddeleri.

**Repoda (`projeler/{proje}/`) yaşayanlar:**
- Taslak (ClickUp'a çıkmadan önceki hâli)
- Ölçüm ve bulgu (o projeye ait)
- Yarım kalan iş

**Gerekçe:** Mert repoyu okumuyor, ClickUp'ı okuyor — ekip de öyle. Kesinleşen bir
şey repoda kalırsa **görünmez** olur. Ama Clara'nın yarım işi ve ölçümü ClickUp'a
gitmemeli: ClickUp'a yazma güvenilmez (ölçüldü: dokuz sayfada iki sessiz hata) ve
her taslak orada gürültü yapar.

**Ayıran test: bu kesinleşti mi?** Kesinleştiyse ClickUp. Kesinleşmediyse repo.

## Karar 2 — İki katmanlı sprint

> **Proje sprint'i PA ile yürür. Haftalık görünüm ondan TÜRETİLİR.**

**Proje sprint'i** — her projenin kendi ritmi. Clara + Mert gereksinimi belirler,
PA discovery'ye çevirir, katman task'ları düşer. ClickUp'ta yaşar.

**Haftalık görünüm** — Mert'in tüm projelerden kesiti. *Bu hafta hangi projeden
hangi işler var, ne bekliyor, kimde.* Mevcut `sprint-yonetimi` skill'i bunu
Çarşamba–Çarşamba döngüsüyle zaten kuruyor.

**Kritik: ikincisi birincisinden TÜRETİLİR, ayrı planlanmaz.** Haftalık görünüm
kendi başına bir plan olursa iki ayrı gerçek olur ve hangisinin bağlayıcı olduğu
belirsizleşir — *"kopya bayatlaması"* (ölçüldü, 2026-08-10: aynı bilgi üç yerde,
biri güncellenmemiş).

Haftalık görünüm bir **rapor**, bir plan değil. Kaynağı proje sprint'leri.

## Klasör düzeni

```
projeler/
  agent-dagitim-yapisi.md     ← mevcut, altyapı
  envanter.md                 ← mevcut, altyapı
  {proje}/                    ← YENİ, proje başına
    taslak/                   ← ClickUp'a çıkmamış gereksinim
    olcumler/                 ← o projeye ait bulgu
```

**`sprint/` klasörü:** haftalık görünümün kaydı burada kalır. İçindeki Python
deneyleri (`qdrant-*.py`, `memory-*.py`) sprint işi değil — ARGE artığı,
temizlenecek.

## Ne YAZILMAZ

- **PA'nın alanı:** `docs/_project/PROJECT-INFO`, `MODUL-INDEX`, `TASK-STATUS`
  proje reposunda ve PA'nın. Clara oraya yazmaz, okur.
- **Durum:** *"şu an nerede"* bilgisi tutulmaz, kaynaktan okunur (`hafiza-duzeni`).
  Repoda duran bir durum satırı bir gün sonra yalan olur.
