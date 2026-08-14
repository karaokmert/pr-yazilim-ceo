# Merkez kapısı korunuyor — `kanal-acilis.py`'nin gerekçesi düştü

**Karar:** Mert, 2026-08-13 23:50 · **Ölçüm:** PCA · **Doğrulama:** Clara

## Karar

`/kanal` kanonu haklı: **merkez yoksa kutu kurulmaz.** 11 Ağustos'ta
`~/.claude/hooks/kanal-acilis.py` içinde yazılı olan *"merkez kapısı gereksiz"*
kararı **düştü.**

## Neden düştü — gerekçe yarısından çürüdü

Hook'un gerekçesi (satır 43-46):

> *"Merkez üç saat sonra gelse hiçbir mesaj **kaybolmaz.** İmleç kimin ne okuduğunu
> tutar. 'Merkez yoksa kanal anlamsız' varsayımı kanalı senkron sanmaktı."*

**Bu cümle doğru** ve bugün de doğru çıktı: PCA (21:52) ve PAD (21:52) merkezden
**7 dakika önce** açıldı, hiçbir mesaj kaybolmadı.

**Ama gerekçe yarısından çürük:** kayıp olmuyor, ama **okunmayan birikiyor.**
Ölçüm (2026-08-13, goat): **201 okunmamış mesaj**, imleç **iki gündür** ilerlememiş.
Yani *"gürültü zararsız, kayıp zararlı"* ilkesi burada tutmuyor — biriken mesaj
çalışmayan bir sistemi **çalışıyor gösteriyor.**

⚠️ Hook'un **kendi üst kısmı** (satır 17-24) zaten bunu söylüyordu: *"okuyacak merkez
olmaz, sonuç kanonun en kötü hâli: çalıştığı sanılan monitör."* Aynı dosya iki yerde
ters şey yazıyor.

## PCA'nın asıl katkısı — bulguyu çelişkiden boşluğa taşıdı

Kapsam *"`ISD-OPEN-YOUR-BOX` ile `/kanal` çelişiyor mu"* diye çizilmişti. PCA ölçtü:
**çelişemezler** — `ISD-OPEN-YOUR-BOX` (`is-duzeni:269-305`) merkez sorusunu **hiç ele
almıyor**, tek kelime geçmiyor; `references/kanal.md`'de de *"merkez yok"* diye dördüncü
bir durum tanımlı değil.

Yani ortada çelişki değil **boşluk** var. **Bu ayrım düzeltmenin yerini değiştiriyor:**
`/kanal` değişmeyecek, **hükmün kendisi tamamlanacak.**

Gerçek çelişki kapsamda olmayan **üçüncü metinle**: `kanal-acilis.py` ile `/kanal`,
ikisi **aynı ölçüme dayanıp ters hüküm üretiyor.**

## Gerçek arıza mekanik — kural tetikleyecek kişiye bağlı

| Metin | Dağıtım | Açılışta ulaşıyor mu |
|---|---|---|
| `ISD-OPEN-YOUR-BOX` | dört personelin **dördü** preload ediyor | ✅ her açılışta |
| `/kanal` metni | `~/.claude/commands/kanal.md`, kullanıcı yazınca | ❌ ulaşmıyor |
| `kanal-acilis.py` | **hiçbir `settings.json`'da bağlı değil** | ❌ hiç çalışmıyor |

Açılışta personelin eline geçen tek metin *"kutunu kur"* diyor ve merkezden
bahsetmiyor. Personel kurar. **Arıza her açılışta tetikleniyor, ama yalnız merkez
kapalıyken görünüyor.**

## Açık iş (bu turda yapılmadı)

**`ISD-OPEN-YOUR-BOX` tamamlanacak** — merkez durumu hükmün içine girecek.
`/kanal` değişmiyor. `kanal-acilis.py`'nin akıbeti (bağlanacak mı, silinecek mi)
ayrıca karara bağlı — şu an yazılmış ama çalışmayan bir dosya.

## Yöntem notu — PCA kendi vakasında taraftı

PCA'nın kutusu bugün merkez yokken kuruldu; yani ölçtüğü arızanın **öznesiydi.**
Devir bloğuna *"kendi davranışını savunma, ölçümü metinler üzerinden yap"* yazıldı ve
uydu: kendi vakasını savunmadı, kapsam dışına çıktığını bildirdi, üçüncü metni buldu.
**Taraf olan bir ölçümcüye sınır çizilirse ölçüm kullanılabilir kalıyor.**

---

## Boşluğun canlı kanıtı — PQA'nın kendi vakası (23:51)

Bulgu teorik değil. PQA kendi açılışını anlattı ve **kanıt o:**

> 21:52'de açıldım. `ISD-OPEN-YOUR-BOX`'ı okudum: *"kutunu kur, izleyicini kur,
> canlılığını doğrula, bir okuma yap."* Dört adım, **merkez sorusu yok.**
>
> Kutuyu kurmaya gittim ve `~/.pr-kanal/skill-project/` dizininin **hiç olmadığını**
> gördüm. O noktada **hüküm bana ne yapacağımı söylemiyordu.** Kurmadım — ama kural
> gereği kurmadım değil, *ortada merkez yok* diye kurmadım. **Bu çıkarım benim,
> kanonun değil.**
>
> Yani hükmü harfiyen uygulasaydım kutuyu kuracaktım ve okuyanı olmayan bir kutu
> açılacaktı. **Beni durduran hüküm değil, o an yaptığım muhakemeydi. Muhakeme her
> seferinde aynı çıkmaz.**

21:54'te `/kanal` geldi ve ADIM 1 merkez sorusunu sordu — koruma çalıştı, **ama
yalnızca Mert komutu yazdığı için.**

**Bu vakanın öğrettiği:** bugün arıza çıkmadı çünkü personel iyi muhakeme etti.
İyi muhakeme bir kural değil — **ölçülemez ve tekrarlanmaz.** Aynı boşluk PCA'da
ters yönde tetiklendi (kutuyu kurdu, bir mesajı okunmadan bekledi). İki personel,
aynı boşluk, iki farklı sonuç.

**Düzeltmenin yeri bu vakadan çıkıyor** (PQA'nın kendi formülasyonu): *"`/kanal`'ı
değiştirmek işe yaramaz çünkü `/kanal` zaten doğru davranıyor — sorun onun
tetiklenmesinin kullanıcıya bağlı olması. Hüküm preload ediliyor, komut edilmiyor.
**Koruma preload edilen tarafa yazılmalı.**"*
