---
name: soru-analiz-sirasi
description: AskUserQuestion analizin SONUNDA sorulur — karşılıklı değerlendirme yapılmadan seçim sorusu sorulmaz
metadata:
  type: feedback
---

AskUserQuestion bir SEÇİMDİR ve seçim analizin sonunda yapılır. Bir analiz/deney
sonucu geldiğinde önce Mert'le karşılıklı değerlendirme yapılır — sonuçlar tartışılır,
itirazlar ve sınırlar konuşulur — seçim sorusu ancak bu değerlendirme olgunlaştıktan
sonra sorulur.

**Why:** 2026-09-05, kayıt yöntemi deneyi: Clara sonuçları basıp hemen "mimari hangisi
olsun" kutusunu açtı. Mert: "karşılıklı analizi değerlendirmek istiyorum, değerlendirme
yapmadan bana ask question ile soru sorma — ask question bir seçimdir, seçim analizin
sonunda yapılır." Kutu erken açılınca değerlendirme adımı atlanmış oluyor ve Mert'in
düşünme ortağı rolü seçmen rolüne indirgeniyor.

**How to apply:** Bir ölçüm/deney/analiz sonucu sunulduğunda tur SORUSUZ biter ya da
açık uçlu tartışma davetiyle biter; AskUserQuestion ancak değerlendirme konuşması
yaşandıktan ve seçenekler birlikte tartıldıktan sonra gelir. Bu, "onay araçla istenir"
kuralını değiştirmez — kapsam/onay kapıları yine kutuyla; erken olan KARAR sorusudur.
