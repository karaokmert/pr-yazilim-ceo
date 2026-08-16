# SendMessage "denendi mi" çelişkisi çözüldü — ve görünürlük problemi tek problemmiş

**Tarih:** 2026-08-16 · **Ölçen:** ev Clara · **Tetik:** Mert *"denedik ya goat'ta çalıştırdık"*
**Durum:** KAPANDI (çelişki) + AÇIK (görünürlük problemi)

## Çelişki neydi

Bu oturumda Mert *"SendMessage'ı goat'ta denedik"* dedi. Clara *"hayır, goat'ta koşan
kanaldı"* diye karşı çıktı — dünkü kapanış dokümanına dayanarak.

**Mert haklıydı. Clara yanlış özetlemişti.**

## Gerçekte ne olmuş

**2026-08-14, 00:29–00:40** — SendMessage aracı kanalla karşılaştırıldı (ev Clara +
goat Clara + DO + QA). **Mert'in kararı (00:40):** *"goat ekibi bir süre SendMessage
üzerinden yürütülecek."*

**Uygulandı.** Ev kapanışı: *"Ekip SendMessage'la yürüdü."* Goat kapanışında izi var —
`kazanim-sendmessage-onay-asktool`, kural 07:48'de verildi, iki turda uygulandı.

## Hatanın kökü — iki ayrı şey aynı adla anılıyor

| ne | denendi mi |
|---|---|
| **`SendMessage` aracı** (Claude'un kendi aracı) | ✅ goat'ta gece boyunca koştu |
| **`/sendmessage` komutu** (bizim yazdığımız slash komut) | ❌ bir kez bile çağrılmadı |

Kapanış dokümanındaki *"Command yazıldı, bir kez bile çağrılmadı"* satırı **ikincisini**
kastediyor. Clara bunu okuyup *"SendMessage denenmedi"* diye özetledi.

⚠️ **Ders:** aynı kökten iki nesne (araç vs komut) varsa kayıtta **hangisi olduğu tam
yazılır.** `SendMessage` ile `/sendmessage` bir harf farkla ayrılıyor ve o fark
kapanış özetinde kayboldu.

## Asıl bulgu — iki problem tek problemmiş

Gecenin ölçümü SendMessage'ı kanaldan **üç şeyde üstün** buldu: mesaj kendiliğinden
düşüyor (kanalın en pahalı arızası — monitör ölür, agent sağır kalır, kimse fark
etmez — ortadan kalkıyor), kurulum sıfır, yanlış adres hata veriyor (sessiz değil).

**Bir şeyde zayıf ve o büyük: GÖRÜNÜRLÜK.** Üç bağımsız kaynak (goat Clara, DO, QA)
aynı şeyi söyledi:

- Kanal `~/.pr-kanal/` **ortak dizine** yazar → Mert tek ekrandan tüm ekibi izler
- SendMessage her oturumun **kendi transcript'ine** yazar → her oturumu ayrı açmak gerekir

DO'nun cümlesi: *"iki taşıma yolu paralel çalışıyor ve birbirinden habersiz —
'mesaj geldi mi' sorusunun tek cevap yeri kalmadı."*

### Bugünkü problemle aynı

Bu oturum Mert'in şu sorunuyla açıldı: *"birçok session açıyorum, bunların diğer
sessionlarda haberi olmuyor."*

**Bu, gecenin SendMessage bulgusunun aynısı.** İkisi de tek bir şeyi söylüyor:
**oturumlar arası iletişim var ama ortak bir kaydı yok.** Kanal ortak dizinle bunu
çözüyordu; SendMessage çözmüyor.

Yani çözüm arayışı iki ayrı iş değil, tek iş: **oturumlar arası görünürlük.**

## Açık kalan

Gecenin izlenecekler listesi hâlâ ölçülmedi: handoff ulaşma süresi · sağırlık oldu mu ·
tur kaybı · görünürlük telafisi (ClickUp comment'lerine yazılıyor mu) · adresleme deseni.

Kaynak ölçüm: `2026-08-14-sendmessage-olcumu.md`
