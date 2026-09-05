"""Araştırma bulgularının clara-analiz koleksiyonuna kaydı — TASARIM.md şemasının
canlı örneği. Hükümler Clara'nın damıtması; embed TEI (mE5-large, 1024).
Bir kayıt bir fikir; content belirti dilinde hüküm; detay kendi kendine yeter."""

import json
import os
import urllib.request
import uuid

QDRANT = "https://rag.prventurestudio.com"
TEI = "https://embed.prventurestudio.com"
QKEY = os.environ["QDRANT_API_KEY"]
EKEY = os.environ["EMBED_API_KEY"]
KOL = "clara-analiz"
TARIH = "2026-09-05"

ORTAK = {"katman": "hukum", "yazan": "clara", "tarih": TARIH,
         "kayit_tarihi": TARIH, "durum": "gecerli",
         "konu": "agent-hafiza", "kaynak_adres": "konular/agent-hafiza/TASARIM.md"}

KAYITLAR = [
    ("kazanim", "Dokümanı cümle cümle ya da çok ince bölmek aramayı iyileştirmez — parça anlam taşımayınca ilk sıradaki isabet düşer; en iyi birim paragraf boyudur.",
     "İç ölçüm (164 soru, 6 yöntem): paragraf hit@1 0.79 / hit@5 0.97 ile birinci; cümle hit@1 0.70, tam doküman 0.63 ile sonuncu. Literatür bağımsız aynı sonuçta: Vectara (NAACL 2025, arXiv:2410.13070) 'semantic chunking maliyeti kazancı karşılamıyor, fixed-size daha iyi'; FloTorch 2026: aşırı küçük parçalar (ort. 43 token) end-to-end doğruluğu %54'e düşürdü, 512-token parçalar %67-69. Ders: arama birimi anlam taşıyacak kadar büyük, tek konuda kalacak kadar küçük olmalı — paragraf bu dengede.",
     ["parcalama", "chunking", "paragraf", "olcum"]),

    ("karar", "Repo dokümanları hafızaya paragraf bazlı ve başlık önekiyle otomatik indekslenir — hafızada yalnız işaret değil metnin kendisi durur.",
     "Mert'in tespitiyle doğdu: 156 kaydın 149'u pointer'dı (kısa hüküm + dosya adresi), metin hafızada değildi — hafıza repo olmadan ölü adres yığınına dönüyordu. Çözüm: doküman katmanı (katman=dokuman) — paragraf birimi, embed girdisi 'passage: {dosya H1} › {bölüm}: {paragraf}'. Başlık öneki ECIR 2026 ölçümüyle destekli (prefix-as-text baseline'ı geçiyor) ve Anthropic Contextual Retrieval'ın sıfır-LLM-maliyetli yaklaşığı. 40 karakterden kısa blok öncekine yapışır, ardışık kısa paragraflar ~400 token'a kadar birleşir. Elle hüküm katmanı kalkmaz — iki katman tek koleksiyonda yarışır.",
     ["indeksleme", "paragraf", "baslik-oneki", "katman"]),

    ("kazanim", "Arama skorları hep 0.8 civarında kümeleniyor ve iyi/alakasız ayrımı skorla yapılamıyor — bu arıza değil mE5'in kasıtlı tasarımı; cevap-yok kararı skora değil içeriğe bakılarak verilir.",
     "İç ölçüm: doğrular 0.81-0.89, alakasız 0.776, yakın-konu tuzaklar 0.83-0.86 — bantlar örtüşüyor, eşik imkânsız. Kök sebep üreticinin kendi açıklamasında (HuggingFace intfloat/multilingual-e5-large discussions/10): InfoNCE temperature=0.01 ile eğitim skorları dar üst banda sıkıştırıyor, 'önemli olan mutlak skor değil göreli sıralama.' Sonuç kural: skor eşiğiyle 'cevap yok' denmez; tüketici agent ilk 5 sonucu OKUR ve yeterliliğe kendisi hükmeder. Günlerce eşik aramak çıkmaz sokakmış — aramayı bıraktık.",
     ["skor", "esik", "cevap-yok", "e5", "dar-bant"]),

    ("kazanim", "Kaydın metnine yazılan geçersizlik damgası aramada görünmez — arama vektöre bakar, metne yazılan uyarıyı okumaz; geçersizlik payload alanına yazılır ve filtreyle dışlanır.",
     "Ölçülmüştü: içeriğine [GEÇERSİZ] eklenen kayıt aramada yine 1. geldi. Sebep mekanik: benzerlik embedding üzerinden, damga embedding'i kayda değer değiştirmiyor. Doğru katman: payload'da durum=gecersiz + yerine=<yeni-id>; aramaya varsayılan filtre must_not durum=gecersiz (MCP fork'una küçük yama). Literatür karşılığı Zep/Graphiti invalidate-don't-delete (invalid_at edge property — yapılandırılmış alan, metin değil). 'Eskiyen doğru silinmez' kararımız doğruydu; yanlış olan damganın yeriydi.",
     ["gecersizleme", "damga", "payload", "filtre"]),

    ("kazanim", "İki kayıttan hangisinin güncel olduğu kararı LLM'e bırakılmaz — tarih/zincir alanıyla kod seçer; LLM yalnız 'aynı konuda mı' sorusuna cevap verir.",
     "arXiv 2606.01435 ('Don't Ask the LLM to Track Freshness'): bi-temporal graf altyapısı olan Zep'te bile geçerlilik kararı LLM prompt'una bırakılınca doğruluk %7; deterministik max(tarih)/zincir seçimi +10.8 puan (uzun bağlamda +21). Bizde karşılığı: yerine zinciri + tarih alanı — okuma anında 'en son supersede eden kazanır' kuralını kod uygular. Çelişki TESPİTİ LLM'e sorulabilir, çelişki ÇÖZÜMÜ sorulamaz.",
     ["celiski", "deterministik", "guncellik", "llm-karar"]),

    ("kazanim", "Doküman indeksini güncel tutmak için her değişiklikte her şeyi yeniden embed etmek gerekmez — git diff değişen dosyayı, chunk hash değişen paragrafı verir; yalnız o işlenir.",
     "LiveVectorLake deseni (arXiv 2601.05270): chunk_id=SHA256(normalize(içerik)), eski/yeni hash listeleri karşılaştırılır → yeni/değişmiş/silinmiş/aynı; %85-95 yerine %10-15 yeniden işleme. Bizde daha da ucuz: git zaten içerik-adresli — registry'de son indekslenen commit SHA tutulur, git diff --name-only <SHA> HEAD değişen dosyaları sıfır maliyetle verir. mtime'a güvenilmez (checkout/rebase bozar), içerik hash'i bozulmaz.",
     ["guncel-tutma", "git", "artimli", "hash"]),

    ("karar", "Arama kalitesinde ilk yatırım reranker olacak — mevcut TEI altyapısına ikinci instance ile bge-reranker-v2-m3; hybrid ve sorgu genişletme onun arkasında.",
     "Faz 2 kararı. Gerekçe: cross-encoder reranker literatürde en yüksek getiri (finans RAG benchmark'ında doğruluk %33.5→%49, ~120ms ek gecikme — arXiv 2511.01386); TEI /rerank endpoint'ini native sunuyor, yeni teknoloji gerekmez, model XLM-RoBERTa tabanlı çok-dilli. Uyarı (arXiv 2606.29959): reranker skoru da cevap-yok/abstain sinyali olarak kullanılamaz — konu yakınlığını skorlar, cevaplama yeterliliğini değil; eşik yasağı reranker'da da geçerli.",
     ["reranker", "faz-2", "tei", "yatirim-sirasi"]),

    ("karar", "Hükme yazmadan önce komşu kontrolü zorunlu: en yakın 5 kayıt çekilir — mükerrer varsa yazılmaz, çelişen varsa yeni yazılıp eski geçersizlenir, yoksa eklenir.",
     "Mem0'ın ADD/UPDATE/DELETE/NOOP deseninin deterministik uyarlaması (arXiv 2504.19413). Bizim ölçülmüş sorunumuzu yazma anında kesiyor: mükerrer hüküm ikizleri sıralamayı bölüyordu (iki doğru kayıt birbirinin skorunu yiyor). NOOP dalı kritik — yalnız 'ekle'si olan sistemde tekrar birikir; bir kullanıcı denetimi Mem0'ın 10.134 kaydının %97.8'ini çöp buldu (mem0 issue #4573). Karar LLM'de değil akışta: benzerlik listesi + tarih/zincir kuralı.",
     ["yazma-disiplini", "mukerrer", "noop", "komsu-kontrolu"]),

    ("kazanim", "Hafızayı otomatik damıtmaya devretmek kalite garantisi vermiyor — damıtma elle kalır; otomasyon damıtmaya değil kapsamaya (paragraf katmanı) ve denetime (komşu kontrolü) verilir.",
     "Mem0/Zep/Letta üçü de ham+damıtılmış iki katman tutuyor — mimarimizin sektör karşılığı gerçek. Fark damıtmada: onlar LLM'e otomatik çıkarttırıyor, biz agent'a bilinçli yazdırıyoruz. Otomatiğin riski ölçülü: %97.8 çöp vakası (mem0 issue #4573); LangMem'in kendi itirafı 'fazla çıkarım hassasiyeti düşürür, eksik çıkarım recall'u.' Türkçe + kurum jargonunda elle damıtma daha güvenilir salience filtresi.",
     ["damitma", "elle", "mem0", "iki-katman"]),

    ("karar", "Embedding modeli için beklenti base'e dönüş — large iki ölçümde de farkını ödetmedi; karar 164-soru setinin base koşumuyla mühürlenir.",
     "16-soru testi: base 15/15 birinci sıra, large 13/15 (iki kayıp da mükerrer ikize, modele değil). Skor marjı aynı (dar bant her ikisinde yapısal). Large maliyeti gerçek: ~3× boyut, CPU'da yavaş. Kapanış ölçümü ucuz: y-paragraf koleksiyonunu base ile yeniden kur (~900 embed), 164 soruyu koş; hit@1/hit@5 farkı anlamlı değilse TEI base'e döner. Reranker gelince ilk-aşama modelinin önemi zaten düşer. AÇIK: koşum henüz yapılmadı.",
     ["model-secimi", "base", "large", "acik-is"]),

    ("kazanim", "Kullanıcının dolaylı şikayet cümlesi ('şu tuhaf davranıyor') her kayıt yönteminde en zayıf arama tipidir — çözüm arama tarafında değil yazma tarafında: hüküm belirti diliyle yazılır.",
     "164-soru deneyi, tip kırılımı: belirti dili hit@1 0.64-0.66 (tüm yöntemlerde en düşük); anahtar kelime 0.88-0.96, İngilizce 0.83-1.00. Semantik arama, soru kaynağı adlandırmayınca zayıflıyor — model sınırı, yöntem seçimi çözmüyor. Telafi: hüküm content'i 'bunu yaşayan yarın nasıl arar' diliyle yazılır (2026-09-04 dersi bu ölçümle güçlendi); paragraf katmanı doğal dilde olduğundan kısmi kapsama verir.",
     ["belirti-dili", "arama-zayiflik", "yazma-kurali"]),

    ("karar", "Üç teknik bilinçli elendi: semantic chunking (maliyet kazancı karşılamıyor), late chunking (e5'e taşınamaz), HyDE/multi-query (reranker varken kazancı eriyor, tek-atış MCP'ye ters).",
     "Semantic: Vectara NAACL 2025 + FloTorch 2026 bağımsız 'değmez' — recall şişiyor, end-to-end düşüyor; bizim elle hüküm zaten aynı işi manuel yapıyor. Late chunking: Jina v2/v3 mimarisine özgü (token-embedding + özel pooling), mE5'e taşımak altyapı işi, kazanç uzun dokümanda — bizim parçalar kısa. HyDE/multi-query: arXiv 2511.01386 — reranking varken kazanç küçülüyor, bazı varyantlar baseline'ı geçemiyor; sorgu başına LLM turu MCP tek-atışına saniyeler ekler. Elenen ölçüsüz değil ölçülü elendi — geri açılacaksa yeni ölçümle.",
     ["elenen", "semantic-chunking", "late-chunking", "hyde"]),

    ("kazanim", "Hafıza güncelliği tartışmasında sektör 'üstüne yazma'dan 'yeni kayıt + eskiyi işaretle'ye döndü — Mem0 2026'da kendi ADD/UPDATE/DELETE yaklaşımını terk etti; bizim kararımız sektörün vardığı yerde.",
     "Mem0 blog (state-of-ai-agent-memory-2026): tek-geçişli extraction'a geçildi, kayıt artık asla üstüne yazılmıyor, güncellik kararı okuma anına ertelendi. Zep zaten invalidate-don't-delete. Tartışmalı olan silme/koruma değil, geçerliliğin NEREDE kontrol edildiği: yazma anında LLM kararı (eski Mem0 — prod'da yanlış silme vakaları, dev.to/mukesh_13) vs okuma anında filtre+deterministik kural (bizim seçim). İkincisindeyiz ve gerekçesi ölçülü.",
     ["surumleme", "sektor-yonu", "mem0", "okuma-aninda"]),
]


def embed(metinler):
    req = urllib.request.Request(
        TEI + "/v1/embeddings",
        data=json.dumps({"input": metinler,
                         "model": "intfloat/multilingual-e5-large"}).encode(),
        headers={"Authorization": f"Bearer {EKEY}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    return [x["embedding"] for x in d["data"]]


def qdrant(yol, govde, metod="PUT"):
    req = urllib.request.Request(
        QDRANT + yol, data=json.dumps(govde).encode(),
        headers={"api-key": QKEY, "Content-Type": "application/json"},
        method=metod)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


qdrant(f"/collections/{KOL}",
       {"vectors": {"size": 1024, "distance": "Cosine"}})

vektorler = embed(["passage: " + h for _, h, _, _ in KAYITLAR])
noktalar = []
for (tur, hukum, detay, etiketler), v in zip(KAYITLAR, vektorler):
    p = dict(ORTAK)
    p.update({"content": hukum, "tur": tur, "detay": detay,
              "etiketler": etiketler})
    noktalar.append({"id": str(uuid.uuid4()), "vector": v, "payload": p})

qdrant(f"/collections/{KOL}/points?wait=true", {"points": noktalar})
n = qdrant(f"/collections/{KOL}/points/count", {"exact": True}, "POST")
print(f"{KOL}: {n['result']['count']} kayıt yazıldı")
