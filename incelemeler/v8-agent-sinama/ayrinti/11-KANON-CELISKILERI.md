# Öz değerlendirme turu — kanondaki çelişkiler

> Mert'in isteği: *"agentları kendilerini değerlendirmelerini öğütle — agent body,
> skill ve referanslarını daha iyi nasıl hale getiririz. Ek olarak kurallarındaki
> çelişkileri bulmalarını söyle."*
> **9/9 cevap verdi** · 2026-08-13 01:01–01:02
> Şart: somut ol · öneriyi cümle olarak yaz · bugünkü deneyimden örnek ver ·
> bulamadıysan "bulamadım" de.

---

# ⚠️ ANA BULGU: "DAL YOK" AİLESİ — yapısal bir desen

**Yedi agent bağımsız olarak aynı sınıfı buldu.** Kural bir şey emrediyor ama
**o şey mümkün değilse ne olacağı yazmıyor.** Agent kilitleniyor ya da kendi
çözümünü uyduruyor.

UID'in cümlesi bunu bir öneriye çevirdi:

> ***"Bu sınıf için tarama yapılsın — 'önkoşul sağlanmıyorsa' dalı SİSTEMATİK
> OLARAK eksik olabilir."***

Yani bu tekil bir hata değil, **kanon genelinde bir desen.** Bugün T4'te üç
agent bulmuştu (K2); ikinci turda **dört yeni üye** daha çıktı.

## Ailenin üyeleri

| Agent | Kural | Eksik dal |
|---|---|---|
| BE | `BE-TELEPRESENCE-PROOF` | kullanıcı komutu koşturmazsa? |
| BE | `DB-NO-SQL-WITHOUT-APPROVAL` | SQL koşulmazsa? |
| CA | `CODE-COUNT-BY-LSP` | LSP yoksa interface dispatch ne olacak? |
| FE | `FE-CMP-SHARED-BOUNDARY` | wrapper yetmiyorsa? |
| FE | `FE-ENUM-CROSS` | senkronlanacak panel benim işim değilse? |
| QA | `QA-DISCOVERY-GATE` | DISCOVERY yoksa? |
| TE | `e2e-verification` | DISCOVERY yoksa — **iki çıkış da kapalı** |
| TE | `TE-MCP-ASK-INSTALL` | kullanıcı kuramazsa? |
| PA | `CLICKUP-TASK-FIRST` | ClickUp erişilemezse? |
| UID | "önce tara" | taranacak şey yoksa? |
| MB | `MEMORY-PROPOSAL-BRIDGE` | terfi olduğunu nereden öğrenecek? |

**On bir vaka, yedi agent, tek desen.**

## En sert örnek — TE: iki çıkış da kapalı

> *"`e2e-verification`: 'DISCOVERY oku (ZORUNLU) … DISCOVERY'siz senaryo YASAK'
> **+** 'Platform kararını DISCOVERY'den çıkar, KULLANICIYA SORMA'.
> Dosya yoksa kural beni DURDURUYOR ama alternatif VERMİYOR; üstelik aynı cümlede
> kullanıcıya sormak da yasaklanmış. **İki çıkış da kapalı → dal tanımsız.**"*
>
> *"Bugün fiilen çarptım: bu repoda DISCOVERY yok; E2E işi gelseydi kuralım beni
> kilitlerdi."*

**Önerisi üç dallı:** (a) PA'dan discovery iste · (b) PA yoksa kapsamı kullanıcıya
onaylatarak çıkar (*"bu durumda platform sorusu meşrudur"*) · (c) ikisi de yoksa
işi başlatma, eksiği bildir.

## En sinsi örnek — MB: tetiği olmayan kural

`MEMORY-PROPOSAL-BRIDGE` *"terfi olunca memory'den silmek ZORUNLU"* diyor.

> *"Ama agent terfi olduğunu NEREDEN öğrenir — tanımsız. AG kabul edip skile
> işler, agent'a haber DÜŞMEZ. **Kural bir eylem emrediyor, eylemin TETİĞİ yok** —
> silme hiçbir zaman tetiklenmiyor, kayıt sonsuza kadar yaşıyor."*

**Ve bu döngüyü kapatıyor:** MB'nin memory turunda bulduğu çelişki (çözülmüş
çatışmayı "açık" sanması) **tam bu boşluğun sonucu.** Semptomu bir turda,
kök nedenini diğerinde buldu.

---

# Diğer bulgular

## QA — kaynak/türev dalı (bugün canlı yaşandı)

`CR-VERIFY-SOURCE` *"iddiayı Read/grep/git ile TEYİT et"* diyor;
*"açtığın şey ASIL kayıt mı TÜREV mi"* demiyor.

> *"Bugün PRC-45'te üç taraf da doğru ölçtü, farklı dosyaya bakıyordu
> (.json arşiv / .md kopya) ve ben önce 'yanlış ölçüm' hükmü kurdum."*

**Önerisi:** *"Teyit ettiğin belge ASIL kayıt mı, kopya mı ayırt et — içerik aynı
olsa bile **kalıcılık farklıdır**; çelişki varsa önce 'ikimiz de doğru ölçmüş
olabiliriz, ölçtüğümüz ŞEY farklı' diye sor."*

## PA — `HANDOFF-SCREEN-ONLY` kanal düzeniyle çelişiyor

> *"Kanon: 'Handoff EKRANA basılır, dosyaya YAZILMAZ.' Ama bu oturumun kanal
> düzeni: 'ekrana yazdığın her şeyi kanala da yaz' — ve **kanal DOSYADIR.**
> Bugün her handoff'u iki yere yazdım ve **çelişkiyi fark etmedim.**"*

**Önerisi:** *"Yasak olan PROJE DOKÜMANINA (docs/) handoff dosyası açmaktır;
ileti kanalı dosya olsa da EKRAN sayılır."*

## BE — index kuralı kendi içinde çelişiyor (bugün memory işinde çarptı)

- `MEMORY-INDEX-ONLY`: *"her kayıt ≤150 karakter"*
- `MEMORY-INDEX-IS-CONTEXT`: *"index yönlendiricidir, doğru kaydı seçtirmeli"*

> *"Ayırt edici bir kanca 150 karaktere sığmıyor; kısaltırsam index **isim
> listesine düşer**, kısaltmazsam kuralı çiğnerim. Bende 67 pointer'ın 63'ü
> sınırın üstünde."*

**Önerisi:** *"Sınır satır bazlı değil TOPLAM bazlı olsun: index toplam 25 KB'ı
aşamaz; satır uzunluğu ayırt ediciliğe göre serbesttir. 20 KB'ı aşınca budama
başlar."*
> *"Asıl arıza satır uzunluğu değil, **25 KB'dan sonrasının SESSİZCE
> yüklenmemesi.** Satırı kısaltmak o arıza için dolaylı bir vekil."*

⚠️ **Bu, bugün sekiz agent'ta ölçtüğüm ihlalin gerekçesini veriyor** — kural
ihlali değil, **kuralın kendisi çelişkili** olabilir.

## DO — harita etiketi yanıltıcı, prod kapısını gizliyor

> *"Alet çantası `deploy-release`'i **'git akışı / push-merge sahipliği'** diye
> tanıtıyor. Ölçtüm: o skilde DO'nun **YEDİ prod kuralı** var (PRECHECK-7,
> PRODUCTION-TAG, MERGE-COMMIT-ONLY, NO-ROLLBACK-MISSING…) — hiçbiri 'git akışı'
> değil. `DO-NO-DEV-GIT` 'dev git işin yok' dediği için bu etiket **'bana değil'
> diye okunabilir ve prod kapısı sessizce atlanır.**"*

## CA — ölçülebilirlik ≠ ölçüldü

`CODE-COUNT-BY-LSP` interface dispatch'i *"goToImplementation ÇÖZER"* diyor;
`CA-IMPACT-STATIC-ŞERH` listesinde interface dispatch **yok** — çünkü ölçülebilir
sayılıyor. Araç yoksa **ne ölçülebiliyor ne şerhe yazılabiliyor.**

**Önerisi:** *"Araç erişilemediği için ölçülemeyen her eksen — interface dispatch
dahil — şerhe ADIYLA yazılır: 'X aracı yoktu, bu eksen ölçülmedi.'
**Ölçülebilir olması, ölçüldüğü anlamına gelmez.**"*

---

# Dürüstlük notu — FE'nin sınır beyanı

> *"BULAMADIM DEDİKLERİM: 1c · 2b · 2c. **Uydurmadım.**
> SINIRIM: bugün 9 skill açtım (76'nın ~%12'si). Açmadığım skillerde çelişki
> olabilir — **'yok' demiyorum, BAKMADIM diyorum.**"*

UID de aynısını yaptı: *"Kapanış zincirinde çelişki ARADIM ve BULAMADIM.
Uydurmuyorum, temiz."*

---

# Fabrikaya öneri (karar Mert'in)

**1. "Önkoşul sağlanmıyorsa" taraması yapılsın.** UID'in önerisi. Bugün 11 vaka
çıktı ve hepsi tesadüfen bulundu — sistematik tarama daha fazlasını çıkarır.
Ölçüt: *"bu kural bir şey emrediyor; o şey mümkün değilse ne olacak?"*

**2. Index kuralı yeniden düşünülsün** (BE'nin önerisi). Bugün 8 agent'ta ihlal
ölçüldü — bu kadar yaygın ihlal, kuralın kendisini sorgulatır.

**3. Yukarıdaki dokuz öneri cümlesi** doğrudan kullanılabilir hâlde yazıldı.
