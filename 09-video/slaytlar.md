# Konu 9 — Video, Arayüzden

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 8'den Konu 9'a: görselden videoya

- Konu 8'de görselleri koddan, bir döngüyle toplu olarak ürettik; her biri birkaç saniyede geldi
- Bugün görsele **zaman** ekliyoruz: birkaç saniyelik kısa video klipler
- Videoyu arayüzden üreteceğiz; kodu yalnızca hesap ve kayıt için yazacağız
- Neden arayüz? Görselde kullandığımız Cloudflare'de video modeli yok; Google'ın video API'si ise ücretli
- Arayüzlerin ücretsiz katmanı var ama sınırlı; her denemeyi düşünerek yapmak gerekiyor
- Konu 8'den gelen alışkanlıklar burada da geçerli: sınır koymak ve her üretimi kayda geçirmek

-----

## Video nedir: art arda gelen kareler

- Bir film şeridi düşün: her kare ayrı bir fotoğraf; kareler hızla art arda geçince göz hareket görür
- Sinema saniyede 24 kare kullanır; telefon videoları çoğunlukla 30, oyunlar 60 kare
- Video modeli tek bir görsel değil, birbirini **tutan** bir kare dizisi üretir
- Zor olan, kareleri çizmek değil; aralarındaki **tutarlılığı** korumak: bir fincan kare kare şekil değiştirmemeli, ışık bir anda zıplamamalı
- Bu yüzden video modeli görsel modelinden çok daha fazla hesap yapar; bir klibin gelmesi dakikalar sürebilir
- Bazı yeni modeller sesi de birlikte üretir: ortam sesi, efekt, bazen konuşma

-----

## Metinden video, görselden video

- **Metinden video:** sahneyi de hareketi de yönerge anlatır; kompozisyonu model kurar
- **Görselden video:** verdiğin görsel ilk kare olur; yönerge yalnızca **ne olacağını** anlatır
- Görselden video tasarımcıya kontrol verir: kompozisyonu, stili, rengi önceden sen belirlemiş olursun
- Bir afiş, ürün fotoğrafı ya da illüstrasyon "canlandırılmış" bir sosyal medya gönderisine dönüşür
- **Yanılgı:** "görseli verdim, video aynısı olur." Model hareket ederken görselde olmayanı da uydurur: nesnenin arka yüzü, gölgeler, değişen ışık

**Sohbete yaz:** senin işlerinden hangisi harekete en uygun olurdu? Neden?

-----

## İyi bir video yönergesinin parçaları

- Konu 7'de görsel yönergesinin parçaları özne, ortam, stil, ışık ve kompozisyondu; video yönergesine hareket, kamera ve süre de eklenir
- **Özne:** sahnede ne var? "Ahşap masada seramik bir fincan"
- **Hareket:** özne ne yapıyor? "Fincandan buhar yükseliyor", "yapraklar yavaşça düşüyor"
- **Kamera:** kamera ne yapıyor? Yaklaşıyor mu, sabit mi duruyor, yana mı dönüyor?
- **Süre ve tempo:** birkaç saniyede kaç şey olabilir? Hareket yavaş mı, hızlı mı?
- Öznenin hareketiyle kameranın hareketini ayrı cümlelerle yaz; ikisi karışınca model birini atlayabilir
- Ses istiyorsan onu da yaz: "yağmur sesi", "kafe uğultusu"; yazmazsan seçimi modele bırakmış olursun

-----

## Kamera dili

- Görüntü yönetmenlerinin yüz yıldır kullandığı kamera terimleri, modelin eğitim verisinde de sık geçer; yönergede İngilizce adlarıyla yazmak çoğu zaman daha iyi sonuç verir
- **Yaklaşma (push in):** kamera özneye doğru ilerler; dikkat ve gerilim yaratır
- **Uzaklaşma (pull out):** kamera geri çekilir; bağlam ortaya çıkar
- **Yana dönüş (pan):** kamera yerinde durur, başını sağa ya da sola çevirir; mekânı tanıtır
- **Yukarı dönüş (tilt up):** kamera yine yerinde, başını aşağıdan yukarı kaldırır; büyüklük duygusu verir
- **Sabit çekim (static shot):** kamera kıpırdamaz; hareketi yalnızca özne taşır, ürün tanıtımında sık kullanılır
- Bir klipte tek bir kamera hareketi seç; üç hareketi birden isteyen yönerge dağınık bir klip çıkarabilir

-----

## Süre, çözünürlük, oran

- **Süre:** model tek seferde birkaç saniyelik kısa bir klip üretir; uzun video, birkaç klibin kurguda birleşmesidir
- **Çözünürlük:** görüntünün piksel boyutu (720p, 1080p, 4K); büyüdükçe modelin yaptığı hesap da artar
- **Oran (Konu 7'deki en-boy oranı):** 16:9 yatay (ekran, sunum), 9:16 dikey (telefon, hikâye, kısa video), 1:1 kare (sosyal medya akışı)
- Metinden videoda oran değişince model sahneyi o çerçeveye göre yeniden kurar; dikey klip, yatayın kırpılmış hâli değildir
- Kararı yayın yeri verir: telefonda izlenecek birkaç saniyelik bir hikâyede en yüksek çözünürlüğün farkı çoğu zaman görülmez
- Her ayar bir bütçe kararıdır; "en yüksek kalite" her zaman doğru cevap değildir

-----

## Neden video görselden pahalı?

- Bir görsel tek bir kare; bir saniyelik video onlarca tutarlı kare, bazen üstüne ses
- Video modelleri büyük ve pahalı donanımda çalışır; ücretli API'ler videoyu **saniye başına** ücretlendirir
- Saniye fiyatı çözünürlüğe göre değişir; bir videonun bedeli kabaca "süre × o çözünürlüğün saniye fiyatı"
- Fatura yalnızca beğendiğin klibi değil, **her denemeyi** sayar; videoda deneme-yanılma pahalıya gelir
- Bu yüzden iş akışı ucuzdan pahalıya gider: önce görseli onaylat, sonra kısa ve düşük çözünürlüklü bir klip dene, en son asıl klibi üret
- Fiyatlar sık değişir: bir projeye başlamadan önce sağlayıcının fiyat sayfasına bakmak işin parçasıdır

-----

## Ücretsiz arayüz, görünmeyen fatura

- Ücretsiz arayüzler videoyu bir **kredi** karşılığında üretir: Konu 8'deki günlük neuron kotası gibi, kredi bitince ertesi günü beklersin
- Harcanan kredi de tıpkı para gibi süre ve çözünürlükle artar: uzun ve büyük klip daha çok kredi yer
- Ücretsiz katmanlar yoğun saatlerde yavaşlayabilir ya da üretimi durdurabilir; öncelik ücretli kullanıcıdadır
- Ücretsiz katmanın da bir amacı var: sağlayıcı seni ücretli pakete alıştırmak ister
- Kart bilgisi isteyen "ücretsiz" bir teklif, iptal etmeyi unutursan ücretli bir aboneliğe dönüşebilir
- Ücretli de olsa ücretsiz de olsa soru aynı: bu klip kaç denemeye, hangi ayara değer?

-----

## Uzun süren iş: kuru temizleme fişi

- Kuru temizlemeciye ceketini bırakırsın; karşılığında ceketi değil, bir **fiş** alırsın
- Tezgâhın önünde saatlerce beklemezsin; başka işine gidersin, sonra uğrayıp "hazır mı?" diye sorarsın
- Video da böyle üretilir: isteği **başlatırsın**, sunucu işi arka planda sürdürür, hazır olunca sonucu alırsın
- Arayüz bu beklemeyi senin yerine yönetir: arada bir "bitti mi?" diye sorar, bitince videoyu gösterir
- Koddan üretimde bu döngüyü programcı yazar: işi başlat, fişin numarasını sakla, aralıklarla sor, bitince indir
- Programcılar buna **asenkron** (eşzamanlı olmayan) iş der: isteği gönderdiğin anda sonuç gelmez
- **Yanılgı:** "cevap gelmedi, demek ki çalışmadı." Uzun işlerde bu çoğu zaman yalnızca **henüz bitmedi** demektir

-----

## Beklemenin arayüz tasarımı

- Kullanıcı ne olduğunu bilmezse bekleyemez: sayfayı yeniler, düğmeye bir daha basar
- İyi arayüzler bekleme sırasında haber verir: yükleme göstergesi, ilerleme çubuğu, "yaklaşık 2 dakika"
- Video üreten bir arayüz de bir şey göstermeli: bir ilerleme, tahmini bir süre ya da "hazır olunca burada görünecek" gibi bir söz
- Yanlış bekleme tasarımı pahalıya patlar: kullanıcı aynı isteği iki kez gönderirse iki kez öder
- Bekleme anı da tasarımın parçası: ne gösterilir, ne zaman, hangi sözle?

**Sohbete yaz:** en son hangi uygulamada beklerken ne olduğunu anlamadın? Ne gösterseydi rahatlardın?

-----

## Etik: hareket eden görüntüye güven

- Gerçekçi video üreten bir model, sahte haber ve birini taklit eden içerik (deepfake) için de kullanılabilir
- Sağlayıcılar gerçek kişi, ünlü ve çocuk içeren istekleri sınırlıyor; görselden videoda istek reddedilebilir
- Google gibi büyük sağlayıcılar ürettikleri videolara gözle görülmeyen bir **filigran** gömüyor; içeriğin yapay zekayla üretildiği sonradan bir yazılımla tespit edilebiliyor
- Konu 7'de yaşayan bir sanatçının adını stil olarak yazmadık; videoda kural genişliyor: yaşayan bir kişinin yüzünü, sesini, adını izinsiz kullanma
- Şeffaflık: bir işte yapay zeka videosu kullandıysan bunu söylemek mesleki bir alışkanlık olmalı
- Üretim günlüğü burada da şeffaflığın kanıtıdır: hangi araç ve model, hangi yönerge, hangi görselden

-----

## Bu konunun ödevi

**Görselin hareketlensin.**

1. Konu 8'de ürettiğin görsellerden birini seç: harekete en uygun olanı
2. Bir hareket yönergesi yaz: kameranın ve öznenin hareketini ayrı ayrı anlat
3. Arayüzde görselden bir klip üret, indir
4. Klibi video günlüğüne kaydet: yönerge, araç ve model, süre, çözünürlük, oran ve beğenip beğenmediğin
5. **İki cümle:** görsel hareket edince ne korundu, ne bozuldu? Bu görsel harekete uygun muydu?
6. **Bir cümle:** bu klip ücretli bir API'yle 1080p'de koddan üretilseydi kaça mal olurdu; daha ucuz hangi ayar işini görürdü?

Ayrıntılar: `odevler/odev9.md`. Puan yok; Konu 11'in başında sıradaki arkadaşlar gösterecek.

-----

## Hatırlanacaklar

1. **Video bir kare dizisidir.** Zor olan kareler arası tutarlılık; bu yüzden yavaş ve pahalı
2. **Görselden video kontrol verir.** Görsel ilk kare olur; yönerge ne olacağını, kamera dili nasıl görüneceğini anlatır
3. **Yönergenin parçaları:** özne, hareket, kamera, süre; öznenin hareketi ile kameranınki ayrı cümlelerde
4. **Her ayar bir bütçe kararı.** Süre ve çözünürlük fiyatı belirler; seçimi yayın yeri yapar
5. **Uzun süren iş:** başlat, başka işe geç, hazır olunca dön; "gelmedi" çoğu zaman "henüz bitmedi" demek
6. **Kayıt:** her klibin yönergesi ve ayarları günlükte; arayüzün geçmişi senin dosyan değil

Sıradaki konu: **Konu 10 — Zincirleme: üretim hattı.** Metin ve görsel modellerini tek bir programda birbirine bağlıyoruz: bir adımın çıktısı ötekinin girdisi.
