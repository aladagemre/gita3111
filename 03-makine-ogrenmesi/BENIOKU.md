# Konu 3 — Makine Öğrenmesi Nedir?

Bu konuda kendi modelimizi eğiteceğiz. Veri: Konu 2'nin ödevinde senin ve arkadaşlarının
etiketlediği renkler. Konu tek bir derse sığmayabilir; bölünürse `ders_notu.md`'de
kaldığın adımdan devam et.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `ornekler/` | Derste birlikte yazacağımız ve çalıştıracağımız dosyalar (00-10) |
| `veri/renkler-etiketli.csv` | Sınıfın etiketleri, tek dosyada |
| `alistirma/` | Derste kendi başına dolduracağın alıştırma |
| `odevler/odev3.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu özeti — derste kaçırdığın yer olursa buraya bak |

## Kurulum

**Dersten önce** çalıştır, indirme biraz sürüyor:

```
uv add -r 03-makine-ogrenmesi/requirements.txt
```

Kurulacak kütüphanelerin listesi bu klasördeki `requirements.txt` dosyasında.

## Çalıştırma

Komutları `gita3111` klasörünün içinden:

```
uv run 03-makine-ogrenmesi/ornekler/01_veriyi_oku.py
```

## Dosyalar

| Dosya | Ne zaman |
|---|---|
| `00_isinma.py` | Ders başında, CSV satırını sözlüğe çevirme |
| `01_veriyi_oku.py` | Sınıfın verisine bakmak: dağılım, anlaşmazlık, tavan |
| `02_ozellik_etiket.py` | Rengi sayıya çevirmek |
| `03_egitim_test.py` | Veriyi ikiye bölmek |
| `04_model_egit.py` | Modeli eğitmek ve ölçmek |
| `05_yanilgilari_gor.py` | Modelin yanıldığı renkler |
| `06_veri_miktari.py` | Veri arttıkça doğruluk nasıl değişiyor |
| `07_bozuk_kodlar.py` | Alıştırma: beş bozuk kod |
| `08_kendi_rengin.py` | Bonus: kendi renklerini tahmin ettir |
| `09_modeli_yokla.py` | Adım 7: model ne öğrendi? Yeni renkler ve kafe paleti |
| `10_gorulmemis_renkler.py` | Adım 8: hiç görmediği renklerde dürüst sınav |
