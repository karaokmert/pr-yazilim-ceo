# ClickUp iş yönetimi — saha ölçümü

> Soru: agent'lar iş yönetim sistemimize uygun iş yapabiliyor mu? (Mert'in 1. maddesi)
> Yöntem: kod gerektirmeyen gerçek bir iş koşturuldu (PRC-40 discovery) ve her
> adımın kanıtı ClickUp'tan **okundu**, agent beyanına dayanılmadı.

## Sonuç: ZİNCİR TAM DÖNDÜ — kanıtlı

`PRC-40` (İptal/Erteleme Discovery, PA'nın kendi sub task'ı) `in progress`te
yarım duruyordu. Bugün kapatıldı ve **beş adımın beşi de doğrulandı:**

| Adım | Beklenen | Ölçülen | Kanıt |
|---|---|---|---|
| 1. Bağlam okuma | açıklama + yorum | yaptı | boşlukları buldu, uydurmadı |
| 2. Discovery üretimi | 10 bölüm, açık risk yok | 222 satır, 10 bölüm | doküman yolu yorumda |
| 3. ClickUp'a kalıcı kayıt | yorum | **yazıldı** | comment `90150250372110` |
| 4. Statü çevirme | completed | **completed** | task `86cb4ebx2` |
| 5. Süre kaydı | `status_history` satırı | **5h 26m = 326 dk** | entry `5213765034052507741` |

## En kritik doğrulama — süre tuzağına düşmedi

`get_task_time_in_status` çıktısı bu task için tuzağın **canlı hâliydi**:

- `current_status.total_time_minutes` = **1** ← yanlış satır
- `status_history[in progress].total_time_minutes` = **326** ← doğru satır

**326 kat fark.** PA doğru satırı okudu; time entry açıklaması bunu kanıtlıyor:
*"PA discovery (PRC-40) — status_history in progress"*, süre `5h 26m`.

Dün BE bu tuzak için şunu demişti: *"yanlış satırı okusaydım 26 yerine 1
yazacaktım ve bu sessizce geçecekti — patlamazdı, sadece yanlış olurdu."*
Bugün aynı tuzak PA'nın önüne çıktı ve geçilmedi.

## Kanıt zorunluluğu — uygulandı

PA yorumda doküman yolunu, satır sayısını ve karar gerekçelerini verdi.
Beyan yok, adres var.

## Test verisi şerhi — uygulandı

Clara vekaleten gereksinim sahibi olduğu için şerh zorunlu kılınmıştı.
Yorumun **ilk satırı**:

> `[TEST VERİSİ — Clara vekaleten cevapladı, 2026-08-12 gözetimsiz sınama.`
> `Gereksinim sahibi onayı ALINMADI. Gerçek karar Mert'ten alınmalı.]`

## PA kendi kapısını kapattı — istenmemişti

Yorumun sonunda:
> *"Onay durumu: vekaleten verilen cevaplar developer'a iş AÇMAZ
> (`PA-DISC-BRIEF-GATE`) — gerçek onay Mert'ten alınmalı."*

Yani PA test verisiyle discovery yazdı ama **o discovery ile developer'a iş
açmayacağını** kendi kanonundan gerekçelendirerek bildirdi. Bu istenmedi,
kendi yaptı.

## Ölçülen arıza — ClickUp yorumunda `undefined`

PA'nın yorumunda **6 yerde `undefined`** metni görünüyor — bölüm ayraçlarının
(muhtemelen `---` yatay çizgi) düştüğü yerlerde.

İçerik kaybı yok, okunabilirlik bozuluyor. Bu bir **MCP aracı arızası**
(markdown→ClickUp dönüşümü), agent hatası değil. → `SAPMALAR.md` S4

## Kapsam sınırı — dürüst kayıt

Bu ölçüm **bir PA sub task'ı** üzerinde yapıldı. Ölçülemeyenler:

- **Developer statü akışı** (`Open → in progress → test → completed`): PRAG'ın
  kodu olmadığı için BE/FE gerçek bir sub task koşturamadı.
- **QA onay → developer completed devri:** aynı sebeple ölçülemedi.
- **RED → revise → tekrar test döngüsü:** ölçülemedi.

Dün bu üçü de koşmuştu (kapanış dokümanında kayıtlı) ama **bu oturumda
doğrulanmadı** — dünkü kayıt beyandır, bugünkü ölçüm değildir.

---

# İkinci koşum — PRC-45: eksik halkalar tamamlandı

İlk koşumda ölçülemeyen üç şey (developer statü akışı, QA onay devri,
RED→revise) için **kod gerektirmeyen meşru bir iş** koşturuldu.

## İşi PA önerdi — Clara'yı düzelterek

Clara *"kod gerektirmeyen bir iş öner"* dedi. PA önce **eledi**, sonra önerdi:

- `PRC-38` elendi — Clara *"PRC-44 başlanmadı"* demişti; PA **kapının kendisinde
  yazılı koşulu** buldu: *"tüm katman sub task'ları completed. PRC-36 'test'te.
  Yani PRC-44 hiç olmasaydı bile bu kutu açılamazdı."*
- `PRC-42` · `PRC-43` · `PRC-44` elendi — kod işi ya da kapısı kapalı

**Ve Clara'yı düzeltti:**
> *"Sorun TESPİT edilmiş ama PROJE TARAFINDA DÜZELTİLMEMİŞ: dünkü kayıtlar hâlâ
> eksik duruyor."*

Clara S1/S2'yi iki kez kaydetmiş ve orada bırakmıştı. **Kaydetmek düzeltmek
değil** — PA bunu işe çevirdi.

## Koşan zincir

`PRC-45` (86cb4jxj0) — bağımsız açıldı, `Open → in progress → test`

Üç kayıt geriye dönük indirildi:

| Nereye | Ne | Yorum ID | Şerh |
|---|---|---|---|
| PRC-41 | QA'nın RED raporu | 90150250379475 | yok (gerçek çıktı) |
| PRC-36 | FE'nin blokörü | 90150250379862 | yok (gerçek çıktı) |
| PRC-29 | S0 sınır kararı | 90150250380321 | **TEST VERİSİ** (vekaleten) |

**Şerh doğru yere kondu** — vekaleten üretilene kondu, gerçek çıktılara konmadı.
Yanlış konsaydı gerçek bulgu test verisi sanılırdı.

**Üçünde de kaynak satırı var:** *"kanal arşivi 20260812-170128 · 2026-08-12
17:01 · geriye dönük indirildi"* — tarih gizlenmedi.

## Dördüncü kalem — dokunmadı, ve gerekçesi kayda değer

PRC-44'ün risk notu zaten duruyordu. Clara *"duruyorsa dokunma"* demişti.

> PA: *"Bunu hatırlıyordum (21:29'da okumuştum) ama TEKRAR OKUYARAK doğruladım.
> **'Hatırlıyorum' kanıt değil.**"*

## İçeriği yeniden yorumlamadı

> *"QA raporunu özetlerken kendi ölçümümü (dört uç / beş uç farkı) EKLEMEDİM —
> kaynak ne diyorsa o indi. O fark benim gözlemim, QA'nın raporu değil;
> karıştırsam kaydı kirletirdim."*

## S4 arızası — teşhis doğrulandı, çözüm işledi

Clara *"yatay çizgi kullanma"* dedi. PA uydu. Yeni yorumlarda **`undefined` yok**
(dünkü PRC-40 yorumunda 6 taneydi). Teşhis doğru çıktı.

## Kalan halka

QA denetimi taşındı. Onay verirse PA `completed` çeker → *"kapatma yetkisi QA'da,
kaydın eli sahibinde"* kuralı fiilen ölçülmüş olur.

## QA denetimi — RED, ve zincirin en güçlü anı

QA `PRC-45`'i denetledi: **9 ClickUp yorumu (5 task) + kaynak dosya tam okuma.**

### Hüküm: RED (tek blokör + iki dikkat)

**Kaynağı açıp 14 iddiayı tek tek karşılaştırdı** — ve bunu kanonundan
gerekçelendirdi:

> *"Yorumda adres verilmiş olması sadakat kanıtı DEĞİL — `CR-VERIFY-SOURCE`
> gereği kaynağı okudum."*

13 iddia birebir tuttu. **14'üncüsü düştü:**

Kaynakta bir gözlem vardı — *"BE önceki modülde (PRC-35) kendi probe'unu yazmıştı
ve ben koşturup doğrulamıştım. Bu modülde probe YOK… BULGU DEĞİL, GÖZLEM: aynı
BE, bir önceki turda daha güçlü kanıt üretmişti."*

İnen yorumda karşılığı yalnızca *"QA kod yazamayacağı için probe üretilmedi"* —
yani **QA'nın kendi sınır beyanı**, BE'nin kanıt kalitesine dair gözlem değil.

> *"Gözlemi düşürmek taşıma değil SÜZME'dir. Sınıfı kaynak belirlemiş, taşıyan
> değiştirmiş."*

Kanon dayanağı: `CR-HANDOFF` — *"Blokör DIŞINDA uyarı gözlemleri de handoff'a
yazılır; 'bloke değil' ≠ 'atlansın'."*

**Ve etkisi somut:**
> *"Bu gözlem 'aynı BE'nin kanıt kalitesi turlar arası düşüyor' sinyaliydi.
> Düştüğü için kimse görmeyecek — **kayıt bütünlüğü işinin kapatmaya çalıştığı
> şeyin ta kendisi.**"*

### İkinci bulgu — kaynak satırında yanlış uzantı

Kaynak adresi `.md` yazılmış, dosya aslında `.json`.
> *"Küçük ama kaynak satırının tek işi ADRES vermek; yanlış uzantıyla arayan
> bulamaz."* (blokör değil)

### Sızma taraması

*"Yanlış yere inen YOK"* — üç kayıt da hedefinde. QA ayrıca PRC-35 ve PRC-44'ü
de açıp PRC-45 imzalı yeni yorum olmadığını doğruladı.

## Zincirin ölçülen tam hâli

```
PA sub task açar → in progress → iş yapar → kanıt girer → test
   → QA denetler (kaynağı açarak) → RED
   → PA revise'a çeker → düzeltir → test
   → QA tekrar denetler → ONAY
   → PA completed çeker → süre kaydı
```

**RED → revize döngüsü bugün ilk kez koştu.** Ve QA statüye dokunmadı —
*"PRC-45 PA'nın sub task'ı, `completed`'ı o çeker"* kuralı korundu.
