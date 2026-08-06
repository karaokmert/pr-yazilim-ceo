# Eksen 4 — Yapısal düzen

**Tarih:** 2026-08-06 · **Repo:** `/Users/karaok/p/agent-project`
**Yöntem:** isimsiz yardımcıya ölçüm verildi; sayımlar `wc`/`grep` ile, kanıt dosya:satır.

## Boyut — iki dosya kendi eşiğini aşıyor

Skill'ler (satır/karakter):
- `is-duzeni` 612 / 34.762
- `yapi-taslari` 507 / 28.979
- `behavior` 469 / 26.628
- `dagitim` 416 / 24.052
- `uretim` 356 / 18.550
- `references/arac-envanteri.md` 397 / 19.207

Toplam **2.757 satır / 152.178 karakter.** Agent body'leri: PAM 209, PAD 179, PQA 136,
PCA 118.

`yapi-taslari/SKILL.md:472` kendi kanonunda *"SKILL.md gövdesi 500 satırın altında"*
diyor. `is-duzeni` 612 (%22 aşım), `yapi-taslari` 507 — **kendi yazdığı eşiği kendisi
aşıyor.**

Tavsiye eşiği ama etkisi somut: compaction'da skill başına 5.000 token sınırı var ve
kırpma dosyanın **sonunu** atıyor. `is-duzeni`'nin son bölümü
(`ISD-CLOSE-WITH-IDENTITIES`, satır 568-608, 40 satırlık gerekçeyle en uzun kural) uzun
oturumda düşme riski en yüksek konumda.

**Yapısal gözlem:** 2.757 satırın 2.360'ı (%86) reference'ta değil, **gövdede** — yani
her açılışta yüklenmesi gereken yerde. Tek reference dosyası var (5 skill'e karşı 1).

Description'lar hedefte: 243-332 karakter, `uretim`'in *"hedef 300 civarı"* kuralına
beşi de uyuyor.

## Konu kayması — bir gerçek, ikisi sınırda, gerisi temiz

**Gerçek kayma:** `dagitim/SKILL.md:111-117` — "Kim ne yapar" bölümü PAD ve PQA'nın rol
dağıtımını tanımlıyor. Bu `is-duzeni`'nin konusu; o skill satır 22-23'te *"Rol tanımı
burada tam yaşar... Tek kaynak burasıdır"* diyor. Üstelik `is-duzeni`'ndeki bir hükme
istisna açıyor ama o hüküm burada tanımlı değil ve **atıf da verilmemiş.** Karşılaştırma:
aynı dosya satır 82'de `YT-AGENT-CANT-SEE-SELF` için düzgün atıf veriyor — disiplin
biliniyor, burada uygulanmamış.

Sınırda ikisi: `is-duzeni:583-604`'te index/sayaç mekaniği (20 satır), `behavior:95-106`'da
`rules-index.json` tarifi. İkisi de savunulabilir.

**Temiz çıkanlar önemli:** `uretim`'de dağıtım kuralı yok (atıf veriyor), `behavior`'da
iş akışı detayı yok (üç kardeşe yönlendiriyor), `yapi-taslari`'nda dağıtım kararı yok.
Her skill'in girişinde *"cevaplamadığı şeyler"* bölümü, kapanışında kardeş adresleri var.
**Sınır beyanı sistematik yazılmış.**

## Tekrar — kimlik düzeyinde temiz, gerekçe düzeyinde bir blok kopyalanmış

Hiçbir hüküm iki kimlikle yazılmamış (`URT-NO-DUPLICATE-ID` tutuyor). Ama:

**Tekrar 1 — hook'un "üç tasarım kararı" bloğu iki yerde, neredeyse birebir.**
`yapi-taslari/SKILL.md:193-203` ↔ `dagitim/SKILL.md:78-93`. Cümle düzeyinde eşleşme:
*"Gömülse iki kaynak olur: frontmatter değişir, hook eskir, kimse fark etmez."*
(yapi-taslari:198 ↔ dagitim:80-82). Aynı şey `SessionStart` seçimi ve matcher filtresi
için de.

Bu `URT-NO-DUPLICATE-ID`'nin lafzına takılmıyor ama **gerekçesine takılıyor:** *"İkisi
bir süre aynı şeyi söyler, sonra biri güncellenir ve öteki eski hâliyle kalır."* — Ve
Eksen 2'nin 4. bulgusu bunun tam olarak gerçekleştiğini gösteriyor.

**Tekrar 2 — %91 preload ölçümü iki yerde, farklı ayrıntı düzeyinde.**
`dagitim:66-72` sayılarıyla, `yapi-taslari:184-186` sayısız. Hangisi kanonik, belirsiz.

**Tekrar 3 — onay kapısı gerekçesi aynı dosyada iki kez.** `is-duzeni:108-111` ↔
`:167-169`, 60 satır arayla neredeyse aynı iki cümle.

**Tekrar 4 — PAM body'sinde iki ISD kuralı yeniden tanımlanmış.**
`pr-agent-manager.md:183` ve `:196` — `ISD-PRINT-AUDIT-RAW` ile `ISD-COMMIT-THEN-PUSH`
tam kural biçiminde, gerekçe paragraflarıyla. `uretim/SKILL.md:186` bunu açıkça
yasaklıyor: *"Body gövde taşımaz... Body'de tam tanım yazarsan iki kaynak üretmiş
olursun."* Hafifletici: `:194` *"Tam tanım is-duzeni'nde"* diyor. Ama diğer üç body bu
hatayı yapmıyor — yalnız PAM'de.

**Tekrar 5 (meşru, kayda geçiyor):** *"ihlali sessizdir"* kalıbı **52 kez.** Bilinçli bir
retorik omurga, tekrar değil. Ama yoğunluk `BHV-RATION-ABSOLUTES`'un mantığına
yaklaşıyor: her ihlal sessizse hiçbiri ayırt edici olmuyor.

## Kural sayımı — 122 gerçek kimlik, index doğru

Skill başına: `behavior` 31 (BHV), `is-duzeni` 28 (ISD), `dagitim` 26 (DAG), `uretim` 13
(12 URT + 1 şablon), `yapi-taslari` 9 (YT), `arac-envanteri.md` 0.
Body başına: PAD 6, PAM 5 (3 PAM + 2 ISD yeniden-tanımı), PQA 4, PCA 4.

**Elenenler:** `URT-SOMETHING` (`uretim:32`) — kod bloğu içi şablon örneği, gerçek kural
değil. PAM'deki 2 ISD yeniden-tanımı yeni kural sayılmadı.

**TOPLAM: 122 tekil kimlik.** Index 123 sayıyor.

**Index doğrulaması temiz ve iki tuzağı da geçmiş:** hayalet kayıt 0, kayıt dışı kural 0
(tek aday `URT-SOMETHING`, index onu doğru olarak saymamış), prefix sayaçları birebir
tutuyor, PAM'deki ISD yeniden-tanımlarını PAM'e yazmamış. `son_guncelleme: 2026-08-04`.

## Memory — dört klasör temiz, dağılım dengesiz

21 dosya (4 MEMORY.md + 17 içerik), 40.187 karakter.
PAM 8 dosya/15.224 kr · PQA 5/13.283 · PAD 5/8.050 · PCA 3/3.630.

**İndeks-disk uyumu dört klasörde de tam, sapma sıfır.** Dört indeks de saf index
biçiminde (en büyüğü 9 satır) — `yapi-taslari:132` kuralına uyulmuş.

**`memory: project` karışması yok** — Claude Code her agent'a kendi adıyla klasör açmış,
fiziksel izolasyon var. Sahiplik ayrıca MEMORY.md başlıklarından ayırt edilebiliyor
(yalnız PCA'da jenerik `# MEMORY`).

**Dengesizlik:** PAM'in memory'si PCA'nın 4,2 katı. PCA'nın iki rolünden (saha + etki
analizi) biri hakkında hiç kayıt yok — bu 08-03'teki *"PCA hiç çağrılmadı"* bulgusuyla
tutarlı.

Küçük tutarsızlık: dosya adı ayırıcısı karışık — PAD/PAM alt çizgi
(`feedback_auto_mode_bash.md`), PQA/PCA tire (`feedback_hat-kapanisi-pam.md`). Kanonda
kural yok, ihlal değil.

## team/ — üretim hattının çıkış ucu hiç çalışmamış

`team/team-1-oy/` **tamamen boş ve git'te hiç yok.**
- `git ls-files team/` → boş (git boş dizin tutmaz)
- `git log -- team/` → **sıfır commit**
- Klasör tarihi 2 Ağustos 18:19 — reponun en eski artefaktlarından

`dagitim`'in beklediği dosyaların **hiçbiri yok:** `.claude-plugin/plugin.json`,
`hooks/hooks.json`, `KURULUM.md`, `.mcp.json`, `setup-{takim}` skill'i. Repo kökünde
`.claude-plugin/marketplace.json` de yok — dizin hiç mevcut değil.

**Anlamı:** `dagitim`'in 26 kuralı — **toplam kanonun %21'i** — sahada hiç sınanmamış.
`uretim/SKILL.md:349` kendi ölçütünü koyuyor: *"aynı durumu iki koşulda koştur — kural
varken ve yokken — ve farka bak. Fark yoksa kural çalışmıyordur."* Bu ölçüt `dagitim`
için hiç uygulanamamış.

Ve gerekçeleri **önceki kuşağın** sahasından geliyor (`DAG-SHIP-PRELOAD-HOOK`'un %91
vakası, `DAG-ONE-COLOR-PER-AGENT`'ın `pink` çakışması) — bu kanonun kendi sahasından
değil.

`trash/` de boş — `ISD-CONSOLIDATE-AT-END` hiç tetiklenmemiş.
