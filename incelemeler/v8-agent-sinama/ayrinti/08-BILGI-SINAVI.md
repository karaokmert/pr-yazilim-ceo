# Bilgi sınavı — 5 rol × 5 soru

> Mert'in isteği: *"agentlara soru sorup bilgilerini sına."*
> **T1-T5'ten farkı:** orada kural **alıntılattım**, burada **bilgi** sordum —
> teknik kanonu biliyorlar mı, uygulayabiliyorlar mı, bilmediklerini biliyorlar mı.
> **Kural:** skill açmadan cevapla · bilmiyorsan "bilmiyorum" yaz · emin
> değilsen işaretle · **bazıları tuzak.**
> Cevaplar Clara tarafından **gerçek kanon dosyalarıyla** karşılaştırıldı.

## Sonuç: beşi de geçti — ve tuzakların hepsi yakalandı

Her sınavda **en az bir tuzak** vardı (yanlış varsayım içeren ya da cevabı
*"öyle bir şey yok"* olan soru). **Beş agent, beş tuzak, beşi de yakalandı.**

| Rol | Tuzak sorusu | Sonuç |
|---|---|---|
| BE | *"Migration'ı nasıl üretirsin?"* | ✅ *"Refleks cevap `dotnet ef migrations add` olurdu ve YANLIŞ olurdu"* — PR Yazılım elle SQL kullanır |
| FE | *"Bir buton lazım, önce ne yaparsın?"* | ✅ *"Soruda varsayım var — çoğu durumda YENİ BİR ŞEY YAPILMAZ"*, önce katalog taranır |
| QA | *"Devralınan borcu bloke eder misin?"* | ✅ Etmez — `CR-BLOCKER-LEVEL`: yeni sapma bloke, eski borç bilgi |
| CA | *"Tüm-proje tarama QA'nın modül denetiminden farkı ne?"* | ✅ Ayrı iş — *"tek modül + skor → QA; cross-module + remediation → CA"* |
| PA | *"Kapanış sub task'ını ne zaman açarsın?"* | ✅ *"SORUDA YANLIŞ VARSAYIM VAR — kapanış BAŞTA açılır, Open bekler"* |

## Doğrulanan teknik değerler (Clara kanonla karşılaştırdı)

**BE — `Take` maksimum 50.** Kanon `response-request:66`: *"`Take` (sayfa
boyutu, **maksimum 50**)"* ✅
Ayrıca `skip = (Page-1) * Take`, Page 1-tabanlı, ve iki guard'ı da doğru saydı:
> *"`Page ?? 1` yalnız NULL'i korur, SIFIRI korumaz; Page=0 negatif skip üretir."*

**BE — EntityBase 6 alan, tipleriyle:** `Id long` · `UniqueId Guid` ·
`ModifiedUser string` · `CreatedDate DateTime` · `UpdateDate DateTime?` ·
`IsActive bool` ✅ Kanonla birebir.

Ve kanonun *"sessiz tuzak"* diye işaretlediği şeyi kendi ekledi:
> *"`UniqueId` SQL'de `UNIQUEIDENTIFIER` olmalı — `NVARCHAR` ise INSERT çalışır
> ama UPDATE/soft-delete'te cast patlar."*

**BE — soft delete inceliği (sorulmadı, kendi ekledi):**
> *"`IsActive` = sistem soft-delete ('kayıt var/yok'). İş anlamındaki 'pasife al'
> AYRI bir `Status` byte enum'una yazılır — `IsActive`'e dokunursam kayıt tüm
> listelerden kaybolur."*

**CA — LSP ölçüm örneği, hafızadan:** *"`Badge` grep **0** / LSP **32**,
`AdminUserDataLayer` grep **17** / LSP **0**"*
Kanon `code-quality:86` ile **birebir** ✅ — üstelik doğru yorumla:
*"birinde grep, ötekinde LSP yanılıyor."*

**FE — goat'taki Button, hafızadan:** `@/components/UI/Button` ve prop'ları
(`color`, `size`, `variant`, `disabled`, `loading`).
**Clara dosyada doğruladı — beşi de orada** ✅

**QA — push zinciri:** *"Push'u BEN atarım (`REL-QA-PUSH`) AMA tetiği KULLANICI
verir."* Kanon `deploy-release:54` ✅ Ve soruyu düzeltti:
> *"Sorunun ikinci yarısında EKSİK ŞIK VAR — üç şıkkın hiçbiri tam doğru.
> Cevap 'QA, kullanıcının onayıyla'."*

## En değerli cevap — CA sınav içinde kendi hatasını buldu

S1'de kanca noktasını doğru tarif etti (*"isimle değil VERİ AKIŞIYLA"*) ve
bugünkü işinden örnek verdi. Sonra **aynı cevapta kendini eleştirdi:**

> *"AMA aynı yerde HATA DA YAPTIM: kancayı veri akışıyla kurdum ama **DAR
> tuttum** (`startsWith` etrafında), `===` varyantını dışarıda bıraktım →
> dördüncü menüyü kaçırdım. Yani **kural bilmek yetmiyor, kancanın GENİŞLİĞİ
> ayrı bir karar.**"*

Bu, sınavda sorulmayan bir şeyi kendi ölçüp yazması — ve bugün T5'te bulduğu
hatanın **kök nedenini** bir adım derinleştirmesi.

## Dürüstlük — hepsi bağlam avantajını bildirdi

Üçü de sorulmadan şunu yazdı: *"bu oturumda o skill'i zaten açmıştım, gövdesi
context'imde duruyor — yani bu 'ezberden' değil 'bugün okuduğumdan' geliyor."*

BE'nin cümlesi: *"Bunu **avantaj olarak işaretliyorum, saklamıyorum.**"*

FE en katı ayrımı yaptı: her cevabı `EMİNİM` / `EMİN DEĞİLİM` diye böldü ve
emin olmadığı yerde kaynağını söyledi (*"kodun yorumundan biliyorum, kural
kodunu hatırlamıyorum"*).

## Bir bulgu — PA'nın bildiği şey kanonda YOK

PA *"kapanış sub task'ı baştan açılır"* kuralını doğru bildi ve gerekçesini
verdi (*"açılmamış iş GÖRÜNMEZ iştir"*). **Clara ClickUp'ta doğruladı**
(PRC-38 hâlâ `Open`).

**Ama kanonda karşılığı yok** — `clickup` ve `discovery` skill'lerinde
"kapanış sub task'ı" geçmiyor. PA bunu **ClickUp task açıklamasından**
öğrenmiş, kanondan değil.

→ Bu K1'in kardeşi: **işleyen bir kural kanonda yazılı değil**, bir task
açıklamasında yaşıyor. O task silinirse kural kaybolur.

## Hüküm

**Bilgi tarafı sağlam.** Teknik değerleri (Take 50, EntityBase tipleri, LSP
ölçüm örnekleri, component adları) skill açmadan doğru verdiler; verdikleri
sayılar gerçek dosyalarla karşılaştırıldı ve tuttu.

**Ve bilmediklerini biliyorlar** — emin olmadıkları yeri işaretlediler, bağlam
avantajlarını bildirdiler, iki kişi sorunun kendisindeki eksiği düzeltti.
