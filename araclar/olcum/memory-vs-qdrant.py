"""Yerel memory (21 dosya, MEMORY.md indeksli) vs Qdrant araması.

Mert'in sorusu: "yerel memory yerine qdrant kullanmak gereksiz o zaman?"

Onemli fark: MEMORY.md her oturum context'e OTOMATIK giriyor (22 satir).
Yani Clara 21 kaydin varligini aramadan biliyor. Qdrant'in cozdugu problem
("1000 kayit var, hangisi alakali") burada YOK.

Bu script iki seyi olcer:
  1. Sadece memory kayitlarini Qdrant'a atip ara -> dogru kaydi buluyor mu?
  2. MEMORY.md indeksi zaten dogru kaydi gosteriyor mu? (yani arama gereksiz mi)

Kullanim: uvx --with qdrant-client --with fastembed python3 sprint/memory-vs-qdrant.py
"""
import json, os, re, uuid, hashlib, time, warnings
from pathlib import Path
warnings.filterwarnings("ignore")

REPO = Path(__file__).resolve().parent.parent
MEM = REPO / ".claude/agent-memory/clara"
MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
VN = "fast-paraphrase-multilingual-mpnet-base-v2"
KOL = "clara-memory-testi"

env = json.load(open(REPO / ".mcp.json"))["mcpServers"]["qdrant"]["env"]
os.environ["FASTEMBED_CACHE_PATH"] = env["FASTEMBED_CACHE_PATH"]

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from fastembed import TextEmbedding

# (soru, beklenen memory dosyasi)
SORULAR = [
    ("cevabim ne kadar uzun olmali", "cevap_uzunlugu"),
    ("bir bulguyu nereye yazarim", "gunluk_kayit"),
    ("mert nasil calisir neyi sevmez", "mert_profil"),
    ("gereksiz personel almak neden yanlis", "yalin_uretim"),
    ("hatirladigim seye guvenebilir miyim", "hatirladigim_kayittir"),
    ("bir isi kac adima bolerim", "plan_task_kosum"),
    ("agent cagirma yasagini nasil asarim", "handoff_dili"),
    ("stres testini nasil kurarim", "stres_testi"),
    ("sahayi nasil izlerim", "saha_izleme"),
    ("mert VS Code kisayolu derken ne demek istiyor", "tabirler"),
]


def topla():
    """Her memory dosyasi TEK kayit — hepsi 3 KB alti, bolmeye gerek yok."""
    kayit = []
    for p in sorted(MEM.glob("*.md")):
        if p.name == "MEMORY.md":
            continue
        tx = p.read_text(encoding="utf-8", errors="replace")
        # frontmatter'i ayir: description aranan metne girmesin (QK-2)
        govde = re.sub(r"^---.*?---\n", "", tx, flags=re.S).strip()
        kayit.append({"aranan": govde, "dosya": p.name, "kar": len(govde)})
    return kayit


def main():
    c = QdrantClient(url=env["QDRANT_URL"], api_key=env["QDRANT_API_KEY"],
                     check_compatibility=False)
    model = TextEmbedding(MODEL)
    kayitlar = topla()

    if c.collection_exists(KOL):
        c.delete_collection(KOL)
    c.create_collection(KOL, vectors_config={VN: VectorParams(size=768, distance=Distance.COSINE)})
    t0 = time.time()
    vs = list(model.embed([k["aranan"] for k in kayitlar]))
    c.upsert(collection_name=KOL, points=[
        PointStruct(id=str(uuid.UUID(hashlib.md5(k["dosya"].encode()).hexdigest())),
                    vector={VN: v.tolist()},
                    payload={"dosya": k["dosya"], "kar": k["kar"]})
        for k, v in zip(kayitlar, vs)])
    kar = [k["kar"] for k in kayitlar]
    print(f"{len(kayitlar)} memory kaydi indekslendi, {time.time()-t0:.1f}s")
    print(f"boyut: min {min(kar)} ort {sum(kar)//len(kar)} max {max(kar)} karakter")
    print(f"(hepsi 514 token siniri civari veya altinda -> bolme gerekmedi)\n")

    print("=" * 76)
    print("QDRANT ARAMASI — 20 kayit icinde")
    print("=" * 76)
    ok = 0
    for soru, bekle in SORULAR:
        v = list(model.embed([soru]))[0].tolist()
        r = c.query_points(collection_name=KOL, query=v, using=VN, limit=3,
                           with_payload=True).points
        isabet = bool(r) and bekle in r[0].payload["dosya"]
        ok += isabet
        print(f"\n{soru}")
        print("  %s %.3f  %s" % ("OK " if isabet else "yok",
              r[0].score, r[0].payload["dosya"]))
        if not isabet:
            # dogru kayit kacinci sirada?
            for i, h in enumerate(r, 1):
                if bekle in h.payload["dosya"]:
                    print(f"       (dogru kayit {i}. sirada: %.3f)" % h.score)
                    break
            else:
                print(f"       (dogru kayit ilk 3'te YOK — beklenen: {bekle})")
    print(f"\n  QDRANT: {ok}/{len(SORULAR)}")

    print("\n" + "=" * 76)
    print("MEMORY.md INDEKSI — arama olmadan dogru kayit bulunabiliyor mu?")
    print("=" * 76)
    indeks = (MEM / "MEMORY.md").read_text(encoding="utf-8")
    satirlar = [l for l in indeks.split("\n") if l.strip().startswith("- [")]
    print(f"\nindeks {len(satirlar)} satir, {len(indeks)} karakter — her oturum context'te\n")
    for soru, bekle in SORULAR:
        # indekste beklenen dosyanin satiri var mi ve tarif ediyor mu?
        bulundu = [l for l in satirlar if bekle in l]
        if bulundu:
            tarif = bulundu[0].split("—")[-1].strip() if "—" in bulundu[0] else ""
            print(f"  OK  {soru[:44]:44s} -> {tarif[:44]}")
        else:
            print(f"  yok {soru[:44]:44s} -> INDEKSTE SATIR YOK ({bekle})")

    print("\n" + "=" * 76)
    print("MALIYET")
    print("=" * 76)
    print(f"  yerel memory : {len(kayitlar)} dosya, {sum(kar)} karakter")
    print(f"                 MEMORY.md {len(indeks)} karakter -> her oturum context'e giriyor")
    print(f"                 arama maliyeti: SIFIR (indeks zaten okundu)")
    print(f"  qdrant       : indeksleme {time.time()-t0:.1f}s, her degisiklikte tekrar")
    print(f"                 + MCP acilis (model RAM'e ~1.5s) + skor gorunmuyor")


if __name__ == "__main__":
    main()
