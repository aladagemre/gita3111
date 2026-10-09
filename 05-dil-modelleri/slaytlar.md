# Konu 5 — Dil Modelleri Nasıl Çalışır?

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 4'ten Konu 5'e

- **Konu 2'de** modele soru sorduk, cevap aldık; model kapalı bir kutuydu
- **Konu 3'te** bir modelin örneklerden nasıl öğrendiğini gördük
- **Konu 4'te** modelin kelimeleri sayı listelerine çevirdiğini gördük
- **Bugün:** model cevabını **nasıl yazıyor**?
- Sohbet modelleri düşünüyor, anlıyor, biliyor gibi görünür; perdenin arkasında ne var?
- Cevap şaşırtıcı derecede basit: sihir yok, sayma ve seçme var

-----

## Dil modeli tek bir iş yapar: sıradaki kelimeyi tahmin eder

- Telefonunun klavyesi yazarken sıradaki kelimeyi önerir; dil modeli de temelde bunu yapar
- Elindeki metne bakar ve "bundan sonra en büyük ihtimalle ne gelir?" diye sorar
- Bu tahmini binlerce kez art arda yapınca paragraflar, şiirler, kodlar çıkar
- Fark ölçekte: telefonun klavyesi son birkaç kelimeye bakar, büyük model binlerce kelimeye
- Ve milyarlarca metinden öğrenmiştir; bu yüzden tahminleri şaşırtıcı derecede akıcı

**Sohbete yaz:** "Sessiz bir çalışma ..." cümlesini sen nasıl bitirirdin?

-----

## Model metni kelime kelime değil, parça parça okur

- Model kelimeleri değil, **belirteç** (token) denen parçaları görür
- Sık geçen kelimeler tek parçadır; seyrek kelimeler birkaç parçaya bölünür
- Parça sözlüğü dilbilgisine göre değil, metinlerde **sık geçen harf dizilerine** göre kurulur
- Bu yüzden parçalar her zaman kök ve ek gibi anlamlı bölünmez: "tasarımı" "tas", "ar", "ımı" diye bölünebilir
- Her parçanın sözlükte bir **numarası** var; model kelimeyi değil, bu numaraları görür
- Konu 4'teki gibi her numara da bir vektöre çevrilir; modelin asıl işlediği bu vektörler

-----

## Türkçe neden daha çok parçaya bölünüyor?

- Parça sözlükleri çoğunlukla İngilizce ağırlıklı metinlerden kurulur
- İngilizcede sık kelimeler kısa ve değişmez; çoğu tek parçadır
- Türkçede ekler art arda dizilir: "görselleştiremediklerimizden" tek bir kelime
- Bu biçimlerin her biri seyrek geçer; sözlükte yoktur, küçük parçalara bölünür
- Sonuç: aynı anlamdaki bir Türkçe cümle, İngilizcesinden belirgin biçimde daha çok parça tutar
- Bunu ödevde kendi cümlelerinle ölçeceksin

-----

## Bağlam penceresi: model yalnızca pencerenin içini görür

- Model bir seferde ancak belli sayıda parçaya bakabilir; buna **bağlam penceresi** denir
- Sohbet uzadıkça ilk yazdıkların pencereden taşar; model onları unutmaz, **hiç görmez**
- Uzun sohbetlerde modelin baştaki talimatları "unutması" bundandır
- Konu 2'de soruya eklediğimiz bağlam da bu pencereye girer
- Türkçe daha çok parçaya bölündüğü için pencereyi daha çabuk doldurur
- Ücretli modellerde fiyat parça sayısına göre hesaplanır: Türkçe aynı iş için daha pahalıya gelir

-----

## Olasılık: hangi kelime, hangi şansla?

- Model sıradaki kelime için tek bir cevap değil, bir **liste** üretir: her aday için bir şans
- Bu şansa **olasılık** denir: 0 ile 1 arasında bir sayı; bütün adayların olasılıkları toplanınca 1 eder
- En basit yolu saymaktır: bir metinde "bir"den sonra 6 kez kelime gelmişse ve 3'ü "yer" ise, "yer"in olasılığı 3/6 = 0.5
- Adayların ve olasılıklarının tamamına **olasılık dağılımı** denir
- Gerçek model de her adımda böyle bir dağılım hesaplar; ama saymaz, milyarlarca metinden öğrendiği vektörlerle hesaplar
- Bugün önce Konu 1'in kafe yorumlarından **sayan** küçük bir model kuracağız

**Tahmin et, sohbete yaz:** müşteriler "biraz" kelimesinden sonra övgü mü yazmış, şikâyet mi?

-----

## Metin üretmek: tahmini tekrar tekrar yapmak

1. Bir başlangıç kelimesi ver
2. Model sıradaki kelime için olasılık dağılımını hesaplar
3. Dağılımdan bir kelime seçilir ve metnin sonuna eklenir
4. Yeni metinle 2. adıma dönülür

- Bu döngü, model "metin bitti" anlamına gelen özel bir parça seçene ya da bir sınıra gelene kadar sürer
- Sohbet modelinin cevabı da kelime kelime ekranda belirir; bu döngüyü canlı izliyorsun
- Asıl soru 3. adımda: dağılımdan **hangi** kelimeyi seçeceğiz?

-----

## Seçmenin iki yolu: hep en olası ya da zar

- **Hep en olası:** her adımda olasılığı en yüksek kelimeyi seç
- Güvenli görünür: her adımda en büyük ihtimal
- **Zar atmak:** kelimeyi olasılığına göre rastgele seç; olasılığı 0.5 olan kelime iki seferden birinde gelir
- En olası kelime çoğu zaman gelir, ama hep değil; her çalıştırmada başka bir metin
- Konu 2'de aynı soruya her seferinde farklı cevap gelmesinin sebebi bu

**Tahmin et, sohbete yaz:** hep en olası kelimeyi seçerek 8 kelimelik bir cümle kursak anlamlı olur mu? İkinci kez çalıştırınca aynı cümle mi gelir?

-----

## Sıcaklık: seçimi ayarlayan düğme

- **Sıcaklık**, modelin en olasıya ne kadar sadık kalacağını belirleyen ayar
- **Düşük sıcaklık:** dağılım sivrilir; en olası kelimenin şansı artar, sonuç tutarlı ve tekrarlanabilir
- **Yüksek sıcaklık:** dağılım düzleşir; seyrek kelimeler de şans bulur, sonuç çeşitli ama dağınık
- Sıcaklık 0'a yaklaştıkça model "hep en olası" yoluna döner
- Yüksek sıcaklık "daha yaratıcı" değil, **daha dağınık** demek: bazen ilginç, bazen anlamsız
- Sohbet sitelerinde bu ayar gizlidir; API'de sen seçersin

-----

## Hangi iş için hangi sıcaklık?

- **Kurumsal tabela, menü, yönlendirme metni:** düşük sıcaklık; tutarlılık ve doğruluk önemli
- **Ürün açıklaması, e-posta:** orta sıcaklık; akıcı ama kontrollü
- **Fikir fırtınası, ilk eskiz, isim bulma:** yüksek sıcaklık; çok seçenek, ayıklamayı sen yaparsın
- Sıcaklık bir **araç ayarıdır**: işin türüne göre seçilir, "en iyisi" yoktur
- Bugün aynı slogan sorusunu üç farklı sıcaklıkla sorup sonuçları bir panoda yan yana koyacağız

**Tahmin et:** yüksek sıcaklıktaki sloganların kaçı kullanılabilir olacak?

-----

## Model bilmez, olası olanı söyler

- Model "doğru olan" kelimeyi değil, **olası olan** kelimeyi seçer
- Çoğu zaman doğru olan aynı zamanda olası olandır; bu yüzden model çoğunlukla doğru görünür
- Ama olası ile doğru ayrıştığında model kendinden emin bir dille yanlış bilgi üretir
- Buna **halüsinasyon** denir: var olmayan bir kitap, uydurma bir kaynak, yanlış bir tarih
- Model "bilmiyorum" demeyi ayrıca öğrenmedikçe boşluğu en olası görünen cümleyle doldurur
- Tasarımcı için kural: modelin yazdığı her bilgiyi, özellikle isim, sayı ve kaynakları kontrol et

-----

## Sohbet modeli nasıl sohbet ediyor?

- Ham bir dil modeli yalnızca metni devam ettirir; soru sorarsan cevap yerine başka sorular yazabilir
- Sohbet modelleri ek bir eğitimden geçer: binlerce örnek soru–cevap ve insanların "bu cevap daha iyi" işaretlemeleri
- Böylece model "bir asistan gibi cevap vermeyi" öğrenir
- Ama altta yatan iş değişmez: sıradaki parçayı tahmin etmek
- Senin yazdığın soru, sohbet geçmişi ve gizli talimatlar tek bir metin olarak pencereye girer; model bunun devamını yazar
- Bu yüzden iyi bir soru, iyi bir başlangıç metnidir: model ona en çok yakışan devamı yazar

-----

## Bu konunun ödevi

**1. Üç sıcaklık.** Kendi seçtiğin bir iş (afiş başlığı, ürün adı, slogan) için dersteki slogan panosunu kendi sorunla çalıştır, `pano.txt` dosyasını getir. Hangi sıcaklık işe yaradı, neden?

**2. Belirteç sayısı.** Bir Türkçe cümle ve aynı anlamda bir İngilizce cümle seç; ikisini de belirteçlere ayır. Hangisi kaç parça?

Ayrıntı: `odevler/odev5.md`

-----

## Hatırlanacak dört şey

1. **Model metni parça parça okur.** Türkçe daha çok parçaya bölünür; pencereyi daha çabuk doldurur, daha pahalıya gelir
2. **Model her adımda sıradaki parçayı tahmin eder.** Uzun metin, bu tahminin tekrarıdır
3. **Tahmin bir olasılık dağılımıdır.** Model doğru olanı değil, olası olanı seçer; bu yüzden halüsinasyon görür
4. **Sıcaklık seçimi ayarlar.** Düşük: neredeyse hep en olası, hep aynı. Yükseldikçe: zar, her seferinde farklı

Sıradaki konu: **Konu 6 — Kaput açma: üretmek ne demek.**
