# Konu 9 — Ölçek: Toplu Üretim

Bu konuda arayüzün yapamadığı işi yapıyoruz: bir şablon ve iki listeyle (3 stil × 4 renk)
12 görseli tek seferde üretmek. Döngüden önce kota hesabı yapacak, küçük bir denemeyle (3 görsel)
sınırın çalıştığını göreceksin. Yazdığın kod, başarısız bir isteği bekleyip yeniden deneyecek ve var olan
görselleri atlayıp kaldığı yerden devam edecek. Her görselin nasıl üretildiğini bir JSON günlüğüne yazacak,
hepsini tek bir kontak sayfasında yan yana koyacaksın. Son olarak görselleri, görsel anlayan (çok kipli) bir
modele okutup brife ne kadar uyduklarını soracaksın.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Kavram slaytları; dersin başında gösterilir |
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–7 ve Bonus |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: bozuk kodlar ve boşluklu sorular (anahtar istemez, görsel üretmez) |
| `uretim.py` | Yardımcı dosya: `ciz` (Konu 8'de yazdığınla aynı işi yapar) ve `gorsele_sor` (görsel anlayan modele soru sormak) |
| `odevler/odev9.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu — adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |

Görseller bu klasörde `izgara/` içine (`suluboya_adacayi.jpg` gibi), kontak sayfası
`kontak_sayfasi.png`'ye, günlük `uretim_gunlugu.json`'a yazılır.

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

Defterin kopyası `uretim.py` ile **aynı klasörde** durmalı; yoksa
`ModuleNotFoundError: No module named 'uretim'` alırsın.

## Anahtar gerekiyor mu?

Isınma, Adım 1 ve Adım 2 anahtarsız; alıştırma defteri de. Adım 3'ten sonrası `anahtar.txt` ister
(bütün konular için tek dosya, `gita3111` klasöründe). Defterin tamamı 12 görsel (Bonus ile en fazla 17)
üretir ve 13 kez görsel anlayan modele soru sorar. Anahtarın yoksa yanındakiyle birlikte, onun ekranında izle.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı
değiştirmek istersen önce aynı klasörde **yeni bir adla kopyala**, kopyada çalış; böylece
`git pull` hiç çakışmaz.

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Anahtar |
|---|---|---|
| Isınma | İç içe döngüyle kombinasyonları saymak | gerekmez |
| Adım 1 | Şablon: yönerge sözlükleri ve kartlar | gerekmez |
| Adım 2 | Kota hesabı ve güvenlik sınırı | gerekmez |
| Adım 3 | Araç; bekleyip yeniden deneyen çizim (`sabirli_ciz`) | gerekir |
| Adım 4 | Üretim döngüsü: önce 3 görsellik deneme, sonra kalanı; var olanı atla, sınırda dur | gerekir |
| Adım 5 | Üretim günlüğü: kartları JSON'a yazmak ve geri okumak | gerekmez |
| Adım 6 | Kontak sayfası; kendi seçimin | gerekmez |
| Adım 7 | Görselleri görsel anlayan modele okutup puanlatmak | gerekir |
| Bonus | Tohum ekseni; sınırın çalıştığını görmek | gerekir |
