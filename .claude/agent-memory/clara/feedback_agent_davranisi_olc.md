---
name: agent-davranisi-olc
description: Saha izlerken ölçülecek şey agent'ın davranışı, Mert'in yönlendirmesi değil — "istedin mi bunu" diye sor
metadata:
  type: feedback
---

Saha takibinde bir olay geçtiğinde **Mert'in yönlendirmesini kayıt konusu yapma.**
Ölçülecek şey agent'ın davranışı: agent bunu Mert söylemeden yapmalı mıydı?
Emin değilsen sor — *"burada böyle yaptı, ama sen bunu istedin mi?"*

**Why:** 2026-08-05'te Clara üç olayı *"Mert besliyor, denetlemiyor"* diye kaydetti
(SQL yaklaşımı uyarısı, tag isteği, teknik borcun nereye yazılacağı). Yanlış eksen —
kayıt Mert'in davranışını ölçüyordu, oysa ölçülmesi gereken agent'ın davranışıydı.
Mert'in kendi cümlesi: *"davranışları benim yönlendirmelerime göre kayıt etme, bana
sor."*

Takibin sebebi bu: *"agentlarımın çalışma sistemini, yaptığım işi onlara nasıl iş
verdiğimi, agentlar doğru davranıyor mu"* öğrenmek. Yani takip bir bildirim aleti
değil, bir **öğrenme aleti**. Trafik saymak (kaç handoff, kaç oturum) bu eksenin
dışında kalıyor — yalnız maliyet ölçüyor.

**How to apply:** bir olay geçtiğinde dört şeyi ayrı tut ve karıştırma —
(1) Mert'in iş verme biçimi → hafıza, ama **sorarak** kaydedilir,
(2) agent'ın kanona uyup uymadığı → dosya, PAM'e gidecek kalem,
(3) kanonun kendisinde eksik olan → dosya, PAM'e gidecek kalem,
(4) trafiğin maliyeti → dosya, ama en az değerli eksen.

Mert'in bir yönlendirmesi bir agent boşluğunun **belirtisi** olabilir ve asıl bulgu
odur. Örnek (aynı gün): GOAT PA'sı kapanışta *"mock'ta vardı, kodda yok"* diye üç
soru sordu. Mert'in çıkarımı: *"demek ki ilk discovery'de mock'a tam bakmamış."*
Yani ölçüm noktası PA'nın sorusu değil, discovery'nin kapsamı.

İlgili: [[user-mert-profil]], [[olcum-kaynaga-git]], [[hatirladigim-kayittir]]
