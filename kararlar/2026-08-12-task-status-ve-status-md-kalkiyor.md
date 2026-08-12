# TASK-STATUS.md ve status.md kalkıyor — olay akışı ClickUp sub task'larında

**Tarih:** 2026-08-12 · **Karar:** Mert · **Getiren:** Clara (fabrika modu)
**Etkilenen kanon:** OY `proje-dosya-duzeni` (+ 16 dosyada `status.md` atfı)

## Karar

İki dosya da kalkıyor:

- **`_project/TASK-STATUS.md`** — prod geçiş kontrol listesi
- **`{modul}/{task}/status.md`** — olay akışı / ilerleme günlüğü

Mert'in gerekçesi: *"olay akışı sub task'ler sayesinde ClickUp'ta zaten."*

## Neden — ve Clara'nın itirazının neden çürüdüğü

**TASK-STATUS için gerekçe zaten kanonun içindeydi.** Tanımı bir **kuyruk**: iş
discovery'de girer, PROD'a çıkınca satır düşer. Kuyruk ClickUp'ın işi, ve statü akışı
(`development → live dev → prod`) ClickUp statüleriyle birebir örtüşüyor.

Kanon bu dosyanın şiştiğini **kendi kabul ediyor**: `DOC-TASK-STATUS-SIZE-GUARD` diye
bir boyut bekçisi kuralı var, 60 satır eşiği konmuş, PA'ya *"buda"* deniyor. Ölçülmüş
vaka kayıtlı: **238 satıra** çıkmış bir TASK-STATUS, ve *"sahibi olmayan dosyaya herkes
yazar → not defterine döner."*

`CLA-FIX-THE-CAUSE`: bir dosya için **boyut bekçisi yazmak zorunda kalınmışsa** o dosya
yanlış yerde duruyordur. Budama kuralı yamaydı; sebep kuyruğun dosyada tutulmasıydı.

**status.md için Clara itiraz etti ve itirazı çürüdü.** İtiraz şuydu: *"bu olay akışı
taşıyor, ClickUp'ta karşılığı yok."* Mert çürüttü: yeni kurulan düzende her katman kendi
sub task'ı, ve olay akışı orada zaten oluşuyor — statü geçişleri, kanıt (commit hash, QA
onay handoff'u), yorumlar.

**Clara'nın hatasının sınıfı:** kanonu okudu, sahada **ne değiştiğini** hesaba katmadı.
Kanon `status.md`'yi tanımlarken sub task düzeni yoktu; karşılığın "olmaması" o düzenin
yokluğundandı, dosyanın vazgeçilmezliğinden değil. **Bir kaydın geçerliliği, dayandığı
düzenin hâlâ ayakta olmasına bağlıdır** — kanon okumak bunu vermiyor.

## PAM'e giderken açık kalan tek soru — kaldırma kararına itiraz DEĞİL

Kanon `status.md`'nin yanında ayrı bir dosya daha tanımlamış: **`DEVIR-{hedef}.md`**.
Gerekçesi kanonun kendi cümlesi:

> *"Bir iş tek turda bitmediyse devralan agent'ın 'nerede kaldık, ne yarım' bilgisine
> ihtiyacı olur. Bu bilgi hiçbir kalıcı belgede yoktur — `status.md` olay akışını tutar,
> working tree'nin yarım hâlini tutmaz."*

Yani kanon bu ihtiyacı `status.md`'nin **dışında** çözmüş. Sub task yorumu bunu
taşıyabilir, ama **taşıyıp taşımadığı ölçülmedi.** PAM'e soru olarak gider; ölçmeden
*"sorun yok"* denmez.

## Kapsam — ölçüldü

`status.md` / `STATUS.md` OY kanonunda **16 dosyada** geçiyor (behavior, commit-review,
handoff, clickup, is-akisi ×4, memory-management ×2, proje-dosya-duzeni ×2, orkestrasyon,
ui-designer). Tek dosya silme işi değil — **cascade**. Yarım kalmış cascade fabrikada
daha önce bulgu olmuştu (`plugin-dagitim/SKILL.md` vakası, 2026-08-11).

## Kaynaklar

- Dosya düzeni kanonu: `v8/ozel-yazilim/.claude/skills/proje-dosya-duzeni/SKILL.md`
  (satır 21, 28, 34, 40, 44, 72-80, 86, 97, 100, 109)
- Yeni sub task düzeni: `pr-yazilim-ceo/gunluk/ev/2026-08-12-clickup-task-takip-testi.md`
- Kapsam daraltma kararı: `kararlar/2026-08-12-clickup-yazma-yetkisi-kapsam-daraltma.md`
