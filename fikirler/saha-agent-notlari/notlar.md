# Saha agent notları — Mert'in gözlemleri

> **Durum:** AÇIK · biriktirme modunda
> **Başlangıç:** 2026-08-10
> **Ne bu:** Mert sahada çalışan agent'larda gördüğü aksaklıkları not olarak veriyor.
> Tartışma sonraya; şimdilik her not kaydedilir + ölçülür + ön hipotez çıkarılır.
> Toplu değerlendirmede örüntüye bakılacak, sonra skill'e dönecek.

**Nasıl işler:** Mert bir not atar → Clara notu ham hâliyle yazar, mümkünse ÖLÇER,
ön hipotez ve ölçüm önerisi ekler. Cevap beklenmez, tartışma açılmaz.

---

## NOT 1 — Agent'lar sürekli Bash/python yazıyor, Write/Read es geçiliyor

**Mert'in cümlesi (2026-08-10 12:54):**
> "Bash python çok fazla yazılmaya başladı. Agentlar python yazıyor sürekli.
> Write read komutları es geçilmeye başladı ve kontrolsüz komutlar yazılmaya başlandı."

### Ölçüm — YAPILDI

Kaynak: `~/.claude/projects/*/*.jsonl` transcript'leri, 2026-08-10 tarihli aktif
oturumlar. Sayılan şey: `tool_use` blokları, araç adına göre.

| Oturum | Toplam araç | Bash | Bash içinde python | heredoc | Read | Write | Edit |
|---|---|---|---|---|---|---|---|
| agent-project (46abe430) | 272 | 186 (%68) | 133 (%71 of Bash) | 33 | 17 | 1 | 1 |
| goat (1f0127b3) | 338 | 204 (%60) | 35 | 22 | 11 | 9 | 36 |
| liston (9421f3d2) | 110 | 69 (%63) | 3 | 0 | 7 | 5 | 7 |
| egelisaglik (acdbcc06) | 45 | 29 (%64) | 0 | 0 | 6 | 1 | 2 |
| web-template-next | 20 | 9 | 0 | 0 | 1 | 0 | 0 |

**Gözlem doğrulandı:** Bash her oturumda araç kullanımının %60-68'i.

### Ama sebep TEK DEĞİL — iki ayrı şey karışıyor

**(a) Kanal betikleri — bizim kendi kurduğumuz düzen, arıza DEĞİL.**
`agent-project` oturumundaki 133 python'ın **78'i** (kanal betiği 38 + hazır betik
çağrısı 40) `send.py` / `read.py` / `setup.py` / `watch.py` çağrısı. Goat'ta 35'in
**29'u** aynı. Agent burada python *yazmıyor*, bizim yazdığımız betiği *çağırıyor*.

→ Bunlar "kontrolsüz komut" değil. Ama Bash sayısını şişirip asıl arızayı
görünmez kılıyorlar. **Ölçüm yaparken ayrılmazsa yanlış teşhis çıkar.**

**(b) Inline python heredoc — ASIL ARIZA.**
`agent-project` 33, goat 22 heredoc bloğu. Örnek (goat, gerçek komut):

```
python3 - << 'PYEOF'
import re
p = "docs/_project/SPRINT-CALISMA.md"
s = open(p, encoding="utf-8").read()
old = "| H2 | 🔴 **BE BUG — boş bonus null yerine 0 kaydediliyor** | _bekliyor_ |"
...
```

Bu tam olarak **Edit'in işi**. Edit'te olan ve burada olmayan üç güvence:
- **Önce oku zorunluluğu** — Edit, okunmamış dosyayı düzenlemeyi reddeder
- **Tam eşleşme kontrolü** — eşleşmezse hata verir; python `.replace()` sessizce hiçbir şey yapmaz
- **Harness dosya takibi** — Write/Edit dosya durumunu bildirir, Bash bildirmez

→ Yani agent kendi yazdığını izlemiyor ve sessiz hata mümkün.

### Ön hipotez — ÖLÇÜLMEDİ, çıkarım

Agent'lar Bash'e kaçıyor çünkü **Read/Edit tek dosya üzerinde çalışıyor**, oysa
yapılan iş çoğunlukla çoklu: "şu 40 ID'yi say", "şu üç dosyada şunu değiştir",
"bu dizinde kaç kural var". Tek araçla yapılamayan işi tek Bash satırına sıkıştırmak
cazip ve çoğu zaman **doğru** — grep bir ölçüm aracı, Read değil.

Yani sebep tembellik değil **araç-iş uyumsuzluğu**. Ve `CLA-FIX-THE-CAUSE` gereği
çözüm *"python yazma"* kuralı olamaz — o yama olur, uyumsuzluk yerinde kalır.

### Ayıran soru (öneri temeli)

**Bash komutu OKUYOR mu, YAZIYOR mu?**
- **Okuyor** (grep, find, wc, ls, git log) → serbest, hatta doğru araç
- **Yazıyor** (`open(...,'w')`, `.replace()` + yaz, `sed -i`, `>` yönlendirme) → burada
  Write/Edit olmalı; sessiz hata riski var ve harness takibi kayboluyor

Bu ayrım ölçülebilir ve otomatik denetlenebilir.

### Ölçüm önerileri (henüz yapılmadı)

1. **Yazan-Bash sayısı:** tüm oturumlarda dosyaya yazan Bash komutlarını ayıkla —
   kaç tanesi Write/Edit ile yapılabilirdi?
2. **Sessiz hata avı:** heredoc python'la yapılan düzenlemelerin kaçı `.replace()`
   sonrası doğrulama yapmadan bitti? (eşleşme olmasa da rc=0 döner)
3. **Kanal betiği yükü:** kanal python çağrılarının Bash içindeki payı — düzen
   değişse (betik yerine araç) bu yük ne kadar düşer?

---

## NOT 2 — Agent açılış hook'u permission modunu auto'ya çevirmeli

**Mert'in cümlesi (2026-08-10 13:06):**
> "agentların açılışında çalışan hook permission modu auto ya çevirmeli."

**İkinci cümlesi (13:07):**
> "Pluginlerde bunu yapamıyoruz bunu sen araştırıp bulmuştun"

### Ölçüm — İLK CEVAP YANLIŞTI, DÜZELTİLDİ (2026-08-11)

**İlk ölçüm (2026-08-10):** `~/.claude/settings.json` → `permissions.defaultMode`
= `auto`. Sonuç: *"global zaten auto, hook'a gerek yok, notun zemini yanlış."*

**⚠️ BU CEVAP YANLIŞTI.** Ayar dosyasını okumak, sahadaki davranışı ölçmek değil.

**İkinci ölçüm (2026-08-11, Mert *"agent'lar hep default mode'da açılıyor ama"*
dedikten sonra)** — canlı oturumların transcript'lerindeki `permissionMode` alanı:

```
2919d16b  default     ← goat agent
fd73df88  default     ← Clara (profil üzerinden)
889bd436  default
de921937  default
d163aa0e  default
fff17836  auto        ← YALNIZ BU (izleyen Clara, doğrudan açılmış)
```

**Altı oturumun beşi `default`.** Global ayar `auto` diyor ama **sahaya geçmiyor.**

### Sebep — SCRUB, ve üç şey birbirine bağlıymış

`settings.json` → `env: {"CLAUDE_CODE_SUBPROCESS_ENV_SCRUB": "1"}`

SCRUB alt süreçlere geçen ortamı temizliyor (kimlik sızıntısına karşı gerçek bir
koruma — `SSH_AUTH_SOCK`, `GEMINI_CLI_IDE_AUTH_TOKEN` gibi değerler bu ortamda
duruyor). **Ama permission modu da o temizliğe takılıyor.**

- VS Code profilleri agent'ı `zsh -c` ile açıyor → **alt süreç** → mod varsayılana düşüyor
- Doğrudan açılan oturum (izleyen Clara) → `auto` alıyor
- `--permission-mode auto` bayrağı eklendi (2026-08-11) → **SCRUB ezdi**, uyarı bastı:
  *"Permission mode forced to default — CLAUDE_CODE_SUBPROCESS_ENV_SCRUB is set"*

Anthropic'in kendi kaydında bilinen hata: **issue #51258** — *"SCRUB permission
mode'u ezmemeli, ikisi bağımsız konular."*

### Mert'in notu HAKLIYDI

Not şuydu: *"agent'ların açılışında çalışan hook permission modu auto'ya
çevirmeli."* İlk cevap *"gerek yok, zaten auto"* oldu — **ölçülmeden reddedildi.**

→ **Ders (`feedback_olcum_yerine_yorum`'un tam vakası):** ayar dosyasını okumak
davranışı ölçmek değil. *"Yapılandırmada şu yazıyor"* ile *"sahada şu oluyor"*
farklı iki iddia; ikincisi ölçülmeden birincisiyle cevap verilmez.

→ Ve `CLA-LABEL-YOUR-EVIDENCE` ihlali: *"okudum"* ile *"ölçtüm"* karıştırıldı.

### Plugin sınırı — DOĞRULANMADI

Mert *"pluginlerde bunu yapamıyoruz, sen araştırmıştın"* dedi. Repo genelinde
arandı (`permission`, `plugin+izin`, `settings+plugin`): **böyle bir kayıt YOK.**

Bulunan tek yakın kayıt — `gunluk/fabrika/2026-08-07.md:85`:
> `setup-ozelyazilim-plugin` izin verilmeyen `disable-model-invocation` alanı taşıyor.

Farklı alan, ama **aynı ailede bir sınır**: plugin manifest'i her ayarı taşıyamıyor.

**İki ihtimal, ayırt edilemedi:**
- Araştırma yapıldı ama **yazılmadı** → `CLA-WRITE-BEFORE-CLOSE` ihlali, bedeli bu an
- Başka bir oturumda konuşuldu, bu repoya hiç girmedi

**Mert'in hatırladığı büyük ihtimalle doğru** ve mekaniği mantıklı: plugin kullanıcının
güvenlik ayarını değiştirebilseydi, bir plugin kurmak izin kapısını sessizce açardı.
Yani `permissions` bloğu plugin'den değil kullanıcı `settings.json`'ından gelir.

### İki itiraz

**(1) Bu bir yama olur.** Hook'la modu auto'ya çevirmek = izin kapısını her açılışta
zorla açmak. Sebebi kaldırmıyor, üstüne katman koyuyor (`CLA-FIX-THE-CAUSE`).

**(2) Kanona aykırı.** Clara izin kuralı ve permission ayarı yazmaz — tek düzeltme
değil, kapıyı kalıcı açar.

### Asıl soru bu değil

Doğru soru: **"agent hangi anda izin soruyor ve o an ne yapıyordu?"**

**NOT 1 ile bağlantı — muhtemel örüntü:** Agent'lar Bash'e kaçıyor ve **Bash izin
isteyen araç**; Read/Edit istemiyor. İzin sürtünmesi ile python'a kaçış aynı arızanın
iki yüzü olabilir. Ama tersi de mümkün: Bash'e kaçış izin sorusunu ÇOĞALTIYOR olabilir.
Hangisi sebep hangisi sonuç — ölçülmedi.

### Ölçüm önerileri (henüz yapılmadı)

1. **Plugin sınırını fiilen ölç:** test plugin'ine `permissions` bloğu koy, yüklenip
   yüklenmediğine bak. Tahminle geçme.
2. **İzin sorusu envanteri:** transcript'lerde izin istemi geçen anları çıkar — hangi
   araç, hangi komut, agent o an ne yapıyordu?
3. **Alt-agent miras kontrolü:** `Agent`/`Task` ile açılan alt-agent izin modunu miras
   alıyor mu, yoksa kendi varsayılanına mı düşüyor?

---

## NOT 3 — Goat'ta PA + Clara birlikte çalıştırma denemesi başarısız

**Mert'in cümlesi (2026-08-10 13:16):**
> "Goat da PA ile Clara yı çalıştırmaya çalıştım ama büyük bir başarısızlık çıktı"

**Düzeltmesi (13:25) — Clara'nın ilk teşhisi YANLIŞTI:**
> "Başarısız olan şey kurulum değildi haklısın. Başarısız olan şey çalışma şekliydi.
> 1. Clara çalıştığı projeye hiç hakimiyet kurmadı
> 2. Clara aldığı soruları netleşmesi için PA'yi hiç çalıştırmadı. Gelen mesajı
> geldiği gibi okudu ve bana özet sorular sordu. Ne gelen mesajı okuyabildim ne
> Clara'nın önerilerini — Clara bana haberci güvenlik görevlisi yaptı. İstediğimiz
> şey bu değildi. Bana karar vermemi kolaylaştıracak güzel brief vermesiydi.
> Anlaşılamayan ya da yetersiz olan bilgiyi PA ile konuşup netlemesiydi."

### Clara'nın ilk teşhisi — YANLIŞ, kayda geçiyor

İlk ölçümde şu denildi: *"kanal teknik olarak çalıştı, başarısız olan hızdı; tek agent
varken aracı katman israftır."*

**Bu yanlıştı ve neden yanlış olduğu önemli:** ölçüm mesajların SAYISINA baktı,
İÇERİĞİNE bakmadı. Sayı "katman gereksiz" diyordu; içerik "katman işini yapmadı"
diyor. İkisi zıt sonuç veriyor — birincisi katmanı kaldırır, ikincisi düzeltir.

→ **Ders:** bir katmanın değerini ölçerken geçen trafiği değil, **taşıdığı içeriği**
oku. Trafik sayısı katmanın işe yarayıp yaramadığını göstermez.

### Ölçüm — YAPILDI (ikinci tur, içerik okunarak)

Kaynak: `~/.pr-kanal/goat/PA-20260809-0907/inbox` — Clara'nın PA'ya yazdığı
**10 mesajın tam metni** + goat oturumu transcript'i (338 araç çağrısı).

**Zaman çizgisi:**
- 06:06 — kanal kuruldu (Clara → PA devir bloğu)
- 06:07-06:08 — PA kutusunu kurdu, izleyici canlı, iki yönlü test geçti
- 06:12 → 08:29 — sprint planlaması kanal üzerinden yürüdü
- 08:29 — **Mert kesti:** *"PA, Clara oturumu kapattı... seninle Clara işi yavaşlattı.
  Bekleyen bir sürü taskimiz var, planlamaya devam edelim. Monitörünü kapatabilirsin."*

**Süre: 2 saat 23 dakika. O sürede kapanan tur: 1 (Tur 3).** Öncesinde Mert doğrudan
konuşurken aynı PA saatte 2-3 tur kapatıyordu.

### Üç bulgu — Mert'in teşhisi doğrulandı

**BULGU 1 — Clara projeye hiç hakimiyet kurmadı.**

Clara'nın 10 mesajında geçen her teknik detay **PA'nın raporundan geri okunmuş**:
`JoinRequestForWheelOperationHandler`, `GUVENLIK-BORC §9`, mapping'in 7 noktası,
`PRY-15941` etki analizi sınırı. Clara'nın kendi okumasından gelen tek dosya adı yok.

→ Sonuç: Clara PA'nın söylediğini PA'ya tekrar etti. **Hakimiyet olmayınca "bu bilgi
yetersiz" diyebilecek zemin de yok** — yetersizliği ancak konuyu bilen fark eder.

**BULGU 2 — Sorular soruldu ama YANLIŞ TÜRDEN.**

10 mesajın 4'ü QUESTION/doğrulama. Ama hepsi **süreç sorusu**:
- *"mesajı aldın mı"* (155543)
- *"izleyicin çalışıyor mu"* (155543)
- *"CA'ya ne gönderdin"* (094605)
- *"kaç task inceledin, kaçı kaldı"* (093555)

Mert'in beklediği **içerik sorusu** — *"bu gereksinim şurada muğlak, netleştir"*,
*"bu cevap yetersiz, kodda karşılığı ne"* — **bir kez bile sorulmadı.**

→ Clara zincirin SAĞLIĞINI ölçtü, işin İÇERİĞİNİ ölçmedi. İkisi farklı iş.

**BULGU 3 — Brief iki ucundan da kesildi.**

17:26 mesajında Clara PA'ya diyor ki: *"brief'i tam metin gönder, ÖZETLEME,
KISALTMA"* — doğru talimat. PA 6222 karakterlik tam brief'i kanala koydu.
Sonra Clara o metni **Mert'e kendi cümleleriyle özetleyerek** aktardı.

→ Mert PA'nın metnini görmedi. Clara'nın kendi değerlendirmesi de yoktu.
**Geriye haberci kaldı** — Mert'in cümlesi: *"bana haberci güvenlik görevlisi yaptı."*

### Kök sebep

**Clara yönetim rolüne konuldu ama yönetim için gereken tek şeyi yapmadı:
işin kendisini öğrenmedi.**

Hakimiyet olmadan üç şey imkânsız hâle geliyor ve üçü de olmadı:
- Gelen bilginin yeterli olup olmadığını yargılamak → yargılamadı, olduğu gibi taşıdı
- Muğlak yeri görüp geri sormak → süreç sordu, içerik sormadı
- Karar için brief üretmek → özet üretti, brief değil

### Ayıran soru (öneri temeli)

Bir aracı katman kurulurken: **bu katman gelen bilgiye BİR ŞEY EKLİYOR mu?**

Eklemiyorsa iki ihtimal var ve karıştırılmamalı:
- Katman **gereksiz** (yalın üretim: kaldır)
- Katman **işini yapmıyor** (hakimiyet yok: düzelt)

Ayırt eden şey: katmanın çözmesi beklenen bir problem VAR MI? Goat'ta vardı —
Mert PA'nın ham çıktısını okumak istemiyordu, süzülmüş karar istiyordu. Yani
katman gerekliydi, **dolduramadı.**

### Ölçüm önerileri (henüz yapılmadı)

1. **Hakimiyet ölçüsü:** aracı Clara oturumunda projeye ait kaç dosya OKUNDU?
   (goat oturumunda: ölçülmedi, ama mesaj içeriğinden ~0 görünüyor)
2. **Soru tipi dağılımı:** aracı katmanın sorduğu soruların kaçı süreç, kaçı içerik?
   Bu oran bir sağlık göstergesi olabilir.
3. **Brief kalite testi:** Mert'e giden metin ile PA'nın ürettiği metin arasındaki
   kayıp — hangi bilgi düştü, düşen bilgi karar için gerekli miydi?

---

## Örüntü — üç notun kesişimi (ÖN, ölçülmedi)

**Ortak eksen: agent kendi işini ölçmüyor, akışı ölçüyor.**

- NOT 1: agent dosyaya yazıyor ama yazdığını doğrulamıyor (heredoc python, sessiz hata)
- NOT 2: izin sürtünmesi görülüyor ama hangi anda doğduğu ölçülmemiş
- NOT 3: aracı katman zincirin sağlığını ölçüyor, işin içeriğini ölçmüyor

Üçünde de aynı şey var: **süreç görünür, içerik görünmez.** Araç çağrısı sayılıyor,
mesaj sayılıyor, kutu kontrol ediliyor — ama üretilen şeyin doğru olup olmadığına
kimse bakmıyor.

Bu bir hipotez. Yeni notlar geldikçe tutup tutmadığı görülecek.

---

## Sonraki adım

Mert not göndermeye devam edecek. Toplu değerlendirme yapıldığında:
1. Ölçüm önerileri koşulur (özellikle NOT 2'nin plugin sınırı — tahminle geçilmeyecek)
2. Örüntü doğrulanır ya da düşer
3. Çıkan kural seti skill'e döner
