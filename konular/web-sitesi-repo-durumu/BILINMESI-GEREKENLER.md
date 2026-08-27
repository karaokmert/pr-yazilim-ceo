# web-sitesi klasörü — repo durumu

**Ölçüm tarihi: 2026-08-27.** Yöntem: `/Users/karaok/p/web-sitesi` altındaki
33 klasörde `git status --porcelain` + `git log @{u}..HEAD` + remote karşılaştırması.

⚠️ Bu bir **anlık fotoğraf.** Tekrar bakılacaksa yeniden ölçülür — aradan geçen
her gün bu tabloyu eskitir.

## Karar

Mert bakıldı ve **"burada iş var, kalsın böyle"** dedi. Hiçbir commit atılmadı,
hiçbir dosya silinmedi. Temizlik ayrı bir iş olarak duruyor, henüz başlamadı.

## Ne bulundu

**Push'lanmamış commit — 2 repo**
- `web-template` — 3 commit yerelde
- `zikirvakti` — 1 commit yerelde

**Symlink dönüşümü commit'siz — 2 repo**
`adalya-IT` ve `yalinnetwork`: `.claude/agents/` ve `.claude/skills/` klasörleri
silinmiş (D) ve aynı isimler `??` olarak duruyor — gerçek dosyalar gitmiş, yerine
plugin'e bağlanan symlink konmuş. Commit'lenmediği için GitHub'da hâlâ eski
kopyalar duruyor. **Commit'lenirse o projeler plugin'e bağlanır** — bu bir karar,
mekanik bir temizlik değil.

**Commit'siz gerçek kod — `karaokai`**
40 değişiklik, `apps/denetim` altında 9 sayfa klasörü + 15 UI component + mock
data + format helper. Hiçbiri GitHub'da yok. Demo/prototip turu gibi duruyor.

**Commit'siz doküman — `adalya-IT`**
11 modül dokümanı (talep-yonetimi, envanter-yonetimi, kullanici-yonetimi, auth,
dashboard-raporlama, bildirimler, kategori-yonetimi, genel, destek-portali/db,
handoff/, PROJECT-INFO.md).

**Gerçek çift kopya — trendyol**
`trendyol-siparis` ve `trendyol-siparis-2` aynı remote'u
(`pryazilim-creative/tedarick`) ve aynı commit'i (`6f888d9`) taşıyor.
⚠️ Ama commit'siz içerikleri FARKLI: `-siparis`'te 3 ekstra dosya var
(`DISCOVERY-model-kodu-gruplama.md`, `.claude/agents`, `.claude/skills`), `-2`'de
yok. **Biri silinmeden önce o dosyalar taşınmalı.**

**Çift SANILAN ama değil — pryazilim-crm**
`pryazilim-crm` (remote: pryazilim-creative, son commit 2026-06-18) ve
`pryazilim-crm-2` (remote: karaokmert, son commit 2025-12-22). Farklı remote,
farklı geçmiş. İsim benziyor, repo ayrı — **silinmez.**

**Git'i hiç olmayan — 3 klasör**
`izmirsagliknoktasi` (içinde yalnız `apps`), `orbis_projesi` (bir `.rar` ve `.bat`
dosyaları taşıyor), `titan` (Python). Versiyon kontrolü yok, GitHub karşılığı yok.

**Bozuk durum — `marwell-template`**
Boş klasör, git'i var ama detached HEAD'de, upstream yok.

**Küçük değişiklikler (1–4 dosya, çoğu `.DS_Store` ve agent-memory)**
balkanbee · ce-teknozzle · cevizioex · demosite · durudiagnostik-new · karaokymm ·
lokumatolyesi · mucizeler-merkezi-next · platinWeb · PR-redesign ·
prproject-managment · pryazilim-crm · pryazilim-crm-2 · rundevu

**Temiz — 5 repo**
btproduct · gazi-template · pruva-medikal · prvm-web · web-template-next

## Bu iş tekrar açılırsa

Sıra bu değil ama kararı olan üç yer var, üçü de Mert'in:
1. `adalya-IT`/`yalinnetwork` symlink dönüşümü commit'lenecek mi
2. `karaokai`'deki 40 dosya nereye gidecek
3. trendyol çiftinden hangisi kalacak (önce 3 dosya taşınacak)
