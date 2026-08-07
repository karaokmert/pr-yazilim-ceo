# Mod ayrımı `pwd` ile ölçülmez — iş belirler, dizin değil

**Tarih:** 2026-08-07
**Karar veren:** Mert
**Etkilenen kanon:** `clara.md` → *"Oturum açılışı — önce NEREDEYİM"*

---

## Ne değişti

Kanon şöyle diyordu:

> `pr-yazilim-ceo`'daysan → EV. Başka bir projedeysen → YÖNETİM.
> Ayrım tek komutla ölçülür: `pwd`. Varsayılmaz.

Artık şöyle: **ayrımı `pwd` vermez, iş verir.** Mert'in ne dediği, hangi projede açık
kanal kutusu olduğu ve o projede açık agent oturumu bulunup bulunmadığı okunur;
belirsizse sorulur.

`pwd` yine okunur ama **başka bir soru için:** *"nereye yazabilirim."*

---

## Neden — hata nasıl yakalandı

Bu oturumun açılışında `pwd` çalıştırıldı, `/Users/karaok/p/pr-yazilim-ceo` döndü ve
*"evdeyim"* denildi. Mert kesti:

> *"şu an başka yerdesin agent project içindesin ama kendini evde sandın demek ki kontrol
> yapını pwd ile yapmamalıydın? sen orada kurulu bir agentsin bu nedenle pwd sana orayı
> verdi her projede çalışabilirsin."*

Mekanik şu: Clara `pr-yazilim-ceo/.claude/agents/` altında kurulu bir agent. Her projede
çalışabiliyor ama oturum çoğu zaman kendi reposundan başlatılıyor — yani `pwd` oturumun
**konusunu** değil, oturumu başlatan `cd`'yi gösteriyor. Clara için neredeyse sabit bir
değer, ve **sabit bir değerle değişken bir soru ölçülmez.**

Arızanın sessizliği burada: `pwd` her oturumda *"EV"* der. Yönetim moduna hiç geçilmez ve
hiçbir şey arızalı görünmez.

---

## Ölçüm — beş sinyal, sıfır bağımsız ölçüm

Ölçüldü (yorum değil): oturumun açıldığı yeri gösterdiği düşünülen beş sinyal yoklandı.

- `pwd` → `/Users/karaok/p/pr-yazilim-ceo`
- ana oturumun `lsof -d cwd` çıktısı → aynı
- oturumu başlatan komut satırı → `cd /Users/karaok/p/pr-yazilim-ceo && claude --agent clara`
- transcript yolu → `~/.claude/projects/-Users-karaok-p-pr-yazilim-ceo/`
- yüklenen proje `CLAUDE.md`'si → `pr-yazilim-ceo`

Beşi de **aynı yeri** gösterdi. İlk okumada bu bir doğrulama gibi görünüyor; değil.
Hepsi tek bir üst-nedenden türüyor — başlatma komutundaki `cd`. Yani elde beş bağımsız
ölçüm değil, **bir gerçeğin beş yansıması** var.

Ve bu turda `pwd` gerçekten doğru cevabı verdi (oturum `pr-yazilim-ceo`'da açılmıştı).
Ölçüt bu yüzden bozuk: **doğru cevabı yanlış nedenle veriyor.** Bu tür arıza en zor
yakalananı, çünkü test her seferinde geçiyor.

---

## Genel ders — çakışan sinyal doğrulama değildir

Ayırt edici test: **bu sinyallerin birbirinden ayrıldığı bir senaryo var mı?** Yoksa o
sinyal ölçmüyor, yansıtıyor.

İkinci ders: bir ölçüt yalnız yanlış cevap verdiğinde bozuk olmaz — **doğru cevabı
yanlış nedenle** verdiğinde de bozuktur.

---

## Yan bulgu — `CLAUDE_CODE_AGENT` ana oturumda doğru

Aynı ölçümde çıktı: `CLAUDE_CODE_AGENT=clara`. Yani değişken ana oturumda **kendi agent
adını** taşıyor.

`gunluk/2026-08-07-kapanis.md` bu değişkenin *"çağıranın adını taşıdığını"* söylüyor ve
fabrikada dört kanon kararı bu teşhis yüzünden bekliyor. İki gözlem çelişmiyor olabilir
(ana oturum ile alt-agent farkı) ama **teşhis bu ayrımı hesaba katmıyor.** Ayrı konu,
ayrı ölçüm gerekiyor — bu kararın kapsamı dışında, sırada.
