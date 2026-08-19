# Webview'ler

Bir webview, editorun icinde calisan ve guvenligini saglamaktan senin sorumlu oldugun gercek bir tarayici baglamidir. Asagidaki her sey bundan cikar: ayri bir guven siniridir, kendi yasam dongusu, kendi kaynak yukleme kurallari ve eklenti kodunla arasindaki tek bagi olusturan bir mesaj kanali vardir.

## Icindekiler

- [WebviewPanel mi WebviewView mi](#webviewpanel-mi-webviewview-mi)
- [Guvenli HTML sablonu](#guvenli-html-sablonu)
- [Bos bir webview'de hata ayiklamak](#bos-bir-webviewde-hata-ayiklamak)
- [Mesajlasma](#mesajlasma)
- [State kaliciligi](#state-kaliciligi)
- [Yasam dongusu ve dispose](#yasam-dongusu-ve-dispose)
- [Temalama](#temalama)

---

## WebviewPanel mi WebviewView mi

Iki konteyner, iclerinde tek bir webview API'si.

**`WebviewPanel`** bir editor sekmesi kaplar. Emir kipiyle olusturulur — genelde bir komuttan — ve kapatilana kadar yasar. Bir dokumanla dikkat icin yarisan icerik icin kullan: bir onizleme, bir rapor, kullanicinin uzerinde calistigi bir form, bir grafik.

```typescript
const panel = vscode.window.createWebviewPanel(
  'myExt.report',                 // viewType — serializer kaydiyla eslesmeli
  'Analysis Report',              // sekme basligi
  vscode.ViewColumn.Beside,       // nerede acilacagi
  {
    enableScripts: true,          // varsayilan kapali; onsuz hicbir sey calismaz
    localResourceRoots: [
      vscode.Uri.joinPath(context.extensionUri, 'media'),
    ],
  }
);
panel.webview.html = getHtml(panel.webview, context.extensionUri);
panel.iconPath = vscode.Uri.joinPath(context.extensionUri, 'media', 'icon.svg');
```

**`WebviewView`** bir kenar cubugu ya da panel konteynerinde yasar. Onu sen olusturmazsin — bir provider kaydedersin ve kullanici view'i actiginda VS Code onu insa eder. Editorun yaninda duran kalici, ortam arayuzu icin kullan.

```typescript
class MySidebarProvider implements vscode.WebviewViewProvider {
  public static readonly viewType = 'myExt.sidebar';   // package.json ile eslesmeli

  constructor(private readonly extensionUri: vscode.Uri) {}

  resolveWebviewView(
    view: vscode.WebviewView,
    context: vscode.WebviewViewResolveContext,
    token: vscode.CancellationToken
  ): void {
    view.webview.options = {
      enableScripts: true,
      localResourceRoots: [vscode.Uri.joinPath(this.extensionUri, 'media')],
    };
    view.webview.html = getHtml(view.webview, this.extensionUri);

    view.webview.onDidReceiveMessage(msg => this.handle(msg));
  }
}

context.subscriptions.push(
  vscode.window.registerWebviewViewProvider(
    MySidebarProvider.viewType,
    new MySidebarProvider(context.extensionUri),
    { webviewOptions: { retainContextWhenHidden: false } }
  )
);
```

Manifest yarisi zorunludur, yoksa view hic gorunmez:

```json
{
  "contributes": {
    "views": {
      "explorer": [
        { "type": "webview", "id": "myExt.sidebar", "name": "My Extension" }
      ]
    }
  }
}
```

Bunu bir agac view'indan ayiran sey `"type": "webview"`dir; onu atlamak VS Code'un bir `TreeDataProvider` beklemesine yol acar ve kayit sessizce baglanmaz.

**Secim.** Kullanicinin calisirken goz attigi bir sey icin kenar cubugu view'i (durum, bir filtre paneli, bir sohbet yuzeyi). Odaklandiklari bir sey icin editor paneli. Bir webview view'i ayrica cok daha agresif sekilde yok edilip yeniden olusturulur — kullanici konteyneri her katladiginda — bu yuzden state kaliciligi orada daha onemlidir.

---

## Guvenli HTML sablonu

```typescript
function getNonce(): string {
  // Render basina taze bir rastgele token. Sabit degil, icerikten turetilmis degil.
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let text = '';
  for (let i = 0; i < 32; i++) {
    text += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return text;
}

function getHtml(webview: vscode.Webview, extensionUri: vscode.Uri): string {
  const nonce = getNonce();

  // asWebviewUri, yerel bir dosya Uri'sini webview'in fiilen yukleyebilecegi
  // vscode-webview-resource:// semasina yeniden yazar. Ham bir file:// yolu engellenir.
  const scriptUri = webview.asWebviewUri(
    vscode.Uri.joinPath(extensionUri, 'media', 'main.js'));
  const styleUri = webview.asWebviewUri(
    vscode.Uri.joinPath(extensionUri, 'media', 'main.css'));

  return /* html */ `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy" content="
    default-src 'none';
    style-src ${webview.cspSource} 'unsafe-inline';
    img-src ${webview.cspSource} https: data:;
    font-src ${webview.cspSource};
    script-src 'nonce-${nonce}';
    connect-src 'none';
  ">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="${styleUri}" rel="stylesheet">
  <title>Analysis Report</title>
</head>
<body>
  <h1 id="title">Analysis</h1>
  <div id="root"></div>
  <script nonce="${nonce}" src="${scriptUri}"></script>
</body>
</html>`;
}
```

Her direktifin ne yaptigi:

- **`default-src 'none'`** — acikca yeniden izin verilmeyen her seyi reddet. Sifirdan basla; diger her direktif bilincli bir istisnadir. Unuttugun her kaynak tipi sessizce izin verilmek yerine engellenir.
- **`style-src ${webview.cspSource}`** — `webview.cspSource`, VS Code'un urettigi webview basina origin string'idir; `asWebviewUri`'nin urettigi URI'lerle eslesen tek deger odur. Buraya sabit bir origin yazmak calismaz. `'unsafe-inline'` yalnizca gercekten satir ici `style="..."` nitelikleri ayarliyorsan eklenir; yapabildiginde onu cikar.
- **`img-src ... https: data:`** — yalnizca ihtiyacin kadar genislet. Satir ici SVG/base64 icin `data:`, gercekten uzak gorseller yukluyorsan (ki bu kullanicinin IP'sini o sunucuya sizdirir — bunun yerine gomulmeyi dusun) `https:`.
- **`script-src 'nonce-${nonce}'`** — onemli olan bu. Yalnizca tam olarak bu nonce'u tasiyan `<script>` etiketleri calisir. `'unsafe-inline'` yok, `'unsafe-eval'` yok. Bir dosya adindan, bir commit mesajindan ya da bir API yanitindan enjekte edilen betigin nonce'u yoktur ve calismaz.
- **`connect-src 'none'`** — webview'den `fetch`/XHR/WebSocket yok. Ag isi, kullanicinin proxy ayarlarina ve kimlik bilgilerine sahip olan extension host'a aittir; webview veriyi `postMessage` uzerinden istemelidir. Gercek bir sebep varsa yalnizca belirli bir host ile genislet.

**Guvenilmeyen icerigi asla string birlestirmeyle HTML'e sokma.** Dosya icerikleri, sembol adlari, hata mesajlari, API yanitlari, commit metni, workspace yollari — hepsi guvenilmez. Nonce'lu bir CSP en dogrudan betik enjeksiyonunu engeller, ama birlestirme yine de bir saldirganin DOM yapini bozmasina ve sahte arayuz uretmesine izin verir.

Iki dogru yaklasim:

```typescript
// 1. Veriyi mesaj kanali uzerinden gecir ve webview'in onu DOM'a *metin* olarak
//    render etmesine izin ver. Varsayilan secim budur.
panel.webview.postMessage({ type: 'setTitle', value: userSuppliedName });
```

```javascript
// media/main.js — guvenilmeyen degerler icin textContent, asla innerHTML.
window.addEventListener('message', (event) => {
  const msg = event.data;
  if (msg.type === 'setTitle') {
    document.getElementById('title').textContent = msg.value;
  }
});
```

```typescript
// 2. Bir deger gercekten baslangic HTML'ine gomulmek zorundaysa onu kacisla.
function escapeHtml(s: string): string {
  return s.replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[c]!));
}
```

Sayfaya gomulen JSON icin `JSON.stringify` tek basina yeterli degildir — bir string icindeki `</script>` dizisi blogu yine de sonlandirir. `<` isaretini kacisla:

```typescript
const payload = JSON.stringify(data).replace(/</g, '\\u003c');
```

**`localResourceRoots`, sinirin ikinci yarisidir.** CSP'den bagimsiz olarak webview'in hangi dizinlerden dosya yukleyebilecegini kapsamlandirir. Ise yarayan en dar kumeye ayarla — `extensionUri` degil, `media/` ve `dist/`. Onu atlamak varsayilan olarak eklenti kokunu verir ki bu istediginden genistir. Workspace dosyalarini yuklemek zorundaysan (bir onizlemedeki gorseller) o belirli klasor Uri'sini ekle ve ona okuma erisimi verdigini bil.

---

## Bos bir webview'de hata ayiklamak

En yaygin ariza: panel acilir, sekmenin basligi dogrudur, icerik alani bostur ya da yalnizca davranissiz statik HTML gosterir.

**Once gelistirici araclarini ac.** Komut Paleti → **"Developer: Open Webview Developer Tools"**. Bu, webview icin gercek bir Chromium devtools penceresidir. Console sekmesi, tam olarak hangi URL'yi tam olarak hangi CSP direktifinin engelledigini soyler. Asagidaki her sebep o konsolda tek bir satirdir; onu acmadan tahmin etmek, acmaktan cok daha fazla zaman kaybettirir.

Sebepler, fiilen gerceklestikleri sirayla:

1. **Eksik ya da uyusmayan nonce.** `<script>` etiketinin `nonce` niteligi yoktur ya da HTML, CSP icine yerlestirilenden farkli bir nonce ile kurulmustur — en sik sebebi `getNonce()`'un ayni render icinde iki kez cagrilmasidir. Onu `getHtml` cagrisi basina bir kez uret ve o tek degiskeni her iki yerde kullan. Konsol `Refused to execute inline script because it violates the following Content Security Policy directive` gosterir.

2. **`enableScripts` ayarlanmamis.** Varsayilani `false`'dur. Hata yok, konsol mesaji yok, sadece etkisiz bir sayfa. `createWebviewPanel` uzerindeki secenek nesnesini ya da `resolveWebviewView` icindeki `webview.options`'i kontrol et.

3. **`asWebviewUri` unutulmus.** Ham bir `file://` yolu ya da goreli bir `./media/main.js`, webview'in origin'inde cozulmez. Belirti, Network sekmesinde 404 sekilli bir basarisizlik ve eksik bir betiktir; sayfa statik HTML'ini render eder ve baska hicbir sey yapmaz. Her yerel kaynak — betikler, stil sayfalari, gorseller, fontlar — `webview.asWebviewUri()`'den gecer.

4. **`localResourceRoots` cok dar.** Uri dogru yeniden yazilmistir ama izin verilen koklerin disina isaret eder, bu yuzden yukleme reddedilir. Dosyalari `media/`'dan `dist/`'e tasiyip koklar dizisini guncellememekten sonra yaygindir. Konsol mesaji, kaynagin izin verilen yerel kaynak koklerinin disinda oldugundan bahseder.

5. **CSP yazim hatasi.** Direktifler arasinda eksik bir noktali virgul sessizce iki direktifi birlestirir ve ikincisi uygulanmayi birakir. `style-src` icinde eksik bir `${webview.cspSource}`, stil sayfasinin yuklendigi ama uygulanmasinin engellendigi anlamina gelir — sayfa bos yerine stilsiz render edilir, ki ipucu budur.

6. **Yuklemeden sonra betik hatasi.** Betik calisir ama ilk satirda hata firlatir (kotu bir import, iki kez cagrilan `acquireVsCodeApi`). Konsol bir CSP ihlali degil normal bir JS istisnasi gosterir. CSP varsaymadan once hatayi oku.

Kullanisli bir ikili arama: govdenin tamamini gecici olarak `<h1>hello</h1>` ile ve betiksiz degistir. O render ediliyorsa HTML hatti calisiyordur ve problem kaynak yuklemede ya da CSP'dedir. Edilmiyorsa problem yukaridadir — html hic atanmamistir ya da panel hemen dispose edilmistir.

---

## Mesajlasma

Iki baglam arasindaki tek kanal. Her iki yon de asenkron ve structured-clone ile serilestirilmistir — duz nesneler, diziler, sayilar, string'ler gonderebilirsin; fonksiyonlari, metotlu sinif ornekleri ni ya da `vscode.Uri` nesnelerini gonderemezsin (`.toString()` cagir).

Protokolu bir kez tanimla ve tipleri paylas:

```typescript
// src/protocol.ts — hem eklenti hem webview bundle'i tarafindan import edilir.
export type ToWebview =
  | { type: 'init'; items: ReadonlyArray<{ id: string; label: string }> }
  | { type: 'setBusy'; busy: boolean }
  | { type: 'error'; message: string };

export type FromWebview =
  | { type: 'ready' }
  | { type: 'select'; id: string }
  | { type: 'save'; text: string };
```

Eklenti tarafi:

```typescript
import type { ToWebview, FromWebview } from './protocol';

function post(webview: vscode.Webview, msg: ToWebview): Thenable<boolean> {
  return webview.postMessage(msg);
}

panel.webview.onDidReceiveMessage(
  (raw: unknown) => {
    // Gelen mesajlar GUVENILMEZDIR. Webview farkli bir guven baglamidir ve
    // workspace'in etkiledigi icerik calistiriyor olabilir. Harekete gecmeden
    // once sekli ve degerleri dogrula — bir alani asla dogrudan bir dosya
    // yoluna, bir kabuk komutuna ya da executeCommand'a gecirme.
    if (typeof raw !== 'object' || raw === null || !('type' in raw)) { return; }
    const msg = raw as FromWebview;

    switch (msg.type) {
      case 'ready':
        void post(panel.webview, { type: 'init', items: loadItems() });
        return;
      case 'select':
        if (typeof msg.id !== 'string' || !isKnownId(msg.id)) { return; }
        void revealItem(msg.id);
        return;
      case 'save':
        if (typeof msg.text !== 'string' || msg.text.length > 100_000) { return; }
        void saveText(msg.text);
        return;
      default:
        return;   // bilinmeyen mesaj tipleri hata firlatilmaz, yok sayilir
    }
  },
  undefined,
  context.subscriptions
);
```

Webview tarafi:

```javascript
// media/main.js
// acquireVsCodeApi() webview basina, sonsuza kadar BIR KEZ cagrilabilir. Ikinci
// bir cagri hata firlatir ve bu genelde bir modul yeniden import'unda ya da
// ikinci bir bundle dahil etmede oldugu icin hata sebebinden cok uzakta yuzeye
// cikar. Giris modulunun en ustunde bir kez cagir ve tutamaci etrafa gecir.
const vscode = acquireVsCodeApi();

window.addEventListener('message', (event) => {
  const msg = event.data;              // ToWebview
  switch (msg.type) {
    case 'init':   render(msg.items);   break;
    case 'setBusy': setBusy(msg.busy);  break;
    case 'error':  showError(msg.message); break;
  }
});

document.getElementById('root').addEventListener('click', (e) => {
  const id = e.target.dataset.id;
  if (id) { vscode.postMessage({ type: 'select', id }); }
});

// Eklentiye DOM'un hazir oldugunu soyle. Eklentinin .html ayarlandiktan hemen
// sonra mesaj gondermesine guvenme — betik dinleyicisini baglamadan once
// gonderilen mesajlar dusurulur.
vscode.postMessage({ type: 'ready' });
```

`ready` el sikismasi onemlidir. `webview.html = ...` webview betigi ayristirip calistirmadan once doner, bu yuzden atamadan hemen sonra tetiklenen bir `postMessage`, dinleyen kimse olmadan iner ve sessizce kaybolur. Webview'in hazir oldugunu duyurmasini sagla ve baslangic yukunu buna yanit olarak gonder.

Eklenti tarafindan `postMessage`, mesajin iletilemedigi durumda `false`'a cozulen bir `Thenable<boolean>` dondurur — ornegin webview gizliyse ve baglami tutmuyorsa. Bunu raporlanacak bir hata degil, normal olarak ele al.

---

## State kaliciligi

Uc mekanizma, uc farkli kaybolma icin.

**1. `setState` / `getState` — webview gizlenir ve sonra tekrar gosterilir.** Bir webview gizlendiginde VS Code onun DOM'unu ve JS baglamini yok eder. Yeniden gosterildiginde HTML sifirdan yeniden degerlendirilir: betigin tekrar, sifirdan calisir. `setState` tam olarak bunun boyunca JSON-serilestirilebilir bir nesneyi kalici kilar.

```javascript
const vscode = acquireVsCodeApi();

// Sag kalan neyse geri yukle; ilk render'da undefined.
let state = vscode.getState() ?? { scrollTop: 0, filter: '', selectedId: null };
applyState(state);

function update(patch) {
  state = { ...state, ...patch };
  vscode.setState(state);            // ucuz; sik cagirmak guvenli
}
```

Kucuk tut — arayuz durumu (kaydirma konumu, aktif sekme, filtre metni, secim), veri degil. Veri, `ready` uzerinde eklentiden yeniden istenmelidir, cunku yetkili kopya zaten eklentidedir.

**2. `retainContextWhenHidden` — ayni kaybolma, kaba kuvvetle cozulmus.**

```typescript
vscode.window.createWebviewPanel('myExt.report', 'Report', vscode.ViewColumn.One, {
  enableScripts: true,
  retainContextWhenHidden: true,   // panel var oldugu surece bellege mal olur
});
```

Bu, gizli baglamin tamamini canli tutar: DOM, JS heap, zamanlayicilar, her sey — her panel icin, tum oturum boyunca. **`setState`'i tercih et.** `retainContextWhenHidden`, yalnizca state gercekten yeniden olusturulamayacaksa savunulabilir — kaydedilmemis kullanici girdisi olan canli bir duzenleme oturumu, sayfa icinde uzun suren bir hesaplama, render'in ortasindaki bir video ya da canvas. Yeniden kurmak zahmetli oldugu icin ona uzanmak, eklentilerin VS Code'u agirlastirmakla un yapmasinin yoludur.

**3. `WebviewPanelSerializer` — pencere yeniden yuklendi ya da yeniden acildi.** `setState` tek basina bir pencere yeniden yuklemesinden sag cikmaz; bir seyin paneli yeniden olusturmasi gerekir. Bir serializer, arti eslesen aktivasyon olayi bunu yapar.

```typescript
class ReportSerializer implements vscode.WebviewPanelSerializer {
  constructor(private readonly extensionUri: vscode.Uri) {}

  async deserializeWebviewPanel(panel: vscode.WebviewPanel, state: unknown): Promise<void> {
    // Panel zaten var — VS Code sekmeyi geri yukledi. Secenekler sag KALMAZ,
    // bu yuzden html ayarlamadan once onlari yeniden uygula.
    panel.webview.options = {
      enableScripts: true,
      localResourceRoots: [vscode.Uri.joinPath(this.extensionUri, 'media')],
    };
    panel.webview.html = getHtml(panel.webview, this.extensionUri);
    wirePanel(panel);

    // `state`, webview'in setState'e en son gecirdigi seydir. Guvenilmez:
    // depolamadan gidip geldi. Kullanmadan once dogrula.
    if (state && typeof state === 'object') {
      void panel.webview.postMessage({ type: 'restore', state });
    }
  }
}

context.subscriptions.push(
  vscode.window.registerWebviewPanelSerializer('myExt.report', new ReportSerializer(context.extensionUri))
);
```

```json
{
  "activationEvents": ["onWebviewPanel:myExt.report"]
}
```

`viewType` string'i uc yerde de eslesmelidir — `createWebviewPanel`, `registerWebviewPanelSerializer` ve `onWebviewPanel:` aktivasyon olayi — yoksa geri yuklenen sekme hicbir zaman cozulmeyen bos bir kabuk gosterir. Aktivasyon olayi olmadan, VS Code paneli geri yuklemeye calistiginda eklentin calismiyordur ve serializer'a hic ulasilmaz.

---

## Yasam dongusu ve dispose

Bir panel her an kapanabilir: kullanici X'e basar, sekme grubunu kapatir ya da pencereyi yeniden yukler. Bu neredeyse her zaman `deactivate()`'ten cok once olur. Yani **bir panele kapsamli her sey, eklenti dispose oldugunda degil panel kapandiginda dispose edilmelidir.**

Panel basina dinleyicileri `context.subscriptions` icine itmek standart sizintidir: bir paneli elli kez acip kapat ve elli olu dinleyici biriktir; her biri kendi panelinin closure'unu canli tutar ve pencere yeniden yuklenene kadar her workspace olayinda tetiklenmeye devam eder.

```typescript
export class ReportPanel {
  private static current: ReportPanel | undefined;
  private readonly disposables: vscode.Disposable[] = [];   // panel basina torba

  public static show(extensionUri: vscode.Uri): void {
    const column = vscode.window.activeTextEditor?.viewColumn ?? vscode.ViewColumn.One;

    // Singleton: kopya yigmak yerine mevcut paneli one getir.
    if (ReportPanel.current) {
      ReportPanel.current.panel.reveal(column);
      return;
    }

    const panel = vscode.window.createWebviewPanel(
      'myExt.report', 'Analysis Report', column,
      {
        enableScripts: true,
        localResourceRoots: [vscode.Uri.joinPath(extensionUri, 'media')],
      }
    );
    ReportPanel.current = new ReportPanel(panel, extensionUri);
  }

  private constructor(
    private readonly panel: vscode.WebviewPanel,
    extensionUri: vscode.Uri
  ) {
    this.panel.webview.html = getHtml(this.panel.webview, extensionUri);

    // Bu panele bagli her sey panelin kendi torbasina gider.
    this.disposables.push(
      this.panel.webview.onDidReceiveMessage(msg => this.handle(msg)),
      vscode.workspace.onDidSaveTextDocument(doc => this.refresh(doc)),
      this.panel.onDidChangeViewState(e => {
        if (e.webviewPanel.visible) { this.refresh(); }
      }),
    );

    // Kullanici kapattiginda VE biz panel.dispose() cagirdiginda tetiklenir.
    this.panel.onDidDispose(() => this.dispose(), null, this.disposables);
  }

  public dispose(): void {
    ReportPanel.current = undefined;
    this.panel.dispose();                    // zaten dispose edildiyse etkisiz
    while (this.disposables.length) {
      this.disposables.pop()?.dispose();
    }
  }
}
```

Desen uzerine notlar:

- `onDidDispose`, her zaman baglaman gereken tek kancadir. Hem kullanici kaynakli kapanma hem programatik `panel.dispose()` icin tetiklenir, boylece tek bir temizlik yolu ikisini de kapsar.
- Singleton yeniden-goster-yeniden-olusturma deseni, rapor/onizleme panelleri icin kullanicilarin bekledigi seydir. Ornegi takip et ve statik referansi `dispose()` icinde temizle — bunu unutmak bayat bir referans birakir ve `reveal()` dispose edilmis bir panelde hata firlatir.
- Eklenti ayrica uzun omurlu kaynaklara sahipse (paylasilan bir onbellek, her panelin kullandigi bir watcher) bunlar panel basina torbaya degil `context.subscriptions`'a aittir. Ayrim kolaylik degil omur uzerinedir.

---

## Temalama

Webview editorun stilinden hicbir sey devralmaz. `#ffffff` sabit yaz ve kullanicilarinin yarisi — koyu temadaki herkes, arti her yuksek kontrast kullanicisi — okunmaz bir sayfa gorur. VS Code her webview'e CSS ozel ozellikleri enjekte eder; onlari kullan.

```css
/* media/main.css */
body {
  background-color: var(--vscode-editor-background);
  color: var(--vscode-editor-foreground);
  font-family: var(--vscode-font-family);
  font-size: var(--vscode-font-size);
  font-weight: var(--vscode-font-weight);
  padding: 0 20px;
}

button {
  background-color: var(--vscode-button-background);
  color: var(--vscode-button-foreground);
  border: none;
  padding: 6px 14px;
  cursor: pointer;
}
button:hover { background-color: var(--vscode-button-hoverBackground); }
button:focus { outline: 1px solid var(--vscode-focusBorder); }

input, textarea {
  background-color: var(--vscode-input-background);
  color: var(--vscode-input-foreground);
  border: 1px solid var(--vscode-input-border, transparent);
}

a { color: var(--vscode-textLink-foreground); }
a:hover { color: var(--vscode-textLink-activeForeground); }

code, pre {
  font-family: var(--vscode-editor-font-family);
  font-size: var(--vscode-editor-font-size);
}

.error { color: var(--vscode-errorForeground); }
.muted { color: var(--vscode-descriptionForeground); }
.panel { border: 1px solid var(--vscode-panel-border); }
```

Degisken adlari, VS Code renk referansindaki tema renk anahtarlarini yansitir; noktalar tirelerle degistirilmis olarak: `button.hoverBackground`, `--vscode-button-hoverBackground` olur. Her temada var oldugundan emin olmadigin her sey icin bir yedek ver: `var(--vscode-input-border, transparent)`.

VS Code ayrica `<body>` uzerine bir sinif koyar — `vscode-light`, `vscode-dark` ya da `vscode-high-contrast` (arti `vscode-high-contrast-light`) — bir degiskenin yetmedigi durumlar icin:

```css
/* Golgeler ve katmanlar genelde tema turune gore farkli muamele ister. */
.card { box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12); }
body.vscode-dark .card { box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5); }

/* Yuksek kontrast temalar, ince dolgular yerine gorunur kenarliklar ister. */
body.vscode-high-contrast .card {
  box-shadow: none;
  border: 1px solid var(--vscode-contrastBorder);
}
```

Her iki mekanizma da canli guncellenir: tema degistirmek, webview'i yeniden olusturmadan degiskenleri yeniden enjekte eder ve body sinifini degistirir; boylece bunlarin uzerine kurulmus bir sayfa, hicbir JavaScript olmadan kullanicinin temasini takip eder. Sabit renkler uzerine kurulmus bir sayfa bunu yapmaz ve gonderildigi anda kullanicilarin buyuk bir kismina bozuk gorunur.

Cok sayida standart kontrole ihtiyacin varsa `@vscode/webview-ui-toolkit` bilesenleri bu temalamayi senin icin uygular — ama benimsemeden once guncel bakim durumunu kontrol et, cunku destek durumu zaman icinde degisti.

---

**Imza kontrolu.** Webview secenekleri, `WebviewView` API'si ve ozel editorler (`registerCustomEditorProvider`, ki ayni webview primitifleri uzerine kuruludur) hepsi evrildi. Yakin zamanda kullanmadigin her seye guvenmeden once projenin `@types/vscode` icindeki `vscode.d.ts`'ine ve `package.json` icindeki `engines.vscode` tabanina karsi dogrula.
