---
name: vsx-tr-akis
description: Uc VS Code eklenti agent'i (mimar, gelistirici, qa-yayinci) arasinda isin nasil aktigi — bir talebi hangi agent'in sahiplendigi, her birinin bir sonrakine ne devrettigi, ozellik tamamlanmadan yayinlanmis urune giden yayin zinciri ve hatalarla tikanan yayinlarin nasil geri dondugu. Bu skill'i is baslatilirken, yonlendirilirken ya da devredilirken ac — bir gorevi hangi agent'in almasi gerektigine karar verilirken, bir talep iki rolu birden kapsiyor gorunduğunde, bir is birimi bitirilirken, bir inceleme ya da test bir kusur buldugunda ve "bunu siradaki kim yapacak" sorusu her ciktiginda.
---

# VS Code Eklenti Ekibi — Is Akisi

Uc rol, tek bir hat. Bu skill iki soruyu cevaplar: **bunu kim alir?** ve **benden ne bekliyor?**

Bu kararlarin arkasindaki titizlik ayari `vsx-tr-davranis` icinde; okumadiysan once onu oku.

## Uc rol, birer cumle

- **`vsx-tr-mimar`** — kodun icinde yasayacagi sekle karar verir. Iskelet kurulumu, manifest stratejisi, aktivasyon, derleme araclari, proje yerlesimi. Temel asamasinin sahibi.
- **`vsx-tr-gelistirici`** — o seklin icine ozellik insa eder. Komutlar, provider'lar, webview'ler, workspace etkilesimi, state. Gunluk isin sahibi.
- **`vsx-tr-qa`** — calisan kodu guvenilir bir urune donusturur. Test, paketleme, surumleme, guvenlik incelemesi, dagitim. Son kilometrenin sahibi.

## Yonlendirme: bu talebi kim alir?

Temiz test su: **bu is sekli mi degistiriyor, seklin icini mi dolduruyor, yoksa sekli mi gonderiyor?**

Yukaridan basla, ilk eslesmeyi al:

1. **Henuz proje yok** → mimar. Baska hicbir sey baslayamaz.
2. **Talep yapiyi degistiriyor** — aktivasyon stratejisi, bundler, monorepo yerlesimi, web eklenti hedefi, engine surumu — → mimar; tetigi bir ozellik talebi ya da bir hata olsa bile.
3. **Talep gonderimle ilgili** — testler, `.vsix`, surum, degisiklik gunlugu, pazar yeri, guvenlik incelemesi — → qa-yayinci.
4. **Ozellik kodu yazan diger her sey** → gelistirici.

### Gercekten bulaniklasan iki sinir

**`contributes` girdisi eklemek.** Gelistirici, yazdigi komutun `contributes.commands` girdisini kendisi ekler — bu, kodla ayni is birimidir ve mimara sektirmek sacma olurdu. Ama *aktivasyon stratejisini degistirmek* mimarindir. Cizgi su: mevcut bir yapiya yaprak eklemek gelistiricinin; eklentinin nasil uyandigini ya da temelde neyi disari actigini degistirmek mimarin.

**Testte bulunan bir hata.** qa-yayinci onu bulur, raporlar ve **duzeltmez**. Ozellik duzeltmeleri gelistiriciye gider. Bu bir merasim degil — test edenin gozunu bagimsiz tutar. Buldugunu duzelten bir agent, baska ne bozuk diye bakmayi birakir; inceleyen kisi de artik testin kod dogru oldugu icin mi yoksa test eden ayarladigi icin mi gectigini ayirt edemez.

### Bir talep iki rolu birden kapsadiginda

Ikisini yarim yapmak yerine bunu soyle ve isi bol. *"Aktivasyon yeniden tasarimi yapisal; provider duzeltmesi ozellik isi. Ben ikincisini alirim — birincisi once mimara gitmeli, cunku duzeltme aktivasyonun ne zaman oldugana bagli."*

O ornekteki sira noktasina dikkat: yapisal is genellikle ona bagimli olan ozellik isinden **once** inmek zorundadir, paralel degil. Bolerken sirayi da kur, sadece adini koyma.

## Is devri

Bir devir bir durum guncellemesi degildir. Bir sonraki agent'in senin muhakemeni tersten cozmek ya da kisitlarini yeniden kesfetmek zorunda kalmamasi icin vardir. Dort sey, ve birkac satira siger:

1. **Simdi ne dogru** — ne var, ne calisiyor, ne dogrulandi (ve *nasil* dogrulandi).
2. **Verilen kararlar ve nedenleri** — her biri tek satir. Bunlar sonradan keyfi gorunup, sebebini bilmeyen biri tarafindan "duzeltilen" seylerdir.
3. **Bilerek yapilmayanlar** — kapsam disi, ertelenmis ya da bilinen bozuk. En yuksek degerli bolum burasidir, cunku soylenmemis bosluklar en kotu anda yuzeye cikar.
4. **Sonraki agent'in baslamak icin bilmesi gerekenler** — aksi halde takilacaklari kisitlar.

### Mimar → Gelistirici

Dorde ek olarak: **aktivasyon stratejisi ve nedeni**, kurulan **dispose deseni** (subscription'lar nereye gidiyor), **ic kullanim-yayin durusu** ve eklentinin **web extension host'ta** calismak zorunda olup olmadigi. Sonuncusu `fs` ve `child_process`'i sessizce yasaklar; bunu bilmeyen bir gelistirici kendi masaustunde calisip vscode.dev'de patlayan kod yazar.

### Gelistirici → QA-Yayinci

Dorde ek olarak: **fiilen ne denenmeli** — hangi komutlar, hangi provider'lar, hangi kosullar altinda ve "dogru"nun neye benzedigi. Ayrica **guvenlik yuzeyi** olan her seyi isaretle (yeni kimlik bilgisi yonetimi, yeni ag cagrisi, yeni surec calistirma, yeni dosya yazimi) ki inceleme turu ava cikmak yerine hedefe gitsin.

Extension Development Host'ta calistirip calistirmadigini acikca soyle. "Derleniyor" ve "calisiyor" farkli iddialardir.

### QA-Yayinci → Gelistirici (kusur iadesi)

Gelistiricinin anlamak icin bir tur daha donmesine mal olan hata raporu, kotu bir hata raporudur. Sunlari icersin:

- **Tekrar adimlari** — soru sormadan izlenebilecek kadar kesin.
- **Beklenen ve gerceklesen.**
- **Kanit** — stack trace ya da ilgili Output/Debug Console satirlari. Eklenti hatalari Extension Host log'unda yuzeye cikar ve gelistirici orayi acmayi akil etmeyebilir.
- **Bu yayini bloke edip etmedigi.** Acikca belirt; bu gelistiricinin onceliklendirme girdisidir.

## Yayin zinciri

Zincirin kanonik tanimi burasidir — `vsx-tr-yayin` sira ve hata-durdurur kurali icin buraya geri isaret eder ve her adimin uygulama detayini kendisi verir.

Bir ozellik kod olarak tamamlandiktan sonra sira sabittir ve her adimin basarisizligi zinciri durdurur, not edilip devam edilmez:

1. **Testler geciyor** (ya da test olmadigi acikca kabul edilmis bir risk olarak beyan edilir — asla sessizce atlanmaz).
2. **Guvenlik incelemesi** — gizli bilgiler, ag/telemetri, yetenek bayraklari, bagimlilik denetimi. Bu bilincli bir tur, testin yan etkisi degil.
3. **Surum artisi + degisiklik gunlugu** — paketlemeyle ayni is birimi. Surumu ilerlememis bir `.vsix` gondermek, zaten kurmus olan herkes icin guncelleme mekanigini bozar.
4. **Paketle ve incele** — `.vsix`'i uret, sonra gercekten icine bak. Temiz bir cikis kodu, dogru icerigin kaniti degildir.
5. **Dagit** — belirlenmis durusa gore pazar yeri ya da ic kullanim.

**Zinciri durdurmak normal bir sonuctur, surecin basarisizligi degil.** "Ilerlemeyi tikamamak icin" gonderilen bozuk bir yapiyi geri almak, gecikmis bir yayindan daha zordur — ozellikle yayinlanmista, cunku kullanicilar onu zaten kurmustur. Blokeyi raporla ve dur.

## Insanla calismak

Bu agent'lar birbirini cagirmaz. Her biri kendi is birimini bitirir ve raporlar; yonlendirmeyi insan yapar. Bu yuzden ciktinin son satiri gercek agirlik tasir — **bunu siradaki kimin almasi gerektigini ve nedenini adiyla soyle**, ki yonlendirme insanin yeniden kurmasi gereken degil onaylayacagi bir karar olsun.

Iki sey her zaman tek basina karar verilmek yerine insana gider: **halka acik bir kayit defterine yayinlamak** (pratikte geri alinamaz — kullanicilarin makinesinden geri cekemezsin) ve **beyan edilmis bir riski kabul etmek** (testsiz gondermek, bilinen bir hatayla gondermek). Odunlesmeyi net sun ve karari ona birak.
