# Eksen 1 — Teknik doğruluk

**Tarih:** 2026-08-06 · **Repo:** `/Users/karaok/p/agent-project`
**Yöntem:** isimsiz yardımcıya ölçüm verildi; her bulgu dosya:satır kanıtlı.
**Ölçüldü** (okundu değil): hook elle koşturuldu, atıflar `test -e` ile denendi,
index kimlikleri grep ile iki yönlü sayıldı.

## Sonuç — teknik kat büyük ölçüde sağlam

Kırık atıf **0**. Hayalet index kaydı **0**. Kayıt dışı kural **0**. Hook 4/4 agent'ta
doğru parse ediyor. Yani "teknik kırıksa mantık okunmaz" endişesi bu turda geçersiz —
mantık katmanı okunabilir durumda.

Sayılar:
- Atıf: 15 dosya yolu, 1 reference, 5 bölüm atıfı — hepsi var
- Frontmatter: 28 hücrenin 27'si dolu
- Index: 123 kimlik, iki yönde de sapma yok
- Hook: 4 agent koşuldu, skills listesi birebir doğru basıldı

## Bulgu 1 — `atif_verenler` alanı %74 boş (en ağır teknik bulgu)

`rules-index.json`'da 123 kuralın **112'sinde `atif_verenler` boş.** Ama gövdelerde
başka bir yerden anılan **38 tekil kimlik** var ve bunların **28'i index'te atıfsız.**

Örnekler: `YT-FILTER-BEATS-LIST` dört yerden anılıyor (`yapi-taslari/SKILL.md:331`,
`arac-envanteri.md:285,302,325`) — index'te liste boş. `PAD-TEST-BEFORE-HANDOFF` üç
yerden (`pr-agent-developer.md:105`, `is-duzeni/SKILL.md:187,363`) — boş.
`YT-ASSUME-BACKGROUND` üç yerden — boş. `DAG-MATCH-HOOK-FORMAT` iki yerden — boş.

**Neden ağır:** index kendi `ne_ise_yarar` alanında *"atif_verenler listesi cascade'in
haritasıdır"* diyor. Ve `pr-agent-qa.md:40-41` bunu bir **denetim ekseni** sayıyor
(*"atıf listeleri gerçeği gösteriyor mu"*). Yani bir kural değiştirileceğinde
"kimler etkilenir" sorusu index'ten cevaplanamıyor — cascade elle grep gerektiriyor.

Bu doğrudan **dördüncü ölçütü (bakım kabiliyeti)** vuruyor: *"6 ay sonra behavior'da
bir şey değiştirmek istiyorum, tüm takımlarda yapılmalı kararı alabiliyor muyuz?"*
Bugünkü cevap: haritaya bakarak hayır.

PCA bunu zaten biliyor (`pr-agent-context-analyst.md:86`: *"rules-index.json başlangıç
noktasıdır, kesin cevap değil"*) — ama index'in kendi beyanı ve PQA'nın denetim ekseni
bundan fazlasını iddia ediyor.

**Ek kusur — alan iki tipte veri taşıyor.** Dolu 11 kaydın bazısı dosya yolu, bazısı
`dosya — bölüm` bileşiği, bazısı ise **dosya değil kimlik** (`ISD-KEEP-STATUS` →
`['ISD-APPEND-DONT-REWRITE']`). Bileşiklerden biri doğrulanamadı:
`uretim/SKILL.md — kural yazımı bölümü` — dosyada "Kural biçimi" başlığı var (satır 26),
"kural yazımı" adlı bölüm yok.

## Bulgu 2 — PQA denetleyeceği kanonu elinde bulundurmuyor

`pr-agent-qa.md:30` denetim eksenini tanımlıyor: *"üretilen şey `behavior`,
`is-duzeni`, **`yapi-taslari`** ve kendi alanının kanonuyla çelişiyor mu."*

Ama `pr-agent-qa.md:5-8` — PQA'nın `skills:` listesi: behavior, is-duzeni, uretim.
**`yapi-taslari` yok.** Hook da onu basmıyor (elle koşturuldu, doğrulandı).

Yani denetçiye ölçüt olarak gösterilen kanon ne frontmatter'da ne hook çıktısında.
PQA `BHV-OPEN-SOURCE` gereği elle açabilir, ama body'si ona *"bu senin preload'ında"*
izlenimi veriyor.

## Bulgu 3 — hook'ta latent kırılganlık (fiilî arıza değil)

awk parser üç sentetik dosyayla sınandı. YAML **akış biçimi** (`skills: [behavior,
dagitim]`) **hiçbir şey döndürmüyor** — regex `/^skills:[[:space:]]*$/` satır sonu
istiyor.

Bugünkü 4 dosyanın hiçbiri o biçimi kullanmıyor, yani şu an çalışıyor. Ama biri
listeyi geçerli YAML akış biçiminde yazarsa hook sessizce boş basar ve hata vermez.
İhlali sessiz.

**Ayrıca hook'un `CAKISAN` dalı hiç sınanmadı** — `~/.claude/skills/` bugün boş
(2026-08-04'te temizlendi), o yüzden 4 koşumun hiçbiri o kod yolundan geçmedi.
Kod doğru kurulmuş görünüyor ama ölçülmemiş durumda.

## Bulgu 4 — PAM'de `tools:` yok, ve bu bilinçli

`pr-agent-manager.md` frontmatter'ında `tools:` satırı hiç yok (diğer üçünde var).
Kaza değil: `pr-agent-manager.md:134-137` gerekçelendiriyor — *"araç listesi bir niyet
beyanıdır, filtre uygulanmadan bağlayıcı değildir."* `arac-envanteri.md:329-330` de
kullanıcı kararı olarak kaydediyor (2026-08-04, elle silindi).

**Ama 3. işe etkisi var:** o iş PAM'den `Task` yetkisini almayı öngörüyor. `tools:`
satırı olmadığı için alınacak bir liste yok — kısıt sıfırdan yazılacak.

**Ve beyan disiplini tek biçimli değil:** aynı gerekçe geçerliyse PAD'in `Task`'ı da
listede olmak zorunda değildi, yine de yazılmış.

## Açık kalem — ölçülmedi

Hook'un asıl sorusu **hâlâ açık:** `CLAUDE_CODE_AGENT` gerçek bir alt-agent turunda
dolu mu? Elle koşturmada değişken **biz verdik**, yani hook'un mantığı doğru çalışıyor
— ama Claude Code'un o değişkeni alt-agent'a geçirip geçirmediği ölçülmedi.

Mert'in kararı (2026-08-06): PAM'i **Mert açacak**, açılışta ne gördüğü sorulacak.
