---
name: karsilastirma-ayni-bicimde
description: İki şey karşılaştırılacaksa ikisi de AYNI biçimde ölçülür — kısaltılmış ölçümü tam değerle karşılaştırmak sessiz yanlış üretir
metadata:
  type: feedback
---

**Bir karşılaştırma yapılacaksa iki taraf da AYNI biçimde ölçülür.** Tam yol
tam yolla, ad adla. Bir tarafı kısaltıp diğeriyle karşılaştırmak, aradaki
farkı **kafadan tamamlamayı** zorunlu kılar — ve o tamamlama bir ölçüm değil
tahmindir.

**Why:** ölçüldü 2026-08-13, **aynı oturumda iki kez arka arkaya.**

`basename` bir **ad** sorusuna cevap verir, bir **yol** sorusuna değil.
Ben yol sorusu sordum, `basename` kullandım, çıkan `egelisaglik` adını
kafamda `/Users/karaok/p/egelisaglik` diye tamamladım. Gerçek yol
`/Users/karaok/p/ozel-yazilim/egelisaglik`'ti.

Bedeli iki yanlış iddia oldu:
- Defterdeki `repo` alanını **"agent uydurmuş"** diye raporladım. Alan
  doğruydu; uyduran bendim.
- Beş agent'ı "egelisaglik'te" saydım. Tam yolla ölçünce **egelisaglik'te
  altı**, goat'ta altı, skill-project'te dört, CEO'da dört çıktı — üç ayrı
  projeyi tek isim altında toplamışım.

Ve tehlikesi şu: **kısaltılmış ölçüm doğru görünür.** `egelisaglik` gerçekten
o klasörün adı — yanlış olan ölçüm değil, ölçümün cevapladığı soru.

**How to apply:** karşılaştırma kuracaksam önce sorarım — *bu iki değer aynı
biçimde mi?* Değilse ya ikisini de tam hâline getiririm ya da ikisini de
kısaltırım. **Farkı kafadan kapatmam.**

Ayıran soru: **bu değeri gördüm mü, yoksa gördüğüm parçadan mı tamamladım?**

İlgili: [[feedback_aracin_ne_olctugu]] · [[feedback_olcum_yerine_yorum]]
