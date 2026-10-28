# Konu 12 — Ajan: Kararı Modele Bırakmak

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 10'dan Konu 12'ye: sırayı kim belirliyor?

- Konu 10'daki hatta her adımın yerini sen yazdın: önce slogan, sonra görsel, her seferinde aynı sırayla
- Konu 11'de modele bir belgeyi okuttun; hangi paragrafların gideceğini yine senin programın seçti
- Bazı işlerde sıra baştan belli değil: "kılavuza uygun bir afiş" önce okumayı, sonra çizmeyi ister; "bu fotoğrafı sadeleştir" yalnızca düzenlemeyi
- Bugün bu kararı modele bırakıyoruz: hangi araç, hangi bilgiyle, hangi sırayla
- Model yalnızca hangi aracın çalışacağını seçip yazar; aracı çalıştıran yine senin programın
- Bu düzenin adı **ajan**; önce içini elle açacağız, sonra bir çerçeveyle kuracağız

-----

## Ajan nedir?

- **Ajan** (agent): bir isteğe hangi araçların, hangi sırayla kullanılacağını bir dil modelinin seçtiği program
- Üç parçası var: seçimi yapan bir dil modeli, modelin kullanabileceği **araçlar** ve ikisini bağlayan bir **döngü**
- Sohbet asistanının "internette arıyorum" demesi bir ajan davranışı: arama bir araç, aramayı seçen model
- Kod asistanlarının (Antigravity gibi) dosya okuyup komut çalıştırması da öyle
- "Ajan" sözcüğü bugün pek çok şey için, çoğu zaman abartılarak kullanılıyor; özünde bu üç parça var
- **Yanılgı:** "ajan her şeyi kendi başına yapabilen bir yapay zeka." Ajan, verdiğin araçlar kadar iş yapar; aracı olmayan işi yapamaz

-----

## Araç: modelin eline verilen fonksiyon

- **Araç** (tool): modele tanıttığımız, adı ve ne işe yaradığı belli bir fonksiyon
- Bir restoran düşün: garson siparişi dinler, menüden seçer, mutfağa iletir; yemeği pişiren mutfaktır
- Model garsondur: hangi aracın gerektiğini seçer ama aracı kendisi çalıştırmaz; aracı senin programın çalıştırır
- Bir aracın üç parçası var: **adı**, **tarifi** (ne yapar, ne zaman seçilir) ve **aldığı bilgiler** (ör. bir yönerge, bir dosya yolu)
- Tasarımdan örnekler: görsel çizen, fotoğraf düzenleyen, marka kılavuzunda arayan, slogan yazan araçlar
- Model yalnızca kendisine tanıtılan araçları kullanabilir; listede olmayan bir araç onun için yoktur

-----

## Model aracın içini görmez

- Model fonksiyonun kodunu hiç görmez; yalnızca adını, tarifini, bilgilerinin adını ve türünü görür
- Garson da mutfağa girmez; menüdeki yemeğin adını ve açıklamasını bilir
- Aracın içini değiştirip tarifini aynı bırakırsan, model için seçimi etkileyen hiçbir şey değişmemiştir
- Araç çalışınca modele yalnızca sonucu döner (ör. "görsel kaydedildi" ya da kılavuzdan birkaç paragraf); kod yine görünmez
- Bu yüzden sonucu açık yaz: "Görsel çizilemedi" gibi bir cümle, modelin bir sonraki adımı seçmesine yardım eder; boş bir sonuç etmez
- **Yanılgı:** "model fonksiyonun ne yaptığını koddan anlar." Anlamaz; ona ne söylediysen onu bilir

-----

## Döngü: karar, iş, sonuç, yeni karar

1. Kullanıcı bir istek yazar; program isteği ve araçların tariflerini modele gönderir
2. Model ya cevabını yazar ya da "şu aracı, şu bilgiyle çalıştır" diyen bir **araç çağrısı** gönderir
3. Program aracı çalıştırır ve sonucunu yeni bir mesaj olarak modele geri gönderir
4. Model sonuca bakar ve yeniden seçer: başka bir araç mı, yoksa son cevap mı?
5. Döngü, model son cevabını yazınca ya da bir sınıra ulaşılınca biter
6. Her turda konuşma büyür: program her istekte o ana kadarki konuşmanın tamamını yeniden gönderir

-----

## Çerçevesiz bir tur

- Araç çağrısının arkasında gizem yok: istek gövdesinde bir alan, cevapta bir alan daha
- İstekte `tools`: her aracın adı, tarifi ve bilgileri, iç içe sözlükler olarak
- Cevapta `tool_calls`: modelin çağırmak istediği aracın adı ve doldurduğu bilgiler
- Programın işi: adı okumak, doğru fonksiyonu çağırmak, listede olmayan bir ada karşı hazırlıklı olmak
- Tek bir tur birkaç satır; döngünün tamamını elle yazmak ise uzun ve hataya açık

```py
arac = {"name": "logo_bul", "description": "Markanın logo dosyasını bulur.", "parameters": bilgiler}
govde = {"messages": [mesaj], "tools": [arac]}
```

-----

## Çerçeve neyi gizler?

- **Ajan çerçevesi** (agent framework): döngünün her seferinde aynı olan kısmını senin yerine yazan bir kütüphane
- Bugün kullandığımız çerçeve **Agno**: aracı sıradan bir Python fonksiyonu olarak yazarsın, gerisini o kurar
- Çerçevenin üstlendikleri: tarifleri isteğe koymak, cevabı okumak, aracı çalıştırmak, sonucu geri göndermek, sınırı saymak
- Üstlenmedikleri: hangi araçların olacağı, tariflerin ne kadar iyi yazıldığı, sonucun doğru olup olmadığı
- Gizlenen iş ortadan kalkmaz: modele yine aynı istekler gider, kota yine harcanır
- Agno tek çerçeve değil (LangChain, CrewAI gibi başkaları da var); hepsinin içinde aynı döngü döner, birini anlayan öbürünü de okuyabilir

-----

## Agno: kullanmadan önce bilinecek iki şey

- Agno'da model `OpenAILike` ile tanıtılır; istekleri `openai` paketi gönderir
- Ad yanıltmasın: bu yalnızca isteğin **biçiminin** adı; istekler Cloudflare'e gider, OpenAI hesabı da ödemesi de gerekmez
- Birçok sağlayıcı aynı biçimi kullanır; biçimin adı onu ilk yaygınlaştıran şirketten kalmış
- Agno, kapatılmazsa her çalıştırmada kendi sunucusuna kullanım bilgisi gönderir (**telemetri**)
- Bu yüzden her ajanda `telemetry=False` yazıyoruz: programımız bizden habersiz kimseye bilgi göndermesin
- Genel ders: bir kütüphaneyi kurmak, onun bütün varsayılan ayarlarını kabul etmek demek değildir

-----

## Agno'da araç: sıradan bir fonksiyon

```py
def acilis_saati(gun: str) -> str:
    """Kafenin verilen gündeki açılış saatini verir. gun: haftanın günü, ör. pazartesi."""
    return saatler[gun]
```

- Aracın adı fonksiyonun adıdır; tarifi, `def` satırının hemen altındaki üç tırnaklı metindir: **docstring**
- `gun: str` bir **tür ipucu**: "bu bilgi metin"; elle yazılan tarifteki `"type": "string"`'in Python'daki karşılığı
- `-> str`: fonksiyonun metin verdiğini söyler
- `return` edilen metin modele geri gider; `print` yalnızca seni bilgilendirir
- Bilgilerin adları da tarifin parçası: `gun`, `dosya`, `yonerge` gibi adlar modele ne yazacağını anlatır

-----

## Tarif bir brif

- Bir tasarımcıya "logoyu daha modern yap" dersen o da sorar: hangi logo, ne kadar, hangi yöne?
- Model çoğu zaman geri sormaz; eksik bilgiyi en olası anlamla doldurup işe başlar
- Muğlak bir brif, ister insana ister modele verilsin, yanlış işi getirir
- Model yanlış aracı seçtiğinde ilk bakılacak yer çoğu zaman model değil, tariftir
- İyi bir tarif: araç **ne yapar**, içinde **ne var**, **ne zaman** seçilmeli, **ne zaman** seçilmemeli
- Kopyala-yapıştırla aynı kalmış iki tarif, menüde aynı açıklamalı iki yemek gibidir: seçim şansa kalır
- Tarifi değiştirince aynı isteği yeniden dene; tek deneme bir şey kanıtlamaz, birkaç istekle bak

-----

## Kararı görünür kılmak

- Ajan çalıştıktan sonra yalnızca son cevabına bakma; hangi araçları, hangi bilgilerle çağırdığına bak
- Kararı modele bırakınca bilgileri de model doldurur: görsel yönergesini, dosya yolunu, arama sorusunu
- Görmediğin bir kararı ne düzeltebilir ne savunabilirsin
- Yanlış görsel geldiğinde ilk soru: model mi yanlış aracı seçti, doğru araç mı kötü bir yönergeyle çalıştı?
- Bir stüdyoda iş dağıtan kişi "bu işi kime, hangi brifle verdim" diye not tutar; ajanın araç kaydı da aynı işi görür
- Şeffaflık için de gerekli: müşteriye "bu görseli şu araç, şu yönergeyle üretti" diyebilmek

-----

## Güvenlik: her araç bir yetki

- Modelin eline verdiğin her araç bir yetkidir: görsel çizmek zararsız, dosya silmek ya da e-posta göndermek değil
- Model yanlış araç seçebilir, isteği yanlış yorumlayabilir, kendisine gelen bir belgedeki bir cümleyi talimat gibi izleyebilir
- Kural: geri alınamayan işleri yapan araçlar bir insan onayından geçmeli
- Kod asistanında komutların onaysız çalışmasını kapalı tutmamızın nedeni de bu
- Ajana yalnızca işin gerektirdiği araçları ver; "belki lazım olur" diye araç ekleme
- Seçimi model yapsa da sonucun sorumluluğu aracı yazan ve ajanı çalıştıran kişidedir

-----

## Sınır ve kota

- Döngü kendiliğinden durmayabilir: model aynı aracı tekrar tekrar çağırabilir, "bir düzenleme daha, bir tane daha"
- Tasarımdaki karşılığı sonu gelmeyen revizyon; bu yüzden sözleşmeye revizyon sayısı yazılır
- Ajanın revizyon sayısı **araç çağrısı sınırıdır**: bir çalıştırmada en fazla şu kadar araç çalışsın
- Her araç çağrısı modele bir istek daha demek; görsel çizen her çağrı ayrıca bir görsel
- Konuşma büyüdükçe istekler de büyür; günlük kota beklediğinden hızlı biter
- Sınırı işin büyüklüğüne göre seç: beklenen adım sayısı artı biraz pay

-----

## Ne zaman fazla gelir?

- Sıra her seferinde aynıysa ajan gerekmez: Konu 10'daki gibi bir hat daha ucuz, daha hızlı ve daha öngörülebilir
- Tek bir aracın varsa seçim zaten belli; modele sormak yalnızca gecikme ve hata ihtimali ekler
- Kararı basit bir kuralla verebiliyorsan (dosya yüklendiyse düzenle, yoksa çiz) bir `if` yeter
- Ajan, isteklerin serbest cümleyle geldiği, araçların çok ve sıranın belirsiz olduğu işlerde anlamlıdır
- Her model kararı bir maliyettir: kota, süre ve yanlış seçim ihtimali
- Final projesinde ajan (RAG gibi) isteğe bağlı bir ekstra; projen sırası belli bir hatsa ajan kullanmaman doğru karar olabilir

**Sohbete yaz:** final projende sırası baştan belli olmayan bir iş var mı?

-----

## Sık yanılgılar

- "Model düşünüp en doğru sırayı bulur." Model düşünmez: isteğe, tariflere ve gelen sonuçlara bakıp bir sonraki adımı seçer ve yazar. Seçim çoğu zaman yerinde olur ama garantisi yoktur
- "Ajan bir önceki isteğimi hatırlıyor." Model hiçbir şey hatırlamaz; bir çalıştırmanın içinde hatırlıyor gibi görünmesinin nedeni, konuşmanın her istekte yeniden gönderilmesi. Çerçeve ayrıca kayıt tutmuyorsa her çalıştırma sıfırdan başlar
- "Çerçeve kullanınca kararlar daha doğru olur." Çerçeve döngüyü yazar; kararın kalitesi modele ve tariflere bağlı
- "Ne kadar çok araç, o kadar iyi ajan." Her araç modelin önüne bir seçenek daha koyar: seçim zorlaşır, yanlış araç ihtimali artar
- "Sınır koymak ajanı kısıtlar." Sınır kotanı ve dosyalarını korur; işi büyükse sınırı bilerek büyütürsün

-----

## Bu konunun ödevi

**Ajanına yeni bir yetenek.**

1. Ders defterinin kopyasına kendi tasarladığın bir araç ekle: tür ipuçları, docstring, `return`
2. En az dört istek yaz; çalıştırmadan önce her biri için kendi planını yaz (hangi araçlar, hangi sırayla)
3. Ajanı çalıştır, kararlarını yazdır, planınla karşılaştır
4. Aracının tarifini bilerek boz, aynı isteği yeniden dene; sonra düzelt
5. **İki cümle:** model nerede senden ayrıştı, tarifte neyi değiştirdin?

Ayrıntılar: `odevler/odev12.md`. Puan yok; Konu 13'ün başında sıradaki arkadaşlar gösterecek.

-----

## Hatırlanacaklar

1. **Ajan = model + araçlar + döngü.** Model seçer, program çalıştırır, sonuç modele döner
2. **Model aracın içini görmez.** Adını, tarifini ve bilgilerini görür; tarif bir brif
3. **Çerçeve döngüyü gizler, kararı değil.** Her çalıştırmadan sonra çağrılan araçlara bak
4. **Her araç bir yetki, her çağrı bir istek.** Sınır koy; geri alınamayan işe insan onayı
5. **Sıra belliyse hat yeter.** Ajan, sırası belirsiz işler için

Sıradaki konu: **Konu 13 — Final atölyesi.** Yeni kavram yok: dönem boyunca öğrendiklerini kendi projende birleştirip projenin çalışan ilk hâlini kuruyorsun. RAG ve ajan zorunlu değil, isteğe bağlı birer ekstra.
