# Konu 11 — RAG: Belgeye Dayalı Cevap

Bu not konunun özetidir; derste çalıştırdığımız `ders.ipynb` defteriyle **aynı sırada** ilerler: Isınma, sonra
Adım 1–7 ve kısa bir Bonus. Derste kaçırdığın bir yer olursa buradan oku, sonra defterde o adımın hücrelerini çalıştır.
Nottaki kod blokları defterdeki hücrelerin birebir aynısı.

**Konu 10'a kadar:** modele ne bilmesi gerektiğini biz yazdık: brif, konu, stil. Konu 2'de buna **bağlam** demiştik: soruya
elle eklenen arka plan bilgisi. Gerisini model kendi bildiğiyle tamamladı.
**Bu konuda:** modelin **bilmediği** bir belgeyi ona okutuyoruz. Belge, sessiz çalışma kafemiz **Sayfa Kahve**'nin marka
kılavuzu (`veri/kilavuz.txt`, her satır bir paragraf, 14 paragraf).

> Kılavuzu paragraflara böl ve her paragrafı vektöre çevir → sorunun vektörüne en yakın paragrafları bul →
> "yalnızca şu bilgilere dayanarak cevap ver" + paragraflar + soru → metin modeli.
> Bu yöntemin adı **RAG** (İngilizce *retrieval-augmented generation*, "bulup getirerek üretmek"). Bağlamı biz yazmıyoruz;
> kod onu belgeden bulup getiriyor.

**Konunun sonunda elinde:** kılavuzun vektörleri (`ciktilar/kilavuz_vektorleri.json`), aynı soruya kılavuzsuz ve kılavuzlu
iki cevap, kılavuzda arama yapan `kilavuzda_ara` fonksiyonu ve kılavuza göre çizilmiş bir afiş (`ciktilar/afis_kilavuzlu.jpg`).

**Kurulum:** yeni kütüphane yok. `git pull` ile konu klasörü geldikten sonra `gita3111` klasöründe bir kez `uv sync` çalıştır.

**Anahtar:** Isınma anahtarsız; alıştırma defteri de. Adım 1'den sonrası `anahtar.txt` ister (Konu 2'deki dosya, `gita3111`
klasöründe). Defterin tamamı (Bonus hariç) 5 vektör isteği, 4 metin isteği ve 1 görsel isteği gönderir. Kılavuzun 14
paragrafı tek istekte vektöre çevrilir ve dosyaya kaydedilir; defteri ikinci kez çalıştırdığında bu istek gitmez. Hepsi
ücretsiz günlük kotanın küçük bir kısmı.

> **Bu nottaki çıktılar hakkında.** Isınmanın, Adım 2'nin ve Adım 3'ün çıktıları her bilgisayarda aynıdır. Vektörler,
> puanlar, cevaplar ve görsel gerçek modellerden gelir; senin ekranında başka olabilir. Notta onların yerinde `...` var.

---

## Isınma: kitaba bakarak cevap, kâğıt üstünde

Önce internetsiz, Konu 4'teki gibi elle verilmiş vektörlerle. Dört kısa paragraflık küçük bir kılavuz kuruyoruz. Her
paragrafa üç sayı verdik; her sayı paragrafın bir konudan ne kadar söz ettiğini söylüyor (0 hiç, 1 tamamen):
**renk**, **yazı tipi**, **açılış saati**. Sözlüğün anahtarı paragrafın kendisi, değeri onun üç sayısı.

```python
ornek_kilavuz = {
    "Ana renkler mürekkep mavisi ve kâğıt beyazıdır.": [0.9, 0.1, 0.0],
    "Başlıklarda serifli bir yazı tipi kullanılır.": [0.1, 0.9, 0.0],
    "Kafe hafta içi 08.00–23.00 arası açıktır.": [0.0, 0.0, 1.0],
    "Menü kartları beyaz zemine mavi mürekkeple, serifli başlıklarla basılır.": [0.6, 0.6, 0.0],
}
print(len(ornek_kilavuz))
```

Çıktı: `4`. Menü kartları paragrafı hem renkten hem yazı tipinden söz ediyor; bu yüzden iki sayısı da 0.6.

Konu 4'teki `benzerlik` fonksiyonu aynen geliyor: iki vektör aynı yöne bakıyorsa 1'e yakın, ilgisizse 0'a yakın bir sayı verir.

```python
from sklearn.metrics.pairwise import cosine_similarity

def benzerlik(a, b):
    sonuc = cosine_similarity([a], [b])
    satir = sonuc[0]
    return satir[0]
```

Soru: "Afişte hangi renkleri kullanayım?" Yalnızca renkten söz ediyor; üç sayısı `[1.0, 0.0, 0.0]`. Konu 4'ün Adım 6'sındaki
döngüyle her paragrafa bir puan veriyoruz:

```python
soru = "Afişte hangi renkleri kullanayım?"
soru_vektoru = [1.0, 0.0, 0.0]

skorlar = {}
for paragraf in ornek_kilavuz:
    vektor = ornek_kilavuz[paragraf]
    skorlar[paragraf] = benzerlik(soru_vektoru, vektor)

print(len(skorlar))
```

Çıktı: `4`, her paragraf için bir puan. En büyükleri Konu 4'teki gibi `Counter` sıralar:

```python
from collections import Counter

sirali = Counter(skorlar)
for paragraf, skor in sirali.most_common(2):
    print(round(skor, 2), paragraf)
```

Çıktı:

```
0.99 Ana renkler mürekkep mavisi ve kâğıt beyazıdır.
0.71 Menü kartları beyaz zemine mavi mürekkeple, serifli başlıklarla basılır.
```

Menü kartları ikinci geldi: içinde "beyaz" ve "mavi" de geçiyor. Açılış saatinin puanı 0, çünkü renkle hiçbir ilgisi yok.

Bulduğumuz iki paragrafı, modele gidecek metnin, yani **yönergenin** içine koyuyoruz. `bilgiler` boş bir metinle başlar;
her turda bir paragraf ve bir yeni satır (`"\n"`) eklenir:

```python
bilgiler = ""
for paragraf, skor in sirali.most_common(2):
    bilgiler = bilgiler + paragraf + "\n"

yonerge = "Yalnızca şu bilgilere dayanarak cevap ver:\n" + bilgiler + "Soru: " + soru
print(yonerge)
```

Çıktı:

```
Yalnızca şu bilgilere dayanarak cevap ver:
Ana renkler mürekkep mavisi ve kâğıt beyazıdır.
Menü kartları beyaz zemine mavi mürekkeple, serifli başlıklarla basılır.
Soru: Afişte hangi renkleri kullanayım?
```

RAG'in üç adımının üçü de burada:

1. **Parçala ve vektöre çevir:** belgeyi parçalara böl (burada her parça bir paragraf), her parçaya sayılar ver (biz elle verdik).
2. **Bul:** sorunun vektörüne en yakın paragraflar (`skorlar`, `most_common`).
3. **Yönergeye koy ve sor:** paragraflar + soru. Bu yönergeyi henüz kimseye göndermedik.

Gerçekte sayıları model verir (Konu 4'teki gibi yüzlerce sayı), yönergeyi de metin modeli okur.

---

## Adım 1 — Model Sayfa Kahve'yi tanıyor mu?

`rag_araclari.py` bu klasördeki yardımcı dosya; anahtarı `../anahtar.txt`'den kendisi okur. İçindeki dört fonksiyonu
eski konulardan tanıyorsun:

| Fonksiyon | Ne yapar | Nereden |
|---|---|---|
| `modele_sor(soru, sicaklik)` | Metin modeline sorar, cevabı metin olarak verir; istek başarısız olursa `None` | Konu 5 (Konu 10'daki hâli) |
| `vektor_al(metin)` | Bir metnin gömme vektörünü verir | Konu 4 |
| `vektorleri_al(metinler)` | Bir metin listesini **tek istekte** vektöre çevirir; aynı sırayla bir vektör listesi verir | yeni (Adım 3) |
| `ciz(yonerge, tohum, yol)` | Görseli üretip `yol`a kaydeder; başarılıysa yolu, değilse `None` verir | Konu 8 |

```python
from rag_araclari import modele_sor, vektor_al, vektorleri_al, ciz
```

`anahtar.txt` yoksa bu satır `FileNotFoundError` verir; Adım 2 yine çalışır.

Önce kılavuz olmadan soruyoruz. Sıcaklık 0.2, yani düşük: yaratıcılık değil, bilgi istiyoruz (Konu 5).

```python
soru = "Sayfa Kahve'nin afişinde hangi renkleri kullanmalıyım?"

kilavuzsuz = modele_sor(soru, 0.2)
print(kilavuzsuz)
```

Çıktı: `...` (modelin cevabı). Okurken üç şeye bak:

- Model Sayfa Kahve'yi tanımadığını söyledi mi?
- Renk önerdiyse bu renkleri nereden buldu? Herhangi bir kafe için de aynılarını önermez miydi?
- Cevap kendinden emin mi, yoksa "genellikle", "olabilir" gibi çekinceler var mı?

Sayfa Kahve uydurma bir marka; kılavuzu modelin eğitim verisinde yok. Gerçek bir marka olsaydı da müşterinin geçen hafta
yazdığı kılavuz orada olmazdı. Model bilmediği yerde boşluğu en olası görünen metinle doldurur. Konu 5'te buna
**uydurma** (halüsinasyon) demiştik.

---

## Adım 2 — Kılavuzu parçala

`veri/kilavuz.txt` Sayfa Kahve'nin marka kılavuzu. Her satır bir paragraf, her paragraf tek bir konu: renkler, yasak
renkler, yazı tipi, logo, insan yüzü, fotoğraf ışığı, çizim tarzı, ses tonu, yasak sözcükler, sosyal medya biçimi, mevsim
vurgusu, menü kartı, açılış saatleri.

RAG'in ilk işi belgeyi **parçalara** bölmek. Bizim kılavuzda bir parça bir satır. Adı Konu 5'tekiyle aynı ama anlamı başka:
orada parça bir belirteçti (kelimenin bir kırıntısı); burada belgenin kendi başına okunabilen bir bölümü, bir paragraf.

Dosyayı Konu 2'de `anahtar.txt`'yi okuduğumuz gibi satır satır okuyoruz: `.strip()` satır sonundaki görünmez `\n`'yi siler,
`if` boş satırları dışarıda bırakır.

```python
paragraflar = []
with open("veri/kilavuz.txt", encoding="utf-8") as dosya:
    for satir in dosya:
        paragraf = satir.strip()
        if paragraf != "":
            paragraflar.append(paragraf)

print(len(paragraflar))
print(paragraflar[2])
```

Çıktı:

```
14
Kırmızı ve turuncu Sayfa Kahve'nin hiçbir tasarımında kullanılmaz. Bu renkler aceleyi ve indirimi çağrıştırır; marka ise sakinlik vaat eder.
```

Sıra numarası `2` üçüncü paragraf demek: Python saymaya 0'dan başlar. Adım 1'deki cevapta kırmızı ya da turuncu var mıydı?

**Neden paragraf?** Bir parça tek bir konuyu kendi başına anlatmalı. Parça bütün bir sayfa olsaydı, renk sorusuna açılış
saatleri de gelirdi; tek bir cümle olsaydı, "kırmızı kullanılmaz" gelir ama gerekçesi ("aceleyi ve indirimi çağrıştırır")
gelmeyebilirdi.

---

## Adım 3 — Paragrafları vektöre çevir ve sakla

Konu 4'te 24 kelime için 24 ayrı istek göndermiştik. O konunun yan notunda dediğimiz gibi, model tek istekte bir liste de
alabiliyor: `vektorleri_al(paragraflar)` 14 paragrafı **tek istekte** gönderir ve aynı sırayla 14 vektör verir.

Kılavuz değişmedikçe vektörleri de değişmez; her çalıştırmada yeniden istemenin anlamı yok. Konu 10'un kuralı:
**ara çıktıyı sakla.** Önce dosyanın yerini belirliyoruz:

```python
import json
from pathlib import Path

klasor = Path("ciktilar")
klasor.mkdir(exist_ok=True)
vektor_dosyasi = klasor / "kilavuz_vektorleri.json"
```

Sonraki hücre Konu 10'daki slogan halkasının kalıbıyla çalışır. Önce sorar: **zaten var mı?**

- Dosya varsa okur; modele hiç istek gitmez.
- Yoksa vektörleri ister, her paragrafı kendi vektörüyle eşleştirir, sözlüğü dosyaya yazar.

Eşleştirme: birinci paragrafa birinci vektör, ikinciye ikinci... `sira` sayacı hangi vektörde olduğumuzu tutar (Konu 6'da her
A'yı türüyle böyle eşleştirmiştik: `turler[sira]`).
Sözlüğün anahtarı paragrafın kendisi, değeri onun vektörü (Konu 4'teki `vektorler_sozlugu` gibi).

```python
if vektor_dosyasi.exists():
    with open(vektor_dosyasi, encoding="utf-8") as dosya:
        kilavuz_vektorleri = json.load(dosya)
    print("Dosyadan okundu, istek gitmedi")
else:
    vektorler = vektorleri_al(paragraflar)
    kilavuz_vektorleri = {}
    sira = 0
    for paragraf in paragraflar:
        kilavuz_vektorleri[paragraf] = vektorler[sira]
        sira = sira + 1
    with open(vektor_dosyasi, "w", encoding="utf-8") as dosya:
        json.dump(kilavuz_vektorleri, dosya, ensure_ascii=False)
    print("Vektörler alındı ve kaydedildi")

print(len(kilavuz_vektorleri))
```

İlk çalıştırmada çıktı `Vektörler alındı ve kaydedildi` ve `14`; bir istek gider. İkinci çalıştırmada
`Dosyadan okundu, istek gitmedi` ve `14`; hiç istek gitmez.

`ciktilar/kilavuz_vektorleri.json`'u VS Code'da açarsan her paragrafın yanında yüzlerce sayı görürsün: kılavuzun modelin
gözündeki hâli.

> **Kılavuzu değiştirirsen** (bir kural ekler, bir paragrafı düzeltirsen) `ciktilar/kilavuz_vektorleri.json`'u sil ve Adım 2'den
> yeniden çalıştır. Silmezsen hücre eski dosyayı okur; arama eski kılavuzda yapılır ve yeni kural hiç bulunmaz. Hata da
> vermez: sessiz bir yanlış.

---

## Adım 4 — Soruya en ilgili paragraflar

Sorunun (Adım 1'deki renk sorusu) vektörü:

```python
soru_vektoru = vektor_al(soru)
print(len(soru_vektoru))
```

Çıktı: `...` (Adım 3'teki paragraf vektörleriyle aynı uzunluk). İki vektör ancak aynı uzunluktaysa karşılaştırılabilir.

Bu adımı derste **sen yazdın**. Plan ısınmadakiyle ve Konu 4'ün Adım 6'sıyla aynı: boş bir `skorlar` sözlüğü; her paragraf
için sorunun vektörüyle paragrafın vektörünün benzerliği; `Counter` ile en büyük üçü. Bir çözüm:

```python
skorlar = {}
for paragraf in kilavuz_vektorleri:
    vektor = kilavuz_vektorleri[paragraf]
    skorlar[paragraf] = benzerlik(soru_vektoru, vektor)

sirali = Counter(skorlar)
for paragraf, skor in sirali.most_common(3):
    print(round(skor, 2), paragraf)
```

Çıktı: `...` (üç puan ve üç paragraf). Isınmadan farklı olarak puanlar 0.99 gibi yüksek çıkmayabilir; Konu 4'teki gibi
sayılara tek başına değil, **yan yana** bak.

**Renk bilgisi altı paragrafa dağılmış:** ana renkler, yasak renkler, fotoğraf ışığı (renkler hafif soluk), çizim tarzı
(mavi ve beyaz risograf), mevsim vurgusu (kışın hardal), menü kartı. Biz yalnızca ilk üçü alıyoruz; ilk üçe girmeyen
paragraf modele **hiç gitmez**. Senin çıktında hangileri dışarıda kaldı? Bir afiş için dışarıda kalmaması gereken hangisiydi?

---

## Adım 5 — Yönerge şablonu: kılavuza bakarak sor

Önce ilk üç paragrafı tek bir metinde topluyoruz (ısınmadaki döngü):

```python
bilgiler = ""
for paragraf, skor in sirali.most_common(3):
    bilgiler = bilgiler + paragraf + "\n"

print(bilgiler)
```

Yönerge üç kısımdan oluşur: **talimat + bilgiler + soru**. Talimat modele iki şey söyler: yalnızca bu bilgilere dayan;
bilgilerde cevap yoksa bunu açıkça söyle.

```python
talimat = "Yalnızca aşağıdaki bilgilere dayanarak cevap ver. Bilgilerde cevap yoksa yalnızca 'Bilmiyorum' yaz."
```

Şablonu derste **sen yazdın**: talimat, iki yeni satır, `Bilgiler:` başlığı ve bilgiler, bir yeni satırla `Soru: ` ve soru.
Bir çözüm:

```python
yonerge = talimat + "\n\nBilgiler:\n" + bilgiler + "\nSoru: " + soru
print(yonerge)
```

Çıktının biçimi şöyle (paragraflar senin Adım 4 çıktına göre değişir):

```
Yalnızca aşağıdaki bilgilere dayanarak cevap ver. Bilgilerde cevap yoksa yalnızca 'Bilmiyorum' yaz.

Bilgiler:
...
...
...

Soru: Sayfa Kahve'nin afişinde hangi renkleri kullanmalıyım?
```

`"Bilgiler:"` başlığı ve boş satırlar model için de işe yarar: hangi metnin kaynak, hangisinin soru olduğu görünür.
Yönergeyi gönderip iki cevabı alt alta yazdırıyoruz (bir istek gider):

```python
kilavuzlu = modele_sor(yonerge, 0.2)

print("KILAVUZSUZ:", kilavuzsuz)
print()
print("KILAVUZLU:", kilavuzlu)
```

Çıktı: `...` (iki cevap). Karşılaştırırken sor:

- Kılavuzlu cevapta mürekkep mavisi ve kâğıt beyazı var mı? Renk kodları (`#1F3A5F`, `#F4F1EA`) kılavuzdakilerle aynı mı?
- Kırmızı–turuncu yasağından söz ediyor mu? Etmiyorsa Adım 4'e dön: o paragraf ilk üçe girmiş miydi?
- Kılavuzlu cevap, bilgilerde olmayan bir şey ekledi mi?

Model yalnızca yönergede gördüğünü bilir; kendisine gelmeyen bir paragrafı bilemez. **RAG'de cevap, bulma adımından daha
iyi olamaz.**

---

## Adım 6 — Fonksiyona koy: `kilavuzda_ara`

Adım 4 ve 5'te yazdıklarını iki fonksiyona koyuyoruz. Yeni bir soru sormak artık tek satır.

`kilavuzda_ara(soru)` soruyu alır ve kılavuzun en ilgili üç paragrafını **tek bir metin** olarak verir. Konu 12'de bu
fonksiyon ajanın araçlarından biri olacak; adı ve işi aynı kalacak.

```python
def kilavuzda_ara(soru):
    soru_vektoru = vektor_al(soru)
    skorlar = {}
    for paragraf in kilavuz_vektorleri:
        vektor = kilavuz_vektorleri[paragraf]
        skorlar[paragraf] = benzerlik(soru_vektoru, vektor)
    sirali = Counter(skorlar)
    bilgiler = ""
    for paragraf, skor in sirali.most_common(3):
        bilgiler = bilgiler + paragraf + "\n"
    return bilgiler
```

Fonksiyonun içindeki `soru_vektoru`, `skorlar`, `sirali` ve `bilgiler` yalnızca fonksiyonun içinde yaşar; dışarıdaki aynı
adlı değişkenlere dokunmaz. Fonksiyon dışarıdan yalnızca `kilavuz_vektorleri`'ni (Adım 3) kullanır.

`kilavuza_sor(soru)` kılavuzda arar, senin şablonunla yönergeyi kurar ve modele sorar:

```python
def kilavuza_sor(soru):
    bilgiler = kilavuzda_ara(soru)
    yonerge = talimat + "\n\nBilgiler:\n" + bilgiler + "\nSoru: " + soru
    return modele_sor(yonerge, 0.2)
```

Bu kez kılavuzda **olmayan** bir soru. Kılavuz menü kartında fiyatların nereye yazılacağını söylüyor (sağa hizalı), ama
fiyatların kendisini söylemiyor.

```python
fiyat_sorusu = "Sayfa Kahve'de bir fincan filtre kahve kaç lira?"

bulunan = kilavuzda_ara(fiyat_sorusu)
print(bulunan)
```

Çıktı: `...` (üç paragraf). **Her zaman üç paragraf gelir.** "En yakın" her zaman vardır; yakın olmak ilgili olmak demek
değil. Gelenlerin arasında "fiyat" sözcüğü geçen bir paragraf olabilir, ama fiyatın kendisi hiçbirinde yok.

```python
fiyat_cevabi = kilavuza_sor(fiyat_sorusu)
print(fiyat_cevabi)
```

Çıktı: `...`. Model "Bilmiyorum" dediyse talimat işe yaradı. Bir fiyat yazdıysa o fiyat verdiğimiz bilgilerin hiçbirinde
yok: talimata rağmen uydurdu. Talimat modeli yönlendirir ama zorlamaz. Konu 5'i hatırla: model kendisine gelen metnin en
olası devamını yazar; talimat da o metne dahil, uyulması zorunlu bir kural değil. **RAG uydurmayı azaltır,
sıfırlamaz.** Cevaptaki her bilgiyi kılavuzla karşılaştırmak yine senin işin.

---

## Adım 7 — Kılavuza uygun bir afiş

Görsel model kılavuzu okumaz; ona yalnızca bir yönerge gider. O yüzden zincir iki halkalı: önce kılavuzdan **görselle
ilgili** kuralları buluyoruz, sonra metin modeline bu kurallara uyan bir görsel yönergesi yazdırıyoruz.

Arama sorusunu dikkatle seçiyoruz: afişin konusunu (sınav haftası) değil, görselin kurallarını arıyoruz.

```python
brif = "Sınav haftasında kafenin gece yarısına kadar açık olduğunu duyuran bir afiş"
arama = "Afiş görselinde hangi renkler ve hangi çizim tarzı kullanılır, neler gösterilmez?"

kurallar = kilavuzda_ara(arama)
print(kurallar)
```

Çıktı: `...`. Renk, çizim tarzı ve insan yüzü kurallarının üçü de geldi mi? Brif afişin **ne söylediğini** anlatıyor
(kafe gece yarısına kadar açık); arama sorusu ise görselin **nasıl görüneceğini** soruyor. Arama, ne sorduysan ona yakın
olanı getirir: brifin kendisini arasaydın başka paragraflar gelirdi.

Görsel model İngilizce yönergeyle daha iyi çalışır (Konu 7). Görselde yazı istemiyoruz: harfleri görsel model bozar,
başlığı tasarımcı dizer (Konu 10). Sıcaklık 0.7: burada biraz yaratıcılık istiyoruz. Uzun isteği üç satırda kuruyoruz;
her satır öncekinin sonuna yeni bir kısım ekliyor.

```python
istek = "Şu kurallara uyan bir afiş görseli için İngilizce, tek paragraflık bir görsel yönergesi yaz. "
istek = istek + "Görselde yazı olmasın. Yalnızca yönergeyi yaz.\n\nKurallar:\n" + kurallar
istek = istek + "\nAfiş: " + brif

gorsel_yonergesi = modele_sor(istek, 0.7)
print(gorsel_yonergesi)
```

Çıktı: `...` (İngilizce bir görsel yönergesi). `ciz` görseli verdiğin yola kaydeder; bir görsel isteği gider:

```python
yol = ciz(gorsel_yonergesi, 42, "ciktilar/afis_kilavuzlu.jpg")
print(yol)
```

Çıktı: `ciktilar/afis_kilavuzlu.jpg`; görsel üretilemediyse `None` ve üstünde durum kodu. Görseli açıp kılavuzla karşılaştır:

- Renkler kılavuza uyuyor mu? Kırmızı ya da turuncu var mı?
- İnsan yüzü var mı?
- Çizim tarzı risografa benziyor mu?

Uymayan bir kural üç yerden birinde kaybolmuştur:

| Nerede kayboldu? | Nasıl anlarsın? | Ne düzeltilir? |
|---|---|---|
| **Aramada:** kural modele hiç gitmedi | `kurallar` çıktısında o paragraf yok | Arama sorusu (ya da kaç paragraf alındığı) |
| **Yönergede:** kural geldi ama metin modeli yönergeye koymadı | `kurallar`'da var, `gorsel_yonergesi`'nde yok | İstek metni (ör. "her kuralı yönergeye yaz") |
| **Çizimde:** kural yönergede vardı ama görsel model uygulamadı | `gorsel_yonergesi`'nde var, görselde yok | Yönergenin dili; bazen hiçbiri: tasarımcı düzeltir |

Ara çıktılara bakmadan hangisinin olduğunu bilemezsin (Konu 10: ara çıktı).

---

## Bonus

**1. Kılavuzsuz afiş.** Aynı brif, kılavuz yok. Bir metin ve bir görsel isteği gider.

```python
istek = "Sayfa Kahve adlı bir kafe için şu afişin görselini anlatan İngilizce, tek paragraflık bir görsel yönergesi yaz. "
istek = istek + "Görselde yazı olmasın. Yalnızca yönergeyi yaz.\n\nAfiş: " + brif

kilavuzsuz_yonerge = modele_sor(istek, 0.7)
print(kilavuzsuz_yonerge)
yol = ciz(kilavuzsuz_yonerge, 42, "ciktilar/afis_kilavuzsuz.jpg")
print(yol)
```

İki afişi yan yana aç: hangisi Sayfa Kahve'ye ait? Tohum aynı (42); farkı yalnızca yönerge yaratıyor.

**2. Kaç paragraf?** Adım 6'daki `kilavuzda_ara` hücresinde `most_common(3)`'ü `most_common(1)` yap ve o hücreyi yeniden
çalıştır. Sonra Adım 1'deki renk sorusunu tek paragrafla sor:

```python
renk_cevabi = kilavuza_sor(soru)
print(renk_cevabi)
```

`kilavuza_sor`'u yeniden çalıştırman gerekmez: o, `kilavuzda_ara`'yı adıyla çağırıyor; yeni hâlini kullanır. Cevap Adım
5'tekine göre ne kadar eksik? Sonra `most_common(14)` dene: her soruda kılavuzun tamamı gider. On dört paragraflık bir
kılavuz için bu olur; iki yüz sayfalık bir kılavuz modelin bağlam penceresine sığmaz (Konu 5), istek pahalılaşır ve küçük
bir kural kalabalıkta kaybolur. Bitince 3'e geri döndür.

**3. Yarım bilgi.** Kılavuz başlık yazı tipini tarif ediyor (serifli, eski kitap baskısını andıran) ama adını vermiyor.

```python
yazi_sorusu = "Sayfa Kahve'nin başlıklarında hangi yazı tipini kullanmalıyım? Yazı tipinin adını yaz."

yazi_cevabi = kilavuza_sor(yazi_sorusu)
print(yazi_cevabi)
```

Model bir yazı tipi adı yazdıysa o ad kılavuzda yok. Tasarımcı için iyi bir öneri olabilir; ama müşteriye "kılavuz böyle
diyor" diye götürülemez. Yarım bilgi, hiç bilgi olmamasından daha kolay uydurmaya yol açar: model eksik kalanı olası
olanla tamamlar.

---

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Anahtar |
|---|---|---|
| Isınma | Elle vektörlerle RAG'in üç adımı: puan, en yakın iki paragraf, yönerge | gerekmez |
| Adım 1 | Hazır araçlar; kılavuzsuz soru | gerekir |
| Adım 2 | Kılavuzu satır satır okuyup paragraflara bölmek | gerekmez |
| Adım 3 | 14 paragrafı tek istekte vektöre çevirmek; JSON'a kaydetmek | gerekir (ilk çalıştırmada) |
| Adım 4 | Sorunun vektörü; en ilgili üç paragraf (sen yazarsın) | gerekir |
| Adım 5 | Yönerge şablonu (sen yazarsın); kılavuzlu cevap | gerekir |
| Adım 6 | `kilavuzda_ara` ve `kilavuza_sor`; kılavuzda olmayan soru | gerekir |
| Adım 7 | Görsel kurallarını aramak; görsel yönergesi; afiş | gerekir |
| Bonus | Kılavuzsuz afiş; kaç paragraf; yarım bilgi | gerekir |

---

## Sık karşılaşılan hatalar ve mesajlarını okumak

| Ne gördün | Ne demek | Ne yap |
|---|---|---|
| `FileNotFoundError: ... '../anahtar.txt'` (Adım 1) | `rag_araclari.py` anahtarı bulamadı | `anahtar.txt` `gita3111` klasöründe mi? Isınma ve alıştırma anahtarsız çalışır |
| `ModuleNotFoundError: No module named 'rag_araclari'` | Defter kopyan `rag_araclari.py` ile aynı klasörde değil | Kopyayı `11-rag` klasörüne taşı |
| `FileNotFoundError: ... 'veri/kilavuz.txt'` | Defter `11-rag` klasöründe değil ya da yol yanlış | Yol defterin durduğu klasöre göre yazılır |
| `RuntimeError: Vektör isteği başarısız, durum kodu: 401 ...` | Anahtar yanlış (404: hesap kimliği yanlış, 429: kota doldu) | `anahtar.txt`'yi düzelt, sonra çekirdeği yeniden başlat (**Restart**): `rag_araclari.py` anahtarı yalnızca ilk `import`'ta okur |
| `NameError: name 'benzerlik' is not defined` (ya da `'Counter'`) | Isınmayı atladın | Isınmanın `benzerlik` ve `Counter` hücrelerini çalıştır |
| `NameError: name 'kilavuz_vektorleri' is not defined` | Adım 3 çalışmadı | Adım 2'den itibaren sırayla çalıştır |
| `ValueError: Incompatible dimension for X and Y matrices: X.shape[1] == 3 while Y.shape[1] == ...` | `soru_vektoru` hâlâ ısınmadaki üç sayılık vektör | Adım 4'ün ilk hücresini (`soru_vektoru = vektor_al(soru)`) çalıştır |
| `KILAVUZLU: None` ve üstünde `İstek başarısız, durum kodu: ...` | Metin isteği olmadı; `modele_sor` çökmek yerine `None` verdi | Durum koduna bak (Konu 2, Adım 5), hücreyi yeniden çalıştır |
| Kılavuzu değiştirdim ama sonuçlar değişmedi | Adım 3 eski vektör dosyasını okudu | `ciktilar/kilavuz_vektorleri.json`'u sil, Adım 2'den yeniden çalıştır |
| `TypeError: can only concatenate str (not "numpy.float64") to str` | Bir puanı metne `+` ile eklemeye çalıştın | Önce metne çevir: `str(round(skor, 2))` |
| Adım 7'de `İstek başarısız, durum kodu: 400` | Görsel yönergesi boş ya da `None` (metin isteği olmamış) | Önceki hücreyi yeniden çalıştır, `gorsel_yonergesi`'ni yazdırıp bak |

---

## Kendini dene

1. Vektörleri neden bir dosyaya kaydettik? Hangi durumda o dosyayı silmen gerekir?
2. `kilavuzda_ara`'da `most_common(3)` yerine `most_common(1)` yazarsan renk sorusunun cevabında ne kaybolabilir?
3. Kılavuzda olmayan bir soruda `kilavuzda_ara` kaç paragraf verir? Bu yüzden talimattaki hangi cümle önemli?
4. Şu yönergede ne eksik? `yonerge = talimat + "\n\nBilgiler:\n" + "\nSoru: " + soru`
5. Afişte kılavuza uymayan bir şey gördün. Kuralın aramada mı, yönergede mi, çizimde mi kaybolduğunu nasıl anlarsın?

Cevaplar notun sonunda.

---

## Bu konuda öğrendiklerin

- Model senin belgeni bilmez; bilmediği yerde susmak yerine olası olanı yazar (uydurma)
- RAG'in üç adımı: parçala ve vektöre çevir → soruya en yakın parçaları bul → talimat + parçalar + soru ile sor
- Bir metin listesini tek istekte vektöre çevirmek ve sonucu ara çıktı olarak saklamak
- Bulma adımını kendi döngünle yazmak (Konu 4'teki `skorlar` ve `Counter`)
- Yönerge şablonu: talimat, bilgiler, soru; "bilmiyorum" kapısı
- RAG'in sınırı: gelmeyen parçayı model bilemez; gelen parçaya rağmen uydurabilir
- Kılavuzdan görsel kurallarını bulup bir görsel yönergesine dönüştürmek

## Bu konunun tek cümlesi

Model senin belgeni bilmez; RAG soruya en yakın parçaları bulup soruyla birlikte gönderir, böylece model cevabı belgeye
bakarak verir: ama yalnızca ona gönderilen parçalara bakabilir.

---

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **RAG** (*retrieval-augmented generation*) | "Bulup getirerek üretmek": modele soru sormadan önce belgeden ilgili parçaları bulup soruyla birlikte göndermek |
| **Bağlam** | Soruyla birlikte modele verilen arka plan bilgisi (Konu 2). RAG'de bağlam, belgeden bulunan parçalardır |
| **Parça** (*chunk*) | Belgenin bölündüğü, kendi başına okunabilen birim; bu konuda bir paragraf. Konu 5'teki parçayla (belirteç) karıştırma |
| **Bulma** (*retrieval*) | Sorunun vektörüne en yakın parçaları seçmek |
| **Uydurma** (halüsinasyon) | Modelin doğru olmayan bir bilgiyi akıcı ve kendinden emin biçimde yazması (Konu 5) |
| **Talimat** | Yönergenin modelin nasıl davranacağını söyleyen kısmı: "yalnızca bu bilgilere dayan; yoksa bilmiyorum de" |
| **Yönerge şablonu** | Sabit kısımları ve değişen yerleri olan yönerge kalıbı: talimat + bilgiler + soru |
| **Gömme vektörü** | Bir metnin anlamını temsil eden sayı listesi (Konu 4) |
| **Ara çıktı** | Bir adımın sonucu; sıradaki adıma gider, saklanırsa yeniden üretilmez (Konu 10) |
| **Marka kılavuzu** | Bir markanın renk, yazı, logo, ses tonu ve görsel kurallarını yazan belge |

---

## Ödev

Kendi markan ya da final projen için kısa bir kılavuz yazıp RAG'le soruyorsun. Ayrıntılar: `odevler/odev11.md`.

## Sonraki konu

**Konu 12 — Ajan.** Bugün kılavuza ne zaman bakılacağına sen karar verdin: her soruda önce `kilavuzda_ara`, sonra model.
Konu 12'de `kilavuzda_ara` bir **araç** olacak. Ajana "Sayfa Kahve için kılavuza uygun bir afiş yap" dediğinde önce kılavuza
bakmaya, sonra çizmeye model kendisi karar verecek.

---

## Kendini dene — cevaplar

1. Kılavuz değişmedikçe vektörleri de değişmez; her çalıştırmada yeniden istemek boşa istek demek (Konu 10: ara çıktıyı
   sakla). Kılavuzu değiştirdiğinde dosyayı silmen gerekir; yoksa arama eski kılavuzda yapılır ve yeni kural bulunmaz.
2. Renk bilgisi kılavuzda altı paragrafa dağılmış. Tek paragraf alınırsa yalnızca en yakını gider; yasak renkler ya da
   mevsim vurgusu gibi kurallar modele hiç ulaşmaz, cevap eksik kalır.
3. Yine üç paragraf verir: "en yakın" her zaman vardır, ilgili olmasa da. Bu yüzden "Bilgilerde cevap yoksa yalnızca
   'Bilmiyorum' yaz" cümlesi önemli: modele bir çıkış kapısı gösterir.
4. `bilgiler` eksik: model talimatı ve soruyu görür ama hiçbir bilgi görmez. Ya "Bilmiyorum" der ya da yine uydurur.
5. Ara çıktılara sırayla bak: kural `kurallar`'da yoksa aramada kayboldu; `kurallar`'da var ama `gorsel_yonergesi`'nde yoksa
   yönergede kayboldu (metin modeli koymadı); `gorsel_yonergesi`'nde de varsa çizimde kayboldu (görsel model uygulamadı).
