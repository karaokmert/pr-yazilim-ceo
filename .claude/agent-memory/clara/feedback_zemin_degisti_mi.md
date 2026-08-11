---
name: zemin-degisti-mi
description: Bir agent'a soru sormadan önce "cevabı elimde var mı" süzgecinden geçir — aynı zeminde tekrar ölçüm gürültü, zemin değişiminde zorunlu (2026-08-11)
metadata:
  type: feedback
---

Bir agent'a soru sormadan önce süzgeç: **bu sorunun cevabı elimde var mı?** Varsa soru
değil, **bağlam** olarak taşınır.

**Why:** 2026-08-11'de Goat'ta QA'ya 12 commit'lik kuyruk incelemesi verildi ve **altı
soru** soruldu. Mert kesti: *"QA her commiti inceledikten sonra neden bir daha inceleme
yapıyor ki?"*

Ölçüldü: altı sorunun **dördü zaten cevaplanmıştı** — ikisi QA'nın kendi hükmüydü
(doküman yerleri, `FE-TEST-BORC` yeri), biri QA'nın kendi bulgusuydu (1A↔1B kilidi), biri
bilinen eski arızaydı (`web_site` CI). Gerçekten yeni olan **iki** soruydu: iki commit'in
aynı dosyada çakışması, ve dört yerde aynı desenin tutarlılığı.

QA kendi payını da kabul etti ve kural çıkardı: *"Kendi onayımı tekrar doğrulamak denetim
değil."* Tekrar ölçümün iki maliyeti: **rapor şişiyor** ve **gerçek bulgu kalabalıkta
kayboluyor.**

**How to apply — ayıran ölçüt ZEMİN:**

- **Aynı zeminde tekrar ölçüm = gürültü.** Onay verilmiş, hiçbir dayanağı değişmemiş, yine
  soruluyor → sorma, bağlam olarak taşı.
- **Zemin değiştiyse tekrar ölçüm ZORUNLU.** Onayın dayandığı bir varsayım çürüdüyse eski
  hüküm taşınmaz.

Aynı gün her ikisinin de örneği çıktı. Meşru olan: QA 1A'yı onayladı, **sonra** "zaman
geri sarma" bulgusu çıktı — o bulgu onayın zeminini sorgulattı, QA 1A'yı geriye dönük
yeniden ölçtü (temiz çıktı). Gürültü olan: doküman yerlerini ikinci kez ölçmek.

⚠️ **Ve bu kuralın kardeşi bir yasağı var:** bir agent'ın kendi bulgusunu ona soru olarak
geri sormak. 1A↔1B kilidini QA bulmuştu; Clara onu *"hâlâ geçerli mi?"* diye geri sordu.
Bulgu zaten kayıtta — soru değil, **doğrulanmış bilgi.**

Bkz. [[iddiayi-tasima-olc]] — tersi durum: agent'ın *eylem* iddiası ölçülür, *bulgusu*
tekrar sorulmaz.
Bkz. [[akisi-bloklamayin]] — gereksiz soru akışı da yavaşlatır.
