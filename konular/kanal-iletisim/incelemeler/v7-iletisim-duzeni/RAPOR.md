# v7'nin iletişim düzeni — neyle tutturuyordu

**Tarih:** 2026-08-03
**Soru:** Mert v7'de bir iletişim/brief/handoff düzeni yakaladığını, v8'de ve sonrasında
hiçbir yerde tutturamadığını söyledi. O düzeni ne sağlıyordu?

## Nerede yaşıyor

`v7/ozel-yazilim/.claude/skills/handoff/SKILL.md` — tek dosya, iki bölüm:

**Brief Formatı** (satır 182-199) — commit öncesi kullanıcıya verilen sözlü rapor.
**Yapılandırılmış Handoff** (satır 42-71) — agent'tan agent'a giden blok.

İkisi de aynı skill'de ve ikisi de tüm 9 agent tarafından preload ediliyor.

## Mekanizma — üç şey, üçü birden

Okundu ve çıkarıldı (ölçüm değil, metin analizi):

**1. Uzunluk yapıyla kısıtlanmış, "kısa yaz" denmemiş.**

Handoff bloğunda: *"Ne: tek cümle"*, *"Neden: tek cümle"*, *"Oku: tek bir dosya yolu
veya commit hash'i. Liste değil."*, *"`----` sınırlayıcı açılış ve kapanış ZORUNLU"*.

Bunlar sayılabilir. Model sayılabilir kısıta uyar. *"Kısa tut"* uymaz çünkü kısanın
ne olduğu belirsiz — her model kendi eşiğini uydurur.

**2. Negatif liste pozitiften güçlü.**

Brief'te üç madde "içermeli", üç madde "içermemeli". Ama içermemeli tarafı çok daha
somut: kod snippet'i yok · terim yok (*"handler", "DataLayer", "endpoint" yerine
"sipariş kaydı oluşturma"*) · *"test ettim, çalışıyor"* yok (*"kullanıcı bunu zaten
bekliyor"*).

Handoff'ta aynı desen: *"'Ne yapılacak' listesi, 'Dikkat edilecek noktalar', 'Kontrol
et' direktifleri YAZMA — bu handoff'u raporlaştırır."*

Neden işe yarıyor: model neyi ekleyeceğini kendiliğinden bulur, neyi **çıkaracağını**
bulamaz. Çıkarma listesi olmadan her cevap büyür.

**3. Ton bir role bağlanmış, sıfata değil.**

> *"Ton: yazılım mühendisi proje yöneticisine rapor veriyor — günlük dil, teknik
> jargon yok, ama teknik kararların gerekçesi var."*

Bu tek cümle onlarca kuralı içinde taşıyor. *"Sade ve anlaşılır ol"* deseydi hiçbir
şey söylememiş olurdu — sadelik herkese göre değişir, ama "mühendis PM'e rapor
veriyor" herkeste aynı resmi üretir.

Ek olarak kanonun kendi örneği de kısa: brief örneği 4 cümle. Kural kendi biçimine
uyuyor.

## Çerçeveleyici cümle

> *"Handoff kısadır — sinyal, rapor değil. Detay yeri handoff değil; DISCOVERY.md,
> STATUS.md, commit mesajı."*

Kilit fikir: **kısaltma, bilgiyi atmak değil — bilgiyi doğru yere koymak.** Detay
siliniyor değil, adreslenmiş bir yere taşınıyor. Bu yüzden kısalık bilgi kaybı
üretmiyor.

## Clara'ya uyarlanırken ne değişti

v7'nin brief'i **tek seferlik** bir çıktı (commit öncesi). Clara'nınki **sohbet** —
her turda brief verilemez. Format birebir alınmadı, mekanizma alındı.

Clara kanonuna yazılan hâli (`.claude/agents/clara.md`, "Nasıl konuşursun"):
bir bulgu · üç paragraf · bir soru (tek kelimeyle cevaplanabilir) — ve üç çıkarma
kuralı: bulgu listesi yazılmaz, nasıl bakıldığının anlatısı yazılmaz, zaten bilinen
bağlam geri özetlenmez.

## Fabrikaya giden

Fabrika agent'larında (PAM, PAD, PQA, PCA) bu düzenin karşılığı **ölçülmedi** —
`gereksinim-behavior.md` okunmadı. Devir bloğu yazıldı ve Mert'e verildi (2026-08-03),
ölçümü PAM yapacak.

Bloğa konan uyarı: tek uzunluk kısıtı dört agent'a giymez. PQA'nın denetim raporu
doğası gereği uzun; ona "üç paragraf" denirse kesilecek ilk şey rahatsız eden bulgu
olur. Ortak olan **ton ve yapı**, uzunluk değil.

## Açık kalan

v7'nin bu düzeninin **davranışa** dönüşüp dönüşmediği ölçülmedi. Mert'in "v7'de
tutuyordu" demesi saha gözlemi ve güçlü bir işaret, ama A/B eval yapılmadı. Yani
buradaki üç mekanizma çıkarım — metinden okundu, davranışla sınanmadı.

Sınanacaksa yolu belli: aynı durumu iki forma (v7 brief kanonu / kanonsuz) verip
çıktı uzunluğunu ve içerdiği gereksiz kalemi karşılaştırmak.
