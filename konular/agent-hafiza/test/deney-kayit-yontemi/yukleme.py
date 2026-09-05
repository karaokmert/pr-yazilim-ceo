#!/usr/bin/env python3
"""
Kayıt yöntemi deneyi — 52 dosyalık korpusu 6 farklı yöntemle Qdrant'a yükler.

Koleksiyonlar (hepsi 1024 boyut, Cosine):
  y-dokuman         — dosya tek kayıt
  y-paragraf        — boş satırla ayrılmış bloklar
  y-paragraf-baslik — paragraf + "H1 › en yakın bölüm başlığı" öneki
  y-cumle           — cümle cümle
  y-parca           — sabit ~800 karakter pencere, 150 bindirme
  y-hukum           — hafiza-large'dan kopya (kaynak_adres filtreli, yeniden embed YOK)

DOKUNULMAZ: hafiza, hafiza-large (yalnız okunur), clara-1, clara-2, test-hafiza.

Kullanım:
  source ~/.zshenv
  python3 yukleme.py
"""

import os
import re
import sys
import time
import uuid
import json
import requests

# ---------------------------------------------------------------------------
# Ayarlar
# ---------------------------------------------------------------------------

QDRANT_URL = "https://rag.prventurestudio.com"
EMBED_URL = "https://embed.prventurestudio.com/v1/embeddings"
EMBED_MODEL = "intfloat/multilingual-e5-large"
VECTOR_SIZE = 1024

REPO_ROOT = "/Users/karaok/p/pr-yazilim-ceo"
KORPUS_LISTESI = os.path.join(
    REPO_ROOT, "konular/agent-hafiza/test/deney-kayit-yontemi/korpus.txt"
)

QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
EMBED_API_KEY = os.environ.get("EMBED_API_KEY")

if not QDRANT_API_KEY or not EMBED_API_KEY:
    print("HATA: QDRANT_API_KEY / EMBED_API_KEY yok. `source ~/.zshenv` çalıştırıldı mı?")
    sys.exit(1)

QDRANT_HEADERS = {"api-key": QDRANT_API_KEY, "Content-Type": "application/json"}
EMBED_HEADERS = {"Authorization": f"Bearer {EMBED_API_KEY}", "Content-Type": "application/json"}

# Dokunulmaz koleksiyonlar — bu isimler asla silinmez/yazılmaz (y-hukum sadece okur).
YASAKLI = {"hafiza", "hafiza-large", "clara-1", "clara-2", "test-hafiza"}

BATCH_SIZE = 32  # embed çağrısı batch büyüklüğü (TEI sunucusu maksimum 32 kabul ediyor)

# Kayıt istatistikleri (rapor için)
STATS = {}
TOPLAM_EMBED_SANIYE = 0.0
TOPLAM_EMBED_CAGRI = 0
UYARILAR = []


# ---------------------------------------------------------------------------
# Yardımcılar — Qdrant
# ---------------------------------------------------------------------------

def qdrant_get(path):
    r = requests.get(f"{QDRANT_URL}{path}", headers=QDRANT_HEADERS, timeout=30)
    return r

def qdrant_delete_collection(name):
    r = requests.delete(f"{QDRANT_URL}/collections/{name}", headers=QDRANT_HEADERS, timeout=30)
    return r

def qdrant_create_collection(name, size=VECTOR_SIZE, distance="Cosine"):
    body = {"vectors": {"size": size, "distance": distance}}
    r = requests.put(f"{QDRANT_URL}/collections/{name}", headers=QDRANT_HEADERS,
                      json=body, timeout=30)
    r.raise_for_status()
    return r.json()

def _retry_gecici_hata(fn, deneme=5, taban_bekleme=2.0):
    """Geçici sunucu hatalarında (502/503/504/bağlantı) exponential backoff ile tekrar dener."""
    son_hata = None
    for i in range(deneme):
        try:
            return fn()
        except RuntimeError as e:
            msg = str(e)
            if any(kod in msg for kod in ("502", "503", "504")) and i < deneme - 1:
                bekleme = taban_bekleme * (2 ** i)
                print(f"    geçici hata, {bekleme:.0f}sn sonra tekrar denenecek ({i+1}/{deneme}): {msg[:200]}")
                time.sleep(bekleme)
                son_hata = e
                continue
            raise
        except requests.exceptions.RequestException as e:
            if i < deneme - 1:
                bekleme = taban_bekleme * (2 ** i)
                print(f"    bağlantı hatası, {bekleme:.0f}sn sonra tekrar denenecek ({i+1}/{deneme}): {e}")
                time.sleep(bekleme)
                son_hata = e
                continue
            raise
    raise son_hata

def qdrant_upsert(name, points):
    """points: [{id, vector, payload}, ...]"""
    def _yap():
        body = {"points": points}
        r = requests.put(f"{QDRANT_URL}/collections/{name}/points?wait=true",
                          headers=QDRANT_HEADERS, json=body, timeout=120)
        if r.status_code >= 300:
            raise RuntimeError(f"upsert hata [{name}]: {r.status_code} {r.text[:500]}")
        return r
    r = _retry_gecici_hata(_yap)
    return r.json()

def qdrant_count(name):
    r = requests.post(f"{QDRANT_URL}/collections/{name}/points/count",
                       headers=QDRANT_HEADERS, json={"exact": True}, timeout=30)
    r.raise_for_status()
    return r.json()["result"]["count"]

def qdrant_scroll_all(name, with_vector=False, batch=100):
    """Bir koleksiyondaki tüm point'leri sayfalayarak döner."""
    points = []
    offset = None
    while True:
        body = {"limit": batch, "with_payload": True, "with_vector": with_vector}
        if offset is not None:
            body["offset"] = offset
        r = requests.post(f"{QDRANT_URL}/collections/{name}/points/scroll",
                           headers=QDRANT_HEADERS, json=body, timeout=60)
        r.raise_for_status()
        result = r.json()["result"]
        points.extend(result["points"])
        offset = result.get("next_page_offset")
        if offset is None:
            break
    return points

def ensure_collection(name):
    """y-* koleksiyonunu sil (varsa) ve yeniden oluştur. Yasaklı isimler asla dokunulmaz."""
    if name in YASAKLI:
        raise RuntimeError(f"YASAK: {name} koleksiyonuna dokunulamaz")
    if not name.startswith("y-"):
        raise RuntimeError(f"GÜVENLİK: yalnız y-* koleksiyonları silinip yeniden oluşturulur, '{name}' değil")
    r = qdrant_get(f"/collections/{name}")
    if r.status_code == 200:
        dr = qdrant_delete_collection(name)
        if dr.status_code >= 300:
            raise RuntimeError(f"silme hata [{name}]: {dr.status_code} {dr.text[:300]}")
    qdrant_create_collection(name)


# ---------------------------------------------------------------------------
# Yardımcılar — Embedding
# ---------------------------------------------------------------------------

def embed_batch(texts, is_query=False):
    """texts: liste. e5 kuralı: passage: / query: öneki DIŞARIDA eklenir (bu fonksiyon eklemez)."""
    global TOPLAM_EMBED_SANIYE, TOPLAM_EMBED_CAGRI

    def _yap():
        t0 = time.time()
        r = requests.post(EMBED_URL, headers=EMBED_HEADERS,
                           json={"input": texts, "model": EMBED_MODEL}, timeout=120)
        dt = time.time() - t0
        _sureyi_ekle(dt)
        if r.status_code >= 300:
            raise RuntimeError(f"embed hata: {r.status_code} {r.text[:500]}")
        return r

    r = _retry_gecici_hata(_yap)
    data = r.json()["data"]
    # Sıra korunur — TEI input sırasını korur.
    return [d["embedding"] for d in data]

def _sureyi_ekle(dt):
    global TOPLAM_EMBED_SANIYE, TOPLAM_EMBED_CAGRI
    TOPLAM_EMBED_SANIYE += dt
    TOPLAM_EMBED_CAGRI += 1

def embed_passages(texts):
    """Belge (passage) embed'i — e5 kuralı gereği 'passage: ' öneki eklenir."""
    prefixed = [f"passage: {t}" for t in texts]
    return embed_batch(prefixed)


def batched(iterable, n):
    buf = []
    for item in iterable:
        buf.append(item)
        if len(buf) >= n:
            yield buf
            buf = []
    if buf:
        yield buf


# ---------------------------------------------------------------------------
# Korpus okuma
# ---------------------------------------------------------------------------

def korpus_yollari():
    with open(KORPUS_LISTESI, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def dosya_oku(goreli_yol):
    tam_yol = os.path.join(REPO_ROOT, goreli_yol)
    with open(tam_yol, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Yöntem 1: y-dokuman — dosya tek kayıt
# ---------------------------------------------------------------------------

def yontem_dokuman(dosyalar):
    kayitlar = []  # (text, payload)
    for sira, (yol, icerik) in enumerate(dosyalar, start=1):
        kayitlar.append((icerik, {
            "content": icerik,
            "kaynak_adres": yol,
            "yontem": "y-dokuman",
            "sira": sira,
        }))
    return kayitlar


# ---------------------------------------------------------------------------
# Yöntem 2 & 3: paragraf bölme (ortak mantık) + başlık önekli varyant
# ---------------------------------------------------------------------------

BASLIK_RE = re.compile(r"^(#{1,6})\s+(.*)$")

def dosya_baslik_haritasi(icerik, dosya_adi_fallback):
    """
    Satır satır gezip: H1 başlığı ve her satır için 'en yakın üst bölüm başlığı'nı çıkarır.
    Döner: h1 (str), satir_no -> en_yakin_baslik (dict, sadece başlık satırları girilir;
    aralar için en yakın öncekini kullanmak çağıran tarafın işi).
    """
    lines = icerik.splitlines()
    h1 = None
    # (satir_index, seviye, metin) listesi
    basliklar = []
    for i, line in enumerate(lines):
        m = BASLIK_RE.match(line.strip())
        if m:
            seviye = len(m.group(1))
            metin = m.group(2).strip()
            basliklar.append((i, seviye, metin))
            if h1 is None and seviye == 1:
                h1 = metin
    if h1 is None:
        h1 = dosya_adi_fallback
    return h1, basliklar


def en_yakin_bolum_basligi(basliklar, satir_index, h1_metni):
    """
    satir_index'ten geriye bakarak en yakın seviye>=2 başlığı bulur.
    Yoksa None döner (bu durumda sadece H1 kullanılır).
    """
    en_yakin = None
    for (i, seviye, metin) in basliklar:
        if i <= satir_index and seviye >= 2:
            en_yakin = metin
        elif i > satir_index:
            break
    return en_yakin


def bloklara_ayir(icerik):
    """
    Boş satır(lar)la ayrılmış bloklar. Her blok (baslangic_satir, metin) olarak döner.
    '---' yatay çizgi satırları ayraç kabul edilir (blok içeriği değil, atlanır).
    """
    lines = icerik.splitlines()
    bloklar = []
    cur_lines = []
    cur_start = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "" or re.match(r"^-{3,}$", stripped):
            if cur_lines:
                bloklar.append((cur_start, "\n".join(cur_lines).strip()))
                cur_lines = []
                cur_start = None
            continue
        if cur_start is None:
            cur_start = i
        cur_lines.append(line)
    if cur_lines:
        bloklar.append((cur_start, "\n".join(cur_lines).strip()))
    return [(s, t) for (s, t) in bloklar if t]


def paragraf_birlestir(bloklar, min_uzunluk=40):
    """
    40 karakterden kısa blokları önceki bloğa yapıştırır.
    Markdown başlık satırı tek başına kayıt olmaz — takip eden bloğa eklenir.
    bloklar: [(satir_no, metin), ...]
    Döner: [(satir_no, metin), ...] birleştirilmiş.
    """
    if not bloklar:
        return []

    # Önce: salt başlık olan blokları takip eden bloğa yapıştır (ileri birleşim).
    merged_forward = []
    i = 0
    while i < len(bloklar):
        satir_no, metin = bloklar[i]
        # Blok sadece başlık satır(lar)ından mı oluşuyor?
        tum_satirlar_baslik = all(
            BASLIK_RE.match(l.strip()) or l.strip() == ""
            for l in metin.splitlines()
        )
        if tum_satirlar_baslik and i + 1 < len(bloklar):
            next_satir_no, next_metin = bloklar[i + 1]
            birlesik = metin + "\n" + next_metin
            merged_forward.append((satir_no, birlesik))
            i += 2
        else:
            merged_forward.append((satir_no, metin))
            i += 1

    # Sonra: kısa (< min_uzunluk) blokları öncekine yapıştır (geri birleşim).
    sonuc = []
    for satir_no, metin in merged_forward:
        if sonuc and len(metin) < min_uzunluk:
            prev_satir_no, prev_metin = sonuc[-1]
            sonuc[-1] = (prev_satir_no, prev_metin + "\n\n" + metin)
        else:
            sonuc.append((satir_no, metin))

    # Kenar durum: ilk blok kendisi kısaysa ve sonrasında blok varsa, sonrakiyle birleştir.
    if len(sonuc) >= 2 and len(sonuc[0][1]) < min_uzunluk:
        satir_no0, metin0 = sonuc[0]
        satir_no1, metin1 = sonuc[1]
        sonuc = [(satir_no0, metin0 + "\n\n" + metin1)] + sonuc[2:]

    return sonuc


def yontem_paragraf(dosyalar):
    kayitlar = []
    for yol, icerik in dosyalar:
        bloklar = bloklara_ayir(icerik)
        birlesik = paragraf_birlestir(bloklar)
        for sira, (satir_no, metin) in enumerate(birlesik, start=1):
            kayitlar.append((metin, {
                "content": metin,
                "kaynak_adres": yol,
                "yontem": "y-paragraf",
                "sira": sira,
            }))
    return kayitlar


def yontem_paragraf_baslik(dosyalar):
    kayitlar = []
    for yol, icerik in dosyalar:
        dosya_adi = os.path.splitext(os.path.basename(yol))[0]
        h1, basliklar = dosya_baslik_haritasi(icerik, dosya_adi_fallback=dosya_adi)
        bloklar = bloklara_ayir(icerik)
        birlesik = paragraf_birlestir(bloklar)
        for sira, (satir_no, metin) in enumerate(birlesik, start=1):
            bolum = en_yakin_bolum_basligi(basliklar, satir_no, h1)
            if bolum and bolum != h1:
                onek = f"{h1} › {bolum}: "
            else:
                onek = f"{h1}: "
            metin_with_onek = onek + metin
            kayitlar.append((metin_with_onek, {
                "content": metin_with_onek,
                "kaynak_adres": yol,
                "yontem": "y-paragraf-baslik",
                "sira": sira,
            }))
    return kayitlar


# ---------------------------------------------------------------------------
# Yöntem 4: y-cumle — cümle cümle
# ---------------------------------------------------------------------------

MADDE_RE = re.compile(r"^\s*([-*+]|\d+[.)])\s+")
CUMLE_SONU_RE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ0-9\"'(])")

def satiri_cumlelere_ayir(satir):
    """Madde imli satır -> satır başına bir kayıt (bölünmez). Düz satır -> cümle cümle böl."""
    stripped = satir.strip()
    if not stripped:
        return []
    if MADDE_RE.match(stripped):
        return [stripped]
    if BASLIK_RE.match(stripped):
        return [stripped]
    if re.match(r"^-{3,}$", stripped):
        return []
    parcalar = CUMLE_SONU_RE.split(stripped)
    return [p.strip() for p in parcalar if p.strip()]


def cumleleri_birlestir(cumleler, min_uzunluk=25):
    """25 karakterden kısa cümleleri komşusuyla (sonrakiyle, yoksa öncekiyle) birleştir."""
    if not cumleler:
        return []
    sonuc = list(cumleler)
    i = 0
    while i < len(sonuc):
        if len(sonuc[i]) < min_uzunluk:
            if i + 1 < len(sonuc):
                sonuc[i] = sonuc[i] + " " + sonuc[i + 1]
                del sonuc[i + 1]
                # tekrar kontrol et (yeni birleşim yine kısa olabilir), i'de kal
                continue
            elif i - 1 >= 0:
                sonuc[i - 1] = sonuc[i - 1] + " " + sonuc[i]
                del sonuc[i]
                i -= 1
                continue
        i += 1
    return sonuc


def yontem_cumle(dosyalar):
    kayitlar = []
    for yol, icerik in dosyalar:
        satirlar = icerik.splitlines()
        tum_cumleler = []
        for satir in satirlar:
            tum_cumleler.extend(satiri_cumlelere_ayir(satir))
        birlesik = cumleleri_birlestir(tum_cumleler)
        for sira, cumle in enumerate(birlesik, start=1):
            kayitlar.append((cumle, {
                "content": cumle,
                "kaynak_adres": yol,
                "yontem": "y-cumle",
                "sira": sira,
            }))
    return kayitlar


# ---------------------------------------------------------------------------
# Yöntem 5: y-parca — sabit pencere ~800 karakter, 150 bindirme
# ---------------------------------------------------------------------------

def en_yakin_bosluktan_kes(metin, hedef_index, arama_penceresi=60):
    """hedef_index civarında (± arama_penceresi) en yakın boşluğu bulur, kesim noktasını döner."""
    n = len(metin)
    if hedef_index >= n:
        return n
    # Sağa doğru ara
    for offset in range(0, arama_penceresi + 1):
        idx = hedef_index + offset
        if idx < n and metin[idx].isspace():
            return idx
        idx = hedef_index - offset
        if idx > 0 and metin[idx].isspace():
            return idx
    return hedef_index  # bulunamazsa olduğu gibi kes


def parcala(metin, pencere=800, bindirme=150):
    n = len(metin)
    if n <= pencere:
        return [metin.strip()] if metin.strip() else []
    parcalar = []
    start = 0
    while start < n:
        hedef_end = min(start + pencere, n)
        if hedef_end < n:
            kesim = en_yakin_bosluktan_kes(metin, hedef_end)
        else:
            kesim = hedef_end
        parca = metin[start:kesim].strip()
        if parca:
            parcalar.append(parca)
        if kesim >= n:
            break
        yeni_start = kesim - bindirme
        # en yakın boşluktan başlat (kelime ortasından başlamamak için)
        if yeni_start > start:
            yeni_start = en_yakin_bosluktan_kes(metin, yeni_start)
        if yeni_start <= start:
            yeni_start = kesim  # ilerlemiyor gibiyse döngü kırılmasın
        start = yeni_start
    return parcalar


def yontem_parca(dosyalar):
    kayitlar = []
    for yol, icerik in dosyalar:
        parcalar = parcala(icerik)
        for sira, parca in enumerate(parcalar, start=1):
            kayitlar.append((parca, {
                "content": parca,
                "kaynak_adres": yol,
                "yontem": "y-parca",
                "sira": sira,
            }))
    return kayitlar


# ---------------------------------------------------------------------------
# Yöntem 6: y-hukum — hafiza-large'dan kopya (yeniden embed YOK)
# ---------------------------------------------------------------------------

def yontem_hukum(korpus_setleri):
    """
    hafiza-large'dan tüm point'leri (vektör dahil) çeker, payload.metadata.kaynak_adres
    korpus.txt'teki 52 yoldan biri olanları aynen y-hukum'a upsert eder.
    Döner: (upsert_edilen_point_sayisi, toplam_tarama_sayisi)
    """
    print("  hafiza-large'dan scroll ile point çekiliyor (with_vector=true)...")
    tum_pointler = qdrant_scroll_all("hafiza-large", with_vector=True)
    print(f"  hafiza-large toplam point: {len(tum_pointler)}")

    gecen_pointler = []
    for p in tum_pointler:
        payload = p.get("payload", {})
        metadata = payload.get("metadata", {})
        kaynak = metadata.get("kaynak_adres")
        if kaynak in korpus_setleri:
            gecen_pointler.append({
                "id": p["id"],
                "vector": p["vector"],
                "payload": payload,  # aynen kopyalanır
            })

    ensure_collection("y-hukum")
    for batch in batched(gecen_pointler, 100):
        qdrant_upsert("y-hukum", batch)

    return len(gecen_pointler), len(tum_pointler)


# ---------------------------------------------------------------------------
# Genel yükleme akışı (embed gerektiren 5 yöntem için ortak)
# ---------------------------------------------------------------------------

def deterministik_id(yontem, kaynak_adres, sira):
    ad = f"{yontem}:{kaynak_adres}:{sira}"
    return str(uuid.uuid5(uuid.NAMESPACE_URL, ad))


def yukle_ve_embedle(koleksiyon_adi, kayitlar):
    """
    kayitlar: [(text, payload), ...]
    Embed edip Qdrant'a batch batch upsert eder.
    """
    ensure_collection(koleksiyon_adi)
    toplam = len(kayitlar)
    if toplam == 0:
        UYARILAR.append(f"{koleksiyon_adi}: hiç kayıt üretilmedi")
        return 0

    yuklenen = 0
    for batch in batched(kayitlar, BATCH_SIZE):
        texts = [t for (t, _) in batch]
        vektorler = embed_passages(texts)
        points = []
        for (text, payload), vec in zip(batch, vektorler):
            pid = deterministik_id(koleksiyon_adi, payload["kaynak_adres"], payload["sira"])
            points.append({"id": pid, "vector": vec, "payload": payload})
        qdrant_upsert(koleksiyon_adi, points)
        yuklenen += len(points)
        print(f"    {koleksiyon_adi}: {yuklenen}/{toplam} yüklendi")
    return yuklenen


# ---------------------------------------------------------------------------
# Ana akış
# ---------------------------------------------------------------------------

def main():
    print("=== Korpus okunuyor ===")
    yollar = korpus_yollari()
    print(f"korpus.txt: {len(yollar)} yol")

    dosyalar = []
    for yol in yollar:
        try:
            icerik = dosya_oku(yol)
            dosyalar.append((yol, icerik))
        except Exception as e:
            UYARILAR.append(f"okunamadı: {yol} — {e}")
    print(f"okunan dosya: {len(dosyalar)}")

    korpus_seti = set(yollar)

    yontemler = [
        ("y-dokuman", yontem_dokuman),
        ("y-paragraf", yontem_paragraf),
        ("y-paragraf-baslik", yontem_paragraf_baslik),
        ("y-cumle", yontem_cumle),
        ("y-parca", yontem_parca),
    ]

    for isim, fn in yontemler:
        print(f"\n=== {isim} ===")
        kayitlar = fn(dosyalar)
        print(f"  üretilen kayıt sayısı: {len(kayitlar)}")
        yuklenen = yukle_ve_embedle(isim, kayitlar)
        dogrulama = qdrant_count(isim)
        STATS[isim] = {
            "uretilen": len(kayitlar),
            "yuklenen": yuklenen,
            "qdrant_count": dogrulama,
        }
        if dogrulama != len(kayitlar):
            UYARILAR.append(
                f"{isim}: üretilen={len(kayitlar)} ama qdrant count={dogrulama}"
            )

    print("\n=== y-hukum ===")
    gecen, toplam_tarama = yontem_hukum(korpus_seti)
    dogrulama = qdrant_count("y-hukum")
    STATS["y-hukum"] = {
        "uretilen": gecen,
        "yuklenen": gecen,
        "qdrant_count": dogrulama,
        "toplam_hafiza_large_point": toplam_tarama,
    }
    if dogrulama != gecen:
        UYARILAR.append(f"y-hukum: filtreden geçen={gecen} ama qdrant count={dogrulama}")

    # ---------------------------------------------------------------
    # Rapor
    # ---------------------------------------------------------------
    print("\n\n========== RAPOR ==========")
    print(f"Toplam embed API çağrısı: {TOPLAM_EMBED_CAGRI}")
    print(f"Toplam embed süresi: {TOPLAM_EMBED_SANIYE:.2f} saniye")
    print()
    for isim, s in STATS.items():
        print(f"{isim}: {json.dumps(s, ensure_ascii=False)}")
    print()
    if UYARILAR:
        print("UYARILAR:")
        for u in UYARILAR:
            print(f"  - {u}")
    else:
        print("Uyarı yok.")

    # Rapor dosyasına da yaz
    rapor_path = os.path.join(
        REPO_ROOT, "konular/agent-hafiza/test/deney-kayit-yontemi/yukleme-sonuc.json"
    )
    with open(rapor_path, "w", encoding="utf-8") as f:
        json.dump({
            "toplam_embed_cagri": TOPLAM_EMBED_CAGRI,
            "toplam_embed_saniye": TOPLAM_EMBED_SANIYE,
            "istatistikler": STATS,
            "uyarilar": UYARILAR,
        }, f, ensure_ascii=False, indent=2)
    print(f"\nSonuç dosyası: {rapor_path}")


if __name__ == "__main__":
    main()
