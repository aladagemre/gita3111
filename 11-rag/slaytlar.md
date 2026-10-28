# Konu 11 — RAG: Belgeye Dayalı Cevap

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 10'dan Konu 11'e: modelin bilmediği şey

- Konu 10'da bir hat kurduk: brif girer, sloganlar ve görseller çıkar; brifi sen yazdın
- Gerçek bir müşteri işinde brif tek başına yetmez: markanın kuralları da vardır
- Renkler, yazı tipleri, yasak sözcükler, logonun nasıl kullanılacağı: hepsi bir belgede yazılıdır, **marka kılavuzunda**
- Dil modeli bu belgeyi hiç görmedi; senin müşterin, senin markan onun eğitim verisinde yok
- Konu 2'de soruya **bağlamı**, yani arka plan bilgisini, elle yazdık; bir kılavuzun tamamını her soruya elle yazamayız
- Bugünkü soru: modele **senin** belgeni nasıl okuturuz?

-----

## Model neyi bilir, neyi bilemez?

- Model eğitildiği metinlerden öğrendi: internette sık geçen şeyleri iyi bilir (Bauhaus, Helvetica, altın oran)
- Az geçen şeyleri zayıf bilir: küçük bir markanın geçmişi, bir şehirdeki yerel bir etkinlik
- Hiç geçmeyenleri hiç bilmez: müşterinin geçen hafta onayladığı kılavuz, ajansın brif arşivi, dünkü toplantı notu
- Eğitimin bir bitiş tarihi var; o tarihten sonra olan hiçbir şey modelde yok
- Bilmediğini çoğu zaman söylemez; boşluğu en olası görünen cümleyle doldurur
- **Yanılgı:** "model internete bakıyor." Bazı sohbet uygulamaları arama yapar; bizim koddan çağırdığımız model ise yalnızca eğitimde öğrendiklerini ve kendisine gönderilen metni bilir

-----

## Uydurma: kendinden emin ama yanlış

- Modelin doğru olmayan bir bilgiyi akıcı ve kendinden emin bir dille yazmasına **uydurma** (halüsinasyon) denir (Konu 5)
- Örnek: bir müzenin açılış saatlerini sorarsın; model makul görünen ama yanlış saatler yazabilir
- Cevap mantıklı göründüğü için tehlikelidir: yanlış olduğu ilk bakışta anlaşılmaz
- Tasarımda bedeli somuttur: yanlış renk kodu baskıya gider, yasak bir sözcük afişe girer, logo yanlış kullanılır
- Uydurma bir arıza değil, modelin çalışma biçiminin sonucu: doğruyu değil, olası olanı seçer
- Çözüm modeli "daha akıllı" yapmak değil; doğru bilgiyi soruyla birlikte ona vermek

-----

## Kitaba bakarak cevap veren öğrenci

- İki öğrenci düşün: biri sınava ezberden girer, öbürü açık kitap sınavına
- Ezberden giren, bilmediği soruda tahmin yürütür; bazen tutturur, bazen uydurur
- Açık kitapla giren önce kitapta ilgili sayfayı bulur, sonra cevabı o sayfaya bakarak yazar
- İyi bir açık kitap öğrencisi, kitapta olmayan bir soruya "kitapta yok" der
- Bugünkü yöntem modeli ikinci öğrenciye çevirir: soruyla birlikte kitabın ilgili sayfalarını da veririz
- Dikkat: öğrenci ancak doğru sayfayı açarsa doğru cevap verir; yanlış sayfayı açan en iyi öğrenci de yanılır

-----

## RAG nedir?

- **RAG**, İngilizce *retrieval-augmented generation*: Türkçesiyle "bulup getirerek üretmek"
- Fikir basit: modele soru sormadan önce belgeden soruyla ilgili parçaları bul, soruyla birlikte gönder; bağlamı sen yazmazsın, belgeden gelir
- Model yeniden eğitilmez; belge değişince modele değil, belgeye dokunursun
- Model cevabı kendi hafızasından değil, önüne konan metinden kurar
- Belge senin elinde kalır: hangi parçanın modele gittiğini görebilir, denetleyebilirsin
- RAG bir model değil, bir **yöntem**: Konu 4'teki gömme vektörlerini ve Konu 5'teki metin modelini birlikte kullanır

-----

## RAG'in üç adımı

- **1. Parçala ve vektöre çevir:** belgeyi kısa parçalara böl (paragraf, madde); her parçayı gömme vektörüne çevir (Konu 4)
- **2. Bul:** sorunun vektörünü al; ona en yakın parçaları seç (Konu 4'teki benzerlik)
- **3. Yönergeye koy ve sor:** "yalnızca şu bilgilere dayanarak cevap ver" + bulunan parçalar + soru → metin modeli
- Birinci adım belge başına bir kez yapılır ve saklanır; ikinci ve üçüncü adım her soruda tekrarlanır
- Kütüphane benzetmesi: kitapları rafa dizmek bir kez yapılır; her okur geldiğinde raftan doğru kitaplar çekilir; okur onları okuyup cevaplar
- Üç adımın üçü de tanıdık iş: bir dosyayı bölmek, sayıları karşılaştırmak, metinleri birleştirmek

-----

## Parçalamak: belgenin nasıl bölündüğü önemli

- Parça çok büyükse (bütün bir sayfa) soruyla ilgisiz bilgi de gelir; model asıl kuralı kalabalıkta kaçırabilir
- Parça çok küçükse (tek cümle) kural ile gerekçesi ayrılır: "kırmızı kullanılmaz" gelir, "neden" gelmez
- İyi bir parça tek bir konuyu kendi başına anlatır: bir kural, bir paragraf
- İyi yazılmış bir marka kılavuzu bu yüzden RAG'e zaten elverişlidir: her bölüm bir konu
- Bir konu birkaç bölüme dağılmışsa (renk kuralları hem genel bölümde hem ürün bölümlerinde) hepsini birden bulmak zorlaşır
- Tasarımcı için ders: belge yazarken de sor: "bu paragraf tek başına okununca anlaşılır mı?"
- **Ad karışmasın:** Konu 5'teki parça bir belirteçti, kelimenin bir kırıntısı; RAG'deki parça belgenin bir bölümüdür

-----

## Bulmak: anlamca en yakın parçalar

- Bulma adımı soruya **anlamca** en yakın parçaları seçer; kelimesi kelimesine eşleşme gerekmez (Konu 4)
- "Logonun etrafında ne kadar boşluk kalmalı?" sorusu, içinde "çevresinde" yazan paragrafı da bulabilir
- Konu 4'ü hatırla: model "benzer" derken "benzer yerlerde geçen"i kasteder; bu her zaman "aynı şeyi söyleyen" değildir
- Kaç parça alınacağına sen karar verirsin: az alırsan gerekli bir kural dışarıda kalabilir, çok alırsan yönerge kalabalıklaşır
- Kural: model yalnızca kendisine gönderilen parçaları bilir; gönderilmeyen parça onun için yoktur
- Bu yüzden RAG'de cevap, bulma adımından daha iyi olamaz

-----

## Yönerge: talimat, bilgiler, soru

- Modele giden metin üç kısımdan oluşur: **talimat + bulunan parçalar + soru**
- Talimat sınırı çizer: "yalnızca aşağıdaki bilgilere dayanarak cevap ver"
- Ve bir çıkış kapısı gösterir: "bilgilerde cevap yoksa bilmiyorum de"; bu kapı yoksa model boşluğu yine kendisi doldurur
- Parçaları "Bilgiler:" gibi bir başlıkla sorudan ayırmak, modelin neyin kaynak neyin soru olduğunu görmesini kolaylaştırır
- Talimat da modelin devamını yazdığı metne dahildir (Konu 5): bir kural değil, bir yönlendirme; model çoğu zaman uyar, her zaman değil
- Şablon bir kez yazılır, her soruda yeniden kullanılır: Konu 10'daki yönerge kalıbı gibi

-----

## Tasarımda nerede işe yarar?

- **Marka kılavuzu:** "Bu afişte hangi renkler olmalı?", "Logoyu fotoğrafın üstüne koyabilir miyim?"
- **Brif arşivi:** ajansın geçmiş brifleri; "bu müşteri daha önce hangi tonu reddetmişti?"
- **Stil rehberi:** bir derginin ya da yayınevinin yazım ve dizgi kuralları; "başlıkta tarih nasıl yazılır?"
- **Ürün bilgisi:** ambalaj metni yazarken ürünün gerçek içeriği ve uyarıları
- **Kendi notların:** moodboard açıklamaları, müşteri toplantısı notları, araştırma özetleri
- Ortak nokta: bilgi bir belgede yazılı, model onu bilmiyor ve yanlış bilgi pahalıya patlıyor

**Sohbete yaz:** sen hangi belgeyi bir modele okutmak isterdin? Ondan ne sorardın?

-----

## Belgeden görsele: kılavuza uygun bir yönerge

- Görsel model kılavuzu okumaz; ona yalnızca bir yönerge gider (Konu 7)
- Bu yüzden zincir iki halkalı: önce kılavuzdan görselle ilgili kurallar bulunur, sonra metin modeli bu kurallarla bir görsel yönergesi yazar
- Ne aradığın, ne bulacağını belirler: afişin konusunu aramak bir şey, görselin kurallarını aramak başka bir şey getirir
- Bir kural üç yerde kaybolabilir: **aramada** (kural metin modeline hiç gitmedi), **yönergede** (metin modeli kuralı görsel yönergesine koymadı) ya da **çizimde** (kural yönergede vardı ama görsel model uygulamadı)
- Hangisinin olduğunu ara çıktılara bakarak bulursun: bulunan parçalar ve yazılan yönerge (Konu 10)
- Kılavuza uygunluğu son kez denetleyen yine tasarımcıdır: model taslak üretir, onay senin

-----

## Neden bütün belgeyi göndermiyoruz?

- Küçük bir belge her soruda bütünüyle gönderilebilir; o zaman bulma adımına gerek kalmaz
- Gerçek belgeler ise büyüktür: iki yüz sayfalık bir kurumsal kimlik kılavuzu, yüzlerce brif
- Modelin bir seferde okuyabileceği metnin bir sınırı var: Konu 5'teki **bağlam penceresi**; pencereye sığmayan kısım hiç okunmaz
- Gönderilen her metin kotadan yer: uzun yönerge, pahalı istek
- Uzun bir metnin ortasındaki küçük bir kural kalabalıkta kaybolabilir; kısa ve ilgili parçalar daha net cevap getirir
- RAG bu yüzden "her şeyi ver" değil, "gerekeni ver" yaklaşımıdır

-----

## RAG'in sınırları

- Uydurmayı azaltır, sıfırlamaz: model talimata rağmen bilgilerde olmayan bir şey ekleyebilir
- Bulma yanılırsa cevap da yanılır: yanlış parça gelirse model onu doğru sanıp kullanır
- Belge yanlışsa ya da eskimişse cevap da öyle olur; RAG belgenin doğruluğunu denetlemez
- Belge değişince vektörler yeniden hesaplanmalı; yoksa arama eski belgede yapılır
- Gönderdiğin parçalar modelin sunucusuna gider: gizli bir müşteri belgesini göndermeden önce izin gerekir
- **Yanılgı:** "RAG kullandım, cevap kesin doğru." Cevaptaki her önemli bilgiyi kaynağıyla karşılaştırmak hâlâ senin işin

-----

## Bu konunun ödevi

**Kendi kılavuzun, kendi RAG'in.**

1. Kendi markan ya da final projen için kısa bir kılavuz yaz: 8–12 paragraf, her paragraf tek bir kural
2. Ders defterinin kopyasıyla kılavuzunu parçala, vektöre çevir, sakla
3. Üç soru sor: kılavuzda cevabı olan, cevabı yarım olan, cevabı hiç olmayan
4. Kılavuzuna uygun bir görsel yönergesi yazdırıp bir görsel üret
5. **Üç cümle:** model nerede kılavuza uydu, nerede uydurdu? Kılavuzunda neyi değiştirirdin?

Ayrıntılar: `odevler/odev11.md`. Puan yok; Konu 12'nin başında sıradaki arkadaşlar gösterecek.

-----

## Hatırlanacaklar

1. **Model senin belgeni bilmez;** bilmediği yerde uydurur
2. **RAG'in üç adımı:** parçala ve vektöre çevir → soruya en yakın parçaları bul → talimatla birlikte yönergeye koy ve sor
3. **Cevap, bulmadan daha iyi olamaz:** modele gitmeyen parçayı model bilemez
4. **Talimat "bilmiyorum" kapısını açar;** ama o kapıdan geçip geçmemek modelin elinde
5. **Belge değişince vektörler de yenilenir;** son kontrol her zaman tasarımcıda

Sıradaki konu: **Konu 12 — Ajan.** Bugün kılavuza ne zaman bakılacağına sen karar verdin. Konu 12'de kılavuzda aramak bir araç olacak; ne zaman bakılacağına model karar verecek.
