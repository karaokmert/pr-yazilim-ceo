# Araç sunucusunun zemini Coolify kalıyor — K8s bu masada değil

**Tarih:** 2026-09-04 · **Karar:** Mert · **Bağlam:** agent hafızası (RAG) ARGE turu

## Karar

Ekip araçları sunucusunun (self-hosted PR araçları — VPN burada, Coolify burada)
zemini **mevcut Coolify** olarak sabitlendi. Qdrant + embedding servisi buraya
kurulacak. K8s'e geçiş bu işin parçası değil.

## Gerekçe

**1 · "K8s + Coolify" bugün kurulabilir bir kombinasyon değil.** Ölçüldü
(2026-09-04, resmi doküman — coolify.io/docs): Coolify Docker ve Docker Swarm
destekliyor, Kubernetes "coming soon". Yani gerçek seçenek uzayı "Coolify mi,
çıplak K8s mi" idi — "K8s üstüne Coolify" değil.

**2 · Araç filosu için Coolify'ın değeri tam da basitliği.** Self-hosted araçların
neredeyse tamamı (Qdrant dahil) docker-compose ile dağıtılıyor; Coolify bunları
doğrudan yutuyor. K8s aynı iş için araç başına manifest/helm bedeli ödetir ve tek
sunucuda karşılığında bir şey vermez.

**3 · İki dünyanın ayrı zeminde durması tutarsızlık değil.** Müşteri üretimi
MicroK8s'te ve orada doğru — müşteri yükü var. Ekip araçları sunucusunda o yük yok.
İş yüküne göre doğru araç.

**4 · Kapı kapanmıyor.** Sunucu sayısı artarsa Coolify Swarm ile büyüyor; K8s
ihtiyacı gerçekten doğarsa araçlar container olduğu için taşınabilir. Karar geri
alınabilir sınıfta.

## Elenen seçenek

**Çıplak K8s'e geçiş** — Coolify'ın tek tık kurulum / env / SSL / UI değeri
kaybolur, her araç için manifest yazılır. Mert isterse ayrı bir ARGE turunda
bedeli-kazancı ölçülebilir; bu iş onu beklemez.

## Bağlam notu

Bu sunucu müşteri deploy zinciri DEĞİL — ekip araçları için açılmış ayrı sunucu
(Mert, 2026-09-04: "self hosted ekip toollarını buraya kuracak şekilde seçtik
sunucuyu"). Clara ilk turda bunu WS deploy zinciri sanıp yanlış çerçeve kurdu;
düzeltildi.
