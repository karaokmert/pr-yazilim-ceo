# Katki Noktalari (Contribution Points)

Bu ekibin en cok kullandigi katki noktalarinin semalari. Tam referans: `code.visualstudio.com/api/references/contribution-points`.

## Icindekiler

- [commands](#commands)
- [menus ve when ifadeleri](#menus-ve-when-ifadeleri)
- [configuration](#configuration)
- [keybindings](#keybindings)
- [views ve viewsContainers](#views-ve-viewscontainers)
- [languages ve grammars](#languages-ve-grammars)
- [Yapay zeka ile ilgili katkilar](#yapay-zeka-ile-ilgili-katkilar)

## commands

```json
"contributes": {
  "commands": [{
    "command": "myExt.doThing",
    "title": "Do The Thing",
    "category": "My Extension",
    "icon": "$(zap)",
    "enablement": "editorLangId == typescript"
  }]
}
```

- **`title`**, kullanicinin palette okudugu seydir. Bir eylem olarak yaz.
- **`category`** onune eklenir ("My Extension: Do The Thing") — komutlarini gruplar ve eklenti adiyla bulunabilir kilar.
- **`icon`** bir `$(codicon-adi)` referansi (codicon listesine bak) ya da acik/koyu gorsel cifti alir. Yalnizca ikonlarin render edildigi yerlerde gorunur, ornegin editor baslik cubuklarinda.
- **`enablement`** false oldugunda komutu soluklastirir. Onu tamamen gizleyen menu `when`'inden farklidir.

## menus ve when ifadeleri

Bir komutu beyan etmek onu komut paleti disinda **hicbir yere** koymaz. Yerlesim `contributes.menus` ile olur:

```json
"menus": {
  "commandPalette": [
    { "command": "myExt.doThing", "when": "editorLangId == typescript" }
  ],
  "editor/context": [
    { "command": "myExt.doThing", "when": "editorHasSelection", "group": "1_modification" }
  ],
  "explorer/context": [
    { "command": "myExt.doThing", "when": "resourceExtname == .json" }
  ],
  "editor/title": [
    { "command": "myExt.doThing", "when": "resourceLangId == markdown", "group": "navigation" }
  ],
  "view/title": [
    { "command": "myExt.refresh", "when": "view == myExt.myView", "group": "navigation" }
  ]
}
```

Yaygin menu konumlari: `commandPalette`, `editor/context`, `editor/title`, `editor/title/context`, `explorer/context`, `view/title`, `view/item/context`, `scm/title`, `terminal/context`, `comments/comment/title`.

**Gruplar siralamayi kontrol eder.** `navigation` en basa gelir ve baslik cubuklarinda ikon olarak render edilir. Digerleri (`1_modification`, `9_cutcopypaste`) sayisal onekine gore siralanir. Grup icinde siralama icin `@n` ekle: `"group": "navigation@2"`.

**Kullanisli `when` baglam anahtarlari:**

| Anahtar | Anlami |
|---|---|
| `editorFocus`, `editorTextFocus` | Editor odakta |
| `editorHasSelection` | Bos olmayan secim |
| `editorLangId == x` | Aktif editorun dili |
| `resourceLangId == x` | Kaynagin dili (gezginde de calisir) |
| `resourceExtname == .x` | Dosya uzantisi |
| `resourceFilename == x` | Tam dosya adi |
| `resourceScheme == file` | URI semasi — sanal workspace'lerde ozellikleri gizlemek icin kullan |
| `explorerResourceIsFolder` | Gezgindeki secim bir klasor |
| `view == viewId` | Hangi view |
| `viewItem == contextValue` | Agac ogesinin `contextValue`'su — oge basina menuler boyle calisir |
| `workspaceFolderCount > 1` | Cok koklu |
| `isWindows`, `isMac`, `isLinux` | Platform |
| `config.myExt.enabled` | Herhangi bir ayarin degeri |

Operatorler: `==`, `!=`, `&&`, `||`, `!`, `=~` (regex), `in`. Kendi anahtarlarini `vscode.commands.executeCommand('setContext', 'myExt.isReady', true)` ile ayarla — arayuzu eklenti durumuna gore kapiya baglamanin standart yolu budur.

Agac ogesi basina menu ogesi yerlestirmek icin `TreeItem` uzerinde `contextValue` ayarla ve `viewItem == oDeger` ile eslestir.

## configuration

```json
"configuration": {
  "title": "My Extension",
  "properties": {
    "myExt.enable": {
      "type": "boolean",
      "default": true,
      "description": "Enable the thing.",
      "scope": "resource"
    },
    "myExt.mode": {
      "type": "string",
      "enum": ["fast", "thorough"],
      "enumDescriptions": ["Quicker, less precise.", "Slower, more precise."],
      "default": "fast",
      "description": "How hard to work."
    },
    "myExt.toolPath": {
      "type": "string",
      "default": "",
      "markdownDescription": "Absolute path to the tool. Leave empty to use `PATH`.",
      "scope": "machine"
    }
  }
}
```

**Anahtarlari her zaman eklenti adiyla namespace'le.** **`scope` gorundugunden daha onemli:**

| Kapsam | Anlami |
|---|---|
| `application` | Yalnizca global; workspace basina ayarlanamaz |
| `machine` | Makine basina; **workspace ayarlariyla gecersiz kilinamaz** |
| `machine-overridable` | Makine varsayilani, workspace gecersiz kilabilir |
| `window` | Varsayilan; pencere/workspace basina |
| `resource` | Dosya/klasor basina — dile ya da klasore ozgu her sey icin dogru olan |
| `language-overridable` | `[typescript]` bloklariyla dil basina |

**Bir yurutulebiliri ya da calistirilan bir yolu adlandiran her sey icin `machine` kullan.** Aksi halde klonlanmis bir depo, commit'lenmis workspace ayarlariyla eklentini keyfi bir binary'ye isaret ettirebilir. Bunu `capabilities.untrustedWorkspaces` icindeki `restrictedConfigurations` ile birlikte kullan.

`markdownDescription` baglantilari ve kod bicimlendirmesini render eder; `deprecationMessage` bir ayari kaldirmadan eskimis olarak isaretler.

## keybindings

```json
"keybindings": [{
  "command": "myExt.doThing",
  "key": "ctrl+alt+t",
  "mac": "cmd+alt+t",
  "when": "editorTextFocus"
}]
```

Kisayollar kit ve paylasilan bir kaynaktir — her eklenti ayni kombinasyonlar icin yarisir. Akorlari (`ctrl+k ctrl+t`) tercih et ve her zaman `when` ile kapsam ver. Yaygin bir kisayolu talep etmeden once catisma olup olmadigini kontrol et.

## views ve viewsContainers

```json
"viewsContainers": {
  "activitybar": [{
    "id": "myExtContainer",
    "title": "My Extension",
    "icon": "resources/icon.svg"
  }]
},
"views": {
  "myExtContainer": [{
    "id": "myExt.myView",
    "name": "Things",
    "when": "myExt.hasThings",
    "icon": "resources/view-icon.svg",
    "contextualTitle": "My Extension Things"
  }]
},
"viewsWelcome": [{
  "view": "myExt.myView",
  "contents": "No things found.\n[Scan Workspace](command:myExt.scan)",
  "when": "!myExt.hasThings"
}]
```

View'lar yeni bir activity bar girdisi yerine mevcut konteynerlere (`explorer`, `scm`, `debug`, `test`) da konabilir — cogu zaman daha iyi secim budur, cunku yeni bir activity bar ikonu kullanicinin ekraninda onemli bir talep demektir.

**`viewsWelcome` yeterince kullanilmiyor.** Bos bir view'i tiklanabilir komut baglantilariyla bir eylem cagrisina cevirir ve bozuk gorunen bir view ile yol gosteren bir view arasindaki farktir. Activity bar ikonlari tek renkli SVG olmalidir.

## languages ve grammars

```json
"languages": [{
  "id": "mylang",
  "aliases": ["My Language"],
  "extensions": [".mylang"],
  "configuration": "./language-configuration.json"
}],
"grammars": [{
  "language": "mylang",
  "scopeName": "source.mylang",
  "path": "./syntaxes/mylang.tmLanguage.json"
}]
```

`language-configuration.json` yorum belirtecleri, parantez ciftleri, otomatik kapanan ciftler ve katlamayi saglar — saglamasi ucuz ve kullanicilar tarafindan hemen fark edilir.

## Yapay zeka ile ilgili katkilar

Chat participant'lari, language model tool'lari ve MCP server provider'lari **stabil API'dir** (chat ve language model icin 1.90'da kesinlesti). Yapay zeka destekli arac gelistirirken ilgilidir:

```json
"chatParticipants": [{
  "id": "myExt.participant",
  "name": "myhelper",
  "fullName": "My Helper",
  "description": "Ask about our internal APIs",
  "isSticky": true
}],
"languageModelTools": [{
  "name": "myExt_lookupThing",
  "displayName": "Look Up Thing",
  "modelDescription": "Looks up a thing by name in the internal registry.",
  "toolReferenceName": "lookupThing",
  "canBeReferencedInPrompt": true,
  "icon": "$(search)",
  "inputSchema": {
    "type": "object",
    "properties": { "name": { "type": "string", "description": "Thing name" } }
  }
}],
"mcpServerDefinitionProviders": [{
  "id": "myExt.mcpProvider",
  "label": "My MCP Servers"
}]
```

`activate()` icinden `vscode.lm.registerTool` ve `vscode.lm.registerMcpServerDefinitionProvider` ile kaydedilir; chat participant'lari ise `vscode.chat.createChatParticipant` ile.

Bunlarin etrafinda tasarim yapmadan once bilinmesi gereken iki kisit: **language model erisimi kullanici onayi gerektirir** ve `lm.selectChatModels()` aktivasyonda degil kullanici tarafindan baslatilan bir eylemden cagrilmalidir. Bunlarin her biri icin minimum `engines.vscode` net olarak belgelenmemis — varsaymak yerine ilgili ozelligin surum notlarindan belirle.
