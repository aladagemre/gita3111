# Konu 4 — Temsil ve Gömme Vektörleri

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 3'te bir renk üç sayıydı; bugün bir kelime yüzlerce sayı olacak

- Konu 3'te model renkleri üç sayıyla (R, G, B) tanıdı ve benzer renkleri bu sayılardan buldu
- Ama sayılarda yakın iki renk gözümüzde uzak olabiliyordu: benzerlik, temsile bağlı
- Bugünün sorusu: bir kelimeyi nasıl sayıya çeviririz ki benzer anlamlı kelimeler birbirine yakın düşsün?
- Bu, dil modellerinin, arama motorlarının ve öneri sistemlerinin temelindeki fikir
- Bugün bir modelden kelimelerin sayılarını alacak, kelimeler arasındaki yakınlığı ölçeceğiz

-----

## Bilgisayar her şeyi sayıya çevirerek temsil eder

- **Renk:** 3 sayı (kırmızı, yeşil, mavi)
- **Fotoğraf:** her piksel için 3 sayı; bir telefon fotoğrafı milyonlarca sayı
- **Ses:** her saniye için binlerce sayı, hoparlör zarının ne kadar ileri geri gideceği
- **Kelime:** ?
- Kelimeye harflerinin sırasına göre sayı vermek işe yaramaz: "kahve" ile "kahin" harfçe yakın, anlamca uzak
- Aradığımız şey, **anlamı** taşıyan sayılar

**Sohbete yaz:** bir kelimeyi sayıya çevirmen gerekse nasıl yapardın?

-----

## Önce elle: iki eksenli bir mood-board

- Tasarımcıların bildiği bir yöntem: kelimeleri iki eksenli bir panoya yerleştirmek
- Yatay eksen **sıcaklık:** soğuk −1 … sıcak +1
- Dikey eksen **enerji:** sakin −1 … canlı +1
- "Ateş" sağ üste düşer: sıcak ve canlı; "buz" sol alta: soğuk ve sakin
- Böylece her kelime **iki sayı** olur; böyle bir sayı listesine **vektör** diyoruz
- Eksenleri biz seçtik; başka biri "lüks–gündelik" ekseni seçseydi bambaşka bir harita çıkardı: temsil bir **seçimdir**

**Sohbete yaz:** sen "kahve"ye hangi iki sayıyı verirdin?

-----

## Her vektör ortadan çıkan bir ok

- İki sayılık bir vektörü haritada bir nokta olarak da, merkezden o noktaya çizilen bir **ok** olarak da düşünebilirsin
- Okun **yönü** kelimenin karakterini söyler: sağ üst sıcak ve canlı, sol alt soğuk ve sakin
- Okun **uzunluğu** o karakterin ne kadar güçlü olduğunu söyler
- "Ilık" ile "kızgın" aynı yöne bakar; biri kısa, biri uzun
- Zıt anlamlı iki kelime tam ters yönlere bakar
- Kelimeler arasındaki benzerliği ölçmek için okları karşılaştıracağız

-----

## Benzerlik okların yönüne bakar, uzunluğuna değil

- İki ok **aynı yöne** bakıyorsa benzerlik **1**'e yakın
- Birbirine **dik** bakıyorsa benzerlik **0**: ilgisizler
- **Tam ters** yöne bakıyorsa benzerlik **−1**: zıtlar
- Okun uzunluğu sayılmaz: "ılık" ile "kızgın" aynı yöne baktığı için çok benzer çıkar
- Bu ölçünün adı **kosinüs benzerliği**; hesabını hazır bir araç yapıyor
- Neden uzunluk değil? Uzun bir metin, kısa bir metinle aynı konudan bahsediyorsa yine benzer saymak isteriz

**Tahmin et, sohbete yaz:** "kahve" ve "çay" mı daha benzer çıkar, "kahve" ve "buz" mu? Hangisi eksi çıkar?

-----

## Eksenleri model kendisi buluyor

- Mood-board'da iki ekseni biz seçtik ve adlarını biz koyduk
- Bir **gömme modeli** çok büyük miktarda metin okur ve kelimeleri bir haritaya kendisi yerleştirir
- Eksen sayısı 2 değil, **yüzlerce**, hatta binlerce
- Eksenlerin hiçbirinin adı yok; "bu eksen sıcaklık" diyemezsin
- Sayıların tek tek anlamı yok; anlam, kelimelerin birbirine göre nerede durduğunda
- Kelimeyi böyle bir vektöre çevirmeye **gömme** (embedding) diyoruz: kelimeyi anlam haritasına gömüyoruz

-----

## Model anlamı nereden öğreniyor?

- Bir dilbilimcinin 1950'lerden kalma sözü: "Bir kelimeyi, yanında durduğu kelimelerden tanırsın"
- "Kahve" metinlerde "fincan", "sabah", "içmek", "kafe" kelimeleriyle birlikte geçer
- "Çay" da aynı kelimelerle geçer; bu yüzden ikisinin vektörü birbirine yakın düşer
- Model hiçbir sözlük okumaz; yalnızca hangi kelimenin hangi kelimelerle birlikte geçtiğine bakar
- Bunu milyonlarca cümlede yapınca, benzer bağlamlarda geçen kelimeler haritada yan yana düşer
- Ünlü bir örnek: "kral" − "erkek" + "kadın" hesabının sonucu "kraliçe"ye çok yakın çıkar

-----

## Benzer, eşanlamlı demek değil

- Model "benzer"i "benzer cümlelerde geçen" diye öğrenir
- "Sıcak" ve "soğuk" aynı cümlelerde geçer: "hava bugün ... ", "... bir içecek"
- Bu yüzden zıt anlamlı kelimeler de haritada birbirine yakın düşebilir
- Mood-board için "huzur"a yakın kelimeler istersen listeye beklemediğin kelimeler girebilir
- Sonucu körü körüne kullanma; listeye bir tasarımcı gözüyle bak

-----

## En yakın komşular

- Bir kelimeye haritada en yakın duran kelimelere **komşu** diyoruz; Konu 3'teki "en yakın komşu" fikrinin aynısı
- Yöntem: hedef kelimeyi listedeki her kelimeyle karşılaştır, her biri için bir benzerlik skoru yaz
- Skorları büyükten küçüğe sırala; en üstteki birkaç kelime komşulardır
- Konu 1'deki `Counter` kelimeleri saymayı ve sıralamayı biliyordu; ona hazır skorları verirsen saymaz, yalnızca **sıralar**
- Bugün "kafe" kelimesinin komşularını bulacağız: kütüphaneye mi yakın, parka mı, sahneye mi?

**Tahmin et ve not al:** "kafe"ye en yakın üç kelime sence hangileri?

-----

## Gömme vektörleri nerede kullanılıyor?

- **Anlamsal arama:** "rahat koltuk" arayınca içinde "konforlu kanepe" yazan ürünü de bulmak
- **Öneri sistemleri:** Spotify'ın sevdiğin şarkıya benzer şarkılar bulması
- **Görsel arama:** Pinterest'te bir görsele benzeyen görselleri bulmak; görseller de vektöre çevrilebilir
- **Metinle görsel eşleme:** görsel üreten modeller yazdığın cümleyi ve görseli aynı haritada buluşturur
- **Sohbet modelleri:** yazdığın her kelime önce böyle bir vektöre çevrilir
- Ortak fikir: "anlamca yakın" olanı bulmak için sayılardaki yakınlığı kullanmak

-----

## Yüzlerce sayı kâğıda sığmaz: gölgesini çizeriz

- İki sayılık bir vektörü haritaya çizebiliriz; yüzlerce sayılık bir vektörü çizemeyiz
- **PCA** (Temel Bileşen Analizi) çok sayıyı, en çok şey anlatan **2 sayıya** indirir
- Bir heykelin duvara düşen gölgesi gibi: üç boyutlu şeyi iki boyuta indirir
- PCA, heykeli en iyi tanıtan açıyı arar; gölgeden heykelin şeklini olabildiğince anlarsın
- Böylece yüzlerce sayılık kelimeleri iki eksenli bir haritaya yerleştirebiliriz
- Ama yeni eksenlerin de adı yok; haritayı yorumlayan sensin

-----

## Harita bir özettir, bilgi kaybeder

- Yüzlerce sayıyı ikiye indirirken bilginin bir kısmı kaybolur
- Haritada yan yana duran iki kelime gerçekte o kadar yakın olmayabilir
- Gölge benzetmesiyle: önden bakınca üst üste görünen iki şey, yandan bakınca uzak olabilir
- Emin olmak için haritaya değil, asıl sayılara bak: iki kelimenin benzerliğini doğrudan ölç
- Şehir haritası gibi: yolu bulmana yeter, binaların yüksekliğini göstermez
- Haritayı keşif için kullan, kesin hüküm için değil

-----

## Gömmeler de yanlı olabilir

- Model anlamı insanların yazdığı metinlerden öğrenir; metinlerdeki önyargıyı da öğrenir
- Örneğin bazı meslekler kadın, bazıları erkek kelimelerine daha yakın düşebilir
- Bu haritayı kullanan bir arama ya da öneri sistemi aynı önyargıyı tekrar üretir
- Konu 3'teki ders burada da geçerli: model verinin aynasıdır
- Tasarımcı için soru: bu öneriler bir dünya görüşünü mü yansıtıyor, benim kitlemi mi?

-----

## Bu konunun ödevi

Kendi seçtiğin **20 kelimeyle** bir anlam haritası çıkar.

1. Dersteki defteri kopyala, kelime listesine kendi 20 kelimeni yaz
2. Haritayı çizdiğimiz adıma kadar çalıştır, haritayı kaydet
3. **Tek cümle:** beklemediğin hangi iki kelime yan yana düştü?
4. **Tek cümle daha:** bu haritayla bir mood-board'a başlasan neyi ekler, neyi çıkarırdın?

Ayrıntılar: `odevler/odev4.md`. Puan yok; Konu 5'in başında sıradaki arkadaşlar gösterecek.

-----

## Hatırlanacaklar: üç kavram, üç cümle

- **Vektör (gömme):** model bir kelimeyi bir sayı listesine çevirir; sayıların tek tek anlamı yok, anlam kelimelerin birbirine göre nerede durduğunda
- **Benzerlik:** aynı yöne bakan iki vektör benzerdir: 1 aynı yön, 0 ilgisiz, −1 zıt; modelin "benzer"i, "benzer yerlerde geçen" demek
- **Boyut indirgeme:** yüzlerce sayıyı 2'ye indirip haritaya çizebiliriz; ama harita bir özettir, bilgi kaybeder

-----

## Sıradaki konu: dil modelleri nasıl yazıyor?

- Bu konuda model kelimeleri sayıya çevirdi
- Konu 5'te modelin **metni nasıl yazdığına** bakacağız
- Metin önce parçalara bölünür; model her seferinde bir sonraki parçayı tahmin eder
- "Sıcaklık" ayarı, modelin hep en olası parçayı mı seçeceğini yoksa zar mı atacağını belirler
