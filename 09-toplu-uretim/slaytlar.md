# Konu 9 — Ölçek: Toplu Üretim

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 8'den Konu 9'a: "neden kod öğreniyorum?"

- Konu 8'de tek bir görseli üretip düzenli bir adla kaydettik ve hataları yakaladık
- Bir görsel için bunu arayüzde de yapabilirdin; birkaç tıklama
- Bugün arayüzün **yapamadığı** işe geçiyoruz: onlarca görseli tek seferde, düzenli ve kayıtlı üretmek
- Dönemin başından beri sorulan "neden kod öğreniyorum?" sorusunun cevabı bu konu
- Yeni olanlar: kombinasyon, şablon, güvenlik sınırı ve kaldığı yerden devam
- Sonra: kendiliğinden yazılan bir üretim günlüğü ve bütün görselleri tek sayfada gösteren bir kontak sayfası
- Hepsi Konu 8'deki `ciz` fonksiyonunun ve dosyaya yazma deseninin üstüne kuruluyor
- Konu 8'in son Bonus sorusu: birkaç stil ve rengin bütün eşleşmelerini nasıl üretirdin, ortadaki bir istek hata verirse ne olur? Bugün ikisini de cevaplıyoruz

-----

## Arayüzün yapamadığı: ölçek

- Bir e-ticaret sitesi 200 ürün için aynı tarzda arka plan görseli istiyor
- Bir festival afişi 6 dilde, 3 ölçüde, 2 renk temasında hazırlanacak: 36 dosya
- Bir marka yeni kimliği için 4 stil × 5 renk paletini müşteriye göstermek istiyor
- Arayüzde her biri ayrı bir yönerge, ayrı bir tıklama, ayrı bir "indir" demek: saatler ve hata
- Kodda bir şablon ve birkaç liste: aynı iş birkaç dakika, her dosya düzenli adlı ve kayıtlı
- Brifi yazmak ve seçmek yine tasarımcının işi; kod yalnızca tekrar eden kısmı üstleniyor

-----

## Kombinasyon: gardırop benzetmesi

- 2 tişört ve 5 pantolonun var: kaç farklı kombin? Her tişört her pantolonla: 2 × 5 = 10
- Bir de 3 ayakkabı eklersen 2 × 5 × 3 = 30; her yeni liste sayıyı **çarpar**
- Görselde de aynısı: stiller × renkler × tohumlar
- Bu çarpma hızla büyür: 4 stil × 7 renk × 3 tohum = 84 görsel
- Buna **kombinatoryal patlama** denir; kotayı ve zamanı yiyen şey budur
- Bu yüzden toplu üretim bir **hesapla** başlamalı: kaç görsel, ne kadar kota?

**Sohbete yaz:** senin bir projende hangi iki şeyi her biri öbürüyle eşleşecek biçimde denemek isterdin? (Ör. 3 yazı tipi × 4 renk: 12 deneme)

-----

## Şablon: sabit kısım ve boşluklar

- Bir **şablon**, sabit bir kısım ve doldurulacak boşluklardan oluşur
- Yönergede: "ahşap masada bir fincan, ___ stilinde, ___ paletiyle"
- Ofis programlarındaki "adres mektup birleştirme" de böyle: tek mektup, yüz farklı isim
- Tasarım sistemlerindeki bileşenler aynı mantıkla çalışır: aynı düğme, farklı metin ve renk
- Şablonun gücü tutarlılık: değişmesini istemediğin her şey sabit kalır
- Boşluklara giden kısa adlar (dosya adı için) ile uzun açıklamalar (model için) ayrı tutulursa her ikisi de temiz kalır

-----

## İç içe döngü: saat ve dakika

- Bir saati düşün: akrep bir saat ilerlerken yelkovan bir tam tur atar
- **İç içe döngü** de aynı mantıkla çalışır: dıştaki döngü bir adım atar, içteki döngü baştan sona döner
- Dıştaki her stil için içteki döngü bütün renkleri gezer; sonra dıştaki bir sonraki stile geçer
- Girinti hangi satırın hangi döngünün içinde olduğunu söyler
- **Yanılgı:** "hata çıkmadıysa kod doğrudur." İçteki işi yapan satır dıştaki döngünün hizasına kayarsa çoğu zaman hata çıkmaz; bazı kombinasyonlar sessizce kaybolur
- İki liste için iki döngü, üç liste için üç döngü; her yeni katman sayıyı çarpar

-----

## Kontrollü varyasyon: iki eksenli ızgara

- Konu 7'de bir seferde tek değişken değiştirdik; bugün geri kalan her şey sabitken iki değişkeni **düzenli** değiştiriyoruz
- Her stil her renkle bir kez: satırları stil, sütunları renk olan bir **ızgara** (tablo) düşün
- Bir satırın tamamı kötüyse sorun stilde; bir sütunun tamamı kötüyse renkte
- Yalnızca bir kutu kötüyse o eşleşmeye özgü bir sorun var
- Rastgele denemede bu ayrımı yapamazsın; düzenli ızgarada göz hemen görür
- Tohum sabit kalmalı: yoksa fark stilden mi renkten mi gürültüden mi, bilemezsin

-----

## Önce hesap, sonra üretim: kota ve sınır

- Ücretsiz kota günlüktür ve sınırlıdır; bir görsel üretimi ondan bir parça yer
- Döngüyü başlatmadan önce sor: kaç görsel, toplam ne kadar kota?
- Bir **güvenlik sınırı** koy: "en fazla şu kadar üret" (kredi kartındaki harcama sınırı gibi)
- Listeyi yanlışlıkla fazla büyütürsen sınır kotanın bir anda bitmesini önler
- Ücretli hizmetlerde aynı hata doğrudan para demek; profesyonel araçların çoğunda bütçe sınırı koyma seçeneği var
- İyi alışkanlık: önce küçük bir deneme (2–3 görsel), beğenirsen hepsi

-----

## Sağlamlık: bir hata bütün işi durdurmamalı

- Elli isteğin birinde internet kopabilir, sunucu meşgul olabilir, bir istek reddedilebilir
- Kötü bir program orada durur; sıradaki işler hiç yapılmaz
- Kuralları Konu 8'den biliyorsun: hatayı yakala, geçici hatada biraz **bekleyip yeniden dene**, deneme sayısına sınır koy
- Bugün bu kuralları tek bir yerde birleştiriyoruz: üç denemede de olmazsa program o işi bırakıp sıradakine geçer
- Kalıcı hatada (yanlış anahtar, kota bitti) beklemek işe yaramaz; basit bir program bunu ayırt edemez, programı sen durdurursun
- İyi bir program her işin sonucunu kaydeder: hangisi üretildi, hangisi olmadı; sonradan bakınca görürsün

-----

## Kaldığı yerden devam

- Uzun bir indirme yarıda kesilince indirme yöneticisi baştan başlamaz, kaldığı yerden devam eder
- Animasyon stüdyolarında saatler süren kare hesaplamaları (render) da böyle: biten kare yeniden hesaplanmaz
- Bunun için her çıktının **kararlı bir adı** olmalı: aynı iş, her zaman aynı ad
- Program her işten önce sorar: "bu dosya zaten var mı?" Varsa atlar
- Kota biterse ya da bağlantı koparsa, ertesi gün aynı programı çalıştırmak yeter
- Konu 8'deki tarihli adlar tek tek üretim için iyiydi; toplu üretimde kararlı adlar gerekir
- **Dikkat:** adda olmayan bir şeyi (özne, tohum) değiştirirsen program yeni iş olduğunu bilemez ve eskileri atlar; öyle bir değişiklikte yeni klasör aç

-----

## Üretim günlüğü: makinenin okuyabileceği kayıt

- Konu 7'de günlüğü elle tuttuk, Konu 8'de dosya adına sığdırdık; bugün program kendisi yazıyor
- Her görsel için: stil, renk, yönergenin tamamı, tohum, model
- Kayıt **JSON** biçiminde: insan okuyabilir, program geri okuyabilir (Konu 2'deki API cevaplarının biçimi)
- Bir müşteri aylar sonra "geçen seferki şu görselin aynısı" dediğinde bütün bilgi elinde
- Şeffaflık için de gerekli: hangi görselin nasıl üretildiğini göstermek (Konu 7: etik ve telif)
- Kayıt, üretimin bir parçası olmalı; sonradan hatırlamaya çalışılan kayıt eksik olur

-----

## Kontak sayfası

- Film fotoğrafçılığında bir rulodaki bütün kareler tek bir kâğıda küçük küçük basılırdı: **kontak sayfası**
- Fotoğrafçı en iyi kareyi bu sayfada seçip işaretlerdi; yalnızca o kare büyütülürdü
- Toplu üretimde aynı ihtiyaç: onlarca görseli tek tek açmak yerine hepsini tek bakışta görmek
- Düzen anlamlı olmalı: satırlar bir değişken, sütunlar öbürü; her kutunun üstünde ne olduğu yazar
- Sayfa bir **karar aracı**: onunla karşılaştırır, eler, kazananı seçersin
- Müşteriye sunumda da işe yarar: seçeneklerin tamamı ve aralarındaki düzen bir arada

-----

## Modele kendi çıktısını okutmak

- Bazı modeller hem metni hem görseli anlar: bunlara **çok kipli** (multimodal) ya da kısaca **görsel anlayan** modeller denir
- Bir görseli ve bir soruyu gönderirsin: "bu görsel brife ne kadar uyuyor?" Model cevap yazar
- Ölçekte işe yarar: 120 görseli gözle tek tek tartmak yerine model ilk elemeyi yapar
- Ama model bir **eleme aracı**, karar verici değil: onun da bir zevki ve yanlılığı var (Konu 3)
- Model brifteki kelimeleri senin gibi değil, eğitim verisindeki örneklere göre yorumlar
- Kural: model listeyi kısaltır, son kararı tasarımcı verir

-----

## Ölçeğin bir bedeli var

- Her görsel elektrik ve işlem gücü harcar; binlercesini üretip çoğunu silmek bir maliyettir
- "Ne olursa olsun yüz tane üret" kolay; iyi bir brif ve düşünülmüş bir tablo daha değerli
- Toplu üretim tasarımcıyı bir **küratöre** dönüştürür: üretmekten çok seçmek
- Seçmek için ölçüt gerekir: brif, hedef kitle, marka; bunlar kodda yazılı değil, onları sen bilirsin
- Az ama düzenli bir tablo, çok ama rastgele bir yığından daha çok şey öğretir

**Sohbete yaz:** bir müşteri senden 300 seçenek göstermeni isterse ne cevap verirsin?

-----

## Bu konunun ödevi

**Kendi ızgaran.**

1. Kendi konunda bir şablon kur: sabit bir özne, en az 2 stil, en az 3 renk (en fazla 12 görsel)
2. Dersteki defterin adımlarıyla ızgarayı üret, kontak sayfasını ve üretim günlüğünü kaydet
3. **İki cümle:** hangi kombinasyon kazandı, neden? Satır ya da sütun olarak bir eğilim var mı?
4. **Bir cümle:** görsel anlayan model de aynı kombinasyonu mu öne çıkardı?

Ayrıntılar: `odevler/odev9.md`. Görsellerini sakla: Konu 10'da birini videoya çevireceğiz. Puan yok; Konu 10'un başında sıradaki arkadaşlar gösterecek.

-----

## Beş cümlede toplu üretim

1. **Kombinasyon çarpılarak büyür.** Her yeni liste sayıyı çarpar; toplu üretim bir hesapla başlar
2. **Şablon tutarlılık sağlar.** Sabit kısım sabit kalır; kısa adlar dosya için, uzun açıklamalar model için
3. **Sınır koy, sağlam yaz.** Güvenlik sınırı, bekleyip yeniden deneme; bir hata bütün işi durdurmaz
4. **Kararlı ad, kaldığı yerden devam.** Aynı iş aynı ad; var olanı atla
5. **Kayıt, sayfa, seçim.** Günlük her şeyi kaydeder, kontak sayfası karşılaştırır, son kararı tasarımcı verir

Sıradaki konu: **Konu 10 — Video üretimi.** Hareket ekliyoruz. Video hem pahalı hem yavaş: sonuç hemen gelmez; bugünkü sınır ve kaldığı yerden devam orada daha da önemli.
