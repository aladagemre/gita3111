# Konu 12 Ödevi — Üçüncü araç

**Puan yok.** Konu 13'ün başında sıradaki arkadaşlar gösterecek. Araç kullanımı final projesi için **zorunlu değil**;
bu ödev, projende kullanmak istersen elinde çalışan bir örnek olsun diye.

Bu ödev kendi `anahtar.txt` dosyanı ister (Konu 2). Ölçüm görsel üretmez: metin modeline yaklaşık 20 istek gönderir
(her biri yaklaşık 15 neuron; günlük kotanın %5'inden az). "İstersen" bölümü en fazla 3 görsel daha üretir.

---

## Ne yapacaksın?

Dersteki programa üçüncü bir araç ekliyorsun: `metin_yaz`. `gorsel_araclari.py`'de hazır duruyor: bir yönerge alır,
dil modelinin yazdığı metni verir (ör. bir afiş sloganı, bir ürün açıklaması).

1. `ders.ipynb`'yi aynı klasörde yeni bir adla kopyala (ör. `odev12-ayse.ipynb`).
2. Adım 1'in ilk hücresindeki son satırın sonuna `, metin_yaz` ekle:
   `from gorsel_araclari import ciz, duzenle, adres, basliklar, metin_yaz`.
3. **Kendi istekleri.** Isınma hücresinde `istekler` listesini kendi projene göre değiştir: **en az 6** istek; en az
   ikisi metin istesin (ör. "afişin altına iki satırlık bir açıklama yaz"), en az biri bilerek muğlak olsun.
   `etiketlerim` listesine her isteğin doğru aracını aynı sırayla yaz: `"uret"`, `"duzenle"` ya da `"metin_yaz"`.
   `print(len(istekler), len(etiketlerim))` aynı sayıyı yazmalı.
4. **Üç aracın tarifi.** Adım 4'teki `araclar` metnine üçüncü aracı ekle, ör.
   `"... metin_yaz: bir afiş ya da gönderi için kısa bir metin yazar."`
   Model aracın adını tariften öğrenir. `karar_ver`'de yalnızca bir yeri değiştir: `yonerge` açıklaması "görsel
   modeline gidecek kısa İngilizce yönerge" diyor; metin Türkçe olsun diye şöyle yaz:
   `yonerge (seçilen araca gidecek kısa yönerge; görsel için İngilizce, metin için Türkçe)`.
5. **Üçüncü dal.** Adım 5'teki `uygula` fonksiyonuna `else`'ten önce bir `elif` ekle (alıştırmanın Soru 5'i):
   ```
   elif arac == "metin_yaz":
       metin = metin_yaz(yonerge)
       print("Metin:", metin)
       return None
   ```
   Metin bir görsel değil; o yüzden dosyaya yazmadan yazdırıp fonksiyondan çıkıyoruz.
6. **Ölç.** Isınma'dan başlayıp Adım 6'nın sonuna kadar sırayla çalıştır. Adım 3'ü (slogan kartları) atlayabilirsin;
   Adım 2'nin `bicim` ve `json_sor` hücrelerini **çalıştırmalısın**. Adım 5'te klasör ve `uygula` hücrelerini çalıştır,
   sonraki dört hücreyi (iki örnek ve görselleri) istersen atla: görsel üretirler. `olc(araclar, istekler, etiketlerim)`
   sonucunu not et.
7. **Düzelt ve yeniden ölç.** Model en çok hangi istekte ayrıştı? Adım 7'deki gibi bir `yeni_araclar` tarifi yaz:
   her araç **ne zaman** seçilmeli, emin değilse ne yapmalı. Önce aynı isteklerle, sonra **en az 3 yeni** istekle
   (`yeni_istekler`, `yeni_etiketlerim`) yeniden ölç.

---

## Teslim edeceğin

1. Defterinin kopyası (`odev12-ayse.ipynb`), çıktılarıyla.
2. İki tarif (ilk ve düzeltilmiş) ve üç ölçüm sonucu (`Doğru: ... / ...`).
3. **İki cümle:** Model en çok hangi istekte ayrıştı? Tarifte neyi değiştirdin ve yeni isteklerde işe yaradı mı?
4. **Bir cümle:** Kendi final projende modelin vermesini isteyeceğin bir karar var mı, yoksa kararlar zaten belli mi?

`anahtar.txt`'yi **gönderme**; defterin içine de anahtar yazma.

---

## İstersen (zorunlu değil)

Adım 8'i çalıştır (Adım 7'deki `yeni_araclar` tarifini kullanır) ve `input` kutusuna üç araçtan her birini
seçtirecek birer istek yaz. Model üçünü de doğru seçti mi? (Görsel isteyen her tur bir görsel üretir.)
