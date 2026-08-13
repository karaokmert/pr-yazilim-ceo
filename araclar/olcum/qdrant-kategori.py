"""D bicimi: anlam birimi + KATEGORI (metadata).

Gorev #1. B bicimine (8/10) metadata eklenir ve ayni 10 soruyla olculur.
Soru: kategori isabeti ARTIRIYOR mu, yoksa yalnizca filtre icin mi ise yariyor?

Iki alt-varyant olculur:
  D1 = metadata payload'da (aranan metne GIRMEZ)  -> saf filtre altyapisi
  D2 = metadata aranan metne de girer             -> kategori anlami tasiyor mu

Kullanim: uvx --with qdrant-client --with fastembed python3 sprint/qdrant-kategori.py
"""
import json, os, re, uuid, hashlib, time, warnings
from pathlib import Path
warnings.filterwarnings("ignore")

REPO = Path(__file__).resolve().parent.parent
MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
VN = "fast-paraphrase-multilingual-mpnet-base-v2"
MAX_KAR = 1400

env = json.load(open(REPO / ".mcp.json"))["mcpServers"]["qdrant"]["env"]
os.environ["FASTEMBED_CACHE_PATH"] = env["FASTEMBED_CACHE_PATH"]

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from fastembed import TextEmbedding

SKIP = {".git", ".remember", "sprint", "node_modules", "panel"}

# ------------------------------------------------------------- kategorileme

TUR_ETIKET = {
    "karar": "verilmis karar ve gerekcesi",
    "bulgu": "olculmus bulgu",
    "ders":  "Clara'nin dersi, duzeltilmesi gereken davranis",
    "kanon": "kural, kanon maddesi",
    "gunluk": "gunluk calisma kaydi",
    "inceleme": "inceleme kaydi, olcum sonucu",
    "fikir": "olgunlasan fikir",
    "proje": "proje/yapi tarifi",
}


def tur_bul(yol: str, baslik: str, govde: str) -> str:
    """Kaydin turunu yoldan + icerik deseninden cikarir. Tek deger doner."""
    b = (baslik or "")
    # icerik deseni yoldan ONCE gelir: gunluk icindeki bir "Bulgu N" bulgudur
    if re.search(r"^\s*Bulgu\s+\d+", b, re.I) or re.search(r"^\s*ASIL BULGU", b, re.I):
        return "bulgu"
    if re.search(r"ders|hata|korluk|clara'nin", b, re.I):
        return "ders"
    if re.search(r"^\s*(karar|neden|kararin sonuc)", b, re.I) and "kararlar/" in yol:
        return "karar"
    # sonra yol
    if yol.startswith("kararlar/"):
        return "karar"
    if yol.startswith(".claude/"):
        return "kanon"
    if yol.startswith("incelemeler/"):
        return "inceleme"
    if yol.startswith("fikirler/"):
        return "fikir"
    if yol.startswith("projeler/"):
        return "proje"
    if yol.startswith("gunluk/"):
        return "gunluk"
    return "gunluk"


def tarih_bul(yol: str, govde: str) -> str:
    """Dosya adindan ya da govdeden ISO tarih cikarir. Bulamazsa bos."""
    m = re.search(r"(20\d\d-\d\d-\d\d)", yol)
    if m:
        return m.group(1)
    m = re.search(r"(20\d\d-\d\d-\d\d)", govde[:400])
    return m.group(1) if m else ""


def konu_bul(yol: str) -> str:
    """Klasor adi konu sayilir (incelemeler/qdrant-kayit-bicimi -> qdrant-kayit-bicimi)."""
    p = Path(yol).parts
    if len(p) > 2:
        return p[1]
    if len(p) == 2:
        return Path(p[1]).stem
    return Path(yol).stem


# ------------------------------------------------------------- bolme (B ile ayni)

def bol_yapisal(text):
    out, cur, title = [], [], None
    for ln in text.split("\n"):
        if re.match(r"^##\s+", ln):
            if cur and "".join(cur).strip():
                out.append((title, "\n".join(cur).strip()))
            title = ln.lstrip("#").strip()
            cur = [ln]
        else:
            cur.append(ln)
    if cur and "".join(cur).strip():
        out.append((title, "\n".join(cur).strip()))
    return [(t, b) for t, b in out if len(b) > 80]


def bol_anlam(text):
    parca = []
    for title, body in bol_yapisal(text):
        if len(body) <= MAX_KAR:
            parca.append((title, body))
            continue
        paragraflar = [p.strip() for p in body.split("\n\n") if p.strip()]
        kova, boy = [], 0
        for p in paragraflar:
            if boy + len(p) > MAX_KAR and kova:
                parca.append((title, "\n\n".join(kova)))
                kova, boy = [], 0
            kova.append(p)
            boy += len(p)
        if kova:
            parca.append((title, "\n\n".join(kova)))
    return parca


def topla(metne_kat: bool):
    kayit = []
    for p in sorted(REPO.rglob("*.md")):
        rel = str(p.relative_to(REPO))
        if any(x in SKIP for x in Path(rel).parts):
            continue
        tx = p.read_text(encoding="utf-8", errors="replace")
        if not tx.strip():
            continue
        for i, (title, body) in enumerate(bol_anlam(tx)):
            tur = tur_bul(rel, title, body)
            tarih = tarih_bul(rel, body)
            konu = konu_bul(rel)
            if metne_kat:
                aranan = (f"[{TUR_ETIKET[tur]}] konu: {konu}\n"
                          f"{rel} — {title or ''}\n\n{body}")
            else:
                aranan = f"{rel} — {title or ''}\n\n{body}"
            kayit.append({
                "aranan": aranan,
                "payload": {"document": body[:600], "dosya": rel,
                            "baslik": title or "(giris)", "i": i, "kar": len(body),
                            "tur": tur, "tarih": tarih, "konu": konu},
            })
    return kayit


def yukle(c, model, ad, kayitlar):
    if c.collection_exists(ad):
        c.delete_collection(ad)
    c.create_collection(ad, vectors_config={VN: VectorParams(size=768, distance=Distance.COSINE)})
    t0, B = time.time(), 24
    for i in range(0, len(kayitlar), B):
        g = kayitlar[i:i + B]
        vs = list(model.embed([k["aranan"] for k in g]))
        c.upsert(collection_name=ad, points=[
            PointStruct(id=str(uuid.UUID(hashlib.md5(
                (k["payload"]["dosya"] + str(k["payload"]["i"]) + ad).encode()).hexdigest())),
                vector={VN: v.tolist()}, payload=k["payload"])
            for k, v in zip(g, vs)])
    print(f"  {ad}: {len(kayitlar)} kayit, {time.time()-t0:.0f}s", flush=True)


SORULAR = [
    ("neyi yanlis olcmusum daha once", "gunluk|incelemeler"),
    ("bir agent kuralina uymadiysa ilk ne kontrol edilir", "preload|clara|gunluk"),
    ("gereksiz personel almak neden yanlis", "yalin|karar|clara"),
    ("agent kendi tanimini gorebiliyor mu", "clara|gunluk|preload"),
    ("bir seyin sonucunu erken okumanin zarari ne", "clara|gunluk"),
    ("bu odada neden ikinci bir denetci yok", "CLAUDE|karar"),
    ("qdrant boyutu neden 768 secildi", "karar"),
    ("kanal kurali kaca kadar tuttu", "gunluk"),
    ("hangi hatayi iki kez yaptim", "gunluk"),
    ("clickup aramasi guvenilir mi", "clickup|incelemeler"),
]


def main():
    c = QdrantClient(url=env["QDRANT_URL"], api_key=env["QDRANT_API_KEY"],
                     check_compatibility=False)
    model = TextEmbedding(MODEL)
    print("yukleniyor:")
    d1 = topla(metne_kat=False)
    d2 = topla(metne_kat=True)
    yukle(c, model, "clara-deney-d1", d1)
    yukle(c, model, "clara-deney-d2", d2)

    # kategori dagilimi
    from collections import Counter
    say = Counter(k["payload"]["tur"] for k in d1)
    print("\nkategori dagilimi:")
    for t, n in say.most_common():
        print(f"  {t:10s} {n:4d}")
    tarihsiz = sum(1 for k in d1 if not k["payload"]["tarih"])
    print(f"  (tarihsiz kayit: {tarihsiz}/{len(d1)})")

    print("\n" + "=" * 76)
    print("B (kategorisiz) vs D1 (payload'da) vs D2 (metne katilmis)")
    print("=" * 76)
    skor = {"b": 0, "d1": 0, "d2": 0}
    for soru, bekle in SORULAR:
        v = list(model.embed([soru]))[0].tolist()
        print(f"\n{soru}")
        for etiket, ad in [("B ", "clara-deney-b"), ("D1", "clara-deney-d1"), ("D2", "clara-deney-d2")]:
            r = c.query_points(collection_name=ad, query=v, using=VN, limit=1,
                               with_payload=True).points
            if not r:
                print(f"    [{etiket}] sonuc yok")
                continue
            p = r[0].payload
            ok = bool(re.search(bekle, p["dosya"], re.I))
            skor[etiket.strip().lower()] += ok
            tur = p.get("tur", "-")
            print(f"    [{etiket}] {'OK ' if ok else 'yok'} %.3f  [%s] %s › %s" % (
                r[0].score, tur, p["dosya"], p["baslik"][:32]))

    print("\n" + "=" * 76)
    print(f"TOPLAM  B: {skor['b']}/10   D1: {skor['d1']}/10   D2: {skor['d2']}/10")
    print("=" * 76)


if __name__ == "__main__":
    main()
