# Konu 2 — İnterneti Koddan Konuşturmak

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Kodun ilk kez bilgisayarının dışına çıkıyor

![Konu 1'de kod ve veri aynı bilgisayardaydı; Konu 2'de model uzakta](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/yerel_uzak.png)

- **Konu 1'in bulgusu:** müşteriler kafeyi **sessiz bir çalışma yeri** olarak anlatıyor
- **Bugün** o kafe için uzaktaki bir modele soru soracağız
- Dersin **kritik konusu**: sonraki konuların çoğu bunun üstüne kuruluyor

-----

## Bugünün sorusu

**Kodumuz uzaktaki bir modele nasıl soru sorar, gelen cevabı nasıl okur?**

- Soruyu paketleyip göndermek
- Gelen cevabın içinden metni çıkarmak
- Bir şey bozulunca bunu anlamak
- Soruya bağlam yazınca cevabın değişip değişmediğine bakmak

**Sohbete yaz:** bir sohbet sitesinde soruyu yazıp Enter'a bastığında sorun nereye gidiyor?

-----

## API, mutfağa giremeyen müşteri için bir garson

![Müşteri, garson ve mutfak; altta kodun, API ve model](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/api_garson.png)

- Mutfağa (modele) giremezsin, siparişi garsona (API'ye) verirsin
- Sohbet sitesinde Enter'a basınca olan da bu; bugün siparişi arayüzsüz, koddan veriyoruz
- Mutfak başkasının (Cloudflare): bu yüzden internet, kota ve kimlik gerekir

-----

## Her istek üç soruya cevap verir

![Adres, başlık ve gövde kartları](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/istek_parcalari.png)

- **Adres**: nereye gidiyorum (hangi model)
- **Başlık**: ben kimim (anahtar burada gider)
- **Gövde**: ne istiyorum (soru)

-----

## Anahtar senin imzan: koda yazılmaz

![Anahtar ayrı dosyada; üç kural](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/anahtar_imza.png)

- Başkasının eline geçerse **senin adına** istek atar, kotanı bitirir
- Cloudflare buna **token** diyor; derste "anahtar" diyoruz, ikisi aynı şey
- Yanlışlıkla paylaştıysan panik yok: panelden silip yenisini üretmek bir dakika

-----

## Cevap düz metin değil, iç içe kutular

![yanit kutusunun içinde result, onun içinde response](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/yanit_katmanlari.png)

- Konu 1'deki sözlüğün aynısı; tek fark, kutunun içinde kutu olması
- Metin en içte: önce `result` katına, sonra `response` katına inersin

**Tahmin et, sohbete yaz:** en dış kutudan doğrudan `response`'u istersen ne olur? Isınmada deneyeceğiz.

-----

## Durum kodu, cevabı okumadan önce ne olduğunu söyler

![200, 401, 404, 429 kartları](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/durum_kodlari.png)

- Gelen pakette iki şey var: **durum kodu** ve **yanıt**
- İlk hane kime bakacağını söyler: **4xx senin tarafın**, **5xx sunucunun**
- Kural: **200 değilse içine girme**; başarısız yanıtın içinde metin yok

-----

## Fonksiyon bir makine: bir kez yaz, istediğin kadar sor

![modele_sor makinesi ve içindeki dört adım](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/fonksiyon_makine.png)

- Bir soru için yaptığımız dört iş tek bir ada toplanıyor: `modele_sor`
- Makineye yalnızca değişen şeyi veriyoruz: soruyu
- Sonra elli soruyu döngüyle sorup cevapları tek dosyaya yazıyoruz: arayüzde yapamayacağın iş

-----

## Bağlam cevabı değiştirir mi?

![Bağlamsız ve bağlamlı iki soru yan yana; cevaplar boş](https://raw.githubusercontent.com/aladagemre/gita3111/main/02-api-ile-konusmak/gorseller/baglam_karsilastirma.png)

**Çalıştırmadan önce tahmin et, sohbete yaz:** hangi cevapta "kahve" geçecek, hangisinde "sessizlik", "odak"?

İki cevabı defterin son adımında yan yana okuyacağız.

-----

## Şimdi deftere geçiyoruz

`ders.ipynb`, yukarıdan aşağı:

- **Isınma:** iç içe sözlük
- **Adım 1–3:** anahtarı oku, isteği hazırla (adres, başlık, gövde), gönder
- **Adım 4–5:** yanıtın içine in; yanlış anahtarla dene
- **Adım 6–8:** fonksiyon, çok soru ve dosya, bağlam

Konu 1'deki gibi: çekirdek **`.venv`**, **Shift + Enter**, hücreler **sırayla**; atlarsan `NameError`.

-----

## Anahtarın yoksa?

Adım 1 `anahtar.txt` ister; dosya yoksa `FileNotFoundError` ile durur.

- Ders boyunca **yanındakiyle birlikte** çalış: onun ekranında izle, hücreleri sen de yaz
- Isınma ve alıştırma defteri (`alistirma.ipynb`) anahtarsız çalışır
- Konu 00'daki kurulum yönergesinin **6. adımını** (Cloudflare hesabı) bugün bitir

Ödev için kendi anahtarın gerekiyor; Konu 4'ten itibaren her derste de gerekecek.

-----

## Soru yazmak da tasarım

- Model senin kafeni tanımıyor; ona ne söylersen onu biliyor
- Konu 1'de veriden bulduğumuz şey ancak soruya yazınca cevaba girebilir
- Model her seferinde başka cümle kurar: tek cevaba değil, birkaç denemedeki yöne bak

Soruyu yazmak bir **brief** yazmak gibi.

**Sohbete yaz:** bağlamlı sloganlardan hangisini kafenin afişine koyardın, neden?

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
