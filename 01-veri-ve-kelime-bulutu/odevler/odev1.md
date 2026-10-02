# Konu 1 Ödevi — Kendi Metninin Kelime Bulutu

**Puan yok.** Bir sonraki derste 2-3 kişi ekranda gösterecek; sıra listesi ilan edildi.

## Yapılacak

Kendi seçtiğin bir Türkçe metinle kelime bulutu üret. Metin ne olabilir:

- Sevdiğin bir şarkının sözleri
- Kendi yazdığın bir şey (ödev, blog yazısı, günlük)
- Bir markanın son 20 sosyal medya gönderisi (kopyala yapıştır)
- Bir haber sitesinden birkaç yazı

En az 300 kelime olsun, yoksa bulut boş görünür.

## Teslim edeceğin iki görsel

1. **Durak kelimeler elenmeden** üretilmiş bulut
2. **Durak kelimeler elendikten sonra** üretilmiş bulut

## Cevaplayacağın tek soru

İki görsel arasındaki farka bak ve bir cümle yaz:

> Eleme yapmadan önce en büyük görünen kelimeler neydi, sonra ne oldu?

## Nasıl yapılır

1. Metnini bir `.txt` dosyası olarak `veri` klasörüne kaydet (ör. adı benim-metnim.txt olsun).
2. `ders.ipynb`'yi aynı klasörde yeni bir adla kopyala (ör. `odev1.ipynb`); depodaki
   defteri değiştirmezsen `git pull` çakışmaz. Kopyayı VS Code'da aç, çekirdek `.venv`.
3. Adım 1'in hücresinde `"veri/kafe-yorumlari.txt"` yolunu kendi metninin yoluna çevir.
4. Adım 3'teki `print(sayac["sessiz"])` satırını sil (senin metninde "sessiz" olmayabilir).
5. Hücreleri sırayla **Adım 6'ya kadar** çalıştır. Bulut, elemeli olanı.
6. Bulut hücresinde `bulut.to_image()` satırının **üstüne** şu satırı ekle ve hücreyi yeniden
   çalıştır; görsel klasörde bir dosya olarak da oluşur:

   ```
   bulut.to_file("elemeli.png")
   ```

**Elemesiz bulut için:** Adım 5'te durak kelimeleri okuyan hücreden sonra yeni bir hücre
aç, içine `durak_kelimeler = []` yaz ve çalıştır (liste boşaldı, hiçbir kelime elenmez).
Ardından eleme yapan sayaç hücresini, sıralama hücresini ve bulut hücresini yeniden çalıştır;
bu kez eklediğin satırdaki dosya adını `"elemesiz.png"` yap.

## Takılırsan

Çalışmayan kodu getir, sorun değil. **Hiç denememiş gelmek** sorun.
Hata mesajının ekran görüntüsünü al, birlikte bakarız.
