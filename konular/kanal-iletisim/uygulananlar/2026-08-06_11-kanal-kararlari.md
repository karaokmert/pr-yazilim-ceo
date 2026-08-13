# Kanal kararları — UYGULANDI (6 karar)

**Süre:** 2026-08-06 → 2026-08-11 · **Doğrulandı:** 2026-08-13 (9 agent, 73 mesaj)

## 1. Ne yapıldı

**Kanal mimarisi** (6 Ağt): yıldız topoloji, merkezde Clara. Her agent'ın `inbox/` +
`outbox/` kutusu; agent'lar **merkez inbox'a** yazar.

**`Task` çağrısı kaldırıldı** (7 Ağt): agent'lar birbirini doğrudan çağırmaz —
iletişim **kanal ve ekran** üzerinden.

**Oturum biçimi `YYYYMMDD-HHMM`** (7 Ağt). Ölçüldü: `clara-20260812-1249` — uygulandı.

**Kanal betikleri fabrikaya asset olarak taşındı** (8 Ağt). Ölçüldü:
`skill-project/tools/kanal/` altında **5 betik** var.

**Compact öncesi devir hook'u** (10 Ağt) · **kanal açılış hook'u** (11 Ağt):
`.claude/hooks/clara-acilis.sh`.

## 2. Neden öyle

**`Task` neden kalktı:** ölçüldü (2026-07-30) — bir agent diğerini çağırdığında
**rapor kullanıcıya değil çağırana gider.** 2026-07-30'da bir denetçi raporunu
üreticiye verdi, atmadığı bir push'u *"attım"* dedi; `origin/main` eski commit'teydi.
**Zincir görünmez olunca hata da görünmez oldu.**

**Betikler neden fabrikaya taşındı:** repoda değildi — n8n kurulabiliyordu ama
konuşamıyordu. Asset olarak taşınınca her proje aynı sürümü kullanıyor.

## 3. Nerede yaşıyor

`skill-project/tools/kanal/` (setup · send · read · watch · archive)
`~/.pr-kanal/{proje}/` (kutular) · `.claude/hooks/clara-acilis.sh`
Clara: `kanal-kurulumu` skill'i (`/kanal` komutuyla)

## 4. ⚠️ Bilinen arıza — düzeltilmedi

**Açılış hook'u kanalı göremiyor.** `DURUM.md` içinde `ACIK` arıyor, ama `setup.py`
artık **`STATUS.md`** yazıyor ve içine `STATE: OPEN` koyuyor. İki dosya adı, iki kelime —
hiç eşleşmiyorlar.

Ölçüldü 2026-08-12: oturum *"açık kanal yok, 9 dizin hiçbiri ACIK değil"* diye açıldı;
oysa **yedi kutu açıktı.** Tek satırlık düzeltme, Mert'in kararını bekliyor.

---
> 6 karar dosyası özetlendikten sonra `.trash`'e alındı.
> ⚠️ `fikirler/relay-guvenlik-bulgusu.md` AÇIK — fabrikaya iletilmeyi bekliyor.
