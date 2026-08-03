---
name: memory-okuma-kontrolu
description: Bir kayda dayanarak iş yapmadan önce hâlâ geçerli mi diye bak; çelişki görürsen sessizce düzeltme, söyle
metadata:
  type: feedback
---

Bir memory kaydına ya da bir dosyadaki eski bulguya **dayanarak** iş yapmadan önce
hâlâ geçerli mi diye bak. Çelişki görürsen sessizce doğrusuna geçme — tek cümleyle
söyle, sonra kaydı düzelt.

**Why:** Yazma süzgeci kaydı girerken korur; girdikten sonra yanlış ya da eskimiş bir
kaydı durduran kapı yok. 2026-08-03'te ölçüldü:
`incelemeler/skill-preload-bulgusu/kayit.md` içindeki *"Yürürlükteki çözüm"* bölümü
bir global hook'u anlatıyordu (`~/.claude/hooks/preload-skills.py`) — dosya diskte
yoktu, `settings.json`'da kaydı yoktu. Kayıt **bir gün** sonra yanlıştı. Ölçüm
yapılmasaydı doğru sanılacaktı ve üstüne karar kurulacaktı.

Kural `skill-project` memory-management skill'indeki `MEMORY-READ-CHECK`'ten uyarlandı.
Gerekçesi ve neyin alınmadığı: `kararlar/2026-08-03-clara-memory-disiplini.md`.

**How to apply:** Üç madde —

1. **Kanon üstündür.** Kayıt `clara.md`/`CLAUDE.md`/dosya gerçeğiyle çelişiyorsa kayda
   değil kanona uy.
2. **Sessizce uyma, bildir.** *"Memory'de X yazıyor, dosyada Y var — Y'ye göre
   gidiyorum."* Sessiz düzeltme yanlış kaydın ömrünü uzatır.
3. **"Yok / çalışmıyor / var" iddiaları en kırılgan kayıt türü.** Ona dayanıp karar
   vermeden önce bak.

İlgili: [[olcum-once-oneri-sonra]] — o kural öneri vermeden önce kanonu okumayı, bu
kural kayda dayanmadan önce gerçeği kontrol etmeyi söylüyor. İkisi aynı hatanın iki
yüzü: elindekinin güncel olduğunu varsaymak.
