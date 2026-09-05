"""hafiza_yedek_2026-09-04.jsonl kayıtlarını `hafiza-large` koleksiyonuna ham HTTP
upsert ile aktarır (client.store DEĞİL — model/koleksiyon TEI çağrısı dışında elle
kontrol edilir çünkü client.store varsayılan modeli kullanır, biz e5-large istiyoruz).

- Vektör: TEI'den "passage: " önekiyle.
- Point id: JSONL'deki id aynen korunur.
- Payload: content/timestamp/metadata aynen korunur; yalnız embedding_model
  "intfloat/multilingual-e5-large" yapılır, embedding_provider "tei" kalır.
"""

import json
import os
import sys
import time

import httpx

QDRANT_URL = "https://rag.prventurestudio.com"
TEI_URL = "https://embed.prventurestudio.com"
COLLECTION = "hafiza-large"
MODEL = "intfloat/multilingual-e5-large"
JSONL_PATH = "/Users/karaok/p/pr-yazilim-ceo/konular/agent-hafiza/test/hafiza_yedek_2026-09-04.jsonl"
BATCH_SIZE = 32

QDRANT_API_KEY = os.environ["QDRANT_API_KEY"]
EMBED_API_KEY = os.environ["EMBED_API_KEY"]


def embed_batch(client: httpx.Client, texts: list[str]) -> list[list[float]]:
    r = client.post(
        f"{TEI_URL}/v1/embeddings",
        headers={"Authorization": f"Bearer {EMBED_API_KEY}"},
        json={"input": texts, "model": MODEL},
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()["data"]
    # TEI/OpenAI-uyumlu endpoint sırayı korur ama garanti için index'e göre sırala
    data.sort(key=lambda d: d["index"])
    return [d["embedding"] for d in data]


def load_records() -> list[dict]:
    records = []
    with open(JSONL_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def main():
    records = load_records()
    print(f"okunan kayıt: {len(records)}")

    with httpx.Client() as client:
        upserted = 0
        for i in range(0, len(records), BATCH_SIZE):
            batch = records[i : i + BATCH_SIZE]
            texts = ["passage: " + rec["payload"]["content"] for rec in batch]

            vectors = embed_batch(client, texts)

            points = []
            for rec, vec in zip(batch, vectors):
                payload = dict(rec["payload"])  # kopya — orijinali bozma
                payload["embedding_model"] = MODEL
                payload["embedding_provider"] = "tei"
                points.append(
                    {
                        "id": rec["id"],
                        "vector": vec,
                        "payload": payload,
                    }
                )

            r = client.put(
                f"{QDRANT_URL}/collections/{COLLECTION}/points",
                headers={"api-key": QDRANT_API_KEY, "Content-Type": "application/json"},
                json={"points": points},
                timeout=120,
            )
            r.raise_for_status()
            upserted += len(points)
            print(f"  batch {i // BATCH_SIZE + 1}: {len(points)} point upsert edildi (toplam {upserted})")

        # count doğrulama
        r = client.post(
            f"{QDRANT_URL}/collections/{COLLECTION}/points/count",
            headers={"api-key": QDRANT_API_KEY, "Content-Type": "application/json"},
            json={"exact": True},
            timeout=30,
        )
        r.raise_for_status()
        count = r.json()["result"]["count"]
        print(f"\ncount doğrulama: qdrant'ta {count} point, jsonl'de {len(records)} kayıt")
        if count != len(records):
            print("UYARI: sayılar eşleşmiyor!")
        else:
            print("OK: sayılar eşleşiyor.")


if __name__ == "__main__":
    main()
