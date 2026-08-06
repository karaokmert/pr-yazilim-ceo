---
name: sprint-3-kanal-kurulumu
description: Sprint 3. iş — fabrikada kanal kurulumu; Clara agent-project'ten çalışacak, görevi agent'lara kanalı handoff'la anlatmak ve düzeni kurmak. Mimari kararlar verildi, kurulum orada.
metadata:
  type: project
---

# Sprint 3. iş — fabrika ile kanal kurulumu

**Durum:** 2026-08-06 akşamı devredildi. 1. ve 2. iş kapandı, sıra 3'te.
**Nerede çalışılacak:** `/Users/karaok/p/agent-project` — Mert Clara'yı orada başlatacak.
**Clara symlink'li** (2026-08-06): `~/.claude/agents/clara.md` + iki skill, yani her
repodan çağrılabilir. Açılış hook'u `pr-yazilim-ceo/.claude/hooks/clara-acilis.sh`.

## Mert'in tarifi — orada ne yapılacak

> *"Orada çalışırken yapman gereken şey agent'lara kanalı handoff'larla anlatmak,
> kanallarını açtırmak ve düzeni kurmak olacak."*

Yani üç iş: **anlat → açtır → düzeni kur.** Ve bunu handoff'la yapıyorum, kendim
kurmuyorum — kanon değişikliği PAD'in, denetim PQA'nın.

## Mimari — 2026-08-06'da karara bağlandı, tartışılmaz

Tam gerekçe: `kararlar/2026-08-06-kanal-mimarisi.md` (10 karar + ek).
**Bu dosya okunmadan kurulum yapılmaz.**

Dört kural, Mert'in cümleleriyle:

```
Her agent kendi kanalını açar.
Her agent kendi kanalını okur ve yazar.
Clara açılan her agent'ın kanalına okuyup yazabilir.
Hiçbir agent doğrudan diğer agent'a yazamaz.
```

Gerekçe: *"Bu sayede onaysız bir iletişim asla kurulamaz."*

**Fiziksel kararlar:**
- Yer: `~/.pr-kanal/{proje}/{proje}-{rol}-{oturum}.md` — proje **dışı**, müşteri
  reposuna yazılmaz. Tarih dizini reddedildi.
- Kanal **silinmez** — `KAPANDI` satırı yazılır. Silme `tail -F`'i sessizce öldürüyor.
- Kanal başlığında **`PID` + `BAŞLANGIÇ`** durur — Clara ölü kanalı bununla ayırt eder
  (`kill -0` + `ps -o lstart`). PID tek başına yetmez: macOS tavanı 4000, dönüşümlü.
- **Kanal başına bir monitör.** Tek monitör OLMAZ: `tail -F` glob'u sonradan açılan
  dosyayı yakalamıyor ve bu sessiz.
- Agent kendi kanalını **yön filtresiyle** izler (`clara -> {rol}`), yoksa kendi
  yazdığını okur.
- **Kapanışı kanal söyler** (Mert, 2026-08-06): Clara agent'ın "iş bitti" yazısını
  okur, kanalı kapanışa çevirir; süreç hâlâ açıksa Mert'e uyarı verir. Saat eşiği
  uydurulmaz.

## Kurulumda kapatılması gereken altı sessiz kayıp yolu

Hiçbirinde otomatik tespit yok — hepsi ölçülmüş:

**Göreli yol** — tek gerçek agent hatası: DO göreli yol kullandı, iki mesaj sessizce
kayboldu. *"Kanonda 'mutlak yol kullan' diye bir kural yok"* → **mimariden gelmeli.**

**Açılış kaybı** — `tail -n 0 -f` kurulmadan önce yazılan mesaj hiç gelmiyor (2 kez).

**Ölü monitor** — ama bu bugün ÇÖZÜLDÜ: monitör ölümü **bildiriliyor**
(`status: failed`, exit kodlu). Belgede yok, ölçümle bulundu.

**inode kaybı** — dosya silinip yeniden oluşursa `tail -F` sessizce ölür.

**Sıra garantisi yok** — 5 eşzamanlı mesaj `4,3,5,1,2` dizildi. **Sıra içeriğe yazılmalı.**

**Kutu karıştırma** — benzer isimli kutulara bakıp yanlış alarm (Clara yaptı).

## Clara'nın kendi riski — mimarinin dayanak noktası

Yıldız topolojide trafik tamamen benden geçiyor. 2026-08-05'te **10 trafik kusuru**
ölçüldü: Mert'in imzasıyla kural yazmak, sözünü kendi lehine genişletmek (**ve aynı
hatayı bir tur sonra tekrarlamak**), olmayan onay uydurmak, uydurma muafiyet yazmak,
çelişkili talimat vermek, mesajın hiç ulaşmaması, **kanalı kurup 8 tur dinlememek**.

Günlüğün hükmü: *"denetim mekanizması Mert de değildi — ÖLÇÜLEN AGENT'LAR oldu."*

**Tasarıma yazılacak sonuç: uçlar itiraz edebilir olmalı.** PA uydurma muafiyeti
çürüttü, DO kayıp mesajı bildirdi.

**Ve merkezin dinlemesi protokolün ŞARTI** — oturum açılışında monitör kurulur, bu bir
adım değil ön koşul. Merkez dinlemezse bütün trafik durur ve durduğu görünmez.

## 3. işte ölçülecek beş kalem

**2. işten devreden üç tanesi:**
- `persistent: true` **compaction'dan sağ çıkıyor mu** — belgelenmemiş. Uzun Clara
  oturumu compaction'a girerse monitörler ölür mü? Yıldızda doğrudan kayıp riski.
- **Olay hızı sınırının sayısı** — *"too many events"* deniyor, sayı yok. Altı agent
  aynı anda yazarsa monitör durdurulur mu?
- **Monitör üst sınırı** — 5 paralel ölçüldü, tavan bilinmiyor.

**1. işten devreden ikisi:**
- **Aynı rolden iki örnek** — hiç kurulmadı. Clara'nın defterinde **iş eşlemesi**
  tutulmalı (`a3f2 → sipariş`, `9c71 → rapor`), yoksa aynı iş ikisine gider.
- **Agent kapanınca kanal ne olur** — karar verildi (arşive), ölçülmedi.

## Fabrikaya girerken bilinmesi gerekenler — 1. işin bulgusu

Tam liste: `incelemeler/fabrika-denetimi/eksikler.md` (altı öncelik).

**Hook alt-agent'ta ÇALIŞMIYOR** ve `CLAUDE_CODE_AGENT` **çağıranın** adını taşıyor
(PCA açıldı, değer `pr-agent-manager` geldi). PAM'in tespiti — **sıra tersine
kurulamaz:** hook'u env sorunu çözülmeden çalıştırmak sistemi bugünkünden **kötü**
yapar. Bugün alt-agent kanonsuz (görünür arıza); o durumda yanlış personelin kanonunu
yüklü sanar (sessiz arıza).

**Kanonun ulaşması garantisiz:** PCA üç skill'den ikisini aldı, `uretim`'i almadı — ve
gelenler **hook'la değil, başka bir yolla** geldi. Hangi mekanizma olduğu ölçülmedi.
**PAD'a üretim işi verilirse üretim kanonsuz yapılır.**

**`Task` değil `Agent`** — kanonda 20 yerde `Task` yazılı, envanter `Agent` diyor, PAM
sahada `Agent` kullandı. Kanon metni gerçeği yanlış tarif ediyor.

**PAM'de `tools:` satırı YOK** (bilinçli, 2026-08-04 kullanıcı kararı). 3. işin *"PAM'in
Task yetkisi kalkar"* maddesi bunu bilmeli: **alınacak liste yok, kısıt sıfırdan
yazılacak.** Ve `tools:` düzenlemesi fiilen engellemiyor (`YT-FILTER-BEATS-LIST`,
ölçüldü: PQA/PCA'da `Write` yok ama beş dosya yazdı).

**PQA denetleyeceği kanonu elinde bulundurmuyor** — `yapi-taslari` denetim ekseninde ama
`skills:` listesinde yok. Aynısı `dagitim` için: `DAG-BUMP-BY-AUDITOR` sürüm bump'ı
yalnız PQA'ya veriyor, PQA o skill'i hiç okumuyor.

## PAM düğümü — çözülmüş, dosyada

PAM'in body'si değişecek ama PAM kendi tanımını değiştiremez (`BHV-NO-SELF-CONFIG`).
Çözüm 2026-08-05'te verildi: **planı Clara yazar** → PAD uygular → PQA denetler+push,
**PAM hiç girmez.** Gerekçe ve reddedilen iki seçenek:
`kararlar/2026-08-05-sprint-planlama-kararlari.md` (Karar 2).

**Ve bu `CLA-ASK-BEFORE-WRITING-OUT` kapsamında:** plan Mert'e gösterilir, onay alınır,
sonra kanala düşer.

## Sprintin kalanı

```
1. Fabrika Ekibinin İncelenmesi     ✓ complete (2026-08-06)
2. Kanal Altyapısı ★darboğaz        ✓ complete (2026-08-06)
3. Fabrika ile Kanal Kurulumu       ← SIRADA, agent-project'te
4. Bilgi Eksiğinin Giderilmesi         (3 ile birlikte yürür)
5. v8 Yeniden Tasarım                  (4'e bağlı)
6. Kanalla Canlıya Geçiş               (5'e bağlı, sprintin son işi)
7. Oturum Takip + Mesai                (kanal kurulunca başlar)
```

Her task'ın ClickUp yorumunda **1. iş taramasından çıkan alt notlar** var — o iş
yapılırken okunacak.
