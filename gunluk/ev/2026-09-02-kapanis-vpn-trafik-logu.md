# Kapanış — 2026-09-02 · VPN trafik logu ve AdGuard (EV)

Oturum "eski işin devamı" olarak açıldı; sunucu/VPN altyapısı seçildi. Konuşma
teşhisle başlamadı, **bir ihtiyaçla** başladı: Mert WireGuard loglarını izlemek istedi.

## Ne bitti

**1 · Kaldığımız yer ölçüldü** (commit: bu oturum)
`konular/altyapi/` commit'sizdi — 28 Ağustos'ta yazılmış ama git'e girmemişti.
Runbook 26 Ağustos tarihli ve 28'deki ilerlemeyi taşımıyor; son durum yalnız
`.remember` kaydından okunabildi: wg-easy v15 ayakta, tünel doğrulanmış, VPN client
çalışıyor (çıkış IP 65.109.150.95), SSH sertleştirme **başlamış ama bitmemiş**.

**2 · Log türü ayrıştırıldı ve karar alındı**
"WireGuard logu" iki ayrı şeydi: servis/bağlantı logu (teşhis) ve trafik logu
(kim nereye gitti). Mert **trafik logunu** seçti. Gerekçesi bir politika: şirket
bilgisayarında kişisel iş yapılmaması.

Clara üç noktadan itiraz etti (kural ile çözüm ters yöne bakıyor · VPN sürekli açık
olmadığı için log yanlış kümeyi ölçüyor · gözetim sebebi kaldırmıyor) ve alternatif
sundu: kaydetmek yerine DNS filtresiyle **engellemek**. Reddedildi, karar trafik
logu. İtiraz ve gerekçesi kanona yazıldı.

**3 · Kurulum mekaniği çıkarıldı — AdGuard Home**
Tek bileşen iki iş: sorgu kaydı + reklam engelleme. Mert'in ikinci sorusu (mobilde
uygulama reklamları engellenir mi) aynı araca çıktı — cihaza hiçbir şey kurmadan,
VPN üstünden.

Kritik olanlar: DoH engelleme + 53 portunun zorla yönlendirilmesi **kurulumun
parçası** (eksikse log "temiz" çıkar ve doğru sanılır) · AdGuard önce kurulur, wg-easy
DNS'i **sonra** çevrilir (ters sırada tüneldeki herkes internetsiz kalır) · DNS
değişince mevcut client config'leri yeniden dağıtılmalı.

Hepsi `konular/altyapi/BILINMESI-GEREKENLER.md`'ye yazıldı.

**4 · Bir hata düzeltildi**
Clara "Coolify'da AdGuard şablonu var" dedi — **ölçmedi**, hatırladığını bilgi gibi
kullandı. Mert "coolify'da yok gibi" deyince düzeltildi. Doğrusu: şablon gerekmiyor,
Docker Compose ile kurulur — ve bu daha iyi, çünkü wg-easy'nin Exited arızası tam
olarak şablondan çıkmıştı.

## Ne yarım kaldı

**Kurulumun kendisi başlamadı.** Sebep tek: **sunucuya girilemiyor.**

Ölçüldü: 1Password agent'ında iki anahtar var (`Hetzner | DEV + WEB SQL`,
`Dev Server | Hetzner Cloude`), EX44 için 28 Ağustos'ta oluşturulan Ed25519 anahtarı
**listede yok**; anahtarsız giriş `Permission denied (publickey,password)` veriyor.
28'in kaldığı yer muhtemelen tam burası — public key sunucuya yazılmış, giriş testi
tamamlanmamış.

## Mert'in kararını bekleyen

**1 · EX44 erişimi** — 1Password'da anahtarın agent'a açılması, ya da Coolify paneline
Mert'in girip kurulumun yanından yürütülmesi. Bu açılmadan hiçbir adım başlamıyor.

**2 · Sorgu kaydının saklama süresi** (24 saat / 7 / 30 / 90 gün). Kurulumun içine
yazılıyor; sonradan silmek birikmiş veriyi geri almaz.

**3 · Ekip bilecek mi** — bildirilmeden tutulan kayıt hem KVKK tarafında sorunlu hem de
öğrenildiğinde asıl zararı güven tarafında verir.

**4 · Kim okuyabilecek** — yalnız Mert mi, herhangi bir yönetici mi.

⚠️ 27 Ağustos kapanışındaki beş karar (turbo.json commit'i, symlink dönüşümü,
karaokai'deki 40 dosya, trendyol çifti, pnpm) **hâlâ açık** — bu oturumda açılmadı.

## Ölçüldü ama çözülmedi

**Sunucunun bugünkü hâli bilinmiyor.** wg-easy hâlâ ayakta mı, dört gündür ne oldu —
ölçülemedi.

**53 portu EX44'te boşta mı** — `systemd-resolved` tutuyorsa AdGuard kalkmaz ve belirti
yine "kurdum ama Exited" olur. Kurulumdan önce ölçülecek ilk şey.

**wg-easy client'lara hangi DNS'i veriyor** — değiştirilecek değerin bugünkü hâli
görülmedi.

**`konular/altyapi/` dört gün commit'siz durdu.** 28'in işi git'e hiç girmemiş; bugün
fark edildi. Bir sonraki oturum kayıt kaybı yaşayabilirdi.

## Bir sonraki hareket

EX44 erişimi açılır, sunucunun bugünkü durumu ölçülür (wg-easy ayakta mı, 53 portu boş
mu, hangi DNS dağıtılıyor), sonra AdGuard compose'u yazılır.
