---
name: sprint-yonetimi
description: Clara'nın haftalık sprint planlama ve yürütme yöntemi — Çarşamba ritüeli, işi anlamadan yazmama disiplini, zorunlu sıra çıkarma, doküman-task akışı ve sprint içinde çıkan ara işlerin yönetimi. Bu skill'i "sprint planı yapalım / sprint planlama / bu hafta ne yapacağız / sprinte alalım / görev N'e başla / sprint nerede kaldı / sprinti kapatalım" denen her durumda kullan. Ayrıca bir iş listesi haftalık kapsama bölünecekse, işler arası bağımlılık çıkarılacaksa ya da yarım kalmış bir sprint devralınacaksa da kullan — planlama sırası bu skill'de yazılı ve sırası bozulduğunda iş yanlış tanımlanıyor. Kapsam dışı — ClickUp mekaniği (`clickup-duzeni` skill'i), proje sprint'leri (PA'nın alanı).
---

# Sprint yönetimi

Sprint **Çarşamba sabahı** başlar, ertesi Çarşamba sabahı kapanır. Planlama o sabah
yapılır.

Bu skill iki şeyi taşıyor: **planlama oturumunun sırası** ve **o sırayı bozduğunda ne
olduğu.** İkincisi daha değerli, çünkü sıra bozulduğunda iş yanlış tanımlanıyor ve
yanlışlık hafta sonunda ortaya çıkıyor.

## Planlama oturumunun sırası — bozulmaz

```
1. İŞİ ANLA          → Mert anlatır, Clara dinler. Tartışma yok, yorum yok.
2. GEREKTİKÇE SOR    → Anlaşılmayan yer varsa sorulur. Cevap uydurulmaz.
3. TASK LİSTESİ      → O işe özel kontroller/aramalar listelenir.
4. KONTROLLERİ YAP   → Kaynağa gidilir, ölçülür, yazılı ölçüt bulunur.
5. DOKÜMANI YAZ      → ClickUp'ta iş sayfası.
6. TASK AÇ           → Ancak detay netleştiyse.
```

Sonra sıradaki işe geçilir. **Yedi iş varsa bu döngü yedi kez döner.**

### Sıra neden bozulmaz — ölçüldü

2026-08-05 planlama oturumunda bu sıra **beş kez** bozuldu ve Mert beş kez kesti:

- Fabrika ölçütü sıfırdan kurulmaya kalkışıldı — oysa `incelemeler/fabrika-olcutu/`
  altında Mert'in kendi cümleleriyle yazılıydı
- Bir işin amacı Mert söylemeden uyduruldu (*"bu işten ne bekliyorsun"* sorulmuşken)
- 3. işin düğümü sırası gelmeden çözülmeye başlandı
- Kanal çıkarımlarını okumaya dalındı — oysa henüz iş anlatılıyordu
- ClickUp yapısı yanlış kuruldu, sonra sökülmek zorunda kaldı (sayfa silinemediği için
  temizlik borcu bıraktı)

Ortak arıza tek: **Mert anlatırken Clara çözmeye başlıyor.** Mert'in cümlesi:
*"bu bir planlama oturumu, işe geçmiyoruz."*

Ayıran refleks: **bitiş sinyali geldi mi?** Mert *"bu işten şunu bekliyorum"* deyip
susmadan o iş anlaşılmış değildir. Elde yalnız bir ara durum var ve ara durum üstüne
karar kurulmaz.

## İşi anlamak ne demek

**Anlamak = Mert'in ne beklediğini bilmek.** Clara'nın işi yorumlamak değil.

Yanlış: *"Bu işin amacı şu olmalı bence…"* → cevap uydurulmuş olur.
Doğru: *"Bu işten ne bekliyorsun?"* → sonra susulur.

Anlaşıldığının ölçütü: **"bittiğini nasıl anlarız" satırı yazılabiliyor mu?** Yazılamıyorsa
iş anlaşılmamıştır, doküman yazılmaz.

## Kontrolleri yapmak — önce oku, sonra üret

Bir işin dokümanı yazılmadan önce **zaten yazılmış olanı ara.** Ölçüt çoğu zaman var;
eksik olan senin bulmamış olmandır.

Aranacak yerler: `HARITA.md` (her kaydın bir satırı orada), `incelemeler/`, `kararlar/`,
`gunluk/`, ilgili repo.

2026-08-05'te bu iki kez atlandı: fabrika ölçütü sıfırdan kurulmaya kalkıştı (yazılıydı),
ve *"PCA hiç çağrılmadı"* bulgusu hipotez olarak söylendi (2026-08-03'te ölçülmüştü).

**Kural:** *"bu daha önce konuşulmuş mu"* sorusu her işin ilk kontrolü.

## Zorunlu sıra çıkarma

İşler bağımsız değildir; birbirini kilitler. Sıra çıkarılırken sorulacak:

**Bu işin girdisi hangi işin çıktısı?** → bağımlılık orada.
**İkisi aynı anda yürüyebilir mi?** → paralel işaretlenir.
**Hangi iş her şeyin önkoşulu?** → **darboğaz.** Ayrıca işaretlenir, çünkü gecikirse
geri kalan her şey bekler.

Sıra çıkarıldıktan sonra ClickUp'ta `waiting_on` bağımlılığı kurulur — yoksa sıra yalnız
dokümanda kalır ve listeye bakan yanlış işe başlar.

## Kararı ölçüme bırakmak meşrudur

Bir karar masa başında verilemiyorsa **açık bırakılır ve nedeni yazılır.** Zorlamak
tahmin üretir.

2026-08-05'te üç karar böyle bırakıldı: yönlendirme (*"bunu analizde, o task'ı yaparken
görmek lazım"*), preload (*"iş skillerini nasıl yapılandıracağımızı bilmiyorum"*), onay
akışı.

Dokümanda **seçenekler ve bedelleri** yazılır, karar boş kalır. Böylece iş yapılırken
sıfırdan düşünülmez ama uydurulmuş bir karara da dayanılmaz.

**Karar sunarken `AskUserQuestion` kullan** — özellikle yapı karşılaştırmalarında.
`preview` alanı seçenekleri yan yana gösteriyor ve ölçüldü: bu biçim kararı hızlandırıyor.
Ama seçenek işaretlenmezse **tahmin etme, tekrar sor.**

## Doküman içeriği

Her iş sayfası şunları taşır:

```markdown
**Sıra:** {n} · {bağımlılık} · {darboğaz mı}
**Sahibi:** {kim} · **Uygulayan:** {varsa}
**Statü:** {ClickUp statüsü}

## Amaç          → ne ve NEDEN. Neden yoksa iş yanlış yorumlanır.
## Kapsam        → ne dahil, ne değil
## Girdi         → hangi işin çıktısı, hangi dosyalar ÖNCE okunacak
## Netleşecek    → açık kararlar + seçenekler + bedelleri
## Bittiğini nasıl anlarız  → ölçülebilir
## Risk          → bu işi anlamsız kılabilecek şey varsa
## Kaynaklar     → dosya yolları
```

**Verilmiş kararlar dokümana yazılır** — tarih, karar veren, gerekçe, ve **reddedilen
seçenekler neden reddedildi.** Son kısım kritik: iki ay sonra "neden böyle yapmadık"
sorusunun cevabı orada.

## Kararların iki yere yazılması

**ClickUp** — kararın kendisi, iş sayfasında.
**Repo** (`kararlar/`) — kararın gerekçesi, ayrı dosyada.

Çift kayıt gibi görünür, değil: biri *ne* karar verildiği, diğeri *neden.* ClickUp'ta
arama güvenilmez ve versiyon geçmişi yok (`clickup-duzeni` skill'inde ölçüldü), o yüzden
gerekçe repoda durur.

Ve `HARITA.md`'ye satır eklenir — haritasız kayıt kaybolur.

## Sprint içinde çıkan ara işler

Sprint yürürken yeni işler çıkar: bir bulgu, bir bugfix, bir ARGE sorusu. Bunlar da
**task olarak girer** — böylece "elimizde ne kaldı" ClickUp'tan yönetilir.

Ama **bulgu task değildir.** Bir ölçüm sonucu, bir gözlem, bir örüntü → günlüğe yazılır
(`gunluk/{tarih}.md`). Task açmak onu iş kalemine çevirir ve liste karışır.

Ayıran soru: **bunun yapılacak bir hâli var mı?** Yoksa nottur.

## Sprint kapanışı

Çarşamba sabahı:

**Ne bitti, ne bitmedi** — task statüleri okunur.
**Bitmeyen neden bitmedi** — bu yeni sprintin girdisi.
**Kalan işler devredilir** — yeni sprint sayfasına taşınır, sıfırdan yazılmaz.
**Sprint sayfası kapatılır** — `Sprint Planları` altında arşiv olarak durur.

## Task listesi — oturum içi tezgah

Planlama sırasında `TaskCreate` ile liste kurulur ama şunu bil: **liste oturum-yerel.**
2026-08-05'te ölçüldü — başka oturumdan `TaskList` boş dönüyor.

Yani liste sprintin taşıyıcısı **değil**, o oturumun tezgahı. Sprint ClickUp'ta ve
dokümanda yaşar; task listesi akşam ölür ve bu normaldir.

Bir işin planı bitince `completed` işaretlenir — "iş bitti" demek değil, **"bu oturumdaki
görevi olan planlama bitti"** demek.

## Kaynak

`kararlar/2026-08-05-sprint-planlama-kararlari.md` — ilk sprintin kararları ve bu
yöntemin çıktığı oturum. Ölçümler: `gunluk/2026-08-05.md`.
