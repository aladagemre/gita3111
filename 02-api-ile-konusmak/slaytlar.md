# Konu 2 — İnterneti Koddan Konuşturmak

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 1'de, bu konuda

**Konu 1'de:** elimizdeki bir metni işledik. Veri bilgisayarındaydı.
Bulgu: müşteriler kafeyi **sessiz bir çalışma yeri** olarak anlatıyor.

**Bu konuda:** veri dışarıdan gelecek. Kodun ilk kez bilgisayarının dışına çıkıyor.

- Bir soruyu uzaktaki bir modele göndereceğiz
- Cevabı geri alıp dosyaya yazacağız
- Aynı işi döngüyle beş kez yapacağız
- Soruya bağlam yazmanın cevabı nasıl değiştirdiğini ölçeceğiz

Bu, dersin **kritik konusu**: Konu 4, 5, 8, 9, 10 ve 11 bunun üstüne kuruluyor.

-----

## Bugünün planı

Her adım bir dosya; dosyalar adım adım büyüyor:

**1.** Anahtarı dosyadan oku — `01_anahtar_oku.py`
**2.** İsteğin üç parçasını hazırla ve gönder — `02_ilk_istek.py`
**3.** Yanıtın içinden metni çek — `03_yaniti_coz.py`
**4.** Hata kodlarını tanı — `04_hata_kodlari.py`
**5.** Soruyu fonksiyona koy, cevabı kaydet — `05_soru_sor.py`
**6.** Aynı işi döngüyle beş kez yap — `06_coklu_soru.py`
**7.** Soruya bağlam koy, farkı ölç — `09_baglam_farki.py`

-----

## Anahtarın yoksa?

Bugünkü örnekler **gerçek istek** atıyor. `anahtar.txt` yoksa program ilk satırda durur:

`FileNotFoundError: [Errno 2] No such file or directory: '../anahtar.txt'`

- Ders boyunca **yanındakiyle birlikte** çalış: onun ekranında izle, kodu sen de yaz
- Adım 3 anahtarsız da çalışır: kayıtlı bir yanıtı okur
- Konu 00'daki kurulum yönergesinin **6. adımını** (Cloudflare hesabı) bugün bitir

Ödev için kendi anahtarın gerekiyor; Konu 4'ten itibaren her derste de gerekecek.

-----

## İstemci ve sunucu

Tarayıcıda her gün yaptığın şeyin kodla yapılan hâli:

- **Sen** (istemci) bir şey istiyorsun
- **Uzaktaki bilgisayar** (sunucu) cevap veriyor
- Tarayıcı da aynı isteği atıyor — sadece üstünde bir arayüz var

Bugün arayüzü kaldırıp isteği kendimiz atacağız.

-----

## Bir sorunun yolculuğu

| Aşama | Ne oluyor | Bozulursa |
|---|---|---|
| 1. Hazırlık | Adres, başlık, gövde hazırlanır | Python hatası |
| 2. Yol | İstek internetten gider | `ConnectionError` — **durum kodu yok** |
| 3. Kimlik | Sunucu anahtara bakar | **401 / 403** |
| 4. İş | Model çalışır | **400 / 404 / 429 / 500** |
| 5. Dönüş | JSON gelir, sen içine girersin | `KeyError`, `TypeError` |

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

`anahtar.txt` dosyan şöyle görünüyor:

```
ACCOUNT_ID = a1b2c3...
API_TOKEN = xyz789...
```

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

-----

## Adım 1 — satır satır ne oldu?

| Aşama | Değer |
|---|---|
| Dosyadaki satır | `'API_TOKEN = xyz789\n'` |
| `partition("=")` sonrası | `('API_TOKEN ', '=', ' xyz789\n')` |
| `ad.strip()` | `'API_TOKEN'` |
| `deger.strip()` | `'xyz789'` |

- `anahtarlar` bir **sözlük** — Konu 1'in konusu
- `"../anahtar.txt"`: `..` **bir üst klasör**; bütün konular aynı dosyayı kullanır
- Anahtarı **ekrana basmıyoruz**; sadece okunduğunu söylüyoruz

-----

## Bir isteğin üç parçası

| Parça | Ne söyler |
|---|---|
| **Adres** | Nereye gidiyorum |
| **Başlık** | Ben kimim |
| **Gövde** | Ne istiyorum |

```python
MODEL = "@cf/google/gemma-4-26b-a4b-it"
adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
basliklar = {"Authorization": f"Bearer {anahtar}"}
govde = {"prompt": "Müşterilerinin sessiz bir çalışma yeri olarak anlattığı bir kafe için üç kısa slogan yaz."}
```

Üçü de sıradan Python değişkeni: iki metin, iki sözlük.

-----

## Üç parçanın klasik hataları

| Parça | Hata | Sonuç |
|---|---|---|
| Adres | Baştaki `f` unutulmuş → sunucuya `{hesap}` yazısı gider | Hata kodu |
| Başlık | `f"Bearer{anahtar}"` → boşluk yok | **401** |
| Gövde | `{"soru": ...}` → sunucu `prompt` bekliyor | **400** |

Şüphelenirsen `print(adres)` — adreste token yok, basmak güvenli.

-----

## Adım 2 — İsteği gönder

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

- `post` demek "sana bir şey gönderiyorum, karşılığında cevap bekliyorum"
- `timeout=60` → "60 saniyede cevap gelmezse vazgeç"
- `status_code` işlerin yolunda gidip gitmediğini söyleyen sayı; `200` = yolunda

-----

## Gelen cevap: JSON

```python
yanit = cevap.json()
print(json.dumps(yanit, ensure_ascii=False, indent=2))
```

- `cevap.json()` gelen içeriği tanıdık bir **sözlüğe** çevirir
- `json.dumps` sözlüğü okunabilir metne çevirir; `indent=2` girintili yazar

Gelen yanıtın biçimi (`veri/ornek_yanit.json`, kayıtlı bir yanıt):

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

-----

## Adım 3 — Yanıtın içine bak

Kayıtlı bir yanıtla çalışıyoruz — **anahtarsız da çalışır**:

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

**Kural:** Yanıtın yapısını bilmiyorsan önce katlarını sor, sonra içine gir.

-----

## Adım 3 — Metni ve belirteci çek

```python
metin = yanit["result"]["response"]
print(metin)

kullanim = yanit["result"]["usage"]
print("Harcanan belirteç:", kullanim["total_tokens"])
```

- İki kat içeri: önce `result`, sonra `response`
- `yanit["response"]` yazarsan **KeyError** — bu konunun en sık hatası
- Belirteç (token) kelime değil, kelime parçası — Konu 5'te açacağız

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

## Adım 4 — Kasten yanlış anahtar

```python
sahte_basliklar = {"Authorization": "Bearer bu-anahtar-sahte"}

cevap = requests.post(adres, headers=sahte_basliklar, json={"prompt": "merhaba"}, timeout=60)

if cevap.status_code == 200:
    print(cevap.json()["result"]["response"])
else:
    print("İstek başarısız:", cevap.status_code)
    print(cevap.text)
```

**Yanıtı okuma sırası:** önce durum kodu, 200 ise içine gir.
`cevap.text` sunucunun gönderdiği ham metin — hatanın açıklaması orada.

-----

## 401'in içi: `result` boş

Yanlış anahtarla gelen yanıt:

```json
{"result": null, "success": false,
 "errors": [{"code": 10000, "message": "Authentication error"}]}
```

`yanit["result"]["response"]` yazarsan:

`TypeError: 'NoneType' object is not subscriptable`

Kodunda yazım hatası yok — **istek başarısız olmuş.** Sebep bir önceki satırda.

-----

## Adım 5 — Soruyu fonksiyona koyalım

```python
def modele_sor(soru):
    cevap = requests.post(adres, headers=basliklar, json={"prompt": soru}, timeout=60)
    return cevap.json()["result"]["response"]
```

- Gönder ve metni çek: iki adım tek isim altında
- `adres` ve `basliklar` yukarıda bir kez hazırlandı; fonksiyon onları kullanıyor
- Artık tek satırla soru sorabiliriz: `modele_sor("...")`

-----

## Adım 5 — Konunun çıktısı

```python
soru = input("Modele ne sormak istiyorsun? ")
metin = modele_sor(soru)
print(metin)

with open("cevap.txt", "w", encoding="utf-8") as dosya:
    dosya.write(f"SORU: {soru}\n\nCEVAP:\n{metin}\n")
```

- Kullanıcıdan soru alıyor
- Modele soruyor
- Cevabı hem ekrana basıyor hem dosyaya yazıyor — Konu 1'deki dosya yazması

-----

## Adım 6 — Aynı işi beş kez yapmak

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

Kodun asıl gücü burada başlıyor: aynı işi elli kez yapmak — arayüzde yapamayacağın şey.

-----

## Ne kaydettik?

`cevaplar.json` dosyasının biçimi:

```json
[
  {"soru": "Müşterilerinin sessiz bir çalışma yeri ... üç kısa slogan yaz.",
   "cevap": "..."},
  {"soru": "Sessiz bir çalışma kafesinin logosu için hangi üç rengi önerirsin, neden?",
   "cevap": "..."}
]
```

- Bir **liste** içinde **sözlükler**
- Konu 1'de sözlükle çalıştık, bu konuda sözlük listesiyle
- Konu 3'ten itibaren veri hep bu şekilde gelecek

-----

## Adım 7 — Neden hep o uzun soru?

Aynı istek, iki biçim:

| Tür | Soru |
|---|---|
| **bağlamsız** | Bir kafe için üç kısa slogan yaz. |
| **bağlamlı** | Müşterilerinin sessiz bir çalışma yeri olarak anlattığı bir kafe için üç kısa slogan yaz. |

Her birini **üç kez** soruyoruz (model her seferinde başka cümle kurar),
sonra cevaplarda kahve kelimelerini ve çalışma yeri kelimelerini sayıyoruz.

-----

## Bağlamı ölçmek

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

Her satır: kelime, bağlamsız cevaplarda kaç kez, bağlamlı cevaplarda kaç kez.

-----

## Bulgu: soru yazmak da tasarım

Kendi sayılarına bak:

- Bağlamsız cevaplarda hangi kelimeler çok: `kahve`, `fincan`, `aroma` mı?
- Bağlamlı cevaplarda `sessiz`, `odak`, `priz` geçiyor mu?
- Sayım yön gösterir; kararı **cevapları okuyarak** verirsin

Model senin kafeni tanımıyor; ona ne söylersen onu biliyor.
Konu 1'de veriden bulduğumuz şey ancak soruya yazınca cevaba girer.
Soruyu yazmak bir **brief** yazmak gibi.

-----

## Adımlar ve dosyalar

| Adım | Ne yaptık | Elimizde ne oluştu |
|---|---|---|
| 1 | Anahtarı okuduk | `hesap`, `anahtar` |
| 2 | İsteği kurup gönderdik | `adres`, `basliklar`, `govde` → `yanit` |
| 3 | İçinden metni çektik | `metin` |
| 4 | Hata kodunu okuduk | `if cevap.status_code == 200` |
| 5 | Fonksiyona sardık, dosyaya yazdık | `modele_sor()`, `cevap.txt` |
| 6 | Döngüye soktuk | `cevaplar.json` |
| 7 | Bağlamın etkisini ölçtük | kelime sayımı |

Her dosya bir öncekinin üstüne kuruluyor.

-----

## En sık görülecek hata mesajları

| Mesaj | Anlamı |
|---|---|
| `FileNotFoundError: ... '../anahtar.txt'` | Anahtar dosyası yok ya da yanlış yerde |
| `KeyError: 'response'` | Bir kat atladın: `["result"]["response"]` |
| `TypeError: list indices must be integers...` | `errors` listesini adla açtın: `[0]` |
| `TypeError: 'NoneType' object is not subscriptable` | İstek başarısız; önce durum kodu |
| `requests.exceptions.ConnectionError` | İnternet yok; istek hiç gitmedi |

Hata mesajını **sondan** oku: en alt satır hatanın türü ve açıklaması.

-----

## Bu konunun ödevi — iki parça

**1. Kendi beş sorun.** `06_coklu_soru.py`'yi yeni bir adla kopyala, kopyayla çalıştır,
`cevaplar.json` getir.
Tek soru cevapla: hangi cevap işe yaramazdı, neden? (İpucu: Adım 7)

**2. Renk etiketleme.** `veri/renkler.csv`'yi kendi adınla kopyala, kopyadaki 20 renge
duygu etiketi ver: sakin / enerjik / ciddi.

İkinci parça **Konu 3'ün verisi.** Yapılmazsa sınıfın eğitecek verisi olmaz.
Doğru cevap yok — herkesin etiketi farklı olacak, mesele de bu.

-----

## Hatırlanacak dört şey

**1. Bir istek üç şeyden oluşur:** nereye, kim olduğun, ne istediğin.

**2. Gelen cevap düz metin değil**, içine girilecek bir sözlüktür. Bilmiyorsan
önce katlarını sor.

**3. Anahtar koda yazılmaz.** Ayrı dosyada durur, teslime konmaz, ekranda
gösterilmez.

**4. Soruya yazdığın bağlam cevabı değiştirir.** Model senin bulgunu bilmez.

Sıradaki konu: **Konu 3 — makine öğrenmesi.** Sınıfın kendi etiketlediği
renklerle model eğiteceğiz.
