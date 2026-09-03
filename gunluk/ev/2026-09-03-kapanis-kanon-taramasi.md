# Kapanış — 2026-09-03 · EV (2. oturum: kanon taraması ve temizlik)

**Tetik:** Mert "eski işin devamı" dedi, sonra yönü kendisi çizdi: *"kendi body ve
skill'lerini tam baştan sona oku, anlamadığın, gereksiz, çelişkili şeyler var ise
sor bana."* Fable üzerindeki ilk oturum.

---

## Ne bitti

**1 · Kanon taraması ve düzeltmeleri** — commit `cbde671`
Gövde + 12 skill + references baştan sona okundu. Bulgular tek tek soruldu,
kararlar `kararlar/2026-09-03-kanon-tarama-duzeltmeleri.md` altında:

- **Saha rolü netleşti:** PA merkez, **Clara PA'ların üstündeki birim** — rutin
  handoff taşımaz, çoklu proje/PA koordinasyonu ve görünürlük onda. Üç dosya
  hizalandı (`proje-yonetimi`, `clara-behavior`, `clara-main`).
- Emekli kanal/kutu sisteminin kalıntıları silindi; sessizlik ölçümü oturum
  kaydının son hareketine bağlandı.
- HARITA.md kuralı kaldırıldı — "klasör haritadır" tek hüküm.
- Skill'lerdeki tablolar listeye çevrildi (tablo kuralı skill'leri de kapsıyor —
  Mert'in kararı).
- Küçükler: günlük yolu `gunluk/{proje}/`, gövde iş sayımı, ölü atıf, Qdrant
  tarihçesi, `ps`→`ListAgents`. İki bayat memory kaydı silindi.

**2 · trash/ düzeni** — commit `e821fa3`
Mert'in kararı: **hiçbir şey doğrudan silinmez, repo kökündeki `trash/` altına
taşınır.** Eski gizli `.trash` içeriği ve `.cop-yedek` (10 kopya sprint-yonetimi
yedeği) taşındı; `.gitignore` ve `hafiza-duzeni` güncellendi. Fabrika agent
symlink'lerinin silinmesi Mert'in işlemiydi, commit'lendi.

**3 · VS Code eklenti temizliği** — commit `933f527` + `d96a103`
vsx-tr takımı (6 skill + 3 agent, EN+TR iki kuşak) ve iki panel eklentisinin
kaynakları (`vsx-agent-panel`, `vsx-clickup-panel`, 152 MB) `trash/`e; kurulu
iki eklenti (`pr-yazilim.vsx-clickup-panel`, `pryazilim.vsx-agent-panel`)
`code --uninstall-extension` ile söküldü, doğrulandı.

**4 · Kanon değerlendirmesi Mert'e verildi.** Örüntü: gövde sağlam, çürüme skill
katmanında — bir karar verildiğinde onu veren dosya güncelleniyor, aynı şeyi
anlatan diğer dosyalar unutuluyor. Tarama arada bir tekrarlanmaya değer; ritmi
Mert söyler.

## Ne yarım kaldı

Bu oturumda yok. **Dünden devredenler hâlâ açık** (bu oturumda bilinçli
açılmadı): sprint takip sistemi · proje ekonomisi aracı (doküman + task adımları,
varlık menülü ekranlar) · yeni iş tipinin `clara-main` tanımının tamamlanması.

## Mert'in kararını bekleyen

Yok — bu oturumun soruları soruldu, kararları alındı. (Dünkü kapanıştaki iki
bekleyen duruyor: proje ekonomisinin ürünleşmesi, Patron App.)

## Ölçüldü ama çözülmedi

- **PA-üstü rol kâğıt üstünde** — masada netleşti, sahada hiç sınanmadı. İlk
  saha oturumunda davranışa dönüp dönmediğine bakılmalı.
- **Goat'ın üç güvenlik açığı** (dünkü kapanışta ayrıntılı) hâlâ açık — canlıya
  çıkmadan kapanmalı.

## Bir sonraki hareket

Sprint takip sistemi (dünden açılmamış iş) ya da PA-üstü rolün ilk saha sınaması
— hangisi önce gelirse.
