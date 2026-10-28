# Konu 9 — Video Üretimi

Bu not konunun özetidir; derste çalıştırdığımız `ders.ipynb` defteriyle **aynı sırada**
ilerler: Isınma, sonra Adım 1–6 ve kısa bir Bonus. Derste kaçırdığın bir yer olursa
buradan oku, sonra defterde o adımın hücrelerini çalıştır. Nottaki kod blokları
defterdeki hücrelerin birebir aynısı. Arayüzde yapılacakların hepsi de burada, adım adım.

**Konu 8'de:** görselleri koddan ve toplu olarak ürettik; her görsel birkaç saniyede geldi.
**Bu konuda:** görsele zaman ekliyoruz. Videoyu **arayüzden** üretiyoruz; kodu iki soruyu cevaplamak için yazıyoruz:

> 1. Aynı klibi ücretli bir API'yle koddan üretseydin kaça mal olurdu? Süre ve çözünürlük bedeli nasıl değiştirir, hangi ayar
>    onu yarıya indirir?
> 2. Ürettiğin her klibin yönergesi ve ayarları nerede kayıtlı?

**Neden arayüz?** Görselde kullandığımız Cloudflare'in kataloğunda video modeli yok. Google'ın video API'sinin de ücretsiz
katmanı yok: koddan video üretmek her saniye için para ödemek demek. Bazı arayüzlerin ise ücretsiz bir günlük kredisi var.

**Konunun sonunda elinde:** `videolar/` klasöründe iki kısa video (biri yalnız yönergeden, biri Konu 8'deki bir görselinden) ve
her klibin nasıl üretildiğini kaydeden bir günlük (`video_gunlugu.json`).

**Kurulum:** yeni kütüphane yok. `git pull` ile konu klasörü geldikten sonra `gita3111` klasöründe
bir kez `uv sync` çalıştır.

**Anahtar:** gerekmez. Defter internete de çıkmaz. Arayüz için kişisel bir Google hesabın gerekiyor (aşağıda).

> **Bu nottaki çıktılar hakkında.** Defterin hesap çıktıları her bilgisayarda aynıdır. Videolar, bekleme süreleri ve kredi
> sayıları arayüzden gelir; senin ekranında farklı olabilir.

---

## Hangi arayüz?

Derste **Google Flow** kullanıyoruz (Google'ın video ve görsel üretme aracı, tarayıcıda çalışır).

- **Ücretsiz:** Google'ın kredi sayfasına göre aboneliği olmayan kullanıcıya da her gün **50 kredi** veriliyor. Kullanmadığın
  kredi ertesi güne geçmez. Kalan kredini görmek için Flow'da sağ üstteki profil resmine tıkla.
- **Harcanan kredi süreye ve çözünürlüğe göre değişir.** Aynı sayfaya göre (28 Ekim 2026) Gemini Omni Flash modeliyle 720p bir
  klip 4 saniyede 7, 6 saniyede 10, 8 saniyede 12, 10 saniyede 15 kredi tutuyor. Derste iki klip üretiyoruz (8 + 6 saniye):
  22 kredi. Ödeve de kredi kalır; istersen ödevi ertesi gün yaparsın. Üretim başarısız olursa kredi düşmez.
- **Kimler kullanabilir:** 18 yaş ve üstü (yaşını doğrulaman istenebilir); Türkiye desteklenen ülkeler arasında. Kişisel bir
  Google hesabıyla gir (okulun verdiği hesap kısıtlı olabilir).
- **Tarayıcı:** bilgisayarda Chrome ya da Edge. Google bunları öneriyor; başka tarayıcıda ve telefonda sorun çıkabilir.
- **Yoğun saat:** aboneliği olmayan kullanıcılar Türkiye saatiyle yaklaşık **17.00–20.00** arasında video üretemeyebilir.
  O saatlerde "şu an üretilemiyor" gibi bir uyarı görürsen sonra dene.
- **Kart:** hesap açarken ya da kredi kullanırken kart bilgisi istenirse **girme**; Flow abone olmanı isterse abone olma.
  İki durumda da hocaya yaz.

**Flow açılmazsa:** hocanın derste söyleyeceği yedek arayüzü kullan. Hangi araç olursa olsun kural aynı: kayıtta kart bilgisi
isteyen bir "ücretsiz" araca kart girme.

**Google AI Plus öğrenci teklifi:** ders bu teklife dayanmıyor. Teklif kayıt sırasında bir ödeme yöntemi istiyor ve süresi
bitince iptal edilmezse aylık ücretli aboneliğe dönüşüyor.

---

## Isınma: bir klip kaç kare?

Video art arda gelen karelerden oluşur. Sinema filmi saniyede 24 kare gösterir; göz kareleri ayrı ayrı değil, hareket olarak görür.

```python
kare_hizi = 24
sure = 8
kare = sure * kare_hizi
print(sure, "saniye:", kare, "kare")
```

Çıktı:

```
8 saniye: 192 kare
```

Video modeli bu 192 kareyi tek tek değil, birbirini **tutacak** biçimde birlikte kurar: bir fincan kare kare şekil
değiştirmemeli, ışık bir anda zıplamamalı. Konu 8'de bir görsel birkaç saniyede geliyordu; 192 tutarlı kareyi kurmak dakikalar
sürebilir. Videonun görselden hem yavaş hem pahalı olmasının nedeni bu.

---

## Adım 1 — Arayüzde ilk klip: başlat ve bırak

Aşağıdaki adımlar Google'ın Flow yardım sayfalarından alındı. Tıklayacağın düğmelerin adları, arayüzün İngilizce hâlindeki gibi
**kalın** yazılı; arayüz Türkçe açılırsa Türkçe karşılıklarını ara. Arayüz sık değişiyor: bir düğme yerinde değilse ya da adı
farklıysa derste ilk denemede birlikte bakacağız.

**İlk kez: Flow'a gir, proje aç**

1. Tarayıcıda `labs.google/fx/tools/flow` adresine git.
2. Kişisel Google hesabınla giriş yap. Kullanım şartlarını onaylaman istenebilir.
3. **+ New project** (yeni proje) düğmesine tıkla; daha önce bir proje açtıysan ona da tıklayabilirsin.

**Metinden klip**

1. Projedeki yönerge kutusuna (prompt box) şu İngilizce yönergeyi yapıştır (Konu 7: modeller çoğunlukla İngilizce metinle
   eğitildi):

   > steam rising from a ceramic coffee cup on a wooden desk, soft morning light, slow camera push in

2. Yönerge kutusundaki **model adına** tıkla. Flow açılışta bir görsel modeliyle gelir (adında "Nano Banana" geçer);
   **Video**'ya geç.
3. Video ayarlarını seç:
   - En-boy oranı (aspect ratio): **16:9**
   - Çıktı sayısı (number of outputs): **1** (her çıktı ayrı kredi yer)
   - Model: **Gemini Omni Flash**, çözünürlük **720p** (yardım sayfasındaki adıyla; listede yoksa derste birlikte seçeceğiz).
     360p ("draft", taslak) seçeneği de olabilir; yaklaşık yarısı kadar kredi yer, ama derste 720p kullanıyoruz. Veo 3.1 Quality
     gibi modeller bir klip için 100 kredi ister; günlük 50 kredin yetmez.
   - Süre (generation length): **8 saniye**

   Model, çözünürlük ve kredi değeri yönerge kutusunun sağ üstündeki ayarlarda (**Settings**) görünür. Üretmeden önce bir bak:
   8 saniyelik klip 12 kredi tutmalı.
4. **Generate** (üret) düğmesine bas. Düğmede yazı yerine yalnızca bir simge olabilir.
5. Klip hemen gelmez. Sekmeyi açık bırak, deftere dön ve **Adım 2**'ye geç; arayüz işi arka planda sürdürüyor.

**Sohbete yaz:** düğmeye bastığında ekranda ne gördün: bir yükleme çubuğu mu, bir yüzde mi, bir mesaj mı, yoksa hiçbir şey mi?

Buna **uzun süren iş** denir: isteği başlatırsın, başka bir işe geçersin, sonuç hazır olunca dönersin. Kuru temizlemeciye ceketini
bırakıp karşılığında fiş almak gibi. Arayüz "bitti mi?" sorusunu senin yerine soruyor; koddan üretimde bunu programcı yazar.

Yönergeyi bir yere kopyala: Adım 6'da günlüğe yazacağız.

---

## Adım 2 — Bir saniye kaç dolar?

Arayüzde para ödemiyorsun; klip ücretsiz kredinle üretiliyor. Aynı klibi **koddan**, ücretli bir video API'siyle üretseydin her
saniyesi için para öderdin. Google'ın resmi fiyat sayfasında (28 Ekim 2026) saniye fiyatı **çözünürlüğe** göre değişiyor. Fiyatları
bir sözlüğe koyuyoruz: anahtar çözünürlük, değer bir saniyenin yaklaşık fiyatı (dolar).

```python
fiyatlar = {
    "360p": 0.034,
    "720p": 0.101,
    "1080p": 0.152,
    "4K": 0.304,
}

sure = 8
fiyat = fiyatlar["720p"]
ucret = sure * fiyat
print(sure, "saniye, 720p:", ucret, "USD")
```

Çıktı:

```
8 saniye, 720p: 0.808 USD
```

Python ondalık sayıyı virgülle değil **noktayla** yazar: `0.101`. Sözlükten değeri anahtarla alıyoruz: `fiyatlar["720p"]`.
Anahtar birebir aynı yazılmalı: `"720P"` (büyük P) sözlükte olmayan başka bir anahtardır; `KeyError` alırsın.

Çözünürlük, görüntünün piksel boyutudur: 720p 1280 × 720, 1080p 1920 × 1080, 4K 3840 × 2160 piksel. 4K, 1080p'nin **dört katı**
piksel: eni de boyu da iki katı. Fiyatı kaç katı?

```python
kat = fiyatlar["4K"] / fiyatlar["1080p"]
print("4K, 1080p'nin", kat, "katı fiyat")
```

Çıktı:

```
4K, 1080p'nin 2.0 katı fiyat
```

İki katı. Fiyat piksel sayısıyla aynı hızda artmıyor; ama her basamak yine de fiyatı belirgin biçimde artırıyor. Asıl soru "en
yüksek kalite hangisi?" değil, "bu klip **nerede** izlenecek?" Çoğu telefon ekranı 4K değil; 4K'nın fazladan pikselleri orada
görünmez, faturada görünür.

---

## Adım 3 — 20 saniyelik tanıtım: hangi ayar bedeli yarıya indirir?

Bir kafe 20 saniyelik bir tanıtım videosu istiyor ve "4K olsun" diyor. Model tek seferde birkaç saniyelik bir klip üretir;
20 saniyelik video, birkaç klibin kurguda birleşmesiyle çıkar. Hesap için toplam süre yeter.

```python
sure = 20
cozunurluk = "4K"
fiyat = fiyatlar[cozunurluk]
ucret = sure * fiyat
print(sure, "saniye,", cozunurluk, ":", ucret, "USD")
```

Çıktı:

```
20 saniye, 4K : 6.08 USD
```

Bu kez anahtarı bir değişkenden aldık: `fiyatlar[cozunurluk]`. Değişkenin içinde `"4K"` var; sözlük ona bakıyor.

Kafenin bütçesi bunun **yarısı**: 3,04 dolar. Önce süreye dokunmadan her çözünürlükte 20 saniyenin bedeline bakıyoruz.
Sözlüğün üstünde dönen bir `for` döngüsü **anahtarları** sırayla verir (Konu 4'teki `for kelime in harita:` gibi); değeri
döngünün içinde anahtarla alıyoruz. `round(..., 2)` noktadan sonra iki basamak bırakır (Konu 3).

```python
for cozunurluk in fiyatlar:
    fiyat = fiyatlar[cozunurluk]
    ucret = round(sure * fiyat, 2)
    print(cozunurluk, ":", ucret, "USD")
```

Çıktı:

```
360p : 0.68 USD
720p : 2.02 USD
1080p : 3.04 USD
4K : 6.08 USD
```

4K'dan 1080p'ye inince süre aynı kalıyor, fiyat yarıya iniyor. Tersini deneyelim: çözünürlük 4K kalsın, süre kısalsın. Bütçeyi
(3,04 dolar) bir değişkene koyuyoruz, her sürenin bedelini onunla karşılaştırıyoruz.

```python
butce = 3.04
sureler = [5, 10, 15, 20]
fiyat = fiyatlar["4K"]
for sure in sureler:
    ucret = round(sure * fiyat, 2)
    if ucret <= butce:
        print(sure, "saniye, 4K:", ucret, "USD, bütçeye sığıyor")
    else:
        print(sure, "saniye, 4K:", ucret, "USD, bütçeyi aşıyor")
```

Çıktı:

```
5 saniye, 4K: 1.52 USD, bütçeye sığıyor
10 saniye, 4K: 3.04 USD, bütçeye sığıyor
15 saniye, 4K: 4.56 USD, bütçeyi aşıyor
20 saniye, 4K: 6.08 USD, bütçeyi aşıyor
```

`<=` "küçük ya da eşit" demek: tam 3,04 dolar da bütçeye sığar. Yarı bütçeyle iki yol var: **20 saniye 1080p** ya da **10 saniye
4K**. Hangisi? Tanıtım nerede gösterilecek: telefonda, kafenin ekranında, sinema perdesinde? 10 saniyeye inersen hangi çekimleri
atardın? Bu bir tasarım kararı; hesap yalnızca seçenekleri önüne koyuyor.

Bu hesap kaç kez denediğini saymıyor. Videoda ilk deneme çoğu zaman istediğin gibi olmaz; üç deneme yaparsan aynı 20 saniyenin
faturası üç katına çıkar. Bu yüzden önce kısa ve düşük çözünürlükte dene, beğendiğini büyüt.

---

## Adım 4 — Klibe dön: izle ve değerlendir

Arayüze dön. Klip hazırsa projede bir kutucuk olarak görünür; fareyle üstüne gel ya da tıkla ve izle. Kutucuk hâlâ boşsa ya
da üstünde "Pending" (bekliyor) yazıyorsa biraz bekle; klip hiç görünmüyorsa sayfayı yenile. Ama **Generate**'e yeniden basma:
yeni bir iş başlar, yeniden kredi düşer.

**İndir ve yerine koy**

1. Fareyle klibin üstüne gel, sağ üst köşedeki üç noktaya (**More**) tıkla, sonra **Download**'a (indir) tıkla. Dosya türü
   sorulursa videoyu seç; **270p** seçeneği hareketli bir GIF verir, onu seçme.
2. Tarayıcı dosyayı İndirilenler klasörüne koyar. VS Code'un sol panelinde `09-video` klasörüne sağ tıkla, **New Folder**'ı
   (yeni klasör) seç, adını `videolar` yap.
3. Bilgisayarının dosya gezgininde İndirilenler klasörünü aç, indirdiğin dosyayı VS Code'daki `videolar` klasörünün üstüne sürükle.
   Sonra VS Code'da dosyaya sağ tıkla, **Rename**'i (yeniden adlandır) seç, adını `metinden.mp4` yap. Dosyanın yeri:
   `09-video/videolar/metinden.mp4`.

`videolar/` klasörü depoya girmez; `git pull` onu etkilemez.

**Tasarımcı gözüyle izle ve sohbete yaz:**

- Yönergede "slow camera push in" (kamera yavaşça yaklaşır) yazdık. Kamera bunu yaptı mı?
- Buhar nasıl hareket ediyor? Nerede inandırıcı, nerede "yapay" duruyor?
- Klipte ses var mı? Yönergede ses yoktu; ne duyuyorsun, sen ne isterdin?
- **Generate**'e bastıktan kaç saniye sonra geldi? Kaç kredi harcandı (sağ üstteki profil resmine tıkla)?

Kameranın hareketi için sinemadan gelen terimler var; bunlara **kamera dili** diyoruz: yaklaşma (push in), uzaklaşma (pull out),
yana dönüş (pan), yukarı dönüş (tilt up), sabit çekim (static shot). Kamera dili, Konu 7'deki yönerge anatomisine yeni bir katman
ekler.

---

## Adım 5 — Görselden klip

Konu 8'de ürettiğin görsellerden birini videonun **ilk karesi** yapıyoruz. Görselin yoksa bu klasördeki `veri/yedek_fincan.jpg`'yi
kullan (masada bir fincan, kare). Görselde gerçek bir kişinin yüzü olmasın: istek reddedilebilir.

Görselin kare (1:1), video yatay (16:9). **Üretmeden önce tahmin et, sohbete yaz:** model kenarları ne yapacak? Görseli
kırpacak mı, kenarlara yeni bir şey mi ekleyecek? Cevap birazdan senin klibinde.

**Arayüzde**

1. Aynı projede yönerge kutusundaki model adına tıkla, **Video**'yu, sonra **Frames**'i (kareler) seç.
2. Bilgisayarının dosya gezgininde görselini bul ve **+ Add start frame** (başlangıç karesi ekle) kutusuna sürükle. Konu 8'in
   görselleri `gita3111` içindeki `08-koddan-toplu-uretim` klasöründe: `izgara/`, `ciktilar/` ya da ödevinin `odev8/` klasörü.
   Yanındaki **+ Add end frame** videonun son karesi içindir; onu boş bırak. Kutuya tıklayınca dosya seçme penceresi de açılabilir;
   derste ilk denemede bakacağız.
3. Yönerge kutusuna **ne olacağını** yaz; sahne görselde zaten var. Örnek:

   > slow camera push in, gentle natural motion, soft morning light

4. Ayarlar Adım 1'deki gibi: **16:9**, çıktı sayısı **1**, Omni Flash **720p**; yalnızca süre **6 saniye** (10 kredi). Flow,
   seçtiğin özelliği desteklemeyen bir modelden kendiliğinden başka bir modele geçebiliyor; üretmeden önce ayarlarda model ve
   kredi değerine bir daha bak. Sonra **Generate**'e bas.
5. Beklerken deftere dön: Adım 6'nın ilk hücresiyle ilk klibin kaydını yaz.
6. Klip gelince indir ve Adım 4'teki gibi `videolar/gorselden.mp4` olarak kaydet.

**Klip gelince karşılaştır ve sohbete yaz:**

- Tahminin tuttu mu: görsel kırpıldı mı, kenarlara yeni bir şey mi eklendi?
- Kompozisyon yerinde kaldı mı? Stil (suluboya, linol, düz vektör...) hareket boyunca korundu mu, yoksa video "fotoğrafa" mı kaydı?
- Hangi görseller harekete uygun: derinliği, boşluğu, hareket edebilecek bir öğesi (buhar, yaprak, su) olanlar mı, düz bir afiş mi?

---

## Adım 6 — Video günlüğü

Konu 8'de her görselin nasıl üretildiğini bir JSON günlüğüne yazmıştık. Arayüzde de bu alışkanlığı sürdürüyoruz: aylar sonra biri
"şunun bir benzerini yapalım" derse yönerge ve ayarlar elinde olmalı. Arayüzün geçmişi senin dosyan değil; kredi biter, araç
değişir, hesap kapanır.

`input` (Konu 8'de de kullandın) ekranın üstünde bir kutu açar; yazdığını **metin** olarak verir, Enter'a basınca hücre devam
eder. Yönergeyi arayüzden kopyalayıp kutuya yapıştır.

```python
yonerge = input("Metinden klibin yönergesi: ")
begendim = input("Beğendin mi? (evet / kısmen / hayır): ")

metin_kaydi = {
    "tur": "metinden",
    "arac": "Google Flow",
    "yonerge": yonerge,
    "gorsel": "yok",
    "sure": 8,
    "cozunurluk": "720p",
    "oran": "16:9",
    "dosya": "videolar/metinden.mp4",
    "begendim": begendim,
}
print(metin_kaydi)
```

Süreyi, çözünürlüğü ve oranı arayüzde seçtiklerinle aynı yap. Süre **sayı** (tırnaksız): Adım 6'nın son hücresinde onunla
çarpma yapacağız. Çözünürlük fiyat sözlüğündeki gibi yazılır (`"720p"`): sözlükte anahtar olarak aranacak. Oran arayüzdeki gibi
(`"16:9"`); hesaba girmiyor ama klibin nasıl göründüğünü belirliyor. Başka bir arayüz kullandıysan `"arac"` değerini değiştir.

Görselden klibin kaydı aynı kalıpta. `"gorsel"` alanına kullandığın görselin yolunu yaz. Konu 8'deki bir görselse yol
klasörün adıyla başlasın, ör. `"08-koddan-toplu-uretim/izgara/suluboya_gece.jpg"`.

```python
yonerge = input("Görselden klibin yönergesi: ")
begendim = input("Beğendin mi? (evet / kısmen / hayır): ")

gorsel_kaydi = {
    "tur": "gorselden",
    "arac": "Google Flow",
    "yonerge": yonerge,
    "gorsel": "veri/yedek_fincan.jpg",
    "sure": 6,
    "cozunurluk": "720p",
    "oran": "16:9",
    "dosya": "videolar/gorselden.mp4",
    "begendim": begendim,
}
print(gorsel_kaydi)
```

İki kaydı bir listeye koyup dosyaya yazıyoruz. `ensure_ascii=False` Türkçe harfleri olduğu gibi yazar, `indent=2` dosyayı
okunur kılar.

```python
import json

kayitlar = [metin_kaydi, gorsel_kaydi]
with open("video_gunlugu.json", "w", encoding="utf-8") as dosya:
    json.dump(kayitlar, dosya, ensure_ascii=False, indent=2)

sayi = len(kayitlar)
print(sayi, "kayıt video_gunlugu.json dosyasına yazıldı")
```

`video_gunlugu.json`'u VS Code'da aç: her klip bir sözlük, ikisi bir listede.

Son olarak günlüğü geri okuyup soruyoruz: bu klipler ücretli bir API'yle koddan üretilseydi kaça mal olurdu? Her kaydın
çözünürlüğü, fiyat sözlüğünde bir anahtar olarak duruyor. Çözünürlüğü önce bir değişkene alıyoruz, sonra fiyatı onunla
buluyoruz; böylece her satır tek bir iş yapıyor.

```python
with open("video_gunlugu.json", encoding="utf-8") as dosya:
    okunan = json.load(dosya)

toplam = 0
for kayit in okunan:
    cozunurluk = kayit["cozunurluk"]
    fiyat = fiyatlar[cozunurluk]
    ucret = kayit["sure"] * fiyat
    toplam = toplam + ucret

toplam = round(toplam, 2)
print("Bu klipler ücretli bir API'yle:", toplam, "USD")
```

Defterdeki değerlerle (8 ve 6 saniye, 720p) çıktı:

```
Bu klipler ücretli bir API'yle: 1.41 USD
```

Kendi süre ve çözünürlüğünü yazdıysan senin sayın farklı olabilir. Az bir para gibi görünüyor, ama bu yalnızca **iki klip**:
her biri tek denemede, tek bir kişi için. Bugün sıfır bütçeyle video yapabiliyoruz, çünkü arayüzün ücretsiz günlük kredisi var.
Kredi bitince ya ertesi günü beklersin ya da ödersin.

---

## Bonus

**1. Ücretsiz kredini planla.** Flow'daki kredi değerleri (28 Ekim 2026, 720p) bir sözlükte: anahtar süre, değer kredi.
Arayüzde gördüğün sayılar farklıysa sözlüğü düzelt.

```python
krediler = {4: 7, 6: 10, 8: 12, 10: 15}
for sure in krediler:
    kredi = krediler[sure]
    saniye_basi = round(kredi / sure, 2)
    print(sure, "saniye:", kredi, "kredi, saniyesi", saniye_basi, "kredi")
```

Çıktı:

```
4 saniye: 7 kredi, saniyesi 1.75 kredi
6 saniye: 10 kredi, saniyesi 1.67 kredi
8 saniye: 12 kredi, saniyesi 1.5 kredi
10 saniye: 15 kredi, saniyesi 1.5 kredi
```

Uzun klibin saniyesi daha ucuz; ama deneme için kısa klip daha az kredi harcar. 50 krediyle 7 tane 4 saniyelik ya da 3 tane
10 saniyelik klip çıkar. Bir günün kredisini nasıl bölerdin: kaç deneme, kaç son hâl?

**2. Dikey video.** Metinden klibin yönergesiyle arayüzde 9:16 oranında (telefon, hikâye) bir klip daha üret (8 saniye,
12 kredi), indir ve `videolar/dikey.mp4` olarak kaydet. Kompozisyon nasıl yeniden kuruldu: fincan nerede duruyor, ne kırpıldı,
ne eklendi? Klibi günlüğe üçüncü kayıt olarak ekle: Adım 6'nın ilk hücresini kopyala; kopyada sözlüğün adını `dikey_kaydi`,
`"oran"`ı `"9:16"`, `"dosya"`yı `"videolar/dikey.mp4"` yap ve kopyayı çalıştır. Sonra `kayitlar` satırını
`[metin_kaydi, gorsel_kaydi, dikey_kaydi]` yap ve Adım 6'nın son iki hücresini yeniden çalıştır.

---

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Nerede |
|---|---|---|
| Isınma | Bir klip kaç kare | defter |
| Adım 1 | Metinden ilk klibi başlatmak; uzun süren iş | arayüz |
| Adım 2 | Fiyat sözlüğü; 4K ile 1080p | defter |
| Adım 3 | 20 saniyelik tanıtım: çözünürlük ve süre seçenekleri, yarı bütçe | defter |
| Adım 4 | Klibi izlemek, indirmek, değerlendirmek | arayüz |
| Adım 5 | Görselden klip | arayüz |
| Adım 6 | Video günlüğü ve "API'yle olsaydı" hesabı | defter |
| Bonus | Ücretsiz krediyi planlamak; dikey video | defter, arayüz |

Defterin hiçbir hücresi anahtar istemez, internete çıkmaz.

---

## Sık karşılaşılan hatalar ve mesajlarını okumak

| Ne görüyorsun | Neden | Ne yapmalı |
|---|---|---|
| Flow'da video üretilemiyor, bir uyarı çıkıyor (akşam saatleri) | Yoğun saat: aboneliği olmayan kullanıcılar Türkiye saatiyle yaklaşık 17.00–20.00 arasında video üretemeyebilir | Biraz sonra dene ya da hocanın paylaştığı ekrandan izle |
| Kredin yetmiyor | O günün 50 kredisi bitti | Ertesi günü bekle; kısa ve düşük çözünürlüklü klip daha az kredi yer |
| Hesap kart bilgisi istiyor ya da abone olmanı istiyor | Ücretli bir pakete yönlendirildin | Kart girme, abone olma; hocaya yaz |
| Klip projede görünmüyor ya da kutucukta "Pending" yazıyor | Henüz bitmedi ya da sayfa yenilenmedi | Bekle, sayfayı yenile; **Generate**'e yeniden basma |
| Ayarlarda model ya da kredi değeri birden değişti | Flow seçtiğin özelliği (ör. Frames) desteklemeyen modelden başka bir modele geçti | Üretmeden önce modele ve krediye bak; anlamadıysan hocaya sor |
| İstek reddedildi | Yönergede ya da görselde gerçek bir kişi, ünlü biri ya da çocuk var | Başka bir görsel ya da yönerge |
| `KeyError: '720P'` | Çözünürlük sözlükteki anahtarla birebir aynı değil (büyük P, boşluk) | Sözlükteki gibi yaz: `"720p"`, `"1080p"`, `"4K"` |
| `TypeError: can't multiply sequence by non-int of type 'float'` | Süre metin (`"8"`); metinle ondalık sayı çarpılmaz | Tırnaksız yaz: `"sure": 8` |
| `NameError: name 'fiyatlar' is not defined` (Adım 6) | Adım 2'nin hücresi çalıştırılmadı | Adım 2'yi çalıştır |
| `NameError: name 'metin_kaydi' is not defined` | Adım 6'nın ilk hücresi çalıştırılmadı | O hücreyi çalıştır |
| Hücre bitmiyor, yanında `[*]` duruyor | `input` kutusu açık ve senden bir şey bekliyor | Ekranın üstündeki kutuya yaz, Enter |
| `FileNotFoundError: ... 'video_gunlugu.json'` | Günlüğü yazan hücre çalıştırılmadı ya da defter başka klasörde | Önce yazan hücreyi çalıştır |
| Günlükte `\u011f` gibi kodlar | `ensure_ascii=False` yazılmamış | `json.dump(..., ensure_ascii=False, indent=2)` |
| `0.6060000000000001` gibi bir sayı | Bilgisayarın ondalık hesabındaki küçük kalıntı | `round(..., 2)` ile iki basamağa yuvarla |

---

## Kendini dene

Cevaplar notun en sonunda. Önce kendin düşün.

1. 30 saniyelik bir tanıtım 1080p'de ücretli bir API'yle kaça mal olur? Bütçen 2 dolarsa 1080p'de en fazla kaç saniye?
2. Bir arkadaşın günlükte süreyi `"sure": "8"` diye yazdı. Hangi hücre hata verir, neden?
3. Metinden video ile görselden video arasındaki fark ne? Hangisi tasarımcıya daha çok kontrol verir?
4. "Kamera yaklaşırken yapraklar düşsün ve kamera sola dönsün": bu yönergede ne sorun var?
5. Arayüzde **Generate**'e bastın, bir dakika geçti, hâlâ bir şey yok. Ne düşünürsün, ne yapmazsın?
6. Görselden video için hangi görselini seçerdin: düz renkli, ortalanmış bir logo mu, derinliği olan bir masa sahnesi mi? Neden?
7. Arayüz yönergeni zaten saklıyor. Günlüğü neden yine de kendin tutuyorsun?

---

## Bu konuda öğrendiklerin

- **Video bir kare dizisi.** Zor olan kareler arası tutarlılık; bu yüzden yavaş ve pahalı.
- **Metinden ve görselden video.** Görsel ilk kare olur; yönerge ne olacağını anlatır.
- **Yönergenin parçaları.** Özne, hareket, kamera, süre; öznenin hareketi ile kameranınki ayrı cümlelerde.
- **Maliyet.** Ücretli API'de bedel = süre × o çözünürlüğün saniye fiyatı. Bedeli yarıya indirmenin iki yolu var: çözünürlüğü
  düşürmek ya da süreyi kısaltmak.
- **Sözlükle hesap.** Anahtarla değer almak (`fiyatlar["720p"]`), anahtarı değişkenden almak, sözlüğün üstünde `for`.
- **Uzun süren iş.** İstek başlar, sonuç sonra gelir; arayüz beklemeyi senin yerine yönetir.
- **Günlük.** `input` ile kayıt, `json.dump` ile dosya, `json.load` ile geri okuma.

## Bu konunun tek cümlesi

> Video kare kare tutarlılık istediği için yavaş ve pahalıdır. Süre ve çözünürlük bedeli belirler, seçimi yayın yeri yapar;
> her klibin yönergesi ile ayarları da senin günlüğünde durur.

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **Kare hızı** | Saniyede gösterilen kare sayısı; sinemada 24 |
| **Metinden video** | Sahnenin de hareketin de yönergeyle anlatıldığı video üretimi |
| **Görselden video** | Verilen görselin ilk kare olduğu video üretimi |
| **Başlangıç karesi (start frame)** | Görselden videoda videonun ilk karesi olan görsel |
| **Kamera dili** | Kameranın hareketini anlatan terimler: push in (yaklaşma), pull out (uzaklaşma), pan (yana dönüş), tilt up (yukarı dönüş), static shot (sabit çekim) |
| **Çözünürlük** | Görüntünün piksel boyutu: 720p (1280 × 720), 1080p (1920 × 1080), 4K (3840 × 2160) |
| **Oran** | Genişlik : yükseklik; 16:9 yatay, 9:16 dikey, 1:1 kare |
| **Kredi** | Ücretsiz arayüzün günlük hakkı; bir klibin harcadığı kredi süre ve çözünürlükle artar |
| **Uzun süren iş (asenkron iş)** | Sonucu istekle aynı anda gelmeyen iş; başlatılır, hazır olunca alınır |
| **Filigran** | Videoya eklenen "yapay zekayla üretildi" işareti: köşede görünen bir logo ya da gözle görülmeyen, yazılımla okunan gömülü bir iz |
| **`input`** | Kullanıcıdan metin alan fonksiyon; yazılanı her zaman metin olarak verir |
| **Video günlüğü** | Her klibin yönergesini, ayarlarını (süre, çözünürlük, oran) ve dosyasını tutan JSON dosyası |

## Ödev

`odevler/odev9.md` (puansız): Konu 8'deki görsellerinden birini arayüzde videoya çevir, video günlüğüne kaydet.
Görsel hareket edince ne korundu, ne bozuldu? Bu klip ücretli bir API'yle 1080p'de üretilseydi kaça mal olurdu?

## Sonraki konu

**Konu 10 — Zincirleme: üretim hattı.** Şimdiye kadar her şeyi ayrı ayrı ürettik: metin (Konu 5), görsel (Konu 8), video (bugün).
Konu 10'da metin ve görsel modellerini tek bir programda birbirine bağlıyoruz: bir adımın çıktısı ötekinin girdisi.

---

## Kendini dene — cevaplar

1. 30 × 0,152 = **4,56 dolar**. 2 dolarla 2 / 0,152 ≈ 13,2, yani en fazla **13 saniye** (13 × 0,152 = 1,98).
   Ya da 720p'ye inersin: 2 / 0,101 ≈ 19,8, yani 19 saniye.
2. Kayıt hücresi hata vermez; sözlük metni de saklar. Hata, günlüğü geri okuyup fiyatı hesaplayan hücrede gelir:
   `kayit["sure"] * fiyat` metinle ondalık sayıyı çarpmaya çalışır, `TypeError`. Süre tırnaksız yazılmalı.
3. Metinden videoda sahneyi de hareketi de yönerge anlatır, kompozisyonu model kurar. Görselden videoda görsel ilk kare olur;
   kompozisyonu, stili, rengi sen belirlemiş olursun. Kontrol görselden videoda.
4. Yönerge iki kamera hareketini birden istiyor (yaklaşma ve sola dönme) ve onları öznenin hareketiyle aynı cümleye koyuyor.
   Bir klipte tek bir kamera hareketi seç; öznenin hareketini ayrı bir cümleyle yaz: "leaves falling slowly. slow camera push in."
5. Büyük olasılıkla **henüz bitmedi**: video dakikalar sürebilir. **Generate**'e bir daha basmazsın: yeni bir iş başlar ve yeniden
   kredi düşer. Ekrandaki ilerleme göstergesine bak, bekle; klip hiç görünmüyorsa sayfayı yenile; yoğun saatse sonra dene.
6. Tek doğru cevap yok. Ama derinliği, boşluğu, hareket edebilecek bir öğesi (buhar, yaprak, su) olan sahne kamera hareketine daha çok yer
   bırakır; düz, ortalanmış bir logo hareket edince ya hiç değişmez ya da bozulur.
7. Arayüzün geçmişi senin dosyan değil: kredi biter, araç değişir, hesap kapanır. Günlük senin klasöründe durur; aylar sonra
   "aynısından bir tane daha" dendiğinde yönerge ve ayarlar elinde. Konu 10'daki üretim hattı da her işi böyle kaydediyor.
