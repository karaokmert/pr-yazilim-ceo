# PR Template — durum

**ClickUp:** folder `901516693775` · Task List `901524326031` · Bugfix `901524326032` · Planning `901524539268`
**Prefix:** PRWST · **Kim:** Tarık (bu hafta)
**Ne:** Proje şablonu / kurulum hattı (`prvm-web`). Yeni projeler bu şablondan üretiliyor.

⚠️ Ölçüm 2026-09-02, ClickUp taraması.

---

## Sprint 7'nin işi — HAZIR VE BEKLİYOR

**PRY-18084 — Mobil provision hattı: koşullu bacak + dev sürüm dağıtımı**
Statü: **Open**, atanmamış.

**ARGE turu bitmiş, kararı Mert 2026-09-01'de vermiş, uygulama bekliyor.**

Kapsam (task açıklamasından):
- `prvm-web` kurulum hattına koşullu mobil bacak
- Şablona `apps/mobile/` iskeleti
- Liston `ci-mobile-release.yml` tabanlı sürüm hattı
- Smoke hattı

⚠️ **İçinde bir AÇIK KARAR var:** Android dev dağıtım yolu — **EAS iç dağıtım mı,
Play iç test mi** — işe başlama gününe bırakılmış. Yani bugüne.

⚠️ Tarık atanmamış.

---

## Diğer açık işler (bağımlılık için)

- PRY-18091 — Veritabanı şema değişikliği akışı (**in progress**, high)
- **PRY-18014 — next 16.3.3 güvenlik yükseltmesi (urgent)** — lıve-dev
- **PRY-18015 — astro 7.2.9 güvenlik yükseltmesi (urgent)** — **PAUSE**'da ⚠️
- PRY-18016 — Node 24 geçişi (high, lıve-dev)
- PRY-18017 — Prisma 7 (high, planning)
- PRY-18018 — ESLint 10 (pause)
- PRY-18019 — tailwind-merge 3 (pause)
- PRY-18020 — zod 4 (planning)
- PRY-18021 — lucide 1.37 (pause)

⚠️ **İki urgent güvenlik yükseltmesinden biri pause'da duruyor** (astro).

---

## Bloke

Yok.
