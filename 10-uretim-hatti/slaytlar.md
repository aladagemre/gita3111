# Konu 10 — Zincirleme: Üretim Hattı

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Parçaları birleştirmek

- Konu 5'te slogan yazdırdın, Konu 8'de görselleri koddan ve toplu olarak ürettin, Konu 9'da arayüzden video yaptın
- Her biri ayrı bir işti; birinin sonucunu öbürüne sen taşıdın: kopyala, yapıştır, dosyayı bul
- Bugün bu taşıma işi programa geçiyor: tek bir **brif** girer, bir taslak seti çıkar
- Yeni olan araçlar değil, aralarındaki **bağlar**: bir adımın çıktısı sıradakinin girdisi
- Konu 8'deki kurallar (kararlı ad, kaldığı yerden devam, üretim günlüğü) hattın her adımında geçerli
- Final projesi de böyle bir hat: konu girer, metin ve görsel çıkar; hepsi düzenli ve kayıtlı

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
- Bugün kuracağın hat bu akışın küçük, otomatik bir örneği: insanların yerini almak için değil, önlerine taslak koymak için

**Sohbete yaz:** senin bildiğin bir tasarım işinde (afiş, ambalaj, sosyal medya serisi) hangi adımlar sırayla gelir? Hangi adımın çıktısı hangisine gider?

-----

## Ara çıktı: istasyonlar arasındaki tabak

- Bir halkanın ürettiği, sıradakine giden sonuca **ara çıktı** denir: sloganlar, görsel yönergeleri, görseller
- Animasyonda storyboard bir ara çıktıdır: render başlamadan önce herkes ona bakar, gerekirse değiştirir
- Ara çıktı bir dosyada durursa üç şey kazanırsın: **bakabilirsin**, **düzeltebilirsin**, **yeniden kullanabilirsin**
- Hattın ortasına girmek mümkün olur: makinenin yazdığı sloganı beğenmezsen dosyada kendin değiştirirsin, hat oradan devam eder
- Ara çıktı yalnızca bellekte (programın içinde) kalırsa program kapanınca kaybolur
- Bu yüzden iyi bir hatta, saklanmaya değer ara çıktılar sıradaki halkaya gitmeden önce bir dosyaya yazılır

-----

## Neyi saklarız, neyi yeniden kurarız?

- **Pahalı olanı sakla:** her görsel günlük kotadan yer; biteni yeniden üretmek boşa harcamaktır
- **Her seferinde farklı çıkanı sakla:** sıcaklığı olan bir model aynı soruya her seferinde başka bir cevap verir (Konu 5)
- Farklı çıkan bir ara çıktı yeniden üretilirse sonraki halkalarla bağı kopar: dünkü görsel, bugünkü sloganla aynı kayıtta durur
- **Ucuz ve her seferinde aynı çıkanı yeniden kur:** iki metni birleştirmek gibi; saklamak yalnızca dosya kalabalığı yapar
- Bir halka çalışmadan önce sorar: "bu zaten var mı?" Varsa onu kullanır, yoksa üretip saklar
- **Boşu saklama:** boş bir sonuç dosyaya yazılırsa hat onu bitmiş iş sanır ve bir daha hiç denemez
- **Yanılgı:** "her seferinde baştan üretmek daha temiz." Daha pahalı, daha yavaş ve sonuçları birbirini tutmaz

-----

## Yapılandırma dosyası: sipariş fişi

- Bir matbaada makine aynıdır; her iş için değişen şey sipariş fişidir: kâğıt, ölçü, adet, renk
- Programda bunun adı **yapılandırma dosyası** (config): ayarlar koddan ayrı bir dosyada durur
- Konu, stil, kaç slogan, sıcaklık, tohum: hepsi bu dosyada; yeni bir müşteri gelince kodu değil fişi değiştirirsin
- Dosya JSON biçiminde ve JSON titizdir: metinler çift tırnakta, ayarlar arasında virgül var, son satırdan sonra yok
- Fişte işin adı da yazar: o brifin bütün çıktıları bu adı taşıyan bir **çalışma klasörüne** gider
- Ad otomatik bir tarihten değil fişten gelirse aynı brif hep aynı klasöre gider ve biten iş atlanır; brif değişince adı sen değiştirirsin
- Bir ayarı kodun ortasına gömmek, sipariş fişini makinenin içine vidalamak gibidir: her değişiklikte makineyi sökersin

-----

## Bir halka koparsa: zincir benzetmesi

- Bir zincir en zayıf halkasından kopar; uzun bir üretim hattında da er geç bir halka işini yapamaz
- Sebepler tanıdık: internet gider, kota biter, model bir yönergeyi reddeder, bir cevap boş gelir
- Kötü bir hat orada durur; sıradaki işler hiç yapılmaz ve neyin eksik kaldığını tek tek aramak gerekir
- İyi bir hat kopan halkayı **kayda geçirir** ve sıradaki işle **devam eder**
- Sonraki çalıştırmada yalnızca eksik olan denenir; bitenler yerinde durur
- Bir halkanın çıktısına sıradakine vermeden önce bakmak gerekir: boş ya da bozuk bir sonuç, hata vermeden sonraki halkayı da bozar
- Hata çıkmaması her şeyin yolunda olduğu anlamına gelmez: hat bazen hata vermeden yanlış bir şey üretir; bunu ancak kayıtlar ortaya çıkarır

-----

## Üretim günlüğü: hattın seyir defteri

- Gemilerde seyir defteri tutulur: ne zaman, nereden, hangi rotayla; bir şey ters gidince geriye bakılır
- Hattın günlüğü de öyle: hangi ayarlarla çalıştı, hangi ara çıktılar oluştu, her işin sonucu ne oldu
- Günlükteki her kayıt aynı biçimde yazılır: hangi halka, ne girdi, ne çıktı, durum (oldu / olmadı)
- Bir halkanın çıktısı sıradakinin girdisi olduğu için günlükte zincir görünür: bu görsel şu yönergeden, o yönerge şu slogandan
- Final projesinde teslim edeceğin üretim günlüğü de böyle bir dosya; hocan işin nasıl üretildiğini oradan okur
- Şeffaflık için de gerekli: bir müşteriye hangi görselin hangi modelle, hangi yönergeyle üretildiğini gösterebilirsin (Konu 7: etik ve telif)

-----

## Metin ve görsel: aynı şeyi mi söylüyorlar?

- Bir afişte slogan ile görsel iki ayrı ses; aralarındaki ilişki tasarımın kendisidir
- Görsel ne gösteriyorsa slogan onu tekrar ederse (kahve fincanı + "Kahve burada") mesaj güvenli ama düz kalır
- Slogan görsele yeni bir anlam eklerse (boş bir masa + "Burada zaman yavaşlar") izleyici iki parçayı kendi kafasında birleştirir
- Roland Barthes bu iki ilişkiye ad verir: metin görselin olası anlamlarından birini seçip sabitlerse **demirleme**, metin ile görsel anlamı birlikte kurarsa **aktarma**
- Görsel modeller harfleri çoğu zaman bozar; bu yüzden yönergeye "görselde yazı olmasın" yazılır, slogan afişe bir tasarım programında dizilir
- Bir hat her slogana bir görsel üretebilir, ama hangi eşleşmenin işe yaradığını bilemez; ilişkiyi kuran ve seçen tasarımcıdır

**Sohbete yaz:** aklında kalan bir afiş ya da reklam düşün. Yazı görseli tekrar mı ediyordu, yoksa ona bir şey mi ekliyordu?

-----

## Otomasyonun yeri: insan döngüde

- Hat yorulmaz ve unutmaz: dosyayı hep aynı adla kaydeder, her işi kayda geçirir, "zaten var mı?" sorusunu her seferinde sorar
- Hattın yapamadığı: brifi yazmak, iyi sloganı seçmek, yazıyı yerleştirmek, "bu marka bu değil" demek
- İyi bir düzende insanın devreye gireceği yerler önceden bellidir: matbaada tiraj, prova baskı onaylandıktan sonra basılır
- Buna **insan döngüde** (human in the loop) denir; profesyonel üretimde yaygın bir düzendir
- Her şeyi otomatik yapan bir hat hızlıdır ama kör; her şeyi elle yapan bir süreç dikkatlidir ama yavaş
- Kod tekrar eden işi üstlenir; karar ve zevk tasarımcıda kalır

-----

## Bu konunun ödevi

**Kendi hattının iskeleti.**

1. Final projen için bir konu seç (bir marka, bir etkinlik, bir kampanya); kendi ayarlar dosyanı yaz
2. Dersteki defterin kopyasıyla iki halkayı çalıştır: metin ve görsel
3. Panoyu ve üretim günlüğünü (`uretim.json`) kaydet
4. **Üç cümle:** hangi halkaya elle müdahale ettin? Hangi slogan–görsel eşleşmesi işe yaradı? Final projende hangi halkayı eklemek istersin?

Ayrıntılar: `odevler/odev10.md`. Güzel olması gerekmiyor; final projesinin ilk taslağı. Puan yok; Konu 11'in başında sıradaki arkadaşlar gösterecek.

-----

## Hatırlanacaklar

1. **Hat:** bir halkanın çıktısı sıradakinin girdisi; başta brif, sonda taslak set
2. **Ayarlar koddan ayrı:** brif değişince kod değil yapılandırma dosyası değişir
3. **Ara çıktıyı sakla:** pahalı ya da her seferinde farklı çıkanı; ucuz ve aynı çıkanı yeniden kur
4. **Kopan halka hattı durdurmaz:** kayda geçer, sonraki çalıştırmada yalnızca o denenir
5. **Hat taslak üretir:** seçim, tipografi ve son karar tasarımcının

Sıradaki konu: **Konu 11 — RAG: belgeye dayalı cevap.** Bu hatta adımların sırasını sen belirledin. Konu 11'de modele bilmediği bir belgeyi okutacağız, Konu 12'de sırayı model belirleyecek.
