# Konu 3 Ödevi — Veri miktarı doğruluğu nasıl değiştiriyor?

**Puan yok.** Konu 4'ün başında sıradaki arkadaşlar gösterecek.

## Yapılacak

`06_veri_miktari.py` dosyasını çalıştır ve çıkan grafiğe bak.

Sonra iki ölçüme bak:

1. Modeli **eğitim verisinin yarısıyla** eğitince doğruluk kaç?
2. Modeli **tamamıyla** eğitince doğruluk kaç?

İkisi de dosyanın çıktısında var: ilk liste eğitim örneği sayıları, ikinci liste
doğruluklar. Yarısı üçüncü sırada (%50), tamamı en sonda (%100).

Kodu değiştireceksen önce dosyayı `ornekler` klasöründe yeni bir adla kopyala, kopyada
değiştir; depodaki dosyaya dokunmazsan `git pull` çakışmaz. Komutları konunun
klasöründen ver (`cd 03-makine-ogrenmesi`, sonra `uv run ornekler/...`).

## Teslim edeceğin

- İki doğruluk oranı
- `veri-miktari.png` grafiği
- **Tek cümle:** aradaki fark ne, neden böyle olmuş olabilir?

## Dikkat

Eğri her zaman düzgün yükselmeyebilir; ortada düşebilir. Bu bir hata değil —
gördüğün şeyi yaz, düzeltmeye çalışma. Neden düştüğünü derste konuşacağız. İpucu için `ders_notu.md`'nin Adım 6 bölümüne bak.

## İstersen (zorunlu değil)

`08_kendi_rengin.py` dosyasını yeni bir adla kopyala, kopyaya kendi seçtiğin 5 rengi
ekle ve modele tahmin ettir.

Modelle aynı fikirde misin? Ayrıldığınız bir renk varsa onu getir — sınıfça
bakalım, kim haklı?
