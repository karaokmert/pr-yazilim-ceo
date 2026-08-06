# Qdrant kayıt biçimi ve arama disiplini — beş biçim, dört ölçüm

**Tarih:** 2026-08-06
**Soru:** Clara gelecekte ihtiyaç duyacağı kayıtları hangi biçimde kaydederse
bulabiliyor?
**Script'ler:** `sprint/kayit-bicimi-deneyi.py`, `qdrant-kategori.py`,
`qdrant-cakisma.py`, `qdrant-filtre.py`

Mert'in tarifi ölçümün sebebiydi: *"sen hepsini dosya gibi atarsan olmaz, kendine göre
anlamlı gruplayarak ve kategori ederek yüklemen lazım... doğru kayıt yöntemini bulana
kadar kayıt etmen lazım ki en iyi indekslediğini netleştirip kurala çevirelim."*

## Ölçüm 1 — kayıt biçimi: A 4/10, B 8-9/10, C 8/10, D1 9/10, D2 7/10

Aynı 71 dosya beş biçimde indekslendi, aynı 10 soru soruldu. Ölçüt: doğru dosya
**birinci sırada** mı? Beklenen dosya deseni sonuç görülmeden yazıldı.

**A — yapısal.** `##` başlığından böl, uzunluk sınırı yok. 574 kayıt, en büyüğü
**9692 karakter.** → **4/10**

**B — anlam birimi.** 1400 karakteri aşanı paragraf sınırından tekrar böl, her parça
kendi başlığını taşır. 787 kayıt, en büyüğü 3020. → **8/10** (desen düzeltmesiyle 9/10)

**C — anlam + öz.** B + her kaydın başına tek cümle özet, özet aranan metne de girer.
→ **8/10**, ama skorlar düştü (0.744→0.674) ve indeksleme %30 arttı.

**D1 — anlam + metadata (payload'da).** B'ye `tur`/`tarih`/`konu` eklendi, aranan
metne **girmedi**. → **9/10**, B ile **birebir aynı skorlar.**

**D2 — anlam + metadata (metne katılmış).** Kategori etiketi aranan metne girdi.
→ **7/10**

## Bulgu 1 — kaybolan şey bilgi değil, ÇÖZÜNÜRLÜK

A'nın kaçırdığı sorularda dönen kayıt hep "doğru konuya yakın ama yanlış dosya"
oldu. En temiz örnek — *"hangi hatayı iki kez yaptım"*:

- A → `fikirler/agent-iletisim-kanali/DENEYIM-web-pa.md` (0.497) — yanlış
- B → `gunluk/2026-08-05.md › Bulgu 25 — Aynı hata ikinci kez` (0.528) — doğru

**Bulgu 25 A'nın indeksinde de vardı.** 9692 karakterlik bloğun içinde eridi; vektör
onu "günlük geneli" olarak temsil etti, "tekrarlanan hata" olarak değil.

Sebep model limitinde: `max_position_embeddings` = **514 token.** A'da 121 kayıt bu
sınırı aşıyordu, 12 tanesi 5000+ karakter, en büyüğü limitin ~6 katı.

## Bulgu 2 — aranan metne EK yazmak isabeti düşürüyor (iki bağımsız kanıt)

C (öz ekleme) ve D2 (kategori ekleme) ayrı denemelerdi, ikisi de aynı sonucu verdi:
metne eklenen sabit ifade skorları düşürüyor.

D2'nin bozduğu iki soru:
- *"qdrant boyutu neden 768 seçildi"* → karar dosyası yerine kendi ölçüm kaydımı
  getirdi (`Sonuç: A 4/10, B 8/10`)
- *"kanal kuralı kaça kadar tuttu"* → günlük yerine kanon yetkisi kararını getirdi

**Mekanizma — sinyal seyreltmesi.** 90 kayıtta aynı *"verilmiş karar ve gerekçesi"*
öneki geçince o kelimeler ayırt edici olmaktan çıkıyor; her kayıt biraz daha
birbirine benziyor.

**Sonuç:** metin kendi başına bırakılır, ek bilgi **payload'a** yazılır. D1'in B ile
birebir aynı sonuç vermesi bunun mekanik kanıtı — payload vektöre hiç dokunmuyor.

## Ölçüm 2 — FİLTRE: 5/7 → 7/7, ve "skor = alaka" varsayımını çürütüyor

D1 üzerinde `tur` filtresiyle arama denendi. **Filtresiz 5/7, filtreli 7/7.**

Düzelen iki soru da kanon sorusuydu:

*"bir şeyin sonucunu erken okumanın zararı ne"*
- filtresiz → `incelemeler/pa-davranis-senaryolari/senaryo-1...` **0.581** — yanlış
- `tur=kanon` → `.claude/agents/clara.md` **0.534** — doğru

*"agent çağırmak neden yasak"*
- filtresiz → `CLAUDE.md` 0.662 — yanlış (oda kuralı, Clara kuralı değil)
- `tur=kanon` → `.claude/agents/clara.md` 0.651 — doğru

**ASIL BULGU:** doğru cevap zaten listede vardı, ikinci sıradaydı. Filtre onu
birinciye **çıkarmadı** — üstündeki yanlışları **kaldırdı.**

Yani 0.581 skorlu kayıt yanlış, 0.534 skorlu kayıt doğru. **Skor alakayı ölçmüyor.**
Sıralamaya güvenmek hata; sıralamayı daraltmak çözüm.

## Bulgu 3 — filtre eşik yerine GEÇMEZ

Formula 1 sorusu `tur=karar` filtresi içinde de bir karar buldu (**0.463**). Filtre
sonuç **sayısını** daraltır, **skoru** değiştirmez — alakasız soru filtre içinde de
en yakın komşusunu bulur.

Ve eşik zaten yazılamıyor. 787 kayıtta ölçüldü:

- *"İtalyan mutfağında makarna pişirme süresi"* → 0.396
- *"2024 Formula 1 şampiyonu kim"* → **0.507** (`HARITA.md`'den)
- *"preload arızası nedir"* (gerçek soru) → **0.564**

**Aralık 0.057.** Dün 4 kayıtlık kutuda alakasız soru 0.156 alıyordu; koleksiyon
büyüdükçe alakasızın en yakın komşusu da yakınlaştı (yüksek boyutlu uzayda mesafe
yoğunlaşması).

## Bulgu 4 — TAZELİK KÖRLÜĞÜ: eskimiş kayıt taze kaydı bastırıyor

En ağır bulgu ve kayıt biçiminden **bağımsız** — vektör aramanın yapısal körlüğü.

*"skill preload sorunu çözüldü mü"* → ilk beş sonucun **üçü** "eskimiş olabilir"
etiketli dosyadan:

- **0.670** `incelemeler/skill-preload-bulgusu/kayit.md › Yürürlükteki çözüm` ← ESKİMİŞ
- 0.651 `gunluk/2026-08-05.md` ← taze, çözümün yazılı olduğu yer
- 0.637 `incelemeler/skill-preload-bulgusu/kayit.md › Bedeli` ← ESKİMİŞ
- 0.621 `incelemeler/skill-preload-bulgusu/kayit.md › Hâlâ açık` ← ESKİMİŞ

Fark 0.019 ve eskimiş olan **birinci.**

**Mekanizma:** benzerlik anlamı ölçer, doğruluğu ölçmez. Eskimiş kayıt soruya *daha
benziyor* çünkü sorunu ayrıntılı anlatıyor; taze kayıt "çözüldü, hook kuruldu" diye
kısa geçiyor — daha doğru ama daha az benzer.

**Ve kendi uyarı sistemim kör noktada:** "eskimiş olabilir" etiketi `HARITA.md`'de
duruyor, kaydın İÇİNDE değil. Vektör o etiketi hiç görmüyor.

## Bulgu 5 — liste sorusu cevaplanamıyor

*"hangi kararlar 5 Ağustos'ta verildi"* → 5 sonuç yalnız **3 ayrı dosyadan** (ikisi
çifter). Beş kararı değil, üç kararın parçalarını getiriyor.

Ve *"preload arızası ne zaman bulundu"* → ilk beşte preload dosyası **hiç yok**
(`fabrika-olcutu`, `sprint-yonetimi`, `pam-claude-md-yetkisi` geldi, skorlar
0.50-0.55). Tam adı yazıldığı halde bulunamadı; `grep` bunu 0.02 saniyede bulur.

## Bulgu 6 — tarih filtresi yarım kullanılabilir: 473/797 kayıt TARİHSİZ

Kategori dağılımı (797 kayıt): gunluk 389, inceleme 132, kanon 102, karar 90,
fikir 26, bulgu 24, ders 18, proje 16.

**Ama %59'u tarihsiz.** Tarih filtresi koyduğumda o kayıtlar **hiç görünmüyor** —
sessiz kayıp. Testte görüldü: `sprint-yonetimi/SKILL.md` (0.501) filtreli aramada
tamamen düştü.

## Bulgu 7 — MCP filtre DESTEKLEMİYOR

`qdrant-find` şeması: `{collection_name, query}` — filtre parametresi yok.
`qdrant-store`: `{collection_name, information, metadata}` — metadata **yazılabiliyor.**

Yani: **metadata yazılabiliyor ama aranırken filtrelenemiyor.** Ölçümün tek işe
yarayan iyileştirmesi (filtre, 5/7→7/7) MCP aracından kullanılamıyor — yalnızca
script'ten.

## Çıkan kurallar

**QK-1 — anlam birimine böl, 1400 karakter üstünü paragraf sınırından ayır.**
Her parça kendi başlığını taşır. Gerekçe: model 514 token'da doyuyor. Ölçüm: 4/10→9/10.

**QK-2 — aranan metne ek yazma; kategori/tarih/konu payload'a gider.**
Gerekçe: sabit önek sinyali seyreltiyor. İki bağımsız ölçüm (C ve D2) aynı sonucu verdi.

**QK-3 — aradığın şeyin türünü biliyorsan filtre koy.** Ölçüm: 5/7→7/7. Filtre
yanlışları kaldırır, doğruyu yukarı çıkarmaz — bu yüzden skor sıralamasına güvenilmez.

**QK-4 — vektör aramanın çıktısı cevap değil ADRES.** Bulunan kaydı açıp okumadan
hüküm verilmez. Gerekçe: skorla alakalıyı alakasızdan ayırmak mümkün değil (0.507 vs
0.564) ve MCP skoru göstermiyor.

**QK-5 — tazelik körlüğü: durum bilgisi kaydın İÇİNDE olmalı.** Eskimiş kayıt taze
kaydı bastırıyor (0.670 vs 0.651). Bir kayıt geçersizleştiyse bunu haritaya yazmak
yetmez — kaydın kendi metnine yazılmalı, yoksa arama geçmişi bugün sanır.

**QK-6 — tam ad/ID araması grep'in işi.** *"preload arızası"* tam adıyla arandı,
vektör ilk beşte getirmedi. Bilinen bir kelime/ID aranıyorsa vektöre gitmeden grep.

## Açık kalem — MCP kararı Mert'te

Filtre tek işe yarayan iyileştirme ama MCP desteklemiyor. Üç yol var, ölçülmeden
kodlanmamalı:

**(a)** Artımlı indeksleme yazılır, **arama script'ten** yapılır — MCP yalnız yazma
için kalır.
**(b)** MCP filtre destekleyen bir sunucuyla değiştirilir (araştırılmadı).
**(c)** Vektör bırakılır; `grep` + `HARITA.md` yeter — bu odada günde ~5-10 arama
yapılıyor ve grep beş aramayı 0.041 saniyede yapıyor.

Ölçülmeyen: model üretimi özet (C'de özet kuralla çıkarıldı), artımlı indeksleme
maliyeti, filtre destekleyen alternatif MCP sunucuları.

**Koleksiyonlar duruyor:** `clara-deney-a/-b/-c/-d1/-d2`. Karşılaştırma
tekrarlanabilir olsun diye silinmedi.
