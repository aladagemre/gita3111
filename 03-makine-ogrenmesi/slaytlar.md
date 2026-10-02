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
**7.** Model ne öğrendi? Kafe paletini soralım
**8.** Hiç görmediği bir renk

Hepsi tek defterde: `ders.ipynb`. Hücreleri sırayla çalıştır (**Shift + Enter**).

-----

## Kural yazmak ile öğretmek

Bir rengin "enerjik" mi "sakin" mi olduğunu kodla söylemek isteseydin:

```py
if kirmizi > 200 and yesil < 100:
    print("enerjik")
```

Bu bir **kural**. Sen yazdın, sen düşündün.

Makine öğrenmesi bunun tersi: kuralı sen yazmıyorsun, **örnek veriyorsun** ve
kuralı modelin bulmasını istiyorsun.

- Kural yazmak: "şu şartlarda şunu yap"
- Öğretmek: "işte 240 örnek, sen çıkar"

-----

## Isınma — sayaç neyi sayıyor?

`{'enerjik': 2, 'sakin': 1}` yazmalı. Ne yazıyor?

```python
sayac = {}
for kayit in kayitlar:
    etiket = kayit["ad"]
    if etiket in sayac:
        sayac[etiket] = sayac[etiket] + 1
    else:
        sayac[etiket] = 1

print(sayac)
```

> {'kırmızı': 1, 'orta mavi': 1, 'şeftali': 1}

Hata mesajı yok, sonuç yanlış. Saydığımız alan `"ad"` değil, `"etiket"` olmalı.

-----

## Adım 1 — Sınıfın verisine bakalım

```python
import csv

with open("veri/renkler-etiketli.csv", encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

print(len(kayitlar))
print(kayitlar[0])
```

- `csv.DictReader` her satırı bir **sözlüğe** çeviriyor: `kayit["ad"]`, `kayit["etiket"]`
- 12 öğrenci × 20 renk = 240 satır. Her renk 12 kez geçiyor

-----

## Sınıf "krem"e ne demiş?

Konu 1'deki sayacın aynısı, yalnızca krem satırlarında:

```python
sayac = {}
for kayit in kayitlar:
    if kayit["ad"] == "krem":
        etiket = kayit["etiket"]
        if etiket in sayac:
            sayac[etiket] = sayac[etiket] + 1
        else:
            sayac[etiket] = 1

print(sayac)
```

> {'enerjik': 5, 'ciddi': 2, 'sakin': 5}

`"krem"` yerine `"kırık beyaz"` yaz:

> {'enerjik': 1, 'sakin': 11}

-----

## Sınıf anlaşabilmiş mi?

| Renk | Dağılım |
|---|---|
| krem | 5 enerjik, 5 sakin, 2 ciddi |
| koyu yeşil | 6 ciddi, 4 sakin, 2 enerjik |
| hardal | 7 enerjik, 3 sakin, 2 ciddi |
| kırık beyaz | 11 sakin, 1 enerjik |
| bordo | 11 enerjik, 1 ciddi |

**20 rengin 20'sinde de sınıf anlaşamamış.** Ama her renkte aynı ölçüde değil.

Kırık beyaz ile krem ekranda neredeyse aynı renk. Aradaki fark kremdeki hafif
sarılık — ve sınıfın yarısı için bu kayma rengi "enerjik" yapmış.

-----

## Anlaşmazlığın koyduğu tavan

Model bir renk için **tek** cevap verebilir. En iyi ihtimalle çoğunluğu söyler,
azınlıktakilerin hepsinde yanılır.

- Kırık beyazda en iyi ihtimalle 12'de 11
- Kremde en iyi ihtimalle 12'de 5

20 rengin hepsi için toplayınca: **0.74.**

Mükemmel bir model bile her dört cevaptan birini "yanlış" bilecek.
Bu yanlışlar modelin kusuru değil; sınıfın kendi içindeki görüş ayrılığı.

-----

## Adım 2 — Rengi sayıya çevirmek

Model "kırmızı" kelimesini anlamaz. Sayı ister.

Renk seçicide `#E63946` yazınca yanında **R 230, G 57, B 70** görürsün.
Dosyada bu üç sayı hazır: `r`, `g`, `b` sütunları.

```python
X = []
y = []
for kayit in kayitlar:
    r = int(kayit["r"])
    g = int(kayit["g"])
    b = int(kayit["b"])
    X.append([r, g, b])
    y.append(kayit["etiket"])

print(len(X), len(y))
print(X[0], y[0])
```

> 240 240
> [230, 57, 70] enerjik

`int(...)`: dosyadan okunan her şey metindir (`'230'`); sayıya çeviriyoruz.

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

```python
from sklearn.model_selection import train_test_split

X_egitim, X_test, y_egitim, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
print(len(X_egitim), len(X_test))
```

> 180 60

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

```python
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_egitim, y_egitim)
dogruluk = model.score(X_test, y_test)
print(round(dogruluk, 2))
```

> 0.77

- **kur** — kaç komşuya bakacağını söyle
- **`fit`** — "bu örneklere bak ve öğren"
- **`score`** — "hiç görmediklerinde kaç tanesini bildin?"

-----

## Sonuç bir şey ifade ediyor mu?

Tek başına 0.77 bir şey söylemez. Kıyas gerekir.
**Kör tahmin:** hiç düşünmeden hep en sık etiketi ("enerjik") söylemek.

```python
enerjik = 0
for etiket in y_test:
    if etiket == "enerjik":
        enerjik = enerjik + 1

kor_tahmin = enerjik / len(y_test)
print(round(kor_tahmin, 2))
```

> 0.45

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

Adım 4'te `n_neighbors=5` yerine başka sayılar:

k=1 → 0.70 · k=5 → 0.77 · k=15 → 0.73 · k=45 → 0.72

- **k=1:** tek arkadaşa sormak. Azınlıktaysa yanılırsın — ezberin en basit hâli
- **k çok büyük:** başka renklerin oyları karışıyor

`random_state=42` yerine 0, 1, 2, 3, 4: doğruluk **0.65 ile 0.78** arasında oynuyor.
60 test satırında tek bir satır ≈ 2 puan. "0.77" değil, "0.65–0.78 arası" demek daha dürüst.

-----

## Adım 5 — Yanıldığı yere bakmak

Yanlış satırın adını bilmek için `kayitlar`'ı da bölüyoruz. **Aynı** `random_state` →
aynı 60 satır teste düşer.

```python
egitim_kayitlari, test_kayitlari = train_test_split(
    kayitlar, test_size=0.25, random_state=42
)
print(len(test_kayitlari))
```

`predict`: "bu renk sence hangisi?" Her zaman bir **liste** ister: `[renk]`.

-----

## Her test satırını sor

```python
for kayit in test_kayitlari:
    r = int(kayit["r"])
    g = int(kayit["g"])
    b = int(kayit["b"])
    renk = [r, g, b]
    tahminler = model.predict([renk])
    tahmin = tahminler[0]
    if tahmin != kayit["etiket"]:
        print(kayit["ad"], "öğrenci:", kayit["etiket"], "model:", tahmin)
```

> lacivert öğrenci: enerjik model: ciddi
> orta mavi öğrenci: sakin model: ciddi
> şeftali öğrenci: ciddi model: enerjik
> ... (14 satır)

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

Aynı model, beş farklı veri miktarı. `X_egitim[:adet]` → baştan `adet` tane örnek.

```python
adetler = [18, 45, 90, 135, 180]
dogruluklar = []
for adet in adetler:
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_egitim[:adet], y_egitim[:adet])
    dogruluk = model.score(X_test, y_test)
    print(adet, round(dogruluk, 2))
    dogruluklar.append(dogruluk)
```

> 18 0.48 · 45 0.72 · 90 0.62 · 135 0.75 · 180 0.77

-----

## Öğrenme eğrisi

```python
import matplotlib.pyplot as plt

plt.plot(adetler, dogruluklar, marker="o")
plt.xlabel("Eğitim örneği sayısı")
plt.ylabel("Test doğruluğu")
plt.show()
```

Eğri önce hızlı yükseliyor, sonra düzleşiyor. **Düzleştiği yer önemli:** oradan
sonra aynı türden veri eklemek pek işe yaramıyor.

Ortadaki düşüş hata değil — ödevde konuşacağız.

-----

## Adım 7 — Model ne öğrendi?

Modelin içini açamayız. Ama kullanıcı testi gibi, hiç görmediği renkleri sorabiliriz.
Bu kez **tüm veriyle** eğitiyoruz:

```python
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X, y)

bej = [232, 220, 196]
sutlu_kahve = [212, 163, 115]
adacayi = [163, 177, 138]
orman_yesili = [52, 78, 65]
kirli_beyaz = [245, 245, 245]

palet = [bej, sutlu_kahve, adacayi, orman_yesili, kirli_beyaz]
tahminler = model.predict(palet)
print(tahminler)
```

> ['enerjik' 'enerjik' 'sakin' 'ciddi' 'sakin']

-----

## Kafe paleti için ikinci görüş

| Renk | Model | En yakın bildiği renk |
|---|---|---|
| bej `#E8DCC4` | enerjik | krem |
| sütlü kahve `#D4A373` | enerjik | bal |
| adaçayı `#A3B18A` | sakin | gri mavi |
| orman yeşili `#344E41` | ciddi | petrol |
| kirli beyaz `#F5F5F5` | sakin | kırık beyaz |

Sıcak nötrler (bej, sütlü kahve) "sakin" değil, "enerjik" tarafta.

**Ama:** bej hakkındaki kararı kremi etiketleyenler veriyor — ve krem sınıfın en
tartışmalı rengi. Bu bir kesinlik değil, "kullanıcıyla sına" işareti.

-----

## Adım 8 — Hiç görmediği bir renk

Rastgele bölmede her renk hem eğitimde hem testte var: model testteki kırık beyazın
kardeşlerini eğitimde görmüş. Dürüst soru: **yeni bir renk gelince ne der?**

```python
X_haric = []
y_haric = []
for kayit in kayitlar:
    if kayit["ad"] != "kırık beyaz":
        r = int(kayit["r"])
        g = int(kayit["g"])
        b = int(kayit["b"])
        X_haric.append([r, g, b])
        y_haric.append(kayit["etiket"])

print(len(X_haric))
```

> 228

-----

## Kırık beyazı hiç görmeyen model

```python
model_haric = KNeighborsClassifier(n_neighbors=5)
model_haric.fit(X_haric, y_haric)

kirik_beyaz = [241, 250, 238]
tahminler = model_haric.predict([kirik_beyaz])
print(tahminler[0])
```

> enerjik

Kırık beyazı görmüş model (Adım 7) "sakin" diyor. Sınıfın 11/12'si de "sakin" demişti.

-----

## Her renk sırayla dışarıda

Aynı şeyi 20 rengin her biri için yapınca:

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

## Sekiz adım, tek defter

| Adım | Ne yaptık | Elimizde |
|---|---|---|
| 1 | Veriyi okuduk, anlaşmazlığa baktık | `kayitlar` |
| 2 | Rengi sayıya çevirdik | `X`, `y` |
| 3 | İkiye böldük | `X_egitim`, `X_test`, `y_egitim`, `y_test` |
| 4 | Eğittik, ölçtük, kör tahminle kıyasladık | `model` |
| 5 | Yanılgılara baktık | modelin yanıldığı 14 rengin listesi |
| 6 | Veri miktarını değiştirdik | öğrenme eğrisi |
| 7 | Kafe paletini sorduk | ikinci görüş |
| 8 | Hiç görmediği renkte sınadık | `model_haric` |

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

Adım 6'nın çıktısına bak: **yarısıyla** (90 örnek) ve **tamamıyla** (180 örnek) eğitilen model.

1. İki doğruluk oranını yaz
2. Tek cümle: fark ne, neden böyle olmuş olabilir?

İstersen defterin sonundaki **Bonus** hücresiyle kendi seçtiğin renkleri de sor —
modelle aynı fikirde misin?

Puan yok; Konu 4'ün başında sıradaki arkadaşlar gösterecek.

-----

## Sonraki konu: Konu 4

**Temsil ve gömme vektörleri.**

Bu konuda rengi üç sayıya çevirdik: `[230, 57, 70]`.
Konu 4'te **kelimeleri** sayıya çevireceğiz — bu kez üç değil, 1024 sayıya.

Bu konunun "en yakın komşu" fikri orada da karşımıza çıkacak: iki kelime
birbirine benziyor mu, sayılarına bakarak söyleyeceğiz.

Ve gri mavi ile gül kurusunun sorusu orada daha da önemli: **sayılardaki yakınlık,
bizim "benzer" dediğimiz şeyi yakalıyor mu?**
