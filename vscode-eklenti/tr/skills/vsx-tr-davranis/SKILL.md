---
name: vsx-tr-davranis
description: VS Code eklenti ekibinin (mimar, gelistirici, qa-yayinci) ortak calisma standardi. Her karari ayarlayan ic kullanim-yayin titizlik kadranini, hatalari sessiz olan bir API icin dogrula-hatirlama disiplinini, dispose ve gizli bilgi sahipligini, kapsam sinirlarini ve isin nasil raporlanacagini kapsar. Bu skill'i her VS Code eklenti isinin basinda ac — iskelet kurma, ozellik yazma, test, paketleme, yayinlama, inceleme ya da hata ayiklama fark etmez, her seyden once. Ayrica bir isin ne kadar titizlik hak ettigi konusunda karar verilecekte de ac.
---

# VS Code Eklenti Ekibi — Calisma Standardi

Ekipteki her agent bunu onceden yukler. Bu bir kontrol listesi degil; uc ayri uzmanin tek bir muhendisin elinden cikmis gibi is uretmesini saglayan ortak muhakemedir.

Diger skill'ler VS Code hakkinda *neyin dogru oldugunu* soyler. Bu skill *nasil calisilacagini* soyler.

## 1. Titizlik kadrani: ic kullanim mi, yayin mi

Bu ekip iki tur eklenti uretiyor ve neredeyse her karar hangisinde oldugunuza gore bukuluyor. Karar vermeden once bunu netlestir — kimse soylememisse hangisini varsaydigini ve nedenini soyle, sessizce secme.

**Ic kullanim eklentisi.** Kitle, ulasabildigin meslektaslarin. Bir hata bir Slack mesaji ve bir yeniden derleme demek. Dagitim, paylasimli bir klasore ya da CI ciktisina konan bir `.vsix`. Makul olarak atlanabilecekler: pazar yeri sunum cilasi (galeri banner'i, ekran goruntuleri, anahtar kelime ayari), ikon sanati, yabancilar icin yazilmis degisiklik gunlugu nesri.

**Yayinlanan eklenti.** Kitle anonim ve urun sirketin adini tasiyor. Bir hata, 1 yildizli bir yorum ve triyaj edemeyecegin bir destek yuku demek. Bir guvenlik acigi ise bir ifsa. Guncelleme mekanigi onemli, cunku kullanicilarda eski surum kurulu ve onlari yukseltmeye zorlayamazsin.

Kadranin **degistirmedigi** seyler:

- **Guvenlik incelemesi.** Gizli bilgi yonetimi, makineden ne cikiyor ve yetenek beyanlarinin durustlugu — alti meslektas icin de alti bin yabanci icin de ayni titizlikte incelenir. Bir ic eklentinin hassas altyapiya erisimi cogu zaman halka acik olandan *daha fazladir*, daha az degil.
- **Dispose disiplini.** Sizdirilan bir dinleyici, meslektasinin editorunu de bir yabancininki kadar yavaslatir.
- **Dogru manifest.** Yanlis bir katki noktasi ikisinde de ayni sekilde basarisiz olur.

Kadran *sunumu ve surec agirligini* degistirir, *muhendislik butunlugunu* degil. Kendini "nasil olsa ic kullanim" diyerek bir seyi atlarken yakalarsan, bu ikisinden hangisini atladigini kontrol et.

Niyet gercekten bilinmiyorsa isleyen bir varsayilan var: **ileride yayinlanabilirmis gibi kur.** Onden maliyeti kucuk (bir LICENSE dosyasi, temiz bir README, gizli bilgilerin dogru yerde durmasi) ve ekiplerin yakalandigi yer sonradan telafi etmektir — genelde yayinlamaya karar verdikleri hafta.

## 2. Dogrula, hatirlama

Extension API, kendinden emin hafizayi belirli ve sinsi bir sekilde cezalandirir: **yanlis manifest ve yanlis API kullanimi sik sik sessizce basarisiz olur.** Bozuk bir katki noktasi hata firlatmaz — katki sadece hic gorunmez. Yanlis yazilmis bir aktivasyon olayi, eklentinin hic uyanmamasi demektir. Kullanici hicbir sey gormez; varsa hata da, kimsenin acmadigi bir kanalda Output panelinin dibinde durur.

Bu yuzden "sekli su olsa gerek" cumlesi, `package.json`'a girecek hicbir sey ve yakin zamanda kullanmadigin hicbir API imzasi icin yeterli degildir. Bak ve dogrula.

API ayrica hareket ediyor. Aktivasyon olaylari esasli sekilde elden gecirildi, test araclari degistirildi, `vsce` namespace degistirdi ve bazi API yuzeyleri (language model, chat, tools) yeni geldi, hala oturuyorlar. Egitim verisi burada hizli bayatliyor.

Pratik disiplin:

- Manifest semasi, provider arayuzleri ve surume duyarli her sey icin dokumantasyon arama araclarini kullan (context7, `code.visualstudio.com/api` adresindeki resmi dokumanlar).
- **Degistirmeden once projeyi oku.** Depoda halihazirda olan konvansiyonlar senin varsayilanlarini yener. Proje webpack kullaniyorsa, sirf sen esbuild'i tercih ediyorsun diye sessizce onu getirme — neyi neden degistirecegini soyle, karari insana birak.
- Bir seyi dogrulayamiyorsan "dogrulanmadi" de ve neye bakacagini soyle. Isaretlenmis bir belirsizlik faydalidir; kendinden emin yanlis bir cevap birine bir ogle sonrasina mal olur.

## 3. Rol sinirlarini asan sahiplik

Uc kural, o an koda dokunan kisiye aittir. Kimse bunlari bir sonraki agent'a birakamaz.

**Her `Disposable` olusturuldugu anda sahiplenilir.** Ya `context.subscriptions`'a, ya da dogru yasam dongusu aninda dispose edilen daha dar bir torbaya (panel basina, oturum basina) it. Bunun "olsa iyi olur" degil pazarliksiz olmasinin sebebi: extension host, *kullanicinin kurdugu diger tum eklentilerle paylasilir*. Bir sizinti senin eklentinin ozel sorunu degildir — tum editoru yavaslatir ve suc sana degil VS Code'a atilir.

**Gizli bilgiler `context.secrets` icinde yasar.** Asla `globalState`, `workspaceState`, `settings.json` ya da kaynak kodda degil. `globalState` diskte sifrelenmemis durur; ayarlar ise diger makinelere senkronlanir ve hata raporlarina yapistirilir. Bu, ic kullanim eklentileri icin de aynen gecerlidir.

**Yokluk normal bir durumdur, bir kenar durum degil.** Aktif editor yok, workspace klasoru yok, secim bos, cok koklu workspace, kaydedilmemis dokuman — bunlar gercek kullanimda surekli olur. `workspaceFolders[0]`'in var oldugunu varsayan kod, tek bir dosya acan kullanici icin hata firlatan koddur. Bos ve coklu durumlari acikca ele al, ya da ozelligi bilerek daralt ve bunu yaptigini soyle.

## 4. Kendi seridinde kal, ve bunu sesli soyle

Her agent'in bir alani var. Bir is seninkinin disina kaydiginda hatali davranis yardim etmeyi reddetmek degil — kaymayi sessizce yutup uzmanin yapacagindan daha kotu bir is cikarmaktir.

Sinira carptiginda adini koy: *"Bu yeni bir aktivasyon stratejisi gerektiriyor, yani yapisal — mimar almali."* Bu cumle bir satira mal olur ve isi dogru yere yonlendirir. Bir hata duzeltmesi olmasi gereken sirada projeyi sessizce yeniden yapilandirmak, degisiklikleri incelenemez hale getiren seydir.

Sinirlar ve is devri mekanigi `vsx-tr-akis` icinde. Is el degistirirken onu oku.

## 5. Isi raporlamak

Ciktini okuyan kisi genelde terminalini goremez ve seni calisirken izlemedi. Onun icin yaz.

- **Neyin degistigi ve bunun ne anlama geldigiyle basla**, sureci anlatmakla degil.
- **Kararlari tek satirlik gerekce ile bildir.** "esbuild, cunku yeni eklentiler icin guncel varsayilan ve config kucuk kaliyor" — sonraki kisinin tersten cozmesi gereken sessiz bir secim degil, ama uc paragrafllik savunma da degil.
- **Yapmadigin seyi yuzeye cikar.** Kapsam disi kalemler, bilinen bosluklar ve yaptigin varsayimlar bir devrin en degerli kismidir, cunku aksi halde gec fark edilecek seyler bunlardir.
- **Dogrulama konusunda durust ol.** "Testler geciyor", "derleniyor" ve "dogru oldugunu saniyorum" birbirinden cok farkli uc iddiadir. Hangisi elinde, onu soyle. Extension Development Host'u calistirmadiysan, calistirmis gibi ima etme.

Kesinlik, ic rahatlatmaya yegdir. "Bu calisiyor, ama webview CSP'sini Restricted Mode altinda dogrulayamadim" diyen bir rapor, her seyin yolunda oldugunu soyleyenden daha faydalidir.
