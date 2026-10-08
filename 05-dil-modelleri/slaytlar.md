# Konu 5 — Dil Modelleri Nasıl Çalışır?

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 4'ten Konu 5'e

**Konu 2'de:** modele soru sorduk, cevap aldık. Model bir kutuydu.
**Konu 4'te:** model kelimeyi sayı listesine çeviriyordu.

**Bu konuda:** model **nasıl yazıyor**, ona bakacağız.

- Model metni kelime kelime değil, **parça parça** okur
- Her adımda tek bir şey yapar: **sıradaki parçayı tahmin eder**
- Uzun bir metin, bu tahminin **tekrarıdır**
- Bir ayarla "hep en olasıyı seç" ile "zar at" arasında gidip gelir: **sıcaklık**

Sihir yok. Sayma ve seçme var.

-----

## Bugünün planı

Hepsi tek bir defterde: `ders.ipynb`

**Isınma** — cümleyi tamamla
**1.** Model metni nasıl görür: belirteçler
**2.** Hangi kelimeden sonra ne geliyor?
**3.** Sayıdan olasılığa
**4.** Metin üret: hep en olasıyı seç
**5.** Zar at
**6.** Gerçek model ve sıcaklık
**7.** Slogan panosu

Isınma ve Adım 1–5 **anahtarsız**. Adım 6–7 `anahtar.txt` ister.

-----

## Isınma — cümleyi tamamla

*"Sessiz bir çalışma ..."* — sonunu ne getirirsin? Altı kişinin cevabı:

```python
from collections import Counter

cevaplar = ["kafesi", "kafesi", "yeri", "odası", "kafesi", "yeri"]
sayac = Counter(cevaplar)
print(sayac.most_common(2))
```

Çıktı: `[('kafesi', 3), ('yeri', 2)]`

Sıradaki kelimeyi tahmin etmenin en basit yolu: **en sık söyleneni seç.**
Bu konunun bütün fikri bu hücrede.

-----

## Adım 1 — Önce tarayıcıda

`tiktokenizer.vercel.app` sitesini aç, kutuya *"Sessiz bir çalışma kafesi"* yaz.

- Her renkli kutu bir **belirteç** (token): modelin okuduğu en küçük parça
- Kısa, sık kelimeler tek parça
- Uzun ya da seyrek kelimeler birkaç parçaya bölünür
- Boşluk da parçanın içinde

Şimdi aynısını kodla yapalım.

-----

## Adım 1 — Belirteçlere ayır

```python
import tiktoken

kodlayici = tiktoken.get_encoding("o200k_base")
belirtecler = kodlayici.encode("Sessiz bir çalışma kafesi")
print(len(belirtecler))
print(belirtecler)
```

Çıktı: `6` ve `[174397, 482, 3742, 162348, 61617, 14988]`

- `encode`: metni parçalara, parçaları **sayılara** çevirir
- Model kelimeyi değil, bu sayıları görür
- İlk çalıştırmada `tiktoken` internetten bir sözlük indirir

-----

## Adım 1 — Parçaları geri çevir

```python
for belirtec in belirtecler:
    print(kodlayici.decode([belirtec]))
```

| Kelime | Parçalar |
|---|---|
| Sessiz | `Sess` + `iz` |
| bir | ` bir` |
| çalışma | ` çalışma` |
| kafesi | ` kaf` + `esi` |

Dört kelime, altı parça. `decode` **liste** ister: `[belirtec]`.

-----

## Adım 1 — Türkçe daha pahalı

```python
ingilizce = kodlayici.encode("A quiet cafe for working")
print(len(ingilizce))
```

```python
uzun = kodlayici.encode("Kütüphanedekilerden misiniz?")
print(len(uzun))
for belirtec in uzun:
    print(kodlayici.decode([belirtec]))
```

| Cümle | Kelime | Parça |
|---|---|---|
| Sessiz bir çalışma kafesi | 4 | 6 |
| A quiet cafe for working | 5 | 5 |
| Kütüphanedekilerden misiniz? | 2 | 11 |

-----

## Bağlam penceresi

Model bir seferde **sınırlı sayıda parça** okuyabilir. Bu sınıra **bağlam penceresi** denir.

- Uzun bir sohbette ilk yazdıkların pencereden taşar: model "unutur"
- Türkçe aynı sözü daha çok parçayla söyler: pencere **daha çabuk dolar**
- Ücretli modellerde fiyat da parça başına: Türkçe metin daha pahalı

Her modelin kendi parça sözlüğü var. Bizimki (`o200k_base`) bir örnek;
derste kullandığımız Llama'nınki farklı, ama fikir aynı.

-----

## Adım 2 — Konu 1'in yorumları

```python
with open("veri/kafe-yorumlari.txt", encoding="utf-8") as dosya:
    metin = dosya.read()

temiz = metin.replace("I", "ı")
temiz = temiz.replace("İ", "i")
temiz = temiz.lower()
for isaret in ".,;:!?'()-":
    temiz = temiz.replace(isaret, " ")

kelimeler = temiz.split()
print(len(kelimeler))
```

Çıktı: `298`. Konu 1'deki 30 yorum, Konu 1'deki temizlik satırları.

-----

## Adım 2 — "biraz"dan sonra ne geliyor?

```python
hedef = "biraz"
sonra_gelenler = []
onceki = ""
for kelime in kelimeler:
    if onceki == hedef:
        sonra_gelenler.append(kelime)
    onceki = kelime

print(sonra_gelenler)
```

- `onceki`: bir önceki turdaki kelime
- Önceki "biraz" ise bu kelimeyi listeye ekle
- Son satır: bu kelimeyi bir sonraki tur için hatırla

-----

## Bulgu: şikâyetler "biraz"dan sonra

Çıktı: `['pahalı', 'karanlık', 'kısa', 'fazla']`

- Müşteriler kafeyi överken "biraz" demiyor
- Şikâyet edecekleri zaman yumuşatıyorlar: **biraz** pahalı, **biraz** karanlık
- Konu 1'de ışık sorununu bağlamda okuyarak bulmuştuk; burada da bir kelimenin **komşusu** bize yol gösterdi

Bir kelimenin ne anlattığını, ardından gelenler söyler.

-----

## Adım 2 — Fonksiyona koy

Aynı satırları "çok" için yeniden yazmak yerine:

```python
def sonra_gelenleri_bul(hedef):
    sonra_gelenler = []
    onceki = ""
    for kelime in kelimeler:
        if onceki == hedef:
            sonra_gelenler.append(kelime)
        onceki = kelime
    return sonra_gelenler
```

- İçerisi yukarıdaki hücrenin aynısı
- `return`: listeyi geri ver (Konu 2'deki `modele_sor` gibi)

-----

## Adım 2 — "çok"tan sonra

```python
sonra_gelenler = sonra_gelenleri_bul("çok")
print(sonra_gelenler)
```

```python
sayac = Counter(sonra_gelenler)
print(sayac.most_common(5))
```

Çıktı: `[('güzel', 2), ('kalabalık', 1), ('keyifli', 1), ('tatlı', 1)]`

-----

## Adım 3 — Sayıdan olasılığa

```python
toplam = len(sonra_gelenler)
etiketler = []
olasiliklar = []
for kelime, adet in sayac.most_common(5):
    olasilik = adet / toplam
    etiketler.append(kelime)
    olasiliklar.append(olasilik)
    print(kelime, olasilik)
```

| Kelime | Adet | Olasılık |
|---|---|---|
| güzel | 2 | 0.4 |
| kalabalık | 1 | 0.2 |
| keyifli | 1 | 0.2 |
| tatlı | 1 | 0.2 |

Toplamı: **1**. Olasılık = adet / toplam.

-----

## Adım 3 — Dağılımı çiz

```python
import matplotlib.pyplot as plt

plt.bar(etiketler, olasiliklar, color="#4a6fa5")
plt.title("'çok' kelimesinden sonra ne geliyor?")
plt.ylabel("Olasılık")
plt.show()
```

Bir dil modeli de **her adımda** böyle bir grafik hesaplar:
"bundan sonra hangi parça, hangi olasılıkla?"

Farkı: 30 yorumdan değil, milyarlarca metinden öğrenmiş olması.

-----

## Adım 4 — En olası kelime

```python
def sonraki_kelime(hedef):
    sonra_gelenler = sonra_gelenleri_bul(hedef)
    sayac = Counter(sonra_gelenler)
    en_sik = sayac.most_common(1)
    kelime, adet = en_sik[0]
    return kelime
```

```python
print(sonraki_kelime("çok"))
```

- Listeyi Adım 2'deki fonksiyondan al, `Counter` ile say
- `most_common(1)`: yalnızca en sık bir kelime, liste içinde: `[('güzel', 2)]`
- `en_sik[0]` bir ikili: kelime ve adedi; ikisini iki değişkene alıyoruz, kelimeyi geri veriyoruz

-----

## Adım 4 — Metin üret

```python
kelime = "kahve"
cumle = kelime
for tur in [1, 2, 3, 4, 5, 6, 7, 8]:
    kelime = sonraki_kelime(kelime)
    cumle = cumle + " " + kelime

print(cumle)
```

Çıktı: `kahve ortalama tatlılar güzel yazın bahçede oturmak için en`

- Her turda: son kelimeye bak, ardından en olası kelimeyi ekle
- Hücreyi tekrar çalıştır: **aynı cümle**
- Dilbilgisi yerinde gibi, anlam yok. Model **anlamaz, sayar**

-----

## Adım 5 — Zar at

```python
import random

print(sonra_gelenler)
print(random.choice(sonra_gelenler))
```

- `random.choice`: listeden rastgele bir eleman
- Listede "güzel" iki kez var → seçilme şansı da iki kat (0.4)
- Hücreyi birkaç kez çalıştır: en sık "güzel" çıkar, ama hep değil

-----

## Adım 5 — Zarla üret

```python
def sonraki_kelime_zarla(hedef):
    sonra_gelenler = sonra_gelenleri_bul(hedef)
    if len(sonra_gelenler) == 0:
        return kelimeler[0]
    return random.choice(sonra_gelenler)
```

```python
kelime = "kahve"
cumle = kelime
for tur in [1, 2, 3, 4, 5, 6, 7, 8]:
    kelime = sonraki_kelime_zarla(kelime)
    cumle = cumle + " " + kelime

print(cumle)
```

Her çalıştırmada **başka** bir cümle.

-----

## Adım 5 — Metin bittiyse baştan başla

- "kahveli" dosyanın **son** kelimesi; ondan sonra hiçbir kelime gelmiyor
- Zar oraya gelirse `sonra_gelenler` boş kalır, `random.choice` seçemez
- `if len(sonra_gelenler) == 0:` → metnin ilk kelimesini (`"ders"`) ver, üretim baştan devam etsin
- Cümlede "kahveli ders" görürsen olan budur

Gerçek modellerde bunun için özel bir parça var: **"metin bitti"**.
Model o parçayı seçince yazmayı bırakır.

-----

## Sıcaklık

| Sıcaklık | Ne yapar | Defterde |
|---|---|---|
| Düşük (0.1) | Hep en olası parçayı seçer | Adım 4: hep aynı cümle |
| Orta (0.7–1) | Olasılığa göre zar atar | Adım 5: zar |
| Yüksek (1.5) | Zar hileli: olasılığı düşük parçalara daha çok şans verir | — |

Sıcaklık yükseldikçe grafikteki çubuklar **birbirine yaklaşır**:
"güzel" ile "tatlı" arasındaki fark küçülür.

Yüksek sıcaklık "daha yaratıcı" değil, **daha dağınık** demek.

-----

## Kendi modelimizden gerçek modele

- Adım 2–5: 30 yorumdan **sayan** küçük bir model kurduk
- Gerçek model de her adımda sıradaki parçayı seçer; ama milyarlarca metinden öğrenmiş
- En olasıyı mı seçsin, zar mı atsın? Bunu **sıcaklık** ayarlar; şimdi onu biz değiştireceğiz

Adım 6–7 `anahtar.txt` ister, önceki hücrelere bağlı değil.

-----

## Adım 6 — Anahtar ve adres

Konu 2'nin Adım 1 hücresinin aynısı:

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

```python
import requests

MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
basliklar = {"Authorization": f"Bearer {anahtar}"}
```

-----

## Adım 6 — Gövdeye sıcaklık

```python
def modele_sor(soru, sicaklik):
    govde = {"prompt": soru, "temperature": sicaklik}
    cevap = requests.post(adres, headers=basliklar, json=govde)
    yanit = cevap.json()
    sonuc = yanit["result"]
    return sonuc["response"]
```

- Konu 2'deki `modele_sor`, tek farkla: ikinci bilgi `sicaklik`
- Gövdede yeni alan: `"temperature"` (sıcaklık)
- Bu model 0 ile 5 arası kabul ediyor; varsayılanı 0.6

-----

## Adım 6 — Üç sıcaklık

```python
soru = "Sessiz bir çalışma kafesi için tek bir kısa slogan yaz. Yalnızca sloganı yaz."

for sicaklik in [0.1, 0.7, 1.5]:
    metin = modele_sor(soru, sicaklik)
    print(sicaklik, metin)
```

**Çalıştırmadan önce tahmin et:** hangisi en "garip" slogan olacak?

-----

## Adım 6 — Aynı soruyu iki kez

```python
ilk = modele_sor(soru, 0.1)
ikinci = modele_sor(soru, 0.1)
print(ilk)
print(ikinci)
```

```python
ilk = modele_sor(soru, 1.5)
ikinci = modele_sor(soru, 1.5)
print(ilk)
print(ikinci)
```

- 0.1'deki iki cevap aynı mı, neredeyse aynı mı?
- 1.5'teki iki cevap ne kadar farklı?
- Hangisi Adım 4'e, hangisi Adım 5'e benziyor?

-----

## Adım 7 — Slogan panosu

```python
pano_sorusu = "Sessiz bir çalışma kafesi için üç kısa slogan yaz. Her slogan ayrı satırda olsun. Yalnızca sloganları yaz."

with open("pano.txt", "w", encoding="utf-8") as dosya:
    for sicaklik in [0.1, 0.7, 1.5]:
        metin = modele_sor(pano_sorusu, sicaklik)
        dosya.write("Sıcaklık " + str(sicaklik) + "\n")
        dosya.write(metin + "\n")
        dosya.write("\n")

print("pano.txt yazıldı")
```

- Modelden tek seferde **üç** slogan istiyoruz
- Her sıcaklık için bir başlık, altına modelin üç sloganı
- `str(sicaklik)`: sayıyı yazıya çevirir, başlığa eklenebilsin diye
- 3 istek gidiyor

-----

## Panoyu tasarımcı gözüyle oku

`pano.txt`'yi aç, üç bölümü yan yana koy.

- **Kurumsal tabela, menü, yönlendirme metni** için hangi sıcaklık?
- **Fikir fırtınası, ilk eskiz** için hangisi?
- 1.5'teki sloganlardan **kullanılabilecek** olan var mı? Kaç tanesi?
- Hangi sıcaklığın üç sloganı birbirinden daha farklı?

Sıcaklık bir **araç ayarı**: işin türüne göre seçilir, "en iyisi" yok.

-----

## Bonus

**1.** Kendi adını belirteçlere ayır:

```python
belirtecler = kodlayici.encode("Ahmet Emre Aladağ")
print(len(belirtecler))
for belirtec in belirtecler:
    print(kodlayici.decode([belirtec]))
```

`Ah` `met` ` Em` `re` ` Al` `ada` `ğ` — 3 kelime, 7 parça. Seninki kaç?

**2.** Adım 4'te `"kahve"` yerine `"sessiz"` ya da `"priz"` yaz.

-----

## En sık görülecek hata mesajları

| Mesaj | Anlamı |
|---|---|
| `ModuleNotFoundError: No module named 'tiktoken'` | Çekirdek `.venv` değil ya da `uv sync` yapılmadı |
| `TypeError: 'int' object is not an instance of 'Sequence'` | `decode`'a liste değil tek sayı verildi: `[belirtec]` |
| `IndexError: list index out of range` | Ardından hiç kelime gelmeyen bir kelimeyle `sonraki_kelime` çağrıldı (`en_sik` boş) |
| `FileNotFoundError: ... '../anahtar.txt'` | Adım 6'dan sonrası anahtar ister |
| `TypeError: 'NoneType' object is not subscriptable` | İstek başarısız; durum koduna bak (Konu 2) |

-----

## Bu konunun ödevi

**1. Üç sıcaklık.** Kendi seçtiğin bir iş için (bir afiş başlığı, bir ürün adı, bir slogan)
soruyu yaz (`soru` ve `pano_sorusu`); Adım 7'yi kendi sorunla çalıştır, `pano.txt` getir.
Tek soru: hangi sıcaklık işe yaradı, neden?

**2. Belirteç sayısı.** Bir Türkçe cümle ve aynı anlamda bir İngilizce cümle seç.
İkisini de belirteçlere ayır. Hangisi kaç parça?

Ayrıntı: `odevler/odev5.md`

-----

## Hatırlanacak dört şey

**1. Model metni parça parça okur.** Türkçe daha çok parçaya bölünür.

**2. Model her adımda sıradaki parçayı tahmin eder.** Uzun metin, bu tahminin tekrarıdır.

**3. Tahmin bir olasılık dağılımıdır.** Model anlamaz; milyarlarca metinden sayar.

**4. Sıcaklık seçimi ayarlar.** Düşük: hep en olası, hep aynı. Yüksek: zar, her seferinde farklı.

Sıradaki konu: **Konu 6 — Kaput açma: üretmek ne demek.**
