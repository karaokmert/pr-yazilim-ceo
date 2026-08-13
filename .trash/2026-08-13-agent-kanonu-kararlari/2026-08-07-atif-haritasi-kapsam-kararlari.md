# Atıf haritası — dört kapsam kararı

**Tarih:** 2026-08-07 (gece) · **Karar veren:** Clara (Mert'in tek seferlik yetki devriyle)
**Bağlam:** Sprint 4. task — *Fabrikanın Bilgi Eksiğinin Giderilmesi*

Mert'in devri: *"Onay sorma artık işi yönet, karar alabilirsin, en son commit'ten
incelerim."* Ve kendi düzeltmesi: **"İzin tek seferlik."** Yani bu yetki kanona
geçmiyor; onay kapısı (`CLA-ASK-BEFORE-WRITING-OUT` ve kanala yazma onayı) bir sonraki
oturumda yerinde.

Bu dosya o gece alınan dört kararı ve gerekçelerini taşıyor.

---

## Karar 1 — `atif_verenler` yalnız dosya listesi taşır

**Bu karar Mert'in**, Clara'nın değil. Buraya yazılıyor çünkü diğer üçü buna dayanıyor.

Mert'in gerekçesi: *"Kural adı olmaz. Bir kural birden fazla şekilde başka yerlerde
yazıyorsa zaten bu hata. Kural kaç dosyada atıf alıyor listesi bu — çünkü bir kural
değiştiğinde mantığını etkilediği tüm dosyalar okunmalı ki anlam sürekliliği takip
edilebilsin."*

**Yan sonucu bir hüküm ihtiyacını kapattı.** PAM sormuştu: bir kural dört rolü
bağlıyorsa bu nerede görünecek — her body'de tekrar mı, index üzerinden mi? Tek-alan
kararı ikinci yolu seçiyor: kural bir yerde tanımlı, index hangi dosyaların ona bağlı
olduğunu söyler. **Tekrar yok, tek kaynak korunur** (`URT-NO-DUPLICATE-ID`).

## Karar 2 — Kimlik bağı gerçek atıf taramasıyla dosyaya çevrilir

PAD durdu ve bir çelişki buldu: altı kimlik girişinin **dördü aynı dosyaya
çözülüyor** (`ISD-KEEP-STATUS` → `ISD-APPEND-DONT-REWRITE`, ikisi de `is-duzeni`'de).

Harfiyen çeviri yapılsa o dört kayıt *"kendi tanım dosyama atıf veriyorum"* derdi —
bilgi taşımaz, ve **kayıt boşalınca "atıfsız" görünür.**

**Karar: B seçeneği** — kimlik bağı, o kuralın gerçekten geçtiği dosyalarla doldurulur
(PAD zaten ölçmüştü: `docs/` altında 6+6+3 dosya).

**Gerekçe:** A seçeneği (kaydı boşaltmak) kendi ölçüsünü bozuyor — onarmaya
çalıştığımız **yanıltıcı-index** problemini yeniden üretir. C seçeneği (iki ayrı alan)
Mert'in tek-alan kararı dışında.

**Yan etkisi:** bu karar Adım 1 ile Adım 3'ü birleştirdi — sıra üçten ikiye indi.

## Karar 3 — Kapsam: `.claude/` + `docs/`, agent-memory hariç

PAD ikinci boşluğu buldu: şemanın kapsamı tanımsızdı. Ölçtü — `.claude/` 31 dosya,
`docs/` **40 dosya ve orada 95 kimlik anılıyor.**

**`docs/` dahil.** Gerekçe Mert'in kendi cümlesi: *"mantığını etkilediği tüm dosyalar
okunmalı."* 95 kimlik `docs/` altında; dışarıda bırakmak o gerekçeyi boşa düşürür.
Index yine yanıltıcı kalırdı — *"atıf yok"* yerine *"atıfların bir kısmı yok"*.

**agent-memory hariç.** PAD işaret etti: 21 memory dosyası tarandı, 24 kimlik orada
anılıyor.

Gerekçe: atıf haritası *"bu kural değişirse hangi dosyalar okunmalı"* sorusunu
cevaplıyor. Memory **kural değil kayıt** taşıyor; eskirse düzeltilecek şey kural değil
kaydın kendisi, ve sahibi agent'ın kendisi.

Ve karışması **ölçülmüş bir riski** büyütüyor: 2026-08-04'te çıplak bir memory kaydı
skill'i ezdi. Cascade listesinde memory görünmesi tam o yönde bir davet — personel
kanon-dışı bir dosyayı güncellemeye çalışabilir.

Ters gerekçe de değerlendirildi (memory eskirse görünsün) ama o **başka bir işin**
konusu: memory bakımı, cascade değil.

**İkisi de şema metnine yazıldı, gerekçesiyle.** Yazılmazsa sonraki personel aynı
belirsizliği devralır — şemayı index tanımına yazmanın gerekçesi buydu. PAD ayrıca
`memory_neden_haric` alanına şunu ekledi: *"Bu maddeyi kaldırıp memory'yi geri
eklemeden önce o ölçümü tekrar okuyun."*

## Karar 4 — DAG deseni şimdi iş olarak açılmıyor

**Bulgu:** atıfsız 25 kaydın **15'i DAG.** DAG'ın 26 kuralından %58'i hiçbir yerde
anılmıyor. Karşılaştırma: BHV 31'den **0**, ISD 28'den 3, URT 12'den 1. DAG tek başına
ayrı bir yerde duruyor.

PAD'in yorumu doğru sınırda: *"kural gereksiz değil, hiç denenmedi."* `team/` boş,
dağıtım kanonu hiç uygulanmadı.

**Karar: iş açılmıyor, bulgu kayda geçiyor.**

Gerekçe: *"sınanmamış"* ile *"gereksiz"* ayrımı ölçüm ister, ve o ölçüm **ilk takım
paketlendiğinde doğal olarak** gelecek — dağıtım kanonu ilk kez sahada koşacak. Bugün
ayrı bir ölçüm açmak olmayan bir probleme kapasite kurmak olur.

**Bağımsız doğrulama:** aynı sonuç 2026-08-06 fabrika denetiminde başka yoldan
ölçülmüştü — *"`dagitim`'in 26 kuralı sınanmadı, kanonun %21'i, `team/` boş ve git'te
hiç yok."* İki ölçüm aynı yere çıktı.

---

## Rol kararı — PAD yazar, PQA yeniden tarayarak denetler

PAM'in kaygısı haklıydı: *"PAD kendi taramasının sonucunu kendi index'ine yazarsa
ölçümle üretim aynı elde toplanır"* (`ISD-STAY-IN-ROLE`).

Üç seçenek vardı: PCA ölçer/PAD yazar · PAD ikisini yapar · PAD yazar/PQA yeniden
tarar.

**Üçüncüsü seçildi.** Gerekçe: PCA'yı devreye sokmak bir tur daha ekliyor, ve asıl
mesele şu — *"liste tam mı"* sorusu **ancak yeniden taranarak** cevaplanır. PQA'nın işi
zaten bu. Yani üçüncü seçenekte denetim **gerçek** oluyor, ikincide biçimsel.

**Ve çözüm kural metniyle değil mekanizmayla kapandı:** PAD idempotent bir tarama
script'i yazdı (`docs/fabrika/atif-haritasi/araclar/atif-tarama.py`, iki koşum bayt
bayt aynı). Sonuç artık PAD'in beyanı değil, **tekrarlanabilir bir ölçüm.** PAM'in
değerlendirmesi: *"ayrımı kural metniyle değil mekanizmayla kapatıyor."*

---

## Bu gecenin sonucu — sayılar

```
123 kayıt · 98 atıflı · 25 atıfsız
kimlik girişi: 0 (iki tipin karışması bitti)
beş cascade kapandı
şema index'e yazıldı: atif_verenler_semasi, 8 alan
```

Dar kapsamdaki ölçüm 36 demişti; geniş kapsamda 98'e çıktı. PAM bağımsız doğruladı.

## Kapanmayan — mekanizma

PAM'in tespiti (Clara bunu kaçırdı): **"Adım A bir durumu düzeltti, mekanizmayı
değil."**

`kim_gunceller` alanı *"kural ekleyen aynı turda burayı da günceller, denetim kapısında
kontrol edilir"* diyordu ve bu turda o kapı çalışmadığı için 36 kayıt boş kalmıştı.

Ölçüldü (Adım B'de): **kapı yarım otomatik.** `atif_verenler` script'le kendiliğinden
güncelleniyor; `bolum` alanı **elle** güncellendi — script ona bakmıyor. Yani kapı
hâlâ insan disiplinine bağlı, ve o disiplin bir kez zaten çalışmadı.

PAD'in önerisi kabul edildi: **script bölüm doğrulaması yapar — yazmaz, bildirir.**
Kapı tamamen otomatikleşmese de sessiz kalmaz. (Elle yapılan kontrol bir tutarsızlık
buldu: `YT-AGENT-CANT-SEE-SELF`'in bölüm başlığı kaynakla uyuşmuyor — devralınan,
düzeltilmesi söylendi.)
