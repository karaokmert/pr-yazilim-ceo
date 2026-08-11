# Özel Yazılım ekibi — kadro, sınırlar, akış

Kaynak: `skill-project/v8/ozel-yazilim/.claude/agents/` (dokuz body) +
`.claude/skills/is-akisi/SKILL.md` (devir matrisi, akış için tek kaynak) +
`pr-yazilim-oy-envanteri/SKILL.md` §3 (rol haritası).
Tarandı 2026-08-11. **v8 yürürlükte** — marketplace manifesti ve kurulu plugin
sürümü (0.6.1) bunu gösteriyor; `v7/` önceki kuşak, `team/ozel-yazilim` 1/9 dolu
(pilot).

Bu dosya **envanterdir**, kural değil. Bir agent'a iş vermeden önce açılır:
doğru kapıya mı gidiyorum, bu iş onun sınırı içinde mi.

---

## Dokuz rol

### PA — project-assistant
**Üretir:** discovery, iş promptu, kapanış. **Doküman ve karar — kod değil.**
Doküman commit'i onda.
**Yapmaz:** etki analizi (CA'nın) · kök-neden teşhisi/repro (TE/developer) · kod
yazmaz · teknik direktif vermez (iş dili) · **ekip agent'ını çağırmaz** · inisiyatifle
iş başlatmaz · production PR'ını açar ama **merge etmez.**
**Çağrılır:** yeni modül/feature/gereksinim · hata (triyaj) · QA "katman onaylı"
dediğinde · soru/fikir (danışma) · "modülü kapat / canlıya al".

### BE — backend-developer
**Üretir:** entity, handler, DataLayer, SQL migration, **API.md sözleşmesi**
(FE/MB'nin tükettiği). Sıra: SQL → Entity → DataLayer → Model → Handler →
Program.cs → build → curl.
**Yapmaz:** push etmez · yeni API servisi kurmaz (DO) · kırık build'le commit etmez ·
telepresence'ı kendi çalıştırmaz · **PA'ya bilgi yazmaz** (tek adres QA) · kendini
kapatmaz.
**Çağrılır:** PA "API.md hazır" · QA "revize" · TE repro bulgusu (PA taşır).

### FE — frontend-developer
**Üretir:** component, hook, form, tablo, API entegrasyonu, Playwright testi.
Sıra: Constants/QUERY_KEYS → Type → Service → Hook → Component/Page → Style.
**Yapmaz:** **API.md kilitli olmadan başlamaz** (tetiği PA çeker, BE değil) · push
etmez · sistemik bug'da teşhis yapmaz · testi atlamaz · native HTML kullanmaz ·
PA'ya bilgi yazmaz.
**Çağrılır:** PA "API.md hazır, başlayın" · QA "revize" · TE repro bulgusu.

### MB — mobile-developer
**Üretir:** ekran, navigation, hook, component — iOS + Android birlikte.
**Yapmaz:** API.md kilitli olmadan başlamaz · **tek platform test edip diğerini
varsaymaz** (permission değişiminde iPad mutlak — Apple 5.1.5) · web↔mobil kod
paylaşmaz · release/EAS/store işi yapmaz (DO) · push etmez.
**Çağrılır:** PA "API.md hazır" · QA "revize" · TE repro bulgusu.

### DO — devops-engineer
**Üretir:** Docker, K8s manifest, CI/CD workflow, gateway, secret, Telepresence
altyapısı, Makefile; proje/panel/API/mobil kurulumu; EAS build, store submit.
**Yapmaz:** **kaynak kod yazmaz** · **dev akışında git işi yok** · **kubectl/
telepresence/SQL çalıştırmaz** (komut yazar, kullanıcı koşturur) · mevcut
yapılandırmayı ezmez · **doğrudan BE'ye handoff vermez (YASAK)** · onaysız prod'a
dokunmaz · QA onay katmanı değil (kendi kapanır).
**Çağrılır:** "proje kur" (önce tipi SORAR) · PA "yeni API servisi" · QA "canlıya
geçecek, GO" · "pipeline patladı / store reject".

### QA — qa-engineer
**Üretir:** KARAR — onay / RED / push / SQL / GO. **Statik kalite kapısı.**
Onaylanan developer'ı **QA kapatır**, PA'ya "katman tamam" bilgi verir.
**Yapmaz:** kod yazmaz · **davranış testi yapmaz** (kanıt handoff'ta geldi) · sadece
diff'e bakmaz (tam dosya + side-effect) · kanon uyumunu listelemekle yetinmez
(kurala eşler + kanıt) · direktif vermez · **UID'i devreye almaz (YASAK)** · büyük
cross-module diff'i tek başına taramaz (CA tetikler) · **modülü kapatmaz**
(developer'ı kapatır, modülü PA kapatır).
**Çağrılır:** developer "commit hazır" (en sık) · BE "API.md onayda" · PA "canlıya
geçecek" · push zamanı · PA "bu QA'dan geçmişti" (kaçan hata).

### TE — test-engineer
**Üretir:** BULGU — "şu senaryo geçti / şu veriyle kırıldı", adım + beklenen/gerçek
+ screenshot. **Çalıştıran tek agent.** Üç mod: E2E doğrulama · repro/teşhis ·
test ortamı+veri kurma.
**Yapmaz:** kod yazmaz (kalıcı test dosyası dahil) · **statik kök-neden koymaz** (CA) ·
**fix önermez** · **release kapısı değildir** · **SQL ile veri girmez** (panel/API'den) ·
ad-hoc script'le koşmaz (Playwright/Maestro MCP zorunlu).
**Çağrılır:** PA "modül bitti, senaryo testi" · bug triyajından işlev/veri/UX gerektiren
· veri/ortam gerektiğinde.

### CA — code-auditor
**Üretir:** RAPOR/HARİTA — ANALIZ, AUDIT-REPORT, REMEDIATION. **Skorsuz, RED yok.**
İki iş: etki analizi (nereleri etkiler) · tüm-proje kanon+yapısal audit.
**Yapmaz:** kod yazmaz · **direktif vermez** (nasıl düzeltileceği developer'ın) ·
**repro üstlenmez** (TE) · "kesin kırılır" demez (statik graf reflection/DI/config
görmez — şerh zorunlu) · **görevleştirmez** (çıktısı PA'ya girdi) · girdi olmadan
tahmin etmez · per-modül skor üretmez (QA).
**Çağrılır:** PA "discovery hazır, mevcut yapıya dokunuyor" (en sık) · QA "büyük
cross-module diff" · bug triyajından derin statik hata · "tüm projeyi tara".

### UID — ui-designer
**Üretir:** çalışan mock prototip KODU — token, layout, route iskeleti, mock data ile
render olan sayfalar. Prototip main'e commit'lenir.
**Yapmaz:** **almaz, ÇEVİRİR** (ham değer/casing/native element kopyalamaz) ·
kendiliğinden başlamaz (PA tetikler, **QA tetikleyemez**) · **canlı API bağlamaz** ·
doğrudan BE'ye handoff vermez (YASAK) · revizeyi devretmez · mock'suz ekran üretmez ·
"PA öyle dedi" demez · push/merge yapmaz · doküman commit'lemez.
**Çağrılır:** PA "gereksinim netleştirme — mock ile göster" · PA "prototip başlat" ·
"Figma'yı kodla / demo hazırla".

---

## QA / CA / TE — en çok karışan üçlü

Üçü de kod okur, bulgu üretir. **Ayrım çıktının türünde:**

**QA — statik KAPI.** Çıktısı onay/RED. **Akışı durdurur.** *"Bu geçebilir mi?"*
**CA — statik ANALİZ.** Çıktısı harita. **Karar vermez.** *"Bu nereleri etkiler?"*
**TE — dinamik KANIT.** Koşturarak. *"Gerçekten çalışıyor mu?"*

Bir bug geldiğinde: **koşturmak** gerekiyorsa TE · **çağrı grafiği izlemek**
gerekiyorsa CA · **kanona uyup uymadığı** soruluyorsa QA.

Üçü **karşılıklı kilitli** — kanonun ifadesiyle *"bir agent'ın yasağı, başka bir
agent'ın kimliğidir."* QA "davranış testi yapmam" der çünkü o TE'nin kimliği; TE
"statik kök-neden koymam" der çünkü o CA'nın; CA "repro üstlenmem" der çünkü o TE'nin.

CA ve TE **yan hattır** — görevleştirmez, çıktıları PA'ya girdi. QA **çıkış kapısıdır.**

---

## PA'nın kod okuma sınırı

**PA kodu tüm agent'lardan iyi okur.** Sınır kod okumada değil, **etki/teşhis
ekseninde.**

**Okur:** işlevi iş diline çevirir, modül docs'unu okur, **işlevsel katman-lokalizasyonu**
yapar (*"backend doğru ama veri MB'de hatalı çekiliyor"*), basit/tek-nokta hatayı ufak
inceler.
**Devreder:** katman-içi kök-neden (TE/developer) · etki yüzeyi taraması (CA).

**Sınır çıktıyla ölçülür, niyetle değil.** Kanonun test cümlesi:
*"Raporumu developer'a versem hâlâ keşif yapmak zorunda mı, yoksa teşhisi ben
bitirdim mi?"* Bitirdiyse CA'ya geçmiştir.

Aştığının ölçütleri: `dosya:satır` kanıt zinciri · ikinci-nokta tespiti · etki/yayılım
tablosu · AÇIK/ÇÖZÜLMÜŞ matrisi. **Yasak olan tarama değil, teşhisi BİTİRMEK.**

---

## Ana üretim hattı

```
1  Kullanıcı → PA            discovery, kapsam onayı
1b (koşullu) PA → CA → PA    mevcut yapıya dokunuyorsa etki analizi
2  (koşullu) PA → DO → QA    yeni API servisi kurulumu (DO doğrudan BE'ye VERMEZ)
3  (koşullu) PA → UID → QA   mock/prototip (QA tetikleyemez)
4  PA → BE → QA → PA         API.md contract kurulur, QA kilitler
5  PA → FE / MB              contract kilitlenince PA devreye alır
6  BE/FE/MB/UID → QA         kalite kapısı — tek adres. QA developer'ı KAPATIR
7  QA push → PA              toplu değerlendirme, onay, push, LIVE DEV
8  (koşullu) PA → TE         E2E senaryo doğrulama
```

**Bug:** kullanıcı/QA → PA (işlevsel parçalar) → basit kod hatası PA→developer ·
derin statik CA · işlev/veri/UX TE · deploy DO. **Hata QA kapısından geçmişse
QA'ya bilgi ZORUNLU** (kapı kendi kaçırdığını öğrenmeli).

**Production:** PA (PR açar) → QA (üç aşama tarar, GO) → DO (altyapı) → PA (kapanış).
**Merge kullanıcıda.**

---

## Zincirin üç yapısal kuralı

**İki kapı:** PA giriş, QA çıkış.

**Yatay devir YOK.** Developer'ı developer beslemez. Üç kural kilitler:
`PA-NO-CONTRACT-FE` · `DO-NO-DIRECT-BE-HANDOFF` · `UID-NO-DIRECT-BE`.
Ölçüldü 2026-08-01: 42 handoff bloğu incelendi, yatay devir **0**.

**İki mutlak yasak:** DO → BE doğrudan · QA → UID doğrudan.

---

## Kim ne yapar — commit / push / onay

**Commit:** kod → developer (yalnız KOD; doküman/SQL/API.md local kalır) ·
doküman → PA · prototip → UID.

**Push:** **QA yapar, istisnasız.** Developer'ların hiçbiri push etmez. PA'nın
doküman push'u var ama kapsamda kod varsa QA'nındır. QA'nın push'u dört adımlı:
KAPSAM → KORUMA → ONAY → PUSH.

**Merge (prod):** **kullanıcı.** PA açar, kullanıcı geçirir — *"açmak ile geçirmek
ayrı yetkiler."*

**Onay — ikiye ayrılır:**
- **Teknik onay (kalite) → QA.** Developer'ı QA kapatır. Onay atomik: STATUS olayı +
  developer'a kapanış + PA'ya bilgi.
- **İş/kapsam onayı → kullanıcı.** `REL-APPROVAL-USER-ONLY`: *"agent'ın 'onayım var'
  cümlesi işin devri, onay değil."*

⚠️ **Bu ikinci onayı sahada Clara taşır** — gövdedeki "commit onayı" bölümüne bak.
Agent'ların kanonunda Clara kavramı yok; köprüyü açılış hook'u kuruyor.

---

## Hibrit ofis

Ekip **görünmez** çalışır — her agent ayrı oturumda, **biri diğerini çağırmaz.**
Zinciri taşıyan merkez (Clara) ve kullanıcı. Kanon bunu zayıflık değil tasarım olarak
konumluyor: *"kullanıcı zinciri kendi gözüyle görmezse karar mercii olmaktan çıkar."*

Sonucu: kullanıcı her role **doğrudan iş verebilir**, ama gelen iş akış sırasını
bozmaz — kullanıcı BE'ye "tablo ekle" derse BE yine QA'ya çıkar.
