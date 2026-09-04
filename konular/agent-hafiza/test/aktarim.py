"""Hükümlerin `hafiza` koleksiyonuna düzgün aktarımı + arama testinin tekrarı.

Düzgün = tek koleksiyon (hafiza), mükerrerler ayıklanmış (elle yazılan ile
taranan ikizlerden zengin olan kalır), şema tam. Mevcut karar kayıtlarına
dokunulmaz. Test: hafiza_testi.SORULAR aynı koleksiyona karşı koşulur;
tekilleştirmede düşen kodların beklentisi kalan ikizine çevrilir.
"""

import asyncio
import os
import sys

sys.path.insert(0, "/Users/karaok/p/qdrant-mcp/src")
import hafiza_testi as ht  # noqa: E402
from qdrant_mcp.settings import Settings  # noqa: E402
from qdrant_mcp.qdrant_memory import QdrantMemoryClient  # noqa: E402

# Elle yazılmış hükümlerden, taranan zengin ikizi olduğu için DÜŞENLER
DUSEN = {
    "surum-sabitle": "latest-image-birakilmaz",
    "grep-satir": "grep-satir-gosterme-disiplini",
    "vpn-amac": "vpn-sabit-cikis-ip",
    "plan-task-kosum": "plan-liste-kosum",
    "sayisal-olcum-yasak": "sayi-olcum-degildir",
    "memory-indeks": "indeks-emir-tasir",
    "memory-hizmetkar": "ciplak-kayit-skilli-ezer",
}


def ayar() -> Settings:
    return Settings(
        qdrant_url="https://rag.prventurestudio.com",
        qdrant_api_key=os.environ["QDRANT_API_KEY"],
        embedding_provider="tei",
        embedding_model="intfloat/multilingual-e5-base",
        tei_url="https://embed.prventurestudio.com",
        tei_api_key=os.environ["EMBED_API_KEY"],
        default_collection_name="hafiza",
    )


async def main():
    ht.gercek_veriyi_yukle()
    kayitlar = [(k, h, t, ko, ka) for k, h, t, ko, ka in ht.HUKUMLER if k not in DUSEN]
    print(f"aktarılacak: {len(kayitlar)} hüküm ({len(DUSEN)} mükerrer düştü)")

    c = QdrantMemoryClient(ayar())
    if os.environ.get("SADECE_TEST") != "1":
        for kod, hukum, tur, konu, kaynak in kayitlar:
            await c.store(hukum, metadata={
                "kod": kod, "tur": tur, "konu": konu, "yazan": "clara",
                "tarih": "2026-09-04", "kaynak_adres": kaynak,
            })
        print("aktarım bitti\n")

    # Test — beklentiler tekilleştirme sonrası kalan koda çevrilir
    for soru, hkod, _bkod, filtre, notu in ht.SORULAR:
        beklenen = DUSEN.get(hkod, hkod)
        hits = await c.find(soru, limit=5, filter=filtre)

        sira = "-"
        if beklenen is not None:
            sira = "YOK"
            for i, h in enumerate(hits, 1):
                if h["metadata"].get("kod") == beklenen:
                    sira = str(i)
                    break
        ilk = f"{hits[0]['score']:.3f} {hits[0]['metadata'].get('kod', hits[0]['metadata'].get('tur','?'))}" if hits else "boş"
        print(f"[{notu}] {soru!r}\n   beklenen sıra={sira:<4} ilk={ilk}\n")

    await c.close()


asyncio.run(main())
