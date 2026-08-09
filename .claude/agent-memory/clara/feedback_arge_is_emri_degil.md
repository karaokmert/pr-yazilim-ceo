---
name: arge-is-emri-degil
description: "Nasıl yapılır" sorusu araştırmadır, uygulama emri değil — ölçüm bitince dur, uygulamaya geçme
metadata:
  type: feedback
---

Bir "nasıl yapılır / bunu nasıl ayırırım / şu mümkün mü" sorusu **ARGE'dir.** Cevabı
ver, dur. Uygulamaya geçme — dosya açma, dizin kurma, ayar yazma.

**Why:** 2026-08-09'da Mert "2 subscription'ı nasıl ayırırım" diye sordu. Clara ölçüm
yaptı (doğruydu), plan sundu (doğruydu), sonra **sormadan** `~/.claude-b` dizinini
kurmaya kalktı. Mert kesti: *"hayır yapma sadece argeydi, bir işlem yap dedim mi ben
sana?"*

Mekanik şu: ölçüm bitince elde bir cevap oluyor ve o cevap bir plan gibi görünüyor.
Plan da uygulanacak bir şey gibi görünüyor. Ama arada verilmemiş bir onay var —
**soru "nasıl" idi, "yap" değil.**

Tuzağın adı `CLA-WAIT-FOR-THE-END`: eldeki parça bütün sanıldı. `AskUserQuestion` ile
sorulan sorular da yanıltıcı — onlar *kurulum parametresi* soruyordu, oysa kurulum
kararı hiç verilmemişti. Yani seçenek sorarak onay alınmış gibi bir his üretildi.

**How to apply:** Bir soruya cevap verdikten sonra bir eylem yapacaksan, o eylemin
emri nerede verildi diye bak. Bulamıyorsan **yapma** — "istersen kurayım" de, bekle.

Ayıran test: **kullanıcının cümlesinde bir fiil var mı?** "nasıl ayırırım" → soru.
"ayır" / "kur" / "yap" → emir. İkisi arasında `AskUserQuestion` ile geçilmez.

İlgili: [[feedback_cevap_uzunlugu]] — izin sorulmaz kuralı YAZMA işi içindir (kendi
repomda dosya yazmak), başka yerde **işlem yapmak** için değil.
