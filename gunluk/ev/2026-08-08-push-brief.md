# Push brief — 2026-08-08, 13:26

**Ölçüm o an yapıldı** (PQA'nın uyarısı gereği — bugün bu sayı beş kez değişti):

```
bekleyen commit : 27
origin/main     : cab8500
HEAD            : 89d131f
çalışma ağacı   : TEMİZ (git diff HEAD boş)
toplam          : 40 dosya, 7.910 ekleme, 336 silme
```

---

## ŞU AN NE OLUYOR

Fabrikanın kanonu iki gündür elden geçiyor ve **hiçbiri yayınlanmadı.** Yerelde
27 commit birikti; sahadaki hiçbir agent bunların hiçbirini görmüyor.

İçinde on dörtten fazla ayrı iş var — kural düzeltmeleri, rol sınırı netleştirmeleri,
kanal düzeni, ölçüm kayıtları, index senkronları. Hepsi denetimden geçti.

**Yayınlanmazsa ne olur:** bugün düzeltilen `is-duzeni` description'ı sahaya inmez —
yani `ISD-OPEN-YOUR-BOX` kuralı yazılı olur ama agent onu **hiç açmaz**, çünkü
tetiklenmiyor. Ölçüldü: düzeltmeden önce test "hiçbiri" dedi.

---

## NASIL ÇÖZÜYORUM

```
Mert onaylar
  → ben PQA'ya push işini iletirim (onayın KAPSAMI yazılı olarak)
  → PQA kendi denetim onayını + Mert'in yayın onayını doğrular
  → push atar
  → origin/main = 89d131f olur, sahaya iner
```

Push'u ben atmıyorum, PAD de atmıyor. Kapıyı PQA açıyor ve yalnız iki onay
birlikteyken: kendi denetim onayı (verildi) + senin yayın onayın (bekliyor).

---

## NEREYE DOKUNUYOR

**Kanon dosyaları (`.claude/`)** — beş skill + dört agent body + `rules-index.json`.
Bugün değişenler: `behavior` ve `is-duzeni` description'ları (tetiklenme düzeltmesi),
`yapi-taslari`'na bir şerh paragrafı, index'e sekiz yeni atıf.

**Süreç dokümanları (`docs/`)** — 21 iş klasörü, ölçüm kayıtları, gereksinimler,
üç devralınan ölçüm dosyası (bugün yayına alındı).

**Kural sayısı: 131 — DEĞİŞMEDİ.** Bugün yeni kimlik üretilmedi, yalnız mevcut
kurallar düzeltildi ve atıflar işlendi.

**Sahadaki takımlar: DOKUNULMADI.** `team/` altı boş, hiçbir müşteri projesi
etkilenmiyor.

**Plugin sürümü: ARTIRILMADI.** Bu repo plugin değil; sürüm bump'ı yalnız takım
paketlenirken gerekir (`DAG-BUMP-BY-AUDITOR`).

---

**NEYE DOKUNMUYORUM:** müşteri projeleri · `team/` altı · başka repolar ·
izin ayarları · plugin sürümü · kural sayısı (131 sabit)

**EN ÖNEMLİ SINIR:** push kapsamı **on dörtten fazla ayrı iş.** Tek işin onayı
diye sunulursa hepsi tek onayla geçer. Bu yüzden onayın kapsamı yazılı olmalı —
PQA push işi kendisine geldiğinde bunu arayacak ve kapsamsız gelirse
push etmeyip soracak (`PQA-GATE-BEFORE-PUSH`).

**AÇIK KARAR:** var — aşağıda. **SÜRE:** push birkaç saniye; karar sende.

---

## Onaydan ÖNCE bilmen gereken iki şey

**1. Yedi karar kalemi açık ve hiçbiri push'u bloke etmiyor.**
`incelemeler/2026-08-08-fabrika-kanon-sorgulama/karar-kalemleri.md` altında.
En önemlisi: index ile kaynak arasında tetik yok — bugün **beş** ayrı arıza
üretti. Bunlar push'tan sonra ayrı işler olarak açılabilir.

**2. Bir şey ölçülmedi ve bunu ayırmam gerekiyor.**
Kanonun **içeriği** ölçüldü (16/16 davranış testi) ve **tetiklenmesi** ölçüldü
(madde 8). Ama sahadaki agent'ın kanonu gerçekten **yüklediği** ölçülmedi —
skill gövdeleri `skills:` alanıyla gelmiyor (bilinen hata) ve açılış hook'u
alt-agent'ta hiç çalışmıyor.

Yani push iyi yazılmış bir kanonu yayınlıyor; o kanonun agent'ın eline geçtiği
**ayrı bir sorun ve hâlâ açık.**
