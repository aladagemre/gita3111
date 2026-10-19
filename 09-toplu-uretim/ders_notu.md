# Konu 9 — Ölçek: Toplu Üretim

Bu not konunun özetidir; derste çalıştırdığımız `ders.ipynb` defteriyle **aynı sırada**
ilerler: Isınma, sonra Adım 1–7 ve kısa bir Bonus. Derste kaçırdığın bir yer olursa
buradan oku, sonra defterde o adımın hücrelerini çalıştır. Nottaki kod blokları
defterdeki hücrelerin birebir aynısı.

**Konu 8'de:** görselleri tek tek ürettik, dosyaya yazdık, hataları yakaladık.
**Bu konuda:** aynı `ciz` fonksiyonuyla bir görsel **ızgarası** üretiyoruz. "Neden kod öğreniyorum?"
sorusunun cevabı bu konu:

> Bir şablon ve iki liste: stiller × renkler, tek hücre. Önce hesap, sonra küçük bir deneme; sınır koyarak,
> kaldığı yerden devam ederek, her şeyi kayda geçirerek; sonunda hepsi tek bir kontak sayfasında.

**Konunun sonunda elinde:** `izgara/` klasöründe 12 görsel, hepsini gösteren bir kontak sayfası
(`kontak_sayfasi.png`) ve her görselin nasıl üretildiğini kaydeden bir günlük (`uretim_gunlugu.json`).

**Kurulum:** yeni kütüphane yok. `git pull` ile konu klasörü geldikten sonra `gita3111` klasöründe
bir kez `uv sync` çalıştır. `json` ve `time` Python'un içinde geliyor.

**Anahtar:** Isınma, Adım 1 ve Adım 2 anahtarsız. Adım 3'ten sonrası `anahtar.txt` ister (Konu 2'deki
dosya, `gita3111` klasöründe). Defterin tamamı 12 görsel (Bonus ile en fazla 17) üretir ve 13 kez
görsel anlayan bir modele soru sorar; ücretsiz günlük kotanın küçük bir kısmı.

> **Bu nottaki çıktılar hakkında.** Isınma, Adım 1 ve 2'nin çıktıları her bilgisayarda aynıdır. Görseller
> ve modelin cevapları gerçek modelden gelir; senin ekranında farklı olur.

---

## Isınma: kaç kombinasyon?

Bir kafe afişi için üç stil ve dört renk paleti deneyeceğiz. Her stil her renkle bir kez: **kombinasyon**.

```python
stiller = ["suluboya", "vektor", "linol"]
renkler = ["adacayi", "gece", "pastel", "toprak"]

for stil in stiller:
    for renk in renkler:
        print(stil, renk)
```

Çıktı: 12 satır (`suluboya adacayi`, `suluboya gece`, ... `linol toprak`).

- **İç içe döngü:** dıştaki döngü bir stil seçer; içteki döngü o stil için bütün renkleri gezer. Sonra
  dıştaki döngü bir sonraki stile geçer. Her stil dört kez, her renk üç kez görünür.
- `print` satırı **iki girinti** içeride: bir girinti `for stil`'in, ikincisi `for renk`'in içinde olduğunu
  gösterir. Girinti kayarsa ya hata alırsın ya da bazı kombinasyonlar sessizce kaybolur (bkz. alıştırma).

Satırları tek tek saymak yerine çarpabiliriz:

```python
print(len(stiller) * len(renkler))
```

Çıktı: `12`. 5 stil ve 6 renk: 5 × 6 = 30. Bir renk eklersen 3 × 5 = 15; üstüne iki stil daha eklersen 5 × 5 = 25. Liste büyüdükçe görsel
sayısı **çarpılarak** büyür; kota da öyle.

---

## Adım 1 — Şablon ve kartlar

Dosya adı için kısa ve Türkçe karaktersiz adlar (`suluboya`) kullanıyoruz; modele ise İngilizce açıklamalar
(`watercolor illustration`) gidecek. İkisini **sözlükte** eşliyoruz (Konu 1):

```python
ozne = "a ceramic coffee cup on a wooden desk next to an open notebook, soft morning light"
brif = "sessiz bir çalışma kafesi için afiş"

stil_yonergeleri = {
    "suluboya": "watercolor illustration",
    "vektor": "flat vector poster",
    "linol": "linocut print",
}
renk_yonergeleri = {
    "adacayi": "sage green and beige palette",
    "gece": "deep navy and warm amber palette",
    "pastel": "soft pastel palette",
    "toprak": "terracotta and olive palette",
}
print(stil_yonergeleri["linol"])
```

Çıktı: `linocut print`.

- Sözlüğün anahtarı kısa ad, değeri yönerge parçası. `stil_yonergeleri["linol"]` → `"linocut print"`.
- `stiller` ve `renkler` Isınma'daki listeler; sözlükler onların yanında duruyor.
- `ozne` bütün görsellerde aynı: şablonun sabit kısmı. `brif` kendi notumuz; günlüğe yazılacak.

Her kombinasyonun bütün bilgisini bir **kart** içinde tutacağız: bir sözlük. Önce tek bir kartı elle yazıyoruz:

```python
kart = {
    "stil": "suluboya",
    "renk": "gece",
    "dosya": "suluboya_gece.jpg",
    "yonerge": ozne + ", watercolor illustration, deep navy and warm amber palette",
    "tohum": 42,
}
print(kart["dosya"])
```

Çıktı: `suluboya_gece.jpg`. Kartın içinde stil, renk, dosya adı, yönergenin tamamı ve tohum var.

Şimdi aynı kartı her kombinasyon için döngüyle kuruyoruz:

```python
kartlar = []
for stil in stiller:
    for renk in renkler:
        stil_metni = stil_yonergeleri[stil]
        renk_metni = renk_yonergeleri[renk]
        kart = {
            "stil": stil,
            "renk": renk,
            "dosya": f"{stil}_{renk}.jpg",
            "yonerge": f"{ozne}, {stil_metni}, {renk_metni}",
            "tohum": 42,
            "model": "flux-1-schnell",
            "brif": brif,
            "durum": "denenmedi",
        }
        kartlar.append(kart)

print(len(kartlar))
```

Çıktı: `12`.

- Önce iki yönerge parçasını sözlükten okuyup ayrı değişkenlere alıyoruz (`stil_metni`, `renk_metni`); f-string'in
  içinde yalnızca düz adlar kalıyor.
- Kartta üç alan daha var: `"model"`, `"brif"` ve `"durum"`. Kart hem üretimi yönetecek hem günlük olacak (Adım 5).
  `"durum": "denenmedi"` başlangıç değeri; üretim sırasında `"uretildi"` ya da `"olmadi"` olur.
- Listeleri ya da sözlükleri değiştirirsen bu hücreyi yeniden çalıştır; yoksa kartlar eski kalır.
- `kartlar.append(kart)`: kartı listeye ekler. Sonunda bir liste, içinde 12 sözlük.

```python
ilk_kart = kartlar[0]
print(ilk_kart["dosya"])
print(ilk_kart["yonerge"])
```

Çıktı:

```
suluboya_adacayi.jpg
a ceramic coffee cup on a wooden desk next to an open notebook, soft morning light, watercolor illustration, sage green and beige palette
```

Bu bir **şablon**: özne ve tohum sabit, stil ve renk düzenli olarak değişiyor. Konu 7'deki kontrollü deneyin
iki eksenli hâli.

---

## Adım 2 — Kota ve güvenlik sınırı

Cloudflare kotayı **neuron** denen bir birimle sayar; günde 10.000 neuron ücretsiz. Bir görsel (1024 × 1024,
4 adım) yaklaşık 58 neuron tutar: Cloudflare 1024'lük görseli 512 × 512'lik 4 kare olarak sayar; 4 kare × 4,8 +
4 adım × 9,6. Yani günde kabaca 170 görsel.

```python
MAKS_URETIM = 12
GORSEL_BASI_NEURON = 58

print("Kart sayısı:", len(kartlar))
print("Tahmini kota:", len(kartlar) * GORSEL_BASI_NEURON, "/ 10000 neuron")
if len(kartlar) > MAKS_URETIM:
    print("Dikkat: kart sayısı sınırı aşıyor; bir çalıştırmada", MAKS_URETIM, "karttan sonra durulacak")
```

Çıktı:

```
Kart sayısı: 12
Tahmini kota: 696 / 10000 neuron
```

- `MAKS_URETIM` bir çalıştırmada en fazla kaç görsel üretileceği. Büyük harfle yazılmış bir değişken:
  Python'da "bunu değiştirme, sabit" demenin geleneği.
- Kart sayısı sınırı aşarsa uyarı yazar; Adım 4'teki döngü sınırda durur.

---

## Adım 3 — Araç ve sabırlı çizim

```python
import time
import requests
from pathlib import Path
from uretim import ciz, gorsele_sor
```

- `uretim.py` bu klasördeki yardımcı dosya. İçindeki `ciz`, Konu 8'de yazdığın fonksiyonla aynı işi yapar:
  yönerge ve tohum alır, görselin baytlarını verir; başarısızsa `None`. Anahtarı `../anahtar.txt`'den kendisi okur. `gorsele_sor`'u Adım 7'de kullanacağız.
- `time` beklemek için. `requests`'i istek göndermek için değil, hata adını yazabilmek için alıyoruz.
- `uretim.py` anahtarı bir kez, bu hücre ilk çalıştığında okur. `anahtar.txt`'yi sonradan düzeltirsen çekirdeği
  yeniden başlat (**Restart**) ve hücreleri baştan çalıştır.

Toplu üretimde bir istek bağlanamazsa bütün iş durmamalı. Bir adım daha: **bekleyip yeniden denemek**.

```python
def sabirli_ciz(yonerge, tohum):
    for deneme in [1, 2, 3]:
        try:
            resim = ciz(yonerge, tohum)
        except requests.exceptions.RequestException:
            print("Bağlanamadım ya da cevap gelmedi")
            resim = None
        if resim is not None:
            return resim
        if deneme < 3:
            print("Deneme", deneme, "olmadı, 5 saniye bekliyorum")
            time.sleep(5)
    return None
```

- `time.sleep(5)`: programı 5 saniye bekletir. Sunucu kısa süreli meşgulse ya da çok hızlı istek
  gönderdiysek (429) bu çoğu zaman yeter.
- `try` / `except`: Konu 8'deki gibi; bu kez `requests.exceptions.RequestException` yakalıyoruz: `requests`'in bütün
  hatalarının ortak adı. Bağlantı kopması (`ConnectionError`) da, cevabın zamanında gelmemesi (`Timeout`) da bununla
  yakalanır. (`uretim.py`'deki istekler 2 dakikada cevap gelmezse bırakılıyor.)
- `return resim` fonksiyonu orada bitirir: başarılı olunca kalan denemeler yapılmaz.
- En fazla üç deneme; son denemeden sonra beklemeye gerek yok (`if deneme < 3`). Üçü de olmazsa `None` döner.
  Yani başarısız her kart 3 istek ve 10 saniye bekleme demek.
- Günlük kota bittiyse beklemek işe yaramaz ve bu kod bunu ayırt etmiyor. Üst üste `429` görürsen hücreyi durdur
  (üstteki menüden **Interrupt**); kota yenilenince kaldığın yerden devam edersin.

---

## Adım 4 — Üretim döngüsü: önce küçük bir deneme

Önce görsellerin klasörü:

```python
klasor = Path("izgara")
klasor.mkdir(exist_ok=True)
```

```python
def toplu_uret(liste, sinir):
    denenen = 0
    for kart in liste:
        yol = klasor / kart["dosya"]
        if yol.exists():
            kart["durum"] = "uretildi"
            print("Zaten var, atlıyorum:", yol)
            continue
        if denenen >= sinir:
            print("Sınıra geldim, duruyorum")
            break
        resim = sabirli_ciz(kart["yonerge"], kart["tohum"])
        denenen = denenen + 1
        if resim is None:
            kart["durum"] = "olmadi"
            print("Olmadı, atlıyorum:", yol)
            continue
        with open(yol, "wb") as dosya:
            dosya.write(resim)
        kart["durum"] = "uretildi"
        print("Kaydedildi:", yol)
    print("Bu çalıştırmada denenen:", denenen)
```

- Döngü bir fonksiyonda: `toplu_uret(liste, sinir)` bir kart listesi ve bir sınır alır. `sinir` bu çalıştırmada en
  fazla kaç görsel deneneceği.
- `klasor / kart["dosya"]`: Konu 8'deki gibi klasör ve dosya adını birleştirir.
- **Zaten varsa** atla: `continue` bu kartı bırakır, döngünün başına döner, sıradakine geçer. Dosya varsa daha önce
  üretilmiştir; o yüzden durumu `uretildi`.
- **Sınıra geldiysen** dur: `break` döngüyü tamamen bitirir (Konu 8).
- Değilse üret ve kaydet. Kartın içine sonucunu yaz: `kart["durum"] = "uretildi"` ya da `"olmadi"`. Sözlüğe
  yeni bir anahtar böyle eklenir.
- `denenen` üretmeyi denediğimiz kartları sayar; atlanan kartlar sayılmaz. Sınır bu sayaca bakar.
- Dosya adında **tarih yok** (Konu 8'deki `kaydet`'ten farkı): aynı kart her zaman aynı adı alır. Bu sayede "zaten
  var mı?" sorusu bir **kaldığı yerden devam** düğmesine dönüşür. Bu yüzden Konu 8'in `kaydet`'ini kullanmıyoruz;
  o, her kayıtta yeni (tarihli) bir ad üretiyordu.

Önce küçük bir deneme:

```python
toplu_uret(kartlar, 3)
```

Üç görsel gelir ve `Sınıra geldim, duruyorum` yazılır. Beğendiysen asıl sınırla devam:

```python
toplu_uret(kartlar, MAKS_URETIM)
```

İlk üç kart **atlanır**, kalan dokuzu üretilir: program kaldığı yerden devam etti. (İlk denemede bir kart olmadıysa
o da yeniden denenir: dosyası yok.) Bir dosyayı silip yeniden
çalıştırırsan yalnızca o kart üretilir. Kota biterse ya da internet koparsa, sonra aynı hücreyi çalıştırmak yeter.

| Konu 8'in dosya adı | Konu 9'un dosya adı |
|---|---|
| `2026-10-19_18-57-25_a-red-bicycle-leanin_7.jpg` | `suluboya_adacayi.jpg` |
| Her kayıt yeni bir ad: hiçbir şey üzerine yazılmaz | Aynı kart aynı ad: zaten varsa atlanır, kaldığı yerden devam edilir |
| Tek tek üretim için iyi | Toplu üretim için iyi |

**Dikkat:** adda olmayan bir şeyi (ör. `ozne`'yi ya da tohumu) değiştirip yeniden çalıştırırsan program bunun yeni
bir iş olduğunu bilemez ve eski görselleri atlar. Öyle bir değişiklikte yeni bir klasör aç.

---

## Adım 5 — Üretim günlüğü: kartları JSON'a yaz

Kartlar zaten günlüğün kendisi: her birinde stil, renk, dosya adı, yönergenin tamamı, tohum, model, brif ve sonuç
(`durum`) var. Hepsini bir **JSON** dosyasına yazıyoruz:

```python
import json

with open("uretim_gunlugu.json", "w", encoding="utf-8") as dosya:
    json.dump(kartlar, dosya, ensure_ascii=False, indent=2)

print("Günlük yazıldı:", len(kartlar), "kart")
```

- `json.dump(kartlar, dosya, ...)`: listeyi dosyaya JSON olarak yazar. Önce yazılacak şey, sonra dosya.
- `ensure_ascii=False`: Türkçe harfler (`brif` alanındaki ç ve ş) `\u00e7` gibi kodlara dönüşmesin, olduğu gibi yazılsın.
- `indent=2`: her kart ayrı satırlarda, okunur biçimde.

JSON, Konu 2'de API'nin cevabındaki biçim: sözlükler ve listeler, metin olarak. Program onu geri okuyabilir:

```python
with open("uretim_gunlugu.json", encoding="utf-8") as dosya:
    okunan = json.load(dosya)

print(len(okunan))
print(okunan[5]["yonerge"])
```

- `json.load` dosyayı yeniden listeye çevirir. `okunan[5]["yonerge"]`: altıncı kartın yönergesi.
- Bir müşteri aylar sonra "altıncı görselin aynısı" derse yönergesi ve tohumu elinde.

---

## Adım 6 — Kontak sayfası: bütün ızgara tek sayfada

Fotoğrafçılar filmdeki bütün kareleri tek kâğıda basıp en iyisini seçerdi: **kontak sayfası**. Bizimki bir
ızgara: satır sayısı stil sayısı, sütun sayısı renk sayısı.

```python
import matplotlib.pyplot as plt

satir = len(stiller)
sutun = len(renkler)

plt.figure(figsize=(12, 9))
sira = 1
for kart in kartlar:
    yol = klasor / kart["dosya"]
    plt.subplot(satir, sutun, sira)
    if yol.exists():
        plt.imshow(plt.imread(yol))
    plt.title(kart["stil"] + " / " + kart["renk"], fontsize=9)
    plt.axis("off")
    sira = sira + 1

plt.savefig("kontak_sayfasi.png", bbox_inches="tight")
plt.show()
```

- Konu 6'daki `subplot` döngüsü, bu kez birden çok satırla: `plt.subplot(satir, sutun, sira)`.
- `subplot` kutuları soldan sağa doldurur, satır bitince alttakine geçer. Kartlar stil stil sıralı olduğu için her
  satır bir stil, her sütun bir renk olur.
- Satır ve sütun sayısı listelerden geliyor: stil ya da renk ekleyince ızgara kendini ayarlar.
- `plt.figure(figsize=(12, 9))`: sayfanın boyutu (genişlik, yükseklik; inç).
- `plt.imread` görseli dosyadan okur (Konu 8). Üretilemeyen kartın kutusu boş kalır.
- `plt.savefig`: sayfayı dosyaya kaydeder; `bbox_inches="tight"` kenardaki boşluğu kırpar.

Sayfaya tasarımcı gözüyle bak: hangi stil brife uyuyor? Hangi renk? Kartlar kontrollü kurulduğu için bir satırın
hepsi kötüyse sorun stilde, bir sütunun hepsi kötüyse renkte. Kazananını dosya adıyla yaz:

```python
benim_secimim = "suluboya_adacayi.jpg"
```

---

## Adım 7 — Modele kendi çıktısını okutmak

Ölçek büyüyünce ilk elemeyi bir **görsel anlayan** modele yaptırabiliriz: metni ve görseli birlikte anlayan,
**çok kipli** (multimodal) bir model (Gemma). `gorsele_sor(yol, soru)` görseli ve soruyu ona gönderir, cevabı metin
olarak verir.

```python
ilk_yol = klasor / ilk_kart["dosya"]
cevap = gorsele_sor(ilk_yol, "Describe this image in one short sentence.")
print(cevap)
```

- Görsel yine base64 metni olarak gidiyor; bu kez Konu 8'in **tersi** yönde: biz görseli base64'e çeviriyoruz,
  model geri çeviriyor.
- Soruyu İngilizce soruyoruz (Konu 7: modeller İngilizcede daha iyi).

```python
brif_ingilizce = "a poster for a quiet cafe where people come to study and work"
soru = f"On a scale of 1 to 5, how well does this image fit this brief: {brif_ingilizce}? Answer with only the number."

for kart in kartlar:
    yol = klasor / kart["dosya"]
    if yol.exists():
        kart["model_puani"] = gorsele_sor(yol, soru)
        print(kart["dosya"], kart["model_puani"])

print("Benim seçimim:", benim_secimim)
```

- `brif_ingilizce` ayrı bir değişkende: ödevde yalnızca bu satırı değiştireceksin.
- Her kartın içine `model_puani` diye yeni bir alan ekliyoruz.
- Model bazen yalnızca bir sayı, bazen bir cümle yazar; o yüzden cevabı olduğu gibi (metin) saklıyoruz.
- 12 istek birkaç dakika sürer. Sonunda kendi seçimin de yazılır: karşılaştır.

**Tartış:** modelin en yüksek puan verdikleri arasında senin seçimin var mı? Model brifteki kelimeleri görselde
neyle eşliyor olabilir? Model bir **ilk eleme** aracı, karar verici değil: onun da bir zevki, bir yanlılığı var
(Konu 3). Kararı sen verirsin; model yüz görseli ona indirmene yardım eder.

Günlüğü puanlarla birlikte yeniden yazıyoruz:

```python
with open("uretim_gunlugu.json", "w", encoding="utf-8") as dosya:
    json.dump(kartlar, dosya, ensure_ascii=False, indent=2)

print("Günlük güncellendi")
```

---

## Bonus

**1. Tohum ekseni.** Adım 6'da seçtiğin kazananı (`benim_secimim`) üç farklı tohumla üret:

```python
for kart in kartlar:
    if kart["dosya"] == benim_secimim:
        kazanan = kart

kazanan_stil = kazanan["stil"]
kazanan_renk = kazanan["renk"]

for tohum in [1, 2, 3]:
    yol = klasor / f"{kazanan_stil}_{kazanan_renk}_{tohum}.jpg"
    if not yol.exists():
        resim = sabirli_ciz(kazanan["yonerge"], tohum)
        if resim is not None:
            with open(yol, "wb") as dosya:
                dosya.write(resim)
    print(yol)
```

- İlk döngü kazananın kartını listede bulur: dosya adı `benim_secimim`'e eşit olan kart.
- Dosya adına stil, renk ve tohum yazılıyor: her tohum ayrı bir dosya; kazananı değiştirirsen yeni dosyalar oluşur.

**2. Sınır gerçekten çalışıyor mu?** Isınma'daki `renkler` listesine ve Adım 1'deki `renk_yonergeleri` sözlüğüne bir
palet ekle (ör. `"mono"` ve `"black and white palette"`). Isınma'yı ve Adım 1'in hücrelerini yeniden çalıştır, sonra:

```python
toplu_uret(kartlar, 2)
```

Üç yeni kart var (her stil için bir); sınır 2 olduğu için ikisi üretilir ve `Sınıra geldim` yazılır. Aynı hücreyi bir
kez daha çalıştırırsan kalan bir kart üretilir. Kontak sayfasını yeniden çizersen ızgara 3 × 5 olur.

---

## Defterin bölümleri

| Adım | Ne yaptık | Elimizde ne oluştu | Anahtar |
|---|---|---|---|
| Isınma | İç içe döngüyle kombinasyonları saydık | `stiller`, `renkler` | gerekmez |
| 1 | Şablon: yönerge sözlükleri ve kartlar | `stil_yonergeleri`, `renk_yonergeleri`, `kartlar` | gerekmez |
| 2 | Kota hesabı ve sınır | `MAKS_URETIM` | gerekmez |
| 3 | Araç; bekleyip yeniden deneyen çizim | `ciz`, `gorsele_sor`, `sabirli_ciz` | gerekir |
| 4 | Klasör; üretim döngüsü: önce 3, sonra kalanı | `klasor`, `toplu_uret`, `izgara/` (12 görsel) | gerekir |
| 5 | Üretim günlüğü: yaz ve geri oku | `uretim_gunlugu.json` | gerekmez |
| 6 | Kontak sayfası; kendi seçimin | `kontak_sayfasi.png`, `benim_secimim` | gerekmez |
| 7 | Modele görselleri okuttuk, puanlattık | `model_puani` alanları | gerekir |
| Bonus | Tohum ekseni; sınırın çalıştığını görmek | `izgara/kazanan_*.jpg` | gerekir |

Derste kendi başına çalışacağın defter: `alistirma.ipynb`. Önce aynı klasörde yeni bir adla kopyala,
kopyada çalış. **Anahtar istemez ve görsel üretmez:** listeler, sözlükler, döngüler ve JSON. İki bölümü var:

- **Bozuk kodlar:** beş kısa hücre, birbirinden bağımsız. Üçü hata mesajı veriyor, ikisi sessizce yanlış sonuç yazıyor.
- **Kendi başına:** `BOSLUK` yazan yerleri doldurduğun altı soru ve bir ek soru (kart listesini kendin kurmak).

---

## Sık karşılaşılan hatalar ve mesajlarını okumak

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `IndentationError: expected an indented block after 'for' statement ...` | İçteki döngünün satırı yeterince içeride değil | İç döngünün satırları iki girinti içeride olmalı |
| Kombinasyonların yalnızca bir kısmı yazılıyor | `print` (ya da `append`) iç döngünün dışına kaymış | Satırı iç döngünün hizasına al |
| `KeyError: 'suluboya '` ya da `KeyError: 2` | Sözlükte olmayan bir anahtar (fazla boşluk, sıra numarası) | Anahtar adını birebir yaz; kartlar sözlük: `kart["dosya"]` |
| `KeyError: 'mono'` (Adım 1) | Listeye eklenen kısa adın yönerge sözlüğünde karşılığı yok | Her kısa adı sözlüğe de ekle, sonra kart hücresini yeniden çalıştır |
| Kontak sayfasında kutular kaymış ya da `ValueError: num must be an integer with 1 <= num <= ...` | Listeler değişti ama kartlar yeniden kurulmadı | Isınma'dan itibaren sırayla yeniden çalıştır |
| `ModuleNotFoundError: No module named 'uretim'` | Defterin kopyası konu klasörünün dışında | Kopya `uretim.py`'nin yanında, `09-toplu-uretim` klasöründe olmalı |
| `FileNotFoundError: ... '../anahtar.txt'` (Adım 3) | Anahtar dosyası yok ya da yanlış yerde | `gita3111` klasöründe durmalı; sonra Adım 3'ün ilk hücresini yeniden çalıştır |
| `KeyError: 'ACCOUNT_ID'` (Adım 3) | `anahtar.txt`'de `=` yerine `:` ya da satır eksik | İki satır `AD = değer` biçiminde olmalı |
| `NameError: name 'ciz' is not defined` ya da `'Path'` | Adım 3'ün ilk hücresi hata verdi ya da çalıştırılmadı | Önce o hücredeki hatayı düzelt |
| `İstek başarısız, durum kodu: 401` (her kartta üç kez) | Anahtar yanlış | `anahtar.txt`'yi düzelt, çekirdeği yeniden başlat (**Restart**), baştan çalıştır: `uretim.py` anahtarı yalnızca ilk okumada alır |
| `Bağlanamadım ya da cevap gelmedi` | İnternet yok ya da sunucu 2 dakikada cevap vermedi | İnternete bak; sonra aynı hücre kaldığı yerden devam eder |
| `İstek başarısız, durum kodu: 429` ve `Deneme ... olmadı` | Çok hızlı istek ya da günlük kota doldu | Bekle; üst üste geliyorsa hücreyi durdur. Kota 03:00'te (Türkiye saati) yenilenir; sonra aynı hücreyi çalıştır, kaldığı yerden devam eder |
| Hücre uzun süre bitmiyor | `sabirli_ciz` bekliyor (başarısız her denemeden sonra 5 saniye) ya da 12 istek sürüyor | Bekle; mesajlara bak |
| `NameError: name 'sabirli_ciz' is not defined` | Adım 3'ün fonksiyon hücresi çalıştırılmadı | Adım 3'ü çalıştır |
| `NameError: name 'toplu_uret' is not defined` | Adım 4'ün fonksiyon hücresi çalıştırılmadı | O hücreyi çalıştır |
| `NameError: name 'klasor' is not defined` (Adım 6 ya da 7) | Adım 4'ün ilk hücresi çalıştırılmadı | Adım 4'ü çalıştır |
| Hiçbir şey üretilmiyor, hepsi `Zaten var` | Görseller önceki bir çalıştırmadan var | Doğru davranış. `ozne`'yi değiştirdiysen yeni bir klasör aç; yoksa günlük de eski görseli yeni yönergeyle kaydeder |
| `TypeError: Object of type TextIOWrapper is not JSON serializable` | `json.dump`'a önce dosya, sonra liste verildi | Önce yazılacak şey: `json.dump(kartlar, dosya)` |
| Günlükte `\u00e7` gibi kodlar | `ensure_ascii=False` yazılmamış | Ekle |
| Kontak sayfasında boş kutular | O kartlar üretilemedi (sınır, kota ya da hata) | `toplu_uret`'i yeniden çalıştır; yalnızca eksikler üretilir |
| `model_puani` `None` | Görsel anlayan modelin isteği başarısız | Üstteki `İstek başarısız, durum kodu` ya da `Bağlanamadım` satırına bak |
| `FileNotFoundError: ... 'izgara/suluboya_adacayi.jpg'` (Adım 7) | İlk görsel yok (Adım 4 çalışmadı ya da ilk kart olmadı) | Önce `toplu_uret`'i yeniden çalıştır |
| `NameError: name 'benim_secimim' is not defined` | Adım 6'nın son hücresi atlandı | O hücreyi çalıştır (kendi kazananının dosya adıyla) |
| Bonus 1'de `NameError: name 'kazanan' is not defined` | `benim_secimim`'deki ad hiçbir kartın dosya adına uymuyor | Adı kontak sayfasındaki gibi, `.jpg` ile birlikte yaz |

---

## Kendini dene

Cevaplar notun en sonunda. Önce kendin düşün.

1. 4 stil, 5 renk ve 3 tohum kaç görsel eder? Günlük ücretsiz kotanın ne kadarı?
2. Bir arkadaşın Konu 8'deki tarihli dosya adını (`2026-10-19_..._7.jpg`) Adım 4'te kullandı. `toplu_uret`'i
   ikinci kez çalıştırınca ne olur?
3. `if denenen >= sinir:` kontrolü neden görseli üretmeden önce yapılıyor?
4. `sabirli_ciz`'deki `time.sleep(5)` satırını silersen 429 hatasında ne değişir?
5. Kontak sayfasında `linol` satırının dördü de kötü, `pastel` sütununda yalnızca biri kötü. Ne söyleyebilirsin?
6. Model bir görsele 5 puan verdi, sen beğenmedin. Hangisine güvenirsin? Model neden yanılmış olabilir?
7. Üretim günlüğünü neden JSON'a yazdık; bir metin dosyasına (`print` gibi) yazsak ne kaybederdik?

---

## Bu konuda öğrendiklerin

- **Kombinasyon.** İç içe döngü her stili her renkle eşler; sayı çarpılarak büyür.
- **Şablon.** Kısa adlar (dosya için) ile uzun yönerge parçaları (model için) sözlükte eşlenir; her
  kombinasyon bir kart (sözlük) olur.
- **Sınır ve kota.** Döngüden önce hesap; önce küçük bir deneme; sınırla kazara kota tüketimini önlemek.
- **Sağlamlık.** Bekleyip yeniden denemek (`time.sleep`); tarihsiz, kararlı dosya adlarıyla kaldığı yerden devam.
- **Günlük.** Kartlar JSON'a yazılır ve geri okunur: her görselin nasıl üretildiği ve durumu (`uretildi`, `olmadi`,
  `denenmedi`) kayıtta.
- **Kontak sayfası.** Bütün kombinasyonları tek sayfada görmek; satırlar ve sütunlar kontrollü deneyin iki ekseni.
- **Çok kipli eleme.** Görsel anlayan bir model ilk elemeyi yapar; kararı tasarımcı verir.

## Bu konunun tek cümlesi

> Bir şablon ve listelerle bir görsel ızgarasını tek seferde üretirsin; sınır koyar, kaldığı yerden devam eder,
> her şeyi kayda geçirir ve hepsini bir kontak sayfasında yan yana değerlendirirsin.

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **Kombinasyon** | İki ya da daha çok listenin her elemanının birbiriyle eşleşmesi: 3 × 4 = 12 |
| **İç içe döngü** | Bir döngünün içinde başka bir döngü; içteki her tur için baştan sona döner |
| **Şablon** | Sabit kısmı ve değişen boşlukları olan yönerge |
| **Kart** | Bir kombinasyonun bütün bilgileri: stil, renk, dosya adı, yönerge, tohum (bir sözlük) |
| **Izgara** | Satırları bir değişken, sütunları öbür değişken olan görsel düzeni |
| **`continue` / `break`** | Döngüde sıradakine geç / döngüyü bitir |
| **`time.sleep(5)`** | Programı 5 saniye bekletmek |
| **Sabit (`MAKS_URETIM`)** | Değişmemesi gereken değer; büyük harfle yazılır |
| **Neuron** | Cloudflare'in kota birimi; günde 10.000 ücretsiz, bir görsel ~58 |
| **Kaldığı yerden devam** | Var olan çıktıları atlayıp yalnızca eksikleri üretmek |
| **`json.dump` / `json.load`** | Python listelerini ve sözlüklerini JSON dosyasına yazmak / dosyadan okumak |
| **Kontak sayfası** | Bütün kombinasyonları tek görselde ızgara hâlinde gösteren sayfa |
| **Çok kipli (multimodal)** | Metni ve görseli birlikte anlayan model |

## Ödev

`odevler/odev9.md` (puansız): kendi konunda bir ızgara üret (en az 2 stil × 3 renk, en fazla 12 görsel);
kontak sayfasını ve üretim günlüğünü getir. Hangi kombinasyon kazandı, neden? Model de aynısını mı seçti?
Görsellerini sakla: Konu 10'da birini videoya çevireceğiz.

## Sonraki konu

**Konu 10 — Video üretimi.** Bugün bir şablonla bir ızgara ürettik. Konu 10'da hareket ekliyoruz: bir görseli ya
da yönergeyi kısa bir videoya çevirmek. Video pahalıdır ve sonucu hemen gelmez; bugünkü kota hesabı, sınır ve
"kaldığı yerden devam" alışkanlığı orada daha da önemli.

---

## Kendini dene — cevaplar

1. 4 × 5 × 3 = 60 görsel; 60 × 58 ≈ 3.480 neuron, günlük kotanın üçte birinden fazla. Sınırsız ve tarihli adlarla
   aynı döngüyü yanlışlıkla iki kez çalıştırmak 6.960 neuron eder: kotanın yaklaşık %70'i. Sınır ve "zaten var mı?"
   bu yüzden var.
2. Her çalıştırmada tarih değiştiği için hiçbir ad "zaten var" olmaz; bütün görseller **yeniden** üretilir ve kota
   harcanır. Kaldığı yerden devam için ad kararlı (aynı kart, aynı ad) olmalı.
3. Sınır bir istek **gönderilmeden önce** bilinmeli: istek bir kez gitti mi kota harcanmıştır. Önce bakınca `sinir`
   0 bile olsa hiç istek gitmez. Ayrıca sayaç "zaten var" kontrolünden sonra olduğu için atlanan kartlar sayılmaz.
4. Bekleme olmadan üç deneme saniyeler içinde biter; çok hızlı istek gönderdiğin için (429) üçü de büyük ihtimalle
   reddedilir ve sunucuyu daha da yorarsın. Bekleme sunucuya nefes aldırır.
5. Sorun büyük ihtimalle **stilde** (linol bu brif için uygun değil), renkte değil; `pastel` sütunundaki tek kötü
   görsel o stil–renk eşleşmesine özgü. Kontrollü kurulum bu ayrımı mümkün kılıyor.
6. Kendine. Model brifteki kelimeleri görseldeki nesnelerle (fincan, defter) eşliyor olabilir; ışığı, havayı,
   markanın kimliğini senin gibi tartmaz. Model ilk eleme içindir, karar senindir.
7. JSON'u program geri okuyabilir (`json.load`, Adım 5): hangi kartın hangi yönergeyle üretildiğini, puanını,
   tohumunu bir sonraki çalıştırmada kullanabilirsin. Düz metin yalnızca insan içindir; programın onu yeniden
   ayrıştırması zor.
