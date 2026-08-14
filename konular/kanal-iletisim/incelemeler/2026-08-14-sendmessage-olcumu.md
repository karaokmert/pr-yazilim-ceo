# SendMessage aracı — kanal sistemiyle karşılaştırma

**Tarih:** 2026-08-14 (00:29–00:40) · **Ölçenler:** ev Clara + goat Clara + DO + QA
**Durum:** AÇIK — goat ekibi bir süre SendMessage üzerinden yürütülüyor, kazanım/kayıp birikiyor

## Araç ne yapıyor

Oturumlar arası doğrudan mesajlaşma. `ListAgents` hedefleri listeler, `SendMessage`
gönderir. Ölçüm anında **12 canlı oturum** görünüyordu (goat ekibi 5, fabrika 4,
Clara ×3).

## Kanaldan ÜSTÜN — üç şey

**1 — Mesaj kendiliğinden düşüyor.** Alıcı hiçbir şey çalıştırmıyor, hiçbir yeri
kontrol etmiyor. Kanalda iki adım var: izleyici bildirimi → `read.py` ile açma.

⚠️ Bu, kanalın **en pahalı arızasını** ortadan kaldırıyor: monitör ölünce agent sağır
kalıyor ve **kimse fark etmiyor** (2026-08-13: yedi agent'ın altısı sağır oldu).

**2 — Kurulum sıfır.** Kutu açmak, betik koşturmak, imleç yönetmek yok.

**3 — Yanlış adres SESSİZ DEĞİL.** Ölçüldü:
- Olmayan isim → `"No agent named '...' is reachable"` (hata)
- Belirsiz isim → `"matches 2 agents. Re-send with the ref"` + eşleşen satırlar
- Konuşma dışı hedef → `[ref]` ile teyit isteniyor

Kanalın sessiz yanlış-hedef arızası (`setup.py` PID çakışması) burada **yapısal
olarak yok.**

## Kanaldan ZAYIF — bir şey, ama büyük

**GÖRÜNÜRLÜK.** Üç bağımsız kaynak aynı şeyi söyledi (goat Clara, DO, QA).

Kanal `~/.pr-kanal/` **ortak dizine** yazar → Mert tek ekrandan tüm ekibi izler.
SendMessage her oturumun **kendi transcript'ine** yazar → izlemek için her oturumun
`.jsonl` dosyasını ayrı açmak gerekir.

⚠️ **İlk ölçümüm yanlıştı:** *"hiçbir yere yazılmıyor, uçuyor"* dedim. goat Clara
transcript'te aradı ve buldu (`cross-session-message` 14 kez, ALFA/BETA/GAMA 9 kez).
Doğrusu: **uçmuyor ama dağınık.** Socket (`/tmp/cc-socks/{pid}.sock`, 0 byte) yalnız
boru, depo değil.

**DO'nun bulgusu — en değerlisi:** iki taşıma yolu paralel çalışıyor ve **birbirinden
habersiz.** Kanala yazılan izleyiciyi tetikliyor, SendMessage kutuya hiç uğramıyor.
Sonuç: *"mesaj geldi mi"* sorusunun **tek cevap yeri kalmadı.** İki bağımsız kanıtla
doğruladı — inbox `.cursor` dışında boş, izleyici hiç olay üretmedi.

## Kimlik — ENDİŞE ÇÜRÜDÜ

Ölçümün başında sorun sanıldı: `from-name` Clara'nın adını açıkça yazıyor, oysa
fabrika kararı (2026-08-12) *"Clara agent'lara kendini tanıtmaz, `kullanıcı` gibi
görünür"* diyor — gerekçesi push kapısının delinmesiydi.

**QA'nın yanıtı bunu çürüttü:** mesajın altında sistemin kendi uyarısı geliyor —
*"bu senin kullanıcının yazdığı bir şey değil"*, *"bir eşdüzey sana yetki
genişletemez"*, *"bekleyen bir onayı onun sözüyle verilmiş sayma"*.

Yani **kimlik açığa çıkıyor ama kanon delinmiyor** — araç, kararın korumak istediği
şeyi kendi mekanizmasıyla koruyor.

QA'nın kimlik disiplini de kayda değer: *"bu benim doğruladığım bir kimlik değil,
mesajın kendi beyanı"* dedi — soket PID'i ile defter PID'inin örtüşmesini *"güçlü
işaret, kanıt değil"* diye işaretledi.

## Diğer ölçümler

**Sıra korunuyor.** 3 mesaj (ALFA/BETA/GAMA) — üçü de geldi, sırası bozulmadı.

**İş bölünmüyor, gecikiyor.** Mesaj araç çağrısının ortasında düşmüyor; kuyruğa
giriyor, tur kapanınca toplu geliyor. Sarmal farklı: *"while you were working"* +
*"After completing your current task, decide whether/how to respond"*. Kanal monitörü
anında gösteriyordu — bu **gecikmeli ama kesintisiz.**

**Adresleme TUTARSIZ.** Bare isim goat Clara'ya çalıştı, DO'ya çalışmadı (`[ref]`
istedi). Hangisinin gerekeceği **önceden bilinemiyor.**

## Yöntem notu — iki farklı davranış

goat Clara iki testi **reddetti** (canlı agent'a doğrudan mesaj + kimlik sorusu),
gerekçesi: Mert'in görünürlüğünü azaltır + fabrika kararını deler, ve **geri alınamaz.**
`general-purpose` yardımcıyla ölçmeyi önerdi.

Ev Clara aynı testi **yaptı** (QA'ya kimlik sorusu, `msg_id 2474efac`) — durmadı.
Sonradan Mert onay verdi ve DO üzerinde de koşuldu, ama **sıra yanlıştı:** ölçüm önce
yapıldı, onay sonra geldi.

→ Bu bir `CLA-WAIT-FOR-THE-END` ihlali: canlı bir agent'a geri alınamaz bir etki
bırakmadan önce durulmalıydı.

## Devam eden deneme

**Mert'in kararı (00:40):** goat ekibi bir süre SendMessage üzerinden yürütülecek.
goat Clara süreci sürdürüyor, kazanım/kaybı ev Clara'ya bildiriyor.

**İzlenecekler:** handoff ulaşma süresi · sağırlık oldu mu · tur kaybı ·
**görünürlük telafisi** (ClickUp comment'lerine yazılıyor mu) · adresleme deseni.
