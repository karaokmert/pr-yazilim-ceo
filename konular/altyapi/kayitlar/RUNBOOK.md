# PR Yazılım — Altyapı Kurulum Runbook

> Bu dosya, bir Claude (web arayüzü) oturumunda planlanan ve kısmen uygulanan altyapı
> kurulumunun kaydıdır. Amaç: Claude Code'un bu bağlamı okuyup kaldığı yerden devam
> edebilmesi. Aşağıdaki "DURUM" ve "SIRADAKİ ADIMLAR" bölümleri en kritik kısımlardır.

**Son güncelleme:** 2026-08-26
**Ortam:** Hetzner (dedicated + cloud karışık), yönetim Coolify + web arayüzü

---

## 1. GENEL MİMARİ (kararlaştırıldı)

İki katmanlı yapı:

- **Dedicated katman — EX44 (`pr-tools`)**: Güç isteyen, sürekli çalışan self-hosted
  araçlar. Coolify ile yönetiliyor. Üzerinde çalışacaklar: n8n, Qdrant, wg-easy (WireGuard),
  ve zamanla eklenecek başka araçlar. Bu makine "self-hosted tool sunucusu" kimliğinde.
- **Cloud katman**: Kritik ve esneklik isteyen her şey. MSSQL (kendi DB sunucusu, cloud'da
  "DB Server" projesi), proje sunucuları. Bunlar kademeli olarak VPN arkasına alınacak.

**Yaklaşım:** VPN kur → cloud servislerini kademeli VPN arkasına al → oraya sadece VPN ile
gir. "Bir günde tüm sunucuları VPN'e kapatma" — kademeli geçiş, her adımı test ederek.

---

## 2. SUNUCU ENVANTERİ

### EX44 — `pr-tools` (ANA TOOL SUNUCUSU, üzerinde çalışıyoruz)
- **IP:** 65.109.150.95  | IPv6: 2a01:4f9:3100:4bd9::2
- **Donanım:** i5-13500 (14 çekirdek / 20 thread), 64GB RAM (non-ECC), 2× 512GB NVMe (Gen4)
- **Lokasyon:** Helsinki (hel1)
- **OS:** Ubuntu 24.04.4 LTS (Noble), kernel 6.8.0-138-generic
- **RAID:** SWRAID1 (md0=swap, md1=/boot, md2=root ~412GB). Kurulumda `[UU]` sağlıklı.
- **Swap:** 82GB (yanlışlıkla; 8GB planlanmıştı ama "365GB boş var, bırak" kararıyla kaldı)
- **Coolify:** v4.3.11 kurulu, panel http://65.109.150.95:8000 (henüz domain/SSL yok)
- **DİKKAT:** Diskler auction'dan geldiğinde ARIZALIYDI (biri SMART FAILED %102, biri 254
  integrity error). Hetzner ikisini de ÜCRETSİZ değiştirdi. Yeni diskler: seri
  S63CNX0Y719216 + S63CNX0Y719217, ikisi de SMART PASSED / %0 / 0 hata. Ders: kurulumdan
  önce `smartctl -a` ile disk sağlığı kontrol edilmeli.

### chatwoot-pr (MEVCUT, ayrı makine — dokunulmuyor)
- Chatwoot + Coolify çalışıyor. ~4GB RAM, dar. Bir kez /run (tmpfs, containerd) dolup
  Coolify erişilemez olmuştu; reboot ile çözüldü. Panel domain: tools.pryazilim.com
  DEĞİL — o EX44 için planlanıyor. chatwoot-pr'de Coolify paneli 8000'de.
- Cloudflare proxy + Let's Encrypt SSL kuruldu (bu makine için ayrı hikaye).

### MSSQL — cloud'da "DB Server" projesi (CX43)
- Korunacak kendi MSSQL sunucusu. Şu an public erişilebilir (güvenlik riski).
- Plan: VPN peer yap, public 1433'ü kapat, sadece VPN'den eriş.
- OS'i (Windows mu Linux mu) NETLEŞMEDİ — WireGuard peer kurulumu buna bağlı.

### Azure SQL (`*.database.windows.net`, örn. a101egeli-sql-server)
- Ayrı, taşınmıyor. URL ile erişilmeye devam edecek.
- YAPILACAK: Azure Portal → SQL → Networking → firewall kuralı ile SADECE proje
  sunucularının çıkış IP'lerine izin ver (şu an geniş açık olabilir).

---

## 3. FATURA / MALİYET NOTLARI (Temmuz 2026 faturası, ~378€/ay)

- Windows Server 2022 lisansı (27.90€/ay) — muhtemelen 20 Haziran'da iptal edilen
  AX41-NVMe #2995756'ya bağlıydı. Hâlâ faturalanıp faturalanmadığı NETLEŞMEDİ.
  YAPILACAK: Ağustos faturasında var mı bak / Hetzner'a sor, boşa ödeme varsa iptal.
- Plesk Web PRO (13.30€/ay) — kullanılıyor mu belirsiz, kontrol edilecek.
- Çok sayıda küçük cloud sunucu (balkanbee, deliverigo, egeli-a101, kargom, liston,
  osinif, paygo-servers, template-project) — konsolidasyon fırsatı olabilir.
- UYARI: 15 Haziran 2026 sonrası cloud fiyat zammı. Mevcut instance'lar rescale
  EDİLENE KADAR eski (ucuz) fiyatta. Gereksiz rescale'den kaçın.

---

## 4. DURUM — NEREDE KALDIK

### TAMAMLANAN
- [x] EX44 diskleri değiştirildi, SMART temiz doğrulandı
- [x] installimage → Ubuntu 24.04 + RAID1 kurulumu
- [x] Reboot, yeni kernel (6.8.0-138) aktif, RAID [UU]
- [x] `apt update && apt upgrade -y` yapıldı
- [x] Coolify v4.3.11 kuruldu, admin hesabı oluşturuldu, localhost server bağlandı
- [x] Coolify'da "VPN" projesi + "production" env + wg-easy servisi EKLENDİ
      (ghcr.io/wg-easy/wg-easy:latest) — ama STATUS: EXITED (henüz düzgün çalışmıyor)

### ŞU AN BURADAYIZ (yarım kalan iş)
wg-easy servisi Coolify'a eklendi ama **Exited** durumda. Deploy etmeden önce Compose
dosyası kontrol edilecek. "Edit Compose file" ile açılıp şunlar doğrulanacak (aşağıdaki
KRİTİK AYARLAR bölümü).

---

## 5. SIRADAKİ ADIMLAR (öncelik sırasıyla)

### A. wg-easy'yi düzgün çalıştır (ŞU AN)
1. Coolify → VPN projesi → wireguard-easy servisi → "Edit Compose file"
2. Compose'da şu KRİTİK AYARLARI doğrula/ekle (aşağıya bak)
3. Deploy et, Status "Running" olmalı
4. Web panel: bir client ekle, QR ile kendi cihazına bağlan, TEST et
5. `WG_HOST=65.109.150.95` istemcilerin bağlanacağı adres

### B. Güvenlik sıkılaştırma (VPN çalışınca — ŞU AN ERTELENDİ, RİSK AÇIK)
> DİKKAT: Sunucu şu an root+parola ile dünyaya açık, firewall/SSH-key YOK. Bu köprü
> kısa tutulmalı. Kullanıcı bilerek "önce VPN'i göreyim" dedi.
1. 1Password ile SSH key oluştur → public key'i EX44'e koy → agent aktifleştir → TEST
   - PC uçsa bile key 1Password bulutunda korunur. 1Password hesabı 2FA + Secret Key/
     Emergency Kit güvenli saklanmalı. Ayrıca bağımsız bir yedek key de tut.
2. SSH parola girişini KAPAT (önce key ile girişi test et, sonra kapat — kilitlenme!)
3. fail2ban kur (SSH brute-force için)
4. unattended-upgrades (otomatik güvenlik yamaları)
5. Firewall — EX44 DEDICATED, Hetzner Cloud Firewall YOK. Sunucu içi çözüm gerekir ve
   Coolify/Docker iptables ile ÇAKIŞMAMALI (normal ufw Docker'la sorun çıkarır).
   Plan: firewall'dan 22'yi kaldır, WireGuard UDP 51820 aç → erişim = SSH key + aktif VPN.
   n8n/Qdrant panellerini SADECE VPN içinden erişilir yap (dışarı açma).

### C. Araçları kur
- n8n (Coolify service şablonu) — panel VPN-only
- Qdrant (Coolify service şablonu) — RAM sever, EX44'te bol

### D. Coolify paneli domain + SSL (opsiyonel)
- chatwoot'taki gibi: Cloudflare (proxy aç, SSL/TLS = Full strict), Let's Encrypt.
- En güvenlisi: paneli domain'de bile bırakmayıp SADECE VPN'den erişilir yapmak.

### E. MSSQL'i VPN arkasına al (kademeli)
1. MSSQL cloud sunucusuna WireGuard peer kur (OS'e göre — Windows/Linux netleşecek)
2. VPN'den SSMS ile MSSQL'e eriş, TEST et
3. Bir proje sunucusunu peer yap, connection string'i VPN IP'sine çevir, TEST
4. Hepsi çalışınca MSSQL public 1433'ü KAPAT
5. Kalan projeleri tek tek geçir

### F. Azure SQL firewall (VPN'den bağımsız, ne zaman olsa olur)
- Azure Portal → SQL Server → Networking → sadece proje sunucu IP'lerine izin

---

## 6. wg-easy İÇİN KRİTİK COMPOSE AYARLARI

Coolify'ın varsayılan şablonu bunları eksik/yanlış getirebilir. Deploy öncesi doğrula:

```yaml
services:
  wg-easy:
    image: 'ghcr.io/wg-easy/wg-easy:latest'
    environment:
      - SERVICE_FQDN_WIREGUARDEASY_8000   # Coolify domain bağlama (web UI)
      - WG_HOST=65.109.150.95             # KRİTİK: sunucu public IP'si
      - 'LANG=${LANG:-en}'
      - PORT=8000                          # Web GUI portu (domain portuyla aynı olmalı)
      - WG_PORT=51820                      # VPN server portu
      # - PASSWORD_HASH='...'             # bcrypt hash TEK TIRNAK içinde (Coolify #3946:
      #                                      $ karakterleri sorun; gerekirse $ -> $$)
    volumes:
      - 'wg-easy:/etc/wireguard'           # KRİTİK: bu volume'u yedekle! Kaybolursa
      #                                      tüm peer configleri ölür.
    ports:
      - '51820:51820/udp'                  # KRİTİK: VPN portu. Açık değilse panel açılır
      #                                      ama HİÇBİR CLIENT BAĞLANAMAZ (en sık hata).
    cap_add:
      - NET_ADMIN
      - SYS_MODULE                         # WireGuard kernel modülü erişimi
    sysctls:
      - net.ipv4.conf.all.src_valid_mark=1
      - net.ipv4.ip_forward=1              # paket yönlendirme
    restart: unless-stopped
```

**Bağlanamama = %99 port sorunu:** UDP 51820 dışarı açık mı? (Şu an firewall yok ama
Docker port mapping doğru olmalı.)

**Yedek:** `/etc/wireguard` volume + `WG_HOST` değeri yedeklenmeli. Ayrıca Coolify'ın
`.env` dosyası: `/data/coolify/source/.env` → 1Password'e yedekle (kurulum scripti uyardı).

---

## 7. AÇIK KARARLAR (henüz netleşmedi)

- **full-tunnel mu split-tunnel mı?** Ekip trafiği için. Kullanıcı önce "bilmiyorum"
  dedi, sonra split-tunnel bakım yükü endişesiyle full-tunnel'a meyletti, ama KESİN
  KARAR YOK. (Amaç: ekip sabit IP'den çıksın + iç servislere erişim.)
  - full-tunnel: tüm trafik EX44'ten. Basit ama gecikme (TR→Helsinki ~50-65ms), tek
    hata noktası, kişisel trafik de geçer (KVKK/gizlilik → ekibe bildir, log tutma).
  - split-tunnel: sadece iş servisleri tünelden. Bakım biraz daha fazla.
- **EX44'e VPN'den erişim yöntemi**: peer olarak mı, panelleri VPN-only mi? (B5'e bağlı)
- **VPN yeri**: Kullanıcı "EX44'e kur, para harcamayayım" dedi. Güvenlik açısından ayrı
  cloud sunucu önerildi ama reddedildi. → EX44'te. İzolasyonu kurulumla sağlayacağız.

---

## 8. GÜVENLİK FELSEFESİ (kararlaştırılan)

- Katmanlı savunma: (1) Hetzner Cloud Firewall port seviyesi [SADECE cloud sunucularda],
  (2) Cloudflare turuncu bulut = WAF/DDoS/IP gizleme [domain trafiği], (3) fail2ban +
  güçlü kimlik + panelleri VPN arkası [uygulama seviyesi].
- EX44 dedicated olduğu için Cloud Firewall YOK — sunucu içi + VPN-only erişim.
- Cloudflare'i zorunlu geçiş yapmak için: 80/443'ü sadece Cloudflare IP aralıklarına aç.
- MSSQL: internetten görünmez olmalı, sadece VPN/private network içinden.
- Log tutma (özellikle full-tunnel'da kişisel trafik) — KVKK + güven.

## 9. DEDICATED RİSK / FELAKET SENARYOSU
- Dedicated'da donanım arızası SENİN krizin (cloud'da Hetzner otomatik taşır).
- RAID1 disk arızasını çözer, MAKİNE arızasını çözmez.
- Çözüm üçlüsü: kritik veriyi burada tutma (zaten cloud'da) + RAID1 + DIŞ yedek.
- EX44'teki araçlar "yeniden kurulabilir" → makine ölse birkaç saat kesinti, veri kaybı
  değil. Coolify config + volume'lar düzenli yedeklenmeli (dış hedef: Storage Box / S3).
