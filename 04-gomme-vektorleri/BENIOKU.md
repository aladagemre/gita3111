# Konu 4 — Temsil ve Gömme Vektörleri

Bu konuda kelimeleri sayıya çevireceğiz. Konu 3'te bir renk üç sayıydı; burada bir
kelime yüzlerce sayı olacak. Sonra bu sayılara bakarak hangi kelimenin hangisine
benzediğini ölçecek ve kelimelerin haritasını çizeceğiz.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–8 ve Bonus |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: bozuk kodlar ve boşluklu sorular (anahtar istemez) |
| `odevler/odev4.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu: adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |

## Çalıştırma

Dersten önce bir kez, **`gita3111` klasöründe** kütüphaneleri indir. Liste
`gita3111` klasöründeki `pyproject.toml` dosyasında. Bu konu yeni bir kütüphane istemiyor;
Konu 2'nin `requests`'i ve Konu 3'ün `scikit-learn`'ü yeterli:

```
cd gita3111
uv sync
```

Sonra:

1. VS Code'da `ders.ipynb`'yi aç.
2. Sağ üstten çekirdek (kernel) olarak **`.venv`**'i seç.
3. Hücreleri yukarıdan aşağı, **Shift + Enter** ile sırayla çalıştır. Her hücre bir
   öncekinin değişkenini kullanır; atlarsan `NameError` alırsın.

`anahtar.txt` bütün konular için tek dosya: konu klasöründe değil, bir üstte,
`gita3111` klasörünün içinde durur. Defter onu `"../anahtar.txt"` yoluyla okur
(`..` = bir üst klasör).

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı
(örneğin alıştırma defterini) değiştirmek istersen önce aynı klasörde **yeni bir adla
kopyala**, kopyada çalış; böylece `git pull` hiç çakışmaz.

## Anahtarın yoksa ne olacak?

Isınma ve `alistirma.ipynb` anahtarsız, internetsiz çalışır. Adım 1'den sonrası
`anahtar.txt` ister; dosya yoksa Adım 1 `FileNotFoundError: ... '../anahtar.txt'`
hatasıyla durur. Anahtarın henüz yoksa derste bu adımları **hocanın paylaştığı ekrandan** izle ve kurulum
yönergesinin 6. adımını (`../00-hazirlik/kurulum-yonergesi.md`) bugün bitir; ödev için
kendi anahtarın gerekiyor.

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Anahtar |
|---|---|---|
| Isınma | Altı kelimeye elle iki sayı vermek, haritasını çizmek, benzerliği ölçmek | gerekmez |
| Adım 1 | Anahtarı dosyadan okumak (Konu 2'nin aynısı) | gerekir |
| Adım 2 | Bir kelimenin vektörünü modelden almak | gerekir |
| Adım 3 | `vektor_al` fonksiyonu | gerekir |
| Adım 4 | İki kelime ne kadar benzer? | gerekir |
| Adım 5 | 24 kelimelik sözlük | gerekir |
| Adım 6 | "kafe"ye en yakın 3 kelime (sen yazıyorsun) | gerekir |
| Adım 7 | Yüzlerce sayıyı 2'ye indirip harita çizmek | gerekir |
| Adım 8 | Haritayı okumak: kümeler, zıt anlamlılar | gerekir |
| Bonus | Kendi 5 kelimeni haritaya eklemek | gerekir |
