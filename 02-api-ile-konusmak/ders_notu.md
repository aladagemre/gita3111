# Konu 2 — İnterneti Koddan Konuşturmak (API)

Bu not konunun özetidir; ısınmadan sonra slaytlarla **aynı sırada** ilerler. Derste
kaçırdığın bir yer olursa buradan oku, sonra ilgili örnek dosyayı çalıştır.

**Konu 1'de:** bilgisayarındaki bir metni işledik. Kafe yorumlarını sayınca bir bulgu
çıktı: müşteriler kafeyi kahvesiyle değil, **sessiz bir çalışma yeri** olarak anlatıyor.

**Bu konuda:** kodun ilk kez bilgisayarının dışına çıkıyor. Uzaktaki bir yapay zeka
modeline soru gönderip cevabını alacağız. Soracağımız sorular da o bulgudan geliyor:
sessiz bir çalışma kafesinin yeni kimliği için slogan, renk, yazı tipi.

**Konunun sonunda elinde:**

- senden soru alıp modele soran ve cevabı dosyaya yazan çalışan bir program
  (`cevap.txt`),
- beş soruyu tek seferde sorup cevapları düzenli bir dosyada toplayan bir program
  (`cevaplar.json`),
- ve bir bulgu: **soruya bağlam yazmak cevabı nasıl değiştiriyor?**

**Kurulum (dersten önce):** konunun klasörüne gir (`cd 02-api-ile-konusmak`) ve bir kez
`uv sync` çalıştır. Bu konunun kütüphaneleri (internete istek atan `requests` ve
`wordcloud`) klasördeki `pyproject.toml` dosyasında yazılı; `uv sync` onları önceden
indirir. Yapmazsan ilk `uv run` komutu indirir, ama ders sırasında beklersin.

> Bu dönemin **kritik konusu**: Konu 4, 5, 8, 9, 10 ve 11 bunun üstüne kuruluyor.
> Buradaki her adım ileride her derste tekrar edecek. Anlamadığın bir yer kalırsa
> şimdi sor; sonra sormak çok daha pahalı.

### Bu not nasıl okunur

- Her adımda üç şey var: **ne yapıyoruz**, **neden gerekiyor**, **atlarsan ne olur**.
- `Kendini dene` kutuları küçük kontrol sorularıdır. Cevapları notun sonunda.
- Örneklerin çoğu gerçek istek atar ve `anahtar.txt` ister; isteyen adımların başında
  **(anahtar gerekir)** yazıyor. Anahtarsız çalışanlar: ısınma, Adım 3, bozuk kodlar ve
  sınıf alıştırması.
- Kodları bu konunun klasöründen çalıştır: önce `cd 02-api-ile-konusmak`, sonra
  `uv run ornekler/...`. Nedenini Konu 1'de gördün; `anahtar.txt` için Adım 1'de bir kez
  daha bakacağız.

---

## Isınma: iç içe sözlük

`00_isinma.py` iki bozuk satır içeriyor. Birazdan sunucudan gelecek cevap tam olarak
bu yapıda olacak; ısınma onun provası. Dosyayı çalıştır, hatayı oku, satırı düzelt,
tekrar çalıştır.

```python
yanit = {
    "success": True,
    "result": {
        "response": "Merhaba!",
        "usage": {"prompt_tokens": 4, "completion_tokens": 2},
    },
    "errors": [],
}

hatali_yanit = {
    "success": False,
    "result": None,
    "errors": [{"code": 10000, "message": "Authentication error"}],
}

# Tamir 1: Merhaba! yazmalı
print(yanit["response"])

# Tamir 2: Authentication error yazmalı
print(hatali_yanit["errors"]["message"])
```

1. **Sözlüğün içindeki sözlük.** Metin dıştaki sözlükte değil, `result` içinde:
   `yanit["response"]` değil, `yanit["result"]["response"]`.
2. **Sözlüğün içindeki liste.** Hatalı bir yanıtta `errors` bir liste olur; önce
   sırayla elemana, sonra anahtara gidilir: `hatali_yanit["errors"][0]["message"]`.

Kural aynı: her köşeli parantez **bir kat** içeri girer. Liste katında sıra numarası,
sözlük katında anahtar adı yazılır.

İfadeyi soldan sağa, kat kat okursan hata yapmazsın:

| İfade | Elde ettiğin şey | Türü |
|---|---|---|
| `yanit` | Bütün yanıt | sözlük |
| `yanit["result"]` | İçteki sözlük | sözlük |
| `yanit["result"]["usage"]` | Kullanım bilgisi | sözlük |
| `yanit["result"]["usage"]["prompt_tokens"]` | `4` | sayı |
| `yanit["errors"]` | Hata listesi (burada boş) | liste |

### Hata mesajını sondan oku

Bu konuda iki hata çok sık çıkacak. Python bir hata verdiğinde en önemli satır
**en alttaki** satırdır: önce hatanın türü, sonra açıklaması. Onun hemen üstünde de
hatanın çıktığı satır numarası yazar.

```text
KeyError: 'response'
```

"Bu sözlükte `response` diye bir anahtar yok." Bir kat atladın demektir: `result`
katına girmeden `response`'u aradın. Isınma dosyasını ilk çalıştırdığında tam olarak
bunu görürsün.

```text
TypeError: list indices must be integers or slices, not str
```

"Listeyi bir adla açmaya çalıştın; liste sadece sıra numarasıyla açılır." `errors`
bir liste; `hatali_yanit["errors"]["message"]` yazınca bu hatayı alırsın (ısınmanın
ikinci satırı). Doğrusu `hatali_yanit["errors"][0]["message"]`.

> **Kendini dene 1.** Yukarıdaki `yanit` için:
> (a) `completion_tokens` değerine hangi ifadeyle ulaşırsın?
> (b) `yanit["errors"][0]` yazarsan hangi hatayı alırsın, neden?
> (c) `yanit["usage"]["prompt_tokens"]` yazarsan?

---

## Anahtarın yoksa?

Bugünkü örneklerin çoğu **gerçek istek** atar ve ilk iş `anahtar.txt` dosyasını okur.
Dosya yoksa program ilk satırda durur:

```text
FileNotFoundError: [Errno 2] No such file or directory: '../anahtar.txt'
```

Anahtarın henüz yoksa:

- Ders boyunca **yanındakiyle birlikte** çalış: istekleri onun ekranında izle, kodu sen
  de kendi dosyana yaz.
- Adım 3 (`03_yaniti_coz.py`) anahtarsız da çalışır: kayıtlı bir yanıtı okur. Isınma,
  bozuk kodlar ve sınıf alıştırması da internet istemez.
- Hesabı **bugün** aç: kurulum yönergesinin 6. adımı (`../00-hazirlik/kurulum-yonergesi.md`).
  Ödev için kendi anahtarın gerekiyor; Konu 4'ten itibaren her derste de gerekecek.

---

## İstemci ve sunucu

Tarayıcıda her gün yaptığın şeyin kodla yapılan hâli:

- **Sen** (istemci) bir şey istiyorsun.
- **Uzaktaki bilgisayar** (sunucu) cevap veriyor.
- Tarayıcı da aynı isteği atıyor; sadece üstünde bir arayüz var. Bugün arayüzü
  kaldırıp isteği kendimiz atıyoruz.

Bir sohbet sitesine soru yazıp Enter'a bastığında da olan budur: sayfa, sorunu
paketleyip bir sunucuya yollar, gelen cevabı ekrana dizer. Modeli çalıştıran
bilgisayar senin bilgisayarın değil. Bu yüzden internet gerekir, bu yüzden bir
**kota** vardır (başkasının bilgisayarını kullanıyorsun) ve bu yüzden kim olduğunu
söylemen gerekir.

Programların birbirine soru sorabildiği bu kapıya **API** denir. Bugün Cloudflare'in
yapay zeka API'sine soru soracağız. İleride görsel üretirken, video üretirken de aynı
kapıdan geçeceğiz; değişen tek şey adres ve gövde olacak.

### Bir sorunun yolculuğu

Kodun bir soru gönderdiğinde beş şey sırayla olur. Her aşama ayrı bir yerde
bozulabilir ve her bozulmanın **ayrı bir işareti** vardır:

| Aşama | Ne oluyor | Bozulursa ne görürsün |
|---|---|---|
| 1. Hazırlık | Programın adresi, başlığı, gövdeyi hazırlar | Python hatası (`KeyError`, `FileNotFoundError`...) |
| 2. Yol | İstek internetten sunucuya gider | `ConnectionError` ya da `ReadTimeout`; **durum kodu yok** |
| 3. Kimlik | Sunucu anahtarına bakar | **401** ya da **403** |
| 4. İş | Sunucu modeli çalıştırır | **400**, **404**, **429** ya da **500** |
| 5. Dönüş | Cevap JSON olarak sana gelir, sen içine girersin | `KeyError`, `TypeError` |

Bu tabloyu akılda tutmanın faydası şu: bir hata aldığında "neresi bozuk?" sorusuna
tahminle değil, işaretle cevap verirsin. Durum kodu bile gelmediyse sorun internette;
401 geldiyse anahtarında; `KeyError` geldiyse sunucu işini yapmış, sen içine yanlış
yoldan giriyorsun.

---

## Anahtar neden gizli?

Anahtar senin kimliğin. Başkasının eline geçerse senin adına istek atar, kotanı
bitirir. Ücretsiz kotan günde 10.000 **neuron** (Cloudflare'in harcama birimi);
yabancı biri bir gecede bunu tüketebilir ve ertesi gün ödevin çalışmaz. Bu yüzden:

- Anahtar **koda yazılmaz**, ayrı bir dosyada (`anahtar.txt`) durur.
- O dosya **ödev teslimine konmaz**.
- Ekran paylaşırken anahtar dosyası **açık bırakılmaz**.

Neden "koda yazılmaz"? Kodunu paylaşmak doğal bir şey: ödev teslim edersin, bir
arkadaşına yardım edersin, sınıfta ekranını açarsın. Anahtar kodun içindeyse her
seferinde anahtarını da paylaşmış olursun. Ayrı dosyada durursa kodu rahatça
paylaşırsın, anahtar evde kalır.

Yanlışlıkla paylaşırsan panik yok, saklamaya da çalışma. Dört adım:

1. Cloudflare paneline gir, eski token'ı sil (artık kimse onunla istek atamaz).
2. Kurulum yönergesindeki gibi yeni bir token üret.
3. `anahtar.txt` içindeki `API_TOKEN` satırını yenisiyle değiştir.
4. `01_anahtar_oku.py` ile yeni anahtarın okunduğunu kontrol et.

Hepsi bir dakikadan kısa sürer.

> **Terim notu:** Bu derste "anahtar" dediğimiz şeye Cloudflare **API token** diyor.
> `anahtar.txt` içindeki `API_TOKEN` satırı ve hata mesajlarındaki "token" kelimesi
> aynı şeyi anlatıyor. İki karışıklığa dikkat:
> - Bu "anahtar", Konu 1'deki **sözlük anahtarı** değil; senin giriş kartın.
> - Aşağıda göreceğin **belirteç** (İngilizcesi de "token") başka bir şey: kelime parçası.

---

## Adım 1 — Anahtarı dosyadan oku

`anahtar.txt` dosyan şöyle görünüyor:

```
ACCOUNT_ID = a1b2c3...
API_TOKEN = xyz789...
```

İki bilgi var: **hesap kimliği** (Account ID; hangi hesabın modeli çalıştırılacak)
ve **token** (sen misin). Hesap kimliği tek başına bir işe yaramaz; token ise
gizlidir.

`01_anahtar_oku.py` bu dosyayı satır satır okuyup bir **sözlüğe** koyar:

```python
anahtarlar = {}
with open("../anahtar.txt", encoding="utf-8") as dosya:  # ".." = bir üst klasör
    for satir in dosya:
        ad, _, deger = satir.partition("=")  # "=" işaretinden ikiye böl
        anahtarlar[ad.strip()] = deger.strip()

hesap = anahtarlar["ACCOUNT_ID"]
anahtar = anahtarlar["API_TOKEN"]

print("Hesap:", hesap)
print("Anahtar okundu.")
```

Konu 1'de dosyayı `dosya.read()` ile tek parça okumuştuk. Burada üç yeni şey var:

- `for satir in dosya` dosyayı **satır satır** gezer.
- `satir.partition("=")` satırı üç parçaya böler: eşittirin solu, eşittirin kendisi,
  sağı. Soldaki üç değişken bu üç parçayı sırayla alır; ortadakini kullanmayacağımız
  için adı `_`.
- `.strip()` baştaki ve sondaki boşlukları (satır sonundaki görünmez `\n` dahil)
  siler.

Tek bir satırın yolculuğunu adım adım izleyelim:

| Aşama | Değer |
|---|---|
| Dosyadaki satır | `'API_TOKEN = xyz789\n'` |
| `partition("=")` sonrası | `('API_TOKEN ', '=', ' xyz789\n')` |
| `ad.strip()` | `'API_TOKEN'` |
| `deger.strip()` | `'xyz789'` |
| Sözlüğe yazılan | `anahtarlar["API_TOKEN"] = "xyz789"` |

**Neden `split` değil de `partition`?** Token'ların içinde bazen `=` işareti olur.
`partition` sadece **ilk** eşittirden böler, gerisini değere bırakır:
`"API_TOKEN = ab=cd"` satırından değer olarak `ab=cd` çıkar. Kırpılmış bir token
401 hatası verirdi.

Satır adları **harfi harfine** aranır: `anahtarlar["ACCOUNT_ID"]` büyük harfle yazılmış
`ACCOUNT_ID` satırını bulur, `account_id` satırını bulmaz.

Anahtarı **ekrana basmıyoruz**; sadece okunduğunu söylüyoruz. Hesap kimliği (Account ID)
tek başına bir işe yaramaz, onu basmak güvenli. Anahtar dosyasında `ACCOUNT_ID = hesap123` yazıyorsa çıktı:

```text
Hesap: hesap123
Anahtar okundu.
```

Sonraki dosyalar (`02`, `04`, `05`, `06`, `09`) aynı okuma satırlarıyla başlar; her
dosya tek başına çalışsın diye. Derste bu satırları bir kez yazarız, sonra açık olan
dosyaya eklenerek ilerleriz.

### Dosya nerede olmalı? Çalışma klasörü

Konu 1'deki kural burada da geçerli: `open(...)` dosyayı **komutu çalıştırdığın
klasöre göre** arar, `.py` dosyasının durduğu yere göre değil. Komutları konunun
klasöründen (`02-api-ile-konusmak`) çalıştırıyoruz; `veri/...` yolları bu yüzden
çalışıyor.

`anahtar.txt` ise bir üst klasörde, `gita3111`'in içinde duruyor; böylece bütün konular
aynı dosyayı kullanıyor. Yoldaki **`..`** "bir üst klasör" demek. `"../anahtar.txt"`,
"bulunduğum klasörden bir üste çık, oradaki `anahtar.txt`'yi aç" anlamına gelir:

```
gita3111/
├── anahtar.txt                  ← "../anahtar.txt" burayı gösterir
└── 02-api-ile-konusmak/         ← komutları buradan çalıştırıyoruz
    ├── ornekler/02_ilk_istek.py
    └── veri/ornek_yanit.json
```

Terminalde `ornekler` klasörüne girip çalıştırırsan iki yol da kayar: `..` artık
`02-api-ile-konusmak` klasörünü gösterir (orada `anahtar.txt` yok), `veri/...` de
`ornekler/veri/...` olarak aranır. Örneğin `03_yaniti_coz.py`:

```text
FileNotFoundError: [Errno 2] No such file or directory: 'veri/ornek_yanit.json'
```

Çözüm: `cd ..` ile konu klasörüne (`02-api-ile-konusmak`) dön, komutu oradan ver:
`uv run ornekler/03_yaniti_coz.py`.

### Adım 1'de sık yapılan hatalar

| Ne oldu | Ne görürsün | Çare |
|---|---|---|
| Windows dosyayı `anahtar.txt.txt` diye kaydetti (uzantılar gizli) | `FileNotFoundError: ... '../anahtar.txt'` | Dosya gezgininde "Dosya adı uzantılarını göster"i aç, fazla `.txt`'yi sil |
| Değeri tırnak içine yazdın: `API_TOKEN = "xyz789"` | Okuma çalışır ama istek **401** döner | Tırnaklar da token'ın parçası sanılıyor; tırnakları sil |
| Satır adında boşluk ya da küçük harf: `API TOKEN = ...`, `api_token = ...` | `KeyError: 'API_TOKEN'` | Tam olarak `API_TOKEN` yaz: büyük harf, alt çizgi |
| Token'ı kopyalarken son karakteri kaçırdın | **401** | Token'ı panelden yeniden üretmek en hızlısı |

> **Kendini dene 2.** `anahtar.txt` dosyasının içi şu olsun:
>
> ```
> account_id = a1b2
> API_TOKEN = "xyz789"
> not: bu satırda eşittir yok
> ```
>
> `anahtarlar` sözlüğünde ne olur? `01_anahtar_oku.py` hangi satırda, hangi hatayla durur?
> Küçük harfi düzeltsen bu dosyayla istek atınca ne olur?

---

## Bir isteğin üç parçası

| Parça | Ne söyler | Kodda |
|---|---|---|
| **Adres** (endpoint, uç nokta) | Nereye gidiyorum | `adres` — bir metin |
| **Başlık** (header) | Ben kimim | `basliklar` — bir sözlük |
| **Gövde** (body) | Ne istiyorum | `govde` — bir sözlük |

Bir kargo gönderisi gibi düşünebilirsin: adres (kime gidiyor), gönderen bilgisi
(kimden geliyor) ve kutunun içi (ne gönderiliyor). Biri eksikse kargo ya yola
çıkmaz ya da geri döner.

```python
MODEL = "@cf/google/gemma-4-26b-a4b-it"
adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
basliklar = {"Authorization": f"Bearer {anahtar}"}
govde = {"prompt": "Müşterilerinin sessiz bir çalışma yeri olarak anlattığı bir kafe için üç kısa slogan yaz."}
```

### Adres: parça parça

```
https://api.cloudflare.com  /client/v4  /accounts/{hesap}  /ai/run/{MODEL}
└──── sunucu ─────────────┘ └ sürüm ──┘ └─ hangi hesap ──┘ └─ hangi model ─┘
```

- Adresin içine Konu 1'deki `f"..."` ile hesap kimliğini ve model adını yerleştiriyoruz.
- Model adı `@cf/` ile başlar ve **harfi harfine** doğru olmalı. Dönem boyunca metin
  için hep aynı modeli kullanacağız: `@cf/google/gemma-4-26b-a4b-it`.
- **En sık hata:** baştaki `f` harfini unutmak. O zaman Python süslü parantezleri
  doldurmaz ve sunucuya kelimesi kelimesine `.../accounts/{hesap}/...` gider.
  Sunucu "`{hesap}`" adında bir hesap bulamaz, istek hata koduyla döner. Şüphelenirsen
  `print(adres)` yaz: adreste token yok, ekrana basmak güvenli.

### Başlık: kimlik

- `Authorization` başlığın adıdır, sunucunun beklediği yazımla yazılır.
- `Bearer` sabit bir kelime: "bu isteği taşıyanın anahtarı şudur" demek. Anahtarın
  önüne **boşlukla** yazılır; değiştirme.
- `f"Bearer{anahtar}"` (boşluksuz) yazarsan sunucuya `Bearerxyz789` gider. Sunucu
  bunu tanımaz ve **401** döner. Tek bir boşluk yüzünden bir saat kaybetmek bu
  konunun klasiğidir.

### Gövde: asıl soru

- Sunucu soruyu `"prompt"` adlı alanda bekler. Alanın adını `"soru"` yaparsan
  sunucu soruyu bulamaz ve **400** (istek bozuk) döner.
- Soru Konu 1'in bulgusundan geliyor: müşteriler kafeyi sessiz bir çalışma yeri
  olarak anlatıyordu. Modelden o kafe için slogan istiyoruz. Bu cümlenin neden bu
  kadar uzun olduğunu Adım 7'de göreceğiz: kısaltırsan cevap bambaşka bir kafeyi
  anlatıyor.

> **Kendini dene 3.** Her satırda üç parçadan hangisi bozuk ve sunucu ne der?
> (a) `basliklar = {"Authorization": f"Bearer{anahtar}"}`
> (b) `adres = "https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"`
> (c) `govde = {"soru": "Üç slogan yaz."}`

---

## Adım 2 — İsteği gönder

**(anahtar gerekir)** Bu kod gerçekten internete çıkar. Dosyası: `02_ilk_istek.py`.

Dosyanın en üstüne iki kütüphane:

```python
import json

import requests
```

En alta istek:

```python
cevap = requests.post(adres, headers=basliklar, json=govde, timeout=60)
print("Durum kodu:", cevap.status_code)
```

Satır satır:

- `requests.post`: "sana bir şey gönderiyorum, karşılığında cevap bekliyorum."
  Tarayıcının adres çubuğuna bir adres yazdığında yapılan istek `get` türündedir,
  yani sadece "bana şu sayfayı ver" der. Biz sunucuya bir soru **gönderdiğimiz**
  için `post` kullanıyoruz.
- `headers=basliklar`: kimlik bilgisini isteğe ekle.
- `json=govde`: gövde sözlüğünü sunucunun anlayacağı **JSON** biçiminde gönder.
  (JSON'u hemen aşağıda görüyoruz.)
- `timeout=60`: 60 saniyede cevap gelmezse vazgeç. Yazmazsan program sonsuza kadar
  bekleyebilir. Normalde cevap birkaç saniyede gelir; uzun cevaplar biraz daha sürer.
- `cevap` bir sözlük değil, cevabın bütününü taşıyan bir nesne: durum kodu, içerik vs.
  `print(cevap)` yazarsan sadece `<Response [200]>` görürsün.
- `status_code`: işin yolunda gidip gitmediğini söyleyen sayı. `200` her şey yolunda.

### Adım 2'de sık yapılan hatalar

**`json=` yerine `data=` yazmak.** `requests.post(adres, headers=basliklar, data=govde)`
de çalışıyormuş gibi görünür, ama gövdeyi JSON olarak değil, bir web formu gibi
gönderir. Sunucu içinde `prompt` bulamaz ve **400** döner. Kural: gövde sözlükse
`json=`.

**İnternet yoksa.** İstek sunucuya hiç ulaşmaz, dolayısıyla durum kodu da gelmez.
Program şu satırla durur:

```text
requests.exceptions.ConnectionError: ...
```

Önce bağlantını kontrol et. Okul ağlarında bazı adresler kapalı olabilir; telefonun
internetiyle dene.

**Sunucu çok geç cevap verirse.** 60 saniye dolunca:

```text
requests.exceptions.ReadTimeout: ...
```

Çoğunlukla geçicidir; birkaç dakika sonra tekrar dene.

**Gelen içerik JSON değilse.** Nadiren sunucu bir hata sayfası (HTML) gönderir.
O zaman `cevap.json()` şunu verir:

```text
requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

"Bu JSON değil" demek. Ne geldiğini görmek için ham metni bas:
`print(cevap.status_code, cevap.text[:300])`.

---

## JSON — sözlüğün ağdaki hâli

**JSON**, sözlük ve listelerin metin olarak yazılmış hâlidir; bilgisayarlar arasında
veri böyle taşınır. İnternetten bir Python sözlüğü gönderemezsin, sadece metin
gönderebilirsin. JSON o metnin ortak biçimi: Python da, tarayıcı da, sunucu da onu
okuyabilir.

Sunucu düz metin göndermiyor, iç içe bir sözlük gönderiyor. `02_ilk_istek.py` onu
sözlüğe çevirip okunaklı basarak bitiyor:

```python
yanit = cevap.json()
print(json.dumps(yanit, ensure_ascii=False, indent=2))
```

- `cevap.json()` gelen içeriği tanıdık bir **sözlüğe** çevirir.
- `json.dumps` sözlüğü ekrana basılacak, girintili bir metne çevirir.

Gelen yanıt şu biçimde. Bu, `veri/ornek_yanit.json` dosyasında kayıtlı duran bir yanıt;
Adım 3'te onu okuyacağız:

```json
{
  "result": {
    "response": "1) Sessizliğin adresi. 2) Kahven, prizin, zamanın. 3) Burada odaklanırsın.",
    "usage": {"prompt_tokens": 24, "completion_tokens": 22, "total_tokens": 46}
  },
  "success": true,
  "errors": [],
  "messages": []
}
```

- `ensure_ascii=False` Türkçe harfler bozulmasın diye. Yazmazsan `ılık yeşil` yerine
  `ılık yeşil` görürsün. Veri bozulmamıştır ama okunmaz.
- `indent=2` iç içe yapı girintili görünsün diye. Yazmazsan hepsi tek satırda gelir.

### JSON ile Python sözlüğü arasındaki üç fark

JSON'u okurken şaşırtan üç küçük fark var. `json.load` ve `.json()` bunları senin
yerine çevirir:

| JSON'da | Python'da | Anlamı |
|---|---|---|
| `true` / `false` | `True` / `False` | doğru / yanlış |
| `null` | `None` | "hiçbir şey" |
| sadece çift tırnak `"..."` | tek ya da çift tırnak | metin |

Ekranda `"success": true` görüp kodda `yanit["success"] == "true"` yazarsan hep
`False` alırsın; çünkü Python'daki değer metin değil, `True`.

### Dört fonksiyon, iki soru

`json` modülündeki dört fonksiyon kafa karıştırır. İki soruyla ayırt edilir:
**hangi yöne** (sözlükten metne mi, metinden sözlüğe mi) ve **nereye** (dosyaya mı,
bir metne mi)? Sonunda **s** olanlar metinle (string) çalışır.

| Fonksiyon | Yön | Nereye / nereden | Bu konuda nerede |
|---|---|---|---|
| `json.dumps(sozluk)` | sözlük → metin | ekrana basmak için metin | ham yanıtı görmek |
| `json.dump(sozluk, dosya)` | sözlük → metin | doğrudan dosyaya | `cevaplar.json` yazmak |
| `json.load(dosya)` | metin → sözlük | dosyadan | kayıtlı yanıtı okumak (Adım 3) |
| `json.loads(metin)` | metin → sözlük | bir metinden | (`cevap.json()` bunu senin yerine yapar) |

> **Kendini dene 4.** Sunucudan şu yanıt geldi:
>
> ```json
> {"success": false, "result": null, "errors": [{"code": 10000, "message": "Authentication error"}]}
> ```
>
> (a) Python'da `yanit["success"]` neye eşit?
> (b) `yanit["result"]`?
> (c) Hata mesajını hangi ifadeyle alırsın?
> (d) Buna rağmen `yanit["result"]["response"]` yazarsan ne olur?

---

## Adım 3 — Metni içinden çek

`03_yaniti_coz.py` sunucuya gitmez; `veri/ornek_yanit.json` dosyasında kayıtlı duran
bir yanıtı okur. Bu yüzden **anahtarsız da çalışır**. Konu kayıtlı bir JSON yanıtının
içine girmek; yanıt ister sunucudan, ister dosyadan gelsin, içi aynı.

```python
with open("veri/ornek_yanit.json", encoding="utf-8") as dosya:
    yanit = json.load(dosya)

print(list(yanit.keys()))
print(list(yanit["result"].keys()))
```

```text
['result', 'success', 'errors', 'messages']
['response', 'usage']
```

`keys()` bir sözlüğün anahtarlarını verir. Her satır bir sonraki adımın yolunu
gösteriyor: en dışta `result` var, onun içinde `response` var, demek ki
`yanit["result"]["response"]`.

> **Kural:** Yanıtın yapısını bilmiyorsan önce katlarını sor, sonra içine gir.
> Dönemin geri kalanında en çok kullanacağın alışkanlık bu.

Bu kural sadece bugünkü model için değil. Konu 8'de görsel üreten bir modele, Konu 10'da
video üreten bir modele istek atacağız; yanıtların yapısı farklı olacak. Her
seferinde aynı yöntemle keşfedeceğiz: katları tek tek sorarak.

```python
metin = yanit["result"]["response"]
print(metin)

kullanim = yanit["result"]["usage"]
print("Harcanan belirteç:", kullanim["total_tokens"])
```

```text
1) Sessizliğin adresi. 2) Kahven, prizin, zamanın. 3) Burada odaklanırsın.
Harcanan belirteç: 46
```

- İki kat içeri giriyoruz: önce `result`, sonra `response`.
- `yanit["response"]` yazarsan **KeyError** alırsın; bu konunun en sık hatası.
- `errors` bir **liste**; ilk hatanın mesajı: `yanit["errors"][0]["message"]`.

### Kaç belirteç harcadık?

`usage` üç sayı tutar; dosya yalnızca toplamı basıyor:

- `prompt_tokens`: senin sorun kaç parçaya bölündü.
- `completion_tokens`: modelin cevabı kaç parça tuttu.
- `total_tokens`: ikisinin toplamı.

Belirteç (token) kelime değil, kelime parçasıdır; ayrıntısı Konu 5'te. Ücretsiz
kotan günde 10.000 **neuron** adlı bir birimle ölçülür; belirteç sayısı bu harcamanın
kaba bir göstergesidir. Uzun soru ve uzun cevap daha çok harcar.

Küçük bir karşılaştırma yapalım: cevabın kaç kelime, kaç belirteç olduğu.

```python
kelime_sayisi = len(metin.split())
print("Cevap:", kelime_sayisi, "kelime,", kullanim["completion_tokens"], "belirteç")
```

Kayıtlı yanıtta `split()` 10 kelime sayıyor (numaralar dahil), model ise 22 belirteç.
Yani bir kelime ortalama iki parçadan fazla. Türkçede kelimeler eklerle uzadığı için (`odaklanırsın`,
`sessizliğin`) bir kelime çoğu zaman birkaç parçaya bölünür. Kendi anahtarınla
kendi sorunun sayılarına bak; Konu 5'te bunun neden önemli olduğunu göreceğiz.

---

## Adım 4 — Hata kodları

Durum kodları üç haneli sayılardır ve **ilk hane** sana kimin tarafına bakacağını
söyler:

| İlk hane | Anlamı | Nereye bakmalı |
|---|---|---|
| **2**xx | Başarılı | — |
| **4**xx | İstekte sorun var: **senin tarafın** | Anahtar, adres, gövde |
| **5**xx | Sunucuda sorun var: **onların tarafı** | Kodunu değiştirme, bekle |

Bu konuda karşına çıkabilecekler:

| Kod | Anlamı | Ne yapmalı |
|---|---|---|
| **200** | Her şey yolunda | — |
| **400** | İstek bozuk | Gövdede yanlış ya da eksik bir alan var (`prompt` yazımı, `json=` yerine `data=`) |
| **401** | Yetki yok | Anahtarı kontrol et; kopyalarken bir karakter düşmüş, tırnak kalmış ya da `Bearer`'dan sonraki boşluk unutulmuş olabilir |
| **403** | İzin yok | Anahtarın izinleri eksik; kurulum yönergesindeki gibi "Create a Workers AI API Token" düğmesiyle yeniden üret |
| **404** | Adres yanlış | Model adını ve hesap kimliğini kontrol et |
| **429** | Kota doldu | Günlük kota her gün 00:00 UTC'de (Türkiye saatiyle 03:00) sıfırlanır; bekle |
| **500** | Sunucu hatası | Senin kodunda sorun yok, biraz sonra tekrar dene |

Adres ya da model adı yanlış olduğunda sunucu bazen 404 yerine 400 döndürür. Bu
yüzden koda ek olarak **sunucunun kendi açıklamasını** da oku: `errors` listesindeki
`message` alanı çoğu zaman sorunu tek cümleyle söyler.

### 401'i canlı görmek

**(anahtar gerekir)** `04_hata_kodlari.py` hesap kimliğini dosyadan okur ama başlığa
kasten **sahte** bir anahtar koyar, sonra durum koduna bakar:

```python
sahte_basliklar = {"Authorization": "Bearer bu-anahtar-sahte"}

cevap = requests.post(adres, headers=sahte_basliklar, json={"prompt": "merhaba"}, timeout=60)

if cevap.status_code == 200:
    print(cevap.json()["result"]["response"])
else:
    print("İstek başarısız:", cevap.status_code)
    print(cevap.text)
```

- `if cevap.status_code == 200:` önce durum koduna bakar; ancak 200 ise içine girer.
- `cevap.text` sunucunun gönderdiği ham metindir; sözlüğe çevrilmemiş hâli. Hata
  açıklaması orada yazar.

Sunucunun gönderdiği yanıt şuna benzer:

```json
{
  "result": null,
  "success": false,
  "errors": [{"code": 10000, "message": "Authentication error"}],
  "messages": []
}
```

Dikkat: `result` bu sefer `null`. Yani sözlük değil, "hiçbir şey". İçine girmeye
çalışırsan:

```text
TypeError: 'NoneType' object is not subscriptable
```

Bu mesaj "`None`'ın içine köşeli parantezle giremezsin" demek. Yeni başlayanlar bu
hatayı görünce kodlarında bir yazım hatası arar; oysa kodun doğru, **istek başarısız
olmuş**. Asıl sebep bir önceki satırda: durum kodu 200 değildi.

### Yanıtı okuma sırası

`04_hata_kodlari.py`'deki `if` bir yanıtı okuma sırasının ta kendisi:

1. **Durum koduna bak.** 200 değilse içine girme; kodu ve sunucunun mesajını bas.
2. **200 ise** `result` katına, oradan `response`'a in.

### İstersen: kodu açıklamaya çevirmek

Her koda bir açıklama yazan bir sözlük ve Konu 1'deki `.get` kalıbı yeterli. Örnek
dosyada yok; istersen `04`'ün kopyasına ekleyebilirsin:

```python
HATA_SOZLUGU = {
    200: "Her şey yolunda.",
    401: "Yetki yok. Anahtarı kontrol et.",
    429: "Kota doldu. 00:00 UTC'de sıfırlanır.",
}
print(HATA_SOZLUGU.get(401, "Tanımadığım bir kod."))
print(HATA_SOZLUGU.get(418, "Tanımadığım bir kod."))
```

```text
Yetki yok. Anahtarı kontrol et.
Tanımadığım bir kod.
```

`HATA_SOZLUGU[418]` yazsaydık `KeyError` alırdık; `.get` tanımadığı kodda bile
program durmasın diye yedek cümleyi döndürür.

> **Kendini dene 5.** Her durumda ne görürsün, ne yaparsın?
> (a) Akşam 50 soruluk bir döngü çalıştırdın; 38. sorudan sonra her isteğin durum
>     kodu `429`.
> (b) Panelden yeni token ürettin, eskisini sildin ama `anahtar.txt` dosyasını
>     güncellemeyi unuttun.
> (c) Wi-Fi kapalıyken programı çalıştırdın.
> (d) Dün çalışan program bugün `500` veriyor; kodunda hiçbir şeyi değiştirmedin.

---

## Adım 5 — Soruyu fonksiyona koy

**(anahtar gerekir)** `05_soru_sor.py`, `02`'deki gibi anahtarı okuyup `adres` ve
`basliklar`'ı hazırlayarak başlar. Sonra iki adımı (gönder, metni çek) tek isim
altında topluyoruz:

```python
def modele_sor(soru):
    cevap = requests.post(adres, headers=basliklar, json={"prompt": soru}, timeout=60)
    return cevap.json()["result"]["response"]
```

**Neden fonksiyon?** Az sonra aynı işi beş kez, ileride elli kez yapacağız. Beş
satırı her soru için kopyalamak hem uzun hem tehlikeli: birinde `Bearer`'ın
boşluğunu unutursun, beşten biri bozulur. Fonksiyonda bir kez doğru yazarsın, hep
doğru çalışır.

**`adres` ve `basliklar` nereden geliyor?** Fonksiyonun dışında, dosyanın üstünde bir
kez hazırlandılar; fonksiyon onları oradan kullanıyor. Fonksiyona yalnızca her
seferinde değişen şeyi, yani soruyu veriyoruz. Anahtar yine koda yazılmıyor:
dosyadan okunuyor.

**İstek başarısız olursa?** Fonksiyon durum koduna bakmıyor. Kota bitmişse ya da
anahtar yanlışsa `result` boş gelir ve program
`TypeError: 'NoneType' object is not subscriptable` ile durur. Böyle bir hata görürsen
Adım 4'e dön: `04_hata_kodlari.py`'deki `if` ile durum koduna bak.

Artık tek satırla soru sorabiliriz: `modele_sor("Sessiz bir çalışma kafesi için üç renk öner.")`.

### Konunun çıktısı

```python
soru = input("Modele ne sormak istiyorsun? ")
metin = modele_sor(soru)
print(metin)

with open("cevap.txt", "w", encoding="utf-8") as dosya:
    dosya.write(f"SORU: {soru}\n\nCEVAP:\n{metin}\n")
```

- `input()` programı durdurup senden bir satır bekler; yazdığın metni döndürür.
- Cevap hem ekrana hem Konu 1'deki gibi dosyaya yazılır.
- `\n` satır sonu demek; `\n\n` araya boş bir satır koyar. `cevap.txt` şu biçimde
  olur (cevap kısmı modelin yazdığı metin):

```text
SORU: Sessiz bir çalışma kafesi için üç renk öner.

CEVAP:
...
```

- `"w"` kipi dosyayı **her seferinde sıfırdan** yazar. Programı ikinci kez
  çalıştırırsan ilk cevap silinir. Bunu bilerek seçtik: `cevap.txt` hep son soruyu
  tutar. Bütün cevapları biriktirmek Adım 6'nın işi.

---

## Adım 6 — Aynı işi beş kez yap

**(anahtar gerekir)** `06_coklu_soru.py`, `05` gibi anahtarı okuyup `modele_sor`'u
tanımlayarak başlar. Sonra soruları `veri/ornek_sorular.txt` dosyasından satır satır
okuyup `sorular` listesine koyar. Hazır dosyadaki beş soru aynı konuda: Konu 1'in
bulgusuyla, sessiz bir çalışma kafesinin yeni kimliği (slogan, renk, yazı tipi,
gönderi fikri, kaçınılacak klişeler). Kendi sorularını sormak için bu iki dosyayı
değiştirme, kopyala: soru dosyasını `veri` klasöründe, `06_coklu_soru.py`'yi `ornekler`
klasöründe yeni bir adla kopyala. Sorularını kopyaya yaz, `06`'nın kopyasında da
`open("veri/ornek_sorular.txt", ...)` satırındaki yolu yeni dosyana çevir. Depodaki dosyalara dokunmazsan
`git pull` çakışmaz.

```python
sorular = []
with open("veri/ornek_sorular.txt", encoding="utf-8") as dosya:
    for satir in dosya:  # her satır bir soru
        sorular.append(satir.strip())

kayitlar = []
for soru in sorular:
    print(soru)
    kayitlar.append({"soru": soru, "cevap": modele_sor(soru)})

with open("cevaplar.json", "w", encoding="utf-8") as dosya:
    json.dump(kayitlar, dosya, ensure_ascii=False, indent=2)
```

- Her soru–cevap çifti bir sözlük; bunların her birine **kayıt** diyoruz. Sonuç bir
  **liste** içinde **sözlükler**. Konu 3'ten itibaren veri hep bu biçimde gelecek.
- `print(soru)` sadece ilerlemeyi görmek için: beş istek birkaç saniye sürer.
- Soru dosyasında boş satır bırakma: boş satır da bir "soru" olarak modele gider.
- `json.dumps` (sonunda **s**) sözlüğü metne çevirip ekrana basmak içindi;
  `json.dump` doğrudan **dosyaya** yazar. İkinci bilgiyi, yani dosyayı vermeyi
  unutursan: `TypeError: dump() missing 1 required positional argument: 'fp'`
  (`fp` dosya demek).
- Kodun asıl gücü burada: aynı işi elli kez yapmak, arayüzde yapamayacağın şey.
  Sohbet penceresine elli soruyu tek tek yapıştırıp cevapları tek tek kopyalamayı
  düşün.

`cevaplar.json` dosyasının biçimi (cevaplar modelin yazdığı metinler):

```json
[
  {"soru": "Müşterilerinin sessiz bir çalışma yeri ... üç kısa slogan yaz.",
   "cevap": "..."},
  {"soru": "Sessiz bir çalışma kafesinin logosu için hangi üç rengi önerirsin, neden?",
   "cevap": "..."}
]
```

### Kaydettiğini geri oku

Dosyaya yazmanın asıl faydası, sonradan açıp üzerinde çalışabilmek. Bonus dosya
`08_cevap_raporu.py` `cevaplar.json`'u okur ve her cevabın kaç kelime olduğunu yazar:

```python
with open("cevaplar.json", encoding="utf-8") as dosya:
    kayitlar = json.load(dosya)
```

```python
butun_metin = ""
for kayit in kayitlar:
    print(len(kayit["cevap"].split()), "kelime:", kayit["soru"])
    butun_metin = butun_metin + " " + kayit["cevap"]
```

Döngü her cevabın kelime sayısını basarken bütün cevapları da tek bir metinde
birleştiriyor.

- `for kayit in kayitlar` her adımda bir **sözlük** verir, metin değil. Bu yüzden
  `kayit.split()` değil, `kayit["cevap"].split()`. (Sınıf alıştırmasının 3. sorusu
  bu hatayı arıyor.)
- Gerçek modelle çalıştırınca cevap uzunlukları çok farklı çıkar: slogan sorusuna
  birkaç satır, gönderi fikri sorusuna uzun bir liste. Hangi soruya ne kadar
  uzun cevap geldiğine bakmak, hangi sorunun modeli "konuşturduğunu" gösterir.

`08` sonra aynı metinden Konu 1'deki kelime bulutunu üretir (`cevaplar-bulutu.png`).
Bu kez `WordCloud`'a sayacı değil metnin kendisini veriyoruz (`generate`); durak
kelimeleri `stopwords=` ile kütüphane eler. Kendi metnin değil, modelin yazdığı metin
hangi kelimelere yaslanıyor?

> **Kendini dene 6.** `06_coklu_soru.py`'yi çalıştırdın; üçüncü sorudan sonra program
> `TypeError: 'NoneType' object is not subscriptable` ile durdu ve `cevaplar.json`
> hiç oluşmadı. (a) İlk iki soru sorulmuştu; dosya neden yine de yok? (b) Sorunun ne
> olduğunu nasıl öğrenirsin?

---

## Adım 7 — Soru yazmak da bir tasarım kararı

Buraya kadar hep aynı uzun soruyu sorduk: "Müşterilerinin sessiz bir çalışma yeri
olarak anlattığı bir kafe için üç kısa slogan yaz." Neden sadece "Bir kafe için üç
kısa slogan yaz" demedik?

**(anahtar gerekir)** `09_baglam_farki.py` bu soruyu ölçüyor. Aynı isteği iki biçimde soruyor:

| Tür | Soru |
|---|---|
| **bağlamsız** | Bir kafe için üç kısa slogan yaz. |
| **bağlamlı** | Müşterilerinin sessiz bir çalışma yeri olarak anlattığı bir kafe için üç kısa slogan yaz. |

Her soruyu **üç kez** soruyor, çünkü model aynı soruya her seferinde başka cümleler
kurar; tek bir cevaba bakıp karar vermek yanıltıcı olur. Cevapları iki uzun metinde
biriktiriyor, ikisini de ekrana basıyor, sonra listedeki her kelimenin iki metinde kaç
kez geçtiğini sayıyor. Listenin ilk yarısı kahve klişeleri (`kahve`, `fincan`,
`aroma`...), ikinci yarısı çalışma yerini anlatan kelimeler (`sessiz`, `odak`, `priz`...).

```python
KELIMELER = ["kahve", "fincan", "aroma", "köpü", "yudum", "sessiz", "odak", "çalış", "priz", "sakin"]

baglamsiz = ""
baglamli = ""
for _ in range(3):  # model her seferinde başka cümle kurar; üçer kez soruyoruz
    baglamsiz = baglamsiz + modele_sor("Bir kafe için üç kısa slogan yaz.") + "\n"
    baglamli = baglamli + modele_sor("Müşterilerinin sessiz bir çalışma yeri olarak anlattığı bir kafe için üç kısa slogan yaz.") + "\n"

print(baglamsiz)
print(baglamli)

for kelime in KELIMELER:
    print(kelime, baglamsiz.lower().count(kelime), baglamli.lower().count(kelime))
```

- `for _ in range(3)` döngüyü üç kez döndürür; sayaca ihtiyacımız olmadığı için adı `_`.
- `metin.count(kelime)` bir metnin içinde başka bir metnin kaç kez geçtiğini sayar.
  Kelimenin sadece **başını** yazıyoruz: `kahve` hem `kahve`yi hem `kahveyle`yi
  yakalar.
- Listede neden `köpük` değil de `köpü` var? Türkçede ek alınca `k` harfi `ğ` olur:
  `köpük` → `köpüğü`. `köpük` diye arasaydık `Köpüğü bol` cümlesini kaçırırdık.
- Son döngünün her satırı üç şey basar: kelime, bağlamsız cevaplarda kaç kez geçtiği,
  bağlamlı cevaplarda kaç kez geçtiği.
- `lower()` Türkçe `I`'yı `ı` değil `i` yapar (Konu 1'deki sorun). Listedeki
  kelimelerde `ı` olmadığı için burada sorun çıkarmaz.

**Bulguyu kendi sayılarınla kur.** Bağlamsız cevaplarda kahve kelimeleri mi çok?
Bağlamlı cevaplarda `sessiz`, `odak`, `priz` geçiyor mu? Beklenen örüntü şu: bulguyu
söylemezsen model "ortalama bir kafe"yi anlatır; Konu 1'de 30 yorumu sayarak
bulduğumuz şey (müşteri buraya çalışmaya geliyor) ancak soruya yazınca cevaba girer.
Model senin kafeni tanımıyor; ona ne söylersen onu biliyor. Soruyu yazmak, bir brief
yazmak gibi bir tasarım işi.

Örüntü senin sayılarında çıkmıyorsa cevapları oku; belki model başka klişelere
(`sıcak`, `sohbet`) yaslanıyor ve listeye eklemen gerekiyor.

**Sayımın sınırı:** "Kahven, prizin, zamanın." gibi bir cümle sayımda bir `kahve`
olarak görünür, ama kahveyi övmüyor; çalışma düzeninin bir parçası olarak anıyor.
Sayım yön gösterir; kararı cevapları okuyarak sen verirsin.

Ödevdeki soru ("beş cevaptan hangisi işe yaramazdı, neden?") buraya bağlanıyor:
işe yaramayan bir cevabın sebebi çoğu zaman modelde değil, **soruda** eksik kalan
bağlamdadır.

> **Kendini dene 7.** (a) Bağlamsız cevaplardan biri "Her yudumda mutluluk" diyor.
> Listede `yudum` olmasaydı sayım ne kaçırırdı? (b) "Sessiz bir çalışma kafesinin
> Instagram hesabı için beş gönderi fikri ver" sorusuna bir bağlam daha ekleyecek
> olsan Konu 1'in bulgularından hangisini eklerdin?

---

## Adımlar ve dosyalar

| Adım | Ne yaptık | Elimizde ne oluştu | Dosya |
|---|---|---|---|
| — | İç içe sözlük provası | — | `00_isinma.py` |
| 1 | Anahtarı okuduk | `hesap`, `anahtar` | `01_anahtar_oku.py` |
| 2 | İsteği kurup gönderdik | `yanit` | `02_ilk_istek.py` |
| 3 | Metni çektik, belirteç saydık | `metin` | `03_yaniti_coz.py` |
| 4 | Hata kodunu okuduk | `if cevap.status_code == 200` | `04_hata_kodlari.py` |
| 5 | Fonksiyona sardık, soru alıp kaydettik | `modele_sor()`, `cevap.txt` | `05_soru_sor.py` |
| 6 | Döngüye soktuk | `cevaplar.json` | `06_coklu_soru.py` |
| 7 | Bağlamın etkisini ölçtük | kelime sayımı | `09_baglam_farki.py` |

Her dosyayı konunun klasöründen (`02-api-ile-konusmak`) çalıştır:
`uv run ornekler/01_anahtar_oku.py`. Ürettikleri dosyalar (`cevap.txt`, `cevaplar.json`)
de bu klasöre yazılır.

`02`, `04`, `05`, `06` ve `09` aynı anahtar okuma satırlarıyla; `06` ve `09` ayrıca
`05`'teki `modele_sor` fonksiyonuyla başlar. Her dosya tek başına çalışsın diye böyle.
Kendi programında bunları yeniden yazmana gerek yok.

Derste kendi başına dolduracağın alıştırma: `alistirma/sinif_alistirmasi.py`.
Ek alıştırma: `07_bozuk_kodlar.py` (beş bozuk parça; anahtar gerekmez, vizedeki soru
tipine benzer). Dosya ilk çalıştırmada hata verir; parçaları sırayla düzelt, her
düzeltmeden sonra yeniden çalıştır. Depodaki dosyayı değil, yeni bir adla kopyasını düzelt. Bonus: `08_cevap_raporu.py` (cevaplarından kelime bulutu, Konu 1'in
kodu yeni veriyle). Önce `06` çalışmış olmalı; çıktısı `cevaplar-bulutu.png`.

---

## Sık karşılaşılan sorunlar

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `FileNotFoundError: ... '../anahtar.txt'` | Hesap açılmamış, dosya yanlış klasörde ya da adı `anahtar.txt.txt` | Dosyayı `gita3111` klasörüne (konu klasörlerinin bir üstüne) koy, uzantıyı kontrol et; komutu konu klasöründen verdiğinden emin ol. Anahtarın yoksa derste yanındakiyle çalış |
| `FileNotFoundError: ... 'veri/...'` | Komutu yanlış klasörden verdin | `cd` ile konu klasörüne (`02-api-ile-konusmak`) geç |
| `ModuleNotFoundError: No module named 'requests'` | Dosyayı `uv run` yerine `python` ile ya da konu klasörünün dışından çalıştırdın | Konu klasöründe `uv run ...`; olmazsa orada `uv sync` |
| `KeyError: 'ACCOUNT_ID'` ya da `KeyError: 'API_TOKEN'` | Dosyada o satır yok ya da adı farklı yazılmış (küçük harf, boşluk) | Dosyayı Adım 1'deki biçime göre düzelt |
| `KeyError: 'response'` | Bir kat atlandı | `yanit["result"]["response"]`; emin değilsen önce ham yanıtı bas |
| `TypeError: list indices must be integers or slices, not str` | `errors` listesini adla açtın | `yanit["errors"][0]["message"]` |
| `TypeError: 'NoneType' object is not subscriptable` | İstek başarısız, `result` boş | Önce durum koduna bak |
| `requests.exceptions.ConnectionError` | İstek sunucuya ulaşmadı | İnternet bağlantını kontrol et |
| `requests.exceptions.ReadTimeout` | Sunucu 60 saniyede cevap vermedi | Biraz sonra tekrar dene |
| `requests.exceptions.JSONDecodeError` | Gelen içerik JSON değil | `print(cevap.status_code, cevap.text[:300])` |
| `TypeError: dump() missing 1 required positional argument: 'fp'` | `json.dump`'a dosyayı vermedin | `json.dump(kayitlar, dosya, ...)` |
| JSON dosyasında `ı` gibi harfler | `ensure_ascii=False` yazılmamış | Ekle; veri bozuk değil, sadece okunmuyor |
| 401 / 403 / 429 | Anahtar, izin ya da kota | Yukarıdaki hata kodları tablosu |

---

## Bu konuda öğrendiklerin

- **API**, programların birbirine soru sorduğu kapıdır. Model senin bilgisayarında
  değil, uzakta çalışır; bu yüzden internet, kota ve kimlik gerekir.
- **Anahtar senin kimliğindir:** koda yazılmaz, ayrı dosyada durur, teslime konmaz,
  ekranda gösterilmez. Sızarsa silip yenisini üretirsin.
- **Dosyayı satır satır okumak:** `for satir in dosya`, `partition`, `strip`.
  Dosyalar programı çalıştırdığın klasöre göre aranır; `..` bir üst klasör demek.
- **Bir istek üç parçadır:** adres (nereye), başlık (kim), gövde (ne). `requests.post`
  üçünü birlikte gönderir.
- **JSON** sözlük ve listelerin metin hâlidir. `true`/`null` Python'da `True`/`None`
  olur. `dumps`/`dump`/`load`/`loads` farkını iki soruyla ayırırsın: hangi yön, nereye.
- **Yanıtı okuma sırası:** önce durum kodu, sonra içerik. Yapıyı bilmiyorsan önce ham
  hâlini bas, sonra kat kat içine gir.
- **Durum kodunun ilk hanesi** kimin tarafına bakacağını söyler: 4xx senin, 5xx
  sunucunun.
- **Fonksiyon ve döngü** aynı isteği beş, elli kez tekrarlamanı sağlar; sonuç bir
  liste içinde sözlükler olarak dosyaya yazılır.
- **Soruya yazdığın bağlam cevabı değiştirir.** Model senin bulgunu bilmez; ona
  söylemezsen ortalama bir cevap verir.

## Bu konunun tek cümlesi

> Bir istek üç şeyden oluşur: nereye, kim olduğun, ne istediğin. Gelen cevap da
> düz metin değil, içine girilecek bir sözlüktür.

---

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **API** | Bir programın başka bir programa soru sorabildiği kapı; bu konuda Cloudflare'in yapay zeka servisi |
| **İstemci** | İsteği gönderen taraf; burada senin Python programın |
| **Sunucu** | İsteği karşılayıp cevap veren uzaktaki bilgisayar |
| **Uç nokta (endpoint)** | İsteğin gönderildiği tam adres |
| **Başlık (header)** | İstekle giden kimlik ve ek bilgiler; burada `Authorization` |
| **Gövde (body)** | İsteğin asıl içeriği; burada `{"prompt": soru}` |
| **Anahtar / API token** | Sunucuya kim olduğunu kanıtlayan gizli metin |
| **Hesap kimliği (Account ID)** | Hangi hesabın modelinin çalışacağını söyleyen kimlik |
| **Durum kodu** | Sunucunun işin nasıl gittiğini söyleyen üç haneli sayısı (200, 401, 429...) |
| **JSON** | Sözlük ve listelerin metin olarak yazılmış, bilgisayarlar arasında taşınan hâli |
| **Belirteç (token)** | Modelin metni böldüğü kelime parçaları; harcamanın kaba ölçüsü |
| **Neuron** | Cloudflare'in ücretsiz kotayı ölçtüğü birim; günde 10.000 |
| **Kota** | Bir günde kullanabileceğin ücretsiz harcama sınırı |
| **Zaman aşımı (timeout)** | Cevap için beklenecek en uzun süre; burada 60 saniye |
| **Bağlam** | Soruya eklediğin ve modelin bilmediği bilgi; burada Konu 1'in bulgusu |
| **Kayıt** | Tek bir soru–cevap çifti; bir sözlük |

---

## Kendini dene — cevaplar

**1.** (a) `yanit["result"]["usage"]["completion_tokens"]` → `2`.
(b) `IndexError: list index out of range`. `errors` listesi boş; sıfırıncı eleman
bile yok. (c) `KeyError: 'usage'`. `usage` en dıştaki sözlükte değil, `result`
içinde; bir kat atlandı.

**2.** Sözlük şu olur:
`{'account_id': 'a1b2', 'API_TOKEN': '"xyz789"', 'not: bu satırda eşittir yok': ''}`.
Eşittir içermeyen not satırı da sözlüğe girer (değeri boş), ama zararsızdır. Program
`hesap = anahtarlar["ACCOUNT_ID"]` satırında `KeyError: 'ACCOUNT_ID'` ile durur:
satır adı küçük harfle yazıldığı için `ACCOUNT_ID` diye bir anahtar yok. Adı
düzeltsen bile token'ın değeri tırnaklarla birlikte okunur: `"xyz789"`. İstek atarsan
sunucu tırnaklı token'ı tanımaz ve **401** döner. Çare: adı büyük harfle yaz,
tırnakları sil.

**3.** (a) Başlık: `Bearer`'dan sonra boşluk yok, sunucuya `Bearerxyz...` gider →
**401**. (b) Adres: baştaki `f` yok; adrese hesap kimliği yerine `{hesap}` yazısı
gider → sunucu böyle bir hesap bulamaz, 4xx türünde bir hata döner. (c) Gövde:
sunucu soruyu `prompt` alanında bekliyor, `soru` alanını tanımıyor → **400**.

**4.** (a) `False`. (b) `None`. (c) `yanit["errors"][0]["message"]` →
`"Authentication error"`. (d) `TypeError: 'NoneType' object is not subscriptable`;
`result` boş olduğu için içine girilemez. Önce durum koduna ya da `success`
alanına bakmak gerekirdi.

**5.** (a) **429**: günlük kota bitti. Türkiye saatiyle 03:00'te sıfırlanır.
Döngüyü küçült, soruları kısalt; kota dolunca beklemekten başka çare yok.
(b) **401**: eski token silindiği için artık geçersiz. `anahtar.txt`'yi güncelle.
(c) Durum kodu gelmez, program `ConnectionError` ile durur; istek sunucuya hiç
ulaşmadı. (d) **500** sunucu tarafı demek; kodunu değiştirme, biraz sonra tekrar dene.

**6.** (a) `json.dump` döngüden **sonra** geliyor. Döngü üçüncü soruda hatayla
durunca program o satıra hiç ulaşmadı; ilk iki cevap sadece bellekteydi ve kayboldu.
(b) Hata `result`'ın boş geldiğini söylüyor, yani istek başarısız oldu. Sebebi durum
kodunda: `04_hata_kodlari.py`'deki gibi `cevap.status_code`'u bas (ya da `modele_sor`'a
o `if`'i ekle). 429 ise kota bitmiştir, 401 ise anahtar yanlıştır.

**7.** (a) O cevabı klişesiz sayardı; "yudum" kahveyi doğrudan söylemeden anıyor.
Sayım sadece listede yazan kelimeleri görür; listeyi cevapları okuyarak genişletmek
gerekir. (b) Örneğin "müşteriler en çok priz ve internetten bahsediyor" ya da
"müşterilerin çoğu öğrenci". Doğru cevap yok; önemli olan, modelin bilemeyeceği ve
senin veriden bulduğun bir bilgiyi eklemek.

---

## Ödev — iki parça

`odevler/odev2.md` (puansız; sırası gelen sınıfta gösterir):

1. **Kendi beş sorun:** soru dosyasının kopyasına aynı konuda kendi beş sorunu yaz,
   `06_coklu_soru.py`'nin kopyasıyla çalıştır (Adım 6), `cevaplar.json` dosyanı getir. Bir de tek cümle: beş cevaptan hangisi
   işe yaramazdı, sence neden? (Adım 7'yi hatırla: sebep soruda olabilir.)
2. **Renk etiketleme:** `veri/renkler.csv` içindeki 20 renge sakin / enerjik / ciddi
   etiketi ver.

İkinci parça **Konu 3'ün verisi**. Yapılmazsa eğitecek veri olmaz. Doğru cevap
yok; herkesin etiketi farklı olacak, mesele de bu.

Birinci parça gerçek anahtar ister.

## Sonraki konu

**Konu 3 — Makine öğrenmesi** (`03-makine-ogrenmesi`). Bu konuda hazır bir modele
soru sorduk. Konu 3'te kendi modelimizi eğiteceğiz, hem de sınıfın ödevde verdiği
renk etiketleriyle.
