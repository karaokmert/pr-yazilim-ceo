# Fabrika `skill-project`'e taşındı — adresler ve kanal varsayılanı

**Tarih:** 2026-08-11 · **Karar:** Mert · **Durum:** kapalı

## Karar

Fabrika işleri artık **`/Users/karaok/p/ozel-yazilim/skill-project`** altında yürür.
`agent-project` referans repo oldu: okunur, yazılmaz, kanonu yürürlükte değil.

Mert'in cümlesi: *"artık fabrika işlerimiz skill projectte çalışacak bu nedenle oraya
taşınmalıyız."* Ve repo hakkında: *"repoyu silmiyoruz ki, zaten bir şey lazım olursa
burdan bakarız."*

## Neden bu bir adres kararından fazlası

Taşıma 2026-08-10'da yapıldı ama bir **kopyalama**ydı: `.claude/` (89 dosya),
`docs/` (88), `team/` (32) iki repoda da duruyor ve hash bazında özdeş. Yani iki canlı
kanon vardı ve hangisinin yürürlükte olduğu hiçbir dosyadan okunamıyordu.

`skill-project/CLAUDE.md` §3'e yazılı olan arızanın repo ölçeğindeki hâli: **ayıran şey
içerik değil statü.** İki özdeş kopyadan hangisinin doğru olduğunu içerik söylemiyor.

## Ne yapıldı

**`agent-project` kapatıldı** (`b89c93a`):
- `CLAUDE.md`'nin **en başına** uyarı bloğu — 229 satırın ortasına konan uyarı okunmaz
- **Açılış hook tetiği kaldırıldı** (`.claude/settings.json` → `hooks` anahtarı yok).
  Betik (`acilis-preload.sh`) diskte duruyor, okunabilir, **koşmaz.** Sebep: orada
  açılan bir agent dünün kanonunu preload etmesin. Bağlamsız bırakmak değil — doğru
  bağlamı vermek; aldığı liste zaten dünün listesi olurdu.

**Adresler düzeltildi:**
- `pr-yazilim-ceo/CLAUDE.md` → "Bakılan yerler" bölümünde iki reponun rolü çevrildi
- Clara body'si → dört yer (`agent-project` → `skill-project`)
- Dört skill description'ı → kapsam-dışı satırlarındaki fabrika adresi

**Düzeltilmeyen — bilinçli:** `references/olcumler.md` dosyalarındaki `agent-project`
satırları. Ayıran soru: satır bir **yer** mi gösteriyor, bir **olay** mı anlatıyor?
Ölçüm kaydı bir tarihtir; düzeltilirse kanıt bozulur.

## Kanal varsayılanı — sebep düzeltildi, tam kaldırılmadı

`setup.py:22` varsayılanı `agent-project`'ti. `--project` yazılmazsa kutu oraya düşer,
`rc=0` döner, arıza görünmez. Skill'de bunu kapatan bir *"her zaman yazılır"* kuralı
vardı — `CLA-FIX-THE-CAUSE`'a göre **yama**: karıştıran şey duruyor, üstüne kontrol
konmuş.

Clara varsayılanı **kaldırmayı** önerdi (verilmezse betik durur → unutmak imkânsız).
Mert varsayılanın kalmasını, ama **uyarı basmasını** seçti:

```python
PROJE = opt("--project", None)
if not PROJE:
    PROJE = "skill-project"
    print(f"UYARI: --project verilmedi, varsayilan kullaniliyor: {PROJE}", file=sys.stderr)
```

**Gerekçe:** kolaylık korunur (çoğu kanal fabrikada kurulacak), sessizlik gider. Yanlış
projede kurulursa satır ekranda durur.

**Kalan risk yazılı:** uyarı `stderr`'e düşer ve okunmayabilir. O yüzden skill'deki
*"`--project` her zaman yazılır"* kuralı **durmaya devam ediyor** — kaldırılmadı.

**Tek kaynak kuruldu:** `skill-project/tools/kanal/` (beş betik). Ölçüldü — betiklerin
kaynağı **yoktu**, yalnız `~/.pr-kanal/` altında iki özdeş kopya vardı. Kaynağı
olmayan bir betik kopyalanarak çoğalır ve arıza kendini yeniden üretir. Kural:
düzeltme **önce kaynağa**, sonra kopyalara.

Üç kopya doğrulandı, aynı hash (`1fd18269a09c38cf9806f40c210d6478`).

## Ölçümle doğrulanan

- `--project` verilince: `stderr` boş (uyarı yok) ✓
- `--project` verilmeyince: `UYARI: ... skill-project` ✓
- Üç kopya aynı hash ✓
- `settings.json` geçerli JSON, `hooks` anahtarı yok ✓

Test iki kutu artığı bıraktı (`deneme-XYZ`, `skill-project/test-rol2-...`) — Clara'nın
`rm -rf` izni yok, silme Mert'e bırakıldı.

## Ne ölçülmedi

**Emekli skill ailesi.** `skill-project/.claude/skills/` altında iki aile yan yana ve
hangi hükmün hangisinde yürürlükte olduğu ölçülmedi. `CLAUDE.md` §5'e **risk olarak**
yazıldı, envanter olarak değil — ad taraması eşlemeyi vermiyor, yalnız okuma veriyor.
