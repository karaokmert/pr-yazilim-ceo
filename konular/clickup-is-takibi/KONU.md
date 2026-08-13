# ClickUp — iş takip düzeni

> Task/sub task düzeni, statü akışı, kanıt zorunluluğu, süre kaydı, sprint yönetimi.

> **Bu dosya bu konunun TEK adresidir.** *"ClickUp'ta sorun var"* dendiğinde
> **buraya bakılır** — soru sorulmasını beklemeden.

---

## ⚠️ ÖNCE BUNLARI BİL — ölçülmüş tuzaklar

Bu işe girmeden önce okunacak beş şey. Hepsi sahada **fiilen** çarptı.

**1. Süre kaydı iki farklı yerde, biri YANLIŞ.**
`current_status.total_time_minutes` ile `status_history[in progress]` **aynı adı taşır,
farklı şeyi ölçer.** Ölçüldü: biri **1 dakika**, diğeri **326 dakika** gösteriyordu —
**326 kat fark.** Yanlış satır okunursa sessizce yanlış sayı yazılır, hata vermez.
→ Doğrusu: `get_task_time_in_status` → `status_history` içinde `status=='in progress'`.

**2. Ve o sayı bile işi ölçmüyor** — iki yönden yanılır:
- **Şişirir:** duvar saatini sayar. Task gece açık kalırsa gece de süreye yazılır
  (326 dk kayıtlı / ~12 dk fiilî çalışma).
- **Eksiltir:** revize turları `revise`/`test` statüsünde geçer, `in progress` yalnız
  **ilk** turu ölçer. İki kez RED alıp düzelten iş **1 dakika** görünür.
→ Sonuç: kayıt **kaliteyi ters ölçüyor.** Metrik olarak kullanılırsa yanlış kişiyi
ödüllendirir. *Karar Mert'te — hangi satır(lar) toplanmalı.*

**3. `since` başlangıç DEĞİL** — "o statüye **en son** geçiş anı". Revize turu yaşandıysa
toplamla tutarsız olur. `start` toplam süreden geri sayılarak üretilir.

**4. Timer kullanılmaz** — ClickUp'ta aynı anda tek timer, ve timer **kullanıcıya** bağlı.
Paralel agent'larda ikincisi hata alır (ölçüldü).

**5. Yazma çağrısının DÖNÜŞÜ ölçüm değildir.** İki yanlış alarm ölçüldü: sub task
açılışında `description` boş göründü (doluydu), `custom_id` null geldi (atanmıştı).
→ Düzeltmeye koşmadan **önce oku.**

**6. API kotası yazma katmanını da keser.** Vuruldu (2026-08-12): *"796 dakika
bekleyin."* Önce yalnız `add_time_entry`, dört dakika sonra **yorum yazma da** kapandı.
→ Bu düzen ClickUp yorumunu *kalıcı kayıt* olarak kullanıyor; kota vurulduğunda
**kalıcı kayıt katmanı tamamen kapanır.** O an üretilen kayıt repoya yazılır
(`bekleyen/` altına), kota açılınca taşınır.

**7. Yatay çizgi (`---`) kullanma.** MCP markdown dönüşümünde `undefined` olarak
basılıyor (ölçüldü: bir yorumda 6 adet). Başlık ya da boş satırla ayır.

---

## Düzenin kendisi — üç fiil

**PA açar · agent yürütür · Clara okur.**
Hiçbir agent yeni sub task AÇMAZ. Clara statü DEĞİŞTİRMEZ.

- Agent **yalnız kendi sub task'ının** statüsünü çevirir. Ana task · başkasının sub
  task'ı · `Closed` · silme → **mutlak yasak.**
- Akış: `Open → in progress → test` (QA'ya devrederken) → QA onayı → `completed`.
  RED gelirse → `revise` → düzelt → `test`.
- **Kapatma yetkisi QA'da, kaydın eli sahibinde.** QA statüye dokunmaz, onay verir;
  `completed`'ı sahibi çeker. Ayrı QA sub task'ı açılmaz.
- **Kanıt zorunlu.** *"Bitti"* beyandır, kayıt değildir. Kod → commit hash ·
  denetim → QA onay handoff'u · analiz → dosya yolu + ölçüm sayısı.
- Kapanış sub task'ı **başta açılır**, `Open` bekler — *"açılmamış iş görünmez iştir."*
  (Bu kural ClickUp task açıklamasında yaşıyor, **kanonda yok** — bulundu 2026-08-12.)

## Sahada ölçülen davranış

**Zincir tam döndü** (2026-08-13, `PRC-45`): sub task açıldı → yürütüldü → kanıt
girildi → QA denetledi → **RED** → revize → **ikinci RED** → revize → **ONAY** →
`completed`. QA hiç statüye dokunmadı.

**QA'nın refleksi:** *"Adres verilmiş olması sadakat kanıtı DEĞİL — kaynağı okudum."*
14 iddiayı tek tek karşılaştırdı, 13'ü tuttu, 14'üncüsü düştü.

---

## Kararlar (8)

**2026-08-05 — Sprint planlama oturumunda verilen kararlar**
Tarih: 2026-08-05 Karar veren: Mert Bağlam: İlk sprint planlama oturumu (5 Ağustos → 12 Ağustos sprinti)
→ `konular/clickup-is-takibi/kararlar/2026-08-05-sprint-planlama-kararlari.md`

**2026-08-06 — Önce plan, sonra görev listesi, sonra koşum**
Tarih: 2026-08-06 Karar: Mert Kanona giren yer: .claude/agents/clara.md → "Nasıl çalışırsın" başlığının ilk alt bölümü
→ `konular/clickup-is-takibi/kararlar/2026-08-06-plan-task-kosum-sirasi.md`

**2026-08-11 — Her takımın sprint yapısı ayrı — ortak skill yok**
Tarih: 2026-08-11 · Karar: Mert · Bağlam: fabrika oturumu, sprint yöntemi işi
→ `konular/clickup-is-takibi/kararlar/2026-08-11-her-takimin-sprint-yapisi-ayri.md`

**2026-08-11 — PA'nın gereksinim kası şarta bağlanır — kaldırılmaz**
PA'nın agent gövdesinde şu satır var (v8/ozel-yazilim/.claude/agents/project-assistant.md):
→ `konular/clickup-is-takibi/kararlar/2026-08-11-pa-gereksinim-kasi-sarta-baglanir.md`

**2026-08-11 — Proje kaydı ve sprint düzeni — ClickUp ana kaynak, repo tezgah**
Clara'nın yeni rolünde gereksinim ve sprint planı üretmek var (birinci iş) ama bunların nerede yaşayacağı tanımsızdı.
→ `konular/clickup-is-takibi/kararlar/2026-08-11-proje-kaydi-ve-sprint-duzeni.md`

**2026-08-12 — Agent iş akışı — ClickUp task takip düzeni**
Tarih: 2026-08-12 · Karar: Mert · Getiren: Clara (fabrika modu) Gereksinim: fikirler/agent-is-akisi/is-akisi-taslak.md (v3) Test kaydı: fikirler/agent-is-akisi/pam-sorulari.md
→ `konular/clickup-is-takibi/kararlar/2026-08-12-agent-is-akisi-clickup-duzeni.md`

**2026-08-12 — ClickUp yazma yetkisi — yasak kalkmaz, kapsamı daralır**
Tarih: 2026-08-12 · Karar: Mert · Getiren: Clara (fabrika modu) Etkilenen kanon: CLICKUP-PA-ONLY-WRITE (OY — clickup/SKILL.md:45, project-assistant/SKILL.md:36)
→ `konular/clickup-is-takibi/kararlar/2026-08-12-clickup-yazma-yetkisi-kapsam-daraltma.md`

**2026-08-12 — TASK-STATUS.md ve status.md kalkıyor — olay akışı ClickUp sub task'larında**
Tarih: 2026-08-12 · Karar: Mert · Getiren: Clara (fabrika modu) Etkilenen kanon: OY proje-dosya-duzeni (+ 16 dosyada status.md atfı)
→ `konular/clickup-is-takibi/kararlar/2026-08-12-task-status-ve-status-md-kalkiyor.md`


## Fikirler (1)

- **agent-is-akisi** (3 dosya) → `konular/clickup-is-takibi/fikirler/agent-is-akisi/`
