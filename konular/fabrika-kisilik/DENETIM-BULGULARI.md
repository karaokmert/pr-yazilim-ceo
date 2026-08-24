# Fabrika denetim bulguları — 2026-08-24 03:35

Dört bağımsız denetim (`plugin-dev:agent-development` + `plugin-dev:skill-development`
standartlarıyla). **Clara'nın kendi okuması yetmedi** — `⚠️` işaretlerine bakıp
"temiz" dedi; denetim cümle SINIFINA baktı ve 14 ihlal buldu.

**Mert'in kararı (03:40):** *"Bu işleri sıraya al, bitti dedikçe verirsin."*
**Ve:** *"Vizyon kalsın, korkuya gerek yok."*

---

# SIRA

| # | İş | Durum |
|---|---|---|
| **1** | `uretim` gövde standardı: dört parça → altı grup | **GÖNDERİLDİ** 03:41 |
| 2 | Gövdelerdeki 14 saflık ihlali (FPD 5, FQA 9) | bekliyor |
| 3 | Gelişim yetkinliği + vizyon üç gövdeye | bekliyor |
| 4 | `docs/tasks` ↔ `docs/isler` çelişkisi — **yön: `tasks`** | bekliyor |
| 5 | İki kırık atıf (`is-duzeni` → `davranis`) | bekliyor |
| 6 | `fabrika-davranis` vaka fazlalığı | bekliyor |

**Sıra gerekçesi:** gövde standardı düzelmeden gövdeler yeniden yazılamaz — aynı
eksik tarife göre yazılırlar.

---

# 1 · uretim gövdeyi DÖRT parça sayıyor (EN AĞIR)

`skills/uretim/SKILL.md:59-61` — *"Gövde dört şey yapar..."*

Ölçüldü: fabrika deposunun tamamında **"altı grup", "vizyon", "gelişim
yetkinliği" sıfır sonuç.** Ve `takim-kurulumu:52,71-72` gövde tarifini bütünüyle
`uretim`'e devretmiş → fabrikada gövde standardının tek adresi orası.

⚠️ **Sonuç:** gövdelerde gelişim/vizyon eksikliği unutma değil, **standardın
onları hiç tanımaması.** Fabrikanın ürettiği her takımın her gövdesi bu tarife
göre yazılıyor.

⚠️ **Clara'nın payı:** iş emrine "kapsam içi" diye koydurdum ama üretim standardını
kontrol etmedim. Kapsamı doğru yazmak yetmiyor — standardın onu tanıyıp tanımadığı
ayrı bir ölçüm.

---

# 2 · Gövdelerde 14 saflık ihlali

Ölçüt (`uretim:75-79`): **"okuyan agent bunu kendisi hakkında ne sanır?"**
— *"bu cümle zamanla yanlış olur mu"* DEĞİL. Gövdeye yazılan teşhis hiç
bayatlamayabilir; her oturumda agent'a kendini eksik tanıtır.

## FPD — 5 ihlal
| Satır | Sınıf | Alıntı |
|---|---|---|
| 21-24 | gerekçe zinciri + risk | *"standardın son noktası sensin... her oturumuna girer"* |
| 40-41 | risk uyarısı | *"sahada agent'ın donduğu yerdir"* |
| 46-48 | **bilişsel teşhis** | *"kendi yazdığını okurken ne demek istediğini biliyorsun"* |
| 55-57 | tasarım savunması | *"senin elinde ayrı bir ağırlığı var"* (21-24'ün tekrarı) |
| 69-71 | gerekçe zinciri | FQA'nın yöntemini açıklıyor |

## FQA — 9 ihlal
| Satır | Sınıf | Alıntı |
|---|---|---|
| **20** | **TEŞHİS — en ağır** | *"hatanı yakalayacak kimse yok"* |
| 17-18 | gerekçe | *"gerekçeyi okuyan göz haklı bulmaya meyleder"* |
| 25-27 | tasarım savunması | kıdemsiz/kıdemli karşılaştırması |
| 30-31 | gerekçe (analoji) | *"bir kanunda tek maddeyi okumak"* |
| 34-35 | gerekçe + meta-yorum | *"İkincisi kişilik değil yöntemin korunması"* |
| 41-42 | **teşhis** | *"yavaş olsan da... frenleyen tek kişi sensin"* |
| 48-49 | gerekçe/risk | *"taranmış sanılır"* |
| 58-60 | gerekçe zinciri | *"düzeltecek kanal bulunmaz"* |
| 69-70 | tasarım savunması | *"FPD ile ikizsiniz"* |

⚠️ **FQA:20, `uretim:73-74`'ün YASAK ÖRNEĞİNİN neredeyse birebir kopyası**
(*"Yanıldığını kimse yakalayamaz"*). Kural yazıldı, ihlali aynı depoda duruyor.

**FPA temiz** — içerik saflığında ihlal yok.

## Ek: karakter/meslek ayrımı FQA ile FPD arasında TERS
Aynı bilgi (*"listeye bakmam, sıfırdan tararım"*) FQA'da **karakter** (s.37-38),
FPD'de **meslek** (s.69-71). Aynı desen *"sınırını yazarsın"* çiftinde tekrar
ediyor — tek seferlik kayma değil, sistematik.

---

# 3 · Gelişim yetkinliği + vizyon

**Üç gövdede de birebir aynı üç cümle** ve fiil **"okursun"** — yazma yönü yok.
Söylenmiyor: düzeltme geldiğinde ne yapacağı · onay aldığında ne yapacağı · bir
hatayı bir kez nasıl yapacağı.

**Vizyon: yalnız "ne olmak istediği."** Mert'in kararı — korku yarısı ile
*"gövdede risk uyarısı yaşamaz"* kuralı birbirini kesiyordu; gerilim vizyonu
daraltarak çözüldü.

---

# 4 · docs/tasks ↔ docs/isler ÇELİŞKİSİ

| Dosya | Ne diyor |
|---|---|
| `fabrika-davranis:126,130-131` | `docs/tasks/{görev}/` |
| `fabrika-is-duzeni:57-63` | `docs/isler/{is-adi}/` |
| `planlama:59,198` | `docs/isler/` |

**Diskte `isler/` VAR, `tasks/` YOK.** Üç rol de `fabrika-davranis`'ı her oturumda
yüklüyor → yanlış yol her oturum okunuyor.

## ✅ MERT'İN KARARI (03:42) — yön: `tasks`

> *"4. `tasks` olarak olsun, `isler` olmasın."*

Yani çelişki **`fabrika-davranis` lehine** çözülüyor:
- `fabrika-is-duzeni:57-63` → `docs/isler/{is-adi}/` yerine `docs/tasks/{görev}/`
- `planlama:59,198` → aynı düzeltme
- **Diskteki `docs/isler/` klasörü de taşınacak** — yalnız metin değişikliği değil

⚠️ **Clara'nın payı:** bu benim gereksinimimden geldi. Mert `docs/tasks/{görev}`
dedi, ben olduğu gibi aktardım, **mevcut düzenle çakışıp çakışmadığını kontrol
etmedim.**

Ayrıca ikinci ayrışma: `davranis` nihai raporu `docs/{iş}/` altına yazdırıyor,
`is-duzeni:68` biten klasörü `docs/trash/`'e taşıtıyor.

---

# 5 · İki kırık atıf

`fabrika-is-duzeni:73` — *"Taşınır, silinmez — gerekçesi `fabrika-davranis`'da."*
`fabrika-is-duzeni:129-130` — *"boşaltmayı kullanıcı topluca yapar
(`fabrika-davranis`)."*

**Hedefte yok.** "Silinmez", "boşaltma", "topluca" kelimelerinin hiçbiri
`fabrika-davranis`'ta geçmiyor.

⚠️ `uretim:340-352` bu arıza sınıfını adıyla tarif ediyor ve *"üç ardışık kapatma
turunun üçünde de yeni kırık atıf doğdu"* diyor. **Kanon kendi uyardığı desene
yeniden düşmüş.**

---

# 6 · fabrika-davranis vaka fazlalığı

**12 vaka anlatısı**, üçü aşım:
- **187-192 (en ağır):** beş ayrı olay, altı satır, **sıfır talimat.** Kural bir
  üst paragrafta zaten tam yazılı (s.184).
- **217-221:** iki vaka, beş satır; kural 212-215'te tam, 223'te kapanıyor
- **26-32:** iki vaka aynı hükmü destekliyor, biri yeter

**"Ölçüldü:" kalıbı 6 kez** — altıncısı birincinin ağırlığını taşımıyor.

**Ayırt edici ölçüt (denetimden):** kural + kısa neden = **gerekçe** (istenen);
geçmiş zamanlı olay anlatısı = **vaka** (fazla).

**Öneri:** "Bir şeyin nerede geçtiğini bulmak" (158-200, 43 satır — dosyanın en
uzun bölümü) `references/arama.md`'ye taşınsın.

## Ve kapatılmamış boşluk
`davranis:45` — *"ürettiğin takımı tanımak buraya girmez"* diyor ama **nereye
gireceğini söylemiyor.** Hafıza bölümü üç tür sayıyor, hiçbiri bunu karşılamıyor.
Fabrika sürekli takım üretiyor — kenar durum değil ana iş.
⚠️ Dosyanın kendi ilkesine (*"yasak değil disiplin yazılır"*) aykırı tek yer.

---

# Kapsam sızması — is-duzeni hükmü davranis'ta

`davranis:208-210` `fabrika-is-duzeni:87-89`'un kısaltılmışını taşıyor (hüküm +
gerekçe + atıf). Atıf verilecekse hüküm verilmemeli.

⭐ **Aynı dosya bunu 116-117'de DOĞRU yapıyor:** sınır cümlesi + atıf, hüküm yok.
Disiplin dosyada mevcut, bir yerde uygulanmamış.

---

# TEMİZ ÇIKANLAR

- Frontmatter: üç gövdede de temiz (name/model/memory/skills/color)
- Uzunluk: FPA 4.394 · FPD 4.696 · FQA 4.454 karakter (sınır 10.000)
- Çapraz tutarlılık: iletişim modu · bire bir mesajlaşma yasağı · görev sıralaması
  · hafıza katmanları — dördü de tek kaynak + atıf deseniyle doğru kurulmuş
- Ölü skill atfı yok
- FPA gövdesi içerik saflığında temiz
