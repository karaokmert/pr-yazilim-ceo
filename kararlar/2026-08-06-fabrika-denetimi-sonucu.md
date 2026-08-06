# Fabrika denetimi kapandı — yapılacak düzenlemeler

**Tarih:** 2026-08-06
**Karar veren:** Mert
**İş:** Sprint 1. iş — *Clara - Fabrika Ekibinin İncelenmesi* (`86cb1nmk4`)
**Kayıt:** `incelemeler/fabrika-denetimi/` (dört eksen + `eksikler.md`)

## Karar

**1. iş kapatıldı.** Dokümandaki dört bitiş şartı karşılandı:
dört eksen için kanıtlı bulgu listesi çıktı, hook hipotezi ölçüldü, dört ölçütün
durumu güncellendi (`incelemeler/fabrika-olcutu/kayit.md` sonuna eklendi), yapılandırma
eksikleri madde madde listelendi.

Mert'in kapatma koşulu: *"tüm gereksinimler karşılanıyorsa ve agent'lar mantıksal
olarak da planına uygunsa yapılacak düzenlemeleri kayıt altına alıp kapatabilirsin."*

**İkinci koşul da karşılanıyor:** dört agent planına uygun. Rol ayrımı tutarlı, her
skill'in sınır beyanı var, atıf disiplini biliniyor, memory dört klasörde sapmasız.
Bulunan dokuz çelişkinin hiçbiri **mimari** değil — sekizi aynı sınıftan: hüküm bir
yerde tam, atıfı başka yerde eksik.

## Denetimin sonucu — üç cümle

**Teknik kat sağlam.** Kırık atıf 0, hayalet index kaydı 0, kayıt dışı kural 0, hook
ana oturumda 4/4 doğru parse, 122 kural düzgün sayılmış, memory sapması 0.

**Yani "yeniden kurma, yapılandır" kararı ölçümle doğrulandı** (karar 2026-08-05).
Onarılacak mimari yok.

**Eksikler iki kökten çıkıyor:** cascade yarım kalıyor, ve üretim hattının çıkış ucu
hiç çalışmadı.

## Yapılacak düzenlemeler — 4. işin girdisi

Sıra önerisi; karar uygulama anında Mert'te. Tam kanıt `eksikler.md`'de.

### Öncelik 1 — cascade onarımı (dördüncü ölçüt buna bağlı)

`atif_verenler` alanı 123 kuralın 112'sinde boş; gövdede anılan 38 kimliğin 28'i
atıfsız. Bu alan index'in kendi beyanında *"cascade'in haritası"* ve PQA'nın denetim
ekseni. Doldurulmalı, ve alanın **tip kararı** verilmeli (bugün bazı kayıtlarda dosya
yolu, bazılarında kimlik var).

Beş yarım cascade düzeltilmeli:
- `yapi-taslari:296-300` PAM'de Bash yok diyor, PAM body'si tersini (body düzeltilmiş,
  skill kalmış) — **PQA bu skill'i ölçüt sayıyor**
- `is-duzeni:73-74` *"tek yazma yetkisi PAD"* mutlak yazılmış; fiilen dört elde yazma
  var, bir delik (PQA `plugin.json` sürümü) hiç tanınmıyor
- `ISD-STAY-IN-ROLE` dört rolü bağlıyor, PCA'nın bölümünde yaşıyor
- `ISD-COMMIT-THEN-PUSH` PAD'in commit ettiğini söylüyor, PAD body'sinde "commit"
  kelimesi hiç yok
- `BHV-NO-SELF-CONFIG` dördünü bağlıyor, yasak yalnız PAM/PAD body'sinde

Ve tekrarlanan gerekçe blokları tek kaynağa indirilmeli — hook'un "üç tasarım kararı"
bloğu iki skill'de neredeyse birebir, ve `URT-NO-DUPLICATE-ID`'nin öngördüğü şey tam
olarak gerçekleşti (yukarıdaki ilk madde).

### Öncelik 2 — alt-agent'a kanon nasıl ulaşacak (kapsam büyüdü)

Hook ölçüldü. Ana oturumda **çalışıyor**; alt-agent'ta **hiç çalışmıyor** ve
`CLAUDE_CODE_AGENT` **çağıranın** adını taşıyor (PCA açıldı, değer
`pr-agent-manager` geldi).

**Sıra kuralı — PAM'in tespiti, kayda geçiyor:** iki arıza birbirini maskeliyor. Hook
alt-agent'ta tetiklenmediği için yanlış env değerini kullanma fırsatı bulmadı. Bu
yüzden **hook'u env sorunu çözülmeden çalışır hâle getirmek sistemi bugünkünden kötü
yapar** — bugün alt-agent kanonsuz kalıyor (görünür arıza), o durumda yanlış
personelin kanonunu yüklü sanarak çalışır (sessiz arıza). Sıra tersine kurulamaz.

Ve asıl bulgu: PCA üç skill'den ikisini aldı, `uretim`'i almadı — **hook'la değil,
başka bir yolla.** Yani kanonun ulaşması kimsenin garanti etmediği bir mekanizmaya
bağlı, tur tur değişebilir, kimse fark etmez. PCA'da zarar yoktu (ölçüm işiydi);
**PAD'a üretim işi verilirse üretim kanonsuz yapılır.**

### Öncelik 3 — sıfırdan üretme yöntemi (en zayıf halka, en büyük iş)

Bir takımın kendi tasarımı hiçbir dosyada yok. Kanon paketlemeyi (26 kural, 416 satır)
ve mevcut kanonu değiştirmeyi (60 satırlık üçüncü hat) ayrıntılı yazmış; kuruluş hattı
**5 satır** ve *"yeni takım kurulurken ya da mevcut kanona ekleme yapılırken"* diye iki
farklı işi aynı hatta koyuyor.

Fabrika bunu kendi kuruluşunda tespit etti ve açık bıraktı
(`docs/fabrika/ekip-kurulumu/gereksinim.md:13-16`).

Kapsamı Mert'le çizilecek — bu bir kural yazma işi değil, **yöntem üretme** işi.

### Öncelik 4 — rapor biçimi (dört tekrar, iş hiç açılmadı)

Biçim kuralı var (7 kural) ama şikâyetin geldiği an — **soru sorma anı** — kapsamın
dışında; `BHV-SHAPE-REPORT` bunu kendi kapsam cümlesiyle dışarıda bırakıyor. Uzunluk
sınırı sayı olarak yok. Tanınmış gerilim: `ISD-PRINT-AUDIT-RAW` denetim raporunun
özetlenmesini yasaklıyor ve gerekçesi ölçülmüş.

### Öncelik 5 — filo bakımını bir kez koştur

Yapı var ama **sıfır kez çalıştı** (*"Son filo taraması — Yapılmadı"*).
`PAM-REPORT-FLEET-AGE` bir tarih karşılaştırması yapıyor, karşılaştıracak tarih yok.

İki açık kalem `durum.md`'de duruyor ve ikisi de *"ikinci takımda ölçmek ucuz,
sekizincide cascade demek"* sınıfında: **kimlik çakışması** (iki takım aynı kimlik
kalıbını kullanırsa atıflar sessizce yanlış kurala tutar) ve **plugin skill'inin en
düşük öncelikte olması** (kullanıcı düzeyinde aynı ad varsa plugin kanonu sessizce
ezilir — ölçülmüş arıza, `dagitim`'in 26 kuralında bu kontrol yok).

Üçüncü kalem: **`docs/` commit sahipliği tanımsız** — PQA bunu kanon boşluğu ilan etti,
iki turda iki kez bildirdi, bedeli ölçüldü.

### Öncelik 6 — küçük ama sessiz kalemler

- **`Task` mı `Agent` mı:** kanonda 20 yerde `Task` yazıyor, envanterde araç adı
  `Agent`. PAM sahada `Agent` kullandı — yani kanon metni gerçeği yanlış tarif ediyor,
  fiilî arıza değil. Metin düzeltilmeli.
- **PQA denetleyeceği kanonu elinde bulundurmuyor:** `yapi-taslari` denetim ekseninde
  ama `skills:` listesinde yok, hook da basmıyor. Aynısı `dagitim` için
  (`DAG-BUMP-BY-AUDITOR` PQA'ya iş veriyor, PQA o skill'i okumuyor).
- **PAM'de `tools:` yok** (bilinçli, gerekçesi yazılı) — ama 3. iş PAM'den `Task`
  yetkisini almayı öngörüyor ve **alınacak liste yok**, kısıt sıfırdan yazılacak.
- **İki skill kendi eşiğini aşıyor:** `is-duzeni` 612 satır, `yapi-taslari` 507 —
  kanonun kendi eşiği 500. Etkisi somut: compaction kırpması dosyanın **sonunu** atıyor.
- **Bir konu kayması:** `dagitim:111-117` rol dağıtımı tanımlıyor, oysa `is-duzeni`
  *"rol tanımının tek kaynağı burasıdır"* diyor — ve atıf verilmemiş.
- **Hook'ta latent kırılganlık:** awk parser YAML akış biçimini sessizce boş döndürüyor.

## Ölçülmemiş kalanlar — dürüstlük kaydı

- Hook alt-agent'ta **neden** tetiklenmiyor (`SessionStart` bir oturum olayı; `Agent`
  ile açılanın ayrı oturum sayılıp sayılmadığı)
- `behavior` + `is-duzeni` alt-agent'a **hangi mekanizmayla** geldi
- `uretim` **neden gelmedi** — diğer ikisi geldiyse ayrımın bir sebebi var
- Aynı ölçümün **PAD'da** tekrarı (PCA sonucunun PAD'da da aynı çıkacağı varsayım)
- Hook'un `CAKISAN` dalı hiç koşmadı (`~/.claude/skills/` boş)
- `tools:` listesinde çözümlenmeyen bir girdi ne yapıyor (`arac-envanteri` *"agent hiç
  başlamıyor"* diyor ama PAD çalışıyor — kısmi yanlış yazım tolere ediliyor olabilir)

## Clara'nın bu işte düzeltilen iki hatası

**Bir:** `CLAUDE_PROJECT_DIR` tanımsızlığından *"hook devre dışı"* çıkarımı yapıldı.
Yanlış — iki ayrı ortam var (hook'u Claude Code çağırıyor; agent'ın `Bash`'ine verilen
ortam `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` ile temizlenmiş). PAM düzeltti.

**İki:** *"Dördüncü ölçüt karşılanmıyor"* denirken gerekçe olarak 08-03'teki
*"mekanizma yok"* tespiti kullanıldı. O tespit geçersizdi — yapı 08-02'de kurulmuş.
Karşılanmama sebebi başka: yapı hiç koşmadı ve cascade haritası boş.

İkisinin ortak dersi `CLA-LABEL-YOUR-EVIDENCE`'a bağlı: bir ölçüm iki farklı şeyi
ölçüyorsa hangisini ölçtüğünü söylemek zorundasın.

---

## DÜZELTME (2026-08-06 akşamı) — bir atıf hatası

Bu dosyada ve `incelemeler/fabrika-denetimi/eksikler.md`'de şu cümle geçiyor:
*"PAM'in tespiti — sıra tersine kurulamaz."*

**Atıf yanlış.** PAM'in ölçtüğü ve söylediği şey şu: iki arıza birbirini maskeliyor
(hook alt-agent'ta tetiklenmediği için yanlış env değerini kullanma fırsatı bulmadı).

**Sıralama sonucunu — "hook'u env düzeltilmeden çalıştırmak sistemi kötüleştirir" —
Clara çıkardı.** Çıkarım muhtemelen doğru ama PAM'e mal edilmesi yanlış; PAM'in kendi
ölçümü dar: *"ana oturum olarak açıldım ve hook çalıştı, alt-agent durumunu bu oturumda
ölçmedim."*

Nasıl bulundu: PAM aynı hatayı fabrikadaki Clara'nın handoff'unda da yakaladı ve
itiraz etti. Yani hata iki kez tekrarlandı ve ikisinde de kaynağı Clara'ydı.

**Sınıfı:** `CLA-LABEL-YOUR-EVIDENCE` ihlali — ölçülen ile çıkarsanan karışmış. Ve
özel bir alt sınıfı var: **kendi çıkarımını karşı tarafa mal etmek.** Bu, ölçümü
olduğundan güçlü gösteriyor çünkü *"ölçen kişi böyle dedi"* ile *"ben böyle
düşünüyorum"* farklı ağırlık taşıyor.

Kural olarak kanona giren hâli: bir handoff'ta karşı tarafın tespiti aktarılırken
**onun cümlesi ile senin çıkarımın ayrı satırda durur.** Karışırsa karşı taraf kendi
söylemediği bir şeyi savunmak zorunda kalır.
