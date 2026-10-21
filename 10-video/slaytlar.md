# Konu 10 — Video Üretimi

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 9'dan Konu 10'a: hareket ekliyoruz

- Konu 9'da bir şablon ve listelerle bir görsel ızgarası ürettik; her görsel birkaç saniyede geldi
- Bugün görsele **zaman** ekliyoruz: kısa bir video klip
- Videoyu hem arayüzden hem koddan üreteceğiz; Konu 9'da seçtiğin görsel bir videonun ilk karesi olacak
- Yeni olan kodun kendisi değil, **bekleme**: video istediğin anda gelmez
- İsteği gönderirsin, bir numara alırsın, sonra arada bir "bitti mi?" diye sorarsın
- İkinci yeni şey **para**: görseller ücretsiz kotadan geliyordu, videonun her saniyesinin bir fiyatı var
- Konu 9'un kapanış sorusu: sonuç dakikalar sonra gelse ve her deneme para tutsa, sınır ve "kaldığı yerden devam" neden daha da önemli olur? Bugün cevaplıyoruz

-----

## Video nedir: art arda gelen kareler

- Bir film şeridi düşün: her kare ayrı bir fotoğraf; saniyede 24 kare hızla geçince göz hareket görür
- Video modeli tek bir görsel değil, birbirini **tutan** bir kare dizisi üretir
- Zor olan kareleri tek tek çizmek değil, aralarındaki **tutarlılık**: fincan kare kare şekil değiştirmemeli, ışık bir anda zıplamamalı
- Bu yüzden video modelleri görsel modellerinden çok daha fazla hesap yapar
- Yeni modellerin çoğu ses de üretir: ortam sesi, efekt, bazen konuşma
- Konu 6'daki gizli uzay burada da var; ama model kareleri tek tek değil, hepsini **birlikte** kurar: tutarlılık buradan gelir

-----

## Metinden video, görselden video

- **Metinden video:** sahneyi de hareketi de yönerge anlatır; kompozisyonu model kurar
- **Görselden video:** verdiğin görsel ilk kare olur; yönerge yalnızca **ne olacağını** anlatır
- Görselden video tasarımcıya kontrol verir: kompozisyonu, stili, rengi sen belirlemiş olursun
- Reklam ajanslarında sık bir iş akışı: önce görseli onaylat (ucuz), sonra hareket ver (pahalı)
- Afiş, ürün fotoğrafı ya da illüstrasyon "canlandırılmış" bir sosyal medya gönderisine dönüşür
- **Yanılgı:** "görseli verdim, video aynısı olur." Model hareket ederken görselde olmayanı da uydurur: nesnenin arka yüzü, gölgeler, değişen ışık

**Sohbete yaz:** senin bir işinden hangisi harekete en uygun olurdu? Neden?

-----

## Kamera dili: hareket yönergesi

- Görsel yönergesinde özne, stil, ışık vardı (Konu 7); videoda bir katman daha var: **kamera**
- **Yaklaşma (push in):** kamera özneye doğru ilerler; dikkat ve gerilim
- **Uzaklaşma (pull out):** kamera geri çekilir; bağlam ortaya çıkar
- **Yana kaydırma (pan):** kamera döner ya da kayar; mekânı tanıtır
- **Yukarı kalkış (tilt up):** alttan yukarı; büyüklük, ihtişam
- Sinematografların yüz yıldır kullandığı bu terimler modelin eğitim verisinde de sık geçer; o yüzden İngilizce adlarıyla yazmak çoğu zaman daha iyi sonuç verir
- Öznenin hareketi (buhar yükselir, yaprak düşer) ile kameranın hareketi ayrı şeylerdir; ikisini ayrı yaz

-----

## Süre, çözünürlük, oran

- **Süre:** model tek seferde kısa klipler üretir (birkaç saniye); uzun video, kliplerin kurguda birleşmesidir
- **Çözünürlük:** 720p (1280 × 720) ve 1080p (1920 × 1080); çözünürlük arttıkça çoğu sağlayıcıda saniye fiyatı da artar
- **Oran:** 16:9 yatay (ekran, sunum), 9:16 dikey (telefon, hikâye, kısa video)
- Oran değişince model sahneyi yeniden kurar; yatayın kırpılmış hâli değildir
- Yayın yeri kararı verir: telefonda izlenecek 6 saniyelik bir hikâyede 1080p'nin farkı çoğu zaman görülmez
- Her ayar bir bütçe kararıdır; "en yüksek kalite" her zaman doğru cevap değildir

-----

## Neden video görselden pahalı?

- Bir görsel tek bir kare; bir saniyelik video onlarca kare, üstüne ses ve kareler arası tutarlılık
- Video modelleri büyük ve pahalı donanımda çalışır; sağlayıcı bunu saniye başına ücretlendirir
- Görselde ücretsiz günlük kota vardı; videoda çoğu sağlayıcı ücretsiz kota vermiyor
- Aynı aile içinde katmanlar var: hafif (ucuz) ve tam (pahalı) modeller arasında fiyat birkaç kat değişebilir
- Bir denemenin bedeli büyüdükçe **deneme alışkanlığı** değişir: önce görselle dene, beğendiğini videoya çevir
- Fiyatlar sık değişir: bir projeye başlamadan önce sağlayıcının fiyat sayfasına bakmak işin parçası

-----

## Uzun süren iş: kuru temizleme fişi

- Kuru temizlemeciye ceketini bırakırsın; ceketi o an almazsın, bir **fiş** alırsın
- Tezgâhın önünde saatlerce beklemezsin; arada bir uğrar ya da arar, "hazır mı?" diye sorarsın
- Hazırsa fişi gösterir, ceketi alırsın
- Video da böyle çalışır: isteği **başlatırsın**, bir **iş numarası** alırsın (fiş), **durumu sorarsın**, hazırsa **indirirsin**
- Fişi kaybedersen ceketi almak zorlaşır; iş numarasını kaybetmek de öyle
- Programcılar buna **asenkron** (eşzamanlı olmayan) iş der: istek ile sonuç aynı anda gelmez
- Konu 2'den beri yaptığımız istekler tersiydi: soruyu sordun, cevap hemen geldi

-----

## Aralıklarla sormak ve zaman aşımı

- Kargo takibinde siteye her saniye bakmazsın; arada bir bakarsın
- Programda da aynı: sor, cevap "henüz değil"se biraz bekle, yeniden sor
- Çok sık sormak sunucuyu yorar, işi hızlandırmaz; çok seyrek sormak hazır olan sonucu geç görmek demek
- Sonsuza kadar sormamak için bir sınır koyarsın ("en fazla şu kadar dakika"); buna **zaman aşımı** denir
- Zaman aşımı işi iptal etmez; yalnızca senin beklemeni bitirir. İş numaran elindeyse sonra yeniden sorarsın
- **Yanılgı:** "cevap gelmedi, çalışmadı." Uzun işlerde çoğu zaman yalnızca **henüz bitmedi**

-----

## Beklemenin arayüz tasarımı

- Kullanıcı ne olduğunu bilmediğinde bekleyemez; sayfayı yeniler, düğmeye bir daha basar
- Bu yüzden iyi arayüzler bekleme sırasında konuşur: yükleme göstergesi, ilerleme çubuğu, "yaklaşık 2 dakika"
- Video üreten arayüzler de ilerlemeyi gösterir ya da "hazır olunca haber vereceğiz" der
- Programın kendisi de bir arayüzdür: "bekliyorum, 40 saniye oldu" yazan kod, susan koddan iyidir
- Yanlış bekleme tasarımı pahalıya patlar: kullanıcı aynı isteği iki kez gönderirse iki kez ödersin
- Tasarımcı olarak bekleme anını da tasarlarsın: ne gösterilir, ne kadar sürede, hangi sözle

**Sohbete yaz:** en son hangi uygulamada beklerken ne olduğunu anlamadın? Ne gösterseydi rahatlardın?

-----

## Aracı hizmet: anahtarı görmeden üretmek

- Video ücretli; her öğrenci kendi kartını vermek zorunda kalmasın diye videolar hocanın hesabından üretiliyor
- Hesabın anahtarı paylaşılmaz: çoğu sağlayıcının kullanım şartları anahtar ve hesap paylaşımını yasaklıyor
- Çözüm bir **aracı hizmet** (proxy): senin isteğini alır, hocanın hesabıyla modele iletir, sonucu sana verir
- Restorandaki garson gibi: mutfağa sen girmezsin, siparişi garson götürür ve getirir
- Sana özel bir **video kodun** var; aracı hizmet seni onunla tanır ve kaç klip ürettiğini sayar
- Aracı hizmet ayarları kilitler: hangi model, hangi çözünürlük, en uzun süre. Kimse yanlışlıkla pahalı bir ayar seçip bütçeyi bitiremez
- Birçok kurum yapay zeka hizmetlerini çalışanlarına böyle açar: tek hesap, tek bütçe, kişi başına sınır

-----

## Ölçek ve sınır: Konu 9'un dersleri videoda

- Konu 9'da sınırı kendin koydun (en fazla şu kadar görsel); burada sınırı aracı hizmet koyuyor: kişi başına klip sayısı
- Bir döngüde video üretmek, görselde olduğundan çok daha hızlı para harcar
- **Kaldığı yerden devam** burada da geçerli: biten videoyu yeniden üretme; iş numarası ve dosya adı elinde
- En pahalı hata: bekleme döngüsünün içinde işi **yeniden başlatmak**. Her turda yeni bir video, yeni bir ücret
- Üretim günlüğüne artık maliyet de yazılır: hangi klip, hangi ayar, kaç dolar
- Bir kampanyanın video kalemini önceden hesaplayabilmek, müşteriye verilen teklifin parçasıdır

-----

## Etik: hareket eden görüntüye güven

- Gerçekçi video, sahte haber ve kişiyi taklit eden içerik (deepfake) üretmek için de kullanılabilir
- Sağlayıcılar insan yüzü ve gerçek kişi içeren istekleri sınırlıyor; bazı bölgelerde ya da görselden videoda istek reddedilebilir
- Büyük sağlayıcılar ürettikleri videolara gözle görülmeyen bir **filigran** (watermark) gömüyor; içeriğin yapay zekayla üretildiği sonradan tespit edilebiliyor
- Konu 7'deki kural videoda daha da önemli: yaşayan bir kişinin yüzünü, sesini, adını izinsiz kullanma
- Şeffaflık: bir işte yapay zeka videosu kullandıysan bunu söylemek mesleki bir alışkanlık olmalı
- Üretim günlüğü burada da şeffaflığın kanıtıdır: hangi model, hangi yönerge, hangi görselden

-----

## Bu konunun ödevi

**Görselin hareketlensin.**

1. Konu 9 ödevinde ürettiğin görsellerden birini seç (kazananın ya da harekete en uygun olanı)
2. Bir hareket yönergesi yaz: kameranın ve öznenin hareketini ayrı ayrı anlat
3. Dersteki defterin adımlarıyla görselden bir video üret; üretim günlüğüne kaydet (model, süre, oran, yönerge, maliyet)
4. **İki cümle:** görsel hareket edince ne korundu, ne bozuldu? Bu görsel harekete uygun muydu?
5. **Bir cümle:** bu klibi 8 saniye isteseydin kaç dolar tutardı; bu iş için o fazladan 4 saniyeye değer miydi?

Ayrıntılar: `odevler/odev10.md`. Puan yok; Konu 11'in başında sıradaki arkadaşlar gösterecek.

-----

## Hatırlanacaklar

1. **Video bir kare dizisidir.** Zor olan kareler arası tutarlılık; bu yüzden pahalı ve yavaş
2. **Görselden video kontrol verir.** Görsel ilk kare olur; yönerge ne olacağını, kamera dili nasıl görüneceğini anlatır
3. **Her ayar bir bütçe kararı.** Süre, çözünürlük ve oran yayın yerine göre seçilir
4. **Uzun iş: başlat, numarayı sakla, aralıklarla sor, indir.** Zaman aşımı beklemeni bitirir, işi değil
5. **Sınır ve kayıt.** İşi bir kez başlat; maliyeti günlüğe yaz

Sıradaki konu: **Konu 11 — Zincirleme: üretim hattı.** Metin, görsel ve video modelleri tek bir programda birbirine bağlanıyor: bir adımın çıktısı ötekinin girdisi.
