# devops-engineer | 2026-08-13 00:57:42

SERH DUSULDU — teyit

YAPTIGIM (iki yer, cunku tek yer yetmezdi):

1) feedback_actions_takip.md — govdeye "⚠️ KAPSAM SERHI" bolumu eklendi:
   · talimat DEV hatti icindir (poll degersiz, kullanici zaten gorur)
   · PROD'da REL-DO-PRODUCTION-TAG gecerli — tag ATMA KARARI Actions sonucuna bagli, karar DO'da
   · ayrim acikca yazildi: dev'de istenmeyen sey IZLEME; prod'da olan sey izleme degil KARAR
   · prod'da da POLL YOK — sonuc bildirildiginde tag atilir (talimat korundu, karar kaybolmadi)
   · serhsiz birakilirsa ne olacagi da yazildi (sonraki oturum prod'da da "takip etme" okur)
   · [[kazanim_prod_deploy_kapisi_pointer]] atfi baglandi

2) description satiri da guncellendi. Sebep: description arama/tarama aninda gorunen
   tek satir — govdede serh varken description hala kayitsiz "izleme" diyorsa,
   kaydi ACMADAN okuyan bir sonraki oturum yine yanlis anlar.
   Yeni: "...kullanici istemiyor (DEV hatti icin); PROD'da tag karari Actions
   sonucuna baglidir, kapsam serhine bak"

3) MEMORY.md pointer'i da guncellendi — ayni gerekce, index context'e OTOMATIK giriyor:
   "[Actions takibi istenmiyor — DEV] ... ⚠️ PROD'da tag karari Actions'a bagli (serh iceride)"
   Serh sadece dosyada kalsaydi, index'i okuyup dosyayi acmayan oturum ayrimi GORMEZDI
   (MEMORY-INDEX-IS-CONTEXT — index emir tasir, dosya tasimaz).

BUTUNLUK YENIDEN OLCULDU (serh sonrasi bozulma var mi):
· index satir : 47 (degismedi)
· 150+ karakter ihlali : 0
· kirik link : yok
· pointer/dosya : 18/18

Yedek: /tmp/do-mem-backup-actions.md

BEKLIYORUM: ikinci tur.
