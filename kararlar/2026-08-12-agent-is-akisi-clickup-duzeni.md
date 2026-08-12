# Agent iş akışı — ClickUp task takip düzeni

**Tarih:** 2026-08-12 · **Karar:** Mert · **Getiren:** Clara (fabrika modu)
**Gereksinim:** `fikirler/agent-is-akisi/is-akisi-taslak.md` (v3)
**Test kaydı:** `fikirler/agent-is-akisi/pam-sorulari.md`

Bu doküman günün tüm kararlarını tek yerde toplar. Tek tek gerekçeleri ayrı
dosyalarda (aşağıda atıflı).

---

## Kararların listesi

**1 · ClickUp yazma yetkisi — yasak kalkmaz, KAPSAMI daralır**
Agent yalnız kendi sub task'ının statüsünü çevirir.
→ `kararlar/2026-08-12-clickup-yazma-yetkisi-kapsam-daraltma.md`

**2 · `TASK-STATUS.md` ve `status.md` kalkıyor** (+ `DEVIR-{hedef}.md`)
Olay akışı sub task'larda zaten tutuluyor.
→ `kararlar/2026-08-12-task-status-ve-status-md-kalkiyor.md`

**3 · Clara OY kanonuna GİRMEZ**
Kanon `kullanıcı` der; Clara perde arkasında kalır.
→ `kararlar/2026-08-12-clara-oy-kanonuna-girmiyor.md`

**4 · Sub task sahipliği BAŞLIK ÖNEKİNDEN okunur** — `[FE] PRAG - ...`
Kural: *"başlık senin kısaltmanla başlamıyorsa dokunma."*

**5 · Ana task her zaman PA'nın.** QA'nın tek istisnası: push ettiği sub task'ı
`live - dev`'e alır.

**6 · Kural iki ayrı yere yazılır:** akış → `is-akisi` (tek kaynak, omurgalar atıf
verir) · mekanik → `clickup` skill'i (PA dilinden GENELE çevrilir).

**7 · Prod'da elle yapılacak işler → ana task yorumu** (`PROD İŞLERİ` başlığı).

**8 · Süre: statü süresi tracked'e işlenir** — agent çeker, hesaplamaz.

**9 · Kanıt ROLE göre değil, ÇIKTI TÜRÜNE göre tanımlanır.**

**10 · Kapsam OY.** Websitesi sonra.

---

## Neden ayrı bir karar dokümanı gerekti

Bu kararlar **tek bir sorudan** doğmadı. Sahada bir düzen kuruldu (bugünkü test),
kanonla çakıştı, ve çakışmayı çözerken **on ayrı karar** çıktı. Hepsi birbirine
bağlı — biri değişirse diğerleri de değişir.

---

## Karar yöntemi — üç kez sunulan seçenekler reddedildi

Günün en belirleyici üç anı, Mert'in sunulan şıkları reddedip **sorunun kendisini
yeniden kurduğu** anlar oldu:

**1) ClickUp kuralı — (a) gevşesin / (b) kalsın diye soruldu, ikisi de reddedildi.**
Sebep `CLA-FIX-THE-CAUSE`: ikisi de **yama**, çünkü ikisi de sebebi yerinde bırakıyor.
Asıl sebep *"statüyü kim çevirir"* değildi — **kural, kendisini askıya alacak meşru
bir yol tanımlamamıştı.** Kural metni *"kullanıcı talimatıyla da AÇILMAZ (istisna
yok)"* diyor, ama bugünkü test tam o yoldan yürüdü. Kapsam daraltma sebebi kaldırıyor:
sınır artık **talimatla değil sahiplikle** çiziliyor.

**2) Kanıt listesi — "her role bir kanıt türü" varsayımı reddedildi.**
Clara dokuz role tek tek kanıt arıyordu. Mert: *"QA okeyleyip UID'e döndüğünde;
TE her işte işe girmez."* Doğru ölçüt buradan çıktı: **kanıt role göre değil çıktı
türüne göre.** Roller her işte yok — rol bazlı liste yazılırsa girmeyen rolün satırı
boş kalır.

**3) Başlık formatı — üç seçenekten en ölçülebilir olanı seçildi.**
Alan sırasına dayanan iki format elendi çünkü **modül adında bir tire geçerse alan
kayar** ve kural sessizce yanlış task'ı işaret eder. Köşeli parantez `startswith` ile
ölçülür, ayraçtan bağımsızdır.

---

## Ölçümle çürüyen üç iddia — kayda geçiyor

**1) *"Kuralın gerekçesi çürüdü"* — YARIM doğruydu.**
Gerekçe *"agent ya skill'siz MCP'ye gider ya hiç yapmaz, **iki durumda da iz
tutarsız**"* diyordu. Ölçüm birinci kısmı çürüttü (yapabildiler — engel skill değil
izin katmanıydı); **ikinci kısım hiç ölçülmedi** (tek tur, kurgusal proje, gözetim
altında). Kanıtlanan *"yapabiliyorlar"*, kanıtlanmayan *"tutarlı yapacaklar"*.

**2) *"Sette v7 artığı statüler var"* — Clara'nın hatası.**
`full stack`, `backend`, `front` gibi statüler *"artık"* diye okundu. Mert düzeltti:
**v7/v8 ayrımı agent kanonundaydı, ClickUp listesinde değil** — liste canlı ve
insanlar da kullanıyor. Hatanın sınıfı: ölçümde görülen bir ismi kanon tarihçesiyle
eşleştirmek.

**3) *"Süre mekanizması tutmadı"* — sebebi başkaydı.**
Tracked'de 9,5 saniye, statü süresi 45 dakika. Arıza sanıldı; **test sırasında bir
kez elle girilmiş bir değermiş.** Kural zaten bunu düzeltiyor.

---

## PAM testi — ölçülen sonuç

Gereksinim taslağı iki kez PAM rolündeki isimsiz yardımcıya okutuldu (ölçüm, iş
devri değil — niyet taşınmadı, doküman savunulmadı).

**v1 → 18 soru, *"Hayır, kanon yazamam"*.** Sorular *"bu ne demek"* tipindeydi:
Clara kim, `test` statüsü var mı, sahiplik nerede yazılı. Yani **doküman
anlaşılmıyordu.**

**v2 → 6 soru, *"Kısmen — 1 ve 2 cevaplanırsa aynı gün başlarım"*.** Sorular
*"bunu nereye yazayım"* tipine döndü. Yedi parçayı **şimdi yazabileceğini** saydı.

⚠️ **Sayının düşmesi tek başına ölçüt değildi — türün değişmesi ölçüttü.**
Aynı sayıda ama yine *"bu ne demek"* tipi soru gelseydi doküman düzelmemiş olurdu.

**PAM ölçümlerimizi denetledi ve doğruladı:** cascade tam 21 dosya · dört kural
ID'sinin dördü de kanonda mevcut ve doğru alıntılanmış · `clickup` skill'i gerçekten
yalnız PA'da. Kendi cümlesi: *"v1'de sayım hatalıydı, bu turda değil. Kalan sorularım
'doküman güvenilmez' değil **'bu kararlar henüz verilmemiş'** cinsinden."*

**PAM'in bulduğu, kimsenin görmediği kural:** `QA-STATUS-GIT-EVENTS`
(`quality/SKILL.md:169`) — *"QA kendi git olaylarını STATUS'a yazar."* `status.md`
kalkınca Actions sonucu nereye yazılacak? **Düşen kural dört değil beş olabilir.**

---

## Bilinen açık — kapatılmadı, işaretlendi

**`QA-STATUS-GIT-EVENTS`.** Push olayı statüde görünüyor (QA sub task'ı `live - dev`'e
alıyor); **Actions sonucu** için yorum yeterli mi, PAM değerlendirecek.

---

## Kaynaklar

- Gereksinim: `fikirler/agent-is-akisi/is-akisi-taslak.md`
- PAM testi + 18 soru: `fikirler/agent-is-akisi/pam-sorulari.md`
- Saha testi: `gunluk/ev/2026-08-12-clickup-task-takip-testi.md`
