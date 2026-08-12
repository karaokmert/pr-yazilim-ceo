---
description: Kanal kur ve izlemeyi başlat — merkez kutusu + izleyici + eski kutuların arşivi
---

Kanal düzenini kur. Bu iş **koşulsuz değil** — yalnız bu komut çağrıldığında yapılır.

## Önce oku

`kanal-kurulumu` skill'ini aç (Skill aracı, `kanal-kurulumu`). Mekanik, ölçülmüş
arızalar ve ayırt edici testler orada. **Skill'i okumadan kurma** — özellikle
`--force`, boru hattı çıkış kodu ve `.cursor` bölümleri.

## Sonra ölç — varsayma

**Hangi proje?** `pwd` mod vermez. Sinyaller: Mert ne dedi · hangi projede açık
agent oturumu var (`ps aux | grep -- --agent`) · `~/.pr-kanal/` altında hangi
dizin taze. Belirsizse **sor.**

**Açık kutu var mı?** `ls -lt ~/.pr-kanal/{proje}/`

⚠️ Kutunun içinde **`STATUS.md`** vardır — `DURUM.md` DEĞİL. (Hook bir dönem
`DURUM.md` arıyordu ve hiç bulamıyordu; sessiz arızaydı, 2026-08-12'de ölçüldü.)

## Eski kutuyu KAPAT — ama okumadan değil

```
python3 /Users/karaok/p/ozel-yazilim/skill-project/tools/kanal/archive.py <ESKI_KUTU>
```

`archive.py` okunmamış mesaj varsa **REDDEDER** ve *"the loss is SILENT"* der.
Bu bir kapıdır, öneri değil.

- Okunmamış varsa → önce `read.py`, sonra arşivle
- Okuyacak vakit yoksa → **kutu açık kalsın.** Açık kutu maliyet değil; kayıp
  mesaj maliyet.
- `--force` **yalnız okunmuş kutuda** kullanılır

## Kendi kutunu kur

```
python3 /Users/karaok/p/ozel-yazilim/skill-project/tools/kanal/setup.py clara \
  --task "<bu oturumda ne yönetiliyor>" --project <proje>
```

`--project` **zorunlu.** Betik merkez adresini agent'lara basar — kutu yoksa
yazacak adres de yoktur, mesajlar gönderenin kendi outbox'ında birikir ve
tek-ekran takip çöker.

## İzleyiciyi kur — `Monitor` aracıyla, `Bash` DEĞİL

```
ToolSearch("select:Monitor")
```

sonra:

```
python3 /Users/karaok/p/ozel-yazilim/skill-project/tools/kanal/watch.py <KUTUN>/inbox 2>&1 \
  | grep -E --line-buffered 'from=|ERROR:|INFO:|watcher started'
```

`persistent: true` ver. Bash'te çalıştırılırsa oturumu bloklar.

## Doğrula — beyanla yetinme

- `watcher started` satırı düştü mü?
- Kutu gerçekten kuruldu mu (`ls`)?
- İlk mesajı gönderdiğinde **gövde uzunluğunu geri okuyup karşılaştır** — `rc=0`
  yetmez, ve `| tail` ile çağırırsan `$?` **tail'den** gelir.

## Kurulduktan sonra

Kutunun adresini Mert'e bildir. Agent'lar oraya doğrudan yazacak.
