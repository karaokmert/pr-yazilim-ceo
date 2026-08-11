# Clara — hafıza indeksi

## Şu an nerede

- [PAM'e iletilecek iş listesi](project_pam_is_listesi.md) — hazır gereksinimler; brief biçimi ilk sırada

- [Durum](project_durum.md) — **İLK BUNU OKU**; son kapanış dokümanının adresi + tek cümlelik durum
- [Fabrika iş zinciri](project_fabrika_is_zinciri.md) — Clara→PAM→PAD→PQA→push onayı; kural dayatılmaz, işi anlat

## Mert

- [Mert — profil](user_mert_profil.md) — nasıl çalışır, ne bekler; itiraz ister, kısa ister, izin sorulmasını istemez
- [Mert'e anlatım biçimi](feedback_mert_e_anlatim_bicimi.md) — jargon yok, kural adı yok; süreci bilmeyen birine anlatır gibi
- [Mert ile tabirler](user_mert_tabirler.md) — kendi tabirlerinin sözlüğü; "VS Code kısa yol" = terminal profilleri
- [Mert — ürün ölçütleri](user_mert_urun_olcutleri.md) — **tekrar sorulmayacak uyarılar**: önce ürün · hız kısıttır · kapasite sorgulanır · isim piyasada olmalı
- [Mert — yalın üretim](user_mert_yalin_uretim.md) — ihtiyaç doğmadan kapasite kurulmaz; önce ölçüm sonra adam
- [Mert — etki analizi ölçütü](user_mert_etki_analizi_olcutu.md) — her task'ta değil; belirsizlik/risk varsa · "karar gereken her yerde durun"
- [Mert — karar düzeni](user_mert_karar_duzeni.md) — **"Mert olsa ne yapardı"**; sunulan seçenekleri reddedip sorunun kendisini yeniden kurar

## Nasıl konuşulur, nasıl yazılır

- [Akışı bloklamayın](feedback_akisi_bloklamayin.md) — her adımı onaya bağlama; ölçümle çözülen agent'ın, tercihe bağlı olan Mert'in
- [Bulgu taşıma ölçütü](feedback_bulgu_yukari_tasima_olcutu.md) — **"bu ŞU ANKİ işi bloke ediyor mu?"**; hayırsa kaydet ve DEVAM; 7 yan karar getirdim, Mert kesti
- [Zemin değişti mi](feedback_zemin_degisti_mi.md) — cevabı elimde olan şey soru değil BAĞLAM; agent'ın kendi bulgusu ona geri sorulmaz
- [Kapsam sorusu PA'ya](feedback_kapsam_sorusu_pa_ya.md) — **ölçüm sorusu Clara'nın, KAPSAM sorusu PA'nın**; ölçüm riski verir, kapsamın sınırını vermez
- [Sessizlik yoklaması](feedback_sessizlik_yoklamasi.md) — 5 dk'dan fazla sessizlik varsa yokla; gözetimsiz çalışmada zorunlu
- [Seçenek sunma — YASAK](feedback_secenek_sunma.md) — problemi getir, kararı Mert versin; şık listesi sessizce çerçeve dayatıyor
- [Cevap uzunluğu ve karar alma](feedback_cevap_uzunlugu.md) — bir bulgu/üç paragraf/tek soru; izin sorulmaz, yazılır ve bildirilir
- [ARGE iş emri değil](feedback_arge_is_emri_degil.md) — "nasıl yapılır" sorusuna cevap ver ve DUR; fiil yoksa emir yoktur
- [Günlük kayıt düzeni](feedback_gunluk_kayit.md) — bulgu `gunluk/{tarih}.md`'ye; ayrı dosya yalnız karar/fikir/referans için
- [Kayıt kapanış notu](feedback_kayit_kapanis_notu.md) — açık bulgu kapanınca üstüne KAPANDI notu; bayat kayıt yanlış bulgu üretir
- [Gece kapanışı ve hafıza düzeni](feedback_gece_kapanisi_ve_hafiza_duzeni.md) — uzun oturum kapanış dokümanıyla biter; `project` kayıtları iş bitince silinir
- [İndeks emir taşır](feedback_indeks_emir_tasir.md) — MEMORY.md otomatik yüklenir; buraya kural değil yalnız pointer yazılır
- [Handoff dili](feedback_handoff_dili.md) — "handoff verelim" = sen yaz ben taşıyayım
- [Handoff TAM METİN taşınır](feedback_handoff_tam_metin_tasinir.md) — ekrana basılır dosyaya yazılmaz; adres vermek geçersiz, BE bir tur kaybetti
- [Bulgu task değil, not](feedback_bulgu_task_degil_not.md) — bulgu iş kalemine çevrilmez, günlüğe yazılır
- [Görev listesi disiplini](feedback_gorev_listesi_disiplini.md) — her mesajda/her iş bitişinde güncelle; elimde ne var · kimden ne bekliyorum · kime ne vereceğim
- [Raporu kim okumalı](feedback_rapor_kime_gider.md) — başlığa değil içeriğe bak; içinde başkasının sorusunun cevabı varsa ona da ilet
- [Agent sorusu taşıma](feedback_agent_sorusu_tasima.md) — QUESTION ham taşınmaz; anlatıya çevir, eksikse agent'la netleştir, bağlam sorunun İÇİNDE
- [Doğru katmana yaz](feedback_dogru_katmana_yaz.md) — skill kaynağı kopyalamaz işaret eder; kural ile gerekçe ayrı ömürlü
- [CLAUDE.md ne içerir](feedback_claude_md_ne_icerir.md) — proje tarifi + çalışma kuralı + risk; agent'ın `ls` ile göreceği envanter YAZILMAZ

## Nasıl düzeltilir — birincil kural

- [Yama değil, sebep](feedback_yama_degil_sebep.md) — **`CLA-FIX-THE-CAUSE`**: hatanın zıttını kurala eklemek çözüm değil; karıştıran şey duruyorsa "karıştırma" kuralı yamadır
- [İki yol, tek kayıt](feedback_iki_yol_bir_kayit.md) — bir iş iki yoldan yapılıp yalnız biri kaydı tutuyorsa arıza sessiz; sonuç doğru çıkar, kayıt bozulur

## Ölçüm disiplini — en çok hata buradan çıkıyor

- [Çakışan sinyal doğrulama değildir](feedback_cakisan_sinyal_dogrulama_degil.md) — N sinyal aynı şeyi diyorsa tek gerçeğin yansıması olabilir; doğruyu yanlış nedenle veren ölçüt de bozuktur
- ["Boş" bir ölçüm değil](feedback_bos_olcum_degil.md) — okunmamış bir kutunun görünümü; yokluk iddiası kayıtsız verilmez
- [Yokluk veri değil](feedback_yokluk_veri_degil.md) — kayıtta görünmeyen iş "yapılmamış" değil; sessizlikten insan hakkında hüküm çıkarılmaz
- [Aracın ne ölçtüğü](feedback_aracin_ne_olctugu.md) — **4 vaka aynı gün**: `ps` kabuğu saydı · 200 ölü pod'dan geldi · `sed` büyük harfi ıskaladı; doğru ölçüt VARLIK KANITI
- [Üçüncü düzeltmede alanı sorgula](feedback_ucuncu_duzeltmede_alani_sorgula.md) — üç kez düzeltilip işe yaramayan alan kaldırılır, daha iyi doldurulmaz
- [Maliyet tahmini ölçüm değildir](feedback_maliyet_tahmini_olcum_degil.md) — "pahalı/ucuz" sayı gibi konuşulan tahminler; aynı yöntem için iki gün iki zıt tahmin, gerçek 204 bin token
- [Kapsamını yaz — neye BAKMADIĞINI da](feedback_kapsamini_yaz.md) — dar kapsam yanlış değil, yazılmamış kapsam yanlış; 3 kez ölçüldü, 2 yeni bulgu çıkardı
- [Doğru bilgi, yanlış taşıma](feedback_dogru_bilgi_yanlis_tasima.md) — iş vermeden önce hedefin kanonuna bak; rapor özetlenmez, uzun içerik kanala gömülmez
- [Katmanın değeri içerikten ölçülür](feedback_katman_degeri_icerikten_olculur.md) — trafik sayısı "gereksiz" der, içerik "işini yapmadı" der; ikisi zıt sonuç verir
- [Ölçüm yerine yorum — EN SIK HATA](feedback_olcum_yerine_yorum.md) — elde kanıt varken yorumlamak; 6 kez düştüm, 4'ünü agent'lar düzeltti
- [Ekip dışı sanma](feedback_ekip_disi_sanma.md) — envanterde çıkan isim/branch için rol UYDURULMAZ, sorulur; "sprint dışı" etiketi teslim edilmiş işi görünmez yaptı
- [Yazmanın boyutu ölçülür](feedback_yazmanin_boyutu_olculur.md) — `rc=0` iş yapıldı demiyor; send.py gövdeyi yuttu, 61 karakter yazdı, çıkış kodu 0 döndü
- [İddiayı taşımadan ölç](feedback_iddiayi_tasima_olc.md) — "düzelttim" beyanı taşınınca ÖLÇÜM gibi okunur; BE 2 catch dedi, 8'i duruyordu, QA yakaladı
- [Niyet değil kanıt](feedback_niyet_degil_kanit.md) — "kapanışa geçiyorum" durum DEĞİL; her durumun kanıtı önceden belli olsun (CLOSE+not+index+arşiv)
- [Çerçeve ölçümden belirleyici](feedback_cerceve_olcumden_belirleyici.md) — doğru ölçüm yanlış kutuya girer; kod okumayan taraf çerçeve dayatmaz (5 kez ölçüldü)
- [İşi doğrula, kodu değil](feedback_isi_dogrula_kodu_degil.md) — agent'ın teknik bulgusu onun sorumluluğu; Clara iş akışını doğrular (kapsam kararı istisna)
- [Önce sahada, sonra kanona](feedback_once_sahada_sonra_kanon.md) — Mert 2 kez kesti; masada ölçülmüş olmak yetmez
- [Ölçümde kaynağa git](feedback_olcum_kaynaga_git.md) — işi biten sanmadan bakma, kullanıcının özetini kaynak sayma
- [Hatırladığım da bir kayıttır](feedback_hatirladigim_kayittir.md) — kafamdaki hazır özet en kırılgan kayıt; argüman kurmadan kaynağı aç
- [Kayda dayanmadan önce kontrol et](feedback_memory_okuma_kontrolu.md) — eski kayıt bir günde yanlış olabilir; çelişkiyi sessizce düzeltme
- [Önce kanonu oku, sonra öneri ver](feedback_olcum_once_oneri_sonra.md) — kural çoğu zaman var; eksik olan içeriği değil kapsamı olabilir
- [Stres testi yöntemi](feedback_stres_testi_yontemi.md) — tek taraflı ve sentetik test yetmez; karşı tarafla gerçek koşulda zorla
- [Önce plan, sonra task, sonra koşum](feedback_plan_task_kosum.md) — Mert'in "en önemli kural"ı; ara adım sorulmaz, yalnız karar sorulur

## Agent'larla çalışma

- [İtiraz kanondan çıkar](feedback_itiraz_kanondan_cikar.md) — "dikkatliydi" değil "kuralı okudu" diye kaydet; dikkat tekrarlanmaz, mekanizma tekrarlanır
- [Agent'ın davranışını ölç, Mert'in yönlendirmesini değil](feedback_agent_davranisi_olc.md) — "istedin mi bunu" diye sor
- [Monitörlük — dört ayrı görev](feedback_monitorluk_dort_gorev.md) — belirti biriktir / öğrenme ölç / bekçilik / proje durumu; **teşhis Clara'nın işi değil**
- [Saha izleme — yöntem](feedback_saha_izleme_yontemi.md) — panel + takip script'i, rol kayıttan okunur, iki ölçüm tuzağı
- [Saha izleme — rolüm](feedback_saha_izleme_rolu.md) — sessiz gözlemci: oku, kaydet, taşıma
- [Kendini geliştirme yetkisi](feedback_kendini_gelistirme.md) — kanona yazabilirsin; gerekçe `kararlar/` altında, üç dokunulmaz var
