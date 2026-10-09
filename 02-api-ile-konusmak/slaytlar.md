# Konu 2 — İnterneti Koddan Konuşturmak

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Kodun ilk kez bilgisayarının dışına çıkıyor

![Konu 1'de kod ve veri aynı bilgisayardaydı; Konu 2'de model uzakta](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/yerel_uzak.png)

- **Konu 1'de** bulgu: müşteriler kafeyi **sessiz bir çalışma yeri** olarak anlatıyor
- **Bu konuda** o kafenin yeni kimliği için uzaktaki bir modele soru soracağız
- Dersin **kritik konusu**: Konu 4, 5, 8, 9, 10 ve 11 bunun üstüne kuruluyor

-----

## Bugünün sorusu

**Kodumuz uzaktaki bir modele nasıl soru sorar, gelen cevabı nasıl okur?**

- Soruyu paketleyip göndermek
- Cevabın içinden metni çıkarmak
- Bir şey bozulunca nerede bozulduğunu anlamak
- Soruya bağlam yazmanın cevabı değiştirip değiştirmediğine bakmak

-----

## API bir garson gibidir

![Müşteri, garson ve mutfak; altta kodun, API ve model](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/api_garson.png)

- Mutfağa (modele) giremezsin, siparişi garsona (API'ye) verirsin
- Sohbet sitesinde Enter'a bastığında da olan bu; bugün arayüzü kaldırıp siparişi kendimiz veriyoruz
- Mutfak başkasının: bu yüzden internet, kota ve kimlik gerekir

-----

## Bir soru beş durakta gidip geliyor

![Hazırlık, yol, kimlik, iş, dönüş](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/istek_yolculugu.png)

- Giden pakette üç şey var: adres, başlık, gövde
- Dönen pakette iki şey: bir durum kodu ve yanıtın kendisi
- Bugün konuştuğumuz model Cloudflare'de çalışıyor

-----

## Her istek üç soruya cevap verir

![Adres, başlık ve gövde kartları](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/istek_parcalari.png)

- **Adres**: nereye gidiyorum (hangi model)
- **Başlık**: ben kimim (anahtar burada gider)
- **Gövde**: ne istiyorum (soru)

Defterde üçü de sıradan Python değişkeni: bir metin, iki sözlük.

-----

## Anahtar senin imzan

![Anahtar ayrı dosyada; üç kural](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/anahtar_imza.png)

- Başkasının eline geçerse **senin adına** istek atar, kotanı bitirir
- Kod anahtarı `anahtar.txt`'den okur; defteri paylaşınca anahtar evde kalır
- Yanlışlıkla paylaştıysan panik yok: panelden silip yenisini üretmek bir dakika

-----

## Cevap düz metin değil, iç içe kutular

![yanit kutusunun içinde result, onun içinde response](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/yanit_katmanlari.png)

- Isınmadaki sözlüğün aynısı; gerçek yanıt yalnızca daha kalabalık
- Her satır **bir kat** iner: önce `result`, sonra `response`
- Kat atlarsan: `KeyError: 'response'`
- Sunucu bunu **JSON** olarak yollar: `true` → `True`, `null` → `None`

-----

## Durum kodu, cevabı okumadan önce ne olduğunu söyler

![200, 401, 404, 429 kartları](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/durum_kodlari.png)

- İlk hane kime bakacağını söyler: **4xx senin tarafın**, **5xx sunucunun**
- Bugün 401'i kendimiz, bilerek üreteceğiz

-----

## Hatanın türü, yolculuğun nerede koptuğunu gösterir

![Beş durak ve her birinin hata işareti](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/hata_nerede.png)

- Durum kodu bile gelmediyse sorun internette
- 401 geldiyse anahtarında
- `KeyError` geldiyse sunucu işini yapmış, sen içine yanlış yoldan giriyorsun

Hata mesajını **sondan** oku: en alt satır hatanın türü.

-----

## Önce durum koduna bak, sonra içine gir

![Durum kodu 200 ise içine gir, değilse açıklamayı oku](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/okuma_sirasi.png)

- Yanlış anahtarda `result` boş gelir (`None`)
- `TypeError: 'NoneType' ...` görürsen yazım hatası arama: **istek başarısız olmuş**

-----

## Fonksiyon bir makine: soru girer, cevap metni çıkar

![modele_sor makinesi ve içindeki dört adım](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/fonksiyon_makine.png)

- Her soru için aynı satırları yeniden yazmıyoruz
- Makineye yalnızca değişen şeyi veriyoruz: soruyu
- Adı `modele_sor`; bundan sonraki konularda hep bunu kullanacağız

-----

## Bir kez yaz, istediğin kadar sor

![Üç soru modele_sor'dan geçip cevaplar.txt dosyasına yazılıyor](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/dongu_dosya.png)

- Sorular bir listede, döngü her birini sırayla sorar
- Cevaplar tek dosyada toplanır: `cevaplar.txt`
- Kodun asıl gücü: aynı işi elli kez yapmak, arayüzde yapamayacağın şey

-----

## Bağlam cevabı değiştirir mi?

![Bağlamsız ve bağlamlı iki soru yan yana; cevaplar boş](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/baglam_karsilastirma.png)

**Çalıştırmadan önce tahmin et:** hangi cevapta "kahve" geçecek, hangisinde "sessizlik", "odak"?

İki cevabı derste yan yana okuyacağız.

-----

## Soru yazmak da tasarım

- Model senin kafeni tanımıyor; ona ne söylersen onu biliyor
- Konu 1'de veriden bulduğumuz şey ancak soruya yazınca cevaba girebilir
- Model her seferinde başka cümle kurar: hücreyi birkaç kez çalıştır, örüntü aynı yönde mi?
- Kelimeye değil, cümlenin ne anlattığına bak

Soruyu yazmak bir **brief** yazmak gibi.

-----

## Şimdi deftere geçiyoruz

`ders.ipynb`, yukarıdan aşağı:

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
- Sağ üstten çekirdek olarak **`.venv`**'i seç
- Hücreye tıkla, **Shift + Enter**: hücre çalışır, alttakine geçer
- Hücreler **yukarıdan aşağı, sırayla**: her hücre bir öncekinin değişkenini kullanır

Bir hücreyi atlarsan `NameError` alırsın. Çare: atladığın hücreye dön, oradan sırayla devam et.

-----

## Anahtarın yoksa?

Adım 1 `anahtar.txt` ister; dosya yoksa `FileNotFoundError` ile durur.

- Ders boyunca **yanındakiyle birlikte** çalış: onun ekranında izle, hücreleri sen de yaz
- Isınma ve alıştırma defteri (`alistirma.ipynb`) anahtarsız çalışır
- Konu 00'daki kurulum yönergesinin **6. adımını** (Cloudflare hesabı) bugün bitir

Ödev için kendi anahtarın gerekiyor; Konu 4'ten itibaren her derste de gerekecek.

-----

## Bu konunun ödevi — iki parça

**1. Kendi soruların.** `ders.ipynb`'yi yeni bir adla kopyala; Adım 7'deki listeye
aynı konuda **kendi beş sorunu** yaz, çalıştır, `cevaplar.txt` getir.
Tek soru cevapla: hangi cevap işe yaramazdı, neden?

**2. Renk etiketleme.** `veri/renkler.csv`'yi kendi adınla kopyala, 20 renge duygu
etiketi ver: sakin / enerjik / ciddi.

İkinci parça **Konu 3'ün verisi.** Doğru cevap yok; herkesin etiketi farklı olacak.

-----

## Hatırlanacak dört şey

**1. Bir istek üç şeyden oluşur:** nereye, kim olduğun, ne istediğin.

**2. Gelen cevap iç içe kutulardır.** Önce durum koduna bak, sonra kat kat in.

**3. Anahtar koda yazılmaz.** Ayrı dosyada durur, teslime konmaz, ekranda gösterilmez.

**4. Soruya yazdığın bağlam cevabı değiştirir.** Model senin bulgunu bilmez.

Sıradaki konu: **Konu 3 — makine öğrenmesi.** Sınıfın etiketlediği renklerle model eğiteceğiz.
