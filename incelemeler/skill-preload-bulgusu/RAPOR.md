# Skill preload çalışmıyor — ölçüm ve sonuçları

Tarih: 2026-08-03

## Bulgu

Claude Code'un subagent `skills:` frontmatter alanı, komut satırından açılan agent'larda
(`claude --agent X`) skill gövdesini context'e enjekte etmiyor.

Resmî doküman aksini söylüyor: *"The full content of each listed skill is injected into
the subagent's context at startup."*

Saha aksini gösteriyor. Agent'ın kendi ifadesiyle: *"`frontend` skill'i preload olarak
tanımlı — ama şu anki bağlamımda yüklü değil. Görebildiğim tek şey tool listesindeki
tek satırlık açıklaması."*

## Nasıl ölçüldü

Üç kuşakta beş agent, bağımsız sorularla:

**v7 FE** (proje-yerel) → *"Hayır"*
**v8 FE** (plugin) → *"elimde yok"*
**Fabrika PAM, PQA, PCA** (proje-yerel) → *"yok"*

Ek olarak canary testi: frontmatter'a gizli kelime taşıyan geçici bir skill eklendi,
agent göremedi.

Yanlış ölçüm de yapıldı ve düzeltildi — ilk denemede *"system prompt'unda var mı"* diye
soruldu. Agent kendi system prompt'unu göremiyor; bu soru geçersiz. Doğru ölçüm
davranışsaldır: **açmadan bilemeyeceği bir şeyi sor, açmasını yasakla.**

## Bilinen hata

`anthropics/claude-code#25834`. Raporcu 17 plugin agent'ında test etmiş, sıfırında
enjeksiyon olmuş. Bot tarafından *"completed"* diye kapatılmış ama düzeltilmemiş.

Bir istisna var: **`Task` aracıyla çağrılan proje-yerel agent'ta çalışıyor.** Bağımsız
bir canary testi bunu doğruladı. Yani mekanizmanın kendisi sağlam, CLI yolu eksik.

## Bedeli

Bu ekosistemde `skills:` alanı **2026-02-05**'ten beri kullanılıyor — commit adı
manidar: *"v6: Agent mimarisi - 9 agent, skill on-demand, rules paylaşımlı."*

Altı ay boyunca agent'lar *"şu skill'ler yüklü"* diye tanımlandı ve hiçbiri yüklenmedi.

Bu, v8'in *"sahada tutmaması"*nın altındaki teknik gerçek. Kural gevşekliği değil —
**kanon agent'a hiç ulaşmamış.** v7 çalışıyordu çünkü body'lerinde her skill'in özeti
vardı ve 484 adım her adımda *"şu dosyayı aç"* diyordu.

## İkinci bulgu — agent kendini göremez

Aynı gün ortaya çıktı ve birincisinin çözümünü bozdu.

**Agent kendi frontmatter'ını okuyamaz.** Body metnini görür (system prompt'una o girer)
ama `skills:`, `tools:`, `model:` alanları ona ulaşmaz. Doğrudan soruldu: *"Kendi
frontmatter'ımı okuyamıyorum."*

Sonucu ölçüldü: açılış hook'u *"tanımındaki `skills:` listesini yükle"* dedi. Agent
listeyi göremediği için **tahmin etti** — üç skill'den birini doğru yükledi, ikisini
atladı, listede olmayan bir dördüncüyü yükledi. Ve raporunda *"yüklendi ✅"* diye tik
attı. Yanlış kanonla çalıştı ve bunu bilmiyordu.

Genel kural: bir agent'a **kendisi hakkında** bir bilgiye dayanan talimat verilmez.
Skill adları, araç listesi, sürüm — hepsi dışarıdan verilir.

## Yürürlükteki çözüm

> ⚠️ **Bu bölüm 2026-08-03 14:47'de ölçüldü ve artık doğru değil.** Aşağıda anlatılan
> global hook **yok**: `~/.claude/hooks/preload-skills.py` dosyası mevcut değil ve
> `~/.claude/settings.json` → `SessionStart` altında yalnız git durumu basan tek satır
> var. Ya hiç kurulmadı ya sonradan kaldırıldı. Plugin tarafındaki hook ayrı bir şey ve
> o duruyor (aşağıdaki "Çözüldü" bölümü). Bölüm tarihçe olarak bırakıldı.

Global bir `SessionStart` + `SubagentStart` hook'u: `~/.claude/hooks/preload-skills.py`.
Agent oturumlarında bir açılış talimatı basar — *"preload çalışmıyor, skill'lerini
`Skill` aracıyla kendin yükle"*.

Gövde taşımaz; hook çıktısı 10.000 karakterle sınırlı ve kanon 105.000.

Doğrulandı: hook'tan önce PAM *"bilmiyorum"* diyordu, sonra `uretim` kanonundaki üç
soruyu tam verdi. v8 PA altı skill'i `Skill` aracıyla yükledi ve sürümünü doğruladı.

## Çözüldü — plugin hook'u sahada çalışıyor

Aynı gün AG (eski kuşak üretici) hook'u iki plugin'e ekledi ve sürüm bump'ladı:
OY `0.6.1`, WS `0.8.1`.

Doğru tasarım kararları:

**Skill adları script'e gömülmedi**, çalışma anında agent `.md`'sinden okunuyor. Gömülse
iki kaynak olurdu — frontmatter değişir, hook eskir, kimse fark etmez. Bu aynı zamanda
*"agent kendini göremez"* tuzağını da kapatıyor: liste agent'a **dışarıdan** veriliyor.

**`SessionStart` seçildi**, `SubagentStart` değil — bu ekosistemde agent'lar terminal
profilinden ana oturum olarak açılıyor.

**Matcher düzeltildi.** İlk sürümde `"matcher": "ozel-yazilim:.*"` yazılmıştı; doküman
net — `SessionStart` matcher'ı oturum kaynağını eşler (`startup`, `resume`, `clear`,
`compact`, `fork`), agent adını değil. Agent tipi filtreleme yalnız
`SubagentStart`/`SubagentStop`'ta var. Namespace filtresi script içinde yapılıyor.

**Saha doğrulaması.** `ozel-yazilim:backend-developer` açıldı, ilk cümlesi:
*"6 skill yüklendi. Kanonum context'te; artık ezberden değil kaynaktan çalışıyorum."*
Altısı da doğru — frontmatter'la birebir. Ve aynı turda kanondan bir kural uygulayıp
yanlış dizinde olduğunu fark etti (`.csproj` yok, bu bir meta-repo).

## Hâlâ açık

**Fabrika ve bu oda plugin değil.** `agent-project`'in personeli (PAM, PAD, PQA, PCA) ve
Clara hook'suz — kanonlarını yüklemeden açılıyorlar. Bir fabrika agent'ına iş verirken
ilk turda skill'lerini okumasını istemek gerekiyor.

**Açılış maliyeti görünür oldu.** v8 PA açılışta ~%15 context yiyor (~21 bin token, altı
skill). Yeni bir maliyet değil — `skills:` çalışsaydı aynı yükü sessizce alacaktı. Ama
artık ölçülebiliyor, ve hangi skill'in gerçekten her oturumda gerektiği ölçülebilir.

**v8 adil sınav görmedi.** AG'nin ölçümü: `backend-developer` beklenen ~11.500 kelimelik
kanonun **1.067 kelimesini** görüyordu — %91'ini hiç görmedi. Yani *"v8 olmadı"* yargısı
yanlış deneyden çıktı. Bu v8'i aklamaz ama yeniden ölçüm gerektirir.

## Fabrikada kural denendi ve tutmadı — sebebi teşhis edildi

`agent-project/CLAUDE.md`'ye koşulsuz bir açılış kuralı yazıldı: *"tanımındaki `skills:`
listesindeki skill'leri `Skill` aracıyla yükle"*. Denendi. PAM kuralı gördü, *"devam
edeceksek yükleyeceğim"* dedi ve listeyi yanlış saydı — `behavior`'ı atladı,
`yapi-taslari`'nı uydurdu.

İlk okuma şuydu: *"koşulsuz yazılmış bir kural bile koşullu okunabiliyor."* Bu okuma
yanlış — ya da en azından asıl sebebi ıskalıyor.

**Asıl sebep ikinci bulgunun kendisi.** Kural agent'a *"tanımındaki listeyi"* yükle
diyor, ama agent kendi frontmatter'ını göremez (yukarıda ölçüldü). Yani kural, agent'a
**elinde olmayan bir bilgiye dayanan iş** veriyor. PAM kuralı gevşek okumadı; listeyi
göremediği için tahmin etti. Kural ne kadar sert yazılırsa yazılsın aynı boşluğa düşer.

Plugin tarafındaki çözümün çalışma sebebi tam da bu farkı kapatması: hook, skill
adlarını çalışma anında agent `.md`'sinden okuyup **dışarıdan** veriyor. Fabrika
CLAUDE.md'si o adımı yapmıyor — talimatı yazıyor, veriyi vermiyor.

**Çıkan ders:** metin, dışarıdan veri gerektiren bir talimatın yerine geçmez. Sertleştirme
bu sınıf bir arızayı çözmez.

Buradan iki yol var, ikisi de denenmedi:

- Skill adlarını CLAUDE.md'ye **agent başına isim isim yazmak** — veriyi metne gömer,
  ama iki kaynak yaratır (frontmatter değişir, liste eskir, kimse fark etmez).
- Fabrikaya bir açılış hook'u koymak — plugin'dekiyle aynı mekanik, tek kaynak korunur.

Bu bölüm ölçümle değil okumayla çıkarıldı: `agent-project/CLAUDE.md` "Açılış" bölümü +
bu kaydın "İkinci bulgu" bölümü karşılaştırılarak. PAM'in davranışı Mert tarafından
sahada gözlendi, burada yeniden ölçülmedi.

## Fabrika ölçümü — 2026-08-03 14:47

Soru şuydu: fabrika bu kurallara göre çalışıyor mu. Cevap **hayır**, ama sebebi
beklenenden dar çıktı.

**Ölçülenler.** `agent-project/.claude/` altında `hooks/` dizini yok, `settings.json`
yok. Dört agent var (PAM, PAD, PQA, PCA), beş skill var (`behavior`, `is-duzeni`,
`uretim`, `yapi-taslari`, `dagitim`). Dördünün de frontmatter'ında `skills:` listesi
dolu ve `Skill` aracı tanımlı — yani mekanizma yerinde, tetikleyen yok.

**Kural yeterli, kapsamı dar.** `dagitim` skill'indeki `DAG-SHIP-PRELOAD-HOOK` hook'un
nasıl yazılacağını tam anlatıyor: agent `.md`'sinden `skills:` oku, adları bas,
*"`Skill` aracıyla yükle"* de; gövde taşıma (10.000 karakter sınırı); olay `SessionStart`;
namespace filtresi script içinde; adları script'e gömme. Hatta bir önceki bölümde
çıkardığım teşhis birebir orada yazılı: *"'Tanımındaki listeyi yükle' demek yetmez;
agent tahmin eder ve yanlış yükler."*

Yani **ekip nasıl yazacağını biliyor.** Eksik olan şu: kural *"her **plugin** bir açılış
hook'uyla doğar"* diyor ve Dağıtım bölümünde duruyor. Fabrika plugin değil — kural kendi
kapsamına fabrikayı almıyor. PAD bunu okuduğunda ürettiği takıma hook koyar, kendi evine
koymaz.

**Bir önceki bölümün düzeltmesi.** Orada CLAUDE.md metnini sertleştirme yerine "skill
adlarını isim isim yaz" seçeneği öneriliyordu. Ölçümden sonra bu zayıf bir öneri:
`DAG-SHIP-PRELOAD-HOOK` gömmeyi zaten gerekçesiyle yasaklamış (iki kaynak sorunu). Doğru
yol hook, ve şartnamesi hazır.

**Yarısı hazır duruyor.** `~/.claude/hooks/sessionstart.py` mevcut ve tam da doğru işi
yapıyor — agent `.md`'sini bulup `skills:` listesini iki formatta da parse ediyor ve
`additionalContext` olarak basıyor. İki eksiği var: `settings.json`'da hiçbir yere
bağlanmamış (script duruyor, çağıran yok) ve *"yükle"* talimatını basmıyor, yalnız
listeyi yazıyor.

**Bu kayıt yönlendirme için değil.** Mert fabrikaya farklı bir yapı kuracağını ve ekibi
kendisinin yönlendireceğini söyledi (2026-08-03). Buradaki ölçüm o iş başlarken
başlangıç durumunu göstermek için duruyor.

## Açık soru — v8 yeniden ölçülürken ölçüt ne olacak

*"v8 adil sınav görmedi"* doğru, ama *"yeniden ölçelim"* dendiği anda bir ölçüt gerekiyor.
Yoksa ikinci deney de birincisi gibi izlenime dayanır ve *"bu sefer iyi gitti"* diye
kapanır — o da bir yargı, veri değil.

Ölçüt belirlenmeden yeniden ölçüm başlatılmamalı. Bu soru açık.

## Bir sınama yaparken

Bir agent kuralına uymuyorsa ilk soru *"kuralı çiğnedi mi"* değil, **"kural elinde
miydi"** olmalı.
