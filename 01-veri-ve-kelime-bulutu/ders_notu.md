# Konu 1 — Veriyi Kodla İşlemek ve Kelime Bulutu

Bu not konunun özetidir; kavram slaytlarından sonra defterle (`ders.ipynb`) **aynı
sırada** ilerler. Derste kaçırdığın bir yer olursa buradan oku, sonra defterde o adımın
hücrelerini çalıştır. Derste anlatılanlardan biraz daha uzun: her adımda **neden** o
adımı attığımızı, atmazsak ne olduğunu ve en sık karşılaşacağın hata mesajlarını da yazdık.

**Bu konunun sorusu:** Bir kafenin görsel kimliğini yenileyeceksin. Elinde
müşterilerin yazdığı 30 yorum var. Tasarıma başlamadan önce bilmek istediğin şey:
**müşteriler bu kafeyi nasıl anlatıyor?** 30 yorumu gözle okuyabilirsin; ama 3000
yorum olsaydı? Bu yüzden kelimeleri **kodla sayacağız**.

**Konunun sonunda elinde:** kendi ürettiğin bir kelime bulutu, en sık geçen kelimelerin
listesi ve aynı sonucun çubuk grafiği. Hepsi defterin içinde, hücrelerin altında görünür.

**Kurulum ve çalıştırma:** bu konunun kütüphaneleri (`wordcloud`, `matplotlib`) `gita3111`
klasöründeki `pyproject.toml` dosyasında yazılı. Dersten önce bir kez terminalde `gita3111`
klasöründe `uv sync` çalıştır; bu, `gita3111` klasöründe `.venv` adında bir ortam kurar. Sonra:

1. VS Code'da `ders.ipynb`'yi aç.
2. Sağ üstten **çekirdek** (kernel) olarak `.venv` seç.
3. Hücrelere sırayla tıklayıp **Shift + Enter** ile çalıştır.

Her hücre bir öncekinin oluşturduğu değişkeni kullanır. Bir hücreyi atlarsan sonraki
hücre `NameError` verir; geri dönüp atladığını çalıştır.

**Notu nasıl kullanmalısın:** Kod bloklarını okurken yanında defterdeki aynı hücreyi
çalıştır. Arada **Kendini dene** kutuları var; önce kendin cevapla, sonra notun sonundaki
cevaplara bak. Bir cevabı yanlış bulduysan o adımı bir kez daha oku.

---

## Konunun haritası

Tek bir defter yazıyoruz. Dosyayı **bir kez** okuyoruz; her adım bir öncekinin ürettiği
şeyi alıp yeni bir şey üretiyor:

```
dosya ──► metin ──► kelimeler ──► sayac ──► kelime bulutu
                        │               │
                (temizlik, durak kelime) └──► most_common ──► çubuk grafik
```

| Bölüm | Adımlar | Ne öğreniyorsun |
|---|---|---|
| Isınma | — | Sözlükten anahtarla okuma, `return`'ün yeri |
| Veriyi içeri almak | 1 | Dosya yolu, dosya okuma, `utf-8` |
| Veriyi temizlemek | 2 | Bölme, noktalama, Türkçe küçültme |
| Saymak ve sıralamak | 3–4 | Elle sözlükle sayaç; aynı işi yapan hazır araç `Counter` ve `most_common` |
| Sonucu anlamlı kılmak | 5 | Durak kelimeler |
| Görselleştirmek | 6 | Kelime bulutu |
| Derinleşme | 7–8 | Bulutun göremedikleri; aynı sonucun çubuk grafiği |

Bu konu bir derste bitmeyebilir. Bitmezse sonraki derste defteri açıp kaldığımız adıma
kadar hücreleri yeniden sırayla çalıştırırız; değişkenler (`metin`, `kelimeler`, `sayac`,
`anlamli`) yeniden oluşur.

---

## Isınma: geçen dönemin iki hatası

Defterin en başında iki küçük bozuk fonksiyon var. Bu konunun tamamı sözlüğe dayandığı
için önce bu ikisini düzeltiyoruz.

### Tamir 1 — Sözlük anahtarla açılır

```python
def puani_getir(ogrenci):
    return ogrenci[1]

print(puani_getir({"ad": "Deniz", "puan": 85}))
```

Hücreyi çalıştırınca hata mesajının son satırı:

```
KeyError: 1
```

`ogrenci[1]` yazan kişi aklında bir **liste** canlandırıyor: "ad birinci, puan ikinci,
o zaman puan 1 numarada". Ama `ogrenci` bir sözlük; sözlükte sıra numarası yoktur.
Python `1` diye bir **anahtar** arar, bulamaz: `KeyError: 1`.

Doğrusu `ogrenci["puan"]`:

```python
def puani_getir(ogrenci):
    return ogrenci["puan"]

print(puani_getir({"ad": "Deniz", "puan": 85}))
```

Çıktı `85`. Bu konuda yazacağımız sayaç da bir sözlük olacak; aynı hatayı orada
`sayac[0]` olarak göreceksin.

### Tamir 2 — `return` nerede durur?

```python
def topla(sayilar):
    toplam = 0
    for sayi in sayilar:
        toplam = toplam + sayi
        return toplam

print(topla([10, 20, 30]))
```

`return` fonksiyonu **o anda** bitirir. Burada `return` döngünün içinde olduğu için
fonksiyon ilk sayıyı ekler eklemez çıkar: `topla([10, 20, 30])` 60 değil **10** verir.

Bu hatanın kötü yanı: **hata mesajı yok.** Kod çalışır, sadece yanlış sonuç verir. Doğrusu
`return`'ü bir girinti sola, döngü bittikten sonraya almak:

```python
def topla(sayilar):
    toplam = 0
    for sayi in sayilar:
        toplam = toplam + sayi
    return toplam

print(topla([10, 20, 30]))
```

> **Kural:** Bir şeyi *biriktiriyorsan* (toplam, liste, sözlük) `return` döngünün
> **dışında** olur. Döngünün içinde `return` ancak "aradığımı buldum, gerisine bakmama gerek
> yok" dediğin durumlarda doğrudur.

### Hata mesajı nasıl okunur?

Bu konu boyunca çok hata mesajı göreceksin. Defterde hepsi hücrenin altında, aynı biçimde
çıkar. Örneğin dosya adını yanlış yazarsan (`kafe-yorumlari` yerine `kafe_yorumlari`):

```
FileNotFoundError                         Traceback (most recent call last)
Cell In[1], line 1
----> 1 with open("veri/kafe_yorumlari.txt", encoding="utf-8") as dosya:
      2     metin = dosya.read()

FileNotFoundError: [Errno 2] No such file or directory: 'veri/kafe_yorumlari.txt'
```

1. **En alttan başla.** Son satır iki parça: hatanın **türü** (`FileNotFoundError`) ve
   **açıklaması** (böyle bir dosya ya da klasör yok).
2. **Oka bak.** `---->` işareti hücrenin hangi satırında patladığını gösterir
   (`line 1`).
3. **Tırnak içindekine bak.** Açıklamada tırnak içinde bir değer varsa (burada dosya
   yolu, `KeyError`'da aranan anahtar), çoğu zaman ipucu tam oradadır.

> **Kendini dene 1:** `topla([5, 5, 5])` bozuk hâliyle ne döndürür? Hata mesajı alır mısın?

---

## Kod dosyayı nerede arıyor?

```py
open("veri/kafe-yorumlari.txt")
```

Bu yol **göreli** bir yoldur: "bulunduğum klasörün içindeki `veri` klasörüne gir,
oradaki dosyayı aç" demek. Peki "bulunduğum klasör" hangisi?

Defter, **kendi durduğu klasörde** çalışır. `ders.ipynb` `01-veri-ve-kelime-bulutu`
klasöründe durduğu için Python dosyayı
`01-veri-ve-kelime-bulutu/veri/kafe-yorumlari.txt` olarak arar ve bulur.

| Defter nerede duruyor | Python dosyayı nerede aradı | Sonuç |
|---|---|---|
| `gita3111/01-veri-ve-kelime-bulutu/` | `gita3111/01-veri-ve-kelime-bulutu/veri/kafe-yorumlari.txt` | Çalışır |
| Masaüstüne kopyalanmış | `Masaüstü/veri/kafe-yorumlari.txt` | `FileNotFoundError` |

Hangi klasörde çalıştığını bilmiyorsan bir hücrede sor:

```py
import os
print(os.getcwd())    # "current working directory": şu an çalıştığım klasör
```

> "No such file or directory" hatasının sebebi neredeyse her zaman ya budur ya da yolda
> bir yazım hatasıdır: `kafe-yorumlari.txt` yerine `kafe_yorumlari.txt` gibi.

**Mutlak yol** ise diskin kökünden başlayan tam yoldur (`C:/Users/...` ya da
`/home/...`). Her yerden çalışır ama başkasının bilgisayarında çalışmaz; çünkü onun
kullanıcı adı ve klasörleri farklıdır. Bu yüzden derste göreli yol kullanıyoruz.

> **Kendini dene 2:** `ders.ipynb`'yi masaüstüne kopyalayıp orada açtın. Adım 1'in hücresi
> çalışır mı? Neden?

## Adım 1 — Dosyayı aç

```python
with open("veri/kafe-yorumlari.txt", encoding="utf-8") as dosya:
    metin = dosya.read()

print(len(metin))
print(metin[:150])
```

Satır satır:

- **`with open(...) as dosya:`** Dosyayı açar ve `dosya` adıyla kullanmamızı sağlar.
  `with` bloğu bitince dosyayı **kendisi kapatır**. Açık unutulan dosya, özellikle
  yazarken, içeriğin diske yazılmamasına yol açabilir.
- **`dosya.read()`** Dosyanın tamamını **tek bir yazı** olarak okur. Sonuç `metin`
  değişkeninde.
- **`encoding="utf-8"`** Dosyadaki baytların hangi kurala göre harfe çevrileceğini
  söyler. Bizim dosyalarımız `utf-8` ile kaydedildi.
- Başka bir metinle denemek istersen değiştireceğin tek yer, tırnak içindeki dosya yolu.
  Dosyayı defterde **yalnızca burada** okuyoruz; sonraki bütün adımlar `metin`'den
  türetilir.

`encoding` yazmazsan ne olur? macOS ve Linux'ta çoğu zaman bir şey olmaz, çünkü
varsayılan zaten `utf-8`. Ama **Windows'ta** Python başka bir kural kullanır ve
şunu görürsün:

```
Ders Ã§alÄ±ÅŸmak iÃ§in en sevdiÄŸim yer.
```

Hata mesajı bile yok; sadece bozuk harfler. Bazı dosyalarda ise
`UnicodeDecodeError` hatası alırsın. İkisinin de çaresi aynı: `encoding="utf-8"`.
Sınıfta herkesin bilgisayarı farklı olduğu için bunu **her zaman** yazıyoruz.

**Dilimleme.** `metin[:150]` "baştan 150 karakter" demek. Köşeli parantezin içindeki
iki nokta, "şuradan şuraya" anlamına gelir:

```py
print(metin[:4])       # baştan 4 karakter  → "Ders"
print(metin[5:13])     # 5'ten 13'e kadar   → "çalışmak"
```

Sayma sıfırdan başlar ve sondaki sayı **dahil değildir**: `metin[5:13]` 5, 6, ... 12
numaralı karakterleri verir. Dilimleme listelerde de aynı çalışır; birazdan
`kelimeler[:8]` ile ilk sekiz kelimeye bakacağız.

Çıktının ilk satırı `2078`: elimizde artık **`metin`** var, 2078 karakterlik, tek
parça, uzun bir yazı. Bu yazıda 30 satır var, her satır bir yorum.

> **Kendini dene 3:** `metin[:1]` ne verir? `metin[0]` ile farkı var mı?

## Adım 2 — Kelimelere ayır ve temizle

Tek parça metinle kelime sayamayız. Önce parçalara ayırıyoruz:

```python
kelimeler = metin.split()
print(len(kelimeler))
print(kelimeler[:8])
```

`metin.split()` metni boşluklardan (ve satır sonlarından) bölüp bir **liste** verir.
Bir değerin arkasına nokta koyarak verdiğimiz bu tür komutlar (`.split()`, `.lower()`,
`.replace()`) o değerin kendi araçlarıdır. Bu konuda birkaçını daha göreceğiz.

Çıktı:

```
298
['Ders', 'çalışmak', 'için', 'en', 'sevdiğim', 'yer.', 'Sessiz,', 'her']
```

Altıncı ve yedinci kelimeye bak: `'yer.'` noktayla, `'Sessiz,'` virgülle yapışık ve
büyük harfle başlıyor. Python için `'Sessiz,'`, `'Sessiz'`, `'sessiz.'` ve `'sessiz'`
**dört ayrı kelime**.

Bu küçük bir kusur gibi görünür; değildir. Bu yorumlarda "sessiz" kelimesi 8 kez
geçiyor, ama bu dört farklı yazılışa dağılmış durumda. Temizlemeden sayarsak tam
yazılışıyla `sessiz` yalnızca **1** kez görünür. Birazdan göreceğin gibi "sessiz" bu
verinin en önemli kelimesi; temizlik yapmasaydık asıl bulguyu hiç görmeyecektik.

Toplamda ham bölmede 224 farklı "kelime" var; temizledikten sonra 196 kalıyor. Aradaki
28 kelime aslında aynı kelimenin noktalama ya da büyük harf yüzünden ayrı sayılmış
kopyaları.

İki ayrı sorunla uğraşıyoruz.

### Sorun 1 — Büyük ve küçük harf

`Sessiz` ile `sessiz` şu an iki ayrı kelime. Hepsini küçültmek gerekir; ama Türkçede
`.lower()` tek başına yetmez:

```python
print("İnternet".lower() == "internet")
print("Işık".lower())
```

```
False
işık
```

İki ayrı sorun var:

- Büyük **İ** küçülürken Python, harfi "i + üstüne nokta işareti" olarak iki parçaya
  ayırıyor. Ekranda `internet` gibi görünür, ama aslında 9 karakterdir ve `internet`
  ile **eşit değildir**.
- Büyük **I** ise noktasız **ı** yerine noktalı **i** olur: `Işık` → `işık`.

Python bu harfleri İngilizce kuralına göre küçültüyor; İngilizcede noktasız ı yok.

Bu gerçekten sayacı bozuyor mu? Yorumlarda "internet" 4 kez geçiyor: üçü cümle
başında `İnternet`, biri cümle ortasında `internet,`. Sadece `.lower()` kullanırsak
sayaç bunu iki ayrı kelime olarak tutar: biri 3, biri 1. Ekranda ikisi aynı görünür;
en sık kelimeler listesinde "internet" 4 yerine 3 ile daha aşağıda çıkar ve neden
olduğunu anlayamazsın.

Çözüm, önce bu iki harfi kendimiz çevirmek, sonra küçültmek. Her satır tek iş yapıyor:

```python
temiz = metin.replace("I", "ı")
temiz = temiz.replace("İ", "i")
temiz = temiz.lower()
```

- **İlk satır:** `metin`'deki her büyük I'yı noktasız ı yap, sonucu `temiz`'e koy.
- **İkinci satır:** `temiz`'deki her büyük İ'yi i yap, sonucu yine `temiz`'e koy.
- **Üçüncü satır:** geri kalan her şeyi küçült.

Sıra önemli: `.lower()` **en sonda**. Önce çağırsaydık İ çoktan iki parçaya
bölünmüş olurdu, `.replace("İ", "i")` onu bulamazdı.

Sonucu **yeni bir değişkene**, `temiz`'e koyduk. `metin` olduğu gibi duruyor; ona ileride
ihtiyacımız olabilir.

### Sorun 2 — Noktalama

`sessiz` ile `sessiz,` de hâlâ iki ayrı kelime. Çözüm: noktalama işaretlerini
**boşluğa çevirmek**, sonra yeniden bölmek:

```python
for isaret in ".,;:!?'()-":
    temiz = temiz.replace(isaret, " ")

kelimeler = temiz.split()
print(kelimeler[:8])
```

- Tırnak içindeki yazı noktalama işaretlerinin listesi; `for isaret in ...` onu
  **karakter karakter** gezer: önce nokta, sonra virgül, ...
- Listenin içinde kesme işareti (`'`) de var: `8'de` gibi yazılışlar için.
- `kelimeler` değişkenine **yeni**, temiz listeyi koyuyoruz; eski ham liste gitti.
  Bundan sonra `kelimeler` hep bu temiz liste.

**Neden silmiyoruz da boşluğa çeviriyoruz?** Yorum yazan insanlar her zaman
noktadan sonra boşluk bırakmaz:

```py
print("yer.Sessiz".replace(".", ""))     # yerSessiz   ← yapışık, anlamsız bir kelime
print("yer.Sessiz".replace(".", " "))    # yer Sessiz  ← iki ayrı kelime
```

Fazladan boşluk sorun değil: `.split()` art arda gelen boşlukları tek boşluk gibi
görür.

**Sık hata: sonucu değişkene geri koymamak.** Şu kod hiçbir şey değiştirmez:

```py
metin = "Sessiz ve sakin."
metin.replace(".", " ")
print(metin)               # Sessiz ve sakin.   ← nokta hâlâ orada
```

`.replace()` metnin kendisini değiştirmez, **yeni bir metin üretir**. Üretilen yeni
metni bir yere koymazsan kaybolur. Doğrusu: `metin = metin.replace(".", " ")`.
Döngüde her turda `temiz = temiz.replace(...)` yazmamızın sebebi bu. Hata mesajı
vermeyen bir hata olduğu için dikkat ister.

### Temiz liste

Hücrenin son satırı `print(kelimeler[:8])`'in çıktısı:

```
['ders', 'çalışmak', 'için', 'en', 'sevdiğim', 'yer', 'sessiz', 'her']
```

Baştaki listeyle karşılaştır: noktalama gitti, hepsi küçük harf. Kelime sayısı
değişmedi (298): hiçbir kelimeyi atmadık, sadece yazılışlarını birleştirdik. Değişen,
**farklı** kelime sayısı.

> **Kendini dene 4:** Dosyadaki metin yalnızca `Işıklandırma SICAK, ortam sakin.` olsaydı,
> temizlik hücrelerinden sonra `temiz` ne olurdu? `kelimeler` kaç kelime olurdu?

## Hatırlatma — Sözlük: anahtar ve değer

Saymaya başlamadan önce, sayacı tutacağımız yapıyı hatırlayalım.

```py
renkler = ["bordo", "mercan"]
renkler[0]           # liste sırayla numaralanır → "bordo"

sayac = {"sessiz": 8, "priz": 5}
sayac["sessiz"]      # sözlük anahtarla açılır → 8
sayac[0]             # HATA: 0 diye bir anahtar yok
```

Son satırın hata mesajı:

```
KeyError: 0
```

`KeyError` "böyle bir anahtar yok" demek; iki noktadan sonra gelen şey Python'un
aradığı anahtar. Mesajı bu gözle okursan sebebi hemen görürsün: "0 diye bir anahtar
aramışım." Aynı hata, olan bir kelimeyi yanlış yazdığında da gelir:

```
KeyError: 'Sessiz'
```

Sözlükteki anahtar `'sessiz'` (küçük harf); biz `'Sessiz'` aradık. Temizliği neden
saymadan **önce** yaptığımızı bu da gösteriyor.

Bir anahtarın sözlükte olup olmadığını hata almadan sormanın yolu `in`:

```py
print("sessiz" in sayac)     # True
print("wifi" in sayac)       # False
```

Bir de sözlüğü döngüyle gezerken ne gezdiğini bil:

```py
for kelime in sayac:
    print(kelime, sayac[kelime])
```

`for kelime in sayac` sözlüğün **anahtarlarını** gezer. Değere ulaşmak için yine
anahtarla açarsın: `sayac[kelime]`.

> **Sözlükten veri anahtarla alınır, sayıyla değil.**

> **Kendini dene 5:** `fiyatlar = {"kahve": 45, "çay": 30}` için `fiyatlar["çay"]`,
> `fiyatlar[1]` ve `"latte" in fiyatlar` ne verir?

## Adım 3 — Elle say: sözlükle sayaç

Önce işi **elle** yapıyoruz ki sayacın nasıl çalıştığını görelim. Bir sonraki adımda
Python'un hazır aracı aynı işi tek satırda yapacak; ama içinde ne olduğunu bilmeden
hazır araca güvenmek zor.

```python
sayac = {}
for kelime in kelimeler:
    if kelime in sayac:
        sayac[kelime] = sayac[kelime] + 1
    else:
        sayac[kelime] = 1

print(len(sayac))
print(sayac["sessiz"])
```

```
196
8
```

196 farklı kelime var; `sessiz` 8 kez geçiyor.

Döngüyü küçük bir örnekle adım adım izleyelim. `kelimeler` şu olsun:
`["sessiz", "priz", "sessiz"]`

| Tur | `kelime` | Sözlükte var mı? | Ne yapıldı | Tur sonunda `sayac` |
|---|---|---|---|---|
| başlangıç | — | — | — | `{}` |
| 1 | `"sessiz"` | yok | `else`: 1 olarak eklendi | `{"sessiz": 1}` |
| 2 | `"priz"` | yok | `else`: 1 olarak eklendi | `{"sessiz": 1, "priz": 1}` |
| 3 | `"sessiz"` | var | `if`: 1 artırıldı | `{"sessiz": 2, "priz": 1}` |

İlk görüşte kelimeyi 1 olarak ekliyoruz, sonraki görüşlerde artırıyoruz.

**Neden `if / else` gerekli?** Hiç görmediğimiz bir kelimeyi doğrudan artırmaya
çalışırsak:

```py
sayac = {}
sayac["sessiz"] = sayac["sessiz"] + 1
```

```
KeyError: 'sessiz'
```

Sağ taraf önce çalışır: Python `sayac["sessiz"]` değerini okumaya çalışır, ama sözlükte
henüz öyle bir anahtar yok.

### Sayaçta sık yapılan üç hata

| Yazdığın | Ne olur | Neden |
|---|---|---|
| `sayac = []` | `TypeError: list indices must be integers or slices, not str` | Boş **liste** kurdun. Liste yalnızca sayıyla açılır; sen kelimeyle açmaya çalıştın. Boş sözlük `{}` ile kurulur |
| `sayac = {}` döngünün **içinde** | Hata yok, ama her kelime 1 görünür | Sözlük her turda sıfırlanır. Başlangıç değeri döngüden **önce** kurulur |
| `else` kısmını unutmak | `KeyError: 'ders'` | İlk görüşte kelime sözlükte henüz yok; artırılacak bir değer de yok |

İkinci satırdaki hata, ısınmadaki `return` hatası gibi **sessiz** bir hatadır: kod
çalışır ama sonuç yanlıştır. Sonucun makul görünüp görünmediğine her zaman bak:
"her kelime bir kez geçmiş" makul değil.

> **Kendini dene 6:** `["kahve", "çay", "kahve", "kahve"]` listesi için döngü bitince
> `sayac` ne olur? `sayac["çay"]` kaç?

## Adım 4 — Hazır araçla say ve sırala: `Counter`

Adım 3'te elle yazdığımız sayacın aynısını Python'un hazır aracı `Counter` tek satırda
kurar:

```python
from collections import Counter

sayac = Counter(kelimeler)
print(sayac["sessiz"])
```

```
8
```

- **`from collections import Counter`** Python'un içinde gelen `collections`
  kütüphanesinden `Counter` aracını alıyoruz. Ayrıca kurmak gerekmez.
- **`Counter(kelimeler)`** listeyi gezer ve her kelimenin kaç kez geçtiğini sayar;
  Adım 3'teki altı satırlık döngünün yaptığı iş.
- **Sonuç yine 8.** Adım 3'te elle bulduğumuz sayının aynısı. İşte elle yazmanın
  getirisi: hazır aracın ne yaptığını artık biliyorsun ve sonucunu kendi sayınla
  doğrulayabiliyorsun.
- `Counter` bir sözlük gibi çalışır: anahtar kelime, değer kaç kez geçtiği. Yine
  **anahtarla** açılır: `sayac["sessiz"]`. Yeni `sayac`, Adım 3'teki sözlüğün yerine geçer.

**Bir fark:** Adım 3'teki sözlük, içinde olmayan bir kelimede `KeyError` verir.
`Counter` ise hata vermez, `0` der; hiç geçmeyen kelime 0 kez geçmiştir. Bunu defterin
sonundaki Bonus'ta göreceksin.

### En sık geçenler: `most_common`

Sözlük kendiliğinden "en çok geçen başta" diye sıralı değil; kelimeler, ilk
görüldükleri sırayla durur. `Counter`'ın bir becerisi daha var: en sık geçenleri sıralar.

```python
for kelime, adet in sayac.most_common(20):
    print(adet, kelime)
```

- **`sayac.most_common(20)`** en sık 20 kelimeyi verir, en çoktan aza.
- **`for kelime, adet in ...`** Döngüde bu kez **iki değişken** var. Her turda bir
  ikili gelir: kelime ve adedi. Python ikiliyi kendisi böler; ilki `kelime`'ye,
  ikincisi `adet`'e girer.

| Tur | `kelime` | `adet` | Yazdırılan |
|---|---|---|---|
| 1 | `"için"` | `10` | `10 için` |
| 2 | `"sessiz"` | `8` | `8 sessiz` |
| 3 | `"var"` | `6` | `6 var` |

**Eşitlik olursa?** Aynı sayıda geçen kelimeler (ör. 5'er kez geçen `çalışmak`, `yer`,
`priz`) metinde ilk görüldükleri sırayla gelir.

İnternette sıralama için `sorted` ve `lambda` kullanan kalıplar görebilirsin. Bu
derste kullanmıyoruz: `lambda` konumuz değil ve o kalıplar sayıyı `x[1]` gibi **sıra
numarasıyla** açar; ısınmada düzelttiğimiz alışkanlık tam olarak buydu.
`most_common` ve `for kelime, adet in` aynı işi adlarla yapar.

> **Kendini dene 7:** Yukarıdaki döngünün ilk turunda `kelime` ve `adet` nedir? Metinde
> hiç geçmeyen bir kelime için `sayac["latte"]` ne verir? Adım 3'teki elle kurduğumuz
> sözlükte ne verirdi?

## Adım 5 — Durak kelimeleri ele

Adım 4'ün çıktısında ilk 10 satıra bak:

```
10 için
8 sessiz
6 var
6 bir
5 çalışmak
5 yer
5 priz
5 ama
5 çok
4 her
```

Aradaki **için, var, bir, ama, çok, her** bu kafe hakkında hiçbir şey söylemiyor. Her
Türkçe metinde en üste çıkarlar ve anlamlı kelimeleri aşağı iterler. Bu, verinin değil
dilin özelliği: bir şarkı sözünde, bir haberde ya da bir tezde de aynı kelimeler
başta olur. Bunlara **durak kelime** (İngilizcesi *stopword*) denir.

Durak kelime listesi hazır bir dosya: `veri/turkce-durak-kelimeler.txt`. Adım 1'deki
gibi okuyup Adım 2'deki gibi bölüyoruz:

```python
with open("veri/turkce-durak-kelimeler.txt", encoding="utf-8") as dosya:
    durak_metni = dosya.read()

durak_kelimeler = durak_metni.split()
print(len(durak_kelimeler))
print(durak_kelimeler[:10])
```

```
171
['acaba', 'ama', 'ancak', 'artık', 'asla', 'aslında', 'ayrıca', 'az', 'bana', 'bazen']
```

Dosyada her satırda bir kelime var, toplam 171. Açıp içine bak; bu bir kara kutu değil,
sıradan bir metin dosyası. `durak_kelimeler` düz bir **liste**.

Sonra kelime listesinden durak kelimeleri ve iki harfli artıkları atıp **anlamlı**
kelimeleri ayrı bir listeye alıyoruz:

```python
anlamli = []
for kelime in kelimeler:
    if kelime not in durak_kelimeler and len(kelime) > 2:
        anlamli.append(kelime)

print(len(kelimeler), len(anlamli))
```

```
298 221
```

- **`anlamli = []`** boş bir liste kuruyoruz; koşulu geçen her kelimeyi içine
  ekleyeceğiz (`.append`).
- **`kelime not in durak_kelimeler`** "kelime listede yoksa" demek. `in`'in tersi.
- **`len(kelime) > 2`** bir-iki harfli artıkları da atar. Noktalamayı boşluğa
  çevirdiğimizde `8'de` gibi yazılışlardan `8` ve `de` gibi parçalar kalabilir.
- **`and`** iki koşulun **ikisi de** doğruysa kelimeyi listeye ekler.
- Çıktı: 298 kelimeden 221'i kaldı; 77 kelime elendi. `kelimeler` olduğu gibi duruyor.

Yeni listeyi `Counter`'a veriyoruz ve bu kez ilk 10'a bakıyoruz:

```python
sayac = Counter(anlamli)
for kelime, adet in sayac.most_common(10):
    print(adet, kelime)
```

```
8 sessiz
5 çalışmak
5 yer
5 priz
4 internet
4 öğrenci
3 ders
3 ortam
3 güzel
3 uygun
```

`sayac` artık durak kelimeleri elenmiş sayaç; Adım 4'tekinin yerine geçer.

İki listeyi yan yana koyalım:

| Sıra | Eleme öncesi | Eleme sonrası |
|---|---|---|
| 1 | için (10) | **sessiz (8)** |
| 2 | sessiz (8) | **çalışmak (5)** |
| 3 | var (6) | **yer (5)** |
| 4 | bir (6) | **priz (5)** |
| 5 | çalışmak (5) | **internet (4)** |
| 6 | yer (5) | **öğrenci (4)** |
| 7 | priz (5) | ders (3) |
| 8 | ama (5) | ortam (3) |
| 9 | çok (5) | güzel (3) |
| 10 | her (4) | uygun (3) |

Artık listenin başı anlamlı.

**İşte bulgu:** müşteriler kafeyi kahvesiyle değil, **sessiz bir çalışma yeri**
olarak anlatıyor. İlk altı kelimenin hepsi bu fikre bağlanıyor: sessiz, çalışmak, yer,
priz, internet, öğrenci. Hatta "priz" ve "internet" gibi **altyapı** kelimelerinin bu
kadar üstte olması, müşterinin bu kafeyi bir çalışma masası gibi kullandığını
gösteriyor.

Yeni kimliği tasarlayacak biri için bu önemli bir karar noktası: afişte buharı tüten
bir fincan mı olmalı, yoksa masada açık bir laptop ve bir priz mi? Menü panosunun
yanında "her masada priz" yazması, yeni bir kahve çeşidinden daha çok müşteri
getirebilir. Kelime bulutunu işe yarar yapan adım budur.

**Durak kelime listesi bir karardır.** Hazır listeyi kullanmak zorunda değilsin.
Kendi metninde hiçbir şey söylemeyen bir kelime sürekli üste çıkıyorsa (ör. her
gönderide geçen marka adı), onu da elemek isteyebilirsin. Tersine, listede olup senin
için anlamlı olan bir kelime varsa (ör. bir şarkıda sürekli tekrar eden "sen") elemek
bulguyu yok edebilir. Hangi kelimeleri elediğini bil ve söyle.

> **Sınır:** `bahçe`, `bahçesi`, `bahçede` ayrı kelimeler olarak sayılıyor. Kod Türkçenin
> eklerini bilmiyor; bu yüzden bazı konular olduğundan küçük görünür. Bunun ne kadar
> fark yarattığını Adım 7'de ölçeceğiz.

> **Kendini dene 8:** `len(kelime) > 2` koşulunu `len(kelime) > 3` yapsaydık, ilk 10
> listesinden hangi kelime(ler) kaybolurdu?

## Adım 6 — Kelime bulutu

```python
from wordcloud import WordCloud

bulut = WordCloud(width=1200, height=800, background_color="white")
bulut.generate_from_frequencies(sayac)
bulut.to_image()
```

- **`from wordcloud import WordCloud`** `wordcloud` kütüphanesinden `WordCloud` aracını
  alıyoruz. Kütüphane bulunamazsa bu satır `ModuleNotFoundError` verir (çekirdek olarak
  `.venv` seçili mi?).
- **`WordCloud(...)`** boş bir bulut **tuvali** hazırlar: boyutu 1200×800 piksel,
  arka planı beyaz. Henüz içinde kelime yok.
- **`generate_from_frequencies(sayac)`** kelimeleri yerleştirir. Girdi olarak doğrudan
  **sayacımızı** (`Counter`, durak kelimeleri elenmiş hâlini) veriyoruz; kelimenin
  boyutu sayaçtaki değeriyle orantılı.
- **`bulut.to_image()`** bulutu resim olarak verir. Hücrenin **son satırı** bir resim
  olunca defter onu hücrenin altında gösterir.

Görseli dosya olarak kaydetmek istersen (ödevde gerekecek) `bulut.to_image()` satırının
üstüne bir satır eklersin: `bulut.to_file("kelime-bulutu.png")`. Dosya, defterin durduğu klasörde oluşur.

**Neden kendi sayacımızı veriyoruz?** Kütüphanenin, ham metni doğrudan alan bir
`generate(metin)` komutu da var. Ama o kendi temizliğini yapar ve bu temizlik
İngilizceye göre ayarlıdır: İngilizce durak kelimeleri eler, Türkçeleri tanımaz, büyük
İ sorununu bilmez. Kendi sayacımızı verdiğimizde neyin sayıldığı **bizim kontrolümüzde**
olur.

Kütüphanenin kendi yazı tipi ç, ğ, ı, İ, ö, ş, ü harflerini gösterir. Başka bir yazı
tipi seçmek istersen `WordCloud(..., font_path="yazı tipi dosyasının yolu")` yazarsın;
seçtiğin yazı tipinde Türkçe harfler yoksa harfler kutu gibi çıkar.

**Bulutun tasarımı.** `WordCloud(...)` parantezinin içine başka ayarlar da yazabilirsin;
hücreyi değiştirip yeniden çalıştır, sonucu karşılaştır:

| Ayar | Ne yapar | Örnek değerler |
|---|---|---|
| `background_color` | Arka plan rengi | `"white"`, `"black"`, `"#1a1a2e"` |
| `colormap` | Renk paleti | `"magma"`, `"viridis"`, `"cividis"`, `"Pastel1"` |
| `max_words` | En fazla kaç kelime | `25` |
| `prefer_horizontal` | Yatay kelime oranı | `1` (hepsi yatay), `0.5` |

Hepsi görünüşü değiştirir; hangi kelimenin büyük olduğunu değiştirmez.

### Bulutu okurken

Kelime bulutunda **yalnızca boyut** veri taşır. Kelimenin yeri, rengi ve yönü
rastgeledir; hücreyi her çalıştırdığında değişebilir. "sessiz ortada, demek ki en
önemli" ya da "priz yeşil, demek ki olumlu" gibi okumalar yanlıştır. Bir tasarımcı
olarak bunu bilmen önemli: izleyici her görsel farkın bir anlamı olduğunu varsayar.
Bulutu bir sunumda kullanırsan, bu yanlış okumayı engellemek senin işin.

### Bulutta sık yaşanan iki sorun

**Sayaç yerine listeyi vermek:**

```py
bulut.generate_from_frequencies(kelimeler)
```

Hata mesajı uzun (kütüphanenin içinden geliyor), ama en alt satırı:

```
AttributeError: 'list' object has no attribute 'items'
```

"Liste nesnesinde `items` diye bir şey yok." Kütüphane bir **sözlük** bekliyor
(kelime → sayı); sen ona kelime **listesi** verdin. Mesajdaki `'list'` sözcüğü ipucu:
yanlış türde bir şey vermişsin.

**Boş sayaç vermek:**

```
ValueError: We need at least 1 word to plot a word cloud, got 0.
```

"Çizmek için en az 1 kelime lazım, 0 geldi." Sayacın boş: ya dosya boş, ya da eleme
her şeyi silmiş. `print(len(sayac))` ile kontrol et.

> **Kendini dene 9:** Adım 5'i atlayıp buluta Adım 3'teki (elemesiz) sayacı verseydin,
> bulutta en büyük kelime hangisi olurdu?

> **Kendini dene 10:** Bulut hücresini iki kez çalıştırdın; ikinci bulutta "priz" sağ
> üstte ve mor, birincide sol altta ve sarıydı. Bir şey mi değişti?

---

## Adım 7 — Bulutun söylemediği iki şey

Bu adım ve bir sonraki, derinleşme bölümüdür.

Buraya kadarki bulgumuz: "müşteriler kafeyi sessiz bir çalışma yeri olarak anlatıyor."
Bir tasarım kararını bir kelime sayımına dayandırmadan önce iki soruyu sormalıyız.

### Soru 1 — Ekler sonucu değiştiriyor mu?

Adım 5'in sonundaki sınırı hatırla: `bahçe`, `bahçesi` ve `bahçede` ayrı sayılıyor.
Basit bir çözüm: içinde **aynı harfler geçen** kelimeleri toplamak. Temiz `kelimeler`
listesini kullanıyoruz (durak kelime elemesi burada önemli değil):

```python
aranan = "kahve"
bulunanlar = []
for kelime in kelimeler:
    if aranan in kelime:
        bulunanlar.append(kelime)

print(len(bulunanlar))
print(bulunanlar)
```

- **`aranan in kelime`** `in`'i bu kez bir **yazının içinde** kullanıyoruz: "`kahve`
  harfleri bu kelimenin içinde geçiyor mu?" `kahvesi`, `kahvenin` için cevap evet.
- Boş bir `bulunanlar` listesi kurup bulduğumuz her kelimeyi içine atıyoruz. Listenin
  uzunluğu (`len`) kaç kez geçtiğini verir.
- Listeyi de yazdırıyoruz: **neyi topladığını görmeden bir toplama güvenme.**

```
6
['kahvesi', 'kahve', 'kahve', 'kahvenin', 'kahveleri', 'kahveli']
```

`"kahve"` yerine başka kelimeler yazıp hücreyi yeniden çalıştırınca:

| Aranan | Tek başına (Adım 3) | İçinde geçenler | Bulunanlar |
|---|---|---|---|
| `sessiz` | 8 | 9 | 8 × `sessiz`, `sessizlik` |
| `kahve` | 2 | **6** | `kahvesi`, `kahve` ×2, `kahvenin`, `kahveleri`, `kahveli` |
| `bahçe` | 2 | 5 | `bahçesi`, `bahçede` ×2, `bahçe` ×2 |
| `priz` | 5 | 5 | 5 × `priz` |
| `ışık` | 2 | 3 | `ışık` ×2, `ışıklandırma` |

İki şey değişti:

- **Bahçe** tek başına 2 idi, toplayınca 5 oldu. Bulutta küçük görünen bahçe, aslında
  priz kadar sık konuşulan bir konu.
- **Kahve** tek başına 2 idi, toplayınca **6** oldu ve prizi geçti. Bulgumuz
  ("müşteri kahveden değil, çalışma ortamından söz ediyor") çöktü mü?

**Dikkat, bu yöntem de kusurlu.** `"çalış"` aratırsan `çalışmak`, `çalışmaya`,
`çalışırken` yanında `çalışanlar`'ı da (kafenin personeli) sayarsın. Başka bir konu olduğu
hâlde. Kısa bir parça çok şey yakalar, bazen de yanlış şeyi. `bulunanlar` listesini
yazdırmamızın sebebi bu.

### Soru 2 — Kelime hangi bağlamda geçiyor?

Sayı, bir kelimenin **kaç kez** geçtiğini söyler; **nasıl** geçtiğini söylemez. "Kahve
harika" ile "kahve fena değil" sayaç için aynı şeydir. Kahve sorusunu cevaplamak için
yorumların kendisini okumamız gerek; ama hepsini değil, yalnızca kahveden söz edenleri.

```python
for satir in temiz.splitlines():
    if "kahve" in satir:
        print(satir)
```

- **`temiz.splitlines()`** metni satırlarına böler. Dosyamızda her satır bir yorum.
  Temizlik satır sonlarına dokunmadı; `temiz` de 30 satır.
- **`"kahve" in satir`** yine yazının içinde arama: "bu parça satırın içinde geçiyor
  mu?" Böylece `kahvesi`, `kahveleri` gibi ekli hâlleri de yakalar.
- Neden `metin` değil de `temiz`? `temiz` küçültülmüş; `Kahve` ile başlayan cümleler ve
  `Işıklandırma` da bulunur. Noktalama gitmiş ama cümle hâlâ okunuyor.

Çıktı:

```
kahvesi fena değil ama asıl sebep ortam  sessiz ve sakin  saatlerce oturabiliyorsunuz 
kahve ortalama  tatlılar güzel  ama buraya ders çalışmaya geliyorum  o yüzden sorun değil 
kahve biraz pahalı ama saatlerce oturmana kimse bir şey demiyor 
cheesecake çok güzel  kahvenin yanına mutlaka deneyin 
kahveleri iyi  özellikle soğuk demleme  ama menü biraz kısa 
laptop ile gelenler çoğunlukta  kütüphane gibi ama kahveli 
```

Altı yorumu okuyunca tablo netleşiyor:

- Üçünde kahve **ılık** bir sözle geçiyor: "fena değil", "ortalama", "biraz pahalı".
  Üçü de hemen ardından asıl sebebi söylüyor: ortam, ders, saatlerce oturabilmek.
- Birinde asıl övülen **cheesecake**; kahve yalnızca yanında.
- Birinde kafe "kütüphane gibi ama kahveli" diye anlatılıyor: kahve bir **ek**, kimlik
  değil.
- Kahveyi doğrudan öven **tek** yorum var.

Bulgu çökmedi, **güçlendi**: müşteri kahveden söz ediyor, ama geliş sebebi o değil.
Sayı tek başına bunu söyleyemezdi; tersine, "kahve 6 kez geçiyor" yanıltıcı bir
cümle olurdu.

### Bir bulgu daha: ışık

Defterdeki sonraki hücre aynı döngü, bu kez `"ışık"` için:

```python
for satir in temiz.splitlines():
    if "ışık" in satir:
        print(satir)
```

```
laptop ile çalışmak için ideal  masalar geniş  ışık yeterli  müzik sessiz 
bahçe akşamları çok keyifli  ışıklandırma sıcak  ortam sakin 
içerisi biraz karanlık  kitap okumak için ışık yetmiyor  bahçe daha aydınlık 
```

Işık yalnızca 3 kez geçiyor; bulutta neredeyse görünmez. Ama bağlamında okununca
somut bir sorun çıkıyor: **iç mekân okumak için karanlık, bahçe aydınlık.** Müşteriler
bu kafeye çalışmak için geliyorsa, bu bir kenar notu değil. Kimlik yenilemesi
yalnızca logo ve afiş değildir; masa lambası, iç mekân aydınlatması ve bahçenin
kullanımı da bu işin parçası olabilir.

**Bu adımın dersi:** Sayma, **nereye bakacağını** söyler; ne bulacağını söylemez.
Sıklık listesi seni kahveye ve ışığa yönlendirir, asıl bulguyu ise yorumları okuyunca
bulursun. Veriyle çalışan her tasarımcı bu iki adımı birlikte atar.

> **Kendini dene 11:** Son hücrede `"ışık"` yerine `"müzik"` yazarsan iki yorum gelir. Kafenin
> kendi gönderilerinde ise "Hafta sonu canlı müzik var" yazıyor (`veri/kafe-gonderileri.txt`).
> Bu iki bilgi yan yana konunca bir tasarımcı için nasıl bir soru doğar?

## Adım 8 — Aynı sonuç, çubuk grafik olarak

Hazırlıktaki ilk defterde (`../00-hazirlik/ilk_defter.ipynb`) grafiği yalnızca verini
değiştirerek çalıştırmıştın; burada grafik kodunu satır satır yazıyoruz.

Kelime bulutu bir **izlenim** verir: "sessiz büyük, gerisi daha küçük." Ama "sessiz,
ikinci sıradakinden **ne kadar** fazla?" ya da "priz mi daha sık, internet mi?"
sorularını buluttan cevaplayamazsın; kelimelerin boyu harf sayısına göre de değişir.
Karşılaştırma için çubuk grafik daha doğru bir araçtır.

Önce çizilecek iki listeyi hazırlıyoruz. `sayac` Adım 5'ten hazır (durak kelimeler
elenmiş hâli):

```python
import matplotlib.pyplot as plt

etiketler = []
degerler = []
for kelime, adet in sayac.most_common(10):
    etiketler.append(kelime)
    degerler.append(adet)
```

Sonra çiziyoruz:

```python
plt.bar(etiketler, degerler, color="#4a6fa5")
plt.title("Müşteri yorumlarında en sık 10 kelime")
plt.ylabel("Kaç kez geçti")
plt.xticks(rotation=45)
plt.show()
```

Satır satır:

- **`import matplotlib.pyplot as plt`** Çizim araçlarını `plt` kısa adıyla alıyoruz.
  Bu kısaltma her yerde böyle kullanılır; internette gördüğün örnekler de `plt` der.
- **İki liste.** `plt.bar` iki ayrı liste ister: çubukların **adları** ve **boyları**.
  `most_common(10)` bize en sık 10 ikiliyi verir; döngü her turda gelen ikiliyi böler:
  kelime `etiketler`e, adedi `degerler`e eklenir.
- **`plt.bar(etiketler, degerler, color=...)`** Çubukları çizer. Renk, tasarım
  programlarından bildiğin onaltılık renk koduyla (`#4a6fa5`) verilebilir.
- **`plt.title`, `plt.ylabel`** Başlık ve dikey eksenin adı. Başlıksız ve eksen adı
  olmayan grafik, izleyiciye "ne ölçtüğümü tahmin et" demektir.
- **`plt.xticks(rotation=45)`** Alttaki kelimeleri 45 derece yatırır ki üst üste
  binmesinler.
- **`plt.show()`** Grafiği hücrenin altında gösterir.

Grafikte ilk bakışta görülen şey, bulutta görülmeyen şey: **sessiz (8)**, arkasından
gelen üç kelimeden (5'er) belirgin biçimde yukarıda; `çalışmak`, `yer` ve `priz` ise
tam olarak eşit. Bulut bunu sezdirir, grafik ölçer.

**Hangisini seçmelisin?** Bu bir tasarım kararı:

| Soru | Daha uygun görsel |
|---|---|
| "Bu metin genel olarak neyi anlatıyor?" (ilk izlenim, afiş, sunum açılışı) | Kelime bulutu |
| "Hangi konu ötekinden ne kadar önde?" (karar, rapor, karşılaştırma) | Çubuk grafik |

> **Kendini dene 12:** Grafikte en sık 10 değil 15 kelime göstermek için hangi satırda
> neyi değiştirirsin?

---

## Defterin bölümleri

Program `ders.ipynb`'de adım adım büyüyor; her adım bir öncekinin ürettiğini
kullanıyor. Dosyayı yalnızca Adım 1'de okuyoruz.

| Defterde | Ne yaptık | Elimizde ne oluştu |
|---|---|---|
| Isınma | İki tamir | — |
| Adım 1 | Dosyayı açtık | `metin` |
| Adım 2 | Kelimelere ayırdık (ham), sonra küçültüp noktalamayı attık, yeniden ayırdık | `temiz`, `kelimeler` |
| Adım 3 | Elle saydık (sözlükle) | `sayac` (sözlük) |
| Adım 4 | `Counter` ile saydık, `most_common` ile sıraladık | `sayac` (Counter) |
| Adım 5 | Durak kelimeleri eledik, anlamlı kelimeleri yeniden saydık | `durak_kelimeler`, `anlamli`, yeni `sayac` |
| Adım 6 | Bulutu çizdirdik | `bulut` |
| Adım 7 | Ekleri topladık, bağlamda okuduk | bulgu |
| Adım 8 | Çubuk grafik çizdik | `etiketler`, `degerler` |

Derste kendi başına dolduracağın alıştırma: `alistirma.ipynb`. Önce beş bozuk kod
(sırayla düzelt; hata mesajı okumak için iyi bir alıştırma), sonra boşluk doldurma
soruları. Soru tipleri vizeyle aynı. Defteri önce yeni bir adla kopyala, kopyada çalış.

Erken bitirirsen defterin sonundaki **Bonus**: Adım 1'deki dosya adını
`veri/kafe-gonderileri.txt` yap ve hücreleri yeniden sırayla çalıştır. Bu kez metin
müşterilerin değil, **kafenin kendi** gönderileri. Adım 3'teki `print(sayac["sessiz"])`
satırı `KeyError: 'sessiz'` verir: kafe kendi gönderilerinde "sessiz" kelimesini **hiç**
kullanmamış. Adım 4'teki aynı satır ise `0` yazar: elle kurduğumuz sözlük olmayan
kelimede hata verir, `Counter` 0 der. Hata veren hücreden sonrakileri tek tek
çalıştırmaya devam et; eleme
sonrası ilk sıralar **kahve (8), yeni (7), bugün (5), hafta (4), soğuk (3)**. Kafe
kendini kahveyle anlatıyor, müşteri sessizlikle. Yeni kimlik hangisini öne çıkarmalı?

---

## Sık karşılaşılan sorunlar

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `FileNotFoundError: ... No such file or directory` | Defter konu klasöründe değil ya da yolda yazım hatası var | Defteri `01-veri-ve-kelime-bulutu` içinden aç; yol `veri/...` ile başlamalı. Emin değilsen bir hücrede `import os` ve `print(os.getcwd())` |
| `NameError: name 'metin' is not defined` (ya da `kelimeler`, `sayac`...) | Önceki bir hücreyi çalıştırmadın ya da çekirdek yeniden başladı | Defterin başından itibaren hücreleri sırayla çalıştır |
| `ModuleNotFoundError: No module named 'wordcloud'` | Çekirdek olarak `.venv` seçili değil ya da `uv sync` yapılmadı | Sağ üstten çekirdeği `.venv` yap; olmadıysa terminalde `gita3111` klasöründe `uv sync` |
| `Ã§alÄ±ÅŸmak` gibi bozuk harfler ya da `UnicodeDecodeError` | `open(...)` içinde `encoding="utf-8"` yok | `encoding="utf-8"` ekle |
| `KeyError: 0` | Sözlüğü sayıyla açmaya çalıştın | Anahtarla aç: `sayac["sessiz"]`. (`Counter`'da hata vermez, sessizce `0` döner) |
| `KeyError: 'kelime'` | Sayaçta olmayan bir kelimeyi okumaya ya da artırmaya çalıştın | Sayarken `if / else`; okurken önce `in` ile kontrol |
| `TypeError: list indices must be integers or slices, not str` | Sayacı `[]` ile liste olarak kurdun | `sayac = {}` |
| `NameError: name 'Counter' is not defined` | `from collections import Counter` satırını çalıştırmadın | Adım 4'ün ilk hücresini çalıştır |
| Sayaçta `a`, `k`, `e` gibi tek harfler | `Counter(metin)`: metni bölmeden verdin, harfleri saydı | Önce kelimelere böl: `Counter(metin.split())` ya da `Counter(kelimeler)` |
| `ValueError: too many values to unpack (expected 2)` | `for kelime, adet in sayac:` yazdın; `most_common(...)` yok | İki değişkenli döngü ikili ister: `for kelime, adet in sayac.most_common(10):` |
| `AttributeError: 'list' object has no attribute 'items'` | Buluta sayaç yerine kelime listesi verdin | `generate_from_frequencies(sayac)` |
| `ValueError: We need at least 1 word ...` | Sayaç boş | Dosya dolu mu, eleme her şeyi silmiş mi? `print(len(sayac))` |
| Bulut görünmüyor | `bulut.to_image()` hücrenin son satırı değil | Görseli göstermek istediğin satırı hücrenin en sonuna koy |
| Bulutta harfler kutu (□□□) | `font_path=` ile seçtiğin yazı tipi Türkçe harfleri içermiyor | `font_path=` ayarını sil (kütüphanenin kendi yazı tipi Türkçe harfleri gösterir) ya da Türkçe harfli bir yazı tipi seç |
| Bulutta 3-5 kelime var | Metin çok kısa | Daha uzun bir metin kullan (ödevde en az 300 kelime) |
| Her kelime 1 kez sayılmış | `sayac = {}` döngünün içinde | Döngüden önceye al |
| Sayaçta `internet` iki kez görünüyor | Yalnızca `.lower()` kullandın | Önce I ve İ'yi `.replace` ile çevir, sonra `.lower()` |

---

## Bu konuda öğrendiklerin

- **Defterde hücreler sırayla çalışır.** Her hücre öncekinin değişkenini kullanır; dosyayı
  bir kez okur, sonra hep aynı değişkenlerle ilerlersin.
- **Dosya yolu, defterin durduğu klasöre göredir.** `FileNotFoundError` görürsen önce
  bunu kontrol et.
- **Dosyayı okurken `encoding="utf-8"` yaz.** Yazmazsan Windows'ta Türkçe harfler bozulur.
- **Temizlik saymadan önce gelir.** Noktalama ve büyük harf temizlenmezse aynı kelime
  birkaç farklı kelime gibi sayılır; bu veride asıl bulgu ("sessiz") kaybolurdu.
- **Türkçe küçültme özel iş.** `"İ".lower()` beklediğini vermez; önce İ ve I'yı kendin
  çevir.
- **`.replace()` metni değiştirmez, yeni metin üretir.** Sonucu değişkene geri koy.
- **Sözlük sayaçtır.** Anahtar kelimedir, değer kaç kez geçtiği. Anahtarla açılır,
  sayıyla değil.
- **`Counter` elle yazdığın sayacın hazır hâlidir.** `Counter(kelimeler)` sayar,
  `sayac.most_common(10)` en sık 10'u verir. Önce elle yazdın ki ne yaptığını bil.
- **`for kelime, adet in sayac.most_common(10):`** Her turda bir ikili gelir: kelime
  ve adedi.
- **Durak kelimeler elenmezse sonucu onlar kaplar.** Elenecek kelime listesi bir
  karardır.
- **Kelime bulutunda yalnızca boyut veri taşır.** Konum ve renk rastgeledir.
- **Sayma nereye bakacağını söyler; bulguyu bağlamda okuyarak bulursun.**
- **Karşılaştırma için çubuk grafik, genel izlenim için bulut.**

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **Defter (notebook)** | Kodun küçük parçalar (hücreler) hâlinde yazıldığı ve çalıştırıldığı dosya: `ders.ipynb` |
| **Hücre** | Defterde tek seferde çalışan kod parçası. Shift + Enter ile çalışır, çıktısı altında görünür |
| **Çekirdek (kernel)** | Defterin hücrelerini çalıştıran Python. Bu konuda `.venv` seçilir |
| **Göreli yol** | Çalıştığın klasörden başlayan dosya yolu (`veri/...`) |
| **Mutlak yol** | Diskin kökünden başlayan tam yol (`C:/Users/...`, `/home/...`) |
| **Kodlama (encoding)** | Dosyadaki baytların hangi kurala göre harfe çevrileceği. Bizde hep `utf-8` |
| **Dilimleme** | Bir yazının ya da listenin bir parçasını almak: `metin[:150]`, `kelimeler[:8]` |
| **Anahtar / değer** | Sözlükte aradığın şey (anahtar) ve karşılığında bulduğun şey (değer) |
| **Sayaç** | Her şeyin kaç kez geçtiğini tutan sözlük: `{"sessiz": 8, ...}` |
| **`Counter`** | Python'un hazır sayacı: `Counter(kelimeler)`. Sözlük gibi anahtarla açılır; olmayan kelimede hata vermez, `0` der |
| **`most_common`** | `Counter`'ın en sık geçenleri en çoktan aza veren becerisi: `sayac.most_common(10)` |
| **Durak kelime (stopword)** | Her metinde sık geçen ama bir şey anlatmayan kelime: ve, bir, için, ama |
| **Ek** | Kelimenin sonuna gelip onu değiştiren parça: kahve**si**, bahçe**de**. Kod ekleri bilmez; bu konuda "içinde geçen" diye yaklaşık olarak topladık |
| **Bağlam** | Bir kelimenin geçtiği cümle. Kelimenin **nasıl** kullanıldığını gösterir |
| **Hata mesajı (traceback)** | Python'un hatayı anlattığı metin. Aşağıdan yukarı okunur |
| **Sessiz hata** | Hata mesajı vermeyen ama yanlış sonuç üreten hata. En tehlikeli tür |

## Bu konunun tek cümlesi

> Sözlük, "kaç kere" sorusunun cevabını tutan yerdir; anahtarla açılır, sayıyla değil.

---

## Kendini dene — cevaplar

1. **10** döndürür. Hata mesajı almazsın; `return` döngünün içinde olduğu için ilk
   sayıyı ekleyip çıkar. Sessiz hata.
2. **Çalışmaz:** `FileNotFoundError`. Defter kendi durduğu klasörde (masaüstü) çalışır ve
   `Masaüstü/veri/kafe-yorumlari.txt` diye bir dosya yok. Defteri konu klasöründen aç.
3. `metin[:1]` → `"D"` (ilk karakter, yazı olarak). `metin[0]` da `"D"` verir. Farkı
   boş metinde görürsün: boş bir yazıda `[:1]` boş yazı verir, `[0]` hata verir. Bu
   konuda ikisi aynı işi görür.
4. `temiz` → `"ışıklandırma sıcak  ortam sakin "` (virgül ve nokta boşluğa döndüğü için
   fazladan boşluklar var). `kelimeler` **4** kelime olur:
   `['ışıklandırma', 'sıcak', 'ortam', 'sakin']`. `Işık` başındaki I noktasız ı oldu.
5. `fiyatlar["çay"]` → `30`. `fiyatlar[1]` → `KeyError: 1`. `"latte" in fiyatlar` →
   `False`.
6. `{"kahve": 3, "çay": 1}`. `sayac["çay"]` → `1`.
7. İlk turda `kelime` → `"için"`, `adet` → `10` (en sık kelime ve adedi).
   `sayac["latte"]` → `0`: `Counter` olmayan kelimede hata vermez. Adım 3'teki elle
   kurduğumuz sözlükte aynı satır `KeyError: 'latte'` verirdi.
8. İlk 10'dan yalnızca **yer** (3 harf) kaybolur; yerine 11. sıradaki `masalar` girer.
   Kısa ama anlamlı kelimeleri de atabileceğin için eşik de bir karardır.
9. **için** (10 kez). Elemesiz sayaçta en üstte o var (Adım 4'ün çıktısı); bulutta en
   büyük kelime de o olurdu. Ödevde göreceğin fark tam olarak bu.
10. **Hayır.** Konum ve renk her çalıştırmada rastgele seçilir; veri taşımaz. Değişmeyen
    tek şey kelimelerin boyutu, çünkü o sayaçtan geliyor.
11. Müşteriler bu kafeye sessizlik için geliyor ("çalışmak için yanlış günü seçmişim");
    kafe ise kendini canlı müzikle tanıtıyor. Soru şu: yeni kimlik iki kitleyi nasıl
    ayıracak? Örneğin canlı müzik gecelerinin önceden ve açıkça duyurulması, ya da
    çalışma alanıyla etkinlik alanının ayrılması. Bu bir kod sorusu değil, tasarım
    sorusu; ama onu soruya kod getirdi.
12. `for kelime, adet in sayac.most_common(10):` satırında `10` yerine `15` yaz. Başlığı da
    ("en sık 10 kelime") güncellemeyi unutma.

---

## Ödev

`odevler/odev1.md`: kendi seçtiğin bir metinle **iki** bulut üret (durak kelimeler
elenmeden ve elendikten sonra) ve aradaki farkı tek cümleyle yaz.

## Sonraki konu

Konu 2'de (`02-api-ile-konusmak`) kodla internete bağlanıp bir yapay zeka modeline soru
soracağız. Bunun için **Cloudflare hesabın ve anahtarın hazır olmalı**. Kurulum
yönergesinin 6. adımı (`../00-hazirlik/kurulum-yonergesi.md`). Hesabın yoksa
derste yanındaki arkadaşınla birlikte takip edersin; ama ödev için kendi hesabın
gerekiyor. Takıldıysan şimdiden söyle.
