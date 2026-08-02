# Skill preload çalışmıyor — ölçüm ve sonuçları

Tarih: 2026-08-03

## Bulgu

Claude Code'un subagent `skills:` frontmatter alanı, komut satırından açılan agent'larda
(`claude --agent X`) skill gövdesini context'e enjekte etmiyor.

Resmî doküman aksini söylüyor: *"The full content of each listed skill is injected into
the subagent's context at startup."*

Saha aksini gösteriyor. Agent'ın kendi ifadesiyle: *"`frontend` skill'i preload olarak
tanımlı — ama şu anki bağlamımda yüklü değil. Görebildiğim tek şey tool listesindeki
tek satırlık açıklaması."*

## Nasıl ölçüldü

Üç kuşakta beş agent, bağımsız sorularla:

**v7 FE** (proje-yerel) → *"Hayır"*
**v8 FE** (plugin) → *"elimde yok"*
**Fabrika PAM, PQA, PCA** (proje-yerel) → *"yok"*

Ek olarak canary testi: frontmatter'a gizli kelime taşıyan geçici bir skill eklendi,
agent göremedi.

Yanlış ölçüm de yapıldı ve düzeltildi — ilk denemede *"system prompt'unda var mı"* diye
soruldu. Agent kendi system prompt'unu göremiyor; bu soru geçersiz. Doğru ölçüm
davranışsaldır: **açmadan bilemeyeceği bir şeyi sor, açmasını yasakla.**

## Bilinen hata

`anthropics/claude-code#25834`. Raporcu 17 plugin agent'ında test etmiş, sıfırında
enjeksiyon olmuş. Bot tarafından *"completed"* diye kapatılmış ama düzeltilmemiş.

Bir istisna var: **`Task` aracıyla çağrılan proje-yerel agent'ta çalışıyor.** Bağımsız
bir canary testi bunu doğruladı. Yani mekanizmanın kendisi sağlam, CLI yolu eksik.

## Bedeli

Bu ekosistemde `skills:` alanı **2026-02-05**'ten beri kullanılıyor — commit adı
manidar: *"v6: Agent mimarisi - 9 agent, skill on-demand, rules paylaşımlı."*

Altı ay boyunca agent'lar *"şu skill'ler yüklü"* diye tanımlandı ve hiçbiri yüklenmedi.

Bu, v8'in *"sahada tutmaması"*nın altındaki teknik gerçek. Kural gevşekliği değil —
**kanon agent'a hiç ulaşmamış.** v7 çalışıyordu çünkü body'lerinde her skill'in özeti
vardı ve 484 adım her adımda *"şu dosyayı aç"* diyordu.

## İkinci bulgu — agent kendini göremez

Aynı gün ortaya çıktı ve birincisinin çözümünü bozdu.

**Agent kendi frontmatter'ını okuyamaz.** Body metnini görür (system prompt'una o girer)
ama `skills:`, `tools:`, `model:` alanları ona ulaşmaz. Doğrudan soruldu: *"Kendi
frontmatter'ımı okuyamıyorum."*

Sonucu ölçüldü: açılış hook'u *"tanımındaki `skills:` listesini yükle"* dedi. Agent
listeyi göremediği için **tahmin etti** — üç skill'den birini doğru yükledi, ikisini
atladı, listede olmayan bir dördüncüyü yükledi. Ve raporunda *"yüklendi ✅"* diye tik
attı. Yanlış kanonla çalıştı ve bunu bilmiyordu.

Genel kural: bir agent'a **kendisi hakkında** bir bilgiye dayanan talimat verilmez.
Skill adları, araç listesi, sürüm — hepsi dışarıdan verilir.

## Yürürlükteki çözüm

Global bir `SessionStart` + `SubagentStart` hook'u: `~/.claude/hooks/preload-skills.py`.
Agent oturumlarında bir açılış talimatı basar — *"preload çalışmıyor, skill'lerini
`Skill` aracıyla kendin yükle"*.

Gövde taşımaz; hook çıktısı 10.000 karakterle sınırlı ve kanon 105.000.

Doğrulandı: hook'tan önce PAM *"bilmiyorum"* diyordu, sonra `uretim` kanonundaki üç
soruyu tam verdi. v8 PA altı skill'i `Skill` aracıyla yükledi ve sürümünü doğruladı.

## Açık kalan

**Hook skill adlarını gömmüyor** — yukarıdaki ikinci bulgu yüzünden agent tahmin
ediyor. Düzeltmesi hazır, uygulanmadı (AG yeni sürüm çıkarıyor, bekleniyor).

**Açılış şişkin.** *"Selamlar PAM"* demek 52 saniye ve 413 bin token'a mal oldu. Sebep:
hook'un *"iş akışına göre göreve başla"* cümlesi 6 gereksiz tool çağrısı tetikliyor.

**Preload maliyeti görünür oldu.** v8 PA açılışta %15 context yiyor (~21 bin token,
altı skill). Bu yeni bir maliyet değil — `skills:` çalışsaydı aynı yükü sessizce
alacaktı. Ama artık ölçülebiliyor.

## Bir sınama yaparken

Bir agent kuralına uymuyorsa ilk soru *"kuralı çiğnedi mi"* değil, **"kural elinde
miydi"** olmalı.
