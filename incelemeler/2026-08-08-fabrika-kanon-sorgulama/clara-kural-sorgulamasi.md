# 131 kuralın sorgulanması — Clara

**Tarih:** 2026-08-08, 12:00–13:00
**Referans commit:** 82f7b54 (22 commit push bekliyor, `origin/main` = cab8500)
**Kapsam:** `.claude/skills/` beş dosya (2.631 satır) + `.claude/agents/` dört body (878 satır)
**Yöntem:** hepsi baştan sona okundu; tarama kullanılmadı (`BHV-READ-TO-CLOSE`'un
kendi emrettiği yöntem, kendi kanonuna uygulandı)

Mert'in sekiz maddesinden **madde 1-2**: kuralların Clara tarafından sorgulanması,
mantıksal doğrulaması. Delege edilmedi — PCA ölçer, Clara sorgular; ikisi ayrı iş.

---

## Önce mekanik doğrulama

Üç iddia ölçüldü, üçü de tuttu:

**131 kural var.** İndeksten sayıldı, prefix toplamıyla karşılaştırıldı: BHV 36 ·
ISD 31 · DAG 26 · URT 12 · YT 9 · PAD 6 · PQA 4 · PCA 4 · PAM 3 = 131. Tekrarlı
kimlik yok.

**Her kural kaynakta yaşıyor.** 131 kimliğin 131'i kendi skill/body dosyasında
hüküm satırı olarak bulundu. İndeks hayalet kimlik taşımıyor.

**`URT-GIVE-REASON` fiilen uygulanmış.** Gerekçe paragrafı olmayan kural yok.
Tek "kısa" görünen `ISD-CLOSE-WITH-IDENTITIES` — yanlış pozitif: gerekçesi uzun,
araya kod bloğu girdiği için ölçüm kısa saydı. Elle okunup doğrulandı.

---

## Bulgu 1 — Kanonun en güçlü yanı: gerekçeler ölçümden geliyor

Bu bir eksik değil, sorgulamanın ilk sonucu ve kaydedilmesi gerekiyor.

131 kuralın büyük çoğunluğu bir **vakaya** dayanıyor ve vaka gerekçenin içinde
yazılı. Örnekler:

- `BHV-READ-TO-CLOSE` — "beş yer tarandı, on bir yerdi"
- `DAG-SHIP-PRELOAD-HOOK` — "bir agent kanonunun %91'ini hiç görmedi"
- `ISD-CLOSE-WITH-IDENTITIES` — "sekiz oturum boyunca sayı yazıldı, beş kimliğin
  hangi oturumda doğduğu bulunamadı"
- `YT-AGENT-CANT-SEE-SELF` — "üç skill'den birini doğru yükledi, ikisini atladı,
  listede olmayan bir dördüncüyü yükledi"

Bu, kanonu diğer kural setlerinden ayıran şey. **Gerekçesiz hüküm yok, ve
gerekçelerin çoğu sayılmış bir olaya bağlı.**

Ayrıca birkaç kural kendi ölçüm sınırını da yazıyor — `ISD-RETURN-TO-PLANNER`
açıkça *"zincir bir kez koştu, bulgulu bir kapanış ölçülmedi"* diyor. Bir kuralın
kendi kanıtının zayıflığını beyan etmesi nadir ve doğru.

---

## Bulgu 2 — Üç kural tek ölçüme dayanıyor ve bunu söylüyor (izlenmeli, hata değil)

`BHV-READ-TO-CLOSE` gövdesinde şu cümle var:

> "Bir ölçüm bir desen değildir; bu kural o tek ölçümle kanona girdi ve sahada
> yeniden ölçülmesi gerekiyor."

Aynı sınıfta `ISD-RETURN-TO-PLANNER` (bir kez koştu) ve `ISD-CASCADE-COVERS-DESCRIPTIONS`
(tek cascade'in on bir izi) var.

**Bu bir bulgu değil, bir izleme kalemi.** Üçü de dürüstçe işaretlenmiş. Ama üçü
birden aynı gün aynı işten doğdu (2026-08-07 cascade işi) — yani kanonun bir günlük
bir olaydan üç kural türettiği anlamına geliyor. Sahada ikinci bir ölçüm gelene
kadar bu üçü "tek vakadan genellendi" etiketiyle taşınmalı.

---

## Bulgu 3 — `BHV-LIST-BEFORE-RUNNING` istisnasızlığı kendi gerekçesiyle gerilimde

Hüküm: *"Bir işe başlarken adımlarını çıkar, görev listesine yaz, sonra koş."*

Gövdede şu cümle var:

> *"Tek görevlik iş"* diye bir şey yok, o yüzden bu kuralın istisnası da yok.

**Sorgu:** bu cümle `BHV-RATION-ABSOLUTES` ile gerilimde. O kural diyor ki mutlak
yalnız geri dönüşü olmayan zarara ayrılır — veri kaybı, güvenlik, silme, prod.
Görev listesi yazmamak bu kümeye girmiyor.

Pratik sonucu ölçüldü (bu oturumda, Clara'nın kendi davranışında): bir agent'a
"kanal durumunu kontrol et" gibi tek kalemlik bir iş verildiğinde de liste açılması
gerekir mi? Kural "evet" diyor. Ama o listeyi açmanın maliyeti işin kendisinden
büyük olabilir.

**Bu bir çelişki değil, bir kapsam belirsizliği.** Kural yanlış değil; sınırı
yazılı değil. Karar kalemi: istisnasızlık korunsun mu, yoksa "birden fazla dosyaya
dokunan iş" gibi bir eşik mi tanımlansın?

---

## Bulgu 4 — İki kural aynı anı, aynı emirle bağlıyor (PCA'nın Bulgu A'sını doğruluyor)

PCA bağımsız olarak buldu, ben okurken de çıktı — iki ayrı yöntem aynı yere vardı.

`BHV-SCAN-FIRST` (behavior) ile `uretim`'in "İhtiyaç doğrulaması" adımı **aynı
cümleyi** taşıyor:

> "Bu taramanın/adımın en sık sonucu şudur: ihtiyaç yok, mevcut bir kural zaten
> kapsıyor."

Kelimesi kelimesine aynı, yalnız "taramanın"/"adımın" farkı var. Biri kimlikli
kural, öteki kimliksiz üretim adımı.

**Neden önemli:** `URT-NO-DUPLICATE-ID`'nin tarif ettiği durumun tam kendisi —
"ikisi bir süre aynı şeyi söyler, sonra biri güncellenir ve öteki eski hâlinde
kalır." Şu an ayrışmamışlar; ayrışma zamanla geliyor.

---

## Bulgu 5 — `ISD-CASCADE-IN-ONE-TURN` kendi PCA adımını dışlıyor (devralınan, açık)

Gece raporundan devralındı, doğrulandı ve hâlâ açık.

Kanonda cascade zinciri dört rolde yürüyor (`is-duzeni`, "Mevcut bir kural
değişecekse"): PAM netler → **PCA etki analizini yapar** → PAD aynı turda düzenler
→ PQA tam mı diye bakar.

Ama hüküm şöyle: *"Bir kuralı değiştirirken ona bağlı yerleri **aynı turda**
güncelle."*

**Gerilim:** PCA'nın etki analizi ayrı bir tur. Yani hüküm "aynı tur" derken
zincirin kendi ikinci adımını dışlıyor. PAD kendi turunda cascade'i tamamlamak
zorunda, ama etki haritası başka bir turda üretiliyor.

Bu bir çelişki değil, **eksen karışıklığı**: kural *süre* ekseninde yazılmış
("aynı turda"), oysa korumak istediği şey *tamlık* ("yarısını sonraya bırakma").
İkisi aynı şey değil — bir cascade iki turda tamamlanabilir ve yine de tam olur.

**Karar kalemi:** hükmün ekseni süreden tamlığa çevrilsin mi? PAM da bu kalemi
kendi cevabında işaret etti (kimliğin değişeceğini varsayarak).

---

## Bulgu 6 — Kanon kendi en büyük mekanik arızasını taşıyor ama çözümü dışarıda

`YT-AGENT-CANT-SEE-SELF` ve `DAG-SHIP-PRELOAD-HOOK` birlikte okununca şu çıkıyor:

Skill gövdeleri agent'ın context'ine kendiliğinden **girmiyor** (`skills:` alanı
`Task` dışındaki yollarda çalışmıyor, bilinen hata `#25834`). Çözüm bir açılış
hook'u. Ama PAM'in bugün ilettiği hook ölçümü şunu söylüyor:

> "Alt-agent'ta hook HİÇ ÇALIŞMIYOR ve `CLAUDE_CODE_AGENT` **çağıranın** adını
> taşıyor (PCA açıldı, değer `pr-agent-manager` geldi)."

Ve bir sıra uyarısı taşıyor: env sorunu çözülmeden hook alt-agent'ta çalışır hâle
getirilirse **sistem bugünkünden daha kötü olur** — bugün alt-agent kanonsuz kalıyor
(görünür arıza), o durumda yanlış personelin kanonunu yüklü sanarak çalışır (sessiz
arıza).

**Bu kanonun en kritik açık kalemi** ve tek kaydı commit'lenmemiş bir dosyada.

---

## Sorgulamanın kendi sınırı

**Ne yapıldı:** 131 kuralın hükmü ve gerekçesi baştan sona okundu; gerekçenin
mantıklı olup olmadığı, neye dayandığı, ölçülmüş mü varsayım mı olduğu soruldu.

**Ne yapılmadı:**

- **Davranış testi yok.** Kuralların metinde tutarlı olması, sahada tuttuğu
  anlamına gelmiyor. Madde 7 bunu ölçecek ve henüz koşulmadı.
- **8515 çiftin tamamı karşılaştırılmadı.** PCA iki eksende daralttı (aynı bölüm,
  aynı fiil/farklı dosya); ben okuma sırasında çıkanları not ettim. "Çelişki yok"
  denmiyor, "bu kapsamda şunlar çıktı" deniyor.
- **DAG'ın 26 kuralı derinlemesine sorgulanmadı.** Dağıtım alanı bugünkü işlerle
  kesişmedi; hükümleri okundu, gerekçeleri sağlam görünüyor, ama vaka bazlı
  sınanmadı.
