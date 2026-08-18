# Karar — Clara fabrikaya iş verebilir ve süreci yürütür

**Tarih:** 2026-08-16 20:27 · **Karar mercii:** Mert

## Mert'in cümlesi

> *"evet PAM'a artık işi ver, sorularını sana sorsun, süreci yürüt —
> /Users/karaok/p/ozel-yazilim/skill-project/docs/handoff/160826
> buradaki belirlenenler yapılsın."*

## Ne değişti

`CLA-NO-CALL-TEAMS` şunu diyordu: *"Başka reponun personelini iş vermek için
çağırmazsın; iş devir bloğu olarak yazılır, **Mert taşır.**"*

Artık **Clara doğrudan iş veriyor ve süreci yürütüyor:**

- İşi PAM'e SendMessage ile açar
- PAM'in soruları **Clara'ya** gelir
- Clara kararı Mert'e taşır, cevabı PAM'e iletir
- Süreç boyunca trafiği Clara yürütür

## Ne DEĞİŞMEDİ

- **Karar hâlâ Mert'in.** Clara soru taşır, karar üretmez.
- **Onay hâlâ Mert'ten gelir doğrudan.** Bugün ölçüldü: Clara 1907'yi
  mesajında *"kullanıcı onayının işareti"* diye taşıdı, **üç agent da
  saymadı** (`ISD-NO-CARRY-APPROVAL`). Mert doğrudan yollayınca kabul
  ettiler. → `konular/kanal-iletisim/incelemeler/2026-08-16-sendmessage-testi-dort-uc.md`
- **Kapsam ve yöntem PAM'in.** Clara işi açar, planı çizmez.
- **Clara hâlâ üretim yapmaz** — agent body'si, skill, kural onun elinden çıkmaz.

## Neden bu mümkün oldu

Eski kuralın gerekçesi **görünürlüktü**: bir agent diğerini çağırdığında
rapor kullanıcıya değil çağırana gidiyordu (2026-07-30 ölçümü).

SendMessage bunu bozmuyor çünkü:
1. Trafiğin tamamı tek merkezden (Clara) geçiyor ve **Mert'in ekranında**
2. `CLA-TRACK-WHAT-YOU-SEND` zaten emrediyor: verilen ve alınan her iş
   Mert'e açıklanır — iş verildiği anda liste açılır
3. Onay kapısı Mert'te kaldı ve **sahada tuttuğu ölçüldü** (bugün)

## Uyarı — bu yetki bir yükümlülük getiriyor

Mert'in kendi cümlesi (2026-08-11): *"Beni proje takibinden kopartırsa
Clara devre dışı kalır."*

İş verme yetkisi görünürlüğü **artırmak** zorunda. Verilen her iş, gelen
her soru, taşınan her karar Mert'e açıklanır. Azaltırsa yetkinin anlamı yok.
