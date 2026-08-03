---
name: olcum-once-oneri-sonra
description: Bir eksiklik teşhis edip çözüm önermeden önce ilgili kanonu oku — kural çoğu zaman zaten var ve önerdiğin şeyi gerekçesiyle yasaklamış olabilir
metadata:
  type: feedback
---

Bir eksikliğin çözümünü önermeden önce, o konudaki mevcut kanonu **oku**. Öneriyi
okumadan verirsen zaten yasaklanmış bir şeyi tavsiye edebilirsin.

**Why:** 2026-08-03'te ölçüldü. Fabrikada skill preload boşluğunu teşhis edip
*"skill adlarını CLAUDE.md'ye agent başına isim isim yaz"* diye öneri verdim. Sonra
`agent-project/.claude/skills/dagitim/SKILL.md` okundu — `DAG-SHIP-PRELOAD-HOOK` skill
adlarını script'e/metne gömmeyi **gerekçesiyle** yasaklamış (iki kaynak sorunu:
frontmatter değişir, kopya eskir, kimse fark etmez). Önerimi kendim geri çekip kayda
düzeltme yazmak zorunda kaldım.

Aynı turda ikinci bir örnek: teşhisim *"kural agent'a elinde olmayan bilgiye dayanan iş
veriyor"*du ve doğruydu — ama o teşhis zaten `DAG-SHIP-PRELOAD-HOOK` içinde birebir
yazılıydı. Yani ekibin bilmediğini sandığım şeyi ekip biliyordu; eksik olan kuralın
**kapsamı**ydı, içeriği değil.

**How to apply:** Bir agent/skill/kural eksikliği teşhis ettiğinde iki soruyu ayır —
*"kural var mı"* ve *"kural bu durumu kapsıyor mu"*. İkincisi çoğu zaman gerçek cevap,
ve bulunması için kanonu açmak gerekiyor. Öneri vermeden önce ilgili SKILL.md'yi grep'le;
öneri verdikten sonra okuyup geri çekmek kaydı kirletiyor.

İlgili: [[cevap-uzunlugu]]
