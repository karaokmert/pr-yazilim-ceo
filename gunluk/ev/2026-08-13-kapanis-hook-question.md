# Kapanış — hook: Question başlığı + tanımlayıcı kuralı (22:58–23:11)

> **Mod:** EV. Kısa oturum, tek iş. Başka repoya yazılmadı;
> dokunulan tek dosya `~/.claude/hooks/sessiz-mod.sh` (global hook, Mert onayladı).

## Ne bitti

**Hook'a iki kural yazıldı ve çalıştığı ölçüldü.**

**1 — `★ Question` kutusuna zorunlu başlık.** Kutu artık konu adıyla açılıyor
(isim tamlaması, soru değil). Ölçüt: kullanıcı yalnız başlığı okuyarak neyin
sorulduğunu anlayabilmeli. Ayrıca gövde kuralı somutlaştı — kutuda geçen her
dosya/terim kutunun İÇİNDE açıklanır, yukarıda açıklanmış olsa bile.

**2 — Tanımlayıcı tek başına basılmaz.** ClickUp task ID'si başlığıyla yazılır
(`PRC-41 (sponsor listesi filtresi)`); aynısı commit hash, PR numarası, branch
ve dosya yolu için.

**Doğrulama:** hook koştu (çıkış kodu 0), geçerli JSON, yedi anahtar metinde
mevcut, 2.895 karakter. Yedek alındı (`sessiz-mod.sh.bak`).

**Karar dosyası:** `konular/clara/kararlar/2026-08-13-question-baslik-ve-tanimlayici.md`

## Neden yama olmadı

Eski kural (*"kutunun içi kendi kendine yetmeli"*) vardı ve İŞLEMİYORDU —
bir sonuç tarif ediyordu, ne yazılacağını söylemiyordu. Üstüne uyarı eklenmedi;
cümlenin kendisi somut hâliyle değiştirildi (`CLA-FIX-THE-CAUSE`).

Kanıt aynı oturumdan: Clara `setup.py` sorusunu sorarken kutuya `PID`,
`f-string` yazdı ve bunları kutu içinde açıklamadı — kural yürürlükteydi,
yazan çiğnediğini fark etmedi.

## Ne yarım kaldı

**Hiçbir şey yarım değil** — ama bir ölçüm borcu var (aşağıda).

## Mert'in kararını bekleyen

Dünkü kapanıştan devreden dört madde **aynen duruyor**, bu oturumda hiçbirine
dokunulmadı:

**1 — `setup.py` PID düzeltmesi kim yazacak?** Mekanizma hâlâ bozuk: kutu adı
dakika hassasiyetiyle üretiliyor (`{ROL}-{YYYYMMDD-HHMM}`), aynı dakikada açılan
iki agent aynı adı hedefliyor, ikincisi var olan kutuyu sahipleniyor. Dün goat'ta
elle çözüldü ama kod aynı. Metin hazır: `f"{ROL}-{SESSION}-{os.getpid()}"`.
Fabrika betiği → `CLA-ASK-BEFORE-WRITING-OUT` kapsamı.

**2 — Beş agent'a `clickup` atıfı** (BE/FE/CA/DO/TE/UID body'lerinde 0 hit).
Devir bloğu yazıldı, taşınmadı.

**3 — "Tutarlı yazacaklar mı" ikinci ölçümü** — 12 Ağustos karar dosyası bekliyor.

**4 — Dünden:** fabrika betiklerine yazma izni · üç fabrika bulgusu · kayıp mesajlar.

## Ölçüldü ama çözülmedi

**Hook kuralları sahada TUTTU MU — ölçülmedi.** Yazılmış olmak uygulanmış olmak
değil. Dünkü sessizlik hook'u da aynı borçla kapandı (2 oturum / 26 mesaj,
örneklem yetersiz).

**Tek taramada çıkacak üç ölçüm** (200+ mesaja ulaşınca):
(1) sessizlik hook'unun ara-blok etkisi · (2) `★ Question` kutularında başlık
oranı · (3) task ID'lerinin kaçında başlık var. Üçü de aynı hook'tan geliyor.

**Ve hook'un yapısal sınırı:** agent body'sinde iz bırakmıyor. Bir agent'a
*"bu kural nerede yazılı"* diye sorulursa gösteremez. Kalıcı olması isteniyorsa
fabrikaya gitmeli.

## Bir sonraki hareket

`setup.py` PID kararı — iki oturumdur bekliyor ve mekanizma her gün aynı arızayı
üretmeye hazır.
