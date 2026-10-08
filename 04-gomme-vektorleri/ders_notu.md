# Konu 4 — Temsil ve Gömme Vektörleri

Bu not konunun özetidir; derste çalıştırdığımız `ders.ipynb` defteriyle **aynı sırada**
ilerler: Isınma, sonra Adım 1–8 ve kısa bir Bonus. Derste kaçırdığın bir yer olursa
buradan oku, sonra defterde o adımın hücrelerini çalıştır. Nottaki kod blokları
defterdeki hücrelerin birebir aynısı; notu okurken defter yanında açık dursun.

**Konu 3'te:** bir rengi üç sayıya çevirdik ve model "benzer" renkleri bu üç sayıya
bakarak buldu. Sonunda bir sorun gördük: gri mavi ile gül kurusu RGB sayılarında yakın,
ama gözümüze hiç benzemiyor. Benzerlik, şeyi hangi sayılarla temsil ettiğimize bağlı.

**Bu konuda:** aynı soruyu kelimeler için soruyoruz. Bir kelime nasıl sayıya çevrilir?
Çevrilince "benzer" kelimeler gerçekten yakın sayılar mı alır? Önce elle, iki sayıyla
deneyeceğiz; sonra bir modelden her kelime için yüzlerce sayı alacağız.

**Konunun sonunda elinde:**

- bir kelimeyi modelden vektör olarak alan bir fonksiyon (`vektor_al`),
- "kafe"ye en çok benzeyen kelimeleri bulan, **senin yazdığın** birkaç satır,
- ve 24 kelimenin haritası: renkler, duygular, tasarım terimleri, mekânlar.

**Kurulum (dersten önce):** `gita3111` klasöründe bir kez `uv sync` çalıştır. Bu konu yeni
bir kütüphane istemiyor: internete istek atan `requests` (Konu 2) ve `scikit-learn`
(Konu 3) yeterli.

**Defteri açmak:** VS Code'da `04-gomme-vektorleri` klasöründeki `ders.ipynb`'yi aç.
Sağ üstten çekirdek (kernel) olarak **`.venv`**'i seç. Sonra hücreleri yukarıdan aşağı,
**Shift + Enter** ile sırayla çalıştır. Her hücre bir öncekinin oluşturduğu değişkeni
kullanır (`harita`, `benzerlik`, `vektor_al`...); bir hücreyi atlarsan sonraki hücre
`NameError` verir.

### Bu not nasıl okunur

- Isınma ve alıştırma defteri anahtarsız, internetsiz çalışır. Isınmadaki bütün sayılar
  bu notta gerçek çıktısıyla yazılı.
- Adım 1'den sonrası `anahtar.txt` ister ve bir modele istek atar. Bu adımların
  çıktılarını notta **yazmıyoruz**: hangi kelimenin hangisine yakın düştüğünü modelin
  kendisi söyleyecek, senin ekranındaki sonuç esas. Notta bunların yerine sorular var:
  "Hangi kelimeler yan yana düştü?" Cevabı kendi çıktında ara.
- `Kendini dene` soruları notun sonunda, cevaplarıyla.

---

## Temsil: her şey sayıya çevrilir

Bilgisayar "kahve" kelimesini anlamaz; sayı ister. Bu derste her şeyi sayıya
çeviriyoruz:

| Şey | Temsili |
|---|---|
| Renk | 3 sayı (R, G, B) — Konu 3 |
| Fotoğraf | her piksel için 3 sayı |
| Ses | saniyede binlerce sayı |
| Kelime | bu konunun sorusu |

Bir şeyi sayıya çevirmenin yoluna **temsil** diyoruz. Konu 3'ün dersi şuydu: temsili
nasıl seçersen, "benzer" kelimesinin anlamını da o belirler. RGB'de gri mavi ile gül
kurusu yakındı, çünkü RGB rengi insan gözünün gördüğü gibi değil, ekranın ürettiği gibi
temsil eder.

Kelimeler için ne yapmalı? Harf harf sayıya çevirsek ("k" = 11, "a" = 1 ...) "kahve" ile
"kahive" çok yakın çıkar, "kahve" ile "çay" çok uzak. Harfler anlamı taşımıyor. Bize
**anlamı** taşıyan sayılar lazım.

## Isınma: elle iki eksenli harita

Bir mood-board hazırlarken kartları bir duvara dizdiğini düşün. Duvarın iki ekseni var:

- **sıcaklık:** soldan sağa, soğuk (−1) … sıcak (+1)
- **enerji:** aşağıdan yukarıya, sakin (−1) … canlı (+1); Konu 3'te renklere verdiğimiz
  "sakin" / "enerjik" etiketlerinin sayıya dönmüş hâli

Altı kelimeyi bu duvara yerleştirip her birine iki sayı verdik. İlk sayı sıcaklık,
ikincisi enerji:

```python
kahve = [0.6, 0.4]
cay = [0.5, -0.4]
buz = [-0.9, 0.1]
deniz = [-0.5, -0.5]
ates = [0.9, 0.9]
kar = [-0.7, -0.2]

print(cay)
```

Çıktı: `[0.5, -0.4]`. Her kelime iki sayılık küçük bir liste. Çay: biraz sıcak (0.5), biraz sakin (−0.4).

Çizerken her noktanın yanına kelimenin adını yazacağız. Bunun için adı sayılarla eşleştiren bir sözlük kuruyoruz:

```python
harita = {
    "kahve": kahve,
    "çay": cay,
    "buz": buz,
    "deniz": deniz,
    "ateş": ates,
    "kar": kar,
}
print(harita["ateş"])
```

Çıktı: `[0.9, 0.9]`.

- `harita` bir sözlük: kelimenin **adı** anahtar, iki sayısı değer. Değişken adlarında
  Türkçe harf kullanmıyoruz (`cay`, `ates`), sözlükteki adlarda kullanıyoruz (`"çay"`,
  `"ateş"`): adlar ekranda görünecek.
- Bu sayıları biz uydurduk. Sen kahveye `[0.8, 0.7]` diyebilirdin; tartışılabilir. Bu da
  temsil seçmenin bir tasarım kararı olduğunu gösteriyor.

Haritayı çizelim:

```python
import matplotlib.pyplot as plt

for kelime in harita:
    nokta = harita[kelime]
    plt.scatter(nokta[0], nokta[1], color="#4a6fa5")
    plt.text(nokta[0], nokta[1], kelime)

plt.axhline(0, color="lightgray")
plt.axvline(0, color="lightgray")
plt.xlabel("soğuk — sıcak")
plt.ylabel("sakin — canlı")
plt.show()
```

- `for kelime in harita:` sözlüğün anahtarlarını gezer: "kahve", "çay", ...
- `nokta = harita[kelime]` o kelimenin iki sayısı. `nokta[0]` yatay, `nokta[1]` dikey konum.
- `plt.scatter(x, y)` o konuma bir nokta koyar. `color="#4a6fa5"`, Konu 1'in grafiğindeki mavi.
- `plt.text(x, y, kelime)` aynı konuma kelimenin kendisini yazar. Etiketsiz bir harita
  altı mavi noktadan ibaret olurdu.
- `plt.axhline(0)` yükseklik 0'da yatay bir çizgi, `plt.axvline(0)` yatayda 0'da dikey
  bir çizgi çeker. İkisi duvarı dört bölgeye ayırır: sağ üst "sıcak ve canlı", sol alt
  "soğuk ve sakin".

Grafikte kahve, çay ve ateş sağda; buz, deniz ve kar solda. Yan yana duranlar
birbirine benziyor. **Kelimeyi sayıya çevirdik ve sayılar anlamı taşıyor** — çünkü
eksenleri biz anlamlı seçtik.

Bir dil modeli de kelimeleri böyle bir haritaya yerleştirir. Farkı iki tane: eksenleri
kimse seçmez, model kendisi bulur; ve eksen sayısı 2 değil, yüzlerce.

### Benzerlik: hazır bir araç

Haritaya bakıp "kahve çaya yakın" demek kolay. Ama yüzlerce eksen olunca bakacak bir
haritamız olmayacak; benzerliği bir **sayıyla** ölçmemiz gerek. Bunun için Konu 3'teki
scikit-learn'ün hazır bir aracı var: `cosine_similarity` (kosinüs benzerliği). Onu
küçük bir fonksiyona koyuyoruz:

```python
from sklearn.metrics.pairwise import cosine_similarity

def benzerlik(a, b):
    sonuc = cosine_similarity([a], [b])
    satir = sonuc[0]
    return satir[0]
```

Bu fonksiyonun içini bilmen gerekmiyor; dersin geri kalanında yalnızca **verdiği
sayıyı** okuyacağız. Yine de satırları okuyalım:

- `cosine_similarity` aslında çok sayıda kelimeyi birden kıyaslamak için yapılmış; bu
  yüzden liste ister: `[a]`, "tek kelimelik bir liste". Konu 3'teki `predict([renk])`
  ile aynı durum.
- Cevabı da bir tablo olarak verir (satırlar ve sütunlar). Bizim tablomuzda tek satır,
  tek sütun var. `satir = sonuc[0]` ilk satırı alır, `satir[0]` o satırın ilk (ve tek) sayısını.
  Konu 2'deki `yanit["result"]` gibi: katman katman, her biri ayrı satırda.

Sayının anlamı:

| Sayı | Anlamı |
|---|---|
| **1** | aynı yön: çok benzer |
| **0** | ilgisiz |
| **−1** | zıt yön |

```python
print(benzerlik(kahve, cay))
print(benzerlik(kahve, buz))
```

Çıktı:

```text
0.3032036572769468
-0.765704864789611
```

Kahve ile çay ikisi de sıcak tarafta ama biri canlı, biri sakin: 0.3, hafif benzer.
Buz karşı tarafta: −0.77, neredeyse zıt.

### Uzaklık değil, yön

Hücrede `buz` yerine `ates` yazıp çalıştırınca `0.9805806756909202` çıkar: neredeyse 1.
Oysa ateş haritada kahveyle aynı yerde değil: çok daha sıcak, çok daha canlı. Kahveye
haritada daha yakın duran çay ise yalnızca 0.3 aldı. Nasıl olur?

Her kelimeyi, haritanın ortasından (0, 0) kelimeye uzanan bir **ok** olarak düşün.
Kahvenin oku sağ üste bakıyor; ateşin oku da sağ üste bakıyor, sadece daha uzun.
Kosinüs benzerliği okların **uzunluğuna** değil, **yönüne** bakar. İki ok aynı yöne
bakıyorsa 1, dik açıdaysa 0, tam ters yöne bakıyorsa −1.

Isınmanın bütün ikilileri:

| İkili | Benzerlik | Okuması |
|---|---|---|
| kahve – ateş | 0.98 | aynı yön; ateş yalnızca "daha fazlası" |
| buz – kar | 0.93 | ikisi de soğuk tarafta |
| kahve – çay | 0.30 | ikisi de sıcak; enerjileri ters |
| çay – ateş | 0.11 | neredeyse ilgisiz: biri sakin, öbürü çok canlı |
| kahve – buz | −0.77 | karşı taraflarda |
| ateş – deniz | −1.0 | tam zıt yön: deniz `[-0.5, -0.5]`, ateş `[0.9, 0.9]` |

Ateş ile deniz neden tam −1? Denizin iki sayısı ateşinkilerin tam tersi işaretli
(ve biraz kısa); ok tam ters yöne bakıyor.

Yön neden önemli? Bir dil modelinde "çok sıcak" ile "biraz sıcak" aynı yöne bakar;
farkları okun uzunluğundadır. Biz "ne hakkında" sorusuyla ilgileniyoruz, "ne kadar"
sorusuyla değil. Bu yüzden yönü ölçüyoruz.

**Kendin dene:** `kar` ile `deniz` ne kadar benzer? Önce haritaya bakıp tahmin et, sonra
`print(benzerlik(kar, deniz))` yazıp çalıştır.

---

## Adım 1 — Anahtarı oku

**(anahtar gerekir)** Konu 2'deki hücrenin birebir aynısı:

```python
anahtarlar = {}
with open("../anahtar.txt", encoding="utf-8") as dosya:
    for satir in dosya:
        parcalar = satir.split("=")
        ad = parcalar[0].strip()
        deger = parcalar[1].strip()
        anahtarlar[ad] = deger

hesap = anahtarlar["ACCOUNT_ID"]
anahtar = anahtarlar["API_TOKEN"]
print("Anahtar okundu")
```

Çıktı: `Anahtar okundu`. `anahtar.txt` bir üst klasörde, `gita3111`'in içinde durur;
`..` "bir üst klasör" demek. Satır satır ne olduğunu hatırlamıyorsan Konu 2 notunun
Adım 1 bölümüne dön. Defterin kopyası `04-gomme-vektorleri` klasöründe durmalı; başka
yere taşırsan `..` başka bir klasörü gösterir ve `FileNotFoundError` alırsın.

## Adım 2 — Bir kelimenin vektörü

**(anahtar gerekir)** Konu 2'deki isteğin aynısı, iki farkla.

```python
import requests

MODEL = "@cf/google/embeddinggemma-300m"
adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
basliklar = {"Authorization": f"Bearer {anahtar}"}
govde = {"text": ["kahve"]}
```

- **Model başka.** Konu 2'deki model metin yazıyordu. Bu model metin yazmaz; verdiğin
  metni bir sayı listesine çevirir. Adı `embeddinggemma-300m`: Google'ın, 100'den çok
  dilde eğitilmiş bir **gömme modeli**. Çok dilli olması bizim için önemli: yalnızca
  İngilizce metinle eğitilmiş bir model Türkçe kelimelerin anlamını bilmez ve saçma
  komşuluklar üretir.
- **Gövde başka.** Konu 2'de `{"prompt": ...}` gönderiyorduk. Burada anahtar `"text"`,
  değeri bir **liste**: `["kahve"]`. Liste, çünkü bu model tek istekte birden çok metni
  çevirebiliyor.
- Adres ve başlık aynı kalıp: yalnızca adresin sonundaki model adı değişti.

```python
cevap = requests.post(adres, headers=basliklar, json=govde)
print(cevap.status_code)
```

Çıktı `200` olmalı ("tamam"). 401 görüyorsan anahtar yanlış; Konu 2'nin Adım 5'ini
hatırla.

### Yanıta katman katman in

Konu 2'deki gibi önce yanıtı sözlüğe çeviriyor, sonra katman katman iniyoruz. Yanıtın
iskeleti kabaca şöyle (sayılar yerine `...` koyduk):

```text
{'result': {'shape': [1, ...], 'data': [[..., ..., ...]]}, 'success': True, ...}
```

`result`'ın içinde iki şey var: `data` (vektörler) ve `shape` (kaç metin, her birinde
kaç sayı). Biz `data`'yı alıyoruz:

```python
yanit = cevap.json()
sonuc = yanit["result"]
vektorler = sonuc["data"]
vektor = vektorler[0]
```

- `sonuc["data"]` bir **liste**; her elemanı da bir sayı listesi. Gönderdiğimiz her metin
  için bir vektör. Biz tek kelime gönderdik, listede tek vektör var; ilki bizim:
  `vektorler[0]`.
- Her satır tek iş yapıyor: yanıtı sözlüğe çevir, `result`'a in, `data`'yı al, ilk
  vektörü al. Bir şey ters giderse hatanın hangi katmanda çıktığını satır numarasından
  görürsün.

```python
print(len(vektor))
print(vektor[:5])
```

`len(vektor)`: vektörde kaç sayı var. Isınmada 2'ydi. Google'ın bu model için yazdığı
belgelere göre 768 sayı bekleniyor; kendi çıktına bak.

`vektor[:5]`: Konu 1'in dilimlemesi, ilk beş sayı. Sıfıra yakın, artılı eksili sayılar
göreceksin.

### Gömme: sayıların tek tek anlamı yok

Isınmada ilk sayı "sıcaklık", ikinci sayı "enerji" demekti. Modelin vektöründe
**bir sayının tek başına adı yoktur.** "Şu sayı renk eksenidir" diyemezsin. Model bu
sayıları, milyonlarca cümlede hangi kelimenin hangi kelimelerle birlikte geçtiğine
bakarak ayarlamış; benzer cümlelerde geçen kelimeler benzer sayılar almış.

Bu sayı listesine **vektör**, bir metni böyle bir listeye çevirmeye **gömme**
(embedding) diyoruz: kelime, yüzlerce boyutlu bir haritanın içine "gömülüyor".
Anlam tek tek sayılarda değil, **kelimelerin birbirine göre nerede durduğunda**.

## Adım 3 — Fonksiyona koy

**(anahtar gerekir)** Her kelime için Adım 2'nin satırlarını yeniden yazmamak için onları
bir fonksiyona koyuyoruz. Konu 2'deki `modele_sor`'un kardeşi:

```python
def vektor_al(kelime):
    govde = {"text": [kelime]}
    cevap = requests.post(adres, headers=basliklar, json=govde)
    yanit = cevap.json()
    sonuc = yanit["result"]
    vektorler = sonuc["data"]
    return vektorler[0]
```

Satırları Adım 2 ile eşleştir:

| Fonksiyondaki satır | Adım 2'deki karşılığı |
|---|---|
| `govde = {"text": [kelime]}` | `govde = {"text": ["kahve"]}`; sabit kelime yerine parametre |
| `cevap = requests.post(...)` | aynısı |
| `yanit`, `sonuc`, `vektorler` | aynısı |
| `return vektorler[0]` | `vektor = vektorler[0]`; değişkene koymak yerine geri ver |

`adres` ve `basliklar` fonksiyonun içinde tanımlı değil; fonksiyon onları Adım 2'de
tanımlanan değişkenlerden kullanır. Adım 2'yi atlarsan `NameError: name 'adres' is not
defined` alırsın.

```python
vektor = vektor_al("çay")
print(len(vektor))
```

Adım 2'deki sayının aynısı çıkmalı: her kelimenin vektörü aynı uzunlukta.

## Adım 4 — İki kelime ne kadar benzer?

**(anahtar gerekir)** **Çalıştırmadan önce tahmin et:** kahve hangisine daha çok benzer,
çaya mı, tipografiye mi?

```python
kahve = vektor_al("kahve")
cay = vektor_al("çay")
tipografi = vektor_al("tipografi")
```

Isınmadaki `kahve` değişkeni iki sayıydı; bu hücre aynı adın içine modelin vektörünü
koyuyor. Isınmanın küçük haritası artık bu değişkenleri kullanmıyor (o, `harita`
sözlüğünde duruyor).

```python
print(benzerlik(kahve, cay))
print(benzerlik(kahve, tipografi))
```

`benzerlik` fonksiyonu ısınmada iki sayıyla çalışıyordu; yüzlerce sayıyla da aynen
çalışır. Okların yönünü yüzlerce boyutta kıyaslar.

Hangisi büyük çıktı? Tahminin tuttu mu?

**Sayıları nasıl okumalı?** Gerçek bir modelin benzerlik sayılarını ısınmadaki gibi
"1 çok benzer, −1 zıt" ölçeğiyle mutlak okumaya çalışma. Her modelin kendi "olağan"
aralığı vardır. Güvenli okuma şu: **iki sayıyı yan yana koy, hangisi büyük?** "Kahve,
çaya tipografiden daha çok benziyor" demek anlamlı; "kahve ile çay şu kadar benzer"
demek o kadar anlamlı değil.

## Adım 5 — 24 kelimelik sözlük

**(anahtar gerekir)** Haritayı kalabalık bir kelime listesiyle çizeceğiz. Dört grup,
altışar kelime:

```python
kelimeler = [
    "kırmızı", "mavi", "yeşil", "bej", "siyah", "beyaz",
    "huzur", "öfke", "neşe", "hüzün", "heyecan", "sakinlik",
    "tipografi", "logo", "afiş", "palet", "kontrast", "serif",
    "kafe", "kütüphane", "park", "ofis", "atölye", "sahne",
]
print(len(kelimeler))
```

Çıktı: `24`. Her satıra bir grubu yazdık ki listeyi okumak kolay olsun: renkler,
duygular, tasarım terimleri, mekânlar. Python için satırların bir anlamı yok; köşeli
parantez kapanana kadar hepsi tek liste.

Renklerde **bej** bilerek var. Konu 3'te kafe paleti için beji sormuştuk; sınıfın
verisiyle eğitilen model onu "enerjik" demişti, ama zayıf bir işaretle (en yakın bildiği
renk olan krem, sınıfın en çok tartıştığı renkti). Şimdi aynı rengin **adına** dil
modelinin gözünden bakacağız: Adım 6'da ve Adım 8'de bejin hangi duygulara yakın
düştüğünü kendi çıktında gör.

```python
vektorler_sozlugu = {}
for kelime in kelimeler:
    vektorler_sozlugu[kelime] = vektor_al(kelime)

print(len(vektorler_sozlugu))
```

Çıktı: `24`.

- Sözlükte her kelimenin karşısına onun vektörü yazılıyor:
  `vektorler_sozlugu["kafe"]` kafenin vektörü.
- Döngü her kelime için bir istek gönderiyor: **24 istek**. Hücre birkaç saniye ile
  birkaç dakika arası sürebilir; internete bağlı. Çalışırken hücrenin solunda `[*]`
  durur; bitince `24` yazar. Beklerken tahmin et: "kafe" hangi üç kelimeye en yakın
  çıkacak? Adım 6'da bakacağız.
- Bir kelimenin vektörünü bir kez alıp sözlükte saklıyoruz. Sonraki adımlar sözlüğü
  kullanır, yeniden istek atmaz; kotanı da boşa harcamazsın.

> **Yan not:** Adım 2'de `data`'nın bir liste olduğunu, çünkü tek istekte birden çok
> metin gönderilebildiğini söylemiştik. 24 kelimeyi tek istekte de gönderebilirdik
> (`{"text": kelimeler}`). O zaman cevaptaki vektörleri kelimelerle sırayla eşleştirmek
> gerekirdi. Biz her kelime için ayrı istek atıyoruz: biraz daha yavaş, ama her satır
> tek bir iş yapıyor.

## Adım 6 — "kafe"ye en yakın 3 kelime

**(anahtar gerekir)** Bu adımı **sen yazıyorsun**. Derste önce beş dakika kendin dene
(defterde planın altındaki boş hücreye); sonra birlikte bakacağız. Plan:

1. `skorlar` adında boş bir sözlük kur.
2. Sözlükteki her kelime için "kafe" ile o kelimenin benzerliğini hesapla,
   `skorlar[kelime]`'ye koy.
3. Konu 1'deki `Counter` ile en büyükleri sırala.

Konu 1'de ne yapmıştık? `sayac` sözlüğü her kelimenin **kaç kez** geçtiğini tutuyordu;
`most_common` en büyüklerini sıralıyordu. Burada `skorlar` her kelimenin kafeye **ne
kadar benzediğini** tutacak. Kalıp aynı, sayılar farklı.

Bir çözüm:

```python
hedef = "kafe"
hedef_vektor = vektorler_sozlugu[hedef]

skorlar = {}
for kelime in vektorler_sozlugu:
    vektor = vektorler_sozlugu[kelime]
    skorlar[kelime] = benzerlik(hedef_vektor, vektor)

print(len(skorlar))
```

Çıktı: `24`.

- `hedef` aradığımız kelime; `hedef_vektor` onun vektörü. İkisini ayrı tuttuk ki hedefi
  değiştirmek için tek bir kelimeyi değiştirmek yetsin.
- Döngü her kelimenin vektörünü alıyor, hedefle benzerliğini ölçüp `skorlar`'a yazıyor.

```python
from collections import Counter

sirali = Counter(skorlar)
for kelime, skor in sirali.most_common(4):
    print(kelime, round(skor, 2))
```

- Konu 1'in `Counter`'ı geri döndü. Orada `Counter(kelimeler)` bir listeyi kendisi
  sayıyordu. Burada ona hazır bir sözlük veriyoruz: kelimeler ve benzerlikleri.
  `Counter` sayıların adet mi benzerlik mi olduğunu umursamaz; büyükten küçüğe sıralar.
- `most_common(4)`: en büyük dört skor. Her turda iki değişken gelir: kelime ve skoru
  (Konu 1'deki `for kelime, adet in ...` kalıbı).
- `round(skor, 2)`: virgülden sonra iki basamak.

**3 komşu istiyorduk, neden 4 yazdık?** Çıktının ilk satırına bak: `kafe 1.0`. Sözlükte
kafe de var, ve her kelime kendisine tam benzer. İlk satır her zaman hedefin kendisi;
3 komşu için 4 satır istiyoruz. (Alıştırma defterindeki 2. bozuk kod bu.)

**Tasarım açısından okuması.** Konu 1'de müşteri yorumlarını saymış ve müşterilerin bu
kafeyi kahvesiyle değil, **sessiz bir çalışma yeri** olarak anlattığını bulmuştuk.
Şimdi modele soruyoruz: "kafe" kelimesi neye yakın? Kütüphaneye mi (sessizlik, çalışma),
parka mı (açık hava, dinlenme), sahneye mi (kalabalık, gösteri)? Kendi çıktına bak.

Model "kafe"nin **genel** anlamını, milyonlarca metinde nasıl geçtiğinden öğrendi.
Konu 1'deki müşteriler ise **bir** kafeyi anlatıyordu. İkisi farklı çıkarsa bu bir hata
değil, bir bulgu: markanın anlatmak istediği kafe, kelimenin herkes için çağrıştırdığı
kafeden farklı. Konu 2'de soruya bağlam yazmanın cevabı değiştirdiğini görmüştük;
burada aynı şeyi tersinden görüyoruz: bağlamsız bir kelime, ortalama anlamını taşır.

**Kendin dene:** `hedef = "kafe"` yerine `"huzur"` yaz, iki hücreyi yeniden çalıştır.
Huzur, kafenin müşterilerine vermek istediği his. Huzura en yakın kelimeler hep duygular
mı? Altı renkten hangisi en üstte: bej mi, mavi mi, beyaz mı? Bu bir palet kararı değil
(model renk görmedi, yalnızca renk **adlarının** hangi metinlerde geçtiğini biliyor), ama
mood-board'a başlarken bir ipucu. Sonra `"afiş"` dene: tasarım terimleri kendi aralarında
mı toplanıyor?

## Adım 7 — Harita

**(anahtar gerekir)** Isınmadaki gibi bir harita istiyoruz. Ama her kelimede yüzlerce sayı
var, kâğıt ise iki boyutlu. Bir yöntemle yüzlerce sayıyı 2 sayıya indirmemiz gerek.

**PCA** (Temel Bileşen Analizi) bunu yapan, scikit-learn'deki hazır bir araç. Sezgisi:
bir heykeli duvara tuttuğun ışıkla düşündüğün **gölge**. Gölge iki boyutlu, heykel üç
boyutlu. Işığı iyi bir açıdan tutarsan gölgeden heykeli tanırsın; kötü bir açıdan
tutarsan yalnızca bir leke görürsün. PCA, gölgenin **en çok şey anlattığı** açıyı
arar. Bizim heykelimiz üç değil yüzlerce boyutlu, ama fikir aynı.

Önce bütün vektörleri bir listeye koyuyoruz (PCA sözlük değil, liste ister):

```python
liste = []
for kelime in vektorler_sozlugu:
    liste.append(vektorler_sozlugu[kelime])

print(len(liste))
```

Çıktı: `24`. Konu 3'teki `X` gibi bir liste: her elemanı bir vektör.

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
pca.fit(liste)
```

- `PCA(n_components=2)`: "2 sayıya indir" ayarıyla bir PCA kur.
- `fit`: Konu 3'teki gibi "önce örneklere bak". PCA 24 vektörün hepsine bakıp en çok
  şey anlatan iki yönü bulur.
- Hücrenin altında `PCA(n_components=2)` yazan bir kutu çıkar. Bu bir hata değil;
  defter, hücrenin son satırının sonucunu gösteriyor: "PCA hazır".

```python
model_haritasi = {}
for kelime in vektorler_sozlugu:
    vektor = vektorler_sozlugu[kelime]
    noktalar = pca.transform([vektor])
    model_haritasi[kelime] = noktalar[0]

print(model_haritasi["kafe"])
```

- `pca.transform([vektor])`: "bu vektörü 2 sayıya çevir". Konu 3'teki `predict` gibi bir
  **liste** ister, tek vektör olsa bile: `[vektor]`. Cevabı da liste olarak verir:
  `noktalar[0]` bizim kelimenin iki sayısı.
- `model_haritasi` ısınmadaki `harita`nın aynısı: anahtar kelimenin adı, değer iki sayısı.
  Adım 6'daki `skorlar` döngüsüyle de aynı biçim.

Çıktı, "kafe"nin iki sayısı: ısınmadaki gibi bir nokta. Konu 3'teki gibi virgülsüz yazılır
(scikit-learn'ün kendi liste türü), okuması aynı. Sayıların kendisi senin koşuna bağlı; önemli olan artık iki tane olmaları.

```python
for kelime in model_haritasi:
    nokta = model_haritasi[kelime]
    plt.scatter(nokta[0], nokta[1], color="#4a6fa5")
    plt.text(nokta[0], nokta[1], kelime)

plt.show()
```

- Isınmadaki çizim döngüsünün aynısı; yalnızca sözlüğün adı değişti (`harita` yerine
  `model_haritasi`).
- `nokta[0]` yatay, `nokta[1]` dikey konum. Isınmadaki gibi.

Bu haritanın eksenlerinin adı yok. Isınmada "sıcaklık" ve "enerji" diye biz koymuştuk;
burada PCA iki yön buldu, ama o yönlerin ne anlama geldiğini söylemiyor. Haritaya bakıp
sen yorumlayabilirsin: "sağa doğru duygular, sola doğru nesneler mi gidiyor?"

### Harita bir özettir

Yüzlerce sayıyı 2'ye indirdik. **Bilgi kaybettik.** Gölge benzetmesine dön: iki farklı
heykel, belli bir açıdan aynı gölgeyi verebilir. Haritada yan yana duran iki kelime,
gerçek yüzlerce boyutlu uzayda o kadar yakın olmayabilir. Haritada uzak duran iki
kelime de gerçekte yakın olabilir.

Bir şehir haritası gibi düşün: yolu bulmana yeter, ama binaların yüksekliğini
göstermez. Haritada bir şey dikkatini çekerse, emin olmak için asıl sayıya bak:
`benzerlik(...)`. Adım 8'de bunu yapıyoruz.

## Adım 8 — Haritayı oku

**(anahtar gerekir)** Haritaya bak ve şu soruları cevapla:

- Dört grup (renkler, duygular, tasarım, mekânlar) ayrı kümeler oluşturdu mu?
- Kendi grubundan kaçan bir kelime var mı? Nereye gitmiş? Neden olabilir?
  (Örneğin "palet" renklerin yanına mı düştü, tasarım terimlerinin yanına mı?)
- Hangi renk duyguların kümesine en yakın? Bej nereye düştü? Konu 3'teki model onu
  "enerjik" demişti; dil modeli onu hangi duygunun yanına koyuyor?
- **huzur** ile **öfke** zıt anlamlı. Haritada uzak mı düştüler?

Haritaya güvenmeden önce asıl sayılara bakalım:

```python
huzur = vektorler_sozlugu["huzur"]
ofke = vektorler_sozlugu["öfke"]
sakinlik = vektorler_sozlugu["sakinlik"]

print(benzerlik(huzur, ofke))
print(benzerlik(huzur, sakinlik))
```

Huzur, öfkeye mi daha çok benziyor, sakinliğe mi? İki sayıyı yan yana koy. Huzur ile
öfke arasındaki sayı, beklediğinden yüksek mi?

### Benzer, eşanlamlı demek değil

Model kelimelerin anlamını sözlükten öğrenmez. **Hangi cümlelerde geçtiklerinden**
öğrenir. Şu cümleye bak:

> "Bugün içimde büyük bir ___ var."

Boşluğa hem "huzur" hem "öfke" gelebilir. İki kelime anlamca zıt, ama ikisi de aynı tür
cümlelerde geçiyor: duygulardan söz eden cümlelerde. Model için bu iki kelime
"aynı mahallenin sakinleri". Bu yüzden zıt anlamlı iki kelime de birbirine yakın
düşebilir; "sıcak" ile "soğuk", "siyah" ile "beyaz" da öyle.

Modelin "benzer" dediği şey **eşanlamlı** değil, **benzer yerlerde geçen**. Bu, gömme
vektörlerinin en çok yanlış anlaşılan yanı.

**Tasarım açısından okuması:** bir marka için kelime seçerken (slogan, ürün adı,
etiket) modelin benzerliğini "anlamca aynı" diye okursan yanılırsın. "Huzur" diye bir
kafe adına en yakın kelimeleri modelden alırsan, listede rakip duyguları da
görebilirsin. Model sana "bu kelimeler aynı konuşmanın parçası" diyor; "aynı şeyi
söylüyor" demiyor.

## Bonus — Kendi 5 kelimen

```python
yeni_kelimeler = ["espresso", "minimal", "gürültü", "sessizlik", "poster"]
for kelime in yeni_kelimeler:
    vektorler_sozlugu[kelime] = vektor_al(kelime)

print(len(vektorler_sozlugu))
```

Çıktı: `29` (24 + 5). Listeye kendi beş kelimeni yaz ve çalıştır. Sonra Adım 7'nin dört
hücresini sırayla yeniden çalıştır: liste yeniden kurulur, PCA yeniden `fit` edilir,
her kelime yeniden 2 sayıya çevrilir, harita 29 kelimeyle çizilir. Yeni kelimelerin hangi gruba yakın düştü?
Örnek listeyi değiştirmeden çalıştırdıysan: "sessizlik" kafeye mi düştü, kütüphaneye mi?
Konu 1'in bulgusu (sessiz çalışma yeri) model için hangi mekâna daha yakın?

Dikkat: yeni kelimeler eklenince PCA başka bir "en iyi açı" bulur; eski 24 kelimenin
yerleri de değişebilir. Harita, içindeki kelimelere göre kurulan bir özet.

---

## Defterin bölümleri

| Adım | Ne yaptık | Elimizde ne oluştu |
|---|---|---|
| Isınma | Altı kelimeye elle iki sayı verdik, çizdik, benzerliği ölçtük | `harita`, `benzerlik` |
| 1 | Anahtarı okuduk | `hesap`, `anahtar` |
| 2 | Bir kelimenin vektörünü aldık | `vektor` |
| 3 | Fonksiyona koyduk | `vektor_al` |
| 4 | İki kelimeyi kıyasladık | — |
| 5 | 24 kelimenin vektörünü aldık | `vektorler_sozlugu` |
| 6 | En yakın komşuları bulduk | `skorlar` |
| 7 | 2 boyuta indirip çizdik | `pca`, `model_haritasi` |
| 8 | Haritayı okuduk | — |
| Bonus | Kendi kelimelerimizi ekledik | — |

Hepsi tek defterde: `ders.ipynb`. Hücreleri her zaman yukarıdan aşağı çalıştır; defteri
yeni açtıysan (ya da çekirdeği yeniden başlattıysan) en baştan başla.

Derste kendi başına çalışacağın defter: `alistirma.ipynb`. Önce aynı klasörde yeni bir
adla kopyala, kopyada çalış; böylece `git pull` çakışmaz. Bu defter internete çıkmaz,
anahtar istemez: ısınmadaki iki sayılık vektörlerle çalışır. İlk üç hücresi vektörleri,
`benzerlik` fonksiyonunu ve kahvenin `skorlar` sözlüğünü kurar. İki bölümü var:

- **Bozuk kodlar:** beş kısa hücre. İkisi hata mesajı veriyor, üçü sessizce yanlış sonuç
  yazıyor; üstlerinde ne yazmaları gerektiği yazıyor.
- **Kendi başına:** `BOSLUK` yazan yerleri doldurduğun sorular ve kendi iki eksenli
  haritan. Doldurmadığın boşluk `NameError: name 'BOSLUK' is not defined` verir; o yüzden
  soruları sırayla çöz.

---

## Sık karşılaşılan hatalar ve mesajlarını okumak

Python bir hata verdiğinde en alttaki satır en önemlisidir: önce hatanın **türü**,
iki noktadan sonra da **açıklaması** gelir.

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `NameError: name 'vektor_al' is not defined` | Bir hücreyi atladın ya da defteri yeni açtın | Hücreleri baştan, sırayla çalıştır |
| `FileNotFoundError: ... '../anahtar.txt'` | Anahtar dosyası yok ya da defterin kopyası başka klasörde | `anahtar.txt` `gita3111` içinde, defter `04-gomme-vektorleri` içinde durmalı |
| `ModuleNotFoundError: No module named 'sklearn'` | Defter `.venv` dışındaki bir çekirdekle çalışıyor | Sağ üstten çekirdek olarak `.venv`'i seç; yoksa `gita3111` klasöründe `uv sync` |
| `requests.exceptions.ConnectionError` | İnternet yok | Bağlantını kontrol et; Isınma ve alıştırma internetsiz çalışır |
| `401` durum kodu, sonra `TypeError: 'NoneType' object is not subscriptable` | Anahtar yanlış; yanıtta `result` boş geliyor | `anahtar.txt`'yi kontrol et (Konu 2, Adım 5) |
| `429` durum kodu, aynı `TypeError` | Günlük kota doldu | Kota gece sıfırlanır; derste o gün hocanın ekranından izle |
| `ValueError: Expected 2D array, got 1D array instead` | `cosine_similarity` ya da `pca.transform`'a köşeli parantezsiz tek vektör verildi | `[a]`, `[vektor]`: liste içine koy |
| `NotFittedError: This PCA instance is not fitted yet.` | `transform`'dan önce `fit` çağrılmadı | Önce `pca.fit(liste)` |
| `KeyError: 'kafe'` | Aranan kelime sözlükte yok (yazım farkı, büyük harf, Adım 5 atlandı) | Kelimeyi listedeki gibi yaz; Adım 5'i çalıştır |
| En yakın "3" kelimede yalnızca 2 komşu görünüyor | İlk satır hedefin kendisi (1.0) | `most_common(4)` |
| Haritada bütün etiketler aynı kelime | `plt.text`'e değişken yerine sabit metin yazıldı | `plt.text(nokta[0], nokta[1], kelime)` |
| "En benzer" diye en küçük sayılar seçildi | Benzerlik uzaklık değil: büyük sayı = çok benzer | Büyükten küçüğe oku |

Son üç satır hata mesajı vermeyen durumlar. Bunlarda Python sana yardım etmez; sonucu
senin kontrol etmen gerekir.

---

## Kendini dene

Cevaplar notun en sonunda. Önce kendin düşün.

1. Isınmanın haritasına `"çikolata"` kelimesini eklemek istiyorsun. İki sayısını ne
   seçerdin, neden? Kahveye benzerliği yüksek mi çıkar?
2. `benzerlik(kahve, ates)` 0.98 çıktı; oysa haritada ateş kahveyle aynı yerde değil. Bunu
   arkadaşına bir cümleyle nasıl anlatırsın?
3. `vektor_al` fonksiyonunda `return vektorler[0]` yerine `return vektorler` yazsaydın
   `len(vektor_al("çay"))` kaç yazardı?
4. Adım 6'da `most_common(4)` yerine `most_common(24)` yazsan ne görürsün?
   Listenin en altındaki kelime ne anlama gelir?
5. Haritada "logo" ile "palet" yan yana düştü. "Bu iki kelime çok benzer" diyebilir
   misin? Emin olmak için ne yaparsın?
6. Model "huzur" ile "öfke"yi birbirine yakın buldu. Model yanılıyor mu?
7. Adım 5'te listeye "Kafe" (büyük harfle) eklesen ve Adım 6'da `hedef = "kafe"`
   yazsan, "Kafe" listenin neresine düşer?
8. Isınmada eksenleri biz seçtik, modelde model seçti. Biri sana "modelin eksenleri
   bizimkilerden daha doğru" derse ne cevap verirsin?

---

## Bu konuda öğrendiklerin

- **Temsil bir seçimdir.** Bir şeyi hangi sayılarla temsil edersen, "benzer"in anlamını
  da o belirler. Isınmada eksenleri biz seçtik; model kendi eksenlerini, okuduğu
  metinlerden çıkarıyor.
- **Vektör (gömme).** Model bir kelimeyi yüzlerce sayılık bir listeye çevirir. Sayıların
  tek tek anlamı yok; anlam, kelimelerin birbirine göre nerede durduğunda.
- **Benzerlik yöne bakar.** Kosinüs benzerliği iki okun aynı yöne bakıp bakmadığını
  ölçer: 1 aynı yön, 0 ilgisiz, −1 zıt. Gerçek bir modelde sayıları yan yana okumak
  daha güvenli.
- **En yakın komşular, Konu 1'in sayacıyla.** Skorları bir sözlüğe koyup `Counter` ile
  sıraladık; ilk satır her zaman hedefin kendisi.
- **Harita bir özettir.** PCA yüzlerce sayıyı 2'ye indirir; bilgi kaybeder. Haritada
  gördüğünü asıl sayıyla doğrula.
- **Benzer, eşanlamlı değildir.** Model "benzer yerlerde geçen" kelimeleri yakın
  koyar; zıt anlamlılar da yakın düşebilir.

## Bu konunun tek cümlesi

> Model kelimeleri sayı listesine çevirir; benzer yerlerde geçen kelimelerin listeleri
> de birbirine benzer — ama "benzer yerlerde geçmek", "aynı anlama gelmek" değildir.

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **Temsil** | Bir şeyin (renk, kelime) sayılara nasıl çevrildiği; "benzerlik" bu seçime bağlıdır |
| **Vektör** | Bir sayı listesi; bu derste bir kelimenin sayılarla temsili. Isınmada 2 sayı, modelde yüzlerce |
| **Gömme (embedding)** | Bir metni, anlamını taşıyan bir vektöre çevirme işi; bunu yapan modele **gömme modeli** denir |
| **Boyut** | Vektördeki sayıların her biri; haritanın bir ekseni. Isınmada 2 boyut (sıcaklık, enerji) |
| **Kosinüs benzerliği** | İki vektörün aynı yöne bakıp bakmadığını ölçen sayı: 1 aynı yön, 0 ilgisiz, −1 zıt |
| **`cosine_similarity`** | scikit-learn'deki kosinüs benzerliği aracı; bizde `benzerlik` fonksiyonunun içinde |
| **En yakın komşu** | Bir kelimeye benzerliği en yüksek olan kelimeler; Konu 3'teki k-NN fikrinin aynısı |
| **Boyut indirgeme** | Çok sayılı vektörleri, az sayıyla (bizde 2) özetleme; çizebilmek için |
| **PCA** | scikit-learn'deki boyut indirgeme aracı; "en çok şey anlatan" yönleri bulur. `fit` öğrenir, `transform` çevirir |
| **`fit` / `transform`** | `fit`: "önce bütün örneklere bak"; `transform`: "şu vektörü 2 sayıya çevir" |
| **Eşanlamlı** | Aynı anlama gelen kelimeler. Modelin "benzer"i bundan farklıdır: benzer yerlerde geçen |

## Ödev

`odevler/odev4.md` (puansız): kendi seçtiğin 20 kelimeyle harita çıkar (fikir: bir
markanın mood-board kelimeleri); beklemediğin hangi iki kelime yan yana düştü, bu
haritayla bir mood-board'a başlasan neyi ekler, neyi çıkarırdın? İkisini birer cümleyle yaz.

## Sonraki konu

**Konu 5 — Dil modelleri nasıl çalışır.** Bu konuda model bir kelimeyi sayıya çevirdi.
Konu 5'te modelin **metni nasıl yazdığına** bakacağız: metin önce parçalara bölünür,
model her seferinde bir sonraki parçayı tahmin eder. Kafe yorumlarından, saymaktan
başka hiçbir şey yapmayan küçük bir "sonraki kelime" modeli kuracağız ve gerçek
modelin "sıcaklık" ayarını deneyeceğiz.

---

## Kendini dene — cevaplar

1. Örneğin `[0.7, 0.1]`: sıcak, ne sakin ne çok canlı. Kahveyle (`[0.6, 0.4]`) aynı
   bölgede, aynı yöne yakın bakıyor; benzerlik yüksek çıkar. Ama başka sayılar da
   seçilebilir: çikolatayı "enerji veren" diye düşünen `[0.6, 0.6]` der. Temsil bir
   seçimdir; tartışmaya açıktır.
2. "Benzerlik okların uzunluğuna değil yönüne bakıyor. Kahve de ateş de sağ üste
   bakıyor; ateş sadece daha uzun bir ok."
3. `1`. `vektorler` vektörlerin listesi; içinde tek vektör var. `len` o listenin
   uzunluğunu sayar, vektörün değil. Sonraki adımlarda `benzerlik` de yanlış şey alır.
4. 24 kelimenin hepsini, kafeye en benzerden en az benzere sıralı görürsün. En alttaki
   kelime, bu 24 kelime içinde kafeyle **en az** birlikte anılan kelime. "Kafenin zıttı"
   demek değil; yalnızca bu listede en uzak olan.
5. Hayır, yalnızca haritaya bakarak diyemezsin: harita yüzlerce sayının 2 sayılık bir
   özeti ve bilgi kaybediyor. Adım 8'deki gibi asıl sayıya bakarsın: önce iki vektörü
   birer değişkene al (`logo = vektorler_sozlugu["logo"]`, `palet = ...`), sonra
   `print(benzerlik(logo, palet))`. Çıkan sayıyı başka ikililerle yan yana koy.
6. Yanılmıyor; başka bir soruya cevap veriyor. Model "bu iki kelime aynı tür
   cümlelerde geçiyor mu?" sorusunu cevaplıyor; "aynı anlama mı geliyor?" sorusunu
   değil. İkisi de duygulardan söz eden cümlelerde geçtiği için yakınlar.
7. Python için "Kafe" ile "kafe" iki ayrı anahtar; model de ikisine ayrı birer vektör
   verir. "Kafe"nin skoru tam 1.0 olmaz; ama iki yazılış aynı kelime olduğu için
   üst sıralarda görmeyi beklersin. Gerçekten öyle mi, kendi çıktında dene. (Bir de:
   `hedef = "Kafe"` yazıp listeye eklemeyi unutursan `KeyError: 'Kafe'` alırsın; hedefi
   listede nasıl yazdıysan öyle yazmalısın.)
8. "Daha doğru" değil, "farklı bir soruya cevap". Bizim eksenlerimiz bir tasarımcının
   bu kelimelere bakışı (sıcaklık, enerji); modelin eksenleri bu kelimelerin metinlerde
   nasıl kullanıldığı. Bir marka için hangisinin işe yaradığı, ne sorduğuna bağlı.
   Konu 3'teki gibi: test hangi soruyu soruyor?
