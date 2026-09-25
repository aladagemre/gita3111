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

Yine **tek bir program** yazacağız, adım adım büyüyecek:

**1.** Anahtarı dosyadan oku
**2.** İsteğin üç parçasını hazırla ve gönder
**3.** Yanıtın içinden metni çek (ve hataları tanı)
**4.** Soruyu bir fonksiyona koy
**5.** Kullanıcıdan soru al, cevabı kaydet
**6.** Aynı işi döngüyle beş kez yap
**7.** Soruya bağlam koy, farkı ölç

-----

## Anahtarın yoksa?

Bugünkü örneklerin çoğu **DEMO modunda** çalışıyor.

- `anahtar.txt` yoksa kayıtlı bir cevap kullanılıyor
- Kod aynı kod; sadece cevap kutudan geliyor
- Yani dersi takip edebilirsin

**Ama bu bir köprü, çözüm değil.** Ödev için kendi anahtarın gerekiyor ve
Konu 4'ten itibaren demo modu yetmiyor. Bugün halledeceğiz.

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
def anahtarlari_oku(yol="../anahtar.txt"):
    degerler = {}
    with open(yol, encoding="utf-8") as dosya:
        for satir in dosya:
            if "=" in satir:
                ad, _, deger = satir.partition("=")
                degerler[ad.strip().upper()] = deger.strip()
    return degerler
```

Konu 1'in dosya okuma bilgisi burada işe yarıyor; bu sefer dosyayı **satır satır** geziyoruz.

`"../anahtar.txt"`: `..` **bir üst klasör** demek. Komutu konu klasöründen verdiğimiz için
bu yol `gita3111/anahtar.txt`'yi gösterir; bütün konular aynı anahtar dosyasını kullanır.

-----

## Okuduğumuzu kullanalım

```python
anahtarlar = anahtarlari_oku()

hesap = anahtarlar["ACCOUNT_ID"]
anahtar = anahtarlar["API_TOKEN"]

print("Account ID okundu mu:", "evet" if hesap else "hayır")
print("Token'ın ilk 6 karakteri:", anahtar[:6] + "...")
```

- `anahtarlar` bir **sözlük** — Konu 1'in konusu
- Anahtarı **asla tam olarak** ekrana basma; sadece okunduğunu doğrula

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

```python
import requests

cevap = requests.post(adres, headers=basliklar, json=govde, timeout=60)

print("Durum kodu:", cevap.status_code)

yanit = cevap.json()
```

- `post` demek "sana bir şey gönderiyorum, karşılığında cevap bekliyorum"
- `timeout=60` → "60 saniyede cevap gelmezse vazgeç". Bu olmazsa program sonsuza
  kadar bekleyebilir
- `status_code` işlerin yolunda gidip gitmediğini söyleyen sayı
- `cevap` henüz bir **yanıt nesnesi**; içindeki veriye ulaşmak için `.json()`
  diyoruz ve elimize tanıdık bir **sözlük** geçiyor

-----

## Gelen cevap: JSON

```python
import json

print(json.dumps(yanit, ensure_ascii=False, indent=2))
```

- `json.dumps` sözlüğü okunabilir metne çevirir — ekrana basmak için
- `ensure_ascii=False` → Türkçe harfler bozulmadan görünsün
- `indent=2` → iç içe yapı girintili yazılsın, gözle takip edilebilsin

Ekranda gördüğün şey:

```json
{
  "result": {
    "response": "1) Sessizliğin adresi. 2) Kahven, prizin, zamanın. ...",
    "usage": {"prompt_tokens": 24, "completion_tokens": 22, "total_tokens": 46}
  },
  "success": true,
  "errors": []
}
```

JSON = sözlüğün ağ üzerinde yazılmış hâli. Yani tanıdık bir şey.

-----

## Adım 3 — Metni içinden çek

```python
metin = yanit["result"]["response"]

print(metin)
```

- İki kat içeri giriyoruz: önce `result`, sonra `response`
- `yanit["response"]` yazarsan **KeyError** alırsın — bu konunun en sık hatası
- `errors` bir **liste**: `yanit["errors"][0]["message"]`

**Kural:** Yanıtın yapısını bilmiyorsan önce ham hâlini bas, sonra içine gir.

-----

## Kaç belirteç harcadık?

```python
kullanim = yanit["result"]["usage"]

print("Harcanan belirteç:", kullanim["total_tokens"])
```

- Üç kat içeride: `result` → `usage` → `total_tokens`
- Belirteç (token) kelime değil, kelime parçası — Konu 5'te açacağız
- Ücretsiz kotan günde 10.000 "neuron" ile ölçülür; belirteç sayısı bunun kaba göstergesi

-----

## Hata kodları

| Kod | Anlamı | Ne yaparsın |
|---|---|---|
| **401** | Yetki yok | Anahtarı kontrol et, bir karakter düşmüş olabilir |
| **403** | İzin yok | Token'ı yeniden üret |
| **404** | Adres yanlış | Model adını ve hesap kimliğini kontrol et |
| **429** | Kota doldu | Kota her gün 00:00 UTC'de sıfırlanır |
| **500** | Sunucu hatası | Senin kodunda sorun yok, tekrar dene |

Birazdan kasten yanlış anahtar gönderip **401'i canlı göreceğiz.**

-----

## Hatayı kodla karşılamak

```python
def durum_acikla(kod):
    aciklama = {
        200: "Her şey yolunda.",
        401: "Yetki yok. Anahtarı kontrol et.",
        429: "Kota doldu. Yarın sıfırlanır.",
        500: "Sunucu hatası. Tekrar dene.",
    }
    return aciklama.get(kod, "Tanımadığım bir kod.")


print(durum_acikla(cevap.status_code))
```

`.get(kod, "...")` — Konu 1'deki sayacın kalıbının aynısı: varsa değeri, yoksa yedek.

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

## Yanıtı okuma sırası

```python
if cevap.status_code == 200:
    metin = cevap.json()["result"]["response"]
    print(metin)
else:
    print("İstek başarısız:", cevap.status_code)
    print(cevap.text[:300])
```

**1.** Önce durum kodu. **2.** 200 ise içine gir.

Kodun ilk hanesi kime bakacağını söyler: **4xx senin tarafın**, **5xx sunucunun.**

-----

## Adım 4 — Soruyu fonksiyona koyalım

```python
def modele_sor(soru, hesap, anahtar):
    adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
    basliklar = {"Authorization": f"Bearer {anahtar}"}
    cevap = requests.post(adres, headers=basliklar, json={"prompt": soru}, timeout=60)
    if cevap.status_code != 200:
        return f"[HATA {cevap.status_code}]"
    return cevap.json()["result"]["response"]
```

Dağınık duran adımları tek isim altında topladık. Artık tek satırla soru sorabiliriz.

-----

## Adım 5 — Konunun çıktısı

```python
soru = input("Modele ne sormak istiyorsun? ")
metin = modele_sor(soru, hesap, anahtar)

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

Kodun asıl gücü burada başlıyor: aynı işi elli kez yapmak — arayüzde yapamayacağın şey.

-----

## Ne kaydettik?

`cevaplar.json` dosyasının içi:

```json
[
  {"soru": "Müşterilerinin sessiz bir çalışma yeri ... üç kısa slogan yaz.",
   "cevap": "1) Sessizliğin adresi. 2) Kahven, prizin, zamanın. ..."},
  {"soru": "Sessiz bir çalışma kafesinin logosu için hangi üç rengi önerirsin, neden?",
   "cevap": "Koyu yeşil, kırık beyaz, meşe tonu: ..."}
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
sonra cevaplarda kahve klişelerini sayıyoruz.

-----

## Bağlamı ölçmek

```python
KLISE = ["kahve", "fincan", "çekirdek", "aroma"]

def klise_say(cevaplar):
    toplam = 0
    for cevap in cevaplar:
        for kelime in KLISE:
            toplam = toplam + cevap.lower().count(kelime)
    return toplam

baglamsiz = []
baglamli = []
for _ in range(3):
    baglamsiz.append(modele_sor("Bir kafe için üç kısa slogan yaz.", hesap, anahtar))
    baglamli.append(modele_sor("Müşterilerinin sessiz bir çalışma yeri olarak anlattığı bir kafe için üç kısa slogan yaz.", hesap, anahtar))

print("Klişe — bağlamsız:", klise_say(baglamsiz), "/ bağlamlı:", klise_say(baglamli))
```

Tam hâli: `09_baglam_farki.py` (çalışma yeri kelimelerini de sayıyor).

-----

## Bulgu: soru yazmak da tasarım

Demo modundaki kayıtlı örnek cevaplarla:

| | kahve klişesi | çalışma yeri |
|---|---|---|
| bağlamsız | 11 | 0 |
| bağlamlı | 1 | 12 |

- Bulguyu söylemezsen model **ortalama bir kafeyi** anlatıyor
- Konu 1'de veriden bulduğumuz şey ancak soruya yazınca cevaba giriyor
- Model senin kafeni tanımıyor; soruyu yazmak bir **brief** yazmak gibi

Kendi anahtarınla dene: aynı örüntü çıkıyor mu?

-----

## Programın tamamı — yedi adım

| Adım | Ne yaptık | Elimizde ne oluştu |
|---|---|---|
| 1 | Anahtarı okuduk | `hesap`, `anahtar` |
| 2 | İsteği kurup gönderdik | `adres`, `basliklar`, `govde` → `yanit` |
| 3 | İçinden metni çektik | `metin` |
| 4 | Fonksiyona sardık | `modele_sor()` |
| 5 | Soru alıp dosyaya yazdık | `cevap.txt` |
| 6 | Döngüye soktuk | `cevaplar.json` |
| 7 | Bağlamın etkisini ölçtük | klişe sayımı |

Her adım bir öncekinin çıktısını kullandı.

-----

## En sık görülecek hata mesajları

| Mesaj | Anlamı |
|---|---|
| `KeyError: 'response'` | Bir kat atladın: `["result"]["response"]` |
| `TypeError: list indices must be integers...` | `errors` listesini adla açtın: `[0]` |
| `TypeError: 'NoneType' object is not subscriptable` | İstek başarısız; önce durum kodu |
| `FileNotFoundError: ... '...'` | Komutu konu klasörünün (`02-api-ile-konusmak`) dışından verdin |
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
önce ham hâlini bas.

**3. Anahtar koda yazılmaz.** Ayrı dosyada durur, teslime konmaz, ekranda
gösterilmez.

**4. Soruya yazdığın bağlam cevabı değiştirir.** Model senin bulgunu bilmez.

Sıradaki konu: **Konu 3 — makine öğrenmesi.** Sınıfın kendi etiketlediği
renklerle model eğiteceğiz.
