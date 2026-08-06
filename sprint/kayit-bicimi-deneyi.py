"""Ayni bilgiyi UC farkli bicimde kaydedip ayni sorulari sorar.

Amac: Clara'nin gelecekte ihtiyac duyacagi kayitlari HANGI bicimde
kaydederse bulabildigini olcmek. Bulan bicim kural olur.

A = YAPISAL   : markdown basligindan bol (dunku hali, kontrol grubu)
B = ANLAM     : her bulgu/karar/ders ayri kayit, 500 token siniri
C = ANLAM+OZ  : ayni + basina tek cumle oz (aramaya oz de girer)

Kullanim: uvx --with qdrant-client --with fastembed python3 sprint/kayit-bicimi-deneyi.py
"""
import json, os, re, uuid, hashlib, time, warnings
from pathlib import Path
warnings.filterwarnings("ignore")

REPO = Path(__file__).resolve().parent.parent
MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
VN = "fast-paraphrase-multilingual-mpnet-base-v2"
MAX_KAR = 1400  # ~460 token, 514 limitinin altinda kalsin

env = json.load(open(REPO / ".mcp.json"))["mcpServers"]["qdrant"]["env"]
os.environ["FASTEMBED_CACHE_PATH"] = env["FASTEMBED_CACHE_PATH"]

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from fastembed import TextEmbedding

SKIP = {".git", ".remember", "sprint", "node_modules", "panel"}

# ---------------------------------------------------------------- bolucular

def bol_yapisal(text):
    """A: ## basligindan bol, uzunluk sinirlamasi YOK (dunku hali)."""
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
    """B: once basliktan bol, sonra UZUN olani paragraf sinirindan tekrar bol.

    Her parca kendi basligini tasir (baglam kaybolmasin) ve MAX_KAR alti kalir.
    """
    parca = []
    for title, body in bol_yapisal(text):
        if len(body) <= MAX_KAR:
            parca.append((title, body))
            continue
        # paragraf sinirindan topla
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


def oz_cikar(title, body):
    """C icin: kaydin ilk anlamli cumlesi + basligi oz sayilir.

    Model degil kural uretiyor - amac 'oz eklemek isabeti artirir mi' sorusu.
    Ilk kalin (**...**) ifade ya da ilk cumle alinir.
    """
    kalin = re.findall(r"\*\*(.+?)\*\*", body)
    if kalin:
        oz = kalin[0].strip(" .:—-")
    else:
        duz = re.sub(r"[#*`>\-]", " ", body)
        cumle = re.split(r"(?<=[.!?])\s", duz.strip())
        oz = (cumle[0] if cumle else "")[:160].strip()
    return f"{title or ''} — {oz}".strip(" —")


# ---------------------------------------------------------------- toplama

def topla(bolucu, ozle=False):
    kayit = []
    for p in sorted(REPO.rglob("*.md")):
        rel = p.relative_to(REPO)
        if any(x in SKIP for x in rel.parts):
            continue
        tx = p.read_text(encoding="utf-8", errors="replace")
        if not tx.strip():
            continue
        for i, (title, body) in enumerate(bolucu(tx)):
            if ozle:
                oz = oz_cikar(title, body)
                aranan = f"OZ: {oz}\n\n{rel}\n\n{body}"
            else:
                aranan = f"{rel} — {title or ''}\n\n{body}"
            kayit.append({
                "aranan": aranan,
                "payload": {"document": body[:600], "dosya": str(rel),
                            "baslik": title or "(giris)", "i": i, "kar": len(body)},
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
            PointStruct(
                id=str(uuid.UUID(hashlib.md5(
                    (k["payload"]["dosya"] + str(k["payload"]["i"]) + ad).encode()).hexdigest())),
                vector={VN: v.tolist()}, payload=k["payload"])
            for k, v in zip(g, vs)])
        print(f"    {min(i+B,len(kayitlar))}/{len(kayitlar)}", end="\r", flush=True)
    kar = [k["payload"]["kar"] for k in kayitlar]
    print(f"  {ad}: {len(kayitlar)} kayit, {time.time()-t0:.0f}s, "
          f"ort {sum(kar)//len(kar)} kar, max {max(kar)} kar", flush=True)


# ---------------------------------------------------------------- sorular
# Clara'nin GELECEKTE soracagi sorular. Beklenen cevap: hangi dosyada olmali.
SORULAR = [
    ("neyi yanlis olcmusum daha once", "gunluk|incelemeler"),
    ("bir agent kuralina uymadiysa ilk ne kontrol edilir", "clara|gunluk"),
    ("gereksiz personel almak neden yanlis", "yalin|karar|clara"),
    ("agent kendi tanimini gorebiliyor mu", "clara|gunluk"),
    ("bir seyin sonucunu erken okumanin zarari ne", "clara|gunluk"),
    ("bu odada neden ikinci bir denetci yok", "CLAUDE|karar"),
    ("qdrant boyutu neden 768 secildi", "karar"),
    ("kanal kurali kaca kadar tuttu", "gunluk"),
    ("hangi hatayi iki kez yaptim", "gunluk"),
    ("clickup aramasi guvenilir mi", "clickup|incelemeler"),
]


def sor(c, model, adlar):
    print("\n" + "=" * 76)
    print("AYNI SORULAR, UC BICIM")
    print("=" * 76)
    for soru, bekle in SORULAR:
        v = list(model.embed([soru]))[0].tolist()
        print(f"\n{soru}")
        print(f"  (beklenen dosya deseni: {bekle})")
        for ad in adlar:
            r = c.query_points(collection_name=ad, query=v, using=VN,
                               limit=3, with_payload=True).points
            etiket = ad.split("-")[-1].upper()
            ilk = r[0] if r else None
            isabet = "?"
            if ilk:
                isabet = "OK " if re.search(bekle, ilk.payload["dosya"], re.I) else "yok"
            print(f"    [{etiket}] {isabet} %.3f  %s › %s" % (
                ilk.score if ilk else 0,
                ilk.payload["dosya"] if ilk else "-",
                (ilk.payload["baslik"][:36] if ilk else "-")))


def main():
    c = QdrantClient(url=env["QDRANT_URL"], api_key=env["QDRANT_API_KEY"],
                     check_compatibility=False)
    t = time.time()
    model = TextEmbedding(MODEL)
    print(f"model hazir {time.time()-t:.1f}s\n")

    print("yukleniyor:")
    yukle(c, model, "clara-deney-a", topla(bol_yapisal))
    yukle(c, model, "clara-deney-b", topla(bol_anlam))
    yukle(c, model, "clara-deney-c", topla(bol_anlam, ozle=True))

    sor(c, model, ["clara-deney-a", "clara-deney-b", "clara-deney-c"])
    print("\n" + "=" * 76)
    print("koleksiyonlar duruyor: clara-deney-a / -b / -c")


if __name__ == "__main__":
    main()
