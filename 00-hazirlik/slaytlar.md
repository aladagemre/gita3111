# Konu 0 — Dersin Tanıtımı ve Kurulum

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Bu ders ne anlatıyor?

- GİTA2112'nin devamı: orada değişken, liste, döngü ve fonksiyonla kodun temelini attık
- Bu dönem yapay zekayı sohbet ekranından değil, **kendi kodumuzdan** kullanacağız
- Sohbet ekranında tek tek sorarsın; kodla yüz soruyu bir kerede sorar, cevapları dosyaya yazarsın
- Ama önce kaputu açacağız: bu modeller nasıl çalışıyor, neden bazen saçmalıyor?
- Matematik yok; her kavramı bir benzetmeyle ve kendi verimizle göreceğiz
- Her konunun sonunda elinde çalışan bir çıktı olacak: bir grafik, bir dosya, bir görsel

-----

## Dönemin iki yarısı

### Birinci yarı: bu şeyler nasıl çalışıyor?

- Veriyi kodla işlemek · koddan bir modele soru sormak (API) · makine öğrenmesi
- Kelimeler nasıl sayıya dönüşür · dil modeli metni nasıl yazar · "üretmek" ne demek

### İkinci yarı: onlarla ne üretiyoruz?

- Arayüzden ve koddan görsel üretimi · toplu üretim · video
- Adımları birbirine bağlayan üretim hattı · kendi kararını veren program
- Dönemin sonunda: kendi kurduğun üretim aracıyla final projesi

-----

## Bir ders nasıl akıyor?

Dersler çevrimiçi ve yaklaşık üç saat; her ders aynı sırayla ilerler:

1. **Nabız yoklaması** (1 dk): küçük bir anket, "kurulumun çalışıyor mu?"
2. **Ödev gösterimi** (20 dk): sırası gelen arkadaş ekranını paylaşır
3. **Kavram** (40 dk): slaytlarla konunun mantığı, kod yok
4. **Birlikte kodlama** (60 dk): ben ekranımda yazarım, sen kendi bilgisayarında aynısını yazarsın
5. **Kendi başına yazma** (40 dk): alıştırmalar; takılınca beklemeden sohbete yaz
6. **Toparlama** (10 dk): konu bittiyse ödev

Bugün farklı: kod yok, kurulumu birlikte göreceğiz.

-----

## Nasıl değerlendirileceksin?

- **Vize %40:** evde yapılır, **yapay zeka yasak**, ardından derste kısa bir sözlü teyit
- **Final projesi %60:** kendi kurduğun üretim aracı, üretim günlüğü ve sunum
- **Konu ödevleri puansız**, ama boş değil: herkes dönem boyunca 2–3 kez ekranını paylaşıp çıktısını gösterecek
- Gösterim sırası önceden belli; hazırlıksız yakalanma
- Çalışmayan kodla gelmek sorun değil; hiç denememiş gelmek sorun

-----

## Yapay zekayla kod yazmak: ne zaman serbest?

- **Kavram konularında serbest**, ama vizede tek başına yazacaksın: aracın yazdığını anlamadan geçmek kendi ayağına sıkmak
- **Vizede yasak:** ölçtüğümüz şey senin kendi programlama becerin
- **Üretim konularında ve finalde serbest, hatta bekleniyor:** kullandığın her yeri üretim günlüğüne yaz
- İyi kullanım: "bu hata ne diyor, açıkla" · kötü kullanım: "ödevi yaz" deyip kopyalamak
- Aracın yazdığı her satırı sesli okuyabiliyor olmalısın

**Sohbete yaz:** geçen dönem Antigravity'yle ne ürettin? Tek cümle.

-----

## Kurulum: dört araç, tek klasör

Gelecek dersten itibaren her derste kod çalıştıracağız. Önce dört araç kurulu olmalı:

- **git:** ders materyalini bilgisayarına indirir ve her hafta günceller
- **uv:** Python'ı ve dersin kütüphanelerini senin yerine kurar
- **VS Code:** kodu yazdığımız ve defterleri açtığımız editör
- **Cloudflare hesabı:** koddan yapay zeka modellerine bağlanmak için ücretsiz anahtar

Hepsi tek bir klasörde buluşur: `gita3111`. Adımları şimdi birlikte göreceğiz; kurulumu **evde**, yazılı yönergeye bakarak yapacaksın: `00-hazirlik/kurulum-yonergesi.md` (yaklaşık 30 dakika).

**Sohbete yaz:** Windows mu kullanıyorsun, macOS mu?

-----

## Terminal nedir?

- Bilgisayara fareyle tıklamak yerine **yazarak** komut verdiğin pencere
- Her zaman bir klasörün **içinde** durur; komutlar o klasörde çalışır
- Windows'ta Başlat → `PowerShell`; macOS'ta Cmd + Boşluk → `Terminal`
- Bu dönem yalnızca üç komut bilmen yeterli:

```text
cd klasor_adi      bir klasörün içine gir
cd ..              bir üst klasöre çık
pwd                neredeyim? (PowerShell'de de aynı)
```

- Dönemin en sık hatası "yanlış klasördeyim" olacak; `pwd` senin pusulan

-----

## Adım 1 — uv: Python'ı kuran araç

**uv ne işe yarar?** Python'ı ve dersin **kütüphanelerini** (başkalarının yazdığı hazır kod paketleri, örneğin kelime bulutu çizen `wordcloud`) senin yerine kurar. Python'ı ayrıca kurmana gerek yok.

**Windows** (PowerShell):

```text
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS** (Terminal):

```text
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Sonra **terminali kapatıp yeniden aç** ve `uv --version` yaz. Bir sürüm numarası görüyorsan tamam; "tanınmıyor" ya da "command not found" diyorsa terminal gerçekten kapatılıp açılmamıştır.

-----

## git ve depo nedir?

- Ders materyali internette bir **depoda** duruyor: github.com/aladagemre/gita3111
- Depo, dosyaların ve onların bütün değişiklik geçmişinin tutulduğu klasör
- **git** bu depoyla bilgisayarın arasında dosya taşıyan araç
- `git clone` → dönemde **bir kez**: depoyu bilgisayarına indirir
- `git pull` → **her dersten önce**: yalnızca yeni ve değişen dosyaları getirir
- Yeni konular geldikçe depoya ekliyorum; klasörü her hafta baştan indirmen gerekmiyor

-----

## Adım 2 — git kurulumu

Önce kurulu mu diye bak: `git --version`. Sürüm numarası çıkarsa bu adımı atla.

**Windows:**

```text
winget install --id Git.Git -e
```

`winget` tanınmıyorsa git-scm.com/download/win adresinden indir; kurulum ekranlarında hiçbir şeyi değiştirmeden **Next** de.

**macOS:** `git --version` yazınca "geliştirici araçlarını yüklemek ister misin?" diye bir pencere açılır; **Yükle** de.

İkisinde de iş bitince **terminali kapat, yeniden aç.**

-----

## Adım 3 — Depoyu indir

Masaüstüne geç ve depoyu indir:

```text
cd Desktop
git clone https://github.com/aladagemre/gita3111.git
```

Masaüstünde artık `gita3111` adında bir klasör var.

- Klasörün yolunda **Türkçe karakter** (ç, ğ, ı, ö, ş, ü) ve **boşluk** olmasın
- "Ders Notları/Yapay Zekâ" gibi bir yol ileride saatlerini yer
- OneDrive'lı Windows'larda Masaüstü yolu uzun olabilir; sorun çıkarsa `C:\gita3111` gibi kısa bir yer seç

-----

## Deponun içi

```text
gita3111/
├── pyproject.toml          dersin kütüphane listesi
├── .venv/                  uv oluşturur (sende oluşur)
├── anahtar.txt             sen oluşturursun (Adım 6)
├── 00-hazirlik/            bu konu: kurulum
├── 01-veri-ve-kelime-bulutu/
│   ├── ders.ipynb          derste birlikte çalıştırdığımız defter
│   ├── alistirma.ipynb     kendi başına çözeceğin alıştırmalar
│   ├── ders_notu.md        evde okuyacağın konu notu
│   └── veri/  odevler/     konunun verisi ve ödevi
└── 02-api-ile-konusmak/    aynı düzen
```

- Her konu kendi klasöründe; baştaki numara hafta değil, **sıra**
- `.venv` ve `anahtar.txt` depoda yok, sende oluşur; `git pull` onlara dokunmaz

-----

## Ortam nedir? `pyproject.toml` ve `.venv`

- Her proje farklı kütüphanelere, bazen farklı Python sürümüne ihtiyaç duyar
- Hepsini bilgisayarın geneline kurarsan projeler birbirini bozar
- Çözüm **ortam**: projeye özel, içinde Python'un ve kütüphanelerin kurulu durduğu bir klasör; bizde adı `.venv`
- `pyproject.toml` dersin **hangi Python'u** ve **hangi kütüphaneleri** kullandığını yazan liste
- `uv sync` bu listeyi okur, eksikleri `.venv`'e kurar
- Sonuç: hiçbir zaman "şu kütüphaneyi kur" diye uğraşmazsın; tek şart komutu `gita3111` klasörünün içinden vermek

-----

## Adım 4 — Kurulumu test et

```text
cd gita3111/00-hazirlik
uv run ornekler/kurulum_testi.py
```

İlk çalıştırmada uv doğru Python sürümünü ve kütüphaneleri indirir; birkaç dakika sürebilir. Ekranda her satırın başında `[OK  ]` ve en altta şunu görmelisin:

```text
KURULUM TAMAM
```

- Cloudflare satırının `[ATLA]` demesi şimdilik normal: anahtarı Adım 6'da ekleyeceksin
- **KURULUM TAMAM** görmüyorsan betik neyin eksik olduğunu yazıyor; ekran görüntüsünü al, derse onunla gel

**Sohbete yaz:** aynı komutu bir üstteki `gita3111` klasöründe yazsan ne olur?

-----

## Hatanın sebebi çoğu zaman nerede durduğun

`gita3111` klasöründe durup aynı komutu yazarsan:

```text
error: Failed to spawn: `ornekler/kurulum_testi.py`
  Caused by: No such file or directory (os error 2)
```

- `ornekler` klasörü `00-hazirlik`'in içinde; `gita3111`'de öyle bir klasör yok
- **"No such file or directory"** → büyük ihtimalle yanlış klasördesin
- **"No module named ..."** → `gita3111`'in dışındasın ya da defterde `.venv` seçili değil
- İlk refleksin: `pwd` yaz, nerede olduğuna bak

-----

## Dönemin kuralı: değiştirmeden önce kopyala

- Depodaki bir dosyayı değiştireceksen önce **aynı klasörde yeni bir adla kopyala**
- Örnek: `alistirma.ipynb` → `benim_alistirmam.ipynb`; sonra kopyada çalış
- **Neden?** `git pull` senin adını verdiğin dosyalara hiç dokunmaz
- Ama depodaki bir dosyayı değiştirdiysen ve ben de o dosyayı güncellediysem, `git pull` durur
- Durursa çözümü bu destenin sonundaki **Ek** slaytında

-----

## Defter nedir? Adım 5 — VS Code

- Bu dönem kodu **defterlerde** (notebook, `.ipynb`) çalıştıracağız
- Defterde kod küçük kutulara (**hücre**) bölünür; her hücreyi ayrı çalıştırıp sonucunu hemen altında görürsün
- Tasarımcı için iyi haber: grafik ve görsel kodun hemen altında çıkar
- VS Code yoksa: code.visualstudio.com → indir → kur
- Sol menüden **Extensions** → **Python** ve **Jupyter** eklentilerini kur (ikisi de Microsoft'un)
- **File → Open Folder** ile `gita3111` klasörünü aç
- **Terminal → New Terminal**: VS Code'un içindeki terminal zaten `gita3111` klasöründe açılır; komutları buradan yaz

-----

## İlk defterin

- VS Code'un terminalinde `uv sync` yaz: ortam hazır olsun
- `00-hazirlik/ilk_defter.ipynb`'i aç ve önce `benim_defterim.ipynb` adıyla kopyala
- Sağ üstte **Select Kernel** → **Python Environments** → `.venv`
- **Çekirdek** (kernel): defterin kodu çalıştırdığı Python; bu dönem her defterde `.venv`'i seçeceksin
- Hücreye tıkla, **Shift + Enter**: hücre çalışır, sonucu altında çıkar
- Kopyada turuncu satırları kendi verinle değiştir, çubuk grafiğin değiştiğini gör

-----

## API anahtarı nedir? Adım 6 — Cloudflare hesabı

- Konu 02'de kodumuzdan internetteki yapay zeka modellerine bağlanacağız
- Model başkasının bilgisayarında çalışıyor; kim olduğunu kanıtlamak için bir **anahtar** gerekiyor
- Anahtar bir şifre gibidir: kimin elindeyse o senin adına istek gönderir
- Hesabı **şimdi** açıyoruz ki sorun çıkarsa çözmeye zamanımız olsun

1. dash.cloudflare.com/sign-up/workers-and-pages adresinde ücretsiz hesap aç, e-postanı doğrula
2. dash.cloudflare.com/?to=/:account/ai/workers-ai adresine git, **Use REST API** bölümünü aç
3. **Account ID**'yi kopyala; **Create a Workers AI API Token** → hiçbir şeyi değiştirmeden **Create API Token** → **Copy**

**Kredi kartı isterse dur ve bana yaz.** Ders tamamen ücretsiz kullanımla tasarlandı.

-----

## Anahtarı nereye kaydedeceksin?

`gita3111` klasörünün içinde, konu klasörlerinin **yanında**, `anahtar.txt` adlı tek bir dosya:

```text
ACCOUNT_ID = buraya_account_id
API_TOKEN = buraya_anahtar
```

- Bütün konuların kodu anahtarı buradan okur
- Bu dosya depoya hiçbir zaman gönderilmez; `git pull` da ona dokunmaz
- Anahtarı **kimseyle paylaşma** ve **ödev teslimine koyma**
- Anahtar ekranı **bir kez** görünür; kapatırsan yenisini üretirsin, sorun değil
- Kaydettikten sonra kurulum testini bir kez daha çalıştır: Cloudflare satırı da **OK** olmalı

-----

## Güvenlik: komutu sen onayla

- Antigravity gibi yapay zeka destekli kod araçları terminalde kendi başına komut çalıştırabilir
- Bir komut dosya silebilir, bir yere veri gönderebilir; araç bunun farkında olmayabilir
- Aracın komutları **onaysız çalıştırmasını kapat**
- Her komutu **okuyup sen onayla**; anlamadığın komutu çalıştırmadan önce sor
- Araç `anahtar.txt` dosyanı okuyup bir yere gönderebilir; bunu durduran şey senin onayın

-----

## Gelecek dersten önce kontrol listesi

- `uv --version` ve `git --version` birer sürüm numarası yazıyor
- `git clone` ile indirdiğim `gita3111` klasörüm var
- `00-hazirlik` içinde `uv run ornekler/kurulum_testi.py` → **KURULUM TAMAM**
- VS Code'da `ilk_defter.ipynb`'in kopyasını `.venv` çekirdeğiyle çalıştırdım, kendi verimle grafik çizdim
- Cloudflare hesabım var; Account ID ve anahtarım `gita3111/anahtar.txt` dosyasında

Beşi de tamamsa hazırsın. Gelecek dersin başında kurulum testini birlikte bir kez daha çalıştıracağız.

-----

## Her dersten önce: gir, çek, kur, aç

1. **Gir:** VS Code'da `gita3111` klasörünü aç, **Terminal → New Terminal**
2. **Çek:** `git pull` (yeni konuyu getirir)
3. **Kur:** `uv sync` (yeni konunun kütüphanelerini kurar)
4. **Aç:** konunun `ders.ipynb` defterini aç, çekirdek olarak `.venv`'i seç

Bu dönemin ritmi bu. Gelecek ders kelime bulutuyla başlıyoruz.

Sondaki iki **Ek** slaytı derste anlatılmaz; evde takılırsan bak.

-----

## Ek — git pull takılırsa

Şu hatayı görürsen bir depo dosyasını değiştirmişsin demektir:

```text
error: Your local changes to the following files would be overwritten by merge
```

1. Değiştirdiğin dosyayı **yeni bir adla kopyala** (emeğin kaybolmasın)
2. Depo dosyalarını ilk hâline döndür: `git restore .`
3. Tekrar dene: `git pull`

Senin oluşturduğun dosyalar (kopyalar, üretilen görseller, `anahtar.txt`) bu işlemden etkilenmez.

-----

## Ek — Sık karşılaşılan sorunlar

| Belirti | Sebep | Çözüm |
|---|---|---|
| `uv` / `git` tanınmıyor | Kurulumdan sonra terminal yenilenmedi | Terminali kapat, yeniden aç |
| İnternet hatası (`uv sync`, `git clone`) | Üniversite ağı bazı adresleri kapatıyor | Telefon internetini paylaşıp tekrar dene |
| "No such file or directory" | Yanlış klasördesin | `pwd` ile bak, doğru klasöre `cd` ile gir |
| "Repository not found" | Depo adresi yanlış yazıldı | Adresi kopyala-yapıştır yap |
| **Select Kernel** listesinde `.venv` yok | `uv sync` çalıştırılmadı ya da alt klasör açıldı | `gita3111`'de `uv sync`; VS Code'da `gita3111`'i aç, listeyi yenile |
| Cloudflare satırı HTTP 401 | Token yanlış kopyalandı | Yeni token üret, `anahtar.txt`'ye yapıştır |
| Cloudflare satırı HTTP 403 | Token'ın izinleri eksik | Token'ı hazır bilgileri değiştirmeden yeniden üret |

Listede olmayan bir şey görürsen: ekran görüntüsü, bana mesaj.
