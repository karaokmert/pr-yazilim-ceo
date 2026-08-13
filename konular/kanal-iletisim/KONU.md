# Kanal — agent iletişimi

> Yıldız topoloji, merkez inbox, handoff taşıma, kanal betikleri.

> **Bu dosya bu konunun TEK adresidir.** Bir iş başlarken burası açılır;
> ne yapıldı, kaç kez değişti, hangi karar alındı — hepsi aşağıda sırayla.
> Yeni bir şey olduğunda buranın SONUNA yazılır.

---

## ⚠️ ÖNCE BUNLARI BİL — ölçülmüş tuzaklar

**1. Monitörler oturumla ölür.** Oturum kapanınca `Monitor` task'ı gider ama dizin
durur, `STATUS.md` `OPEN` yazar, mesajlar yerinde — **hiçbir şey arızalı görünmez.**
Yeni oturumda kanal varsa monitör **yeniden kurulur.**

**2. `PID` canlılık kanıtı DEĞİL.** Tek geçerli sinyal: kutunun **kendi son yazım
zamanı** (PCA ölçümü).

**3. Kanal TAŞIYICIDIR, kayıt değil.** Oturum kapanınca arşive gömülür. Ölçüldü —
iki bağımsız vaka aynı gün: QA'nın RED raporu ve bir karar cevabı kanalda kalıp
kayboldu, ertesi gün PA aradı bulamadı.
→ Üretilen rapor/karar **kalıcı katmana** (ClickUp yorumu / repo) geçer.

**4. Arşivleme okunmamış mesajı REDDEDER** — `--force` kaybı sessizleştirir, son çare.
Önce `read.py`, sonra `archive.py`.

**5. `send.py` tip adları sabit:** `TASK|INFO|QUESTION|CLOSE`. Başka tip `rc=1` döner
ve mesaj **gitmez** (Clara bir kez düştü, PA iş beklerken bekledi).

**6. Boru hattı çıkış kodunu yutar.** `python3 send.py ... | tail -3` yazarsan `$?`
**tail'in** kodudur. Ölçüldü: bir agent bu yüzden `send.py`'ye yanlış arıza atfetti.

---

## Kararlar (6)

**2026-08-06 — Kanal mimarisi — yıldız topoloji, merkezde Clara**
Tarih: 2026-08-06 Karar veren: Mert İş: Sprint 2. iş — Clara - Kanal Sisteminin Altyapısı (86cb1nmm7), sprintin darboğazı Girdi: yapılmış üç kanal deneyinin çıkarımları (gunluk/web-kanal-2/,…
→ `konular/kanal-iletisim/kararlar/2026-08-06-kanal-mimarisi.md`

**2026-08-07 — Kanal kutusunun `{oturum}` biçimi `YYYYMMDD-HHMM` oldu**
Kanal kutusu adresindeki {oturum} alanı YYYYMMDD-HHMM biçiminde yazılır.
→ `konular/kanal-iletisim/kararlar/2026-08-07-oturum-bicimi-tarih-saat.md`

**2026-08-07 — Karar: `Task` çağrısı kaldırıldı — iletişim kanal ve ekran üzerinden**
Tarih: 2026-08-07 Karar veren: Mert Kapsam: agent-project fabrikası (PAM/PAD/PQA/PCA) — ve emsal olarak diğer ekipler
→ `konular/kanal-iletisim/kararlar/2026-08-07-task-kaldirildi-iletisim-kanal-ve-ekran.md`

**2026-08-08 — Kanal betikleri fabrikaya asset olarak taşınır**
Karar: Mert, 2026-08-08 22:26 Tetik: N8N takımı üretim kapısı — PQA ikinci denetimde B8 bağımlılığını buldu
→ `konular/kanal-iletisim/kararlar/2026-08-08-kanal-betikleri-asset-olarak-tasinir.md`

**2026-08-10 — Compact öncesi devir hook'u — Mert'in kararı**
Tarih: 2026-08-10 11:47 · Karar: Mert · Durum: karar verildi, üretilmedi
→ `konular/kanal-iletisim/kararlar/2026-08-10-compact-oncesi-devir-hooku.md`

**2026-08-11 — Karar — kanal kurulumu açılış hook'una alındı, merkez kapısı yok**
Tarih: 2026-08-11 · Karar veren: Mert · Oturum: YÖNETİM (fabrika) Uygulama: ~/.claude/hooks/kanal-acilis.py + ~/.claude/settings.json (SessionStart) · yedek: settings.json.yedek-20260811-1008
→ `konular/kanal-iletisim/kararlar/2026-08-11-kanal-acilis-hooku.md`


## İncelemeler (2)

- **Kanal betikleri git'te değil — boşluk ölçüldü, BÜYÜK** (92 satır) → `konular/kanal-iletisim/incelemeler/kanal-asset-boslugu/RAPOR.md`
- **v7'nin iletişim düzeni — neyle tutturuyordu** (90 satır) → `konular/kanal-iletisim/incelemeler/v7-iletisim-duzeni/RAPOR.md`

## Fikirler (1)

- **agent-iletisim-kanali** (3 dosya) → `konular/kanal-iletisim/fikirler/agent-iletisim-kanali/`
