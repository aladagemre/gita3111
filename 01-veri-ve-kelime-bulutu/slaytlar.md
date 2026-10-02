# Konu 1 — Veriyi Kodla İşlemek

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Bu konunun planı

**1. Kurulum kontrolü** — herkes evde yaptığı kurulumu `kurulum_testi.py` ile gösterir *(yalnızca Konu 01'in ilk oturumunda)*

**2. Isınma** — geçen dönemin en sık iki hatası, düzeltmeli

**3. Kelime bulutu** — bir metin dosyasından başlayıp görsele varacağız

**4. Derinleşme** — bulutun göremediği şeyler ve aynı sonucun çubuk grafiği

Hepsi **tek bir defterde**: `ders.ipynb`. Her hücre bir öncekinin ürettiğini kullanır:
dosyayı aç → kelimelere ayır → temizle → say → sırala → ele → çizdir → bağlamda oku.

-----

## Defter nasıl çalışır?

- VS Code'da `01-veri-ve-kelime-bulutu` klasörünü aç, `ders.ipynb`'ye tıkla
- Sağ üstten **çekirdek** (kernel) olarak `.venv` seç
- Hücreye tıkla, **Shift + Enter**: hücre çalışır, alt hücreye geçer
- Sıra önemli: atlanan hücrenin değişkeni yoktur → `NameError`
- Bir şey karışırsa: üstteki **Restart**, sonra hücreleri baştan sırayla çalıştır

-----

## Isınma — Tamir 1

Öğrencinin puanını (85) yazmalı. Hata veriyor:

```python
def puani_getir(ogrenci):
    return ogrenci[1]

print(puani_getir({"ad": "Deniz", "puan": 85}))
```

`KeyError: 1` → "1 diye bir anahtar aradım, bulamadım". Sözlükte sıra numarası yok.

```python
def puani_getir(ogrenci):
    return ogrenci["puan"]

print(puani_getir({"ad": "Deniz", "puan": 85}))
```

-----

## Isınma — Tamir 2

Toplamı (60) yazmalı. Hata yok, ama **10** yazıyor:

```python
def topla(sayilar):
    toplam = 0
    for sayi in sayilar:
        toplam = toplam + sayi
        return toplam

print(topla([10, 20, 30]))
```

`return` döngünün içinde: fonksiyon ilk turda biter. Bir girinti sola:

```python
def topla(sayilar):
    toplam = 0
    for sayi in sayilar:
        toplam = toplam + sayi
    return toplam

print(topla([10, 20, 30]))
```

-----

## Hedef: bu görseli üretmek

Bir kafenin görsel kimliğini yenileyeceksin. Elinde müşterilerin yazdığı 30 yorum var.
Tasarıma başlamadan önce sorumuz:

> Müşteriler bu kafeyi nasıl anlatıyor? Neyi seviyorlar?

30 yorumu gözle okuyabilirsin. Ama 3000 yorum olsaydı?

İşte bu yüzden sayacağız. Sonunda elimizde bir **kelime bulutu** olacak: kelimenin
boyutu, kaç kez geçtiğiyle orantılı.

-----

## Kod dosyayı nerede arıyor?

```py
open("veri/kafe-yorumlari.txt")
```

- Bu bir **göreli yol**: "bulunduğum klasördeki `veri` klasörüne gir"
- Defter, **kendi durduğu klasörde** çalışır: `01-veri-ve-kelime-bulutu`
- O yüzden `veri/...` bulunur
- Defteri başka klasöre kopyalarsan ya da yolu yanlış yazarsan: `FileNotFoundError`

-----

## Hata mesajı nasıl okunur?

```
FileNotFoundError                         Traceback (most recent call last)
Cell In[1], line 1
----> 1 with open("veri/kafe_yorumlari.txt", encoding="utf-8") as dosya:
      2     metin = dosya.read()

FileNotFoundError: [Errno 2] No such file or directory: 'veri/kafe_yorumlari.txt'
```

1. **En alttan başla:** hatanın türü (`FileNotFoundError`) ve açıklaması
2. **Oka bak:** `---->` hücrenin hangi satırında patladığını gösterir
3. **Tırnak içine bak:** ipucu çoğu zaman orada. Burada: `kafe_yorumlari` alt çizgili, dosyanın adı tireli

-----

## Adım 1 — Dosyayı aç

```python
with open("veri/kafe-yorumlari.txt", encoding="utf-8") as dosya:
    metin = dosya.read()

print(len(metin))
print(metin[:150])
```

- `metin[:150]` → "baştan 150 karakter". Buna **dilimleme** denir; listelerde de
  aynı şekilde çalışır: `kelimeler[:8]` ilk sekiz kelime demek
- `encoding="utf-8"` yazmazsan Türkçe harfler bozulabilir
- `with` bloğu dosyayı iş bitince kendisi kapatır
- Artık elimizde **`metin`** var: 2078 karakterlik, tek parça, uzun bir yazı

-----

## Adım 2 — Metni kelimelere ayır

Tek parça metinle kelime sayamayız. Önce parçalara ayırmalıyız:

```python
kelimeler = metin.split()
print(len(kelimeler))
print(kelimeler[:8])
```

- `.split()` metni boşluklardan bölüp bir **liste** verir
- Artık elimizde **`kelimeler`** var: `['Ders', 'çalışmak', 'için', 'en', 'sevdiğim', 'yer.', 'Sessiz,', 'her']`

Altıncı ve yedinci kelimeye bak: `'yer.'` noktalı, `'Sessiz,'` virgüllü ve büyük harfli.
"sessiz" yorumlarda 8 kez geçiyor; ama bu hâliyle tam yazılışıyla **yalnızca 1** kez
görünür. Temizlemeden sayarsak asıl bulguyu kaçırırız.

-----

## Sorun 1 — Büyük ve küçük harf

`Sessiz` ile `sessiz` şu an iki ayrı kelime. Hepsini küçültmeliyiz.

Ama Türkçede `.lower()` tek başına yetmiyor:

```python
print("İnternet".lower() == "internet")
print("Işık".lower())
```

Çıktı: `False` ve `işık`.

Yorumlarda üç kez `İnternet`, bir kez `internet` var. Python büyük **İ**'nin üstündeki
noktayı ayrı bir işaret olarak bırakıyor — ve sayaç aynı kelimeyi **ikiye bölüyor**:
biri 3, biri 1. Ekranda ikisi aynı görünür.
Büyük **I** da noktasız **ı** yerine noktalı **i** oluyor.

-----

## Türkçe için güvenli küçültme

```python
temiz = metin.replace("I", "ı")
temiz = temiz.replace("İ", "i")
temiz = temiz.lower()
```

- Önce İ ve I'yı kendimiz çeviriyoruz, **sonra** `.lower()`
- Sıra önemli: `.lower()` önce çalışsaydı İ çoktan bozulmuş olurdu
- Sonuç yeni bir değişkende: **`temiz`**. `metin` olduğu gibi duruyor
- Dikkat: `.replace()` metni değiştirmez, **yeni metin üretir**. Bu yüzden
  `temiz = temiz.replace(...)` yazıyoruz; `temiz.replace(...)` tek başına hiçbir şey yapmaz

-----

## Sorun 2 — Noktalama

`sessiz` ile `sessiz,` de iki ayrı kelime. Saymadan önce noktalamayı temizleyelim:

```python
for isaret in ".,;:!?'()-":
    temiz = temiz.replace(isaret, " ")

kelimeler = temiz.split()
print(kelimeler[:8])
```

- Tırnak içindeki yazı, noktalama işaretlerinin listesi; döngü onu **karakter karakter** gezer
- Noktalamayı **silmiyoruz, boşluğa çeviriyoruz**: silseydik `yer.Sessiz` → `yerSessiz` olurdu
- `kelimeler` artık temiz liste: `['ders', 'çalışmak', 'için', 'en', 'sevdiğim', 'yer', 'sessiz', 'her']`

-----

## Sözlük: anahtar ve değer

Saymaya başlamadan önce bir hatırlatma.

Liste sırayla numaralanır:

```py
renkler = ["bordo", "mercan"]
print(renkler[0])        # bordo
```

Sözlük anahtarla açılır:

```py
sayac = {"sessiz": 8, "priz": 5}
print(sayac["sessiz"])   # 8
print(sayac[0])          # HATA! 0 diye bir anahtar yok
```

Bu konunun tek kritik cümlesi: **sözlükten veri anahtarla alınır, sayıyla değil.**

Hata mesajını oku: `KeyError: 0` → "0 diye bir anahtar aradım, bulamadım".

-----

## Adım 3 — Elle say: sözlükle sayaç

Önce işi **elle** yapıyoruz ki sayacın nasıl çalıştığını görelim:

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

- `kelimeler` bir önceki adımda hazırlandı — döngü onu geziyor
- İlk görüşte kelimeyi 1 olarak ekliyoruz, sonraki görüşlerde artırıyoruz
- Çıktı: **196** farklı kelime, `sessiz` **8** kez

Elimizde artık `{"ders": 3, "çalışmak": 5, "için": 10, ...}` gibi bir sözlük var.

-----

## Sayaçta üç sık hata

| Yazdığın | Ne olur |
|---|---|
| `sayac = []` | `TypeError: list indices must be integers or slices, not str` |
| `sayac = {}` döngünün **içinde** | Hata yok ama her kelime 1 görünür — sessiz hata |
| `sayac[kelime] = sayac[kelime] + 1` (`else` yok) | `KeyError: 'ders'` — ilk görüşte anahtar henüz yok |

Sonuca her zaman bir göz at: "her kelime bir kez geçmiş" makul değil.

-----

## Adım 4 — Hazır araçla say: `Counter`

Adım 3'te elle yazdığımız sayacın aynısını Python'un hazır aracı `Counter` tek satırda kurar:

```python
from collections import Counter

sayac = Counter(kelimeler)
print(sayac["sessiz"])
```

- Çıktı yine **8**. Adım 3'te elle bulduğumuz sayının aynısı
- `Counter` da bir sözlük gibi çalışır: `sayac["sessiz"]` → anahtarla açılır
- Önce elle yazdık ki içini bilelim; artık hazır aracı güvenle kullanabiliriz

-----

## Adım 4 — En sık geçenler: `most_common`

`Counter`'ın bir becerisi daha var: en sık geçenleri sıralar.

```python
for kelime, adet in sayac.most_common(20):
    print(adet, kelime)
```

- `most_common(20)`: en sık 20 kelime, en çoktan aza
- Döngüde **iki değişken** var: her turda bir ikili gelir, kelime ve adedi
- İlk tur: `kelime` = `"için"`, `adet` = `10`; ikinci tur: `"sessiz"`, `8`; ...

-----

## Sonuca bakalım

İlk sıralara bak: **için · sessiz · var · bir · çalışmak · yer · priz · ama · çok**

**için, var, bir, ama, çok** bu kafe hakkında hiçbir şey söylemiyor. Her Türkçe metinde
en üste çıkarlar ve anlamlı kelimeleri aşağı iterler. Bu bir sonuç değil, gürültü.

Bunlara **durak kelime** (stopword) denir. Elemeliyiz.

-----

## Adım 5 — Durak kelimeleri okumak

Durak kelimeler hazır bir dosyada, her satırda bir kelime:

```python
with open("veri/turkce-durak-kelimeler.txt", encoding="utf-8") as dosya:
    durak_metni = dosya.read()

durak_kelimeler = durak_metni.split()
print(len(durak_kelimeler))
print(durak_kelimeler[:10])
```

- Adım 1'in aynısı, başka bir dosya: önce metin, sonra liste
- **171** kelime: `ama`, `ancak`, `bana`, `bazen`, ...
- Durak kelimeler düz bir **liste**

-----

## Adım 5 — Anlamlı kelimeleri ayır

Durak kelimeleri ve iki harfli artıkları atıp **anlamlı** kelimeleri ayrı bir listeye alıyoruz:

```python
anlamli = []
for kelime in kelimeler:
    if kelime not in durak_kelimeler and len(kelime) > 2:
        anlamli.append(kelime)

print(len(kelimeler), len(anlamli))
```

- `not in` "listede yoksa" demek
- `len(kelime) > 2` koşulu tek-iki harfli artıkları da atıyor
- Çıktı: `298 221`. 77 kelime elendi

-----

## Yeni listeyi sayalım

Yeni listeyi `Counter`'a veriyoruz, bu kez ilk 10:

```python
sayac = Counter(anlamli)
for kelime, adet in sayac.most_common(10):
    print(adet, kelime)
```

Şimdi listenin başı anlamlı: **sessiz · çalışmak · yer · priz · internet · öğrenci**

Müşteriler kafeyi kahvesiyle değil, **sessiz bir çalışma yeri** olarak anlatıyor.
"priz" ve "internet" gibi altyapı kelimeleri bile üstte.
Yeni kimliği tasarlayacak biri için bu bir bulgu: afişte fincan mı olmalı, masada
açık bir laptop mı?

-----

## Adım 6 — Kelime bulutu

```python
from wordcloud import WordCloud

bulut = WordCloud(width=1200, height=800, background_color="white")
bulut.generate_from_frequencies(sayac)
bulut.to_image()
```

- Girdi olarak doğrudan **sayacımızı** (`Counter`) veriyoruz
- Kelimenin boyutu, sözlükteki değeriyle orantılı
- Son satır `bulut.to_image()`: defter görseli hücrenin altında gösterir

Tasarımla oyna: `background_color="black"`, `colormap="magma"`, `max_words=25`.
Görünüş değişir; hangi kelimenin büyük olduğu değişmez.

-----

## Bulutu okurken

Bulutta **yalnızca boyut** veri taşır. Konum, renk ve yön **rastgele**; hücreyi her
çalıştırdığında değişebilir.

"sessiz ortada, demek ki en önemli" ya da "priz yeşil, demek ki olumlu" — ikisi de
yanlış okuma.

İzleyici her görsel farkın bir anlamı olduğunu varsayar. Bulutu sunumda kullanıyorsan
bu yanlış okumayı engellemek **tasarımcının işi**.

-----

## Adım 7 — Bulutun göremediği: ekler

`kahve`, `kahvesi`, `kahvenin` ayrı sayılıyor. İçinde "kahve" geçen kelimeleri toplayalım:

```python
aranan = "kahve"
bulunanlar = []
for kelime in kelimeler:
    if aranan in kelime:
        bulunanlar.append(kelime)

print(len(bulunanlar))
print(bulunanlar)
```

`6 ['kahvesi', 'kahve', 'kahve', 'kahvenin', 'kahveleri', 'kahveli']`

`"kahve"` yerine başka kelime yaz, yeniden çalıştır:
**sessiz 9 · kahve 6 · bahçe 5 · priz 5 · ışık 3**

Kahve toplayınca 6'ya çıktı, prizi geçti. Bulgumuz çöktü mü?

-----

## Adım 7 — Bulutun göremediği: bağlam

Sayı **kaç kez** geçtiğini söyler, **nasıl** geçtiğini söylemez. Kahveden söz eden
yorumları okuyalım:

```python
for satir in temiz.splitlines():
    if "kahve" in satir:
        print(satir)
```

- `.splitlines()` metni satırlara böler; her satır bir yorum
- "kahvesi **fena değil** ama asıl sebep ortam ..."
- "kahve **ortalama**  tatlılar güzel  ama buraya ders çalışmaya geliyorum ..."
- "kahve **biraz pahalı** ama saatlerce oturmana kimse bir şey demiyor"
- "kütüphane gibi **ama kahveli**"

Kahveyi doğrudan öven **tek** yorum var. Bulgu çökmedi, güçlendi.

-----

## Bir bulgu daha: ışık

```python
for satir in temiz.splitlines():
    if "ışık" in satir:
        print(satir)
```

- "masalar geniş  **ışık yeterli**  müzik sessiz"
- "bahçe akşamları çok keyifli  **ışıklandırma sıcak**  ortam sakin"
- "**içerisi biraz karanlık**  kitap okumak için ışık yetmiyor  **bahçe daha aydınlık**"

Bulutta neredeyse görünmeyen bir kelime, somut bir tasarım sorunu çıkardı: çalışmaya
gelinen bir yerde iç mekân okumak için karanlık.

> Sayma **nereye bakacağını** söyler. Bulguyu **bağlamda okuyarak** bulursun.

-----

## Adım 8 — Aynı sonuç, çubuk grafik

`plt.bar` iki liste ister: adlar ve boylar. `most_common(10)`'dan ikisini ayırıyoruz:

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

- Her turda gelen ikiliyi böldük: kelime `etiketler`e, adedi `degerler`e
- `rotation=45`: alttaki kelimeler üst üste binmesin
- Başlık ve eksen adı olmayan grafik, izleyiciye "ne ölçtüğümü tahmin et" der

-----

## Bulut mu, grafik mi?

Grafikte ilk bakışta görülen: **sessiz (8)** ötekilerden (5) belirgin biçimde önde;
`çalışmak`, `yer`, `priz` tam eşit. Bulut bunu sezdirir, grafik **ölçer**.

| Soru | Görsel |
|---|---|
| "Bu metin genel olarak neyi anlatıyor?" | Kelime bulutu |
| "Hangi konu ötekinden ne kadar önde?" | Çubuk grafik |

Hangisini seçeceğin, izleyicine ne söylemek istediğine bağlı. Bu bir **tasarım kararı**.

-----

## Defterin tamamı

| Adım | Ne yaptık | Elimizde ne oluştu |
|---|---|---|
| 1 | Dosyayı açtık | `metin` |
| 2 | Kelimelere ayırdık, küçülttük, noktalamayı attık | `kelimeler`, `temiz` |
| 3 | Elle saydık | `sayac` (sözlük) |
| 4 | `Counter` ile saydık, `most_common` ile sıraladık | `sayac` (Counter) |
| 5 | Durak kelimeleri eledik, yeniden saydık | `anlamli`, yeni `sayac` |
| 6 | Çizdirdik | kelime bulutu |
| 7 | Ekleri topladık, bağlamda okuduk | bulgu |
| 8 | Çubuk grafik çizdik | grafik |

Her adım bir öncekinin ürettiğini kullandı. Dosyayı **bir kez** okuduk.

Erken bitirirsen: `alistirma.ipynb` ve defterin sonundaki **Bonus** (kafenin kendi gönderileri).
Bonus'ta fark: Adım 3'ün elle sayacı olmayan kelimede `KeyError` verir, `Counter` `0` der.

-----

## Bu konunun ödevi

Kendi seçtiğin bir Türkçe metinle **iki** kelime bulutu üret:

1. Durak kelimeler **elenmeden**
2. Durak kelimeler **elendikten sonra**

Sonra tek bir cümle yaz: eleme öncesi en büyük kelimeler neydi, sonra ne oldu?

- Metin en az 300 kelime olsun
- Şarkı sözü, kendi yazın, bir markanın gönderileri — hepsi olur
- Puan yok; bir sonraki derste sıradaki arkadaşlar ekranda gösterecek

-----

## Hatırlanacak dört şey

**1. Sözlük anahtarla açılır.** `sayac["sessiz"]` doğru, `sayac[0]` hata.

**2. Türkçe küçültme özel iş.** `"İ".lower()` beklediğini vermez.

**3. Temizlik olmadan sonuç yanıltır.** Noktalama ve durak kelimeler elenmeden
çıkan bulut, metnin değil dilin fotoğrafıdır.

**4. Sayı nereye bakacağını söyler.** Bulguyu kelimeyi bağlamında okuyarak bulursun.

Sıradaki konu (Konu 2): **kod ile internete bağlanıyoruz.** Cloudflare hesabınız ve
anahtarınız hazır olsun.
