# Karar: Devir bloğu Mert'in onayıyla SendMessage ile iletilir

**Tarih:** 2026-08-19 · **Karar mercii:** Mert · **Etkilenen:** `CLA-NO-CALL-TEAMS`

## Karar

Clara, hazırladığı devir bloğunu **Mert'in onayıyla** `SendMessage` aracıyla hedef
agent'a doğrudan iletir. Mert'in taşıyıcı olması şartı kalktı.

Mert'in cümlesi: *"benim onayımla handoffu send message ile iletiyorsun."*

## Ne değişti, ne değişmedi

**Değişen:** taşıma yolu. Blok artık kopyalanıp yapıştırılmıyor; Clara iletiyor.

**Değişmeyen — ve bu kısım kritik:**

1. **Onay hâlâ şart.** Blok önce Mert'e gösterilir, o "ilet" der, sonra gidilir.
   Onaysız iletim yok. Bu, `CLA-ASK-BEFORE-WRITING-OUT` ile aynı mantık: kapı
   kaldırılmadı, kapıdan geçme biçimi değişti.

2. **Görünürlük şartı hâlâ ayakta.** `CLA-TRACK-WHAT-YOU-SEND` yürürlükte —
   verilen iş listeye girer, dönen rapor Mert'e **aynen** basılır. Bu kural
   olmasa yeni yol Mert'i takipten koparırdı ve o zaman Clara devre dışı kalırdı
   (Mert'in kendi ölçütü).

3. **İş verme yasağı değişmedi.** Clara agent'a iş TANIMLAMAZ, hazırlanmış ve
   onaylanmış bir bloğu TAŞIR. Hedef kıdemlidir ve kendi kanonunu uygular;
   Clara direktif yazmaz, bulguyu yazar.

## Gerekçe

Eski kuralın dayanağı 2026-07-30 ölçümüydü: bir agent diğerini çağırdığında rapor
kullanıcıya değil **çağırana** gider, zincir görünmez olur, hata da görünmez olur.

O gerekçe `Agent` aracı için geçerliydi — çağırmak hedefi alt göreve dönüştürür.
`SendMessage` farklı bir mekanik: hedef **kendi oturumunda kalır**, kendi kapısını
kendi açar, raporunu kendi kullanıcısına verir. Yani görünürlük kaybı otomatik değil.

Kalan risk, raporun Mert'e ulaşmaması. Onu iki şey kapatıyor: onay kapısı (blok
gitmeden Mert görür) ve rapor basma zorunluluğu (dönen cevap ham hâliyle ekrana).

## Uygulama

- `clara.md` → `CLA-NO-CALL-TEAMS` gövdesi güncellendi
- `.claude/skills/sendmessage-akisi/` → Clara'nın iletim yetkisi eklenecek (ayrı iş)

## İlk uygulama

Aynı gün, RED-2 devir bloğu PAM'e (`PAM · Lider - 0819-18:20`) iletildi.
İçerik: deneyin kanona girmemiş iki çıkarımı (`URT-NO-CONTENT-IN-DESCRIPTION`
gerekçesinin ölçümle kapatılamaması + yeni agent tipinin oturum içinde
çağrılamaması).
