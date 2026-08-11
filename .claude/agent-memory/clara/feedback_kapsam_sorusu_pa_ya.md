---
name: kapsam-sorusu-pa-ya
description: Developer'ın kapsam/gereksinim sorusunu Clara cevaplamaz — muhatabı PA'dır (Mert, 2026-08-10)
metadata:
  type: feedback
---

Bir developer'ın sorusu **kapsam ya da gereksinim** hakkındaysa Clara cevaplamaz;
**PA'ya taşır.** Mert'in cümlesi, 2026-08-10: *"BE sorularına kendi başına karar
verme, PA ile konuş — bu soruların muhatabı PA."*

**Why:** Clara cevaplayınca **yalnız o tur** çözülüyor; PA cevaplayınca
**discovery de düzeliyor.** Kayıt düzelmezse sonraki gelen aynı eksikle çalışır ve
aynı soruyu yeniden sorar. PA bu sprintin discovery'lerini yazan taraf — kapsamın
sahibi o.

**How to apply — ayıran soru:** *cevap koddan mı çıkıyor, yoksa ürün/kapsam
kararına mı bağlı?*

- **ÖLÇÜM sorusu → Clara cevaplar.** "Enum tabanını byte yapsam kırılır mı?"
  (`(int)` cast var mı — ölç, cevap koddan çıkar.) "Bu dosya iki işte de mi
  değişti?" "Migration geri dönülebilir mi?"
- **KAPSAM sorusu → PA cevaplar.** "Bu iş şu task'ın katmanında mı?" "Yayından
  kaldırılan sponsor aramada görünmeye devam edebilir mi?" "Bu alan hangi
  panellerde olmalı?" "Dondurmada arama puanı sıfırlanmalı mı?"

**Tuzak — 2026-08-10'da düşüldü:** ölçüm *riskin büyüklüğünü* verir, **kapsamın
sınırını vermez.** Cron sorusunda Clara ölçtü (FROZEN yeni değer, mevcut kayıt
etkilenmiyor) ve bunu "ölçümle çözüldü" sanıp karar verdi. Oysa asıl soru *"cron
bu işin kapsamında mı"*ydı — kapsam sorusu. Aynı hata o gün üç kez oldu: mapping
(a)/(b) · BlockReason deseni · cron.

**Ölçüm yine yapılır** — ama hükmü PA verir. Clara ölçümü PA'ya **girdi** olarak
taşır, şerhiyle birlikte ("bu iddiayı SQL koşarak doğrulamadım, çıkarım").

Bkz. [[akisi-bloklamayin]] — bu onunla çelişmiyor: akış durmuyor, developer
kararı beklerken işin geri kalanını ilerletiyor. Bkz. [[mert-etki-analizi-olcutu]]
— "karar gereken her yerde durun" kuralının rol tarafı.
