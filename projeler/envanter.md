# PR Yazılım proje envanteri

Tarih: 2026-08-03 · Ölçüm: üç paralel tarama (`ozel-yazilim/` 16 proje, `p/` altı 8 klasör)

Bu dosya **referans**, bir kerelik bulgu değil — proje durumu değiştiğinde güncellenir.
Kaynak: `docs/_project/PROJECT-INFO.md`, README, `iac/ingress*.yml`,
`.github/workflows/`, `git log -1`.

Etiketler: **[M]** müşteri projesi · **[Ü]** PR Yazılım'ın kendi ürünü ·
**[A]** altyapı/şablon · **[?]** sahibi dosyalardan çıkarılamadı

---

## Kendi ürünler

**WupDoc [Ü]** — `ozel-yazilim/wupdoc` · sağlık turizmi listeleme platformu: hasta
dünya genelindeki doktorları puan/yorum bazında sıralar, talep ve randevu oluşturur.
Dört panel (site, doktor/klinik, yönetim, partner/ajans).
18 .NET servisi + Azure Cognitive Search + 6 consumer + 6 cron · PROD, `wupdoc.com` ·
son commit 2026-07-24 (PR #1236) · **envanterin en büyük ve en olgun projesi.**
README'de açıkça *"WupDoc #Inhouse"*.
Mobil tarafı ayrı: `p/mobile-app/wupdoc-mobile`, son aktivite 2026-03-02, store'a
çıkmış (tahmin).

**BalkanBee [?]** — `ozel-yazilim/balkanbee` · Balkanlar için ikinci el pazaryeri
(ilan, satıcı, kurumsal hesap, çoklu dil). 9 .NET servisi + 3 panel + React Native
`mobile-seller` + 22 workflow · PROD + mobil store'a çıkmış · son commit 2026-07-09.
**Sahibi belirsiz ve bu bir bulgu:** `docs/` altında tek bir audit raporu var,
PROJECT-INFO/MODUL-INDEX yok, README hâlâ `dotnet-template` metni. Marka + çoklu dil
yatırımı kendi ürün olduğunu düşündürüyor **(çıkarım, ölçüm değil)**.
Not: `liston` reposunda `balkanbee-demo` adlı ikinci bir remote var.

**`web-sitesi` altındaki kendi işler [Ü]** — `PR-redesign`, `pryazilim-crm`,
`pryazilim-crm-2`, `prproject-managment`, `prvm-web`. İkisi CRM denemesi (iki ayrı
sürüm), biri kurumsal site yenilemesi.

---

## Müşteri projeleri — canlı ve aktif

**Egeli OSGB [M]** — `ozel-yazilim/egelisaglik` · iş sağlığı ve güvenliği yönetim
platformu (firma, personel, uzman/hekim, eğitim, ziyaret, sertifika, faturalama).
8 .NET servisi + 4 panel + `mobile-expert` + Excel aracı · PROD · **son commit
2026-08-03 (bugün)** — en aktif iki projeden biri.

**GOAT [?]** — `ozel-yazilim/goat` · global oyun/oyuncu platformu (casino oyunları,
canlı yayın, sponsor, cüzdan, skor tahmini). 12 .NET servisi + 4 panel + 29 workflow ·
**prod altyapısı ayakta ama gerçek kullanıcı trafiği yok** — hedef kitleye
sunulmamış · son commit 2026-08-03 (bugün).
2026-06-12'de dışarıdan devralınmış. Domainler PR Yazılım dışı (bettaktik99.com,
panelstaff.org). `docs/_project/GUVENLIK-BORC.md`'de açılış öncesi kapatılması gereken
🔴 bulgular kayıtlı.

**Osinif [M]** — `ozel-yazilim/osinif` · online eğitim + birebir mentorluk platformu
(kredi satın alma, 20/40 dk seans, 40 kişilik canlı etkinlik). 10+ .NET servisi +
4 panel + `mobile-student` + 8 cron · PROD, `osinif.com`, gerçek veri ·
son commit 2026-07-31 (v1.2.0 prod GO).

**Deliverigo [M]** — `ozel-yazilim/deliverigo` · restoran siparişi + kurye yönetim
platformu (sipariş, kurye atama, muhasebe, harita/polygon). 7 .NET servisi + 4 panel +
`mobile-courier` · PROD, `deliverigo.com` · son commit 2026-06-25.
**Risk:** ayrı dev ortamı yok — `main` doğrudan production'a çıkıyor.

**A101/Egeli [M]** — `ozel-yazilim/a101egeli` · A101 market zincirinin tüm şubeleri
için OSGB takip platformu. `egelisaglik`'in izole klonu (A101 ölçeği yüzünden ayrı
kurulum). 7 .NET servisi + 4 panel · PROD · son commit 2026-06-17.

**Liston [M]** — `ozel-yazilim/liston` · emlak platformu (emlakçı başvuru/onay, ilan,
paket/üyelik). 8 .NET servisi + 2 panel + `mobile-app` · dev canlı
(`loap.pryazilim.com`), **production kapsam dışı** — henüz canlıya çıkmadı ·
son commit 2026-07-24 (EIDS kimlik doğrulama discovery).

**Platin Outsourcing [M]** — üç repo, mali müşavir işi:
- `platin-agent-web` · operatör paneli (GİB hesapları, görev başlat, sonuç/PDF izle) ·
  dev canlı, prod domain tanımlı, **prod gate eşiğinde** · son commit 2026-08-02
- `platin-agent` · XML beyannameyi BDP `.ebyn` paketine çevirip GİB'e otomatik yükleyen
  ajan (ayda 4000+ beyanname hedefi, ~10-12 ay ömürlü köprü çözüm) · .NET 10 console +
  Playwright · **erken POC, entry point boş** · **git altında değil**
- `platin-crm-ui` · şirket içi iş takip aracı, **sadece UI kapsamı** (backend'i müşteri
  yazıyor) · Next.js + mock data · deploy yok · son commit 2026-07-01

---

## Yarı yolda durmuş

**Bavyera Loyalty [M]** — `ozel-yazilim/bavyera-loyalty` + `p/mobile-app/bavyera-loyalty` ·
sadakat mobil uygulaması (bakiye/puan, QR ödeme, kampanya). Expo SDK 54 ·
**backend hiç bağlanmamış, ekranlar mock veriyle** · son commit 2026-05-12 ·
deploy izi yok.

**BT Products [M]** — `ozel-yazilim/btproducts` · hastanelere medikal test cihazı kuran
firmanın cihaz/varlık takibi, depo, transfer, sayım sistemi. Turborepo + 3 Next.js panel ·
**mock veriyle Coolify'da yayında**, gerçek domain ve .NET backend yok (sonraki faz) ·
son commit 2026-06-15 · müşteri kapsam PDF'i repoda (14.05.2026 v1).

**Turmed / ORBIS [?]** — `ozel-yazilim/turmed` · fabrika ERP'si (sipariş, stok, lot,
üretim, sevkiyat, packing list). **PR Yazılım kanonu değil** — FastAPI + Vite + Ant
Design, dışarıdan gelmiş/devralınmış (tahmin) · müşterinin Windows makinesinde
`KURULUM.bat` ile lokal · **git altında değil**, içinde `orbis_projesi.rar`.
Not: `p/web-sitesi/orbis_projesi` diye ikinci bir kopya da var.

**Kargomcom [?]** — `ozel-yazilim/kargomcom` · boş kabuk, yalnız VS Code config kalmış ·
**git altında değil**.
🔴 **`.vscode/launch.json` içinde düz metin şifreler:** SQL `sa`, Redis, Azure storage
account key, RabbitMQ — dev sunucusu `65.21.249.114`. Şifreler başka projelerde de
kullanılıyorsa etki tek projeden geniş. **Rotasyon kararı bekliyor.**

---

## Altyapı ve şablonlar

**pryazilim.core [A]** — `ozel-yazilim/pryazilim.core` · tüm .NET projelerinin ortak
altyapısı (cache, queue, logging, database, search, models, utility). 9 NuGet paketi,
GitHub Packages üzerinden dağıtılıyor, sürüm 0.1.4–0.5.0 · son commit 2026-06-26.

**dotnet-template [A]** — `ozel-yazilim/dotnet-template` · yeni özel yazılım projesinin
iskeleti: 4 API + websocket + panel + mobil + 5 kütüphane + tam CI/CD hattı
(11 workflow, K8s, Traefik) · son commit 2026-07-17.

**prvmautomation [A]** — `ozel-yazilim/prvmautomation` · yeni proje için DEV/PROD ortamı
kuran bash otomasyonu (Ubuntu, MicroK8s, Redis, SQL Server, Azure/GitHub CLI) · aktif
kullanımda · son commit 2026-06-24.

**web-sitesi ailesi [A+M]** — `p/web-sitesi` · 29 ayrı proje, kapsayıcı klasör (repo
değil). Baskın hat Turborepo + Next.js admin + Astro SSG + Prisma + Coolify.
Şablonlar: `web-template`, `web-template-next`, `gazi-template`, `demosite`.
Müşteri siteleri: durudiagnostik, balkanbee, btproduct, pruva-medikal,
izmirsagliknoktasi, lokumatolyesi, zikirvakti, yalinnetwork, rundevu…
En yeni aktivite: `gazi-template` 2026-08-03.

**skill-project / agent-project** — bkz. `CLAUDE.md` → "Bakılan yerler".

---

## Bekleyen iş

**Medivita OSGB [M]** — `ozel-yazilim/medivita-teklif-brief.html` (2026-07-16) ·
teklif öncesi kapsam belgesi. Çok şubeli OSGB platformu, dört panel + mobil.
**Egeli OSGB'nin üzerine kurulacak** ("bugün canlıda ve gerçek veriyle aktif" diye
referans veriliyor), iki farkla: bölge katmanı (yetki modeli, kozmetik filtre değil) ve
yüksek hacim (binlerce şube/personel, toplu işlem).
Müşteri içeriği toplanmış: `p/proje-icerik/egeli-saglik/Medivita`.

---

## Envanterden çıkan üç gözlem

**Bir — kendi ürün sayısı az ve dikkat müşteriye akıyor.** Net kendi ürün: WupDoc
(+ BalkanBee, sahiplik belirsiz). Bugün dokunulan iki proje `egelisaglik` ve `goat` —
ikisi de müşteri işi. WupDoc'a son dokunuş 24 Temmuz. Bu bir suçlama değil, finansman
modelinin mekanik sonucu: nakit müşteriden gelince dikkat de oraya gidiyor.

**İki — kendi ürünlerde dokümantasyon disiplini düşüyor.** BalkanBee envanterin en
büyük projelerinden biri (22 workflow, canlı prod, store'da mobil app) ve `docs/`
altında tek bir audit raporu var. Müşteri projesinde kapsam yazmak zorunlu; kendi
ürününde kimse zorlamıyor. **Çıkarım:** ürün teknik olarak bitiyor, iş olarak
tanımlanmıyor.

**Üç — üç proje git altında değil:** `kargomcom`, `platin-agent`, `turmed`.
`platin-agent` aktif bir müşteri POC'si (kardeş reposu dün commit almış) ve
versiyonlanmıyor — kaybedilebilir iş.

## Ölçümün sınırı

Sahiplik etiketleri dosya izlerinden çıkarıldı (README, PROJECT-INFO, domain, teklif
PDF'i). **[?]** işaretli üçünde ölçüm yetmedi, Mert'in doğrulaması gerekiyor.
`web-sitesi` altındaki 29 proje tek tek incelenmedi — yalnız listelendi ve baskın
teknoloji hattı çıkarıldı.
