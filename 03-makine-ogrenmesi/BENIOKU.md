# Konu 3 — Makine Öğrenmesi Nedir?

Bu konuda kendi modelimizi eğiteceğiz. Veri: Konu 2'nin ödevinde senin ve arkadaşlarının
etiketlediği renkler. Konu tek bir derse sığmayabilir; bölünürse `ders_notu.md`'de
kaldığın adımdan devam et.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–8 ve Bonus |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: bozuk kodlar ve boşluklu sorular |
| `veri/renkler-etiketli.csv` | Sınıfın etiketleri, tek dosyada (`hex,ad,r,g,b,ogrenci,etiket`) |
| `odevler/odev3.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu — adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |

## Çalıştırma

Dersten önce bir kez, **`gita3111` klasöründe** kütüphaneleri indir (liste
`gita3111` klasöründeki `pyproject.toml` dosyasında; `scikit-learn` büyük, indirme biraz sürüyor):

```
cd gita3111
uv sync
```

Sonra:

1. VS Code'da `ders.ipynb`'yi aç.
2. Sağ üstten çekirdek (kernel) olarak **`.venv`**'i seç.
3. Hücreleri yukarıdan aşağı, **Shift + Enter** ile sırayla çalıştır. Her hücre bir
   öncekinin değişkenini kullanır; atlarsan `NameError` alırsın.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı
(örneğin alıştırma defterini) değiştirmek istersen önce aynı klasörde **yeni bir adla
kopyala**, kopyada çalış; böylece `git pull` hiç çakışmaz.

## Defterin bölümleri

| Bölüm | Ne yapılıyor |
|---|---|
| Isınma | Sayaç neyi sayıyor? Sessiz bir hatayı bulmak |
| Adım 1 | Sınıfın verisi; bir rengin etiketlerini saymak |
| Adım 2 | Rengi sayıya çevirmek (X ve y) |
| Adım 3 | Veriyi ikiye bölmek: eğitim ve test |
| Adım 4 | Modeli eğitmek, kör tahminle kıyaslamak |
| Adım 5 | Modelin yanıldığı renkler ve grafiği |
| Adım 6 | Veri arttıkça doğruluk: öğrenme eğrisi |
| Adım 7 | Model ne öğrendi? Kafe paletini sormak |
| Adım 8 | Hiç görmediği bir renkte sınamak |
| Bonus | Kendi seçtiğin rengi sormak |
