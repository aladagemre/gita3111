# Konu 8 — Koddan Görsel ve Toplu Üretim

Bu konuda önce Konu 7'deki işi koddan yapıyoruz: hazır `ciz` fonksiyonuyla bir görsel üretip dosyanın adını ve yerini
kendin seçiyorsun, yönergeyi kullanıcıya sorduruyorsun. Sonra arayüzün yapamadığı işe geçiyoruz: bir şablon ve iki
listeyle (3 stil × 4 renk) 12 görseli tek seferde üretmek. Döngüden önce kota hesabı yapacak, küçük bir denemeyle (3 görsel)
sınırın çalıştığını göreceksin. Yazdığın kod var olan görselleri atlayıp kaldığı yerden devam edecek, her görselin nasıl
üretildiğini bir JSON günlüğüne yazacak ve hepsini tek bir kontak sayfasında yan yana koyacak. Alıştırmada aynı döngüyü
ve kontak sayfasını kendi elinle yazacaksın.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Kavram slaytları; dersin başında gösterilir |
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–6 ve Bonus |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: kendin yazacağın iki soru, bozuk kodlar ve boşluklu sorular (anahtar istemez, görsel üretmez) |
| `uretim.py` | Yardımcı dosya: `ciz` ve `sabirli_ciz` (görseli üretip verdiğin yola kaydeder), `gorsele_sor` (görsel anlayan modele soru sormak). İçini okuman gerekmiyor |
| `veri/ornek_izgara/` | Alıştırmanın kontak sayfası için hazır dört görsel |
| `odevler/odev8.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu — adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |

Defterin çıktıları: tek görseller `ciktilar/` içine (`ilk.jpg`, `benim.jpg`); ızgara `izgara/` içine
(`suluboya_adacayi.jpg` gibi 12 görsel, `kontak_sayfasi.png`, `uretim_gunlugu.json`). Ödevin çıktıları `odev8/` içine.
Bu klasörler depoya girmez.

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

Isınma anahtarsız; alıştırma defteri de. Adım 1'den sonrası `anahtar.txt` ister (bütün konular için tek dosya,
`gita3111` klasöründe). Defterin ana akışı 15 görsel üretir; Bonus ile en fazla 21 görsel ve görsel anlayan modele
13 soru. Hepsi ücretsiz günlük kotanın küçük bir kısmı. Anahtarın yoksa yanındakiyle birlikte, onun ekranında izle.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı
değiştirmek istersen önce aynı klasörde **yeni bir adla kopyala**, kopyada çalış; böylece
`git pull` hiç çakışmaz. `ciktilar/`, `izgara/` ve `odev8/` depoya girmez; içlerini istediğin gibi değiştirebilirsin.

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Anahtar |
|---|---|---|
| Isınma | İç içe döngüyle kombinasyonları saymak | gerekmez |
| Adım 1 | Aynı iş koddan: tek görsel, `input` ile yönerge, üzerine yazma | gerekir |
| Adım 2 | Şablon: yönerge sözlükleri ve kartlar | istek yok |
| Adım 3 | Kota hesabı ve güvenlik sınırı | istek yok |
| Adım 4 | Toplu üretim: önce 3 görsellik deneme, sonra kalanı; var olanı atla, sınırda dur | gerekir |
| Adım 5 | Üretim günlüğü: kartları JSON'a yazmak | istek yok |
| Adım 6 | Kontak sayfası; kendi seçimin | istek yok |
| Bonus | Görselleri görsel anlayan modele puanlatmak; tohum ekseni; sınırı denemek | gerekir |
