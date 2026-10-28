# Konu 12 — Ajan: Kararı Modele Bırakmak

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 10'dan Konu 12'ye: sırayı kim belirliyor?

- Konu 10'daki hatta her adımın yerini sen yazdın: önce slogan, sonra görsel, her seferinde aynı sırayla
- Konu 11'de modele bir belgeyi okuttun; hangi paragrafların gideceğini yine senin programın seçti
- Bazı işlerde sıra baştan belli değil: "kılavuza uygun bir afiş" önce okumayı, sonra çizmeyi ister; "bu fotoğrafı sadeleştir" yalnızca düzenlemeyi
- Bugün bu kararı modele bırakıyoruz: hangi araç, hangi bilgiyle, hangi sırayla
- Çalıştıran yine senin programın; model yalnızca karar veriyor
- Bu düzenin adı **ajan**; önce içini elle açacak, sonra bir çerçeveyle kuracağız

-----

## Ajan nedir?

- **Ajan** (agent): bir istek verildiğinde, elindeki araçlardan hangisini ne zaman kullanacağına kendisi karar veren program
- Üç parçası var: kararı veren bir dil modeli, modelin kullanabileceği **araçlar** ve ikisini bağlayan bir **döngü**
- Sohbet asistanının "internette arıyorum" demesi bir ajan davranışı: arama bir araç, aramaya karar veren model
- Kod asistanlarının (Antigravity gibi) dosya okuyup komut çalıştırması da öyle
- "Ajan" sözcüğü bugün pek çok şey için, çoğu zaman abartılarak kullanılıyor; çekirdeği bu üç parçadır
- **Yanılgı:** "ajan her şeyi kendi başına yapabilen bir yapay zeka." Ajan, verdiğin araçlar kadar iş yapar; aracı olmayan işi yapamaz

-----

## Araç: modelin eline verilen fonksiyon

- **Araç** (tool): modele tanıttığımız, adı ve ne işe yaradığı belli bir fonksiyon
- Bir restoran düşün: garson siparişi dinler, menüden seçer, mutfağa iletir; yemeği pişiren mutfaktır
- Model garsondur: hangi aracın gerektiğine karar verir ama aracı kendisi çalıştırmaz; çalıştıran program
- Bir aracın üç parçası var: **adı**, **tarifi** (ne yapar, ne zaman seçilir) ve **aldığı bilgiler** (ör. bir yönerge, bir dosya yolu)
- Tasarımdan örnekler: görsel çizen, fotoğraf düzenleyen, marka kılavuzunda arayan, slogan yazan araçlar
- Model hangi araçların var olduğunu yalnızca senin tarifinden bilir; tarifte yoksa onun için yoktur

-----

## Model aracın içini görmez

- Model fonksiyonun kodunu hiç görmez; yalnızca adını, tarifini ve bilgilerinin türünü görür
- Garson da mutfağa girmez; menüdeki yemeğin adını ve açıklamasını bilir
- Aracın içi değişip tarifi aynı kalırsa model kararını değiştirmek için bir neden görmez
- Aracın verdiği sonuç (ör. "görsel kaydedildi" ya da kılavuzdan üç paragraf) modele geri döner: model sonucu görür, kodu görmez
- Bu yüzden bir aracın tarifi, bir tasarımcıya verilen brif gibidir: eksikse iş yanlış gelir
- **Yanılgı:** "model fonksiyonun ne yaptığını koddan anlar." Anlamaz; ona ne söylediysen onu bilir

-----

## Döngü: karar, iş, sonuç, yeni karar

1. Kullanıcı bir istek yazar; program isteği ve araçların tariflerini modele gönderir
2. Model ya cevabını yazar ya da "şu aracı, şu bilgiyle çalıştır" der; buna **araç çağrısı** denir
3. Program aracı çalıştırır ve sonucunu yeni bir mesaj olarak modele geri gönderir
4. Model sonuca bakar ve yeniden karar verir: başka bir araç mı, yoksa son cevap mı?
5. Döngü, model son cevabını yazınca ya da bir sınıra ulaşılınca biter
6. Her turda konuşma büyür: model her seferinde o ana kadar olan her şeyi yeniden okur

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
- Çerçevenin varsayılan ayarları da bir karardır; neyi açık bıraktığını öğrenmeden kullanma

-----

## Agno: kullanmadan önce bilinecek iki şey

- Agno'da model `OpenAILike` adlı bir sınıfla tanıtılır ve `openai` paketiyle konuşur
- Ad yanıltmasın: bu yalnızca isteğin **biçiminin** adı; istekler Cloudflare'e gider, OpenAI hesabı da ödemesi de gerekmez
- Birçok sağlayıcı aynı biçimi konuşur; biçimin adı onu ilk yaygınlaştıran şirketten kalmış
- Agno, kapatılmazsa her çalıştırmada kendi sunucusuna kullanım bilgisi gönderir (**telemetri**)
- Bu yüzden her ajanda `telemetry=False` yazıyoruz: programımız bizden habersiz kimseye bilgi göndermesin
- Genel ders: bir kütüphaneyi kurmak, onun bütün varsayılanlarını kabul etmek değildir

-----

## Agno'da araç: sıradan bir fonksiyon

```py
def acilis_saati(gun: str) -> str:
    """Kafenin verilen gündeki açılış saatini verir. gun: haftanın günü, ör. pazartesi."""
    return saatler[gun]
```

- Aracın adı fonksiyonun adıdır; tarifi, ilk satırdaki üç tırnaklı metindir: **docstring**
- `gun: str` bir **tür ipucu**: "bu bilgi metin"; elle yazılan tarifteki `"type": "string"`in Python'daki karşılığı
- `-> str`: fonksiyonun metin verdiğini söyler
- `return` edilen metin modele geri gider; `print` yalnızca seni bilgilendirir
- Bilgilerin adları da tarifin parçası: `gun`, `dosya`, `yonerge` gibi adlar modele ne yazacağını anlatır

-----

## Tarif bir brif

- Bir tasarımcıya "logoyu daha modern yap" dersen o da sorar: hangi logo, ne kadar, hangi yöne?
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
- Bir stüdyoda iş dağıtan kişi "bu işi kime, neden verdim" diye not tutar; ajanın kaydı aynı alışkanlık
- Şeffaflık için de gerekli: müşteriye "bu görseli şu araç, şu yönergeyle üretti" diyebilmek

-----

## Güvenlik: her araç bir yetki

- Modele verdiğin her araç ona verdiğin bir yetkidir: görsel çizmek zararsız, dosya silmek ya da e-posta göndermek değil
- Model yanılabilir, isteği yanlış anlayabilir, okuduğu bir belgedeki bir cümleyi talimat sanabilir
- Kural: geri alınamayan işleri yapan araçlar bir insan onayından geçmeli
- Kod asistanında komutların onaysız çalışmasını kapalı tutmamızın nedeni de bu
- Ajana yalnızca işin gerektirdiği araçları ver; "belki lazım olur" diye araç ekleme
- Model karar verse de sorumluluk aracı kuran ve çalıştırandadır

-----

## Sınır ve kota

- Döngü kendiliğinden durmayabilir: model "bir düzenleme daha" der, yine beğenmez, yine düzenler
- Tasarımdaki karşılığı sonu gelmeyen revizyon; bu yüzden sözleşmeye revizyon sayısı yazılır
- Ajanın revizyon sayısı **araç çağrısı sınırıdır**: bir çalıştırmada en fazla şu kadar araç çalışsın
- Her araç çağrısı modele bir istek daha demek; görsel çizen her çağrı ayrıca bir görsel
- Konuşma büyüdükçe istekler de büyür; aynı günlük kota beklediğinden hızlı harcanır
- Sınırı işin büyüklüğüne göre seç: beklenen adım sayısı artı biraz pay

-----

## Ne zaman fazla gelir?

- Sıra her seferinde aynıysa ajan gerekmez: Konu 10'daki gibi bir hat daha ucuz, daha hızlı ve her seferinde aynı sonucu verir
- Tek bir aracın varsa karar zaten belli; modele sormak yalnızca gecikme ve hata ihtimali ekler
- Kararı basit bir kuralla verebiliyorsan (dosya yüklendiyse düzenle, yoksa çiz) bir `if` yeter
- Ajan; isteklerin serbest cümleyle geldiği, araçların çok, sıranın belirsiz olduğu yerde anlamlı
- Her model kararı bir maliyettir: kota, süre ve yanlış seçim ihtimali
- Final projesinde ajan zorunlu değil; projen sırası belli bir hatsa ajan kullanmaman doğru karar olabilir

**Sohbete yaz:** final projende sırası baştan belli olmayan bir iş var mı?

-----

## Sık yanılgılar

- "Ajan bilgisayarımda kendi başına bir şeyler çalıştırıyor." Çalıştıran, senin yazdığın ve izin verdiğin kod
- "Model aracın kodunu okuyup ne yaptığını anlıyor." Yalnızca adını, tarifini ve bilgilerini görür
- "`openai` paketini kullanıyorsam OpenAI'ye para ödüyorum." Paketin adı biçimin adı; ücreti isteğin gittiği yer belirler
- "Çerçeve kullanınca kararlar daha doğru olur." Çerçeve döngüyü yazar; kararın kalitesi modele ve tariflere bağlı
- "Ne kadar çok araç, o kadar akıllı ajan." Her araç bir seçenek ve bir yetki daha; seçim zorlaşır, risk artar
- "Sınır koymak ajanı kısıtlar." Sınır kotanı ve dosyalarını korur; işi büyükse sınırı bilerek büyütürsün

-----

## Bu konunun ödevi

**Ajanına yeni bir yetenek.**

1. Ders defterinin kopyasına kendi tasarladığın bir araç ekle: tür ipuçları, docstring, `return`
2. En az dört istek yaz; çalıştırmadan önce her biri için kendi planını yaz (hangi araçlar, hangi sırayla)
3. Ajanı çalıştır, kararlarını yazdır, planınla karşılaştır
4. Aracının tarifini bilerek boz, aynı isteği yeniden dene; sonra düzelt
5. **İki cümle:** model nerede senden ayrıştı, tarifte neyi değiştirdin?

Ayrıntılar: `odevler/odev12.md`. Puan yok; Konu 13'ün başında sıradaki arkadaşlar gösterecek. Ajan final projesi için zorunlu değil.

-----

## Hatırlanacaklar

1. **Ajan = model + araçlar + döngü.** Model karar verir, program çalıştırır, sonuç modele döner
2. **Model aracın içini görmez.** Adını, tarifini ve bilgilerini görür; tarif bir brif
3. **Çerçeve döngüyü gizler, kararı değil.** Her çalıştırmadan sonra çağrılan araçlara bak
4. **Her araç bir yetki, her çağrı bir istek.** Sınır koy; geri alınamayan işe insan onayı
5. **Sıra belliyse hat yeter.** Ajan, sırası belirsiz işler için

Sıradaki konu: **Konu 13 — Final atölyesi.** Yeni kavram yok: dönem boyunca öğrendiklerini kendi projende birleştirip çalışan bir çekirdeğe dönüştürüyorsun.
