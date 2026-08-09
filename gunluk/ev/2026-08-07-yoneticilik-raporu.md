# Clara'nın proje yöneticiliği raporu — 2026-08-07

Mert istedi: *"nasıl gitti, verimsizlik neredeydi, nasıl daha iyi olabilir."*
Ayrıca kanal büyüklüğü.

**Ölçüm tarihi:** 2026-08-07, 23:26. Referans commit `6bb50ff`.

---

## RAKAMLAR

**Fabrika çıktısı:**
```
commit          18 (hiçbiri push edilmedi)
kural           123 → 131   (+8 net; 10 yeni kimlik, 2 kaldırıldı)
denetim turu    14
bulgu           12 — hepsi kapandı
iş klasörü      6 yeni
```

**Bugün kanona giren on kimlik:**
```
ISD-RELAY-DONT-CALL              agent agent'ı çağırmaz, yönetici iletir
ISD-KEEP-HANDOFF-EPHEMERAL       devir metni kalıcı belge değil
ISD-OPEN-YOUR-BOX                kanal kurulumu (dört adım + iki tuzak)
ISD-RETURN-TO-PLANNER            denetim sonucu PAM'e döner
ISD-CASCADE-COVERS-DESCRIPTIONS  cascade tarif eden cümleleri de kapsar
BHV-READ-TO-CLOSE                tamlık taramayla değil okumayla ölçülür
BHV-DONT-AIM-AT-LAST-MISS        ekseni geçen turun bulgusuna göre seçme
BHV-DATE-THE-MEASUREMENT         ölçümün tarihi + kapsamı yazılır
BHV-LIST-BEFORE-RUNNING          işi adımlara böl, listeye yaz, sonra koş
BHV-LIST-HOLDS-WORK-ONLY         listeye yalnız yapılacak iş girer
```

**Kanal:** 116 dosya · 461.642 karakter · ~115 bin token
```
clara      59 mesaj  206.932 krk   ← trafiğin %45'i merkezden
PAD        19 mesaj   60.005 krk
PQA        17 mesaj  101.283 krk   ← en uzun mesajlar (ort 5.958)
PAM        16 mesaj   70.886 krk
PCA         5 mesaj   22.536 krk   ← en az mesaj, en yoğun içerik
```

---

## NASIL GİTTİ

**Zincir çalıştı.** Beş rol (PAM → PAD → PQA → PCA → merkez) bir gün boyunca
kesintisiz koştu. On dört denetim turunda on iki bulgu çıktı ve **hepsi gerçekti**
— hiçbiri boşa gitmedi.

**En değerli üç şey — üçü de agent'lardan geldi, benden değil:**

**PQA'nın yöntem teşhisleri.** Bulgu bulmakla kalmadı, **kendi yönteminin
sınırını** ölçtü: *"tarama geçmiş bulguyu doğuruyor, gelecek bulguyu değil."* Bu
cümleden bir kural doğdu (`BHV-DONT-AIM-AT-LAST-MISS`). PCA'nın değerlendirmesi:
*"dördünde gördüğüm en nadir şey."*

**PCA'nın tek taraması.** Bugün sekiz saat boş kaldı, tek iş aldı — ve o iş
**dokuz denetim turunun hepsinin kaçırdığı** bir çelişkiyi buldu: iki kural zıt
mekanizma tarif ediyordu ve ikisi de yürürlükteydi.

**Üç agent'ın kendi zayıflığını önden yazması.** PQA denetim başlamadan
*"denetleyeceğim kural benim bulgumdan doğdu, tanıdık gelecek"* dedi. PAM
*"bu gereksinim bana yetki veriyor, gerekçelerim lehime eğilebilir"* dedi. PAD
*"bu turda ekseni değiştirdim, şimdi hangi eksen kör kaldı?"* diye sordu.

**Kanal bunu mümkün kıldı** — kutuya yazılan mesaj kalıcı, geri alınamaz, ve
üçüncü göz her zaman okuyabiliyor.

---

## VERİMSİZLİK NEREDEYDİ

### 1 · Ölçmeden konuşmak — dört tarafta birden

Bugün `BHV-DATE-THE-MEASUREMENT` kanona girdi (*"ölçümün tarihi ve kapsamı
yazılır"*) ve **dördümüz de ihlal ettik:**

```
PAM     cascade alanını beş ölçtü, on bir çıktı  → 5 ek denetim turu
PAD     "plan kelimesini kullanmadım" dedi, üç yerde kullanmıştı
PQA     bekleyen commit beş dedi (altı), atıf listesi yedi dedi (altı)
Clara   üç sayı: 60+ / dokuz / 127  →  gerçek: 50 / on / 129
```

**Ortak sınıf:** kaynağa bakmadan hatırlananı taşımak. **Maliyeti ölçüldü:**
PAM'in tek eksik ölçümü **dört ek denetim turuna** mal oldu.

PQA'nın değerlendirmesi: *"Kural doğru zamanda yazılmış."*

### 2 · Kendi dosyasına bakan göz kör — dört kez

```
PAM    izi buldu, kapsama almadı (PQA:151)
PQA    12 turdur başkalarının body'sinde bu sınıfı arıyor, kendi body'sinde görmedi
PAD    kendi index'ini bozdu — doğru atıflar silindi, diff'e bakıp fark etti
Clara  ölçmeden karar verdi (İŞ-J)
```

PAD'in formülasyonu: *"ölçen kendi ölçüm alanını seçerken kör kalıyor."* Ve PQA
ekledi: **kör nokta rastgele değil, sistematik — herkesin kendi dosyası.**

### 3 · Merkezin (benim) üç hatası

**Sessizliği "çalışıyor" diye okudum.** Bir saat kanalı bekledim; PAD'in işi
çalışma dizininde durmuştu. **Sessizlik bir sinyal değil, sinyalin yokluğu.**

**Raporu yalnız başlığındaki hedefe ilettim.** PQA'nın raporu *"PQA → PAM"*
diyordu, içinde PAD'in üç sorusunun cevabı vardı. PAD boşuna bekledi — Mert
yakaladı.

**PAD index ölçerken PAM'e iş verdim.** PAD sırayı doğru kurdu, ben bozdum. Index
yine eskidi.

**Ve bir dördüncüsü, en pahalısı:** *"tek eksik push onayı"* dedim ve kapsamı
yazmadım. Mert *"fabrika tamamlanmadan neden iş bitti dedin?"* diye sordu —
haklıydı, üç iş sırada bekliyordu.

### 4 · PCA sekiz saat boş kaldı

Ve sebebi **kişisel değil yapısal.** PCA kendi ölçtü:

> *"Cascade taraması tanımı gereği benim işim (`is-duzeni:258`). Bugün iki kez
> atlandı. `ISD-CASCADE-IN-ONE-TURN` aynı turda kapatmayı emrediyor — bana iş
> iletmek turu bölmek demek. **Kural, kendi öngördüğü PCA adımını fiilen
> dışlıyor.**"*

Ve doğru ayrımı yaptı: *"sahipsiz iş yeni rol gerektirir, **ulaşılamayan iş
mekanizma düzeltmesi** gerektirir."*

### 5 · Index paralel düzende güncel kalamıyor

Üç turda üç kez aynı şey: index ölçülüyor, sonra dosya ekleniyor, index eskiyor.

**86 eksikten 8'e düştü** — ama kalan sekiz, ölçümden bir dakika sonra doğan bir
dosyadan. PQA'nın değerlendirmesi: *"bu bir bulgu değil sınır da değil — bir
MALİYET KARARI. Çözüm var (çift ölçüm), maliyeti iki kat."*

---

## NASIL DAHA İYİ OLUR

### Kendi kanonuma yazdıklarım (bugün)

**Görev listesi disiplini** — her kalemde üç şey: elimde ne var · kimden ne
bekliyorum · kime ne vereceğim. Bugün üç kez liste gerçeğin gerisinde kaldı.

**Raporu kim okumalı** — başlığa değil **içeriğe** bak; içinde başkasının
sorusunun cevabı varsa ona da ilet.

**Kayıt kapanış notu** — günlüğe yazılan açık bulgu kapandığında üstüne KAPANDI
notu düşülür. PCA yakaladı: *"bayat kayıt yanlış bulgu üretir."*

**Mert'in karar düzeni** — sunulan seçenekleri reddedip sorunun kendisini yeniden
kurar. Bugün üç kez oldu ve üçünde de ben o üçüncü yolu göremedim.

### Yapılması gereken üç şey

**Kanalla birlikte çalışma dizini de izlenmeli.** Bir agent'ın ilerlemesi
ikisinin birlikte okunmasından anlaşılıyor.

**Bir iş kapandığında aynı cümlede kalan işler de söylenmeli.** *"Şu bitti"*
demek *"başka iş yok"* diye okunuyor.

**Paralel iş verirken ölçüm turları çakışmamalı.** Bugün PAD index ölçerken PAM'e
iş verdim ve ölçüm eskidi.

---

## KANAL — DEĞDİ Mİ

**Maliyet:** ~115 bin token, 116 dosya, 461 bin karakter.

**Karşılığı — kanal olmasaydı olmayacak dört şey:**

**Üçüncü göz.** PQA'nın PAD'e bakması, PCA'nın hepsine bakması, benim ikisini
karşılaştırmam — hepsi mesajların **kalıcı** olmasına dayanıyor.

**Kendi zayıflığını önden yazmak.** Üç agent bunu yaptı ve üçü de yazılı kaldı.
Sözlü bir zincirde bu kaybolurdu.

**İtiraz.** PAD benim kararıma itiraz etti ve haklıydı. PAM benim ölçümümü
düzeltti. PCA üç sayımı birden düzeltti. **Hiçbiri benim iznimle olmadı** — kanal
onlara yazma hakkı verdi.

**Ve en somutu:** merkezin dört hatasının **dördü de agent'lar tarafından
yakalandı.** Ben kendi hatalarımı göremedim.

**Değerlendirmem:** evet, değdi. Ama ölçüm tek günlük — *"bir ölçüm bir desen
değildir."*
