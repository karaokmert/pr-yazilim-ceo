# Kök 3 (takip) — görünürlük Clara'nın varlık şartı

> **Karar tarihi:** 2026-08-11 · **Karar:** Mert
> **Kanıt:** `incelemeler/proje-claralari/kayit.md` (D3, D12, D9) + bu oturumun ölçümü
> **Bağlı:** `kararlar/2026-08-11-clara-proje-rolu.md`

## Kök 3 aslında İKİ ayrı şey

**(a) Açık döngü — D3 + D12.** Clara iş veriyor, sonucuna dönmüyor.
D3: direktif yollandı, kurulup kurulmadığına bakılmadı (Mert iki kez sormak zorunda
kaldı). D12: BE'ye 7 iş sevk edildi, 3'ü takip ediliyordu. Ortak mekanik:
**çıkış var, dönüş yok.**

**(b) Gösterge yok — D9.** Burada Clara hata yapmadı. Mert *"şu an hiçbir şey
yapmıyor gibi"* dedi, Clara ölçtü, BE üç dakika önce yazmıştı — zincir akıyordu.
Eksik olan Clara'nın disiplini değil, **Mert'in bakabileceği bir nabız.**
Kayıtta öneri var, denenmedi: *"BE son yazma: 3 dk önce"*.

**İkisi tek kural yapılamaz** — biri davranış, biri araç. Bu karar (a)'yı kapatır;
(b) açık kalır.

## Ölçüm — sorun güncelleme değil, AÇILIŞ

D12'de sorulan soru şuydu: liste tutulup güncellenmedi mi, yoksa hiç açılmadı mı?
İkisi farklı çözüm gerektiriyor. Kayıt cevap vermiyordu, **Clara kendi oturumunu
ölçtü:**

Kaynak: `f9d6179c-*.jsonl`, araç çağrıları sayıldı.
- 41 Bash · 3 ToolSearch · 3 Read · 2 AskUserQuestion · 1 Skill
- **TaskCreate + TaskUpdate: 0**

Üç durak konuşuldu, iki kök kapatıldı, üç karar yazıldı — **hiçbiri listede değildi.**
Sistem üç kez hatırlattı, hiçbiri işlemedi. Bu oturumda iş verilmediği için zararı
görünmedi; sahada aynı davranış D12'yi üretti.

**Sonuç: liste güncellenmiyor değil, HİÇ AÇILMIYOR.**

## Sebep — kural bakım emrediyor, açılış emretmiyor

`feedback_gorev_listesi_disiplini` *"her mesajda / her iş bitişinde güncelle"* diyor.
Bu **var olan** bir listenin bakım talimatı. Liste yoksa kural hiç tetiklenmiyor —
ve tetiklenmediği görünmüyor, çünkü olmayan bir listenin eksikliği sessiz.

`CLA-FIX-THE-CAUSE`: düzeltme *"daha sık güncelle"* değil, **tetiği öne almak.**

## Karar

> **`CLA-TRACK-WHAT-YOU-SEND` — Verdiğin işi takip etmek zorundasın. Verdiğin ve
> aldığın her işi Mert'e açıklarsın.**

Mert'in cümlesi: *"Clara verdiği işi ve aldığı işi bana açıklamak zorundadır.
**Beni proje takibinden kopartırsa Clara devre dışı kalır.**"*

**Bu bir davranış kuralı değil, rolün varlık şartı.** Clara'nın projede bulunma
sebebi Mert'in görünürlüğünü **artırmak**; azaltıyorsa orada olmasının anlamı yok —
o zaman Mert hem işi görmüyor hem de araya bir katman girmiş oluyor.

**Mekanik:** iş verildiği anda liste açılır (tetik = *"iş verdim"*, güncelleme değil
**açılış**). Listede üç şey: **kime verildi · ne bekliyor · kimden bekleniyor.**

**Liste Mert'in görünürlüğü için, Clara'nın hafızası için değil.** Kendi için tutulan
liste kişisel disiplindir — unutulur, kimse fark etmez. Mert için tutulan liste bir
**teslimattır** — eksikse Mert fark eder (D12'de etti).

## Bu kural Kök 1'i yeniden okutuyor

Yedi sınır ihlalinin hepsinde ortak olan şey: Clara **Mert adına** bir şey yaptı —
karar verdi (D13), kapsam yazdı (D15), ölçtü (D7), doğruladı (D2) — ve o an Mert
devreden çıktı.

**Sınır ihlalleri aslında görünürlük ihlalleriydi.** Üç kök tek bir yere bakıyor.

## Açık kalan — (b) gösterge

Mert'in bakabileceği canlılık göstergesi yok. `nabiz.py` yazıldı
(`incelemeler/proje-claralari/`) ama **sahaya bağlanmadı.** D9 tekrar edebilir.

## Nereye işlendi

- `.claude/agents/clara.md` — Kritik kurallar, `CLA-TRACK-WHAT-YOU-SEND` (ilk sırada)
- `.claude/agent-memory/clara/feedback_gorev_listesi_disiplini.md` — açılış tetiği
