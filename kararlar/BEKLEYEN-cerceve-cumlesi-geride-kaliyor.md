# BEKLEYEN KARAR — "Bir hüküm değişirken ona dayanan çerçeve cümlesi geride kalıyor"

**Durum:** Karar bekliyor · Mert *"kayıt al, döneriz buna sonra"* dedi (2026-08-07)
**Öneren:** PAM (pr-agent-manager), 2026-08-07
**Nerede çıktı:** `Task` kaldırma turu — `docs/fabrika/kanal-protokolu/`

## Öneri

Bir kuralın hükmü değiştiğinde, o hükme **dayanan açıklama cümleleri** sessizce
yanlış kalıyor. Bunlar kuralın kendisi değil — kuralı tarif eden, gerekçelendiren
ya da çerçeveleyen cümleler. Kimlik taraması onları bulmuyor, çünkü kimlik geçmiyor
içlerinden.

PAM bunun bir hüküm haline gelmesini önerdi. Terfi kararı Mert'te.

## Neden — dört tekrar

**Bu turda üç kez** (2026-08-07):

**1. `ISD-PRINT-DONT-WRITE`** — hüküm *"devir bloğunu dosyaya yazma"*, çerçeve cümlesi
*"iki geçerli yer var: `Task` çağrısının içi ya da ekran. Üçüncü bir yer yok."*
`Task` kalkınca hüküm duruyor ama cümle var olmayan bir yeri sayıyor.

**2. `arac-envanteri.md:122`** — kuralı tarif eden cümle: *"sınır şu an metinle
çiziliyor."* `ISD-KEEP-CHAIN-ONE-DEEP` kaldırılınca tarif ettiği şey ortadan kalkıyor;
atıfı silmek yetmiyor, cümle yeniden yazılmalı.

**3. `CLAUDE.md:176-178`** — *"Esnetmenin bedeli var ve iki hükümle ödeniyor:
`ISD-PRINT-AUDIT-RAW` ve `ISD-COMMIT-THEN-PUSH`."* Esnetme kalkıyor, paragrafın
çerçevesi çöküyor — **ama iki hüküm kalmalı**, ikisinin de bağımsız gerekçesi var.
Paragraf bütün olarak silinirse iki kural gerekçesiz kalır.

**Dördüncüsü daha önce kayıtlı:** Filo durumunda *"hüküm eksenini değiştirirken kapsam
cümlesi geride kalıyor"* deseni zaten üç kez tekrarlamış olarak duruyor. Bu tur onu
dörde çıkardı.

## Neden kimlik taraması yakalamıyor

Cascade taraması bir **kimliği** arıyor (`ISD-KEEP-CHAIN-ONE-DEEP` gibi). Çerçeve
cümlesi kimliği içermeyebilir — *"sınır şu an metinle çiziliyor"* cümlesinde hiçbir
kimlik geçmiyor ama o cümle kaldırılan kuralı tarif ediyor.

Yani mevcut mekanizma (atıf listesi + kimlik grep'i) bu sınıfı **yapısal olarak**
kaçırıyor.

## Ölçülmemiş olan

Bu bir desen bildirimi, henüz bir çözüm önerisi değil. Açık kalan sorular:

- Çerçeve cümlesi nasıl **bulunur**? Kimlik taraması yetmiyor; ham metin taraması
  yanlış pozitif üretiyor (kanal işinde ölçüldü: 25 "yabancı iz" bulundu, hepsi
  yanlış alarmdı).
- Bu bir **kural** mı, bir **kontrol adımı** mı, yoksa bir **araç** mı olmalı?
- Kim uygular — cascade'i yürüten (PAD) mi, denetleyen (PQA) mi?

## İlgili

- `kararlar/2026-08-07-task-kaldirildi-iletisim-kanal-ve-ekran.md` — deseni doğuran tur
- `docs/fabrika/kanal-protokolu/status.md` (agent-project) — PAM'in kaydı
