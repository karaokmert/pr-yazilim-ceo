# Fabrika düzeni — UYGULANDI (6 karar)

**Süre:** 2026-08-04 → 2026-08-11 · **Doğrulandı:** 2026-08-13

## 1. Ne yapıldı

**Fabrika `skill-project`'e taşındı** (11 Ağustos). `agent-project` tarihçe oldu —
dosyalar yerinde ama **kanonu yürürlükte değil.** Ölçüldü: `skill-project/team/` var.

**v7 symlink'leri kaldırıldı** (4 Ağustos): yerel agent/skill kopyaları emekli edildi,
tek kaynak plugin oldu.

**Fabrika denetimi kapandı** (6 Ağustos): dört eksende ölçüm yapıldı, düzenlemeler
listelendi.

**PAM davranış kuralları netleşti** (7 Ağustos, üç karar):
`PAM-WRITE-DOCS-ONLY` behavior'a taşındı · `ISD-STAY-IN-ROLE` bulgusu düştü ·
zincir kapanışı PAM'e döner.

## 2. Neden öyle

**Taşınma neden gerekti:** iki repoda aynı dosyaların kopyaları vardı ve hash bazında
özdeş olabiliyorlardı. Ayıran şey içerik değil **statü** — hangisinin yürürlükte
olduğu belirsizdi. Tek yer, tek kanon.

**Symlink neden kalktı:** yerel kopya plugin'den ayrışınca agent hangi sürümü okuduğunu
bilmiyor. Ölçüldü: v7 kopyası okunup *"OY ekibinde şu araç yok"* denildi — yürürlükteki
v8'de o alan hiç yoktu.

## 3. Nerede yaşıyor

`/Users/karaok/p/ozel-yazilim/skill-project/` — fabrika ekibi (PAM/PAD/PQA/PCA),
`team/` altında üretilen takımlar, `tools/kanal/` betikleri.

## 4. Bilinmesi gereken

⚠️ İki repoda **aynı dosyaların kopyaları duruyor.** Bir adres verirken hangisi olduğu
tam yazılır; fark varsa **`skill-project`'teki doğrudur.**

---
> 6 karar dosyası özetlendikten sonra `.trash`'e alındı.
