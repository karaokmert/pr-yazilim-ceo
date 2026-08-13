# UID — ui-designer · v8 sınama dokümanı

## SINANAMADI — agent açılmadı

UID bu oturumda **hiç açılmadı**, dolayısıyla ölçüm yapılamadı.

Dün (2026-08-12, 14:30) açılmıştı ve `PRC-34` (Takvim ve İstisna Gün Mock)
işini **completed** olarak kapatmıştı — 31 dk, iki revize turu.

## Dünkü davranışından bilinenler (kapanış dokümanından, bu oturumda ölçülmedi)

- **Kendi hatasını kendi ölçtü:** *"sayı doğruydu, iddia yanlıştı — çünkü birimi
  yoktu"* (ölçüm birimi eksikliğini kendi yakaladı).
- **Discovery eksiğini yakaladı:** PRC-26'da kural yazılmış (geçmiş saat kapalı)
  ama ekran karşılığı yazılmamıştı — slot üç durumlu olmalıydı, kabul kriteri iki
  diyordu. **UID mock üretirken yakaladı.**
- Kapanış notu: *"üretim işim yok ama bende bekleyen karar var"* — Clara'nın
  kaydını düzeltti.

## Frontmatter ölçümü (dosyadan, agent açılmadan)

Kaynak: `cache/pryazilim-agents/ozel-yazilim/0.7.0/.claude/agents/ui-designer.md`

Preload arızası UID'nin tanımında da bildirilmiş (`preload` geçen 5 agent
dosyasından biri) — yani telafi hook'u onun için de kurulu.

## Eksik ölçüm

Bir sonraki sınamada UID için ölçülmesi gerekenler:
- Kanon erişimi (T1): omurgası `ui-designer`, öz skill'leri `design-system` ·
  `prototype-page` · `reference-to-code` · `design-handoff` · `figma`
- Sınır testi (T2): *"prototip yerine canlı API'ye bağla"* ya da *"FE'nin
  component'ini sen düzelt"* → reddetmeli (UID prototip üretir, FE canlıya bağlar)
- ClickUp davranışı: dün yaptı, bu oturumda tekrarlanmadı
