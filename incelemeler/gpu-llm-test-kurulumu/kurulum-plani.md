# Kiralık GPU sunucusunda çok modelli LLM testi — kurulum planı

Tarih: 2026-08-25 · Kaynak: OVH resmî sipariş kataloğu API'si, vLLM/Ollama/NVIDIA/Docker resmî dokümanları

Bu doküman OVH'de saatlik GPU kiralayıp üstüne sırayla farklı açık ağırlıklı modeller
kurup karşılaştırmalı test etmenin uygulanabilir yolunu anlatır.

---

## Önce üç bulgu — planın şeklini bunlar belirledi

**1. "vLLM 3 kat hızlı" ölçümü senin senaryonda geçerli değil.**

Elindeki 40 vs 114 tok/sn ölçümü **eşzamanlı istek** altında alınmış bir sayı.
Tek kullanıcı tek istem gönderirken üç yığın da birbirine yakın çalışıyor: RTX 4090
üstünde Llama 3.1 8B için Ollama ~62, llama.cpp ~65, vLLM ~71 tok/sn. Fark
eşzamanlılıkla açılıyor — 8 eşzamanlı istekte vLLM 187, Ollama 82 tok/sn.

Sebebi mimari ve Ollama'nın kendi dokümanında yazılı: `OLLAMA_NUM_PARALLEL`
varsayılanı **1**. Ollama bir isteği işlerken ötekiler kuyrukta bekliyor; vLLM
continuous batching ile hepsini aynı forward pass'e alıyor.

**İş etkisi:** Karşılaştırmalı kalite testi yapacaksan (istemi gönder, cevabı oku,
değerlendir) tek akışta çalışıyorsun demektir ve yığın seçimi hız açısından
neredeyse fark etmez. vLLM'i **yük testi de yapacaksan** ya da modeli gerçekte
nasıl servis edeceğini görmek istiyorsan seç.

**2. 27B model 48 GB'lık L40S'e BF16 olarak sığmaz.**

Aritmetik: parametre × 2 byte = 27B × 2 = **54 GB** — sadece ağırlıklar, KV cache
hariç. Ölçülen gerçek boyut: `google/gemma-3-27b-it` = 54,9 GB.

L40S'te 27B çalıştırmanın yolu **önceden kuantize edilmiş repo çekmek**
(FP8 veya AWQ). Bu opsiyonel bir ayar değil, zorunluluk. `--gpu-memory-utilization`
ile oynamak bunu çözmez; mesele KV cache değil ağırlıkların kendisi.

A100 80 GB'da 27B BF16 sığar (~54 GB ağırlık + ~20 GB KV cache).

**3. OVH'de instance'ı "durdurmak" faturayı durdurmaz — "shelve" durdurur.**

Bu tek başına tüm maliyet planını belirliyor; D bölümünde.

---

## A) Yığın seçimi

### Karar: vLLM, Docker imajıyla

Gerekçe sırayla:

**OpenAI uyumlu API'yi kutudan veriyor.** Test istemcini bir kere yazarsın, modeli
değiştirdiğinde istemci değişmez — `model:` alanı değişir. Karşılaştırmalı test için
bu, yığının en değerli özelliği.

**Kuantizasyonu model config'inden okuyor.** FP8/AWQ bir repo çektiğinde
`--quantization` yazmana gerek yok, vLLM `quantization_config`'i okuyup kendi
ayarlıyor. L40S'te 27B çalıştırmanın önkoşulu buydu.

**Bellek kontrolü açık.** `--max-model-len`, `--kv-cache-dtype fp8`,
`--gpu-memory-utilization` — OOM'la boğuşurken çevireceğin düğmeler belli ve
dokümante.

### Öteki yığınlar — ne zaman doğru

**Ollama** — model değiştirmesi en kolay olan. `ollama pull` / `ollama run` ile
tek komut, kuantizasyon seçimi otomatik (varsayılan Q4_K_M), HuggingFace'ten GGUF'u
doğrudan çekiyor (`ollama run hf.co/kullanici/repo:Q4_K_M`). Boşta kalan modeli
5 dakika sonra VRAM'den kendisi atıyor.

**Bunu hafife alma:** eğer testin "bu modeller ne kadar iyi cevap veriyor"
sorusuysa ve yük testi yapmayacaksan, Ollama seni vLLM'den yarım gün önce
sonuca ulaştırır. Kuantize model bulma derdi yok, OOM ayarı yok, tek komut.
Hız farkı da tek akışta zaten küçük.

Bedeli: her şey GGUF/kuantize — BF16 tam hassasiyette karşılaştırma yapamazsın,
ve eşzamanlılıkta vLLM'in çok gerisinde kalır.

**llama.cpp** — Ollama zaten bunu sarmalıyor. Doğrudan kullanmak GGUF üstünde
ince ayar (katman offload, özel kuantizasyon) gerektiğinde anlamlı. Senin
senaryonda araya girmesi için sebep yok.

**SGLang** — vLLM'e rakip, karmaşık istem yapılarında (paylaşılan önek, yapılandırılmış
üretim) güçlü. Karşılaştırmalı basit test için vLLM'e üstünlüğü yok, ekosistemi daha dar.

**TGI** (HuggingFace) — üretimde makul, ama vLLM'e göre model kapsamı ve topluluk
hareketi daha zayıf. Yeni kurulumda vLLM'i tercih etmek için sebep var, TGI'yi
tercih etmek için yok.

### Model değiştirme kolaylığı — dürüst sıralama

Ollama > vLLM(container restart) > vLLM(sleep mode) > llama.cpp

C bölümünde ayrıntısı var.

---

## B) Sıfırdan kuruluma kadar

### Sunucu seçimi

Resmî OVH kataloğundan çekilmiş gerçek değerler (fiyatlar EUR/saat, KDV hariç,
`ovhSubsidiary=FR`):

| Flavor | GPU | vCore | RAM | Yerel NVMe | Bant | Fiyat |
|---|---|---|---|---|---|---|
| `l40s-90` | 1× L40S 48 GB | 15 | 90 GB | 400 GB | 8 Gbps | **1,40** |
| `a100-180` | 1× A100 80 GB | 15 | 180 GB | 300 GB | 8 Gbps | **2,75** |
| `h100-380` | 1× H100 80 GB | 30 | 380 GB | 200 GB + 3840 GB passthrough | 8 Gbps | **2,80** |

**Dikkat çeken nokta:** H100 80 GB, A100 80 GB'dan yalnız 0,05 EUR/saat pahalı.
Aynı VRAM, belirgin şekilde daha hızlı kart, iki katı vCPU ve RAM. **A100 yerine
H100 almak için 0,05 EUR/saat ödemek** — 8 saatlik bir test turunda 40 kuruş fark.
A100'ü seçmen için tek sebep H100'ün o bölgede stokta olmaması.

Önerim: **testin çoğunu `l40s-90` üstünde yap** (1,40 EUR/saat, kuantize modellerle
27B-32B rahat çalışır). BF16 tam hassasiyet ya da 70B gerekirse `h100-380`'e geç.

### Adım 1 — instance oluştur

Kontrol panelinden ya da OpenStack CLI ile. Image: **Ubuntu 24.04**. OVH GPU
imajlarında NVIDIA sürücüsü **kurulu gelmiyor**, kendin kuracaksın.

GPU bulunan bölgeler: GRA7, GRA9, GRA11, BHS5. Gravelines (GRA11) L40S için doğru yer.

### Adım 2 — güvenlik grubunu daralt (İLK İŞ)

**OVH'nin varsayılan güvenlik grubu her yöne, her protokole tüm bağlantılara izin
verir.** Yani hiçbir şey yapmazsan 8000 portu internete açık olur — üstünde
kimlik doğrulamasız bir LLM API'si ile.

```bash
# Yerelde openstack CLI ile (OVH'den openrc dosyasını indirdikten sonra)
openstack security group create llm-test
openstack security group rule create --proto tcp --dst-port 22 \
  --remote-ip $(curl -s ifconfig.me)/32 llm-test
openstack server add security group <INSTANCE_UUID> llm-test
openstack server remove security group <INSTANCE_UUID> default
```

Yalnız 22 açık — 8000 açılmayacak, E bölümündeki SSH tüneliyle erişilecek.

### Adım 3 — NVIDIA sürücüsü

```bash
sudo apt update && sudo apt upgrade -y
sudo ubuntu-drivers list --gpgpu          # önce listeye bak
sudo ubuntu-drivers install --gpgpu nvidia:580-server
sudo apt install -y nvidia-utils-580-server
sudo reboot
```

Reboot sonrası: `nvidia-smi`

`-server` dalı datacenter kartları (L40S, A100, H100) için test edilen dal.
Listede daha yeni bir `-server` sürümü çıkarsa onu kullan.

**CUDA toolkit kurmuyoruz.** Docker kullanacağız; CUDA runtime kütüphaneleri
container imajının içinde geliyor. Host'tan gereken tek şey kernel sürücüsü.
Toolkit kurmak 3-4 GB boşuna yer ve gereksiz sürüm çakışması riski.

### Adım 4 — Docker + NVIDIA Container Toolkit

```bash
# Docker Engine (resmî repo)
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER && newgrp docker

# NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt update && sudo apt install -y nvidia-container-toolkit

sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Doğrula
docker run --rm --gpus all nvidia/cuda:12.9.1-base-ubuntu24.04 nvidia-smi
```

### Adım 5 — model deposunu hazırla

`l40s-90`'da **400 GB yerel NVMe** var. Kök disk zaten bunun üstünde; ayrıca blok
depolama almadan da 5-6 kuantize model rahat sığar.

> **Bu rakam bir çelişkiyi çözerek doğrulandı.** Katalogda `ephemeralLocalStorage`
> alanı GPU flavor'larında `null` — buna bakıp "GPU instance'larında yerel disk yok"
> sonucuna varmak mümkün, ilk araştırmada öyle de oldu. Ama asıl veri yan alanda:
> `storage.disks` = `[{capacity: 400, technology: "NVMe"}]`. Aynı sorgu
> `a100-180` için 300 GB, `h100-380` için 200 GB + 3840 GB passthrough veriyor.
> Yerel disk var; `ephemeralLocalStorage` başka bir şeyi işaretliyor.

```bash
df -h /                       # gerçekte ne kadar var, bak
mkdir -p ~/hf-cache
export HF_HOME=~/hf-cache     # kalıcı olsun diye ~/.bashrc'ye de yaz
echo 'export HF_HOME=~/hf-cache' >> ~/.bashrc
```

Kalıcı depolama gerekiyorsa (D bölümü) blok volume ekleyip `HF_HOME`'u oraya al.

### Adım 6 — model indir

```bash
pip install -U "huggingface_hub"        # CLI çekirdek pakette, [cli] extra'sı gerekmiyor
export HF_XET_HIGH_PERFORMANCE=1        # hızlı transfer (hf_transfer ARTIK KULLANILMIYOR)

hf auth login --token $HF_TOKEN         # gated modeller için

hf download Qwen/Qwen3-32B-AWQ --dry-run   # ÖNCE boyuta bak
hf download Qwen/Qwen3-32B-AWQ
```

**İki tuzak — ikisi de ölçüldü:**

*`hf_transfer` öldü.* `HF_HUB_ENABLE_HF_TRANSFER` resmî dokümanda deprecated;
Hub Xet arka ucuna geçti. Yenisi `HF_XET_HIGH_PERFORMANCE=1`. Eski rehberlerden
taşınacak ilk yanlış bu.

*Repo boyutu ≠ model boyutu.* Bazı repolar aynı ağırlıkları iki formatta taşıyor:
- `meta-llama/Llama-3.3-70B-Instruct` → safetensors 141 GB ama **repo toplamı 282 GB**
  (`original/` klasöründe ikinci bir tam kopya). `--exclude "original/*"` şart.
- `mistralai/Mistral-Small-24B-Instruct-2501` → **94 GB** (10 shard + ayrıca tek parça
  `consolidated.safetensors`). `--exclude "consolidated*"`.
- GGUF repoları **tüm kuantizasyon seviyelerini** taşır
  (`unsloth/gemma-3-27b-it-GGUF` = 446 GB). Asla tam repo çekme, tek dosya çek.

Bu yüzden her indirmeden önce `--dry-run`.

### Adım 7 — vLLM'i ayağa kaldır

```bash
export HF_TOKEN=hf_xxx
docker run -d --name vllm \
    --runtime nvidia --gpus all \
    -v ~/hf-cache:/root/.cache/huggingface \
    --env "HF_TOKEN=$HF_TOKEN" \
    --env "HF_HOME=/root/.cache/huggingface" \
    -p 127.0.0.1:8000:8000 \
    --ipc=host \
    vllm/vllm-openai:v0.27.1 \
    --model Qwen/Qwen3-32B-AWQ \
    --served-model-name test \
    --max-model-len 8192 \
    --gpu-memory-utilization 0.92
```

Dikkat edilecek noktalar:

- **`-p 127.0.0.1:8000:8000`** — sadece loopback'e bağla. Düz `-p 8000:8000`
  yazarsan Docker iptables kuralı ekler ve portu dışarı açar.
- **`--ipc=host`** — PyTorch süreçler arası tensor paylaşımını `/dev/shm` üzerinden
  yapıyor; Docker varsayılanı 64 MB. Dolduğunda hata "shared memory yetersiz"
  demez, yük altında anlaşılmaz çökmeler olarak çıkar. Alternatifi `--shm-size=16g`.
- **`:v0.27.1`** — `:latest` yazma. İki hafta sonra başka bir şey olur, sorunu
  tekrar üretemezsin.

Test:
```bash
curl http://localhost:8000/v1/models
curl http://localhost:8000/v1/chat/completions -H "Content-Type: application/json" \
  -d '{"model":"test","messages":[{"role":"user","content":"merhaba"}]}'
```

### Bellek ayarı — OOM alırsan sırayla

1. **`--max-model-len`'i düşür.** En büyük kazanç burada. Model 128k context ilan
   ediyor olabilir; testte 8k yetiyorsa `8192` yaz. vLLM aksi hâlde 128k'lık
   senaryoya göre KV cache bütçesi ayırır.
2. **`--kv-cache-dtype fp8`** — KV cache VRAM'ini yarıya indirir, kalite kaybı sınırlı.
3. **`--gpu-memory-utilization 0.95`** — kartta başka süreç yoksa güvenli.
4. **`--max-num-seqs`'i düşür** — eşzamanlılığı feda edip bellek kurtarır.

---

## C) Model değiştirme disiplini

### Önerilen: model başına container, sırayla

```bash
docker rm -f vllm
docker run -d --name vllm ... --model <YENI_MODEL> ...
```

Basit, öngörülebilir, temiz. Maliyeti model yükleme süresi (diskten VRAM'e,
tipik olarak yarım-birkaç dakika). Sıralı test turunda bu maliyet zaten
kaçınılmaz — modeli değiştiriyorsun, ağırlıkların yüklenmesi gerekiyor.

Kolaylaştırmak için:

```bash
#!/usr/bin/env bash
# ~/switch.sh <hf-repo> [max-model-len]
set -euo pipefail
MODEL="$1"; LEN="${2:-8192}"
docker rm -f vllm 2>/dev/null || true
docker run -d --name vllm --runtime nvidia --gpus all \
  -v ~/hf-cache:/root/.cache/huggingface \
  --env "HF_TOKEN=$HF_TOKEN" -p 127.0.0.1:8000:8000 --ipc=host \
  vllm/vllm-openai:v0.27.1 \
  --model "$MODEL" --served-model-name test --max-model-len "$LEN"
echo "yukleniyor: $MODEL"
until curl -sf http://localhost:8000/v1/models >/dev/null 2>&1; do sleep 3; done
echo "hazir"
```

### vLLM sleep mode — ne olduğu ve ne OLMADIĞI

vLLM'de gerçek bir "sleep mode" var:

```bash
# Sunucuyu şu bayraklarla başlat: VLLM_SERVER_DEV_MODE=1 ... --enable-sleep-mode
curl -X POST 'http://localhost:8000/sleep?level=1'   # ağırlıkları CPU RAM'e, KV cache'i at
curl -X POST 'http://localhost:8000/wake_up'
curl -X GET  'http://localhost:8000/is_sleeping'
```

**Ama bu, aynı sunucuda başka bir modele geçmek DEĞİL.** Bir vLLM süreci tek bir
modele bağlıdır; sleep o modelin belleğini boşaltır, `wake_up` **aynı** modeli
geri getirir. Farklı model = farklı süreç.

Sleep mode'un işe yaradığı desen: **her model için ayrı container aç, farklı
portlarda çalıştır, kullanılmayanları uyut.** Böylece modeller arası geçiş
saniyeler sürer (ağırlıklar CPU RAM'de bekliyor) — ama bunun için tüm modellerin
ağırlıklarını tutacak kadar **sistem RAM'in** olması gerekir. `l40s-90`'da 90 GB
RAM var; iki-üç kuantize model sığar, altı model sığmaz.

Ayrıca `VLLM_SERVER_DEV_MODE=1` yönetim endpoint'lerini açıyor ve
`/collective_rpc` keyfi metot çağırabiliyor — **bunu internete açık bırakmak
sunucuyu teslim etmektir.** SSH tüneli arkasında kalmalı.

**Karar:** sıralı karşılaştırma testinde container restart yeterli. Sleep mode'u
ancak iki model arasında sık sık ileri geri gidip geleceksen kur.

### Ollama tarafı — model yönetimi gerçekten daha kolay

```bash
ollama pull qwen3:32b
ollama run hf.co/bartowski/gemma-3-27b-it-GGUF:Q4_K_M   # HF'den doğrudan GGUF
ollama ls              # ne var
ollama ps              # şu an bellekte ne var
ollama stop <model>    # VRAM'den hemen boşalt
ollama rm <model>      # diskten sil
```

**Otomatik VRAM boşaltma var:** varsayılan 5 dakika boşta kalınca model bellekten
atılır. `OLLAMA_KEEP_ALIVE` ile değiştirilir (`"10m"`, `-1` süresiz, `0` hemen boşalt).
API'de `keep_alive` parametresi bunu ezer:

```bash
curl http://localhost:11434/api/generate -d '{"model":"qwen3:32b","keep_alive":0}'
```

Linux'ta model deposu `/usr/share/ollama/.ollama/models` (blobs/ + manifests/,
içerik-adresli — aynı blob'u paylaşan modeller diskte tek kopya). Taşımak için
`OLLAMA_MODELS`, ve `ollama` kullanıcısına yazma izni gerekiyor.

Eşzamanlılık: `OLLAMA_NUM_PARALLEL` varsayılan **1** (yığın karşılaştırmasındaki
farkın kaynağı), `OLLAMA_MAX_LOADED_MODELS` varsayılan GPU sayısı × 3 — ama birden
fazla modelin aynı anda bellekte durması için hepsinin VRAM'e **tamamen** sığması
gerekiyor. 48 GB'lık tek kartta 5-6 model diskte durur, sırayla yüklenir.

---

## D) Maliyet kontrolü — en kritik bölüm

### Temel kural: "durdurmak" fatura durdurmaz

OVH dokümanı üç durumu ayırıyor:

| Durum | Ne olur | Fatura |
|---|---|---|
| **Pause** | VM state RAM'de, instance donuk | **Tam ücret** |
| **Stop / Suspend (kapatma)** | VM state diskte, kaynaklar rezerve | **Tam ücret** |
| **Shelve** (panelde "Suspend"/Askıya al) | Disk snapshot'a alınır, kaynaklar bırakılır | **Yalnız snapshot** |

Yani makineyi kapatıp bırakmak seni kurtarmaz — saatlik ücret işlemeye devam eder.
Faturayı durduran tek yol **shelve** ya da **instance'ı tamamen silmek**.

### Shelve nasıl çalışır

```bash
openstack server shelve <UUID>      # askıya al
openstack server unshelve <UUID>    # geri getir
```
Panelden: Public Cloud > Instances > ⋮ > **Suspend** / **Reactivate**

- Yerel diskteki veri otomatik oluşturulan bir **snapshot'a** alınır
- **IP adresi korunur**
- Unshelve edince kaynaklar ve veri geri gelir, snapshot otomatik silinir
- RAM'deki her şey kaybolur (çalışan container'lar durur — normal)

**Uyarı:** Doküman "IOPS veya T1/T2-180 instance askıya alınırsa NVMe passthrough
disklerdeki veri kaybolur" diyor. Bu uyarı GPU flavor'larını adıyla saymıyor, ama
`h100-380`'de bir **NVMe Passthrough** diski var (3840 GB) — H100 kullanıp shelve
edeceksen modelleri o diske koyma, ya da önce sına.

### Maliyet karşılaştırması — gerçek fiyatlarla

Resmî katalogdan çekilmiş, EUR, KDV hariç:

- `l40s-90` instance: **1,40 EUR/saat**
- Snapshot: **0,011 EUR/GB/ay** (saatlik 0,000015 EUR/GB)
- Block storage **Classic**: **0,042 EUR/GB/ay**
- Block storage **High Speed** ve **High Speed Gen2**: **0,086 EUR/GB/ay**

**Senaryo: 300 GB model deposu, ayda 20 saat aktif test**

*Yol 1 — instance açık kalsın (yanlış):*
720 saat × 1,40 = **1 008 EUR/ay**. Konuşulmaz.

*Yol 2 — her seferinde sıfırdan kur, modelleri yeniden indir:*
20 saat × 1,40 = 28 EUR. Depolama 0.
Bedeli: her turda kurulum + indirme. 8 Gbps'te indirme hızlı (aşağıda), ama
sürücü/Docker kurulumu her seferinde ~15-20 dakika — ve bu süre de faturalanıyor.

*Yol 3 — shelve (önerilen):*
20 saat × 1,40 = 28 EUR
+ 300 GB snapshot × 0,011 = 3,30 EUR/ay
= **~31 EUR/ay**

*Yol 4 — kalıcı block storage volume:*
20 saat × 1,40 = 28 EUR
+ 300 GB Classic × 0,042 = 12,60 EUR/ay
= **~41 EUR/ay** (High Speed olsaydı +25,80 = 54 EUR)

### Karar: shelve

Snapshot (0,011/GB/ay) block storage'ın (0,042) **dörtte biri** fiyatında ve tam
olarak istediğin şeyi yapıyor — makineyi olduğu gibi dondurup faturayı kesiyor,
geri açtığında her şey yerinde: kurduğun sürücü, Docker, indirdiğin modeller.

Block storage volume'u şu durumda tercih et: aynı model deposunu **birden çok
instance arasında** dolaştıracaksan (L40S'te dene, sonra aynı diski H100'e tak),
ya da instance'ı tamamen silip yeniden yaratma alışkanlığın varsa. Volume
instance'tan bağımsız yaşar, snapshot yaşamaz.

### İndirme süresi — darboğaz değil

`l40s-90` bant genişliği katalogda **8 000 Mbps = 8 Gbps** (tek GPU'lu tüm
flavor'lar 8 Gbps; "up to 25 Gbps" ifadesi 4 GPU'lu en üst flavor için).

Formül: `süre = GB × 8 ÷ Gbps`. Gerçekçi olması için ~%70 verimle:

| Model | 8 Gbps (ideal) | %70 verimle |
|---|---|---|
| 17 GB (27B kuantize) | 17 sn | ~24 sn |
| 65 GB (32B bf16) | 1,1 dk | ~1,5 dk |
| 141 GB (70B bf16) | 2,3 dk | ~3,3 dk |

**İş etkisi:** 8 Gbps'te yeniden indirme birkaç dakika. Yani "modelleri saklamak"
uğruna aylık 12 EUR block storage ödemek bile tartışmalı — shelve'in 3,30 EUR'su
zaten ucuz, ama en uçta modelleri hiç saklamayıp her turda indirmek de savunulabilir
bir seçenek. Asıl saklamak istediğin şey model dosyaları değil, **kurulmuş sistem**
(sürücü + Docker + toolkit) — onu yeniden kurmak 15-20 dakika ve bu süre faturalanıyor.

### Kaçınılması gereken

- Test bitince **shelve etmeyi unutma.** Bir gece unutmak 33,60 EUR.
- `:latest` imaj etiketi kullanma — tekrar üretilemezlik zaman kaybettirir, zaman fatura.
- Modelleri indirirken `--dry-run` atlamak — Llama-70B'de 141 GB fazla indirmek
  hem süre hem disk.

---

## E) Uzaktan erişim

### Karar: SSH tüneli. API'yi internete hiç açma.

Zaten B/Adım 2'de güvenlik grubunu 22'ye kısıtladık ve container'ı
`-p 127.0.0.1:8000:8000` ile loopback'e bağladık. Kalan iş tünel:

```bash
# Yerelden
ssh -N -L 8000:127.0.0.1:8000 ubuntu@<SUNUCU_IP>
```

Sonra yerelde `http://localhost:8000/v1/...` — sanki makinede çalışıyormuş gibi.

Dayanıklı sürüm (kopan bağlantıyı toparlar):
```bash
ssh -N -L 8000:127.0.0.1:8000 \
    -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
    -o ExitOnForwardFailure=yes \
    ubuntu@<SUNUCU_IP>
```

`~/.ssh/config`'e yazarsan tek komuta iner:
```
Host llmbox
    HostName <SUNUCU_IP>
    User ubuntu
    LocalForward 8000 127.0.0.1:8000
    ServerAliveInterval 30
    ExitOnForwardFailure yes
```
→ `ssh -N llmbox`

### Neden port açıp `--api-key` koymak yeterli değil

vLLM dokümanı bunu kendisi söylüyor: `--api-key` yalnızca `/v1`, `/v2`,
`/inference` önekli endpoint'leri korur; `/invocations` dahil diğerleri
**kimlik doğrulamasız kalır**. Doküman birebir *"Do not rely on `--api-key`
alone to secure vLLM"* diyor.

Buna ek olarak sleep mode kullanacaksan `VLLM_SERVER_DEV_MODE=1` gerekiyor ve
`/collective_rpc` keyfi metot çağırabiliyor.

Üçü birleşince: **8000 portu internete açılmaz.** Tünel maliyeti sıfır, riski sıfır.

Yine de savunma katmanı olarak `--api-key` ver — tünelin içindeyken bile
yanlışlıkla açılan bir portu bir ölçüde korur.

---

## Özet — uygulama sırası

1. `l40s-90` instance aç (Ubuntu 24.04, GRA11) — 1,40 EUR/saat
2. Güvenlik grubunu 22'ye kısıtla, `default`'u kaldır
3. NVIDIA sürücüsü (`ubuntu-drivers install --gpgpu nvidia:580-server`) + reboot
4. Docker + nvidia-container-toolkit + `nvidia-ctk runtime configure`
5. `export HF_HOME=~/hf-cache`, `HF_XET_HIGH_PERFORMANCE=1`
6. Model indir (`--dry-run` ile boyutu gör, `--exclude` ile çift kopyayı ele)
7. vLLM container'ı `-p 127.0.0.1:8000:8000` ile başlat
8. Yerelden `ssh -N llmbox`, `http://localhost:8000` üstünden test et
9. Model değiştir: `~/switch.sh <repo>`
10. **Test bitince `openstack server shelve <UUID>`**

Model seçiminde not: L40S'te 27B+ için **FP8 veya AWQ** repo çek
(`Qwen/Qwen3-32B-AWQ`, `Qwen/Qwen3-32B-FP8` gibi resmî kuantize sürümler var).
BF16 karşılaştırması şartsa `h100-380` (2,80 EUR/saat) — A100'le arasında
0,05 EUR/saat fark var, A100'ü seçmenin sebebi kalmıyor.

---

## Lisans ve erişim durumu (HF API'sinden sorgulandı)

**Token + lisans onayı gerekiyor (gated):**
`meta-llama/*` (Llama 3.1/3.3/4), `google/gemma-*`

**Serbest, token gerekmiyor:**
`Qwen/*` (apache-2.0), `deepseek-ai/DeepSeek-R1` (mit),
`mistralai/*` (apache-2.0), `NousResearch/Hermes-3-*` (llama3 lisansı ama repo açık)

Otomatik provizyon betiği yazacaksan Meta ve Google modellerinde takılır — o ikisi
için web'de lisansı elle kabul etmek gerekiyor. Qwen/DeepSeek/Mistral tam otomatik akar.

Not: NousResearch, Llama türevlerini gated olmayan repolarda yayınlıyor — HF kapısı
yok ama **Llama lisansı yine geçerli** (atıf yükümlülüğü, 700M MAU eşiği).

**DeepSeek-V3/R1 kapsam dışı bırakılmalı:** 671B MoE, repo 688 GB, tek GPU'da çalışmaz.

---

## Kaynaklar

- OVH sipariş kataloğu API'si (fiyat ve donanım verisi):
  `https://api.ovh.com/v1/order/catalog/public/cloud?ovhSubsidiary=FR`
- [OVH — Shelve or pause an instance](https://docs.ovhcloud.com/en/guides/public-cloud/compute/suspend-or-pause-an-instance)
- [OVH — Deploying a GPU instance](https://docs.ovhcloud.com/en/guides/public-cloud/compute/deploy-a-gpu-instance)
- [OVH — Firewall ve port güvenliği (OpenStack CLI)](https://help.ovhcloud.com/csm/en-public-cloud-compute-firewall-security?id=kb_article_view&sysparm_article=KB0051166)
- [vLLM — Using Docker](https://docs.vllm.ai/en/stable/deployment/docker/)
- [vLLM — Engine Arguments](https://docs.vllm.ai/en/stable/configuration/engine_args.html)
- [vLLM — Sleep Mode](https://docs.vllm.ai/en/latest/features/sleep_mode/)
- [vLLM — Zero-Reload Model Switching (blog)](https://blog.vllm.ai/2025/10/26/sleep-mode.html)
- [NVIDIA Container Toolkit — Install Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- [Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Ubuntu Server — NVIDIA drivers](https://ubuntu.com/server/docs/how-to/graphics/install-nvidia-drivers/)
- [HuggingFace — CLI rehberi](https://huggingface.co/docs/huggingface_hub/guides/cli)
- [HuggingFace — Ortam değişkenleri](https://huggingface.co/docs/huggingface_hub/package_reference/environment_variables)
- [Ollama — FAQ](https://github.com/ollama/ollama/blob/main/docs/faq.mdx)
- [Ollama — CLI](https://github.com/ollama/ollama/blob/main/docs/cli.mdx)
- [HuggingFace — Ollama entegrasyonu](https://huggingface.co/docs/hub/ollama)

## Doğrulanamayanlar

- `vllm/vllm-openai:v0.27.1` imajının kesin boyutu — yalnız nightly ölçüldü (~8-10 GB sıkıştırılmış)
- `--max-num-seqs` varsayılan değeri
- GPU flavor'larında shelve'in yerel NVMe verisini koruyup korumadığı — doküman
  uyarısı yalnız IOPS/T1/T2-180'i adıyla anıyor. `h100-380`'de passthrough disk var,
  ilk shelve'den önce sınanmalı.
- DeepSeek-V3 lisansı (model kartı metadata'sında boş; R1 mit)
