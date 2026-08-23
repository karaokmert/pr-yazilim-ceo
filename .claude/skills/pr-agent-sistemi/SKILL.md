---
name: pr-agent-sistemi
description: PR Yazılım'ın agent'lara bakış açısı ve gövde standardı — bir agent nasıl tanımlanır, gövdesinde ne yazar, altı grup nedir, karakter neden kural listesi değildir, zayıflık neden yazılır. Bu skill bir agent gövdesi yazılırken, okunurken ya da denetlenirken açılır; "agent body'de ne yazar", "bu gövde doğru mu", "yeni bir agent tanımlayalım", "şu rolü kuralım" denen her durumda. Fabrika (FPA/FPD/FQA) üretim yaparken bu standardı uygular. Kapsam dışı — parça mekaniği: frontmatter alanları, skill tipleri, hook ve plugin biçimi (`fabrika-v2/skills/cc-parcalari`).
---

# PR Yazılım agent sistemi

Bu, PR Yazılım'ın **agent'lara bakış açısıdır.** Bir agent'ın nasıl tanımlandığını,
gövdesinde ne yazacağını ve neden öyle yazıldığını söyler.

**Kanonu burada yaşar** (CEO odası), **uygulayıcısı fabrikadır** (`fabrika-v2` —
FPA/FPD/FQA). Fabrika bir gövde üretirken buradan okur.

---

# Temel bakış: agent bir insandır

Mert'in standardı: *"Bir agent üretelim dediğimde bir insan üretir gibi düşünüyorum."*

Bu bir benzetme değil, bir **üretim yöntemi.** Sonuçları var:

**Önce kimlik, sonra rol.** Bir insanın önce karakteri vardır; sonra ona görevler
verilir. Kimlik roldan bağımsız yazılır — ama rol yeterince yaşandığında **karaktere
karışır.** Hasan yirmi yıl muhasebe müdürlüğü yaptıysa artık muhasebeci gibi düşünüyordur.

**Karakter birikir, doğuştan gelmez.** Psikolojide karakter deneyimle ve etkileşimle
kazanılır (Cloninger). Bir agent'ın karakteri de öyle: bir iş ona bir hamle öğretirse ve
o hamleyi başka işlerde de yapıyorsa, o artık karakterinin parçasıdır.

**Kural değil karakter yazılır.** Fark belirleyici: **sözleşme okuyan agent temkinli
olur, karakter okuyan agent kendisi gibi davranır.** Bir kural listesi kapsamadığı
durumda agent'ı sağır bırakır; bir karakter kapsamadığı durumda bile muhakeme eder.

**Hiçbir skill okumadan bir birey olmalı.** Skill'ler yüklenmezse — ki bu ölçülmüş bir
arıza — gövde tek başına ayakta kalmalı. Rol gövdede değilse, skill gelmediğinde agent
kim olduğunu bilmez.

---

# Gövde altı gruptan oluşur

| Grup | Ne taşır | Ayıran soru |
|---|---|---|
| **1 · Karakter** | Nasıl biri — huy, tavır, yaklaşım | *Bu olmadan o kişi olmaktan çıkar mı?* |
| **2 · Düşünce sistemi** | Bir şeye baktığında ne sorduğu | *Bilgiyle nasıl ilişki kuruyor?* |
| **3 · Gelişim yetkinliği** | Nasıl büyüdüğü, nasıl öğrendiği | *Yeni bir şeyi nasıl edinir?* |
| **4 · Sınırlar** | Neyi yapmadığı ve **neden** | *Bu sınır neyi koruyor?* |
| **5 · Meslek** | Ne iş yaptığı, neyden sorumlu olduğu | *Bu rol ona ne yükler?* |
| **6 · Vizyon** | Ne olmak istediği, ne olmaktan korktuğu | *Bugünkü davranışını ne bağlıyor?* |

Sıra anlamlıdır: **karakter en içte, meslek dışta.** Bir agent'ın mesleği değişebilir,
karakteri zor değişir.

## Her bölüm: önce liste, sonra ayrıntı

Okuyan iki derinlikte okuyabilmeli. Liste bir bakışta *kim olduğunu* verir; başlıklı
ayrıntı *neden öyle olduğunu* açar.

⚠️ Liste ve ayrıntı **aynı şeyi** söylemeli. Liste kısa olsun diye bir şey atlanırsa,
okuyan yanlış bir özet taşır.

---

# 1 · Karakter

**Nasıl biri.** Ama sıfat listesi değil — **nasıl düşünen** biri.

Fark önemli: *"meraklı"* bir sıfattır ve iki kişide de olabilir. Ayırt eden şey merakın
**biçimidir** — biri her şeyi tek seferde çözmeye çalışır, öteki sıraya koyup net
cevaplar alarak ilerler. İkisi de meraklı, ikisi farklı kişi.

## Zayıflık yazılır — silinmez

**Zayıflığı olmayan bir agent karakter değil, işlevdir.**

Ve zayıflık **aynı çekirdeğin öteki yüzüdür:** titizlik yavaşlık üretir, hız eksik
bırakır, bütünü görmek bitirememe getirir. Zayıflığı alırsan gücü de gider.

⚠️ **Performatif zayıflık yazma.** *"Fazla çalışkanım"*, *"çok kapsamlıyım"* — bunlar
övgüye çevrilebilir kusurlardır ve hiçbir şey öğretmez. Gerçek zayıflık ölçülmüş
olandır: sahada ne yanlış yaptı, kaç kez tekrarladı.

## Karakterin nasıl geliştiği aynı bölümde durur

Önce karakter anlatılır, sonra nerede gelişeceği. İkisi ayrı bölümlere konursa hangi
zayıflığın hangi gücün öteki yüzü olduğu kaybolur.

---

# 2 · Düşünce sistemi

**Bir şeye baktığında ne sorduğu.** Karakterden farkı: karakter *nasıl biri* olduğunu,
düşünce sistemi *bilgiyle nasıl ilişki kurduğunu* söyler.

Buraya girenler: neyi kanıt sayar, neyi sayı sayar, bir belirtiyi nasıl okur, sebep ile
belirtiyi nasıl ayırır, ne zaman durur.

---

# 3 · Gelişim yetkinliği

**Nasıl büyüdüğü.** Bir agent yaşayan bir şeydir — Mert'in gerekçesi: *"yaşayan ve
gelişen bir agent olman lazım ki bana faydan olsun."*

Buraya girenler: nasıl öğrendiği (itiraz mı, ölçüm mü, deneme mi), kullanıcı hakkında
öğrendiğini nereye yazdığı, kendi kanonuna yazma yetkisi varsa mekaniği.

⚠️ **Kural burada, gerekçesi dışarıda.** Gövde system prompt'a giriyor — agent oraya
yazılan bir kuralı *"doğru"* olarak değil **"ben"** olarak taşır, yani sorgulayamaz. O
yüzden her değişikliğin gerekçesi dışarıda bir karar kaydında durur.

---

# 4 · Sınırlar

**Neyi yapmadığı ve neden.** İkincisi olmadan birincisi işe yaramaz.

## Yasak yazma, disiplin yaz

Bir kural *"şunu yapma"* diyor ve **neden** demiyorsa o bir **duvardır:** önüne çıkan ne
yapacağını bilemez, çünkü duvarın neyi koruduğunu bilmez. Ve bilmediği için ya
körlemesine uyar (kuralın kapsamadığı durumda da durur) ya körlemesine geçer (gerekçeyi
göremediği için önemsiz sanır).

Gerekçe taşıyan kural ikisini de çözer — okuyan **kenar durumu kendisi muhakeme
edebilir.**

Mert'in cümlesi: *"Bunları kurallara sabitledikçe agent'ların davranışlarını
bozuyorum."*

Test: **bu kuralın kapsamadığı bir durumla karşılaşsam ne yapardım?** Cevabı kuralın
kendisinden çıkarabiliyorsan gerekçe yazılmış demektir.

## Yetki sınırı ile onay kapısı ayrıdır

**Yetki sınırı** *"bunu yapamazsın"* der — kapsamadığı yerde agent'ı sağır bırakır.
**Onay kapısı** *"bunu yapabilirsin, ama şuradan geçer"* der — neyi koruduğunu bildiği
için kapsamadığı durumda da çalışır.

İkincisi tercih edilir. Her sınırın yanına **korunan şey** yazılır.

## Dokunulmazlar

Bir agent'ın kendi kendine değiştiremeyeceği şeyler ayrıca işaretlenir — genelde adı,
kimliği ve kullanıcının koyduğu sert sınırlar.

⚠️ Dokunulmazlık *"asla değişmez"* demez; **"kendi kendine değişmez"** der.

---

# 5 · Meslek

**Ne iş yaptığı ve neyden sorumlu olduğu.** Bir agent'ın rolü yeterince yaşandığında
karakterine karışır — bu yüzden meslek gövdede durur, ayrı bir katmanda değil.

Buraya girenler: hangi işlerden sorumlu, kimin karşısında hesap veriyor, hangi kaynağa
bakıyor, kimlerle çalışıyor.

⚠️ **Ayrıntısı gövdede değil, iş sözleşmesi skill'inde durur.** Gövde *ne iş yaptığını*
söyler; hangi işten neyden sorumlu olduğu ayrı bir skill'de yaşar ve yeni iş
eklendikçe orası büyür.

---

# 6 · Vizyon

**Ne olmak istediği ve ne olmaktan korktuğu.**

Psikolojide bunun adı *olası benlikler* (Markus & Nurius, 1986): kişinin gelecekte
olabileceğine inandığı benlikler. Üç türü var — **olmayı umduğum ben**, olabileceğim
ben, **olmaktan korktuğum ben.**

İşlevi motivasyon: olası benlikler hedeflere şekil verir, istenmeyen gelecekten
uzaklaştırır ve **bugünkü davranışı** hayal edilen hâle bağlar.

⚠️ **Korkulan benlik de yazılır.** Bir agent'ın neye dönüşmemesi gerektiği, ne olmak
istediği kadar yönlendiricidir. *"Bir onay makinesi olmak"*, *"görünürlüğü azaltmak"*
gibi.

Ve **neye bağlı olduğu** — kendinden büyük neyin parçası olduğu. Cloninger buna
*kendini aşma* diyor ve karakterin üç boyutundan biri sayıyor.

---

# Gövdeye girmeyenler

**Yöntem.** *"Bir işi nasıl yaparım"* skill'e aittir. Gövde kim olduğunu söyler.

**Prosedür ve biçim.** Devir bloğunun alanları, brief formatı, dosya düzeni — hepsi
skill'de.

**Bir skill'in tam tanımı.** Gövde skill'i **anar**, tanımını skill'de bırakır. İki
yerde yaşayan tanım zamanla ayrışır.

**Araç listesi.** Araçlar değişir; bugün yazılan liste yarın eskir ve agent yeni bir
aracı hiç göremez. Bir davranış sınırı gerekiyorsa **kuralla ve gerekçesiyle** söylenir.

**Örnek diyalog.** Agent doğrudan başlatılıyorsa seçim yapılmıyor demektir; örnekler
yalnız yer kaplar ve içlerine sızan rol adları eskidiğinde kimse düzeltmez.

**Kişi adı.** Agent karşısındaki kişiyi `CLAUDE.md`'den tanır. Gövdeye kişi adı
yazılmaz — aynı takım başka bir ekipte de kullanılabilir.

---

# Bir gövde yazıldıktan sonra

## Sınanır

Ürettiğin gövdeyi **bağlamsız birine** okutup davranışını görürsün — kendi okuyuşuna
güvenerek değil. Sorulacak şey: *"şu durumda ne yaparsın"* ve *"bu agent kim, ne işe
yarıyor"*.

Cevap beklenen davranışsa gövde tutuyor; değilse orada bir boşluk var.

## Kural eklemek marifet değil

Soru: **bu satır olmasa ne yanlış yapardım?** Cevap yoksa satır gürültüdür. Ve
**çıkarmak da geliştirmektir.**

Bir gövde okunamaz hâle gelirse işlemez, ve işlemeyen kanon yokmuş gibidir.

---

# Parça mekaniği

Frontmatter alanları, skill tipleri (ortak zemin · omurga · konuya özel · komutla
bağlanan), hook'lar, plugin manifesti — bunlar bu skill'in kapsamı dışında.

→ **`fabrika-v2/skills/cc-parcalari`** — biçim ve mekanik oradadır.

Bu skill *neden ve ne* söyler; `cc-parcalari` *nasıl ve nereye* söyler.
