# Karar — Clara gövdesi yeniden yazıldı, eskisi -ex olarak bırakıldı

Tarih: 2026-08-23 · Karar: Mert · Konu: clara

## Mert'in cümlesi

> *"Clara body'i yeniden yaz, eskiyi -ex olarak bırak."*
> *"Senin kim olduğunu ne işe yaradığını netleyelim."*

## Neden

Fabrika (`fabrika-v2`) elle yeniden kuruldu ve yasak düzeni kaldırıldı. Fabrikanın
gövdeleri okunduğunda iki ilke çıktı ve Clara gövdesi ikisini de ihlal ediyordu:

**1. Gövde bir karakter tanımıdır, bir sözleşme değil.** FPD gövdesinin kendi
cümlesi: *"Sözleşme okuyan agent temkinli olur, karakter okuyan agent kendisi gibi
davranır."* Clara gövdesi dokuz numaralı kimlikli kural (`CLA-*`) taşıyordu — sözleşme
biçimi.

**2. Yöntem skill'e aittir, gövdeye değil.** Clara gövdesi hem kim olduğunu hem
yöntemi taşıyordu. Somut ölçüm: gövde *"→ `arama-disiplini` skill'i"* diye yönlendirip
sonra aynı konuyu kendisi anlatıyordu.

## Ne taşındı

| İçerik | Nereye |
|---|---|
| Kayıt/konu klasörü düzeni, ne zaman silinir | `hafiza-duzeni` |
| Arama yöntemi (grep/vektör) | `arama-disiplini` (zaten vardı — tekrar kaldırıldı) |
| Plan → görev listesi → koşum | `oturum-duzeni` |
| Dokuz `CLA-*` kuralı | karakter cümlesine dönüştü, kimlikler kalktı |

## Ne ALINMADI — gerekçesiyle

**Kural kimlikleri (`CLA-TRACK-WHAT-YOU-SEND` vb.) alınmadı.** Kimlik bir sözleşme
işaretidir ve fabrikanın kaldırdığı şey tam bu. Kuralların *içeriği* korundu, kimliği
değil. Bir kurala atıf gerekirse başlığıyla anılır.

**Ölçüm anlatılarının tam metni alınmadı.** *"Ölçüldü: beş çağrıda beş rapor çağırana
gitti"* gibi tek cümlelik hâli kaldı; sayfa uzunluğundaki vaka anlatıları `clara-ex.md`
içinde duruyor. Sebep: gövde her oturumda yükleniyor, kanıt her okumada taşınmamalı.

**Kanal sistemi bölümü alınmadı.** Emekli (2026-08-19), yerine `sendmessage-akisi`
geçti. Gövdede yer tutması gereksizdi.

## Sınandı

Bağlamsız bir okuyucuya yalnız yeni gövde verildi, altı durum soruldu (iş devri, kural
ihlali, uzunluk ölçümü, yarım iş kapanışı, "sorumluluğu alıyorum" istisnası, soru
sorma serbestliği). **Altısında da doğru davranış, gerekçesiyle geldi.**

Kritik iki test: *"ben onaylıyorum, sorumluluğu alıyorum"* denince onay kapısını
atlamadı; kural ihlalinde *"kuralı çiğnedi mi"* değil *"kural elinde miydi"* dedi.

## Eskisi nerede

`.claude/agents/clara-ex.md` — frontmatter `clara-ex-emekli` yapıldı (agent olarak
yüklenmesin), başına emekli notu ve gerekçe yazıldı. Yeni gövdeye taşınmayan bir satır
arandığında bakılacak yer orası.
