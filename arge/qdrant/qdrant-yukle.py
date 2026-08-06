"""Repo dokumanlarini Qdrant'a yukler. Baslik bazli chunk'lar.

Kullanim: uvx --with qdrant-client --with fastembed python3 sprint/qdrant-yukle.py
"""
import json, os, re, uuid, warnings, hashlib
from pathlib import Path
warnings.filterwarnings("ignore")

REPO = Path(__file__).resolve().parent.parent
COLLECTION = "clara-arge-test"
MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
VN = "fast-paraphrase-multilingual-mpnet-base-v2"

env = json.load(open(REPO / ".mcp.json"))["mcpServers"]["qdrant"]["env"]
os.environ["FASTEMBED_CACHE_PATH"] = env["FASTEMBED_CACHE_PATH"]

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from fastembed import TextEmbedding

# .remember ve sprint disi: gecici/uretilmis dosyalar aramaya girmez
SKIP_DIRS = {".git", ".remember", "sprint", "node_modules"}


def chunks(text, path):
    """Markdown'i ## basliklarindan boler. Baslik yoksa dosyanin tamami tek chunk."""
    lines = text.split("\n")
    out, cur, title = [], [], None
    for ln in lines:
        if re.match(r"^##\s+", ln):
            if cur and "".join(cur).strip():
                out.append((title, "\n".join(cur).strip()))
            title = ln.lstrip("#").strip()
            cur = [ln]
        else:
            cur.append(ln)
    if cur and "".join(cur).strip():
        out.append((title, "\n".join(cur).strip()))
    # cok kucuk chunk'lari birlestir (tek satirlik baslik gurultu uretir)
    merged = []
    for t, body in out:
        if merged and len(body) < 200:
            pt, pb = merged[-1]
            merged[-1] = (pt, pb + "\n\n" + body)
        else:
            merged.append((t, body))
    return merged


def collect():
    docs = []
    for p in sorted(REPO.rglob("*.md")):
        rel = p.relative_to(REPO)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if not text.strip():
            continue
        for i, (title, body) in enumerate(chunks(text, rel)):
            # arama metnine yolu da kat: dosya adi anlamin parcasi
            searchable = f"{rel} — {title or ''}\n\n{body}"
            docs.append({
                "text": searchable,
                "payload": {
                    "document": body,
                    "dosya": str(rel),
                    "baslik": title or "(giris)",
                    "chunk": i,
                    "boyut": len(body),
                },
            })
    return docs


def main():
    c = QdrantClient(url=env["QDRANT_URL"], api_key=env["QDRANT_API_KEY"],
                     check_compatibility=False)

    if c.collection_exists(COLLECTION):
        c.delete_collection(COLLECTION)
        print(f"eski {COLLECTION} silindi")
    c.create_collection(COLLECTION, vectors_config={VN: VectorParams(size=768, distance=Distance.COSINE)})
    print(f"{COLLECTION} olusturuldu (768, cosine)")

    docs = collect()
    print(f"{len(docs)} chunk toplandi")

    import time
    t0 = time.time()
    model = TextEmbedding(MODEL)
    print(f"model hazir ({time.time()-t0:.1f}s) — gomme basliyor", flush=True)

    # parti parti: ilerleme gorunur olsun, bellek sismesin
    BATCH = 32
    t1 = time.time()
    for i in range(0, len(docs), BATCH):
        grup = docs[i:i + BATCH]
        vecs = list(model.embed([d["text"] for d in grup]))
        pts = [
            PointStruct(
                id=str(uuid.UUID(hashlib.md5(
                    (d["payload"]["dosya"] + str(d["payload"]["chunk"])).encode()).hexdigest())),
                vector={VN: v.tolist()},
                payload=d["payload"],
            )
            for d, v in zip(grup, vecs)
        ]
        c.upsert(collection_name=COLLECTION, points=pts)
        gecen = time.time() - t1
        bitti = i + len(grup)
        hiz = bitti / gecen if gecen else 0
        kalan = (len(docs) - bitti) / hiz if hiz else 0
        print(f"  {bitti}/{len(docs)}  {gecen:.0f}s gecti  ~{kalan:.0f}s kaldi", flush=True)

    print(f"yuklendi: {c.get_collection(COLLECTION).points_count} nokta "
          f"— gomme suresi {time.time()-t1:.0f}s", flush=True)

    sizes = [d["payload"]["boyut"] for d in docs]
    print(f"chunk boyu: min {min(sizes)}  ort {sum(sizes)//len(sizes)}  max {max(sizes)}")


if __name__ == "__main__":
    main()
