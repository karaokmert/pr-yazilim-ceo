# clara — plugin

Clara'nın masaüstü bedeni tek pakette: agent gövdesi, 12 skill, açılış
hook'u ve hafıza MCP tanımı. Sürüm 0.1.0.

## İçerik

- `agents/clara.md` — gövde (karakter, düşünce sistemi, sınırlar)
- `skills/` — omurga (clara-main · clara-is-disiplini · clara-behavior) +
  iş skill'leri (proje-yonetimi · saha-task-takibi · saha-monitorluk ·
  sprint-yonetimi · agent-sinama · clickup-duzeni · arama-disiplini ·
  hafiza-duzeni · pr-agent-sistemi)
- `hooks/` — açılış direktifi: gövdedeki `skills:` listesini okuyup omurgayı
  açtırır (skill'ler preload edilmiyor — ölçüldü 2026-08-23)
- `.mcp.json` — `hafiza` sunucusu: **remote** MCP
  (https://mcp.prventurestudio.com/mcp), kimlik `MCP_BEARER_TOKEN`
  ortam değişkeninden

## Kurulum gereksinimleri

1. `MCP_BEARER_TOKEN` ortam değişkeni tanımlı olmalı (değeri Coolify'daki
   qdrant-mcp servisininkiyle aynı; `make token` ile ~/.zshenv'e eklenir).
2. Başka bir şey gerekmez — hafıza sunucu tarafında yaşar, lokal model
   ya da repo klonu istemez.

## Kaynak ve sürüm düzeni

Kanonun yaşayan hâli bu repodadır (`.claude/agents/clara.md` ve skill
kaynakları); plugin o kanonun paketlenmiş fotoğrafıdır. Kanon değişince
buraya kopyalanır ve `plugin.json` sürümü artırılır — paketlenmeyen
değişiklik sahaya inmez.

Clara fabrika ürünü değildir; kanonu ve bu paket yalnız Clara'nın elinden
çıkar (karar: kendi kanonun yalnız senin elinden çıkar).
