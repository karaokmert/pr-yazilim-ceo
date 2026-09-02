# PR Yazılım Altyapı — Adım Adım Transcript

> Web arayüzündeki Claude oturumunun kronolojik özeti. Her adım: ne yapıldı, hangi
> komut/aksiyon, sonuç. Claude Code bu dosyayı okuyup nerede kalındığını anlayabilir.

---

## FAZ 0 — Planlama ve karar

1. **İhtiyaç:** Ekibin (6-15 kişi) sabit IP'den internete çıkması + iç servislere/MSSQL'e
   güvenli erişim. Çözüm: WireGuard VPN.
2. **VPN teknolojisi kararı:** WireGuard (wg-easy paneliyle). OpenVPN/Tailscale/Headscale
   tartışıldı; wg-easy seçildi (ücretsiz, açık kaynak, GPL).
3. **full vs split tunnel:** Tartışıldı, kesin karar YOK (bkz SETUP.md §7).
4. **Mimari:** İki katman — EX44 dedicated (araçlar) + cloud (MSSQL, projeler, VPN
   başta EX44'te). Cloud private network / vSwitch tartışıldı; basit tutuldu: "VPN kur,
   servisleri VPN arkasına al."

## FAZ 1 — chatwoot-pr (mevcut makine, referans)

5. chatwoot-pr Coolify paneline IP:8000 ile erişim. Şifre sıfırlama denendi:
   `docker exec -ti coolify sh -c "php artisan root:reset-password"` → "no space left on
   device" hatası.
6. Teşhis: `/run` (tmpfs, 382MB) DOLU — `/run/containerd` 381MB. `df -h` → asıl disk %52.
7. Çözüm: `reboot` (tmpfs RAM'de, reboot temizler). Sonra şifre sıfırlama çalıştı.
8. Cloudflare'e tools.pryazilim.com eklendi (proxy önce kapalı → SSL alındı → sonra açıldı).
   SSL/TLS mode = Full (strict) olmalı (redirect loop önlemi).
9. IP:8000 erişimini kapatma tartışıldı: ufw inactive çıktı. Portlar: 22,80,443,8080,8000
   açık (docker-proxy). Hetzner Cloud Firewall önerildi ama chatwoot-pr'de bırakıldı.

## FAZ 2 — Envanter / maliyet

10. Temmuz 2026 faturası incelendi (~378€/ay). Windows Server lisansı (27.90€) + Plesk
    (13.30€) sorgulandı → kesin durum netleşmedi, kontrol edilecek (SETUP.md §3).
11. Hetzner activity log (CSV) incelendi: 20 Haziran'da AX41-NVMe #2995756 iptal edilmiş.
    Hesapta 2FA aktif (iyi).
12. MSSQL keşfi: bir K8s sunucusunda (`ubuntu-16gb-hel1-4`) prod-secrets içinde
    `Server=tcp:a101egeli-sql-server.database.windows.net,1433` → Azure SQL olduğu anlaşıldı.
    Kendi MSSQL'i ayrı ("DB Server" CX43 cloud). K8s sunucusu rebuild edilecekti (ayrı iş).

## FAZ 3 — EX44 kurulumu (ANA İŞ)

13. EX44 auction makinesi, Rescue System'de açıldı. `installimage` başlatıldı, Ubuntu
    24.04 seçildi, config editörü açıldı.
14. **Disk sağlık kontrolü** (kurulumdan önce, kritik ders):
    ```
    smartctl -a /dev/nvme0n1 | grep -iE 'health|percentage|power on|integrity|error'
    smartctl -a /dev/nvme1n1 | grep -iE 'health|percentage|power on|integrity|error'
    ```
    Sonuç: nvme1n1 SMART **FAILED**, %102 used. nvme0n1 254 integrity error. → ARIZALI.
15. Hetzner'a mail: SMART verisiyle disk değişimi talebi. Hetzner "quick test OK" demişti
    ama SMART FAILED gösteriyordu — bu çelişki vurgulandı. Hetzner ikisini de değiştirdi.
16. Yeni diskler SMART kontrolü: ikisi de PASSED / %0 / 0 hata / 0 saat. TEMİZ.
17. `installimage` tekrar: Ubuntu 24.04, SWRAID 1, SWRAIDLEVEL 1, HOSTNAME pr-tools.
    PART: /boot/efi esp 256M, swap 8G (AMA 82G oldu — düzenleme hatası, bırakıldı),
    /boot ext3 1024M, / ext4 all. Kaydet (F2), çık (F10), Yes onay.
18. Kurulum tamamlandı → `reboot`. Host key değişti (yeniden kurulum): `ssh-keygen -R 65.109.150.95`
19. Doğrulama:
    ```
    cat /proc/mdstat        # md0/md1/md2 hepsi [UU]
    df -h /                 # /dev/md2 387G %1
    swapon --show           # md0 81.9G (82GB swap - bırakıldı)
    cat /etc/os-release     # 24.04.4 LTS Noble
    hostnamectl             # pr-tools
    ```
20. `apt update && apt upgrade -y` → kernel 6.8.0-138'e güncellendi → `reboot` (host key
    DEĞİŞMEZ bu sefer, sadece reboot).
21. Reboot sonrası: `uname -r` → 6.8.0-138-generic ✓. RAID md2 resync devam ediyordu
    (arka planda, sorun değil).

## FAZ 4 — Coolify

22. Coolify kuruldu:
    ```
    curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
    ```
    v4.3.11. Panel: http://65.109.150.95:8000
23. `.env` yedekleme uyarısı verildi: `/data/coolify/source/.env` → 1Password'e (YAPILACAK).
24. Panele girildi, admin hesabı oluşturuldu. Setup wizard: "This machine" (localhost)
    seçildi → Docker Engine OK → "My first project" oluştu → Setup complete.

## FAZ 5 — wg-easy (YARIM KALDI, ŞU AN BURADAYIZ)

25. Coolify'da "VPN" projesi → "production" env → wg-easy servisi eklendi
    (ghcr.io/wg-easy/wg-easy:latest). **Status: Exited** (henüz çalışmıyor).
26. SIRADAKİ: "Edit Compose file" → SETUP.md §6'daki kritik ayarları doğrula → deploy →
    client ekle → test.

---

## KRİTİK DERSLER
- Kurulumdan önce `smartctl` ile disk sağlığı kontrol et (auction makinelerinde şart).
- Hetzner "quick test" SMART FAILED diski kaçırabilir — kendi verini göster.
- installimage'da PART değerlerini kaydetmeden iki kez kontrol et (82GB swap dersi).
- Reboot host key: yeniden kurulumda değişir (ssh-keygen -R gerekir), sadece reboot'ta değişmez.
- wg-easy bağlanamama = %99 UDP 51820 kapalı.
- Coolify + WireGuard: cap_add NET_ADMIN/SYS_MODULE + sysctls şart.
