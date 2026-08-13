"""Gorev #2: metadata filtreli arama olcumu.

Uc soru:
  1. Filtre isabeti ARTIRIYOR mu? (tur=karar ile ararsam karar sorusu duzelir mi)
  2. Filtre alakasiz sonucu ENGELLIYOR mu? (esik yazamiyorum, filtre yerine gecer mi)
  3. MCP'nin qdrant-find'i filtre destekliyor mu? (semasinda parametre YOK -> muhtemelen hayir)

Kullanim: uvx --with qdrant-client --with fastembed python3 sprint/qdrant-filtre.py
"""
import json, os, warnings, re
from pathlib import Path
warnings.filterwarnings("ignore")

REPO = Path(__file__).resolve().parent.parent
MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
VN = "fast-paraphrase-multilingual-mpnet-base-v2"
KOL = "clara-deney-d1"   # kazanan bicim (metadata payload'da)

env = json.load(open(REPO / ".mcp.json"))["mcpServers"]["qdrant"]["env"]
os.environ["FASTEMBED_CACHE_PATH"] = env["FASTEMBED_CACHE_PATH"]

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, MatchAny, Range
from fastembed import TextEmbedding

# (soru, beklenen dosya deseni, hangi tur ile filtrelenmeli)
FILTRE_TESTI = [
    ("qdrant boyutu neden 768 secildi", "karar", "karar"),
    ("gereksiz personel almak neden yanlis", "karar|clara", "karar"),
    ("bu odada neden ikinci denetci yok", "karar|CLAUDE", "karar"),
    ("bir seyin sonucunu erken okumanin zarari ne", "clara", "kanon"),
    ("agent cagirmak neden yasak", "clara", "kanon"),
    ("hangi hatayi iki kez yaptim", "gunluk", "bulgu"),
    ("clickup aramasi guvenilir mi", "clickup", "ders"),
]

# Alakasiz sorular: filtre bunlari engelliyor mu?
ALAKASIZ = [
    "italyan mutfaginda makarna pisirme suresi",
    "2024 formula 1 sampiyonu kim",
    "bisiklet zinciri nasil yaglanir",
]


def ara(c, model, soru, flt=None, limit=3):
    v = list(model.embed([soru]))[0].tolist()
    return c.query_points(collection_name=KOL, query=v, using=VN, limit=limit,
                          query_filter=flt, with_payload=True).points


def main():
    c = QdrantClient(url=env["QDRANT_URL"], api_key=env["QDRANT_API_KEY"],
                     check_compatibility=False)
    model = TextEmbedding(MODEL)

    print("=" * 78)
    print("TEST 1 — filtre isabeti artiriyor mu? (filtresiz vs tur-filtreli)")
    print("=" * 78)
    ham, filt = 0, 0
    for soru, bekle, tur in FILTRE_TESTI:
        r1 = ara(c, model, soru)
        f = Filter(must=[FieldCondition(key="tur", match=MatchValue(value=tur))])
        r2 = ara(c, model, soru, f)
        o1 = bool(r1) and bool(re.search(bekle, r1[0].payload["dosya"], re.I))
        o2 = bool(r2) and bool(re.search(bekle, r2[0].payload["dosya"], re.I))
        ham += o1
        filt += o2
        print(f"\n{soru}   (filtre: tur={tur})")
        print("  filtresiz: %s %.3f  %s" % ("OK " if o1 else "yok",
              r1[0].score if r1 else 0, r1[0].payload["dosya"] if r1 else "-"))
        print("  filtreli : %s %.3f  %s" % ("OK " if o2 else "yok",
              r2[0].score if r2 else 0, r2[0].payload["dosya"] if r2 else "-"))
    print(f"\n  TOPLAM  filtresiz {ham}/{len(FILTRE_TESTI)}   filtreli {filt}/{len(FILTRE_TESTI)}")

    print("\n" + "=" * 78)
    print("TEST 2 — filtre alakasiz soruyu engelliyor mu? (esik yerine gecer mi)")
    print("=" * 78)
    f_karar = Filter(must=[FieldCondition(key="tur", match=MatchValue(value="karar"))])
    for soru in ALAKASIZ:
        r1 = ara(c, model, soru, limit=1)
        r2 = ara(c, model, soru, f_karar, limit=1)
        print(f"\n{soru}")
        print("  filtresiz: %.3f  %s" % (r1[0].score, r1[0].payload["dosya"]))
        print("  tur=karar: %.3f  %s" % (r2[0].score, r2[0].payload["dosya"]))
    print("\n  NOT: filtre sonuc SAYISINI daraltir, SKORU degistirmez.")
    print("       Alakasiz soru filtre icinde de en yakin komsuyu bulur -> esik yerine GECMEZ.")

    print("\n" + "=" * 78)
    print("TEST 3 — tarih filtresi kullanilabilir mi? (473/797 kayit tarihsiz)")
    print("=" * 78)
    # tarihsiz kayitlar filtreye HIC girmez -> sessiz kayip
    f_taze = Filter(must=[FieldCondition(key="tarih", range=None,
                                         match=MatchAny(any=["2026-08-05", "2026-08-06"]))])
    soru = "en son ne olctum"
    r1 = ara(c, model, soru, limit=3)
    r2 = ara(c, model, soru, f_taze, limit=3)
    print(f"\n{soru}")
    print("  filtresiz:")
    for h in r1:
        print("    %.3f  [%s]  %s" % (h.score, h.payload.get("tarih") or "TARIHSIZ", h.payload["dosya"]))
    print("  tarih in (08-05, 08-06):")
    for h in r2:
        print("    %.3f  [%s]  %s" % (h.score, h.payload.get("tarih") or "TARIHSIZ", h.payload["dosya"]))

    print("\n" + "=" * 78)
    print("TEST 4 — MCP qdrant-find filtre destekliyor mu?")
    print("=" * 78)
    print("  Arac semasi (bu oturumda yuklendi):")
    print("    qdrant-find: {collection_name, query}  -> filtre parametresi YOK")
    print("    qdrant-store: {collection_name, information, metadata}")
    print()
    print("  Yani: metadata YAZILABILIYOR ama ARANIRKEN filtrelenemiyor.")
    print("  Filtre yalnizca script'ten (qdrant-client) kullanilabilir.")


if __name__ == "__main__":
    main()
