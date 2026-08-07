# Preload listesi ile çağrılan skill ayrımı — üç katmanlı desen

**Tarih:** 2026-08-07
**Karar mercii:** Mert
**Durum:** Kapalı
**Kapsam:** Fabrika (`agent-project`) — sonra v8'in diğer skill'lerine uygulanacak

---

## Karar

Bir personelin kanonu **üç katmanda** yaşar ve hangisinin ne taşıdığı ayrılır:

**Preload listesi** (`skills:` frontmatter) — **her zaman** gerekli olan skill'ler.
Personel onlarsız hiçbir iş yapamaz.

**Description** — o skill'in **ne zaman** açılacağı. Net, iş anına bağlı ifade:
*"paket dağıtılırken"*, *"sürüm artırılırken"*. Agent bunu görünce kendisi çağırır.

**Body** — listede olmayan bir skill'i **açma yetkisinin var olduğu** ve hangi işte
açılacağı. Tetik cümlesi burada yaşar.

`dagitim` PQA'nın preload listesine **eklenmez.** Sürekli yüklenmesi context şişirir;
PQA'nın ona ihtiyacı yalnız dağıtım sırası geldiğinde doğar.

---

## Gerekçe — Mert'in gerekçesi

> "PQA'nın dağıtımın her zaman yüklenmesi context şişirir, sadece dağıtım sırası
> geldiğinde çağırmasını istediğim için ayırmıştım. Body dağıtımı ne zaman açacağını
> net bilirse yeterli olur."

Yani liste **bilerek** böyle çizilmiş. Bu kararın asıl bulgusu da burada:

**Eksik olan skill değil, gerekçenin yazılı olmaması.** Bir tasarım kararı hiçbir yere
yazılmadığı için sonraki bakan onu arıza olarak okudu. Clara bugün okudu ve *"liste
yanlış çizilmiş"* dedi; yarın PQA'nın kendisi okur ve *"listem eksik"* diye gereksiz
bir gereksinim açar.

---

## Ölçülen durum

### Bulgu gerçek — kural muhatabına ulaşmıyor

`DAG-BUMP-BY-AUDITOR` (`.claude/skills/dagitim/SKILL.md:117`) sürüm alanını değiştirme
işini **PQA'ya** veriyor. `dagitim` yalnız **PAD'in** listesinde.

```
PAM   behavior · is-duzeni · uretim
PAD   behavior · is-duzeni · yapi-taslari · uretim · dagitim
PQA   behavior · is-duzeni · uretim
PCA   behavior · is-duzeni
```

PQA'ya verilmiş bir görev, PQA'nın preload etmediği bir dosyada duruyor.

Ölçüt zaten yazılıydı: *"bir personel bir kuralın muhatabıysa, o kuralı taşıyan skill
onun listesinde olmalı"* (`docs/fabrika/body-denetimi/gereksinim.md:235`). **Bu ölçüt
bu kararla değişiyor** — muhatap olmak preload gerektirmez, *açabilmek* yeterlidir.

### Description'lar şişkin değil — kapanış dokümanı düzeltildi

Kapanış dokümanı *"76 skill'in 76'sı 300 hedefini aşıyor, medyan 664"* diyordu. O ölçüm
**v8 plugin'inin** skill'lerine ait. Fabrikanınkiler ölçüldü:

```
behavior      242   is-duzeni     277   dagitim       306
uretim        317   yapi-taslari  331
```

Beşi de hedefin etrafında. İki ayrı küme tek bulgu sanılmıştı.

### `dagitim`'in description'ı istenen işi zaten yapıyor

> "...paket doğrulanırken, **sürüm artırılırken**, kurulum sihirbazı yazılırken..."

Tetik cümlesi orada. Yani PQA'nın o skill'i bulması için gereken şey yazılı.

---

## Asıl boşluk — üçüncü katman hiç yazılı değil

Description doğru, preload listesi bilerek dar. Eksik olan şu: **PQA listesinde olmayan
bir skill'i açabileceğini bilmiyor.**

Preload listesi personele *"bunlar senin"* diyor. Listede olmayan bir skill'in ihtiyaç
anında açılabileceği **hiçbir yerde yazmıyor.**

Bu ölçüldü — PAM ölçüm turunda hook'un söylediği üç skill dışında hiçbir şeye uzanmadı.
Dar bir talimat aldı ve dar kaldı.

Karşılaştırma: Clara'nın kendi kanonu bunu açıkça yazıyor (*"iki skill'in var ve preload
edilmiyorlar... tetiklenmezlerse `Skill` aracıyla adıyla açarsın"*). Fabrikada bu cümlenin
karşılığı yok.

---

## Uygulama

**Bir — PQA'nın body'sine tetik cümlesi.** Dağıtım/sürüm işine girmeden önce `dagitim`
skill'ini açacağı yazılır. Preload listesi değişmez.

**İki — description'lar "ne zaman kullanılır" ölçütüne göre gözden geçirilir.**
Fabrikada beşi de büyük ölçüde uygun; ölçüt netleştirilip yazılır ki sonraki üretimler
aynı deseni sürdürsün.

**Üç — "listede olmayanı açabilirsin" cümlesi kanona girer.** Yeri `yapi-taslari` ya da
`behavior` — fabrikanın kararı.

Bu değişiklikleri **fabrika yapar** (PAD üretir / PQA denetler). Clara yazmaz.

---

## Yayılım

Mert'in kararı: bu desen v8'in diğer skill'lerine de uygulanacak. Fabrika burada
**örnek** üretiyor — bu yüzden burada verilen karar tek bir düzeltme değil, bir desen.

Not: v8'in 76 skill'inde description şişmesi ölçülmüş (medyan 664) ve bu ayrı bir iş —
bu desen oraya uygulanırken o onarım da gündeme gelir.
