# Push onayı — Mert'e sunum (2026-08-08, 00:45)

**Durum:** PQA denetim onayı VERİLDİ (00:43). Yayın onayı bekleniyor.
**Repo:** `agent-project` · `origin/main` = `cab8500` · `HEAD` = `82f7b54`

---

## ŞU AN NE OLUYOR

Fabrikanın kanonu bir günde baştan elden geçti: `Task` çağrısı kaldırıldı,
kanal düzeni kanona girdi, tamlık ölçümü ve görev listesi disiplini yazıldı.

**22 commit birikti ve hiçbiri push edilmedi.** On bir ayrı işten geliyorlar.

**Denetim tamam:** on altı tur. Her commit **tek tek** denetlendi, sonra
**birlikte** — çünkü Mert sordu: *"hepsi bir başka bozulma yaratmış olabilir."*
Birleşik denetim bir bulgu çıkardı (kural zincirinde özne yok), kapatıldı.

## NASIL ÇÖZÜYORUM

Onayı **iş bazında** istiyorum. On bir işi ayrı listeliyorum. Tamamı
onaylanırsa PQA tek push atar.

## GİDECEK ON BİR İŞ

**1 · `Task` kaldırma** (4 commit)
`dba695d` `b55a7ba` `1856d77` `db66a3e`
Üç karar kanona işlendi: agent agent'ı çağırmaz · eski *"yalnız PAM çağırır"*
kuralı kalktı · sınır araçta değil hedefte.

**2 · Kanal protokolü dökümanı** (1) — `324dc4f`

**3 · Tamlık ölçümü** (3) — `9654ece` `06c4ee0` `7bf2941`
Dört yeni kural: tamlık taramayla değil okumayla ölçülür · eksen geçen turun
bulgusuna göre seçilmez · ölçümün tarihi ve kapsamı yazılır · cascade tarif
eden cümleleri de kapsar.

**4 · Görev listesi disiplini** (1) — `350bb42`
*"Tek görevlik iş diye bir şey yok, o yüzden bu kuralın istisnası da yok."*

**5 · Kanal yöntemi kanona** (1) — `5d53bc4`
Yeni reference dosyası (`kanal.md`). Sabah ölçtüğümde kanal mekaniği kanonda
**sıfır** yerde geçiyordu.

**6 · Zincir kapanışı** (1) — `2d59fee`
Denetim sonucu PAM'e döner, PAM dökümanını düzeltir, o commit de denetlenir.

**7 · Yarım cascade** (1) — `3792a47`

**8 · Kanon bütünlüğü** (2) — `c3827b5` `b8df60b`

**9 · Index onarımı** (2) — `6bb50ff` `e8e9054`
Atıf listeleri: 86 eksikten sıfıra.

**10 · Rol sınırı + planlayana dönüş + Bulgu 13** (3)
`eae041b` `deefcc8` `82f7b54`

**11 · Önceki işler** (3) — `60e4f95` `eacdc93` `f94b2ff`
Sonuncusu **dört gün önceden** push edilmeden kalmış.

## NEREYE DOKUNUYOR

**Kanon:** dört agent tanımı · `is-duzeni` · `behavior` · `uretim` ·
`yapi-taslari` + `arac-envanteri` · `CLAUDE.md` · `rules-index.json` · yeni
`references/kanal.md`
**Toplam:** 12 dosya, 1.745 ekleme, 315 silme
**Kural sayısı:** 123 → **131** (on kimlik doğdu, iki kimlik takas edildi)
**Dökümanlar:** 24 dosya, 5.178 ekleme
**Agent hafızaları:** DOKUNULMUYOR (`.gitignore`'da)

## NEYE DOKUNULMUYOR

Müşteri projeleri · plugin dosyaları · diğer repolar · kanal betikleri
(`~/.pr-kanal/` — asset kararı ayrı iş, yarına)

## EN ÖNEMLİ SINIR — İKİ KARAR

**1 · İki dosya commit'lenmemiş durumda:**
```
docs/fabrika/katman-olcutu/            24K
docs/filo/hook-olcumu-2026-08-06.md    16K
```
**Kural indeksinde on kural bu dosyalara atıf veriyor.** Push atılırsa,
yayınlanan kanonda **olmayan** dosyalara atıf verilmiş olur.

PQA bunu bulgu yazmadı (*"şema sorusu, index hatası değil"*) ama push kararını
etkilediğini söyledi. **Commit'lenirlerse çelişki kendiliğinden kapanır.**

**2 · Kapsam yazılı olmalı.** PQA'nın şartı: *"kapsamı yazılmamış onay eksik
onaydır ve varsayımla tamamlanmaz."* Onay **22 commit / on bir iş** için mi,
yoksa bir kısmı mı — yazılı olmalı.

## PQA'NIN BEYAN SINIRI — bilmeniz gereken

> *"'Yirmi iki commit tutarlı' cümlem **dokuz eksende ölçülmüş** bir sonuç,
> **satır satır okumaya dayanan bir kanıt değil.** 1.745 satırın tam metni bu
> turda okunmadı — tam okuma için kanon dosyası başına bir tur gerekir."*

Yani denetim güçlü ama **tam okuma yapılmadı** ve PQA bunu kendi yazdı.

## AÇIK KARAR

**Var:** (a) push edilsin mi, hangi kapsamla · (b) iki dosya önce commit'lensin
mi

**SÜRE:** onay gelince push tek adım (~1 dk)
