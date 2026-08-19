# Agac View'lari, Durum Cubugu ve Arayuz Yuzeyleri

`vscode.window` namespace'indeki arayuz yuzeyleri icin ayrintili referans. Ust skill kurallari kapsar; bu dosya sekilleri kapsar.

Bunlarin her biri sahip oldugun bir sey uretir. `createTreeView`, `createStatusBarItem`, `createOutputChannel`, `createQuickPick`, `registerFileDecorationProvider` — hepsi dispose edilebilir dondurur; onlari olusturdugun anda `context.subscriptions` icine it, ilginc kodun sonunda `activate`'in dibinde degil.

## Icindekiler

- [TreeDataProvider](#treedataprovider)
- [Yenileme olayi](#yenileme-olayi)
- [TreeItem ayrintili](#treeitem-ayrintili)
- [contextValue ve oge basina menuler](#contextvalue-ve-oge-basina-menuler)
- [createTreeView mi registerTreeDataProvider mi](#createtreeview-mi-registertreedataprovider-mi)
- [Tembel yukleme ve performans](#tembel-yukleme-ve-performans)
- [Bos durum: viewsWelcome](#bos-durum-viewswelcome)
- [StatusBarItem](#statusbaritem)
- [QuickPick](#quickpick)
- [InputBox](#inputbox)
- [Bildirimler](#bildirimler)
- [OutputChannel ve LogOutputChannel](#outputchannel-ve-logoutputchannel)
- [FileDecorationProvider](#filedecorationprovider)

---

## TreeDataProvider

Bir agac view'i bir cekme arayuzudur. Bir agac kurup teslim etmezsin; her seferinde tek bir dugum hakkindaki sorulari cevaplarsin ve hangi sorularin sorulacagina VS Code karar verir.

Arayuz *senin* dugum tipin uzerinde generic'tir. `TreeItem`'in kendisi yerine gercek bir alan tipi kullan — bir dugumde bir komut tetiklendiginde alttaki veriye ihtiyacin olacak ve `TreeItem` onu tasimaz.

```typescript
import * as vscode from 'vscode';

interface Task {
  id: string;
  label: string;
  status: 'pending' | 'running' | 'failed' | 'done';
  parentId?: string;
}

export class TaskTreeProvider implements vscode.TreeDataProvider<Task> {
  private readonly _onDidChangeTreeData =
    new vscode.EventEmitter<Task | undefined | void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  private tasks: Task[] = [];

  constructor(private readonly context: vscode.ExtensionContext) {}

  // VS Code'un render edecegi her dugum icin cagrilir. Ucuz ve senkron tut.
  getTreeItem(element: Task): vscode.TreeItem {
    const hasChildren = this.tasks.some(t => t.parentId === element.id);
    const item = new vscode.TreeItem(
      element.label,
      hasChildren
        ? vscode.TreeItemCollapsibleState.Collapsed
        : vscode.TreeItemCollapsibleState.None,
    );

    item.id = element.id;                 // stabil id, yenilemeler arasinda genisleme durumunu korur
    item.description = element.status;    // label'dan sonra soluk metin
    item.iconPath = iconForStatus(element.status);
    item.contextValue = `task.${element.status}`;  // menu `when` ifadelerinin eslestigi sey
    item.command = {
      command: 'myExt.openTask',
      title: 'Open Task',
      arguments: [element],
    };
    return item;
  }

  // Yalnizca kok icin ve kullanicinin genislettigi dugumler icin cagrilir.
  getChildren(element?: Task): Task[] {
    return element
      ? this.tasks.filter(t => t.parentId === element.id)
      : this.tasks.filter(t => t.parentId === undefined);
  }

  // Arayuzde istege bagli — TreeView.reveal() cagirdiysan ZORUNLU.
  getParent(element: Task): Task | undefined {
    return element.parentId
      ? this.tasks.find(t => t.id === element.parentId)
      : undefined;
  }

  setTasks(tasks: Task[]): void {
    this.tasks = tasks;
    this._onDidChangeTreeData.fire();   // bu olmadan view hala eski veriyi gosterir
  }

  dispose(): void {
    this._onDidChangeTreeData.dispose();
  }
}
```

`getChildren` bir promise dondurebilir. Asenkron sorun degil ve beklenendir — cocuklari bir ag cagrisindan ya da bir alt surecten gelen bir dugum `Promise<Task[]>` dondurmeli ve VS Code cozulurken o dugumde bir donen gosterge gosterir. Sorun olan sey bu isi `getTreeItem` icinde yapmaktir; o, her yeniden cizimde gorunur her satir icin cagrilir.

Kaydet ve hangi kaydi istedigini not et (bir sonraki bolum secimi acikliyor):

```typescript
const provider = new TaskTreeProvider(context);
context.subscriptions.push(
  provider,
  vscode.window.registerTreeDataProvider('myExt.tasks', provider),
);
```

View id'si (`myExt.tasks`), `package.json` icindeki bir `contributes.views` girdisiyle eslesmeli. Onsuz kayit sessizce hicbir sey yapmaz — baglanacak bir view yoktur.

## Yenileme olayi

Bu en yaygin agac view'i hatasidir, bu yuzden acikca soylemeye deger: **alttaki dizini degistirmek hicbir sey yapmaz.** VS Code verini izlemez. Provider'i yalnizca `onDidChangeTreeData` tetiklendiginde yeniden sorgular.

Disari actigin `EventEmitter` mekanizmadir. Neyi tetikledigin yenilemenin kapsamini belirler:

```typescript
// Tum agac — VS Code getChildren(undefined)'i yeniden sorgular ve asagi yurur.
this._onDidChangeTreeData.fire();
this._onDidChangeTreeData.fire(undefined);  // ayni sey

// Tek alt agac — VS Code getChildren(element)'i yeniden sorgular ve yalnizca o dugumun altini yeniden kurar.
this._onDidChangeTreeData.fire(someTask);
```

Dogru olan en dar kapsami tetikle. `TreeItem.id` degerlerin stabilse tam agac tetiklemesi hicbir seyi katlamaz, ama genisletilmis her dugum icin `getChildren`'i yeniden calistirir — cocuklari bir surecten gelen bir agacta bu, tek bir yaprak degisikligi icin bir is patlamasidir.

Emitter'in tip parametresi `undefined` (ya da `void`) icermelidir, yoksa tum-agac formu tip kontrolunden gecmez:

```typescript
new vscode.EventEmitter<Task | undefined | void>();
```

Ilgili iki tuzak:

- Verin yerinde degistirilmek yerine yeniden olusturulabiliyorsa **`TreeItem.id` ayarla.** Onsuz VS Code dugumleri label yoluna gore tanimlar ve yeniden adlandirmadan sonraki bir yenileme agaci katlar ve secimi kaybeder.
- **`getChildren` icinden tetikleme.** Yeniden girer ve ya sonsuz bir yenileme dongusu ya da kalici titreyen bir view elde edersin.

## TreeItem ayrintili

```typescript
const item = new vscode.TreeItem(label, collapsibleState);
```

Ilk argüman, alt string'leri vurgulamak istediginde bir `TreeItemLabel` (`{ label, highlights }`) da olabilir — arama sonuclari icin kullanisli.

| Ozellik | Ne yapar |
| --- | --- |
| `label` | Birincil metin. `string` ya da vurgulama araliklariyla `TreeItemLabel`. |
| `description` | Label'dan sonra soluk metin. `true`, onu `resourceUri`'den turetir. |
| `tooltip` | Zengin hover icerigi icin `string` ya da `MarkdownString`. |
| `iconPath` | `ThemeIcon`, bir `Uri` ya da `{ light, dark }` dosya yollari. |
| `collapsibleState` | `None`, `Collapsed` ya da `Expanded`. |
| `command` | Satira tek tiklamada calisir. |
| `resourceUri` | Satiri bir dosyaya baglar — ikon, dekorasyonlar ve Git renkleri takip eder. |
| `contextValue` | Oge basina menu `when` ifadelerinin eslestigi string. |
| `id` | Yenilemeler arasinda stabil kimlik. |
| `accessibilityInformation` | Ekran okuyucu etiketi ve rolu. |

### collapsibleState

`None` yaprak demektir — dondurme oku yoktur ve onun icin `getChildren` hic cagrilmaz. `Collapsed` ve `Expanded` ikisi de "bu dugumun cocuklari var" demektir; fark yalnizca ilk render'dadir.

Bunu cocuklarin gercekten var olup olmadigindan hesapla. `getChildren`'i bos dizi donduren `Collapsed` bir dugum, genisletildiginde hicbir seye acilan bir dondurme oku render eder ki bu kullaniciya hata gibi okunur. Isi yapmadan gercekten bilemedigin durumda, `Collapsed` arti `[]` donduren asenkron bir `getChildren` durust bir odunlesmedir — ama bilmeyi tercih et.

### iconPath

Uc form, tercih sirasina gore azalan:

```typescript
// 1. ThemeIcon — isimle yerlesik bir codicon, $() sarmalayicisi olmadan.
item.iconPath = new vscode.ThemeIcon('check');
item.iconPath = new vscode.ThemeIcon('error', new vscode.ThemeColor('charts.red'));

// 2. Temaya duyarli dosya cifti — kendi SVG'lerin, tema basina bir tane.
item.iconPath = {
  light: vscode.Uri.joinPath(context.extensionUri, 'media', 'light', 'task.svg'),
  dark: vscode.Uri.joinPath(context.extensionUri, 'media', 'dark', 'task.svg'),
};

// 3. Tek Uri — her iki temada ayni ikon. Genelde yanlis; artwork bilincli
//    olarak notr degilse birinde okunaksiz olacaktir.
item.iconPath = vscode.Uri.joinPath(context.extensionUri, 'media', 'logo.png');
```

`ThemeIcon` tercih edilir cunku kullanicinin ikon temasini ve renk token'larini otomatik devralir ve bundle boyutuna mal olmaz. Ikinci argüman bir `ThemeColor`'dir ve bir *tema renk id'si* alir — bir hex degeri degil. Harfi harfine bir renk ayarlamanin API'si yoktur; bu bilinclidir, ki eklentiler yuksek kontrast ve renk korlugune duyarli temalari bozamasin.

Codicon isimleri VS Code dokumanlarindaki codicon referansindan gelir. `iconPath` icinde ciplak ismi (`'check'`) gecirirsin; satir ici ikonlari destekleyen metin ozelliklerinde ise `$(check)` formunu kullanirsin. Ikisini karistirmak sik yapilan bir hatadir — `new ThemeIcon('$(check)')` hicbir sey render etmez.

### MarkdownString ile tooltip

```typescript
const md = new vscode.MarkdownString();
md.appendMarkdown(`**${task.label}**\n\n`);
md.appendMarkdown(`Status: \`${task.status}\`\n\n`);
md.appendCodeblock(task.lastError ?? '(no errors)', 'text');
item.tooltip = md;
```

Tooltip'in tiklanabilir bir komut baglantisina ihtiyaci varsa `md.isTrusted = true` ayarla ve `command:` URI'leri kullan — ama yalnizca string'in her parcasi senin urettigin icerikse. Workspace iceriginden kurulmus bir string uzerinde `isTrusted` bir komut enjeksiyonu vektorudur. Araya sokulan her deger icin `appendMarkdown` yerine (kacislayan) `appendText`'i tercih et.

### resourceUri

`resourceUri` ayarlamak, dosya sekilli satirlari bedavaya almanin yoludur:

```typescript
item.resourceUri = vscode.Uri.file(task.filePath);
item.iconPath = undefined;          // karari dosya ikon temasina birak
item.description = true;            // iceren klasoru description olarak goster
```

VS Code o zaman kullanicinin dosya ikon temasini, Git dekorasyonlarini (degistirilmis, izlenmeyen), problem dekorasyonlarini ve `FileDecorationProvider` ile kaydedilmis her seyi uygular. `resourceUri` ayarlamayan bir dosya agaci, gezginin icinde yabanci gorunur ve bunlarin hepsini bosuna kaybeder.

## contextValue ve oge basina menuler

`contextValue`, bir ogeye ekledigin duz bir string'dir; menu katkilari onu `viewItem` baglam anahtari uzerinden bir `when` ifadesinde eslestirir. Satir basina baglam menuleri ve satir ici eylem dugmeleri icin tum mekanizma budur.

```typescript
item.contextValue = task.status === 'running' ? 'task.running' : 'task.idle';
```

```jsonc
// package.json
"contributes": {
  "menus": {
    "view/item/context": [
      {
        "command": "myExt.cancelTask",
        "when": "view == myExt.tasks && viewItem == task.running",
        "group": "inline"
      },
      {
        "command": "myExt.rerunTask",
        "when": "view == myExt.tasks && viewItem =~ /^task\\./",
        "group": "1_actions"
      }
    ]
  }
}
```

Onemli noktalar:

- Her zaman `view == <senin view id'n>` ile kapsam ver, yoksa menu ogelerin ayni `contextValue`'yu kullanan diger eklentilerin agaclarinda gorunur.
- `==` tam eslesmedir. Deger aileleri icin yukaridaki gibi `=~` regex operatorunu kullan.
- `group: "inline"`, eylemi sag tik menusu yerine satirda bir hover ikonu olarak koyar. Bunu en yaygin bir ya da iki eylem icin sakla.
- Komut ilk argüman olarak *dugumu* alir (`TreeItem`i degil `Task`i), cunku `getChildren`'in dondurdugu sey odur. Cok secimli view'lar ikinci argüman olarak tum secimi gecirir.
- `contextValue`'yu degistirmek degisiklik olayini tetiklemeyi gerektirir — o `TreeItem`'in bir parcasidir, bu yuzden menu degismeden once satirin yeniden sorgulanmasi gerekir.

## createTreeView mi registerTreeDataProvider mi

`registerTreeDataProvider` provider'i baglar ve yalnizca bir `Disposable` dondurur. `createTreeView` ayni seyi yapar ve geriye bir `TreeView<T>` nesnesi — view'in kendisini — verir.

Sunlardan herhangi birine ihtiyacin varsa `createTreeView` kullan:

```typescript
const view = vscode.window.createTreeView('myExt.tasks', {
  treeDataProvider: provider,
  showCollapseAll: true,
  canSelectMany: false,
  // dragAndDropController: ...  // yalnizca surukle/birak uyguluyorsan dahil et
});
context.subscriptions.push(view);

// Programatik reveal — TreeDataProvider.getParent()'in UYGULANMASINI GEREKTIRIR.
await view.reveal(someTask, { select: true, focus: true, expand: 2 });

// Baslik metni ve view konteyner ikonunda sayisal bir rozet.
view.title = 'Tasks';
view.message = 'No workspace folder open.';   // agac govdesini bu metinle degistirir
view.badge = { value: failedCount, tooltip: `${failedCount} failed` };

// Gozlem.
view.onDidChangeSelection(e => { /* e.selection: readonly Task[] */ });
view.onDidChangeVisibility(e => {
  if (e.visible) { provider.startPolling(); } else { provider.stopPolling(); }
});
view.onDidExpandElement(e => { /* e.element */ });
view.onDidCollapseElement(e => { /* e.element */ });

// Okuyabilecegin durum.
view.visible;    // boolean
view.selection;  // readonly Task[]
```

`getParent` olmadan `reveal` calisma aninda hata firlatir. `TreeDataProvider`'in "istege bagli" uyesinin istege bagli olmadigi tek yerdir ve arayuz onsuz sorunsuz derlendigi icin gozden kacmasi kolaydir.

`onDidChangeVisibility`, bir agac view'inin arka planda CPU maliyeti olmasini engelleyen kancadir. Katlanmis bir kenar cubugu bolumundeki bir view gorunmezdir ve sen durdurmadikca yoklayicini hayatta tutar.

`view.message`, *gecici* aciklayici bir durum icin dogru aractir ("Taraniyor...", "Task'lari gormek icin bir hesap baglayin"). Dugmeler gerektiren kalici bir bos durum icin bunun yerine `viewsWelcome` kullan — asagiya bak.

## Tembel yukleme ve performans

Agac cekme tabanlidir ki bu bir armagandir: yalnizca kullanicinin fiilen baktigi seyin bedelini odersin. Bunu carcur etmek kolaydir.

- `getChildren` kok icin, sonra genisletildikce her dugum icin cagrilir — katlanmis alt agaclar icin asla. Tum hiyerarsiyi constructor'inda ya da `setTasks` icinde onceden yurume.
- `getTreeItem` gorunur her satir icin ve her yenilemeden sonra tekrar cagrilir. Ucuz olmali: I/O yok, `fs.statSync` yok, buyuk bir dosyanin string ayristirmasi yok. Bir satirin ikonu bir stat cagrisina bagliysa, o seviyeyi `getChildren` icinde yuklerken stat'i yap ve dugum tipinde onbellekle.
- Asenkron `getChildren` yavas is icin dogru yerdir. Promise beklerken VS Code o dugumde bir donen gosterge render eder.
- Tek bir cagridan binlerce cocuk dondurme. Birkac yuz satirin otesinde view zaten kullanilabilir olmaktan cikar; ilk sayfayi arti, komutu sonraki sayfayi getiren ve hedefli bir yenileme tetikleyen sentetik bir "Daha fazla yukle..." dugumu dondur.
- Iptal `TreeDataProvider` arayuzunun bir parcasi degildir — token yoktur. Bekleyen bir `getChildren` alakasiz hale gelirse (kullanici dugumu katladi, workspace degisti) bunu bir nesil sayaciyla kendin korumali ve bayat sonucu atmalisin.

## Bos durum: viewsWelcome

Gercekten gosterecek hicbir seyi olmayan bir agac bos bir dikdortgen olarak render edilir ki bu bozuktan ayirt edilemez. `contributes.viewsWelcome` onu bunun yerine metin ve komut baglantilariyla doldurur.

```jsonc
"contributes": {
  "viewsWelcome": [
    {
      "view": "myExt.tasks",
      "contents": "No tasks found in this workspace.\n[Create a task](command:myExt.createTask)\nOr read the [setup guide](https://example.com/docs).",
      "when": "myExt:hasWorkspace && !myExt:hasTasks"
    },
    {
      "view": "myExt.tasks",
      "contents": "Open a folder to see tasks.\n[Open Folder](command:vscode.openFolder)",
      "when": "workbenchState == empty"
    }
  ]
}
```

Bilinmesi gereken mekanikler:

- `[Label](command:someCommand)` seklinde yazilan Markdown baglantilari tam genislikte dugmeler olarak render edilir. Siradan URL baglantilari satir ici baglantilar olarak render edilir. Bu fark, birincil eylem ile dokumantasyonu ayirt etme seklindir.
- Welcome icerigi yalnizca provider sifir kok cocuk dondurdugunde gorunur. Agacta satir varken onu zorlayamazsin.
- Bunu kullanisli kilan sey `when` ifadesidir. Kendi anahtarlarini eklentiden sur:

```typescript
await vscode.commands.executeCommand('setContext', 'myExt:hasTasks', tasks.length > 0);
```

Bu anahtarlari cevabin degistigi her noktada ayarla — yuklemeden sonra, yenilemeden sonra, bir hatadan sonra. Yalnizca aktivasyonda calisan bir `setContext` cagrisi, welcome view'ini sonsuza kadar ilk durumunda takili birakir.

Durumlari ayirt etmek meselenin ozudur. "Henuz task yok" ve "task sunucusuna baglanilamadi" kullanici icin farkli problemlerdir; farkli `when` ifadeleriyle iki `viewsWelcome` girdisinin hicbir maliyeti yoktur ve bir destek turunu kurtarir.

## StatusBarItem

```typescript
const status = vscode.window.createStatusBarItem(
  'myExt.buildStatus',                    // stabil id — kullanicilarin arayuzden gizlemesini saglar
  vscode.StatusBarAlignment.Left,
  100,                                    // daha yuksek oncelik daha sola oturur
);
context.subscriptions.push(status);

status.name = 'Build Status';             // durum cubugunun kendi baglam menusunde gosterilir
status.text = '$(sync~spin) Building';    // $(codicon) satir ici render edilir; ~spin animasyon yapar
status.tooltip = new vscode.MarkdownString('Click to open the build log');
status.command = 'myExt.showBuildLog';
status.show();
```

Sonra durum degistikce gecis yaptir:

```typescript
function setResult(ok: boolean, detail: string) {
  status.text = ok ? '$(check) Build' : '$(error) Build';
  status.tooltip = detail;
  status.backgroundColor = ok
    ? undefined
    : new vscode.ThemeColor('statusBarItem.errorBackground');
}
```

Notlar:

- `backgroundColor` pratikte yalnizca iki tema rengi kabul eder: `statusBarItem.warningBackground` ve `statusBarItem.errorBackground`. Digerleri yok sayilir. Bu bilinclidir — durum cubugu bir tuval degildir.
- Sol hizalama mevcut workspace ya da gorevle ilgili seyler icindir; sag ise mevcut editorle ilgili seyler icin (satir sonu, dil modu). Oncelik ayni taraftaki ogeleri siralar.
- Oge alakali degilken `hide()`. Her zaman mevcut olan, her zaman ayni seyi soyleyen bir durum cubugu ogesi, kullanicinin kaldiramayacagi bir gurultudur — `name`'in onemli olmasinin sebebi budur: ona kendisi gizlemenin bir yolunu verir.
- Metni kisa tut. Burasi paylasilan bir seritir; uzun bir string diger eklentilerin ogelerini ekran disina iter.
- Onu dispose et. Sizdirilmis bir durum cubugu ogesi eklenti devre disi kaldiktan sonra hayatta kalir ve yeniden yukleme yapilana kadar ekranda kalir.

## QuickPick

Iki seviyede API. Once basit olana uzan.

### window.showQuickPick

```typescript
interface TaskPick extends vscode.QuickPickItem {
  task: Task;
}

const picks: TaskPick[] = tasks.map(t => ({
  label: t.label,
  description: t.status,
  detail: t.id,          // ikinci satir, soluk
  task: t,
}));

const chosen = await vscode.window.showQuickPick(picks, {
  title: 'Run Task',
  placeHolder: 'Select a task to run',
  matchOnDescription: true,
  matchOnDetail: false,
  ignoreFocusOut: false,
});

if (!chosen) { return; }   // kapatildi — hata degil, yaygin durum
await runTask(chosen.task);
```

**Kullanici Escape'e bastiginda ya da baska yere tikladiginda `showQuickPick` `undefined`'a cozulur.** Her cagri noktasinin bu erken donuse ihtiyaci var. Kapatmayi bir hata gibi ele almak — loglamak, bir mesaj gostermek — gurultulu eklentiler ureten kotu bir aliskanliktir.

`QuickPickItem`'i kendi alaninla genisletmek (yukarida `task`), secimden veriye geri donmenin temiz yoludur. Alternatif olan `label` uzerinden eslestirme, iki oge ayni label'i paylastigi anda bozulur.

### window.createQuickPick

Tek seferlik fonksiyonun ifade edemeyecegi bir davranisa ihtiyacin oldugunda nesne formunu kullan: bir mesgul gostergesi, kullanici yazdikca degisen sonuclar, dugmeler ya da bir secimden sonra acik kalmak.

```typescript
const qp = vscode.window.createQuickPick<TaskPick>();
qp.title = 'Search Tasks';
qp.placeholder = 'Type to search the server';
qp.matchOnDescription = true;
qp.busy = true;
qp.buttons = [
  { iconPath: new vscode.ThemeIcon('refresh'), tooltip: 'Reload' },
];

const disposables: vscode.Disposable[] = [];
let generation = 0;

disposables.push(
  // Dinamik filtreleme: statik bir listeyi filtrelemek yerine tus vurusu basina sonuc getir.
  qp.onDidChangeValue(async value => {
    const mine = ++generation;
    qp.busy = true;
    const results = await searchTasks(value);
    if (mine !== generation) { return; }   // daha yeni bir sorgu bunun yerini aldi
    qp.items = results.map(t => ({ label: t.label, description: t.status, task: t }));
    qp.busy = false;
  }),
  qp.onDidAccept(() => {
    const [picked] = qp.selectedItems;
    if (picked) { void runTask(picked.task); }
    qp.hide();
  }),
  qp.onDidTriggerButton(() => void reload()),
  qp.onDidHide(() => {
    disposables.forEach(d => d.dispose());
    qp.dispose();
  }),
);

qp.show();
```

`onDidHide`'in `dispose`'u tetiklemesi standart yasam dongusudur: secici modal-vari ve tek kullanimliktir, bu yuzden `context.subscriptions` icinde yasamak yerine kendini temizler.

Nesil sayaci onemlidir. `onDidChangeValue` tus vurusu basina tetiklenir, istekler sirasiz biter ve koruma olmadan `"bui"` icin yavas bir yanit, `"build"` icin dogru sonuclarin uzerine yazabilir.

`items`'i `onDidChangeValue`'dan kendin surdugunde, sen temizlemedikce VS Code yine de kendi bulanik filtresini ustune uygular. Sunucu zaten filtreledeyse bu cifte filtreleme gecerli sonuclari gizler — alisilmis duzeltme label'lari yazilan metni icerecek sekilde tutmak ya da yerlesik filtreyi kabul edip `onDidChangeValue`'yu yalnizca aday kumesini genisletmek icin kullanmaktir.

### Ayiricilar

```typescript
qp.items = [
  { label: 'Recent', kind: vscode.QuickPickItemKind.Separator } as TaskPick,
  ...recent,
  { label: 'All Tasks', kind: vscode.QuickPickItemKind.Separator } as TaskPick,
  ...all,
];
```

Bir ayirici oge secilebilir degildir ve `label` disinda her seyi yok sayar. Gruplamanin dogru yolu budur; label'inda tirelerle sahte bir oge secilebilirdir ve eninde sonunda secilecektir.

## InputBox

```typescript
const name = await vscode.window.showInputBox({
  title: 'New Task',
  prompt: 'Task name',
  value: suggestedName,
  valueSelection: [0, suggestedName.length],  // kolay uzerine yazma icin onceden sec
  placeHolder: 'e.g. build-frontend',
  ignoreFocusOut: true,
  password: false,
  validateInput: text => {
    if (!text.trim()) { return 'Name is required.'; }
    if (!/^[a-z0-9-]+$/.test(text)) { return 'Use lowercase letters, digits, and dashes.'; }
    if (existingNames.has(text)) { return `"${text}" already exists.`; }
    return undefined;   // undefined (ya da null) gecerli demektir
  },
});

if (name === undefined) { return; }   // kapatildi
```

- `validateInput` her tus vurusunda calisir ve bir promise dondurebilir. Hizli tut; aga gitmek zorundaysa icinde geciktir ya da iyimser dogrula ve kabulde yeniden kontrol et. `undefined` olmayan bir mesaj donderdigi surece girdi kabul edilemez.
- Duz bir string yerine bir `InputBoxValidationMessage` (`{ message, severity }`) dondurmek, sert bir hata yerine tikamayan bir uyari gostermeni saglar. Ona guvenmeden once tam sekli guncel `vscode.d.ts`'e karsi dogrula.
- `ignoreFocusOut: true`, odak baska yere gittiginde kutuyu acik tutar. Kullanicinin editore bakmasi gerekebilecek cok adimli akislar icin kullan; kullanicinin otomatik kapanmayi bekledigi hizli tek istemlerde kapali birak.
- `password: true` girdiyi maskeler ama gizli yapmaz. Bu sekilde topladigin sey yine de depolama icin `context.secrets`'a ihtiyac duyar — asla `globalState`'e degil.
- Bos bir string, kapatmadan farkli *gecerli* bir donus degeridir. Dogruluk degil `=== undefined` kontrol et, yoksa hicbir sey yazmayip Enter'a basan kullanici sessizce iptal olarak islenir.

Gercekten cok adimli girdi icin `createInputBox`, `createQuickPick` ile ayni nesne seviyesi kontrolu verir (`step`, `totalSteps`, geri dugmeleri, `onDidChangeValue`).

## Bildirimler

```typescript
const OPEN = 'Open Log';
const DISMISS = 'Not Now';

const choice = await vscode.window.showWarningMessage(
  'Build finished with 3 warnings.',
  OPEN,
  DISMISS,
);

if (choice === OPEN) {
  await vscode.commands.executeCommand('myExt.showBuildLog');
}
```

Donus degeri secilen dugmenin tam string'idir ya da bildirim kapatildiysa veya zaman asimina ugradiysa `undefined`. Satir ici harfi harfine degerler yerine sabitlerle karsilastir ki bir yazim hatasi olu bir dal degil bir derleme hatasi olsun.

Secenek nesnesi asiri yuklemesi `modal` ve oge basina kontrol ekler:

```typescript
const confirm = await vscode.window.showWarningMessage(
  'Delete 12 tasks? This cannot be undone.',
  { modal: true, detail: 'Tasks will be removed from the server.' },
  'Delete',
);
if (confirm !== 'Delete') { return; }
```

`modal: true` cevaplanana kadar editoru bloke eder ve VS Code kendi Cancel dugmesini ekler. Bunu yikici, geri alinamaz eylemler icin sakla. Baska her sey icin bir modal, kullanicilari bir eklentiyi kaldirmaya iten en hizli yoldur.

**Bildirimleri asiri kullanmamak uzerine.** Bir bildirim boler, odagi okuma konumundan calar ve ust uste yigilir. Karar kurali:

| Durum | Yuzey |
| --- | --- |
| Kullanici simdi bir seye karar vermeli | Dugmeli bildirim, ya da yikiciysa modal |
| Kullanicinin az once tetikledigi bir eylem basarisiz oldu | "Open Log" dugmeli `showErrorMessage` |
| Kullanicinin baslattigi devam eden is | `window.withProgress` |
| Ortam durumu (derleme durumu, baglanti) | Durum cubugu ogesi |
| Tani ayrintisi, arac ciktisi, izler | Cikti kanali |
| Rutin basari ("kaydedildi", "bicimlendirildi") | Hicbir sey |

Bildirim olarak "Islem basariyla tamamlandi" neredeyse her zaman yanlistir: kullanici olup bittigini izledi ve bolme, onaylamanin degdiginden daha pahaliya mal olur.

## OutputChannel ve LogOutputChannel

```typescript
const output = vscode.window.createOutputChannel('My Extension');
context.subscriptions.push(output);

output.appendLine(`Starting build for ${folder.name}`);
output.append('.');            // yeni satir yok — ilerleme noktalari
output.show(true);             // true = preserveFocus, imleci CALMA
```

Argumansiz `show()`, odagi panele tasir ve kullaniciyi tus vurusunun ortasinda editorden disari ceker. Kullanici acikca gormek istemedigi surece `true` gecir.

### LogOutputChannel

Tanilar icin kanali `{ log: true }` ile olustur ve bunun yerine seviyeli bir logger al:

```typescript
const log = vscode.window.createOutputChannel('My Extension', { log: true });
context.subscriptions.push(log);

log.trace('resolved config', config);       // kullanici Trace seviyesini ayarlamadikca gizli
log.debug('spawning', binPath, args);
log.info('build started');
log.warn('deprecated setting "myExt.oldKey" in use');
log.error(err instanceof Error ? err : String(err));

log.onDidChangeLogLevel(level => { /* kendi isinin ayrintisini ayarla */ });
```

Bunun duz bir kanala gore kazandirdiklari:

- Her satir otomatik olarak VS Code'un kendi log formatinda bir zaman damgasi ve seviye oneki alir.
- Kullanici, cikti panelinin dislisi menusu ve **Developer: Set Log Level** komutu uzerinden kanal basina ayrinti seviyesini kontrol eder. Ayarin altindaki seviyeler hic yazilmaz, bu yuzden sicak bir yoldaki `log.trace` devre disiyken neredeyse hicbir seye mal olmaz.
- `log.logLevel` ve `onDidChangeLogLevel`, kimsenin gormeyecegi pahali mesajlari kurmayi atlamani saglar.
- Kanal, kullanicilardan hata bildirirken calistirmalari istenen log toplama komutlarina katilir.

**Tani loglamasinin ait oldugu yer burasidir, `console.log` degil.** `console.log`, extension host'un gelistirici araclarina gider — siradan kullanicilarin asla acmadigi ve kolayca disari aktaramadigi bir yer. Bir hata raporunda gormek isteyecegin her sey bir cikti kanalinda olmak zorundadir.

Eklenti basina tek kanal normdur. Birden fazla kanal, gercekten farkli hedef kitleleri olduklarinda gerekcelidir (arac stdout'unu gosteren kullaniciya donuk bir "Build Output", arti tanilar icin bir "My Extension" log kanali), log seviyelerinin yerine gecmek icin degil.

## FileDecorationProvider

Dosya dekorasyonlari, `resourceUri` tasiyan her satira bir rozet (bir ya da iki karakter), bir renk ve bir tooltip ekler — gezginde, acik editor sekmelerinde ve kendi agac view'larinda. Git'in `M`/`U` isaretlerinin arkasindaki mekanizma budur.

```typescript
class TaskDecorationProvider implements vscode.FileDecorationProvider {
  private readonly _onDidChange = new vscode.EventEmitter<vscode.Uri | vscode.Uri[]>();
  readonly onDidChangeFileDecorations = this._onDidChange.event;

  provideFileDecoration(uri: vscode.Uri): vscode.FileDecoration | undefined {
    const status = statusFor(uri);
    if (!status) { return undefined; }   // dekorasyon olmamasi normal cevaptir
    return {
      badge: status === 'failed' ? '!' : undefined,
      color: new vscode.ThemeColor(
        status === 'failed' ? 'errorForeground' : 'gitDecoration.modifiedResourceForeground',
      ),
      tooltip: `Task ${status}`,
      propagate: true,   // rengi ust klasorlere kabart
    };
  }

  refresh(uris: vscode.Uri[]): void { this._onDidChange.fire(uris); }
  dispose(): void { this._onDidChange.dispose(); }
}

const deco = new TaskDecorationProvider();
context.subscriptions.push(deco, vscode.window.registerFileDecorationProvider(deco));
```

Insanlari yakalayan kisitlar:

- `badge` en fazla iki karakterdir. Daha uzun string'ler sarilmaz, kesilir.
- `color`, API'nin her yerinde oldugu gibi bir `ThemeColor` id'si olmalidir.
- Provider gorunur her kaynak icin ve siklikla cagrilir. Tuttugun bir map'ten cevap ver; icinde dosya sistemine stat cekme.
- Dekorasyonlar yalnizca bir `resourceUri`'nin var oldugu yerlere baglanir. `resourceUri` olmayan bir agac ogesi dekore edilemez — bunu ayarlamak icin bir sebep daha.
- Birden fazla eklenti ayni kaynagi dekore eder; VS Code birlestirir ve seninkini dusurebilir. Onemli bir sey icin bir dekorasyonun tek sinyal olmasina guvenme.

---

**Imza kontrolu.** `TreeView.badge`, `LogOutputChannel`, `InputBoxValidationMessage`, `TreeItemLabel` vurgulari ve surukle-birak controller'i orijinal agac view'i API'sinden sonra eklendi ve bazilari kararli hale gelmeden once sekil degistirdi. Yakin zamanda kullanmadigin her seyi `@types/vscode` icindeki guncel `vscode.d.ts`'e ve `package.json` icindeki `engines.vscode` tabanina karsi dogrula — o tabandan yeni bir API sorunsuz derlenir ve kullanicinin daha eski editorunde calisma aninda patlar.
