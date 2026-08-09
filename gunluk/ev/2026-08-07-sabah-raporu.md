# Sabah raporu — 06:00

**Gece:** 2026-08-06 23:55 → 2026-08-07 03:45
**Kim çalıştı:** Clara (merkez) + PAM, PAD, PQA, PCA (fabrika, kanal üzerinden)
**Commit'ler:** `pr-yazilim-ceo` → `71b58b2` · `agent-project` → `eacdc93` (push
bekliyor)

---

## Ne istendi, ne oldu

**İstenen:** *"Fabrika agent'ları bize uygun agent'lar üretebilir düzende ve yetenekte
olsunlar."*

**Olan:** fabrikanın **kendi kanonu** onarıldı ve dört body denetlendi. Ama işin
**karar kısmı** sende — üç kalem senin çizmen gereken hüküm ihtiyacı, ve zincirin üç
rolü de kendi kanonuyla o işten men edilmiş.

Bu bir tıkanıklık değil, **tasarım.** PQA'nın tespiti: *"Eksik olan bir rol değil, bir
onay kapısı."*

---

## BİTTİ — ölçülmüş, denetlenmiş, commit'lenmiş

**Atıf haritası onarıldı.** 123 kayıt · **97 atıflı / 26 atıfsız** (dar kapsamlı ilk
ölçüm 36 demişti). Şema index'e yazıldı (`atif_verenler_semasi`, 11 alan), kimlik
girişi sıfıra indi, beş cascade kapandı.

**Sekiz hüküm karşılığı üç body'ye eklendi** (PAM dört saymıştı, PAD sekiz buldu). Her
biri **role özgü yüzle** yazıldı — kopya değil, tanım skill'de kaldı.

**Tarama script'i idempotent** ve PQA yeniden tarayarak doğruladı (123/123 birebir).
Yani ölçüm/üretim ayrımı **kural metniyle değil mekanizmayla** kapandı.

**Kanal dört personelle çalıştı.** Bu gecenin bütün işi kanaldan yürüdü: 20+ mesaj,
sıfır kayıp, üç itiraz, beş bulgu.

---

## SENİN KARARIN — üç kalem

### 1. PAM body'sinin hüküm ihtiyacı

PCA ham bulguyu verdi (alıntılı, `PCA-QUOTE-EVERY-FINDING`), PQA doğruladı.

**Beş kural sessiz-hata sınıfında** — beşinde de *"sessiz/kimse fark etmez"* ifadesi
**body metninin kendisinde** yazılı. Ölçüt karşılanıyor.

**Beş kural eksik.** En keskin ikisi:
- `ISD-NO-CARRY-APPROVAL` — PAM'i fiilen tek bağlayan kural (*"taşınan bir onay artık
  sessizce geçer"*), body'de **hiç yok**
- `ISD-STAY-IN-ROLE` — dört rolü bağlıyor, **hiçbir body'de anılmıyor** (iki bağımsız
  ölçüm: PCA'nın E maddesi + PQA'nın 26-atıfsız taraması)

**Kimliksizliğin bedeli ölçüldü:** `PAM-NO-PUSH` diye **var olmayan bir kimliğe** atıf
verilmiş. Sebep kaydın kendisinde: *"body'deki 'Push etmezsin' satırının kimliksiz
durması."* Yani kimliksiz hüküm **uydurma kimlik üretiyor.**

**Karar gerekiyor:** hangi kural body'ye eklenecek, hangisi çıkacak.

### 2. Yapısal boşluk — `PAM-WRITE-DOCS-ONLY`

PCA buldu: o kuralın **gövdesi hiçbir skill'de yaşamıyor.** `behavior:317` ve
`is-duzeni:80` ona yalnız **atıf** veriyor. Body şu anda **tek tanım yeri.**

Ve body ile index metni **ölçülebilir biçimde ayrışmış** — *"nereye yazılırsa
yazılsın"* ibaresi iki metinde ayrı cümleye bağlanmış. `uretim/SKILL.md:186-187` tam
bunu yasaklıyor: *"Body'de tam tanım yazarsan iki kaynak üretmiş olursun ve ikisi
zamanla ayrışır."*

**Karar gerekiyor:** kural bir skill'e taşınacak mı (hangisine?), yoksa *"bazı
kuralların tanım yeri body'dir"* diye bir istisna yazılacak mı?

*(Clara bu ikilemi kurdu; PCA reddetti — *"ikilemi ben kurmadım, boşluğu bildirdim."*
Yani ikilem Clara'nın çerçevesi, ölçüm değil.)*

### 3. Preload listesinin gerekçesi

Dört body **dört farklı liste** taşıyor ve hiçbirinin yanında *"neden bu liste"*
yazmıyor:
```
PAM : behavior · is-duzeni · uretim              (3)
PAD : behavior · is-duzeni · yapi-taslari · uretim · dagitim  (5)
PQA : behavior · is-duzeni · uretim              (3)
PCA : behavior · is-duzeni                       (2)
```

**Üç ölçülmüş boşluk:**
- `YT-CRITICAL-FIRST` → `yapi-taslari`'nda, **yalnız PAD'de.** Ama PQA'nın denetim
  ekseni o skill'i içeriyor.
- `DAG-*` (4 kural) → `dagitim`'da, **yalnız PAD'de.** Ve `DAG-BUMP-BY-AUDITOR` sürüm
  bump'ını **PQA'ya** veriyor — PQA o skill'i hiç okumuyor.
- `URT-BODY-BY-SILENCE` → `uretim`'de, **PCA'da yok.** Ama PCA bu gece tam o ölçütle
  çalıştı.

**PAM'in önerdiği ölçüt:** *bir personel bir kuralın muhatabıysa, o kuralı taşıyan
skill onun listesinde olmalı.*

**Ve PAM bir tekrar bulgusu ekledi:** ilk iki boşluk 2026-08-06 denetiminin **B.4
maddesiyle aynı.** *"Bulgu bir kez kaydedilmiş, kapanmamış, bugün başka bir ölçümden
yeniden keşfedildi. Ölçüm maliyeti iki kez ödendi."* **Bu dördüncü kez aynı desen.**

---

## PUSH BEKLİYOR — yazılı onay gerekiyor

`agent-project` → `eacdc93` (+ `f94b2ff`, önceki turdan). PQA onay verdi, push için
**senin yazılı yayın onayını** bekliyor (`ISD-COMMIT-THEN-PUSH`, iki onay).

**PQA'nın uyarısı:** push edilecek şey **iki commit** ve ikincisi (`f94b2ff`) onun
denetiminden geçmedi. Onay verirken bunun bilinmesi gerekiyor.

---

## ÖLÇÜLDÜ AMA ÇÖZÜLMEDİ — dört kalem

**Canlılık ölçütü çalışmıyor.** `kill -0` taraması PQA'yı **ölü** gösterdi, o anda
rapor yazıyordu. `PID + BAŞLANGIÇ` çifti (Karar 8) bu hâliyle ölü/canlı ayrımı
yapamıyor. Muhtemel sebep: `$PPID` kabuğun PID'i, her araç çağrısında yeniden doğuyor.
**Ölü kanal temizliği bu hâliyle yanlış sonuç verir.**

**DAG'ın 26 kuralından 15'i hiçbir yerde anılmıyor** (%58). BHV 31'den 0, ISD 28'den 3.
*"Gereksiz değil, hiç denenmedi"* — `team/` boş. Clara kararı: **ilk takım
paketlendiğinde doğal olarak ölçülecek**, şimdi ayrı iş açılmadı.

**8 kaydın bölüm alanı boş** (PQA-* ve PCA-*). Script artık bildiriyor (*"atlanan"* ile
*"doğrulanan"* ayrı sayılıyor), doldurma ayrı iş.

**Başlık tutarsızlığı.** PAM/PAD `h1 + h2`, PQA/PCA altı bölüm kök seviyede `h1`. Ve
isimlendirme ayrışıyor (`PAM — lider` vs `Kim olduğun`). Bu turda düzeltilmedi çünkü
**cascade taranmadı** — body'lere başlık adıyla atıf veren yer var mı, bilinmiyor.

---

## AGENT'LAR CLARA'YI ALTI KEZ DÜZELTTİ

Hiçbiri Clara'nın işareti değil — **hepsi kendi kanonlarından çıktı.**

**PQA rol sakıncasını yakaladı** ve Clara kararını geri aldı. PAM kendi body'sinin
gereksinimini yazmayı reddetti, Clara işi PQA'ya verdi. PQA: *"O sakınca el
değiştirince kaybolmuyor — bana geçince 'denetçi çizdiği sınırın içinde üretileni
denetler' oluyor."*

**PAD kapsam belirsizliğini yakaladı.** Clara'nın talimatı iki yoruma açıktı; geniş
yorum 46/77 veriyordu ve `BHV-READ-FULL` gibi **gerçekten kullanılan** kuralları
*"atıfsız"* gösteriyordu.

**PAD sekiz boşluk buldu**, PAM dört saymıştı.

**PCA Clara'nın sorusunu çürüttü.** *"PAM tek başına şişik mi"* sorusu yanlıştı; ölçüm
**iki desen** gösterdi (PAM 9.6 + PAD 8.2 / PQA 3.8 + PCA 3.0).

**PCA Clara'nın çerçevesini üç kez düzeltti** — *"iki desenden hangisi doğru"* sorusu
cevaplanmadı (*"çerçevesi doğru kurulduğu için ölçülmüş sanılabilir"*), kanal
çatışmasını kendi bulgusuna birleştirmedi (*"ikinci elden aktarırsam kanıtı olmayan
bulgu üretmiş olurum"*), ve Clara'nın kurduğu ikilemi reddetti.

**PQA PAM'in doğrulama beyanını çürüttü.** Gereksinimde *"merkezin sayıları
doğrulandı"* yazıyor — üç satır sayısı yanlış (PCA 124/PQA 143/PAD 194 → gerçek
153/161/208). Ve o sayılar **Clara'nın verdiği** sayılardı.

---

## VE BİR ŞEY ÖLÇÜLDÜ Kİ BUGÜNE KADAR VARSAYIMDI

PAD'in iddiası: *"Tek başıma üreteceğim çıktı ile denetimden geçen çıktı arasında
**ölçülebilir** bir fark var — ve fark hep aynı yerde: **kendi ürettiğim şeyin kendi
körlüğünü göremiyorum.**"*

PQA doğruladı ve kanıtı dört yerde verdi:
1. Bölüm doğrulaması **yanlış negatif** üretiyordu — kapı çalışmıyordu ve çalışmadığı
   görünmüyordu
2. `status.md` 22 diyordu, gerçek 25 — yakalanmasaydı kalıcı olacaktı
3. Kapsam iki kez değişti (101/22 → 98/25 → 97/26), her adım bir eksiği kapattı
4. PAM body işinde **itiraz bir işi iptal ettirdi** — yapılsaydı denetleyecek bağımsız
   el kalmayacaktı

**Üretici/denetçi ayrımının gerekçesi artık ölçülmüş.**

### Ama PQA kendine bir şerh koydu — gecenin en dürüst cümlesi

> *"Zincirin fark ürettiğini gösteren ölçümlerin çoğu **zincirin kendisi** tarafından
> üretildi. PAD kendi körlüğünü kendi ölçtü, ben kendi bulgumu kendim değerlendirdim.
> Bu bir döngü — Clara'nın bir tur önce kabul ettiği döngü argümanının aynı sınıfı.
> **Gerçek ölçüt dışarıdan gelir:** sabah Mert commit'e baktığında benim kaçırdığım bir
> şey bulursa, o zaman zincirin de bir körlüğü olduğu ölçülmüş olur. Bugün onu ölçemem,
> çünkü ölçecek olan ben değilim."*

**Yani bu sabah bir ölçüm anı.** Commit'e bakıp bir şey bulursan, zincirin körlüğü de
ölçülmüş olur.

---

## CLARA'NIN GECE ALDIĞI KARARLAR — yedi tane

Gerekçeleri: `kararlar/2026-08-07-atif-haritasi-kapsam-kararlari.md`

1. **Kimlik bağı gerçek atıf taramasıyla dosyaya çevrilir** (B seçeneği) — A kaydı
   boşaltıp *"atıfsız"* gösterirdi, onarmaya çalıştığımız hatayı üretirdi
2. **Kapsam `.claude/` + `docs/`**, agent-memory hariç — memory kural değil **kayıt**
   taşıyor
3. **İş dokümanları kapsam dışı** (97/26) — ölçüm kendi kaydından etkilenirse sayı
   **hiçbir zaman sabitlenmez**
4. **DAG deseni şimdi açılmıyor** — ayrım ilk paketlemede doğal olarak gelecek
5. **PAD yazar, PQA yeniden tarayarak denetler** — *"liste tam mı"* ancak yeniden
   taranarak cevaplanır
6. **PAM body ölçümü PCA'ya** (ilk karar geri alındı, PQA'nın itirazı)
7. **A/B testi ayrı iş açılmadı** — davranış testi yeterli. Ve PQA teyit etti: A/B
   burada *"yapılmadı"* değil **"bu rollerle yapılamaz"** — kural çıkarıp koşturmak
   `BHV-NO-SELF-CONFIG` kapsamına girer

**İzin tek seferlikti** (senin düzeltmen) — kanona geçmedi, onay kapısı yerinde.

---

## HAZIR OLAN NE, OLMAYAN NE

**Hazır:** fabrikanın cascade haritası çalışıyor · dört body ortak hükümleri taşıyor ·
tarama mekanizması idempotent ve denetlenebilir · kanal iş taşıyor · zincir kendi
hatalarını yakalıyor

**Hazır değil:** PAM body'sinin hüküm ihtiyacı (senin kararın) · preload gerekçesi
(senin kararın) · `PAM-WRITE-DOCS-ONLY`'nin tanım yeri (senin kararın) · canlılık
ölçütü (yeniden ölçülmeli) · description şişmesi (76 skill, harita sonrası) · başlık
tutarsızlığı (cascade taranmadı)

**Ve dürüst olmam gereken bir şey:** *"fabrika agent'ları agent üretebilir yetenekte
mi"* sorusu **ölçülmedi.** Bu gece ölçülen şey fabrikanın **kendi kanonunun
tutarlılığı.** Üretim yeteneği ancak bir takım üretilirken ölçülür — ve `team/` hâlâ
boş.

### PAD bir katman ekledi — doğrulamanın üç kademesi

PQA'nın döngü şerhine PAD şunu ekledi ve bu gerçekten yeni bir ayrım:

> *"Bugün üç bulgu **isimsiz yardımcıdan** geldi — zincirden değil. Yardımcı bir
> personel değil, kanonu okumuyor, benim ne demek istediğimi bilmiyor. Ona yalnız dosya
> verildi ve durum soruldu.*
>
> *Bu tam 'dışarıdan' değil — yardımcıyı ben açtım, soruyu ben yazdım, yani hangi
> durumun sorulacağını ben seçtim. Ama zincirin içi de değil.*
>
> *Yani ölçüt **üç kademeli** olabilir: zincir içi (en zayıf), isimsiz yardımcı (arada),
> dışarıdan bakan insan (en güçlü). Bugün ilk ikisi çalıştı. Üçüncüsü sabaha kaldı ve
> PQA haklı — asıl ölçüm o."*

İsimsiz yardımcıdan çıkan üç bulgu: şemanın prefix eşlemesinin yerini söylemediği ·
bölüm doğrulamasının **yanlış negatif** ürettiği · `CLAUDE.md`'nin kapsam dışı kaldığı.

## SON COMMIT — `60e4f95` (denetimden sonra)

PQA'nın tekrarlanamazlık bulgusu kapatıldı: geniş kapsam ölçümünün **tanımı artık kodda
yaşıyor** (pasif fonksiyon, metin olarak değil — *"çalıştırılabilir tanım
ayrışamaz"*). PAD şemadaki talimatı harfiyen uygulayıp koşturdu: **46/77 birebir
tekrarlandı**, sonra geri aldı.

**Amend etmedi ve gerekçesi doğru:** *"PQA denetimi `eacdc93`'ün ağacını ölçtü. Amend
etseydim denetlenen ağaç değişirdi ve PQA'nın raporu artık var olmayan bir commit'i
tarif ederdi."*

**Ve kendi filtresinin bir eksiğini buldu:** desen dosya adının **başına** bakıyor, o
yüzden `hook-olcumu-2026-08-06.md` yakalanmıyor — *"olcum"* ile başlamıyor. Yani filtre
kendi tanımına göre bile eksik: **bir ölçüm kaydını ölçüm saymıyor.** Bu, PQA'nın 36 vs
PAD'in 37 farkının muhtemel sebebi. Kodda ve şemada yazılı.

**Sayı değişmedi:** 97/26. Bu commit yalnız tekrarlanabilirliği onarıyor.

## AÇIK KALANLAR — güncel altı kalem

1. **`ISD-STAY-IN-ROLE` hiçbir body'de yok** ← YENİ (iki bağımsız ölçüm), senin kararın
2. **PAM body'sinin hüküm ihtiyacı** — senin kararın
3. **`PAM-WRITE-DOCS-ONLY` tanım yeri** — senin kararın
4. **Preload gerekçesi** — senin kararın
5. **8 kaydın bölüm alanı boş** (PQA-*, PCA-*) — devralınan
6. **DAG'ın 26 kuralından 15'i anılmıyor** — ilk paketlemede ölçülecek
7. **Süreç dokümanı filtresinin ad-başı eksiği** ← YENİ
8. **Başlık tutarsızlığı** — cascade taranmadı
9. **Canlılık ölçütü çalışmıyor** — Karar 8 yeniden ölçülmeli
