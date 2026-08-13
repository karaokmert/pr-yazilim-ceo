# Sprint planlama oturumunda verilen kararlar

**Tarih:** 2026-08-05
**Karar veren:** Mert
**Bağlam:** İlk sprint planlama oturumu (5 Ağustos → 12 Ağustos sprinti)

Bu oturumda yedi işin gereksinimi tek tek netleştirildi. Aşağıdaki üç karar verildi,
üçü ölçüme bırakıldı.

---

## Karar 1 — Fabrika yeniden kurulmuyor, yapılandırılıyor

Soru 2026-08-03'te sorulmuş, cevaplanmamıştı: *fabrika bugünkü hâlinden devam mı
edecek, yoksa preload dersiyle baştan mı kurulacak?*

**Mert:** *"Baştan kurmaya gerek yok. Yapılandırmaya ihtiyaçları var. Yeniden değil —
yeniden kurmak çok gereksiz zaman kaybı."*

**Sonucu:** 1. işin kapsamı daraldı. *"Bu ekip doğru mu kurulmuş"* sorusu kapandı —
mimari doğru, roller ayrımı sağlam, kurallar yazılı. Kalan soru: **neyi eksik.** İş
artık bir yeniden-tasarım denetimi değil, **eksik envanteri.**

Gerekçe yalın felsefeyle aynı: çalışan bir şeyi yeniden kurmak israf.

---

## Karar 2 — PAM düğümü: planı Clara yazar

**Düğüm:** PAM'in body'si değişecek (`Task` yetkisi kalkacak) ama PAM kendi tanımını
değiştiremez (`BHV-NO-SELF-CONFIG`). Plan da PAM'den çıkacaktı ve plan kendi body'si
hakkında — zincir kırılıyordu.

**Karar:**

```
Mert → Clara (planı yazar)
         ↓ kanal
       PAD (uygular)
         ↓
       PQA (denetler + push)

PAM hiç devreye girmez.
```

**Gerekçe:** kural bozulmuyor, Clara zaten fabrikanın dışında (denetleyen ile
denetlenen ayrı el), Clara'nın elinde `plugin-dev` + `skill-creator` var, PAM kendi
değişimini hiç görmediği için yorumlama fırsatı da olmuyor.

**Reddedilenler:**
- *PAM planı yazar, Mert onaylar* — **emsal oluşturur**, sonraki sefer "onay varsa
  olur" diye okunur.
- *Kanona istisna yazılır* — **istisna zamanla genişler.**

**Bunun Clara'ya etkisi:** Clara fabrika kanonuna **plan yazan** taraf oluyor. Bu
`CLA-ASK-BEFORE-WRITING-OUT` kapsamına giriyor — plan Mert'e gösterilir, onay alınır,
sonra kanala düşer.

---

## Karar 3 — Kanal kimliği: proje bazlı oturum kimliği

Her agent açılışında tekil bir kimlik üretir, kanal adı o kimliği taşır. Kimlik
**proje bazlı** — iki katmanlı:

```
{proje}-{rol}-{oturum-kimliği}-inbox

goat-be-a3f2-inbox
goat-be-9c71-inbox     ← aynı projede ikinci BE
egeli-be-4d18-inbox    ← başka proje
```

**Bir karar iki soruyu birden çözüyor:**
- **Çoklu proje izolasyonu** — proje adı kanal adında, 5-6 proje sızmıyor
- **Aynı rolden iki örnek** — oturum kimliği tekil, iki BE = iki kanal, yarış durumu yok

**Reddedilenler:**
- *Tek kuyruk + sahiplenme* — **yarış durumu** (ikisi aynı anda okursa) ve işi kimin
  aldığı önceden bilinmez.
- *İkinci BE yasak* — **paralel geliştirme imkânsız** olur.

**Zorunlu sonucu:** gönderen taraf `goat-be-a3f2` gibi bir adresi tahmin edemez. Yani
**keşif mekanizması artık isteğe bağlı değil, mimarinin şartı.** Kimlik tekil olduğu
anda adres defteri zorunlu hâle geliyor.

---

## Karar 4 — Hook ölçümü 1. işin içinde

Hook riski: `agent-project/.claude/settings.json` hook'u `SessionStart` olayına bağlı
— bu bir alt-agent olayı değil. Alt-agent'ta çalışmıyorsa 4. iş anlamsızlaşır (kanon
verilir, eline ulaşmaz) ve 5 temelsiz kalır.

**Karar:** ölçüm 1. işin **ilk adımı** olur, sprintin önüne alınmaz. Gerekçe: 1 ve 2
paralel yürüdüğü için zaman kaybı yok, ve 4 zaten 3'ü de bekliyor.

---

## Ölçüme bırakılan üç karar

Bu üçü masa başında verilemedi — hepsi ölçüm gerektiriyor.

**Yönlendirme** (2. iş) — BE doğrudan QA'ya mı yazar, PA dağıtıcı mı olur, hibrit mi?
Mert: *"Bunu analizde, o task'ı yaparken görmek lazım."* Üç seçenek masada, gerekçeleri
ClickUp dokümanında.

**Preload stratejisi** (5. iş) — kaç skill preload olacak? Mert: *"Çünkü iş skillerini
nasıl yapılandıracağımızı bilmiyorum."* Yani preload bir girdi değil, **skill
yapılandırmasının sonucu.** Sıra ters kurulmuştu.

**Onay akışı** (6. iş) — her handoff onay gerektirir mi, onay nereden gelir, onay
beklerken agent ne yapar? 6. işin kendi gündemi.

**Örüntü:** üç açık kararın hepsi ölçüme bağlı. Yani soru-cevap turu doğal sınırına
geldi — kalan sorular masa başında değil, işin içinde cevaplanacak.

---

## Sprint yapısı

**Kayıt yeri kararı:** sprint yapısı + task'lar + statüler **ClickUp**'ta (Mert her
yerden görebilsin, repo bunu yapamıyor). Bulgu, ölçüm, karar, gerekçe **repo**'da
(arama kesin, `git log` geçmişi tutuyor). Kanon dosyaları repoda kalır — Claude Code
onları diskten okuyor.

**ClickUp yapısı:** `CLARA DOC` → `Sprint Planları` → `Sprint 2026-08-05 → 2026-08-12`
→ yedi iş sayfası. `Görevler` listesinde yedi task, altı bağımlılık.

**Sprint akış kuralı (Mert'in tarifi):** iş detaylandırılır → karar netleşir → doküman
yazılır → **sonra** task açılır. Detayı netleşmemiş işe task açılmaz.

**İsimlendirme:** `Clara - <kısa anlaşılır başlık>`. Ön ek sabit `Clara` (liste onun
listesi), işin içinde kim varsa başlıkta geçer (`Clara - PAM ile v8...`).

**Sonraki adım:** bu oturumun deneyimi bir **iş yönetim sistemi skill'ine** çevrilecek
— içinde sprint ritüeli, ClickUp düzeni, ara işlerin yönetimi.
