# Konu 9 — Video Üretimi

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 8'den Konu 9'a: görsele zaman ekliyoruz

- Konu 8'de görselleri koddan ürettik, bir döngüyle birçoğunu birden; her biri birkaç saniyede geldi
- Bugün görsele **zaman** ekliyoruz: birkaç saniyelik kısa video klipler
- Videoyu arayüzden üreteceğiz; kod yalnızca hesap ve kayıt için
- Neden arayüz? Video modellerinin ücretsiz bir API'si yok: koddan üretmek her saniye için para ödemek demek
- Arayüzlerin ücretsiz katmanı var ama sınırlı; her denemeyi düşünerek yapmak gerekiyor
- Konu 8'den gelen alışkanlıklar burada da geçerli: sınır koymak ve her üretimi kayda geçirmek

-----

## Video nedir: art arda gelen kareler

- Bir film şeridi düşün: her kare ayrı bir fotoğraf; kareler hızla art arda geçince göz hareket görür
- Sinema saniyede 24 kare kullanır; telefon videoları çoğunlukla 30, oyunlar 60 kare
- Video modeli tek bir görsel değil, birbirini **tutan** bir kare dizisi üretir
- Zor olan kareleri çizmek değil, aralarındaki **tutarlılık**: fincan kare kare şekil değiştirmemeli, ışık bir anda zıplamamalı
- Bu yüzden video modelleri görsel modellerinden çok daha fazla hesap yapar; hem yavaş hem pahalıdır
- Yeni modellerin çoğu sesi de birlikte üretir: ortam sesi, efekt, bazen konuşma

-----

## Metinden video, görselden video

- **Metinden video:** sahneyi de hareketi de yönerge anlatır; kompozisyonu model kurar
- **Görselden video:** verdiğin görsel ilk kare olur; yönerge yalnızca **ne olacağını** anlatır
- Görselden video tasarımcıya kontrol verir: kompozisyonu, stili, rengi önceden sen belirlemiş olursun
- Ajanslarda sık görülen bir iş akışı: önce görseli onaylat (ucuz), sonra hareket ver (pahalı)
- Bir afiş, ürün fotoğrafı ya da illüstrasyon "canlandırılmış" bir sosyal medya gönderisine dönüşür
- **Yanılgı:** "görseli verdim, video aynısı olur." Model hareket ederken görselde olmayanı da uydurur: nesnenin arka yüzü, gölgeler, değişen ışık

**Sohbete yaz:** senin bir işinden hangisi harekete en uygun olurdu? Neden?

-----

## İyi bir video yönergesinin parçaları

- Görsel yönergesinde özne, stil ve ışık vardı (Konu 7); videoda bunlara **zaman** ekleniyor
- **Özne:** sahnede ne var? "Ahşap masada seramik bir fincan"
- **Hareket:** özne ne yapıyor? "Fincandan buhar yükseliyor", "yapraklar yavaşça düşüyor"
- **Kamera:** kamera ne yapıyor? Yaklaşıyor mu, sabit mi duruyor, yana mı kayıyor?
- **Süre ve tempo:** birkaç saniyede kaç şey olabilir? Kısa bir klipte tek bir hareket genellikle yeter
- Öznenin hareketiyle kameranın hareketini ayrı cümlelerle yaz; karışınca model ikisinden birini atlar
- Ses istiyorsan onu da yaz: "yağmur sesi", "kafe uğultusu"; yazmazsan model kendisi seçer

-----

## Kamera dili

- Sinematografların yüz yıldır kullandığı terimler modelin eğitim verisinde de sık geçer; İngilizce adlarıyla yazmak çoğu zaman daha iyi sonuç verir
- **Yaklaşma (push in):** kamera özneye doğru ilerler; dikkat ve gerilim yaratır
- **Uzaklaşma (pull out):** kamera geri çekilir; bağlam ortaya çıkar
- **Yana kaydırma (pan):** kamera döner ya da kayar; mekânı tanıtır
- **Yukarı kalkış (tilt up):** kamera alttan yukarı bakar; büyüklük duygusu verir
- **Sabit çekim (static shot):** kamera kıpırdamaz; hareketi yalnızca özne taşır, ürün tanıtımında sık kullanılır
- Bir klipte tek bir kamera hareketi seç; üç hareketi birden isteyen yönerge çoğu zaman karmaşık bir sonuç verir

-----

## Süre, çözünürlük, oran

- **Süre:** model tek seferde kısa klipler üretir, birkaç saniyelik; uzun bir video, kliplerin kurguda birleşmesidir
- **Çözünürlük:** görüntünün piksel boyutu: 720p, 1080p, 4K; çözünürlük arttıkça hesap ve fiyat artar
- **Oran:** 16:9 yatay (ekran, sunum), 9:16 dikey (telefon, hikâye, kısa video), 1:1 kare (akış)
- Oran değişince model sahneyi yeniden kurar; dikey video, yatayın kırpılmış hâli değildir
- Kararı yayın yeri verir: telefonda izlenecek birkaç saniyelik bir hikâyede en yüksek çözünürlüğün farkı çoğu zaman görülmez
- Her ayar bir bütçe kararıdır; "en yüksek kalite" her zaman doğru cevap değildir

-----

## Neden video görselden pahalı?

- Bir görsel tek bir kare; bir saniyelik video onlarca kare, üstüne ses ve kareler arası tutarlılık
- Video modelleri büyük ve pahalı donanımda çalışır; ücretli API'ler bunu **saniye başına** ücretlendirir
- Saniye fiyatı çözünürlüğe göre değişir; bir videonun bedeli kabaca "süre × o çözünürlüğün saniye fiyatı"
- Görselde ücretsiz bir günlük kota vardı (Cloudflare); videonun ücretsiz bir API katmanı yok
- Fatura yalnızca beğendiğin klibi değil, **her denemeyi** sayar; video denemesi pahalı bir alışkanlıktır
- Bu yüzden iş akışı ucuzdan pahalıya gider: önce görselle dene, sonra kısa ve düşük çözünürlüklü bir klip, en son asıl klip
- Fiyatlar sık değişir: bir projeye başlamadan önce sağlayıcının fiyat sayfasına bakmak işin parçası

-----

## Ücretsiz arayüz, görünmeyen fatura

- Ücretsiz arayüzler videoyu bir **kredi** ya da günlük hak karşılığında üretir; kredi bitince ertesi günü beklersin
- Kredi de tıpkı para gibi süre ve çözünürlükle artar: uzun ve büyük klip daha çok kredi yer
- Ücretsiz katmanlar yoğun saatlerde yavaşlayabilir ya da üretimi durdurabilir; ücretli kullanıcı önce gelir
- Ücretsiz araç bedava değildir: sağlayıcı seni ücretli pakete alıştırmak ister; deneme süresinden sonra ücret başlayabilir
- Kart bilgisi isteyen "ücretsiz" bir teklif, iptal etmeyi unutursan ücretli bir aboneliğe dönüşür
- Tasarımcı için soru aynı kalır: bu klip kaç denemeye ve hangi ayara değer?

-----

## Uzun süren iş: kuru temizleme fişi

- Kuru temizlemeciye ceketini bırakırsın; ceketi o an almazsın, bir **fiş** alırsın
- Tezgâhın önünde saatlerce beklemezsin; başka işine gidersin, sonra uğrayıp "hazır mı?" diye sorarsın
- Video da böyle üretilir: istek **başlar**, sunucu işi arka planda sürdürür, hazır olunca sonucu alırsın
- Arayüz bu beklemeyi senin yerine yönetir: arada bir "bitti mi?" diye sorar, bitince videoyu gösterir
- Koddan üretimde bu işi programcı yazar: işi başlat, iş numarasını sakla, aralıklarla sor, bitince indir
- Programcılar buna **asenkron** (eşzamanlı olmayan) iş der: istek ile sonuç aynı anda gelmez
- **Yanılgı:** "cevap gelmedi, çalışmadı." Uzun işlerde çoğu zaman yalnızca **henüz bitmedi**

-----

## Beklemenin arayüz tasarımı

- Kullanıcı ne olduğunu bilmezse bekleyemez: sayfayı yeniler, düğmeye bir daha basar
- İyi arayüzler bekleme sırasında konuşur: yükleme göstergesi, ilerleme çubuğu, "yaklaşık 2 dakika"
- Video üreten arayüzler de ilerlemeyi gösterir ya da "hazır olunca burada görünecek" der
- Yanlış bekleme tasarımı pahalıya patlar: kullanıcı aynı isteği iki kez gönderirse iki kez öder
- Tasarımcı olarak bekleme anını da tasarlarsın: ne gösterilir, ne kadar sürede, hangi sözle

**Sohbete yaz:** en son hangi uygulamada beklerken ne olduğunu anlamadın? Ne gösterseydi rahatlardın?

-----

## Etik: hareket eden görüntüye güven

- Gerçekçi video, sahte haber ve kişiyi taklit eden içerik (deepfake) üretmek için de kullanılabilir
- Sağlayıcılar insan yüzü, ünlü kişi ve çocuk içeren istekleri sınırlıyor; görselden videoda istek reddedilebilir
- Büyük sağlayıcılar ürettikleri videolara gözle görülmeyen bir **filigran** gömüyor; içeriğin yapay zekayla üretildiği sonradan tespit edilebiliyor
- Konu 7'deki kural videoda daha da önemli: yaşayan bir kişinin yüzünü, sesini, adını izinsiz kullanma
- Şeffaflık: bir işte yapay zeka videosu kullandıysan bunu söylemek mesleki bir alışkanlık olmalı
- Üretim günlüğü burada da şeffaflığın kanıtıdır: hangi araç, hangi yönerge, hangi görselden

-----

## Bu konunun ödevi

**Görselin hareketlensin.**

1. Konu 8'de ürettiğin görsellerden birini seç: harekete en uygun olanı
2. Bir hareket yönergesi yaz: kameranın ve öznenin hareketini ayrı ayrı anlat
3. Arayüzde görselden bir klip üret, indir
4. Klibi video günlüğüne kaydet: yönerge, süre, çözünürlük, araç, beğendin mi
5. **İki cümle:** görsel hareket edince ne korundu, ne bozuldu? Bu görsel harekete uygun muydu?
6. **Bir cümle:** bu klip ücretli bir API'yle 1080p'de koddan üretilseydi kaça mal olurdu; daha ucuz hangi ayar işini görürdü?

Ayrıntılar: `odevler/odev9.md`. Puan yok; Konu 11'in başında sıradaki arkadaşlar gösterecek.

-----

## Hatırlanacaklar

1. **Video bir kare dizisidir.** Zor olan kareler arası tutarlılık; bu yüzden yavaş ve pahalı
2. **Görselden video kontrol verir.** Görsel ilk kare olur; yönerge ne olacağını, kamera dili nasıl görüneceğini anlatır
3. **Yönergenin parçaları:** özne, hareket, kamera, süre; özne ve kamera ayrı cümlelerde
4. **Her ayar bir bütçe kararı.** Süre ve çözünürlük fiyatı belirler; seçimi yayın yeri yapar
5. **Uzun süren iş:** başlat, başka işe geç, hazır olunca dön; "gelmedi" çoğu zaman "henüz bitmedi" demek
6. **Kayıt:** her klibin yönergesi ve ayarları günlükte; arayüzün geçmişi senin dosyan değil

Sıradaki konu: **Konu 10 — Zincirleme: üretim hattı.** Metin ve görsel modellerini tek bir programda birbirine bağlıyoruz: bir adımın çıktısı ötekinin girdisi.
