---
name: clickup-token-yeri
description: Mert'in ClickUp kişisel API token'ı (pk_) ~/.zshenv içinde CLICKUP_TOKEN değişkeninde durur — değeri kayda yazılmaz, yeri bilinir
metadata:
  type: reference
---

Mert'in ClickUp kişisel API anahtarı (`pk_...`) **`~/.zshenv` → `CLICKUP_TOKEN`**
ortam değişkeninde (Mert'in kararı, 2026-09-04). Kullanım: `$CLICKUP_TOKEN`
(kabuk `~/.zshenv`'i yüklemediyse `source ~/.zshenv`).

Tarihçe: önce `~/.clickup-token` (2026-08-11) ve `.tmp-cu-token` (2026-08-14)
dosyalarındaydı — ikisi de geçersizleşmişti (token yenilenince eskiler ölür),
2026-09-04'te silindi. Script kanonu (`clickup-dinle.py`) zaten önce
`CLICKUP_TOKEN`'a bakar — uyumlu.

⚠️ Ölçüldü (2026-08-11): mcp-remote'un OAuth önbelleğindeki token (`~/.mcp-auth`)
`api.clickup.com` için **çalışmaz** — o `mcp.clickup.com` kapısının token'ı, 401 döner.
⚠️ Ölçüldü (2026-09-04): token yenilendiğinde eski `pk_` değerleri geçersizleşir —
"Token invalid / OAUTH_025" görürsen ilk şüphe bayat token.

`pk_` token `Authorization` header'ına **Bearer'sız, düz** yazılır.
Token değeri hiçbir kayda yazılmaz — yeri bilinir, değeri değişkenden okunur.
