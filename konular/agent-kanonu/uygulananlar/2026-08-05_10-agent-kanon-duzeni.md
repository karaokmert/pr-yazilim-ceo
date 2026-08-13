# Agent kanon düzeni — UYGULANDI (5 karar) + 1 ÇELİŞKİ

**Süre:** 2026-08-05 → 2026-08-10 · **Uygulandı:** plugin `ozel-yazilim 0.7.0`

---

## 1. Ne yapıldı

**`tools:` sınırı kaldırıldı** (6 Ağustos). Agent tanımlarında araç listesi tutulmuyor;
kısıt **kuralla** korunuyor. Ölçüldü: 9 agent tanımında `tools:` satırı **yok.**

**Üç katmanlı desen kuruldu** (7 Ağustos): preload listesi ile çağrılan skill ayrıldı.
- **body** — kim olduğun, her oturumda yüklenir
- **skill (preload)** — omurga + çekirdek, `skills:` listesinde (6-7 tane)
- **skill (çağrılan)** — öz/alet skill'leri, işe girerken açılır (~120 tane)
Ölçüldü: 9 agent tanımının 9'unda da `skills:` listesi var.

**Kural skill'de kalır, body'ye kopyalanmaz** (7 Ağustos). Body kural kodunu **anar**,
gövdesini taşımaz — böylece tek kaynak korunur.

**Atıf haritası — dört kapsam kararı** (7 Ağustos): hangi skill hangisine atıf verir,
çift tanım nasıl önlenir.

**`agent-sinama` skill'ine iki ders eklendi** (10 Ağustos): OY pilot rol sınamasından.

## 2. Neden öyle

**`tools:` neden kalktı:** araç listesi bir kısıt gibi görünüyordu ama **yanlış katmanda**
duruyordu. Bir agent'ın neyi yapmayacağı araç yokluğuyla değil **kuralla** tanımlanır —
araç kaldırılınca agent *"yapamıyorum"* der, kural varken *"benim işim değil"* der.
İkincisi doğru davranış.

**Üç katman neden gerekti:** her şey preload edilirse context şişer, hiçbiri edilmezse
agent kanonsuz kalır. Ayrım: **her işte lazım olan** preload'a, **bir işe özel olan**
çağrılana.

**Kural neden kopyalanmaz:** kopyalanan kural iki yerde yaşar ve biri değişince öteki
sessizce yanlış kalır. Body'de kod anılır, gövde skill'de durur.

## 3. Nerede yaşıyor

`plugin 0.7.0` → `.claude/agents/*.md` (9 agent, `skills:` listeleriyle)
`.claude/skills/` (~120 skill) · Clara tarafı: `.claude/skills/agent-sinama/`

## 4. ⚠️ ÇÖZÜLMEMİŞ ÇELİŞKİ — release tag

**Karar (2026-08-05, Mert):** *"Prod çıkışında `vX.Y.Z` release tag'i atılmayacak.
Tag adımı akıştan çıkıyor."* Mert'in cümlesi: *"Clara ben bu tag sistemini hiç sevmedim."*

**Kanon (bugün, 0.7.0):** `REL-DO-PRODUCTION-TAG` — *"Prod deploy sonrası versiyon TAG'i
(`v{x.y.z}`) + not **ZORUNLU**; atlamak **YASAK**."*

**Ölçüldü 2026-08-13:** karar ya uygulanmamış ya geri alınmış — **hiçbir yerde yazmıyor.**
DO bugün prod'a çıksa kanona uyup tag atar.

→ **Karar Mert'te:** kanon mu düzeltilecek, karar mı geri alınacak?
Karar dosyası bu yüzden `kararlar/` altında **bırakıldı**, şerhi içinde.

---

## Buradan çıkan genel ders

**Bir karar "verildi" demek "sahada tutuyor" demek değil.** Bu, aynı gün ölçülen üçüncü
vakaydı (PA'nın TASK-STATUS alarmı · MB'nin çözülmüş sandığı çatışma · bu).
→ Bir karara dayanmadan önce **kanonda karşılığı var mı** diye bakılır.

---

> 5 karar dosyası buraya özetlendikten sonra `.trash`'e alındı.
> `2026-08-05-release-tag-sistemi-kaldirildi.md` **taşınmadı** — çelişki açık.
