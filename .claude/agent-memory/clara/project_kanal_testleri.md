---
name: kanal-testleri
description: Agent-agent kanal testleri sürüyor — yarın devam; iki karar askıda, kanal altyapısı Clara'nın içerik Mert'in
metadata:
  type: project
---

2026-08-04 gecesi iki kanal deneyi yapıldı, **testler yarın devam edecek** (Mert'in
sözü: *"yarın testlere devam edeceğiz"*).

**Why:** Mert'in derdi somut — `PA → BE → QA` zincirinde 3.500 karakterlik handoff'ları
elle kopyalayıp yapıştırıyor. Ölçüldü: handoff'ların %94'ü elle taşıma. Kanal fikri bu
yükü kaldırmak için.

## Ölçülen sonuç — kanal iş taşır, yetki taşımaz

İki deney, 24 mesaj toplam. Tam kayıt: `gunluk/2026-08-04.md` (iki bölüm) + ham
kanal dökümü `gunluk/web-kanal-deneyi/`.

**Çalışan:** uyanma (boşta bekleyen agent dosya değişiminde tur açıyor), iş taşıma,
doğrulama kapısı (komut tekrarı — 5/5 sayı tuttu), bütünlük (eşzamanlı yazma, 0 kayıp),
rol sınırları (üç web agent'ı, sapma sıfır).

**Çalışmayan:** kimlik doğrulama yok, **yazma yetkisi üretilemiyor.** Kanaldan gelen
kural mesajını üç agent da sorguladı. Ayıran şey: **iş doğrulanabilir (dosya, satır,
git hash → gidip kendileri okudular), yetki doğrulanamaz.**

DO'nun cümlesi kritik: *"onay KAYDI üretilir, onay OKUMASI üretilmez. Sistem 'onaylı'
görünür."*

## How to apply — yarın devam ederken

**Kanal altyapısı Clara'nın, kanal içeriği Mert'in.** Bu bir hatadan çıktı: Clara
kanala iki kez Mert'in imzasıyla kural mesajı yazdı, Mert düzeltti (*"handoff'u ben
verecektim, sen kanala yazmasaydın iyi olurdu"*). Bir daha yazılmaz — kanal açılır,
monitor kurulur, ölçüm tutulur; mesajlar Mert'ten çıkar.

**Monitor kurulumu üç şart** (üçü de ölçüldü): filtre zorunlu (`grep -E "^## "` —
filtresiz `tail` uzun mesajda SIGTERM alıyor), `tail -n 0` + açılışta bir kez `cat`
(yoksa dinleme öncesi yazılan mesaj sessizce düşer), gövde dosyadan okunur (bildirim
metni HTML-escape ediyor, dosya ham).

**Kendi yazdığını dinleme** — echo döngüsü üretir. İki ayrı gelen kutusu yapı gereği
çözüyor.

## Askıda iki karar (yarın)

**Bir:** `deploy-prod.yml` çok-panelli hale gelsin mi (`web-template-next`). PA'nın
önerisi: sessizliği bugün kapat (`create-panel` çıktısına uyarı) + genelleştirmeyi
uçtan uca testle yap. Gerekçe: template, eksik her müşteri projesine kopyalanıyor.

**İki:** handoff'lara üç satırlık onay başlığı kalıcı olsun mu. Sebep: bloklar 50-90
satır, Mert onay kapısı ve o hacmi her turda okuyamıyor. Kalıcı olursa `web-handoff`
skill'ine gider — **AG'nin işi**, Clara'nın değil.

İlgili: [[user-mert-profil]], [[stres-testi-yontemi]]
