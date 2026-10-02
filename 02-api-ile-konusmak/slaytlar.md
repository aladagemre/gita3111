# Konu 2 — İnterneti Koddan Konuşturmak

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 1'de, bu konuda

**Konu 1'de:** elimizdeki bir metni işledik. Veri bilgisayarındaydı.
Bulgu: müşteriler kafeyi **sessiz bir çalışma yeri** olarak anlatıyor.

**Bu konuda:** veri dışarıdan gelecek. Kodun ilk kez bilgisayarının dışına çıkıyor.

- Bir soruyu uzaktaki bir modele göndereceğiz
- Cevabı geri alıp içinden metni çekeceğiz
- Aynı işi döngüyle birkaç kez yapıp cevapları dosyaya yazacağız
- Soruya bağlam yazmanın cevabı nasıl değiştirdiğine bakacağız

Bu, dersin **kritik konusu**: Konu 4, 5, 8, 9, 10 ve 11 bunun üstüne kuruluyor.

-----

## Bugünün planı

Hepsi tek bir defterde: `ders.ipynb`

**Isınma** — iç içe sözlük
**1.** Anahtarı dosyadan oku
**2.** İsteği hazırla: adres, başlık, gövde
**3.** Gönder
**4.** Gelen yanıta bak
**5.** Yanlış anahtarla dene
**6.** Fonksiyona koy
**7.** Birden çok soru, cevaplar dosyaya
**8.** Soruya bağlam koymak cevabı değiştirir mi?

-----

## Defteri çalıştırmak

- VS Code'da `02-api-ile-konusmak` klasöründeki `ders.ipynb`'yi aç
- Sağ üstten çekirdek olarak bu klasörün **`.venv`**'ini seç
- Hücreye tıkla, **Shift + Enter**: hücre çalışır, alttakine geçer
- Hücreler **yukarıdan aşağı, sırayla**: her hücre bir öncekinin değişkenini kullanır

Bir hücreyi atlarsan: `NameError: name '...' is not defined`
Çare: atladığın hücreye dön, oradan sırayla devam et.

-----

## Anahtarın yoksa?

Adım 1'den sonraki hücreler `anahtar.txt` ister. Dosya yoksa Adım 1 durur:

`FileNotFoundError: [Errno 2] No such file or directory: '../anahtar.txt'`

- Ders boyunca **yanındakiyle birlikte** çalış: onun ekranında izle, hücreleri sen de yaz
- Isınma ve alıştırma defteri (`alistirma.ipynb`) anahtarsız çalışır
- Konu 00'daki kurulum yönergesinin **6. adımını** (Cloudflare hesabı) bugün bitir

Ödev için kendi anahtarın gerekiyor; Konu 4'ten itibaren her derste de gerekecek.

-----

## Isınma — iç içe sözlük

Modelden gelen yanıt **sözlüğün içinde sözlük** olacak. Önce elle bir tane kuralım.
Son satır hata veriyor. Neden?

```python
yanit = {
    "success": True,
    "result": {"response": "Merhaba!"},
}

print(yanit["response"])
```

`KeyError: 'response'` — "bu sözlükte `response` diye bir anahtar yok."

-----

## Isınma — katman katman in

`"response"` doğrudan `yanit`'ın içinde değil, `"result"`'ın içinde:

```python
sonuc = yanit["result"]
print(sonuc)
```

```python
metin = sonuc["response"]
print(metin)
```

Her satır **bir kat** iner. Her katın kendi değişkeni var: önce `sonuc`, sonra `metin`.

-----

## İstemci ve sunucu

Tarayıcıda her gün yaptığın şeyin kodla yapılan hâli:

- **Sen** (istemci) bir şey istiyorsun
- **Uzaktaki bilgisayar** (sunucu) cevap veriyor
- Tarayıcı da aynı isteği atıyor — sadece üstünde bir arayüz var

Programların birbirine soru sorduğu bu kapıya **API** denir.
Bugün arayüzü kaldırıp isteği kendimiz atacağız.

-----

## Bir sorunun yolculuğu

| Aşama | Ne oluyor | Bozulursa |
|---|---|---|
| 1. Hazırlık | Adres, başlık, gövde hazırlanır | Python hatası |
| 2. Yol | İstek internetten gider | `ConnectionError` — **durum kodu yok** |
| 3. Kimlik | Sunucu anahtara bakar | **401 / 403** |
| 4. İş | Model çalışır | **400 / 404 / 429 / 500** |
| 5. Dönüş | Yanıt gelir, sen içine girersin | `KeyError`, `TypeError` |

Hata aldığında "neresi bozuk?" sorusunu tahminle değil, **işaretle** cevaplarsın.

-----

## Anahtar neden gizli?

Anahtarın senin kimliğin. Başkasının eline geçerse **senin adına** istek atar ve
kotanı bitirir.

Üç kural:

- Anahtar **koda yazılmaz** — ayrı bir dosyada durur
- O dosya **ödev teslimine konmaz**
- Ekran paylaşırken **açık bırakılmaz**

Yanlışlıkla paylaştıysan panik yok: panelden silip yenisini üretmek 30 saniye.

-----

## Adım 1 — Anahtarı dosyadan oku

`anahtar.txt` (`gita3111` klasöründe) şöyle görünüyor:

```
ACCOUNT_ID = a1b2c3...
API_TOKEN = xyz789...
```

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
print(hesap)
```

-----

## Adım 1 — bir satırın yolculuğu

| Aşama | Değer |
|---|---|
| Dosyadaki satır | `'API_TOKEN = xyz789\n'` |
| `satir.split("=")` | `['API_TOKEN ', ' xyz789\n']` |
| `parcalar[0].strip()` | `'API_TOKEN'` |
| `parcalar[1].strip()` | `'xyz789'` |

- `..` **bir üst klasör**: bütün konular aynı `anahtar.txt`'yi kullanır
- `anahtarlar` bir **sözlük** — Konu 1'in konusu
- Ekrana yalnızca **hesap kimliğini** basıyoruz; anahtarın kendisini değil

-----

## Adım 2 — İsteğin üç parçası

| Parça | Ne söyler |
|---|---|
| **Adres** | Nereye gidiyorum |
| **Başlık** | Ben kimim (anahtar burada gider) |
| **Gövde** | Ne istiyorum |

```python
import requests

MODEL = "@cf/google/gemma-4-26b-a4b-it"
adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
basliklar = {"Authorization": f"Bearer {anahtar}"}
govde = {"prompt": "Sessiz bir çalışma kafesi için üç kısa slogan yaz."}
```

Üçü de sıradan Python değişkeni: bir metin, iki sözlük.

-----

## Üç parçanın klasik hataları

| Parça | Hata | Sonuç |
|---|---|---|
| Adres | Baştaki `f` unutulmuş → sunucuya `{hesap}` yazısı gider | Hata kodu |
| Başlık | `f"Bearer{anahtar}"` → boşluk yok | **401** |
| Gövde | `{"soru": ...}` → sunucu `prompt` bekliyor | **400** |

Şüphelenirsen `print(adres)` — adreste anahtar yok, basmak güvenli.

-----

## Adım 3 — Gönder

```python
cevap = requests.post(adres, headers=basliklar, json=govde)
print(cevap.status_code)
```

- `post` demek "sana bir şey gönderiyorum, karşılığında cevap bekliyorum"
- `status_code` işlerin yolunda gidip gitmediğini söyleyen sayı
- `200` = "tamam"

-----

## Adım 4 — Gelen yanıta bak

```python
yanit = cevap.json()
print(yanit)
```

Gelen yanıt bir sözlük. Isınmadakinin aynısı, sadece daha kalabalık:

```python
sonuc = yanit["result"]
metin = sonuc["response"]
print(metin)
```

İki kat iniyoruz: önce `result`, sonra `response`.

-----

## Yanıtın biçimi: JSON

Sunucular veriyi **JSON** adlı metin biçiminde yollar; `cevap.json()` onu sözlüğe çevirir.
Kısaltılmış hâli:

```json
{"success": true, "errors": [], "result": {"response": "..."}}
```

| JSON'da | Python'da |
|---|---|
| `true` / `false` | `True` / `False` |
| `null` | `None` |

Ekranda `true` görüp kodda `"true"` yazarsan eşleşmez: değer metin değil, `True`.

-----

## Hata kodları

| Kod | Anlamı | Ne yaparsın |
|---|---|---|
| **401** | Yetki yok | Anahtarı kontrol et, bir karakter düşmüş olabilir |
| **403** | İzin yok | Token'ı yeniden üret |
| **404** | Adres yanlış | Model adını ve hesap kimliğini kontrol et |
| **429** | Kota doldu | Kota her gün 00:00 UTC'de sıfırlanır |
| **500** | Sunucu hatası | Senin kodunda sorun yok, tekrar dene |

İlk hane kime bakacağını söyler: **4xx senin tarafın**, **5xx sunucunun.**

-----

## Adım 5 — Yanlış anahtarla dene

Bilerek sahte bir anahtar gönderiyoruz. Durum kodu ne oldu?

```python
sahte_basliklar = {"Authorization": "Bearer yanlis-anahtar"}
cevap = requests.post(adres, headers=sahte_basliklar, json=govde)
print(cevap.status_code)
print(cevap.text)
```

- `cevap.text` sunucunun gönderdiği ham metin — hatanın açıklaması orada
- Bu yanıtta `result` boş (`null`): içine girersen
  `TypeError: 'NoneType' object is not subscriptable`

-----

## Adım 5 — Önce durum koduna bak

```python
if cevap.status_code == 200:
    print("Tamam")
else:
    print("Bir sorun var:", cevap.status_code)
```

**Yanıtı okuma sırası:** önce durum kodu, 200 ise içine gir.

`TypeError: 'NoneType' ...` görürsen kodunda yazım hatası arama: **istek başarısız
olmuş.** Sebep durum kodunda.

-----

## Adım 6 — Fonksiyona koy

Her soru için aynı satırları yazmamak için:

```python
def modele_sor(soru):
    govde = {"prompt": soru}
    cevap = requests.post(adres, headers=basliklar, json=govde)
    yanit = cevap.json()
    sonuc = yanit["result"]
    return sonuc["response"]
```

```python
print(modele_sor("Sessiz bir çalışma kafesinin logosu için üç renk öner."))
```

`adres` ve `basliklar` yukarıda bir kez hazırlandı; fonksiyona yalnızca değişen şeyi,
soruyu veriyoruz.

-----

## Adım 7 — Birden çok soru, cevaplar dosyaya

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

Kodun asıl gücü burada: aynı işi elli kez yapmak — arayüzde yapamayacağın şey.

-----

## Adım 8 — Bağlam cevabı değiştirir mi?

Konu 1'in bulgusunu soruya koyunca sloganlar nasıl değişiyor?

```python
baglamsiz = modele_sor("Bir kafe için üç kısa slogan yaz.")
baglamli = modele_sor("Müşterilerinin sessiz bir çalışma yeri olarak anlattığı bir kafe için üç kısa slogan yaz.")

print(baglamsiz)
print()
print(baglamli)
```

İki cevabı yan yana oku. Hangisinde "kahve" var, hangisinde "sessizlik", "odak"?

-----

## Bulgu: soru yazmak da tasarım

- Bağlamsız soruda model **ortalama bir kafeyi** anlatır: kahve, fincan, aroma
- Bağlamlı soruda Konu 1'de veriden bulduğumuz şey cevaba girer
- Model her seferinde başka cümle kurar: hücreyi bir kez daha çalıştır, yine bak

Model senin kafeni tanımıyor; ona ne söylersen onu biliyor.
Soruyu yazmak bir **brief** yazmak gibi.

-----

## Adımlar

| Adım | Ne yaptık | Elimizde ne oluştu |
|---|---|---|
| 1 | Anahtarı okuduk | `hesap`, `anahtar` |
| 2 | İsteği hazırladık | `adres`, `basliklar`, `govde` |
| 3 | Gönderdik | `cevap`, durum kodu |
| 4 | İçinden metni çektik | `yanit` → `sonuc` → `metin` |
| 5 | Hata kodunu okuduk | `if cevap.status_code == 200` |
| 6 | Fonksiyona koyduk | `modele_sor()` |
| 7 | Döngüye soktuk | `cevaplar.txt` |
| 8 | Bağlamın etkisine baktık | iki cevap yan yana |

-----

## En sık görülecek hata mesajları

| Mesaj | Anlamı |
|---|---|
| `FileNotFoundError: ... '../anahtar.txt'` | Anahtar dosyası yok ya da yanlış yerde |
| `NameError: name 'hesap' is not defined` | Bir hücreyi atladın; sırayla çalıştır |
| `KeyError: 'response'` | Bir kat atladın: önce `result` |
| `TypeError: 'NoneType' object is not subscriptable` | İstek başarısız; önce durum kodu |
| `requests.exceptions.ConnectionError` | İnternet yok; istek hiç gitmedi |

Hata mesajını **sondan** oku: en alt satır hatanın türü ve açıklaması.

-----

## Bu konunun ödevi — iki parça

**1. Kendi soruların.** `ders.ipynb`'yi yeni bir adla kopyala; Adım 7'deki `sorular`
listesine aynı konuda **kendi beş sorunu** yaz, çalıştır, `cevaplar.txt` getir.
Tek soru cevapla: hangi cevap işe yaramazdı, neden? (İpucu: Adım 8)

**2. Renk etiketleme.** `veri/renkler.csv`'yi kendi adınla kopyala, kopyadaki 20 renge
duygu etiketi ver: sakin / enerjik / ciddi.

İkinci parça **Konu 3'ün verisi.** Yapılmazsa sınıfın eğitecek verisi olmaz.
Doğru cevap yok — herkesin etiketi farklı olacak, mesele de bu.

-----

## Hatırlanacak dört şey

**1. Bir istek üç şeyden oluşur:** nereye, kim olduğun, ne istediğin.

**2. Gelen cevap düz metin değil**, içine girilecek bir sözlüktür. Her satırda
bir kat in.

**3. Anahtar koda yazılmaz.** Ayrı dosyada durur, teslime konmaz, ekranda
gösterilmez.

**4. Soruya yazdığın bağlam cevabı değiştirir.** Model senin bulgunu bilmez.

Sıradaki konu: **Konu 3 — makine öğrenmesi.** Sınıfın kendi etiketlediği
renklerle model eğiteceğiz.
