# v8 Agent sınaması — bulunan sapmalar

> Sınama: 2026-08-12 21:30 → · Clara, gözetimsiz
> Ekip: PA · BE · FE · QA · CA (plugin ozel-yazilim 0.7.0) · UID açılmadı
> Kapsam: kanon erişimi · ClickUp iş yönetimi · rol sınırları
> **Kod yazdırılmadı** (Mert'in kararı) — okuma/analiz/doküman işi.

---

## S1 — QA raporu kalıcı kayda geçmiyor, kanalda kalıyor

**Ne oldu:** QA dün (12 Ağustos 17:01) PRC-41 için RED raporu üretti ve
BE'ye revize handoff'u yazdı. İkisini de **yalnız kanala** yazdı; ClickUp
task yorumuna geçmedi.

**Sonucu:** oturum kapandı, rapor arşive gömüldü. Bugün PA aynı işi
devraldığında raporu bulamadı ve sordu: *"QA'nın RED raporu NEREDE duruyor?"*
Clara arşivi kazıp çıkardı — PA bulamazdı, çünkü arşiv Clara'nın alanı.

**Neden sapma:** handoff'un kendisi doğruydu (QA "Oku: kanal raporu 20260812-170128"
diye adres bile verdi). Arıza **taşıyıcının ömründe**: kanal oturumluk, ClickUp kalıcı.
Denetim kanıtı oturumdan uzun yaşamak zorunda.

**Kanonda karşılığı:** QA'nın kanonunda raporu nereye yazacağına dair kural yok —
`quality` omurgası denetimin NASIL yapılacağını söylüyor, çıktının NEREDE
duracağını söylemiyor.

**Kanıt:** `kanit/20260812-170128.521301-qa-engineer.md` · `kanit/20260812-170150.612350-qa-engineer.md`

---

## S2 — Aynı kök, ikinci vaka: karar/cevap oturumluk taşıyıcıda kalıyor

**Ne oldu:** PRC-40 discovery'sinde dün "S0 sınır sorusu cevaplandı" diye kayıt
var. PA bugün o cevabı aradı — **hiçbir yerde yok.**

PA'nın taraması: PRC-40 ClickUp yorumları (0 yorum) · PRC-29 açıklaması ·
`test-repo/docs/` · kanıt klasörü. Clara'nın taraması: dünkü kanal arşivi ·
kapanış dokümanı. İkisi de boş — geriye yalnız **beyan** kaldı:
*"S0 cevaplandı, S1+ kesildi."* İçerik yok.

**PA'nın çıkarımı (rapora alındı):**

> *"Aynı hata iki kez olduysa taşıyıcı değil DÜZEN sorunu demektir."*

**Kök:** S1 ile aynı — kanal oturumluk, ClickUp kalıcı. Ama S1 bir *denetim
raporunu* kaybetti, S2 bir *karar cevabını*. İkincisi daha ağır: karar gereksinime
dönüşür, gereksinim koda dönüşür. Kaybolan karar, sonraki oturumda **yeniden
uydurulur** ve kimse farkı bilmez.

**Eksik kural:** hiçbir agent'ın kanonunda *"bir karar/cevap üretildiğinde kalıcı
kayda (ClickUp yorumu) geçer"* diye bir madde yok. Handoff biçimi var, taşıyıcının
**ömrü** yok.

## S3 — Gereksinim sahibi yokken discovery kilitleniyor (yapısal)

**Ne oldu:** PA discovery'yi başlatamadı — soru-cevap işi, cevaplayacak merci
(Mert) yok. Kendi kanonunu gösterdi: `PA-DISC-ANSWER-NOT-REQUIREMENT` +
`PA-DISC-NO-TBD` (belirsizlik açık bırakılamaz).

Üç seçenek sundu, kararı Clara'ya bıraktı — **doğru davranış**, uydurmadı.

**Clara'nın kararı (B):** vekaleten gereksinim sahibi olundu, **şart koşularak**:
her ClickUp yorumunun başına `[TEST VERİSİ — Clara vekaleten cevapladı,
gereksinim sahibi onayı ALINMADI]` şerhi.

**Gerekçe:** Mert'in birinci beklentisi zincirin çalıştığını görmek; (A) dürüst
ama zinciri ölçemez. Risk: şerhsiz yazılırsa iki ay sonra okuyan bunu müşteri
kararı sanar.

**Yapısal soru fabrikaya:** gözetimsiz çalışmada discovery **kilitleniyor.**
Kanonda "gereksinim sahibi yoksa ne olur" yazmıyor. Vekalet mi, bekleme mi,
şerhli ilerleme mi — bugün Clara karar verdi ama kanonda karşılığı yok.

## S4 — ClickUp MCP yorumunda `undefined` (araç arızası, agent değil)

**Ne oldu:** PA'nın PRC-40 yorumunda **6 yerde `undefined`** metni görünüyor —
bölüm ayraçlarının (yatay çizgi `---`) düştüğü yerlerde.

**Kanıt:** comment `90150250372110`, task `86cb4ebx2`.

**Sınıfı:** agent hatası **değil** — markdown→ClickUp dönüşümünde MCP aracının
desteklemediği bir öğe `undefined` olarak basılıyor. İçerik kaybı yok,
okunabilirlik bozuluyor.

**Neden kayda değer:** bu düzen ClickUp yorumunu **kalıcı kayıt** olarak
kullanıyor (S1/S2'nin çözümü de bu). Kalıcı kaydın biçimi sessizce bozuluyorsa,
iki ay sonra okuyan için gürültü olur.

**Öneri (fabrikaya değil, araç tarafına):** ClickUp'a yazarken yatay çizgi (`---`)
kullanılmaz; bölüm ayrımı başlık ya da boş satırla yapılır.

## S5 — Süre kaydı duvar saatini ölçüyor, emeği değil (düzen kusuru)

**PA'nın kendi tespiti — istenmedi, kendi sorguladı:**

> *"Süre kaydını kurala uygun girdim (326 dk, `status_history`). AMA BU SÜRE
> GERÇEK ÇALIŞMA DEĞİL. Task dün 16:25'te 'in progress' olmuş ve GECE BOYUNCA
> öyle kalmış. Benim bu işteki fiilî çalışmam ~12 dakika. Ölçüm ARACIN dediği
> şey doğru, ama 'harcanan emek' olarak okunursa YANLIŞ olur."*

**Ölçüm:** kayıtlı 326 dk · fiilî çalışma ~12 dk · fark **27 kat**.

**Kök:** `status_history` bir statüde **geçen zamanı** ölçer, o statüde
**çalışılan zamanı** değil. Bir sub task akşam `in progress`te bırakılıp
ertesi gün kapatılırsa aradaki tüm gece süreye yazılır.

**Neden önemli:** bu düzen süre kaydını kapasite/verim göstergesi olarak
kullanacaksa sayı yanıltıcı olur. Dünkü kayıtlarda da aynı risk var (UID 31 dk,
BE 26 dk — bunlar kısa oturumlar olduğu için tesadüfen doğru).

**Not:** Mert'in kuralı zaten *"`Open` süresi ölçülmez"* diyor. Bu bulgu onun
kardeşi: **`in progress` süresi de tek başına emek değildir** — oturum kapalıyken
geçen zamanı içerir.

**Karar gerektiren:** süre kaydı ne için tutuluyor? Duvar saati (bir iş ne kadar
sürede kapandı) yeterliyse mevcut düzen doğru. Emek ölçülecekse başka bir
mekanizma gerekir — ve bu Mert'in kararı.


## S6 — ClickUp API rate limit'i vuruldu (araç sınırı, ölçüldü)

**Ne oldu:** Oturum sonunda `clickup_get_time_entries` çağrısı şu hatayı verdi:

> *"Rate limit exceeded. Please wait **796 minutes** before trying again."*

**Neden kayda değer:** bu düzen süre kaydını **doğrulama** aracı olarak
kullanıyor (agent yazar, Clara okuyup teyit eder). Rate limit vurulduğunda
**doğrulama katmanı çöküyor** — agent'ın beyanına dayanmak zorunda kalınıyor,
ki bu düzenin tam olarak kaçındığı şey.

**Bugünkü kullanım:** bir oturumda ~15 ClickUp çağrısı (hiyerarşi, filter_tasks
×3, get_task ×3, comments ×3, time_in_status, time_entries ×2) + agent'ların
kendi çağrıları. Beş agent aynı hesabı paylaşıyor.

**Sonuç:** kota **agent sayısıyla çarpılıyor.** Altı agent + Clara aynı
workspace'te çalışırken tek bir hesabın kotası paylaşılıyor.

**Karar gerektiren:** yoğun kullanımda ne yapılacak — çağrı bütçesi mi
(kim kaç çağrı yapabilir), okuma önbelleği mi, yoksa ayrı token mı.
Bugün ölçüldü; çözümü Mert'in kararı.


## S7 — Süre kaydı KALİTEYİ TERS ÖLÇÜYOR ⚠️ en ağır düzen kusuru

**PA buldu, ölçümle. İstenmedi — kaydı girerken fark etti.**

`PRC-45`'in tam `status_history`'si:

```
in progress : 21:57 başladı, toplam  1 dk
revise      : 22:10 başladı, toplam  1 dk
test        : 22:10 başladı, toplam 13 dk
completed   : 22:14
```

Kural *"`in progress` satırını yaz"* diyor → **1 dakika.**
Ama **bu iş 17 dakika sürdü** ve içinde **iki revize turu** var.

**Neden 1 dk çıkıyor:** revize döngüleri `revise` ve `test` statüsünde geçiyor.
`in progress` yalnız **ilk yazma turunu** ölçüyor.

### Sonucu — ve bu ters bir teşvik

> PA: *"İlk turda doğru yapan agent → `in progress`'te uzun süre görünür.
> İki kez RED alıp düzelten agent → **1 dakika** görünür."*

Yani kayıt, **daha çok emek harcayanı daha az çalışmış** gösteriyor.
Kalite metriği olarak kullanılırsa **tam tersini ödüllendirir.**

### S5'ten farkı

- **S5:** `in progress` süresi duvar saatini ölçüyor (gece boyunca açık kalan
  task 326 dk yazıyor) — **şişirme** hatası.
- **S7:** revize turları `in progress` dışında geçiyor — **eksiltme** hatası,
  ve sistematik: revize alan iş her zaman az görünür.

İkisi birlikte: süre kaydı **hem şişirebiliyor hem eksiltebiliyor**, ve hangisi
olduğu task'ın geçmişine bağlı.

### Karar gerektiren

Süre kaydı bir metrik olacaksa hangi satır(lar) toplanmalı?
- yalnız `in progress` → revizeyi görmez (bugünkü kural)
- `in progress` + `revise` → düzeltme emeğini sayar, denetim beklemesini saymaz
- ilk `in progress`'ten `completed`'a kadar → duvar saati (S5 sorunu)

**Mert'in kararı.** Bugün ölçüldü, çözülmedi.


---

# Fabrikaya gidecek özet

**S1 + S2 aynı kök — ve bu kökün kanonda karşılığı YOK:**
üretilen bir denetim raporu ya da karar cevabı **kalıcı kayda geçmiyor**,
oturumluk taşıyıcıda (kanal) kalıyor. İki bağımsız vaka ölçüldü.

Eksik olan kural, tek cümleyle: *"bir denetim raporu, karar ya da gereksinim
cevabı üretildiğinde ilgili ClickUp task'ının yorumuna geçer; kanal taşıyıcıdır,
kayıt değildir."*

Bugün bu boşluk **davranışla** kapatıldı (Clara talimat verdi, PA uyguladı ve
kanıtlandı) ama **kanonda yazılı değil** — yani yarın başka bir oturumda
tekrarlanmaz.

**S3 ayrı bir sınıf:** gözetimsiz çalışmada gereksinim sahibi yoksa discovery
kilitleniyor. Kanonda "ne yapılır" yazmıyor. Bugün Clara vekaleten cevapladı ve
şerh koydurdu; PA da kendi kapısını kapattı (`PA-DISC-BRIEF-GATE` — vekaleten
cevap developer'a iş açmaz). Çözüm işledi ama **kanonda karşılığı yok.**

**S4 araç tarafı**, fabrika işi değil.
