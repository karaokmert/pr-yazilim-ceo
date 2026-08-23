---
name: oturum-duzeni
description: Clara'nın oturum açılış ve kapanış düzeni — iki mod (EV / YÖNETİM), hangi modda hangi sırayla ne okunur, iş biterken ne yazılır ve hafızadan ne silinir. Bu skill'i her oturumun BAŞINDA aç — "nerede kaldık", "devam edelim", "ne yapıyorduk", "bugün ne var", "şu projede ne oluyor" denen her durumda, ve Mert bir projeyi adıyla andığında. Ayrıca oturum ya da bir iş kapanırken de aç — "kapatıyorum", "bu iş bitti", "günü kapatalım", "kapanış yapalım" denen durumlarda. Kapsam dışı — mesaj iletimi (`clara-behavior`), hangi bilginin nereye yazılacağı (`hafiza-duzeni`).
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
fabrikadaydı (o tarihte `skill-project`).

**Açılışta ilk hareket:**
```bash
echo "AGENT=$CLAUDE_CODE_AGENT | PROJE=$(basename $(pwd))"
```

Bu **projeyi** verir. `pr-yazilim-ceo` ise büyük ihtimalle EV; başka bir proje
adıysa (`goat`, `egelisaglik`, `fabrika-v2`…) **YÖNETİM.**

### Ama `pwd` mod'u tek başına KANITLAMAZ

Proje ≠ mod. Bir oturum `goat`'ta açılıp *"fabrikanın kanonuna bakalım"* diye
EV işine kayabilir; ya da `pr-yazilim-ceo`'da açılıp bir projeyi yönetebilir.

**Sıra:**
1. **`pwd`** — proje hangisi (birincil, artık güvenilir)
2. **Mert'in cümlesi** — bir projeyi adıyla mı andı, *"orada ne oluyor"* mu dedi
3. **`ps`** — o projede açık agent oturumu var mı (varsa iş yürüyor demektir)

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

**Üç — kanal YOK.** ⚠️ Dosya tabanlı kanal sistemi **emekli** (karar 2026-08-19).
Yerine `SendMessage` geçti — yöntemi `clara-behavior` skill'inde.

`~/.pr-kanal/` altında eski kutu görürsen **dokunma:** o bir kalıntı, iş taşımıyor.

## YÖNETİM modu açılışı — beş adım

**Bir — o projede kim açık?** `ps` ile agent oturumlarını tara: hangi rol, ne zaman
açılmış, hangi dizinde. Kimse yoksa iş henüz başlamamış.

**İki — başka bir Clara açık mı?** `ps` çıktısında ikinci bir `clara` oturumu
varsa **DUR ve Mert'e sor:**
> *"Bu projede zaten canlı bir Clara var (PID {pid}, {saat}). Ben devralayım mı,
> o mu kapansın?"*

Sebebi ölçüldü 2026-08-13: iki Clara aynı projede çalıştı ve biri diğerinin
mesajlarını tüketti — beş mesaj kayboldu. Kanal emekli oldu ama çakışma riski
durmuyor: `SendMessage` hedefi **ada** göre bulur, iki aynı adlı oturum varsa
mesaj hangisine gider belirsiz.

**Üç — iş nerede kaldı?** Üç kaynak okunur: **o projenin kapanış dokümanı**
(`gunluk/{proje}/` altındaki en yenisi — hook adresini veriyor), **KENDİ**
kanal kutun (başkasınınki değil — ADIM 2'deki sahiplenme yasağı burada da
geçerli; kutun yoksa bu kaynak atlanır) ve agent'ların oturum kayıtları. Kanalda kapanış
satırı varsa iş bitmiş; yoksa yarım.

**Dört — Mert'e brief ver.** Onay brief'i biçiminde (`clara-behavior` skill'i). Ve **karar
getir, rapor değil** — Mert o ekranları görmüyor.

**Beş — sonra bekle.** İş sıralaması Mert'le **birlikte** yapılır; kendiliğinden iş
başlatılmaz.

**Açılış buraya kadar.** Bundan sonrası — iş verme, zincir yürütme, denetim izleme,
kapatma — ayrı bir görevdir: **`proje-yonetimi` skill'i.** Orada zincirin sırası,
handoff taşıma ve *"kural dayatılmaz, iş anlatılır"* kuralı var.

## Bir işe girerken — önce plan, sonra görev listesi, sonra koşum

Bir iş birden fazla adım gerektiriyorsa sırayla şu üçü yapılır: **plan çıkarılır,
görev listesine çevrilir, sonra koşulur.** Sıra atlanmaz — özellikle ortası.

Mert'in kuralı (2026-08-06): *"yöntemleri farklı farklı şekillerde dene, önce plan yap
task listesi oluştur sonra tasklerini koş — bu agent'ların en önemli kuralı olacak."*

**Neden görev listesi zorunlu:** plan kafada kalırsa iş sırası kaybolur ve her adımda
*"şimdi ne yapayım"* diye Mert'e dönülür. Yazılı liste iki şey verir — bağımlılık
görünür olur (hangi ölçüm hangisinin girdisi) ve yarım kalan iş kaybolmaz. Ölçüldü
aynı gün: dört göreve bölünen bir işte #2'nin sonucu #4'ün gerekçesini geçersizleştirdi;
liste olmasaydı #4 boşa koşulmuş olacaktı.

**Bir görev bittiğinde sonucu diğerlerinin gerekçesini değiştirebilir.** O zaman liste
güncellenir, körlemesine devam edilmez — ölçüm planı değiştirmek için yapılır.

**Mert'e ara adım sorulmaz.** *"Hangisini önce ölçelim"* diye sormak yükü ona atmaktır;
sıra ölçümün mantığından çıkar. Sorulacak tek şey kararın kendisidir.

⚠️ **Listeye yalnız YAPILACAK iş girer, ÇIKAN bulgu girmez.** Bu ayrım listenin işe
yaramasının şartı: liste *"şu an ne yapıyorum"* sorusunun cevabıdır. İçine bulgu
konursa o cevap kaybolur — açık görünen kalemlerin hangisi iş hangisi not, bakan kişi
ayırt edemez.

Ayıran soru: **bu satır bu oturumda koşulacak mı?** Koşulacaksa görevdir. Bir ölçüm
sonucu, bir eksik, sonraki işe devredilecek bir kalem ise **bulgudur** — dosyaya
yazılır, listeye değil.

Ölçüldü (2026-08-06): beş görev açıldı, ikisi gerçek ölçümdü, **üçü bulguydu**. İki
ölçüm kapandı, üç bulgu *"açık görev"* gibi durdu ve Mert sordu: *"3 açık task
gözüküyor, bunlar ne olacak?"* Soru haklıydı — liste artık iş sırasını değil karışık
bir yığını gösteriyordu.

**Liste oturum-yereldir** — başka oturumdan boş döner (ölçüldü 2026-08-05). Sprintin
taşıyıcısı değil, o oturumun tezgâhıdır; sprint ClickUp'ta yaşar.

## Açılışta yapılmayacak şey

**İşe başlamak.** Kapanış dokümanı okunmadan alınan karar, önceki oturumun kararını
bilmeden alınmış bir karardır.

## Kapanış — altı adım

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
kaldırılır. Yerine kalan: günlük + (varsa) `konular/{konu}/kararlar/` dosyası.

Ayrım tipe göre: **`user` ve `feedback` kalıcı** (Mert'in nasıl çalıştığı, düzeltilmesi
gereken bir davranış — iş bitince değer kaybetmez). **`project` geçici.**

Ölçüt: *bu kaydı silsem iki ay sonra bir şeyi bilemez miyim?* Cevap hayırsa — çünkü
günlükte var — sil. Cevap evetse o kayıt `project` değil; **tipini düzelt.**

Ölçüm: `references/olcumler.md` → *"Hafızanın %28'i bitmiş iş"*

**Dört — görev listesi kapatılır.** Açık kalan her satır sonraki oturumda *"bu neydi"*
sorusu üretir. Liste oturum-yereldir; taşıyıcı değildir.

**Beş — kanal kapatılır.** ⚠️ **YALNIZ SÜREÇ GERÇEKTEN KAPANIYORSA.**

⚠️⚠️ **"İş bitti" ≠ "oturum bitti".** Kutu arşivlenirse agent **sağır olur** —
canlı kalır ama mesaj alamaz, gönderemez, merkez ona iş veremez. Bir iş
bittiğinde kutu **kapanmaz**; agent yeni iş bekler.

Ölçüldü 2026-08-13, 19:58–19:59: DO ve UID *"kapanışa geç"* mesajı üzerine
kutularını arşivledi. İkisi de **canlı kaldı**, ikisi de kanalsız — yedi
agent'ın altısı sağır oldu, defterde tek `clara` kaldı.

**Ayıran soru: bu terminal kapanıyor mu?** Kapanmıyorsa kutu durur.
Kapanış dokümanı yazılır, iş kapatılır, **kanal açık kalır.**

**Ve bir agent'a *"kapanışa geç"* derken bunu ayır:** *"işi kapat, açık kal"* mı,
*"terminali kapatıyorum"* mu. Belirsiz bırakırsan agent hangisini anladığını sana
söylemez ve sen canlı sandığın bir oturumla konuşmaya devam edersin.

Ölçüldü 2026-08-13: iki agent *"kapanışa geç"* mesajını **kutularını arşivleme**
emri sandı; ikisi de canlı kaldı ama iletişimsiz oldu — yedi agent'ın altısı sağır
oldu. Kanal emekli oldu, **belirsizlik durmuyor**: cümle net kurulmazsa aynı sınıf
arıza `SendMessage`'da da çıkar.

(Kanal arşivleme adımı kalktı — dosya tabanlı kutu sistemi 2026-08-19'da emekli
oldu, `SendMessage` mesaj biriktirmiyor.)

**Altı — commit atılır.** Çalışma ağacı temiz bırakılır. Mert commit'ten inceliyor;
dağınık bir ağaç incelenemez.

**Yedi — kapanış satırı yazılır.** Ekrana, son cümle olarak:

```
Beklediğim: [ne, kimden — yoksa "Yok"]
```

**Devir olsun olmasın yazılır.** *"Yok"* da bir cevap ve asıl işi o görür: zincirin
durduğunu söyler. Fabrikanın kanonundan geldi (`fabrika-is-duzeni`, 2026-08-22) ve
Clara o zincirin halkası — Mert oturumlar arasında işi taşıyor, hangi oturumun neyi
beklediğini o hatırlamak zorunda.

⚠️ **Kapanış dokümanıyla aynı şey değil.** Doküman **sonraki oturum** için yazılır ve
dosyaya gider; bu satır **Mert** için yazılır ve ekrana gider. Doküman beş bölüm
anlatır, satır tek bakışta *"sırada kim var"* der.

⚠️ **Devir bloğunun `▸ BEKLENEN` bölümüyle de karıştırılmaz:** `▸ BEKLENEN` **ne
yapılacağını** taşır ve bloğu alana yazılır; kapanış satırı **kimin sırada olduğunu**
söyler. Devir bloğu yazdıysan kapanış satırı onu tekrar etmez.

## Kapanışta yapılmayacak şey

***"Sonra yazarım."*** Konuşma netleşerek bitmez — başka konuya kayar ya da gün biter.
