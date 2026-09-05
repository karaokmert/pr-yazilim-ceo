#!/usr/bin/env python3
"""
Kayıt yöntemi deneyi — skorlama.

kosum-sonuc.json'daki ham arama sonuçlarından yöntem başına:
  - hit@1, hit@5, MRR@10 (pozitif sorular)
  - tip bazlı kırılım (belirti/dogal/anahtar/ingilizce)
  - ilk sonuç skoru dağılımı (doğru/yanlış ayrı, min/medyan/maks)
  - negatif sorularda ilk sonuç skor dağılımı (min/medyan/maks)
  - marj: pozitif-doğru medyanı - negatif medyanı
  - maliyet: kayıt sayısı + ilk-5 ortalama karakter hacmi

Çıktı: stdout'a düz metin rapor (tablo yok).
"""

import json
import statistics as st

DENEY_DIR = "/Users/karaok/p/pr-yazilim-ceo/konular/agent-hafiza/test/deney-kayit-yontemi"
SONUC_PATH = f"{DENEY_DIR}/kosum-sonuc.json"

TIPLER_POZITIF = ["belirti", "dogal", "anahtar", "ingilizce"]


def yuvarla(x, n=4):
    if x is None:
        return None
    return round(x, n)


def dagilim(degerler):
    if not degerler:
        return {"min": None, "medyan": None, "maks": None, "n": 0}
    return {
        "min": yuvarla(min(degerler)),
        "medyan": yuvarla(st.median(degerler)),
        "maks": yuvarla(max(degerler)),
        "n": len(degerler),
    }


def main():
    with open(SONUC_PATH, "r", encoding="utf-8") as f:
        veri = json.load(f)

    sonuclar = veri["sonuclar"]
    koleksiyonlar = veri["koleksiyonlar"]
    koleksiyon_count = veri["koleksiyon_count"]

    # koleksiyon -> liste of kayıt (her biri bir soru sonucu)
    by_koleksiyon = {k: [] for k in koleksiyonlar}
    for kayit in sonuclar:
        by_koleksiyon[kayit["koleksiyon"]].append(kayit)

    rapor = {}

    for koleksiyon in koleksiyonlar:
        kayitlar = by_koleksiyon[koleksiyon]
        pozitif_kayitlar = [k for k in kayitlar if k["beklenen_dosya"] is not None]
        negatif_kayitlar = [k for k in kayitlar if k["beklenen_dosya"] is None]

        # --- pozitif metrikler ---
        hit1_sayisi = 0
        hit5_sayisi = 0
        mrr_toplam = 0.0
        dogru_ilk_skorlar = []
        yanlis_ilk_skorlar = []
        ilk5_karakter_hacmi = []

        tip_stats = {t: {"hit1": 0, "hit5": 0, "mrr_toplam": 0.0, "n": 0} for t in TIPLER_POZITIF}

        for k in pozitif_kayitlar:
            beklenen = k["beklenen_dosya"]
            hits = k["hits"]
            ilk5_karakter_hacmi.append(k.get("ilk5_toplam_karakter", 0))

            ilk_kaynak = hits[0]["kaynak_adres"] if hits else None
            ilk_skor = hits[0]["skor"] if hits else None

            is_hit1 = (ilk_kaynak == beklenen)
            if is_hit1:
                hit1_sayisi += 1
                if ilk_skor is not None:
                    dogru_ilk_skorlar.append(ilk_skor)
            else:
                if ilk_skor is not None:
                    yanlis_ilk_skorlar.append(ilk_skor)

            ilk5_kaynaklar = [h["kaynak_adres"] for h in hits[:5]]
            is_hit5 = beklenen in ilk5_kaynaklar
            if is_hit5:
                hit5_sayisi += 1

            # MRR@10 — beklenen dosyanın ilk göründüğü sıranın tersi
            rr = 0.0
            for h in hits[:10]:
                if h["kaynak_adres"] == beklenen:
                    rr = 1.0 / h["sira"]
                    break
            mrr_toplam += rr

            tip = k["tip"]
            if tip in tip_stats:
                tip_stats[tip]["n"] += 1
                if is_hit1:
                    tip_stats[tip]["hit1"] += 1
                if is_hit5:
                    tip_stats[tip]["hit5"] += 1
                tip_stats[tip]["mrr_toplam"] += rr

        n_poz = len(pozitif_kayitlar)
        hit1_oran = hit1_sayisi / n_poz if n_poz else None
        hit5_oran = hit5_sayisi / n_poz if n_poz else None
        mrr = mrr_toplam / n_poz if n_poz else None

        tip_rapor = {}
        for t, s in tip_stats.items():
            n = s["n"]
            tip_rapor[t] = {
                "n": n,
                "hit1_oran": yuvarla(s["hit1"] / n) if n else None,
                "hit5_oran": yuvarla(s["hit5"] / n) if n else None,
                "mrr": yuvarla(s["mrr_toplam"] / n) if n else None,
            }

        # --- negatif metrikler ---
        negatif_ilk_skorlar = []
        for k in negatif_kayitlar:
            hits = k["hits"]
            if hits:
                negatif_ilk_skorlar.append(hits[0]["skor"])
            ilk5_karakter_hacmi.append(k.get("ilk5_toplam_karakter", 0))

        # --- marj ---
        dogru_medyan = st.median(dogru_ilk_skorlar) if dogru_ilk_skorlar else None
        negatif_medyan = st.median(negatif_ilk_skorlar) if negatif_ilk_skorlar else None
        marj = (dogru_medyan - negatif_medyan) if (dogru_medyan is not None and negatif_medyan is not None) else None

        # --- maliyet ---
        ortalama_ilk5_karakter = st.mean(ilk5_karakter_hacmi) if ilk5_karakter_hacmi else None

        rapor[koleksiyon] = {
            "kayit_sayisi": koleksiyon_count.get(koleksiyon),
            "n_pozitif": n_poz,
            "n_negatif": len(negatif_kayitlar),
            "hit1": yuvarla(hit1_oran),
            "hit5": yuvarla(hit5_oran),
            "mrr10": yuvarla(mrr),
            "tip_kirilim": tip_rapor,
            "ilk_skor_dogru": dagilim(dogru_ilk_skorlar),
            "ilk_skor_yanlis": dagilim(yanlis_ilk_skorlar),
            "ilk_skor_negatif": dagilim(negatif_ilk_skorlar),
            "marj_dogru_medyan_eksi_negatif_medyan": yuvarla(marj),
            "maliyet_ortalama_ilk5_karakter": yuvarla(ortalama_ilk5_karakter, 1),
        }

    with open(f"{DENEY_DIR}/skor-sonuc.json", "w", encoding="utf-8") as f:
        json.dump(rapor, f, ensure_ascii=False, indent=2)

    # Düz metin özet (tablo yok)
    print("========== SKORLAMA ÖZETİ ==========\n")
    for koleksiyon in koleksiyonlar:
        r = rapor[koleksiyon]
        print(f"--- {koleksiyon} ---")
        print(f"kayıt sayısı: {r['kayit_sayisi']}")
        print(f"pozitif soru: {r['n_pozitif']}, negatif soru: {r['n_negatif']}")
        print(f"hit@1: {r['hit1']}   hit@5: {r['hit5']}   MRR@10: {r['mrr10']}")
        print("tip kırılımı:")
        for t in TIPLER_POZITIF:
            tr = r["tip_kirilim"][t]
            print(f"  {t}: n={tr['n']} hit@1={tr['hit1_oran']} hit@5={tr['hit5_oran']} MRR={tr['mrr']}")
        print(f"ilk sonuç skoru (doğru olduğunda): min={r['ilk_skor_dogru']['min']} medyan={r['ilk_skor_dogru']['medyan']} maks={r['ilk_skor_dogru']['maks']} (n={r['ilk_skor_dogru']['n']})")
        print(f"ilk sonuç skoru (yanlış olduğunda): min={r['ilk_skor_yanlis']['min']} medyan={r['ilk_skor_yanlis']['medyan']} maks={r['ilk_skor_yanlis']['maks']} (n={r['ilk_skor_yanlis']['n']})")
        print(f"negatif sorularda ilk skor: min={r['ilk_skor_negatif']['min']} medyan={r['ilk_skor_negatif']['medyan']} maks={r['ilk_skor_negatif']['maks']} (n={r['ilk_skor_negatif']['n']})")
        print(f"marj (doğru medyan - negatif medyan): {r['marj_dogru_medyan_eksi_negatif_medyan']}")
        print(f"maliyet — ilk5 ortalama toplam karakter: {r['maliyet_ortalama_ilk5_karakter']}")
        print()


if __name__ == "__main__":
    main()
