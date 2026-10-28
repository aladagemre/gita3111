# Konu 12 — Ajan: Kararı Modele Bırakmak

Bu not konunun özetidir; derste çalıştırdığımız `ders.ipynb` defteriyle **aynı sırada**
ilerler: Isınma, sonra Adım 1–9 ve üç parçalı bir Bonus. Derste kaçırdığın bir yer olursa
buradan oku, sonra defterde o adımın hücrelerini çalıştır. Nottaki kod blokları
defterdeki hücrelerin birebir aynısı.

**Konu 10'da:** hattın adımlarını ve sırasını sen yazdın. **Konu 11'de:** modele bir belgeyi okuttun; hangi paragrafların
gideceğini senin programın seçti. **Bu konuda:** sırayı modele bırakıyoruz:

> Modelin elinde üç araç var: görsel çizmek, fotoğraf düzenlemek, Sayfa Kahve'nin marka kılavuzunda aramak. Kullanıcı bir
> cümle yazar; hangi araçların, hangi bilgilerle, hangi sırayla çalışacağını model seçer. Araçları çalıştıran yine
> bizim programımız. Bu düzene **ajan** denir.

Önce bu işin bir turunu **elle**, çerçevesiz yapıyoruz (Adım 2–4): araç tarifi, istekte `tools`, cevapta `tool_calls`,
aracı çalıştıran program. Sonra aynı işi **Agno** adlı bir ajan çerçevesiyle kuruyoruz (Adım 5–9) ve çerçevenin bizim
yerimize ne yaptığını görüyoruz.

**Konunun sonunda elinde:** üç (sonra dört) araçlı bir ajan; kılavuza bakarak çizdiği afişler; kendi yazdığın bir aracın
tarifi. Bonus'ta bir ajan çalıştırmasının modele kaç istek gönderdiğini ve ne kadar kota harcadığını da hesaplıyorsun.

**Kurulum:** `git pull` ile konu klasörü geldikten sonra `gita3111` klasöründe bir kez `uv sync` çalıştır. Bu konunun iki
yeni kütüphanesi böylece kurulur: `agno` (ajan çerçevesi) ve `openai`. Adı yanıltmasın: `openai` yalnızca isteğin
biçimini kuran paket; istekler Cloudflare'e gider, OpenAI hesabı da ödemesi de gerekmez (Adım 5).

**Anahtar:** Isınma anahtarsız. Adım 1 ve sonrası `anahtar.txt` ister (Konu 2'deki dosya, `gita3111` klasöründe).
Defterin tamamı (Bonus dahil) metin ve arama modellerine yaklaşık 30 istek gönderir ve 10 kadar görsel üretir ya da
düzenler; günlük ücretsiz kotanın %10'undan az.

> **Bu nottaki çıktılar hakkında.** Isınma'nın çıktısı her bilgisayarda aynıdır. Modelin kararları, yazdığı yönergeler,
> son cevapları ve görseller gerçek modelden gelir; senin ekranında farklı olur. Notta "senin çıktına bak" dediğimiz
> yerlerde cevabı biz de bilmiyoruz.

---

## Isınma: ajanı önce sen oyna

Model araçları yalnızca adlarından ve kısa tariflerinden tanıyacak. Senin elinde de şimdilik yalnızca bu var:

```python
tarifler = {
    "afis_ciz": "Sıfırdan yeni bir görsel çizer: afiş, menü kapağı, ilan.",
    "fotograf_duzenle": "Var olan bir fotoğraf dosyasını yönergeye göre değiştirir.",
    "kilavuzda_ara": "Sayfa Kahve'nin marka kılavuzunda arar: renkler, yazı tipleri, ses tonu, yasak sözcükler.",
}

for ad in tarifler:
    print(ad, ":", tarifler[ad])
```

Çıktı: üç satır, her biri `ad : tarif` (ör. `afis_ciz : Sıfırdan yeni bir görsel çizer: afiş, menü kapağı, ilan.`).

- Sözlüğü `for ad in tarifler` ile geziyoruz: `ad` sırayla her anahtar, `tarifler[ad]` onun değeri (Konu 1).

Sonra beş istek ve her biri için bir plan:

```python
istekler = [
    "kafeye bir afiş yap",
    "veri/fincan.jpg fotoğrafının arka planını sadeleştir",
    "Sayfa Kahve hafta sonu kaçta açılıyor?",
    "Sayfa Kahve için kılavuza uygun bir afiş yap",
    "afişi Instagram'da paylaş",
]
planim = [
    ["afis_ciz"],
    ["fotograf_duzenle"],
    ["kilavuzda_ara"],
    ["kilavuzda_ara", "afis_ciz"],
    [],
]

sira = 0
for istek in istekler:
    print(istek, "->", planim[sira])
    sira = sira + 1
```

Çıktı: beş satır, her biri `istek -> plan` (ör. `Sayfa Kahve için kılavuza uygun bir afiş yap -> ['kilavuzda_ara', 'afis_ciz']`).

- `planim`'in her elemanı bir liste: içinde araç adları, çalışacakları sırayla. Boş liste (`[]`) "hiçbir araç".
- İki listeyi aynı anda gezmek için bir **sıra sayacı** tutuyoruz: `sira` 0'dan başlar, her turda bir artar;
  `planim[sira]` o sıradaki istek için plan.
- Dördüncü istekte sıra önemli: kılavuza bakmadan çizilen afiş kılavuza ancak şans eseri uyar.
- Beşinci istek ("afişi Instagram'da paylaş") için elimizde araç yok. Doğru davranış, bunu yapamayacağını söylemek:
  ajan, verdiğin araçlar kadar iş yapabilir. Modelin gerçekte ne yaptığına Bonus 2'de bakıyorsun.
- Ajana derste birinci ve dördüncü isteği veriyoruz (Adım 6 ve 7); öbürleri Bonus 2'de.

---

## Adım 1 — Hazır parçalar

```python
import requests
import matplotlib.pyplot as plt
from ajan_araclari import hesap, anahtar, basliklar, adres
from ajan_araclari import ciz, duzenle, en_yakin_paragraflar, modele_sor, tarifi_goster
```

- `ajan_araclari.py` bu klasördeki yardımcı dosya. Araçların **içinde** çalışacak hazır fonksiyonlar orada:
  - `ciz(yonerge, tohum, yol)`: Konu 8'deki fonksiyon; görseli `yol`a kaydeder, başarılıysa yolu, değilse `None` verir.
  - `duzenle(girdi_yolu, yonerge, tohum, yol)`: var olan bir görseli yönergeye göre değiştirir. Konu 7'deki `duzenle`;
    bu kez tohumu ve kayıt yolunu da sen veriyorsun. `ciz` gibi kaydeder. Girdi dosyası yoksa istek göndermez,
    `Böyle bir dosya yok` yazar.
  - `en_yakin_paragraflar(soru, kac)`: Konu 11'deki `kilavuzda_ara`'nın içindeki iş. Sorunun vektörünü kılavuz
    paragraflarının vektörleriyle karşılaştırır, soruya en yakın paragrafları tek bir metin olarak verir. Tek fark: kaç
    paragraf geleceğini `kac` ile sen söylüyorsun. `kilavuzda_ara`'nın kendisini Adım 5'te araç olarak, aynı adla
    yeniden yazıyoruz.
  - `modele_sor(soru, sicaklik)`: Konu 5'te yazdığın fonksiyon.
  - `tarifi_goster(fonksiyon)`: Agno'nun bir fonksiyondan kuracağı araç tarifini yazdırır (Adım 5).
- Anahtarı `../anahtar.txt`'den yardımcı dosya kendisi okur; bu hücre ilk çalıştığında, bir kez. `anahtar.txt`'yi
  sonradan düzeltirsen çekirdeği yeniden başlat (**Restart**).
- `import` satırı uzun olmasın diye ikiye bölündü; ikisi de aynı dosyadan alıyor.

```python
def goster(yol):
    resim = plt.imread(yol)
    plt.imshow(resim)
    plt.axis("off")
    plt.show()

goster("veri/fincan.jpg")
```

Çıktı: fincan fotoğrafı.

- Bugün çok görsel açacağız; Konu 8'deki dört satırı (`imread`, `imshow`, `axis`, `show`) bir fonksiyona koyduk.

```python
bulunan = en_yakin_paragraflar("logonun çevresinde ne kadar boşluk bırakılır?", 2)
print(bulunan)
```

Çıktı: kılavuzdan iki paragraf, senin ekranında. Logonun çevresindeki boşluğu anlatan paragraf aralarında mı?

- `2`: en yakın iki paragraf. İlk çalıştırmada kılavuzun 14 paragrafı vektöre çevrilir ve Konu 11'deki gibi
  `ciktilar/kilavuz_vektorleri.json` dosyasına saklanır (Konu 10'daki "ara çıktıyı sakla" fikri); sonraki aramalarda
  yalnızca sorunun vektörü istenir.
- Bu fonksiyon birazdan bir aracın içinde çalışacak: model kılavuz aracını seçince bu metin ona gidecek.

---

## Adım 2 — Araç tarifi, elle

```python
yonerge_alani = {"type": "string", "description": "kısa, İngilizce bir yönerge"}
alanlar = {"yonerge": yonerge_alani}
parametreler = {"type": "object", "properties": alanlar, "required": ["yonerge"]}

ciz_aciklamasi = "Sıfırdan yeni bir görsel çizer: afiş, menü kapağı, ilan."
ciz_tarifi = {"name": "ciz", "description": ciz_aciklamasi, "parameters": parametreler}

duzenle_aciklamasi = "Elimizdeki tek fotoğrafı, veri/fincan.jpg dosyasını, yönergeye göre değiştirir."
duzenle_tarifi = {"name": "duzenle", "description": duzenle_aciklamasi, "parameters": parametreler}

print(duzenle_tarifi)
```

Çıktı: `duzenle_tarifi` sözlüğü: `{'name': 'duzenle', 'description': 'Elimizdeki tek fotoğrafı, ...', 'parameters': {...}}`.

- Her aracın üç parçası var:
  - `name`: aracın adı. Model kararını bu adla bildirecek.
  - `description`: aracın ne yaptığını anlatan cümle, kısaca **tarifi**. Model aracın ne işe yaradığını yalnızca bu
    cümleden öğrenir.
  - `parameters`: aracın aldığı bilgiler. `"type": "string"` bilginin **metin** olduğunu, `"required"` zorunlu olduğunu
    söyler. Tek bilgi var: `yonerge`. Bilginin kendi kısa tarifi de var (`yonerge_alani`'ndaki `description`): modele bu
    alana ne yazacağını anlatır. Dıştaki `"type": "object"` ve `"properties"` her araçta aynı kalan kalıp:
    "bilgiler bir sözlük olarak gelecek, işte alanları".
- Üç parçanın bütününe **araç tarifi** diyoruz (`ciz_tarifi`, `duzenle_tarifi`).
- İç içe sözlükleri en içten başlayarak, her katmanı ayrı satırda kuruyoruz: önce bir bilginin tarifi
  (`yonerge_alani`), sonra bilgiler (`alanlar`), sonra bilgilerin kalıbı (`parametreler`), en son araç.
- İki aracın adı yardımcı dosyadaki fonksiyonların adıyla aynı: `ciz` ve `duzenle`. Model fonksiyonları görmez; yalnızca
  bu tarifleri görür.
- İki araç aynı `parametreler` sözlüğünü kullanıyor: ikisi de yalnızca bir yönerge alıyor. Düzenlenecek dosyayı
  tarifte söylüyoruz: elimizde tek fotoğraf var.

---

## Adım 3 — İstekte `tools`, cevapta `tool_calls`

```python
MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
metin_adresi = adres(MODEL)

mesaj = {"role": "user", "content": "veri/fincan.jpg fotoğrafının arka planını sadeleştir"}
govde = {"messages": [mesaj], "tools": [ciz_tarifi, duzenle_tarifi]}
cevap = requests.post(metin_adresi, headers=basliklar, json=govde, timeout=60)
print(cevap.status_code)
```

Çıktı: `200`.

- Soru bu kez `prompt` ile değil, sohbet biçiminde (`messages`) gidiyor: bir mesaj listesi; her mesajın bir rolü
  (`user`: kullanıcı) ve içeriği (`content`) var.
- Araç tarifleri `tools` alanında, bir liste olarak. Model, Konu 2'den beri kullandığımız llama.
- `adres(MODEL)` Konu 2'deki adresi kurar; ayrı bir satırda, çünkü `requests.post`'un içine ikinci bir fonksiyon
  çağrısı koymuyoruz.

```python
yanit = cevap.json()
print(yanit)
```

Çıktı: yanıtın bütünü, senin ekranında. `result`'ın içinde modelin yazdığı bir cümle var mı? Konu 2'de görmediğin alan
hangisi?

- Konu 2'deki kural: yapısını bilmediğin bir yanıtın önce **bütününe** bak, sonra kat kat in.
- Yeni alan `tool_calls`: model bir metin yazmak yerine bir **araç çağrısı** gönderdi.

```python
sonuc = yanit["result"]
cagrilar = sonuc["tool_calls"]
cagri = cagrilar[0]
print("Model şunu çağırmak istiyor:", cagri["name"])
print("Bilgiler:", cagri["arguments"])
```

Çıktı: modelin seçtiği araç ve bilgileri, ör. `Model şunu çağırmak istiyor: duzenle` ve
`Bilgiler: {'yonerge': '...'}`. Hangi aracı seçtiğine ve yönergeyi hangi dilde yazdığına senin çıktında bak.

- `tool_calls` bir liste. Her çağrının bir adı (`name`) ve modelin doldurduğu bilgileri (`arguments`, bir sözlük) var.
- Katmanları tek tek açıyoruz: `result` → `tool_calls` (liste) → ilk eleman `[0]` (sözlük).
- Model hiçbir şey çizmedi, hiçbir dosyaya dokunmadı. Yalnızca "şu aracı, şu bilgiyle çalıştır" diyen bir sözlük
  gönderdi.
- Konu 5'te sonraya bıraktığımız **yapılandırılmış çıktı** bu: serbest bir cümle değil, alanları belli bir cevap.
  Programımız onu metin gibi okumaz, sözlük gibi doğrudan kullanır (Adım 4).

---

## Adım 4 — Aracı çalıştıran program

```python
ad = cagri["name"]
bilgiler = cagri["arguments"]
yonerge = bilgiler["yonerge"]

if ad == "ciz":
    yol = ciz(yonerge, 42, "ciktilar/elle_cizim.jpg")
elif ad == "duzenle":
    yol = duzenle("veri/fincan.jpg", yonerge, 42, "ciktilar/elle_duzenleme.jpg")
else:
    print("Listede olmayan bir araç:", ad)
    yol = None

print("Sonuç:", yol)
```

Çıktı: `Sonuç: ciktilar/elle_duzenleme.jpg` (model `duzenle`'yi seçtiyse) ya da `Sonuç: ciktilar/elle_cizim.jpg`.

- Kararı uygulayan **bizim programımız**: adı okuyor, doğru fonksiyonu çağırıyor. Modelin yazdığı yönerge
  `bilgiler["yonerge"]`; tohumu (`42`) ve dosya yollarını biz veriyoruz.
- `else` dalı bir **güvenlik ağı**: model listede olmayan bir ad yazarsa (`"edit"`, `"üret"`) program yanlış bir şey
  çalıştırmaz, `Listede olmayan bir araç` yazar. Modelin cevabına körü körüne güvenme.

```python
goster(yol)
```

Çıktı: düzenlenmiş fincan ya da yeni görsel. (`Sonuç: None` yazdıysa bu hücre hata verir; üstteki mesaja bak.)

Kararı model verdi, işi program yaptı. Ama model sonucu hiç görmedi. Bir **ajan** burada durmaz:

1. Aracın sonucu ("görsel şuraya kaydedildi") yeni bir mesaj olarak modele geri gönderilir.
2. Model sonuca bakıp yeniden karar verir: başka bir araç mı, yoksa kullanıcıya cevabını mı yazacak?
3. Yeni bir araç isterse program onu da çalıştırır, sonucu yine geri gönderir...
4. ...ta ki model cevabını yazana ya da bir **sınıra** ulaşılana kadar.

Bu döngüyü elle yazmak uzun iş: her turda mesaj listesini büyütmek, her aracı adına göre çalıştırmak, sınırı saymak.
**Ajan çerçeveleri** bu işi üstlenir.

---

## Adım 5 — Agno: model ve araçlar

```python
from agno.agent import Agent
from agno.models.openai.like import OpenAILike

taban_adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/v1"
model = OpenAILike(id="@cf/google/gemma-4-26b-a4b-it", api_key=anahtar, base_url=taban_adres)
```

Çıktı yok.

- `Agent` ajanın kendisi; `OpenAILike` ajanın istek göndereceği model.
- Adı yanıltmasın: `openai` paketi ve `OpenAILike` ("OpenAI'ye benzeyen") yalnızca isteğin **biçiminin** adı. Birçok
  sağlayıcı bu biçimi kullanır. İstek Cloudflare'e gidiyor, model Cloudflare'in ücretsiz modeli; OpenAI hesabı da
  ödemesi de gerekmiyor.
- `base_url` Cloudflare'deki hesabının bu biçimi kabul eden adresi: Konu 2'deki adresin `ai/run/...` yerine `ai/v1` ile
  biten hâli. Model adı adreste değil, `id`'de.
- Model de değişiyor: llama yerine Google'ın `gemma-4` modeli (Konu 8'in Bonus'unda görselleri okuyan model). Adım 3'te
  llama yeterliydi: tek bir istekti ve cevabını Konu 2'deki `result` biçiminde kendimiz okuduk. Ajanda ise model bir
  döngü içinde karar veriyor; hocanın denemesinde llama aynı aracı gereksiz yere birkaç kez çağırdı, gemma her aracı
  bir kez.

Üç araç, üç fonksiyon:

```python
def afis_ciz(yonerge: str) -> str:
    """Sıfırdan yeni bir görsel çizer: afiş, menü kapağı, ilan. Yönerge İngilizce bir görsel tarifi olmalı."""
    print("afis_ciz çalıştı:", yonerge)
    yol = ciz(yonerge, 42, "ciktilar/afis.jpg")
    if yol is None:
        return "Görsel çizilemedi."
    return "Görsel kaydedildi: " + yol
```

```python
def fotograf_duzenle(dosya: str, yonerge: str) -> str:
    """Var olan bir fotoğraf dosyasını değiştirir. dosya: fotoğrafın yolu, ör. veri/fincan.jpg. Yönerge İngilizce olmalı."""
    print("fotograf_duzenle çalıştı:", dosya, "|", yonerge)
    yol = duzenle(dosya, yonerge, 42, "ciktilar/duzenlenmis.jpg")
    if yol is None:
        return "Fotoğraf düzenlenemedi."
    return "Düzenlenmiş fotoğraf kaydedildi: " + yol
```

```python
def kilavuzda_ara(soru: str) -> str:
    """Sayfa Kahve'nin marka kılavuzunda arar ve soruyla en ilgili üç paragrafı verir.
    Kılavuzda renkler, yazı tipleri, ses tonu, yasak sözcükler, logo ve fotoğraf kuralları, açılış saatleri var."""
    print("kilavuzda_ara çalıştı:", soru)
    return en_yakin_paragraflar(soru, 3)
```

Çıktı yok: üç hücre yalnızca fonksiyonları tanımlar.

- Her biri yardımcı dosyadaki bir fonksiyonu saran küçük bir fonksiyon. Neden sarıyoruz? Modelin yalnızca **karar
  vermesi gereken** bilgileri doldurmasını istiyoruz: yönergeyi (ve düzenlemede dosyayı) model yazsın, tohumu ve kayıt
  yolunu biz verelim.
- `yonerge: str` bir **tür ipucu**: "bu bilgi metin" (`str`, Python'da metnin türü). Adım 2'de elle yazdığın
  `"type": "string"`'in Python'daki karşılığı. `-> str` "bu fonksiyon metin verir" demek. Python tür ipucunu denetlemez;
  Agno okuyup modele iletir.
- `def` satırının hemen altındaki, üç tırnakla (`"""`) açılıp kapanan metin bir **docstring**: fonksiyonun tarifi.
  Üç tırnak arasındaki metin birkaç satıra yayılabilir. Agno aracın tarifini (`description`) buradan okur. Docstring
  `def`'in hemen altında, fonksiyonun **ilk** satırı olmalı; araya başka bir satır girerse tarif olmaktan çıkar
  (alıştırmanın 4. bozuk kodu).
- `return` ettiğimiz metin modele geri gider; model sonraki kararını ona bakarak verir. `print` yalnızca bize: aracın ne
  zaman, hangi bilgiyle çalıştığını ekranda görelim diye.
- Görsel çizilemezse `ciz` `None` verir; araç bunu modele bir cümleyle söylüyor (`Görsel çizilemedi.`).
- Araçların adı fonksiyonların adı: `afis_ciz`, `fotograf_duzenle`, `kilavuzda_ara`. `ciz` ve `duzenle` adlarını
  yardımcı dosya zaten kullanıyor; aynı adı verseydik yardımcı fonksiyonun üzerine yazardık.
- Üçüncü araç Konu 11'deki `kilavuzda_ara`: aynı ad, aynı iş. Soruyu alır, kılavuzun en ilgili üç paragrafını tek bir
  metin olarak verir. Farkı, artık bir araç olması: tür ipuçları ve tarifi var; içinde `en_yakin_paragraflar` çalışıyor.

```python
tarifi_goster(fotograf_duzenle)
```

Çıktı: Agno'nun modele göndereceği tarif:

```
{
  "name": "fotograf_duzenle",
  "description": "Var olan bir fotoğraf dosyasını değiştirir. dosya: fotoğrafın yolu, ör. veri/fincan.jpg. Yönerge İngilizce olmalı.",
  "parameters": {
    "type": "object",
    "properties": {
      "dosya": {
        "type": "string"
      },
      "yonerge": {
        "type": "string"
      }
    },
    "required": [
      "dosya",
      "yonerge"
    ]
  }
}
```

Adım 2'deki sözlüğün aynı üç parçası: `name` fonksiyonun adından, `description` docstring'den, `parameters`
fonksiyonun bilgilerinden ve tür ipuçlarından. Elle kurduğun iç içe sözlüğü Agno senin yerine kurdu.

Bir fark var: Adım 2'de `yonerge`'nin kendi tarifi vardı; burada bilgilerin yalnızca türü var. Bilgilere ne yazılacağını
bu yüzden docstring'in içinde söyledik: `dosya: fotoğrafın yolu, ör. veri/fincan.jpg`.

---

## Adım 6 — İlk ajan

```python
araclar = [afis_ciz, fotograf_duzenle, kilavuzda_ara]
ajan = Agent(model=model, tools=araclar, tool_call_limit=3, telemetry=False)
```

Çıktı yok.

- Ajan = model + araç listesi + iki ayar.
- Araçları listeye **adlarıyla**, parantezsiz yazıyoruz: fonksiyonu çalıştırmıyoruz, ajana teslim ediyoruz.
  `afis_ciz()` yazsaydın fonksiyon o anda, yönergesiz çalışırdı ve hata verirdi.
- `tool_call_limit=3`: bir çalıştırmada **en fazla 3 araç** çalışır. Sınır dolunca Agno aracı çalıştırmaz, modele
  "sınır doldu" der. Görsel kotan böyle korunur.
- `telemetry=False`: yazmazsan Agno her çalıştırmada kendi sunucusuna kullanım bilgisi gönderir. Biz göndermiyoruz;
  bugünkü her `Agent`'ta bu ayar var.

```python
cevap = ajan.run("kafeye bir afiş yap")
print(cevap.content)
```

Çıktı: modelin son cevabı, senin ekranında (ör. afişi çizdiğini ve nereye kaydettiğini söyleyen bir cümle). Hücre
çalışırken `afis_ciz çalıştı: ...` satırı da görünür: o satırı aracın içindeki `print` yazıyor. Bir çalıştırma birkaç
saniye, bazen yarım dakika sürer.

- `ajan.run` bütün döngüyü çalıştırır: isteği modele gönderir, seçilen aracı çalıştırır, sonucu modele geri gönderir,
  son cevabı alır.
- Ekranda renkli bir yazı çıkarsa Agno bir sorunu haber veriyor; hücre yine de biter. Kırmızı `ERROR`: Agno modele
  ulaşamadı ya da istek reddedildi; durum kodu bu satırda yazar (`401` anahtar, `429` kota ya da hız sınırı). Sarı
  `WARNING Could not run function ...` ve altında uzun, kırmızı bir yazı: hata **aracın içinde** (ör. yanlış yazılmış
  bir ad). Kırmızı yazının son satırı hatayı söyler (ör. `NameError`); aracın `def` hücresini düzelt, sonra araç
  listesini ve ajanı yeniden kur.

```python
def kararlari_goster(cevap):
    if cevap.tools is None:
        print("Araç kaydı yok. Ajanın son mesajı:", cevap.content)
        return
    sayi = len(cevap.tools)
    print("Çağrılan araç sayısı:", sayi)
    for cagri in cevap.tools:
        print("-", cagri.tool_name, cagri.tool_args)

kararlari_goster(cevap)
```

Çıktı: `Çağrılan araç sayısı: ...` ve her çağrı için bir satır, ör. `- afis_ciz {'yonerge': '...'}`.

- `cevap.tools`: bu çalıştırmada çağrılan araçların listesi. Her çağrının adı `tool_name`, bilgileri `tool_args`.
  Konu 2'deki `cevap.status_code` gibi **noktayla** okunuyorlar: bunlar sözlük değil, Agno'nun kendi kayıtları.
- Fonksiyonun ilk üç satırı bir güvenlik ağı: kırmızı `ERROR` çıktıysa (anahtar yanlış, kota doldu, bağlantı koptu) Agno araç
  listesini hiç kurmaz (`None`) ve `cevap.content`'e kısa bir hata metni koyar.
- Yanında değer olmayan `return` "fonksiyondan burada çık" demek: liste yoksa gezecek bir şey de yok.
- Model hiç araç çağırmadıysa liste boştur: `Çağrılan araç sayısı: 0`.

Modelin `afis_ciz`'e gönderdiği yönergeye bak. Sen dört sözcük yazdın; model ne yazdı, hangi dilde, senin söylemediğin
neleri ekledi? Kararı modele bırakınca **yönergeyi de model yazıyor**; ne yazdığını okumak senin işin.

```python
goster("ciktilar/afis.jpg")
```

Çıktı: modelin yönergesiyle çizilen afiş. (Model `afis_ciz`'i çağırmadıysa dosya yok ve hücre `FileNotFoundError`
verir; isteği yeniden çalıştır.)

---

## Adım 7 — Çok adım: sırayı model seçiyor

```python
cevap = ajan.run("Sayfa Kahve için kılavuza uygun bir afiş yap")
kararlari_goster(cevap)
```

Çıktı: kararlar, senin ekranında. Kaç araç, hangi sırayla? Isınmadaki planınla karşılaştır.

- Isınmada bu istek için iki araçlık bir plan yazdın: önce kılavuz, sonra çizim. Ajanın kodunda bu sıra hiçbir yerde
  yazmıyor; sırayı model seçiyor.
- Model `kilavuzda_ara`'ya ne sordu? `afis_ciz`'e giden yönergede kılavuzdan gelen bir şey var mı: mürekkep mavisi ve
  kâğıt beyazı, insan yüzü olmaması, risograf baskı tarzı?

```python
goster("ciktilar/afis.jpg")
```

Çıktı: afiş. Model `afis_ciz`'i çağırmadıysa bir önceki afişi görürsün: araç hep aynı dosyaya (`ciktilar/afis.jpg`)
kaydediyor.

```python
for mesaj in cevap.messages:
    print(mesaj.role, "|", mesaj.content)
    print()
```

Çıktı: bütün konuşma, mesaj mesaj. Model önce kılavuza bakıp sonra çizdiyse aşağı yukarı şöyle:

```
user | Sayfa Kahve için kılavuza uygun bir afiş yap

assistant | None

tool | (kılavuzdan üç paragraf)

assistant | None

tool | Görsel kaydedildi: ciktilar/afis.jpg

assistant | (modelin son cevabı)
```

- Agno Adım 4'ün sonundaki döngüyü bizim yerimize çalıştırdı; bütün konuşma `cevap.messages` listesinde.
- `user`: senin isteğin; `assistant`: modelin cevabı; `tool`: aracın modele geri giden sonucu.
- Araç isteyen `assistant` mesajının çoğu zaman metni olmaz (`None`): asıl içeriği araç çağrısıdır. Hangi aracı,
  hangi bilgiyle istediğini `kararlari_goster` gösterdi; burada konuşmanın sırasını görüyorsun.
- Her `assistant` mesajı modele giden ayrı bir isteğin cevabı; her istekte o ana kadarki bütün konuşma yeniden gider.
- Model kılavuza baktıysa paragraflar `tool` mesajında; afişin yönergesini yazarken bu paragraflar da modele giden
  konuşmanın içindeydi. Bu, Konu 11'deki "yalnızca şu bilgilere dayanarak" fikrinin ajan hâli; tek fark, bilgiyi ne
  zaman getireceğini modelin seçmesi.

---

## Adım 8 — Tarifi boz, düzelt

Model araçları adlarından ve tariflerinden tanıyor. Tarif kötüyse karar da kötüleşir mi? `kilavuzda_ara`'nın tarifini
bilerek tek, tembel bir cümleye indiriyoruz:

```python
def kilavuzda_ara(soru: str) -> str:
    """Arama yapar."""
    print("kilavuzda_ara çalıştı:", soru)
    return en_yakin_paragraflar(soru, 3)

araclar = [afis_ciz, fotograf_duzenle, kilavuzda_ara]
ajan = Agent(model=model, tools=araclar, tool_call_limit=3, telemetry=False)
```

Çıktı yok.

- Fonksiyonun içi aynı; yalnızca docstring değişti.
- Fonksiyonu yeniden tanımladıktan sonra araç listesini ve ajanı da **yeniden kuruyoruz**: eski liste ve eski ajan eski
  fonksiyonu tutuyor. Yalnızca `def` hücresini çalıştırıp eski ajanı kullanırsan ajan eski tarifle çalışır.

```python
cevap = ajan.run("Sayfa Kahve için bir menü kapağı çiz")
kararlari_goster(cevap)
goster("ciktilar/afis.jpg")
```

Çıktı: kararlar ve bir menü kapağı, senin ekranında. Model kılavuza baktı mı? Kapağın renkleri kılavuzdaki mürekkep
mavisi ve kâğıt beyazı mı? Kılavuzun yasakladığı bir şey (kırmızı, turuncu, insan yüzü, parlak üç boyutlu yüzey) var mı?

- İstekte "kılavuz" sözcüğü yok. Bir tasarımcı yine de önce kılavuza bakardı: Sayfa Kahve için çalışıyor.
- "Arama yapar." modele neyi, nerede aradığını söylemiyor.

Şimdi tarifi düzeltiyoruz:

```python
def kilavuzda_ara(soru: str) -> str:
    """Sayfa Kahve'nin marka kılavuzunda arar ve soruyla en ilgili üç paragrafı verir.
    Kılavuzda renkler, yazı tipleri, ses tonu, yasak sözcükler, logo ve fotoğraf kuralları, açılış saatleri var.
    Sayfa Kahve için görsel ya da metin üretmeden önce kuralları öğrenmek için mutlaka bunu kullan."""
    print("kilavuzda_ara çalıştı:", soru)
    return en_yakin_paragraflar(soru, 3)

araclar = [afis_ciz, fotograf_duzenle, kilavuzda_ara]
ajan = Agent(model=model, tools=araclar, tool_call_limit=3, telemetry=False)
```

```python
cevap = ajan.run("Sayfa Kahve için bir menü kapağı çiz")
kararlari_goster(cevap)
goster("ciktilar/afis.jpg")
```

Çıktı: yeni kararlar ve yeni kapak, senin ekranında. Karar değişti mi? Kapak değişti mi?

- İyi bir tarif iki şey söyler: araç **ne yapar** (içinde ne var) ve **ne zaman** seçilmeli. Yeni tarifin son cümlesi
  ikincisi: "Sayfa Kahve için görsel ya da metin üretmeden önce ... mutlaka bunu kullan."
- Aynı model, aynı istek, aynı fonksiyon; değişen yalnızca tarif.
- Model yanlış aracı seçtiğinde ya da gereken bir aracı atladığında ilk bakılacak yer çoğu zaman model değil, **tariftir**.
  Muğlak bir brif, ister insana ister modele verilsin, yanlış işi getirir.
- Bozuk tarifle de kılavuza baktıysa bu da bir bulgu: model aracı adına (`kilavuzda_ara`) bakarak seçmiş olabilir; ad
  da tarifin bir parçası. Ama tek denemeden emin olamayız: aynı isteği birkaç kez denemek, başka isteklerle de bakmak
  gerekir.

---

## Adım 9 — Kendi aracın: `slogan_yaz`

```python
def slogan_yaz(konu: str) -> str:
    """BURAYA TARİFİ SEN YAZ."""
    print("slogan_yaz çalıştı:", konu)
    soru = "Şu konu için Türkçe, en fazla altı sözcüklük tek bir slogan yaz. Yalnızca sloganı yaz. Konu: " + konu
    slogan = modele_sor(soru, 0.7)
    if slogan is None:
        return "Slogan yazılamadı."
    return slogan
```

Çıktı yok. Bu hücreyi **değiştirerek** çalıştır: docstring'i sen yazacaksın.

- Fonksiyonun içi hazır: Konu 5'teki `modele_sor` (llama) ile tek bir slogan istiyor. Sıcaklık 0.7: biraz çeşitlilik.
- Tırnakların arasındaki `BURAYA TARİFİ SEN YAZ.` metnini sil, kendi tarifini yaz:
  - Araç ne yapar, ne verir?
  - Ne zaman seçilmeli? (Ör. afiş için metin gerektiğinde.)
  - `konu` bilgisine ne yazılmalı? Model kılavuzdan gelen kuralları (ses tonu, yasak sözcükler) `konu`'ya
    ekleyebilir; tarifinde bunu iste.
- Baştaki ve sondaki üç tırnak kalsın; birini silersen `SyntaxError` alırsın. Tarif tek satıra sığmazsa üç tırnak
  arasında birkaç satıra yayılabilir.
- İstersen `soru` cümlesini de değiştir: sloganın biçimini (uzunluk, dil, ton) o belirliyor.

Örnek bir tarif (senin cümlelerin farklı olabilir):

```
"""Sayfa Kahve için Türkçe, kısa bir slogan yazar ve sloganı verir. Afiş ya da gönderi için metin gerektiğinde kullan.
konu: sloganın konusu ve uyması gereken kurallar, ör. kılavuzdaki ses tonu ve yasak sözcükler."""
```

```python
tarifi_goster(slogan_yaz)
```

Çıktı: Agno'nun kurduğu tarif. Yazdığın cümle `description`'da mı? (Hâlâ `BURAYA TARİFİ SEN YAZ.` görünüyorsa
`def` hücresini değiştirdikten sonra çalıştırmamışsındır.) Tarifin birkaç satıra yayıldıysa satır sonları orada `\n`
(yeni satır işareti) olarak görünür.

```python
araclar = [afis_ciz, fotograf_duzenle, kilavuzda_ara, slogan_yaz]
ajan = Agent(model=model, tools=araclar, tool_call_limit=4, telemetry=False)

istek = "Sayfa Kahve'nin yeni sessiz çalışma odası için kılavuza uygun bir slogan yaz, sonra o sloganla bir afiş çiz"
cevap = ajan.run(istek)
kararlari_goster(cevap)
print(cevap.content)
```

Çıktı: kararlar ve son cevap. Model senin aracını çağırdı mı, hangi sırayla, `konu`'ya ne yazdı?

- Dört araç, sınır 4: bu iş üç adım istiyor (kılavuz, slogan, afiş). Sınır işin büyüklüğüne göre seçilir: beklenen araç
  sayısı artı biraz pay.
- Model senin aracını çağırmadıysa tarifini değiştir; `def` hücresini ve bu hücreyi yeniden çalıştır.

```python
goster("ciktilar/afis.jpg")
```

Çıktı: afiş. Slogan afişin yönergesine taşınmış mı, afişte yazı doğru çıkmış mı? Slogan kılavuzun ses tonuna uyuyor mu
(ünlem yok; "indirim", "hemen" yok)?

Bu afiş bugünün çıktısı: araçlarını bizim kurduğumuz, sırasını modelin seçtiği bir programın işi.

---

## Bonus

Üç küçük deneme, derste vakit kalırsa ya da evde. Birinciyi Adım 9'dan hemen sonra çalıştır: Adım 9'daki çalıştırmanın
isteklerini sayıyor.

### Bonus 1 — Bir çalıştırma kaç istek?

```python
istek_sayisi = 0
for mesaj in cevap.messages:
    if mesaj.role == "assistant":
        istek_sayisi = istek_sayisi + 1

print("Modele giden istek:", istek_sayisi)
```

Çıktı: `Modele giden istek: ...`, senin ekranında (Adım 9'daki çalıştırma için).

- Konu 1'deki sayaç: Adım 7'de gördüğün gibi her `assistant` mesajı modele giden ayrı bir isteğin cevabı.
- Bir cümle yazdın; modele birden çok istek gitti. Model her turda bir araç çağırdıysa istek sayısı, araç çağrısı
  sayısından bir fazladır: son cevap için de bir istek gider.

```python
olcum = cevap.metrics
girdi = olcum.input_tokens
cikti = olcum.output_tokens
noron = girdi * 0.009091 + cikti * 0.027273
yuvarlak = round(noron)

print("Girdi belirteci:", girdi, "| çıktı belirteci:", cikti)
print("Model istekleri için yaklaşık neuron:", yuvarlak)
```

Çıktı: girdi ve çıktı belirteci (token) sayıları ve yaklaşık neuron, senin ekranında.

- `cevap.metrics`: Agno'nun bu çalıştırmada saydığı toplam belirteçler (Konu 5). Girdi: modele giden; çıktı: modelin yazdığı.
- Cloudflare'in fiyat sayfasına göre gemma-4'te bir milyon girdi belirteci 9.091, bir milyon çıktı belirteci 27.273
  neuron; belirteç başına 0,009091 ve 0,027273 (kodda ondalık ayırıcı nokta: `0.009091`).
- Girdi neden büyük? Her istekte bütün konuşma ve bütün araç tarifleri yeniden gidiyor; kılavuz paragrafları da
  konuşmaya eklendikçe istek büyüyor.
- Bunun üstüne her `afis_ciz` çağrısı bir görsel: görsel başına yaklaşık 58 neuron (Konu 8'deki hesap). Günlük ücretsiz kota
  10.000 neuron; bütün modeller aynı kotadan yer.
- `tool_call_limit` olmasaydı ve model her turda "bir düzenleme daha" deseydi her tur bir istek ve bir görsel daha
  harcardı.

### Bonus 2 — Isınmadaki öbür istekler

```python
cevap = ajan.run("veri/fincan.jpg fotoğrafının arka planını sadeleştir")
kararlari_goster(cevap)
goster("ciktilar/duzenlenmis.jpg")
```

Çıktı: `fotograf_duzenle çalıştı: ...`, kararlar ve düzenlenmiş fotoğraf. Doğru araç seçildi mi, model `dosya`
bilgisine ne yazdı? Senin çıktına bak.

- Adım 4'te dosya yolunu biz yazmıştık; şimdi o da modelin kararı. Model var olmayan bir yol yazarsa (`fincan.jpg`)
  `duzenle` `Böyle bir dosya yok` der, araç modele `Fotoğraf düzenlenemedi.` cevabını verir; model başka bir yol
  deneyebilir. Sınır burada da işe yarar.

```python
cevap = ajan.run("Sayfa Kahve hafta sonu kaçta açılıyor?")
kararlari_goster(cevap)
print(cevap.content)
```

Çıktı: kararlar ve son cevap, senin ekranında.

- Üçüncü istek bir soru; çizilecek ya da düzenlenecek bir şey yok. Kılavuza bakıldı mı, yoksa model saatleri kendisi mi
  yazdı? Cevaptaki saatler kılavuzdakiyle (`veri/kilavuz.txt`, son paragraf) aynı mı?
- Model kılavuza baktıysa ajan bu kez yalnızca bilgi getirip cevap yazdı: Konu 11'deki "önce kılavuzda ara, sonra
  cevapla" işi, ama kılavuza bakma kararı modelin.

```python
cevap = ajan.run("afişi Instagram'da paylaş")
kararlari_goster(cevap)
print(cevap.content)
```

Çıktı: kararlar ve son cevap; ikisini birlikte oku.

- Beşinci isteği hiçbir araç karşılamıyor. Model yapamayacağını söyledi mi, yoksa bir araç mı çağırdı?
- Son cevabında yapmadığı bir şeyi ("paylaştım") yapmış gibi anlatıyor mu? Son cevap da bir model cümlesi; ajanın ne
  yaptığını `kararlari_goster`'den oku.

### Bonus 3 — Ajanın genel brifi: `instructions`

```python
genel_brif = "Sayfa Kahve için çalışan bir tasarım asistanısın."
genel_brif = genel_brif + " Bir şey üretmeden önce kılavuza bak. Görsel yönergelerini İngilizce yaz."

araclar = [afis_ciz, fotograf_duzenle, kilavuzda_ara]
ajan = Agent(model=model, tools=araclar, instructions=genel_brif, tool_call_limit=3, telemetry=False)
cevap = ajan.run("bir indirim afişi çiz")
kararlari_goster(cevap)

mesajlar = cevap.messages
ilk_mesaj = mesajlar[0]
print(ilk_mesaj.role, "|", ilk_mesaj.content)
```

Çıktı: kararlar ve `system | Sayfa Kahve için çalışan bir tasarım asistanısın. ...`.

- Docstring tek bir aracı tarif eder; `instructions` ise bütün işi anlatan **genel brif**. Agno onu konuşmanın başına
  bir **sistem mesajı** (`system`) olarak koyar; her istekte modele o da gider.
- İstekte bilerek "indirim" var; kılavuz bu sözcüğü yasaklıyor. Bu kez kılavuza bakıldı mı? Model isteğe itiraz etti mi,
  yoksa yine de çizdi mi? Senin çıktına bak.
- Bir kural ya aracın tarifinde ("ne zaman kullan") ya da ajanın genel brifinde durur. Kural tek bir aracı
  ilgilendiriyorsa o aracın tarifine, bütün işi ilgilendiriyorsa genel brife yaz; düzeltmen gerektiğinde nerede
  olduğunu bilirsin.

---

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Anahtar |
|---|---|---|
| Isınma | Üç aracın tarifi; beş istek için kendi planın | gerekmez |
| Adım 1 | Hazır parçalar; fincan; kılavuzda bir arama | gerekir |
| Adım 2 | Araç tarifi, elle (iç içe sözlükler) | gerekmez |
| Adım 3 | İstekte `tools`, cevapta `tool_calls` | gerekir |
| Adım 4 | Aracı çalıştıran program; ajan döngüsü nedir | gerekir |
| Adım 5 | Agno: model (`OpenAILike`) ve üç araç fonksiyonu; `tarifi_goster` | istek göndermez |
| Adım 6 | İlk ajan; `cevap.tools` ile kararları görmek | gerekir |
| Adım 7 | Çok adım: kılavuz sonra çizim; `cevap.messages` | gerekir |
| Adım 8 | Tarifi bozmak ve düzeltmek | gerekir |
| Adım 9 | Kendi aracın: `slogan_yaz`'ın tarifi; dört araçlı ajan | gerekir |
| Bonus 1 | Bir çalıştırma kaç istek, ne kadar kota | istek göndermez (Adım 9'un sonucunu okur) |
| Bonus 2 | Isınmadaki öbür istekler: fotoğraf düzenleme, kılavuzdan bir soru, aracı olmayan iş | gerekir |
| Bonus 3 | Genel brif: `instructions` | gerekir |

---

## Sık karşılaşılan hatalar ve mesajlarını okumak

| Mesaj / belirti | Ne oldu | Ne yapmalı |
|---|---|---|
| `ModuleNotFoundError: No module named 'ajan_araclari'` | Defterin kopyası başka bir klasörde | Kopya `ajan_araclari.py`'nin yanında olmalı |
| `ModuleNotFoundError: No module named 'agno'` | Kütüphaneler kurulmamış ya da çekirdek `.venv` değil | `gita3111`'de `uv sync`; çekirdek olarak `.venv` |
| `FileNotFoundError: [Errno 2] No such file or directory: '../anahtar.txt'` | Anahtar dosyası yok ya da yeri yanlış | Konu 2'deki `anahtar.txt`, `gita3111` klasöründe |
| `KeyError: 'tool_calls'` (Adım 3) | Model araç çağırmadı, metin yazdı | Bir önceki hücrenin `print(yanit)` çıktısına bak; isteği yeniden gönder |
| `Listede olmayan bir araç: ...` (Adım 4) | Model tarifte olmayan bir ad yazdı | Güvenlik ağı çalıştı; isteği yeniden gönder |
| Kırmızı `ERROR` satırları, `Araç kaydı yok. Ajanın son mesajı: ...` | Agno modele ulaşamadı ya da istek reddedildi (anahtar, kota, bağlantı) | `ERROR` satırındaki durum kodunu oku: 401 anahtar, 429 kota ya da hız sınırı |
| Adım 7'de yalnızca `user` satırı; Bonus 1'de `Modele giden istek: 0` ve sıfır belirteç | Ajan hata verdi; modelden hiç cevap gelmedi | Çalıştırma hücresindeki `ERROR` satırına bak; sorunu çözüp yeniden çalıştır |
| `TypeError: afis_ciz() missing 1 required positional argument: 'yonerge'` | Araç listesine `afis_ciz()` (parantezli) yazıldı | Listede parantez yok: `[afis_ciz, ...]` |
| Sarı `WARNING Could not run function ...` ve uzun, kırmızı bir `ERROR`; hücre yine de biter | Aracın içinde bir hata var (ör. bir adı yanlış yazdın). Agno hücreyi durdurmaz, hatayı modele aracın sonucu olarak gönderir | Kırmızı yazının son satırındaki hatayı oku (ör. `NameError`), `def` hücresini düzelt, araç listesini ve ajanı yeniden kur |
| Ajan eski tarifle davranıyor | `def` hücresi çalıştı ama araç listesi ve ajan yeniden kurulmadı | Aynı hücredeki `araclar = ...` ve `ajan = ...` satırlarını da çalıştır |
| Görsel eski | Bu çalıştırmada `afis_ciz` çağrılmadı; dosya bir öncekinden kaldı | `kararlari_goster`'in çıktısına bak |
| `FileNotFoundError: ... 'ciktilar/afis.jpg'` (Adım 6) | Model `afis_ciz`'i çağırmadı; afiş dosyası hiç oluşmadı | `kararlari_goster`'in çıktısına bak; isteği yeniden çalıştır |
| `SyntaxError` (Adım 9) | Docstring yazılırken üç tırnaktan biri silindi | Baştaki ve sondaki üç tırnak kalmalı |
| `Böyle bir dosya yok: ...` | Model düzenleme için olmayan bir dosya yolu yazdı | Yolu istekte açık yaz: `veri/fincan.jpg` |
| `NameError: name 'model' / 'kararlari_goster' / 'cevap' is not defined` | Bir hücre atlandı | Adımları sırayla çalıştır |

---

## Kendini dene

1. Model bir aracı seçerken neleri görür, neleri görmez?
2. Adım 4'te `else` dalı ne işe yarıyor? Silseydik model `"edit"` yazınca ne olurdu?
3. `def afis_ciz(yonerge: str) -> str:` satırındaki `: str` ve `-> str` ne anlatıyor? Elle yazılan tarifteki karşılıkları ne?
4. Bir araç fonksiyonu sonucu `print` ile yazıp `return` etmezse model ne görür?
5. `tool_call_limit=3` ne zaman devreye girer? Sınır dolunca Agno ne yapar, ne yapmaz?
6. Model bir çalıştırmada iki araç çağırdı; her turda bir tane. Modele kaç istek gitti? Neden?
7. `telemetry=False` yazmazsak ne olur?
8. Sırası her seferinde aynı olan bir iş için (konu → slogan → görsel) ajan mı kurarsın, hat mı? Neden?

---

## Bu konuda öğrendiklerin

- **Ajan:** kararı veren bir dil modeli, modelin kullanabileceği araçlar ve ikisini bağlayan bir döngü.
- **Araç tarifi:** ad, tarif ve bilgiler. Elle iç içe sözlüklerle (`tools`), Agno'da bir fonksiyonla: ad fonksiyonun adı,
  tarif docstring, bilgiler `def` satırındaki tür ipuçlu adlar (`yonerge: str`).
- **Araç çağrısı:** model "şu aracı, şu bilgiyle çalıştır" der (`tool_calls`); çalıştıran programdır.
- **Döngü:** aracın sonucu modele geri gider, model yeniden karar verir; son cevaba ya da sınıra kadar.
- **Kararı görünür kılmak:** `cevap.tools` (hangi araç, hangi bilgi), `cevap.messages` (bütün konuşma).
- **Tarif bir brif:** ne yapar, ne zaman seçilir. Yanlış seçimde önce tarife bak.
- **Sınır ve kota:** `tool_call_limit`; her araç çağrısı bir istek daha, her görsel ayrıca kota.

---

## Bu konunun tek cümlesi

Ajan, kararı modele bırakan bir döngüdür: model hangi aracın, hangi bilgiyle çalışacağını seçer, aracı program
çalıştırır; kararın kalitesi araçları ne kadar net tarif ettiğine, güvenliği de hangi araçları verdiğine ve koyduğun
sınıra bağlıdır.

---

## Sözlükçe

| Terim | Anlamı |
|---|---|
| Ajan (agent) | Bir isteğe hangi araçların, hangi sırayla kullanılacağını bir dil modelinin seçtiği program: model + araçlar + döngü |
| Araç (tool) | Modele tanıtılan, adı, tarifi ve aldığı bilgileri belli bir fonksiyon |
| Tarif (description) | Aracın ne yaptığını ve ne zaman seçileceğini anlatan cümle; model aracın ne işe yaradığını yalnızca bundan öğrenir |
| Araç tarifi | Modele giden üç parçanın bütünü: ad, tarif, bilgiler (`tools` içindeki her sözlük; `tarifi_goster` bunu yazdırır) |
| Araç çağrısı (tool call) | Modelin "şu aracı, şu bilgiyle çalıştır" diyen cevabı (`tool_calls`) |
| Yapılandırılmış çıktı | Serbest bir cümle yerine alanları belli bir cevap; burada `tool_calls`'taki `name` ve `arguments` (Konu 5'te adı geçti) |
| Ajan çerçevesi (agent framework) | Araç tariflerini kuran, döngüyü çalıştıran, sınırı sayan kütüphane; bu derste Agno |
| `messages` | Sohbet biçimindeki istek: rolü (`user`, `assistant`, `tool`, `system`) ve içeriği olan mesajların listesi |
| Tür ipucu (type hint) | `yonerge: str` gibi, bir bilginin türünü söyleyen not; `-> str` fonksiyonun verdiği türü söyler |
| Docstring | `def` satırının hemen altındaki üç tırnaklı metin; Agno aracın tarifini buradan okur |
| `tool_call_limit` | Bir ajan çalıştırmasında en fazla kaç aracın çalışacağı; döngünün durma koşulu |
| Telemetri | Bir programın kullanım bilgisini kendi geliştiricisine göndermesi; Agno'da `telemetry=False` ile kapanır |
| `OpenAILike` | Agno'da OpenAI'nin istek biçimini kullanan bir modeli tanıtmanın yolu; istek Cloudflare'e gider, OpenAI hesabı gerekmez |
| Genel brif (`instructions`) | Ajanın bütün işi için yazılan brif; Agno onu konuşmanın başına bir sistem mesajı (`system`) olarak koyar |
| Belirteç (token) | Modelin metni böldüğü parçalar; kota girdi ve çıktı belirteçlerine göre harcanır |

---

## Ödev

Ödev `odevler/odev12.md` dosyasında: ajanına kendi tasarladığın bir araç ekleyeceksin, en az dört istekle modelin
kararlarını kendi planınla karşılaştıracak, bir tarifi bozup düzelteceksin. Puan yok; Konu 13'ün başında sıradaki
arkadaşlar gösterecek. Ajan final projesi için zorunlu değil.

---

## Sonraki konu

**Konu 13 — Final atölyesi.** Yeni kavram yok: dönem boyunca öğrendiklerini (koddan görsel, hat, RAG, ajan) kendi
projende birleştirip projenin çalışan ilk hâlini kuruyorsun. Ajan, projen sırası belirsiz bir iş içeriyorsa bir seçenek;
sırası belliyse Konu 10'daki hat daha ucuz ve daha öngörülebilir.

---

## Kendini dene — cevaplar

1. **Görür:** aracın adını, tarifini (docstring ya da `description`), bilgilerinin adlarını ve türlerini; aracı
   çağırdıktan sonra da `return` edilen sonucu. **Görmez:** fonksiyonun kodunu.
2. Model listede olmayan bir ad yazarsa programın yanlış bir şey çalıştırmasını engeller ve durumu söyler. Silseydik
   `"edit"` için `if` de `elif` de tutmaz, hiçbir şey çalışmaz; `yol` hiç tanımlanmadığı için `print` satırı
   `NameError` verirdi (hücre ilk kez çalışıyorsa).
3. `: str` "bu bilgi metin", `-> str` "fonksiyon metin verir". Elle yazılan tarifte `"type": "string"`.
4. `None`. `print` yalnızca ekrana yazar; modele `return` edilen gider (alıştırmanın 3. bozuk kodu).
5. Bir çalıştırmada üç araç çalıştıktan sonra model bir araç daha isterse. Agno o aracı çalıştırmaz, modele "sınır
   doldu" der; ama döngüyü durdurmaz: modele istek gitmeye devam edebilir.
6. Üç: iki araç çağrısı için iki istek, son cevap için bir istek daha.
7. Agno her çalıştırmada kendi sunucusuna kullanım bilgisi gönderir.
8. Hat. Sıra belliyse kararı modele bırakmak yalnızca istek, gecikme ve yanlış seçim ihtimali ekler (Konu 10).
