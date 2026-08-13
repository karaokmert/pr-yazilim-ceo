# Agent kanonu — skill, preload, kural düzeni — bilinmesi gerekenler

> Bu konuda bir iş geldiğinde **önce bu dosya okunur.**
> Hepsi sahada fiilen çarptı; hiçbiri tahmin değil.

**1. Üç katman var ve karışırsa üçü birden şişer:** body (kim olduğun, her oturumda
yüklenir) · skill (bir işin yöntemi, description'la tetiklenir) · reference
(kanıt/ayrıntı, **kendiliğinden yüklenmez** — `BEHAVIOR-REFERENCE-NOT-AUTOLOADED`).

**2. Skill'e deneyim yazılmaz, kural ve gerekçe yazılır.** Ayıran test: *"bu satır
yarın da doğru olacak mı?"* Tarih/sayı/kişi adı içeren cümle **deneyimdir**, eskir.

**3. "Dal yok" ailesi — yapısal desen.** Yedi agent bağımsız buldu (11 vaka): kural bir
şey emrediyor ama **o şey mümkün değilse ne olacağı yazmıyor.** Örnek: `e2e-verification`
hem *"DISCOVERY oku ZORUNLU"* hem *"kullanıcıya SORMA"* — dosya yoksa iki çıkış da kapalı.
→ Yeni kural yazılırken sorulacak: *"önkoşul sağlanmazsa ne olur?"*

**4. `grep` alt dizeyi bulur, adı doğrulamaz.** `x` araması `önek-x`i de getirir.
Ölçüldü 2026-08-11: `dagitim` arandı, `plugin-dagitim` sanıldı, **yanlış bilgi Mert'e
taşındı ve karar ona dayandı.**

**5. ⚠️ Bir karar "verildi" demek "sahada tutuyor" demek değil.** Ölçüldü 2026-08-13:
Mert 5 Ağustos'ta *"release tag sistemi kaldırılıyor"* dedi; kanon bugün hâlâ
`REL-DO-PRODUCTION-TAG` — *"tag ZORUNLU, atlamak YASAK"* diyor. **Karar kaydı ile
yürürlükteki kanon çelişiyor ve bunu kimse fark etmemiş.**
→ Bir karara dayanmadan önce **kanonda karşılığı var mı** diye bakılır.
