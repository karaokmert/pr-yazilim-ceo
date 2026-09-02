# Proje Ekonomisi Aracı — bilinmesi gerekenler

**Ne:** ClickUp üstüne kurulacak plan + maliyet katmanı. Kendi MCP'si olur, ClickUp API
ile konuşur. Kayıt ClickUp'ta kalır — plan ve para bu araçta.

**Durum (2026-09-02):** gereksinim konuşuldu, doküman yazılmadı, task açılmadı.
Ekran denemesi yapıldı ama Mert'in kurgusuyla örtüşmedi — planlama tarafı burada
bırakıldı, task tarafına sonra dönülecek.

---

## Neden doğdu — Mert'in dört şikâyeti

1. **MCP problemi** — ClickUp MCP'si rate limit'e takılıyor, tek tek çağrı yapıyor.
   (Ölçüldü 2026-09-01: iki task 8 saat bloke oldu.)
2. **Uzun akış yapamıyor** — her adım canlı veriye yazıyor, taslak aşaması yok.
3. **Yük planlaması yapamıyor** — bakmak için önce atamak gerekiyor.
4. **Hayali plan yapamıyor** — yazdığı an gerçek oluyor.

⚠️ **1 numara ötekilerden ayrı sınıfta.** O bir araç sınırı; 2-3-4 bir model eksiği:
**ClickUp'ta plan diye bir kavram yok, sadece atanmış iş var.**

---

## Zincir — konuşulan her ihtiyaç bunun bir noktası

Taahhüt (teklifte müşteriye verilen süre)
→ Plan süresi (içeride gerçekten ayrılan; taahhüt 2 hafta olsa da plan 4 gün olabilir)
→ Blok yerleşimi (kişiye ve tarihe bağlanır)
→ Task'a bölme (ClickUp'a basılır)
→ Otomatik sayaç (in-progress'e geçince time track başlar)
→ Maliyet (saat × kişinin o ayki saat maliyeti)
→ Karşılaştırma (plan vs gerçek, gelir vs maliyet)

---

## Hiyerarşi

- **Müşteri** — üst varlık. Altında birden çok proje, sözleşme, aylık fatura, bakım taahhüdü.
- **Proje** — **ölçüm birimi.** Gelir/maliyet/kâr burada toplanıyor.
- **Blok** — **planlama birimi.** Kişiye + tarih aralığına bağlı. YALNIZ bizde yaşıyor,
  ClickUp'ta karşılığı yok.
- **Task** — **yürütme birimi.** ClickUp'ta. Ekip alışkanlığı değişmiyor.

⚠️ Mert'in düzeltmesi: *"Taskler proje bazında ölçülüyor. Blok değil."* Clara blok
bazında ölçüm önermişti, geri aldı.

---

## Kararlaşan şeyler

**Kullanıcı:** proje yöneticileri (*"ben ya da başkası farketmez"*). Tek kişilik tezgâh
değil, paylaşılan kayıt.

**Planlama iki anda yapılıyor:** teklif anında ve sözleşmeden sonra. Üçüncü bir şey var:
**bakım müşterileri** — her ay düzenli yapılması beklenen işler.

**Bakım taahhütleri müşteriden müşteriye değişiyor** — standart paket yok. Bugün dağınık
duruyorlar: *"bazıları sözleşmede bazıları iş dokümanında."*
⚠️ Bu, aracın ilk işinin bir **toplama işi** olacağı anlamına geliyor.

**Bakım işi sprint planına giriyor**, yükü değişken (bazı ay 1 hafta, bazı ay 3 hafta),
iki kaynaktan besleniyor: sözleşmedeki düzenli işler + ay içi gelen istekler.

**Time estimate var, time track yok.** Tahmini Mert kendi deneyiminden yapıyor.
→ Kararlaşan: **sayaç otomatik olacak** — statü in-progress'e geçince başlar, bitince
durur. Kimse elle saat girmiyor.
⚠️ Araç tahmin ÜRETMİYOR, Mert'in tahminini **taşıyor ve topluyor.**

**Maliyet:** kişi başına aylık maliyet → o ayın iş gününe bölünüp saat maliyeti çıkıyor
(Buse 100k → ~650 ₺/saat). Aya göre değişken.

**Bloklar peş peşe DEĞİL.** Aralarında müşteri onayı / karar boşlukları var.
Örnek: Buse Eylül 1-15 tasarım → backend Ekim 10-25. Aradaki 25 gün prototip onayı.
⚠️ **Sonucu:** gecikme otomatik kaymamalı. Buse 3 gün sarksa bile backend Ekim 10'da
başlar — onu tutan Buse değil, müşterinin onayı. Zincir varsayan araç yanlış alarm verir.

**Boşluk sebebi kayıt altına ALINMIYOR.** Mert: *"o boşluklara iş almak için plan
yapacağım zaten."* Boşluk bir doldurma fırsatı, takip kalemi değil.

**Sapma görünür olmalı** — *"kayıp görmeliyim."* Plan dondurulur, gerçekleşen üstüne
çizilir; araç planı kendiliğinden güncellemez.

**Müşteri bir varlık** — altında ayrı ayrı projeler.

---

## Aracın cevaplaması beklenen sorular

- Bu işi alabilir miyim, ne zaman başlarım? (müsaitlik penceresi)
- Plan tuttu mu, nerede kaydık?
- Proje kâr mı zarar mı? (300k'ya verdik, ne harcadık)
- Bu bakım müşterisi bizi yiyor mu? (ayda 50k kesiyoruz, bu ay ne kadar emek gitti)
- Kişinin ayının ne kadarı faturalanabilir işe gitti? (doluluk)
- Bu ay ne söz verdik, yaptık mı? (bakım taahhüt kontrolü)

---

## Açık kararlar

**Ekip araca giriyor mu?** Mert: *"bu kararı henüz vermedim."* Buse kendi planını görecek
mi, yoksa ona yalnız ClickUp task'ları mı gidecek?
⚠️ Karar ertelenebilir ama **kullanıcı ve rol kavramı en baştan modelde olmalı** —
sonradan izin açmak yeniden yazma demek.

**Sayaç geçen zamanı mı çalışılan zamanı mı ölçüyor?** Pazartesi açılıp Cuma kapanan
task'ta sayaç 96 saat der, gerçekte 20 saat olabilir. İki task aynı anda açıksa ikisi
birden sayar. Mesai saatiyle sınırlansın mı?

**Task olmayan zaman nereye yazılıyor?** Toplantı, inceleme, araştırma task değil —
sayaç saymaz. İlk doluluk tablosu *"herkes ayının yarısını boşa harcıyor"* diyecek ve
bu doğru olmayacak. İç işler task'lansın mı, yoksa "ölçülmeyen zaman" ayrı kategori mi?

**Blok bazında sapma ölçülemiyor.** Ölçüm proje bazında olduğu için *"Buse'ye 2 hafta
ayırdık, gerçekte ne sürdü"* sorusunun cevabı yok. Katlanılabilir mi, yoksa task'lar
bloğa etiketlensin mi?

**Otomatik sayaç ClickUp'ta nasıl tetiklenecek?** ClickUp'ın kendi otomasyonu statü
değişiminde time track başlatabiliyor mu, yoksa bizim MCP'nin mi tetiklemesi gerekiyor
— **ölçülmedi.**

---

## Ürünleşme

Mert: *"ClickUp'u kullanırsak ürün haline getiremeyiz."*
Clara'nın itirazı (kabul edilmedi/edildi belirsiz, konu kapanmadı): ClickUp'ı kullanmak
ürünleşmeyi kapatmıyor, **ClickUp'a bağımlı olmak** kapatıyor. Plan katmanı kendi veri
modelinde yaşıyorsa ClickUp bir çıkış hedefi olur, yarın Jira ikinci çıkış olur.
Model ClickUp'ın hiyerarşisini kendi modeli sanıyorsa eklenti olur, tek başına satılamaz.

---

## Clara'nın eklediği, Mert'in onaylamadığı iki şey

Bunlar gereksinimden çıkarıldı, Mert doğrulamadı — bir sonraki turda sorulmalı:

1. **Bakım yükünün geçmiş ortalaması tutulmalı** — plan yaparken kişinin üstüne pay
   konur, yoksa her plan iyimser çıkar.
2. **Boşluğa konan işin taşma kontrolü** — boşluk doldurmak yeni çakışma üretebilir.

---

## Üretilenler (2026-09-02)

- Gereksinim resmi: https://claude.ai/code/artifact/cc473801-9459-4f78-839a-90a92ca9deb8
- Ekran denemesi: https://claude.ai/code/artifact/76e598c3-d538-47d4-9966-e5d2804657e0

⚠️ **Ekran denemesi Mert'in kurgusuyla örtüşmedi.** Clara ekranları SORULARDAN kurdu
(kim boş, kâr mı zarar mı); Mert VARLIKLARDAN bekliyordu:
**Müşteriler · Projeler · Taskler · Plan · Maliyet.**
Mert'in kurgusu doğru — bir yönetim programı varlık üzerinden gezilir, rapor üzerinden
değil. Clara'nın ekranları o varlıkların İÇİNDEKİ görünümler.
Yeniden çizilecekse varlık menüsünden başlanır.
