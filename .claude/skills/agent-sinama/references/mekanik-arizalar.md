# Agent sınama — mekanik arızaların ölçümü

Bu dosya **kanıt** taşır. Skill'den atıfla çağrılır, kendiliğinden yüklenmez.

Ham kayıtlar: `incelemeler/skill-preload-bulgusu/kayit.md` ·
`incelemeler/fabrika-denetimi/` · `gunluk/2026-08-06.md`

## Preload arızası (2026-08-03'te bulundu)

`skills:` frontmatter alanı skill gövdesini enjekte etmiyor. Bilinen hata:
`anthropics/claude-code#25834`.

**Ölçek:** üç kuşakta beş agent'la sınandı, hepsinde aynı. **Altı ay** boyunca agent'lar
kanonlarını hiç okumadan çalıştı ve kimse fark etmedi — çünkü ihlal sessizdi.

**Sayı:** bir agent tanımında ~11.500 kelimelik skill seti listeliyordu; context'e giren
~1.067 kelime (yalnız description'lar). Kayıp **%91.**

## Agent kendi frontmatter'ını göremiyor

Doğrudan soruldu, agent'ın cevabı: *"Kendi frontmatter'ımı okuyamıyorum."*

**Somut zarar:** bir açılış hook'u *"tanımındaki listeyi yükle"* dedi. Agent listeyi
göremediği için **tahmin etti**, üç skill'den birini doğru yükledi, ve raporunda
*"yüklendi"* diye tik attı.

## Hook alt-agent'ta çalışmıyor (2026-08-06)

Ana oturumda hook **çalışıyor** — PAM açıldı, mesaj geldi, üç skill'i yükledi.

Alt-agent'ta **hiç çalışmıyor.** PCA `Agent` ile açıldı: hook mesajı gelmedi, skill
listesi gelmedi.

**Ve `CLAUDE_CODE_AGENT` çağıranın adını taşıyor:** PCA açıldı, değer
`pr-agent-manager` geldi. Yani hook alt-agent'ta çalışsa **yanlış personelin kanonunu**
yüklerdi.

**Sıralama sonucu:** iki arıza birbirini maskeliyor. Hook alt-agent'ta tetiklenmediği
için yanlış env değerini kullanma fırsatı bulmadı. Yani **hook'u env sorunu çözülmeden
çalıştırmak sistemi bugünkünden kötü yapar** — bugün alt-agent kanonsuz (görünür arıza),
o durumda yanlış kanonu yüklü sanarak çalışır (sessiz arıza).

## Kanonun ulaşması garantisiz

PCA üç skill'den **ikisini aldı**, birini almadı. Ve gelen ikisi **hook'la değil, başka
bir yolla** geldi — hangi mekanizma olduğu ölçülmedi.

**Sonucu:** alt-agent'ın kanonu ne kadar aldığı tur tur değişebilir ve kimse fark etmez.

## `CLAUDE_PROJECT_DIR` ile hook'un çalışması çelişmiyor

Bir ölçümde `CLAUDE_PROJECT_DIR` agent'ın `Bash` ortamında **tanımsız** bulundu ve
*"hook devre dışı"* çıkarımı yapıldı. **Yanlıştı.**

İki ayrı ortam var: hook'u Claude Code kendi çağırıyor; agent'ın `Bash` aracına verilen
ortam `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` ile temizlenmiş. Yani ölçüm doğru, çıkarım
yanlış.

**Ders:** bir ölçüm iki farklı şeyi ölçüyorsa hangisini ölçtüğünü söylemek zorunlu.

## Araç listesi bağlayıcı değil

`tools:` listesinde bir araç olmaması onu **engellemiyor.** Ölçüldü: iki agent'ın
listesinde `Write` yoktu, sahada **beş dosya yazdılar** ve hiçbiri hata dönmedi.

**Sonucu:** araç listesi bir **niyet beyanı**, filtre uygulanmadan bağlayıcı değil.
Kısıt gerekiyorsa mekanizma gerekir, liste yetmez.

## Araç adı kanonda yanlış olabilir

Bir kanonda 20 yerde `Task` yazılıydı; araç envanterinde adı **`Agent`**. Sahada agent
`Agent` kullandı — yani kanon metni gerçeği yanlış tarif ediyordu.

**Ders:** kanondaki araç adı sahada doğrulanmadan ölçüt sayılmaz.
