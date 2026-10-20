# Konu 10 — Video Üretimi

Bu konuda görsele zaman ekliyoruz: kısa video klipler. Önce bir videonun kaça mal olduğunu hesaplayacak,
arayüzden bir klip üreteceksin. Sonra konunun yeni fikrini önce internetsiz, sahte bir işle öğreneceksin:
**uzun süren iş.** İsteği başlat, iş numarasını sakla, arada bir "bitti mi?" diye sor (bir sınıra kadar), bitince indir.
Ardından aynı şeyi gerçek hizmetle yapıp bir yönergeden ve Konu 9'daki görselinden iki video üretecek,
ikisini de defterde izleyecek ve maliyetleriyle birlikte bir günlüğe kaydedeceksin.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Kavram slaytları; dersin başında gösterilir |
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–8 ve Bonus |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: bozuk kodlar ve boşluklu sorular (anahtar istemez, internete çıkmaz, klip üretmez) |
| `video.py` | Yardımcı dosya: `anahtarlari_oku`, sahte iş (`sahte_baslat`, `sahte_durum`) ve bütün adımları tek fonksiyonda yapan `video_uret` |
| `veri/yedek_fincan.jpg` | Konu 9'un görseli yoksa görselden video için kullanılan yedek görsel |
| `odevler/odev10.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu — adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |

Videolar bu klasörde `videolar/` içine (`metinden.mp4`, `gorselden.mp4`), günlük `video_gunlugu.json`'a yazılır.

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

Defterin kopyası `video.py` ile **aynı klasörde** durmalı; yoksa
`ModuleNotFoundError: No module named 'video'` alırsın.

## Anahtar gerekiyor mu?

Isınma, Adım 1 ve Adım 2 anahtarsız; alıştırma defteri de. Adım 3'ten sonrası `anahtar.txt`'de (`gita3111` klasöründe)
iki yeni satır ister; derste dağıtılır:

```
VIDEO_ADRES = https://...
VIDEO_KOD = ...
```

Videolar hocanın hesabından, bir **aracı hizmet** üzerinden üretilir; `VIDEO_KOD` sana özel ve klip hakkını onunla sayar.
Kimseyle paylaşma, ödevle gönderme. Defter 2 klip üretir (4'er saniye, 720p); Bonus ile 3. Başlatma hücrelerini
**bir kez** çalıştır: her çalıştırma yeni bir klip ve yeni bir ücret demek.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı
değiştirmek istersen önce aynı klasörde **yeni bir adla kopyala**, kopyada çalış; böylece
`git pull` hiç çakışmaz.

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Anahtar |
|---|---|---|
| Isınma | Bir video kaç para: süre ve fiyat, yarı fiyatına, video ile görsel | gerekmez |
| Adım 1 | Arayüzden bir klip (kod yok) | kendi öğrenci hesabın |
| Adım 2 | Sahte işle: başlat, iş numarası, aralıklarla sor, zaman aşımı | gerekmez |
| Adım 3 | Video kodunu oku | gerekir |
| Adım 4 | Gerçek işi başlat | gerekir |
| Adım 5 | Aralıklarla sor: `bekle` fonksiyonu | gerekir |
| Adım 6 | İndir ve defterde izle | gerekir |
| Adım 7 | Görselden video (Konu 9'un görseli) | gerekir |
| Adım 8 | Üretim günlüğü ve toplam maliyet | gerekmez |
| Bonus | Dikey video; iş numarasıyla yeniden sormak | gerekir |
