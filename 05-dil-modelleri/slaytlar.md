# Konu 5 — Dil Modelleri Nasıl Çalışır?

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 4'ten Konu 5'e

- **Konu 2'de:** modele soru sorduk, cevap aldık. Model kapalı bir kutuydu
- **Konu 4'te:** model kelimeyi sayı listesine çeviriyordu
- **Bugün:** model **nasıl yazıyor**?

Sihir yok. Sayma ve seçme var.

-----

## Dil modeli tek bir iş yapar: sıradaki kelimeyi tahmin eder

![Sessiz bir çalışma cümlesinin sonu boş bir kutu: sen nasıl bitirirdin?](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/sonraki_parca.png)

- **Sohbete yaz:** "Sessiz bir çalışma ..." cümlesini sen nasıl bitirirdin?
- En sık söyleneni seçmek: tahminin en basit yolu
- Az önce bir dil modeli gibi davrandın

-----

## Model metni kelime kelime değil, parça parça okur

![Renkli bir afiş tasarımı: 4 kelime, 9 renkli parça](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/belirtec_seridi.png)

- Her renkli kutu bir **belirteç** (token)
- Sık kelimeler tek parça, seyrek kelimeler bölünür
- Model kelimeyi değil, parçanın **numarasını** görür

-----

## Aynı söz: Türkçede 9 parça, İngilizcede 4

![Türkçe ve İngilizce cümlenin ve uzun bir kelimenin kelime ve parça sayısı](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/turkce_ingilizce.png)

- İngilizce cümle: her kelime tek parça
- Türkçe ekler art arda dizilir; her biçim seyrek kalır, bölünür

-----

## Tek bir Türkçe kelime 10 parçaya dağılıyor

![Görselleştiremediklerimizden: 10 renkli parça](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/uzun_kelime.png)

Parça sözlüğü dilbilgisinden değil, metinlerde **sık geçen harf dizilerinden** kurulmuş.

-----

## Bağlam penceresi: model yalnızca pencerenin içini görür

![Kafe yorumlarının parçaları; son 16 parça mavi çerçevenin içinde, öncekiler gri](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/baglam_penceresi.png)

- Uzun sohbette ilk yazdıkların pencereden taşar: model onları **hiç görmez**
- Türkçe pencereyi daha çabuk doldurur; ücretli modellerde daha pahalıya gelir

-----

## Tahmin et: müşteriler "biraz"dan sonra ne yazmış?

![biraz kelimesinden sonra gelen dört boş kutu](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/biraz_sonra.png)

- Veri: Konu 1'in 30 kafe yorumu. Model yok, sadece sayacağız
- **Sohbete yaz:** "biraz"dan sonra övgü mü gelir, şikâyet mi?
- Cevabı defterde, Adım 2'de bulacağız

-----

## Olasılık dağılımı: "bir"den sonra hangi kelime, hangi şansla?

![bir kelimesinden sonra yer 0.50, şey 0.33, köşe 0.17](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/bir_dagilim.png)

- Olasılık = adet / toplam: "yer" 6 geçişin 3'ü
- Üç olasılığı topla: kaç ediyor?
- Gerçek model de her adımda böyle bir dağılım hesaplar; 30 yorumdan değil, milyarlarca metinden öğrenmiş

-----

## Metin üretmek = tahmini tekrar tekrar yapmak

![kahve kelimesinden başlayan, sekiz soru işaretli kutudan oluşan zincir](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/acgozlu_zincir.png)

- Her turda son kelimeden sonra **en olası** kelimeyi ekle
- **Tahmin et:** 8 tur sonra anlamlı bir cümle çıkar mı?
- İkinci kez çalıştırınca aynı cümle mi gelir? Defterde Adım 4'te göreceğiz

-----

## Zar at: en olası çoğu zaman gelir, ama hep değil

![bir kelimesinden sonra gelen altı kutu, üçü yer](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/zar.png)

- Listede üç kez geçen kelimenin şansı, bir kez geçenin üç katı
- Her çalıştırmada **başka** bir cümle

-----

## Sıcaklık: aynı dağılım, üç ayar

![bir dağılımı sıcaklık 0.5, 1 ve 2'de; örnek çizim](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/sicaklik.png)

- **Sıcaklık:** gerçek modelde en olasıyı mı seçeceğini, zar mı atacağını belirleyen ayar
- **Örnek çizim:** bizim "bir" sayımımızdan hesaplandı, model çıktısı değil
- Düşük: uzun çubuk uzar → en olası daha sık seçilir. Yüksek: çubuklar eşitlenir → seyrek seçenekler şans bulur
- Yüksek sıcaklık "daha yaratıcı" değil, **daha dağınık**: bir seçim kuralı ayarı

-----

## Slogan panosu: aynı soru, üç sıcaklık, yan yana

![Üç sütunlu boş pano: sıcaklık 0.1, 0.7, 1.5](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/slogan_pano.png)

- **Kurumsal tabela, menü, yönlendirme** için hangi sıcaklık?
- **Fikir fırtınası, ilk eskiz** için hangisi?
- **Tahmin et:** 1.5'teki sloganlardan kaçı kullanılabilir olacak?

Sıcaklık bir **araç ayarı**: işin türüne göre seçilir, "en iyisi" yok.

-----

## Şimdi deftere geçiyoruz: `ders.ipynb`

**Isınma** — sınıfın cevaplarını `Counter` ile say
**1.** Cümleyi belirteçlere ayır (önce `tiktokenizer.vercel.app`)
**2.** "biraz" ve "çok"tan sonra ne geliyor?
**3.** Sayıdan olasılığa, çubuk grafik
**4.** Hep en olasıyı seçerek metin üret
**5.** Zarla üret
**6.** Gerçek model, üç sıcaklık
**7.** Slogan panosu: `pano.txt`

Isınma ve Adım 1–5 **anahtarsız**. Adım 6–7 `anahtar.txt` ister.

-----

## Adım 2'den sonra: "biraz" bir iş listesi

![Dört şikâyet cümlesi ve her birinin kimin işi olduğu](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/biraz_okuma.png)

- Işık ve menü tasarımcının işi; fiyat değil
- "biraz fazla sessiz": aynı özellik, iki kullanıcı
- Bir kelimenin ne anlattığını, ardından gelenler söyler

-----

## Bu konunun ödevi

**1. Üç sıcaklık.** Kendi seçtiğin bir iş (afiş başlığı, ürün adı, slogan) için Adım 7'yi kendi sorunla çalıştır, `pano.txt` getir. Hangi sıcaklık işe yaradı, neden?

**2. Belirteç sayısı.** Bir Türkçe cümle ve aynı anlamda bir İngilizce cümle seç; ikisini de belirteçlere ayır. Hangisi kaç parça?

Ayrıntı: `odevler/odev5.md`

-----

## Hatırlanacak dört şey

**1. Model metni parça parça okur.** Türkçe daha çok parçaya bölünür.

**2. Model her adımda sıradaki parçayı tahmin eder.** Uzun metin, bu tahminin tekrarıdır.

**3. Tahmin bir olasılık dağılımıdır.** Model anlamaz; milyarlarca metinden öğrendiği olasılıklarla seçer.

**4. Sıcaklık seçimi ayarlar.** Düşük: neredeyse hep en olası, hep aynı. Yükseldikçe: zar, her seferinde farklı.

Sıradaki konu: **Konu 6 — Kaput açma: üretmek ne demek.**
