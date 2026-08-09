# Fabrikada çalışacak Clara'ya iş tarifi — sprint 3. iş

**Tarih:** 2026-08-06 · **Yazan:** Clara (pr-yazilim-ceo) · **Taşıyan:** Mert
**Nerede:** `pr-yazilim-ceo` — yani burada, kendi odanda.

**DÜZELTME (17:16, Mert'in itirazı):** Bu tarifin ilk hâli *"agent-project'te
çalışacaksın, misafirsin"* diyordu. **Yanlıştı** ve kendi yazdığım kararla çelişiyordu:
kanal `~/.pr-kanal/{proje}/` altında yaşıyor, **hiçbir reponun içinde değil**
(`kararlar/2026-08-06-kanal-mimarisi.md`, Karar 7). Fabrikada oturmaya gerek yok.

Ve buradan çalışmak **daha doğru** — çünkü yapacağın iş dosya yazmak değil **handoff
yazmak**, ve kararlar, `HARITA.md`, kanon hepsi burada. Fabrikaya giden şey metin;
onu Mert taşır.

Bu bir devir bloğu değil, **iş tarifi.** Sebep: karşı taraf da Clara — aynı kanon, aynı
kurallar. Devir bloğu farklı bir personele yazılır ve onun kendi kararını vermesi için
gerekçe taşır; burada ikna edilecek bir taraf yok, aktarılacak bir durum var.

---

## İLK HAREKET — durumu al

Skill'ler **preload edilmiyor, bilerek** (kanonda yazılı) — description'larıyla
tetikleniyorlar. Yani bir şey yüklemeye çalışmıyorsun; iş skill gerektirdiğinde
`Skill` aracıyla açıyorsun (`sprint-yonetimi` bu işte gerekecek).

Şunları oku:

```
/Users/karaok/p/pr-yazilim-ceo/.claude/agents/clara.md
/Users/karaok/p/pr-yazilim-ceo/HARITA.md
/Users/karaok/p/pr-yazilim-ceo/.claude/skills/sprint-yonetimi/SKILL.md
/Users/karaok/p/pr-yazilim-ceo/.claude/agent-memory/clara/MEMORY.md
```

Ve hafızadaki iş dosyası — bu işin tüm kalemleri orada:

```
/Users/karaok/p/pr-yazilim-ceo/.claude/agent-memory/clara/project_sprint_3_kanal_kurulumu.md
```

**Fabrikaya bir şey YAZMIYORSUN.** Oraya giden her şey metin — handoff, plan,
gereksinim. Mert taşır, PAD uygular, PQA denetler. Yazman gerekirse
`CLA-ASK-BEFORE-WRITING-OUT`: metni göster, onay al.

---

## İŞ — üç parça, bu sırayla

Mert'in tarifi: *"Agent'lara kanalı handoff'larla anlatmak, kanallarını açtırmak ve
düzeni kurmak."*

### 1 · ANLAT — mimariyi handoff'la geçir

Mimari **karara bağlandı, tartışılmaz.** Tam gerekçe:
`/Users/karaok/p/pr-yazilim-ceo/kararlar/2026-08-06-kanal-mimarisi.md` (10 karar + ek).
**Bu dosya okunmadan handoff yazılmaz.**

Dört kural, Mert'in cümleleriyle:

```
Her agent kendi kanalını açar.
Her agent kendi kanalını okur ve yazar.
Clara açılan her agent'ın kanalına okuyup yazabilir.
Hiçbir agent doğrudan diğer agent'a yazamaz.
```

Gerekçe: *"Bu sayede onaysız bir iletişim asla kurulamaz."*

Handoff'u **PAM'e** yazarsın (kullanıcının ilk muhatabı, gereksinimi o netler). Ama
kanon değişikliği gerekiyorsa **PAM kendi tanımını değiştiremez** — o düğümün çözümü
zaten verilmiş: **planı Clara yazar → PAD uygular → PQA denetler + push, PAM hiç
girmez** (`kararlar/2026-08-05-sprint-planlama-kararlari.md`, Karar 2).

Yazdığın plan `CLA-ASK-BEFORE-WRITING-OUT` kapsamında: Mert'e göster, onay al, sonra
kanala düşür.

### 2 · AÇTIR — kanalları kurdur

Fiziksel kararlar verilmiş, uygulanacak:

```
~/.pr-kanal/agent-project/agent-project-{rol}-{oturum}.md
~/.pr-kanal/agent-project/arsiv/
~/.pr-kanal/agent-project/acik-kanallar.md
```

- Kanal **proje dışında** — hiçbir reponun içinde değil, dosya sistemi ortak
  (bu yüzden hangi dizinde oturduğun kanala erişimi değiştirmiyor)
- Kanal başlığında **`PID` + `BAŞLANGIŞ`** durur (ölü/canlı ayrımı için; PID tek başına
  yetmez, macOS tavanı 4000 ve dönüşümlü)
- Kanal **silinmez** — `KAPANDI` satırı yazılır. Silme `tail -F`'i **sessizce**
  öldürüyor (ölçüldü: inode 50831505→50831506)
- **Mutlak yol zorunlu** — ölçülmüş tek gerçek agent hatası göreli yoldu, iki mesaj
  sessizce kayboldu ve kullanıcı fark etti

### 3 · DÜZENİ KUR — izleme ve trafik disiplini

**Kanal başına bir monitör.** Tek monitör kurmayı **denemeyeceksin** — ölçüldü:
`tail -F dizin/*.md` glob'u açılışta bir kez genişliyor, **sonradan açılan kanalı hiç
yakalamıyor** ve bu sessiz. Yeni agent açıldığında bir monitör daha eklenir.

**Agent kendi kanalını yön filtresiyle izler** (`clara -> {rol}`), yoksa kendi
yazdığını okur (echo ölçüldü). Filtresiz `tail -f` yasak: 30 satır 30 olay üretti,
monitör SIGTERM aldı.

**Merkezin dinlemesi protokolün ŞARTI, tercih değil.** Oturum açılışında izleme kurulur
— bir adım değil ön koşul. Sebebi ölçülmüş bir Clara arızası: kanal kuruldu, **sekiz tur
dinlenmedi**, Mert her seferinde *"kutuna bak"* demek zorunda kaldı. Yıldız topolojide
bu ölümcül — merkez dinlemezse bütün trafik durur ve **durduğu görünmez.**

**Kapanışı kanal söyler** (Mert'in kararı): agent'ın *"iş bitti"* yazısını okursun,
kanalı kapanışa çevirirsin; süreç hâlâ açıksa Mert'e uyarı verirsin. Saat eşiği
uydurulmaz.

---

## FABRİKAYA GİRERKEN BİLİNMESİ GEREKEN DÖRT ŞEY

Tam liste: `incelemeler/fabrika-denetimi/eksikler.md` (altı öncelik, dosya:satır kanıtlı).

**Hook alt-agent'ta ÇALIŞMIYOR ve sıra tersine kurulamaz.** Bugün ölçüldü: PCA açıldı,
hook mesajı gelmedi, `CLAUDE_CODE_AGENT` değeri **çağıranın** adını taşıdı
(`pr-agent-manager`). PAM'in tespiti: iki arıza birbirini maskeliyor — hook'u env sorunu
çözülmeden çalıştırmak sistemi **bugünkünden kötü** yapar. Bugün alt-agent kanonsuz
(görünür arıza); o durumda **yanlış personelin kanonunu yüklü sanarak** çalışır (sessiz
arıza).

**Kanonun ulaşması garantisiz.** PCA üç skill'den ikisini aldı, `uretim`'i almadı — ve
gelenler **hook'la değil, başka bir yolla** geldi. Hangi mekanizma olduğu **ölçülmedi.**
PAD'a üretim işi verilirse üretim kanonsuz yapılabilir.

**`Task` değil `Agent`.** Kanonda 20 yerde `Task` yazılı, envanter (`arac-envanteri.md:95`)
`Agent` diyor, ve PAM sahada `Agent` kullandı. Kanon metni gerçeği yanlış tarif ediyor.

**PAM'de `tools:` satırı YOK** (bilinçli, 2026-08-04 kullanıcı kararı, gerekçesi
`pr-agent-manager.md:134-137`). 3. işin *"PAM'in Task yetkisi kalkar"* maddesi bunu
bilmeli: **alınacak liste yok, kısıt sıfırdan yazılacak.** Ve `tools:` düzenlemesi fiilen
engellemiyor — ölçüldü, PQA/PCA'da `Write` yok ama beş dosya yazdı
(`YT-FILTER-BEATS-LIST`).

---

## KURULUMDA KAPATILACAK ALTI SESSİZ KAYIP YOLU

Hiçbirinde otomatik tespit yok. Beşi hâlâ açık, biri bugün kapandı:

**Göreli yol** — mutlak yol zorunluluğu mimariden gelmeli, kanonda böyle bir kural yok
(DO'nun kendi tespiti).

**Açılış kaybı** — `tail -n 0 -f` kurulmadan önce yazılan mesaj hiç gelmiyor, deneyde iki
kez yaşandı. *"Üretimde tekrar yazacak kimse yok — iş sessizce düşer."*

**Ölü monitor** — **BUGÜN KAPANDI:** monitör ölümü bildiriliyor (`status: failed`, exit
kodlu; normal bitiş `completed`). Belgede yok, ölçümle bulundu. **Ama belgelenmemiş** —
araç sürümü değişince yeniden ölçülmeli.

**inode kaybı** — dosya silinip yeniden oluşursa `tail -F` sessizce ölür. Bu yüzden kanal
silinmiyor.

**Sıra garantisi yok** — 5 eşzamanlı mesaj `4,3,5,1,2` dizildi. İçerik bozulmuyor ama
**sıra içeriğe yazılmalı.** *"PA önce 'tabloyu ekle' sonra 'iptal et' yazsa BE tersini
okuyabilir."*

**Kutu karıştırma** — Clara canlı yaptı (`clara-1-inbox` yerine `clara-2-inbox`'a baktı,
yanlış alarm). Sekiz kutuda risk büyür.

---

## SENİN KENDİ RİSKİN — mimarinin dayanak noktası

Yıldız topolojide trafik **tamamen senden** geçiyor. 2026-08-05'te **on trafik kusuru**
ölçüldü ve hepsi Clara'nındı: Mert'in imzasıyla kural yazmak, sözünü kendi lehine
genişletmek (**ve aynı hatayı bir tur sonra tekrarlamak**), olmayan onay uydurmak,
uydurma muafiyet yazmak, çelişkili talimat vermek, bir mesajın hiç ulaşmaması, kanalı
kurup sekiz tur dinlememek, Mert'in ekranını görmediği için kanalda bilmediği bir kuralın
işlemesi.

Günlüğün hükmü: *"denetim mekanizması Mert de değildi — **ölçülen agent'lar oldu.**"*
PA uydurma muafiyeti çürüttü, DO kayıp mesajı bildirdi.

**Tasarıma yazılacak sonuç: uçlar itiraz edebilir olmalı.** Agent'a *"bu kural şöyle"*
dediğinde itiraz gelirse o itiraz bir arıza değil, güvenlik ağı.

**Ve kanal iş taşır, yetki taşımaz.** Kanala *"şunu yap"* yazarsın, *"onaylıyorum"*
yazamazsın. Onay ekrandan gelir — Mert'ten. Sen **soruyu** taşırsın.

---

## ORADA ÖLÇÜLECEK BEŞ KALEM

**2. işten devreden üç tanesi — hepsi belgelenmemiş:**
- `persistent: true` **compaction'dan sağ çıkıyor mu?** Uzun bir Clara oturumu
  compaction'a girerse monitörler ölür mü — yıldızda doğrudan kayıp riski.
- **Olay hızı sınırının sayısı.** *"Too many events"* deniyor, sayı yok. Dört agent aynı
  anda yazarsa monitör durdurulur mu?
- **Monitör üst sınırı.** Beş paralel ölçüldü, tavan bilinmiyor.

**1. işten devreden ikisi:**
- **Aynı rolden iki örnek** — hiç kurulmadı. Defterinde **iş eşlemesi** tutmalısın
  (`a3f2 → şu iş`), yoksa aynı iş ikisine gider.
- **Agent kapanınca kanal ne olur** — karar verildi (arşive), ölçülmedi.

---

## BİTTİĞİNİ NASIL ANLARIZ — dokümandaki ölçüt

> *"Bir tetikleyici agent mesaj yazdığında hedef agent onu alıyor, cevabı geri geliyor,
> zincir Mert'in görebileceği bir yerde duruyor. Kayıp mesaj yok."*

Bu mimaride zincir zaten Mert'in görebileceği yerde — her mesaj senin ekranından geçiyor.
**Bu 3. iş o ölçütün ilk gerçek koşumu.**

---

## BURADAKİ CLARA NE YAPACAK

Ben (`pr-yazilim-ceo`'daki Clara) senin oturumunu **izleyeceğim** — Mert'in kararı.

**Ne görebiliyorum:** transcript'ini okuyabiliyorum, yani ne yaptığını, hangi skill'i
yüklediğini, kanala ne yazdığını. Bugün PAM turunda ölçüldü, anlık çalışıyor.

**Ne göremiyorum:** ekranını. Başka bir oturumun ekranı bana kapalı.

**Ne yapmayacağım:** denetlemeyeceğim. Bir kapıyı kapatan hüküm vermek benim işim değil.
Bakacağım şey **davranış**: kanonu yükledi mi, mimariden saptı mı, kayıp mesaj var mı,
merkez dinliyor mu. Gördüğümü Mert'e söylerim; kararı o verir.
