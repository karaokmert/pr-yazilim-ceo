---
name: clickup-sprint-mekanigi
description: PR Team space'inde bir task sprinte "Sonraki Sprint" custom field checkbox'ı ile alınır — sprint listesine elle eklenerek değil
metadata:
  type: project
---

Bir task'ı sprinte almak için **task üzerindeki "Sonraki Sprint" checkbox custom
field'ı işaretlenir**; ClickUp otomasyonu task'ı sprint listesine kendisi taşır.

Field id: `a320e4f0-8618-453a-b808-92f125fa2f4e` (checkbox, space 48321079)
Yanında bir de `4008a31b-f80f-41e3-bc53-36f49baabc45` "Sprint Task" checkbox'ı var.

**Why:** 2026-09-02'de Mert "sonraki sprinte taşı" dedi, ben `add_task_to_list` ile
altı task'ı Sprint 8 listesine elle eklemeye çalıştım. Altı çağrı da
`success: true` döndü ama liste boş göründü ve Mert'in temizlemesi gerekti.
Mert'in düzeltmesi: *"Taski oluşturup sonraki sprint custom fieldini checklersen
sprint 7 ye otomatik gider zaten."*

**How to apply:** Sprint'e alma isteği geldiğinde `clickup_update_task` +
`custom_fields` kullan. `add_task_to_list` bu space'te sprint için doğru araç
değil. Ve genel ders: bir ekibin kurulu akışı varsa mekanizmayı **sormadan
varsayma** — API'nin `success` dönmesi doğru yolu kullandığın anlamına gelmiyor.

⚠️ `clickup_filter_tasks` sprint listelerini boş gösteriyor (Sprint 3–8 hepsi boş
dönüyor), oysa içlerinde task olabilir. **Sprint doğrulaması için task'ın kendi
"Sprint" custom field'ını oku** (`8770d739-932e-4711-ac30-f0a824a559aa`,
short_text) — Mert bu alanı otomasyonla dolduruyor ve kendi cümlesi: *"Ben
otomatik yazıyorum ki sen kontrol ettiğinde oku diye."* Liste sorgusu yerine bu
alan kullanılır. İlgili: [[clickup-durum-2026-09-02]]
