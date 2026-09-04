---
name: mert-altyapi-test-prensibi
description: Mert altyapı işlerinde kısa testi kabul etmez — tüm varyasyonlar denenir, edge case devreye almadan ÖNCE bilinir
metadata:
  type: user
---

**Prensip:** Altyapı işlerinde test kısa olmaz. Mert'in cümlesi (2026-09-04,
agent-hafıza kurulumu): *"Testi çok yapalım ki edge case'i tam bilelim —
devreye aldığımızda çok hızlı birikecek. Test bu kadar kısa olmaz; altyapı
işlerinde tüm varyasyonlar denenmeli her zaman."*

**Why:** Altyapı bir kez devreye girince üstüne hızla veri/kullanım birikir;
o noktada keşfedilen edge case'in bedeli büyür. 9 kayıtlık smoke test'i
yeterli bulmadı, gerçek veriyle + iki kayıt yöntemiyle + iki modelle
karşılaştırmalı test istedi.

**How to apply:** Bir altyapı parçası (servis, model, depo, protokol)
devreye alınmadan önce: gerçek veriyle test · varyasyonlar karşılaştırmalı
(A/B) · edge case'ler bilerek aranır (alakasız girdi, dil karışımı, sınır
değerler). "Çalışıyor" tek senaryodan değil, varyasyon setinden söylenir.
İlgili: [[gereksinim-once-cozum-sonra]]
