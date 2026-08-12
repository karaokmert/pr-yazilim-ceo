# ClickUp task takip düzeni — canlı test (2026-08-12)

> **Tetik:** Mert — *"Projelerde akışlar birbirine girdi, kimin hangi işi bitirdiği belli
> olmadan diğer işe gidildi, her task yarım kaldı."*
> **Ölçüm ortamı:** ClickUp "Task Denemesi" listesi (901525085863) + `~/p/temp/test-repo`
> + altı OY agent'ı (PA, UID, BE, FE, QA, CA) canlı kanalda.

## Teşhis — arıza takip aracının yokluğu değildi

ClickUp zaten vardı ve yine karıştı. Sebep: **ClickUp'a yalnız PA yazıyordu**
(`CLICKUP-PA-ONLY-WRITE`), gerçek iş agent'ta ilerliyordu, araya Clara giriyordu.
Üç katman, tek gerçek — ve kayıt gerçeğin bir tur gerisinde kalıyordu.

Asıl kırılma: **"bitti" bir beyandır, kayıt değildir.** Beyan üstüne akış ilerliyor,
sonra denetim "eksik" diyor ve iş geri geliyor — ama o arada agent başka işe başlamış
oluyor. İki iş de yarım.

## Kurulan düzen

**Üç fiil, çakışma yok:** PA açar · agent yürütür · Clara okur.

Ana task altında **beş sub task** (üç değil):

    PRC-26  Randevu Takvimi              [in progress]
      └ PA   Discovery                    ← PA'nın kendi işi de görünür
      └ UID  Mock
      └ BE   Contract
      └ FE   Ekran
      └ PA   Kapanış                      ← baştan Open durur

**Sıra:** PA işi alır → ana task `in progress` + kendi discovery sub task'ı `in progress`
→ discovery biter → discovery `completed` + **aynı anda** katman sub task'ları (sahipsiz)
+ kapanış sub task'ı açılır → katmanlar yürür → hepsi biterse PA kapanışı `in progress`
alır, konsolide eder, ana task `live - dev` + kapanış notu.

**Statü akışı:** `Open → in progress → test` (QA'ya devrederken, agent çeker)
→ QA onayı → `completed` (yine agent çeker). RED gelirse `revise`.

**Kapatma yetkisi QA'da, kaydın eli sahibinde.** QA statüye dokunmaz, onay verir.

**Kanıt zorunlu:** kod → commit hash (`local, push bekliyor` diye işaretli) · denetim →
QA onayı · CA → rapor yolu + ölçüm sayısı · canlı → push hash.

**Süre:** `completed` sonrası agent kendi `in progress` süresini ClickUp'tan çekip
`add_time_entry` ile tracked'e yazar. **Timer kullanılmaz** — ölçüldü: ClickUp'ta aynı
anda tek timer çalışıyor ve timer kullanıcıya bağlı, task'a değil; paralel agent'larda
ikincisi hata alıyor. `time_estimate` de kullanılmaz (o "tahmin" demek).

## Fabrikaya gidecek üç bulgu — kanonda karşılığı YOK

**1. Paylaşılan çalışma ağacında stage disiplini.**
Kanonda *"developer yalnız KOD commit'ler, push YOK"* var; *"yalnız KENDİ yolunu
stage'lersin"* yok. Tek repoda birden çok agent çalışırken `git add .` çeken taraf
diğerinin yarım dosyalarını kendi commit'ine katıyor — ve o an "kimin ne yaptığı"
kayboluyor, yani çözmeye çalışılan şeyin tam tersi.
Kural: `git add .` yasak · herkes kendi yolunu stage'ler · commit öncesi `git status`,
sonrası `git show --stat`.
*PA yakaladı (`git add docs` ile sınırlamıştı), sonra UID ve BE'ye de uygulandı.*

**2. Risk cevabı bir KURAL üretiyorsa, o kuralın EKRAN KARŞILIĞI ayrı bir maddedir.**
*"Geçmişe müsaitlik tanımlanamıyor"* bir kural; *"o slot ekranda nasıl görünür"* onun
ekran karşılığı. İkisi aynı şey değil.
PA discovery'de kuralı yazdı, ekran diline çevirmeyi atladı; kabul kriteri iki durum
(dolu/boş) derken kurallar **üçüncü** durumu (kapalı) zorunlu kılıyordu. UID mock
üretirken yakaladı. UID'siz bir işte yakalanmazdı — kural discovery'nin kendisine
yazılırsa her işte yakalanır.
*PA'nın öz eleştirisi: "kuralı ben yazdım, ekran diline çevirmeyi atladım."
Clara'nın düzeltmesi: kabul kriterini Clara yazmıştı, hata zincirde.*

**3. Yazma çağrısının DÖNÜŞÜ bir ölçüm değildir — sonucu okuyarak doğrula.**
İki vaka, aynı kök: sub task açıldığında dönen yanıtta `description` boş göründü
(doluydu), başka bir açılışta `custom_id` null geldi (atanmıştı). Özet/create yanıtları
eksik alan döndürebiliyor.
*PA iki kez de düzeltmeye koşmadan önce okuyup ölçtü, ikisi de yanlış alarmdı.
Düzeltseydi var olan açıklamaların üstüne yazacaktı.*

## Ölçüm disiplini — sahada doğrulanan iki ders

**"X kez görünüyor" eksik cümledir — birimi yaz.** UID *"istisna gün etiketi 44 kez"*
dedi, QA **21** saydı ve farkı kovaladı; fark bir bulgu ortaya çıkardı. UID sonra çözdü:
44 = 21 slot × 2 + legend + menü (her slot snapshot'ta iki kez geçiyor). *"Sayı doğruydu,
iddia yanlıştı — çünkü birimi yoktu."*

**Ölçüm aracını doğrulamadan sonucuna güvenme.** UID aynı turda "Kayıt tamponu 0" saydı,
paniğe kapılmadı, veriye baktı — veride 3 vardı, hata kendi regex'indeydi (etiket parantez
içeriyordu). Düzeltmeye koşmadan aracı doğruladı.

## Zincirin ölçülen davranışı

- **Agent kendi statüsünü çevirebiliyor** — en kritik teknik doğrulama. PA'nın çevirmesi
  biliniyordu; asıl soru agent'tı, çünkü düzenin tamamı buna dayanıyor. UID `in progress`
  çekti, çalıştı.
- **İzin katmanı tek kapıymış** — `create_task` ve `update_task` ayrı denendi, ikisi de
  aynı izinle açıldı. Önce ikisi de blokluydu (*"Blocked by classifier"*), Mert
  `settings.json`'a ekledi.
- **QA kapısı işini yaptı:** iki tur RED. Birinci turda mock veri boşluğu + rol kısıtının
  tek ekranda kalması; ikinci turda çelişkinin **yer değiştirdiği** (aynı kopukluk, ters
  yönden — iki veri kümesi bir gün kayık). Denetim olmasa demo kabul edilirdi.
- **UID kök çözüm seçti, yama değil:** rolü her ekrana ayrı `useState` ile koymak yerine
  tek kaynağa (Context) taşıdı. Gerekçesi: *"aynı kısıt üç yerde ayrı yaşarsa biri
  unutulunca sessizce açık kalır — bulgunun kendisi zaten tam olarak o."*
- **BE gerçek bir çelişki buldu:** repoda .NET yok, PR Yazılım backend'i .NET. Ölçerek
  geldi (SDK 10.0.202 kurulu, NuGet feed erişilebilir, `cache 0.2.0`'da distributed lock
  API'si var). Ve kendi kanıt sınırını kendi kurdu: *"MSSQL/Redis/K8s yok — kod DERLENİR,
  KOŞMAZ. 'Çalışıyor' diyemem, 'derleniyor' diyebilirim."*

## Bilinçli test sapması

Kanonda ClickUp'a yalnız PA yazar (`CLICKUP-PA-ONLY-WRITE`, `CLICKUP-ROLE-STATUS`).
Mert bu testte kuralı **askıya aldı** — agent'lar kendi statülerini kendi çeviriyor.
CA çelişkiyi kanondan **önceden** buldu ve bildirdi, PA da sapmayı kayda geçirerek
uyguladı. İkisi de doğru davrandı; sessizce uygulasalardı test yanlış okunurdu.
Kalıcı olup olmayacağı testin çıktısına göre ayrıca karara bağlanacak.

## Test kurgusunun sınırları

- **PRAG kurgusal bir projedir**, kodda karşılığı yok. Discovery'nin *"mevcut durumu
  koddan oku"* adımı yapılamadı; emsal analojisiyle (osinif, yazarlık doğrulandı: insan
  developer) kuruldu.
- `PRC-37` (PA discovery) **geriye dönük** `completed` açıldı — sahada bu sub task ilk
  açılacak ve `in progress` başlayacak. Testte görülen sıra sahadaki sıra değildir.
- Test listesi ve repo, test bitince silinecek (Mert'in kararı).

---

## Fabrikaya giden / gidecek

**1. CLICKUP-PA-ONLY-WRITE kural değişimi — devir bloğu YAZILDI, Mert taşıyacak.**
Blok 15:42'de ekrana basıldı: kurulan iş akışının tamamı + çakışma + kuralın üç
gerekçesinden birinin çürüdüğü ölçüm + iki yol (a: kural gevşer, b: kural kalır,
ev tarafı düzeltilir). Karar fabrikanın, gerekçesiyle dönecek.

**2. Paylaşılan çalışma ağacında stage disiplini — BLOK HENÜZ YAZILMADI.**
Mert: *"bunu bi yazalım sonra"* (15:44). Bulgu §"Fabrikaya gidecek üç bulgu"
altında duruyor: kanonda *"developer yalnız KOD commit'ler"* var, *"yalnız KENDİ
yolunu stage'ler"* yok. Bugün üç agent'ta (PA, UID, BE) uygulandı ve tuttu.

**3. Risk cevabı → ekran karşılığı ayrımı — BLOK HENÜZ YAZILMADI.**
Discovery kanonuna girecek. PA'nın öz eleştirisinden doğdu.

**4. Yazma çağrısının dönüşü ölçüm değildir — BLOK HENÜZ YAZILMADI.**
İki yanlış alarm vakası; `clickup-duzeni` ve OY clickup skill'ini ilgilendirir.
