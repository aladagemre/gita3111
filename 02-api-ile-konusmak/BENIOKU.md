# Konu 2 — İnterneti Koddan Konuşturmak

Bu konuda kodun bilgisayarının dışına çıkıyor: bir soruyu uzaktaki bir modele
gönderip cevabını alacaksın. Konu 1'in bulgusundan (müşteriler kafeyi sessiz bir
çalışma yeri olarak anlatıyor) yola çıkıp modele o kafenin yeni kimliğini soracaksın.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma ve Adım 1–8 |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: bozuk kodlar ve boşluklu sorular |
| `veri/renkler.csv` | Ödevin ikinci parçası için 20 renk (Konu 3'ün verisi) |
| `odevler/odev2.md` | Bu konunun ödevi — iki parça |
| `ders_notu.md` | Konu notu — adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |
| `slaytlar.md` | Kavram slaytları (görselli) — dersin ilk bölümü, defterden önce |
| `gorseller/` | Slaytlardaki şemaların PNG dosyaları |

## Çalıştırma

Dersten önce bir kez, **`gita3111` klasöründe** kütüphaneleri indir (liste
`gita3111` klasöründeki `pyproject.toml` dosyasında):

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

`ders.ipynb`'nin Adım 1'i `anahtar.txt`'yi okur; dosya yoksa
`FileNotFoundError: ... '../anahtar.txt'` hatasıyla durur, sonraki adımlar da çalışmaz.
Anahtarın henüz yoksa:

- Derste **yanındakiyle birlikte** çalış: istekleri onun ekranında izle, hücreleri sen de yaz.
- Isınma (defterin ilk bölümü) ve `alistirma.ipynb` anahtarsız çalışır.
- Kurulum yönergesinin 6. adımını (Cloudflare hesabı, `../00-hazirlik/kurulum-yonergesi.md`)
  **bugün** bitir. Ödev için kendi anahtarın gerekiyor.

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Anahtar |
|---|---|---|
| Isınma | İç içe sözlüğe kat kat inmek | gerekmez |
| Adım 1 | Anahtarı dosyadan okumak | gerekir |
| Adım 2 | İsteğin üç parçası: adres, başlık, gövde | gerekir |
| Adım 3 | İsteği göndermek, durum kodu | gerekir |
| Adım 4 | Gelen yanıta bakmak, metni çekmek | gerekir |
| Adım 5 | Kasten yanlış anahtar, 401, önce durum koduna bakmak | gerekir |
| Adım 6 | `modele_sor` fonksiyonu | gerekir |
| Adım 7 | Döngüyle birden çok soru, cevaplar `cevaplar.txt`'ye | gerekir |
| Adım 8 | Soruya bağlam yazmak cevabı nasıl değiştiriyor | gerekir |
