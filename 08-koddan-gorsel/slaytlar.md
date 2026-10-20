# Konu 8 — Koddan Görsel Üretimi

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 7'den Konu 8'e: aracın içini açıyoruz

- Konu 7'de görsel üreten bir aracı **arayüz gibi** kullandık: `ciz("...")` yazdık, `001.jpg` çıktı
- Arada ne oldu? Bugün o arayı **kendimiz yazıyoruz**
- Yeni olanlar: görselin bayt olarak gelmesi, onu dosyaya yazmak, dosyalara düzenli ad vermek, hataları yakalamak
- Gerisini biliyorsun: anahtar, adres, istek, durum kodu Konu 2'den; tohum ve yönerge Konu 7'den
- Bu konunun sonunda kendi küçük üretim aracın olacak
- Konu 9'da bu araçla onlarca görsel üreteceğiz; bugün eklediğimiz hata kontrolleri orada işe yarayacak

-----

## Arayüz ne yapıyordu, kod ne yapacak?

- Bir üretim arayüzünde yönergeyi bir kutuya yazarsın, ayarları düğmelerle seçersin, "üret"e basarsın
- Görseli beğenirsen "indir"e basarsın; tarayıcı ona bir ad verir: çoğu zaman anlamsız bir ad
- Hangi tohumla, hangi ayarla ürettiğini genellikle bir yere yazmazsın; bir hafta sonra aynısını üretemezsin
- Kodda her düğme bir **değişken**, "üret" bir **istek**, "indir" bir **dosyaya yazma** işlemi
- Kod her şeyi kaydedebilir: ne istendi, ne zaman, hangi tohumla
- Üstelik aynı işi bir kez değil, istediğin kadar tekrarlayabilir

-----

## Ayarlar değişkende: tekrarlanabilirlik

- Yönerge, tohum, model adı: hepsi birer değişken
- Değişkeni değiştirip yeniden çalıştırırsın; geri kalan her şey aynı kalır (Konu 7'deki kontrollü deney)
- Aynı değişkenlerle bir ay sonra çalıştırırsın, aynı görseli alırsın (model sürümü değişmediyse): iş **tekrarlanabilir** olur
- Bir müşteri "geçen ayki afişin aynısı, yalnızca rengi farklı" dediğinde ne yapacağını bilirsin
- Yönergenin parçalarını (stil, renk, konu) ayrı değişkenlerde tutmak bir **şablon** kurmak demek
- Şablon + değişken listesi = toplu üretim (Konu 9)

-----

## Her dosya bayttır; bazıları harftir

- Bilgisayardaki her dosya, 0 ile 255 arasındaki sayılardan oluşan bir dizidir: **bayt**
- Bir metin dosyasında bu sayıların her biri (ya da birkaçı) bir **harfe** karşılık gelir
- Bir görselde aynı sayılar renkleri, sıkıştırma bilgisini, boyutu anlatır; harflere karşılık gelmez
- Bu yüzden görselleri, sesleri, PDF'leri **ikili dosya** (binary) diye ayrı tutarız
- Dosyanın sonundaki uzantı (.jpg, .png, .txt) bir etikettir; asıl tür, baytların içinde yazar

-----

## Görsel nasıl metne dönüşür? base64

- Konu 2'de gördük: API'ler cevabı JSON içinde, **metin** olarak gönderir
- Ama görsel metin değil, bayt. Çözüm: baytları harf ve rakamlara çeviren bir kodlama, **base64**
- 64 farklı karakter kullanır: büyük harfler, küçük harfler, rakamlar ve iki işaret
- Her 3 bayt 4 karakter olur; görsel metne çevrilince yaklaşık üçte bir büyür
- E-posta ekleri de yıllardır böyle gönderilir: ek ayrı bir dosya gibi görünür, ama aslında e-postanın içinde base64 metni olarak durur
- Öbür uçta metin geri çevrilir ve tek bayt kaybolmadan aynı görsel elde edilir
- **Yanılgı:** base64 şifreleme ya da sıkıştırma değildir; dosyayı büyütür ve herkes geri çevirebilir

-----

## Desen: istek → metin → bayt → dosya

- **İstek:** yönergeyi ve tohumu gönderirsin (Konu 2'deki adres, başlık, gövde)
- **Durum kodu:** önce cevabın başarılı olup olmadığına bakarsın
- **Metin:** yanıtın içinde görsel, base64 metni olarak durur
- **Bayt:** metni geri çevirince görselin baytları elde edilir
- **Dosya:** baytları bir dosyaya yazarsın
- Görsel üretimi, görsel düzenleme, ileride video çoğunlukla bu deseni kullanır; bir kez öğrenince başka yerlerde de tanırsın

-----

## Dosya adlandırma: tasarımcının eski derdi

- "afis_son.jpg", "afis_son_2.jpg", "afis_SON_bu.jpg": her tasarım klasörünün hikâyesi
- Kötü ad bir hafta sonra işe yaramaz: hangisi hangi müşteriye, hangi ayarla, hangi gün?
- İyi bir dosya adı kendini anlatır: **ne zaman**, **ne istendi**, **hangi ayarla**
- Tarih yıl-ay-gün sırasıyla yazılırsa (2026-10-19) dosyalar adlarına göre sıralanınca tarih sırasına da girer
- Dosya adında boşluk, Türkçe karakter, `/` ve `:` gibi işaretler sorun çıkarabilir; tire ve alt çizgi güvenlidir
- Kod adı her seferinde aynı kurala göre üretir; insan unutur, kod unutmaz

-----

## Üzerine yazma tehlikesi

- Bir dosyayı var olan bir adla kaydedersen eskisi **sessizce** silinir; geri dönüşüm kutusuna bile gitmez
- Toplu üretimde bu, saatlerce emek verilmiş dosyaların tek bir satırla kaybolması demek
- Kural: yazmadan önce sor, **bu ad alınmış mı?**
- Alınmışsa ya yazmayı bırak ya da adı değiştir (bir sayı, bir saniye ekle)
- Çıktıları tek bir klasörde toplamak hem düzen hem güvenlik sağlar: neyin nerede olduğunu bilirsin
- Tasarım programlarındaki "Farklı Kaydet" ve sürüm geçmişi de aynı ihtiyaçtan doğdu

-----

## İki tür başarısızlık

- **Sunucu cevap verdi ama "olmaz" dedi:** anahtar yanlış (401), çok hızlı istek ya da kota doldu (429), ayar sınır dışı (400)
- Bunu Konu 2'den biliyorsun: durum koduna bakarsın, 200 değilse yanıtın içine girmezsin
- **Cevap hiç gelmedi:** internet yok, adres yanlış, sunucu çökmüş
- İkincisinde program bir **hata fırlatır** ve olduğu yerde durur
- Tek bir görsel üretirken bu küçük bir sorun; yüz görsellik bir işin ortasında bütün işin durması demek
- İyi bir araç iki durumu da tanır ve kullanıcıya ne olduğunu anlaşılır bir dille söyler

-----

## `try` ve `except`: B planı

- Python'da "dene; şu hata çıkarsa çökme, şunu yap" demenin yolu: `try` ve `except`
- `try` bloğuna riskli işi yazarsın; `except` bloğuna o iş başarısız olursa ne yapılacağını
- Matbaa benzetmesi: kâğıt biterse makine durur; iyi bir operatör kâğıdı yeniler, işi kaldığı yerden sürdürür
- Hangi hatayı yakaladığını **adıyla** söylersin; tanımadığın hataları sessizce geçiştirmezsin
- Hata mesajını kullanıcıya anlaşılır yaz: "İnternetini kontrol et", uzun bir İngilizce hata metninden iyidir
- Amaç hatayı saklamak değil, programın hatayla **başa çıkabilmesi**

-----

## Tekrar denemek ve beklemek

- Bazı hatalar geçicidir: sunucu bir an meşguldür ya da kısa sürede çok istek gönderilmiştir (429)
- Böyle durumlarda birkaç saniye bekleyip **yeniden denemek** çoğu zaman işe yarar (bekleme kodunu Konu 9'da yazacağız)
- Ama sınır koy: üç deneme, beş deneme; sonsuza kadar denemek kotayı ve zamanı yer
- Kalıcı hatada (yanlış anahtar) yeniden denemek işe yaramaz; önce sebebi düzelt
- Ücretsiz kota günlüktür: dolduysa birkaç saniye beklemek işe yaramaz, kota ertesi gün yenilenir
- Deneme yaparken kaç istek gönderdiğini takip et
- Konu 9'da onlarca istek gönderirken bu kurallara ihtiyacımız olacak

-----

## Programı kullanıcıya açmak

- Şimdiye kadar yönergeyi kodun içine yazdık; her değişiklikte kodu düzenledik
- `input` ile program yönergeyi **kullanıcıdan** sorar: kodu bilmeyen biri de kullanabilir
- Kullanıcı sen olabilirsin, bir ekip arkadaşın ya da bir müşteri
- Kullanıcıya güvenme: boş bir yönerge, çok uzun bir metin, dosya adında sorun çıkaracak işaretler gelebilir
- İyi bir araç ne beklediğini söyler ("Yönerge (İngilizce):") ve beklenmeyen girdiye hazırlıklıdır
- Konu 9'da aynı işi bir döngüye koyacağız: tek bir yönerge yerine bir liste

-----

## Görsel göndermek: bir form doldurmak gibi

- Görsel düzenlemede modele yalnızca metin değil, bir **görsel** de gönderirsin
- Bunun yolu bir web formuna dosya eklemek gibidir: birkaç yazı alanı (talimat, boyut) ve bir dosya
- Dosya yine ikili okunur ve gönderilir
- Düzenleme modellerinin çoğu bir boyut sınırı koyar; büyük görseli önce küçültmek gerekir
- Gelen cevap yine base64 metni: desen aynı, yalnızca giden paket farklı
- Formlar her şeyi metin olarak gönderir; sayılar bile yazı olarak gider

-----

## Neden kod?

- Arayüz tek görsel için hızlıdır; kod **kayıt, tekrar, ölçek ve sağlamlık** için
- **Kayıt:** her dosyanın adı, görselin ne zaman, hangi yönergeyle ve hangi tohumla üretildiğini söyler
- **Tekrar:** aynı ayarlarla aynı görseli bir ay sonra yeniden alırsın
- **Ölçek:** bir yönerge yerine bir liste, bir tohum yerine on tohum: Konu 9
- **Sağlamlık:** bir hata bütün işi durdurmaz, kullanıcıya ne olduğu söylenir
- Tasarımcının işi değişmez: brifi yazmak, sonuçları değerlendirmek, seçmek; kod tekrarı üstlenir

-----

## Bu konunun ödevi

**5 yönerge × 2 tohum = 10 görsel.**

1. Dersteki defteri kopyala; kendi seçtiğin bir konuda beş farklı yönerge yaz
2. Her yönergeyi iki farklı tohumla üret ve düzenli adlandırmayla ayrı bir `odev8/` klasörüne kaydet
3. Hiçbir dosya üzerine yazılmasın
4. **İki cümle:** aynı yönergenin iki tohumu arasındaki fark neydi? Hangi yönerge iki tohumda da tutarlı kaldı?

Ayrıntılar: `odevler/odev8.md`. Puan yok; Konu 9'un başında sıradaki arkadaşlar gösterecek.

-----

## Hatırlanacak beş şey

1. **Görsel bir ikili dosyadır.** İkili okunur, ikili yazılır; harf değil, bayt
2. **base64 görseli metne çevirir.** API görseli JSON içinde metin olarak gönderir; geri çevirince tek bayt kaybolmaz
3. **Desen:** istek → durum kodu → metin → bayt → dosya
4. **Dosya adı kendini anlatır.** Ne zaman, ne istendi, hangi tohum; yazmadan önce "bu ad alınmış mı?"
5. **Hatayı yakala, çökme.** Sunucu "olmaz" derse durum koduna bak; cevap hiç gelmezse `try` / `except`

Sıradaki konu: **Konu 9 — Ölçek: toplu üretim.** Bugünkü aracı onlarca görsel için kullanacağız.
