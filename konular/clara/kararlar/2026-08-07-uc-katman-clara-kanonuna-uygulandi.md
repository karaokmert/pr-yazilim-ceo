# Üç katman Clara'nın kendi kanonuna uygulandı

**Tarih:** 2026-08-07
**Karar mercii:** Mert (*"repon istediğin düzende mi, kendi alanını bir incele"*)
**Durum:** Kapalı

---

## Karar

Clara'nın body'sinden **yöntem anlatan bölümler skill'lere taşındı.** Body'de yalnız
kimlik, sınır, refleks ve **tetikleyici** kaldı.

İki yeni skill açıldı, iki mevcut skill genişletildi:

- **`oturum-duzeni`** (yeni, 137 + 88 ref) — açılış/kapanış, iki mod, hafıza temizliği
- **`onay-brief`** (yeni, 88) — Mert'e iş sunma biçimi
- **`hafiza-duzeni`** (111 → 153) — kayıt yeri kuralı + kaydın denetlenebilirliği
- **`arama-disiplini`** — değişmedi (body'deki kısım zaten atıftı)

**Body: 953 → 771 satır.** Her turda taşınan yük ~2.000 token azaldı.

---

## Neden gerekti

Kanonun kendi kuralı (*"Üç katman"* bölümü, 2026-08-07) şunu diyor:

> **body** = kim olduğun (her turda yüklenir, en pahalı yer) · **skill** = bir işin
> yöntemi · **reference** = kanıt ve ayrıntı

Ve aynı gün Mert genel hükmü koymuştu:
`kararlar/2026-08-07-kural-skillde-kalir-bodyye-kopyalanmaz.md` — *"bir kuralın tanım
yeri skill'dir."*

**Bu hüküm fabrikaya uygulandı, Clara'ya uygulanmadı.** Ölçüm:

- Body 5 günde **273 → 953 satır** (18 commit)
- 953 satırın **429'u yöntem** — yani skill'e ait olan
- Oturum açılışı tek başına **176 satır** ve oturumda **bir kez** lazım
- Her tur taşınan toplam: **~12.400 token** (10.200'ü body)

En pahalı yere en az tetiklenen şey konmuştu.

---

## Taşıma ölçütü — satır sayısı değil, tetiklenme anı

Ayıran soru: **bu bölüm her cümlede mi lazım, yoksa bir işe girerken mi?**

- Her cümlede → **body** (kimlik, sınır, refleks)
- Bir işe girerken → **skill** (yöntem, sıra, adımlar)
- Sorulduğunda → **reference** (ölçüm, vaka, tarih)

**Body'de kalanlar ve neden:**

- **Plan → task → koşum** — Mert *"en önemli kural"* dedi, her işte geçerli
- **Üç katman** — kendi yazma refleksim, kimlik
- **Kritik kurallar, ton, üç sert sınır** — dokunulmaz

---

## En kritik risk: tetikleyici kalmalı

Skill'e taşınan kuralın **tetikleyicisi body'de kalmazsa kural sessizce kaybolur.**
Skill'ler preload edilmiyor (bu repoda ölçülmüş arıza —
`incelemeler/skill-preload-bulgusu/`), description'la tetikleniyorlar.

Bu yüzden her taşınan bölüm için body'de bir yönlendirme satırı bırakıldı. Ve
`oturum-duzeni` için özel bir ifade kullanıldı: **"koşulsuz AÇ"** — çünkü oturum başında
kullanıcı *"oturum açıyorum"* demez, doğrudan işe girer; description'ın tetiklenmesini
beklemek yetmez.

---

## Sınama

Kırpılmış body isimsiz bir yardımcıya (`general-purpose`) okutuldu, üç durum soruldu
(oturum açılışı · onay sunma · bulgu yazma). Niyet taşınmadı — yalnız dosya verildi,
davranış soruldu.

**Sonuç: üçünde de doğru davranış + doğru adres.** Yardımcının kendi cümlesi:

> *"Dosyada bulamadığım tek şey: DURUM 1 için hangi dosyaların hangi sırayla okunacağı.
> Dosya bunu `oturum-duzeni`'ne devrediyor — ve bu bir eksiklik değil, katman ayrımının
> gereği."*

Yani boşluğu **fark etti** ve **doğru yeri gösterdi.** Aranan davranış buydu: body
eksik olduğunu bilecek, nereye gideceğini bilecek.

Ayrıca kendiliğinden şunu söyledi: *"üç durumda da aynı desen var — dosya kararı ve
ayıran soruyu veriyor, yöntemi skill'e bırakıyor."* Katman ayrımı **okunabilir** hâle
gelmiş.

---

## Yan işler (aynı oturum)

- **`HARITA.md` eşlendi** — 9 haritasız kayıt eklendi (5 karar, 2 fikir, 1 sprint +
  yeni *Sprint* bölümü). Harita 119 → 131 satır.
- **1,1 MB artık silindi** — `panel-kanal.png` + `session-report-*.html`; ikisi de tek
  seferlik çıktıydı, atıf almıyordu. `.gitignore`'a tekrar önleyici satır girdi.
- **Yanlış pozitif düzeltildi** — ilk ölçümde *"5 kırık atıf"* bulunmuştu; beşi de cümle
  içinde geçen dosya adlarıydı (harita atfı değil). Ölçütün kendisi gevşekti.

---

## Açık kalan

**`i-have-adhd` skill'i** — Clara'nın yazmadığı, MIT lisanslı, `disable-model-invocation:
true` olan bir skill `.claude/skills/` altında duruyor (142 satır). Dışarıdan gelmiş.
Kalsın mı kaldırılsın mı — **Mert'in kararı.**

**Hedef tutmadı.** Plan ~600 satırdı, 771'de kalındı. Kalan bölümler kimlik ve refleks;
daha fazla kesmek kanonu değil karakteri budamak olurdu. Zorlanmadı.
