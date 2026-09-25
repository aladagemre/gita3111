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
├── anahtar.txt                 ← sen oluşturacaksın (Adım 6)
├── 00-hazirlik/                ← bu konu
│   ├── pyproject.toml
│   ├── kurulum-yonergesi.md
│   └── ornekler/
├── 01-veri-ve-kelime-bulutu/
│   ├── pyproject.toml
│   ├── ders_notu.md
│   ├── slaytlar.md
│   ├── ornekler/   veri/   alistirma/   odevler/
├── 02-api-ile-konusmak/
└── ...
```

- Her konu **kendi klasöründe**, başında sıra numarası var
- Konuların başında hafta değil **sıra** numarası var: bir konu bir dersten kısa da sürebilir, uzun da
- Her konu klasöründe aynı düzen: not, slayt, örnekler, veri, alıştırma, ödev

-----

## Her konu kendi başına bir uv projesi

Her konu klasöründe bir `pyproject.toml` dosyası var:

```toml
[project]
name = "gita3111-01-veri-ve-kelime-bulutu"
version = "0.1.0"
requires-python = ">=3.13,<3.15"
dependencies = [
    "matplotlib>=3.10",
    "wordcloud>=1.9",
]
```

- Bu dosya o konunun **hangi Python'u** ve **hangi kütüphaneleri** kullandığını yazar
- `uv run` bu dosyayı okur, eksik ne varsa **kendisi kurar**
- Sen hiçbir zaman "şu kütüphaneyi kur" diye uğraşmazsın

Tek şart: komutu **konunun klasörünün içinden** çalıştırmak. uv bu dosyayı komutu
çalıştırdığın klasörde arar.

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
- **"No module named ..."** → büyük ihtimalle yine yanlış klasördesin; uv o konunun `pyproject.toml` dosyasını bulamadı
- Önce `pwd` yaz, nerede olduğuna bak

Hatanın sebebi çoğu zaman kodda değil, **nerede durduğunda.**

-----

## Kurulumdan sonra: ilk grafiğin

`00-hazirlik/ornekler/` klasöründe hazır bir grafik betiği var. Kod yazmanı
beklemiyorum; yalnızca **veriyi değiştireceksin**. Önce dosyayı kopyala
(`grafik.py` → `benim_grafigim.py`), sonra kopyada şu kısmı değiştir:

```python
#---- DEĞİŞTİRECEĞİN YER ----
etiketler = ["Pzt", "Sal", "Çar", "Per", "Cum"]
degerler = [3, 7, 2, 8, 5]
baslik = "Haftalık bir şey"
#----------------------------
```

- Kendinden bir veri koy: bir haftada kaç saat çizim yaptığın, en sevdiğin beş rengi kaç kez kullandığın…
- Çalıştır: `uv run ornekler/benim_grafigim.py`
- `00-hazirlik` klasöründe `grafik.png` oluşur

Grafik kodunun **nasıl yazıldığını** Konu 01'de öğreneceğiz.

-----

## Önemli kural: depo dosyasını değiştirmeden önce kopyala

Grafik betiğini neden önce kopyaladık? Dönem boyunca kuralımız bu:

- Depodaki bir dosyayı değiştireceksen önce **aynı klasörde yeni bir adla kopyala**
- Örnek: `grafik.py` → `benim_grafigim.py`, `sinif_alistirmasi.py` → `benim_alistirmam.py`
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

## Adım 5 — VS Code

- Geçen dönemden kuruluysa **dokunma**
- Değilse: code.visualstudio.com → indir → kur
- **File → Open Folder** ile `gita3111` klasörünü aç

VS Code'un içinde de terminal var: **Terminal → New Terminal**. Açılan terminal
`gita3111` klasöründe başlar; konuya geçmek için `cd 00-hazirlik` yaz.

Dönem boyunca kodu VS Code'da yazacak, VS Code'un terminalinde çalıştıracağız.

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
| İnternet hatası (`uv run`, `git clone`) | Üniversite ağı bazı adresleri kapatıyor | Telefon internetini paylaşıp tekrar dene |
| "No such file or directory" | Yanlış klasördesin | `pwd` ile bak, `cd gita3111/00-hazirlik` |
| "Repository not found" | Depo adresi yanlış yazıldı | Adresi kopyala-yapıştır yap |
| Cloudflare satırı HTTP 401 | Token yanlış kopyalandı | Yeni token üret, `anahtar.txt`'ye yapıştır |
| Cloudflare satırı HTTP 403 | Token'ın izinleri eksik | Token'ı hazır bilgileri değiştirmeden yeniden üret |

Listede olmayan bir şey görürsen: ekran görüntüsü, bana mesaj.

-----

## Gelecek dersten önce kontrol listesi

- [ ] `uv --version` ve `git --version` birer sürüm numarası yazıyor
- [ ] `git clone` ile indirdiğim `gita3111` klasörüm var
- [ ] `00-hazirlik` içinde `uv run ornekler/kurulum_testi.py` → **KURULUM TAMAM**
- [ ] Kendi verimle `grafik.png` ürettim
- [ ] VS Code'da `gita3111` klasörünü açabiliyorum
- [ ] Cloudflare hesabım var; Account ID ve anahtarım `gita3111/anahtar.txt` dosyasında

Altısı da tamamsa hazırsın. Gelecek dersin başında kurulum testini birlikte bir kez
daha çalıştıracağız; herkesin ekranında **KURULUM TAMAM** görmeden kelime bulutuna
geçmeyeceğiz.

-----

## Her dersten önce: üç satır

```text
cd gita3111
git pull
cd 01-veri-ve-kelime-bulutu
```

- `git pull` → yeni konuyu getirir
- Konunun klasörüne gir → `uv run` o konunun kütüphanelerini kendisi kurar
- Ders öncesi indirme yapmak istersen konunun klasöründe bir kez `uv sync` çalıştır; derste beklemezsin

Bu dönemin ritmi bu: **çek, gir, çalıştır.**
