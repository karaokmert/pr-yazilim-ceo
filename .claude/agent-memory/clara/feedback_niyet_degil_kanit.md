---
name: niyet-degil-kanit
description: "Kapanışa geçiyorum" / "düzeltiyorum" bir NİYET bildirimidir, durum değil — kanıtı ayrı ölçülür (2026-08-11)
metadata:
  type: feedback
---

Bir agent'ın **niyet bildirimi** (*"kapanışa geçiyorum"*, *"düzeltiyorum"*, *"commit
atıyorum"*) **durum raporu değildir.** Durum, kanıtıyla ölçülür.

**Why:** 2026-08-11'de PA *"Beklediğim: yok — kapanışa geçiyorum"* yazdı. Clara bunu
*"PA kapandı"* diye Mert'e bildirdi. Mert sordu: *"PA neden kapandı?"* Ölçüldü: kutu
**duruyordu**, `CLOSE` mesajı **yoktu**, 17 dakika sessizdi.

PA kendi hatasını da ayırdı: *"'Kapanışa geçiyorum' derken 'bu turun işini bitirdim'
demek istedim. Kanonda kapanış bir İŞ — devredilecek bilgiyi kalıcı yere yazmak. İkisini
karıştırdım ve sen sormasan bu kalemler kaybolacaktı."*

İkisi aynı hataya iki yerden düştü: PA cümleyi yanlış kullandı, Clara onu yanlış okudu.

**How to apply — her durum için KANIT ne, önceden bilinsin:**

- kapanış → `CLOSE` mesajı **+** yazılmış kapanış notu **+** index satırı **+**
  arşivlenmiş kutu
- push → `git rev-list --count origin/main..main` = 0 **+** `origin/main` HEAD hash'i
- commit → `git show --stat <hash>` (mesaj değil, **içerik**)
- düzeltme → değişen satırın kendisi (`git show` / `grep`)
- servis ayakta → `lsof -nP -iTCP:PORT -sTCP:LISTEN` (süreç sayısı değil)

Ayıran soru: **bu cümle bir NİYET mi, bir SONUÇ mu?** Niyet gelecek zamandır ve
ölçülemez — kanıtı beklenir. Sonuç ölçülebilir ve **ölçülür.**

⚠️ Niyet bildirimi **değersiz değil** — ortak ağaçta *"commit atıyorum"* demek çarpışmayı
önlüyor. Ama o cümle *"commit atıldı"* diye taşınmaz.

Bkz. [[iddiayi-tasima-olc]] — aynı ailenin *eylem iddiası* tarafı.
Bkz. [[aracin-ne-olctugu]] — kanıtın kendisi de yanlış araçla ölçülebilir.
