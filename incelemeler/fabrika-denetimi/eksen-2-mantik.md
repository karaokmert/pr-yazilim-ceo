# Eksen 2 — Mantıksal tutarlılık

**Tarih:** 2026-08-06 · **Repo:** `/Users/karaok/p/agent-project`
**Yöntem:** isimsiz yardımcıya ölçüm verildi; her bulguda iki çelişen yer, dosya:satır,
iki hüküm ve sonucu.

## Sonuç — dokuz çelişki, üçü ağır

Kanon iyi yazılmış ve kendi tuzaklarının çoğunu biliyor. Bulunan çelişkilerin **yedisi
aynı sınıftan**: hüküm bir yerde tam, atıfı başka yerde eksik. Yani arıza kural
kalitesinde değil, **cascade'in yarım kalmasında** — ki bu Eksen 1'in `atif_verenler`
bulgusuyla aynı kökü gösteriyor.

## En ağır üç

### 1. PQA'ya "yalnız sen yapabilirsin" denen iş, PQA'nın okumadığı dosyada

`dagitim/SKILL.md:117-119` — `DAG-BUMP-BY-AUDITOR`: *"Sürüm alanını yalnız PQA
değiştirsin... PQA'nın dosyaya el sürmeme kuralının **tek istisnası** budur."*

`pr-agent-qa.md:118-120` — `PQA-NO-FILE-EDIT`: *"Denetlediğin dosyaya el sürme."*
PQA body'sinde tanınan tek istisna `agent-memory` (satır 71). **Sürüm bump istisnası
body'de hiç anılmıyor.**

Ve `pr-agent-qa.md:5-8` — PQA'nın `skills:` listesinde **`dagitim` yok** (yalnız PAD'de).

**Sonuç:** PQA `plugin.json` sürümünü bump etmesi istendiğinde elindeki tek hüküm
`PQA-NO-FILE-EDIT` — istisnayı bilmediği için ya reddeder, ya da yaparsa kendi kritik
kuralını gerekçesiz ihlal etmiş olur. `rules-index.json`'da bu kuralın `atif_verenler`
listesi **boş** — cascade hiç kurulmamış.

İhlali sessiz ve bedeli ölçülmüş: `dagitim/SKILL.md:155-161` — *"altı oturumun dördü
eski sürümle koştu."*

### 2. Araç adı kanon boyunca `Task`, envanterde `Agent` — 20 yerde

`yapi-taslari/references/arac-envanteri.md:95` — *"`Agent` — kendi context penceresi
olan sub-agent açar."* Envanterde **`Task` adında araç yok** (`Task*` yalnız görev
listesi dörtlüsü: TaskCreate/Get/List/Update — bunlar sub-agent açmıyor).

Ama `Task` araç adı olarak 20 yerde kullanılıyor. Kritik olan:
`pr-agent-developer.md:4` — frontmatter `tools: ... Bash, Task, Skill`.

**Sonuç:** iki farklı ağırlıkta hasar. Birincisi mekanik — `arac-envanteri.md:323-324`
kendi hükmü: *"Listedeki hiçbir girdi bir araca çözümlenmezse agent genellikle hiç
başlamıyor"*, ve kısmi yanlış yazım **sessiz.** Yani PAD `Agent` aracını hiç almamış
olabilir ve `PAD-TEST-BEFORE-HANDOFF` (davranış testi) uygulanamaz durumda olabilir —
hata mesajı çıkmadan. İkincisi metinsel: `is-duzeni` "araç şurada var/yok" diye kural
gerekçelendiriyor ama adı yanlış olan bir araç üzerinden.

**Ölçülmedi:** `Task`'ın harness'ta `Agent`'a takma ad olup olmadığı. Burada gösterilen
şey kanonun **kendi envanteriyle çeliştiği.** (Clara notu: bu odada `Agent` aracı
çalışıyor, `Task` adı yok — yani takma ad olmama olasılığı yüksek ama ölçülmesi gerek.)

### 3. Sub-agent izolasyonu `PQA-GATE-BEFORE-PUSH`'u uygulanamaz kılıyor

`pr-agent-qa.md:125-127` — *"Onaylamadan push atma; onaylamak için de dosyayı
bütünüyle okumuş ol."*

Ama push **ayrı bir iş olarak, ayrı bir çağrıyla** geliyor (`pr-agent-qa.md:104,131`).
Ve `yapi-taslari/SKILL.md:148-149`: *"Bir subagent taze ve izole bir context penceresiyle
başlar... okunmuş dosyaları görmez."*

**Sonuç:** push turuna gelen PQA denetim turunda okuduğunu görmüyor. İki okuma mümkün
ve kanon hangisi olduğunu söylemiyor: (a) push turunda yeniden tam okur → denetim iki
kez yapılır, `ISD-CLOSE-THE-LOOP` akışı bozulur; (b) okumadan push atar → kuralın ikinci
yarısı ihlal edilir.

Bu bir yazım hatası değil, **mekanikle kuralın çarpışması** — çözümü kural metninde
değil akış tasarımında. 3. ve 6. işi doğrudan ilgilendiriyor.

## Diğer altı — hepsi yarım cascade

**4. `yapi-taslari` PAM'de Bash yok diyor, PAM body'si "Bash senin elinde" diyor.**
`yapi-taslari/SKILL.md:296-300` PAM'i *"Bash'i olmayan ama fiilen alan"* örneği olarak
kullanıyor — bu tarif `tools:` satırı silinmeden önceki hâle ait.
`pr-agent-manager.md:199-200` sahayı doğru tarif ediyor (commit `08a6410` düzeltmiş),
`yapi-taslari` düzeltilmemiş. PQA bu skill'i ölçüt sayıyor (`pr-agent-qa.md:30`).
`ISD-CASCADE-IN-ONE-TURN`'ün kendi ihlali kanonun içinde duruyor.

**5. "PAD tek yazma yetkisi" üç yerde delinmiş, biri tanınmıyor.**
Ana hüküm `is-duzeni/SKILL.md:73-74` mutlak: *"tek yazma yetkisi olan personel budur."*
Tanınan delikler: PAM `docs/` (satır 565-566 + `PAM-WRITE-DOCS-ONLY`), PQA/PCA memory.
**Tanınmayan:** PQA `plugin.json` sürümü — ürün dosyası, `docs/` değil, memory değil.
Fiilen dört elde yazma var; `is-duzeni` *"rol tanımının tek kaynağı burasıdır"* diyor
ama yazma yetkisinin tam listesi orada yok.

**6. `ISD-STAY-IN-ROLE` dördünü bağlıyor, PCA'nın bölümünde yaşıyor.**
`is-duzeni/SKILL.md:132` — kural `### PCA — analist` başlığı altında, ama gövdesi dört
rolden üçünü örnek veriyor. Index'te `bolum` alanı `"PCA — analist"`, `atif_verenler`
boş. `ISD-APPEND-DONT-REWRITE`'ın kendi uyarısı bu hataya birebir uyuyor: *"Yan cümlede
yaşayan kural index'ten bulunamaz."*

**7. `ISD-COMMIT-THEN-PUSH` PAD'in commit ettiğini söylüyor; PAD body'sinde "commit"
kelimesi hiç yok.** `is-duzeni/SKILL.md:92` hükmü koyuyor, `pr-agent-developer.md`'nin
tamamında kelime geçmiyor. `URT-BODY-BY-SILENCE`'ın ölçütüne göre (*"atlanırsa hata ne
zaman görünür"*) bu body'ye yazılması gereken sınıfta: PAD commit etmezse PQA'nın
denetleyeceği git durumu olmaz ve kayıp sessiz.

**8. `BHV-NO-SELF-CONFIG` dördünü bağlıyor, yasak yalnız ikisinin body'sinde.**
PAM (`:164-166`) ve PAD (`:49-55`) taşıyor; PQA ve PCA **hiç anmıyor.** Ve
`yapi-taslari/SKILL.md:291-295` ölçümü: *"PQA ile PCA'nın listesinde Write yok, sahada
beş dosya yazıldı ve hiçbiri hata dönmedi."* Yani ikisi de fiilen kendi tanımını
yazabiliyor ve ikisinin de body'sinde bu yasak yok.

**9. Kanonun kendi işaretlediği açık kalem — hook yazılmadı.**
`is-duzeni/SKILL.md:191-192`: *"Deterministik zorlama bir hook gerektirir
(`URT-HOOK-WHEN-DETERMINISTIC`) ve **henüz yazılmadı.**"* Yani
`ISD-KEEP-CHAIN-ONE-DEEP`'in (zincir tek katman) mekanik zorlaması yok.
`arac-envanteri.md:122-124` aynı boşluğu ikinci kez teyit ediyor.

`arac-envanteri.md:361-397` "Ölçülmeyenler" bölümü dokuz kalem sayıyor. Üçü sınır
tasarımını ilgilendiriyor — en kritiği: **`tools` hiç yazılmazsa arka planda ne kaldığı
bilinmiyor** (satır 372-375). Bu doğrudan PAM'i ilgilendiriyor, çünkü PAM'in `tools:`
satırı yok.
