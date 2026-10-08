# Konu 3 — Makine Öğrenmesi Nedir? (matematiksiz)

Bu not konunun özetidir; derste çalıştırdığımız `ders.ipynb` defteriyle **aynı sırada**
ilerler: Isınma, sonra Adım 1–8 ve kısa bir Bonus. Derste kaçırdığın bir yer olursa
buradan oku, sonra defterde o adımın hücrelerini çalıştır. Nottaki kod blokları
defterdeki hücrelerin birebir aynısı; notu okurken defter yanında açık dursun.

**Konu 2'de:** hazır bir modele soru sorduk; model kutunun içindeydi.
**Bu konuda:** kutuyu açıyoruz ve kendi modelimizi eğitiyoruz. Veri: sınıfın Konu 2
ödevinde etiketlediği 20 renk.

**Neden renk?** Konu 1'de müşterilerin kafeyi "sessiz bir çalışma yeri" olarak
anlattığını bulduk. O kafenin paleti **sakin** hissettirmeli. Peki bir rengin sakin mi
enerjik mi olduğunu bir program söyleyebilir mi? Bu konuda bunu, sınıfın kendi
etiketlerinden öğrenen bir modelle deniyoruz. Sonunda iki şey öğrenmiş olacaksın:
modelin nasıl çalıştığı ve modelin yanılgılarının **sınıfın renk algısı hakkında**
ne söylediği.

**Konunun sonunda elinde:** sınıfın verisiyle eğitilmiş bir model, modelin yanıldığı
renklerin listesi, bir öğrenme eğrisi grafiği ve kafe paleti için modelden alınmış bir
"ikinci görüş".

**Kurulum (dersten önce):** `gita3111` klasöründe bir kez `uv sync` çalıştır; indirme
birkaç dakika sürebilir. Bu konunun kütüphaneleri ve defteri çalıştıran parça `gita3111`
klasöründeki `pyproject.toml` dosyasında yazılı; `uv sync` onları indirip `gita3111`
klasörünün içinde bir `.venv` klasörü kurar. Dikkat: paketin adı `scikit-learn`, ama kodda
`sklearn` diye çağrılır (`from sklearn... import ...`). Adlar farklı; ikisi aynı kütüphane.

**Defteri açmak:** VS Code'da `03-makine-ogrenmesi` klasöründeki `ders.ipynb`'yi aç.
Sağ üstten çekirdek (kernel) olarak **`.venv`**'i seç. Sonra hücreleri
yukarıdan aşağı, **Shift + Enter** ile sırayla çalıştır. Her hücre bir öncekinin
oluşturduğu değişkeni kullanır (`kayitlar`, `X`, `model`...); bir hücreyi atlarsan
sonraki hücre `NameError` verir. Takılırsan üstteki menüden "Restart" ile çekirdeği
yeniden başlat ve hücreleri yine en baştan çalıştır.

> **Bu nottaki sayılar hakkında.** Buradaki bütün sayılar **yedek veri setinden**:
> 12 kişinin 20 rengi etiketlediği, 240 satırlık hazır bir dosya. Sınıfın kendi
> verisiyle sayılar farklı çıkacak; derste gördüğün sayılar esas. Nottaki yorumları
> kendi sayılarına uygulamayı dene: "bizde de böyle mi?"

---

## Isınma: sayaç neyi sayıyor?

Bu konuda tablo hâlinde veriyle çalışıyoruz. Tablonun her satırı Python'da bir
**sözlük** olacak: sütun adları anahtar, satırdaki değerler değer. Defterin ilk hücresi
üç satırlık küçük bir örnek kuruyor:

```python
kayitlar = [
    {"ad": "kırmızı", "etiket": "enerjik"},
    {"ad": "orta mavi", "etiket": "sakin"},
    {"ad": "şeftali", "etiket": "enerjik"},
]

ilk = kayitlar[0]
print(ilk["etiket"])
```

`kayitlar` bir liste; her elemanı bir sözlük. `kayitlar[0]` ilk sözlük, onun
`"etiket"`i de `enerjik`. İki adımı iki ayrı satırda yaptık: önce kaydı al, sonra
içinden alanı al.

İkinci hücre etiketleri sayıyor ve `{'enerjik': 2, 'sakin': 1}` yazmalı:

```python
sayac = {}
for kayit in kayitlar:
    etiket = kayit["ad"]
    if etiket in sayac:
        sayac[etiket] = sayac[etiket] + 1
    else:
        sayac[etiket] = 1

print(sayac)
```

Çıktı ise `{'kırmızı': 1, 'orta mavi': 1, 'şeftali': 1}`. Hata mesajı yok, ama sonuç
yanlış: sayaç renk adlarını sayıyor. Düzeltme tek kelime: `kayit["ad"]` yerine
`kayit["etiket"]`. Bu konunun en tehlikeli hataları böyledir: Python itiraz etmez,
sonucu senin kontrol etmen gerekir.

Kaydın tamamını saymaya kalkarsan (`sayac[kayit]`) Python bu kez hata verir:

```text
TypeError: unhashable type: 'dict'
```

Okuması: "sözlük (dict) başka bir sözlüğün anahtarı olamaz." Saymak istediğin şey
kaydın kendisi değil, içindeki bir alan.

---

## Kural yazmak ile öğretmek

Bir rengin "enerjik" olup olmadığını kodla söyleyebilirsin. Aşağıda `kirmizi` ve
`yesil`, rengin içindeki kırmızı ve yeşil miktarı (0 ile 255 arası bir sayı); bu
sayıları Adım 2'de göreceğiz:

```py
if kirmizi > 200 and yesil < 100:
    print("enerjik")
```

Bu bir **kural**: sen düşündün, sen yazdın. Makine öğrenmesi bunun tersi. Kuralı sen
yazmıyorsun, **örnek veriyorsun** ve kuralı modelin bulmasını istiyorsun.

- Kural yazmak: "şu şartlarda şunu yap."
- Öğretmek: "işte 240 örnek, kuralı sen çıkar."

**Kural neden yetmiyor?** Üç sebep var, üçünü de bu konuda kendi verimizde göreceğiz:

1. **Kural, yazanın sezgisidir.** Yukarıdaki kural "enerjik = canlı kırmızı" diyor.
   Sınıfın "enerjik" dediği renklere bakınca (Adım 2'nin sonunda) şeftali, tarçın,
   bal gibi sıcak ama hiç de canlı olmayan tonları da görecek misin?
2. **Kural yazmak sıkıcı ve kırılgandır.** 20 renk için belki yazarsın; 2000 renk
   için her yeni istisnada bir `if` daha eklersin.
3. **İnsanlar anlaşamaz.** Aynı renge biri "sakin", öbürü "ciddi" diyorsa hangisinin
   kuralını yazacaksın? Model bu soruya bir cevap veriyor: **çoğunluğun**. Bu cevabın
   iyi ve kötü yanlarını Adım 5'te konuşacağız.

## Adım 1 — Sınıfın verisine bak

```python
import csv

with open("veri/renkler-etiketli.csv", encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

print(len(kayitlar))
print(kayitlar[0])
```

Çıktı:

```text
240
{'hex': '#E63946', 'ad': 'kırmızı', 'r': '230', 'g': '57', 'b': '70', 'ogrenci': 'ogrenci01', 'etiket': 'enerjik'}
```

`csv.DictReader` her satırı bir **sözlüğe** çevirir (ısınmadaki sözlüklerin aynısı).
`list(...)` bu satırları bir listede toplar. Isınmadaki küçük `kayitlar` listesinin yerine
artık gerçek veri geçti. Dosyada yedi sütun var: `hex` (renk kodu), `ad`, `r`, `g`, `b`
(rengin üç sayısı; Adım 2'de), `ogrenci` ve `etiket`. Her satır **bir öğrencinin bir
renge verdiği etiket**. 12 öğrenci × 20 renk = 240 satır. Aynı renk dosyada 12 kez
geçiyor, her seferinde başka bir öğrencinin gözünden.

Bu yapıyı aklında tut; bu konunun en ilginç bulguları bu "12 kez" gerçeğinden çıkıyor.

### Sınıf "krem"e ne demiş?

Konu 1'deki sayacın aynısı; bu kez yalnızca krem satırlarını sayıyor:

```python
sayac = {}
for kayit in kayitlar:
    if kayit["ad"] == "krem":
        etiket = kayit["etiket"]
        if etiket in sayac:
            sayac[etiket] = sayac[etiket] + 1
        else:
            sayac[etiket] = 1

print(sayac)
```

Çıktı: `{'enerjik': 5, 'ciddi': 2, 'sakin': 5}`. `"krem"` yerine `"kırık beyaz"` yazıp
hücreyi yeniden çalıştırınca: `{'enerjik': 1, 'sakin': 11}`.

Aynı sayımı 20 rengin hepsi için yapınca (renk adını değiştirip hücreyi yeniden
çalıştırarak) şöyle bir tablo çıkıyor. Yirmi satırdan beşi:

| Renk | Dağılım |
|---|---|
| krem | 5 enerjik, 5 sakin, 2 ciddi |
| koyu yeşil | 6 ciddi, 4 sakin, 2 enerjik |
| hardal | 7 enerjik, 3 sakin, 2 ciddi |
| kırık beyaz | 11 sakin, 1 enerjik |
| bordo | 11 enerjik, 1 ciddi |

Yedek veride 20 rengin 20'sinde de aynı renge farklı etiketler verilmiş. Bu bir hata
değil; gerçek veri böyledir, insanlar aynı şeye farklı etiket verir. Ama "anlaşamamak"
her renkte aynı ölçüde değil.

**Tasarım açısından okuması:** kırık beyaz ile krem ekranda neredeyse aynı renk.
Ama sınıf kırık beyaza neredeyse oybirliğiyle "sakin" derken, krem tam ortadan
ikiye bölünmüş. Aradaki tek fark kremdeki hafif sarılık. Demek ki küçük bir sıcaklık
kayması, rengin hissettirdiği şeyi değiştirebiliyor; kafe paleti için bir "sakin
beyaz" seçerken bu fark önemli. Bu iki rengi Adım 8'de tekrar göreceğiz.

**Kendin dene:** `if kayit["ad"] == "krem":` satırını silip altındaki satırların
girintisini bir kademe geri al. Sayaç bu kez bütün etiketleri sayar. Yedek veride
sonuç: 100 enerjik, 78 sakin, 62 ciddi. "Enerjik" biraz önde; bu bilgiye Adım 4'te
"kör tahmin" hesaplarken ihtiyacımız olacak. Bir etiket ezici çoğunlukta olsaydı
(diyelim 240'ın 220'si) model tembelleşirdi: hep onu der ve yine de çoğu zaman haklı
çıkardı.

### Anlaşmazlığın koyduğu tavan

Bu tablodan önemli bir sonuç çıkıyor. Modelin göreceği tek şey rengin kendisi. Aynı
renge 12 kişi farklı cevaplar verdiyse model, o renk için **tek bir** cevap
verebilir. En iyi ihtimalle çoğunluğun cevabını verir ve azınlıktakilerin hepsinde
yanılır. Kırık beyazda en iyi ihtimalle 12'de 11'ini bilir, kremde 12'de 5'ini.

Bunu 20 rengin hepsi için yapıp topladık: her rengin en çok verilen etiketinin sayısı,
toplam 240 satıra bölündü. Sonuç, sadece renge bakan en iyi modelin doğruluğu. Bu
hesabı defterde yapmıyoruz (her renk için ayrı sayaç gerekiyor); sonucunu veriyoruz.

Yedek veride bu sayı **0.74**. Yani mükemmel bir model bile her dört cevaptan birini
"yanlış" bilecek. Bu yanlışlar modelin kusuru değil; sınıfın kendi içindeki görüş
ayrılığı. Bu sayıya **tavan** diyoruz.

## Adım 2 — Rengi sayıya çevir

Model "kırmızı" kelimesini anlamaz, sayı ister. Bir tasarım programının renk seçicisini
hatırla: `#E63946` yazınca yanında **R 230, G 57, B 70** görürsün. Renk kodu bu üç
sayının kısaltılmış yazılışıdır: kırmızı, yeşil ve mavi miktarı (RGB), her biri 0 ile
255 arasında. `E6` → 230, `39` → 57, `46` → 70. Bu çeviriyi elle yapmayacağız:
dosyada üç sayı zaten hazır, `r`, `g` ve `b` sütunlarında.

```python
X = []
y = []
for kayit in kayitlar:
    r = int(kayit["r"])
    g = int(kayit["g"])
    b = int(kayit["b"])
    X.append([r, g, b])
    y.append(kayit["etiket"])

print(len(X), len(y))
print(X[0], y[0])
```

Çıktı:

```text
240 240
[230, 57, 70] enerjik
```

- `int(kayit["r"])`: dosyadan okunan her şey **metindir**. Adım 1'in çıktısında
  `'r': '230'` tırnak içindeydi. `int` metni sayıya çevirir: `'230'` → `230`.
- `[r, g, b]` üç sayılık küçük bir liste: bir renk. `X.append(...)` bu rengi `X`
  listesinin sonuna ekler. Yani `X` renklerden oluşan bir liste; her rengi de üç sayı.
- `y.append(kayit["etiket"])` aynı kaydın etiketini `y`'nin sonuna ekler.

`int`'i unutursan ne olur? `X`'e `['230', '57', '70']` gibi metinler girer. Bu döngüde
hata çıkmaz; model eğitilirken (Adım 4) şu mesajla durur:

```text
ValueError: dtype='numeric' is not compatible with arrays of bytes/strings.
```

Okuması: "sayı bekliyordum, metin geldi." Metinleri toplamaya kalkarsan daha sinsi bir
şey olur: `'230' + '57'` hata vermez, `'23057'` yazar; Python iki metni yan yana
yapıştırır. Alıştırma defterinin ilk bozuk kodu bu.

### Üç sayıyı okumayı öğren

Model rengi yalnızca bu üç sayı olarak görecek. Senin de bu sayılara bakıp rengi
kabaca tahmin edebilmen, modelin neyi görüp neyi göremediğini anlamanı kolaylaştırır:

| Renk | RGB | Nasıl okunur |
|---|---|---|
| lacivert `#1D3557` | 29, 53, 87 | Üçü de küçük: koyu. Mavi en büyük: mavimsi |
| kırık beyaz `#F1FAEE` | 241, 250, 238 | Üçü de büyük ve birbirine yakın: açık, neredeyse renksiz |
| krem `#FEFAE0` | 254, 250, 224 | Kırık beyaza çok yakın, ama mavi biraz düşük: hafif sarımsı |
| bordo `#9A031E` | 154, 3, 30 | Kırmızı baskın, öbür ikisi neredeyse sıfır: koyu ama doygun |
| gri mavi `#8D99AE` | 141, 153, 174 | Üçü birbirine yakın, mavi biraz önde: grimsi mavi |

Kısaca: üç sayı da küçükse renk koyudur, üçü de büyükse açıktır; üçü birbirine
yakınsa renk grimsidir, biri öbürlerinden çok büyükse renk o yöne doygundur.

### Başta yazdığımız kural ne kadar iş görüyor?

Artık kuralı gerçek veride sınayabiliriz: her kayıt için üç sayıya bak, etiket
"enerjik" ise ve `kirmizi > 200 and yesil < 100` şartı tutuyorsa say. Yedek veride
sonuç: 100 "enerjik" etiketinden kural yalnızca **8**'ini yakalıyor.

Kural 20 renkten sadece birini (kırmızıyı) tanıyor. Bordo, şeftali, somon, tarçın ve
bal da sınıfın çoğunluğuna göre enerjik; ama hiçbiri "kırmızı 200'den büyük, yeşil
100'den küçük" şartına uymuyor. Sınıfın "enerjik" kavramı, kuralı yazan kişininkinden
çok daha geniş: canlı renklerle birlikte **sıcak** tonların neredeyse hepsini içeriyor.
İşte örnekten öğrenmenin gücü burada: kimsenin aklına gelmeyen bu genişliği veri
kendisi taşıyor.

## Öznitelik ve etiket: X ve y

Adım 2'nin döngüsü iki liste dolduruyor:

- **X** (öznitelikler): modelin **baktığı** şey; burada üç sayı.
- **y** (etiket): modelin **tahmin etmesi gereken** şey; burada "enerjik", "sakin", "ciddi".
- `X[5]`'in cevabı `y[5]`'tir. İkisi aynı sırada olmak zorunda.

**Model neye bakmıyor?** Bu soru en az "neye bakıyor" kadar önemli. Model rengin
adını görmüyor ("bordo" kelimesinin çağrışımlarını bilmiyor). Rengin nerede
kullanıldığını görmüyor (bir duvarda mı, bir düğmede mi). Rengin yanındaki öbür
renkleri görmüyor; oysa bir tasarımcı için bir rengin etkisi komşularına çok bağlı.
Sen renge bakarken bunların hepsi devrede; modelde yalnızca üç sayı var. Modelin
bazı yanılgıları tam olarak bu eksikten gelecek.

Öznitelik seçmek bir tasarım kararıdır: "bu problemde neye bakmak önemli?" Burada
en basit seçimi yaptık. İleride rengin açıklığını ya da doygunluğunu ayrı öznitelik
olarak eklemek mümkün; Konu 4'te "aynı şeyi farklı sayılarla temsil etmek" fikrine
geri döneceğiz.

**Sıra kayarsa ne olur?** Diyelim X'i doldururken bazı satırları atladın ama y'yi
atlamadın. İki durum var:

- **Uzunluklar farklıysa** program Adım 4'te, eğitim sırasında durur:

  ```text
  ValueError: Found input variables with inconsistent numbers of samples: [200, 240]
  ```

  Okuması: "girdilerinin örnek sayıları tutarsız: biri 200, öbürü 240." Bu iyi bir
  hata; sana sorunun yerini gösteriyor.
- **Uzunluklar aynı ama sıra kaymışsa** hiçbir hata mesajı almazsın. Model lacivertin
  cevabı olarak şeftalinin etiketini öğrenir ve sessizce saçma sonuçlar üretir. Bunu
  önlemenin yolu basit: X ve y'yi **aynı döngüde, aynı kayıttan** doldur.

Alıştırma defterindeki 2. bozuk kod bu hatanın küçük bir örneği: iki liste aynı
döngüde ama aynı koşulla dolmuyor, biri 3 öğeli kalırken öbürü 6 öğeli oluyor.

## Adım 3 — Veriyi ikiye böl: eğitim ve test

Modeli 240 örnekle eğitip yine aynı 240 örnekle sınarsak ne ölçmüş oluruz? **Ezberi.**
Sınavda çıkmış soruyla sınav yapmak gibi: öğrenip öğrenmediğini anlamak için
**görmediği** soruyu sormak gerekir.

- **Eğitim verisi:** model bunlara bakarak öğrenir.
- **Test verisi:** model bunları hiç görmez; ölçüm burada yapılır.

```python
from sklearn.model_selection import train_test_split

X_egitim, X_test, y_egitim, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
print(len(X_egitim), len(X_test))
```

Çıktı: `180 60`.

- `from sklearn.model_selection import train_test_split`: kütüphaneden yalnızca
  bölme işini yapan parçayı alıyoruz.
- Soldaki **dört değişken tek satırda** dolar: fonksiyon dört liste verir, Python
  onları soldaki adlara sırayla dağıtır. Sıra önemli; karıştırma. Sıra her zaman:
  eğitim X, test X, eğitim y, test y.
- Satır uzun olduğu için parantezin içini alt satıra aldık. Parantez kapanana kadar
  Python satırı bitmiş saymaz.
- `test_size=0.25`: verinin dörtte biri (60 örnek) teste ayrılır, 180'i eğitimde kalır.
- `train_test_split` satırları **karıştırarak** böler. Karıştırmasaydı test verisi
  dosyanın son 60 satırı olurdu: yani son üç öğrencinin etiketleri. Model bu
  öğrencilerin hiçbirini görmeden sınanırdı; bu ayrı bir soru olurdu.
- `random_state=42`: karıştırma rastgeledir; bu sayı her çalıştırmada **aynı**
  karıştırmanın çıkmasını sağlar. Böylece sen ve arkadaşın aynı sonucu görürsünüz ve
  bir şeyi değiştirdiğinde farkın senin değişikliğinden geldiğini bilirsin. 42'nin
  özel bir anlamı yok; herhangi bir sayı olabilir.

### Test verisine "bakmak" neden hile?

Kimse bilerek kopya çekmez; test verisi genellikle kazara sızar. Üç tanıdık yol:

1. **Aynı veride eğitip ölçmek.** En açık olanı. Alıştırma defterindeki 5. bozuk kod.
2. **Cevabı özniteliğin içine koymak.** Örneğin X'e üç sayının yanına etiketi de
   eklemek. Model cevabı sorudan okuyabilir, sonuç gerçekte olduğundan iyi görünür.
   (Etiketi metin olarak eklersen scikit-learn şikâyet eder; ama sayıya çevrilmiş bir
   etiket sessizce geçer.)
3. **Test sonucuna bakıp ayar yapmak, sonra yine aynı testte ölçmek.** Diyelim komşu
   sayısını 5'ten 9'a çıkardın, testte doğruluk arttı, 9'da karar kıldın. Bunu elli
   kez yaparsan test verisine göre ayar çekmiş olursun; test artık "görülmemiş" değildir.

Üçünün ortak sonucu: **sayı gerçekte olduğundan iyi görünür**. Bu, kötü bir sayıdan
daha tehlikelidir, çünkü sana yanlış bir güven verir. Bir tasarım müşterisine "bu
model renkleri %98 doğru etiketliyor" dediğini, sonra yeni renklerde modelin yazı
tura gibi davrandığını düşün.

## Adım 4 — Modeli eğit ve ölç

Kullandığımız modelin adı **k-NN** (k en yakın komşu). Mantığı tek cümle:

> Bu renge en çok benzeyen 5 rengi bul; onlar ne dediyse onu de.

Buradaki **k** kaç komşuya bakılacağı; bizde 5. Formül yok. "Benzemek" burada üç RGB
sayısının birbirine yakın olması demek. Komşular farklı şeyler diyorsa çoğunluk kazanır.

**Elle bir örnek.** Model eğitim verisinde hiç olmayan buz mavisi `#CFE3F2`
(207, 227, 242) rengini soruyor olsun. Üç sayının hepsi büyük ve birbirine yakın:
açık, hafif mavimsi bir renk. Verideki renklerden buna en yakın olanı kırık beyaz
(241, 250, 238). Kırık beyaz dosyada 12 kez geçtiği için beş en yakın komşunun beşi de
kırık beyaz etiketleri çıkar. Sınıfın 11 kişisi kırık beyaza "sakin" dediği için bu
beşin çoğunluğu da "sakin"dir; model de "sakin" der.

Bu örnek bizim veri hakkında önemli bir şey gösteriyor: her renk dosyada 12 kez
geçtiği için, modelin "5 komşusu" çoğu zaman **aynı rengin 5 ayrı etiketi**. Yani
bizim modelimiz pratikte şunu yapıyor: "bu renge en çok benzeyen renk hangisiyse,
onu etiketleyen arkadaşlarından beşine sor, çoğunluk ne dediyse onu de."

```python
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_egitim, y_egitim)
dogruluk = model.score(X_test, y_test)
print(round(dogruluk, 2))
```

Çıktı: `0.77`.

`KNeighborsClassifier(n_neighbors=5)` modeli **oluşturur**: kaç komşuya bakacağını
söylüyoruz. `fit` ve `score` ise `metin.split()` ya da `X.append()` gibi, bir şeyin
arkasına nokta koyup verilen komutlar; yeni olan tek şey bu kez o şeyin bir model olması.

- `fit`: "bu örneklere bak ve öğren."
- `score`: "hiç görmediklerinin kaçını bildin?" 0 ile 1 arası bir sayı döndürür.
- `round(dogruluk, 2)`: sayıyı virgülden sonra iki basamağa yuvarlar (0.7666... → 0.77).
- Bir komut daha var, `predict`: "şu renk sence hangisi?" Onu Adım 5'te kullanıyoruz.

`fit` ile k-NN aslında hiçbir hesap yapmaz; eğitim örneklerini bir kenara kaydeder.
Asıl iş, soru geldiğinde (`score` ya da `predict` sırasında) yapılır: en yakın beş
örnek o anda aranır. Başka modeller `fit` sırasında çok daha fazla iş yapar; ama
"önce örnekleri ver, sonra soru sor" düzeni hepsinde aynıdır.

`fit`'i unutup doğrudan soru sorarsan:

```text
NotFittedError: This KNeighborsClassifier instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator.
```

Okuması: "bu model henüz eğitilmedi; kullanmadan önce `fit`'i çağır." Hata
mesajları İngilizce ama çoğu zaman ne yapman gerektiğini açıkça söyler; son satırı
dikkatle oku.

## Sonuç bir şey ifade ediyor mu?

0.77, test renklerinin %77'sini bildi demek. Doğruluk tek başına anlamsız; iki kıyas
noktası gerekir.

**Alttan kıyas — kör tahmin:** hiç düşünmeden hep en sık etiketi deseydik test
verisinde kaçını bilirdik? Adım 1'de en sık etiketin "enerjik" olduğunu gördük.
Test verisindeki "enerjik" etiketlerini sayıp toplam test satırına bölüyoruz:

```python
enerjik = 0
for etiket in y_test:
    if etiket == "enerjik":
        enerjik = enerjik + 1

kor_tahmin = enerjik / len(y_test)
print(round(kor_tahmin, 2))
```

Çıktı: `0.45`. Önce bölmeyi ayrı bir satırda yapıp sonucu `kor_tahmin`'e koyduk, sonra
yuvarlayıp yazdırdık.

**Üstten kıyas — tavan:** Adım 1'de gördük; sınıf anlaşamadığı için sadece renge bakan
hiçbir model belli bir sayıyı geçemez. Aynı hesabı yalnızca bu 60 test satırı için
yapınca tavan 0.80 çıkıyor (60 satırdan 48'i).

Üç sayıyı yan yana koyunca tablo netleşiyor:

| | Doğruluk | Ne anlama geliyor |
|---|---|---|
| Kör tahmin (hep "enerjik") | 0.45 | Hiç düşünmeden alınabilecek puan |
| Bizim model | 0.77 | 60 test satırından 46'sı |
| Tavan | 0.80 | Sınıfın anlaşmazlığı yüzünden aşılamayacak sınır |

Model kör tahmini açık farkla geçti: gerçekten bir örüntü öğrenmiş. Ve tavana iki
cevap kalmış. Yani bu veriyle modeli daha "akıllı" yapmaya çalışmak boşuna; kalan
yanlışların neredeyse hepsi modelin değil, **sınıfın görüş ayrılığının** payı. Bu
sonucu doğru okumak, doğruluğu yükseltmeye çalışmaktan daha değerli.

### k'yı değiştirmek: kaç arkadaşa sormalı?

Adım 4'ün ilk hücresinde `n_neighbors=5` yerine başka sayılar yazıp yeniden çalıştır.
Yedek veride: k=1 → 0.70, k=5 → 0.77, k=15 → 0.73, k=45 → 0.72.

- **k=1** "tek bir arkadaşa sor" demek. O arkadaş azınlıktaysa model de azınlığın
  cevabını verir. Tek bir örneğe fazla güvenmek, **ezberlemenin** en basit hâli:
  model genel eğilimi değil, rastgele bir örneği tekrarlıyor.
- **k=5** çoğu renkte aynı rengin beş etiketine bakıyor; çoğunluğu iyi yakalıyor.
- **k=15 ve k=45**: her renk eğitimde yaklaşık 9 kez geçiyor. Komşu sayısı bundan
  büyük olunca model başka renklerin oylarını da saymaya başlıyor; lacivertin
  kararına petrolün etiketleri karışıyor.

Bu deneme bir tuzak da içeriyor: en iyi k'yı test verisine bakarak seçersek, yukarıda
"test sonucuna bakıp ayar yapmak" dediğimiz şeyi yapmış oluruz. (Nitekim k=9 bu testte
0.78 veriyor; 5'ten iyi görünüyor ama bu, bu 60 satıra özgü olabilir.) Burada sadece
fikri görmek için deniyoruz; ciddi bir işte ayar için ayrı bir veri parçası kullanılır.
Denemeden sonra `n_neighbors=5`'e geri dön ve hücreyi yeniden çalıştır; sonraki adımlar
bu modeli kullanıyor.

### Tek sayıya güvenme

Adım 3'te `random_state=42` yerine başka sayılar verirsen bölme değişir, doğruluk da
değişir. Yedek veride `random_state` 0, 1, 2, 3, 4 için sonuçlar: 0.65, 0.67, 0.72,
0.68, 0.78. Aynı model, aynı veri; sadece hangi 60 satırın teste düştüğü değişiyor.
Test verisi küçük olunca tek bir satır bile sonucu yaklaşık iki puan oynatıyor
(1/60 ≈ 0.017). O yüzden "0.77" demek yerine "0.65 ile 0.78 arasında bir yerde" demek
daha dürüst. Adım 6'daki grafiğin neden dalgalandığını anlamak için bu bilgiye
ihtiyacın olacak.

### Eğitim verisinde ölçseydik?

`model.score(X_test, y_test)` yerine `model.score(X_egitim, y_egitim)` yazarsan model
gördüğü sorularla sınanır. Genelde bu sayı testtekinden **yüksek** çıkar; model görmüş
olduğu soruları daha iyi bilir. Alıştırma defterindeki 5. bozuk kodun küçük verisinde
bu fark çok açık (eğitimde 1.0, testte 0.33). Bizim veride ise şaşırtıcı bir şey
oluyor: eğitimde 0.69, testte 0.77. Neden? Çünkü eğitim verisinde de her renk birden
çok kez, farklı etiketlerle geçiyor. Model bir renk için tek cevap verebildiğinden,
eğitimde gördüğü azınlık etiketlerinde de yanılıyor. Ezber, anlaşmazlığı çözemiyor.
Bu, "tavan" fikrinin başka bir görünüşü. Kural yine değişmez: **doğruluk test
verisinde ölçülür.**

## Adım 5 — Yanıldığı yere bak

Doğruluk tek bir sayı; asıl öğretici olan modelin **nerede** yanıldığı. Bunun için
test satırlarının adlarını bilmemiz gerek. `X_test`'te yalnızca sayılar var; adlar
`kayitlar`'da. Çözüm: `kayitlar`'ı da **aynı** ayarlarla bölmek.

```python
egitim_kayitlari, test_kayitlari = train_test_split(
    kayitlar, test_size=0.25, random_state=42
)
print(len(test_kayitlari))
```

Çıktı: `60`. Liste uzunluğu (240) ve `random_state` (42) aynı olduğu için karıştırma
da aynı çıkar: `test_kayitlari`, `X_test`'teki 60 rengin kayıtları, aynı sırada. Bu
sefer tek liste verdik, o yüzden fonksiyon iki şey döndürüyor: eğitim ve test.

Şimdi her test kaydını tek tek modele soruyoruz:

```python
for kayit in test_kayitlari:
    r = int(kayit["r"])
    g = int(kayit["g"])
    b = int(kayit["b"])
    renk = [r, g, b]
    tahminler = model.predict([renk])
    tahmin = tahminler[0]
    if tahmin != kayit["etiket"]:
        print(kayit["ad"], "öğrenci:", kayit["etiket"], "model:", tahmin)
```

- Döngünün ilk dört satırı Adım 2'deki gibi: kayıttan üç sayıyı al, `renk` listesini kur.
- `model.predict([renk])`: "bu renk sence hangisi?" `predict` her zaman bir **renk
  listesi** ister, tek renk sorsan bile; o yüzden `renk`'i köşeli parantez içine
  koyuyoruz. Cevabı da liste olarak verir; `tahminler[0]` o listenin ilk (ve tek) elemanı.
- `if tahmin != kayit["etiket"]:` model öğrencinin etiketinden farklı bir şey dediyse
  yanılmış demektir: ekrana yazdır.

Yedek veride ilk üç satır:

```text
lacivert öğrenci: enerjik model: ciddi
orta mavi öğrenci: sakin model: ciddi
şeftali öğrenci: ciddi model: enerjik
```

Toplam 14 satır çıkıyor.

`predict`'e rengi köşeli parantez olmadan verirsen (`model.predict(renk)`) uzun bir
mesaj alırsın:

```text
ValueError: Expected 2D array, got 1D array instead:
array=[29 53 87].
```

Okuması: "iki boyutlu bir dizi (renklerden oluşan bir liste) bekliyordum, tek boyutlu
geldi (tek bir renk)." Çözüm, rengi bir listenin içine koymak: `model.predict([renk])`.
Mesajın devamındaki `reshape` önerisini görmezden gelebilirsin; o, bu derste
kullanmadığımız bir kütüphanenin yolu.

### Yanılgıları okumak

Yedek veride 60 test satırından 14'ünde model yanılıyor. Her yanlışı Adım 1'in
sayacıyla (o renge sınıfın tamamının ne dediğiyle) yan yana koyunca iki grup çıkıyor:

**Birinci grup (14 yanılgının 12'si): öğrenci azınlıkta.** Örneğin bir öğrenci
şeftaliye "ciddi" demiş; sınıfın 10 kişisi "enerjik" demiş, model de "enerjik" diyor.
Bu satır "yanlış" sayılıyor ama model sınıfın ortak görüşünü söylüyor. Bu 12 satırın
yarısında azınlıktaki öğrenci sıcak, toprak tonlu bir renge (şeftali, tarçın, bal,
somon, gül kurusu) "ciddi" demiş. Sınıfın bir kısmı bu tonları ağırbaşlı buluyor;
model bu sesi hiç duyamıyor.

**İkinci grup (2 yanılgı): model sınıfın çoğunluğundan da ayrılmış.** Orta mavi için
model "ciddi" diyor, oysa sınıfın 8 kişisi "sakin" demiş. Sebep Adım 4'teki gözlem:
model eğitimdeki 11 orta mavi etiketinden (7 sakin, 3 ciddi, 1 enerjik) yalnızca 5'ine bakabiliyor ve rastlantıyla o beşin
içinde "ciddi" diyenler ağır basmış. Koyu yeşilde de benzer bir durum var (6 ciddi,
4 sakin; model "sakin" diyor).

**Tasarım açısından okuması:**

- **Model bir "çoğunluk sesi" üretir.** Sınıfın verisiyle eğitilen bir model, sınıfın
  ortalama görüşünü tekrarlar ve azınlığı siler. Bir marka paleti için bu işe
  yarayabilir ("çoğu insan bu rengi sakin buluyor"); ama hedef kitlen o azınlıksa
  model sana yanlış yol gösterir.
- **"Yanlış" satırlar tartışmalı renklerin haritasıdır.** Yanılgılar sınıfın bölündüğü
  renklerde toplanıyor (şeftali, gül kurusu ve bal ikişer kez). Adım 1'deki en
  tartışmalı renkler (krem, koyu yeşil, hardal) ise tek bir duyguyu taşımak için
  riskli. Kafe için "kesin sakin" bir renk arıyorsan bu renklerden uzak dur.
- **Model "hata yapıyor" demek her zaman "model kötü" demek değildir.** Bazen hata
  modelde, bazen etikette, bazen de sorunun kendisinde: "Bu renk sakin mi?" sorusunun
  tek bir doğru cevabı olmayabilir.

Listeye bakarken kendine şunu sor: "Ben olsam bu renge ne derdim, model mi haklı,
öğrenci mi?"

## Adım 6 — Veri arttıkça ne oluyor?

Modeli eğitim verisinin önce ilk 18 örneğiyle, sonra 45, 90, 135 ve 180 örnekle
(yani %10, %25, %50, %75 ve tamamıyla) eğitip her seferinde aynı test verisinde
ölçüyoruz:

```python
adetler = [18, 45, 90, 135, 180]
dogruluklar = []
for adet in adetler:
    X_ilk = X_egitim[:adet]
    y_ilk = y_egitim[:adet]
    yeni_model = KNeighborsClassifier(n_neighbors=5)
    yeni_model.fit(X_ilk, y_ilk)
    dogruluk = yeni_model.score(X_test, y_test)
    print(adet, round(dogruluk, 2))
    dogruluklar.append(dogruluk)
```

- `X_ilk = X_egitim[:adet]` Konu 1'in dilimlemesi: baştan `adet` tane örnek. `adet` 18 iken
  ilk 18 renk, 90 iken ilk 90 renk. `y_ilk` aynı satırların etiketleri.
- Döngü her tur yeni bir model kurup eğitiyor, ölçüyor, sonucu yazdırıp
  `dogruluklar` listesine ekliyor. Bu modellere `yeni_model` adını verdik ki Adım 4'teki
  `model` değişmesin. Son turda (180 örnek) `yeni_model` Adım 4'teki modelin aynısı.

Yedek veride çıktı:

```text
18 0.48
45 0.72
90 0.62
135 0.75
180 0.77
```

Sonra iki listeyi çiziyoruz:

```python
import matplotlib.pyplot as plt

plt.plot(adetler, dogruluklar, marker="o")
plt.xlabel("Eğitim örneği sayısı")
plt.ylabel("Test doğruluğu")
plt.show()
```

`plt.plot` noktaları çizgiyle birleştirir: yatayda `adetler`, dikeyde `dogruluklar`.
`marker="o"` her ölçümü bir nokta olarak gösterir. `xlabel` ve `ylabel` eksenlerin adı.

Eğri genelde önce hızlı yükselir, sonra düzleşir. **Düzleştiği yer önemli:** oradan
sonra veri eklemek pek işe yaramıyor demektir. Bizim veride düzleşme noktası tavanın
hemen altı: 180 örnekle 0.77'ye, tavana (0.80) iki cevap kalana kadar geldik. Aynı
20 renge daha çok öğrenci etiketi eklemek bu tavanı yükseltmez. Tavanı yükseltmek
için **başka türlü** veri gerekir: daha çok renk ya da rengin kullanıldığı bağlam gibi
yeni bilgiler.

**18 örnekle neden bu kadar kötü?** 18 örnekte 20 rengin ancak 14'ü var; 6 renk hiç
yok. Model görmediği bir rengi sorulduğunda ona en çok benzeyen başka bir rengin
etiketlerini kullanmak zorunda kalıyor. Az veri, "tanıdık renk" sayısını azaltıyor.

**Eğri ortada düşebilir.** Yedek veride 45 örnekten 90 örneğe çıkınca doğruluk
0.72'den 0.62'ye iniyor. Bu bir hata değil; düzeltmeye çalışma. İpucu: 90 örneklik
parçada gri mavi yalnızca bir kez geçiyor ve onu etiketleyen öğrenci azınlıktan
("ciddi" demiş). Model de gri maviyi sorduğunda bu tek etiketin yanına en yakın başka
rengin, gül kurusunun etiketlerini ekliyor. Test verisi de küçük (Adım 4'teki "tek
sayıya güvenme" bölümünü hatırla). Neden olduğunu ödevde kendi verinle düşüneceksin,
Konu 4'ün başında birlikte konuşacağız.

## Adım 7 — Model ne öğrendi? Kafe paletini sor

Modelin içini açıp "kuralını" okuyamayız. Ama bir tasarımcının kullanıcı testinde
yaptığını yapabiliriz: ona hiç görmediği renkler gösterip cevaplarına bakmak. Bunun
için modeli bu kez **tüm veriyle** (`X`, `y`) eğitiyoruz; ölçüm yapmıyoruz, sadece
soru soruyoruz.

```python
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X, y)

bej = [232, 220, 196]
sutlu_kahve = [212, 163, 115]
adacayi = [163, 177, 138]
orman_yesili = [52, 78, 65]
kirli_beyaz = [245, 245, 245]

palet = [bej, sutlu_kahve, adacayi, orman_yesili, kirli_beyaz]
tahminler = model.predict(palet)
print(tahminler)
```

- Beş renk, Konu 1'deki "sessiz çalışma kafesi" için aday bir palet: bej `#E8DCC4`,
  sütlü kahve `#D4A373`, adaçayı `#A3B18A`, orman yeşili `#344E41`, kirli beyaz
  `#F5F5F5`. Sayıları renk seçicinin RGB kutularından aldık.
- `palet` beş rengin listesi; `X` gibi, her elemanı üç sayılık bir renk. `predict`'e
  bu kez beş rengi birden veriyoruz, beş cevap geliyor.

Çıktı:

```text
['enerjik' 'enerjik' 'sakin' 'ciddi' 'sakin']
```

Cevaplar paletle aynı sırada. (Aralarında virgül yok, çünkü `predict` sıradan bir
Python listesi değil, scikit-learn'ün kendi dizisini döndürüyor; okuması aynı.)

Yedek veride sonuç, her rengin "en yakın bildiği renk"iyle birlikte (bu sütunu ayrı
bir komutla bulduk; defterde göstermiyoruz):

| Renk | Modelin cevabı | En yakın bildiği renk |
|---|---|---|
| bej `#E8DCC4` | enerjik | krem |
| sütlü kahve `#D4A373` | enerjik | bal |
| adaçayı `#A3B18A` | sakin | gri mavi |
| orman yeşili `#344E41` | ciddi | petrol |
| kirli beyaz `#F5F5F5` | sakin | kırık beyaz |

Kafelerde çok sevilen sıcak nötrler (bej, sütlü kahve) bu sınıfın verisine göre
"sakin" değil, "enerjik" tarafta. Adaçayı ve kirli beyaz ise güvenli görünüyor.

Ama bu tabloyu okumadan önce "en yakın bildiği renk" sütununa bak. **Bej hakkındaki
kararı aslında model vermiyor; kremi etiketleyen arkadaşların veriyor.** Ve krem,
Adım 1'de gördüğümüz gibi sınıfın en çok tartıştığı renk (5 enerjik, 5 sakin). Yani
bejin "enerjik" çıkması güçlü bir bulgu değil, zayıf bir işaret: "bu bölge tartışmalı,
kullanıcıyla sınanmalı." Modelin bildiği dünya 20 renkten ibaret. 20 rengin hiçbirine
benzemeyen bir renk sorarsan, model yine de bir cevap verir; ama o cevap bir tahminden
çok, en yakın tanıdığın görüşüdür.

Bu, veriyi kimin ve hangi renklerle topladığının da bir tasarım kararı olduğunu
gösteriyor. Kafe paleti hakkında güvenilir bir model istiyorsan, etiketleme ödevine
bej ve kahve tonları da koymak gerekirdi.

**Kendin dene: koyuluk her renkte aynı işi mi yapıyor?** Paletteki beş rengin
sayılarını aynı rengin koyudan açığa sürümleriyle değiştir. Maviler (`[10, 31, 68]`,
`[74, 127, 176]`, `[207, 227, 242]`) yedek veride ciddi, sakin, sakin çıkıyor.
Kırmızılar (`[92, 0, 16]`, `[214, 40, 40]`, `[250, 212, 212]`) ise üçü de enerjik.
Sınıfın gözünde koyuluk tek başına ciddiyet getirmiyor; renk tonu koyuluktan güçlü
basıyor. Bordoya 12 kişiden 11'inin "enerjik" demesi bunun kaynağı.

## Adım 8 — Hiç görmediği bir renk: dürüst sınav

Adım 3'teki bölmeye geri dönelim. Satırları karıştırıp dörtte birini teste ayırdık;
ama her renk dosyada 12 kez geçtiği için, testteki bir kırık beyaz satırının kardeşleri
eğitimde duruyor. Model teste gelmeden kırık beyazın ne olduğunu başka öğrencilerden
zaten duymuş. Adım 3'teki test aslında şunu ölçüyor: "bilinen bir renk için başka bir
öğrencinin ne diyeceğini tahmin edebiliyor mu?"

Bu kötü bir soru değil. Ama "yeni bir renk gelince model ne der?" sorusunun cevabı
değil. Onu ölçmek için bir rengi **tamamen** dışarıda bırakmak gerekir: model o rengin
hiçbir satırını görmeden eğitilir, sonra o renk sorulur. Kırık beyazla deneyelim:

```python
X_haric = []
y_haric = []
for kayit in kayitlar:
    if kayit["ad"] != "kırık beyaz":
        r = int(kayit["r"])
        g = int(kayit["g"])
        b = int(kayit["b"])
        X_haric.append([r, g, b])
        y_haric.append(kayit["etiket"])

print(len(X_haric))
```

Çıktı: `228`. Adım 2'nin döngüsünün aynısı, tek farkla: `if kayit["ad"] != "kırık beyaz":`
satırı kırık beyazın 12 satırını atlıyor (`!=` "eşit değilse" demek). 240 − 12 = 228.

```python
model_haric = KNeighborsClassifier(n_neighbors=5)
model_haric.fit(X_haric, y_haric)

kirik_beyaz = [241, 250, 238]
tahminler = model_haric.predict([kirik_beyaz])
print(tahminler[0])
```

Çıktı: `enerjik`. Adım 7'deki model (kırık beyazı görmüş olan) ne diyor?

```python
tahminler = model.predict([kirik_beyaz])
print(tahminler[0])
```

Çıktı: `sakin`. Sınıfın 11/12'si de "sakin" demişti. Aynı renk, iki model, iki cevap.
Kırık beyazı hiç görmeyen modelin en yakın bildiği renk krem; kremi etiketleyenlerin
neredeyse yarısı da "enerjik" demişti.

**Kendin dene:** `"kırık beyaz"` yerine `"gri mavi"` yaz, `kirik_beyaz` listesinin
sayılarını `[141, 153, 174]` yap ve Adım 8'in üç hücresini sırayla yeniden çalıştır. Yedek veride gri
maviyi hiç görmeyen model de "enerjik" diyor (sınıfın 10/12'si "sakin" demişti).

### Aynı şeyi 20 renk için yapınca

Bu deneyi 20 rengin her biri için sırayla yapıp her seferinde dışarıdaki rengin 12
etiketinden kaçını bildiğini topladık (hesabı defterde yapmıyoruz; iç içe döngü
gerektiriyor). Sonuç:

| Test türü | Doğruluk |
|---|---|
| Rastgele bölme (bilinen renkler, Adım 4) | 0.77 |
| Hiç görülmemiş renkler | **0.60** |

Aradaki fark "tanıdık renk" avantajının büyüklüğü. İkisi de doğru sayı, ama farklı
soruların cevabı. Bir sonucu raporlarken **hangi soruyu sorduğunu** da söylemen gerekir.

Yirmi rengin 4'ünde (kırık beyaz, gri mavi, gül kurusu, zeytin) rengi hiç görmeyen
model sınıfın çoğunluğundan ayrılıyor. İkisi özellikle öğretici:

- **Kırık beyaz → model "enerjik" diyor, sınıf "sakin" (11/12).** Kırık beyazı hiç
  görmeyen modelin en yakın bildiği renk krem. Sayılarda neredeyse ikiz: (241, 250,
  238) ile (254, 250, 224). Ama sınıf ikisini çok farklı hissetmiş. Model bu farkı
  göremez; onun için iki renk arasındaki mesafe küçük.
- **Gri mavi → model "enerjik" diyor, sınıf "sakin" (10/12).** Gri mavinin RGB'de en
  yakın komşusu gül kurusu çıkıyor. Birisi soğuk grimsi bir mavi, öbürü tozlu bir
  pembe; bir tasarımcı bu ikisine asla "benzer" demez. Ama üç sayının farkına
  bakınca yakınlar.

**Tasarım açısından okuması:** RGB sayılarının yakınlığı ile **insan gözünün**
benzerlik algısı aynı şey değil. Model "benzerlik" kavramını bizim ona verdiğimiz
temsilden alıyor; temsil kötüyse model de "benzer" diye yanlış şeyleri eşleştiriyor.
Bir tasarımcının renk seçerken RGB kaydırıcıları yerine ton-doygunluk-açıklık
seçicisini tercih etmesinin sebebi de buna benzer: o gösterim, algıya daha yakın.
Konu 4'ün sorusu tam burada başlıyor: **bir şeyi hangi sayılarla temsil edersen,
"benzer" kelimesinin anlamını da o belirler.**

## Bonus — Kendi rengini sor

Defterin son hücresi:

```python
benim_rengim = [106, 13, 173]
tahminler = model.predict([benim_rengim])
print(tahminler[0])
```

`model`, Adım 7'de tüm veriyle eğitilen model. Hücrede canlı bir mor var (`#6A0DAD`).
Yedek veride model ona "sakin" diyor: en yakın bildiği renk puslu mor. Bir tasarımcı bu
doygun mora "sakin" demekte zorlanır; ama model canlılığı ayrı bir şey olarak görmüyor,
yalnızca 20 renkten hangisine yakın olduğunu biliyor (Adım 7'deki bej gibi).

Sonra renk seçiciden kendi rengini seç, RGB sayılarını `benim_rengim`'e yaz ve çalıştır.
Modelle aynı fikirde misin? Ayrıldığınız bir renk varsa not al; Konu 4'ün başında sınıfça
bakacağız.

---

## Defterin bölümleri

| Adım | Ne yaptık | Elimizde ne oluştu |
|---|---|---|
| Isınma | Sayacın neyi saydığını düzelttik | — |
| 1 | Veriyi okuduk, bir rengin etiketlerini saydık | `kayitlar` |
| 2 | Sayıya çevirdik | `X`, `y` |
| 3 | İkiye böldük | `X_egitim`, `X_test`, `y_egitim`, `y_test` |
| 4 | Eğittik, ölçtük, kör tahminle kıyasladık | `model`, doğruluk |
| 5 | Yanılgılara baktık | modelin 14 yanılgısının listesi |
| 6 | Veri miktarını değiştirdik | öğrenme eğrisi |
| 7 | Modeli kafe paletiyle yokladık | kafe paleti için ikinci görüş |
| 8 | Hiç görmediği bir renkte sınadık | `model_haric` |
| Bonus | Kendi rengini sorduk | — |

Hepsi tek defterde: `ders.ipynb`. Hücreleri her zaman yukarıdan aşağı çalıştır; defteri
yeni açtıysan (ya da çekirdeği yeniden başlattıysan) Adım 1'den başla. Isınmadaki
küçük `kayitlar` listesi Adım 1'de gerçek veriyle değişiyor; Adım 1'i atlarsan Adım 2
üç satırlık ısınma listesiyle çalışmaya kalkar ve `KeyError: 'r'` verir (o listede `r` yok).

Derste kendi başına çalışacağın defter: `alistirma.ipynb`. Önce aynı klasörde yeni bir
adla kopyala, kopyada çalış; böylece `git pull` çakışmaz. İki bölümü var:

- **Bozuk kodlar:** beş kısa hücre. Hepsi hata mesajı vermeden **yanlış sonuç** yazıyor
  (asıl tehlikeli hatalar da bunlar); üstlerinde ne yazmaları gerektiği yazıyor.
- **Kendi başına:** `BOSLUK` yazan yerleri doldurduğun sorular. Doldurmadığın boşluk
  `NameError: name 'BOSLUK' is not defined` verir; o yüzden soruları sırayla çöz. Her
  sorunun üstünde doğru çıktı yazılı.

Alıştırma defteri dosya okumaz; ilk iki hücresi altı renklik küçük bir veriyi ve onun
`X`, `y` listelerini kendisi kurar. Önce o iki hücreyi çalıştır.

---

## Sık karşılaşılan hatalar ve mesajlarını okumak

Python bir hata verdiğinde en alttaki satır en önemlisidir: önce hatanın **türü**
(`ValueError`, `FileNotFoundError`), iki noktadan sonra da **açıklaması** gelir.
Üstteki satırlar hatanın kodun neresinde çıktığını gösterir.

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `NameError: name 'kayitlar' is not defined` | Bir hücreyi atladın ya da defteri yeni açtın | Hücreleri baştan, sırayla çalıştır |
| `ModuleNotFoundError: No module named 'sklearn'` | Defter `.venv` dışındaki bir çekirdekle çalışıyor | Sağ üstten çekirdek olarak `.venv`'i seç; yoksa `gita3111` klasöründe `uv sync` |
| `FileNotFoundError: [Errno 2] No such file or directory: 'veri/renkler-etiketli.csv'` | Defterin kopyası konu klasörünün dışında | Defter `03-makine-ogrenmesi` klasöründe durmalı; kopyayı oraya al |
| `KeyError: 'r'` | Adım 1 atlandı (ısınmadaki küçük liste duruyor) ya da veri dosyası eski (sütunlar `hex,ad,ogrenci,etiket`) | Adım 1'i çalıştır; yine olursa `gita3111` klasöründe `git pull` |
| `ValueError: dtype='numeric' is not compatible with arrays of bytes/strings.` | X'in içine metin girmiş: `int(...)` unutuldu ya da etiket X'e karıştı | `r = int(kayit["r"])`; X'te yalnızca sayılar olmalı |
| `ValueError: Found input variables with inconsistent numbers of samples: [200, 240]` | X ve y farklı uzunlukta | İkisini aynı döngüde doldur |
| `NotFittedError: This KNeighborsClassifier instance is not fitted yet.` | `fit` çağrılmadan `predict` ya da `score` | Önce `model.fit(X_egitim, y_egitim)` |
| `ValueError: Expected 2D array, got 1D array instead` | `predict`'e tek renk köşeli parantez olmadan verildi | `model.predict([renk])` |
| `ValueError: Expected n_neighbors <= n_samples_fit, but n_neighbors = 5, n_samples_fit = 2` | Komşu sayısı eğitim örneği sayısından büyük | Daha çok örnek ver ya da `n_neighbors`'ı küçült |
| Grafik görünmüyor | Hücrenin son satırı `plt.show()` değil ya da `matplotlib` hücresi atlandı | Adım 6'nın `import matplotlib.pyplot as plt` hücresini çalıştır, `plt.show()` ekle |
| `'230' + '57'` → `'23057'` | Metinler toplanmaz, yan yana yapıştırılır | Önce `int(...)` ile sayıya çevir |
| Doğruluk %100 değil | Normal: sınıfın kendisi de anlaşamadı | Tavanla kıyasla; %100 çıksaydı asıl o şüpheli olurdu |
| Doğruluk %100 ya da ona çok yakın | Test verisi bir yoldan sızmış | Eğitimde mi ölçtün? Etiket X'e mi karıştı? |
| Model hep aynı etiketi diyor | Bir etiket ezici çoğunlukta (veri dengesiz) | Bu bir sonuçtur: model çoğunluğu tekrarlıyor |

Son dört satır hata mesajı vermeyen durumlar. Bunlarda Python sana yardım etmez; sonucu
kıyas noktalarıyla (kör tahmin, tavan) karşılaştırmak senin işin.

---

## Kendini dene

Cevaplar notun en sonunda. Önce kendin düşün.

1. Veride bir renk 12 kez geçiyor ve 12 kişinin 12'si de aynı etiketi vermiş.
   Sadece bu renkten oluşan bir test verisinde modelin doğruluğu en fazla kaç olabilir?
   Peki 6 kişi "sakin", 6 kişi "ciddi" demişse?
2. Arkadaşın "modelim %98 doğru" diyor. Kör tahmin %45, tavan %80. Ona ilk soracağın
   soru ne olmalı?
3. Adım 3'teki `train_test_split(...)` satırında `random_state=42`'yi silersen ne
   değişir? Kod çalışmaya devam eder mi?
4. Adım 3'te `X_egitim, X_test, y_egitim, y_test` yerine yanlışlıkla
   `X_egitim, y_egitim, X_test, y_test` yazdın. Adım 4'ün hücresi hata verir mi? Ne olur?
5. k=1 ile k=5 arasındaki farkı "arkadaşa sormak" benzetmesiyle bir cümlede anlat.
6. Adım 7'de bej için model "enerjik" dedi. Bu cevaba neden fazla güvenmemelisin?
7. Adım 8'deki "hiç görmediği renkler" doğruluğu (0.6), Adım 4'teki doğruluktan (0.77)
   düşük. Hangisi yanlış?
8. Etiketleme ödevini yeniden tasarlasan, kafe paleti hakkında daha güvenilir bir model
   elde etmek için neyi değiştirirdin?

---

## Bu konuda öğrendiklerin

- **Kural yazmak ile öğretmek farklıdır.** Kural, yazanın sezgisini taşır; model,
  örnekleri etiketleyenlerin ortak sezgisini. Bizim veride sınıfın "enerjik" kavramı,
  tek satırlık bir kuralın yakalayabileceğinden çok daha genişti.
- **Öznitelik ve etiket.** Modelin baktığı şey X, tahmin etmesi gereken şey y. Aynı
  sırada olmak zorundalar. Modelin neye **bakmadığı** da (rengin adı, bağlamı,
  komşu renkler) sonuçları belirler.
- **Eğitim ve test ayrımı.** Model test verisini hiç görmez. Görürse ölçtüğün şey
  öğrenme değil ezber olur. Sızıntı çoğu zaman kazara olur ve hata mesajı vermez.
- **Doğruluk iki kıyasla anlam kazanır.** Alttan kör tahmin, üstten tavan. Bizim model
  kör tahmini açık farkla geçti ve tavana iki cevap yaklaştı.
- **Tek sayıya güvenme.** Farklı bölmeler farklı sonuç verir; küçük test verisinde
  tek bir satır bile sonucu oynatır.
- **Yanılgılar veriden haber verir.** Modelin yanılgılarının çoğu sınıfın azınlık
  görüşleriydi; model bir "çoğunluk sesi" üretir.
- **"Test" hangi soruyu soruyor?** Bilinen renklerde 0.77, hiç görülmemiş renklerde
  0.6. İkisi de doğru, ama farklı soruların cevabı.
- **Benzerlik, temsile bağlıdır.** RGB'de yakın olan iki renk (gri mavi ile gül kurusu)
  gözümüze hiç benzemeyebilir. Bu, Konu 4'ün başlangıç noktası.

## Bu konunun tek cümlesi

> Model kural almaz, örnek alır; ne kadar öğrendiğini ancak hiç görmediği örneklerde
> ölçebilirsin ve yanıldığı yerler çoğu zaman verinin kendisi hakkında konuşur.

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **Makine öğrenmesi** | Kuralı elle yazmak yerine, örneklerden kural çıkaran programlar |
| **Model** | Örneklerden öğrendiği şeyi saklayan ve yeni örneklere cevap veren nesne; bizde `model` |
| **Öznitelik (X)** | Modelin baktığı bilgi; bizde bir rengin üç RGB sayısı |
| **Etiket (y)** | Modelin tahmin etmesi gereken cevap; bizde "enerjik", "sakin" ya da "ciddi" |
| **Sınıflandırma** | Her örneğe önceden belli birkaç etiketten birini verme işi |
| **Eğitim verisi** | Modelin öğrenirken baktığı örnekler |
| **Test verisi** | Modelin hiç görmediği, ölçüm için ayrılmış örnekler |
| **Eğitmek (`fit`)** | Modele örnekleri verip öğrenmesini istemek |
| **Tahmin (`predict`)** | Eğitilmiş modelden yeni bir renk (ya da renk listesi) için cevap istemek |
| **Doğruluk (`score`)** | Test örneklerinin kaçta kaçını doğru bildiği; 0 ile 1 arası |
| **Kör tahmin** | Hiç düşünmeden hep en sık etiketi söylemek; alttan kıyas noktası |
| **Tavan** | Veri içindeki anlaşmazlık yüzünden hiçbir modelin aşamayacağı doğruluk |
| **k-NN (en yakın komşular)** | Yeni örneğe en çok benzeyen k örneğe bakıp çoğunluğun cevabını veren model |
| **Ezberleme** | Modelin genel eğilimi değil tek tek örnekleri tekrarlaması; görülmemiş örneklerde kötü sonuç verir |
| **Sızıntı** | Test verisinin ya da cevabın bir yoldan eğitime karışması; sonucu sahte biçimde iyileştirir |
| **`random_state`** | Rastgele karıştırmanın her seferinde aynı çıkmasını sağlayan sayı |
| **RGB** | Bir rengi kırmızı, yeşil, mavi miktarıyla (0–255) üç sayı olarak yazma biçimi; renk seçicideki R, G, B kutuları |
| **Renk kodu (hex)** | Aynı üç sayının kısaltılmış yazılışı: `#E63946` = R 230, G 57, B 70 |
| **Temsil** | Bir şeyin (renk, kelime) sayılara nasıl çevrildiği; "benzerlik" bu seçime bağlıdır |

## Ödev

`odevler/odev3.md` (puansız): Adım 6'nın çıktısından modelin eğitim verisinin
**yarısıyla** (90 örnek) ve **tamamıyla** (180 örnek) eğitildiğindeki iki doğruluğunu
al, öğrenme eğrisi grafiğini getir, farkı tek cümleyle yorumla.

## Sonraki konu

**Konu 4 — Temsil ve gömme vektörleri.** Bu konuda rengi üç sayıya çevirdik:
`[230, 57, 70]`. Konu 4'te **kelimeleri** sayıya çevireceğiz; bu kez üç değil, yüzlerce
sayıya. Bu konudaki "en yakın komşu" fikri orada da devam ediyor: iki kelime
birbirine benziyor mu, sayılarına bakarak söyleyeceğiz. Ve Adım 8'deki soru orada
daha da önemli hâle geliyor: sayılar, bizim "benzer" dediğimiz şeyi yakalıyor mu?

---

## Kendini dene — cevaplar

1. Herkes aynı etiketi verdiyse en fazla **1.0** (12'de 12). 6'ya 6 bölünmüşse en fazla
   **0.5**: model tek bir cevap verebilir, hangisini seçerse seçsin öbür altı kişide
   yanılır. Tavan fikri budur.
2. "Nerede ölçtün?" Tavan %80 iken %98 doğruluk, aynı renklere verilen farklı
   etiketleri de bildiği anlamına gelir; bu imkânsız. Büyük ihtimalle eğitim verisinde
   ölçülmüş ya da etiket özniteliğe karışmış.
3. Kod çalışmaya devam eder, ama her çalıştırmada bölme farklı olur, doğruluk da
   değişir (yedek veride 0.65 ile 0.78 arası gibi). Sonuçları başkalarıyla ya da kendi
   önceki denemenle kıyaslayamazsın.
4. Evet, `fit` satırında hata verir: `y_egitim` adlı değişkene aslında test öznitelikleri
   (60 satır) düşer, `X_egitim` ise 180 satır kalır:
   `ValueError: Found input variables with inconsistent numbers of samples: [180, 60]`.
   Alıştırma defterindeki 3. bozuk kodda ise veri ikiye eşit bölündüğü için uzunluklar
   tutuyor ve hiçbir hata çıkmıyor; yanlışlığı ancak `y_egitim`'in içine bakınca
   görürsün. Sıra her zaman: eğitim X, test X, eğitim y, test y.
5. k=1 tek bir arkadaşa sormak, o azınlıktaysa yanılırsın; k=5 beş arkadaşa sorup
   çoğunluğa uymak, tek kişinin farklı görüşü seni yanıltmaz.
6. Çünkü cevabı bej hakkında bir şey bilen biri değil, en yakın bildiği renk olan
   kremi etiketleyenler veriyor ve krem sınıfın en çok tartıştığı renk (5'e 5).
   Model 20 rengin dışını bilmiyor.
7. İkisi de yanlış değil; farklı soruların cevabı. 0.77 "bilinen bir renk için başka
   birinin etiketini tahmin etme" başarısı, 0.6 "hiç görülmemiş bir renge etiket
   verme" başarısı. Yeni renkler hakkında karar vereceksen 0.6'ya bakmalısın.
8. Birkaç iyi cevap: etiketleme listesine kafede kullanılabilecek tonları (bejler,
   kahveler, yeşillerin açık tonları) eklemek; rengi tek başına değil bir mekân
   görselinin içinde göstermek; etiketleyenlere kafenin kullanıcılarına benzeyen
   kişileri de katmak. Hepsinin ortak noktası: modelin kalitesi, verinin nasıl
   toplandığıyla başlıyor.
