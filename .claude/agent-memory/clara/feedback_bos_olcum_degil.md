---
name: bos-olcum-degil
description: "Boş" bir ölçüm değil, okunmamış bir kutunun görünümü. Bir kaynağın boş görünmesi ile onu okumamış olmak ayrı şeyler; imleç/kayıt tutmadan "yok" denmez.
metadata:
  type: feedback
---

# "Boş" bir ölçüm değil

**Kural:** Bir kaynağın *"boş"* görünmesi ile onu **okumamış** olmak ayrı
şeylerdir. Kayıt tutmadan (imleç, kanıt, ne zaman baktığın) *"yok"* denmez.

**Why:** 2026-08-07. Dört agent'ın outbox'ını `ls` ile taradım ve PQA'nın
kutusu boş göründü; *"outbox'ın boş, neredesin"* diye sordum. PQA'nın raporu
**dokuz dakika önce** yazılmıştı (9140 byte). Sebebi de kendisi buldu: kutunun
`.cursor` dosyası **hiç oluşmamıştı**, yani o kutuyu bir kez bile imleçle
okumamıştım.

Onun cümlesi: *"'Outbox'in bos' bir olcum degil, okunmamis bir kutunun
gorunumu."*

Aynı hatayı aynı gün ikinci kez o da yaşadı: kendi arşivlenmiş kutusunu
aradı, bulamadı, *"kayboldu"* sandı — iki arşiv dizini yan yana yaşıyordu
(`arsiv/` ve `archive/`) ve o yalnız birine bakmıştı.

**How to apply:** Bir şeyin yokluğunu bildirmeden önce üç soru: *(1)* nereye
baktım, *(2)* o yerin tamamı mı yoksa bir kısmı mı, *(3)* baktığımın kaydı var
mı — yoksa "baktım" bir hatıra, ölçüm değil.

Özellikle **yokluk iddiaları** için geçerli: "mesaj gelmedi", "kayıt yok",
"dosya bulunamadı", "agent cevap vermedi". Bunların hepsi *"ben görmedim"*
ile karışabiliyor ve ikisi farklı şey.

Ve ilgili mekanik: `CLA-WAIT-FOR-THE-END` — bitiş sinyali gelmeden bakılan bir
sonuç da aynı yanılgıyı üretiyor.

Gerekçe: `gunluk/2026-08-07-kapanis.md`
İlgili: [[cakisan-sinyal-dogrulama-degil]] · [[olcum-yerine-yorum]] · [[olcum-kaynaga-git]]
