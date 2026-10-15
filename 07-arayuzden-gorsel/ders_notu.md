# Konu 7 — Görsel Üretimi: Yönergeden Görsele

Bu not konunun özetidir; derste çalıştırdığımız `ders.ipynb` defteriyle **aynı sırada**
ilerler: Isınma, sonra Adım 1–8 ve kısa bir Bonus. Derste kaçırdığın bir yer olursa
buradan oku, sonra defterde o adımın hücrelerini çalıştır. Nottaki kod blokları
defterdeki hücrelerin birebir aynısı.

**Konu 6'da:** üretmenin, öğrenilmiş bir haritada bir nokta seçip oradan geri kurmak
olduğunu gördük. Noktayı biz seçtik.
**Bu konuda:** noktayı **yönerge** (prompt) seçiyor. Gerçek bir görsel üreticiyi tasarımcı
gözüyle yönetmeyi öğreniyoruz: rastgele denemekten **kontrollü denemeye**.

> Görsel bir anda çıkmaz; gürültüden adım adım temizlenir. Tohum rastgeleliği sabitler.
> İyi deney, bir seferde tek bir şeyi değiştirir.

**Bu konuda yeni kod yazmıyoruz:** hazır hücrelerde yalnızca tırnak içindeki metinleri ve
sayıları değiştiriyoruz. `gorsel_araci.py` adlı hazır bir aracı bir arayüz gibi kullanıyoruz: içine yönergeyi yazıyorsun, görsel çıkıyor. Aracın içini (istek, anahtar,
yanıtı dosyaya yazmak) **Konu 8'de** birlikte açacağız.

**Konunun sonunda elinde:** `ciktilar/` klasöründe yaklaşık 25 görsel, bir stil panosu
(`stil_panosu.png`) ve kendi brifin için bir başlangıç.

**Kurulum:** yeni kütüphane yok. `git pull` ile konu klasörü geldikten sonra `gita3111`
klasöründe bir kez `uv sync` çalıştır.

**Anahtar:** Isınma anahtarsız. Adım 1'den sonrası `anahtar.txt` ister (Konu 2'deki dosyanın
aynısı, `gita3111` klasöründe). Defterin tamamı yaklaşık 25 görsel üretir; Cloudflare'in
ücretsiz günlük kotasının küçük bir kısmı. Kota her gün 03:00'te (Türkiye saati) yenilenir.

> **Bu nottaki çıktılar hakkında.** Görseller her çalıştırmada (tohum vermediğinde) değişir
> ve her modelde farklıdır; o yüzden notta görsel yok, **sorular** var. Kendi çıktına bak.

---

## Isınma: yönergenin parçaları

İyi bir yönerge rastgele kelimeler değil, parçaları belli bir tariftir.

```python
ozne = "a ceramic coffee cup on a wooden desk"   # özne: ahşap masada seramik bir fincan
ortam = "next to an open notebook"               # ortam: açık bir defterin yanında
stil = "watercolor illustration"                 # stil: suluboya illüstrasyon
isik = "soft morning light"                      # ışık: yumuşak sabah ışığı
kompozisyon = "top-down view"                    # kompozisyon: tepeden bakış

yonerge = f"{ozne}, {ortam}, {stil}, {isik}, {kompozisyon}"
print(yonerge)
```

- Her parça ayrı bir değişkende. `f"..."` içindeki `{...}` yerine değişkenin değeri gelir
  (Konu 2'de adresi de böyle kurmuştuk).
- `#` ile başlayan kısımlar **yorum**: Python onları okumaz, yalnızca sana Türkçesini söylüyor.

| Parça | Soru | Örnekler |
|---|---|---|
| Özne | Ne görüyoruz? | *a ceramic coffee cup*, *a bicycle*, *an old library* |
| Ortam | Nerede, yanında ne var? | *on a wooden desk*, *in a rainy street* |
| Stil | Hangi teknik, hangi üslup? | *watercolor illustration*, *flat vector poster*, *linocut print*, *35mm film photograph* |
| Işık | Ne zaman, nasıl aydınlanıyor? | *soft morning light*, *warm desk lamp at night*, *overcast daylight* |
| Kompozisyon | Kamera nerede? | *top-down view*, *close-up*, *wide shot* |

`stil` satırındaki metni `"flat vector poster"` yapıp yeniden çalıştırınca yönergenin yalnızca
o parçası değişir (denemeden sonra yeniden `"watercolor illustration"` yap). Bugünkü bütün deneyler bu fikre dayanıyor: **bir seferde tek parça.**

**Neden İngilizce?** Görsel üreticiler çoğunlukla İngilizce açıklamalı görsellerle eğitildi.
Konu 5'teki gibi: Türkçe metin daha çok belirtece (parçaya) bölünür ve eğitim verisinde çok
daha az bulunur. Adım 6'da bunu sınayacağız.

---

## Adım 1 — İlk görsel

```python
from gorsel_araci import ciz, duzenle, yan_yana
```

Bu satır bu klasördeki `gorsel_araci.py` dosyasından üç fonksiyonu alır. Konu 4'teki
`from sklearn.decomposition import PCA` gibi; tek fark, bu dosya senin klasöründe.

```python
ilk = ciz(yonerge)
print(ilk)
```

- `ciz(yonerge)`: yönergeyi Cloudflare'deki bir görsel modeline gönderir, gelen görseli
  `ciktilar/` klasörüne numarayla kaydeder (`001.jpg`, `002.jpg`...) ve ekranda gösterir.
- `ciz` kaydettiği dosyanın **yolunu** geri verir; `ilk` değişkeninde duruyor (`ciktilar/001.jpg`
  gibi). Adım 8'de bu görseli düzenleyeceğiz.

Aracın üç fonksiyonu:

| Fonksiyon | Ne yapar |
|---|---|
| `ciz(yonerge, ...)` | Yönergeden görsel üretir, kaydeder, gösterir; dosya yolunu geri verir |
| `duzenle(yol, talimat)` | Var olan bir görseli talimatla değiştirir; yeni dosyanın yolunu geri verir |
| `yan_yana(yollar, basliklar)` | Birkaç görseli başlıklarıyla yan yana gösterir; `kaydet="..."` verirsen panoyu dosyaya yazar |

**Bak:** görsel yönergedeki her parçayı karşılıyor mu? Hangisini atlamış?

---

## Adım 2 — Aynı yönerge, aynı görsel mi?

Görsel üretici işe **rastgele bir gürültüyle** başlar (eski televizyonlardaki karıncalanma gibi).
Gürültü her seferinde farklıysa görsel de farklı olmalı. Sınıyoruz:

```python
birinci = ciz(yonerge, goster=False)
ikinci = ciz(yonerge, goster=False)
yan_yana([birinci, ikinci], ["1. deneme", "2. deneme"])
```

- `goster=False`: görseli hemen gösterme; biz birazdan ikisini yan yana göstereceğiz.
- `yan_yana` iki liste alır: görsellerin yolları ve başlıkları. İki liste aynı sırada olmalı
  (Konu 3'teki X ve y gibi).

Büyük ihtimalle iki farklı görsel geldi. Rastgeleliği sabitlemenin yolu **tohum** (seed):
başlangıçtaki gürültüyü üreten sayı.

```python
birinci = ciz(yonerge, tohum=42, goster=False)
ikinci = ciz(yonerge, tohum=42, goster=False)
yan_yana([birinci, ikinci], ["tohum 42", "yine tohum 42"])
```

**Aynı model + aynı yönerge + aynı tohum = aynı görsel.** 42'nin özel bir anlamı yok;
herhangi bir tam sayı olur. Önemli olan, deney boyunca **aynı** kalması.

Bu, deney yapabilmenin şartı. Bir şeyi değiştirdiğimizde farkın o değişiklikten geldiğinden
emin olmak için geri kalan her şeyi sabit tutarız. Bundan sonra hep `tohum=42`.

---

## Adım 3 — Gürültüden görsele: adım sayısı

Model gürültüyü bir anda değil, **adım adım** temizler. Bu yönteme **difüzyon** (diffusion)
denir. Bu modelde adım sayısını 1 ile 8 arasında seçebiliyoruz; seçmezsen 4.

```python
yollar = []
for adim in [1, 2, 4, 8]:
    yol = ciz(yonerge, tohum=42, adim=adim, goster=False)
    yollar.append(yol)

yan_yana(yollar, ["1 adım", "2 adım", "4 adım", "8 adım"])
```

- `yollar = []`: boş bir liste; her turda üretilen görselin yolunu ekliyoruz (`append`).
  Konu 2'de soruları listeden döngüyle sormuştuk; burada cevapları (görselleri) listeye topluyoruz.
- Tohum sabit; yalnızca `adim` değişiyor. Kontrollü deneyin ilk örneği.
- **Dikkat:** dört görsel aynı üretimin ara kareleri değil. Her biri baştan, farklı adım sayısıyla
  üretildi. Aynı tohumla başladıkları için aynı gürültüden yola çıkıyorlar.

**Bak:** 1 adımla 8 adım arasındaki fark nerede: biçimde mi, renkte mi, ayrıntıda mı? Fark
beklediğinden küçükse şaşırma: bu model (FLUX.1 schnell) az adımda bitirmek için özel olarak
eğitildi. Daha çok adım daha çok süre ve kota demek; bu model 4 adımda çoğu zaman yeterli.

### Difüzyon nasıl öğrenildi?

Eğitimde milyonlarca görsele adım adım gürültü eklendi, ta ki görsel tamamen karıncalanana
kadar. Model her adımda "bu gürültünün altında ne vardı?" sorusunu cevaplamayı öğrendi.
Üretirken bu işi **tersine** yapıyor: saf gürültüden başlayıp her adımda biraz temizliyor.
Yönerge, temizlerken hangi yöne gideceğini söylüyor.

Konu 6'nın diliyle: gürültü, haritada rastgele bir **başlangıç noktası**. Her adım bu noktayı
yönergenin tarif ettiği bölgeye biraz kaydırıyor; en sonda çözücü noktadan görseli geri kuruyor.
Tohum başlangıç noktasını belirlediği için aynı tohum aynı görseli veriyor.

---

## Adım 4 — Kontrollü deney: yalnızca stil değişsin

```python
stiller = ["watercolor illustration", "flat vector poster", "35mm film photograph"]

yollar = []
for yeni_stil in stiller:
    deneme = f"{ozne}, {ortam}, {yeni_stil}, {isik}, {kompozisyon}"
    yol = ciz(deneme, tohum=42, goster=False)
    print(yol, deneme)
    yollar.append(yol)

yan_yana(yollar, stiller, kaydet="stil_panosu.png")
```

- Her turda yeni stille bir `deneme` yönergesi kuruyoruz: dört parça aynı, yalnızca stil değişiyor.
  Isınmadaki `yonerge` ve `stil` değişmeden kalıyor; sonraki adımlar onları kullanacak.
- `print(yol, deneme)` her görselin dosya adını ve yönergesini yazıyor: üretim günlüğüne bunları,
  model (`flux`) ve tohumla (`42`) birlikte yazacaksın.
- `kaydet="stil_panosu.png"`: panoyu bu klasöre bir görsel dosyası olarak da kaydeder. Ödevde
  kendi panonu böyle kaydedeceksin.

**Bak:** tohum aynı olduğu için üç görselin kompozisyonu (fincanın yeri, açısı) birbirine
benziyor mu? Benziyorsa stil değişikliği yalnızca "yüzeyi" değiştirmiş demektir.

### Yalnızca ışık değişsin

```python
isiklar = ["warm desk lamp at night", "harsh midday sun", "overcast daylight"]

yollar = []
for yeni_isik in isiklar:
    deneme = f"{ozne}, {ortam}, {stil}, {yeni_isik}, {kompozisyon}"
    yol = ciz(deneme, tohum=42, goster=False)
    print(yol, deneme)
    yollar.append(yol)

yan_yana(yollar, isiklar)
```

Bu kez stil sabit (Isınmadaki suluboya), yalnızca ışık değişiyor: gece masa lambası, sert öğle
güneşi, bulutlu gün.

**Tartış:** hangi ışık "sessiz bir çalışma yeri" brifine en çok uyuyor? Konu 1'deki
yorumlarda iç mekânın karanlık bulunduğunu hatırla: ışık seçimi bir tasarım kararı.

---

## Adım 5 — Uzun yönerge daha mı iyi?

Slaytlardaki iddia: "iyi yönerge uzun değil, net olandır." Sınıyoruz.

```python
kisa = "a ceramic coffee cup on a wooden desk, watercolor illustration, soft morning light"
uzun = "a ceramic coffee cup on a wooden desk, minimal, extremely detailed, 8k, masterpiece, at night, sunny, watercolor, photorealistic"

yol_kisa = ciz(kisa, tohum=42, goster=False)
yol_uzun = ciz(uzun, tohum=42, goster=False)
yan_yana([yol_kisa, yol_uzun], ["kısa ve net", "uzun ve çelişkili"])
```

Uzun yönergede birbiriyle **çelişen** istekler var: *minimal* ve *extremely detailed*,
*at night* ve *sunny*, *watercolor* ve *photorealistic*. Bir de internetten kopyalanan
kalıplar: *8k, masterpiece*.

**Bak:** hangisi brife daha yakın? Çelişen isteklerden model hangisini seçmiş? Model
çelişkiden birini seçmek zorunda ve hangisini seçeceğini sen belirleyemiyorsun. "8k,
masterpiece" gibi kalıplar da çoğu zaman bir şey katmaz.

Senin denemende iddia tutmadıysa bu da bir bulgu: tek modelde, tek tohumla yapılan tek deney
kesin hüküm vermez. Tohumu değiştirip tekrarla.

---

## Adım 6 — Türkçe mi, İngilizce mi?

```python
turkce = "ahşap masada seramik bir kahve fincanı, suluboya illüstrasyon, yumuşak sabah ışığı"
ingilizce = "a ceramic coffee cup on a wooden desk, watercolor illustration, soft morning light"

yol_tr = ciz(turkce, tohum=42, goster=False)
yol_en = ciz(ingilizce, tohum=42, goster=False)
yan_yana([yol_tr, yol_en], ["Türkçe", "İngilizce"])
```

**Bak:** Türkçe yönergenin hangi kısımları görsele girdi, hangileri kayboldu? Fincan var mı,
suluboya mı, ışık sabah ışığı mı? Fark çıkmadıysa bu model kısa Türkçe yönergeyi iyi anlıyor
demektir; daha uzun ve ayrıntılı bir Türkçe yönergeyle dene.

Modeller çoğunlukla İngilizce metinle eğitildi ve Türkçe metin daha çok belirtece (parçaya)
bölünür (Konu 5). **Pratik kural:** yönergeyi İngilizce yaz; aklına Türkçe geliyorsa önce
çevir, sonra kısalt. Çeviri için bir sohbet modeli kullanabilirsin; ama çeviriyi okuyup
her parçanın yerinde olduğunu kontrol et.

---

## Adım 7 — Başka bir model, başka bir karakter

```python
yol_flux = ciz(yonerge, tohum=42, goster=False)
yol_sdxl = ciz(yonerge, tohum=42, model="sdxl", goster=False)
yan_yana([yol_flux, yol_sdxl], ["flux", "sdxl"])
```

- `yonerge` Isınmadaki yönerge (suluboya, sabah ışığı).
- `model="sdxl"`: Stable Diffusion XL (Stability AI). Şimdiye kadar kullandığımız varsayılan
  model `flux`: FLUX.1 schnell (Black Forest Labs).
- İki model farklı verilerle, farklı yöntemlerle eğitildi. Aynı tohum aynı görseli **vermez**;
  tohum yalnızca aynı modelin içinde işe yarar.

**Bak:** renk, çizgi, ayrıntı, kompozisyon: iki modelin "eli" nerede farklı? Bir tasarımcının
üslubu gibi her modelin bir karakteri var. Doğru modeli seçmek de bir karar.

### Negatif yönerge, en ve boy

```python
yol_afis = ciz(yonerge, tohum=42, model="sdxl", negatif="text, letters, watermark, people", en=1024, boy=576)
```

`sdxl` iki şey daha alıyor:

- **Negatif yönerge** (`negatif`): görselde **istemediğin** şeyler. Burada yazı, harf, filigran
  ve insan. Bir istek, garanti değil.
- **En ve boy** (`en`, `boy`): görselin piksel boyutu. 1024 × 576 tam 16:9: yatay bir afiş ya da
  sunum görseli. Dikey bir hikâye görseli için `en=576, boy=1024`.

`flux` bu ikisini almıyor; `ciz(yonerge, en=1024)` yazarsan araç
`ValueError: flux negatif yönerge, en ve boy almıyor; bunlar için model="sdxl" kullan.` der.

---

## Adım 8 — Var olanı değiştirmek: görsel düzenleme

```python
yeni = duzenle(ilk, "make the background a plain sage green color, keep the cup the same")
yan_yana([ilk, yeni], ["önce", "sonra"])
```

- `duzenle` iki şey alır: düzenlenecek görselin yolu (`ilk`, Adım 1'deki görsel) ve bir talimat.
  Talimat: "arka planı düz adaçayı yeşili yap, fincan aynı kalsın".
- `ciktilar/` içinde iki yeni dosya görürsün: modele gönderilen küçük kopya (png) ve sonuç (jpg).
- Arkada üçüncü bir model çalışıyor: FLUX.2 klein. Araç görseli 512 × 512'ye küçültüp gönderiyor;
  sonuç da 512 × 512.

**Bak:** fincan korundu mu, yoksa model başka şeyleri de değiştirdi mi? Talimatı değiştirip
dene: `"add steam rising from the cup"` (fincandan yükselen buhar ekle), `"turn it into a pencil
sketch"` (karakalem çizime çevir). Tasarımcının işi çoğu zaman sıfırdan üretmek değil,
eldekini değiştirmek: ürün fotoğrafının arka planı, bir afişin renk varyasyonları.

---

## Bonus — Kendi brifin

Seçtiğin bir marka ya da etkinlik için Isınmadaki beş parçayı yeniden yaz ve Isınma hücresini
çalıştır. Sonra Adım 4'teki stil döngüsünü kendi stillerinle çalıştır; panoyu
`kaydet="odev7_pano.png"` ile kaydet. Ödev bunun üzerine kurulu.

---

## Etik ve telif: derste konuştuklarımız

- **Eğitim verisi.** Görsel üreticiler internetten toplanan yüz milyonlarca görselle eğitildi;
  çoğunun sahibine sorulmadı. Sanatçılar ve fotoğraf ajansları dava açtı.
- **Üslup taklidi.** "Yaşayan bir illüstratörün tarzında" istemek, o kişinin yıllarca kurduğu
  üslubu onun izni olmadan kullanmak demek. **Derste kural:** yaşayan bir sanatçının adını stil
  olarak yazmıyoruz.
- **Telif belirsizliği.** Üretilen görselin telif durumu birçok ülkede belirsiz; bazı ülkelerde
  insan katkısı olmayan görsel telifle korunmuyor. Ticari işte müşteriye görselin nasıl
  üretildiğini söylemek gerekir.
- **Yanıltıcı görsel.** Gerçek kişileri, markaları, olayları yanıltıcı biçimde üretmek sahte
  haber ve sahte reklam demek.
- **Derste kural:** her çıktıda kullanılan **model, tohum ve yönerge** üretim günlüğüne yazılır.

---

## Defterin bölümleri

| Adım | Ne yaptık | Elimizde ne oluştu | Anahtar |
|---|---|---|---|
| Isınma | Yönergeyi beş parçadan kurduk | `yonerge` | gerekmez |
| 1 | Aracı aldık; ilk görsel | `ciz`, `duzenle`, `yan_yana`, `ilk` | gerekir |
| 2 | Aynı yönerge iki kez; sonra tohumla iki kez | — | gerekir |
| 3 | 1, 2, 4, 8 adım | adım şeridi | gerekir |
| 4 | Yalnızca stil, sonra yalnızca ışık değişti | `stil_panosu.png` | gerekir |
| 5 | Kısa ve uzun yönerge | — | gerekir |
| 6 | Türkçe ve İngilizce yönerge | — | gerekir |
| 7 | flux ve sdxl; negatif yönerge, en ve boy | yatay afiş | gerekir |
| 8 | Görsel düzenleme | düzenlenmiş görsel | gerekir |
| Bonus | Kendi brifin | `odev7_pano.png` | gerekir |

Hücreleri her zaman yukarıdan aşağı çalıştır. Defteri yeni açtıysan Isınma hücresini ve
Adım 1'in içe aktarma (`from gorsel_araci import ...`) hücresini çalıştırmadan sonraki adımlar
`NameError` verir (`yonerge`, `ciz` tanımlı olmaz).

Bu konuda alıştırma defteri yok: ilk oturum vizenin sözlü teyidiyle açılıyor ve konu kod
yazmayı değil, aracı yönetmeyi öğretiyor.

---

## Sık karşılaşılan hatalar ve mesajlarını okumak

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `ModuleNotFoundError: No module named 'gorsel_araci'` | Defterin kopyası konu klasörünün dışında | Kopya `07-arayuzden-gorsel` klasöründe, `gorsel_araci.py`'nin yanında durmalı |
| `FileNotFoundError: ... '../anahtar.txt'` | Anahtar dosyası yok ya da yanlış yerde | Dosya `gita3111` klasöründe durmalı (Konu 2) |
| `RuntimeError: anahtar.txt okunamadı: iki satır olmalı, ...` | Dosyada `ACCOUNT_ID = ...` ya da `API_TOKEN = ...` satırı yok (ör. `=` yerine `:` yazılmış) | İki satırı `AD = değer` biçiminde yaz |
| `RuntimeError: İstek başarısız, durum kodu 401` | Anahtar yanlış ya da süresi dolmuş | `anahtar.txt`'yi kontrol et (kurulum yönergesinin 6. adımı) |
| `RuntimeError: İstek başarısız, durum kodu 404` | `ACCOUNT_ID` yanlış ya da tırnak içinde yazılmış | `anahtar.txt`'deki `ACCOUNT_ID`'yi tırnaksız, eksiksiz yaz |
| `RuntimeError: İstek başarısız, durum kodu 429` | Kota doldu ya da çok hızlı istek attın | Biraz bekle; günlük kota 03:00'te yenilenir |
| `RuntimeError: İstek başarısız, durum kodu 400` | Ayar sınır dışı: ör. `adim=20` (flux en fazla 8) | Sınırları kontrol et: flux `adim` 1–8, sdxl `adim` en fazla 20, `en`/`boy` 256–2048 |
| `ValueError: flux negatif yönerge, en ve boy almıyor ...` | `negatif`, `en` ya da `boy` flux'a verildi | `model="sdxl"` ekle |
| `KeyError: 'dalle'` ya da `'SDXL'` | `model` olarak tanımsız bir ad yazıldı (büyük-küçük harf de önemli) | Yalnızca `"flux"` ya da `"sdxl"` |
| `TypeError: ciz() got an unexpected keyword argument 'steps'` | Aracın Türkçe adları yerine API'nin adları yazıldı | `adim=`, `tohum=`, `negatif=`, `en=`, `boy=` |
| `requests.exceptions.ConnectionError` | İnternet yok | İnternete bağlan |
| `NameError: name 'yonerge' is not defined` (ya da `'ciz'`, `'ozne'`, `'ilk'`) | Isınma ya da Adım 1'in hücreleri çalıştırılmadı; Adım 1 hata verdiyse `ilk` de yok | Hücreleri baştan sırayla çalıştır |
| `FileNotFoundError: ... 'ciktilar/001.jpg'` (Adım 8) | `ciktilar/` klasörü silindi ya da dosya taşındı | Adım 1'den yeniden çalıştır |
| `SyntaxError: (unicode error) 'unicodeescape' ...` | `duzenle`'ye Windows yolu ters bölüyle verildi: `"C:\Users\..."` | Düz bölü kullan: `"C:/Users/..."` |
| `PIL.UnidentifiedImageError: cannot identify image file ...` | Görsel HEIC (iPhone) ya da bozuk | JPG ya da PNG'ye çevir |
| `IndexError: list index out of range` (`yan_yana`) | Başlık sayısı görsel sayısından az | İki listeyi aynı uzunlukta yaz |
| Görseller yan yana değil alt alta, tek tek çıkıyor | `goster=False` yazılmamış | Döngüdeki `ciz`'e `goster=False` ekle |

---

## Kendini dene

Cevaplar notun en sonunda. Önce kendin düşün.

1. Bir arkadaşın aynı yönergeyle senden çok daha güzel bir görsel aldı. Aynısını almak için
   ondan hangi üç bilgiyi istemelisin?
2. Stil, ışık ve kompozisyonu aynı anda değiştirdin; yeni görsel daha iyi. Hangi değişikliğin
   işe yaradığını söyleyebilir misin? Ne yapmalıydın?
3. Adım 3'te neden adım sayısını değiştirirken tohumu sabit tuttuk?
4. "Görsel kötü çıktı, yönergeye 'masterpiece, 8k, ultra detailed' ekleyeyim" diyen birine
   ne söylersin?
5. Bir müşteri için Instagram hikâyesi (dikey) görseli üreteceksin. Hangi model ve hangi
   `en`/`boy` değerleri?
6. Negatif yönergeye "text" yazdın ama görselde yine harfe benzer şekiller var. Model mi
   bozuk?
7. Bir müşteri "şu ünlü illüstratörün tarzında bir afiş" istiyor. Ne yaparsın?

---

## Bu konuda öğrendiklerin

- **Difüzyon.** Model rastgele bir gürültüden başlar, her adımda biraz temizler; yönerge yönü
  belirler. Çoğu modelde az adım kaba sonuç verir; bugünkü FLUX.1 schnell az adım için eğitildiği
  için fark küçük olabilir. Çok adım daha yavaş ve pahalı.
- **Tohum.** Başlangıç gürültüsünü belirleyen sayı. Aynı model + yönerge + tohum = aynı görsel.
- **Yönerge anatomisi.** Özne, ortam, stil, ışık, kompozisyon. Uzun değil net; çelişkisiz.
- **Kontrollü deney.** Bir seferde tek değişken; sonuçları yan yana bir panoda karşılaştırmak.
- **Dil.** Modeller İngilizce yönergede daha iyi; Türkçe parçalar kaybolabilir.
- **Modellerin karakteri.** Aynı yönergeye farklı modeller farklı "ellerle" cevap verir.
- **Negatif yönerge, en ve boy, düzenleme.** İstemediğini söylemek, şekli baştan seçmek, var olanı
  talimatla değiştirmek.
- **Etik ve telif.** Eğitim verisi, üslup taklidi, telif belirsizliği; şeffaflık: model, tohum
  ve yönerge günlüğe yazılır.

## Bu konunun tek cümlesi

> Görsel gürültüden adım adım temizlenerek çıkar; tasarımcı yönergeyi bir tarif gibi yazar ve
> her seferinde tek bir şeyi değiştirerek dener.

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **Yönerge (prompt)** | Modele ne üretmesini istediğini anlatan metin |
| **Difüzyon** | Gürültüden başlayıp adım adım temizleyerek görsel üretme yöntemi |
| **Gürültü** | Rastgele noktalardan oluşan, hiçbir şey göstermeyen görüntü; karıncalanma |
| **Adım (step)** | Difüzyonda bir temizleme turu |
| **Tohum (seed)** | Başlangıç gürültüsünü belirleyen sayı; aynı tohum aynı gürültü |
| **Negatif yönerge** | Görselde istemediğin şeyleri yazdığın ikinci yönerge |
| **En-boy oranı** | Görselin genişliğinin yüksekliğine oranı: 1:1 kare, 16:9 yatay, 9:16 dikey |
| **Kontrollü deney** | Diğer her şeyi sabit tutup tek bir şeyi değiştirerek yapılan deney |
| **Görsel düzenleme** | Var olan bir görseli bir talimatla değiştirmek |
| **FLUX / SDXL** | Bugün kullandığımız iki görsel modeli: Black Forest Labs'in FLUX'u ve Stability AI'ın Stable Diffusion XL'i |
| **Üretim günlüğü** | Hangi görseli hangi model, tohum ve yönergeyle ürettiğini yazdığın kayıt |

## Ödev

`odevler/odev7.md` (puansız): seçtiğin bir marka ya da etkinlik için üç farklı görsel dil
denemesi; tohum sabit, yalnızca stil değişiyor. Pano + iki cümle + üretim günlüğü.

## Sonraki konu

**Konu 8 — Koddan görsel üretimi.** Bugün `gorsel_araci.py`'yi bir arayüz gibi kullandık.
Konu 8'de içini açıyoruz: isteği kendimiz kuracak, gelen görseli (metin değil, ikili veri:
binary)
dosyaya kendimiz yazacak, dosya adlarını düzenleyecek ve hataları yakalayacağız.

---

## Kendini dene — cevaplar

1. **Model, yönerge ve tohum.** Üçü aynıysa aynı görseli alırsın. Biri eksikse (çoğu zaman
   tohum) aynısını alamazsın. Üretim günlüğü tam bunun için.
2. Söyleyemezsin: üç şey birden değişti. Önce tek birini değiştirip (ör. yalnızca ışık) aynı
   tohumla denemeliydin; sonra ötekileri tek tek.
3. Fark adım sayısından mı, gürültüden mi geldi, ayırt etmek için. Tohum değişseydi her görsel
   başka bir gürültüden başlardı; farkın adım sayısından geldiğini bilemezdik.
4. Bu kalıplar çoğu zaman bir şey katmıyor (Adım 5). Önce yönergeyi parçalarına ayır: özne,
   stil, ışık net mi, çelişen istek var mı? Sorunu bulmak için tek bir parçayı değiştirip dene.
5. `sdxl` (en ve boy alan model), dikey: `en=576, boy=1024` (9:16). flux en ve boy almıyor.
6. Bozuk değil: negatif yönerge bir istek, garanti değil. Görsel üreticiler yazı benzeri şekiller
   üretmeye yatkın; gerekirse görseli düzenle (Adım 8) ya da yazıyı sonradan tasarım programında
   koy.
7. Yaşayan bir sanatçının adını stil olarak yazmıyoruz. Müşteriyle o tarzın **hangi özelliklerini**
   sevdiğini konuş (renk paleti, çizgi kalınlığı, doku) ve yönergeye bunları yaz. Gerekiyorsa
   o illüstratörün kendisine iş ısmarlamayı öner.
