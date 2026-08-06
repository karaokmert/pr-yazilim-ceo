# Agent'larda `tools:` sınırı kaldırıldı — kısıt kuralla korunur

**Tarih:** 2026-08-06 · **Karar veren:** Mert
**Kapsam:** `agent-project` fabrika personeli (PAD, PQA, PCA). PAM'de zaten yoktu.
**Uygulayan:** Clara (`CLA-ASK-BEFORE-WRITING-OUT` — metin gösterildi, onay alındı)

Mert'in cümlesi: *"Tools'dan tanımlamaları kaldır, Clara tools sınırını kullanmak
istemiyorum hiçbir agent'ta istemiyorum."* Ve: *"Hangi tool'ları kullanacağı kurala
bağlı olsun."*

## Ne silindi

```
pr-agent-developer.md:4        tools: Read, Grep, Glob, Write, Edit, Bash, Task, Skill
pr-agent-qa.md:4               tools: Read, Grep, Glob, Bash, Skill
pr-agent-context-analyst.md:4  tools: Read, Grep, Glob, Bash, WebSearch, WebFetch, Skill
```

PAM'de `tools:` satırı yoktu — bilinçli, 2026-08-04 kullanıcı kararı
(`pr-agent-manager.md:134-137`). Yani bu karar yeni bir yön değil, **o kararın diğer
üçüne yayılması.**

## Gerekçe — liste bir kapı değil, bir beyan

**Ölçüldü:** `tools:` fiilen engellemiyor. PQA ve PCA'nın listesinde `Write` yoktu ama
**beş dosya yazdılar** (`YT-FILTER-BEATS-LIST`). Yani liste bir yetki sınırı değil,
bir niyet bildirimi.

**Ve yanlış beyan zararlı.** Bugün tam bu oldu: üç personelin listesinde `Monitor` ve
`ToolSearch` görülmedi, buradan *"üçü monitör kuramaz"* çıkarımı yapıldı. Oysa liste
hiçbir şeyi kanıtlamıyor — ne varlığı ne yokluğu. Karar verilecek yerde yanlış bir
zemin üretti.

İkinci bir ölçüm aynı yöne bakıyor: `pr-agent-developer`'da `Task` yazılıydı, oysa
gerçek araç adı `Agent` (`arac-envanteri.md:95`; PAM sahada `Agent` kullandı). Yani
liste yalnız engellemiyor değil, **yanlış da olabiliyor** ve yanlışlığı sessiz.

## Bunun yerine ne var — kural

Kısıt kuralla korunur, listeyle değil. Örnekler kanonda zaten duruyor:
`PQA-NO-FILE-EDIT`, `BHV-NO-SELF-CONFIG`, `PAM-WRITE-DOCS-ONLY`.

Farkı şu: liste bir aracı **teknik olarak** kısıtlamaya çalışıyor ve başarısız oluyor;
kural bir davranışı **gerekçesiyle** yasaklıyor ve ihlali görünür oluyor — çünkü
kanıtı dosyada kalıyor.

## Ne çözülmedi — bilinerek

**Kanon metnindeki 20 `Task` girdisi duruyor.** Bu karar yalnız frontmatter'daki bir
kopyayı kaldırdı; gövde metinlerindeki tutarsızlık ayrı iş (fabrika denetiminin Ö.1
kalemi, `incelemeler/fabrika-denetimi/eksikler.md`).

**Kısıtın beyanı da kalktı.** Satır silinince her personele her araç açılıyor. Fiilen
zaten böyleydi — ama artık *"şu araçları kullanmam"* diye bir yazılı iz de yok. Bunun
bedeli kabul edildi: yanlış bir beyandan, hiç beyan olmaması iyi.

## Sıradaki iş buna bağlıydı

Karar bir handoff'u bekletiyordu: dört personele kanal mimarisi anlatılacak ve
monitör kurmaları istenecek. `Monitor` deferred bir araç, `ToolSearch` ile şema
yüklemek gerekiyor — üçünün listesinde ikisi de yoktu.

Şimdi liste yok, yani engel de yok (ya da hiç yoktu — ölçülecek). Handoff'ta monitör
maddesi *"kur ve sonucu bildir"* biçiminde gidecek; kurulmazsa arıza kanıtlanır.
