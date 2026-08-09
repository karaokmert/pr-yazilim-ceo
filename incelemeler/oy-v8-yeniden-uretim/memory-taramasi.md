# OY memory taraması — kanona taşınacak saha bilgisi

**Ölçen:** Clara (Explore taraması) · **Tarih:** 2026-08-09
**Kapsam:** `~/.claude/agent-memory/ozel-yazilim-*` — dokuz kutu, 936 KB, ~198 dosya

**Sonuç: memory'nin ~2/3'ü kanona taşınmalı, ~1/3'ü çöp.**

---

## Kutu dağılımı — ve okunan asıl şey

- `project-assistant` 244K / 49 dosya — %73'ü kullanıcı geri bildirimi
- `qa-engineer` 192K / 40 — denetim yöntemi + kaçan hata öz eleştirisi
- `backend-developer` 184K / 40 — 18 kazanım, en olgun kutu
- `frontend-developer` 124K / 27 — 12 öz-hata kaydı, duvar yoğunluğu en yüksek
- `devops-engineer` 108K / 20 — saha gerçeği ağırlıklı
- `code-auditor` 52K / 14 — yalnız yöntem dersleri (doğru, CA statik)
- `mobile-developer` 20K / 5 · `test-engineer` 12K / 3 · `ui-designer` **0**

**Kutu doluluğu kanon kalitesini ölçmüyor, sahaya çıkma sıklığını ölçüyor.** UID boş ve
TE 3 dosya — kanonları mükemmel olduğu için değil, **hiç sahaya çıkmadıkları için.**
TE'nin tuttuğu tek not bile *"PROJECT-INFO'da test kullanıcı bölümü boş"* şikayeti.

**Bunun yeniden üretimde sonucu var: memory'si olmayan agent kanonun eksiğini
raporlayamaz.** En riskli iki rol, memory'si en boş olan ikisidir — çünkü onlar için
düzeltme sinyali hiç üretilmedi.

---

## Kanonun okunan iki eksikliği

### 1. Kanon "ne yapılır"ı söylüyor, "nasıl yanılırsın"ı söylemiyor

Dokuz kutunun en kalın dosyaları kural değil, **aracın sessizce yalan söylediği an**
kayıtları. Ortak imza: *derleme yeşil / araç sessiz / hata yok gibi görünür.*

**Sessiz kırılma envanteri — kanonda karşılığı yok:**

- `HandlerOptions` varsayılanları **açık** — yalnız `AdminUser=true` yazmak endpoint'i
  herkese bırakıyor; üye token'ıyla moderasyon yapılabildi, statik incelemede görünmedi
- `Enum.IsDefined` + byte enum: `(int)` cast **derleme yeşil**, çalışma anında patlıyor
- `mutationFn: ApiService.x` → `this` kopuyor; **build + tsc yakalamıyor**, tıklayınca
  patlıyor (goat'ta `.bind()`'lı 7 yer tuzağın kanıtı — en az iki kişi düşmüş)
- `DateView isUtc` ters sezgisel: verilmezse 3 saat çıkarıyor. **Çoğunluk deseni yanlış**
  (102'de 42) — emsale uyulursa hata üretiliyor. QA da kaçırdı
- `grep -c` çoklu dosyada `0\n0` dönüp koşulu kırıyor → araç *"hata yok"* diyor, vardır
- `git rev-parse branch:yol` olmayan dosyada **exit 0** → "yeni" ile "güncellenmiş"
  ayrımı sessizce kayboluyor
- LSP **0 sonuç ≠ tüketici yok** — indeks yüklenmemiş olabilir, araç hata vermiyor
- `gh run list --workflow` gösterim adını kabul etmiyor → **hata vermeden** timeout'a
  kadar boş bekliyor
- `nc -z` VPN arkasında köreliyor — 24/24 port "açık" çıktı, hiçbiri kurulu değildi
- `telepresence quit` (`-s` yok) sonraki intercept'i 30s bekletiyor; Ctrl+C intercept'i
  **bırakmıyor** (cluster kapalı makineye trafik yollamaya devam ediyor)

**En ağır vaka — uydurma numaraya gerçek SMS gitti.** Agent `90-5559990001/2` uydurup
`send-basket-code` çağırdı, iki gerçek aboneye SMS gitti. Ve **aynı turda kendi raporuna
"dev'de SMS sağlayıcısı canlı" diye yazmıştı** — bilgi elindeyken düştü.

### 2. "Preloaded ≠ okunmuş" — beş kayıt, üç kutu, bağımsız yazılmış

PA (`feedback_preload_okumak_degil.md` + `feedback_yapi_bilgisi_gereksinim_degil.md`),
BE (`feedback_kanon_okuma_zamani.md` — 5 ihlal · `feedback_denetimde_kanon_once.md` —
kanonsuz 4 yanlış bulgu, **biri developer'a hatalı kod yazdırdı**), FE
(`kazanim_skil-taramasi-dosyadan-degil-alet-cantasindan.md` — 3 skill kaçtı).

**Teşhis: kanon okunuyor ama uygulama anında hafızadan çalışılıyor — çünkü kanon
"ne zaman aç" eşiğini vermiyor.**

Bu, Mert'in 1. ve 6. maddesinin sahadan gelen kanıtı: *hangi işte hangi skill'e
gidileceği net değilse, agent gitmiyor.*

---

## Kural adayları — memory'de tekrar eden kalıplar

**"Emsal kanon değil" — altı kayıt, beş kutu.** BE, FE, PA, MB, DO bağımsız yazmış.
Kural adayı: *emsal desen kanonu doğrulamaz, kanon skill'den okunur.*

**"Kendi ölçüm aracından şüphelen" — beş kayıt, üç kutu.** QA, CA, DO. Kural adayı:
*"EKSİK/YOK" çıkan ölçüm önce kendi komutundan şüphelenir.*

**"Push onayı atlanmaz" — üç kez tekrarlandı** (QA kutusu, biri revize-3'te kullanıcı
uyarısıyla).

**"Ekranda doğrula, kod okuması yetmez" — üç uçta aynı ders** (PA, FE, BE).
Mert'in cümlesi: *build yeşili doğrulama sayılmaz.*

---

## Skill boşlukları — kanon eksik, agent kendi notuyla doldurmuş

**LIVE DEV geri-besleme kolu kanonda yok.** `is-akisi` madde 7 LIVE DEV'de bitiyor;
gerçek akış `LIVE DEV → operasyon testi → subtask → revize → düzeltme → tekrar LIVE DEV
→ prod`. PA'nın revize yakalama tetiği yok — PA fark etmedi, kullanıcı söyledi.

**Dış insan katkısının içeri alınması hiçbir skill'de yok.** Dış tasarımcı PR'ında doğru
fiil merge/cherry-pick değil **dosya indirme**; PA kanon boşluğu yüzünden git refleksine
düştü, ikisi de yanlıştı, kullanıcı düzeltti.

**Sprint planlama yöntemi skill değil, memory'de yaşıyor** — 11KB + 7KB iki dosya,
*"her geliştirme buraya eklenir"* notuyla. PA kendi kanonunu memory'de yazmış.

**Onay brief kalıbı memory'de** — *"skill gelince SİL"* damgalı.

**Telepresence çoklu servis tarifi `dev-environment`'ta yok** — 15KB memory'de,
*"2/2 tuttu, terfi notu OLGUN"* işaretli.

**`ozel-yazilim` plugin'inde ClickUp MCP'si yok** — PA kanonu ClickUp'ı zorunlu tutuyor
(`CLICKUP-TASK-FIRST`), araç pakette yok; `websitesi` plugin'inin MCP'si kullanılıyor.
**Yalnız OY kurulu bir makinede PA kanonun emrettiği işi yapamaz.**

Ayrıca: enum tüketici sayımı (`enum-sync`'te yok — kanıt: ~2 ay sessiz prod hatası),
prod dayanıklılık üçlüsü (5 projede ölçüldü: probe yok, `npm ci` kullanan 0/5, ACR
kuralı prod imajını siliyor), CI kapsamı dışı manifest, PROD damgası sahipsizliği.

---

## Kanonla çelişkiler — silinmemeli, notla taşınmalı

Beş vaka, hepsi `kanon_saha_celiskileri.md` ve PA kutusunda:

- **`ENUM-BYTE`** — kanon `: byte` zorunlu diyor, osinif enum'larının hepsi `int`
- **`CQ-COMMENT-WHY`** — kanon ticket referansını kodda yasaklıyor, osinif'te 74 satır
  `PRY-*` yorumu var
- **NVARCHAR standartları** — kanon Email 100/Phone 20, egelisaglik'te canlı DB
  sorgusuyla doğrulandı: hepsi `NVARCHAR(MAX)` (index'lenemez)
- **`BE-PERF-SQL-SIDE`** — `CompanyDataLayer` **iki deseni birden** taşıyor; agent bu
  tuzağa düşüp developer'a yanlış yönlendirme yaptı
- **`PA-DISC-CHUNK`** — kullanıcı 2026-08-03'te kanonun tersine karar verdi
  (*"BE tümünü bitirsin, QA'ya bir kez gitsin"*), memory'de *"AG düzeltene kadar"*
  damgasıyla duruyor

**Taşıma biçimi:** silinmez — kanona *"kanon sahadan ileride, mevcut koda dokunma"*
notuyla girer. Aksi hâlde emsale bakan agent yanılır.

---

## Çöp — taşınmayacak

Proje-özel kapanış devirleri · bayat domain/yol notları (`*.ulak.ws` ölü, 10 modül
dokümanında hâlâ duruyor) · `core.logging` ölü paket (gövde tamamen yorumda,
`Exception(ex)` no-op) · `app.config.ts` gelince kalkacak koşullu kayıtlar ·
*"skill'e girince SİLİNİR"* damgalı geçici düzenler.

Bunlar zaten kendi ölüm tarihini yazmış.

---

## Canlı borç — yeniden üretimde düşmemeli

**QA kapanış indeksinde 2 açık devir** (goat chat B4 FE pushlanmadı · osinif sprint
sahipsiz iki kalem) + **3 açık prod kapısı.**

**DO açık kalemleri:** egelisaglik prod secret'ları **dış IP** kullanıyor
(`85.95.231.42,51433` — DB portları dünyaya açık, kullanıcı teyitli *"genel PR Yazılım
standardında çözülmeli"*), osinif probe yok, ingress otomasyon dışı.

Bunlar ya taşınmalı ya kapatılmalı; aksi hâlde **sessizce düşer.**
