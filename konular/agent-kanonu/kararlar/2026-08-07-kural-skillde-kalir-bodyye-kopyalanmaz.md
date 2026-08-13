# Kural skill'de kalır, body'ye kopyalanmaz

**Tarih:** 2026-08-07
**Karar mercii:** Mert
**Durum:** Kapalı

---

## Karar

`ISD-NO-CARRY-APPROVAL` ve onunla aynı sınıftaki beş kural **`is-duzeni` skill'inde
kalır**, PAM'in body'sine kopyalanmaz.

Genel hüküm: **bir kuralın tanım yeri skill'dir.** Body kuralı tekrar etmez, gerekirse
atıf verir.

---

## Gerekçe

Kapanış dokümanı (`gunluk/2026-08-07-kapanis.md`) bunu *"beş kural eksik"* diye
raporlamıştı. Ölçüm bunu çürüttü — kural eksik değil, başka yerde yaşıyor ve zincir tam:

- `ISD-NO-CARRY-APPROVAL` → `.claude/skills/is-duzeni/SKILL.md:454`
- PAM'in frontmatter'ı `is-duzeni`'yi preload listesinde taşıyor
- Açılış hook'u (`acilis-preload.sh`) PAM'e o listeyi dışarıdan okutuyor

Yani kural PAM'e ulaşıyor. Body'ye kopyalamak **tekrar** olurdu.

Ve tekrarın bedeli bu fabrikada zaten ölçülmüş: `PAM-WRITE-DOCS-ONLY`'nin index hükmü
kaynağıyla **iki kez** ayrıştı (`docs/fabrika/baglam-dosyasi-yetkisi/status.md:140` ve
`:221`). İki kaynaklı bir kuralda biri değişir, diğeri eskir, kimse fark etmez.

---

## Ölçüm — hook çalışıyor

2026-08-06'da ölçülemeden kalan soru bugün ölçüldü. PAM fabrika reposunda çağrıldı,
yalnız ortamı soruldu (ölçüm çağrısı —
`kararlar/2026-08-06-clara-olcum-icin-agent-cagirabilir.md`).

PAM'in ham cevabı:

```
CLAUDE_CODE_AGENT=pr-agent-manager
```

> "Evet. Oturum başında `## Oturum açılışı — kanonunu yükle` başlıklı bir SessionStart
> hook çıktısı geldi — `behavior`, `is-duzeni`, `uretim` skill'lerini yüklememi
> söylüyordu."

İki şey doğrulandı: **değişken alt agent'ın kendi adını taşıyor** (ebeveynin değil), ve
**hook tetikleniyor**, doğru listeyi veriyor.

### Çürütülen hipotez

Clara önce `pr-yazilim-ceo` reposunda ölçüm yaptı, değişkende `clara` gördü ve
*"değişken çağıranın adını taşıyor, o yüzden `pr-agent-*` filtresi hiç tutmuyor"*
diye bir hipotez kurdu. **Yanlıştı** — ölçüm yanlış repoda yapılmıştı.

Kayıt sebebi: hipotez doğru görünüyordu ve üstüne dört kararın hepsi kurulacaktı.
Ölçüm hipotezi değil, hipotez ölçümü beklemeliydi.

---

## Kalan risk — kabul edildi

Hook bir **talimat**, bir **zorlama** değil. PAM ölçüm turunda kanonu yüklemedi çünkü
Clara *"sadece şunu yap, başka hiçbir şey yapma"* demişti. Yani:

**Yükleme garanti değil.** Bir personel meşgulse, talimatı yanlış okursa ya da dar bir
talimat alırsa kanonsuz çalışmaya başlar — ve hiçbir hata görünmez.

Bu risk bilinerek kabul edildi. Karşılığında iki kaynaklı kural tekrarından kaçınıldı.

**Açık soru (bu kararın kapsamı dışında):** yüklemeyi garanti altına almanın yolu ne?
Bu ayrı bir iş — kural tekrarıyla çözülmez, mekanizmayla çözülür.

---

## Seçenekler ve neden bu

**A (seçildi)** — Kural skill'de kalsın.
Kazanç: tek kaynak, bakım yükü yok. Bedel: yükleme atlanırsa kural görünmez.

**B (elendi)** — Beş kural body'ye de yazılsın.
Kazanç: body her zaman yüklü. Bedel: iki kaynak — fabrikada iki kez ölçülmüş arıza.
