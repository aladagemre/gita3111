# Konu 8 — Bir haftalık gönderi seti

Bu not `ders.ipynb` defteriyle **aynı sırada** ilerler (Isınma, Adım 1–5, Bonus); kod blokları defterdeki
hücrelerin birebir aynısı. Kaçırdığın yeri buradan oku, sonra defterde o adımın hücrelerini çalıştır.

**Konu 7'de:** görselleri bir arayüz gibi kullandığımız hazır bir araçla tek tek ürettik; yönergenin
parçalarını ve kontrollü deneyi gördük.
**Bu konuda:** sosyal medya tasarımcısının en sık yaptığı işi koddan yapıyoruz. Müşteri haftalık
içerik takvimini gönderiyor; her gün için bir gönderi (4:5) ve aynı görselden bir hikâye (9:16)
hazırlıyor, hepsini tek bir onay sayfasıyla müşteriye yolluyoruz.

> Görseli yapay zekâ üretir; geri kalan her şeyi (takvimi okumak, başlığı yazmak, ölçüye uyarlamak,
> onay sayfası, günlük) Python yapar. Bir kez üret, çok kez uyarla. Her üretimi kayda geçir.

**Bugünün müşterisi:** Sayfa Kahve, üniversitenin yanındaki sessiz bir çalışma kafesi. Kılavuzu
`../11-rag/veri/kilavuz.txt` dosyasında: mürekkep mavisi (#1F3A5F) ve kâğıt beyazı (#F4F1EA), kırmızı
ve turuncu hiç yok, iki renkli risograf baskı tarzı, insan yüzü yok, serifli başlıklar, fısıltı gibi bir
ses tonu ("indirim", "kampanya" yok; ünlem yok).

**Konunun sonunda elinde:** `ciktilar/` klasöründe beş gönderi, beş hikâye, bir onay sayfası
(`onay_sayfasi.jpg`) ve bir üretim günlüğü (`gunluk.csv`).

**Kota:** ana akış 7 görsel üretir, Bonus'la 10. Her görsel ücretsiz günlük kotadan yer; yazı, ölçü ve
onay sayfası yemez.

## Isınma — Takvimde ne var?

**İçerik takvimi**, bir haftanın ya da ayın paylaşım planıdır: hangi gün, hangi başlık, hangi görsel.
Müşteriler çoğu zaman bir tabloyla gönderir. Bizimki `veri/takvim.csv`: her satır bir gün, sütunlar
`gun`, `baslik`, `sahne`. Sahnenin içinde virgül olduğu için tırnak içinde yazılı; `csv` bunu kendisi çözer.

```python
import csv

with open("veri/takvim.csv", encoding="utf-8-sig") as dosya:
    okuyucu = csv.DictReader(dosya)
    takvim = list(okuyucu)

for satir in takvim:
    print(satir["gun"], "·", satir["baslik"])
```

- `csv.DictReader` her satırı bir sözlüğe çevirir; anahtarlar sütun adları (Konu 3).
- `utf-8-sig`: Excel'in dosyanın başına koyduğu görünmez işareti atlar. O işaret okunursa ilk sütunun
  adı `gun` değil görünmez bir harfle başlayan başka bir ad olur ve `KeyError: 'gun'` alırsın.
- Başlıklar Türkçe, sahneler İngilizce: sahne görsel modeline gider (modeller İngilizceyi daha iyi
  anlıyor, Konu 7), başlığı Python yazar.

5 gönderi + 5 hikâye = 10 dosya, ama modele **5 istek** gider: hikâye için yeni görsel üretmiyoruz, aynı
görseli Python dikey ölçüye yerleştiriyor. **Üretmek kota yer, uyarlamak yemez.**

## Adım 1 — Pazartesi'nin gönderisi

`uretim.py` bu klasördeki yardımcı dosya. Defterde onun fonksiyonlarını çağırıyoruz:

| Fonksiyon | Ne yapar | Kim yapar |
|---|---|---|
| `ciz(yonerge, yol)` | Görseli üretir, `yol`a kaydeder; olmazsa nedenini yazar, `None` verir | yapay zekâ |
| `sabirli_ciz(yonerge, yol)` | `ciz` gibi; olmazsa 5 sn bekleyip yeniden dener (en fazla 3 kez) | yapay zekâ |
| `gonderi_yap(gorsel_yolu, baslik, bicim, yol)` | Görseli zemine yerleştirir, başlığı altına yazar; `bicim`: `"gonderi"` ya da `"hikaye"` | Python |
| `onay_sayfasi(yollar, yol)` | Dosyaların küçük hâllerini adlarıyla tek sayfaya dizer | Python |
| `gunluge_ekle(gunluk, gun, yonerge, dosya)` | Günlüğe saatiyle bir satır ekler | Python |
| `goster(yol)` | Dosyayı defterde gösterir | Python |

İlk denemede yönerge yalnızca sahne. `takvim[0]` listenin ilk satırı (Python saymaya 0'dan başlar).
Konu 7'deki `ciz`'den farkı: tohum yok, çünkü bu konudaki model şu an tohum kabul etmiyor (Adım 2).

**Başlığı neden modele yazdırmıyoruz?** Görsel modelleri harfleri de resim gibi çizer: kelimeyi bozar,
ş, ğ, ı, İ gibi harfleri sık sık yanlış çizer, fontu sen seçemezsin. Müşteri başlığı değiştirirse görseli
baştan üretmen gerekir. Tasarım programındaki **şablon** mantığı: görsel bir katman, yazı ayrı bir katman.
Yazıyı Python koyunca harfler hep doğru; font (DejaVu Serif, `veri/DejaVuSerif.ttf`, serbest lisanslı,
lisansı `veri/DejaVu_LISANS.txt`) ve renk hep kılavuzdaki gibi. Başlık şeridi gönderinin beşte biri
(270 piksel): kılavuz yazının görselin en fazla beşte birini kaplamasını istiyor.

## Adım 2 — Marka dili: stil cümlesi

Haftalık set yan yana durduğunda bir aile gibi görünmeli: **marka dili**. Yapay zekâyı kendi hâline
bırakırsan ortalama bir görsel verir; seti tutarlı yapan senin kararların. Arayüzlerde bunun için bir
"stil referansı" görseli yüklersin; kodda karşılığı **stil cümlesi**: kılavuzu görsel modelinin anlayacağı
dile çevirdiğin, her sahnenin sonuna eklenen sabit cümle. Kılavuzun "görsel modeli için özeti" gibi.

```python
STIL = "two-color risograph print illustration, deep ink blue and warm paper white"
STIL = STIL + ", flat shapes, soft grain, plenty of empty space"
STIL = STIL + ", no text, no letters, no faces"

yonerge = pazartesi["sahne"] + ", " + STIL
gorsel = ciz(yonerge, "ciktilar/Pazartesi_gorsel.jpg")
gonderi = gonderi_yap(gorsel, pazartesi["baslik"], "gonderi", "ciktilar/Pazartesi_gonderi.jpg")
gunluge_ekle("ciktilar/gunluk.csv", "Pazartesi", yonerge, gorsel)
goster(gonderi)
```

Stil cümlesini üç satırda kuruyoruz; her satır kılavuzdan bir öbek: renk ve teknik; biçim, doku ve
boşluk; yasaklar. `STIL + ", ..."` metnin sonuna ekler. `STIL` büyük harfle yazılmış: "defter boyunca
değişmeyecek" demek, bir gelenek. Hangi kural tuttu, hangisi tutmadı? Tutmayanı daha açık yaz; ama bütün
hafta bu cümleyle üretileceği için kararı şimdi ver.

**Aynı yönerge, aynı görsel mi?** Hayır: tohum olmadığı için her seferinde başka görsel gelir. İki sonucu var:

- Adım 1 ile 2 arasındaki farkın bir kısmı rastlantı; Konu 7'deki gibi tam bir kontrollü deney değil.
  Ama renkler ve baskı tarzı stil cümlesinden gelir: **tutarlılığı stil cümlesi sağlar.**
- Beğendiğin bir görseli yeniden üreterek geri alamazsın. Bu yüzden **dosyayı ve yönergeyi saklarız**:
  `gunluge_ekle` her üretimi `ciktilar/gunluk.csv` dosyasına yazar. Bir hücreyi yeniden çalıştırırsan
  aynı adlı dosyanın üstüne yeni bir görsel yazılır; beğendiysen dokunma.

## Adım 3 — Bütün hafta

```python
for satir in takvim[1:]:
    gun = satir["gun"]
    yonerge = satir["sahne"] + ", " + STIL
    gorsel = sabirli_ciz(yonerge, f"ciktilar/{gun}_gorsel.jpg")
    gonderi_yap(gorsel, satir["baslik"], "gonderi", f"ciktilar/{gun}_gonderi.jpg")
    gunluge_ekle("ciktilar/gunluk.csv", gun, yonerge, gorsel)
    print(gun, "hazır")
```

Satır satır: günü al; yönergeyi kur (sahne + stil); görseli üret ve günün adıyla kaydet; gönderiyi yap; günlüğe yaz.

- **`takvim[1:]`** bir dilim: 1 numaralı satırdan listenin sonuna kadar. 0 numaralı Pazartesi Adım 2'de
  hazırlandı; döngü Salı'dan Cuma'ya gezer (4 istek). Konu 1'deki `kelimeler[:8]` de bir dilimdi: iki
  noktanın solu başlangıç, sağı bitiş; boş bırakılan taraf "baştan" ya da "sona kadar" demek.
- **Dosya adı günden geliyor** (`Çarşamba_gonderi.jpg`): her gün kendi dosyasına. Hepsine aynı adı
  verseydin her tur bir öncekinin üstüne yazardı; elinde yalnızca Cuma kalırdı.
- **`sabirli_ciz`**: isteklerden biri takılırsa set yarım kalmasın. Üç denemede de olmazsa `None` verir;
  `gonderi_yap` o günü atlar ve söyler.

**Üretim günlüğü** (`ciktilar/gunluk.csv`): her satırda zaman, gün, tam yönerge, dosya. Müşteri "şunu
değiştir" dediğinde hangi görselin hangi yönergeyle üretildiğini ve yeni denemeye nereden başlayacağını
buradan bilirsin. Günlükten satır silinmez, yalnızca eklenir; yeniden üretimler de kayda girer.

## Adım 4 — Hikâyeler ve onay sayfası

```python
gonderiler = []
hikayeler = []
for satir in takvim:
    gun = satir["gun"]
    gorsel = f"ciktilar/{gun}_gorsel.jpg"
    hikaye = gonderi_yap(gorsel, satir["baslik"], "hikaye", f"ciktilar/{gun}_hikaye.jpg")
    gonderiler.append(f"ciktilar/{gun}_gonderi.jpg")
    hikayeler.append(hikaye)
```

Bu hücrede `ciz` yok: **sıfır istek**. Hikâyede (1080 × 1920) görsel üstten 250 piksel aşağıda başlar,
altta 320 piksel boş kalır. Telefonda hikâyenin üst şeridinde profil adı, alt şeridinde yanıt kutusu durur;
başlık oraya düşerse okunmaz.

```python
tum_dosyalar = gonderiler + hikayeler
onay_sayfasi(tum_dosyalar, "ciktilar/onay_sayfasi.jpg")
goster("ciktilar/onay_sayfasi.jpg")
```

`gonderiler + hikayeler` iki listeyi uç uca ekler. Onay sayfası satır başına en fazla beş küçük resim
dizer: üstte gönderiler, altta hikâyeler, her birinin altında dosya adı. Müşteri "Çarşamba_gonderi.jpg
olmamış" diye adıyla söyleyebilir. Sayfanın tarihini de Python yazar.

## Adım 5 — Hangi gün olmamış?

Onay sayfasına müşteriden önce sen bak, kılavuzun gözüyle: yalnızca mürekkep mavisi ve kâğıt beyazı (en
fazla küçük bir hardal vurgu), **kırmızı ve turuncu yok**, insan yüzü yok; bir de bizim kuralımız: görselde
yazı yok. Stil cümlesi iki rengi söylese de model kendi alışkanlığına kayıp yasak bir rengi ekleyebilir:
kendi hâline bırakılan yapay zekâ ortalamaya kayar, seçmek ve "bu olmamış" demek tasarımcının işi. Sorunlu
gün herkeste başka; kendi onay sayfana bak. Hepsi uyuyorsa en zayıf bulduğun günü seç.

Sonra yalnızca o günü yenileyen hücreyi kendin yazıyorsun. İhtiyacın olanlar:

1. İlk satır seçtiğin gün: `gun = "Perşembe"` gibi, takvimdeki yazımla (Türkçe harfleriyle).
2. O günün satırı: `takvim` içinde bir `for`, içinde `if satir["gun"] == gun:` ve `secilen = satir`.
3. Yönerge Adım 3'teki gibi: `secilen["sahne"] + ", " + STIL`.
4. **Yeni dosya adları**: `f"ciktilar/{gun}_gorsel_2.jpg"`, `_gonderi_2`, `_hikaye_2`. Eskisinin üstüne
   yazma: yenisi başka bir yerden bozuk çıkabilir ve eskisini bir daha üretemezsin.
5. Gönderi ve hikâye için iki `gonderi_yap`, günlük için bir `gunluge_ekle`, sonunda `goster`.

Yasağı yönergeye de yazabilirsin (`... + STIL + ", no orange, no red"`). Bu modelde ayrı bir negatif
yönerge alanı yok (Konu 7); yasak, yönergenin içinde bir istek: bazen işe yarar, bazen yaramaz, dene ve gör.
Yönergeyi hiç değiştirmesen de yeni bir görsel gelir (aynı yönerge, başka görsel). Tek günü yenilemek bir
istek; bütün hafta beş istek olurdu ve iyi olan günler de değişirdi.

Sonraki hücre eskisini ve yenisini yan yana koyar. Yenisi uyduysa haftanın listelerinde o günün yerine
yenisini yazıp (Salı için `gonderiler[1]` ve `hikayeler[1]`; Pazartesi 0) onay sayfasını yeniden kurarsın;
uymadıysa bir deneme daha (`_3`). Eski dosya duruyor, günlükte de hangisinin nasıl üretildiği yazıyor.

## Bonus — Kendi müşterin

`veri/benim_takvimim.csv` dosyasında hayalî bir fotoğraf kulübünün üç günü var; satırları kendi müşterinle
değiştir, `BENIM_STILIM` cümlesini yeniden yaz. Çıktılar ve günlük `ciktilar/benim/` içine. Kendi renklerin
için: `gonderi_yap(..., zemin="#FFFFFF", renk="#222222")`.

Kendi stil cümleni kurarken: önce müşterinin görsel dilini Türkçe üç-dört öbekle yaz (renk, teknik,
doku, ne olmayacak), sonra her öbeği İngilizceye çevir. Yaşayan bir sanatçının adını stil olarak yazma
(Konu 7): üslubun özelliklerini yaz.

## Şeffaflık ve telif

- Müşteriye görsellerin yapay zekâyla üretildiğini söyle; teklifte ya da sözleşmede yaz. Bazı müşteriler
  sınır koyar (ör. "son işte üretilmiş insan görseli olmasın"). Günlük bunun kaydıdır.
- Yapay zekâ çıktısının kime ait olduğu birçok ülkede hâlâ tartışmalı. Başka bir markanın logosunu,
  ürününü ya da yaşayan bir sanatçının adını yönergeye koyma.

## Sık hatalar

| Ne gördün | Neden | Ne yap |
|---|---|---|
| `ModuleNotFoundError: No module named 'uretim'` | Defter `uretim.py` ile aynı klasörde değil | Defteri `08-koddan-toplu-uretim` içinde aç |
| `FileNotFoundError: anahtar.txt bulunamadı` | Anahtar dosyası `gita3111` klasöründe değil | Konu 2'deki dosyayı oraya koy |
| `KeyError: 'başlık'` | Sütunun adı `baslik` (Türkçe harfsiz) | Takvimin ilk satırındaki adı aynen yaz |
| `KeyError: 'gun'` (kendi takviminde) | Excel'in gizli işareti ya da Türkçe Excel'in noktalı virgülü | `utf-8-sig` ile oku; takvimi VS Code'da ya da Google E-Tablolar'da hazırla (İndir → CSV) |
| Klasörde tek gönderi var | Döngüde dosya adı sabit | Adı günden kur: `f"ciktilar/{gun}_gonderi.jpg"` |
| Beğendiğin görsel gitti | Hücreyi yeniden çalıştırdın, aynı adlı dosyanın üstüne yazıldı | Yeni denemeyi yeni adla kaydet (`_2`) |
| `Görsel gelmedi (durum kodu 429)` | Çok sık istek ya da günlük kota | Biraz bekle; olmazsa yarın |
| `NameError: name 'STIL' is not defined` | Adım 2'nin hücresi çalışmadı | Yukarıdan sırayla çalıştır |
| `NameError: name 'secilen' is not defined` (Adım 5) | `gun` takvimdekinden farklı yazıldı (`Sali`), `if` hiç tutmadı | Gün adını takvimdeki gibi yaz |

## Kendini dene

1. Takvime Cumartesi eklenirse Adım 3'ün döngüsünde neyi değiştirmen gerekir?
2. Müşteri bütün başlıkları değiştirdi, görseller kalsın dedi. Kaç istek gider?
3. Stil cümlesinden `no text, no letters` öbeğini silersen ne olabilir? Neden riskli?
4. Aynı yönergeyle iki kez üretirsen iki görsel neden farklı çıkar, ama neden yine de birbirine benzer?
5. Onay sayfasında dosya adlarının yazması müşteriye ne kazandırır?

Cevaplar: (1) hiçbir şey; döngü tablodaki her satırı gezer. (2) sıfır; başlık Python'da. (3) model görsele
harfe benzeyen lekeler ya da uydurma yazılar koyabilir; üstüne başlık binince kalabalık ve marka dışı
görünür. (4) model her seferinde başka bir rastgele gürültüden başlar (tohum yok); ama yönerge ve stil
cümlesi aynı olduğu için renk, teknik ve konu aynı kalır. (5) geri bildirim dosyanın adıyla gelir.

## Sözlükçe

| Terim | Anlamı |
|---|---|
| **İçerik takvimi** | Hangi gün hangi başlıkla hangi görselin paylaşılacağını gösteren plan |
| **Gönderi / hikâye** | Akışta kalan paylaşım (burada 4:5, 1080 × 1350) / 24 saatlik dikey paylaşım (9:16, 1080 × 1920) |
| **Marka dili** | Bir markanın bütün işlerinde tekrar eden renk, teknik, ses ve düzen |
| **Stil cümlesi** | Marka dilinin görsel modeline yazılmış, her yönergeye eklenen sabit hâli |
| **Uyarlama** | Hazır bir görseli başka bir ölçüye ya da yerleşime koymak; kota yemez |
| **Onay sayfası** | Müşterinin bütün seti tek bakışta görüp adıyla geri bildirim verdiği sayfa |
| **Üretim günlüğü** | Her üretimin zamanını, yönergesini ve dosyasını tutan kayıt |
| **Kota** | Ücretsiz hesabın günlük hakkı; yalnızca üretim (istek) harcar |

## Ödev

`odevler/odev8.md`: kendi müşterin için 5 günlük takvim ve stil cümlesi → onay sayfası, takvim, günlük ve
üç cümle "stil cümlemi nasıl kurdum". Seçenek: logo teslim paketi. Gösterim Konu 9'un başında.

## Sonraki konu

**Konu 9 — Gönderini hareketlendir.** Bu haftanın yazısız görsellerinden (`ciktilar/..._gorsel.jpg`)
birini ücretsiz bir arayüzde 6 saniyelik dikey bir videoya çevireceğiz. Yazıyı ve logoyu yine sonradan biz ekleriz.
