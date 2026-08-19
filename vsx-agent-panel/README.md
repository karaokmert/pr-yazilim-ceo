# Agent Durum Paneli

Acik Claude Code agent oturumlarini VS Code kenar cubugunda canli listeler.

**Dagitim:** ic kullanim (`.vsix`). Marketplace'e cikmaz.

## Gelistirme

```bash
npm install
npm run watch     # izleyici build
```

Sonra VS Code'da **F5** — Extension Development Host acilir.

Kenar cubugunda "Agent Durumu" ikonu gorunur; panel acildiginda eklenti uyanir.

## Veri kaynagi

`~/.claude/sessions/<pid>.json` — her canli oturum bir dosya. Icerik olculdu:
`pid`, `name`, `agent`, `cwd`, `status`, `startedAt`, `updatedAt`, `messagingSocketPath`.

Ayrinti ve olcum kaniti icin devir notuna bakiniz.

## Kurulum (ic dagitim)

`.vsix` dosyasi ekip icinde paylasilir. Kurulum:

```bash
code --install-extension vsx-agent-panel-0.1.0.vsix
```

Ya da VS Code icinde: Komut Paleti -> **Extensions: Install from VSIX**.

> **ONEMLI — otomatik guncelleme YOK.** VSIX'ten kurulan eklentiler kendini
> guncellemez. Yeni surum ciktiginda ayni komut yeni dosyayla tekrar
> calistirilir. Hangi surumde oldugunuzu Extensions panelinde gorebilirsiniz.

## Test

```bash
npm test     # gercek VS Code indirilir, testler onun icinde kosar
```

## Ayarlar

| Ayar | Varsayilan | Ne yapar |
|---|---|---|
| `vsxAgentPanel.refreshIntervalSeconds` | 5 | Gecen sure etiketlerinin tazelenme araligi |
| `vsxAgentPanel.staleThresholdMinutes` | 15 | Bu sureden uzun sessiz oturum "unutulmus" sayilir |

Ikisi de yeniden yukleme gerektirmeden etkili olur.

## Gizlilik

Eklenti yalniz `~/.claude/sessions` dizinini **okur**. Yazmaz, silmez,
ag cagrisi yapmaz, telemetri toplamaz, calistirilabilir bir sey baslatmaz.
