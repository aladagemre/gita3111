# Konu 12 — Araç Kullanımı: Modelin Karar Verdiği Program

Bu not konunun özetidir; derste çalıştırdığımız `ders.ipynb` defteriyle **aynı sırada**
ilerler: Isınma, sonra Adım 1–8 ve kısa bir Bonus. Derste kaçırdığın bir yer olursa
buradan oku, sonra defterde o adımın hücrelerini çalıştır. Nottaki kod blokları
defterdeki hücrelerin birebir aynısı.

**Konu 11'e kadar:** hangi fonksiyonun ne zaman çalışacağına sen karar verdin; `ciz`'i sen çağırdın, sırayı sen yazdın.
**Bu konuda:** bir kararı modele bırakıyoruz:

> Kullanıcı serbest bir cümle yazar. Model iki araçtan hangisinin gerektiğine karar verir ve kararını alanları belli
> bir cevap (JSON) olarak gönderir. Program kararı okur ve o aracı çalıştırır. Sonra kararları ölçeriz: kaçında
> seninle aynı fikirde?

**Konunun sonunda elinde:** serbest cümleyle çalışan, iki araçtan birini kendisi seçen küçük bir program; `ciktilar/`
klasöründe onun ürettiği ya da düzenlediği görseller; ve modelin kararlarının doğruluğu: önce muğlak, sonra
netleştirilmiş bir araç tarifiyle.

**Kurulum:** yeni kütüphane yok. `git pull` ile konu klasörü geldikten sonra `gita3111` klasöründe bir kez `uv sync`
çalıştır.

**Anahtar:** Isınma anahtarsız. Adım 1'den sonrası `anahtar.txt` ister (Konu 2'deki dosya, `gita3111` klasöründe).
Defterin tamamı metin modeline yaklaşık 33 istek gönderir ve en fazla 5 görsel üretir ya da düzenler; günlük
ücretsiz kotanın %10'undan az. Ölçüm adımları (Adım 6–7) görsel üretmez, yalnızca karar sorar.

> **Bu nottaki çıktılar hakkında.** Isınma'nın çıktısı her bilgisayarda aynıdır. Modelin kararları, sloganları ve
> görseller gerçek modelden gelir; senin ekranında farklı olur. Notta "senin çıktına bak" dediğimiz yerlerde cevabı
> biz de bilmiyoruz.

---

## Isınma: kararı önce sen ver

Elimizde iki araç olacak: **uret** sıfırdan yeni bir görsel üretir, **duzenle** elimizdeki bir görseli değiştirir.
Elimizdeki tek görsel bir fincan fotoğrafı. Model karar vermeden önce **sen** karar veriyorsun:

```python
istekler = [
    "kafe için yeni bir afiş görseli yap",
    "şu fincan fotoğrafının arka planını sadeleştir",
    "menü kapağı için bir görsel üret",
    "bu görseldeki renkleri daha sıcak yap",
    "afişi daha sıcak yap",
    "yaz kampanyası için bir görsel",
]
etiketlerim = ["uret", "duzenle", "uret", "duzenle", "uret", "uret"]

print(len(istekler), len(etiketlerim))
```

Çıktı: `6 6`. Her isteğin bir etiketi var.

- `etiketlerim` listesinde hocanın etiketleri duruyor; katılmadığın yeri değiştir. Sıra önemli: listenin ilk elemanı
  ilk isteğin etiketi.
- Etiketler yalnızca `"uret"` ya da `"duzenle"` olmalı; Türkçe karakter yok, model de bu adları kullanacak.

İki listeyi yan yana yazdırıyoruz:

```python
sira = 0
for istek in istekler:
    print(etiketlerim[sira], "<-", istek)
    sira = sira + 1
```

Çıktı: altı satır, her biri `etiket <- istek` (ör. `duzenle <- şu fincan fotoğrafının arka planını sadeleştir`).

- İki listeyi aynı anda gezmek için bir **sıra sayacı** tutuyoruz: `sira` 0'dan başlar, her turda bir artar.
  `etiketlerim[sira]` o sıradaki etiket.
- `sira = sira + 1` satırı döngünün içinde olmalı; dışında kalırsa hep ilk etikete bakılır (alıştırmada var).

Hangi istekte karar vermek zor geldi? "afişi daha sıcak yap" iki türlü okunabilir: var olan bir afişi mi değiştirelim,
yeni ve daha sıcak bir afiş mi üretelim? Elimizde afiş yok, yalnızca fincan fotoğrafı var. Bu etiketler Konu 3'teki
**test verisi** gibi: doğru cevabı insan verdi. Adım 6'da modelin kararlarını bunlarla karşılaştıracağız.

---

## Adım 1 — Araçlar ve elimizdeki görsel

```python
import requests
import matplotlib.pyplot as plt
from pathlib import Path
from gorsel_araclari import ciz, duzenle, adres, basliklar
```

- `gorsel_araclari.py` bu klasördeki yardımcı dosya. İçindeki iki fonksiyon modelin seçeceği **araçlar**:
  - `ciz(yonerge, tohum)`: Konu 8'de yazdığın, Konu 9'da kullandığın fonksiyon. Yeni bir görsel üretir.
  - `duzenle(dosya, yonerge, tohum)`: Konu 8 Adım 9'daki düzenleme isteğinin fonksiyon hâli. Görseli en fazla 512
    piksele küçültür, form olarak (`data=` ve `files=`) gönderir.
- İkisi de görselin baytlarını verir; başarısızsa `None`.
- Model bu fonksiyonları değil, araçların **adlarını** görecek: yeni görsel için `uret`, düzenleme için `duzenle`.
  Hangi adın hangi fonksiyonu çalıştıracağını Adım 5'te biz yazacağız.
- `adres` ve `basliklar` metin modeline istek göndermek için. Anahtarı `../anahtar.txt`'den yardımcı dosya kendisi
  okur; bu hücre ilk çalıştığında, bir kez. `anahtar.txt`'yi sonradan düzeltirsen çekirdeği yeniden başlat (**Restart**).

```python
MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
metin_adresi = adres(MODEL)
```

Metin modeli Konu 2'den beri kullandığımız model. `adres(MODEL)` adresi kurar (Konu 2'deki f-string'in aynısı).

```python
fincan = plt.imread("veri/fincan.jpg")
plt.imshow(fincan)
plt.axis("off")
plt.show()
```

Elimizdeki görsel: `veri/fincan.jpg` (Konu 8'deki fincan). `duzenle` hep bu görseli değiştirecek. `plt.imread` görseli
okur, `plt.imshow` gösterir (Konu 8).

---

## Adım 2 — Alanları belli cevap: JSON modu

Konu 2'de modelden bir cevap istedik, bir paragraf geldi. Paragrafı insan okur; program okuyamaz. Program için
cevabın **alanları belli** olmalı. Buna **yapılandırılmış çıktı** denir.

```python
bicim = {"type": "json_object"}
soru = "Sessiz bir çalışma kafesi için bir slogan öner. Cevabı JSON ver; alanlar: slogan, ton, hedef_kitle."
govde = {"prompt": soru, "response_format": bicim}

cevap = requests.post(metin_adresi, headers=basliklar, json=govde, timeout=60)
print(cevap.status_code)
```

Çıktı: `200`.

- `"response_format"` (cevabın biçimi) gövdeye eklenen yeni alan. `{"type": "json_object"}` "cevabı JSON olarak ver"
  demek. Cloudflare buna **JSON modu** diyor.
- Hangi alanları istediğimizi sorunun içinde yazıyoruz: `slogan, ton, hedef_kitle`.
- `200` gelmediyse sonraki hücreyi çalıştırma (Konu 2). Model istenen biçime uyamazsa da hata dönebilir: JSON modu
  biçimi garanti etmez.

```python
yanit = cevap.json()
sonuc = yanit["result"]
kart = sonuc["response"]
print(kart)
print(kart["ton"])
```

Çıktı (senin cevabın farklı olur):

```
{'slogan': '...', 'ton': 'samimi', 'hedef_kitle': '...'}
samimi
```

- Cevabı Konu 2'deki gibi iki katmanda açıyoruz. Fark `sonuc["response"]`'ta: bu kez bir paragraf değil,
  bir **sözlük**. Konu 9'daki kartlar gibi; alanına adıyla erişiyoruz: `kart["ton"]`.

| Konu 2 | Konu 12 |
|---|---|
| `govde = {"prompt": soru}` | `govde = {"prompt": soru, "response_format": bicim}` |
| `sonuc["response"]` bir metin (paragraf) | `sonuc["response"]` bir sözlük |
| İnsan okur | Program okur: `kart["ton"]` |

Bu isteği çok kez göndereceğiz; bir fonksiyona koyuyoruz:

```python
def json_sor(soru, sicaklik):
    govde = {"prompt": soru, "temperature": sicaklik, "response_format": bicim}
    cevap = requests.post(metin_adresi, headers=basliklar, json=govde, timeout=60)
    if cevap.status_code != 200:
        print("İstek başarısız, durum kodu:", cevap.status_code)
        return None
    yanit = cevap.json()
    sonuc = yanit["result"]
    return sonuc["response"]
```

- Konu 5'teki `modele_sor` gibi sıcaklığı da alıyor: `sicaklik` gövdedeki `"temperature"` alanına gidiyor.
- Durum kodu 200 değilse `None` verir ve kodu yazar.
- `timeout=60`: cevap 60 saniyede gelmezse istek bırakılır (Konu 10).

---

## Adım 3 — Metin artık veri

```python
kartlar = []
for tur in range(5):
    kart = json_sor(soru, 0.9)
    kartlar.append(kart)
    print(kart["ton"], "|", kart["slogan"])
```

Çıktı: beş satır, her biri `ton | slogan`.

- `range(5)`: 5 kez. `tur` kaçıncı turda olduğumuzu tutar; burada kullanmıyoruz.
- Sıcaklık 0.9: her seferinde farklı bir slogan gelsin (Konu 5).
- `kartlar.append(kart)`: her kartı listeye ekler (Konu 9). Sonunda bir liste, içinde beş sözlük.

Kartlar artık **veri**: bir tabloya dökülebilir, süzülebilir. Konu 1'deki gibi süzüyoruz:

```python
for kart in kartlar:
    if kart["ton"] == "samimi":
        print(kart["slogan"])
```

- Yalnızca `ton` alanı tam olarak `"samimi"` olanları yazar. Kaç tane yazdı? Üstteki `ton` değerlerine bak.
- `ton` serbest bir alan: model her seferinde başka bir kelime yazabilir ("samimi", "Samimi", "sıcak ve samimi").
  Program için bunların hepsi farklı; `"Samimi"` süzgeçten geçmez.

Bir form tasarlarken serbest metin kutusu yerine **açılır menü** koymak gibi, alanın alabileceği değerleri soruda
sınırlıyoruz:

```python
soru = "Sessiz bir çalışma kafesi için bir slogan öner. Cevabı JSON ver; alanlar: slogan, ton (yalnızca samimi, resmi ya da esprili), hedef_kitle."

kartlar = []
for tur in range(5):
    kart = json_sor(soru, 0.9)
    kartlar.append(kart)
    print(kart["ton"], "|", kart["slogan"])

print("Samimi olanlar:")
for kart in kartlar:
    if kart["ton"] == "samimi":
        print(kart["slogan"])
```

- Tek fark sorudaki parantez: `ton (yalnızca samimi, resmi ya da esprili)`.
- Değerler artık üç seçenekten biri mi? Senin çıktına bak. Model kurala uymazsa süzgeç o kartı yine
  kaçırır; bu yüzden çıktıyı gözle de kontrol et.
- Bir sonraki adımda aynısını yapacağız: alanın değerini sınırlı bir listeden seçtireceğiz. Liste bu kez tonlar değil,
  **araçlar**.

---

## Adım 4 — Karar da bir alan

Modele araçlarımızı **tarif ediyoruz**: adları ve ne yaptıkları. Bu tarif bilerek kısa ve biraz muğlak; Adım 7'de
düzelteceğiz.

```python
araclar = "uret: görsel üretir. duzenle: görseli düzenler."
```

```python
def karar_ver(istek, tarif):
    soru = "Elindeki araçlar: " + tarif
    soru = soru + " Kullanıcının isteğine en uygun aracı seç."
    soru = soru + " Cevabı JSON ver; alanlar: arac (yalnızca aracın adı), yonerge (görsel modeline gidecek kısa İngilizce yönerge)."
    soru = soru + " Kullanıcının isteği: " + istek
    return json_sor(soru, 0)
```

- Soru parça parça kuruluyor: her satır soruya bir cümle ekler (`soru = soru + "..."`). Önce araçlar, sonra ne
  istediğimiz, sonra cevabın alanları, en sonda kullanıcının isteği.
- İki alan istiyoruz: `arac` (aracın adı: modelin **kararı**) ve `yonerge` (seçilen araca gidecek İngilizce yönerge;
  modelin kullanıcının Türkçe cümlesinden çıkardığı).
- `tarif` ayrı bir bilgi olarak geliyor; Adım 7'de başka bir tarifle aynı fonksiyonu çağıracağız.
- Sıcaklık 0: aynı isteğe her seferinde aynı karar gelsin (Konu 5). Kararı ölçeceğiz (Adım 6); ölçüm tekrar
  edilebilir olmalı.

```python
karar = karar_ver("şu fincan fotoğrafının arka planını sadeleştir", araclar)
print(karar)
print("Model şunu seçti:", karar["arac"])
print("Yönerge:", karar["yonerge"])
```

Çıktı (modelin kararı; senin ekranında farklı olabilir):

```
{'arac': '...', 'yonerge': '...'}
Model şunu seçti: ...
Yönerge: ...
```

- Kararı ekrana yazdırmak bu konunun alışkanlığı: modelin ne seçtiğini **görmeden** ne yaptığını bilemezsin.
- Yönergeye bak: kullanıcının cümlesinin çevirisi mi, daha fazlası mı?

---

## Adım 5 — Program kararı uygular

Model hiçbir şey çizmedi; yalnızca bir sözlük gönderdi. Kararı uygulayan **bizim programımız**.

```python
klasor = Path("ciktilar")
klasor.mkdir(exist_ok=True)
```

```python
def uygula(karar, dosya_adi):
    arac = karar["arac"]
    yonerge = karar["yonerge"]
    print("Model şunu seçti:", arac)
    print("Yönerge:", yonerge)
    if arac == "uret":
        resim = ciz(yonerge, 42)
    elif arac == "duzenle":
        resim = duzenle("veri/fincan.jpg", yonerge, 42)
    else:
        print("Bilinmeyen araç:", arac)
        resim = None
    if resim is None:
        print("Görsel yok")
        return None
    yol = klasor / dosya_adi
    with open(yol, "wb") as dosya:
        dosya.write(resim)
    print("Kaydedildi:", yol)
    return yol
```

- `arac` alanına bakıp doğru fonksiyonu çağırıyor: `if / elif / else` (GİTA2112).
- `else` dalı bir **güvenlik ağı**: model listede olmayan bir ad yazarsa (`"üret"`, `"edit"`) program yanlış aracı
  çalıştırmaz; `Bilinmeyen araç` yazar ve `None` verir. Modelin cevabına körü körüne güvenme.
- Görsel geldiyse `"wb"` ile dosyaya yazar (Konu 8) ve yolunu verir; gelmediyse `Görsel yok` yazar ve `None` verir.
- Tohum ikisinde de 42: aynı kararı yeniden uygularsan aynı görsel gelir.

```python
yol = uygula(karar, "karar_1.jpg")
```

Model `duzenle` seçtiyse fincan düzenlenir, `uret` seçtiyse yeni bir görsel üretilir. Hangisi oldu?

```python
gorsel = plt.imread(yol)
plt.imshow(gorsel)
plt.axis("off")
plt.show()
```

`Görsel yok` yazdıysa bu hücre hata verir (`AssertionError`): gösterilecek dosya yok. Üstteki mesaja bak.

Şimdi başka türden bir istek:

```python
karar = karar_ver("kafe için yeni bir afiş görseli yap", araclar)
yol = uygula(karar, "karar_2.jpg")
```

```python
gorsel = plt.imread(yol)
plt.imshow(gorsel)
plt.axis("off")
plt.show()
```

Bugün "yapay zeka ajanı" denen şeyin çekirdeği bu: model **karar verir**, program **uygular**. Gizemli bir şey yok:
bir sözlük ve bir `if`.

| Kim ne yapıyor? | |
|---|---|
| Kullanıcı | Serbest bir cümle yazar |
| Model | Cümleyi okur; `arac` ve `yonerge` alanlı bir sözlük gönderir. Hiçbir şey çizmez |
| Program (`uygula`) | `arac`'a bakar, `ciz`'i ya da `duzenle`'yi çağırır, sonucu kaydeder |

---

## Adım 6 — Model ne kadar doğru seçiyor?

İki örnek bir şey kanıtlamaz. Isınmadaki altı isteğin hepsini soruyoruz ve kararları senin etiketlerinle
karşılaştırıyoruz: Konu 3'teki **doğruluk** (doğru / toplam). Bu adımda görsel üretmiyoruz; her istek tek bir metin
isteği.

```python
def olc(tarif, liste, etiketler):
    sira = 0
    dogru = 0
    for istek in liste:
        karar = karar_ver(istek, tarif)
        arac = karar["arac"]
        beklenen = etiketler[sira]
        if arac == beklenen:
            dogru = dogru + 1
        else:
            print("Ayrıştık:", istek, "| ben:", beklenen, "| model:", arac)
        sira = sira + 1
    print("Doğru:", dogru, "/", len(liste))
```

- `olc` bir tarif, bir istek listesi ve bir etiket listesi alıyor; Adım 7'de başka listelerle çağıracağız.
- Isınmadaki sıra sayacı burada da var: `etiketler[sira]` o isteğin senin etiketin.
- Karar etiketle aynıysa `dogru` bir artar; değilse ayrıştığınız istek yazılır.
- `dogru = 0` döngünün **dışında**, başta bir kez. İçine koyarsan her turda sıfırlanır (alıştırmada var).

```python
olc(araclar, istekler, etiketlerim)
```

Çıktı: ayrıştığınız istekler (varsa) ve `Doğru: ... / 6`. Senin çıktına bak.

- Ayrıştığınız istekler, Isınma'da senin de zorlandığın istekler mi?
- Model mi yanıldı, yoksa istek mi iki türlü okunabiliyor? Modelin elinde yalnızca `araclar` metni var: "görseli
  düzenler" hangi görseli?

---

## Adım 7 — Sorun modelde değil tarifte

Bir tasarımcıya "afişi daha sıcak yap" desen o da sorar: hangi afiş? Modele verdiğimiz tarif de bir **brif**. Muğlak
brif, ister insana ister modele verilsin, yanlış işi getirir. Tarifi netleştiriyoruz:

```python
yeni_araclar = "uret: sıfırdan yeni bir görsel üretir."
yeni_araclar = yeni_araclar + " duzenle: YALNIZCA elimizdeki tek görseli, bir fincan fotoğrafını değiştirir."
yeni_araclar = yeni_araclar + " Kullanıcı 'bu', 'şu' ya da 'fotoğraf' diyerek o görseli işaret ediyorsa duzenle seç."
yeni_araclar = yeni_araclar + " Emin değilsen uret seç."
print(yeni_araclar)
```

- Tarif dört cümle: `uret` ne yapar; `duzenle` neyi değiştirir; `duzenle` **ne zaman** seçilmeli; emin değilse ne
  yapmalı.
- Tek satır çok uzun olmasın diye metni parça parça ekliyoruz (Adım 4'teki gibi).

Aynı altı istekle yeniden ölçüyoruz:

```python
olc(yeni_araclar, istekler, etiketlerim)
```

Sonuç değişti mi? Hangi istekte? Senin çıktına bak.

**Dikkat:** tarifi bu altı isteğe bakarak düzelttik ve yine bu altı istekle ölçtük. Konu 3'ü hatırla: test sonucuna
bakıp ayar yapmak, sonra aynı testte ölçmek, ölçümü güvenilmez yapar. Tarif yeni isteklerde de işe yarıyor mu?

```python
yeni_istekler = [
    "bu fincanın fotoğrafını siyah beyaz yap",
    "kahve festivali için bir poster tasarla",
    "fotoğraftaki fincanı kırmızı yap",
    "yeni şubemiz için bir tanıtım görseli hazırla",
    "görseli biraz daha aydınlat",
]
yeni_etiketlerim = ["duzenle", "uret", "duzenle", "uret", "duzenle"]

olc(yeni_araclar, yeni_istekler, yeni_etiketlerim)
```

- Modelin hiç görmediği beş istek; önce yine sen etiketle (`yeni_etiketlerim`).
- Son isteğe bak: "görseli biraz daha aydınlat". "Görseli" diyor, yani var olan bir görseli işaret ediyor; ama "bu",
  "şu" ya da "fotoğraf" demiyor. Kuralımız ona ne dedirtiyor? Kuralı fazla dar yazmak da bir hata.

Tarif yazmak bir kez yapılıp biten iş değil:

> Yaz → ölç → ayrışan isteğe bak → tarifi düzelt → **yeni** isteklerle yeniden ölç.

---

## Adım 8 — Serbest cümleyle çalışan araç

Parçaları birleştiriyoruz: kullanıcı bir cümle yazar, model karar verir, program uygular.

```python
for tur in range(3):
    istek = input("Ne istiyorsun? (bitirmek için boş bırak) ")
    if istek == "":
        print("Boş istek, duruyorum")
        break
    karar = karar_ver(istek, yeni_araclar)
    uygula(karar, f"istek_{tur}.jpg")
```

- Her döngünün bir **durma koşulu** olmalı. Burada iki tane var: `range(3)` en fazla 3 tur (Konu 9'daki `MAKS_URETIM`
  gibi bir sınır); boş bırakıp Enter'a basarsan `break` döngüyü bitirir.
- `input` kutusuna kendi isteğini Türkçe yaz. Her tur bir karar ve bir görsel demek.
- Dosya adına tur numarası yazılıyor: `istek_0.jpg`, `istek_1.jpg`, `istek_2.jpg` (sayma 0'dan başlıyor).
- Adım 7'deki `yeni_araclar` tarifini kullanıyor.

`ciktilar/` klasörüne bak. Model senin cümlelerinde doğru aracı seçti mi?

Bu döngüde her turdan sonra karar yine **senin** elinde: yeni bir cümle yazıyorsun ya da duruyorsun. Gerçek
"ajanlarda" aracın sonucu modele geri gider ve model bir sonraki adıma kendisi karar verir; sonucu beğenmezse yeniden
düzenler, yine beğenmez... Durma koşulu olmayan böyle bir döngü kotayı bitirene kadar dönebilir. O yüzden ilk yazılan
satır hep sınırdır.

---

## Bonus — Gerçek `tools` alanı (hoca gösterimi)

Adım 4'te kararı bir JSON alanı olarak **kendimiz** istedik. Modeller bunun standart bir yolunu da sunar: araçlar
gövdedeki `tools` alanında tanımlanır, model cevabında `tool_calls` (araç çağrıları) listesi döner.

```python
yonerge_alani = {"type": "string", "description": "görsel modeline gidecek kısa İngilizce yönerge"}
bilgiler = {"yonerge": yonerge_alani}
parametreler = {"type": "object", "properties": bilgiler, "required": ["yonerge"]}

uret_araci = {"name": "uret", "description": "Sıfırdan yeni bir görsel üretir.", "parameters": parametreler}
duzenle_tarifi = "Elimizdeki fincan fotoğrafını değiştirir; yalnızca kullanıcı o görseli işaret ediyorsa."
duzenle_araci = {"name": "duzenle", "description": duzenle_tarifi, "parameters": parametreler}
```

- Her aracın bir adı (`name`), bir tarifi (`description`) ve aldığı bilgiler (`parameters`) var.
- Bilgilerin biçimi iç içe sözlükler; her katmanı ayrı satırda kuruyoruz. İki aracımız da aynı bilgiyi alıyor: `yonerge`.
- Adım 7'deki ders burada da geçerli: `description` bir brif. Muğlaksa model yanlış aracı seçer.

```python
mesaj = {"role": "user", "content": "şu fincan fotoğrafının arka planını sadeleştir"}
govde = {"messages": [mesaj], "tools": [uret_araci, duzenle_araci]}
cevap = requests.post(metin_adresi, headers=basliklar, json=govde, timeout=60)
print(cevap.status_code)

yanit = cevap.json()
sonuc = yanit["result"]
if "tool_calls" in sonuc:
    cagrilar = sonuc["tool_calls"]
    ilk_cagri = cagrilar[0]
    print("Model şunu çağırmak istiyor:", ilk_cagri["name"])
    print("Bilgiler:", ilk_cagri["arguments"])
else:
    print("Araç çağrılmadı; model şunu yazdı:", sonuc["response"])
```

- Soru bu kez `prompt` ile değil, sohbet biçiminde (`messages`) gidiyor: bir mesaj listesi; her mesajın bir rolü
  (`user`: kullanıcı) ve içeriği var.
- Model araç çağırmaya karar verirse `tool_calls` gelir; ilk çağrının adı (`name`) ve bilgileri (`arguments`)
  yazdırılır. Karar vermezse cevabı metin olarak yazdırıyoruz.
- Fikir Adım 4'tekiyle aynı: model aracı **seçer**, çalıştıran yine biziz.

Gerçek ajanlarda bundan sonra aracın sonucu ("görseli kaydettim") yeni bir mesaj olarak modele geri gönderilir ve
model bir sonraki adıma karar verir: **çağrı döngüsü**. Bu döngüye de Adım 8'deki gibi bir sınır konur.

---

## Defterin bölümleri

| Adım | Ne yaptık | Elimizde ne oluştu | Anahtar |
|---|---|---|---|
| Isınma | İsteklere kendimiz etiket verdik | `istekler`, `etiketlerim` | gerekmez |
| 1 | Araçlar, metin modelinin adresi, elimizdeki görsel | `ciz`, `duzenle`, `metin_adresi` | gerekir |
| 2 | JSON modu: alanları belli cevap | `bicim`, `json_sor` | gerekir |
| 3 | Beş slogan kartı; süzmek; alanın değerini sınırlamak | `kartlar` | gerekir |
| 4 | Araç tarifi; kararı bir alan olarak istemek | `araclar`, `karar_ver`, `karar` | gerekir |
| 5 | Program kararı uygular | `uygula`, `ciktilar/karar_1.jpg`, `ciktilar/karar_2.jpg` | gerekir |
| 6 | Kararların doğruluğu | `olc` | gerekir |
| 7 | Tarifi netleştirmek; yeni isteklerle ölçmek | `yeni_araclar`, `yeni_istekler` | gerekir |
| 8 | Serbest cümleyle çalışan araç; durma koşulu | `ciktilar/istek_0.jpg` ... | gerekir |
| Bonus | Gerçek `tools` alanı | `uret_araci`, `duzenle_araci` | gerekir |

Derste kendi başına çalışacağın defter: `alistirma.ipynb`. Önce aynı klasörde yeni bir adla kopyala, kopyada çalış.
**Anahtar istemez ve internete çıkmaz:** modelin kararları `veri/kararlar.json` dosyasında hazır (el yapımı örnekler).
İki bölümü var:

- **Bozuk kodlar:** beş kısa hücre, birbirinden bağımsız. İkisi hata mesajı veriyor, üçü sessizce yanlış sonuç yazıyor.
- **Kendi başına:** `BOSLUK` yazan yerleri doldurduğun altı soru ve iki ek soru (araç sayacı; kendi muğlak isteğin).

---

## Sık karşılaşılan hatalar ve mesajlarını okumak

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `ModuleNotFoundError: No module named 'gorsel_araclari'` | Defterin kopyası konu klasörünün dışında | Kopya `gorsel_araclari.py`'nin yanında, `12-arac-kullanimi` klasöründe olmalı |
| `FileNotFoundError: [Errno 2] No such file or directory: '../anahtar.txt'` (Adım 1) | Anahtar dosyası yok ya da yanlış yerde | `gita3111` klasöründe durmalı; sonra Adım 1'in ilk hücresini yeniden çalıştır |
| `KeyError: 'ACCOUNT_ID'` (Adım 1) | `anahtar.txt`'de `=` yerine `:` ya da satır eksik | Satırlar `AD = değer` biçiminde olmalı |
| `NameError: name 'adres' is not defined` | Adım 1'in ilk hücresi hata verdi ya da çalıştırılmadı | Önce o hücredeki hatayı düzelt |
| `401` ya da `İstek başarısız, durum kodu: 401` | Anahtar yanlış | `anahtar.txt`'yi düzelt, çekirdeği yeniden başlat (**Restart**), baştan çalıştır |
| Adım 2'de `200` dışında bir kod | Model istenen biçime uyamadı ya da kota/hız sorunu | Hücreyi bir kez daha çalıştır; `429` ise bekle |
| `TypeError: string indices must be integers, not 'str'` (Adım 2) | `sonuc["response"]` sözlük değil metin olarak geldi | Hocaya söyle: cevabı sözlüğe çeviren tek bir satır eklenecek |
| `TypeError: 'NoneType' object is not subscriptable` | `json_sor` `None` verdi: istek başarısız | Üstteki `İstek başarısız, durum kodu` satırına bak |
| `KeyError: 'ton'` ya da `KeyError: 'arac'` | Model istenen alanı yazmadı ya da başka adla yazdı (`"tool"`, `"araç"`) | `print(kart)` ya da `print(karar)` ile cevaba bak; hücreyi yeniden çalıştır |
| `Bilinmeyen araç: ...` | Model listede olmayan bir ad yazdı | `else` dalı çalıştı: doğru davranış. Tarifi netleştir (Adım 7) |
| `Görsel yok`, ardından `AssertionError` | Görsel üretilemedi; gösterilecek dosya yok | Üstteki durum koduna bak; hücreyi yeniden çalıştır |
| `NameError: name 'karar_ver' is not defined` | Adım 4'ün fonksiyon hücresi çalıştırılmadı | Adım 4'ü çalıştır |
| `NameError: name 'klasor' is not defined` | Adım 5'in ilk hücresi çalıştırılmadı | O hücreyi çalıştır |
| `IndexError: list index out of range` (Adım 6) | Etiket listesi istek listesinden kısa | Her isteğe bir etiket: `print(len(istekler), len(etiketlerim))` aynı sayıyı yazmalı |
| `Doğru` sayısı beklenmedik (ör. 0 ya da 1) | `sira = sira + 1` döngünün dışında ya da `dogru = 0` döngünün içinde | Alıştırmanın 4. ve 5. bozuk kodu |
| Etiketin `"üret"` (ü ile) | Etiketler model adlarıyla birebir aynı olmalı | `"uret"`, `"duzenle"`: Türkçe karakter yok |
| Adım 8'de hücre bitmiyor | `input` kutusu senin cevabını bekliyor | Kutuya yaz ya da boş bırakıp Enter |
| `Bağlanamadım` ya da `ReadTimeout` | İnternet yok ya da sunucu cevap vermedi | İnternete bak; hücreyi yeniden çalıştır |

---

## Kendini dene

Cevaplar notun en sonunda. Önce kendin düşün.

1. Konu 2'deki cevapla bugünkü JSON cevabı arasındaki fark ne? Program için neden önemli?
2. `ton` alanını neden "yalnızca samimi, resmi ya da esprili" diye sınırladık? Bir arayüz tasarımında karşılığı ne?
3. Adım 5'te model bir şey çizdi mi? Görseli kim üretti?
4. `uygula`'daki `else` dalını silersen ve model `"üret"` yazarsa ne olur?
5. Model altı istekten dördünde seninle aynı fikirde. Doğruluk kaç? Bu sayı modelin "iyi" olduğunu mu gösterir?
6. Tarifi altı isteğe bakarak düzelttin, doğruluk 6/6 oldu. Neden yeni isteklerle de ölçmelisin?
7. Bir arkadaşın "yalnızca görsel üretiyorum, düzenleme yok" diyor. Araç kullanımı ona ne kazandırır?
8. Adım 8'deki döngüde `range(3)` olmasaydı ve `input` yerine model kendi sonucuna bakıp karar verseydi ne olabilirdi?

---

## Bu konuda öğrendiklerin

- **Yapılandırılmış çıktı.** `response_format` ile cevap bir paragraf değil, alanları belli bir sözlük olur; program
  onu okuyabilir, süzebilir.
- **Alanı sınırlamak.** Serbest alanın değerleri dağılır; değerleri soruda bir listeyle sınırlamak açılır menü gibidir.
- **Karar da bir alan.** Model `arac` ve `yonerge` alanlı bir karar gönderir; çizen, düzenleyen bizim fonksiyonumuz.
- **Kararı görünür kılmak.** Modelin seçtiğini her zaman ekrana yazdır; bilinmeyen bir ada karşı `else` koy.
- **Ölçmek.** Elle etiketlenmiş istekler bir test verisidir; doğruluk = doğru / toplam. Ayrışan isteklere bak.
- **Tarif bir brif.** Muğlak tarif yanlış seçim getirir; tarifi netleştir, yeni isteklerle yeniden ölç.
- **Durma koşulu.** Her döngüye bir sınır; karar modelde olunca daha da gerekli.

## Bu konunun tek cümlesi

> Modelden alanları belli bir cevap isteyebilirsin; "hangi aracı çağırayım" kararı da böyle bir cevaptır: program
> kararı uygular, ama kararın kalitesi araçları ne kadar net tarif ettiğine bağlıdır.

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **Yapılandırılmış çıktı** | Modelin serbest metin yerine alanları belli bir cevap (ör. JSON sözlüğü) vermesi |
| **JSON modu (`response_format`)** | Cloudflare'de cevabı JSON olarak isteme yolu: `{"type": "json_object"}` |
| **Alan** | Sözlükteki bir anahtar ve değeri: `"ton": "samimi"` |
| **Araç (tool)** | Modele tanıttığımız, adı ve ne yaptığı belli bir fonksiyon (`ciz`, `duzenle`) |
| **Araç tarifi** | Modele araçların ne yaptığını ve ne zaman seçileceğini anlatan metin; bir brif |
| **Karar** | Modelin `arac` ve `yonerge` alanlı cevabı |
| **Ajan** | Kararı modelin verdiği, uygulamayı programın yaptığı; çoğu zaman bunu döngüde tekrarlayan program |
| **Doğruluk** | Doğru karar sayısı / toplam karar (Konu 3) |
| **Test verisi** | Doğru cevabı insanın verdiği, ölçüm için ayrılmış örnekler (Konu 3) |
| **Durma koşulu** | Döngüyü bitiren kural: tur sınırı, boş istek, "bitti" kararı |
| **Çağrı döngüsü** | Aracın sonucunun modele geri verildiği, modelin bir sonraki adıma karar verdiği döngü |
| **`tools` / `tool_calls`** | Araçları modele tanımanın standart alanı / modelin cevabındaki araç çağrıları |

## Ödev

`odevler/odev12.md` (puansız): kendi projene üçüncü bir araç (`metin_yaz`) ekle; en az 6 istekle modelin üç araç
arasından doğru seçip seçmediğini ölç; bir tarifi düzeltip yeniden ölç (en az 3 yeni istekle).

## Sonraki konu

**Konu 13 — Final atölyesi ve sunum.** Yeni kavram yok. Dönem boyunca öğrendiklerini kendi projende bir araya
getireceksin: önce çekirdeği (girdi → en az bir görsel) çalıştır, sonra anlatılabilir hâle getir. Bugünkü araç
kullanımı final projesi için **zorunlu değil**; kullanırsan ekstra sayılır.

---

## Kendini dene — cevaplar

1. Konu 2'de `sonuc["response"]` bir metindi: insan okur ama program içinden "tonu" çekip alamaz. Bugün bir sözlük:
   `kart["ton"]` ile alana adıyla erişilir, süzülür, tabloya dökülür.
2. Serbest alanda model aynı şeyi farklı yazar ("samimi", "Samimi", "sıcak"); süzgeç bunları farklı sayar. Değerleri
   sınırlamak bir formda serbest metin kutusu yerine açılır menü koymak gibidir: herkes aynı seçeneklerden birini yazar.
3. Hayır. Model yalnızca bir sözlük gönderdi (`arac`, `yonerge`). Görseli `uygula`'nın çağırdığı `ciz` ya da
   `duzenle` üretti.
4. `if` ve `elif`'in ikisi de tutmaz; `resim` hiç tanımlanmamış olur ve `if resim is None:` satırında
   `UnboundLocalError: cannot access local variable 'resim' where it is not associated with a value` alırsın. Hata
   mesajı asıl sorunu (bilinmeyen araç adı) söylemez. `else` bu yüzden var: bilinmeyen adı yakalar ve söyler.
5. 4 / 6 ≈ 0,67. Tek başına bir şey söylemez: altı istek çok az, ve ayrışılan istekler belki iki türlü okunabiliyor
   (sorun istekte ya da tarifte olabilir). Konu 3'teki gibi: sayıya değil, ayrışılan örneklere bak.
6. Tarifi o altı isteğe göre ayarladın; aynı isteklerle ölçmek ezberi ölçer (Konu 3: test sonucuna bakıp ayar
   yapmak). Tarifin işe yarayıp yaramadığını yalnızca görülmemiş istekler gösterir.
7. Büyük ihtimalle hiçbir şey. Tek bir aracı olan, tek adımlı bir işte karar zaten belli; araç kullanımı yalnızca bir
   istek, biraz gecikme ve bir hata ihtimali ekler. Araç kullanımı birden çok seçenek ve gerçek bir karar olduğunda
   anlamlı.
8. Model sonucu beğenmeyip yeniden düzenleyebilir, yine beğenmeyebilir: döngü durmadan döner, her tur kota harcar.
   Tur sınırı (`range(3)`) bu yüzden ilk yazılan satır olmalı.
