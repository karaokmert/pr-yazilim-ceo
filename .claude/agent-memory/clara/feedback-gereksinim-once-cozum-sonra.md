---
name: feedback-gereksinim-once-cozum-sonra
description: Gereksinim konuşulurken mimari/maliyet sorusu sorulmaz — Mert bunu iki kez düzeltti, önce ihtiyaç netleşir sonra çözüm
metadata:
  type: feedback
---

Yeni bir proje gereksinimi konuşulurken **çözüm sorusu sorma.** Ne yapılacağı
netleşmeden nasıl yapılacağına geçme.

**Why:** 2026-09-02, proje ekonomisi aracı gereksinim oturumu. Clara iki kez çözüm
tarafına kaydı ve Mert ikisinde de durdurdu:
- Clara "bizim ekrandan yazma var mı, senkron maliyeti ne" diye sordu → Mert:
  *"Maliyeti değil de işi planlasak? Önce gerçekten gereksinimi düşünsen sadece
  gereksinimi geliştirmeye odaklansan sonra çözüm ve nasıl yaparızı konuşsak?"*
- Clara doküman yazma aşamasına atlayıp "proje kimin, iç araç mı ürün mü" diye
  sordu → Mert: *"daha doküman yazmak için çok erken değil mi?"*

**How to apply:** Gereksinim aşamasında sorulacak sorular şunlar: kim kullanacak,
ne zaman kullanılacak, hangi soruya cevap arıyor, bugün nasıl yapıyor, nerede
tıkanıyor, veri nereden geliyor. Sorulmayacaklar: mimari, senkron yönü, maliyet,
teknoloji, repo, kim yapacak.

Çözüm tarafında bir tuzak görürsen **not düş, sorma** — doküman aşamasında açık
karar olarak yazılır.

**Üçüncü vaka (2026-09-04, agent-hafıza kurulumu):** Bu sefer soru değil KOŞUM —
Clara resim bütünüyle netleşmeden kurulum adımları verdi, kendi başına curl testi
koştu. Mert: *"çok acele ediyorsun, tüm işi netlemeden süreç yürütüyorsun. Daha ne
yapmak istediğimi bile anlamadın."* İşaret önceden vardı: Clara "domain silelim
VPN-only" çerçevesi kurdu, Mert `rag.prventurestudio.com` istiyordu — çerçeve
Mert'e sorulmadan kurulmuştu. Kural genişledi: **yalnız soru değil, YÜRÜTME de
bekler — Mert "resim tamam" demeden kuruluma/koşuma geçilmez.**
