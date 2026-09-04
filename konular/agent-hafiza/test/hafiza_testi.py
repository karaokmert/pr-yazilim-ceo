"""Agent hafızası — büyük test: kayıt yöntemi (hüküm vs blok) + model karşılaştırması.

Kullanım:
    uv run --with qdrant-client --with httpx --with pydantic-settings --with fastmcp \
        python hafiza_testi.py [koleksiyon-eki]

Koleksiyon eki verilmezse "" kullanılır (clara-1 / clara-2).
Model değişince ek verilir (örn. "large" → clara-1-large / clara-2-large) ve
aynı veri yeni modelle yeniden yazılıp aynı sorular koşulur.

Kaynak veri: Clara'nın gerçek kayıtları (konular/, agent-memory) — 2026-09-04
itibarıyla elle derlendi. Hassas içerik yok; iç know-how sınıfı.
"""

import asyncio
import os
import sys

sys.path.insert(0, "/Users/karaok/p/qdrant-mcp/src")
from qdrant_mcp.settings import Settings  # noqa: E402
from qdrant_mcp.qdrant_memory import QdrantMemoryClient  # noqa: E402

# ---------------------------------------------------------------- HÜKÜMLER (clara-1)
# (kod, hüküm, tur, konu, kaynak)
HUKUMLER = [
    ("grep-satir", "Aramada grep -l dosya adı verir, cevap vermez; satır gösteren -h ile aranır. Aynı soru -l ile 11 dosya adı, -h ile 47 satır ve bir çelişki döndürdü — çelişki kendiliğinden göründü.", "kazanim", "arama", "konular/olcum-arama/kararlar/2026-08-16-vektor-cikti-grep-disiplini-girdi.md"),
    ("dosya-degil-sorgu", "Erişim problemine yeni dosya açmak çözüm değildir; 485 markdown varken dert dosyalama değil sorgudur.", "karar", "arama", "agent-memory/feedback_dosya_degil_sorgu.md"),
    ("olcum-yerine-yorum", "Elde kanıt varken yorumlamak en sık ölçüm hatasıdır; kanıt açılıp okunur, üstüne yorum kurulmaz.", "kazanim", "olcum", "agent-memory/feedback_olcum_yerine_yorum.md"),
    ("bos-olcum-degil", "Boş dönen bir sorgu ölçüm değildir — okunmamış bir kutunun görünümü olabilir; yokluk iddiası kayıtsız verilmez.", "kazanim", "olcum", "agent-memory/feedback_bos_olcum_degil.md"),
    ("yokluk-veri-degil", "Kayıtta görünmeyen iş yapılmamış sayılmaz; sessizlikten insan hakkında hüküm çıkarılmaz.", "kazanim", "olcum", "agent-memory/feedback_yokluk_veri_degil.md"),
    ("karsilastirma-bicim", "Kısaltılmış ölçüm tam değerle karşılaştırılmaz; basename ad verir yol vermez — iki farklı biçimi kıyaslamak tahmini ölçüm sanmaktır.", "kazanim", "olcum", "agent-memory/feedback_karsilastirma_ayni_bicimde.md"),
    ("aracin-olctugu", "Bir aracın ne saydığı doğrulanmadan sonucu kullanılmaz: ps kabuğu saydı, sayım ölü pod'lardan geldi, sed büyük harfi ıskaladı — doğru ölçüt varlık kanıtıdır.", "kazanim", "olcum", "agent-memory/feedback_aracin_ne_olctugu.md"),
    ("kapsamini-yaz", "Her ölçümün kapsamı yazılır — neye BAKILMADIĞI da; kapsamsız ölçüm sonraki ölçümcüyü kör bırakır.", "karar", "olcum", "agent-memory/feedback_kapsamini_yaz.md"),
    ("yama-degil-sebep", "Hata düzeltilirken sebep kaldırılır, üstüne kural konmaz; 'şunu karıştırma' kuralı varsa karıştıran şey hâlâ oradadır ve kural bir yamadır.", "karar", "duzeltme", "agent-memory/feedback_yama_degil_sebep.md"),
    ("iki-yol-bir-kayit", "Bir iş iki yoldan yapılıp yalnız biri kayıt tutuyorsa arıza sessizdir: sonuç doğru çıkar, kayıt bozulur.", "kazanim", "duzeltme", "agent-memory/feedback_iki_yol_bir_kayit.md"),
    ("agent-cagirma", "Bir agent'a iş SendMessage ile verilir; Agent aracıyla çağrılan işin raporu kullanıcıya değil çağırana gider ve iş görünmez olur. Bilgi çıkarmak (tarama, analiz) için çağırmak serbesttir.", "karar", "agent-iletisim", "clara gövdesi + karar 2026-09-02"),
    ("handoff-tam-metin", "Handoff tam metin taşınır, adres verilmez; adres veren bir devir turu kaybettirdi — alan taraf dosyayı açmak zorunda kaldı.", "kazanim", "agent-iletisim", "agent-memory/feedback_handoff_tam_metin_tasinir.md"),
    ("rapor-kime", "Bir rapor başlığa değil içeriğe göre yönlendirilir; içinde başkasının sorusunun cevabı varsa ona da iletilir.", "kazanim", "agent-iletisim", "agent-memory/feedback_rapor_kime_gider.md"),
    ("plan-task-kosum", "Önce plan, sonra görev listesi, sonra koşum — Mert'in en önemli kuralı; ara adım sorulmaz, yalnız karar sorulur.", "karar", "calisma-duzeni", "agent-memory/feedback_plan_task_kosum.md"),
    ("sayisal-olcum-yasak", "Hiçbir şey sayıdan ibaret okunmaz: dosya, kod, fikir, klasör sayı değil içeriktir; sayı işaret olabilir, hüküm olamaz.", "karar", "calisma-duzeni", "CLAUDE.md kurallar"),
    ("mert-kisa-cevap", "Mert kısa cevap ister: sonuç + kritik nokta; detayı kendisi ister, istemeden verilmez.", "tercih", "mert", "agent-memory/user_mert_profil.md"),
    ("mert-secenek-sunma", "Mert'e bağlamsız şık listesi sunulmaz; problem anlatılır, kararı kendisi kurar — şık listesi sessizce çerçeve dayatır.", "tercih", "mert", "agent-memory/feedback_secenek_sunma.md"),
    ("mert-onay-brief", "Mert'e iş sunarken brief üç blok: şu an ne oluyor / nasıl çözüyorum / nereye dokunuyor — boş alanlar da yazılır.", "tercih", "mert", "clara-behavior skill"),
    ("mert-etki-analizi", "Etki analizi her task'ta istenmez; belirsizlik ya da risk varsa istenir — karar gereken her yerde durulur.", "tercih", "mert", "agent-memory/user_mert_etki_analizi_olcutu.md"),
    ("coolify-zemin", "Araç sunucusunun zemini Coolify'dır; Coolify K8s üstünde çalışmaz (Docker/Swarm destekler), K8s'e geçiş ayrı bir karardır.", "karar", "altyapi", "konular/altyapi/kararlar/2026-09-04-arac-sunucusu-zemini-coolify.md"),
    ("surum-sabitle", "Container image'larında latest bırakılmaz, sürüm sabitlenir; Coolify şablonu v14'e göre yazılmışken latest v15 çekti ve wg-easy Exited oldu.", "kazanim", "altyapi", "konular/altyapi/BILINMESI-GEREKENLER.md"),
    ("vpn-amac", "VPN'in asıl amacı sabit çıkış IP'sidir: ekip tek adresten çıkar, müşteri firewall'ına tek IP taahhüdü verilir.", "karar", "altyapi", "konular/altyapi/kararlar/2026-08-28-vpn-kararlari.md"),
    ("redirect-dns", "Tarayıcı 'too many redirects' verdiğinde ilk ölçüm SSL modu değil DNS'in doğru makineye bakıp bakmadığıdır; Cloudflare proxy açıkken dig origin'i göstermez.", "kazanim", "altyapi", "konular/altyapi/BILINMESI-GEREKENLER.md"),
    ("domain-strateji", "Domain stratejisi: pryazilim.net dev ortamları, pryazilim.com ana şirket araçları, prventurestudio.com AI şirketinin servisleri — AI araçları oraya subdomain alır.", "karar", "altyapi", "konular/altyapi/BILINMESI-GEREKENLER.md"),
    ("fastembed-cache", "FastEmbed modeli varsayılanda geçici alana indirir; FASTEMBED_CACHE_PATH verilmezse her sıfırlamada model yeniden iner.", "kazanim", "embedding", "auto-memory fastembed-tmp-cache-tuzagi.md"),
    ("e5-onek", "e5 ailesi modeller sorguya 'query: ', belgeye 'passage: ' öneki ister; eklenmezse arama kalitesi sessizce düşer.", "kazanim", "embedding", "konular/agent-hafiza/BILINMESI-GEREKENLER.md"),
    ("model-secim", "Türkçe embedding modeli kararı TR-MTEB benchmark'ıyla verilir; multilingual-e5 ailesi açık modellerin birincisidir, BGE-M3 orada test edilmemiştir.", "karar", "embedding", "konular/agent-hafiza/BILINMESI-GEREKENLER.md"),
    ("hf-begeni", "Hugging Face'te model seçerken beğeni sayısına bakılır; indirme sayısı otomasyon çekmeleriyle şişer, kalite göstergesi değildir.", "kazanim", "embedding", "konular/hugging-face/BILINMESI-GEREKENLER.md"),
    ("hf-lisans", "Model kartında 'license: other' görülen her yerde lisans metni okunur; FLUX.1-dev ticari kullanılamaz, aynı işi yapan schnell Apache-2.0 ile serbesttir.", "kazanim", "embedding", "konular/hugging-face/BILINMESI-GEREKENLER.md"),
    ("memory-indeks", "Agent'ın MEMORY.md indeksi oturum başında ilk 200 satır otomatik yüklenir; indekse pointer yazılır, kural yazılmaz — indeksteki cümle davranış talimatına dönüşür.", "karar", "hafiza", "OY memory-management skill"),
    ("memory-hizmetkar", "Hafıza skill'in hizmetkârıdır: skille çelişen çıplak kayıt doğru kuralı ezer, agent skili hiç açmadan kayda yaslanır.", "kazanim", "hafiza", "OY memory-management skill"),
    ("terfi-koprusu", "İki ve daha çok projede işe yarayan pattern skill-oneri etiketiyle işaretlenir; etiket adı sabittir çünkü terfi köprüsü onu tarar — eşanlamlı ad köprüyü kırar.", "karar", "hafiza", "OY memory-management skill"),
    ("guvenlik-acik-is", "rag ve embed servislerinde güvenlik sıkılaştırma (VPN'e alma, erişim daraltma) kurulumlar bitince yapılacak — açık iş, Mert'in takviminde.", "acik-is", "altyapi", "konular/agent-hafiza/PLAN.md"),
    ("fork-yama", "qdrant-mcp fork'una TEI sağlayıcısı, e5 önekleri ve qdrant_get aracı eklendi; hafiza-v2 branch'inde commit ve push kararı bekliyor.", "acik-is", "hafiza", "~/p/qdrant-mcp hafiza-v2 branch"),
    ("model-testi-acik", "mE5-base ile mE5-large karşılaştırması yapılacak; base'in ilk testinde sıralama kenarları yumuşak çıktı, alakalı-alakasız skor bandı dardı.", "acik-is", "embedding", "konular/agent-hafiza/PLAN.md"),
    ("sprint-carsamba", "Sprint planlama Çarşamba ritüelidir: kaynak Google Sheets, kayıt ClickUp, kişi kişi ilerlenir — sıra bozulunca iş yanlış tanımlanır.", "karar", "saha", "agent-memory/sprint-planlama-akisi.md"),
]

# ---------------------------------------------------------------- BLOKLAR (clara-2)
BLOK_PLANI = [
    ("blok-arama", "arama", ["grep-satir", "dosya-degil-sorgu"]),
    ("blok-olcum", "olcum", ["olcum-yerine-yorum", "bos-olcum-degil", "yokluk-veri-degil", "karsilastirma-bicim", "aracin-olctugu", "kapsamini-yaz"]),
    ("blok-duzeltme", "duzeltme", ["yama-degil-sebep", "iki-yol-bir-kayit"]),
    ("blok-agent-iletisim", "agent-iletisim", ["agent-cagirma", "handoff-tam-metin", "rapor-kime"]),
    ("blok-calisma-duzeni", "calisma-duzeni", ["plan-task-kosum", "sayisal-olcum-yasak"]),
    ("blok-mert", "mert", ["mert-kisa-cevap", "mert-secenek-sunma", "mert-onay-brief", "mert-etki-analizi"]),
    ("blok-altyapi", "altyapi", ["coolify-zemin", "surum-sabitle", "vpn-amac", "redirect-dns", "domain-strateji"]),
    ("blok-embedding", "embedding", ["fastembed-cache", "e5-onek", "model-secim", "hf-begeni", "hf-lisans"]),
    ("blok-hafiza", "hafiza", ["memory-indeks", "memory-hizmetkar", "terfi-koprusu"]),
    ("blok-acik-isler", "acik-is", ["guvenlik-acik-is", "fork-yama", "model-testi-acik"]),
    ("blok-saha", "saha", ["sprint-carsamba"]),
]

# ---------------------------------------------------------------- SORULAR
# (soru, beklenen hüküm kodu, beklenen blok kodu, filtre, not)
SORULAR = [
    ("aramada neden her seferinde farklı sonuç buluyorum", "grep-satir", "blok-arama", None, "farklı kelime"),
    ("yeni bir self hosted aracı hangi platforma kuruyoruz", "coolify-zemin", "blok-altyapi", None, "farklı kelime"),
    ("docker imajının sürümünü latest bırakmak sakıncalı mı", "surum-sabitle", "blok-altyapi", None, "yakın kelime"),
    ("Mert'e uzun detaylı rapor mu yazmalıyım", "mert-kisa-cevap", "blok-mert", None, "farklı kelime"),
    ("başka bir agent'a görevi nasıl iletirim", "agent-cagirma", "blok-agent-iletisim", None, "farklı kelime"),
    ("site sürekli kendine yönlendiriyor ve açılmıyor", "redirect-dns", "blok-altyapi", None, "belirti dili"),
    ("Türkçe için hangi gömme modelini seçmeliyiz", "model-secim", "blok-embedding", None, "farklı kelime"),
    ("arama cümlesinin başına bir ek koymak gerekiyor muydu", "e5-onek", "blok-embedding", None, "dolaylı anlatım"),
    ("haftalık planlama hangi gün ve nasıl yapılır", "sprint-carsamba", "blok-saha", None, "farklı kelime"),
    ("bir hatayı yeni kural ekleyerek çözmek doğru mu", "yama-degil-sebep", "blok-duzeltme", None, "farklı kelime"),
    ("which day do we do sprint planning", "sprint-carsamba", "blok-saha", None, "EDGE: İngilizce"),
    ("lisans", "hf-lisans", "blok-embedding", None, "EDGE: tek kelime"),
    ("akvaryum balığı bakımı nasıl yapılır", None, None, None, "EDGE: alakasız"),
    ("indirilen model dosyaları neden sürekli kayboluyor", "fastembed-cache", "blok-embedding", None, "belirti dili"),
    ("işi nasıl sunmalıyım", "mert-onay-brief", "blok-mert", {"tur": "tercih"}, "filtre: tur=tercih (blokta filtresiz)"),
    ("iki farklı yoldan yapılan işte kayıt neden bozuluyor", "iki-yol-bir-kayit", "blok-duzeltme", None, "farklı kelime"),
]


def gercek_veriyi_yukle() -> None:
    """gercek_hukumler.jsonl varsa HUKUMLER'e ekler (kod bazında tekilleştirir)."""
    import json
    from pathlib import Path

    yol = Path(__file__).parent / "gercek_hukumler.jsonl"
    if not yol.exists():
        return
    mevcut = {k for k, *_ in HUKUMLER}
    eklenen = 0
    for satir in yol.read_text().splitlines():
        satir = satir.strip()
        if not satir:
            continue
        k = json.loads(satir)
        if k["kod"] in mevcut:
            continue
        HUKUMLER.append((k["kod"], k["hukum"], k["tur"], k["konu"], k["kaynak"]))
        mevcut.add(k["kod"])
        eklenen += 1
    print(f"gercek_hukumler.jsonl: {eklenen} hüküm eklendi (toplam {len(HUKUMLER)})")


async def temizle(ek: str) -> None:
    """Koleksiyonları silip temiz kurulum sağlar (tekrar koşumda çift kayıt olmasın)."""
    c = QdrantMemoryClient(ayarlar(f"clara-1{ek}"))
    for ad in (f"clara-1{ek}", f"clara-2{ek}"):
        try:
            await c.client.delete_collection(ad)
            print(f"{ad}: eski koleksiyon silindi")
        except Exception:
            pass
    await c.close()


def ayarlar(koleksiyon: str) -> Settings:
    return Settings(
        qdrant_url="https://rag.prventurestudio.com",
        qdrant_api_key=os.environ["QDRANT_API_KEY"],
        embedding_provider="tei",
        embedding_model=os.environ.get("HAFIZA_MODEL", "intfloat/multilingual-e5-base"),
        tei_url="https://embed.prventurestudio.com",
        tei_api_key=os.environ["EMBED_API_KEY"],
        default_collection_name=koleksiyon,
    )


async def doldur(ek: str) -> None:
    c1 = QdrantMemoryClient(ayarlar(f"clara-1{ek}"))
    for kod, hukum, tur, konu, kaynak in HUKUMLER:
        await c1.store(hukum, metadata={"kod": kod, "tur": tur, "konu": konu, "yazan": "clara", "kaynak_adres": kaynak})
    print(f"clara-1{ek}: {len(HUKUMLER)} hüküm yazıldı")
    await c1.close()

    hukum_map = {k: (h, t) for k, h, t, _, _ in HUKUMLER}
    c2 = QdrantMemoryClient(ayarlar(f"clara-2{ek}"))
    for blok_kod, konu, uyeler in BLOK_PLANI:
        icerik = "\n".join(f"- {hukum_map[u][0]}" for u in uyeler)
        await c2.store(f"{konu.upper()} kuralları ve dersleri:\n{icerik}",
                       metadata={"kod": blok_kod, "konu": konu, "yazan": "clara", "uyeler": uyeler})
    print(f"clara-2{ek}: {len(BLOK_PLANI)} blok yazıldı\n")
    await c2.close()


async def test(ek: str) -> None:
    c1 = QdrantMemoryClient(ayarlar(f"clara-1{ek}"))
    c2 = QdrantMemoryClient(ayarlar(f"clara-2{ek}"))

    for soru, hkod, bkod, filtre, notu in SORULAR:
        h1 = await c1.find(soru, limit=5, filter=filtre)
        h2 = await c2.find(soru, limit=5)  # blokta tur filtresi yok

        def sira(hits, kod):
            if kod is None:
                return "-"
            for i, h in enumerate(hits, 1):
                if h["metadata"].get("kod") == kod:
                    return str(i)
            return "YOK"

        s1, s2 = sira(h1, hkod), sira(h2, bkod)
        t1 = f"{h1[0]['score']:.3f} {h1[0]['metadata'].get('kod','?')}" if h1 else "boş"
        t2 = f"{h2[0]['score']:.3f} {h2[0]['metadata'].get('kod','?')}" if h2 else "boş"
        print(f"[{notu}] {soru!r}")
        print(f"   hüküm: beklenen sıra={s1:<4} ilk={t1}")
        print(f"   blok : beklenen sıra={s2:<4} ilk={t2}\n")

    await c1.close()
    await c2.close()


async def main():
    ek = f"-{sys.argv[1]}" if len(sys.argv) > 1 else ""
    gercek_veriyi_yukle()
    if os.environ.get("SADECE_TEST") != "1":
        await temizle(ek)
        await doldur(ek)
    await test(ek)


if __name__ == "__main__":
    asyncio.run(main())
