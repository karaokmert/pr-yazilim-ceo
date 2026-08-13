# relay.sh — komut enjeksiyonu bulgusu

**Tarih:** 2026-08-10 · **Durum:** fabrikaya iletilmeyi bekliyor
**Kaynak:** otomatik güvenlik taraması (HIGH), Clara doğruladı

---

## Devir bloğu — çalışma anında kopyala, PAM'e taşı

```
KİMDEN → KİME: Clara → PAM
TÜR: İŞ

NE: Kanal relay betiğinde komut enjeksiyonu var. `.claude/relay.sh`
    mesajın `to` alanını doğrulamadan kabuk komutuna gömüyor
    (`ls -d $K/$hedef-*/`, tırnaksız) ve dosya yolunu Python
    kaynağına string olarak interpolasyonla koyuyor
    (`python3 -c "...open('$out')..."`). Aynı sorun `from` alanında da var.
    JSON'a `"to": "; <komut>"` yazan bir mesaj kabukta komut çalıştırır.

NEDEN: Betiğin işi başkasının yazdığı dosyayı okumak — girdiye
    güvenmemesi gereken tek yer tam da burası. Kötü niyet şart değil:
    bir agent bozuk JSON üretse de aynı yola girer. Ve betik taşıma
    yöneticisinin elinde çalışıyor, yani hata kanalın ortasında patlar.
    Otomatik güvenlik taraması HIGH olarak işaretledi (2026-08-10).

NEREYE BAK: /Users/karaok/p/pr-yazilim-ceo/.claude/relay.sh
    (satır 11, 13, 16 — betik gece kuruldu, commit 3288b9d)
    Aynı desenin ~/.pr-kanal/*/tools/ altındaki betiklerde de olup
    olmadığı KONTROL EDİLMEDİ — kapsam fabrikada ölçülmeli.

BEKLEDİĞİM: düzeltilmiş betik + aynı desenin kanal araçlarında
    taranmış olması. Betiğin nerede yaşayacağı (repo içi mi, kanal
    tools/ altında asset mi) da fabrikanın kararı.
```

---

## Dayanak — ne ölçüldü

**Betiğin yeri:** `.claude/relay.sh`, 821 bayt, 2026-08-10 06:51.
Commit izi: `3288b9d` (kuruldu) → `8f29d29`.

**Açık satırlar:**

```bash
# satır 11 — dosya yolu Python KAYNAĞINA gömülü
hedef=$(python3 -c "import json;print(json.load(open('$out'))['to'])" 2>/dev/null)

# satır 13 — tırnaksız değişken, glob ile birlikte kabuğa gidiyor
hedef_kutu=$(ls -d $K/$hedef-*/ 2>/dev/null | head -1)

# satır 16 — aynı desen, `from` alanı
gonderen=$(python3 -c "import json;print(json.load(open('$out'))['from'])" 2>/dev/null)
```

**İstismar yolu:** kutuya düşen bir JSON'da `"to": "; <komut>"` →
satır 13'te komut ikamesi (`$(...)`) içinde kabuk onu ayrı komut olarak
yorumlar.

## Neden bugün patlamıyor — ve neden yine de düzeltilmeli

**Bugünkü risk düşük:** kutulara yazan şey kendi agent'larımız ve
`send.py`; dışarıdan girdi almıyor.

**Ama üç sebeple bırakılmaz:**

1. Betiğin **tanımı gereği** işi başkasının yazdığı dosyayı okumak —
   girdiye güvenmemesi gereken tek yer burası.
2. **Kötü niyet gerekmiyor.** Bozuk JSON üreten bir agent aynı yola sokar;
   `to` alanına boşluk/noktalama gelen bir mesaj yeter.
3. Betik **taşıma yöneticisinin** elinde çalışıyor — hata kanalın
   ortasında, zincirin görünmediği yerde patlar.

## Düzeltmenin şekli (fabrikanın kararı, öneri değil emir değil)

Üç dokunuş yeterli görünüyor:
- dosya yolunu Python'a **argv ile** geçir (`-c '...' "$out"`), kaynağa gömme
- `to`/`from` alanını **allowlist**'ten geçir: `^[a-zA-Z0-9_-]+$`
- `ls` çağrısındaki değişkeni **tırnakla**

**Ama kapsam Clara tarafında ölçülmedi:** aynı desen `~/.pr-kanal/*/tools/`
altındaki beş betikte (`setup/send/read/watch/archive.py`) var mı,
bakılmadı. Fabrika önce onu taramalı — tek dosya düzeltip aynı hatayı
beş yerde bırakmak, düzeltmemekten daha kötü çünkü kapandı sanılır.

## Bağlam

Betik `ISD-RELAY-DONT-CALL` gereği kuruldu: taşıma yöneticinin işi olduğu
için agent'lar birbirinin kutusuna doğrudan yazmıyor, relay taşıyor.
Yani betik **kanal mimarisinin bir parçası**, geçici bir yardımcı değil —
düzeltme de o gözle yapılmalı.
