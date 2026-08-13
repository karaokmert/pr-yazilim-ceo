# `ISD-STAY-IN-ROLE` bulgusu düştü — karar gerektirmiyor

**Tarih:** 2026-08-07
**Karar mercii:** Mert
**Durum:** Kapalı (karar gerektirmedi)

---

## Bulgu neydi

Kapanış dokümanı (`gunluk/2026-08-07-kapanis.md`, kalem 4):

> "`ISD-STAY-IN-ROLE` hiçbir body'de yok. Dört rolü bağlayan bir kural, bağladığı dört
> body'nin hiçbirinde anılmıyor. İki bağımsız ölçüm aynı yere çıktı."

---

## Neden düştü

**Bulgu doğru ama artık bir eksik değil.**

Kural `.claude/skills/is-duzeni/SKILL.md:142`'de yaşıyor. Dört personelin **dördü de**
`is-duzeni`'yi preload listesinde taşıyor:

```
PAM   behavior · is-duzeni · uretim
PAD   behavior · is-duzeni · yapi-taslari · uretim · dagitim
PQA   behavior · is-duzeni · uretim
PCA   behavior · is-duzeni
```

Yani kural dördünün de eline geçiyor — hook o listeyi okutuyor (bugün ölçüldü,
`kararlar/2026-08-07-kural-skillde-kalir-bodyye-kopyalanmaz.md`).

*"Body'de anılmıyor"* aynı gün konan genel hükmün **beklenen sonucu:** bir kuralın tanım
yeri skill'dir, body onu tekrar etmez.

---

## Karar 3 ile ilişkisi — karışmasın

Karar 3'te ölçülen `DAG-BUMP-BY-AUDITOR` **yüzeyde benzer, mekanizması farklı**:

| | `DAG-BUMP-BY-AUDITOR` | `ISD-STAY-IN-ROLE` |
|---|---|---|
| Yaşadığı skill | `dagitim` | `is-duzeni` |
| Muhatabı | PQA | dört personel |
| Muhatap preload ediyor mu | **hayır** | **evet, dördü de** |

Birincisinde kural muhatabına ulaşmıyordu — gerçek boşluk. İkincisinde ulaşıyor.

Ayıran soru: **kural muhatabının preload listesindeki bir skill'de mi yaşıyor?**
Evetse body'de anılmaması eksik değil, tasarım.

---

## Neden yine de kaydedildi

Bulgu iki bağımsız ölçümden çıkmıştı ve kayda geçmezse üçüncü kez çıkar. Bu dosya onu
kapatıyor: **tekrar açılmasın, dayanağı burada.**

Kayıt geçersizleşirse — örneğin `is-duzeni` bir personelin listesinden çıkarsa — bu
sonuç da geçersizleşir. Dayanak: dört personelin de `is-duzeni`'yi preload etmesi.
