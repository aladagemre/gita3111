# Konu 7 — Görsel Üretimi: Yönergeden Görsele

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## İkinci yarıya hoş geldin: artık üretiyoruz

- Birinci yarıda kaputu açtık: veri, API, makine öğrenmesi, gömme, dil modeli, gizli uzay
- İkinci yarıda bu modellerle **üretiyoruz**: görsel, toplu üretim, video, üretim hattı
- Bugün bir görsel üreticiyi tasarımcı gözüyle yönetmeyi öğreniyoruz
- Hedef: "rastgele deneyip şansını beklemek"ten **kontrollü denemeye** geçmek
- Bugün yeni kod yazmıyoruz: hazır bir aracı arayüz gibi kullanıyor, yalnızca metinleri ve sayıları değiştiriyoruz; aracın içini Konu 8'de açacağız
- Bu konudan itibaren yapay zeka araçları serbest ve bekleniyor; her üretimin modelini, tohumunu ve yönergesini üretim günlüğüne yaz

-----

## Konu 6'dan Konu 7'ye

- Konu 6'da öğrenilmiş bir haritada **noktayı biz seçtik** ve oradan bir A geri kurduk
- Görsel üreticide noktayı **yönerge** (prompt) seçer: yazdığın cümle haritada bir bölgeyi tarif eder
- Harita çok daha büyük: yüz milyonlarca görsel ve onların açıklamalarından öğrenildi
- Model işe haritada **rastgele bir başlangıç noktasından** başlar: buna gürültü diyoruz
- Her adımda bu noktayı yönergenin tarif ettiği bölgeye biraz kaydırır
- En sonda çözücü, Konu 6'daki gibi, noktadan görseli geri kurar

-----

## Difüzyon: gürültüden görsele

- Rastgele başlangıç noktasını hemen çözücüye verirsen anlamsız bir **gürültü** görürsün: eski televizyonlardaki karıncalanma gibi
- Konu 6'daki `[[20, 20]]` gibi: verinin olmadığı bir yerdesin; "rastgele pikseller yalnızca gürültü olur" demiştik, başlangıç tam olarak o
- Her **adımda** nokta yönergenin bölgesine biraz yaklaşır; ekranda bu, gürültünün bir kısmının silinmesi gibi görünür
- Bu yöntemin adı **difüzyon** (diffusion)
- Model bunu nasıl öğrendi? Eğitimde görsellere adım adım gürültü eklendi; model bu işi **tersine** yapmayı öğrendi
- Adım sayısı süreyi ve kotayı belirler
- Derste farklı adım sayılarıyla baştan üretip sonuçları karşılaştıracağız

**Tahmin et, sohbete yaz:** yalnızca 1 adımda üretilen bir görsel, 8 adımdakinden ne kadar farklı olur?

-----

## Tohum: rastgeleliğin anahtarı

- Başlangıç noktası (gürültü) rastgeledir; başlangıç değişirse görsel de değişir
- Başlangıç gürültüsünü üreten sayıya **tohum** (seed) denir
- Yönerge **bölgeyi** seçer, tohum o bölgeye **hangi noktadan** yola çıkılacağını seçer
- **Aynı model + aynı yönerge + aynı tohum = aynı görsel**
- Tohum, deney yapabilmenin şartı: bir şeyi değiştirdiğinde farkın gerçekten o değişiklikten geldiğinden emin olursun
- Sohbet arayüzlerinin çoğu tohumu gizler; API'de ve profesyonel araçlarda sen seçersin

-----

## Yönergenin anatomisi

İyi bir yönerge rastgele kelimeler değil, parçaları belli bir tariftir. Örnek brif: bir kitabevinin yağmurlu gece afişi.

- **Özne:** ne görüyoruz? *vitrini ışıklı küçük bir kitabevi*
- **Ortam:** nerede, yanında ne var? *yağmurlu, dar bir sokakta*
- **Stil:** hangi teknik ya da üslup? *linol baskı, izometrik illüstrasyon, sinematik fotoğraf*
- **Işık:** ne zaman, nasıl aydınlanıyor? *neon yansımaları, alacakaranlık*
- **Kompozisyon:** kamera nerede? *geniş açı, göz hizası, kuşbakışı*
- İstersen altıncı parça, **renk ve malzeme:** *mürdüm ve hardal palet, ıslak kaldırım taşı*

Bir brif yazar gibi düşün: modele neyi, nasıl, hangi duyguyla istediğini anlat.

-----

## Hangi dilde yazmalı?

**Tahmin et, sohbete yaz:** aynı yönergeyi Türkçe yazarsak görsel İngilizcedekine ne kadar benzer?

- Görsel üreticiler çoğunlukla İngilizce açıklamalı görsellerle eğitildi
- Konu 5'i hatırla: Türkçe metin daha çok belirtece (parçaya) bölünür ve eğitim verisinde çok daha az bulunur
- Derste aynı yönergeyi iki dilde deneyip farkı kendin göreceksin
- Stil ve teknik terimlerin İngilizcesini öğrenmek (watercolor, linocut, isometric, bokeh) bir tasarımcıya bugün çok şey kazandırır

-----

## Uzun yönerge daha iyi değildir

- Yaygın inanış: "ne kadar çok sıfat, o kadar iyi görsel"
- İnternette dolaşan kalıplar: *8k, masterpiece, best quality, award winning, trending*
- Bunlar çoğu zaman bir şey katmaz; bazen görseli herkesinkine benzeyen jenerik bir hâle iter
- **Çelişen istekler** daha kötü: *minimal* ve *son derece detaylı* aynı anda; *gece* ve *güneşli* aynı anda
- Model çelişkiden birini seçmek zorunda; hangisini seçeceğini sen belirleyemezsin
- İyi yönerge uzun değil, **net** olandır: her kelime bir işe yaramalı

-----

## Kontrollü deney: bir seferde tek değişken

- Üç şeyi birden değiştirirsen sonuç değiştiğinde **hangisinin** etkilediğini bilemezsin
- Bilimdeki deneyin aynısı: diğer her şeyi sabit tut, tek şeyi değiştir
- Görselde: tohum sabit, özne sabit, ışık sabit; yalnızca **stil** değişsin
- Sonra stil sabit, yalnızca **ışık** değişsin
- Sonuçları **yan yana** koy: bir karşılaştırma panosu
- Tasarım ajanslarında müşteriye seçenek sunmanın da en dürüst yolu bu: farkın nereden geldiği görünür

-----

## Modellerin karakteri

- Her görsel üretici farklı verilerle, farklı yöntemlerle eğitildi
- Bu yüzden aynı yönergeye farklı "ellerle" cevap verirler: renk, çizgi, ayrıntı, kompozisyon alışkanlıkları farklı
- Bir modelin güçlü olduğu yerde öbürü zayıf olabilir: biri yazıda iyi, öbürü fotoğraf gerçekçiliğinde
- Tohum yalnızca **aynı modelde** işe yarar; iki model aynı tohumla aynı görseli vermez
- Bugün karşılaştırmada iki model var: **FLUX** (Black Forest Labs) ve **Stable Diffusion XL** (Stability AI); düzenlemede üçüncü bir model çalışıyor
- Bir tasarımcı nasıl iş için doğru illüstratörü seçerse, doğru modeli seçmek de bir karar

-----

## Negatif yönerge ve en-boy oranı

- **Negatif yönerge:** görselde **istemediğin** şeyleri yazarsın: *yazı, harf, filigran, insan*
- Bir istektir, garanti değildir; model yine de bazılarını koyabilir
- Her model desteklemez: bugünkü iki modelden yalnızca biri negatif yönerge alıyor
- **En-boy oranı:** görselin şekli. Kare (1:1) sosyal medya gönderisi, yatay (16:9) sunum ve web afişi, dikey (9:16) hikâye ve poster
- En-boy oranını sonradan kırpmak yerine baştan doğru seçmek kompozisyonu korur
- Model eğitildiği boyutlardan çok uzaklaşınca tuhaf kompozisyonlar ve tekrar eden nesneler çıkabilir

-----

## Var olanı değiştirmek: görsel düzenleme

- Tasarımcının işi çoğu zaman sıfırdan üretmek değil, eldekini **değiştirmek**
- Yeni modeller bir görsel ve bir talimat alır: *ürünün rengini laciverte çevir*, *arka plandaki kişiyi çıkar*, *gündüz sahnesini akşama çevir*
- Model görselin geri kalanını korumaya çalışır; ama her zaman başaramaz
- Kontrollü deney burada da geçerli: tek talimat, sonucu öncesiyle yan yana koy
- Ürün fotoğrafının arka planını değiştirmek, bir afişin renk varyasyonları, bir eskizi farklı tekniklere çevirmek
- Bugün bir görseli talimatla düzenleyeceğiz

-----

## Arayüzler: aynı ilkeler her yerde

- Görsel üretimi birçok arayüzden yapılabilir: sohbet asistanları, Adobe Firefly, Canva, Midjourney, Ideogram
- Arayüzler bazı ayarları gizler (tohum, adım sayısı), bazılarını düğmeye çevirir (en-boy oranı, stil)
- Bugün öğrendiğin ilkeler hepsinde geçerli: net yönerge, tek değişken, yan yana karşılaştırma
- Biz bugün defterde hazır bir araç kullanıyoruz: bütün ayarlar elimizin altında ve her görsel bir dosya olarak kaydediliyor
- Konu 8'de bu aracın içini açacağız; Konu 9'da aynı fikirle yüzlerce görsel üreteceğiz

-----

## Etik: bu görseller neyle eğitildi?

- Görsel üreticiler internetten toplanan yüz milyonlarca görselle eğitildi
- Bu görsellerin çoğunun sahibine sorulmadı; birçok sanatçı ve fotoğraf ajansı dava açtı
- "Yaşayan bir illüstratörün tarzında" istemek, o kişinin yıllarca kurduğu üslubu onun izni olmadan kullanmak demek
- Model eğitim verisindeki görsellere çok benzeyen, hatta neredeyse aynısı olan çıktılar verebilir
- Kendine sor: bu görseli bir insana ısmarlasaydım, aynı şeyi istemek doğru olur muydu?
- Derste kuralımız: yaşayan bir sanatçının adını stil olarak yazmıyoruz

-----

## Telif ve müşteriye karşı dürüstlük

- Üretilen görselin telif durumu birçok ülkede hâlâ belirsiz
- Bazı ülkelerde insan katkısı olmayan bir görsel telifle korunmuyor; yani başkası da aynısını kullanabilir
- Ticari bir işte müşteriye görselin yapay zekayla üretildiğini ve bunun risklerini söylemek gerekir
- Gerçek kişileri, markaları ve logoları yanıltıcı biçimde üretmek ayrı bir sorun: sahte haber ve sahte reklam
- Platformlar üretilen görselleri etiketlemeye ve filigranlamaya başladı
- Derste kuralımız: her çıktıda kullanılan **model, tohum ve yönerge** üretim günlüğüne yazılır

-----

## Bu konunun ödevi

Seçtiğin bir marka ya da etkinlik için **üç farklı görsel dil** dene.

1. Dersteki defteri kopyala; yönergenin beş parçasını (özne, ortam, stil, ışık, kompozisyon) kendi brifine göre yaz
2. Tohumu sabit tutup yalnızca **stili** üç kez değiştir; karşılaştırma panosunu kaydet
3. **İki cümle:** hangi görsel dil bu marka için işe yaradı, neden?
4. Üretim günlüğüne model adını, tohumu ve üç yönergeyi yaz

Ayrıntılar: `odevler/odev7.md`. Puan yok; Konu 8'in başında sıradaki arkadaşlar gösterecek.

-----

## Hatırlanacak beş şey

1. **Difüzyon gürültüden başlar.** Görsel bir anda çıkmaz; her adımda biraz daha temizlenir
2. **Tohum rastgeleliği sabitler.** Aynı model, yönerge ve tohum aynı görseli verir
3. **Yönerge bir tariftir.** Özne, ortam, stil, ışık, kompozisyon; uzun değil net
4. **Bir seferde tek değişken.** Sonuçları yan yana koy ki farkın nereden geldiği görünsün
5. **Model, tohum ve yönerge yazılır.** Etik ve telif belirsizliğinde şeffaflık senin sorumluluğun

Sıradaki konu: **Konu 8 — Koddan görsel üretimi.** Bugün kullandığımız aracın içini açıyoruz.
