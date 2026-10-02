# Konu 2 — İnterneti Koddan Konuşturmak (API)

Bu not konunun özetidir; derste çalıştırdığımız `ders.ipynb` defteriyle **aynı sırada**
ilerler: Isınma, sonra Adım 1–8. Derste kaçırdığın bir yer olursa buradan oku, sonra
defterde o adımın hücrelerini çalıştır.

**Konu 1'de:** bilgisayarındaki bir metni işledik. Kafe yorumlarını sayınca bir bulgu
çıktı: müşteriler kafeyi kahvesiyle değil, **sessiz bir çalışma yeri** olarak anlatıyor.

**Bu konuda:** kodun ilk kez bilgisayarının dışına çıkıyor. Uzaktaki bir yapay zeka
modeline soru gönderip cevabını alacağız. Soracağımız sorular da o bulgudan geliyor:
sessiz bir çalışma kafesinin yeni kimliği için slogan, renk, yazı tipi.

**Konunun sonunda elinde:**

- modele tek satırla soru soran bir fonksiyon (`modele_sor`),
- birkaç soruyu tek seferde sorup cevapları bir dosyada toplayan bir hücre
  (`cevaplar.txt`),
- ve bir bulgu: **soruya bağlam yazmak cevabı nasıl değiştiriyor?**

**Kurulum (dersten önce):** konunun klasörüne gir (`cd 02-api-ile-konusmak`) ve bir kez
`uv sync` çalıştır. Bu konunun kütüphanesi (internete istek atan `requests`) ve defteri
çalıştıran parça klasördeki `pyproject.toml` dosyasında yazılı; `uv sync` onları indirip
klasörün içinde bir `.venv` klasörü kurar.

**Defteri açmak:** VS Code'da `02-api-ile-konusmak` klasöründeki `ders.ipynb`'yi aç.
Sağ üstten çekirdek (kernel) olarak bu klasörün **`.venv`**'ini seç. Sonra hücreleri
yukarıdan aşağı, **Shift + Enter** ile sırayla çalıştır.

> Bu dönemin **kritik konusu**: Konu 4, 5, 8, 9, 10 ve 11 bunun üstüne kuruluyor.
> Buradaki her adım ileride her derste tekrar edecek. Anlamadığın bir yer kalırsa
> şimdi sor; sonra sormak çok daha pahalı.

### Bu not nasıl okunur

- Her adımda üç şey var: **ne yapıyoruz**, **neden gerekiyor**, **atlarsan ne olur**.
- Buradaki kod blokları defterdeki hücrelerin aynısı. Notu okurken defter yanında açık
  dursun.
- `Kendini dene` kutuları küçük kontrol sorularıdır. Cevapları notun sonunda.
- Adım 1'den sonraki hücreler `anahtar.txt` ister ve gerçekten internete çıkar; bu
  adımların başında **(anahtar gerekir)** yazıyor. Anahtarsız çalışanlar: Isınma ve
  alıştırma defteri (`alistirma.ipynb`).
- Modelin cevaplarını bu notta yazmıyoruz: model her seferinde başka cümle kurar, senin
  ekranındaki cevap buradakiyle zaten aynı olmazdı. Cevabın yerinde `(modelin cevabı)`
  yazıyorsa, orada kendi ekranındaki metni düşün.

---

## Defterle çalışmak

Konu 1'de kodu `.py` dosyalarına yazıp terminalden çalıştırıyorduk. Bu konuda kod bir
**defterde** (`.ipynb`) duruyor. Defter küçük kutulardan oluşur; her kutuya **hücre**
denir. İki tür hücre var:

- **Yazı hücresi:** açıklama. Çalıştırılmaz, okunur.
- **Kod hücresi:** Python. Shift + Enter ile çalışır, çıktısı hemen altında görünür.

Üç kural:

1. **Sırayla çalıştır.** Bir hücrede tanımlanan değişken (`hesap`, `adres`...) sonraki
   hücrelerde kullanılır. Bir hücreyi atlarsan sonraki hücre şunu verir:

   ```text
   NameError: name 'hesap' is not defined
   ```

   "`hesap` diye bir şey tanımlanmadı" demek. Atladığın hücreye dön, oradan devam et.

2. **Hücrenin solundaki işaret** ne olduğunu söyler: `[*]` hâlâ çalışıyor (örneğin
   sunucudan cevap bekliyor), `[5]` bitti ve sıradaki beşinci çalıştırılan hücreydi.

3. **Takılırsan baştan başla.** Üstteki menüden "Restart" (çekirdeği yeniden başlat)
   bütün değişkenleri siler; sonra hücreleri yine en baştan sırayla çalıştır.

Defter kendi durduğu klasörü **çalışma klasörü** kabul eder. `ders.ipynb`
`02-api-ile-konusmak` içinde duruyor; içindeki `"../anahtar.txt"` yolu da bu yüzden
doğru yeri gösteriyor (Adım 1'de ayrıntısı var).

---

## Isınma: iç içe sözlük

Birazdan sunucudan gelecek cevap, **sözlüğün içinde bir sözlük** olacak. Isınma onun
provası: önce elle bir tane kuruyoruz. Defterdeki ilk kod hücresi bilerek hata veriyor:

```python
yanit = {
    "success": True,
    "result": {"response": "Merhaba!"},
}

print(yanit["response"])
```

```text
KeyError: 'response'
```

`yanit` sözlüğünde iki anahtar var: `success` ve `result`. `response` bunların arasında
yok; `result`'ın değeri olan **içteki sözlüğün** içinde. Yani bir kat atladık.

Doğrusu **katman katman inmek**. Her satır bir kat iner ve bulduğunu yeni bir değişkene
koyar:

```python
sonuc = yanit["result"]
print(sonuc)
```

```text
{'response': 'Merhaba!'}
```

```python
metin = sonuc["response"]
print(metin)
```

```text
Merhaba!
```

Satırları sesli oku: "`yanit`'ın içinden `result`'ı al, adı `sonuc` olsun." "`sonuc`'un
içinden `response`'u al, adı `metin` olsun." Her cümle tek bir iş anlatıyor. Bu konunun
geri kalanında yanıtın içine hep böyle, kat kat gireceğiz.

| Değişken | Ne tutuyor | Türü |
|---|---|---|
| `yanit` | Bütün yanıt | sözlük |
| `sonuc` | `yanit["result"]`, içteki sözlük | sözlük |
| `metin` | `sonuc["response"]` | metin |

### Hata mesajını sondan oku

Python bir hata verdiğinde en önemli satır **en alttaki** satırdır: önce hatanın türü,
sonra açıklaması. Onun üstünde hatanın çıktığı satır gösterilir (defterde bir okla).

Bu konuda iki hata çok sık çıkacak:

```text
KeyError: 'response'
```

"Bu sözlükte `response` diye bir anahtar yok." Ya bir kat atladın ya da adı yanlış
yazdın (`Response`, `responce`). Sözlük anahtarları **harfi harfine** aranır.

```text
TypeError: 'NoneType' object is not subscriptable
```

"İçi boş bir şeyin (`None`) içine köşeli parantezle girmeye çalıştın." Bu konuda
neredeyse her zaman **istek başarısız olmuş** demektir. Adım 5'te canlı göreceğiz.

> **Kendini dene 1.** Isınmadaki `yanit` için:
> (a) `print(yanit["success"])` ne yazar?
> (b) `sonuc = yanit["result"]` satırından sonra `sonuc["result"]` yazarsan ne olur?
> (c) `sonuc = yanit["Result"]` yazarsan?

---

## Anahtarın yoksa?

Adım 1 `anahtar.txt` dosyasını okur. Dosya yoksa hücre durur:

```text
FileNotFoundError: [Errno 2] No such file or directory: '../anahtar.txt'
```

Adım 1'den sonraki bütün hücreler bu dosyadan okunan bilgiye dayanır. Anahtarın henüz
yoksa:

- Ders boyunca **yanındakiyle birlikte** çalış: istekleri onun ekranında izle, hücreleri
  sen de kendi defterine yaz.
- Isınma ve alıştırma defteri (`alistirma.ipynb`) internet istemez.
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
| 2. Yol | İstek internetten sunucuya gider | `ConnectionError`; **durum kodu yok** |
| 3. Kimlik | Sunucu anahtarına bakar | **401** ya da **403** |
| 4. İş | Sunucu modeli çalıştırır | **400**, **404**, **429** ya da **500** |
| 5. Dönüş | Yanıt sana gelir, sen içine girersin | `KeyError`, `TypeError` |

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
arkadaşına yardım edersin, sınıfta ekranını açarsın. Anahtar defterin içindeyse her
seferinde anahtarını da paylaşmış olursun. Ayrı dosyada durursa defteri rahatça
paylaşırsın, anahtar evde kalır.

Yanlışlıkla paylaşırsan panik yok, saklamaya da çalışma. Dört adım:

1. Cloudflare paneline gir, eski token'ı sil (artık kimse onunla istek atamaz).
2. Kurulum yönergesindeki gibi yeni bir token üret.
3. `anahtar.txt` içindeki `API_TOKEN` satırını yenisiyle değiştir.
4. Defterde Adım 1, 2 ve 3'ü yeniden çalıştır: durum kodu `200` olmalı.

Hepsi bir dakikadan kısa sürer.

> **Terim notu:** Bu derste "anahtar" dediğimiz şeye Cloudflare **API token** diyor.
> `anahtar.txt` içindeki `API_TOKEN` satırı ve hata mesajlarındaki "token" kelimesi
> aynı şeyi anlatıyor. İki karışıklığa dikkat:
> - Bu "anahtar", Konu 1'deki **sözlük anahtarı** değil; senin giriş kartın.
> - Konu 5'te göreceğin **belirteç** (İngilizcesi de "token") başka bir şey: kelime parçası.

---

## Adım 1 — Anahtarı dosyadan oku

**(anahtar gerekir)** `anahtar.txt` dosyan şöyle görünüyor:

```
ACCOUNT_ID = a1b2c3...
API_TOKEN = xyz789...
```

İki bilgi var: **hesap kimliği** (Account ID; hangi hesabın modeli çalıştırılacak)
ve **token** (sen misin). Hesap kimliği tek başına bir işe yaramaz; token ise
gizlidir.

Defterdeki hücre bu dosyayı satır satır okuyup bir **sözlüğe** koyar:

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

Konu 1'de dosyayı `dosya.read()` ile tek parça okumuştuk. Burada üç yeni şey var:

- `for satir in dosya` dosyayı **satır satır** gezer.
- `satir.split("=")` satırı eşittir işaretinden böler ve parçaları bir **liste** olarak
  verir. Konu 1'de `split()`'i boşluklardan bölmek için kullanmıştık; parantezin içine
  bir işaret yazarsan o işaretten böler.
- `.strip()` baştaki ve sondaki boşlukları (satır sonundaki görünmez `\n` dahil) siler.

Tek bir satırın yolculuğunu adım adım izleyelim:

| Aşama | Değer |
|---|---|
| Dosyadaki satır | `'API_TOKEN = xyz789\n'` |
| `parcalar = satir.split("=")` | `['API_TOKEN ', ' xyz789\n']` |
| `ad = parcalar[0].strip()` | `'API_TOKEN'` |
| `deger = parcalar[1].strip()` | `'xyz789'` |
| `anahtarlar[ad] = deger` | `anahtarlar["API_TOKEN"] = "xyz789"` |

Döngü bitince sözlükte iki kayıt var; son iki satır onları birer değişkene alıyor.
Satır adları **harfi harfine** aranır: `anahtarlar["ACCOUNT_ID"]` büyük harfle yazılmış
`ACCOUNT_ID` satırını bulur, `account_id` satırını bulmaz.

Anahtarı da hesap kimliğini de **ekrana basmıyoruz**; yalnızca okunduğunu söylüyoruz.
Ekran paylaşırken (derste, sunumda) bu ikisi görünmesin. Çıktı:

```text
Anahtar okundu
```

### Dosya nerede olmalı?

`open(...)` dosyayı **çalışma klasörüne** göre arar. Defterin çalışma klasörü, defterin
durduğu klasördür: `02-api-ile-konusmak`.

`anahtar.txt` ise bir üst klasörde, `gita3111`'in içinde duruyor; böylece bütün konular
aynı dosyayı kullanıyor. Yoldaki **`..`** "bir üst klasör" demek. `"../anahtar.txt"`,
"bulunduğum klasörden bir üste çık, oradaki `anahtar.txt`'yi aç" anlamına gelir:

```
gita3111/
├── anahtar.txt                  ← "../anahtar.txt" burayı gösterir
└── 02-api-ile-konusmak/         ← defterin çalışma klasörü
    ├── ders.ipynb
    └── veri/renkler.csv
```

Defterin kopyasını başka bir yere (örneğin Masaüstüne) taşırsan `..` artık başka bir
klasörü gösterir ve `FileNotFoundError` alırsın. Kopyaları hep aynı klasörde tut.

### Adım 1'de sık yapılan hatalar

| Ne oldu | Ne görürsün | Çare |
|---|---|---|
| Windows dosyayı `anahtar.txt.txt` diye kaydetti (uzantılar gizli) | `FileNotFoundError: ... '../anahtar.txt'` | Dosya gezgininde "Dosya adı uzantılarını göster"i aç, fazla `.txt`'yi sil |
| `anahtar.txt` konu klasörüne kondu | Aynı `FileNotFoundError` | Dosya bir üstte, `gita3111` klasöründe durmalı |
| Dosyada boş bir satır ya da `=` içermeyen bir satır var | `IndexError: list index out of range` | O satırı sil. `split("=")` o satırda tek parça verir, `parcalar[1]` yoktur |
| Değeri tırnak içine yazdın: `API_TOKEN = "xyz789"` | Okuma çalışır ama istek **401** döner | Tırnaklar da token'ın parçası sanılıyor; tırnakları sil |
| Satır adında boşluk ya da küçük harf: `API TOKEN = ...`, `api_token = ...` | `KeyError: 'API_TOKEN'` | Tam olarak `API_TOKEN` yaz: büyük harf, alt çizgi |
| Token'ı kopyalarken son karakteri kaçırdın | **401** | Token'ı panelden yeniden üretmek en hızlısı |

`IndexError`'a dikkat: dosyanın sonunda fazladan bir **boş satır** bırakmak (son satırdan
sonra iki kez Enter) bu hatayı vermeye yeter. Hata mesajı "listenin o sırasında eleman
yok" der; gerçek sebep dosyadaki boş satırdır.

> **Kendini dene 2.** `anahtar.txt` dosyasının içi şu olsun:
>
> ```
> account_id = a1b2
> API_TOKEN = "xyz789"
> not: bu satırda eşittir yok
> ```
>
> (a) Adım 1 hücresi hangi satırda, hangi hatayla durur?
> (b) Not satırını silersen bu sefer hangi hatayı alırsın?
> (c) Onu da düzeltirsen hücre çalışır. Bu dosyayla istek atınca ne olur?

---

## Adım 2 — İsteği hazırla: adres, başlık, gövde

Bir isteğin üç parçası var:

| Parça | Ne söyler | Kodda |
|---|---|---|
| **Adres** (endpoint, uç nokta) | Nereye gidiyorum | `adres` — bir metin |
| **Başlık** (header) | Ben kimim | `basliklar` — bir sözlük |
| **Gövde** (body) | Ne istiyorum | `govde` — bir sözlük |

Bir kargo gönderisi gibi düşünebilirsin: adres (kime gidiyor), gönderen bilgisi
(kimden geliyor) ve kutunun içi (ne gönderiliyor). Biri eksikse kargo ya yola
çıkmaz ya da geri döner.

```python
import requests

MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
basliklar = {"Authorization": f"Bearer {anahtar}"}
govde = {"prompt": "Sessiz bir çalışma kafesi için üç kısa slogan yaz."}
```

`import requests` internete istek atan kütüphaneyi getirir. Bu hücre hiçbir şey
basmaz ve internete de çıkmaz; yalnızca dört değişken hazırlar. İstek bir sonraki
adımda gidecek.

### Adres: parça parça

```
https://api.cloudflare.com  /client/v4  /accounts/{hesap}  /ai/run/{MODEL}
└──── sunucu ─────────────┘ └ sürüm ──┘ └─ hangi hesap ──┘ └─ hangi model ─┘
```

- Adresin içine `f"..."` ile hesap kimliğini ve model adını yerleştiriyoruz. Baştaki
  `f`, Python'a "süslü parantezlerin içine değişkenin değerini koy" der.
- Model adı `@cf/` ile başlar ve **harfi harfine** doğru olmalı. Dönem boyunca metin
  için hep aynı modeli kullanacağız: `@cf/meta/llama-3.3-70b-instruct-fp8-fast`.
- **En sık hata:** baştaki `f` harfini unutmak. O zaman Python süslü parantezleri
  doldurmaz ve sunucuya kelimesi kelimesine `.../accounts/{hesap}/...` gider.
  Sunucu "`{hesap}`" adında bir hesap bulamaz, istek hata koduyla döner. Şüphelenirsen
  `print(adres)` yaz: adreste anahtar yok, ekrana basmak güvenli.

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
  olarak anlatıyordu. Modelden o kafe için slogan istiyoruz. Soruya bu bilginin
  yazılmasının cevabı nasıl değiştirdiğini Adım 8'de göreceğiz.

> **Kendini dene 3.** Her satırda üç parçadan hangisi bozuk ve sunucu ne der?
> (a) `basliklar = {"Authorization": f"Bearer{anahtar}"}`
> (b) `adres = "https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"`
> (c) `govde = {"soru": "Üç slogan yaz."}`

---

## Adım 3 — Gönder

**(anahtar gerekir)** Bu hücre gerçekten internete çıkar.

```python
cevap = requests.post(adres, headers=basliklar, json=govde)
print(cevap.status_code)
```

Her şey yolundaysa çıktı:

```text
200
```

Satır satır:

- `requests.post`: "sana bir şey gönderiyorum, karşılığında cevap bekliyorum."
  Tarayıcının adres çubuğuna bir adres yazdığında yapılan istek `get` türündedir,
  yani sadece "bana şu sayfayı ver" der. Biz sunucuya bir soru **gönderdiğimiz**
  için `post` kullanıyoruz.
- `adres`: isteğin gideceği yer.
- `headers=basliklar`: kimlik bilgisini isteğe ekle.
- `json=govde`: gövde sözlüğünü sunucunun anlayacağı biçimde (**JSON**, Adım 4'te)
  gönder.
- `cevap` bir sözlük değil, sunucudan gelen her şeyi taşıyan bir nesne: durum kodu,
  içerik vs. `print(cevap)` yazarsan sadece `<Response [200]>` görürsün.
- `status_code`: işin yolunda gidip gitmediğini söyleyen üç haneli sayı. `200`
  "tamam" demek. Diğer kodları Adım 5'te göreceğiz.

Hücre çalışırken solunda `[*]` görürsün: cevap bekleniyor. Normalde birkaç saniye
sürer; model uzun bir cevap yazıyorsa biraz daha.

### Adım 3'te sık yapılan hatalar

**`json=` yerine `data=` yazmak.** `requests.post(adres, headers=basliklar, data=govde)`
de çalışıyormuş gibi görünür, ama gövdeyi JSON olarak değil, bir web formu gibi
gönderir. Sunucu içinde `prompt` bulamaz ve **400** döner. Kural: gövde sözlükse
`json=`.

**İnternet yoksa.** İstek sunucuya hiç ulaşmaz, dolayısıyla durum kodu da gelmez.
Hücre şu satırla durur:

```text
requests.exceptions.ConnectionError: ...
```

Önce bağlantını kontrol et. Okul ağlarında bazı adresler kapalı olabilir; telefonun
internetiyle dene.

**Hücre bitmiyorsa.** `[*]` bir dakikadan uzun sürüyorsa sunucu ya da bağlantı
yavaştır. Hücrenin yanındaki kare düğmeyle (Interrupt) durdur, biraz sonra tekrar
çalıştır.

**Adım 2'yi atladıysan.** `NameError: name 'adres' is not defined`. Adım 2'nin
hücresini çalıştır, sonra bunu.

---

## Adım 4 — Gelen yanıta bak

**(anahtar gerekir)** Sunucu düz metin göndermiyor; Isınmadaki gibi iç içe bir sözlük
gönderiyor. Önce bütününe bakalım:

```python
yanit = cevap.json()
print(yanit)
```

- `cevap.json()` sunucudan gelen içeriği tanıdık bir **sözlüğe** çevirir.
- `print(yanit)` sözlüğü olduğu gibi basar. Uzun bir satır gelir; içinde `'success'`,
  `'errors'` ve `'result'` anahtarlarını ara. Modelin yazdığı metin `'result'`'ın
  içindeki `'response'`'ta durur.

Yanıtın biçimi, kısaltılmış hâliyle şöyle (modelin cevabının yerine `...` koyduk):

```json
{"success": true, "errors": [], "result": {"response": "..."}}
```

`result`'ın içinde `response`'tan başka bilgiler de görebilirsin (örneğin harcanan
**belirteç** sayısını tutan `usage`). Onlar Konu 5'in konusu; şimdilik bize
`response` yeter.

Şimdi Isınmadaki iki satırın aynısıyla metne iniyoruz:

```python
sonuc = yanit["result"]
metin = sonuc["response"]
print(metin)
```

```text
(modelin cevabı: üç kısa slogan)
```

- İki kat içeri giriyoruz: önce `result`, sonra `response`.
- `yanit["response"]` yazarsan **KeyError** alırsın; bu konunun en sık hatası.
- Ekranda gördüğün cevap yanındakinin cevabıyla aynı değil; hücreyi yeniden
  çalıştırırsan (Adım 3 ile birlikte) senin cevabın da değişir. Model her seferinde
  yeni cümle kurar.

> **Kural:** Yanıtın yapısını bilmiyorsan önce bütününü bas (`print(yanit)`), sonra
> kat kat içine gir. Dönemin geri kalanında en çok kullanacağın alışkanlık bu.

Bu kural sadece bugünkü model için değil. Konu 8'de görsel üreten bir modele, Konu
10'da video üreten bir modele istek atacağız; yanıtların yapısı farklı olacak. Her
seferinde aynı yöntemle keşfedeceğiz: önce bütününe bakıp, sonra kat kat inerek.

### JSON — sözlüğün ağdaki hâli

**JSON**, sözlük ve listelerin metin olarak yazılmış hâlidir; bilgisayarlar arasında
veri böyle taşınır. İnternetten bir Python sözlüğü gönderemezsin, sadece metin
gönderebilirsin. JSON o metnin ortak biçimi: Python da, tarayıcı da, sunucu da onu
okuyabilir. `json=govde` sözlüğümüzü JSON'a çevirip yolladı; `cevap.json()` gelen
JSON'u sözlüğe çevirdi.

JSON'u okurken şaşırtan üç küçük fark var. `cevap.json()` bunları senin yerine çevirir:

| JSON'da | Python'da | Anlamı |
|---|---|---|
| `true` / `false` | `True` / `False` | doğru / yanlış |
| `null` | `None` | "hiçbir şey" |
| sadece çift tırnak `"..."` | tek ya da çift tırnak | metin |

Bir dokümanda `"success": true` görüp kodda `yanit["success"] == "true"` yazarsan hep
`False` alırsın; çünkü Python'daki değer metin değil, `True`. (Alıştırma defterindeki
2. bozuk kod tam olarak bu.)

**Gelen içerik JSON değilse.** Nadiren sunucu bir hata sayfası gönderir. O zaman
`cevap.json()` şunu verir:

```text
requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

"Bu JSON değil" demek. Ne geldiğini görmek için `print(cevap.text)` yaz: sunucunun
gönderdiği ham metin.

> **Kendini dene 4.** Sunucudan şu yanıt geldi ve `yanit = cevap.json()` ile sözlüğe
> çevrildi:
>
> ```json
> {"success": false, "result": null, "errors": [{"code": 10000, "message": "Authentication error"}]}
> ```
>
> (a) Python'da `yanit["success"]` neye eşit?
> (b) `yanit["result"]`?
> (c) Buna rağmen Adım 4'teki iki satırı (`sonuc = ...`, `metin = ...`) çalıştırırsan ne olur?
> (d) Hata mesajına (`Authentication error`) kat kat inmek için hangi satırları yazarsın?

---

## Adım 5 — Yanlış anahtarla dene

**(anahtar gerekir)** Durum kodları üç haneli sayılardır ve **ilk hane** sana kimin
tarafına bakacağını söyler:

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
yüzden koda ek olarak **sunucunun kendi açıklamasını** da oku: `cevap.text` içindeki
`message` alanı çoğu zaman sorunu tek cümleyle söyler.

### 401'i canlı görmek

Defterde başlığa kasten **sahte** bir anahtar koyup aynı isteği gönderiyoruz:

```python
sahte_basliklar = {"Authorization": "Bearer yanlis-anahtar"}
cevap = requests.post(adres, headers=sahte_basliklar, json=govde)
print(cevap.status_code)
print(cevap.text)
```

- Adres ve gövde aynı; değişen tek şey başlık. Yani hatanın sebebi kesin olarak anahtar.
- `cevap.text` sunucunun gönderdiği ham metindir; sözlüğe çevrilmemiş hâli. Hata
  açıklaması orada yazar.

Durum kodu `401` gelir; ham metin şuna benzer:

```json
{"success": false, "result": null, "errors": [{"code": 10000, "message": "Authentication error"}]}
```

Dikkat: `result` bu sefer `null`, yani Python'da `None`: sözlük değil, "hiçbir şey".
Adım 4'teki gibi içine girmeye çalışırsan:

```text
TypeError: 'NoneType' object is not subscriptable
```

Bu mesaj "`None`'ın içine köşeli parantezle giremezsin" demek. Yeni başlayanlar bu
hatayı görünce kodlarında bir yazım hatası arar; oysa kodun doğru, **istek başarısız
olmuş**. Asıl sebep bir önceki satırda: durum kodu 200 değildi.

> Bu hücre `cevap` değişkeninin üstüne yazdı: artık `cevap` 401'li yanıtı tutuyor.
> Bundan sonraki adımlar `cevap`'ı değil, kendi isteklerini kullandığı için sorun yok.
> Ama Adım 4'ün hücrelerini şimdi yeniden çalıştırırsan yukarıdaki `TypeError`'ı
> görürsün. Doğru yanıtı geri almak için Adım 3'ü yeniden çalıştır.

### Yanıtı okuma sırası

Yanıta güvenmeden önce durum koduna bakarız:

```python
if cevap.status_code == 200:
    print("Tamam")
else:
    print("Bir sorun var:", cevap.status_code)
```

Sahte anahtardan sonra çalıştırınca çıktı:

```text
Bir sorun var: 401
```

Bu `if` bir yanıtı okuma sırasının ta kendisi:

1. **Durum koduna bak.** 200 değilse içine girme; kodu ve sunucunun mesajını oku.
2. **200 ise** `result` katına, oradan `response`'a in.

> **Kendini dene 5.** Her durumda ne görürsün, ne yaparsın?
> (a) Akşam 50 soruluk bir döngü çalıştırdın; 38. sorudan sonra her isteğin durum
>     kodu `429`.
> (b) Panelden yeni token ürettin, eskisini sildin ama `anahtar.txt` dosyasını
>     güncellemeyi unuttun.
> (c) Wi-Fi kapalıyken Adım 3'ü çalıştırdın.
> (d) Dün çalışan defter bugün `500` veriyor; hiçbir şeyi değiştirmedin.

---

## Adım 6 — Fonksiyona koy

**(anahtar gerekir)** Şu ana kadar bir soru sormak için dört iş yaptık: gövdeyi
hazırla, gönder, sözlüğe çevir, iki kat in. Her soru için bu satırları yeniden yazmamak
için onları tek bir isim altında topluyoruz:

```python
def modele_sor(soru):
    govde = {"prompt": soru}
    cevap = requests.post(adres, headers=basliklar, json=govde)
    yanit = cevap.json()
    sonuc = yanit["result"]
    return sonuc["response"]
```

Bu hücre hiçbir şey basmaz; yalnızca fonksiyonu **tanımlar**. Satırlar, Adım 2–4'te
tek tek yazdıklarımızın aynısı:

| Satır | Ne yapıyor | Hangi adımdan |
|---|---|---|
| `govde = {"prompt": soru}` | Gelen soruyu gövdeye koy | Adım 2 |
| `cevap = requests.post(...)` | Gönder | Adım 3 |
| `yanit = cevap.json()` | Sözlüğe çevir | Adım 4 |
| `sonuc = yanit["result"]` | Bir kat in | Adım 4 |
| `return sonuc["response"]` | Metni fonksiyonun sonucu olarak geri ver | Adım 4 |

Şimdi tek satırla soru sorabiliriz:

```python
print(modele_sor("Sessiz bir çalışma kafesinin logosu için üç renk öner."))
```

```text
(modelin cevabı: üç renk önerisi)
```

**Neden fonksiyon?** Az sonra aynı işi üç kez, ileride elli kez yapacağız. Beş
satırı her soru için kopyalamak hem uzun hem tehlikeli: birinde bir harfi unutursun,
sorulardan biri bozulur. Fonksiyonda bir kez doğru yazarsın, hep doğru çalışır.

**`adres` ve `basliklar` nereden geliyor?** Fonksiyonun dışında, Adım 2'de bir kez
hazırlandılar; fonksiyon onları oradan kullanıyor. Fonksiyona yalnızca her seferinde
değişen şeyi, yani soruyu veriyoruz. Anahtar yine koda yazılmıyor: Adım 1'de dosyadan
okundu.

**İstek başarısız olursa?** Fonksiyon durum koduna bakmıyor. Kota bitmişse ya da
anahtar yanlışsa `result` boş gelir ve hücre
`TypeError: 'NoneType' object is not subscriptable` ile durur. Böyle bir hata görürsen
Adım 5'e dön: durum koduna bak.

**Fonksiyonu değiştirdiysen** tanım hücresini yeniden çalıştır. Defter, hücreyi son
çalıştırdığın andaki hâlini hatırlar; hücrede yazıyı değiştirmek yetmez.

---

## Adım 7 — Birden çok soru, cevaplar dosyaya

**(anahtar gerekir)** Kodun asıl gücü burada: aynı işi tekrar tekrar yapmak.

```python
sorular = [
    "Sessiz bir çalışma kafesinin logosu için hangi üç rengi önerirsin?",
    "Bu kafenin afişinde serif mi sans-serif mi yazı tipi uygun olur?",
    "Bu kafenin Instagram hesabı için üç gönderi fikri ver.",
]

with open("cevaplar.txt", "w", encoding="utf-8") as dosya:
    for soru in sorular:
        metin = modele_sor(soru)
        print(soru)
        print(metin)
        dosya.write(soru + "\n" + metin + "\n\n")
```

Satır satır:

- `sorular` sıradan bir **liste**; her elemanı bir soru metni.
- `open("cevaplar.txt", "w", ...)` dosyayı **yazmak** için açar (`"w"` = write). Konu 1'de
  dosya yazmayı görmüştük.
- `for soru in sorular` her turda listeden bir soru alır.
- `metin = modele_sor(soru)` soruyu modele sorar; her turda bir istek gider.
- İki `print` hem soruyu hem cevabı ekrana basar; hücre çalışırken ilerlemeyi görürsün.
- `dosya.write(...)` soruyu, cevabı ve araya satır sonlarını dosyaya yazar. `"\n"` satır
  sonu demek; `"\n\n"` araya bir boş satır koyar.

Hücre bitince konunun klasöründe (`02-api-ile-konusmak`) `cevaplar.txt` oluşur. VS
Code'da açıp okuyabilirsin. Biçimi şöyle:

```text
Sessiz bir çalışma kafesinin logosu için hangi üç rengi önerirsin?
(modelin cevabı)

Bu kafenin afişinde serif mi sans-serif mi yazı tipi uygun olur?
(modelin cevabı)

Bu kafenin Instagram hesabı için üç gönderi fikri ver.
(modelin cevabı)
```

Dikkat edilecekler:

- `"w"` kipi dosyayı **her seferinde sıfırdan** yazar. Hücreyi ikinci kez çalıştırırsan
  ilk cevaplar silinir, yerine yenileri gelir.
- Üç soru, üç istek demek: hücre birkaç saniye `[*]` gösterir. Elli soru yazarsan elli
  istek gider; kotanı düşün.
- Listedeki her soru tırnak içinde ve sonunda virgül var. Virgülü unutursan Python iki
  soruyu **birleştirip** tek soru yapar ve hata da vermez; cevap tuhaf gelir.
- Sohbet penceresine elli soruyu tek tek yapıştırıp cevapları tek tek kopyalamayı düşün.
  Arayüzde yapamayacağın şey bu.

**Kendi sorularını sormak için** defteri yeni bir adla kopyala (ödevde de böyle
yapacaksın), kopyada `sorular` listesini değiştir. Kopya aynı klasörde dursun ki
`../anahtar.txt` yolu doğru kalsın.

> **Kendini dene 6.** Hücreyi çalıştırdın; üçüncü soruda hücre
> `TypeError: 'NoneType' object is not subscriptable` ile durdu.
> (a) `cevaplar.txt` dosyasında ne var?
> (b) Sorunun ne olduğunu nasıl öğrenirsin?

---

## Adım 8 — Soruya bağlam koymak cevabı değiştirir mi?

**(anahtar gerekir)** Adım 7'deki soruların hepsinde "sessiz bir çalışma kafesi" ya
da "bu kafe" diyorduk. Peki bunu söylemeseydik? Aynı isteği iki biçimde soruyoruz:

| Tür | Soru |
|---|---|
| **bağlamsız** | Bir kafe için üç kısa slogan yaz. |
| **bağlamlı** | Müşterilerinin sessiz bir çalışma yeri olarak anlattığı bir kafe için üç kısa slogan yaz. |

```python
baglamsiz = modele_sor("Bir kafe için üç kısa slogan yaz.")
baglamli = modele_sor("Müşterilerinin sessiz bir çalışma yeri olarak anlattığı bir kafe için üç kısa slogan yaz.")

print(baglamsiz)
print()
print(baglamli)
```

- İki ayrı istek gidiyor; cevaplar iki değişkende duruyor.
- Ortadaki `print()` boş bir satır basar: iki cevap birbirine karışmasın diye.

```text
(bağlamsız sorunun cevabı)

(bağlamlı sorunun cevabı)
```

**İki cevabı yan yana oku.** Hangisinde `kahve`, `fincan`, `aroma` gibi kelimeler var?
Hangisinde `sessiz`, `odak`, `çalışmak`? Beklenen örüntü şu: bulguyu söylemezsen model
**ortalama bir kafeyi** anlatır. Konu 1'de 30 yorumu sayarak bulduğumuz şey (müşteri
buraya çalışmaya geliyor) ancak soruya yazınca cevaba girer. Model senin kafeni
tanımıyor; ona ne söylersen onu biliyor. Soruyu yazmak, bir brief yazmak gibi bir
tasarım işi.

**Tek denemeye güvenme.** Model aynı soruya her seferinde başka cümleler kurar. Hücreyi
iki üç kez çalıştır, her seferinde iki cevabı yeniden oku. Örüntü her denemede aynı
yönde mi? Bir denemede bağlamsız cevap da "odak" diyorsa bu, bulgunun çöktüğü anlamına
gelmez; tek bir örnek, bir eğilimi ne kanıtlar ne çürütür.

**Okurken dikkat:** "Kahven, prizin, zamanın." gibi bir slogan `kahve` kelimesini
içerir ama kahveyi övmez; çalışma düzeninin bir parçası olarak anar. Kelimeye değil,
cümlenin ne anlattığına bak.

Ödevdeki soru ("beş cevaptan hangisi işe yaramazdı, neden?") buraya bağlanıyor:
işe yaramayan bir cevabın sebebi çoğu zaman modelde değil, **soruda** eksik kalan
bağlamdadır.

> **Kendini dene 7.** (a) Bağlamsız cevaplardan biri "Her yudumda mutluluk" diyor.
> İçinde `kahve` kelimesi yok. Bu cevap kahve klişesi mi? (b) "Bu kafenin Instagram
> hesabı için üç gönderi fikri ver" sorusuna bir bağlam daha ekleyecek olsan Konu 1'in
> bulgularından hangisini eklerdin?

---

## Adımlar ve defter

| Adım | Ne yaptık | Elimizde ne oluştu |
|---|---|---|
| Isınma | İç içe sözlüğe kat kat indik | `sonuc`, `metin` |
| 1 | Anahtarı dosyadan okuduk | `hesap`, `anahtar` |
| 2 | İsteğin üç parçasını hazırladık | `adres`, `basliklar`, `govde` |
| 3 | Gönderdik | `cevap`, durum kodu `200` |
| 4 | Yanıta baktık, metni çektik | `yanit` → `sonuc` → `metin` |
| 5 | Yanlış anahtarla hata kodunu gördük | `if cevap.status_code == 200` |
| 6 | Fonksiyona koyduk | `modele_sor()` |
| 7 | Döngüyle birden çok soru sorduk | `cevaplar.txt` |
| 8 | Bağlamın etkisine baktık | iki cevap yan yana |

Hepsi tek defterde: `ders.ipynb`. Hücreleri her zaman yukarıdan aşağı çalıştır; defteri
yeni açtıysan (ya da çekirdeği yeniden başlattıysan) Adım 1'den başla.

Derste kendi başına çalışacağın defter: `alistirma.ipynb`. Önce yeni bir adla kopyala,
kopyada çalış. İki bölümü var:

- **Bozuk kodlar:** beş kısa hücre. Bazıları hata verir, bazıları hata vermeden yanlış
  sonuç basar; üstlerinde ne yazmaları gerektiği yazıyor. Vizedeki soru tipine benzer.
- **Kendi başına:** `BOSLUK` yazan yerleri doldurduğun sorular. Doldurmadan çalıştırırsan `NameError: name 'BOSLUK' is not defined` alırsın.

Alıştırma defteri internete çıkmaz, anahtar istemez.

---

## Sık karşılaşılan sorunlar

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `NameError: name '...' is not defined` | Bir hücreyi atladın ya da defteri yeni açtın | Hücreleri baştan, sırayla çalıştır |
| `FileNotFoundError: ... '../anahtar.txt'` | Hesap açılmamış, dosya yanlış klasörde ya da adı `anahtar.txt.txt` | Dosyayı `gita3111` klasörüne (konu klasörlerinin bir üstüne) koy, uzantıyı kontrol et; defterin kopyası konu klasöründe dursun. Anahtarın yoksa derste yanındakiyle çalış |
| `IndexError: list index out of range` (Adım 1) | `anahtar.txt`'de boş ya da `=` içermeyen bir satır var | O satırı sil |
| `KeyError: 'ACCOUNT_ID'` ya da `KeyError: 'API_TOKEN'` | Dosyada o satır yok ya da adı farklı yazılmış (küçük harf, boşluk) | Dosyayı Adım 1'deki biçime göre düzelt |
| `ModuleNotFoundError: No module named 'requests'` | Defter `.venv` dışındaki bir çekirdekle çalışıyor | Sağ üstten çekirdek olarak konu klasörünün `.venv`'ini seç; yoksa konu klasöründe `uv sync` |
| `KeyError: 'response'` | Bir kat atlandı | Önce `sonuc = yanit["result"]`, sonra `sonuc["response"]`; emin değilsen `print(yanit)` |
| `TypeError: 'NoneType' object is not subscriptable` | İstek başarısız, `result` boş | Önce durum koduna bak (Adım 5) |
| `requests.exceptions.ConnectionError` | İstek sunucuya ulaşmadı | İnternet bağlantını kontrol et |
| `requests.exceptions.JSONDecodeError` | Gelen içerik JSON değil | `print(cevap.text)` ile ne geldiğine bak |
| Hücre çok uzun süre `[*]` | Sunucu ya da bağlantı yavaş | Kare düğmeyle durdur, biraz sonra tekrar çalıştır |
| 401 / 403 / 429 | Anahtar, izin ya da kota | Adım 5'teki hata kodları tablosu |

---

## Bu konuda öğrendiklerin

- **API**, programların birbirine soru sorduğu kapıdır. Model senin bilgisayarında
  değil, uzakta çalışır; bu yüzden internet, kota ve kimlik gerekir.
- **Anahtar senin kimliğindir:** koda yazılmaz, ayrı dosyada durur, teslime konmaz,
  ekranda gösterilmez. Sızarsa silip yenisini üretirsin.
- **Dosyayı satır satır okumak:** `for satir in dosya`, `split("=")`, `strip()`.
  `..` bir üst klasör demek.
- **Bir istek üç parçadır:** adres (nereye), başlık (kim), gövde (ne). `requests.post`
  üçünü birlikte gönderir.
- **JSON** sözlük ve listelerin metin hâlidir. `true`/`null` Python'da `True`/`None`
  olur.
- **İç içe sözlüğe kat kat inilir:** her satırda bir kat, her katın kendi değişkeni.
  Yapıyı bilmiyorsan önce bütününü bas.
- **Yanıtı okuma sırası:** önce durum kodu, sonra içerik. Durum kodunun ilk hanesi
  kimin tarafına bakacağını söyler: 4xx senin, 5xx sunucunun.
- **Fonksiyon ve döngü** aynı isteği üç, elli kez tekrarlamanı sağlar; cevaplar bir
  dosyada toplanır.
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
| **İstemci** | İsteği gönderen taraf; burada senin defterin |
| **Sunucu** | İsteği karşılayıp cevap veren uzaktaki bilgisayar |
| **Uç nokta (endpoint)** | İsteğin gönderildiği tam adres |
| **Başlık (header)** | İstekle giden kimlik ve ek bilgiler; burada `Authorization` |
| **Gövde (body)** | İsteğin asıl içeriği; burada `{"prompt": soru}` |
| **Anahtar / API token** | Sunucuya kim olduğunu kanıtlayan gizli metin |
| **Hesap kimliği (Account ID)** | Hangi hesabın modelinin çalışacağını söyleyen kimlik |
| **Durum kodu** | Sunucunun işin nasıl gittiğini söyleyen üç haneli sayısı (200, 401, 429...) |
| **JSON** | Sözlük ve listelerin metin olarak yazılmış, bilgisayarlar arasında taşınan hâli |
| **Neuron** | Cloudflare'in ücretsiz kotayı ölçtüğü birim; günde 10.000 |
| **Kota** | Bir günde kullanabileceğin ücretsiz harcama sınırı |
| **Bağlam** | Soruya eklediğin ve modelin bilmediği bilgi; burada Konu 1'in bulgusu |
| **Defter (notebook)** | Kodun hücre hücre yazılıp çalıştırıldığı `.ipynb` dosyası |
| **Hücre** | Defterdeki tek bir kutu; yazı ya da kod |
| **Çekirdek (kernel)** | Defterdeki kodu çalıştıran Python; bu konuda klasörün `.venv`'i |

---

## Kendini dene — cevaplar

**1.** (a) `True`. (b) `KeyError: 'result'`. `sonuc` zaten `result`'ın içindeki sözlük;
onun içinde bir `result` daha yok, bir kat fazla inmeye çalıştın. (c) `KeyError: 'Result'`.
Sözlük anahtarları harfi harfine aranır; büyük `R` ile yazılmış bir anahtar yok.

**2.** (a) Üçüncü satırda (`not: ...`), `deger = parcalar[1].strip()` satırında
`IndexError: list index out of range` ile durur. O satırda `=` yok; `split("=")` tek
parçalı bir liste verir, `parcalar[1]` yoktur. (b) `KeyError: 'ACCOUNT_ID'`: satır adı
küçük harfle yazıldığı için sözlükte `ACCOUNT_ID` diye bir anahtar yok, `account_id`
var. (c) Token'ın değeri tırnaklarla birlikte okunur: `"xyz789"`. Sunucu tırnaklı
token'ı tanımaz ve **401** döner. Çare: not satırını sil, adı büyük harfle yaz,
tırnakları sil.

**3.** (a) Başlık: `Bearer`'dan sonra boşluk yok, sunucuya `Bearerxyz...` gider →
**401**. (b) Adres: baştaki `f` yok; adrese hesap kimliği yerine `{hesap}` yazısı
gider → sunucu böyle bir hesap bulamaz, 4xx türünde bir hata döner. (c) Gövde:
sunucu soruyu `prompt` alanında bekliyor, `soru` alanını tanımıyor → **400**.

**4.** (a) `False`. (b) `None`. (c) `sonuc = yanit["result"]` çalışır ama `sonuc`
`None` olur; `metin = sonuc["response"]` satırı
`TypeError: 'NoneType' object is not subscriptable` verir. Önce durum koduna ya da
`success` alanına bakmak gerekirdi. (d) Her satırda bir kat:
`hatalar = yanit["errors"]` (bir liste), `ilk_hata = hatalar[0]` (listenin ilk elemanı,
bir sözlük), `print(ilk_hata["message"])`. Listede sıra numarasıyla, sözlükte adla
inilir.

**5.** (a) **429**: günlük kota bitti. Türkiye saatiyle 03:00'te sıfırlanır.
Döngüyü küçült, soruları kısalt; kota dolunca beklemekten başka çare yok.
(b) **401**: eski token silindiği için artık geçersiz. `anahtar.txt`'yi güncelle,
Adım 1'den itibaren hücreleri yeniden çalıştır. (c) Durum kodu gelmez, hücre
`ConnectionError` ile durur; istek sunucuya hiç ulaşmadı. (d) **500** sunucu tarafı
demek; kodunu değiştirme, biraz sonra tekrar dene.

**6.** (a) İlk iki soru ve cevapları. `dosya.write` döngünün **içinde**, her sorudan
hemen sonra çalışıyor; ilk iki tur bitmişti. `with` bloğu hata çıkınca da dosyayı
düzgün kapatır. Üçüncü soru dosyada yok: hata `modele_sor` içinde, `write`'a gelmeden
çıktı. (b) Hata `result`'ın boş geldiğini söylüyor, yani istek başarısız oldu. Sebebi
durum kodunda: Adım 5'teki gibi bir istek atıp `cevap.status_code`'u bas. 429 ise kota
bitmiştir, 401 ise anahtar yanlıştır.

**7.** (a) Evet. "Yudum" kahveyi adını söylemeden anıyor. Bu yüzden kelimeye değil,
cümlenin ne anlattığına bakarak okuyoruz; sadece `kahve` kelimesini arayan biri bu
cevabı kaçırırdı. (b) Örneğin "müşteriler en çok priz ve internetten bahsediyor" ya da
"müşterilerin çoğu öğrenci". Doğru cevap yok; önemli olan, modelin bilemeyeceği ve
senin veriden bulduğun bir bilgiyi eklemek.

---

## Ödev — iki parça

`odevler/odev2.md` (puansız; sırası gelen sınıfta gösterir):

1. **Kendi beş sorun:** `ders.ipynb`'yi yeni bir adla kopyala, Adım 7'deki `sorular`
   listesine aynı konuda kendi beş sorunu yaz, hücreleri sırayla çalıştır ve
   `cevaplar.txt` dosyanı getir. Bir de tek cümle: beş cevaptan hangisi işe yaramazdı,
   sence neden? (Adım 8'i hatırla: sebep soruda olabilir.)
2. **Renk etiketleme:** `veri/renkler.csv` içindeki 20 renge sakin / enerjik / ciddi
   etiketi ver.

İkinci parça **Konu 3'ün verisi**. Yapılmazsa eğitecek veri olmaz. Doğru cevap
yok; herkesin etiketi farklı olacak, mesele de bu.

Birinci parça gerçek anahtar ister.

## Sonraki konu

**Konu 3 — Makine öğrenmesi** (`03-makine-ogrenmesi`). Bu konuda hazır bir modele
soru sorduk. Konu 3'te kendi modelimizi eğiteceğiz, hem de sınıfın ödevde verdiği
renk etiketleriyle.
