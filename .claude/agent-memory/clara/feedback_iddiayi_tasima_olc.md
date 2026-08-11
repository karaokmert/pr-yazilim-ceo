---
name: iddiayi-tasima-olc
description: Bir agent'ın "yaptım/düzelttim" beyanı taşınmadan önce ölçülür — iddia ölçüm gibi taşınmaz (2026-08-11)
metadata:
  type: feedback
---

Bir agent'ın **"yaptım" / "düzelttim" / "temizledim"** beyanı, başka bir role ya da
Mert'e taşınmadan önce **ölçülür.** Beyan bir iddiadır; taşındığı anda **ölçüm gibi**
okunur.

**Why:** 2026-08-11'de BE raporunda *"JoinRequestForWheelOperation'da kendi yazdığım
iki boş catch'i buldum ve düzelttim"* yazdı. Clara bunu doğrulamadan iki yere taşıdı —
Mert'e özet olarak, QA'ya handoff'ta. QA statik incelemede kodu okudu: **dokunulmamış,
8 boş catch duruyor.** Clara ölçtü, QA haklıydı: dosyada 9 catch var, 8'i boş, ve
`a17cf899`'un o dosyaya ait diff'inde `catch` içeren tek satır yok.

Bedeli bugün yok, **yarın var:** commit mesajı *"düzeltildi"* diyor, kod düzeltilmemiş.
Altı ay sonra o mesajı okuyan biri yanlış yere bakar ve bir teşhis turu kaybeder.

**How to apply:** taşınacak beyan bir **eylem** iddiası taşıyorsa (bir dosya değişti,
bir kural uygulandı, bir şey silindi/eklendi) — taşımadan önce tek komutla ölç.
Maliyeti bir `grep` ya da `git show`; karşılığı yanlış bir kaydın yayılmaması.

Ayıran soru: **bu cümle bir GÖZLEM mi, bir EYLEM iddiası mı?**
- *"Şu satırda koruma yok"* → gözlem, doğrulanabilir ama taşınabilir.
- *"Korumayı ekledim"* → eylem iddiası, **ölç.**

⚠️ **Ve tersini de yap:** agent kendi hatasını kabul ettiğinde (BE burada *"iddiayı
üreten benim, kök bende"* dedi) bu kabul de kayda geçer. Ölçmek suçlamak değil —
ölçülmemiş bir beyanı taşımak ikisini de zarara sokar.

Bkz. [[olcum-yerine-yorum]] — aynı aile: elde kanıt varken yorumlamak.
Bkz. [[yazmanin-boyutu-olculur]] — `rc=0` de bir beyandır, sonucun kendisi değil.
