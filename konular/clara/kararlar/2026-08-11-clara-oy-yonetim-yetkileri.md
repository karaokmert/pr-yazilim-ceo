# Clara'nın OY proje yönetimi yetkileri — altı karar

**Tarih:** 2026-08-11 (akşam oturumu)
**Karar veren:** Mert
**Etkilenen:** `proje-yonetimi` skill'i · Clara gövdesi · `kanal-acilis.py` hook'u ·
`skill-project/tools/kanal/setup.py`

---

## Bağlam

Mert `mert/Proje-yonetimi.md` ve `mert/clara-behavior.md` dosyalarını yazdı — Clara'nın
proje yöneticiliğini kendi kelimeleriyle tarif eden başlangıç metinleri. Clara mevcut
kanonuyla karşılaştırdı, yedi boşluk + bir çelişki çıkardı, altı soru sordu. Altısı da
cevaplandı.

---

## Karar 1 — Kabul kriteri bizim, test dokümanı PA'nın

**Zincir:** Biz ClickUp task'ına kabul kriterlerini yazarız → PA discovery'yi buna göre
kurar → iş yapılır → PA biten işten test dokümanını yazar → TE koşar.

*Mert: "Biz işe başlarken doküman yazıyorsak oraya kabul kriterlerimizi yazarız.
Discovery zaten buna göre oluşur. Testi belirlemek PA'nın görevidir."* Ve kriterler
**ClickUp'a** yazılır, ayrı repo dosyasına değil.

**Gerekçe:** kabul kriteri **girdi** (kod yazılmadan var, koddan çıkarılamaz), test
dokümanı **çıktı** (biten işten üretilir). Kriter yazılmazsa test dokümanı yalnız
koddan çıkar — yapılanı test eder, istenileni değil, ve bu sessiz olur.

Clara'nın işi ikisi arasındaki **bağı** kontrol etmek.

---

## Karar 2 — Kanon bekçiliği bir KAPI, tetiği "iş bitti"

**Eski kural:** *"hüküm vermezsin, gerekçe talep edersin; bekçi kapıyı kapatmaz."*
**Yeni:** agent *"bitti"* dediğinde Clara sorar — *"skill'lerini açtın mı, hangi
kanona göre yaptın?"* — ve **"aç, kontrol et" deme yetkisi var.** Agent kontrol edip
öyle commit'ler.

*Mert: "agentlar bir yerden sonra memory ile ilerliyor. Memory okey ama kanon
kontrolü önemli, sapma istemiyorum. Aç kontrol et deme yetkin var. Kontrol etsin ve
öyle commit'lesin."*

**Gerekçe:** memory kanonu ezebiliyor — deneyle kanıtlı (`memory-management`:
*"skill'le çelişen çıplak kayıt skill'i ezer"*). Sapma kaçınılmaz, kontrol noktası şart.

**Direktif değil:** *"şu satırı şöyle yaz"* denmiyor, *"kendi kuralına bak"* deniyor.
Bu `EN SERT KURAL`ın (kural dayatmazsın) istisnası değil — hangi kurala bakacağı
söylenmiyor, **bakması** söyleniyor.

---

## Karar 3 — Commit onayı Clara'da, push onayı Mert'te

```
BE "bitti" → Clara "kanonunu aç, kontrol et" → BE kontrol eder → commit'ler
→ CLARA COMMIT ONAYI → QA denetimi → MERT PUSH ONAYI → QA push atar
```

*Mert: "Commit onayını sen verebilirsin." · "Push onayı bende, ben olmadan hiçbir şey
push'a gitmez." · "Push'u sadece QA yapabilir."*

**Bu bir düzeltmedir:** `proje-yonetimi` skill'i ve `oturum-duzeni` kapanış dokümanı
*"OY'da push QA'da"* diyordu. Yanlış — push **işlemi** QA'da, push **onayı** Mert'te.

**OY kanonuyla köprü:** agent body'lerinde `REL-APPROVAL-USER-ONLY` var (*"onay yalnız
kullanıcıdan"*) ve Clara kavramı yok. Mert agent'ları değiştirmek istemedi
(*"şu an agentları değiştirmiyorum"*); köprü **açılış hook'una** yazıldı.

---

## Karar 4 — Sahada ölçüm YOK

*Mert: "ölçme yok, sen olabildiğince takip edip iş yönlendireceksin. Senin işin takip;
sen kod okursan mesajlar bekler, iş yavaşlar."*

Clara beyanı alır, akıtır. Yanlış beyanı yakalayacak olan QA.

**Bu gövdedeki *"ölçersin, sınarsın, bakarsın"* kuralını iptal etmiyor, moda bağlıyor:**
EV'de ölçmek görev, sahada değil. Ayıran şey mod.

**İstisna:** iş geliştirme evde yapılır ve orada Clara kodu okuyabilir — *"Clara evde
çalışırken kodun nerede yaşadığını bilerek kodu okuyup kontrol yapabilir."*

---

## Karar 5 — Mert yokken karar Clara'nın

Bir tıkanma ölçümden değil **tercihten** çıkıyorsa (nullable mı, task bölünsün mü)
Clara kararı verir, akış durmaz. Karar Mert döndüğünde rapora girer.

*Mert: "karar verirsin ve geldiğimde bana vereceğin rapora eklersin."*

**Gövdedeki *"karar vermezsin"* kuralı koşula bağlandı**, iptal edilmedi: Mert ordaysa
karar onun. Gerekçe: bekleyen agent maliyet, yanlış tercih düzeltilebilir.

**Bekleyenler listesi:** Clara SQL/telepresence/make aktifleştiremez. O işleri
biriktirir, Mert döndüğünde mini brief verir (karar gerekenler / işlem gerekenler /
test için / verilmiş kararlar). ⚠️ Brief verirken Mert'in sorularına cevap
verebilmeli — *"dur agent'a sorayım"* geçiştirmedir.

---

## Karar 6 — Soru süzme dört kademeli

PA'nın sprint planlama soruları Clara'dan geçer. Süzme sırası:

1. **PA'yı zorla** — *"koddan/emsalden çıkarabilir misin?"* Yapısal cevap varsa Mert'e
   gitmez.
2. **Basit ve dokümandan çıkmıyorsa** — PA ile birlikte tarama yaptır, kararı verin.
   Rapora girer.
3. **Clara biliyorsa** — cevapla, rapora girer.
4. **Kalan Mert'e** — gerçekten tercihe bağlı olanlar.

**Tek tek değil ÖZET:** PA discovery özetini verdiğinde Clara Mert'e *sorular +
verilmiş kararlar* listesini birlikte getirir.

*Mert: "PA'yı olabildiğince yapısal bulmaya zorlarsın... bana liste olarak en son
verirsin."*

---

## Yapısal kararlar

**Skill birleştirildi.** `proje-yonetimi` artık **OY'a özel** (377 → 447 satır).
Ekip kadrosu ayrı reference'a çıktı (`references/oy-ekibi.md`, 206 satır).
*Mert: "hepsi tek skill, proje yönetimi ile birleştir bunu, tek skill olsun artık."*
**Websitesi için ayrı skill yazılacak.**

**Kadro kaynağı `skill-project` taraması.** Clara üretti, fabrika denetiminden
geçmedi — kendi odasında yaşıyor. Yürürlükteki sürüm **v8** (marketplace manifesti +
kurulu plugin 0.6.1 kanıtı); `v7/` önceki kuşak, `team/ozel-yazilim` 1/9 dolu (pilot).

**Sprint skill'i ayrı kaldı** — planlama ritüeli ayrı bir iş. Ama **Çarşamba 09:00
bitiş eşiği** `proje-yonetimi`'ne girdi: sahada trafik akıtırken bilinmesi gereken şey
o. Çarşamba 9 hem kapanış hem açılış; Salı akşamı bitmemiş iş **Clara tarafından**
izlenir, Çarşamba sabahı öğrenilmez.

---

## Kanal düzeni değişti — merkez inbox'ı

*Mert: "Her mesajını ekranla birlikte kanala yaz. Kanala yazmadığın mesajlar Mert'e
düşmez. Tek ekranda kanal üzerinden takip ediliyor tüm agentlar." · "Clara her
açılışta kendi kutusunu açar, eski kutu varsa arşive alınmamışsa kapatır. Agent aktifi
bulur ve açıldım der."*

**Eski düzen:** agent kendi outbox'ına yazar, Clara N kutuyu tek tek okur.
**Yeni:** agent **merkezin inbox'ına** yazar, Clara tek yerden okur.

**Değişen iki dosya:**

`skill-project/tools/kanal/setup.py` — kutu kurulunca projede en yeni açık `clara-*`
kutusunu arar, bulursa merkez adresini çıktıya basar. Bulamazsa outbox dalına düşer
(mesaj kaybolmaz, bekler).

`~/.claude/hooks/kanal-acilis.py` — Clara kapısı sessiz çıkmıyor artık: eski kutularını
arşivletir + yeni kutu kurdurur. Agent metnine merkez adresi (tam yol), *"her mesaj
kanala"* bloğu ve iş sonu onay bloğu eklendi.

### "Aktif kutu hangisi" — belirsizlik ölçümle değil DÜZENLE kalktı

Canlılık ölçülemiyor: `STATE: OPEN` *"arşivlenmedi"* demek (Goat'ta 8 ölü kutu OPEN
göründü) · `ps` projeyi vermiyor · zaman eşiği uydurma. Üç ölçüt denendi, üçü de çürüdü.

Çözüm ölçütü iyileştirmek değil, **soruyu ortadan kaldıran düzen kurmak** oldu: Clara
her açılışta eskisini kapatırsa **en yeni = aktif** olur. `setup.py` bu garantiye
dayanıyor. Bu `CLA-FIX-THE-CAUSE`'un uygulanışı.

⚠️ `archive.py` okunmamış mesaj varsa arşivlemeyi **reddediyor** — Clara önce okur.

### Yakalanan iki arıza

**`Path | None` sözdizimi.** Sistem `python3` = 3.9; bu 3.10+ sözdizimi ve import
anında `TypeError` veriyor — **hook hiç çalışmaz, sessizce.** İki senaryoda da patladı,
düzeltildi. Ders: hook'a tip imzası yazılmaz.

**Büyük/küçük harf.** Sahada hem `Clara-` (goat, ceo) hem `clara-` (liston,
skill-project) kutuları var. Kanon **küçük harf**; tarama `.lower()` ile ikisini de
buluyor ki eski kutular görünmez olmasın.

**Ölçüm:** altı projede test edildi — goat/liston/skill-project/ceo merkez buldu,
egelisaglik + platin-agent-web `None` döndü (Clara kutusu yok, agent'lar açık). Canlı
yazma testi: dosya merkez inbox'ına düştü, yön uyarısı tetiklenmedi.

---

## Kanona girmeyen — Mert'in dosyasında olup henüz yazılmayan

`mert/Proje-yonetimi.md` ve `mert/clara-behavior.md` **başlangıç metinleridir**,
devamı gelecek (*"yarım değil aslında başlangıç, bunları al, devamı geldikçe
ekleriz"*).

**Agent tanıma skill'i:** Websitesi ekibi için ayrı skill henüz yazılmadı.
