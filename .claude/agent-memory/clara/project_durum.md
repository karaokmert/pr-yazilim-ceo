---
name: durum
description: İLK BUNU OKU — son kapanış dokümanının adresi ve tek cümlelik durum. Oturum açılışında ilk okunan kayıt.
metadata:
  type: project
---

# Durum

**Son kapanış:** `gunluk/2026-08-07-kapanis-2.md` — oku, çalışmaya başlayabilirsin.
Bir öncekini (`2026-08-07-kapanis.md`) **iptal etmiyor, üstüne ekliyor**; sprint durumu
ve bekleyen kalemler orada.

**Tek cümlede:** Kanal düzeni JSON'a geçti ve beş araca dönüştü
(`~/.pr-kanal/agent-project/tools/`), dört fabrika ucu doğruladı; `kanal-kurulumu`
skill'i v3'e güncellendi (464 + 404 ref); sıradaki hareket `agent-project`'te
**açılışın tek başına çalışıp çalışmadığını** ölçmek.

**Ölçülecek asıl soru:** agent kanal protokolünün adresini nereden bilecek? Sıfır
bağlamlı sınamada yardımcı adresi görev promptundan aldı — *"verilmeseydi aramayı
bilmezdim."* Dört uç bunu üç kez söyledi: kanal kurulumu kanonlarında yok. Skill'in
handoff şablonu geçici olarak kapatıyor (adres blokta veriliyor), kalıcı çözüm PAD'de.

**Mert'in kararını bekleyen 4 kalem:** push onayı (3 commit, biri denetimden geçmedi) ·
`docs/` commit sahipliği (3 klasör commit'lenmemiş) · bozuk `behavior/SKILL.md`
description'ı (mekanik sorun) · **şablonun `KAPANIS` hatası PAD'e nasıl gidecek**
(devir bloğu yazılmadı).

**Bilinen şablon hatası:** `SABLON-JSON.md` kapanış komutu `KAPANIS` diyor, `send.py`
yalnız `TASK|INFO|QUESTION|CLOSE` kabul ediyor → o komut `rc=1` verir. Skill'de doğrusu
yazılı; şablona **dokunulmadı** (Mert: sadece bildir).

**Çözülmemiş ölçüm:** canlılık — üç sinyalden ikisi yanlış; tek çalışan *"kutunun kendi
son yazım zamanı"*, ama eşik uydurulmuyor, otomatik temizlik yok.

**Kaynaklar:** `~/.pr-kanal/{proje}/SABLON-JSON.md` (neden böyle) ·
`~/.pr-kanal/{proje}/tools/` (nasıl yapılır) · `kanal-kurulumu` skill'i (kim ne yapar).
