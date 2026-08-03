---
name: indeks-emir-tasir
description: MEMORY.md otomatik context'e girer, dosyalar girmez — indekse kural değil yalnız pointer yazılır
metadata:
  type: feedback
---

`MEMORY.md`'ye **kural, talimat ya da doktrin yazma.** Yalnız tek satır pointer:
`- [Başlık](dosya.md) — tek cümle kanca`, 150 karakteri geçmeden. Gerekçe ve detay
ayrı dosyada yaşar. İkisi birlikte yazılır — pointer'sız dosya yetim, dosyasız
pointer yalan.

**Why:** Mekanik bir asimetri var. `MEMORY.md` oturum başında **otomatik** context'e
giriyor; memory dosyaları girmiyor, `Read` gerektiriyor. Yani indekse yazılan cümle
pasif bir not değil, **davranış talimatı** — ilk cümleyi kurarken zaten uygulanmış
oluyor, hiçbir dosya açılmadan.

`skill-project` memory-management skill'inde deneyle kanıtlanmış: bir agent'ın
indeksine *"kullanıcıya X de"*, dosyasına *"Y de"* yazılmış. Agent X demiş, dosyayı
hiç açmamış, üstelik CLAUDE.md'deki gerçek adı **sessizce ezmiş** ve çelişkiyi
bildirmemiş.

Clara için sonucu doğrudan: indekse kural yazarsam kendi kanonumu, kendimin
göremediği bir yerden ezerim — ve `clara.md`'ye yazma yetkim olmamasının sebebi de
tam bu. Arka kapıdan aynı şeyi yapmış olurum.

Karar ve neyin alınmadığı: `kararlar/2026-08-03-clara-memory-disiplini.md`.

**How to apply:** Bir memory kaydı yazarken sor — *"bu satır tek başına okunduğunda
bana ne YAPTIRIR?"* Bir şey yaptırıyorsa indekse ait değil, dosyaya ait. İndeks
yalnızca *"şurada şöyle bir şey var"* der.

İlgili: [[memory-okuma-kontrolu]], [[olcum-once-oneri-sonra]]
