# Coolify tek-tık servis envanteri — 2026-09-05

Kaynak: coolify.io/services (340 girdi; "X with Postgres/MySQL/MariaDB" gibi sürüm çeşitleri tek sayıldı → ~290 araç).
Yazan: Clara (web). Tanımlar genel bilgi, ölçülmedi. Etiket bizim için:

- **[kurulu]** bugün tools sunucusunda var
- **[OY]** özel yazılım projelerinde aday
- **[WS]** websitesi projelerinde aday
- **[araç]** kendi tools sunucumuza aday (ekip/ajan altyapısı)
- **[ofis]** ofis içi / eğlence
- **[satış]** müşteriye "kendi sunucunda" satılabilir
- **[–]** bizim için konu değil

---

## 1 · İlişkisel ve belge veritabanları
- **PostgreSQL** — standart ilişkisel DB. [araç][OY]
- **MySQL** — web dünyasının klasik ilişkisel DB'si. [WS]
- **MariaDB** — MySQL'in topluluk çatalı, yerine geçer. [WS]
- **MongoDB** — JSON belge tabanlı NoSQL. [–]
- **ClickHouse** — sütun tabanlı analitik DB; olay yığını üstünde toplama sorgusu. [OY-aday, hafıza: arge-clickhouse]
- **InfluxDB** — zaman serisi DB; metrik/sensör verisi. [OY-IoT]
- **DenoKV** — Deno'nun anahtar-değer DB'si. [–]
- **Autobase** — Postgres için kendi barındırdığın yönetilen-DB (yedek, yüksek erişilebilirlik). [–]
- **Neon WS Proxy** — Neon serverless Postgres'e websocket köprüsü. [–]

## 2 · Bellek-içi depo / önbellek
- **Redis** — anahtar-değer; önbellek, oturum, kuyruk. [kurulu-n8n içinde][OY][araç]
- **KeyDB** — çok çekirdekli Redis çatalı; geliştirmesi yavaşladı. [–]
- **Dragonfly** — Redis/Memcached uyumlu, yüksek hacim için. [–, hafıza: arge-redis-sinifi]

## 3 · Vektör veritabanı
- **Qdrant** — vektör arama; hafızamız bunun üstünde. [kurulu][araç]
- **Weaviate** — vektör + yapısal filtre, modül sistemi. [–]
- **Chroma** — hafif vektör DB, prototip için. [–]

## 4 · Metin arama motoru
- **Meilisearch** — anlık arama, yazım toleransı, facet; tek konteyner. [OY-aday, hafıza: arge-meilisearch]
- **Typesense** — Meilisearch sınıfı, şema önceden, küme desteği. [OY-aday]
- **Elasticsearch** — büyük ölçek arama + log analitiği; ağır. [–]
- **Elasticsearch + Kibana** — Elastic + görselleştirme paneli. [–]

## 5 · Meta arama (Google önyüzü)
- **SearXNG** — 70+ motoru toplayan gizlilik odaklı arama. [araç-ajanlar için web arama]
- **Whoogle** — Google sonuçlarını takipsiz gösteren önyüz. [–]

## 6 · Veritabanı yönetim ve yedek
- **pgAdmin** — Postgres web yönetimi. [araç]
- **phpMyAdmin** — MySQL/MariaDB web yönetimi. [WS]
- **CloudBeaver** — çok-DB web istemcisi (DBeaver'ın web'i). [araç]
- **Redis Insight** — Redis görsel istemci. [araç]
- **Drizzle Gateway** — Drizzle ORM için web stüdyo. [–]
- **Databasus** — Postgres/MySQL/Mongo zamanlı yedek. [araç]
- **Pgbackweb** — Postgres yedek, web arayüzlü. [araç]
- **Sequin** — Postgres değişikliklerini (CDC) kuyruğa/HTTP'ye akıtır. [OY-aday]

## 7 · LLM sohbet arayüzü
- **Open WebUI** — ChatGPT benzeri arayüz; Ollama/OpenAI API. [araç]
- **Ollama + Open WebUI** — üstteki + yerel model çalıştırıcı. [araç-GPU gerekir]
- **LibreChat** — çok modelli sohbet arayüzü, ajan/araç desteği. [araç]
- **Lobe Chat** — modern tasarımlı çok modelli sohbet. [–]

## 8 · LLM gateway
- **LiteLLM** — tüm LLM API'lerini tek OpenAI-biçimli kapıya toplar; anahtar, kota, maliyet. [araç-öncelikli]
- **NewAPI** — LLM gateway + AI varlık yönetimi (Çin kökenli). [–]

## 9 · LLM akış ve ajan platformları
- **Flowise** — sürükle-bırak LLM akışı / RAG / ajan. [satış-chatbot]
- **Flowise with Databases** — üstteki + Postgres/Redis paketli. [satış]
- **Langflow** — Python tabanlı görsel LLM akışı. [–]
- **AnythingLLM** — belge yükle-konuş, hazır RAG uygulaması. [ofis][satış]
- **MindsDB** — DB'ye SQL ile AI modeli bağlar. [–]
- **Hermes Agent (WebUI)** — kalıcı hafızalı otonom ajan + web sohbet. [–]
- **Spacebot** — düşün/çalış/hatırla süreçli ajan sistemi. [–]
- **Openclaw** — çok sağlayıcılı AI kod asistanı + tarayıcı otomasyonu. [–]
- **Jean** — AI kod ajanlarını orkestre eden masaüstü/sunucu istemci (coollabs). [araç-izle]
- **MetaMCP** — MCP sunucularını toplayıp tek kapıdan sunar. [araç-aday]

## 10 · LLM gözlem, veri ve çeviri
- **Langfuse** — LLM çağrı izi: prompt, cevap, token, süre, maliyet. [araç-öncelikli]
- **Label Studio** — veri etiketleme (metin/görsel/ses). [–]
- **Argilla** — AI için veri kümesi kürasyon aracı. [–]
- **Unstructured** — PDF/Office belgeleri RAG için parçalar. [araç-aday]
- **LibreTranslate** — kendi makine çevirisi API'si. [araç-aday]

## 11 · İş akışı otomasyonu
- **n8n** — genel amaçlı akış; üç şablon (sade / Postgres / Postgres+Worker). [kurulu]
- **Activepieces** — Zapier'e yakın, daha basit n8n rakibi. [–]
- **Windmill** — script'lerden akış ve iç araç üretir; geliştirici odaklı. [–]
- **Budibase** — low-code iş uygulaması + akış. [–]
- **Mage AI** — veri boru hattı (ETL) aracı. [–]
- **Prefect** — Python iş akışı orkestrasyonu (Airflow sınıfı). [–]

## 12 · Arka plan iş / kuyruk motoru (kod tarafı)
- **Trigger.dev** — TypeScript arka plan işleri; tekrar deneme, zamanlama, uzun süren iş. [WS-aday]
- **Inngest** — olay tetikli dayanıklı iş akışı motoru. [WS-aday]
- **Hatchet** — yüksek hacimli görev kuyruğu + akış. [–]

## 13 · Mesaj broker / gerçek zaman
- **RabbitMQ** — servisler arası mesaj kuyruğu; OY kanonu bunu kullanıyor. [OY]
- **Mosquitto** — hafif MQTT broker (IoT). [OY-IoT]
- **EMQX Enterprise** — ölçekli MQTT broker. [OY-IoT]
- **Soketi** — Pusher uyumlu WebSocket sunucu. [WS-aday]
- **Soketi App Manager** — Soketi uygulama yönetim paneli. [WS-aday]

## 14 · Ekip sohbeti ve topluluk
- **Mattermost** — kendi Slack'in. [satış]
- **Rocket.Chat** — kurumsal sohbet, güvenlik odaklı. [satış]
- **Matrix Synapse** — federatif, uçtan uca şifreli sohbet sunucusu. [–]
- **Once Campfire** — 37signals'ın tek odalı basit grup sohbeti. [ofis]
- **NodeBB** — forum/tartışma platformu. [satış]
- **Soju** — IRC bouncer. [–]
- **Buzz** — insan + AI ajan ortak çalışma alanı (Nostr). [–]

## 15 · Görüntülü görüşme
- **Jitsi** — kendi video konferansın; ACS'in adayı, kayıt ayrı (Jibri). [OY-aday, ağır]

## 16 · Push bildirim
- **ntfy** — HTTP ile telefona bildirim; en ucuz "iş bitti" haberi. [araç-öncelikli]
- **Gotify** — kendi bildirim sunucun + mobil uygulama. [araç]
- **Apprise API** — 80+ bildirim kanalına tek API. [araç-aday]

## 17 · WhatsApp / çok kanallı mesaj API
- **Evolution API** — WhatsApp'ı API'ye çevirir (resmi değil, hesap riski). [OY-aday]
- **Gowa** — Go ile yazılmış hafif WhatsApp web API. [OY-aday]

## 18 · Müşteri destek / helpdesk
- **Chatwoot** — çok kanallı gelen kutusu (WhatsApp, web chat, mail). [araç-aday][satış]
- **Chaskiq** — pazarlama/destek mesajlaşma platformu. [–]
- **FreeScout** — hafif paylaşımlı gelen kutusu (Laravel). [araç-aday]
- **osTicket** — klasik destek bileti sistemi. [–]
- **GLPI** — BT varlık + servis masası (ITSM). [–]

## 19 · CRM / ERP / İK
- **EspoCRM** — açık kaynak CRM. [satış]
- **Twenty** — modern CRM (Notion hissi). [araç-aday]
- **Odoo** — tam ERP paketi (satış, stok, muhasebe, İK). [satış]
- **Dolibarr** — KOBİ ERP/CRM. [satış]
- **OrangeHRM** — İK yönetimi. [–]

## 20 · E-posta
- **Usesend** — Resend/SendGrid alternatifi, AWS SES üstünden gönderim. [araç-aday]
- **Plunk** — AWS için açık kaynak e-posta platformu. [araç-aday]
- **Listmonk** — bülten ve liste yönetimi. [araç-aday][WS]
- **Stalwart** — tam mail sunucusu (IMAP/SMTP/JMAP). [–, bakım ağır]
- **Mailpit** — sahte SMTP; geliştirme ortamında maili yakalar. [OY][WS-dev]
- **Open Archiver** — e-posta arşivleme, tam metin arama. [–]
- **Sessy** — e-posta sistemleri gözlem/analiz. [–]

## 21 · Form, anket, geri bildirim
- **Formbricks** — ürün içi anket platformu. [WS-aday]
- **HeyForm** — sohbet tarzı form/anket. [WS-aday]
- **OpnForm** — form oluşturucu (Typeform benzeri). [WS-aday]
- **LimeSurvey** — klasik anket aracı. [–]
- **Fider** — kullanıcı geri bildirimi/özellik oylama. [satış]

## 22 · Proje ve görev yönetimi
- **Plane** — Jira/Linear alternatifi proje aracı. [–, ClickUp var]
- **Leantime** — hedef odaklı proje yönetimi. [–]
- **Redmine** — klasik proje yönetimi. [–]
- **Vikunja** — yapılacaklar/görev uygulaması. [–]
- **Fizzy** — 37signals kanban. [–]

## 23 · Zaman takibi ve randevu
- **Kimai** — zaman takibi. [–, ClickUp'ta çözüldü]
- **Rallly** — toplantı saati oylama (Doodle). [ofis]
- **Easyappointments** — online randevu planlayıcı. [satış]

## 24 · E-imza
- **Documenso** — açık kaynak belge imzalama. [araç-aday]
- **DocuSeal** — DocuSign alternatifi, form alanlı imza. [araç-aday][satış]

## 25 · Low-code / tablo uygulamaları
- **NocoDB** — DB'yi Airtable gibi gösterir. [araç-aday]
- **Teable** — Postgres üstü görsel tablo arayüzü. [araç-aday]
- **Grist** — ilişkisel hesap tablosu. [–]
- **Appsmith** — iç araç (admin panel) üreticisi. [araç-aday]
- **Lowcoder** — iç araç üreticisi (OpenBlocks çatalı). [–]
- **NocoBase** — AI destekli no-code/low-code platform. [–]

## 26 · Wiki / dokümantasyon
- **BookStack** — kitap/bölüm/sayfa yapılı wiki. [ofis-aday]
- **Wiki.js** — güçlü, eklentili wiki. [–]
- **DokuWiki** — dosya tabanlı hafif wiki. [–]
- **MediaWiki** — Wikipedia'nın motoru. [–]
- **Outline** — ekip bilgi tabanı (Notion hissi). [ofis-aday]
- **Docmost** — ortak çalışmalı wiki. [–]

## 27 · Not ve kişisel bilgi yönetimi
- **AppFlowy** — Notion alternatifi çalışma alanı. [–]
- **Affine** — Notion + Miro karışımı. [–]
- **Alexandrie** — hızlı Markdown çalışma alanı. [–]
- **SilverBullet** — Markdown tabanlı kişisel bilgi sistemi. [–]
- **SiYuan** — blok tabanlı not uygulaması. [–]
- **TriliumNext** — hiyerarşik not/bilgi tabanı. [–]
- **Memos** — hafif, hızlı not (Twitter-tarzı). [–]
- **Joplin** — Joplin not uygulamasının senkron sunucusu. [–]
- **CodiMD** — gerçek zamanlı ortak Markdown. [–]

## 28 · Yer imi, okuma, RSS
- **Karakeep** — link/not/görsel kaydet, AI etiketler. [ofis-aday]
- **Linkding / Linkding Plus** — minimal yer imi yöneticisi (+arşiv). [–]
- **Readeck** — "sonra oku" içerik kaydedici. [–]
- **FreshRSS** — RSS okuyucu. [–]
- **Miniflux** — minimalist RSS okuyucu. [–]
- **Glance** — RSS + hava + takvim tek pano. [ofis-aday]
- **Redlib** — Reddit gizlilik önyüzü. [–]

## 29 · Pano / başlangıç sayfası
- **Homepage** — statik, hızlı uygulama panosu. [araç-aday]
- **Dashy** — durum kontrollü kişisel pano. [araç-aday]
- **Heimdall** — uygulama kısayol panosu. [–]
- **Homarr** — servisler için ana sayfa. [–]
- **Organizr** — homelab servis düzenleyici. [–]

## 30 · Tasarım ve çizim
- **Penpot** — Figma alternatifi tasarım/prototip. [araç-aday, Figma var]
- **Penpot with S3** — üstteki, dosyalar S3'te. [–]
- **Excalidraw** — el çizimi hissiyle beyaz tahta. [ofis]

## 31 · CMS ve site
- **WordPress** — üç sürüm (MySQL/MariaDB/DB'siz). [WS]
- **ClassicPress** — Gutenberg'siz WordPress; üç sürüm. [WS-aday]
- **Ghost** — yayıncılık/blog CMS'i. [WS-aday]
- **Drupal** — kurumsal CMS. [–]
- **Joomla** — klasik CMS. [–]
- **Vvveb** — görsel site/blog/e-ticaret CMS'i; üç sürüm. [–]
- **Nitropage** — görsel site oluşturucu; iki sürüm. [–]
- **Cockpit** — headless CMS, hafif. [–]
- **Directus** — DB'yi API + yönetim paneline çevirir; iki sürüm. [WS-aday]
- **Strapi** — headless CMS, API üretir. [WS-aday]
- **Moodle** — e-öğrenme platformu. [satış]

## 32 · Backend-as-a-service
- **Supabase** — açık kaynak Firebase: Postgres + auth + storage + realtime. [OY-aday]
- **Appwrite** — web/mobil için BaaS. [–]
- **PocketBase** — tek dosyalık backend (SQLite + auth + realtime). [WS-aday, küçük iş]
- **Trailbase** — Rust/SQLite hızlı uygulama sunucusu. [–]
- **Kuzzle** — genel backend yapı taşları. [–]
- **Convex** — reaktif DB/backend. [–]
- **Celld** — Deno ile dağıtık Durable Objects. [–]
- **Rivet Engine** — uzun ömürlü durumlu süreçler. [–]
- **ElectricSQL** — Postgres alt kümelerini istemciye senkronlar (local-first). [–]

## 33 · Feature flag
- **Flipt** — Git yanında feature flag. [OY-aday]
- **Unleash** — kurumsal feature flag; iki sürüm. [OY-aday]

## 34 · Dosya / PDF / görsel dönüştürme
- **Gotenberg** — HTML/Office → PDF API; fatura/rapor üretimi. [OY-öncelikli]
- **ConvertX** — 1000+ format dosya dönüştürücü, web. [ofis]
- **Vert** — yerel çalışan dosya dönüştürücü. [ofis]
- **Stirling PDF** — sunucu taraflı PDF araç kutusu (birleştir/böl/OCR/imza). [ofis]
- **Bento PDF** — PDF işlemleri tarayıcıda, sunucuya çıkmaz. [ofis]
- **Imgcompress** — görsel sıkıştırma/dönüştürme/arka plan silme. [ofis][WS-aday]
- **Next Image Transformation** — Vercel görsel optimizasyonunun yerine geçer. [WS-aday]
- **FileFlows** — medya dosyalarını otomatik küçültür/işler. [–]

## 35 · Bulut dosya ve ofis
- **Nextcloud** — dosya + takvim + ofis; üç DB sürümü. [ofis-aday][satış]
- **ownCloud** — Nextcloud'un atası. [–]
- **Seafile** — hızlı dosya senkron/paylaşım. [–]
- **Pydio Cells** — kurumsal büyük dosya paylaşımı. [–]
- **LibreOffice** — tarayıcıdan ofis paketi. [–]

## 36 · Nesne depolama (S3 uyumlu)
- **Garage** — hafif, dağıtık S3 uyumlu depo. [OY-aday, Blob yerine]
- **SeaweedFS** — ölçekli dağıtık dosya sistemi, S3 uyumlu. [OY-aday]

## 37 · Dosya yönetimi ve paylaşım
- **FileBrowser** — web dosya gezgini. [araç]
- **Cloudreve** — dosya yönetim/paylaşım sistemi. [–]
- **Chibisafe** — hızlı dosya kasası/yükleme. [–]
- **Zipline** — ShareX uyumlu yükleme sunucusu. [–]
- **SFTPGo** — SFTP/FTP/WebDAV sunucusu. [OY-aday, müşteri dosya teslimi]
- **Pairdrop** — tarayıcıdan cihazlar arası AirDrop. [ofis]
- **Snapdrop** — Pairdrop'un atası. [–]
- **Syncthing** — cihazlar arası dosya senkron. [–]

## 38 · Yedekleme ve belge arşivi
- **Duplicati** — şifreli zamanlı yedek. [araç-aday]
- **Paperless-ngx** — kağıt belgeleri taranmış aranabilir arşiv. [ofis-aday]

## 39 · Medya sunucu ve kitaplık
- **Jellyfin** — açık kaynak video/müzik sunucusu. [ofis]
- **Plex** — medya sunucusu (kapalı kaynak). [–]
- **Emby** — medya sunucusu. [–]
- **Navidrome** — müzik sunucusu (Subsonic uyumlu). [ofis]
- **Audiobookshelf** — sesli kitap/podcast sunucusu. [–]
- **Calibre Web (+Automated Book Downloader)** — e-kitap kitaplığı. [–]
- **Grimmory** — kitap koleksiyonu yönetimi. [–]

## 40 · Fotoğraf
- **Immich** — Google Photos alternatifi. [ofis]
- **Ente Photos (+S3)** — uçtan uca şifreli fotoğraf. [–]

## 41 · Podcast, kayıt, indirme
- **Castopod** — podcast barındırma. [–]
- **Cap** — Loom alternatifi ekran kaydı/paylaşım. [ofis][araç-aday]
- **MeTube** — youtube-dl web arayüzü. [–]
- **qBittorrent / Transmission** — torrent istemcileri. [–]
- **Sonarr / Radarr / Prowlarr / Overseerr** — dizi/film indirme otomasyonu. [–]

## 42 · Medya ve alışkanlık takip
- **Yamtrack** — film/dizi/oyun/kitap takibi; iki sürüm. [–]
- **Ryot** — yaşam takipçisi (medya, spor). [–]
- **Embystat** — Emby istatistik. [–]

## 43 · Web analitiği
- **Umami** — hafif, çerezsiz web analitiği. [WS-öncelikli][araç]
- **Swetrix** — Avrupa merkezli çerezsiz analitik. [WS-aday]
- **Rybbit** — gizlilik-öncelikli analitik. [WS-aday]
- **GoatCounter** — çok hafif sayaç. [–]
- **OpenPanel** — Mixpanel benzeri ürün analitiği. [OY-aday]
- **Wakapi** — WakaTime uyumlu kodlama istatistiği. [–]

## 44 · İş zekâsı / rapor
- **Metabase** — DB'ye bağlan, SQL'siz pano. [araç-öncelikli, proje ekonomisi]
- **Superset** — güçlü BI (Airbnb), daha zor. [–]

## 45 · Sosyal medya
- **Mixpost** — sosyal medya planlama. [–, pazarlama başlarsa]
- **Postiz** — sosyal medya planlama. [–]

## 46 · Uptime, durum, değişim izleme
- **Uptime Kuma** — ayakta mı, düşünce bildir; üç sürüm. [araç-öncelikli — WS kanonu "monitoring yok" diyor, karar gerekir]
- **Checkmate** — sunucu/site izleme. [–]
- **Statusnook** — durum sayfası + uç nokta izleme. [araç-aday]
- **Healthchecks** — cron işi zamanında koşmadıysa haber verir. [araç-aday]
- **Changedetection** — web sayfası değişince bildirir. [–]

## 47 · Metrik ve sunucu izleme
- **Grafana (+Postgres)** — metrik/log görselleştirme. [araç-aday]
- **Beszel (+Agent)** — hafif sunucu/Docker izleme, geçmiş + alarm. [araç-öncelikli]
- **Glances** — anlık sistem izleme. [–]
- **Observium** — ağ cihazı izleme. [–]
- **Web Check** — bir siteyi analiz eden OSINT aracı. [–]

## 48 · Log, iz, hata takibi
- **SigNoz** — OpenTelemetry log+iz+metrik. [araç-aday, hacim büyüyünce]
- **OpenObserve** — log/metrik/iz/oturum kaydı, ucuz depolama. [araç-aday]
- **Glitchtip** — Sentry uyumlu hata takibi. [OY-öncelikli]
- **Bugsink** — hafif hata takibi. [OY-aday]
- **Dozzle (+Auth)** — Docker loglarını web'de izle. [araç]

## 49 · Konum
- **Traccar** — GPS takip sistemi. [OY-aday, araç filosu işi çıkarsa]

## 50 · Git sunucusu
- **Gitea (+Runner)** — hafif kendi GitHub'ın; üç DB sürümü. [–, sözleşme gerektirirse]
- **Forgejo** — Gitea'nın topluluk çatalı; üç sürüm. [–]
- **GitLab** — tam DevOps platformu; ağır. [–]
- **OneDev** — Git + CI + kanban tek pakette. [–]

## 51 · CI/CD
- **Jenkins** — klasik otomasyon sunucusu. [–]
- **GitHub Runner** — kendi sunucunda GitHub Actions koşucusu. [araç-aday, dakika kotası biterse]

## 52 · Paket ve imaj deposu
- **Docker Registry** — kendi imaj kaydın. [araç-aday, ACR yerine]
- **Nexus / Nexus ARM** — evrensel paket deposu (npm/NuGet/Docker). [–]

## 53 · Geliştirici araçları
- **Portainer** — Docker yönetim arayüzü. [–, Coolify var]
- **Code Server** — tarayıcıda VS Code. [–]
- **Hoppscotch** — Postman alternatifi API istemcisi. [araç-aday]
- **Proxyscotch** — Hoppscotch için CORS proxy. [–]
- **Jupyter Notebook** — Python not defteri. [–]
- **Marimo** — reaktif Python not defteri. [–]
- **IT Tools** — geliştirici yardımcıları (encode, hash, jwt…). [ofis]
- **Browserless** — headless Chrome servisi. [araç-aday, ajan tarama]
- **Termix** — SSH/uzak masaüstü yönetimi. [–]
- **Librespeed** — hız testi. [–]
- **CyberChef** — şifreleme/kodlama/veri analizi çakısı. [–]
- **Diun** — Docker imajı güncellenince bildirir. [araç-aday]
- **Cloudflare DDNS** — dinamik IP'yi Cloudflare'a yazar. [–]

## 54 · Kimlik ve tek giriş (SSO)
- **Authentik** — esnek kimlik sağlayıcı. [araç-aday, araç sayısı artınca]
- **Keycloak (+Postgres)** — kurumsal IAM. [OY-aday]
- **Logto** — modern kimlik çözümü. [–]
- **Pocket ID (+Postgres)** — hafif OIDC, passkey ile. [araç-aday]
- **SuperTokens** — uygulama içi auth kütüphanesi; iki sürüm. [–]

## 55 · Şifre ve sır yönetimi
- **Vaultwarden** — Bitwarden uyumlu şifre kasası. [araç-öncelikli, 1Password yerine]
- **Passbolt** — ekip şifre yöneticisi. [–]
- **Infisical** — uygulama sırları merkezi; env buradan çekilir. [araç-öncelikli]

## 56 · Güvenli paylaşım, captcha, güvenlik
- **OneTimeSecret** — tek görüntülemelik gizli link. [ofis]
- **PrivateBin** — sıfır-bilgi pastebin. [–]
- **Cryptgeon** — güvenli not/dosya paylaşımı. [–]
- **Cap Captcha** — kendi CAPTCHA'n. [WS-aday, Turnstile yerine]
- **Faraday** — zafiyet yönetimi. [–]

## 57 · Ağ, VPN, tünel
- **Cloudflared** — Cloudflare Tunnel istemcisi; portu açmadan yayınla. [araç-aday]
- **Newt (Pangolin)** — Pangolin tünel ajanı. [–]
- **Tailscale Client** — WireGuard tabanlı özel ağ. [araç-öncelikli, rag/hafıza VPN'e alınacak]
- **Netbird Client** — Tailscale alternatifi. [–]
- **WireGuard Easy** — WireGuard + web paneli. [–]
- **Pi-hole** — ağ geneli reklam engelleme. [ofis]

## 58 · Yerelleştirme
- **Tolgee** — geliştirici odaklı çeviri yönetimi. [OY-aday, çok dilli proje]
- **Weblate** — sürekli yerelleştirme. [–]

## 59 · Kısa link
- **Shlink** — URL kısaltıcı + istatistik. [WS-aday]
- **Slash** — link kısaltma/paylaşım. [–]

## 60 · Ev otomasyonu / IoT
- **Home Assistant** — ev otomasyonu. [–]
- **ESPHome** — ESP cihaz yazılımı. [–]

## 61 · Harita
- **Martin** — PostGIS'ten vektör harita tile'ı üretir. [OY-aday, harita ağırlıklı proje]

## 62 · Oyun sunucuları
- **Minecraft / Terraria / Satisfactory / Palworld** — oyun sunucuları. [ofis]
- **Foundry VTT** — masaüstü rol oyunu platformu. [–]

## 63 · Kişisel finans ve fatura
- **Actual Budget / Budge / Firefly III / Sure** — kişisel bütçe. [–]
- **Invoice Ninja** — faturalama. [–, muhasebe programı var]
- **Paymenter** — hosting firmaları için faturalama. [–]

## 64 · Ev, aile, sağlık, diğer
- **Baby Buddy** — bebek takibi. [–]
- **Grocy** — ev/mutfak stoku. [–]
- **Homebox** — ev envanteri. [–]
- **Mealie** — tarif/öğün planlama. [ofis]
- **Gramps Web** — soy ağacı. [–]
- **SparkyFitness** — fitness takibi. [–]
- **Reactive Resume** — CV oluşturucu. [–]
- **Firefox** — tarayıcıda uzak tarayıcı. [–]
- **Bitcoin Core** — Bitcoin tam düğüm. [–]
- **Bluesky PDS** — Bluesky kişisel veri sunucusu. [–]

---

## Öncelik özeti (etiketlerden)

**[araç-öncelikli]:** LiteLLM · Langfuse · ntfy · Uptime Kuma (karar gerekir) · Beszel · Metabase · Vaultwarden · Infisical · Tailscale
**[OY-öncelikli]:** Gotenberg · Glitchtip · Mailpit (dev)
**[WS-öncelikli]:** Umami

Bu dosya tanım ve etiket taşır; karar taşımaz. Bir araç kurulmaya karar verildiğinde kararı hafıza taşır.
