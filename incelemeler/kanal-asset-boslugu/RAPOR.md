# Kanal betikleri git'te değil — boşluk ölçüldü, BÜYÜK

**Ölçen:** PCA (fabrika), 2026-08-08 18:56
**Rapor:** `agent-project/docs/fabrika/kanal-protokolu/asset-boslugu-olcumu.md`
**Tetik:** PQA'nın N8N gereksinim denetiminde B6 bulgusu

## Soru

N8N takımı kanal düzeni taşıyacak. Betikler nereden gelecek? Kanal kanonu
2026-08-07'de *"asset olarak fabrikaya taşınmaları kararlaştırıldı"* diyor —
**taşınmadı.** Boşluk küçük mü (betikler kolaylık) büyük mü (zorunlu altyapı)?

## Cevap: BÜYÜK — betikler zorunlu altyapı

**Ölçüm:** beş betik, **532 satır**, tek yerde (`~/.pr-kanal/agent-project/tools/`).
Fabrika git'inde **hiçbir kopyası yok** — iki eksende sınandı (dosya adı +
betiğe özgü string'ler), ikisi de boş döndü. Diğer proje dizinlerinde de yok.

`SABLON-JSON.md` **661 satır** ve o da repo dışında.

### Asıl bulgu: tel-üstü biçim tarif edilmiş, DURUM biçimi edilmemiş

PCA kendi okumasıyla cevaplayamayacağını söyledi (*"betikleri gördüm, tarafsız
değerlendiremem"*) ve **temiz bağlamlı bir yardımcıya sınattı** — yalnız iki
belge verildi, `tools/` açması yasaklandı.

**Sonuç: beş betikten hiçbiri uyumlu biçimde yeniden yazılamaz.**

```
VAR  mesaj JSON'u (tam şema) · dosya adı deseni · STATUS.md ·
     çıkış kodları · bayraklar · atomik yazma
YOK  .cursor iç yapısı · .announced · HANDOVER.json şeması ·
     archive-log.json · arşiv hedef dizini · ~/.pr-kanal kök yolu ·
     watch.py çıktı satırı · read.py ekran biçimi
```

`.cursor` belgelerde **dört kez** anılıyor, hiçbirinde içeriği yok — yalnız ne
işe yaradığı yazılı.

**Ayrışmaların beşte dördü sessiz sınıfta.** En kritiği `.cursor`: biçim farklı
olursa mevcut `read.py` ya `rc=2` verir ya **hepsini yeniden okur** — belgenin
kendi yasakladığı iki yönlü sessiz hata. `HANDOVER.json` ayrışırsa **devir
sessizce kaybolur**, ki mekanizmanın var olma sebebi tam buydu.

**Mesajlar taşınabilir olurdu** (JSON tam tanımlı). Ayrışma mesajda değil
**durum dosyalarında** — iki kanal birbirinin mesajını okur ama birbirinin
**nerede kaldığını** bilmez.

### Belge kendi yetersizliğini zaten ölçmüş

`SABLON:640-648`: *"şablon NEDEN BÖYLE'yi cevaplıyor, NASIL YAPILIR'ı ARAÇLAR
cevaplıyor."* PCA'nın bağımsız sınaması bunu doğruluyor.

**Fark:** o ölçüm *"dört adım kuruldu"* diyor (betikler **varken** kullanım);
bu ölçüm *"beş betik yeniden yazılamaz"* diyor (betikler **yokken** üretim).
Çelişmiyorlar — boşluk ikincisinde.

## İki yan bulgu

**Kanona geçen tespit eksik.** `kanal.md:274-276` boşluğun **varlığını** taşıyor
ama şablondaki asıl tespiti — *"şablon nasıl-yapılır'ı cevaplamıyor"* —
taşımıyor. Git'teki kanon boşluğun varlığını biliyor, **büyüklüğünü bilmiyor.**
Ve büyüklüğü anlatan cümle, tam da git dışında kalan dosyada duruyor.

**Üç iç çelişki.** `STATE: OPEN` (:381) ile `DURUM: AÇIK` (:602) aynı dosyada —
gerçek `STATUS.md` `STATE: OPEN` kullanıyor, :602 yanlış. Ve filtre
`ERROR:|INFO:` arıyor (`kanal.md:74`) ama şablon **`HATA:`** çıktısı tarif
ediyor (:487). PCA bunu **ölçemedi** ve ölçmeden söylemedi — o oturumda hata
durumu hiç oluşmadı. Betik Türkçe basıyorsa filtre hata satırlarını geçirmez ve
bu **sessiz** bir arıza olur.

> Clara notu: izleyici 22:15'te yeniden kurulurken filtreye `HATA:` eklendi —
> ölçüm beklerken maliyeti sıfır olan bir önlem.

## Ne yapılacak

**Karar Mert'te.** İki yol, PAM gereksinimde ikisini de bedelleriyle yazdı:

- **Fabrikaya asset olarak taşınır** → fabrikanın bekleyen işi N8N takımının
  **önkoşulu** olur
- **N8N takımı kendi mekanizmasını kurar** → iki uygulama doğar ve ayrışır
  (ve yukarıdaki ölçüm ayrışmanın **sessiz** olacağını gösteriyor)

**Neden önkoşul:** PAD *"kanal kur"* talimatını uygulayamaz — kuracağı şeyin
kaynağı yok. İşaretlenmemiş önkoşul üretim anında durdurur.

## PCA'nın ölçmedikleri

Betiklerin **içeriği** okunmadı (kasıtlı — sınamanın geçerliliği buna bağlıydı),
yani *"betikler belgelenmemiş davranış taşıyor mu"* açık. Diğer on proje
dizininin nasıl kurulduğu ölçülmedi. Taşımanın **nasıl** yapılacağı kapsam dışı.
