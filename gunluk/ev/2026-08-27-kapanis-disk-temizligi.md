# Kapanış — 2026-08-27 · Disk temizliği ve repo durumu (EV)

Oturum "yeni iş" olarak açıldı. İki iş yürüdü, ikincisi birinciden doğdu.

## Ne bitti

**1 · `web-sitesi` repo durumu taraması** (commit yok — salt ölçüm)
33 klasör tarandı: push'lanmamış commit, commit'siz içerik, çift kopya.
Bulgular `konular/web-sitesi-repo-durumu/BILINMESI-GEREKENLER.md`'de.
Mert: **"burada iş var, kalsın böyle"** — hiçbir şey commit'lenmedi/silinmedi.

**2 · Disk temizliği** — üç turda, her turu Mert onayladı:

| Tur | Ne silindi | Sonuç |
|---|---|---|
| `web-sitesi` | `.turbo` (43 GB) + `.next` (11.5 GB) + `~/.npm` | 72 → 17 GB |
| `ozel-yazilim` | `bin`+`obj` (.NET, 29.5 GB) + `.next`+`.turbo` | 66 → 27 GB |
| `~/p` geneli | 60+ gün dokunulmamış 66 `node_modules` + `.vscode-test` | 48 → 34 GB |

**Disk boş alan: ~19 GB → 95 GB (kullanım %11).**

Silinen her şey yeniden üretilebilirdi. Kaynak koda, commit'e, push'lanmamış
değişikliğe dokunulmadı. `bin`/`obj`'nin git'te takipsiz olduğu silmeden önce
`git ls-files` ile doğrulandı.

**3 · Turbo cache limiti eklendi**
`web-template-next/turbo.json` → `cacheMaxSize: "2GB"`, `cacheMaxAge: "7d"`.
Turbo 2.10 destekliyor; doküman üzerinden doğrulandı (context7), hatırlamayla
değil. Mert'in kararı: "ondan türetilenlerde çözülmüş olur."

⚠️ Bu değişiklik **commit'lenmedi** — `web-sitesi` reposu Clara'nın yazma alanı
değil, ve o repoda zaten commit'siz iş duruyor (Mert "kalsın" dedi).

## Ne yarım kaldı

**`web-template-next/turbo.json` commit'siz** — çalışma ağacında duruyor.
Commit kararı Mert'in.

**18 projede turbo limiti yok** — `turbo.json` miras alınmaz, kopyalanır.
Template'ten bundan sonra türetilenler limiti taşır, mevcut 18 proje taşımaz.
Bugün hepsi sıfırdan başladı ama limitsizler.

## Mert'in kararını bekleyen

**1 · `adalya-IT` / `yalinnetwork` symlink dönüşümü** — `.claude/agents` ve
`.claude/skills` klasörleri silinip symlink'e çevrilmiş, commit'siz. Commit'lenirse
o projeler plugin'e bağlanır; bu bir karar, mekanik temizlik değil.

**2 · `karaokai`'deki 40 commit'siz dosya** — `apps/denetim` altında 9 sayfa
klasörü + 15 UI component + mock data. Hiçbiri GitHub'da yok.

**3 · trendyol çifti** — `trendyol-siparis` ve `-2` aynı repo, aynı commit.
⚠️ Biri silinmeden önce `-siparis`'teki 3 dosya taşınmalı (`-2`'de yok).

**4 · 18 projeye turbo limiti yayılımı** — elle yazmak sürdürülebilir değil.

**5 · npm → pnpm geçişi** — 12 projede `package-lock.json`. pnpm global store +
hardlink kullanır; `~/.npm` 19 GB'a çıkarken `~/Library/pnpm` 3.4 GB'de kalmıştı.
Riski var, ayrı iş.

## Ölçüldü ama çözülmedi

**.NET `bin`/`obj`'nin üst sınırı yok** — turbo'daki `cacheMaxSize`'ın karşılığı
yok. Periyodik `dotnet clean` ya da süpürme düzeni kurulmadıkça birkaç ay sonra
yine ~30 GB.

**`~/p/docs/AuthKey_544L52H86W.p8`** — Apple imzalama anahtarı. Apple bir kez
indirtir, sonra yalnız yenisini oluşturmaya izin verir (eskisi iptal olur).
**Yedeği var mı ve hangi projede kullanılıyor — ikisi de bilinmiyor, taranmadı.**
Silme konusu olmadığı için ölçülmedi.

## Bir sonraki hareket

Yok — Mert kapanış dedi. Yukarıdaki beş karar açık duruyor, sorulduğunda açılır.
