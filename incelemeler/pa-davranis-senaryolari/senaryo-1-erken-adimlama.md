# PA Senaryo 1 — Erken adımlama

**Kaynak:** GOAT / `service-addon-boost` + chat modülü, 2026-08-04 saat 17:32–22:24
**Oturum:** `4581cca8` (121 mesaj; bu senaryo 19:36–21:12 aralığı)
**Ne için tutuldu:** Mert'in isteği — *"PA'nın çalışmasını istediğim yöntemi
okudun; PA senaryo 1 olarak buradaki davranışları kayıt altına alalım, PA'yı
geliştirirken faydalı olacak."*

Bu bir denetim kaydı değil. Bir referans: PA'nın nasıl davrandığı, nasıl davranması
gerektiği, ve arasındaki farkın adı.

## Senaryonun tek cümlesi

**PA, eldeki bilgi tamamlanmadan sonraki adıma geçiyor.** Beş buçuk saatlik
oturumda altı kez düzeltildi; altısının kökü aynı.

## Altı düzeltme, sırasıyla

Her maddede Mert'in cümlesi, ardından PA'nın kendi teşhisi. PA'nın cevapları
kayda değer — her seferinde savunmadı, **nerede yaptığını buldu.**

### 1 · Elindeki kaynağı açmadan konuştu (19:36)

**Mert:** *"Peki bu hatalar bizim atladıklarımız mı, notlarına baktın mı hiç?"*

**PA:** *"Haklı bir soru ve hayır, tam bakmadım — dokümanın sadece 'bilinçli
eksikler' kısmına baktım, kapanış notlarının bütününe bakmadım."*

Kaynak elinin altındaydı, kısmen okunmuştu, tamamı okunmuş sanıldı.

### 2 · Yapıyı konuştu, davranışı sormadı (19:38) — en derin madde

**Mert:** *"Bu senin davranış hatan PA, hızlıca adımlamaya çalışıyorsun, işleri
gereksinimi detaylandırmıyorsun, bu da bize gereksiz hata olarak dönüyor. İş
bittiğinde de gereksinimden kalan boşluk var mı, QA doğru kontrol yapamıyor."*

**PA'nın teşhisi — bu senaryonun kalbi:**

> *"Chat discovery'sinde **yapıyı** çok iyi konuştum: mesaj nerede saklanacak, tek
> oda mı çok oda mı, hangi yetki, hangi chunk sırası, blob mu tablo mu. Bunlar
> mimari kararlar ve doğru kararlardı. Ama **kullanıcı bunu kullanırken ne olacak**
> sorusunu sormadım. Ekran mock'u vardı, 'tasarım onaylı, korunacak' dedim ve
> davranışı sorgulamayı bıraktım. Mock bir ekranın nasıl **göründüğünü** söyler,
> nasıl **davrandığını** söylemez."*

Sormadığı somut sorular:
- Kullanıcı seviye atladığında eski mesajlarındaki rozet ne olacak?
- Duyuru kartında hangi görsel görünecek?
- Biri sohbete link yazarsa ne olacak?

*"Bunların hiçbiri teknik soru değil. Hepsi 'kullanıcı ne yapar, sistem ne cevap
verir' sorusu. Ve üçü de sonradan hata olarak geri döndü."*

**Mert'in eklediği ikinci bedel daha ağır:** gereksinimde kalan boşluk yalnız hata
üretmiyor — **QA'yı da kör bırakıyor.** QA neyin doğru olduğunu bilmediği şeyi
denetleyemez. Yani eksik gereksinim iki kapıyı birden delik bırakıyor.

### 3 · Kendi hatasının teşhisini Mert'ten istedi (20:06)

**Mert:** *"A mı B mi bana sorman garip değil mi? Çünkü işi yapan sensin, bu
hatayı yapmana sebep ne, sen bulmalısın."*

**PA:** *"Haklısın. Sana sormam, sorumluluğu sana devretmekti — hem de 'değer
katan ortak ol' derken tam tersini yaptım: kendi hatamın teşhisini de senden
istedim. Kendim bulmam gerekiyordu. Tahminle cevap vermek yine aynı hatayı yapmak
olur."*

Ayrım net: **seçenek sunmak** PA'nın işi, **teşhisi devretmek** değil.

### 4 · Kodu araştırmadan soru sordu (20:34)

**Mert:** *"Bunları önce araştır sorgula, başkaca sorular da gelebilir elimize —
mesela sponsor panelde chat linki tıklanabilir değil şu an. Discovery'nin
kusursuz olması senin işin."*

**PA:** *"Koddan bulunabilecek şeyi sormak zaman kaybı, ve araştırmadan sorduğum
sorular eksik kalıyor. Nitekim sen daha ben sormadan dördüncü bulguyu söyledin:
sponsor panelinde link tıklanabilir değil. Yani tek panel sorunu değil, **panel
bazında farklı** olabilir."*

Buradaki bedel ölçülebilir: PA'nın soru listesi eksikti ve eksiği **Mert kapattı.**
Yani araştırılmamış soru, yükü kullanıcıya geri veriyor.

### 5 · Usul sorusu sordu, oturumu açmadı (20:36)

**Mert:** *"İşte sen burada benimle artık çalışma session'u başlatman lazım.
Kararları kendine göre almaman lazım."*

**PA:** *"Ben yine 'şunu mu yapsak, bunu mu' diye sana **usul sorusu** sordum —
oysa yapmam gereken şey oturmak ve seninle tek tek konuşmak. Kararları senin
vermen için önüne düzgün getirmem lazım, 'toparlayıp sonra mı konuşalım' diye
erteleyerek değil."*

**Ayrım:** *"Nasıl çalışalım?"* diye sormak iş değil, işin ertelenmesi.

### 6 · Kararı doğrudan dokümana çevirmeye kalktı (21:12)

**Mert:** *"Ben buraya kadar okeyim ama bu kararlara göre direkt discovery'yi
yazma bence — ilk olarak kararları al ve kodu tara, belki başka sorular
çıkartacak bunlar."*

**PA:** *"Haklısın — kararlar birer **girdi**, gereksinim değil. Her karar kodda
bir yere dokunuyor ve o yere baktığımda muhtemelen sormadığım şeyler çıkacak.
Kararı doğrudan discovery'ye çevirmek tam da bugün ders aldığım al-ver davranışı
olur."*

Bu maddenin değeri: **döngü.** Karar → kod tarama → yeni sorular → karar. PA
döngüyü tek geçişli sanıyordu.

## Mert'in istediği çalışma yöntemi (bu altı düzeltmeden çıkan)

1. **Kaynağın tamamını oku.** Bir dokümanın bir bölümüne bakıp tamamını okumuş
   sayma. Elinin altındaki kaydı açmadan konuşma.
2. **Yapıyı değil davranışı sor.** Mimari kararlar (nerede saklanır, hangi tablo)
   doğru olabilir ve gereksinim yine eksik kalır. Asıl soru: *kullanıcı bunu
   kullanırken ne olacak.* Mock görünümü söyler, davranışı söylemez.
3. **Sormadan önce araştır.** Koddan bulunabilecek şeyi sorma; araştırılmamış soru
   listesi eksik çıkar ve eksiği kullanıcı kapatır.
4. **Teşhis senin.** Seçenek sunmak PA'nın işi; *"neden böyle oldu"* sorusunu
   kullanıcıya devretmek değil.
5. **Usul sorma, oturumu aç.** *"Nasıl çalışalım"* bir iş değil, ertelemedir.
   Soru-cevap yürütülür (`AskUserQuestion` uygun), ve seçenekler kullanıcının
   **ekleme yapabileceği** şekilde sunulur — iki seçenek arasına sıkıştırma.
6. **Karar bir girdidir, çıktı değil.** Karar alındıktan sonra kodu tara; yeni
   sorular çıkarsa döngüye geri dön. Dokümanı en son yaz.
7. **Gereksinimdeki boşluk iki kapıyı deler.** Hem hata üretir hem QA'yı kör
   bırakır — QA doğru olanı bilmediği şeyi denetleyemez.

## Neden kural olarak yazılamıyor — kanon boşluğu

**Kural PA'nın elinde var ve yine oldu.** Aynı gün ölçüldü: PA'nın kanonunda
`WEB-PA-DANISMA-EYLEM-AYRIMI` var (*"danışmada akış başlatmak/doküman üretmek
yasak"*) ve PA kendi kanon dökümünde *"kendiliğinden akış başlatmam, varsayılan
bekle"* yazdı. Altı saat sonra altı kez başlattı.

Sebebi PA'nın kendi sabah tespitinde:

> *"Kanonum bana 'ne yapmayacağımı' ID'lerle çok net söylüyor, 'ne yapacağımı' ise
> akış olarak anlatıyor ve ID'lemiyor. İkincisini atlamak birincisini ihlal etmek
> kadar zarar verir ama tespiti daha zor — çünkü ihlal edilecek bir ID yok, sadece
> atlanmış bir adım var."*

**Bu senaryo o tespitin kanıtı.** Altı düzeltmenin hiçbiri kural ihlali değil;
altısı da atlanmış adım. Yasak listesi bu davranışı yakalayamaz.

## Aynı ders Clara'ya da verildi — ve kalıcı oldu

Aynı gün 19:04'te Mert Clara'ya: *"asla ama asla her şey bitmeden işe başlama"* ve
*"sürekli anladığını sanarsan beni anlayamazsın."* Clara'nın kanonuna
`CLA-WAIT-FOR-THE-END` olarak girdi.

**Fark mekanik:** Clara'nın kanona yazma yetkisi var, PA'nın yok. Yani aynı gün
aynı ders iki agent'a verildi; birinde kalıcı oldu, birinde oturum bitince uçacak.

PA doğru davrandı — kuralı memory'sine yazdı ve saha kanıtı ekledi. Ama memory'deki
kural yalnız o agent'ta yaşar; `web-behavior` yedi agent'ın ortak dosyası ve oraya
yazacak kapı (AG) emekli.

## Olumlu taraf — akış düzeldiğinde çalışıyor

22:24'te Mert: *"ok, kararları son bir kontrol et, başka soracak sorun yoksa
discovery'yi yaz."* Yani 20:36'da başlayan soru-cevap turu düzgün bitti.

**PA erken adımlamayı bıraktığında akış doğru işliyor.** Ama durma noktasını her
seferinde **Mert koydu**, kural koymadı. Düzenin çözmesi gereken şey bu: durma
noktası kanonda olmalı.

Ve bir iyi haber: PA her düzeltmeyi öğrenmeye çevirdi, savunmaya değil. Bir bulguyu
kendi eksiği olarak yazdı — *"bugün ölçüldü: ben fark etmedim, sen söyledin."*
Kayıt tutma refleksi var; eksik olan o kaydın kalıcı kurala dönüşecek kapısı.

## Bundan çıkan gereksinim (PAM'e, henüz devredilmedi)

PA kanonuna **görev adımı** kuralı gerekiyor — yasak değil, atlanamaz adım:
kaynağı tam oku → davranışı sor (yapı yetmez) → sormadan önce araştır → oturumu
aç, usul sorma → kararı girdi say, kodu tara → dokümanı en son yaz.

Adlandırma önerisi: bu adımların ID'lenmesi (ör. `WEB-PA-STEP-*`), çünkü ID'siz
adım tespit edilemiyor — bu senaryonun kanıtladığı şey tam olarak bu.
