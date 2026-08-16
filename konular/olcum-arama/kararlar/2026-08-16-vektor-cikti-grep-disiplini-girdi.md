# Vektör arama kanondan çıktı, grep disiplini girdi

**Tarih:** 2026-08-16 · **Karar:** Mert (Qdrant) + Clara (skill düzeltmesi)
**Dokunulan:** `~/.claude/skills/arama-disiplini/SKILL.md` (yeniden yazıldı)

## Ne değişti

**Çıkan:** *"Ne aradığını kelimeyle söyleyemiyorsan → vektör arama (Qdrant)"* kuralı.

**Giren:** dört maddelik `grep` disiplini — satır gösterme (`-l` değil `-h`), kelime
tahmini uyarısı, alt dize tuzağı, karşıt alan araması.

## Neden — iki ayrı gerekçe

### 1. Vektör arama artık YOK

Ölçüldü 2026-08-15: Qdrant bulut tarafı `403 ExpiredSignature`, yerel taraf `000`
(ayakta değil).

**Sebep arıza değil, Mert'in kararı:** *"Qdrant'ı mantıklı bulmadık ve kullanmadık,
o nedenle kapattım."*

⚠️ Clara bunu bilmiyordu ve kanonunda kural olarak duruyordu. Yani **kanon olmayan
bir araca yönlendiriyordu** — bir "niyet sorusu" geldiğinde vektöre gidecek, hata
alacak, sonra grep'e dönecekti. Ölü kural sessiz maliyet.

### 2. grep yanlış kullanılıyordu

Mert'in şikayeti: *"grep çok riskli oluyor, sürekli farklı bulgu çıkıyor."*

Ölçüldü, sebebi iki katmanlı:

**a) `-l` bayrağı cevabı kesiyor.** Aynı soru iki biçimde soruldu:
- `grep -ril "sendmessage"` → **11 dosya adı**, hiçbiri cevabı göstermiyor
- `grep -rih "sendmessage"` → **47 satır**, ilk 25'inde cevap + **bir çelişki** görüldü

İkinci biçimde hiçbir dosya açılmadan hem cevap hem çelişki çıktı. Birincisinde
11 dosya açmak gerekirdi.

**b) Kelime tahmini bulguyu değiştiriyor.** Aynı soru için dar kalıp doğru dosyayı
**hiç bulamadı** (dosya tam o klasördeydi), geniş kalıp **sekiz sonucun içine gömdü.**
Değişen dosyalar değil, Clara'nın seçtiği kelimeydi.

## Bugün bu hata neye mal oldu

Sabah Mert *"SendMessage'ı goat'ta denedik"* dedi, Clara *"hayır, kanaldı"* diye
karşı çıktı. Clara `-l` ile arayıp dosya adlarına bakmış, birini açıp okumuştu.

Satırla arayınca çelişki **kendiliğinden göründü**: iki satır birbirini kesiyordu ve
Mert haklıydı. Ayrıntı: `konular/kanal-iletisim/incelemeler/2026-08-16-sendmessage-celiskisi-cozuldu.md`

## Sınır

Satırla arama daha çok çıktı üretir. Kural *"hep satır göster"* değil:
**önce dizinle daralt, sonra satırla bak.** `-l` yalnız sayım ve toplu düzenleme
girdisi için doğru.
