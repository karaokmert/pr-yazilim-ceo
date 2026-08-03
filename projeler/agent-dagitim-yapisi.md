# Agent'lar diskte nasıl duruyor — dağıtım haritası

Tarih: 2026-08-03 · Ölçüm: `find`, `ls -la`, symlink hedefleri takip edildi

Mert: *"sen bizim yapımızı öğren diye taratıyorum, çöpleri sistemi güncelleyeni gör."*

Bu dosya **referans** — bir agent'ı ya da kanonu okumadan önce hangi kopyanın yürürlükte
olduğunu buradan doğrula.

## Yürürlükteki kaynak — plugin

Agent ve skill'ler plugin'den gelir, projeye kopyalanmaz.

**Marketplace (asıl kaynak):** `~/.claude/plugins/marketplaces/pryazilim-agents/`
— altında `v7/` ve `v8/` var. **`v8/` yürürlükte**, içinde iki aile:
`v8/ozel-yazilim/` (9 agent) ve `v8/websitesi/` (7 agent).

**Cache (yüklü sürümler):** `~/.claude/plugins/cache/pryazilim-agents/ozel-yazilim/`
— sekiz sürüm yan yana duruyor: 0.1.0, 0.3.0, 0.4.0, 0.4.1, 0.5.1, 0.6.0, 0.6.1.
Aynı dosyanın (`backend-developer.md`) diskte **9 kopyası** var.

**Fabrika ayrı:** `agent-project/.claude/agents/` — dört agent (PAM, PAD, PQA, PCA).
Plugin'den gelmiyor, repoda yaşıyor. Bu bilinçli: fabrika kendi reposunda üretiliyor.

## Araç kısıtlaması iki ailede farklı

Fabrika `tools:` kullanıyor (beyaz liste). v8 OY/websitesi `disallowedTools` kullanıyor
ve içinde yalnız `Workflow` var — pratikte kısıt yok.
Ayrıntı: `incelemeler/agent-arac-envanteri/kayit.md`.

## Eski kuşak kalıntıları — silinmedi, "şimdilik kalsın" (Mert, 2026-08-03)

**Global symlink'ler — `~/.claude/agents/`, 20 tane, hepsi symlink.**
Hepsi `skill-project`'e bakıyor (yürürlükteki plugin'e değil):

- **Dokuzu `v7/ozel-yazilim/`'e:** backend-developer, code-auditor, qa-engineer,
  test-engineer, ui-designer, devops-engineer, frontend-developer, mobile-developer,
  project-assistant
- Yedisi `v8/websitesi/`'ye: web-* ailesi
- Dördü `skill-project` köküne: agent-generator, ag-qa, skill-manager, task-manager

**Bunun görünür sonucu:** oturum açıldığında agent listesinde hem `ozel-yazilim:backend-developer`
(plugin, v8) hem çıplak `backend-developer` (symlink, **v7**) görünüyor. İkisi
çağrılabilir. Yanlış aileyi çağırma riski `~/.claude/CLAUDE.md`'de yazılı bir endişe;
bu mekanizma tam onu üretiyor.

**Proje içi kopyalar — 27 dosya, hepsi gerçek dosya (symlink değil):**

- `web-sitesi/zikirvakti/.claude/agents/` — 9 dosya. Ayrıksı: içinde plugin'de hiç
  olmayan `maintenance.md` ve `project-manager.md` var, başka bir kuşaktan.
- `web-sitesi/mucizeler-merkezi-next/` — 6 dosya
- `web-sitesi/lokumatolyesi/` — 6 dosya
- `web-sitesi/karaokymm/` — 6 dosya

Son üçünde `code-auditor.md` (5477 byte) ve `qa-engineer.md` (7246 byte) **byte-byte
aynı** — kopyala-yapıştır çoğaltma. Boyutlar plugin sürümünden çok küçük, yani plugin
öncesi kuşak.

**`skill-project/.claude/agents/`** — iki eski fabrika kopyası duruyor
(`pr-agent-manager.md`, `pr-agent-qa.md`); yürürlükteki hâlleri `agent-project`'te.
Ayrıca iki symlink `../../ag-agent/agents/`'e bakıyor.

## Örüntü — her sürüm geçişi kopyasını bırakıyor

v7 symlink'leri, `web-sitesi`'ndeki 27 dosya, `skill-project`'teki iki fabrika kopyası,
cache'teki sekiz sürüm. Hiçbiri silinmemiş.

**Ve bunun ölçülmüş bir bedeli var.** 2026-08-03'te Clara iki kez yanlış cevap verdi:
(1) `backend-developer.md`'nin v7 kopyasını okuyup *"OY ekibinde `Skill` aracı yok"*
dedi — yürürlükteki v8'de `tools:` alanı hiç yoktu; (2) yalnız `tools:` arayıp
`disallowedTools`'u aramadı.

Yani kalıntı masum değil: **grep dosyanın yolunu değil içeriğini getiriyor**, ve okuyan
hangi kuşağı okuduğunu bilmiyorsa yanlış sonuç üretir. Bir agent da aynısını yapar.

## Okuma kuralı — bundan sonra

Bir agent tanımı ya da kanon okunacaksa **yolu doğrula:**

- Yürürlükteki OY/websitesi agent'ı → `~/.claude/plugins/marketplaces/pryazilim-agents/v8/`
- Yürürlükteki fabrika agent'ı → `~/p/agent-project/.claude/agents/`
- `v7/` yolu geçen her şey **tarihçe**, yürürlükte değil
- `skill-project` yolu geçen her şey **tarihçe** (`CLAUDE.md` → "Bakılan yerler")
- `web-sitesi/*/.claude/agents/` → plugin öncesi kalıntı

`find` ile arama yapılıyorsa sonuç sayısı 1'den fazlaysa **hangisi olduğu söylenmeden
sonuç kullanılmaz.**
