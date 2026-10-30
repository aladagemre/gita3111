# Konu 10 — Afiş yarın matbaada: son kontrol

Bir afişi matbaaya ya da Instagram'a göndermeden önceki son kontrolü yapan küçük bir **üretim hattı** kuracaksın.
Hat, Sayfa Kahve'nin "Sessiz Okuma Gecesi" afişindeki yazıları bir yapay zekâ modeline okutur, yazım hatası ve eksik
bilgi için bir metin modeline sorar, tarihle günün tutup tutmadığını ve yazı renklerinin okunup okunmadığını Python'la
hesaplar ve bütün bulguları tek bir rapora yazar. Modelin önerilerinden hangisini kabul edeceğine sen karar verirsin. Her adımın sonucu bir dosyada saklanır; internet kesilse bile hat
kaldığı yerden devam eder. Sonunda aynı hattı kendi müşterinin afişiyle çalıştırırsın.

Konu yarım oturum sürüyor: aynı oturumun ilk yarısı Konu 9 (video).

| Dosya / klasör | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Konunun başında gösterilen slaytlar |
| `ders.ipynb` | Derste birlikte çalıştırdığımız defter: Isınma, 5 adım ve kısa bir Bonus |
| `alistirma.ipynb` | Kendi başına çözeceğin defter: "model mi, Python mı?" soruları, bozuk kodlar, boşluklar (anahtar istemez, internete çıkmaz) |
| `halkalar.py` | Hattın hazır parçaları: `afisi_oku`, `modele_sor`, `gun_adi`, `renkleri_cikar`, `kontrast` ve dosya işlemleri |
| `veri/afis.jpg` | Denetleyeceğimiz afiş (içinde bilerek bırakılmış hatalar var) |
| `veri/afis_temiz.jpg` | Aynı afişin düzeltilmiş hâli |
| `odevler/odev10.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu: adım adım açıklama, sık hatalar, kendini dene, sözlükçe |

Hattın çıktıları `ciktilar/sayfa_kahve/` içine yazılır: `okunan.txt`, `yazim.txt`, `rapor.md`. Alıştırma defteri
`alistirma_ciktilar/` klasörünü kullanır. İki klasör de depoya girmez.

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

Defter `halkalar.py` ile aynı klasörde durmalı; yoksa `ModuleNotFoundError: No module named 'halkalar'` alırsın.
Depodaki bir defteri değiştirmek istersen önce aynı klasörde yeni bir adla kopyala, kopyada çalış; böylece `git pull`
çakışmaz.

## Anahtar gerekiyor mu?

Isınma, Adım 3, Adım 4 ve alıştırma defteri anahtar istemez. Adım 1, Adım 2 ve Bonus `anahtar.txt` ister (bütün
konular için tek dosya, `gita3111` klasöründe; Konu 2). Defter 1 görsel okuma ve 1 metin isteği gönderir (Bonus 1 istek
daha); Adım 1 ve 2'yi yeniden çalıştırmak yeni istek göndermez. Hepsi ücretsiz günlük kotanın küçük bir kısmıdır.
Anahtarın yoksa Adım 1, 2 ve 5'i hocanın paylaştığı ekrandan izle.
