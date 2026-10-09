# Konu 3 — Makine Öğrenmesi Nedir?

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 2'de modele soru sorduk, bugün kendi modelimizi eğitiyoruz

![Kafe paleti: bej, sütlü kahve, adaçayı, orman yeşili, kirli beyaz](https://raw.githubusercontent.com/aladagemre/gita3111/main/03-makine-ogrenmesi/gorseller/kafe_soru.png)

- Konu 2'de hazır bir model kullandık; bugün kutuyu açıyoruz
- Veri: sınıfın Konu 2 ödevinde etiketlediği 20 renk
- Bugünün sorusu: Konu 1'deki sessiz kafenin paleti gerçekten **sakin** mi?

-----

## Kuralı ya sen yazarsın ya da model örneklerden çıkarır

![Kural yazmak ile örnekten öğrenmek](https://raw.githubusercontent.com/aladagemre/gita3111/main/03-makine-ogrenmesi/gorseller/kural_ornek.png)

- **Kural yazmak:** "şu şartta şunu de" diye sen yazarsın
- **Makine öğrenmesi:** örnekleri verirsin, kuralı model çıkarır
- Modelin örneklere bakıp öğrenmesine **eğitim** diyoruz

-----

## 20 rengin hiçbirinde sınıf oy birliğine varmadı

![Her rengin enerjik, sakin, ciddi etiket dağılımı](https://raw.githubusercontent.com/aladagemre/gita3111/main/03-makine-ogrenmesi/gorseller/dagilim.png)

- Her renk 12 kez etiketlendi; hepsinde farklı etiketler var
- Bordo ve kırık beyazda neredeyse herkes aynı şeyi demiş, kremde sınıf ikiye bölünmüş
- Bu bir hata değil; gerçek veri böyle görünür

-----

## Ekranda neredeyse aynı iki renk, sınıfta bambaşka iki karar

![Kırık beyaz ve krem, etiket dağılımlarıyla](https://raw.githubusercontent.com/aladagemre/gita3111/main/03-makine-ogrenmesi/gorseller/krem_kirik.png)

Defterde bu iki rengi canlı sayacağız: krem 5–5–2, kırık beyaz 11–1.

-----

## Anlaşmazlık bir tavan koyuyor

![Model her renge tek cevap verir; azınlıktaki etiketleri bilemez](https://raw.githubusercontent.com/aladagemre/gita3111/main/03-makine-ogrenmesi/gorseller/tavan.png)

- Model bir renge **tek** cevap verir; en iyi ihtimalle çoğunluğu söyler
- Mükemmel bir model bile her dört cevaptan birini "yanlış" bilir
- Bu yanlışlar modelin değil, sınıfın görüş ayrılığının payı

-----

## Model renk görmez, üç sayı görür

![Kırmızı rengin R, G, B değerleri: 230, 57, 70](https://raw.githubusercontent.com/aladagemre/gita3111/main/03-makine-ogrenmesi/gorseller/rgb_uc_sayi.png)

- Renk seçicide `#E63946` yazınca yanında R 230, G 57, B 70 görürsün
- Dosyada bu üç sayı hazır: `r`, `g`, `b` sütunları

-----

## X modelin baktığı şey, y tahmin etmesi gereken şey

![Veri dosyasının ilk beş satırı: X sütunları ve y sütunu](https://raw.githubusercontent.com/aladagemre/gita3111/main/03-makine-ogrenmesi/gorseller/xy_tablo.png)

- **X** = öznitelikler (üç sayı), **y** = etiket
- Her satırın X'i ile y'si aynı sırada durmalı
- Model rengin adına, nerede kullanıldığına bakmıyor

-----

## Baştaki kural sınıfın "enerjik"ini tanımıyor

![100 enerjik etiketinden kuralın yakaladığı 8 tanesi](https://raw.githubusercontent.com/aladagemre/gita3111/main/03-makine-ogrenmesi/gorseller/kural_sonuc.png)

- Kural yalnızca kırmızıyı tanıyor
- Sınıfın "enerjik"i çok daha geniş: sıcak tonların neredeyse hepsi
- Bu genişlik kimsenin kuralında yoktu; verinin içinde zaten var

-----

## Veriyi ikiye bölüyoruz: eğitim ve test

![240 satırın 180'i eğitime, 60'ı teste ayrılıyor](https://raw.githubusercontent.com/aladagemre/gita3111/main/03-makine-ogrenmesi/gorseller/bolme.png)

- Aynı örneklerle eğitip aynı örneklerle sınarsak **ezberi** ölçeriz
- Test satırlarını model hiç görmez; ölçüm orada yapılır
- Derste çözülen sorunun aynısıyla sınav yapılmaz

-----

## En yakın komşular: en benzer 5 örnek ne dediyse onu de

![Test rengi bal ve en yakın beş eğitim satırının etiketleri](https://raw.githubusercontent.com/aladagemre/gita3111/main/03-makine-ogrenmesi/gorseller/knn.png)

- "Benzer" burada üç sayının birbirine yakın olması demek
- Her renk 12 kez geçtiği için model çoğu zaman **aynı rengi etiketleyen beş arkadaşa** soruyor
- Kaç komşu? k=1 → 0.70, k=5 → 0.77, k=15 → 0.73

-----

## Üç sayı: kör tahmin, model, tavan

![Kör tahmin 0.45, model 0.77, tavan 0.80](https://raw.githubusercontent.com/aladagemre/gita3111/main/03-makine-ogrenmesi/gorseller/uc_sayi.png)

- **Kör tahmin:** hiç düşünmeden hep en sık etiketi ("enerjik") söylemek
- Model kör tahmini açık farkla geçiyor; tavana iki cevap kalıyor
- Başka bölmelerde doğruluk 0.65 ile 0.78 arasında oynuyor: tek sayıya güvenme

-----

## Yanlışların çoğu azınlık görüşü

![Modelin 14 yanılgısı: 12'si azınlık görüşü, 2'si çoğunluktan ayrılma](https://raw.githubusercontent.com/aladagemre/gita3111/main/03-makine-ogrenmesi/gorseller/yanilgilar.png)

- Model bir **çoğunluk sesi** üretir; azınlığın algısını siler
- Azınlık yanılgılarının yarısında öğrenci sıcak toprak tonlarına "ciddi" demiş
- Hedef kitlen o azınlıksa model sana yanlış yol gösterir

-----

## Veri arttıkça doğruluk yükseliyor, sonra düzleşiyor

![Öğrenme eğrisi: 18, 45, 90, 135, 180 örnekle test doğruluğu](https://raw.githubusercontent.com/aladagemre/gita3111/main/03-makine-ogrenmesi/gorseller/ogrenme_egrisi.png)

- Düzleştiği yerden sonra aynı türden veri eklemek pek işe yaramıyor
- Gereken **başka türlü** veri: daha çok renk, rengin kullanıldığı yer
- Ortadaki düşüş hata değil; ödevde konuşacağız

-----

## Kafe paleti için ikinci görüş

![Kafe paletinin beş rengi, modelin cevabı ve en yakın bildiği renk](https://raw.githubusercontent.com/aladagemre/gita3111/main/03-makine-ogrenmesi/gorseller/kafe_cevap.png)

- Sıcak nötrler (bej, sütlü kahve) "sakin" değil, "enerjik" tarafta
- Bejin kararını kremi etiketleyenler veriyor; krem sınıfın en tartışmalı rengi
- Bu bir kesinlik değil, "kullanıcıyla sına" işareti

-----

## Hiç görmediği bir renk gelince ne oluyor?

![Kırık beyazı görmüş ve hiç görmemiş iki modelin cevabı](https://raw.githubusercontent.com/aladagemre/gita3111/main/03-makine-ogrenmesi/gorseller/gorulmemis.png)

- Rastgele bölmede her renk eğitimde de vardı; bu kolay bir sınav
- Yeni bir renk gelince model sayıları ona en yakın **bildiği** renklerin etiketini söyler
- Sonucu söylerken sorulan soruyu da söyle: bilinen renk mi, yeni renk mi?

-----

## RGB'de yakın, gözde uzak

![Gri maviye gül kurusu RGB'de orta maviden daha yakın](https://raw.githubusercontent.com/aladagemre/gita3111/main/03-makine-ogrenmesi/gorseller/rgb_yakin.png)

- Gri maviyi hiç görmeyen model ona gül kurusunun etiketini veriyor
- Model "benzerlik"i rengi hangi sayılarla verdiğimizden (**temsilden**) alıyor
- Konu 4'ün sorusu: sayılardaki yakınlık bizim "benzer" dediğimiz şeyi yakalıyor mu?

-----

## Şimdi deftere geçiyoruz: `ders.ipynb`

Hücreleri yukarıdan aşağı sırayla çalıştır (**Shift + Enter**).

- **Isınma:** sayaç neyi sayıyor?
- **Adım 1–2:** veriyi oku, krem ve kırık beyazı say, X ve y'yi kur
- **Adım 3–4:** eğitim/test böl, modeli eğit, kör tahminle kıyasla
- **Adım 5–6:** yanıldığı renkler, öğrenme eğrisi
- **Adım 7–8:** kafe paletini sor, kırık beyazı dışarıda bırak
- **Bonus:** kendi rengini sor

-----

## Bu konunun ödevi

Defterde Adım 6'nın çıktısına bak: **yarısıyla** (90 örnek) ve **tamamıyla** (180 örnek) eğitilen model.

1. İki doğruluk oranını yaz
2. Öğrenme eğrisini `veri-miktari.png` olarak kaydet
3. Tek cümle: fark ne, neden böyle olmuş olabilir?

Puan yok; Konu 4'ün başında birkaç kişi ekranını paylaşıp gösterecek.

-----

## Hatırlanacaklar

- **Öznitelik ve etiket:** modelin baktığı şey X, tahmin etmesi gereken şey y; aynı sırada olmalı
- **Eğitim ve test:** model test verisini hiç görmez; görürse ölçtüğün şey ezber olur
- **Yanılma normaldir, ölçülür:** doğruluğu kör tahmin ve tavanla kıyasla
- **Test hangi soruyu soruyor?** Bilinen renklerde 0.77, hiç görülmemiş renklerde 0.60

Konu 4'te rengin yerine kelimeleri sayıya çevireceğiz; "en yakın komşu" fikri orada da var.
