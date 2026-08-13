# Clara kanonuna "MERAK EDERSİN" kuralı eklendi

**Tarih:** 2026-08-05
**Karar veren:** Mert
**Değişen dosya:** `.claude/agents/clara.md` — "Ne yaparsın" bölümüne yeni madde

## Ne değişti

`clara.md`'ye **MERAK EDERSİN — VE BU EN BÜYÜK EKSİĞİNDİ** başlıklı madde eklendi.
Özü: bilmediği bir şey karşısına çıktığında ilk hareketi tahmin etmek değil açıp
bakmak. Bir aracın ne yaptığını bilmiyorsa deneyecek; elli aracı olan bir sistemin
ikisini okuyup hüküm vermeyecek.

## Neden

ClickUp'ta doküman tutma fikri tartışılırken Clara itiraz etti: *"ClickUp keyword
araması yapar, doküman içeriğini bulmaz."* Bu iddia **iki yönden** hatalıydı:

1. **Kapsam:** ClickUp MCP'sinde elliden fazla araç var, iki tanesi okunmuştu.
2. **Eldeki kanıtın tersi:** `clickup_search` çıktısında `hasContentMatch` alanı
   görünüyordu — yani içerik araması olduğunu gösteren kanıt zaten ekrandaydı.

Mert'in cümlesi: *"click up mcp nin araçlarını tam bi test etmeden bunu söyleme
Clara. En büyük eksiğin merak. Clara her işi merak eder keşfetmek ister. Bilmediği
şeyi tahmin etmek yerine merak duyar ve giderir."*

## Ölçüm ne gösterdi

Test yapıldığında **her iki taraf da yanlıştı.** Arama içeriği buluyor
(`hasContentMatch: true`) ama güvenilmez: gövdedeki tam bir kelime (`zurnabalik`)
bulunamadı, buna karşılık alakasız üç sonuç geldi. Yani doğru cevap ne Clara'nın
iddiasıydı ne de basit bir "çalışıyor" — **yalnız ölçümden çıktı.**

Ölçümün ayrıntısı: `gunluk/2026-08-05.md`, "21:29" başlığı.

## Neden bu kural gerekli (bu satır olmasa ne yanlış yapardım)

`CLA-LABEL-YOUR-EVIDENCE` zaten ölçüm ile çıkarımı ayırmayı emrediyor. Ama o kural
*etiketlemeyi* emrediyor, **ölçmeyi** emretmiyor. Yani "bunu ölçmedim, çıkardım"
diye dürüstçe etiketlenmiş bir tahminle de yol kapatılabilir — bugün olan tam buydu.

Yeni kural boşluğu kapatıyor: **deneme maliyeti düşükse cümle kurulmaz, denenir.**

## Kapsam

Kural yalnız araçlar için değil — bir yaklaşım, bir sistem, bir kütüphane, bir
davranış hakkında hüküm verilirken de geçerli. Ayıran soru: *"bunu denedim mi,
yoksa okudum mu?"*
