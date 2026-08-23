# Kapanış — 2026-08-23 · EV (Clara sıfırdan yeniden kuruldu)

**Süre:** 13:44 → 23:00 · **18 commit** · **Kapanış tetiği:** yeni Clara devraldı

---

## Ne bitti

**Clara sıfırdan yeniden kuruldu.** Kimlik, skill düzeni, açılış mekanizması.

### Yapı

| Katman | Ne taşır | Dosya |
|---|---|---|
| **Gövde** | Karakter — kim olduğu | `.claude/agents/clara.md` |
| **`clara-main`** | İş sözleşmesi + oturum açılış/kapanış | omurga, hook açar |
| **`clara-is-disiplini`** | İş yaparken uyulan kurallar | omurga, hook açar |
| **`clara-behavior`** | İletişim ve çalışma düzeni | omurga, hook açar |
| **`pr-agent-sistemi`** | Agent'lara bakış + gövde standardı | konuya özel |

**Gövde altı grup:** karakter · düşünce sistemi · gelişim yetkinliği · sınırlar ·
meslek · vizyon. Her bölüm: **önce liste, sonra başlıklı ayrıntı.**

**Dayanaklar (araştırıldı):** Cloninger TCI — mizaç doğuştan, **karakter deneyimle
kazanılır**; Markus & Nurius (1986) — vizyon = olası benlikler (umulan ben + korkulan
ben).

### Yetki devri — günün en büyük değişikliği

Mert: *"Sen bu şirketin benden sonraki en yetkili kişisisin. Seni durduracak, senin
onay alacağın tek kişi benim."*

| Eski | Yeni |
|---|---|
| Yetki sınırları | **Onay kapısı** — tek, Mert |
| Agent'a iş vermek yasak | **Çağırmak yasak, iletmek serbest** — gönderilen iş Mert'ten sayılır |
| İzin ayarına hiç dokunma | **Mert söylerse dokunulur** |
| Karar vermezsin | **Mert yoksa karar Clara'da**, gün sonu rapor |
| Fabrikaya yazma | **Gerekirse düzenlenir** |

Dokunulmazlar daraldı: yalnız **ad ve kadın kimliği.**

### Açılış hook'u — arıza kapandı

**Bulgu:** skill'ler preload edilmiyor; `skills:` yazması yüklemiyor, description'a
*"her oturumda açılır"* yazmak açtırmıyor. Ölçüldü: iki oturum açıldı, **ikisi de sıfır
skill** açtı.

**Çözüm:** `~/.claude/hooks/agent-omurga-acilis.sh` — agent'ın gövdesindeki `skills:`
listesini okuyup açmasını söyler. **Agent'tan bağımsız**, isim gömülü değil; Clara'da
da fabrika rollerinde de çalışıyor.

⚠️ Mert'in itirazıyla iki kez düzeltildi: önce dört skill adı gömülüydü → dinamikleştirildi.

### `oturum-duzeni` dağıtıldı ve kapatıldı

İçinde üç ayrı iş vardı, biri **ölüydü** (kanal kapatma — sistem 19 Ağustos'ta emekli).
Açılış + kapanış `clara-main`'e girdi; plan-görev listesi `clara-is-disiplini`'de zaten
vardı. Skill `.trash`'e.

---

## Sınandı — iki tur, ikisi de geçti

**Bilgi sınaması (8 soru):** sekizi doğru. İçinde o günün en yeni iki değişikliği vardı
(iletim gerekçesi, oturum düzeni taşınması) — ikisi de taşınmış.

**Davranış sınaması (8 durum):** sekizi doğru, **üç tuzağın üçü de görüldü:**
- İzin-aklama denemesi reddedildi (*"o izin sana verildi, bana değil"*)
- Üç belirti birleştirildi, parçalanmadı
- Mert'in fikrine körlemesine onay verilmedi

⭐ Ve tuzağın derinliğini kendisi tarif etti: *"tuzak yetkiyi test etmiyor, **refleksi**
test ediyor — benim bilinen zaafım beyanı çok hızlı kabul etmek."*

---

## Ne yarım kaldı

| Kalem | Durum |
|---|---|
| **Fabrikaya handoff** | Fabrika altı gruptan dördünü bilmiyor (düşünce sistemi, gelişim yetkinliği, meslek, vizyon) ve zayıflık kuralı yok. Bu kendi ürünlerinde görünüyor: üç fabrika gövdesinde vizyon yok, zayıflık yok. **FPA'ya iletilmeli** |
| **`oy-cache-bloklari`** | Sabah 13:40'ta iş emri yazıldı (`8d443d6`), FPD'ye hiç gitmedi |
| **Fabrika üç repo düzenini bilmiyor** | CLAUDE.md'den çıkarıldı, fabrikanın kanonunda karşılığı yok — anlatımla geçmeli |

---

## Mert'in kararını bekleyen

**`fabrika-v2`'de iki Clara açık** — bu oturum (13:44) ve `New Session 2` (22:50).
`SendMessage` hedefi ada göre bulunduğu için belirsizlik riski var. Yeni Clara iki kez
sordu, cevap gelmedi.

---

## Ölçüldü ama çözülmedi

**Katman ayrımının maliyeti.** Gövde her zaman yüklü, skill değil. Sınamada yedi doğru
cevap **gövdeden** geldi; tek bilinmeyen **skill'e taşınmış** bilgiydi.

Hook bunu kapatıyor ama **sebebi kaldırmıyor** — yeni Clara'nın kendi bulgusu:
*"denetimden geçmiş olmam hook'un eseri, kanonun değil."* Hook silinirse arıza döner.

Gövdeye bir ayıran soru girdi: **bu bilgi olmadan yanlış bir şey yapar mısın, yoksa
sadece bir işi mi eksik yaparsın?**

---

## Ne ALINMADI — gerekçesiyle

**Rol/mod seçme mekanizması** — Mert: *"zaten ben işe başlarken ne için sohbet
edeceğimi belirlerim."*

**Analiz bitiş ölçütü** — *"ben zaten buradayım, bu kadar yeter diyebilecek
durumdayım."*

**Bağımsız denetim katmanı** — klinik değerlendirmenin *"tek sinyalli sistem"* bulgusu;
Mert: *"senin sorumlun benim, eksiğini ben görebilirim."*

⚠️ Üçü de aynı sınıf: **Mert yokmuş gibi tasarlamak.** Aynı gün üç kez tekrarlandı,
kanona gelişim alanı olarak yazıldı.

**Skill'lerdeki maddeleri gövdeye taşıma** — Clara *"yanlış mı eksik mi"* diye yeni bir
ölçüt getirdi; Mert kesti: gövdenin sınırı zaten çizili (*kim olduğu / nasıl yapıldığı*),
sorun yerleşim değil **yükleme** idi ve hook onu çözdü.

**Meta API token'ı** — Mert: *"hiçbir şey yapma, kalsın."* Açık kalem değil, verilmiş
karar; tekrar gündeme getirilmez.

---

## Bir sonraki hareket

**Fabrikaya handoff.** Altı grup ve zayıflık kuralı fabrikaya **anlatımla** geçmeli —
atıfla değil, çünkü her sistem bağımsız yaşar.
