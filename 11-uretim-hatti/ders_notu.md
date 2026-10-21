# Konu 11 — Zincirleme: Üretim Hattı

Bu not konunun özetidir; derste çalıştırdığımız `ders.ipynb` defteriyle **aynı sırada**
ilerler: Isınma, sonra Adım 1–8 ve kısa bir Bonus. Derste kaçırdığın bir yer olursa
buradan oku, sonra defterde o adımın hücrelerini çalıştır. Nottaki kod blokları
defterdeki hücrelerin birebir aynısı.

**Konu 10'a kadar:** her iş ayrı bir defterdi: Konu 5'te slogan, Konu 8'de tek görsel, Konu 9'da bir ızgara, Konu 10'da video.
**Bu konuda:** bunları tek bir **hatta** bağlıyoruz:

> `ayarlar.json`'daki brif → metin modeliyle sloganlar → görsel modeliyle her slogana bir görsel → (Bonus) videoya çevrilen bir görsel.
> Bir halkanın çıktısı, sıradaki halkanın girdisi. Biten halka yeniden çalışmaz, kopan halka hattı durdurmaz, her şey kayda geçer.

**Konunun sonunda elinde:** `ciktilar/kafe_afisi_1/` klasöründe üç slogan (`sloganlar.json`), her slogana bir görsel
(`gorsel_1.jpg` ...), ikisini yan yana gösteren bir pano (`pano.png`) ve hattın üretim günlüğü (`uretim.json`).

**Kurulum:** yeni kütüphane yok. `git pull` ile konu klasörü geldikten sonra `gita3111` klasöründe bir kez `uv sync` çalıştır.

**Anahtar:** Isınma, Adım 1 ve Adım 2 anahtarsız. Adım 3'ten sonrası `anahtar.txt` ister (Konu 2'deki dosya, `gita3111`
klasöründe). Defterin tamamı 4 metin ve 3 görsel isteği gönderir (Bonus 1 ile 4 görsel); Adım 6'da bilerek
reddedilen 3 görsel isteği de var. Hepsi ücretsiz günlük kotanın küçük bir kısmı. Video (Bonus 2) varsayılan olarak kapalı; açarsan `anahtar.txt`'deki Konu 10 satırları
(`VIDEO_ADRES`, `VIDEO_KOD`) da gerekir.

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

- Üç satırın üçü de değişti. Hattın başındaki tek girdi sonuna kadar taşınır; bu yüzden hattın en önemli satırı brif.
- Konuyu kendi seçtiğin bir şeyle değiştirip bir kez daha dene.

Gerçek hatta her halka bir istek. Bugünkü hat 3 slogan ve 3 görsel istiyor:

```python
slogan_istegi = 3
gorsel_istegi = 3
calistirma = 5

print("Hiçbir şeyi saklamadan:", calistirma * (slogan_istegi + gorsel_istegi))
print("Bitenleri saklayarak:", slogan_istegi + gorsel_istegi)
```

Çıktı:

```
Hiçbir şeyi saklamadan: 30
Bitenleri saklayarak: 6
```

Görsel başına yaklaşık 58 neuron (Konu 9): saklamadan 15 görsel ~870 neuron, saklayarak 3 görsel ~174. Bir slogan bunun yanında çok
ucuz (10 neuron'dan az). Ama Adım 4'te göreceğiz: sloganı saklamanın asıl sebebi kota değil.

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
  "tohum": 42,
  "video": false,
  "hareket": "the camera slowly moves closer"
}
```

Bu bir **yapılandırma dosyası** (config): hattın bütün ayarları koddan ayrı, tek yerde. Müşteri ya da konu değişince kodu değil
bu dosyayı değiştiririz. Biçimi JSON (Konu 2 ve Konu 9): tek katman bir sözlük.

```python
import json

with open("ayarlar.json", encoding="utf-8") as dosya:
    ayarlar = json.load(dosya)

print(ayarlar)
```

- `json.load` dosyayı okuyup sözlüğe çevirir; Konu 9'da günlüğü geri okurken kullandık.
- Dosyada `false` yazıyor, ekranda `False` görünür: JSON'da `true` / `false` küçük harfle yazılır, Python'a `True` / `False`
  olarak gelir. Dosyaya `True` yazarsan `json.load` hata verir (bkz. sık hatalar).
- JSON'da metinler **çift tırnak** içinde, sayılar tırnaksız; son satırdan sonra virgül yok.

Her ayarı bir değişkene alıyoruz:

```python
calisma = ayarlar["calisma"]
konu = ayarlar["konu"]
stil = ayarlar["stil"]
slogan_sayisi = ayarlar["slogan_sayisi"]
sicaklik = ayarlar["sicaklik"]
tohum = ayarlar["tohum"]
video_istendi = ayarlar["video"]
hareket = ayarlar["hareket"]

print(konu, "/", stil)
```

Çıktı: `sessiz bir çalışma kafesi / risograph print poster, two colors`.

- Aşağıdaki hücreler bu kısa adları kullanıyor (`konu`, `stil`, `tohum`...).
- `konu` Türkçe (slogan için, Türkçe soruyla gidecek), `stil` ve `hareket` İngilizce (görsel ve video modeline gidecek; Konu 7).
- `ayarlar.json`'u değiştirirsen bu iki hücreyi yeniden çalıştır; yoksa değişkenler eski değerleri taşır.

---

## Adım 2 — Çalışma klasörü

```python
from pathlib import Path

klasor = Path("ciktilar") / calisma
klasor.mkdir(parents=True, exist_ok=True)
print(klasor)
```

Çıktı: `ciktilar/kafe_afisi_1` (Windows'ta `ciktilar\kafe_afisi_1`).

- Hattın bütün çıktıları tek bir klasöre gidiyor: `ciktilar/` içinde, adı `ayarlar.json`'daki `calisma` alanından gelen bir klasör.
- `/` Konu 8'deki gibi yolları birleştirir.
- `parents=True`: `ciktilar/` henüz yoksa onu da kur. `exist_ok=True`: klasör zaten varsa hata verme (Konu 8).

**Neden klasör adında otomatik tarih yok?** Konu 8'de dosya adına tarih ve saat eklemiştik: hiçbir şey üzerine yazılmasın diye.
Klasöre otomatik tarih eklesek her çalıştırmada yeni bir klasör açılırdı; içinde hiçbir şey "zaten var" olmazdı ve hat her şeyi
baştan üretirdi. Konu 9'un kuralı geçerli: **aynı iş, aynı ad**.

| Klasör adı | Ne olur |
|---|---|
| Kodda otomatik tarih (`2026-11-04_18-57-25`) | Her çalıştırma yeni klasör; her şey yeniden üretilir, kota gider |
| `ayarlar.json`'da senin verdiğin ad (`kafe_afisi_1`) | Aynı brif aynı klasör; biten atlanır, kaldığı yerden devam |

Tarihli bir arşiv istiyorsan tarihi adın içine **sen** yaz: `"calisma": "2026-11-04_kafe"`. Brifi değiştirdiğinde (konu, stil,
tohum) `calisma` adını da değiştir: yeni brif yeni klasörde başlar, eskisi olduğu gibi kalır. (Konu 9'daki uyarının aynısı:
adda olmayan bir şeyi değiştirirsen program bunun yeni bir iş olduğunu bilemez.)

---

## Adım 3 — Hazır halkalar

```python
from halkalar import modele_sor, sabirli_ciz, video_uret
```

`halkalar.py` bu klasördeki yardımcı dosya. Eski konularda yazdığın fonksiyonlar içinde hazır:

| Fonksiyon | Nereden | Ne yapar | Başarısızsa |
|---|---|---|---|
| `modele_sor(soru, sicaklik)` | Konu 5 | Metin modeline (`llama-3.3-70b`) sorar, cevabı metin olarak verir | `None` (Konu 5'tekinden tek farkı: çökmez) |
| `sabirli_ciz(yonerge, tohum)` | Konu 9 | Görsel modeline (`flux-1-schnell`) en fazla üç kez dener, görselin baytlarını verir | `None` |
| `video_uret(yonerge, yol, gorsel_yolu)` | Konu 10 | Video aracı hizmetine görseli gönderir, bitene kadar bekler, videoyu `yol`'a kaydeder; video zaten varsa istek göndermez | `None` |

`halkalar.py` anahtarı `../anahtar.txt`'den kendisi okur: bu hücre ilk çalıştığında. `anahtar.txt`'yi sonradan düzeltirsen çekirdeği yeniden
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

- `.strip()`: baştaki ve sondaki boşlukları (satır sonları dahil) siler. Konu 1'de satırları temizlerken kullandık.
- `.replace('"', "")`: düz tırnakları hiçle değiştirir, yani siler. Tırnak işaretinin kendisini tek tırnak içine yazıyoruz: `'"'`.
- Model kıvrık tırnak (`“ ”`) ya da `Slogan:` yazdıysa aynı satırı o işaretle bir kez daha yaz:
  `temiz = temiz.replace("Slogan: ", "")`.
- Modelin cevabı Cloudflare'de varsayılan olarak 256 belirteçle (token) sınırlı (`max_tokens`). Slogana fazlasıyla yeter; ama
  modelden uzun bir metin istersen cevap yarıda kesilir.
- `cevap` `None` ise (istek başarısız) `.strip()` hata verir: `AttributeError: 'NoneType' object has no attribute 'strip'`.
  Üstteki `İstek başarısız` satırına bak.

---

## Adım 4 — 1. halka: sloganlar (ara çıktıyı sakla)

Bir halkanın sonucu hattın **ara çıktısı**. Sloganları bir dosyada saklıyoruz: `sloganlar.json`.

```python
slogan_dosyasi = klasor / "sloganlar.json"

def slogan_halkasi():
    if slogan_dosyasi.exists():
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

- Dosya varsa: `json.load` ile oku, ver. Modele hiç istek gitmez; `return` fonksiyonu orada bitirir.
- Yoksa: `slogan_sayisi` kez sor. `range(slogan_sayisi)` = "3 kez" (`slogan_sayisi` 3). Her cevabı temizle, listeye ekle; sonunda
  listeyi dosyaya yaz ve ver.
- Bir cevap gelmezse (`None`) o turu atla (`continue`): hat durmaz, liste bir eksik olur.
- Dosyaya yazmak Konu 9'daki günlükle aynı: `json.dump(..., ensure_ascii=False, indent=2)`.
- Fonksiyon `slogan_dosyasi`, `soru`, `sicaklik` ve `slogan_sayisi`'yı yukarıdaki hücrelerden alıyor.

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
çalıştırmada yeniden üretseydik `gorsel_1.jpg` dünkü sloganla, günlük bugünkü sloganla kalırdı: görsel ile metin birbirini
tutmazdı.

> **Kural:** pahalı ya da her seferinde farklı çıkan ara çıktıyı sakla. Ucuz ve her seferinde aynı çıkanı (Adım 5'teki
> yönergeler gibi) yeniden kur.

Bir dikkat: üç istekten biri başarısız olursa dosyaya iki slogan yazılır ve sonraki çalıştırmalar o ikisiyle devam eder. Üçünü de
istiyorsan `sloganlar.json`'u sil, hücreyi yeniden çalıştır.

---

## Adım 5 — 2. halka: her slogana bir görsel

Önce her slogan için görsel yönergesini kuruyoruz:

```python
yonergeler = []
for slogan in sloganlar:
    yonerge = f"{stil}, a poster illustration that expresses this idea: {slogan}, no text, no letters"
    yonergeler.append(yonerge)
    print(yonerge)
```

Çıktı: üç yönerge, her biri `risograph print poster, two colors, a poster illustration that expresses this idea: ...,
no text, no letters` biçiminde.

- Bu bir kalıp (Konu 9'daki şablon): sabit kısım ve iki değişen yer (`stil`, `slogan`).
- Yönergeleri saklamıyoruz: sloganlardan ve ayarlardan her seferinde aynı biçimde, bedavaya kurulur.
- Sloganlar Türkçe, yönergenin geri kalanı İngilizce. Görsel model çoğunlukla İngilizce metinle eğitildi (Konu 7); Türkçe
  sloganın fikrini ne kadar anladığı görsellerde görülür.
- **"no text, no letters"** bilerek orada: tipografiyi modele bırakmıyoruz. Görsel modeller harfleri çoğu zaman bozar; sloganı
  afişe tasarımcı dizer. Hat **taslak** üretir; son biçim tasarımcının.

Görsel halkası tek bir görsel için çalışan bir fonksiyon:

```python
def gorsel_halkasi(sira, yonerge):
    yol = klasor / f"gorsel_{sira}.jpg"
    kayit = {"halka": "gorsel", "girdi": yonerge, "cikti": str(yol), "durum": "denenmedi"}
    if yol.exists():
        kayit["durum"] = "uretildi"
        print("Zaten var, atlıyorum:", yol)
        return kayit
    resim = sabirli_ciz(yonerge, tohum)
    if resim is None:
        kayit["durum"] = "olmadi"
        print("Olmadı, atlıyorum:", yol)
        return kayit
    with open(yol, "wb") as dosya:
        dosya.write(resim)
    kayit["durum"] = "uretildi"
    print("Kaydedildi:", yol)
    return kayit
```

- Slogan halkasıyla **aynı kalıp**: zaten var mı? Varsa onu ver. Yoksa üret, sakla, ver. Konu 9'daki `toplu_uret`'in tek görsellik hâli.
- `yol.exists()`: dosya varsa atla (Konu 9). Atlanan görselin durumu da `uretildi`: dosya orada.
- Her yoldan bir **kayıt** (sözlük) çıkıyor: hangi halka (`halka`), ne girdi (`girdi`: yönerge), hangi dosya çıktı (`cikti`),
  sonuç ne (`durum`: `uretildi` ya da `olmadi`).
- `kayit["durum"] = ...`: sözlükteki bir değeri değiştirir (Konu 9'daki `kart["durum"]`).
- `str(yol)`: yolu metne çevirir. Kayıt sonunda JSON'a yazılacak; JSON `Path`'i yazamaz (Konu 10'daki günlükte de böyleydi).
- `return kayit` fonksiyonu orada bitirir; hangi yoldan çıkarsa çıksın elimize bir kayıt gelir.

Şimdi zinciri kuruyoruz:

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

- Görsel model boş yönergeyi kabul etmez: durum kodu 400 ("isteğin hatalı", Konu 2). `sabirli_ciz` üç kez dener (Konu 9); kalıcı
  bir hatada beklemek işe yaramaz ama basit bir program bunu ayırt edemez.
- Hücre **çökmedi**: `gorsel_halkasi` hata yerine `"durum": "olmadi"` yazan bir kayıt verdi. Bir döngünün içinde olsaydık döngü
  sıradaki görsele geçerdi.
- Hat iki şeyi birlikte yapıyor: kopuk halkayı **kayda geçiriyor** (hangi görsel, `durum`: `olmadi`) ve kopmayanlarla **devam ediyor**.
- `gorsel_4.jpg` hiç oluşmadı; hattı yarın yeniden çalıştırırsan yalnızca o denenir (kaldığı yerden devam).

| Kopan halka hattı durdurursa | Kopan halka kayda geçerse |
|---|---|
| Üçüncü görselde internet gitti: dördüncü ve beşinci hiç denenmedi | Üçüncü `olmadi` diye kaydedildi; dördüncü ve beşinci üretildi |
| Neyin eksik olduğunu bulmak için klasöre tek tek bakarsın | Eksikler günlükte yazıyor |
| Baştan çalıştırırsın | Yeniden çalıştırınca yalnızca eksik olan denenir |

---

## Adım 7 — Üretim günlüğü: `uretim.json`

```python
gunluk = {"ayarlar": ayarlar, "sloganlar": sloganlar, "kayitlar": kayitlar}

with open(klasor / "uretim.json", "w", encoding="utf-8") as dosya:
    json.dump(gunluk, dosya, ensure_ascii=False, indent=2)

print("Günlük yazıldı:", len(kayitlar), "kayıt")
```

Çıktı: `Günlük yazıldı: 4 kayıt`.

- `gunluk` bir sözlük, içinde üç bölüm: hangi ayarlarla çalıştı (`ayarlar`), hangi sloganlar çıktı (`sloganlar`), her görselin
  sonucu ne (`kayitlar`).
- `klasor / "uretim.json"`: günlük, çıktıların yanında, aynı klasörde. Her brifin günlüğü kendi klasöründe.
- `json.dump` Adım 4'teki gibi: önce yazılacak şey, sonra dosya.

Program günlüğü geri okuyup eksikleri bulabilir:

```python
with open(klasor / "uretim.json", encoding="utf-8") as dosya:
    okunan = json.load(dosya)

okunan_kayitlar = okunan["kayitlar"]
for kayit in okunan_kayitlar:
    if kayit["durum"] == "olmadi":
        print("Eksik:", kayit["cikti"])
```

Çıktı: `Eksik: ciktilar/kafe_afisi_1/gorsel_4.jpg`.

- `okunan["kayitlar"]`: sözlüğün `kayitlar` bölümü, bir liste. Önce onu ayrı bir değişkene alıyoruz, sonra geziyoruz.
- Final projesinin teslimindeki **üretim günlüğü** bu dosya: hangi brif, hangi model ayarı, ne çıktı, ne eksik kaldı.

---

## Adım 8 — Pano: slogan ve görsel yan yana

Konu 9'da yazdığın kontak sayfası, bu kez tek satır:

```python
import matplotlib.pyplot as plt

sutun = len(sloganlar)

plt.figure(figsize=(12, 5))
sira = 0
for slogan in sloganlar:
    sira = sira + 1
    yol = klasor / f"gorsel_{sira}.jpg"
    plt.subplot(1, sutun, sira)
    if yol.exists():
        resim = plt.imread(yol)
        plt.imshow(resim)
    plt.title(slogan, fontsize=9)
    plt.axis("off")

plt.savefig(klasor / "pano.png", bbox_inches="tight")
plt.show()
```

- `plt.subplot(1, sutun, sira)`: 1 satır, `sutun` sütun, `sira`'ncı kutu (Konu 6 ve 9).
- `plt.imread` görseli dosyadan okur, `plt.imshow` kutuya koyar; dosya yoksa kutu boş kalır.
- `plt.title(slogan, ...)`: her kutunun üstünde onu doğuran slogan.
- Pano da çalışma klasörüne kaydediliyor: `pano.png`.
- Döngü sloganları geziyor; Adım 6'daki dördüncü kayıt panoda yok (sloganı yoktu).

**Tartış:** hangi slogan hangi görselle güçlü? Slogan ile görselin **aynı şeyi söylediği** kutu mu daha iyi, yoksa birbirini
**tamamladığı** kutu mu (görsel bir şey gösteriyor, slogan ona yeni bir anlam ekliyor)? Afişte metin ile görselin ilişkisi
tasarımcının asıl işi; hat bunu senin yerine düşünmez.

Videoya çevirmek isteyeceğin görseli yaz (Bonus 2 bunu kullanır):

```python
secilen = klasor / "gorsel_1.jpg"
```

---

## Bonus

**1. Ara çıktıya elle dokun.** Ara çıktıyı saklamanın bir faydası daha var: hattın ortasında araya girebilirsin.

1. `ciktilar/kafe_afisi_1/sloganlar.json`'u VS Code'da aç, ikinci sloganı kendi yazdığın bir sloganla değiştir, kaydet.
   Tırnakları ve virgülleri bırak; JSON biçimi bozulmasın.
2. Aynı klasördeki `gorsel_2.jpg`'yi sil.
3. Adım 4'ün ilk çağrı hücresinden Adım 5'in sonuna kadar sırayla yeniden çalıştır, sonra Adım 8'in pano hücresini.

Slogan halkası dosyadan okur (senin sloganınla, istek gitmez). Görsel halkası 1 ve 3'ü atlar, yalnızca 2'yi üretir: tek istek.
Panoda yalnızca bir kutu değişir. Hat makinenin işini yapıyor; sen istediğin yerde araya girip yönünü değiştiriyorsun.

**2. 3. halka: video.** Varsayılan olarak kapalı: video hocanın hesabından, ücretli üretiliyor ve sayısı sınırlı (Konu 10).
Açmak için `ayarlar.json`'da `"video": false` satırını `"video": true` yap, kaydet, Adım 1'in iki hücresini yeniden çalıştır.

```python
def video_halkasi(gorsel_yolu):
    video_yolu = klasor / "video.mp4"
    kayit = {"halka": "video", "girdi": str(gorsel_yolu), "cikti": str(video_yolu), "durum": "denenmedi"}
    sonuc = video_uret(hareket, video_yolu, gorsel_yolu)
    if sonuc is None:
        kayit["durum"] = "olmadi"
    else:
        kayit["durum"] = "uretildi"
    return kayit
```

- Aynı kalıp, üçüncü kez. "Zaten var mı?" sorusunu Konu 10'daki `video_uret` kendisi soruyor: `video.mp4` varsa
  `Zaten var, yeni iş başlatmıyorum` der ve istek göndermez. Başarılıysa dosyanın yolunu, değilse `None` verir; halka buna
  bakıp kaydın durumunu yazıyor.
- Girdisi görsel halkasının çıktısı (`secilen`); hareketin ne olacağı ayarlarda (`hareket`).
- `video_uret` Konu 10'daki işi yapar: görseli metne çevirip gönderir, iş numarasını alır, bitene kadar 10 saniyede bir sorar
  (en fazla 6 dakika), videoyu indirip kaydeder.

```python
if video_istendi:
    kayit = video_halkasi(secilen)
    kayitlar.append(kayit)
else:
    print("Video kapalı: ayarlar.json'da video false")
```

- Video kapalıysa `Video kapalı: ayarlar.json'da video false` yazar, istek gitmez.
- Açıksa birkaç dakika sürebilir; ekranda `İş başladı: ...` ve `Henüz bitmedi, geçen süre: ... saniye` satırlarını görürsün.
- **Zaman aşımı olursa** (`Zaman aşımı; iş sürüyor olabilir. İş numarası: ...`) hücreyi yeniden çalıştırma: `video.mp4` henüz
  yok, yeni ve ücretli bir iş başlar. Konu 10'un kuralı: işi bir kez başlat, numarayı sakla. İş numarasını not et; Konu 10
  defterinde `bekle(is_no)` ile yeniden sorabilirsin, bu ücretsiz.

Günlüğü videoyla birlikte yeniden yaz:

```python
gunluk = {"ayarlar": ayarlar, "sloganlar": sloganlar, "kayitlar": kayitlar}

with open(klasor / "uretim.json", "w", encoding="utf-8") as dosya:
    json.dump(gunluk, dosya, ensure_ascii=False, indent=2)

print("Günlük güncellendi:", len(kayitlar), "kayıt")
```

Video kaydının `girdi`'si bir görsel kaydının `cikti`'sı: zincir günlükte de görünüyor.

---

## Defterin bölümleri

| Adım | Ne yaptık | Elimizde ne oluştu | Anahtar |
|---|---|---|---|
| Isınma | Sahte halkalarla zincir; konuyu değiştirmek; istek hesabı | — | gerekmez |
| 1 | Ayarlar dosyasını okuduk | `ayarlar`, `konu`, `stil`, `tohum` ... | gerekmez |
| 2 | Çalışma klasörü | `klasor` (`ciktilar/kafe_afisi_1/`) | gerekmez |
| 3 | Hazır halkalar; bir deneme sloganı, temizleme | `modele_sor`, `sabirli_ciz`, `video_uret`, `soru` | gerekir |
| 4 | 1. halka: sloganlar; ara çıktıyı sakla | `slogan_halkasi`, `sloganlar`, `sloganlar.json` | gerekir |
| 5 | 2. halka: yönergeler ve görseller | `yonergeler`, `gorsel_halkasi`, `kayitlar`, `gorsel_1.jpg` ... | gerekir |
| 6 | Bir halkayı bilerek kopardık | `olmadi` durumlu bir kayıt | gerekir |
| 7 | Üretim günlüğü: yaz ve eksikleri bul | `uretim.json` | gerekmez |
| 8 | Pano; kendi seçimin | `pano.png`, `secilen` | gerekmez |
| Bonus | Ara çıktıya elle dokunmak; 3. halka: video | `video_halkasi`, `video.mp4` | gerekir |

Derste kendi başına çalışacağın defter: `alistirma.ipynb`. Önce aynı klasörde yeni bir adla kopyala, kopyada çalış.
**Anahtar istemez ve internete çıkmaz:** halkalar sahte ve her çağrıyı sayıyor; kaç istek gittiğini görebiliyorsun. İki bölümü var:

- **Bozuk kodlar:** beş kısa hücre, birbirinden bağımsız. İkisi hata mesajı veriyor, üçü sessizce yanlış sonuç yazıyor.
- **Kendi başına:** `BOSLUK` yazan yerleri doldurduğun altı soru ve bir ek soru (ara çıktıyı kendin saklamak).

---

## Sık karşılaşılan hatalar ve mesajlarını okumak

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `FileNotFoundError: ... 'ayarlar.json'` (Adım 1) | Defterin kopyası konu klasörünün dışında ya da dosya adı farklı | Kopya `ayarlar.json`'un yanında, `11-uretim-hatti` klasöründe olmalı |
| `JSONDecodeError: Expecting value: line 8 column 12 ...` | `ayarlar.json`'a `True` / `False` (büyük harf) ya da tırnaksız metin yazılmış | JSON'da `true` / `false` küçük harf; metinler çift tırnak içinde |
| `JSONDecodeError: Illegal trailing comma before end of object ...` | Son satırdan sonra virgül kalmış | Son ayarın sonundaki virgülü sil |
| `JSONDecodeError: Expecting ',' delimiter ...` | İki satır arasında virgül eksik | Her ayarın sonuna (sonuncusu hariç) virgül |
| `KeyError: 'Konu'` ya da `KeyError: 'video'` | Ayar adı dosyadakinden farklı (büyük harf, eksik satır) | Adı dosyadakiyle birebir yaz; kendi ayarlar dosyanda bütün satırlar olmalı |
| `NameError: name 'modele_sor' is not defined` (ya da `'sabirli_ciz'`) | Adım 3'ün import hücresi hata verdi (çoğunlukla anahtar dosyası) ya da çalıştırılmadı | Önce o hücredeki hatayı düzelt, sonra sırayla devam et |
| `ModuleNotFoundError: No module named 'halkalar'` | Defterin kopyası konu klasörünün dışında | Kopya `halkalar.py`'nin yanında olmalı |
| `FileNotFoundError: ... '../anahtar.txt'` (Adım 3) | Anahtar dosyası yok ya da yanlış yerde | `gita3111` klasöründe durmalı; sonra Adım 3'ün ilk hücresini yeniden çalıştır |
| `İstek başarısız, durum kodu: 401` | Anahtar yanlış | `anahtar.txt`'yi düzelt, çekirdeği yeniden başlat (**Restart**), baştan çalıştır |
| `AttributeError: 'NoneType' object has no attribute 'strip'` (Adım 3) | Deneme isteği başarısız oldu, `cevap` `None` | Üstteki `İstek başarısız` ya da `Bağlanamadım` satırına bak |
| `Slogan gelmedi, atlıyorum` | Bir metin isteği başarısız oldu | Hat iki sloganla devam eder. Üçünü istiyorsan `sloganlar.json`'u sil, yeniden çalıştır |
| `sloganlar` boş liste: `[]` | Bütün metin istekleri başarısız oldu ve boş liste dosyaya yazıldı | Sorunu düzelt (anahtar, internet), `sloganlar.json`'u sil, yeniden çalıştır |
| Hep `Dosyadan okundu`, sloganlar eski konudan | `ayarlar.json`'da konuyu değiştirdin ama `calisma` aynı kaldı | Yeni brif için `calisma` adını da değiştir |
| `JSONDecodeError` (Adım 4, Bonus 1 sonrası) | `sloganlar.json`'u elle düzeltirken bir tırnak ya da virgül silindi | Dosyayı düzelt: `["...", "...", "..."]` biçiminde olmalı |
| Görsel eski sloganı anlatıyor | Sloganı değiştirdin ama görseli silmedin | O görseli sil; görsel halkası yalnızca olmayanı üretir |
| `TypeError: Object of type PosixPath is not JSON serializable` (Windows'ta `WindowsPath`) | Kayda `yol` metne çevrilmeden yazıldı | `str(yol)` |
| `İstek başarısız, durum kodu: 400` (Adım 6) | Boş yönerge; bilerek | Doğru davranış: kayıtta `olmadi` |
| `İstek başarısız, durum kodu: 429` ve `Deneme ... olmadı` | Çok hızlı istek ya da günlük kota doldu | Bekle; üst üste geliyorsa hücreyi durdur (**Interrupt**). Kota yenilenince aynı hücreyi yeniden çalıştır; kaldığı yerden devam eder |
| `NameError: name 'klasor' is not defined` | Adım 2 çalıştırılmadı | Sırayla çalıştır |
| `NameError: name 'slogan_halkasi' is not defined` ya da `'gorsel_halkasi'` | Fonksiyonun tanımlandığı hücre atlandı | O hücreyi çalıştır |
| Panoda boş kutu | O görsel üretilemedi | Kayıtta `olmadi` yazar; Adım 5'in döngü hücresini, sonra panoyu yeniden çalıştır |
| `Video kapalı ...` ama `ayarlar.json`'da `true` yazdım | Adım 1 yeniden çalıştırılmadı | Adım 1'in iki hücresini yeniden çalıştır |
| `Zaman aşımı; iş sürüyor olabilir. İş numarası: ...` (Bonus 2) | Video işi 6 dakikadan uzun sürdü | Hücreyi yeniden çalıştırma (yeni ücretli iş); numarayı not et, Konu 10 defterinde `bekle(is_no)` ile sor |
| `anahtar.txt'de VIDEO_ADRES ya da VIDEO_KOD satırı yok` | Konu 10'un satırları anahtar dosyasında yok | Konu 10'daki iki satırı ekle, çekirdeği yeniden başlat |

---

## Kendini dene

Cevaplar notun en sonunda. Önce kendin düşün.

1. Bir arkadaşın çalışma klasörünü `ayarlar.json`'dan değil, Konu 8'deki gibi o anki tarih ve saatle kurdu. Hattı üç kez
   çalıştırınca ne olur?
2. Yönergeleri neden saklamadık da sloganları sakladık?
3. `ayarlar.json`'da konuyu "gece açık bir kitapçı" yaptın, kaydettin ve bütün defteri yeniden çalıştırdın; `calisma` adını
   değiştirmedin. Ne görürsün?
4. Görsel halkası kopunca hata verip dursaydı (`return` yerine program çökseydi), beş görsellik bir hatta üçüncü görselde
   internet gidince ne olurdu?
5. Görsel yönergesinde neden "no text, no letters" yazıyoruz? Slogan afişe nasıl girecek?
6. Video kaydının `girdi`'si neden bir dosya yolu?
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
| **Halka** | Hattın bir adımı: slogan, görsel, video |
| **Ara çıktı** | Bir halkanın ürettiği, sıradaki halkaya giden sonuç (ör. `sloganlar.json`) |
| **Yapılandırma dosyası (config)** | Programın ayarlarını koddan ayrı tutan dosya (`ayarlar.json`) |
| **Çalışma klasörü** | Bir brifin bütün çıktılarının toplandığı klasör |
| **Kayıt** | Bir işin girdisi, çıktısı ve sonucu (bir sözlük) |
| **Üretim günlüğü** | Hattın ayarlarını, ara çıktılarını ve bütün kayıtlarını tutan dosya (`uretim.json`) |
| **`true` / `false`** | JSON'da doğru / yanlış; Python'a `True` / `False` olarak gelir |
| **`.strip()` / `.replace(a, b)`** | Baştaki ve sondaki boşlukları silmek / metindeki `a`'ları `b` ile değiştirmek |
| **`str(yol)`** | Dosya yolunu metne çevirmek (JSON'a yazmak için) |
| **`parents=True`** | Klasörü kurarken üst klasör yoksa onu da kurmak |

## Ödev

`odevler/odev11.md` (puansız): kendi projenin hat iskeleti. Kendi ayarlar dosyan, en az iki halka çalışıyor (metin ve görsel),
panosu ve üretim günlüğü. Güzel olması gerekmiyor; final projesinin ilk taslağı.

## Sonraki konu

**Konu 12 — Araç kullanımı: modelin karar verdiği program.** Bugün hangi halkanın ne zaman çalışacağına sen karar verdin: önce
slogan, sonra görsel, sonra video; sıra kodda yazılı. Peki kullanıcı "kafeye aylık bir afiş yap" ya da "şu görselin arka planını
sadeleştir" diye serbest bir cümle yazsa, hangi halkanın çalışacağına kim karar verir? Konu 12'de bu kararı modele bırakıyoruz:
modele elimizdeki fonksiyonları ("araçları") tanıtıyoruz, model cümleye bakıp hangisinin çağrılacağını söylüyor, program o aracı
çalıştırıyor. Bugünkü görsel halkası gibi fonksiyonlar o konunun araçları olacak.

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
6. Çünkü video halkasının girdisi görsel halkasının çıktısı. Günlükte bu bağ görünüyor: hangi videonun hangi görselden, o görselin
   hangi yönergeden çıktığı.
7. Kendine. Genellikle: metin (slogan, başlık), görsel, (isteğe bağlı) video, pano. Metin halkasının çıktısı mutlaka saklanmalı:
   her seferinde farklı çıkar ve sonraki halkalar ona dayanır. Görseller de: pahalı.
