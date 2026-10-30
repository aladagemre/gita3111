# Konu 10 — Afiş yarın matbaada: son kontrol

Bu not `ders.ipynb` ile aynı sırada ilerler. Derste kaçırdığın bir yeri buradan oku, sonra defterde o hücreyi çalıştır.

## Bu konuda ne yapıyoruz?

Sayfa Kahve'nin "Sessiz Okuma Gecesi" afişi bitti; yarın matbaaya ve Instagram'a gidecek. Basılmış bir afişteki hata
geri alınamaz: "yalnız" yerine "yanlız" yazmışsan, tarihin yanına yanlış günü koymuşsan, saati unutmuşsan ya da bir
satırı açık renkle yazıp okunmaz bırakmışsan, düzeltmenin tek yolu yeniden bastırmaktır. Bu konuda o son kontrolü yapan
küçük bir program kuruyorsun: afişi okuyan, dört ayrı kontrolden geçiren ve bulguları tek bir rapora yazan bir
**üretim hattı**. Sonunda elinde `ciktilar/sayfa_kahve/rapor.md` olur; raporu okuyup son kararı veren yine sensin.
Aynı hattı kendi müşterinin afişiyle de çalıştırırsın.

## Üretim hattı nedir?

Bir matbaadaki prova masasını düşün: afiş masadan masaya geçer, her masada biri tek bir şeye bakar (yazıya, tarihe,
renge) ve notunu yazar; sonunda notlar tek bir raporda toplanır. Programdaki karşılığı: **üretim hattı**, birkaç adımın
(bazısı model, bazısı Python) arka arkaya çalıştığı, her adımın sonucunu bir dosyaya sakladığı ve bir adım bozulunca
kaldığı yerden devam edebilen bir programdır.

## Hangi iş modele, hangisi Python'a?

| Adım | İş | Kim | Neden |
|---|---|---|---|
| 1 | Afişteki yazıları okumak | Görseli okuyan model (`gemma-4`) | Python görseldeki harfleri okuyamaz |
| 2 | Yazım hatası ve eksik bilgi | Metin modeli (llama, Konu 5) | Türkçe bilgisi gerekir |
| 3 | Tarih ile gün tutuyor mu | Python | Takvim hesabı |
| 4 | Yazılar okunuyor mu | Python | Renk ölçümü bir formül |
| 5 | Rapor | Python ve sen | Notları bir araya koymak |

Kural: **Python'un yapabildiğini Python yapar.** Dil modeli "14 Kasım 2026 hangi gün?" sorusunu hesaplamaz,
kelimelerden tahmin eder; Python'un takvim hesabı ise her seferinde aynıdır.

## Isınma — Python'un tek başına yakaladıkları

`from halkalar import *` satırı, bu konunun yardımcı dosyası `halkalar.py` içindeki bütün fonksiyonları deftere alır.
İlk hücrede `gun_adi("14 Kasım 2026")` takvimden günü hesaplar. Afişte "Cuma" yazıyor; Python ne diyor? `benim`
satırına kendi doğum gününü, ayın adı yazıyla ("3 Mart 2005"), yazıp dene.

İkinci hücre renk ölçer. **Kontrast**, iki renkten biri ötekinden ne kadar açık, onu söyleyen bir sayıdır: 1 ise iki
renk aynıdır, 21 ise beyaz üstüne siyahtır. Web için yazılmış okunurluk kurallarına (WCAG) göre küçük yazıyla zemini
arasında en az **4,5** olmalı; büyük başlıklarda en az 3.

```python
mavi = "#1F3A5F"
hardal = "#D9A441"
beyaz = "#F4F1EA"

mavi_oran = kontrast(mavi, beyaz)
hardal_oran = kontrast(hardal, beyaz)
print("Mavi yazı:", mavi_oran)
print("Hardal yazı:", hardal_oran)
```

Python sayıyı yazdırırken ondalık ayırıcı olarak nokta kullanır: `4.5`, "dört virgül beş" diye okunur.
Çıktına bak: iki renkten hangisi eşiği geçiyor?

## Adım 1 — Afişi oku ve okuduğunu sakla

İlk hücrede iki ayar var: `afis` (hangi afiş) ve `klasor` (notların gideceği yer). `goster(afis)` afişi defterde gösterir.
Kodu çalıştırmadan önce afişe kendin bak ve kaç sorun gördüğünü not et.

Metni tasarım dosyasından kopyalayabilirdin, ama matbaaya giden şey dışa aktardığın görseldir; müşterinin gönderdiği
afişte kaynak dosya da elinde olmaz. `afisi_oku` afişi görsel okuyan modele gönderir ve "bütün yazıları, düzeltmeden,
satır satır yaz" der. Okunan metin bir dosyaya kaydedilir. Bir adımın dosyaya kaydedilen sonucuna **ara çıktı** denir.

```python
import os

yol = f"{klasor}/okunan.txt"
if os.path.exists(yol):
    print("Afiş daha önce okunmuş; dosyadan alıyorum.")
    okunan = dosyadan_oku(yol)
else:
    okunan = afisi_oku(afis)
    dosyaya_yaz(okunan, yol)
print(okunan)
```

Satır satır:

- `yol` ara çıktının adı: `ciktilar/sayfa_kahve/okunan.txt`. `f"..."` süslü parantezin içindeki değişkeni metne koyar.
- `os.path.exists(yol)` "bu dosya var mı?" diye sorar. Varsa afiş daha önce okunmuştur: modele gitmeden dosyadan alırız.
- Yoksa (`else`) modele sorar, cevabı dosyaya yazarız.

Ara çıktının üç yararı var: afiş bir kez okunur (kota korunur); sonraki bir adım bozulursa bu adımın işi kaybolmaz;
modelin ne okuduğunu dosyayı açıp gözünle denetleyebilirsin. Dosyayı aç ve afişle karşılaştır: model "Herkez"i olduğu
gibi mi yazmış, düzeltmiş mi? Okurken düzelten bir model hatayı gizler. Bir satır yanlış okunduysa dosyada düzelt,
kaydet ve hücreyi yeniden çalıştır; hat senin metninle devam eder.

## Adım 2 — Yazım hatası ve eksik bilgi

Okunan metin bir sorunun sonuna eklenir ve metin modeline gider: Türkçe yazım hataları ve afişte tarih, saat, yerden
hangisinin eksik olduğu. Üç tırnak (`"""`) birkaç satırlık metin yazmayı sağlar. Gün adını modele sormuyoruz; onu
Adım 3'te Python denetler. Sonra Adım 1'deki kalıbın aynısı gelir:

```python
yol = f"{klasor}/yazim.txt"
if os.path.exists(yol):
    print("Yazım denetimi daha önce yapılmış; dosyadan alıyorum.")
    yazim = dosyadan_oku(yol)
else:
    yazim = modele_sor(soru, 0.2)
    dosyaya_yaz(yazim, yol)
print(yazim)
```

Sıcaklık 0.2, çünkü denetimde yaratıcılık istemiyoruz (Konu 5).

### Hangi öneri doğru? Son karar senin

Modelin cevabını madde madde oku ve her öneriye "kabul" ya da "ret" de. Model hata kaçırabilir; ama doğru bir şeyi
"düzeltmeye" de kalkabilir. Hocanın 30 Ekim 2026'daki denemesinde cevapta şu öneriler vardı:

- "Herkez" yerine "Herkes": **kabul**, gerçek bir yazım hatası.
- Saat eksik: **kabul**, afişte saat yok.
- "kafemizde" yerine "kafemize": **ret**. "Kitabını getir, kafemizde sessizliğe katıl." doğru bir cümle; öneri onu bozar.
  (Bu kelimede asıl sorun başka: Sayfa Kahve kendine "kafe" demiyor. Bunu model bilemez; Konu 11'in konusu.)
- "Moda Caddesi 12" yerine "Moda Caddesi No: 12": **ret**. Bu bir yazım hatası değil; afişte "No:" yazmak zorunlu değil.

Model her çalıştırmada başka bir cevap verebilir; senin çıktın farklı olabilir. Senin çıktında kaç yanlış öneri var?
Ders değişmez: model önerir, afişe neyin gireceğine tasarımcı karar verir.

### Model cevap vermezse?

İnternet kesilebilir, sunucu meşgul olabilir. `afisi_oku` ve `modele_sor` o zaman 5 saniye bekleyip yeniden sorar, en
fazla 3 kez; olmazsa "model cevap vermedi" notu döndürür ve `dosyaya_yaz` bu notu kaydetmez. Defterde bunu sunucu
adresini bilerek bozarak görürsün (`os.listdir` klasördeki dosyaların adlarını verir):

```python
import halkalar

halkalar.SUNUCU = "https://api.cloudflare.invalid"
bozuk = modele_sor(soru, 0.2)
dosyaya_yaz(bozuk, f"{klasor}/deneme.txt")
halkalar.SUNUCU = "https://api.cloudflare.com"

dosyalar = os.listdir(klasor)
print(bozuk)
print(dosyalar)
```

`.invalid` ile biten adresler hiçbir yerde yoktur; istek hiçbir sunucuya ulaşmaz. Klasörde `okunan.txt` ve `yazim.txt`
durur, `deneme.txt` oluşmaz. **Hat kaldığı yerden devam eder:** bağlantı gelince yalnızca eksik adım yeniden sorulur.

## Adım 3 — Tarih ile gün tutuyor mu?

Baştan sona Python. `tarihi_bul(okunan)` metindeki tarihi ("14 Kasım 2026"), `gunu_bul(okunan)` metinde yazan gün adını
("Cuma") bulur; `gun_adi(tarih)` gerçek günü hesaplar. Sonra karşılaştırırız:

```python
if yazan == dogru:
    gun_bulgusu = "Tarih ve gün tutarlı: " + tarih + ", " + dogru + "."
else:
    gun_bulgusu = "Gün yanlış: " + tarih + " bir " + dogru + "; afişte " + yazan + " yazıyor."
print(gun_bulgusu)
```

`gun_bulgusu` rapora girecek cümle. Afişinde tarih ya da gün adı yoksa `tarihi_bul` ve `gunu_bul` `yok` verir. Bu
adımda modele hiç sorulmaz; sorulsaydı ne olurdu, Bonus'ta.

## Adım 4 — Yazılar okunuyor mu?

`renkleri_cikar(afis, 5)` afişteki en yaygın 5 rengi, en yaygından başlayarak verir; ilki zemindir. JPEG sıkıştırması
renkleri biraz oynatır; bu yüzden Isınma'daki 10.18 burada 10.25 gibi görünebilir.

```python
renk_bulgulari = []
for renk in renkler[1:]:
    oran = kontrast(renk, zemin)
    if oran < 4.5:
        bulgu = renk + " zeminde zor okunur (kontrast " + str(oran) + ")"
        renk_bulgulari.append(bulgu)
print(renk_bulgulari)
```

- `renkler[1:]` listenin ikinci elemanından sonrası: zemini kendisiyle karşılaştırmıyoruz.
- `oran < 4.5`: eşiğin **altında** kalan renk zor okunur.
- `str(oran)` sayıyı metne çevirir; metinle sayı `+` ile birleşmez.

Python ölçer ama hangi rengin yazı, hangisinin süs olduğunu bilmez. Listeye giren her rengi afişte bul: yazıysa sorun,
yalnızca bir daire ya da çizgiyse sorun olmayabilir. Bu ölçüm her rengi **ana zemine** göre yapar; mavi bandın üstündeki
beyaz yazının zemini mavidir, onu ayrı denetlemelisin:

```py
print(kontrast("#F4F1EA", "#1F3A5F"))
```

## Adım 5 — Rapor

Notlar tek bir metinde toplanır: `rapor = rapor + ...` her satırda rapora bir parça ekler. `\n` yeni satırdır, `#` ve
`-` Markdown'da başlık ve madde işaretidir. VS Code'da `rapor.md`'yi açıp sağ üstteki önizleme düğmesine basarsan
başlıklı, düzgün bir sayfa görürsün.

Hattın en kolay büyüyen yeri burası. Örnek kontrol:

```python
if "@" in okunan:
    kendi = "Instagram adresi yazıyor."
else:
    kendi = "Instagram adresi yok."
rapor = rapor + "\n## Benim kontrolüm\n" + kendi + "\n"
```

`"@" in okunan`, "okunan metinde @ işareti geçiyor mu?" demek. Altındaki boş hücreye kendi kontrolünü yaz: semtin adı
geçiyor mu, "ücretsiz" sözü var mı, müşterinin bir kuralına uyuyor mu ("ünlem kullanmayalım" dediyse `"!" in okunan`).
Raporu kaydettikten sonra dosyayı aç; Adım 2'de reddettiğin önerileri sil ya da yanına "ret" yaz.

**Kendi afişinle:** afişi `veri/` içine `.jpg` olarak koy, Adım 1'deki iki satırı değiştir (ör.
`afis = "veri/benim_afisim.jpg"`, `klasor = "ciktilar/benim_afisim"`), menüden Restart'a bas, baştan çalıştır.

## Bonus — Gün sorusunu modele sorsaydık?

Aynı "14 Kasım 2026 hangi gün?" sorusu metin modeline gider (1 istek). Model doğru bilmiş de olabilir; ders değişmez:
modelin cevabını her seferinde denetlemen gerekir, Python'un hesabını gerekmez. Temiz afişin (`veri/afis_temiz.jpg`)
renklerini alıştırmanın 3. maddesinde ölçersin.

## Sık hatalar

| Ne görüyorsun | Neden | Ne yap |
|---|---|---|
| `NameError: name 'okunan' is not defined` | Yukarıdaki bir hücreyi atladın ya da çekirdek yeniden başladı | Hücreleri baştan sırayla çalıştır |
| `FileNotFoundError: ... '../anahtar.txt'` | Anahtar dosyası `gita3111` klasöründe değil | Konu 2'deki gibi `anahtar.txt` oluştur; olmazsa Adım 1–2'yi hocanın ekranından izle |
| Kendi afişini koydun ama Sayfa Kahve'nin metni çıkıyor | `klasor`u değiştirmedin; hat eski `okunan.txt`'yi buldu | `klasor` satırını değiştir ya da eski dosyayı sil |
| "Deneme 1 olmadı" yazıları | Bağlantı ya da sunucu sorunu; ya da adresi bozan hücreyi yarıda durdurdun | Bekle; düzelmezse Restart ve baştan çalıştır |
| `TypeError: can only concatenate str (not "float") to str` | Sayıyı metne `str(...)` olmadan ekledin | `str(oran)` |
| Model "Herkez"i bulmadı | Model okurken düzeltti ya da denetimde kaçırdı | `okunan.txt`'ye bak; rapora elle not düş |
| Model doğru bir kelimeyi "düzeltmek" istedi | Model öneri yapar, kesin bilmez | Öneriyi reddet; raporda sil ya da "ret" yaz |
| Bütün renkler "zor okunur" çıktı | Karşılaştırmayı ters yazdın (`>`) | Eşiğin altı: `oran < 4.5` |

## Kendini dene

1. Hücreyi ikinci kez çalıştırdığında Adım 1 ne yazar? Modele istek gider mi? Neden?
2. Adım 2'de model 3 denemede de cevap vermezse klasörde hangi dosyalar olur? Ertesi gün hücreleri yeniden çalıştırınca
   kaç istek gider?
3. "Afişteki tarih bir hafta sonuna mı denk geliyor?" Bunu model mi yapmalı, Python mı? Neden?
4. "Afiş metni müşterinin ses tonuna uyuyor mu?" Bunu model mi yapmalı, Python mı?
5. Kontrastı 3,8 olan bir renk başlıkta kullanılabilir mi, küçük dipnotta?
6. Renk kontrolü bir rengi "zor okunur" diye işaretledi ama o renk bir süs çizgisi. Raporu nasıl düzeltirsin?

## Sözlükçe

- **Üretim hattı:** arka arkaya çalışan adımlardan oluşan, her adımın sonucunu saklayan ve bozulan adımdan devam edebilen program.
- **Ara çıktı:** bir adımın dosyaya kaydedilmiş sonucu (`okunan.txt`, `yazim.txt`).
- **Kontrast oranı:** iki rengin açıklık farkı; 1 ile 21 arası. Küçük yazıda en az 4,5, büyük başlıkta en az 3.
- **WCAG:** web içeriğinin herkes için erişilebilir olması için yazılmış uluslararası kurallar; kontrast eşikleri buradan.
- **HEX renk:** `#1F3A5F` gibi yazılan renk kodu; ilk iki hane kırmızı, sonraki ikisi yeşil, son ikisi mavi.
- **Kota:** ücretsiz hesabın günlük istek hakkı; ara çıktı onu korur.
- **`os.path.exists(yol)`:** dosya varsa `True`, yoksa `False`.

Sıradaki konu: hat afişi denetledi ama müşterinin kurallarını bilmiyor ("kafe" değil "çalışma evi" de, turuncu
kullanma). Konu 11'de hatta bir hafıza vereceğiz: müşterinin notlarını hatırlayan bir arama.
