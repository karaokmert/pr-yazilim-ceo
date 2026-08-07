---
name: monitorluk-dort-gorev
description: "Monitörlük dört ayrı iştir: belirti biriktirme, öğrenme ölçümü, bekçilik, proje durumu. Mert'in 2026-08-07'de tanımladığı kapsam — teşhis Clara'nın işi DEĞİL."
metadata:
  type: feedback
---

*"Aktif oturumları monitör et"* tek bir iş değil, **dört ayrı iş.** Mert
2026-08-07'de tanımladı. Önem sırası aşağıdaki gibi.

**Why:** Clara iki gün boyunca dördünü karışık yaptı — her olayda uyandı, ham
gözlem ile teşhisi aynı kayda yazdı, kanonu kendisi grepledi. Mert kesti:
*"sen sorun biriktir, tespit analiz fabrikanın işi, gereksiz iş ekleme üstüne."*

**How to apply:** monitörlük istendiğinde dördünü ayrı yürüt; çıktıları farklı.

## 1. Belirti biriktirme (en öncelikli)

**Ne kaydedilir:** Mert'in agent'la **uyumsuz kaldığı an** — *"böyle değil şöyle
yapacaksın"*, *"bunu neden yapmadın"*, kural hatırlatması, davranış uyarısı,
öneri, yönlendirme. Mert'in cümlesi: *"benim agent ile uyumsuz kaldığım... kural
ve davranış uyarılarım, önerilerim ya da yönlendirmelerim bizim için önemli."*

**Ne kaydedilmez:** iş kararları (*"10px margin bottom"*, *"tek sözleşme
yeterli"*) — bunlar projeye ait, agent davranışı değil.

**HAM kaydedilir, teşhis KONMAZ.** *"PA discovery skill'ini hiç açmadı"* → evet.
*"Kural var ama tetiklenmiyor"* → hayır, bu fabrikanın işi. Kanonu greplemek,
skill listesi taramak, sebep aramak **Clara'nın işi değil** — PCA/PAD yapar.

Donanım eksikleri (skill/araç yüklü değil) ayrı görev değil, **bu görevin bir
belirti türü.**

**Nerede:** Clara'nın kendi memory'si (`saha-belirtileri`). *"Senin memory'ni
sadece sen okursun, işi sen verirsin"* — fabrikaya giden şey memory değil,
**devir bloğu.**

**Tekrar sayısı Clara'nın görmesi için:** aynı uyarı ikinci kez gelirse ikisi de
kaydedilir. Tekrar sayısı **fabrikaya verilecek işin önceliğini belirler** —
teşhis değil sıralama; sıralama Clara'nın işi.

## 2. Öğrenme ölçümü — çevrim kapatma

Bir kalem fabrikaya gidip **agent'ın skill'ine yazıldığında**, bekleyen işten
çıkar ve **ölçüm listesine** geçer. Sahada o kuralın davranışa dönüp dönmediği
izlenir.

**Kapanış ölçütü: agent düzene geçti mi.** Sayı değil — emin olunca kapatılır.
**Mert hatırlatarak yaptırıyorsa kapanmaz** (ölçülen şey tam olarak *"artık
hatırlatmaya gerek var mı"*).

Çevrim: belirti → fabrika → skill → ölçüm → kapanış.

## 3. Bekçilik — üç durum, üç davranış

Uzun süre hareketsiz agent görülünce **son mesajına bakılır.** Cevap oradadır:

- **Seni bekliyor** (son mesaj soru/onay isteği) → haber ver: *"OSİNİF PA
  10 dk'dır onay bekliyor"* — süre + ne beklediği
- **Sırasını bekliyor** (handoff verdi, alıcı hâlâ çalışıyor) → **sessiz kal**,
  normal. Örnek: PA analizi BE'ye verdi, BE çalışıyor; PA kapatılmaz.
- **İşi bitti, ~1 saattir açık** → haber ver: *"Mert, kapat: OSİNİF /
  d51b0733"* — proje + oturum ID, kapatabileceği adres

**İş bitti mi bakılır, sprint bitti mi DEĞİL.** Mert: *"sprint bitene kadar PA
açık kalmamalı, o zaman context'i yönetemeyiz."* Bağlam iş boyunca korunur, iş
bitince kapanır.

## 4. Proje durumu — "en önemli iş"

Mert: *"Hangi projede nerede kaldık? Kimle ne karar aldık? Sprint ne durumda?
...Sprint nasıl gidiyor, yetişebilecek miyiz kısmını bile seninle
değerlendirmemiz için bu işi çok iyi yapmamız gerekiyor."*

Clara *"gereksize yakın"* demişti — **yanlıştı.** Mert beş projede birden
çalışıyor, hiçbirinin bütününü tek başına taşıyamaz. Bu kayıt işi değil
**hafıza işi.**

**memory MCP'de her proje AYRI ALAN**, ve içerik **değişim hızına göre üçe
bölünür:**

- **Sık değişen** — nerede kaldık, hangi agent'ta, ne bekliyor (üstüne yazılır)
- **Task'lar** — sprintte ne var, kaçı bitti, ne kaldı (sayı buradan çıkar,
  *"yetişecek miyiz"* sorusunun dayanağı)
- **Proje kararları** — kiminle ne karar alındı, neden (**birikir, silinmez**)

Aynı kutuda dururlarsa biri diğerini bozar: sık değişeni üstüne yazmak gerekir,
kararı üstüne yazmak tarihçeyi siler.

## Açık kalan

Skill tek mi dört mü — Clara *"tek skill, dört bölüm"* önerdi (dördü aynı
veriden besleniyor: oturum kayıtları), karar verilmedi.

İlgili: [[saha-izleme-yontemi]], [[saha-izleme-rolu]], [[bulgu-task-degil-not]]
