# Konu 10 — Video Üretimi

Bu not konunun özetidir; derste çalıştırdığımız `ders.ipynb` defteriyle **aynı sırada**
ilerler: Isınma, sonra Adım 1–8 ve kısa bir Bonus. Derste kaçırdığın bir yer olursa
buradan oku, sonra defterde o adımın hücrelerini çalıştır. Nottaki kod blokları
defterdeki hücrelerin birebir aynısı.

**Konu 9'da:** bir şablon ve listelerle bir görsel ızgarası ürettik; her görsel birkaç saniyede geldi.
**Bu konuda:** görsele zaman ekliyoruz. Kodun yeni fikri **uzun süren iş**:

> Video istediğin anda gelmez; hazır olması birkaç dakika sürebilir. İsteği başlatırsın, bir iş numarası alırsın, numarayı saklarsın,
> arada bir "bitti mi?" diye sorarsın (bir sınıra kadar), bitince indirirsin. Ve her saniyenin bir fiyatı var.

**Konunun sonunda elinde:** `videolar/` klasöründe iki kısa video (biri yalnız yönergeden, biri Konu 9'daki
görselinden) ve her videonun nasıl üretildiğini ve kaça mal olduğunu kaydeden bir günlük (`video_gunlugu.json`).

**Kurulum:** yeni kütüphane yok. `git pull` ile konu klasörü geldikten sonra `gita3111` klasöründe
bir kez `uv sync` çalıştır.

**Anahtar:** Isınma, Adım 1 ve Adım 2 anahtarsız; Isınma ve Adım 2 internetsiz de çalışır. Adım 3'ten sonrası `anahtar.txt`'ye derste
eklediğimiz iki satırı (`VIDEO_ADRES`, `VIDEO_KOD`) ister. Videolar hocanın hesabından bir **aracı hizmet**
üzerinden üretiliyor; defter 2 klip üretir (4'er saniye, 720p), Bonus ile 3. Klip hakkın sınırlı.

> **Bu nottaki çıktılar hakkında.** Isınma ve Adım 2'nin çıktıları her bilgisayarda aynıdır. Videolar,
> bekleme süreleri ve iş numaraları gerçek hizmetten gelir; senin ekranında farklı olur.

---

## Isınma: bir video kaç para?

Görseller ücretsiz kotadan geliyordu. Video saniye başına ücretlidir. Dersin modeli Gemini Omni Flash; Gemini API
fiyat sayfasına göre 720p'de (1280 × 720 piksel) saniyesi **yaklaşık 0,10 dolar** (Ekim 2026). Aracı hizmet çözünürlüğü 720p'ye kilitliyor.

```python
UCRET_SANIYE = 0.10

sure = 4
print(sure, "saniyelik klip:", sure * UCRET_SANIYE, "USD")
```

Çıktı: `4 saniyelik klip: 0.4 USD`.

- `UCRET_SANIYE` büyük harfle: değişmeyen bir sabit (Konu 9'daki `MAKS_URETIM` gibi).
- Python ondalık sayıları **noktayla** yazar: `0.10`. Notta Türkçe yazımla 0,10 diyoruz; ikisi aynı sayı.
- Fiyatlar sık değişir; bu rakam Ekim 2026'daki fiyat sayfasından alındı ve yaklaşık bir değer.

Bir müşteri 20 saniyelik bir tanıtım istiyor. Aracı hizmet klipleri 4, 6 ya da 8 saniye üretiyor; daha uzun bir video, klipleri
kurguda birleştirerek yapılır. 20 = 8 + 8 + 4:

```python
klipler = [8, 8, 4]
toplam = 0
for klip in klipler:
    toplam = toplam + klip

print("Toplam süre:", toplam, "saniye")
print("Ücret:", toplam * UCRET_SANIYE, "USD")
```

Çıktı: `Toplam süre: 20 saniye` ve `Ücret: 2.0 USD`. Toplamı Konu 1'deki sayaçla buluyoruz: `toplam` 0'dan başlar,
her klipte üstüne eklenir.

Müşterinin bütçesi bunun yarısı. Çözünürlük kilitli; oranı (16:9 ya da 9:16) değiştirmek fiyatı değiştirmiyor. Aynı işi yarı
fiyatına nasıl yaparsın?

```python
kisa_klipler = [4, 6]
toplam_kisa = 0
for klip in kisa_klipler:
    toplam_kisa = toplam_kisa + klip

print("Toplam süre:", toplam_kisa, "saniye")
print("Ücret:", toplam_kisa * UCRET_SANIYE, "USD")
```

Çıktı: `Toplam süre: 10 saniye` ve `Ücret: 1.0 USD`.

- Fiyatı yalnızca **süre** belirliyor: yarı fiyat, yarı süre. 20 saniye yerine 10 saniyelik bir kurgu, iki klip (4 + 6).
- Tek klipte de aynı: 8 saniyelik klip yerine 4 saniyelik klip yarı fiyat.
- **Süre kararı bir bütçe kararıdır.** Sosyal medyada izlenen bir tanıtım için 10 saniye yeter mi? Hangi planları atardın?

Video ile görseli karşılaştıralım. Konu 9'da bir görsel ~58 neuron tutuyordu; Cloudflare ücretsiz kotayı aşanlardan
1.000 neuron için 0,011 dolar alıyor.

```python
gorsel_ucreti = 58 * 0.011 / 1000
klip_ucreti = 4 * UCRET_SANIYE

print("Bir görsel:", gorsel_ucreti, "USD")
print("Bir klip kaç görsel eder:", klip_ucreti / gorsel_ucreti)
```

Çıktı: `Bir görsel: 0.000638 USD` ve `Bir klip kaç görsel eder: 626.95...`.

- 4 saniyelik bir klip yaklaşık **600 görsel** eder. Video art arda gelen onlarca kareden oluşur (saniyede 24 kare:
  4 saniye yaklaşık 100 kare); karelerin birbirini tutması ve ses de işin içinde.
- Bir video denemesi yüzlerce görsel denemesine bedel: önce görselle dene (ucuz), beğendiğini videoya çevir (pahalı).

---

## Adım 1 — Arayüzden bir klip (kod yok)

Konu 7'deki gibi önce arayüzden. Öğrenci hesabınla (Google AI Plus öğrenci teklifi) Gemini uygulamasında video
üretme seçeneğini aç ve kısa bir yönerge yaz, ör. "masada buharı tüten bir seramik fincan, kamera yavaşça yaklaşıyor".
Hesabın yoksa hocanın ekranından izle.

Sonuç kaç saniyede geldi? Beklerken ekranda ne gördün? Arayüz beklemeyi senin yerine yönetiyor: isteği gönderiyor,
arka planda soruyor, bitince gösteriyor. Kodda bunu **sen** yapacaksın.

---

## Adım 2 — Uzun süren iş: önce sahte bir işle

Gerçek video beklemeden önce internetsiz, **sahte** bir işle deniyoruz. `video.py` bu klasördeki yardımcı dosya;
içindeki iki fonksiyon gerçek aracı hizmet gibi cevap veriyor.

```python
import time
from video import sahte_baslat, sahte_durum

govde = {
    "yonerge": "steam rising from a ceramic coffee cup on a wooden desk, soft morning light, slow camera push in",
    "sure": "4",
    "oran": "16:9",
}
yanit = sahte_baslat(govde)
print(yanit)
```

Çıktı: `{'is_no': 'sahte_1'}`.

- `sahte_baslat(govde)` işi başlatır ve bir **iş numarası** verir. Video gelmedi; yalnızca numara geldi.
  Kuru temizlemecideki fiş gibi: ceketi değil, fişi alırsın.
- `govde` gerçek istekte de aynı olacak: yönerge (İngilizce, Konu 7), süre ve oran.
- Süre tırnak içinde (`"4"`): aracı hizmet onu metin olarak bekliyor (Konu 8'deki form alanları gibi).
- `time` beklemek için (Konu 9).

```python
is_no = yanit["is_no"]
durum = sahte_durum(is_no)
print(durum)
```

Çıktı: `{'bitti': False}`.

- İş numarasını bir değişkende saklıyoruz (`is_no`) ve `sahte_durum(is_no)` ile soruyoruz.
- Sahte iş **5 saniye** sürer. Hücreyi birkaç saniye arayla yeniden çalıştırırsan (**Ctrl + Enter** hücrede kalır)
  5 saniye sonra `{'bitti': True, 'video': 'sahte_video.mp4'}` görürsün.

Elle sormak yorucu; döngüye veriyoruz:

```python
yanit = sahte_baslat(govde)
is_no = yanit["is_no"]

for deneme in range(10):
    durum = sahte_durum(is_no)
    if durum["bitti"]:
        print("Hazır:", durum["video"])
        break
    print("Henüz bitmedi, soru", deneme + 1)
    time.sleep(2)

if not durum["bitti"]:
    print("Zaman aşımı. İş numarası:", is_no)
```

Çıktı:

```
Henüz bitmedi, soru 1
Henüz bitmedi, soru 2
Henüz bitmedi, soru 3
Hazır: sahte_video.mp4
```

- Hücre yeni bir sahte iş başlatıyor ki saat sıfırdan başlasın.
- `range(10)`: "10 kez". `deneme` 0'dan başlar; ekrana `deneme + 1` yazıyoruz ki sorular 1'den saysın.
- Bittiyse `break` döngüden çıkar. Bitmediyse `time.sleep(2)`: 2 saniye bekle, yeniden sor.
- 0., 2. ve 4. saniyede iş sürüyordu (üç kez `Henüz bitmedi`), 6. saniyede bitmişti.
- Döngü en fazla 10 × 2 = 20 saniye bekler. Bitmezse sondaki `if` "zaman aşımı" der. **Zaman aşımı** sonsuza kadar
  beklememenin yolu.
- `if not durum["bitti"]`: "iş bitmediyse". `not` bir koşulu tersine çevirir.

**Dene:** `range(10)` yerine `range(2)` yazıp çalıştır: zaman aşımı. Sonra `sahte_durum(is_no)` hücresini
çalıştır: iş **bitmiş**. Zaman aşımı işi iptal etmez; yalnızca senin beklemeni bitirir. İş numaran elindeyse sonra
yeniden sorarsın.

"Çalışmadı" sandığımız şeylerin çoğu "henüz bitmedi"dir. İyi bir program ne olduğunu söyler: "bekliyorum, şu kadar
saniye oldu." Arayüzlerdeki yükleme göstergesi de aynı işi yapar.

---

## Adım 3 — Video kodunu oku

`anahtar.txt`'ye derste iki satır ekledik:

```
VIDEO_ADRES = https://...
VIDEO_KOD = ...
```

```python
import requests
from pathlib import Path
from IPython.display import Video
from video import anahtarlari_oku
```

- `requests` istek göndermek için (Konu 2), `Path` dosya yolları için (Konu 8), `Video` videoyu defterde oynatmak için.
- `anahtarlari_oku` (`video.py`) Konu 9'daki `anahtari_oku`'nun aynısı; bu kez bütün satırları bir sözlük olarak veriyor.

```python
anahtarlar = anahtarlari_oku()
VIDEO_ADRES = anahtarlar["VIDEO_ADRES"]
VIDEO_KOD = anahtarlar["VIDEO_KOD"]
basliklar = {"Authorization": "Bearer " + VIDEO_KOD}

print("Aracı hizmet:", VIDEO_ADRES)
```

Çıktı: `Aracı hizmet: https://...` (hocanın verdiği adres).

- Video kodu başlıkta gidiyor, Konu 2'deki gibi: `Bearer`, bir boşluk, kod.
- Video kodu senin kimliğin: aracı hizmet klip sayını onunla tutar. Hocanın Gemini anahtarını hiç görmüyorsun.
  Kodunu kimseyle paylaşma, ödevle birlikte gönderme.

---

## Adım 4 — Gerçek işi başlat

```python
adres = VIDEO_ADRES + "/baslat"
cevap = requests.post(adres, headers=basliklar, json=govde, timeout=60)
print(cevap.status_code)
yanit = cevap.json()
print(yanit)
```

Çıktı: `200` ve `{'is_no': '...'}` (aracı hizmet başka bilgi de ekleyebilir).

- Adım 2'deki `govde`'yi bu kez aracı hizmete gönderiyoruz: Konu 2'deki `requests.post`, adres `/baslat`.
- `timeout=60`: cevap 60 saniyede gelmezse istek bırakılır.
- **Bu hücreyi bir kez çalıştır.** Her çalıştırma yeni bir iş başlatır: yeni bir klip, yeni bir ücret, klip hakkından bir eksik.
- `200` değilse yanıtta bir `hata` metni var (ör. `video kodu tanınmadı`, `klip hakkın doldu`). Sonraki hücreyi çalıştırma.

```python
is_no = yanit["is_no"]
print("İş numaram:", is_no)
```

İş numaranı bir kenara yaz. Defter kapanırsa ya da bağlantı koparsa iş sunucuda sürmeye devam eder; numarayla yeniden
sorarsın ve yeni bir ücret ödemezsin.

---

## Adım 5 — Bekle: aralıklarla sor

Adım 2'deki döngünün gerçek hâli, bir fonksiyonda (Adım 7'de bir kez daha bekleyeceğiz):

```python
def bekle(is_no):
    durum_adresi = VIDEO_ADRES + "/durum/" + is_no
    for deneme in range(36):
        cevap = requests.get(durum_adresi, headers=basliklar, timeout=30)
        durum = cevap.json()
        if "hata" in durum:
            print("Hata:", durum["hata"])
            return None
        if durum["bitti"]:
            print("Hazır, yaklaşık", deneme * 10, "saniyede")
            return durum["video"]
        print("Henüz bitmedi, geçen süre:", deneme * 10, "saniye")
        time.sleep(10)
    print("Zaman aşımı. İş sürüyor olabilir; iş numarası:", is_no)
    return None
```

- `requests.get`: **get** "bana şunu ver" demek, gövde göndermez. `post` gövdeyle bir şey gönderir (Konu 2).
  Durum adresi `/durum/` ve iş numarası.
- Cevapta `hata` varsa iş başarısız oldu (ör. model yönergeyi reddetti): yaz ve `None` döndür.
- `bitti` ise videonun adresini döndür. `return` fonksiyonu orada bitirir (Konu 9).
- Değilse ne kadar beklediğimizi yaz, 10 saniye bekle, yeniden sor. `deneme * 10` yaklaşık geçen süre.
- En fazla 36 kez: 36 × 10 saniye = **6 dakika**. Bir video birkaç dakika sürebilir; 6 dakikayı sınır seçtik.
  Döngü biterse zaman aşımı; iş numarasını yazıp `None` döndürür.
- İki ayrı sınır var: `timeout=30` **tek bir sorunun** sınırı; `range(36)` **bütün bekleyişin** sınırı.

```python
video_adresi = bekle(is_no)
print(video_adresi)
```

Çıktı (senin sürelerin farklı olur):

```
Henüz bitmedi, geçen süre: 0 saniye
Henüz bitmedi, geçen süre: 10 saniye
...
Hazır, yaklaşık 50 saniyede
https://.../indir/...
```

- `None` yazdıysa üstteki mesaja bak: `Hata: ...` ise iş başarısız; `Zaman aşımı` ise iş hâlâ sürüyor olabilir, bu
  hücreyi yeniden çalıştır (yeni ücret yok).
- Bağlantı hatasıyla hücre durursa yine aynı hücreyi çalıştır: iş numarası `is_no`'da duruyor.

---

## Adım 6 — İndir ve izle

```python
klasor = Path("videolar")
klasor.mkdir(exist_ok=True)
metin_yolu = klasor / "metinden.mp4"
```

Videolar `videolar/` klasörüne kaydedilecek (klasörü Konu 8'deki gibi `mkdir` açıyor). İlk videonun yolu `videolar/metinden.mp4`.

```python
cevap = requests.get(video_adresi, headers=basliklar, timeout=120)
print(cevap.status_code)
with open(metin_yolu, "wb") as dosya:
    dosya.write(cevap.content)

print("Kaydedildi:", metin_yolu)
```

Çıktı: `200` ve `Kaydedildi: videolar/metinden.mp4`.

- Video bu kez **base64 değil, doğrudan bayt** olarak geliyor: `cevap.content`. Konu 8'deki araçta `sdxl` de böyleydi.
- Baytları Konu 8'deki gibi `"wb"` ile yazıyoruz: **w**rite + **b**inary.
- Adım 5 `None` yazdıysa bu hücreyi çalıştırma: adres yok.

```python
Video(metin_yolu, embed=True)
```

- `Video` videoyu defterin içinde oynatır. `embed=True`: videoyu defterin içine göm; VS Code başka türlü göstermiyor.

Tasarımcı gözüyle izle:

- Yönergede "slow camera push in" (kamera yavaşça yaklaşır) yazdık. Kamera bunu yaptı mı?
- Buhar nasıl hareket ediyor? Fizik inandırıcı mı; nerede "yapay" duruyor?
- Sesi aç: model ses de üretiyor. Yönergede ses yoktu; ne duyuyorsun?

Hareket yönergesi bir **kamera dili**: yaklaşır (push in), uzaklaşır (pull out), yana kayar (pan), yukarı kalkar
(tilt up). Konu 7'deki yönerge anatomisine yeni bir katman.

---

## Adım 7 — Görselden video

Konu 9'da seçtiğin görseli videonun **ilk karesi** yapıyoruz.

```python
gorsel_yolu = Path("../09-toplu-uretim/izgara/suluboya_adacayi.jpg")
if not gorsel_yolu.exists():
    print("Konu 9'un görseli yok; yedek görseli kullanıyorum")
    gorsel_yolu = Path("veri/yedek_fincan.jpg")

print(gorsel_yolu)
```

Çıktı: Konu 9'daki görselin yolu (`izgara/suluboya_adacayi.jpg` ile biter) ya da (görsel yoksa) `Konu 9'un görseli yok; yedek görseli
kullanıyorum` ve `veri/yedek_fincan.jpg`.

- Yolda kendi kazananının adını yaz (Konu 9 Adım 6'daki `benim_secimim`). Ödevin görselleri `../09-toplu-uretim/odev9/` içinde.
- `..` bir üst klasör: defter `10-video` klasöründe çalışıyor, Konu 9'un klasörü onun yanında.
- `exists()` (Konu 9): dosya yoksa `veri/` klasöründeki yedek görsele geçiyoruz.

```python
import base64

with open(gorsel_yolu, "rb") as dosya:
    baytlar = dosya.read()
kodlu = base64.b64encode(baytlar)
metin = kodlu.decode()

uzunluk = len(metin)
print(uzunluk, "karakter")
```

Çıktı: bir karakter sayısı (yedek görselde `45216 karakter`).

- Görseli gövdeye koymak için metne çevirmemiz gerekiyor: JSON bayt taşıyamaz.
- Konu 8'de base64 **metnini** baytlara çözmüştük (`b64decode`); şimdi tersi: baytları metne (`b64encode`).
- `b64encode` sonucu yine bayt olarak verir (başında `b'`); `.decode()` onu düz metne çevirir.
- Görsel `"rb"` ile açılıyor: **r**ead + **b**inary (Konu 8).

```python
gorsel_govde = {
    "yonerge": "slow camera push in, gentle natural motion, soft morning light",
    "sure": "4",
    "oran": "16:9",
    "gorsel": metin,
}
adres = VIDEO_ADRES + "/baslat"
cevap = requests.post(adres, headers=basliklar, json=gorsel_govde, timeout=60)
print(cevap.status_code)
yanit = cevap.json()
print(yanit)
```

- Gövdeye `"gorsel"` alanı ekleniyor. Yönerge artık ne olduğunu değil, **ne olacağını** anlatıyor: sahne görselde zaten var.
- Bu hücreyi de bir kez çalıştır. `200` değilse hata metnini oku (ör. görselde bir insan yüzü varsa istek reddedilebilir).

```python
gorsel_is_no = yanit["is_no"]
video_adresi = bekle(gorsel_is_no)
```

```python
gorsel_video_yolu = klasor / "gorselden.mp4"
cevap = requests.get(video_adresi, headers=basliklar, timeout=120)
print(cevap.status_code)
with open(gorsel_video_yolu, "wb") as dosya:
    dosya.write(cevap.content)

Video(gorsel_video_yolu, embed=True)
```

- Aynı `bekle` fonksiyonu, yeni iş numarasıyla; sonra Adım 6'nın indirmesi, yeni dosya adıyla.

İlk kareyi Konu 9'daki görselle karşılaştır:

- Kompozisyon korundu mu? Stil (suluboya, linol...) hareket boyunca korundu mu, yoksa video "fotoğrafa" mı kaydı?
- Kare görsel yatay videoya nasıl sığdı: kırpıldı mı, kenarlar uyduruldu mu?
- Hangi görseller harekete uygun? Derinliği, boşluğu, yön veren çizgileri olanlar mı; düz bir afiş mi?

---

## Adım 8 — Üretim günlüğü

Konu 9'daki gibi her videonun nasıl üretildiğini kaydediyoruz; bu kez **maliyet** de kayıtta.

```python
metin_kaydi = {
    "dosya": str(metin_yolu),
    "gorsel": "yok",
    "yonerge": govde["yonerge"],
    "model": "gemini-omni-1.1-flash",
    "sure": govde["sure"],
    "oran": govde["oran"],
    "cozunurluk": "720p",
    "is_no": is_no,
    "maliyet_usd": 4 * UCRET_SANIYE,
}
gorsel_kaydi = {
    "dosya": str(gorsel_video_yolu),
    "gorsel": str(gorsel_yolu),
    "yonerge": gorsel_govde["yonerge"],
    "model": "gemini-omni-1.1-flash",
    "sure": gorsel_govde["sure"],
    "oran": gorsel_govde["oran"],
    "cozunurluk": "720p",
    "is_no": gorsel_is_no,
    "maliyet_usd": 4 * UCRET_SANIYE,
}
kayitlar = [metin_kaydi, gorsel_kaydi]
```

- Her video bir sözlük. `str(...)`: yol bir `Path`; JSON onu yazamaz, metne çeviriyoruz.
- Gövdeyi olduğu gibi kaydetmiyoruz: içinde görselin on binlerce karakterlik base64 metni var.
- `maliyet_usd`: 4 saniye × 0,10 = 0,4.

```python
import json

toplam_ucret = 0
for kayit in kayitlar:
    toplam_ucret = toplam_ucret + kayit["maliyet_usd"]
print("Bu defterin videoları:", toplam_ucret, "USD")

with open("video_gunlugu.json", "w", encoding="utf-8") as dosya:
    json.dump(kayitlar, dosya, ensure_ascii=False, indent=2)
print("Günlük yazıldı")
```

Çıktı: `Bu defterin videoları: 0.8 USD` ve `Günlük yazıldı`.

- Toplam Konu 1'in sayacıyla; günlük Konu 9'daki `json.dump` ile (`ensure_ascii=False`, `indent=2`).
- Sınıfın tamamı bu defteri çalıştırınca 12 öğrenci × 0,80 = yaklaşık 10 dolar. Görselde aynı para 15.000 görsel ederdi.

---

## Bonus

**1. Dikey video (bir klip daha; klip hakkın varsa).** Aynı yönerge, 9:16 (telefon, hikâye):

```python
dikey_govde = {
    "yonerge": govde["yonerge"],
    "sure": "4",
    "oran": "9:16",
}
cevap = requests.post(adres, headers=basliklar, json=dikey_govde, timeout=60)
yanit = cevap.json()
print(yanit)
```

```python
dikey_is_no = yanit["is_no"]
video_adresi = bekle(dikey_is_no)

dikey_yolu = klasor / "dikey.mp4"
cevap = requests.get(video_adresi, headers=basliklar, timeout=120)
with open(dikey_yolu, "wb") as dosya:
    dosya.write(cevap.content)

Video(dikey_yolu, embed=True)
```

Kompozisyon yeniden nasıl kuruldu? Fincan nerede duruyor, ne kırpıldı? Fiyat değişmedi: oran fiyatı etkilemiyor, süre etkiliyor.

**2. İş numarasıyla yeniden sor (ücretsiz).** Adım 4'teki işin numarası `is_no`'da duruyor:

```python
tekrar = bekle(is_no)
print(tekrar)
```

Çıktı: hiç `Henüz bitmedi` yok; `Hazır, yaklaşık 0 saniyede` ve aynı video adresi. İş çoktan bitti; yeni bir iş başlamadı,
yeni bir ücret yok. Konu 9'daki "kaldığı yerden devam"ın video hâli.

**3. Yardımcı dosyayı oku.** `video.py`'deki `video_uret` bugün yazdığın her şeyi tek fonksiyonda yapıyor: dosya zaten
varsa hiç istek göndermiyor, başlatıyor, bekliyor (bağlantı koparsa bırakmıyor, biraz sonra yeniden soruyor), indiriyor.
Konu 11'de üretim hattının son halkası bu fonksiyon olacak.

---

## Defterin bölümleri

| Adım | Ne yaptık | Elimizde ne oluştu | Anahtar |
|---|---|---|---|
| Isınma | Maliyet hesabı: süre ve fiyat, yarı fiyatına, video ile görsel | `UCRET_SANIYE` | gerekmez |
| 1 | Arayüzden bir klip | (kendi hesabında bir video) | kendi hesabın |
| 2 | Sahte işle başlat, sor, bekle, zaman aşımı | `govde` | gerekmez |
| 3 | Video kodunu oku | `VIDEO_ADRES`, `basliklar` | gerekir |
| 4 | Gerçek işi başlat | `is_no` | gerekir |
| 5 | Aralıklarla sor | `bekle`, `video_adresi` | gerekir |
| 6 | İndir ve izle | `videolar/metinden.mp4` | gerekir |
| 7 | Görselden video | `videolar/gorselden.mp4` | gerekir |
| 8 | Üretim günlüğü, toplam maliyet | `video_gunlugu.json` | gerekmez |
| Bonus | Dikey video; iş numarasıyla yeniden sor | `videolar/dikey.mp4` | gerekir |

Derste kendi başına çalışacağın defter: `alistirma.ipynb`. Önce aynı klasörde yeni bir adla kopyala,
kopyada çalış. **Anahtar istemez, internete çıkmaz, klip üretmez:** dersteki sahte işle çalışıyor. İki bölümü var:

- **Bozuk kodlar:** beş kısa hücre, birbirinden bağımsız. Üçü hata mesajı veriyor, ikisi sessizce yanlış çalışıyor.
- **Kendi başına:** `BOSLUK` yazan yerleri doldurduğun altı soru ve bir ek soru (bekleme döngüsünü kendin kurmak).

---

## Sık karşılaşılan hatalar ve mesajlarını okumak

| Ne görüyorsun | Sebebi | Ne yapmalı |
|---|---|---|
| `ModuleNotFoundError: No module named 'video'` | Defterin kopyası konu klasörünün dışında | Kopya `video.py`'nin yanında, `10-video` klasöründe olmalı |
| `FileNotFoundError: ... '../anahtar.txt'` (Adım 3) | Anahtar dosyası yok ya da yanlış yerde | `gita3111` klasöründe durmalı |
| `KeyError: 'VIDEO_ADRES'` ya da `KeyError: 'VIDEO_KOD'` | `anahtar.txt`'ye iki yeni satır eklenmemiş ya da `=` yerine `:` yazılmış | İki satırı `AD = değer` biçiminde ekle, Adım 3'ü yeniden çalıştır |
| `NameError: name 'time' is not defined` (Adım 5) | Adım 2'nin ilk hücresi çalıştırılmadı (`import time` orada) | Adım 2'yi çalıştır |
| `401` ve `{'hata': ...}` (Adım 4) | Video kodu yanlış | `anahtar.txt`'deki `VIDEO_KOD` satırını hocanın verdiğiyle karşılaştır, Adım 3'ü yeniden çalıştır |
| `429` ve `{'hata': ...}` (Adım 4) | Klip hakkın doldu | Hocaya yaz; yeni iş başlatma |
| `KeyError: 'is_no'` | `/baslat` başarısız oldu; yanıtta iş numarası değil hata var | Üstteki hücrenin yazdığı hata metnini oku |
| Hep `Henüz bitmedi`, sonunda `Zaman aşımı` | İş 6 dakikadan uzun sürdü (yoğun saat) | Yeni iş başlatma; `video_adresi = bekle(is_no)` hücresini yeniden çalıştır |
| `Hata: ...` (bekle içinde) | Model işi reddetti ya da bir sorun çıktı (ör. görselde insan yüzü) | Yönergeyi ya da görseli değiştirip yeni iş başlat |
| `requests.exceptions.ConnectionError` ya da `ReadTimeout` | İnternet koptu ya da aracı hizmet cevap vermedi | İnternete bak; aynı hücreyi yeniden çalıştır. İş sunucuda sürüyor, iş numaran elinde |
| `requests.exceptions.JSONDecodeError` | Aracı hizmet JSON yerine başka bir şey döndürdü (ör. bakımda) | Durum kodunu yazdır; birkaç dakika sonra yeniden dene, sürerse hocaya yaz |
| `MissingSchema: Invalid URL 'None'` (Adım 6) | Adım 5 `None` döndürdü; indirilecek adres yok | Önce Adım 5'teki mesaja bak |
| Video oynamıyor, boş bir kutu | `embed=True` yazılmamış ya da dosya boş | `Video(yol, embed=True)`; indirmenin durum kodu `200` mü? |
| `FileNotFoundError` (Adım 7, `open`) | Görsel yolu yanlış ve yedeğe geçilmedi | Yol hücresini yeniden çalıştır; yazdığı yola bak |
| `Konu 9'un görseli yok; yedek görseli kullanıyorum` | Konu 9'un görseli o adla yok | Kendi görselin istiyorsan dosya adını Konu 9'daki gibi yaz |
| `TypeError: write() argument must be str, not bytes` | Dosya `"w"` ile açılmış | Baytlar için `"wb"` |
| `TypeError: can't multiply sequence by non-int of type 'float'` | `"4" * 0.10`: süre metin | Önce sayıya çevir: `int(sure)` |
| `0.6000000000000001` | Bilgisayarın ondalık hesabındaki küçük kalıntı (6 × 0,10) | 0,60 oku; sorun değil |
| Aynı videodan iki tane, iki ücret | `/baslat` hücresi iki kez çalıştırıldı | Başlatma hücrelerini bir kez çalıştır; beklemek için yalnızca `bekle` hücresini yinele |

---

## Kendini dene

Cevaplar notun en sonunda. Önce kendin düşün.

1. 30 saniyelik bir tanıtım: en az kaç klip, kaç dolar? Bütçen 2 dolarsa en fazla kaç saniyelik bir tanıtım yapabilirsin?
2. Bekleme döngüsünde `time.sleep(10)`'u silersen ne olur? Video daha mı çabuk gelir?
3. Bir arkadaşın `sahte_baslat` (gerçekte `/baslat` isteği) satırını döngünün içine yazdı. Gerçek hizmette ne olur?
4. `bekle` "Zaman aşımı" dedi. Ne yaparsın, ne yapmazsın?
5. `range(36)` ile `timeout=30` arasındaki fark ne?
6. Görselden video için hangi görselini seçerdin: düz renkli, ortalanmış bir logo mu, derinliği olan bir masa sahnesi mi? Neden?
7. Günlüğe neden maliyet de yazdık?

---

## Bu konuda öğrendiklerin

- **Maliyet.** Video saniye başına ücretli; çözünürlük kilitliyken fiyatı süre belirler, oran belirlemez. Bir klip yüzlerce görsel eder.
- **Uzun süren iş.** Başlat → iş numarasını sakla → aralıklarla sor (`time.sleep`) → bitince indir.
- **Zaman aşımı.** Döngünün sınırı bütün bekleyişin sınırıdır; işi iptal etmez. `timeout` ise tek bir isteğin sınırı.
- **`requests.get`.** Gövdesiz istek: "bana şunu ver". Durum sormak ve indirmek için.
- **Görselden video.** Görsel base64 metni olarak gövdeye girer (`b64encode` + `decode`); ilk kare olur.
- **Kamera dili.** Hareket yönergesi: yaklaşma, uzaklaşma, yana kaydırma, yukarı kalkış; öznenin hareketi ayrı yazılır.
- **Günlük ve bütçe.** Her videonun ayarları ve maliyeti kayıtta.

## Bu konunun tek cümlesi

> Video hemen dönmez: isteği başlatırsın, iş numarasını saklarsın, bir sınıra kadar arada bir sorarsın, bitince
> indirirsin; ve her saniyenin bir fiyatı olduğu için her ayar bir bütçe kararıdır.

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **Uzun süren iş (asenkron iş)** | Sonucu istekle aynı anda gelmeyen iş; başlatılır, sonra sorulur |
| **İş numarası** | Başlatılan işin kimliği; durumu sormak ve sonucu almak için saklanır |
| **Aralıklarla sormak (polling)** | "Bitti mi?" sorusunu belli aralıklarla tekrarlamak |
| **Zaman aşımı** | Beklemeye konan üst sınır; aşılınca beklemek bırakılır, iş iptal olmaz |
| **`time.sleep(10)`** | Programı 10 saniye bekletmek |
| **`requests.get`** | Gövdesiz istek: bir şeyi almak (durum, dosya) |
| **Aracı hizmet (proxy)** | İsteği alıp başka bir hesapla asıl hizmete ileten ara sunucu |
| **Video kodu** | Aracı hizmetin seni tanıdığı kişisel kod; Gemini anahtarı değil |
| **Çözünürlük** | Görüntünün piksel boyutu: 720p (1280 × 720), 1080p (1920 × 1080); dersin aracı hizmeti 720p'ye kilitli |
| **Oran** | Genişlik : yükseklik; 16:9 yatay, 9:16 dikey |
| **Görselden video** | Verilen görselin ilk kare olduğu video üretimi |
| **Kamera dili** | Kameranın hareketini anlatan terimler: push in, pull out, pan, tilt |
| **`cevap.content`** | Yanıtın ham baytları (video gibi) |

## Ödev

`odevler/odev10.md` (puansız): Konu 9 ödevindeki görsellerinden birini videoya çevir; videoyu ve günlüğü getir.
Görsel hareket edince ne korundu, ne bozuldu? Aynı klip 8 saniye olsaydı kaç dolar tutardı?

## Sonraki konu

**Konu 11 — Zincirleme: üretim hattı.** Şimdiye kadar her şeyi ayrı ayrı ürettik: metin (Konu 5), görsel (Konu 8–9),
video (bugün). Konu 11'de bunları tek bir programda birbirine bağlıyoruz: bir adımın çıktısı ötekinin girdisi. Video,
hattın son (isteğe bağlı) ve en pahalı halkası; bugünkü "bir kez başlat, numarayı sakla" kuralı orada da geçerli.

---

## Kendini dene — cevaplar

1. 30 = 8 + 8 + 8 + 6: en az **4 klip**; 30 × 0,10 = **3 dolar** (yaklaşık). 2 dolarla en fazla **20 saniye** (ör. 8 + 8 + 4):
   bütçeyi süre belirliyor.
2. Video daha çabuk gelmez: işin süresi senin ne sıklıkla sorduğuna bağlı değil. Döngü 36 soruyu birkaç saniyede bitirir ve
   iş bitmeden "zaman aşımı" der. Sunucuyu da gereksiz yere yorar.
3. Her turda **yeni bir iş** başlar: yeni bir klip, yeni bir ücret. Hiçbiri beklenmediği için hiçbiri indirilmez; klip hakkı
   birkaç turda biter. Başlatma döngünün **dışında**, bir kez.
4. Yeni iş başlatmazsın. İş numarası elinde: bir süre sonra `bekle(is_no)` ile yeniden sorarsın. Zaman aşımı işi iptal etmedi.
5. `timeout=30` **tek bir isteğin** cevabı için en fazla 30 saniye bekler. `range(36)` (her turda 10 saniye) **bütün bekleyişi**
   en fazla yaklaşık 6 dakikayla sınırlar.
6. Kendine. Derinliği, boşluğu, hareket edebilecek bir öğesi (buhar, yaprak, su) olan sahne kamera hareketine daha çok yer
   bırakır; düz, ortalanmış bir logo hareket edince ya hiç değişmez ya da bozulur.
7. Video ücretli: kampanyanın kaça mal olduğunu bilmek, bütçeyi aşmamak ve müşteriye teklif vermek için. Konu 9'daki gibi
   aylar sonra "aynısını üret" denirse ayarlar ve maliyet kayıtta.
