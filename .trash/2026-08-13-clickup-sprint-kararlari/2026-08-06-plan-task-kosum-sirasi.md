# Önce plan, sonra görev listesi, sonra koşum

**Tarih:** 2026-08-06
**Karar:** Mert
**Kanona giren yer:** `.claude/agents/clara.md` → "Nasıl çalışırsın" başlığının ilk
alt bölümü

## Karar

Bir iş birden fazla yöntem denemeyi gerektiriyorsa sıra şudur: **plan çıkarılır,
görev listesine çevrilir, sonra koşulur.** Sıra atlanmaz.

Mert'in cümlesi: *"Bana sormaan gerek yok, yöntemleri farklı farklı şekillerde dene,
önce plan yap task listesin oluştur sonra tasklerini koş — bu agentların en önemli
kuralı olacak. Sende bunu benimse."*

İki parçası var ve ikisi ayrı: **(1)** plan→liste→koşum sırası, **(2)** ara adımı
Mert'e sormama.

## Neden bu karar çıktı

Qdrant kayıt biçimi ölçümü sırasında Clara, iki yöntemi ölçtükten sonra
*"hangisini önce ölçelim?"* diye sordu. Bu soru yükü Mert'e atıyordu — oysa sıra
ölçümün kendi mantığından çıkıyor: metadata filtresi ancak metadata varsa
ölçülebilir, artımlı indeksleme ancak biçim netleştikten sonra anlamlı.

Yani Clara'nın cevaplayabileceği bir soruyu Mert'e sordu.

## Görev listesinin neden zorunlu olduğu — aynı gün ölçüldü

Karar verildikten sonra iş dört göreve bölündü, bağımlılıklarıyla:

- #1 kategorili biçim → #2 filtreli arama → #4 artımlı indeksleme (zincir)
- #3 çakışma/tazelik testi (bağımsız, paralel koştu)

**#2'nin sonucu #4'ün gerekçesini geçersizleştirdi.** Filtre ölçümde tek işe yarayan
iyileştirme çıktı (5/7 → 7/7) ama MCP'nin `qdrant-find` aracı filtre desteklemiyor.
Yani artımlı indeksleme yazmak, MCP'den kullanılamayan bir sisteme yatırım olurdu.

Liste olmasaydı #4 sırayla koşulup boşa kodlanmış olacaktı. Liste olduğu için gerekçe
güncellendi ve karar Mert'e bırakıldı.

**Buradan çıkan ikinci kural:** bir görev bittiğinde sonucu diğerlerinin gerekçesini
değiştirebilir; o zaman liste güncellenir. Ölçüm planı değiştirmek için yapılır, plana
uymak için değil.

## Ne sorulur, ne sorulmaz

**Sorulmaz:** ara adım sırası, hangi yöntemin önce denenmesi, bir ölçümün nasıl
kurulacağı. Bunlar ölçümün mantığından çıkar ve Clara'nın işidir.

**Sorulur:** bir yol seçilecekse (MCP değiştirilsin mi, vektör bırakılsın mı), bir
maliyet göze alınacaksa, bir kural kalkacaksa. Yani **karar.**

## Sınırı

Bu kural her işe uygulanmaz — tek adımlı bir iş için liste açmak gürültüdür. Eşik:
**iş üç veya daha fazla ayrı adım gerektiriyorsa ya da yöntemler arasında bağımlılık
varsa** liste açılır.

## İlgili kayıtlar

- Ölçümün kendisi: `incelemeler/qdrant-kayit-bicimi/kayit.md`
- Aynı gün kanona giren ikinci değişiklik:
  `kararlar/2026-08-06-arama-disiplini.md`

---

# EK — listeye ne girer, ne girmez (2026-08-06, aynı gün)

**Karar veren:** Mert · **Tetikleyen:** ölçülmüş bir Clara hatası

## Ne oldu

Fabrika denetiminde (sprint 1. iş) beş görev açıldı. İkisi gerçek ölçümdü (hook
alt-agent turu, `Task`/`Agent` araç adı) — ikisi de koşuldu ve kapandı. **Üçü bulguydu:**
cascade onarımı, sıfırdan üretme yöntemi, rapor biçimi. Üçü de o oturumda yapılacak iş
değil, **sonraki sprint işine devredilecek kalemlerdi.**

Sonuç: iş bittiğinde listede üç kalem *"açık görev"* gibi durdu. Mert sordu:
*"Sprint - Task 1 için şu an önümüzde 3 açık task gözüküyor? Bunlar ne olacak?"*

Soru haklıydı. Liste artık iş sırasını göstermiyordu, karışık bir yığın gösteriyordu —
ve bakan kişi hangisinin iş hangisinin not olduğunu ayırt edemiyordu.

## Karar

**Listeye yalnız yapılacak iş girer; çıkan bulgu girmez.**

Ayıran soru: **bu satır bu oturumda koşulacak mı?** Koşulacaksa görev. Bir ölçüm
sonucu, bir eksik, devredilecek bir kalem ise bulgu — dosyaya yazılır.

**İşin sonunda liste kapatılır.** Bulgular dosyaya taşınmış, görevler bitmiş olur.
Geride kalan her satır bir sonraki oturumda *"bu neydi"* sorusu üretir.

## Neden bu ayrım listenin işe yaramasının şartı

Liste tek bir soruyu cevaplıyor: *"şu an ne yapıyorum."* İçine bulgu konursa o cevap
kaybolur. Ve kaybı sessizdir — liste dolu görünür, üstelik verimli görünür; yalnız
işe yaramaz olur.

Bu, `sprint-yonetimi` skill'indeki kuralın aynısı, farklı yerde: *"bulgu task değildir.
Bir ölçüm sonucu, bir gözlem, bir örüntü → günlüğe yazılır. Task açmak onu iş kalemine
çevirir ve liste karışır."* Kural ClickUp için yazılmıştı; ölçüm gösterdi ki **oturum
tezgahı için de geçerli** — ve Clara ilk kuralı bilirken ikincisine düştü.

## Bunun agent'lara yayılması — Mert'in kararı

Mert: *"Tezgahındaki task'leri yönetmen önemli, bunu agent'lara da vereceğiz çünkü
artık. Her iş için önce liste oluşturacak, planlama yapacaklar."*

Yani bu kural yalnız Clara'nın değil; üretilecek agent kanonlarına girecek. O yayılım
**fabrikanın işi** (sprint 4. iş — *"Çalışma düzeni: planla → task listesi → adım adım
→ handoff"* maddesi zaten o işin kapsamında yazılı).

Yayılırken taşınacak iki şey: **sıra** (plan → liste → koşum) ve **süzgeç** (listeye
yalnız koşulacak iş girer). İkisi ayrı kural ve ikincisi olmadan birincisi zamanla
kendi kendini bozuyor — bugün ölçüldü.
