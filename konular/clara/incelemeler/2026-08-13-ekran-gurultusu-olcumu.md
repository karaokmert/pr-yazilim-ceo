# Ekran gürültüsü — ölçüm ve sessiz mod hook'u

**Tarih:** 2026-08-13
**Tetik:** Mert — *"sen dahil tüm agentlar aşırı gürültülü, adım adım düşüncelerini ekrana yazıyorlar"*

## Ne ölçüldü

`~/.claude/projects/-Users-karaok-p-pr-yazilim-ceo/` altındaki 145 transcript.
Yöntem: her metin bloğunun ardından ne geldiğine bakıldı — **araç çağrısı** geliyorsa
"ara metin" (iş bitmeden yazılmış), **kullanıcıya dönüyorsa** "asıl cevap".

**Kapsam:** son 40 oturum, agent adına göre ayrıştırıldı (`agentName` alanı).
Kapsam dışı: başka projelerin transcript'leri, 40'tan eski oturumlar.

## Sayılar

**Clara (13 oturum):** 1087 asıl cevap, 2638 ara metin.
Cevap başına **2,4 ara blok**. Toplam metnin **%34'ü** ara laf.
Asıl cevapların %15'i 1803 karakter eşiğini aşıyor.

**OY ekibi (23 oturum):** 226 asıl cevap, 1284 ara metin.
Cevap başına **5,7 ara blok**. Toplam metnin **%40'ı** ara laf.
Asıl cevapların **%56'sı** eşiği aşıyor.

Yani ekip Clara'dan hem daha çok ara laf yazıyor hem daha uzun cevap veriyor.

## Kaynak ayrımı — asıl bulgu

Plugin **2026-08-02 20:59**'da devreye girmiş; o tarihten sonraki **62 Clara oturumunun
hepsinde** system prompt'a `explanatory` emri gelmiş. Karşılaştırma grubu YOK —
plugin öncesi Clara oturumu bu klasörde bulunmuyor.

Ama ayrım başka yoldan yapıldı: 62 oturumdaki **6433 ara metin bloğunun 902'sinde**
`★ Insight` işareti var.

- **%14 (902 blok)** → plugin'in emri
- **%86 (5531 blok)** → agent alışkanlığı

⚠️ İlk teşhis *"plugin'in işiydi"* denildi ve **eksikti** — ölçüldüğünde gürültünün
altıda birini açıkladığı çıktı.

## Plugin ne yapıyordu

`explanatory-output-style@claude-plugins-official` — bir `SessionStart` hook'u
(`hooks-handlers/session-start.sh`), sistem promptuna şunu ekliyordu:

> *"Kod yazmadan önce ve sonra, her zaman `★ Insight ─────` biçiminde kısa eğitici
> açıklamalar ver... İçgörüleri sona bırakma, kod yazarken ver."*

Ve kritik cümle: ***"İçgörü verirken tipik uzunluk kısıtlarını aşabilirsin."***
Yani Clara kanonundaki "bir bulgu / üç paragraf / tek soru" kuralını **açıkça
iptal ediyordu.**

Plugin'in kendi README'si uyarıyordu: *"Bu plugin'in ek talimatlarının ve çıktısının
token maliyetini kabul etmiyorsanız kurmayın."*

**Mert 2026-08-13 20:36'da kaldırdı** — `enabledPlugins` 13'ten 12'ye indi, doğrulandı.

## Araç envanteri (alt agent araştırması + doğrulama)

Sürüm: **2.1.231** (ölçüldü).

**Var olan ve çıktı kısan ayarlar** (hiçbiri ayarlı değildi, hepsi varsayılanda):
`viewMode: "focus"` · `spinnerTipsEnabled` · `showTurnDuration` ·
`promptSuggestionEnabled` · `terminalProgressBarEnabled` · `showThinkingSummaries` ·
`prefersReducedMotion` · `axScreenReader` · `BASH_MAX_OUTPUT_LENGTH` (env)

⚠️ **Mert bunları KAPATMADI** — *"kalsınlar bunlar lazım"* (2026-08-13 20:52).
Bunlar arayüz süsü; şikayet edilen şey agent metniydi.

**Bulunamayanlar:**
- `concise`/`terse` diye hazır bir output style **YOK**. Dört stil var (Default,
  Proactive, Explanatory, Learning) ve son üçü çıktıyı **uzatıyor**.
- `CLAUDE_CODE_VERBOSE` diye bir env değişkeni **YOK** (alt agent'ın ara kaynağı
  uydurmuş, kendisi çürüttü).
- `/output-style` komutu **v2.1.91'de kaldırılmış** — bu sürümde çalışmaz, `/config`.

**Output style yazılabilir:** `~/.claude/output-styles/{ad}.md` (dizin yoktu).
⚠️ `keep-coding-instructions: true` konmazsa Claude Code'un tüm mühendislik
talimatları düşer — sessiz ama beceriksiz agent üretir.

## Neden hook seçildi, output style değil

Hook sistem promptuna **ekler** (geri alınabilir); output style sistem promptunu
**değiştirir** (riskli). Ve aynı mekanizmanın çalıştığı kanıtlı — plugin de
`SessionStart` hook'uydu ve 902 kutu üretti. Aynı kol ters yöne çevrildi.

**Çürütülen fikir:** Mert *"hook agent ekrana bir şey yollarken çalışsın"* dedi.
Dokuz hook olayı var (`PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`,
`SubagentStop`, `SessionStart`, `SessionEnd`, `PreCompact`, `Notification`) —
**"ekrana yazarken" diye bir olay yok.** En yakını `Stop` ama o metin yazıldıktan
SONRA ateşleniyor, ve ara metinler `Stop`'a hiç gelmiyor (tur ortasında akıyorlar).

## Kurulan hook

**Dosya:** `~/.claude/hooks/sessiz-mod.sh`
**Bağlantı:** global `~/.claude/settings.json` → `hooks.SessionStart` (mevcut git
hook'unun yanına eklendi, o bozulmadı)
**Yedek:** `/tmp/settings.json.yedek-2052`

Kural özeti:
- **İşe başlarken** planı bir kez söyle (tüm adımlar tek paragrafta)
- **Arada sessiz** — adım adım ilerleme duyurusu yok
- **Plan değişirse söyle** — sessizlik ilerleme raporu için, sapma için değil
- **İş bitince** ne bulduğunu söyle, nasıl bulduğunu değil
- **Uzunluk kısıtını AŞMA** (plugin'in tersi)
- **`★ Question` kutusu** — karar sorarken, turda bir kez, kendi kendine yeten içerik
- **İş anlatımı için kutu YOK** — cevabın tamamı zaten o olmalı
- **Sınır maddesi:** *"bu sunum kuralıdır, kapsam kuralı değil — ölçüm ve
  doğrulama aynen sürer"*

### Mert'in düzelttiği yer

İlk taslak *"ne yapacağının duyurusunu yazma"* diyordu. Mert kesti:
*"ne yapacağını duymak istiyorum tabii ki, o an ne yaptığını duymak istemiyorum.
İşe başlarken anlatsın, iş bitince anlatsın."*

Ayrım: **plan bir kez söylenir, adımlar söylenmez.** İlk taslak ikisini birden
kesiyordu — uzun bir işte kullanıcı kör kalırdı.

Ve `★ Insight` kutusu Mert'in ilk önerisindeydi; çürütüldü: kaldırılan plugin'le
**aynı mekanizma** (her iş anlatımında kutu aç) ve iyi bir yönetici raporunun
kutuya ihtiyacı yok — rapor cevabın kendisi.

## AÇIK — ölçülmedi

**Hook tuttu mu?** Birkaç oturum sonra aynı ölçüm tekrar koşulmalı: ara metin oranı
%31'den nereye indi? Düşmediyse metin yetersiz, sertleştirilir.
Ölçüm betiği: `/tmp/olc5.py` (kalıcı yere taşınmalı).

**OY ekibinde etkisi zayıf olabilir** — ekip agent'ları kendi plugin'lerinden ek
talimat alıyor, bu hook üstüne biniyor, yerine geçmiyor. Ayrı ölçülmeli.

**Bu oturum eski promptla koştu** — hook açılışta yükleniyor, temiz ölçüm sonraki
oturumda.
