> **UYARI — bu dosya yürürlükteki kaynak DEĞİL.**
> Sprint yapısı 2026-08-05'te ClickUp'a taşındı ve orada yaşıyor:
> `CLARA DOC → Sprint Planları → Sprint 2026-08-05 → 2026-08-12` (+ yedi iş alt sayfası)
> ve `Görevler` listesinde yedi task. Bu dosya planlamanın ilk taslağı — yedi işin adları
> ve kapsamları sonradan değişti, ClickUp güncel. Tarihsel kayıt olarak duruyor.
> Karar gerekçesi: `kararlar/2026-08-05-sprint-planlama-kararlari.md`

# Sprint: 5 Ağustos → 12 Ağustos 2026

**Sahibi:** Clara. Kararlar Mert'in, kalemlerin yürütülmesi ve takibi Clara'da.
**İcracı:** PAM (5. kalem) — iş kanaldan verilir, PAM yapar.
**Bitiş:** 12 Ağustos Çarşamba sabahı. Yeni sprint o sabah planlanır.

Bu dosya **iskelet.** Her kalemin detayı sırası geldiğinde ayrı dosyada yazılır —
şimdi yazılsa tahmin olur, çünkü 1. kalemin çıktısı 4 ve 5'in detayını değiştirecek.

---

## Sprintin tek cümlesi

Fabrika ekibi kendi işini bilerek yapabilir hâle gelecek, Clara ile fabrika arasında
iş taşıyan bir kanal kurulacak, ve v8 agent'ları sahadan öğrenilenlerle temizlenerek
`agent-project` altına taşınacak.

---

## Zorunlu sıra

Kalemler bağımsız değil; birbirini kilitliyor. Sıra şu:

```
1 ─┐
   ├→ 3 → 4 → 5 → 6
2 ─┘

7 ────────────────→ (hepsinin üstünde paralel)
```

**1 ve 2 paralel yürür** — birbirine bağlı değil, ikisi de bu haftanın ilk yarısında
bitmeli yoksa zincir tıkanır.

**Neden bu sıra:**
- **3, 2'ye bağlı** — kanal altyapısı olmadan fabrika kanalı kurulamaz.
- **4, 3'e bağlı** — bilgi aktarımı kanaldan geçecek.
- **4, 1'e de bağlı** — neyin eksik olduğu bilinmeden ne aktarılacağı belli olmaz.
- **5, 4'e bağlı** — bilgisi eksik bir PAM'e sekiz agent taşıması vermek en pahalı
  hata; çıktı yanlışsa sekiz dosya geri alınır.
- **6, 5'e bağlı** — taşınmamış agent kanala bağlanamaz.

**Clara'nın eli 3 bitene kadar bağlı.** Sorumluluk Clara'da ama PAM'e iş vermek
kanaldan geçiyor ve kanal henüz kurulu değil. Bu, sıranın neden pazarlık konusu
olmadığını gösteriyor.

---

## Kalemler

### 1 — Fabrika ekibinin düzeni ve talimatları denetlenecek

Fabrika ekibinin (PAM/PAD/PQA/PCA) elinde ne var, ne eksik. Talimatları tutarlı mı,
düzen işliyor mu, bilgi boşluğu nerede.

**Neden:** 5. kalemin girdisi bu. Ne eksik olduğu bilinmeden 4. kalemde ne
aktarılacağı belirlenemez.

**Bittiğini nasıl anlarız:** Fabrika ekibinin her üyesi için "elinde ne var / ne eksik"
kaydı çıkmış olur. Eksikler madde madde listelenmiş olur.

**Bilinen tuzak:** Agent kendi frontmatter'ını göremiyor ve skill'leri preload
olmuyor (hook telafi ediyor). Yani PAM "biliyorum" diyebilir ama elinde olmayabilir —
**sorulmaz, ölçülür.**

---

### 2 — Kanal sisteminin altyapısı geliştirilecek

Bir tetikleyici agent ile o projeye bağlı agent'ların haberleşebildiği, düzgün bir
altyapıya sahip kanal sistemi.

**Neden:** Bu sprintin taşıyıcı altyapısı. 3, 4, 5, 6 hepsi buradan geçiyor.

**Bittiğini nasıl anlarız:** Bir tetikleyici agent bir mesaj yazdığında hedef agent
onu alıyor, cevabı geri geliyor, ve zincir Mert'in görebileceği bir yerde duruyor.
Kayıp mesaj yok.

**Bu kalemin içinde çözülmesi gereken bir şey Clara'nın kendi tarafında:** 2026-08-05'te
ölçüldü — Clara'nın talimat trafiği kusurluydu (tekrarlanan mesajlar, iptal edilen
talimatlar, hiç ulaşmayan mesajlar). Kanalı kurmak yetmiyor, **kanala yazan tarafın
disiplini de kurulmalı.** Yoksa altyapı sağlam, trafik bozuk olur.

**Elde olan:** `web-kanal-2` deneyi (17 mesaj, sapma sıfır), izin/yetki ölçümleri,
kanalın yetki taşımadığı doğrulaması.

---

### 3 — Fabrika ekibi ile Clara arasına kanal kurulacak

**Neden:** 4 ve 5 bu kanaldan yürüyecek. Clara'nın PAM'e iş verebilmesinin tek yolu.

**Bittiğini nasıl anlarız:** Clara kanala bir iş yazıyor, PAM alıyor, yaptığını geri
yazıyor, Mert zinciri görüyor.

**Kanon durumu:** `CLA-NO-CALL-TEAMS` ikiye bölünecek — `Agent`/`Task` ile agent
çağırmak **yasak kalır** (rapor yönü bozulur, denetim kaybolur), kanala yazmak
**serbest olur** (zincir dosyada durur). Karar 2026-08-05'te verildi, gerekçesi
`kararlar/` altına yazılacak.

---

### 4 — Fabrika ekibinin bilgi eksiği giderilecek (Clara aracılığıyla)

Agent nasıl üretilir, skill nasıl yazılır — netleştirilecek.

**Neden:** Mert'in cümlesi: *"PAM ne yapacağını da hep bilecek."* Yani bu bir eğitim
değil, **kanon boşluğu kapatma** işi. Fabrika kendi işini bilerek yapmalı.

**Bittiğini nasıl anlarız:** PAM'e bir üretim işi verildiğinde "nasıl yapılır" diye
sormuyor, yapıyor. Ölçüm: kanondan okunmuş bir davranış çıkıyor mu.

**Girdisi 1. kalemin çıktısı.**

---

### 5 — v8 agent'ları `agent-project` altına temiz taşınacak

v8 agent'ları zaten üretildi ve **sahada çalışıyor.** Bu bir sıfırdan üretim değil,
**taşıma** — sahada takip edilen eksikler düzeltilerek, memory'ler ve oturum
kayıtları elden geçirilerek yeni düzene aktarım.

**Neden beş hafta sürmeyecek:** v8'in ilk üretimi beş hafta sürdü ama iki sebebi vardı
ve ikisi de artık yok — (1) skill preload olmuyordu, çözülemiyordu; şimdi hook telafi
ediyor, (2) tüm kurallar sıfırdan üretiliyordu; şimdi kurallar var.

**İcracı PAM.** İş kanaldan verilir (3'e bağlı), PAM yapar, Clara takip eder.

**Bittiğini nasıl anlarız:** Agent'lar `agent-project` altında, temiz, sahadan gelen
düzeltmeler işlenmiş, eski kuşak artıkları taşınmamış.

**Paralel yürüyen iş:** Sahadaki eksiklerin takibi sprint boyunca ayrı bir Clara
oturumunda devam eder. Buradan çıkan bulgular taşımanın girdisi olur.

---

### 6 — Taşınan v8 agent'ları kanal sistemiyle çalışacak

**Neden:** Taşıma tek başına yeterli değil; agent'lar birbirleriyle ve Clara'yla
kanaldan haberleşebilmeli.

**Bittiğini nasıl anlarız:** Taşınmış bir agent kanaldan iş alıp cevap veriyor.

**5'e bağlı.**

---

### 7 — Clara ile takip ve iş yönetim mekanizması genişletilecek

Sağlıklı bir takip düzeni: hangi iş nerede, ne bekliyor, ne kadar bekledi.

**Neden:** Bugün ölçüldü ve iki iş görünmeden bekledi — bir webhook işi **42 saat**,
PLATIN SSL promptu **~48 saat.** İkisi de "askıda" olduğunu hiçbir yerde göstermiyordu.
Sebebi: PA'nın görevleri **ID'siz** çıkıyor, izlenemiyor.

**Bittiğini nasıl anlarız:** "Şu iş ne aşamada" sorusu tek yerden cevaplanıyor, ve
bir iş uzun süre beklediğinde bu görünür oluyor.

**Elde olan:** Canlı panel (`topla.py` + `index.html`, 10 saniyede yenileniyor,
5 proje izleniyor). Panelde iki karar hâlâ askıda — uzun bekleyenler yanıp sönsün mü,
`pr-yazilim-ceo` oturumları panelde kalsın mı.

**Bu kalem hepsinin üstünde paralel yürür.**

---

## Sprintin içinde çözülmesi gereken, kalem olmayan işler

**Agent'lara task listesi kuralı.** Plan aldıktan sonra agent kendini adımlara böler.
İki faydası ölçüldü: (1) agent kendini kaybetmez — bugün GOAT tam mock incelemesini
atladı, PA kapanmış kalemleri tekrar sordu, (2) Mert agent'ın penceresine baktığında
ilerlemeyi canlı görür. **Sınırı:** liste oturum-yerel, başka oturumdan görünmüyor
(2026-08-05'te ölçüldü) — yani beş agent = beş pencere, toplu görüntü vermez.
Fabrikanın kanonu olduğu için 4. kalemin içinden geçer.

**9 kopya meselesi.** `backend-developer.md` ekosistemde **9 yerde** duruyor: arşiv,
v7, v8, plugin cache, marketplace, bir müşteri projesi. Hangisi yürürlükte olduğu
belirsiz ve bu bugün somut zarar verdi — v7 kopyası okundu, v8 hakkında yanlış teşhis
kuruldu. 5. kalemin taşıması bu kirliliği çözmeli, yoksa aynı hata tekrarlanır.

---

## Kayıt yeri kararı (ölçüldü, 2026-08-05)

ClickUp ve repo eşit test edildi — üç soru, iki tarafa:

**Kesinlik:** Gövdeye gömülü tam kelime (`zurnabalik`) — repo 4 sonuç, ClickUp **0**.
Repo kazandı.

**Ayırt etme:** `backend-developer.md` repoda **9 kopya**, hangisi yürürlükte belirsiz.
ClickUp'ta kopya sorunu yok. **Ama** kirlilik bizim kayıt dosyalarımızda değil,
çok-kuşaklı agent dosyalarında — `clara.md` tek kopya. Yani problem "repo" değil,
agent dosyalarının kuşak birikimi.

**Geçmiş:** ClickUp MCP'sinde doküman geçmişi aracı **yok** (create/update/list/get,
hepsi bu) ve `update` içeriği tamamen eziyor. Repoda `git log` "bu satır neden
değişti" sorusunu cevaplıyor.

**Sonuç:** Kayıtlar (bulgu, ölçüm, karar, gerekçe) **repoda** kalır. Sprint kalemleri
ve statüleri **ClickUp'ta** durur — Mert her yerden görebilsin diye; repo bunu yapamıyor.
Detay: `gunluk/2026-08-05.md`, "21:29" ve "21:43" başlıkları.

**ClickUp yapısı:** `Clara` space → `Görevler` listesi (şu an boş) + `CLARA DOC`
dokümanı. Statü seti henüz kurulmadı — `Askıda` statüsü öneriliyor, çünkü 42 ve 48
saatlik bekleyen işler bugün hiçbir yerde görünmedi.

---

## Açık kalanlar

- ClickUp `Görevler` listesinin statü seti kurulmadı.
- Panel iki kararı bekliyor (uzun bekleyen vurgusu, `pr-yazilim-ceo` oturumlarının
  görünürlüğü).
- Sprint planı bir skill'e çevrilecek — bu oturum onun prototipi.
- Kanon: `CLA-NO-CALL-TEAMS`'in bölünmesi yazılacak, gerekçesi `kararlar/` altına.
