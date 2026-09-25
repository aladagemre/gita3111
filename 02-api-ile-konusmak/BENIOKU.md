# Konu 2 — İnterneti Koddan Konuşturmak

Bu konuda kodun bilgisayarının dışına çıkıyor: bir soruyu uzaktaki bir modele
gönderip cevabını alacaksın. Konu 1'in bulgusundan (müşteriler kafeyi sessiz bir
çalışma yeri olarak anlatıyor) yola çıkıp modele o kafenin yeni kimliğini soracaksın.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `ornekler/` | Derste birlikte yazacağımız dosyalar (00-09) |
| `veri/` | Örnek sorular, kayıtlı yanıtlar (demo modu için), renk listesi |
| `alistirma/` | Derste kendi başına dolduracağın alıştırma |
| `odevler/odev2.md` | Bu konunun ödevi — iki parça |
| `ders_notu.md` | Konu notu — adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |

## Çalıştırma

Komutları **bu konunun klasörünün içinden** çalıştır. `gita3111` klasöründeysen önce
içeri gir, dersten önce kütüphaneleri indir (liste klasördeki `pyproject.toml`
dosyasında), sonra çalıştır:

```
cd 02-api-ile-konusmak
uv sync
uv run ornekler/02_ilk_istek.py
```

`uv sync`'i atlarsan ilk `uv run` kütüphaneleri kendisi indirir; sadece biraz bekletir.

`anahtar.txt` bütün konular için tek dosya: konu klasöründe değil, bir üstte,
`gita3111` klasörünün içinde durur. Kodlar onu `"../anahtar.txt"` yoluyla okur
(`..` = bir üst klasör).

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı
(örneğin bir alıştırmayı) değiştirmek istersen önce aynı klasörde **yeni bir adla
kopyala**, kopyada çalış; böylece `git pull` hiç çakışmaz.

## Anahtarın yoksa ne olacak?

Örneklerin çoğu **DEMO modunda** çalışır: `anahtar.txt` yoksa kayıtlı bir yanıtla
aynı şeyi gösterirler. Yani derse yetişebilirsin. Ama ödev için kendi anahtarın
gerekiyor — ders öncesi hazırlıktaki 5. adımı bugün bitir.

## Dosyalar

| Dosya | Ne zaman |
|---|---|
| `00_isinma.py` | Ders başında, iç içe sözlük provası |
| `01_anahtar_oku.py` | Anahtarı dosyadan okumak |
| `02_ilk_istek.py` | İlk istek, ham yanıt |
| `03_yaniti_coz.py` | Yanıtın içinden metni çekmek |
| `04_hata_kodlari.py` | 401, 429, 500 ne demek |
| `05_soru_sor.py` | Konunun hedef çıktısı |
| `06_coklu_soru.py` | Döngüyle beş soru, JSON kaydı |
| `07_bozuk_kodlar.py` | Alıştırma: beş bozuk kod |
| `08_cevap_raporu.py` | Bonus: cevaplardan kelime bulutu |
| `09_baglam_farki.py` | Adım 7: soruya bağlam yazmak cevabı nasıl değiştiriyor |
