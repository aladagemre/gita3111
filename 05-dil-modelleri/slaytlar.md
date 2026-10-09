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

## Dil modeli tek bir iş yapar: sıradaki parçayı tahmin eder

![Sessiz bir çalışma cümlesinin devamı için üç aday ve sayıları](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/sonraki_parca.png)

- "Sessiz bir çalışma ..." cümlesini sen nasıl bitirirdin?
- En sık söyleneni seçmek: tahminin en basit yolu
- Az önce bir dil modeli gibi davrandın

-----

## Model metni kelime kelime değil, parça parça okur

![Sessiz bir çalışma kafesi: 4 kelime, 6 renkli parça](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/belirtec_seridi.png)

- Her renkli kutu bir **belirteç** (token)
- Sık kelimeler tek parça, seyrek kelimeler bölünür
- Model kelimeyi değil, parçanın **numarasını** görür

-----

## Türkçe aynı sözü daha çok parçayla söylüyor

![Üç cümlenin kelime ve parça sayısı](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/turkce_ingilizce.png)

- İngilizce cümle: her kelime tek parça
- Türkçe ekler art arda dizilir; her biçim seyrek kalır, bölünür

-----

## Tek bir Türkçe kelime 8 parçaya dağılıyor

![Kütüphanedekilerden misiniz: 11 renkli parça](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/uzun_kelime.png)

Parça sözlüğü dilbilgisinden değil, metinlerde **sık geçen harf dizilerinden** kurulmuş.

-----

## Bağlam penceresi: model yalnızca pencerenin içini görür

![Kafe yorumlarının parçaları; son 16 parça mavi çerçevenin içinde, öncekiler gri](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/baglam_penceresi.png)

- Uzun sohbette ilk yazdıkların pencereden taşar: model onları **hiç görmez**
- Türkçe pencereyi daha çabuk doldurur; ücretli modellerde daha pahalıya gelir
- Her modelin kendi parça sözlüğü var; fikir aynı

-----

## Kendi küçük modelimiz: "biraz"dan sonra ne geliyor?

![biraz kelimesinden sonra gelen dört kelime: pahalı, karanlık, kısa, fazla](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/biraz_sonra.png)

- Veri: Konu 1'in 30 kafe yorumu
- Model yok, sadece sayıyoruz: hangi kelimeden hemen sonra ne gelmiş?
- Müşteriler överken "biraz" demiyor; şikâyeti yumuşatırken diyor

-----

## Bulgu: "biraz" neyi düzelteceğini söylüyor

![Dört şikâyet cümlesi ve her birinin kimin işi olduğu](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/biraz_okuma.png)

- Işık ve menü tasarımcının işi; fiyat değil
- "biraz fazla sessiz": aynı özellik, iki kullanıcı
- Bir kelimenin ne anlattığını, ardından gelenler söyler

-----

## "çok"tan sonra: bir olasılık dağılımı

![çok kelimesinden sonra güzel 0.4, kalabalık, keyifli, tatlı 0.2](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/cok_dagilim.png)

- Olasılık = adet / toplam; hepsinin toplamı **1**
- "çok" çoğunlukla övgü; beşten üçü **bahçe**. "biraz" düzeltilecekleri, "çok" korunacakları veriyor
- Gerçek model de her adımda böyle bir dağılım hesaplar; 30 yorumdan değil, milyarlarca metinden

-----

## Hep en olasıyı seç: her ikili gerçek, cümle anlamsız

![kahve ortalama tatlılar güzel yazın bahçede oturmak için en: kelime kutuları zinciri](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/acgozlu_zincir.png)

- Metin üretmek = tahmini tekrarlamak
- Her seferinde **aynı** cümle
- Bir yorum gibi duruyor ama hiçbir müşteri yazmadı: kafe sitesinde fark eder miydin?

-----

## Zar at: "güzel" çoğu zaman gelir, ama hep değil

![çok kelimesinden sonra gelen beş kutu, ikisi güzel](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/zar.png)

- Listede iki kez geçen kelimenin şansı iki kat
- Her çalıştırmada **başka** bir cümle
- Gerçek modelde "metin bitti" diye bir parça da var; onu seçince yazmayı bırakır

-----

## Sıcaklık: aynı dağılım, üç ayar

![çok dağılımı sıcaklık 0.5, 1 ve 2'de](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/sicaklik.png)

- Düşük: uzun çubuk uzar → hep en olası (Adım 4)
- 1: olasılığa göre zar (Adım 5)
- Yüksek: çubuklar eşitlenir → seyrek seçenekler daha çok şans bulur
- Çizim bizim "çok" sayımımızdan hesaplandı; gerçek model aynı işi kendi olasılıklarına yapar

-----

## Yüksek sıcaklık "daha yaratıcı" değil, "daha dağınık"

| Sıcaklık | Ne yapar | Defterde |
|---|---|---|
| Düşük (0.1) | Hep en olası parçayı seçer | Adım 4: hep aynı cümle |
| Orta (0.7–1) | Olasılığa göre zar atar | Adım 5: zar |
| Yüksek (1.5) | Zar hileli: düşük olasılıklara daha çok şans | Adım 6'da göreceğiz |

Sıcaklık bir **seçim kuralı** ayarı, yaratıcılık düğmesi değil.

-----

## Kendi modelimizden gerçek modele

- Defterde önce 30 yorumdan **sayan** küçük bir model kuracağız
- Gerçek model de her adımda sıradaki parçayı seçer; milyarlarca metinden öğrenmiş
- En olasıyı mı seçsin, zar mı atsın? Bunu **sıcaklık** ayarlar; gerçek modelde onu biz değiştireceğiz

-----

## Slogan panosu: aynı soru, üç sıcaklık, yan yana

![Üç sütunlu boş pano: sıcaklık 0.1, 0.7, 1.5](https://raw.githubusercontent.com/aladagemre/gita3111/main/05-dil-modelleri/gorseller/slogan_pano.png)

- **Kurumsal tabela, menü, yönlendirme** için hangi sıcaklık?
- **Fikir fırtınası, ilk eskiz** için hangisi?
- 1.5'teki sloganlardan kaçı kullanılabilir?

Sıcaklık bir **araç ayarı**: işin türüne göre seçilir, "en iyisi" yok.

-----

## Şimdi deftere geçiyoruz: `ders.ipynb`

**Isınma** — cevapları `Counter` ile say
**1.** Cümleyi belirteçlere ayır (önce `tiktokenizer.vercel.app`)
**2.** "biraz" ve "çok"tan sonra ne geliyor?
**3.** Sayıdan olasılığa, çubuk grafik
**4.** Hep en olasıyı seçerek metin üret
**5.** Zarla üret
**6.** Gerçek model, üç sıcaklık
**7.** Slogan panosu: `pano.txt`

Isınma ve Adım 1–5 **anahtarsız**. Adım 6–7 `anahtar.txt` ister.

-----

## Bu konunun ödevi

**1. Üç sıcaklık.** Kendi seçtiğin bir iş (afiş başlığı, ürün adı, slogan) için Adım 7'yi kendi sorunla çalıştır, `pano.txt` getir. Hangi sıcaklık işe yaradı, neden?

**2. Belirteç sayısı.** Bir Türkçe cümle ve aynı anlamda bir İngilizce cümle seç; ikisini de belirteçlere ayır. Hangisi kaç parça?

Ayrıntı: `odevler/odev5.md`

-----

## Hatırlanacak dört şey

**1. Model metni parça parça okur.** Türkçe daha çok parçaya bölünür.

**2. Model her adımda sıradaki parçayı tahmin eder.** Uzun metin, bu tahminin tekrarıdır.

**3. Tahmin bir olasılık dağılımıdır.** Model anlamaz; milyarlarca metinden sayar.

**4. Sıcaklık seçimi ayarlar.** Düşük: hep en olası, hep aynı. Yüksek: zar, her seferinde farklı.

Sıradaki konu: **Konu 6 — Kaput açma: üretmek ne demek.**
