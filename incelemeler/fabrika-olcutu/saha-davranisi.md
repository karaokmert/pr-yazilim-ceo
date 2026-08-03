# Fabrika sahada nasıl çalıştı — vizyonla karşılaştırma

Tarih: 2026-08-03 (gece)

Mert sordu: *"Fabrikanın konuşmalarını oku — ne yapıyorlar, vizyona uygun mu
ilerliyorlar?"*

Ölçüt `kayit.md`'de duruyor (dört şart, Mert'in kendi cümlelerinden). Bu dosya
fabrikanın **fiilî davranışını** o ölçütle karşılaştırıyor.

## Kaynak ve yöntem

`~/.claude/projects/-Users-karaok-p-agent-project/` — 41 oturum tarandı (`git log`
değil, oturum kayıtları). Beş büyük oturum satır satır okundu, toplam ~4.700 satır.

Önce bir sayım yapıldı: hangi oturumlarda `Task`/`Agent` ile ekip personeli çağrılmış.
Sonuç: **41 oturumun 2'sinde.** Bu iki oturum ayrıntılı incelendi
(`90eeb9a2`, `58749256`), ayrıca üç büyük iş oturumu (`b34a383a`, `fedec8f1`,
`3fa67e0d`).

## Zincir çalıştı — ve iyi çalıştı

İlk sayım yanlış yorumlanabilirdi (*"2/41, zincir işlemiyor"*). Ölçüm tersini gösterdi:
zincir iki kez döndü ve **ikisinde de düzgün döndü.**

`58749256` oturumu (2026-08-03 akşamı) tam alternasyon yaptı: PAM → PAD → PQA → PAD →
PQA → PAD → PQA → PAD → PQA → PAD → PQA. **Beş PAD turu, beş PQA turu.**

**11 çağrının 11'i yapılandırılmış devir bloğuyla** başladı — `KİMDEN → KİME`, `TÜR`,
`NE`, `NEDEN`, `NEREYE BAK`, `BEKLEDİĞİM`. Serbest metin yok. Push çağrısında ayrı bir
`KULLANICI ONAYI` alanı ve Mert'in birebir cümlesi vardı (*"b onaylıyorum"*), PQA
bunu doğruladı: *"varsaymadım, bloktan okudum."*

**Beş denetim turu, dördü RED, toplam 7 bulgu.** Hiçbir tur *"onaylandı"* diye geçmedi.

PQA'nın en değerli yakalaması üçüncü turda: PAM işi *"kapandı"* diye gönderdi, PQA
commit eksiğini buldu —

> *"Working tree'de `rules-index.json` değişik, staged alan boş. Onay gelip push atarsam
> sahaya inen şey PAD'in düzelttiği hüküm değil, benim iki tur önce reddettiğim bayat
> hüküm olur. Dosya diskte doğru görünür. Bu ayrımı kimse fark etmez, çünkü herkes
> çalışma ağacını okur."*

PAM bunu üzerine aldı: *"Bu bulguyu ben kaçırdım ve kayda geçti."*

PQA hiçbir yerde beyanı kanıt saymadı — `git show`, `git log -S`, JSON parse, karakter
karşılaştırma ile ölçtü. Ve kendi sınırını korudu: *"Denetlediğim dosyaya dokunmadım
(`PQA-NO-FILE-EDIT`), çözüm önermedim (`PQA-NO-PROPOSE-FIX`)."*

**Kural ihlali bulunamadı.** PAD plan dışına yazmadı; yazma bloklandığında dolanmayı
denemedi ve yarım işi devretmedi (*"cascade yarım, PQA'ya devretmiyorum, PAM'a
dönüyorum"*). Commit PAD attı, push PQA attı — doğru bölüşüm.

PAD `general-purpose` çağırdı (7 kez) ama bu kanon gereği: yazdığı kuralı isimsiz
yardımcıya okutup davranış sınaması. Ve gerçek bulgu üretti: *"5 durum soruldu, biri
YANLIŞ çıktı. Suçlu metnimdi."*

## Kendi kusurunu bulma refleksi çalışıyor

Üç ayrı örnek, üçü de kimse söylemeden:

**PAD kapanışta:** *"PQA'nın denetlediğini göremiyorum, onun transkriptinde değilim.
'Denetimden geçti' yazmam beyanı kanıt saymak olurdu."*

**PQA ikinci turda:** kendi ürettiği bulgunun düzeltmesinde yeni bir bulgu buldu —
*"Bulgu 1 ve 2'nin düzeltilmesi sırasında aynı ayrışma bir kez daha üretildi, bu kez
ters yönde."*

**PQA daha önce (`fedec8f1`):** `ISD-KEEP-CHAIN-ONE-DEEP` hükmünün **sahayı yanlış
tarif ettiğini** ölçtü — hüküm *"`Task` yalnız PAM'de durur"* diyordu, ölçüm `Task`'ın
PAD'de de olduğunu gösterdi. Kural aynı gün düzeltildi (araçtan davranışa:
*"Personeli yalnız PAM çağırır"*).

**Ve PAM kendi hatasını dokümandan düzeltti:** push sonrası `WebFetch` ile subagent
dokümanını okudu ve *"sana 'sub-agent'lar yalnız arka planda çalışıyor' dedim, yanlış —
arka plan varsayılan ama zorunlu değil. Yani bu oturumdaki beş turluk karanlığı
önleyebilirdim"* dedi.

## Ölçütle karşılaştırma — dört şart

### Kestirmeden yapmama: ✅ karşılanıyor, hatta fazlasıyla

Beş turluk revize döngüsü, her turda ölçüm, hiçbir turda *"yeterince iyi"* denmedi.
Ama bunun bir bedeli var ve Mert onu söyledi:

> *"Baksana minik bir iş 2 saatimizi aldı, bu böyle olur mu hiç?"*

PAM savunmadı: *"Haklısın ve bunu savunmayacağım. Beş ayrı iş, dokuz commit. Bunlar
'minik iş' değildi — ama minik bir iş gibi başladılar, ve bence asıl problem bu."*

Yani şart karşılanıyor ama **iş kapsamının başta doğru ölçülmesi** ayrı bir boşluk.

### Bakım kabiliyeti: ⚠️ kısmen — refleks var, mekanizma yok

Fabrika bugün kendi kanonundaki üç hükmü düzeltti, biri sahayı yanlış tarif ettiği için.
Yani **kendi bakımını yapabiliyor.**

Ama filo bakımı (8 takım senaryosu) hâlâ sahipsiz — bkz. `zayif-noktalar.md`. Ve daha
somut bir kayıp var, `3fa67e0d` oturumunda tespit edilip iki gün sonra doğrulandı:

> *"Gerçek kayıp: öz-denetim komutları. Eski AG'de `AG-SELF-AUDIT-RUN` vardı — 'düzeni
> koruyan şey senin dikkatin değil, çalıştırdığın komut; dikkat yorulur, komut
> yorulmaz.' Bugün böyle bir şey yok. `.claude/` altında tek bir script yok."*

Doğrulandı: PQA index senkronunu **elle** Python one-liner'larıyla ölçtü, PAD index'i
`/tmp/index-guncelle.py` gibi tek kullanımlık script'lerle güncelledi. Bugün tuttu —
*"ama tutmasının sebebi kapı değil dikkat."*

### Sıfırdan üretme: ❌ hiç sınanmadı

**`team/` klasörüne bugüne kadar hiç commit atılmamış.** `git log -- team/` boş.
`team/team-1-oy/` var ama git'te izi yok.

Ölçülen üç büyük iş oturumunun **üçü de fabrikanın kendi yapılanmasıydı:**
- `b34a383a` (2,2 MB) — açılış hook'u + kendi personel body'leri + `CLAUDE.md`
- `fedec8f1` (1,2 MB) — aynı işin denetimi
- `58749256` (1,2 MB) — bağlam dosyası yetkisi (yine kendi kanonu)

Değişen her dosya `.claude/` ya da `docs/fabrika/` altında. Mert'in kendi kapsam
cümlesi bunu doğruluyor: *"Kapsam `.claude/skills/` ile sınırlı — `team/` altı dışarıda
kalmalı."*

Yani ana ölçüt — *"OY v8 hiç olmasaydı onu üretecek adımları bilmek"* — **hiç
denenmedi.** Fabrika adımları yazdı, 121 kurala bağladı, ama bir kez yürümedi.

### Alan bağımsızlığı: ❌ ölçülemez

Fabrika yalnız kendi üstünde çalıştı; farklı bir alanda (marketing, oyun, n8n) hiç
sınanmadı. Bu şart sıfırdan üretme denenmeden ölçülemez.

## PCA hiç çağrılmadı

İki zincir oturumunun ikisinde de `pr-agent-context-analyst` **tool çağrısı yok.**
Metinde 400'den fazla anılmış, bir kez çalıştırılmamış.

Bu bir ihlal değil ama bir işaret: dört personelin biri hiç iş görmedi. Kuruluşta
Mert'in şerhi vardı — *"dörtlüye ihtiyacımız var ama asla doğru kabul etme"* ve
Claude'un önerisi *"üçle başla, dördüncüyü ölçerek ekle"* idi. Dördüncü eklendi,
ölçüm yapılmadı.

## Harness kaynaklı iki kayıp

**`Task` oturum içinde aktifleşmiyor.** `90eeb9a2`'de PAM'in frontmatter'ına `Task`
eklendi ama oturum başında yüklenen araç listesi değişmedi:
*"Frontmatter değişikliği çalışan oturumda etkili olmuyor."* Sonuç: o oturumun
tamamı elle yürüdü — PAM 6 blok bastı, Mert taşıdı.

**`SendMessage` çalışmadı** (`"exists but is not enabled in this context"`). PAM
PAD'i devam ettirmek yerine her turda **yeni agent** açmak zorunda kaldı — beş turluk
döngünün her turu taze context. Bu, iki saatlik sürenin bir sebebi.

## Sonuç — fabrikanın sorunu kalite değil

Ölçülen davranış vizyonla **uyumlu**: zincir düzgün dönüyor, denetim gerçek bulgu
üretiyor, roller birbirine karışmıyor, kendi kusurunu buluyor, beyanı kanıt saymıyor.
Bunlar taklit edilemez şeyler — kanon davranışa dönüşmüş.

Uyumsuz olan tek şey **nerede çalıştığı.** Fabrika 121 kural, sekiz commit, üç kanon
düzeltmesi üretti ve hepsi kendi üstüne. `team/` boş.

Yani teşhis: **fabrika iyi kurulmuş, hiç saha görmemiş.** Ve kuruluş oturumunun kendi
uyarısı duruyor:

> *"Riskli olan bu hâl değil, bu hâlin uzaması. Boşta duran bir kanon zamanla
> gerçeklikten kayar ve kimse fark etmez."*

## Sıradaki adım — karar bekliyor

En küçük gerçek iş `team/` altına bir takım paketlemek. Bir hamlede dört şeyi birden
sınar: sıfırdan üretme adımları, `dagitim` skill'inin 20 kuralı (sıfır test), push
kapısı, ve alan bağımsızlığı (OY dışı bir alan seçilirse).

İkinci aday: öz-denetim script'i (`AG-SELF-AUDIT-RUN`'ın karşılığı) — çünkü bugünkü
denetim dikkate dayanıyor ve dikkat yorulur.
