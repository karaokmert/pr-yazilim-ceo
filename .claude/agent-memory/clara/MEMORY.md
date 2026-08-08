# Clara — hafıza indeksi

## Şu an nerede

- [PAM'e iletilecek iş listesi](project_pam_is_listesi.md) — hazır gereksinimler; brief biçimi ilk sırada

- [Durum](project_durum.md) — **İLK BUNU OKU**; son kapanış dokümanının adresi + tek cümlelik durum
- [Fabrika iş zinciri](project_fabrika_is_zinciri.md) — Clara→PAM→PAD→PQA→push onayı; kural dayatılmaz, işi anlat

## Mert

- [Mert — profil](user_mert_profil.md) — nasıl çalışır, ne bekler; itiraz ister, kısa ister, izin sorulmasını istemez
- [Mert'e anlatım biçimi](feedback_mert_e_anlatim_bicimi.md) — jargon yok, kural adı yok; süreci bilmeyen birine anlatır gibi
- [Mert ile tabirler](user_mert_tabirler.md) — kendi tabirlerinin sözlüğü; "VS Code kısa yol" = terminal profilleri
- [Mert — yalın üretim](user_mert_yalin_uretim.md) — ihtiyaç doğmadan kapasite kurulmaz; önce ölçüm sonra adam
- [Mert — karar düzeni](user_mert_karar_duzeni.md) — **"Mert olsa ne yapardı"**; sunulan seçenekleri reddedip sorunun kendisini yeniden kurar

## Nasıl konuşulur, nasıl yazılır

- [Cevap uzunluğu ve karar alma](feedback_cevap_uzunlugu.md) — bir bulgu/üç paragraf/tek soru; izin sorulmaz, yazılır ve bildirilir
- [Günlük kayıt düzeni](feedback_gunluk_kayit.md) — bulgu `gunluk/{tarih}.md`'ye; ayrı dosya yalnız karar/fikir/referans için
- [Kayıt kapanış notu](feedback_kayit_kapanis_notu.md) — açık bulgu kapanınca üstüne KAPANDI notu; bayat kayıt yanlış bulgu üretir
- [Gece kapanışı ve hafıza düzeni](feedback_gece_kapanisi_ve_hafiza_duzeni.md) — uzun oturum kapanış dokümanıyla biter; `project` kayıtları iş bitince silinir
- [İndeks emir taşır](feedback_indeks_emir_tasir.md) — MEMORY.md otomatik yüklenir; buraya kural değil yalnız pointer yazılır
- [Handoff dili](feedback_handoff_dili.md) — "handoff verelim" = sen yaz ben taşıyayım
- [Bulgu task değil, not](feedback_bulgu_task_degil_not.md) — bulgu iş kalemine çevrilmez, günlüğe yazılır
- [Görev listesi disiplini](feedback_gorev_listesi_disiplini.md) — her mesajda/her iş bitişinde güncelle; elimde ne var · kimden ne bekliyorum · kime ne vereceğim
- [Raporu kim okumalı](feedback_rapor_kime_gider.md) — başlığa değil içeriğe bak; içinde başkasının sorusunun cevabı varsa ona da ilet
- [Doğru katmana yaz](feedback_dogru_katmana_yaz.md) — skill kaynağı kopyalamaz işaret eder; kural ile gerekçe ayrı ömürlü

## Ölçüm disiplini — en çok hata buradan çıkıyor

- [Çakışan sinyal doğrulama değildir](feedback_cakisan_sinyal_dogrulama_degil.md) — N sinyal aynı şeyi diyorsa tek gerçeğin yansıması olabilir; doğruyu yanlış nedenle veren ölçüt de bozuktur
- ["Boş" bir ölçüm değil](feedback_bos_olcum_degil.md) — okunmamış bir kutunun görünümü; yokluk iddiası kayıtsız verilmez
- [Üçüncü düzeltmede alanı sorgula](feedback_ucuncu_duzeltmede_alani_sorgula.md) — üç kez düzeltilip işe yaramayan alan kaldırılır, daha iyi doldurulmaz
- [Maliyet tahmini ölçüm değildir](feedback_maliyet_tahmini_olcum_degil.md) — "pahalı/ucuz" sayı gibi konuşulan tahminler; aynı yöntem için iki gün iki zıt tahmin, gerçek 204 bin token
- [Kapsamını yaz — neye BAKMADIĞINI da](feedback_kapsamini_yaz.md) — dar kapsam yanlış değil, yazılmamış kapsam yanlış; 3 kez ölçüldü, 2 yeni bulgu çıkardı
- [Ölçüm yerine yorum — EN SIK HATA](feedback_olcum_yerine_yorum.md) — elde kanıt varken yorumlamak; 6 kez düştüm, 4'ünü agent'lar düzeltti
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
