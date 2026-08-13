# ClickUp task takip düzeni — UYGULANDI

**Karar:** 2026-08-12 (Mert) · **Uygulandı:** plugin `ozel-yazilim 0.7.0`
**Doğrulandı:** 2026-08-13, sahada koştu (PRAG testi, 9 agent)

---

## 1. Ne yapıldı

Agent'ların ClickUp'ta nasıl çalışacağı kurala bağlandı. **Üç fiil:** PA açar ·
agent yürütür · Clara okur.

- Agent **yalnız kendi sub task'ının** statüsünü çevirir. Ana task · başkasının sub
  task'ı · `Closed` · silme → mutlak yasak.
- Sub task sahipliği **başlık önekinden** okunur: `[FE] PRAG - ...`
  Kural: *"başlık senin kısaltmanla başlamıyorsa dokunma."*
- **Kapatma yetkisi QA'da, kaydın eli sahibinde.** QA onay verir, `completed`'ı sahibi
  çeker. Ayrı QA sub task'ı açılmaz.
- **Kanıt zorunlu** — ve **role göre değil ÇIKTI TÜRÜNE göre** tanımlanır.
- `TASK-STATUS.md` ve `status.md` **kalktı** — olay akışı sub task'larda zaten tutuluyor.
- Süre: statü süresi tracked'e işlenir, agent çeker (hesaplamaz).
- Prod'da elle yapılacak işler → ana task yorumu (`PROD İŞLERİ` başlığı).

Kapsam **OY**; Websitesi sonraya bırakıldı.

## 2. Neden öyle — üç kritik gerekçe

**Yasak kalkmadı, KAPSAMI daraldı.** Sahadan iki teklif geldi: (a) kural gevşesin,
(b) aynen kalsın. **İkisi de reddedildi — ikisi de yama** (`CLA-FIX-THE-CAUSE`).

> Asıl sebep *"statüyü kim çevirir"* değildi: **kural, kendisini askıya alacak meşru
> bir yol tanımlamamıştı.** Metin *"kullanıcı talimatıyla da AÇILMAZ (istisna yok)"*
> diyordu ama test tam o yoldan yürüdü.
>
> Kapsam daraltma sebebi kaldırıyor: sınır artık **talimatla değil sahiplikle**
> çiziliyor. *"Kendi sub task'ı"* ölçülebilir — bir kişinin o oturumdaki iznine bağlı
> değil. İstisnaya ihtiyaç kalmıyor.

**Kanıt role göre değil çıktı türüne göre.** Clara dokuz role tek tek kanıt arıyordu.
Mert kesti: *"QA okeyleyip UID'e döndüğünde; TE her işte işe girmez."*
→ Roller her işte yok; rol bazlı liste yazılırsa girmeyen rolün satırı boş kalır.

**Başlık formatı köşeli parantezle.** Alan sırasına dayanan iki format elendi çünkü
**modül adında bir tire geçerse alan kayar** ve kural sessizce yanlış task'ı işaret
eder. `[FE]` öneki `startswith` ile ölçülür, ayraçtan bağımsızdır.

## 3. Nerede yaşıyor

- **Kanon:** `plugin 0.7.0 → clickup/SKILL.md` — `CLICKUP-OWN-TASK-ONLY`,
  `CLICKUP-STATUS-SET`
- **Akış tarafı:** `is-akisi` skill'i (tek kaynak, omurgalar atıf verir)
- **Mekanik taraf:** `clickup` skill'i (PA dilinden genele çevrildi)

## 4. Çürütülen varsayımlar — aynı yola tekrar girilmesin

**"Kuralın gerekçesi çürüdü" — YARIM doğruydu.**
Eski gerekçe iki şey söylüyordu: *"agent'lar yazamaz"* + *"tutarlı yazmazlar."*
Clara birincisini çürüttü, **ikincisini hiç ölçmedi.** Fabrika düzeltti.
→ Kanıtlanan: *"yapabiliyorlar."* Kanıtlanmayan: *"tutarlı yapacaklar."*
**Bu kısıt gevşetilecekse önce ikincisi ölçülmeli.**

**"Her role bir kanıt türü" varsayımı** — reddedildi (yukarıda).

**Alan sırasına dayalı başlık formatı** — elendi (tire tuzağı).

---

## Sahada ölçülen sonuç (2026-08-13, PRAG testi)

Zincir **tam döndü**: sub task açıldı → yürütüldü → kanıt girildi → QA denetledi →
**RED** → revize → **ikinci RED** → revize → **ONAY** → `completed`.
QA hiç statüye dokunmadı; kural tuttu.

⚠️ **Ama üç arıza çıktı** (ayrıntı: `incelemeler/` ve `BILINMESI-GEREKENLER.md`):
- Süre kaydı **326 kat** yanılabiliyor (`current_status` vs `status_history`)
- Ve o sayı bile işi ölçmüyor — **revize alan iş kısa görünüyor** (kaliteyi ters ölçer)
- API kotası vurulduğunda **kalıcı kayıt katmanı tamamen kapanıyor**

**Bunlar hâlâ açık — Mert'in kararını bekliyor.**

---

> **Bu dosya, işin tek kaydıdır.** Fikir taslakları (`GEREKSINIM-...`, `is-akisi-taslak`,
> `pam-sorulari` — 1309 satır) ve dört ayrı karar dosyası (275 satır) buraya
> özetlendikten sonra **silindi.** Gerekçeler ve çürütülen varsayımlar korundu.
