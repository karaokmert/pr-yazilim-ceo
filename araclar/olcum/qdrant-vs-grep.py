"""Ayni soruyu grep ve vektor aramaya sorar, ikisinin bulduklarini yan yana koyar.

Sorular UC TIPTE (yukleme sonucu gorulmeden yazildi):
  A = kelimeyi biliyorum      -> grep'in en guclu oldugu yer
  B = kavrami biliyorum, kelimeyi bilmiyorum -> vektorun iddiasi
  C = sadece niyeti biliyorum  -> gercek kullanim

Kullanim: uvx --with qdrant-client --with fastembed python3 sprint/qdrant-vs-grep.py
"""
import json, os, re, subprocess, warnings
from pathlib import Path
warnings.filterwarnings("ignore")

REPO = Path(__file__).resolve().parent.parent
COLLECTION = "clara-arge-test"
MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
VN = "fast-paraphrase-multilingual-mpnet-base-v2"

env = json.load(open(REPO / ".mcp.json"))["mcpServers"]["qdrant"]["env"]
os.environ["FASTEMBED_CACHE_PATH"] = env["FASTEMBED_CACHE_PATH"]

from qdrant_client import QdrantClient
from fastembed import TextEmbedding

# (tip, dogal-dil-sorusu, grep-icin-makul-anahtar-kelime)
# grep kelimesi: bu soruyu soran birinin AKLINA GELECEK kelime, cevabin icindeki degil.
SORULAR = [
    ("A", "preload arizasi nedir",                      "preload"),
    ("A", "CLA-ARGUE-BACK kurali ne diyor",             "CLA-ARGUE-BACK"),
    ("B", "gereksiz personel almak neden yanlis",       "personel"),
    ("B", "agent kendi tanimini gorebiliyor mu",        "frontmatter"),
    ("B", "bir seyin sonucunu erken okumanin zarari",   "erken"),
    ("C", "neyi yanlis olcmusum daha once",             "yanlis olcum"),
    ("C", "hangi kararin gerekcesi zayif kalmis",       "gerekce"),
    ("C", "bu odada ikinci bir denetci neden yok",      "denetci"),
]


def grep_ara(kelime):
    """git grep -i, sadece .md; dosya:satir dondurur."""
    try:
        r = subprocess.run(
            ["grep", "-rniI", "--include=*.md", "--exclude-dir=.git",
             "--exclude-dir=.remember", "--exclude-dir=sprint", kelime, "."],
            cwd=REPO, capture_output=True, text=True, timeout=30)
        hits = [l for l in r.stdout.strip().split("\n") if l]
        return hits
    except Exception as e:
        return [f"HATA: {e}"]


def main():
    c = QdrantClient(url=env["QDRANT_URL"], api_key=env["QDRANT_API_KEY"],
                     check_compatibility=False)
    model = TextEmbedding(MODEL)

    print(f"koleksiyon: {c.get_collection(COLLECTION).points_count} nokta\n")
    print("=" * 78)

    for tip, soru, kelime in SORULAR:
        print(f"\n[{tip}] {soru}")
        print("-" * 78)

        g = grep_ara(kelime)
        print(f"  GREP '{kelime}': {len(g)} satir")
        for h in g[:3]:
            f, ln, txt = (h.split(":", 2) + ["", ""])[:3]
            print(f"     {f}:{ln}  {txt.strip()[:58]}")
        if len(g) > 3:
            print(f"     ... +{len(g)-3} satir daha")

        v = list(model.embed([soru]))[0].tolist()
        r = c.query_points(collection_name=COLLECTION, query=v, using=VN,
                           limit=3, with_payload=True).points
        print(f"  VEKTOR: ilk 3")
        for h in r:
            p = h.payload
            print(f"     %.3f  %s › %s" % (h.score, p.get("dosya"), p.get("baslik", "")[:38]))

    print("\n" + "=" * 78)


if __name__ == "__main__":
    main()
