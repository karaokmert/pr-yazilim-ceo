# VPN kararları — 2026-08-28

Üç karar verildi ve bir varsayım çürüdü. Hepsi wg-easy'nin **Exited** durumunu
çözerken çıktı — arıza teşhisi, arkasındaki asıl soruyu (bu araç doğru araç mı, ne için
kuruyoruz) açtı.

---

## Karar 1 — VPN'in işi sabit çıkış IP'si, mesh değil

**Ne:** WireGuard + wg-easy ile merkezî bir VPN. Tailscale/Headscale gibi mesh
çözümler elendi.

**Neden:** Mert'in cümlesi belirledi — *"ekibin nerede olursa olsun VPN ile hep sabit
IP'yi kullanması; bu sayede SQL Server'a erişimi tek IP'ye indirebilirim, müşteriye tek
IP verebilirim."*

İş modeli bunu zorunlu kılıyor: PR Yazılım Azure servislerine, kendi MSSQL'ine ve **dış
müşterilerin sunucularına** erişerek çalışıyor. Bu servislerin firewall'ları IP bazlı
kısıtlanacak, dolayısıyla çıkışın tek ve öngörülebilir bir adresten olması gerekiyor.

⚠️ **Ayrım şuydu:** mesh (Tailscale/Headscale) *iç servislere erişim* problemini daha
iyi çözer — cihazlar birbirine doğrudan bağlanır, merkez düşse de ayakta kalır. Ama
*sabit çıkış IP'si* problemini doğrudan çözmez; onun için ayrıca bir çıkış düğümü
tanımlamak gerekir. Bizim asıl ihtiyacımız ikincisi olduğu için merkezî çözüm kazandı.

**Bunun anlamı:** VPN artık bir kolaylık değil, **müşteriye verilen bir taahhüdün
altyapısı.**

---

## Karar 2 — full-tunnel, ihtiyaç oldukça açılıp kapanan

**Ne:** VPN açıkken tüm trafik tünelden geçer (split-tunnel değil). Ama ekip VPN'i
sürekli açık tutmayacak — yalnız bu servislerle iş yaparken açacak.

**Neden split değil:** Müşteri sunucusuna hangi adresten, hangi porttan gidileceği
önceden bilinmiyor. Split-tunnel'da her yeni müşteri için "şu adresi de tünele ekleyin"
demek gerekir; unutulan biri sessizce kişisel IP'den çıkar ve **bunu fark etme şeklin
müşterinin firewall'ına takılmak olur.** Full-tunnel bu defter tutma işini ortadan
kaldırıyor.

**Bedelleri — ve neden kabul edilebilir oldukları:**

TR→Helsinki ~50-65ms gecikme tüm trafiğe biner. Ama VPN sürekli açık olmayacağı için
bu bedel **yalnız o işi yaparken** ödeniyor — ve o iş zaten uzak servislere (Azure,
MSSQL, müşteri sunucusu) gidiyor, gecikme oraya nasılsa var.

EX44 düşerse ekip internetsiz kalmaz — VPN'i kapatır, normal işine devam eder. Duran
şey yalnız bu servislere erişim olur.

⚠️ **Bu ikinci nokta bir düzeltmeyle geldi.** Clara önce full-tunnel'ı duyunca "EX44
artık ekibin çalışma şartı, felaket senaryosu değişmeli" dedi. Mert *"ekip VPN'i her
zaman değil, sadece bu servislere işlem yaparken kullanacak"* deyince abartı çöktü.
Runbook §9'daki felaket senaryosu **olduğu gibi geçerli** — EX44 hâlâ "yeniden
kurulabilir bir araç sunucusu".

**Ders:** bir kararın bedelini hesaplarken **kullanım sıklığını** sormadan hesaplama.
Aynı mimari karar, sürekli açık bir VPN'de kritik, ihtiyaç oldukça açılan bir VPN'de
sıradan.

---

## Karar 3 — wg-easy v15, ve `latest` bırakılmaz

**Ne:** Image `ghcr.io/wg-easy/wg-easy:latest` yerine `:15`. Coolify şablonundan
`entrypoint` bloğu ve `_PASSWORD` satırı silindi, `WG_HOST` doğrudan IP'ye
(`65.109.150.95`) sabitlendi, `restart: unless-stopped` eklendi.

**Neden v15 (v14'e sabitlemek yerine):** v14 artık geliştirilmiyor — güvenlik yaması
gelmez ve bir gün taşımak zorunda kalınır. Makine yeni kuruluyor; ilk günden emekli bir
sürüme sabitlemek birkaç ay sonra aynı işi tekrar yapmak demek. Ayrıca silinen şey zaten
**bozuk olan kısımdı** — yama değil, kaldırma.

**Neden `latest` bırakılmaz:** Bugünkü arızanın kaynağı tam olarak buydu. Kurulduğu gün
çalışan bir compose, bir sonraki image pull'unda sessizce bozulur. Hiçbir şey hata
vermez — container ölür, "Exited" yazar, sebebi görünmez.

---

## Çürüyen varsayım — devir paketi ölçüm değildir

Claude Desktop'tan gelen transcript *"wg-easy servisi eklendi, status Exited"* diyordu.
Mert *"sunucuda kurulum yok ki, boş geliyor"* deyince Clara bunu "servis hiç
yaratılmamış" diye okudu ve üç senaryo üretti (makine yeniden kuruldu / yanlış makinedeyiz
/ paket olmayan bir şeyi anlatıyor).

**Üçü de yanlıştı.** Ekran görüntüsü gelince görüldü: servis duruyordu, Exited'dı — yani
devir paketi doğruydu, Mert'in kastettiği container'ın ayakta olmadığıydı.

⚠️ **Ders:** elde ölçüm yokken senaryo üretme. Bir cümle iki türlü okunabiliyorsa
**tek komut sorup beklemek**, üç ihtimal kurmaktan hızlıdır. Clara burada kendi
çıkarımını veri sanmaya başlamıştı.

---

## Açık kalan — Floating IP

Sabit IP artık müşteriye verilen bir taahhüt. Hetzner'da makine değişirse IP değişir ve
o an **her müşterinin firewall'ında kural güncellemek** gerekir.

Hetzner'ın **Floating IP** ürünü bunu çözüyor: makineden bağımsız, taşınabilir adres.
Bugün EX44'e bağlanır, yarın başka makineye taşınır, müşteri fark etmez.

⚠️ **Ölçülmedi:** Floating IP bir Hetzner **Cloud** ürünü; EX44 **dedicated**. Dedicated
tarafta karşılığının ne olduğu (ek IP satın alma? subnet?) doğrulanmadı. Kurulumu bloke
etmiyor — sonradan da taşınabilir — ama taahhüt verilmeden önce netleşmeli.
