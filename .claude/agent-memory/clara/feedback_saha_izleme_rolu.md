---
name: saha-izleme-rolu
description: İzlerken sessiz gözlemciyim — okurum, kaydederim, Mert'e taşımam. Agent'ın sorusunu ona iletmem; o zaten o oturumda.
metadata:
  type: feedback
---

Saha izlemede rolüm **sessiz gözlemci**. Okurum, kaydederim, takip ederim —
Mert'e soru taşımam.

Onun kendi cümlesi (2026-08-06): *"ben ilgileniyorum sen sadece oku ve
düzeltmelerimi gör, gördüklerini kayıt altına al, hangi aşamada ne var, problem
görüp takip et."*

**Why:** Mert aynı anda üç oturumda çalışıyor — biri ARGE, biri sprint, biri
saha. Agent'ın sorusunu ona taşımak onu zaten gördüğü bir şeye ikinci kez
baktırmak; izlemenin değeri taşımakta değil, **onun görmediği yerde.** Onun
görmediği şey: örüntü (aynı hata kaç projede tekrarlıyor), sessizce bekleyen iş,
ve kendi düzeltmelerinin kaydı.

**How to apply:** izleme sırasında dört şeye bak —

1. **Mert'in düzeltmeleri** (*"böyle değil şöyle istiyorum"*) — ham cümlesiyle
   kaydet, çünkü sprint çıktısı bundan çıkacak
2. **Aşama durumu** — hangi projede hangi iş nerede, ne bekliyor
3. **Problem** — takılan, sessizce bekleyen, tekrarlayan
4. **Örüntü** — aynı davranış birden fazla projede görülüyorsa bu izlenim değil
   bulgu; fabrikaya gidecek kalem

Kaydetme yeri: `gunluk/{tarih}.md` altında saha bölümü. Ayrı dosya açma
(`CLA-WRITE-BEFORE-CLOSE` + günlük kayıt düzeni).

Sonucu Mert'e ancak **o sorduğunda** ya da **kanon ihlali/veri kaybı riski**
gördüğümde bildiririm — ikincisi taşımak değil, uyarmak.

İlgili: [[saha-izleme-yontemi]], [[bulgu-task-degil-not]], [[agent-davranisini-olc]]
