# Memory düzeni — bilinmesi gerekenler

> Bu konuda bir iş geldiğinde **önce bu dosya okunur.**
> Hepsi sahada fiilen çarptı; hiçbiri tahmin değil.

**1. İndeks EMİR taşır, dosya taşımaz.** `MEMORY.md` context'e **otomatik** girer —
agent hiçbir tool çağırmadan onu görür ve uygular. Dosyalar `Read` gerektirir.
→ İndekse **kural/talimat yazılmaz**, yalnız pointer. Deneyle kanıtlı: indekse
*"X de"* yazıldı, dosyaya *"Y de"* — agent X dedi, dosyayı hiç açmadı.

**2. Skill'le çelişen çıplak kayıt skill'i EZER.** Agent memory'de eşleşen kayıt
bulunca skill'i **hiç açmadan** ona yaslanır. Ölçüldü (2026-08-13): QA'nın memory'sinde
*"ONAY = PUSH"* yazıyordu, kanon tam tersini söylüyor. QA'nın cümlesi: *"sonraki
oturumda okuyup onaysız push atabilirdim."*

**3. Auto-injection 200 satır / 25KB yükler**, sonrası **hiç yüklenmez.** Şişmiş
index = en değerli kaydın görünmez olması.

**4. v7 mirası düştü — 1028 yetim dosya.** Plugin geçişinde isim alanı değişti
(`qa-engineer` → `ozel-yazilim-qa-engineer`), eski dizin duruyor ama agent bakmıyor.
⚠️ **Toptan kopyalama yasak** — içinde v8 kanonuyla çelişen kayıtlar var (UID kanıtladı).

**5. İki kayıt tek tek masum, yan yana kuralı silebilir.** FE bunu buldu: iki tercih
kaydı birleşince kanonun bir adımını örtüyordu.
