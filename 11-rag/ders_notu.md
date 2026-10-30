# Konu 11 — Müşterinin söylediklerini unutmayan bir hafıza

Ders notu. Birlikte çalıştırdığımız defter `ders.ipynb`, kendi başına çözdüğün defter `alistirma.ipynb`, ödev
`odevler/odev11.md`.

## Bu konuda ne yapıyoruz?

Serbest çalışan bir tasarımcı müşterisini tek bir yerden dinlemez. İstekler WhatsApp'tan gelir, bir kısmı e-postada
kalır, bir kısmı toplantıda söylenip kimsenin defterine geçmez. Jüride hocalar aynı eleştiriyi iki hafta arayla
tekrar eder. Üç hafta sonra yeni bir afiş yaparken bunların yarısı akılda değildir; müşteri "bunu söylemiştim" der,
bir revizyon turu daha başlar.

Bu konuda Sayfa Kahve (üniversite yakınında sessiz bir çalışma kafesi) için bir **müşteri hafızası** kurduk.
Hafızada iki şey var: müşterinin yazılı marka kılavuzu (`veri/kilavuz.txt`) ve senin topladığın notlar
(`veri/notlar.txt`). Hafızaya bir soru soruyorsun; o da notları anlamına göre arıyor, en yakınlarını buluyor ve
cevabı yalnız o notlara dayanarak yazıyor. Yeni bir not ekleyince hafıza büyüyor, cevap da değişiyor.

Konunun sonunda elinde iki şey var: büyüyen bir not dosyası ve ona soru sormanı sağlayan dört satır kod.

## RAG: açık kitap sınavı

Bu yöntemin adı **RAG** (İngilizce *retrieval-augmented generation*, "bulup getirerek üretmek"). En kolay benzetme
açık kitap sınavı: öğrenci cevabı ezberinden değil, önündeki kitaptan verir. Ama kitabın doğru sayfasını açmak da
onun işidir. RAG'in iki yarısı var:

1. **Bul:** sorunun anlamına en yakın notları bul.
2. **Önüne koy:** bu notları soruyla birlikte modele ver ve "yalnız bunlara dayan" de.

Bir başka benzetme: yeni başlayan bir stajyere müşteriyi sorsan önce müşteri dosyasını açar, ilgili sayfaları bulur,
sonra cevap verir. Model de öyle; tek farkı dosyayı açmayı ona bizim yaptırmamız.

Hangi işi kim yapıyor?

| İş | Kim yapıyor |
|---|---|
| Notları dosyadan okumak, yeni not eklemek | Python |
| Notları ve soruyu vektöre çevirmek | Vektör modeli (Konu 4) |
| Puanları büyükten küçüğe dizmek, en yakınları seçmek | Python |
| Notları ve soruyu tek bir yönergede birleştirmek | Python |
| Notlara bakıp cevabı yazmak | Dil modeli (gemma-4; Konu 10'da afişi okuyan model) |

Yapay zekâ yalnızca iki yerde var: anlamı sayıya çevirmek ve notları okuyup cevap yazmak. Kalan her şeyi sıradan
bir Python betiği yapar.

## Isınma: kelime araması neden yetmez?

Bir dosyada bir şey ararken çoğumuz kelimeyle ararız (Ctrl + F). Soru şu: "Masada oturan bir öğrencinin portresini
çekeyim mi?"

```python
aranan = "portre"
for not_metni in notlar:
    if aranan in not_metni:
        print(not_metni)
```

`"portre"` hiçbir şey bulmaz. `"öğrenci"` bir not bulur ama yanlış notu: hedef kitleyle ilgili olanı. Doğru not
"Fotoğraflarda insan yüzü olmasın" diyor; soruyla anlamı aynı, ama ortak kelimesi yok. Kelime araması iki türlü
yanılır: ortak kelime yoksa doğru notu kaçırır, ortak kelime varsa konusu başka bir notu getirir. Üstelik doğru
kelimeyi ("yüz") tahmin edebiliyorsan notu zaten hatırlıyorsun demektir.

## Adım 1 — Hafızayı vektöre çevir

```python
hafiza = hafizayi_kur(kilavuz + notlar)
print(len(hafiza))
```

`kilavuz + notlar` iki listeyi uç uca ekler: 14 kılavuz kuralı ve 16 not, 30 metin. `hafizayi_kur` (yardımcı
dosyadaki fonksiyon) hepsini **tek istekte** vektör modeline gönderir ve bir sözlük kurar: anahtar metnin kendisi,
değer onun 768 sayılık vektörü. Konu 4'teki `vektorler_sozlugu` ile aynı yapı; tek fark, 30 metnin 30 ayrı istek
yerine tek istekte gitmesi.

## Adım 2 — Soruya en yakın 3 not

```python
soru = "Masada oturan bir öğrencinin portresini çekeyim mi?"
soru_vektoru = vektor_al(soru)

for metin in hafiza:
    vektor = hafiza[metin]
    puan = benzerlik(soru_vektoru, vektor)
    kisa = round(puan, 2)
    print(kisa, metin)
```

Konu 4'teki işin aynısı: sorunun vektörünü alıp hafızadaki her metinle benzerliğini ölçüyoruz. Benzerlik iki vektör
aynı yöne bakıyorsa büyük, ilgisizse küçük çıkar. Bu soruda fotoğrafla ilgili metinler üstte, fatura ve matbaa
notları altta kalır.

30 satırda en büyük üç puanı gözle bulmak yorucu; yardımcıdaki `hafizada_ara` aynı hesabı yapar, puanları büyükten
küçüğe dizer ve ilk `kac` metni bir liste olarak verir.

```python
bulunanlar = hafizada_ara(soru, hafiza, 3)
for metin in bulunanlar:
    print(metin)
```

**İlgisiz not var mı?** Fatura notu tasarım sorularında gelmez, çünkü anlamı başka yöne bakıyor. Ama "Afişi matbaaya
ne zaman göndermeliyim?" diye sorarsan matbaa notu gelir. Hafızada ilgisiz not yoktur; yalnız o soruyla ilgisi
olmayan not vardır.

**Anlamca arama da yanılabilir.** "Surat" ile "yüz" anlamca yakın olduğu için "Gönderiye gülen surat koyabilir
miyim?" sorusunda "insan yüzü" notu emoji notunun önüne geçebilir. Arama ayrıca her zaman `kac` tane metin getirir;
cevabı hiçbir notta olmayan bir soruda da en yakın üçü gelir. Bu yüzden ikinci yarıdaki kural önemli.

## Adım 3 — Notlara dayanarak cevap

Konu 10'daki hattın afişten okuduğu yazıları `veri/afis_metni.txt`'ye yazdık. Önce hafızada afişle ilgili notları
arıyoruz ("Etkinlik afişinin metninde hangi bilgiler olmalı, hangi sözcükler olmamalı?"), sonra bulduklarımızı
soruyla birlikte modelin önüne koyuyoruz.

Arama beş metin getirir. Hepsi afişle ilgili olmayabilir: arama her zaman istediğin sayıda metin getirir, ilgisi
zayıf olsa bile (hocanın denemesinde menü kartlarının kuralı da geldi). Asıl soru şu: "kafe" notu bu beşin içinde mi?

```python
def yonerge_kur(soru, bulunanlar):
    yonerge = "Yalnız aşağıdaki notlara dayan. Notlarda yoksa 'notlarda yok' de.\n"
    yonerge = yonerge + "Kısa maddelerle cevap ver; her maddede dayandığın notu yaz.\n\nNOTLAR:\n"
    for metin in bulunanlar:
        yonerge = yonerge + "- " + metin + "\n"
    yonerge = yonerge + "\nSORU: " + soru
    return yonerge
```

`yonerge_kur` bir metin birleştirir; modele istek göndermez. Üç parçası var:

- **Kural:** "Yalnız aşağıdaki notlara dayan. Notlarda yoksa 'notlarda yok' de." Konu 5'te gördük: model bilmediği
  bir şey sorulunca çoğu zaman "bilmiyorum" demez, olası görünen bir cevap uydurur (halüsinasyon). Kural bu kapıyı
  kapatmaya çalışır; tamamen kapattığının garantisi yoktur, o yüzden cevabı yine sen okursun.
- **Notlar:** `hafizada_ara`'nın bulduğu metinler, her biri bir satırda. Hafızanın tamamı değil, yalnız bulunanlar.
- **Soru:** afişin metniyle birlikte.

"Her maddede dayandığın notu yaz" isteği cevabı kontrol edilebilir yapar: model "saat eksik" diyorsa yanında
"14 Ekim e-postası" yazmalı. Yazdığı not listede yoksa ya da notta öyle bir şey geçmiyorsa uydurmuştur.

Yardımcıdaki `modele_sor` Konu 5'tekinden iki yerde ayrılır. Birincisi, yönergeyi düz metin (`"prompt"`) olarak değil,
sohbetteki bir mesaj gibi (`"messages"`) gönderir. Hocanın denemesinde düz metinle giden bu uzun yönergeyi model
sürdürülecek bir belge sandı: afişin sonuna uydurma bir saat ekledi, sonra aynı soru-cevap satırlarını onlarca kez
tekrarladı. İkincisi, Konu 5'teki llama yerine Konu 10'da afişi okuyan gemma-4'ü kullanır: denemede llama aynı notlarla
bir seferinde "Ücretsiz" sözünü buldu, bir seferinde "ücretsiz sözcüğü yok" dedi; gemma-4 dört denemenin dördünde eksik
saati ve "Ücretsiz" sözünü buldu. Modelin "düşünme" adımı kapalı: cevap hızlı gelir ve az kota harcar.

**Arama kaçırırsa model de kaçırır.** Afişte "kafemizde" yazıyor; müşteri "kafe değil, çalışma evi" demişti. O not
bulunanlar arasında değilse model bunu göremez, çünkü önüne konmamıştır. Defterdeki **Dene** hücresi aynı hafızada
başka bir cümleyle arar ("Afiş metninde hangi sözcükler kullanılmamalı?"); cümleyi kendin değiştirebilir ya da `kac`'ı
büyütebilirsin. Hangi notların geleceğini arama cümlesi belirler; bir not gelirken bir başkası listeden düşebilir.
Afişin iki ayrı sorusu varsa (hangi bilgiler olmalı, hangi sözcükler olmamalı) iki ayrı arama yapıp bulunanları `+`
ile birleştirmek bir çözüm.

## Adım 4 — Hafıza büyür

```python
yeni_not = "Sayfa Kahve, WhatsApp, 30 Ekim: Etkinlik afişlerinde 'ücretsiz' sözcüğü de olmasın, kampanya gibi duruyor; 'çay ikramı' demek yeter."

with open("veri/notlar.txt", "a", encoding="utf-8") as dosya:
    dosya.write(yeni_not + "\n")

hafiza[yeni_not] = vektor_al(yeni_not)
print(len(hafiza))
```

Yeni not iki yere giriyor:

- **Dosyaya**, yarın da orada olsun diye. `"a"` (*append*) dosyanın sonuna ekler. `"w"` (*write*) dosyayı silip
  baştan yazar: bu satırda `"w"` olsaydı üç haftalık notların tek bir notla yer değiştirirdi. `"\n"` satır sonu;
  unutursan bir sonraki not bu notun sonuna yapışır.
- **Sözlüğe**, şimdi aranabilsin diye. Dosyaya yazmak vektörü kendiliğinden üretmez; vektörü ayrıca alıp sözlüğe
  koyuyoruz.

Sonra Adım 3'teki aramanın ve sorunun aynısı. Kodun hiçbir yerini değiştirmedik; hafızaya yalnız bir satır ekledik.
Yeni not bulunanlar arasına girdiyse "Ücretsiz çay ikramı" satırı artık bir sorun olarak çıkmalı. Dosyaya ekleme ve
sözlüğe koyma işini yardımcıdaki `not_ekle` tek satırda yapar; ödevde ve finalde işine yarar.

Konu 12'de bu hafızanın bir kopyası stüdyo asistanının olacak (`12-ajan/ciktilar/hafiza.txt`, ilk kullanımda Sayfa
Kahve'nin kılavuzundan ve ilk notlarından açılır). "Kurallara bak" aracı bu konudaki anlamca aramayı yapar, "hatırla"
aracı yeni notu o kopyanın sonuna ekler. Bugün hafızaya ne zaman bakılacağına sen karar verdin; orada asistan karar verecek.

## Hafızanın bakımı

Hafıza büyüdükçe bakım ister:

- **Çelişen kurallar.** Kılavuz "kışın hardal sarısı vurgu olarak eklenir" diyor. Müşteri yarın "kışın da hardal
  kullanmayalım" derse iki metin birlikte gelir ve model hangisine uyacağını bilemeyebilir. Notlardaki tarih bu
  yüzden var. Eski kural geçersiz olunca onu dosyadan sil ya da yanına "geçersiz, 2 Kasım" yaz.
- **Tekrar eden notlar.** Ekleme hücresini ya da defteri baştan ikinci kez çalıştırırsan not dosyaya iki kez yazılır.
  Dosyayı aç, fazlasını sil.
- **Bir dosya, bir müşteri.** İki müşterinin notları aynı dosyada olursa birinin kuralı diğerinin cevabına karışır.

## Ne zaman arama gerekir? (dürüst not)

30 metin için hepsini yönergeye koymak da olurdu; modelin önüne sığar ve "kafe" notu da kaçmazdı. Arama, notlar bir dönem boyunca ve birkaç
müşteriyle yüzlere çıkınca gerekir: hepsi sığmaz, sığsa da model ilgisiz notların arasında asıl kuralı gözden
kaçırabilir. Ama sayı az olsa bile "hangi not bu cevabı belirledi?" sorusunu sorabilmek her zaman işe yarar.

## Gizlilik: notlar nereye gidiyor?

Hafızaya sorduğun her soru, bulunan notlarla birlikte Cloudflare'in sunucusuna gider; hafızayı kurarken bütün notlar
gider. Bu yüzden notlara müşterinin telefon numarasını, adresini, fatura ya da ödeme bilgisini, bir başkasının
kişisel bilgisini yazma. Türkiye'de kişisel verileri KVKK korur; gerçek bir müşteriyle çalışıyorsan notlarını
böyle bir araca koyduğunu ona söyle. Ödevde uydurma ya da izinli bilgi kullan.

## Sık hatalar

| Ne gördün? | Neden? | Ne yapmalı? |
|---|---|---|
| `FileNotFoundError: ... 'veri/notlar.txt'` | Defter `11-rag` klasöründe değil | Defteri `11-rag` içinde aç |
| `FileNotFoundError: anahtar.txt bulunamadı` | Anahtar dosyası `gita3111` klasöründe değil | Konu 2'deki gibi oraya koy |
| `NameError: name 'hafiza' is not defined` | Adım 1'i atladın ya da çekirdek yeniden başladı | Defteri yukarıdan sırayla çalıştır |
| Yeni not dosyada iki kez var | Defteri ikinci kez çalıştırdın: Adım 4 her çalıştırmada aynı notu dosyaya yeniden ekler | `veri/notlar.txt`'yi aç, fazla satırı sil |
| İki not tek satırda birleşti | `write` içinde `"\n"` unutuldu | Dosyayı aç, satırı ikiye böl |
| Notların hepsi gitti, tek not kaldı | Dosyayı `"w"` ile açtın | `gita3111` klasöründe `git checkout 11-rag/veri/notlar.txt` ilk 16 notu geri getirir; sonradan eklediklerini yeniden yaz |
| Cevap yerine `None` | İstek başarısız oldu | Üstteki mesajı oku (anahtar, kota, internet) |
| Model "notlarda yok" dedi ama not hafızada var | Arama o notu getirmedi | Bulunanlara bak; aramanın sorusunu değiştir ya da `kac`'ı büyüt |
| Cevap afişin metnini sürdürüyor, aynı satırları tekrar ediyor | Konu 5'teki `modele_sor`'u kullandın: yönergeyi düz `"prompt"` olarak gönderiyor | `rag_araclari`'ndaki `modele_sor`'u kullan (`"messages"` ile gönderir) |

## Kendini dene

1. "Afişi matbaaya ne zaman göndermeliyim?" sorusunda hangi notlar gelir? Fatura notu kaçıncı sırada; tasarım
   sorularındakinden yukarıda mı? Neden olabilir?
2. "Gönderiye gülen surat koyabilir miyim?" diye sor. Emoji notu birinci mi geldi? Gelmediyse neden olabilir?
3. `yonerge_kur`'dan ilk satırı (kuralı) silip Adım 3'ü yeniden çalıştır. Cevap nasıl değişti?
4. Hafızana kılavuzla çelişen bir not ekle ("Sayfa Kahve, WhatsApp, 31 Ekim: Başlıklarda da serifsiz yazı kullanalım.")
   ve başlıkların yazı tipini sor. Model hangisine uydu, bunu söyledi mi? (Denemeden sonra bu satırı dosyadan sil.)
5. Cevabı hiçbir notta olmayan bir soru sor ("Afiş hangi kâğıda basılsın?"). Model "notlarda yok" dedi mi?

## Sözlükçe

- **RAG** (*retrieval-augmented generation*): soruya en yakın bilgiyi bulup modelin önüne koyarak cevap ürettirmek.
- **Hafıza:** bu konuda kılavuz ve notlardan oluşan, her metnin vektörüyle saklandığı sözlük.
- **Vektör (gömme):** bir metnin anlamını temsil eden sayı listesi (Konu 4).
- **Benzerlik:** iki vektörün ne kadar aynı yöne baktığını gösteren sayı; büyükse anlamca yakın.
- **Anlamca arama:** kelime yerine vektör benzerliğiyle arama.
- **Yönerge:** modele gönderilen metnin tamamı: kural, notlar, soru.
- **Uydurma:** modelin bilmediği yerde olası görünen ama dayanağı olmayan bir cevap yazması (Konu 5).
- **Kaynak göstermek:** cevabın hangi nota dayandığını yazmak; cevabı kontrol edilebilir yapar.
- **`"a"` ve `"w"`:** dosyayı sonuna eklemek için ya da silip baştan yazmak için açmak.
