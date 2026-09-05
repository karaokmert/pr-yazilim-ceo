#!/usr/bin/env python3
"""
Kayıt yöntemi deneyi — koşum.

164 soruyu 6 Qdrant koleksiyonuna (y-dokuman, y-paragraf, y-paragraf-baslik,
y-cumle, y-parca, y-hukum) karşı çalıştırır, ham sonuçları kaydeder.

SADECE ARAMA yapılır — hiçbir koleksiyona yazılmaz.

Kullanım:
  source ~/.zshenv
  python3 kosum.py
"""

import os
import sys
import time
import json
import requests

# ---------------------------------------------------------------------------
# Ayarlar
# ---------------------------------------------------------------------------

QDRANT_URL = "https://rag.prventurestudio.com"
EMBED_URL = "https://embed.prventurestudio.com/v1/embeddings"
EMBED_MODEL = "intfloat/multilingual-e5-large"

REPO_ROOT = "/Users/karaok/p/pr-yazilim-ceo"
DENEY_DIR = os.path.join(REPO_ROOT, "konular/agent-hafiza/test/deney-kayit-yontemi")
SORULAR_PATH = os.path.join(DENEY_DIR, "sorular.jsonl")
SONUC_PATH = os.path.join(DENEY_DIR, "kosum-sonuc.json")

QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
EMBED_API_KEY = os.environ.get("EMBED_API_KEY")

if not QDRANT_API_KEY or not EMBED_API_KEY:
    print("HATA: QDRANT_API_KEY / EMBED_API_KEY yok. `source ~/.zshenv` çalıştırıldı mı?")
    sys.exit(1)

QDRANT_HEADERS = {"api-key": QDRANT_API_KEY, "Content-Type": "application/json"}
EMBED_HEADERS = {"Authorization": f"Bearer {EMBED_API_KEY}", "Content-Type": "application/json"}

KOLEKSIYONLAR = ["y-dokuman", "y-paragraf", "y-paragraf-baslik", "y-cumle", "y-parca", "y-hukum"]
BATCH_SIZE = 32
SEARCH_LIMIT = 10


# ---------------------------------------------------------------------------
# Retry — yukleme.py'deki örnekle aynı disiplin
# ---------------------------------------------------------------------------

def _retry_gecici_hata(fn, deneme=5, taban_bekleme=2.0):
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


# ---------------------------------------------------------------------------
# Embedding
# ---------------------------------------------------------------------------

def embed_batch(texts):
    def _yap():
        r = requests.post(EMBED_URL, headers=EMBED_HEADERS,
                           json={"input": texts, "model": EMBED_MODEL}, timeout=120)
        if r.status_code >= 300:
            raise RuntimeError(f"embed hata: {r.status_code} {r.text[:500]}")
        return r
    r = _retry_gecici_hata(_yap)
    data = r.json()["data"]
    return [d["embedding"] for d in data]


def batched(iterable, n):
    buf = []
    for item in iterable:
        buf.append(item)
        if len(buf) >= n:
            yield buf
            buf = []
    if buf:
        yield buf


def embed_sorular(sorular):
    """query: önekiyle, 32'lik batch'lerle, sıra korunarak embed eder."""
    tum_vektorler = []
    metinler = [f"query: {s['soru']}" for s in sorular]
    toplam = len(metinler)
    islenen = 0
    for batch in batched(metinler, BATCH_SIZE):
        vektorler = embed_batch(batch)
        tum_vektorler.extend(vektorler)
        islenen += len(batch)
        print(f"  embed: {islenen}/{toplam}")
    return tum_vektorler


# ---------------------------------------------------------------------------
# Qdrant arama
# ---------------------------------------------------------------------------

def qdrant_search(koleksiyon, vector, limit=SEARCH_LIMIT):
    def _yap():
        body = {"vector": vector, "limit": limit, "with_payload": True}
        r = requests.post(f"{QDRANT_URL}/collections/{koleksiyon}/points/search",
                           headers=QDRANT_HEADERS, json=body, timeout=60)
        if r.status_code >= 300:
            raise RuntimeError(f"search hata [{koleksiyon}]: {r.status_code} {r.text[:500]}")
        return r
    r = _retry_gecici_hata(_yap)
    return r.json()["result"]


def qdrant_count(koleksiyon):
    r = requests.post(f"{QDRANT_URL}/collections/{koleksiyon}/points/count",
                       headers=QDRANT_HEADERS, json={"exact": True}, timeout=30)
    r.raise_for_status()
    return r.json()["result"]["count"]


def kaynak_adres_al(payload):
    """y-hukum'da metadata.kaynak_adres, diğerlerinde kaynak_adres — ikisini de kontrol eden tek yardımcı."""
    if not payload:
        return None
    if "kaynak_adres" in payload:
        return payload["kaynak_adres"]
    metadata = payload.get("metadata")
    if metadata and "kaynak_adres" in metadata:
        return metadata["kaynak_adres"]
    return None


def icerik_al(payload):
    """Maliyet ölçümü için kayıt içeriğinin karakter hacmini almak üzere content alanını çeker."""
    if not payload:
        return ""
    if "content" in payload:
        return payload["content"] or ""
    metadata = payload.get("metadata")
    if metadata and "content" in metadata:
        return metadata["content"] or ""
    return ""


# ---------------------------------------------------------------------------
# Ana akış
# ---------------------------------------------------------------------------

def main():
    print("=== Sorular okunuyor ===")
    sorular = []
    with open(SORULAR_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                sorular.append(json.loads(line))
    print(f"soru sayısı: {len(sorular)}")

    print("\n=== Soru embed'leri alınıyor (query: önekiyle) ===")
    t0 = time.time()
    vektorler = embed_sorular(sorular)
    print(f"embed süresi: {time.time()-t0:.1f}sn")
    assert len(vektorler) == len(sorular)

    print("\n=== Koleksiyon kayıt sayıları ===")
    koleksiyon_count = {}
    for k in KOLEKSIYONLAR:
        c = qdrant_count(k)
        koleksiyon_count[k] = c
        print(f"  {k}: {c}")

    print("\n=== Arama koşumu ===")
    sonuclar = []  # her biri bir soru×koleksiyon kaydı
    toplam_arama = len(sorular) * len(KOLEKSIYONLAR)
    yapilan = 0
    t0 = time.time()
    for soru_idx, (soru, vec) in enumerate(zip(sorular, vektorler)):
        for koleksiyon in KOLEKSIYONLAR:
            hits = qdrant_search(koleksiyon, vec, limit=SEARCH_LIMIT)
            ilk5 = hits[:5]
            hit_listesi = []
            for sira, h in enumerate(hits, start=1):
                payload = h.get("payload", {})
                hit_listesi.append({
                    "sira": sira,
                    "skor": h.get("score"),
                    "kaynak_adres": kaynak_adres_al(payload),
                })
            ilk5_toplam_karakter = sum(len(icerik_al(h.get("payload", {}))) for h in ilk5)
            sonuclar.append({
                "soru_idx": soru_idx,
                "soru": soru["soru"],
                "beklenen_dosya": soru.get("beklenen_dosya"),
                "tip": soru.get("tip"),
                "koleksiyon": koleksiyon,
                "hits": hit_listesi,
                "ilk5_toplam_karakter": ilk5_toplam_karakter,
            })
            yapilan += 1
        if (soru_idx + 1) % 20 == 0 or soru_idx == len(sorular) - 1:
            gecen = time.time() - t0
            print(f"  {soru_idx+1}/{len(sorular)} soru işlendi ({yapilan}/{toplam_arama} arama, {gecen:.0f}sn)")

    print(f"\nToplam arama: {yapilan}, süre: {time.time()-t0:.1f}sn")

    cikti = {
        "soru_sayisi": len(sorular),
        "koleksiyonlar": KOLEKSIYONLAR,
        "koleksiyon_count": koleksiyon_count,
        "search_limit": SEARCH_LIMIT,
        "sonuclar": sonuclar,
    }
    with open(SONUC_PATH, "w", encoding="utf-8") as f:
        json.dump(cikti, f, ensure_ascii=False, indent=2)
    print(f"\nHam sonuç dosyası: {SONUC_PATH}")


if __name__ == "__main__":
    main()
