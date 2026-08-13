# Karar — ★ Question başlığı zorunlu + tanımlayıcı tek başına basılmaz

**Tarih:** 2026-08-13, 22:59–23:10
**Karar mercii:** Mert
**Uygulandığı yer:** `~/.claude/hooks/sessiz-mod.sh` (global SessionStart hook)
**Yedek:** `~/.claude/hooks/sessiz-mod.sh.bak`

## Karar

Hook'taki `★ Question` bölümüne **zorunlu başlık** eklendi ve yeni bir bölüm
açıldı: **tanımlayıcı tek başına basılmaz.**

Mert'in cümlesi: *"Question bölümünde sorulan sorunun bağlamı açıklaması net
olur. Kullanıcı başlığı okuyarak yanıt verebilecek kadar net bilgi içermelidir."*
Ve ikincisi: *"ClickUp taskinden bahsederken daima task başlığını da ekle, tek
başına task id basılmaz."*

## Neden — eski kural soyuttu, ölçülemiyordu

Hook'ta zaten bir kural vardı: *"Kutunun içi kendi kendine yetmeli."*
**İşlemedi.** Sebebi mekanik: kural bir SONUÇ tarif ediyordu (yetmeli) ama
**ne yazılacağını** söylemiyordu. Ölçütü yoktu, dolayısıyla ihlali de görünmüyordu.

Aynı oturumda kanıtlandı: Clara `setup.py` PID düzeltmesini sorarken kutuya
`setup.py`, `PID`, `f-string` yazdı — bunların ne olduğu kutunun İÇİNDE
açıklanmıyordu, yukarıdaki paragraflarda açıklanmıştı. Yani kural yürürlükteydi
ve yazan onu çiğnediğini fark etmedi.

**Yama olmaması için:** *"kendi kendine yetmeli"* cümlesinin üstüne bir uyarı
eklenmedi — cümlenin kendisi somut hâliyle DEĞİŞTİRİLDİ (`CLA-FIX-THE-CAUSE`).

## Ne yazıldı

**Başlık zorunlu.** Kutu bir konu adıyla açılır (isim tamlaması, soru değil).
Ayıran örnek: *"setup.py kutu adı çakışması"* evet; *"Ne yapalım?"* hayır.
Ölçüt: kullanıcı YALNIZ başlığı okuyarak neyin sorulduğunu anlayabilmeli.

**Gövde kendi kendine yeter — ve bu artık somut.** Kutuda geçen her dosya adı,
kod parçası ya da terim kutunun İÇİNDE açıklanır, **yukarıda açıklanmış olsa
bile.** Eski hâlde bu boşluk vardı: yazan yukarıda anlattığı için kutuyu eksik
bırakıyordu.

**Tanımlayıcı tek başına basılmaz.** ClickUp task ID'si başlığıyla yazılır —
`PRC-41 (sponsor listesi filtresi)`. Aynı kural commit hash, PR numarası,
branch adı ve dosya yolu için de geçerli. Gerekçe: tanımlayıcı ADRESİ verir,
başlık NE OLDUĞUNU söyler; adres tek başına okuyanı tıklamaya zorlar.

## Kapsam — bu bir hook, kanon değil

Hook global (`SessionStart`), yani **tüm agent'lara** gidiyor: Clara + OY
ekibinin dokuz rolü. Mert bunu bilerek onayladı — *"herkes buna göre ilerlesin."*

⚠️ **Sınırı:** hook agent'ların body'sinde iz bırakmaz. Bir agent'a *"bu kural
nerede yazılı"* diye sorulursa gösteremez; davranışında olur, kanonunda olmaz.
Kalıcı olması istenirse fabrikaya (`skill-project`) gitmesi gerekir.

## Ölçüldü / ölçülmedi

**Ölçüldü:** hook koştu (`çıkış kodu 0`), geçerli JSON üretti, yedi anahtar
metnin içinde doğrulandı (`Başlık zorunlu`, `Konu:`, `Tanımlayıcı tek başına
basılmaz`, `PRC-41`, `Turda bir kez`, `İş anlatımı`, `Sınır`). Metin 2.895
karakter.

**ÖLÇÜLMEDİ:** kuralın sahada TUTUP TUTMADIĞI. Yazılmış olmak uygulanmış olmak
değil. Dünkü sessizlik hook'u ölçümü de aynı borçla kapanmıştı (2 oturum /
26 mesaj — örneklem yetersiz).

**Yapılacak ölçüm:** 200+ mesaja ulaşınca üç şey birlikte ölçülür —
(1) sessizlik hook'unun ara-blok etkisi, (2) `★ Question` kutularında başlık
oranı, (3) task ID'lerinin kaçında başlık var. Üçü de aynı hook'tan geliyor,
tek taramada çıkar.
