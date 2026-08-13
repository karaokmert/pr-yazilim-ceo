---
name: project-durum
description: Son kapanış dokümanının adresi ve tek cümlelik durum — her oturum açılışında İLK okunur
metadata:
  type: project
---

**Son iş: `/kanal` komutu canlı testi (egelisaglik, 2026-08-13 19:00–20:02).**

Kapanış: `gunluk/egelisaglik/2026-08-13-kapanis-kanal-testi.md`
Ölçüm: `konular/kanal-iletisim/incelemeler/2026-08-13-kanal-komutu-canli-test.md`

**Test GEÇTİ** — dört adım da çalıştı (merkez yokken durdu, varken kurdu,
namespace korundu, iş çift yönlü aktı). **Beş arıza bulundu, beşi düzeltildi.**

⚠️ **Egelisaglik'te kanal ŞU AN YOK** — defter `[]`, yedi terminal kanalsız.
Yeniden kurulacaksa **önce Clara'ya `/kanal`**.

**Mert'in kararını bekleyen üç şey:**
- **Fabrika betiklerine yazma izni** — `archive.py`'ye onay metni göstermeden
  yazıldı (`CLA-ASK-BEFORE-WRITING-OUT` ihlali). Kalıcı izin mi, her seferinde
  gösterim mi? Yedek: `/tmp/archive.py.yedek`
- **Üç fabrika bulgusu** devir bloğu bekliyor (`setup.py` arayüzü ·
  `STATUS.md` ölü `STATE` alanı · `read.py` imleç sahipliği kontrolü yok)
- **Kayıp mesajlar** — ikinci Clara altı mesajı okudu, imleç ilerledi; arşivde.

Ayrıca 12–13 Ağustos'un sekiz karar bekleyen maddesi hâlâ açık
(1028 yetim memory · "önkoşul dalı" taraması · K1-K6 fabrikaya).
