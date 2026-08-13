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

### Ayrımı `pwd` VERMEZ

Clara `pr-yazilim-ceo`'da **kurulu** bir agent ve her projede çalışabilir. `pwd`
oturumun konusunu değil **başlatan `cd`'yi** gösterir — yani onun için neredeyse sabit.

Arıza sessiz: `pwd` her oturumda *"EV"* der, yönetim moduna hiç geçilmez.

**Penceren ölçülebilir — IDE'ye canlı sor.** Mert seni hangi VS Code penceresinden
başlattıysa oradasın, ve bunu pencerenin kendisi söyler: `mcp__ide__getDiagnostics`
çağrısı açık dosyaların yollarını döner — hangi projenin altındalarsa pencere o
projededir. Kaynak pencerenin kendisi ve zaman *şimdi*; bu yüzden hatasız. Yedek:
`GEMINI_CLI_IDE_WORKSPACE_PATH` env değişkeni — ama iki zayıflığı var: onu yazan başka
bir eklenti (kaldırılırsa sinyal sessizce gider) ve oturum başında donmuş (pencere
değişse haberi olmaz). Sıra: **önce IDE'ye canlı sor, env yedek, `pwd` hiç.**

**Pencere mod'u verir ama konuyu vermez.** Pencere ölçümü *"neredeyim"i* kapatır;
*"bu oturum ne hakkında"* hâlâ Mert'in niyetidir — ölçülmez, söylenir. Üç şeye bakılır:
Mert ne dedi (bir projeyi adıyla andı mı, *"orada ne oluyor"* diye mi sordu) ·
`~/.pr-kanal/` altında hangi projede açık kutu var · o projede açık agent oturumu var
mı. **Belirsizse sorulur** — varsayılmaz, çünkü yanlış mod yanlış açılış sırası demektir.

**`pwd` yine okunur, ama başka soru için:** *"nereye yazabilirim."* `pr-yazilim-ceo`
içindeysen kendi kanonun serbest, dışına yazmak onaya tabi. Yani `pwd` yazma sınırını
verir, **mod'u vermez** — ikisi ayrı soru, tek ölçütle cevaplanmazlar.

Ölçüm: `references/olcumler.md` → *"Beş sinyal, sıfır bağımsız ölçüm"*

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
