# Yayin Oncesi Guvenlik ve Izin Incelemesi

Ic ya da halka acik her yayindan once yapilan bilincli kontrol listesi turu. Kendi adimi olarak calistir — teste katmak, atlanmasinin yoludur, cunku gecen bir test paketi tamamlanmis gibi hissettirir.

**Bu, ic eklentiler icin tam gucuyle gecerlidir.** Ic gelistirici araclari siklikla production altyapisinin, kaynak kontrolunun ve ic API'lerin kimlik bilgilerini tutar. Hedef kitle daha kucuktur; patlama yaricapi cogu zaman degildir.

## Icindekiler

- [1. Gizli bilgiler ve kimlik bilgileri](#1-gizli-bilgiler-ve-kimlik-bilgileri)
- [2. Makineden cikan veri](#2-makineden-cikan-veri)
- [3. Yetenek beyanlari](#3-yetenek-beyanlari)
- [4. Bagimliliklar](#4-bagimliliklar)
- [5. Guvenilmeyen girdi](#5-guvenilmeyen-girdi)
- [Raporlama](#raporlama)

## 1. Gizli bilgiler ve kimlik bilgileri

**Kural: kimlik bilgileri `context.secrets` icinde yasar, baska hicbir yerde.**

`context.secrets` asenkrondur ve isletim sistemi anahtarligiyla desteklenir. Alternatiflerin hepsi basarisiz olur:

- `globalState` / `workspaceState` — diskte duz metin JSON.
- `contributes.configuration` (ayarlar) — duz metin, Settings Sync ile makineler arasi senkronlanir ve rutin olarak hata raporlarina ve ekran paylasimlarina yapistirilir.
- Kaynak sabitleri — herkesin acabilecegi `.vsix` icinde gonderilir.
- Pakette gonderilen `.env` — ayni problem, arti bilincli gorunuyor.

Yalnizca bariz isimleri degil, deseni ara:

```bash
# Asla kimlik bilgisi tutmamasi gereken depolama API'leri
grep -rn "globalState\.update\|workspaceState\.update" src/

# Atamalarin yaninda olasi kimlik bilgisi isimleri
grep -rniE "(token|secret|apikey|api_key|password|credential|bearer)\s*[:=]" src/

# Kimlik bilgisi sekilli ayar okumalari
grep -rn "getConfiguration" src/ | grep -iE "token|key|secret|password"

# Gonderilebilecek kimlik bilgisi benzeri dosyalar
find . -name ".env*" -not -path "./node_modules/*"
```

Sonra hicbirinin pakete girmedigini dogrula:

```bash
mkdir -p /tmp/sec && unzip -q *.vsix -d /tmp/sec
grep -rniE "(api[_-]?key|secret|password|bearer )" /tmp/sec/extension/ | grep -v node_modules
```

**Yanlis yerdeki bir gizli bilgi yayini durdurur.** Gelistiriciye doner. Takip maddesi olarak not edilmez, cunku "gelecek sprint tasiriz" kimlik bilgisini gonderir.

Kontrol edilmeye deger bir incelik: `context.secrets` icinde dogru sekilde saklanan ama sonra *loglanan* bir token — bir OutputChannel'a, `console.log`a ya da bir hata mesajina — aynen ifsa olmustur. Loglama yollarini da ara.

## 2. Makineden cikan veri

Her giden cagriyi sirala: `fetch`, `https.request`, `axios`, herhangi bir SDK ve aga ulasan baslatilmis her surec.

Her biri icin uc soruyu cevapla:

1. **Ne gonderiliyor?** Belirli olarak — dosya icerikleri, dosya yollari, workspace adlari ve tanimlayicilarin hepsi ekiplerin varsaydigindan daha hassastir. Kaynak kodun makineden cikmasi bircok kurulus icin ciddi bir ifsadir.
2. **Nereye gidiyor?** Birinci taraf bir uc nokta, ucuncu taraf bir analitik servisinden farkli bir konusmadir.
3. **Kullanici biliyor mu?**

**Telemetri**nin yayinlanan eklentiler icin sert kurallari vardir: onu README'de ifsa et ve kullanicinin genel ayarina saygi goster. VS Code `vscode.env.isTelemetryEnabled` ve `onDidChangeTelemetryEnabled` sunar; kendini yazmak yerine `@vscode/extension-telemetry` kullan, cunku genel ayara senin icin saygi gosterir. Kullanici devre disi biraktiginda telemetri gondermek pazar yeri politikasini ihlal eder ve daha onemlisi, editorun senin adina verdigi bir sozu bozar.

Ic eklentiler icin de ifsa meslektaslara borcludur — onlar bunu bir listeleme sayfasi yerine bir README'de alir.

## 3. Yetenek beyanlari

`capabilities` icindeki her iki bayrak da kodun fiilen yaptigini yansitmalidir. Koda karsi dogrula; manifest'in sozunu kabul etme.

**`untrustedWorkspaces`** — soru sudur: *biri bu eklenti kurulu ama workspace guvenilmez halde kotu niyetli bir depo acarsa, o depo kod calistirilmasina yol acabilir mi?*

Eklenti sunlari yapiyorsa guvenli **degildir** (`supported: false` ya da `"limited"`):

- Yolu workspace ayarlarindan ya da bir workspace dosyasindan gelen bir binary calistiriyor.
- Workspace'ten betikler calistiriyor (`package.json` script'leri, task tanimlari, hook'lar).
- Workspace tarafindan saglanan config'i kod olarak yukluyor ve degerlendiriyor.
- Workspace icerigini onu yorumlayan bir seye geciriyor.

`"limited"` ise, tehlikeli ayarlari `restrictedConfigurations` icinde listele ki guven verilene kadar workspace degerleri yok sayilsin. Bir yurutulebiliri adlandiran her ayar oraya aittir ve ayrica `scope: "machine"` olmalidir.

**`virtualWorkspaces`** — *dosyalar diskte degilken bu calisiyor mu?* Eklenti workspace yollarinda Node `fs` kullaniyorsa, workspace dosyalarina karsi surec baslatiyorsa ya da `uri.fsPath`in gercek oldugunu varsayiyorsa calismaz. **Belirtilmediginde varsayilani `true`dur**, bu yuzden gercek dosyalara ihtiyaci olan bir eklenti bilincli olarak `false` beyan etmelidir, yoksa sessizce basarisiz olacagi bir baglamda sunulur.

## 4. Bagimliliklar

```bash
npm audit
npm audit --production        # fiilen gonderilen
npm ls --all --depth=0
```

Paketlenmis bagimliliklar `.vsix` icinde gonderilir — savunmasiz bir gecisli bagimlilik artik senin eklentinin acigidir ve onu sen dagitiyorsun.

Muhakeme gecerlidir: yalnizca gelistirmede kullanilan bir derleme aracindaki prototip kirlenmesi uyarisi yayin durdurucu degildir; yayinlanan bir eklentide calisma aninda erisilebilir olan her sey oyledir. Onemli olan, denetimin **calistirilmis ve okunmus** olmasi ve duzeltilmeyen her seyin bir gozden kacirma degil bir karar olmasidir.

Ayrica bakmaya deger: son yayindan beri eklenen bagimliliklar. Yeni bir gecisli bagimlilik agaci, islevselligin onu hak edip etmedigini sormak icin iyi bir andir.

## 5. Guvenilmeyen girdi

Tehdit modelinde workspace saldirgan kontrolundedir — herkes bir meslektasina bir depo gonderebilir.

- **Kabuk komutlarini asla birlestirerek kurma.** Argumanlari bir dizi olarak gecir; `;` ya da `$()` iceren bir dosya adi gecerli bir dosya adidir ve bir komut enjeksiyonudur.
- **Webview mesajlarini dogrula.** Webview ayri bir guven baglamidir; yukunu guvenen ve dosya ya da surec isi yapan bir mesaj handler'i bir yetki yukseltme yoludur. Harekete gecmeden once mesaj seklini kontrol et.
- **Workspace ya da kullanici icerigini webview HTML'ine asla kacislanmamis enjekte etme.** Onu `postMessage` uzerinden gonder ve metin olarak ayarla, ya da kacisla.
- **Yol gecisi**: `../` iceren workspace'e goreli bir yol workspace'in disina ulasabilir. Okumadan ya da yazmadan once coz ve icerilmeyi dogrula.
- **Kaynak sinirlari**: dusmanca ya da sadece devasa bir dosya extension host'u takmamali. Dosya boyutlarini sinirla ve surec zaman asimlari ayarla.

## Raporlama

Bes maddenin her birini bir ozet cumlesi olarak degil, sonucuyla birlikte acik bir satir olarak raporla. "Guvenlik incelemesi gecti", hangi kontrollerin fiilen calistigini gizler.

```
Gizli bilgiler: GECTI — token context.secrets icinde; state/ayarlarda kimlik bilgisi yok; loglanmiyor
Veri cikisi:    GECTI — internal-api.example.com'a bir cagri (yalnizca dosya yolu + satir); README'de ifsa edilmis
Yetenekler:     KALDI — untrustedWorkspaces beyan edilmemis; eklenti workspace ayarlarindan
                        myExt.linterPath calistiriyor. supported:"limited" + restrictedConfigurations
                        gerekiyor ve ayar scope:"machine" olmali. YAYINI BLOKE EDER.
Bagimliliklar:  GECTI — npm audit: 2 orta, ikisi de yalnizca dev (derleme araci), gonderilmiyor
Guvenilmeyen g: GECTI — spawn() argüman dizisiyle; webview mesajlari ayirt edici alanla dogrulaniyor
```

Gizli bilgilerde ya da yeteneklerde bir `KALDI` yayini durdurur ve gelistiriciye doner. Geri kalan her sey, onerinle birlikte yuzeye cikarilacak ve insanin karar verecegi bir muhakeme meselesidir.
