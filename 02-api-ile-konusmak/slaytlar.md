# Konu 2 — İnterneti Koddan Konuşturmak

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Kodun ilk kez bilgisayarının dışına çıkıyor

- Konu 1'de kod da veri de senin bilgisayarındaydı; her şey yerel
- Bugün kodumuz internet üzerinden **başka bir bilgisayardaki** bir yapay zeka modeline soru soracak
- O model çok büyük; dizüstü bilgisayarına sığmaz, güçlü sunucularda çalışır
- Sohbet sitelerinin yaptığı da bu: yazdığın soru uzaktaki bir modele gider, cevap geri gelir
- Bugün aynı işi arayüz olmadan, doğrudan koddan yapacağız
- Dersin **kritik konusu**: görsel üretimi, toplu üretim ve finaldeki araçlar bunun üstüne kuruluyor

**Sohbete yaz:** bir sohbet sitesinde soruyu yazıp Enter'a bastığında sorun nereye gidiyor?

-----

## İstemci ve sunucu

- İnternetteki her konuşmanın iki tarafı var: **istemci** soran, **sunucu** cevap veren
- Tarayıcında bir web sitesi açtığında tarayıcın istemci, sitenin bilgisayarı sunucu
- İstemci bir **istek** gönderir, sunucu bir **yanıt** döndürür
- Instagram'da akışı yenilemek, hava durumuna bakmak, harita açmak: hepsi istek ve yanıt
- Bugün istemci biziz: kodumuz istek gönderecek, yanıtı okuyacak
- Sunucu Cloudflare'in bilgisayarları; modeli onlar çalıştırıyor

-----

## API: mutfağa giremeyen müşteri için garson

- Bir restoranda mutfağa girip yemeği kendin yapamazsın; siparişi **garsona** verirsin
- Garson siparişi mutfağa iletir, yemeği sana getirir; mutfağın içini görmen gerekmez
- **API** (uygulama programlama arayüzü) programlar için garson: bir hizmete koddan nasıl sipariş verileceğini tanımlar
- Mutfak: yapay zeka modeli · garson: API · müşteri: senin kodun
- Garsonun dili bellidir: siparişi menüdeki biçimde vermezsen anlamaz
- Hava durumu uygulamaları, ödeme sayfaları, harita gömen siteler: hepsi başka bir hizmetin API'sini kullanır

-----

## Bir isteğin üç parçası

Her istek bir zarf gibi üç soruya cevap verir:

- **Adres — nereye?** Zarfın üstündeki adres: isteğin hangi sunucuya, hangi modele gideceği
- **Başlık — ben kimim?** Zarftaki imza: senin anahtarın burada gider
- **Gövde — ne istiyorum?** Zarfın içindeki mektup: modele sorduğun soru

- Üçünden biri eksik ya da yanlışsa istek ya hiç ulaşmaz ya da geri çevrilir
- Bütün API'ler bu üç parçayla çalışır; bugün öğrendiğin şey ileride görsel ve video üretiminde de aynı

-----

## Adres: hangi kapıya, hangi modele?

- İnternetteki her hizmetin bir adresi (URL) var; tarayıcının üstündeki adres çubuğundaki gibi
- Adresin başı **hangi sunucu** olduğunu söyler: örneğin `api.cloudflare.com`
- Devamı o sunucunun **hangi hizmeti** olduğunu söyler: bizim için hesabın ve kullanacağımız model
- Cloudflare'de onlarca model var; adresteki model adını değiştirince başka bir modelle konuşursun
- Model adları uzun ve tuhaf görünür: hangi firmanın modeli, kaçıncı sürümü, ne kadar büyük olduğu içinde yazar

-----

## Anahtar: senin imzan

- Sunucu her istekte "bu kim?" diye sorar; cevabı isteğin başlığındaki **anahtar** verir
- Cloudflare buna **token** diyor; derste "anahtar" diyoruz, ikisi aynı şey
- Anahtar bir şifre gibidir: kimin elindeyse **senin adına** istek atar ve kotanı bitirir
- Bu yüzden anahtar koda yazılmaz; ayrı bir dosyada durur, kod onu oradan okur
- Ekran paylaşırken, ödev teslim ederken, bir yere kod yapıştırırken anahtar görünmemeli
- Yanlışlıkla paylaştıysan panik yok: panelden silip yenisini üretmek bir dakika

-----

## Yanıt önce bir durum kodu söyler

- Sunucu her yanıtın başına üç haneli bir **durum kodu** koyar: "ne oldu?"
- **200** her şey yolunda · **400** isteğin biçimi bozuk · **401** anahtar yanlış · **403** anahtarın izni yok
- **404** böyle bir adres yok · **429** çok sık istek attın, biraz bekle · **500** sunucu tarafında sorun
- İlk hane kime bakacağını söyler: **4 ile başlıyorsa senin tarafında**, **5 ile başlıyorsa sunucuda**
- Tarayıcıda gördüğün "404 Not Found" sayfası da aynı sistem
- Kural: **200 değilse yanıtın içine girme**; başarısız yanıtın içinde cevap metni yoktur

-----

## Yanıtın içi: JSON, iç içe kutular

- Başarılı yanıt düz bir metin değil, **JSON** adlı bir biçimde gelir
- JSON, Konu 1'deki sözlüğün aynısı: anahtar ve değer çiftleri
- Tek fark, bir değerin içinde başka bir sözlük olabilmesi: kutunun içinde kutu

```json
{
  "success": true,
  "result": {
    "response": "Sessizliğin tadını çıkar."
  }
}
```

- Modelin cevabı en içte: önce `result` kutusunu açarsın, sonra içindeki `response`'u
- Hangi bilginin hangi kutuda olduğunu API'nin belgesi söyler

-----

## Kota, hız sınırı ve maliyet

- Model çalıştırmak pahalıdır: güçlü ekran kartları, elektrik, soğutma
- Bu yüzden her hizmet kullanımı ölçer ve sınırlar
- **Kota:** belli bir sürede kullanabileceğin toplam miktar; bizim derste ücretsiz kotayla çalışıyoruz
- **Hız sınırı:** kısa sürede çok fazla istek atarsan sunucu 429 der ve bekletir
- Ücretli hizmetlerde fiyat çoğunlukla gönderdiğin ve aldığın metnin uzunluğuna göre hesaplanır
- Tasarımcı için anlamı: toplu üretim yaparken hem süreyi hem bütçeyi planlamak gerekir

-----

## Neden arayüz değil de kod?

- Sohbet ekranında bir soru sorarsın, cevabı okursun; elli soruda elli kez kopyala-yapıştır
- Kodla aynı soruyu bir listedeki elli ürün, elli renk, elli slogan için tek seferde sorarsın
- Cevaplar otomatik olarak bir dosyaya yazılır; düzenli, karşılaştırılabilir
- Aynı kodu yarın tekrar çalıştırırsın: işin **tekrarlanabilir** olur
- Cevabı başka bir programa verebilirsin: bir grafiğe, bir görsel üreticiye, bir web sayfasına
- Dönemin ikinci yarısındaki bütün üretim araçları bu fikrin üstüne kurulu

-----

## Fonksiyon: bir kez kur, istediğin kadar kullan

- Bir soru sormak için birkaç iş yapıyoruz: isteği hazırla, gönder, durum koduna bak, cevabı çıkar
- Her soruda bunları baştan yazmak hem uzun hem hataya açık
- Hepsini tek bir adın altında toplarız: bir **fonksiyon**
- Fonksiyon bir makine gibi: içine soruyu koyarsın, cevap metni çıkar
- Makineye yalnızca **değişen** şeyi veririz; adres ve anahtar her seferinde aynı
- Geçen dönem öğrendiğin fonksiyon kavramı, bugün gerçek bir işin içinde

-----

## Model seni tanımıyor: bağlam

- Model senin kafeni, müşterini, projeni bilmez; yalnızca sorunda yazanı bilir
- "Bir kafe için slogan yaz" dersen her kafeye uyan sıradan bir cevap gelir
- Soruya arka plan bilgisi eklersen, yani **bağlam** verirsen, cevap o bilgiye göre şekillenir
- Konu 1'de yorumlardan çıkardığımız bulgu, ancak soruya yazılırsa cevaba girebilir
- Soruyu yazmak bir **brief** yazmak gibidir: hedef kitle, ton, kısıtlar, ne istemediğin
- İyi bir brief tasarımcıdan iyi iş çıkarır; iyi bir soru da modelden

-----

## Aynı soru, farklı cevap

- Aynı soruyu iki kez sorarsan büyük ihtimalle iki farklı cevap alırsın
- Bu bir hata değil; model cevabını her seferinde biraz rastlantıyla kurar (nedenini Konu 5'te göreceğiz)
- Tek bir cevaba bakıp "model bunu düşünüyor" demek yanıltıcı
- Bir fikri değerlendirmek için birkaç deneme yap, cevapların **ortak yönüne** bak
- Kodla bu kolay: aynı soruyu beş kez sorup beş cevabı yan yana koyarsın

-----

## Bu modelleri kim sağlıyor?

- **Cloudflare Workers AI:** farklı firmaların açık modellerini çalıştırıyor; derste bunu kullanıyoruz, ücretsiz kotası var
- **OpenAI, Anthropic, Google:** kendi modellerini kendi API'leriyle sunuyorlar, çoğunlukla ücretli
- Adres, anahtar ve gövdenin ayrıntıları değişir; mantık hep aynı
- Bir hizmette öğrendiğin şeyi diğerine birkaç satır değiştirerek taşırsın
- Görsel ve video üreten modeller de aynı şekilde API ile çağrılır

-----

## Bu konunun ödevi: iki parça

**1. Kendi soruların.** Dersteki defteri yeni bir adla kopyala, aynı konuda **kendi beş sorunu** yaz, çalıştır, `cevaplar.txt` dosyasını getir. Tek soru cevapla: hangi cevap işe yaramazdı, neden?

**2. Renk etiketleme.** `veri/renkler.csv` dosyasını kendi adınla kopyala, 20 renge birer duygu etiketi ver: sakin / enerjik / ciddi.

- İkinci parça **Konu 3'ün verisi**: sınıfın etiketleriyle bir model eğiteceğiz
- Doğru cevap yok; herkesin etiketi farklı olacak, olmalı da

-----

## Hatırlanacak dört şey

1. **Bir istek üç şeyden oluşur:** nereye (adres), kim olduğun (başlık), ne istediğin (gövde)
2. **Önce durum koduna bak, sonra kutuları aç.** 200 değilse içinde cevap yok
3. **Anahtar koda yazılmaz.** Ayrı dosyada durur, teslime konmaz, ekranda gösterilmez
4. **Model yalnızca sorunda yazanı bilir.** Bağlam vermezsen sıradan cevap alırsın

Sıradaki konu: **Konu 3 — Makine öğrenmesi.** Sınıfın etiketlediği renklerle kendi modelimizi eğiteceğiz.
