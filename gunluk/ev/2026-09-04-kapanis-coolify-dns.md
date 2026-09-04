# Kapanış — 2026-09-04 sabah · Coolify redirect arızası (EV)

Oturum "eski işin devamı" olarak açıldı; Mert "tools serveri" dedi — VPN/altyapı
işi. SSH erişim ölçümüyle başladı, Mert yönü çevirdi: **Coolify'da problem var** —
`tools.pryazilim.com` "too many redirects" veriyordu.

## Ne bitti

**1 · Arıza teşhis edildi ve çözüldü.** Asıl sebep DNS: A kaydı EX44'ü değil
178.105.134.101'i (Hetzner Cloud, Nürnberg — kimliği bilinmiyor) gösteriyordu.
Mert proxy'yi kapattı, IP'yi 65.109.150.95'e çevirdi; Coolify LE sertifikasını
kendisi aldı; Mert tarafındaki kalıntı döngüyü macOS DNS flush çözdü. Panel açık.
Teşhis + dersler: `konular/altyapi/BILINMESI-GEREKENLER.md` (bu commit).

**2 · SSH erişimi yeniden ölçüldü — hâlâ kapalı, geri gitmiş.** 1Password agent
"no identities" veriyor (2 Eylül'de iki anahtar vardı; muhtemelen kilitliydi).
EX44 Ed25519 anahtarı sorunu 2 Eylül'den beri aynı.

## Ne yarım kaldı

**AdGuard turu başlamadı** — ama zemin değişti: Coolify paneli artık dışarıdan
açık, kurulum SSH olmadan panel üzerinden de yürüyebilir. Sıradaki üç ölçüm:
wg-easy ayakta mı · 53 portu boşta mı · client'lara hangi DNS dağıtılıyor.

## Mert'in kararını bekleyen

2 Eylül'den dört karar aynen duruyor: SSH erişimi (1Password) · log saklama
süresi · ekip bilecek mi · kim okuyacak.

## Ölçüldü ama çözülmedi

- **178.105.134.101 hangi makine** — sorulmadı, netleşmedi.
- **Cloudflare SSL modu** hâlâ ne ise o; proxy tekrar açılırsa önce Full (strict)
  yapılmalı, yoksa döngü geri gelir.

## Bir sonraki hareket

Mert'in cümlesi: "VPN konusuna devam edeceğiz." Dönüldüğünde: panel üzerinden
sunucu durumu ölçümü → AdGuard compose.
