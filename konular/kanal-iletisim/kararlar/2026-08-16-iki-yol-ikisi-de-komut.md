# Karar — kanal ve SendMessage iki ayrı komut, seçim kullanıcının

**Tarih:** 2026-08-16 19:10 · **Karar mercii:** Mert

## Mert'in cümlesi

> *"Kanal ya da SendMessage iki farklı command canım, hangisini isterse onu kullanıyorum."*

## Karar

**Kanal düzeni KALKMIYOR ve askıya da alınmıyor.** İkisi de yaşıyor, ikisi de
**kullanıcının komutu.** Seçim oturum başında **onun**, agent'ın değil.

## Fabrika kanonundaki hata

`ISD-OPEN-YOUR-BOX` (`is-duzeni/SKILL.md:269`):

> *"Oturum açılışında kendi kutunu kur, izleyicini kur, canlılığını doğrula ve bir okuma
> yap…"*

**Hatası koşulsuz olması.** Agent açılışta kutu kuruyor — kullanıcı kanal istemiş olsun ya
da olmasın.

**Ölçüldü (2026-08-16):**

| | |
|---|---|
| `is-duzeni`'nde `kanal`/`kutu` geçen satır | **40** |
| `is-duzeni`'nde `SendMessage` geçen satır | **0** |
| `references/kanal.md` | 12.057 bayt, duruyor |

Yani kanonda ikinci yolun **adı bile geçmiyor.**

## Bugünkü bedeli — ölçülü

Sabah **dört personel de kutu kurdu** (kanon öyle emrediyor). Sonra iletim `SendMessage`'a
kaydı, dokuz kutu **10:18'de arşivlendi**, gün boyu tüm trafik SendMessage ile yürüdü.

**İlk saat o belirsizlikte gitti.** DO'nun cümlesi: *"iki taşıma yolu paralel çalışıyor ve
birbirinden habersiz — 'mesaj geldi mi' sorusunun tek cevap yeri kalmadı."*

## ⚠️ Bu karar zaten vardı — fabrikaya geçmemiş

Clara'nın kanonunda yazılı (2026-08-13):

> *"Kanal AÇILIŞTA KURULMAZ. Yalnız `/kanal` komutuyla kurulur — Mert istediğinde.
> Açılışta açık kutu görürsen bilgi olarak not et, dokunma."*

Gerekçesi de ölçülmüş: merkez (okuyan) yokken kutu kurulursa **okunmayan mesaj birikiyor**
— goat'ta 202 mesaj, imleç iki gün ilerlememişti.

**Boşluk şu:** karar Clara'nın odasında verildi, fabrika kanonuna taşınmadı. Bugünkü saat
kaybı bu taşınmamanın bedeli.

## Yarının işi

`ISD-OPEN-YOUR-BOX` **koşullu** hâle gelecek. Kanal metni **silinmeyecek** — düzen duruyor,
yalnız **tetiği** değişiyor: açılış değil, **kullanıcı komutu.**

Ve ikinci yol tanımlanacak: kullanıcı `/sendmessage` derse iletim SendMessage üzerinden.

### Etki alanı — ölçülmeli (PCA)

- dört personel body'sindeki kutu/izleyici tarifleri
- `references/kanal.md` (12 KB)
- `tools/kanal/` betikleri + `/kanal` komutu
- `CLAUDE.md`'nin kanal protokolü kısmı
- `rules-index.json`'da `ISD-OPEN-YOUR-BOX`'a atıf verenler

⚠️ **Kapsam kimlikle kapanmaz.** *"Kutu"*, *"kanal"*, *"izleyici"* geçen her yer taranmalı
ve **okumayla** kapatılmalı (`ISD-CASCADE-COVERS-DESCRIPTIONS`).

### Zemin

Bu işin zemini: `konular/kanal-iletisim/kararlar/2026-08-13-merkez-kapisi-korunuyor.md`
— *"merkez yoksa kutu kurulmaz"* hükmü doğrudan ilgili.
