# Konu 6 — Üretmek Ne Demek?

Bu konuda yapay zekanın hiç görmediği bir şeyi nasıl "ürettiğine" bakacağız. 136 farklı
fontta yazılmış A harfini 784 sayıdan **2 sayıya** sıkıştıracak, 2 sayıdan geri kuracak ve
bu 2 sayıyla bir **harita** çizeceksin. Sonra haritada hiçbir fontun durmadığı noktalardan
yeni A'lar üretecek, iki font arasında yürüyeceksin. Fikir şu: üretmek, öğrenilmiş bir
haritada bir nokta seçip oradan geri kurmak.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Kavram slaytları; dersin başında gösterilir |
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–8 ve Bonus |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: bozuk kodlar ve boşluklu sorular (vize biçiminde) |
| `veri/harfler.npz` | 136 fontta A, a, g ve R harfleri (28 × 28 piksel), font adları ve türleri |
| `odevler/odev6.md` | Bu konunun ödevi — iki parça |
| `ders_notu.md` | Konu notu — adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |

## Çalıştırma

Yeni kütüphane yok; NumPy, Matplotlib ve scikit-learn önceki konulardan kurulu. Yeni
konuyu almak için **`gita3111` klasöründe** bir kez:

```
git pull
uv sync
```

Sonra:

1. VS Code'da `ders.ipynb`'yi aç.
2. Sağ üstten çekirdek (kernel) olarak **`.venv`**'i seç.
3. Hücreleri yukarıdan aşağı, **Shift + Enter** ile sırayla çalıştır. Her hücre bir
   öncekinin değişkenini kullanır; atlarsan `NameError` alırsın.

## Anahtar gerekiyor mu?

Hayır. Bu konuda internete hiç çıkmıyoruz; bütün iş senin bilgisayarında.

## Beklenti

Üretilen harfler **bulanık** olacak. Amaç güzel bir font yapmak değil, üretmenin
mekanizmasını görmek.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı
(örneğin alıştırma defterini) değiştirmek istersen önce aynı klasörde **yeni bir adla
kopyala**, kopyada çalış; böylece `git pull` hiç çakışmaz.

## Defterin bölümleri

| Bölüm | Ne yapılıyor |
|---|---|
| Isınma | Bir sayı tablosunu resim olarak çizmek |
| Adım 1 | 136 fontun A'sını yüklemek ve çizmek |
| Adım 2 | Her A'yı 2 sayıya sıkıştırmak (PCA, Konu 4) |
| Adım 3 | 2 sayıdan A'yı geri kurmak |
| Adım 4 | Kaç sayı yeter? 1'den 100'e |
| Adım 5 | A'ların haritası |
| Adım 6 | Haritada bir nokta seçip yeni bir A üretmek |
| Adım 7 | Haritanın iki ekseni boyunca yürümek: eksenler ne anlatıyor? |
| Adım 8 | İki font arasında yürümek (ara değerleme) |
| Bonus | Aynı işi g, a ve R harfleriyle |

## Vize

Bu konu bitince vize verilir: evde yapılır, **yapay zeka yasak**, ardından derste kısa bir
sözlü teyit. Kapsam Konu 1–6. Soru biçimleri: kavram soruları, kod okuma, bozuk kodu
düzeltme ve boşluk doldurma.
