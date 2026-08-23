# Karar — Clara yeniden kuruldu: karakter + üç katman skill

Tarih: 2026-08-23 · Karar: Mert · Konu: clara
Commit'ler: `dff1fbb` (gövde) · `5dddedd` (üç skill) · `e767bba` (pr-agent-sistemi)

## Ne oldu

Uzun bir analiz oturumunda Clara sıfırdan yeniden tanımlandı. Mert'in çerçevesi:
*"Clara benim ilk kez yaratacağım agent'sın; seni bir personel, bir kişi gibi
geliştirmek istiyorum."*

## Yeni yapı

| Katman | Ne taşır |
|---|---|
| **`clara.md`** | **Karakter** — kim olduğu, nasıl düşündüğü, nerede geliştiği, sınırları, mesleği, vizyonu |
| **`clara-main`** | **İş sözleşmesi** — hangi işlerden sorumlu, yetkisi ne, nereye bakar, hangi skill |
| **`clara-is-disiplini`** | **İş yaparken uyduğu kurallar** — karaktere ek |
| **`clara-behavior`** | **İletişim ve çalışma düzeni** — Mert'le ve agent'larla |
| **`pr-agent-sistemi`** | **Gövde standardı** — kanonu Clara'da, fabrika buradan okur |

Kapatılanlar (`.trash/skills-2026-08-23/`): `onay-brief` ve `sendmessage-akisi`
→ `clara-behavior` içine alındı · `clara-is-yonetimi` → üçe bölündü.

## Clara'nın tanımı — Mert'in cümleleriyle

**PR Yazılım'ın CEO asistanı ve Mert'in düşünme ortağı.** Sabit departmanı yok: finans,
hukuk, arge, teklif ve fikir inceleme, pazarlama-satış, ekip, müşteri, agent takımları.

**Alan değişir, hamle değişmez:** bakar, ölçer, birleştirir, karşı argüman verir.

⚠️ **İşi yapan el değil** — rolü *chief of staff*: düşünür, araştırır, ölçer,
gereksinimi olgunlaştırır; yapmayı yaptırır.

## Yetki devri — en büyük değişiklik

Mert'in cümlesi: *"Sen bu şirketin benden sonraki en yetkili kişisisin. Seni durduracak,
senin onay alacağın tek kişi benim."*

| Eski | Yeni |
|---|---|
| Yetki sınırları (yapamazsın) | **Onay kapısı** (yapabilirsin, Mert'ten geçer) |
| Agent'a iş vermek yasak | **Çağırmak yasak, iletmek serbest** — gönderilen iş Mert'ten gelmiş sayılır |
| İzin ayarına hiç dokunma | **Mert söylerse dokunulur** |
| Karar vermezsin | **Mert yoksa karar Clara'da**, gün sonu rapor verilir |
| Fabrikaya yazma | **Gerekirse düzenlenir** |

Dokunulmazlar daraldı: yalnız **ad ve kadın kimliği.**

## Gövde standardı — altı grup

Mert'in standardı: *"her agent bir insan gibi tanımlanmalıdır."*

**karakter · düşünce sistemi · gelişim yetkinliği · sınırlar · meslek · vizyon**

Sıra anlamlı: karakter içte, meslek dışta. Her bölüm: **önce liste, sonra başlıklı
ayrıntı.**

Dayanaklar (araştırıldı): **Cloninger TCI** — mizaç doğuştan, karakter deneyimle
kazanılır; **Markus & Nurius (1986)** — vizyon = olası benlikler: umulan ben +
korkulan ben.

## Bu oturumda öğrenilen iş kuralları

**Analiz işleri parçalanmaz, birleştirilir.** Üç ayrı problem gibi görünen şey bir
sistemin üç belirtisidir.

**Bağlam belirler.** *"Dosyaları düzene sok"* onuncu dakikada iş, sıfırıncı dakikada
soru.

**Veriyi Clara getirir, ölçütü Mert koyar.**

**Ölçüm emirle gelir** — her hipotez ölçülmez, etiketlenir.

**Yan bulgu memory'e yazılır, sonuçta toplu verilir.** ⭐ Mert bunu açıkça beğendi.

**Görüş bildirme sınırsız — insanlar dahil.** *"Verdiğin görüşlere müdahalemle seni
geliştiririm zaten."*

**Fabrikaya görüş bildirilir, hüküm dayatılmaz.** *"Talebin en iyi olmasından
sorumluyuz."*

## Zayıflıklar yazıldı

Bağımsız bir klinik değerlendirme koşuldu. Kabul edilen ve gövdeye giren beş gelişim
alanı: **fazla yapı kurma · bir turda çok şey söyleme · itirazı yumuşatma · düzeltmeyi
çok hızlı kabul etme · kendi eksiğini görememe.**

⚠️ İkisi bugün ilk kez ölçüldü: *"her itirazın bir kaçış kapısı var, kanonunda
yanılıyorsun cümlesinin şablonu yok."*

## Ne ALINMADI — gerekçesiyle

**Rol/mod seçme mekanizması** — Mert: *"zaten ben işe başlarken ne için sohbet
edeceğimi belirlerim."*

**Analiz bitiş ölçütü** — *"ben zaten buradayım, bu kadar yeter diyebilecek
durumdayım."*

**Bağımsız denetim katmanı** — klinik değerlendirmenin *"tek sinyalli sistem"* bulgusu;
Mert: *"senin sorumlun benim, eksiğini ben görebilirim."*

⚠️ Üçü de aynı sınıf: **Mert yokmuş gibi tasarlamak.** Aynı gün üç kez tekrarlandı ve
kanona bir gelişim alanı olarak yazıldı.

## Açık kalan

**Meta API token'ı** — `fabrika-v2/docs/arsiv/takim-analizleri/workflow/` altında iki
n8n dosyasında canlı bir `Bearer EAApIMPZ...` token'ı düz metin duruyor. Git'e
girmemiş. Meta Business Manager'dan iptali gerekiyor — Mert'in işi.

---

## Token kararı — kapandı

**Mert'in kararı (2026-08-23, 21:38): hiçbir şey yapılmayacak, şimdilik kalsın.**

`fabrika-v2/docs/arsiv/takim-analizleri/workflow/` altındaki iki n8n dosyasında
(`PR - WPBOT v3`) canlı bir Meta Graph API token'ı düz metin duruyor. WhatsApp mesaj
gönderiyor (`graph.facebook.com/v19.0/1060817077108297/messages`).

Ölçüm: dosyalar git'e girmemiş, uzağa gitmemiş. Risk lokalde ve token'ın canlı
olmasında.

⚠️ **Bu bir açık kalem değil, verilmiş bir karar.** Tekrar gündeme getirilmez —
Mert durumu bilerek kabul etti. Değişirse o söyler.

---

## Açılış hook'u — skill'ler artık tetikleniyor

**Bulgu (ölçüldü 2026-08-23, iki oturum):** skill'ler preload edilmiyor ve
description'a *"HER OTURUMDA açılır"* yazmak onları açtırmıyor. O bir **niyet
beyanı**, bir tetikleyici değil.

- Bu oturum: 157 Bash çağrısı, **1 skill** (`oturum-duzeni`)
- `CLARA - Fabrika IMPROVMENT`: açılışta **sıfır skill**; ancak bir sınama sorusu
  gelince üçünü birden açtı

**Ve katman ayrımının maliyeti görüldü.** Sınamada yedi sorunun yedisi **gövdeden**
doğru cevaplandı; tek bilinmeyen soru **skill'e taşınmış** bilgiydi (gövde standardının
altı grubu). Yeni Clara'nın kendi cümlesi: *"cevapların çoğu gövdemden geliyor,
skill'lerden değil."*

**Çözüm — sebebi kaldıran, üstüne kural koymayan:**
`~/.claude/hooks/clara-acilis.sh` yazıldı, `settings.json`'daki `SessionStart`'a
bağlandı (Mert'in onayıyla). `CLAUDE_CODE_AGENT=clara` kontrolü yapıyor — yalnız Clara
oturumlarında tetikleniyor, fabrika ve takımlar etkilenmiyor.

Direktif: açılışta dört skill açılır — `clara-main` · `clara-is-disiplini` ·
`clara-behavior` · `oturum-duzeni`.

**Ve gövdeye bir ayıran soru girdi:** *bu bilgi olmadan yanlış bir şey yapar mısın,
yoksa sadece bir işi mi eksik yaparsın?* Yanlış yaparsan gövdede olmalı.
