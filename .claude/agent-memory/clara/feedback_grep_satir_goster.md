---
name: grep-satir-goster
description: grep -l dosya adı verir cevap vermez — varsayılan satır göstermek; Mert'in "sürekli farklı bulgu çıkıyor" şikayetinin sebebi buydu
metadata:
  type: feedback
---

**`grep -l` kullanma, eşleşen satırı göster.** `-l` dosyaların içine bakar ama
sana yalnız dosya adını söyler — cevabı görmek için dosyaları açman gerekir.

**Why:** Mert 2026-08-16'da *"grep çok riskli oluyor, sürekli farklı bulgu
çıkıyor"* dedi. Ölçüldü, sebep grep değil çağırma biçimiydi. Aynı soru
(*"SendMessage'ı nasıl kullanmışız"*) iki biçimde soruldu:

- `grep -ril` → **11 dosya adı**, hiçbiri cevabı göstermiyor
- `grep -rih` → **47 satır**, ilk 25'inde cevap **ve bir çelişki** göründü,
  hiçbir dosya açılmadan

O çelişki dosya adı listesinde görünmüyordu — ve Clara o sabah `-l` ile bakıp
Mert'e yanlış bilgi vermişti (*"SendMessage goat'ta denenmedi"* — denenmişti).

İkinci sebep: **kelime tahmini.** grep aradığın kelimeyi bulur, aradığın şeyi
değil. Soruyu kelimeye çevirirken tahmin yürüyor; her tahmin farklı küme
döndürüyor. Ölçüldü aynı gün: dar kalıp doğru dosyayı **hiç bulamadı** (dosya
tam o klasördeydi), geniş kalıp **sekiz sonucun içine gömdü.**

**How to apply:** Varsayılan satır göster (`-h` ya da satır veren biçim).
`-l` yalnız iki durumda doğru: **sayım** (kaç dosya etkileniyor) ve **toplu
düzenleme girdisi** (hangi dosyaları düzenleyeceğim). Çıktı çok gelirse kalıbı
genişletme — **dizinle daralt, ikinci kelimeyle boru hattında filtrele, `head`
ile kes.** Tek kelimeyle ara, kalıpla değil: kalıp senin cümle kurgunu dayatır.

⚠️ Vektör arama (Qdrant) **kapalı** — Mert kapattı, kanondan çıkarıldı.
Tam kanon: `~/.claude/skills/arama-disiplini/SKILL.md`

İlgili: [[dosya-degil-sorgu]] · [[olcum-yerine-yorum]]
