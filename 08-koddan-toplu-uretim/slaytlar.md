# Konu 8 — Koddan Görsel ve Toplu Üretim

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 7'den Konu 8'e: neden kod öğreniyorum?

- Konu 7'de görselleri hazır bir araçla tek tek ürettik; yönergeyi ve tohumu bilerek değiştirdik
- Tek bir görsel için bunu arayüzde de yapabilirdin: yaz, üret, indir
- Bugün önce aynı işi koddan yapıyoruz; bu kez dosyanın adını ve yerini sen seçiyorsun
- Sonra arayüzün yapamadığına geçiyoruz: onlarca görseli tek seferde, düzenli adlarla ve kayıtlı üretmek
- Dönemin başından beri sorulan "neden kod öğreniyorum?" sorusunun cevabı bu konu
- Yeni olanlar: kombinasyon, şablon, kart, güvenlik sınırı, kaldığı yerden devam, programın kendi yazdığı üretim günlüğü, kontak sayfası
- Görseli üretip dosyaya yazan kısım hazır bir yardımcı dosyada; senin işin onu yönetmek

-----

## Arayüz ne yapıyordu, kod ne yapıyor?

- Arayüzde yönergeyi bir kutuya yazar, ayarları düğmelerle seçer, "üret"e basarsın
- Görseli beğenirsen "indir"e basarsın; tarayıcı dosyaya çoğu zaman anlamsız bir ad verir
- Hangi tohumla, hangi ayarla ürettiğini çoğu zaman bir yere yazmazsın; bir hafta sonra aynısını üretemezsin
- Kodda her kutu ve düğme bir **değişken**, "üret" bir **fonksiyon çağrısı**, "indir" dosyanın **yolu**
- Kod her şeyi kaydedebilir: ne istendi, hangi tohumla, hangi modelle
- Üstelik aynı işi bir kez değil, istediğin kadar ve her seferinde aynı biçimde yapar

-----

## Ayarlar değişkende: tekrarlanabilirlik

- Yönerge, tohum, model adı, dosyanın yolu: hepsi birer değişken
- Bir değişkeni değiştirip yeniden çalıştırırsın; geri kalan her şey aynı kalır (Konu 7'deki kontrollü deney)
- Aynı değişkenlerle bir ay sonra çalıştırırsın, aynı görseli alırsın (model sürümü değişmediyse): iş **tekrarlanabilir** olur
- Bir müşteri "geçen ayki afişin aynısı, yalnızca rengi farklı" dediğinde ne yapacağını bilirsin
- Değişkeni kullanıcıya da sordurabilirsin (`input`): kodu bilmeyen bir ekip arkadaşın da aracı kullanır
- Kullanıcıya körü körüne güvenme: boş bir yönerge ya da dosya adında sorun çıkaracak işaretler gelebilir

-----

## Dosyanın adını sen koyarsın

- "afis_son.jpg", "afis_son_2.jpg", "afis_SON_bu.jpg": her tasarım klasörünün hikâyesi
- Kötü ad bir hafta sonra işe yaramaz: hangisi hangi müşteriye, hangi ayarla, hangi seçenek?
- İyi bir ad kendini anlatır: içindeki seçenekler adda yazar (`kahve_afisi_lacivert.jpg`)
- Dosya adında boşluk, Türkçe karakter, `/` ve `:` gibi işaretler sorun çıkarabilir; tire ve alt çizgi güvenlidir
- Çıktıları tek bir klasörde toplamak hem düzen hem güvenlik sağlar: neyin nerede olduğunu bilirsin
- Kod adı her seferinde aynı kurala göre kurar; insan unutur, kod unutmaz

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
- Boşluklara giden kısa adlar (dosya için) ile uzun açıklamalar (model için) ayrı tutulursa ikisi de temiz kalır

-----

## İç içe döngü: saat ve dakika

- Bir saati düşün: akrep bir saat ilerlerken yelkovan bir tam tur atar
- **İç içe döngü** de aynı mantıkla çalışır: dıştaki döngü bir adım atar, içteki döngü baştan sona döner
- Dıştaki her stil için içteki döngü bütün renkleri gezer; sonra dıştaki bir sonraki stile geçer
- Girinti hangi satırın hangi döngünün içinde olduğunu söyler
- **Yanılgı:** "hata çıkmadıysa kod doğrudur." İçteki işi yapan satır dıştaki döngünün hizasına kayarsa çoğu zaman hata çıkmaz; bazı kombinasyonlar sessizce kaybolur
- İki liste için iki döngü, üç liste için üç döngü; her yeni katman sayıyı çarpar

-----

## Kart: bir görselin bütün bilgisi tek yerde

- Toplu üretimde her görselin bir **kartı** olur: stil, renk, dosya yolu, yönergenin tamamı, tohum, model
- Kütüphanedeki katalog fişi ya da matbaadaki iş emri gibi: bir işin bütün bilgisi tek bir kâğıtta
- Python'da kart bir **sözlük**, bütün kartlar bir **liste**: sözlüklerden oluşan bir liste
- Kart hem üretimi yönetir (ne üretilecek, nereye kaydedilecek) hem kaydı tutar (sonunda ne oldu)
- Karta sonradan yeni bilgi eklenebilir: üretildi mi, olmadı mı, kim seçti
- Kartlar elle değil döngüyle kurulur: listeler değişince kartlar da aynı kurala göre yeniden kurulur

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

- Ücretsiz kota günlüktür ve sınırlıdır; görsel, metin ve görsel okuma aynı kotadan harcar
- Döngüyü başlatmadan önce sor: kaç görsel, toplam ne kadar kota?
- Bir **güvenlik sınırı** koy: "bir çalıştırmada en fazla şu kadar üret" (kredi kartındaki harcama sınırı gibi)
- Listeyi yanlışlıkla fazla büyütürsen sınır kotanın bir anda bitmesini önler
- Ücretli hizmetlerde aynı hata doğrudan para demek; profesyonel araçların çoğunda bütçe sınırı koyma seçeneği var
- İyi alışkanlık: önce küçük bir deneme (2–3 görsel), beğenirsen hepsi

-----

## Sağlamlık: bir hata bütün işi durdurmamalı

- Elli isteğin birinde internet kopabilir, sunucu meşgul olabilir, bir istek reddedilebilir
- Kötü bir program orada durur; sıradaki işler hiç yapılmaz
- İyi bir program geçici hatada biraz **bekleyip yeniden dener** ve deneme sayısına bir sınır koyar
- Üç denemede de olmazsa o işi "olmadı" diye not eder ve sıradakine geçer
- Kalıcı hatada (yanlış anahtar, kota bitti) beklemek işe yaramaz; basit bir program bunu ayırt edemez, programı sen durdurursun
- Matbaa benzetmesi: kâğıt sıkışınca iyi bir operatör sıkışanı çıkarır, işi kaldığı yerden sürdürür
- Bekleyip yeniden deneyen kod hazır yardımcı dosyada; senden beklenen, ne yaptığını bilmek

-----

## Kaldığı yerden devam

- Uzun bir indirme yarıda kesilince indirme yöneticisi baştan başlamaz, kaldığı yerden devam eder
- Animasyon stüdyolarında saatler süren kare hesaplamaları (render) da böyle: biten kare yeniden hesaplanmaz
- Bunun için her çıktının **kararlı bir adı** olmalı: aynı iş, her zaman aynı ad
- Program her işten önce sorar: "bu dosya zaten var mı?" Varsa atlar
- Kota biterse ya da bağlantı koparsa, ertesi gün aynı programı çalıştırmak yeter
- Adda tarih ya da sıra numarası olsaydı her çalıştırma yeni bir iş sanılırdı; hepsi baştan üretilirdi
- **Dikkat:** adda olmayan bir şeyi (özne, tohum) değiştirirsen program yeni iş olduğunu bilemez ve eskileri atlar; öyle bir değişiklikte yeni klasör aç

-----

## Üretim günlüğü: makinenin okuyabileceği kayıt

- Konu 7'de günlüğü elle tuttuk; bugün program kendisi yazıyor
- Her görsel için: stil, renk, yönergenin tamamı, tohum, model ve sonuç (üretildi mi?)
- Kayıt **JSON** biçiminde: insan okuyabilir, program geri okuyabilir (Konu 2'deki API cevaplarının biçimi)
- Bir müşteri aylar sonra "geçen seferki şu görselin aynısı" dediğinde bütün bilgi elinde
- Şeffaflık için de gerekli: hangi görselin nasıl üretildiğini gösterebilmek (Konu 7: etik ve telif)
- Kayıt üretimin bir parçası olmalı; sonradan hatırlanarak yazılan kayıt eksik olur

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
2. Dersteki defterin adımlarıyla ızgarayı ayrı bir klasöre üret; kontak sayfasını ve üretim günlüğünü kaydet
3. **İki cümle:** hangi kombinasyon kazandı, neden? Satır ya da sütun olarak bir eğilim var mı?
4. **Bir cümle:** ızgaranda seni en çok şaşırtan kutu hangisiydi?

Ayrıntılar: `odevler/odev8.md`. Görsellerini sakla: Konu 9'da birini videoya çevireceğiz. Puan yok; Konu 9'un başında sıradaki arkadaşlar gösterecek.

-----

## Beş cümlede koddan toplu üretim

1. **Aynı iş koddan.** Ayarlar değişkende, dosyanın adı ve yeri senin elinde; iş tekrarlanabilir
2. **Kombinasyon çarpılarak büyür.** Şablon ve listelerden kartlar kurulur; toplu üretim bir hesapla başlar
3. **Sınır koy, sağlam yaz.** Güvenlik sınırı, önce küçük deneme; bir hata bütün işi durdurmaz
4. **Kararlı ad, kaldığı yerden devam.** Aynı iş aynı ad; var olanı atla
5. **Kayıt, sayfa, seçim.** Günlük her şeyi kaydeder, kontak sayfası karşılaştırır, son kararı tasarımcı verir

Sıradaki konu: **Konu 9 — Video, arayüzden.** Hareket ekliyoruz, bu kez kod yazmadan. Bugünkü görsellerinden birini videoya çevireceğiz; video hem yavaş hem pahalı bir üretim olduğu için "önce hesap" alışkanlığı orada da işe yarayacak.
