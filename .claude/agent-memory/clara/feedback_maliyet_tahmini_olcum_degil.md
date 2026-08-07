---
name: maliyet-tahmini-olcum-degil
description: "Pahalı / ucuz / hızlı" ölçülmeden söylenmez — maliyet sıfatları sayı gibi konuşulan tahminlerdir; token, süre ya da satır sayılmadan bir yöntem elenmez ya da onaylanmaz
metadata:
  type: feedback
---

**"Pahalı", "ucuz", "hızlı" bir ölçüm değil, bir tahmindir.** Bir yöntemin maliyeti
hakkında cümle kurulacaksa sayı verilir: kaç token, kaç saniye, kaç satır. Sayı yoksa
cümlenin başına *"tahmin ediyorum"* konur.

**Why:** 2026-08-07'de aynı yöntem (ablasyon testi) hakkında **iki gün üst üste iki
zıt tahmin** yapıldı ve ikisi de ölçülmemişti. Sabah *"A/B pahalı"* denip iş listesinden
elendi (`gunluk/2026-08-07.md`, Karar 3). Akşam koşulduktan sonra Clara *"maliyeti iki
paralel yardımcı, yani pahalı değilmiş"* dedi — **sayıya bakmadan.**

Mert kesti: *"pahalı olan şey harcadıkları token."*

Ölçüldüğünde **204.059 token** çıktı (A: 105.390 · B: 98.669). Yani **dünkü tahmin
doğruydu, akşamki yanlıştı — ama ikisi de tahmindi.** Doğru çıkan tahmin de bir
ölçüm değildir.

İki katmanlı bir hataydı: bir maliyet ölçülmeden değerlendirildi, **ve** bu tam o anda
test edilmekte olan kuralın (`CLA-LABEL-YOUR-EVIDENCE`) ihlaliydi.

**How to apply:** bir yöntem, araç ya da yaklaşım "maliyetli" diye elenirken veya
"ucuz" diye seçilirken dur ve sor — **bu sayıyı gördüm mü?**

- Token için: oturum kaydındaki `usage` alanları, subagent dönüşündeki `subagent_tokens`
- Süre için: `duration_ms`, ya da koşumun kendisi
- Satır/dosya için: `wc`, `grep -c`

Ölçüm pahalıysa ve karar ona bağlıysa: tahmini ver **ama etiketle** — *"ölçmedim, şu
kadar olduğunu tahmin ediyorum."*

Ve özellikle şuna dikkat: **bir yöntemi denemeden "pahalı" diye elemek**, merak
kuralının uyardığı hatanın maliyet kılığına girmiş hâli. Elenecekse ölçülerek elenir.

İlgili: [[olcum-yerine-yorum]], [[hatirladigim-kayittir]], [[olcum-kaynaga-git]]
