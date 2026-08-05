---
name: bulgu-task-degil-not
description: Bulgu task'e çevrilmez, nota düşülür — task listesi karışıyor, notlar sonraki oturumda okunur
metadata:
  type: feedback
---

Bir bulgu çıktığında onu **iş kalemi / task yapma.** Nota düş, sonraki oturumda
bakılır.

**Why:** Mert'in cümlesi (2026-08-05, 19:03, GOAT kapanışında bir agent'a):
*"notlara düş, bulguyu task'e çevirme, sonra çok karışıyor. Not al, işi ilerki
session'larda bakarız."* Aynı gün beş projede paralel iş yürüdü ve her modül
kapanışı birkaç bulgu üretti — hepsi task olsaydı liste asıl işi gömerdi.

**How to apply:** Clara tarafında karşılığı: bulgular `gunluk/{tarih}.md`'ye başlık
olarak birikir, `TaskCreate` ile iş kalemi açılmaz. Aynı şey PAM'e gidecek kalemler
için de geçerli — birikirler, devir bloğu yazılırken toplanır, tek tek iş olarak
akmazlar.

Not: bu, kaydı ERTELEMEK değil. Kayıt aynı turda yazılır
([[gunluk-kayit-duzeni]], `CLA-WRITE-BEFORE-CLOSE`); ertelenen şey yalnız o kaydın
İŞE dönüşmesi.

İlgili: [[gunluk-kayit-duzeni]], [[cevap-uzunlugu-ve-karar-alma]], [[user-mert-profil]]
