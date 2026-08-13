# `/kanal` komutu — canlı test (egelisaglik, 2026-08-13)

**Ne ölçüldü:** yeni `/kanal` komutunun iki dalı da (merkez YOK → dur,
merkez VAR → kur) gerçek agent'larla, gerçek projede.

**Kapsam:** egelisaglik projesi · üç agent (clara, ui-designer, ardından
devops) · 19:06–19:26 arası. **Neye bakılmadı:** çok-Clara kilidi (tek Clara
açıktı, kilit tetiklenmedi), kapanış/arşiv dalı (ADIM 6 hiç koşmadı),
`websitesi` namespace'i (yalnız `ozel-yazilim` sınandı).

## Geçen dört şey

**Merkez YOK dalı — kutu kurulmadı.** Klasör (`~/.pr-kanal/egelisaglik/`)
19:17'ye kadar hiç oluşmadı, o sırada altı agent açıktı. Hook kaldırma
işi tuttu: eskiden altı agent altı kutu açardı.

**Merkez VAR dalı — kutu kuruldu.** UID defterde canlı `clara` kaydını
buldu, `kill -0 3367` geçti, kutusunu kurdu.

**Namespace düzeltmesi tuttu.** `ozel-yazilim__ui-designer` — `:` gitti
(glob kırılması çözüldü), namespace kaldı (`websitesi` ile çakışma önlendi).

**Zincir kapandı.** UID'nin `INFO` mesajı merkez inbox'ına düştü.
Dosya: `20260813-192338.884094-ozel-yazilim__ui-designer-20260813-1922.json`

## Üç arıza — üçü de komutta, agent'larda değil

**1 — Çift tarih damgası.** Kutu adı `...-1922-1923` çıktı.
Sebep: `setup.py:38` `SESSION = strftime("%Y%m%d-%H%M")` ile damgayı
**kendisi** üretiyor; komut ADIM 0'da agent'a da *"damgala"* diyordu.
İki agent üst üste aynı sonucu verdi (clara + ui-designer) — kişisel
hata değil, arayüz belirsizliği.
→ Düzeltildi: komut artık *"tarih ekleme, betik ekler"* diyor.

**2 — Defter atomik yazılmıyor.** Monitör defteri yazılırken okudu ve
`ui-designer` kaydını iki kez saydı. Veri bozulmadı (sonraki tarama
düzeldi) ama **okuyan taraf yarım JSON görebiliyor.**
→ Düzeltildi: komut `os.replace()` ile takas emrediyor.

**3 — ADIM 1'de sınır yoktu.** Goat'ta UID beş tur tarama yaptı; komut
*"defterde ara"* diyordu ama *"bu tek komut yeter"* demiyordu. Boşluk
görünce doldurdu — doğru refleks, eksik olan sınırdı.
→ Düzeltildi: *"defter tek kaynaktır, yokluğu kanıt gerektirmez."*

## Fabrikaya gidecek bulgu

**`setup.py` arayüzü belirsiz:** "tam ad" mı bekliyor, "önek" mi belli
değil. Komut tarafında yamalandı ama asıl düzeltme betikte —
parametre adı ya da docstring bunu söylemeli.
Dosya: `skill-project/tools/kanal/setup.py:38`

## Clara'nın kendi ölçüm hataları (aynı oturum)

**`basename` ile yol karşılaştırma** — `egelisaglik` adını
`/Users/karaok/p/egelisaglik` diye tamamladım, gerçeği
`/Users/karaok/p/ozel-yazilim/egelisaglik`'ti. Defterdeki doğru `repo`
alanını "agent uydurmuş" diye raporladım.
→ Kanona yazıldı: `feedback_karsilastirma_ayni_bicimde`

**`ls` ile yokluk ölçümü** — inbox'ı "boş" diye raporladım; `ls` gizli
dosyaları göstermiyor, mesaj oradaydı. `find` gerçeği verdi.
Aynı sınıf hata: aracın ne ölçtüğünü sormadan sonucu kullanmak.

---

# İkinci yarı — sahiplenme ve çöküş (19:34–20:00)

## Arıza 4 — ikinci Clara kutuyu SAHİPLENDİ (en ciddi bulgu)

İkinci Clara açıldı (PID 85534, 19:34). `/kanal` **hiç çalıştırılmadı** — yani
tek-Clara kilidine hiç ulaşılmadı. Açılış akışı (`oturum-duzeni` YÖNETİM ADIM 3)
onu doğrudan kanala götürdü: birinci Clara'nın kutusunu buldu, **beş mesajı okudu**,
imleci ilerletti.

**Birinci Clara o mesajları bir daha görmedi** — `.cursor` tek, okuyan ilerletiyor.
Ve kaybettiğini bilmiyor: `read.py` ona *"yeni mesaj yok"* diyor, teknik olarak doğru.

**Kök neden — kanonda iki kural çelişiyordu (ikisi de Clara'nın kendi yazdığı):**
- EV modu: *"açık kutu görürsen dokunma"* ✅
- YÖNETİM ADIM 2: *"ölç ama KURMA"* — kurmayı yasaklıyor, **okumayı değil**
- YÖNETİM ADIM 3: *"kanal kutuları okunur"* ❌

Agent YÖNETİM'deydi, ADIM 3'ü uyguladı — **kanona uydu.** Arıza itaatsizlikte değil,
çelişen kural çiftinde.

→ Düzeltildi: ADIM 2'ye sahiplenme yasağı, ADIM 3 *"KENDİ kutun"* oldu.

**Kilit yanlış yerde:** `/kanal` komutunun içinde yaşıyor ama açılış akışı o
komuttan geçmiyor. Kapıya kilit takılmış, duvarda delik var.

## Arıza 5 — "iş bitti" ile "oturum bitti" ayrılmamıştı

19:53'te kapanış adımı yazıldı: *"oturum kapanırken kutu arşivlenir."*
**"Oturum kapanmak" tanımlanmadı.**

Altı dakika sonra sistem çöktü: DO (19:58) → UID (19:59) → Clara (20:00)
kutularını arşivledi, **üçü de canlı kaldı.** Yedi agent'ın altısı sağır oldu —
mesaj alamaz, gönderemez, merkez iş veremez.

Tetikleyici muhtemelen Clara'nın *"kapanışa geç"* mesajıydı (arşivde
`195805-clara.json` duruyor).

→ Düzeltildi: *"iş bitti ≠ oturum bitti"*, ayıran soru **"bu terminal kapanıyor mu?"**
Ayrıca merkez tarafına uyarı: *"kapanışa geç"* derken belirsiz bırakma.

## Kazanım — `archive.py` defter temizliği (Clara yazdı, sahada çalıştı)

`archive.py` `live-channel.json`'ı **hiç bilmiyordu**; ADIM 6 *"deftere yaz ve sil"*
diyordu ama silme tamamen agent'ın hatırlamasına bağlıydı — unutulduğunda uyarı yok.

Eklenen kod (satır 120, `sys.exit(3)`'ten **önce** — `--force` dalında da çalışsın):
kutu adına göre kaydı bulur, atomik yazar (`os.replace`), bulamazsa uyarı basar.

**Üç kez sahada çalıştı** (DO 19:58, UID 19:59, Clara 20:00) — üçünde de doğru satırı
sildi, diğerlerine dokunmadı. Kontrollü testte de doğrulandı.

**Neden asıl çözüm bu:** kural hatırlamaya dayanır, kod dayanmaz.

## Veri kaybı: yok

Üç arşiv düzgün, Clara'nın kutusunda 14 mesaj korunmuş, `HANDOVER.json`'lar yazılmış.

## Kapanışta duran durum

Yedi terminal açık (PA×2, QA, BE, UID, DO, Clara), **hiçbirinin kanalı yok.**
Defter `[]`. Yeniden kurmak için önce Clara'ya `/kanal`, sonra diğerleri.

## Fabrikaya gidecek üç bulgu

1. **`setup.py` arayüzü belirsiz** — "tam ad" mı "önek" mi bekliyor yazmıyor;
   iki agent üst üste çift damga üretti. (`setup.py:38`)
2. **`STATUS.md`'de `STATE: OPEN` ölü alan** — kapanışta güncellenmiyor, dosyanın
   kendi `LIVENESS` satırı bunu itiraf ediyor.
3. **`read.py` imleç sahipliği kontrol etmiyor** — `send.py` yazarken `ROLE`
   kontrolü yapıyor ama okumada hiç kontrol yok. Bugünkü kayıp buradan geldi.

## Clara'nın ölçüm hataları (dördü, hepsi aynı sınıf)

Aracın ne ölçtüğünü sormadan sonucu kullanmak:
- `basename` **ad** verir yol değil → yanlış proje yolu iddiası
- `ls` gizli dosyaları göstermez → "inbox boş" yanlış raporu
- `outbox` gönderimi kanıtlamaz → `send.py` doğrudan hedefe yazıyor
- **`kill -0` canlılık kanıtı değil** — kanonda iki kez çürütülmüş, Clara yine de
  sahiplenme yasağına ölçüt diye yazdı, sonra düzeltti. Hatası ters yönde:
  canlıyı ölü gösterir → canlı Clara'nın kutusu devralınır.
