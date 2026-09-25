# Konu 1 — Veriyi Kodla İşlemek

Bu klasörde ne var:

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `ornekler/` | Derste birlikte yazacağımız dosyalar, sırayla numaralı (00-10) |
| `veri/` | Üzerinde çalışacağımız metinler ve Türkçe durak kelime listesi |
| `alistirma/` | Derste kendi başına dolduracağın alıştırma |
| `odevler/odev1.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu: her adımın nedeni, sık hatalar, kendini dene soruları — derste kaçırdığın yer olursa buraya bak |

## Çalıştırma

Komutları **`gita3111` klasörünün içinden** çalıştır:

```
uv run 01-veri-ve-kelime-bulutu/ornekler/01_dosya_oku.py
```

Kütüphane eksik derse:

```
uv add wordcloud matplotlib
```

## Bu konuda ne üreteceksin

Bir metin dosyasından kelime bulutu. Önce kelimeleri sayacağız, sonra işe yaramaz
kelimeleri eleyeceğiz, sonra görseli üreteceğiz. Sonunda bulutun göremediği şeylere
(ekler, bağlam) bakıp aynı sonucu bir çubuk grafikle çizeceğiz.

## Dosyalar ne işe yarıyor

| Dosya | Ne zaman |
|---|---|
| `00_isinma.py` | Konunun başında, geçen dönemin iki hatası |
| `01` - `05` | Derste birlikte, sırayla |
| `06_iki_metin.py` | Bonus: aynı kod farklı metinde ne yapıyor |
| `07_bozuk_kodlar.py` | Alıştırma: beş bozuk kod, düzelt |
| `08_bulut_tasarimi.py` | Bonus: bulutun rengi, arka planı, kelime sayısı ve yönü |
| `09_kok_ve_baglam.py` | Derinleşme (notta Adım 8): ekli kelimeleri toplamak, kelimeyi yorumların içinde okumak |
| `10_cubuk_grafik.py` | Derinleşme (notta Adım 9): aynı sonucun `matplotlib` ile çubuk grafiği |

Erken bitirirsen `06` ve `08` senin için.
