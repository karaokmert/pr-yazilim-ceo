# Oturum düzeni — ölçümler

Bu dosya `oturum-duzeni` skill'indeki kuralların **kanıtıdır.** Skill kuralı ve
gerekçesini taşır; buradaki tarihli ölçümler *"bunu nereden biliyoruz"* sorusunun cevabı.

---

## Beş sinyal, sıfır bağımsız ölçüm

**Tarih:** 2026-08-07 · **Karar:** `kararlar/2026-08-07-mod-ayrimi-pwd-ile-olculmez.md`

Mod ayrımının `pwd` ile yapılabileceği varsayılmıştı. Beş sinyal ölçüldü:

- `pwd`
- ana oturumun `lsof` cwd'si
- başlatma komutu
- transcript yolu
- yüklenen `CLAUDE.md`

**Beşi de aynı yeri gösterdi.** Bu doğrulama gibi göründü ama değildi — hepsi tek bir
`cd`'nin yansımasıydı. Yani beş sinyal değil, **bir sinyalin beş kopyası.**

**Genel ders — çakışan sinyal doğrulama değildir.** Ayıran test: *bu sinyallerin
birbirinden ayrıldığı bir senaryo var mı?* Yoksa bağımsız değiller.

**İkinci ders:** bir ölçüt **doğru cevabı yanlış nedenle** verdiğinde de bozuktur. Bu
türün en zor yakalananı — test her seferinde geçiyor. `pwd` her oturumda *"EV"* diyordu
ve çoğu oturum gerçekten EV'di; ölçüt çalışıyor sanıldı.

**Yan bulgu (açık):** `CLAUDE_CODE_AGENT=clara` ana oturumda **doğru** dolu. Kapanış
dokümanındaki *"çağıranın adını taşıyor"* teşhisi ana/alt oturum ayrımını hesaba
katmıyor — ayrı ölçüm gerekiyor.

---

## Hafızanın %28'i bitmiş iş

**Tarih:** 2026-08-07 · **Karar:** `kararlar/2026-08-07-acilis-kapanis-duzeni.md`

Hafıza 943 satırdı. `project` tipindeki kayıtlar **260 satır** tutuyordu — yani %28'i
**bitmiş** işlerin ayrıntısıydı.

Bu kanonun kendi kuralıyla çelişiyordu: *"iş hakkında olan dosyaya gider."* Kural
vardı, uygulanmıyordu — çünkü **silme anı tarif edilmemişti.** Kayıt açmanın tetiği
yazılıydı, kapatmanın tetiği yoktu.

Çözüm kapanışın üçüncü adımı oldu: iş biterken `project` kaydı silinir.

---

## Açılış ve kapanış kanonda hiç tarif edilmemişti

**Tarih:** 2026-08-07 · **Karar:** `kararlar/2026-08-07-acilis-kapanis-duzeni.md`

Kanonun 15 bölümü tarandı — oturumun nasıl açılacağı ya da kapanacağı **hiçbirinde**
yoktu. `CLA-WRITE-BEFORE-CLOSE` bir refleksti (*"kapanmadan önce yaz"*), bir prosedür
değil: neyin yazılacağı, hangi sırayla, nereye — tarif edilmemişti.

Sonuç: her oturum kendi kapanışını uyduruyordu ve sonraki oturum ne bulacağını
bilmiyordu.

---

## Monitör oturumla birlikte ölüyor

**Tarih:** 2026-08-07

Oturum kapanınca `Monitor` task'ı gidiyor. Ama kanalın **hiçbir yerinde iz bırakmıyor**:

- dizin duruyor
- `DURUM.md` hâlâ `ACIK` yazıyor
- mesajlar yerinde

Yani kanal sağlıklı görünüyor ve mesaj gelmiyor. Arıza sessiz — bu yüzden açılışın
üçüncü adımı *"kontrol et"* değil, **"yeniden kur."**

**Ayrıca:** `DURUM.md`'deki `PID` canlılık kanıtı değil. `kill -0` taraması çalışan bir
agent'ı (PQA) ölü gösterdi — o sırada rapor yazıyordu. Mekanizma yeniden ölçülmeden
ölü kanal temizliği yapılmaz.

---

## Pencere ölçümü: üç yöntem yarıştı

**Tarih:** 2026-08-09

Mert *"hangi projedesin"* diye sordu; üç yöntem sırayla ölçüldü:

- **`pwd`** → `pr-yazilim-ceo` dedi. Yanlış — terminal profili Clara'yı her seferinde
  eve `cd`'leyerek başlatıyor, ölçüm doğmadan bozuk. Totoloji: her zaman "EV" der.
- **env** → `GEMINI_CLI_IDE_WORKSPACE_PATH=/Users/karaok/p/agent-project`. Doğru ama
  ikinci elden: yazan Gemini eklentisi (Clara değil) ve oturum başında donmuş.
- **IDE canlı sorgu** → `mcp__ide__getDiagnostics` dört açık dosya döndü, dördü de
  `agent-project` altında. Kaynak pencerenin kendisi, zaman şimdi.

Sonuç: gerçek pencere **fabrikaydı**, `pwd` evi gösteriyordu. Mert'in sorusu üç turdu
ve her turda bir yöntem elendi — *"hatasız olacak olanı"* canlı sorgu çıktı.
