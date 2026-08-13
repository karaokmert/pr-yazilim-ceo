# Yerel agent/skill symlink'leri kaldırıldı — v7 emekli edildi

Tarih: 2026-08-04

Mert: *"Bence artık onları kaldıralım. skill-project içinde hepsi var zaten,
symlink'lerini kaldıralım `.claude` içinde plugin olmayan. Artık OY7'leri emekli
edelim."*

## Neden — ölçülmüş maliyet

Bir OY agent'ı çağrıldığında açılış maliyeti **145.047 token** ölçüldü (`code-auditor`,
tek tur, hiç araç çağırmadan). Bileşimi:

- `skill_listing` ~23.700 token — **197 skill'in açıklaması**
- `agent_listing_delta` ~10.100 token — agent listesi
- `deferred_tools_delta` ~7.800 token
- `hook_success` ~3.700 token (preload hook'unun metni)

197 skill açıklamasının **6'sının gövdesi** yükleniyor (hook'un yüklettiği kanon), geri
kalan 191'i hiç kullanılmıyor. Mert'in ifadesi: *"hiçbiri gerekli değil, skill'lerin
referansları agent'ların ve skill'lerin içinde oluyor."*

Ve bu maliyet **her agent çağrısında `cache_create` olarak** ödeniyor — yani tam bedel
+ %25. Ölçüm: bir açılışın bedeli, aynı bağlamı 12 kez önbellekten okumaya eşit.

## Silinen — 50 symlink, hepsi symlink (gerçek dosya yok)

Doğrulandı: `find ~/.claude/skills ~/.claude/agents -maxdepth 1 ! -type l` boş döndü.
Hedefler `skill-project` içinde duruyor; symlink silmek hedefi silmiyor.

**`~/.claude/skills/` — 30 symlink.**

v8 plugin'inde karşılığı olanlar (12, kayıpsız): `backend`, `behavior`, `clickup`,
`database`, `deploy-release`, `devops`, `figma`, `frontend`, `handoff`,
`memory-management`, `mobile`, `quality`.

Karşılığı olmayanlar (18) — iki gruba ayrılıyor:

*AG ailesi (8)* — `agent-generator`, `ag-qa`, `agent-production-standard`, `cascade`,
`drift-tarama`, `ground-truth`, `memory-terfi`, `teshis`. Eski agent üretim hattı;
fabrika (`agent-project`) onların yerine geldi. Gerçekten emekli.

*v7 iş skill'leri ve yardımcılar (10)* — `testing`, `planning`, `ui-design`,
`mobile-testing`, `maintenance`, `finish`, `pause`, `environment`, `skill-health`,
`memory-consolidate`.

**Şerh:** bu 10'unun v8'de **adı değişmiş** olabilir — v8'de `e2e-verification`,
`test-engineer`, `project-planning`, `ui-designer` var. İçeriğin taşınıp taşınmadığı
**ölçülmedi.** Bir eksik çıkarsa `skill-project`'ten geri getirilir.

**`~/.claude/agents/` — 20 symlink.** Dokuzu `v7/ozel-yazilim/`'e bakıyordu
(`backend-developer`, `code-auditor`, `qa-engineer`, `test-engineer`, `ui-designer`,
`devops-engineer`, `frontend-developer`, `mobile-developer`, `project-assistant`),
yedisi `v8/websitesi/`'ye, dördü `skill-project` köküne (`agent-generator`, `ag-qa`,
`skill-manager`, `task-manager`).

Bunların silinmesinin ayrı bir gerekçesi var: oturum listesinde hem
`ozel-yazilim:backend-developer` (plugin, v8) hem çıplak `backend-developer` (symlink,
**v7**) görünüyordu ve ikisi de çağrılabiliyordu. `~/.claude/CLAUDE.md`'deki *"yanlış
aileden agent çağırma"* endişesini tam bu mekanizma üretiyordu.

## Ölçülen bir kaza — v7 sessizce okunuyordu

`goat` projesinde bugün çalışan `project-assistant` oturumu (`ff6e7d83`,
08:46→20:37) incelendi. Agent hook'un talimatıyla altı skill yükledi ve dördünün yolu
`~/.claude/skills/...` idi — yani **v7 gövdesi.**

En büyüğü `behavior`: 12.878 token, v7 kanonu. Aynı adda bir `behavior` v8 plugin'inde
de var. Yani agent v8 ailesinden çağrıldı ama **v7 kanonunu okudu.**

Bu, symlink temizliğinin asıl gerekçesi: maliyet ikincil, **yanlış kanon okumak
birincil.**

## Yürürlükte kalan

**Plugin:** `~/.claude/plugins/marketplaces/pryazilim-agents/v8/` — OY 76 skill + web 16.
**Fabrika:** `/Users/karaok/p/agent-project/.claude/` — 4 agent + 5 skill, repoda yaşıyor.
**Clara:** `/Users/karaok/p/pr-yazilim-ceo/.claude/agents/clara.md`.

`~/.claude/skills/` ve `~/.claude/agents/` **boş.**

## Geri alma

Symlink listesi `/tmp/silinen-skill-symlinkleri.txt` ve
`/tmp/silinen-agent-symlinkleri.txt` dosyalarına yazıldı (geçici — kalıcı kayıt bu
dosyadaki listelerdir). Hedefler `skill-project` içinde duruyor; bir symlink gerekirse
`ln -s <hedef> ~/.claude/skills/<ad>` ile geri gelir.

## Ölçülmeyen — açık kalan

**742 `SKILL.md`** var plugin cache'inde; yürürlükte olması gereken 92. Yerel 30'u
silmek `skill_listing`'i 30 azaltır, **167 kalır.** Asıl fatura cache'teki eski
sürümlerde ve resmi plugin'lerde (63 skill).

Bir sonraki adım: hangi plugin kaç skill yüklüyor, hangileri kaldırılabilir.
