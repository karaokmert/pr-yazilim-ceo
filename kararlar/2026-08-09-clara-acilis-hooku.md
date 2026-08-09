# Clara açılış hook'u — tasarım ve settings yazma yetkisinin daralması

**Tarih:** 2026-08-09
**Karar veren:** Mert
**Durum:** Kapalı

## Karar

İki karar bir arada:

**Bir — açılış hook'u sinyal + direktif tasarımıyla çalışır.** Eski `clara-acilis.sh`
(3 Ağustos, hiç bağlanmamış) açılışta tüm skill'leri okutuyordu; bu her oturuma yük
bindirir ve bugünkü kanonla çelişir (skill'ler işi geldiğinde tetiklenir). Yeni hook
**mod kararı vermez** — dört sinyali deterministik toplar (son kapanış dokümanının
adresi · açık kanal kutuları · açık agent oturumları · uyarı: pwd sinyal değildir)
ve tek direktif basar: `oturum-duzeni`'ni aç, modu sinyallerden belirle, belirsizse sor.

**İki — Clara kendi hook kaydını KENDİ reposunun `settings.json`'ına yazabilir.**
`CLA-ASK-BEFORE-WRITING-OUT` istisnası "settings.json yazılmaz" diyordu; bu karar onu
görünür biçimde daraltıyor: `pr-yazilim-ceo/.claude/settings.json` içindeki **hooks
bloğu** Clara'nın kanonunun parçası sayılır ve Clara yazabilir. Sınır aynen duruyor:
**permissions bloğu ve global `~/.claude/settings.json` hâlâ yasak** — onlar kapı
açar, hook kaydı açmaz.

## Gerekçe

Açılış ritüeli (`oturum-duzeni` skill'i) Clara'nın hafızasına emanetti ve hafızaya
emanet ritüel atlanıyor. Kök sebep iki mekanik gerçek:

- **pwd körlüğü:** VS Code profili `cd pr-yazilim-ceo && claude --agent clara` ile
  açıyor — pwd her oturumda evi gösterir, oturumun konusunu göstermez. Clara bu yüzden
  kendini hep EV modunda sanıyordu.
- **Skill preload çalışmıyor** (2026-08-03 ölçümü) — açılış talimatını frontmatter'a
  koymak işlemiyor.

Hook bu ikisinin yamasını değil sebebini kaldırıyor (`CLA-FIX-THE-CAUSE`): "açılışı
unutma" kuralı yazmak yerine sinyalleri her açılışta mekanik olarak eline veriyor.

Settings daralması olmadan hook bağlanamazdı: kaydı her seferinde Mert'in yapıştırması
ya kuralı sessizce deldirir ya işi süründürürdü. Görünür karar ikisinden de ucuz.

## Ölçümler (2026-08-09 oturumu)

- `CLAUDE_CODE_AGENT` Clara'nın kendi oturumunda `clara` dolu geliyor — kapı mekanizması
  çalışır (6 Ağustos'taki boş-değişken arızası fabrika alt-agent bağlamındaydı, ayrı).
- Eski hook hiçbir settings'e bağlı değildi: global SessionStart'ta yalnız git satırı
  var, bu oturumda script çıktısı yok.
- `~/.pr-kanal/` altında 14 dizinden 12'si test artığı — hook bu yüzden yalnız DURUM'u
  ACIK olanları basar (gürültü filtresi).

## Ek — aynı gün: `gunluk/` proje bazlı ayrıştı (Mert, 09:33)

İlk tasarımın eksiği ilk gerçek koşumda çıktı: *"son kapanış"* sinyali **tek akıştan**
geliyordu. Goat için açılan yeni Clara, en üstte EV'in kapanışını buldu ve Mert'e EV'in
push kuyruğunu özetledi — Mert yakaladı: *"osinif'la goat'taki günlük karıştığında yeni
açılan Clara onu özetleyemez, gereksiz özet verir."*

Sebep hook'ta değil dosya düzenindeydi (`CLA-FIX-THE-CAUSE`): kapanışlar tek isim
uzayını paylaşıyordu, *"en yeni"* anlamsızdı. Düzeltme:

- **`gunluk/{proje}/` ayrımı** — EV işi `gunluk/ev/`, yönetilen projeler kendi adıyla
  (`goat/`, `websitesi/`...). Günlük dosyası da kapanış da aynı klasöre.
- **Hook sinyali proje bazlı liste oldu** — her projenin son kapanışı ayrı satır +
  direktif: *yalnız kendi modunun kapanışını oku, diğerini özetleme.*
- **Eski düz dosyalar `gunluk/ev/`e taşındı** — geçmiş kayıtlar karışık içerikli
  (Goat gözlemi EV günlüğünün içinde), geriye dönük bölünmedi.
- `oturum-duzeni` skill'i ve `project_durum.md` yeni yollara güncellendi.

## İlgili

- `kararlar/2026-08-03-clara-yazma-sinirinin-degismesi.md` — yazma sınırının önceki daralması
- `.claude/hooks/clara-acilis.sh` — hook'un kendisi
- `.claude/settings.json` — SessionStart kaydı
