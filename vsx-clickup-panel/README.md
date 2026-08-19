# ClickUp Task Paneli

ClickUp'ta size atanmis task'lari VS Code kenar cubugunda gosterir: listeler,
detayini acar ve statusunu degistirir. Task'a bakmak icin tarayiciya gecmeyi
ortadan kaldirmak icin yazildi.

**Dagitim:** PR Yazilim ic kullanimi. Marketplace'e yayinlanmaz; `.vsix` olarak paylasilir.

## Kurulum

```bash
code --install-extension vsx-clickup-panel-0.1.0.vsix
```

Alternatif: Komut Paleti → **Extensions: Install from VSIX**.

> **Otomatik guncelleme yoktur.** VSIX ile kurulan eklentiler kendini
> guncellemez. Yeni surum duyuruldugunda ayni komutu yeni dosyayla tekrar
> calistirin.

## Baslangic

1. Activity Bar'daki **ClickUp** simgesine tiklayin.
2. **Token Gir** baglantisina tiklayin (ya da Komut Paleti → `ClickUp: Token Gir`).
3. Personal API Token'inizi yapistirin. Token'i ClickUp'ta
   **Settings → Apps → API Token** bolumunden alirsiniz; `pk_` ile baslar.

Token dogrulandiktan sonra atanmis acik task'lariniz panelde listelenir.

## Kullanim

| Eylem | Nasil |
|---|---|
| Task detayini ac | Task'a tiklayin — salt-okunur Markdown belgesi acilir |
| Sub task'lari gor | Ok isaretiyle task'i genisletin |
| Statu degistir | Task satirindaki `$(arrow-swap)` simgesi → listeden secin |
| Listeyi yenile | Panel basligindaki yenile simgesi |
| Cikis | Komut Paleti → `ClickUp: Token'i Sil` |

## Yapilandirma

| Ayar | Aciklama |
|---|---|
| `clickupPanel.teamId` | Task'larin cekilecegi ClickUp Workspace (team) ID. Bos birakilirsa ilk yuklemede secim sorulur ve secim buraya yazilir. |

## Gizlilik ve guvenlik

- **Token `context.secrets` icinde saklanir** — isletim sisteminin kimlik
  deposunda. Ayarlarda, `globalState`'te ya da diske duz metin olarak
  yazilmaz, Settings Sync ile baska makinelere gitmez.
- **Tek dis hedef `https://api.clickup.com`.** Baska hicbir sunucuya istek
  gonderilmez.
- **Telemetri yoktur.** Kullanim verisi toplanmaz, hicbir yere raporlanmaz.
- **Dosya yazilmaz, surec calistirilmaz.** Eklenti workspace icerigini okumaz.

Token'i iptal etmek icin ClickUp'ta ayni ekrandan silin; eklenti bir sonraki
istekte 401 alip oturumu temizler.

## Bilinen sinirlar

- Task listesi ilk sayfayla sinirlidir (ClickUp sayfa basina 100 task doner).
- Ust task'i baskasina atanmis sub task'lar kok seviyede gosterilir.

## Gelistirme

```bash
npm install
npm run compile      # tek seferlik derleme
npm run watch        # izleyerek derle
npm test             # gercek VS Code ornegi icinde testler
npx @vscode/vsce package   # .vsix uret
```

Ardindan VS Code'da **F5** — Extension Development Host acilir.
