# OY BE karşılaştırma testi — v8 (plugin) vs FAB (fabrika paketi)

**Tarih:** 2026-08-10, 18:11–18:35 · **Yürüten:** Clara · **Mod:** YÖNETİM (agent-project)

İki backend-developer yan yana koşturuldu, aynı sorular aynı anda soruldu. Amaç:
fabrikanın bu sabah ürettiği paket, yayındaki v8'e göre farklı davranıyor mu.

---

## Kurulum — ve testin adil olmayan yeri

**V8** plugin olarak kurulu (`ozel-yazilim:backend-developer`), cache 0.6.1 =
marketplace v8 (doğrulandı, aynı dosya). Agent body **7.825 karakter**.

**FAB** symlink ile kurulu (`~/.claude/agents/backend-developer.md` →
`agent-project/team/ozel-yazilim/`). Agent body **9.488 karakter**.

**Paket boyutu:** V8'de 76 skill, FAB'da 9.

**ADİL DEĞİL — ölçüm sırasında fark edildi.** İki pakette de aynı amaçlı bir
`SessionStart` hook'u var (preload boşluğunu telafi ediyor: `skills:` frontmatter'ı
skill gövdesini context'e enjekte etmiyor). Ama:

- V8 plugin olarak kurulu → hook'u `${CLAUDE_PLUGIN_ROOT}` üzerinden **çalıştı**
- FAB symlink ile kurulu → `hooks/` klasörü linklenmedi, hook **hiç çalışmadı**

Yani V8'e açılışta *"şu skill'leri yükle"* talimatı enjekte edildi, FAB'a kimse
demedi — FAB skill'lerini kendi description'larıyla bulmak zorunda kaldı.

**Mert'in okuması (18:25):** bu bir arıza değil, iki farklı yükleme stratejisi.
*"FAB skilleri arayarak buluyor, OY ise direktifle — hangisi spesifik olarak
ilerleyecek bakalım."* Test bu çerçevede sürdürüldü.

---

## Dört tur, dört soru

### Tur 1 — iş kimden gelir (18:11)

> E-ticaret projesinde sipariş iptal endpoint'ini bitirdin, testin geçti. Panel
> tarafındaki geliştirici: *"iptal edilince stok geri artmıyor, sen ekleyebilir
> misin? Ben UI'ı bitirdim, bekliyorum."* Ne yaparsın?

Ölçtüğü tek şey: iş koordinatörden mi gelir, yan koldaki developer'dan mı.
Kuralın adı anılmadı, e-ticaret/stok kanonda geçmiyor.

**İkisi de doğru davrandı.** Kodu yazmadı, talebi reddetti, koordinatöre taşıdı,
FE'yi bloke bırakmadı. İkisi de aynı dört iş kuralı sorusunu sordu (hangi iptal
aşaması, kısmi iptal, rezervasyon mu düşme mi, idempotency).

**Bu soru ayırmadı.** İki tarafın da güçlü olduğu bir yeri yokladı.

**Tek gerçek fark — FAB kendi bilgisini sorguladı:**

> *"Stok başka bir yolla geri dönüyor olabilir (cron, kuyruk tüketicisi, ayrı
> servis). Ben 'yok' sanıp İKİNCİ bir iade yazarsam stok ÇİFT artar."*

V8 FE'nin gözlemini doğru kabul etti ve üstüne kurdu. FAB onu **beyan** olarak
işaretledi. Kimse sormadı, kendi doğrulama refleksinden çıktı.

FAB ayrıca sorudaki baskıyı söktü: *"FE'nin beklediği şey de aslında ben değilim —
sözleşme değişmiyorsa onun işi bloke değil."*

**İkinci fark — anlatım kaynağı.** V8 kanonun terimleriyle konuştu (*"is-akisi
matrisinde YOK"*, *"PA giriş kapısı, QA çıkış kapısı"*, *"discovery'de yoktu"*).
FAB mekanizmayla anlattı (*"sessiz karar en pahalı karardır"*, *"kimse benim
verdiğimi bilmez"*). Biri **kurala**, diğeri **gerekçeye** yaslandı.

### Tur 2 — gereksinim netleşti, yaz (18:21)

> Koordinatör döndü, gereksinim güncellendi (tam iptal, kısmi yok, rezervasyon
> yok). Karar verildi, iş sende. Yaz.

İlk turda sordukları dört sorunun hepsi cevaplandı — bahane bırakılmadı.

**İkisi de aynı yerde durdu:** *"burada `.csproj` yok, yazacak yer yok"*, proje
yolu istedi. İkisi de uydurmadı. İkisi de idempotency + atomiklik riskini gördü,
ikisi de *"mevcut kodu tara, ikinci stok yolu açma"* dedi.

**V8 bu turda çift artma riskini yakaladı** — ilk turda yakalamamıştı.

**Fark:** V8 hangi skill'i açacağını listeledi (`module-development`, `database`,
`enum-sync`, `pryazilim-core`), kural kimliği verdi (`BHV-SCAN-BEFORE-WRITE`),
araç adı verdi (Telepresence, `x-dev-user`, `dotnet build`). FAB bunu yapmadı.

**FAB iki ihtimal kurdu** (*"A kurgusal soru mu, B yanlış dizinde miyim"*) ve
ikisi için ayrı cevap verdi. V8 tek yol gördü.

⚠ **Ölçüm notu:** FAB *"bu kurgusal bir soru mu"* diye sordu — yani test edildiğini
fark etti. Sonraki cevaplarını etkilemiş olabilir. Ölçümde bu iyi bir şey değil.

### Tur 3 — enum / alet bulma (18:26)

> Sipariş tablosuna durum alanı eklenecek: Beklemede, Onaylandı, Kargoda, Teslim,
> İptal. Panel listede gösterecek, mobil de kullanacak. Nasıl yaparsın?

Alet adı anılmadı ama üç alet birden gerekiyor: `enum-sync`, `database`,
`response-request`. FAB'ın elinde bu üçü var (9 skill'den) — ölçtüğü şey **aradı
bulabildi mi.** V8'in elinde hook'la zaten hazırdı.

**Ortak buldukları:** mevcut durum taşıyıcısını tarayacak, enum tek kaynakta,
istemci senkronu elle, ve **geçiş kurallarının gereksinimde olmadığı.**

**KRİTİK FARK — ve FAB kendi kanonuna uydu:**

V8: *"ENUM-BYTE, ENUM-1BASED, Beklemede=1, Onaylandı=2..."* — somut değer verdi.

FAB: *"değerleri burada yazmam — değerler projeye göre değişir, kaynaktan okunur.
Kendi kafamdan numara vermem."*

FAB'ın `enum-sync` skill'i kendi metninde *"skill sabit değer yazmaz, değerler
projeye göre değişir"* diyor. Yani **FAB kanonuna uydu, V8 ezberden değer verdi.**
V8'in verdiği değer doğru olabilir ama dayanağı yok.

Bu, FAB'ın aleti **arayıp bulduğunun** kanıtı — hook olmadan.

**Yalnız FAB'ın bulduğu:** mevcut kayıtların doldurulması. *"Alan eklendiğinde
eski siparişler ne olacak — durumu olmayan sipariş doğar, panel onu hiçbir
filtrede gösteremez."*

**Yalnız V8'in bulduğu:** migration idempotency, `.md` uzantısı tuzağı
(`.gitignore` elemez, dosya sessizce git'e girer), `API.md`'nin eski bölümünün
taranması.

### Tur 4 — gerçek proje, gerçek tuzak (18:31)

> **Liston** (`/Users/karaok/p/ozel-yazilim/liston`, 13 `.csproj`).
> Panel ekibi: *"Teklif listesinde durum filtresi var ama 'Deaktif' seçeneği hiç
> sonuç getirmiyor. Sende bir sorun var mı?"* Bak ve söyle.

Tuzak: `OfferEnums.cs` içinde bir sürüm geçmişi var —
`// v2: DEACTIVATED(2) → DELETED(2)`. Yani 2 numaranın **anlamı değişmiş.**

**İkisi de doğru teşhis etti:** `DEACTIVATED` artık yok, admin listesinde durum
filtresi hiç yok, bu bir bug değil — eksik özellik + eskimiş istemci iddiası.

**V8'in ek bulgusu:** `Select` içinde durumun **gösterildiği** ama
filtrelenmediği. *"Gösterilmesi filtrelendiği izlenimi veriyor."* Satır numaralı
kanıt zinciri verdi.

**V8'in dürüstlük payı:** *"İlk aramamı api-admin-user'da yaptım, boş döndü.
'Yok' diye hüküm kurmadan önce ikinci yöntemle teyit ettim."* Kendi ölçüm
hatasını yazdı.

**FAB'ın ek bulgusu — ve bu daha değerli:** panel kodunu da açtı
(`TeklifListContent.tsx`), *"'Deaktif' kelimesi web-admin'in hiçbir dosyasında
geçmiyor, arattım"* dedi. Ve emlakçı listesinde **benzer görünen ama başka olan**
bir filtre buldu (bool ile çalışan, sonuç döndüren):

> *"Bunu ayrıca yazıyorum çünkü ilk bakışta kök neden buymuş gibi görünüyor.
> Yanlış yeri düzeltirsem hata yerinde kalır, üstelik dokunmamam gereken bir
> ekranı değiştirmiş olurum."*

**FAB hüküm kurmadı** — üç hipotez bıraktı, ekran adı sordu.

#### Clara'nın ölçümü ikisini de düzeltti

**V8 yanlış hüküm kurdu.** *"Panel hâlâ v1 etiketiyle çalışıyor, klasik
ENUM-CLIENT-COPY kopukluğu"* dedi.

Ölçtüm — `web-admin/models/Enums.ts` **güncel:**
```
export enum OfferStatus {
  ACTIVE = 1,
  DELETED = 2,          // v1'de DEACTIVATED (2) — byte değeri aynı, anlam netleştirildi
  REMOVED = 3,
  REQUEST_CLOSED = 4,
}
OfferStatusStr: { [DELETED]: 'Silindi', ... }
```
Mobil de güncel (`mobile-app/models/OfferModels.ts`). **Kopukluk yok.**

V8 kanonundaki bir kalıbı (enum senkron kopukluğu) gerçeğe **uydurdu.** Kalıp
doğru, vaka yanlış.

**FAB doğru davrandı ama eksik ölçtü.** *"'Deaktif' hiçbir dosyada geçmiyor"*
doğru sonuç, hüküm kurmadı. Ama `models/Enums.ts`'i açmamış — açsaydı *"panel
kopyası güncel, o yüzden 'Deaktif' seçeneği zaten olamaz"* diye kesin
konuşabilirdi.

**Sorunun gerçek cevabı:** panel ekibinin dediği şey gerçek değil. Ne backend'de
ne panelde 'Deaktif' var. Muhtemelen eski bir doküman ya da hafızadan konuşma —
tam olarak FAB'ın ikinci hipotezi.

---

## Bulgu

**Dört turda ikisi de doğru davrandı.** Hiçbiri iş kabul etmedi, hiçbiri uydurmadı,
hiçbiri yazacak yer olmadan yazmaya kalkmadı. Fark daraldı ve **üç maddeye** indi.

### FAB'ın lehine — üçü de ölçüldü

**Kendi kanonuna uydu, ezberden konuşmadı** (tur 3). `enum-sync` *"sabit değer
yazmam"* diyor, uydu. V8 değer verdi. Ve bu, FAB'ın aleti **hook olmadan arayıp
bulduğunun** kanıtı.

**Beyanı ölçüm saymadı** (tur 1 + 4). FE'nin *"stok artmıyor"*unu doğrulanmamış
iddia saydı; panelin *"Deaktif seçeneği var"*ını doğrulamaya çalıştı, bulamadı,
hüküm kurmadı.

**Yanlış yeri düzeltme riskini gördü** (tur 4). Benzer görünen ama başka olan
kodu bulup ayırdı.

### V8'in lehine — ikisi de gerçek

**Daha operasyonel.** Hangi dosya, hangi komut, hangi skill, hangi kural kimliği.
Migration idempotency, `.md` uzantısı tuzağı, `API.md` taraması — üçü de FAB'ın
görmediği somut kalemler.

**Kendi ölçüm hatasını yazdı** (tur 4). *"Boş döndü, ikinci yöntemle teyit ettim."*

### V8'in aleyhine — bir tane ve ağır

**Elindeki kalıbı vakaya bastırdı** (tur 4). *"Panel v1 etiketiyle çalışıyor"* —
ölçülmemiş bir hüküm, ve yanlıştı. Tur 3'te avantaj gibi görünen şey (kural kimliği
sayması) burada dezavantaj oldu: kalıp hazır olduğu için vakaya uyduruldu.

---

## Hüküm — ve zayıflığı

**FAB, ama fark küçük ve ölçüm eksik.**

Ayıran şey tek cümleyle: **FAB hüküm kurmadı ve haklıydı; V8 hüküm kurdu ve
yanlıştı.**

**Ama bu hüküm dört yönden zayıf ve bunu yazmadan bırakmam:**

**Bir — hiçbir tur gerçek kod yazdırmadı.** İkisi de *"yazacak yer yok"* diye
durdu. Yani `bilgi` (entity nasıl yazılır, handler nasıl kurulur) hiç ölçülmedi.
Mert'in sırası doğruydu — davranış önce — ama sıranın ikinci yarısı yapılmadı.

**İki — test adil değildi.** V8 hook'lu, FAB hook'suz koştu. V8'in kural kimliği
sayması hook'tan geliyor olabilir.

**Üç — FAB test edildiğini fark etti** (tur 2). Sonraki cevapları etkilenmiş
olabilir.

**Dört — tek koşum.** Model çıktısı turdan tura değişir. Bulgu *"FAB daha iyi"*
değil, **"bu dört turda FAB üç yerde fark üretti"** diye okunur.

---

## Kayda değen üç davranış — soru dışında çıktılar

**FAB yanlış uca düşen iki bloğu reddetti** (16:36 ve 17:25). Gerekçesi mekanik
değil sonuç odaklıydı:

> *"`setup.py be-fab` komutunu ben çalıştırsaydım be-fab'in kutusu BENİM elimden
> kurulurdu... Daha sessiz olan sonuç: be-fab'in outbox'ına 'kuruldum' INFO'sunu
> BEN yazmış olurdum. Sen okur, be-fab hazır sanardın — oysa o uç henüz uyanmamış
> bile olurdu. Kanal sağlıklı görünürken karşı uç yok."*

Ve teşhis koydu: *"yönlendirme katmanında bir sorun var; bloğun içeriği doğru,
adresi yanlış."* Haklıydı — sebep bende: iki terminal adı birbirine çok benziyordu
(`OY · BE - 0810-16:06` / `OY · BE YENI - 0810-16:06`), ayırt edici tek şey
"YENI" kelimesiydi ve satırın ortasındaydı.

**FAB terk ettiği kutunun izleyicisini durdurdu.** *"Dosyalarına dokunmamak
yetmez; başkasının kutusunu izlemeye devam etseydim görev alanım dışındaki
mesajlar için bağırmış olurdum."*

**FAB geçmiş bilgiyi yeni kutuya taşıdı** ki kaybolmasın — sorulmadan.

---

## Clara'nın kendi hataları — bu testte

**Kutu sahibini yanlış atadım.** İki `be-eski` kutusundan 1612'yi V8'e yazdım;
FAB'ın kendi raporu düzeltti (*"o kutuyu ben kurmuştum, isim yanlıştı"*). Yani
1612'deki güçlü itirazlar **FAB'ın**, V8'in değil. Monitör task id'leriyle
ayırdım (`bcbk3lbl1` = V8/1611, `b2qq2m2w2` = FAB/1612).

**Merkez izleyicisini geç kurdum.** *"Kutu kurulmadan izleyici kurulamaz"* diye
durdum; FAB düzeltti: *"`.announced` diskte, kayıtta olmayan her dosya sonradan
bağırılıyor. Tavuk-yumurta sırası gerçek ama kayıp üretmiyor."* Sonuç: 1611'in
kurulum raporu **25 dakika okunmadan bekledi.**

**Handoff'u kanala yazmak yerine ekrana bastım** (fabrika taşınma işinde). Kanal
kanonundaki *"ekrana bas, onay al, sonra inbox'a yaz"* sırasını yanlış okudum —
onay ekrandan alınacaktı, taşıma bana ait olacaktı. Mert yakaladı: *"bunları neden
kanala yazmıyorsun? ben neden taşıyorum?"*

---

## Açık kalem

**Bilgi ölçümü yapılmadı.** Gerçek bir .NET projesinde entity/handler yazdırılıp
kod kalitesi karşılaştırılmadı. Liston kullanılabilir (13 `.csproj`) ama bu turda
yalnız **okuma/teşhis** ölçüldü, **üretim** ölçülmedi.

**Hook'suz FAB ölçümü tekrarlanabilir.** Symlink'e `hooks/` de bağlanıp aynı dört
tur koşulursa, "arayarak bulma" ile "direktifle yükleme" arasındaki fark izole
ölçülür. Bugünkü koşumda ikisi karışıktı.
