---
name: mert-tabirler
description: Mert'in kendine özgü tabirleri ve karşılık geldiği yerler — "VS Code kısa yol" gibi ifadelerin sözlüğü
metadata:
  type: user
---

# Mert ile tabirler

Mert'in bir şeyi kendi adıyla değil **işlevi**yle andığı durumlar. Buradaki her satır
bir yanlış anlama sonrası yazıldı — yani bunlar tahmin değil, düzeltme kaydı.

**Why:** Aynı ifadeyi ikinci kez yanlış yorumlamak zaman yakıyor ve Mert'i kendini
tekrar etmeye zorluyor. Kendi cümlesi: *"tekrardan anlatmak zorunda kalmıyım."*

**How to apply:** Bir tabir bu listede varsa doğrudan oraya git, teyit sorma. Listede
yoksa ve birden fazla okuması varsa **bakmadan önce sor** — üç aday sıralamak, yanlış
dosyayı açıp geri dönmekten hızlı.

---

## "VS Code kısa yol"

**Anlamı:** `settings.json` içindeki `terminal.integrated.profiles.osx` — agent'ları
terminalden tıklamayla çağıran terminal profilleri. Her profil bir agent'ı
`claude --agent <isim>` ile açıyor, isminde tarih + klasör damgası var.

**Dosya:** `~/Library/Application Support/Code/User/settings.json`

**NE DEĞİL:** `keybindings.json` (tuş kısayolları — orada tek kayıt var, terminalde
shift+enter, ona dokunulmaz). "Son açılan projeler" listesi de değil.

**Gelen tipik istek:** kısa yol ekle / çıkart / sırala / geçersizi kaldır.

**Sıralama = JSON anahtar sırası.** VS Code profilleri dosyadaki yazım sırasına göre
gösteriyor, alfabetik değil. "Şunu en üste al" denince anahtar bloğu
`terminal.integrated.profiles.osx` objesinin başına taşınır.

**Bilinmesi gereken:** profil adı `Grup · Rol` biçiminde (`OY · BE`, `Web · FSD`).
Bir profilin ölü olup olmadığı, işaret ettiği agent'ın gerçekten var olmasına bakılarak
ölçülür — plugin'li isimler (`ozel-yazilim:backend-developer`) geçerli, çıplak isimler
(`backend-developer`) v7 kalıntısı ve `~/.claude/agents/` boş olduğu için ölü.

**2026-08-04 durumu — 36 → 21 profil, sıra: Clara → Web (7) → OY (9) → fabrika (4).**
Silinenler: OY7 grubu (9, ölü v7 hedefi), AG + AG-QA (agent üretimi artık fabrikada),
SM + TM (aynı eski marketplace), v8-PAM + v8-PQA (PAM/PQA kopyası). Ölçüm ve gerekçe:
`gunluk/2026-08-04.md`.

**Eğilim:** Mert emekli kuşağı listede tutmuyor. Bir profil artık yürürlükte olmayan
bir yapıya işaret ediyorsa kaldırılır — *"onları da artık öldürcez"*. Yani ölü profil
bulduğumda önerinin yönü belli: silme tarafı.

İlgili: [[mert-profil]]
