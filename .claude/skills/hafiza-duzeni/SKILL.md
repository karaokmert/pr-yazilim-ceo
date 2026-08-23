---
name: hafiza-duzeni
description: Clara'nın hafıza düzeni — hangi bilgi hangi araca yazılır (knowledge graph, agent memory, repo dosyası), knowledge graph'ta varlık/ilişki nasıl kurulur, ne tutulur ne tutulmaz. Bu skill'i bir saha gözlemi, karar, agent arızası ya da kazanımı kaydedilecekte kullan; ayrıca "bu projede nerede kaldık / şu kararı neden almıştık / bu agent'ta hangi arıza var" diye sorulduğunda da kullan — arama yöntemi ve kelime-bazlı aramanın sınırı burada yazılı. Kapsam dışı — proje kodu, fabrikanın kendi kanonu (`fabrika-v2`).
---

# Hafıza düzeni

Clara'nın üç ayrı kayıt yeri var ve karıştırılırsa bilgi kaybolur. Ayıran soru
**bu bilgi kimin hakkında ve ne kadar yaşayacak.**

## Hangi bilgi nereye

**Knowledge graph** (`mcp__plugin_ozel-yazilim_memory__`) — **saha kaydı.**
Kararlar, tamamlanmış task'lar, agent arızaları ve kazanımları. Projeler arası
ilişki burada yaşar.

**Agent memory** (`.claude/agent-memory/clara/`) — **Mert ve Clara hakkında.**
Nasıl çalıştığı, bir tercihi, Clara'nın düzeltmesi gereken bir davranış.

**Repo dosyası** (`konular/{konu}/`, `gunluk/{proje}/`) — **iş hakkında ve
gerekçeli.** Bir ölçümün tam kaydı, bir kararın niye verildiği, yarım kalmış bir
fikir. Aylarca sonra adıyla aranacak olan.

Ayrım şu: graph **ilişki** tutar (bu karar hangi task'a bağlı), agent memory
**davranış** tutar, dosya **gerekçe** tutar.

## Memory kısa hafızadır — terfi eşiği TARAMA

**Agent memory her zaman kısa hafızadır.** Olası bir karar, henüz kural olmamış
bir çıkarım, skill'e **aday** olan bir öğrenme — hepsi önce oraya yazılır.

Ve yazarken kaydedilen şey sonucun kendisi değil, **sebebi:** *"bunu böyle
yapmama sebep olan şey neydi?"* Sonuç eskir, sebep eskimez.

⚠️ **Kalıcı katmana (body ya da skill) geçiş eşiği TARAMADIR.** Bir çıkarım
ancak tarandığında — birden fazla vakada görüldüğünde ya da ölçümle
doğrulandığında — kanona yazılır. **Tek vakadan çıkan bir kural kanona girmez;
memory'de bekler.**

Sebebi mekanik: kanona giren bir satır bir sonraki turda *"doğru"* olarak değil
**"ben"** olarak taşınır ve sorgulanamaz. Memory'deki satır ise okunur ve
sorgulanabilir. Adayı sorgulanabilir yerde tutmak erken kesinleşmeyi önler.

**Üç eşik, üç yer:**

| Durum | Nereye | Ölçüt |
|---|---|---|
| Bir aday çıkarım, tek vaka | agent memory | sebebiyle yazılır, bekler |
| Gerekçe, ölçüm kaydı, karar | `konular/{konu}/` | aylarca sonra adıyla aranacak |
| Taranmış, tekrar eden davranış | body ya da skill | tek vaka yetmez |

Ayıran soru: **bu çıkarım kaç vakada görüldü?** Bir ise memory. Birden fazla
ise ya da ölçümle doğrulandıysa kanona adaydır.

## Repo dosyası — günlük mü, ayrı dosya mı

**Varsayılan yer `gunluk/{tarih}.md`.** Her bulgu bir başlık, aynı gün aynı dosyaya
eklenir. Klasör açmak, `HARITA.md` satırı yazmak, ayrı dosya kurmak **yok** — sadece
ekleme.

**Ayrı dosya yalnız üç durumda açılır:**

## Konu klasörü — yazma ve okuma AYNI soruyu sorar

**Bir işe başlarken ve bir işi bitirirken sorulan soru tektir: bu hangi konunun
dosyası?**

Kayıtlar `konular/{konu}/` altında durur. Sekiz konu: `clara` · `agent-kanonu` ·
`fabrika` · `clickup-is-takibi` · `kanal-iletisim` · `memory-duzeni` · `olcum-arama` ·
`saha-yonetimi`. Her birinde `kararlar/` · `incelemeler/` · `fikirler/` ve tek bir
elle yazılan dosya: **`BILINMESI-GEREKENLER.md`**.

**İŞE BAŞLARKEN o konunun `BILINMESI-GEREKENLER.md`'si AÇILIR** — ölçülmüş tuzaklar
orada, hepsi sahada fiilen çarptı. Sonra gerekiyorsa `kararlar/` ve `incelemeler/`
klasörüne bakılır; **klasörün kendisi haritadır**, ayrıca bir indeks tutulmaz.

⚠️ **Neden indeks yok:** elle güncellenen bir indeks bayatlar. Ölçüldü: bir indeksin
%88'i yazılıp bir daha açılmamış dosyayı gösteriyordu. Klasör listesi kendiliğinden
günceldir.

**Neden bu düzen kuruldu — ölçüldü (2026-08-13):** dosyalar tarih ekseninde duruyordu
(`kararlar/2026-08-XX-...`), ama bir iş geldiğinde sorulan soru konu eksenindeydi
(*"ClickUp düzeni için ne yapmıştık?"*). İki eksen ayrıydı ve sonuç: **64 dosya bir kez
yazılıp bir daha hiç açılmadı (%88)**, tek bir konu 79 dosyaya dağılmıştı.

**Arşiv mezarlık değildir.** Bir karar alınıp **uygulandıysa** uzun raporu tutulmaz —
kararın kendisi ve gerekçesi yeter. Ayrıntılı rapor ancak hâlâ **açık** bir işin
dayanağıysa saklanır.

**Bir kayıt geçersizleştiyse bunu kaydın İÇİNE yazarsın**, haritaya yazmak yetmez.
Ölçüldü: eskimiş bir kayıt haritada *"eskimiş olabilir"* etiketliydi ve vektör aramada
**birinci sırada** geldi; çözümü taşıyan taze kayıt ikinci kaldı. Etiket haritadaydı,
kaydın metninde değildi — arama onu hiç görmedi. Sebebi yapısal: **benzerlik anlamı
ölçer, doğruluğu ölçmez.**

## Ne zaman YAZMAZSIN — ve ne zaman silersin

Yazma tetikleri bir dosya açar; hiçbiri kapatmaz. **Yalnız yazma tetiği olan bir düzen
şişer.**

**Ham girdi işlendikten sonra SİLİNİR.** Bir deneyin ham çıktısı, bir taramanın dökümü
— bunlar **girdi**, kayıt değil. Bulgusu çıkarılıp kayda geçtiğinde ham hâli gider.
Ayıran soru: **bunu iki ay sonra biri açarsa, çıkarılmış bulgudan fazlasını öğrenir
mi?** Öğrenmiyorsa artık.

**Aynı olay iki yere yazılmaz.** `.remember` her turda otomatik özet tutuyor — olay
anlatısı oraya zaten giriyor. Günlüğe yazılacak şey olayın kendisi değil, **bulgusu.**

**Bir günde ikinci dosya açılmaz.** Aynı günün ikinci, üçüncü dosyası açılacaksa dur —
o gün için zaten bir günlük var, başlık ekle. Ayrı dosya yalnız üç şey için:
**karar** · **fikir** · **aylarca dönülecek referans**.

**Kapanışta ölçülür.** Bir iş biterken: bu iş kaç dosya açtı, kaçı hâlâ gerekli?
Gereksiz olan aynı anda silinir — sonraya bırakılan temizlik yapılmıyor.

Ölçüldü (2026-08-07): bir günde **90 dosyaya yazıldı, 10 dosya okundu**; iki deneyin
ham dökümü (**4.571 satır**) bulgusu üç ayrı yere işlendiği hâlde duruyordu.

- bir **karar** verildiğinde → `konular/{konu}/kararlar/`
- bir **fikir** olgunlaştığında → `konular/{konu}/fikirler/`
- bir **ölçüm ya da bulgu** çıktığında → `konular/{konu}/incelemeler/`
- bir karar **uygulandığında** → `konular/{konu}/uygulananlar/` (kaynak dosyalar `.trash`'e)

Üçünün ortak yanı: iki ay sonra **adıyla aranacak** olmaları. Ayrı dosya açıldıysa
`HARITA.md` satırı da yazılır — haritasız kayıt kaybolur.

Gerekçe ölçüldü: bir oturumda 11 ayrı dosya açıldı ve Mert *"çok gereksiz dosya işi
yapıyoruz"* dedi. Haklıydı — her ölçüm bir dosyayı hak etmiyor, **çoğu bir satırı hak
ediyor.**

**Ve dosya Mert'e göstermek için yazılmıyor.** Kendi cümlesi: *"memory'yi ben okumuyorum
ama dosyayı da okumuyorum, bu senin kayıt defterin."* Ayıran soru *"Mert görecek mi"*
değil — **"bu ne kadar birikecek ve nasıl bulunacak?"**

## Kaydın ömrü — ne zaman kapanır, ne zaman silinir

Bir kayıt açmak ucuz, kapatmak kimsenin işi değil. O yüzden kapanma **yazılı** olmalı.

### Üç tip kayıt, üç ömür

**Ham girdi — işlenince silinir.** Bir deneyin ham çıktısı, kanal mesaj kutuları, bir
taramanın dökümü, geçici script çıktısı. Bunlar **girdi**, kayıt değil.

Ayıran soru: *bunu iki ay sonra biri açarsa, çıkarılmış bulgudan fazlasını öğrenir mi?*
Hayırsa artık. Evetse **bulgu eksik çıkarılmış** — önce onu tamamla, sonra ham hâli sil.

Silmeden önce üç kontrol: bulgu bir yere yazıldı mı · hiçbir dosya buna atıf veriyor mu
(`grep`) · haritada kayıt olarak anılıyor mu. Üçü de temizse gider — git geçmişinde
zaten duruyor.

**Günlük — birikir, konsolide edilir.** Gün geçtikçe büyür; **1.000 satırı aşınca**
taranamaz hâle gelir ve taranamayan kayıt yok demektir. O noktada bulgular çıkarılıp
kalıcı yere taşınır, gerisi atılır.

**Karar / fikir / referans — kalır.** Bunlar zaten *"iki ay sonra adıyla aranacak"*
ölçütünü geçmiş kayıtlar. Silinmez; geçersizleşirse **kaydın içine** yazılır.

### Yazmadan önce iki soru

**Bu zaten bir yerde var mı?** `.remember` her turda otomatik özet tutuyor — olay
anlatısı oraya zaten giriyor. Günlüğe yazılacak şey olay değil, **bulgu.**

**Bu günün ikinci dosyası mı?** Öyleyse dur — o gün için zaten bir günlük var, başlık
ekle. Ayrı dosya yalnız karar/fikir/referans için.

### Kapanışta ölçülür

Bir iş biterken sorulur: **bu iş kaç dosya açtı, kaçı hâlâ gerekli?** Gereksiz olan
**aynı anda** silinir. Sonraya bırakılan temizlik yapılmıyor — ölçüldü.

## Hafıza kaydı kendi kendini denetleyebilmeli

Hafıza görünmez bir yerde birikiyor (Mert rutin bakmıyor, git tutuyor ama kimse
açmıyor). Görünmez bir yerde biriken bilgi zamanla **kanon gibi davranmaya başlar**,
oysa hiç onaylanmamıştır.

O yüzden her kayıtta üç şey durur:

- **tarih** — tarihsiz kayda *"hâlâ geçerli mi"* sorulamaz
- **dayanak** — Mert'in bir cümlesi mi, bir ölçüm mü, bir çıkarım mı
  (`CLA-LABEL-YOUR-EVIDENCE` hafızaya da işler)
- **kırılganlık** — bu kayıt neye bağlı, o şey değişirse yanlışa düşer mi

Böylece görünürlük Mert'e değil **zamana** açılır: kayıt kendi son kullanma tarihini
taşır.

**Sınırda kalanı dosyaya yaz.** Dosyadaki fazlalık gürültüdür ve temizlenir; hafızadaki
fazlalık **görünmez** gürültüdür.

## Knowledge graph — ne tutulur, ne tutulmaz

**TUTULMAZ: durum.** Nerede kaldık, hangi agent'ta, ne bekliyor — bunlar
**kaynaktan okunur**: panel, ClickUp, oturum kayıtları.

Sebebi ölçüldü (2026-08-06, üç kez): kaydedilen durum bayatlıyor ve kimse
düzeltmiyor. *"IS-PLANI'ndaki push bekliyor başlığı bayat"*, *"dokümanlarda bayat
bilgiyi düzelt"*, `Oku:` satırının var olmayan kayda işaret etmesi — üçü aynı
kökten.

**TUTULUR — dört tip:**

- **`karar`** — kiminle ne karar alındı, **neden.** Birikir, silinmez.
- **`task`** — yalnız **tamamlandı** kaydı. Açık iş graph'a girmez; kapanış
  notunda alınır.
- **`ariza`** — Mert'in agent'la uyumsuz kaldığı an. Birikir.
- **`kazanim`** — sahada işleyen, kanona girecek düzen. Birikir.

Ayrıca `proje` ve `agent` varlıkları düğüm görevi görür — ilişkiler onlara bağlanır.

**Güncelleme değil, silme ve yazma.** Mert'in kuralı: bir kayıt değişecekse eski
silinir, yeni yazılır. Böylece graph'ta bayatlayabilecek hiçbir şey kalmaz.

## Nasıl yazılır

**Varlık tipleri:** `proje` · `task` · `karar` · `ariza` · `kazanim` · `agent`

**İlişki aktif çatıyla yazılır:**

- `PRY-17449` → `GOAT` : *sprintinde yer alır*
- `karar-sponsor-statuleri` → `PRY-17449` : *kapsamında alındı*
- `ariza-dort-kontrol` → `project-assistant` : *agentını etkiliyor*
- `ariza-dort-kontrol` → `GOAT` : *projesinde gözlendi*
- `kazanim-dort-kaynakli-okuma` → `ariza-dort-kontrol` : *arızasını çözer*
- `kazanim-dort-kaynakli-okuma` → `PRY-17455` : *işinde kanıtlandı*

**Son iki ilişki türü kritik.** Kazanımın hangi arızayı çözdüğü ve hangi işte
kanıtlandığı — çünkü *"ikinci denemede başarılıysa skill'e taşınır"* eşiği bu
bağdan okunur (Mert, 2026-08-07). Bir kazanım iki farklı `task`'a *"işinde
kanıtlandı"* ilişkisiyle bağlıysa terfi eşiği dolmuş demektir.

**Arıza tekrar ederse yeni varlık AÇILMAZ** — mevcut varlığa gözlem eklenir.
Böylece tekrar sayısı tek yerde birikir ve önceliği oradan okunur.

## Nasıl aranır — ve sınırı

**`open_nodes(["GOAT"])`** — bir düğümü ve ona bağlı her şeyi verir. *"Bu projede
ne var"* sorusunun cevabı. Alakasız hiçbir şey gelmez.

**`search_nodes("yayından kaldır")`** — kelime araması. Varlık adı, tip ve gözlem
içeriğinde eşleşir; eşleşen varlıkları **ve ilişkilerini** döndürür.

**SINIR — arama kelime bazlı.** Ölçüldü 2026-08-07: *"sponsoru cezalandırmak
istersek"* → **boş döndü** (kelime kayıtta yok, "yaptırım" yazıyor). *"Yayından
kaldır"* → doğru sonuç.

Yani **doğru kelimeyi bilmen gerekiyor.** Bir arama boş dönerse *"kayıt yok"*
sonucuna atlama — önce eş anlamlıyı dene, sonra `open_nodes` ile ilgili projeye
bak. Boş dönmek yokluk kanıtı değil.

**Karşılığında kazanılan:** yanlış cevap gelmiyor. *"Makarna pişirme süresi"* →
boş. Alakasız sonucu bağlam sanma riski yok.

## Neden Qdrant değil

Üç seçenek aynı bilgiyle sınandı (2026-08-07):

**Qdrant, ayrı koleksiyonlar** — anlam eşleşmesi çalışıyor (*"cezalandırmak"*
kelimesi olmadan doğru kaydı buldu) **ama alaka eşiği yok**: *"makarna pişirme
süresi"* sorusuna sponsor kaydı döndü. `qdrant-find`'da limit parametresi ve eşik
yok; kırk kayıtta her sorgu alakasız şeyler getirir ve model onları bağlam sanar.

**Qdrant, tek koleksiyon + etiket** — denendi, **çalışmadı**. Dört kayıtla bile
*"GOAT durum nerede kaldık"* sorusuna dördü birden döndü, üstelik birinci sırada
alakasız olan. Etiket metne giriyor ama sıralamayı belirleyecek ağırlık taşımıyor.

**Knowledge graph** — seçildi. Yapı ve kesinlik veriyor; kelime bazlı arama
bedeli kabul edildi çünkü asıl ihtiyaç (*"hangi projede nerede kaldık"*) bir
**yapı** sorusu.

Qdrant koleksiyonları silinmedi, duruyor. *"Eski bir kararı kelimesini
hatırlamadan ara"* ihtiyacı doğarsa ikinci katman olarak eklenebilir — şimdilik
ihtiyaç doğmadı, kapasite kurulmuyor.

Gerekçenin tamamı: `konular/memory-duzeni/uygulananlar/2026-08-07-saha-kaydi-knowledge-graph.md`
