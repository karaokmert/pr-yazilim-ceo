---
name: project-durum
description: Açık işlerin adresi — açılışta OKUNMAZ; yalnız Mert 'eski işin devamı' derse ya da bir konu sorulursa bakılır
metadata:
  type: project
---

⚠️ **Bu dosya açılışta okunmaz.** Açılış `AskUserQuestion` ile başlar; burası
yalnız Mert *"eski işin devamı"* dediğinde ya da bir konu sorulduğunda açılır.
→ `kararlar/2026-08-26-acilis-sirasi-soruyla-baslar.md`

**Son iş: tools.pryazilim.com redirect arızası çözüldü (EV, 2026-09-04 sabah).**
Kapanış: `gunluk/ev/2026-09-04-kapanis-coolify-dns.md`
Coolify paneli artık `https://tools.pryazilim.com` üzerinden erişilebilir —
**SSH'sız yönetim yolu açıldı.** Mert: "VPN konusuna devam edeceğiz."

## AÇIK — devam eden

**VPN / AdGuard turu (altyapı).** Sıradaki: sunucu durumu ölçümü (wg-easy ayakta mı ·
53 portu boşta mı · client'lara hangi DNS dağıtılıyor) → AdGuard compose.
Artık Coolify paneli açık olduğundan SSH açılmasa da panel üzerinden ilerlenebilir.
Mert'in 4 açık kararı duruyor: EX44 SSH erişimi (1Password'da EX44 anahtarı yok,
agent bazen tümden boş = 1Password kilitli) · log saklama süresi · ekip bilecek mi ·
kim okuyacak. → `konular/altyapi/BILINMESI-GEREKENLER.md`

**Dünden (2026-09-03) bilinçli açılmayanlar:** sprint takip sistemi · proje
ekonomisi aracı · PA-üstü rol saha sınaması · fabrika eleştiri turu
(`fabrika-v2/docs/oy-9/00-ELESTIRILER.md` FPA'da işlenmedi) · MEMORY.md'ye ölüm
koşulu temizliği.

## BİLMEDEN İŞE BAŞLAMA

**1. Clara 2026-08-23'te sıfırdan kuruldu.** Omurga üç skill, hook açtırıyor,
preload yok.

**2. Yetki devri:** sınır yok, tek onay kapısı Mert. `Agent` ile iş verilmez,
`SendMessage` ile iletilir; bilgi çıkarma için `Agent` serbest (2026-09-02).

**3. Fabrika `fabrika-v2`:** FPA / FPD / FQA.

**4. Qdrant KAPALI.** `grep -l` değil satır göster.

**5. EX44 `pr-tools`:** 65.109.150.95 (Hetzner dedicated, Helsinki). Coolify v4,
wg-easy v15, panel `tools.pryazilim.com`. 178.105.134.101 = Hetzner Cloud'da başka
makine (kimliği netleşmedi).
