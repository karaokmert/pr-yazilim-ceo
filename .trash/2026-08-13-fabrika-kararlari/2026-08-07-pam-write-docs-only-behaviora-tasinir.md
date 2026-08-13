# `PAM-WRITE-DOCS-ONLY` gövdesi `behavior`'a taşınır

**Tarih:** 2026-08-07
**Karar mercii:** Mert
**Durum:** Kapalı

---

## Karar

`PAM-WRITE-DOCS-ONLY`'nin **gövdesi `behavior` skill'ine taşınır.** PAM'in body'si
kuralı tekrar etmez, atıf verir. `behavior`'daki mevcut tekrar (aynı ayıran testin
ikinci kopyası) gövdenin içinde erir.

Bu, `kararlar/2026-08-07-kural-skillde-kalir-bodyye-kopyalanmaz.md` ile konan genel
hükmün uygulanmasıdır: **bir kuralın tanım yeri skill'dir.**

---

## Gerekçe — Mert'in gerekçesi

> "Çünkü kapanış sadece PAM'in değil diğer agent'ların da bilmesi gereken bir kural."

Kural **çok taraflı.** Yalnız PAM'i bağlamıyor — diğer üç personelin de PAM'in nereye
yazabildiğini bilmesi gerekiyor ki kendi sınırlarını bilsinler.

Kanıtı kaynakta duruyor: `is-duzeni` kuralı PAD'in kapsamını çizerken kullanıyor —

> "Cümleyi kapsamsız okumak iki yönlü hata üretir — ya PAD `docs/`'a yazmaya kalkar,
> ya PAM'in kendi alanına yazması ihlal sanılır."
> (`.claude/skills/is-duzeni/SKILL.md:80`)

Çok taraflı bir kural tek tarafın body'sinde yaşayamaz. Orada yaşarsa diğer üçü onu
ancak dolaylı öğrenir — ve dolaylı öğrenilen kural yanlış öğrenilir.

**Not:** Clara bu seçeneği "tutarlılık" gerekçesiyle önermişti (biçimsel). Mert'in
gerekçesi işlevsel ve daha sağlam — kararın dayanağı bu, tutarlılık değil.

---

## Ölçülen durum — üç yerde üç parça

Kapanış dokümanı bunu *"gövdesi hiçbir skill'de yaşamıyor, iki skill ona yalnız atıf
veriyor"* diye raporlamıştı. **"Yalnız atıf" yanlış** — iki skill de kuralın kapsamını
tanımlıyor.

**Gövde** — `.claude/agents/pr-agent-manager.md:146`. Hüküm + ayıran test
(*"okuyan bir agent bunu talimat olarak uygular mı?"*).

**`behavior`** — `.claude/skills/behavior/SKILL.md:317`. Aynı ayıran testi **kelimesi
kelimesine** tekrar ediyor, `CLAUDE.md`'nin ikiye bölünmesini anlatıyor.

**`is-duzeni`** — `.claude/skills/is-duzeni/SKILL.md:80`. Kuralı PAD'in kapsamını
çizerken kullanıyor.

Sorun tekrar sayısı değil, **aynı testin iki yerde birebir yazılı olması.** Biri
değişirse diğeri eskir — ve bu kuralın kendisinde iki kez ölçülmüş bir arıza
(`docs/fabrika/baglam-dosyasi-yetkisi/status.md:140` ve `:221`).

---

## Kabul edilen bedel

PAM'i fiilen bağlayan en keskin kural artık kendi body'sinde görünmeyecek — hook'un
skill'i yüklemesine bağımlı hale geliyor.

Bu risk Karar 1'de zaten kabul edilmişti (*"yükleme garanti değil"*) ve burada tekrar
kabul ediliyor. Çözümü kural tekrarı değil, yükleme mekanizmasını garantiye almak —
ayrı iş.

---

## Seçenekler ve neden bu

**A (seçildi)** — Gövde `behavior`'a, body atıf versin.
Kazanç: tek kaynak + kural dört personelin de eline geçer.
Bedel: PAM'in body'sinde görünmez, hook'a bağımlı.

**B (elendi)** — Gövde body'de kalsın, `behavior`'daki tekrar atfa çevrilsin.
Kazanç: kural PAM'in gözünün önünde.
Bedel: Karar 1'in genel hükmüne istisna açar + çok taraflı kural tek tarafta kalır.

**C (elendi)** — Olduğu gibi kalsın.
Bedel: iki kaynak, ölçülmüş arıza sınıfı.

---

## Uygulama

Bu değişikliği **fabrika yapar** (`agent-project`, PAD üretir / PQA denetler). Clara
yazmaz. Devir bloğu Mert tarafından taşınır.

Dokunulacak üç yer: `behavior/SKILL.md` (gövde girer, tekrar erir) ·
`pr-agent-manager.md:146` (gövde çıkar, atıf girer) · `rules-index.json` (tanım yeri
değişir).
