# Mevcut Bir Eklentiyi Yeniden Yapilandirmak

Zaten var olan bir projedeki yapisal problemlere tani koymak ve duzeltmeleri incelenebilir kalacak sekilde kapsamlandirmak.

## Icindekiler

- [Kapsamlandirma ilkesi](#kapsamlandirma-ilkesi)
- [Tani koymak](#tani-koymak)
- [Her sey uzerinde aktivasyon](#her-sey-uzerinde-aktivasyon)
- [Bundle yok](#bundle-yok)
- [Dispose deseni yok](#dispose-deseni-yok)
- [Bayat engines ve types](#bayat-engines-ve-types)
- [Manifest kaymasi](#manifest-kaymasi)
- [Her sey extension.ts icinde](#her-sey-extensionts-icinde)
- [Birden fazla duzeltmeyi siralamak](#birden-fazla-duzeltmeyi-siralamak)

## Kapsamlandirma ilkesi

Buyuk patlama seklinde bir yeniden yapilandirma incelenemez ve tehlikelidir, tek ve belirli bir sebeple: yapisal degisiklikle davranis degisikligini karistirir. Sonrasinda bir sey bozuldugunda — ve bozulacaktir — hangi degisikligin sebep oldugunu kimse soyleyemez, bu yuzden duzeltme her seyi geri almak olur; dogru olan kisimlar dahil.

Yani: **bir problemin adini koy, bir duzeltme oner, yalnizca onu degistir.** Dort yapisal problemi olan bir proje, her biri bagimsiz dogrulanabilir ve geri alinabilir dort degisiklik alir.

Daha az bariz ikinci bir sebep var. Mevcut yapi cogu zaman kimsenin yazmadigi bir kisiti kodlar — tuhaf bir derleme adimi bir CI tuhafligi yuzunden vardir, garip bir aktivasyon olayi bir musterinin kurulumu yuzunden. Seyleri tek tek degistirmek o kisitlari, sebebini atfedebilecegin hatalar olarak yuzeye cikarir. Hepsini birden degistirmek onlari bir muamma olarak yuzeye cikarir.

**Bir secimin hata oldugunu varsaymadan once sor.** "Bu webpack kullaniyor; bilincli mi?" bir soruya mal olur ve arada bir seni tasiyici bir seyi kaldirmaktan kurtarir.

## Tani koymak

Yapisal problemlerin cogunu bulan hizli bir tarama:

```bash
# Aktivasyon stratejisi
jq '.activationEvents, .engines, .main, .browser' package.json

# Hic derleme adimi var mi?
jq '.scripts' package.json

# Manifest derleme ciktisi yerine kaynaga mi isaret ediyor?
jq -r '.main' package.json     # "./src/extension.js" ya da bundle edilmemis "./out/..." bir koku

# Paket siniri
cat .vscodeignore 2>/dev/null || echo ".vscodeignore YOK"

# Fiilen ne gonderilecek
npx @vscode/vsce ls | head -50

# Dispose disiplini: kayitlari subscription'larla karsilastir
grep -rn "vscode\.\(commands\|languages\|window\|workspace\)\.register\|createStatusBarItem\|createFileSystemWatcher\|onDid" src/ | wc -l
grep -rn "context\.subscriptions\.push" src/ | wc -l

# Yanlis yerdeki gizli bilgiler
grep -rn "globalState\.update\|workspaceState\.update" src/

# Giris noktasinin boyutu
wc -l src/extension.ts
```

Iki `grep | wc -l` sayimi bir sezgisel yontemdir, kanit degil — bir `push` birkac dispose edilebilir alabilir. Buyuk bir fark arastirmaya deger; kucuk bir fark mutlaka problem degildir.

## Her sey uzerinde aktivasyon

**Belirti:** `"activationEvents": ["*"]`, ya da modern bir engine'de `contributes.commands`'i tekrarlayan uzun bir `onCommand:` listesi.

**Maliyet:** eklenti her pencerede acilis sirasinda aktive olur. `vsce package` ayrica `--allow-star-activation` verilmedikce `*` ile derlemeyi reddeder.

**Duzeltme:** neyin gercekten hazir olmasi gerektigini belirle.

- Komutlar, view'lar ya da diller uzerinden erisilebilen her sey → **olaylari tamamen sil.** VS Code 1.74+ uzerinde otomatik uretilirler (bkz. manifest skill'i).
- Dogal bir tetigi olmayan arka plan isi → `onStartupFinished`.
- Yalnizca belirli projelerle ilgili → `workspaceContains:<glob>`.

**Dogrula:** oncesinde ve sonrasinda `Developer: Show Running Extensions` — eklenti artik acilis aktivasyon listesinde gorunmemeli ve onu cagirdiginda gorunmeli.

Bu genelde mevcut en yuksek degerli yapisal duzeltmedir ve siklikla en kucuk diff'tir.

## Bundle yok

**Belirti:** betiklerde `esbuild`/`webpack` yok, `main` `out/extension.js`'e isaret ediyor, `vsce ls` icinde yuzlerce dosya.

**Maliyet:** buyuk bir `.vsix`, yavas kurulumlar ve daha yavas aktivasyon — her `require` bir dosya okumasidir.

**Duzeltme:** bir bundler ekle (config `derleme-kurulumu.md` icinde), `main`'i paketlenmis ciktiya yonlendir, `.vscodeignore`'u guncelle ve hata ayiklayicinin ihtiyac duydugu watch gorevini ekle.

**Dogrula:** `vsce ls` artik bir avuc dosya gostermeli. Sonra paketle, `.vsix`'i kur ve eklentinin hala aktive oldugunu dogrula — bundle etmek dinamik `require`'lari ve eski yerlesimi varsayan her calisma zamani varlik yolunu bozar ve ikisi de derleme aninda gorunmez.

Dikkat: goreli yolla yuklenen varliklar (webview HTML, gramerler) `.vscodeignore` icinde acikca tutulmali ve `__dirname` yerine `context.extensionUri` uzerinden referans verilmeli.

## Dispose deseni yok

**Belirti:** `registerCommand` ve olay dinleyici sonuclari degiskenlere atanmis ya da yok sayilmis, az sayida `context.subscriptions.push` cagrisi.

**Maliyet:** aktivasyon dongulari boyunca sizdirilan dinleyiciler ve yinelenen kayitlar. Gelistirmede nadiren gorunur sekilde bozulur — uzun bir oturum boyunca editoru yavaslatir ve bu kadar uzun sure hayatta kalmasinin sebebi de tam olarak budur.

**Duzeltme:** her dispose edilebiliri `context.subscriptions`'a it. Daha kisa omurlu kaynaklar icin (webview panelleri, oturum basina watcher'lar) dogru anda dispose edilen kapsamli bir dizi kullan.

Bunu artimli yapmak guvenlidir — her kayit bagimsizdir, bu yuzden buyuk bir supurme yerine diger islerin yaninda inebilir. En cok giris noktasinda kurmak onemlidir, cunku yeni kod taklit yoluyla yazilir.

## Bayat engines ve types

**Belirti:** `engines.vscode` birkac yillik, ya da `@types/vscode` `engines.vscode`'dan yeni.

**Maliyet:** cok dusuk bir taban kullanabilecegin API'leri engeller ve elle aktivasyon olaylari zorlar; engine'in onundeki tipler ise destekledigini iddia ettigin surumde var olmayan API'lere karsi derleme yapar ve bu, bir kullanicinin makinesinde calisma aninda basarisiz olur. `vsce` bu eslemeyi kontrol eder.

**Duzeltme:** desteklenen gercek minimum surume karar ver, ikisini de eslesen caret araliklariyla ona ayarla. Tabani yukseltmek eski VS Code'daki kullanicilar icin **kirici bir degisikliktir** — bir major surum artisina ve degisiklik gunlugune aittir.

`@types/vscode`'un yayinlanan VS Code surumunun gerisinde kaldigini unutma; tabani urun surumunden turetme.

## Manifest kaymasi

**Belirti:** `contributes` icinde handler'i olmayan komutlar, manifest'te olmayan kayitli komutlar, semasi olmadan `getConfiguration()` ile okunan ayarlar.

**Maliyet:** tiklandiginda hata firlatan palet girdileri, gorunmeyen komutlar, arayuzde gorunmeyen ve dogrulamasi olmayan ayarlar.

**Duzeltme:** her iki yonde de uzlastir.

```bash
# Beyan edilmis komutlar
jq -r '.contributes.commands[]?.command' package.json | sort > /tmp/declared.txt
# Kayitli komutlar
grep -rhoE "registerCommand\(\s*['\"]([^'\"]+)" src/ | sed -E "s/.*['\"]//" | sort > /tmp/registered.txt
comm -3 /tmp/declared.txt /tmp/registered.txt

# Kodda okunan ayarlar ile beyan edilmis olanlar
grep -rhoE "get(<[^>]+>)?\(\s*['\"]([^'\"]+)" src/ | sed -E "s/.*['\"]//" | sort -u
jq -r '.contributes.configuration.properties | keys[]' package.json 2>/dev/null | sort
```

Her oksuz bir karardir: olu beyani sil ya da eksik yariyi ekle. Ikisi de kucuktur.

## Her sey extension.ts icinde

**Belirti:** aktivasyonu, komut handler'larini, provider'lari ve is mantigini tutan yuzlerce satirlik bir `extension.ts`.

**Maliyet:** hicbir sey extension host olmadan test edilemez ve her sey incelemede catisir.

**Duzeltme, tek bir supurme yerine artimli olarak:** bir `register(context)` fonksiyonu export eden ozellik modulleri cikar ve saf mantigi **`vscode` import'u olmayan** modullere tasi — bunlar harness olmadan birim testi yapilabilir hale gelir ki gercek odul budur.

Bunu bagimsiz bir refactor olarak degil, ozelliklere dokunuldukca yap. Bin satiri tasiyan saf hareket commit'i incelemesi cok zordur ve ince bir davranis degisikliginin saklandigi yer tam olarak orasidir.

## Birden fazla duzeltmeyi siralamak

Birkac problem bir arada oldugunda sira onemlidir — sonraki duzeltmeler oncekiler tarafindan dogrulanir:

1. **Manifest ve aktivasyon** — en kucuk diff, en buyuk anlik kazanim, kod degisikligi yok.
2. **Bundle etme** — neyin gonderildigini degistirir; derlenmis `.vsix`'i kurarak dogrula.
3. **`.vscodeignore` ve paket incelemesi** — 2. adimin gercekten dusundugun seyi yaptigini teyit eder.
4. **Dispose disiplini** — artimli, sonraki islere yayilmasi guvenli.
5. **Modul cikarma** — en buyuk ve en riskli; sona birak, ozellik ozellik.

Bunlari ayri ayri indir. 2. adim bir seyi bozarsa, bunun 2. adim oldugunu bilmek istersin.
