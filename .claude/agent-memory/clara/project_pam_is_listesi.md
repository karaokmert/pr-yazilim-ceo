---
name: pam-is-listesi
description: PAM'e iletilecek işlerin listesi — hazır gereksinimler ve kanona girmesi gereken kararlar. Bir iş fabrikaya gitmeye hazır olduğunda buraya yazılır, iletildiğinde satırı silinir.
metadata:
  type: project
---

# PAM'e iletilecek iş listesi

## Fabrikaya gidecek gereksinim adayları (N8N oturumundan, 2026-08-09)

1. **`validate && commit` yasağı** — `claude plugin validate` başarısızlıkta
   rc=0 dönüyor; doğrulama ÇIKTIYLA kanıtlanır. Kanıt:
   `incelemeler/plugin-validate-cikis-kodu.md`
2. **Sessizlik türleri + merkez kuralları** — dört tür ölçüldü; "beyan başlama
   değildir, merkez tetik atar" + "takılan agent'ın üç hâli" kural adayları.
   Kanıt: `arge/agent-oturum-modu/onay-akisi-tikanmasi.md`
3. **`uretim-standardi` yetimliği** — üretici katmanda var, dağıtımda yok,
   fabrika kanonu atıf vermiyor. Karar: kullanılacak mı, emekli mi?
4. **`<araclar>` yer tutucusu** — kanal.md'de tanımsız; asset taşınınca çözülür.
5. **Denetçinin durma eşiği** — bulgu sınıflaması (durduran/işaretlenen) kanona.
6. **Rol açma testi** — skill 3 kapıdan geçiyor, rol hiçbirinden
   (üretim-refleksi gereksinimi PAD kuyruğunda — bu kalem onun parçası).

Eski kalemler: brief biçimi kanona girdi (üretim-refleksi) · kanal protokolü
kanon işi asset taşımayla birleşti · fabrika denetimi 6 önceliğinin çoğu kapandı
(cascade ✓, Task→Agent ✓, N8N sıfırdan-üretimi ✓).
