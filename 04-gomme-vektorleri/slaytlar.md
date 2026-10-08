# Konu 4 — Temsil ve Gömme Vektörleri

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 3'ten Konu 4'e

**Konu 3'te:** bir rengi üç sayıya çevirdik: `[230, 57, 70]`.
Model "benzer" renkleri bu üç sayıya bakarak buldu.

**Ve bir sorun gördük:** gri mavi ile gül kurusu RGB'de yakın, gözümüzde çok uzak.
Benzerlik, seçtiğimiz sayılara bağlı.

**Bu konuda:** kelimeleri sayıya çevireceğiz.

- Önce elle: iki sayıyla
- Sonra modelle: yüzlerce sayıyla
- Sonunda kelimelerin haritası

-----

## Konunun planı

**Isınma** — elle iki eksenli harita
**1.** Anahtarı oku
**2.** Bir kelimenin vektörü
**3.** Fonksiyona koy
**4.** İki kelime ne kadar benzer?
**5.** 24 kelimelik sözlük
**6.** "kafe"ye en yakın 3 kelime — **sen yazıyorsun**
**7.** Harita
**8.** Haritayı oku

Hepsi tek defterde: `ders.ipynb`. Isınma anahtarsız çalışır.

-----

## Temsil: her şey sayıya çevrilir

Bilgisayar "kahve" kelimesini anlamaz. Sayı ister.

| Şey | Temsili |
|---|---|
| Renk | 3 sayı (R, G, B) |
| Fotoğraf | her piksel için 3 sayı |
| Ses | saniyede binlerce sayı |
| Kelime | **?** |

Bir kelimeyi hangi sayılarla temsil edersen, "benzer" kelimesinin anlamını da o belirler.

-----

## Isınma — elle bir mood-board

İki eksen:

- **sıcaklık:** soğuk −1 … sıcak +1
- **enerji:** sakin −1 … canlı +1 (Konu 3'teki sakin / enerjik gibi)

```python
kahve = [0.6, 0.4]
cay = [0.5, -0.4]
buz = [-0.9, 0.1]
deniz = [-0.5, -0.5]
ates = [0.9, 0.9]
kar = [-0.7, -0.2]

print(cay)
```

> [0.5, -0.4]

-----

## Adları olan bir sözlük

Anahtar: kelimenin adı · değer: iki sayısı

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

> [0.9, 0.9]

-----

## Haritayı çiz

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

- `for kelime in harita`: sözlüğün anahtarlarını (kelimeleri) gezer
- `plt.scatter`: bir nokta koy
- `plt.text`: noktanın yanına kelimeyi yaz
- `axhline` / `axvline`: gri sıfır çizgileri

-----

## Kelime = bir ok

Her kelime, haritanın ortasından (0, 0) çıkan bir **ok** gibi düşünülebilir.

- Kahve sağ üste bakıyor: sıcak ve biraz canlı
- Ateş de sağ üste bakıyor, sadece oku daha uzun
- Deniz sol alta bakıyor: ateşin tam tersi

**Aynı yöne bakan iki ok benzerdir.** Uzunluk önemli değil, yön önemli.

-----

## Benzerlik: hazır bir araç

```python
from sklearn.metrics.pairwise import cosine_similarity

def benzerlik(a, b):
    sonuc = cosine_similarity([a], [b])
    satir = sonuc[0]
    return satir[0]
```

İçini bilmen gerekmiyor. Verdiği sayıyı okuman yeter:

| Sayı | Anlamı |
|---|---|
| **1** | aynı yön |
| **0** | ilgisiz |
| **−1** | zıt yön |

-----

## Ölçelim

```python
print(benzerlik(kahve, cay))
print(benzerlik(kahve, buz))
```

> 0.3032036572769468
> -0.765704864789611

| İkili | Benzerlik | Neden |
|---|---|---|
| kahve – ateş | 0.98 | aynı yön, ateşin oku daha uzun |
| kahve – çay | 0.30 | ikisi de sıcak; biri canlı, biri sakin |
| kahve – buz | −0.77 | karşı taraflarda |
| ateş – deniz | −1.0 | tam zıt yön |

-----

## Model eksenleri kendisi bulur

Isınmada eksenleri **biz** seçtik: sıcaklık ve enerji.

Bir dil modeli milyonlarca metin okur ve kelimeleri bir haritaya yerleştirir:

- Eksenlerin adı yok; model kendisi bulur
- 2 eksen değil, **yüzlerce**
- Aynı tür cümlelerde geçen kelimeler yakın düşer

Bu sayı listesine **vektör**, bu çeviriye **gömme** (embedding) diyoruz.

Modelin kaç sayı verdiğini kendi çıktında göreceksin.

-----

## Adım 1 — Anahtarı oku

Konu 2'deki hücrenin aynısı.

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

-----

## Adım 2 — Bir kelimenin vektörü

Konu 2'deki istek, iki farkla: **model** ve **gövde**.

```python
import requests

MODEL = "@cf/google/embeddinggemma-300m"
adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
basliklar = {"Authorization": f"Bearer {anahtar}"}
govde = {"text": ["kahve"]}
```

```python
cevap = requests.post(adres, headers=basliklar, json=govde)
print(cevap.status_code)
```

> 200

Model Google'ın; 100'den çok dil biliyor. Türkçe kelimeler için bu önemli.

-----

## Yanıta katman katman in

```python
yanit = cevap.json()
sonuc = yanit["result"]
vektorler = sonuc["data"]
vektor = vektorler[0]
```

```python
print(len(vektor))
print(vektor[:5])
```

- `data` bir **liste**: tek istekte birden çok metin gönderebiliriz
- Biz tek kelime gönderdik; ilki bizim: `vektorler[0]`
- `vektor[:5]`: ilk beş sayı (Konu 1'in dilimlemesi)

Kaç sayı çıktı? Isınmada 2'ydi.

-----

## Adım 3 — Fonksiyona koy

Konu 2'deki `modele_sor`'un kardeşi:

```python
def vektor_al(kelime):
    govde = {"text": [kelime]}
    cevap = requests.post(adres, headers=basliklar, json=govde)
    yanit = cevap.json()
    sonuc = yanit["result"]
    vektorler = sonuc["data"]
    return vektorler[0]
```

```python
vektor = vektor_al("çay")
print(len(vektor))
```

-----

## Adım 4 — Önce tahmin et

**Kahve hangisine daha çok benzer: çaya mı, tipografiye mi?**

```python
kahve = vektor_al("kahve")
cay = vektor_al("çay")
tipografi = vektor_al("tipografi")
```

```python
print(benzerlik(kahve, cay))
print(benzerlik(kahve, tipografi))
```

- Isınmadaki `kahve` 2 sayıydı; aynı ad artık modelin vektörü
- `benzerlik` ikisiyle de çalışır
- Sayılara tek başına değil, **yan yana** bak: hangisi büyük?

-----

## Adım 5 — 24 kelime, 4 grup

```python
kelimeler = [
    "kırmızı", "mavi", "yeşil", "bej", "siyah", "beyaz",
    "huzur", "öfke", "neşe", "hüzün", "heyecan", "sakinlik",
    "tipografi", "logo", "afiş", "palet", "kontrast", "serif",
    "kafe", "kütüphane", "park", "ofis", "atölye", "sahne",
]
print(len(kelimeler))
```

```python
vektorler_sozlugu = {}
for kelime in kelimeler:
    vektorler_sozlugu[kelime] = vektor_al(kelime)

print(len(vektorler_sozlugu))
```

**bej**: Konu 3'te kafe paleti için modele sorduğumuz renk.

24 istek: hücre biraz sürer; solunda `[*]` durur, bitince `24` yazar.

**Beklerken tahmin et:** "kafe" bu 24 kelimeden hangi üçüne en yakın çıkar? Not al.

-----

## Adım 6 — Sen yaz: "kafe"ye en yakın 3 kelime

Plan:

1. `skorlar` adında boş bir sözlük
2. Her kelime için: "kafe" ile benzerliğini hesapla, `skorlar[kelime]`'ye koy
3. Konu 1'in `Counter`'ı ile en büyükleri sırala

İpucu, Konu 1'den:

```py
for kelime, adet in sayac.most_common(10):
    print(adet, kelime)
```

**5 dakika.** Sonra birlikte bakalım.

-----

## Adım 6 — Birlikte

```python
hedef = "kafe"
hedef_vektor = vektorler_sozlugu[hedef]

skorlar = {}
for kelime in vektorler_sozlugu:
    vektor = vektorler_sozlugu[kelime]
    skorlar[kelime] = benzerlik(hedef_vektor, vektor)

print(len(skorlar))
```

```python
from collections import Counter

sirali = Counter(skorlar)
for kelime, skor in sirali.most_common(4):
    print(kelime, round(skor, 2))
```

`Counter`'a hazır sözlük verince saymaz; sayıları büyükten küçüğe dizer.

-----

## Neden 4?

İlk satıra bak: **kafe 1.0**. Her kelime kendisine tam benzer.
3 komşu için 4 satır istiyoruz.

Konu 1'de müşteriler bu kafeyi **sessiz bir çalışma yeri** diye anlatmıştı.

- Model "kafe"yi neye yakın buluyor: kütüphaneye mi, parka mı, sahneye mi?
- Müşterilerin gözündeki kafe ile modelin gözündeki kafe aynı mı?
- Aynı değilse: slogan "kafe" kelimesine yaslanamaz

`hedef = "kafe"` yerine `"huzur"` yaz: kafenin vermek istediği his hangi renge yakın?

-----

## Adım 7 — Yüzlerce sayıyı 2'ye indirmek

Kâğıt iki boyutlu. **PCA**, yüzlerce sayıyı en çok şey anlatan 2 sayıya indirir.

Bir heykelin duvara düşen **gölgesi** gibi: şekli tanırsın ama derinlik kaybolur.

```python
liste = []
for kelime in vektorler_sozlugu:
    liste.append(vektorler_sozlugu[kelime])

print(len(liste))
```

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
pca.fit(liste)
```

-----

## Her kelime 2 sayı

```python
model_haritasi = {}
for kelime in vektorler_sozlugu:
    vektor = vektorler_sozlugu[kelime]
    noktalar = pca.transform([vektor])
    model_haritasi[kelime] = noktalar[0]

print(model_haritasi["kafe"])
```

-----

## Haritayı çiz

```python
for kelime in model_haritasi:
    nokta = model_haritasi[kelime]
    plt.scatter(nokta[0], nokta[1], color="#4a6fa5")
    plt.text(nokta[0], nokta[1], kelime)

plt.show()
```

- `fit`: "önce bütün vektörlere bak" (Konu 3'teki gibi)
- `transform`: "bu vektörü 2 sayıya çevir"; Konu 3'teki `predict` gibi liste ister: `[vektor]`
- Isınmadaki çizim döngüsünün aynısı

-----

## Harita bir özettir

Yüzlerce sayıyı 2'ye indirdik. **Bilgi kaybettik.**

- Haritada yan yana duran iki kelime gerçekte o kadar yakın olmayabilir
- Uzak duran iki kelime gerçekte yakın olabilir
- Emin olmak için asıl sayıya bak: `benzerlik(...)`

Bir şehir haritası gibi: yolu bulmana yeter, ama binaların yüksekliğini göstermez.

-----

## Adım 8 — Haritayı oku

- Dört grup ayrı kümeler oluşturdu mu?
- Kendi grubundan kaçan bir kelime var mı? Nereye gitmiş?
- Hangi renk duyguların kümesine en yakın? Bej nereye düştü?
- **huzur** ile **öfke** zıt anlamlı. Haritada uzak mı düştüler?

```python
huzur = vektorler_sozlugu["huzur"]
ofke = vektorler_sozlugu["öfke"]
sakinlik = vektorler_sozlugu["sakinlik"]

print(benzerlik(huzur, ofke))
print(benzerlik(huzur, sakinlik))
```

-----

## Benzer, eşanlamlı demek değil

Model kelimelerin anlamını sözlükten değil, **hangi cümlelerde geçtiklerinden** öğrenir.

> "Bugün içimde büyük bir ___ var."

Boşluğa hem "huzur" hem "öfke" gelebilir. İkisi de aynı tür cümlelerde geçer.
Bu yüzden zıt anlamlı iki kelime de yakın düşebilir.

Modelin "benzer"i = **benzer yerlerde geçen**.

Mood-board için "huzur"a yakın kelimeler istersen, araya öfke de girebilir.

-----

## Bonus — Kendi 5 kelimen

```python
yeni_kelimeler = ["espresso", "minimal", "gürültü", "sessizlik", "poster"]
for kelime in yeni_kelimeler:
    vektorler_sozlugu[kelime] = vektor_al(kelime)

print(len(vektorler_sozlugu))
```

Kendi kelimelerini yaz. Sonra Adım 7'nin dört hücresini sırayla yeniden çalıştır.

Örnek listede: "sessizlik" kafeye mi düştü, kütüphaneye mi?

-----

## Sekiz adım, tek defter

| Adım | Ne yaptık | Elimizde |
|---|---|---|
| Isınma | Elle iki sayılık harita, benzerlik | `harita`, `benzerlik` |
| 1–2 | Modelden bir kelimenin vektörü | `vektor` |
| 3 | Fonksiyona koyduk | `vektor_al` |
| 4 | İki kelimeyi kıyasladık | — |
| 5 | 24 kelimenin vektörü | `vektorler_sozlugu` |
| 6 | En yakın komşular | `skorlar` |
| 7 | 2 boyuta indirip çizdik | harita |
| 8 | Haritayı okuduk | — |

-----

## Üç yeni kavram, üç cümle

**Vektör (gömme).** Model bir kelimeyi bir sayı listesine çevirir; sayıların tek tek
anlamı yok, anlam kelimelerin birbirine göre nerede durduğunda.

**Benzerlik.** Aynı yöne bakan iki vektör benzerdir: 1 aynı yön, 0 ilgisiz, −1 zıt.
Modelin "benzer"i, "benzer yerlerde geçen" demek.

**Boyut indirgeme.** Yüzlerce sayıyı 2'ye indirip haritaya çizebiliriz; ama harita bir
özettir, bilgi kaybeder.

-----

## Bu konunun ödevi

Kendi seçtiğin **20 kelimeyle** bir harita çıkar.

1. Defteri kopyala, Adım 5'teki listeye kendi 20 kelimeni yaz
2. Adım 7'ye kadar çalıştır, haritayı kaydet
3. **Tek cümle:** beklemediğin hangi iki kelime yan yana düştü?
4. **Tek cümle daha:** bu haritayla bir mood-board'a başlasan neyi ekler, neyi çıkarırdın?

Ayrıntılar: `odevler/odev4.md`. Puan yok; Konu 5'in başında sıradaki arkadaşlar gösterecek.

-----

## Sonraki konu: Konu 5

**Dil modelleri nasıl çalışır?**

Bu konuda model kelimeleri sayıya çevirdi.
Konu 5'te modelin **metni nasıl yazdığına** bakacağız:

- Metin önce parçalara bölünür
- Model her seferinde bir sonraki parçayı tahmin eder
- "Sıcaklık" ayarı, en olası parçayı mı seçeceğini, zar mı atacağını belirler
