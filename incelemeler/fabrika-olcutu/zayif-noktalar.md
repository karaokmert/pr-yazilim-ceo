# Fabrikanın bilinen zayıf noktaları — kuruluş oturumundan

Tarih: 2026-08-03 (gece) · Kaynak: aynı oturum, `a6c6fcb6-...jsonl`, 6736 satır

Bu dosya `kayit.md`'nin eşi. Orada fabrikanın **ölçütü** var (ne olması gerektiği),
burada **kendi kanonunun kabul ettiği zayıflıklar** var.

Yöntem: dört paralel tarama, anahtar kelime eksenli. **Sınır: o kelimelerle
söylenmemiş bir şey kaçmış olabilir.**

Bir uyarı — transcript'te `[user]` etiketli uzun mesajların çoğu Mert'in değil, o
oturumda çalıştırılan **sınama agent'larının** raporudur. Aşağıda kimin söylediği
ayrılmıştır.

## En büyük boşluk — filo bakımı sahipsiz

Mert'in sorusu (kendi cümlesi):

> *"Sahada 8 takım kurduk diyelim, 6 ay sonra behavior neredeyse hepsinde benzer ama
> bir şey değiştirmek istiyorum — tüm takımlarda bu düzenleme yapılmalı kararı
> alabiliyor muyuz? Claude Code'a bir özellik geldi, hoop diye tüm agent'larda
> kullanılsın istiyoruz — bu taramayı nasıl yapıyoruz? Yani genel agent
> takımlarımızın bakımından, yeni özelliklerden kim sorumlu?"*

Oturumda **cevaplanmadı.** *"Ayrı bir oturuma bırakıldı, orada muhtemelen yeni bir rol
ya da yeni bir hat çıkacak"* denildi — **o oturum hiç olmadı.**

Dört alt soru sahipsiz kaldı: bir `behavior` değişikliği 8 ayrı iş mi açar; yeni Claude
Code özelliğini kim fark eder; `yapi-taslari` skill'ini kim güncel tutar (ölçülmüş
mekanik taşıyor — mekanik değişirse skill yanlışa döner); kimlik çakışmasını kim ölçer.

**Bu boşluk fabrikanın var olma sebebiyle aynı.** v7'nin ölçülmüş tek arızası bakım
zorluğuydu (*"bir kural değişimi günlerimi alıyordu"*). Fabrika onu çözmek için kuruldu
ve bakım sorusu fabrikada da sahipsiz kaldı.

`docs/filo/durum.md` ve `PAM-REPORT-FLEET-AGE` kuralı var — ama o yalnız *"tarama
tarihi eskiyse söyle"* diyor. Taramayı kimin yapacağı, neyi tarayacağı, bulguyu kimin
takıma çevireceği yazılı değil.

## Fabrika kendi skill'lerini hiç açmadı — ölçüldü

7 oturumun **7'sinde de `Skill` aracı çağrısı sıfır.**

Daha ağırı: dört fabrika oturumunda `skill_listing` attachment'ı da yok — yani
kullanılabilir skill listesi context'e hiç girmemiş.

PAD skill dosyalarına 29 kez erişti, hepsi `Read`/`Bash` ile ve hep aynı ikisine
(`is-duzeni` + `behavior`). **`uretim` ve `dagitim` gövdesi bir kez bile açılmadı.**

1.319 kural anması, 147 farklı kimlik sayıldı — ama çoğu *sayma* bağlamında, uygulama
değil. 32 hayalet kimlik: transcript'te var, kanonda yok.

## `dagitim` — 20 kural, sıfır test

İkinci en kalabalık skill. Üreten agent'ın kendi şerhi:

> *"`team/team-1-oy/` şu an boş ve bu repoda henüz `marketplace.json` yok — bu skill ilk
> gerçek paketlemeden önce yazıldı, kuralların hiçbiri gerçek bir artifact üzerinde
> sınanmadı."*

Ve soru-cevapla sınanamaz, çünkü kuralları mekanik. Tek yol gerçekten bir takım
paketlemek.

## Araç kısıtı sahada tutmadı

PQA'nın frontmatter'ında `Write`/`Edit` **yok.** Sahada **4 Write + 1 Edit** yaptı,
hepsi başarılı, hata dönmedi.

Ölçüm agent'ının cümlesi: *"beyan edilen tool seti sahada uygulanmamış — agent kendisine
tanımlanmamış aracı çağırdı ve harness izin verdi."*

Bu bugün OY tarafında ölçülen şeyle birleşince tablo tamamlanıyor
(`incelemeler/agent-arac-envanteri/kayit.md`): OY'de kısıt hiç yok, fabrikada kısıt var
ama **işlemiyor.** Yani *"denetçi kod yazmaz"* iki tarafta da yalnız metne dayanıyor.

## Çözülmemiş kanon çelişkileri

**`BHV-FLAG-INHERITED` ↔ `BHV-SCAN-BEFORE-CREATE`** — çakıştığı fark edildi,
*"bildireyim mi düzelteyim mi"* diye soruldu, **boşluk etiketiyle bırakıldı.**

**`BHV-RATION-ABSOLUTES` kendi metniyle çelişiyor** — kural mutlaklığı BÜYÜK HARFE
bağlanmış, ama aynı skill'de *"hiçbiri atlanmaz"*, *"rapora girmez"*, *"dokunma"* gibi
küçük harfli mutlak kipler var ve okuyan agent için aynı etkiyi yapıyor.
*"Ölçüt tipografi değil dil olmalı"* denildi, düzeltilmedi.

**PQA'nın kimlikleri kendi yasakladığı deseni taşıyor** (`PQA-NO-FILE-EDIT`,
`PQA-NO-PROPOSE-FIX` — `NO-` deseni). PQA kendi buldu ve *"ölçmediğim için bulgu diye
yazmıyorum"* dedi.

Örüntü tek cümleyle özetlenmiş: **"Kural bir tarafa yazılmış, karşı taraf boşta."**

## Kanonun yalnız yasak tarafı sınandı

Clara'nın kendi meta-ölçümü (aynı oturumda):

> *"Bütün testler 'şunu yapma' biçimindeydi, agent direndi. Yasak testleri kanonun
> güvenliğini ölçüyor, faydasını ölçmüyor. Elimizdeki güven, kapsadığı alanın
> yarısından geliyor."*

Yani fabrikanın *"doğru şeyi üretebildiği"* hiç ölçülmedi. Bugüne kadar ölçülen tek şey
yanlış şeyi üretmeyi reddettiği.

## Ortak `memory: project` denetimi deliyor

> *"PAD 'bu kuralı şu yüzden böyle yazdım' diye memory'ye not düşerse, PQA onu okur ve
> artık dosyaya değil gerekçeye bakar. Denetim biter. Ve ihlali sessiz: kimse memory'yi
> paylaşmaya karar vermedi, öyle geldi."*

Not: memory agent adıyla ayrışıyor (`.claude/agent-memory/<agent-adı>/`), yani teknik
karışma yok. Risk, ikisinin de aynı repoya yazması ve **memory'yi hiçbir denetimin
okumaması.** Clara bunu kurala bağlamayı önerdi, Mert: *"yok yazma."*

## Plandan sapmayı yakalayacak göz yok

> *"Boşluk bildirilmezse denetim zincirinde onu yakalayacak hiçbir göz yok — PQA planı
> değil dosyayı denetler, PAM revize turlarına girmiyor."*

`PAD-NO-SILENT-DEVIATION` bunu kurala bağlıyor ama kural agent'ın kendi bildirimine
dayanıyor; bildirmezse mekanizma yok.

## Ertelenmiş işler — hepsi aynı koşula bağlı

Neredeyse tamamı **"ilk gerçek takım kurulana kadar"**:

- v8'in yeniden ölçülmesi (adil sınav görmedi — kanonunun %91'ini görmemişti)
- Preload listesinin daraltılması (açılış maliyeti ~%15 context ≈ 30 bin token,
  21 bini skill)
- Kimlik öneki / namespace (8 takımda `BHV-NO-RUSH` çakışması gerçek risk ama
  ölçülmemiş ihtiyaca kural yazılmadı)
- PAM'in alan bilgisi toplama yöntemi (PCA body'sinde, ilk araştırmadan sonra skill'e
  terfi edecek)
- Fabrika ve CEO odası için hook (ikisi plugin değil; `CLAUDE.md`'ye açılış kuralı
  yazıldı, **denendi ve tutmadı** — agent kuralı gördü, *"devam edeceksek yükleyeceğim"*
  dedi. Mert: *"kalsın şimdilik böyle."*)
- Migration (164 bin kelime reference, ne kadarı gerekli bilinmiyor)

**Ve terfi hattı tanımlı ama koşmuyor:** *"Öneri kutusunda 40+ aday birikmiş, 'İşlenmiş:
henüz yok' yazıyordu. Terfi zinciri kuruldu ama koşmadı, çünkü kimse tetiklemiyordu.
Bu boşluk yeni değil, tekrarlıyor — ve bu sefer daha sinsi: bizde öneri kutusu bile
yok."*

## Açık kalan teknik sorular

**`SessionStart` matcher'ı** oturumun nasıl başladığını eşliyor (`startup|resume|clear|
compact|fork`), agent adını değil. `hooks.json`'da `"matcher": "ozel-yazilim:.*"`
yazılmış. Soru cevaplanmadı: eşleşmeyen matcher hook'u tamamen susturur mu, yoksa yok
sayılıp hook yine çalışır mı? *"Birincisinde telafi tamamen sessizce ölür."*

**AG'nin 16/16 doğrulaması nasıl yapıldı** — script doğrudan mı, hook zinciri üzerinden
mi? Doğrudansa matcher hiç sınanmamış olur. Soruldu, cevaplanmadı.

**GitHub issue'ları doğrulanmadı.** `#25834` gerçekten kapandı mı, düzeltme sürümü var
mı — *"eğer düzeltildiyse hook'a gerek kalmaz."* Oturumdaki şerh: *"bu linkleri ben
doğrulamadım, araştırmayı yapan agent getirdi."*

**`/doctor` + `/context` hiç koşulmadı** — 76 skill listeleme bütçesini taşırıyor mu.
İki kez teklif edildi, gerçek bir OY projesinde yapılması gerekiyor.

**Skill listeleme bütçesi context'in %1'i** ve taşınca **en az çağrılan skill'in
açıklaması düşürülüyor** → kendini besleyen sarmal: *"az çağrılan skill'in açıklaması
silinir → daha da az çağrılır → tamamen kaybolur."* 76 skill'lik kütüphane için
doğrudan risk, ölçülmedi.

**Kanıt eşiği yok.** `STD-GROUND-TRUTH` *"yaygınsa geçerli"* diyor, sayı vermiyor. Dış
sistemlerde de yok. *"Bu soruyu kimse çözmemiş, siz kendi eşiğinizi koymak
zorundasınız"* — konmadı.

**Kapıyı kim kapatsın — agent mı mekanizma mı?** Bugün QA push ediyor. Karşılaştırılan
sistemde CI kapatıyor, LLM yalnız yorum yapıyor. Cevaplanmadı.

## Kapanmamış kanon ihlali

`messaging/SKILL.md:40` örnek kodu `new HttpClient()` gösteriyor;
`data-access.md:49` bunu socket exhaustion gerekçesiyle yasaklıyor.
*"Örnek kod en çok kopyalanan şeydir."*

## Bu kayıttan çıkan tek sonuç

Fabrika **kâğıt üzerinde sağlam, sahada hiç sınanmadı.** Kendi kusurunu bulabildiği
ölçüldü (oturum-07 sayaç hatası), yasak tarafı direndiği ölçüldü — ama üretim tarafı,
bakım tarafı ve paketleme tarafı hiç denenmedi.

Ve oturumun kendi uyarısı duruyor: *"Riskli olan bu hâl değil, bu hâlin uzaması. Boşta
duran bir kanon zamanla gerçeklikten kayar ve kimse fark etmez."*
