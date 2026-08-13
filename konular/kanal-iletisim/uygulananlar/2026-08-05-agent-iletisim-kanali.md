# Agent iletişim kanalı — UYGULANDI

**Fikir:** 2026-08-05 · **Uygulandı:** kanal v3 (JSON, beş betik)
**Doğrulandı:** sahada sürekli kullanımda — 2026-08-13 gecesi 9 agent tek merkezden yönetildi

---

## 1. Ne yapıldı

Agent'lar arası **dosya tabanlı mesajlaşma kanalı** kuruldu. Yıldız topoloji:
merkezde yönetici (Clara), her agent'ın `inbox/` + `outbox/` kutusu.

- **Mesaj başına bir JSON dosyası** (`{zaman}-{gonderen}.json`)
- **Beş betik:** `setup.py` · `send.py` · `read.py` · `watch.py` · `archive.py`
- Kutu adı: `{rol}-{YYYYMMDD-HHMM}` · durum `STATUS.md`'de (`STATE: OPEN`)
- Agent'lar **merkez inbox'a** yazar, kendi outbox'ına değil

## 2. Neden öyle

**Neden dosya, neden bellek değil:** agent oturumları birbirini görmez; ortak
tek zemin dosya sistemi. Ve dosya **iz bırakır** — kim ne zaman ne yazdı,
sonradan denetlenebilir.

**Neden mesaj başına ayrı dosya:** tek dosyaya append eden iki agent birbirinin
yazısını ezer. Ayrı dosya çakışmayı yapısal olarak imkânsız kılar.

**Neden yıldız, neden herkes herkese değil:** ölçüldü (2026-07-30) — bir agent
diğerini doğrudan çağırdığında **rapor kullanıcıya değil çağırana gider.**
Zincir görünmez olunca hata da görünmez olur. Merkez, görünürlüğü garanti eder.

## 3. Nerede yaşıyor

`/Users/karaok/p/ozel-yazilim/skill-project/tools/kanal/` — beş Python betiği
Clara tarafı: `kanal-kurulumu` skill'i (`/kanal` komutuyla açılır)

## 4. Ölçülmüş tuzaklar — `BILINMESI-GEREKENLER.md`'de

Monitörler oturumla ölür · `PID` canlılık kanıtı değil · kanal **taşıyıcıdır,
kayıt değil** · arşivleme okunmamış mesajı reddeder · tip adları sabit
(`TASK|INFO|QUESTION|CLOSE`) · boru hattı çıkış kodunu yutar.

---

## Sahada ölçülen sonuç

**Web PA'nın deneyimi** (2026-08-05, ilk koşum): iki agent kanalda çalıştı,
düzen tuttu. Tespiti: *"kanal çalışıyor ama okuma disiplini gerekiyor —
mesaj gelmiş olması okunduğu anlamına gelmiyor."*

**2026-08-13 gecesi:** 9 agent tek merkezden yönetildi, iki tur iş koştu,
73 mesaj işlendi, kayıp yok.

---

> Fikir dosyaları (`DISCOVERY.md` 117 satır + `DENEYIM-web-pa.md` 184 satır)
> buraya özetlendikten sonra `.trash`'e alındı.
> ⚠️ `relay-guvenlik-bulgusu.md` **AÇIK** — fikirler/ altında kaldı.
