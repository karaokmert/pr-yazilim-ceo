# ClickUp yazma yetkisi — yasak kalkmaz, kapsamı daralır

**Tarih:** 2026-08-12 · **Karar:** Mert · **Getiren:** Clara (fabrika modu)
**Etkilenen kanon:** `CLICKUP-PA-ONLY-WRITE` (OY — `clickup/SKILL.md:45`,
`project-assistant/SKILL.md:36`)

## Karar

Agent **yalnız kendi sub task'ının** statüsünü çevirir. Ana task, başkasının sub
task'ı, `Closed`, `revise` ve task silme **mutlak yasak kalır.**

Yani yasak kaldırılmıyor — **sınırı değişiyor.**

## Neden bu, neden diğer ikisi değil

Sahadan gelen teklif iki yol sunuyordu: (a) kural gevşesin, (b) kural aynen kalsın.
İkisi de yama, çünkü ikisi de **sebebi** yerinde bırakıyor.

**Sebep şu:** kural mutlak bir yasak koydu ve kendisini askıya alacak meşru bir yol
tanımlamadı. Saha bir istisnaya ihtiyaç duyunca yasak kırıldı — ve kırılma bir kararla
değil, bir **talimatla** oldu (2026-08-12 testi: Mert kuralı o oturuma özel askıya aldı).
Emsali var: PA daha önce mutlak yasağı okuyup kendi istisnasını açmıştı
(`behavior/references/saha-kanitlari.md:37`).

Kuralın kendi metni bunu zaten yasaklıyordu:

> *"Bu yasak, kullanıcı talimatıyla da AÇILMAZ (istisna yok). 'Sen açıkça söylediğin
> için uygulayabilirim' YASAK — agent yasağa kendi kararıyla istisna açamaz."*

Yani bugünkü test, kuralın açıkça yasakladığı yoldan yürüdü. Bu tekrarlanırsa kural
fiilen ölür ve kimse ihlal göremez.

**(a) neden yama:** yetkiyi açar ve *"agentlar tutarlı yazacak"* varsayımına dayanır —
bu ölçülmedi (aşağıda).

**(b) neden yama:** kuralı korur ama saha onu bugün zaten çiğnedi; yarın yine çiğneyecek
ve her projede aynı istisna yeniden açılacak.

**Kapsam daraltma neden sebebi kaldırıyor:** sınır artık **talimatla** değil
**sahiplikle** çiziliyor. "Kendi sub task'ı" ölçülebilir bir şey — kimin hangi task'a
dokunacağı task sahipliğinden çıkar, bir kişinin o oturumdaki iznine bağlı değil.
İstisnaya ihtiyaç kalmıyor, çünkü sahanın ihtiyaç duyduğu şey zaten kapsamın içinde.

## Ölçümün sınırı — kayda geçiyor

Sahadan gelen mesaj *"kuralın üç gerekçesinden biri çürüdü"* diyordu. **Yarım doğru.**

Gerekçe 1 iki şey söylüyordu: *"agent ya skill açmadan MCP'ye gider ya hiç yapmaz —
**iki durumda da iz tutarsız.**"*

- **Birinci kısım çürüdü:** agentlar skill'siz de MCP'ye gitti ve statü çevirdi. Engel
  skill değil **izin katmanıydı** (`settings.json`); izin açılınca `create_task` ve
  `update_task` ikisi de geçti. UID, BE, PA ayrı ayrı ölçtü.
- **İkinci kısım ölçülmedi:** *"iz tutarsız kalır"* iddiası tek turda, üç agent'la,
  gözetim altında test edildi. Ölçüm dosyası sınırını kendi yazıyor: PRAG **kurgusal**
  bir proje, `PRC-37` geriye dönük açıldı, *"testte görülen sıra sahadaki sıra değildir."*

Yani kanıtlanan şey **"yapabiliyorlar"**; kanıtlanmayan şey **"tutarlı yapacaklar"**.
Kural ikincisi için konmuştu.

Gerekçe 2 (*"iz bırakan aksiyon, tek yazan rol izi tutarlı kılar"*) ve gerekçe 3
(*"tablo v7'den geldi, insan developer içindi"*) **ayakta** — çürütülmedi.

Kapsam daraltma bu yüzden doğru ölçekte: gerekçe 2'yi korur (iz bırakan asıl aksiyonlar —
`Closed`, silme, ana task — hâlâ tek elde), ölçülmemiş varsayıma dayanmaz.

## Fabrikaya giden

Gereksinim PAM'e gider; kanonu Clara yazmaz. Netleştirilecek noktalar devir bloğunda.

## Kaynaklar

- Kural gerekçesi: `skill-project/docs/agent-dogrulama/V8-TAMAMLAMA-DURUM.md:510-525`
- Kural metni: `v8/ozel-yazilim/.claude/skills/clickup/SKILL.md:45`
- Saha kanıtı (PA'nın kendi istisnası): `behavior/references/saha-kanitlari.md:37`
- Bugünkü ölçüm: `pr-yazilim-ceo/gunluk/ev/2026-08-12-clickup-task-takip-testi.md`
