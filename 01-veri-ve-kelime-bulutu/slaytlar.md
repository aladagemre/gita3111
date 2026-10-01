# Konu 1 — Veriyi Kodla İşlemek

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Bu konunun planı

**1. Kurulum kontrolü** — herkes evde yaptığı kurulumu `kurulum_testi.py` ile gösterir *(yalnızca Konu 01'in ilk oturumunda)*

**2. Isınma** — geçen dönemin en sık iki hatası, düzeltmeli

**3. Kelime bulutu** — bir metin dosyasından başlayıp görsele varacağız

**4. Derinleşme** — bulutun göremediği şeyler ve aynı sonucun çubuk grafiği

Bu konu boyunca **tek bir program** yazacağız. Her adımda üstüne bir parça ekleyeceğiz:
dosyayı aç → kelimelere ayır → temizle → say → sırala → ele → çizdir → bağlamda oku.

-----

## Hedef: bu görseli üretmek

Bir kafenin görsel kimliğini yenileyeceksin. Elinde müşterilerin yazdığı 30 yorum var.
Tasarıma başlamadan önce sorumuz:

> Müşteriler bu kafeyi nasıl anlatıyor? Neyi seviyorlar?

30 yorumu gözle okuyabilirsin. Ama 3000 yorum olsaydı?

İşte bu yüzden sayacağız. Sonunda elimizde bir **kelime bulutu** olacak: kelimenin
boyutu, kaç kez geçtiğiyle orantılı.

-----

## Adım 0 — Kod dosyayı nerede arıyor?

```python
open("veri/kafe-yorumlari.txt")
```

- Python bu dosyayı **kodun çalıştığı klasöre** göre arar
- Kod dosyasının durduğu yere göre değil
- Bu yüzden komutları hep konunun klasöründen çalıştırıyoruz:
  `cd 01-veri-ve-kelime-bulutu`, sonra `uv run ornekler/...`
- "No such file or directory" hatasının sebebi neredeyse her zaman budur

-----

## Hata mesajı nasıl okunur?

```
Traceback (most recent call last):
  File ".../ornekler/01_dosya_oku.py", line 4, in <module>
    with open("veri/kafe-yorumlari.txt", encoding="utf-8") as dosya:
         ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'veri/kafe-yorumlari.txt'
```

1. **En alttan başla:** hatanın türü (`FileNotFoundError`) ve açıklaması
2. **Bir üste çık:** hangi satırda (`line 4`), `^^^^` ile satırın hangi parçasında
3. **Tırnak içine bak:** ipucu çoğu zaman orada — burada aranan dosya yolu

Emin değilsen sor: `import os` → `print(os.getcwd())` şu an hangi klasördesin?

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
- Artık elimizde **`metin`** var: tek parça, uzun bir yazı

-----

## Adım 2 — Metni kelimelere ayır

Tek parça metinle kelime sayamayız. Önce parçalara ayırmalıyız. Aynı dosyanın devamı:

```python
kelimeler = metin.split()
print(len(kelimeler))
print(kelimeler[:8])
```

- `.split()` metni boşluklardan bölüp bir **liste** verir
- Artık elimizde **`kelimeler`** var: `['Ders', 'çalışmak', 'için', 'en', 'sevdiğim', 'yer.', 'Sessiz,', 'her']`
- `metin` gitmedi, duruyor — sadece ondan yeni bir şey ürettik

Altıncı ve yedinci kelimeye bak: `'yer.'` noktalı, `'Sessiz,'` virgüllü ve büyük harfli.
"sessiz" yorumlarda 8 kez geçiyor; ama bu hâliyle tam yazılışıyla **yalnızca 1** kez
görünür. Temizlemeden sayarsak asıl bulguyu kaçırırız.

-----

## Sorun 1 — Büyük ve küçük harf

`Sessiz` ile `sessiz` şu an iki ayrı kelime. Hepsini küçültmeliyiz.

Ama Türkçede `.lower()` tek başına yetmiyor:

```python
print("İnternet".lower() == "internet")   # False
print("Işık".lower())                      # işık
```

Yorumlarda üç kez `İnternet`, bir kez `internet` var. Python büyük **İ**'nin üstündeki
noktayı ayrı bir işaret olarak bırakıyor — ve sayaç aynı kelimeyi **ikiye bölüyor**:
biri 3, biri 1. Ekranda ikisi aynı görünür.
Büyük **I** da noktasız **ı** yerine noktalı **i** oluyor.

-----

## Türkçe için güvenli küçültme

Yeni dosya, `02_kelime_say.py`. Okuma satırları aynı:

```python
with open("veri/kafe-yorumlari.txt", encoding="utf-8") as dosya:
    metin = dosya.read()

temiz = metin.replace("I", "ı").replace("İ", "i").lower()   # .lower() en sonda
```

- Önce İ ve I'yı kendimiz çeviriyoruz, **sonra** `.lower()`
- Sıra önemli: `.lower()` önce çalışsaydı İ çoktan bozulmuş olurdu
- Sonuç yeni bir değişkende: **`temiz`**. `metin` olduğu gibi duruyor

-----

## Sorun 2 — Noktalama

`sessiz` ile `sessiz,` de iki ayrı kelime. Saymadan önce noktalamayı temizleyelim:

```python
for isaret in ".,!?:;()[]\"'…-–—/":
    temiz = temiz.replace(isaret, " ")
kelimeler = temiz.split()
print(kelimeler[:8])
```

- Noktalamayı **silmiyoruz, boşluğa çeviriyoruz**
- Silseydik `yer.Sessiz` gibi yapışık kelimeler oluşurdu
- Dikkat: `.replace()` metni değiştirmez, **yeni metin üretir**. Bu yüzden
  `temiz = temiz.replace(...)` yazıyoruz; `temiz.replace(...)` tek başına hiçbir şey yapmaz
- Baştaki listeyle karşılaştır: noktalama gitti, hepsi küçük harf

-----

## Sözlük: anahtar ve değer

Saymaya başlamadan önce bir hatırlatma.

Liste sırayla numaralanır:

```python
renkler = ["bordo", "mercan"]
print(renkler[0])        # bordo
```

Sözlük anahtarla açılır:

```python
sayac = {"sessiz": 8, "priz": 5}
print(sayac["sessiz"])   # 8
print(sayac[0])          # HATA! 0 diye bir anahtar yok
```

Bu konunun tek kritik cümlesi: **sözlükten veri anahtarla alınır, sayıyla değil.**

Hata mesajını oku: `KeyError: 0` → "0 diye bir anahtar aradım, bulamadım".

-----

## Adım 3 — Saymak

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

- `kelimeler` bir önceki adımda hazırlandı — döngü onu geziyor
- İlk görüşte kelimeyi 1 olarak ekliyoruz, sonraki görüşlerde artırıyoruz
- Çıktı: **196** farklı kelime, `sessiz` **8** kez

Elimizde artık `{"ders": 3, "çalışmak": 5, "için": 10, ...}` gibi bir sözlük var.
(Aynı işin `.get` ile kısa yazılışı ders notunda.)

-----

## Sayaçta üç sık hata

| Yazdığın | Ne olur |
|---|---|
| `sayac = []` | `TypeError: list indices must be integers or slices, not str` |
| `sayac = {}` döngünün **içinde** | Hata yok ama her kelime 1 görünür — sessiz hata |
| `sayac[kelime] = sayac[kelime] + 1` (`else` yok) | `KeyError: 'ders'` — ilk görüşte anahtar henüz yok |

Sonuca her zaman bir göz at: "her kelime bir kez geçmiş" makul değil.

-----

## Adım 4 — Değere göre sıralamak

Sözlük sıralı değil. En sık geçenleri görmek için sıralamalıyız.

`03_ilk_20.py`: `02`'nin okuma, temizleme ve sayma satırları aynen; sondaki iki
`print` yerine:

```python
sirali = sorted(sayac, key=sayac.get, reverse=True)   # değere göre; parantez yok
for kelime in sirali[:20]:
    print(sayac[kelime], kelime)
```

- `sorted(sayac)` anahtarları alfabetik sıralar
- `key=sayac.get` "değerine göre sırala" demek
- Dikkat: `sayac.get` yazarken **parantez yok** — fonksiyonun kendisini veriyoruz, sıralama onu kendisi çağıracak
- Parantez koyarsan: `TypeError: get expected at least 1 argument, got 0`
- `sirali` bir **kelime listesi**; sayıya yine sözlükten ulaşıyoruz: `sayac[kelime]`

-----

## Sonuca bakalım

İlk sıralara bak: **için · sessiz · var · bir · çalışmak · yer · priz · ama · çok**

**için, var, bir, ama, çok** bu kafe hakkında hiçbir şey söylemiyor. Her Türkçe metinde
en üste çıkarlar ve anlamlı kelimeleri aşağı iterler. Bu bir sonuç değil, gürültü.

Bunlara **durak kelime** (stopword) denir. Elemeliyiz.

-----

## Adım 5 — Durak kelimeleri elemek

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

- Durak kelimeler düz bir **liste**; `not in` "listede yoksa" demek
- Yeni satır `if kelime not in ...`; altındaki dört satır bir girinti içeri kaydı
- `len(kelime) > 2` koşulu tek-iki harfli artıkları da atıyor

-----

## Yeni sayacı sıralayalım

Adım 4'teki sıralama, bu kez ilk 10:

```python
sirali = sorted(sayac, key=sayac.get, reverse=True)
for kelime in sirali[:10]:
    print(sayac[kelime], kelime)
```

Şimdi listenin başı anlamlı: **sessiz · çalışmak · yer · priz · internet · öğrenci**

Müşteriler kafeyi kahvesiyle değil, **sessiz bir çalışma yeri** olarak anlatıyor.
"priz" ve "internet" gibi altyapı kelimeleri bile üstte.
Yeni kimliği tasarlayacak biri için bu bir bulgu: afişte fincan mı olmalı, masada
açık bir laptop mı?

-----

## Adım 6 — Sonucu dosyaya yazmak

Ekrana basmak yeter mi? Hayır — sonucu saklamalıyız. `04`'ün son satırları:

```python
with open("sonuc.txt", "w", encoding="utf-8") as dosya:   # "w": yazma modu
    for kelime in sirali[:20]:
        dosya.write(f"{sayac[kelime]}\t{kelime}\n")
```

- `"w"` yazma modu demek: dosya yoksa oluşturur, varsa **üzerine yazar**
- `\t` sekme karakteri, sütunlar hizalı görünsün diye
- `\n` satır sonu — `.write()` kendi başına satır atlamaz
- `"w"` yazmazsan: `io.UnsupportedOperation: not writable`

-----

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

- Girdi olarak doğrudan **sayaç sözlüğümüzü** veriyoruz
- Kelimenin boyutu, sözlükteki değeriyle orantılı
- Program ekrana bir şey yazmaz; klasörde `kelime-bulutu.png` oluşur

-----

## Bulutu okurken

Bulutta **yalnızca boyut** veri taşır. Konum, renk ve yön **rastgele**; her çalıştırmada
değişebilir.

"sessiz ortada, demek ki en önemli" ya da "priz yeşil, demek ki olumlu" — ikisi de
yanlış okuma.

İzleyici her görsel farkın bir anlamı olduğunu varsayar. Bulutu sunumda kullanıyorsan
bu yanlış okumayı engellemek **tasarımcının işi**.

-----

## Adım 8 — Bulutun göremediği: ekler

`bahçe`, `bahçesi`, `bahçede` ayrı sayılıyor. `09_kok_ve_baglam.py`: okuma ve temizleme
aynı (eleme yok); sonra aynı harflerle başlayanları topluyoruz:

```python
for kok in ["sessiz", "kahve", "bahçe", "priz", "ışık"]:
    bulunanlar = []
    for kelime in kelimeler:
        if kelime.startswith(kok):   # bu harflerle mi başlıyor?
            bulunanlar.append(kelime)
    print(kok, len(bulunanlar), bulunanlar)
```

**sessiz 9 · kahve 6 · bahçe 5 · priz 5 · ışık 3**

`kahve 6 ['kahvesi', 'kahve', 'kahve', 'kahvenin', 'kahveleri', 'kahveli']`

Kahve toplayınca 6'ya çıktı, prizi geçti. Bulgumuz çöktü mü?

-----

## Adım 8 — Bulutun göremediği: bağlam

Sayı **kaç kez** geçtiğini söyler, **nasıl** geçtiğini söylemez. Kahveden söz eden
yorumları okuyalım:

```python
for aranan in ["kahve", "ışık"]:
    print(aranan)
    for satir in temiz.splitlines():   # her satır bir yorum
        if aranan in satir:
            print("  ", satir)
```

- "kahvesi **fena değil** ama asıl sebep ortam ..."
- "kahve **ortalama**  tatlılar güzel  ama buraya ders çalışmaya geliyorum ..."
- "kahve **biraz pahalı** ama saatlerce oturmana kimse bir şey demiyor"
- "kütüphane gibi **ama kahveli**"

Kahveyi doğrudan öven **tek** yorum var. Bulgu çökmedi, güçlendi.

-----

## Bir bulgu daha: ışık

Aynı döngünün `"ışık"` turu:

- "masalar geniş  **ışık yeterli**  müzik sessiz"
- "bahçe akşamları çok keyifli  **ışıklandırma sıcak**  ortam sakin"
- "**içerisi biraz karanlık**  kitap okumak için ışık yetmiyor  **bahçe daha aydınlık**"

Bulutta neredeyse görünmeyen bir kelime, somut bir tasarım sorunu çıkardı: çalışmaya
gelinen bir yerde iç mekân okumak için karanlık.

> Sayma **nereye bakacağını** söyler. Bulguyu **bağlamda okuyarak** bulursun.

-----

## Adım 9 — Aynı sonuç, çubuk grafik

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

- `plt.bar` iki liste ister: adlar ve boylar. Sayıyı yine **anahtarla** alıyoruz
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

## Programın tamamı

| Adım | Ne yaptık | Elimizde ne oluştu |
|---|---|---|
| 0–1 | Dosyayı açtık | `metin` |
| 2 | Küçülttük, noktalamayı attık, kelimelere ayırdık | `temiz`, `kelimeler` |
| 3 | Saydık | `sayac` |
| 4 | Sıraladık | `sirali` |
| 5 | Durak kelimeleri eledik | yeni `sayac` |
| 6 | Dosyaya yazdık | `sonuc.txt` |
| 7 | Çizdirdik | `kelime-bulutu.png` |
| 8 | Ekleri topladık, bağlamda okuduk | bulgu |
| 9 | Çubuk grafik çizdik | `kelime-grafik.png` |

Her adım bir öncekinin çıktısını girdi olarak aldı. Zincir buydu.

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
