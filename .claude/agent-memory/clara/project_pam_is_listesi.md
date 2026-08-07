---
name: pam-is-listesi
description: PAM'e iletilecek işlerin listesi — hazır gereksinimler ve kanona girmesi gereken kararlar. Bir iş fabrikaya gitmeye hazır olduğunda buraya yazılır, iletildiğinde satırı silinir.
metadata:
  type: project
---

# PAM'e iletilecek iş listesi

Buraya bir iş **hazır olduğunda** yazılır: gereksinimi netleşmiş, gerekçesi yazılı, karar
verilmiş. İletildiğinde satır silinir.

Sıra Mert'te — bu liste hazırlık, öncelik değil.

---

## 1. Brief/handoff biçimi — "kim nereye dokunuyor" kalıbı

**Karar veren:** Mert, 2026-08-07. Kendi cümlesi: *"Tüm agent'ların sen dahil bana
sunduğu iş brief'lerinin ve handoff'ların bu yapıda olmasını istiyorum, bu şekilde olması
benim kararımı kolaylaştırır."*

**Kaynak:** `incelemeler/pa-davranis-senaryolari/onay-brief-kalibi.md` (tam kalıp + kabul
edilmiş örnek orada; kopyalanmaz, atıf verilir)

**Clara tarafı yapıldı:** kanona yazıldı (*"Onay brief'i"* bölümü). Aynı biçimi
kullanıyorum.

**Fabrikaya gidecek olan:** kalıbın kanona girmesi. Eklenecek kurallar:

1. Her iş kalemi **üç blok**: şu an ne oluyor → nasıl çözüyorum (AKIŞ) → nereye dokunuyor
2. Sonda **üç satır**: neye dokunmuyorum · en önemli sınır · açık karar + süre
3. **Ölçüm anlatısı brief'e girmez** — sonuç girer, yöntem sorulunca verilir

**Üçüncü bloğun genellemesi — Mert'in kavrayışı:** o blok tek bir soruyu cevaplıyor,
**"kim nereye dokunuyor?"** Alanlar role göre değişir, soru aynı kalır:

```
backend      → handler · DataLayer · cache · tablo · emsal
frontend     → component · hook · state · stil · emsal
agent üreten → agent body · skill · reference · hook · index
kural yazan  → kural kimliği · katman · cascade · index
ölçüm yapan  → ne ölçüldü · yöntem · kanıt nerede · neyi çürütüyor
```

Yani alan listesi ezberlenmez, **türetilir.** Bu ayrım kanona yazılmazsa her agent kendi
alanlarını uydurur ve tek biçim yine bozulur.

**En pahalı ders — ters yönde öğrenildi:** üç denemede teknik detay **çıkarıldı**, oysa
Mert daha fazlasını istiyordu. *"Teknik olmasın tabii ki, ama akışsal da anlatsın
istiyorum."* Ayrım: teknik **terim** değil teknik **AKIŞ.**

**Kabul ölçütü:** *"başka biri bana bu modülü nasıl yaptın dese anlatabiliyor muyum?"*
Brief iki işi birden yapıyor — onay almak ve Mert'i işin sahibi hâline getirmek.

**Ve Mert'in ikinci beklentisi:** PAM bunu öğrendikten sonra **agent üretiminde de bu
düzeni kullanacağını bilir** — yani ürettiği her yeni agent'ın kanonuna bu kalıp girer.

**Kapsam uyarısı:** OY + WEB ikisi de brief veriyor. `ISD-ONE-TEAM-PER-TURN` gereği her
takıma **ayrı tur** — ortak olan yalnız gerekçe, o bir kez yazılır ve atıf verilir.

**Gecikme kaydı:** kalıp 2026-08-04'te hazırdı ve devredilmedi. Bu gecikmenin kendisi bir
bulgu — **hazır bir gereksinim kendiliğinden üretime girmiyor, taşınması gerekiyor.**

---

## 2. Kanal protokolü — kanona girecek ama HENÜZ DEĞİL

**Durum:** yaşayan taslak, `kanal-kurulumu` skill'inde. Dört fabrika agent'ı kanala
bağlandı ve çalıştı, ama **kanonlarında yok** — her oturumda elden anlatılıyor.

**Dört bağımsız uç aynı şeyi bildirdi:** *"kanal kurulumu kanonumda yok, bir sonraki
oturumda bilmeyeceğim."*

**Mert'in kararı — neden bekliyor:** *"Önünü arkasını hatalarını risklerini görmeden
yazarsak hata yaparız. Şimdi yazmayacağız, iş yapacağız."*

**Geçiş şartı:** sahada olgunlaşması. Yedi açık kalem var (oturum biçimi, canlılık ölçütü,
ilk kutuyu kim açar, iş talimatı onay yerine geçer mi, inbox/outbox ayrımı, JSON deposu,
kanona giriş zamanı) — ayrıntı `kanal-kurulumu` skill'inin *"Açık kalemler"* bölümünde.

**PAM'in gereksinimi hazır:** `agent-project/docs/fabrika/kanal-protokolu/gereksinim.md`
(sekiz hüküm + bir gerçek çakışma + dört açık soru). Olgunlaşınca plana çevrilecek.

---

## 3. Fabrika denetiminden çıkan altı öncelik

**Kaynak:** `incelemeler/fabrika-denetimi/eksikler.md` (dosya:satır kanıtlı)
**Karar:** `kararlar/2026-08-06-fabrika-denetimi-sonucu.md`

Özet sıra:

1. **Cascade onarımı** — `atif_verenler` 112/123 kuralda boş; index'in kendi beyanında
   *"cascade haritası"* ve PQA'nın denetim ekseni. **Dördüncü ölçüt (bakım kabiliyeti)
   buna bağlı.** Bu iş şu an PAM'de (gereksinim yazılıyor).
2. **Alt-agent'a kanon ulaştırma** — hook alt-agent'ta çalışmıyor, `CLAUDE_CODE_AGENT`
   çağıranın adını taşıyor. **Sıra tersine kurulamaz:** hook'u env düzeltilmeden
   çalıştırmak sistemi bugünkünden kötü yapar.
3. **Sıfırdan üretme yöntemi** — en zayıf halka, en büyük iş. Bir takımın kendi tasarımı
   (hangi roller, kaç personel, devir hattı) hiçbir dosyada yok. Kapsamı Mert'le çizilecek.
4. **Rapor biçimi** — 1. maddeyle aynı kökten; brief kalıbı bunun bir parçası.
5. **Filo bakımını bir kez koştur** + kimlik çakışması + plugin skill'inin ezilmesi.
6. **Küçük sessiz kalemler** — `Task`→`Agent` metin düzeltmesi, PQA'nın ölçüt skill'i
   elinde değil, iki skill kendi satır eşiğini aşıyor.
