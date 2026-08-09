# Fabrika kapasitesi — OY ölçeğini kaldırıyor mu

**Ölçen:** Clara (Explore taraması + kaynaktan doğrulama) · **Tarih:** 2026-08-09

**Soru:** Fabrika 9 rol / 76 skill / 574 kurallık bir takımı üretebilir mi?

**Cevap: üretebilir ama TEK İŞ OLARAK üretemez.** Süreç doğru, ölçeklenme mekanizması
eksik — ve eksikliği fabrikanın kendi `docs/` altında açık gereksinim olarak duruyor.

---

## Süreç sağlam — bunlar yerinde

**Dört rol, iki hat.** Kuruluş: PAM → PAD → PQA → PAM → onay → push. Öğrenme:
PAM → PCA → PAM → (gerekirse) PAD → PQA. Tek kaynak
`agent-project/.claude/skills/is-duzeni/SKILL.md`.

**Üç sert kapı** (`uretim/SKILL.md`):
- `URT-NO-PRODUCTION-WITHOUT-NEED` — gereksinim doğrulanmadan üretim yok
- `URT-NO-AUDIT-WITHOUT-TEST` — test edilmemiş çıktı denetime gitmez
- `URT-NO-PUSH-WITHOUT-AUDIT` — denetimsiz push yok

**Skill açma testi var ve keskin:** üç soru (bağımsız tetiklenir mi · ayırt eden
description yazılabilir mi · paketi var mı). *"Üç paragraflık bir skill bir skill
değil, yanlış yere konmuş bir bölümdür."*

**İki test kültürü:** anlaşılırlık testi + davranış testi, ikisi de **isimsiz
`general-purpose` yardımcıya** verilir — üretenin kendi gözü ölçüm sayılmaz.

**Zincir PAM'de kapanır** (`ISD-RETURN-TO-PLANNER`) — geri bildirim döngüsü var.

---

## Üç eksik — OY ölçeği için kritik

### 1. Parçalama ölçütü yok (doğrulandı)

Kanonda **"bir işte en fazla şu kadar" tarzı hiçbir sınır yok.** Üç parçalama kuralı
var ve hiçbiri iş hacmine bakmıyor:

- `ISD-ONE-TEAM-PER-TURN` — ekseni **takım sayısı** ("aynı değişiklik altı takıma
  gidecekse bu altı iştir")
- `BHV-READ-FULL` — ekseni **dosya boyutu** (okuma disiplini)
- `ISD-CASCADE-IN-ONE-TURN` — bölmenin **tersi**, cascade bölünemez

Ve `BHV-LIST-BEFORE-RUNNING` hacim ölçütünü **açıkça reddediyor**: *"Sorulacak soru
'bu iş büyük mü küçük mü' değil, 'bu işin adımları neler'."*

Sahada bölme yapılmış ama **kuralla değil, PAM'in kararıyla** — ve ölçüt her iki
vakada da **hata sınıfı farkı**, hacim değil.

### 2. Rol açma testi yok (kaynaktan doğrulandı)

`grep` ile arandı: `.claude/skills/` altında *"rol açma"*, *"yeni rol"*, *"rol eklemeye
değer"* — **sıfır sonuç.** Skill için üç soruluk kapı var, **rol için hiçbir şey yok.**

OY'de 9 rol var ve yeniden üretimde bu rollerin hepsi mi kalacak sorusu sorulacak.
Kapı yoksa cevap sezgiyle verilir.

Fabrika bunu kendi eksikliği olarak yazmış: `docs/fabrika/uretim-refleksi/` —
**"STATE: KAPANDI — PAD kuyruğunda. Üretim başlamadı."**

### 3. "Çalışıyor mu" kapısı yok — katman-2 boşluğu

PQA'nın kendi kapanış raporundan: *"Üretilen takımın kendisi çalışıyor mu — kanonda
bunun kapısı yok."*

Kanondaki tüm test/denetim hükümleri **dosya** için yazılmış. Bir plugin'in gerçekten
yüklendiğini, hook'unun çalıştığını, skill'in agent'ın eline geçtiğini ölçen **hiçbir
kapı yok.**

**Ve bu tam olarak OY'nin hastalığı.** OY'nin dosyaları tutarlı ölçüldü (31 Temmuz:
0 yetim, 0 çift tanım, 0 kırık atıf) ama sahada %46'sı hiç açılmadı. Aynı kapı
eksikliğiyle yeniden üretilirse **aynı sonuç çıkar.**

---

## Ölçek kanıtı — n8n

Fabrikanın **tek gerçek ürünü**: 3 agent (290 satır), 7 skill (1.434 satır), 82 kural.
Paket toplamı 2.500 satır.

**Maliyet:** ~15 saat / 2 oturum · **5 denetim turu** (üçü GEÇMEDİ) · 2.753 satır süreç
dokümanı · 21 commit.

**İlk 5,5 saatte tek satır ürün üretilmedi** — gereksinim + iki denetim turu + dört
ölçüm raporu + altı bulgu düzeltmesi. Kullanıcı kesti.

**Ve bir sapma belgelenmedi:** gereksinim **4 rol** yazdı, ürün **3 rol** çıktı
(koşturan rolü QA'ya birleşmiş). Birleştirme kararı gereksinime yazılmamış.

### Oran

OY / n8n: rol **3×**, skill **11×**, kural **7×**. Doğrusal varsaymak yanlış olur ama
en iyimser tahminle bile bu, n8n'in birkaç katı bir iş — ve n8n'de zaten
*"saatlerdir napıyorsunuz"* denmişti.

---

## Fabrikanın kendi yükü — devreden işler

`docs/fabrika/` altında **18 iş klasörü** var. **17'sinde `STATE:` satırı yok** — yani
kendi kanonu `ISD-KEEP-STATUS` kendi işlerinde uygulanmamış. Durum ancak metinden
okunuyor.

**Üretim başlamamış olanlar:** `uretim-refleksi` (rol açma testi — PAD kuyruğunda),
`gorev-listesi`, `kanon-butunlugu`, `cascade-turu`, `tamlik-olcumu`, `body-denetimi`.

**Yarım kalanlar:** `atif-haritasi` (Adım B — beş cascade onarımı PAD'de),
`arac-envanteri` (denetim bekliyor), `zit-mekanizma` (yarım cascade izi).

**İki kritik devreden kalem:**

**Kanal betikleri fabrikaya taşınmadı.** n8n'in `KURULUM.md`'si bunu iki önkoşuldan
biri olarak **başa** yazıyor: *"Betikler şu an fabrikanın git deposunda değil."*
Takım kurulabiliyor ama **konuşamıyor.**

**`docs/filo/durum.md` hâlâ "Kurulmuş takım: henüz yok" diyor** — n8n üretildi, filo
kaydına işlenmedi.

---

## Ne anlama geliyor

**"Fabrika bunu yapabilir" doğru ama eksik bir cümle.** Yapabilir; tek iş olarak
veremeyiz. Verirsek üç şeyden biri olur ve üçü de sessiz:

- İş yarıda kalır (n8n'de 5,5 saat sıfır çıktı verdi — 3 rol için)
- Her rolde biraz eksik üretilir ve çıktı dosya olarak var görünür
- Rol sayısı gereksinimden sapar, sapma belgelenmez (n8n'de tam bu oldu)

**Önkoşul iki kalem** ve ikisi de fabrikanın kendi kuyruğunda:
1. **Rol açma testi** (`docs/fabrika/uretim-refleksi/`) — 9 rolün hangisi kalacak
   sorusu bu kapı olmadan cevaplanamaz
2. **Kanal betiklerinin taşınması** — üretilen takım konuşamıyor

Üçüncüsü — **"çalışıyor mu" kapısı** — OY işinin kendi içinde çözülebilir: pilot rolün
kabul ölçütü *"dosya üretildi"* değil *"sahada açıldı"* olur.
