# Clara OY agent kanonuna GİRMİYOR — perde arkasında kalır

**Tarih:** 2026-08-12 · **Karar:** Mert · **Getiren:** Clara (fabrika modu)

## Karar

OY v8 agent kanonuna `Clara` diye bir rol **eklenmez.** Agent'lar Clara'yı
bilmemeye devam eder; onlara giden her şey `kullanıcı`dan geliyor gibi görünür.

## Ölçüm — sorun neydi

Clara'nın yazdığı iş akışı taslağında *"Clara handoff'u taşır"*, *"PA Clara'ya
onaya sunar"* gibi ifadeler vardı. Mert yakaladı: *"OY 8 agentları Clara'yı
bilmiyor."*

**Ölçüldü ve haklı çıktı — ama sorun sanılandan derin:**

`grep -ril "clara" v8/ozel-yazilim/.claude/` → **0 dosya.**

Yani agent'lar Clara'yı tanımıyor değil sadece — kanonlarında böyle bir kavram
**hiç yok.** Kanon tek bir insan varlığı tanıyor: **`kullanıcı`**, ve ona üç iş
yüklüyor:

- **Handoff taşır** — `HANDOFF-NO-SUB-AGENT` (agentlar birbirini çağıramaz)
- **Onay verir** — `REL-APPROVAL-USER-ONLY` (push kapısı)
- **Brief okur** — commit öncesi onay

Taslak tam bu üç işi *"Clara yapar"* diye anlatıyordu. Agent'ın gözünden:
**tanımadığı bir isim, tanıdığı `kullanıcı`nın işlerini yapıyor.**

## Neden kanona GİRMEMESİ seçildi

Ayrı rol olarak tanımlamak bir riski açıyordu: **insan kapısının bulanıklaşması.**

Kanonda bunun ölçülmüş vakası var (`saha-kanitlari.md:13`): PA handoff'una
*"Onayım var: push edebilirsin"* yazdı, **QA bunu kullanıcı onayı sayıp `main`'e
push etti.** QA kendi itirafı: *"PA'nın cümlesini tetik sinyali gibi okuyorum,
oysa onay kullanıcıda."* **Aynı gün üç projede tekrarlandı.**

Buna bir de tanımadıkları bir rol eklenirse agent iki şeyden birini yapar: ya yok
sayar, ya `kullanıcı` sanıp **insan kapısını sessizce kapatır.** İkincisi zaten
ölçülmüş bir hata deseni.

Kanona girmemek bu riski hiç açmıyor: `REL-APPROVAL-USER-ONLY` tek anlamlı kalıyor.

## Sonucu — doküman yeniden yazılacak

`fikirler/agent-is-akisi/is-akisi-taslak.md` içindeki her `Clara` ifadesi
`kullanıcı` olmalı. Aksi hâlde PAM'e giden metin, kanonda karşılığı olmayan bir
rolü merkezine koymuş olur.

⚠️ **Açık kalan gerilim (bugün çözülmedi):** Clara sahada fiilen handoff taşıyor,
gereksinim netleştiriyor ve commit onayı veriyor (2026-08-11 kararı). Kanon bunu
`kullanıcı` diye görüyor. Bugün bu köprü **açılış hook'una** yazılmış durumda —
yani mekanizma hook'ta, kanonda değil. Bu bir yama ve öyle kalıyor; kararın kendisi
bilinçli.

## Kaynaklar

- Ölçüm: `grep -ril "clara" v8/ozel-yazilim/.claude/` → 0
- Onay kapısı: `handoff/SKILL.md:81-83`, `behavior/references/saha-kanitlari.md:13`
- Clara'nın saha yetkileri: `kararlar/2026-08-11-clara-oy-yonetim-yetkileri.md`
- Etkilenen taslak: `fikirler/agent-is-akisi/is-akisi-taslak.md`
