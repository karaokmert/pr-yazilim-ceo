---
name: oturum-duzeni
description: Clara'nın oturum açılış ve kapanış düzeni — iki mod (EV / YÖNETİM), hangi modda hangi sırayla ne okunur, iş biterken ne yazılır ve hafızadan ne silinir. Bu skill'i her oturumun BAŞINDA aç — "nerede kaldık", "devam edelim", "ne yapıyorduk", "bugün ne var", "şu projede ne oluyor" denen her durumda, ve Mert bir projeyi adıyla andığında. Ayrıca oturum ya da bir iş kapanırken de aç — "kapatıyorum", "bu iş bitti", "günü kapatalım", "kapanış yapalım" denen durumlarda. Kapsam dışı — kanal kurma mekaniği (`kanal-kurulumu`), hangi bilginin nereye yazılacağı (`hafiza-duzeni`).
---

# Oturum düzeni

Bir oturum bağlam taşımadan başlar. Konuşma geçmişi yoktur, önceki oturumun ne yaptığı
bilinmez. **Açılış bir okuma işidir, bir çalışma işi değil.**

## Önce NEREDEYİM

İlk soru *"nerede duruyorum"* değil, **"bu oturumda ne yapıyorum"** — çünkü cevabı
açılış sırasını belirliyor ve iki mod var.

**EV — fikir olgunlaştırıyorsan.** İşin ölçmek, karşı argüman vermek, kanona yazmak.
Sprint burada planlanır, kararlar burada verilir.

**YÖNETİM — bir projede agent'ları yönetiyorsan.** Orada fikir olgunlaştırmıyorsun;
işin trafiği taşımak, durumu Mert'e getirmek, kanalı ayakta tutmak. Ve **o reponun
kanonu sana ait değil** — dosyalarına yazmadan önce onay alırsın
(`CLA-ASK-BEFORE-WRITING-OUT`).

### `pwd` ARTIK PROJEYİ VERİR — ilk sinyal budur

**Değişti 2026-08-13.** Clara kısayolu `cd /Users/karaok/p/pr-yazilim-ceo &&`
ile çağrılıyordu ve bu `cd` **gereksizdi** — agent tanımı `~/.claude/agents/clara.md`
symlink'iyle zaten global bulunuyor. O `cd` yüzünden `pwd` **hep aynı yeri**
gösteriyordu.

`cd` kaldırıldı. Ölçüldü aynı gün: `goat`'tan açılan Clara → `PWD=/Users/karaok/p/goat`.
Eskiden üç oturumun üçü de `pr-yazilim-ceo` diyordu, oysa ikisi CEO'da biri
`skill-project`'teydi.

**Açılışta ilk hareket:**
```bash
echo "AGENT=$CLAUDE_CODE_AGENT | PROJE=$(basename $(pwd))"
```

Bu **projeyi** verir. `pr-yazilim-ceo` ise büyük ihtimalle EV; başka bir proje
adıysa (`goat`, `egelisaglik`, `skill-project`…) **YÖNETİM.**

### Ama `pwd` mod'u tek başına KANITLAMAZ

Proje ≠ mod. Bir oturum `goat`'ta açılıp *"fabrikanın kanonuna bakalım"* diye
EV işine kayabilir; ya da `pr-yazilim-ceo`'da açılıp bir projeyi yönetebilir.

**Sıra:**
1. **`pwd`** — proje hangisi (birincil, artık güvenilir)
2. **Mert'in cümlesi** — bir projeyi adıyla mı andı, *"orada ne oluyor"* mu dedi
3. **`~/.pr-kanal/{proje}/`** — o projede kanal/defter var mı, açık agent var mı

İkisi çelişirse **Mert'in cümlesi kazanır** — mod onun niyetidir, dizinin değil.
**Hâlâ belirsizse sorulur**; varsayılmaz, çünkü yanlış mod yanlış açılış sırası
demektir.

**Ve `pwd` ikinci bir soruya daha cevap verir:** *"nereye yazabilirim."*
⚠️ Ama **kayıtlarının kökü sabittir** — hangi dizinden açılırsan açıl, `konular/`
ve `gunluk/` **`/Users/karaok/p/pr-yazilim-ceo`** altındadır. Başka bir projedeysen
oraya yazmak `CLA-ASK-BEFORE-WRITING-OUT` kapsamındadır (önce metni göster, onay al).

Ölçüm: `references/olcumler.md` → *"Beş sinyal, sıfır bağımsız ölçüm"* (eski durum,
`cd` kaldırılmadan önce)

## EV modu açılışı — üç adım

**Bir — `project_durum.md`'yi oku.** Hafızada duruyor ve tek satırlık bir işaret taşır:
son kapanış dokümanının adresi. Ayrıntı orada değil, **adres** orada.

**İki — kapanış dokümanını oku** (`gunluk/ev/{tarih}-kapanis.md`). Beş şey söyler: ne
bitti · ne yarım kaldı · Mert'in kararını bekleyen ne var · ölçüldü ama çözülmedi ne var
· bir sonraki hareket. Ölçütü şudur: **okuyup çalışmaya başlayabilmelisin.**

**Yalnız kendi modunun kapanışını oku.** `gunluk/` proje bazlı ayrışır
(`ev/` · `goat/` · `websitesi/` ...) ve açılış hook'u her projenin son kapanışını
ayrı listeler. Başka projenin kapanışı bu oturumun işi değildir — okunmaz,
**özetlenmez** (ölçüldü: tek akışta yeni oturum yanlış projenin durumunu özetledi).

**Üç — kanal KURMA.** ⚠️ Açılışta kanal kurulmaz (karar 2026-08-13).
Kanal yalnız **`/kanal` komutuyla** kurulur — Mert istediğinde.

Açık kutu görürsen **bilgi olarak not et, dokunma:** monitörler ölmüştür (oturum
kapanınca `Monitor` task'ı gider), ama dizin durur ve `STATUS.md` `STATE: OPEN`
yazar — hiçbir şey arızalı görünmez.

**Uyarı:** `STATUS.md`'deki `PID` canlılık kanıtı **değil** (`DURUM.md` DEĞİL —
o ad bir dönem kullanıldı, hook onu arıyordu ve hiç bulamıyordu; sessiz arızaydı).
Ölü kanal temizliği `/kanal` içinde yapılır.

## YÖNETİM modu açılışı — beş adım

**Bir — o projede kim açık?** `ps` ile agent oturumlarını tara: hangi rol, ne zaman
açılmış, hangi dizinde. Kimse yoksa iş henüz başlamamış.

**İki — kanal ne durumda?** `~/.pr-kanal/{proje}/` var mı, kaç kutu açık,
`live-channel.json` defteri var mı. ⚠️ **Ölç ama KURMA** — kanal `/kanal`
komutuyla kurulur, açılışta değil.

Kanal yoksa: Mert'e söyle (*"kanal yok, `/kanal` yazayım mı"*) ve **bekle.**
Kanalsız da çalışılır — o zaman handoff'ları Mert elle taşır.

**Üç — iş nerede kaldı?** Üç kaynak okunur: **o projenin kapanış dokümanı**
(`gunluk/{proje}/` altındaki en yenisi — hook adresini veriyor), kanal kutuları
(son mesajlar, kim ne demiş) ve agent'ların oturum kayıtları. Kanalda kapanış
satırı varsa iş bitmiş; yoksa yarım.

**Dört — Mert'e brief ver.** Onay brief'i biçiminde (`onay-brief` skill'i). Ve **karar
getir, rapor değil** — Mert o ekranları görmüyor.

**Beş — sonra bekle.** İş sıralaması Mert'le **birlikte** yapılır; kendiliğinden iş
başlatılmaz.

**Açılış buraya kadar.** Bundan sonrası — iş verme, zincir yürütme, denetim izleme,
kapatma — ayrı bir görevdir: **`proje-yonetimi` skill'i.** Orada zincirin sırası,
handoff taşıma ve *"kural dayatılmaz, iş anlatılır"* kuralı var.

## Açılışta yapılmayacak şey

**İşe başlamak.** Kapanış dokümanı okunmadan alınan karar, önceki oturumun kararını
bilmeden alınmış bir karardır.

## Kapanış — beş adım

İki tetiği var: **bir iş bitti** (zincir kapandı, çıktı denetlendi) ya da **oturum
kapanıyor** (Mert *"kapatıyorum"* dedi, uzun bir iş sona erdi).

**Bir — kalıcı olan ne varsa yazılır.** `CLA-WRITE-BEFORE-CLOSE` zaten emrediyor: bir
teşhis, bir ölçüt, bir karar gerekçesi, bir açık soru. **Yarım da yazılır.**

**İki — kapanış dokümanı yazılır** (`gunluk/{proje}/{tarih}-kapanis.md` — EV'de
`{proje}` = `ev`, YÖNETİM'de projenin adı: `goat`, `websitesi`...). Günlük dosyası da
aynı klasöre gider (`gunluk/{proje}/{tarih}.md`). **Klasör ayrımı atlanmaz** — kapanışlar
tek akışa yazıldığında sonraki oturum yanlış projenin durumunu özetliyor (ölçüldü,
2026-08-09: Goat için açılan Clara'ya EV'in push kuyruğu özetlendi). Beş bölüm: ne bitti
(commit hash'leriyle) · ne yarım kaldı (nerede, kimde, ne bekliyor) · Mert'in kararını
bekleyen (madde madde, her birinin **neden onun kararı olduğu**) · ölçüldü ama çözülmedi
· bir sonraki hareket (tek cümle).

Bu doküman **sonraki oturum için** yazılır, Mert için değil. Mert konuşmayı hatırlıyor;
sonraki oturum hatırlamıyor.

**Üç — hafıza temizlenir.** Biten işin `project` kaydı **silinir**, `MEMORY.md` satırı
kaldırılır. Yerine kalan: günlük + `HARITA.md` satırı + (varsa) `kararlar/` dosyası.

Ayrım tipe göre: **`user` ve `feedback` kalıcı** (Mert'in nasıl çalıştığı, düzeltilmesi
gereken bir davranış — iş bitince değer kaybetmez). **`project` geçici.**

Ölçüt: *bu kaydı silsem iki ay sonra bir şeyi bilemez miyim?* Cevap hayırsa — çünkü
günlükte var — sil. Cevap evetse o kayıt `project` değil; **tipini düzelt.**

Ölçüm: `references/olcumler.md` → *"Hafızanın %28'i bitmiş iş"*

**Dört — görev listesi kapatılır.** Açık kalan her satır sonraki oturumda *"bu neydi"*
sorusu üretir. Liste oturum-yereldir; taşıyıcı değildir.

**Beş — commit atılır.** Çalışma ağacı temiz bırakılır. Mert commit'ten inceliyor;
dağınık bir ağaç incelenemez.

## Kapanışta yapılmayacak şey

***"Sonra yazarım."*** Konuşma netleşerek bitmez — başka konuya kayar ya da gün biter.
