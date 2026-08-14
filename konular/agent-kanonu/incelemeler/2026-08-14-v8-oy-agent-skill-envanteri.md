# V8 Özel Yazılım — Agent / Skill Envanteri

**Ölçüm:** 2026-08-14 · **Kaynak:** `v8/ozel-yazilim` (plugin 0.7.0, marketplace `source` ile doğrulandı)
**Kapsam:** 9 agent · 77 skill · yönlendirme ölçümü main SKILL.md içindeki backtick atıflarıyla yapıldı

---

## Ortak preload çekirdeği (dokuz agentın hepsinde)

- `behavior`
- `handoff`
- `memory-management`
- `is-akisi`
- `pr-yazilim-oy-envanteri`

Aşağıdaki listelerde bu beşi **tekrar yazılmadı** — yalnız agenta özel preload'lar gösterildi.

---

# Agent Listesi

## project-assistant

**Alanı:** Proje yöneticisi — gereksinim, discovery, orkestrasyon, bug triyaj, ClickUp. Kod okur ama yazmaz; teknik direktif vermez.

**Main skill:** `project-assistant`

### 1. Preloaded skiller (8)

Ortak çekirdek (5) + agenta özel:

- `project-assistant` ← **main**
- `dev-deploy`
- `prod-deploy`

### 2. On-demand skiller (10) — main skill bunları yönlendiriyor

- `bug-triyaj`
- `clickup`
- `danisma`
- `discovery`
- `figma`
- `impact-analiz`
- `orkestrasyon`
- `proje-dosya-duzeni`
- `proje-islemleri`
- `project-planning`

---

## ui-designer

**Alanı:** UI tasarımcı — Figma/gereksinim/hazır kod → PR Yazılım kanonuna çeviri. Prototip KODU üretir (mock veriyle), FE canlı API bağlar.

**Main skill:** `ui-designer`

### 1. Preloaded skiller (6)

Ortak çekirdek (5) + agenta özel:

- `ui-designer` ← **main**

### 2. On-demand skiller (12) — main skill bunları yönlendiriyor

- `code-quality`
- `component`
- `database`
- `design-handoff`
- `design-system`
- `enum-sync`
- `figma`
- `prototype-page`
- `reference-to-code`
- `response-request`
- `screen-structure`
- `tasarim-prensipleri`

---

## backend-developer

**Alanı:** Senior backend (.NET/C#) — entity, handler, DataLayer, SQL migration, API.md sözleşmesi. Ürüne kod commit'ler; push QA'da.

**Main skill:** `backend`

### 1. Preloaded skiller (6)

Ortak çekirdek (5) + agenta özel:

- `backend` ← **main**

### 2. On-demand skiller (21) — main skill bunları yönlendiriyor

- `acs-gorusme`
- `api-project`
- `auth`
- `code-quality`
- `cronjob`
- `database`
- `dev-environment`
- `enum-sync`
- `excel-export`
- `gosterim-formatlari`
- `iap`
- `local-payment`
- `messaging`
- `module-development`
- `notification`
- `pryazilim-core`
- `realtime`
- `response-request`
- `search`
- `tasarim-prensipleri`
- `upload`

---

## frontend-developer

**Alanı:** Senior frontend (Next.js/React/Tailwind) — component, hook, form, tablo, API entegrasyonu, Playwright testi.

**Main skill:** `frontend`

### 1. Preloaded skiller (6)

Ortak çekirdek (5) + agenta özel:

- `frontend` ← **main**

### 2. On-demand skiller (19) — main skill bunları yönlendiriyor

- `auth`
- `code-quality`
- `component`
- `data-access`
- `database`
- `design-handoff`
- `dev-environment`
- `enum-sync`
- `excel-export`
- `figma`
- `form`
- `gosterim-formatlari`
- `list`
- `realtime`
- `response-request`
- `screen-structure`
- `style`
- `tasarim-prensipleri`
- `upload`

---

## mobile-developer

**Alanı:** Senior mobil (React Native/Expo) — ekran, navigation, hook, component; iOS + Android cross-platform.

**Main skill:** `mobile`

### 1. Preloaded skiller (6)

Ortak çekirdek (5) + agenta özel:

- `mobile` ← **main**

### 2. On-demand skiller (19) — main skill bunları yönlendiriyor

- `auth`
- `code-quality`
- `data-access-mobile`
- `design-handoff`
- `dev-environment`
- `enum-sync`
- `gosterim-formatlari`
- `iap`
- `local-payment`
- `mobile-release`
- `navigation-mobile`
- `notification`
- `realtime`
- `response-request`
- `screen-structure-mobile`
- `state-mobile`
- `style-mobile`
- `tasarim-prensipleri`
- `upload`

---

## qa-engineer

**Alanı:** Senior QA — STATİK kod kalite kapısı. Commit/PR inceler, kanon uyumu denetler, main'e push eder.

**Main skill:** `quality`

### 1. Preloaded skiller (8)

Ortak çekirdek (5) + agenta özel:

- `quality` ← **main**
- `dev-deploy`
- `prod-deploy`

### 2. On-demand skiller (17) — main skill bunları yönlendiriyor

- `auth`
- `backend`
- `code-auditor`
- `code-quality`
- `commit-review`
- `database`
- `enum-sync`
- `escaped-bug-analysis`
- `frontend`
- `mobile`
- `module-audit`
- `module-development`
- `orkestrasyon`
- `production-audit`
- `response-request`
- `setup-ozelyazilim-plugin`
- `style-mobile`

---

## test-engineer

**Alanı:** Test engineer — çalıştıran tek agent. E2E senaryo, hata repro, test ortamı + veri kurulumu.

**Main skill:** `test-engineer`

### 1. Preloaded skiller (6)

Ortak çekirdek (5) + agenta özel:

- `test-engineer` ← **main**

### 2. On-demand skiller (10) — main skill bunları yönlendiriyor

- `backend`
- `code-auditor`
- `code-quality`
- `data-access`
- `database`
- `dev-environment`
- `e2e-verification`
- `quality`
- `repro-diagnosis`
- `test-data-setup`

---

## code-auditor

**Alanı:** Code auditor + etki analisti — derin statik analiz. Etki haritası ve tüm-proje yapısal audit; kod/direktif yazmaz.

**Main skill:** `code-auditor`

### 1. Preloaded skiller (6)

Ortak çekirdek (5) + agenta özel:

- `code-auditor` ← **main**

### 2. On-demand skiller (6) — main skill bunları yönlendiriyor

- `code-quality`
- `impact-analiz`
- `impact-analysis`
- `module-audit`
- `project-assistant`
- `structural-audit`

---

## devops-engineer

**Alanı:** Senior DevOps — Docker, K8s (MicroK8s), CI/CD, gateway, secret, Telepresence, EAS/store dağıtımı. Kaynak kod yazmaz.

**Main skill:** `devops`

### 1. Preloaded skiller (8)

Ortak çekirdek (5) + agenta özel:

- `devops` ← **main**
- `dev-deploy`
- `prod-deploy`

### 2. On-demand skiller (12) — main skill bunları yönlendiriyor

- `api-project`
- `ci-cd`
- `code-quality`
- `cronjob`
- `dev-environment`
- `docker-k8s`
- `env-config`
- `iap`
- `mobile-release`
- `notification`
- `quality`
- `system-topology`

---

# Hiçbir Agentin Yönlendirme Vermediği Skiller

**YOK — sıfır.**

77 skillin 77'si en az bir agentın ya preload listesinde ya da bir main skillin backtick yönlendirmesinde geçiyor.

⚠️ **Ölçümün sınırı:** bu, *yönlendirme satırı var* demektir — *yönlendirme doğru tetikliyor* demek DEĞİL.
Bir main skill `- **Excel içe/dışa aktarma** → `excel-export`` yazmışsa bu ölçümde kapsanmış sayılır;
o satırın agentı gerçekten doğru anda o skile götürüp götürmediği **ölçülmedi.**
Senin istediğin yönlendirme skili tam bu boşluğu kapatacak.
