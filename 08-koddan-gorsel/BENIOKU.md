# Konu 8 — Koddan Görsel Üretimi

Konu 7'de `gorsel_araci.py`'yi bir arayüz gibi kullandık. Bu konuda aynı işi **kendin yazıyorsun**:
modele istek göndermek, metin olarak gelen görseli (base64) baytlara çevirip dosyaya yazmak,
dosyaya kendini anlatan bir ad vermek, aynı adın üzerine yazmamak ve hataları yakalamak. Sonunda yönergeyi
kullanıcıdan alıp görsel üreten ve düzenli bir klasöre kaydeden kendi küçük aracın olacak.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Kavram slaytları; dersin başında gösterilir |
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–9 ve Bonus |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: bozuk kodlar ve boşluklu sorular (anahtar istemez) |
| `veri/fincan.jpg` | Isınma ve alıştırmada kullanılan küçük bir görsel |
| `odevler/odev8.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu — adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |

`ciz` ve `kaydet` ile ürettiğin görseller bu klasörde `ciktilar/` içine, tarih, yönerge ve tohum taşıyan
adlarla kaydedilir. Adım 4 ve Adım 9'un dosyaları (`deneme.jpg`, `ilk.jpg`, `ilk_kucuk.jpg`) konu klasörüne yazılır.

## Çalıştırma

Yeni kütüphane yok. Yeni konuyu almak için **`gita3111` klasöründe** bir kez:

```
git pull
uv sync
```

Sonra:

1. VS Code'da `ders.ipynb`'yi aç.
2. Sağ üstten çekirdek (kernel) olarak **`.venv`**'i seç.
3. Hücreleri yukarıdan aşağı, **Shift + Enter** ile sırayla çalıştır. Her hücre bir öncekinin
   değişkenini kullanır; atlarsan `NameError` alırsın.

Isınmada ve Adım 4'te iki hücre **bilerek** hata verir (`UnicodeDecodeError`, `TypeError`); Adım 8'de
bir hücre bilerek bağlantı hatası verir. Hatayı oku, sonraki hücreye geç.

## Anahtar gerekiyor mu?

Isınma ve alıştırma defteri **anahtarsız**. Adım 1'den sonrası `anahtar.txt` ister: bütün konular
için tek dosya, `gita3111` klasöründe (Konu 2). Defterin tamamı 5 görsel üretir. Anahtarın yoksa
Adım 1–9'u yanındakiyle birlikte, onun ekranında izle.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı
değiştirmek istersen önce aynı klasörde **yeni bir adla kopyala**, kopyada çalış; böylece
`git pull` hiç çakışmaz.

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Anahtar |
|---|---|---|
| Isınma | Görseli metin gibi açmayı denemek; `"rb"`; base64 | gerekmez |
| Adım 1 | Anahtar, adres, başlık (Konu 2) | gerekir |
| Adım 2 | İsteği göndermek | gerekir |
| Adım 3 | Yanıtın içi: görsel base64 metni olarak geliyor | gerekir |
| Adım 4 | Metni baytlara çevirip `"wb"` ile dosyaya yazmak | gerekir |
| Adım 5 | `ciz` fonksiyonu; durum kodu kontrolü | gerekir |
| Adım 6 | Düzenli klasör ve kendini anlatan dosya adı (tarih, yönerge, tohum); "bu ad alınmış mı?" | gerekir |
| Adım 7 | `kaydet` fonksiyonu; yönergeyi `input` ile kullanıcıdan almak | gerekir |
| Adım 8 | Bağlantı hatasını `try` / `except` ile yakalamak | gerekir |
| Adım 9 | Görseli koddan düzenlemek | gerekir |
| Bonus | Tekrar deneme; Konu 7'nin aracını okumak; Konu 9 sorusu | yalnız 1. madde gerekir |
