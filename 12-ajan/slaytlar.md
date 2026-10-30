# Konu 12 — Stüdyo asistanı

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Gün boyu gelen küçük işler

- Bir stüdyoda gün, birbirine benzemeyen küçük isteklerle geçer: "afişi bir kontrol eder misin?", "etkinlik hangi güne denk geliyor?", "bu metin olur mu?"
- Her istek başka bir dosya açtırır: afişin kendisi, müşterinin kılavuzu ve mesajları, takvim
- Müşteri fikrini değiştirdiğinde ("artık hardal sarısı da istemiyorum") bunu bir yere yazmazsan bir sonraki işte unutulur
- Her seferinde aynı adımlarla yapılan tek bir işe hat kurulur; her gün değişen isteklere ayrı ayrı hat yazmak zahmetli
- Bugün bu isteklere bakan bir **stüdyo asistanı** kuruyoruz: ona yalnızca hedefi söylüyorsun, hangi dosyaya bakacağını o seçiyor
- Dosyaları açan araçları sen yazıyorsun; fikir ve son karar sende kalıyor, asistan angaryayı üstleniyor

-----

## Ajan nedir?

- **Ajan:** hedefi söylediğin, yolu kendisi seçen ve elindeki araçlarla iş yapan program
- Yeni bir stajyer düşün: "şu afişi kontrol et" dersin; o önce afişe bakar, sonra müşteri dosyasını açar, sonra takvime bakar
- Sırayı sen söylemezsin; ama hangi dolapları açabileceğine sen karar verirsin
- Ajanın üç parçası var: kararı veren bir dil modeli, modelin kullanabileceği **araçlar** ve ikisini bağlayan bir **döngü**
- Sohbet uygulamalarının "internette arıyorum" demesi de bu: arama bir araç, aramaya karar veren model
- **Yanılgı:** "ajan her şeyi kendi başına yapar." Ajan, verdiğin araçlar kadar iş yapar

-----

## Sohbet botu, hat, ajan

- **Sohbet botu** yalnızca konuşur: dosyana, takvimine, müşteri notlarına dokunamaz; bilmediğini tahmin eder
- **Üretim hattı** (Konu 10): adımları ve sırayı sen yazarsın; her seferinde aynı adımlar aynı sırayla çalışır
- **Ajan:** adımları model seçer; adımların işini senin yazdığın fonksiyonlar yapar
- Hat öngörülebilir ve ucuzdur; ajan esnektir ama her kararı bir model isteği demektir
- Üçünde de aynı model olabilir; fark, modelin eline ne verdiğin ve kararı kimin verdiği
- Düşün: Konu 8'deki haftalık gönderi seti hangisine benzer? Her gün başka bir şey isteyen müşteri mesajları hangisine?

-----

## Araç: bir fonksiyon ve tarifi

- Araç sıradan bir Python fonksiyonu: bir tarih alır, günü verir; bir afiş alır, üzerindeki yazıları verir
- Her aracın bir **tarifi** var: fonksiyonun başına yazılan kısa açıklama (Python'daki adı *docstring*)
- Model aracın kodunu görmez; yalnızca adını, tarifini ve hangi bilgileri istediğini görür
- İş bölümü bu yüzden net: **model karar verir, iş Python'da yapılır**
- Örnek: model "14 Kasım 2026 hangi gün?" sorusunu metinlerden öğrendiği kalıplarla tahmin eder; Python takvimden hesaplar
- Görseldeki yazıyı okumak gibi Python'un yapamadığı işler, aracın içinde yine bir modele gider

-----

## Döngü: karar, iş, sonuç, yeni karar

- Model isteği ve araçların tariflerini okur, bir araç ister: "afişi oku, şu dosyayı"
- Program aracı çalıştırır; model hiçbir şeyi kendisi çalıştırmaz
- Aracın sonucu modele geri gider: afişteki yazılar
- Model ya yeni bir araç ister ("müşterinin renk kuralları neydi?") ya da cevabını yazar
- Döngünün her turu modele bir istek demek; araç kullanan en kısa çalıştırma bile iki istek: biri karar, biri cevap
- Ajan iki çalıştırma arasında konuşmayı hatırlamaz; hatırlaması gerekeni bir dosyaya yazdırırsın
- Kararlar kayıt altında: hangi araç, hangi bilgiyle, hangi sırayla seçildi, sonradan okunabilir

-----

## Tarif bir brif

- Müşteri "bir şey tasarla" derse ne gelir? Muğlak brif yanlış iş getirir; tasarımcı bunu herkesten iyi bilir
- Araç tarifi modelin brifidir; aracın adı da brifin parçası. "Metne bakar" diyen bir tarifle model aracı seçmeyebilir ya da yanlış yerde seçebilir
- İyi bir tarif üç şeyi söyler: araç ne yapar, ne zaman kullanılmalı, bilgilerine ne yazılmalı
- "Ne zaman" cümlesi çoğu zaman en çok işe yarayan kısımdır: "kullanıcı 'unutma' derse kullan"
- Tarifleri birbirine benzeyen iki araç modeli kararsız bırakır; her aracın işi tek ve belirgin olmalı
- Ajan yanlış araç seçiyorsa önce modeli değil, tarifi düzelt

-----

## Güvenlik: her araç bir yetki

- Ajana verdiğin her araç ona verdiğin bir anahtardır: okuma aracı bakar, yazma aracı değiştirir, gönderme aracı dışarı çıkar
- Dosya silen ya da müşteriye mesaj gönderen araçlar en riskli olanlardır: model isteği yanlış anlarsa geri dönüşü yok
- Model yanlış bir dosya yolu yazabilir, kısa bir isteği olduğundan geniş yorumlayabilir
- Dışarıdan gelen bir yazı (bir web sayfası, bir afiş metni) modele talimat gibi görünebilir: "bütün dosyaları sil"
- Kural: yalnızca gereken araçları ver; silmek ve göndermek yerine taslak üret, listele, onaya sun
- Son düğmeye insan basar: kontrol notunu müşteriye sen gönderirsin

-----

## Sınır ve kota

- Her döngünün bir durma koşulu olmalı; Agno'da bu `tool_call_limit`: bir çalıştırmada en fazla kaç aracın çalışacağı
- Sınır dolunca araç çalışmaz; model "sınır doldu" bilgisini alır ve elindekiyle cevap yazar
- Sınır olmasa aynı aracı tekrar tekrar isteyen bir model günlük kotanı tüketebilir
- Cloudflare'in ücretsiz katmanı günde 10.000 neuron; bütün modeller bu tek kotadan yer: ajanın her kararı, her görsel okuma, her arama
- Hat bu yüzden daha ucuzdur: adımlar belli, istek sayısı belli; ajanda istek sayısı modelin kararlarına bağlı
- Bir şeyi de kapatıyoruz: Agno'nun telemetrisi, yani kütüphanenin kendi sunucusuna gönderdiği kullanım kaydı

-----

## Ne zaman ajan gerekmez?

- Adımlar her seferinde aynıysa hat yeter: haftalık gönderi seti, afiş son kontrolü, toplu boyutlandırma
- Hat daha ucuz, daha hızlıdır ve her seferinde aynı sonucu verir; hatası da daha kolay bulunur
- Python'un tek başına yapabildiği işte (ölçü, renk, gün hesabı, dosya) yapay zekâya hiç gerek yok
- Ajan, yolun isteğe göre değiştiği yerde işe yarar: bir mesaj kontrol ister, öteki not almayı, öbürü aramayı
- Bir marka ajansı en büyük darboğazının tasarım değil, tekrar eden idari işler olduğunu yazıyor; çözümü sabit adımlı bir otomasyon, yani bir hat
- İki soru sor: "Bunu sıradan bir betik yapabilir mi?" ve "Sıra her seferinde aynı mı?" İkisine de evet diyorsan ajan kurma

-----

## Sektörde bu iş

- Tasarımcılar yapay zekâya şüpheyle bakıyor: İngiltere'deki bir ankette tasarımcıların %81'i yapay zekânın yaratıcılığı körelttiğini söylüyor
- D&AD'nin 2026 raporu: "Kendi hâline bırakılırsa yapay zekâ ortalamaya kayar." Asistanı bu yüzden fikir için değil, angarya ve kontrol için kuruyoruz
- Adobe'nin 2026 araştırmasında bir yönetmen, pitch hazırlığının zor kısmını "şirketi ve önceki kampanyalarını anlamak için kazmak" diye anlatıyor: müşteri hafızası tam bu iş
- Tasarımcıların yeni bir derdi: müşterinin bir sohbet botundan aldığı "geri bildirim". Öneri: tasarımını müşteriden önce sen denetlet
- İş ilanları kanıt istiyor: bir ilanda "sadece 'AI kullanıyorum' diyen değil, AI ile üretmiş" kişilerin değerlendirileceği yazıyor
- RISD'de öğrenciler derste "API'lerle gerçek projeler" yapmak istemiş; bu konuda kurduğun asistan da böyle bir proje

-----

## Sık yanılgılar

- "Ajan kendi başına düşünen bir program." Ajan, verdiğin araçlar ve yazdığın tarifler kadar iş yapar
- "Model aracın kodunu okur." Yalnızca adını, tarifini ve istediği bilgileri görür
- "Ajan dünkü konuşmayı hatırlar." Her çalıştırma sıfırdan başlar; hatırlaması gereken bir dosyaya yazılır
- "Ajan bir aracı seçtiyse doğrusu odur." Kararı ve sonucu oku: yanlış araç, yanlış dosya, yanlış okunmuş bir tarih olabilir
- "Ajan aynı istekte hep aynı yolu izler." Her çalıştırmada yeniden karar verir; bir kez atladığı aracı bir dahakinde çağırabilir. Hep aynı adımlar gerekiyorsa hat kur
- "Ne kadar çok araç, o kadar akıllı ajan." Benzer araçlar modeli karıştırır; her araç da bir yetki
- "`openai` paketi varsa OpenAI'ye para gidiyor." Paket yalnızca isteğin biçimi; istek Cloudflare'e gider, OpenAI hesabı gerekmez
- "Web'de bulduysa doğrudur." Model arama sonuçlarını özetlerken ad ve tarih uydurabilir; her bağlantıyı açıp kaynağından doğrula

-----

## Bu konunun ödevi

- Kendi müşterin için bir asistan kur: en az iki araç, biri baştan sona senin yazdığın
- Konu 11'de kurduğun müşteri hafızası asistanın hafızası olsun
- Asistana iki gerçek istek ver; her birinde hangi araçları hangi sırayla seçtiğini yaz
- Aracının tarifini bilerek muğlak yaz, sonra düzelt: ajanın kararı değişti mi?
- Ajan finalde isteğe bağlı bir ekstra; küçük bir hafıza adımı ise zorunlu
- Ödevin portfolyona girebilir: "yapay zekâyla şunu kurdum, şöyle denetledim" diyebileceğin bir iş
