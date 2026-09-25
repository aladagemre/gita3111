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

Yine tek bir program, adım adım büyüyecek.

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

VERI = "veri/renkler-etiketli.csv"

with open(VERI, encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

print("Toplam satır:", len(kayitlar))
print("İlk kayıt   :", kayitlar[0])
```

- `csv.DictReader` her satırı bir **sözlüğe** çeviriyor
- Yani tanıdık bir yapı: `kayit["hex"]`, `kayit["etiket"]`

-----

## Etiket dağılımı

```python
sayac = {}
for kayit in kayitlar:
    sayac[kayit["etiket"]] = sayac.get(kayit["etiket"], 0) + 1

for etiket in sorted(sayac, key=sayac.get, reverse=True):
    print(sayac[etiket], etiket)
```

Bu tam olarak Konu 1'in kelime sayacı — sadece kelime yerine etiket sayıyoruz.

Dağılım dengeli mi? Bir etiket ezici çoğunluktaysa model tembelleşir: hep onu der.

-----

## Sınıf anlaşabilmiş mi?

Aynı renge kaç farklı etiket verilmiş?

> kırmızı → ciddi, enerjik, sakin
> orta mavi → ciddi, enerjik, sakin
> lacivert → ciddi, enerjik, sakin

**20 rengin 20'sinde de sınıf anlaşamamış.**

Bu bir hata değil. Gerçek veri böyledir — insanlar aynı şeye farklı etiket verir.
Bu konunun asıl sorusu: **model bu kararsızlıkla ne yapıyor?**

-----

## Ama her renkte aynı ölçüde değil

```python
renk_sayaclari = {}
for kayit in kayitlar:
    ad = kayit["ad"]
    if ad not in renk_sayaclari:
        renk_sayaclari[ad] = {}
    renk_sayaclari[ad][kayit["etiket"]] = renk_sayaclari[ad].get(kayit["etiket"], 0) + 1

uzlasma = {}
for ad in renk_sayaclari:
    uzlasma[ad] = max(renk_sayaclari[ad].values())

for ad in sorted(uzlasma, key=uzlasma.get)[:3]:
    print(ad, renk_sayaclari[ad])
```

> krem → 5 enerjik, 5 sakin, 2 ciddi
> kırık beyaz → 11 sakin, 1 enerjik

Ekranda neredeyse aynı iki renk. Aradaki fark kremdeki hafif sarılık —
ve sınıfın yarısı için bu kayma rengi "enerjik" yapmış.
-----

## Anlaşmazlığın koyduğu tavan

Model bir renk için **tek** cevap verebilir. En iyi ihtimalle çoğunluğu söyler,
azınlıktakilerin hepsinde yanılır.

```python
tavan = sum(uzlasma.values()) / len(kayitlar)
print(f"En iyi modelin bile geçemeyeceği sınır: {tavan:.2f}")
```

**0.74.** Mükemmel bir model bile her dört cevaptan birini "yanlış" bilecek.

Bu yanlışlar modelin kusuru değil; sınıfın kendi içindeki görüş ayrılığı.

-----

## Adım 2 — Rengi sayıya çevirmek

Model "kırmızı" kelimesini anlamaz. Sayı ister.

```python
def hex_to_rgb(hex_kod):
    hex_kod = hex_kod.lstrip("#")
    kirmizi = int(hex_kod[0:2], 16)
    yesil = int(hex_kod[2:4], 16)
    mavi = int(hex_kod[4:6], 16)
    return (kirmizi, yesil, mavi)


print(hex_to_rgb("#E63946"))   # (230, 57, 70)
```

`16` tabanı: renk kodları onaltılık yazılır. `E6` = 230.

`16`'yı unutursan: `ValueError: invalid literal for int() with base 10: 'E6'`

-----

## Baştaki kural ne kadar iş görüyor?

```python
yakalanan = 0
for kayit in kayitlar:
    kirmizi, yesil, mavi = hex_to_rgb(kayit["hex"])
    if kayit["etiket"] == "enerjik" and kirmizi > 200 and yesil < 100:
        yakalanan = yakalanan + 1
print("Kuralın yakaladığı 'enerjik' etiketi:", yakalanan)
```

100 "enerjik" etiketinden **8**'i. Kural yalnızca kırmızıyı tanıyor.

Sınıfın "enerjik" kavramı çok daha geniş: bordo, şeftali, somon, tarçın, bal...
Canlı renklerle birlikte **sıcak** tonların neredeyse hepsi.

Kimsenin aklına gelmeyen bu genişliği veri kendisi taşıyor.

-----

## Öznitelik ve etiket: X ve y

```python
X = []
y = []
for kayit in kayitlar:
    X.append(hex_to_rgb(kayit["hex"]))
    y.append(kayit["etiket"])

print(X[0], "->", y[0])
```

- **X** = modelin **baktığı** şey (öznitelikler)
- **y** = modelin **tahmin etmesi gereken** şey (etiket)

`X[5]`'in cevabı `y[5]`'tir. İkisi aynı sırada olmalı — karışırsa model yanlış
şeyi öğrenir ve **kimse fark etmez.**

Model neye **bakmıyor**? Rengin adına, nerede kullanıldığına, yanındaki renklere.

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

print("Eğitim örneği:", len(X_egitim))
print("Test örneği  :", len(X_test))
```

- Soldaki **dört değişken tek satırda** doluyor: fonksiyon dört şey birden
  döndürüyor, Python da sırayla dağıtıyor. Sıra önemli, karıştırma
- `test_size=0.25` → dörtte biri teste ayrılıyor
- `random_state=42` → her çalıştırmada aynı bölme olsun diye; karşılaştırma yapabilelim

-----

## Adım 4 — Model: en yakın komşular

Kullanacağımız modelin mantığı tek cümle:

> Bu renge en çok benzeyen 5 rengi bul. Onlar ne dediyse onu de.

- Formül yok, sezgi var
- "Benzeme" burada RGB sayılarının yakınlığı demek
- Konu 4'te aynı fikri kelimeler için kullanacağız

Bizim veride her renk 12 kez geçiyor: model çoğu zaman **aynı rengi etiketleyen
beş arkadaşına** soruyor.

Basit görünüyor ama gerçek işlerde hâlâ kullanılıyor.

-----

## Modeli eğitmek

```python
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=5)

model.fit(X_egitim, y_egitim)

dogruluk = model.score(X_test, y_test)
print(f"Test doğruluğu: {dogruluk:.2f}")
```

`model` burada bir **araç**: kurduktan sonra üç düğmesi var.

- **kur** — kaç komşuya bakacağını söyle
- **`fit`** — "bu örneklere bak ve öğren"
- **`score`** — "hiç görmediklerinde kaç tanesini bildin?"
- (dördüncüsü `predict` — "şu yeni örnek sence hangisi?")

`fit`, `score` ve `predict`, `metin.split()` ya da `sayac.get()` gibi: bir şeyin
üstüne nokta koyup komut veriyoruz. Yeni olan tek şey, bu şeyin bir model olması.

-----

## Sonuç bir şey ifade ediyor mu?

Diyelim doğruluk **%77** çıktı. İyi mi?

Kıyas olmadan bilemeyiz. Alttan kıyas — hiç düşünmeden hep en sık etiketi deseydik:

```python
sayac = {}
for etiket in y_egitim:
    sayac[etiket] = sayac.get(etiket, 0) + 1
en_sik = sorted(sayac, key=sayac.get, reverse=True)[0]

kor_tahmin = y_test.count(en_sik) / len(y_test)
print(f"Hep '{en_sik}' deseydik: {kor_tahmin:.2f}")
```

**%45.** Demek ki model gerçekten bir şey öğrenmiş.
-----

## Alttan ve üstten kıyas

| | Doğruluk |
|---|---|
| Kör tahmin (hep "enerjik") | 0.45 |
| Bizim model | **0.77** |
| Tavan (test verisinde) | 0.78 |

Model kör tahmini açık farkla geçti ve **tavana bir cevap kaldı.**

Bu veriyle modeli daha "akıllı" yapmaya çalışmak boşuna. Kalan yanlışlar
modelin değil, sınıfın görüş ayrılığının payı.
-----

## Kaç arkadaşa sormalı? Tek sayıya güvenmeli mi?

```python
for k in [1, 5, 15, 45]:
    deneme = KNeighborsClassifier(n_neighbors=k)
    deneme.fit(X_egitim, y_egitim)
    print(f"k={k:<3} {deneme.score(X_test, y_test):.2f}")
```

k=1 → 0.70 · k=5 → 0.77 · k=15 → 0.73 · k=45 → 0.72

- **k=1:** tek arkadaşa sormak. Azınlıktaysa yanılırsın — ezberin en basit hâli
- **k çok büyük:** başka renklerin oyları karışıyor

`random_state`'i değiştirince doğruluk **0.65 ile 0.78** arasında oynuyor.
60 test satırında tek bir satır ≈ 2 puan. "0.77" değil, "0.65–0.78 arası" demek daha dürüst.

-----

## Adım 5 — Yanıldığı yere bakmak

```python
tahminler = model.predict(X_test)

yanlislar = []
for i in range(len(y_test)):
    if tahminler[i] != y_test[i]:
        yanlislar.append({"hex": hex_test[i],
                          "gercek": y_test[i],
                          "tahmin": tahminler[i]})

print(f"{len(y_test)} örnekten {len(yanlislar)} tanesinde yanıldı.")
```

Doğruluk tek bir sayı. Asıl öğretici olan **nerede** yanıldığı.

-----

## Yanılgıları görselleştirmek

Her yanlış tahmini bir renk karesi olarak çizdiriyoruz, altında sınıfın etiketi ve
modelin tahmini.

Bakınca üç şey görürsün:

- Bazı yanlışlar **makul** — sınıf da o renkte anlaşamamıştı
- Bazıları ara tonlarda — model sınırda kalmış
- Bazılarında model haklı, **etiket tartışmalı**

Model "hata yapıyor" demek her zaman "model kötü" demek değildir.
-----

## Yanlışların çoğu azınlık görüşü

14 yanılgının **12'sinde** model sınıfın çoğunluğunu söylüyor; yanlış sayılan
öğrenci azınlıkta.

> şeftali — bir öğrenci "ciddi", sınıfın 10'u "enerjik", model "enerjik"

Bu 12'nin yarısında azınlık, sıcak toprak tonlarına (şeftali, tarçın, bal, somon,
gül kurusu) "ciddi" demiş.

- Model bir **çoğunluk sesi** üretir; azınlığın algısını siler
- Hedef kitlen o azınlıksa model sana yanlış yol gösterir

-----

## Adım 6 — Veri arttıkça ne oluyor?

```python
for oran in [0.1, 0.25, 0.5, 0.75, 1.0]:
    adet = int(len(X_egitim) * oran)
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_egitim[:adet], y_egitim[:adet])
    print(adet, "örnek ->", round(model.score(X_test, y_test), 2))
```

Grafiği çizince eğri genelde önce hızlı yükselir, sonra düzleşir.

**Düzleştiği yer önemli:** oradan sonra veri eklemek işe yaramıyor demektir.

Bizde eğri tavanın hemen altında düzleşiyor. Aynı 20 renge daha çok öğrenci
eklemek tavanı yükseltmez; **başka türlü** veri gerekir: daha çok renk, bağlam.

-----

## Adım 7 — Model ne öğrendi?

Modelin içini açamayız. Ama kullanıcı testi gibi, hiç görmediği renkleri sorabiliriz:

```python
adlar = []
for kayit in kayitlar:
    adlar.append(kayit["ad"])

tam_model = KNeighborsClassifier(n_neighbors=5)
tam_model.fit(X, y)

rgb = hex_to_rgb("#E8DCC4")                       # bej
mesafeler, siralar = tam_model.kneighbors([rgb])
print(tam_model.predict([rgb])[0], "- komşusu:", adlar[siralar[0][0]])
```

`kneighbors`: "cevabı hangi komşulara bakarak verdin?"

-----

## Kafe paleti için ikinci görüş

Konu 1'deki "sessiz çalışma kafesi" için aday palet:

| Renk | Model | En yakın bildiği renk |
|---|---|---|
| bej | enerjik | krem |
| sütlü kahve | enerjik | bal |
| adaçayı | sakin | gri mavi |
| orman yeşili | ciddi | petrol |
| kirli beyaz | sakin | kırık beyaz |

Sıcak nötrler "sakin" değil, "enerjik" tarafta.

**Ama:** bej hakkındaki kararı kremi etiketleyenler veriyor — ve krem sınıfın en
tartışmalı rengi. Bu bir kesinlik değil, "kullanıcıyla sına" işareti.

Dosya: `09_modeli_yokla.py`

-----

## Adım 8 — Hiç görmediği renkler

Rastgele bölmede her renk hem eğitimde hem testte var: model testteki lacivertin
9 kardeşini eğitimde görmüş.

Dürüst soru: **yeni bir renk gelince ne der?**

Bir rengi tamamen dışarıda bırak, kalan 19 renkle eğit, o rengi sor. 20 renk için tekrarla.

| Test türü | Doğruluk |
|---|---|
| Rastgele bölme (bilinen renkler) | 0.77 |
| Hiç görülmemiş renkler | **0.60** |

İkisi de doğru — farklı soruların cevabı.

Dosya: `10_gorulmemis_renkler.py`

-----

## RGB'de yakın, gözde uzak

- **Kırık beyaz** → model "enerjik" (sınıf 11/12 "sakin"). En yakın bildiği renk: krem
- **Gri mavi** → model "enerjik" (sınıf 10/12 "sakin"). En yakın bildiği renk: gül kurusu

Soğuk grimsi bir mavi ile tozlu bir pembe — bir tasarımcı bunlara asla "benzer" demez.
Ama üç sayının farkına bakınca yakınlar.

Model "benzerlik" kavramını ona verdiğimiz **temsilden** alıyor.

-----

## Programın tamamı — sekiz adım

| Adım | Ne yaptık | Elimizde ne oluştu |
|---|---|---|
| 1 | Veriyi okuduk, anlaşmazlığa baktık | `kayitlar`, tavan |
| 2 | Sayıya çevirdik | `X`, `y` |
| 3 | İkiye böldük | `X_egitim`, `X_test` |
| 4 | Eğittik, ölçtük, kıyasladık | `model`, `dogruluk` |
| 5 | Yanılgılara baktık | `yanilgilar.png` |
| 6 | Veri miktarını değiştirdik | `veri-miktari.png` |
| 7 | Yeni renklerle yokladık | kafe paleti için ikinci görüş |
| 8 | Hiç görmediği renklerde sınadık | dürüst doğruluk |

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
