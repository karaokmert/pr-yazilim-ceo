# Agent'lar onay akışına düşüyor — oturum modu meselesi

**Tarih:** 2026-08-08 · **Teşhis eden:** Mert
**Durum:** açık (ölçülecek: mod nasıl set edilir, kalıcı mı)

## Belirti

Fabrikanın dört agent'ı N8N işinde çalışırken **ikisi** (PAD ve PQA) Bash
komutlarında onay ekranına düştü ve orada **bekledi.** PAD 44 dakika
(17:43→18:27), PQA benzer sürede. Onayları Mert elle verdi.

## Clara'nın ilk teşhisi — doğru ama YÜZEYSEL

`agent-project/.claude/settings.local.json`'da `Bash` için tek açık kural
`Bash(env)` ve 2026-08-06'dan kalma artık var olmayan bir kutunun `mkdir`'i.
`Read` verilmiş, `Bash` verilmemiş.

Buna ek olarak komutların kendi biçimi de uyarı tetikledi: PAD'de değişken
atamasında `~` (*"Tilde in assignment value"*), PQA'da `/tmp`'ye heredoc.

**Bu teşhis yanlış değil ama yetersiz** — izin listesini genişletmek ya da
komut biçimini düzeltmek belirtiyi azaltır, sebebi kaldırmaz.

## Mert'in teşhisi — SEBEP

**Agent'lar açılırken auto mode'da değilse her araç çağrısı onay akışına
düşüyor.** Yani mesele tek tek komutların izinli olup olmaması değil, oturumun
hangi modda başlatıldığı.

Fark önemli: izin listesi **hangi komutun** sorulmayacağını belirler; oturum modu
**sorulup sorulmayacağını** belirler. Birincisi bir liste bakımı, ikincisi bir
başlatma parametresi — ve liste ne kadar uzatılırsa uzatılsın yanlış modda
açılmış bir oturum yine sorar.

## Clara'nın ölçüm hatası — kayda geçiyor

Sabah 17:04'te *"kanal ayakta, dördü de kurdu, iki yönlü test geçti"* denildi.
Ölçüm doğruydu ama **eksikti.**

Ölçülen: mesaj gidiyor mu, geliyor mu.
Ölçülmeyen: agent **iş yapabiliyor mu.**

İki yönlü test bir `send.py` çağrısıydı ve o zaten izinliydi — yani test tam da
**tıkanmayan yolu** sınadı. Kanal kurulumu agent'ların kendi kutularına yazmaktı;
asıl iş başka komutlar gerektiriyordu ve onlar hiç denenmemişti.

**Sorulmayan ayırt edici soru:** *"bu agent'lar hangi modda açıldı?"*

Bu, `kanal-kurulumu` skill'indeki *"doğrulanmamış altyapıya iş yüklenirse iş
yapılır ama bir yön sessiz kalabilir"* uyarısının yeni bir biçimi — orada
yön sessiz kalıyordu, burada **agent** sessiz kaldı.

## Neden bu bir ARGE kalemi

Üç şey ölçülmedi:

**1. Mod nasıl set ediliyor?** Oturum açılışında mı, ayarla mı, komut satırı
bayrağıyla mı. Mert'in gözlemi belirtiden çıktı, mekanizma doğrulanmadı.

**2. Mod kalıcı mı?** Bir agent yeniden başlatıldığında modu korunuyor mu, yoksa
her açılışta tekrar mı verilmeli. Fabrika agent'ları gün içinde birkaç kez
kapanıp açılıyor — kalıcı değilse bu her seferinde tekrarlanacak bir adım.

**3. Alt-agent'ta ne oluyor?** Ekosistemde bilinen bir örüntü var: hook'lar
alt-agent'ta çalışmıyor, `CLAUDE_CODE_AGENT` çağıranın adını taşıyor. Mod da
aynı sınıfta bir arıza gösteriyor olabilir.

## Bunun yanında duran ayrı boşluk

**Takılan agent bunu bildiremiyor.** Kanonda karşılığı yok (arandı:
`takil|blok|beklemede kal|ilerleyemi` → ilgili kural sıfır).

Ve bu kuralla **çözülemez** de: onay ekranı açıkken agent hiçbir şey yapamaz,
mesaj da yazamaz. Yani *"takılırsan bildir"* kuralı yazılırsa **var olmayan bir
mekanizmaya yaslanmış** olur — PCA'nın bugün emsalde bulduğu arıza sınıfının
aynısı.

**Tek çözüm merkezin ölçmesi:** kutunun kendi son yazım zamanı (kanonun zaten
onayladığı canlılık sinyali). Sinyal Clara'nın elindeydi, kullanılmadı.

## Sonraki adım

Mod mekanizması ölçülecek: nasıl set edilir, kalıcı mı, alt-agent'ta geçerli mi.
Ölçüm sonucu bir karar kalemi üretirse `kararlar/` altına gider.
