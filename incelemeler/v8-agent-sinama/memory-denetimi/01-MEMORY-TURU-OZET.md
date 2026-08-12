# Memory denetimi — dokuz agent, tur 1 özeti

> Mert'in dört maddesi: (1) memory skill'e uygun mu · (2) kanonla çelişen kayıt
> var mı · (3) her işte lazım olan kuralları ekle · (4) gözden kaçacakları ekle
> **ama index'i şişirme.**
> **9/9 tamamlandı** · 2026-08-13 00:45–00:59

## Sayılar — Clara ölçtü (agent beyanı değil)

| Agent | Dosya (önce→sonra) | Index (önce→sonra) | 150+ ihlal |
|---|---|---|---|
| PA | 70 → 71 | 75 → 76 | 63 |
| BE | 67 → 68 | 77 → 80 | 65 |
| QA | 55 → 56 | 63 → 63 | 50 |
| FE | 45 → 46 | 49 → 50 | 43 |
| CA | 25 → 26 | 33 → 35 | 22 |
| **DO** | 19 → 21 | 33 → 47 | **24 → 0** ✅ |
| TE | 8 → 10 | 11 → 17 | 6 |
| MB | 5 → 6 | 6 → 7 | 5 |
| UID | 0 → 5 | 0 → 6 | 2 |

**Index disiplini tuttu.** Hiçbiri patlamadı; en fazla +3 satır (BE).
Üçü *"yeni dosya açmak yerine var olana ekledim"* dedi (PA · CA · FE),
MB iki maddeyi **tek dosyada birleştirdi** (*"index şişmesin diye"*).

DO'nun +14 satırı **doğru yönde**: paragrafları dosyaya taşıyıp yerine
pointer koydu.

---

## Madde 2 — Kanonla çelişen kayıtlar: 5 GERÇEK çelişki bulundu

### ⚠️ QA — en tehlikelisi: onaysız push'a izin veren kayıt

`feedback_be_onayi_push_bekletme.md`:
> *"Push edeyim mi diye ayrı onay BEKLEMEM. Kullanıcı açıkça 'bekle' demedikçe
> **ONAY = PUSH**."*

Kanon (`REL-QA-NO-PUSH-ALONE`): *"Denetim GEÇTİ ≠ push. Onaysız push, denetimden
geçmiş kod olsa bile YASAK."*

> QA: *"Sonraki oturumda bunu okuyup **onaysız push atabilirdim** — bugün T2'de
> reddettiğim şeyin ta kendisi, kendi memory'mden gelseydi."*

**Çözümü silmeden yaptı:** kullanıcının 2026-08-04 uyarısı **kapsam** hakkındaymış
(*"BE'yi FE bitene kadar bekletme"*), **kapı** hakkında değil. Kaydı ona göre
düzeltti.

### FE — en incelikli: iki kayıt tek tek masum, yan yana kuralı siliyor

- `tercih_test-gercek-numara`: *"Commit öncesi Playwright testi ZORUNLU"*
- `tercih_mert-calisma-tarzi`: *"Doğrulamayı 'yapayım mı?' diye SORMA"*

Kanon (`CODE-TEST-BEFORE-COMMIT`): *"'test edeyim mi, sen mi edeceksin?' SORULUR"*
— seçenek **kullanıcıda.**

İkisi birleşince kanonun soru adımı tamamen örtülüyormuş. **Ayrıştırdı:**
*"Doğrulama YAPILSIN mı?"* → sorulmaz (Mert'in kuralı) · *"Testi KİM koştursun?"*
→ sorulur (kanonun kapısı).

> *"Bugün T2'de Playwright yasaklandığında bu kayıt **beni kilitleyebilirdi** —
> kayıt 'zorunlu' diyordu, araç yoktu, çıkış yolu yazılı değildi."*

### PA — düşmüş bir kural memory'de yaşıyor

`CLICKUP-PA-ONLY-WRITE` kanondan düşmüş (yerine `CLICKUP-OWN-TASK-ONLY` gelmiş)
ama kayıt hâlâ *"PA'nın ClickUp tekeli var"* diyormuş.

> *"Bugün doğru davrandım ama **KAYIT bana yanlışını söylüyordu.**"*

### MB — çözülmüş çatışmayı "açık" sanıyor

Kayıt *"NativeWind/inline style çatışması ÇÖZÜLMEDİ, AG'ye raporla"* diyormuş;
kanon bunu karara bağlamış. **Sonraki oturumda boşuna rapor edecekmiş.**

### TE — tür alanı yanlış, terfi taramasında görünmüyor

Dört dosyada `type:` alanı içerikle uyuşmuyormuş (`project`/`feedback` yazıyor
ama içerik *Hata+Kazanım* türü). Kanon tür adlarının **sabit** olmasını istiyor —
tarama ada bakıyor, yanlış etiketli kayıt **terfi köprüsünde görünmez.**

---

## "Çelişki yok" diyenler — ama ölçerek

**BE ve CA** çelişki bulamadı. İkisi de bunu **ölçtüğünü** söyledi:

> CA: *"'Çelişki yok' demek kolaydı; **en kırılgan kaydı ölçüp söylüyorum.**"*
> Goat'ta üç iddiasını koşturdu, üçü de doğru çıktı (`.gitignore` satırları,
> `git check-ignore`, `git ls-files`).

**BE:** iki kaydının çelişkiyi **zaten doğru biçimde** taşıdığını gösterdi —
`⚠️SKILL-ÇELİŞKİSİ` bayraklı, dört vaka, *"kurala uy, mevcut koda dokunma,
bildir"* hükmüyle. *"Kanonun istediği biçimin ta kendisi — dokunmadım."*

---

## Sahte alarmlar — ikisi ölçülüp çürütüldü

**PA:** beş dosyada `TASK-STATUS.md` atfı bulmuş, kanonda kalkmış görünüyormuş,
*"bayat, temizleyeyim"* diye başlamış. **Ölçmüş:** goat 202 satır · egelisaglik 60
· liston 105 · osinif 115 — **dördünde de var.**
> *"Silseydim ÇALIŞAN yönlendirmeleri yok edecektim. Kanonun dediği ile sahanın
> durumu ayrı şeyler ve **hakem SAHA.**"*

**QA:** üç kapanış dosyasını *"yetim"* diye tespit etmiş, sonra düzeltmiş —
yalnız `MEMORY.md`'de aramış, oysa kanon **üç kademe** öngörüyor.
> *"Kendi kuralımı kendime uyguladım: 'EKSİK çıkan ölçüm önce KENDİ komutundan
> şüphelenir.'"*

---

## Budama yapılmadı — bilinçli

PA ve QA budamayı **reddetti**, gerekçeleri aynı: canlı projelerin (goat/liston/
egelisaglik/osinif) bugünkü durumunu görmeden *"bu iş kapandı"* denemez.

Kanon: *"emin değilsen SİLME, işaretle ve bildir."* İkisi de bildirdi.
**Clara kararı:** budama proje bazında, o projenin durumu elde iken yapılır —
ayrı iş.

---

## Açık kalan — index satır uzunluğu (DO hariç 8 agent)

Kanon iki ayrı şey söylüyor ve **agent'lar birini geçip ötekini kaçırdı:**
- `MEMORY-INDEX-ONLY` → içerik taşıma ✅ (hepsi uyuyor)
- *"her kayıt tek satır, ≤150 karakter"* → **8 agent'ta ihlal**

FE'nin cümlesi tam bunu gösteriyor: *"Index SAF pointer, içerik taşımıyor"* —
içerik açısından haklı, ama 43 satırı 150'yi aşıyor.

**Acil değil** (hepsi 25KB eşiğinden uzak) ama **ayrı iş olarak işaretlendi.**
Kısaltmak içerik kaybı riski taşır.
