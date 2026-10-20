# Konu 6 — Üretmek Ne Demek?

Bu not konunun özetidir; derste çalıştırdığımız `ders.ipynb` defteriyle **aynı sırada**
ilerler: Isınma, sonra Adım 1–8 ve kısa bir Bonus. Derste kaçırdığın bir yer olursa
buradan oku, sonra defterde o adımın hücrelerini çalıştır. Nottaki kod blokları
defterdeki hücrelerin birebir aynısı; notu okurken defter yanında açık dursun.

**Konu 4'te:** kelimeleri sayı listelerine çevirdik ve PCA ile yüzlerce sayıyı 2'ye indirip
bir **harita** çizdik.
**Konu 5'te:** dil modelinin metni, olasılıklardan bir seçim yaparak ürettiğini gördük.
**Bu konuda:** iki fikri birleştiriyoruz:

> Üretmek, öğrenilmiş bir haritada bir nokta seçip oradan geri kurmaktır.

Bunu görmek için 136 farklı fontta yazılmış **A** harfini kullanıyoruz. Harfleri 2 sayıya
sıkıştırıyoruz, 2 sayıdan geri kuruyoruz, sonra haritada **hiçbir fontta olmayan** noktalardan
yeni A'lar üretiyoruz.

**Konunun sonunda elinde:** 136 A'nın haritası, haritanın iki ekseni boyunca yürüyen A'lar ve
iki font arasında yürüyen beş A.

**Kurulum:** yeni kütüphane yok. NumPy (Konu 4), Matplotlib ve scikit-learn (Konu 3) zaten
kurulu. `git pull` ile konu klasörü geldikten sonra `gita3111` klasöründe bir kez `uv sync`
çalıştırman yeterli.

**Defteri açmak:** VS Code'da `06-uretmek-ne-demek` klasöründeki `ders.ipynb`'yi aç.
Sağ üstten çekirdek (kernel) olarak **`.venv`**'i seç. Hücreleri yukarıdan aşağı,
**Shift + Enter** ile sırayla çalıştır. Her hücre bir öncekinin değişkenini kullanır
(`resimler`, `pca`, `kodlar`...); bir hücreyi atlarsan sonraki hücre `NameError` verir.

**Anahtar:** gerekmez. Bu konuda internete hiç çıkmıyoruz; bütün iş senin bilgisayarında.

> **Beklenti ayarı.** Üretilen harfler **bulanık** olacak. Amaç güzel bir font yapmak
> değil, üretmenin mekanizmasını görmek. Görsel üreten büyük modeller aynı fikri çok
> daha büyük haritalarla ve çok daha güçlü bir "geri kurucu" ile yapıyor.

---

## Isınma: bir resim, bir sayı tablosudur

Konu 3'te bir renk üç sayıydı (R, G, B). Siyah-beyaz bir resim de sayılardan oluşur: her
kare (**piksel**) bir sayı. 0 boş, 1 mürekkep.

```python
import matplotlib.pyplot as plt

arti = [
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
]
plt.imshow(arti, cmap="gray_r")
plt.show()
```

- `arti` bir **liste listesi**: 5 satır, her satırda 5 sayı. Bir tablo gibi düşün.
- `plt.imshow` bu tabloyu resim olarak çizer: her sayı bir kare.
- `cmap="gray_r"` renk ölçeği: 0 beyaz, 1 siyah. (`gray` tersini yapar: 0 siyah.)

**Denemeler:**

- **T harfi:** ilk satırı `[1, 1, 1, 1, 1]`, üçüncü satırı `[0, 0, 1, 0, 0]` yap. Artık üst çizgi ve ortadan inen bir sap var.
- **`0.5`:** o kare **gri** olur. Sayı 0 ile 1 arasında olabilir; ne kadar büyükse o kadar koyu.

Bilgisayar için harf, fotoğraf, afiş: hepsi böyle tablolar. Bugünkü harfler 28 satır, 28
sütun: her biri **784** sayı. Renkli bir fotoğrafta her piksel için 3 sayı var (Konu 3'teki RGB).

---

## Adım 1 — 136 fontta A harfi

```python
import numpy as np

veri = np.load("veri/harfler.npz")
resimler = veri["A"] / 255
fontlar = list(veri["fontlar"])
turler = list(veri["turler"])

print(resimler.shape)
print(fontlar[0], turler[0])
```

Çıktı:

```
(136, 784)
C059 Bold serif
```

- `veri/harfler.npz` bu konunun veri dosyası. İçinde 136 fontta yazılmış **A, a, g ve R**
  harfleri, fontların adları ve türleri var. `.npz` NumPy'ın kendi dosya biçimi.
- `np.load` dosyayı açar. `veri["A"]` bir sözlükten değer alır gibi A harflerini verir.
- Dosyada her piksel 0 ile 255 arasında (Konu 3'teki RGB gibi). `/ 255` her sayıyı 255'e
  böler: hepsi 0 ile 1 arasına iner, ısınmadaki gibi. NumPy dizisinde bölme **her sayıya
  ayrı ayrı** uygulanır (Konu 4'ün Isınma 2'sindeki `kral - erkek` gibi).
- `list(...)` font adlarını ve türlerini bildiğimiz Python listesine çevirir.
- `resimler.shape`: dizinin **boyutları**. `(136, 784)` = 136 satır, her satırda 784 sayı.
  Her satır bir fontun A'sı. Konu 3'teki tablonun aynısı; yalnızca sütun sayısı çok fazla.

Font türleri dörde ayrılıyor: **serifli** (harf uçlarında küçük tırnaklar olan, gazete
yazısı gibi; dosyada `serif`), **serifsiz** (tırnaksız; dosyada `sans`), **mono** (her harfi aynı genişlikte, daktilo gibi) ve
**el yazısı**.

### Bir A'yı çizmek

```python
ilk = resimler[0]
plt.imshow(ilk.reshape(28, 28), cmap="gray_r")
plt.show()
```

784 sayı yan yana, tek sıra hâlinde duruyor. Resim olarak çizmek için onları 28'erli 28
satıra bölmemiz gerekiyor: `reshape(28, 28)` "28 satır, 28 sütun olarak diz" demek.
Sayıların kendisi değişmez, yalnızca diziliş değişir. 28 × 28 = 784, o yüzden tam oturur.

### İlk sekiz A

```python
sira = 1
for resim in resimler[:8]:
    plt.subplot(1, 8, sira)
    plt.imshow(resim.reshape(28, 28), cmap="gray_r")
    plt.axis("off")
    sira = sira + 1
plt.show()
```

- `resimler[:8]`: ilk 8 satır (Konu 3'teki `X_egitim[:adet]` gibi).
- `plt.subplot(1, 8, sira)`: resmi 1 satır, 8 sütunluk bir ızgaranın `sira` numaralı kutusuna çiz.
  Kutular 1'den başlar, 0'dan değil.
- `sira = sira + 1`: her turda bir sonraki kutuya geç. Konu 1'deki sayacın aynısı.
- `plt.axis("off")`: kenardaki sayıları (eksenleri) gizler.

Aynı harf sekiz farklı karakterde: kalın, eğik, ince, tırnaklı. Bir tipograf bu farklara
ad verir. Bilgisayar yalnızca 784 sayı görüyor.

---

## Adım 2 — Sıkıştır: 784 sayıdan 2 sayıya

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
pca.fit(resimler)
kodlar = pca.transform(resimler)

print(kodlar.shape)
print(kodlar[0])
```

Çıktı:

```
(136, 2)
[-3.12237157 -0.57654979]
```

(Son basamaklar bilgisayardan bilgisayara biraz değişebilir; önemli olan ilk iki basamak.)

- **PCA** Konu 4'ten tanıdık: çok sayıyı, en çok şey anlatan birkaç sayıya indirir.
- `n_components=2`: 2 sayıya ineceğiz.
- `fit`: PCA 136 A'nın hepsine bakıp aralarındaki farkı en iyi anlatan iki **yönü** bulur.
  Konu 3'teki `fit` gibi: "önce örneklere bak, öğren".
- `transform`: her A'yı bu iki yöne göre **2 sayıya** çevirir. Bu iki sayıya harfin **kodu**
  diyoruz. Buradaki "kod", yazdığımız Python kodu değil: harfin sıkıştırılmış hâli, kısa bir özeti.
- `kodlar.shape` `(136, 2)`: her A artık iki sayı. 784'ten 2'ye: neredeyse 400 kat küçüldü.

Bu iki sayı tek başına bir şey ifade etmiyor (Konu 4'teki gibi). Anlam, A'ların birbirine
göre nerede durduğunda.

---

## Adım 3 — Geri kur: 2 sayıdan 784 sayıya

Konu 4'te PCA'yı yalnızca harita çizmek için kullanmıştık. Bugün yeni bir şey yapıyoruz:
**geri dönüyoruz.**

```python
geri = pca.inverse_transform(kodlar)

plt.subplot(1, 2, 1)
plt.imshow(resimler[0].reshape(28, 28), cmap="gray_r")
plt.title("asıl")
plt.subplot(1, 2, 2)
plt.imshow(geri[0].reshape(28, 28), cmap="gray_r")
plt.title("2 sayıdan")
plt.show()
```

- `inverse_transform`: `transform`'un tersi. 2 sayılık koddan 784 sayılık bir resim kurar.
- `geri` de `(136, 784)`: her A'nın geri kurulmuş hâli.
- İki `subplot` yan yana iki kutu: solda asıl A, sağda 2 sayıdan kurulan A.
  `plt.title` kutunun üstüne başlık yazar.

Sonuç: bulanık ama okunur bir A. Yalnızca 2 sayı sakladık; geri kalan 782 sayıyı PCA
**öğrendiklerinden** doldurdu. PCA 136 A'ya bakarak "bir A genel olarak neye benzer"i
öğrenmişti; 2 sayı yalnızca "bu A, genel A'dan ne kadar ve hangi yönde farklı"yı söylüyor.

### Sıkıştır ve geri kur

Bu ikiliye **sıkıştır ve geri kur** diyoruz:

| Parça | Ne yapar | Bizde |
|---|---|---|
| **Kodlayıcı** | Resmi küçük bir koda sıkıştırır | `transform` |
| **Kod** | Resmin sıkıştırılmış hâli | `kodlar` (2 sayı) |
| **Çözücü** | Koddan resmi geri kurar | `inverse_transform` |

Bu yapının yapay zekadaki adı **otokodlayıcı** (autoencoder). PCA bunun en basit hâli.
Görsel üreten büyük modeller de bu ikiliyi kullanır: görseli önce küçük bir koda sıkıştırır,
bütün işi o kodun üstünde yapar, en sonda geri kurar.

---

## Adım 4 — Kaç sayı yeter?

```python
sira = 1
for boyut in [1, 2, 5, 10, 40, 100]:
    pca_dene = PCA(n_components=boyut)
    pca_dene.fit(resimler)
    kod_dene = pca_dene.transform(resimler)
    geri_dene = pca_dene.inverse_transform(kod_dene)
    plt.subplot(1, 6, sira)
    plt.imshow(geri_dene[0].reshape(28, 28), cmap="gray_r")
    plt.title(boyut)
    plt.axis("off")
    sira = sira + 1
plt.show()
```

Döngü her turda yeni bir PCA kuruyor; tek fark `n_components`. Her turda aynı A'yı (ilk
font) sıkıştırıp geri kuruyor ve bir kutuya çiziyor. Başlık, kaç sayı kullanıldığı.

- **1 ve 2 sayı:** "ortalama bir A". Fontun kendine özgü hiçbir şeyi yok.
- **5 ve 10 sayı:** kalınlık ve genel biçim geliyor, kenarlar hâlâ yumuşak.
- **40 ve 100 sayı:** asıl A'dan gözle ayırt edilmiyor.

Bir JPEG dosyasının "kalite" ayarı da aynı dengeyi kurar: daha az sayı, daha küçük
dosya, daha bulanık resim. Sıkıştırma **bilgi kaybettirir**; ne kadar kaybedileceği bir karar.

Peki 2 sayı bu kadar kötüyse neden 2'de kalıyoruz? Çünkü **2 sayı bir harita demek**:
kâğıda çizebiliriz.

---

## Adım 5 — Harita: her A bir nokta

```python
renkler = {"serif": "red", "sans": "blue", "mono": "green", "el yazısı": "purple"}

sira = 0
for nokta in kodlar:
    tur = turler[sira]
    plt.scatter(nokta[0], nokta[1], color=renkler[tur])
    sira = sira + 1

plt.xlabel("kodun 1. sayısı")
plt.ylabel("kodun 2. sayısı")
plt.show()
```

- Her A'nın 2 sayılık kodunu bir **nokta** olarak çiziyoruz. Bu haritaya **gizli uzay** (latent
  space) denir: "gizli", çünkü eksenlerinin adı yok.
- `renkler` her türe bir renk veren bir sözlük: kırmızı serifli, mavi serifsiz, yeşil mono, mor el yazısı
  (yalnızca 2 font: haritada 2 nokta). `renkler[tur]` sözlükten o türün rengini alır: `renkler["serif"]` → `"red"`.
- Döngü her A'nın noktasını alıyor; `sira` ile aynı sıradaki türü buluyoruz (`turler[sira]`).
  Bu kez `sira` 0'dan başlıyor, çünkü listede sıra 0'dan başlar (`subplot`'taki kutular ise 1'den).
- `plt.scatter` bir nokta koyar (Konu 4). `xlabel` ve `ylabel` eksen adları.

**Ne görüyoruz?** Kırmızılar (serifli) ile maviler (serifsiz) **karışık**. Harita serifli ile
serifsizi ayırmadı. Ama noktalar rastgele de değil: solda ve sağda iki büyük öbek var. PCA A'ları
başka bir şeye göre dizmiş. Neye göre olduğunu Adım 7'de haritanın kendisini "çizerek" göreceğiz.

Konu 4'teki gibi eksenlerin adı yok. Bu iki yönü PCA kendisi buldu: 136 A'nın **en çok
hangi bakımdan** birbirinden farklı olduğunu.

---

## Adım 6 — Haritada bir nokta seç, bir A üret

```python
nokta = [[0, 0]]
yeni = pca.inverse_transform(nokta)

plt.imshow(yeni[0].reshape(28, 28), cmap="gray_r")
plt.show()
```

- `[[0, 0]]`: içinde **tek bir nokta** olan bir liste. `transform` gibi `inverse_transform`
  da her zaman bir liste ister; tek nokta da olsa köşeli parantez içinde (Konu 4'teki
  `pca.transform([vektor])` gibi).
- Cevap da liste içinde gelir: `yeni[0]`.

Bu A, 136 fontun **hiçbirinde yok.** Haritanın ortasındaki bir noktadan geldi. İşte bu
konunun fikri:

> **Üretmek**, öğrenilmiş bir haritada bir nokta seçip oradan geri kurmaktır.

**Denemeler:**

- `[[4, 4]]`, `[[-4, -4]]`, `[[4, -4]]`: haritanın farklı köşelerinden farklı A'lar.
- `[[20, 20]]`: haritanın **çok dışı**. Harf dağılıyor, zemin koyulaşıyor. Orada hiç veri
  yoktu; harita oranın neye benzediğini bilmiyor. Görsel üreticiler de eğitim verisinden çok
  uzak isteklerde tuhaflaşır.

---

## Adım 7 — Haritanın eksenleri: iki yönde yürü

Haritanın ortasından (0, 0) geçen iki çizgi üzerinde yürüyoruz. Önce **soldan sağa**:

```python
sira = 1
for x in [-4, -2, 0, 2, 4]:
    yeni = pca.inverse_transform([[x, 0]])
    plt.subplot(1, 5, sira)
    plt.imshow(yeni[0].reshape(28, 28), cmap="gray_r")
    plt.axis("off")
    sira = sira + 1
plt.show()
```

- İkinci sayı 0'da sabit, birinci sayı −4'ten 4'e gidiyor: haritanın yatay ekseni boyunca beş durak.
- Her durakta Adım 6'daki işi yapıyoruz: `[[x, 0]]` noktasından bir A geri kuruyoruz.

Soldan sağa A **eğiliyor**: solda dik, sağda italik. Şimdi **yukarıdan aşağı**:

```python
sira = 1
for y in [4, 2, 0, -2, -4]:
    yeni = pca.inverse_transform([[0, y]])
    plt.subplot(1, 5, sira)
    plt.imshow(yeni[0].reshape(28, 28), cmap="gray_r")
    plt.axis("off")
    sira = sira + 1
plt.show()
```

- Bu kez birinci sayı 0'da sabit, ikinci sayı 4'ten −4'e: dikey eksen.
- `y` neden 4'ten başlıyor? Haritada yukarısı büyük `y`; yukarıdan aşağı yürüyoruz.

Yukarıdan aşağı A **inceliyor**: yukarıda kalın, aşağıda ince. En alttaki A'nın zemini griye
dönüyor: PCA orada bazı piksellere "eksi mürekkep" veriyor. Düz çizgilerle çalışan basit
haritamız ince A'ları o kadar iyi kuramıyor.

**Ne öğrendik?** Kimse PCA'ya "eğiklik" ya da "kalınlık" demedi. 136 A'ya bakıp en çok bu iki
bakımdan farklılaştıklarını **kendisi buldu**. Adım 5'teki iki öbek: solda dik A'lar, sağda
eğik A'lar.

Serifli ile serifsizin ayrılmaması da anlaşıldı: hem serifli hem serifsiz fontların dik ve
eğik hâlleri var. PCA bizim kategorilerimize değil, **pikseller** arasındaki en büyük farka
bakıyor; o fark da eğiklik çıktı.

### Bu bir tasarım aracı

Haritanın bir eksenini kaydırmak bir **özelliği ayarlamak** demek: bir "eğiklik" düğmesi,
bir "kalınlık" düğmesi. Değişken fontlar (variable fonts) da kalınlığı ve eğikliği böyle
sürgülerle ayarlatır. Fark: orada eksenleri tasarımcı belirler, burada model veriden buldu.

---

## Adım 8 — İki font arasında yürümek

```python
dik = fontlar.index("Liberation Serif Regular")
egik = fontlar.index("Lato Black Italic")
bas = kodlar[dik]
son = kodlar[egik]
ok = son - bas

sira = 1
for oran in [0, 0.25, 0.5, 0.75, 1]:
    ara = bas + oran * ok
    yeni = pca.inverse_transform([ara])
    plt.subplot(1, 5, sira)
    plt.imshow(yeni[0].reshape(28, 28), cmap="gray_r")
    plt.title(oran)
    plt.axis("off")
    sira = sira + 1
plt.show()
```

- `fontlar.index("...")`: bir elemanın listedeki sırasını verir. "Liberation Serif Regular"
  dik, ince, serifli; "Lato Black Italic" kalın, eğik, serifsiz.
- `bas` ve `son`: iki fontun A'larının haritadaki noktaları (ikişer sayı).
- `ok = son - bas`: baştan sona giden ok. Konu 4'ün Isınma 2'sindeki çıkarmanın aynısı
  (`kral - erkek`).
- `oran * ok`: oku kısaltır. `oran` 0.5 ise okun yarısı.
- `bas + oran * ok`: baştan başlayıp okun `oran` kadarını yürü.
- `[ara]`: `ara` zaten iki sayı; köşeli parantez onu Adım 6'daki `[[x, y]]` gibi tek noktalık
  bir listeye koyar.

| `oran` | Nerede |
|---|---|
| 0 | baştasın (`bas`) |
| 0.5 | tam ortada |
| 1 | sondasın (`son`) |

Ortadaki üç A, iki fontun arasındaki **ara formlar**; hiçbiri gerçek bir font değil. Buna
**ara değerleme** (interpolation) diyoruz: haritada iki nokta arasında yürümek.

Dürüst olalım: bizim haritamız basit (PCA, yalnızca 2 sayı), o yüzden ara formlar iki
harfin üst üste binmiş, bulanık hâli gibi görünüyor. Görsel üreten büyük modellerin haritası
çok daha zengin; orada iki yüz, iki ürün ya da iki üslup arasında yürüyünce gerçekten yeni,
inandırıcı biçimler çıkar.

---

## Bonus — Başka bir harf

Adım 1'in ilk hücresinde `veri["A"]` yerine `veri["g"]` yaz ve hücreleri **Adım 1'den
başlayarak** sırayla yeniden çalıştır. Adım 2'yi atlama: atlarsan hata çıkmaz ama PCA hâlâ A'ları
öğrenmiş olur ve harita A'nın haritası kalır.

Küçük **g**'nin iki ünlü biçimi var:

- **İki katlı g:** üstte bir halka, altta kapalı ikinci bir halka (çoğu serif fontta).
- **Tek katlı g:** üstte bir halka, altta açık bir kanca (çoğu sans fontta ve el yazısında).

Adım 7'nin soldan sağa yürüyüşünde g'nin bu iki biçimi arasında bir geçiş görüyor musun? Harita bu kez
neyi "en önemli fark" diye seçmiş? Sonra `veri["a"]` (o da iki katlı / tek katlı olabilir)
ve `veri["R"]` dene.

---

## Bu konunun büyük resmi: görsel üreticiler bunu nasıl yapıyor?

Bugün yaptığımız şey, görsel üreten modellerin (Konu 7'den itibaren kullanacaklarımızın)
temelindeki fikrin küçük bir modeli:

| Bizim defterde | Görsel üreticide |
|---|---|
| 136 A harfi | yüz milyonlarca görsel |
| 784 piksel | milyonlarca piksel |
| 2 sayılık kod | binlerce sayılık kod |
| PCA (düz çizgilerle sıkıştırır) | çok katmanlı bir sinir ağı (eğri yollarla sıkıştırır) |
| haritada noktayı biz seçiyoruz | noktayı yazdığın yönerge (prompt) seçiyor |

Yönerge yazınca olan şey özetle: model yönergeyi Konu 4'teki gibi bir vektöre çeviriyor,
o vektöre uyan bir kodu haritada adım adım arıyor ve en sonda o koddan görseli geri kuruyor.
"Adım adım arama" kısmını Konu 7'de konuşacağız: model rastgele bir başlangıç noktasından
(gürültüden) başlıyor ve her adımda yönergeye biraz daha yaklaşıyor.

---

## Defterin bölümleri

| Adım | Ne yaptık | Elimizde ne oluştu |
|---|---|---|
| Isınma | Bir sayı tablosunu resim olarak çizdik | `arti` |
| 1 | 136 fontun A'sını yükleyip çizdik | `resimler`, `fontlar`, `turler` |
| 2 | Her A'yı 2 sayıya sıkıştırdık | `pca`, `kodlar` |
| 3 | 2 sayıdan A'yı geri kurduk | `geri` |
| 4 | 1–100 sayıyla geri kurmayı karşılaştırdık | — |
| 5 | A'ların haritasını çizdik | harita |
| 6 | Haritadan yeni bir A ürettik | `yeni` |
| 7 | Haritanın iki ekseni boyunca yürüdük | 10 A |
| 8 | İki font arasında yürüdük | 5 A |
| Bonus | g, a ve R harfleri | — |

Derste kendi başına çalışacağın defter: `alistirma.ipynb`. Önce aynı klasörde yeni bir adla
kopyala, kopyada çalış. Anahtar istemez. R harfleriyle çalışıyor ve iki bölümü var:

- **Bozuk kodlar:** beş kısa hücre. Bazıları hata mesajı veriyor, biri sessizce yanlış sonuç
  yazıyor; üstlerinde ne yapmaları gerektiği yazıyor.
- **Kendi başına:** `BOSLUK` yazan yerleri doldurduğun sorular. Doldurmadığın boşluk
  `NameError: name 'BOSLUK' is not defined` verir. Her sorunun üstünde doğru çıktı yazılı.

Bu iki bölüm vizedeki kod sorularının biçiminde: bozuk kodu düzeltmek ve boşluk doldurmak.

---

## Sık karşılaşılan hatalar ve mesajlarını okumak

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `TypeError: Invalid shape (784,) for image data` | 784 sayıyı tek sıra hâlinde çizmeye çalıştın | `.reshape(28, 28)` ekle |
| `ValueError: cannot reshape array of size 784 into shape (28,)` | `reshape`'e tek sayı verdin | İki sayı: `reshape(28, 28)` |
| `NotFittedError: This PCA instance is not fitted yet` | `transform` ya da `inverse_transform`'u `fit`'ten önce çalıştırdın | Önce `pca.fit(resimler)` |
| `ValueError: Expected 2D array, got 1D array instead` | `inverse_transform`'a tek köşeli parantezle nokta verdin: `[0, 0]` | Liste içinde liste: `[[0, 0]]` |
| `ValueError: num must be an integer with 1 <= num <= 8, not 0` | `subplot`'ta kutu numarası 0'dan başladı | Sayaç 1'den başlamalı: `sira = 1` |
| `ValueError: n_components=200 must be between 0 and min(n_samples, n_features)=136` | 136 resimle en fazla 136 sayıya inilebilir | Daha küçük bir sayı seç |
| `FileNotFoundError: ... 'veri/harfler.npz'` | Defterin kopyası konu klasörünün dışında | Kopya `06-uretmek-ne-demek` klasöründe durmalı |
| `KeyError: 'B is not a file in the archive'` | Dosyada yalnızca A, a, g ve R var | Bu dört harften birini seç |
| `ValueError: 'Times' is not in list` | `fontlar.index` listede olmayan bir ad aldı | `for ad in fontlar: print(ad)` ile adları alt alta yazdır, birini birebir kopyala |
| `NameError: name '...' is not defined` (ör. `pca`, `PCA`, `kodlar`, `plt`) | Bir hücreyi atladın ya da çekirdek yeniden başladı (`plt` Isınma'da alınıyor) | Hücreleri baştan sırayla çalıştır |
| Adım 5'te `IndexError: list index out of range` | Sayaç `sira = 1` ile başladı | Bu döngüde `sira = 0`: liste sırası 0'dan başlar |
| Bonus'ta hata yok ama harfler hâlâ A gibi | Harfi değiştirdikten sonra Adım 2 (`fit`) yeniden çalıştırılmadı | Adım 1'den başlayıp Adım 2 dahil sırayla çalıştır |
| Bütün resimler tek kutuya üst üste çiziliyor | Döngüde `sira = sira + 1` satırı eksik | Satırı döngünün içine, en alta ekle |

---

## Kendini dene

Cevaplar notun en sonunda. Önce kendin düşün.

1. 28 × 28 piksellik bir resim kaç sayıdır? Renkli olsaydı (her piksel için R, G, B) kaç sayı olurdu?
2. Adım 2'de her A'yı 2 sayıya indirdik. Bir arkadaşın "o zaman 136 A'yı 272 sayıyla
   saklayabiliriz" diyor. Eksik olan ne?
3. Adım 4'te 100 sayıyla geri kurulan A aslından ayırt edilmiyordu. O hâlde neden haritayı
   100 sayıyla çizmiyoruz?
4. Adım 6'da `[[0, 0]]` noktasından çıkan A hiçbir fontta yok. Bu A'yı "kim tasarladı"?
5. Adım 6'da `[[20, 20]]` noktasından kurulan A dağılıyor. Neden?
6. Adım 8'de `oran` 0.5 iken nerede durursun? `oran` 1.5 yapsan ne olur?
7. Bir görsel üreticiye "kedi ile köpeğin tam ortası bir hayvan" dersen model ne yapmaya
   çalışır? Bu konunun hangi adımı buna benziyor?

---

## Bu konuda öğrendiklerin

- **Resim = sayı tablosu.** Her piksel bir sayı; 28 × 28 bir harf 784 sayı.
- **Sıkıştır ve geri kur.** Kodlayıcı resmi küçük bir koda sıkıştırır, çözücü koddan geri
  kurar. Sıkıştırma bilgi kaybettirir; kayıp, kodun boyuna bağlı.
- **Gizli uzay (harita).** Kodların oluşturduğu harita. Eksenlerinin adı yok ama anlamı
  var: bizde eğiklik ve kalınlık çıktı. Model bu eksenleri veriden kendisi buldu.
- **Üretmek.** Haritada bir nokta seçip oradan geri kurmak. Verinin bol olduğu bölgelerde
  inandırıcı, verinin olmadığı bölgelerde bozuk sonuç çıkar.
- **Ara değerleme.** İki nokta arasında yürümek: iki örneğin arasındaki ara formlar.

## Bu konunun tek cümlesi

> Üretmek, öğrenilmiş bir haritada bir nokta seçip oradan geri kurmaktır.

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **Piksel** | Bir resmin en küçük karesi; siyah-beyaz resimde bir sayı, renkli resimde üç sayı (R, G, B) |
| **`imshow`** | Bir sayı tablosunu resim olarak çizen komut |
| **`reshape`** | Sayıların dizilişini değiştirmek: 784 sayıyı 28 × 28 tabloya dizmek |
| **`.shape`** | Bir NumPy dizisinin boyutları: `(136, 784)` = 136 satır, 784 sütun |
| **Sıkıştırmak** | Bir şeyi daha az sayıyla anlatmak; bilgi kaybettirir |
| **Kod** | Sıkıştırılmış hâl; bizde her A için 2 sayı |
| **Kodlayıcı / çözücü** | Sıkıştıran parça (`transform`) / geri kuran parça (`inverse_transform`) |
| **Otokodlayıcı (autoencoder)** | Kodlayıcı ile çözücüyü birlikte öğrenen model; PCA en basit hâli |
| **Gizli uzay (latent space)** | Kodların oluşturduğu harita; "gizli" çünkü eksenlerinin adı yok |
| **Ara değerleme (interpolation)** | Haritada iki nokta arasında yürümek; ara formları üretmek |
| **`fontlar.index(...)`** | Bir elemanın listedeki sırasını veren komut |
| **Serifli / serifsiz / mono** | Tırnaklı / tırnaksız / her harfi eşit genişlikte yazı karakteri (dosyada `serif`, `sans`, `mono`) |

## Ödev

`odevler/odev6.md` (puansız). Konu 7'nin ilk oturumu vizenin sözlü teyidine ayrıldığı için
gösterimi Konu 8'in başında, Konu 7'nin ödeviyle birlikte. İki parça:

1. Kendi seçtiğin bir harfle (g, a ya da R) haritayı, iki eksen boyunca yürüyüşü ve iki font
   arasındaki yürüyüşü çıkar. İki cümle: yürürken harfte ne değişiyor, harita neyi "en önemli
   fark" diye seçmiş?
2. Adım 6'daki noktayı değiştirerek **en garip** A'yı bul; noktasını ve neden garip olduğunu yaz.

## Vize

Bu konu bitince vize verilir: evde yapılır, **yapay zeka yasak**, ardından derste kısa bir
sözlü teyit. Kapsam Konu 1–6. Soru biçimleri: kavram soruları, kod okuma, bozuk kodu
düzeltme ve boşluk doldurma (son ikisi alıştırma defterlerindeki gibi).

## Sonraki konu

**Konu 7 — Görsel üretimi.** Bugün haritada noktayı biz seçtik ve geri kurduk. Konu 7'de
gerçek bir görsel üreticiye yönerge yazacağız: noktayı yönerge seçecek. Gürültüden
adım adım temizlenen görseli farklı adım sayılarıyla karşılaştıracak, tohum, stil ve ışıkla
kontrollü deneyler yapacağız.

---

## Kendini dene — cevaplar

1. 784 sayı. Renkli olsaydı her piksel için 3 sayı: 784 × 3 = 2352.
2. **PCA'nın kendisi.** 2 sayılık kod tek başına bir şey anlatmaz; geri kurmak için PCA'nın
   136 A'dan öğrendiklerine (ortalama A ve iki yön) ihtiyaç var. Çözücü olmadan kod işe yaramaz.
   Bir de 2 sayıdan geri kurulan A bulanık: asıl A'yı değil, ona benzeyen bir A'yı saklıyoruz.
3. 100 sayıyı kâğıda çizemeyiz; harita 2 sayı ister. Ama 100 sayılık bir "harita" da vardır:
   gerçek modeller öyle çalışır. Yalnızca biz onu göremeyiz.
4. Kimse tek başına. PCA 136 fontu tasarlayanların işinden bir harita çıkardı; o noktayı
   sen seçtin. Görsel üreticilerin telif tartışması da buradan doğuyor (Konu 7).
5. `[[20, 20]]` haritanın çok dışında; orada hiç font yok. Harita oraları "tahmin ediyor" ve
   tahmin gerçek A'lara benzemiyor. Verinin olmadığı yerde üretilen şey güvenilmez.
6. `oran` 0.5: tam ortada. `oran` 1.5: sondan da öteye, aynı yönde yarım ok daha (`bas + 1.5 * ok`). Lato Black
   Italic'ten bile daha kalın ve eğik bir A çıkar; çok uzağa gidersen bozulur (Adım 6'daki
   `[[20, 20]]` gibi).
7. "Kedi" ile "köpek" arasındaki bir noktayı arar: Adım 8'deki ara değerlemenin aynısı. Büyük
   modellerin haritası zengin olduğu için sonuç inandırıcı bir "ara hayvan" olabilir.
