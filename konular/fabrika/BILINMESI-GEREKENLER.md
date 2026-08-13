# Fabrika — agent üretim hattı — bilinmesi gerekenler

> Bu konuda bir iş geldiğinde **önce bu dosya okunur.**
> Hepsi sahada fiilen çarptı; hiçbiri tahmin değil.

**1. Fabrika `skill-project`'te** (2026-08-10'da taşındı). `agent-project` tarihçedir,
kanonu yürürlükte değil. İki repoda **aynı dosyaların kopyaları** var ve hash bazında
özdeş olabilir — ayıran şey içerik değil **statü.**

**2. Clara fabrikaya iş VERMEZ.** Devir bloğu yazılır, Mert taşır. Ölçüm için agent
çağırmak serbest (2026-08-06 kararı) — ayıran soru: **çıktı bir ürün mü, bir ölçüm mü?**

**3. Preload arızası var ve telafi ediliyor.** `skills:` frontmatter'ı plugin
agent'larında **sessizce çalışmıyor** (Claude Code #15178). `hooks/preload-skills.py`
açılışta yükleme talimatı basıyor. Telafi **çalışıyor** ama agent disiplinine bağlı.

**4. Kural skill'de kalır, body'ye kopyalanmaz** (2026-08-07 kararı).
