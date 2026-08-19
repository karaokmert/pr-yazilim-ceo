# Kapanış — 2026-08-19 akşam · Fabrika skill temizliği + Clara'nın iletim yetkisi

**Mod:** EV · **Süre:** 17:02 → 19:05 · **Repo:** `skill-project`
**Ekip:** PAM · PAD · PCA kapanışa alındı; **PQA açık** (push işi sürüyor)

> Bu günün İKİNCİ kapanışı. Birincisi (`-gece-nobeti-ve-ogrenme-dongusu.md`)
> 18 Ağustos 20:13 → 19 Ağustos 16:50 arasını kapsıyor. Bu dosya 17:02'den
> sonrasını taşır.

---

## 1. NE BİTTİ

### Fabrika skill listesi 26 → 5 indirildi
**Commit:** `26c1148` (77 dosya, +3173/−7804)

Mert'in tetiği: *"fabrika agentlarındaki problemleri gidermemiz gerekiyor,
bizi çok yavaşlatıyor ve hantallaştırıyorlar."*

**Ölçüm dayanağı:** dört agent'ın (`pr-agent-manager/developer/qa/context-analyst`)
frontmatter'ında yalnız beş skill yazılı — `behavior`, `is-duzeni`, `uretim`,
`yapi-taslari`, `dagitim`. Kalan 21'e **sıfır agent atfı**.

`trash/2026-08-19_1754-emekli-fabrika-skilleri/` altına taşınanlar:
- **7 kırık symlink** — hepsi `../../ag-agent/skills/`'e bakıyordu, o klasör bu
  repoda YOK. Yani zaten çalışmıyorlardı: `agent-generator`,
  `agent-production-standard`, `cascade`, `drift-tarama`, `ground-truth`,
  `memory-terfi`, `teshis`
- **9 emekli klasör** — `uretim-standardi` (120K), `uretim-akisi`, `kanon-sagligi`,
  `saha-olcumu`, `plugin-dagitim`, `memory-management`, `environment`, `finish`,
  `pause`
- **5 `deney-*`** — RED-2 aparatının skill symlink'leri

⚠️ **Yanlış pozitif ayıklandı:** `cascade` 15 kez geçiyordu ama **hiçbiri skill adı
değildi** — hepsi "cascade" kavramı olarak. Hükmü artık `is-duzeni` + `behavior`
taşıyor. Aynı şekilde `ground-truth`/`environment` sayıları kelime çakışmasıydı, ve
v8'in `memory-management`'ı fabrikanınkinden **ayrı bir dosya** (ona dokunulmadı).

### RED-2 deney aparatı silindi
PAD'in kendi yazdığı `docs/fabrika/suzgec-olcumu/deney/temizlik.sh` ile koşuldu —
kendi komutumu yazmaktansa. Beş `deney-agent-*.md` symlink'i + aparat gitti,
kalıntı taraması temiz.

**Silmeden önce çıkarım taraması yapıldı** (bu turda öğrenilen kural, aşağıda):
gereksinim yazılı ✓ · ölçüm kayıtları duruyor (9 dosya) ✓ · PCA'nın dersleri
`e3fadef`'te commit'li ✓ · `skills:` bulgusu `yapi-taslari`'nda ✓

### `rules-index.json` kırık atıfları temizlendi
Dört kuralın `atif_verenler` listesinde taşınan skill'lere işaret eden satırlar vardı:
`ISD-COMMIT-THEN-PUSH`, `ISD-RETURN-TO-PLANNER`, `ISD-ASK-IN-TWO-STEPS`,
`DAG-BUMP-BY-AUDITOR`. JSON geçerli, 137 kural yerinde. Yedek: `/tmp/rules-index.bak.json`.

### İki çöp klasörü birleşti — ve bir arıza yakaladı
`.trash/` (benim açtığım) → `trash/` (var olan düzen). **Bulgu:** `trash/`
`.gitignore`'da, `.trash/` değildi — yani 21 emekli skill **commit'e girecekti**.
Birleştirmeden sonra görünmez oldular; doğru davranış, trash bir bekleme alanı.

### Fabrika dördü memory'lerini commit'ledi
`001d067` (PAD) · `e3fadef` (PAM) · `4ca5aab` + `09db7b6` (PAM düzeltmeleri)
`aa1f493` (Clara). `.claude/agent-memory/` tamamen temiz.

---

## 2. KARARLAR (Mert'in, bu oturumda verildi)

### Clara devir bloğunu SendMessage ile iletir
**Karar:** `konular/clara/kararlar/2026-08-19-handoff-sendmessage-ile-iletilir.md`

Mert'in cümlesi: *"benim onayımla handoffu send message ile iletiyorsun."*

`CLA-NO-CALL-TEAMS` değişti — eskiden *"Mert taşır"*, şimdi *"onayla Clara taşır"*.
Gerekçe mekanik: `Agent` hedefi alt göreve dönüştürür ve raporu çağırana getirir;
`SendMessage` hedefi **kendi oturumunda bırakır**. Kalan risk (rapor Mert'e
ulaşmaz) iki şeyle kapatıldı: onay kapısı + dönen cevabı **ham hâliyle** basma.

Uygulandı: `~/.claude/agents/clara.md` (kural gövdesi) ve
`~/.claude/skills/sendmessage-akisi/SKILL.md` (Clara bölümü ikiye ayrıldı —
**saha ağında izleyici**, **fabrika ağında taşıyıcı**).

### `e3fadef` kapsam taşkını olduğu gibi kalıyor
PAM'in commit'i 20 dosya aldı, 16'sı PCA ve PQA'nın (ortak git stage'i).
Mert: bölünmüyor, mesajı da düzeltilmiyor — içerik doğru ve eksiksiz, yanlış olan
yalnız atıf; memory dosyaları zaten klasöre göre ayrık.

### Eşzamanlı commit için kural YAZILMIYOR
Sebep kaldırıldı, üstüne kontrol konmadı (`CLA-FIX-THE-CAUSE`). Düzeltilen şey
Clara'nın talimatı, kanona eklenen bir kural değil.

### Gün kapanışı tek commit
Üç ayrı iş (temizlik, v8 kanon, dokümanlar) tek commit'te — `26c1148`.

---

## 3. CLARA NE ÖĞRENDİ (üç yeni hafıza kaydı)

Mert'in tetiği: *"ben senin gelişimini söyledim — sen bu çıkarımlardan geliştin mi?"*

### `olcum-araci-silinmeden-cikarimi-alinir`
Bir aparat/deney/ham kayıt silinecekse **önce çıkarımının bir yere girdiğini ölç**.
Kanonda *"iki ay sonra biri açarsa fazlasını öğrenir mi"* sorusu yazılıydı ama ham
kayıt için okunuyordu; **ölçüm ARACI ayrı sınıf** — cevap alınmadan araç atılmaz.
Somut tetik: `trash`'e taşırken içinde `deney/`, `APARAT.md`, ham çıktı varsa DUR.

### `baskasinin-olcumu-bana-ulasmiyor`
PCA'nın koştuğu ölçümün çıkarımı **onun** hafızasına girer, Clara'nınkine girmez.
RED-2 iki gün önce koştu, izi yoktu; 2986 satır sıfırdan okundu. Kanondaki
*"değerlendirilip bırakılan itiraz öğrenilmemiş sayılır"* satırının tam vakası.

### `ortak-repoda-eszamanli-commit`
Birden çok agent aynı repoda commit'lerken `git add`+`commit` **yetmez** — stage
ortak. Doğrusu iki adım: `git add <klasör>` + `git commit -m "..." -- <klasör>`.

⚠️ Bu kayıt **iki kez düzeltildi** ve ikisini de PAM ölçtü:
1. **Argüman sırası** — Clara `git commit -- <yol> -m "..."` yazmıştı, HATA VERİYOR
   (`--`'dan sonrası pathspec sayılır). Doğrusu `-m` önce, `--` sonra.
2. **Takip edilmeyen dosya** — `-- <yol>` yalnız git'in ZATEN takip ettiğini alır;
   yeni dosya düşer. Ve bu **sessiz**: klasörde değişmiş bir dosya varsa
   (memory'de `MEMORY.md` hep değişir) commit atılır, eksik görünmez.

Clara ikisini de `/tmp`'de temiz repoda birebir doğruladı.

⚠️ **Desen:** bugün Clara üç kez hata yaptı, **üçünü de başkası yakaladı** — Mert
aparatı, PAM komutu iki kez. `yarim-olcum-deseni` kaydının 3., 4. ve 5. vakası.

---

## 4. NE YARIM KALDI

| Ne | Kimde | Ne bekliyor |
|---|---|---|
| **Push** | PQA | 7 commit `origin/main` önünde. Denetim + **Mert'in onayı**. |
| **RED-2 katman kararı** | PAD | `docs/fabrika/red2-sinir-isaretleri/gereksinim.md` — iki çıkarımın nereye yazılacağı |
| **PQA kapanışı** | Clara | Push bitince kapanış verilecek |

---

## 5. MERT'İN KARARINI BEKLEYEN

**Push onayı** — 7 commit hazır, PQA denetimde. Neden onun: canlıya çıkan iş.

**`URT-NO-CONTENT-IN-DESCRIPTION` şerhi** — PAD'in katman kararı geldiğinde kuralın
gövdesine ölçüm şerhi düşülecek. Neden onun: kanon değişikliği.

---

## 6. ÖLÇÜLDÜ AMA ÇÖZÜLMEDİ

**`CLAUDE.md` §3'teki "iki skill ailesi yan yana" borç bloğu artık geçersiz.**
Blok kendisi *"emekli aile temizlendiğinde bu blok silinir"* diyor — emekli aile
bugün temizlendi, blok duruyor. Kimse görevlendirilmedi.

**Agent listesi tazelenmesi belirsiz.** Yeni tanımlanan agent tipi bir oturumda
6 dakikada çağrılabildi (PAD), başka oturumda 40 dakika sonra bile çağrılamadı
(PCA). Tetikleyici iki ölçümde de belirlenemedi. RED-2 gereksiniminin (b) maddesi.

**`rules-index.json` bakımsız.** Bugün dört kırık atıf temizlendi ama sabahki
ölçüm 138 eksik referans saymıştı. Bütünsel bir index işi gerekiyor.

---

## 7. BİR SONRAKİ HAREKET

PQA'nın push'u bitince kapanışını ver; sonra `CLAUDE.md` §3 borç bloğunun
silinmesi için gereksinim yaz.
