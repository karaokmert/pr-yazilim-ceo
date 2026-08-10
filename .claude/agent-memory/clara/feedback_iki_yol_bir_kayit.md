---
name: iki-yol-bir-kayit
description: Bir iş iki yoldan yapılabiliyorsa ve yalnız biri kaydı tutuyorsa, arıza sessizdir — sonuç doğru çıkar, kayıt bozulur. Ölçüldü 2026-08-10.
metadata:
  type: feedback
---

# İki yol, tek kayıt — sessiz arızanın imzası

**Bir iş iki farklı yoldan yapılabiliyorsa ve yalnız biri kaydı tutuyorsa, o kayıt
er geç bozulur — ve bozulduğu görünmez.**

**Why:** Ölçüldü, 2026-08-10. Fabrika kanalında outbox imleci **on üç saat**
ilerlemedi. Sebep bir unutma değildi: Mert *"sadece mesaja bakma, oturumları da
incele"* demişti; Clara mesajları `Monitor` bildiriminden ve oturum kayıtlarından
okudu. **İçerik ulaştı, iş yürüdü, hiçbir belirti çıkmadı** — ama `read.py`
çalışmadığı için imleç dondu.

Arıza ancak **kapanış kapısında** göründü: `archive.py` üç agent'ın kutusunu reddetti
(`rc=2`, *"46 unread, loss is SILENT"*). O kapı bir oturumda **bir kez** açılıyor.

**Ayıran soru: doğru sonucu doğru yoldan mı aldım?** Sonuç doğruysa kimse yolu
sorgulamıyor — tehlike burada.

**How to apply:** Bir işin iki yolu varsa ikisinden birini seç:
- Her yol kaydı **kendi** tutsun (yollar eşitlenir)
- Ya da ikinci yol **sonucu taşımasın**, yalnız *"bak"* desin (tek yol kalır)

`CLA-FIX-THE-CAUSE` burada birebir geçerli: *"Clara `read.py` çalıştırmayı unutmasın"*
bir **yama** — karıştıran şey (iki yol) yerinde duruyor. Sebep, yolun ikiliği.

**Ve bu sınıfın akrabaları aynı gün iki kez daha çıktı:** iki Clara oturumu açıktı,
hangisinin canlı olduğu yazılı değildi (PCA sorarak kurtardı) · bir dosya taşındı,
içindeki atıflar taşınmadı. Ortak imza: **iki tane var, hangisinin geçerli olduğu
kayıtlı değil.**

İlgili: [[feedback_olcum_yerine_yorum]] · [[feedback_yama_degil_sebep]]
