# Konu 0 — Dersin Tanıtımı ve Kurulum

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Dönemin haritası

Bu ders GİTA2112'nin devamı. Orada kodun temelini attık; burada yapay zekayı
**kendi kodumuzdan** kullanacağız.

- **Önce:** bu şeyler nasıl çalışıyor — veri, web servisleri, temsil, dil modelleri, üretken modeller
- **Ortada:** vize
- **Sonra:** onlarla ne üretiyoruz — görsel, video, üretim hatları
- **Sonda:** kendi üretim aracını kurduğun final projesi

Dersi haftalara değil **konulara** böldük. Bir konu bir dersten kısa da sürebilir,
uzun da. Her konunun sonunda elinde çalışan bir çıktı olacak; hiçbir derste sadece
dinlemeyeceğiz.

-----

## Nasıl değerlendirileceksin?

- **Vize %40** — take-home, evde yapılır, **yapay zeka yasak**, derste sözlü teyit var
- **Final projesi %60** — kendi kurduğun üretim aracı + üretim günlüğü + sunum
- **Konu ödevleri: puansız**

Ödevler puansız ama sıra listesi var: herkes dönem boyunca 2-3 kez sınıfta
çıktısını gösterecek.

Çalışmayan kodla gelmek sorun değil. Hiç denememiş gelmek sorun.

-----

## Yapay zeka ile kod yazmak (vibecoding)

Geçen dönem Antigravity ile araç ürettiniz. Bu derste de kullanacağız — ama nerede
serbest, nerede yasak, baştan net olsun:

- **Vizede yasak.** Ölçtüğümüz şey senin kendi programlama becerin.
- **Üretim konularında (dönemin ikinci yarısı) serbest ve bekleniyor.** Orada
  ölçtüğümüz şey aracı yönetme becerisi.
- **Kavram konularında serbest** — ama unutma: vizede tek başına yazacaksın.
  Aracın yazdığını anlamadan geçmek kendi ayağına sıkmaktır.

Kullandığın her yerde üretim günlüğüne yazacaksın.

**Güvenlik kuralı:** yapay zeka aracının terminal komutlarını **onaysız çalıştırmasını
kapat.** Her komutu okuyup sen onayla. Araç `anahtar.txt` dosyanı okuyup bir yere
gönderebilir; bunu durduran şey senin onayın.

-----

## Bu dersten sonra: kurulum

Gelecek dersten itibaren (Konu 01) her derste kod çalıştıracağız. Bunun için
bilgisayarında birkaç araç kurulu olmalı.

- Şimdi adımları **birlikte göreceğiz**; kurulumu **bu dersten sonra evde** yapacaksın
- Evde bu slaytlara değil, **yazılı yönergeye** bakarak ilerle: `00-hazirlik/kurulum-yonergesi.md`
- Toplam süre yaklaşık **30–45 dakika**
- Gelecek dersin başında herkesin kurulumunun çalıştığını **birlikte kontrol edeceğiz**

Takıldığın yerde dur, ekran görüntüsü al ve bana yaz. Yarım kalmış kurulumla derse
gelmek sorun değil; **hiç denememiş olarak gelmek sorun.**

-----

## Ne kuracağız?

| Ne | Ne işe yarıyor |
|---|---|
| **uv** | Python'ı ve kütüphaneleri senin yerine kuran araç |
| **git** | Ders deposunu indiren ve her yeni konuda güncelleyen araç |
| **gita3111 klasörü** | Ders deposunun bilgisayarındaki kopyası |
| **VS Code** | Kod yazacağın editör (geçen dönemden duruyorsa dokunma) |
| **Cloudflare hesabı** | Konu 02'den itibaren kodla yapay zekaya bağlanmak için. **Ücretsiz.** |

Python'ı ayrıca kurmana gerek yok; uv onu da hallediyor.

-----

## Önce terminal: üç komut yeter

Bütün kurulum terminalde yapılıyor. Korkutucu görünür ama bu dönem neredeyse hep aynı
üç şeyi yapacağız:

```text
cd klasor_adi      bir klasörün içine gir
cd ..              bir üst klasöre çık
pwd                neredeyim? (PowerShell'de de aynı)
```

- **Terminali açmak:** Windows'ta Başlat → `PowerShell`; macOS'ta Cmd+Boşluk → `Terminal`
- Komutu yaz ya da yapıştır, **Enter**'a bas
- Terminal her zaman **bir klasörün içinde** durur. Komutlar o klasöre göre çalışır.

Bu dönemin en sık hatası "yanlış klasördeyim" olacak. `pwd` senin pusulan.

-----

## Adım 1 — uv kurulumu

**Windows** (PowerShell):

```text
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS** (Terminal):

```text
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Sonra **terminali kapat ve yeniden aç**, ve kontrol et:

```text
uv --version
```

Bir sürüm numarası görüyorsan tamam. "tanınmıyor" ya da "command not found" diyorsa
terminali gerçekten kapatıp açmamışsındır.

-----

## Adım 2 — git kurulumu

Önce kurulu mu diye bak: `git --version`. Sürüm numarası çıkarsa bu adımı atla.

**Windows:**

```text
winget install --id Git.Git -e
```

`winget` tanınmıyorsa git-scm.com/download/win adresinden indir; kurulum ekranlarında
hiçbir şeyi değiştirmeden **Next** de.

**macOS:** `git --version` yazınca "geliştirici araçlarını yüklemek ister misin?" diye
bir pencere açılır. **Yükle** de.

İkisinde de iş bitince **terminali kapat, yeniden aç.**

-----

## git ne işe yarıyor?

Ders materyali bir **depoda** duruyor: github.com/aladagemre/gita3111

- Dönem başında depoda yalnızca ilk konular var
- Yeni konular geldikçe depoya ekliyorum
- Sen her seferinde klasörü baştan indirmiyorsun; **git yalnızca yeni ve değişen dosyaları** getiriyor

İki komut bilmen yeterli:

| Komut | Ne zaman | Ne yapar |
|---|---|---|
| `git clone ...` | Dönemde **bir kez** | Depoyu bilgisayarına indirir |
| `git pull` | **Her dersten önce** | Yeni konuları indirir |

-----

## Adım 3 — Depoyu indir

Masaüstüne geç ve depoyu indir:

```text
cd Desktop
git clone https://github.com/aladagemre/gita3111.git
```

Masaüstünde artık `gita3111` adında bir klasör var.

**Klasör yolu uyarısı:**
- Yolda **Türkçe karakter** (ç, ğ, ı, ö, ş, ü) ve **boşluk** olmasın
- "Ders Notları/Yapay Zekâ" gibi bir yol ileride saatlerini yer
- OneDrive'lı Windows'larda Masaüstü yolu uzun olabilir; sorun çıkarsa `C:\gita3111` gibi kısa bir yer seç

-----

## Deponun içi

```text
gita3111/
├── pyproject.toml              ← dersin kütüphane listesi
├── anahtar.txt                 ← sen oluşturacaksın (Adım 6)
├── 00-hazirlik/                ← bu konu
│   ├── kurulum-yonergesi.md
│   ├── ilk_defter.ipynb
│   └── ornekler/kurulum_testi.py
├── 01-veri-ve-kelime-bulutu/
│   ├── ders.ipynb              ← derste birlikte çalıştıracağımız defter
│   ├── alistirma.ipynb         ← kendi başına çözeceğin alıştırmalar
│   ├── ders_notu.md            ← evde okuyacağın konu notu
│   ├── slaytlar.md
│   └── veri/   odevler/
├── 02-api-ile-konusmak/
└── ...
```

- Her konu **kendi klasöründe**, başında sıra numarası var
- Konuların başında hafta değil **sıra** numarası var: bir konu bir dersten kısa da sürebilir, uzun da
- Her konu klasöründe aynı düzen: ders defteri, alıştırma defteri, not, slayt, veri, ödev

-----

## Depo tek bir uv projesi

`gita3111` klasöründe bir `pyproject.toml` dosyası var:

```toml
[project]
name = "gita3111"
version = "0.1.0"
requires-python = ">=3.13,<3.15"
dependencies = [
    "matplotlib>=3.10",
    "requests>=2.32",
    "scikit-learn>=1.6",
    "wordcloud>=1.9",
]
```

- Bu dosya dersin **hangi Python'u** ve **hangi kütüphaneleri** kullandığını yazar
- `gita3111` klasöründe `uv sync` dersen uv bu dosyayı okur, eksik ne varsa **kendisi kurar**
  ve `gita3111` klasöründe `.venv` adlı tek bir ortam oluşturur
- Defteri açınca VS Code'a "bu ortamı kullan" diyeceğiz (Adım 5)
- Sen hiçbir zaman "şu kütüphaneyi kur" diye uğraşmazsın

Tek şart: komutu **`gita3111` klasörünün ya da bir konu klasörünün içinden** çalıştırmak.
uv bu dosyayı bulunduğun klasörde ve onun üstündeki klasörlerde arar.

-----

## Adım 4 — Kurulumu test et

```text
cd gita3111/00-hazirlik
uv run ornekler/kurulum_testi.py
```

İlk çalıştırmada uv doğru Python sürümünü ve kütüphaneleri indirir; birkaç dakika
sürebilir. Ekranda şunu görmelisin:

```text
[OK  ] Doğru klasördesin — şu an: .../Desktop/gita3111/00-hazirlik
[OK  ] Python sürümü — bulunan: 3.13
[OK  ] matplotlib kurulu
[OK  ] wordcloud kurulu
[OK  ] ipykernel kurulu
[OK  ] Grafik üretimi — kurulum_testi_ciktisi.png oluştu
[ATLA] Cloudflare bağlantısı — anahtar.txt yok (Konu 02'ye, API dersine kadar sorun değil)
----------------------------------------
KURULUM TAMAM
```

**KURULUM TAMAM** görmüyorsan betik neyin eksik olduğunu zaten yazıyor. Çıktının ekran
görüntüsünü al, derse onunla gel.

-----

## Yanlış klasörden çalıştırırsan

`gita3111` klasöründe durup testi çalıştırmayı denersen:

```text
[EKSİK] Doğru klasördesin — şu an: .../Desktop/gita3111
      -> Önce `cd gita3111/00-hazirlik` yaz, sonra `uv run ornekler/kurulum_testi.py`.
```

Bu dönem göreceğin hataların çoğu bu türden olacak:

- **"No such file or directory"** → büyük ihtimalle yanlış klasördesin
- **"No module named ..."** → büyük ihtimalle yine yanlış klasördesin; uv `pyproject.toml` dosyasını bulamadı
- Önce `pwd` yaz, nerede olduğuna bak

Hatanın sebebi çoğu zaman kodda değil, **nerede durduğunda.**

-----

## Önemli kural: depo dosyasını değiştirmeden önce kopyala

Dönem boyunca kuralımız bu:

- Depodaki bir dosyayı değiştireceksen önce **aynı klasörde yeni bir adla kopyala**
- Örnek: `ilk_defter.ipynb` → `benim_defterim.ipynb`, `alistirma.ipynb` → `benim_alistirmam.ipynb`
- Sonra kopyada çalış

**Neden?** `git pull` senin adını verdiğin dosyalara hiç dokunmaz. Ama depodaki bir
dosyayı değiştirdiysen ve ben de o dosyayı güncellediysem, `git pull` durur.

-----

## git pull takılırsa

Şu hatayı görürsen:

```text
error: Your local changes to the following files would be overwritten by merge
```

bir depo dosyasını değiştirmişsin demektir. Çözüm üç adım:

1. Değiştirdiğin dosyayı **yeni bir adla kopyala** (emeğin kaybolmasın)
2. Depo dosyalarını ilk hâline döndür:

```text
git restore .
```

3. Tekrar dene:

```text
git pull
```

Senin oluşturduğun dosyalar (kopyalar, üretilen görseller, `anahtar.txt`) bu işlemden
etkilenmez.

-----

## Adım 5 — VS Code ve defterler

Bu dönem kodu **defterlerde** (notebook, `.ipynb`) çalıştıracağız: kod küçük kutulara
(**hücre**) bölünmüş; her hücreyi ayrı çalıştırıp sonucunu hemen altında görürsün.

- VS Code yoksa: code.visualstudio.com → indir → kur
- VS Code'da sol menüden **Extensions** → **Python** ve **Jupyter** eklentilerini kur (ikisi de Microsoft'un)
- **File → Open Folder** ile `gita3111` klasörünü aç

VS Code'un içinde terminal de var: **Terminal → New Terminal**.

-----

## İlk defterin

Önce terminalde ortamı hazırla:

```text
cd gita3111
uv sync
```

Sonra VS Code'da **File → Open Folder** ile `gita3111` klasörünü aç, `00-hazirlik/ilk_defter.ipynb` dosyasını aç:

- Sağ üstte **Select Kernel** → **Python Environments** → `.venv` seç
- Bir hücreye tıkla, **Shift + Enter**: hücre çalışır, sonucu altında görünür
- Grafik hücresindeki iki listeyi kendi verinle değiştir ve yeniden çalıştır:

```python
import matplotlib.pyplot as plt

gunler = ["Pzt", "Sal", "Çar", "Per", "Cum"]
saatler = [3, 7, 2, 8, 5]

plt.bar(gunler, saatler)
plt.title("Bu hafta kaç saat çizim yaptım?")
plt.show()
```

Değiştirmeden önce defteri kopyala: `benim_defterim.ipynb`.

-----

## Adım 6 — Cloudflare hesabı

Konu 02'de kodumuzdan yapay zeka modellerine bağlanacağız. Hesabı **şimdi** açıyoruz
ki sorun çıkarsa çözmeye zamanımız olsun.

1. dash.cloudflare.com/sign-up/workers-and-pages adresinde ücretsiz hesap aç
2. E-postana gelen doğrulama bağlantısına tıkla
3. dash.cloudflare.com/?to=/:account/ai/workers-ai adresine git
4. **Use REST API** bölümünü aç:
   - **Account ID**'yi kopyala
   - **Create a Workers AI API Token** → hazır bilgileri değiştirmeden **Create API Token** → **Copy**

**Kredi kartı isterse dur ve bana yaz.** Bu dersin tamamı ücretsiz kullanımla
tasarlandı; kart bilgisi girme.

-----

## Anahtarı nereye kaydedeceksin?

`gita3111` klasörünün içinde, konu klasörlerinin **yanında**, `anahtar.txt` adlı tek
bir dosya:

```text
ACCOUNT_ID = buraya_account_id
API_TOKEN = buraya_anahtar
```

- Bütün konuların kodu anahtarı **buradan** okur
- Bu dosya depoya hiçbir zaman gönderilmez; `git pull` da ona dokunmaz

**Üç kural:**
- Anahtarı **kimseyle paylaşma**, arkadaşına da gönderme
- Anahtarı **ödev teslimine koyma**
- Anahtar ekranı **bir kez** görünür; kapatırsan yenisini üretirsin (sorun değil)

Anahtarı kaydettikten sonra kurulum testini bir kez daha çalıştır: Cloudflare satırı da
**OK** olmalı.

-----

## Sık karşılaşılan sorunlar

| Belirti | Sebep | Çözüm |
|---|---|---|
| `uv` / `git` tanınmıyor | Kurulumdan sonra terminal yenilenmedi | Terminali kapat, yeniden aç |
| İnternet hatası (`uv sync`, `git clone`) | Üniversite ağı bazı adresleri kapatıyor | Telefon internetini paylaşıp tekrar dene |
| "No such file or directory" | Yanlış klasördesin | `pwd` ile bak, `cd gita3111/00-hazirlik` |
| "Repository not found" | Depo adresi yanlış yazıldı | Adresi kopyala-yapıştır yap |
| Defterde **Select Kernel** listesinde `.venv` yok | `uv sync` çalıştırılmadı ya da VS Code'da alt klasör açıldı | `gita3111` klasöründe `uv sync`; VS Code'da `gita3111` klasörünü aç, listeyi yenile |
| Cloudflare satırı HTTP 401 | Token yanlış kopyalandı | Yeni token üret, `anahtar.txt`'ye yapıştır |
| Cloudflare satırı HTTP 403 | Token'ın izinleri eksik | Token'ı hazır bilgileri değiştirmeden yeniden üret |

Listede olmayan bir şey görürsen: ekran görüntüsü, bana mesaj.

-----

## Gelecek dersten önce kontrol listesi

- [ ] `uv --version` ve `git --version` birer sürüm numarası yazıyor
- [ ] `git clone` ile indirdiğim `gita3111` klasörüm var
- [ ] `00-hazirlik` içinde `uv run ornekler/kurulum_testi.py` → **KURULUM TAMAM**
- [ ] VS Code'da `ilk_defter.ipynb` defterini açıp `.venv` çekirdeğiyle çalıştırdım, kendi verimle grafik çizdim
- [ ] Cloudflare hesabım var; Account ID ve anahtarım `gita3111/anahtar.txt` dosyasında

Altısı da tamamsa hazırsın. Gelecek dersin başında kurulum testini birlikte bir kez
daha çalıştıracağız; herkesin ekranında **KURULUM TAMAM** görmeden kelime bulutuna
geçmeyeceğiz.

-----

## Her dersten önce: üç adım

```text
cd gita3111
git pull
uv sync
```

- `git pull` → yeni konuyu getirir
- `uv sync` → yeni konunun kütüphaneleri varsa onları kurar
- VS Code'da konunun `ders.ipynb` defterini aç, çekirdek olarak `.venv`'i seç

Bu dönemin ritmi bu: **çek, kur, aç.**
