# Konu 11 — Zincirleme: Üretim Hattı

Bu konuda önceki konularda ayrı ayrı öğrendiğin adımları tek bir programda birleştiriyoruz. Bir brif dosyası
(`ayarlar.json`) hattın bütün ayarlarını taşıyor. Metin modeli konuya üç slogan yazıyor, görsel modeli her slogana bir görsel
üretiyor; istersen (Bonus) bir görsel videoya çevriliyor. Yazdığın hat biten işi yeniden üretmiyor ve kopan bir halkayı kayda
geçirip devam ediyor. Sonunda sloganları ve görselleri yan yana gösteren bir pano çıkıyor; hattın bütün kaydı da `uretim.json`'a yazılıyor.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Kavram slaytları; dersin başında gösterilir |
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–8 ve Bonus |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: bozuk kodlar ve boşluklu sorular (anahtar istemez, internete çıkmaz) |
| `ayarlar.json` | Hattın brif dosyası: konu, stil, slogan sayısı, sıcaklık, tohum, video açık mı |
| `halkalar.py` | Yardımcı dosya: `modele_sor` (Konu 5), `sabirli_ciz` (Konu 9) ve `video_uret` (Konu 10) hazır |
| `odevler/odev11.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu — adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |

Hattın bütün çıktıları `ciktilar/` içinde, adı `ayarlar.json`'daki `calisma` alanından gelen bir klasöre yazılır
(derste `ciktilar/kafe_afisi_1/`): `sloganlar.json`, `gorsel_1.jpg` ..., `pano.png`, `uretim.json`.

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
(Bonus 1 ile 4 görsel); Adım 6'da bilerek reddedilen 3 görsel isteği de var. Video (Bonus 2) varsayılan olarak kapalı; açarsan `anahtar.txt`'deki
Konu 10 satırları (`VIDEO_ADRES`, `VIDEO_KOD`) da gerekir. Anahtarın yoksa yanındakiyle birlikte, onun ekranında izle.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı (defter ya da `ayarlar.json`)
değiştirmek istersen önce aynı klasörde **yeni bir adla kopyala**, kopyada çalış; böylece `git pull` hiç çakışmaz.
`ciktilar/` klasörü depoya girmez; içindekileri istediğin gibi değiştirebilirsin.
Derste `ayarlar.json`'u doğrudan değiştirdiysen (ör. Bonus 2'de `"video": true`) ve `git pull` bu dosya yüzünden
hata verirse, `gita3111` klasöründe `git checkout 11-uretim-hatti/ayarlar.json` dosyayı depodaki hâline döndürür.

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Anahtar |
|---|---|---|
| Isınma | Sahte halkalarla bir zincir; istek hesabı | gerekmez |
| Adım 1 | Brif dosyası: `ayarlar.json`'u okumak | gerekmez |
| Adım 2 | Çalışma klasörü; neden otomatik tarih yok | gerekmez |
| Adım 3 | Hazır halkalar; bir deneme sloganı ve temizleme | gerekir |
| Adım 4 | 1. halka: sloganlar; ara çıktıyı saklamak | gerekir |
| Adım 5 | 2. halka: yönergeler ve görseller | gerekir |
| Adım 6 | Bir halkayı bilerek koparmak: hat durmuyor | gerekir |
| Adım 7 | Kayıt: `uretim.json`; eksikleri bulmak | gerekmez |
| Adım 8 | Pano: slogan ve görsel yan yana; kendi seçimin | gerekmez |
| Bonus | Ara çıktıya elle dokunmak; 3. halka: video | gerekir |
