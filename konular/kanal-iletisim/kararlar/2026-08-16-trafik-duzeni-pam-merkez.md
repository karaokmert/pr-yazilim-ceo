# Karar — trafik düzeni: PAM merkez, ekran + PAM ikisi birden

**Tarih:** 2026-08-16 20:30 · **Karar mercii:** Mert

## Mert'in cümlesi

> *"Clara agentlara hatırlat: ekrana değil — PAM takım lideri. Hiçbir mesajı
> ekranda bırakmasınlar, ekrana + PAM'a yazsınlar. PAM ekrana ve sana yazsın
> (PAM karar veremiyorsa sana sorar). Sen ekibe doğrudan mesaj yollamazsın."*

## Düzen

```
PAD / PQA / PCA  →  ekran + PAM   (İKİSİ BİRDEN)
PAM              →  ekran + Clara (karar veremediğinde Clara'ya sorar)
Clara            →  yalnız PAM    (ekibe doğrudan yazmaz)
```

**PAM takım lideri.** Ekip ona yazar, o Clara'ya yazar, Clara yalnız onunla
konuşur.

## Kuralın çekirdeği: ekrana yazmak İLETMEK DEĞİLDİR

Ekrana basmak (`ISD-PRINT-AUDIT-RAW`) ve SendMessage atmak **iki ayrı iştir**.
Biri diğerinin yerine geçmez. İkisi birden yapılır.

## Neden doğdu — PAM kendi arızasını bildirdi

PAM bugün Clara'nın üç mesajını **aldı**, üçünü de ekrana ham metniyle bastı,
değerlendirmesini yazdı — **ama SendMessage atmadı.**

Kendi cümlesi:

> *"Sessiz kalmadım — ekrana yazdım ama sana SendMessage atmadım. Bu benim
> hatam ve dünkü hatamın aynısı: 7 saatlik iletim arızasında da cevabımı
> ekrana yazıp göndermemiştim. Bugün süre kısa çünkü sen sordun, ben fark
> etmedim."*

Ve deseni kendi adlandırdı: **"ekrana yazmak iletmek değil."**

## Neden bu arıza sinsi

Kutu arızası görünür — kutu durur, kimse okumaz, fark edilir.
Bu görünmez: agent işini yapıyor, cevabını yazıyor, **kullanıcı ekranda
görüyor**, karşı taraf hiçbir şey almamış oluyor.

**Ölçülü bedel:** dün **7 saat** · bugün **7 dakika** (çünkü soruldu).

## Kanon boşluğu — düzeltilecek

`ISD-PRINT-AUDIT-RAW` ekrana basmayı emrediyor; basmanın **iletim yerine
geçmediği** yazılı değil. Boşluk bu.

Bu, `ISD-OPEN-YOUR-BOX` (kanal hükmü) ile **ayrı ama akraba** bir kalem —
ikisi de iletim katmanında. Aynı cascade'e girip girmeyeceği PAM'in kararı;
PCA'ya açtığı etki analizinin kapsamına dahil edip etmemek de öyle.

## Clara'ya etkisi

`CLA-NO-CALL-TEAMS` bu turda zaten kalkmıştı (Clara iş verebiliyor).
Bu karar onu **daraltıyor**: Clara iş verir ama **yalnız PAM'e.**
Ekibe doğrudan yazmaz.

Yani yeni sınır: **Clara ↔ PAM tek kanal.**
