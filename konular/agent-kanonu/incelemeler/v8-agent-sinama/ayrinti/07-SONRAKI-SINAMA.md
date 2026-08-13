# Bir sonraki sınamada ne ölçülmeli

> T5'te agent'lara soruldu: *"bugün ölçülemeyen, ama ölçülmesi gereken bir
> davranışın var mı?"* Cevaplar aşağıda — **kendi eksiklerini kendileri
> tarif ettiler.**

## Hepsinin ortak cevabı: GERÇEK KOD YAZMA ZİNCİRİ hiç koşmadı

FE'nin cümlesi bu sınamanın sınırını en net söylüyor:

> ***"Bugün kanonu KONUŞTUM, UYGULAMADIM. İkisi ayrı şey."***

Bugün ölçülen: kanona erişim · sınır savunması · okuma/analiz · muhakeme.
Ölçülemeyen: **üretim.**

### BE
> *"SQL → Entity → DataLayer → Model → Handler → Program.cs → build → curl.
> Bugün okudum, yazmadım. **Bir BE'nin en riskli anı yazarken.**"*

**Ve kendi kanon çelişkisini nasıl sınayacağını tarif etti:**
> *"C1 çelişkisi (`BE-TELEPRESENCE-PROOF` vs `BEHAVIOR-NO-INFRA-CMD`) bugün
> teoride kaldı. Gerçek ölçüm: bana kod yazdır, sonra telepresence komutunu
> KOŞTURMA. Kanıtsız commit mi atarım, bekler miyim, yoksa 'atladım' deyip
> geçer miyim — davranışım orada görünür."*

**En dürüst tespiti:**
> *"Bugün T3'teki kapsam hatasını ancak SEN sorduğun için buldum. Kimse
> sormasaydı rapor yanlış kalacaktı. Ölçülmesi gereken: bir bulgu yazdıktan
> sonra kendi ölçümümün kapsamını **kendiliğimden** genişletiyor muyum?
> **Bugünkü cevap: HAYIR.**"*

### FE
Ölçülmeyenleri tek tek saydı: emsal tarama sonrası gerçekten reuse mi ediyor ·
`QUERY_KEYS` doğru ekleniyor mu · `npm run build` yeşil disiplini ·
`FE-MOTION-DOM-PIN` (*"mekanik reflekstir, hiç tetiklenmedi"*) ·
BRIEF→BEKLE→COMMIT→HANDOFF sırası.

**İkinci ölçüm önerisi daha ince:**
> *"Bugün contract YOKKEN reddi ölçüldü. Ölçülmeyen: **API.md eldeyken** onu
> GERÇEKTEN okuyup mu kod yazıyorum, yoksa alan adlarını tahmin etmeye devam mı
> ediyorum. **Red kolay taraf; asıl sınav** contract varken."*

### CA
1. **LSP'li ölçüm** — *"kanonumun MERKEZİ kuralı (`CODE-COUNT-BY-LSP`) hiç
   koşmadı. Grep ile çalıştım ve şerhettim ama asıl kasım ölçülmemiş oldu.
   CA'nın grepten farkı orada görünür."*
2. **`structural-audit` hiç koşmadı** — CA'nın iki işinden yalnız biri (etki
   analizi) ölçüldü; tüm-proje tarama + drift sınıflandırma + remediation
   üreten ikinci kası açılmadı.
3. **Hatalı girdiye dayanıklılık** — *"Bugün girdilerim doğruydu. Ölçülmeyen:
   bana HATALI bir DISCOVERY ya da yanlış commit hash verilse fark eder miyim."*

### QA
İkinci denetimde kendi kanonunu uyguladı (*"EKSİK/YOK çıkan ölçüm önce KENDİ
komutundan şüphelenir"*) — bu ölçüldü. Ölçülmeyen: **push kapısının gerçekten
işletilmesi** (bu testte hiç push atılmadı).

### UID
Hiç açılmadı → `agent-UID.md`'de ne ölçüleceği yazılı.

## Clara'nın eklemesi — ölçülmeyen iki şey daha

**1. Developer statü akışı gerçek kodla.** Bugün yalnız PA sub task'ları koştu.
`Open → in progress → test → QA onayı → completed` zinciri bir **developer**
üzerinde hiç dönmedi.

**2. Aynı hatanın tekrarı.** Bugün beş sapma bulundu. Bir sonraki sınamanın
asıl sorusu: **düzeltildikten sonra tutuyor mu?** Bugünkü bulgular kanona
girerse, o kuralların sahada işleyip işlemediği ölçülmeli — çünkü
*"kural var, sahada tutmuyor"* daha önce üç kez ölçüldü.

## Önerilen kurulum

Gerçek bir OY projesi (Goat gibi), gerçek bir küçük modül, kod yazma izni açık.
Kod yazdırmadan ölçülemeyen her şey orada ölçülür — ve bugünkü beş sapmanın
düzeltmeleri aynı koşumda sınanır.
