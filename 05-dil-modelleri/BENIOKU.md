# Konu 5 — Dil Modelleri Nasıl Çalışır?

Bu konuda bir dil modelinin metni nasıl yazdığına bakacağız: metni parçalara (belirteçlere)
nasıl böldüğüne, sıradaki parçayı nasıl tahmin ettiğine ve **sıcaklık** ayarının bu seçimi
nasıl değiştirdiğine. Önce Konu 1'in kafe yorumlarından, yalnızca sayarak, minicik bir
"sonraki kelime" modeli kuracaksın; sonra aynı fikri gerçek modelde, üç sıcaklıkta slogan
üreterek deneyeceksin.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Kavram slaytları; dersin başında gösterilir |
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–7 ve Bonus |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: bozuk kodlar ve boşluklu sorular (anahtar istemez) |
| `veri/kafe-yorumlari.txt` | Konu 1'deki 30 kafe yorumu (aynı dosya); Adım 2–5'in verisi |
| `odevler/odev5.md` | Bu konunun ödevi — iki parça |
| `ders_notu.md` | Konu notu — adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |

## Çalıştırma

Dersten önce bir kez, **`gita3111` klasöründe** kütüphaneleri indir (liste
`gita3111` klasöründeki `pyproject.toml` dosyasında; bu konunun yenisi `tiktoken`):

```
cd gita3111
uv sync
```

Sonra:

1. VS Code'da `ders.ipynb`'yi aç.
2. Sağ üstten çekirdek (kernel) olarak **`.venv`**'i seç.
3. Hücreleri yukarıdan aşağı, **Shift + Enter** ile sırayla çalıştır. Her hücre bir
   öncekinin değişkenini kullanır; atlarsan `NameError` alırsın.

`tiktoken` ilk çalıştırmada (Adım 1) internetten bir sözlük dosyası indirir; birkaç saniye
sürer. Dosya bilgisayarın geçici dosyalar klasöründe durur; o klasör temizlenmedikçe yeniden
inmez. İnternet yoksa Adım 1 `ConnectionError` verir; Adım 2–5 sözlüğü kullanmadığı için
oradan devam edebilirsin.

## Anahtar gerekiyor mu?

Isınma ve Adım 1–5 **anahtarsız** çalışır. Adım 6 ve 7 gerçek modele soru sorar ve
`anahtar.txt` ister. Bu dosya bütün konular için tek dosya: konu klasöründe değil, bir üstte,
`gita3111` klasörünün içinde durur (Konu 2). Anahtarın yoksa Adım 6–7'yi yanındakiyle
birlikte, onun ekranında izle.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı
(örneğin alıştırma defterini) değiştirmek istersen önce aynı klasörde **yeni bir adla
kopyala**, kopyada çalış; böylece `git pull` hiç çakışmaz.

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Anahtar |
|---|---|---|
| Isınma | Cümle tamamlama cevaplarını `Counter` ile saymak | gerekmez |
| Adım 1 | Metni belirteçlere ayırmak; Türkçe ile İngilizceyi kıyaslamak | gerekmez |
| Adım 2 | "biraz" ve "çok" kelimelerinden sonra ne geldiğini bulmak | gerekmez |
| Adım 3 | Sayıları olasılığa çevirmek, çubuk grafik | gerekmez |
| Adım 4 | Hep en olası kelimeyi seçerek metin üretmek | gerekmez |
| Adım 5 | Zar atarak metin üretmek | gerekmez |
| Adım 6 | Gerçek model, üç sıcaklıkta aynı soru | gerekir |
| Adım 7 | Slogan panosu: `pano.txt` | gerekir |
| Bonus | Kendi adını belirteçlere ayırmak; başka bir kelimeden üretmek; bir bulguyu soruya koymak | 1–2 gerekmez, 3 gerekir |
