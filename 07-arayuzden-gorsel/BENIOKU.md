# Konu 7 — Görsel Üretimi: Yönergeden Görsele

Bu konuda bir görsel üreticiyi tasarımcı gözüyle yönetmeyi öğreneceğiz: yönergeyi parçalarına
ayırmak, **tohumla** rastgeleliği sabitlemek, adım sayısının görseli nasıl değiştirdiğini
görmek, bir seferde tek bir şeyi değiştirerek **kontrollü deney** yapmak, iki modeli
karşılaştırmak ve var olan bir görseli talimatla düzenlemek. Bu konuda yeni kod yazmıyoruz: hazır
bir aracı (`gorsel_araci.py`) arayüz gibi kullanıyor, defterin hücrelerinde yalnızca metinleri ve sayıları
değiştiriyoruz; aracın içini Konu 8'de açacağız.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Kavram slaytları; dersin başında gösterilir |
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–8 ve Bonus |
| `gorsel_araci.py` | Görsel üretim aracı: `ciz`, `duzenle`, `yan_yana`. İçini Konu 8'de açacağız |
| `odevler/odev7.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu — adım adım açıklamalar, etik ve telif, sık hatalar, kendini dene soruları, sözlükçe |

Ürettiğin görseller bu klasörde `ciktilar/` içine numarayla kaydedilir (`001.jpg`, `002.jpg`...).

## Çalıştırma

Yeni kütüphane yok. Yeni konuyu almak için **`gita3111` klasöründe** bir kez:

```
git pull
uv sync
```

Sonra:

1. VS Code'da `ders.ipynb`'yi aç.
2. Sağ üstten çekirdek (kernel) olarak **`.venv`**'i seç.
3. Hücreleri yukarıdan aşağı, **Shift + Enter** ile sırayla çalıştır.

Defterin kopyası `gorsel_araci.py` ile **aynı klasörde** durmalı; yoksa
`ModuleNotFoundError: No module named 'gorsel_araci'` alırsın.

## Anahtar gerekiyor mu?

Isınma anahtarsız. Adım 1'den sonrası `anahtar.txt` ister: bütün konular için tek dosya,
`gita3111` klasöründe (Konu 2). Defterin tamamı yaklaşık 25 görsel üretir; Cloudflare'in
ücretsiz günlük kotasının küçük bir kısmı. Anahtarın yoksa yanındakiyle birlikte, onun
ekranında izle.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı
değiştirmek istersen önce aynı klasörde **yeni bir adla kopyala**, kopyada çalış; böylece
`git pull` hiç çakışmaz. `gorsel_araci.py`'yi değiştirme: Konu 8'de birlikte açacağız.

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Anahtar |
|---|---|---|
| Isınma | Yönergeyi beş parçadan kurmak: özne, ortam, stil, ışık, kompozisyon | gerekmez |
| Adım 1 | Aracı almak; ilk görsel | gerekir |
| Adım 2 | Aynı yönerge iki kez; sonra aynı tohumla iki kez | gerekir |
| Adım 3 | Gürültüden görsele: 1, 2, 4, 8 adım | gerekir |
| Adım 4 | Kontrollü deney: yalnızca stil, sonra yalnızca ışık | gerekir |
| Adım 5 | Kısa ve net yönerge ile uzun ve çelişkili yönerge | gerekir |
| Adım 6 | Türkçe ve İngilizce yönerge | gerekir |
| Adım 7 | İki model: flux ve sdxl; negatif yönerge, en ve boy | gerekir |
| Adım 8 | Görsel düzenleme: var olanı talimatla değiştirmek | gerekir |
| Bonus | Kendi brifinle stil panosu | gerekir |

## Arayüzden de yapabilirsin

Aynı ilkeler (net yönerge, tek değişken, yan yana karşılaştırma) sohbet asistanlarının görsel
üretiminde, Adobe Firefly'da, Canva'da da geçerli. Arayüzler tohum gibi bazı ayarları gizler;
defterde hepsi elinin altında ve her görsel bir dosya olarak kaydediliyor.
