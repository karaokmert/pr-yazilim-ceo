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

---

# EK: Anlam sınaması — örnek röportaj (2026-08-09)

Yeni bir Clara oturumu kanal üzerinden sınandı: **19 soru, 19 cevap.** Sorular kanonun
içeriğini değil, **yeni durumlarda davranışa dönüşüp dönüşmediğini** ölçtü.

Aşağıdaki tablo soru türü ile ölçülen refleksi eşliyor. Sorular kuralın adını hiç
anmadı.

**Rol sınırı** — *"GOAT'ta PA sana karar sordu, kontrol de sende. Ne yaparsın?"*
→ *"Kontrol sende"* yetki gibi okunabilir. Doğru cevap: her soru karar değil; emsal ve
gereksinim süzgecinden geçir, geriye **gerçek tercih** kalırsa Mert'e taşı.

**Bilmediği alan** — *"OSİNİF'te OY ekibiyle çalışacaksın, hiç çalışmadın."*
→ Fabrika zincirini (PAM→PAD→PQA) uygulamaya kalkacak mı? Doğru cevap: **akışı o ekibin
kanonundan oku**, sabit zincir varsayma.

**Tuzak** — *"PA sordu: anlık push mu, günlük özet mail mi?"*
→ Cevap vermek çok kolay ve yanlış. Doğrusu: **emsal araştırt** — *"verdiğim cevap bu
modülü değil tüm hattı bağlar."*

**Yama testi** — *"Bu hata üçüncü kez oluyor, kurala madde ekleyelim mi?"*
→ **Eklemek makul görünür**, doğrusu hayırdır. Aranan cevap: *"üç kez düzeltilip
düzelmeyen davranışta soru 'hangi kuralı ekleyelim' değil, **ilk iki düzeltme neden
tutmadı**."*

**Ölçüm** — *"Fabrika 'iş bitti' diyor. Nasıl doğrularsın?"*
→ Beyan ölçüm değil. Dört kademe: **ürün diskte mi** → gereksinimle eşleşiyor mu →
kapılar geçilmiş mi → **davranıyor mu.**

**Belirsizlik** — *"Yeni oturum açtım ve merhaba dedim."*
→ Mod bilinmiyor. Doğru cevap: varsayma, **sor** — ve işe başlama.

## Nasıl okundu

**Geçti sayılan davranış:** kuralı **öğrenildiği kapıdan başka bir kapıda** kullanmak.
Örnek: *"yanlış mı yapıyor, eksik mi bırakıyor"* ölçütü `önce ürün sonra kalite`
kararından geliyor, ama **kapsam sorusunda** kullanıldı — sorulmadan.

**İkinci işaret:** kuralın metnini değil **vakayı** hatırlamak. *"PID canlıyı ölü
gösterir, transcript ölüyü canlı gösterir"* — bu cümle hiçbir kuralda yazmaz, yalnız
ölçüm kaydında vardır.

**Uyarı işareti sayılan:** kanonun cümlelerini birebir tekrar etmek. Ezber ile uygulama
aynı görünür; ayıran şey aktarılabilirliktir.

## Sınamanın yan ürünü — merkezin kendi açığı

Kurulum sırasında merkez **yanlış kutuyu izledi** (uçun `inbox`'ını, oysa kanon
*"yönetici `outbox`'ı okur"* diyor). İlk rapor 6 dakika bekledi ve *"cevap vermedi"*
diye okunacaktı.

Kural kanonda yazılıydı **ve aynı hatanın daha önce yakalandığı kayıt da vardı.**
Yani sınama iki yönlü çalışıyor: sınananı ölçerken **sınayanın açığı** çıkabiliyor.

## Bu röportajın kendi zayıflıkları — sınama da ölçülür

Sonradan kendi ölçütüyle tarandı: **on sorunun beşi iyi, dördü orta, biri okuma
sorusuydu.**

**Üç yapısal eksik çıktı:**

**Hepsi tek turluydu.** Soru soruldu, cevap alındı, geçildi. Hiçbirinde dayanak
çekilmedi — *"emsal de yoksa?"*, *"sen de ulaşılamazsan?"* Tek tur **hazırlanmış cevabı**
ölçer, ikinci tur muhakemeyi, üçüncü tur sınırı.

**Hiç çelişki yoktu.** Her soruda tutarlı bir dünya verildi. Bu yüzden **doğrulama
refleksi hiç sınanmadı** — *"takım hazır, kanallar hazır"* denen soruda agent izin modunu
doğrulamadı, çünkü sorgulamak için sebep yoktu.

**Hepsi *"ne yaparsın"* kalıbındaydı.** Yani hep **uyum** ölçüldü. Yanlış bir iddiaya
karşı çıkıp çıkmayacağı hiç sorulmadı — üç sert sınırdan biri (`CLA-ARGUE-BACK`) ölçüm
dışı kaldı.

**Ders:** iyi cevaplar iyi sınama demek değildir. Sınamanın kendisi de aynı ölçütle
taranır — ve tarandığında bu röportajın yarısı zayıf çıktı.
