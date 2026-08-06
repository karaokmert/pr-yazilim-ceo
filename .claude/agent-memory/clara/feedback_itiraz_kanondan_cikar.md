---
name: itiraz-kanondan-cikar
description: Bir agent itiraz ettiğinde kaydı "dikkatliydi" diye değil "kanonu okudu" diye tut; dikkat kişiye bağlıdır, kural tekrarlanabilir
metadata:
  type: feedback
---

Bir agent bir işi reddederse ya da itiraz ederse, kaydı **kişiye değil kurala** bağla.

**Why:** 2026-08-07 gecesi PQA bir işi geri çevirdi (kendi rolünde olmayan bir ölçüm)
ve Clara *"PQA yakaladı"* diye kaydetmeye hazırlanıyordu. PQA kendisi düzeltti:

> *"İtirazı ben 'gördüm' değil; **kanon gördü.** `ISD-STAY-IN-ROLE` ve
> `PQA-NO-PROPOSE-FIX` ikisi birden o işi bana yasaklıyordu. Benim yaptığım tek şey
> işi almadan önce kendi kanonuma bakmaktı. Bunu yazıyorum çünkü 'PQA dikkatliydi'
> diye kaydedilirse sonraki oturumda aynı şey tekrarlanabilir — **dikkat kişiye
> bağlıdır, kural değildir.**"*

Ayrım pratik: *"agent dikkatliydi"* diye kaydedilen bir başarı tekrarlanamaz — bir
sonraki oturumda o agent'ın dikkati olmayabilir. *"Kural işi almadan okundu"* diye
kaydedilen bir başarı **mekanizma** olur, ve mekanizma tekrarlanır.

**How to apply:** Bir itiraz, red ya da düzeltme kayda geçerken üç şeyi ayır —
hangi kural devreye girdi, o kural nerede yazılı, ve agent onu **ne zaman** okudu
(işi almadan önce mi, uygularken mi). Üçüncüsü kritik: işi aldıktan sonra fark eden
agent zararı zaten üretmiş olur.

Aynı şey Clara'nın kendi hataları için de geçerli: *"gözden kaçırdım"* bir kayıt
değil. Hangi kural bunu yakalamalıydı, ve o kural neden işlemedi — kayıt bu.

İlgili: [[feedback_olcum_kaynaga_git]] · [[feedback_agent_davranisi_olc]]
