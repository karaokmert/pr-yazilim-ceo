# Karar — Clara iletebilir, ama soru sormak için

Tarih: 2026-08-23 · Karar: Mert · Konu: clara

## Mert'in cümlesi

> *"Sen iletebilirsin soru sormak için, iş yaptırma — yapılanı öğren."*

## Neyi çözdü

İki kanon çatışıyordu:

- **Clara kanonu (2026-08-19):** onaylı devir bloğunu `SendMessage` ile Clara iletir.
- **Fabrika kanonu (2026-08-22, `fabrika-is-duzeni`):** birincil yol devir bloğu
  yazmak, **onu kullanıcı taşır**; çağırmayı ve mesajlaşmayı kullanıcı ister.
  Gerekçe ölçülmüş: beş çağrının beşinde de rapor kullanıcıya değil çağırana gitti.

## Karar

**Ayıran şey iletimin YÖNÜ değil, mesajın TÜRÜ.**

| Tür | Clara iletebilir mi |
|---|---|
| **Soru** — ne yapıldı, nasıl duruyor, ne karar verildi | **Evet**, onaysız |
| **Bilgi** — bilinmesi gereken bir şey | **Evet** |
| **İş** — devir bloğu, yapılacak bir şey | **Hayır** — Mert taşır |
| **Onay isteği** | **Hayır** — zaten Mert'in kararı |

Sebep tutuyor: fabrika kanonunun koruduğu şey *"kullanıcının zinciri görmesi"* —
ve zincir **iş** akışında oluşur, soru sormakla değil. Bir soru kimseye iş
başlatmaz, hiçbir kapı açmaz, kimsenin raporunu yanlış yere göndermez.

## Yürürlükteki hâli

`CLA-NO-CALL-TEAMS` daralır: onaylı bir **iş** bloğunu Clara artık iletmez —
2026-08-19 kararının o kısmı geri alındı. Soru ve bilgi iletimi serbest kalır.

Dönen cevap **ham hâliyle ekrana basılır**; Clara'nın yorumu ayrı paragraf olur.
`CLA-TRACK-WHAT-YOU-SEND` yürürlükte.
