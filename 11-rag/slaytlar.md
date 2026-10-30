# Konu 11 — Müşterinin söylediklerini unutmayan bir hafıza

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## "Bunu söylemiştim": dağınık istekler, unutulan revizyonlar

- Müşteri bir isteğini WhatsApp'tan yazar, bir başkasını e-postada söyler, üçüncüsünü toplantıda geçerken anar
- Jüride hocalar aynı eleştiriyi iki hafta arayla tekrar eder: "kenarlarda nefes yok"
- Üç hafta sonra yeni afişi yaparken bunların yarısı akılda değildir
- Sonuç: bir revizyon turu daha, müşteride "beni dinlemiyor" duygusu, kaybolan saatler
- Bilgi aslında var; ama dağınık, ve kimse onu aramıyor
- Bugünün işi: bir müşterinin kurallarını ve notlarını tek yerde tutan, soru sorulabilen bir hafıza

-----

## Sektörde de zor kısım hatırlamak

- Adobe'nin 2026 araştırmasında bir yönetmen, birkaç günlük sunum hazırlığının zor kısmını "şirketi ve önceki kampanyalarını anlamak için kazmak" diye anlatıyor
- Bir marka ajansı: "En büyük darboğazımız tasarım değil, tekrar eden idari işti"; müşteri kabulünü ve teslimi otomatikleştirerek çözmüşler
- Tasarımcılar yapay zekâ çıktısına az güveniyor: Figma'nın 2025 raporunda çıktıya güvenebildiğini söyleyenler yaklaşık üçte bir
- Bu yüzden bugünkü araç yaratıcı kararı vermiyor; unuttuğunu hatırlatıyor ve nereden hatırladığını gösteriyor
- Fikir ve seçim sende kalıyor, angarya araca geçiyor

-----

## RAG: açık kitap sınavı

- **RAG** (*retrieval-augmented generation*): "bulup getirerek üretmek"
- Açık kitap sınavında öğrenci cevabı ezberinden değil, önündeki kitaptan verir; doğru sayfayı açmak da onun işidir
- Model de senin müşterini tanımaz; onun kurallarını eğitiminde hiç görmemiştir
- Biz soruya uygun notları bulup modelin önüne koyarız; model cevabı o notlara bakarak yazar
- Başka bir benzetme: yeni stajyere müşteriyi sorduğunda önce müşteri dosyasını açar, sonra cevap verir
- Model notlarını "öğrenmez"; her soruda notlar yeniden önüne konur

-----

## İki yarı: bulmak ve önüne koymak

- **Bulmak:** sorunun anlamına en yakın notları seçmek (Konu 4'teki vektörler ve benzerlik)
- **Önüne koymak:** seçilen notları bir kural ve soruyla birlikte tek bir yönergede modele vermek
- Yapay zekâ iki yerde çalışır: metni vektöre çevirmek ve notları okuyup cevap yazmak
- Kalanı sıradan bir Python betiği yapar: dosyayı okumak, not eklemek, puanları sıralamak, yönergeyi birleştirmek
- Cevap, bulunan notlardan iyi olamaz: önüne konmayan notu model göremez
- Hafızaya bilgi eklemek için modeli yeniden eğitmek gerekmez; dosyaya bir satır eklemek yeter

-----

## Kelimeyle aramak, anlamla aramak

- Ctrl + F kelimenin şeklini arar: "font" diye ararsan "yazı tipi" yazan notu bulamazsın
- Ortak kelime olunca da yanılabilir: aynı kelime iki ayrı konuda geçebilir
- Türkçenin ekleri işi zorlaştırır: "fotoğrafta" diye ararsan "fotoğraflarda" geçen not çıkmaz
- Anlamca arama metni bir vektöre çevirir; anlamı yakın iki metnin vektörleri aynı yöne bakar (Konu 4)
- Böylece soru ile not ortak bir kelime taşımasa da birbirini bulur
- Kelime araması notta hangi kelimenin geçtiğini bilmeni ister; bunu biliyorsan notu zaten hatırlıyorsundur

-----

## Anlamca arama da yanılır

- "Gönderiye gülen yüz koyabilir miyim?" sorusu emoji notu yerine "fotoğrafta insan yüzü olmasın" notunu getirebilir: "yüz" iki anlamda
- Arama her zaman istediğin sayıda not getirir; cevabı hiçbir notta olmayan bir soruda da "en yakın üç" gelir
- Kısa, tek konulu notlar daha iyi bulunur; bir satıra üç ayrı istek yazarsan hiçbiri tam eşleşmez
- Arama bir notu kaçırırsa model de kaçırır; cevabı okumadan önce hangi notların geldiğine bak
- Çözüm çoğu zaman aramanın sorusunu değiştirmek ya da biraz daha fazla not getirmek

-----

## "Yalnız notlara dayan" neden önemli?

- Konu 5'te gördük: model bilmediği yerde çoğu zaman "bilmiyorum" demez, olası görünen bir cevap uydurur
- Müşteri hafızasında uydurma pahalıdır: müşterinin hiç söylemediği bir kural afişe girer
- Yönergenin başındaki kural: "Yalnız bu notlara dayan; notlarda yoksa 'notlarda yok' de"
- "Notlarda yok" da bir cevaptır: müşteriye sorman gereken soruyu gösterir
- Kaynak istemek cevabı kontrol edilebilir yapar: "saat eksik (14 Ekim e-postası)"
- Kural uydurmayı azaltır ama sıfırlamaz; son okuma her zaman tasarımcının

-----

## Hafıza büyür

- Her yeni mesaj, her jüri notu dosyaya bir satır olarak eklenir; hafıza dönem boyunca büyür
- Yeni bir not eklenince aynı soru farklı bir cevap alabilir: kod değişmez, hafıza değişir
- Revizyon geçmişi kendiliğinden birikir: kim, ne zaman, hangi kanaldan ne istedi
- Jüri notları da hafızada: aynı eleştiriyi üçüncü kez duymadan önce sen görürsün
- Bir dosya, bir müşteri: iki müşterinin kuralları birbirine karışmasın
- Final projende bu hafızadan bilgi çeken küçük bir adım zorunlu

-----

## Hafızanın bakımı

- Eski kural geçersiz olabilir: kılavuz "kışın hardal sarısı vurgu" der, müşteri bir gün "hardalı bırakalım" der
- Çelişen iki metin birlikte gelirse model hangisine uyacağını bilemeyebilir
- Her notun başına kaynağı ve tarihi yaz; yeni olanın eskiyi geçtiğini modele ayrıca söylemek gerekir
- Geçersiz kuralı sil ya da yanına "geçersiz" ve tarihi yaz
- Neredeyse aynı iki not arama sonuçlarında iki yer kaplar, başka bir notu dışarıda bırakır
- Arada bir dosyayı baştan sona oku: hafıza, bakımı yapılan bir defter kadar iyidir

-----

## Gizlilik: müşteri bilgisi nereye gidiyor?

- Hafızayı kurarken bütün notlar, her soruda da bulunan notlar modelin sunucusuna gider (bu derste Cloudflare)
- Telefon numarası, adres, fatura ve ödeme bilgisi, başkalarının kişisel bilgileri notlara girmez
- Türkiye'de kişisel verileri KVKK korur; müşterinin bilgisini bir yapay zekâ servisine koymak bir sorumluluktur
- Gerçek bir müşteriyle çalışıyorsan notlarını böyle bir araca koyduğunu ona söyle
- Henüz duyurulmamış bir ürün ya da gizli bir proje varsa o notları hafızaya hiç koyma
- Bu dersteki örnekler uydurma; ödevde de uydurma ya da izinli bilgi kullan

-----

## Ne zaman arama gerekir, ne zaman gerekmez?

- Az not varsa hepsini yönergeye koymak da olur; bir müşterinin birkaç düzine notu modelin önüne sığar
- Arama, notlar bir dönem boyunca ve birkaç müşteriyle yüzlere çıkınca gerekir
- Çok sayıda ilgisiz not, modelin asıl kuralı gözden kaçırmasına yol açabilir
- Daha kısa yönerge daha az kota harcar
- Not sayısı ne olursa olsun kaynak göstermek işe yarar: hangi notun cevabı belirlediğini görürsün
- Önce basit olanı dene; yetmediği yerde arama ekle

-----

## Sık yanılgılar

- **"Model notlarımı öğrendi."** Hayır; her soruda notlar yeniden önüne konur. Dosyayı silersen hiçbir şey hatırlamaz
- **"Anlamca arama hiç yanılmaz."** Yanılır; gelen notlara bakmadan cevaba güvenme
- **"Ne kadar çok not getirirsem o kadar iyi."** İlgisiz notlar asıl kuralı gölgeleyebilir
- **"Kural yazdım, artık uydurmaz."** Kural uydurmayı azaltır, sıfırlamaz
- **"Dosyaya yazdım, artık aranır."** Vektörü alınmamış bir not aranamaz
- **"Hafıza kendini günceller."** Eski kuralı silmek ya da işaretlemek senin işin

-----

## Ödev ve sıradaki konu

- **Ödev 11:** kendi müşterin için en az 8 notluk bir hafıza (müşterinin istekleri ve aldığın eleştiriler)
- Hafızana 3 soru sor; her sorunun cevabını ve gelen notları kaydet
- Bir not ekle ve cevabı değişen bir soru göster
- Bu hafıza, final projendeki zorunlu küçük RAG adımının temeli
- **Sıradaki: Konu 12 — Stüdyo asistanı.** Bu hafızanın bir kopyası asistanın olacak: kurallara kendisi bakacak, "unutma" dediğini o kopyaya yazacak
- Bugün hafızaya ne zaman bakılacağına sen karar verdin; Konu 12'de ne zaman bakacağına asistan karar verecek
