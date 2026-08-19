# Fabrika v2 üretimi — ihtiyaçtan sıfırdan ekip

Tarih: 2026-08-19 akşam
İstek: Mert *"skill-project'teki dört fabrika agentını sıfırdan ürettir. Kuralları yok
say. Skill plugini ve plugin-dev pluginini kullan. İhtiyacı belirle, bizim canonlardan
bahsetme, çıktıyı test et. Skilleri asla sen verme — sen sadece öner."*

Sonra: *"ben pc'den uzaklaştım, kararlar sende artık."*

## Sekiz şikayet (ihtiyacın kaynağı)

Mert'in kendi cümleleri: ürün çok gecikiyor · kapsam değişimi sorun üretiyor,
*"sürekli neden olmazı açıklıyorlar"* · kural kimlik sistemi gereksiz · bir ekleme
5 yeri etkiliyorsa 4'ü kaçıyor · fikri geliştirmiyor ilerletmiyorlar · body/skill/
referans geçişi kurulamıyor, *"bir kararın nereye yazılacağı hâlâ net değil"* · bir
talep verildiğinde ne olacağı kurgulanamıyor · *"skillerimiz sıradanlaşıyor, agentlar
çok sıkışık hale geliyor, iş yapamaz hale geldim v8 agentlarında."*

## Yapılan

`~/p/fabrika-v2` — 43 dosya, commit `3a3ad33`.

Akış: ihtiyaç dokümanı (283 satır, sıfır kanon terimi) → üç bağımsız tasarım (hız /
bağlantı / kullanıcı deneyimi odaklı) → birleşik tasarım → dört paralel üretim →
üç eksenli sınama → symlink.

**Üç tasarım da bağımsız olarak aynı yapıya vardı: 3 rol, 2 onay kapısı.** Yakınsama
kararı bir tercihten bir bulguya çevirdi. Kaldırılan rol: ayrı ölçümcü — üçü de aynı
gerekçeyle kaldırdı (ölçüm bir rol değil, alet; role çevrilince rapor ürüne tercih
ediliyor).

Roller: `fabrika-ortak` (kullanıcıya karşı sorumlu, fikri ilerletir, yayınlar) ·
`fabrika-yapici` (ürüne karşı sorumlu, üretir, kendi çıktısını sınar) ·
`fabrika-korgoz` (sisteme karşı sorumlu, gerekçe okumadan ölçer).

## Sınama sonuçları

Mekanik **72/72** · Davranış **9/9** · Yeterlik **geçti**.

Yeterlik testinin en güçlü sonucu: üç rol istendi, ekip sahayı ölçüp **iki rol + iki
alet** önerdi — çünkü ödeme kanonu (`local-payment`, `iap`) OY'da zaten kurulu ve
kopyası çıkarılmamalı. Bedelini de yazdı (*"tek muhatap kaybolur, rol adı hatırlanır
akış hatırlanmayabilir"*) ve kanıtsız iddiada bulunmadı.

## Ölçülen karşılaştırma

Agent'ın önündeki kanon: **4.800 → 851 satır** (5,6 kat), ayrıntı 2.394 satır
referansa indi. Kural kimliği **138 → 0**. Onay kapısı **7 → 2**. Skill kelime
sayısı: mevcut 2.559–9.489 (resmi eşik 1.500–2.000, hiçbiri uymuyor) → yeni
991–1.265 (dokuzu da eşiğin altında). Referans atfı: mevcut 4 atıf / 3 skill'in hiç
referansı yok → yeni 18 atıf, 0 kırık.

## Kendi ölçümüm iki kez yanlış çıktı

Bunu yazıyorum çünkü tekrarlanacak bir hata.

**Zaman damgası eksikti.** İlk mekanik koşumda 7 kırık referans buldum ve rapora
yazdım. Üçü kırık değildi — o dosyalar 19:40-19:42'de yazıldı, ölçüm 19:39'da koştu.
Gerçek sayı 4. **Paralel üretim sürerken alınan ölçüm zaman damgası taşımalı**, yoksa
bitmemiş işi kusur diye raporlar.

**Tarama deseni çapraz atıfa kör.** `references/[a-z0-9-]+\.md` deseni
`../baska-skill/references/x.md` ön ekini yutuyor, kalanı yerel dizinde arıyor ve var
olan dosyayı kırık gösteriyor. Bir üretici yakaladı, ben değil.

## Mekanik bulgu: symlink sonrası tanınma asimetrik

Symlink kurulduktan hemen sonra **aynı oturumda** skill'ler ve command'lar tanındı,
**agent'lar tanınmadı** (`agent type not found`). Agent listesi oturum başında
okunuyor. Yani yeni agent ancak bir sonraki oturumda çağrılabilir. Bilinmezse
*"agent çalışmıyor"* diye yanlış teşhis üretir.

## Ölçülmeyen — karar bunu bilmeden verilmemeli

**Gerçek uçtan uca koşum yapılmadı.** Yalnız birinci durak (ortak) koşuldu. Yapıcı
gerçekten üretiyor mu, korgöz gerçekten denetliyor mu, **hook'lar gerçekten tetikleniyor
mu** — hiçbiri canlı ölçülmedi. Hook'ların JSON'u geçerli, promptları doğru; fiilen
çalıştıkları görülmedi.

**Gecikme sahada ölçülmedi.** Yapısal olarak çözüldü (7→2 kapı, `Stop` hook'u dosyasız
bitişi engelliyor) ama gerçek bir işin süresi ölçülmedi.

**Sıradanlaşma yarım kaldı.** `emsal-zorunlulugu` kaynak zorunluluğu koyuyor ama gerçek
ilaç bir deneyim havuzu ve o havuz yok.

## Sonraki adım

Symlink kurulu (`.claude/agents/` + `skills/` + `commands/`). Bir sonraki oturumda
üç agent çağrılabilir olacak. Gerçek sınama: `/is-basla <gerçek talep>` → KAPI 1 →
yapıcı → korgöz → KAPI 2. Bu koşum gecikmeyi, hook'ları ve üretim kalitesini birden
ölçer.

Ondan önce bu ekip **umut verici ama kanıtlanmamış.**

## Açık bulgu — Mert'in kararına bırakıldı

`<example>` bloklarının yeri. Üretilen agent'lar description'da 3-4 blok taşıyor,
gövdede sıfır. Resmi örnek `agent-creator` **ikisini birden** kullanıyor (description'da
3, gövdede 4). Description her turda context'te, yani orada duran blok her tur maliyet;
ama tetikleme keskinliği de veriyor. Tek başıma değiştirmedim — ölçüm iki yönü de
destekliyor, seçim bir tercihe bağlı. Ölçülmesi gereken: blokların token maliyeti ve
tetikleme isabetine katkısı.
