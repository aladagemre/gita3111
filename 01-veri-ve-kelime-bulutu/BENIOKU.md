# Konu 1 — Veriyi Kodla İşlemek

Bu klasörde ne var:

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: ısınma, Adım 1–8 ve bir bonus |
| `alistirma.ipynb` | Derste kendi başına çözeceğin alıştırma: beş bozuk kod, sonra boşluk doldurma |
| `veri/` | Üzerinde çalışacağımız metinler ve Türkçe durak kelime listesi |
| `odevler/odev1.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu: her adımın nedeni, sık hatalar, kendini dene soruları — derste kaçırdığın yer olursa buraya bak |

## Çalıştırma

Dersten önce bir kez, terminalde `gita3111` klasöründe kütüphaneleri indir:

```
cd gita3111
uv sync
```

Bu konunun kütüphaneleri (`wordcloud`, `matplotlib`) `gita3111` klasöründeki `pyproject.toml`
dosyasında yazılı; `uv sync` onları `gita3111/.venv` ortamına kurar. Sonra:

1. VS Code'da `ders.ipynb`'yi aç.
2. Sağ üstten **çekirdek** (kernel) olarak `.venv` seç.
3. Hücrelere sırayla tıklayıp **Shift + Enter** ile çalıştır.

Hücreler birbirinin değişkenini kullanır; atlarsan `NameError` alırsın.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı
(örneğin bir defteri) değiştirmek istersen önce aynı klasörde **yeni bir adla
kopyala** (ör. `alistirma.ipynb` → `benim_alistirmam.ipynb`), kopyada çalış; böylece
`git pull` hiç çakışmaz.

## Bu konuda ne üreteceksin

Bir metin dosyasından kelime bulutu. Önce kelimeleri sayacağız, sonra işe yaramaz
kelimeleri eleyeceğiz, sonra görseli üreteceğiz. Sonunda bulutun göremediği şeylere
(ekler, bağlam) bakıp aynı sonucu bir çubuk grafikle çizeceğiz.

## Defterin bölümleri

| Bölüm | Ne zaman |
|---|---|
| Isınma | Konunun başında, geçen dönemin iki hatası |
| Adım 1–6 | Derste birlikte, sırayla: dosyayı aç, temizle, say, sırala, ele, bulut |
| Adım 7–8 | Derinleşme: ekli kelimeleri toplamak, kelimeyi yorumların içinde okumak; çubuk grafik |
| Bonus | Aynı defter, kafenin kendi gönderileriyle |

Erken bitirirsen: `alistirma.ipynb`, sonra defterin sonundaki bonus.
