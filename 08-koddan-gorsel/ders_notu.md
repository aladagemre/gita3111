# Konu 8 — Koddan Görsel Üretimi

Bu not konunun özetidir; derste çalıştırdığımız `ders.ipynb` defteriyle **aynı sırada**
ilerler: Isınma, sonra Adım 1–9 ve kısa bir Bonus. Derste kaçırdığın bir yer olursa
buradan oku, sonra defterde o adımın hücrelerini çalıştır. Nottaki kod blokları
defterdeki hücrelerin birebir aynısı.

**Konu 2'de:** koddan bir modele istek gönderip metin cevabı aldık.
**Konu 7'de:** `ciz("...")` yazdık, `ciktilar/001.jpg` çıktı. Arada ne olduğunu görmedik.
**Bu konuda:** o arayı **kendimiz yazıyoruz**:

> İstek → durum kodu → base64 metni → bayt → `"wb"` ile dosya. Dosya adı kendini anlatır;
> yazmadan önce "bu ad alınmış mı?" diye sorulur. Hata olunca program çökmez.

Konu 7'de kod yazmadık; bugün yeniden yazıyoruz. Yeni kavram çok, ama her biri ayrı bir adımda geliyor;
anahtar, istek, durum kodu ve fonksiyon Konu 2'den tanıdık.

**Konunun sonunda elinde:** yönergeyi kullanıcıdan alıp görsel üreten ve düzenli bir klasöre,
kendini anlatan bir adla kaydeden iki fonksiyon (`ciz`, `kaydet`) ve koddan düzenlenmiş bir görsel.

**Kurulum:** yeni kütüphane yok. `git pull` ile konu klasörü geldikten sonra `gita3111` klasöründe
bir kez `uv sync` çalıştır. `base64`, `pathlib` ve `datetime` Python'un içinde geliyor; `PIL`
(görsel açıp küçültmek için) önceki konulardan kurulu.

**Anahtar:** Isınma anahtarsız. Adım 1'den sonrası `anahtar.txt` ister (Konu 2'deki dosyanın aynısı,
`gita3111` klasöründe). Defterin tamamı 5 görsel üretir; ücretsiz günlük kotanın küçük bir kısmı.

**Bilerek hata veren hücreler:** Isınma'da, Adım 4'te ve Adım 8'de birer hücre bilerek hata verir.
Kırmızı yazı orada bir deneyin sonucudur; okuyup devam et.

> **Bu nottaki çıktılar hakkında.** Isınmanın çıktıları her bilgisayarda aynıdır. Adım 2'den sonraki
> görseller gerçek modelden gelir; uzunluklar ve dosya adlarındaki tarih senin ekranında farklı olur.

---

## Isınma: görsel de bir dosya, ama metin değil

Konu 2'de cevapları `"w"` ile bir metin dosyasına yazmıştık. Bu klasörde `veri/fincan.jpg` adında
küçük bir görsel var. Onu bir metin dosyası gibi açmayı deniyoruz:

```python
with open("veri/fincan.jpg", encoding="utf-8") as dosya:
    icerik = dosya.read()
```

Çıktı (son satır):

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
```

Python dosyadaki sayıları harflere çevirmeye çalıştı (`encoding="utf-8"` bunu söylüyor) ve
çeviremedi. Bir görsel harflerden değil, **baytlardan** oluşur: 0 ile 255 arasında sayılar.
Aralık Konu 3'teki RGB değerleriyle aynı; ama JPEG'de bu sayılar doğrudan renkler değil,
sıkıştırılmış veri. Bu tür dosyaya **ikili dosya** (binary) denir. Görseller, sesler, PDF'ler
ikili dosyadır.

İkili dosyayı açmanın yolu `"rb"`: **r**ead (oku) + **b**inary (ikili). `encoding` yazılmaz;
harfe çevirme yok.

```python
with open("veri/fincan.jpg", "rb") as dosya:
    baytlar = dosya.read()

print(len(baytlar))
print(baytlar[:12])
```

Çıktı:

```
9579
b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01'
```

- `len(baytlar)`: görsel 9579 bayt (yaklaşık 9,5 KB).
- `baytlar[:12]`: ilk 12 bayt. Başındaki `b'...'` "bu bir bayt dizisi" demek. `\xff` gibi
  yazılanlar harfe karşılık gelmeyen baytlar.
- İlk iki bayt (`\xff\xd8`) her JPEG'de aynıdır. `JFIF` yazısı da çoğu JPEG'de bulunur ve "ben bir
  JPEG'im" der. (Fotoğraf makinelerinin JPEG'lerinde onun yerine `Exif` görebilirsin.)

### Isınma 2: görseli metne çevirmek, base64

API'ler cevabı JSON içinde, **metin** olarak gönderir (Konu 2). Görsel ise bayt. **base64**,
baytları harf ve rakamlara çeviren bir kodlama (`b64encode`); öbür uçta geri çevrilir (`b64decode`):

```python
import base64

metin = base64.b64encode(baytlar)
print(len(metin))
print(metin[:40])
```

Çıktı:

```
12772
b'/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAUDBAQE'
```

- 9579 bayt 12772 karaktere dönüştü: base64'te her 3 bayt 4 karakter olur; metin üçte bir kadar uzar.
- İçinde yalnızca harf, rakam, `+` ve `/` var. Her JPEG'in base64 hâli `/9j/` ile başlar.
- Başta hâlâ `b'...'` görünüyor: `b64encode` sonucu bayt olarak verir; ama bu baytların her biri bir harfe karşılık gelir.
- **Yanılgı:** base64 şifreleme ya da sıkıştırma değildir. Dosyayı büyütür ve herkes geri çevirebilir.

Geri çevirip asılla karşılaştırıyoruz:

```python
geri = base64.b64decode(metin)
print(geri == baytlar)
```

Çıktı: `True`. Tek bayt kaybolmadı. E-posta ekleri de yıllardır base64 metni olarak gönderilir.

---

## Adım 1 — Anahtar, adres, başlık

Konu 2'nin Adım 1–2'sinin aynısı:

```python
anahtarlar = {}
with open("../anahtar.txt", encoding="utf-8") as dosya:
    for satir in dosya:
        parcalar = satir.split("=")
        ad = parcalar[0].strip()
        deger = parcalar[1].strip()
        anahtarlar[ad] = deger

hesap = anahtarlar["ACCOUNT_ID"]
anahtar = anahtarlar["API_TOKEN"]
print("Anahtar okundu")
```

```python
import base64
import requests

MODEL = "@cf/black-forest-labs/flux-1-schnell"
adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
basliklar = {"Authorization": f"Bearer {anahtar}"}
```

- Yalnızca model değişti: `@cf/black-forest-labs/flux-1-schnell`, Konu 7'deki `flux` (FLUX.1 schnell).
- `import base64` Isınma 2'de de vardı; burada bir daha alıyoruz ki deftere Adım 1'den başlayan da kullanabilsin.
  Aynı kütüphaneyi iki kez almak sorun değil.

---

## Adım 2 — İsteği gönder

```python
govde = {"prompt": "a ceramic coffee cup on a wooden desk, watercolor illustration", "seed": 42}
cevap = requests.post(adres, headers=basliklar, json=govde)
print(cevap.status_code)
```

- Gövdede iki alan var: `prompt` (yönerge) ve `seed` (tohum). Konu 7'deki
  `ciz(yonerge, tohum=42)` tam olarak bunu gönderiyordu.
- `200` gördüysen istek başarılı. Görsel birkaç saniyede gelir.

---

## Adım 3 — Yanıtın içi

```python
yanit = cevap.json()
sonuc = yanit["result"]
metin = sonuc["image"]

print(len(metin))
print(metin[:40])
```

Konu 2'deki gibi önce `result` kutusunu, sonra içindeki alanı açıyoruz. Metin modelinde alanın
adı `response` idi; görsel modelinde `image`. İçinde çok uzun bir harf dizisi var ve `/9j/` ile
başlıyor: görsel, base64 metni olarak geldi (Isınma 2). Bu kez başta `b'` yok: JSON'dan gelen
her şey düz metindir.

---

## Adım 4 — Metinden görsele, görselden dosyaya

`b64decode` metni baytlara çevirir:

```python
resim = base64.b64decode(metin)
print(len(resim))
```

Bir sayı yazar: görselin bayt sayısı. Şimdi baytları dosyaya yazacağız. Önce Konu 2'deki gibi `"w"` ile deniyoruz:

```python
with open("deneme.jpg", "w") as dosya:
    dosya.write(resim)
```

Çıktı (son satır):

```
TypeError: write() argument must be str, not bytes
```

Hata "yazılacak şey metin olmalı, bayt değil" diyor: `"w"` metin yazar, biz bayt verdik. (Dosya açıldığı için klasörde boş bir `deneme.jpg`
oluştu; silebilirsin.) Baytları yazmanın yolu `"wb"`: **w**rite (yaz) + **b**inary (ikili).

```python
with open("ilk.jpg", "wb") as dosya:
    dosya.write(resim)
```

Klasörde `ilk.jpg` oluştu; VS Code'da tıklayıp açabilirsin. Defterde göstermek için:

```python
import matplotlib.pyplot as plt

plt.imshow(plt.imread("ilk.jpg"))
plt.axis("off")
plt.show()
```

- `plt.imread` bir görsel dosyasını okuyup sayı tablosuna çevirir; `plt.imshow` Konu 6'daki gibi çizer.
- Konu 7'de `ciz` yazınca arka planda olan buydu: metin → bayt → dosya.

| Kip | Anlamı | Ne için |
|---|---|---|
| `"r"` | metin oku | `.txt`, `.md`, `.csv` |
| `"w"` | metin yaz | `cevaplar.txt` (Konu 2) |
| `"rb"` | ikili oku | `.jpg`, `.png`, `.pdf`, ses |
| `"wb"` | ikili yaz | görseli dosyaya kaydetmek |

---

## Adım 5 — Fonksiyona koy: `ciz`

```python
def ciz(yonerge, tohum):
    govde = {"prompt": yonerge, "seed": tohum}
    cevap = requests.post(adres, headers=basliklar, json=govde)
    if cevap.status_code != 200:
        print("İstek başarısız, durum kodu:", cevap.status_code)
        return None
    yanit = cevap.json()
    sonuc = yanit["result"]
    metin = sonuc["image"]
    return base64.b64decode(metin)
```

- Adım 2–4'ün (dosyaya yazma hariç) aynısı, tek bir adın altında (Konu 2'deki `modele_sor` gibi). Böylece her
  görselde aynı satırları yeniden yazmayız.
- **Yeni:** durum koduna bakıyoruz. 200 değilse fonksiyon bir mesaj yazar ve `None` döndürür.
  `None`, Python'da "hiçbir şey" demek.
- `return` fonksiyonu **orada bitirir**: alttaki `cevap.json()` satırları hiç çalışmaz. Böylece
  program, içinde görsel olmayan bir yanıtı açmaya çalışıp çökmez.
- Fonksiyon görselin **baytlarını** geri verir; dosyaya yazmak başka bir fonksiyonun işi (Adım 7).
  Her fonksiyon tek bir iş yapar.
- Konu 7'deki `ciz` kaydedip gösteriyordu ve tohum zorunlu değildi; bizimki şimdilik yalnızca baytları
  veriyor. Aynı ad, farklı bir fonksiyon.

```python
resim = ciz("a red bicycle leaning on a yellow wall, flat vector poster", 7)
print(len(resim))
```

Yine görselin bayt sayısını görürsün. Henüz dosyaya kaydetmedik.

---

## Adım 6 — Düzenli klasör, düzenli ad

"gorsel.jpg", "gorsel2.jpg", "son_son.jpg"... Bir hafta sonra hangisi neydi, bilemezsin. Dosya adı
kendini anlatmalı: **ne zaman**, **hangi yönergeyle**, **hangi tohumla**.

```python
from pathlib import Path
from datetime import datetime

klasor = Path("ciktilar")
klasor.mkdir(exist_ok=True)
```

- `Path` (pathlib kütüphanesinden) dosya ve klasör yollarıyla çalışır.
- `klasor.mkdir(exist_ok=True)`: `ciktilar` klasörünü oluşturur. `exist_ok=True` "zaten varsa
  sorun yok" demek; yazmazsan ikinci çalıştırmada `FileExistsError` alırsın.
- `datetime` tarih ve saatle çalışan kütüphane.

Adı üç parçadan kuruyoruz. Önce **tarih**:

```python
simdi = datetime.now()
tarih = simdi.strftime("%Y-%m-%d_%H-%M-%S")
print(tarih)
```

Çıktı (senin ekranında o anın tarihi): `2026-10-19_18-57-25`

- `datetime.now()`: şu anki tarih ve saat.
- `strftime(...)`: tarihi istediğimiz biçimde yazar. `%Y` yıl, `%m` ay, `%d` gün, `%H` saat,
  `%M` dakika, `%S` saniye. **Dikkat:** küçük `m` ay, büyük `M` dakika; bu ikisini karıştırmak en sık yapılan hatalardan biri.
- Yıl başta olduğu için dosyalar adlarına göre sıralanınca tarih sırasına da girer.
- İki nokta (`:`) yerine tire kullanıyoruz: Windows dosya adında `:` kabul etmez.

Sonra **yönergenin başı**:

```python
yonerge = "a red bicycle leaning on a yellow wall, flat vector poster"
tohum = 7
ozet = yonerge[:20].replace(" ", "-")
ad = f"{tarih}_{ozet}_{tohum}.jpg"
print(ad)
```

Çıktı: `2026-10-19_18-57-25_a-red-bicycle-leanin_7.jpg`

- `yonerge[:20]`: yönergenin ilk 20 karakteri (Konu 3'teki `[:adet]` gibi; boşluklar da sayılır).
  Kesik olabilir (`leanin`); amaç hatırlatmak.
- `.replace(" ", "-")`: boşlukları tireye çevirir. Dosya adında boşluk sorun çıkarabilir.
- Üçüncü parça tohum; en sona `.jpg` ekliyoruz.
- Bizim kod yalnızca boşluğu düzeltiyor. Yönergenin ilk 20 karakterinde `/` olursa Python onu bir alt
  klasör sanır; Windows'ta `\ : ? * " < > |` işaretleri de hata verir. Yönergeye bu işaretleri koyma.

Son olarak klasörle birleştiriyoruz:

```python
yol = klasor / ad
print(yol)
```

- `klasor / ad`: `Path`'te `/` "bu klasörün içindeki bu dosya" demek.
- Windows'ta yol ekranda `ciktilar\2026-...` diye, ters bölüyle görünür; ikisi aynı şey.

Yazmadan önce bakıyoruz: bu adda bir dosya **zaten var mı**?

```python
if yol.exists():
    print("Bu ad alınmış, üzerine yazmıyorum:", yol)
else:
    with open(yol, "wb") as dosya:
        dosya.write(resim)
    print("Kaydedildi:", yol)
```

- `yol.exists()`: dosya varsa `True`.
- Varsa üzerine yazmıyoruz; önceki görsel kaybolmasın. Yoksa Adım 4'teki gibi `"wb"` ile yazıyoruz.

Hücreyi **bir kez daha** çalıştır: `Bu ad alınmış, üzerine yazmıyorum` yazar. `yol` değişmedi
(tarih bir önceki hücrede hesaplandı), dosya artık var.

---

## Adım 7 — Hepsi bir arada: yönergeyi kullanıcıdan al

Adım 6'nın satırlarını da bir fonksiyona koyuyoruz:

```python
def kaydet(resim, yonerge, tohum):
    simdi = datetime.now()
    tarih = simdi.strftime("%Y-%m-%d_%H-%M-%S")
    ozet = yonerge[:20].replace(" ", "-")
    yol = klasor / f"{tarih}_{ozet}_{tohum}.jpg"
    if yol.exists():
        print("Bu ad alınmış, üzerine yazmıyorum:", yol)
        return None
    with open(yol, "wb") as dosya:
        dosya.write(resim)
    return yol
```

- `kaydet` baytları, yönergeyi ve tohumu alır; dosyanın yolunu geri verir.
- Ad alınmışsa `None` döndürür ve hiçbir şeyi silmez.
- Adda saniye olduğu için bu kontrol çoğu zaman devreye girmez. Ama aynı saniyede iki kayıt olursa ya da
  bir gün adı tarihsiz kurarsan (Konu 7'deki `001.jpg` gibi) seni korur.

```python
yonerge = input("Yönerge (İngilizce): ")
tohum = 1
resim = ciz(yonerge, tohum)
if resim is not None:
    yol = kaydet(resim, yonerge, tohum)
    print(yol)
```

- Şimdiye kadar yönergeyi kodun içine yazdık; şimdi programın kendisi soruyor.
- `input` GİTA2112'den tanıdık: kullanıcıya bir soru sorar, yazdığını metin olarak verir. VS
  Code'da ekranın üstünde bir kutu açılır; yönergeni İngilizce yaz, **Enter**'a bas.
- `resim is not None`: "resim boş değilse", yani istek başarılıysa.
- Sonuç: `ciktilar/` içinde adı kendini anlatan bir dosya: görselin ne zaman, hangi yönergeyle ve
  hangi tohumla üretildiğini söylüyor. Konu 7'de elle tuttuğumuz üretim günlüğünün bir kısmı artık
  dosya adında (yönergenin tamamı ve model adı yine günlükte durmalı).

---

## Adım 8 — Hata yakalama: cevap hiç gelmezse

İki tür başarısızlık var:

| Durum | Örnek | Ne olur | Nasıl yakalanır |
|---|---|---|---|
| Sunucu cevap verdi ama "olmaz" dedi | 401 anahtar yanlış, 429 çok hızlı istek, 400 ayar yanlış | Yanıt gelir, içinde görsel yok | Durum kodu (`ciz` içinde) |
| Cevap hiç gelmedi | internet yok, adres yanlış | `requests.post` hata fırlatır, program **durur** | `try` / `except` |

İkincisini görmek için isteği var olmayan bir adrese gönderiyoruz. `.invalid` diye bir alan adı
yoktur; bilgisayar o sunucuyu bulamaz. Asıl `adres`'e dokunmuyoruz; bozuk adres ayrı bir değişkende:

```python
bozuk_adres = "https://api.cloudflare.invalid/ai/run/flux"
cevap = requests.post(bozuk_adres, headers=basliklar, json=govde)
```

Uzun bir kırmızı yazı çıkar (hata zinciri). **Yalnızca en alttaki satırı oku:**

```
ConnectionError: HTTPSConnectionPool(host='api.cloudflare.invalid', port=443): ...
```

Hücre orada durdu. Bir döngünün ortasında olsaydık bütün iş dururdu. `try` / `except` ile "dene;
şu hata çıkarsa çökme, şunu yap" diyoruz:

```python
try:
    cevap = requests.post(bozuk_adres, headers=basliklar, json=govde)
except requests.exceptions.ConnectionError:
    print("Sunucuya ulaşılamadı. İnternetini kontrol et, sonra yeniden dene.")
```

- `try:` altındaki satırlar denenir.
- Orada `requests.exceptions.ConnectionError` çıkarsa program durmaz, `except` altındaki satırlara
  geçer. `except`'ten sonra yazdığımız ad, en alttaki satırdaki hatanın adı. Bu hata `requests`
  kütüphanesine ait; bu yüzden başında `requests.exceptions.` var.
- Hatayı **adıyla** yakalıyoruz. Yalnızca `except:` yazmak her hatayı sessizce geçiştirir; yazım
  hatalarını bile saklar ve neyin bozulduğunu bulmayı zorlaştırır.

Çıktı:

```
Sunucuya ulaşılamadı. İnternetini kontrol et, sonra yeniden dene.
```

Gerçek bir araçta `try`'ı `ciz` çağrısının etrafına koyarsın: bir döngüde bir istek bağlanamazsa program durmaz, sıradakine geçer.

---

## Adım 9 — Var olanı değiştirmek: düzenleme koddan

Bu adımı derste hoca gösterir; sen izle, evde kendin çalıştır.

Konu 7'deki `duzenle` başka bir modelle (FLUX.2 klein) çalışıyordu ve görseli **bir form gibi**
gönderiyordu: yazı alanları (talimat, boyut, tohum) + bir dosya (görsel). Düzenleyici en fazla
512 × 512 piksel kabul ediyor; önce küçültüyoruz:

```python
from PIL import Image

gorsel = Image.open("ilk.jpg")
gorsel.thumbnail((512, 512))
gorsel.save("ilk_kucuk.jpg")
```

- `PIL` (Pillow) görsel açıp düzenlemeye yarayan kütüphane.
- `Image.open` görseli açar. `thumbnail((512, 512))` en-boy oranını koruyarak 512 × 512'lik bir kutuya sığdırır;
  sonucu bir değişkene atamıyoruz, çünkü görseli **yerinde** değiştirir. İç içe parantez: `(512, 512)`
  tek bir bilgi, "en ve boy".
- `save` yeni bir dosyaya yazar.

```python
DUZENLEYICI = "@cf/black-forest-labs/flux-2-klein-4b"
duzen_adresi = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{DUZENLEYICI}"
alanlar = {
    "prompt": "make the background a plain sage green color",
    "width": "512",
    "height": "512",
    "seed": "42",
}

with open("ilk_kucuk.jpg", "rb") as dosya:
    dosyalar = {"input_image_0": dosya}
    duzen_cevap = requests.post(duzen_adresi, headers=basliklar, data=alanlar, files=dosyalar)

print(duzen_cevap.status_code)
```

- Bu kez `json=` yok. Yazı alanları `data=` ile, dosya `files=` ile gidiyor: bir web formuna dosya
  eklemek gibi.
- Formlar her şeyi metin olarak gönderir; o yüzden sayılar tırnak içinde: `"512"`, `"42"`.
- `"input_image_0"` modelin ilk girdi görselinin alanı (sayma 0'dan başlıyor).
- Dosya `"rb"` ile açılıyor (Isınma). İstek `with` bloğunun **içinde** gönderiliyor, çünkü dosya ancak
  açıkken okunabilir.

Üstteki hücre `200` yazmadıysa bir sonrakini çalıştırma: yanıtta görsel yok (Adım 5'teki kural).

```python
yanit = duzen_cevap.json()
sonuc = yanit["result"]
metin = sonuc["image"]
duzenlenmis = base64.b64decode(metin)

yol = kaydet(duzenlenmis, "edit sage green background", 42)
plt.imshow(plt.imread(yol))
plt.axis("off")
plt.show()
```

Yanıt yine base64: Adım 3–4'ün aynısı. Bu kez `kaydet` ile düzenli bir ada yazıp gösteriyoruz.
Dosya adındaki 42, düzenleme isteğine gönderdiğimiz tohum. Cevabı neden ayrı bir değişkende (`duzen_cevap`)
tuttuk? İstek hiç gitmezse bu hücre `NameError` verir ve hata görünür olur. Aynı adı kullansaydık Adım 2'nin
`cevap`'ı sessizce kullanılır, eski görsel "düzenlenmiş" diye kaydedilirdi.

**Üretimde de düzenlemede de desen aynı:** istek → durum kodu → base64 metni → bayt → `"wb"` ile dosya.
İleride video üretimi de çoğunlukla bu deseni kullanır.

---

## Bonus

**1. Tekrar deneme.**

```python
for deneme in [1, 2, 3]:
    resim = ciz("a paper boat on a puddle, linocut print", 3)
    if resim is not None:
        print("Başarılı, deneme:", deneme)
        break
    print("Olmadı")

if resim is None:
    print("Üç denemede de olmadı; durum koduna bak")
```

- Kısa sürede çok istek gönderdiysen (429) yeniden denemek işe yarayabilir. Günlük kota dolduysa
  beklemek de yeniden denemek de işe yaramaz; kota ertesi gün 03:00'te (Türkiye saati) yenilenir.
- `break` döngüyü erken bitirir: başarılı olunca kalan denemeler yapılmaz.
- Sınır koyduk: en fazla üç deneme. Üçü de olmazsa döngüden sonraki `if` bunu söylüyor.
- Bu kod denemeler arasında beklemiyor; gerçek bir araçta birkaç saniye beklenir (`time.sleep`). Beklemeyi Konu 9'da ekleyeceğiz.

**2. Konu 7'nin aracını oku.** `../07-arayuzden-gorsel/gorsel_araci.py` dosyasını VS Code'da aç.
Çoğu parçasını artık tanıyorsun:

| Araçtaki fonksiyon | Bu defterde |
|---|---|
| `anahtari_oku`, `adres_ve_baslik` | Adım 1 |
| `ciz` | Adım 2–5 (kaydetmeyi de kendisi yapıyor; `write_bytes` = `open(..., "wb")` + `write`) |
| `durumu_denetle` | Adım 5'teki durum kodu kontrolü (`None` yerine hata fırlatıyor) |
| `yeni_dosya_adi` | Adım 6 (tarih yerine sıra numarası: `001.jpg`, `002.jpg`...) |
| `resmi_goster` | Adım 4'teki `imshow` |
| `duzenle` | Adım 9 |

Bir istisna: araçtaki `sdxl` modeli görseli base64 metni olarak değil, doğrudan bayt olarak
gönderiyor (`cevap.content`). Desenin "metin" adımı orada yok.

**3. Konu 9'a hazırlık.** Bu iki fonksiyonla (`ciz`, `kaydet`) birkaç stil ve birkaç rengin bütün
eşleşmelerini nasıl üretirdin? Ortadaki bir istek hata verirse ne olur?

---

## Defterin bölümleri

| Adım | Ne yaptık | Elimizde ne oluştu | Anahtar |
|---|---|---|---|
| Isınma | Görseli metin gibi açmayı denedik; `"rb"`; base64 | `baytlar`, `metin` | gerekmez |
| 1 | Anahtar, adres, başlık | `adres`, `basliklar` | gerekir |
| 2 | İsteği gönderdik | `cevap` | gerekir |
| 3 | Yanıtın içine baktık | `metin` (base64) | gerekir |
| 4 | Metni baytlara çevirip `"wb"` ile yazdık | `ilk.jpg` | gerekir |
| 5 | `ciz` fonksiyonu | `ciz(yonerge, tohum)` | gerekir |
| 6 | Klasör ve kendini anlatan dosya adı | `klasor`, `tarih`, `ad`, `yol` | gerekir |
| 7 | `kaydet` fonksiyonu; yönerge `input` ile | `ciktilar/...jpg` | gerekir |
| 8 | Bağlantı hatasını `try` / `except` ile yakaladık | — | gerekir |
| 9 | Görseli koddan düzenledik | düzenlenmiş görsel | gerekir |
| Bonus | Tekrar deneme; aracı okumak; Konu 9 sorusu | — | yalnız 1. madde gerekir |

`ilk.jpg`, `ilk_kucuk.jpg` ve `deneme.jpg` konu klasörüne; `ciz` + `kaydet` ile üretilenler `ciktilar/`
klasörüne yazılır.

Derste kendi başına çalışacağın defter: `alistirma.ipynb`. Önce aynı klasörde yeni bir adla
kopyala, kopyada çalış. **Anahtar istemez:** modelin yanıtını taklit ediyor (`veri/fincan.jpg`'yi
base64'e çevirip API'nin biçiminde bir sözlüğe koyuyor). İki bölümü var:

- **Bozuk kodlar:** beş kısa hücre, birbirinden bağımsız. Dördü hata mesajı veriyor, biri sessizce
  yanlış sonuç yazıyor; üstlerinde ne yapmaları gerektiği yazıyor.
- **Kendi başına:** `BOSLUK` yazan yerleri doldurduğun yedi soru ve bir ek soru (küçük bir `kaydet`
  fonksiyonu). Her sorunun üstünde doğru çıktı yazılı.

---

## Sık karşılaşılan hatalar ve mesajlarını okumak

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff ...` | Görsel metin gibi açıldı | `open(..., "rb")` |
| `TypeError: write() argument must be str, not bytes` | Baytlar `"w"` ile yazıldı | `open(..., "wb")` |
| `KeyError: 'image'` | Yanıtta `image` doğrudan aranıyor; önce `result` açılmalı | `sonuc = yanit["result"]`, sonra `sonuc["image"]` |
| `KeyError: 'response'` | Konu 2'nin alan adı kullanıldı | Görsel modelinde alan `image` |
| `TypeError: object of type 'NoneType' has no len()` (Adım 5) | `ciz` başarısız oldu ve `None` döndü; sonraki satır onu görsel sandı | Üstte `İstek başarısız, durum kodu: ...` yazıyor; ona bak. Sonra `if resim is not None:` ile kontrol et |
| `TypeError: 'NoneType' object is not subscriptable` (Adım 3 ya da 9) | Durum kodu 200 değilken yanıt açıldı; `result` boş | Üstteki hücrenin yazdığı durum koduna bak |
| `İstek başarısız, durum kodu: 401` | Anahtar yanlış | `anahtar.txt`'yi kontrol et |
| `İstek başarısız, durum kodu: 404` | `ACCOUNT_ID` yanlış ya da model adı yanlış yazılmış | `anahtar.txt` ve `MODEL` satırı |
| `İstek başarısız, durum kodu: 429` | Kısa sürede çok istek ya da günlük kota doldu | Biraz bekle; kota dolduysa ertesi gün 03:00'te (Türkiye) yenilenir |
| `NameError: name 'base64' is not defined` | Isınma 2 ve Adım 1'in ikinci hücresi çalıştırılmadı | Adım 1'in iki hücresini çalıştır |
| `FileNotFoundError: ... 'ciktilar/...'` | Klasör oluşturulmadan içine yazılmak istendi | `klasor.mkdir(exist_ok=True)` (Adım 6'nın ilk hücresi) |
| `FileNotFoundError: ... 'ciktilar/2026-..._a/b...'` ya da Windows'ta `OSError` | Yönergenin ilk 20 karakterinde `/` ya da Windows'un kabul etmediği bir işaret (`\ : ? * " < > |`) var | Yönergeyi bu işaretler olmadan yaz (macOS'ta `:` hata vermeyebilir ama yine kullanma) |
| `FileNotFoundError: ... '../anahtar.txt'` | Anahtar dosyası yok ya da yanlış yerde | `gita3111` klasöründe durmalı |
| `FileNotFoundError: ... 'veri/fincan.jpg'` | Defterin kopyası konu klasörünün dışında | Kopya `08-koddan-gorsel` klasöründe durmalı |
| `ConnectionError: ...` (Adım 8 dışında) | İnternet yok | İnternete bağlan |
| `NameError: name 'datetime' is not defined` (Adım 6 ya da 7) | Adım 6'nın ilk hücresi çalıştırılmadı | Adım 6'dan başlayarak çalıştır |
| `NameError: name 'ciz' is not defined` (Adım 7) | Adım 5'in `ciz` hücresi çalıştırılmadı | Adım 5'i çalıştır |
| `NameError: name 'resim' is not defined` | Adım 4'ün `b64decode` hücresi atlandı | O hücreyi çalıştır |
| `FileNotFoundError: ... 'ilk.jpg'` (Adım 9) | Adım 4'ün `"wb"` hücresi çalıştırılmadı | Adım 4'ü çalıştır |
| `İstek başarısız, durum kodu: 400` | Yönerge boş ya da bir ayar sınır dışı | Yönergeyi yaz; ayarlara bak |
| Adım 7'de hücre bitmiyor, yıldız `[*]` dönüyor | `input` cevap bekliyor | Ekranın üstündeki kutuya yönergeni yaz, Enter |
| Dosya adındaki ay tuhaf (`2026-57-19`) ya da dakika hep aynı sayı | `%m` (ay) ile `%M` (dakika) karıştı | Küçük `m` ay, büyük `M` dakika |
| `Bu ad alınmış, üzerine yazmıyorum` | Adım 6'nın son hücresini ikinci kez çalıştırdın (beklenen sonuç) ya da aynı saniyede aynı yönerge ve tohumla ikinci kayıt yapıldı | Bu bir hata değil; tohumu değiştir ya da bir saniye sonra tekrar çalıştır |

---

## Kendini dene

Cevaplar notun en sonunda. Önce kendin düşün.

1. Bir `.pdf` dosyasını açmak için hangi kipi kullanırsın? Bir `.csv` dosyasını?
2. 3 MB'lık bir fotoğrafı base64'e çevirip bir API'ye gönderiyorsun. Gönderilen metin kabaca kaç MB?
3. Dosya adına tarihi neden `19-10-2026` değil `2026-10-19` diye yazdık?
4. `kaydet` fonksiyonundaki `if yol.exists():` satırlarını silersen ne olur? Ne zaman fark edersin?
5. Arkadaşın `ciz` fonksiyonunda durum kodu kontrolünü sildi. Anahtarı yanlışsa hangi hatayı görür, hata nerede çıkar?
6. Neden `except:` yerine `except requests.exceptions.ConnectionError:` yazdık?
7. Bir müşteri "geçen ay ürettiğin afişin aynısını, bu kez kırmızıyla" istiyor. Elinde yalnızca dosya var. Dosyanın adı sana nasıl yardım eder?

---

## Bu konuda öğrendiklerin

- **İkili dosya.** Görseller harf değil bayttır: `"rb"` ile okunur, `"wb"` ile yazılır.
- **base64.** Baytları harf ve rakamlara çevirir; API görseli JSON içinde böyle gönderir. Metin üçte bir
  büyür, geri çevirince tek bayt kaybolmaz. Şifreleme değildir.
- **Desen.** İstek → durum kodu → base64 metni → bayt → dosya. Düzenleme de aynı.
- **Dosya adı.** Ne zaman (`datetime`), hangi yönerge (yönergenin başı), hangi tohum. Klasör `pathlib`
  ile; yazmadan önce `exists()`.
- **İki tür başarısızlık.** Sunucu "olmaz" derse durum kodu; cevap hiç gelmezse `try` / `except`.
- **Kullanıcıya açmak.** `input` ile yönerge kullanıcıdan gelir; fonksiyonlar (`ciz`, `kaydet`) birer iş yapar.

## Bu konunun tek cümlesi

> Görsel bir ikili dosyadır: base64 metni olarak gelir, baytlara çevrilir, `"wb"` ile kendini anlatan
> bir ada yazılır; hata olunca program çökmez, ne olduğunu söyler.

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **Bayt (byte)** | 0 ile 255 arasında bir sayı; her dosya bayt dizisidir |
| **İkili dosya (binary)** | Baytları harflere karşılık gelmeyen dosya: görsel, ses, PDF |
| **`"rb"` / `"wb"`** | Bir dosyayı ikili okumak / ikili yazmak için açma kipleri |
| **base64** | Baytları harf, rakam, `+` ve `/` ile yazan kodlama; görseli metin içinde taşımak için |
| **`b64encode` / `b64decode`** | Baytları base64 metnine çevirmek / geri çevirmek |
| **`Path` (pathlib)** | Dosya ve klasör yollarıyla çalışan araç; `klasor / ad` ile yol kurulur |
| **`mkdir(exist_ok=True)`** | Klasör oluşturmak; zaten varsa hata vermemek |
| **`exists()`** | Bir dosya ya da klasörün var olup olmadığını söyler |
| **`datetime.now()` / `strftime`** | Şu anki tarih ve saat / onu istenen biçimde yazmak |
| **`None`** | Python'da "hiçbir şey"; başarısız bir fonksiyonun döndürdüğü değer |
| **`try` / `except`** | "Dene; şu hata çıkarsa çökme, şunu yap" |
| **`input`** | Kullanıcıdan metin almak |
| **Form gönderimi (multipart)** | Yazı alanları ile dosyayı birlikte göndermek; `data=` ve `files=` |

## Ödev

`odevler/odev8.md` (puansız): kendi seçtiğin bir konuda 5 yönerge × 2 tohum = 10 görsel, düzenli
adlandırmayla ayrı bir `odev8/` klasörüne; hiçbir dosya üzerine yazılmasın. İki cümle: aynı
yönergenin iki tohumu arasındaki fark neydi?

## Sonraki konu

**Konu 9 — Ölçek: toplu üretim.** Bugün tek tek ürettik. Konu 9'da bir yönerge şablonu ve
değişken listeleriyle bütün kombinasyonları tek seferde üreteceğiz, sonuçları bir kontak sayfasında
toplayacağız. Bugünkü hata yakalama ve dosya adı kuralları orada gerçek ihtiyaca dönüşecek.

---

## Kendini dene — cevaplar

1. Önce dosyanın ikili mi metin mi olduğuna bak: `.pdf` ikili, `"rb"`. `.csv` metin, `"r"` (ve `encoding="utf-8"`).
2. Yaklaşık 4 MB: base64 metni üçte bir büyür (her 3 bayt 4 karakter).
3. Yıl-ay-gün sırasıyla yazılınca dosya adına göre sıralama, tarih sırasıyla aynı olur. Gün-ay-yıl
   sırasında 01-11-2026, 19-10-2026'dan önce sıralanır.
4. Aynı adla ikinci kez kaydedince önceki görsel **sessizce** silinir. Çoğu zaman ancak eski görseli
   aradığında fark edersin; o zaman geri getirmek mümkün olmaz.
5. Sunucu 401 döndürür; yanıtta `result` boş (`None`) gelir. `sonuc["image"]` satırında
   `TypeError: 'NoneType' object is not subscriptable` görür. Bu mesaj asıl sebebi (yanlış anahtar)
   söylemez; hata başka bir satırda, başka bir adla çıkar. Durum kodu kontrolü bu yüzden var.
6. `except:` her hatayı sessizce geçiştirir: yazım hatalarını, yanlış değişken adlarını bile. Program
   "internet yok" der ama asıl sorun başka bir yerdedir. Hatayı adıyla yakalayınca yalnızca beklediğin
   durumu karşılarsın.
7. Dosya adında tarih, yönergenin başı ve tohum var. Yönergenin tamamını günlükten bulup aynı tohumla,
   yalnızca renk kısmını değiştirerek üretirsin; çoğu zaman benzer bir kompozisyon alırsın (yönerge
   değiştiği için ve model sürümü değişmiş olabileceği için aynısı garanti değil).
