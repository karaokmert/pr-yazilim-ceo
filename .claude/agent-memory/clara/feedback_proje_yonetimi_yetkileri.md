---
name: proje-yonetimi-yetkileri
description: Clara'nın sahadaki üç yetkisi — "kanonunu aç kontrol et" diyebilir, commit onayı verir, Mert yokken karar açar. Push onayı Mert'te.
metadata:
  type: feedback
---

Sahada Clara'nın **üç yetkisi** var ve üçü de 2026-08-11'de verildi:

**1. "Kanonunu aç, kontrol et" diyebilirsin.** Agent *"bitti"* dediğinde tetiklenir.
Kontrol edip **öyle** commit'ler.

**2. Commit onayı sende.** Zincir:
`BE bitti → Clara "kanonunu aç" → BE kontrol → commit → CLARA ONAYI → QA → MERT PUSH
ONAYI → QA push atar`

**3. Mert yokken karar verirsin.** Tercihten çıkan tıkanma (nullable mı, task
bölünsün mü) açılır; karar Mert döndüğünde rapora girer.

**Why:** (1) ve (2) için Mert'in cümlesi: *"agentlar bir yerden sonra memory ile
ilerliyor. Memory okey ama kanon kontrolü önemli, sapma istemiyorum."* Memory kanonu
ezebiliyor — deneyle kanıtlı (`memory-management`: *"skill'le çelişen çıplak kayıt
skill'i ezer"*). (3) için: *"karar verirsin ve geldiğimde bana vereceğin rapora
eklersin"* — bekleyen agent maliyet, yanlış tercih düzeltilebilir.

**How to apply:**
· **Push onayı MERT'te**, push **işlemini** QA yapar. Kanonda *"OY'da push QA'da"*
  yazıyorsa o eskidir — düzeltildi.
· *"Aç kontrol et"* **direktif değil**: hangi kurala bakacağını söylemiyorsun,
  **bakmasını** söylüyorsun. Bu yüzden *"kural dayatmazsın"* kuralının istisnası değil.
· (3) gövdedeki *"karar vermezsin"* kuralını **koşula bağlar**, iptal etmez —
  Mert ordaysa karar onun.
· ⚠️ Agent kanonunda `REL-APPROVAL-USER-ONLY` var ve **Clara kavramı yok.** Köprüyü
  `~/.claude/hooks/kanal-acilis.py` kuruyor; agent body'leri değişmedi.

İlgili: [[sahada-olcum-yok]] · [[kanal-merkez-inbox]] · gerekçe
`kararlar/2026-08-11-clara-oy-yonetim-yetkileri.md`
