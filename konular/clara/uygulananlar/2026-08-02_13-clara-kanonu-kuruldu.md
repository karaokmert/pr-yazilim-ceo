# Clara'nın kanonu — KURULDU ve 23 kararla şekillendi

**Süre:** 2026-08-02 → 2026-08-13 · **Karar mercii:** Mert
**Uygulandı:** `.claude/agents/clara.md` (body — her oturumda yüklenir)

---

## 1. Ne yapıldı

On bir günde 23 karar alındı ve hepsi kanona girdi. Kanon üç şeyi tanımlıyor:
**kim olduğum · neyi yapmadığım · nasıl çalıştığım.**

**Kuruluş (2 Ağustos):** Clara bir asistan değil düşünme ortağı olarak kuruldu —
yönetim kurulu yüksekliğinde konuşur, karşı argüman verir, karar vermez.

**Yetki genişlemesi (3 Ağustos):** kendi kanonuna yazma yetkisi verildi.
Mert'in gerekçesi: *"yaşayan ve gelişen bir agent olman lazım ki bana faydan olsun."*
Aynı gün `CLA-WRITE-HERE-ONLY` kaldırıldı, yerine `CLA-ASK-BEFORE-WRITING-OUT` geldi —
başka repoya yazabilir ama **önce metni gösterir, onay alır.**

**Davranış kuralları:** merak (5 Ağt) · ölçüm için agent çağırma (6 Ağt) ·
açılış-kapanış düzeni (7 Ağt) · hangi kararı kendi verir (8 Ağt) ·
**yama değil sebep** (9 Ağt) · önce ürün sonra kalite (8 Ağt).

**Saha rolü (11 Ağustos):** OY projelerinde yönetim temsilcisi — commit onayı Clara'da,
push onayı Mert'te. Üç kök kapatıldı: sınır ihlalleri · sunum · **görünürlük**
(*"beni proje takibinden koparırsa Clara devre dışı kalır"*).

**Dosya düzeni (13 Ağustos):** konu eksenine geçildi — yazma ve okuma aynı soruyu
sorar hâle geldi.

## 2. Neden öyle — üç kritik gerekçe

**Kanon yetkisi neden verildi ama üç şey dokunulmaz kaldı.**
Ad, kadın kimliği ve üç sert sınır (`CLA-ASK-BEFORE-WRITING-OUT` ·
`CLA-NO-CALL-TEAMS` · `CLA-ARGUE-BACK`) Mert'te kaldı.
> *Sebep: kimliğini ve sınırını kendi değiştiren bir agent'ın zamanla nereye
> kaydığını ölçecek hiçbir şey kalmaz.*

**Kural burada, gerekçesi dışarıda.** Body system prompt'a giriyor — oraya yazılan
kural bir sonraki turda *"doğru"* olarak değil **"ben"** olarak taşınır, yani
sorgulanamaz. Bu yüzden her kanon değişikliğinin gerekçesi ayrı dosyada durur.

**`CLA-FIX-THE-CAUSE` birinci kural oldu** (9 Ağustos). Mert'in cümlesi:
*"Eksinin yanına artı getirilerek sıfır yapılmaz — eksi ortadan kaldırılır.
O hatayı yapmana sebep olan şeyin zıttını kurala eklemek çözüm değil."*

## 3. Nerede yaşıyor

`.claude/agents/clara.md` — body, her oturumda yüklenir
Skill'ler: `oturum-duzeni` · `proje-yonetimi` · `saha-monitorluk` · `sprint-yonetimi` ·
`kanal-kurulumu` · `agent-sinama` · `arama-disiplini` · `hafiza-duzeni` ·
`onay-brief` · `clickup-duzeni`

## 4. Çürütülen varsayımlar

**"Clara başka repoya hiç yazmamalı"** — kalktı (3 Ağustos). Ama yükü **arttı**:
o repoların kendi kapıları (PQA, push kapısı) Clara yazdığında atlanıyor, yani
doğruluğu kendi garantilemek zorunda.

**"Clara agent çağıramaz"** — daraldı (6 Ağustos). Ölçüm için çağırabilir; **iş
vermek için** çağıramaz. Ayıran soru: *çıktı bir ürün mü, bir ölçüm mü?*

**"Tek eşikli cevap uzunluğu kuralı"** — çürütüldü (11 Ağustos). Ölçüldü: 27 cevabın
25'inde ihlal edildi (%92) **ve Mert ihlallerin çoğunu haklı buldu.**
→ *Haklı ihlal üreten bir kural, kural değildir.* Bildirim turu / düşünme turu
ayrımına geçildi.

**"Clara OY kanonuna girer"** — reddedildi (12 Ağustos). Agent kanonu `kullanıcı`
der; Clara perde arkasında kalır, köprüyü açılış brief'i kurar.

---

## Açık kalan

⚠️ **`BEKLEYEN-cerceve-cumlesi-geride-kaliyor.md`** — PAM'in önerisi (7 Ağustos):
*"bir hüküm değişirken ona dayanan çerçeve cümlesi geride kalıyor."*
Mert: *"kayıt al, döneriz buna sonra."* **Hâlâ dönülmedi** — `kararlar/` altında duruyor.

---

> 23 karar dosyası (2026-08-02 → 08-13) buraya özetlendikten sonra `.trash`'e alındı.
> Gerekçeler ve çürütülen varsayımlar korundu. Kanonun kendisi
> `.claude/agents/clara.md`'de yaşıyor.
