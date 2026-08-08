---
name: durum
description: İLK BUNU OKU — son kapanış dokümanının adresi ve tek cümlelik durum. Oturum açılışında ilk okunan kayıt.
metadata:
  type: project
---

# Durum

**Son kapanış:** `gunluk/2026-08-08-kapanis.md` — oku, çalışmaya başlayabilirsin.

**Tek cümlede:** Fabrika kanonunun sekiz maddelik denetimi tamamlandı ve **push
edildi** — 27 commit, `origin/main` = `89d131f`, kanon 123→131 kural. Davranış
testinde dört rol de geçti (16/16).

## Şu an nerede

**Oturum kapandı, iş bitti.** Yarım kalan yok; üç iş zinciri de denetimden geçti.

Dört fabrika agent'ına kapanış bildirimi gitti. Kutular arşivlenmeyi bekliyor —
**arşivleme merkezde** (outbox imleçleri Clara'da, `ISD-OPEN-YOUR-BOX`).

## Bir sonraki iş — YENİ SESSION'DA

**N8N kurulumu yapan bir agent takımı üretilecek — fabrikanın İLK GERÇEK ÜRÜNÜ.**

Bugüne kadar fabrika yalnız kendi kanonunu işledi; `team/` altı **boş**. Bu iş
`DAG`'ın 26 kuralını ilk kez sahada sınayacak: paketleme, manifest, marketplace,
sürüm, kurulum sihirbazı, hook yerleşimi, MCP, terminal kısayolu.

Sıra PAM'den başlar — gereksinim netleştirmesi.

## Mert'in kararını bekleyen

**Yedi karar kalemi:** `incelemeler/2026-08-08-fabrika-kanon-sorgulama/karar-kalemleri.md`

En kritiği **atıf sahipliği boşluğu** — index'i kim günceller, kanonda tanımsız;
bugün beş vaka üretti. Clara'nın önerisi mekanik çözüm (script üretsin).

## En kritik ölçülmemiş şey

**Sahada kanon yükleniyor mu — ÖLÇÜLMEDİ.**

Bugünkü 16/16 davranış testi dosyaları **elle okutarak** yapıldı. Sahada skill
gövdeleri gelmiyor (`#25834`) ve açılış hook'u alt-agent'ta hiç çalışmıyor.

Yani ölçülen şey kanonun **kalitesi**, dağıtımın çalışması değil. Bu ayrım
korunmalı — "kanon iyi" ile "kanon agent'ın elinde" aynı şey değil.
