#!/usr/bin/env python3
"""SessionStart — kanal kurulum talimatini KOSULLU olarak enjekte eder.

NEDEN VAR
Kanal protokolu (yildiz topoloji, inbox/outbox, bes betik) fabrika
kanonunda TAM (skill-project: is-duzeni/SKILL.md + references/kanal.md),
ama OY ve Websitesi agentlarinin kanonunda HIC YOK — olculdu 2026-08-11:
plugin cache'inde 'pr-kanal|inbox|outbox' icin sifir eslesme.

Bu bosluk bugune kadar elle kapatiliyordu: Clara her agent icin handoff
yazip adresi veriyordu. Yama, cunku Clara yazmayi atlarsa agent kanali
aramayi bile bilmiyor. Bu hook sebebi kaldirir.

NEDEN PLUGIN'E YAZILMADI
Kanal IKI UCLU: kutu acan uc + okuyan merkez. Merkez = Clara, ve Clara
plugin'e girmiyor (Mert'in karari, 2026-08-11: "Clara bana ozel kalacak").
Plugin'e yazilsa, plugin'i alan kisinin agentlari her acilista kutu acar,
izleyici kurar, "kuruldum" yazar -- ve okuyacak MERKEZ olmaz. Sonuc
kanonun en kotu hali: "calistigi sanilan monitor". O yuzden burada,
kullanici seviyesinde yasar. Plugin guncellemesi bunu ezmez (iki
mekanizma bagimsiz; olculdu -- global git satiri + proje hooku ayni
oturumda birden calisti).

MATCHER TUZAGI -- FILTRE BURADA, settings.json'DA DEGIL
SessionStart matcher'i oturumun NASIL basladigini esler (startup/resume/
clear/compact/fork), agent adini DEGIL. Agent-tipi matcher yalniz
SubagentStart/Stop'ta var. settings.json'a agent adi yazilirsa hicbir
degerle eslesmez ve hook SESSIZCE HIC CALISMAZ. Ayni ders plugin'in
preload-skills.py'sinde yazili.

IKI KAPI -- biri kapanirsa SESSIZ cikis (kod 0, cikti yok)
  1. Clara mi?     -> EVET ise cik. Clara merkezdir; kanali ise gore kurar,
                      acilista kurmaz (bos kutu uretir).
  2. Kutum var mi? -> Bu rol icin acik kutu varsa KURMA, adresi hatirlat.
                      Ayni oturumda ikinci kutu acilmasin.

MERKEZ KAPISI NEDEN YOK -- Mert'in karari, 2026-08-11
Uc ayri olcut denendi ve ucu de curudu: STATE: OPEN canlilik degil sadece
"arsivlenmedi" (Goat'ta sekiz olu kutu OPEN gorundu) · `ps` canliligi verir
ama PROJEYI vermez (her Clara oturumunun cwd'si pr-yazilim-ceo -- onu
baslatan `cd`) · zaman esigi kanonun "uydurulmaz" dedigi sey.

Ucuncu olcut degisiminde asil soru soruldu: merkez kapisi GEREKLI MI?
Degil. Kanal ASENKRON -- agent kendi outbox'ina yazar, mesaj diske duser,
imlec kimin ne okudugunu tutar. Merkez uc saat sonra gelse hicbir mesaj
kaybolmaz. "Merkez yoksa kanal anlamsiz" varsayimi kanali senkron sanmakti.
Kanon ilkesi: "gurultu zararsiz, kayip zararli."

Karar ve gerekce: pr-yazilim-ceo/kararlar/2026-08-11-kanal-acilis-hooku.md
"""
import json
import os
import sys
from pathlib import Path

KANAL_KOK = Path.home() / ".pr-kanal"
ARAC_YOLU = Path("/Users/karaok/p/ozel-yazilim/skill-project/tools/kanal")


def sessiz_cik():
    """Cikti yok, kod 0. Hook calisti ama hicbir sey enjekte etmedi."""
    sys.exit(0)


def bas(metin: str):
    """SessionStart additionalContext olarak enjekte eder."""
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": metin,
        }
    }))
    sys.exit(0)


def acik_kutular(proje_dizini: Path) -> list[Path]:
    """STATE: OPEN olan kutular. STATUS.md yoksa kutu sayilmaz."""
    bulunan = []
    if not proje_dizini.is_dir():
        return bulunan
    for kutu in sorted(proje_dizini.iterdir()):
        if not kutu.is_dir() or kutu.name in ("tools", "archive", ".claude"):
            continue
        status = kutu / "STATUS.md"
        if not status.is_file():
            continue
        try:
            if "STATE: OPEN" in status.read_text(encoding="utf-8"):
                bulunan.append(kutu)
        except OSError:
            continue
    return bulunan


def main():
    # --- girdi: cwd stdin'den gelir; env'e guvenilmez ---
    try:
        veri = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sessiz_cik()

    cwd = veri.get("cwd") or ""
    # cwd GERCEKTEN bir dizin olmali. Olculdu 2026-08-11: kontrol yokken
    # cwd=/yok girdisi "--project yok" talimati uretti (2088 karakter).
    # Ev dizini/tmp'de acilan agent sacma bir proje adiyla kutu kurar,
    # ariza sessiz olur.
    if not cwd or not Path(cwd).is_dir():
        sessiz_cik()

    proje = Path(cwd).name

    # agent adi: stdin once (plugin bunu boyle cozuyor), env yedek
    rol = (veri.get("agent_type")
           or os.environ.get("CLAUDE_CODE_AGENT")
           or "")
    if not rol:
        sessiz_cik()

    # Plugin agentlari "ozel-yazilim:backend-developer" seklinde gelir.
    # Iki nokta dizin adinda tasinmaz -- namespace atilir, rol kalir.
    rol = rol.split(":")[-1]

    # --- KAPI 1: Clara merkezdir, kendi hooku var ---
    if rol == "clara":
        sessiz_cik()

    # Merkez kapisi YOK (bkz. modul docstring) -- kanal asenkron, mesaj
    # okunmasa da kaybolmaz. Kutular yalniz KAPI 2 icin taranir.
    proje_dizini = KANAL_KOK / proje
    kutular = acik_kutular(proje_dizini)

    # --- KAPI 2: bu rolun kutusu zaten var mi? ---
    benim = [k for k in kutular if k.name.startswith(f"{rol}-")]
    if benim:
        bas(
            f"[KANAL — kutun ZATEN VAR, yeniden kurma]\n"
            f"  KUTU  : {benim[-1]}\n"
            f"  MERKEZ: clara (merkez kutusu acilmamis olabilir — mesajin\n"
            f"          outbox'ta bekler, imlecle okunur, kaybolmaz)\n"
            f"  ARAC  : {ARAC_YOLU}\n\n"
            f"Izleyicin oturumla birlikte OLMUSTUR — monitor yeniden kurulur:\n"
            f"  Monitor araci ile (Bash DEGIL — bildirim uretmez):\n"
            f"  python3 {ARAC_YOLU}/watch.py {benim[-1]}/inbox 2>&1 \\\n"
            f"    | grep -E --line-buffered 'from=|ERROR:|INFO:|watcher started'\n\n"
            f"Sonra imlecten okumayi yap:\n"
            f"  python3 {ARAC_YOLU}/read.py {benim[-1]}/inbox"
        )

    # --- IKISI DE GECTI: kurulum talimati ---
    bas(
        f"[KANAL — kutunu KUR, sonra bekle]\n"
        f"  PROJE : {proje}\n"
        f"  MERKEZ: clara\n"
        f"  ARAC  : {ARAC_YOLU}\n\n"
        f"Bu bir ALTYAPI isi — uretim isine baslamadan once yapilir.\n"
        f"Dort adim, sirasi atlanmaz:\n\n"
        f"1) KUTUNU KUR (elle mkdir YOK — betik kurar):\n"
        f"   python3 {ARAC_YOLU}/setup.py {rol} \\\n"
        f"     --task \"<tek satir is tarifi>\" --project {proje}\n"
        f"   `--project` ZORUNLU. Atlanirsa varsayilan kullanilir ve kutun\n"
        f"   YANLIS projeye dusler; rc=0 alirsin, fark etmezsin.\n"
        f"   setup.py kalan komutlari MUTLAK yollarla ekrana basar — onlari kullan.\n\n"
        f"2) IZLEYICINI KUR — `Monitor` ARACI ile, `Bash` ile DEGIL.\n"
        f"   Bash(run_in_background) surec calistirir ama BILDIRIM URETMEZ;\n"
        f"   canli gorunur, kimse uyanmaz. `tail -F` de kullanilmaz —\n"
        f"   bos dizinde hic baslamaz, dolu dizinde sonrakini gormez.\n"
        f"   Once: ToolSearch(\"select:Monitor,TaskOutput\")\n"
        f"   IKISI DE gelmezse monitor KURMA, merkeze bildir.\n\n"
        f"3) CANLILIGI DOGRULA: TaskOutput(<id>, block:false) -> running\n"
        f"   `TaskList` DEGIL — o baska defter, bos doner.\n\n"
        f"4) MERKEZE HABER VER (kutu yolu setup.py ciktisinda):\n"
        f"   python3 {ARAC_YOLU}/send.py <KUTUN>/outbox {rol} clara \\\n"
        f"     INFO \"kuruldum, izleyici canli\"\n\n"
        f"YAPININ OZU:\n"
        f"  · inbox : merkez yazar, sen OKURSUN\n"
        f"  · outbox: sen yazarsin, merkez OKUR\n"
        f"  · Baska hicbir kutuya dokunmazsin. Agent->agent YOK.\n\n"
        f"YAZMA: `send.py` kullan. `printf` YASAK — cikis kodu 0 verip bozuk\n"
        f"  JSON uretir, ariza okuyan tarafta patlar. Uzun govde `--stdin`.\n"
        f"  Mutlak yol zorunlu. type: TASK|INFO|QUESTION|CLOSE.\n\n"
        f"OKUMA: bildirim gelince imlecten SONRASININ TAMAMINI oku — son\n"
        f"  dosyayi degil; bir bildirim birden fazla mesaj tasiyabilir.\n"
        f"  `read.py` rc=2 verirse DURMUSTUR, okumamistir — `&&` ile zincirleme.\n\n"
        f"KAPANIS: outbox'a CLOSE yaz, sonra BEKLE. Kutunu kendin arsivleme.\n\n"
        f"Kurulum bitince BEKLE — merkez sana is yazacak."
    )


if __name__ == "__main__":
    main()
