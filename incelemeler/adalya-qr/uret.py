#!/usr/bin/env python3
"""
Adalya Tobacco — link sayfası QR kodu üretici.

Statik QR: hedef adres karenin İÇİNE gömülüdür. Hiçbir aracı servise
bağımlı değildir, dolayısıyla ölmesi mümkün değildir. Yönlendirme
esnekliği QR'da değil, hedef sayfanın kendisinde yaşar.

Bağımlılık: segno (saf Python, başka hiçbir şey gerektirmez)
    python3 -m pip install --user segno

Çalıştırma:
    python3 uret.py
"""

import segno

# --- Kareye gömülen içerik. DEĞİŞTİRİLEMEZ KARAR ---
# Basılmış her QR bu adresi taşır. Sonradan değiştirmek, basılı
# tüm materyalin yenilenmesi anlamına gelir. Hedefi değiştirmek
# gerektiğinde QR'a değil, bu adresin gösterdiği sayfaya dokunulur.
HEDEF = "https://links.adalyatobacco.com"

# --- Hata düzeltme seviyesi ---
# H = %30. Karenin %30'u hasar görse (çizik, leke, ıslanma, üstüne
# etiket) hâlâ okunur. Baskıya giden iş için tek doğru seçim.
HATA_DUZELTME = "h"

# --- Sessiz alan (quiet zone) ---
# Karenin etrafındaki boş çerçeve, modül cinsinden. Standart minimum 4.
# Bunu kısmak tarayıcıların kareyi bulmasını engeller — matbaanın
# "boşluk çok, kırpalım" teklifi buradan reddedilir.
SESSIZ_ALAN = 4

# --- Üretilecek dosyalar ---
# scale: SVG'de birim büyüklüğü (vektör olduğu için sonsuz ölçeklenir,
#        değer sadece dosyadaki koordinat ölçeğini belirler)
#        PNG'de piksel/modül — nihai çözünürlüğü belirler.
CIKTILAR = [
    # Baskı için: vektör. Matbaanın istediği format budur.
    ("adalya-qr-baski.svg", {"scale": 10}),

    # Matbaa PDF isterse: aynı vektör veri, PDF kabında.
    # Boyut noktadan (1/72 inç) hesaplanır: scale 28.35 ≈ 1 cm/modül
    # değil — 33 modül x 8.5pt ≈ 280pt ≈ 9.9 cm kenar (sessiz alan dahil).
    ("adalya-qr-baski.pdf", {"scale": 8.5}),

    # Ekran/dijital için: yüksek çözünürlüklü raster.
    # 33 modül x 30px + sessiz alan ≈ 1230px — Instagram, WhatsApp,
    # e-posta imzası, sunum için fazlasıyla yeterli.
    ("adalya-qr-dijital.png", {"scale": 30}),

    # Küçük baskıda (etiket, kartvizit) matbaa PNG istiyorsa diye
    # 300 DPI'da ~2.5cm karşılığı yüksek çözünürlük.
    ("adalya-qr-baski-yuksek.png", {"scale": 90}),
]


def main() -> None:
    qr = segno.make_qr(HEDEF, error=HATA_DUZELTME)

    print(f"Hedef      : {HEDEF}")
    print(f"Sürüm      : {qr.version} ({qr.symbol_size(border=0)[0]} x "
          f"{qr.symbol_size(border=0)[1]} modül)")
    print(f"Hata düzelt: {qr.error.upper()} (%30 hasara dayanıklı)")
    print(f"Sessiz alan: {SESSIZ_ALAN} modül")
    print()

    for dosya, ayar in CIKTILAR:
        qr.save(
            dosya,
            border=SESSIZ_ALAN,
            dark="black",
            light="white",
            **ayar,
        )
        genislik = qr.symbol_size(scale=ayar["scale"], border=SESSIZ_ALAN)[0]
        print(f"  {dosya:32s}  {genislik} birim/px")

    print()
    print("Doğrulama: üretilen dosyayı telefonla tara, adres birebir")
    print("eşleşiyor mu diye kontrol et. Bu adım atlanamaz.")


if __name__ == "__main__":
    main()
