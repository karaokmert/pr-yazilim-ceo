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

**OY ekibi (v8) — hiçbirinde `tools:` alanı YOK.** Yani doküman kuralı gereği
**46 aracın hepsine sahipler**, `Skill` dahil.

Ölçüm: `backend-developer.md`'nin diskteki 9 kopyası tarandı. `tools:` alanı yalnız
**v7** kopyasında var (`marketplaces/pryazilim-agents/v7/`, 415 satır). v8'in tüm
sürümlerinde (0.1.0 → 0.6.1 ve `marketplaces/.../v8/`) alan hiç yok.

v7'deki hâli (emekli kanon, referans olarak):
`Read, Write, Edit, Glob, Grep, Bash` + 6 Playwright MCP. `test-engineer`'da ayrıca
3 Maestro, `ui-designer`'da 4 Figma MCP vardı; `qa-engineer` ve `code-auditor`'a
`Write`/`Edit` verilmemişti.

**v8 kısıtı `disallowedTools` ile yapıyor** (Mert'in tespiti, sonra ölçüldü) — ve
içinde tek bir şey var:

- OY ailesi, dokuz agent'ın dokuzunda da: `disallowedTools: Workflow`
- Websitesi ailesi, yedi agent: `disallowedTools:` **boş** — hiçbir kısıt yok

Yani `Workflow` dışında **hiçbir araç kapalı değil.** `qa-engineer` ve `code-auditor`
`Write`, `Edit`, `Bash`, `Task`, `Skill` dahil her şeye sahip.

### Bu kaydın ilk hâli yanlıştı — düzeltme notu

İlk yazımda *"OY ekibinde `Skill` aracı yok, bu bir açık"* denmişti. **Yanlış.**
Sebep: grep sonucunda v7 kopyası da listeye karışmıştı ve yürürlükteki hâl sanıldı.
Ayrıca yalnız `tools:` arandı, `disallowedTools` hiç aranmadı — yani ölçüm yarımdı ve
yarım ölçüm yanlış sonuç verdi.

Mert itiraz etti (*"OY 8'de yok ama disallow'da da değil"*, sonra *"oraya
yazdıklarımız aktif oluyordu, biz disallow'u kullandık"*) ve ikisi de ölçümle
doğrulandı.

Ders, bugün kanona eklenen kuralın bir başka biçimi: kaynağa gitmek yetmiyor,
**hangi kaynağa** gidildiğini kontrol etmek gerekiyor. Aynı dosyanın 9 kopyası varsa
"okudum" bir kanıt değil. Ve bir alanı aramak, **onun karşıtını aramamak** demek
değil.

### Asimetri — iki ekip iki farklı yöntem

Fabrika `tools:` kullanıyor (**beyaz liste** — yalnız izin verilenler),
OY/websitesi `disallowedTools` kullanıyor (**siyah liste** — yalnız yasaklananlar).

Aradaki fark gelecekte ortaya çıkar: Claude Code yeni bir araç eklediğinde beyaz liste
onu **otomatik kapatır**, siyah liste **otomatik açar.** Yani OY ekibi bir sonraki
sürümün getirdiği her aracı sormadan alır.

Bu bir arıza değil ama bir tercih ve tercihin kaydı bulunamadı.

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

## Asıl açık — kural metne kaldı, mekanizma kalmadı

v7 her agent'ın aracını tek tek sayıyordu. v8 `disallowedTools`'a geçti ve içine
yalnız `Workflow` yazdı — yani pratikte **kısıt kalmadı.**

Somut sonuç: v7'de `qa-engineer` ve `code-auditor`'a `Write`/`Edit` verilmemişti,
*"kod yazmazsın"* kuralı **mekanik olarak** engelliydi. v8'de ikisi de yazabiliyor.
`code-auditor`'ın description'ında büyük harfle *"KOD YAZMAZSIN"* yazıyor ve bunu
tutan tek şey artık o cümle.

Bu bir arıza mı, bilinmiyor. İki okuma var:

**Bilinçli tercih olabilir.** Araçla kısıtlamak bakım maliyeti getirir — bir agent'ın
yeni bir araca ihtiyacı olduğunda liste güncellenmeli. v8'in tasarım yönü buydu.
Mert'in ifadesi bu yönü destekliyor: *"oraya yazdıklarımız aktif oluyordu, biz
disallow'u kullandık"* — yani `tools:` alanının davranışı sorun çıkarmış.

**Ama kısıtın kalkması ayrı bir karar.** `disallowedTools`'a geçmek bir şey,
o listeyi tek satırda bırakmak başka şey. İkincisinin gerekçesi bulunamadı.

**Neden önemli:** v8'in ölçülmüş arızası kuralların davranışa dönüşmemesiydi
(preload). O mekanik çözüldü. Ama araç kısıtı da bir mekanizmaydı ve o hâlâ yok —
yani *"denetçi kod yazmaz"* bugün yalnız agent'ın kurala uymasına bağlı, hiçbir
teknik engel yok.

**Karar Mert'te:** `Write`/`Edit`'in QA ve CA'dan alınması gerekli mi? Alınırsa
`disallowedTools: Workflow, Write, Edit` yeterli — tek satır, dokuz dosya.

## Fabrikaya MCP verilmemiş — sebep bilinmiyor

Fabrika ekibi (`agent-project`) `tools:` alanını **kullanıyor** — yani orada kısıt
bilinçli. Ama MCP aracı hiç yok.

Agent üretiyorlar, tarayıcı ya da mobil cihaz sürmüyorlar — Playwright/Maestro
gerekmemesi makul. Ama `LSP` (tip bilgisi, referans bulma) bir kanon denetçisi için
anlamlı olabilir ve yok.

Mert'e soruldu, cevap alınmadı: MCP'siz olması tercih mi, boşluk mu.

## Karar bekleyen

Hiçbir araç önerilmiyor — öneri vermek için ölçüm yok.

**Birinci soru (Mert'te):** v8'de `tools:` alanının kaldırılması karar mı, kayıp mı?
Cevap "kayıp" ise `qa-engineer` ve `code-auditor`'ın yazma yetkisi gerçek bir risk —
denetçi düzeltme yapabilir hâle gelmiş ve bunu tutan tek şey kanon metni.

**İkinci soru (ölçüm gerektirir):** listedeki araçların hangileri bir subagent'ta
gerçekten çalışıyor? Doküman `skills:` konusunda yanlış çıktı; aynı kaynağın diğer
iddiaları da ölçülmeden kanona alınmamalı.
