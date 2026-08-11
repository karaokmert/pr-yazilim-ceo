---
name: claude-md-ne-icerir
description: CLAUDE.md bir projenin tarifi ve çalışma kuralıdır — envanter, sayım, liste girmez; agent'ın repoyu tarayıp göreceği şey yazılmaz
metadata:
  type: feedback
---

Bir `CLAUDE.md`'ye **agent'ın repoyu tarayarak göreceği hiçbir şey yazılmaz.**
Skill adı listesi, dosya sayımı, klasör envanteri, "şu skill şunu yapar"
tarifi — hepsi dışarıda kalır.

İçine giren dört şey: **proje bilgisi** (bu repo ne, neden var) ·
**çalışma kuralları** (burada nasıl çalışılır) · **riskli noktalar** ·
**bu projede çalışırken dikkat edilecekler**.

**Why:** Mert'in kuralı (2026-08-11): *"Claude md bir projenin tarifi ve
çalışma kuralıdır. Bu nedenle sayısal şeyler içinde olmaz — agent zaten
repoyu tarayıp görebileceği şeyleri claude.md'ye yazmayız."*

İki sebebi var. Birincisi gereksizlik: `ls .claude/skills/` agent'ın elinde,
aynı bilgiyi kimlik kartına kopyalamak her okumada taşınan ölü yük.
İkincisi **eskime**: envanter diskle birlikte değişir, metin değişmez —
ve eskiyen envanter yanlış bilgi verir, boş bilgiden kötüdür.

**How to apply:** Bir `CLAUDE.md` satırı yazarken sor — **bunu agent
`ls`/`grep` ile görebilir mi?** Görebiliyorsa satır çıkar.

Ayıran örnek, aynı konudan iki cümle:

> envanter (YAZILMAZ): *"emekli aile: `uretim-standardi` · `uretim-akisi` ·
> `agent-production-standard` · … (on sekiz ad)"*
> risk (YAZILIR): *"bu repoda iki skill ailesi yan yana duruyor ve hangisinin
> yürürlükte olduğu belirsiz — birine dayanmadan önce sorulur."*

Birincisi `ls` ile görünür ve bir hafta sonra yanlış olur. İkincisi `ls` ile
**görünmez** (iki aile aynı klasörde eşit görünüyor) ve eskimez.

Ölçüldü aynı gün: Clara `CLAUDE.md` §5'e on sekiz emekli skill adını yazdı,
sonra listeyi *"ölçülmemiş"* diye sorguladı — yanlış itiraz. Sorun listenin
ölçülmemiş olması değil, **kimlik kartına envanter girmesiydi.** Mert kesti.

İlgili: [[dogru-katmana-yaz]] — hangi bilginin hangi dosyaya gittiği; bu
kayıt onun `CLAUDE.md` özel hâli.
