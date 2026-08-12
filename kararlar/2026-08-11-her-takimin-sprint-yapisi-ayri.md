# Her takımın sprint yapısı ayrı — ortak skill yok

**Tarih:** 2026-08-11 · **Karar:** Mert · **Bağlam:** fabrika oturumu, sprint yöntemi işi

## Karar

**Üç ayrı sprint yapısı olur, hiçbiri diğerinin skill'ini kullanmaz.**

```
OY (müşteri projeleri)  →  PA + ekip, ClickUp task'ları, discovery üretimi
Clara + Mert            →  haftalık döngü, Çarşamba–Çarşamba
Fabrika                 →  kendi işi, kendi kanonu
```

Mert'in cümlesi: *"OY başka Clara başka Fabrika başka hepsi ortak skill kullanmaz.
her takımın sprint yapısı başka."*

**Ve sprint'i kapsam bitirir, takvim değil.** Sprint kapsamdaki işler bitince biter;
Çarşamba sabahı bir **kontrol anı** olarak kalır (*"kapsam tükendi mi, tükenmiyorsa
neden"*). Kabul edilen bedel: bitiş öngörülebilir olmaz.

## Neden bu karar — ve neden sorulan soru yanlıştı

Clara üç seçenek sundu: *"fabrika üretir Clara taşır"* / *"fabrika Clara'nın reposuna
yazar"* / *"yalnız OY plugin'e girer"*. **Üçü de tek bir ortak yöntem varsayıyordu** ve
soru *"hangi repo yazacak"* diye kurulmuştu.

Mert hiçbirini seçmedi; sorunun kendisini reddetti.

### Kırılan sıçrama

PAM'in ve Clara'nın ortak akıl yürütmesi şuydu:

> iskelet dört kaynakta ortak çıktı → **demek ki** tek yöntem yazılmalı

**İlk kısım ölçüm, ikinci kısım sıçrama.** Ortak bir iskeletin var olması, onu tek
dosyaya yazma gerekçesi değil — ve ölçüm bunu hiç desteklemedi.

Clara S1'i (*"yöntem tek mi iki mi"*) kendi kapatmıştı, gerekçesi *"iskelet ortak çıktı,
tek yöntem"*. O kapatma da aynı sıçramayı taşıyordu.

### Ölçüm aslında tersini söylüyordu

PCA raporu §3.2: egelisaglik sprint yapısını **hiç kullanmıyor** ve bu bir eksik değil —
*"task bazlı cherry-pick modeli **kalıcı olarak benimsendi**"*. Devralınan bir branch 254
çakışma verdiği için başka bir model seçilmiş.

Yani sahada zaten **üç takım üç yapı** vardı. Rapor bunu yazdı, ikisi de okudu, ikisi de
tartmadı: düzeltilecek bir sapma sanıldı. Mert onu **olgu** olarak kabul etti.

## Ortak olan ne — iskelet duruyor, yeri değişti

Ölçüm değerini kaybetmedi. Dört kaynakta (Clara'nın iki skill'i + goat + osinif) aynı
iskelet çıktı:

```
ANLA  →  SOR  →  DOĞRULA  →  KALICI KAYDA İNDİR
```

**Ama bu bir şablon değil, bir sınama ölçütü.** Bir takımın yöntemi kurulurken *"dört
adım da var mı"* diye bakılır; adımın **biçimi** o takımın işi.

Ölçülmüş iki ayrıntı, biçimin neden takıma bırakıldığını gösteriyor:

- **DOĞRULA sahada** = kaydın söylediği ile kodun gösterdiğini karşılaştırmak (goat'ta 9
  turun 7'sinde yapılmış). Fabrikada bunun karşılığı başka bir şey olur.
- **Son adım "discovery yaz" DEĞİL.** osinif'te 7 işin 4'ü discovery'ye, 3'ü karar
  satırına indi — ayıran şey işin cevabı (*yapılacak* → discovery, *yapılmayacak* → karar
  satırı). "Her iş için discovery" diyen bir kural boş dosya ürettirir.

## Bu kararın doğduğu asıl bulgu

Sprint yöntemi işinin gerekçesi *"tutarlılık"* değil, **tekrar eden keşif maliyeti**
(PCA §3.1, üç kanıt):

- osinif sprint'i 2026-08-09 kapandı (`ec4f448b`), goat 2026-08-10 açıldı (`d6a06a4f`)
- goat, osinif'e **sıfır atıf** veriyor (`grep -i "osinif|önceki sprint|emsal sprint"`)
- buna rağmen **aynı akışı** yazmışlar — ve ikisi de aynı şerhi düşmüş:
  goat *"deneme — kanon değil"* · osinif *"(Deneme akışı — kanona girmedi.)"*

Yani doğru yöntem iki kez bağımsız bulundu, iki kez de bulan ona güvenmedi. Kaybedilen
yalnız keşif zamanı değil — **bulunanın kullanılamaması.**

Bu, karardan sonra da geçerli: her takım kendi yöntemini yazar, ama **yazar** — bir daha
keşfedilmez.

## Ne yapılacak

1. **Fabrika kendi sprint yöntemini yazar** (PAM, Aşama 2 onaylı — kendi repoları).
2. **OY tarafı için yöntem yazılmaz** — çıkan bulgu gereksinim olarak bırakılır.
3. **Clara–Mert döngüsü için Clara yazar** (kendi kanonu).
4. S1 ve S4 düşer — ortak skill olmayınca *"tek mi iki mi"* ve *"hangi repo"* soruları
   konusuz kalır.

## Ek — Fabrika için "sprint" yazılmaz, "iş düzeni" yazılır (Clara, 23:15)

**Karar Clara'nın** — Mert bir süre yoktu, yetki Clara'daydı. Mert döndüğünde
raporlanacak; itiraz ederse geri dönülebilir.

### PAM kendi sınırını Clara'ya geri uyguladı

Clara işi verirken kritik sınır koymuştu: *"olmayan probleme çözüm kurma — bu bugün bir
yerde acıdı mı diye sor."* Yukarıdaki karar *"fabrika kendi sprint yöntemini yazar"*
diyordu; PAM o maddede **durdu ve ölçtü**:

- `grep -ril "sprint" .claude/skills/` → **sıfır sonuç.** Yürürlükteki beş skill'in
  hiçbirinde kavram yok.
- `docs/fabrika/` altında 29 iş klasörü: **21'i** `gereksinim.md` + `status.md` ikilisi,
  **7'si** ölçüm/bulgu klasörü (gereksinim yok çünkü iş değil ölçüm), 1'i yarım.
- 2026-08-11'de **altı iş klasörü aynı gün** açılmış — kapsam önceden çizilip döneme
  yayılan bir küme değil; iş **çıktıkça** açılıyor, çoğu tek oturumda kapanıyor.
- ⚠️ **En keskin kanıt:** `docs/fabrika/gorev-listesi/gereksinim.md:182` — fabrika
  Clara'nın sprint yapısını daha önce **değerlendirmiş ve bilinçli olarak almamış**
  (*"Alınmayan — Clara'ya özgü olan. Sprint'in ClickUp'ta yaşaması (fabrikada ClickUp
  yok)"*).

**Clara ölçümü bağımsız doğruladı:** skill'lerde sıfır (teyit) · 29 klasör, bugün 6'sı
(teyit). Clara'nın geniş taraması `docs/` altında başka klasörlerde *"sprint"* buldu
(`ekosistem-arastirma`, `agent-dogrulama`, `handoff`) — ama onlar araştırma ve geçmiş
kayıt, çalışma düzeni değil. **PAM'in kapsamı doğru olandı.**

### Karar: B — "iş düzeni" olarak yazılır, "sprint" olarak değil

Üç seçenek vardı: **A)** hiç yazılmaz · **B)** var olan düzen "iş düzeni" adıyla
belgelenir · **C)** sprint olarak yazılır, döneme bölünür.

**Neden C değil:** fabrikaya sorulduğunda cevap *"acımadı"* çıktı. C'yi savunmak,
Clara'nın kendi kuralını ilk sınamada bozması olurdu.

**Neden A değil:** fabrikanın bir düzeni **var ve yazılı değil.** 29 klasörün 21'i aynı
ikiliyi taşıyor — bu bir desen ve tutarlı. Kanonda parçaları var
(`ISD-OPEN-REQUIREMENT`, `ISD-KEEP-STATUS`) ama düzenin kendisi — iş nasıl açılır, ölçüm
klasörü işten nasıl ayrılır, ne zaman kapanır — yazılı değil. **Yazılı olmayan düzen, bu
kararın tam konusu:** iki kez bağımsız bulunup iki kez güvenilmeyen şey.

**Neden B:** Mert'in cümlesi *"her takımın sprint yapısı başka"* idi. PAM'in gözlemi —
fabrikanın *"başka"*lığı, döneme bölünmemiş olması olabilir. B bunu inkâr etmeden
belgeliyor; C simetriyi tamamlamak için gerçeği bükerdi.

**Fabrika da egelisaglik gibi muafiyet örneği olarak yazılır** — ve gerekçesi daha güçlü,
çünkü fabrika Clara'nın yapısını görüp almamaya karar vermiş.

### İskeletin yeri burada da aynı

Dört adım fabrikanın düzenine **zorla yerleştirilmez.** Karşılığı var mı diye bakılır;
karşılığı olmayan adım **bulgu** olarak yazılır (*"eksik"* değil, *"fabrikada bu adımın
karşılığı yok/şöyle"*).

### En değerli kalem — henüz hiç yazılmamış

7 klasörde `gereksinim.md` yok **çünkü onlar iş değil ölçüm.** Bu ayrım şu an yalnız
pratikte var, hiçbir yerde yazılı değil.

## Bilinen boşluklar — bu karar kapatmadı

- **Websitesi (WS) kanalına hiç bakılmadı.**
- **Sprint'in işe yarayıp yaramadığı ölçülmedi** (PCA §7: *"yapının varlığını ölçtüm,
  sonucunu değil"*). Kanona bağlanan şey yaygın olan, kanıtlanmış olan değil.
- **ClickUp'ın gerçek durumu ölçülmedi** — yalnız dosyaların ClickUp hakkında yazdıkları.
- **Ara dosyanın değeri ölçülmedi** — bu yüzden "opsiyonel" yazıldı.

## Kaynaklar

- Ölçüm: `skill-project/docs/fabrika/sprint-saha-olcumu/OLCUM-uc-proje-sprint.md` (348 satır, PCA)
- Taslak: `skill-project/docs/fabrika/sprint-yonetimi/yontem-taslagi.md` (PAM)
- Günlük: `gunluk/fabrika/2026-08-11.md`
