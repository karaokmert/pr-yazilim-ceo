# Gece nöbeti — karar defteri (2026-08-10)

**Mert 00:35'te yattı.** Kontrol Clara'da. Beklentisi: sabaha OY takımı
`agent-project`'te Clara'nın testinden geçmiş hâlde hazır + alınan kararlar
gerekçeleriyle + hangi agent ne durumda.

**Sınır: yayındaki v8 plugin'leri kalmaya devam ediyor** (Mert'in teyidi) — sahadaki
`ozel-yazilim@pryazilim-agents 0.6.1`'e dokunulmuyor.

Bu dosya kararların yazıldığı yer. Her karar: **ne · neden · neye dayandı · alternatifi
neden seçilmedi.**

---

## Açılış durumu (00:36 ölçümü)

Dört fabrika agent'ı **00:28'de** açılmış, `agent-project` dizininde:
`pr-agent-manager` · `pr-agent-developer` · `pr-agent-qa` · `pr-agent-context-analyst`

Dördü de **00:30-00:31'de** kendi kanal kutusunu kurmuş, izleyicisini `Monitor` ile
bağlamış, canlılığını doğrulamış, ilk okumasını yapmış (hepsi boş) ve **iş bekliyor.**
Kanon yüklü olduğunu dördü de ayrı ayrı bildirmiş.

Kanal: `~/.pr-kanal/agent-project/`, JSON düzeni, araçlar `tools/` altında
(`send.py`, `read.py`, `watch.py`, `archive.py`, `setup.py`).

**Yani zincir hazır, iş verilmemiş.** Gecenin ilk hamlesi bu.

---

## KARAR 1 — İş PAM'e kanaldan verilecek, doğrudan çağrıyla değil

**Ne:** OY yeniden üretimi gereksinimini PAM'in inbox'una `send.py` ile yazıyorum.
Agent'ları `Agent` aracıyla çağırmıyorum.

**Neden:** `CLA-NO-CALL-TEAMS`. Bir agent diğerini çağırdığında rapor kullanıcıya değil
**çağırana** gider — zincir görünmez olur. Ölçüldü (2026-07-30): bir denetçi doğrudan
çağrıldı, raporunu üreticiye verdi, atmadığı bir push'u attım dedi.

Kanal bu sorunu çözüyor: mesajlar kalıcı dosya, kim ne demiş sabahleyin okunabilir.
Mert zinciri elden taşımıyor ama **kayıt** taşıyor.

**Alternatif neden seçilmedi:** Mert uyuyor, elden taşıma yok. Kanal zaten kurulu ve
dördü de kutusunu açmış — kurulu bir mekanizmayı atlayıp doğrudan çağırmak hem kanonu
çiğner hem izi siler.

---

## KARAR 2 — Gereksinim kanala kopyalanmayacak, adresi verilecek

**Ne:** Mesaj gövdesine gereksinimin kendisini değil **yolunu** yazıyorum.

**Neden:** Kanal disiplini (ölçüldü, 2026-08-09: PAM'in kutusu 48 KB'a çıkınca okuma
13.831 token harcadı). Uzun içerik kanala gömülmez — özet + adres gider, ayrıntı
dosyadan okunur.

Ve ikinci sebep: gereksinim **`pr-yazilim-ceo` reposunda** duruyor, PAM oradan
okuyabilir. Kopyalarsam iki nüsha olur, biri güncellenir diğeri bayatlar.

---

## BULGU 1 (00:42) — `send.py` sessizce yanlış yere yazıyor

**Ne oldu:** İlk beş mesajı `send.py <kutu-adi> ...` diye gönderdim. Araç
`written: ... (3053 chars)` dedi, **exit 0 verdi**, hiçbir uyarı çıkmadı. Ama mesajlar
kutunun **köküne** düştü — `inbox/` boş kaldı. **PAM işi hiç görmedi.**

**Nasıl yakalandı:** on dakika sonra ilerleme kontrolü yaptım; PAM'in outbox'unda yeni
mesaj yoktu ve inbox'u boştu. Kontrol etmeseydim sabaha kadar *"PAM çalışıyor"*
sanacaktım.

**Sebep:** araç verilen dizine yazıyor, hedefi kendisi türetmiyor. Doğru kullanım
`send.py <kutu>/inbox ...`. Yön hatası kontrolü var ama yalnız `outbox` adı verildiğinde
çalışıyor — kutu kökü verildiğinde sessiz.

**Düzeltme:** beş mesaj doğru adrese yeniden gönderildi, kökteki artıklar silindi.

**Neden bu bir bulgu:** Bu tam olarak memory taramasında çıkardığım **sessiz kırılma**
sınıfı — *"araç sessiz, exit 0, hata yok gibi görünür."* Ve kanonun en büyük eksiği
olarak işaretlediğim şeyin canlı örneği. Aynı gece, kendi elimde.

**Yeni takıma taşınacak:** bu vaka sessiz kırılma envanterine girer. Ayrıca `send.py`
kutu kökü verildiğinde uyarmalı — ama **o düzeltme fabrikanın işi**, kanal betikleri
zaten PAD kuyruğunda. Not olarak iletilecek, gece işi durdurulmayacak.

---

## KARAR 3 (00:58) — Gereksinimin iki kalemi düşürülüyor: kural zaten var

**PAM'in bulgusu benim hatamı yakaladı ve haklı.**

Gereksinime *"description biçim kuralı yazılacak"* ve *"reference çağırma kuralı
yazılacak"* diye iki kalem koymuştum. PAM ölçtü: **fabrikada ikisi de zaten var** —
`URT-DESCRIBE-MOMENTS`, `URT-NO-CONTENT-IN-DESCRIPTION`, `BHV-OPEN-SOURCE`.

**Kaynaktan doğruladım** (`agent-project/.claude/skills/uretim/SKILL.md:220-231`).
Ve fabrikanın ölçütü benimkinden **keskin**: *"description'daki bir cümle skill
açılmadan da kullanılabiliyorsa orada olmamalı."* Hedef 300 karakter de yazılı.

**Kararım: iki kalem gereksinimden düşer.** Yerine tek satır: *mevcut hüküm OY'ye
uygulanacak.*

**Gerekçe — `CLA-FIX-THE-CAUSE`:** var olan bir kuralın yanına ikincisini yazmak yama.
Sorun kural eksikliği değil, **uygulanmaması.** İkinci kimlik yazmak
`URT-NO-DUPLICATE-ID`'yi de çiğnerdi — PAM bunu kendi kanonundan doğru okudu.

**Kendi hatam neydi:** OY'nin kanonunu ölçtüm, **fabrikanın kanonunu bu eksende
ölçmedim.** Mert'in altı maddesini "yeni hüküm ihtiyacı" diye okudum; oysa dördü mevcut
hükmün uygulanması.

---

## KARAR 4 (00:58) — "En riskli iki rol" teşhisim çürüdü, düzeltiliyor

Gereksinime yazmıştım: *"UID ve TE en riskli iki rol, çünkü memory'leri boş — kanonun
eksiğini raporlayamazlar."*

**PDM dokuz rolü tam okuyup ölçtü ve çürüttü:** o iki rolün sınırları **daha keskin**,
bulanık değil — UID'de 13 kuralın 8'i negatif, dokuz rolde **en yüksek oran.**

**Gerçek ayıran: kapı sahipliği + zorunlu çağrı.** CA da kapısız ama iki rol onu
çağırmak **zorunda** (`QA-IMPACT-REACTIVE-TRIGGER` + PA'nın `impact-analiz`'i —
kaynaktan doğrulandı). **TE ve UID'i kimse zorunlu çağırmıyor.** Boş memory bir sebep
değil, bir **sonuç**.

**Kararım: teşhis düzeltilir ve gereksinime yazılır.** Bu bir kayıt meselesi değil,
tasarım meselesi — yeni takımda TE ve UID için ya bir zorunlu çağrı tetiği kurulur ya
da rol kararı gözden geçirilir.

**Ve PAM'in bir bonusu var:** UID-FE ucu eksende örtüşüyor (aynı repo, aynı React, iki
paylaşılan skill, aynı kapı) — **dokuz rolde tek gerçek birleşme adayı.** Bu, rol açma
ölçütünün ilk çıktısı olacak.

**Neden bu benim hatamın aynısı değil:** ben *"memory boş → risk"* dedim, bu bir
korelasyondu ve sebep sandım. PAM sebebi ölçtü. Aynı hata sınıfı: **belirtiyi sebep
sanmak.**
