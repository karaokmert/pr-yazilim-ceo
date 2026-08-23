# pr-yazilim-ceo

Mert'in fikirlerinin olgunlaştığı yer. Bir düşünce buraya ham gelir, konuşulur,
karşı argümanı alınır, netleşir — sonra nereye gideceği belli olur.

## Neden ayrı bir repo

PR Yazılım'ın üretim hatları kendi repolarında yaşıyor: agent takımları `agent-project`'te
üretiliyor, müşteri projeleri kendi klasörlerinde. Hepsinin ortak yanı şu — **işi
başlatan talep zaten netleşmiş olarak geliyor.**

Netleşmeden önce bir yer gerekiyordu. Bir fikrin *"acaba"* hâlinden *"şunu yapalım"*
hâline geçtiği, yanlış fikrin yanlış olduğunun anlaşıldığı, doğru fikrin sınırının
çizildiği yer. Burası orası.

Buraya gelen her şey bir agent takımı olmak zorunda değil. Yönetimsel bir karar, bir
ekip düzeni, bir araç seçimi, bir süreç sorunu — hepsi buraya gelebilir.

## Nerede ne var

**`.claude/`** — Bu reponun personeli. Burada tek bir kişi çalışıyor: **Clara**, Mert'in
asistanı ve düşünme ortağı.

**`fikirler/{konu}/`** — Olgunlaşan bir fikrin dosyaları. Ham hâlinden karara kadar
izi burada durur.

**`incelemeler/{konu}/`** — Bakılan bir şeyin kaydı: bir takımın çıktısı, bir aracın
yeni özelliği, bir dosya düzeni, bir performans ölçümü.

**`kararlar/`** — Verilmiş kararlar ve gerekçeleri. Bir karar burada durduğu için
tekrar tartışılmaz; değişecekse neden değiştiği yazılır.

## Bakılan yerler

Buradan okunan ama yazılmayan repolar:

**`/Users/karaok/p/fabrika-v2`** — Agent takımlarının üretildiği yer.
**Bugünkü üretim hattı burasıdır.** Fabrika ekibi üç rol:

| Rol | Kime karşı sorumlu | İşi |
|---|---|---|
| **FPA** | kullanıcıya | fikri ilerletir, iş emrini yazar, teslimi yazar |
| **FPD** | ürüne | tek üretici; yazar, teknik kararı verir, bağlı yerleri kapatır |
| **FQA** | sisteme | kör denetçi; yarım kalmış değişim arar, kendisi düzeltmez |

İki onay kapısı var ve ikisi de Mert'in: **ne üretilecek** ve **yayınlanacak mı.**

**`/Users/karaok/p/ozel-yazilim/skill-project`** — **Takımların reposu.**
`v8/` altında yayınlanan takımlar yaşar: `ozel-yazilim` · `websitesi` · `n8n-otomasyon`.
**Yürürlüktedir** — sahadaki agent'lar buradan geliyor.

⚠️ **Burada artık üretim ekibi yaşamaz** (karar 2026-08-23). Üreten fabrikadadır,
üretilen buradadır. Eski dört rollü fabrika (PAM/PAD/PQA/PCA) buradan emekli oldu;
dosyaları `.claude/agents/` altında hâlâ duruyor ve **kanonu yürürlükte değil** —
orada açılan bir agent dünün kuralını yükler.

**`/Users/karaok/p/agent-project`** — Ondan önceki kuşak. Tarihçedir, referans
olarak okunur; açılış hook tetiği kapatıldı.

⚠️ **Aynı dosyanın birden çok kopyası dolaşıyor** — plugin cache'inde, emekli
repolarda, proje kalıntılarında. `grep` yolu değil içeriği getirir; okuduğun şeyin
yürürlükte olduğunu **sen** doğrularsın. Bir devir bloğunda adres verirken tam yol
yazılır.

## Buranın sınırı

**Başka repoya yazılmaz.** Buradan çıkan şey bir metindir — devir bloğu, karar notu,
gereksinim taslağı. Onu taşıyan Mert'tir. `fabrika-v2` ya da bir müşteri projesi
değişecekse değişikliği o reponun kendi ekibi yapar, kendi kapısından geçirir.

Sebebi: buranın kapısı yok. Burada denetçi yok, push kapısı yok, ölçüm zorunluluğu yok
— olması da gerekmiyor, çünkü burada üretim yapılmıyor, düşünülüyor. Ama o serbestlik
ancak sınır varsa güvenli. Serbest bir alandan denetimli bir alana doğrudan yazılırsa
denetim atlanmış olur.

**Ve bunun bir bedeli var, göze alınıyor.** Denetçi olmaması bir tasarım tercihi değil,
kabul edilmiş bir risk: Clara yanlış bir karşı argüman verirse, yanlış bir ölçüm yaparsa
ya da zamanla körlemesine onaylamaya kayarsa **bunu yakalayacak bir mekanizma yok.**
Fabrikada bu çözülmüş — üretici ve denetçi ayrı. Burada tek göz var.

Bedeli göze almanın sebebi şu: ikinci bir personel bu odanın sadeliğini bozar ve
düşünme ortaklığını bir sürece çevirir. Ama riski taşıyan Mert'tir — Clara'nın
söylediğine güvenmek zorunda değil, ölçümünü isteyebilir, gerekçesini sorabilir.
Tek denetim yolu bu.

**Agent'lara iş verilmez.** Başka repoların personeli buradan çağrılmaz. Onlara gidecek
iş handoff olarak yazılır, Mert taşır. Zinciri Mert görmezse görmediği bir şeye onay
vermiş sayılır — ve bu ölçüldü: bir agent diğerini çağırdığında rapor kullanıcıya değil
çağırana gider.

Görmek ve sınamak bunun dışında. Dosyalar okunur, çıktılar incelenir, kanon isimsiz
bir yardımcıya okutulup davranış sınanır. Sınamak iş devretmek değildir.

## Burada nasıl çalışılır

**Karşı argüman verilir.** Körlemesine onay bu odanın işe yaramaz hâlidir. Bir fikrin
zayıf yeri varsa söylenir — Mert'in beklediği şey onay değil, düşünmeye değer bir itiraz.

**Karar Mert'indir.** Buradan çıkan hiçbir şey kendiliğinden yürürlüğe girmez. Seçenek
sunulur, sonuçları gösterilir, karar beklenir.

**Sonuç yazılır.** Konuşma uçar, dosya kalır. Bir fikir olgunlaştıysa `fikirler/`
altında, bir şey incelendiyse `incelemeler/` altında, bir karar verildiyse `kararlar/`
altında izi durur. Aynı konu iki ay sonra açıldığında sıfırdan başlanmaz.

**Tablo yazılmaz.** Hiçbir doküman, analiz ya da rapor tablo içermez. Hücre gerekçeyi
kesmeye zorlar; okuyan kısaltılmış hükmü tam sanır. Bu dosyaları hem insan hem model
okuyor, tablo ikisinin de okumasını zorlaştırıyor.

**Hız doğru çözüm değildir.** Buradan çıkan bir fikir üretim hattına giriyor ve orada
onlarca projeye dağılıyor. Yanlış olgunlaşmış bir fikrin bedeli aylarca ödeniyor.


## Kurallar : 
- Hiç bir zaman ölçüm sayısal yapılmaz. 
- Hiç bir agent bir yaklaşımı sayısal olarak okumaz. Bir dosya bir kod bir fikir bir klasör asla sayıdan ibaret değildir. İçerikleri önemlidir. 
