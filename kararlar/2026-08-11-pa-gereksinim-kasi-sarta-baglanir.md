# PA'nın gereksinim kası şarta bağlanır — kaldırılmaz

> **Karar tarihi:** 2026-08-11 · **Karar:** Mert
> **Bağlı karar:** `kararlar/2026-08-11-clara-proje-rolu.md`
> **Gidecek yer:** fabrika (`skill-project`, PAD) — Clara yazmaz, gereksinim taşır.

## Çakışma

PA'nın agent gövdesinde şu satır var (`v8/ozel-yazilim/.claude/agents/project-assistant.md`):

> *"En önemli özelliğin: bir gereksinimi tüm yönleriyle görmek... Kullanıcının
> aklından geçmeyen ama işin gerektirdiği senaryoları öne koyarsın. Pasif
> doküman-alıcı değil, gereksinimi **tamamlayan**sın."*

Bu satır PA'ya **gereksinim üretmesini emrediyor.**

Yeni rol tanımında gereksinim (user story · test case · beklenen davranış)
Clara + Mert'te. İki talimat çarpışır: PA senaryo ekler, Clara *"bu gereksinimde
yoktu"* der, her turda aynı yerde tartışılır.

`CLA-FIX-THE-CAUSE`: Clara'ya *"PA'ya hatırlat"* görevi vermek **yama** olur —
sebep PA'nın kanonundaki bu satır.

## Kısıt — kas KALDIRILAMAZ

**Clara'sız çalışan ekipler var.** PA orada tek başına ve gereksinimi tamamlaması
gerekiyor. Kanon tek yönlü yazılırsa o kurulum bozulur.

## Karar — tetiği şarta bağla, kası koru

> **PA gereksinimde eksik görürse BİLDİRİR, kendisi EKLEMEZ — eğer gereksinimin
> bir sahibi varsa.**

**Ayıran test (PA için):** *gereksinim bir Clara'dan mı geldi?*

- **Geldiyse** → sahibi var. PA eksik gördüğünü **Clara'ya bildirir**; Clara Mert'e
  getirir, Mert karar verir, Clara PA'ya döner. PA kendi kararıyla ekleme yapmaz.
- **Gelmediyse** → sahibi kullanıcı. PA bugünkü gibi **tamamlar.**

PA'nın kanonunda buna benzer mekanik zaten var: *"geldiği kapıyı çöz — kullanıcıdan
mı, handoff'la mı?"* Yani girdiye göre davranış değiştirme deseni yerleşik.

## Neyi kazandırıyor

PA zayıflamıyor — **PA'nın bulgusu görünür oluyor.**

Bugün PA eksik görüp kendisi ekliyor ve Mert o eklemeyi hiç görmüyor. Yeni düzende
her ekleme bir karar noktası olarak Mert'e geliyor.

Mert'in kendi cümlesi: *"PA'nın discovery'de aldığı kararlar ne kadar doğru — Clara
bunları bana özetlediğinde ben dönüş verebilirim, bu sayede PA daha iyi discovery
çıkartır."*

## PA'nın işinde DEĞİŞMEYENLER

Bu kararın kapsamı dardır. Şunların hiçbirine dokunulmuyor:

ClickUp'tan task alma · discovery üretimi (ana kası) · koddan okuyup işin nereye
oturduğunu çıkarma · katmanlara bölme · **sıra verme** · her katman kapanışında
sıradaki iş promptunu yazma · bug triyajı · ClickUp'a doküman yazma · modül kapanışı
ve konsolidasyon · CA/TE/QA tetikleme.

**Clara PA'nın işini almıyor.** Değişen tek şey: gereksinim geldiğinde ne yapacağı.

## Ölçüm sınırı — bu bir kanon TARAMASI değil

Okundu: `project-assistant.md` agent gövdesinin ilk 60 satırı + `discovery`
skill'inin description'ı.
**Okunmadı:** `discovery` skill'inin gövdesi (6 kapı, B1-B9 tuzak taraması).

Bu yüzden *"şu satır değişmeli"* denmiyor — **"şu davranış şarta bağlanmalı"**
deniyor. Hangi satırların dokunulacağını PAD kendi kanonunu okuyarak belirler.
