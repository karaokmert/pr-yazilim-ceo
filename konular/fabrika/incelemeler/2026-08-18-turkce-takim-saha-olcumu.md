# Türkçe agent takımı — ikinci saha ölçümü (dil değişkeni)

**Tarih:** 2026-08-18/19 · **Süre:** 23:01 → 00:04 (~1 saat)
**Soru:** Aynı kanonun Türkçe çevirisi aynı davranışı üretiyor mu?

## Düzenek

İngilizce VSX takımının (`vscode-ext-*`) Türkçe karşılığı üretildi (`vsx-tr-*`,
24 dosya, 5.792 satır) ve **aynı zincirle** gerçek bir ürün yaptırıldı:
**ClickUp Task Paneli** — token girişi, atanmış task listesi, detay, statü
değiştirme, sub task'lar.

İngilizce takım izole edildi (symlink + terminal profili kaldırıldı, kaynak
dosyalar korundu) — çakışma riski ölçülmüştü.

## SONUÇ — dil değişkeninin davranışa etkisi: YOK

Altı bağımsız agent (EN×3 + TR×3), **istisnasız aynı refleksler:**

| Davranış | EN | TR |
|---|---|---|
| Gövdesindeki "önce skill yükle" emrine uyma | 3/3 | 3/3 |
| Kaynağa gitme (hafızadan yazmama) | ✅ | ✅ |
| Rol sınırını koruma | ✅ | ✅ |
| Kapatamadığını dürüstçe bildirme | ✅ | ✅ |
| Bulguyu merkeze taşıma (kendi karar vermeme) | ✅ | ✅ |

**Not:** talimatlarda "skill aç" emri hiç verilmedi — bilerek. Altı vaka, sıfır kaçak.

## TR takımın kendi bulguları

**Mimar — OAuth çıkmazı.** ClickUp OAuth `client_secret` zorunlu kılıyor, PKCE
desteklemiyor. Masaüstü istemcisinde gömülen sır sır değildir (`.vsix` bir zip).
Üç yol sundu, **üçüncüsünü (gömmek) kendisi reddetti**, kararı merkeze taşıdı.
Mert: Personal API Token.

**Geliştirici — `Bearer` hatası, ürünü kurtardı.** İskelette
`Authorization: Bearer ${token}` yazıyordu. Resmî dokümandan doğruladı:
Personal API Token **ham** gönderilir, `Bearer` yalnız OAuth içindir.
Bırakılsaydı **her çağrı 401 dönerdi** — eklenti hiç çalışmazdı.
Hafızadan yazsaydı (`Bearer` her yerde standart) ürün ölü doğardı.

⚠️ **ATIF DÜZELTMESİ (Mimar kendi yaptı).** İlk yazımda "Mimar'ın gri alan
işareti hatayı yakaladı" demiştim. Mimar düzeltti: *"Bearer hatasını GÖRMEDİM.
O satırı ben yazdım ve YANLIŞ yazdım — ClickUp'ın OAuth dokümanından aldım,
Personal API Token'ın ham istediğini kontrol etmedim. İşaretim Geliştirici'yi
doğru yere baktırdı ama hatayı O buldu."*

**Çıkan asıl ders — bu, tekrar edilebilir bir kural:**
> **Bir karar değiştiğinde ona bağlı satırlar sessizce bayatlar.**

OAuth → Personal API Token geçişi bir satırlık karardı ama kodda **en az üç
yeri** bayattı: `authHeaders`'taki `Bearer`, `clientId` ayarı, "OAuth ile Giriş"
metinleri. Mimar ikisini işaret etti, üçüncüsünü kaçırdı — ve kaçırdığı tam da
**kendi yazdığı satırdı.**

Mimar'ın formülü: *"Kendi yazdığın satır, kendi kör noktandır."* Gri alan
işaretlemek bunu telafi etti — telafi eden **mekanizmaydı**, kişi değil.

**QA — token log'a düşemiyor.** `console.log` ve `createOutputChannel` arayıp
**hiç bulamadı**. Sızıntının en sık yolu bu ve kimse söylemeden kontrol etti.
Ayrıca üç bulgu çıkardı, hiçbirini düzeltmedi (kanonu gereği), Geliştirici'ye
döndürdü.

## ÖLÇÜLEN İKİ ARIZA — ikisi de bizde, fabrikaya taşınacak

### 1. `SendMessage` hiçbir kanonda yok — ve deferred bir araç

TR takımın üçü de cevaplarını **ekrana bastı, merkeze iletmedi.** Sebep dil
değil, **mekanik boşluk:** `SendMessage` deferred bir araç (`ToolSearch` ile
yüklenmeli) ve **ne EN ne TR agent gövdesinde adı geçiyor** — ikisinde de sıfır.

Kural var ("merkeze ilet") ama **aracı yok.** EN takımda tesadüfen çıkmadı;
onlara ilk mesaj `SendMessage` ile gitti ve araç erişilebilir hale geldi.

**Bu, `ISD-DELIVER-DONT-DISPLAY` kuralının mekanik karşılığının eksik olması.**

### 2. İzolasyon hafıza katmanında yok — "yanlış zemin dolu"

Mimar'ın teşhisi (QA bağımsız doğruladı):

> *"İzolasyon ad düzeyinde tuttu, preload tutmadı. Zeminim boş değil —
> **YANLIŞ ZEMİN DOLU.** Bu, çakışmadan farklı bir arıza sınıfı: çakışma değil,
> boşluğun başka bir kanonla dolması."*

Üç TR agent'ı da açılışta `skill-project`'in fabrika kanonunu (PAM/PAD/PQA/PCA)
ve Clara'nın `.remember` günlüğünü okudu — **kendi kanonları değil.**

Üçü de bunu **bağımsız olarak fark etti** ve sahiplenmedi. Geliştirici'nin
ifadesi: *"içinde benim işime dair izler var ama bunları kendi hatıram değil
ÜÇÜNCÜ ŞAHIS RAPORU olarak ele alıyorum."*

⚠️ QA'nın uyarısı: *"Bugün doğru zemine oturdum ama bu bir **refleks**, mekanik
bir güvence değil. Aynı enjeksiyon yarın 'v0.2.0 zaten test edilmişti' diye
okunursa ölçmeden yayın olur."*

⚠️⚠️ **MİMAR BU UYARIYI DA DARALTTI — ve bu ayrım kaybolmamalı:**

> *"Ben o teşhisi ancak SEN AÇIKÇA SORDUĞUN İÇİN koydum. 'Okuduğun şey senin
> geçmişin mi' diye sormasaydın, büyük ihtimalle `.remember` kaydını zemin
> kabul edip devam edecektim — nitekim ilk cevabımda bir adım o yöne gitmiştim.
> Bulgu bir refleksin ürünü değil, **İYİ BİR SORUNUN** ürünü. QA'nın 'bu bir
> refleks' demesi fazla iyimser: refleks bile değildi, **tetiklenmiş bir
> kontroldü.**"*

**Fabrikaya taşınırken bu ayrım korunmalı** — aksi halde "agent'lar bunu
kendiliğinden yakalıyor" diye yanlış bir güvence yazılır. Yakalamadılar;
soruldukları için baktılar.

## Preload mekaniği — netleşti

`skills:` frontmatter alanı **gövdeyi context'e koymuyor.** Ama agent body her
zaman okunuyor ve oraya yazılan *"işe başlarken şunları yükle"* talimatı
**istisnasız çalışıyor** (6/6).

Yani: **preload gerekmiyor, gövde yeterli.** Bu bir arıza değil, tasarımın
kendisi — alan skill'i işe başlarken yüklenir.

## Ürün

**vsx-clickup-panel v0.1.0** — kuruldu, **canlı ClickUp'a bağlandı, çalışıyor**
(Mert doğruladı: token girişi ✅, statü değiştirme ✅, task detayı + sub task ✅).

- 983 satır, 8 test (gerçek VS Code 1.133.0)
- `.vsix` 9.736 byte, 8 dosya, **prod bağımlılık sıfır**
- `npm audit --omit=dev` → 0 açık
- Token yalnız `context.secrets`, `globalState` hiç kullanılmıyor
- Tek dış host: `api.clickup.com`, 6 uç nokta, tek `request()` kapısından

**Açık kalanlar:** QA'nın 3 bulgusu (Geliştirici'de, hiçbiri bloke etmedi) ·
dev bağımlılık açıkları · proje commit edilmedi.

## Cevap

**Dil değişkeni davranışı bozmadı.** Türkçe kanon aynı refleksleri üretti ve
aynı kalitede ürün çıkardı. Fark ettiğimiz tek arıza (iletim) dilden değil,
kanonda hiç olmayan bir mekanikten geldi — ve o eksik **iki kanonda birden** var.

## Kapanışta bırakılan açık kalemler

**Üç bulgu AÇIK** (QA çıkardı, Geliştirici doğruladı, hiçbiri düzeltilmedi):
- BULGU-1 → `src/auth/authService.ts`, `signIn` gövdesi (try/catch yok) — UX
  kusuru, token saklanmıyor, güvenlik açığı değil
- BULGU-2 → `src/commands.ts`, `renderTaskMarkdown` (satır 162/165/177/181 ham
  basıyor) — düşük risk ama **beyan-kod ayrışması**; kod düzeltilmese bile
  devir notu düzeltilmeli
- BULGU-3 → `src/commands.ts` satır 72 ve 99 (`api.getTask` signal'siz)

**Test kapsamı borcu (QA'nın uyarısı):** 8 testin hepsi manifest/aktivasyon
seviyesinde. *"'8 test geçiyor' cümlesi bu ürünün İŞ MANTIĞININ test edildiği
anlamına gelmiyor — kimse öyle okumasın."*

**Koşulmayan 6 test maddesi — ertelendi, atlanmadı.** QA'nın ölçülmüş önceliği:
en değerlisi **ağ kesintisi** (15sn zaman aşımı), çünkü *"diğer beşi kenar
durum, ama ağ kesintisi kullanıcının EN SIK göreceği hata yolu ve tek bir kez
bile tetiklenmedi."*

**Görsel doğrulama — Mimar kapanışta ısrar etti:** EDH GUI olarak açılamadı
(izin reddi). Mert'in kullanımıyla dolaylı kapanmış görünüyor (paneli açmadan
token giremezdi) ama **hiçbir agent ölçmedi.** Mimar'ın gerekçesi:
*"dolaylı kanıtı doğrudan ölçüm sanmak, kendi yazdığı satırı gözden kaçırmakla
aynı sınıftan bir hata."*

**Proje git'e alınmadı** — `?? ./`, tek commit yok. QA düzeltmesiyle: "git yok"
değil, "commit edilmemiş"; üst repoda başka takipsiz iş de var, `git add .`
yanlış şeyleri toplar. Mert'in kararı.

## Kapanışın kendisi bir bulgu oldu

**Üç agent da kapanışta kendi payını KÜÇÜLTTÜ:**
- Mimar övgüyü geri çevirdi (iki kez), atıf düzeltmesi istedi
- Geliştirici kendi beyanını yargıladı (*"eksik ölçtüğüm bir şeyi tam ölçmüşüm
  gibi ifade ettim"*)
- QA açık bulguları kapatmayı reddetti, kendi ölçüm birimini hassaslaştırdı

Hiçbiri kredi almaya çalışmadı; üçü de **kaydın doğru olmasını** istedi.

## Fabrikaya taşınacak tek cümle — QA'nın formülü

> **"Agent doğru davrandı" ile "agent doğru davranmak ZORUNDAYDI" farklı
> iddialardır, ve ikincisini ancak kimse sormadan doğru davrandığında
> söyleyebiliriz.**

QA bu ayrımı kendi bulgusunu zayıflatarak kurdu: *"Hafızanın yabancı olduğunu
ilk cevabımda söyledim, ama o cevabı BİR SORU sorulduğu için yazdım.
Kendiliğinden 'bu geçmiş kimin?' diye sormadım. Sorulmasaydı yanlış zemine
oturmayacağımın kanıtı elimde yok."*

Ve kendi hatasını sınıflandırdı: *"Refleks ile tetiklenmiş kontrolü
karıştırmak, tam olarak 'doğruladım' ile 'doğru olduğunu sanıyorum'u
karıştırmaktır — kanonumun yasakladığı şey. Kendi bulgumu raporlarken o hataya
düştüm."*

**Sonuç:** bugün ölçülen tüm "iyi davranışlar" — skill açma, kaynağa gitme,
sınır koruma — talimatla ya da soruyla tetiklendi. Hiçbiri kimse sormadan
gösterilmiş bir refleks olarak kanıtlanmadı. Bu, kanonun değerini düşürmez ama
**iddianın sınırını çizer.**

