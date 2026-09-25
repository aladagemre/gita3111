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

**Kurulum (dersten önce):** `uv add -r 02-api-ile-konusmak/requirements.txt` — internete istek atan
`requests` kütüphanesini kurar.

> Bu dönemin **kritik konusu**: Konu 4, 5, 8, 9, 10 ve 11 bunun üstüne kuruluyor.
> Buradaki her adım ileride her derste tekrar edecek. Anlamadığın bir yer kalırsa
> şimdi sor; sonra sormak çok daha pahalı.

### Bu not nasıl okunur

- Her adımda üç şey var: **ne yapıyoruz**, **neden gerekiyor**, **atlarsan ne olur**.
- `Kendini dene` kutuları küçük kontrol sorularıdır. Cevapları notun sonunda.
- Kod parçalarının çoğu anahtarsız da çalışır. Gerçek anahtar isteyenlerin başında
  **(anahtar gerekir)** yazıyor.
- Kodları `gita3111` klasörünün içinden çalıştır. Nedenini Adım 1'de göreceksin.

---

## Isınma: iç içe sözlük

`00_isinma.py` iki küçük tamir içeriyor. Birazdan sunucudan gelecek cevap tam olarak
bu yapıda olacak; ısınma onun provası.

```python
YANIT = {
    "success": True,
    "result": {
        "response": "Merhaba!",
        "usage": {"prompt_tokens": 4, "completion_tokens": 2},
    },
    "errors": [],
}

print(YANIT["result"]["response"])
```

1. **Sözlüğün içindeki sözlük.** Metin dıştaki sözlükte değil, `result` içinde:
   `YANIT["response"]` değil, `YANIT["result"]["response"]`.
2. **Sözlüğün içindeki liste.** Hatalı bir yanıtta `errors` bir liste olur; önce
   sırayla elemana, sonra anahtara gidilir: `yanit["errors"][0]["message"]`.

Kural aynı: her köşeli parantez **bir kat** içeri girer. Liste katında sıra numarası,
sözlük katında anahtar adı yazılır.

İfadeyi soldan sağa, kat kat okursan hata yapmazsın:

| İfade | Elde ettiğin şey | Türü |
|---|---|---|
| `YANIT` | Bütün yanıt | sözlük |
| `YANIT["result"]` | İçteki sözlük | sözlük |
| `YANIT["result"]["usage"]` | Kullanım bilgisi | sözlük |
| `YANIT["result"]["usage"]["prompt_tokens"]` | `4` | sayı |
| `YANIT["errors"]` | Hata listesi (burada boş) | liste |

### Hata mesajını sondan oku

Bu konuda iki hata çok sık çıkacak. Python bir hata verdiğinde en önemli satır
**en alttaki** satırdır: önce hatanın türü, sonra açıklaması. Onun hemen üstünde de
hatanın çıktığı satır numarası yazar.

```text
KeyError: 'response'
```

"Bu sözlükte `response` diye bir anahtar yok." Bir kat atladın demektir: `result`
katına girmeden `response`'u aradın.

```text
TypeError: list indices must be integers or slices, not str
```

"Listeyi bir adla açmaya çalıştın; liste sadece sıra numarasıyla açılır." `errors`
bir liste; `yanit["errors"]["message"]` yazınca bu hatayı alırsın. Doğrusu
`yanit["errors"][0]["message"]`.

> **Kendini dene 1.** Yukarıdaki `YANIT` için:
> (a) `completion_tokens` değerine hangi ifadeyle ulaşırsın?
> (b) `YANIT["errors"][0]` yazarsan hangi hatayı alırsın, neden?
> (c) `YANIT["usage"]["prompt_tokens"]` yazarsan?

---

## Anahtarın yoksa? Demo modu

Örneklerin çoğu **DEMO modunda** çalışır: `anahtar.txt` yoksa kayıtlı bir cevap
kullanılır. Kod aynı kod, sadece cevap kutudan gelir. Yani dersi takip edebilirsin.

Ama bu bir köprü, çözüm değil. Ödev için kendi anahtarın gerekiyor ve Konu 4'ten
itibaren demo modu yetmiyor. Hesabı ders öncesi kurulum yönergesinin 5. adımıyla
aç (`00-hazirlik/kurulum-yonergesi.md`).

Örnek dosyalar anahtar dosyasını üç durumdan birinde bulur:

| Durum | Ekranda ne görürsün | Ne oluyor |
|---|---|---|
| **tamam** | Hiçbir uyarı yok, "İstek gönderiliyor..." | Gerçek modelle konuşuyorsun |
| **yok** | `[DEMO MODU] anahtar.txt yok; ...` | Kayıtlı cevap kullanılıyor |
| **bozuk** | `[UYARI] anahtar.txt var ama ... okunamadı` | Dosya var ama içinde `ACCOUNT_ID` ya da `API_TOKEN` satırı yok; yine kayıtlı cevap kullanılıyor |

"Yok" ile "bozuk" neden ayrı? Dosyası olmayan kişi bunu zaten bilir. Ama dosyası
bozuk olan kişi "dosyam var, demek ki çalışıyor" sanar ve günlerce kayıtlı cevaba
bakar. `[UYARI]` satırını görürsen dosyanı düzelt.

**Demo modunda olduğunu nasıl anlarsın?** Her soruya **aynı** cevap gelir: "1)
Sessizliğin adresi. 2) Kahven, prizin, zamanın. 3) Burada odaklanırsın." Farklı
sorular sorduğun hâlde bu cümleyi görüyorsan gerçek modelle konuşmuyorsun.

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

`anahtarlari_oku()` fonksiyonu bu dosyayı satır satır okuyup bir **sözlük** döndürür:

```python
def anahtarlari_oku(yol="anahtar.txt"):
    degerler = {}
    with open(yol, encoding="utf-8") as dosya:
        for satir in dosya:                         # dosyayı satır satır gez
            if "=" in satir:
                ad, _, deger = satir.partition("=")  # "=" işaretinden ikiye böl
                degerler[ad.strip().upper()] = deger.strip()
    return degerler
```

Konu 1'de dosyayı `dosya.read()` ile tek parça okumuştuk. Burada üç yeni şey var:

- `for satir in dosya` dosyayı **satır satır** gezer.
- `satir.partition("=")` satırı üç parçaya böler: eşittirin solu, eşittirin kendisi,
  sağı. Soldaki üç değişken bu üç parçayı sırayla alır; ortadakini kullanmayacağımız
  için adı `_`.
- `.strip()` baştaki ve sondaki boşlukları (satır sonundaki görünmez `\n` dahil)
  siler; `.upper()` büyük harfe çevirir. Böylece `account_id = ...` diye yazsan da
  `ACCOUNT_ID` olarak okunur.

Tek bir satırın yolculuğunu adım adım izleyelim:

| Aşama | Değer |
|---|---|
| Dosyadaki satır | `'API_TOKEN = xyz789\n'` |
| `partition("=")` sonrası | `('API_TOKEN ', '=', ' xyz789\n')` |
| `ad.strip().upper()` | `'API_TOKEN'` |
| `deger.strip()` | `'xyz789'` |
| Sözlüğe yazılan | `degerler["API_TOKEN"] = "xyz789"` |

**Neden `split` değil de `partition`?** Token'ların içinde bazen `=` işareti olur.
`partition` sadece **ilk** eşittirden böler, gerisini değere bırakır:
`"API_TOKEN = ab=cd"` satırından değer olarak `ab=cd` çıkar. Kırpılmış bir token
401 hatası verirdi.

**Neden `if "=" in satir`?** Dosyada boş satır ya da kendine yazdığın bir not
olabilir. Eşittir içermeyen satırlar atlanır, program bozulmaz.

Kullanımı:

```python
anahtarlar = anahtarlari_oku()
hesap = anahtarlar["ACCOUNT_ID"]
anahtar = anahtarlar["API_TOKEN"]

print("Account ID okundu mu:", "evet" if hesap else "hayır")
print("Token'ın ilk 6 karakteri:", anahtar[:6] + "...")
```

Anahtarı **asla tam olarak** ekrana basma; sadece okunduğunu doğrula. İlk 6 karakter
"doğru dosyayı mı okudum?" sorusuna cevap vermeye yeter, anahtarı kullanmaya yetmez.

### Dosya nerede olmalı? Çalışma klasörü

`open("anahtar.txt")` dosyayı **programı çalıştırdığın klasörde** arar, `.py`
dosyasının durduğu klasörde değil. Bütün komutları `gita3111` klasöründen
çalıştırdığımız için `anahtar.txt` de oraya konur:

```
gita3111/
├── anahtar.txt                  ← burada
└── 02-api-ile-konusmak/
    ├── ornekler/02_ilk_istek.py
    └── veri/ornek_yanit.json
```

Terminalde `ornekler` klasörüne girip `uv run 02_ilk_istek.py` dersen program
`anahtar.txt` dosyasını da, `02-api-ile-konusmak/veri/...` dosyalarını da bulamaz:

```text
FileNotFoundError: [Errno 2] No such file or directory: '02-api-ile-konusmak/veri/ornek_sorular.txt'
```

Çözüm: `cd` ile `gita3111` klasörüne dön, komutu oradan ver.

### Adım 1'de sık yapılan hatalar

| Ne oldu | Ne görürsün | Çare |
|---|---|---|
| Windows dosyayı `anahtar.txt.txt` diye kaydetti (uzantılar gizli) | `anahtar.txt bulunamadı` ya da demo modu | Dosya gezgininde "Dosya adı uzantılarını göster"i aç, fazla `.txt`'yi sil |
| Değeri tırnak içine yazdın: `API_TOKEN = "xyz789"` | Okuma çalışır ama istek **401** döner | Tırnaklar da token'ın parçası sanılıyor; tırnakları sil |
| Satır adında boşluk: `API TOKEN = ...` | `KeyError: 'API_TOKEN'` ya da `[UYARI]` | Alt çizgiyle yaz: `API_TOKEN` |
| Token'ı kopyalarken son karakteri kaçırdın | **401** | Token'ı panelden yeniden üretmek en hızlısı |

> **Kendini dene 2.** `anahtar.txt` dosyasının içi şu olsun:
>
> ```
> account_id = a1b2
> API_TOKEN = "xyz789"
> not: bu satırda eşittir yok
> ```
>
> `anahtarlari_oku()` ne döndürür? Bu dosyayla istek atarsan ne olur?

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

**(anahtar gerekir)** Bu kod gerçekten internete çıkar. Anahtarın yoksa
`02_ilk_istek.py` aynı adımları demo modunda gösterir.

```python
import requests

cevap = requests.post(adres, headers=basliklar, json=govde, timeout=60)
print("Durum kodu:", cevap.status_code)
yanit = cevap.json()
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
- `cevap.json()` gelen içeriği tanıdık bir **sözlüğe** çevirir.

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

Anahtarın yoksa sunucudan gelecek yanıtın kayıtlı bir kopyasını dosyadan
yükleyebilirsin. Aşağıdaki iki satır demo modunun yaptığı işin aynısı:

```python
import json

with open("02-api-ile-konusmak/veri/ornek_yanit.json", encoding="utf-8") as dosya:
    yanit = json.load(dosya)
```

Sunucu düz metin göndermiyor, iç içe bir sözlük gönderiyor. Görmek için ham hâlini
okunaklı basıyoruz:

```python
print(json.dumps(yanit, ensure_ascii=False, indent=2))
```

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

(Bu, demo modunun kullandığı `02-api-ile-konusmak/veri/ornek_yanit.json` dosyası.)

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
| `json.load(dosya)` | metin → sözlük | dosyadan | demo yanıtını okumak |
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

```python
metin = yanit["result"]["response"]
print(metin)
```

- İki kat içeri giriyoruz: önce `result`, sonra `response`.
- `yanit["response"]` yazarsan **KeyError** alırsın; bu konunun en sık hatası.
- `errors` bir **liste**; ilk hatanın mesajı: `yanit["errors"][0]["message"]`.

> **Kural:** Yanıtın yapısını bilmiyorsan önce ham hâlini bas, sonra içine gir.
> Dönemin geri kalanında en çok kullanacağın alışkanlık bu.

Bu kural sadece bugünkü model için değil. Konu 8'de görsel üreten bir modele, Konu 10'da
video üreten bir modele istek atacağız; yanıtların yapısı farklı olacak. Her
seferinde aynı yöntemle keşfedeceğiz: `03_yaniti_coz.py` dosyasının yaptığı gibi
katları tek tek sorarak.

```python
print("En dıştaki anahtarlar:", list(yanit.keys()))
print("result'ın türü       :", type(yanit["result"]).__name__)
print("result'ın anahtarları:", list(yanit["result"].keys()))
```

```text
En dıştaki anahtarlar: ['result', 'success', 'errors', 'messages']
result'ın türü       : dict
result'ın anahtarları: ['response', 'usage']
```

`dict` Python'da sözlüğün adı. Her satır bir sonraki adımın yolunu gösteriyor:
`result` bir sözlük, içinde `response` var, demek ki `yanit["result"]["response"]`.

### Kaç belirteç harcadık?

Aynı yöntemle üç kat içeri:

```python
kullanim = yanit["result"]["usage"]
print("Soru     :", kullanim["prompt_tokens"], "belirteç")
print("Cevap    :", kullanim["completion_tokens"], "belirteç")
print("Toplam   :", kullanim["total_tokens"], "belirteç")
```

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

Demo yanıtında `split()` 10 kelime sayıyor (numaralar dahil), model ise 22 belirteç.
Yani bir kelime ortalama iki parçadan fazla. Türkçede kelimeler eklerle uzadığı için (`odaklanırsın`,
`sessizliğin`) bir kelime çoğu zaman birkaç parçaya bölünür. Kendi anahtarınla
kendi sorunun sayılarına bak; Konu 5'te bunun neden önemli olduğunu göreceğiz.

---

## Hata kodları

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

Derste kasten yanlış anahtarla 401 hatası ürettik (`04_hata_kodlari.py`). Sunucunun
gönderdiği yanıt şuna benzer:

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

Bu yüzden bir yanıtı her zaman aynı sırayla okuruz:

1. **Durum koduna bak.** 200 değilse içine girme; kodu ve `errors` mesajını bas.
2. **200 ise** `result` katına, oradan `response`'a in.

```python
if cevap.status_code == 200:
    metin = cevap.json()["result"]["response"]
    print(metin)
else:
    print("İstek başarısız:", cevap.status_code)
    print(cevap.text[:300])
```

### Hatayı kodla karşılamak

Her koda bir açıklama yazan bir sözlük ve Konu 1'deki `.get` kalıbı yeterli
(dosyadaki sözlük tablodaki bütün kodları içerir; burada kısaltıldı):

```python
HATA_SOZLUGU = {
    200: "Her şey yolunda.",
    401: "Yetki yok. Anahtarı kontrol et.",
    429: "Kota doldu. 00:00 UTC'de sıfırlanır.",
}

def acikla(kod):
    return HATA_SOZLUGU.get(kod, "Tanımadığım bir kod.")   # varsa açıklama, yoksa yedek cümle

print(acikla(401))
print(acikla(418))
```

```text
Yetki yok. Anahtarı kontrol et.
Tanımadığım bir kod.
```

`HATA_SOZLUGU[418]` yazsaydık `KeyError` alırdık; `.get` tanımadığı kodda bile
program durmasın diye yedek cümleyi döndürür.

> **Kendini dene 5.** Her durumda ne görürsün, ne yaparsın?
> (a) Akşam 50 soruluk bir döngü çalıştırdın; 38. sorudan sonra bütün cevaplar
>     `[HATA 429]`.
> (b) Panelden yeni token ürettin, eskisini sildin ama `anahtar.txt` dosyasını
>     güncellemeyi unuttun.
> (c) Wi-Fi kapalıyken programı çalıştırdın.
> (d) Dün çalışan program bugün `500` veriyor; kodunda hiçbir şeyi değiştirmedin.

---

## Adım 4 — Soruyu fonksiyona koy

Şimdiye kadar yazdığımız dağınık adımları (adres, başlık, gövde, gönder, kontrol
et, metni çek) tek isim altında topluyoruz:

```python
def modele_sor(soru, hesap, anahtar):
    """Soruyu modele gönderir, cevabın METNİNİ döndürür."""
    adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
    basliklar = {"Authorization": f"Bearer {anahtar}"}
    cevap = requests.post(adres, headers=basliklar, json={"prompt": soru}, timeout=60)
    if cevap.status_code != 200:
        return f"[HATA {cevap.status_code}]"
    return cevap.json()["result"]["response"]
```

Tam hâli `05_soru_sor.py` içinde.

**Neden fonksiyon?** Az sonra aynı işi beş kez, ileride elli kez yapacağız. Beş
satırı her soru için kopyalamak hem uzun hem tehlikeli: birinde `Bearer`'ın
boşluğunu unutursun, beşten biri bozulur. Fonksiyonda bir kez doğru yazarsın, hep
doğru çalışır.

**Neden `hesap` ve `anahtar` parametre?** Fonksiyonun içine anahtarı yazsaydık
(`anahtar="cf_..."`) anahtar koda gömülmüş olurdu. Parametre olunca fonksiyon
anahtarı bilmez; kim çağırırsa o verir. `07_bozuk_kodlar.py` dosyasının 4.
sorusu tam olarak bunu düzeltiyor.

**Neden hata olunca metin döndürüyor?** Fonksiyon hata kodunu görünce durmuyor,
`"[HATA 401]"` gibi bir metin döndürüyor. Böylece beş soruluk bir döngüde tek
bir soru başarısız olursa diğer dördü yine sorulur. Bedeli şu: hata metni de
cevap gibi dosyaya yazılır. Dosyayı açtığında `[HATA` ile başlayan cevaplara bak.

**Kullanımı (anahtar gerekir):** artık tek satırla soru sorabiliriz:

```python
metin = modele_sor("Sessiz bir çalışma kafesi için üç renk öner.", hesap, anahtar)
print(metin)
```

---

## Adım 5 — Konunun çıktısı

```python
soru = input("Modele ne sormak istiyorsun? ")
metin = modele_sor(soru, hesap, anahtar)
print(metin)

with open("cevap.txt", "w", encoding="utf-8") as dosya:
    dosya.write(f"SORU: {soru}\n\nCEVAP:\n{metin}\n")
```

- `input()` programı durdurup senden bir satır bekler; yazdığın metni döndürür.
- Cevap hem ekrana hem Konu 1'deki gibi dosyaya yazılır.
- `\n` satır sonu demek; `\n\n` araya boş bir satır koyar. `cevap.txt` şöyle görünür:

```text
SORU: Sessiz bir çalışma kafesi için üç renk öner.

CEVAP:
Koyu yeşil, kırık beyaz, meşe tonu: ...
```

- `"w"` kipi dosyayı **her seferinde sıfırdan** yazar. Programı ikinci kez
  çalıştırırsan ilk cevap silinir. Bunu bilerek seçtik: `cevap.txt` hep son soruyu
  tutar. Bütün cevapları biriktirmek Adım 6'nın işi.

Anahtarın yoksa `05_soru_sor.py` yine sorunu alır, kayıtlı cevabı dosyaya yazar;
böylece akışın tamamını görebilirsin.

---

## Adım 6 — Aynı işi beş kez yap

`06_coklu_soru.py` soruları `02-api-ile-konusmak/veri/ornek_sorular.txt` dosyasından satır satır
okuyup `sorular` listesine koyar. Hazır dosyadaki beş soru aynı konuda: Konu 1'in
bulgusuyla, sessiz bir çalışma kafesinin yeni kimliği (slogan, renk, yazı tipi,
gönderi fikri, kaçınılacak klişeler). Kendi sorularını sormak için o dosyayı değiştir. Kendi
kopyanı kullanacaksan dosyanın başındaki `SORULAR_DOSYASI` satırındaki yolu da değiştir.

```python
sorular = []
with open("02-api-ile-konusmak/veri/ornek_sorular.txt", encoding="utf-8") as dosya:
    for satir in dosya:                    # her satır bir soru
        if satir.strip():                  # boş satırları atla
            sorular.append(satir.strip())

kayitlar = []
for soru in sorular:
    metin = modele_sor(soru, hesap, anahtar)
    kayitlar.append({"soru": soru, "cevap": metin})

with open("cevaplar.json", "w", encoding="utf-8") as dosya:
    json.dump(kayitlar, dosya, ensure_ascii=False, indent=2)
```

- Her soru–cevap çifti bir sözlük; bunların her birine **kayıt** diyoruz. Sonuç bir
  **liste** içinde **sözlükler**. Konu 3'ten itibaren veri hep bu biçimde gelecek.
- Dosya her istekten sonra 1 saniye bekler (`time.sleep`), sunucuyu yormamak için.
  Art arda çok hızlı istek atan programları sunucu **429** ile durdurabilir.
- `json.dumps` (sonunda **s**) sözlüğü metne çevirip ekrana basmak içindi;
  `json.dump` doğrudan **dosyaya** yazar. İkinci bilgiyi, yani dosyayı vermeyi
  unutursan: `TypeError: dump() missing 1 required positional argument: 'fp'`
  (`fp` dosya demek).
- Kodun asıl gücü burada: aynı işi elli kez yapmak, arayüzde yapamayacağın şey.
  Sohbet penceresine elli soruyu tek tek yapıştırıp cevapları tek tek kopyalamayı
  düşün.

`cevaplar.json` dosyasının içi şöyle görünür:

```json
[
  {"soru": "Müşterilerinin sessiz bir çalışma yeri ... üç kısa slogan yaz.",
   "cevap": "1) Sessizliğin adresi. 2) Kahven, prizin, zamanın. ..."},
  {"soru": "Sessiz bir çalışma kafesinin logosu için hangi üç rengi önerirsin, neden?",
   "cevap": "Koyu yeşil, kırık beyaz, meşe tonu: ..."}
]
```

### Kaydettiğini geri oku

Dosyaya yazmanın asıl faydası, sonradan açıp üzerinde çalışabilmek. Aşağıdaki kod
`cevaplar.json`'u okur ve her cevabın kaç kelime olduğunu yazar:

```python
with open("cevaplar.json", encoding="utf-8") as dosya:
    okunan = json.load(dosya)

for kayit in okunan:
    print(len(kayit["cevap"].split()), "kelime —", kayit["soru"][:45])
```

- `for kayit in okunan` her adımda bir **sözlük** verir, metin değil. Bu yüzden
  `kayit.split()` değil, `kayit["cevap"].split()`. (Sınıf alıştırmasının 3. sorusu
  bu hatayı arıyor.)
- Gerçek modelle çalıştırınca cevap uzunlukları çok farklı çıkar: slogan sorusuna
  birkaç satır, gönderi fikri sorusuna uzun bir liste. Hangi soruya ne kadar
  uzun cevap geldiğine bakmak, hangi sorunun modeli "konuşturduğunu" gösterir.
- Demo modunda beş satırın beşi de aynı sayıyı verir. Sebebini artık biliyorsun.

Bonus: `08_cevap_raporu.py` aynı dosyadan Konu 1'deki kelime bulutunu üretir
(`cevaplar-bulutu.png`). Kendi metnin değil, modelin yazdığı metin hangi kelimelere
yaslanıyor?

> **Kendini dene 6.** `cevaplar.json` dosyanı açtın; beş kaydın beşinde de `cevap`
> aynı. Bunun iki olası sebebi ne, hangisi olduğunu nasıl anlarsın?

---

## Adım 7 — Soru yazmak da bir tasarım kararı

Buraya kadar hep aynı uzun soruyu sorduk: "Müşterilerinin sessiz bir çalışma yeri
olarak anlattığı bir kafe için üç kısa slogan yaz." Neden sadece "Bir kafe için üç
kısa slogan yaz" demedik?

`09_baglam_farki.py` bu soruyu ölçüyor. Aynı isteği iki biçimde soruyor:

| Tür | Soru |
|---|---|
| **bağlamsız** | Bir kafe için üç kısa slogan yaz. |
| **bağlamlı** | Müşterilerinin sessiz bir çalışma yeri olarak anlattığı bir kafe için üç kısa slogan yaz. |

Her soruyu **üç kez** soruyor, çünkü model aynı soruya her seferinde başka cümleler
kurar; tek bir cevaba bakıp karar vermek yanıltıcı olur. Sonra cevaplarda iki grup
kelimeyi sayıyor: kahve klişeleri (`kahve`, `fincan`, `aroma`...) ve çalışma yerini
anlatan kelimeler (`sessiz`, `odak`, `priz`...).

Sayma işi Konu 1'deki sayacın kardeşi:

```python
def turkce_kucult(metin):
    return metin.replace("I", "ı").replace("İ", "i").lower()


def kelime_say(cevaplar, kelimeler):
    """Cevaplarda, listedeki kelimelerin toplam kaç kez geçtiğini sayar."""
    toplam = 0
    for cevap in cevaplar:
        kucuk = turkce_kucult(cevap)
        for kelime in kelimeler:
            toplam = toplam + kucuk.count(kelime)
    return toplam


KLISE = ["kahve", "fincan", "çekirdek", "aroma", "köpü", "yudum"]
ornek = ["Güne bir fincan kahveyle başla.", "Köpüğü bol, sohbeti koyu."]
print(kelime_say(ornek, KLISE))
```

```text
3
```

- `metin.count(kelime)` bir metnin içinde başka bir metnin kaç kez geçtiğini sayar.
  Kelimenin sadece **başını** yazıyoruz: `kahve` hem `kahve`yi hem `kahveyle`yi
  yakalar.
- Listede neden `köpük` değil de `köpü` var? Türkçede ek alınca `k` harfi `ğ` olur:
  `köpük` → `köpüğü`. `köpük` diye arasaydık `Köpüğü bol` cümlesini kaçırırdık.
- Konu 1'deki `turkce_kucult` burada da gerekli: `lower()` büyük `I`'yı `i` yapar,
  Türkçede ise `ı` olmalı.

`09_baglam_farki.py` dosyasının demo modunda (kayıtlı örnek cevaplarla,
`02-api-ile-konusmak/veri/baglam_ornek_cevaplar.json`) çıktısı:

```text
--- Sayım (3'er cevapta) ---
               kahve klişesi    çalışma yeri
bağlamsız                 11               0
bağlamlı                   1              12
```

**Bulgu:** Bulguyu söylemeyince model "ortalama bir kafe"yi anlatıyor: kahve, fincan,
aroma. Konu 1'de 30 yorumu sayarak bulduğumuz şey (müşteri buraya çalışmaya geliyor)
ancak soruya yazınca cevaba giriyor. Model senin kafeni tanımıyor; ona ne söylersen
onu biliyor. Soruyu yazmak, bir brief yazmak gibi bir tasarım işi.

Bu sonuç kayıtlı örnek cevaplardan. Kendi anahtarınla çalıştır ve kendi sayılarına
bak: aynı örüntü çıkıyor mu? Çıkmıyorsa cevapları oku; belki model başka klişelere
(`sıcak`, `sohbet`) yaslanıyor ve listeye eklemen gerekiyor.

**Sayımın sınırı:** Bağlamlı cevaplarda sayım bir kahve klişesi buldu: "Kahven,
prizin, zamanın." Ama bu cümle kahveyi övmüyor, kahveyi çalışma düzeninin bir
parçası olarak anıyor. Sayım yön gösterir; kararı cevapları okuyarak sen verirsin.

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
| — | Hata kodlarını tanıdık | `HATA_SOZLUGU`, `acikla()` | `04_hata_kodlari.py` |
| 4–5 | Fonksiyona sardık, soru alıp kaydettik | `modele_sor()`, `cevap.txt` | `05_soru_sor.py` |
| 6 | Döngüye soktuk | `cevaplar.json` | `06_coklu_soru.py` |
| 7 | Bağlamın etkisini ölçtük | kahve klişesi / çalışma yeri sayımı | `09_baglam_farki.py` |

Her dosyayı `gita3111` klasöründen çalıştır: `uv run 02-api-ile-konusmak/ornekler/01_anahtar_oku.py`.
Ürettikleri dosyalar (`cevap.txt`, `cevaplar.json`) de oraya yazılır.

`05`, `06` ve `09`, önceki dosyalardaki fonksiyonları kendi içlerinde tekrar içerir;
her dosya tek başına çalışsın diye. Kendi programında bunları yeniden yazmana gerek yok.

Derste kendi başına dolduracağın alıştırma: `alistirma/sinif_alistirmasi.py`.
Ek alıştırma: `07_bozuk_kodlar.py` (beş bozuk kod; anahtar gerekmez, vizedeki soru
tipine benzer). Bonus: `08_cevap_raporu.py` (cevaplarından kelime bulutu, Konu 1'in
kodu yeni veriyle). Önce `06` çalışmış olmalı; çıktısı `cevaplar-bulutu.png`.

---

## Sık karşılaşılan sorunlar

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `anahtar.txt bulunamadı` | Hesap açılmamış, dosya yanlış klasörde ya da adı `anahtar.txt.txt` | Demo moduyla devam et; dosyayı `gita3111` klasörüne koy, uzantıyı kontrol et |
| `FileNotFoundError: ... '02-api-ile-konusmak/veri/...'` | Komutu yanlış klasörden verdin | `gita3111` klasörüne dön |
| `ModuleNotFoundError: No module named 'requests'` | Kütüphane kurulu değil | `uv add -r 02-api-ile-konusmak/requirements.txt` |
| `[UYARI] anahtar.txt var ama ... okunamadı` | Dosyada `ACCOUNT_ID` ya da `API_TOKEN` satırı eksik | Dosyayı Adım 1'deki biçime göre düzelt |
| Beş soruya beş aynı cevap | Demo modundasın | Gerçek anahtarla çalıştır |
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
  Dosyalar programı çalıştırdığın klasörde aranır.
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
| **Demo modu** | Anahtar yokken kayıtlı bir cevapla çalışma; kod aynı, cevap kutudan |
| **Bağlam** | Soruya eklediğin ve modelin bilmediği bilgi; burada Konu 1'in bulgusu |
| **Kayıt** | Tek bir soru–cevap çifti; bir sözlük |

---

## Kendini dene — cevaplar

**1.** (a) `YANIT["result"]["usage"]["completion_tokens"]` → `2`.
(b) `IndexError: list index out of range`. `errors` listesi boş; sıfırıncı eleman
bile yok. (c) `KeyError: 'usage'`. `usage` en dıştaki sözlükte değil, `result`
içinde; bir kat atlandı.

**2.** `{"ACCOUNT_ID": "a1b2", "API_TOKEN": '"xyz789"'}`. Küçük harfli `account_id`
büyük harfe çevrilir; eşittir içermeyen not satırı atlanır. Ama token'ın değeri
tırnaklarla birlikte okunur: `"xyz789"`. İstek atarsan sunucu tırnaklı token'ı
tanımaz ve **401** döner. Çare: tırnakları sil.

**3.** (a) Başlık: `Bearer`'dan sonra boşluk yok, sunucuya `Bearerxyz...` gider →
**401**. (b) Adres: baştaki `f` yok; adrese hesap kimliği yerine `{hesap}` yazısı
gider → sunucu böyle bir hesap bulamaz, 4xx türünde bir hata döner. (c) Gövde:
sunucu soruyu `prompt` alanında bekliyor, `soru` alanını tanımıyor → **400**.

**4.** (a) `False`. (b) `None`. (c) `yanit["errors"][0]["message"]` →
`"Authentication error"`. (d) `TypeError: 'NoneType' object is not subscriptable`;
`result` boş olduğu için içine girilemez. Önce durum koduna ya da `success`
alanına bakmak gerekirdi.

**5.** (a) **429**: günlük kota bitti. Türkiye saatiyle 03:00'te sıfırlanır.
Döngüyü küçült, soruları kısalt; bu sırada demo moduyla çalışmaya devam edebilirsin.
(b) **401**: eski token silindiği için artık geçersiz. `anahtar.txt`'yi güncelle.
(c) Durum kodu gelmez, program `ConnectionError` ile durur; istek sunucuya hiç
ulaşmadı. (d) **500** sunucu tarafı demek; kodunu değiştirme, biraz sonra tekrar dene.

**6.** Birinci ihtimal: demo modundasın. Ekranın başında `[DEMO MODU]` ya da
`[UYARI]` satırı olur, cevap da "Sessizliğin adresi..." diye başlar. İkinci ihtimal:
her istek aynı hatayı aldı. O zaman beş cevabın beşi de `[HATA 401]` ya da
`[HATA 429]` gibi `[HATA` ile başlar; koda göre hata kodları tablosuna bak.

**7.** (a) O cevabı klişesiz sayardı; "yudum" kahveyi doğrudan söylemeden anıyor.
Sayım sadece listede yazan kelimeleri görür; listeyi cevapları okuyarak genişletmek
gerekir. (b) Örneğin "müşteriler en çok priz ve internetten bahsediyor" ya da
"müşterilerin çoğu öğrenci". Doğru cevap yok; önemli olan, modelin bilemeyeceği ve
senin veriden bulduğun bir bilgiyi eklemek.

---

## Ödev — iki parça

`odevler/odev2.md` (puansız; sırası gelen sınıfta gösterir):

1. **Kendi beş sorun:** soru dosyasına aynı konuda kendi beş sorunu yaz, `06_coklu_soru.py` ile
   çalıştır, `cevaplar.json` dosyanı getir. Bir de tek cümle: beş cevaptan hangisi
   işe yaramazdı, sence neden? (Adım 7'yi hatırla: sebep soruda olabilir.)
2. **Renk etiketleme:** `veri/renkler.csv` içindeki 20 renge sakin / enerjik / ciddi
   etiketi ver.

İkinci parça **Konu 3'ün verisi**. Yapılmazsa eğitecek veri olmaz. Doğru cevap
yok; herkesin etiketi farklı olacak, mesele de bu.

Birinci parça gerçek anahtar ister: demo modunda beş soruya aynı cevap gelir.

## Sonraki konu

**Konu 3 — Makine öğrenmesi** (`03-makine-ogrenmesi`). Bu konuda hazır bir modele
soru sorduk. Konu 3'te kendi modelimizi eğiteceğiz, hem de sınıfın ödevde verdiği
renk etiketleriyle.
