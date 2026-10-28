# Konu 10 — Zincirleme: Üretim Hattı

Bu not konunun özetidir; derste çalıştırdığımız `ders.ipynb` defteriyle **aynı sırada**
ilerler: Isınma, sonra Adım 1–7 ve kısa bir Bonus. Derste kaçırdığın bir yer olursa
buradan oku, sonra defterde o adımın hücrelerini çalıştır. Nottaki kod blokları
defterdeki hücrelerin birebir aynısı.

**Şimdiye kadar:** her iş ayrı bir defterdi: Konu 5'te slogan, Konu 8'de koddan ve toplu olarak görsel.
**Bu konuda:** ikisini tek bir **hatta** bağlıyoruz:

> `ayarlar.json`'daki brif → metin modeliyle sloganlar → görsel modeliyle her slogana bir görsel.
> Bir halkanın çıktısı, sıradaki halkanın girdisi. Biten halka yeniden çalışmaz, kopan halka hattı durdurmaz, her şey kayda geçer.

**Konunun sonunda elinde:** `ciktilar/kafe_afisi_1/` klasöründe üç slogan (`sloganlar.json`), her slogana bir görsel
(`gorsel_1.jpg` ...) ve hattın üretim günlüğü (`uretim.json`). Bonus'u da yaparsan ikisini yan yana gösteren bir pano (`pano.png`).

**Kurulum:** yeni kütüphane yok. `git pull` ile konu klasörü geldikten sonra `gita3111` klasöründe bir kez `uv sync` çalıştır.

**Anahtar:** Isınma, Adım 1 ve Adım 2 anahtarsız. Adım 3'ten sonrası `anahtar.txt` ister (Konu 2'deki dosya, `gita3111`
klasöründe). Defterin tamamı 4 metin ve 3 görsel isteği gönderir (Bonus 2 ile 4 görsel); Adım 6'da bilerek
reddedilen 3 görsel isteği de var. Hepsi ücretsiz günlük kotanın küçük bir kısmı.

> **Bu nottaki çıktılar hakkında.** Isınma, Adım 1 ve 2'nin çıktıları her bilgisayarda aynıdır. Sloganlar ve görseller gerçek
> modellerden gelir; senin ekranında farklı olur. Notta onların yerinde `...` var.

---

## Isınma: hat kâğıt üstünde

Önce sahte halkalarla: üç küçük fonksiyon, hiçbiri internete çıkmıyor.

```python
def slogan_yaz(konu):
    return konu + ": burada zaman yavaşlar"

def yonerge_kur(slogan, stil):
    return stil + " poster, idea: " + slogan

def gorsel_ciz(yonerge):
    return "[görsel] " + yonerge
```

Bu hücre bir şey yazmaz; fonksiyonları yalnızca tanımlar. Şimdi zinciri kuruyoruz:

```python
konu = "sessiz bir çalışma kafesi"
slogan = slogan_yaz(konu)
yonerge = yonerge_kur(slogan, "risograph")
gorsel = gorsel_ciz(yonerge)

print(slogan)
print(yonerge)
print(gorsel)
```

Çıktı:

```
sessiz bir çalışma kafesi: burada zaman yavaşlar
risograph poster, idea: sessiz bir çalışma kafesi: burada zaman yavaşlar
[görsel] risograph poster, idea: sessiz bir çalışma kafesi: burada zaman yavaşlar
```

Her satır bir öncekinin sonucunu alıyor: `slogan_yaz`'ın çıktısı `yonerge_kur`'un girdisi, onun çıktısı `gorsel_ciz`'in girdisi.
**Hat** (pipeline) budur.

**Tahmin et:** ilk satırdaki konuyu `"gece açık bir kitapçı"` yapıp yeniden çalıştırırsan üç satırdan kaçı değişir? Defterde
sıradaki hücre üsttekinin kopyası; yalnızca ilk satırı farklı:

```python
konu = "gece açık bir kitapçı"
slogan = slogan_yaz(konu)
yonerge = yonerge_kur(slogan, "risograph")
gorsel = gorsel_ciz(yonerge)

print(slogan)
print(yonerge)
print(gorsel)
```

Çıktı:

```
gece açık bir kitapçı: burada zaman yavaşlar
risograph poster, idea: gece açık bir kitapçı: burada zaman yavaşlar
[görsel] risograph poster, idea: gece açık bir kitapçı: burada zaman yavaşlar
```

- Üç satırın üçü de değişti. Hattın başındaki tek girdi sonuna kadar taşınır: başta yanlış bir kelime, sonda yanlış bir görsel.
  Bu yüzden hattın en önemli satırı brif.
- Gerçek hatta her halka bir istek. Aşağıda sahte halkaları gerçek modellerle değiştiriyoruz.

---

## Adım 1 — Ayarlar dosyası: `ayarlar.json`

Konu klasöründe `ayarlar.json` diye bir dosya var:

```json
{
  "calisma": "kafe_afisi_1",
  "konu": "sessiz bir çalışma kafesi",
  "stil": "risograph print poster, two colors",
  "slogan_sayisi": 3,
  "sicaklik": 0.9,
  "tohum": 42
}
```

Bu bir **yapılandırma dosyası** (config): hattın bütün ayarları koddan ayrı, tek yerde. Müşteri ya da konu değişince kodu değil
bu dosyayı değiştiririz. Biçimi JSON: tek katmanlı bir sözlük.

```python
import json

with open("ayarlar.json", encoding="utf-8") as dosya:
    ayarlar = json.load(dosya)

print(ayarlar)
```

- `json.load`, Konu 8'deki `json.dump`'ın tersi: dosyayı okuyup Python sözlüğüne çevirir. Konu 9'da video günlüğünü geri
  okurken de bunu kullandık.
- JSON titizdir: metinler **çift tırnak** içinde, sayılar tırnaksız, ayarlar arasında virgül var, son satırdan sonra virgül yok.
  Bir kural bozulursa `json.load` hata verir (bkz. sık hatalar).

Her ayarı bir değişkene alıyoruz:

```python
calisma = ayarlar["calisma"]
konu = ayarlar["konu"]
stil = ayarlar["stil"]
slogan_sayisi = ayarlar["slogan_sayisi"]
sicaklik = ayarlar["sicaklik"]
tohum = ayarlar["tohum"]

print(konu, "/", stil)
```

Çıktı: `sessiz bir çalışma kafesi / risograph print poster, two colors`.

- Aşağıdaki hücreler bu kısa adları kullanıyor (`konu`, `stil`, `tohum`...).
- `konu` Türkçe (Türkçe slogan sorusuna gidecek), `stil` İngilizce (görsel yönergesine gidecek; Konu 7).
- `ayarlar.json`'u değiştirirsen bu iki hücreyi yeniden çalıştır; yoksa değişkenler eski değerleri taşır.

---

## Adım 2 — Çalışma klasörü

```python
import os

klasor = "ciktilar/" + calisma + "/"
os.makedirs(klasor, exist_ok=True)
print(klasor)
```

Çıktı: `ciktilar/kafe_afisi_1/`.

- Hattın bütün çıktıları tek bir klasöre gidiyor: `ciktilar/` içinde, adı `ayarlar.json`'daki `calisma` alanından gelen bir klasör.
- Yol düz bir metin, Konu 8'deki `klasor = "izgara/"` gibi. Sondaki `/` sayesinde dosya adını doğrudan ekleyebiliriz:
  `klasor + "sloganlar.json"` → `ciktilar/kafe_afisi_1/sloganlar.json`.
- `os.makedirs(klasor, exist_ok=True)`: klasörü açar; `ciktilar/` henüz yoksa onu da. `exist_ok=True`: klasör zaten varsa
  hata verme. `os` Python'un içinde geliyor; Konu 8'deki `os.path.exists` da onun.
- Konu 8'de klasörü `sabirli_ciz` kendisi açıyordu. Bu hatta ilk yazılan dosya bir görsel değil, sloganlar (`sloganlar.json`);
  o yüzden klasörü baştan biz açıyoruz.

**Neden klasör adında otomatik tarih yok?** Klasöre her çalıştırmada o anın tarihini ve saatini eklesek her seferinde yeni bir
klasör açılırdı; içinde hiçbir şey "zaten var" olmazdı ve hat her şeyi baştan üretirdi. Kural Konu 8'deki gibi: **aynı iş, aynı ad**.

| Klasör adı | Ne olur |
|---|---|
| Kodda otomatik tarih (`2026-11-04_18-57-25`) | Her çalıştırma yeni klasör; her şey yeniden üretilir, kota gider |
| `ayarlar.json`'da senin verdiğin ad (`kafe_afisi_1`) | Aynı brif aynı klasör; biten atlanır, kaldığı yerden devam |

Tarihli bir arşiv istiyorsan tarihi adın içine **sen** yaz: `"calisma": "2026-11-04_kafe"`. Brifi değiştirdiğinde (konu, stil,
tohum) `calisma` adını da değiştir: yeni brif yeni klasörde başlar, eskisi olduğu gibi kalır. Program yalnızca klasörün adına
bakar; adda olmayan bir şeyi değiştirirsen bunun yeni bir iş olduğunu bilemez.

---

## Adım 3 — Hazır halkalar

```python
from halkalar import modele_sor, sabirli_ciz
```

`halkalar.py` bu klasördeki yardımcı dosya. Önceki konulardan iki fonksiyon içinde hazır:

| Fonksiyon | Nereden | Ne yapar | Başarısızsa |
|---|---|---|---|
| `modele_sor(soru, sicaklik)` | Konu 5 | Metin modeline (`llama-3.3-70b`) sorar, cevabı metin olarak verir | `None` (Konu 5'tekinden tek farkı: çökmez) |
| `sabirli_ciz(yonerge, tohum, yol)` | Konu 8 | Görsel modeline (`flux-1-schnell`) en fazla üç kez dener, görseli `yol`a kaydeder ve `yol`u verir | `None` (dosya oluşmaz) |

`halkalar.py` anahtarı `../anahtar.txt`'den kendisi okur: bu hücre ilk çalıştığında. Hücre bir şey yazmaz; dosya yoksa
`FileNotFoundError: ... '../anahtar.txt'` verir. `anahtar.txt`'yi sonradan düzeltirsen çekirdeği yeniden
başlat (**Restart**). Halkalar hazır; onları **birbirine bağlamak** bugün senin işin.

Konu 5'teki slogan sorusunu bir kalıba çeviriyoruz: sabit kısım ve sonunda brifteki konu. Önce tek bir istek:

```python
soru = "Şu konu için tek bir kısa slogan yaz. Yalnızca sloganı yaz, açıklama ekleme: " + konu

cevap = modele_sor(soru, sicaklik)
print(cevap)
```

Çıktı: modelin cevabı (`...`). Model talimata her zaman uymaz: sloganı tırnak içine alabilir, başına `Slogan:` yazabilir,
sonuna bir açıklama ekleyebilir. Bu cevap bir sonraki halkaya (görsel yönergesine) gidecek; önce temizliyoruz:

```python
temiz = cevap.strip()
temiz = temiz.replace('"', "")
print(temiz)
```

- `.strip()`: baştaki ve sondaki boşlukları (satır sonları dahil) siler. Konu 2'de anahtar dosyasının satırlarını temizlerken kullandık.
- `.replace('"', "")`: düz tırnakları hiçle değiştirir, yani siler (Konu 1'de metni temizlerken kullandık). Tırnak işaretinin
  kendisini tek tırnak içine yazıyoruz: `'"'`.
- Model kıvrık tırnak (`“ ”`) ya da `Slogan:` yazdıysa aynı satırı o işaretle bir kez daha yaz:
  `temiz = temiz.replace("Slogan: ", "")`. Adım 4'teki fonksiyonda aynı temizleme satırları var; eklediğin satırı oraya da
  ekle (orada değişkenin adı `slogan`).
- Modelin cevabı Cloudflare'de varsayılan olarak 256 belirteçle (token) sınırlı. Slogana fazlasıyla yeter; ama modelden uzun bir
  metin istersen cevap yarıda kesilir.
- `cevap` `None` ise (istek başarısız) `.strip()` hata verir: `AttributeError: 'NoneType' object has no attribute 'strip'`.
  Üstteki `İstek başarısız` satırına bak.

---

## Adım 4 — 1. halka: sloganlar (ara çıktıyı sakla)

Bir halkanın sonucu hattın **ara çıktısı**. Sloganları bir dosyada saklıyoruz: `sloganlar.json`.

```python
slogan_dosyasi = klasor + "sloganlar.json"

def slogan_halkasi():
    if os.path.exists(slogan_dosyasi):
        with open(slogan_dosyasi, encoding="utf-8") as dosya:
            sloganlar = json.load(dosya)
        print("Dosyadan okundu, istek gitmedi")
        return sloganlar
    sloganlar = []
    for tur in range(slogan_sayisi):
        cevap = modele_sor(soru, sicaklik)
        if cevap is None:
            print("Slogan gelmedi, atlıyorum")
            continue
        slogan = cevap.strip()
        slogan = slogan.replace('"', "")
        sloganlar.append(slogan)
    with open(slogan_dosyasi, "w", encoding="utf-8") as dosya:
        json.dump(sloganlar, dosya, ensure_ascii=False, indent=2)
    print("Üretildi ve kaydedildi")
    return sloganlar
```

Fonksiyon her çağrıldığında önce sorar: **zaten var mı?**

- Dosya varsa (`os.path.exists(slogan_dosyasi)`, Konu 8): `json.load` ile oku, ver. Modele hiç istek gitmez; `return`
  fonksiyonu orada bitirir.
- Yoksa: `slogan_sayisi` kez sor. `range(slogan_sayisi)` = "3 kez" (`slogan_sayisi` 3). Her cevabı temizle, listeye ekle; sonunda
  listeyi dosyaya yaz ve ver.
- Bir cevap gelmezse (`None`) o turu atla (`continue`): hat durmaz, liste bir eksik olur.
- Dosyaya yazmak Konu 8'deki günlükle aynı: `json.dump(..., ensure_ascii=False, indent=2)`. Önce yazılacak şey, sonra dosya.
- Fonksiyon `slogan_dosyasi`, `soru`, `sicaklik` ve `slogan_sayisi`'yı yukarıdaki hücrelerden alıyor.
- Hücre yalnızca fonksiyonu tanımlar; istekler fonksiyonu çağırınca gider. Adım 3'teki deneme sloganı listeye girmez:
  fonksiyon üç yeni istek gönderir.

```python
sloganlar = slogan_halkasi()
print(sloganlar)
```

Çıktı: `Üretildi ve kaydedildi` ve üç slogan (`[...]`). Üç istek gitti. Aynı çağrı bir kez daha:

```python
sloganlar = slogan_halkasi()
print(sloganlar)
```

Çıktı: `Dosyadan okundu, istek gitmedi` ve **aynı** üç slogan. Hiç istek gitmedi.

Yalnızca kota için değil, **tutarlılık** için de saklıyoruz. Sıcaklık 0.9; her istekte başka bir slogan gelir (Konu 5). Sloganları her
çalıştırmada yeniden üretseydik `gorsel_1.jpg` dünkü sloganla üretilmiş olurdu, günlükte ise bugünkü slogan yazardı: görsel ile
metin birbirini tutmazdı.

> **Kural:** pahalı ya da her seferinde farklı çıkan ara çıktıyı sakla. Ucuz ve her seferinde aynı çıkanı (Adım 5'teki
> yönergeler gibi) yeniden kur.

Bir dikkat: üç istekten biri başarısız olursa dosyaya iki slogan, üçü de başarısız olursa (ör. anahtar yanlış) boş bir liste
(`[]`) yazılır; sonraki çalıştırmalar dosyadakiyle devam eder. Sorunu düzelttikten sonra `sloganlar.json`'u sil, hücreyi
yeniden çalıştır.

---

## Adım 5 — 2. halka: her slogana bir görsel

Önce her slogan için görsel yönergesini kuruyoruz:

```python
yonergeler = []
for slogan in sloganlar:
    yonerge = stil + ", a poster illustration that expresses this idea: " + slogan + ", no text, no letters"
    yonergeler.append(yonerge)
    print(yonerge)
```

Çıktı: üç yönerge, her biri `risograph print poster, two colors, a poster illustration that expresses this idea: ...,
no text, no letters` biçiminde.

- Bu bir kalıp: sabit kısım ve iki değişen yer (`stil`, `slogan`).
- Yönergeleri saklamıyoruz: sloganlardan ve ayarlardan her seferinde aynı biçimde, bedavaya kurulur.
- Sloganlar Türkçe, yönergenin geri kalanı İngilizce. Görsel model çoğunlukla İngilizce metinle eğitildi (Konu 7); Türkçe
  sloganın fikrini ne kadar anladığı görsellerde görülür.
- **"no text, no letters"** bilerek orada: tipografiyi modele bırakmıyoruz. Görsel modeller harfleri çoğu zaman bozar; sloganı
  afişe tasarımcı dizer. Hat **taslak** üretir; son biçim tasarımcının.

Görsel halkası tek bir görsel için çalışan bir fonksiyon:

```python
def gorsel_halkasi(sira, yonerge):
    yol = klasor + "gorsel_" + str(sira) + ".jpg"
    kayit = {"halka": "gorsel", "girdi": yonerge, "cikti": yol}
    if os.path.exists(yol):
        kayit["durum"] = "uretildi"
        print("Zaten var, atlıyorum:", yol)
        return kayit
    sonuc = sabirli_ciz(yonerge, tohum, yol)
    if sonuc is None:
        kayit["durum"] = "olmadi"
        print("Olmadı, atlıyorum:", yol)
        return kayit
    kayit["durum"] = "uretildi"
    print("Kaydedildi:", yol)
    return kayit
```

- Slogan halkasıyla **aynı kalıp**: zaten var mı? Varsa onu ver. Yoksa üret, sakla, ver.
- `yol = klasor + "gorsel_" + str(sira) + ".jpg"`: `str` sayıyı metne çevirir (Konu 5); metne yalnızca metin eklenebilir.
  `sira` 1 ise yol `ciktilar/kafe_afisi_1/gorsel_1.jpg`.
- `os.path.exists(yol)`: bu dosya var mı? Varsa atla. Atlanan görselin durumu da `uretildi`: dosya orada.
- `sabirli_ciz(yonerge, tohum, yol)` görseli `yol`a kendisi kaydeder. Başarılıysa `yol`u, olmazsa `None` verir; halka bu dönüşe
  bakıp kaydın durumunu yazıyor.
- Her yoldan bir **kayıt** (sözlük) çıkıyor: hangi halka (`halka`), ne girdi (`girdi`: yönerge), hangi dosya çıktı (`cikti`),
  sonuç ne (`durum`: `uretildi` ya da `olmadi`).
- `kayit["durum"] = ...`: sözlüğe yeni bir anahtar ve değer ekler.
- `return kayit` fonksiyonu orada bitirir; hangi yoldan çıkarsa çıksın elimize bir kayıt gelir.

Halkayı bir döngüyle her yönergeye uyguluyoruz:

```python
kayitlar = []
sira = 0
for yonerge in yonergeler:
    sira = sira + 1
    kayit = gorsel_halkasi(sira, yonerge)
    kayitlar.append(kayit)

print(len(kayitlar), "kayıt")
```

Çıktı: üç kez `Kaydedildi: ciktilar/kafe_afisi_1/gorsel_1.jpg` (... `_2`, `_3`) ve `3 kayıt`.

- Her yönerge görsel halkasına gidiyor; gelen kayıt `kayitlar` listesine ekleniyor.
- `sira` her turun **başında** bir artıyor: ilk görsel `gorsel_1.jpg`. Sayaç başta arttığı için turun ortasında bir şey
  atlansa bile sıra kaymaz.
- Hücreyi yeniden çalıştırırsan üçü de `Zaten var, atlıyorum` der; istek gitmez.
- Üç görsel bir dakika kadar sürer.

Görsellere bak: görselde yine de yazı çıktı mı, harfler okunuyor mu? Görseller sloganların **fikrini** mi taşıyor, yoksa yalnızca
stili mi?

---

## Adım 6 — Bir halka koparsa hat durmasın

Gerçek bir hatta bir halka er geç kopar: internet gider, kota biter, bir yönerge reddedilir. Derste bunu beklemek yerine bilerek
koparıyoruz: dördüncü görseli **boş bir yönergeyle** istiyoruz.

```python
kayit = gorsel_halkasi(4, "")
kayitlar.append(kayit)

print(kayit)
print(len(kayitlar), "kayıt")
```

Çıktı:

```
İstek başarısız, durum kodu: 400
Deneme 1 olmadı, 5 saniye bekliyorum
İstek başarısız, durum kodu: 400
Deneme 2 olmadı, 5 saniye bekliyorum
İstek başarısız, durum kodu: 400
Olmadı, atlıyorum: ciktilar/kafe_afisi_1/gorsel_4.jpg
{'halka': 'gorsel', 'girdi': '', 'cikti': 'ciktilar/kafe_afisi_1/gorsel_4.jpg', 'durum': 'olmadi'}
4 kayıt
```

- Görsel model boş yönergeyi kabul etmez: durum kodu 400 ("istek bozuk", Konu 2). `sabirli_ciz` üç kez dener; kalıcı
  bir hatada beklemek işe yaramaz ama basit bir program bunu ayırt edemez.
- Hücre **çökmedi**: `gorsel_halkasi` hata yerine `"durum": "olmadi"` yazan bir kayıt verdi. Bir döngünün içinde olsaydık döngü
  sıradaki görsele geçerdi.
- Hat iki şeyi birlikte yapıyor: kopan halkayı **kayda geçiriyor** (hangi görsel, `durum`: `olmadi`) ve kopmayanlarla **devam ediyor**.
- `gorsel_4.jpg` hiç oluşmadı; hattı yarın yeniden çalıştırırsan yalnızca o denenir (kaldığı yerden devam).
- Bu hücreyi iki kez çalıştırırsan aynı kayıt listeye iki kez girer (`5 kayıt`). Adım 5'in döngü hücresinden yeniden başla:
  liste sıfırlanır, görseller zaten var, istek gitmez.

| Kopan halka hattı durdurursa | Kopan halka kayda geçerse |
|---|---|
| Üçüncü görselde internet gitti: dördüncü ve beşinci hiç denenmedi | Üçüncü `olmadi` diye kaydedildi; dördüncü ve beşinci üretildi |
| Neyin eksik olduğunu bulmak için klasöre tek tek bakarsın | Eksikler günlükte yazıyor |
| Baştan çalıştırırsın | Yeniden çalıştırınca yalnızca eksik olan denenir |

---

## Adım 7 — Üretim günlüğü: `uretim.json`

```python
gunluk = {"ayarlar": ayarlar, "sloganlar": sloganlar, "kayitlar": kayitlar}

with open(klasor + "uretim.json", "w", encoding="utf-8") as dosya:
    json.dump(gunluk, dosya, ensure_ascii=False, indent=2)

print("Günlük yazıldı:", len(kayitlar), "kayıt")
```

Çıktı: `Günlük yazıldı: 4 kayıt`.

- `gunluk` bir sözlük, içinde üç bölüm: hangi ayarlarla çalıştı (`ayarlar`), hangi sloganlar çıktı (`sloganlar`), her görselin
  sonucu ne (`kayitlar`).
- `klasor + "uretim.json"`: günlük, çıktıların yanında, aynı klasörde. Her brifin günlüğü kendi klasöründe.
- `durum`u `olmadi` olan kayıtlar eksiklerin listesi: hattı yeniden çalıştırınca denenecek olanlar. Program da günlüğü geri okuyup
  onları bulabilir; alıştırmanın 6. sorusunda sen sayacaksın.
- Final projesinin teslimindeki **üretim günlüğü** bu dosya: hangi brif, hangi model ayarı, ne çıktı, ne eksik kaldı.

**Defteri yarın baştan çalıştırırsan ne görürsün?**

| Adım | İkinci çalıştırmada ekranda | İstek |
|---|---|---|
| 3 | Yeni bir deneme sloganı | 1 metin |
| 4 | İki çağrıda da `Dosyadan okundu, istek gitmedi`, aynı üç slogan | 0 |
| 5 | Üç kez `Zaten var, atlıyorum` | 0 |
| 6 | Yine üç kez `400` ve `olmadi`: `gorsel_4.jpg` hiç oluşmadığı için her seferinde denenir | 3 (reddedilen) |
| 7 | `Günlük yazıldı: 4 kayıt` | 0 |

Hat kaldığı yerden devam ediyor: biten iş yeniden üretilmiyor, yalnızca eksik olan deneniyor.

---

## Bonus

**1. Pano: slogan ve görsel yan yana.** Konu 8'deki kontak sayfası, bu kez tek satır:

```python
import matplotlib.pyplot as plt

sutun = len(sloganlar)

plt.figure(figsize=(12, 5))
sira = 0
for slogan in sloganlar:
    sira = sira + 1
    yol = klasor + "gorsel_" + str(sira) + ".jpg"
    plt.subplot(1, sutun, sira)
    if os.path.exists(yol):
        resim = plt.imread(yol)
        plt.imshow(resim)
    plt.title(slogan, fontsize=9)
    plt.axis("off")

plt.savefig(klasor + "pano.png", bbox_inches="tight")
plt.show()
```

- `plt.subplot(1, sutun, sira)`: 1 satır, `sutun` sütun, `sira`'ncı kutu (Konu 6 ve 8).
- `plt.imread` görseli dosyadan okur, `plt.imshow` kutuya koyar; dosya yoksa kutu boş kalır.
- `plt.title(slogan, ...)`: her kutunun üstünde onu doğuran slogan.
- Pano da çalışma klasörüne kaydediliyor: `pano.png`.
- Döngü sloganları geziyor; Adım 6'daki dördüncü kayıt panoda yok (sloganı yoktu).

**Tartış:** hangi slogan hangi görselle güçlü? Slogan ile görselin **aynı şeyi söylediği** kutu mu daha iyi, yoksa birbirini
**tamamladığı** kutu mu (görsel bir şey gösteriyor, slogan ona yeni bir anlam ekliyor)? Afişte metin ile görselin ilişkisi
tasarımcının asıl işi; hat bunu senin yerine düşünmez.

**2. Ara çıktıya elle dokun.** Ara çıktıyı saklamanın bir faydası daha var: hattın ortasında araya girebilirsin.

1. `ciktilar/kafe_afisi_1/sloganlar.json`'u VS Code'da aç, ikinci sloganı kendi yazdığın bir sloganla değiştir, kaydet.
   Tırnakları ve virgülleri bırak; JSON biçimi bozulmasın.
2. Aynı klasördeki `gorsel_2.jpg`'yi sil.
3. Adım 4'ün ilk çağrı hücresinden Adım 5'in sonuna kadar sırayla yeniden çalıştır, sonra Adım 7'nin günlük hücresini ve panoyu.

Slogan halkası dosyadan okur (senin sloganınla, istek gitmez). Görsel halkası 1 ve 3'ü atlar, yalnızca 2'yi üretir: tek istek.
Panoda yalnızca bir kutu değişir. Hat makinenin işini yapıyor; sen istediğin yerde araya girip yönünü değiştiriyorsun.

---

## Defterin bölümleri

| Adım | Ne yaptık | Elimizde ne oluştu | Anahtar |
|---|---|---|---|
| Isınma | Sahte halkalarla zincir; konuyu değiştirmek | — | gerekmez |
| 1 | Ayarlar dosyasını okuduk | `ayarlar`, `konu`, `stil`, `tohum` ... | gerekmez |
| 2 | Çalışma klasörü | `klasor` (`ciktilar/kafe_afisi_1/`) | gerekmez |
| 3 | Hazır halkalar; bir deneme sloganı, temizleme | `modele_sor`, `sabirli_ciz`, `soru` | gerekir |
| 4 | 1. halka: sloganlar; ara çıktıyı sakla | `slogan_halkasi`, `sloganlar`, `sloganlar.json` | gerekir |
| 5 | 2. halka: yönergeler ve görseller | `yonergeler`, `gorsel_halkasi`, `kayitlar`, `gorsel_1.jpg` ... | gerekir |
| 6 | Bir halkayı bilerek kopardık | `olmadi` durumlu bir kayıt | gerekir |
| 7 | Üretim günlüğü | `uretim.json` | istek yok; Adım 4–6 gerekir |
| Bonus | Pano; ara çıktıya elle dokunmak | `pano.png` | 2. bölüm gerekir |

Derste kendi başına çalışacağın defter: `alistirma.ipynb`. Önce aynı klasörde yeni bir adla kopyala, kopyada çalış.
**Anahtar istemez ve internete çıkmaz:** halkalar sahte ve her çağrıyı sayıyor; kaç istek gittiğini görebiliyorsun.

- **Yaz** (en sonda; derste önce bunu çöz): ara çıktıyı (sloganları) kendin saklamak. Bu konuda kendi elinle yazdığın kod.
- **Bozuk kodlar:** beş kısa hücre, birbirinden bağımsız. İkisi hata mesajı veriyor, üçü sessizce yanlış sonuç yazıyor.
- **Kendi başına:** `BOSLUK` yazan yerleri doldurduğun altı soru.

---

## Sık karşılaşılan hatalar ve mesajlarını okumak

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `FileNotFoundError: ... 'ayarlar.json'` (Adım 1) | Defterin kopyası konu klasörünün dışında ya da dosya adı farklı | Kopya `ayarlar.json`'un yanında, `10-uretim-hatti` klasöründe olmalı |
| `JSONDecodeError: Expecting value ...` | `ayarlar.json`'da bir metin tırnaksız ya da tek tırnakla yazılmış | Metinler çift tırnak içinde: `"konu": "gece açık bir kitapçı"` |
| `JSONDecodeError: Illegal trailing comma before end of object ...` | Son satırdan sonra virgül kalmış | Son ayarın sonundaki virgülü sil |
| `JSONDecodeError: Expecting ',' delimiter ...` | İki satır arasında virgül eksik | Her ayarın sonuna (sonuncusu hariç) virgül |
| `KeyError: 'Konu'` ya da `KeyError: 'tohum'` | Ayar adı dosyadakinden farklı (büyük harf, eksik satır) | Adı dosyadakiyle birebir yaz; kendi ayarlar dosyanda bütün satırlar olmalı |
| `NameError: name 'modele_sor' is not defined` (ya da `'sabirli_ciz'`) | Adım 3'ün import hücresi hata verdi (çoğunlukla anahtar dosyası) ya da çalıştırılmadı | Önce o hücredeki hatayı düzelt, sonra sırayla devam et |
| `ModuleNotFoundError: No module named 'halkalar'` | Defterin kopyası konu klasörünün dışında | Kopya `halkalar.py`'nin yanında olmalı |
| `FileNotFoundError: ... '../anahtar.txt'` (Adım 3) | Anahtar dosyası yok ya da yanlış yerde | `gita3111` klasöründe durmalı; sonra Adım 3'ün ilk hücresini yeniden çalıştır |
| `İstek başarısız, durum kodu: 401` | Anahtar yanlış | `anahtar.txt`'yi düzelt, çekirdeği yeniden başlat (**Restart**), baştan çalıştır |
| `AttributeError: 'NoneType' object has no attribute 'strip'` (Adım 3) | Deneme isteği başarısız oldu, `cevap` `None` | Üstteki `İstek başarısız` ya da `Bağlanamadım` satırına bak |
| `Slogan gelmedi, atlıyorum` | Bir metin isteği başarısız oldu | Hat iki sloganla devam eder. Üçünü istiyorsan `sloganlar.json`'u sil, yeniden çalıştır |
| `sloganlar` boş liste: `[]` | Bütün metin istekleri başarısız oldu ve boş liste dosyaya yazıldı | Sorunu düzelt (anahtar, internet), `sloganlar.json`'u sil, yeniden çalıştır |
| Hep `Dosyadan okundu`, sloganlar eski konudan | `ayarlar.json`'da konuyu değiştirdin ama `calisma` aynı kaldı | Yeni brif için `calisma` adını da değiştir |
| `JSONDecodeError` (Adım 4, Bonus 2 sonrası) | `sloganlar.json`'u elle düzeltirken bir tırnak ya da virgül silindi | Dosyayı düzelt: `["...", "...", "..."]` biçiminde olmalı |
| Görsel eski sloganı anlatıyor | Sloganı değiştirdin ama görseli silmedin | O görseli sil; görsel halkası yalnızca olmayanı üretir |
| `TypeError: can only concatenate str (not "int") to str` | Yolu kurarken sayı metne çevrilmedi: `"gorsel_" + sira` | `"gorsel_" + str(sira) + ".jpg"` |
| `İstek başarısız, durum kodu: 400` (Adım 6) | Boş yönerge; bilerek | Doğru davranış: kayıtta `olmadi` |
| `İstek başarısız, durum kodu: 429` ve `Deneme ... olmadı` | Çok hızlı istek ya da günlük kota doldu | Bekle; üst üste geliyorsa hücreyi durdur (**Interrupt**). Kota yenilenince aynı hücreyi yeniden çalıştır; kaldığı yerden devam eder |
| `NameError: name 'klasor' is not defined` | Adım 2 çalıştırılmadı | Sırayla çalıştır |
| `NameError: name 'slogan_halkasi' is not defined` ya da `'gorsel_halkasi'` | Fonksiyonun tanımlandığı hücre atlandı | O hücreyi çalıştır |
| Panoda boş kutu | O görsel üretilemedi | Kayıtta `olmadi` yazar; Adım 5'in döngü hücresini, sonra panoyu yeniden çalıştır |

---

## Kendini dene

Cevaplar notun en sonunda. Önce kendin düşün.

1. Bir arkadaşın çalışma klasörünü `ayarlar.json`'dan değil, o anki tarih ve saatle kurdu. Hattı üç kez çalıştırınca ne olur?
2. Yönergeleri neden saklamadık da sloganları sakladık?
3. `ayarlar.json`'da konuyu "gece açık bir kitapçı" yaptın, kaydettin ve bütün defteri yeniden çalıştırdın; `calisma` adını
   değiştirmedin. Ne görürsün?
4. Görsel halkası kopunca hata verip dursaydı (`return` yerine program çökseydi), beş görsellik bir hatta üçüncü görselde
   internet gidince ne olurdu?
5. Görsel yönergesinde neden "no text, no letters" yazıyoruz? Slogan afişe nasıl girecek?
6. `gorsel_halkasi` neden `sabirli_ciz`'in verdiği sonuca (`sonuc`) bakıyor? Bakmasaydı günlükte ne yanlış olurdu?
7. Final projende hattın kaç halkası olur? Hangi halkanın çıktısını mutlaka saklarsın?

---

## Bu konuda öğrendiklerin

- **Hat.** Bir halkanın çıktısı sıradakinin girdisi; hattın başındaki brif sonuna kadar taşınır.
- **Yapılandırma dosyası.** Ayarlar koddan ayrı, `ayarlar.json`'da; brif değişince kod değişmez.
- **Çalışma klasörü.** Adı ayarlardan gelir; aynı brif aynı klasör, yeni brif yeni klasör.
- **Ara çıktıyı saklamak.** Pahalı ya da her seferinde farklı çıkanı sakla; ucuz ve aynı çıkanı yeniden kur.
- **Her halka aynı kalıp.** Zaten var mı? Varsa onu ver. Yoksa üret, sakla, ver.
- **Kopan halka.** Hattı durdurmaz; kayda `olmadi` diye geçer, sonraki çalıştırmada yalnızca o denenir.
- **Üretim günlüğü.** `uretim.json`: ayarlar, ara çıktılar ve her işin sonucu bir arada.
- **İnsan döngüde.** Hat taslak üretir; slogan seçimi, tipografi ve son karar tasarımcının.

## Bu konunun tek cümlesi

> Bir ayarlar dosyasıyla çalışan hat, halkaları birbirine bağlar; biteni yeniden üretmez, kopanı kayda geçirip devam eder ve
> her şeyi tek bir klasörde, üretim günlüğüyle birlikte bırakır.

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **Hat (pipeline)** | Bir adımın çıktısının bir sonrakinin girdisi olduğu adımlar dizisi |
| **Halka** | Hattın bir adımı: slogan, görsel |
| **Ara çıktı** | Bir halkanın ürettiği, sıradaki halkaya giden sonuç (ör. `sloganlar.json`) |
| **Yapılandırma dosyası (config)** | Programın ayarlarını koddan ayrı tutan dosya (`ayarlar.json`) |
| **Çalışma klasörü** | Bir brifin bütün çıktılarının toplandığı klasör |
| **Kayıt** | Bir işin girdisi, çıktısı ve sonucu (bir sözlük) |
| **Üretim günlüğü** | Hattın ayarlarını, ara çıktılarını ve bütün kayıtlarını tutan dosya (`uretim.json`) |
| **`.strip()` / `.replace(a, b)`** | Baştaki ve sondaki boşlukları silmek / metindeki `a`'ları `b` ile değiştirmek |
| **`os.makedirs(klasor, exist_ok=True)`** | Klasörü (gerekirse üst klasörüyle birlikte) açmak; zaten varsa hata vermemek |
| **`os.path.exists(yol)`** | "Bu yolda bir dosya var mı?" sorusu: `True` ya da `False` (Konu 8) |

## Ödev

`odevler/odev10.md` (puansız): kendi projenin hat iskeleti. Kendi ayarlar dosyan, iki halka çalışıyor (metin ve görsel),
panosu ve üretim günlüğü. Güzel olması gerekmiyor; final projesinin ilk taslağı.

## Sonraki konu

Bu hatta adımların sırasını sen belirledin. Konu 11'de modele bilmediği bir belgeyi okutacağız, Konu 12'de sırayı model belirleyecek.

---

## Kendini dene — cevaplar

1. Her çalıştırmada yeni bir klasör açılır; içinde hiçbir şey "zaten var" olmaz. Üç çalıştırmada 9 slogan, 9 görsel üretilir:
   kota üç kat harcanır ve her klasörde başka sloganlar olur. Kaldığı yerden devam için klasörün adı kararlı olmalı.
2. Yönerge sloganlardan ve ayarlardan her seferinde aynı biçimde, bedavaya kurulur. Slogan ise hem istek harcar hem her
   seferinde farklı çıkar (sıcaklık); yeniden üretilirse görsellerle uyuşmaz.
3. `Dosyadan okundu` ve eski (kafe) sloganlar; görseller de `Zaten var`. Program klasör adına bakıyor, konuya değil. Yeni brif için
   `calisma` adını değiştir.
4. Dördüncü ve beşinci görsel hiç denenmezdi; neyin eksik olduğunu klasöre bakarak bulman gerekirdi. Kopan halka kayda geçince
   hat devam eder ve eksik günlükte yazar.
5. Görsel modeller harfleri çoğu zaman bozar ve yazının yerine, biçimine tasarımcı karar vermeli. Slogan afişe tasarımcının
   elinde (bir tasarım programında) dizilir; hat görseli ve sloganı taslak olarak hazırlar.
6. `None` "görsel üretilemedi, dosya yok" demek. Halka buna bakmasaydı her kayda `uretildi` yazardı: günlük, olmayan bir dosyayı
   var gösterirdi ve eksikleri günlükten bulamazdın. Hata çıkmaması her şeyin yolunda olduğunu göstermez.
7. Kendine. Genellikle: metin (slogan, başlık), görsel, pano. Metin halkasının çıktısı mutlaka saklanmalı: her seferinde farklı
   çıkar ve sonraki halkalar ona dayanır. Görseller de: kotadan yer.
