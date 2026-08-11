---
name: gorev-listesi-disiplini
description: İş VERİLDİĞİ ANDA liste açılır (tetik: 'iş verdim'), her mesaj/her iş bitişinde güncellenir — Mert'in görünürlüğü için, Clara'nın hafızası için değil
metadata:
  type: feedback
---

**İŞ VERİLDİĞİ ANDA liste açılır.** Tetik *"iş verdim"* — güncelleme değil **açılış.**
Sonra: kanala her mesaj düştüğünde ya da her iş bittiğinde düzene sokulur. Sıradaki iş
kafadan değil **listeden** takip edilir.

⚠️ **Liste Mert'in görünürlüğü için tutulur, Clara'nın hafızası için değil.**
Bu ayrım çözümü belirliyor: kendi için tutulan liste kişisel disiplindir, unutulur ve
kimse fark etmez; Mert için tutulan liste bir **teslimattır** — eksikse Mert fark eder.
Kural gövdede: `CLA-TRACK-WHAT-YOU-SEND` (*"beni proje takibinden kopartırsa Clara
devre dışı kalır"*).

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

**Ve asıl boşluk buydu — ölçüldü (2026-08-11):** bu kural *"güncelle"* diyordu, yani
**var olan** bir listenin bakımını emrediyordu; **açılmasını** emretmiyordu. D12'de olan
tam bu: BE'ye 7 iş sevk edildi, **liste hiç açılmadı**, Mert sordu, Clara *"3 iş"* dedi.
Aynı düzeltme **beş dakika arayla iki Clara'ya birden** gitti — kişisel dalgınlık değil.
Ve aynı gün Clara'nın kendi oturumunda: 41 Bash · 3 Read · **0 görev kalemi.**

**How to apply:** Her kalemde üç şey yazılı olur — **elimde ne var · kimden ne
bekliyorum · kime ne vereceğim.** Bağımlılık varsa `addBlockedBy` ile kurulur ve
açıklamaya da yazılır (yeniden yazımda kaybolmasın).

Bir iş kapandığında **aynı cümlede kalan işler de söylenir.** *"Şu bitti"*
demek, *"başka iş yok"* diye okunuyor — kapsamı yazılmamış bir beyan
([[olcum-yerine-yorum]] ile aynı sınıf).
