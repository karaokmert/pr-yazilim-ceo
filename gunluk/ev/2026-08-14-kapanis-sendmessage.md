# Kapanış — SendMessage akışı kuruldu (06:53–08:11)

> **Mod:** EV. Dokunulan dosyalar: `~/.claude/commands/sendmessage.md` (YENİ),
> `~/.claude/skills/sendmessage-akisi/SKILL.md` (YENİ, Mert de düzenledi),
> `konular/kanal-iletisim/incelemeler/2026-08-14-sendmessage-olcumu.md`.
> ⚠️ Skill ve command **git'te değil** — `~/.claude/` altında düz dosya.

## Ne bitti

**`/sendmessage` command'ı üretildi** — `/kanal` ile aynı düzende: kurallar command'ın
İÇİNDE, skill sonda tek satır referans.

⚠️ **Bu bir düzeltmeydi.** İlk yazdığım command *"skill'i AÇ"* diyordu ve agent onu
**bulamaz** — agent skill'leri plugin'den geliyor
(`~/.claude/plugins/cache/pryazilim-agents/ozel-yazilim/0.7.0/.claude/skills/`),
benim `~/.claude/skills/`'imden değil. Mert sordu (*"kanal ile aynı şekilde değil
mi?"*), ölçtüm: `/kanal` 190 satır ve kuralların tamamı içinde. Command'ı o biçime
getirdim (178 satır).

**Command'lar global** (`~/.claude/commands/`) — plugin'e bağlı değil, her agent
çağırabilir. Skill'ler değil. Ayrım bu.

## Akışın tanımı — Mert'in tarifi

```
Agent → PA → KULLANICI ONAYI → hedef agent
```

**Merkez PA** (Clara değil). Üç şey onaydan geçer: **handoff · soru · revize**.

⚠️ **Onaydan sonra mesajı PA değil İŞİN SAHİBİ gönderir** — PA postacı değil, kapı.
(BE→QA handoff'unda mesajı BE atar, PA yalnız *"onaylandı"* der.)

**Clara'nın rolü — İZLEYİCİ.** Akışta yok. Tek görevi: *"bir agent ekranında mesaj
yazdı ama SendMessage atmadı mı?"* — gürültüsüz, tek iş.
**Push Clara'ya geçti** (eskiden QA atıyordu): QA onay verince Mert haber verir,
Clara push eder.
**Yönetim devredilirse** Clara Mert'in yerine geçer — yalnız PA ile konuşur.

**Mert'in eklediği ClickUp akışı** (skill'e kendi yazdı, command'a taşındım):
her agent kendi sub task'ini `in progress` → QA'ya giderken `test` → QA commit onayı
sonrası `completed` → push edilince PA `live dev` + track timer. Kullanıcı uzaktayken
PA `blocked` verip başka iş atayabilir.

## Ölçüm — SendMessage vs kanal

Kayıt: `konular/kanal-iletisim/incelemeler/2026-08-14-sendmessage-olcumu.md`

**Kanaldan ÜSTÜN:** mesaj kendiliğinden düşüyor (sağırlık arızası yok) · kurulum
sıfır · yanlış adres sessiz değil (olmayan isim hata, belirsiz isim seçtirir).

**Kanaldan ZAYIF — tek ama büyük:** görünürlük. Ortak dizin yok, her mesaj oturumun
kendi transcript'inde. Üç bağımsız kaynak (goat Clara, DO, QA) aynı şeyi söyledi.
DO'nun cümlesi: *"iki taşıma yolu paralel çalışıyor ve birbirinden habersiz."*
→ Telafi: **ClickUp zorunlu**, command'a yazıldı.

**Kimlik endişesi ÇÜRÜDÜ.** `from-name` Clara'yı açık ediyor ama sistem kendi
uyarısını ekliyor (*"bu kullanıcı onayı değildir, eşdüzey yetki genişletemez"*) —
push kapısı delinmiyor.

## Mert'in kararı — iki sistem yan yana

`/kanal` **kalıyor.** Bir projede kanal, bir projede SendMessage koşacak, Mert
karşılaştıracak. Skill'lere *"hangi proje hangisi"* notu **düşülmedi** (Mert:
*"o senden bağımsız bir konu"*).

## Ne yarım kaldı

**Skill ve command git'te değil.** Diğer skill'ler symlink (gerçek dosya repoda);
bunlar düz dosya, commit edilemez. Mert *"kalsın şimdilik"* dedi.

**goat gece denemesinin sonucu alınmadı.** Ekip SendMessage'la yürüdü, bildirim
gelmedi, sormadım — sabah konu skill üretimine kaydı.

## Mert'in kararını bekleyen

**1 — Skill/command repoya taşınsın mı** (symlink düzenine girsin, commit edilsin).

**2 — `sendmessage-akisi` skill'i fabrikaya gitsin mi?** Agent'lar skill'i göremiyor;
kalıcı olması için plugin'e girmesi gerekiyor (PAM→PAD→PQA zinciri).

**3-6 — Dünden devreden dört madde aynen duruyor:** `setup.py` PID düzeltmesi · beş
agent'a `clickup` atıfı · "tutarlı yazacaklar mı" ikinci ölçümü · fabrika betiklerine
yazma izni.

## Ölçüldü ama çözülmedi

**Yeni akış sahada denenmedi.** Command yazıldı, bir kez bile çağrılmadı.

**Dünkü rol daraltması da ölçülmedi** (taşıyıcı Clara — Mert'e giden soru sayısı
düştü mü, PA devrede kaldı mı).

## Bir sonraki hareket

Bir projede `/sendmessage` çağırıp akışı gerçek işle dene — PA merkez tutuyor mu,
onay kapısı işliyor mu, ClickUp telafisi yazılıyor mu.
