"""Gorev #3: cakisma + tazelik testi. Kayit biciminden BAGIMSIZ arama riski.

Simdiye kadarki sorular tek dogru cevapliydi. Gercekte bir soru birden fazla
kayda dokunuyor. Iki risk olculur:

  CAKISMA  — ilk 3 sonuc ayni konunun farkli parcalari mi (cesitlilik yok mu)?
  TAZELIK  — eskimis bir kayit taze kaydi bastiriyor mu?

Ikinci risk somut: incelemeler/skill-preload-bulgusu "eskimis olabilir" etiketli
(HARITA.md) ama dun 0.741 ile birinci geldi. Eskimis kayit en guclu cevapsa,
arama gecmisi bugun sanabilir.

Kullanim: uvx --with qdrant-client --with fastembed python3 sprint/qdrant-cakisma.py
"""
import json, os, warnings, re
from collections import Counter
from pathlib import Path
warnings.filterwarnings("ignore")

REPO = Path(__file__).resolve().parent.parent
MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
VN = "fast-paraphrase-multilingual-mpnet-base-v2"
KOLEKSIYON = "clara-deney-b"   # kazanan bicim

env = json.load(open(REPO / ".mcp.json"))["mcpServers"]["qdrant"]["env"]
os.environ["FASTEMBED_CACHE_PATH"] = env["FASTEMBED_CACHE_PATH"]

from qdrant_client import QdrantClient
from fastembed import TextEmbedding

# Coklu-cevapli sorular: her biri bilerek birden fazla kayda dokunuyor
SORULAR = [
    "preload arizasi ne zaman bulundu ve simdi durumu ne",
    "clara kac kez duzeltildi ve hangi konularda",
    "agent cagirma yasaginin gerekcesi ne",
    "kanal deneyinde neler olcuIdu",
    "hangi kararlar 5 agustosta verildi",
]


def main():
    c = QdrantClient(url=env["QDRANT_URL"], api_key=env["QDRANT_API_KEY"],
                     check_compatibility=False)
    model = TextEmbedding(MODEL)

    print("=" * 78)
    print("CAKISMA TESTI — ilk 5 sonuc kac AYRI dosyadan geliyor?")
    print("=" * 78)
    for soru in SORULAR:
        v = list(model.embed([soru]))[0].tolist()
        r = c.query_points(collection_name=KOLEKSIYON, query=v, using=VN,
                           limit=5, with_payload=True).points
        dosyalar = [h.payload["dosya"] for h in r]
        ayri = len(set(dosyalar))
        say = Counter(dosyalar)
        tekrar = [f"{d.split('/')[-1]}×{n}" for d, n in say.items() if n > 1]
        print(f"\n{soru}")
        print(f"  5 sonuc -> {ayri} ayri dosya" + (f"  TEKRAR: {', '.join(tekrar)}" if tekrar else "  (hepsi ayri)"))
        for h in r:
            print("    %.3f  %s › %s" % (h.score, h.payload["dosya"], h.payload["baslik"][:34]))

    print("\n" + "=" * 78)
    print("TAZELIK TESTI — eskimis kayit taze kaydi bastiriyor mu?")
    print("=" * 78)
    # HARITA.md'de "eskimis olabilir" etiketli tek kayit: skill-preload-bulgusu
    # Onu bastirmasi gereken taze kaynak: gunluk/2026-08-05 (hook sonrasi durum)
    for soru in ["skill preload sorunu cozuldu mu",
                 "agent skilleri simdi yukleniyor mu",
                 "preload arizasi hala gecerli mi"]:
        v = list(model.embed([soru]))[0].tolist()
        r = c.query_points(collection_name=KOLEKSIYON, query=v, using=VN,
                           limit=5, with_payload=True).points
        print(f"\n{soru}")
        for h in r:
            d = h.payload["dosya"]
            # tarih cikar: dosya adindan
            m = re.search(r"(20\d\d-\d\d-\d\d)", d)
            tarih = m.group(1) if m else "tarihsiz"
            eskimis = "  <-- ESKIMIS ETIKETLI" if "skill-preload-bulgusu" in d else ""
            print("    %.3f  [%s]  %s › %s%s" % (
                h.score, tarih, d, h.payload["baslik"][:30], eskimis))


if __name__ == "__main__":
    main()
