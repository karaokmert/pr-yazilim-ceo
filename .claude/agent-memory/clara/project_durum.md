---
name: project-durum
description: Son kapanış dokümanının adresi ve tek cümlelik durum — her oturum açılışında İLK okunur
metadata:
  type: project
---

**Son iş: hook'a Question başlığı + tanımlayıcı kuralı (EV, 2026-08-13 22:58–23:11).**

Kapanış: `gunluk/ev/2026-08-13-kapanis-hook-question.md`
Karar: `konular/clara/kararlar/2026-08-13-question-baslik-ve-tanimlayici.md`

`~/.claude/hooks/sessiz-mod.sh`'e iki kural yazıldı, çalıştığı ölçüldü:
`★ Question` kutusu **zorunlu başlıkla** açılır (konu adı, soru değil) ve
**tanımlayıcı tek başına basılmaz** (task ID/commit/branch → yanına başlık).
Hook global — tüm agent'lara gidiyor, Mert bilerek onayladı.
⚠️ Hook agent body'sinde iz bırakmaz; kalıcılık isteniyorsa fabrikaya gitmeli.

**Mert'in kararını bekleyen — dördü de dünden devrediyor, dokunulmadı:**
- **`setup.py` PID düzeltmesi** (EN ACİL, iki oturumdur bekliyor) — kutu adı
  dakika bazlı, aynı dakikada açılan iki agent aynı adı üretiyor, ikincisi
  var olan kutuyu SAHİPLENİYOR. Metin hazır: `f"{ROL}-{SESSION}-{os.getpid()}"`.
  Fabrika betiği = onay gerek.
- **Beş agent'a `clickup` atıfı** — blok hazır, taşınmadı.
- **"Tutarlı yazacaklar mı" ölçümü** — 12 Ağustos karar dosyası bekliyor.
- **Dünden:** fabrika betiklerine yazma izni · üç fabrika bulgusu · kayıp mesajlar.

**Ölçüm borcu (tek taramada çıkar, 200+ mesaj gerekiyor):** sessizlik hook'unun
ara-blok etkisi · Question kutularında başlık oranı · task ID'lerinde başlık oranı.
