# `claude plugin validate` başarısızlıkta da `rc=0` dönüyor

**Bulan:** PAD (fabrika), 2026-08-08 22:48 · N8N takımı ADIM 1 doğrulamasında
**Doğrulayan:** Clara, aynı ölçümü tekrarladı

## Ölçüm

```
$ claude plugin validate team/n8n-otomasyon --strict
Validating plugin manifest: .../plugin.json

✘ Found 4 errors:
  ❯ agents[0]: Path not found: ./.claude/agents/n8n-planlayan.md
  ❯ agents[1..3]: (aynı sınıf)

✘ Validation failed
$ echo $?
0
```

Araç ekrana **"Validation failed"** yazıyor ve **sıfır** dönüyor.

## Neden önemli

`DAG-VALIDATE-BEFORE-COMMIT` doğrulamayı commit öncesi zorunlu kılıyor. Bir agent
bunu doğal biçimde şöyle kurar:

```bash
claude plugin validate ... && git commit ...
```

Bu zincirde **başarısız doğrulama başarılıymış gibi geçer.** Ve arıza sessizdir:
commit atılır, doğrulama yapılmış sayılır, hata pakete girer.

## Aynı sınıfın üçüncü vakası — bugün

```
printf          rc=0 veriyor, BOZUK JSON üretiyor          (kanal, ölçüldü)
read.py         DURMUŞken && zinciri geçiyor               (kanal, ölçüldü)
plugin validate rc=0 veriyor, "Validation failed" yazıyor  (bugün)
```

Üçünün ortak mekaniği: **iş yapılmamışken çıkış kodu "başarılı" diyor.** Kanal
kanonu ilk ikisini yakalayıp `printf`'i yasakladı ve `&&` zincirini kesti — ama o
kurallar **kanal betikleri için** yazıldı.

## Kanon boşluğu — PAD'in tespiti

Dağıtım kanonu şunu diyor: *"bir script'in geçti demesi tek başına kanıt
değildir."* Ama o kural **üç `plugin-dev` script'i** için yazılmış; resmî
`claude plugin validate` komutu için değil.

**Yani kural doğru sınıfı tarif ediyor ama kapsamı dar.** Ve bugün tam o kapsam
dışında bir vaka çıktı.

PAD kuralı yazmadı (üretim sınırı) — **bildirdi ve karar Clara'ya bıraktı.**

## Ne yapılmalı

Ölçüt basit: **bu aracın çıkış koduna güvenilmez, ÇIKTISI okunur.** Bir doğrulama
adımı `&&` ile zincirlenmezse ve çıktıda `✘` aranırsa arıza kapanır.

**Fabrikaya gidecek gereksinim adayı:** `DAG-VALIDATE-BEFORE-COMMIT`'in yanına —
*"doğrulamanın geçtiği çıkış koduyla değil çıktıyla kanıtlanır; `validate &&
commit` zinciri kurulmaz."*

Gerekçe hazır ve tarihli: bu vaka.

## Şerh

Ölçüm **bu makinede, bu Claude Code sürümüyle** yapıldı. Aracın sonraki bir
sürümü davranışı düzeltebilir — o zaman kural gereksizleşir ama zararsız kalır
(çıktı okumak yanlış sonuç vermiyor).
