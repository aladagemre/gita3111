# Konu 12 — Araç Kullanımı: Modelin Karar Verdiği Program

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 11'den Konu 12'ye: kararı kim veriyor?

- Konu 11'de halkaları bir hatta bağladık: bir halkanın çıktısı bir sonrakinin girdisi oldu
- O hatta her kararı sen verdin: hangi halka, hangi sırayla, ne zaman
- Programın her satırı senin önceden verdiğin bir karardı; program yalnızca uyguladı
- Bugün bir karar noktasını modele bırakıyoruz: kullanıcı serbest bir cümle yazıyor, model hangi aracın gerektiğine karar veriyor
- Program o kararı okuyup uyguluyor; çizen yine bizim fonksiyonumuz
- Bu, "yapay zeka ajanı" denen şeyin çekirdeği; bugün içini açıp bakacağız
- Dönemin en ileri konusu, ama yeni kod az: bir sözlük, bir `if` ve iyi yazılmış bir tarif

-----

## Mektup ve form: yapılandırılmış çıktı

- Bir müşteriye "projeni anlat" dersen bir mektup yazar: zengin ama her seferinde başka düzende
- Bir başvuru formu verirsen her bilgi kendi kutusunda gelir: ad, bütçe, teslim tarihi
- Mektubu insan okur; formu bir program da okuyabilir, yüz formu bir tabloya dökebilir
- Dil modelleri de iki türlü cevap verebilir: serbest bir paragraf ya da alanları belli bir cevap
- Alanları belli cevaba **yapılandırılmış çıktı** denir; çoğu zaman JSON biçiminde, yani bir sözlük
- Konu 2'deki cevaplar mektuptu; bugünküler form
- Form tasarımı tasarımcının bildiği bir iş: hangi kutular, hangi sırayla, hangi açıklamayla

-----

## Serbest kutu mu, açılır menü mü?

- Bir formda "renk" alanını serbest kutu yaparsan biri "lacivert", biri "Lacivert", biri "koyu mavi" yazar
- İnsan üçünü aynı sayar; bir program üçünü üç farklı renk sayar
- Açılır menü bunu çözer: herkes aynı seçeneklerden birini seçer
- Modelden alan isterken de aynısı geçerli: değerleri bir listeyle sınırlamak açılır menü gibidir
- Sınırlı alanla süzmek, saymak, karşılaştırmak mümkün olur
- **Yanılgı:** "model alanı istediğim gibi doldurur." Model kurala çoğu zaman uyar, her zaman değil; çıktıya bakmak yine senin işin

-----

## Araç nedir?

- **Araç** (tool): modele tanıttığımız, adı ve ne yaptığı belli bir fonksiyon
- Benzetme: Konu 11'deki mutfağa bir garson ve bir menü ekleyelim. Her yemeğin bir adı ve kısa bir açıklaması var; garson siparişi dinler, menüden seçer, mutfağa iletir
- Garson yemeği pişirmez; pişiren mutfak. Model de aracı çalıştırmaz; çalıştıran program
- Bir aracın üç parçası var: adı, tarifi (ne yapar, ne zaman seçilir), aldığı bilgiler
- Tasarım dünyasında örnek: bir görsel üretme aracı, bir düzenleme aracı, bir metin yazma aracı
- Model hangi araçların var olduğunu yalnızca senin tarifinden bilir; tarifte yoksa onun için yoktur

-----

## Karar da bir alan

- Modelden yalnızca bir slogan ya da bir ton değil, bir **karar** da isteyebiliriz
- Karar iki alanlı bir form: hangi araç, o araca ne söylenecek (yönerge)
- Program kararı okur ve doğru fonksiyonu çağırır: "araç buysa şunu çalıştır, şuysa öbürünü"
- Model hiçbir şey çizmez, hiçbir dosyaya dokunmaz; yalnızca bir sözlük gönderir
- Bu yüzden program, modelin listede olmayan bir şey yazmasına karşı hazırlıklı olmalı: "bilinmeyen araç" diyen bir dal
- **Yanılgı:** "ajan bilgisayarımda kendi başına bir şeyler çalıştırıyor." Çalıştıran, senin yazdığın ve izin verdiğin kod

-----

## Kararı görünür kılmak

- Model bir karar verdiğinde onu ekrana yazdır: hangi aracı seçti, hangi yönergeyle
- Görmediğin bir kararı ne düzeltebilir ne savunabilirsin
- Bir stüdyoda iş dağıtan kişi "bu işi kime, neden verdim" diye not tutar; aynı alışkanlık
- Yanlış görsel geldiğinde ilk soru: model mi yanlış araç seçti, yoksa doğru araç mı kötü çalıştı?
- Kayıt bu ikisini ayırır: karar bir yerde, sonuç başka bir yerde
- Şeffaflık için de gerekli: bir müşteriye "bu görseli şu araç, şu yönergeyle üretti" diyebilmek

-----

## Ajan: gizemli değil

- 2026'da "yapay zeka ajanı" denen şeyin çekirdeği üç parça: model karar verir, program aracı çalıştırır, sonuç modele geri gider
- Sohbet asistanının "internette arıyorum" demesi bir araç çağrısı; arayan asistanın arkasındaki program
- Kod asistanlarının (Antigravity gibi) terminalde komut çalıştırması da bir araç; bu yüzden komutları onaysız çalıştırmayı kapalı tutuyoruz
- Her araç modelin eline verilen bir yetki: görsel üretmek zararsız, dosya silmek ya da e-posta göndermek değil
- Kural: geri alınamayan işleri yapan araçlar bir insan onayından geçmeli
- Model karar verse de sorumluluk aracı kuran ve çalıştırandadır

-----

## Sonsuz döngü ve durma koşulu

- Bir ajan aracın sonucuna bakıp bir sonraki adıma karar verebilir: "görsel olmadı, yeniden düzenleyeyim"
- Yeniden bakar, yine beğenmez, yine düzenler... Kimse durdurmazsa döngü kota bitene kadar dönebilir
- Benzetme: sonu gelmeyen revizyon. "Bir tur daha" diyen müşteriyle sözleşmeye revizyon sayısı yazılır
- **Durma koşulu** her döngünün ilk yazılan satırıdır: en fazla şu kadar tur, ya da "bitti" kararı, ya da insanın "dur" demesi
- Konu 9'daki güvenlik sınırının aynısı; karar modelde olunca daha da gerekli
- Ücretli bir hizmette durmayan döngü doğrudan fatura demektir

-----

## Model doğru mu seçiyor? Ölçmek

- İki örnekte doğru seçmesi bir şey kanıtlamaz; birçok örnekle ölçmek gerekir
- Konu 3'ü hatırla: doğru cevabı insanın verdiği örnekler bir **test verisi**dir
- Önce sen karar verirsin (etiketlersin), sonra modelin kararlarını seninkilerle karşılaştırırsın
- **Doğruluk** = aynı fikirde olduğunuz karar sayısı / toplam karar
- Sayıdan çok ayrıştığınız örnekler öğretir: model mi yanıldı, yoksa istek mi iki türlü okunabiliyor?
- Bazen tek bir "doğru cevap" yoktur; o zaman sorun modelde değil, eksik kalan kuraldadır

-----

## Araç tarifi yazmak brif yazmaktır

- Bir tasarımcıya "logoyu daha modern yap" dersen o da sorar: hangi logo, ne kadar, hangi yöne?
- Muğlak bir brif, ister insana ister modele verilsin, yanlış işi getirir
- Model araçlarını yalnızca tarifinden tanır; tarif muğlaksa seçim de muğlak olur
- İyi bir tarif: araç ne yapar, **ne zaman** seçilmeli, **ne zaman** seçilmemeli, emin değilse ne yapılmalı
- Model yanlış araç seçtiğinde ilk düzeltilecek yer çoğu zaman model değil, tariftir
- Tasarımcının zaten bildiği bir beceri burada ölçülebilir hâle gelir: tarifi değiştir, doğruluğun değişimine bak

**Sohbete yaz:** "afişi biraz daha canlı yap" isteği hangi durumlarda yeni bir görsel, hangi durumlarda düzenleme demek?

-----

## Ölçüyü kandırmamak

- Tarifi düzeltirken ayrıştığın örneklere bakarsın; bu doğru
- Ama aynı örneklerle yeniden ölçersen yalnızca o örnekleri ezberleyen bir kural yazmış olabilirsin
- Konu 3'teki tuzak: test sonucuna bakıp ayar yapmak, sonra aynı testte ölçmek
- Çözüm: tarifi düzelttikten sonra, tarifi yazarken bakmadığın **yeni** isteklerle de ölç
- Yeni kural fazla dar da çıkabilir: bir durumu düzeltirken başka bir durumu dışarıda bırakır
- Döngü: yaz, ölç, ayrışana bak, düzelt, yeni örneklerle yeniden ölç

-----

## Ne zaman gereksiz?

- Tek bir aracın varsa karar zaten belli; modele sormak yalnızca bir istek, biraz gecikme ve bir hata ihtimali ekler
- Kararı basit bir kuralla verebiliyorsan (dosya yüklendiyse düzenle, yoksa üret) bir `if` yeter
- Araç kullanımı, isteklerin serbest cümleyle geldiği ve birden çok seçeneğin olduğu yerde anlamlı
- Her model kararı bir maliyettir: kota, süre ve yanlış seçim ihtimali
- Bir kafe sitesinde "menü görseli üret" düğmesi için ajan gerekmez; "ne istersen yaz" kutusu için gerekebilir
- Final projesinde araç kullanımı zorunlu değil; projen tek adımlıysa hiç kullanmaman doğru karar olabilir

**Sohbete yaz:** kendi final projende modelin vermesini isteyeceğin bir karar var mı, yoksa kararlar zaten belli mi?

-----

## Bu konunun ödevi

**Üçüncü araç.**

1. Dersteki programa üçüncü bir araç ekle: `metin_yaz` (ör. afiş için slogan ya da açıklama metni)
2. Üç aracın tarifini yaz; kararı uygulayan koda üçüncü dalı ekle
3. Kendi projene göre en az 6 istek yaz ve önce kendin etiketle; modelin seçimini ölç
4. Bir tarifi düzelt ve en az 3 **yeni** istekle yeniden ölç
5. **İki cümle:** model en çok hangi istekte ayrıştı, tarifte neyi değiştirdin?

Ayrıntılar: `odevler/odev12.md`. Puan yok; Konu 13'ün başında sıradaki arkadaşlar gösterecek. Araç kullanımı final için zorunlu değil.

-----

## Hatırlanacaklar

1. **Form, mektup değil.** Yapılandırılmış çıktı modelin cevabını programın okuyabileceği alanlara koyar
2. **Alanı sınırla.** Açılır menü gibi: değerler bir listeden gelirse süzmek ve saymak mümkün olur
3. **Model karar verir, program uygular.** Model hiçbir şey çizmez; kararı görünür kıl, bilinmeyen araca hazırlıklı ol
4. **Ölç, sonra yeni örneklerle yeniden ölç.** Doğruluk bir sayı; asıl ders ayrışılan örneklerde
5. **Tarif bir brif.** Yanlış seçimde önce tarife bak; her döngüye bir durma koşulu koy

Sıradaki konu: **Konu 13 — Final atölyesi ve sunum.** Yeni kavram yok: dönem boyunca öğrendiklerini kendi projende birleştirip çalışan bir çekirdeğe dönüştürüyorsun.
