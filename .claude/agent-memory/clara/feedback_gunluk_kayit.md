---
name: gunluk-kayit
description: Bulgu günlüğe yazılır (gunluk/{tarih}.md), ayrı dosya yalnız karar/fikir/referans için — Mert dosya enflasyonundan şikâyet etti
metadata:
  type: feedback
---

Ölçüm ve bulgu **`gunluk/{tarih}.md`** dosyasına yazılır — her bulgu bir başlık, aynı
gün aynı dosyaya eklenir. Klasör açma, `HARITA.md` satırı yazma, ayrı dosya kurma yok.

Ayrı dosya **yalnız üç şey için**: karar (`kararlar/`), olgunlaşmış fikir
(`fikirler/{konu}/`), aylarca dönülecek referans (`projeler/`, `incelemeler/{konu}/`).
Ortak ölçüt: iki ay sonra **adıyla aranacak** mı?

**Dayanak:** Mert'in cümleleri, 2026-08-03/04 oturumu — *"çok gereksiz dosya işi
yapıyoruz"*, *"memory'i aktif kullan, her şeyi her an dosyaya yazmaya çalışma"*.

**Why:** O oturumda 11 ayrı dosya açıldı. Her ölçüm bir dosyayı hak etmiyor; çoğu bir
satırı hak ediyor. Ve dosya açmanın maliyeti görünmez: klasör + dosya + harita satırı
+ commit = dört adım, tek bulgu için.

Ama bulgular **memory'ye de gitmiyor** — ölçüldü ve sebebi mekanik: memory dosyaları
otomatik yüklenmiyor, indeks satırı dışında hiçbiri context'e girmiyor. 8 kayıtta
yönetilebilir, 50 kayıtta hangisini açacağımı bilemem. Dosya grep'lenebilir, memory
grep'lenmez (pratikte açılmaz).

**Ayıran soru değişti.** Eskiden *"Mert'in görmesi gerekiyor mu"* idi; Mert bunu
çürüttü: *"memory'i ben okumuyorum ama dosyayı da okumuyorum, bu senin kayıt
defterin."* Yeni soru: **"bu ne kadar birikecek ve nasıl bulunacak?"**

**How to apply:** Bir ölçüm bittiğinde günlüğe başlık ekle, geç. Karar verildiğinde
`kararlar/` altına yaz. Bir konuya haftalarca dönülecekse ayrı dosya aç. Şüphede
kalırsan günlüğe yaz — günlükten ayrı dosyaya taşımak kolay, tersi zor.

İlgili: [[cevap-uzunlugu-ve-karar-alma]], [[hatirladigim-kayittir]]
