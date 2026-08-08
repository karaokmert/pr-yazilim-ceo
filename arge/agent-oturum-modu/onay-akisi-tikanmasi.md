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

---

## İKİNCİ VAKA — ölü monitör (22:18)

Aynı gün, aynı sınıf, **farklı mekanizma.**

**PCA'nın monitörü 19:06'da öldü** (task killed). PCA bunu **22:18'de** fark
etti — üç saat dinlemiyordu. Kutusu duruyordu, mesajları birikiyordu, dışarıdan
her şey normal görünüyordu.

**PCA'nın cümlesi bulgunun kendisi:** *"kutu duruyor olması dinliyor olmam demek
değil."*

### Neden PAD vakasından daha sinsi

```
PAD  (17:43→18:27)  onay ekranında asılı   → bir İNSAN ekranda gördü
PCA  (19:06→22:18)  dinleyici ölmüş        → görülecek HİÇBİR ŞEY yok
```

Onay ekranı en azından bir yerde duruyor. Ölü monitörün hiçbir görünür izi yok —
ve kanal tarafında sessizlik yine *"çalışıyor"* ile aynı görünüyor.

### Bu, Clara'nın çözümünü de deliyor

18:27'de şu karara varılmıştı: *"izin-bekleme hâlini yalnız MERKEZ ölçebilir."*
Ama **merkez de bir monitöre güveniyor** — ve Clara'nın izleyicisi de bugün
öldü (oturum yeniden başladığında yok olmuştu).

Yani: *"merkez ölçer"* çözümü, **merkezin ölçüm aracının canlı olduğunu
varsayıyor.** Doğrulanmamış bir mekanizmaya yaslanmak — PAM'in bugün kanona aday
gösterdiği desenin ta kendisi: *"doğrulanmamış bir mekanizmaya yaslanmak hiç
korumadan KÖTÜDÜR, çünkü koruma varmış gibi görünür."*

**Eksik olan katman:** monitörün kendisinin canlılığını kim ölçüyor? Bugün
cevap: **hiç kimse.** İki uç da kendi kendine fark etti (PCA kendi monitörünü,
Clara oturum yeniden başlarken).

### Filtre düzeltmesi — iki uç bağımsız aynı yere vardı

PCA ve Clara **aynı anda** filtreye Türkçe deseni ekledi:

```
önce   'from=|ERROR:|INFO:|watcher started'
sonra  'from=|ERROR:|INFO:|HATA:|BILGI:|watcher started'
```

**PCA'nın gerekçesi bir filtre ayarından fazlası** — ölçülemeyen bir
belirsizlikte hangi tarafa yanılmak gerektiğini söylüyor:

> *"Yanlış olan desen zarar vermez (hiç eşleşmez), EKSİK olan desen sessizliğe
> dönüşür. Asimetrik maliyet, ucuz taraf seçilir."*

### Açık ölçüm

`Monitor`'ün **otomatik durdurma eşiği** kanal kanonunda *"ölçülmedi"* diye
işaretli. PCA'nın vakası o eşiğin **ilk gerçek verisi** olabilir — kendi
kutusundaki kanıttan (ölmeden önce kaç olay bağırdı, hangi aralıkta) ölçmesi
istendi. Üç uca da monitör kontrolü gönderildi (22:19); üçünün verisi bir araya
gelince *"monitör ne sıklıkta ölüyor"* sorusunun ilk cevabı çıkacak.
