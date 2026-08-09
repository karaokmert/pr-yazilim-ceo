# OY v8 — yapı ölçümü (yeniden üretim girdisi)

**Ölçen:** Clara · **Tarih:** 2026-08-09 · **Yöntem:** kaynak dosya sayımı (frontmatter
`skills:` alanı + skill dizini)

**Kapsam:** yalnız **yapı** ölçüldü — hangi skill nerede, kim neyi preload ediyor.
Sahada ne açıldığı bu ölçümün konusu değil (onu PCA ölçtü, 173 oturum,
`agent-project/docs/ozel-yazilim/takim-analizi/saha-olcumu-pca.md`).

**Kaynak:** `~/.claude/plugins/marketplaces/pryazilim-agents/v8/ozel-yazilim/.claude/`
Cache (`plugins/cache/pryazilim-agents/ozel-yazilim/0.6.1`) ile **birebir aynı**
(`diff -rq` → tek fark `.in_use`). Yani yürürlükteki sürüm bu.

---

## Ölçülen sayılar

**9 agent, 971 satır body** (100–126 satır, medyan 105). Dağılım dar — uçlarda body yok.

**76 skill, 12.629 satır** (`*.md` toplamı, reference dahil).

**15 skill preload ediliyor, 61'i etmiyor.**

Preload dağılımı:
- **5 çekirdek skill 9/9 rolde:** `pr-yazilim-oy-envanteri`, `memory-management`,
  `is-akisi`, `handoff`, `behavior`
- **9 rol omurgası, her biri 1 rolde:** `backend`, `frontend`, `mobile`, `devops`,
  `quality`, `code-auditor`, `project-assistant`, `test-engineer`, `ui-designer`
- **`deploy-release` 2 rolde** (devops + qa)

Rol başına: 6 skill (7 rolde), 7 skill (devops, qa).

**Bu yapı fabrikanın `standart-cikarimi.md`'de bağımsız olarak çıkardığı desenle
birebir uyuşuyor** — çekirdek 5 + omurga + alet. Yani standart doğru okunmuş.

---

## Yanlış bulgu ve düzeltmesi — liste okuması yeterli değil

Alet katmanı listesinde üç şey şüpheli göründü ve **üçü de yanlış alarm çıktı.**
Kaydediliyor çünkü bu bulgular gereksinime yazılsaydı fabrikaya yanlış iş verilecekti.

**`impact-analiz` + `impact-analysis` — çift sanıldı, değil.** Biri PA'nın
**koordinasyon** skill'i (CA'dan analiz ister, dönüşünü değerlendirir), diğeri CA'nın
**yürütme** skill'i (tarar, çağrı grafiği çıkarır). İkisinin description'ı birbirini
adıyla anıyor. Bu tam olarak fabrikanın "uçlu desen" diye çıkardığı standardın
uygulanmış hâli.

**`pryazilim-core` — "core preload dışında" sanıldı, doğrusu bu.** Paylaşılan .NET
altyapı paketinin envanteri; birincil sahibi backend, diğer roller okumaz. Alet
katmanında olması tasarım.

**Ders:** skill adları listesinden bulgu çıkarılmaz. Ad benzerliği çift tanım
göstermiyor; description açılmadan hüküm verilemez. Ölçüm ekseni değişince bulgu da
değişiyor — PCA sahada *açılmayanı* saydı, ben *listeyi* okudum, ikisi farklı şey
gösteriyor ve ikisi de tek başına eksik.

---

## Yeniden üretim için ne anlama geliyor

**61/76 preload dışı olması tasarımın kendisi**, kazası değil. OY'nin tasarım tercihi
şuydu: omurga skill'i bir *"iş → hangi alet"* eşlemesi taşır, agent iş anında açar.

Sahada tutmadığı ölçüldü (35 skill hiç açılmamış, dokuzunda konu konuşulmuşken).
**Ama sebep ayırt edilmedi** — üç aday var (omurga tablosu okunmuyor / okunuyor ama
tetiklenmiyor / agent bildiğini sanıyor) ve üçü farklı çözüm istiyor.

Yeniden üretimde bu karar tekrar verilecek: alet katmanı kalsın mı, preload'a mı
girsin, yoksa birleştirilip azaltılsın mı. **Karar ölçüme bağlı ve ölçüm yapılmadı.**

---

## İki ölçüm çelişmiyor — eksenleri farklı

`skill-project/docs/agent-dogrulama/DENETIM-BRIEF-v8-tamamlama.md` (2026-07-31):
**634 ID · 0 yetim · 0 çift tanım · 0 kırık atıf · 102/102 cache.**

Fabrikanın saha ölçümü (2026-08-09): **574 kimlik, 352'si hiç anılmamış, 5 ölü atıf.**

Çelişki yok — biri **metin tutarlılığını** ölçtü, diğeri **saha kullanımını**. Tutarlı
bir kanon hiç okunmuyor olabilir. PAM'in kendi düzelttiği hatanın aynısı:
*mekanizmanın varlığı çalıştığını göstermez.*

**Ama bir ders çıkıyor ve gereksinime girmeli: ölçüm ekseni dar olursa "0" yanıltır.**

"0 kırık atıf" ölçümü **dosya atıflarını** taradı; **MCP araç adlarını taramadı.**
Kaynaktan doğrulandı — kanonda üç yerde `mcp__maestro__*` yazıyor, doğru ad
`mcp__plugin_ozel-yazilim_maestro__*` ve o adın kanonda **sıfır kullanımı var**:

- `skills/mobile-release/SKILL.md:66` (smoke test adımı)
- `skills/mobile-release/SKILL.md:68` (izin kontrolü)
- `skills/e2e-verification/references/maestro-mekanik.md:53` (**sorun giderme
  talimatı** — "araçlar görünmüyorsa şu izni kontrol et")

Üçüncüsü en zararlısı: talimat agent'a **yanlış deseni arattırıyor**, agent bulamıyor,
*"iznim yok"* sonucuna varıyor. Oysa izin var, adı başka. **Talimat kendi amacının
tersini üretiyor.**

Aynı ders PCA'nın ölçümünde de var: ham metinde arayınca on beş konunun on beşi
"geçiyor" çıkmış, eşleşmelerin bir kısmı agent'ın kendi description'ından geliyormuş —
ekseni daraltıp yeniden ölçmüş. **İki bağımsız vaka, aynı arıza: dar eksen "temiz"
gösteriyor.**

---

## Açık — ölçülmedi

**Rol başına oturum sayısı** (PCA da ölçemedi — `subagent_type` sayımı güvenilmez,
agent'lar terminal profilinden doğrudan açılıyor olabilir).

**Reference katmanının rol dağılımı** — 77 reference dosyasının hangi skill'e bağlı
olduğu bu ölçümde çıkarılmadı.

**Kural kimliklerinin skill bazında dağılımı** — 574 kimlik var, hangi skill'de kaç
tane olduğu sayılmadı.
