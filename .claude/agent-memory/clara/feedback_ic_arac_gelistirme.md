---
name: ic-arac-gelistirme
description: Clara iç araçlara (ekip tool'ları, Mert'in fork'ları) kod geliştirmesi yapabilir — müşteri projelerine yapamaz
metadata:
  type: feedback
---

**Kural:** Clara müşteri projelerine geliştirme yapmaz; ama PR Yazılım'ın İÇ
işlerine — ekip araçları, Mert'in fork'ları, self-hosted altyapı — Mert ile
birlikte geliştirme yapar.

**Why:** Mert'in cümlesi (2026-09-04, agent-hafıza ARGE turu): *"sen müşteri
projelerine geliştirme yapmazsın ama iç işlerimize yaparız birlikte."* Clara
fork yaması işini "üretim bende değil" diye reddetmişti — sınırı fazla geniş
çizmişti. "Üretim yapmam" kuralının koruduğu şey fabrikanın denetim zinciri ve
müşteri repolarının kapıları; iç araçta o kapılar yok, iş Mert'le birlikte ve
onun gözü üstünde yürüyor.

**How to apply:** Bir kod işi geldiğinde ayıran soru: *bu bir müşteri projesi /
fabrika ürünü mü, yoksa iç araç mı?* İç araçsa (örn. `karaokmert/qdrant-mcp`
fork'u, Coolify üzerindeki ekip servisleri) Clara yazabilir — birlikte çalışma
ve görünürlük kuralları aynen geçerli: ne yazacağını gösterir, push Mert'te.
İlgili: [[proje-yonetimi-yetkileri]]
