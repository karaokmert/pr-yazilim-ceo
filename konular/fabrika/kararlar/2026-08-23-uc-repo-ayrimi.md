# Karar — Üç repo, üç ayrı iş: üreten ile üretilen ayrıldı

Tarih: 2026-08-23 · Karar: Mert · Konu: fabrika

## Mert'in cümlesi

> *"CEO (senin repon) · fabrika-v2 fabrika ekip reposu · skill-project takımların
> reposu. Artık skill-project'te üretim ekibi yaşamayacak, sadece takımlar
> yaşayacak. Sen kendi reponda, üretim ekibi fabrika-v2'de yaşayacak."*

## Karar

| Repo | Ne yaşar |
|---|---|
| `pr-yazilim-ceo` | **Clara** — kanon, skill'ler, kayıtlar |
| `fabrika-v2` | **üretim ekibi** — FPA / FPD / FQA |
| `skill-project` | **takımlar** — `v8/` altında OY · WS · n8n |

## Gerekçe

**Üreten ile üretilen ayrışır.** Fabrika kendi reposunda oturur, ürettiği takımlar
kendi havuzunda birikir. Karışık durduğunda iki soru cevapsız kalıyordu: bir
takımın kanonu mu değişti yoksa fabrikanın kanonu mu, ve bir dosyanın hangi kuşağa
ait olduğu.

## Ölçülmüş durum — dosyalar taşınmadı

`skill-project/.claude/agents/` altında **eski üretim ekibi hâlâ duruyor:**
`pr-agent-manager` · `pr-agent-developer` · `pr-agent-qa` ·
`pr-agent-context-analyst` · `agent-generator` · `ag-qa`.

Kanon taşındı, dosyalar taşınmadı. Orada bir agent açılırsa **dünün kanonunu
yükler** ve bunu kimse fark etmez — arıza sessiz.

⚠️ Bu bir **açık kalem**: temizliği fabrikanın işi (o repoya Clara yazmaz).
Fabrikaya iş emri olarak gitmesi gerekiyor.

## Yürürlükteki hâli

- Clara gövdesi: "Üç repo, üç ayrı iş" tablosu
- `pr-yazilim-ceo/CLAUDE.md`: "Bakılan yerler" bölümü
- `~/.claude/CLAUDE.md`: tüm agent'ları bağlayan üç repo maddesi
