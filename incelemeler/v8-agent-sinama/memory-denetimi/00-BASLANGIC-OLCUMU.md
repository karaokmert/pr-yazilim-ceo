# Memory denetimi — başlangıç ölçümü (Clara, agent raporlarından ÖNCE)

> **Neden bu dosya var:** agent'ların raporlarını doğrulayabilmek için.
> *"Index 77'den 60'a indi"* diyen bir agent'ı ancak başlangıç sayısı
> elimdeyse ölçebilirim.
> **Ölçüm anı:** 2026-08-13 00:45, görev verilmeden hemen önce.
> **Kaynak:** `~/.claude/agent-memory/ozel-yazilim-*`

| Agent | Dosya | Index (satır) |
|---|---|---|
| project-assistant | 70 | 75 |
| backend-developer | 67 | 77 |
| qa-engineer | 55 | 63 |
| frontend-developer | 45 | 49 |
| code-auditor | 25 | 33 |
| devops-engineer | 19 | 33 |
| test-engineer | 8 | 11 |
| mobile-developer | 5 | 6 |
| **ui-designer** | **0** | **—** |

**Toplam: 294 dosya**

## Ölçüm notları

- **UID'nin memory'si BOŞ** (0 dosya). Bugün hiç açılmadı; kutusu da yok.
- **MB neredeyse boş** (5 dosya) — bu gece açıldı.
- **PA ve BE en ağır** (70/67 dosya, 75/77 satır index).
- Index satır sayısı dosya sayısına yakın → indexler **büyük ölçüde pointer**
  görünüyor (içerik taşımıyorlar). Ama bu satır sayısından çıkarım; agent'ların
  kendi denetimi asıl ölçüm.

## Beklenen hareket

Mert'in talebi index'i **şişirmemek.** Yani sağlıklı sonuç:
- dosya sayısı artabilir (yeni kural kayıtları)
- **index satırı sabit kalmalı ya da AZALMALI** (var olan kayda ekleme +
  bayat kayıt temizliği)

Index'i büyüten bir agent talimatı yanlış uygulamış olur.
