# Konu 12 — Araç Kullanımı: Modelin Karar Verdiği Program

Bu konuda bir kararı modele bırakıyoruz. Önce modelden serbest bir paragraf yerine **alanları belli** bir cevap
(JSON) istemeyi öğreneceksin. Sonra kullanıcının serbest cümlesine bakıp iki araçtan hangisinin gerektiğine
(yeni görsel üret ya da elimizdeki fincan fotoğrafını düzenle) modelin karar vermesini sağlayacaksın; kararı
uygulayan senin yazdığın program olacak. Modelin kararlarını kendi etiketlerinle karşılaştırıp **ölçecek**, araçların
tarifini netleştirip yeniden ölçeceksin. Sonunda serbest cümleyle çalışan küçük bir araç elinde olacak.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Kavram slaytları; dersin başında gösterilir |
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–8 ve Bonus |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: bozuk kodlar ve boşluklu sorular (anahtar istemez, internete çıkmaz) |
| `gorsel_araclari.py` | Yardımcı dosya: modelin seçeceği iki aracın fonksiyonları, `ciz` (yeni görsel; modelin gördüğü adı `uret`) ve `duzenle` (görsel düzenleme); ödev için `metin_yaz` |
| `veri/fincan.jpg` | Elimizdeki görsel: `duzenle` bunu değiştirir (Konu 8'deki fincan) |
| `veri/kararlar.json` | Alıştırmanın el yapımı örnek kararları |
| `odevler/odev12.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu — adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |

Üretilen ve düzenlenen görseller bu klasörde `ciktilar/` içine yazılır (`karar_1.jpg`, `istek_0.jpg` gibi).

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

Defterin kopyası `gorsel_araclari.py` ile **aynı klasörde** durmalı; yoksa
`ModuleNotFoundError: No module named 'gorsel_araclari'` alırsın.

## Anahtar gerekiyor mu?

Isınma anahtarsız; alıştırma defteri de. Adım 1'den sonrası `anahtar.txt` ister (bütün konular için tek dosya,
`gita3111` klasöründe). Defterin tamamı metin modeline yaklaşık 33 istek gönderir ve en fazla 5 görsel üretir;
günlük ücretsiz kotanın %10'undan az. Anahtarın yoksa yanındakiyle birlikte, onun ekranında izle.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı
değiştirmek istersen önce aynı klasörde **yeni bir adla kopyala**, kopyada çalış; böylece
`git pull` hiç çakışmaz.

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Anahtar |
|---|---|---|
| Isınma | Altı isteğe önce kendin karar vermek (`uret` mi, `duzenle` mi) | gerekmez |
| Adım 1 | Araçlar, metin modeli, elimizdeki görsel | gerekir |
| Adım 2 | JSON modu: alanları belli cevap (`response_format`) | gerekir |
| Adım 3 | Metin artık veri: beş slogan kartı, süzmek, alanın değerini sınırlamak | gerekir |
| Adım 4 | Karar da bir alan: model `arac` ve `yonerge` gönderir | gerekir |
| Adım 5 | Program kararı uygular (`if / elif / else`) | gerekir |
| Adım 6 | Model ne kadar doğru seçiyor? (görsel üretmez) | gerekir |
| Adım 7 | Tarifi netleştirmek; yeni isteklerle yeniden ölçmek (görsel üretmez) | gerekir |
| Adım 8 | Serbest cümleyle çalışan araç; durma koşulu | gerekir |
| Bonus | Gerçek `tools` alanı (hoca gösterimi) | gerekir |
