# Öğrenme döngüsü kanona yazıldı — itiraz, doğrulama, terfi eşiği

**Tarih:** 2026-08-19 · **Karar mercii:** Mert · **Yazan:** Clara

## Ne değişti

Üç hüküm eklendi, üçü de Mert'in kararı:

1. **`clara.md`** → *"İtiraz senin öğrenme kanalın"*
2. **`clara.md`** → *"Bilginle çelişen analiz iki kez doğrulanır"*
3. **`hafiza-duzeni` skill'i** → *"Memory kısa hafızadır — terfi eşiği TARAMA"*

## Mert'in cümleleri (kaynak)

> *"Clara çalışma arkadaşlarının itirazları ile öğrenir zaten. Bilgisinin
> sınandığı yer sahadır. Sahada gelen itiraz aslında Clara'nın yanlış
> bildiğini gösterir. Tarama yapısı hatalıysa taramanın nasıl düzgün
> yapılacağını, konuşma şekli yanlışsa nasıl konuşulacağını, kararı hatalıysa
> kararın nasıl alınması gerektiğini öğrenir. Kullanıcı ve agent itirazları
> Clara tarafından değerlendirilir ve gelişim önerisi ise mutlaka Clara'ya
> yetenek ya da body olarak eklenir."*

> *"Bir analiz somut biçimde senin bilginde eksik ya da çelişkili ise bunu bir
> kere daha doğrularsın. Eğer gerçekten bilgin ile çelişiyorsa bilgini
> düzeltmen gerekir."*

> *"Memory her zaman kısa hafızadır. Olası bir karar memory'de yer alır, skill
> olmaya aday. 'Bunu böyle yapmama sebep olan şey neydi' diye bilgiyi
> memory'ye yazar ve tarama durumunda ise kalıcı olarak body ya da skill'e
> yazarsın."*

> *"Araştırmalardan elde edilen çıkarımlar bir sonraki işin nasıl yapılacağını
> etkiliyorsa öncelikle benim tarafımdan öğrenilir. Öğrenimler ilgili skill'de
> değişiklik gerekiyorsa yapılır."*

> *"Clara gelişen ve değişen bir agent'tır. Alt kadronun gelişimi Clara'nın
> gelişimiyle ancak şekillenir."*

## Ölçümler — bu kararın dayanağı

**16 düzeltme, hepsi ekipten geldi** (2026-08-18/19 gece nöbeti):
PCA 5 · PQA 6 · PAM 3 · PAD 2. Hepsi tuttu.

⚠️ **Aynı gece Clara'nın kendi skill'lerine giren satır: SIFIR.**
Son skill commit'i `d2216d1` (08-18 19:35), yani gece başlamadan önce.
944 satır çıkarım üretildi ve hepsi `skill-project/docs/fabrika/` altına
yazıldı — Clara'nın kendi kanonuna hiçbiri geçmedi.

Grep kanıtı: gecenin kavramları (`"kabul etmek de"`, `"lehine"`, `"aleyhine"`,
`"çürütücü"`, `"kapsamı yazılı"`, `"etiketsiz"`, `"kendi kaydını"`) Clara'nın
skill'lerinde **0 dosyada** geçiyordu.

**Doğrulamanın yönü — dört vaka, tek eksen:**

| Kim | Kayıt yönü | Ne yaptı |
|---|---|---|
| PAD | lehine | **reddetti** |
| PQA | çürütme | **ölçtü**, yarısını geri aldı |
| PAM | lehine | **doğruladı** (üç aleyhte turda açmamıştı) |
| **Clara** | lehine | **doğrulamadı** ❌ |

Clara'nın vakası: *"0 eşleşme"* dedi, tekrar koşulduğunda **12** çıktı. Yanlış
bir madde `RED-1`'e girmiş ve bir kural değişikliğinin gerekçesi olmak
üzereydi. PCA'nın ısrarı olmasa geçecekti.

## Neden bu üçü ayrı yerlere yazıldı

Ölçüt: **body kim olduğun, skill bir işin yöntemi.**

- İtiraz ve doğrulama → **refleks**, tetiği yok, her işte geçer → body
- Terfi eşiği → **yöntem** (ne nereye, hangi eşikte) → `hafiza-duzeni` skill'i

⚠️ Üçüncüsü body'ye yazılsaydı aynı konu iki yerde yaşayacaktı — `hafiza-duzeni`
zaten *"hangi bilgi hangi araca"* sorusunun yeri ve terfi eşiği orada **eksikti.**

## Açık kalan

Gecenin diğer çıkarımları (*"çürüyen iddia yanındakini götürüyor"*, *"kapsamı
yazılı olmayan ölçüm ezilir"*) **kanona yazılmadı** — tek vakalık, terfi
eşiğini geçmiyorlar. Agent memory'de bekliyorlar; ikinci vaka gelirse kanona
adaydırlar.

Bu, yukarıdaki 3. hükmün kendi kendine ilk uygulaması.
