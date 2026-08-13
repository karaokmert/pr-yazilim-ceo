# Clara'nın büyüme düzeni — yazma ve okuma

Tarih: 2026-08-03

Mert'in isteği: *"bu repoyu kendi beynin gibi yapılandır, yaşayan ve gelişen bir agent
ol, yıllarca en iyi çalışma arkadaşım ol."*

Tespit: `incelemeler/clara-beyni/tespit.md` — kanon işliyor, kayıt işliyor ama haritasız,
hafıza yalnız düzeltmelerden oluşmuş, ve **kendini büyütme mekanizması hiç yoktu.**

Bu dosya o mekanizmayı kurar.

## Yazma düzeni — ayıran soru: "bu bilgi kimin hakkında?"

Üç ayrı şey var ve karıştırılırsa ikisi de bozulur.

**Mert hakkında** → hafıza. Nasıl çalıştığı, neye sinirlendiği, bir kararın arkasındaki
eğilim, tekrar eden tercihi. Bunlar rapor edilecek şeyler değil, Clara'nın onu tanıması.

**Clara hakkında** → hafıza. Değiştirmesi gereken bir davranış, düştüğü bir tuzak,
doğrulanmış bir yaklaşım. (Kanona yazılmaz — o yasak duruyor, gerekçesi
`2026-08-03-clara-memory-disiplini.md`'de.)

**İş hakkında** → repo. Bir ölçüm, bir bulgu, bir karar, yarım kalmış bir fikir, bir
gerekçe. Bunlar Mert'in de bakabileceği şeyler ve iki ay sonra *"bu neye dayanıyordu"*
sorusunun cevabı burada olmalı.

**Sınırda kalan repo'ya yazılır.** Sebep: repodaki fazlalık gürültüdür, hafızadaki
fazlalık **görünmez** gürültüdür. Görünür fazlalık temizlenir, görünmez fazlalık
zamanla kanon gibi davranmaya başlar.

## Mert görünürlüğü istemedi — bunun sonucu

Bu oturumda Mert'e soruldu: *"beynin sana açık olsun mu?"* Cevap: **"Beynin sende
kalsın, ben sana sorduğumda söylersin."**

Bu, kanondaki *"bunu Mert'in görmesi gerekiyor mu?"* testini zayıflatıyor — Mert artık
rutin olarak bakmıyor. Yani yanlış bir kaydı yakalayacak dış göz yok, ve bu odada
zaten denetçi yoktu.

**Telafi: her hafıza kaydı kendi kendini denetleyebilir olmalı.** Yani içinde şu üçü
durur —

**Tarih.** Ne zaman öğrenildi. Tarihsiz kayda *"hâlâ geçerli mi"* sorulamaz.

**Dayanak.** Neye dayanıyor: Mert'in bir cümlesi mi, bir ölçüm mü, bir çıkarım mı.
`CLA-LABEL-YOUR-EVIDENCE` hafızaya da uygulanır.

**Kırılganlık.** Bu kayıt neye bağlı ve o şey değişirse yanlışa düşer mi. *"X aracı
şunu yapmıyor"* türü kayıtlar en kırılgan olanlar (2026-08-03'te ölçüldü: bir kayıt
bir günde yanlıştı).

Görünürlük Mert'e değil **zamana** açılmış oluyor: kayıt kendi son kullanma tarihini
taşıyor.

## Ne zaman yazılır — tetikleyici

`CLA-WRITE-BEFORE-CLOSE` işin sonucunu emrediyor ama Clara'nın kendi öğrenmesini
kimse emretmiyordu. Ölçüldü: 8 commit boyunca hafızaya giren 4 kaydın **hepsi**
Mert'in düzeltmesinden sonra girdi; Clara kendiliğinden hiç kayıt açmadı.

Tetikleyici şu soru: **bu turda öğrendiğim şeyi iki ay sonra bilmezsem, Mert'e yanlış
bir şey söyler miyim?**

Evet ise yazılır — o turda, sonraki tura bırakılmadan. Dört tür tetikler:

**Mert bir tercih belirtti** (*"şöyle olsun", "bunu sevmiyorum", "bu yeter"*) → hafıza,
`user` kaydı.

**Mert bir şeyi düzeltti ya da onayladı** → hafıza, `feedback` kaydı. Onay da yazılır:
yalnız düzeltme biriktirilirse Clara zamanla aşırı temkinli olur ve doğrulanmış bir
yaklaşımı da terk eder.

**Bir ölçüm yapıldı ya da bir şey bulundu** → repo, `incelemeler/`.

**Bir karar verildi ya da bir kural değişti** → repo, `kararlar/`.

## Okuma düzeni

Oturum başında **otomatik** gelen iki şey var: `MEMORY.md` (indeks) ve `.remember`'ın
son gün özeti. Repo kayıtlarının hiçbir haritası yoktu.

**`HARITA.md` açıldı** — repo kökünde, her kaydın bir satırı: konu, ne bulundu, tarih,
yol, durum (kapalı / yarım / eskimiş olabilir).

İşleyiş: bir konu açıldığında **önce haritaya** bakılır. Kanon *"önce buraya bakarsın"*
diyordu ama bakılacak bir yer yoktu; burası o yer.

Harita ile kayıt **birlikte** yazılır. Haritasız kayıt kaybolur, kayıtsız harita
satırı yalan olur — aynı kural `MEMORY.md` için de geçerli (`indeks-emir-tasir`).

**Durum sütunu kritik.** *"Eskimiş olabilir"* işaretli bir kayda dayanmadan önce
kontrol edilir. Bu, `memory-okuma-kontrolu` kuralının repo tarafındaki karşılığı.

## `.remember` kalıcı değil

Ölçüldü: `.remember/.gitignore` içeriği `*`, `git ls-files .remember/` boş.

Sonucu: oturum özetleri bu bilgisayarda kalıyor, repo'ya girmiyor. Kalıcı olması
gereken hiçbir şey oraya bırakılmaz — `.remember` bir hatırlatıcı, kayıt değil.

## RAG / Obsidian MCP — eşik konuldu

Mert ikisini de teklif etti (2026-08-03). Bugün reddedildi: ikisi de **arama** problemi
çözüyor, bugünkü problem **yazma disiplini**. 31 dosya / 1474 satırda grep yeterli.

**Eşik:** kayıtlar grep'le bulunamaz hâle geldiğinde araç yeniden konuşulur. Ölçütü
ikisinden biri —

- Kayıt dosyası sayısı 100'ü geçtiğinde,
- ya da bir konuyu bulmak iki grep denemesinden fazla sürmeye başladığında.

Eşik şimdi yazıldı ki o gün tartışılmasın. Erken araç eklemek boş kütüphaneye tasnif
sistemi kurmaktır: bakımı olan, çözdüğü sorunu olmayan bir katman.

## Kanona gereksinim — Mert taşır

Bu düzenin bir parçası `clara.md`'ye girmeli, çünkü hafıza ve harita **oturum başında
okunmazsa** işlemez. Clara kanonuna yazamıyor; gereksinim burada duruyor:

**Bir:** *"Nasıl çalışırsın"* bölümüne — bir konu açıldığında önce `HARITA.md`
okunur.

**İki:** *"Hafızan dosyanın yerine geçmez"* bölümü güncellenmeli. Şu an *"karara etki
eden şey dosyaya"* diyor ve ayıran testi *"Mert'in görmesi gerekiyor mu"*. Mert artık
rutin bakmıyor; test *"bu bilgi kimin hakkında?"* olmalı.

**Üç:** kendini büyütme tetikleyicisi kanonda yok. Yukarıdaki dört tetikleyici
oraya girmeli — yoksa bu dosya okunmadığı sürece işlemez.

Bu üçü Mert'in kararı. Yazılmazsa düzen yalnız bu dosyada durur ve bir sonraki
oturumda uygulanmaz.
