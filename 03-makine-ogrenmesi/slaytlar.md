# Konu 3 — Makine Öğrenmesi Nedir?

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 2'den Konu 3'e: hazır modelden kendi modelimize

- Konu 2'de hazır bir modele soru sorduk; model kapalı bir kutuydu
- Bugün kutuyu açıyoruz: bir model nasıl ortaya çıkar, neyi bilir, neyi bilemez?
- Bunu milyarlarca metinle değil, sınıfın kendi verisiyle göreceğiz: Konu 2 ödevinde etiketlediğiniz 20 renk
- Model kuracağız, eğiteceğiz, sınavdan geçireceğiz ve yanıldığı yerlere bakacağız
- Matematik yok; her kavramın bir günlük hayat karşılığı var

-----

## Yapay zeka, makine öğrenmesi, derin öğrenme

- Üç terim sık karıştırılır; iç içe halkalar gibi düşün
- **Yapay zeka:** insan zekası gerektiren işleri yapan programların genel adı; en dış halka
- **Makine öğrenmesi:** yapay zekanın bir yolu; kuralı insan yazmaz, program örneklerden çıkarır
- **Derin öğrenme:** makine öğrenmesinin çok katmanlı, çok büyük modellerle yapılanı; en iç halka
- Sohbet modelleri ve görsel üreticiler derin öğrenme ürünleri
- Bugün en basit makine öğrenmesi modellerinden biriyle çalışıyoruz; ama temel fikirler büyük modellerde de aynı

-----

## Kuralı ya sen yazarsın ya da model örneklerden çıkarır

- **Klasik program:** kuralı sen yazarsın. "E-postada 'bedava kazandınız' geçiyorsa spam klasörüne at"
- Spam yazanlar kelimeyi değiştirir; kural yazan her seferinde bir adım geride kalır
- **Makine öğrenmesi:** binlerce örnek verirsin: "bu spam, bu değil"
- Program örneklerdeki ortak deseni kendisi bulur; bu sürece **eğitim** denir
- Eğitimin sonunda elde edilen şeye **model** denir: yeni bir örnek gelince cevap veren kural kümesi
- Kuralı yazmanın zor ya da imkânsız olduğu her yerde makine öğrenmesi devreye girer

-----

## Makine öğrenmesi zaten her yerde

- **Telefonun kamerası:** portre modunda yüzü bulup arka planı bulanıklaştırır
- **Yüz tanıma:** telefonun kilidini senin yüzünle açar, başkasınınkiyle açmaz
- **Spotify ve Netflix:** dinlediğine, izlediğine bakıp sana öneri yapar; Netflix sana gösterdiği kapak görselini bile seçer
- **Photoshop ve Canva:** arka planı tek tıkla silen araç binlerce örnekle eğitildi
- **E-posta:** spam filtresi ve otomatik cümle tamamlama
- Ortak nokta: hiçbirinde "şu şartta şunu yap" kuralını bir insan tek tek yazmadı

-----

## Veri: öznitelik ve etiket

- Makine öğrenmesinin verisi bir tabloya benzer: her satır bir örnek
- **Öznitelik:** modelin baktığı bilgiler; tablonun sütunları
- **Etiket:** modelin tahmin etmesi gereken cevap
- Ev fiyatı örneği: metrekare, oda sayısı, semt öznitelik; fiyat etiket
- Bizim verimiz: bir rengin sayıları öznitelik, öğrencinin o renge verdiği "sakin / enerjik / ciddi" etiketi etiket
- Kodda geleneksel adları: öznitelikler **X**, etiketler **y**; her satırın X'i ile y'si aynı sırada durmalı

-----

## Model renk görmez, sayı görür

- Bilgisayar için her şey sayıdır; renk de
- Ekrandaki her renk üç ışığın karışımı: **kırmızı, yeşil, mavi** (RGB), her biri 0 ile 255 arasında
- Tasarım programlarındaki renk seçicide gördüğün `#E63946` gibi kod da bu üç sayının kısaltması
- Model rengin adını, nerede kullanıldığını, hangi duyguyu çağrıştırdığını bilmez; yalnızca üç sayıya bakar
- Bu yüzden modelin "benzer renk" dediği şey, sayıları birbirine yakın renk demek
- Sayılardaki yakınlık gözümüzdeki benzerlikle her zaman örtüşmez; bunu konunun sonunda konuşacağız

-----

## İki tür soru: sınıflandırma ve sayı tahmini

- **Sınıflandırma:** cevap birkaç kategoriden biri. "Bu renk sakin mi, enerjik mi, ciddi mi?"
- **Sayı tahmini (regresyon):** cevap bir sayı. "Bu evin fiyatı ne olur?"
- Spam filtresi, yüz tanıma, renk duygusu: sınıflandırma
- Ev fiyatı, yarın kaç kişinin kafeye geleceği, bir gönderinin kaç beğeni alacağı: sayı tahmini
- Bugünkü işimiz sınıflandırma: her renge üç etiketten birini vereceğiz

**Sohbete yaz:** "bir afiş tasarımının kaç beğeni alacağını tahmin etmek" hangisi?

-----

## Etiketleri insanlar verir

- Modelin öğrendiği her şey etiketlerden gelir; etiketleri de çoğunlukla **insanlar** verir
- Büyük şirketler binlerce kişiye görsel, metin, ses etiketletir
- "Bu fotoğrafta kedi var mı?" gibi sorularda insanlar çoğunlukla anlaşır
- "Bu renk sakin mi?" gibi **öznel** sorularda anlaşamazlar; renk algısı kültüre, deneyime, zevke bağlı
- Etiketler tutarsızsa model de tutarsız olanı öğrenir
- Bugünkü veride her rengi 12 öğrenci etiketledi: bu anlaşmazlığı kendi gözümüzle göreceğiz

**Tahmin et, sohbete yaz:** neredeyse aynı görünen iki açık renge sınıf aynı etiketi mi verdi?

-----

## Eğitim ve test: ezberi değil, öğrenmeyi ölç

- Bir öğretmen sınavda derste çözdüğü soruların aynısını sorarsa ne ölçer? **Ezberi**
- Model için de aynısı: eğittiğin örneklerle sınarsan sonuç olduğundan iyi görünür
- Bu yüzden veriyi ikiye böleriz: **eğitim** verisi ve **test** verisi
- Model yalnızca eğitim verisini görür; test verisi sınav günü çıkar
- Genellikle verinin dörtte üçü eğitime, dörtte biri teste ayrılır
- Test verisi eğitime bir kez bile karışırsa ölçüm bozulur; buna **sızıntı** denir

-----

## Ezber tuzağı: aşırı öğrenme

- Bir öğrenci soruların cevabını ezberler ama konuyu anlamaz: soru biraz değişince bilemez
- Model de eğitim örneklerini fazla ezberleyebilir; buna **aşırı öğrenme** denir
- Eğitim verisinde mükemmel, yeni örneklerde kötü sonuç verir
- Tersi de olur: model fazla kaba kalır, en belirgin deseni bile yakalayamaz
- İyi model ikisinin arasında: örneklerden genel bir kural çıkarır, yeni örneğe uygular
- Test verisi tam olarak bunu ölçer: model **görmediği** örneklerde ne kadar iyi?

-----

## En yakın komşular: bana arkadaşını söyle

- Bugünkü modelin fikri bir atasözü kadar basit: "bana arkadaşını söyle, sana kim olduğunu söyleyeyim"
- Yeni bir renk gelince model eğitim verisindeki **en benzer** renklere bakar
- Bu komşuların çoğunluğu hangi etiketi verdiyse onu söyler
- Kaç komşuya bakılacağı (**k**) bizim kararımız: 1 komşu çok oynak, çok fazla komşu çok genel
- Model aslında hiçbir "kural" yazmaz; bütün eğitim verisini hatırlar ve her soruda yeniden bakar
- Emlakçının bir evin fiyatını çevredeki benzer evlerin fiyatına bakarak tahmin etmesi de aynı mantık

-----

## Model ne kadar iyi? Doğruluk

- **Doğruluk:** test örneklerinin yüzde kaçını doğru bildiği; 0 ile 1 arası bir oran
- 100 test örneğinden 80'ini bildiyse doğruluk 0.80
- Tek başına bir doğruluk sayısı az şey söyler: 0.80 iyi mi, kötü mü?
- Cevap, neyle kıyasladığına bağlı; bunun için iki referans noktası kullanacağız: alt sınır ve üst sınır

-----

## Alt sınır: kör tahmin

- **Kör tahmin:** hiç düşünmeden hep en sık etiketi söylemek
- Verinin yarısı "enerjik" ise, her renge "enerjik" diyen tembel bir model bile 0.50 doğruluk alır
- Bir model kör tahmini geçemiyorsa hiçbir şey öğrenmemiş demektir
- Bu yüzden her doğruluk sayısını önce kör tahminle karşılaştırırız
- Gerçek hayatta da geçerli: nadir görülen bir durumu yakalayan bir sistem, "hep yok" diyerek bile yüksek doğruluk alabilir; doğruluk tek başına yanıltabilir

-----

## Üst sınır: insanlar anlaşamıyorsa tavan

- Model bir renge **tek** cevap verir; en iyi ihtimalle sınıfın çoğunluğunu söyler
- Bir renge 12 öğrenciden 8'i "enerjik", 4'ü "sakin" dediyse model en fazla 8'ini bilebilir
- Azınlıktaki öğrencileri **hiçbir model** bilemez; onların görüşü verinin içinde ama tek cevaba sığmaz
- Kusursuz bir modelin bile ulaşabileceği en yüksek doğruluğa **tavan** diyoruz
- Tavana yakın bir model, verinin izin verdiği kadarını öğrenmiş demektir
- Öznel işlerde düşük doğruluk her zaman kötü model demek değildir; bazen insanların anlaşamadığı demektir

-----

## Daha çok veri her zaman işe yarar mı?

- Makine öğrenmesinde sık duyulan cümle: "daha çok veri, daha iyi model"
- Ama veri toplamak ve etiketlemek pahalıdır; ne kadarının yeteceğini bilmek gerekir
- Aynı türden veri eklemek ile **yeni türden** veri eklemek aynı şey değildir
- 20 rengi 100 kişiye etiketletmek mi, 100 rengi 20 kişiye etiketletmek mi daha çok şey öğretir?
- Bugün eğitim örneği sayısını adım adım artırıp doğruluğun ne yaptığını izleyeceğiz

**Tahmin et, sohbete yaz:** eğitim örneği arttıkça doğruluk hep artar mı?

-----

## Hiç görmediği örnek: genelleme

- Bir modelin asıl sınavı, hiç görmediği türden bir örnekle karşılaşmasıdır
- Eğitimde gördüğü renklerin başka öğrencilerden gelen etiketlerini tahmin etmek kolay bir sınavdır
- Eğitimde **hiç bulunmayan** bir rengi tahmin etmek zor bir sınavdır
- Modelin yeni durumlara doğru cevap verebilmesine **genelleme** denir
- Bir sonucu söylerken sorulan soruyu da söyle: model bilinen örneklerde mi sınandı, yenilerinde mi?
- Bir şirketin "modelimiz %95 doğru" demesi, hangi verilerle sınandığını söylemezse eksik bilgidir

**Tahmin et, sohbete yaz:** bir rengi hiç görmemiş model ona ne der?

-----

## Model çoğunluğun sesidir

- Model, etiketlerdeki çoğunluğu öğrenir; azınlığın algısını siler
- Hedef kitlen o azınlıksa model sana yanlış yol gösterir
- Gerçek dünyada bu ciddi sonuçlar doğurur: yüz tanıma sistemlerinin koyu tenli kadınlarda çok daha sık yanıldığı araştırmalarla gösterildi
- Sebep çoğunlukla veri: eğitim verisinde bazı gruplar az temsil ediliyordu
- Buna **yanlılık** (bias) denir; model kendi başına önyargılı değildir, verinin önyargısını öğrenir
- Tasarımcı için soru: bu modelin verisinde kimin sesi var, kimin sesi yok?

-----

## Benzerlik, temsile bağlı

- Model "benzer" kavramını rengi hangi sayılarla verdiğimizden alır; buna **temsil** denir
- RGB'de sayıları yakın iki renk, gözümüze hiç benzemeyebilir
- Tersi de olur: gözümüze çok benzeyen iki renk RGB'de uzak düşebilir
- Bu yüzden tasarım programlarında RGB dışında renk sistemleri de var: HSB, Lab
- Aynı model, farklı temsille farklı sonuçlar verir
- Konu 4'ün sorusu: kelimeleri sayıya çevirirsek, sayılardaki yakınlık bizim "benzer anlam" dediğimiz şeyi yakalar mı?

-----

## Bu konunun ödevi

Dersteki defterde eğitim örneği sayısını artırdığımız adımın çıktısına bak: **yarısıyla** ve **tamamıyla** eğitilen modeli karşılaştır.

1. İki doğruluk oranını yaz
2. Öğrenme eğrisini `veri-miktari.png` olarak kaydet
3. Tek cümle: fark ne, neden böyle olmuş olabilir?

Puan yok; Konu 4'ün başında birkaç kişi ekranını paylaşıp gösterecek.

-----

## Hatırlanacaklar

- **Makine öğrenmesi:** kuralı insan yazmaz, model örneklerden çıkarır
- **Öznitelik ve etiket:** modelin baktığı şey X, tahmin etmesi gereken şey y; aynı sırada olmalı
- **Eğitim ve test:** model test verisini hiç görmez; görürse ölçtüğün şey ezber olur
- **Doğruluğu kıyasla:** alt sınır kör tahmin, üst sınır insanların anlaşabildiği kadarı (tavan)
- **Model çoğunluğun sesidir:** verinin dışında kalanı bilemez, verideki önyargıyı öğrenir

Sıradaki konu: renklerin yerine kelimeleri sayıya çevireceğiz; "en yakın komşu" fikri orada da var.
