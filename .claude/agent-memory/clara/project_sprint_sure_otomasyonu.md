---
name: sprint-sure-otomasyonu
description: n8n otomasyonu task lıve-dev/completed'a geçince in progress süresini atananın adına ClickUp'a yazar — kişi bazlı saat dashboard'dan okunur
metadata:
  type: project
---

**Süre takibi otomasyonu canlı (2026-09-04).** n8n workflow'u
"ClickUp — In Progress Süresini Set Time Yap" (`4dAX6MEcW4Dpf0SQ`,
n8n.prventurestudio.com, aktif): task `lıve-dev` (p48321079_zbBfSi4O) ya da
`completed` (p48321079_56Wfuinh) statüsüne geçince `in progress` toplam süresini
**atananın adına** time entry olarak yazar.

**Why:** Mert kişi bazlı saatleri ClickUp dashboard'dan standart görmek istiyor —
Clara'nın rapor katmanı yerine kaynak düzeltildi. ClickUp'ta statü→timer
otomasyonu yok; timer yerine "çıkışta set time" modeli seçildi (tek aktif timer
çakışması yok, paralel task yürütülebilir).

**Kritik keşif (ölçüldü):** ClickUp API `time_entries` ucu `assignee` alanıyla
**başka kullanıcı adına** kayıt yazabiliyor (admin token yeter) — kişi başı token
gerekmez. MCP aracı bu alanı açmıyor; ham API/curl gerekir.

**Koruma — fark mantığı (Mert'in tasarımı):** her geçişte in progress toplamı ile
atananın task'taki kayıtlı süresi karşılaştırılır; eşitse eklemez, fazlaysa yalnız
**farkı** ekler — revize turları kaybolmaz, mükerrer olmaz. Kayıt açıklaması
"⏱ otomatik — in progress süresi".

**Ölçülmüş tuzaklar:** (1) workflow güncellenirken webhook yeniden kaydedilir —
o pencerede gelen statü geçişleri KAYBOLUR (17:25 vakası: 5 geçişten biri 22dk
kaybetti, elle backfill'lendi); güncellemeden sonra ilk geçişleri kontrol et.
(2) `in progress`'i hiç görmeden completed'a giden işin süresi ölçülemez —
statü disiplini konusu, "açık unutulan" ile birlikte sorulur. (3) Eşik YOK
(Mert'in kararı): şişkin süre (19s30m vakası) olduğu gibi yazılır, hesabı
sahibine sorulur. Backfill 2026-09-04'te yapıldı: 8 task, 5 kişi.

**How to apply:** günlük sprint kontrolünde süre verisi artık ClickUp time entry'lerden
okunur; `in progress` süresi ile tracked süre arasında büyük fark = arıza sinyali.
Fark dalı (revize turu) canlıda henüz görülmedi — ilk revizede doğrula.
Debug: n8n API `N8N_API_KEY` (~/.zshenv), executions ucundan; credential
"ClickUp pk (Authorization)" (header, Bearer'sız). İlişkili: [[clickup-token-yeri]],
[[sprint-planlama-akisi]]
