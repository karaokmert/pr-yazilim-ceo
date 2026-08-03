# Fabrika neye göre ölçülür — kuruluş oturumundan çıkarıldı

Tarih: 2026-08-03 (gece)

Mert sordu: *"Fabrikamız ne kadar iyi?"* — ve itiraz etti: ölçülecek şey ürettiği ürün
değil, **kendi yapılanması** (*"önce kendisi bizim istediğimiz gibi mi, onu bilmezsek
ürettikleri çöp olur"*).

İtiraz doğruydu ama bir eksik vardı: *"bizim istediğimiz gibi"* bir ölçüt değil, bir
dilek. Ölçüt yazılı değildi — **ta ki kuruluş oturumu okunana kadar.**

## Kaynak ve yöntem

`~/.claude/projects/-Users-karaok-p-ozel-yazilim-skill-project/a6c6fcb6-...jsonl`
— 13,5 MB, 6736 satır, 869 kullanıcı mesajı, 2026-07-31 23:26 → 08-03 11:39.

Bütün okunamadı (bağlamın birkaç katı). Dört paralel tarama yapıldı: niyet, kararlar,
kronoloji, zayıf noktalar. **Yöntem sınırı: taramalar anahtar kelimeye dayalı** — o
kelimelerle söylenmemiş bir şey kaçmış olabilir.

Aşağıdaki alıntılar Mert'in kendi cümleleri, birebir.

## Fabrikanın ölçütü — dört şart

### Bir: sıfırdan üretme

> *"OY v8 i düzelt bir kriter değil, sonuç adımı. Bizim bu ekipten beklentimiz OY v8
> hiç olmasaydı onu üretecekleri adımları bilemeleriydi."*

Bu ana ölçüt. Fabrika mevcut bir takımı onaran değil, **yokken kurabilen** ekip olmalı.

### İki: alan bağımsızlığı

> *"PR Yazılım için yazılım geliştirme ekibi kur başka bir konu ama marketing ekibi kur
> başka bir konu. Bizim üretici kadromuz bu ikisini de yapamazsa sorun doğar."*

> *"Mesela game development agent takımı kurmak istiyorum. Ya da N8n yönetim ekibi. Ya
> da bir haber portalı yönetim agent takımı — bu örneği sayısız çoğaltabiliriz."*

Yani fabrika yazılıma özgü olmamalı. Bugünkü kanonu bu açıdan hiç sınanmadı.

### Üç: kestirmeden yapmama

> *"PAM'a yeni bir agent takımı kurmak istiyoruz dediğimde ne yapacak, nasıl davranacak,
> hedefi ne — tamamen öğrenir ve **bunu kestirmeden yapmaz.** Bunun için çalıştığı
> reponun en büyük hakimi olmalıdır."*

> *"Bu gereksinimi belirlemek için ön hazırlık — bu çok uzun sürebilir, belki günler alır
> ama detaylandır."*

Yavaşlık burada bir kusur değil şart. Fabrikanın *"hız doğru çözüm değildir"* kuralı
buradan geliyor.

### Dört: bakım kabiliyeti

> *"Sahada 8 takım kurduk diyelim, 6 ay sonra behavior neredeyse hepsinde benzer ama bir
> şey değiştirmek istiyorum — tüm takımlarda bu düzenleme yapılmalı kararı alabiliyor
> muyuz? Yani genel agent takımlarımızın bakımından, yeni özelliklerden kim sorumlu?"*

Bu v7'nin ölçülmüş arızasının doğrudan karşılığı: *"bir kural değişimi günlerimi
alıyordu, mutlaka çelişkiler kalıyordu."*

## Rollerin ayrılma gerekçesi — Mert'in kendi cümleleri

**PAM ile PAD neden ayrı:**

> *"Lider sadece plan ve analiz yapmalı. İşi yazan, nereye yazacağını netleyen kişi
> uygulamacı olmalı. Takım liderinin netliği görevi tam anlamak olmalı."*

Ayrımın gerekçesi iş bölümü değil: **belirsiz talebi net gereksinime çevirmek kendi
başına bir iş.**

**PQA neden ayrı göz:** OY'deki QA akışına dayandırıldı —
> *"QA reddeder, developer düzeltir, onayda PA'ya bilgi gider. Burada da böyle olmalı.
> Sürekli 2 yere handoff taşınmaz."*

Push sahipliği: *"push işini QA yapmalı her zaman. Kendi body'sini kimse düzeltemez;
sorun PAM'a iletilir, PAM PAD'e, PQA inceler ve push'lar."*

**PCA neden var:** iki iş için — dış dünya araştırması (*"game developer ne bilmeli? İş
ilanlarına bile bakabilir, CV'ler inceleyebilir"*) ve etki analizi (*"6 takımda da bu
senaryo var der"*).

**Ve dörtlü sayısı bile sorgulanmak üzere verildi:**
> *"Bana kalırsa PA gibi, FSD, QA ve CA gibi bir dörtlüye ihtiyacımız var **ama asla
> doğru kabul etme.**"*

> *"Belki 2 agent üretip skill/command ile yönetimi daha doğru bulacağız. Amacımız tek
> doğruyu kabul edip işimize uydurmak değil."*

## Reddedilenler — kanona geçmeyen gerekçeler

Bunlar fabrikanın **ne olmadığını** tanımlıyor ve hiçbiri kanonda gerekçesiyle durmuyor.

**Orkestratör modeli reddedildi.** Claude *"sadece lider konuşsun, diğerleri arkasında
subagent olsun"* önerdi:
> *"Ben hepsiyle muhattap olmayı seviyorum. Handoff'u taşıma işi beni kontrollü tutuyor.
> Kime ne iş verildiğini görüyorum, bu sayede hatayı yakalayıp müdahale edebiliyorum."*

**Ortak çekirdek behavior plugin'i reddedildi.**
> *"Bence hiçbiri ortak olamaz. Çünkü fabrika behavior'a bak, web'e bak, OY'ye bak — her
> şeyi farklı bunların. İsimlendirmeleri bile farklı olmalı ki çakışmasınlar."*

**Toptan taşıma reddedildi.**
> *"Bence hiçbir şeyi direkt taşımayalım. Yavaş yavaş taşıyalım, ürete ürete gidelim."*
> *"Örnekleri inceleyelim, esinlenelim ama bire bir asla taşımayalım."*

**İlk `CLAUDE.md` üç kez reddedildi** ve gerekçesi bir kural üretti:
> *"Mesela 4 agent'i söylemesine gerek yok. İlerde 5 olursa ne olacak? CLAUDE.md üst
> bakıştır."*

**Okunmaz rapor reddedildi — üç kez.**
> *"Ürettiğin raporların hiçbiri insan okumasına uygun değil."*
> *"Bak yine kocaman bir duvar. 5 soru sordun, açıklamalar yazdın, hepsi yukarıda koca
> bir blok — hangisini okuyup yanıt vereyim, 10 dk sürer."*
> *"12 soru var ama hiçbirini anlamadım; dokümanı okumak zorunda değilim ki?"*

Bu üç kez tekrarlanan tek şikâyet. **Fabrikanın ölçütlerinden biri olmalı:** ürettiği
agent'ın çıktısı insan okunabilir mi.

## Fabrika bitmedi — beklemeye alındı

Kronoloji bunu net gösteriyor. 2026-08-02 23:35'te ilk fabrika commit'i düştü. Aynı
gece preload arızası bulundu ve 23:50'de:

> *"AG'ye yeni bir sürüm çıkartmasını söyledim. PAM ekosistemi şimdilik beklesin,
> fabrika yapısı vs hepsi beklesin."*

O günden beri fabrika üzerinde yapılan iş yalnız **kendi ayarları** oldu
(`docs/fabrika/` altında beş klasör: açılış hooku, atıf haritası, ekip kurulumu, hook
sonrası temizlik, tek muhatap).

Yani *"fabrika ne kadar iyi"* sorusunun cevabı: **bilinmiyor, çünkü hiç sınanmadı.**
Sınanmaya başladığı gece daha büyük bir arıza çıktı.

Ve `team/` klasörü boş — `dagitim` skill'i (20 kural) hiçbir gerçek paket üzerinde
denenmedi.

## Mert'in kendi teşhisi — sorun nerede

> *"Sorun fabrika mimarisinde bence. Agent body'de ne olmalı, hook nasıl kurulmalı,
> agent skill'i hangi aşamada okur nasıl tetiklenir... kesinleştiremediğimiz için
> ürettiğimiz dokümanlar teoride harika ama içerikleri doğru yönlendirmeyi taşımıyor.
> Sayısal ölçümler doğru ama pratik problemli ve **PAM sürekli sayı ölçüyor, kural
> ölçüyor, içerik akış progress'i doğru yorumlamıyor.**"*

> *"Docs folder'ı içinde o kadar fazla ölçüm yaptım ki. Binlerce analiz yaptım, binlerce
> gereksinim belirledim ama **yöntemi kuramadım.**"*

Bu ikinci alıntı önceki kuşağın teşhisiyle birebir aynı
(`kararlar/2026-08-02-clara-kurulumu.md` → *"Clara hep tasarladı, hiç iş yapmadı"*).
Yani örüntü kişide değil düzende: **ölçüm bol, kapanış yok.**

## Clara da sınanmak üzere kuruldu — ve sınanmadı

Aynı oturumda bu oda açıldı. Mert'in cümlesi:

> *"İşte o yüzden Clara'ya verelim bu işi dedim. Clara ilk saha deneyimini yaşasın.
> **Sonra onu ölçelim, bakalım gerçekten iyi mi, işi doğru yönetti mi?**"*

Bu ölçüm yapılmadı. `incelemeler/clara-ilk-sinama/kayit.md` kanonun **kurulum**
sınamasıdır (dört baskı testi, agent kullanılmadan önce); saha performansı ölçümü
değil.

## Sıradaki adım — karar bekliyor

Ölçüt artık var (yukarıdaki dört şart). Fabrikayı bu ölçütle okumak mümkün.

Ama asıl soru Mert'te ve bu turda soruldu, cevap alınmadı: **fabrika bugünkü hâlinden
devam mı edecek, yoksa preload dersiyle baştan mı kurulacak?**

İkisi farklı iş. Devam etmek fabrikayı ölçütle denetleyip eksik kapatmak; baştan kurmak
ise fabrikanın kendi kanonunu yeniden yazmak — ve o iş fabrikanın kendi eliyle
yapılamaz (`BHV-NO-SELF-CONFIG`).
