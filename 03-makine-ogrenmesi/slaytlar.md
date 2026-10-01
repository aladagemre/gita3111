# Konu 3 — Makine Öğrenmesi Nedir?

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 2'den Konu 3'e

**Konu 2'de:** hazır bir modele soru sorduk. Model kutunun içindeydi.

**Bu konuda:** kutuyu açıyoruz. Kendi modelimizi eğiteceğiz.

- Sınıfın Konu 2 ödevinde etiketlediği renklerle
- Matematik yok, formül yok
- Sonunda model yanılacak — ve asıl konumuz o olacak

Bu konuda öğreneceğin şey, dönemin geri kalanında "model" dediğimiz şeyin ne olduğu.

-----

## Konunun planı

**1.** Sınıfın verisine bakalım — anlaşabilmiş miyiz?
**2.** Rengi sayıya çevirelim
**3.** Veriyi ikiye bölelim: eğitim ve test
**4.** Modeli eğitelim ve ölçelim
**5.** Yanıldığı yerlere bakalım
**6.** Veri arttıkça ne değişiyor?
**7.** Model ne öğrendi? Yeni renklerle yoklayalım
**8.** Hiç görmediği renklerde dürüst sınav

Her adım bir dosya: bir öncekini kopyala, birkaç satır ekle.

-----

## Kural yazmak ile öğretmek

Bir rengin "enerjik" mi "sakin" mi olduğunu kodla söylemek isteseydin:

```python
if kirmizi > 200 and yesil < 100:
    return "enerjik"
```

Bu bir **kural**. Sen yazdın, sen düşündün.

Makine öğrenmesi bunun tersi: kuralı sen yazmıyorsun, **örnek veriyorsun** ve
kuralı modelin bulmasını istiyorsun.

- Kural yazmak: "şu şartlarda şunu yap"
- Öğretmek: "işte 240 örnek, sen çıkar"

-----

## Adım 1 — Sınıfın verisine bakalım

```python
import csv

with open("veri/renkler-etiketli.csv", encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

print(len(kayitlar))
print(kayitlar[0])
```

- `csv.DictReader` her satırı bir **sözlüğe** çeviriyor
- Yani tanıdık bir yapı: `kayit["hex"]`, `kayit["etiket"]`
- 12 öğrenci × 20 renk = 240 satır. Her renk 12 kez geçiyor

Dosya: `01_veriyi_oku.py`

-----

## Sınıf anlaşabilmiş mi?

Her renk için ayrı bir sayaç — Konu 1'in sayacı, sözlüğün içinde:

```python
renkler = {}  # her renk için ayrı bir sayaç
for kayit in kayitlar:
    ad = kayit["ad"]
    if ad not in renkler:
        renkler[ad] = {}
    renkler[ad][kayit["etiket"]] = renkler[ad].get(kayit["etiket"], 0) + 1

for ad in renkler:
    print(ad, renkler[ad])
```

> kırık beyaz {'enerjik': 1, 'sakin': 11}
> krem {'enerjik': 5, 'ciddi': 2, 'sakin': 5}

**20 rengin 20'sinde de sınıf anlaşamamış.** Ama her renkte aynı ölçüde değil.

Kırık beyaz ile krem ekranda neredeyse aynı renk. Aradaki fark kremdeki hafif
sarılık — ve sınıfın yarısı için bu kayma rengi "enerjik" yapmış.

-----

## Anlaşmazlığın koyduğu tavan

Model bir renk için **tek** cevap verebilir. En iyi ihtimalle çoğunluğu söyler,
azınlıktakilerin hepsinde yanılır.

```python
tutan = 0  # model her renkte en iyi ihtimalle çoğunluğu bilir
for ad in renkler:
    tutan = tutan + max(renkler[ad].values())
print("Tavan:", round(tutan / len(kayitlar), 2))
```

**0.74.** Mükemmel bir model bile her dört cevaptan birini "yanlış" bilecek.

Bu yanlışlar modelin kusuru değil; sınıfın kendi içindeki görüş ayrılığı.

-----

## Adım 2 — Rengi sayıya çevirmek

Model "kırmızı" kelimesini anlamaz. Sayı ister.

```python
import csv

with open("veri/renkler-etiketli.csv", encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

X = []
y = []
for kayit in kayitlar:
    kod = kayit["hex"]
    X.append((int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16)))
    y.append(kayit["etiket"])

print(len(X), len(y))
print(kayitlar[0]["hex"], X[0], y[0])
```

- `kod[1:3]` → `"E6"` (0. karakter `#`, onu atlıyoruz)
- `int("E6", 16)` → 230: renk kodları 16 tabanında yazılır
- `16`'yı unutursan: `ValueError: invalid literal for int() with base 10: 'E6'`

> #E63946 (230, 57, 70) enerjik

Dosya: `02_ozellik_etiket.py`

-----

## Öznitelik ve etiket: X ve y

- **X** = modelin **baktığı** şey (öznitelikler): üç sayı
- **y** = modelin **tahmin etmesi gereken** şey (etiket)

`X[5]`'in cevabı `y[5]`'tir. İkisi aynı döngüde, aynı sırada doluyor — karışırsa
model yanlış şeyi öğrenir ve **kimse fark etmez.**

Model neye **bakmıyor**? Rengin adına, nerede kullanıldığına, yanındaki renklere.

-----

## Baştaki kural ne kadar iş görüyor?

`kirmizi > 200 and yesil < 100` kuralını sınıfın verisinde sınayınca:

100 "enerjik" etiketinden yalnızca **8**'ini yakalıyor. Kural yalnızca kırmızıyı tanıyor.

Sınıfın "enerjik" kavramı çok daha geniş: bordo, şeftali, somon, tarçın, bal...
Canlı renklerle birlikte **sıcak** tonların neredeyse hepsi.

Kimsenin aklına gelmeyen bu genişliği veri kendisi taşıyor.

-----

## Adım 3 — Neden veriyi ikiye bölüyoruz?

Modeli 240 örnekle eğitip yine aynı 240 örnekle sınarsak ne ölçmüş oluruz?

**Ezberi.**

Sınavda çıkmış soruyla sınav yapmak gibi. Öğrenci soruyu ezberlemiş olabilir;
öğrendiğini anlamak için **görmediği** soru sormak gerekir.

- **Eğitim verisi:** model bunlara bakarak öğrenir
- **Test verisi:** model bunları hiç görmez, ölçüm burada yapılır

-----

## Bölmeyi kodla yapmak

`02`'yi kopyala, en alta bölmeyi ekle:

```python
import csv
from sklearn.model_selection import train_test_split

with open("veri/renkler-etiketli.csv", encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

X = []
y = []
for kayit in kayitlar:
    kod = kayit["hex"]
    X.append((int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16)))
    y.append(kayit["etiket"])

X_egitim, X_test, y_egitim, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
print(len(X_egitim), len(X_test))
```

- Soldaki **dört değişken tek satırda** doluyor; sıra önemli, karıştırma
- `test_size=0.25` → dörtte biri (60 satır) teste ayrılıyor
- `random_state=42` → her çalıştırmada aynı bölme; karşılaştırma yapabilelim

-----

## Adım 4 — Model: en yakın komşular

Kullanacağımız modelin mantığı tek cümle:

> Bu renge en çok benzeyen 5 rengi bul. Onlar ne dediyse onu de.

- Formül yok, sezgi var
- "Benzeme" burada RGB sayılarının yakınlığı demek
- Konu 4'te aynı fikri kelimeler için kullanacağız

Bizim veride her renk 12 kez geçiyor: model çoğu zaman **aynı rengi etiketleyen
beş arkadaşına** soruyor.

-----

## Modeli eğitmek

`03`'ü kopyala: bir `import` ekle, en alttaki `print` yerine modeli yaz:

```python
import csv
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

with open("veri/renkler-etiketli.csv", encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

X = []
y = []
for kayit in kayitlar:
    kod = kayit["hex"]
    X.append((int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16)))
    y.append(kayit["etiket"])

X_egitim, X_test, y_egitim, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_egitim, y_egitim)
print("Model:", round(model.score(X_test, y_test), 2))

print("Hep enerjik:", round(y_test.count("enerjik") / len(y_test), 2))
```

- **kur** — kaç komşuya bakacağını söyle
- **`fit`** — "bu örneklere bak ve öğren"
- **`score`** — "hiç görmediklerinde kaç tanesini bildin?"

-----

## Sonuç bir şey ifade ediyor mu?

> Model: 0.77
> Hep enerjik: 0.45

Tek başına 0.77 bir şey söylemez. Kıyas gerekir.

**Alttan kıyas — kör tahmin:** hiç düşünmeden hep en sık etiketi söylemek.
Sınıfın verisinde en sık etiket "enerjik" (100 enerjik, 78 sakin, 62 ciddi).

Model kör tahmini açık farkla geçiyor: gerçekten bir şey öğrenmiş.

-----

## Alttan ve üstten kıyas

| | Doğruluk |
|---|---|
| Kör tahmin (hep "enerjik") | 0.45 |
| Bizim model | **0.77** |
| Tavan (bu 60 test satırında) | 0.80 |

Model kör tahmini açık farkla geçti ve **tavana iki cevap kaldı.**

Bu veriyle modeli daha "akıllı" yapmaya çalışmak boşuna. Kalan yanlışlar
modelin değil, sınıfın görüş ayrılığının payı.

-----

## Kaç arkadaşa sormalı? Tek sayıya güvenmeli mi?

`04`'te `n_neighbors=5` yerine başka sayılar:

k=1 → 0.70 · k=5 → 0.77 · k=15 → 0.73 · k=45 → 0.72

- **k=1:** tek arkadaşa sormak. Azınlıktaysa yanılırsın — ezberin en basit hâli
- **k çok büyük:** başka renklerin oyları karışıyor

`random_state=42` yerine 0, 1, 2, 3, 4: doğruluk **0.65 ile 0.78** arasında oynuyor.
60 test satırında tek bir satır ≈ 2 puan. "0.77" değil, "0.65–0.78 arası" demek daha dürüst.

-----

## Adım 5 — Yanıldığı yere bakmak

`04`'ü kopyala. Bu kez `kayitlar`ı da bölüyoruz: yanlış satırın adını ve kodunu bilelim.

```python
import csv
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

with open("veri/renkler-etiketli.csv", encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

X = []
y = []
for kayit in kayitlar:
    kod = kayit["hex"]
    X.append((int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16)))
    y.append(kayit["etiket"])

X_egitim, X_test, y_egitim, y_test, k_egitim, k_test = train_test_split(
    X, y, kayitlar, test_size=0.25, random_state=42
)

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_egitim, y_egitim)
tahminler = model.predict(X_test)
```

`predict`: "şu örnekler sence hangisi?" — her test satırı için bir tahmin.

-----

## Yanılgıları görselleştirmek

Dosyanın devamı: yanlışları topla, her birini kendi renginde bir çubuk olarak çiz.

```python
yazilar = []
kodlar = []
for i in range(len(y_test)):
    if tahminler[i] != y_test[i]:
        yazi = k_test[i]["ad"] + ": öğrenci " + y_test[i] + ", model " + tahminler[i]
        print(yazi)
        yazilar.append(yazi)
        kodlar.append(k_test[i]["hex"])

plt.barh(range(len(yazilar)), 1, color=kodlar, tick_label=yazilar)
plt.xticks([])
plt.savefig("yanilgilar.png", bbox_inches="tight")
```

Doğruluk tek bir sayı. Asıl öğretici olan **nerede** yanıldığı.
Görsel: `yanilgilar.png`

-----

## Yanlışların çoğu azınlık görüşü

60 test satırından 14'ünde yanıldı. 14 yanılgının **12'sinde** model sınıfın
çoğunluğunu söylüyor; yanlış sayılan öğrenci azınlıkta.

> şeftali: öğrenci ciddi, model enerjik — sınıfın 10'u "enerjik"

Bu 12'nin yarısında azınlık, sıcak toprak tonlarına (şeftali, tarçın, bal, somon,
gül kurusu) "ciddi" demiş.

- Model bir **çoğunluk sesi** üretir; azınlığın algısını siler
- Hedef kitlen o azınlıksa model sana yanlış yol gösterir

-----

## Adım 6 — Veri arttıkça ne oluyor?

`04`'ün ilk yarısı aynı; üstte bir `import` daha:

```python
import csv
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

with open("veri/renkler-etiketli.csv", encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

X = []
y = []
for kayit in kayitlar:
    kod = kayit["hex"]
    X.append((int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16)))
    y.append(kayit["etiket"])

X_egitim, X_test, y_egitim, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
```

-----

## Aynı model, beş farklı veri miktarı

```python
adetler = []
dogruluklar = []
for oran in [0.1, 0.25, 0.5, 0.75, 1.0]:
    adet = int(len(X_egitim) * oran)
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_egitim[:adet], y_egitim[:adet])
    adetler.append(adet)
    dogruluklar.append(round(model.score(X_test, y_test), 2))

print(adetler)
print(dogruluklar)
plt.plot(adetler, dogruluklar, marker="o")
plt.xlabel("Eğitim örneği sayısı")
plt.ylabel("Test doğruluğu")
plt.savefig("veri-miktari.png")
```

> [18, 45, 90, 135, 180]
> [0.48, 0.72, 0.62, 0.75, 0.77]

Eğri önce hızlı yükseliyor, sonra düzleşiyor. **Düzleştiği yer önemli:** oradan
sonra aynı türden veri eklemek pek işe yaramıyor.

Ortadaki düşüş hata değil — ödevde konuşacağız.

-----

## Adım 7 — Model ne öğrendi?

Modelin içini açamayız. Ama kullanıcı testi gibi, hiç görmediği renkleri sorabiliriz:

```python
import csv
from sklearn.neighbors import KNeighborsClassifier

with open("veri/renkler-etiketli.csv", encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

X = []
y = []
for kayit in kayitlar:
    kod = kayit["hex"]
    X.append((int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16)))
    y.append(kayit["etiket"])

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X, y)

for kod in ["#E8DCC4", "#D4A373", "#A3B18A", "#344E41", "#F5F5F5"]:
    rgb = (int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16))
    # kneighbors: cevabı hangi komşulara bakarak verdin?
    mesafeler, siralar = model.kneighbors([rgb])
    print(kod, model.predict([rgb])[0], "en yakın:", kayitlar[siralar[0][0]]["ad"])
```

-----

## Kafe paleti için ikinci görüş

> #E8DCC4 enerjik en yakın: krem
> #D4A373 enerjik en yakın: bal
> #A3B18A sakin en yakın: gri mavi
> #344E41 ciddi en yakın: petrol
> #F5F5F5 sakin en yakın: kırık beyaz

Sıcak nötrler (bej, sütlü kahve) "sakin" değil, "enerjik" tarafta.

**Ama:** bej hakkındaki kararı kremi etiketleyenler veriyor — ve krem sınıfın en
tartışmalı rengi. Bu bir kesinlik değil, "kullanıcıyla sına" işareti.

-----

## Adım 8 — Hiç görmediği renkler

Rastgele bölmede her renk hem eğitimde hem testte var: model testteki lacivertin
kardeşlerini eğitimde görmüş.

Dürüst soru: **yeni bir renk gelince ne der?**

Bir rengi tamamen dışarıda bırak, kalan 19 renkle eğit, o rengi sor. 20 renk için tekrarla.

```python
import csv
from sklearn.neighbors import KNeighborsClassifier

with open("veri/renkler-etiketli.csv", encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

renkler = {}
for kayit in kayitlar:
    renkler[kayit["ad"]] = kayit["hex"]
```

-----

## Her renk sırayla dışarıda

```python
tutan = 0
for disarida in renkler:
    # Bu rengin hiçbir satırını görmeyen bir model
    X = []
    y = []
    for kayit in kayitlar:
        if kayit["ad"] != disarida:
            kod = kayit["hex"]
            X.append((int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16)))
            y.append(kayit["etiket"])
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X, y)

    kod = renkler[disarida]
    tahmin = model.predict([(int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16))])[0]
    print(disarida, tahmin)
    for kayit in kayitlar:
        if kayit["ad"] == disarida and kayit["etiket"] == tahmin:
            tutan = tutan + 1

print("Hiç görmediği renklerde doğruluk:", round(tutan / len(kayitlar), 2))
```

| Test türü | Doğruluk |
|---|---|
| Rastgele bölme (bilinen renkler) | 0.77 |
| Hiç görülmemiş renkler | **0.60** |

İkisi de doğru — farklı soruların cevabı.

-----

## RGB'de yakın, gözde uzak

- **Kırık beyaz** → model "enerjik" (sınıf 11/12 "sakin"). En yakın bildiği renk: krem
- **Gri mavi** → model "enerjik" (sınıf 10/12 "sakin"). En yakın bildiği renk: gül kurusu

Soğuk grimsi bir mavi ile tozlu bir pembe — bir tasarımcı bunlara asla "benzer" demez.
Ama üç sayının farkına bakınca yakınlar.

Model "benzerlik" kavramını ona verdiğimiz **temsilden** alıyor.

-----

## Sekiz adım, sekiz dosya

| Adım | Ne yaptık | Dosya |
|---|---|---|
| 1 | Veriyi okuduk, anlaşmazlığa ve tavana baktık | `01_veriyi_oku.py` |
| 2 | Rengi sayıya çevirdik: X ve y | `02_ozellik_etiket.py` |
| 3 | İkiye böldük | `03_egitim_test.py` |
| 4 | Eğittik, ölçtük, kör tahminle kıyasladık | `04_model_egit.py` |
| 5 | Yanılgılara baktık | `05_yanilgilari_gor.py` |
| 6 | Veri miktarını değiştirdik | `06_veri_miktari.py` |
| 7 | Kafe paletini sorduk | `09_modeli_yokla.py` |
| 8 | Hiç görmediği renklerde sınadık | `10_gorulmemis_renkler.py` |

-----

## Dört yeni kavram, dört cümle

**Öznitelik ve etiket.** Modelin baktığı şey X, tahmin etmesi gereken şey y.
Aynı sırada olmak zorundalar.

**Eğitim ve test ayrımı.** Model test verisini hiç görmez. Görürse ölçtüğün şey
öğrenme değil ezber olur.

**Yanılma normaldir, ölçülür.** Doğruluğu kör tahmin ve tavanla kıyasla. %100
çıkıyorsa sevinme, önce bir yerde hata aramaya başla.

**Test hangi soruyu soruyor?** Bilinen renklerde 0.77, hiç görülmemiş renklerde 0.60.
Sonucu söylerken soruyu da söyle.

-----

## Bu konunun ödevi

Veriyi ikiye böl: **önce yarısıyla** eğit, sonra **tamamıyla**.

1. İki doğruluk oranını yaz
2. Tek cümle: fark ne, neden böyle olmuş olabilir?

İstersen `08_kendi_rengin.py` ile kendi seçtiğin renkleri de tahmin ettir —
modelle aynı fikirde misin?

Puan yok; Konu 4'ün başında sıradaki arkadaşlar gösterecek.

-----

## Sonraki konu: Konu 4

**Temsil ve gömme vektörleri.**

Bu konuda rengi üç sayıya çevirdik: `(230, 57, 70)`.
Konu 4'te **kelimeleri** sayıya çevireceğiz — bu kez üç değil, 1024 sayıya.

Bu konunun "en yakın komşu" fikri orada da karşımıza çıkacak: iki kelime
birbirine benziyor mu, sayılarına bakarak söyleyeceğiz.

Ve gri mavi ile gül kurusunun sorusu orada daha da önemli: **sayılardaki yakınlık,
bizim "benzer" dediğimiz şeyi yakalıyor mu?**
