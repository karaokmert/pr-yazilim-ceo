# Karar — kanal kurulumu açılış hook'una alındı, merkez kapısı yok

**Tarih:** 2026-08-11 · **Karar veren:** Mert · **Oturum:** YÖNETİM (fabrika)
**Uygulama:** `~/.claude/hooks/kanal-acilis.py` + `~/.claude/settings.json`
(`SessionStart`) · yedek: `settings.json.yedek-20260811-1008`

---

## Ne karara bağlandı

**Bir.** OY ve Websitesi agent'ları açılışta kanal kurulum talimatını
**kullanıcı seviyesindeki** bir hook'tan alır. Plugin'e yazılmaz.

**İki.** Hook'ta **merkez kapısı yok** — agent, o projede açık bir Clara olup
olmadığına bakmadan kutusunu kurar.

**Üç.** Kapsam sınırı yok: her projede çalışır.

**Dört.** **Her projede ayrı Clara.** Tek Clara tüm projeleri yönetmez.

---

## Neden hook'a alındı — sebep, yama değil

Kanal protokolü fabrika kanonunda **tam**: `skill-project`'te
`.claude/skills/is-duzeni/SKILL.md:269` (`ISD-OPEN-YOUR-BOX` hükmü, dört adım)
ve `references/kanal.md` (betik adları, `--project` zorunluluğu, `Monitor`
şartı, geçerli tipler). PAM bunu 2026-08-11 09:37'de kimse söylemeden uyguladı
— kutusunu kurdu, izleyicisini doğruladı, merkeze haber verdi.

**Ama OY ve Websitesi kanonunda hiç yok.** Ölçüldü (2026-08-11): plugin
cache'inde `ozel-yazilim/0.6.1` ve `websitesi/0.8.1` altında
`pr-kanal|inbox|outbox|watch.py|setup.py` için **sıfır eşleşme.**

O boşluk bugüne kadar **elle** kapatılıyordu: Clara her agent için handoff
yazıp adresi veriyordu. Bu bir yamaydı — Clara yazmayı atlarsa agent kanalı
aramayı bile bilmiyor. `CLA-FIX-THE-CAUSE`: sebep, protokolün agent'ın
elinde olmaması. Hook sebebi kaldırır.

## Neden plugin'e yazılmadı

Mert'in kısıtı: *"plugini alacak kişilerde Clara henüz olmayacak, Clara bana
özel kalacak — onlara ayrı bir agent üreteceğim."*

Kanal **iki uçlu**: kutu açan uç + okuyan merkez. Merkez Clara. Plugin'e
yazılsa, plugin'i alan kişinin agent'ları her açılışta kutu açar, izleyici
kurar, `INFO "kuruldum"` yazar — ve okuyacak merkez **hiç olmaz**. Sonuç
kanonun en kötü hâli: *"çalıştığı sanılan monitör."*

Ölçüldü: plugin hook'u (`preload-skills.py`) ile global hook **çakışmıyor**,
ikisi de çalışıyor. Bu oturumda üç hook birden koştu (global git satırı +
Clara açılışı + remember). Yani plugin güncellemesi global hook'u ezmiyor.

---

## Merkez kapısı NEDEN YOK — üç ölçüt çürütüldü

Clara ilk tasarımda bir kapı koydu: *"o projede açık merkez varsa kur, yoksa
sessiz çık."* Gerekçesi *"merkez yoksa kanal anlamsız"* idi. Ölçüt üç kez
değişti, üçü de çürüdü:

**`STATE: OPEN`** — canlılık sinyali değil, yalnız *"arşivlenmedi"* demek.
Goat'ta sekiz kutu `OPEN` görünüyordu, hepsi dünden kalma ve monitörleri ölü.
Hook onlara *"merkez var"* deyip ölü adres gösterecekti.

**`ps` ile canlı Clara oturumu** — canlılığı veriyor ama **projeyi vermiyor.**
Ölçüldü: üç Clara oturumunun `cwd`'si de `pr-yazilim-ceo`, çünkü VS Code
profili `cd pr-yazilim-ceo && claude` ile açıyor. Clara'nın kendi kanonundaki
*"pwd sinyal değildir"* kuralı burada da geçerli. Kapı buna bağlansa
`skill-project`'te hep kapalı kalırdı — sessiz arıza.

**Zaman eşiği** — kanonun açıkça *"uydurulmaz"* dediği şey: *"günlerce
bekleyen işler ölçüldü, hiçbiri askıda değildi."*

### Üçüncü ölçüt değişiminde asıl soru soruldu

Kanonun dersi işledi: *"bir alan üç kez düzeltilip hâlâ boş dönüyorsa sorun
doldurma biçiminde değil, alanın kendisinde."*

**Mert kesti:** *"Agent'lar merkez olup olmamasına bakmaksızın şimdilik
açsınlar. Zaten kendi outbox'larına yazıyorlar. Clara açık mı diye kontrol
etmeye gerek yok."*

**Ve haklıydı — Clara kanalı senkron sanmıştı.** Kanal asenkron: agent kendi
outbox'ına yazar, mesaj **diske düşer**, imleç kimin ne okuduğunu tutar.
Merkez üç saat sonra gelse hiçbir mesaj kaybolmaz. *"Merkez yoksa kanal
anlamsız"* varsayımı kanalı bir konuşma sanmaktı. Kanon ilkesi bunu zaten
söylüyordu: **"gürültü zararsız, kayıp zararlı."**

**Kalan bedel, bilinerek kabul edildi:** okunmayan mesaj **birikir.** Kanal
kullanılmayan bir projede açılan agent kutu kurar ve mesajı bir Clara açılana
kadar bekler. Kayıp yok, artık var.

---

## Her projede ayrı Clara — gerekçe

Tek merkezin tüm projeleri yönetmesi üç yerden bozuluyor:

**Bağlam karışır.** Ölçüldü 2026-08-09: kapanış dokümanları tek akışta
tutulduğunda yeni oturum **yanlış projenin** durumunu özetledi (Goat için
açılan Clara'ya evin push kuyruğu anlatıldı). Çözüm `gunluk/{proje}/` ayrımı
oldu; kanal `~/.pr-kanal/{proje}/` ile aynı ilkeyi taşıyor.

**Yük tek noktada birikir ve körlüğe döner.** Dört projede altı agent = yirmi
dört outbox tek izleyiciye düşer. `Monitor` çok olay üreten monitörleri
**otomatik durduruyor** — yani gürültü sonunda **sessizliğe** dönüşür.

**Yıldız topolojinin anlamı kalmaz.** Merkezin gerekçesi kontrol değil
**müdahale imkânı**; dört projeyi birden izleyen merkez hiçbirinde zamanında
müdahale edemez.

**Karşı argüman ve cevabı:** *"projeler arası öğrenme kaybolur"* — kaybolmaz,
çünkü öğrenme oturumla değil **dosyayla** taşınıyor (`kararlar/`, `HARITA.md`,
hafıza). Ayrım bilgi kaybı üretmiyor, bir oturumun kapsamını daraltıyor.

`clara` bir **rol adı**, tek varlık değil — her projede o projenin merkezi.
Tıpkı `backend-developer`ın her projede farklı biri olması gibi. Ölçüldü: aynı
rol üç ayrı `cwd` ile çağrıldığında `--project goat` · `liston` · `a101egeli`
üretiyor; kutular ayrı dizinlerde, birbirini görmüyor.

---

## Hook'un yapısı — iki kapı

```
1. Clara mı?     → EVET ise sessiz çık (merkez kanalı işe göre kurar,
                   açılışta kurmaz — boş kutu üretir)
2. Kutum var mı? → VARSA kurma, adresi + izleyici komutunu hatırlat
                   (monitör oturumla ölüyor, yeniden kurulur)
```

İkisi de geçerse dört adımlı kurulum talimatı basar: `setup.py` (`--project`
yazılı) → `Monitor` ile izleyici (`Bash` yasak, bildirim üretmiyor) →
`TaskOutput` ile canlılık → `send.py` ile merkeze haber.

**Filtre betiğin içinde, `settings.json`'da değil.** `SessionStart` matcher'ı
oturumun *nasıl başladığını* eşler (startup/resume/clear), **agent adını
değil**; agent-tipi matcher yalnız `SubagentStart/Stop`'ta var. Matcher'a agent
adı yazılırsa hook **sessizce hiç çalışmaz.** Aynı ders plugin'in
`preload-skills.py` başlığında yazılı — okunmadan yazılsaydı aynı çukura
düşülecekti.

**Girdi `stdin`'den JSON**: `cwd` ve `agent_type` oradan gelir, env yedek.
Plugin de böyle yapıyor.

### Ölçülen ve düzeltilen iki arıza

**`cwd` doğrulaması yoktu** — `cwd=/yok` girdisi `--project yok` talimatı
üretti (2088 karakter). Ev dizini ya da `/tmp`'de açılan agent saçma bir proje
adıyla kutu kurardı, arıza sessiz olurdu. `Path(cwd).is_dir()` eklendi.

**Namespace rol adında taşınıyordu** — `ozel-yazilim:backend-developer` iki
nokta içeriyor, dizin adında taşınmaz. `rol.split(":")[-1]` eklendi.

### Merkez kutusunun ADI talimattan çıkarıldı

Agent'a merkezin kutu yolu **verilmiyor**, yalnız `clara` rol adı veriliyor —
`send.py` alıcıyı rol adıyla alıyor, kutu adıyla almıyor (PAM bu sabah öyle
yazdı, mesaj ulaştı).

Sebep bilgi eksikliği değil **sınır**: kanon *"başka hiçbir kutuya
dokunmazsın"* diyor. Adres verilse agent merkezin kutusuna doğrudan yazmayı
deneyebilir.

---

## Test edildi

Beş senaryo (stdin ile, `settings.json`'a bağlanmadan önce):
Clara → sessiz · kutusu olmayan rol → talimat · kutusu olan rol (PAM) →
hatırlatma · bozuk/boş/eksik girdi → `rc=0`, çıktı yok · üç ayrı proje →
üç ayrı `--project`.

**Sahada henüz ölçülmedi** — gerçek bir açılışta koşması izlenecek.

---

## Açık kalan

**`references/kanal.md` adres vermiyor.** PAM'in ölçümü: protokol kanonunda
tam ama betiklerin **disk yolu** yok — reference `<araclar>/setup.py` diyor.
PAM yolu `find` ile kendi buldu. Ayrıca reference satır 274-276'daki
*"betikler git'te değil, asset'e taşınmadı"* maddesi **tarihi geçmiş** —
betikler artık `skill-project/tools/kanal/` altında ve git'te.
İkisi de PAD'in işi, devir bloğu yazılacak.

**Betik yolu hook'ta sabit** (`ARAC_YOLU`). `skill-project` taşınırsa hook
kırılır — tek satır düzeltme, ama sessiz.

**Okunmayan mesaj birikmesi** — merkez kapısı olmadığı için kabul edilen
bedel. Ölçülmedi: kaç oturum sonra kaç kutu birikiyor.
