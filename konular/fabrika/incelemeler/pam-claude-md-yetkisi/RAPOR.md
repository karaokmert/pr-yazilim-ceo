# PAM'in `CLAUDE.md` yetkisi talebi — yapıldı, blok ölçüldü

Tarih: 2026-08-03 (akşam)

## Talep

PAM (fabrika agent'ı) bir sorun tarifi gönderdi: `agent-project`'te `CLAUDE.md`'ye kimin
dokunabileceği kanonda tanımsız, iki kural çelişiyor, kullanıcı kararı verilmiş (PAM ve
PAD dokunabilir) ama kanona yazılmamış. Soru üç oturumda üç kez doğmuş.

PAD işi almış, `behavior/SKILL.md`'deki `BHV-NO-SELF-CONFIG`'i düzeltmiş ve iki turluk
davranış testinden geçirmiş. Sonra `pr-agent-manager.md`'ye yazmaya çalışırken auto mode
sınıflandırıcısı iki kez bloklamış. PAM de PAD'i tekrar çağıramamış (Task çağrısı da
bloklandı).

PAM iki şey istedi: Clara'nın o reponun `settings.json`'ına izin kuralı eklemesi, ya da
düzeltmeyi doğrudan yapması.

## Clara üç kez reddetti, sonra kural değişti

İtirazın özü: izin kuralı bir düzeltme değil **kapı**; blok bir arıza değil çalışan bir
kapı; ve engel deterministik değil (PAM'in kendi kaydı: *"usually transient, retrying
often succeeds"*).

Mert üç kez ısrar etti ve dördüncüsünde kararını verdi. Kural değişti — sınır
*"yazamazsın"*dan *"onaysız yazamazsın"*a taşındı
(`kararlar/2026-08-03-clara-yazma-sinirinin-degismesi.md`).

Süreç şöyle işledi: metin yazılmadan önce Mert'e gösterildi, onaylandı, sonra yazıldı.
Yeni kural `CLA-ASK-BEFORE-WRITING-OUT` ilk kez burada uygulandı.

## Yazılan üç değişiklik

**`.claude/agents/pr-agent-manager.md`** — `PAM-WRITE-DOCS-ONLY`'ye iki istisna eklendi:
`CLAUDE.md` proje bağlamıdır (ürün değil), yazılabilir; **kendi tanımı** yazılamaz, çünkü
denetleyeni denetlenenle aynı el yapar. Kapsamın davranış olduğu, dosya listesi olmadığı
tekrar vurgulandı.

**`.claude/agents/pr-agent-developer.md`** — `PAD-WRITE-WHAT-WAS-ASKED` altındaki cascade
çelişkisi giderildi. `CLAUDE.md` *"dokunamazsın"* örnek listesinden çıkarıldı, yerine
ayrım kondu: *"plan `CLAUDE.md`'yi kapsıyorsa yazarsın, kapsamıyorsa bildirirsin — ayıran
şey dosyanın adı değil, planın kapsamı."* Örnek listesine `kendi tanımın` eklendi.

**`.claude/rules-index.json`** — `PAM-WRITE-DOCS-ONLY` kaydına `not` alanı eklendi (PAD
kaydında zaten vardı, PAM'de yoktu). 121 kural sayısı değişmedi.

Commit ve push atılmadı — o `agent-project`'in kendi işi.

## Ölçüm — blok geçici, izin kuralı gereksiz

Bu, PAM'in talebindeki asıl soruyu cevaplıyor.

`pr-agent-developer.md`'ye ilk `Edit` **bloklandı** — PAM'in aldığı mesajın aynısı:
*"Stage 2 classifier error - blocking based on stage 1 assessment (usually transient —
retrying often succeeds)."*

**Aynı içerikle ikinci deneme geçti.** Hiçbir şey değiştirilmedi, izin kuralı
eklenmedi, ayar dosyasına dokunulmadı.

Sonuç: engel deterministik değil ve kalıcı bir açık gerektirmiyor. PAM'in kendi
teşhisi doğruydu; eksik olan şey teşhise güvenip tekrar denemekti.

Bu artık bir çıkarım değil, **ölçüm**. Aynı blok üç ayrı elde görüldü (PAD iki kez,
PAM bir kez, Clara bir kez) ve bir kez tekrar denemeyle aşıldı.

## Açık kalan

`agent-project` uncommitted durumda ve diff'te fabrikanın önceki değişiklikleri de var
(`behavior/SKILL.md` + on `docs/` dosyası). Denetim ve commit fabrikada — PQA'nın kapısı
atlanmadı, yalnız yazan el değişti.
