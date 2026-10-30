# Konu 8 — Bir haftalık gönderi seti

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Bir sosyal medya tasarımcısının haftası

- Cuma akşamı müşteriden bir tablo gelir: önümüzdeki haftanın beş günü, her gün için bir başlık ve görselde ne olacağı
- Pazartesi sabahına kadar her gün için bir **gönderi** ve aynı görselden bir **hikâye** istenir: on dosya
- On dosya da aynı markadan geldiği belli olacak kadar tutarlı olmalı: renk, teknik, yazı tipi, ses
- Müşteri hepsini tek bakışta görmek ister; biri olmamışsa (ya müşteri söyler ya sen fark edersin) yalnızca o günü yenilersin
- İşin yaratıcı kısmı kararlardır ve küçüktür; büyük kısmı tekrardır: üret, indir, şablona koy, başlığı yaz, ölçüye uyarla, doğru adla kaydet
- Bugün böyle bir haftayı baştan sona yapıyoruz; örnek müşterimiz Sayfa Kahve, üniversitenin yanındaki sessiz bir çalışma kafesi
- Ödevde aynı işi kendi seçtiğin bir müşteriyle yapacaksın: bir öğrenci kulübü, ailenin dükkânı, kendi markan; Konu 12'ye kadar onunla çalışacaksın

-----

## İçerik takvimi: haftanın tablosu

- **İçerik takvimi**, bir markanın ne zaman neyi paylaşacağını gösteren plandır; bir derginin yayın planı ya da bir ders programı gibi
- Çoğu zaman bir tablodur: her satır bir gün; sütunlarda gün, başlık ve görselin tarifi; bazen saat, platform ve not
- Takvimi bazen müşteri, bazen ajansın içerik ekibi yazar; küçük işlerde tasarımcının kendisi
- Tablo, müşteriyle tasarımcının aynı şeye baktığı bir anlaşmadır: hangi gün ne çıkacak, ikisi de bilir
- Tasarımcı için iyi haber: tablo bir yapıdır ve yapıyı bilgisayar okuyabilir
- Bir tabloyu satır satır okuyup her satıra aynı işi yapmak sıradan bir betiğin en iyi yaptığı iştir; yapay zekâ gerekmez
- Yapay zekânın girdiği tek yer, satırdaki tarifi görsele çevirmektir

-----

## Sektörde bu iş

- Türkiye'deki sosyal medya ve grafik tasarım ilanları görseli, kısa dikey videoyu (Reels, Shorts) ve platform ölçülerini birlikte istiyor
- İlanlarda adı geçen araçlar: Midjourney, Adobe Firefly, Photoshop'un üretken dolgusu, Runway, Kling, Gemini, ChatGPT
- Bazı ilanlar "yapay zekâ kullanıyorum" demeyi yeterli bulmuyor; onunla gerçekten üretilmiş iş görmek istiyor: portfolyo
- Adobe'nin 2025'te 16.000'den fazla içerik üreticisiyle yaptığı ankette yapay zekâ en çok düzenleme ve büyütmede (%55), sonra görsel üretiminde (%52) kullanılıyor
- Bir yazılım satıcısının anketine göre görsel yeniden boyutlandıran tasarımcıların %85'i bu işte zorlanıyor
- Bir marka ajansı en büyük darboğazının tasarım değil, tekrar eden idari işler olduğunu anlatıyor
- Kod yazan tasarımcılar da var: bir ajansta bir tasarımcı tekrar eden işler için dokuz Figma eklentisi yazmış; kontrast denetleyen eklentisinin günlerce süren bir işi dakikalara indirdiğini söylüyor

-----

## Arayüzde on kez, kodda bir döngü

- Arayüzde her gün için aynı hareketler: yönergeyi yaz, üret, indir, şablona koy, başlığı yaz, dikey ölçüye uyarla, doğru adla kaydet
- Beş günde bu otuzu aşkın hareket eder, revizyonla daha fazlası; her biri bir dalgınlık fırsatı: yanlış başlık, yanlış dosya adı, unutulmuş hikâye
- Kodda bu hareketler bir kez yazılır ve tablonun her satırına aynen uygulanır
- **Yapay zekâ** yalnızca bir betiğin yapamadığı işi yapar: "pencere kenarında bir fincan" tarifini görsele çevirmek
- **Python** geri kalanını yapar: tabloyu okumak, başlığı yazmak, ölçüye uyarlamak, dosyayı adlandırmak, onay sayfasını kurmak, kaydı tutmak
- Python bu işleri her seferinde aynı ve hatasız yapar, kota da harcamaz; model ise başlığın harflerini bile güvenilir çizemez
- Kural: bir işi sıradan bir betik yapabiliyorsa onu yapay zekâya verme

-----

## Marka dili: set bir aile gibi durmalı

- **Marka dili**, bir markanın her işinde tekrar eden renk, teknik, doku, yazı tipi ve sestir; logoyu görmeden markayı tanıtan şey
- Haftalık set müşterinin sayfasında yan yana durur; biri kopuksa hemen göze batar
- Müşterinin kılavuzu marka dilini yazıya döker: Sayfa Kahve için mürekkep mavisi ve kâğıt beyazı, kırmızı ve turuncu asla, iki renkli risograf baskı, insan yüzü yok, fısıltı gibi bir ses
- D&AD'nin 2026 raporu uyarıyor: kendi hâline bırakılan yapay zekâ ortalamaya kayar; sana "herhangi bir kafe" görseli verir
- Kuralı yönergeye yazmak da garanti değil: model kendi alışkanlığına kayıp kılavuzun yasakladığı bir rengi ya da bir yüzü yine ekleyebilir
- Seti tutarlı yapan model değil, senin kararların: hangi kural yönergeye girer, hangi görsel elenir, hangisi yenilenir
- Tasarımcıların şüphesi de gerçek: İngiltere'de yapılan bir ankette tasarımcıların %81'i yapay zekânın yaratıcılığı körelttiğini düşünüyor
- Bu derste yapay zekâ yaratıcılığın yerine değil angaryanın yerine giriyor; fikir ve seçim sende kalıyor

-----

## Stil cümlesi: stil referansının koddaki hâli

- Arayüzlerde tutarlılık için bir **stil referansı** görseli yüklersin; model her yeni görselde ona benzemeye çalışır
- Kodda karşılığı **stil cümlesi**: kılavuzu görsel modelinin anlayacağı dile çevirdiğin, her yönergenin sonuna eklenen sabit bir cümle
- Yönerge = günün sahnesi + stil cümlesi; sahne her gün değişir, stil cümlesi hiç değişmez
- Kurarken önce Türkçe üç-dört öbek yaz (renk ve teknik; biçim ve doku; boşluk; ne olmayacak), sonra her öbeği İngilizceye çevir
- "Ne olmayacak" da kılavuzdan gelir: yazı yok, insan yüzü yok, parlak yüzey yok
- Yaşayan bir sanatçının adını stil olarak yazma; sevdiğin üslubun özelliklerini yaz (Konu 7)
- Stil cümlesi bütün sete aynı uygulanır; sonradan değiştirirsen bütün haftayı yeniden üretirsin, o yüzden karar baştan verilir

-----

## Aynı yönerge, başka görsel: neden dosyayı saklarız

- Görsel modeli her üretimde rastgele bir gürültüden başlar (Konu 7); gürültü her seferinde başka olduğu için aynı yönerge başka bir görsel verir
- Bazı modeller **tohum** kabul eder: gürültüyü belirleyen sayıyı sabitlersen aynı görsel geri gelir; Konu 7'de böyle yaptık
- Bu konuda kullandığımız model şu anki hâliyle tohum kabul etmiyor (30 Ekim 2026): her istek yeni bir görsel demek
- Sonuç: tutarlılığı tohum değil stil cümlesi sağlar; her seferinde başka ama aynı aileden bir görsel gelir
- Beğendiğin bir görseli yeniden üreterek geri alamazsın; bir fotoğraf karesi gibi, o an bir kez olur
- Bu yüzden dosyayı saklarsın: yeni denemeyi eskisinin üstüne değil, yeni bir adla kaydedersin ("Çarşamba_gonderi_2.jpg")
- Araçlar değişir; bugün tohum alan bir model yarın almayabilir. İş akışını buna dayanıklı kur: dosya ve kayıt senin elinde kalsın

-----

## Yazıyı yapay zekâ değil, tasarımcı koyar

- Görsel modelleri harfleri de resim gibi çizer: kelimeler bozulur; ş, ğ, ı, İ gibi harfler sık sık yanlış çıkar
- Fontu, puntoyu, rengi ve hizayı sen seçemezsin; kılavuzun yazı kuralları uygulanamaz
- Başlık değişince görseli baştan üretmen gerekir: hem kota hem tutarlılık gider
- Çözüm, tasarım programlarındaki **şablon** mantığı: görsel bir katman, yazı ayrı bir katman
- Kodda model yazısız görsel üretir (yönergede "no text"), başlığı Python seçtiğin fontla, kılavuzdaki renkle, ölçülü bir şeride yazar
- Böylece başlık değişikliği sıfır istekle biter; yazımdan ve dilden yine sen sorumlusun
- Serbest lisanslı ve Türkçe harfleri olan bir font seç; teslim ettiğin işte fontun lisansı da hesaba girer

-----

## Bir kez üret, çok kez uyarla

- Aynı içerik farklı yerlerde farklı ölçü ister: akışta dikey gönderi (4:5, 1080 × 1350), hikâyede tam ekran (9:16, 1080 × 1920), bazen kare kapak ya da yatay afiş
- Her ölçü için yeniden üretmek kota harcar ve görselin kendisini değiştirir; set dağılır
- Doğrusu görseli bir kez üretip ölçülere yerleştirmek; bu, bilgisayarın hesapla yaptığı bir iş
- Her ölçünün kendi kuralı var: hikâyede ekranın üst şeridinde profil adı, alt şeridinde yanıt kutusu durur; başlık oraya girmemeli
- Kılavuzun kuralları da hesaba girer: Sayfa Kahve'de yazı görselin en fazla beşte birini kaplar
- Yeniden boyutlandırma tasarımcıların en sevmediği işlerden; kodda bir kez yazılınca her gün ve her ölçü için aynı çalışır
- "Kare de istiyorum" diyen müşteriye cevap yeni bir üretim değil, aynı görselin yeni bir yerleşimidir

-----

## Kota bir bütçedir

- Ücretsiz katmanın günlük bir hakkı var: **kota**; her görsel üretimi ondan harcar, yazı ve ölçü harcamaz
- Matbaadaki kâğıt gibi düşün: baskıya girmeden önce kaç tabaka gideceğini hesaplarsın
- Hesap basit: kaç gün, o kadar üretim; hikâye ve kapak eklemek sayıyı değiştirmez
- Revizyon da bütçeden yer: bütün haftayı yeniden üretmek beş istek, tek günü yenilemek bir istek
- Bağlantı kopabilir ya da sunucu yoğun olabilir; sabırlı bir betik bekleyip yeniden dener, set yarım kalmaz
- Ücretli bir serviste kota paradır; bu alışkanlık müşterinin bütçesiyle çalışırken de geçerli
- Çalıştırmadan önce sayıyı söyle: "bu döngü beş görsel üretecek"

-----

## Onay sayfası ve üretim günlüğü

- **Onay sayfası**: setin küçük hâlleri, adlarıyla, tek sayfada; fotoğrafçıların kontak baskısı, ajansların sunum panosu gibi
- Müşteri tutarlılığı ancak yan yana görünce değerlendirebilir
- Dosya adı yazılıysa geri bildirim netleşir: "Çarşamba_gonderi.jpg olmamış"; hangi dosyayı değiştireceğin karışmaz
- **Üretim günlüğü**: her üretimin zamanı, günü, yönergesi ve dosyası, bir tabloda
- Günlük revizyonların hafızasıdır: "ilki daha iyiymiş" denirse hangi dosyanın ilk deneme olduğu ve hangi yönergeyle üretildiği oradadır
- Günlükten satır silinmez, eklenir; yeniden üretimler de kayda girer
- Aynı zamanda şeffaflığın kanıtı: hangi görselin nasıl üretildiğini müşteriye ve portfolyonda gösterebilirsin

-----

## Şeffaflık ve telif

- Müşteriye görsellerin yapay zekâyla üretildiğini söyle; teklifte ya da sözleşmede yaz
- Müşteriler sınır koyabiliyor: Adobe'nin 2026 araştırmasında, yapay zekâyla üretilmiş insan görselini taslakta serbest bırakıp son reklamda yasaklayan müşteriler anlatılıyor
- Yapay zekâ çıktısının kime ait olduğu birçok ülkede tartışmalı; insan katkısı olmayan bir görselin telifle korunmadığı yerler var
- Senin katkın görünür olsun: stil cümlesi, seçim, yerleşim, yazı, revizyon
- Başka markaların logolarını ve ürünlerini, yaşayan sanatçıların adlarını yönergeye koyma
- Adobe'nin 2025 araştırmasında yaratıcı profesyonellerin %45'i nihai işte yapay zekâya asla tam güvenmeyeceğini söylüyor; teslimden önce her görseli sen kontrol et: eller, nesneler, yazıya benzeyen lekeler
- Üretim günlüğü şeffaflığın kaydıdır

-----

## Bu konunun ödevi

Kendi müşterini seç: bir öğrenci kulübü, ailenin dükkânı, kendi markan ya da bir arkadaşının işletmesi. Konu 12'ye kadar onunla çalışacaksın.

1. Müşterin için **5 günlük** bir içerik takvimi yaz: gün, başlık, sahne (sahne İngilizce ve yazısız)
2. Müşterinin görsel dilinden bir **stil cümlesi** kur
3. Haftanın gönderilerini ve hikâyelerini üret; teslim: **onay sayfası, takvim, üretim günlüğü**
4. **Üç cümle:** stil cümleni nasıl kurdun, ilk denemede ne tutmadı, nasıl düzelttin?
5. İstersen bunun yerine **logo teslim paketi**: logonu müşterinin istediği ölçülere ve açık/koyu zemine yerleştiren bir döngü (anahtar istemez)

Ayrıntılar: `odevler/odev8.md`. Puan yok; Konu 9'un başında sıradaki arkadaşlar gösterecek.

Sıradaki konu: **Konu 9 — Gönderini hareketlendir.** Bu haftanın yazısız görsellerinden birini kısa bir videoya çevireceğiz; yazıyı ve logoyu yine sonradan biz koyacağız.
