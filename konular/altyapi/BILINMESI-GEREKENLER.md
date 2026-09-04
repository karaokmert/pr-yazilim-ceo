# Altyapı — bilinmesi gerekenler

PR Yazılım'ın sunucu altyapısı: Hetzner'da dedicated + cloud karışık bir yapı, üstünde
Coolify ile yönetilen self-hosted araçlar, ve ekibi tek çıkış IP'sine toplayacak bir VPN.

**Bu konu bir iş alanı değil, henüz bir konu.** Sebebi Mert'in kararı (2026-08-26):
*"bunu biz öğreniriz, sonra seninle beraber bir agent'a çevirelim — artık bu işleri o
yapsın deyip fabrikaya iletiriz."* Yani sorumluluk tanımı şimdi yazılmaz; iş yapıldıkça
birikir, birikince gövde olur.

⚠️ **Bu yüzden burada biriken şeyin türü önemli.** Bir agent gövdesine giden şey adım
listesi değil: **hangi karar neye dayanarak verildi, hangi tuzağa düşüldü, ne ölçülmeden
söylendi.** Adımlar `kayitlar/RUNBOOK.md`'de duruyor ve orada kalsın; buraya karar ve
ders yazılır.

---

## Nerede duruyoruz

**Ana makine:** EX44 `pr-tools` — 65.109.150.95, Helsinki, Ubuntu 24.04, Coolify v4.3.11.
64GB RAM, 14 çekirdek, RAID1 2×512GB NVMe. Kimliği "self-hosted tool sunucusu":
n8n, Qdrant, wg-easy ve zamanla eklenecekler burada yaşayacak.

**Yarım kalan tek iş:** Coolify'da wg-easy servisi eklendi ama **Exited** — çalışmıyor.
Ondan sonraki her şey (güvenlik sıkılaştırma, araç kurulumu, MSSQL'i VPN arkasına alma)
bu adıma bağlı.

**Mimari kararı:** iki katman. Dedicated katman (EX44) araçları taşır; cloud katman
kritik ve esneklik isteyen her şeyi taşır (MSSQL, proje sunucuları). Geçiş yöntemi
kademeli — *"bir günde tüm sunucuları VPN'e kapatma"*, her adım test edilerek.

---

## VPN neden var — asıl ihtiyaç

**Sabit çıkış IP'si.** PR Yazılım Azure servislerine, kendi MSSQL'ine ve **dış
müşterilerin sunucularına** erişerek çalışıyor. Ekip nerede olursa olsun tek bir adresten
çıkarsa, o servislerin firewall'ı tek IP'ye kısıtlanabilir — ve müşteriye tek IP
verilebilir.

⚠️ Bu, VPN'i bir kolaylık olmaktan çıkarıp **müşteriye verilen taahhüdün altyapısı**
yapıyor. Kararların gerekçesi burada: `kararlar/2026-08-28-vpn-kararlari.md`.

---

## Açık kararlar

Bunlar dosyaların içine gömülü kalmasın diye buraya çıkarıldı — gömülü karar takip
edilmiyor.

**Floating IP gerekli mi.** Sabit IP artık müşteriye taahhüt; makine değişirse IP değişir
ve her müşterinin firewall'ında kural güncellemek gerekir. Hetzner'ın Floating IP'si
bunu çözüyor ama ⚠️ **ölçülmedi:** o bir Cloud ürünü, EX44 dedicated — dedicated
tarafta karşılığı ne, doğrulanmadı. Kurulumu bloke etmiyor.

**EX44'e VPN'den erişim yöntemi** — peer olarak mı, panelleri VPN-only mi.

**MSSQL sunucusunun OS'i** (cloud "DB Server" CX43) — Windows mu Linux mu netleşmedi.
WireGuard peer kurulumu buna bağlı.

**Fatura kalemleri** — Windows Server 2022 lisansı (27.90€/ay) hâlâ faturalanıyor mu
(bağlı olduğu AX41-NVMe 20 Haziran'da iptal edilmişti), Plesk Web PRO (13.30€/ay)
kullanılıyor mu. Temmuz 2026 faturası ~378€/ay.

---

## Açık risk — kabul edilmiş

Sunucu **root + parola** ile dünyaya açık: SSH key yok, fail2ban yok, firewall yok.
Bu bilerek ertelendi (*"önce VPN'i göreyim"*). Runbook bunu *"kısa tutulacak bir köprü"*
diye yazıyor ama **köprünün ne zaman açıldığı hiçbir yerde yazmıyor** — süre bilinmeden
risk ölçülemiyor.

⚠️ Ders: kabul edilen bir riskin **başlangıç tarihi** yazılır. Tarihsiz bir "geçici"
kalıcıya dönüştüğünde kimse fark etmez.

---

## wg-easy neden Exited'dı — çözüldü (2026-08-28)

Compose okununca sebep göründü, loga bile gerek kalmadı: Coolify'ın hazır şablonu
wg-easy **v14** için yazılmış, ama image `latest` ve o artık **v15**.

Üç kırık vardı. **Entrypoint ezilmişti** — şablon container'ın kendi başlangıcını iptal
edip `wgpw` (v14'ün parola-hash aracı) çağırıyordu; v15'te o komut yok, container
açılır açılmaz ölüyordu. Exited'ın sebebi buydu ve tek başına yeterliydi. **`_PASSWORD`
okunmuyordu** — v15 parolayı ilk açılışta web sihirbazından alıyor. **`WG_HOST` bir
domain'e bağlıydı** (`${SERVICE_FQDN_WIREGUARDEASY}`), oysa sunucuda henüz domain yok;
boş kalırsa panel açılır ama hiçbir client bağlanamaz.

Doğru olanlar zaten yerindeydi: `cap_add` (NET_ADMIN, SYS_MODULE), `sysctls`, UDP 51820
port mapping, volume.

⚠️ **Bunun genel dersi wg-easy'ye özel değil:** bir platformun hazır şablonu, çektiği
image'ın sürümünden **geri kalabiliyor.** Coolify v14 şablonu gösteriyor, `latest` v15
çekiyor, ikisi konuşmuyor. Her Coolify servisinde tekrarlanabilir ve belirtisi hep aynı
— *"kurdum ama Exited"*. Bu yüzden `latest` bırakılmaz, sürüm numarası yazılır.

---

## Kritik dersler (yaşanmış)

**Auction makinesinde kurulumdan ÖNCE disk sağlığı ölçülür.** EX44'ün iki diski de
arızalı geldi: biri SMART FAILED %102 used, öteki 254 integrity error. Hetzner'ın kendi
"quick test"i bunu **OK** diye geçmişti — kendi ölçümünü göstermek gerekti, gösterilince
ikisi de ücretsiz değiştirildi.
`smartctl -a /dev/nvme0n1 | grep -iE 'health|percentage|power on|integrity|error'`

⚠️ Bunun genel hâli: **sağlayıcının "test ettik" beyanı bir ölçüm değildir.** Çelişkiyi
kendi verinle göstermek çalışıyor.

**installimage'da PART değerleri kaydetmeden iki kez okunur.** Swap 8GB planlandı, 82GB
oldu — düzenleme hatası. Zararsız olduğu için bırakıldı ama düzeltilebilir bir anda
fark edilmedi.

**SSH host key ne zaman değişir:** yeniden kurulumdan sonra değişir (`ssh-keygen -R <ip>`
gerekir), sadece reboot'ta değişmez. Karışırsa gerçek bir MITM uyarısı normal sanılır.

**wg-easy bağlanamama = neredeyse her zaman UDP 51820 kapalı.** Panel açılır, hiçbir
client bağlanamaz — belirti yanıltıcı.

**Coolify + WireGuard:** `cap_add: NET_ADMIN, SYS_MODULE` + `sysctls` (src_valid_mark,
ip_forward) şart. Eksikse container kalkar ama tünel kurulmaz.

**Coolify'ın `.env`'i yedeklenir:** `/data/coolify/source/.env` → 1Password.
wg-easy'nin `/etc/wireguard` volume'ü de — kaybolursa tüm peer config'leri ölür.

**tmpfs dolabilir ve disk dolu sanılır.** chatwoot-pr'de `/run` (382MB tmpfs) `containerd`
ile doldu, `df -h /` asıl diski %52 gösteriyordu. Belirti "no space left on device",
sebep ise başka bir dosya sistemi. Reboot çözdü (tmpfs RAM'de).

---

## Yapıdaki gerilim — dedicated risk

Dedicated'da donanım arızası Hetzner'ın değil **bizim** krizimiz; cloud'da makine
otomatik taşınır. RAID1 disk arızasını çözer, **makine** arızasını çözmez.

Bugünkü cevap: kritik veri EX44'te tutulmuyor (zaten cloud'da), araçlar yeniden
kurulabilir, Coolify config + volume'lar dışarı yedeklenir (Storage Box / S3).

⚠️ Bu cevap **full-tunnel seçilirse geçersiz olur** — yukarıdaki açık karara bak.

---

## Kayıtlar

`kayitlar/RUNBOOK.md` — kurulum runbook'u: envanter, adım adım sıradaki işler, wg-easy
compose ayarları, güvenlik felsefesi, fatura notları.

`kayitlar/TRANSCRIPT.md` — kronolojik kayıt: hangi adım ne zaman, hangi komut, ne sonuç.

⚠️ İkisi de Claude Desktop'ta yürütülen bir oturumun devir paketi (2026-08-26). O oturum
kapandı; buradan devam ediyoruz.

---

## Trafik logu ve reklam engelleme — karar ve mekanik (2026-09-02)

**Mert'in kararı: trafik logu tutulacak.** Gerekçesi bir politika: *"şirket
bilgisayarlarını kişisel işler için kullanmamaları gerekiyor, bankacılık işlemlerini
kendi pc'lerinden yapmaları gerekiyor."*

⚠️ **Clara'nın itirazı kayda geçsin — karar buna rağmen verildi.** İtiraz üç
noktadaydı: (1) kural kişisel trafiği şirket makinesinden *uzak tutmayı* amaçlıyor,
çözüm ise onu şirket sunucusuna *yazıyor* — kural tutulursa log boş kalır, tutulmazsa
istenmeyen veri birikir. (2) VPN sürekli açık değil (Karar 2), yani log "şirket
bilgisayarında ne yapıldığını" değil "VPN açıkken ne yapıldığını" ölçer; bunlar aynı
küme değil. (3) Gözetim sebebi kaldırmıyor, üstüne katman ekliyor — sebebi kaldıran şey
engellemek ya da politikanın sonuç doğurması. Sunulan alternatif (DNS filtresiyle
engelleme, kayıt tutmadan) reddedildi.

**WireGuard bu logu vermez.** `wg show` yalnız peer'ın son handshake'ini ve toplam bayt
sayısını verir — hedef adres tutmaz. "Kim nereye gitti" tünelde değil **çıkışta**
cevaplanır.

### Kurulacak yapı — AdGuard Home

Tek bileşen iki işi birden yapıyor: **sorgu kaydı** (hangi client, hangi saat, hangi
alan adı) ve **reklam engelleme**. İkincisi Mert'in ayrı sorusundan çıktı — mobilde
uygulama reklamları VPN üstünden, cihaza hiçbir şey kurmadan engelleniyor.

Katmanlar ve ne verdikleri:

**DNS logu** — okunabilir olanı verir (isim, IP değil). Tek başına **delik**: DoH
kullanan tarayıcı ve doğrudan IP'ye giden trafik görünmez. Bu yüzden DoH engelleme
listesi + tünelden çıkan 53 portunun zorla AdGuard'a yönlendirilmesi **kurulumun
parçası**, opsiyon değil. Eksikse log "temiz" çıkar ve temiz olduğu için doğru sanılır.

**NAT/conntrack kaydı** — baypası yakalar ama isim değil numara verir, hacmi büyük.
Clara'nın önerisi: **şimdilik kurulmaz.** Ancak "biri kasten atlatıyor" şüphesi doğarsa
gerekir; şimdi kurmak okunmayacak veri biriktirmek olur.

**Tam paket kaydı** — kapsam dışı bırakıldı. Full-tunnel'da bu, ekibin bankacılık
oturumunu diske yazmak demek.

### Kurulum sırası — bozulursa ekip internetsiz kalır

AdGuard **önce** kurulur ve çalıştığı doğrulanır, **sonra** wg-easy'nin
`WG_DEFAULT_DNS` değeri ona çevrilir. Ters sırada: tüneldeki herkes ad çözemez.

⚠️ DNS değiştikten sonra **mevcut client config'leri eski DNS'i kullanmaya devam eder.**
Her cihazın config'i yeniden indirilip kurulmalı — yoksa ne reklam engellenir ne log
dolar, ve bu sessizce olur.

### Reklam engellemenin sınırları (soruldu, ölçülmedi — bilinen davranış)

YouTube reklamı geçmez (reklam videoyla aynı adresten gelir), uygulama içi sponsorlu
içerik geçmez (aynı sebep), bazı uygulamalar reklam ağı engellenince açılmaz —
istisna yazmak bir bakım işi. Ve VPN sürekli açık olmadığı için bu "reklamsız telefon"
değil, "VPN açıkken reklamsız".

⚠️ Bir gerilim: reklam engelleme ekibin **kişisel** kullanımını iyileştiriyor, yani
VPN'i kişisel işler için açık tutmayı cazip hâle getiriyor — trafik logunun gerekçesiyle
ters yöne bakıyor.

### Düzeltilen hata — ölçmeden söylenen

Clara *"Coolify'da AdGuard hazır şablonu var"* dedi; **ölçmedi**, başka Coolify
kurulumlarından hatırladığını elindeki bilgi gibi kullandı. Mert *"coolify'da yok
gibi"* deyince düzeltildi.

Doğrusu: AdGuard Home kendi başına çalışan açık kaynak bir uygulama (`adguard/adguardhome`),
şablon olup olmaması hiçbir şeyi değiştirmiyor — Coolify'ın **Docker Compose**
seçeneğiyle compose kendimiz yazılır. Ve bu **daha iyi**: wg-easy'nin Exited arızası tam
olarak şablondan çıkmıştı. Şablon yoksa o tuzak da yok.

⚠️ Ders (tekrar): *hatırladığın da bir kayıttır ve en kırılgan olanıdır.* Bir platformun
neyi barındırdığı, o platforma bakılarak söylenir.

### Kurulumdan önce ölçülecek — sunucuya girilmediği için yapılamadı

**53 portu EX44'te boşta mı.** Ubuntu'da `systemd-resolved` çoğu zaman tutar; tutuyorsa
AdGuard kalkmaz ve belirtisi yine *"kurdum ama Exited"* olur — wg-easy'nin aynısı.

**wg-easy bugün client'lara hangi DNS'i veriyor.** Değiştirilecek değerin bugünkü hâli
görülmeden ayar yazılmaz.

## tools.pryazilim.com "too many redirects" — çözüldü (2026-09-04)

**Belirti:** Coolify paneline domain verildi (`tools.pryazilim.com`), Cloudflare'dan
SSL açıldı, önce çalıştı, sonra tarayıcı "too many redirects" verdi.

**Asıl sebep SSL modu değil, DNS kaydıydı.** A kaydı EX44'ü (65.109.150.95) değil
**178.105.134.101**'i gösteriyordu — Hetzner **Cloud** (Nürnberg) tarafında başka bir
makine. Cloudflare proxy açıkken bu görünmüyordu (dig hep CF IP'lerini döndürüyor);
proxy kapatılınca ortaya çıktı. 307 döngüsünü o yanlış makinedeki servis üretiyordu.

**Çözüm:** Mert A kaydını 65.109.150.95'e çevirdi (proxy DNS-only). DNS düzelir
düzelmez Coolify Let's Encrypt sertifikasını kendisi aldı (04:03 UTC), panel açıldı.
Mert tarafında tarayıcı hâlâ döngü gösterdi — macOS DNS flush
(`dscacheutil -flushcache` + `killall -HUP mDNSResponder`) çözdü.

⚠️ **Dersler:**
- *"Too many redirects" görüldüğünde ilk ölçüm SSL modu değil, DNS'in doğru makineye
  bakıp bakmadığıdır.* Proxy açıkken `dig` origin'i göstermez — proxy kapatılmadan ya
  da CF DNS panelinden bakılmadan kayıt doğrulanamaz.
- Cloudflare proxy'si (turuncu bulut) tekrar açılacaksa **önce SSL modu "Full
  (strict)"** yapılır — origin'de artık geçerli LE sertifikası var; Flexible'da
  Coolify'ın "Redirect HTTP to HTTPS" ayarıyla döngü geri gelir.
- Sunucu tarafı düzeldikten sonra istemcide arıza sürerse tarayıcı 301 önbelleği ve
  OS DNS önbelleği şüphelidir — gizli pencere ilk test.

**Durum notu:** `tools.pryazilim.com` = Coolify panelinin kendi adresi (instance URL).
178.105.134.101'in hangi makine olduğu sorulmadı/netleşmedi — Cloud projelerinden biri.

### Açık karar — Mert'in

**Sorgu kaydının saklama süresi** (24 saat / 7 / 30 / 90 gün). Kurulumun içine yazılıyor;
sonradan "şu tarihten öncesini sil" demek birikmiş veriyi geri almaz. İki karar daha
aynı yerde bekliyor: **ekip bilecek mi** (bildirilmeden tutulan kayıt hem KVKK tarafında
sorunlu hem de öğrenildiğinde asıl zararı güven tarafında verir) ve **kim okuyabilecek**.
