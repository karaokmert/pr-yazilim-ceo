# Kapanış — Clara'nın saha rolü daraltıldı (23:51–00:21)

> **Mod:** EV. Tek iş. Dokunulan dosya: `~/.claude/skills/proje-yonetimi/SKILL.md`
> (Clara'nın kendi skill'i, Mert onayladı). Yedek: `SKILL.md.bak`.

## Ne bitti

**Mert kanal yönetimini Clara'ya devredemiyordu ve sebebi bulundu: eksik kural değil,
ÇELİŞEN kural.** Skill'de "yorum yapma" kuralı yoktu; tersini söyleyen dört yer vardı.

**Temizlenen dört çelişki:**

1. **`"Kapsam sorusu → sen cevaplarsın... Ne senin ne PA'nın"`** — darboğazın kaynağı.
   PA'yı açıkça yasaklıyor, iki seçenek bırakıyordu: kendim cevapla (yorum) ya da
   Mert'e getir (tıkanma). → Her soru PA'ya gider, kapsam sorusu dahil.
2. **Dört kademeli soru süzme** (*"sen biliyorsan cevapla"*) → tek kademe.
3. **`"Clara okur — statü değiştirmez"`** → `blocked` yetkisi verildi.
4. **`"yanıtını beklersin"`** → akış durmaz, sıradakine geçilir.

**Eklenen:** skill'in başına **üç kontrol** (ClickUp doğru mu · kanona baktın mı ·
yorumsuz taşıma) + *"çelişirse bu bölüm kazanır"*. Ve **yöntem/iş yorumu** ayrımı.

**Karar dosyası:** `konular/clara/kararlar/2026-08-14-clara-sahada-tasiyici.md`

## Neden yama olmadı

Üstüne *"yorum yapma"* kuralı eklenmedi — çelişen satırların kendisi değiştirildi
(`CLA-FIX-THE-CAUSE`). Eklenseydi eski satırlar yerinde kalacak, bir sonraki oturum
yine ikisi arasında kalacaktı.

## Ne yarım kaldı

**Hiçbir şey yarım değil** — ama bir ölçüm borcu var (aşağıda).

## Mert'in kararını bekleyen

Dünkü kapanıştan devreden dört madde **aynen duruyor**, bu oturumda dokunulmadı:

**1 — `setup.py` PID düzeltmesi kim yazacak?** Kutu adı dakika hassasiyetiyle
üretiliyor, aynı dakikada açılan iki agent aynı adı hedefliyor. Metin hazır:
`f"{ROL}-{SESSION}-{os.getpid()}"`. Fabrika betiği → `CLA-ASK-BEFORE-WRITING-OUT`.

**2 — Beş agent'a `clickup` atıfı** (BE/FE/CA/DO/TE/UID body'lerinde 0 hit). Devir
bloğu yazıldı, taşınmadı.

**3 — "Tutarlı yazacaklar mı" ikinci ölçümü** — 12 Ağustos karar dosyası bekliyor.

**4 — Dünden:** fabrika betiklerine yazma izni · üç fabrika bulgusu · kayıp mesajlar.

## Ölçüldü ama çözülmedi

**Yeni rol sahada TUTTU MU — ölçülmedi.** Skill değişti, davranış değişmedi henüz.
Ölçüm ancak goat'ta (ya da başka bir OY projesinde) bir oturum yürütülünce alınır.

**Ölçülecek üç şey:** (1) BE/FE sorularının kaçı PA'ya taşındı, kaçı Mert'e gitti ·
(2) taşınan mesajların kaçı ham, kaçı yorumlanmış · (3) kaç task `blocked`'a alındı
ve comment'i tam mı.

**Ve dünkü hook borcu duruyor:** `★ Question` başlık kuralı + tanımlayıcı kuralı sahada
ölçülmedi (200+ mesaja ulaşınca tek taramada çıkar).

## Bir sonraki hareket

Goat'ta (ya da bir OY projesinde) yeni rolle bir oturum yürüt — Mert'e giden soru
sayısı düşüyor mu, PA devrede kalıyor mu, akış blocked'la sürüyor mu.
