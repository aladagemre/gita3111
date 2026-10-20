# Konu 11 — Zincirleme: Üretim Hattı

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 10'dan Konu 11'e: parçaları birleştirmek

- Konu 5'te slogan yazdırdık, Konu 8'de tek görsel ürettik, Konu 9'da bir ızgara, Konu 10'da bir video
- Her biri ayrı bir defterdi; birinin sonucunu öbürüne sen taşıdın: kopyala, yapıştır, dosyayı bul
- Bugün bu taşıma işini programa veriyoruz: tek bir **brif** girer, bir taslak seti çıkar
- Yeni olan araçlar değil, aralarındaki **bağlar**: bir adımın çıktısı sıradakinin girdisi
- Konu 9'daki kurallar (kararlı ad, kaldığı yerden devam, kayıt) hattın her adımında geçerli
- Final projesi tam olarak bu: konu girer; metin, görsel ve video çıkar, hepsi düzenli ve kayıtlı
- Konu 10'da gördün: video geç gelir ve her deneme bir bedel ödetir; bir hatta bu bedel her halkada birikir

-----

## Hat nedir: mutfak benzetmesi

- Bir restoran mutfağında her istasyonun tek bir işi var: biri doğrar, biri pişirir, biri tabağa koyar
- Doğrayanın çıktısı pişirenin girdisi; pişirenin çıktısı tabaklayanın girdisi
- Programlamada buna **hat** (pipeline) denir; her istasyon hattın bir **halkası**
- Halkalar birbirini tanımaz; yalnızca kendisine geleni alır, işler, sonucunu sıradakine bırakır
- Bu yüzden bir halkayı değiştirmek kolaydır: başka bir görsel modeli denemek için yalnızca o halka değişir
- **Yanılgı:** "hat tek büyük bir program." Hayır: küçük, ayrı ayrı denenebilen parçaların sırayla bağlanması

-----

## Tasarımda hatlar zaten var

- Bir reklam kampanyası: brif → fikir ve slogan → görsel → farklı ölçülere uyarlama → yayın
- Bir kitap: metin → editörlük → dizgi → kapak → baskı öncesi kontrol
- Bir animasyon: senaryo → storyboard → animatik → animasyon → render
- Her okun iki ucunda farklı bir kişi, farklı bir araç ve bir **teslim dosyası** var
- Ajanslarda bu düzene "iş akışı" denir; dosya adlandırma ve klasör düzeni kuralları bunun için yazılır
- Bugün kurduğumuz hat bu akışın küçük, otomatik bir taslağı: insanların yerine değil, onların önüne taslak koymak için

**Sohbete yaz:** senin bildiğin bir tasarım işinde (afiş, ambalaj, sosyal medya serisi) hangi adımlar sırayla gelir? Hangi adımın çıktısı hangisine gider?

-----

## Ara çıktı: istasyonlar arasındaki tabak

- Bir halkanın ürettiği, sıradakine giden sonuca **ara çıktı** denir: sloganlar, görsel yönergeleri, görseller
- Animasyonda storyboard bir ara çıktıdır: render başlamadan önce herkes ona bakar, gerekirse değiştirir
- Ara çıktı bir dosyada durursa üç şey kazanırsın: **bakabilirsin**, **düzeltebilirsin**, **yeniden kullanabilirsin**
- Hattın ortasına girmek mümkün olur: makinenin yazdığı sloganı beğenmezsen dosyada kendin değiştirirsin, hat oradan devam eder
- Ara çıktı yalnızca bellekte (programın içinde) kalırsa program kapanınca kaybolur
- Bu yüzden iyi bir hatta her halkanın sonucu, bir sonraki halkaya gitmeden önce bir dosyaya yazılır

-----

## Neyi saklarız, neyi yeniden kurarız?

- **Pahalı olanı sakla:** her görsel kotadan yer, her video para tutar; biteni yeniden üretmek boşa harcamaktır
- **Her seferinde farklı çıkanı sakla:** sıcaklığı olan bir model aynı soruya her seferinde başka bir cevap verir (Konu 5)
- Farklı çıkan bir ara çıktı yeniden üretilirse sonraki halkalarla bağı kopar: dünkü görsel, bugünkü sloganla aynı kayıtta durur
- **Ucuz ve her seferinde aynı çıkanı yeniden kur:** iki metni birleştirmek gibi; saklamak yalnızca dosya kalabalığı yapar
- Bir halka çalışmadan önce sorar: "bu zaten var mı?" Varsa onu kullanır, yoksa üretip saklar
- **Yanılgı:** "her seferinde baştan üretmek daha temiz." Daha pahalı, daha yavaş ve sonuçları birbirini tutmaz

-----

## Yapılandırma dosyası: sipariş fişi

- Bir matbaada makine aynıdır; her iş için değişen şey sipariş fişidir: kâğıt, ölçü, adet, renk
- Programda bunun adı **yapılandırma dosyası** (config): ayarlar koddan ayrı bir dosyada durur
- Konu, stil, kaç slogan, sıcaklık, tohum, video açık mı kapalı mı: hepsi bu dosyada
- Yeni bir müşteri geldiğinde kodu değil fişi değiştirirsin; kodu açmadan, bozmadan
- Dosya JSON biçiminde: Konu 2'den ve Konu 9'dan tanıdığın sözlük yapısı, yalnızca bu kez sen yazıyorsun
- JSON titizdir: metinler çift tırnakta, doğru/yanlış küçük harfle (`true`, `false`), son satırdan sonra virgül yok
- Bir ayarı kodun ortasına gömmek, sipariş fişini makinenin içine vidalamak gibidir: her değişiklikte makineyi sökersin

-----

## Klasör düzeni: her işin bir çekmecesi

- Bir hat çalıştıkça dosya üretir: metinler, görseller, pano, kayıt; düzen yoksa birkaç günde kaybolurlar
- Her brif için bir **çalışma klasörü**: o işin bütün çıktıları ve kaydı aynı yerde
- Klasörün adını kim verir? Program otomatik bir tarihle verirse her çalıştırma yeni bir klasör açar ve hiçbir şey "zaten var" olmaz
- Ad ayarlardan gelirse aynı brif hep aynı klasöre gider; biten iş atlanır (Konu 9: aynı iş, aynı ad)
- Tarih yine de işe yarar: arşiv için adı sen koyarsın (`2026-11-04_kafe`); brif değişince yeni ad, yeni klasör
- Ajanslardaki kural da aynı: proje adı ve sürüm dosya adında; "son_son_gercekson.psd" bir düzen değildir

-----

## Bir halka koparsa: zincir benzetmesi

- Bir zincir en zayıf halkasından kopar; uzun bir hatta da bir halka er geç kopar
- Sebepler tanıdık: internet gider, kota biter, model bir yönergeyi reddeder, bir cevap boş gelir
- Kötü bir hat orada durur; sıradaki işler hiç yapılmaz ve neyin eksik kaldığını tek tek aramak gerekir
- İyi bir hat kopuk halkayı **kayda geçirir** ve sıradaki işle **devam eder**
- Sonraki çalıştırmada yalnızca eksik olan denenir; bitenler yerinde durur
- Bir halkanın çıktısını sıradakine vermeden bakmak gerekir: boş ya da bozuk bir sonuç, hata vermeden bir sonraki halkayı da bozar
- **Yanılgı:** "hata çıkmadıysa her şey yolunda." Hat bazen hata vermeden yanlış bir şey üretir; bunu yalnızca kayıt gösterir

-----

## Kayıt: hattın seyir defteri

- Gemilerde seyir defteri tutulur: ne zaman, nereden, hangi rotayla; bir şey ters gidince geriye bakılır
- Hattın kaydı da öyle: hangi ayarlarla çalıştı, hangi ara çıktılar oluştu, her işin sonucu ne oldu
- Her kaydın aynı biçimi var: hangi halka, ne girdi, ne çıktı, durum (oldu / olmadı)
- Bir halkanın çıktısı sıradakinin girdisi olduğu için kayıtta zincir görünür: bu video şu görselden, o görsel şu sloganından
- Final projesinde teslim edilen **üretim günlüğü** budur; hangi model, hangi parametre, ne çıktı, ne düzeltildi
- Şeffaflık için de gerekli: bir müşteriye ya da hocana hangi işin nasıl üretildiğini gösterebilirsin (Konu 7: etik ve telif)

-----

## İki model arasında: talimat ve temizlik

- Bir modelin çıktısı başka bir modelin girdisi olunca küçük kusurlar büyür
- Metin modeline "yalnızca sloganı yaz" dersin; çoğu zaman uyar, bazen tırnak, "Slogan:" ya da bir açıklama ekler
- Model bir talimatı "kesin kural" olarak değil, "olası devam" olarak okur (Konu 5); uymaması bir arıza değil, doğası
- O yüzden iki halka arasına küçük bir **temizlik** konur: boşlukları ve tırnakları silmek (Konu 1'in araçları)
- Görsel modeller harfleri çoğu zaman bozar: sloganı görselin içine yazdırmak yerine "görselde yazı olmasın" denir
- Tipografi tasarımcının işi: slogan afişe, görselin üstüne, bir tasarım programında dizilir

-----

## Metin ve görsel: aynı şeyi mi söylüyorlar?

- Bir afişte slogan ile görsel iki ayrı ses; aralarındaki ilişki tasarımın kendisidir
- Görsel ne gösteriyorsa slogan onu tekrar ederse (kahve fincanı + "Kahve burada") mesaj güvenli ama düz kalır
- Slogan görsele yeni bir anlam eklerse (boş bir masa + "Burada zaman yavaşlar") izleyici iki parçayı kendi kafasında birleştirir
- Roland Barthes, metnin görselin olası anlamlarından birini seçip sabitlemesine **demirleme**, metinle görselin birbirini tamamlayıp anlamı birlikte kurmasına **aktarma** der
- Bir hat her slogana bir görsel üretebilir, ama hangi eşleşmenin işe yaradığını bilemez
- Hat seçenekleri yan yana koyar; ilişkiyi kuran ve seçen tasarımcıdır

**Sohbete yaz:** aklında kalan bir afiş ya da reklam düşün. Yazı görseli tekrar mı ediyordu, yoksa ona bir şey mi ekliyordu?

-----

## Otomasyonun yeri: insan döngüde

- Hat yorulmaz ve unutmaz: dosya adını, kaydı, "zaten var mı?" sorusunu her seferinde aynı yapar
- Hattın yapamadığı: brifi yazmak, iyi sloganı seçmek, yazıyı yerleştirmek, "bu marka bu değil" demek
- İyi bir hatta insanın araya girdiği yerler bellidir: ara çıktılara bakılır, beğenilmeyen değiştirilir, hat oradan devam eder
- Buna **insan döngüde** (human in the loop) denir; profesyonel üretim araçlarının çoğu böyle çalışır
- Her şeyi otomatik yapan bir hat hızlıdır ama kör; her şeyi elle yapan bir süreç dikkatlidir ama yavaş
- Kod tekrar eden işi üstlenir; karar ve zevk tasarımcıda kalır

-----

## Bu konunun ödevi

**Kendi hattının iskeleti.**

1. Final projen için bir konu seç (bir marka, bir etkinlik, bir kampanya); kendi ayarlar dosyanı yaz
2. Dersteki defterin kopyasıyla en az iki halkayı çalıştır: metin ve görsel
3. Panoyu ve kaydı (`uretim.json`) kaydet
4. **Üç cümle:** hangi halkaya elle müdahale ettin? Hangi slogan–görsel eşleşmesi işe yaradı? Final projende hangi halkayı eklemek istersin?

Ayrıntılar: `odevler/odev11.md`. Güzel olması gerekmiyor; final projesinin ilk taslağı. Puan yok; Konu 12'nin başında sıradaki arkadaşlar gösterecek.

-----

## Hatırlanacaklar

1. **Hat:** bir halkanın çıktısı sıradakinin girdisi; başta brif, sonda taslak set
2. **Ayarlar koddan ayrı:** brif değişince kod değil yapılandırma dosyası değişir
3. **Ara çıktıyı sakla:** pahalı ya da her seferinde farklı çıkanı; ucuz ve aynı çıkanı yeniden kur
4. **Kopan halka hattı durdurmaz:** kayda geçer, sonraki çalıştırmada yalnızca o denenir
5. **Hat taslak üretir:** seçim, tipografi ve son karar tasarımcının

Sıradaki konu: **Konu 12 — Araç kullanımı.** Bugün hangi halkanın ne zaman çalışacağına sen karar verdin. Konu 12'de kullanıcının cümlesine bakıp hangi halkanın çağrılacağına model karar verecek.
