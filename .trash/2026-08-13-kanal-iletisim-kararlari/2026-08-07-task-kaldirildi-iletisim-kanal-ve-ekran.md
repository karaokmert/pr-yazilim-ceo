# Karar: `Task` çağrısı kaldırıldı — iletişim kanal ve ekran üzerinden

**Tarih:** 2026-08-07
**Karar veren:** Mert
**Kapsam:** `agent-project` fabrikası (PAM/PAD/PQA/PCA) — ve emsal olarak diğer ekipler

## Karar

**Agent'lar birbirini `Task` aracıyla çağırmaz.** İletişim iki yoldan biriyle olur:

- **Kanaldan gelen handoff** — agent kendi `outbox`'ına yazar, yönetici okur ve
  hedefin `inbox`'ına iletir
- **Ekrandan gelen handoff** — yönetici ekrana basar, kullanıcı taşır

İkisi birbirini dışlamaz. Kanala yazılması ekrana basılmayacağı anlamına gelmez;
kullanıcının görmesi gereken bir devir hem kanala hem ekrana gider.

Mert'in cümlesi: *"KARAR Task yok artık. İletişim ekrandan gelen handoff ya da
kanaldan gelen handoff ile yapılır."*

## Neden

Zincirin görünürlüğü. Bir agent diğerini `Task` ile çağırdığında rapor kullanıcıya
değil **çağırana** gidiyor — ölçüldü, 2026-07-30: bir denetçi doğrudan çağrıldı,
raporunu üreticiye verdi, atmadığı bir push'u attım dedi ve `origin/main` eski
commit'teydi. Zincir görünmez olunca hata da görünmez oldu.

Kanal bunu mekaniğe taşıyor: kutuya yazılan mesaj kalıcıdır, yönetici okur, ilettiği
görünür. Görünürlük artık bir kural metnine değil dosyanın kendisine dayanıyor.

## Neyi etkiliyor

**`ISD-KEEP-CHAIN-ONE-DEEP` — KALDIRILIYOR.** (Mert'in kararı, 2026-08-07)

Kural *"personeli yalnız PAM çağırır"* diyor ve gerekçesi doğrudan araca dayanıyor:
*"sınır araçla değil davranışla çizili, `Task` aracı iki personelde var."*

`Task` kalkınca *"çağırmak"* diye bir eylem kalmıyor — kimse kimseyi çağırmıyor,
yönetici iletiyor. Kuralın işlevi kanal topolojisinin kendisine geçti: kanal zaten
agent'ın agent'a yazmasına izin vermiyor, her agent yalnız kendi kutusuna yazıyor.

Yerine kanona giren şey bir yasak değil bir **tanım**: iletişim kanal aracılığıyla ve
yöneticinin iletmesiyle yapılır.

Bu kural cascade'in merkezi: **16 atıf var ve dört agent body'sinin hepsi dahil**
(PAM ölçtü, 2026-08-07).

**`ISD-PRINT-DONT-WRITE`** — Kural şu an *"iki geçerli yer var: bir sub-agent'a
gidiyorsa blok `Task` çağrısının görev tanımıdır, kullanıcıya sunuluyorsa ekrana
basılır. Üçüncü bir yer yok"* diyor.

`Task` ucu ortadan kalktı. PAM'in değerlendirmesi: bu bir kapsam cümlesi eklemesi
**değil**, eksen değişimi. Kapsam cümlesi eklenirse hüküm *"Task ya da ekran, bir de
kanal"* der ve okuyan `Task`'ı hâlâ geçerli sanır — ihlali sessiz olur çünkü cümle
kendi içinde tutarlı görünür.

**Bir tuzak (PAM'in bulgusu):** kanal kutusu bir dosyadır. Yeni hüküm *"dosyaya yazma"*
diye kalırsa kendi kendini çeler. Ayrımı taşıyacak şey dosya/ekran ayrımı değil,
**kalıcı iş belgesi / geçici devir metni** ayrımı: kanal dosyası devir metnini taşır
ve okununca işlevi biter; `docs/` altındaki belge kalır.

**Düzeltme (2026-08-07):** Bu dosyanın ilk hâlinde *"index'teki atıf listesi boş, yani
liste güvenilir başlangıç noktası değil"* yazıyordu. Bilgi **eskimiş**. PAM aynı gün
ölçtü: liste dolu — `ISD-PRINT-DONT-WRITE` 4 atıf, `ISD-KEEP-CHAIN-ONE-DEEP` 16 atıf.
Kaynak ölçüm (PQA, 2026-08-03) o gün doğruydu; atıf haritası onarımı aradaki turlarda
koştu. Ayrım önemli: yanlış bilgi düzeltilir, **tarihi geçmiş bilgi yeniden ölçülür**.

**Devir bloğunun biçim kuralları** (`ISD-NAME-BOTH-ENDS`, `ISD-MARK-TYPE`,
`ISD-SAY-WHY`, `ISD-POINT-DONT-PASTE`, `ISD-NO-EXTRA-SECTION`, `ISD-ONE-TARGET`)
— bunlar taşıyıcıdan bağımsız, biçimi düzenliyorlar. Kanal mesajının içine giren
blok da aynı biçimde yazılır.

**`ISD-POINT-DONT-PASTE` bu düzende daha da önemli.** İş belgesi (gereksinim.md)
dosyada yaşar ve adresle gösterilir; devir metni bloktur ve taşınır. İkisi ayrı
şeyler — kanal ikisini de bozmuyor, yalnız devir metninin taşıyıcısını değiştiriyor.

## Yasak araca değil, hedefe bağlı (Mert, 2026-08-07)

**Hiçbir araç yasaklanmıyor.** `tools:` / `disallowedTools:` satırı hiçbir agent'a
eklenmiyor. Mert'in cümlesi: *"Araçları yasaklamıyoruz, `tools`'a araç eklemiyoruz
hiçbir araç için."*

Sınır **kime çağrı yapıldığında**:

- **Ekosistem agent'ını çağırmak yasak.** PAM, PAD, PQA, PCA — ya da başka bir
  ekipten bir personel. Bunlarla iletişim kanaldan ve yöneticinin iletmesiyle olur.
- **Ara araçlar serbest.** `general-purpose`, `Explore` gibi isimsiz yardımcılar
  kullanılabilir.

Gerekçe kararın kendi gerekçesinden çıkıyor: engellenen risk *"rapor kullanıcıya
değil çağırana gidiyor."* İsimsiz yardımcı **rapor vermiyor, ölçüm veriyor** ve
hiçbir kapıyı kapatmıyor — zincirin görünürlüğü orada risk altında değil.

Bu ayrım kanonda zaten var (`CLAUDE.md:180`, `is-duzeni:19`, `is-duzeni:214`):
*"isimsiz yardımcı bir rol değil, bir alet: ölçüm alır, kapı kapatmaz."* Karar o
ayrımı korur ve mekanikleştirmez.

**Bunun koruduğu şey:** davranış testi. Bir agent kendi ürettiği dosyayı kendi
okuyup *"anlaşılır"* diyemiyor — temiz bir yardımcıya okutup davranış ölçüyor
(`uretim:307`, `PAD-TEST-BEFORE-HANDOFF`). İsimsiz yardımcı da kaldırılsaydı bu
kapı sessizce kapanırdı (PAM'in bulgusu, 2026-08-07).

**`CLAUDE.md` düzeltilmeli.** Satır 165-168 hâlâ *"PAM diğer üç personeli `Task` ile
çağırır"* ve *"sınır araçla değil kuralla çizili"* diyor — ikisi de eskidi. Satır 180
(isimsiz yardımcı ayrımı) doğru ve korunur.

## Ne değişmiyor

Devir bloğunun kendisi. Biçim aynı, gerekçe zorunluluğu aynı, direktif yasağı aynı,
tek hedef kuralı aynı. Değişen yalnız **taşıyıcı**: `Task` çağrısı yerine kanal kutusu
ya da ekran.

## Uygulama

Bu karar `docs/fabrika/kanal-protokolu/` işinin kapsamına giriyor. PAM gereksinimi
güncelledi (2026-08-07), PAD kanona yazacak, PQA denetleyecek. Push onayı Mert'te.
