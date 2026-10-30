# Konu 9 — Gönderini hareketlendir

Sayfa Kahve, Konu 8'de hazırladığın haftalık seti onayladı ve bir şey daha istedi: "Perşembe gönderisini hikâyede de
paylaşalım, ama biraz kıpırdasın." Markalar durağan gönderinin yanında kısa, dikey videolar da istiyor; Türkiye'deki bazı
sosyal medya tasarımcısı ilanları yapay zekâyla görsel ve video üretmeyi, Reels ve dikey videoyu aynı ilanda arıyor. Bu
konuda Konu 8'deki bir gönderinin **yazısız** görselini birkaç saniyelik dikey bir videoya çeviriyorsun: buhar yükselir,
yağmur camdan süzülür, ışık kayar; ürün ve kompozisyon yerinde kalır. Buna **görselden video** denir: verdiğin görsel ilk
kare olur, model yalnızca ardından olacakları üretir. Yazıyı ve logoyu en sonda bir düzenleyicide eklersin.

**Konunun sonunda elinde:** aynı görselden iki kısa dikey video (iki varyasyon) ve birinin yazısı eklenmiş son hâli.

**Kod ve anahtar yok.** Video arayüzden üretiliyor: Cloudflare'de video modeli yok, Google'ın video modellerini koddan
kullanmak ücretli. Google'ın kredi sayfasına göre arayüzün günlük ücretsiz kredisi bu işe yetiyor (3. bölümdeki kredi planı).

## 1. Görselini seç

- Konu 8'de ürettiğin görseller `08-koddan-toplu-uretim/ciktilar/` içinde (ödevdekiler `odev8/` içinde). Adı
  `_gorsel` ile biten **yazısız** dosyayı al (ör. `Perşembe_gorsel.jpg`); `_gonderi` ve `_hikaye` dosyalarında başlık var,
  onları verme.
- Hareket edebilecek bir öğe ara: buhar, ışık, sayfa, perde, yaprak, camdaki yağmur. Sayfa Kahve setinde Perşembe görseli
  (yağmurlu cam, açık kitap, dumanı tüten fincan) en kolay aday; Cuma görseli (kitabı tutan iki el) en riskli olanı: model
  parmakları her karede yeniden çizer.
- Ürün ortaya yakın dursun. İnsan yüzü olmasın: istek reddedilebilir, Sayfa Kahve'nin kılavuzu da yüz istemiyor.
- Konu 8 görselin yoksa bu klasördeki `veri/yedek_fincan.jpg`'yi kullan (Konu 8'in Perşembe görseli: yağmurlu bir
  pencerenin önünde açık bir kitap ve buharı tüten bir fincan, mavi-krem düz çizim).
- Görselin kare, video dikey (9:16): model kenarları kırpabilir ya da kenarlara yeni bir şey ekleyebilir. Ürün ortadaysa
  ikisi de idare eder; ilk taslakta hangisinin olduğuna bak.

## 2. Yönergeyi yaz: ne hareket eder, ne sabit kalır

Sahne zaten görselde; yönerge yalnızca **olacak şeyi** anlatır. Üç cümle, İngilizce (Konu 7: modeller çoğunlukla İngilizce
metinle eğitildi):

1. **Hareket:** tek bir şey; nasıl ve ne yöne. "Thin steam rises slowly from the cup."
2. **Sabit:** ürünü ve kompozisyonu adıyla an. "The cup, the book and the table stay completely still and keep their shape."
3. **Kamera:** tek bir hareket ya da hiç. "Static camera." (sabit kamera) ya da "Very slow camera push in." (çok yavaş yaklaşma)

Süre, oran ve çözünürlük yönergeye değil, ayarlara yazılır. Yazı, logo, insan istenmez. "Make it move" (hareket ettir) gibi
belirsiz bir yönerge zayıf sonuç verir; Google'ın kendi kılavuzu da kamerayı, öznenin hareketini ve ortamdaki etkiyi tarif
etmeyi öneriyor. Hareketin de bir ses tonu var: Sayfa Kahve "fısıltı gibi" konuşuyorsa hareket de yavaş ve küçük olmalı.

**Sayfa Kahve için üç yönerge.** A, Perşembe görseli, buhar (sıcak bir an):
```text
Thin steam rises slowly from the coffee cup and drifts to the left. The cup, the open book and the table stay completely still and keep their shape and colors. Static camera.
```
B, aynı görsel, yağmur. Yalnızca hareket cümlesi değişti; A ile birlikte müşteriye iki varyasyon:
```text
Raindrops run slowly down the window glass. The cup, the open book and the table stay completely still and keep their shape and colors. Static camera.
```
C, Pazartesi görseli, ışık (sabah hissi; kamera da çok az oynuyor):
```text
Soft morning sunlight moves slowly across the table from left to right, as if a cloud is passing. The cup, the notebook and the table stay completely still. Very slow camera push in.
```

## 3. Flow'da üret

Derste **Google Flow** kullanıyoruz (Google'ın tarayıcıda çalışan görsel ve video aracı). Düğme adları arayüzün İngilizce
hâlindeki gibi **kalın** yazıldı; Türkçe açılırsa karşılıklarını ara.

1. Bilgisayarda Chrome ya da Edge ile `labs.google/fx/tools/flow` adresine git, kişisel Google hesabınla gir (18 yaş ve
   üstü). Kart bilgisi ya da abonelik istenirse **girme**, hocana yaz.
2. Yeni bir proje aç (proje listesindeki yeni proje düğmesi).
3. Yönerge kutusundaki **model adına** tıkla, **Video**'yu, sonra **Frames**'i (kareler) seç.
4. Görselini **+ Add start frame** (başlangıç karesi) kutusuna sürükle. **+ Add end frame** boş kalsın.
5. Yönergeni yapıştır.
6. Ayarlar: oran **9:16** (dikey), çıktı sayısı **1** (her çıktı ayrı kredi yer), model **Gemini Omni Flash**, çözünürlük
   **360p** (düşük çözünürlüklü taslak), süre **6 saniye**. Üretmeden önce kredi değerine bak: 5 olmalı. Seçtiğin model
   bir ayarı desteklemiyorsa Flow seni kendiliğinden başka bir modele geçirir; değer farklıysa ayarları yeniden kontrol et.
7. **Generate**'e (üret; düğmede yalnız bir simge olabilir) bas. Klip dakikalar sürebilir. Kutucukta "Pending" (bekliyor)
   yazıyorsa bekle; **yeniden basma**, ikinci basış ikinci bir üretimdir. Klip hiç görünmüyorsa sayfayı yenile; "Pending"
   uzun süre kalırsa sağ üstteki bildirimlere bak.
8. Taslağı izle: ürün yerinde kaldı mı, hareket okunuyor mu? Kaydıysa "sabit" cümlesini güçlendir ya da hareketi küçült,
   bir taslak daha dene.
9. Yönerge tuttuysa aynı yönergeyle **720p, 6 saniye** (10 kredi) asıl sürümü üret. Taslak yönergeyi sınar, klibi değil:
   asıl sürüm aynı yönergeyle yapılan yeni bir üretimdir, ufak farklar çıkar; yine izle.
10. İndir: klibin üstüne gel, üç noktaya (**More**), sonra **Download**'a tıkla; videoyu seç (**270p** hareketli
    GIF verir, onu seçme). Dosyayı bu klasörde `videolar/` içine koy, adlandır (ör. `persembe_buhar.mp4`). `videolar/`
    depoya girmez.

**Kredi planı.** Google'ın kredi sayfasına göre aboneliği olmayan kullanıcıya her gün 50 kredi veriliyor; kullanılmayan kredi
ertesi güne geçmez, kalanı sağ üstteki profil resminden görürsün.

| İş | Ayar | Kredi |
|---|---|---|
| İki taslak (A ve B) | 360p, 6 sn | 5 + 5 |
| İki asıl sürüm | 720p, 6 sn | 10 + 10 |
| Toplam | | 30 (20 kredi yeniden deneme için kalır) |

Aboneliği olmayanlar Türkiye saatiyle yaklaşık 17.00–20.00 arasında video üretemeyebilir; uyarı görürsen sonra dene.
Flow açılmazsa hocanın söyleyeceği yedek arayüzü kullan; kural aynı: kart girme.

## 4. Yazıyı ve logoyu sonradan ekle

Konu 8'de yazıyı görsele model değil Python koymuştu; videoda da yazı en sona kalır. Model her kareyi yeniden çizer: harf
kayabilir, logo bir karede eğrilip öbüründe düzelebilir, Türkçe harfler bozulabilir. Sonradan eklenen yazıyı değiştirmek de
bedava: tarih değişti ya da yazım hatası çıktı diye yeni video üretmen gerekmez.

**Canva'nın ücretsiz sürümüyle** (`canva.com`; menü adları Türkçe arayüzde biraz farklı olabilir):

1. Yeni bir tasarım aç: Instagram hikâyesi ya da 1080 × 1920 özel boyut.
2. Videonu **Yüklemeler**'den sayfaya sürükle; sayfayı doldursun.
3. Kılavuz logoyu doğrudan fotoğrafın üstüne koymayı yasaklıyor: alta kâğıt beyazı (#F4F1EA) bir şerit koy, Konu 8'deki
   hikâyede olduğu gibi. Başlığı **Metin** ile şeride yaz, mürekkep mavisi (#1F3A5F), listedeki serifli bir fontla.
   Logon varsa görsel olarak yükle, şeride koy.
4. Şeridi ve yazıyı ekranın alt ve üst kenarından uzak tut. Müşteri yazdı: "Hikâyelerde yazı ekranın üst ve alt kenarına
   çok yakın olmasın, telefonda kesiliyor."
5. **Paylaş** → **İndir** → MP4. Ücretli (taçlı) bir öğe kullanırsan filigranlı çıkabilir ya da ödeme ister; kullanma.

Canva yerine CapCut'ın ücretsiz sürümü de olur; şablon kullanırsan sonuna filigranlı bir kapanış eklenebilir. Ücretsiz
kullanım koşulları değişebilir: ilk dışa aktarmada filigran var mı, bak. Klipte ses gelebilir; müzik müşterinin seçimiyse
düzenleyicide sesi kapat.

## 5. Müşteriye sun

- İki varyasyon götür, aralarında tek şey değişsin (A buhar, B yağmur). Konu 7'deki kontrollü deneyin aynısı.
- Her birine tek cümle gerekçe yaz, sonra önerini ve nedenini söyle: "A'yı öneriyorum; buhar sıcak bir an, yağmur ise
  gözü ürünün önündeki cama çekiyor."
- Ham klibi değil, yazısı eklenmiş son hâli göster: müşteri hareketi değil, hikâyeyi değerlendirecek.
- Videonun yapay zekâyla üretildiğini söyle; paylaşırken yapay zekâ etiketini aç (Meta fotogerçekçi videoda isteyebiliyor).
- Mekânı olduğundan farklı gösterme: kafede olmayan bir bahçe, gerçekte olmayan bir kalabalık müşteriyi yanıltır.

## Sık sorunlar

| Ne oldu | Ne yap |
|---|---|
| Fincan eriyor, kitap şekil değiştiriyor | "Sabit" cümlesinde ürünü adıyla an; kamerayı sabitle; hareketi küçült |
| Kareye görselde olmayan bir şey girdi (el, insan, ikinci fincan) | Yönergede tek hareket bırak; hızlı hareket ve kamera dönüşü isteme |
| Videoda harfler ya da yazı belirdi | Görselin gerçekten yazısız mı? Yazısız hâlini ver, yeniden dene |
| Hiçbir şey kıpırdamıyor | Hareketi somutlaştır: nereden, ne yöne, ne hızla ("rises slowly and drifts to the left") |
| Klip yatay geldi | Oran yönergeyle değil, ayarlarla seçilir: 9:16 |
| Kredi bitti | Ertesi gün; her zaman önce 360p taslak |
| Görsel ya da üretim reddedildi | Gerçek bir kişi, ünlü ya da çocuk olmasın; başka görsel dene. Google'a göre başarısız üretimin kredisi bir saat içinde geri gelir |

## Kendini dene: bu yönergede ne yanlış?

1. `Animate this image, make it cinematic and amazing.`
2. `Steam rises, the pages turn, the light moves, rain falls, the camera orbits around the table and zooms in.`
3. `Steam rises from the cup. The words "Sessiz Okuma Gecesi" and the Sayfa Kahve logo appear at the top.`
4. `Steam rises slowly from the cup. Static camera.` (Bu yönergeye hangi cümle eklenmeli?)
5. `A smiling young woman reads next to the cup while customers chat in the background.`
6. `Steam rises slowly from the cup. The cup and the table stay still. Static camera. Vertical 9:16, 6 seconds.`

## Ödev ve sonraki konu

Ödev: `odevler/odev9.md` (kendi müşterin için iki varyasyon ve yazısı eklenmiş son hâl). Aynı oturumun ikinci yarısı:
**Konu 10 — Afiş yarın matbaada: son kontrol.** Afiş matbaaya gitmeden önce yazım hatasını, yanlış günü ve okunmayan
rengi yakalıyoruz.

## Kendini dene — cevaplar

1. Ne hareket edeceği, ne sabit kalacağı ve kamera yok; "cinematic, amazing" modele bir şey söylemiyor.
2. Beş hareket birden: birkaç saniyeye tek olay sığar. Kamera dönüşü fincanın görünmeyen arka yüzünü uydurtur.
3. Yazı ve logo videoya verilmiş: karede kayar, değişince yeniden üretmek gerekir. Sonradan, düzenleyicide.
4. "Sabit" cümlesi eksik: `The cup, the book and the table stay completely still and keep their shape.`
5. Görselde olmayan insanlar ekliyor; kılavuz yüz istemiyor, mekânı da olduğundan kalabalık gösteriyor. Müşteriler son
   reklamda yapay zekâyla üretilmiş insan istemeyebilir.
6. Yönergenin kendisi iyi; ama oran ve süre ayarlardan seçilir, yönergeye yazmak işe yaramaz. Son cümleyi sil.
