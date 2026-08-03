# Token tüketimi neden arttı — 2-3 Ağustos ölçümü

Tarih: 2026-08-04

Mert: *"Son zamanlarda çok fazla token tüketmeye başladım, sürekli limitim doluyor.
2 ve 3 Ağustos'taki oturumlara bakalım."*

## Kaynak

`session-report` plugin'inin analizörü (`analyze-sessions.mjs --since 7d`), ham çıktı
`/tmp/session-report.json` (456 KB). Girdi: `~/.claude/projects/` altındaki JSONL
oturum kayıtları.

Sonra en pahalı beş oturumun transcript'i ayrıca tarandı (araç dağılımı için).

**Not: bu sayı oturumun hangi klasörde açıldığını söyler, işin nerede yapıldığını
değil.**

## Günlük tablo — artış gerçek

```
2026-07-28 Tue     723,857,520   14.9%   39 oturum
2026-07-29 Wed     120,126,649    2.5%   29 oturum
2026-07-30 Thu     597,716,350   12.3%   23 oturum
2026-07-31 Fri     933,438,688   19.2%   54 oturum
2026-08-01 Sat     541,652,646   11.2%    2 oturum
2026-08-02 Sun     749,433,370   15.4%   31 oturum
2026-08-03 Mon   1,179,785,931   24.3%  122 oturum
```

Haftanın toplamı 4,85 milyar token. **3 Ağustos tek başına %24,3** ve 122 oturum —
haftanın en yüksek günü.

Dikkat çeken kontrast: 1 Ağustos'ta **2 oturum** 541 milyon token yaktı; 3 Ağustos'ta
122 oturum 1,18 milyar. Yani oturum sayısı tüketimi açıklamıyor.

## Sebep — uzun oturum, çok Bash

En pahalı beş oturumun araç dağılımı:

**egelisaglik 08-02 (`63a3e5ae`)** — 270,8 milyon token, **1143 dakika (19 saat)**,
439 araç çağrısı: Bash 236, Edit 119, Write 54, Read 30.

**goat 08-03 (`14da9519`)** — 140,7 milyon, 323 dk, 320 çağrı: Bash 209, Edit 60,
Read 22.

**egelisaglik 08-03 (`4f61a4df`)** — 126,4 milyon, 798 dk (13 saat), 261 çağrı:
Bash 217.

**egelisaglik 08-02 (`b061e113`)** — 94,7 milyon, **yalnız 114 dk**, 378 çağrı:
Bash 150 + **Playwright 121** (evaluate 62, click 33, type 15, navigate 11).

**goat 08-03 (`1e552217`)** — 79 milyon, **yalnız 86 dk**, 229 çağrı: Bash 115 +
Playwright 15.

Örüntü tek: **her oturumda 100-240 arası Bash çağrısı.** Ve mekanik şu — her araç
çağrısı bir API turu demek, her API turu o ana kadarki **tüm bağlamı** yeniden
gönderiyor. 236 Bash çağrısı = 236 kez bağlamın tekrar okunması.

Bu yüzden cache-read %96,3: bağlam sürekli yeniden okunuyor, ama önbellekten.

## İkinci sebep — cache break

Haftada **343 kez** 100k üzeri cache break. Dağılım: egelisaglik 44, skill-project 28,
goat 12, osinif 8.

Cache break, bağlamın önbellekten düşüp **baştan kurulması** demek. Uzun oturumlarda
sık oluyor ve her seferinde tam bedel ödeniyor.

## Üçüncü sebep — "bitene kadar devam et" kalıbı

En pahalı üç prompt'un üçü de aynı biçimde ve hepsi `egelisaglik`:

> *"okey o zaman devam edelim. test tüm işler bitince her şeyi bitirelim öyle"* —
> 91,8 milyon token (%1,89)

> *"be dev de iste playwright ile sen test et. Veri gerirse anlamlı üret."* —
> 68,9 milyon (%1,42)

> *"her panelde işi bitir sonra toplu test yapacağız"* — 46,8 milyon (%0,97)

Üçü toplam **%4,3**. Bu kalıp bir oturumu 13-19 saate uzatıyor ve bağlamı sürekli
büyütüyor: her yeni panel önceki tüm panellerin bağlamını taşıyor.

## Playwright oturumlarının verimsizliği

`b061e113`: 114 dakikada 94,7 milyon token. Karşılaştırma: `4f61a4df` 798 dakikada
126,4 milyon.

Yani **dakika başına 7 kat daha pahalı.** Sebep Playwright: her `browser_snapshot` ve
`browser_evaluate` sayfanın tam DOM'unu bağlama sokuyor, ve o bağlam sonraki her
çağrıda tekrar gönderiliyor.

62 kez `browser_evaluate` çağrılmış. Her biri bir öncekinin çıktısını taşıyor.

## Clara'nın payı

`pr-yazilim-ceo` bu oturum (`4a51f312`) 08-03'te 64 milyon token — günün 8. en pahalı
oturumu, %5,4'ü.

Sebebi bu oturumda dört kez paralel tarama açılması: subagent ortalaması **1,43 milyon
token/çağrı**, 262 çağrı, toplam 375 milyon (haftanın %7,7'si).

Yani paralel tarama işe yaradı ama pahalı. Ölçüt: `clara.md`'deki *"cevap bir sayıya mı
yargıya mı dayanıyor"* sorusu — yargıysa tarama açmadan konuşulur.

## Ne yapılabilir — dört madde

**Bir: oturumu böl.** *"Tüm paneller bitene kadar devam"* yerine panel başına bir
oturum. 19 saatlik bir oturumun son saatinde bağlam ilk saatin 20 katı ve her araç
çağrısı o bedeli ödüyor.

Beklenen kazanç en büyük olan: `63a3e5ae` 270 milyon token yaktı; beş oturuma bölünse
her biri kendi bağlamıyla başlar.

**İki: Playwright'ı ayrı oturuma al.** Tarayıcı testi bağlamı şişiren en hızlı şey
(dakika başına 7 kat). Kod yazma ile test aynı oturumda olmasın.

**Üç: Bash çağrısını azalt.** 236 çağrı = 236 API turu. Birleştirilebilir komutlar
(`&&` ile zincirleme) tur sayısını düşürür. Bu bir agent davranışı, kanona
yazılabilir.

**Dört: `/compact` yerine yeni oturum.** Compact bağlamı özetliyor ama özet de bağlamda
kalıyor. Kapanış kaydı yazıp yeni oturum açmak daha temiz — ve bu zaten fabrikanın
`ISD-CONSOLIDATE-AT-END` kuralının yaptığı şey.

## Ölçülmeyen

**Gerçek para maliyeti.** 4,85 milyar token'ın %96'sı cache-read ve cache-read çok daha
ucuz. Yani token sayısı maliyeti doğrudan vermiyor — limit tarafı ayrı bir mekanik.

**`session-report` script'inin sayma yöntemi doğrulanmadı.** Özellikle `by_subagent_type`
altındaki `calls` alanı sıfır dönüyor; "ortalama 1,43M/çağrı" rakamı toplam olabilir.
