# Konu 6 — Üretmek Ne Demek?

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 5'ten Konu 6'ya: kaputun son parçası

- **Konu 3'te** bir modelin örneklerden nasıl öğrendiğini gördük
- **Konu 4'te** her şeyin sayıya çevrilebildiğini ve sayılarla bir **harita** çizilebildiğini gördük
- **Konu 5'te** dil modelinin metni olasılıklardan seçerek ürettiğini gördük
- **Bugün:** bir model hiç görmediği bir görseli nasıl "üretir"?
- Bu, birinci yarının son ve en önemli kavramı; Konu 7'den itibaren görsel üreticileri kullanırken hep bunu hatırlayacağız
- Cevabı tanıdık bir malzemeyle arayacağız: harflerle

-----

## "Üretmek" ne olabilir?

- Model bir görseli bir yerden kopyalayıp yapıştırmıyor; eğitim verisinde o görsel yok
- Rastgele pikseller de üretmiyor; rastgele pikseller yalnızca gürültü olurdu
- Ortada bir yerde: gördüğü binlerce örnekten bir **düzen** öğreniyor ve o düzene uyan yeni bir şey kuruyor
- Bir tasarımcı da böyle çalışır: yüzlerce font görmüş biri, hiç var olmayan bir A'yı kâğıda çizebilir
- Soru şu: bu "düzen" bilgisayarda nasıl tutuluyor ve ondan yeni bir şey nasıl çıkıyor?

**Sohbete yaz:** hiç görmediğin bir şeyi çizmen istense nereden başlarsın?

-----

## Bilgisayar için resim bir sayı tablosudur

- Her resim küçük karelerden oluşur: **piksel**
- Siyah-beyaz bir resimde her piksel bir sayı: o karenin ne kadar koyu olduğu
- Renkli resimde her piksel üç sayı: Konu 3'teki kırmızı, yeşil, mavi
- Küçük bir harf bile yüzlerce sayı
- Telefonunla çektiğin bir fotoğraf ise on milyonlarca sayı
- Konu 4'teki gibi: bilgisayar harfi görmez, sayıları görür; harfin ne olduğu sayıların düzeninde saklı

-----

## Sıkıştırmak: daha az sayıyla anlatmak

- Bir resmi daha az sayıyla anlatmaya **sıkıştırma** denir
- Günlük hayattan: JPEG fotoğraflar, telefonda gönderdiğin videolar, galerideki küçük önizleme resimleri
- Bir eskiz de sıkıştırmadır: birkaç çizgiyle bir yüzü anlatırsın, her gözeneği değil
- Sıkıştırma **seçmektir**: neyin önemli olduğuna karar verip gerisini atarsın
- Çok sıkıştırırsan bilgi kaybolur: JPEG'in kalite ayarını düşürünce resim bulanıklaşır
- İyi sıkıştırma, en az sayıyla en çok şeyi anlatandır

-----

## Sıkıştır ve geri kur

- Sıkıştırmanın işe yaraması için geri kurabilmen gerekir
- **Kodlayıcı:** resmi küçük bir **koda** sıkıştırır; yüzlerce sayıyı birkaç sayıya
- Buradaki "kod" Python kodu değil: resmin kısa özeti
- **Çözücü:** o koddan resmi geri kurar; birkaç sayıyı yeniden yüzlerce sayıya
- İkisini birlikte öğrenen modele **otokodlayıcı** (autoencoder) denir
- Kodu küçültmenin bir bedeli var: bir şeyler kaybolur
- Çözücü eksik bilgiyi **öğrendiklerinden** doldurmaya çalışır
- Asıl soru: kod çok küçülürse çözücü elindekinden ne kurabilir?

-----

## Konu 4'teki gölgeyi hatırla

- Konu 4'te PCA ile yüzlerce sayıyı 2 sayıya indirdik: heykelin duvara düşen gölgesi
- Bu bir kodlayıcıydı: her kelimeyi 2 sayılık bir koda sıkıştırdı
- Bugün bir adım daha atıyoruz: **gölgeden heykele geri dönüyoruz**
- PCA'nın iki yönü var: sıkıştırırken kodlayıcı, geri kurarken çözücü; bu yüzden en basit otokodlayıcı
- Görsel üreten büyük modellerin otokodlayıcıları çok daha güçlü, ama fikir aynı

**Tahmin et, sohbete yaz:** yalnızca 2 sayıdan geri kurulan bir A okunur mu, yoksa bir leke mi olur?

-----

## Gizli uzay: kodların haritası

- Her A 2 sayılık bir koda sıkışınca, her A bir **nokta** olur; bütün noktalar bir **harita**
- Bu haritaya **gizli uzay** (latent space) denir; "gizli" çünkü eksenlerinin adı yok
- Konu 4'teki gibi: eksenleri biz seçmiyoruz, model verideki en büyük farklardan kendisi buluyor
- Haritada pikselleri birbirine benzeyen A'lar yakın, çok farklı olanlar uzak düşer
- Bir tasarımcının stil panosu gibi: benzer işler bir köşede, zıt işler öbür köşede
- Gerçek modellerde harita 2 değil binlerce boyutlu; ama mantık aynı

**Tahmin et, sohbete yaz:** A'ların haritası serifli fontları bir köşeye, serifsizleri başka köşeye toplar mı?

-----

## Üretmek: haritada bir nokta seçmek

- Haritada **hiçbir A'nın durmadığı** boş bir nokta seç
- O noktanın 2 sayısını çözücüye ver; çözücü bir A kurar
- Bu A eğitim verisindeki hiçbir fontta yok: **yeni**
- İşte üretmenin özü: öğrenilmiş bir haritada bir nokta seçip oradan geri kurmak
- Görsel üreticiler de bunu yapar: yazdığın yönerge (prompt) haritada bir yer tarif eder, model oradan bir görsel kurar
- Tarif edilen yer tek bir nokta değil, bir **bölgedir**; bölgenin neresinden yola çıkılacağını rastgele bir başlangıç belirler (Konu 7: tohum)

-----

## Haritanın kenarları: verinin bittiği yer

- Haritanın içi, modelin gördüğü örneklerle dolu; oradan gelen sonuçlar inandırıcı
- Haritanın dışı boş: model oranın neye benzediğini hiç görmedi
- Oradan bir nokta seçersen çözücü yine bir şey kurar, ama tuhaf, bozuk, dağınık bir şey
- Görsel üreticilerdeki altı parmaklı eller, okunmayan yazılar, eriyen nesneler kısmen bundan
- Kural: model, verisinin çok olduğu yerde iyi, az olduğu yerde kötü üretir
- Konu 3'teki ders burada da geçerli: model verinin aynasıdır

-----

## Eksenler ne anlatıyor?

- Model haritanın eksenlerine ad vermez; yalnızca verideki en büyük farkları bulur
- Ama haritayı adım adım tarayıp her noktadan bir A kurarsan, eksenin ne anlattığını **görebilirsin**
- Bir eksen boyunca yürüyünce harfte hep aynı şey değişiyorsa, o eksen bir **özellik düğmesi** gibidir
- Tasarımcı için bu çok tanıdık bir araç: bir özelliği bir sürgüyle ayarlamak
- Fark: değişken fontta eksenleri tasarımcı belirler; burada model veriden kendisi bulur

**Tahmin et, sohbete yaz:** yüzlerce fontun A'ları en çok hangi bakımdan birbirinden farklıdır? Haritanın iki ekseni ne olabilir?

-----

## Ara değerleme: iki nokta arasında yürümek

- Haritada iki nokta seç: biri serifli bir A, öbürü serifsiz bir A
- Aralarındaki düz çizgi üzerinde adım adım yürü; her adımda çözücüye sor
- Ortada iki fontun **ara formları** çıkar; hiçbiri gerçek bir font değil
- Buna **ara değerleme** (interpolation) denir
- Tipografide tanıdık: **değişken fontlar** bir özelliği sürgüyle ayarlatır; sürgü iki uç tasarım arasında ara değerleme yapar
- Görsel üreticilerde aynı fikirle iki yüz, iki ürün, iki üslup arasında yumuşak geçişler yapılır

-----

## Büyük modeller bunu nasıl yapıyor?

- **Veri:** bizde yüz küsur A; görsel üreticide yüz milyonlarca görsel ve açıklamaları
- **Kod:** bizde 2 sayı; görsel üreticide binlerce sayı
- **Sıkıştırıcı:** bizde PCA, düz çizgilerle sıkıştırır; büyük modellerde çok katmanlı sinir ağları, eğri yollarla sıkıştırır
- **Noktayı seçen:** bizde biz; görsel üreticide yazdığın yönerge
- **Yol:** model rastgele bir başlangıç noktasından (gürültüden) başlar ve yönergeye uyan bölgeye adım adım yaklaşır; bunu Konu 7'de konuşacağız
- Ölçek değişiyor, fikir değişmiyor

-----

## Üretilen şey kimin?

- Haritayı model çizdi, ama haritanın malzemesi binlerce tasarımcının işi
- Bugün üreteceğimiz A'lar, onlarca fontu tasarlayan insanların emeğinden çıkan bir haritadan geliyor
- Görsel üreticiler internetteki milyonlarca görselden öğrendi; çoğunun sahibine sorulmadı
- Haritada bir sanatçının işlerinin yoğun olduğu bölgeye gidersen, onun üslubuna çok benzeyen şeyler çıkar
- Bu yüzden "yaşayan bir sanatçının tarzında" istemek tartışmalı
- Konu 7'de bu soruyu etik ve telif açısından konuşacağız

-----

## Bu konunun ödevi

**1. Kendi harfinin haritası.** Dersteki defteri kopyala; A yerine g, a ya da R ile haritayı, iki eksen boyunca yürüyüşü ve iki font arasındaki yürüyüşü çıkar. İki cümle: yürürken harfte ne değişiyor, harita neyi "en önemli fark" diye seçmiş?

**2. En garip A.** Haritada farklı noktalar deneyerek en garip A'yı bul. Noktasını ve neden garip olduğunu iki cümleyle yaz.

- Ayrıntılar: `odevler/odev6.md`
- Puan yok; Konu 7'nin ilk oturumu vizenin sözlü teyidine ayrıldığı için Konu 8'in başında gösterilecek

-----

## Vize

- Bu konu bitince vize veriliyor: **evde** yapılır, **yapay zeka yasak**
- Kapsam: Konu 1–6
- Soru biçimleri alıştırma defterlerindekiyle aynı: kavram soruları, kod okuma, bozuk kodu düzeltme, boşluk doldurma
- Teslim tarihi ve yolu derste duyurulacak
- Teslimden sonra Konu 7'nin ilk oturumunda kısa bir **sözlü teyit**: kendi kodunu açıklayacaksın
- Hazırlık için: her konunun alıştırma defterini baştan, kendi başına yeniden çöz
- Takıldığın konunun ders notundaki "Kendini dene" sorularına bak

-----

## Hatırlanacak dört şey

1. **Resim bir sayı tablosudur.** Her piksel bir sayı; harf de, fotoğraf da
2. **Sıkıştır ve geri kur.** Kodlayıcı küçük bir koda indirir, çözücü öğrendiklerinden geri kurar; kod küçüldükçe bilgi kaybolur
3. **Gizli uzay bir haritadır.** Eksenlerin adı yok ama anlamı var; model onları veriden kendisi bulur
4. **Üretmek, haritada bir nokta seçmektir.** Verinin çok olduğu yerde inandırıcı, olmadığı yerde bozuk sonuç çıkar

Sıradaki konu: **Konu 7 — Görsel üretimi.** Noktayı artık yönerge seçecek.
