# Konu 4 — Temsil ve Gömme Vektörleri

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Konu 3'te bir renk üç sayıydı; bugün bir kelime yüzlerce sayı olacak

![Kırmızı üç sayıya, kahve yüzlerce sayıya dönüşüyor](https://raw.githubusercontent.com/aladagemre/gita3111/main/04-gomme-vektorleri/gorseller/temsil_seridi.png)

- Konu 3: kırmızı = `[230, 57, 70]`; model benzer renkleri bu üç sayıdan buldu
- Sorun da gördük: gri mavi ile gül kurusu sayılarda yakın, gözümüzde uzak
- Benzerlik, şeyi hangi sayılarla temsil ettiğimize bağlı

-----

## Bilgisayar her şeyi sayıya çevirerek temsil eder

| Şey | Temsili |
|---|---|
| Renk | 3 sayı (R, G, B) |
| Fotoğraf | her piksel için 3 sayı |
| Ses | saniyede binlerce sayı |
| Kelime | **?** |

Bugünün sorusu: Konu 1'in müşterileri kafeyi **sessiz bir çalışma yeri** diye anlattı.
Bir dil modeli "kafe" kelimesini hangi kelimelere yakın buluyor?

-----

## Önce elle: iki eksenli bir mood-board

![Beş kelimenin sıcaklık ve enerji haritası; kahve soru işareti](https://raw.githubusercontent.com/aladagemre/gita3111/main/04-gomme-vektorleri/gorseller/isinma_haritasi.png)

- **sıcaklık:** soğuk −1 … sıcak +1 · **enerji:** sakin −1 … canlı +1
- Her kelime iki sayı. Böyle bir sayı listesine **vektör** diyoruz
- **Sohbete yaz:** sen kahveye hangi iki sayıyı verirdin? Tek doğru yok: temsil bir **seçim**

-----

## Her kelime ortadan çıkan bir ok

![Merkezden altı kelimeye çizilmiş oklar](https://raw.githubusercontent.com/aladagemre/gita3111/main/04-gomme-vektorleri/gorseller/oklar.png)

- Biz kahveye `[0.6, 0.4]` verdik: sağ üste bakıyor, sıcak ve biraz canlı
- Ateş de sağ üste bakıyor, yalnızca oku daha uzun
- Deniz sol alta bakıyor: ateşin tam tersi

-----

## Benzerlik okların yönüne bakar, uzunluğuna değil

![Buz–kar 0.93 aynı yön, ateş–çay 0.11 neredeyse dik, ateş–deniz −1 zıt yön](https://raw.githubusercontent.com/aladagemre/gita3111/main/04-gomme-vektorleri/gorseller/benzerlik_yon.png)

- **1** aynı yön · **0** dik, ilgisiz · **−1** zıt yön
- Kar okunun boyu buzunkinden kısa, yine de 0.93: uzunluk sayılmıyor
- Bu sayıyı hazır bir araç veriyor: `cosine_similarity` (scikit-learn, Konu 3). Benzerlik büyükse iki kelime "yakın"

-----

## Tahmin et: kahve çaya mı benzer, buza mı?

![Kahve, çay ve buzun okları; iki benzerlik soru işareti](https://raw.githubusercontent.com/aladagemre/gita3111/main/04-gomme-vektorleri/gorseller/kahve_tahmin.png)

- Oklara bak: hangi ikili daha çok aynı yöne bakıyor?
- **Sohbete yaz:** hangisi büyük çıkar, hangisi eksi?
- Cevabı defterin ısınmasında sen hesaplayacaksın

-----

## Mood-board'da eksenleri biz seçtik; model kendisi buluyor

![Solda adlı iki eksen, sağda adsız yüzlerce eksen](https://raw.githubusercontent.com/aladagemre/gita3111/main/04-gomme-vektorleri/gorseller/yuzlerce_eksen.png)

- Dil modeli milyonlarca metin okur, kelimeleri bir haritaya yerleştirir
- 2 eksen değil **yüzlerce**; hiçbirinin adı yok
- Kelimeyi vektöre çevirmeye **gömme** (embedding) diyoruz. Kaç sayı? Kendi çıktında göreceksin

-----

## En yakın komşu: skorları büyükten küçüğe sırala

![Denizin skorları Counter ile sıralanıyor: kar ve buz en yakın](https://raw.githubusercontent.com/aladagemre/gita3111/main/04-gomme-vektorleri/gorseller/komsular.png)

- Bir kelimeye en yakın kelimelere **komşu** diyoruz
- Her kelimenin hedefle benzerliğini bir sözlüğe yaz: `skorlar`
- Konu 1'in `Counter`'ı sözlüğü büyükten küçüğe dizer: denizin komşuları kar ve buz

-----

## Defterde 24 kelime, 4 grup: "kafe" kime yakın çıkacak?

![Renkler, duygular, tasarım, mekânlar: altışar kelime](https://raw.githubusercontent.com/aladagemre/gita3111/main/04-gomme-vektorleri/gorseller/kelime_gruplari.png)

- **Tahmin et ve not al:** kafeye en yakın üç kelime hangileri?
- Kütüphaneye mi yakın, parka mı, sahneye mi?
- **bej:** Konu 3'te kafe paleti için modele sorduğumuz renk

-----

## Yüzlerce sayı kâğıda sığmaz: gölgesini çizeriz

![Konu 3'ün 20 rengi: 3 sayıdan 2 sayılık haritaya](https://raw.githubusercontent.com/aladagemre/gita3111/main/04-gomme-vektorleri/gorseller/renk_golgesi.png)

- **PCA** (Temel Bileşen Analizi) çok sayıyı en çok şey anlatan 2 sayıya indirir
- Bir heykelin duvara düşen gölgesi gibi: PCA, heykeli en iyi tanıtan açıyı arar
- Konu 3'ün renklerinde gölge şekli iyi koruyor: açıklar sağda, koyular solda

-----

## Harita bir özettir, bilgi kaybeder

![Kırmızı ile tarçın haritada gerçekte olduğundan yakın](https://raw.githubusercontent.com/aladagemre/gita3111/main/04-gomme-vektorleri/gorseller/bilgi_kaybi.png)

- Haritada yan yana duran iki nokta (renk ya da kelime) gerçekte o kadar yakın olmayabilir
- Emin olmak için asıl sayıya bak: benzerliği ölç
- Şehir haritası gibi: yolu bulmana yeter, binaların yüksekliğini göstermez

-----

## Şimdi deftere geçiyoruz

`ders.ipynb`, hücreleri yukarıdan aşağı **Shift + Enter** ile.

- **Isınma** — slayttaki haritayı sen çiz, kahve tahminini ölç, kahveye kendi sayılarını ver (anahtarsız)
- **Adım 1–3** — anahtarı oku, bir kelimenin vektörünü al, `vektor_al` fonksiyonu
- **Adım 4** — kahve çaya mı benzer, tipografiye mi?
- **Adım 5** — 24 kelimelik sözlük
- **Adım 6** — "kafe"ye en yakın 3 kelime: **sen yazıyorsun**
- **Adım 7** — PCA ile harita
- **Adım 8** — haritayı oku: kümeler; huzur öfkeye mi yakın, sakinliğe mi?

-----

## Adım 6 — Sen yaz: "kafe"ye en yakın 3 kelime

1. `skorlar` adında boş bir sözlük kur
2. Her kelime için "kafe" ile benzerliğini hesapla, `skorlar[kelime]` olarak sakla
3. Konu 1'in `Counter`'ı ile en büyükleri sırala

İpucu, Konu 1'den: `for kelime, adet in sayac.most_common(10):`

**5 dakika.** Sonra birlikte bakalım.

-----

## Adım 8'den sonra: benzer, eşanlamlı demek değil

![Huzur, öfke, neşe, hüzün aynı boşluğa giriyor](https://raw.githubusercontent.com/aladagemre/gita3111/main/04-gomme-vektorleri/gorseller/ayni_bosluk.png)

- Ekranına bak: huzur–öfke, huzur–sakinlikten ne kadar geride kaldı?
- Model anlamı sözlükten değil, kelimenin **hangi cümlelerde geçtiğinden** öğrenir: zıtlar aynı boşluğa girer
- Mood-board için "huzur"a yakın kelimeler istersen araya öfke de girebilir

-----

## Bu konunun ödevi

Kendi seçtiğin **20 kelimeyle** bir harita çıkar.

1. Defteri kopyala, Adım 5'teki listeye kendi 20 kelimeni yaz
2. Adım 7'nin sonuna kadar çalıştır, haritayı kaydet
3. **Tek cümle:** beklemediğin hangi iki kelime yan yana düştü?
4. **Tek cümle daha:** bu haritayla bir mood-board'a başlasan neyi ekler, neyi çıkarırdın?

Ayrıntılar: `odevler/odev4.md`. Puan yok; Konu 5'in başında sıradaki arkadaşlar gösterecek.

-----

## Hatırlanacaklar: üç kavram, üç cümle

**Vektör (gömme).** Model bir kelimeyi bir sayı listesine çevirir; sayıların tek tek
anlamı yok, anlam kelimelerin birbirine göre nerede durduğunda.

**Benzerlik.** Aynı yöne bakan iki vektör benzerdir: 1 aynı yön, 0 ilgisiz, −1 zıt.
Modelin "benzer"i, "benzer yerlerde geçen" demek.

**Boyut indirgeme.** Yüzlerce sayıyı 2'ye indirip haritaya çizebiliriz; ama harita bir
özettir, bilgi kaybeder.

-----

## Sonraki konu: Konu 5

**Dil modelleri nasıl çalışır?**

Bu konuda model kelimeleri sayıya çevirdi.
Konu 5'te modelin **metni nasıl yazdığına** bakacağız:

- Metin önce parçalara bölünür
- Model her seferinde bir sonraki parçayı tahmin eder
- "Sıcaklık" ayarı, modelin en olası parçayı mı seçeceğini yoksa zar mı atacağını belirler
