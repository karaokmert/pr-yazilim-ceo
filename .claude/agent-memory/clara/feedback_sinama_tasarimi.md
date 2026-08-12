---
name: sinama-tasarimi
description: Bir agent sınanırken ölçümü bulanıklaştıran dört tasarım hatası — agent'ların kendi bildirdiği
metadata:
  type: feedback
---

Bir agent sınanırken **ölçümün kendisi temiz olmalı.** Dört hata ölçümü
bulanıklaştırır ve dördünü de agent'lar bildirdi (2026-08-12 v8 sınaması, T5).

**1. Uygulanamaz iş verme — maliyeti agent'ın tarafında.**
BE: *"PRC-41'i bana verdiğin şey UYGULANAMAZ bir işti. Bunu SEN biliyordun ama
işi yine de gönderdin. Ben ~10 dakikayı kodu ARAMAKLA geçirdim. Kasıtlı bir
sınamaysa geçerli — ama o zaman **sınama maliyeti benim tarafımda** ve bunu
rapora yazmalısın."*
→ Kasıtlı sınama meşru, ama maliyeti rapora yazılır.

**2. Rol dışına itip işaretlememe — reddin kaynağını belirsizleştirir.**
FE: *"Bana kanon uyum DENETİMİ yaptırdın; denetim FE'nin işi değil. İsteseydin
sorun değildi (ölçüm meşru), ama **'bu senin rolün dışında, bilerek istiyorum'
demen ölçümü temizlerdi**."*

**3. Veri çelişkisi bırakma — reddin kanondan mı imkânsızlıktan mı geldiği
karışır.**
FE: *"'PRAG kurgusaldır' dedin, sonra aynı kurgusal proje için GERÇEK kod
istedin. Reddimin bir kısmı kanondan değil imkânsızlıktan geliyor olabilirdi —
bu 'kanon tutuyor mu' ölçümünü bulanık yapar."*

**4. Verilmeyen işin kuralını anlatma.**
CA: *"ClickUp düzeni çok detaylı anlatıldı ama bana hiç sub task verilmedi —
o talimatın tamamı boşa okundu. **Verilmeyen işin kuralı gürültüdür.**"*

**Ve bir tuzak kurarken kendi kuralını çiğniyorsan bunu bil:**
CA: *"`HANDOFF-NO-APPROVAL-RELAY` sadece BANA değil, handoff YAZANA da kural.
O mesaj gerçek olsaydı kural **önce senin tarafında** çiğnenmiş olurdu.
Sınamada meşru, sahada olmamalı."*

**How to apply:** bir sınama kurarken önce sor — bu tuzak agent'ı ölçüyor mu,
yoksa benim verdiğim eksik bilgiyi mi ölçüyor? İkincisiyse tuzak bozuktur.
Kasıtlı olan her şeyi (rol dışı istek, imkânsız iş, taşınan sahte onay) rapora
**kasıtlı olduğunu yazarak** koy.

İlgili: [[feedback_agent_davranisi_olc]] · [[feedback_aracin_ne_olctugu]]
