# N8N otomasyon takımı — tasarım kararları

**Durum:** yarım (üretim PAD'de, push kapısında duracak)
**Başladı:** 2026-08-08 17:08 · Mert'in gereksinimi
**Not:** Mert bunu bir **test işi** olarak veriyor; ekip bilmiyor, onlar için gerçek üretim.

## Kapsam (Mert, 17:08)

Takım otomasyonu **hem tasarlar hem kurar** — çıktı bir tasarım dokümanı değil,
N8N sunucusunda çalışan otomasyon. Mevcut otomasyonların bakımı ikincil.

Erişim **belirsiz** işaretlendi. Clara ölçtü: iki repoda, ortam değişkenlerinde ve
MCP kaydında N8N'e dair hiçbir teknik iz yok.

## PAM'in ölçümü — tasarımı belirleyen üç mekanik

PAM `docs.n8n.io`'yu **kendi kararıyla** okudu (kaynak verilmemişti):

1. **Bir node gelen her veri öğesi için ayrı çalışır.** Tek öğeyle geçen otomasyon
   üç öğeyle kırılabilir — *"çalıştı"* tek çalıştırmayla kanıtlanamaz.
2. **Elle çalıştırma ile aktivasyon ayrı şey.** Editörde çalışan otomasyon tetik
   altında farklı davranabilir.
3. **Credential workflow'dan ayrı durur.** Otomasyonun mantığı taşınabilir,
   kimliği taşınamaz — "kuruldu" denen otomasyon credential eksikliğinden
   sessizce çalışmıyor olabilir.

### Erişim ucu — daraldı, kapanmadı

Public REST API **var** (dokümanda *"GUI'de yapabildiklerinizin çoğu"*; bir
*"API'yi kapat"* talimatının bulunması varsayılanın açık olduğunu gösteriyor).
Ama **yüzeyi ölçülemedi** — endpoint listesi, kimlik başlığı, credential'ın
API'den yönetilip yönetilemediği. Dört deneme, dördü 404; `docs.n8n.io`
sitemap'inde public API bölümü yok. PAM tahmin etmedi, ölçemediğini söyledi.

**Neden kritik:** API workflow oluşturabiliyorsa takım otomasyonu doğrudan kurar.
Kuramıyorsa üretebileceği en fazla içe aktarılabilir bir tanım olur — yani
*"hem tasarlar hem kurar"* kapsamı **teknik olarak karşılanamaz.**

## Rol sayısı kararı — dört

**PAM'in çıkarımı (emsal ölçümünden):** rol sayısı fazlardan değil **ayrık
malzeme sayısından** çıkıyor.

Faz ekseni iki emsalde de özdeş (planla → üret → statik denetle → dinamik koştur
→ dağıt). 9−7=2 farkın **tamamı** üretici rolünün bölünmesinden: OY'de yığınlar
ayrık (backend/frontend/mobil, kod paylaşımı yok, aralarında `API.md` **sözleşmesi**
var), WS'de üretici tek çünkü devredilecek şey yok.

**Malzeme ayrıksa sözleşme gerekir, sözleşme varsa rol sınırı oradan geçer.**

N8N'de o koşul **yok** — node'lar aynı tuvalde, aynı veri yapısını paylaşıyor,
elle senkronlanan sözleşme dosyası yok. Yani OY'nin üç üretici rolünü doğrulayan
koşul burada mevcut değil.

```
planlayan/gereksinim  otomasyon ihtiyacını gereksinime çevirir
üreten                workflow'u kurar (node, bağlantı, expression)
koşturan/doğrulayan   gerçek veriyle koşturur, veri çokluğunu sınar
denetçi + kapı        kanona uygunluk + aktivasyon kapısı
```

**Koşturanın ayrı kalma gerekçesi mevcut:** veri-çokluğu mekaniği. Üretenin kendi
otomasyonunu tek örnek veriyle doğrulaması *"sahte yeşil"* üretir (emsalin kendi
terimi). **DO/altyapı rolü yok** — sunucu zaten var, kurulacak altyapı yok.

## Üç rol kesişmesi

**(a) üreten ↔ koşturan** — üretenin kendi işini denemesi kaçınılmaz. Sınır
*"kim çalıştırır"* değil, **"kim hüküm verir"**. Emsalde iki farklı çözüm var;
OY'ninki seçildi (kanıt üretende, kapı davranış testi yapmaz). Gerekçe: WS'de
sınır bulanıklaşıyor, yeni bir takımda bulanık sınırı baştan almanın sebebi yok.

**(b) denetçi ↔ koşturan** — koşturanın bulgusu akışı **durdurmaz**, denetçininki
durdurur.

**(c) planlayan ↔ üreten** — **PAM'in kendi bulduğu, emsalde karşılığı yok.**
N8N'de gereksinim ile tasarım birbirine çok yakın: *"her yeni müşteri kaydında
şunu yap"* neredeyse node dizisinin kendisi. Emsalde iş dili ile teknik dil
arasında doğal mesafe var, burada o mesafe küçük. Önlem yazılmazsa planlayan
fiilen tasarım yapar, üreten kopyalayıcı olur. **Gereksinimin en özgün kalemi.**

## Doğrulama eşiği — üç kademe

*"Başarılı çalıştı"* ile *"doğru çalıştı"* ayrı şey:

1. Elle çalıştırma geçti mi (**en zayıf kanıt**)
2. **Çok öğeli** veriyle geçti mi (asıl risk — node her öğe için ayrı koşuyor)
3. **Aktif** hâlde tetikle geçti mi (elle çalıştırma bunu kanıtlamaz)

**Şerh:** bazı hata ayıklama özellikleri (Debug in editor, pinned data) dokümanda
*"n8n Cloud ve kayıtlı Community planları"* için yazılı. Bizim sunucuda geçerli mi
**ölçülmedi** — geçerli değilse doğrulama yöntemi değişir.

## Üç kırılgan yer

1. **Erişim ucu** — takımın ne yapabileceği buna bağlı, diğer her şey bunun
   üstüne kuruluyor.
2. **Credential** — workflow'dan ayrı; "kuruldu" denen otomasyon kimlik eksik
   olduğu için çalışmıyor olabilir ve bu **sessiz arıza**. Ayrıca: agent bir
   credential'ı görmeli mi? Yeni bir risk sınıfı.
3. **Aktivasyon** — geri alınamaz. Push yanlış giderse revert var; aktif
   otomasyon yanlış giderse **yapılmış iş yapılmış olur.**

## Kararlar

**Clara'nın verdiği (Mert'in önceki kararlarından türetildi):**

- **S2 erişim** → "bilinmiyor" (Mert 17:08). Üreten rolün tanımı **iki dallı**
  yazılacak: A) API ile doğrudan kurar, B) içe aktarılabilir tanım üretir.
  Karar gelince dal seçilir, tasarım yeniden yazılmaz.
- **S3 sunucu yönetimi** → takımın işi **değil.** Mert *"n8n'de yapmak
  istediğimiz otomasyonları yönetecek"* dedi — sunucuyu değil.
- **S4 aktivasyon** → **kullanıcı onayıyla.** Bu ekosistemde geri alınamaz her iş
  kullanıcı onayına bağlı (push kapısı, prod müdahale).

**Mert'e giden (17:21 itibariyle açık):**

- **S1 — otomasyon çeşitliliği.** Tek tip mi, çok çeşitli mi? Not: çeşitlilik
  çıksa bile PAM'in ölçütüyle bölünme haksız (sözleşme yok).
- **S5 — agent credential görebilir mi?** Görmezse "kuruldu ama çalışmıyor"
  riski, görürse agent'a kimlik bilgisi yetkisi. **Yeni risk sınıfı.**

İkisi de rol sayısını değiştirmiyor — dört rol iskeleti ikisinden bağımsız yazılabilir.
