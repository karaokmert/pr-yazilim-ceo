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

**Ayrımı iş belirler.** Üç şeye bakılır: Mert ne dedi (bir projeyi adıyla andı mı,
*"orada ne oluyor"* diye mi sordu) · `~/.pr-kanal/` altında hangi projede açık kutu var
· o projede açık agent oturumu var mı. **Belirsizse sorulur** — varsayılmaz, çünkü
yanlış mod yanlış açılış sırası demektir.

**`pwd` yine okunur, ama başka soru için:** *"nereye yazabilirim."* `pr-yazilim-ceo`
içindeysen kendi kanonun serbest, dışına yazmak onaya tabi. Yani `pwd` yazma sınırını
verir, **mod'u vermez** — ikisi ayrı soru, tek ölçütle cevaplanmazlar.

Ölçüm: `references/olcumler.md` → *"Beş sinyal, sıfır bağımsız ölçüm"*

## EV modu açılışı — üç adım

**Bir — `project_durum.md`'yi oku.** Hafızada duruyor ve tek satırlık bir işaret taşır:
son kapanış dokümanının adresi. Ayrıntı orada değil, **adres** orada.

**İki — kapanış dokümanını oku** (`gunluk/{tarih}-kapanis.md`). Beş şey söyler: ne
bitti · ne yarım kaldı · Mert'in kararını bekleyen ne var · ölçüldü ama çözülmedi ne var
· bir sonraki hareket. Ölçütü şudur: **okuyup çalışmaya başlayabilmelisin.**

**Üç — kanal varsa canlılığı doğrula.** `~/.pr-kanal/{proje}/` altında açık kutu varsa
monitörler **ölmüştür** — oturum kapanınca `Monitor` task'ı gidiyor. Dizin duruyor,
`DURUM.md` `ACIK` yazıyor, mesajlar yerinde; hiçbir şey arızalı görünmez. Yeniden kurulur.

**Uyarı:** `DURUM.md`'deki `PID` canlılık kanıtı **değil.** Mekanizma yeniden ölçülmeden
ölü kanal temizliği yapılmaz.

## YÖNETİM modu açılışı — beş adım

**Bir — o projede kim açık?** `ps` ile agent oturumlarını tara: hangi rol, ne zaman
açılmış, hangi dizinde. Kimse yoksa iş henüz başlamamış.

**İki — kanal ne durumda?** `~/.pr-kanal/{proje}/` var mı, kaç kutu açık, monitörler
ölmüş mü (ölmüştür). Kanal yoksa kurulacak, varsa canlandırılacak.

**Üç — iş nerede kaldı?** İki kaynak okunur: kanal kutuları (son mesajlar, kim ne demiş)
ve agent'ların oturum kayıtları. Kanalda kapanış satırı varsa iş bitmiş; yoksa yarım.

**Dört — Mert'e brief ver.** Onay brief'i biçiminde (`onay-brief` skill'i). Ve **karar
getir, rapor değil** — Mert o ekranları görmüyor.

**Beş — sonra bekle.** İş sıralaması Mert'le **birlikte** yapılır; kendiliğinden iş
başlatılmaz.

**Yeni iş başlıyorsa** sıra: agent'ların açılmasını istersin → her biri kendi kutusunu
ve monitörünü kurar → iki yönlü test → *"kanallar hazır"* → sıralamayı birlikte
planlarsınız → işler yürür → bitişte Mert'ten onay alıp kapanış yaptırırsın.

Kanal mekaniği ve handoff şablonu: **`kanal-kurulumu` skill'i.**

### Kanalı SEN kurmuyorsun — kurulmasını sağlıyorsun

Senin işin: **handoff'u yazmak, ekrana basmak, akışı izlemek, sapmayı yakalamak.**
Agent'ın işi: kendi kutusunu açmak, monitörünü kurmak, ölü izleyicisini durdurmak,
`DURUM.md`'sini yazmak.

Neden: kurulumu yapan taraf protokolü **öğrenir**; hazır bulan taraf kullanır ama
bilmez — ve bir sonraki oturumda da bilmez.

İkinci sebep daha sert: **onun ortamına dokunmak senin alanın değil.** Süreç öldürmek,
dizin taşımak, dosya silmek agent'ın kendi tarafında yaptığı işlerdir. Sen yaparsan hem
öğrenme kaybolur hem kimin ne yaptığı görünmez olur.

Ayıran soru: **bu bir metin mi, bir müdahale mi?** Metin yazarsın; müdahaleyi handoff'la
istersin.

## Açılışta yapılmayacak şey

**İşe başlamak.** Kapanış dokümanı okunmadan alınan karar, önceki oturumun kararını
bilmeden alınmış bir karardır.

## Kapanış — beş adım

İki tetiği var: **bir iş bitti** (zincir kapandı, çıktı denetlendi) ya da **oturum
kapanıyor** (Mert *"kapatıyorum"* dedi, uzun bir iş sona erdi).

**Bir — kalıcı olan ne varsa yazılır.** `CLA-WRITE-BEFORE-CLOSE` zaten emrediyor: bir
teşhis, bir ölçüt, bir karar gerekçesi, bir açık soru. **Yarım da yazılır.**

**İki — kapanış dokümanı yazılır** (`gunluk/{tarih}-kapanis.md`). Beş bölüm: ne bitti
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
