# Mert'e sorulacaklar — 2026-08-07 gece

Mert 22:00'de iki saatliğine ayrıldı. Yönetim Clara'da. Kararı Mert'te olan
kalemler burada birikiyor; **iş durmuyor**, karar gerektiren yerde Clara en
savunulabilir yolu seçip **gerekçesini yazıyor.**

---

## 1 · PUSH ONAYI — en öncelikli

**On iki commit, yedi ayrı iş.** Brief hazır: `gunluk/2026-08-07-push-brief.md`

PQA'nın şartı: onay **yazılı** olmalı ve **kapsamı** da yazılı olmalı — *"kapsamı
yazılmamış onay eksik onaydır, varsayımla tamamlanmaz."*

Sayı gece boyunca artacak; sunumdan hemen önce yeniden ölçülecek.

---

## 2 · `ISD-CASCADE-IN-ONE-TURN` kimlik değişimi — KARAR ALINDI, uygulanıyor

Mert 21:58: *"Evet değişsin, artık aynı tur imkânsız."*

Bedeli kabul edildi: kimlik değişimi bir cascade daha demek.

---

## 3 · PCA her turda çağrılmayacak — KARAR ALINDI

Mert 21:58: *"PCA total çakışmaları bütünsel tarar, her turda iş ona gitmez."*

Ve aynı gün kanıtlandı: PCA'nın **tek** taraması beş bulgu çıkardı, birincisi
dokuz denetim turunun hepsinin kaçırdığı şeydi.

**Açık kalan alt soru (Clara not ediyor, karar gerekmiyor):** bütünsel tarama
**hangi sıklıkta** koşulacak? Her iş sonrası mı, günlük mü, sprint sonu mu?
Ölçüm yok — bir kez koştu. Clara'nın önerisi: birkaç kez daha koşsun, aralık
ölçümle belirlensin.

---

## 4 · "Komşu cümle çevresi ne kadar" — SORU DÜŞTÜ

PAM sormuştu. Clara'nın değerlendirmesi: soru **anlamsız kaldı.** PCA'nın Bulgu
1'i on bir satır arayla duruyordu ve dokuz tur görmedi — yani sorun **mesafe
değil, yan yana konmamış olması.** Mesafe eşiği yanlış çözüm; doğru çözüm
bütünsel tarama, o da (3)'te karara bağlandı.

PAM'e iletildi, itiraz ederse yeniden açılır.

---

## 5 · Görev listesi kuralının iki küçük sorusu — CEVAPLANDI

Mert 21:45: *"Tek tasklık bir liste olmaz. İş tek kalem görünse de içinde adımlar
var."* → koşulsuz, istisna yok. Kurala girdi.

Ekranda görünürlük ölçümü ertelendi (19:06): *"agentlar yeniden başladığında
anlaşılır."*

---

## Yöntem — Mert'in verdiği araç (22:01)

> *"Kararsız kaldığın yerde fabrika agent'ları ile aranızda karar değerlendirmesi
> yapabilirsin. PAM'in önerisini PQA'ya sorabilirsin, ikinci göz gibi
> kullanabilirsin."*

Yani bir karar için Mert'i beklemek zorunda değilim: **PAM önerir, PQA bağımsız
değerlendirir, ben karar veririm.** Karar bende kalırsa gerekçesiyle buraya
yazılır.

Bu bugün zaten işe yaradı — PQA bağımsız baktığında üç agent'ın da göremediğini
buldu (dokuz turda dokuz bulgu). Ve PCA'nın tek bütünsel taraması beş bulgu daha
çıkardı.

**Sınır:** bu mekanizma **kapı açan** kararlar için kullanılmaz. Yayın onayı,
bir kuralın kaldırılması, kapsamın kalıcı genişletilmesi — bunlar Mert'te kalır.
Ayıran soru: *bu karar bir şeyi geri alınamaz hâle getiriyor mu?*

---

## Clara'nın gece boyunca aldığı kararlar

### K1 · İŞ-J ile İŞ-E aynı turda mı ele alınsın? (22:13)

**Durum:** İkisi de `ISD-CLOSE-THE-LOOP`'a dokunuyor ve ikisi de döngünün
şeklini değiştiriyor.
- **İŞ-J** (zıt mekanizma): *"doğrudan PQA'ya döner"* → *"yönetici üzerinden
  döner"*
- **İŞ-E** (zincir kapanışı): PQA onaylar → PAM'e bilgi → PAM commit → PQA son
  denetim

**Kararım:** PAD'e çakışmayı bildirdim ve **aynı turda ele almasını önerdim** —
ama kararı ona bıraktım.

**Gerekçe:** ayrı turlarda yapılırsa ilki, ikincinin değiştireceği cümleyi yazar.
Bugün **dört kez** yaşanan sınıf tam bu: *"bir düzeltme, dokunmadığın bir cümleyi
yanlış hâle getirebilir."*

**Karşı görüş kayıtlı:** PAM ikisini bilerek ayrı yazdı, gerekçesi vardı — *"biri
EKSİKLİK tarif ediyor, biri AKTİF ÇELİŞKİ."* İkisi farklı aciliyette.

**Neden Mert'i beklemedim:** bu bir yöntem kararı, kapı açan bir karar değil.
Ayıran soru — *geri alınamaz mı?* Hayır: yanlış çıkarsa bir sonraki denetim
turunda yakalanır.

### K3 · Üç gereksinim adayı — PAM değerlendirdi, üçü de gerçek (22:30)

PCA'nın yetenek analizinden çıkan üç aday. PAM üçünü de değerlendirdi ve **üçüne
de "gerçek gereksinim"** dedi — ama üçünü de **inceltti**:

**Aday 1 — geçici araç hatası / kalıcı izin reddi ayrımı.** PAM ekledi: bu ayrım
kanal dışında da gerekli. *"Monitor kurulumunda 'ToolSearch ikisini de
getirmiyorsa monitör kurma' kuralı tam bu sınıf — geçici araç yokluğu ile kalıcı
yetki reddi aynı sonucu veriyor ama farklı davranış gerektiriyor."*

**Aday 2 — `PQA-NO-PROPOSE-FIX` kapsamı.** PAM'in gerekçesi somut ve güçlü:
*"PQA'nın YÖNTEM teşhisleri bugün kanona ÜÇ kural olarak girdi. Eğer o teşhisler
'çözüm önerisi' sayılsaydı ÜÇÜ DE yasak olurdu ve kanon bugün üç kural eksik
kalırdı."* Kapsam cümlesi şunu ayırmalı: **dosya düzeltmesi önermek yasak, kendi
yönteminin sınırını ölçmek yasak değil.**

**Aday 3 — PAM'in "iş verme" fiili.** PAM en ağırı diyor **ve çözümü ters
kurdu:** *"Benim TASK göndermemem kuralın İŞLEDİĞİNİN kanıtı, arızası değil.
Sorun kanonun PAM'i hâlâ 'iş VERİR' diye tanımlaması. Fiil yanlış: PAM iş
TANIMLAR, yönetici İLETİR."*

Ve uyardı: *"Gereksinim 'PAM'e TASK yetkisi verilsin' değil, 'kanondaki fiil
sahayla eşitlensin' olmalı. Bu ayrım önemli çünkü birincisi kuralı geri alır."*

**Clara'nın kararı:** üçünü de gereksinim olarak açtıracağım — ama **bu gece
değil.** Elimde zaten iki iş denetimde, biri sırada. Sıra bittiğinde PAM'e
verilecek. Gerekçe: bugün on yedi commit birikti ve hiçbiri push edilmedi;
kanona daha fazla kural eklemek yerine mevcut yığının kapanmasını beklemek daha
temiz.

### K4 · `ISD-RETURN-TO-PLANNER` — ilk kullanıcı üç eksik buldu (22:30)

Kural bugün yazıldı, bugün ilk kez koştu. Clara PAM'e sordu: *"ilk kullanıcı
olarak kuralın eksik yerini görürsen yaz."* PAM üç şey buldu:

**Eksik 1 (net):** *"Kural 'PAM dökümanlarını düzeltir' diyor ama HANGİ
dökümanlar belirsiz. Bu turda üç işin dökümanı vardı ve ben beşini güncelledim —
doğru tahmin ettim ama TAHMİN ETTİM."*

**Eksik 2 (sınırda):** commit denetlenir ama **bulgu çıkarsa ne olacağı yazılı
değil.** Bu bilinerek bırakılmıştı (*"ölçülmedi"* diye hükme girdi) — ama ilk
kullanıcı olarak PAM söylüyor: *"bugün bulgu çıkmadı, çıkarsa ne yapacağımı
bilmiyorum."*

**Eksik 3 (sınırda):** *"'PAM push onayı verir' diyor. Ben NE onaylıyorum tam
belli değil — kendi commit'imi mi, tüm bekleyen commit'leri mi? Bugün ikisini
ayırarak yazdım ama o ayrımı KURAL SÖYLEMİYOR, ben ekledim."*

**Bu üçü de bir sonraki turun gereksinimi.** Kural bir günde yazıldı ve ilk
koşumunda üç eksik verdi — bu, `BHV-DATE-THE-MEASUREMENT`'in *"bir ölçüm bir
desen değildir"* cümlesinin canlı kanıtı.

### K5 · YAPISAL ÇELİŞKİ — iki kural indeksin eskimesini mümkün kılıyor (22:35)

**PQA'nın teşhisi, ve bugünkü en somut mekanizma bulgusu.**

**Ne oldu:** PAD kural indeksini iki kez düzeltmeye çalıştı, ikisinde de eksik
kaldı. Üçüncü ölçümde 86 atıf eksik çıktı.

**Sebep dikkat değil, sıra:**
```
22:29:33   PAM'in doküman commit'i (on dosya)
22:30:06   PAD'in index commit'i     (33 saniye sonra)
```
PAD'in **ölçümü** daha önce koşmuş. Yani ölçüm doğruydu — **ölçüldüğü anda.**

**Ve iki kural bunu yapısal olarak mümkün kılıyor:**
- `PAD-SYNC-INDEX` — *"index'i aynı turda güncelle"*
- `ISD-RETURN-TO-PLANNER` — *"PAM'in commit'i turun sonunda"* (bugün yazıldı)

İkisi birlikte: **index, kendisinden sonra dosya eklenen bir zincirde ölçülüyor.**

PQA'nın cümlesi: *"Senin beyanın doğruydu — 'bir sonraki sefer yakalamayabilirim'
demiştin ve bu turda gerçekleşti: yakaladın, geri aldın, yeniden koşturdun, ve
YİNE eksik kaldı."*

**Clara'nın geçici çözümü (kural değil):** bu tura özel bir sıra önerdim —
üretim → PAM'in docs commit'i beklenir → index EN SON → commit. PAD'e dayatmadım,
itiraz edebilir.

**Kalıcı çözüm sizin kararınız.** İki seçenek görünüyor ama ölçmedim:
- Sıra kanona yazılır (*"index turun son adımıdır"*)
- Ya da index iki kez ölçülür (önce ve sonra), fark varsa uyarır

### K6 · Index paralel düzende güncel kalamıyor — ve bu Clara'nın hatası (23:22)

**K5'in devamı ve daha keskin hâli.**

PAD sırayı düzeltti — Clara'nın önerisini uyguladı, PAM'in bilinen commit'ini
bekledi, index'i **en son** ölçtü. Ve **yine eksik kaldı.**

**Clara'nın bağımsız ölçümü (şema filtresiyle):** 86 eksik → **11 eksik.** Büyük
kısım kapandı. Ama kalanların **dokuzu tek bir dosyadan:**
`docs/fabrika/rol-sinir-netlestirme/gereksinim.md` — PAM'in **az önce yazdığı**
yeni iş klasörü.

**Zamanlama:**
```
22:43   Clara PAM'e yeni iş veriyor (dört gereksinim adayı)
22:44   PAD index'i ölçüyor  (PAM'in BİLİNEN commit'ini bekleyerek)
22:45   PAM yeni gereksinim yazıyor → index yine eskiyor
```

**Yani sorun sıra değil, EŞZAMANLILIK.** Üç agent paralel çalışırken index tek
bir anın fotoğrafını çekiyor ve o an geçerken eskiyor.

**Ve bu benim yönetim hatam:** PAM'e index ölçümü sürerken iş verdim. PAD sırayı
doğru kurdu, ben bozdum.

**Kararınız gereken:** index'in *"her an güncel"* olması bu paralel düzende
mümkün görünmüyor. Üç seçenek var ama hiçbirini ölçmedim:
- **Sıra kanona yazılır** ve paralel çalışma index turu boyunca durur (yavaşlar)
- **Index iki kez ölçülür** (PAD'in değerlendirmesi: *"tek ölçüm sıraya bağlı,
  çift ölçüm sırayı önemsiz kılıyor — daha sağlam ama iki kat maliyetli"*)
- **Kabul edilir:** index bir *"son ölçüm anı"* kaydıdır, canlı ayna değil — ve
  bu şemaya yazılır

PQA'ya da sordum: *"bu bir bulgu mu, yoksa kabul edilmesi gereken bir sınır mı?"*

**Bir de gerçek bir eksik var, ayrı sınıf:** `YT-AGENT-CANT-SEE-SELF` →
`.claude/hooks/acilis-preload.sh`. Bu bir `.sh` dosyası; şema *".md dosyaları"*
diyor. Yani ya atıf kapsam dışı, ya şema eksik. **Ölçmedim, işaret ediyorum.**

### K7 · KAPANIŞ KARARI — yeni bulgu turu açılmıyor (00:38)

Mert'in cümlesi: *"Clara bende işlerin bitmesi önemli, sürekli dön başa
olmasın."*

**Haklı ve ölçüldü:** bugün **on beş denetim turu** oldu ve her tur yeni bir
bulgu çıkardı. Kapanmayan bir döngü.

**Clara'nın kararı:**
- **Yeni bulgu turu açılmıyor.** PCA'ya yeni sorgulama verilmiyor, yeni eksen
  aranmıyor.
- **Kalan tek iş kapatılıyor:** PAD Bulgu 13'ü düzeltir → PQA son denetim →
  push onayı → gün kapanır.
- **Karar defteri ve PCA'nın gereksinimleri yarına kalır** — hepsi yazılı,
  kaybolmaz.

**Gerekçe ölçülmüş:** PAD *"döngü yakınsıyor"* dedi ve dört göstergeyle
destekledi; PQA bağımsız doğruladı ve bir tanesini ekledi (*"yeni bir eksen sıfır
bulgu verdi"*). Bulgular yapısal olmaktan çıkıp cilaya döndü.

**Ve PQA'nın kendi cümlesi:** *"Bu iş artık bulgu üretmiyor, TUR üretiyor. Devam
kararının maliyeti bulgu başına değil tur başına hesaplanmalı."*

### K2 · PCA'ya yetenek analizi işi verildi (22:08)

Mert'in isteğiyle. Ama kapsamı ben çizdim ve **bir şeyi bilerek yaptım:** beş
sorunun içine *"dört rol yetiyor mu"* sorusunu koydum ve **"yetiyor" cevabını da
aynı ciddiyetle ölçmesini** istedim.

**Gerekçe:** bu soru sorulunca *"hayır, beşinci gerek"* cevabı gelmesi kolaydır —
agent kendine iş yaratır. Yalın üretim kuralı: ihtiyaç doğmadan kapasite
kurulmaz. O yüzden yetmiyorsa **ölçümle** göstermesini istedim: hangi iş sahipsiz
kaldı, kaç kez, ne maliyetle.

Ayrıca beşinci soru: *"benim yönetimimde ne gördün?"* — ve *"iyi yönettin"*
cevabının işe yaramayacağını yazdım.

