# Memory düzeni

> Hangi bilgi nereye yazılır, index disiplini, kaydın ömrü, agent memory envanteri.

> **Bu dosya bu konunun TEK adresidir.** Bir iş başlarken burası açılır;
> ne yapıldı, kaç kez değişti, hangi karar alındı — hepsi aşağıda sırayla.
> Yeni bir şey olduğunda buranın SONUNA yazılır.

---

## ⚠️ ÖNCE BUNLARI BİL — ölçülmüş tuzaklar

**1. İndeks EMİR taşır, dosya taşımaz.** `MEMORY.md` context'e **otomatik** girer —
agent hiçbir tool çağırmadan onu görür ve uygular. Dosyalar `Read` gerektirir.
→ İndekse **kural/talimat yazılmaz**, yalnız pointer. Deneyle kanıtlı: indekse
*"X de"* yazıldı, dosyaya *"Y de"* — agent X dedi, dosyayı hiç açmadı.

**2. Skill'le çelişen çıplak kayıt skill'i EZER.** Agent memory'de eşleşen kayıt
bulunca skill'i **hiç açmadan** ona yaslanır. Ölçüldü (2026-08-13): QA'nın memory'sinde
*"ONAY = PUSH"* yazıyordu, kanon tam tersini söylüyor. QA'nın cümlesi: *"sonraki
oturumda okuyup onaysız push atabilirdim."*

**3. Auto-injection 200 satır / 25KB yükler**, sonrası **hiç yüklenmez.** Şişmiş
index = en değerli kaydın görünmez olması.

**4. v7 mirası düştü — 1028 yetim dosya.** Plugin geçişinde isim alanı değişti
(`qa-engineer` → `ozel-yazilim-qa-engineer`), eski dizin duruyor ama agent bakmıyor.
⚠️ **Toptan kopyalama yasak** — içinde v8 kanonuyla çelişen kayıtlar var (UID kanıtladı).

**5. İki kayıt tek tek masum, yan yana kuralı silebilir.** FE bunu buldu: iki tercih
kaydı birleşince kanonun bir adımını örtüyordu.

---

## Kararlar (1)

**2026-08-07 — Saha kaydı knowledge graph'a yazılır**
Tarih: 2026-08-07 Karar veren: Mert Durum: Yürürlükte (şimdilik — Qdrant ölçüldü, elendi)
→ `konular/memory-duzeni/kararlar/2026-08-07-saha-kaydi-knowledge-graph.md`


## İncelemeler (1)

- **Agent memory envanteri — 1537 dosya yetim, ortak konu SIFIR** (154 satır) → `konular/memory-duzeni/incelemeler/agent-memory-envanteri/RAPOR.md`
