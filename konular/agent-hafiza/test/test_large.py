"""hafiza-large koleksiyonuna karşı hafiza_testi.SORULAR test setini ham HTTP ile koşar.

hafiza_testi.py'deki SORULAR (soru, beklenen hüküm kodu, beklenen blok kodu, filtre, not)
kullanılır; blok kodu burada anlamsız (tek koleksiyon), filtre varsa metadata.<alan>
yoluna çevrilir. aktarim.py'deki DUSEN çevirisi ile mükerrer düşen kodlar da uygulanır —
büyük test dosyası (hafiza_yedek) zaten tekilleştirilmiş olabilir, DUSEN çevirisi
sadece o kod koleksiyonda yoksa devreye girer (aşağıda kontrol edilir).
"""

import json
import os
import sys

import httpx

sys.path.insert(0, "/Users/karaok/p/pr-yazilim-ceo/konular/agent-hafiza/test")
import hafiza_testi as ht  # noqa: E402

QDRANT_URL = "https://rag.prventurestudio.com"
TEI_URL = "https://embed.prventurestudio.com"
COLLECTION = "hafiza-large"
MODEL = "intfloat/multilingual-e5-large"

QDRANT_API_KEY = os.environ["QDRANT_API_KEY"]
EMBED_API_KEY = os.environ["EMBED_API_KEY"]

# aktarim.py'deki mükerrer-düşen çevirisi (elle hüküm -> taranan zengin ikiz)
DUSEN = {
    "surum-sabitle": "latest-image-birakilmaz",
    "grep-satir": "grep-satir-gosterme-disiplini",
    "vpn-amac": "vpn-sabit-cikis-ip",
    "plan-task-kosum": "plan-liste-kosum",
    "sayisal-olcum-yasak": "sayi-olcum-degildir",
    "memory-indeks": "indeks-emir-tasir",
    "memory-hizmetkar": "ciplak-kayit-skilli-ezer",
}


def embed_query(client: httpx.Client, text: str) -> list[float]:
    r = client.post(
        f"{TEI_URL}/v1/embeddings",
        headers={"Authorization": f"Bearer {EMBED_API_KEY}"},
        json={"input": "query: " + text, "model": MODEL},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["data"][0]["embedding"]


def to_qdrant_filter(filtre: dict | None) -> dict | None:
    if not filtre:
        return None
    must = [{"key": f"metadata.{k}", "match": {"value": v}} for k, v in filtre.items()]
    return {"must": must}


def search(client: httpx.Client, vector: list[float], filtre: dict | None, limit: int = 5) -> list[dict]:
    body = {"vector": vector, "limit": limit, "with_payload": True}
    qf = to_qdrant_filter(filtre)
    if qf:
        body["filter"] = qf
    r = client.post(
        f"{QDRANT_URL}/collections/{COLLECTION}/points/search",
        headers={"api-key": QDRANT_API_KEY, "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["result"]


def get_existing_kodlar(client: httpx.Client) -> set[str]:
    """Koleksiyondaki tüm metadata.kod değerlerini toplar (DUSEN çevirisi kararı için)."""
    kodlar = set()
    offset = None
    while True:
        body = {"limit": 200, "with_payload": True, "with_vector": False}
        if offset:
            body["offset"] = offset
        r = client.post(
            f"{QDRANT_URL}/collections/{COLLECTION}/points/scroll",
            headers={"api-key": QDRANT_API_KEY, "Content-Type": "application/json"},
            json=body,
            timeout=60,
        )
        r.raise_for_status()
        res = r.json()["result"]
        for p in res["points"]:
            kod = p["payload"].get("metadata", {}).get("kod")
            if kod:
                kodlar.add(kod)
        offset = res.get("next_page_offset")
        if not offset:
            break
    return kodlar


def main():
    with httpx.Client() as client:
        mevcut_kodlar = get_existing_kodlar(client)
        print(f"koleksiyonda {len(mevcut_kodlar)} benzersiz kod var\n")

        sonuclar = []
        for soru, hkod, _bkod, filtre, notu in ht.SORULAR:
            beklenen = hkod
            if beklenen is not None and beklenen not in mevcut_kodlar:
                beklenen = DUSEN.get(beklenen, beklenen)

            vec = embed_query(client, soru)
            hits = search(client, vec, filtre, limit=5)

            sira = "-"
            if beklenen is not None:
                sira = "YOK"
                for i, h in enumerate(hits, 1):
                    if h["payload"].get("metadata", {}).get("kod") == beklenen:
                        sira = str(i)
                        break

            if hits:
                ilk_skor = hits[0]["score"]
                ilk_kod = hits[0]["payload"].get("metadata", {}).get("kod", "?")
                ilk = f"{ilk_skor:.3f} {ilk_kod}"
            else:
                ilk_skor = None
                ilk_kod = None
                ilk = "boş"

            print(f"[{notu}] {soru!r}")
            print(f"   beklenen kod={beklenen}  sıra={sira:<4} ilk={ilk}\n")

            sonuclar.append({
                "soru": soru,
                "beklenen": beklenen,
                "sira": sira,
                "ilk_skor": ilk_skor,
                "ilk_kod": ilk_kod,
                "notu": notu,
            })

        # özet
        toplam = len(sonuclar)
        ilk_sirada = sum(1 for s in sonuclar if s["sira"] == "1")
        ilk5 = sum(1 for s in sonuclar if s["sira"] not in ("YOK", "-"))
        yok = sum(1 for s in sonuclar if s["sira"] == "YOK")
        beklentisiz = sum(1 for s in sonuclar if s["sira"] == "-")

        print("=" * 60)
        print(f"ÖZET: toplam={toplam}  1.sırada={ilk_sirada}  ilk5'te={ilk5}  YOK={yok}  beklentisiz(alakasız-soru)={beklentisiz}")

        dogru_skorlari = [s["ilk_skor"] for s in sonuclar if s["sira"] == "1" and s["ilk_skor"] is not None]
        alakasiz_skorlari = [s["ilk_skor"] for s in sonuclar if s["beklenen"] is None and s["ilk_skor"] is not None]
        if dogru_skorlari:
            print(f"doğru cevap (1.sırada) skor bandı: {min(dogru_skorlari):.3f} – {max(dogru_skorlari):.3f}")
        if alakasiz_skorlari:
            print(f"alakasız soru ilk sonuç skor bandı: {min(alakasiz_skorlari):.3f} – {max(alakasiz_skorlari):.3f}")

        # ham veriyi de dök (rapor için)
        out_path = "/Users/karaok/p/pr-yazilim-ceo/konular/agent-hafiza/test/test_large_sonuc.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(sonuclar, f, ensure_ascii=False, indent=2)
        print(f"\nham sonuçlar: {out_path}")


if __name__ == "__main__":
    main()
