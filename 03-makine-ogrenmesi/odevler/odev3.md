# Konu 3 Ödevi — Veri miktarı doğruluğu nasıl değiştiriyor?

**Puan yok.** Konu 4'ün başında sıradaki arkadaşlar gösterecek.

## Yapılacak

`ders.ipynb`'yi aynı klasörde yeni bir adla kopyala (ör. `ders-ayse.ipynb`), kopyayı aç
ve hücreleri baştan Adım 6'nın sonuna kadar sırayla çalıştır. Depodaki dosyaya
dokunmazsan `git pull` çakışmaz.

Adım 6'nın ilk hücresi her satırda iki sayı yazıyor: eğitim örneği sayısı ve doğruluk.
İki satıra bak:

1. Modeli **eğitim verisinin yarısıyla** (90 örnek) eğitince doğruluk kaç?
2. Modeli **tamamıyla** (180 örnek) eğitince doğruluk kaç?

Adım 6'nın ikinci hücresi grafiği çiziyor. Grafiği dosyaya kaydetmek için o hücrede
`plt.show()` satırının **üstüne** şu satırı ekle ve hücreyi yeniden çalıştır:

```py
plt.savefig("veri-miktari.png")
```

`veri-miktari.png` defterin yanına, konu klasörüne kaydedilir.

## Teslim edeceğin

- İki doğruluk oranı
- `veri-miktari.png` grafiği
- **Tek cümle:** aradaki fark ne, neden böyle olmuş olabilir?

## Dikkat

Eğri her zaman düzgün yükselmeyebilir; ortada düşebilir. Bu bir hata değil —
gördüğün şeyi yaz, düzeltmeye çalışma. Neden düştüğünü derste konuşacağız. İpucu için
`ders_notu.md`'nin Adım 6 bölümüne bak.

## İstersen (zorunlu değil)

Kopyandaki **Bonus** hücresine kendi seçtiğin 5 rengi sırayla yaz (RGB sayılarını renk
seçiciden al) ve modele tahmin ettir.

Modelle aynı fikirde misin? Ayrıldığınız bir renk varsa onu getir — sınıfça
bakalım, kim haklı?
