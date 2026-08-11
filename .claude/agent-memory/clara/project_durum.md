---
name: durum
description: İLK BUNU OKU — son kapanış dokümanının adresi ve tek cümlelik durum. Oturum açılışında ilk okunan kayıt.
metadata:
  type: project
---

# Durum

> **`gunluk/` proje bazlı:** `gunluk/ev/` (Clara'nın kendi işi) · `gunluk/fabrika/`
> (fabrika hattı) · `gunluk/{proje}/`. Açılış hook'u her projenin son kapanışını ayrı
> listeler — **yalnız kendi modunun kapanışı okunur.**

## Son kapanış — FABRİKA hattı

**`gunluk/fabrika/2026-08-11-kapanis.md`** ← **bunu oku, çalışmaya oradan başla.**

**Tek cümle:** Fabrika ekibi **`skill-project`'e taşındı** ve OY v8'in **sekiz rolü
düzeltildi** (48 description, on bir commit, push yok) — sıradaki iş **yedi karar
kalemi**, kalem 1'den devam edilecek.

**Destek belgeleri (gerekirse):**
- `gunluk/fabrika/2026-08-11-sabah-brief.md` — **yedi kararın tam metni**
- `gunluk/fabrika/2026-08-10-aksam-tasima-ve-pa-turu.md` — 1.479 satır, gecenin tam izi
- `gunluk/fabrika/2026-08-10-be-karsilastirma-testi.md` — v8 vs FAB, dört tur

## Son kapanış — EV hattı

`gunluk/ev/2026-08-09-kapanis-3.md` (açılış hook'u + `gunluk/` dosya düzeni)

## İlk hareket

**Fabrika modundaysan:** kapanış dokümanını oku, sonra **karar kalemlerini sırayla
sun** — Mert *"grup 2 ve karar noktalarını inceleriz"* dedi. Kalem 1 (`CLAUDE.md`)
sunuldu, cevap alınmadı.

**Yeni iş açma.** Kalan her kalem ya bir **karar** ya bir **saha ölçümü**.

**Push: ON BİR COMMIT BEKLİYOR.** `origin/main` = `3c54b57`. Mert commit onayı verdi
(*"commit onayım var, push yok"*), push onayı ayrı ve alınmadı.

**Fabrika ekibi AÇIK ama durdu** — dört kutu (`pr-agent-*-1402/1403`) + iki BE
(`be-eski-1611`, `be-fab-1728`). Arşivlenmedi. **Monitör oturumla ölür**, yeniden
kurulur.

## ⚠️ İLK MEKANİK İŞ — kapanışta bulundu

**Taşınan `docs/` (90 dosya) ve `team/` (31 dosya) COMMIT'LENMEMİŞ.** Taşıma
commit'i `25e1bf3` yalnız `.claude/` altını kapsıyor — `git add .claude/` denmiş,
gerisi dışarıda kalmış. Diskte var, git'te yok.

PQA taşımayı denetledi ve **doğruydu** (dosyalar taşınmıştı) — ama *"commit'lendi
mi"* sorusu hiç sorulmadı. Denetim kapsamı ile commit kapsamı ayrı şeyler.

## Bu oturumda öğrenilen — kanona aday

**Bayat = yanlış değil.** Bir sayı **üç şekilde** bayatlar: değeri değişir · değeri
kalır · **sorusu ortadan kalkar** (sayı doğru, ölçtüğü problem geçersiz).
Üçüncüsü en sinsisi — sayı doğru görünmeye devam ediyor.

**Yatay kapsam / dikey kapsam.** Yatay *"neyi saydım"* (küme, desen, birim), dikey
*"hangi kuralla saydım"* (ölçüt sürümü). İkincisi canlı işte kritik — kural **tur
ortasında** değişiyor. Bir gecede ölçüt altı kez değişti ve her değişim önceki
ölçümleri sessizce bayattı.

**Çelişki tek elin dikkatinden güçlü.** Dört çelişki, dört farklı kök, hiçbirini tek
el bulmadı. On üç ölçüm vakasının hepsi yakalandı; son üçünde **yakalayan ile yapan
aynı kişiydi.**

**Doğru sonuç yanlış araçtan da çıkabilir** (PAD): *"ölçüm beni yanlış yöne
götürüyordu, metin kurtardı."*

**Ham veri kendi hatasını yakalatıyor** (PCA): ham sayıları yazdığı için yanlış
sınıflandırma görünür oldu; yalnız sınıfı yazsaydı kimse fark etmezdi.

**Bir dosyayı bir kez okumuş olmak, sonraki turda hâlâ okumuş olmak değil** —
**iki dakikalık** bayatlama yetti (PCA, `BHV-OPEN-SOURCE`).

## Clara'nın dört hatası — ve teşhisinin çürütülmesi

Üçlü ölçümü beklenen değerle bozmak · denetim kapısını kendi okumasıyla geçmek ·
adres satırını okumadan iletmek · **ham raporu özetlemek**.

**Dördünü de ekip yakaladı.** Ve *"yavaşlamam gerekiyor"* teşhisini PAM çürüttü:
*"üçü farklı kökten (bilgi türü · rol sınırı · okuma); yavaşlık bir kez bile hata
önlemedi — hepsi DİKKAT değil YAPI sorunuydu."*

Doğru çözümler, üçü de bir **davranış**: ölçüm sonucu devir nesnesi değildir ·
kapıyı bekle, varsayma · `to` alanını oku.

## En ağır kalem — sekiz turun tamamını niteler

**Hiçbir turda SAHA davranışı ölçülmedi** (PCA'nın şerhi, PAM ve PQA onayladı).
Metin ölçümü çalışmayı göstermez. Sekiz tur **dosya ölçütüyle** kapandı —
`agent-project`'te öğrenilen *"dosya üretildi değil sahada açıldı"* uygulanmadı.

## Ölçüldü ama çözülmedi

**Beş saatlik oturum limiti** — zincir 23:08–04:30 durdu, iş kaybı olmadı ama
tekrar olacak. Mert: *"bunu hallederiz sonra."*

**Kanal varsayılanı hâlâ `agent-project`** — repo taşındı, varsayılan taşınmadı.

**Kanal protokolü agent kanonlarında yok** — dördüncü kez ölçüldü.

**`deploy-release` kendine atıf veriyor** (`SKILL.md:121`) — pakette tek vaka.
