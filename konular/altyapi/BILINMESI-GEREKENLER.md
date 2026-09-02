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
