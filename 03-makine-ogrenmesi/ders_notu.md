# Konu 3 — Makine Öğrenmesi Nedir? (matematiksiz)

Bu not konunun özetidir; ısınmadan sonra slaytlarla **aynı sırada** ilerler. Derste
kaçırdığın bir yer olursa buradan oku, sonra ilgili örnek dosyayı çalıştır. Notun
içindeki kod parçaları birbirinin devamıdır: hepsini sırayla tek bir dosyaya
yapıştırırsan baştan sona çalışan bir program elde edersin.

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
renkleri gösteren bir görsel (`yanilgilar.png`) ve kafe paleti için modelden alınmış
bir "ikinci görüş".

**Kurulum (dersten önce):** `uv add -r 03-makine-ogrenmesi/requirements.txt` — indirme birkaç dakika sürebilir.
Dosyada kütüphanenin tam adı yazılı: `scikit-learn`. Kodda ise `sklearn` diye çağrılır;
elle kurarken `uv add sklearn` yazarsan yanlış pakete gidersin.

> **Bu nottaki sayılar hakkında.** Buradaki bütün sayılar **yedek veri setinden**:
> 12 kişinin 20 rengi etiketlediği, 240 satırlık hazır bir dosya. Sınıfın kendi
> verisiyle sayılar farklı çıkacak; derste gördüğün sayılar esas. Nottaki yorumları
> kendi sayılarına uygulamayı dene: "bizde de böyle mi?"

---

## Isınma: CSV satırını sözlüğe çevirmek

Bu konuda tablo hâlinde veriyle çalışıyoruz. `00_isinma.py` iki küçük tamir içeriyor:

1. **Satırı sözlüğe çevir.** CSV'nin ilk satırındaki sütun adları anahtar olur,
   satırdaki değerler değer olur:
   `["#E63946", "kırmızı", "enerjik"]` → `{"hex": "#E63946", "ad": "kırmızı", "etiket": "enerjik"}`.
2. **Etiketleri say.** Konu 1'in sayacı; ama sayılan şey kaydın kendisi değil,
   `kayit["etiket"]`.

İkinci tamirdeki hatayı düzeltmeden çalıştırırsan Python şunu söyler:

```text
TypeError: unhashable type: 'dict'
```

Okuması: "sözlük (dict) başka bir sözlüğün anahtarı olamaz." Sayaca kaydın tamamını
koymaya çalışıyorsun; oysa saymak istediğin şey kaydın içindeki etiket.

---

## Kural yazmak ile öğretmek

Bir rengin "enerjik" olup olmadığını kodla söyleyebilirsin. Aşağıda `kirmizi` ve
`yesil`, rengin içindeki kırmızı ve yeşil miktarı (0 ile 255 arası bir sayı); nasıl
bulunduğunu Adım 2'de göreceğiz:

```python
if kirmizi > 200 and yesil < 100:
    return "enerjik"
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

VERI = "03-makine-ogrenmesi/veri/renkler-etiketli.csv"

with open(VERI, encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

print("Toplam satır:", len(kayitlar))
print("İlk kayıt   :", kayitlar[0])
```

`csv.DictReader` her satırı bir **sözlüğe** çevirir (ısınmada elle yaptığımız iş).
Dosyada dört sütun var: `hex`, `ad`, `ogrenci`, `etiket`. Yani her kayıt tanıdık bir
sözlük: `kayit["hex"]`, `kayit["etiket"]`. Her satır **bir öğrencinin bir renge
verdiği etiket**. 12 öğrenci × 20 renk = 240 satır. Aynı renk dosyada 12 kez geçiyor,
her seferinde başka bir öğrencinin gözünden.

Bu yapıyı aklında tut; bu konunun en ilginç bulguları bu "12 kez" gerçeğinden çıkıyor.

### Etiket dağılımı

```python
sayac = {}
for kayit in kayitlar:
    sayac[kayit["etiket"]] = sayac.get(kayit["etiket"], 0) + 1

for etiket in sorted(sayac, key=sayac.get, reverse=True):
    print(sayac[etiket], etiket)
```

Konu 1'in kelime sayacı; sadece kelime yerine etiket sayıyoruz. Yedek veride sonuç:
100 enerjik, 78 sakin, 62 ciddi.

Neden bakıyoruz? Bir etiket ezici çoğunluktaysa (diyelim 240'ın 220'si "enerjik")
model tembelleşir: hep onu der ve yine de çoğu zaman haklı çıkar. Böyle bir modelin
"yüksek doğruluğu" hiçbir şey öğrenmediğini gizler. Bizim dağılım o kadar dengesiz
değil, ama "enerjik" biraz önde. Bu bilgiye Adım 4'te "kör tahmin" hesaplarken
ihtiyacımız olacak.

### Sınıf anlaşabilmiş mi?

Yedek veride 20 rengin 20'sinde de aynı renge farklı etiketler verilmiş. Bu bir hata
değil; gerçek veri böyledir, insanlar aynı şeye farklı etiket verir. Ama "anlaşamamak"
her renkte aynı ölçüde değil. Her renk için "en çok verilen etiketi kaç kişi seçmiş?"
sorusunu soralım:

```python
renk_sayaclari = {}
for kayit in kayitlar:
    ad = kayit["ad"]
    if ad not in renk_sayaclari:
        renk_sayaclari[ad] = {}
    renk_sayaclari[ad][kayit["etiket"]] = renk_sayaclari[ad].get(kayit["etiket"], 0) + 1

uzlasma = {}
for ad in renk_sayaclari:
    uzlasma[ad] = max(renk_sayaclari[ad].values())

print("En çok tartışılan renkler:")
for ad in sorted(uzlasma, key=uzlasma.get)[:3]:
    print(f"  {ad:<12} {uzlasma[ad]}/12  {renk_sayaclari[ad]}")

print("En çok anlaşılan renkler:")
for ad in sorted(uzlasma, key=uzlasma.get, reverse=True)[:3]:
    print(f"  {ad:<12} {uzlasma[ad]}/12  {renk_sayaclari[ad]}")
```

Burada sözlüğün içinde sözlük var: `renk_sayaclari["krem"]` kendi başına bir sayaç.
Konu 1'deki sayacın aynısı, sadece her renk için ayrı bir tane.

Yedek veride tablo şöyle:

| Renk | En çok verilen etiket | Kaç kişi | Dağılım |
|---|---|---|---|
| krem | (berabere) | 5/12 | 5 enerjik, 5 sakin, 2 ciddi |
| koyu yeşil | ciddi | 6/12 | 6 ciddi, 4 sakin, 2 enerjik |
| hardal | enerjik | 7/12 | 7 enerjik, 3 sakin, 2 ciddi |
| kırık beyaz | sakin | 11/12 | 11 sakin, 1 enerjik |
| bordo | enerjik | 11/12 | 11 enerjik, 1 ciddi |

**Tasarım açısından okuması:** kırık beyaz ile krem ekranda neredeyse aynı renk.
Ama sınıf kırık beyaza neredeyse oybirliğiyle "sakin" derken, krem tam ortadan
ikiye bölünmüş. Aradaki tek fark kremdeki hafif sarılık. Demek ki küçük bir sıcaklık
kayması, rengin hissettirdiği şeyi değiştirebiliyor; kafe paleti için bir "sakin
beyaz" seçerken bu fark önemli. Bu iki rengi Adım 8'de tekrar göreceğiz.

### Anlaşmazlığın koyduğu tavan

Bu tablodan önemli bir sonuç çıkıyor. Modelin göreceği tek şey rengin kendisi. Aynı
renge 12 kişi farklı cevaplar verdiyse model, o renk için **tek bir** cevap
verebilir. En iyi ihtimalle çoğunluğun cevabını verir ve azınlıktakilerin hepsinde
yanılır. O hâlde hiçbir model şundan iyi olamaz:

```python
tavan = sum(uzlasma.values()) / len(kayitlar)
print(f"Sadece renge bakan bir modelin çıkabileceği en yüksek doğruluk: {tavan:.2f}")
```

Yedek veride bu sayı **0.74**. Yani mükemmel bir model bile her dört cevaptan birini
"yanlış" bilecek. Bu yanlışlar modelin kusuru değil; sınıfın kendi içindeki görüş
ayrılığı. `sum(...)` bir listedeki ya da sözlük değerlerindeki sayıları toplar.

## Adım 2 — Rengi sayıya çevir

Model "kırmızı" kelimesini anlamaz, sayı ister. Renk kodu (`#E63946`) üç sayının
yan yana yazılmış hâlidir: kırmızı, yeşil, mavi miktarı (RGB).

```python
def hex_to_rgb(hex_kod):
    hex_kod = hex_kod.lstrip("#")          # "#E63946" → "E63946"
    kirmizi = int(hex_kod[0:2], 16)        # "E6" → 230
    yesil = int(hex_kod[2:4], 16)
    mavi = int(hex_kod[4:6], 16)
    return (kirmizi, yesil, mavi)


print(hex_to_rgb("#E63946"))   # (230, 57, 70)
```

- `.lstrip("#")` baştaki `#` işaretini siler.
- `hex_kod[0:2]` Konu 1'in dilimlemesi: 0. karakterden başla, 2.'den önce dur, yani
  ilk iki karakter. `[2:4]` sonraki iki, `[4:6]` son iki.
- `int("E6", 16)`: renk kodları onaltılık (16 tabanında) yazılır; `int` onu bildiğimiz
  sayıya çevirir.
- Sonuç `hex_to_rgb("#E63946")` → `(230, 57, 70)`. Parantez içindeki bu üçlüye
  **demet** (tuple) denir: liste gibi sıralıdır ama değiştirilemez.

`16`'yı unutursan Python kodu onluk sayı sanar ve `E` harfinde takılır:

```text
ValueError: invalid literal for int() with base 10: 'E6'
```

Okuması: "`'E6'` metnini 10 tabanında (base 10) bir sayı olarak okuyamadım."
Mesajın sonundaki `base 10` sana eksik olanı söylüyor.

### Üç sayıyı okumayı öğren

Model rengi yalnızca bu üç sayı olarak görecek. Senin de bu sayılara bakıp rengi
kabaca tahmin edebilmen, modelin neyi görüp neyi göremediğini anlamanı kolaylaştırır:

| Renk | RGB | Nasıl okunur |
|---|---|---|
| lacivert `#1D3557` | (29, 53, 87) | Üçü de küçük: koyu. Mavi en büyük: mavimsi |
| kırık beyaz `#F1FAEE` | (241, 250, 238) | Üçü de büyük ve birbirine yakın: açık, neredeyse renksiz |
| krem `#FEFAE0` | (254, 250, 224) | Kırık beyaza çok yakın, ama mavi biraz düşük: hafif sarımsı |
| bordo `#9A031E` | (154, 3, 30) | Kırmızı baskın, öbür ikisi neredeyse sıfır: koyu ama doygun |
| gri mavi `#8D99AE` | (141, 153, 174) | Üçü birbirine yakın, mavi biraz önde: grimsi mavi |

Kısaca: üç sayı da küçükse renk koyudur, üçü de büyükse açıktır; üçü birbirine
yakınsa renk grimsidir, biri öbürlerinden çok büyükse renk o yöne doygundur.

### Başta yazdığımız kural ne kadar iş görüyor?

Artık kuralı gerçek veride sınayabiliriz:

```python
yakalanan = 0
enerjik_sayisi = 0
for kayit in kayitlar:
    kirmizi, yesil, mavi = hex_to_rgb(kayit["hex"])
    if kayit["etiket"] == "enerjik":
        enerjik_sayisi = enerjik_sayisi + 1
        if kirmizi > 200 and yesil < 100:
            yakalanan = yakalanan + 1

print(f"Sınıfın {enerjik_sayisi} 'enerjik' etiketinden kuralın yakaladığı: {yakalanan}")
```

`kirmizi, yesil, mavi = hex_to_rgb(...)`: fonksiyon üç sayı döndürüyor, Python da
sırayla üç değişkene dağıtıyor.

Yedek veride sonuç: 100 "enerjik" etiketinden kural yalnızca **8**'ini yakalıyor.
Kural 20 renkten sadece birini (kırmızıyı) tanıyor. Bordo, şeftali, somon, tarçın ve
bal da sınıfın çoğunluğuna göre enerjik; ama hiçbiri "kırmızı 200'den büyük, yeşil
100'den küçük" şartına uymuyor. Sınıfın "enerjik" kavramı, kuralı yazan kişininkinden
çok daha geniş: canlı renklerle birlikte **sıcak** tonların neredeyse hepsini içeriyor.
İşte örnekten öğrenmenin gücü burada: kimsenin aklına gelmeyen bu genişliği veri
kendisi taşıyor.

## Öznitelik ve etiket: X ve y

```python
X = []
y = []
for kayit in kayitlar:
    X.append(hex_to_rgb(kayit["hex"]))
    y.append(kayit["etiket"])

print(X[0], "->", y[0])
```

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
  `07_bozuk_kodlar.py`'nin 2. sorusu tam bu hata.

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

print("Eğitim örneği:", len(X_egitim))
print("Test örneği  :", len(X_test))
```

- Soldaki **dört değişken tek satırda** dolar: fonksiyon dört şey döndürür, Python
  sırayla dağıtır (Konu 2'deki `ad, _, deger = satir.partition("=")` gibi). Sıra
  önemli; karıştırma. Sıra her zaman: eğitim X, test X, eğitim y, test y.
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

1. **Aynı veride eğitip ölçmek.** En açık olanı. `07_bozuk_kodlar.py`'nin 5. sorusu.
2. **Cevabı özniteliğin içine koymak.** Örneğin X'e renk kodunun yanına etiketi de
   eklemek. Model cevabı sorudan okur, doğruluk %100'e fırlar. `07`'nin 3. sorusu.
3. **Test sonucuna bakıp ayar yapmak, sonra yine aynı testte ölçmek.** Diyelim komşu
   sayısını 5'ten 9'a çıkardın, testte doğruluk arttı, 9'da karar kıldın. Bunu elli
   kez yaparsan test verisine göre ayar çekmiş olursun; test artık "görülmemiş" değildir.

Üçünün ortak sonucu: **sayı gerçekte olduğundan iyi görünür**. Bu, kötü bir sayıdan
daha tehlikelidir, çünkü sana yanlış bir güven verir. Bir tasarım müşterisine "bu
model renkleri %98 doğru etiketliyor" dediğini, sonra yeni renklerde modelin yazı
tura gibi davrandığını düşün.

## Adım 4 — Model: en yakın komşular

Kullandığımız modelin adı **k-NN** (k en yakın komşu). Mantığı tek cümle:

> Bu renge en çok benzeyen 5 rengi bul; onlar ne dediyse onu de.

Buradaki **k** kaç komşuya bakılacağı; bizde 5. Formül yok. "Benzemek" burada üç RGB
sayısının birbirine yakın olması demek. Komşular farklı şeyler diyorsa çoğunluk kazanır.

**Elle bir örnek.** Model eğitim verisinde hiç olmayan buz mavisi `#CFE3F2`
(207, 227, 242) rengini soruyor olsun. Üç sayının hepsi büyük ve birbirine yakın:
açık, hafif mavimsi bir renk. Eğitim verisindeki renklerden buna en yakın olanı kırık
beyaz (241, 250, 238). Kırık beyaz dosyada 12 kez geçtiği için beş en yakın komşunun
beşi de kırık beyaz etiketleri çıkar. Sınıfın 11 kişisi kırık beyaza "sakin" dediği
için bu beşin çoğunluğu da "sakin"dir; model de "sakin" der.

Bu örnek bizim veri hakkında önemli bir şey gösteriyor: her renk dosyada 12 kez
geçtiği için, modelin "5 komşusu" çoğu zaman **aynı rengin 5 ayrı etiketi**. Yani
bizim modelimiz pratikte şunu yapıyor: "bu renge en çok benzeyen renk hangisiyse,
onu etiketleyen arkadaşlarından beşine sor, çoğunluk ne dediyse onu de." Adım 7'de
bunu kendi gözünle göreceksin.

```python
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=5)   # kur: kaç komşuya bakacak?
model.fit(X_egitim, y_egitim)                 # öğren: bu örneklere bak
dogruluk = model.score(X_test, y_test)        # ölç: görmediklerinin kaçını bildin?
print(f"Test doğruluğu: {dogruluk:.2f}")
```

İlk satır modeli **oluşturur**. `fit` ve `score` ise `metin.split()` ya da
`sayac.get()` gibi, bir şeyin arkasına nokta koyup verilen komutlar; yeni olan tek şey
bu kez o şeyin bir model olması. Bir komut daha var, `predict`: "şu yeni örnek sence
hangisi?" Onu Adım 5'te kullanıyoruz.

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

`dogruluk` 0 ile 1 arası bir sayı: 0.77, test renklerinin %77'sini bildi demek.
Doğruluk tek başına anlamsız; iki kıyas noktası gerekir.

**Alttan kıyas — kör tahmin:** hiç düşünmeden hep eğitim verisindeki en sık etiketi
deseydik test verisinde kaçını bilirdik?

```python
sayac = {}
for etiket in y_egitim:
    sayac[etiket] = sayac.get(etiket, 0) + 1
en_sik = sorted(sayac, key=sayac.get, reverse=True)[0]

kor_tahmin = y_test.count(en_sik) / len(y_test)
print(f"Hep '{en_sik}' deseydik: {kor_tahmin:.2f}")
```

**Üstten kıyas — tavan:** Adım 1'de gördük; sınıf anlaşamadığı için sadece renge bakan
hiçbir model belli bir sayıyı geçemez. Yedek verinin bu 60 test satırında o tavan
0.78 (60 satırdan 47'si).

Üç sayıyı yan yana koyunca tablo netleşiyor:

| | Doğruluk | Ne anlama geliyor |
|---|---|---|
| Kör tahmin (hep "enerjik") | 0.45 | Hiç düşünmeden alınabilecek puan |
| Bizim model | 0.77 | 60 test satırından 46'sı |
| Tavan | 0.78 | Sınıfın anlaşmazlığı yüzünden aşılamayacak sınır |

Model kör tahmini açık farkla geçti: gerçekten bir örüntü öğrenmiş. Ve tavana bir
cevap kalmış. Yani bu veriyle modeli daha "akıllı" yapmaya çalışmak boşuna; kalan
yanlışlar modelin değil, **sınıfın görüş ayrılığının** payı. Bu sonucu doğru okumak,
doğruluğu yükseltmeye çalışmaktan daha değerli.

### k'yı değiştirmek: kaç arkadaşa sormalı?

```python
for k in [1, 5, 15, 45]:
    deneme = KNeighborsClassifier(n_neighbors=k)
    deneme.fit(X_egitim, y_egitim)
    print(f"k={k:<3} test doğruluğu: {deneme.score(X_test, y_test):.2f}")
```

Yedek veride: k=1 → 0.70, k=5 → 0.77, k=15 → 0.73, k=45 → 0.72.

- **k=1** "tek bir arkadaşa sor" demek. O arkadaş azınlıktaysa model de azınlığın
  cevabını verir. Tek bir örneğe fazla güvenmek, **ezberlemenin** en basit hâli:
  model genel eğilimi değil, rastgele bir örneği tekrarlıyor.
- **k=5** çoğu renkte aynı rengin beş etiketine bakıyor; çoğunluğu iyi yakalıyor.
- **k=15 ve k=45**: her renk eğitimde yaklaşık 9 kez geçiyor. Komşu sayısı bundan
  büyük olunca model başka renklerin oylarını da saymaya başlıyor; lacivertin
  kararına petrolün etiketleri karışıyor.

Bu deneme bir tuzak da içeriyor: en iyi k'yı test verisine bakarak seçtik. Yukarıda
"test sonucuna bakıp ayar yapmak" dediğimiz şey tam bu. Burada sadece fikri görmek
için yapıyoruz; ciddi bir işte ayar için ayrı bir veri parçası kullanılır.

### Tek sayıya güvenme

`random_state=42` yerine başka sayılar verirsek bölme değişir, doğruluk da değişir:

```python
for tohum in [0, 1, 2, 3, 4]:
    X_e, X_t, y_e, y_t = train_test_split(X, y, test_size=0.25, random_state=tohum)
    deneme = KNeighborsClassifier(n_neighbors=5)
    deneme.fit(X_e, y_e)
    print(f"random_state={tohum}  doğruluk: {deneme.score(X_t, y_t):.2f}")
```

Yedek veride sonuçlar 0.65, 0.67, 0.72, 0.68, 0.78. Aynı model, aynı veri; sadece
hangi 60 satırın teste düştüğü değişiyor. Test verisi küçük olunca tek bir satır bile
sonucu yaklaşık iki puan oynatıyor (1/60 ≈ 0.017). O yüzden "0.77" demek yerine "0.65
ile 0.78 arasında bir yerde" demek daha dürüst. Adım 6'daki grafiğin neden
dalgalandığını anlamak için bu bilgiye ihtiyacın olacak.

### Eğitim verisinde ölçseydik?

```python
print(f"Eğitim verisinde: {model.score(X_egitim, y_egitim):.2f}")
print(f"Test verisinde  : {model.score(X_test, y_test):.2f}")
```

Genelde eğitim verisindeki sayı testtekinden **yüksek** çıkar; model görmüş olduğu
soruları daha iyi bilir. `07_bozuk_kodlar.py`'deki küçük veride bu fark çok açık.
Bizim veride ise şaşırtıcı bir şey oluyor: eğitimde 0.69, testte 0.77. Neden?
Çünkü eğitim verisinde de her renk birden çok kez, farklı etiketlerle geçiyor.
Model bir renk için tek cevap verebildiğinden, eğitimde gördüğü azınlık etiketlerinde
de yanılıyor. Ezber, anlaşmazlığı çözemiyor. Bu, "tavan" fikrinin başka bir
görünüşü. Kural yine değişmez: **doğruluk test verisinde ölçülür.**

## Adım 5 — Yanıldığı yere bak

Doğruluk tek bir sayı; asıl öğretici olan modelin **nerede** yanıldığı.
`model.predict(X_test)` ile her test satırı için tahmin alıp gerçek etiketle
karşılaştırıyoruz. Hangi rengin yanlış gittiğini görmek için renk adlarını da bölmeye
katıyoruz; `train_test_split` kaç liste verirsen hepsini aynı karıştırmayla böler:

```python
adlar = []
for kayit in kayitlar:
    adlar.append(kayit["ad"])

X_egitim, X_test, y_egitim, y_test, ad_egitim, ad_test = train_test_split(
    X, y, adlar, test_size=0.25, random_state=42
)

tahminler = model.predict(X_test)

for i in range(len(y_test)):
    if tahminler[i] != y_test[i]:
        print(f"{ad_test[i]:<14} öğrenci: {y_test[i]:<8} model: {tahminler[i]:<8}"
              f"sınıfın tamamı: {renk_sayaclari[ad_test[i]]}")
```

Aynı `random_state=42` ile böldüğümüz için bölme Adım 3'tekiyle birebir aynı; model
yeniden eğitilmeden kullanılabiliyor. Son sütunda Adım 1'deki `renk_sayaclari`
sözlüğünü kullanıyoruz: her yanlışın yanında o renge sınıfın tamamının ne dediğini
görmek, yanılgıyı okumanın anahtarı.

`predict` her zaman bir **liste** ister, tek renk sorsan bile. `model.predict((230, 57, 70))`
yazarsan uzun bir mesaj alırsın:

```text
ValueError: Expected 2D array, got 1D array instead:
array=[230  57  70].
```

Okuması: "iki boyutlu bir dizi (liste içinde liste) bekliyordum, tek boyutlu geldi."
Çözüm, rengi bir listenin içine koymak: `model.predict([(230, 57, 70)])`. Mesajın
devamındaki `reshape` önerisini görmezden gelebilirsin; o, bu derste kullanmadığımız
bir kütüphanenin yolu.

### Yanılgıları okumak

Yedek veride 60 test satırından 14'ünde model yanılıyor. Hepsine son sütunla birlikte
bakınca iki grup çıkıyor:

**Birinci grup (14 yanılgının 12'si): öğrenci azınlıkta.** Örneğin bir öğrenci
şeftaliye "ciddi" demiş; sınıfın 10 kişisi "enerjik" demiş, model de "enerjik" diyor.
Bu satır "yanlış" sayılıyor ama model sınıfın ortak görüşünü söylüyor. Bu 12 satırın
yarısında azınlıktaki öğrenci sıcak, toprak tonlu bir renge (şeftali, tarçın, bal,
somon, gül kurusu) "ciddi" demiş. Sınıfın bir kısmı bu tonları ağırbaşlı buluyor;
model bu sesi hiç duyamıyor.

**İkinci grup (2 yanılgı): model sınıfın çoğunluğundan da ayrılmış.** Orta mavi için
model "ciddi" diyor, oysa sınıfın 8 kişisi "sakin" demiş. Sebep Adım 4'teki gözlem:
model orta mavinin 12 etiketinden yalnızca 5'ine bakabiliyor ve rastlantıyla o beşin
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

`05_yanilgilari_gor.py` aynı yanlışları renk karesi olarak çizer (`yanilgilar.png`);
her karenin üstünde rengin adı ve kodu da yazar. Görsele bakarken kendine şunu sor:
"Ben olsam bu kareye ne derdim, model mi haklı, öğrenci mi?"

## Adım 6 — Veri arttıkça ne oluyor?

`06_veri_miktari.py` modeli eğitim verisinin önce %10'u, sonra %25'i, %50'si, %75'i
ve tamamıyla eğitip her seferinde aynı test verisinde ölçer, sonra sonucu
`veri-miktari.png` grafiğine çizer. Çekirdeği şu döngü:

```python
for oran in [0.1, 0.25, 0.5, 0.75, 1.0]:
    adet = int(len(X_egitim) * oran)
    deneme = KNeighborsClassifier(n_neighbors=5)
    deneme.fit(X_egitim[:adet], y_egitim[:adet])
    print(adet, "örnek ->", round(deneme.score(X_test, y_test), 2))
```

- `int(...)` kesirli sayıyı tam sayıya çevirir: 180 × 0.1 = 18.0 → 18.
- `X_egitim[:adet]` Konu 1'in dilimlemesi: baştan `adet` tane örnek.
- `round(..., 2)` sayıyı virgülden sonra iki basamağa yuvarlar.

Yedek veride sonuç:

| Eğitim örneği | Doğruluk |
|---|---|
| 18 | 0.48 |
| 45 | 0.72 |
| 90 | 0.62 |
| 135 | 0.75 |
| 180 | 0.77 |

Eğri genelde önce hızlı yükselir, sonra düzleşir. **Düzleştiği yer önemli:** oradan
sonra veri eklemek pek işe yaramıyor demektir. Bizim veride düzleşme noktası tavanın
hemen altı: 180 örnekle 0.77'ye, tavana (0.78) bir cevap kalana kadar geldik. Aynı
20 renge daha çok öğrenci etiketi eklemek bu tavanı yükseltmez. Tavanı yükseltmek
için **başka türlü** veri gerekir: daha çok renk ya da rengin kullanıldığı bağlam gibi
yeni bilgiler.

**18 örnekle neden bu kadar kötü?** 18 örnekte 20 rengin ancak 14'ü var; 6 renk hiç yok. Model
görmediği bir rengi sorulduğunda ona en çok benzeyen başka bir rengin etiketlerini
kullanmak zorunda kalıyor. Az veri, "tanıdık renk" sayısını azaltıyor.

**Eğri ortada düşebilir.** Yedek veride 45 örnekten 90 örneğe çıkınca doğruluk
0.72'den 0.62'ye iniyor. Bu bir hata değil; düzeltmeye çalışma. İpucu: 90 örneklik
parçada gri mavi yalnızca bir kez geçiyor ve onu etiketleyen öğrenci azınlıktan
("ciddi" demiş). Model de gri maviyi sorduğunda bu tek etiketin yanına en yakın başka
rengin, gül kurusunun etiketlerini ekliyor. Test verisi de küçük (Adım 4'teki "tek
sayıya güvenme" bölümünü hatırla). Neden olduğunu ödevde kendi verinle düşüneceksin,
Konu 4'ün başında birlikte konuşacağız.

## Adım 7 — Model ne öğrendi? Yeni renklerle yoklamak

Modelin içini açıp "kuralını" okuyamayız. Ama bir tasarımcının kullanıcı testinde
yaptığını yapabiliriz: ona hiç görmediği renkler gösterip cevaplarına bakmak. Bunun
için modeli bu kez **tüm veriyle** eğitiyoruz; ölçüm yapmıyoruz, sadece soru
soruyoruz. Her cevabın yanında `kneighbors` ile modelin hangi komşulara baktığını da
yazdırıyoruz:

```python
tam_model = KNeighborsClassifier(n_neighbors=5)
tam_model.fit(X, y)

for hex_kod in ["#0A1F44", "#4A7FB0", "#CFE3F2", "#E8DCC4", "#A3B18A"]:
    rgb = hex_to_rgb(hex_kod)
    tahmin = tam_model.predict([rgb])[0]
    mesafeler, siralar = tam_model.kneighbors([rgb])
    komsular = set()
    for sira in siralar[0]:
        komsular.add(adlar[sira])
    print(hex_kod, "->", tahmin, " komşusu:", komsular)
```

- `kneighbors` iki şey döndürür: en yakın beş komşunun uzaklıkları ve veri içindeki
  sıra numaraları. Biz uzaklıkları kullanmıyoruz; sıra numarasıyla `adlar` listesinden
  komşunun adını okuyoruz.
- `[0]`: `predict` ve `kneighbors` birden çok renk için çalışacak şekilde tasarlandı,
  cevabı liste olarak verir. Biz tek renk sorduğumuz için ilk elemanı alıyoruz.
- `set()` aynı adı bir kez tutar; beş komşu aynı renkse tek ad görürsün.

`09_modeli_yokla.py` aynı işi üç grup renk için yapar. Yedek verideki bulgular:

**Koyuluk maviyi ciddileştiriyor, kırmızıyı ciddileştirmiyor.** Aynı mavinin koyudan
açığa üç sürümü: çok koyu mavi → ciddi, orta mavi → sakin, buz mavisi → sakin. Aynı
deneyi kırmızıyla yapınca çok koyu kırmızı da, canlı kırmızı da, toz pembe de
"enerjik". Sınıfın gözünde koyuluk tek başına ciddiyet getirmiyor; renk tonu (hue)
koyuluktan güçlü basıyor. Bordoya 12 kişiden 11'inin "enerjik" demesi bunun kaynağı.

**Kafe paleti için ikinci görüş.** Konu 1'deki "sessiz çalışma kafesi" için aday bir
palet:

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

## Adım 8 — Hiç görmediği renkler: dürüst sınav

Adım 3'teki bölmeye geri dönelim. Satırları karıştırıp dörtte birini teste ayırdık;
ama her renk dosyada 12 kez geçtiği için, testteki bir lacivert satırının 9 kardeşi
eğitimde duruyor. Model teste gelmeden lacivertin ne olduğunu başka öğrencilerden
zaten duymuş. Adım 3'teki test aslında şunu ölçüyor: "bilinen bir renk için başka bir
öğrencinin ne diyeceğini tahmin edebiliyor mu?"

Bu kötü bir soru değil. Ama "yeni bir renk gelince model ne der?" sorusunun cevabı
değil. Onu ölçmek için bir rengi **tamamen** dışarıda bırakmak gerekir: model o rengin
hiçbir satırını görmeden eğitilir, sonra o renk sorulur. Bunu 20 rengin her biri için
sırayla yaparız. `10_gorulmemis_renkler.py` tam bunu yapar; çekirdeği şu:

```python
renk_kodlari = {}
for kayit in kayitlar:
    renk_kodlari[kayit["ad"]] = kayit["hex"]

tutan = 0
for disarida in renk_kodlari:
    X_e = []
    y_e = []
    y_t = []
    for kayit in kayitlar:
        if kayit["ad"] == disarida:
            y_t.append(kayit["etiket"])
        else:
            X_e.append(hex_to_rgb(kayit["hex"]))
            y_e.append(kayit["etiket"])
    deneme = KNeighborsClassifier(n_neighbors=5)
    deneme.fit(X_e, y_e)
    tahmin = deneme.predict([hex_to_rgb(renk_kodlari[disarida])])[0]
    tutan = tutan + y_t.count(tahmin)

print(f"Hiç görmediği renklerde doğruluk: {tutan / len(kayitlar):.2f}")
```

`renk_kodlari` her rengin adını koduyla eşleyen küçük bir sözlük; 20 rengi tek tek
gezmek için onu kullanıyoruz. `y_t.count(tahmin)`: dışarıda kalan rengin 12 etiketinden kaçı modelin
tahminiyle aynı, onu sayıyor.

Yedek veride sonuç: **0.60**. Rastgele bölmede 0.77 idi. Aradaki fark "tanıdık renk"
avantajının büyüklüğü. İkisi de doğru sayı, ama farklı soruların cevabı. Bir sonucu
raporlarken **hangi soruyu sorduğunu** da söylemen gerekir.

`10_gorulmemis_renkler.py`'nin çıktısında model 20 rengin 4'ünde sınıfın çoğunluğundan
ayrılıyor. İkisi özellikle öğretici:

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

---

## Adımlar ve dosyalar

| Adım | Ne yaptık | Elimizde ne oluştu | Dosya |
|---|---|---|---|
| 1 | Veriyi okuduk, dağılıma ve anlaşmazlığa baktık | `kayitlar`, `uzlasma`, tavan | `01_veriyi_oku.py` |
| 2 | Sayıya çevirdik | `X`, `y` | `02_ozellik_etiket.py` |
| 3 | İkiye böldük | `X_egitim`, `X_test`, `y_egitim`, `y_test` | `03_egitim_test.py` |
| 4 | Eğittik, ölçtük, kör tahminle kıyasladık | `model`, `dogruluk` | `04_model_egit.py` |
| 5 | Yanılgılara baktık | `yanilgilar.png` | `05_yanilgilari_gor.py` |
| 6 | Veri miktarını değiştirdik | `veri-miktari.png` | `06_veri_miktari.py` |
| 7 | Modeli yeni renklerle yokladık | kafe paleti için ikinci görüş | `09_modeli_yokla.py` |
| 8 | Hiç görmediği renklerde sınadık | dürüst doğruluk | `10_gorulmemis_renkler.py` |

Her dosyayı `gita3111` klasöründen çalıştır: `uv run 03-makine-ogrenmesi/ornekler/01_veriyi_oku.py`.
Görseller (`yanilgilar.png`, `veri-miktari.png`) de oraya kaydedilir.

Derste kendi başına dolduracağın alıştırma: `alistirma/sinif_alistirmasi.py`
(scikit-learn gerekmez).

Ek alıştırma: `07_bozuk_kodlar.py` (beş bozuk kod; bazıları programı çökertir,
bazıları hata mesajı vermeden sessizce yanlış sonuç üretir; asıl tehlikeli olanlar
bunlar). Bonus: `08_kendi_rengin.py` (kendi seçtiğin renkleri modele tahmin ettir).

---

## Sık karşılaşılan hatalar ve mesajlarını okumak

Python bir hata verdiğinde en alttaki satır en önemlisidir: önce hatanın **türü**
(`ValueError`, `FileNotFoundError`), iki noktadan sonra da **açıklaması** gelir.
Üstteki satırlar hatanın kodun neresinde çıktığını gösterir; kendi dosyanın adını
ve satır numarasını orada ararsın.

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `ModuleNotFoundError: No module named 'sklearn'` | Kütüphane kurulu değil | `uv add -r 03-makine-ogrenmesi/requirements.txt` |
| `FileNotFoundError: [Errno 2] No such file or directory: '03-makine-ogrenmesi/veri/renkler-etiketli.csv'` | Komut yanlış klasörden çalıştırıldı | `gita3111` klasöründen çalıştır |
| `ValueError: invalid literal for int() with base 10: 'E6'` | `int(...)` içinde `16` unutuldu | `int(hex_kod[0:2], 16)` |
| `ValueError: Found input variables with inconsistent numbers of samples: [200, 240]` | X ve y farklı uzunlukta | İkisini aynı döngüde doldur |
| `NotFittedError: This KNeighborsClassifier instance is not fitted yet.` | `fit` çağrılmadan `predict` ya da `score` | Önce `model.fit(X_egitim, y_egitim)` |
| `ValueError: Expected 2D array, got 1D array instead` | `predict`'e tek renk liste içine konmadan verildi | `model.predict([rgb])` |
| `ValueError: Expected n_neighbors <= n_samples_fit, but n_neighbors = 5, n_samples_fit = 2` | Komşu sayısı eğitim örneği sayısından büyük | Daha çok örnek ver ya da `n_neighbors`'ı küçült |
| `ValueError: dtype='numeric' is not compatible with arrays of bytes/strings.` | X'in içine metin (örneğin etiket) karışmış | X'te yalnızca sayılar olmalı |
| Doğruluk %100 değil | Normal: sınıfın kendisi de anlaşamadı | Tavanla kıyasla; %100 çıksaydı asıl o şüpheli olurdu |
| Doğruluk %100 ya da ona çok yakın | Test verisi bir yoldan sızmış | Eğitimde mi ölçtün? Etiket X'e mi karıştı? |
| Model hep aynı etiketi diyor | Bir etiket ezici çoğunlukta (veri dengesiz) | Bu bir sonuçtur: model çoğunluğu tekrarlıyor |

Son üç satır hata mesajı vermeyen durumlar. Bunlarda Python sana yardım etmez; sonucu
kıyas noktalarıyla (kör tahmin, tavan) karşılaştırmak senin işin.

---

## Kendini dene

Cevaplar notun en sonunda. Önce kendin düşün.

1. Veride bir renk 12 kez geçiyor ve 12 kişinin 12'si de aynı etiketi vermiş.
   Sadece bu renkten oluşan bir test verisinde modelin doğruluğu en fazla kaç olabilir?
   Peki 6 kişi "sakin", 6 kişi "ciddi" demişse?
2. Arkadaşın "modelim %98 doğru" diyor. Kör tahmin %45, tavan %78. Ona ilk soracağın
   soru ne olmalı?
3. `train_test_split(X, y, test_size=0.25, random_state=42)` satırında
   `random_state`'i silersen ne değişir? Kod çalışmaya devam eder mi?
4. `X_egitim, X_test, y_egitim, y_test` yerine yanlışlıkla
   `X_egitim, y_egitim, X_test, y_test` yazdın. Program hata verir mi? Ne olur?
5. k=1 ile k=5 arasındaki farkı "arkadaşa sormak" benzetmesiyle bir cümlede anlat.
6. Adım 7'de bej için model "enerjik" dedi. Bu cevaba neden fazla güvenmemelisin?
7. Adım 8'deki "hiç görmediği renkler" doğruluğu (0.60), Adım 4'teki doğruluktan (0.77)
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
  kör tahmini açık farkla geçti ve tavana bir cevap yaklaştı.
- **Tek sayıya güvenme.** Farklı bölmeler farklı sonuç verir; küçük test verisinde
  tek bir satır bile sonucu oynatır.
- **Yanılgılar veriden haber verir.** Modelin yanılgılarının çoğu sınıfın azınlık
  görüşleriydi; model bir "çoğunluk sesi" üretir.
- **"Test" hangi soruyu soruyor?** Bilinen renklerde 0.77, hiç görülmemiş renklerde
  0.60. İkisi de doğru, ama farklı soruların cevabı.
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
| **Tahmin (`predict`)** | Eğitilmiş modelden yeni bir örnek için cevap istemek |
| **Doğruluk (`score`)** | Test örneklerinin kaçta kaçını doğru bildiği; 0 ile 1 arası |
| **Kör tahmin** | Hiç düşünmeden hep en sık etiketi söylemek; alttan kıyas noktası |
| **Tavan** | Veri içindeki anlaşmazlık yüzünden hiçbir modelin aşamayacağı doğruluk |
| **k-NN (en yakın komşular)** | Yeni örneğe en çok benzeyen k örneğe bakıp çoğunluğun cevabını veren model |
| **Ezberleme** | Modelin genel eğilimi değil tek tek örnekleri tekrarlaması; görülmemiş örneklerde kötü sonuç verir |
| **Sızıntı** | Test verisinin ya da cevabın bir yoldan eğitime karışması; sonucu sahte biçimde iyileştirir |
| **`random_state`** | Rastgele karıştırmanın her seferinde aynı çıkmasını sağlayan sayı |
| **RGB** | Bir rengi kırmızı, yeşil, mavi miktarıyla (0–255) üç sayı olarak yazma biçimi |
| **Demet (tuple)** | Liste gibi sıralı ama değiştirilemeyen dizi; `(230, 57, 70)` |
| **Temsil** | Bir şeyin (renk, kelime) sayılara nasıl çevrildiği; "benzerlik" bu seçime bağlıdır |

## Ödev

`odevler/odev3.md` (puansız): önce `06_veri_miktari.py` dosyasını çalıştır. Sonra
modeli eğitim verisinin **yarısıyla** ve **tamamıyla** eğit, iki doğruluğu ve
`veri-miktari.png` grafiğini getir, farkı tek cümleyle yorumla.

## Sonraki konu

**Konu 4 — Temsil ve gömme vektörleri.** Bu konuda rengi üç sayıya çevirdik:
`(230, 57, 70)`. Konu 4'te **kelimeleri** sayıya çevireceğiz; bu kez üç değil, 1024
sayıya. Bu konudaki "en yakın komşu" fikri orada da devam ediyor: iki kelime
birbirine benziyor mu, sayılarına bakarak söyleyeceğiz. Ve Adım 8'deki soru orada
daha da önemli hâle geliyor: sayılar, bizim "benzer" dediğimiz şeyi yakalıyor mu?

---

## Kendini dene — cevaplar

1. Herkes aynı etiketi verdiyse en fazla **1.0** (12'de 12). 6'ya 6 bölünmüşse en fazla
   **0.5**: model tek bir cevap verebilir, hangisini seçerse seçsin öbür altı kişide
   yanılır. Tavan fikri budur.
2. "Nerede ölçtün?" Tavan %78 iken %98 doğruluk, aynı renklere verilen farklı
   etiketleri de bildiği anlamına gelir; bu imkânsız. Büyük ihtimalle eğitim verisinde
   ölçülmüş ya da etiket özniteliğe karışmış.
3. Kod çalışmaya devam eder, ama her çalıştırmada bölme farklı olur, doğruluk da
   değişir (yedek veride 0.65 ile 0.78 arası gibi). Sonuçları başkalarıyla ya da kendi
   önceki denemenle kıyaslayamazsın.
4. Evet, hata verir, çünkü `y_egitim` adlı değişkene aslında test öznitelikleri
   düşer ve uzunluklar tutmaz (`inconsistent numbers of samples`). Hata vermese bile
   model yanlış şeyi öğrenir. Sıra her zaman: eğitim X, test X, eğitim y, test y.
5. k=1 tek bir arkadaşa sormak, o azınlıktaysa yanılırsın; k=5 beş arkadaşa sorup
   çoğunluğa uymak, tek kişinin farklı görüşü seni yanıltmaz.
6. Çünkü cevabı bej hakkında bir şey bilen biri değil, en yakın bildiği renk olan
   kremi etiketleyenler veriyor ve krem sınıfın en çok tartıştığı renk (5'e 5).
   Model 20 rengin dışını bilmiyor.
7. İkisi de yanlış değil; farklı soruların cevabı. 0.77 "bilinen bir renk için başka
   birinin etiketini tahmin etme" başarısı, 0.60 "hiç görülmemiş bir renge etiket
   verme" başarısı. Yeni renkler hakkında karar vereceksen 0.60'a bakmalısın.
8. Birkaç iyi cevap: etiketleme listesine kafede kullanılabilecek tonları (bejler,
   kahveler, yeşillerin açık tonları) eklemek; rengi tek başına değil bir mekân
   görselinin içinde göstermek; etiketleyenlere kafenin kullanıcılarına benzeyen
   kişileri de katmak. Hepsinin ortak noktası: modelin kalitesi, verinin nasıl
   toplandığıyla başlıyor.
