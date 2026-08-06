# Fabrika yapılandırma eksikleri — 4. işin girdisi

**Tarih:** 2026-08-06 · **Kaynak:** dört eksen ölçümü (aynı klasör)
**Ne değil:** bu bir hüküm listesi değil, kanıtlı eksik envanteri. Karar Mert'te.

## Önce sonuç — "yapılandır, yeniden kurma" kararı doğrulandı

Teknik kat sağlam: kırık atıf 0, hayalet index kaydı 0, kayıt dışı kural 0, hook 4/4
doğru parse, 122 kural düzgün sayılmış, memory dört klasörde tertemiz (sapma sıfır).
Rol ayrımı tutarlı, her skill'in sınır beyanı var, atıf disiplini biliniyor.

Yani onarılacak bir mimari yok. Eksikler **yapılandırma** sınıfında ve **iki kökten**
çıkıyor.

## KÖK 1 — Cascade yarım kalıyor (dokuz çelişkinin sekizi)

Bir kural bir yerde tam yazılıyor, ona bağlı yerler güncellenmiyor. Kanonun kendi
kuralları bunu yasaklıyor (`ISD-CASCADE-IN-ONE-TURN`, `PAD-CASCADE-SAME-TURN`) — yani
arıza kural kalitesinde değil, **uygulamada.**

**Kanıtı index'in kendinde:** `atif_verenler` alanı 123 kuralın **112'sinde boş.**
Gövdede anılan 38 tekil kimliğin **28'i orada atıfsız.** Bu alanın adı index'in kendi
beyanında *"cascade'in haritası"* ve `pr-agent-qa.md:40-41`'de bir **denetim ekseni.**

Doğrudan sonucu: **dördüncü ölçüt bugün karşılanmıyor.** *"6 ay sonra behavior'da bir
şey değiştirmek istiyorum, tüm takımlarda yapılmalı kararı alabiliyor muyuz?"* —
haritaya bakarak hayır, cascade elle grep gerektiriyor.

**Eksik 1.1 — `atif_verenler` doldurulmalı.** 28 kimlik için atıf listesi eksik. Ve
alan **iki tipte veri taşıyor** (bazı kayıtlarda dosya yolu, bazılarında kimlik:
`ISD-KEEP-STATUS` → `['ISD-APPEND-DONT-REWRITE']`) — tip kararı verilmeli. Bir kayıt
doğrulanamadı: `uretim/SKILL.md — kural yazımı bölümü` (dosyada "Kural biçimi" var).

**Eksik 1.2 — dört kuralın bağı hiç kurulmamış.** `ISD-STAY-IN-ROLE`, `PQA-NO-FILE-EDIT`,
`DAG-BUMP-BY-AUDITOR`, `ISD-CONSOLIDATE-AT-END` — dördü de en az bir body'de anılıyor
ya da anılması gerekiyor, index'te `atif_verenler` tamamen boş.

**Eksik 1.3 — beş yarım cascade düzeltilmeli:**
- `yapi-taslari:296-300` PAM'de Bash yok diyor; PAM body'si (`:199-200`) tersini.
  Body düzeltilmiş (commit `08a6410`), skill düzeltilmemiş. **PQA bu skill'i ölçüt
  sayıyor.**
- `is-duzeni:73-74` *"tek yazma yetkisi PAD"* mutlak yazılmış; fiilen dört elde yazma
  var ve bir delik (PQA `plugin.json` sürümü) hiç tanınmıyor.
- `ISD-STAY-IN-ROLE` (`is-duzeni:132`) dört rolü bağlıyor, PCA'nın bölümünde yaşıyor;
  index'te `bolum` alanı `"PCA — analist"`.
- `ISD-COMMIT-THEN-PUSH` PAD'in commit ettiğini söylüyor; **PAD body'sinde "commit"
  kelimesi hiç yok.**
- `BHV-NO-SELF-CONFIG` dördünü bağlıyor, yasak yalnız PAM ve PAD body'sinde;
  PQA/PCA'da yok — ve ölçüldü ki ikisi de fiilen yazabiliyor
  (`yapi-taslari:291-295`).

**Eksik 1.4 — tekrarlanan gerekçe blokları tek kaynağa indirilmeli.**
Hook'un "üç tasarım kararı" bloğu `yapi-taslari:193-203` ve `dagitim:78-93`'te
neredeyse birebir. `URT-NO-DUPLICATE-ID`'nin gerekçesi bunu yasaklıyor ve **tam olarak
öngördüğü şey gerçekleşti** (Eksik 1.3'ün ilk maddesi). Ayrıca: %91 preload ölçümü iki
yerde farklı ayrıntıda, onay kapısı gerekçesi `is-duzeni` içinde iki kez (60 satır
arayla), PAM body'sinde iki ISD kuralı tam tanım biçiminde yeniden yazılmış
(`uretim:186` bunu açıkça yasaklıyor, diğer üç body yapmıyor).

## KÖK 2 — Üretim hattının çıkış ucu hiç çalışmadı

`team/team-1-oy/` **boş ve git'te hiç yok** — sıfır commit. `docs/filo/durum.md:10`:
*"Kurulmuş takımlar — Henüz yok."*

**Eksik 2.1 — `dagitim`'in 26 kuralı sınanmadı.** Kanonun **%21'i.**
`uretim/SKILL.md:349` kendi ölçütünü koyuyor: *"aynı durumu iki koşulda koştur — kural
varken ve yokken. Fark yoksa kural çalışmıyordur."* Bu ölçüt `dagitim` için hiç
uygulanamadı. Ve gerekçeleri **önceki kuşağın** sahasından geliyor, bu kanonun kendi
sahasından değil.

**Eksik 2.2 — sıfırdan üretme yöntemi yazılı değil (EN ZAYIF HALKA).**
Bir takımın **kendi tasarımı** hiçbir dosyada yok: hangi roller, kaç personel, hangi
işler tek elde birleşir, devir hattı ne. Elde olan iki uç var, aradaki dönüşüm boş:
- `pr-agent-manager.md:81-96` — 15 satır **tutum** (acele etme, günler sürebilir)
- `pr-agent-context-analyst.md:33-42` — PCA'nın **ölçüm** tarifi (hangi roller var)
- Arada: PCA *"şu beş rol var"* der → *"bizim takım şu üç agent olsun"* kararına geçiş.
  Yöntem yok. Ve `PCA-NO-PROPOSE-RULE` PCA'yı bu geçişten men ediyor.

PAM'e verilen tek bitiş testi: *"PAD bu gereksinimle katman kararı verebilir mi?"* —
o ise *"bu kural skill'e mi hook'a mı"* sorusu. **Rol mimarisinin doğruluğunu ölçen
hiçbir eşik yok.**

Ve fabrika bunu **kendi kuruluşunda tespit etti:**
`docs/fabrika/ekip-kurulumu/gereksinim.md:13-16` — *"rol mimarisi tasarımı hiçbir
belgede kimseye verilmemişti... ikinci kez yapılamazdı."* Dörtlü kuruldu, boşluk açık
bırakıldı.

**Yapısal kanıt:** `is-duzeni:149-153` kuruluş hattını **5 satırda** tarif ediyor ve
*"yeni takım kurulurken **ya da** mevcut kanona ekleme yapılırken"* diye iki farklı işi
aynı hatta koyuyor. Üçüncü hat (mevcut olanı değiştirme) **60 satır.** Kanonun ağırlığı
değiştirme tarafında.

**Eksik 2.3 — alan bağımsızlığı ölçülemez durumda, ama beklenenden iyi.**
123 kuralın hüküm cümlelerinin **hiçbirinde** yazılım domain terimi yok (`frontend` 0,
`API` 0, `.NET` 0, `React` 0; `backend` 2 ve `developer` 5 yalnız gerekçe içinde biçim
örneği). Kanon domain'den temiz.

Araç varsayımı yoğun (`plugin` 74, `script` 85, `push` 45) ama bu ölçüt açısından engel
değil — marketing takımı da plugin olacak.

Gerçekten anlamsız kalan üç kalem: `ISD-APPEND-DONT-REWRITE`'ın ayrım ölçütü *"commit"*;
`CLAUDE.md:199` *"gerçek proje koduna yazılmaz"* (kod olmayan alanda tanımsız);
`behavior:209`'daki grep talimatı.

**Asıl boşluk 2.2 ile aynı** — marketing takımının rol mimarisini çıkarma yöntemi yok.

## Ayrı kalem — ölçüm gerektiren üç şey

**Ö.1 — `Task` mı `Agent` mı? (EN RİSKLİ, karar öncesi ölçülmeli)**
`pr-agent-developer.md:4` frontmatter'ında `tools: ... Bash, Task, Skill`. Ama
`arac-envanteri.md:95` envanterinde araç adı **`Agent`** ve `Task` diye bir araç yok
(`Task*` yalnız görev listesi dörtlüsü). Kanon boyunca 20 yerde `Task` geçiyor.

`arac-envanteri.md:323-324`'ün kendi hükmü: *"Listedeki hiçbir girdi bir araca
çözümlenmezse agent genellikle hiç başlamıyor"* ve kısmi yanlış yazım **sessiz.**
Doğruysa PAD sub-agent açamıyor ve `PAD-TEST-BEFORE-HANDOFF` uygulanamaz durumda —
hata mesajı çıkmadan.

*Clara notu:* bu odada `Agent` aracı çalışıyor, `Task` adı yok — takma ad olmama
olasılığı yüksek ama ölçülmesi gerek.

**Ö.2 — Hook alt-agent'ta çalışıyor mu? (4. işin ön koşulu)**
Hook elle koşturuldu, mantığı **doğru**: 4 agent için skills listesini birebir doğru
basıyor, namespace filtresi çalışıyor, boş değişkende sessiz çıkıyor. Ama
`CLAUDE_CODE_AGENT` değişkenini **biz verdik.** Claude Code'un onu gerçek bir alt-agent
turunda geçirip geçirmediği ölçülmedi.

Mert'in kararı (2026-08-06): **PAM'i Mert açacak**, açılışta ne gördüğü sorulacak.
Cevap hayırsa 4. işin tamamı boşa gider — kanon verilir, eline ulaşmaz, "giderildi"
görünür.

**Ö.3 — Hook'un `CAKISAN` dalı hiç koşmadı.** `~/.claude/skills/` bugün boş
(2026-08-04 temizliği), o yüzden 4 koşumun hiçbiri o kod yolundan geçmedi. Kod doğru
görünüyor, ölçülmemiş.

## Ayrı kalem — filo bakımı: yapı var, sıfır kez koştu

**Önceki tespit düzeltildi.** Ölçüt dosyası (2026-08-03) bunu *"kısmen — refleks var,
mekanizma yok"* diye kaydetmişti. **Geçersiz:** madde 2026-08-02'de kapatılmış
(`docs/fabrika/ekip-dogrulama/oturum-06-filo-bakimi.md`). Sorumlu isimli (PAM),
kural var (`PAM-REPORT-FLEET-AGE`), yayılma sırası dört rolde tanımlı
(`is-duzeni:267-327`), iki kural koruyor (`ISD-FIND-WHAT-IT-REPLACES`,
`ISD-ONE-TEAM-PER-TURN`).

Ama dört kalem açık — hepsi `docs/filo/durum.md`'de duruyor:

**F.1 — Hiç koşmadı.** *"Son filo taraması — Yapılmadı."* `PAM-REPORT-FLEET-AGE` bir
tarih karşılaştırması yapıyor, karşılaştıracak tarih yok. Kuralın davranış üretip
üretmediği ölçülmedi.

**F.2 — Kimlik çakışması: görülmüş, kuralı yazılmamış.** `durum.md:257-260`: iki takım
aynı kimlik kalıbını kullanırsa (`BHV-NO-RUSH` iki farklı hükmü gösterirse) atıflar
**sessizce yanlış kurala tutar.** *"İkinci takımda ölçmek ucuz, sekizincide cascade
demek."* — Bu tam Mert'in 8-takım senaryosu.

**F.3 — Plugin skill'i en düşük öncelikte, sahada sessizce ezilir.**
`durum.md:271-275` — ölçülmüş arıza (fabrikanın kendi `behavior`'ı v7 kanonunu getirdi,
hata mesajı çıkmadı). *"Takım kurulurken kontrol edilmeli"* bir **not**, `dagitim`'in
26 kuralında bu kontrol yok.

**F.4 — `docs/` commit sahipliği tanımsız.** PQA bunu **kanon boşluğu** ilan etti, iki
turda iki kez bildirdi, bedeli ölçüldü (`gereksinim.md` hiç commit edilmedi). Hüküm
yazılmadı.

**Mimari bedel (karar değil, bilgi):** ortak çekirdek yok (Mert'in kararı) — yani 8
takımda bir behavior değişikliği **8 ayrı iş** ve `ISD-ONE-TEAM-PER-TURN` bunu zorunlu
kılıyor. Karar alınabilir, uygulaması 8 tur.

## Ayrı kalem — insan okunabilir çıktı: dördüncü tekrar, iş açılmadı

Biçim kuralı **var ve iyi yazılmış** (7 kural: `BHV-SHAPE-REPORT`, `BHV-NO-EVIDENCE`,
`BHV-NO-REOPEN`, `BHV-STAND-ALONE`, `BHV-NO-ORNAMENT`, `BHV-WRITE-AS-COLLEAGUE`,
`URT-NO-TABLE`).

**R.1 — Soru sorma anı kapsam dışı.** Mert'in şikâyetlerinden ikisi soru **sayısı ve
yerleşimi** hakkındaydı (*"5 soru sordun, hepsi koca bir blok"*, *"12 soru var ama
hiçbirini anlamadım"*). Kanonda soru sayısını sınırlayan, tek tek soran ya da blok
biçimini düzenleyen **tek kural yok.** Ve `BHV-SHAPE-REPORT` kendi kapsam cümlesiyle bu
anı **açıkça dışarıda bırakıyor** (`:373-376`).

**R.2 — Uzunluk sınırı sayı olarak yok.** `CLAUDE.md:132` bir tutum bildiriyor ama
kimliksiz, eşiksiz, ve *"agent üretirken"* kapsamına yazılmış — **üretilen dosya için,
rapor için değil.**

**R.3 — Dördüncü tekrarda ve iş hâlâ açılmadı.** `durum.md:120-133`: *"Dört oturumdur
aynı şikâyet geliyor... Önerilen yön: raporu kısaltmak değil biçimini değiştirmek —
bulgu üstte kısa, kanıt altta. **Kapsamı çizilmedi, iş açılmadı.**"*

**R.4 — Tanınmış gerilim.** `ISD-PRINT-AUDIT-RAW` denetim raporunun özetlenmesini
**yasaklıyor** ve gerekçesi ölçülmüş (*"üç bulgu çıktı, üçü de PAM'in hatasıydı"*).
Yani en uzun metin türü kısaltılamıyor, bilinçli. Çözüm önerisi var, kural yok.

## Boyut ve yerleşim — küçük kalemler

**B.1 — İki skill kendi eşiğini aşıyor.** `yapi-taslari:472` *"500 satırın altında"*
diyor; `is-duzeni` 612 (%22 aşım), `yapi-taslari` 507. Etkisi somut: compaction'da
skill başına 5.000 token sınırı var ve kırpma **sonu** atıyor. `is-duzeni`'nin son
bölümü (`ISD-CLOSE-WITH-IDENTITIES`, 40 satırlık gerekçe) düşme riski en yüksek
konumda.

**B.2 — Gövde/reference dengesi.** 2.757 satırın **%86'sı** gövdede, yani her açılışta
yüklenmesi gereken yerde. Tek reference dosyası var (5 skill'e karşı 1).

**B.3 — Bir konu kayması.** `dagitim:111-117` — "Kim ne yapar" bölümü PAD/PQA rol
dağıtımını tanımlıyor, oysa `is-duzeni:22-23` *"Rol tanımı... Tek kaynak burasıdır"*
diyor. Üstelik `is-duzeni`'ndeki bir hükme istisna açıyor ama atıf vermemiş — aynı dosya
satır 82'de düzgün atıf veriyor, yani disiplin biliniyor.

**B.4 — PQA denetleyeceği kanonu elinde bulundurmuyor.** `pr-agent-qa.md:30` denetim
eksenine `yapi-taslari`'yı koyuyor; PQA'nın `skills:` listesinde o skill **yok** ve hook
da basmıyor. Aynı hasar `dagitim` için de var (`DAG-BUMP-BY-AUDITOR` PQA'ya iş
veriyor, PQA o skill'i okumuyor).

**B.5 — PAM'de `tools:` yok, bilinçli ama 3. işi etkiliyor.** Gerekçesi yazılı
(`pr-agent-manager.md:134-137`, kullanıcı kararı 2026-08-04). 3. iş PAM'den `Task`
yetkisini almayı öngörüyor — **alınacak liste yok, kısıt sıfırdan yazılacak.**
Ve beyan disiplini tek biçimli değil: aynı gerekçeyle PAD'in `Task`'ı da yazılmayabilirdi,
yazılmış.

**B.6 — Hook'ta latent kırılganlık.** awk parser YAML **akış biçimini**
(`skills: [behavior, dagitim]`) sessizce boş döndürüyor. Bugün 4 dosyanın hiçbiri o
biçimde değil — fiilî arıza değil, sessiz kırılma riski.

**B.7 — Memory dağılımı dengesiz.** PAM 15.224 karakter, PCA 3.630 (4,2 kat). PCA'nın
iki rolünden biri hakkında hiç kayıt yok — 2026-08-03'teki *"PCA hiç çağrılmadı"*
bulgusuyla tutarlı. Küçük tutarsızlık: dosya adı ayırıcısı karışık (PAD/PAM alt çizgi,
PQA/PCA tire); kanonda kural yok, ihlal değil.

**B.8 — *"ihlali sessizdir"* kalıbı 52 kez.** Bilinçli retorik omurga, tekrar değil.
Ama `BHV-RATION-ABSOLUTES`'un mantığına yaklaşıyor: her ihlal sessizse hiçbiri ayırt
edici olmuyor.

## Sırayla ne yapılmalı — öneri, karar Mert'te

1. **Ö.2 (hook alt-agent)** — 4. işin ön koşulu, Mert açacak
2. **Ö.1 (`Task`/`Agent`)** — sessiz arıza riski, kanon değişikliği öncesi ölçülmeli
3. **Eksik 1.1 + 1.2 + 1.3** — cascade onarımı; dördüncü ölçüt buna bağlı
4. **Eksik 2.2** — sıfırdan üretme yöntemi; en zayıf halka, en büyük iş
5. **R.1–R.3** — rapor biçimi; dört tekrar, en görünür şikâyet
6. **F.2 + F.3** — kimlik çakışması ve skill ezilmesi; *"ikinci takımda ucuz"*
7. **B.4, B.5, F.4** — küçük ama sessiz kalemler

---

# ÖLÇÜM SONUCU — hook (2026-08-06, aynı gün eklendi)

Yukarıdaki Ö.2 ölçüldü. **Kaynak:** PAM + PCA, `agent-project` oturumu
`2be4c5d8`; ham kayıt `agent-project/docs/filo/hook-olcumu-2026-08-06.md`.

## Ana oturum — hook ÇALIŞIYOR

PAM (ana oturum, `claude --agent pr-agent-manager`):
- Hook mesajı **geldi**, metni tam
- `CLAUDE_CODE_AGENT=pr-agent-manager` (kendi adı, doğru)
- `CLAUDE_PROJECT_DIR` **tanımsız** — ama hook yine de çalıştı
- Üç skill yüklendi: `behavior`, `is-duzeni`, `uretim` — frontmatter'la birebir

**Clara'nın hatası düzeltildi:** `CLAUDE_PROJECT_DIR` tanımsızlığından *"hook devre
dışı"* çıkarımı yapılmıştı — YANLIŞ. İki ayrı ortam var: hook'u Claude Code kendi
çağırıyor, agent'ın `Bash` aracına verilen ortam `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1`
ile temizlenmiş. Ölçüm ile çalışan hook çelişmiyor.

## Alt-agent — İKİ ARIZA BİRDEN

PCA (`Agent` ile açıldı, açılan `pr-agent-context-analyst`):

```
AGENT=pr-agent-manager     ← ÇAĞIRANIN adı, açılanın değil
PROJDIR=                   ← hiç tanımsız
Hook mesajı  : GELMEDİ
Skill listesi: GELMEDİ
```

Okuduğu: `behavior`, `is-duzeni` — **hook'la değil, başka bir yolla**, `<command-name>`
blokları hâlinde. Okumadığı: `uretim`, `yapi-taslari`, `dagitim`.

Gelen dosyalar **doğruydu** (fabrika kanonu, doğru base directory) — geliş yolu hook
değil ve **ne olduğu ölçülmedi.**

## PAM'in tespiti — sıralama kuralı (Clara'nın göremediği)

**İki arıza birbirini maskeliyor.** Hook alt-agent'ta tetiklenmediği için yanlış env
değerini kullanma fırsatı hiç bulmadı.

Sonucu: **hook'u env sorunu çözülmeden çalışır hâle getirmek sistemi bugünkünden kötü
yapar.** Bugün alt-agent kanonsuz kalıyor — eksik ama görünür arıza. O durumda
alt-agent **yanlış personelin kanonunu yüklü sanarak** çalışır ve bu sessizdir.
**Sıra tersine kurulamaz.**

## Asıl bulgu — kanonun ulaşması garantisiz

PCA üç skill'den ikisini aldı, birini almadı. Yani kanonun alt-agent'a ulaşması
**kimsenin garanti etmediği bir mekanizmaya bağlı** — tur tur değişebilir, kimse fark
etmez. PCA için zarar yoktu (ölçüm işiydi, üretim kanonu gerekmedi). **PAD'a üretim
işi verilirse üretim kanonsuz yapılır** — ki hook'un var olma sebebi tam bu.

## Ö.1 kısmen cevaplandı — `Task` değil `Agent`

PAM alt-agent'ı **`Agent` aracıyla** açtı. Kanonda 20 yerde `Task` yazıyor;
`arac-envanteri.md:95` doğru olanı (`Agent`) söylüyor. Yani **kanon metni gerçeği
yanlış tarif ediyor** ama fiilî arıza değil — PAM doğru aracı bulup kullandı.

Ölçülmemiş kalan: `tools:` listesindeki `Task` girdisi bir araca çözümlenmiyorsa ne
oluyor (`arac-envanteri.md:323-324` *"agent genellikle hiç başlamıyor"* diyor ama PAD
çalışıyor — yani kısmi yanlış yazım tolere ediliyor olabilir).

## 4. işin kapsamı büyüdü

Ana oturum turunda *"hayır çıkmadı"* denilebilirdi. Alt-agent turu bunu değiştirdi:
**zincirin yürüdüğü yerde hook çalışmıyor ve env değeri yanlış.** İş boşa gitmiyor
ama artık tek bir hook düzeltmesi değil — **"alt-agent'a kanon nasıl ulaşacak"**
sorusunun kendisi.

## Hâlâ ölçülmedi

- Hook alt-agent'ta **neden** tetiklenmiyor (`SessionStart` bir oturum olayı; `Agent`
  ile açılanın ayrı oturum sayılıp sayılmadığı)
- `behavior` + `is-duzeni` **hangi mekanizmayla** geldi
- `uretim` **neden gelmedi** — diğer ikisi geldiyse ayrımın bir sebebi var
- Aynı ölçümün **PAD'da** tekrarı (PCA sonucunun PAD'da da aynı çıkacağı varsayım)
