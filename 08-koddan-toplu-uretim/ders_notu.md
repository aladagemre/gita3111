# Konu 8 — Koddan Görsel ve Toplu Üretim

Bu not konunun özetidir; derste çalıştırdığımız `ders.ipynb` defteriyle **aynı sırada**
ilerler: Isınma, sonra Adım 1–6 ve kısa bir Bonus. Derste kaçırdığın bir yer olursa
buradan oku, sonra defterde o adımın hücrelerini çalıştır. Nottaki kod blokları
defterdeki hücrelerin birebir aynısı.

**Konu 7'de:** görselleri hazır bir araçla (`gorsel_araci.py`) tek tek ürettik; yönergeyi ve tohumu bilerek değiştirdik.
**Bu konuda:** önce aynı işi koddan, dosyanın adını kendimiz koyarak yapıyoruz. Sonra arayüzün yapamadığına geçiyoruz:
bir görsel **ızgarası**. "Neden kod öğreniyorum?" sorusunun cevabı bu konu:

> Bir şablon ve iki liste: stiller × renkler, birkaç hücre. Önce hesap, sonra küçük bir deneme. Sınır koyar,
> kaldığı yerden devam eder, her şeyi kayda geçiririz. Sonunda hepsi tek bir kontak sayfasında.

**Konunun sonunda elinde:** `ciktilar/` klasöründe iki tek görsel; `izgara/` klasöründe 12 görsel, hepsini gösteren bir
kontak sayfası (`kontak_sayfasi.png`) ve her görselin nasıl üretildiğini kaydeden bir günlük (`uretim_gunlugu.json`).
Alıştırmada toplu üretimin döngüsünü ve kontak sayfasını kendi elinle yazacaksın.

**Kurulum:** yeni kütüphane yok. `git pull` ile konu klasörü geldikten sonra `gita3111` klasöründe
bir kez `uv sync` çalıştır. `os` ve `json` Python'un içinde geliyor.

**Anahtar:** Isınma anahtarsız. Adım 1'den sonrası `anahtar.txt` ister (Konu 2'deki dosya, `gita3111` klasöründe).
Defterin ana akışı 15 görsel üretir; Bonus ile en fazla 21 görsel ve görsel anlayan bir modele 13 soru. Hepsi ücretsiz
günlük kotanın küçük bir kısmı.

> **Bu nottaki çıktılar hakkında.** Isınma, Adım 2 ve Adım 3'ün çıktıları her bilgisayarda aynıdır. Görseller
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

Çıktı: `12`. 5 stil ve 6 renk: 5 × 6 = 30. Elimizdeki 3 × 4'e bir renk eklersen 3 × 5 = 15; üstüne iki stil daha
eklersen 5 × 5 = 25. Liste büyüdükçe görsel sayısı **çarpılarak** büyür. Arayüzde bunların her biri ayrı bir yönerge,
ayrı bir "üret" ve ayrı bir "indir" demek.

---

## Adım 1 — Aynı iş koddan: tek görsel

```python
from uretim import ciz
import matplotlib.pyplot as plt
```

- `uretim.py` bu klasördeki yardımcı dosya. Görsel üretmenin bütün ayrıntısı (isteği göndermek, cevabı çözmek,
  dosyaya yazmak) onun içinde; **içini okuman gerekmiyor**. Bize üç fonksiyon veriyor: `ciz`, `sabirli_ciz` (Adım 4)
  ve `gorsele_sor` (Bonus).
- `ciz(yonerge, tohum, yol)` görseli üretir ve `yol`a kaydeder. Başarılıysa `yol`u, olmazsa `None` ("hiçbir şey") verir.
  Klasör yoksa kendisi açar.
- `uretim.py` anahtarı `../anahtar.txt`'den bir kez, bu hücre ilk çalıştığında okur. `anahtar.txt`'yi sonradan
  düzeltirsen çekirdeği yeniden başlat (**Restart**) ve hücreleri baştan çalıştır.
- `matplotlib`'i görseli defterde göstermek için alıyoruz (Konu 6).

Yönergeyi parçalardan kuruyoruz ve ilk görseli üretiyoruz:

```python
ozne = "a ceramic coffee cup on a wooden desk next to an open notebook, soft morning light"
stil_metni = "watercolor illustration"
yonerge = ozne + ", " + stil_metni

sonuc = ciz(yonerge, 42, "ciktilar/ilk.jpg")
print(sonuc)
```

Çıktı: `ciktilar/ilk.jpg` (istek başarısızsa önce `İstek başarısız, durum kodu: ...`, sonra `None`).

- `ozne` bütün görsellerde aynı kalacak: şablonun sabit kısmı. `stil_metni` değişecek. Yönerge İngilizce (Konu 7).
- Dosyanın yolunu **sen** koyuyorsun: `ciktilar` klasörü, içinde `ilk.jpg`. Görseli VS Code'un sol panelinde
  `ciktilar` klasörünü açıp tıklayarak görebilirsin.

Defterde göstermek için:

```python
resim = plt.imread("ciktilar/ilk.jpg")
plt.imshow(resim)
plt.axis("off")
plt.show()
```

`plt.imshow` Konu 6'dan tanıdık: orada bir sayı tablosunu resim olarak çiziyordu. `plt.imread` görsel dosyasını okuyup
böyle bir sayı tablosuna çevirir; `plt.imshow` onu çizer, `plt.axis("off")` kenardaki sayıları gizler.

**Konu 7'den farkı:** Konu 7'deki `ciz` dosyaya kendisi bir sıra numarası veriyordu (`001.jpg`, `002.jpg`...).
Bugünkü `ciz` yolu senden istiyor. Bu farkın neden önemli olduğu Adım 4'te çıkıyor.

**Programı kullanıcıya açmak.** `input` (GİTA2112'den tanıdık) kullanıcıya bir soru sorar ve yazdığını metin olarak
verir. VS Code'da ekranın üstünde bir kutu açılır; yönergeni İngilizce yazıp **Enter**'a basarsın.

```python
istek = input("Yönerge (İngilizce): ")
sonuc = ciz(istek, 7, "ciktilar/benim.jpg")
print(sonuc)
```

Kodu bilmeyen biri de bu hücreyle görsel üretebilir. Kutuyu boş bırakıp Enter'a basarsan model boş yönergeyi kabul etmez:
`İstek başarısız, durum kodu: 400`.

Defterdeki tahmin sorusu: aynı yola (`ciktilar/benim.jpg`) bu kez fincanın yönergesiyle çizersek senin görseline ne olur?

```python
sonuc = ciz(yonerge, 7, "ciktilar/benim.jpg")
print(sonuc)
```

Senin görselin gider, yerinde fincan olur. Uyarı yok, geri dönüşüm kutusu yok: aynı yola yazılan dosya eskisinin
**üzerine yazılır**. Tek tek üretirken her görsele ayrı bir ad vermek senin işin. Adım 4'te bu kuralı tersinden
kullanacağız: dosya zaten varsa hiç üretme.

---

## Adım 2 — Şablon ve kartlar

Dosya adı için kısa ve Türkçe karaktersiz adlar (`suluboya`) kullanıyoruz; modele ise İngilizce açıklamalar
(`watercolor illustration`) gidecek. İkisini **sözlükte** eşliyoruz (Konu 1):

```python
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
- Bu adım ve Adım 3 istek göndermiyor.

Her kombinasyonun bütün bilgisini bir **kart** içinde tutacağız: bir sözlük. Önce tek bir kartı elle yazıyoruz:

```python
kart = {
    "stil": "suluboya",
    "renk": "gece",
    "yol": "izgara/suluboya_gece.jpg",
    "yonerge": ozne + ", watercolor illustration, deep navy and warm amber palette",
    "tohum": 42,
}
print(kart["yol"])
```

Çıktı: `izgara/suluboya_gece.jpg`. Kartın içinde stil, renk, dosyanın yolu, yönergenin tamamı ve tohum var.

Şimdi aynı kartı her kombinasyon için döngüyle kuruyoruz:

```python
klasor = "izgara/"
kartlar = []
for stil in stiller:
    for renk in renkler:
        stil_metni = stil_yonergeleri[stil]
        renk_metni = renk_yonergeleri[renk]
        kart = {
            "stil": stil,
            "renk": renk,
            "yol": klasor + stil + "_" + renk + ".jpg",
            "yonerge": ozne + ", " + stil_metni + ", " + renk_metni,
            "tohum": 42,
            "model": "flux-1-schnell",
            "brif": "sessiz bir çalışma kafesi için afiş",
            "durum": "denenmedi",
        }
        kartlar.append(kart)

print(len(kartlar))
```

Çıktı: `12`.

- `klasor` ızgaranın klasörü. Her kartın yolu klasör + stil + `_` + renk + `.jpg`: aynı kart her zaman aynı yolu alır.
  Bu, Adım 4'teki "kaldığı yerden devam"ın anahtarı.
- Önce iki yönerge parçasını sözlükten okuyup ayrı değişkenlere alıyoruz (`stil_metni`, `renk_metni`); sonra kartı kuruyoruz.
- Kartta üç alan daha var: `"model"`, `"brif"` ve `"durum"`. Kart hem üretimi yönetecek hem günlük olacak (Adım 5).
  `"durum": "denenmedi"` başlangıç değeri; üretim sırasında `"uretildi"` ya da `"olmadi"` olur.
- Listeleri ya da sözlükleri değiştirirsen bu hücreyi yeniden çalıştır; yoksa kartlar eski kalır.
- `kartlar.append(kart)`: kartı listeye ekler. Sonunda bir liste, içinde 12 sözlük.

```python
ilk_kart = kartlar[0]
print(ilk_kart["yol"])
print(ilk_kart["yonerge"])
```

Çıktı:

```
izgara/suluboya_adacayi.jpg
a ceramic coffee cup on a wooden desk next to an open notebook, soft morning light, watercolor illustration, sage green and beige palette
```

Bu bir **şablon**: özne ve tohum sabit, stil ve renk düzenli olarak değişiyor. Konu 7'deki kontrollü deneyin
iki eksenli hâli.

---

## Adım 3 — Önce hesap: kota ve sınır

Konu 2'den hatırla: Cloudflare kotayı **neuron** ile sayar ve günde 10.000 neuron ücretsiz. Bütün modeller (görsel,
metin, görsel okuma) bu aynı kotadan yer. Bir görsel (1024 × 1024, 4 adım) yaklaşık 58 neuron tutar. Hesap şöyle:
Cloudflare 1024 × 1024'lük görseli 512 × 512'lik 4 parça sayar; her parça 4,8, her adım 9,6 neuron:
4 × 4,8 + 4 × 9,6 ≈ 58. Günde kabaca 170 görsel eder.

```python
MAKS_URETIM = 12
GORSEL_BASI_NEURON = 58

tahmin = len(kartlar) * GORSEL_BASI_NEURON
print("Kart sayısı:", len(kartlar))
print("Tahmini kota:", tahmin, "/ 10000 neuron")
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
- Kart sayısı sınırı aşarsa uyarı yazar; Adım 4'teki döngü sınırda durur. Şimdi yazmaz: 12 kart sınırı aşmıyor
  (Bonus 3'te listeyi büyütünce görürsün).

---

## Adım 4 — Toplu üretim: önce küçük bir deneme

```python
import os
from uretim import sabirli_ciz
```

- `sabirli_ciz(yonerge, tohum, yol)`, `ciz`'in sabırlı hâli: istek olmazsa 5 saniye bekleyip yeniden dener, en fazla üç
  kez. Sunucu bir an meşgulse ya da çok hızlı istek gönderdiysek (durum kodu 429) bu çoğu zaman yeter. Üçü de olmazsa
  `None` verir; yani başarısız her kart 3 istek ve 10 saniye bekleme demek.
- Günlük kota bittiyse beklemek işe yaramaz ve `sabirli_ciz` bunu ayırt etmiyor. Üst üste `429` görürsen hücreyi durdur
  (hücrenin yanındaki kare düğme, **Interrupt**); kota yenilenince kaldığın yerden devam edersin.
- `os`, Python'la birlikte gelen ve dosya, klasör işlerini yapan modül; kurulum istemez. `os.path.exists(yol)`, "bu yolda
  bir dosya var mı?" sorusunu cevaplar: `True` ya da `False`.

```python
def toplu_uret(liste, sinir):
    denenen = 0
    for kart in liste:
        yol = kart["yol"]
        if os.path.exists(yol):
            kart["durum"] = "uretildi"
            print("Zaten var, atlıyorum:", yol)
            continue
        if denenen >= sinir:
            print("Sınıra geldim, duruyorum")
            break
        sonuc = sabirli_ciz(kart["yonerge"], kart["tohum"], yol)
        denenen = denenen + 1
        if sonuc is None:
            kart["durum"] = "olmadi"
            print("Olmadı, atlıyorum:", yol)
        else:
            kart["durum"] = "uretildi"
            print("Kaydedildi:", yol)
    print("Bu çalıştırmada denenen:", denenen)
```

- Döngü bir fonksiyonda, çünkü onu farklı sınırlarla iki kez çağıracağız: `toplu_uret(liste, sinir)` bir kart
  listesi ve bir sınır alır. `sinir` bu çalıştırmada en fazla kaç görsel deneneceği.
- **Zaten varsa** atla: `continue` bu kartı bırakır, döngünün başına döner, sıradakine geçer. Dosya varsa daha önce
  üretilmiştir; o yüzden durumu `uretildi`.
- **Sınıra geldiysen** dur: `break` döngüyü tamamen bitirir.
- Değilse üret. Kartın içine sonucunu yaz: `kart["durum"] = "uretildi"` ya da `"olmadi"`. Sözlükteki bir değer böyle
  değiştirilir; anahtar yoksa eklenir (Bonus'taki `model_puani` gibi).
- `sonuc is None`: "sonuç hiçbir şey mi?" `sabirli_ciz` üç denemede de başaramadıysa `None` verir; soru `True` olur.
- `denenen` üretmeyi denediğimiz kartları sayar; atlanan kartlar sayılmaz. Sınır bu sayaca bakar.
- Adım 1'deki üzerine yazma tehlikesi burada işe yarar bir kurala dönüşüyor: aynı kart her zaman aynı yolu aldığı için
  "zaten var mı?" sorusu **kaldığı yerden devam** demek.

Önce küçük bir deneme:

```python
toplu_uret(kartlar, 3)
```

Üç görsel gelir ve `Sınıra geldim, duruyorum` yazılır. `izgara/` klasörüne bak; beğendiysen asıl sınırla devam:

```python
toplu_uret(kartlar, MAKS_URETIM)
```

İlk üç kart **atlanır**, kalan dokuzu üretilir: program kaldığı yerden devam etti. (İlk denemede bir kart olmadıysa
o da yeniden denenir: dosyası yok.) Bir dosyayı silip yeniden çalıştırırsan yalnızca o kart üretilir. Kota biterse ya da
internet koparsa, sonra aynı hücreyi çalıştırmak yeter.

| Konu 7'nin dosya adı | Bugünkü dosya adı |
|---|---|
| `001.jpg`, `002.jpg`, ... | `suluboya_adacayi.jpg` |
| Her kayıt yeni bir numara: hiçbir şey üzerine yazılmaz | Aynı kart aynı ad: zaten varsa atlanır, kaldığı yerden devam edilir |
| Adına bakıp ne olduğunu bilemezsin | Adı stil ve rengi söylüyor |

**Dikkat:** yolda olmayan bir şeyi (ör. `ozne`'yi ya da tohumu) değiştirip yeniden çalıştırırsan program bunun yeni
bir iş olduğunu bilemez ve eski görselleri atlar. Öyle bir değişiklikte Adım 2'deki `klasor`'u da değiştir
(ör. `"izgara2/"`).

---

## Adım 5 — Üretim günlüğü: kartları JSON'a yaz

Kartlar zaten günlüğün kendisi: her birinde stil, renk, yol, yönergenin tamamı, tohum, model, brif ve sonuç
(`durum`) var. Hepsini ızgaranın klasörüne bir **JSON** dosyası olarak yazıyoruz:

```python
import json

gunluk_yolu = klasor + "uretim_gunlugu.json"
with open(gunluk_yolu, "w", encoding="utf-8") as dosya:
    json.dump(kartlar, dosya, ensure_ascii=False, indent=2)

print("Günlük yazıldı:", gunluk_yolu)
```

Çıktı: `Günlük yazıldı: izgara/uretim_gunlugu.json`.

- `json.dump(kartlar, dosya, ...)`: listeyi dosyaya JSON olarak yazar. Önce yazılacak şey, sonra dosya.
- `ensure_ascii=False`: Türkçe harfler (`brif` alanındaki ç ve ş) `\u00e7` gibi kodlara dönüşmesin, olduğu gibi yazılsın.
- `indent=2`: her kart ayrı satırlarda, okunur biçimde.
- JSON, Konu 2'de API'nin cevabındaki biçim: sözlükler ve listeler, metin olarak. İnsan da okuyabilir, program da
  `json.load` ile geri okuyabilir (alıştırmada var).

Dosyayı VS Code'da aç. Bir müşteri aylar sonra "şu görselin aynısı, yalnızca rengi farklı" derse yönergesi, tohumu ve
modeli burada.

---

## Adım 6 — Kontak sayfası: bütün ızgara tek sayfada

Fotoğrafçılar filmdeki bütün kareleri tek kâğıda basıp en iyisini seçerdi: **kontak sayfası**. Bizimki bir
ızgara: satır sayısı stil sayısı, sütun sayısı renk sayısı.

```python
satir = len(stiller)
sutun = len(renkler)

plt.figure(figsize=(12, 9))
sira = 1
for kart in kartlar:
    plt.subplot(satir, sutun, sira)
    if os.path.exists(kart["yol"]):
        resim = plt.imread(kart["yol"])
        plt.imshow(resim)
    plt.title(kart["stil"] + " / " + kart["renk"], fontsize=9)
    plt.axis("off")
    sira = sira + 1

plt.savefig(klasor + "kontak_sayfasi.png", bbox_inches="tight")
plt.show()
```

- Konu 6'daki `subplot` döngüsü, bu kez birden çok satırla: `plt.subplot(satir, sutun, sira)` sayfayı `satir` × `sutun`
  kutuya böler ve `sira`ncı kutuyu seçer.
- `subplot` kutuları soldan sağa doldurur, satır bitince alttakine geçer. Kartlar stil stil sıralı olduğu için her
  satır bir stil, her sütun bir renk olur.
- Satır ve sütun sayısı listelerden geliyor: stil ya da renk ekleyince ızgara kendini ayarlar.
- `plt.figure(figsize=(12, 9))`: sayfanın boyutu (genişlik, yükseklik; inç).
- Görseli çizmeden önce `os.path.exists` ile soruyoruz: üretilemeyen kartın dosyası yok, `plt.imread` onu açamaz ve hata
  verir. Böylece o kartın kutusu boş kalır; başlığı yine yazılır.
- `fontsize=9`: başlığın yazı boyutu.
- `plt.savefig`: sayfayı dosyaya kaydeder; `bbox_inches="tight"` kenardaki boşluğu kırpar. `plt.show()`'dan **önce**
  gelmeli: gösterilen sayfa kapanır, sonradan kaydedilen dosya boş çıkar.

Sayfaya tasarımcı gözüyle bak: hangi stil brife uyuyor? Hangi renk? Kartlar kontrollü kurulduğu için bir satırın
hepsi kötüyse sorun stilde, bir sütunun hepsi kötüyse renkte. Kazananını yoluyla yaz:

```python
benim_secimim = "izgara/suluboya_adacayi.jpg"
```

Bugünün çıktısı `izgara/` klasöründe: 12 görsel, `kontak_sayfasi.png` ve `uretim_gunlugu.json`. Arayüzde 12 yönerge,
12 tıklama ve 12 indirme olacak iş burada birkaç hücre; üstelik kayıtlı ve yarıda kalırsa kaldığı yerden sürüyor.

---

## Bonus

**1. Modele kendi çıktısını okutmak.** Ölçek büyüyünce ilk elemeyi bir **görsel anlayan** modele yaptırabiliriz:
metni ve görseli birlikte anlayan, **çok kipli** (multimodal) bir model (Gemma). `gorsele_sor(yol, soru)` görseli ve
soruyu ona gönderir, cevabı metin olarak verir.

```python
from uretim import gorsele_sor

cevap = gorsele_sor(ilk_kart["yol"], "Describe this image in one short sentence.")
print(cevap)
```

Soruyu İngilizce yazıyoruz (Konu 7: modeller çoğunlukla İngilizce metinle eğitildi). Sonra her görsele aynı soruyu
soruyoruz: brife 1 ile 5 arasında ne kadar uyuyor?

```python
brif_ingilizce = "a poster for a quiet cafe where people come to study and work"
soru = "On a scale of 1 to 5, how well does this image fit this brief: " + brif_ingilizce + "? Answer with only the number."

for kart in kartlar:
    if os.path.exists(kart["yol"]):
        kart["model_puani"] = gorsele_sor(kart["yol"], soru)
        print(kart["yol"], kart["model_puani"])

print("Benim seçimim:", benim_secimim)
```

- `brif_ingilizce` ayrı bir değişkende: kendi brifine göre değiştirebilirsin.
- Her kartın içine `model_puani` diye yeni bir alan ekleniyor. Model "yalnızca sayı" isteğine her zaman uymayabilir,
  bir cümle de yazabilir; o yüzden cevabı olduğu gibi (metin) saklıyoruz. 12 istek birkaç dakika sürebilir.
- Puanları günlüğe eklemek için Adım 5'in hücresini bir kez daha çalıştır.

**Tartış:** modelin en yüksek puan verdikleri arasında senin seçimin var mı? Model brifteki kelimeleri görselde neyle
eşliyor olabilir? Model bir **ilk eleme** aracı, karar verici değil: onun da bir zevki, bir yanlılığı var (Konu 3).

**2. Tohum ekseni.** Seçtiğin kazananı (`benim_secimim`) üç farklı tohumla üret:

```python
for kart in kartlar:
    if kart["yol"] == benim_secimim:
        kazanan = kart

for tohum in [1, 2, 3]:
    yol = klasor + kazanan["stil"] + "_" + kazanan["renk"] + "_" + str(tohum) + ".jpg"
    sonuc = sabirli_ciz(kazanan["yonerge"], tohum, yol)
    print(sonuc)
```

- İlk döngü kazananın kartını listede bulur: yolu `benim_secimim`'e eşit olan kart.
- Yola stil, renk ve tohum yazılıyor: her tohum ayrı bir dosya (`izgara/suluboya_adacayi_1.jpg` gibi). `str(tohum)`
  sayıyı metne çevirir; yoksa metinle birleştirilemez.
- Aynı yönerge, üç tohum: fark kompozisyonda mı, renkte mi, ayrıntıda mı? Hangisini müşteriye götürürdün?

**3. Sınır gerçekten çalışıyor mu?** Isınma'daki `renkler` listesine ve Adım 2'deki `renk_yonergeleri` sözlüğüne bir
palet ekle (ör. `"mono"` ve `"black and white palette"`). Isınma'yı, Adım 2'nin hücrelerini ve Adım 3'ü yeniden çalıştır
(Adım 3 bu kez `Dikkat: kart sayısı sınırı aşıyor; ...` yazar: 15 kart, sınır 12), sonra:

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
| 1 | Tek görsel koddan; `input` ile yönerge; üzerine yazma | `ciz`, `ozne`, `yonerge`, `ciktilar/` (2 görsel) | gerekir |
| 2 | Şablon: yönerge sözlükleri ve kartlar | `stil_yonergeleri`, `renk_yonergeleri`, `klasor`, `kartlar` | istek yok |
| 3 | Kota hesabı ve sınır | `MAKS_URETIM` | istek yok |
| 4 | Toplu üretim döngüsü: önce 3, sonra kalanı | `sabirli_ciz`, `toplu_uret`, `izgara/` (12 görsel) | gerekir |
| 5 | Üretim günlüğü | `izgara/uretim_gunlugu.json` | istek yok |
| 6 | Kontak sayfası; kendi seçimin | `izgara/kontak_sayfasi.png`, `benim_secimim` | istek yok |
| Bonus | Görsel anlayan modelle eleme; tohum ekseni; sınırı denemek | `model_puani` alanları, tohumlu üç dosya | gerekir |

Derste kendi başına çalışacağın defter: `alistirma.ipynb`. Önce aynı klasörde yeni bir adla kopyala,
kopyada çalış. **Anahtar istemez ve görsel üretmez:** `veri/ornek_izgara/` klasöründeki hazır görsellerle çalışır
(altı kartın dördünün görseli var, ikisi "üretilememiş"). Üç bölümü var:

- **Kendin yaz:** toplu üretim döngüsünü (görsel üretmeden, `print` ile) ve 2 × 3'lük bir kontak sayfasını kendi elinle
  yazıyorsun. Kontak sayfasında kart listesi yok: yolları Isınma'daki iç içe döngüyle, Adım 2'deki kalıba göre
  kendin kuruyorsun. Derste önce bunlar.
- **Bozuk kodlar:** altı kısa hücre, birbirinden bağımsız. Üçü hata mesajı veriyor, üçü sessizce yanlış sonuç yazıyor.
- **Kendi başına:** `BOSLUK` yazan yerleri doldurduğun yedi soru.

---

## Sık karşılaşılan hatalar ve mesajlarını okumak

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `IndentationError: expected an indented block after 'for' statement ...` | İçteki döngünün satırı yeterince içeride değil | İç döngünün satırları iki girinti içeride olmalı |
| Kombinasyonların yalnızca bir kısmı yazılıyor | `print` (ya da `append`) iç döngünün dışına kaymış | Satırı iç döngünün hizasına al |
| `ModuleNotFoundError: No module named 'uretim'` | Defterin kopyası konu klasörünün dışında | Kopya `uretim.py`'nin yanında, `08-koddan-toplu-uretim` klasöründe olmalı |
| `FileNotFoundError: ... '../anahtar.txt'` (Adım 1) | Anahtar dosyası yok ya da yanlış yerde | `gita3111` klasöründe durmalı; sonra Adım 1'in ilk hücresini yeniden çalıştır |
| `KeyError: 'ACCOUNT_ID'` (Adım 1) | `anahtar.txt`'de `=` yerine `:` ya da satır eksik | İki satır `AD = değer` biçiminde olmalı |
| `NameError: name 'ciz' is not defined` | Adım 1'in ilk hücresi hata verdi ya da çalıştırılmadı | Önce o hücredeki hatayı düzelt |
| `İstek başarısız, durum kodu: 401` | Anahtar yanlış | `anahtar.txt`'yi düzelt, çekirdeği yeniden başlat (**Restart**), baştan çalıştır: `uretim.py` anahtarı yalnızca ilk okumada alır |
| `İstek başarısız, durum kodu: 400` (Adım 1, `input`) | Yönerge kutusu boş geçildi | Hücreyi yeniden çalıştır, bir yönerge yaz |
| `FileNotFoundError: ... 'ciktilar/ilk.jpg'` (Adım 1) | `ciz` başarısız oldu, dosya yazılmadı | Üstteki hücrenin `İstek başarısız` satırına bak |
| Görselim kayboldu, yerinde başka bir görsel var | Aynı yola ikinci kez çizildi: üzerine yazıldı | Her görsele ayrı bir ad ver (Adım 1'in dersi) |
| `KeyError: 'suluboya '` ya da `KeyError: 2` | Sözlükte olmayan bir anahtar (fazla boşluk, sıra numarası) | Anahtar adını birebir yaz; kartlar sözlük: `kart["yol"]` |
| `KeyError: 'mono'` (Adım 2) | Listeye eklenen kısa adın yönerge sözlüğünde karşılığı yok | Her kısa adı sözlüğe de ekle, sonra kart hücresini yeniden çalıştır |
| `NameError: name 'os' is not defined` ya da `'sabirli_ciz'` | Adım 4'ün ilk hücresi çalıştırılmadı | Adım 4'ü baştan çalıştır |
| `NameError: name 'toplu_uret' is not defined` | Adım 4'ün fonksiyon hücresi çalıştırılmadı | O hücreyi çalıştır |
| `Bağlanamadım ya da cevap gelmedi` | İnternet yok ya da sunucu 2 dakikada (görsel anlayan model 3 dakikada) cevap vermedi | İnternete bak; sonra aynı hücre kaldığı yerden devam eder |
| `İstek başarısız, durum kodu: 429` ve `Deneme ... olmadı` | Çok hızlı istek ya da günlük kota doldu | Bekle; üst üste geliyorsa hücreyi durdur. Kota 03:00'te (Türkiye saati) yenilenir; sonra aynı hücreyi çalıştır, kaldığı yerden devam eder |
| Hücre uzun süre bitmiyor | `sabirli_ciz` bekliyor (başarısız her denemeden sonra 5 saniye) ya da 9–12 istek sürüyor | Bekle; mesajlara bak |
| Hiçbir şey üretilmiyor, hepsi `Zaten var` | Görseller önceki bir çalıştırmadan var | Doğru davranış. `ozne`'yi değiştirdiysen `klasor`'u da değiştir; yoksa günlük eski görseli yeni yönergeyle kaydeder |
| `TypeError: Object of type TextIOWrapper is not JSON serializable` | `json.dump`'a önce dosya, sonra liste verildi | Önce yazılacak şey: `json.dump(kartlar, dosya)` |
| Günlükte `\u00e7` gibi kodlar | `ensure_ascii=False` yazılmamış | Ekle |
| Kontak sayfasında kutular kaymış ya da `ValueError: num must be an integer with 1 <= num <= ...` | Listeler değişti ama kartlar yeniden kurulmadı | Isınma'dan itibaren sırayla yeniden çalıştır |
| Kontak sayfasında boş kutular | O kartlar üretilemedi (sınır, kota ya da hata) | `toplu_uret`'i yeniden çalıştır; yalnızca eksikler üretilir |
| `kontak_sayfasi.png` bembeyaz, ekrandaki sayfa doğru | `plt.savefig` satırı `plt.show()`'dan sonra yazılmış | Önce `savefig`, sonra `show` |
| `NameError: name 'benim_secimim' is not defined` | Adım 6'nın son hücresi atlandı | O hücreyi çalıştır (kendi kazananının yoluyla) |
| Bonus 2'de `NameError: name 'kazanan' is not defined` | `benim_secimim`'deki yol hiçbir kartın yoluna uymuyor | Yolu kontak sayfasındaki gibi, `izgara/` ve `.jpg` ile birlikte yaz |
| `model_puani` `None` | Görsel anlayan modelin isteği başarısız | Üstteki `İstek başarısız, durum kodu` ya da `Bağlanamadım` satırına bak |

---

## Kendini dene

Cevaplar notun en sonunda. Önce kendin düşün.

1. 4 stil, 5 renk ve 3 tohum kaç görsel eder? Günlük ücretsiz kotanın ne kadarı?
2. Bir arkadaşın kartların yolunu Konu 7'deki gibi sıra numarasıyla kurdu ve her çalıştırmada numara bir sonrakinden
   devam ediyor. `toplu_uret`'i ikinci kez çalıştırınca ne olur?
3. `if denenen >= sinir:` kontrolü neden görseli üretmeden önce yapılıyor?
4. Adım 1'de aynı yola iki kez çizince ilk görsel kayboldu. Adım 4'te aynı şey neden olmuyor?
5. Kontak sayfasında `linol` satırının dördü de kötü, `pastel` sütununda yalnızca biri kötü. Ne söyleyebilirsin?
6. Model bir görsele 5 puan verdi, sen beğenmedin. Hangisine güvenirsin? Model neden yanılmış olabilir?
7. Üretim günlüğünü neden JSON'a yazdık; bir metin dosyasına (`print` gibi) yazsak ne kaybederdik?

---

## Bu konuda öğrendiklerin

- **Aynı iş koddan.** `ciz(yonerge, tohum, yol)` görseli üretip senin seçtiğin yola kaydeder; yönerge parçaları
  değişkende, istersen kullanıcıdan (`input`). Aynı yola ikinci kez yazılan dosya eskisinin üzerine yazılır.
- **Kombinasyon.** İç içe döngü her stili her renkle eşler; sayı çarpılarak büyür.
- **Şablon ve kart.** Kısa adlar (dosya için) ile uzun yönerge parçaları (model için) sözlükte eşlenir; her
  kombinasyon bir kart (sözlük) olur, bütün kartlar bir liste.
- **Sınır ve kota.** Döngüden önce hesap; önce küçük bir deneme; sınırla kazara kota tüketimini önlemek.
- **Sağlamlık ve kaldığı yerden devam.** `sabirli_ciz` bekleyip yeniden dener; kararlı yollar ve "zaten var mı?"
  sorusuyla yalnızca eksikler üretilir.
- **Günlük.** Kartlar JSON'a yazılır: her görselin nasıl üretildiği ve durumu (`uretildi`, `olmadi`, `denenmedi`) kayıtta.
- **Kontak sayfası.** Bütün kombinasyonları tek sayfada görmek; satırlar ve sütunlar kontrollü deneyin iki ekseni.
- **Çok kipli eleme (Bonus).** Görsel anlayan bir model ilk elemeyi yapar; kararı tasarımcı verir.

## Bu konunun tek cümlesi

> Bir şablon ve listelerle bir görsel ızgarasını tek seferde üretirsin; sınır koyar, kaldığı yerden devam eder,
> her şeyi kayda geçirir ve hepsini bir kontak sayfasında yan yana değerlendirirsin.

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **`ciz(yonerge, tohum, yol)`** | Görseli üretip `yol`a kaydeden hazır fonksiyon; başarısızsa `None` |
| **Yol** | Dosyanın klasörüyle birlikte adı: `ciktilar/ilk.jpg` |
| **Üzerine yazmak** | Var olan bir dosyanın yerine aynı adla yenisini kaydetmek; eskisi geri gelmez |
| **`input`** | Kullanıcıya bir soru sorup yazdığını metin olarak almak |
| **Kombinasyon** | İki ya da daha çok listenin her elemanının birbiriyle eşleşmesi: 3 × 4 = 12 |
| **İç içe döngü** | Bir döngünün içinde başka bir döngü; içteki döngü, dıştakinin her turunda baştan sona döner |
| **Şablon** | Sabit kısmı ve değişen boşlukları olan yönerge |
| **Kart** | Bir kombinasyonun bütün bilgileri: stil, renk, yol, yönerge, tohum, model, durum (bir sözlük) |
| **Izgara** | Satırları bir değişken, sütunları öbür değişken olan görsel düzeni |
| **`continue` / `break`** | Döngüde sıradakine geç / döngüyü bitir |
| **`os.path.exists(yol)`** | Bu yolda bir dosya var mı? `True` ya da `False` |
| **Sabit (`MAKS_URETIM`)** | Değişmemesi gereken değer; büyük harfle yazılır |
| **Neuron** | Cloudflare'in kota birimi; günde 10.000 ücretsiz, bir görsel ~58 |
| **Kaldığı yerden devam** | Var olan çıktıları atlayıp yalnızca eksikleri üretmek |
| **`json.dump` / `json.load`** | Python listelerini ve sözlüklerini JSON dosyasına yazmak / dosyadan okumak |
| **Kontak sayfası** | Bütün kombinasyonları tek görselde ızgara hâlinde gösteren sayfa |
| **Çok kipli (multimodal)** | Metni ve görseli birlikte anlayan model |

## Ödev

`odevler/odev8.md` (puansız): kendi konunda bir ızgara üret (en az 2 stil × 3 renk, en fazla 12 görsel) ve `odev8/`
klasörüne kaydet; kontak sayfasını ve üretim günlüğünü getir. Hangi kombinasyon kazandı, neden?
Görsellerini sakla: Konu 9'da birini videoya çevireceğiz.

## Sonraki konu

**Konu 9 — Video, arayüzden.** Bugün bir şablonla bir ızgara ürettik. Konu 9'da hareket ekliyoruz: bu kez kod
yazmadan, bir arayüzde. Bugünkü görsellerinden birini kısa bir videoya çevireceğiz. Video yavaş ve pahalı bir üretim;
bugünkü "önce hesap" alışkanlığı orada da işe yarayacak.

---

## Kendini dene — cevaplar

1. 4 × 5 × 3 = 60 görsel; 60 × 58 ≈ 3.480 neuron, günlük kotanın üçte birinden fazla. Sınırsız ve her seferinde yeni
   adlarla aynı döngüyü yanlışlıkla iki kez çalıştırmak 6.960 neuron eder: kotanın yaklaşık %70'i. Sınır ve
   "zaten var mı?" bu yüzden var.
2. Her çalıştırmada numaralar değiştiği için hiçbir yol "zaten var" olmaz; bütün görseller **yeniden** üretilir ve kota
   harcanır. Kaldığı yerden devam için yol kararlı olmalı: aynı kart, aynı yol.
3. Sınır bir istek **gönderilmeden önce** bilinmeli: istek bir kez gitti mi kota harcanmıştır. Önce bakınca `sinir`
   0 bile olsa hiç istek gitmez. Ayrıca sayaç "zaten var" kontrolünden sonra olduğu için atlanan kartlar sayılmaz.
4. Çünkü `toplu_uret` çizmeden önce soruyor: "bu yolda dosya var mı?" Varsa hiç çizmiyor, atlıyor. Adım 1'de bu soruyu
   soran yoktu; `ciz` yolu verilen yere körü körüne yazdı.
5. Sorun büyük ihtimalle **stilde** (linol bu brif için uygun değil), renkte değil; `pastel` sütunundaki tek kötü
   görsel o stil–renk eşleşmesine özgü. Kontrollü kurulum bu ayrımı mümkün kılıyor.
6. Kendine. Model brifteki kelimeleri görseldeki nesnelerle (fincan, defter) eşliyor olabilir; ışığı, havayı,
   markanın kimliğini senin gibi tartmaz. Model ilk eleme içindir, karar senindir.
7. JSON'u program geri okuyabilir (`json.load`): hangi kartın hangi yönergeyle üretildiğini, tohumunu, durumunu bir
   sonraki çalıştırmada kullanabilirsin. Düz metin yalnızca insan içindir; programın onu yeniden ayrıştırması zor.
