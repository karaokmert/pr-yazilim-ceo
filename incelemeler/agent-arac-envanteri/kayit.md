# Agent'lara verilebilecek araçlar — envanter ve fabrika karşılaştırması

Tarih: 2026-08-03 (akşam)

Mert sordu: *"Agent'lara verebileceğimiz tool'lar neler var?"*

İki kaynak kullanıldı ve **ayrı tutuluyor**: (a) Claude Code dokümantasyonu
(`claude-code-guide` ajanı taradı — **okuma**, ölçüm değil), (b) diskteki gerçek agent
tanımları (**ölçüm** — grep).

## Ölçüm — bugün kim ne kullanıyor

**Fabrika ekibi** (`agent-project/.claude/agents/`), dördü de MCP'siz:

- `pr-agent-manager` — Read, Grep, Glob, Write, Edit, WebFetch, Skill, Task
- `pr-agent-developer` — Read, Grep, Glob, Write, Edit, Bash, Task, Skill
- `pr-agent-qa` — Read, Grep, Glob, Bash, Skill
- `pr-agent-context-analyst` — Read, Grep, Glob, Bash, WebSearch, WebFetch, Skill

Yani 7 farklı araç kullanılıyor; **hiçbirinde MCP aracı yok.**

**OY ekibi** (plugin cache, `pryazilim-agents/ozel-yazilim/agents/`) tersini yapıyor —
MCP var, `Skill` yok:

- `test-engineer` — Read, Glob, Grep, Bash + 6 Playwright + 3 Maestro MCP
- `backend-developer` — Read, Write, Edit, Glob, Grep, Bash + 6 Playwright MCP
- `frontend-developer` — aynısı + 6 Playwright MCP
- `mobile-developer` — Read, Write, Edit, Glob, Grep, Bash + 3 Maestro MCP
- `ui-designer` — Read, Write, Edit, Glob, Grep + 4 Figma MCP
- `qa-engineer`, `devops-engineer`, `code-auditor` — yalnız temel araçlar

**Bulgu: `Skill` aracı fabrikanın dördünde var, OY ekibinin hiçbirinde yok.**
Bu potansiyel olarak önemli — bkz. aşağıda "En kritik açık".

Mekanik not: plugin cache'inde OY agent tanımlarının çok sayıda kopyası duruyor ve
çoğunda `tools:` alanı hiç yok. Eski sürüm kalıntısı olabilir; **doğrulanmadı.**

## Doküman okuması — 46 built-in araç

Kaynak: `code.claude.com/docs/en/tools-reference.md` ve `sub-agents.md`.
**Bu bir okuma, ölçüm değil** — aşağıdaki "güvenilirlik" başlığına bakılmadan
kullanılmamalı.

Fabrikanın kullanmadığı, işe yarayabilecek olanlar:

**Görev/paralellik:** `TaskCreate`, `TaskGet`, `TaskList`, `TaskUpdate`, `TaskStop`,
`Monitor` (arka plan komut takibi), `Workflow` (dinamik iş akışı orkestrasyonu).
`TodoWrite` deprecated sayılıyor, yerine `Task*` ailesi.

**İletişim:** `SendMessage` (agent-agent/peer mesajlaşma), `AskUserQuestion`,
`PushNotification`, `SendUserFile`, `ReportFindings` (kod inceleme sonucu için).

**Zamanlama:** `CronCreate`, `CronDelete`, `CronList`, `ScheduleWakeup`.

**Kod/ortam:** `LSP` (dil sunucusu — tip bilgisi, referans bulma), `PowerShell`,
`NotebookEdit`, `EnterWorktree`/`ExitWorktree` (izole çalışma kopyası),
`EnterPlanMode`/`ExitPlanMode`.

**Keşif:** `ToolSearch`, `ListMcpResourcesTool`, `ReadMcpResourceTool`,
`WaitForMcpServers`.

**Diğer:** `Artifact`, `EndConversation`, `RemoteTrigger`, `ShareOnboardingGuide`,
`Agent` (= Task'ın yeni adı).

## Sözdizimi (doküman)

`tools:` hem virgüllü liste hem YAML dizisi kabul ediyor.
**Boş bırakılırsa tüm araçlar verilir** — hiçbiri değil, hepsi.
Kısıtlama için ayrı alan var: `disallowedTools: Write, Edit`.
MCP jokerleri yalnız `disallowedTools`'ta: `mcp__server`, `mcp__*`.
Agent frontmatter'ında `isolation: worktree` mümkün.
Agent iç içe çağrı derinliği varsayılan 3 katman.

## Güvenilirlik uyarısı — doküman ile gerçek çelişiyor

Rapor şunu iddia ediyor: *"`skills:` alanı skill içeriğini başlangıçta context'e
enjekte eder (pre-loading)."*

**Bu bugünkü ölçümle çelişiyor.** `incelemeler/skill-preload-bulgusu/kayit.md`:
`skills:` listesi gövdeyi enjekte etmiyor (`anthropics/claude-code#25834`), üç kuşakta
beş agent'la sınandı. `backend-developer` beklenen ~11.500 kelimenin 1.067'sini
görüyordu.

Sonucu genel bir kural: **bu listedeki hiçbir araç ölçülmeden kanona alınmamalı.**
Doküman bir aracın var olduğunu söylüyor; o aracın bir subagent'ta çalıştığını
söylemiyor.

## En kritik açık — `Skill` aracı OY ekibinde yok

İki gerçek yan yana:

**Bir:** `skills:` frontmatter'ı çalışmıyor (ölçülmüş).
**İki:** `Skill` diye ayrı bir araç var, agent çalışma anında skill çağırabiliyor
(dokümanda yazıyor) — ve fabrikanın dördünde tanımlı, OY ekibinin hiçbirinde yok.

Eğer `Skill` aracı gerçekten çalışıyorsa, preload arızasının çözümü olabilir ve OY
ekibinde eksik. Fabrika hook'la çözdü; OY tarafında `Skill` aracının olmaması ya
bilinçli bir tercih ya bir boşluk.

**Bu bir hipotez, ölçüm değil.** Ayıran ölçüm: `Skill` aracı verilmiş bir subagent'a
isimli bir skill'i çalışma anında yükletip içeriğinden bir soru sormak. Yüklüyorsa
mekanizma var; yüklemiyorsa doküman yine yanlış.

## Fabrikaya MCP verilmemiş — sebep bilinmiyor

Fabrika ekibi agent üretiyor, tarayıcı ya da mobil cihaz sürmüyor — Playwright/Maestro
gerekmemesi makul. Ama `LSP` (tip bilgisi, referans bulma) bir kanon denetçisi için
anlamlı olabilir ve yok.

Mert'e soruldu, cevap alınmadı: MCP'siz olması tercih mi, boşluk mu.

## Karar bekleyen

Hiçbir araç önerilmiyor — çünkü öneri vermek için ölçüm yok. Sıradaki adım tek bir
şey: **`Skill` aracının bir subagent'ta gerçekten çalışıp çalışmadığını ölçmek.**
Diğer 39 aracın hiçbiri o ölçüm yapılmadan konuşulmamalı.
