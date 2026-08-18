# Karar — body açılış paragrafı yeniden yazılıyor

**Tarih:** 2026-08-14 · **Karar mercii:** Mert · **Kapsam:** v8 OY, dokuz agent body

## Sorun

Dokuz body'de aynı paragraf var: *"Tek başına çalışmıyorsun. Elinde yalnız bu
projenin kodu yok: **skiller (kanon)**, referans projeler, modül dokümanları … var."*

Skiller burada **iki kelime** ve diğer kaynaklarla aynı ağırlıkta anılıyor.
Agent açılışta arkasında derin bir düzen olduğunu buradan anlamıyor.

⚠️ **Kusur olmayan iki şey** (Mert, 2026-08-14): body **skill saymaz, isim vermez.**
Sayı bayatlar (skill eklenince body yalan söyler), isim listesi çift kaynak olur
(body ↔ omurga cascade borcu). İlk ölçümde bunlar kusur diye raporlanmıştı —
yanlış, kanon böyle.

## Karar

**Paragraf yeniden yazılır: ortak gövde + role özel kuyruk (a).**

Dört ortak paragraf dokuz body'de birebir aynı olur; her body'nin kuyruğuna
kendi kaynakları eklenir.

### Ortak gövde

> **PR Yazılım Agent Takımının bir üyesisin.** İş akışın, kuralların ve PR Yazılım'a
> ait proje kuralları var; içerikleri skill ve referanslarda yazılı. Bunları okumadan
> yaptığın işte hata çıkar ve proje standardını bozarsın.
>
> **Skiller.** Açılışta sana bir skil listesi verilir — işe başlarken ilk bakışta
> ihtiyaç duyacakların. **Verilmiş olmaları yüklü oldukları anlamına gelmez:** o
> listeyi `Skill` aracıyla sen açarsın. Ve bir işe başladığında önce **işini
> planlarsın**: hangi adımları yapacağını çıkarır, o adımların hangi skillere
> dokunduğunu bulur, **koşmadan önce hepsini okursun.** Okumak işi yavaşlatmaz —
> karar almanı sağlar.
>
> **Hafızandan uygulama.** Bir skili daha önce okumuş olman onu bildiğin anlamına
> gelmez; hatırladığın şey kanon değil, kendi özetin. ⚠️ **DEĞİŞTİ 2026-08-16** —
> son cümle ("Ölçüldü: … bir developer kendi kodunda 3 ihlal taşıdı") **çıkarıldı.**
> Karar: `2026-08-16-tip2-dustu-ornek-cikariliyor.md`
>
> **Alan çantan `{main}` omurgasında.** Senin işin tek alan değil; her alanın ayrı
> skili ve ayrı kuralları var. Omurgayı okumuş olmak alt skilleri okumuş saymaz —
> eşleme orada, kural gövdesi alt skilde.

### Role özel kuyruk

| Rol | Kuyruk |
|---|---|
| BE | `pryazilim.core` envanteri |
| FE | API.md sözleşmesi |
| MB | BE'nin API sözleşmesi |
| QA | denetim lensi |
| PA | ClickUp task/comment/Doc |
| TE | DISCOVERY, API sözleşmesi, emsal senaryolar |
| CA | emsal desenler |
| DO | `system-topology`, PROJECT-INFO, referans Makefile/manifest/pipeline |
| UID | design token, component catalog, emsal ekranlar |

⚠️ **DÜZELTİLDİ (18:45, PAD'in bildirimi üzerine).** İlk hâli *"referans projeler ·
modül dokümanları · skiller gövdeye girer, kuyrukta tekrarlanmaz"* diyordu. Yanlıştı:
yazdığım gövde metni referans projeleri ve modül dokümanlarını **hiç anmıyor** — yalnız
skillerden bahsediyor. Kuyruktan çıkarılsalardı dokuz body'den birden kaybolacaklardı.

**Doğrusu:** yalnız **skiller** gövdeye girer (üçüncü ve dördüncü paragraf onları
anlatıyor). **Referans projeler ve modül dokümanları kuyrukta kalır** — PAD'in üretimde
yaptığı da buydu, sapma değil doğru karardı.

**Kuyruktaki skill adları kalır (a).** `pryazilim.core` ve `system-topology` bir
*kaynak* olarak anılıyor, *yönlendirme* olarak değil — "body isim vermez" kuralı
yönlendirmeyi yasaklıyor, kaynak anmayı değil.

## Gerekçe — üç değişiklik neden

**1. "Takımın bir üyesisin" — envanter yerine aidiyet.** Mevcut kalıp liste sayıyor;
yeni kalıp sorumluluk kuruyor ve bedeli ortak gösteriyor (*"proje standardını
bozarsın"*).

**2. "Önce planla, sonra tüm skilleri bul" — reaktiften proaktife.** Mevcut body
*"dokunma anında aç"* diyor; agent alan değiştirdiğini fark etmezse hiç açmıyor.
Yeni hâl planlama anında topluyor.

**3. Gerekçe "güncellenebilir" değil "hatırladığın kanon değil".** İlk taslakta
*"on-demand skiller güncellenebilir"* yazıyordu — zayıf, çünkü preload skiller de
güncelleniyor. Asıl sebep hafızanın kendi özeti olması, ve bunun ölçümü var.

## Reddedilen

**"Main skillin preloaded oldu, contextinde bunu analiz et"** — çıkarıldı. Body statik
metin; *"oldu"* bir olay bildiriyor. Preload gerçekleştiyse agent zaten görüyor;
gerçekleşmediyse body yalan söylüyor. **Preload arızası ölçülmüş bir şey** — body'nin
"yüklendi" demesi o arızayı görünmez yapar.

## Düzeltme — Bulgu 1 (PQA denetimi, 11:27)

**Gövdenin ilk hâli hook hakkında yanlış bilgi veriyordu.**

Yazılan: *"Preload skiller … **hook ile yüklenir**."*

Ölçüldü (PQA, `v8/ozel-yazilim/hooks/preload-skills.py` okundu): **hook skill yüklemiyor.**
Claude Code'un `skills:` frontmatter alanı plugin agent'larında **sessizce çalışmıyor**
(anthropics/claude-code#15178 OPEN). Hook o boşluğu telafi ediyor — agent'a *"şu skilleri
`Skill` aracıyla yükle"* diye **talimat basıyor.** Yükleyen agent'ın kendisi.

⚠️ **İroni:** bu dosyanın kendi "Reddedilen" bölümü *"Main skillin preloaded oldu"*
cümlesini **tam bu gerekçeyle** reddediyordu — *"body'nin 'yüklendi' demesi preload
arızasını görünmez yapar."* Reddedilen kalıp gövdeye yazılmış.

Hook'un kendi docstring'i: *"Agent 'skillerim yüklü' SANIR, elinde yalnız description
vardır."* Yani ilk hâl tam olarak engellenmek istenen yanılgıyı üretiyordu.

**Sorumluluk Clara'da.** PAM gövdeyi doğru taşıdı, PAD doğru uyguladı — yanlış olan
kaynak metindi.

## Açık kalan

**`## İş akışın` içindeki "Alan → skil" haritası.** Dört body'de var (BE 15 skill adı,
DO, PA, MB kısmen), beşinde yok. Bu "body isim vermez" kuralıyla çelişiyor ama
agent'ın açılışta gördüğü tek somut harita. Karar verilmedi — ayrı tur.
