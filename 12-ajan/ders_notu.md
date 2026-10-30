# Konu 12 — Stüdyo asistanı (ders notu)

Bu notu `ders.ipynb` ile aynı sırada oku. İş: Sayfa Kahve için bir günün dört küçük işi (14 Kasım hangi gün,
afişin kontrolü, müşterinin yeni bir isteğini not almak, bir gönderi metnini denetlemek). Konu 10'da bunlardan
yalnızca afiş kontrolünün adımlarını ve sırasını sen yazmıştın; bu konuda bir asistana yalnızca hedefi söylüyorsun,
hangi aracı hangi sırayla kullanacağına model karar veriyor. Araçların içini ise sen yazıyorsun.

## Ajan nedir?

**Ajan**, hedefi söylediğin, yolu kendisi seçen ve elindeki araçlarla iş yapan bir programdır.

Yeni bir stajyer düşün. "Şu afişi kontrol et" dersin. O önce afişe bakar, sonra müşteri dosyasını açar, tarih şüpheli
gelirse takvime bakar. Sırayı sen söylemezsin; ama hangi dolapları açabileceğine sen karar verirsin.

| | Ne yapar | Adımları kim seçer |
|---|---|---|
| Sohbet botu | Yalnızca konuşur; dosyana, takvimine dokunamaz | — |
| Üretim hattı (Konu 10) | Yazdığın adımları her seferinde aynı sırayla çalıştırır | Sen, kodda |
| Ajan | Senin verdiğin araçları kullanarak iş yapar | Model, her istekte yeniden |

- **Araç:** senin yazdığın bir Python fonksiyonu ve onun **tarifi**. Model aracın kodunu görmez, yalnızca adını ve
  tarifini okur. Aracı çalıştıran yine senin programındır.
- **Döngü:** model bir araç ister → program aracı çalıştırır → sonuç modele döner → model ya yeni bir araç ister ya
  da cevabını yazar. Döngünün her turu modele bir istek demek.
- **Ajan her zaman gerekmez.** Adımlar her seferinde aynıysa Konu 10'daki hat yeter: daha ucuzdur, daha hızlıdır ve
  hep aynı sonucu verir. Ajan, yolun isteğe göre değiştiği yerde işe yarar: bir istek "afişi kontrol et", öteki
  "müşteri fikrini değiştirdi, not al".

## Isınma — Araç: bir fonksiyon ve tarifi

```python
from ajan_araclari import gun_adi, tarifi_goster

def gunu_hesapla(tarih: str):
    """Bir tarihin haftanın hangi gününe denk geldiğini takvimden hesaplar. tarih: '14 Kasım 2026' gibi bir tarih."""
    return gun_adi(tarih)

gun = gunu_hesapla("14 Kasım 2026")
print(gun)
```

- `def` satırının altındaki üç tırnaklı metin aracın **tarifi** (Python'daki adı *docstring*). Bu derste ilk kez
  yazıyoruz, çünkü model aracı bu metni okuyarak seçer.
- `tarih: str` bir **tür ipucu**: "bu bilgi bir metin". Agno bunu modele iletir, model de buraya metin yazar.
- Aracın içi tek satır: yardımcı dosyadaki `gun_adi`. Takvim hesabı Python'un işi; yapay zekâ gerekmez.
- Aracı ajana vermeden önce kendin bir kez çağırmak iyi bir alışkanlık: `Cumartesi` çıktıysa aracın çalışıyor.

`tarifi_goster(gunu_hesapla)` modelin bildiği her şeyi üç satırda yazar: aracın adı, tarifi, bilgisinin adı. "Düşün"
sorusunun cevabı: birinci istekte kullanır (tarih → gün). İkincide kullanmaz; tarif renkten söz etmiyor. Üçüncüde
belki: 12 Kasım'ın gününü sorabilir, ama matbaa kuralı için başka bir araç (müşteri notları) gerekir.

## Adım 1 — İlk ajan: tek araç

```python
from agno.agent import Agent
from ajan_araclari import model_kur, kararlari_goster

model = model_kur()
ajan = Agent(model=model, tools=[gunu_hesapla], tool_call_limit=4, telemetry=False)
```

- **Agno**, ajan döngüsünü bizim yerimize çalıştıran bir kütüphane. Döngüyü elle de yazabilirdik; Agno bu tekrar eden
  kısmı üstleniyor.
- `model_kur()` Cloudflare'deki `gemma-4` modelini Agno'ya tanıtır. İçinde `OpenAILike` geçer ve `openai` paketi
  kullanılır: bu yalnızca **isteğin biçiminin** adı. İstek Cloudflare'e gider; OpenAI hesabı da ödeme de gerekmez.
- `tools=[gunu_hesapla]`: araçlar parantezsiz yazılır. `gunu_hesapla()` fonksiyonu çalıştırır; `gunu_hesapla` fonksiyonu ajana verir.
- `tool_call_limit=4`: bir çalıştırmada en fazla 4 araç çalışır; sınır dolunca Agno modele "sınır doldu" der.
  Model bir döngüye takılırsa ücretsiz kotan böyle korunur.
- `telemetry=False`: Agno'nun kendi sunucusuna kullanım kaydı göndermesini kapatır; bugünkü her ajanda var.

```python
cevap = ajan.run("14 Kasım 2026 hangi gün?")
print(cevap.content)
kararlari_goster(cevap)
```

`cevap.content` ajanın son cevabı. `cevap.tools` ajanın kullandığı araçların listesi: her birinin adı `tool_name`,
modelin araca verdiği bilgiler `tool_args`. `kararlari_goster` bu listeyi sırayla yazar; ajan hiç araç kullanmadıysa
(`cevap.tools` boşsa) bunu söyler.

**Model kendi bilseydi neden yanlış olabilirdi?** Dil modeli takvim hesaplamaz; Konu 5'te gördüğün gibi, metinlerde
gördüğü kalıplara bakarak sıradaki sözcüğü tahmin eder. "14 Kasım 2026" için doğru günü tahmin edebilir de, edemeyebilir
de; Python ise her seferinde hesaplar. Bu konunun ana fikri: **model karar verir, iş Python'da yapılır.** Bu
çalıştırma modele en az iki istek gönderir: biri araç kararı için, biri sonucu görüp cevabı yazmak için.

## Adım 2 — Üç araç: "bu afişi kontrol et"

```python
from ajan_araclari import gorseldeki_yazi, en_yakin_kurallar

def afisi_oku(yol: str):
    """Bir afiş görselindeki bütün yazıları ve renkleri okur. yol: görselin dosya yolu, ör. veri/afis.jpg"""
    return gorseldeki_yazi(yol)

def kurallara_bak(soru: str):
    """Müşterinin marka kurallarında ve notlarında soruya en yakın beş kuralı bulur: renk, yazı, sözcük, afişte ne olmalı."""
    return en_yakin_kurallar(soru, 5)
```

- `afisi_oku` Konu 10'daki görsel okumayı kullanır (orada yardımcıdaki hazır bir fonksiyondu; burada aynı adla bir
  araç, içi `gorseldeki_yazi`). Görseldeki yazıyı okumak yapay zekânın işi; bir betik bunu yapamaz.
- `kurallara_bak` Konu 11'deki anlamca aramayı kullanır: soruyu ve hafızadaki her satırı vektöre çevirir, soruya en
  yakın beş satırı verir.

Ajan bu üç araçla ve `tool_call_limit=6` ile yeniden kuruluyor: bu iş daha çok adım isteyebilir.

```python
cevap = ajan.run("veri/afis.jpg afişini müşterinin kurallarına göre kontrol et")
print(cevap.content)
kararlari_goster(cevap)
```

Kodun hiçbir yerinde "önce afişi oku, sonra kurallara bak" yazmıyor; sırayı model seçiyor. Senin çıktında sıra ne
oldu, kaç araç kullandı? İstek "kurallara göre kontrol et" diyor, tarihten söz etmiyor: ajan `gunu_hesapla`'u çağırmadıysa
yanlış günü de yakalayamaz.

Raporu afişle karşılaştır. Afişte bilerek bırakılmış yedi sorun var: yazım hatası, yanlış gün, eksik saat, okunurluğu
düşük bir yazı, yasak bir renk, müşterinin kullanmadığı bir sözcük, kenara dayanan başlık. Ajan hepsini bulamayabilir,
afişte olmayan bir sorun da yazabilir; kılavuzun bir cümlesini harfiyen uygulayıp tartışmalı bir şey de yakalayabilir.
`kurallara_bak`'ın sonucuna da bak: arama her zaman en yakın beş kuralı getirir, afişle ilgisiz olsalar bile (Konu 11).
Kontrol notunu müşteriye gönderen sensin, son okuma da senin.

## Adım 3 — "Unutma": hafızaya not yazdırmak

Ajan iki `ajan.run` arasında konuşmayı hatırlamaz; her çalıştırma sıfırdan başlar. Hatırlamasını istediğin şeyi bir
dosyaya yazdırırsın. Hafıza `ciktilar/hafiza.txt`: `veri/kilavuz.txt` ile `veri/notlar.txt`'nin (Konu 11) ilk
kullanımda birleştirilmiş kopyası, her satırı bir kural ya da not. Ajan kopyaya yazar; `veri/` değişmez, `git pull`
da çakışmaz.

```python
from ajan_araclari import hafizaya_ekle

def hatirla(not_metni: str):
    """Müşterinin yeni bir isteğini ya da kuralını hafızaya kalıcı olarak yazar. Kullanıcı 'unutma' ya da 'not al' derse kullan."""
    return hafizaya_ekle(not_metni)

araclar = [afisi_oku, gunu_hesapla, kurallara_bak, hatirla]
ajan = Agent(model=model, tools=araclar, tool_call_limit=6, telemetry=False)
```

Tarifin ikinci cümlesi modele aracın **ne zaman** seçileceğini söylüyor. İyi bir tarifin çoğu zaman en işe yarayan
kısmı budur.

```python
cevap = ajan.run("Müşteri artık afişlerde hardal sarısı da istemiyor, unutma.")
print(cevap.content)
kararlari_goster(cevap)
```

```python
from ajan_araclari import hafizayi_oku

notlar = hafizayi_oku()
sayi = len(notlar)
print(sayi, "satır")
print(notlar[-1])
```

İlk açılışta hafızada 30 satır var (kılavuzun 14 paragrafı, 16 not). `hatirla` çalıştıysa 31 olur ve son satır
`Asistanın notu, <bugünün tarihi>: ...` diye başlar. Notu ajan kendi cümlesiyle yazdı: senin söylediğinle aynı mı?
Hücreyi her çalıştırışında yeni bir not eklenir; yanlış ya da tekrar eden bir not olursa `ciktilar/hafiza.txt`'yi açıp
satırı sil. Dosyayı silersen hafıza ilk hâline döner.

Sonra Adım 2'deki istek aynen tekrarlanıyor. Kod aynı, hafıza farklı: cevabın değiştiyse sebebi yeni not. Kılavuz
hardalı "küçük vurgu" olarak serbest bırakıyor, yeni not yasaklıyor. Notun tarihi bu yüzden önemli: hangisinin daha
yeni olduğunu ajan ancak tarihten anlayabilir.

Araçları da Adım 2'yle karşılaştır. Ajan her çalıştırmada yolu yeniden seçer: aynı istekte bir kez `gunu_hesapla`'u
atlayıp bir kez çağırabilir. Konu 10'daki hat her afişte aynı adımları çalıştırır, tarihi hiç atlamaz. Her afişte aynı
kontrol gerekiyorsa hat kur; asistan, iş her gün değiştiğinde işe yarar. Adımın son hücresi cevabı
`ciktilar/afis_kontrolu.txt`'ye kaydeder: müşteriye gidecek notun taslağı.

## Adım 4 — Kendi aracın: ad ve tarif bir brif

Bir sözcüğün metinde geçip geçmediğine bakmak sıradan Python'un işi: model bir sözcüğü gözden kaçırabilir, `in`
kaçırmaz. Bu aracın içini sen yazıyorsun. Hücre şöyle başlıyor:

```python
def metne_bak(metin: str):
    """Metne bakar."""
    yasaklar = ["kafe", "indirim", "kampanya", "fırsat", "hemen"]
    bulunan = []

    return bulunan

deneme = metne_bak("Hemen gel, kafemizde sınav haftası indirimi!")
print(deneme)
tarifi_goster(metne_bak)
```

Boş satıra yazdığın üç satır şöyle olmalı (girinti `bulunan = []` ile aynı hizadan başlar):

```py
    for sozcuk in yasaklar:
        if sozcuk in metin.lower():
            bulunan.append(sozcuk)
```

`deneme` `['kafe', 'indirim', 'hemen']` vermeli: "kafemizde" içinde "kafe", "indirimi" içinde "indirim" geçiyor;
`lower()` olmasa baştaki "Hemen" bulunmazdı. `return` ettiğin liste modele gider, model sonraki adımına buna bakar.

```python
araclar = [afisi_oku, gunu_hesapla, kurallara_bak, hatirla, metne_bak]
ajan = Agent(model=model, tools=araclar, tool_call_limit=6, telemetry=False)

cevap = ajan.run("Bu gönderi metni müşterinin kurallarına uyuyor mu: 'Hemen gel, kafemizde sınav haftası indirimi!'")
print(cevap.content)
kararlari_goster(cevap)
```

Aracın adı da tarifi de bilerek tembel: `metne_bak`, "Metne bakar." Model aracı bu ikisinden tanır. Elinde tarifinde
"kural" ve "sözcük" geçen `kurallara_bak` da var; ajan senin aracını seçmeyip kuralları getirerek metne kendisi
bakabilir. Muğlak brif yanlış iş getirir, muğlak tarif yanlış araç seçimi. İyi bir tarif örneği:

```py
"""Bir metinde Sayfa Kahve'nin istemediği sözcükleri (kafe, indirim, kampanya, fırsat, hemen) arar, bulduklarını
liste olarak verir. Bir gönderi, başlık ya da afiş metni müşterinin kurallarına uyuyor mu diye sorulunca kullan.
metin: kontrol edilecek metnin tamamı."""
```

Tarifi değiştirince önce `def` hücresini, sonra aynı isteği çalıştıran alttaki hücreyi çalıştır: araç listesi
kurulduğu andaki fonksiyonu tutar. Muğlak tarifle de senin aracın seçildiyse bu bir tahmindi, başka bir istekte
tutmayabilir. Kendi aracına işini söyleyen bir ad ver (`yasak_sozcuk_bul` gibi).

## Bonus — Yarışma ve staj takipçisi

Tek araçlı bir ajan: `webde_ara`, içinde ücretsiz bir web araması.

- Arama `ddgs` paketiyle yapılıyor: ücretsiz, anahtar istemez. Ajanın kendi kararları yine Cloudflare kotasından gider.
- `add_datetime_to_context=True` ajana bugünün tarihini söyler. Model bugünün tarihini kendiliğinden bilmez;
  "önümüzdeki iki ay" bu bilgi olmadan anlamsız.
- **Listedeki her bağlantıya tıkla.** Model arama sonuçlarını özetlerken yarışma adı ya da tarih uydurabilir
  ("bilinmiyor" yaz demek bunu tam önlemez); "tahmini" bir tarih bir sitede değil, modelin tahmininde. Adı ve son
  tarihi yarışmanın kendi sitesinden doğrula.

## Sık hatalar

| Ne görüyorsun | Ne demek | Ne yap |
|---|---|---|
| `ModuleNotFoundError: No module named 'agno'` | Kütüphane kurulu değil ya da çekirdek yanlış | `gita3111` klasöründe `uv sync`; çekirdek `.venv` |
| Kırmızı `ERROR` ve `401` / `429` | Anahtar yanlış / kota ya da hız sınırı | `anahtar.txt`'yi kontrol et (Konu 2) / biraz bekle, kota ertesi gün yenilenir |
| `Ajan çalışamadı: ...` | Ajan modele ulaşamadı; sebep yanında yazar | Üstteki iki satıra bak |
| Sarı `WARNING Could not run function` | Hata aracın içinde; Agno hücreyi durdurmaz, hatayı modele sonuç olarak gönderir | Aracı kendin çağırıp hatayı gör, `def`i düzelt, ajanı yeniden kur |
| `Ajan hiç araç kullanmadı` | Model cevabı kendisi yazdı | Tarifi daha açık yaz ya da isteği aracın tarifine yaklaştır |
| Tarifi düzelttin ama ajan aynı davranıyor | Ajan eski fonksiyonu tutuyor | Araç listesini ve ajanı kuran hücreyi de çalıştır |
| `Böyle bir dosya yok: ...` | Model afişin yolunu yanlış yazdı | İstekte yolu açıkça yaz: `veri/afis.jpg` |
| `deneme` `[]` veriyor ya da `IndentationError` | Döngü yok, `return`ün altında kaldı ya da girinti kaydı | Üç satırı `bulunan = []` ile `return` arasına, `for`'u `bulunan` hizasında yaz |

## Kendini dene

1. Konu 10'daki hattı ajana çevirmek mantıklı olur muydu? Hangi durumda evet, hangi durumda hayır?
2. Ajana `afisi_sil(yol)` aracı verseydin, "eski afişi temizle" isteği seni hangi riske sokardı?
3. `tool_call_limit=2` olsaydı Adım 2'deki kontrol neden eksik kalırdı?
4. Kendi müşterin için ajana hangi aracı verirdin? Adını, bilgisini ve tarifini yaz.

## Sözlükçe

- **Ajan:** hedefi söylediğin, hangi aracı hangi sırayla kullanacağını kendisi seçen program.
- **Araç:** ajanın kullanabildiği, senin yazdığın fonksiyon; modele yalnızca adı, tarifi ve bilgileri görünür.
- **Tarif (docstring):** `def` satırının altındaki üç tırnaklı açıklama; model aracı adıyla birlikte bundan tanır.
- **Döngü:** model araç ister → program çalıştırır → sonuç modele döner → yeni karar ya da cevap.
- **Agno:** döngüyü bizim yerimize çalıştıran ajan kütüphanesi.
- **`cevap.tools`:** ajanın kullandığı araçların listesi (`tool_name`, `tool_args`).
- **`tool_call_limit`:** bir çalıştırmada en fazla kaç aracın çalışacağı; kota ve güvenlik için.
- **Telemetri:** bir kütüphanenin kendi sunucusuna gönderdiği kullanım kaydı; `telemetry=False` ile kapalı.
- **Hafıza:** ajanın iki çalıştırma arasında unutmaması gereken şeyleri tutan dosya (`ciktilar/hafiza.txt`).
