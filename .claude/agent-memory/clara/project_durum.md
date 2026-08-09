---
name: durum
description: İLK BUNU OKU — son kapanış dokümanının adresi ve tek cümlelik durum. Oturum açılışında ilk okunan kayıt.
metadata:
  type: project
---

# Durum

> **`gunluk/` artık proje bazlı** (2026-08-09): `gunluk/ev/` · `gunluk/{proje}/`.
> Açılış hook'u her projenin son kapanışını ayrı listeler — **yalnız kendi modunun
> kapanışı okunur**, başka projeninki özetlenmez. Eski düz dosyalar `gunluk/ev/`e taşındı.

**Son kapanış (ev):** `gunluk/ev/2026-08-09-kapanis-2.md` (kısa oturum: pencere ölçümü)
**Ondan önceki:** `gunluk/ev/2026-08-09-kapanis.md` (aşağıdaki A/B özeti onun)

> **Push kapandı.** Aşağıdaki *"İlk hareket: PUSH"* satırı artık geçersiz — ölçüldü,
> `origin/main..HEAD` boştu. Bekleyen sıra (A bölümü) aynen duruyor.

> Aynı gün **iki ayrı oturum** çalıştı ve ikisi de bu kaydı yazdı. Aşağıda ikisi de var —
> biri fabrika/N8N hattı, diğeri Clara'nın kendi kanonu. Karışmıyorlar.

## A — Fabrika hattı (N8N oturumu)

**N8N işi KAPANDI.** Fabrikanın ilk gerçek ürünü `n8n-otomasyon` v0.1.0 push'landı
(`a948fd5`, 21 commit): 3 rol, 7 skill, 82 kural — beş kanıt katmanından geçti.
Ayrıntı: `gunluk/2026-08-09.md` → *"N8N İŞİ KAPANDI — 07:28"*

**Bekleyenler, sırayla:**

1. **OY plan kararı** — PQA denetiminden geçti, **Mert'in kalem kararı bekleniyor**
   (5 kalem + ertelenen kalem-5; `agent-project/docs/ozel-yazilim/takim-analizi/rapor-analiz-plan.md`)
2. **Kanal asseti taşıma** — PAD'de onaylı+dondurulmuş plan, tek komutla başlar
3. **Filo taraması** — ilk takım sahada, `docs/filo/durum.md` doldurulacak
4. **N8N ilk gerçek iş** — saha kanıtı; kurulum katman-2'yi ölçecek
5. **N8N erişim ucu** — Mert'ten API bilgisi gelince dal sabitlenir

## B — Clara'nın kendi kanonu (bu oturum)

**Rol tanımı düzeltildi ve sınama yöntemi kuruldu.**

**Roller artık ALTI:** proje-yonetimi · saha-monitorluk · sprint-yonetimi ·
kanal-kurulumu · agent-sinama · oturum-duzeni.
**Davranışlar rol değil:** arama-disiplini · hafiza-duzeni · onay-brief · clickup-duzeni.

**Birincil kural kondu — `CLA-FIX-THE-CAUSE`:** *bozuk olan yamayla düzeltilmez, sebebi
ortadan kaldırılır.* Kapsam **yönetilen tüm işler.** Kritik kuralların birincisi.

**Anlam sınaması kanona girdi:** ayıran test *"bu sorunun cevabı kanonda yazılı mı"* —
yazılıysa okuma sorusudur. Ve üç ek: **tek tur ölçmez (üstüne gidilir)** · **çelişki
koymadan doğrulama refleksi ölçülmez** · **itiraz sınanmadan sınama tamam değil.**

**Sahada sınandı:** yeni Clara kanaldan 19 soruyla sınandı, onbir davranış tuttu.

## İlk hareket

**PUSH** — bekleyen commit'ler var. Kontroller (hassas bilgi + uzak çakışma) yapılıp
`git push origin main`.

## Açık iki konu

**Ortak hafıza** — graph npx önbelleğinde (silinebilir), yedek `~/.pr-memory/`.
Yapılandırmaya dokunulmadı, Mert erteledi.

**Sınama skill'inin yeni sürümü sınanmadı** — üstüne gitme / çelişki / itiraz eklendi ama
gerçek bir turla ölçülmedi.

## Kalıcı dersler (bugün)

Dört sessizlik türü (`arge/agent-oturum-modu/`) · push kapsamı push anında ölçülür ·
**beyan başlama değildir** · standart devralınır · **ayarın varlığı uygulandığının kanıtı
değil** (model `fable` yazılıydı, opus koşuyordu) · kanal ayrımı **izinle değil adresle**
sağlanıyor.
