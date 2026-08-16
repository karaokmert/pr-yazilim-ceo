---
name: project-durum
description: Son kapanış dokümanının adresi ve tek cümlelik durum — her oturum açılışında İLK okunur
metadata:
  type: project
---

**Son iş: arama disiplini düzeltildi + SendMessage çelişkisi çözüldü
(EV, 2026-08-16 13:01–17:55).**

Kapanış: `gunluk/ev/2026-08-16-kapanis-arama-disiplini.md`
Karar: `konular/olcum-arama/kararlar/2026-08-16-vektor-cikti-grep-disiplini-girdi.md`

⚠️ **İKİ ŞEYİ BİLMEDEN İŞE BAŞLAMA:**

**1. Qdrant KAPALI.** Mert kapattı (*"mantıklı bulmadık, kullanmadık"*). Vektör
arama kanondan çıkarıldı — `arama-disiplini` artık grep + `ls` diyor.

**2. `grep -l` KULLANMA, satır göster.** `-l` dosya adı verir, cevap vermez.
Ölçüldü: aynı soru `-l` ile 11 dosya adı, `-h` ile 47 satır → cevap **ve bir
çelişki** hiçbir dosya açılmadan göründü. Mert'in *"grep riskli, sürekli farklı
bulgu çıkıyor"* şikayetinin sebebi buydu.

**Açık konu — OTURUMLAR ARASI GÖRÜNÜRLÜK (bugünün ana işi, karar bekliyor).**
Mert: *"birçok session açıyorum, bunların diğer sessionlarda haberi olmuyor."*
⚠️ Çözüm **YENİ DOSYA DEĞİL** — Clara defter önerdi, Mert reddetti:
*"sürekli yazılan, okuması zahmetli dosyalama sisteminden sıkıldım"* (485 md dosyası).
Doğru teşhis: **sorgu problemi.** Var olan kapanış dokümanlarını Clara okusun.
Engel teknik değil — kanonda *"başka projenin kapanışını okuma"* yasağı var,
CEO ofisi için kaldırılmalı.

**Bulgu: bu problem ile gecenin SendMessage görünürlük zaafı AYNI problem**
(`konular/kanal-iletisim/incelemeler/2026-08-16-sendmessage-celiskisi-cozuldu.md`).

**Obsidian ölçüldü — pencere olabilir, beyin olamaz.** Backlink/Dataview/arama
Obsidian sürecinde yaşıyor, dosyada durmuyor, agent'a kapalı. En popüler MCP
Obsidian'ın açık olmasını şart koşuyor. Kazanç Mert'in bakma penceresi olması.

**Mert'in kararını bekleyen — altısı da devrediyor, dokunulmadı:**
`/sendmessage` repoya taşınsın mı · `sendmessage-akisi` fabrikaya gitsin mi ·
`setup.py` PID düzeltmesi (kutu adı dakika bazlı, aynı dakikada açılan iki agent
aynı adı üretiyor) · beş agent'a `clickup` atıfı · "tutarlı yazacaklar mı"
ikinci ölçümü · fabrika betiklerine yazma izni

**Push durumu:** kuyruk SIFIR, ağaç temiz (`b35284d` push edildi 2026-08-16).
