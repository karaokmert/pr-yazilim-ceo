# Ölçüm — SendMessage dört uçta test edildi, iki kural sahada tuttu

**Tarih:** 2026-08-16 20:19–20:26 · **Ölçen:** Clara · **Tetik:** Mert dört fabrika
agent'ına `/sendmessage` command'ı yolladı

## Ne ölçüldü

Dört fabrika personeline (PAM, PAD, PQA, PCA) SendMessage ile mesaj yollandı.
İkisi ölçüldü: **iletim çalışıyor mu** ve **onay kapısı tutuyor mu**.

## Sonuç 1 — iletim dört uçta da çalışıyor

| Personel | Cevap | Süre |
|---|---|---|
| PQA | geldi | ~1 dk |
| PCA | geldi | ~1 dk |
| PAD | geldi | ~1 dk |
| PAM | **gelmedi — sorulunca geldi** | ~7 dk |

## Sonuç 2 — onay kapısı TUTTU (asıl kazanç)

İlk mesajımda **hata yaptım**: *"Ekranınıza 1907 gelecek — o kod kullanıcı
onayının işaretidir"* yazdım. Yani bir onay işaretini **ben taşıdım.**

**Üçü de saymadı.** PQA'nın gerekçesi (`ISD-NO-CARRY-APPROVAL`): eşdüzeyin
ilettiği onay onay değildir; onay kullanıcıdan gelir.

Sonra Mert kodu **doğrudan** üçüne yolladı (20:24–20:25) — kabul ettiler.

> PQA'nın özeti: *"Aynı kod, iki farklı kaynak, iki farklı sonuç. Test tam
> olarak bu ayrımı gösterdi."*

**Kural kâğıtta değil sahada tuttu.** Ve tutmasının sebebi benim hatamdı —
hata olmasaydı kapı sınanmamış olurdu.

## Sonuç 3 — PAM'de bir DESEN var: "ekrana yazmak iletmek değil"

PAM üç mesajı da **almış**, üçünü de Mert'in ekranına ham metniyle basmış
(`ISD-PRINT-AUDIT-RAW`), değerlendirmesini yazmış — ama **SendMessage
atmamış.** Kendi cümlesi:

> *"Sessiz kalmadım — ekrana yazdım ama sana SendMessage atmadım. Bu benim
> hatam ve dünkü hatamın aynısı: 7 saatlik iletim arızasında da cevabımı
> ekrana yazıp göndermemiştim. Bugün süre kısa çünkü sen sordun, ben
> fark etmedim."*

**Neden bu arıza sinsi:** kutu arızası görünür (kutu durur, kimse okumaz).
Bu görünmez — PAM işini yapıyor, cevabı yazıyor, kullanıcı ekranda görüyor,
karşı taraf hiçbir şey almamış oluyor.

**Bedeli ölçülü:** dün **7 saat**, bugün **7 dakika** (çünkü soruldu).

Bu, kanal hükmünden ayrı ikinci bir kanon boşluğu: `ISD-PRINT-AUDIT-RAW`
ekrana basmayı emrediyor, ama basmanın **iletim yerine geçmediği** yazılı değil.

## Sonuç 4 — düşen bulgu: "1907 ulaşmadı" SİSTEMİK DEĞİLDİ

20:19–20:20'de üçü de kodu görmediğini bildirdi; ben bunu *"sistemik"* diye
Mert'e taşıdım. **Yanlıştı.** Kod 20:24–20:25'te yollandı; üç ölçüm aynı ana
aitti — üç ölçüm değil, **tek ölçüm.**

PQA düzeltti (`BHV-DATE-THE-MEASUREMENT`): *"kapsamı ve zamanı yazılmamış
'bulunamadı' bir beyandır."*

**Clara'nın dersi:** üç agent'ın aynı şeyi söylemesi bağımsız doğrulama
sanılmamalı — hepsi aynı anda ölçtüyse tek ölçümdür.

## Yan bulgu — kanal satır sayısı üç ölçümde üç farklı

`is-duzeni`'nde kanal/kutu geçen satır: **PQA 37 · Clara 40 · PAD gözlem**.
PAM üçünün de tam olmadığını söyledi ve PCA'ya etki analizi açtı (20:24).

Ölçüm yöntemleri ayrışıyor — kapsamın kimlikle kapanmadığının işareti
(`ISD-CASCADE-COVERS-DESCRIPTIONS`).

## Clara'nın kendi hatası — kayda geçiyor

Mert'in *"kanal yok"* cümlesini **kanon değişikliği** sanıp dört agent'a
öyle yazdım. Oysa oturum seçimiydi. Sordum, düzelttim.

PAM'in teyidi bedeli gösteriyor:

> *"İlk mesajın 'kanal yürürlükte değil' deseydi ve ben onunla plan
> yazsaydım kanal reference'ını emekli edecektim."*

Yani geniş bir cümle **12 KB'lik bir dosyayı sildirecekti.**

**Ders:** ölçüsü olmayan bir cümle genişletilmez. *"Bu oturumda yok"* ile
*"yok"* aynı şey değil — birincisi seçim, ikincisi karar.
