# Onay brief kalıbı — Mert'in onaylayabildiği biçim

**Tarih:** 2026-08-04, 23:00–23:11
**Nasıl bulundu:** Mert *"tam istediğimi anlatamıyorum, sen öner ben olana kadar
seni düzeltirim"* dedi. Dört deneme yapıldı, dördüncüsü tuttu (*"işte budur"*).
**Kaynak iş:** GOAT `#PRY-17484` chat davranış tamamlama, BE'nin gerçek plan onayı.

## Sorun neydi

BE bir plan onayı sundu, Mert onaylayamadı. Kendi cümleleri:

> *"Okuyunca insan olarak anlamak çok zor, çok karışık ve dağınık."*
> *"Bu benim onun hakim olduğu her şeye hakim olduğumu düşünen birinin özet
> bilgisi. Ben sadece bu mesajı okuyarak onay veremiyorum."*
> *"Bu kodu yazdırıp sonra başka biri bana gelip bu modülü nasıl yaptın dese hiçbir
> şey açıklayamam."*

**Teşhis:** brief onay için değil, agent'ın kendini anlatması için yazılmıştı —
ölçüm anlatısı, teknik gerekçe, ders çıkarımı. Doğru bilgiler ama Mert onay
verebilmek için gerekeni bulmak zorunda kalıyordu.

## Kalıp (dördüncü deneme — kabul edilen)

Her iş kalemi için **üç blok**, sırayla:

1. **Şu an ne oluyor** — mevcut davranış ve neden yanlış
2. **Nasıl çözüyorum** — akış, adım adım (`→` ile zincir)
3. **NEREYE YAZILIYOR** — beş sabit satır

Beş sabit satır — **boş olanlar da yazılır:**

    Handler:    hangi handler, yeni mi mevcut mu, hangi adıma giriyor
    DataLayer:  hangi DataLayer, sorgu şekli (N+1 var mı)
    Cache:      hangi cache kullanılıyor / yeni açılıyor mu / yok
    Tablo:      değişiyor mu — değişiyorsa hangi tablo, NE İŞE YARIYOR,
                migration nasıl
    Emsal:      hangi mevcut desen izleniyor + yazarı (insan/agent)

Sonda üç blok:

    ═══ NEYE HİÇ DOKUNMUYORUM     (dokunulmayan yerler tek tek)
    ═══ EN ÖNEMLİ SINIR           (bu işi yıkabilecek tek şey)
    AÇIK KARAR: yok/var · SÜRE:   (tek satır)
    >>> "Başla" dersen ...        (net bekleme cümlesi)

## Neden boş satır da yazılıyor

*"Tablo: DEĞİŞMİYOR"*, *"Cache: yok"* — boş bırakmak **"atladı mı, gerekmiyor mu"**
sorusunu doğuruyor. Yazılmış bir "yok" bir karardır; yazılmamış olan bir boşluktur.

## SQL üretimi olan işte Tablo satırı

Yalnız tablo adı yetmez, **ne işe yaradığı** da yazılır:

> *"Tablo: ChatMessageReport açılıyor — engellenen mesajların kaydı, 'hangi
> kullanıcı kaç kez denedi' sorusunu cevaplamak için. Migration elle yazılıyor."*

## Tutmayan üç deneme — ve neden

**Deneme 1 (karar odaklı):** en üstte "senden ne istendiği", sonra iş listesi,
sonra tek risk. Teknik detay kasten çıkarılmıştı.
**Neden tutmadı:** *"mesaj kaydına rozet eklenecek"* cümlesi Mert'in o modülü
bilmesini varsayıyor. Aynı hata — hakimiyet varsayımı.

**Deneme 2 (soru-cevap):** *"Ne yapacaksın? Karar vermem gereken bir şey var mı?
Ne kırılabilir?"* başlıkları.
**Neden tutmadı:** biçim değişti, içerik eksikliği aynı kaldı.

**Deneme 3 (kullanıcı odaklı):** *"bugün ne bozuk → iş bitince ne olacak"*.
Teknik detay tamamen çıkarıldı.
**Neden tutmadı — ve bu asıl ders:** Clara ters yöne gitti. Mert teknik detayı
**daha fazla** istiyordu, daha az değil. Kendi cümlesi:

> *"Ben şu an hangi yapıya dokunulacak bilmiyorum, hangi cache kullanılacak
> bilmiyorum, veri nereden alınacak bilmiyorum. Engelleme backend'de mi yapılacak
> yoksa DB'ye mi yazılacak bilmiyorum. Handler'da process nasıl ilerleyecek
> bilmiyorum."*
> *"Teknik olmasın tabii ki, ama akışsal da anlatsın istiyorum."*

**Ayrım kritik: teknik TERİM değil, teknik AKIŞ.** *"Tek projeksiyonlu sorgu +
bellekte eşleştirme"* terim; *"mesajlar okunur → kullanıcı ID'leri çıkarılır →
güncel bilgi tek sorguda alınır → bellekte birleştirilir"* akış. İkincisi
anlaşılıyor ve aktarılabiliyor.

## Kabul ölçütü

Mert'in kendi testi: **"başka biri bana bu modülü nasıl yaptın dese
anlatabiliyor muyum?"** Brief bunu sağlamıyorsa yetersiz.

Yani brief iki işi birden yapıyor: onay almak **ve** Mert'i modülün sahibi
haline getirmek.

## Tam örnek

Kabul edilen dördüncü deneme, iki iş kalemiyle:

```
ONAY İSTİYORUM — chat işi (#PRY-17484)

═══ İŞ 1 · Mesajlarda rozet/seviye güncel görünsün

Şu an: mesaj gönderilirken kullanıcının o anki rozeti mesajın içine
yazılıyor. Kullanıcı sonra seviye atlayınca eski mesajlar eski rozetle
kalıyor — yazılmış blob dosyası bir daha değişmiyor.

Nasıl çözüyorum: rozeti mesajın içinden okumayı bırakıyorum.
  Sohbet açılır → mesajlar blob'dan okunur (eskisi gibi)
  → o sayfadaki kullanıcı ID'leri çıkarılır
  → her birinin GÜNCEL rozeti/adı/fotosu tek sorguda okunur
  → mesajla bellekte birleştirilip ekrana gider

NEREYE YAZILIYOR
  Handler: mesaj listeleme handler'ı (GetChatMessages) — birleştirme
    adımı buraya giriyor, yeni handler açmıyorum
  DataLayer: ChatDataLayer'a "bu ID'lerin güncel bilgisi" sorgusu
    ekliyorum — tek projeksiyonlu, mesaj başına sorgu YOK
  Cache: seviye listesi zaten cache'te duruyor (TTCoin modülündeki
    seviye cache'i), onu kullanıyorum — yeni cache açmıyorum
  Tablo: DEĞİŞMİYOR. Kullanıcı bilgisi mevcut kullanıcı tablosundan
    okunuyor, yeni alan/tablo yok
  Emsal: TTCoinDataLayer'daki desen (insan developer yazmış, Mart 2026)

═══ İŞ 3 · Sohbette link engelleme

Şu an: kimse engellenmiyor, sohbete link yazılabiliyor.

Nasıl çözüyorum — kritik karar: engelleme mesaj kaydedilmeden
ÖNCE, gönderme adımında.
  Kullanıcı mesajı gönderir
  → metin link kontrolünden geçer
  → link varsa: kayıt YOK, kullanıcıya uyarı döner
  → link yoksa: normal akış, blob'a yazılır

Yani blob'a hiç yazılmıyor, sonradan temizlik gerekmiyor.

NEREYE YAZILIYOR
  Handler: mesaj gönderme handler'ı (SendChatMessage) — kontrol
    kaydetme çağrısından ÖNCE, ilk adım olarak
  Kontrol kodu: ortak yardımcıya yazılıyor (link tespiti), böylece
    duyuru/yorum gibi başka yerlerde de kullanılabilir
  DataLayer: DOKUNULMUYOR — engelleme veri katmanına inmiyor
  Cache: yok
  Tablo: DEĞİŞMİYOR — engellenen mesaj hiç kaydedilmiyor, log
    tablosu da açmıyorum (istersen ayrı iş olarak açılır)
  Doğrulama: 37 örnekle iki sıkılık denendi; seçilende kaçan link 0,
    masum engel 100'de 3

═══ NEYE HİÇ DOKUNMUYORUM
Socket tarafı · geçmiş mesaj dosyaları · mesaj saklama yeri
(blob kalıyor) · mevcut duyurular · kullanıcı tablosu

═══ EN ÖNEMLİ SINIR
Mesajlar blob'da dosya olarak duruyor ve geçmiş dosyalar geriye
dönük yazılmıyor. Bu işte alan EKLEMEK güvenli, var olan bir alanı
yeniden adlandırmak yıkıcı olurdu. Sadece ekleme yapıyorum.

AÇIK KARAR: yok · SÜRE: bugün

>>> "Başla" dersen kodlamaya geçiyorum.
```

## Gereksinim olarak (PAM'e, henüz devredilmedi)

Bu kalıp bir **developer brief** kuralıdır — BE/FE/MB'nin plan onayı isterken
uyacağı biçim. Kanonda şu an brief zorunluluğu var
(`WEB-BEHAVIOR-NO-COMMIT-WITHOUT-BRIEF` / OY karşılığı) ama **biçimi tanımlı
değil**, o yüzden her agent kendi anlatısını kuruyor.

Kalıbın kendisi yukarıda. Eklenmesi gereken üç kural:
1. Her iş kalemi üç bloktan oluşur (şu an ne oluyor / nasıl çözüyorum-akış /
   nereye yazılıyor).
2. "Nereye yazılıyor" bölümünde beş satır **her zaman** yazılır; boş olan
   "yok"/"DEĞİŞMİYOR" diye açık yazılır.
3. Ölçüm anlatısı brief'e girmez — sonuç girer (*"kaçan link 0, masum engel
   100'de 3"*), yöntem anlatısı sorulunca verilir.

## İlgili

- `incelemeler/pa-davranis-senaryolari/senaryo-1-erken-adimlama.md`
- `kararlar/2026-08-04-cok-proje-yonetim-duzeni.md`
- `gunluk/2026-08-04.md`
