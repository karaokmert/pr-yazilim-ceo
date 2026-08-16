# Karar — fabrikada push PQA'da kalıyor

**Tarih:** 2026-08-14 11:15 · **Karar mercii:** Mert · **Getiren:** PAM (sabah raporu)

## Çelişki

Aynı eylem iki farklı sahibe verilmişti:

| Kaynak | Kim atar |
|---|---|
| Fabrika kanonu — `ISD-COMMIT-THEN-PUSH` | **PQA** (kullanıcı onayıyla) |
| `/sendmessage` komutu | **Clara** ("Değişti — eskiden QA atıyordu") |

PAM bunu kendi kararıyla plana yazamadı (`ISD-STAY-IN-ROLE`) — yazacağı şey tam
olarak bu hükmün yeni hâliydi. Doğru davranış: sordu.

## Karar

**PQA atar. Fabrika kanonu yürürlükte kalıyor.**

`/sendmessage`'ın *"push'u Clara atar"* satırı **bu odada uygulanmaz.** Komut kendi
bağlamında (OY saha ekibi) geçerli olabilir; fabrikada kanon kazanır.

## Gerekçe

PQA denetleyen taraf — atmadan önce kodu görmüş oluyor. Denetimle push aynı elde
kalınca *"denetlenmemiş şey push edildi"* hâli yapısal olarak zorlaşıyor.

Alternatifin (Clara atar) tek üstünlüğü onayın kimden geçtiğinin tek yerde görünmesiydi
— ama o zaten korunuyor: **onay kapısı Clara'da kalıyor.** PQA *"push'a hazır"* der,
Clara kullanıcıya sunar, onay çıkarsa PQA atar. Yani görünürlük kaybı yok.

## Değişmeyen

**Onay kapısı Clara'da.** Push öncesi onay Clara üzerinden kullanıcıya gider.

## Açık kalan — ikisi de bugün bloke etmiyor

**1. `/sendmessage` metni değişmedi.** Çelişki artık kayıtlı ama komutu okuyan bir
sonraki personel yine *"Clara atar"* görecek. Komut metnine *"fabrikada geçersiz"*
notu düşmek bir üretim işi — body turu bittikten sonra.

**2. İletimi kim yapar** (`ISD-RELAY-DONT-CALL` vs komutun 8/11. adımı). Sabahki
ilk kanon sorusu, hâlâ cevapsız. Bugünkü zinciri bloke etmiyor çünkü onay kapısı
yerinde duruyor.

## Clara'nın notu

Bu soruyu bugün iki kez yanlış çerçeveledim: önce *"bekleyen push var"* sandım
(ölçtüm, yoktu — `HEAD = origin/main = 0acf91b`), sonra Mert düzeltti. Bekleyen
**commit** yoktu, bekleyen **kural** vardı. İkisi ayrı şey.
