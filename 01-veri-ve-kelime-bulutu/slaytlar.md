# Konu 1 — Veriyi Kodla İşlemek

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Metin de bir veri

- Veri deyince akla tablolar ve sayılar gelir; oysa dünyadaki verinin çoğu **metin**
- Müşteri yorumları, sosyal medya gönderileri, şarkı sözleri, haberler, mesajlar
- Bir insan birkaç yüz yorumu okuyabilir; on bin yorumu okuyamaz
- Bilgisayar okumaz ama **sayar**: hangi kelime kaç kez geçiyor?
- Saymak basit görünür, ama doğru saymak için önce metni temizlemek gerekir
- Bugün bu iş için yeni bir şey öğrenmiyoruz: liste, sözlük, döngü ve `if` yetiyor

-----

## Yakın okuma, uzak okuma

- **Yakın okuma:** bir metni satır satır, dikkatle okumak; edebiyat dersinde yaptığın şey
- **Uzak okuma:** binlerce metni okumadan, sayarak genel bir resim çıkarmak
- Uzak okuma "ne çok konuşuluyor?" sorusunu cevaplar; yakın okuma "nasıl konuşuluyor?" sorusunu
- İkisi birbirinin yerine geçmez: sayma nereye bakacağını gösterir, okuma anlamı verir
- Tasarımda karşılığı: kullanıcı araştırmasında önce eğilimi görmek, sonra tek tek alıntılara inmek

-----

## Bugünün sorusu: müşteriler bu kafeyi nasıl anlatıyor?

- Bir kafenin görsel kimliğini yenileyeceksin; tasarıma başlamadan önce müşteriyi dinlemek istiyorsun
- Elinde kafeye yazılmış 30 müşteri yorumu var
- 30 yorumu gözle okursun; 3000 yorum olsaydı?
- Yorumları kodla sayıp müşterinin kafeyi hangi kelimelerle anlattığını bulacağız

**Tahmin et, sohbete yaz:** bir kafe yorumunda en çok geçen üç kelime sence hangileri?

-----

## Bir metni saymanın beş adımı

1. **Dosya:** yorumlar bir metin dosyasında durur
2. **Metin:** dosyayı açıp tek bir uzun yazı olarak okuruz
3. **Kelimeler:** yazıyı kelimelere böleriz ve temizleriz
4. **Sayaç:** her kelimenin kaç kez geçtiğini sayarız
5. **Görsel:** sonucu bir kelime bulutu ya da çubuk grafikle gösteririz

- Her adım bir öncekinin ürettiğini kullanır; dosyayı yalnızca bir kez okuruz
- Bu beş adım, metinle çalışan her programın iskeleti

-----

## Bilgisayar "kelime" bilmez, boşluktan böler

- Bilgisayar için metin harflerden ve işaretlerden oluşan uzun bir dizi
- "Kelime" dediğimiz şeyi bulmak için en basit yol: metni **boşluklardan** bölmek
- Ama o zaman `Kahve`, `kahve`, `kahve.` ve `kahve,` dört **ayrı** kelime sayılır
- Büyük harf ve noktalama, aynı kelimeyi parçalara dağıtır
- Temizlemeden sayarsak en sık geçen kelime bile listenin altında kalabilir
- Bu yüzden saymadan önce her kelimeyi **aynı biçime** getiririz

-----

## Temizlik: aynı kelimeyi aynı yaz

- **Küçültmek:** bütün harfleri küçük harfe çeviririz; "Kahve" ile "kahve" birleşir
- **Noktalamayı atmak:** nokta, virgül, ünlem gibi işaretleri kaldırırız
- Noktalamayı silmek yerine **boşluğa** çeviririz: "yer.Sessiz" silinirse "yerSessiz" diye tek kelime olur
- Temizlikte **sıra** önemlidir; yanlış sırada yapılan doğru adımlar bile sonucu bozabilir
- Temizlik bir tasarım kararıdır: "kahve" ile "kahveler" aynı mı sayılsın? Cevap sorunun ne olduğuna bağlı

-----

## Türkçe tuzağı: İ ve I

- Python'ın küçültme komutu İngilizce kurallarıyla çalışır
- İngilizcede büyük I'nın küçüğü noktalı i'dir: "IŞIK" küçülünce "işik" olur
- Türkçe büyük **İ** küçülürken noktası ayrı bir işaret olarak kalır: ekranda "internet" görünür ama bilgisayar için farklıdır
- Sonuç: aynı kelime iki ayrı satırda sayılır ve sayılar bölünür
- Çözüm: **önce** İ ve I'yı kendimiz doğru harfe çeviririz, **sonra** küçültürüz
- Ders: hazır araçlar çoğu zaman İngilizce düşünülerek yazılır; Türkçe metinde sonucu mutlaka kontrol et

-----

## Sözlük: anahtar ve değer

- Python'da sözlük, her **anahtara** bir **değer** bağlayan yapı
- Telefon rehberi gibi: isim anahtar, numara değer; numarayı isimle bulursun
- Sözlükte sıra numarası yoktur; "ilk eleman" diye sormazsın, anahtarın adını söylersin
- Kelime saymak için ideal: anahtar kelimenin kendisi, değer kaç kez geçtiği
- Örnek: "kahve" → 5, "sessiz" → 3, "masa" → 2
- Geçen dönem en çok zorlandığımız konulardan biriydi; bugün her adımda kullanacağız

-----

## Saymanın mantığı: çetele tutmak

- Kâğıt kalemle sayarken ne yaparsın? Kelimeyi ilk görünce yazar, yanına bir çizgi çekersin
- Aynı kelimeyi tekrar görünce yeni satır açmaz, yanına bir çizgi daha eklersin
- Kodda da aynısı: her kelime için tek soru, "bu kelime sözlükte var mı?"
- Yoksa değerini 1 yaparız; varsa değerine 1 ekleriz
- Bütün kelimeler bitince elimizde her kelimenin kaç kez geçtiğini söyleyen bir sözlük olur
- Önce bunu elle yazacağız, sonra Python'un hazır sayacı `Counter`'ın aynı işi tek satırda yaptığını göreceğiz

-----

## Durak kelimeler: her metinde en üstteler

- Sayımı sıralayınca listenin başında hep aynı kelimeler çıkar: **ve, bir, bu, için, çok, ama**
- Bunlar dilin yapıştırıcısıdır; metnin **konusu** hakkında bir şey söylemezler
- Bunlara **durak kelime** denir; hazır bir listeyle elenir
- Her dilde böyledir: birkaç işlev kelimesi metnin büyük kısmını oluşturur, çoğu kelime ise bir iki kez geçer
- Elemeden çizilen bir kelime bulutu metnin değil, **dilin** fotoğrafıdır
- Hangi kelimenin durak sayılacağı da bir karardır: kafe yorumlarında "kafe" kelimesi bir şey anlatır mı?

-----

## Kelime bulutu nedir?

- Her kelimenin **boyutu**, metinde kaç kez geçtiğine göre belirlenir
- Tek bakışta "bu metin genel olarak neyi anlatıyor?" sorusuna cevap verir
- Sunumlarda, raporlarda, sosyal medya analizlerinde sık kullanılır
- Hazırlaması kolay, okuması eğlenceli; bu yüzden çok da yanlış kullanılır
- Bugün bulutu kendi sayacımızdan çizeceğiz ve neyi gösterip neyi göstermediğini konuşacağız

-----

## Bulutta yalnızca boyut veri taşır

- Kelimelerin **konumu**, **rengi** ve **yönü** rastgeledir; her çizimde değişir
- "Bu kelime ortada, demek ki önemli" yanlış bir okumadır
- "Bu kelime kırmızı, demek ki olumsuz" da yanlış bir okumadır
- İzleyici her görsel farkın bir anlamı olduğunu varsayar
- Tasarımcının işi, veri taşımayan görsel farkları ya kaldırmak ya da anlamlı hâle getirmek
- Uzun kelimeler daha çok yer kaplar; bu da sıklığı olduğundan büyük gösterir

-----

## Bulut mu, çubuk grafik mi?

- **Kelime bulutu** sezdirir: "genel tema ne?" sorusuna hızlı bir izlenim verir
- **Çubuk grafik** ölçer: "hangisi ne kadar önde?" sorusunu kesin cevaplar
- Bulutta birbirine yakın iki kelimenin hangisinin büyük olduğunu gözle ayırt edemezsin
- Grafikte uzunluk karşılaştırması kolaydır; insan gözü uzunluğu alandan daha iyi okur
- Hangisini seçeceğin, izleyicine ne söylemek istediğine bağlı: bir **tasarım kararı**

-----

## Saymanın sınırları

- **Ekler:** "kahve", "kahvesi", "kahvenin" bilgisayar için ayrı kelimeler; Türkçede bu sorun büyük
- **Olumsuzluk:** "hiç sessiz değil" cümlesi de "sessiz" sayımına bir ekler
- **Bağlam:** "servisi fena değil" bir övgü mü, bir şikâyet mi? Sayı söylemez
- **Az geçen ama önemli:** iki kez geçen bir şikâyet, yirmi kez geçen bir övgüden daha değerli olabilir
- Sayı **kaç kez** geçtiğini söyler, **nasıl** geçtiğini söylemez
- Bu yüzden saydıktan sonra öne çıkan kelimelerin geçtiği yorumları **okuruz**

-----

## Tasarımcı için ne işe yarar?

- **Kullanıcı araştırması:** müşteriler ürünü hangi kelimelerle anlatıyor?
- **Marka sesi:** bir markanın kendi gönderileri hangi kelimeleri tekrar ediyor? Müşterininkiyle örtüşüyor mu?
- **Rakip analizi:** rakiplerin yorumlarında hangi şikâyetler öne çıkıyor?
- **Brief:** "müşteri ne istiyor?" sorusuna sezgi yerine veriyle başlamak
- **İçerik:** şarkı sözleri, şiirler, konuşmalar üzerine bilgi görselleştirmesi
- Ortak nokta: sayma bir başlangıç noktası, bulgu ise okuyarak ve yorumlayarak çıkar

-----

## Bu konunun ödevi

Kendi seçtiğin bir Türkçe metinle **iki** kelime bulutu üret:

1. Durak kelimeler **elenmeden**
2. Durak kelimeler **elendikten sonra**

- Sonra tek cümle yaz: eleme öncesi en büyük kelimeler neydi, sonra ne oldu?
- Metin en az 300 kelime olsun: şarkı sözü, kendi yazın, bir markanın gönderileri
- Puan yok; bir sonraki derste sıradaki arkadaşlar ekranda gösterecek

-----

## Hatırlanacak dört şey

1. **Sözlük anahtarla açılır.** Değeri sıra numarasıyla değil, anahtarın adıyla alırsın
2. **Türkçe küçültme özel iş.** Büyük İ ve I önce elle çevrilir, sonra küçültülür
3. **Temizlik olmadan sonuç yanıltır.** Elenmemiş bulut metnin değil dilin fotoğrafıdır
4. **Sayı nereye bakacağını söyler.** Bulguyu kelimeyi bağlamında okuyarak bulursun

Sıradaki konu: kodumuzla internetteki bir yapay zeka modeline soru soracağız. Cloudflare anahtarın hazır olsun.
