# Konu 10 — Afiş yarın matbaada: son kontrol

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Basıldıktan sonra fark edilen hata

- Afiş asıldı; biri "yanlız" kelimesinin fotoğrafını çekip paylaşıyor
- Tarih doğru, yanındaki gün yanlış: insanlar bir gün erken gelip kapıyı kapalı buluyor
- Saat hiç yazılmamış; herkes "kaçta?" diye mesaj atıyor ya da hiç gelmiyor
- Açık sarı bir satır ekranda güzel duruyordu; duvarda, üç adım öteden okunmuyor
- Matbaadan çıkmış hata geri alınmaz: yeniden baskı, yeniden para, kaçan etkinlik
- Dijitalde de iz kalır: gönderiyi düzeltsen bile ekran görüntüsü dolaşır
- Soru: senin ya da tanıdığın birinin başına geldi mi? Hangi hata?

-----

## Son kontrol neden zor?

- Kendi yazdığın metni okurken beynin ne yazdığını bildiği için okumaz, tamamlar
- Saatlerce baktığın bir afişte göz alışır; eksik olanı görmez
- Kontrol listesi uzun: yazım, tarih, gün, saat, yer, iletişim bilgisi, renk, ölçü, taşma payı
- Teslim gecesi yorgunsun ve acelen var; yorgun göz hatayı daha kolay kaçırır
- Müşteri de bakar; ama hatayı onun bulması senin için iyi bir haber değildir
- Bir tasarımcının önerisi: işini müşteriden önce sen denetle, hatayı ilk sen gör
- Bu konuda bu kontrolün sıkıcı ve tekrar eden kısmını bir programa veriyoruz

-----

## Üretim hattı nedir?

- Bir matbaadaki prova masasını düşün: afiş masadan masaya geçer
- Her masada biri yalnızca tek bir şeye bakar: biri yazıya, biri tarihe, biri renge
- Her masa notunu yazar; sonunda bütün notlar tek bir raporda toplanır
- Bir masa o gün kapalıysa ötekilerin notları kaybolmaz; masa açılınca yalnız oraya bakılır
- Programdaki karşılığı: birkaç adımın arka arkaya çalıştığı, her adımın sonucunu sakladığı program
- Adımların bazısı yapay zekâ, bazısı sıradan Python
- Hattın gücü tekrarında: aynı hat yarın başka bir afişi, öbür gün yirmi afişi aynı özenle denetler

-----

## Hangi masaya kim oturur?

- Görseldeki yazıyı okumak: **model**. Python bir görselde yalnızca piksel görür, harf görmez
- Türkçe yazım hatası, eksik bilgi: **model**. Dil bilgisi ve bağlam gerekir
- Tarih ile gün tutuyor mu: **Python**. Bu bir takvim hesabı
- Yazı zeminde okunuyor mu: **Python**. Bu bir renk formülü
- Dosyanın ölçüsü, çözünürlüğü, adı: **Python**. Bunlar dosyanın içinde yazılı
- Kural: Python'un yapabildiğini Python yapar; model yalnızca Python'un yapamadığı yerde
- Neden? Python'un cevabı her seferinde aynıdır, bedavadır ve kotadan yemez

-----

## Model neden takvim bilmez?

- Dil modeli hesap yapmaz; bir sonraki kelimeyi tahmin eder (Konu 5)
- "Şu tarih hangi gün?" sorusunda doğru gün de, yanlış gün de akıcı bir cümle olarak gelir
- Bazen tutturur, bazen tutturamaz; hangisi olduğunu cevaba bakarak anlayamazsın
- Aynı soruyu iki kez sorduğunda iki farklı cevap alabilirsin
- Python'un takvimi ise yüz kez sorsan yüz kez aynı günü verir
- Tasarımcılar bunu yaşayarak biliyor: Figma'nın 2025 anketinde yapay zekâ çıktısına güvenebildiğini söyleyenler üçte birin biraz altında
- Bu yüzden hattın güvenilir olması gereken yerlerine model değil, hesap koyuyoruz

-----

## Ara çıktı: masanın notu

- Ara çıktı, bir adımın işi bitince dosyaya kaydedilen sonucudur
- Kotayı korur: afiş bir kez okunur, hattı yeniden çalıştırınca modele yeniden sorulmaz
- Ücretsiz hesabın her gün bir sınırı var; boşa giden her istek o sınırdan yer
- Zamanı korur: görsel okuyan model bir cevap için uzun süre düşünebilir
- Denetlenebilir: modelin afişte ne okuduğunu dosyayı açıp kendi gözünle görürsün
- Düzeltilebilir: model bir satırı yanlış okuduysa dosyada düzeltirsin, hat senin metninle sürer
- Matbaadaki karşılığı: imzalı prova çıktısı. "Neyi onayladık?" sorusunun cevabı odur

-----

## Bir halka koparsa

- İnternet kesilir, sunucu meşgul olur, model boş bir cevap döner; bunlar sık olur
- İlk kural: hemen pes etme. Birkaç saniye bekle, yeniden sor
- İkinci kural: sonsuza kadar deneme. Üç denemeden sonra dur ve söyle
- Üçüncü kural: başarısızlığı başarı gibi kaydetme. Boş cevabı dosyaya yazan hat, ertesi gün o boşluğu gerçek sanır
- Dördüncü kural: sessiz geçme. Raporda "bu kontrol yapılamadı" yazsın
- Ara çıktı sayesinde hat kaldığı yerden devam eder: biten adımlar yeniden yapılmaz
- Gündelik karşılığı: kargo teslim edilemeyince firma paketi atmaz; not bırakır, ertesi gün yeniden dener

-----

## Okunurluk: kontrast

- Kontrast oranı, yazı ile zemininin açıklık farkını ölçen bir sayıdır: 1 aynı renk, 21 beyaz üstüne siyah
- Web erişilebilirlik kuralları (WCAG): küçük yazı için en az 4,5; büyük başlık için en az 3
- Bilgi taşıyan çizim ve simgeler için de en az 3; yalnız süs olan öğeler için eşik yok
- Ölçü rengin tonuna değil açıklığına bakar: iki "farklı" renk aynı açıklıkta olabilir
- Ekranda güzel görünen açık sarı ya da açık gri, projeksiyonda ve güneş altında ilk kaybolan yazıdır
- Renk körlüğü olan biri kırmızıyla yeşili ayırt edemeyebilir ama açıklık farkı yüksek yazıyı okur
- Bir bilgiyi yalnızca renkle verme ("kırmızılar iptal"); yanına bir kelime ya da işaret ekle
- Hızlı deneme: afişi gri tonlamaya çevir; okunmayan satır, kontrastı düşük olandır

-----

## Sektörde bu iş

- Bir yazılım ajansında bir tasarımcı kendi Figma eklentilerini yazmış; biri kontrast denetliyor
- Onun sözüyle bu eklenti "günlerce süren işi dakikalara indiriyor"
- Ortak noktaları: tekrar eden, hacimli, aynı kurala göre yapılan işler
- Programlama bilmeyen tasarımcılara Python ile afiş tasarlamayı öğreten dersler var (ör. Letterform Archive)
- Adobe'nin 2026 araştırmasına göre yapay zekâ en çok işin başında (fikir) ve sonunda (rötuş, renk düzeltme) kullanılıyor
- Son kontrol tam bu "son" kısma giriyor: yaratıcı karar senin, angarya programın
- Kendi küçük aracını yazabilen tasarımcı, aynı denetimi her seferinde elle yapmak zorunda kalmaz

-----

## Sık yanılgılar

- "Model her şeyi kontrol eder." Hatayı kaçırabilir, okurken düzeltebilir, doğru bir kelimeyi de "düzeltmeye" kalkabilir
- "Rapor temizse afiş temizdir." Hat yalnızca baktığı şeyi bulur; hiyerarşi, boşluk, hizayı denetlemez
- "Python ölçtüyse doğrudur." Ölçüm doğrudur; ama bir rengin yazı mı süs mü olduğunu bilmez
- "Kontrast yüksekse tasarım iyidir." Okunur olmak gerekli ama yetmez
- "Her şeyi modele sormak daha kolay." Daha yavaş, kotadan yer ve her cevabı ayrıca denetlemen gerekir
- "Bir hata çıkınca hattı baştan çalıştırmak gerekir." Ara çıktı varsa yalnızca bozulan adım yeniden yapılır

-----

## Sorumluluk kimde?

- Afiş senin imzanı taşır; "program kontrol etti" demek hatanın sorumluluğunu kaldırmaz
- Hat bir yardımcıdır, son göz değil: raporu oku, afişe yeniden bak, sonra gönder
- Modelin her önerisi yalnızca bir öneridir; kabul ya da ret kararı tasarımcınındır
- Müşterinin henüz yayımlanmamış işini bir sunucuya gönderiyorsun; içinde kişisel bilgi varsa önce sor
- Telefon numarası, adres, kişi adı gibi bilgileri gereksiz yere modele gönderme
- Erişilebilirlik bir incelik değil, saygıdır: afişi yalnız iyi gören genç gözler okumayacak
- Bir hatayı hat bulduysa raporu müşteriye de gösterebilirsin: neyi denetlediğin görünür olur

-----

## Sırada: hattın hafızası

- Bugünkü hat afişi denetliyor ama müşterini tanımıyor
- Sayfa Kahve kendine "kafe" değil "çalışma evi" diyor; turuncu renk kullanmıyor; saatin mutlaka yazmasını istiyor
- Bu kurallar WhatsApp'ta, e-postada, toplantı notunda dağınık duruyor; her afişte hepsini hatırlamak zor
- Konu 11'de hatta bir hafıza vereceğiz: müşterinin notlarını saklayan ve soruya en yakın notu bulan bir arama
- Konu 12'de bu araçları kendi seçip sıraya koyan bir asistan kuracağız
- Ödev 10: kendi müşterinin bir afişini hattan geçir; raporu ve düzelttiğin hâlini getir
