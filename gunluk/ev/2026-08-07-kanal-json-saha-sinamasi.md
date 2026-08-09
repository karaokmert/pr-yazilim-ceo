# Kanal JSON düzeni — saha sınaması (2026-08-07, 14:30–15:00)

**Mert'in talimatı:** *"en hızlı okuma, yazma ve haberleşme sistemini kurgulayın.
Mesajların silinme, karışma, iş bitiminde arşivlenme/silinme, yeni başlangıçta
açılma senaryolarını net olarak oluşturup deneyimleyin. Bu görev tamamen senin
kontrolünde."*

**Sonuç:** düzen kuruldu, beş araca dönüştü, dört uç doğruladı. Şablon:
`~/.pr-kanal/agent-project/SABLON-JSON.md` (542 satır) · Araçlar: `araclar/`

---

## YÖNTEM — dört uca ayrı ölçüm, sonra kendi yazdığımı onlara sınattım

Görev listesi beş kalem: hız ölçümü (PAM) · tek izleyici (PAD) · yaşam döngüsü
senaryoları (PQA) · yetim süreç + envanter (PCA) · şablon v3.

Sonra kritik adım: **kendi yazdığım on adımlık testi onlara sınattım.** Kendi
testini geçen tasarım kanıtlanmış olmuyor.

---

## KURULAN SİSTEM

```
kur.py       kutu + DURUM.md + boş imleçler (tek komut)
yaz.py       .tmp + os.replace (atomik), printf YASAK
oku.py       imleçten oku; imleç dosyası yoksa büyük kutuda DURUR
izleyici.py  dizin yoklar, KALICI yayın kaydı (.izleyici-gorulen)
arsivle.py   okunmamış varsa REDDEDER; devri DEVIR.json ile taşır
```

Çıkış kodları: `0` iş yapıldı · `1` hata · `2` durdum karar gerekiyor ·
`3` zorla yapıldı veri atlandı.

---

## ON BULGU — hepsi ölçüldü, hepsi kapandı

**`tail -F` iki katmanlı kırık.** Katman 1: zsh boş glob'da `NOMATCH` verip
komutu **hiç başlatmıyor** — ve yeni kutu her zaman boş, yani kurulum anı tam o
an. Katman 2: dolu dizinde bile sonrakini görmüyor; PQA `ps` ile kanıtladı,
`tail`'e dizin değil **dosya listesi** gidiyor. → dizin yoklama.

**`printf` çıkış kodu 0 verip bozuk JSON üretiyor** (PAM). İlk testinde geçmişti
çünkü kaçışları elle yazmıştı; gerçekçi gövdeyle kırıldı. Kazancı 385 ms değil,
**doğruluk riski.**

**"Son 10" varsayılanı iki yönlü sessiz hata üretiyordu** (PQA Bulgu 4). 12 iş
emri + silinmiş imleç → 10 yapılmış iş yeniden okundu, 2 mesaj sessizce atlandı.
→ artık büyük kutuda **durup soruyor.**

**Devir mekanizma değil disiplindi** (PQA Bulgu 3). Arşive taşınan kutunun imleci
ve okunmamışları hiç geçmiyordu; arşivdeki dört gece kutusunda `.cursor` sayısı
**0**. → `arsivle.py` okunmamış varsa reddediyor, `DEVIR.json` + `son-arsiv.json`
üretiyor.

**Monitör yeniden başlatmada arada geleni yutuyordu** (PQA Bulgu 5). Ve bu istisna
değil kural — monitör her oturumda ölüyor. → diskte kalıcı yayın kaydı.
İki kayıt **birleştirilmez** (PAD): `.cursor` = agent ne okudu,
`.izleyici-gorulen` = izleyici neyi bağırdı.

**Çıkış kodları tutarsızdı ve `&&` geçiyordu** (üç uç bağımsız). `oku.py` durup
hiçbir şey okumazken `rc=0` dönüyordu → `oku.py && yaz.py` zincirinde okunmamış
işe cevap yazılıyordu. Tam `printf`'in yasaklanma sınıfı.

**Şablon kendi iddiasını tutmuyordu** (PCA Çelişki 1). *"Boş `.cursor` ile
silinmiş `.cursor` ayrılıyor"* yazıyordu, kod ayırmıyordu (ikisi de `""`
oluyordu). PCA'nın tespiti: **"niyet doğru yazılmış, kod uygulamamış."**

**Bozuk JSON'da imleç ilerliyordu** (PQA Bulgu B) — *"görünür hata + sessiz
kayıp."* → imleç artık bozuk dosyanın önünde duruyor.

**Yön uyarısı kutu adından türetiyordu** (PAD Bulgu 2) → `DURUM.md`'deki `ROL`
alanından okuyor; `DURUM.md` yoksa uyarmıyor (bilinmiyor ≠ yanlış).

**Kapanış artık iki taraflı** (PCA). Agent kendi kutusunu **tek başına
kapatamıyor**: outbox imleci merkezin. Tasarım doğru ama v2'de mümkündü, artık
değil — bilinmezse kilit gibi görünür.

---

## CANLILIK — üç sinyal, ikisi yanlış

**`kill -0 PID` → YANLIŞ**, ikinci kez çürütüldü: iki canlı agent'ı ölü gösterdi.

**Transcript son değişim zamanı → YANLIŞ, ve daha kötü yönde.** Ben bunu bu sabah
*"çalışan aday"* diye işaretlemiştim; PCA çürüttü, doğruladım: transcript
**proje** bazlı (58 transcript / 5 kutu), 11 kutunun hepsi *"0 dk"* çıkıyor. Yani
**ölü kutuyu canlı** gösteriyor — `kill -0` canlıyı ölü der (zararsız), bu
ölüyü canlı der (temizlik hiç yapılmaz).

**Kutunun kendi son yazım zamanı → ÇALIŞIYOR.** Canlı dörtlü 0–3 dk · merkez
30 dk · `websitesi` 202 dk · `hukuk-testi` 1022 dk. Ama **eşik uydurulmaz** —
otomatik temizlik yapılmıyor.

---

## ÇOK YAZARLI ÇAKIŞMA — ayrım korunmalı

**Mekanizma DOĞRULANDI** (PCA'nın bariyerli 4-process testi): 522 bayt gövde
(`PIPE_BUF` 512'nin üstünde), 97/99 yazar değişimi, 100/100 geçerli, 0 karışma.

**Agent eşzamanlılığı ÖLÇÜLEMEDİ.** Dört agent 100 mesaj yazdı, 0 karışma çıktı —
ama yazar değişimi **3/99**, kesişen ikili **0/6**: dördü sırayla yazdı.

Yani sıfır karışma *"çakışma engellendi"* değil, **"çakışma hiç olmadı"** demek.
Agent ana döngüsü sıralı; *"eşzamanlı yaz"* demek eşzamanlılık üretmiyor.

---

## CLARA'NIN HATALARI — üçü aynı sınıftan

**Monitörü kurmadım.** Kanonda *"merkezin dinlemesi şart, tercih değil"* yazılı
ve gerekçesi ölçülmüş (Clara 8 tur dinlemedi, kanal tek yönlü çalıştı). Dördüne
yazdım, dinlemedim. Üç uç bana glob'un çözümünü yazdı, o bilgiyle kendi
monitörümü kurmadım.

**İmleç tutmadım.** Dört outbox'ı `ls` ile taradım. PQA yakaladı: raporu 14:14'te
yazılmış, ben 14:23'te *"outbox'ın boş"* diye sordum. `.cursor` yoktu. Onun
cümlesi: **"Boş" bir ölçüm değil, okunmamış bir kutunun görünümü.**

**Ölçümün ölçtüğü şeyi doğrulamadım.** Çakışma testinde 100 dosya/0 karışma
gördüm ve *"hedef kapandı"* dedim. Ayırt edici sinyal elimdeydi — dosya
adlarındaki zaman damgaları. Bakmadım çünkü sayım beklentimi doğruluyordu.
**Doğrulanan beklenti sorgulanmıyor.**

PAM aynı hatayı yaptı ve kendi memory kaydından alıntıladı: *"bir gözlem iki
açıklamaya birden uyuyorsa hiçbirini seçme."* Kural kayıtlıydı, tetik çekilmedi.

**Ve bir kez bash yazdım, çöktü** — macOS `/bin/bash` 3.2, `declare -A` yok.

---

## YÖNTEM KURALI — eşzamanlılık sayımla sınanmaz

Sayım *"kaç dosya"* der; eşzamanlılık bir **zaman** iddiasıdır. PCA'nın
tekrarlanabilir hâle getirdiği ders — ve kendi uyarısı: *"benim o gün nasıl fark
ettiğim değil, ayrımın kendisi kayda değer."*

---

## AÇIK KALANLAR

**Araçlara tek nokta bağımlılığı** (PQA). Betikler `~/.pr-kanal/` altında,
**git'te değil.** Dizin silinirse yeniden üretme tarifi yok. v2 kurulabilir ama
kopyalanamazdı; v3 kopyalanabilir ama **araçlara bağımlı.**

**Agent kanonları hâlâ kanalı bilmiyor** — dört uç **üçüncü kez** söyledi.

**Yetim süreç** — PCA teşhis etti (PAD'in `/tmp/globtest` artığı, PPID 1, kanala
dokunmuyor). Kimse öldürmedi.

**`Monitor` otomatik durdurma eşiği** ölçülmedi · **1000 dosyalı kutu**
ölçülmedi · **Bu senaryolar otomatik sınanmıyor** (PQA Bulgu 6).

**Kanal protokolünün kanona girmesi** — Mert'in kararı.

---

# EK — İsimler globalleşti (15:30–16:00)

**Mert'in kararı:** *"dosyalarımızı Türkçe kullanmayalım, global isimler haline
getirelim"* + *"bunları da İngilizce yapabilirsin, mesajlaşma Türkçe yapılacak
zaten."*

Gerekçe: araçlar `agent-project`'e **asset** olarak girecek, plugin setup skill'i
ile her makinenin lokaline kurulacak. Yani git'e girecek ve global okunabilir
olmalı.

**Ne değişti:** `araclar/` → `tools/` · `kur/yaz/oku/izleyici/arsivle.py` →
`setup/send/read/watch/archive.py` · JSON alanları `from/to/time/type/body` ·
türler `TASK/INFO/QUESTION/CLOSE` · `STATUS.md` (`ROLE/SESSION/STARTED/TASK/
STATE/STORE`) · `HANDOVER.json` · `archive-log.json` · `.announced` · bayraklar
`--project/--task/--force/--last/--all/--cursor`.

**Gövde Türkçe kaldı**, kod içindeki gerekçe yorumları da.

## Çeviri iki kez kırdı — ve sınıfı bugünkü bir bulgunun aynısı

Otomatik değiştirme bağlam ayırmadı:

- `("tur","type")` → `return` içindeki heceyi yakaladı, **`retypen`** oldu
- ikinci turda `OTURUM` içindeki `TUR` bozuldu → **`OMSGTYPEUM`**

İkisi de PAD'in aynı gün bulduğu tuzak: **ham metin araması bağlamı ayırmıyor.**
PAD `"alici": "clara"` alan adını gövde içeriği sanmıştı. Çözüm ikisinde de aynı:
sınır belirt — PAD parse etti, ben `\b` kelime sınırı kullandım.

**Ders:** bir çeviriyi otomatik yapıyorsan her turdan sonra **uçtan uca koştur.**
Syntax kontrolü yetmiyor — `OMSGTYPEUM` geçerli Python'du, `STATUS.md`
üretiliyordu, sadece alan adı saçmaydı.

## Geçiş sınaması — dört uçla koşuldu

Dördü de eski kutusunu `CLOSE` ile kapattı, yeni kutuyu `tools/setup.py` ile
kurdu. Beş eski kutu arşivlendi (`clara-ceo` dahil), beş yeni kutu `STATE: OPEN`.

**Ve geçiş anında bir arıza ortaya çıktı:** dört uç kapanış mesajını **eski
araçla** yazdı, yeni `watch.py` onları `from=? type=?` gösterdi. Kayıp yok
(dosya görüldü, bildirim geldi) ama **yazar görünmüyordu.**

Çözüm: `read.py` ve `watch.py` yeni alanı bulamazsa eski Türkçe karşılığına
bakıyor ve satırı **`[LEGACY-FORMAT]`** diye işaretliyor. Sessizce çevirmiyor —
sessiz çeviri *"hangi format"* bilgisini kaybettirir, ve o bilgi geçişin bittiğini
ölçmenin tek yolu.

**Neden önemli:** aynı körlük asset güncellemesinde tekrar eder. Sahada eski
format mesaj varken yeni araç kurulursa yazar kaybolur.

## Taşıma testi — bir sabit yol arızası bulundu

Araçlar `/tmp`'ye kopyalanıp çalıştırıldı. `setup.py` çıktısında **sabit yol**
basıyordu (`~/.pr-kanal/agent-project/araclar`), yani taşındığında **var olmayan
bir adres** veriyordu. Asset olarak dağıtılınca yol değişeceği için bu tam
kırılma noktasıydı. Düzeltildi: `os.path.dirname(os.path.abspath(__file__))`.
