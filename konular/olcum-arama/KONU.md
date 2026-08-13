# Ölçüm ve arama

> Hangi araçla aranır (grep/vektör/Qdrant), ölçüm disiplini, vektörün körlükleri.

> **Bu dosya bu konunun TEK adresidir.** Bir iş başlarken burası açılır;
> ne yapıldı, kaç kez değişti, hangi karar alındı — hepsi aşağıda sırayla.
> Yeni bir şey olduğunda buranın SONUNA yazılır.

---

## ⚠️ ÖNCE BUNLARI BİL

**1. Üç araç, üç soru tipi:** bildiğin kelime → `grep` · niyet sorusu → vektör ·
liste sorusu → `ls`. Yanlış araç **sessizce** yanlış cevap verir.

**2. Vektörün üç körlüğü:** çıktısı cevap değil **adres** · **skor alakayı ölçmez** ·
eskimiş kayıt soruya daha benzer görünür (sorunu ayrıntılı anlatır; taze kayıt
*"çözüldü"* diye kısa geçer).

**3. Bir kayıt geçersizleştiyse kaydın İÇİNE yazılır** — haritaya yazmak yetmez.
Ölçüldü: `skill-preload-bulgusu` haritada *"eskimiş"* etiketliydi, vektör aramada
**birinci** geldi (0.670), taze kayıt ikinci (0.651).

**4. Sayı verirken neyi saydığını söyle.** *"111 kural var"* eksik cümle;
*"111 kural var, şablon örneği olan biri elendi"* tam.

---

## Kararlar (2)

**2026-08-05 — Qdrant MCP: bu oda ayrı bir vektör alanı kullanır**
pr-yazilim-ceo odasının Qdrant MCP'si 768 boyutlu, kendi collection'ında çalışır. Buradaki notlar sunucudaki mevcut 1024 boyutlu ekosisteme katılmaz — ekibin aramasında çıkmaz, çıkması da istenmiyor.
→ `konular/olcum-arama/kararlar/2026-08-05-qdrant-mcp-ayri-alan.md`

**2026-08-06 — Arama disiplini: grep mi vektör mü, ve vektörün üç körlüğü**
Tarih: 2026-08-06 Karar: Clara (ölçüme dayalı), Mert'in tetiğiyle Kanona giren yer: .claude/agents/clara.md → "Kayıtlar" bölümü + yeni "Ararken" alt bölümü
→ `konular/olcum-arama/kararlar/2026-08-06-arama-disiplini.md`


## İncelemeler (1)

- **Qdrant kayıt biçimi ve arama disiplini — beş biçim, dört ölçüm** (186 satır) → `konular/olcum-arama/incelemeler/qdrant-kayit-bicimi/RAPOR.md`
