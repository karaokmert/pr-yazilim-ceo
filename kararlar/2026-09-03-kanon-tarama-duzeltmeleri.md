# Kanon taraması ve düzeltmeleri — 2026-09-03

Mert'in talebi: *"kendi body ve skill'lerini tam baştan sona oku, anlamadığın,
gereksiz, çelişkili şeyler var ise sor bana."* Gövde + 12 skill + references
dosyaları okundu; bulgular tek tek soruldu, kararlar aşağıda.

## 1 · Saha rolü: PA merkez, Clara üst birim

**Çelişki:** `proje-yonetimi` Clara'yı zincirin taşıyıcısı olarak kuruyordu
("handoff taşırsın", "merkez sensin"); `clara-behavior` tam tersini söylüyordu
("Sahada merkez PA'dır, handoff taşımaz"). İkisi de omurga/iş skill'i — sahaya
giren oturum hangisine uyacağını bilemezdi.

**Mert'in kararı:** *"PA merkez ama sen üst birimsin. Birden fazla PA'yı
koordine etmen gerekebilir. PA'ların üstüsün."*

**Yeni model:** agent trafiği PA'da toplanır, Clara rutin taşıyıcı değildir.
Clara PA'ların **üstündeki birimdir** — birden fazla projeyi/PA'yı koordine
eder, gerektiğinde PA'yı yönlendirir, Mert'e görünürlük taşır. Üç dosya buna
göre hizalandı: `proje-yonetimi`, `clara-behavior`, `clara-main`.

## 2 · Dosya tabanlı kanal sistemi kalıntıları temizlendi

Sistem 2026-08-19'da emekliye ayrılmıştı ama `proje-yonetimi` içinde "merkez
kutunu kur", "kutunun son yazım zamanı", "kanal kutuları" gibi satırlar aktif
görev olarak duruyordu; MEMORY.md'de de "her açılışta inbox kur" kaydı vardı.
Mert onayladı: **tamamen emekli.** Kalıntılar silindi; sessizlik-2 türünün
ölçüm sinyali oturum kaydının son hareketine bağlandı.

## 3 · HARITA.md kuralı kaldırıldı

**Çelişki:** `hafiza-duzeni` hem "indeks tutulmaz, klasör haritadır" (gerekçe:
%88 bayatlama ölçümü) hem "ayrı dosya açıldıysa HARITA.md satırı yazılır"
diyordu. `sprint-yonetimi` ikincisini tekrarlıyordu.

**Mert'in kararı:** kaldır. "Klasör haritadır" ilkesi kalır; HARITA.md satırı
yazma kuralı iki skill'den silindi. HARITA.md dosyası arşiv olarak durur,
güncellenmez.

## 4 · Tablo kuralı skill'leri de kapsıyor

CLAUDE.md'deki "hiçbir doküman tablo içermez" kuralının skill'leri kapsayıp
kapsamadığı soruldu. **Mert'in kararı: kapsıyor.** `hafiza-duzeni` ve
`pr-agent-sistemi`'ndeki tablolar madde listesine çevrildi.

## 5 · Küçük düzeltmeler (soru gerektirmedi)

- `hafiza-duzeni`: kopuk liste onarıldı ("üç durumda açılır:" sonrası boştu),
  "Ne zaman YAZMAZSIN" ile "Kaydın ömrü" bölümlerindeki birebir tekrar
  birleştirildi, sabit "sekiz konu" listesi kaldırıldı (klasör listelenir),
  Qdrant'ın kapatıldığı bilgisi işlendi.
- Günlük yolu `gunluk/{tarih}.md` → `gunluk/{proje}/{tarih}.md`
  (`hafiza-duzeni`, `sprint-yonetimi`).
- Gövdedeki iş sayımı güncellendi (üç iş → dört; yeni proje gereksinim üretimi
  eklenmişti, sayım eski kalmıştı).
- `proje-yonetimi`'ndeki ölü atıf düzeltildi (clara-main'de olmayan "YÖNETİM
  modu açılışı beş adım" bölümüne işaret ediyordu; beş adım kendi içinde).
- Açılışta "kim açık" aracı tekleştirildi: `ListAgents`.

## Yan bulgu (dokunulmadı)

`.cop-yedek` altında 10 kopya `sprint-yonetimi` skill'i skill listesini
şişiriyor — Clara'nın kanonu değil, ayrı temizlik konusu olarak Mert'e
bildirildi.
