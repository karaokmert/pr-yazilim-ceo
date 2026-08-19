# Derleme ve Arac Kurulumu

Bir VS Code eklenti derlemesi icin calisan yapilandirmalar. Bunlar yapistirilacak sablonlar degil,
uyarlanacak baslangic noktalaridir — her blogun yanindaki gerekce, hangi kismin tasiyici hangisinin
proje tercihi oldugunu soyler.

## Icindekiler

- [1. esbuild kurulumu](#1-esbuild-kurulumu)
- [2. webpack alternatifi](#2-webpack-alternatifi)
- [3. Cift masaustu + web derlemesi](#3-cift-masaustu--web-derlemesi)
- [4. tsconfig.json](#4-tsconfigjson)
- [5. .vscode/launch.json](#5-vscodelaunchjson)
- [6. .vscode/tasks.json](#6-vscodetasksjson)
- [7. .vscodeignore](#7-vscodeignore)

---

## 1. esbuild kurulumu

esbuild, eklenti dokumantasyonunun onerdigi bundler'dir. Derleme bir config dosyasi degil duz bir
Node betigidir; asagidaki watch/production ayrimini ve problem matcher eklentisini ekstra arac
olmadan mumkun kilan da budur.

Proje kokunde `esbuild.js`:

```javascript
const esbuild = require('esbuild');

const production = process.argv.includes('--production');
const watch = process.argv.includes('--watch');

/**
 * tasks.json icindeki VS Code problem matcher'inin aradigi tam isaretleri uretir.
 * Bunlar olmadan bir watch derlemesi asla "bitti" diye raporlamaz ve hata ayiklayici
 * preLaunchTask'inda sonsuza kadar bekler. Bkz. bolum 6.
 * @type {import('esbuild').Plugin}
 */
const esbuildProblemMatcherPlugin = {
  name: 'esbuild-problem-matcher',
  setup(build) {
    build.onStart(() => {
      console.log('[watch] build started');
    });
    build.onEnd((result) => {
      result.errors.forEach(({ text, location }) => {
        console.error(`✘ [ERROR] ${text}`);
        if (location) {
          console.error(`    ${location.file}:${location.line}:${location.column}:`);
        }
      });
      console.log('[watch] build finished');
    });
  },
};

async function main() {
  const ctx = await esbuild.context({
    entryPoints: ['src/extension.ts'],
    bundle: true,
    format: 'cjs',
    minify: production,
    sourcemap: !production,
    sourcesContent: false,
    platform: 'node',
    outfile: 'dist/extension.js',
    external: ['vscode'],
    logLevel: 'silent',
    plugins: [esbuildProblemMatcherPlugin],
  });

  if (watch) {
    await ctx.watch();
  } else {
    await ctx.rebuild();
    await ctx.dispose();
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
```

Her secenegin neden oyle oldugu:

- **`external: ['vscode']` zorunludur.** `vscode` modulu calisma aninda extension host tarafindan
  enjekte edilir; diskte yoktur ve cozulemez. Onu bundle etmek, sebebe isaret etmeyen bir hata
  mesajiyla yukleme aninda basarisizlik uretir. Host'un sagladigi ya da paketlenmeden kalmasi
  gereken (yerel bir `.node` eklentisi gibi) baska her modul de bu diziye girer.
- **`format: 'cjs'` + `platform: 'node'`** — masaustu extension host CommonJS yukler. ESM cikti
  yuklenmez.
- **`sourcemap` yalnizca dev'de, `minify` production'da.** Sourcemap'ler breakpoint'lerin bundle
  yerine TypeScript'e inmesini saglayan seydir; ayrica gonderilen boyutu kabaca ikiye katlar ve
  kaynagi ifsa ederler, bu yuzden yayinlanan derlemede kapalidirlar. `sourcesContent: false`, dev
  sourcemap'ini dosyalari gomme yerine diskteki dosyalara referans vererek kucuk tutar — kaynaklar
  orada oldugu icin lokalde sorun degil.
- **`logLevel: 'silent'` + eklenti.** esbuild'in kendi ciktisi bastirilir ki konsol formatinin
  sahibi eklenti olsun. Eklentiyi cikarirsan bunu da cikar, yoksa hata raporlamasini tamamen
  kaybedersin.
- **`esbuild.build()` yerine `esbuild.context()`** — bir context hem `.watch()` hem de tek seferlik
  `.rebuild()` destekler, boylece tek betik her modu kapsar.

Eslesen `package.json` betikleri:

```json
{
  "main": "./dist/extension.js",
  "scripts": {
    "compile": "npm run check-types && node esbuild.js",
    "watch": "npm-run-all -p watch:*",
    "watch:esbuild": "node esbuild.js --watch",
    "watch:tsc": "tsc --noEmit --watch --project tsconfig.json",
    "check-types": "tsc --noEmit",
    "package": "npm run check-types && node esbuild.js --production",
    "vscode:prepublish": "npm run package"
  }
}
```

**esbuild tip kontrolu yapmaz.** Tipleri soyup uretir; bir tip hatasi mutlu mesut bundle edilir ve
calisma aninda patlar. `check-types`'in (`tsc --noEmit`) ayri calismasinin sebebi budur — derlemeden
once bir kez ve watch modunda surekli olarak `watch:tsc` seklinde. Bunu atlamak, bir esbuild eklenti
kurulumunun yerine gectigi tsc kurulumundan daha kotu hale gelmesinin en yaygin yoludur.

`vscode:prepublish`, `vsce package` / `vsce publish` tarafindan otomatik calistirilir; gonderilen
`.vsix`'in lokalde en son ne derlendiyse o degil, production bundle'i icermesini garanti eden sey
budur.

---

## 2. webpack alternatifi

webpack'i somut bir sebep varsa kullan: mevcut bir ekip konvansiyonu ya da esbuild'in
karsilayamadigi loader'lar. Daha yavastir ve config daha buyuktur; varsayilan olarak bir avantaji
yoktur.

`webpack.config.js`:

```javascript
'use strict';

const path = require('path');

/** @type {import('webpack').Configuration} */
const extensionConfig = {
  target: 'node',
  mode: 'none', // --mode CLI bayragiyla ayarlanir; 'none' surpriz varsayilanlari onler
  entry: './src/extension.ts',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'extension.js',
    libraryTarget: 'commonjs2',
  },
  externals: {
    vscode: 'commonjs vscode', // esbuild'deki ayni zorunlu kural: host saglar
  },
  resolve: {
    extensions: ['.ts', '.js'],
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        exclude: /node_modules/,
        use: [{ loader: 'ts-loader' }],
      },
    ],
  },
  devtool: 'nosources-source-map',
  infrastructureLogging: {
    level: 'log', // tasks.json icindeki webpack problem matcher'i icin gerekli
  },
};

module.exports = [extensionConfig];
```

Notlar:

- `externals: { vscode: 'commonjs vscode' }`, `external: ['vscode']`in webpack yazilisidir.
- `ts-loader` derlerken tip kontrolu yapar, bu yuzden esbuild'in ihtiyac duydugu ayri `check-types`
  adimi burada gerekmez.
- `devtool: 'nosources-source-map'` kaynagi gommeden stack trace'leri esler. Tam breakpoint
  sadakati istiyorsan gelistirme sirasinda `source-map` kullan ve her iki durumda da sourcemap'leri
  `.vscodeignore` ile `.vsix` disinda tut.
- `infrastructureLogging.level: 'log'` kozmetik degildir — yerlesik `$ts-webpack-watch` matcher'i
  derleme baslangic/bitisini algilamak icin o ciktiyi ayristirir.

Betikler: `"compile": "webpack"`, `"watch": "webpack --watch"`,
`"package": "webpack --mode production --devtool hidden-source-map"`.

---

## 3. Cift masaustu + web derlemesi

Bir web eklentisi Node'da degil bir **Web Worker**'da calisir. Ikisini birden desteklemek, tek bir
kaynak agacindan iki bundle uretmek ve ikisini de manifest'te beyan etmek demektir.

```javascript
const shared = {
  bundle: true,
  format: 'cjs',           // her iki host da CommonJS yukler
  minify: production,
  sourcemap: !production,
  external: ['vscode'],
  logLevel: 'silent',
  plugins: [esbuildProblemMatcherPlugin],
};

const nodeCtx = await esbuild.context({
  ...shared,
  entryPoints: ['src/extension.ts'],
  platform: 'node',
  outfile: 'dist/extension.js',
});

const webCtx = await esbuild.context({
  ...shared,
  entryPoints: ['src/web/extension.ts'],
  platform: 'browser',
  outfile: 'dist/web/extension.js',
});
```

Manifest tarafi:

```json
{
  "main": "./dist/extension.js",
  "browser": "./dist/web/extension.js"
}
```

`main` masaustu host tarafindan, `browser` web host tarafindan kullanilir. Bir eklenti yalnizca
birini ya da ikisini birden beyan edebilir; onu tarayici tabanli bir VS Code'da kurulabilir yapan
sey `browser` beyanidir.

### Web bundle'ini sekillendiren kisitlar

- **Node API'si yok.** `fs` ve `child_process` bir Web Worker'da yoktur. Node global'leri de yoktur:
  `process`, `os`, `path`, `util`, `url`, `setImmediate`. Web giris noktasindan erisilebilen her sey
  bunlardan kacinmali. `fs` yerine workspace dosya sistemi API'lerini kullan; surec baslatmanin ise
  bir karsiligi yok — o ozellik web'de basitce sunulamaz.
- **Her zaman tek dosya.** `importScripts` ve dinamik `import()` kullanilamaz, yani kod bolme masada
  degildir. Web bundle'i tam olarak tek bir cikti dosyasi olmalidir.
- **`require()` bir shim'dir** ve yalnizca `require('vscode')`u cozer. Bundle'dan sag cikan baska
  herhangi bir calisma zamani `require`i hata firlatir.

Alisilmis yapi, yalnizca web-guvenli modulleri import eden ayri bir `src/web/extension.ts` girisi ve
yalnizca masaustu girisinin arkasinda tutulan node-ozel koddur.

### Nasil kontrol edilir

Bunu kaynaktan akil yurutme. Uretilen urunu kontrol et:

```bash
# 1. Web cikti dizini altinda tam olarak tek dosya olmali.
ls -R dist/web

# 2. Node built-in'lerine bundle icinden erisilememeli.
grep -nE "require\((['\"])(fs|path|os|child_process|util|url)\1\)" dist/web/extension.js

# 3. Sag kalan tek require 'vscode' olmali.
grep -oE "require\([^)]*\)" dist/web/extension.js | sort -u
```

2. adimdaki herhangi bir eslesme, web girisinden node-ozel bir module erisilebildigi anlamina gelir —
izini surup kapiya bagla. Mevcutsa daha temiz bir kontrol: eklentiyi web extension host test
kosucusu altinda calistir; o, bir metin eslesmesine degil gercekten eksik olan global'e takilir.

---

## 4. tsconfig.json

```jsonc
{
  "compilerOptions": {
    "module": "Node16",
    "target": "ES2022",
    "lib": ["ES2022"],
    "moduleResolution": "Node16",
    "outDir": "out",
    "rootDir": "src",
    "sourceMap": true,
    "strict": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true
  },
  "exclude": ["node_modules", ".vscode-test"]
}
```

**`module`/`target`'i varsaymak yerine guncel dokumana karsi dogrula.** Extension host, VS Code'un
paketli Node'unu calistirir ve o surum VS Code surumleriyle hareket eder — bugun onerilen cift, eski
bir egitim dokumanindaki ya da uretilmis bir sablondaki cift olmak zorunda degil. Host'un
destekledigin den yukseg ini hedeflemek, host'un ayristiramayacagi sozdizimi uretir; cok asagiyi
hedeflemek ise yalnizca daha kotu cikti uretir.

Alan alan:

- **`lib`**, `target` ile eslesmeli ve node hedefli bir eklenti icin `"DOM"` icermemeli. DOM tipleri,
  extension host'ta cokecek kod icin `document.querySelector` yazip temiz derlemeni saglar. Webview
  betikleri ayri bir derleme birimidir ve kendi DOM lib'lerine sahip olabilir.
- **`outDir` / `rootDir`** — bir bundler varken `outDir` cogunlukla tip kontrolu ve test derlemeleri
  icindir; gonderilen urun esbuild uzerinden `dist/`'ten gelir. `rootDir: "src"` tutmak dizin seklini
  `out/` icinde korur ki bu, test kosucusunun derlenmis test dosyalarini bulmasi acisindan onemlidir.
- **`sourceMap: true`** — breakpoint'lerin TypeScript'e geri eslenmesi icin gerekli. Bundler ayrica
  kendi sourcemap'ini uretir; bundle'i mi yoksa tsc ciktisini mi hata ayikladigina bagli olarak her
  iki yol da onemlidir.
- **`strict: true`** — VS Code API'si surekli istege bagli degerler dondurur (`activeTextEditor`,
  `workspaceFolders`, provider sonuclari). Strict mode, "kullanici hayal etmedigim bir durumdaydi"
  calisma zamani cokmelerini derleme hatalarina cevirir.
- **`skipLibCheck: true`** yaygin olarak ayarlanir cunku bagimliliklardaki `.d.ts` dosyalarinin tip
  kontrolunu atlar. O olmadan, bir gecisli bagimliligin baska biriyle catisan tipler gondermesi,
  senin duzeltemeyecegin bir sebeple derlemeni bozar. Kendi kodunun kontrolunu zayiflatmaz.

Tip paketi eslemesi de buraya ait: **`@types/vscode`, `engines.vscode` tabaninda ya da altinda
olmali**, ikisinde de eslesen caret araliklariyla — orn. `"engines": { "vscode": "^1.X.0" }` ile
`"@types/vscode": "^1.X.0"`. Engine'in onundeki tipler, destekledigini iddia ettigin en eski surumde
eksik olan API'lere karsi derleme yapar. Ayrica `@types/vscode`, yayinlanan VS Code surumunun
gerisinde kalir; bu yuzden "kurulu olan VS Code'um" yazilacak yanlis sayidir — yayinlanan guncel tip
surumune bak ve tabani gercekten desteklemeyi amacladigin bir surume ayarla.

---

## 5. .vscode/launch.json

```jsonc
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run Extension",
      "type": "extensionHost",
      "request": "launch",
      "args": ["--extensionDevelopmentPath=${workspaceFolder}"],
      "outFiles": ["${workspaceFolder}/dist/**/*.js"],
      "preLaunchTask": "${defaultBuildTask}"
    },
    {
      "name": "Extension Tests",
      "type": "extensionHost",
      "request": "launch",
      "args": [
        "--extensionDevelopmentPath=${workspaceFolder}",
        "--extensionTestsPath=${workspaceFolder}/out/test/suite/index"
      ],
      "outFiles": [
        "${workspaceFolder}/dist/**/*.js",
        "${workspaceFolder}/out/test/**/*.js"
      ],
      "preLaunchTask": "${defaultBuildTask}"
    }
  ]
}
```

- **`--extensionDevelopmentPath`**, ikinci VS Code penceresini bu projeye yonlendirir ki eklentiyi
  pazar yerinden degil kaynaktan yuklesin.
- **`--extensionTestsPath`**, derlenmis test paketi girisine isaret eder — dikkat, bu `out/` (tsc)
  yoludur, paketlenmis `dist/` yolu degil. Testler tipik olarak bundle edilmez, `tsc` ile derlenir,
  cunku test kosucusu tek tek paket dosyalarini yukler.
- **`outFiles`**, fiilen yuklenen sey neyse ona isaret etmeli. Manifest'in `main`'i
  `dist/extension.js` yuklerken bu `out/**/*.js`'e isaret ediyorsa, hata ayiklayici calisan kodun
  sourcemap'ini bulamaz ve breakpoint'ler dogrulanmamis (ici bos daire) gorunur ve hicbir zaman
  tetiklenmez. Hem paketlenmis kod hem tsc ile derlenmis testler devredeyken ikisini de listele.

### Bayat bundle arizasi

`preLaunchTask`, baslatmadan once derleyen seydir. Yanlis ayarla ve ariza sessiz ve gercekten kafa
karistirici olur: **hata ayiklayici basariyla baslar ve bir onceki derlemeyi calistirir.** Duzenlemen
orada degildir, yeni koddaki breakpoint'ler hic tetiklenmez ve bariz sonuc — "kodum calistirilmiyor"
— yanlistir.

Yanlis ayarlamanin iki yolu:

1. **Tamamen eksik.** Hicbir sey derlemez; her zaman diskte ne varsa onu hata ayiklarsin.
2. **Isim uyusmazligi.** String, `tasks.json` icindeki bir gorevin `label`i ile tam olarak eslesmeli.
   `${defaultBuildTask}` bunu asar; `"group": { "kind": "build", "isDefault": true }` ile isaretlenmis
   goreve cozulur ve bu yuzden kayabilecek bir ismi sabit yazmaktan tercih edilir.

Bayat bundle'dan suphelendiysen `dist/extension.js`'in degisiklik zamanini son duzenlemene karsi
kontrol et. Aksi halde bir saate mal olan bir sorunun bir saniyelik cevabidir.

---

## 6. .vscode/tasks.json

```jsonc
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "watch",
      "dependsOn": ["npm: watch:tsc", "npm: watch:esbuild"],
      "presentation": { "reveal": "never" },
      "group": { "kind": "build", "isDefault": true }
    },
    {
      "type": "npm",
      "script": "watch:esbuild",
      "group": "build",
      "problemMatcher": "$esbuild-watch",
      "isBackground": true,
      "label": "npm: watch:esbuild",
      "presentation": { "group": "watch", "reveal": "never" }
    },
    {
      "type": "npm",
      "script": "watch:tsc",
      "group": "build",
      "problemMatcher": "$tsc-watch",
      "isBackground": true,
      "label": "npm: watch:tsc",
      "presentation": { "group": "watch", "reveal": "never" }
    }
  ]
}
```

Bilesik `watch` gorevi varsayilan derleme gorevidir, boylece launch.json icindeki
`${defaultBuildTask}` ona cozulur ve hem bundler watch'unu hem tip kontrolu watch'unu calistirir.

### Arka plan problem matcher'i neden hata ayiklamanin calisip calismayacagini belirler

Bir watch gorevi asla sonlanmaz. Bu yuzden VS Code, derlemenin bittigi sinyali olarak "surec cikti"yi
kullanamaz — gorevin **ciktisini** okumak zorundadir. Problem matcher'in `background.beginsPattern` ve
`endsPattern` alanlari o sozlesmedir: cikti `beginsPattern` ile eslestiginde VS Code bir derlemeyi
devam ediyor sayar; `endsPattern` ile eslestiginde derleme bitmis sayilir ve hata ayiklama oturumunun
baslamasina izin verilir.

**`endsPattern` hicbir zaman eslesmezse F5 sonsuza kadar takilir** ve hicbir hata gostermez — VS Code
hala calistigina inandigi bir derlemeyi bekliyordur. Bu, en yaygin "baslamadan once oylece takiliyor"
kurulumlarindan biridir ve teknik olarak hicbir sey yanlis olmadigi icin sessizdir.

Bolum 1'deki `esbuildProblemMatcherPlugin` tam olarak bunun icin vardir. esbuild kendi basina boyle
isaretler uretmez; eklenti `[watch] build started` ve `[watch] build finished` yazdirir ve
`$esbuild-watch` tam olarak o string'lerle eslesir. **`problemMatcher: "$esbuild-watch"`i korurken
eklentiyi kaldirmak F5'i bozar.** Ikisi, iki dosyadaki tek bir mekanizmadir.

Ciktisi yerlesik bir matcher ile eslesmeyen ozel bir derleme betigi kullaniyorsan desenleri satir ici
tanimla:

```jsonc
{
  "problemMatcher": {
    "owner": "custom",
    "fileLocation": ["relative", "${workspaceFolder}"],
    "pattern": {
      "regexp": "^(.*):(\\d+):(\\d+):\\s+(warning|error):\\s+(.*)$",
      "file": 1, "line": 2, "column": 3, "severity": 4, "message": 5
    },
    "background": {
      "activeOnStart": true,
      "beginsPattern": "^\\[watch\\] build started$",
      "endsPattern": "^\\[watch\\] build finished$"
    }
  }
}
```

Takilmaya tani koymak: gorev terminalini ac (Terminal → Run Task ya da gorev cikti paneli) ve
derlemenin fiilen ne yazdirdigini oku. Karakter karakter `endsPattern` ile karsilastir. Uyusmazlik
genelde degismis bir log string'i ya da artik eslesmeyen bir sabitlenmis regex'tir.

---

## 7. .vscodeignore

`.vscodeignore`, gonderilen `.vsix`'ten dislar. `.gitignore` sozdizimini kullanir ama amaci terstir —
burasi paket siniridir, kaynak kontrolu degil.

### Disliyici liste tarzi (daha basit, dokuman ornegiyle uyumlu)

```
.vscode/**
.vscode-test/**
node_modules/**
out/**
src/**
.gitignore
.yarnrc
esbuild.js
vsc-extension-quickstart.md
**/tsconfig.json
**/eslint.config.mjs
**/*.map
**/*.ts
```

Bundle edilmis bir eklenti icin belgelenmis ornek `.vscode`, `node_modules`, `out/`, `src/`,
`tsconfig.json`, `webpack.config.js` ve `esbuild.js`'i dislar — bu liste, arti sourcemap'ler ve
basibos TypeScript.

### Her seyi disla-sonra-yeniden-dahil-et tarzi (daha guvenli varsayilan)

```
# Her seyi disla...
**

# ...sonra yalnizca gonderileni yeniden dahil et.
!dist/**
!package.json
!README.md
!CHANGELOG.md
!LICENSE
!icon.png
!media/**
!syntaxes/**

# Yeniden dahil etmeler istenmeyen seyleri geri cekebilir; onlari tekrar disla.
!dist/**/*.map
dist/**/*.map
```

Bu tarz kapali basarisiz olur: sonradan eklenen yeni bir dizin sessizce gonderilmek yerine varsayilan
olarak dislanir. Disliyici liste tarzi ise acik basarisiz olur ve kimlik bilgileriyle ic notlarin
yayinlanmis paketlere boyle girer. Proje zaten digerini kullanmiyorsa bu tarzi tercih et.

Olumsuzlamanin siraya bagli oldugunu ve yeniden dahil edilen bir dizinin tum alt agacini getirdigini
unutma — yukaridaki sondaki `dist/**/*.map`in var olma sebebi, `!dist/**`in aksi halde production
sourcemap'lerini geri cekmesidir.

### Gonderilmesi gerekenler

Paketlenmis cikti (`dist/`), `package.json`, README, CHANGELOG, LICENSE, ikon ve tum calisma zamani
varliklari: webview HTML/CSS/JS, gorseller, dil gramerleri, snippet'ler, temalar. **Calisma zamani
varliklari**, her-seyi-disla tarzinin **alisilmis kurbanlaridir** — eklenti sorunsuz kurulur ve sonra
bir webview bos acilir, cunku yukledigi HTML hic paketlenmemistir.

### Bu dosyayi okuyarak degil, derlenmis paketi inceleyerek dogrula

Bir `.vscodeignore` okunarak dogrulanamaz. Sondaki bir slash, bir olumsuzlama ile sonraki bir desen
arasindaki siralama sorunu ya da alt agacini surukleyen yeniden dahil edilmis bir dizin — hepsi neyin
eslestigini metinde gorunmeyen sekillerde degistirir. Paketi derle ve iceriklerini listele:

```bash
npx @vscode/vsce ls          # derlemeden, neyin paketlenecegini gosterir
npx @vscode/vsce package     # .vsix'i uret
unzip -l my-extension-0.0.1.vsix
```

Gercek dosya listesini oku. Her calisma zamani varliginin mevcut oldugunu ve `src/`, testlerin,
`.env`'in ve production sourcemap'lerinin olmadigini dogrula. Ignore dosyasi ya da proje yerlesimi her
degistiginde bunu yap — gercek soruyu cevaplayan tek kontrol budur. Tam paketleme dogrulama proseduru
`vsx-tr-yayin` icinde yasar.
