# Konu 1 — Veriyi Kodla İşlemek ve Kelime Bulutu

Bu not konunun özetidir; ısınmadan sonra slaytlarla **aynı sırada** ilerler. Derste
kaçırdığın bir yer olursa buradan oku, sonra ilgili örnek dosyayı çalıştır. Derste
anlatılanlardan biraz daha uzun: her adımda **neden** o adımı attığımızı, atmazsak ne
olduğunu ve en sık karşılaşacağın hata mesajlarını da yazdık.

**Bu konunun sorusu:** Bir kafenin görsel kimliğini yenileyeceksin. Elinde
müşterilerin yazdığı 30 yorum var. Tasarıma başlamadan önce bilmek istediğin şey:
**müşteriler bu kafeyi nasıl anlatıyor?** 30 yorumu gözle okuyabilirsin; ama 3000
yorum olsaydı? Bu yüzden kelimeleri **kodla sayacağız**.

**Konunun sonunda elinde:** kendi ürettiğin bir kelime bulutu (`kelime-bulutu.png`),
en sık 20 kelimenin listesi (`sonuc.txt`) ve isteğe bağlı olarak aynı sonucun çubuk
grafiği (`kelime-grafik.png`).

**Kurulum:** bu konunun kütüphaneleri (`wordcloud`, `matplotlib`) klasördeki
`pyproject.toml` dosyasında yazılı. Terminalde bu konunun klasörüne gir
(`cd 01-veri-ve-kelime-bulutu`); ilk `uv run ...` komutu kütüphaneleri kendisi indirir.
Ders sırasında beklememek için dersten önce aynı klasörde bir kez `uv sync` çalıştır.

**Notu nasıl kullanmalısın:** Kod bloklarını okurken yanında örnek dosyayı çalıştır.
Arada **Kendini dene** kutuları var; önce kendin cevapla, sonra notun sonundaki
cevaplara bak. Bir cevabı yanlış bulduysan o adımı bir kez daha oku.

---

## Konunun haritası

Tek bir program yazıyoruz. Her adım bir öncekinin ürettiği şeyi alıp yeni bir şey
üretiyor:

```
dosya ──► metin ──► kelimeler ──► sayac ──► sirali ──► sonuc.txt
                        │                                  │
                  (temizlik, durak kelime)          kelime-bulutu.png
                                                    kelime-grafik.png
```

| Bölüm | Adımlar | Ne öğreniyorsun |
|---|---|---|
| Isınma | — | Sözlükten anahtarla okuma, `return`'ün yeri |
| Veriyi içeri almak | 0–1 | Dosya yolu, dosya okuma, `utf-8` |
| Veriyi temizlemek | 2 | Bölme, noktalama, Türkçe küçültme |
| Saymak ve sıralamak | 3–4 | Sözlükle sayaç, değere göre sıralama |
| Sonucu anlamlı kılmak | 5–6 | Durak kelimeler, dosyaya yazma |
| Görselleştirmek | 7 | Kelime bulutu |
| Derinleşme | 8–9 | Bulutun göremedikleri; aynı sonucun çubuk grafiği |

Bu konu bir derste bitmeyebilir. Bitmezse sonraki derse kaldığımız adımdan, o ana
kadar üretilen değişkenleri hatırlayarak başlarız (yukarıdaki şema tam da bunun için).

---

## Isınma: geçen dönemin iki hatası

`00_isinma.py` iki küçük bozuk fonksiyon içeriyor. Bu konunun tamamı sözlüğe
dayandığı için önce bu ikisini düzeltiyoruz. Dosyayı olduğu gibi çalıştırınca şunu
görürsün:

```
10
Traceback (most recent call last):
  File ".../ornekler/00_isinma.py", line 16, in <module>
    print(puani_getir({"ad": "Deniz", "puan": 85}))
          ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".../ornekler/00_isinma.py", line 6, in puani_getir
    return ogrenci[1]
           ~~~~~~~^^^
KeyError: 1
```

İlk satır `topla`'nın sonucu (60 olmalıydı); hata mesajı ise `puani_getir`'den geliyor.

### Tamir 1 — Sözlük anahtarla açılır

```python
def puani_getir(ogrenci):
    return ogrenci[1]
```

Fonksiyona verilen öğrenci `{"ad": "Deniz", "puan": 85}`.

`ogrenci[1]` yazan kişi aklında bir **liste** canlandırıyor: "ad birinci, puan ikinci,
o zaman puan 1 numarada". Ama `ogrenci` bir sözlük; sözlükte sıra numarası yoktur.
Python `1` diye bir **anahtar** arar, bulamaz: `KeyError: 1`.

Doğrusu `ogrenci["puan"]`. Bu konuda yazacağımız sayaç da bir sözlük olacak; aynı hatayı
orada `sayac[0]` olarak göreceksin.

### Tamir 2 — `return` nerede durur?

```python
def topla(sayilar):
    toplam = 0
    for sayi in sayilar:
        toplam = toplam + sayi
        return toplam
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
```

> **Kural:** Bir şeyi *biriktiriyorsan* (toplam, liste, sözlük) `return` döngünün
> **dışında** olur. Döngünün içinde `return` ancak "aradığımı buldum, gerisine bakmama gerek
> yok" dediğin durumlarda doğrudur.

### Hata mesajı nasıl okunur?

Bu konu boyunca çok hata mesajı göreceksin. Hepsi aynı biçimde okunur:

```
Traceback (most recent call last):
  File ".../ornekler/01_dosya_oku.py", line 4, in <module>
    with open("veri/kafe-yorumlari.txt", encoding="utf-8") as dosya:
         ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'veri/kafe-yorumlari.txt'
```

1. **En alttan başla.** Son satır iki parça: hatanın **türü** (`FileNotFoundError`) ve
   **açıklaması** (böyle bir dosya ya da klasör yok).
2. **Bir üste çık.** `line 4` hangi satırda patladığını, altındaki `^^^^` işaretleri de
   o satırın tam olarak hangi parçasında patladığını gösterir.
3. **Tırnak içindekine bak.** Açıklamada tırnak içinde bir değer varsa (burada dosya
   yolu, `KeyError`'da aranan anahtar), çoğu zaman ipucu tam oradadır.

> **Kendini dene 1:** `topla([5, 5, 5])` bozuk hâliyle ne döndürür? Hata mesajı alır mısın?

---

## Adım 0 — Kod dosyayı nerede arıyor?

```python
open("veri/kafe-yorumlari.txt")
```

Bu yol **göreli** bir yoldur: "bulunduğum klasörün içindeki `veri` klasörüne gir,
oradaki dosyayı aç" demek. Peki "bulunduğum klasör" hangisi?

Python bu dosyayı **komutu çalıştırdığın klasöre** göre arar; kod dosyasının durduğu
yere göre değil. Bu yüzden komutları hep konunun klasöründen
(`gita3111/01-veri-ve-kelime-bulutu`) çalıştırıyoruz: önce `cd 01-veri-ve-kelime-bulutu`,
sonra `uv run ornekler/...`.

Aynı kodu iki farklı yerden çalıştıralım:

| Komutu nereden çalıştırdın | Python dosyayı nerede aradı | Sonuç |
|---|---|---|
| `gita3111/01-veri-ve-kelime-bulutu/` | `gita3111/01-veri-ve-kelime-bulutu/veri/kafe-yorumlari.txt` | Çalışır |
| `gita3111/` | `gita3111/veri/kafe-yorumlari.txt` | `FileNotFoundError` |

İkinci satırda konu klasörüne girilmemiş; `gita3111`'in hemen içinde `veri` diye bir
klasör yok.

Kodun hangi klasörden çalıştığını bilmiyorsan sor:

```python
import os
print(os.getcwd())    # "current working directory": şu an çalıştığım klasör
```

Çıktının sonu `01-veri-ve-kelime-bulutu` ile bitmiyorsa, terminalde önce `cd` ile konu
klasörüne geç.

> "No such file or directory" hatasının sebebi neredeyse her zaman budur. Geri kalan
> durumlarda sebep genellikle yolda bir yazım hatasıdır: `kafe-yorumlari.txt` yerine
> `kafe_yorumlari.txt` gibi.

**Mutlak yol** ise diskin kökünden başlayan tam yoldur (`C:/Users/...` ya da
`/home/...`). Her yerden çalışır ama başkasının bilgisayarında çalışmaz; çünkü onun
kullanıcı adı ve klasörleri farklıdır. Bu yüzden derste göreli yol kullanıyoruz.

> **Kendini dene 2:** Terminalin `gita3111/01-veri-ve-kelime-bulutu/ornekler` klasöründe
> açık. `uv run 01_dosya_oku.py` yazarsan dosya bulunur mu? Neden?

## Adım 1 — Dosyayı aç

`01_dosya_oku.py`'nin ilk yarısı:

```python
# Adım 1 — Dosyayı aç, kelimelere böl
# Çalıştır: uv run ornekler/01_dosya_oku.py

with open("veri/kafe-yorumlari.txt", encoding="utf-8") as dosya:
    metin = dosya.read()

print(len(metin))
print(metin[:150])
```

Satır satır:

- **İlk iki satır** yorum: Python `#` ile başlayan satırları okumaz. Her örnek dosya
  böyle başlar: adımın adı ve dosyanın nasıl çalıştırılacağı.
- **`with open(...) as dosya:`** Dosyayı açar ve `dosya` adıyla kullanmamızı sağlar.
  `with` bloğu bitince dosyayı **kendisi kapatır**. Açık unutulan dosya, özellikle
  yazarken, içeriğin diske yazılmamasına yol açabilir.
- **`dosya.read()`** Dosyanın tamamını **tek bir yazı** olarak okur. Sonuç `metin`
  değişkeninde.
- **`encoding="utf-8"`** Dosyadaki baytların hangi kurala göre harfe çevrileceğini
  söyler. Bizim dosyalarımız `utf-8` ile kaydedildi.
- Başka bir metinle denemek istersen değiştireceğin tek yer, tırnak içindeki dosya yolu.

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

```python
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

Tek parça metinle kelime sayamayız. Önce parçalara ayırıyoruz; `01_dosya_oku.py`'nin
devamı:

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
print("İnternet".lower() == "internet")   # False
print("Işık".lower())                      # işık
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

Çözüm, önce bu iki harfi kendimiz çevirmek, sonra `.lower()` demek. Yeni dosya
`02_kelime_say.py`; okuma satırları `01` ile aynı:

```python
# Adım 2–3 — Temizle ve say
# Çalıştır: uv run ornekler/02_kelime_say.py

with open("veri/kafe-yorumlari.txt", encoding="utf-8") as dosya:
    metin = dosya.read()

temiz = metin.replace("I", "ı").replace("İ", "i").lower()   # .lower() en sonda
```

Sıra önemli: `.lower()` **en sonda**. Önce çağırsaydık İ çoktan iki parçaya
bölünmüş olurdu, `.replace("İ", "i")` onu bulamazdı.

`.replace(...).replace(...).lower()` gibi arka arkaya yazılan komutlar soldan sağa
çalışır; her biri bir öncekinin ürettiği yeni metinle çalışır.

Sonucu **yeni bir değişkene**, `temiz`'e koyduk. `metin` olduğu gibi duruyor; ona ileride
ihtiyacımız olabilir.

### Sorun 2 — Noktalama

`sessiz` ile `sessiz,` de hâlâ iki ayrı kelime. Çözüm: noktalama işaretlerini
**boşluğa çevirmek**, sonra bölmek:

```python
for isaret in ".,!?:;()[]\"'…-–—/":
    temiz = temiz.replace(isaret, " ")
kelimeler = temiz.split()
print(kelimeler[:8])
```

- Tırnak içindeki yazı noktalama işaretlerinin listesi; `for isaret in ...` onu
  **karakter karakter** gezer.
- `\"` tırnak işaretinin kendisi. Yazının sınırı da tırnak olduğu için önüne `\`
  koyuyoruz; "bu tırnak yazının sonu değil, içindeki bir karakter" demek.

**Neden silmiyoruz da boşluğa çeviriyoruz?** Yorum yazan insanlar her zaman
noktadan sonra boşluk bırakmaz:

```python
print("yer.Sessiz".replace(".", ""))     # yerSessiz   ← yapışık, anlamsız bir kelime
print("yer.Sessiz".replace(".", " "))    # yer Sessiz  ← iki ayrı kelime
```

Fazladan boşluk sorun değil: `.split()` art arda gelen boşlukları tek boşluk gibi
görür.

**Sık hata: sonucu değişkene geri koymamak.** Şu kod hiçbir şey değiştirmez:

```python
metin = "Sessiz ve sakin."
metin.replace(".", " ")
print(metin)               # Sessiz ve sakin.   ← nokta hâlâ orada
```

`.replace()` metnin kendisini değiştirmez, **yeni bir metin üretir**. Üretilen yeni
metni bir yere koymazsan kaybolur. Doğrusu: `metin = metin.replace(".", " ")`.
Döngüde her turda `temiz = temiz.replace(...)` yazmamızın sebebi bu. Hata mesajı
vermeyen bir hata olduğu için dikkat ister.

### Temiz liste

Döngünün ardından gelen `print(kelimeler[:8])` satırının çıktısı:

```
['ders', 'çalışmak', 'için', 'en', 'sevdiğim', 'yer', 'sessiz', 'her']
```

Baştaki listeyle karşılaştır: noktalama gitti, hepsi küçük harf. Kelime sayısı
değişmedi (298): hiçbir kelimeyi atmadık, sadece yazılışlarını birleştirdik. Değişen,
**farklı** kelime sayısı.

Bundan sonra hep bu temiz `kelimeler` listesiyle çalışıyoruz. Bütün örnek dosyalar aynı
okuma ve temizleme satırlarıyla başlar; dosyayı açınca bu satırları tanıyacaksın.

> **Kendini dene 4:** Dosyadaki metin yalnızca `Işıklandırma SICAK, ortam sakin.` olsaydı,
> temizlik satırlarından sonra `temiz` ne olurdu? `kelimeler` kaç kelime olurdu?

## Hatırlatma — Sözlük: anahtar ve değer

Saymaya başlamadan önce, sayacı tutacağımız yapıyı hatırlayalım.

```python
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

```python
print("sessiz" in sayac)     # True
print("wifi" in sayac)       # False
```

Bir de sözlüğü döngüyle gezerken ne gezdiğini bil:

```python
for kelime in sayac:
    print(kelime, sayac[kelime])
```

`for kelime in sayac` sözlüğün **anahtarlarını** gezer. Değere ulaşmak için yine
anahtarla açarsın: `sayac[kelime]`.

> **Sözlükten veri anahtarla alınır, sayıyla değil.**

> **Kendini dene 5:** `fiyatlar = {"kahve": 45, "çay": 30}` için `fiyatlar["çay"]`,
> `fiyatlar[1]` ve `"latte" in fiyatlar` ne verir?

## Adım 3 — Say

`02_kelime_say.py`'nin devamı:

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

```python
sayac = {}
sayac["sessiz"] = sayac["sessiz"] + 1
```

```
KeyError: 'sessiz'
```

Sağ taraf önce çalışır: Python `sayac["sessiz"]` değerini okumaya çalışır, ama sözlükte
henüz öyle bir anahtar yok.

Aynı işin kısa hâli (örnek dosyalarda uzun hâli kullanıyoruz; kısa hâli internette
çok göreceğin için burada):

```python
sayac = {}
for kelime in kelimeler:
    sayac[kelime] = sayac.get(kelime, 0) + 1
```

`sayac.get(kelime, 0)` şu demek: **varsa değerini ver, yoksa 0 ver.** Yoksa 0 + 1 = 1
olarak eklenir; varsa bir artırılır. `if / else` bloğunun tamamı tek satıra indi. İkisi
birebir aynı sonucu verir; istediğini kullan.

### Sayaçta sık yapılan üç hata

| Yazdığın | Ne olur | Neden |
|---|---|---|
| `sayac = []` | `TypeError: list indices must be integers or slices, not str` | Boş **liste** kurdun. Liste yalnızca sayıyla açılır; sen kelimeyle açmaya çalıştın. Boş sözlük `{}` ile kurulur |
| `sayac = {}` döngünün **içinde** | Hata yok, ama her kelime 1 görünür | Sözlük her turda sıfırlanır. Başlangıç değeri döngüden **önce** kurulur |
| `sayac.get(kelime) + 1` | `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'` | İkinci değeri (`0`) unuttun. Kelime yoksa `.get` "hiçbir şey" (`None`) verir; hiçbir şeye 1 eklenemez |

İkinci satırdaki hata, ısınmadaki `return` hatası gibi **sessiz** bir hatadır: kod
çalışır ama sonuç yanlıştır. Sonucun makul görünüp görünmediğine her zaman bak:
"her kelime bir kez geçmiş" makul değil.

> **Kendini dene 6:** `["kahve", "çay", "kahve", "kahve"]` listesi için döngü bitince
> `sayac` ne olur? `sayac["çay"]` kaç?

## Adım 4 — Değere göre sırala

Sözlük kendiliğinden "en çok geçen başta" diye sıralı değil; kelimeler, ilk
görüldükleri sırayla durur. En sık geçenleri görmek için.
`03_ilk_20.py`: `02`'nin okuma, temizleme ve sayma satırları aynen; sondaki iki `print`
yerine:

```python
sirali = sorted(sayac, key=sayac.get, reverse=True)   # değere göre; parantez yok
for kelime in sirali[:20]:
    print(sayac[kelime], kelime)
```

Parça parça:

- **`sorted(sayac)`** tek başına anahtarları **alfabetik** sıralar. Bize bu lazım değil.
- **`key=sayac.get`** "her kelimeyi, `sayac.get(kelime)` sonucuna göre, yani **değerine
  göre** sırala" demek.
- **`reverse=True`** büyükten küçüğe. Yazmazsan en az geçenler başa gelir.
- **Sonuç bir liste**, ve içinde yalnızca **kelimeler** var, sayılar yok. Sayıya
  ulaşmak için yine sözlüğü anahtarla açıyoruz: `sayac[kelime]`.

Küçük bir örnekle:

```python
fiyatlar = {"kahve": 45, "çay": 30, "latte": 60}

print(sorted(fiyatlar))                                   # ['kahve', 'latte', 'çay']
print(sorted(fiyatlar, key=fiyatlar.get))                 # ['çay', 'kahve', 'latte']
print(sorted(fiyatlar, key=fiyatlar.get, reverse=True))   # ['latte', 'kahve', 'çay']
```

İlk satırdaki alfabetik sıraya dikkat: `çay` **en sonda**. Python harfleri kendi
numaralarına göre sıralar ve ç, ş, ö, ü gibi Türkçe harflerin numaraları z'den
büyüktür. Bu konuda alfabetik sıralamaya ihtiyacımız yok, ama ileride karşına
çıkarsa şaşırma.

**`sayac.get` yazarken parantez yok.** Fonksiyonun **kendisini** veriyoruz; `sorted`
onu her kelime için kendisi çağıracak. Parantez koyarsan, `sorted`'a vermeden önce
fonksiyonu kendin çağırmış olursun, hem de kelimesiz:

```
TypeError: get expected at least 1 argument, got 0
```

"`get` en az 1 değer bekliyordu, 0 aldı." Bu mesajı görürsen parantezi sil.

**Eşitlik olursa?** Aynı sayıda geçen kelimeler (ör. 5'er kez geçen `çalışmak`, `yer`,
`priz`) sözlükte bulundukları sırayı korur; yani metinde ilk görüldükleri sıra.

İnternette `sorted(sayac.items(), key=lambda x: x[1])` kalıbını görebilirsin. Aynı
işi yapar ama bu derste kullanmıyoruz: `lambda` henüz konumuz değil ve `x[1]` neyin
açıldığını söylemediği için okuması zor. Üstelik "sayıyla açma" alışkanlığını
güçlendirir; ısınmada düzelttiğimiz hata tam olarak buydu.

> **Kendini dene 7:** `sirali[0]` ne verir, `sayac[sirali[0]]` ne verir? `sayac[0]` ne
> verir?

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

`04_durak_kelime.py`: okuma ve temizleme aynı. Sonra durak kelimeleri okuyup sayma
döngüsüne **tek satır** ekliyoruz:

```python
with open("veri/turkce-durak-kelimeler.txt", encoding="utf-8") as dosya:
    durak_kelimeler = dosya.read().split()

sayac = {}
for kelime in kelimeler:
    if kelime not in durak_kelimeler and len(kelime) > 2:
        if kelime in sayac:
            sayac[kelime] = sayac[kelime] + 1
        else:
            sayac[kelime] = 1
```

- **Durak kelime listesi** hazır bir dosya: `veri/turkce-durak-kelimeler.txt`. İçinde
  her satırda bir kelime var (`ama`, `ancak`, `bana`, `bazen`, `bir`, `biraz`, ...),
  toplam 171 kelime. Açıp içine bak; bu bir kara kutu değil, sıradan bir metin dosyası.
- **`dosya.read().split()`** dosyadaki kelimeleri bir **liste** yapar. `in` ve `not in`
  listede de çalışır: "bu kelime listede var mı?"
- **Yeni olan tek satır** `if kelime not in durak_kelimeler and len(kelime) > 2:`.
  Altındaki dört satır Adım 3'teki sayma satırları; bir girinti içeri kaydılar, yani
  yalnızca koşul doğruysa çalışırlar.
- **`kelime not in durak_kelimeler`** "kelime listede yoksa" demek. `in`'in tersi.
- **`len(kelime) > 2`** bir-iki harfli artıkları da atar. Noktalamayı boşluğa
  çevirdiğimizde `8'de` gibi yazılışlardan `8` ve `de` gibi parçalar kalabilir.
- **`and`** iki koşulun **ikisi de** doğruysa kelimeyi sayar.

Sonra yeni sayacı Adım 4'teki gibi sıralıyoruz, bu kez ilk 10:

```python
sirali = sorted(sayac, key=sayac.get, reverse=True)
for kelime in sirali[:10]:
    print(sayac[kelime], kelime)
```

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
> fark yarattığını Adım 8'de ölçeceğiz.

> **Kendini dene 8:** `len(kelime) > 2` koşulunu `len(kelime) > 3` yapsaydık, ilk 10
> listesinden hangi kelime(ler) kaybolurdu?

## Adım 6 — Sonucu dosyaya yaz

Ekrana basılan sonuç, terminali kapatınca kaybolur. Saklamak, bir arkadaşına göndermek
ya da iki metni karşılaştırmak için dosyaya yazıyoruz. `04`'ün son satırları:

```python
with open("sonuc.txt", "w", encoding="utf-8") as dosya:   # "w": yazma modu
    for kelime in sirali[:20]:
        dosya.write(f"{sayac[kelime]}\t{kelime}\n")
```

- **`"w"`** yazma modu: dosya yoksa oluşturur, varsa **içini silip baştan yazar**.
  Programı iki kez çalıştırırsan ikinci sonuç birincinin yerine geçer; alt alta
  eklenmez.
- **`\t`** sekme (sütunlar hizalı dursun diye), **`\n`** satır sonu. `.write()` kendi
  başına satır atlamaz; `\n` yazmazsan 20 kelimenin hepsi tek satıra yapışır.
- **`f"..."`** Başında `f` olan metinde süslü parantezin içi, değişkenin **değeriyle**
  değiştirilir: `f"{sayac[kelime]}\t{kelime}"` → `8	sessiz`.
- **`encoding="utf-8"`** okurken olduğu gibi yazarken de gerekli; yoksa Windows'ta
  `ç`, `ş` gibi harfler bozuk yazılabilir.
- Dosya, komutu çalıştırdığın klasöre, yani `01-veri-ve-kelime-bulutu` klasörüne
  yazılır (Adım 0'daki kural yazarken de geçerli).

`sonuc.txt`'nin ilk satırları şöyle:

```
8	sessiz
5	çalışmak
5	yer
5	priz
4	internet
```

**Sık hata: modu unutmak.** `open("sonuc.txt")` yazarsan dosya **okuma** modunda açılır
ve `.write()` şu hatayı verir (dosya hiç yoksa ondan önce `FileNotFoundError` gelir):

```
io.UnsupportedOperation: not writable
```

"Bu dosyaya yazılamaz" demek. Çaresi `"w"` eklemek.

> **Kendini dene 9:** `dosya.write(f"{kelime}: {sayac[kelime]} kez\n")` yazsaydık
> `sonuc.txt`'nin ilk satırı ne olurdu?

## Adım 7 — Kelime bulutu

`05_kelime_bulutu.py`: `04`'ün okuma, temizleme, eleme ve sayma satırları aynen.
En üste:

```python
from wordcloud import WordCloud
```

En alta:

```python
bulut = WordCloud(width=1200, height=800, background_color="white")
bulut.generate_from_frequencies(sayac)
bulut.to_file("kelime-bulutu.png")
```

- **`from wordcloud import WordCloud`** `wordcloud` kütüphanesinden `WordCloud` aracını
  alıyoruz. Kütüphane kurulu değilse bu satır `ModuleNotFoundError` verir.
- **`WordCloud(...)`** boş bir bulut **tuvali** hazırlar: boyutu 1200×800 piksel,
  arka planı beyaz. Henüz içinde kelime yok.
- **`generate_from_frequencies(sayac)`** kelimeleri yerleştirir. Girdi olarak doğrudan
  **sayaç sözlüğümüzü** (durak kelimeleri elenmiş hâlini) veriyoruz; kelimenin boyutu
  sözlükteki değeriyle orantılı.
- **`to_file(...)`** görseli PNG olarak kaydeder. Program ekrana bir şey yazmaz;
  konunun klasöründe `kelime-bulutu.png` oluşur.

**Neden kendi sayacımızı veriyoruz?** Kütüphanenin, ham metni doğrudan alan bir
`generate(metin)` komutu da var. Ama o kendi temizliğini yapar ve bu temizlik
İngilizceye göre ayarlıdır: İngilizce durak kelimeleri eler, Türkçeleri tanımaz, büyük
İ sorununu bilmez. Kendi sayacımızı verdiğimizde neyin sayıldığı **bizim kontrolümüzde**
olur.

Kütüphanenin kendi yazı tipi ç, ğ, ı, İ, ö, ş, ü harflerini gösterir. Başka bir yazı
tipi seçmek istersen `WordCloud(..., font_path="yazı tipi dosyasının yolu")` yazarsın;
seçtiğin yazı tipinde Türkçe harfler yoksa harfler kutu gibi çıkar.

### Bulutu okurken

Kelime bulutunda **yalnızca boyut** veri taşır. Kelimenin yeri, rengi ve yönü
rastgeledir; programı her çalıştırdığında değişebilir. "sessiz ortada, demek ki en
önemli" ya da "priz yeşil, demek ki olumlu" gibi okumalar yanlıştır. Bir tasarımcı
olarak bunu bilmen önemli: izleyici her görsel farkın bir anlamı olduğunu varsayar.
Bulutu bir sunumda kullanırsan, bu yanlış okumayı engellemek senin işin.

`08_bulut_tasarimi.py` ile renk paleti, arka plan, kelime sayısı ve yazı yönüyle
oynayabilirsin. Hepsi görünüşü değiştirir; hangi kelimenin büyük olduğunu değiştirmez.

### Bulutta sık yaşanan iki sorun

**Sayaç yerine listeyi vermek:**

```python
bulut.generate_from_frequencies(kelimeler)
```

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

> **Kendini dene 10:** Aynı programı iki kez çalıştırdın; ikinci bulutta "priz" sağ
> üstte ve mor, birincide sol altta ve sarıydı. Bir şey mi değişti?

---

## Adım 8 — Bulutun söylemediği iki şey

Bu adım ve bir sonraki, derinleşme bölümüdür. Dosyası: `09_kok_ve_baglam.py`.

Buraya kadarki bulgumuz: "müşteriler kafeyi sessiz bir çalışma yeri olarak anlatıyor."
Bir tasarım kararını bir kelime sayımına dayandırmadan önce iki soruyu sormalıyız.

### Soru 1 — Ekler sonucu değiştiriyor mu?

Adım 5'in sonundaki sınırı hatırla: `bahçe`, `bahçesi` ve `bahçede` ayrı sayılıyor.
Basit bir çözüm: **aynı harflerle başlayan** kelimeleri toplamak. `09_kok_ve_baglam.py`:
okuma ve temizleme aynı (bu dosyada durak kelime elemesi yok), sonra:

```python
for kok in ["sessiz", "kahve", "bahçe", "priz", "ışık"]:
    bulunanlar = []
    for kelime in kelimeler:
        if kelime.startswith(kok):   # bu harflerle mi başlıyor?
            bulunanlar.append(kelime)
    print(kok, len(bulunanlar), bulunanlar)
```

- **`kelime.startswith(kok)`** "kelime bu harflerle başlıyor mu?" sorusunu sorar.
- Her kök için boş bir `bulunanlar` listesi kuruyoruz ve o harflerle başlayan her kelimeyi
  içine atıyoruz. Listenin uzunluğu (`len`) kaç kez geçtiğini verir.
- Listeyi de yazdırıyoruz: **neyi topladığını görmeden bir toplama güvenme.**

```
sessiz 9 ['sessiz', 'sessiz', 'sessiz', 'sessiz', 'sessiz', 'sessiz', 'sessizlik', 'sessiz', 'sessiz']
kahve 6 ['kahvesi', 'kahve', 'kahve', 'kahvenin', 'kahveleri', 'kahveli']
bahçe 5 ['bahçesi', 'bahçede', 'bahçe', 'bahçe', 'bahçede']
priz 5 ['priz', 'priz', 'priz', 'priz', 'priz']
ışık 3 ['ışık', 'ışıklandırma', 'ışık']
```

İki şey değişti:

- **Bahçe** tek başına 2 idi, toplayınca 5 oldu. Bulutta küçük görünen bahçe, aslında
  priz kadar sık konuşulan bir konu.
- **Kahve** tek başına 2 idi, toplayınca **6** oldu ve prizi geçti. Bulgumuz
  ("müşteri kahveden değil, çalışma ortamından söz ediyor") çöktü mü?

**Dikkat, bu yöntem de kusurlu.** `"çalış"` ile başlayanları toplarsan `çalışmak`,
`çalışmaya`, `çalışırken` yanında `çalışanlar`'ı da (kafenin personeli) sayarsın. Başka
bir konu olduğu hâlde. Kısa bir başlangıç çok şey yakalar, bazen de yanlış şeyi.
`bulunanlar` listesini yazdırmamızın sebebi bu.

### Soru 2 — Kelime hangi bağlamda geçiyor?

Sayı, bir kelimenin **kaç kez** geçtiğini söyler; **nasıl** geçtiğini söylemez. "Kahve
harika" ile "kahve fena değil" sayaç için aynı şeydir. Kahve sorusunu cevaplamak için
yorumların kendisini okumamız gerek; ama hepsini değil, yalnızca kahveden söz edenleri.

Aynı dosyanın devamı:

```python
for aranan in ["kahve", "ışık"]:
    print(aranan)
    for satir in temiz.splitlines():   # her satır bir yorum
        if aranan in satir:
            print("  ", satir)
```

- **`temiz.splitlines()`** metni satırlarına böler. Dosyamızda her satır bir yorum.
  Temizlik satır sonlarına dokunmadı; `temiz` de 30 satır.
- **`aranan in satir`** `in`'i bu kez bir **yazının içinde** kullanıyoruz: "bu parça
  satırın içinde geçiyor mu?" Böylece `kahvesi`, `kahveleri` gibi ekli hâlleri de
  yakalar.
- Neden `metin` değil de `temiz`? `temiz` küçültülmüş; `Kahve` ile başlayan cümleler ve
  `Işıklandırma` da bulunur. Noktalama gitmiş ama cümle hâlâ okunuyor.

`kahve` turunun çıktısı:

```
kahve
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

Döngünün ikinci turu `"ışık"`:

```
ışık
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

> **Kendini dene 11:** `["kahve", "ışık"]` listesine `"müzik"` eklersen iki yorum gelir. Kafenin
> kendi gönderilerinde ise "Hafta sonu canlı müzik var" yazıyor (`kafe-gonderileri.txt`).
> Bu iki bilgi yan yana konunca bir tasarımcı için nasıl bir soru doğar?

## Adım 9 — Aynı sonuç, çubuk grafik olarak

Dosyası: `10_cubuk_grafik.py`. Hazırlık klasöründeki `grafik.py`'yi yalnızca
çalıştırmıştın; burada grafik kodunu satır satır yazıyoruz.

Kelime bulutu bir **izlenim** verir: "sessiz büyük, gerisi daha küçük." Ama "sessiz,
ikinci sıradakinden **ne kadar** fazla?" ya da "priz mi daha sık, internet mi?"
sorularını buluttan cevaplayamazsın; kelimelerin boyu harf sayısına göre de değişir.
Karşılaştırma için çubuk grafik daha doğru bir araçtır.

`10_cubuk_grafik.py`: `04`'ün okuma, temizleme, eleme ve sayma satırları aynen.
En üste:

```python
import matplotlib.pyplot as plt
```

En alta:

```python
sirali = sorted(sayac, key=sayac.get, reverse=True)
etiketler = sirali[:10]
degerler = []
for kelime in etiketler:
    degerler.append(sayac[kelime])

plt.bar(etiketler, degerler, color="#4a6fa5")
plt.title("Müşteri yorumlarında en sık 10 kelime")
plt.ylabel("Kaç kez geçti")
plt.xticks(rotation=45, ha="right")   # kelimeler üst üste binmesin
plt.tight_layout()                    # kenardaki yazılar kesilmesin
plt.savefig("kelime-grafik.png", dpi=150)
```

Satır satır:

- **`import matplotlib.pyplot as plt`** Çizim araçlarını `plt` kısa adıyla alıyoruz.
  Bu kısaltma her yerde böyle kullanılır; internette gördüğün örnekler de `plt` der.
- **İki liste.** `plt.bar` iki ayrı liste ister: çubukların **adları** ve **boyları**.
  Adlar hazır: `sirali[:10]`, en sık 10 kelime. Boyları döngüyle topluyoruz; sayıyı
  yine **anahtarla** alıyoruz: `sayac[kelime]`.
- **`plt.bar(etiketler, degerler, color=...)`** Çubukları çizer. Renk, tasarım
  programlarından bildiğin onaltılık renk koduyla (`#4a6fa5`) verilebilir.
- **`plt.title`, `plt.ylabel`** Başlık ve dikey eksenin adı. Başlıksız ve eksen adı
  olmayan grafik, izleyiciye "ne ölçtüğümü tahmin et" demektir.
- **`plt.xticks(rotation=45, ha="right")`** Alttaki kelimeleri 45 derece yatırır ki üst
  üste binmesinler.
- **`plt.tight_layout()`** Kenarlardaki yazıların kesilmemesi için boşlukları ayarlar.
- **`plt.savefig(...)`** Dosyaya kaydeder; `dpi=150` çözünürlüğü belirler. Grafik
  ekranda açılmaz; konunun klasöründe `kelime-grafik.png` oluşur.

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

## Adımlar ve dosyalar

Slaytlardaki program adım adım büyüyor; her adım bir öncekinin çıktısını kullanıyor.
Aynı sıra `ornekler/` klasöründe de var. Her dosya tek başına çalışır: okuma ve temizleme
satırlarıyla başlar, sonra o adımın yeni satırlarını ekler. Her dosyayı konunun klasöründen
(`01-veri-ve-kelime-bulutu`) çalıştır:

```
uv run ornekler/01_dosya_oku.py
```

| Adım | Ne yaptık | Elimizde ne oluştu | Dosya |
|---|---|---|---|
| Isınma | İki tamir | — | `00_isinma.py` |
| 0–1 | Dosyayı açtık | `metin` | `01_dosya_oku.py` |
| 2 | Kelimelere ayırdık (ham), sonra temizleyip yeniden ayırdık | `kelimeler`, `temiz` | `01_dosya_oku.py`, `02_kelime_say.py` |
| 3 | Saydık | `sayac` | `02_kelime_say.py` |
| 4 | Sıraladık | `sirali` | `03_ilk_20.py` |
| 5 | Durak kelimeleri eledik | yeni `sayac` | `04_durak_kelime.py` |
| 6 | Dosyaya yazdık | `sonuc.txt` | `04_durak_kelime.py` |
| 7 | Çizdirdik | `kelime-bulutu.png` | `05_kelime_bulutu.py` |
| 8 | Ekleri topladık, bağlamda okuduk | bulgu | `09_kok_ve_baglam.py` |
| 9 | Çubuk grafik çizdik | `kelime-grafik.png` | `10_cubuk_grafik.py` |

Tablodaki adım numarası bu notun adımıdır; dosya adındaki sayı dosyanın sırasıdır.
İkisi her zaman aynı değil (ör. 7. adım `05` dosyasında).

Derste kendi başına dolduracağın alıştırma: `alistirma/sinif_alistirmasi.py`. Soru
tipleri vizeyle aynı: boşluk doldurma ve hata bulma.

Erken bitirirsen:

- `06_iki_metin.py`: `04`'ün kodu, tek fark dosya yolu: kafenin **kendi** gönderileri.
  Kafe kendini kahveyle anlatıyor, müşteri başka bir şeyle. Kimlik hangisini öne
  çıkarmalı?
- `07_bozuk_kodlar.py`: beş bozuk kod, beş farklı hata türü. Sırayla düzelt; her
  düzeltmeden sonra yeniden çalıştır. Hata mesajı okumak için iyi bir alıştırma.
- `08_bulut_tasarimi.py`: `05`'in bulutu, daha çok ayarla: renk paleti, arka plan,
  kelime sayısı ve yazı yönü.

---

## Sık karşılaşılan sorunlar

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `FileNotFoundError: ... No such file or directory` | Komut yanlış klasörden çalıştırıldı ya da yolda yazım hatası var | `cd 01-veri-ve-kelime-bulutu` ile konu klasörüne geç; yol `veri/...` ile başlamalı. Emin değilsen `print(os.getcwd())` |
| `ModuleNotFoundError: No module named 'wordcloud'` | Dosyayı `uv run` yerine `python` ile ya da konu klasörünün dışından çalıştırdın | Konu klasörüne gir, `uv run ...` ile çalıştır; olmazsa orada `uv sync` |
| `Ã§alÄ±ÅŸmak` gibi bozuk harfler ya da `UnicodeDecodeError` | `open(...)` içinde `encoding="utf-8"` yok | Okurken de yazarken de `encoding="utf-8"` ekle |
| `KeyError: 0` | Sözlüğü sayıyla açmaya çalıştın | Anahtarla aç: `sayac["sessiz"]` ya da `sayac[sirali[0]]` |
| `KeyError: 'kelime'` | Sayaçta olmayan bir kelimeyi okumaya ya da artırmaya çalıştın | Sayarken `if / else` ya da `.get(kelime, 0)`; okurken önce `in` ile kontrol |
| `TypeError: list indices must be integers or slices, not str` | Sayacı `[]` ile liste olarak kurdun | `sayac = {}` |
| `TypeError: get expected at least 1 argument, got 0` | `key=sayac.get()` yazdın | Parantezi sil: `key=sayac.get` |
| `io.UnsupportedOperation: not writable` | Dosyayı `"w"` olmadan açıp yazmaya çalıştın | `open("sonuc.txt", "w", encoding="utf-8")` |
| `AttributeError: 'list' object has no attribute 'items'` | Buluta sayaç yerine kelime listesi verdin | `generate_from_frequencies(sayac)` |
| `ValueError: We need at least 1 word ...` | Sayaç boş | Dosya dolu mu, eleme her şeyi silmiş mi? `print(len(sayac))` |
| Bulutta harfler kutu (□□□) | `font_path=` ile seçtiğin yazı tipi Türkçe harfleri içermiyor | `font_path=` ayarını sil (kütüphanenin kendi yazı tipi Türkçe harfleri gösterir) ya da Türkçe harfli bir yazı tipi seç |
| Bulutta 3-5 kelime var | Metin çok kısa | Daha uzun bir metin kullan (ödevde en az 300 kelime) |
| Her kelime 1 kez sayılmış | `sayac = {}` döngünün içinde | Döngüden önceye al |
| Sayaçta `internet` iki kez görünüyor | Yalnızca `.lower()` kullandın | Önce `.replace("I", "ı").replace("İ", "i")`, sonra `.lower()` |

---

## Bu konuda öğrendiklerin

- **Dosya yolu, çalıştığın klasöre göredir.** Komutları konunun klasöründen
  (`01-veri-ve-kelime-bulutu`) çalıştır; `FileNotFoundError` görürsen önce bunu kontrol et.
- **Dosyayı okurken ve yazarken `encoding="utf-8"` yaz.** Yazmazsan Windows'ta Türkçe
  harfler bozulur.
- **Temizlik saymadan önce gelir.** Noktalama ve büyük harf temizlenmezse aynı kelime
  birkaç farklı kelime gibi sayılır; bu veride asıl bulgu ("sessiz") kaybolurdu.
- **Türkçe küçültme özel iş.** `"İ".lower()` beklediğini vermez; önce İ ve I'yı kendin
  çevir.
- **`.replace()` metni değiştirmez, yeni metin üretir.** Sonucu değişkene geri koy.
- **Sözlük sayaçtır.** Anahtar kelimedir, değer kaç kez geçtiği. Anahtarla açılır,
  sayıyla değil.
- **`sorted(sayac, key=sayac.get, reverse=True)`** kelimeleri sıklığına göre sıralar ve
  bir kelime **listesi** verir; sayıya yine sözlükten ulaşırsın.
- **Durak kelimeler elenmezse sonucu onlar kaplar.** Elenecek kelime listesi bir
  karardır.
- **Kelime bulutunda yalnızca boyut veri taşır.** Konum ve renk rastgeledir.
- **Sayma nereye bakacağını söyler; bulguyu bağlamda okuyarak bulursun.**
- **Karşılaştırma için çubuk grafik, genel izlenim için bulut.**

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **Göreli yol** | Çalıştığın klasörden başlayan dosya yolu (`veri/...`) |
| **Mutlak yol** | Diskin kökünden başlayan tam yol (`C:/Users/...`, `/home/...`) |
| **Kodlama (encoding)** | Dosyadaki baytların hangi kurala göre harfe çevrileceği. Bizde hep `utf-8` |
| **Dilimleme** | Bir yazının ya da listenin bir parçasını almak: `metin[:150]`, `kelimeler[:8]` |
| **Anahtar / değer** | Sözlükte aradığın şey (anahtar) ve karşılığında bulduğun şey (değer) |
| **Sayaç** | Her şeyin kaç kez geçtiğini tutan sözlük: `{"sessiz": 8, ...}` |
| **Durak kelime (stopword)** | Her metinde sık geçen ama bir şey anlatmayan kelime: ve, bir, için, ama |
| **Kök / başlangıç** | Bir kelimenin eklerden önceki kısmı. Bu konuda "aynı harflerle başlayan" diye yaklaşık olarak kullandık |
| **Bağlam** | Bir kelimenin geçtiği cümle. Kelimenin **nasıl** kullanıldığını gösterir |
| **Hata mesajı (traceback)** | Python'un hatayı anlattığı metin. Aşağıdan yukarı okunur |
| **Sessiz hata** | Hata mesajı vermeyen ama yanlış sonuç üreten hata. En tehlikeli tür |

## Bu konunun tek cümlesi

> Sözlük, "kaç kere" sorusunun cevabını tutan yerdir; anahtarla açılır, sayıyla değil.

---

## Kendini dene — cevaplar

1. **10** döndürür. Hata mesajı almazsın; `return` döngünün içinde olduğu için ilk
   sayıyı ekleyip çıkar. Sessiz hata.
2. **Bulunmaz.** Python yolu çalıştığın klasöre (`ornekler`) göre arar:
   `01-veri-ve-kelime-bulutu/ornekler/veri/kafe-yorumlari.txt` diye bir yer yok.
   Önce `cd ..` ile bir üst klasöre, yani `01-veri-ve-kelime-bulutu`'ya çık; komutu
   oradan yaz: `uv run ornekler/01_dosya_oku.py`.
3. `metin[:1]` → `"D"` (ilk karakter, yazı olarak). `metin[0]` da `"D"` verir. Farkı
   boş metinde görürsün: boş bir yazıda `[:1]` boş yazı verir, `[0]` hata verir. Bu
   konuda ikisi aynı işi görür.
4. `temiz` → `"ışıklandırma sıcak  ortam sakin "` (virgül ve nokta boşluğa döndüğü için
   fazladan boşluklar var). `kelimeler` **4** kelime olur:
   `['ışıklandırma', 'sıcak', 'ortam', 'sakin']`. `Işık` başındaki I noktasız ı oldu.
5. `fiyatlar["çay"]` → `30`. `fiyatlar[1]` → `KeyError: 1`. `"latte" in fiyatlar` →
   `False`.
6. `{"kahve": 3, "çay": 1}`. `sayac["çay"]` → `1`.
7. `sirali[0]` → `"sessiz"` (en sık kelime). `sayac[sirali[0]]` → `8` (onun sayısı).
   `sayac[0]` → `KeyError: 0`. Sıralanmış **liste** sayıyla, **sözlük** anahtarla açılır.
8. İlk 10'dan yalnızca **yer** (3 harf) kaybolur; yerine 11. sıradaki `masalar` girer.
   Kısa ama anlamlı kelimeleri de atabileceğin için eşik de bir karardır.
9. `sessiz: 8 kez`
10. **Hayır.** Konum ve renk her çalıştırmada rastgele seçilir; veri taşımaz. Değişmeyen
    tek şey kelimelerin boyutu, çünkü o sayaçtan geliyor.
11. Müşteriler bu kafeye sessizlik için geliyor ("çalışmak için yanlış günü seçmişim");
    kafe ise kendini canlı müzikle tanıtıyor. Soru şu: yeni kimlik iki kitleyi nasıl
    ayıracak? Örneğin canlı müzik gecelerinin önceden ve açıkça duyurulması, ya da
    çalışma alanıyla etkinlik alanının ayrılması. Bu bir kod sorusu değil, tasarım
    sorusu; ama onu soruya kod getirdi.
12. `etiketler = sirali[:10]` satırında `10` yerine `15` yaz. Başlığı da
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
