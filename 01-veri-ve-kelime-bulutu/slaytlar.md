# Konu 1 — Veriyi Kodla İşlemek

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Geçen hafta Python'u tazeledin, bugün gerçek bir metne uyguluyoruz

- Geçen hafta: liste, sözlük, döngü ve `if` tekrarı; bir de kurulum
- İlk defterde verisini değiştirip bir grafik çizdin; o grafiğin kodunu **bu konuda** öğreneceğiz
- Bugün aynı araçlar, gerçek bir metin: bir kafeye yazılmış **30 müşteri yorumu**
- Yeni olan tek şey ölçek: gözle okunabilecek şeyi kodla saymak

-----

## Bugünün sorusu: müşteriler bu kafeyi nasıl anlatıyor?

- Kafenin görsel kimliğini yenileyeceksin; tasarıma başlamadan önce müşteriyi dinlemek istiyorsun
- 30 yorumu gözle okursun; 3000 yorum olsaydı?
- **Tahmin et, sohbete yaz:** yorumlarda en çok geçen üç kelime sence hangileri?
- Cevabı sayarak bulacağız; tahminlerine dersin ortasında döneceğiz

-----

## Bugünün yolu: beş durak

![dosya, metin, kelimeler, sayaç ve bulut adımlarını gösteren akış şeması](https://raw.githubusercontent.com/aladagemre/gita3111/main/01-veri-ve-kelime-bulutu/gorseller/akis.png)

- Dosyayı **bir kez** okuruz; her adım bir öncekinin ürettiğini kullanır

-----

## Bilgisayar "kelime" bilmez, boşluktan böler

![Ham bölmede sessiz kelimesinin dört farklı yazılışa dağılması](https://raw.githubusercontent.com/aladagemre/gita3111/main/01-veri-ve-kelime-bulutu/gorseller/ham_bolme.png)

- `yer.` ile `yer`, `Sessiz,` ile `sessiz` bilgisayar için ayrı kelimeler
- "sessiz" 8 kez geçiyor; tam bu yazılışıyla yalnızca **1** kez görünüyor
- Temizlemeden sayarsak asıl bulguyu kaçırırız
- **Sence?** Büyük harfleri küçültmek çözer mi? "İnternet" küçülünce ne olur?

-----

## Türkçe tuzağı: büyük İ küçülünce bozuluyor

![İnternet kelimesinin küçültülünce dokuz karaktere çıkması](https://raw.githubusercontent.com/aladagemre/gita3111/main/01-veri-ve-kelime-bulutu/gorseller/turkce_kucultme.png)

- Python, **İ**'yi küçültürken noktayı ayrı bir işaret olarak bırakır
- Ekranda ikisi de "internet"; sayaç ise 3 ve 1 diye ikiye böler
- Büyük **I** da noktasız ı yerine noktalı **i** olur: "Işık" → "işık"

-----

## Temizlik üç adım, sıra önemli

![Gerçek kelimelerin üç temizlik adımından geçişi](https://raw.githubusercontent.com/aladagemre/gita3111/main/01-veri-ve-kelime-bulutu/gorseller/temizlik.png)

1. İ ve I'yı **kendimiz** çeviririz
2. **Sonra** küçültürüz; sıra ters olursa İ çoktan bozulmuş olur
3. Noktalamayı **boşluğa** çeviririz; silseydik `yer.Sessiz` → `yerSessiz` olurdu

-----

## Sayaç bir sözlük: kelime anahtar, sayı değer

![Sayaç sözlüğü: dört kelime ve kaç kez geçtikleri, bir de tahmin sorusu](https://raw.githubusercontent.com/aladagemre/gita3111/main/01-veri-ve-kelime-bulutu/gorseller/sozluk.png)

- Sözlükte her **anahtarın** bir **değeri** var: "sessiz" → 8
- Değeri almak için anahtarı söylersin: "sessiz" diye sorarsan 8 gelir
- **Tahmin et:** "ilk kelime" diye 0 ile sorarsan ne olur? Cevap defterde, ilk hücreden başlayarak

-----

## Sayaç: ilk görüşte 1 yaz, sonra 1 ekle

![Gerçek bir yorumun kelime kelime sayılması, sayacın tur tur hâli](https://raw.githubusercontent.com/aladagemre/gita3111/main/01-veri-ve-kelime-bulutu/gorseller/sayac_tur.png)

- Her kelime için tek soru: "bu anahtar sayaçta var mı?"
- Yoksa 1 yazılır, varsa üstüne 1 eklenir
- Bütün yorumlar bitince elimizde 196 anahtarlı bir sözlük olur
- Defterde önce bunu **elle** yazacağız; sonra Python'un hazır sayacıyla (`Counter`) karşılaştıracağız

-----

## Elemeden önce listenin başı dilin kendisi

![En sık 10 kelime: durak kelimeler elenmeden önce ve sonra](https://raw.githubusercontent.com/aladagemre/gita3111/main/01-veri-ve-kelime-bulutu/gorseller/durak_once_sonra.png)

- **için, var, bir, ama, çok, her** her Türkçe metinde üste çıkar; kafe hakkında bir şey söylemez
- Bunlara **durak kelime** denir; hazır bir listeyle eleriz
- Eledikten sonra: **sessiz · çalışmak · yer · priz · internet · öğrenci**

-----

## Müşteriler kafeyi kahvesiyle değil, sessizliğiyle anlatıyor

![Durak kelimeler elendikten sonra 30 yorumun kelime bulutu](https://raw.githubusercontent.com/aladagemre/gita3111/main/01-veri-ve-kelime-bulutu/gorseller/bulut.png)

- Sohbete yazdığın tahminlere dön: kaç kişi "kahve" demişti?
- Bulutta "kahve" küçük; büyük olanlar **sessiz, çalışmak, yer, priz**
- Tasarım için anlamı: yeni kimlik "kahve" değil, **sessiz bir çalışma yeri** vaadi üzerine kurulabilir

-----

## Bulutta yalnızca boyut veri taşır

![Aynı sayaçtan iki kez çizilmiş iki kelime bulutu](https://raw.githubusercontent.com/aladagemre/gita3111/main/01-veri-ve-kelime-bulutu/gorseller/iki_bulut.png)

- Konum, renk ve yön rastgele; her çizimde değişir
- "sessiz ortada, demek ki önemli" ya da "priz mavi, demek ki olumlu": ikisi de yanlış okuma
- İzleyici her görsel farkın bir anlamı olduğunu varsayar; bu yanlış okumayı önlemek **tasarımcının işi**

-----

## Bulut sezdirir, çubuk grafik ölçer

![Aynı sayımın kelime bulutu ve çubuk grafik olarak yan yana gösterimi](https://raw.githubusercontent.com/aladagemre/gita3111/main/01-veri-ve-kelime-bulutu/gorseller/bulut_vs_grafik.png)

- "Bu metin genel olarak neyi anlatıyor?" → kelime bulutu
- "Hangi konu ötekinden ne kadar önde?" → çubuk grafik
- Bulutta uzun kelime daha çok yer kaplar; grafikte çalışmak, yer, priz tam eşit
- Hangisini seçeceğin izleyicine ne söylemek istediğine bağlı: bir **tasarım kararı**

-----

## Ekleri toplayınca kahve prizi geçiyor. Bulgumuz çöktü mü?

![Kahve geçen beş farklı kelimenin toplamının 6 etmesi, priz 5](https://raw.githubusercontent.com/aladagemre/gita3111/main/01-veri-ve-kelime-bulutu/gorseller/kahve_toplam.png)

- `kahve`, `kahvesi`, `kahvenin` bilgisayar için ayrı kelimeler; tek başına "kahve" yalnızca 2
- İçinde "kahve" geçenleri toplayınca **6**: priz 5'i geçiyor
- **Tahmin et, sohbete yaz:** bulgu çöktü mü, çökmedi mi? Sayı bunu söyleyebilir mi?
- Cevabı defterde yorumların kendisini okuyarak bulacağız

-----

## Şimdi deftere geçiyoruz

`ders.ipynb`, aynı yolu kodla yürüyoruz:

- **Önce (yalnız ilk oturum):** kurulum testi; herkesin ekranında **KURULUM TAMAM**
- **Isınma:** geçen dönemden iki bozuk kod; hatayı önce sen bul
- **Adım 1–2:** dosyayı aç → `metin`; böl, Türkçe küçült, noktalamayı at → `kelimeler`
- **Adım 3–5:** elle say → `sayac`; `Counter` ve `most_common`; durak kelimeleri ele → `anlamli`
- **Adım 6–8:** kelime bulutu; kahve ve ışık yorumlarını oku; çubuk grafik

-----

## Defterde takılırsan

- Çekirdek (kernel) olarak `.venv` seç; hücreyi **Shift + Enter** ile çalıştır
- Sıra önemli: atlanan hücrenin değişkeni yoktur → `NameError`
- Defter kendi klasöründe çalışır; `veri/...` bu klasörün içindeki `veri` demek
- Hata mesajında üç soru: **türü ne**, **hangi satır** (ok işareti), **tırnak içinde ne var**

-----

## Kahve çok anılıyor ama az övülüyor

![Kahve geçen altı yorumun alıntı kartları ve tonları](https://raw.githubusercontent.com/aladagemre/gita3111/main/01-veri-ve-kelime-bulutu/gorseller/kahve_yorumlar.png)

- Defterde Adım 7'de okuduk: sayı **kaç kez** geçtiğini söyler, **nasıl** geçtiğini söylemez
- Üç yorum ılık: "fena değil", "ortalama", "biraz pahalı"; kahveyi doğrudan öven **tek** yorum var
- Bulgu çökmedi, güçlendi: kimlikte kahveyi öne çıkarmak, müşterinin söylemediğini vaat etmek olur

-----

## Bulutta görünmeyen bulgu: iç mekân karanlık

![Işık geçen üç gerçek yorumun alıntı kartları](https://raw.githubusercontent.com/aladagemre/gita3111/main/01-veri-ve-kelime-bulutu/gorseller/isik_kartlar.png)

- "ışık" bulutta neredeyse görünmüyor: yalnızca 2 kez
- Okuyunca somut bir tasarım sorunu çıkıyor: çalışmaya gelinen bir yerde içerisi okumak için karanlık

> Sayma **nereye bakacağını** söyler. Bulguyu **bağlamda okuyarak** bulursun.

-----

## Bu konunun ödevi

Kendi seçtiğin bir Türkçe metinle **iki** kelime bulutu üret:

1. Durak kelimeler **elenmeden**
2. Durak kelimeler **elendikten sonra**

Sonra tek cümle yaz: eleme öncesi en büyük kelimeler neydi, sonra ne oldu?

- Metin en az 300 kelime olsun: şarkı sözü, kendi yazın, bir markanın gönderileri
- Puan yok; bir sonraki derste sıradaki arkadaşlar ekranda gösterecek

-----

## Hatırlanacak dört şey

1. **Sözlük anahtarla açılır.** "sessiz" anahtarı 8'i verir; 0 diye bir anahtar yoktur
2. **Türkçe küçültme özel iş.** Büyük İ ve I önce elle çevrilir
3. **Temizlik olmadan sonuç yanıltır.** Elenmemiş bulut metnin değil dilin fotoğrafıdır
4. **Sayı nereye bakacağını söyler.** Bulguyu kelimeyi bağlamında okuyarak bulursun

Sıradaki konu (Konu 2): kod ile internete bağlanıyoruz. Cloudflare hesabın ve anahtarın hazır olsun.
