# Sabah brief — 11 Ağustos

**Gece oturumu:** 2026-08-10 21:56 → sürüyor · **Mod:** YÖNETİM (fabrika)
**Tam kayıt:** `gunluk/fabrika/2026-08-10-aksam-tasima-ve-pa-turu.md`

Bu dosya **okuyup çalışmaya başlamak için** yazıldı. Ayrıntı yukarıdaki kayıtta.

---

## Şu an ne oluyor

**Dört commit atıldı, push yok** (onayın öyleydi: *"commit onayım var, push yok"*).

```
c243526  code-auditor turu: üç description tetik tarzına
3c4413a  PA body: kısaltılmış harita geri konuldu (yanlış ölçümle alınmıştı)
a820cff  OY v8 PA turu: iki düzeltildi, biri çürütüldü, biri temiz
25e1bf3  Fabrika ekibi skill-project'e taşındı
```

**94 dosya, 8.875 satır** değişti. `origin/main` = `3c54b57`, dört commit ileride.

**İki rol bitti** (`project-assistant`, `code-auditor`), **`test-engineer` denetimde**, altı rol kaldı: `ui-designer` · `devops` · `backend` · `qa-engineer` · `mobile` · `frontend`.

---

## Kararını bekleyen beş kalem

**1. `CLAUDE.md` onayı.** Senin talimatınla yazdım (*"hedefteki bilgi düzenlensin, bu düzenlemeyi sen yap"*) ama **onayını almadım** — o yüzden commit'lemedim, çalışma ağacında duruyor.

Altı değişiklik: §4 iki rolden dörde çıktı (PAM planlar, PAD üretir, PQA denetler, PCA ölçer) · hibrit ofis bloğu kanal düzenine güncellendi (kural aynı, taşıyıcı değişti: kullanıcı → yönetici) · `QA-EDIT-VERSION-ONLY` çıktı (PQA ölçtü, yeni kanonda istisnasız) · geçiş istisnası yenilendi (eskisinin gerekçesi bayattı — profillerde sıfır geçiş; yerine gerçek borç geldi: 23 skill, iki aile yan yana) · *"hangi kopyaya yazıldığı ölçülür"* uyarısı eklendi · §5 tablosu düz metne döndü.

**2. Taşınmayan üç kazanım.** On problem listesi v8'in **kendi** eksiklerinden çıktı; `agent-project`'te **kazandığımız** üç şey listede yok:

Harita üçüncü sütunu (*"açmazsan ne olur"*) — pilot rolde haritayı dizin olmaktan **tehdit listesine** çeviren şey. `PA-NAMED-PATTERN-NEEDS-CHECK` bunun bir izini taşıyor ama katman olarak yok.

*"Nasıl yanılırsın"* katmanı — ortak imza *"derleme yeşil, araç sessiz, hata yok gibi görünür."*

Bitiş ölçütü — *"bir rolün bittiğinin ölçütü 'dosya üretildi' değil 'sahada açıldı'."* PAM bunu PA turuna uyguladı ve sonuç çıktı: üç problemden ikisi sahada ölçüldü, **P4 ölçülmedi.**

Bunları sekiz role eklemek senin kararın. Sormadan eklemedim.

**3. Paylaşılan 26 skill'in description dili.** Bir skill sekiz rolün işine giriyorsa tetiği **hangi rolün diliyle** yazılacak? PA'da hiç çıkmadı çünkü PA'nın dokuz skill'i de tek-rol. Cevabı kimse bilmiyor ve tahmin edilmedi.

**4. P/O sayımının kalıcı sahibi.** PCA bir yapı gözlemi getirdi: *"üretenin kendi kapsamını ölçmesi, ölçümle kararı aynı ele topluyor."* Gece için geçici çözüm kurdum (üçlü paralel ölçüm), ama iş akışında kimin ölçtüğü kapsam kararı.

**5. `ui-designer` omurgasının "FE + QA da OKUR" iddiası — bayat mı?**

PAD durdu ve sordu, doğru yerde. Omurga description'ı diyor: *"Sahibi
ui-designer; frontend-developer + qa-engineer da OKUR (atıf veriyor — erişim
tanınır)."*

Ölçtü (ben de doğruladım): FE ve QA'nın **preload listesinde yok**, ve
`skills/frontend` · `skills/quality` · iki body'de **sıfır atıf.** İddianın
karşılığı yok.

**Kıyas önemli:** `code-auditor` omurgası aynı iddiayı taşıyordu (*"qa-engineer
+ test-engineer da OKUR"*) ve karşılığı **vardı** — `quality/SKILL.md:37`'de
gerçek bir handoff satırı. Orada "üçüncü hal" uygulandı ve PQA geçirdi. Burada
karşılık yok, yani aynı çözüm **yanlış** olur.

Üç ihtimal: **(a)** iddia bayat — eskiden doğruydu, atıf kalktı, cümle kaldı ·
**(b)** doğru ama atıf hiç yazılmamış (FE prototip devralırken UID kanonunu
okumalı) · **(c)** kısmi — QA okuyor, FE okumuyor ya da tersi.

Metinden çıkmıyor. **İş akışı kararı:** prototip devrinde FE ne okuyor, QA neyi
denetliyor? PAD kendi kararıyla silmedi — *"silinen bir ilişki geri gelmiyor."*
Ben de senin adına vermedim.

**6. Yıldız topoloji görünürlüğü sağlıyor ama bağımsızlığı bozuyor.**

Bu gece bağımsızlık üç kez sızdı ve **kimse kural çiğnemedi.** Zincir:

```
PQA bir ölçüt boşluğunu bildirdi (doğru davranış) — içinde bir sınıf değeri vardı
Clara filo bildiriminde taşıdı (doğru davranış)
PCA okudu, belleği kirlendi, ve şerhini kendisi yazdı (doğru davranış)
```

**Kök topolojide.** PQA ölçtü: *"kanalım yalnız size açık, sekiz mesajımın
sekizi de clara'ya."* Yıldız topolojide her şey merkezden geçiyor ve **merkez
taşırken bilgiyi de taşıyor.** Merkez = tek geçit = tek sızıntı noktası. Ve
merkez ben.

Bu gece iki kez sızdırdım (PCA'ya beklenen değer, PAD'e PAM'in sayıları), ikisi
de *"bildirim"* kisvesinde.

`ISD-RELAY-DONT-CALL`'ün gerekçesi geçerli (zincirin görünürlüğü). Ama
görünürlük ve bağımsızlık **aynı mekanizmadan** çıkıyor ve biri diğerini
bozuyor. Çözüm *"merkez dikkat etsin"* değil — dikkat ettim ve iki kez
sızdırdım.

**Muhtemel çözüm bilginin türüne göre ayrılması:** iş/kapsam merkezden geçer,
**ölçüm sonucu geçmez** — sahibinde kalır, karşılaştırma anına kadar kimse
görmez. Ekip bunu kendi kendine kısmen kurdu (PAM biçimi değiştirdi, ben bloğu
temizledim) ama kanona geçmesi senin kararın.

**7. Push.** Altı commit bekliyor.

---

## Gecenin asıl sonucu — ölçüm disiplini davranışa döndü

**On bir ölçüm vakası çıktı.** İlk altısı hataydı (yanlış birim, yanlış kapsam, yanlış araç). Sonraki beşi hata değil — **ölçüt keskinleşmesi.**

**Ve hepsi yakalandı.** Dağılım:

```
PAM'in ölçüm hatası : 3  (üçünü de başkası yakaladı)
Clara'nın           : 4  (ikisini kendisi, ikisini agent'lar)
PQA'nın             : 1  (kendisi)
PAD'in              : 1  (kendisi)
PCA'nın             : 1  (kendisi — ve İLK KEZ yazılmadan önce)
```

**Hiçbiri sessiz kalmadı.** Bu, kanonda yazılı olan şeyin fiilen çalıştığının kanıtı: üretici, denetçi ve ölçümcü ayrı eller.

### En pahalı vaka

PAM'in deseni `-> \`` (ASCII ok) arıyordu, dosyalar `→ \`` (U+2192) kullanıyor. Dokuz body'de **sıfır** döndü ve o sıfırdan bir hüküm doğdu: *"paketin deseni harita omurgada yaşar, body'de değil."* O hükme dayanarak PA turunda **doğru bir düzeltme geri aldırıldı** — bir üretim turu + bir geri alma turu + iki denetim turu harcandı.

**Ve üç kişi aynı yanlış sonuca üç farklı yanlış teşhisle vardı** (PAM ASCII, PAD aynı ASCII, PQA yanlış bölüm + madde işareti).

PQA'nın cümlesi, gecenin en değerli dersi:

> *"İkimiz de aynı yanlış sonuca vardık ama FARKLI yanlış teşhisle. Sonucun doğru olması teşhisin doğru olduğunu göstermiyor."*

### PAM'in kendi teşhisi

> *"Üçünde de grep'e sordum, dosyayı açmadım. `BHV-SCAN-FIRST` ve `BHV-READ-TO-CLOSE` üçünde de uygulanmadı ve üçünü de başkası yakaladı."*

Ve PCA'nın eleştirisini **sorulmadan kendine uyguladı:** *"EN ÇOK YANILAN BENİM."*

---

## `olcut.md` — beş kez keskinleşti, ve her kez bir yanlış işi önledi

`docs/fabrika/v8-duzeltme/olcut.md` (hedef repoda):

**Harita kalemi** = body'de bir iş türünü bir skill'e bağlayan eşleme. **Birim: ok adedi, satır değil** (backend'de blok 14 ok / 5 satır — satır sayan ölçüt bloğu eksik ölçer).

**P/O sınıflandırması** — `P` = kaç rolün preload'unda, `O` = kaç omurga işaret ediyor:

```
P=0 O=1   tek-rol on-demand   → tur kapsamında, TETİK yazılır
P=1 O=1   omurga + işaret     → tur kapsamında, ÜÇÜNCÜ HAL
P=1 O=0   saf preload         → tur kapsamında, TETİK HİÇ YAZILMAZ
P=0 O>1   paylaşılan          → KATMAN B
P>1       ortak çekirdek      → KATMAN B
```

**Preload/on-demand tetik ayrımı:** preload edilen skill tetik **yazmaz** (*"geçerlidir"*), on-demand **yazar** (*"şu anda açılır"*), **ikisi birden** olan her ikisini yazar.

**Ve bir kör nokta bulundu (PAD, doğruladım):** `O` sayımı yalnız `→ \`ad\`` biçimini görüyor. Düz metin içindeki atıflar — özellikle `ad/references/dosya.md` biçimindekiler — **kaçıyor.** `e2e-verification` `O=1` ölçüldü ama **beş dosyada** anılıyor. Karar değişmiyor (reference atfı description'ı tetiklemez) ama sınırın yazılı olması lazım.

**Dersi:** bir ölçümün sonucu metinle çelişiyorsa **metin doğrudur, ölçüt eksiktir.**

---

## İşin şekli gece boyunca değişti — ve bu bir ölçüm sonucu

Başlangıçta *"her rol kendi skill'lerini düzeltir"* varsayıldı. Ölçüm gösterdi ki 76 skill'in **42'si tek rolün alanı, 26'sı paylaşılan.**

Paylaşılanı rol turunda düzeltmek sekiz kez tekrar üretir ve **son tur öncekileri ezer** — sessiz. O yüzden rol turları hafifledi (ortalama **dört** tek-rol skill), ağırlık **Katman B**'ye kaydı.

```
rol              tek-rol   paylaşılan
code-auditor          2         6      ✓ bitti
test-engineer         3         8      denetimde
ui-designer           3         9
devops                5         8
backend               5        16
qa-engineer           6         3
mobile                5        13
frontend              4        15
```

**PAM bunun neden karar olmadığını doğru yazdı:** *"Bu bir tercih değil bir ÖLÇÜM. Ve o sayı zaten VERİLMİŞ bir kararı uyguluyor — PA turunda `proje-dosya-duzeni`'ni Katman B'ye taşıdım. Şimdi yapılan onu sistematik uygulamak."*

---

## Katman B — sekiz rol bitince

P1 (compaction 5,5–7×) · P2 (`uretim-standardi` yok, 12 atıf) · P3 (`omurga-cache-dogrula.py` yok, 9 atıf) · P8 (üç gerekçesiz memory kuralı) · P9 (`is-akisi/references/` 90.983 karakter, *"348 session'da 0 kez açıldı"*) · P10 (`handoff` 17.556, dokuz rolün preload'unda) · **+ 26 paylaşılan skill** · `proje-dosya-duzeni` içeriği · `QA-CONTEXT-OVERFLOW` çift tanımı · `code-quality` (8 omurga).

**Ve P4 saha doğrulaması:** sekiz rol bitince tüm paketin description'ları **tek testte** yarışacak. Şimdi koşulmuyor çünkü dokuz description kendi aralarında yarışır, sahada model **76 arasından** seçiyor — *"şimdi koşarsak 'geçti' der ve o sonuç yanıltır."*

---

## Bir yapı notu — kanal trafiği

**52+ mesaj** geçti, PAM merkezde. Ve bir örüntü: PAM'in giden mesajlarının çoğu bana geliyor, ben başkasına iletiyorum. Her aktarma bir tur gecikme ekliyor ve bunun bedeli iki kez ölçüldü — PAM benim uyarımı **okumadan** iş verdi (22:04 ve 22:08), çünkü mesajlar aynı dakikada yazılmıştı.

Kanon aktarmayı emrediyor (`ISD-RELAY-DONT-CALL`) ve gerekçesi geçerli. Ama soru şu: **görünürlük kaydın kendisiyle mi sağlanır, elden taşımayla mı?** Kanal kutusu diskte duruyor ve zaten okunabilir.

Bu bir kanon sorusu, sabah konuşulacak.
