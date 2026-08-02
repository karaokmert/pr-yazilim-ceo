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

**`/Users/karaok/p/agent-project`** — Agent takımlarının üretildiği yer. Fabrika ekibi
(PAM, PAD, PQA, PCA) burada yaşıyor, ürettikleri takımlar `team/` altında birikiyor.
Bugünkü üretim hattı burasıdır.

**`/Users/karaok/p/ozel-yazilim/skill-project`** — Önceki kuşağın reposu. v7 ve v8
agent'ları, ölçümler, araştırma kayıtları orada. Referans olarak okunur; oradaki kanon
yürürlükte değil, tarihçedir.

İkisi ayrı repo ve karıştırılmamalı. Bir devir bloğunda adres verirken hangisi olduğu
tam yazılır — *"agent-project"* ile *"skill-project"* arasındaki fark, yürürlükteki
kanon ile emekli kanon arasındaki farktır.

## Buranın sınırı

**Başka repoya yazılmaz.** Buradan çıkan şey bir metindir — devir bloğu, karar notu,
gereksinim taslağı. Onu taşıyan Mert'tir. `agent-project` ya da bir müşteri projesi
değişecekse değişikliği o reponun kendi ekibi yapar, kendi kapısından geçirir.

Sebebi: buranın kapısı yok. Burada denetçi yok, push kapısı yok, ölçüm zorunluluğu yok
— olması da gerekmiyor, çünkü burada üretim yapılmıyor, düşünülüyor. Ama o serbestlik
ancak sınır varsa güvenli. Serbest bir alandan denetimli bir alana doğrudan yazılırsa
denetim atlanmış olur.

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
