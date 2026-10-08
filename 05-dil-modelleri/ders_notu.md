# Konu 5 — Dil Modelleri Nasıl Çalışır?

Bu not konunun özetidir; derste çalıştırdığımız `ders.ipynb` defteriyle **aynı sırada**
ilerler: Isınma, sonra Adım 1–7 ve kısa bir Bonus. Derste kaçırdığın bir yer olursa
buradan oku, sonra defterde o adımın hücrelerini çalıştır. Nottaki kod blokları
defterdeki hücrelerin birebir aynısı; notu okurken defter yanında açık dursun.

**Konu 2'de:** uzaktaki bir modele soru sorduk, cevabını aldık. Model bir kutuydu: soru
girdi, metin çıktı.
**Konu 4'te:** modelin kelimeleri sayı listesine çevirdiğini gördük.
**Bu konuda:** modelin **nasıl yazdığına** bakıyoruz. Cevap şaşırtıcı derecede basit:

> Dil modeli bir sonraki parçayı tahmin eder; metin, bu tahminin tekrarıdır.
> Sıcaklık, en olasıyı mı seçeceğini yoksa zar mı atacağını ayarlar.

Bunu görmek için gerçek modelin içini açmıyoruz. Onun yerine Konu 1'deki 30 kafe
yorumundan, yalnızca **sayarak**, minicik bir "sonraki kelime" modeli kuruyoruz. Sonra
gerçek modele dönüp aynı fikri bir ayarla (sıcaklık) deniyoruz.

**Konunun sonunda elinde:** bir cümlenin belirteçlere bölünmüş hâli, "çok" kelimesinden
sonra ne geldiğini gösteren bir olasılık grafiği, 30 yorumdan cümle üreten iki küçük
fonksiyon ve üç sıcaklıkta üretilmiş sloganlardan oluşan bir pano (`pano.txt`).

**Kurulum (dersten önce):** `gita3111` klasöründe bir kez `uv sync` çalıştır. Bu konunun
yeni kütüphanesi `tiktoken` (metni parçalara ayıran araç) ve öteki kütüphaneler `gita3111`
klasöründeki `pyproject.toml` dosyasında yazılı; `uv sync` hepsini indirip `gita3111`
klasörünün içindeki `.venv` klasörüne kurar.

**Defteri açmak:** VS Code'da `05-dil-modelleri` klasöründeki `ders.ipynb`'yi aç.
Sağ üstten çekirdek (kernel) olarak **`.venv`**'i seç. Sonra hücreleri
yukarıdan aşağı, **Shift + Enter** ile sırayla çalıştır. Her hücre bir öncekinin
oluşturduğu değişkeni kullanır (`kodlayici`, `kelimeler`, `sayac`...); bir hücreyi atlarsan
sonraki hücre `NameError` verir. Takılırsan üstteki menüden "Restart" ile çekirdeği
yeniden başlat ve hücreleri yine en baştan çalıştır.

**Anahtar:** Isınma ve Adım 1–5 anahtarsız, internetsiz çalışır (tek istisna: `tiktoken`
ilk çalıştırmada bir kez sözlük dosyası indirir). Adım 6 ve 7 gerçek modele soru sorar;
`anahtar.txt` ister (Konu 2'deki dosyanın aynısı, `gita3111` klasöründe).

> **Bu nottaki çıktılar hakkında.** Adım 1–4'ün çıktıları her bilgisayarda aynıdır;
> burada gerçek çalıştırmadan alındı. Adım 5 zar atar: her çalıştırmada başka bir cümle
> çıkar, nottakiler yalnızca **örnek**. Adım 6–7'nin çıktıları gerçek modelden gelir ve
> her seferinde değişir; o yüzden notta model cevabı yok, **sorular** var. Kendi
> çıktına bak.

---

## Isınma: cümleyi tamamla

Sınıfa şunu sorduğumuzu düşün: *"Sessiz bir çalışma ..."* cümlesinin sonuna ne
getirirsin? Altı kişinin cevabı bir listede:

```python
from collections import Counter

cevaplar = ["kafesi", "kafesi", "yeri", "odası", "kafesi", "yeri"]
sayac = Counter(cevaplar)
print(sayac.most_common(2))
```

Çıktı:

```text
[('kafesi', 3), ('yeri', 2)]
```

`Counter` Konu 1'den tanıdık: listedeki her elemanın kaç kez geçtiğini sayar.
`most_common(2)` en sık iki elemanı, en çoktan aza, (eleman, adet) ikilileri olarak verir.

Hücre küçük ama konunun bütün fikri burada. Bir cümlenin devamını tahmin etmenin en basit
yolu: **daha önce en sık söyleneni seçmek.** Altı kişiden üçü "kafesi" demiş; birisi
"Sessiz bir çalışma" yazdığında sıradaki kelime için en iyi tahminin "kafesi".

Bir dil modeli de bunu yapar. Farkları:

- Altı cevaptan değil, **milyarlarca** metinden sayar.
- Yalnızca bir önceki kelimeye değil, **önceki bütün metne** bakar.
- Saymayı doğrudan yapmaz; sayımın sonucunu yüz milyonlarca sayının içinde (Konu 4'teki
  vektörler gibi) saklar.

Ama yaptığı işin özü aynı: "bundan sonra en olası ne gelir?"

---

## Adım 1 — Model metni nasıl görür: belirteçler

Sen bir cümleyi kelime kelime okursun. Model ise **parça parça** okur. Bu parçalara
**belirteç** (İngilizcesi *token*) denir. Bir belirteç bazen bir kelimedir, bazen bir
kelimenin bir parçası, bazen tek bir harf ya da noktalama işareti.

**Önce tarayıcıda.** `tiktokenizer.vercel.app` sitesini aç, kutuya bir cümle yaz. Her
parça ayrı bir renkle gösterilir. Kod yazmadan görmenin en hızlı yolu bu. Birkaç Türkçe
ve İngilizce cümle dene: hangisi daha çok renge bölünüyor?

**Sonra kodda.** Aynı işi `tiktoken` kütüphanesiyle yapıyoruz:

```python
import tiktoken

kodlayici = tiktoken.get_encoding("o200k_base")
belirtecler = kodlayici.encode("Sessiz bir çalışma kafesi")
print(len(belirtecler))
print(belirtecler)
```

Çıktı:

```text
6
[174397, 482, 3742, 162348, 61617, 14988]
```

- `tiktoken.get_encoding("o200k_base")`: bir **parça sözlüğü** yükler. `o200k_base` bu
  sözlüğün adı; yaklaşık 200 bin parçalık bir sözlük. `kodlayici` artık metni parçalara
  ayırmayı bilen bir araç.
- `kodlayici.encode(...)`: metni parçalara ayırır ve her parçanın **sözlükteki sıra
  numarasını** verir. Sonuç bir sayı listesi.
- İlk çalıştırmada `tiktoken` bu sözlüğü internetten indirir (birkaç saniye). Sonra
  bilgisayarında saklar, bir daha indirmez.

Model kelimeleri değil, **bu sayıları** görür. Konu 4'ü hatırla: model her sayıyı daha
sonra uzun bir sayı listesine (vektöre) çevirir ve onunla çalışır.

Sayılar bize bir şey söylemiyor; parçaları geri çevirelim:

```python
for belirtec in belirtecler:
    print(kodlayici.decode([belirtec]))
```

Çıktı (her satır bir parça; bazılarının başında boşluk var):

```text
Sess
iz
 bir
 çalışma
 kaf
esi
```

- `decode` `encode`'un tersi: sayıyı metne çevirir.
- `decode` bir **liste** ister. Tek bir parçayı çevirmek için onu köşeli parantez içine
  koyuyoruz: `[belirtec]`. Unutursan:

  ```text
  TypeError: 'int' object is not an instance of 'Sequence'
  ```

  Okuması: "tam sayı (int) bir dizi (liste) değil." Alıştırma defterinin ilk bozuk kodu bu.
- Parçanın başındaki boşluk da parçaya dahil: ` bir` ile `bir` sözlükte iki ayrı parça.

**Dört kelime, altı parça.** `bir` ve `çalışma` sözlükte tek parça olarak var; çok sık
geçtikleri için. `Sessiz` ve `kafesi` ise ikiye bölünmüş. Bölünme yerleri dilbilgisine
uymuyor (`kaf` + `esi`, `kafe` + `si` değil). Sözlük dilbilgisinden değil, metinlerde
**hangi harf dizilerinin sık geçtiğinden** kurulmuş.

### Aynı söz, kaç parça?

Aynı anlamda bir İngilizce cümle:

```python
ingilizce = kodlayici.encode("A quiet cafe for working")
print(len(ingilizce))
```

Çıktı: `5`. Beş kelime, beş parça: her kelime tek parça.

Uzun bir Türkçe kelime:

```python
uzun = kodlayici.encode("Kütüphanedekilerden misiniz?")
print(len(uzun))
for belirtec in uzun:
    print(kodlayici.decode([belirtec]))
```

Çıktı: `11`, sonra parçalar: `K`, `üt`, `ü`, `phan`, `ed`, `ek`, `iler`, `den`, ` mis`,
`iniz`, `?`.

| Cümle | Kelime | Parça |
|---|---|---|
| Sessiz bir çalışma kafesi | 4 | 6 |
| A quiet cafe for working | 5 | 5 |
| Kütüphanedekilerden misiniz? | 2 | 11 |

**Neden?** Parça sözlüğü çoğunlukla İngilizce metinlerden kurulmuş. İngilizcede sık
geçen kelimeler sözlüğe bütün olarak girmiş. Türkçe ise ekleri art arda dizen bir dil
(kütüphane-de-ki-ler-den): aynı kök onlarca farklı biçimde geçer, her biçim seyrek kalır,
sözlük de onları parçalara bölmek zorunda kalır.

### Bağlam penceresi: model neden "unutur"?

Bir model bir seferde **sınırlı sayıda parça** okuyabilir. Bu sınıra **bağlam penceresi**
denir. Sohbet uygulamalarında sorduğun soru, modelin önceki cevapları ve yapıştırdığın
metin hep bu pencereye girer. Pencere dolunca en eski kısım dışarıda kalır; model onu artık
görmez. Uzun bir sohbetin başında söylediğin bir şeyi modelin "unutması" bundandır: aslında
unutmuyor, **hiç görmüyor**.

Türkçe için bunun iki sonucu var:

- Aynı sözü söylemek için daha çok parça harcadığımız için pencere **daha çabuk dolar**.
- Ücretli modellerde fiyat parça başınadır; aynı iş Türkçe yapılınca **daha pahalıya** gelir.

Bir not: her modelin kendi parça sözlüğü var. `o200k_base` bir örnek (bazı OpenAI
modellerinin kullandığı sözlük). Adım 6'da kullandığımız Llama modelinin sözlüğü farklı;
aynı cümleyi biraz farklı bölüyor olabilir. Ama fikir aynı: model metni parçalara bölerek
okur ve Türkçe genelde daha çok parçaya bölünür.

---

## Adım 2 — Hangi kelimeden sonra ne geliyor?

Şimdi kendi küçük "dil modelimizi" kuruyoruz. Veri: Konu 1'deki 30 kafe yorumu. Dosyanın
aynısı bu konunun `veri` klasöründe (`veri/kafe-yorumlari.txt`). Önce okuyup Konu 1'deki
gibi temizliyoruz:

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

Çıktı: `298`. Konu 1'deki satırların aynısı: önce Türkçe **I** ve **İ** elle çevriliyor,
sonra küçük harfe geçiliyor, noktalama işaretleri boşluğa dönüyor, metin kelimelere
bölünüyor. Bu kez durak kelimeleri **atmıyoruz**: "bir", "çok", "ama" gibi kelimeler
cümlenin akışının parçası, sonraki kelimeyi tahmin ederken onlara ihtiyacımız var.

### "biraz" kelimesinden sonra

Yorumlarda "biraz"dan **hemen sonra** hangi kelimeler gelmiş?

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

Çıktı:

```text
['pahalı', 'karanlık', 'kısa', 'fazla']
```

Döngüyü satır satır okuyalım:

- `onceki = ""`: başlangıçta "önceki kelime" yok; boş bir metinle başlıyoruz.
- `for kelime in kelimeler:` kelimeleri sırayla dolaşır.
- `if onceki == hedef:` bir önceki kelime "biraz" mıydı? Öyleyse şu anki kelime,
  "biraz"dan hemen sonra gelen kelimedir; listeye ekle.
- `onceki = kelime`: turun son işi. Şu anki kelimeyi, bir sonraki tur için "önceki"
  olarak hatırla.

Son satırın **girintisi** önemli. `if`'in içine kayarsa yalnızca eşleşme olduğunda
çalışır; `onceki` hiç "biraz" olamaz ve liste boş kalır. Hata mesajı çıkmaz, sadece
`[]` görürsün. Alıştırma defterinin 2. bozuk kodu bu.

**Tasarım açısından okuması:** dört kelimenin dördü de şikâyet: biraz pahalı, biraz
karanlık, biraz kısa (çalışma saatleri), biraz fazla (kalabalık). Müşteriler kafeyi
överken "biraz" demiyor; eleştirirken **yumuşatıyor**. Yani "biraz" kelimesi bu yorumlarda
bir şikâyet işareti. Konu 1'de ışık sorununu, yorumları bağlamda okuyarak bulmuştuk; burada
da bir kelimenin **komşusu** bize nereye bakacağımızı söyledi. Bir marka için müşteri
yorumlarında "biraz", "keşke", "ama" gibi kelimelerin ardına bakmak, şikâyetleri hızla
bulmanın bir yolu.

### "çok" kelimesinden sonra

Aynı hücre, tek fark ilk satır:

```python
hedef = "çok"
sonra_gelenler = []
onceki = ""
for kelime in kelimeler:
    if onceki == hedef:
        sonra_gelenler.append(kelime)
    onceki = kelime

print(sonra_gelenler)
```

Çıktı:

```text
['güzel', 'kalabalık', 'keyifli', 'güzel', 'tatlı']
```

"güzel" iki kez geçiyor. Hangisinin en sık olduğunu ısınmadaki `Counter` söyler:

```python
sayac = Counter(sonra_gelenler)
print(sayac.most_common(5))
```

Çıktı:

```text
[('güzel', 2), ('kalabalık', 1), ('keyifli', 1), ('tatlı', 1)]
```

Beş istedik, dört geldi: listede yalnızca dört farklı kelime var. `most_common` olmayanı
uyduramaz.

İki hücre neredeyse aynı; yalnızca `hedef` değişti. Aynı satırları her kelime için
yeniden yazmak yerine Adım 4'te bunları bir fonksiyona koyacağız (Konu 2'deki
`modele_sor`'u hatırla).

---

## Adım 3 — Sayıdan olasılığa

"çok"tan sonra 5 kelime gelmiş, "güzel" bunların 2'si. O zaman "çok"tan sonra "güzel"
gelme **olasılığı** 2 / 5 = 0.4. Her kelime için aynı hesap:

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

Çıktı:

```text
güzel 0.4
kalabalık 0.2
keyifli 0.2
tatlı 0.2
```

- `toplam = len(sonra_gelenler)`: "çok"tan sonra gelen kelimelerin **toplam** sayısı (5).
  Dikkat: `len(sayac)` değil. `sayac`'ın uzunluğu **farklı** kelime sayısı (4); onunla
  bölersen olasılıkların toplamı 1'i geçer. Alıştırma defterinin 3. bozuk kodu bu.
- `for kelime, adet in sayac.most_common(5):` Konu 1'deki gibi her turda iki değişken gelir.
- `etiketler` ve `olasiliklar` grafiğin iki listesi: adlar ve boylar.

Olasılıkları topla: 0.4 + 0.2 + 0.2 + 0.2 = **1**. Her zaman 1 etmeli; çünkü "çok"tan sonra
**bir şey** mutlaka geliyor ve bunlar bütün seçenekler.

Konu 1 Adım 8'deki çubuk grafiğin aynısı:

```python
import matplotlib.pyplot as plt

plt.bar(etiketler, olasiliklar, color="#4a6fa5")
plt.title("'çok' kelimesinden sonra ne geliyor?")
plt.ylabel("Olasılık")
plt.show()
```

Bir çubuk (güzel) öbür üçünün iki katı. Bu grafiğe **olasılık dağılımı** denir:
olası her seçeneğe ne kadar şans verildiğini gösterir.

**Gerçek model ne yapıyor?** Tam olarak bunu, ama her adımda ve çok daha büyük ölçekte.
Bir cümlenin devamını yazarken model sözlüğündeki **her parça** için (yaklaşık 100–200 bin
parça) bir olasılık hesaplar. O grafikte 200 bin çubuk vardır; çoğu sıfıra çok yakındır,
birkaçı öne çıkar. Bizim grafiğimiz 30 yorumdan sayıldı; modelinki milyarlarca metinden
öğrenildi.

---

## Adım 4 — Metin üret: hep en olasıyı seç

Adım 2'nin satırlarını bir fonksiyona koyuyoruz. Fonksiyon bir kelime alır, ondan sonra
en sık gelen kelimeyi geri verir:

```python
def sonraki_kelime(hedef):
    sonra_gelenler = []
    onceki = ""
    for kelime in kelimeler:
        if onceki == hedef:
            sonra_gelenler.append(kelime)
        onceki = kelime
    sayac = Counter(sonra_gelenler)
    en_sik = sayac.most_common(1)
    secilen, adet = en_sik[0]
    return secilen
```

- İlk altı satır Adım 2'deki hücrenin aynısı; yalnızca `hedef` artık fonksiyona dışarıdan
  veriliyor.
- `sayac.most_common(1)` en sık **bir** kelimeyi verir, ama yine bir **liste** olarak:
  `[('güzel', 2)]`.
- `en_sik[0]` o listenin ilk (ve tek) elemanı: `('güzel', 2)` ikilisi.
- `secilen, adet = en_sik[0]` ikiliyi iki değişkene açar: `secilen` = `'güzel'`,
  `adet` = `2`. Konu 1'deki `for kelime, adet in ...` satırının aynı fikri.
- `return secilen` yalnızca kelimeyi geri verir. `return en_sik[0]` yazsaydık fonksiyon
  `('güzel', 2)` ikilisini verirdi; Adım 4'ün ikinci hücresinde bu ikiliyi bir metne
  eklemeye çalışınca hata çıkardı. Alıştırma defterinin 4. bozuk kodu bu.

Deneyelim:

```python
print(sonraki_kelime("çok"))
```

Çıktı: `güzel`.

### Tahmini tekrarla: metin

Metin üretmek, bu tahmini **tekrarlamak** demek. "kahve"den başlıyoruz; her turda son
kelimenin ardından en olası kelimeyi bulup cümleye ekliyoruz:

```python
kelime = "kahve"
cumle = kelime
for tur in range(8):
    kelime = sonraki_kelime(kelime)
    cumle = cumle + " " + kelime

print(cumle)
```

Çıktı:

```text
kahve ortalama tatlılar güzel yazın bahçede oturmak için en
```

- `range(8)`: "8 kez tekrarla". `tur` değişkenini kullanmıyoruz; yalnızca kaç kez
  döneceğini söylüyor.
- `kelime = sonraki_kelime(kelime)`: döngünün kalbi. Bulunan kelime, bir sonraki turda
  **yeni hedef** oluyor. Bu satırı `yeni = sonraki_kelime(kelime)` diye yazıp `kelime`'yi
  güncellemeyi unutursan model hep aynı kelimeye bakar ve aynı kelimeyi tekrarlar
  ("kahve ortalama ortalama ortalama..."). Alıştırma defterinin 5. bozuk kodu bu.
- `cumle = cumle + " " + kelime`: cümlenin sonuna bir boşluk ve yeni kelimeyi ekler.

**Okuması:** cümle bir yerden sonra bir şey anlatıyor gibi: "tatlılar güzel, yazın bahçede
oturmak için..." Ama bütün olarak anlamsız. Her kelime yalnızca **bir önceki** kelimeye
bakılarak seçildi; modelin cümlenin başından, konudan, anlamdan haberi yok. Yine de
kelimeler birbirine "uyuyor", çünkü her ikili gerçekten bir yorumda yan yana geçmiş.

Hücreyi bir kez daha çalıştır: **aynı cümle** çıkar. Hep en olasıyı seçen bir model her
seferinde aynı şeyi yazar. Bu kurala "açgözlü seçim" denir.

**Gerçek model bundan ne kadar farklı?** Gerçek model bir önceki kelimeye değil, **önceki
bütün metne** (bağlam penceresinin izin verdiği kadarına) bakar ve olasılıkları 30 yorumdan
değil milyarlarca metinden öğrenmiştir. Bu yüzden tutarlı, anlamlı paragraflar yazabilir.
Ama yaptığı iş temelde aynıdır: **sıradaki parçayı seç, ekle, tekrarla.**

**Ardından hiçbir şey gelmeyen kelime.** Başlangıç kelimesini değiştirirsen bir hata
görebilirsin. Dosyanın son kelimesi "kahveli" ("Kütüphane gibi ama kahveli."); ondan sonra
hiçbir kelime yok. `sonraki_kelime("kahveli")` boş bir listeyle `Counter` kurar,
`most_common(1)` boş liste verir ve `en_sik[0]` şu hatayı verir:

```text
IndexError: list index out of range
```

Okuması: "listenin bu sırasında eleman yok." "kahve" ile başladığımızda bu olmuyor; açgözlü
seçim "kahveli"ye hiç varmıyor.

### Model neden uydurur?

Bu küçük model yorumlarda geçen her şeyi "biliyor" gibi görünüyor; ama aslında yalnızca
hangi kelimenin hangisinden sonra geldiğini biliyor. "kahve ortalama tatlılar güzel" bir
bilgi değil, sık görülen kelime ikililerinin art arda dizilmesi.

Büyük dil modelleri de aynı yoldan yanılır. Model bir sorunun **doğru** cevabını aramaz;
o sorudan sonra **en olası** görünen metni üretir. Çoğu zaman en olası metin doğru
metindir, çünkü eğitim verisinde doğrular daha sık geçer. Ama verinin az olduğu yerde
(seyrek bir konu, yerel bir bilgi, bir kişinin özgeçmişi) model yine akıcı, kendinden emin,
ama **uydurma** bir metin yazar. Buna uydurma (İngilizcesi *hallucination*) denir.
"Model gerçeği biliyor" sanmak bu konunun en önemli tuzağı.

---

## Adım 5 — Zar at

Şimdi en sıkını seçmek yerine **zar atalım**. `random.choice` bir listeden rastgele bir
eleman seçer:

```python
import random

print(sonra_gelenler)
print(random.choice(sonra_gelenler))
```

`sonra_gelenler` hâlâ Adım 2'deki "çok" listesi: `['güzel', 'kalabalık', 'keyifli', 'güzel', 'tatlı']`.
İkinci satır her çalıştırmada bu beşinden birini yazar; örneğin bir çalıştırmada `tatlı`.

Hücreyi birkaç kez çalıştır. "güzel" en sık çıkar ama hep değil. Neden? Listede "güzel"
**iki kez** var; beş elemandan ikisi "güzel" olduğu için seçilme şansı 2 / 5 = 0.4.
Adım 3'teki olasılığın aynısı. Biz ayrıca bir olasılık vermedik: listede sık geçen kelime,
listede çok yer kapladığı için zarda da sık çıkıyor. (Bilgisayarda bu hücreyi 10 000 kez
çalıştırdık: "güzel" yaklaşık 4 000 kez, öbür üçü yaklaşık 2 000'er kez çıktı.)

Adım 4'teki fonksiyonun aynısı, yalnızca sondaki satırlar farklı:

```python
def sonraki_kelime_zarla(hedef):
    sonra_gelenler = []
    onceki = ""
    for kelime in kelimeler:
        if onceki == hedef:
            sonra_gelenler.append(kelime)
        onceki = kelime
    if len(sonra_gelenler) == 0:
        return kelimeler[0]
    secilen = random.choice(sonra_gelenler)
    return secilen
```

- `Counter` ve `most_common` yerine `random.choice`: en sık kelimeyi değil, olasılığına göre
  zarla bir kelime seçiyor.
- `if len(sonra_gelenler) == 0:` **metin bittiyse baştan başla.** Dosyanın son kelimesi
  "kahveli" ("Kütüphane gibi ama kahveli."); ondan sonra hiçbir kelime gelmiyor. Zar oraya
  gelirse `sonra_gelenler` boş kalır ve `random.choice` boş listeden seçemez
  (`IndexError: Cannot choose from an empty sequence`). Bu satır o durumda metnin ilk
  kelimesini (`kelimeler[0]`, yani "ders") verir; üretim dosyanın başından devam eder.

Aynı üretim hücresi, zarla:

```python
kelime = "kahve"
cumle = kelime
for tur in range(8):
    kelime = sonraki_kelime_zarla(kelime)
    cumle = cumle + " " + kelime

print(cumle)
```

Her çalıştırmada başka bir cümle çıkar. Bizim denememizde birkaç örnek (seninkiler farklı
olacak):

```text
kahve biraz karanlık kitap okumak için geniş ışık yeterli
kahve ortalama tatlılar güzel ama buraya ders çalışmak için
kahve biraz fazla sessiz ve sakin saatlerce oturmana kimse
```

Hücreyi üç kez çalıştır, cümleleri karşılaştır. Adım 4'teki cümleyle ortak bir başlangıç
görebilirsin ("kahve ortalama tatlılar güzel"): "ortalama"dan sonra yorumlarda yalnızca
"tatlılar" geçiyor, zar ne atarsa atsın seçenek tek. Seçeneğin çok olduğu yerde ise
cümleler ayrılıyor.

**"kahveli ders".** Ara sıra cümlenin ortasında "kahveli ders" görürsün (örneğin "kahve
biraz pahalı ama kahveli ders çalışmak için en"). Zar metnin sonuna geldi, üretim baştan
devam etti. Bilgisayarda 20 000 kez denedik: yaklaşık 17 çalıştırmada bir oluyor.

Gerçek modellerde bu durum için özel bir parça vardır: **"metin bitti"**. Model sözlüğündeki
öbür parçalar gibi onun için de bir olasılık hesaplar; o parçayı seçince yazmayı bırakır.
Bir modelin cevabının nerede biteceğini de böylece kendisi "tahmin eder".

---

## Sıcaklık: en olası mı, zar mı?

Adım 4 ve 5, gerçek modellerdeki **sıcaklık** (İngilizcesi *temperature*) ayarının iki ucu:

| Sıcaklık | Ne yapar | Defterdeki karşılığı |
|---|---|---|
| Çok düşük (0'a yakın) | Hep en olası parçayı seçer | Adım 4: hep aynı cümle |
| 1 civarı | Olasılıklara göre zar atar | Adım 5: "güzel" 0.4, öbürleri 0.2 |
| Yüksek (1'in üstü) | Zarı **hileli** hâle getirir: olasılığı düşük parçalara daha çok şans verir | — |

Sıcaklığı Adım 3'teki grafikle düşün:

- **Sıcaklık düşerken** uzun çubuk uzar, kısalar kısalır. 0'a yaklaşınca yalnızca "güzel"
  kalır: bu, Adım 4'ün açgözlü seçimi.
- **Sıcaklık yükselirken** çubuklar birbirine yaklaşır. "güzel" ile "tatlı" arasındaki fark
  küçülür. Çok yüksek sıcaklıkta bütün çubuklar eşitlenir: model sözlüğündeki herhangi bir
  parçayı neredeyse aynı şansla seçer ve metin anlamsızlaşır.

Bizim küçük modelimizde sıcaklık ayarı yok (yalnızca iki ucu var); bu ayar gerçek modelin
olasılıklarını hesaplarken kullanılır. Adım 6'da gerçek modelde deneyeceğiz.

**Tuzak:** yüksek sıcaklık "daha yaratıcı" değil, **daha dağınık** demek. Bazen beklenmedik
güzel bir fikir çıkar; çoğu zaman tuhaf, yarım ya da anlamsız bir metin. Sıcaklık bir
yaratıcılık düğmesi değil, bir **seçim kuralı** ayarı.

---

## Adım 6 — Gerçek model ve sıcaklık

Bu adımdan sonrası gerçek modele soru soruyor; `anahtar.txt` ister. Konu 2'deki Adım 1
hücresinin aynısı:

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

Adres ve başlık Konu 2'deki gibi:

```python
import requests

MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
basliklar = {"Authorization": f"Bearer {anahtar}"}
```

`modele_sor` fonksiyonu da Konu 2'deki; tek fark, ikinci bir bilgi alması:

```python
def modele_sor(soru, sicaklik):
    govde = {"prompt": soru, "temperature": sicaklik}
    cevap = requests.post(adres, headers=basliklar, json=govde)
    yanit = cevap.json()
    sonuc = yanit["result"]
    return sonuc["response"]
```

- `def modele_sor(soru, sicaklik):` fonksiyon artık iki şey alıyor: soru ve sıcaklık.
- `"temperature": sicaklik`: gövdeye yeni bir alan. Sunucu İngilizce ad bekliyor:
  `"temperature"`. `"sicaklik"` yazarsan sunucu bu alanı tanımaz.
- Bu model 0 ile 5 arasında bir sıcaklık kabul ediyor; hiç yazmazsan 0.6 kullanıyor.
  (Konu 2'de sıcaklık vermediğimiz için cevaplar 0.6 ile üretiliyordu.)
- Geri kalan dört satır Konu 2'nin aynısı.

Aynı soruyu üç sıcaklıkta soruyoruz. Tek bir slogan istiyoruz ki cevapları yan yana
karşılaştırmak kolay olsun:

```python
soru = "Sessiz bir çalışma kafesi için tek bir kısa slogan yaz. Yalnızca sloganı yaz."

for sicaklik in [0.1, 0.7, 1.5]:
    metin = modele_sor(soru, sicaklik)
    print(sicaklik, metin)
```

Her satırda önce sıcaklık, sonra slogan yazar. **Çalıştırmadan önce tahmin et:** hangisi
en "garip" slogan olacak? Hangisi en "sıradan"?

Bu adımın çıktılarını notta vermiyoruz: model her seferinde başka bir cümle kurar. Kendi
çıktına bak ve şu soruları sor:

- 0.1'deki slogan "bir kafe sloganı denince akla ilk gelen" türden mi?
- 1.5'teki slogan dilbilgisi olarak düzgün mü? Türkçe mi kaldı?
- Hangisini bir tabelaya yazardın?

Şimdi aynı sıcaklıkta iki kez soralım. Önce düşük:

```python
ilk = modele_sor(soru, 0.1)
ikinci = modele_sor(soru, 0.1)
print(ilk)
print(ikinci)
```

Sonra yüksek:

```python
ilk = modele_sor(soru, 1.5)
ikinci = modele_sor(soru, 1.5)
print(ilk)
print(ikinci)
```

Beklenen: 0.1'de iki cevap **aynı ya da neredeyse aynı**; 1.5'te iki cevap **belirgin
farklı**. Düşük sıcaklık Adım 4'e (hep en olası, hep aynı), yüksek sıcaklık Adım 5'e (zar)
benziyor. Senin çıktında da böyle mi? 0.1'de bile iki cevap farklı çıkabilir: sıcaklık
tam 0 değil ve sunucu tarafında küçük rastlantılar olabiliyor. Fark ne kadar büyük?

---

## Adım 7 — Slogan panosu

Bir tasarımcı tek bir fikre değil, bir **panoya** bakarak karar verir. Bu kez modelden tek
seferde **üç** slogan istiyoruz ve her sıcaklığın sloganlarını başlığıyla tek bir dosyaya
yazıyoruz:

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

- `pano_sorusu`: Adım 6'daki sorunun üç sloganlık hâli. Üç sloganı ayrı satırlara
  yazmasını da soruda istiyoruz; model çoğu zaman uyar, ama biçimi garanti değil.
- `open("pano.txt", "w", ...)`: Konu 2'deki `cevaplar.txt` gibi. `"w"` "yazmak için aç"
  demek; dosya varsa **baştan** yazılır.
- Döngü her sıcaklık için bir kez döner: modele sorar, önce başlığı, sonra cevabı yazar.
- `str(sicaklik)`: sayıyı (0.1) metne (`"0.1"`) çevirir. Metinle sayı `+` ile
  birleştirilemez; `"Sıcaklık " + 0.1` yazarsan
  `TypeError: can only concatenate str (not "float") to str` alırsın.
- `dosya.write("\n")`: bölümler arasına boş bir satır.
- 3 sıcaklık = 3 istek.

Dosyanın biçimi şöyle olur (sloganların yerine senin modelinin yazdıkları gelir):

```text
Sıcaklık 0.1
<slogan>
<slogan>
<slogan>

Sıcaklık 0.7
<slogan>
...
```

Klasörde `pano.txt`'yi aç, üç bölümü yan yana oku ve tasarımcı gözüyle değerlendir:

- **Kurumsal bir tabela, menü başlığı, yönlendirme metni** için hangi sıcaklık? Burada
  tutarlılık ve tekrarlanabilirlik önemli: yarın aynı soruyu sorduğunda aynı tonda bir
  cevap almak istersin.
- **Fikir fırtınası, ilk eskiz, isim avı** için hangisi? Burada çeşitlilik önemli:
  birbirine benzeyen üç fikir, tek fikirden farksız.
- 1.5'teki sloganlardan **kullanılabilecek** olan var mı? Kaç tanesi? Kullanılamayanların
  sorunu ne: anlamsız mı, dilbilgisi bozuk mu, konudan mı kopmuş?
- Hangi sıcaklığın üç sloganı birbirinden daha farklı? Hangisininki aynı kalıbın tekrarı gibi?

Sıcaklık, işin türüne göre seçilen bir **araç ayarı**; "en iyi sıcaklık" diye bir şey yok.
Konu 2'de "soruyu yazmak bir tasarım kararı" demiştik; sıcaklığı seçmek de öyle.

---

## Bonus

**1. Kendi adın kaç parça?**

```python
belirtecler = kodlayici.encode("Ahmet Emre Aladağ")
print(len(belirtecler))
for belirtec in belirtecler:
    print(kodlayici.decode([belirtec]))
```

Çıktı: `7`, sonra `Ah`, `met`, ` Em`, `re`, ` Al`, `ada`, `ğ`. Üç kelime, yedi parça; `ğ`
kendi başına bir parça. Tırnak içine kendi adını ve soyadını yaz, yeniden çalıştır.
Yanındakinin adı kaç parça? Türkçe harfler (ç, ğ, ı, ö, ş, ü) içeren adlar daha mı çok
bölünüyor?

**2. Başka bir kelimeden başla.** Adım 4'teki üretim hücresinde `"kahve"` yerine `"sessiz"`
ya da `"priz"` yaz, yeniden çalıştır. Örneğin "sessiz" ile açgözlü seçim şunu verir:
`sessiz ve sakin saatlerce oturabiliyorsunuz sınav haftası her masada`. Dikkat: dosyanın son
kelimesi olan "kahveli" ile başlarsan `IndexError` alırsın; ondan sonra hiç kelime yok.

---

## Neden olasılıkları gerçek modelden almadık?

Bazı modeller bir cevabın yanında her parçanın olasılığını da gönderebiliyor (bu bilgiye
*logprobs* deniyor). Bu konuda bunu kullanmadık; olasılıkları kendi küçük modelimizden,
sayarak çıkardık. İki sebebi var:

- Derste kullandığımız Llama modeli bu bilgiyi göndermiyor. Gönderen modellerde ise yanıt
  çok katmanlı (listenin içinde sözlük, onun içinde liste...) ve okumak için bu derste
  kullanmadığımız yapılar gerekiyor.
- Sayarak kurduğumuz model **içini görebildiğimiz** bir model. "güzel"in olasılığının neden
  0.4 olduğunu biliyoruz: beş kelimeden ikisi. Gerçek modelin verdiği bir 0.4'ün nereden
  geldiğini göremezdik.

Fikir aynı: gerçek model de her adımda Adım 3'teki gibi bir dağılım hesaplar ve sıcaklık
bu dağılımdan nasıl seçileceğini belirler.

**Yapılandırılmış çıktı nerede?** Modelden serbest metin yerine belirli alanları olan bir
cevap istemek (örneğin her slogan için `slogan`, `ton`, `hedef kitle` alanları) bu konunun
ilk planında vardı. Konu 12'ye (araç kullanımı) taşındı: orada modelin cevabını doğrudan
bir programın kullanacağı veri olarak işleyeceğiz ve bu fikir oraya daha iyi oturuyor.

---

## Defterin bölümleri

| Adım | Ne yaptık | Elimizde ne oluştu |
|---|---|---|
| Isınma | Cümle tamamlama cevaplarını saydık | en sık cevap: "kafesi" |
| 1 | Metni belirteçlere ayırdık; Türkçe ile İngilizceyi kıyasladık | `kodlayici`, `belirtecler` |
| 2 | Bir kelimeden sonra gelenleri topladık, saydık | `kelimeler`, `sonra_gelenler`, `sayac` |
| 3 | Sayıları olasılığa çevirip çizdik | `etiketler`, `olasiliklar`, grafik |
| 4 | Hep en olasıyı seçerek metin ürettik | `sonraki_kelime()` |
| 5 | Zarla seçerek metin ürettik | `sonraki_kelime_zarla()` |
| 6 | Gerçek modeli üç sıcaklıkta denedik | `modele_sor(soru, sicaklik)` |
| 7 | Slogan panosu | `pano.txt` |
| Bonus | Kendi adını belirteçlere ayırdık; başka kelimeden başladık | — |

Hepsi tek defterde: `ders.ipynb`. Hücreleri her zaman yukarıdan aşağı çalıştır; defteri
yeni açtıysan (ya da çekirdeği yeniden başlattıysan) en baştan başla. Adım 6'ya doğrudan
atlamak istersen bile Adım 6'nın ilk hücresinden başlaman yeter; Adım 6–7 öncekilerin
değişkenlerini kullanmıyor.

Derste kendi başına çalışacağın defter: `alistirma.ipynb`. Önce aynı klasörde yeni bir
adla kopyala, kopyada çalış; böylece `git pull` çakışmaz. Anahtar istemez; dosya da okumaz:
ilk hücresi on kelimelik küçük bir metin kurar. İki bölümü var:

- **Bozuk kodlar:** beş kısa hücre. Biri hata mesajı veriyor, öbürleri sessizce yanlış
  sonuç yazıyor; üstlerinde ne yazmaları gerektiği yazıyor.
- **Kendi başına:** `BOSLUK` yazan yerleri doldurduğun sorular. Doldurmadığın boşluk
  `NameError: name 'BOSLUK' is not defined` verir; o yüzden soruları sırayla çöz. Her
  sorunun üstünde doğru çıktı yazılı.

---

## Sık karşılaşılan hatalar ve mesajlarını okumak

Python bir hata verdiğinde en alttaki satır en önemlisidir: önce hatanın **türü**
(`IndexError`, `TypeError`), iki noktadan sonra da **açıklaması** gelir.

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `ModuleNotFoundError: No module named 'tiktoken'` | Defter `.venv` dışındaki bir çekirdekle çalışıyor ya da `uv sync` yapılmadı | Sağ üstten çekirdek olarak `.venv`'i seç; `gita3111` klasöründe `uv sync` |
| Adım 1 ilk çalıştırmada uzun bekliyor ya da bağlantı hatası veriyor | `tiktoken` sözlük dosyasını internetten indiriyor | İnternete bağlan, hücreyi yeniden çalıştır; bir kez indikten sonra internet gerekmez |
| `TypeError: 'int' object is not an instance of 'Sequence'` | `decode`'a tek sayı verildi | `kodlayici.decode([belirtec])`: köşeli parantez |
| `NameError: name 'kelimeler' is not defined` | Bir hücreyi atladın ya da defteri yeni açtın | Hücreleri baştan, sırayla çalıştır |
| `FileNotFoundError: ... 'veri/kafe-yorumlari.txt'` | Defterin kopyası konu klasörünün dışında | Kopya `05-dil-modelleri` klasöründe durmalı |
| `sonra_gelenler` boş: `[]` | `onceki = kelime` satırı `if`'in içine kaymış ya da hedef kelime yazım hatalı (`"Biraz"`) | Satırı `for`'un hizasına al; hedefi küçük harfle yaz |
| Olasılıkların toplamı 1'i geçiyor | `len(sayac)` ile bölündü (farklı kelime sayısı) | `toplam = len(sonra_gelenler)` |
| `TypeError: can only concatenate str (not "tuple") to str` | Fonksiyon `('güzel', 2)` ikilisini döndürüyor | `secilen, adet = en_sik[0]`, `return secilen` |
| `IndexError: list index out of range` | `sonraki_kelime` ardından hiç kelime gelmeyen bir kelimeyle çağrıldı ("kahveli" ya da metinde olmayan bir kelime) | Başka bir başlangıç kelimesi seç |
| `IndexError: Cannot choose from an empty sequence` | `sonraki_kelime_zarla` içindeki `if len(sonra_gelenler) == 0:` satırları yazılmamış; zar "kahveli"ye geldi | İki satırı ekle (Adım 5) |
| Üretilen cümle aynı kelimeyi tekrarlıyor | Döngüde `kelime` güncellenmiyor | `kelime = sonraki_kelime(kelime)` |
| `FileNotFoundError: ... '../anahtar.txt'` | Anahtar dosyası yok ya da yanlış yerde | Dosya `gita3111` klasöründe durmalı (Konu 2) |
| `TypeError: 'NoneType' object is not subscriptable` | İstek başarısız oldu (yanlış anahtar, kota) | Konu 2 Adım 5: önce durum koduna bak |
| `TypeError: can only concatenate str (not "float") to str` | Adım 7'de sıcaklık metne çevrilmeden eklendi | `str(sicaklik)` |

---

## Kendini dene

Cevaplar notun en sonunda. Önce kendin düşün.

1. "Sessiz bir çalışma kafesi" 6 parça, "A quiet cafe for working" 5 parça. Aynı uzunlukta
   bir Türkçe ve bir İngilizce metin, aynı bağlam penceresine sığar mı?
2. Adım 3'te `toplam = len(sonra_gelenler)` yerine `toplam = len(sayac)` yazsaydık
   "güzel"in olasılığı kaç çıkardı? Neden yanlış?
3. Adım 2'de hedefi `"Biraz"` (büyük harfle) yazarsan ne olur? Hata mesajı alır mısın?
4. Adım 4'teki üretim hücresini on kez çalıştırırsan kaç farklı cümle görürsün? Adım 5'te?
5. "biraz"dan sonra gelen dört kelimenin olasılığı kaç? Adım 4'ün kuralıyla "biraz"dan sonra
   hangi kelime seçilir? (İpucu: dördü de eşit.)
6. Arkadaşın "sıcaklığı 2'ye çıkardım, çok daha yaratıcı sloganlar geldi" diyor. Ona ne
   sorarsın?
7. Bir ajans müşteriye her ay aynı biçimde bir bülten metni hazırlatacak. Sıcaklığı yüksek
   mi, düşük mü seçersin? Neden?
8. Bir modele bir kişinin özgeçmişini sordun, akıcı ve ayrıntılı bir cevap geldi. Bu cevaba
   neden hemen güvenmemelisin? Bu konunun hangi adımı bunu açıklıyor?

---

## Bu konuda öğrendiklerin

- **Belirteç.** Model metni kelime kelime değil, parça parça okur ve her parçayı bir sayı
  olarak görür. Türkçe ekler yüzünden daha çok parçaya bölünür: bağlam penceresi daha çabuk
  dolar, ücretli modellerde daha pahalıdır.
- **Sonraki parçanın tahmini.** Bir kelimeden sonra hangi kelimelerin geldiğini sayarak
  küçük bir dil modeli kurduk. "biraz"dan sonra hep şikâyet geliyordu; "çok"tan sonra en sık
  "güzel".
- **Olasılık dağılımı.** Adet / toplam. Bütün seçeneklerin olasılığı toplamı 1. Gerçek model
  her adımda sözlüğündeki her parça için böyle bir dağılım hesaplar.
- **Metin = tahminin tekrarı.** Seçilen kelime bir sonraki turun hedefi olur. Anlam yok,
  yalnızca sayma var; büyük modellerde de temel iş bu. Uydurma buradan çıkar.
- **Sıcaklık.** Düşük: hep en olası, hep aynı (açgözlü). Yüksek: zar, her seferinde farklı.
  Yüksek sıcaklık "yaratıcı" değil, "dağınık".
- **Sıcaklık bir tasarım kararı.** Tutarlılık gereken iş için düşük, çeşitlilik gereken iş
  için yüksek.

## Bu konunun tek cümlesi

> Dil modeli bir sonraki parçayı tahmin eder; metin, bu tahminin tekrarıdır. Sıcaklık, en
> olasıyı mı seçeceğini yoksa zar mı atacağını ayarlar.

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **Dil modeli** | Bir metnin devamında hangi parçanın geleceğini tahmin eden model |
| **Belirteç (token)** | Modelin okuduğu en küçük metin parçası: bir kelime, bir kelime parçası ya da bir işaret |
| **Parça sözlüğü** | Bir modelin tanıdığı bütün belirteçlerin listesi; her belirtecin bir sıra numarası var. Bizimki `o200k_base` |
| **`encode` / `decode`** | Metni parça numaralarına çevirmek / numaraları metne geri çevirmek |
| **Bağlam penceresi** | Modelin bir seferde okuyabildiği en fazla parça sayısı; dışında kalanı görmez |
| **Olasılık** | Bir seçeneğin seçilme şansı; 0 ile 1 arası. Burada adet / toplam |
| **Olasılık dağılımı** | Bütün seçeneklerin olasılıkları birlikte; toplamları 1 |
| **Açgözlü seçim** | Her adımda en olası parçayı seçmek; her seferinde aynı metin |
| **Örnekleme (zar)** | Parçayı olasılığına göre rastgele seçmek; her seferinde başka metin |
| **Sıcaklık (temperature)** | Seçimin ne kadar "zar" olacağını ayarlayan sayı; düşükse en olasıya, yüksekse rastlantıya yakın |
| **Uydurma (hallucination)** | Modelin doğru olmayan bir bilgiyi akıcı ve kendinden emin biçimde yazması; model doğruyu değil olası metni üretir |
| **`random.choice`** | Bir listeden rastgele bir eleman seçen komut |
| **`range(n)`** | "n kez tekrarla"; `for tur in range(8):` döngüyü 8 kez döndürür |

## Ödev

`odevler/odev5.md` (puansız), iki parça:

1. Kendi seçtiğin bir yaratıcı iş için soruyu yaz (Adım 6'daki `soru` ve Adım 7'deki
   `pano_sorusu`), Adım 7'yi kendi sorunla çalıştır,
   `pano.txt`'yi getir. Tek soru: hangi sıcaklık işe yaradı, neden?
2. Bir Türkçe cümle ve aynı anlamda bir İngilizce cümle seç; ikisini de belirteçlere ayır,
   parça sayılarını karşılaştır.

## Sonraki konu

**Konu 6 — Kaput açma: üretmek ne demek.** Bu konuda üretmenin "olasılık dağılımından seçim"
olduğunu gördük. Konu 4'te kelimelerin bir haritada nokta olduğunu görmüştük. Konu 6 bu iki
fikri birleştiriyor: üretmek, öğrenilmiş bir haritada nokta seçmek. Görsel üreten modellere
geçmeden önceki son kavramsal adım.

---

## Kendini dene — cevaplar

1. Aynı **parça** sayısına kadar sığar; ama aynı uzunlukta (aynı sözü söyleyen) Türkçe metin
   daha çok parça tuttuğu için pencereye daha az Türkçe **söz** sığar. Pencere kelimeyle
   değil, parçayla ölçülür.
2. `len(sayac)` farklı kelime sayısı, yani 4. "güzel" 2 / 4 = 0.5 çıkardı; öbürleri 0.25.
   Toplam 0.5 + 0.25 + 0.25 + 0.25 = 1.25: 1'i geçiyor. Olasılık "kaç kez geçti / toplam kaç
   kelime geldi" olmalı; toplam 5.
3. Hata mesajı almazsın; liste boş çıkar (`[]`). Temizlik satırları bütün metni küçük harfe
   çevirdi; `kelimeler` listesinde "Biraz" diye bir kelime yok. Python itiraz etmez, sonucu
   kontrol etmek senin işin.
4. Adım 4'te hep **bir** cümle: hep en olası seçildiği için. Adım 5'te büyük ihtimalle her
   seferinde farklı (bazen aynı cümle denk gelebilir; arada "kahveli ders" ile baştan başlar).
5. Dördü de 1 / 4 = 0.25. Eşitlikte `most_common` listede **ilk görüleni** öne koyar; Adım 4'ün
   kuralıyla "pahalı" seçilir. Yani açgözlü seçimde eşitlik bile her seferinde aynı sonucu verir.
6. "Kaç tanesini gerçekten kullanabilirsin?" Yüksek sıcaklık çeşitliliği artırır ama
   olasılığı düşük, çoğu zaman anlamsız parçaları da seçtirir. Birkaç ilginç slogan çıkmış
   olabilir; ama yanlarında kaç tane bozuk slogan var? Karşılaştırmak için aynı soruyu 0.7'de
   de sormalı.
7. Düşük. Her ay aynı ton ve biçim isteniyor; tutarlılık, şaşırtıcılıktan önemli. Düşük
   sıcaklıkta aynı soru benzer cevaplar verir.
8. Model doğru cevabı değil, sorudan sonra **en olası** görünen metni üretir. Bir kişinin
   özgeçmişi eğitim verisinde az geçer ya da hiç geçmez; model yine akıcı bir metin yazar,
   ama boşlukları olası görünen ayrıntılarla doldurur (uydurma). Adım 4: küçük modelimiz de
   "kahve ortalama tatlılar güzel..." diye akıcı ama bilgi taşımayan bir cümle kurdu.
