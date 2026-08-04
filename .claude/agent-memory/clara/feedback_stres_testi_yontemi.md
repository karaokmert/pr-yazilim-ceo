---
name: stres-testi-yontemi
description: Bir mekanizmayı sınarken tek taraflı ve sentetik test yetmez — karşı tarafla gerçek koşulda, kırılana kadar zorla
metadata:
  type: feedback
---

Bir mekanizma sınanırken **tek taraflı test yarım ölçümdür** ve **sentetik test
yanıltıcıdır**. Karşı tarafla, gerçek koşulda, kırılana kadar zorla.

**Why:** Mert 2026-08-04'te iki kez düzeltti. Birincisi: *"iletişim ile test yapman
lazım, böyle kendi kendine olmaz."* İkincisi: *"bunu stres testi olarak gör, her şeyi
deneyip öyle ilerleyin ki sahada hatalar bulmayalım."*

Ölçüldü ve haklı çıktı: Clara'nın tek başına yaptığı "yarım okuma mümkün" testi
sentetikti — kendi kendine satır satır yazıp okudu, oysa gerçek yazma
`cat >> ... <<'EOF'` ile tek `write()` yapıyor. Karşı taraf bunu yakaladı ve test
geçersizdi.

Aynı gün ikinci kanıt: agent-agent kanalı deneyinde **en değerli bulgular kanal
çöktüğünde çıktı, konuşulduğunda değil.** İlk üç tur sohbetti; asıl bilgi ilk gerçek
iş taşındığında ve monitor öldüğünde geldi.

**How to apply:** Bir mekanizmayı değerlendirirken —

1. **Konuşarak sınama.** Sohbet mekanizmayı zorlamaz. Gerçek yük taşıt.
2. **Kendi kendine ölçüp "test ettim" deme.** İki taraflı bir mekanizma tek taraftan
   ölçülmez; karşı tarafın kurulumu seninkinden farklı olabilir ve fark tam da
   aradığın şeydir (ölçüldü: Clara-1'in filtresi monitor'ünü ayakta tuttu, Clara'nınki
   çöktü — aynı mesaj).
3. **Cevabı hemen yazma.** Mert'in düzeltmesi: *"senin hatan hemen yazıyor olman."*
   Basmadan önce sınamaları koştur, sonuçla yaz.
4. **Kırılma noktasını ara.** Uzun mesaj, eşzamanlı yazma, yazarken okuma, dosya
   silinme, karakter kaçışı — hepsi denendi ve beşi arıza çıkardı.

İlgili: [[olcum-once-oneri-sonra]], [[hatirladigim-kayittir]]
