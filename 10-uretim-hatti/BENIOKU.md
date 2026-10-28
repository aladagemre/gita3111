# Konu 10 — Zincirleme: Üretim Hattı

Bu konuda önceki konularda ayrı ayrı öğrendiğin adımları tek bir programda birleştiriyoruz. Bir ayarlar dosyası
(`ayarlar.json`) hattın brifini ve bütün ayarlarını taşıyor. Metin modeli konuya üç slogan yazıyor, görsel modeli her slogana
bir görsel üretiyor. Yazdığın hat biten işi yeniden üretmiyor ve kopan bir halkayı kayda geçirip devam ediyor; hattın üretim
günlüğü `uretim.json`'a yazılıyor. Bonus'ta sloganları ve görselleri yan yana gösteren bir pano çıkıyor.

Konu yarım oturum sürüyor: aynı oturumun ilk yarısı Konu 9 (video).

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Kavram slaytları; konunun başında gösterilir |
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–7 ve Bonus |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: kendi yazacağın bir soru, bozuk kodlar ve boşluklu sorular (anahtar istemez, internete çıkmaz) |
| `ayarlar.json` | Hattın ayarlar dosyası: çalışma adı, konu, stil, slogan sayısı, sıcaklık, tohum |
| `halkalar.py` | Yardımcı dosya: `modele_sor` (Konu 5) ve `sabirli_ciz` (Konu 8) hazır |
| `odevler/odev10.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu — adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |

Hattın bütün çıktıları `ciktilar/` içinde, adı `ayarlar.json`'daki `calisma` alanından gelen bir klasöre yazılır
(derste `ciktilar/kafe_afisi_1/`): `sloganlar.json`, `gorsel_1.jpg` ..., `uretim.json` ve Bonus'ta `pano.png`.
Alıştırma defteri `alistirma_ciktilari/` klasörünü kullanır.

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

Defterin kopyası `halkalar.py` ve `ayarlar.json` ile **aynı klasörde** durmalı; yoksa
`ModuleNotFoundError: No module named 'halkalar'` ya da `FileNotFoundError: ... 'ayarlar.json'` alırsın.

## Anahtar gerekiyor mu?

Isınma, Adım 1 ve Adım 2 anahtarsız; alıştırma defteri de. Adım 3'ten sonrası `anahtar.txt` ister
(bütün konular için tek dosya, `gita3111` klasöründe). Defterin tamamı 4 metin ve 3 görsel isteği gönderir
(Bonus 2 ile 4 görsel); Adım 6'da bilerek reddedilen 3 görsel isteği de var. Hepsi ücretsiz günlük kotanın küçük bir kısmı.
Anahtarın yoksa yanındakiyle birlikte, onun ekranında izle.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı (defter ya da `ayarlar.json`)
değiştirmek istersen önce aynı klasörde **yeni bir adla kopyala**, kopyada çalış; böylece `git pull` hiç çakışmaz.
`ciktilar/` klasörü depoya girmez; içindekileri istediğin gibi değiştirebilirsin.
Derste `ayarlar.json`'u doğrudan değiştirdiysen ve `git pull` bu dosya yüzünden hata verirse, `gita3111` klasöründe
`git checkout 10-uretim-hatti/ayarlar.json` dosyayı depodaki hâline döndürür.

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Anahtar |
|---|---|---|
| Isınma | Sahte halkalarla bir zincir | gerekmez |
| Adım 1 | Ayarlar dosyası: `ayarlar.json`'u okumak | gerekmez |
| Adım 2 | Çalışma klasörü; neden otomatik tarih yok | gerekmez |
| Adım 3 | Hazır halkalar; bir deneme sloganı ve temizleme | gerekir |
| Adım 4 | 1. halka: sloganlar; ara çıktıyı saklamak | gerekir |
| Adım 5 | 2. halka: yönergeler ve görseller | gerekir |
| Adım 6 | Bir halkayı bilerek koparmak: hat durmuyor | gerekir |
| Adım 7 | Üretim günlüğü: `uretim.json` | istek yok; Adım 4–6 gerekir |
| Bonus | Pano: slogan ve görsel yan yana; ara çıktıya elle dokunmak | 2. bölüm gerekir |
