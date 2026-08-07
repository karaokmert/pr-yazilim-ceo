# Kaydın ömrü — ne zaman yazılmaz, ne zaman silinir

**Tarih:** 2026-08-07
**Karar mercii:** Mert
**Durum:** Kapalı

---

## Sorunu Mert koydu

> *"Repona çok fazla dosya var. Genel olarak ekosistemimizde çok fazla dosyaya yazma
> işi var. Kayıt yönetimini unutmayalım diye yazalım diyoruz ama okunamayan ya da
> taraması belli olmayan bir sürü bayat ya da eskimiş dosya üretiyoruz. Status'a yaz,
> gereksinime yaz diyoruz — agent 1 iş yaparken 10 yere kayıt atıyor. Bunu sende de
> görüyorum."*

---

## Ölçüm

**Yazma/okuma oranı:** bir günde **90 dosyaya yazıldı**, bir oturumda **10 dosya
okundu.**

**Geri dönülme:** `incelemeler/` + `kararlar/` altındaki 50 dosyanın **45'i tek
commit'lik** — yazıldı, bir daha dokunulmadı.

**Kayıt yeri sayısı: dokuz.** Ve biri (`.remember/`, 1 MB, otomatik yazıyor) kanonda
hiç anılmıyordu — günlükle çakıştığı ölçüldü.

**En büyük artık:** iki kanal deneyinin ham mesaj kutuları, **4.571 satır**. Bulgusu
üç ayrı yere işlenmişti (`fikirler/` deneyim · `kararlar/` mimari · `kanal-kurulumu`
skill'i ölçümler) — **ham girdi yine de silinmemişti.**

**Şişme:** `gunluk/2026-08-06.md` **2.983 satır**. Bir günde **yedi ayrı dosya**
açıldığı gün de var (08-07).

---

## Kök sebep

Kanonda **dört yazma tetiği** vardı, **sıfır kapanma tetiği.**

Her tetik bir dosya açıyor, hiçbiri kapatmıyor. Ham girdinin işlendikten sonra ne
olacağı hiç yazılmamıştı — bu yüzden duruyordu.

Mert'in tarifi doğru ama eksik: **asıl sorun "10 yere yazmak" değil, 10'un hiçbirinin
kapanmaması.**

Ve şu ayrım ortaya çıktı: **`kararlar/` ve `incelemeler/` temizdi.** 50 dosya, hepsi
haritada, hepsi bir karar ya da ölçüm. Sorun tamamen `gunluk/` altındaydı — yani
*"nereye yazılır"* kuralı çalışıyordu, eksik olan *"ne zaman kapanır"*.

---

## Karar — dört kural

**Bir — ham girdi işlendikten sonra silinir.** Deney çıktısı, kanal kutuları, tarama
dökümü: bunlar **girdi**, kayıt değil. Ayıran soru: *iki ay sonra biri açarsa,
çıkarılmış bulgudan fazlasını öğrenir mi?* Hayırsa artık; evetse bulgu eksik
çıkarılmış — önce o tamamlanır.

**İki — aynı olay iki yere yazılmaz.** `.remember` olay anlatısını zaten tutuyor.
Günlüğe yazılan şey olay değil, **bulgu.**

**Üç — bir günde ikinci dosya açılmaz.** O gün için zaten bir günlük var, başlık
eklenir. Ayrı dosya yalnız üç şey için: karar · fikir · aylarca dönülecek referans.

**Dört — kapanışta ölçülür.** *Bu iş kaç dosya açtı, kaçı hâlâ gerekli?* Gereksiz olan
**aynı anda** silinir; sonraya bırakılan temizlik yapılmıyor.

Ek: **günlük 1.000 satırı aşınca konsolide edilir** — taranamayan kayıt yok demektir.

---

## Sıra: önce kural, sonra temizlik

Mert'in kararı. Clara *"ham artıkları sileyim mi"* diye sordu, Mert **hayır** dedi:

> *"Dursun — önce kuralı yazalım."*

Gerekçe: silme bir **karara** dayanmalı, Clara'nın o anki seçimine değil. Kural önce
yazılırsa temizlik onun uygulaması olur ve bir dahaki sefere aynı ölçüt işler.

Bu ayrım kanonun kendi mantığıyla aynı: bir oturumda verilen izin kural yerine geçmez.

---

## Yer

Tetik ve ayıran sorular **body**'de (*"Ne zaman YAZMAZSIN"*), yöntem ve üç-tip-üç-ömür
tablosu **`hafiza-duzeni` skill**'inde (*"Kaydın ömrü"*), ölçümün tamamı
`gunluk/2026-08-07.md` → *"Kayıt envanteri"*.

---

## Açık kalan

**Ortak hafıza sorusu ertelendi** (Mert: *"önce doküman yapısını düzene sokalım, sonra
ortak memory kısmını değerlendirelim"*).

Ölçülmüş olan: agent memory ve repo dosyaları **taşınmıyor** — `agent-project`'te açılan
Clara'nın hafızası boş başlıyor. Taşınan tek şey knowledge graph, ama o da
`~/.npm/_npx/.../dist/memory.jsonl` içinde yani **npx paket önbelleğinde** duruyor
(silinebilir). Yedeği `~/.pr-memory/memory.jsonl` altına alındı; yapılandırmaya
dokunulmadı.
