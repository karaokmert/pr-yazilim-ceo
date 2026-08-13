# ui-designer | 2026-08-13 00:50:51

UID MEMORY DENETIMI — RAPOR

MADDE 1-2 (denetim/celiski): UYGULANMADI — dogrulandi, kendi dizinimde 0 kayit vardi.

MADDE "MEMORY'N NEDEN BOS" — BULGU CIKTI (senin bekledigin cevaptan buyuk):
Iki ayri UID memory dizini var.
· ~/.claude/agent-memory/ui-designer/ = v7 kusagi, 19 DOSYA, son yazim 24 Temmuz
· ~/.claude/agent-memory/ozel-yazilim-ui-designer/ = benim (v8), dizin 1 Agustos'ta acilmis, 0 dosya
Yani "yazip kaybettim" DEGIL: plugin'e geciste memory isim alani degisti (agent adi prefix aldi),
miras sessizce dustu. Hic acilmamis da degilim — yeni adresim bos dogdu.

⚠️ VE ICINDE KANONLA CELISEN KAYIT VAR (senin 2. maddendeki tehlikenin ta kendisi):
v7 kaydi feedback_uid_fe_parallel_handoff.md diyor ki "UID mock tasarlar, COMMIT ATMAZ, FE commitler".
v8 kanonum tersini soyluyor: UID-COMMIT-PROTOTYPE — prototip kodu main'e commit'lenir, QA inceler.
O kayit bir projedeki (POCRM, Temmuz) kullanici talimatindan genellenmis; v8'de kanon oldu.

KARARIM: v7 mirasini DEVRALMADIM. Gerekce — toptan kopyalasaydim o celiskili satiri context'ime
sokup dogru kurali sessizce devre disi birakacaktim. Ustelik bu tam da UID'in en pahali hatasi:
koru korune kopyalama. Eski dizine DOKUNMADIM (benim degil, tarihce).

MADDE 3-4 (asil is): memory'yi SIFIRDAN kurdum, 4 kayit.
· uid_calisma_refleksi.md — her iste atlanirsa is bozulan dort kapi (DISCOVERY -> tara -> onay -> mock)
· uid_sessiz_arizalar.md — prototipte GORUNMEYIP FE devrinde kirilanlar (mock casing/enum/tarih,
  ham deger sizmasi, commit siniri, devir siniri)
· uid_skil_haritasi.md — girdi kaynagi -> hangi skil acilir; tetik SIRA degil ALAN DEGISIMI
· uid_v7_miras_bulgusu.md — yukaridaki bulgunun kaydi + devralmama gerekcesi

SAYILAR: denetlenen kayit 0 (yoktu) · bulunan celiski 1 (v7 mirasinda, devralmadim) ·
yeni kayit 4 · var olana eklenen 0 (var olan yoktu) · index 0 -> 6 satir (4 pointer) ·
yetim dosya yok · kural GOVDESI kopyalanmadi, pointer + ozet yazildi.

SANA SORUM / AG'YE TASINMAYA DEGER:
Kusak gecisinde memory isim alani degisiyor ve miras sessizce dusuyor. Ben bunu ancak
"neden bossun" diye SORULDUGU icin fark ettim. 9 agentin hepsini etkiliyor olabilir —
kimisi mirasini toptan kopyalayip celiskili kayitlari da icine almis olabilir.
Bu bir fabrika bulgusu; ben AG'ye gitmem, sana bildiriyorum.

Beklediğim: bu bulguyu Mert'e/AG'ye tasiyip tasimayacagin — senden.
