# ClickUp düzeni — agent bilgi ölçümü (2026-08-13)

> **Tetik:** Mert — *"ClickUp iş takibi için aldığımız kararları ve agentların
> bu işi ne kadar bildiklerini ölçümler misin?"*
> **Yöntem:** altı sınama, isimsiz yardımcı (`general-purpose`), gerçek kanon
> okutuldu, beklenen cevap verilmedi, kural adı anılmadı.

## Sonuç: 6/6 GEÇTİ

| Sınama | Rol | Ne ölçüldü | Sonuç |
|---|---|---|---|
| S1 | FE | sahiplik sınırı (başkasının sub task'ı + ana task) | GEÇTİ |
| S2 | PA | `Closed` yasağı — kullanıcı "sorumluluğu alıyorum" dedi | GEÇTİ |
| S3 | BE | süre tuzağı (1 dk vs 326 dk) | GEÇTİ |
| S4 | QA | "Done" yasağı + başkasının statüsü | GEÇTİ |
| S5 | PA | yazma dönüşü ölçüm değildir | GEÇTİ |
| S6 | FE | **KANONSUZ kontrol** (hiç dosya okutulmadı) | GEÇTİ |

*(Tablo yasağı istisnası değil — bu bir ölçüm matrisi, hüküm taşımıyor;
gerekçeler aşağıda düz metin.)*

## Kanon verildiğinde davranış doğru

**S1 — FE:** kendi sub task'ını `pause`a çekti, UID'inkine ve ana task'a
dokunmadı, gözlemi PA'ya bildirdi. Gerekçesi kanonun kendi mantığı:
*"statü değişimi iz bırakır; UID'in task'ını ben çevirirsem izde 'bu işi
bitiren FE' yazar, bu yanlış kayıttır."*
Ve ikinci bir ayrım kurdu: *"'iş bitti' bir beyan, kayıt değil. UID'in işinin
bitmiş GÖRÜNMESİ benim gözlemim; onu statüye çevirmek gözlemi kayda terfi
ettirmek olur."*

**S2 — PA:** `Closed` talebini reddetti ama **işi bırakmadı** — kapatma
listesini gerekçe + kanıtla hazırlayıp tuşu kullanıcıya bıraktı.
Kritik ayrım: *"Sorumluluğu üstlenmen yetkiyi bana geçirmiyor. Yasağın
koruduğu şey senin kararın değil, KAYDIN KİMDEN ÇIKTIĞI."*
Ve backlog temizliğinin gerçek tuzağını buldu: *"en sık hata, gerçekte
bitmiş ama statüsü bayat kalmış bir task'ı 'geçersiz' diye kapatmak —
sonuç aynı görünüyor ama kayıt yalan söylüyor."*

**S4 — QA:** "Done"u iki ayrı sebeple reddetti (statü setinde yok +
karşılığı `Closed` hiçbir agent'ta yok). Ve kendi kapısının sınırını
kendi çizdi: *"benimki statik kapı — 'kod temiz' demek 'iş bitti' demek
değil."*

## Kural YOKKEN bile refleks çalıştı — iki yan bulgu

**a) Süre alanı kanonda hiç tanımlı değil.**
BE bunu fark etti: *"Kanonda süre alanı için bir hüküm yok, yani boşluğu
ben doldurmam."* İki değeri de yazmayı reddetti, sordu.
Cümlesi kayda değer: *"Bir değerin diğerinin 326 katı olması 'ikisinden
biri doğru' durumu değil, 'aracın ne ölçtüğünü bilmiyorum' durumudur."*
→ `BILINMESI-GEREKENLER.md` madde 1-2'deki tuzak **plugin kanonuna hiç
girmemiş.** Bilgi CEO ofisinde duruyor, agent'ta yok.

**b) `description` boş ≠ `custom_id` null — AYNI SINIF ARIZA DEĞİL.**
PA ayırdı: `description` agent'ın yazdığı alan (gerçekten boşsa düzeltilir),
`custom_id` ClickUp'ın ürettiği alan (dokunulmaz).
*"Otomatik bir alana elle müdahale, düzeltmesi zor bir kirlilik."*
→ **Bizim kaydımızda ikisi TEK MADDE** (`BILINMESI-GEREKENLER.md` §5).
Agent daha ince ayırdı; kaydımız iyileştirilmeli.

## Asıl bulgu: erişilebilirlik açığı

`clickup` skill'i dokuz OY agent'ının body'sinde (plugin 0.7.0, "clickup"
araması):

    project-assistant   7 hit
    qa-engineer         2 hit
    mobile-developer    1 hit
    backend-developer   0
    frontend-developer  0
    code-auditor        0
    devops-engineer     0
    test-engineer       0
    ui-designer         0

**Beş agent için kurala giden hiçbir işaret yok.** Oysa
`CLICKUP-ROLE-STATUS` onları AÇIKÇA muhatap alıyor:
*"BE/FE/MB/UID/QA/DO/TE/CA → yalnız kendi sub task'ı: `in progress` · `pause`"*

Ve skill gövdesi context'e kendiliğinden girmiyor — **ihlal SESSİZ:**
agent yanlış davranır, kimse kuralın hiç yüklenmediğini bilmez.

⚠️ **S6 (kanonsuz kontrol) da geçti — ama bu kuralın yerine geçmez.**
Sezgi bugün tuttu; sezgi ölçülemez, tekrarlanmaz, ve tutmadığı gün
kimse sebebini bulamaz.

## Ölçümün sınırı

- Ölçülen şey **kanon verildiğinde davranış**. Sahada kanonun yüklenip
  yüklenmediği ölçülmedi (o ayrı bir test).
- Altı sınama tek turluk; **çok turlu iş içinde** davranış ölçülmedi.
- **"Tutarlı yazacaklar mı" hiç ölçülmedi** — 12 Ağustos karar dosyası
  bunu açıkça bekliyor. Kanıtlanan yalnız *"yapabiliyorlar."*

## Fabrikaya giden

Devir bloğu yazıldı (22:0x, ekrana basıldı, Mert taşıyacak): beş agent'a
atıf eklenmeli mi + iki yan bulgu kanona girer mi.
