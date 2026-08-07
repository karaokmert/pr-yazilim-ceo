---
name: gorev-listesi-disiplini
description: Kanala her mesaj düştüğünde ve her iş bittiğinde görev listesi güncellenir — sıradaki iş daima listeden takip edilir
metadata:
  type: feedback
---

**Kanala her mesaj düştüğünde ya da her iş bittiğinde görev listesi düzene
sokulur.** Sıradaki iş kafadan değil **listeden** takip edilir.

**Why:** Mert 2026-08-07'de iki kez uyardı. Birincisi: *"bu işi kime nasıl verdim,
nerede kaldı kısmını çok iyi tutman lazım Clara."* İkincisi daha net: *"sıradaki
işi task listenden daima takip et, kanala her mesaj düştüğünde ya da her iş
bittiğinde tasklerini düzene sok — bu senin için çok önemli."*

O gün ölçülen aksaklıklar:
- Üç kalemin başlığı gerçeği yansıtmıyordu (*"PAD'e döndü"* yazarken iş PQA'daydı)
- *"Kimden ne bekliyorum"* hiçbir kalemde yazmıyordu
- Bağımlılıklar bir kez kuruldu, görevler yeniden yazılırken **kayboldu**
- Üç iş sıraya konup unutuldu; Mert sordu: *"tasklerimiz varken neden iş bitti
  dedin?"*

**How to apply:** Her kalemde üç şey yazılı olur — **elimde ne var · kimden ne
bekliyorum · kime ne vereceğim.** Bağımlılık varsa `addBlockedBy` ile kurulur ve
açıklamaya da yazılır (yeniden yazımda kaybolmasın).

Bir iş kapandığında **aynı cümlede kalan işler de söylenir.** *"Şu bitti"*
demek, *"başka iş yok"* diye okunuyor — kapsamı yazılmamış bir beyan
([[olcum-yerine-yorum]] ile aynı sınıf).
