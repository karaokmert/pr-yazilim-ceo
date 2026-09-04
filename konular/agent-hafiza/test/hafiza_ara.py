"""Hafıza arama CLI — kanal testinin Koşul Q aracı.

Kullanım:
    uv run --with qdrant-client --with httpx --with pydantic-settings --with fastmcp \
        python hafiza_ara.py "soru metni" [koleksiyon]

Varsayılan koleksiyon: clara-1. Çıktı: en iyi 5 hüküm + skor + kaynak adresi.
Anahtarlar ortamdan okunur: QDRANT_API_KEY, EMBED_API_KEY.
"""

import asyncio
import os
import sys

sys.path.insert(0, "/Users/karaok/p/qdrant-mcp/src")
from qdrant_mcp.settings import Settings  # noqa: E402
from qdrant_mcp.qdrant_memory import QdrantMemoryClient  # noqa: E402


async def main():
    if len(sys.argv) < 2:
        print("kullanım: hafiza_ara.py 'soru' [koleksiyon]")
        sys.exit(1)
    soru = sys.argv[1]
    koleksiyon = sys.argv[2] if len(sys.argv) > 2 else "clara-1"

    s = Settings(
        qdrant_url="https://rag.prventurestudio.com",
        qdrant_api_key=os.environ["QDRANT_API_KEY"],
        embedding_provider="tei",
        embedding_model="intfloat/multilingual-e5-base",
        tei_url="https://embed.prventurestudio.com",
        tei_api_key=os.environ["EMBED_API_KEY"],
        default_collection_name=koleksiyon,
    )
    c = QdrantMemoryClient(s)
    hits = await c.find(soru, limit=5)
    if not hits:
        print("sonuç yok")
    for h in hits:
        m = h["metadata"]
        print(f"[{h['score']:.3f}] ({m.get('tur','?')}/{m.get('konu','?')}) {h['content']}")
        if m.get("kaynak_adres") or m.get("kaynak"):
            print(f"        kaynak: {m.get('kaynak_adres') or m.get('kaynak')}")
    await c.close()


asyncio.run(main())
