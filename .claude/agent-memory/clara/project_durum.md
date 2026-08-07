---
name: durum
description: Şu an nerede duruyoruz — açık iş, Mert'in bekleyen kararları, kapanış dokümanının adresi. Tek satırlık işaret, ayrıntı günlükte.
metadata:
  type: project
---

# Şu an nerede

**Son kapanış:** `gunluk/2026-08-07-kapanis.md` — **yeni oturum bunu okur.**

**Durum:** Sprint 4. task (fabrikanın bilgi eksiği) çalışıldı, atıf haritası onarıldı
(123 kayıt, 97/26). **Mert'in dört kararı bekliyor** + push onayı. 3. task (kanal
kurulumu) bilerek açık — kanal çalışıyor ama kanona yazılmadı.

**Fabrika kanaldan yönetiliyor:** `~/.pr-kanal/agent-project/` altında dört personel
bağlı (PAM/PAD/PQA/PCA). Yöntem `kanal-kurulumu` skill'inde.

---

Bu dosya **tek satırlık işaret** olarak tutulur. Ayrıntı üç yerde:
günlük (`gunluk/{tarih}.md`) · harita (`HARITA.md`) · kararlar (`kararlar/`).

Kural: `project` kayıtları geçicidir, iş bitince silinir —
[[feedback_gece_kapanisi_ve_hafiza_duzeni]].
