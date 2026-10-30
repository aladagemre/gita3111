# Konu 9 — Gönderini Hareketlendir

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Müşteri bu kez "biraz kıpırdasın" diyor

- Sayfa Kahve Konu 8'deki haftalık seti onayladı; şimdi bir gönderiyi hikâyede, "biraz canlı" görmek istiyor
- Hikâye ve Reels telefonda dikey ve kısa; durağan bir görsel orada hızla geçilip gidiyor
- İş: onaylı bir görseli 4–6 saniyelik dikey bir videoya çevirmek; buhar yükselir, ürün yerinde kalır
- Sektörde bu iş: Eylül 2026'da Türkiye'de bir tasarımcı ilanı, yapay zekâyla video üretmeyi ve dikey Reels'i birlikte istiyor
- Bugün kod yok: Cloudflare'de video modeli yok, Google'ınkini koddan kullanmak ücretli; ücretsiz bir arayüz kullanıyoruz
- Konunun sonunda: kendi müşterin için iki kısa dikey video ve yazısı eklenmiş bir son hâl

-----

## Görselden video: aynı kareye zaman

- **Metinden video:** sahneyi de hareketi de yönerge anlatır; kompozisyonu ve ürünü model kurar
- **Görselden video:** verdiğin görsel ilk kare olur; model yalnızca ardından olacakları üretir
- Benzetme: onaylı fotoğrafı bir görüntü yönetmenine verip "yalnız buharı oynat" demek
- Tasarımcı görselden başlar: renk, kompozisyon ve ürün zaten onaylı; hikâye akıştaki gönderiyle aynı kareden doğar
- Görselin yalnızca bir parçası kıpırdıyorsa buna **sinemagraf** denir; sakin bir markaya yakışır
- **Yanılgı:** "Video görselin aynısı olur." Model her kareyi yeniden çizer; ürün kayabilir, kenara yeni şey girebilir

-----

## Yönerge: ne hareket eder, ne sabit kalır

- Sahne zaten görselde; yönerge yalnızca **olacak şeyi** anlatır
- Üç soru, üç cümle: Ne hareket ediyor? Ne kıpırdamıyor? Kamera ne yapıyor?
- **Hareket:** tek bir şey, nasıl ve ne yöne. "İnce bir buhar yavaşça yükselip sola dağılıyor"
- **Sabit:** ürünü adıyla an. "Fincan, kitap ve masa tamamen sabit; biçimleri değişmiyor"
- **Kamera:** tek bir hareket ya da hiç. "Sabit kamera" ya da "çok yavaş yaklaşma"
- Süre, oran ve çözünürlük yönergeye yazılmaz; arayüzün ayarlarından seçilir
- Google'ın kılavuzu da aynısını söylüyor: "hareket ettir" gibi belirsiz bir yönerge zayıf sonuç verir
- Başka müşteri, aynı kalıp: çiçekçide yapraklar hafifçe sallanır; vazo ve buket sabit; kamera sabit

-----

## Neye hareket yakışır, neye yakışmaz

- Yakışan: küçük, doğal hareketler; buhar, ışık ve gölge, sayfa, perde, yaprak, camdaki yağmur
- Riskli: eller, yüzler, kalabalık, dönen bir ürün; model görmediği yüzü her karede uydurmak zorunda kalır
- Kamera ne kadar az oynarsa ürün o kadar güvende; ürün işinde sabit kamera yeter
- Birkaç saniyeye tek bir olay sığar; üç hareket isteyen yönerge üçünü de yarım yapar
- Yavaş hareket hem sakin görünür hem ürünü korur; hızlı hareket daha çok uydurma demektir
- Hareketin de bir tonu var: kılavuz "fısıltı gibi" diyorsa hareket de küçük ve yavaş olmalı

**Sohbete yaz:** Konu 8 setinden hangi görsel harekete en uygun? Ne hareket etmeli, ne kesinlikle kıpırdamamalı?

-----

## Yazı ve logo videoya verilmez

- Konu 8'de yazıyı görsele Python koydu; videoda da yazı ve logo en sona, bir düzenleyiciye kalır
- Model her kareyi yeniden çizer: harfler kayar, logo bir karede eğrilip öbüründe düzelir
- Google yeni modelinin yazıyı okunur çizdiğini söylüyor; okunur olmak markanın fontu ve yeri olmak demek değil
- Logo markanın değişmez parçasıdır: yeniden çizilmez, olduğu gibi konur
- Sonradan eklenen yazıyı değiştirmek bedava: tarih, yazım hatası, İngilizcesi; yeni kredi gerekmez
- Videoya verilen görsel de yazısız olmalı: başlıklı gönderi değil, Konu 8'deki çıplak görsel
- Yazıyı ücretsiz bir düzenleyici (Canva, CapCut) ekler; ücretli bir öğe filigran ya da ödeme getirebilir

-----

## Dikey, kısa, önce taslak

- **Oran:** hikâye ve Reels 9:16 dikeydir; kare görselin kenarları kırpılabilir ya da model kenarları doldurabilir
- Hikâyenin üstünü ve altını uygulamanın düğmeleri kapatır; ürünü ve yazıyı ortaya yakın tut
- **Süre:** tek klip birkaç saniye; hikâyeye 4–6 saniye yeter, uzun video kısa kliplerin kurgusudur
- **Neden pahalı:** görsel tek bir kare; bir saniyelik video birbirini tutan onlarca kare
- Ücretsiz arayüz, Konu 8'deki kota gibi, günlük bir **krediyle** çalışır; uzun ve net klip daha çok kredi yer
- Ucuzdan pahalıya git: önce düşük çözünürlüklü bir taslakla yönergeyi sına, sonra asıl sürümü üret
- Taslak yönergeyi sınar, klibi değil: asıl sürüm aynı yönergeyle yapılan yeni bir üretimdir

-----

## Ücretsiz arayüz ve koşulları

- Derste Google Flow: Google'ın tarayıcıda çalışan görsel ve video aracı; 18 yaş ve üstü, Türkiye'de açık
- Google'ın kredi sayfasına göre abonesiz kullanıcıya da her gün ücretsiz kredi var; ilk girişte birlikte bakacağız
- Kullanılmayan kredi ertesi güne geçmez; abonesiz kullanıcı yoğun saatlerde video üretemeyebilir
- Klip dakikalar sürebilir; yeniden basma: ikinci basış ikinci bir üretim, ikinci bir kredi demektir
- Kart isteyen "ücretsiz" teklife kart girme: unutulan deneme ücretli aboneliğe dönüşebilir
- Flow açılmazsa hocanın söyleyeceği yedek arayüz; kural aynı: kartsız, kişisel fotoğraf yok
- Hangi araç olursa olsun soru aynı: bu klip kaç denemeye değer, müşteriye hangisini götüreceğim?

-----

## Müşteriye sunmak: iki varyasyon, bir öneri

- Tek video götürürsen müşteri "evet" ya da "hayır" der; iki varyasyonla "hangisi" der
- Varyasyonlar arasında tek şey değişsin: biri buhar, öteki yağmur; Konu 7'deki kontrollü deney
- Her varyasyona tek cümle gerekçe: "A sıcak bir an, ürünü net gösteriyor; B havayı anlatıyor"
- Önerini nedeniyle söyle; seçimi tümüyle müşteriye bırakmak, tasarım kararını da bırakmaktır
- Ham klibi değil, yazısı eklenmiş son hâli göster: müşteri hikâyeyi değerlendirir
- Yönergelerini sakla: "B olsun ama yağmur azalsın" denirse küçük bir değişiklikle yeniden kullanırsın

-----

## Etik: hareketli görüntüye güven

- Hareketli görüntü belge gibi okunur: izleyen kafeyi ve buharı "gerçekten böyle" sanar
- Mekânı ve ürünü olduğundan farklı gösterme: olmayan bir bahçe, olmayan bir kalabalık, menüde olmayan bir tatlı
- Gerçek bir kişiyi, ünlüyü ya da tanınan bir mekânı taklit etme; araç izin verse de sorumluluk sende
- Müşteriler de sınır koyuyor: Adobe'nin 2026 araştırmasında bazı markalar yapay zekâ insanını son reklamda yasaklıyor
- Etiketle: Meta fotogerçekçi videoda yapay zekâ etiketi isteyebiliyor; paylaşırken aç, müşteriye de söyle
- Google'a göre bu modelin her videosunda gözle görülmeyen bir filigran (SynthID) var; saklamaya çalışmak boşuna

-----

## Sık yanılgılar

- **"Ne kadar çok hareket, o kadar iyi."** Birkaç saniyeye tek olay sığar; fazlası ürünü bozar
- **"Yazıyı da yönergeye yazarım."** Yazı ve logo karede kayar; yazı sonradan, düzenleyicide
- **"Görsel olduğu gibi kalır."** "Ne sabit kalır" cümlesi yoksa ürün de kıpırdayabilir
- **"Gelmedi, demek ki olmadı."** Çoğu zaman henüz bitmedi; yeniden basmak iki kat kredi yer
- **"En yüksek çözünürlük her zaman doğrudur."** Hikâye telefonda izlenir, kredi sınırlı; önce taslak
- **"Taslağı beğendim, asıl sürüm aynısı olur."** Asıl sürüm yeni bir üretimdir; yine izle
- **"Ücretsiz deneme yazıyor, kartımı girerim."** İptal edilmeyen deneme ücretli aboneliğe dönüşebilir

-----

## Bu konunun ödevi ve sıradaki adım

**Kendi müşterin için bir hikâye videosu.**

1. Konu 8 ödevindeki setten bir gönderinin yazısız görselini seç
2. İki yönerge yaz (hareket, sabit, kamera); aralarında yalnız hareket değişsin
3. Önce taslak, sonra iki dikey asıl sürüm üret
4. Birini seç; yazısını ve logosunu ücretsiz bir düzenleyicide ekle
5. Müşterine kısa bir mesaj yaz: önerin, nedeni ve videonun yapay zekâyla üretildiği

Ayrıntılar: `odevler/odev9.md`. Puan yok; Konu 11'in başında sıradaki arkadaşlar gösterecek.

Sıradaki konu, aynı oturumun ikinci yarısı: **Konu 10 — Afiş yarın matbaada: son kontrol.** Yazım hatasını, yanlış günü ve okunmayan rengi afiş matbaaya gitmeden yakalıyoruz.
