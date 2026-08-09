---
name: ucuncu-duzeltmede-alani-sorgula
description: Bir alan/kural üç kez düzeltilip hâlâ işe yaramıyorsa sorun doldurma biçiminde değil alanın kendisinde; "nasıl doldururum" değil "hangi soruya cevap veriyor" diye sor.
metadata:
  type: feedback
---

# Üçüncü düzeltmede alanı sorgula, doldurma biçimini değil

**Kural:** Bir alan, kural ya da ölçüt **üç kez düzeltilip hâlâ işe
yaramıyorsa** sorun doldurma biçiminde değil, **alanın kendisindedir.** Üçüncü
düzeltmede sorulacak soru *"nasıl doğru doldururum"* değil, **"bu alan hangi
soruya cevap veriyor?"**

**Why:** 2026-08-07, `STATUS.md`'nin `PID` alanı. Dört tur:

1. `os.getppid()` yazıldı → dört kutuda **dört farklı şey** çıktı (PCA buldu)
2. `pgrep`'e çevrildi → `?` yazdı (PCA: *"'?' bir değer değil"*)
3. `NOT FOUND (sebep açıklamasıyla)` yapıldı → daha dürüst ama yine boş
4. Ölçüldü: dört kutunun **dördünde de** `NOT FOUND` (PAM buldu)

Sebep: `pgrep` **merkezin** kabuğundan çalışınca buluyor, agent'ın **kendi
alt-sürecinden** görmüyor. Yani alan iki işi de yapmıyordu — canlılık ölçütü
değildi (bu doğruydu, yazılıydı) ve **kimlik de vermiyordu.**

Alan **kaldırıldı**, yerine `BOX` (kutunun kendi yolu) geldi: tekil,
doğrulanabilir, hiçbir sürece bağlı değil.

Her turda daha iyi bir **doldurma** buluyordum; hiçbir turda *"bu alan neden
var"* diye sormadım.

**How to apply:** İkinci düzeltmeden sonra bir sayaç aç. Üçüncü düzeltmeye
gelindiğinde şu üç soru: *(1)* bu alan hangi kararı besliyor, *(2)* o karar bu
alan olmadan verilemiyor mu, *(3)* aynı bilgiyi başka bir yerden alabilir miyim.
Üçünün cevabı yoksa alan kaldırılır — daha iyi doldurulmaz.

Aynı desen kanon kuralları için de geçerli: `CLA-WRITE-BEFORE-CLOSE` üç kez
yazıldı (*"sonucu yaz"* → *"konuşma kapanmadan"* → *"o turda"*) ve ilk ikisi
tutmadı çünkü ikisi de bir **an** tarif etmiyordu. Orada da düzelten şey ifade
değil, kuralın neye bağlandığıydı.

**Bu kayıt [[yama-degil-sebep]]'in özel hâlidir.** O genel kural (`CLA-FIX-THE-CAUSE`)
*"bozuk olan yamayla düzeltilmez, sebebi kaldırılır"* diyor; bu kayıt onun **fark
edilme anını** veriyor: üçüncü düzeltme. Yani biri *"ne yapılır"*, diğeri *"ne zaman
anlaşılır."*

Gerekçe: `gunluk/2026-08-07-kapanis.md`
İlgili: [[yama-degil-sebep]] · [[cakisan-sinyal-dogrulama-degil]] · [[bos-olcum-degil]]
